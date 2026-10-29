#!/usr/bin/env python3
"""Extrai (secao -> nome/endereco do local de votacao) dos zips detalhe_votacao_secao, para classificar tipo de local.
Uso: python -I 01b_locais.py DIR_ZIPS DIR_SAIDA 2022 2026"""
import os, sys, zipfile
import pandas as pd

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
COLS = KEY + ["NR_TURNO", "CD_CARGO", "NR_LOCAL_VOTACAO", "NM_LOCAL_VOTACAO", "DS_LOCAL_VOTACAO_ENDERECO"]


def main(zdir, saida, anos):
    os.makedirs(saida, exist_ok=True)
    for ano in anos:
        z = zipfile.ZipFile(os.path.join(zdir, f"detalhe_votacao_secao_{ano}.zip"))
        nome = [n for n in z.namelist() if n.upper().endswith("_BR.CSV")]
        if len(nome) != 1:
            raise SystemExit(f"ERRO: esperava 1 arquivo *_BR.csv em {ano}, achei {nome}")
        partes = []
        with z.open(nome[0]) as f:
            hdr = pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns
        falt = [c for c in COLS if c not in hdr]
        if falt:
            raise SystemExit(f"ERRO {ano}: colunas ausentes {falt}")
        with z.open(nome[0]) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", usecols=COLS, chunksize=500_000):
                ch = ch[(ch.CD_CARGO == 1) & (ch.NR_TURNO == 2)].drop(columns=["CD_CARGO", "NR_TURNO"])
                partes.append(ch)
        d = pd.concat(partes, ignore_index=True).drop_duplicates(KEY)
        p = os.path.join(saida, f"locais_{ano}.parquet")
        d.to_parquet(p, index=False)
        print(p, len(d))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
