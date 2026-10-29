#!/usr/bin/env python3
"""Fase 2 (A11): votos nominais por candidato e por secao no 1o turno (Presidente). Uso: python -I 12_candidatos_t1.py DIR_ZIPS DIR_SAIDA ANO [--procs 4]"""
import glob, os, re, sys, zipfile
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
NOME = re.compile(r"(?i)^bweb_1t_([A-Z]{2})_\d{4}(\d{4})\d{4,6}\.zip$")


def proc(zp):
    z = zipfile.ZipFile(zp); nome = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
    with z.open(nome) as f:
        hdr = [c.replace(" ", "") for c in pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns]
    need = KEY + ["CD_CARGO_PERGUNTA", "CD_TIPO_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS"]
    falt = [c for c in need if c not in hdr]
    if falt:
        raise SystemExit(f"ERRO {zp}: colunas ausentes {falt}")
    out = []
    with z.open(nome) as f:
        for ch in pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, chunksize=500_000, header=0, names=hdr, usecols=need):
            ch = ch[(ch.CD_CARGO_PERGUNTA == "1") & (ch.CD_TIPO_VOTAVEL == "1")]
            ch["v"] = pd.to_numeric(ch.QT_VOTOS, errors="coerce").fillna(0)
            ch["NR_VOTAVEL"] = pd.to_numeric(ch.NR_VOTAVEL, errors="coerce")
            for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"):
                ch[c] = pd.to_numeric(ch[c], errors="coerce")
            out.append(ch.groupby(KEY + ["NR_VOTAVEL"])["v"].sum().reset_index())
    return pd.concat(out).groupby(KEY + ["NR_VOTAVEL"], as_index=False)["v"].sum()


def main(zdir, saida, ano, procs=4):
    zips = [z for z in glob.glob(os.path.join(zdir, "*.zip")) if NOME.match(os.path.basename(z)) and NOME.match(os.path.basename(z)).group(2) == str(ano)]
    if len(zips) != 28:
        raise SystemExit(f"ERRO: esperava 28 zips de 1o turno de {ano}, achei {len(zips)}")
    with ProcessPoolExecutor(procs) as ex:
        d = pd.concat(list(ex.map(proc, zips)), ignore_index=True)
    w = d.pivot_table(index=KEY, columns="NR_VOTAVEL", values="v", aggfunc="sum", fill_value=0)
    w.columns = [f"v{int(c)}" for c in w.columns]
    os.makedirs(saida, exist_ok=True)
    w.reset_index().to_parquet(os.path.join(saida, f"cand_t1_{ano}.parquet"), index=False)
    print(ano, w.shape, {c: int(w[c].sum()) for c in w.columns[:20]})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[5]) if len(sys.argv) > 5 else 4)
