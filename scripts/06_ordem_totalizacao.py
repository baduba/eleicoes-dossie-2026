#!/usr/bin/env python3
"""Fase 2 (A1): extrai de detalhe_votacao_secao o horario de recebimento do BU e da primeira totalizacao parcial por secao (cargo Presidente).
Uso: python -I 06_ordem_totalizacao.py DIR_ZIPS DIR_SAIDA 2018 2022 2026   (2014 nao tem esses campos: ERRO explicito se pedido)"""
import os, sys, zipfile
import pandas as pd
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
COLS = KEY + ["NR_TURNO", "CD_CARGO", "DT_RECEBIMENTO_BU_HOR_TSE", "DT_PRIM_TOT_PARCIAL_HOR_TSE"]


def main(zdir, saida, anos):
    os.makedirs(saida, exist_ok=True)
    for ano in anos:
        z = zipfile.ZipFile(os.path.join(zdir, f"detalhe_votacao_secao_{ano}.zip"))
        nome = [n for n in z.namelist() if n.upper().endswith("_BR.CSV")]
        with z.open(nome[0]) as f:
            hdr = pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns
        falt = [c for c in COLS if c not in hdr]
        if falt:
            raise SystemExit(f"ERRO {ano}: o produto detalhe_votacao_secao nao tem {falt}; A1 nao pode ser executado para {ano}")
        partes = []
        with z.open(nome[0]) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", usecols=COLS, chunksize=500_000):
                partes.append(ch[ch.CD_CARGO == 1].drop(columns="CD_CARGO"))
        d = pd.concat(partes, ignore_index=True)
        for c in ("DT_RECEBIMENTO_BU_HOR_TSE", "DT_PRIM_TOT_PARCIAL_HOR_TSE"):
            d[c] = pd.to_datetime(d[c], format="%d/%m/%Y %H:%M:%S", errors="coerce")
        for t, g in d.groupby("NR_TURNO"):
            g = g.drop(columns="NR_TURNO").drop_duplicates(KEY)
            p = os.path.join(saida, f"ordem_{ano}_t{t}.parquet"); g.to_parquet(p, index=False)
            print(p, len(g), "sem hora de 1a totalizacao:", int(g.DT_PRIM_TOT_PARCIAL_HOR_TSE.isna().sum()), "| min", g.DT_PRIM_TOT_PARCIAL_HOR_TSE.min(), "| max", g.DT_PRIM_TOT_PARCIAL_HOR_TSE.max())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]])
