#!/usr/bin/env python3
"""A34 (Adendo 16): duracao do voto por eleitor a partir do log da urna (so o arquivo de log; nenhum identificador de eleitor ou mesario e lido ou gravado).
Para cada habilitacao ("Eleitor foi habilitado"): duracao ate o primeiro "Voto confirmado para [Presidente]" seguinte, sem outra habilitacao no meio.
Tambem grava o intervalo do lado errado (voto confirmado ate a proxima habilitacao), usado so como placebo de forma.
Saida: uma linha por secao e dia (1 = 1o turno, 2 = 2o turno) com `dur` (segundos, uma por voto pareado) e `gap` (segundos, lado errado).
Uso local : python -I 45_a34_extrai_duracoes.py local ZIP UF ANO SAIDA.parquet
      remoto: python -I 45_a34_extrai_duracoes.py remoto URL UF ANO LISTA_SECOES.csv SAIDA.parquet [--threads 12]"""
import argparse
import importlib.util
import os
import sys
import zipfile
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import urna_parse as U

spec = importlib.util.spec_from_file_location("au08", os.path.join(AQUI, "08_arquivos_urna.py"))
au = importlib.util.module_from_spec(spec); spec.loader.exec_module(au)

DIAS = {2026: {1: "04/10/2026", 2: "25/10/2026"}, 2022: {1: "02/10/2022", 2: "30/10/2022"}}
M_HAB, M_CONF = "Eleitor foi habilitado", "Voto confirmado para [Presidente]"


def duracoes(linhas, ano):
    """Retorna {dia: dict(dur, gap, n_hab, n_conf, n_sem_voto, n_neg)}; ordem das linhas = ordem do log."""
    dia_de = {d: t for t, d in DIAS[ano].items()}
    out = {t: dict(dur=[], gap=[], n_hab=0, n_conf=0, n_sem_voto=0, n_neg=0) for t in (1, 2)}
    pend = None            # (dia, data, segundos) da habilitacao pendente
    ult_conf = None        # (dia, data, segundos) do ultimo voto confirmado ainda sem proxima habilitacao
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5:
            continue
        msg = p[4]
        if msg != M_HAB and msg != M_CONF:
            continue
        data = p[0][:10]; t = dia_de.get(data)
        if t is None:
            continue
        s = int(p[0][11:13]) * 3600 + int(p[0][14:16]) * 60 + int(p[0][17:19])
        o = out[t]
        if msg == M_HAB:
            o["n_hab"] += 1
            if pend is not None:
                out[pend[0]]["n_sem_voto"] += 1
            if ult_conf is not None and ult_conf[1] == data:
                g = s - ult_conf[2]
                if g >= 0:
                    o["gap"].append(g)
            ult_conf = None
            pend = (t, data, s)
        else:
            o["n_conf"] += 1
            if pend is not None and pend[1] == data:
                d = s - pend[2]
                if d >= 0:
                    o["dur"].append(d)
                else:
                    o["n_neg"] += 1
                pend = None
                ult_conf = (t, data, s)
    if pend is not None:
        out[pend[0]]["n_sem_voto"] += 1
    return out


def linhas_secao(uf, key, logbytes, ano):
    seq = duracoes(U.ler_log(logbytes), ano)
    return [dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=t, **o) for t, o in seq.items()]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("modo"); ap.add_argument("args", nargs="+"); ap.add_argument("--threads", type=int, default=12)
    a = ap.parse_args()
    rows = []
    if a.modo == "local":
        zp, uf, ano, saida = a.args[0], a.args[1], int(a.args[2]), a.args[3]
        z = zipfile.ZipFile(zp)
        for key, f in au.agrupa(z.namelist(), ano).items():
            if "log" not in f:
                rows.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=0, erro="sem log")); continue
            try:
                rows += linhas_secao(uf, key, z.read(f["log"]), ano)
            except Exception as e:                               # noqa: BLE001
                rows.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=0, erro=f"{type(e).__name__}: {e}"))
    else:
        from concurrent.futures import ThreadPoolExecutor
        from remotezip import RemoteZip
        url, uf, ano, lista, saida = a.args[0], a.args[1], int(a.args[2]), a.args[3], a.args[4]
        want = pd.read_csv(lista)
        wk = set(zip(want.cd_municipio, want.zona, want.secao))
        rz0 = RemoteZip(url); g = {k: f for k, f in au.agrupa(rz0.namelist(), ano).items() if (k[1], k[2], k[3]) in wk}; rz0.close()
        print(f"{uf} {ano}: {len(g)} secoes encontradas de {len(wk)} pedidas", flush=True)
        keys = list(g)

        def trabalha(chunk):
            rz = RemoteZip(url); out = []
            for key in chunk:
                f = g[key]
                if "log" not in f:
                    out.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=0, erro="sem log")); continue
                try:
                    out += linhas_secao(uf, key, rz.read(f["log"]), ano)
                except Exception as e:                           # noqa: BLE001
                    out.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=0, erro=f"{type(e).__name__}: {e}"))
            rz.close()
            return out
        chunks = [keys[i::a.threads] for i in range(a.threads)]
        with ThreadPoolExecutor(a.threads) as ex:
            for r in ex.map(trabalha, chunks):
                rows += r
    d = pd.DataFrame(rows)
    for c in ("dur", "gap"):
        if c in d:
            d[c] = d[c].map(lambda x: list(x) if isinstance(x, list) else None)
    d.to_parquet(saida, index=False)
    print(saida, len(d), "linhas;", int(d.get("erro", pd.Series(dtype=object)).notna().sum()), "erros", flush=True)


if __name__ == "__main__":
    main()
