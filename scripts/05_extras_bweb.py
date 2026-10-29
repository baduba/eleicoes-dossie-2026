#!/usr/bin/env python3
"""Fase 2: extrai do BWeb (todos os cargos) (a) totais por secao x cargo e tipo de votavel (A8) e (b) identificacao da carga/urna da secao (A10).
Uso: python -I 05_extras_bweb.py DIR_ZIPS DIR_SAIDA --anos 2022 2026 [--procs 4]
Saidas: cargos_{ano}_t{t}.parquet, carga_{ano}_t{t}.parquet. Coluna obrigatoria ausente => ERRO."""
import argparse, glob, os, re, sys, zipfile
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd

NOME = re.compile(r"(?i)^bweb_(\d)t_([A-Z]{2})_\d{4}(\d{4})\d{4,6}\.zip$")
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
OBRIG = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "QT_COMPARECIMENTO", "CD_TIPO_VOTAVEL", "QT_VOTOS", "NR_URNA_EFETIVADA",
         "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA"]
FLASH = ["CD_FLASHCARD_URNA_EFETIVADA", "CD_FLASCARD_URNA_EFETIVADA"]


def proc(zpath):
    m = NOME.match(os.path.basename(zpath))
    ano, turno = int(m.group(3)), int(m.group(1))
    with zipfile.ZipFile(zpath) as z:
        nome = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(nome) != 1:
            raise SystemExit(f"ERRO {zpath}: csv {nome}")
        with z.open(nome[0]) as f:
            hdr = [c.replace(" ", "") for c in pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns]
        falt = [c for c in OBRIG if c not in hdr]
        fl = [c for c in FLASH if c in hdr]
        if falt or not fl:
            raise SystemExit(f"ERRO {zpath}: colunas ausentes {falt} flashcard={fl}")
        cols = OBRIG + [fl[0]]
        agg, car = [], []
        with z.open(nome[0]) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, chunksize=500_000, header=0, names=hdr, usecols=cols):
                ch["v"] = pd.to_numeric(ch.QT_VOTOS, errors="coerce").fillna(0)
                ch["tv"] = pd.to_numeric(ch.CD_TIPO_VOTAVEL, errors="coerce").fillna(-1).astype(int)
                for t_ in (1, 2, 3, 4, 5):
                    ch[f"t{t_}"] = np.where(ch.tv == t_, ch.v, 0)
                ch["tout"] = np.where(~ch.tv.isin([1, 2, 3, 4, 5]), ch.v, 0)
                g = ch.groupby(KEY + ["CD_CARGO_PERGUNTA"], sort=False).agg(t1=("t1", "sum"), t2=("t2", "sum"), t3=("t3", "sum"), t4=("t4", "sum"), t5=("t5", "sum"),
                                                                           tout=("tout", "sum"), comp=("QT_COMPARECIMENTO", "first")).reset_index()
                agg.append(g)
                p = ch[ch.CD_CARGO_PERGUNTA == "1"].drop_duplicates(KEY)
                car.append(p[KEY + ["NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA", fl[0], "DT_CARGA_URNA_EFETIVADA"]].rename(columns={fl[0]: "CD_FLASHCARD"}))
    a = pd.concat(agg, ignore_index=True)
    a = a.groupby(KEY + ["CD_CARGO_PERGUNTA"], as_index=False).agg(t1=("t1", "sum"), t2=("t2", "sum"), t3=("t3", "sum"), t4=("t4", "sum"), t5=("t5", "sum"), tout=("tout", "sum"), comp=("comp", "first"))
    a["ano"], a["turno"] = ano, turno
    c = pd.concat(car, ignore_index=True).drop_duplicates(KEY)
    c["ano"], c["turno"] = ano, turno
    return a, c


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("zips"); ap.add_argument("saida"); ap.add_argument("--anos", type=int, nargs="+", required=True); ap.add_argument("--procs", type=int, default=4)
    a = ap.parse_args(); os.makedirs(a.saida, exist_ok=True)
    zips = [z for z in glob.glob(os.path.join(a.zips, "*.zip")) if NOME.match(os.path.basename(z)) and int(NOME.match(os.path.basename(z)).group(3)) in a.anos]
    zips.sort(key=os.path.getsize, reverse=True)
    if len(zips) != 56 * len(a.anos):
        raise SystemExit(f"ERRO: esperava {56*len(a.anos)} zips, achei {len(zips)}")
    A, C = [], []
    with ProcessPoolExecutor(a.procs) as ex:
        for i, (x, y) in enumerate(ex.map(proc, zips), 1):
            A.append(x); C.append(y); print(f"[{i}/{len(zips)}] ok", flush=True)
    A = pd.concat(A, ignore_index=True); C = pd.concat(C, ignore_index=True)
    for (ano, t), g in A.groupby(["ano", "turno"]):
        g.to_parquet(os.path.join(a.saida, f"cargos_{ano}_t{t}.parquet"), index=False)
    for (ano, t), g in C.groupby(["ano", "turno"]):
        g.to_parquet(os.path.join(a.saida, f"carga_{ano}_t{t}.parquet"), index=False)
    print("fim", len(A), len(C))


if __name__ == "__main__":
    main()
