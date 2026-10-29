#!/usr/bin/env python3
"""A32 (Adendo 11), item 1: sequencia de habilitacoes por secao-dia a partir do log da urna (so o arquivo de log; nenhum identificador de eleitor ou mesario e lido ou gravado).
Saida: uma linha por secao e dia (1 = 1o turno, 2 = 2o turno) com `ts` (segundos desde 00:00, horario da urna) e `tp` (uma letra por habilitacao: M manual, B biometrica, O outra).
O log do 2o turno contem os eventos dos dois dias; cada log lido da T1 e T2 da mesma urna.
Uso local : python -I 38_a32_extrai_logs.py local ZIP UF ANO SAIDA.parquet
      remoto: python -I 38_a32_extrai_logs.py remoto URL UF ANO LISTA_SECOES.csv SAIDA.parquet [--threads 12]"""
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
M_HAB, M_BIO, M_REQ, M_MES = "Eleitor foi habilitado", "Tipo de habilitação do eleitor [biométrica]", "Solicitação de dado pessoal do eleitor para habilitação manual", "habilitou o eleitor"


def sequencias(linhas, ano):
    dia_de = {d: t for t, d in DIAS[ano].items()}
    out = {1: ([], []), 2: ([], [])}
    flag_m = flag_b = False
    n = 0
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5:
            continue
        n += 1
        msg = p[4]
        if msg == M_HAB:
            t = dia_de.get(p[0][:10])
            if t is not None:
                hh, mm, ss = int(p[0][11:13]), int(p[0][14:16]), int(p[0][17:19])
                out[t][0].append(hh * 3600 + mm * 60 + ss)
                out[t][1].append("M" if flag_m else ("B" if flag_b else "O"))
            flag_m = flag_b = False
        elif msg == M_BIO:
            flag_b = True
        elif msg == M_REQ or msg.endswith(M_MES):
            flag_m = True
    return out, n


def linhas_secao(uf, key, logbytes, ano):
    seq, n = sequencias(U.ler_log(logbytes), ano)
    return [dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, dia=t, n_linhas=n, n_hab=len(ts), ts=ts, tp="".join(tp)) for t, (ts, tp) in seq.items()]


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
    if "ts" in d:
        d["ts"] = d.ts.map(lambda x: list(x) if isinstance(x, list) else None)
    d.to_parquet(saida, index=False)
    print(saida, len(d), "linhas;", int(d.get("erro", pd.Series(dtype=object)).notna().sum()), "erros", flush=True)


if __name__ == "__main__":
    main()
