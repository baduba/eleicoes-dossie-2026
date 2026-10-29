#!/usr/bin/env python3
"""Extrai o modelo da urna por secao e turno (CD_MODELO_URNA) dos zips detalhe_votacao_secao, para controle de red team.
Uso: python -I 01c_modelo_urna.py DIR_ZIPS DIR_SAIDA 2022 2026"""
import os, sys, zipfile
import pandas as pd

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
COLS = KEY + ["NR_TURNO", "CD_CARGO", "CD_MODELO_URNA"]


def main(zdir, saida, anos):
    os.makedirs(saida, exist_ok=True)
    for ano in anos:
        z = zipfile.ZipFile(os.path.join(zdir, f"detalhe_votacao_secao_{ano}.zip"))
        nome = [n for n in z.namelist() if n.upper().endswith("_BR.CSV")]
        if len(nome) != 1:
            raise SystemExit(f"ERRO: esperava 1 *_BR.csv em {ano}: {nome}")
        with z.open(nome[0]) as f:
            hdr = pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns
        falt = [c for c in COLS if c not in hdr]
        if falt:
            raise SystemExit(f"ERRO {ano}: colunas ausentes {falt}")
        partes = []
        with z.open(nome[0]) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", usecols=COLS, chunksize=500_000):
                partes.append(ch[ch.CD_CARGO == 1].drop(columns="CD_CARGO"))
        d = pd.concat(partes, ignore_index=True).drop_duplicates(KEY + ["NR_TURNO"])
        p = os.path.join(saida, f"modelo_urna_{ano}.parquet")
        d.to_parquet(p, index=False)
        print(p, len(d), d.groupby("NR_TURNO").CD_MODELO_URNA.value_counts().to_dict())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
