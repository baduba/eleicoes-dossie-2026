#!/usr/bin/env python3
"""Fase 2 (A4, A5): processa os arquivos de urna (BU, RDV, assinatura, log) por secao a partir de zips locais ou remotos (range requests).
Uso local : python -I 08_arquivos_urna.py local ZIP ANO TURNO PARQUET_BWEB SAIDA.parquet
      remoto: python -I 08_arquivos_urna.py remoto URL UF ANO TURNO PARQUET_BWEB LISTA_SECOES.csv SAIDA.parquet [--threads 8]
Nenhum campo e usado sem validacao contra o BWeb (feita em f2_a4_a10.py)."""
import argparse, io, os, re, sys, zipfile
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urna_parse as U

NOME26 = re.compile(r"^o(\d{5})([a-z]{2})(\d{5})(\d{4})(\d{4})-(bu|rdv|imgbu|vota|log)\.(dat|vsc|jez)$")
NOME22 = re.compile(r"^o(\d{5})-(\d{5})(\d{4})(\d{4})\.(bu|rdv|imgbu|vscmr|logjez)$")
DIA = {(2026, 1): "04/10/2026", (2026, 2): "25/10/2026", (2022, 1): "02/10/2022", (2022, 2): "30/10/2022"}


def agrupa(nomes, ano):
    g = {}
    for n in nomes:
        b = n.split("/")[-1]
        if ano == 2026:
            m = NOME26.match(b)
            if m:
                key = (m.group(2).upper(), int(m.group(3)), int(m.group(4)), int(m.group(5))); g.setdefault(key, {})[m.group(6)] = n
        else:
            m = NOME22.match(b)
            if m:
                key = (None, int(m.group(2)), int(m.group(3)), int(m.group(4))); ext = {"vscmr": "vota", "logjez": "log"}.get(m.group(5), m.group(5)); g.setdefault(key, {})[ext] = n
    return g


def secao(arqs, ano, turno, nominal):
    """arqs: dict {bu, rdv, imgbu, vota, log: bytes}"""
    r = {}
    try:
        bu = U.bu_campos(arqs["bu"])
        c1 = bu["cargos"].get(1, [])
        r.update(bu_comp=bu["comparecimento"], bu_aptos=bu["aptos"], bu_emissao=bu["emissao"], bu_carga24=bu["carga24"],
                 bu_lula=sum(q for t, q, pn in c1 if t == 1 and pn and pn[1] == 13), bu_dir=sum(q for t, q, pn in c1 if t == 1 and pn and pn[1] == 22),
                 bu_branco=sum(q for t, q, pn in c1 if t == 2), bu_nulo=sum(q for t, q, pn in c1 if t == 3), bu_n_cargos=len(bu["cargos"]),
                 bu_total_cargo1=sum(q for t, q, pn in c1))
    except Exception as e:                                           # noqa: BLE001
        r["erro_bu"] = f"{type(e).__name__}: {e}"
    try:
        rd = U.rdv_cargos(arqs["rdv"]).get(1)
        if rd is None:
            r["erro_rdv"] = "cargo 1 ausente no RDV"
        else:
            r.update(rdv_total=sum(rd.values()), rdv_lula=sum(v for (e, n), v in rd.items() if n == "13"), rdv_dir=sum(v for (e, n), v in rd.items() if n == "22"),
                     rdv_outros_numeros=sum(v for (e, n), v in rd.items() if n not in ("13", "22")), rdv_enums=";".join(f"{e}:{v}" for e, v in sorted(Counter_(rd).items())),
                     rdv_sem_numero=sum(v for (e, n), v in rd.items() if n == ""), rdv_enum_sem_numero=";".join(f"{e}:{v}" for (e, n), v in sorted(rd.items()) if n == ""))
    except Exception as e:                                           # noqa: BLE001
        r["erro_rdv"] = f"{type(e).__name__}: {e}"
    try:
        r.update(U.vsc_checa(arqs["vota"], {"bu": arqs["bu"], "rdv": arqs["rdv"], "imgbu": arqs["imgbu"], "log": arqs["log"]}))
    except Exception as e:                                           # noqa: BLE001
        r["erro_vsc"] = f"{type(e).__name__}: {e}"
    try:
        r.update(U.log_metricas(U.ler_log(arqs["log"]), nominal, DIA[(ano, turno)]))
    except Exception as e:                                           # noqa: BLE001
        r["erro_log"] = f"{type(e).__name__}: {e}"
    return r


def Counter_(rd):
    from collections import Counter
    c = Counter()
    for (e, n), v in rd.items():
        c[e] += v
    return c


def nominal_map(bweb_parquet):
    d = pd.read_parquet(bweb_parquet, columns=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "ab_nominal_min"])
    return {(r.SG_UF, r.CD_MUNICIPIO, r.NR_ZONA, r.NR_SECAO): r.ab_nominal_min + 540 for r in d.itertuples()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("modo"); ap.add_argument("args", nargs="+"); ap.add_argument("--threads", type=int, default=8)
    a = ap.parse_args()
    if a.modo == "local":
        zp, ano, turno, bweb, saida = a.args[0], int(a.args[1]), int(a.args[2]), a.args[3], a.args[4]
        uf = os.path.basename(zp).split("_")[-1][:2].upper()
        nom = nominal_map(bweb)
        z = zipfile.ZipFile(zp); g = agrupa(z.namelist(), ano)
        linhas = []
        for key, f in g.items():
            if set(f) != {"bu", "rdv", "imgbu", "vota", "log"}:
                linhas.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], erro_arquivos=f"incompleto: {sorted(f)}")); continue
            arqs = {k: z.read(v) for k, v in f.items()}
            kk = (uf, key[1], key[2], key[3])
            linhas.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], **secao(arqs, ano, turno, nom.get(kk, 17 * 60)), nominal_conhecido=kk in nom))
        pd.DataFrame(linhas).to_parquet(saida, index=False); print(saida, len(linhas))
    else:
        from remotezip import RemoteZip
        url, uf, ano, turno, bweb, lista, saida = a.args[0], a.args[1], int(a.args[2]), int(a.args[3]), a.args[4], a.args[5], a.args[6]
        nom = nominal_map(bweb)
        want = pd.read_csv(lista)
        wk = set(zip(want.cd_municipio, want.zona, want.secao))
        rz0 = RemoteZip(url); nomes = rz0.namelist(); g = {k: f for k, f in agrupa(nomes, ano).items() if (k[1], k[2], k[3]) in wk}
        rz0.close()
        print(f"{uf}: {len(g)} secoes encontradas de {len(wk)} pedidas", flush=True)
        keys = list(g)
        def trabalha(chunk):
            rz = RemoteZip(url); out = []
            for key in chunk:
                f = g[key]
                if set(f) != {"bu", "rdv", "imgbu", "vota", "log"}:
                    out.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], erro_arquivos=f"incompleto: {sorted(f)}")); continue
                arqs = {k: rz.read(v) for k, v in f.items()}
                kk = (uf, key[1], key[2], key[3])
                out.append(dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], **secao(arqs, ano, turno, nom.get(kk, 17 * 60)), nominal_conhecido=kk in nom))
            rz.close(); return out
        n = a.threads; chunks = [keys[i::n] for i in range(n)]
        res = []
        with ThreadPoolExecutor(n) as ex:
            for r in ex.map(trabalha, chunks):
                res += r
        pd.DataFrame(res).to_parquet(saida, index=False); print(saida, len(res))


if __name__ == "__main__":
    main()
