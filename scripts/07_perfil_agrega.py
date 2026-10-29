#!/usr/bin/env python3
"""Fase 2 (A9): agrega o perfil de comparecimento e abstencao (TSE) por turno x UF x municipio x zona x faixa etaria x genero x instrucao.
Uso: python -I 07_perfil_agrega.py DIR_ZIPS DIR_SAIDA 2018 2022 2026
Usa o arquivo *_BRASIL.csv de cada zip. Coluna obrigatoria ausente => ERRO."""
import os, sys, zipfile
import pandas as pd
G = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "CD_FAIXA_ETARIA", "DS_FAIXA_ETARIA", "CD_GENERO", "CD_GRAU_INSTRUCAO"]
V = ["QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCAO", "QT_COMPAREC_FACULTATIVO", "QT_ABST_FACULTATIVO", "QT_COMPAREC_OBRIGATORIO", "QT_ABST_OBRIGATORIO"]


def main(zdir, saida, anos):
    os.makedirs(saida, exist_ok=True)
    for ano in anos:
        z = zipfile.ZipFile(os.path.join(zdir, f"perfil_comparecimento_abstencao_{ano}.zip"))
        nome = [n for n in z.namelist() if n.upper().endswith("_BRASIL.CSV")]
        if len(nome) != 1:
            raise SystemExit(f"ERRO {ano}: esperava 1 arquivo *_BRASIL.csv, achei {nome}")
        with z.open(nome[0]) as f:
            hdr = list(pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns)
        instr = [c for c in ("CD_GRAU_INSTRUCAO", "CD_GRAU_ESCOLARIDADE") if c in hdr]      # 2018 usa ESCOLARIDADE
        falt = [c for c in G[:-1] + V if c not in hdr] + ([] if instr else ["CD_GRAU_INSTRUCAO|CD_GRAU_ESCOLARIDADE"])
        if falt:
            raise SystemExit(f"ERRO {ano}: colunas ausentes {falt}")
        acc = None
        with z.open(nome[0]) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", usecols=G[:-1] + instr + V, chunksize=1_500_000):
                ch = ch.rename(columns={instr[0]: "CD_GRAU_INSTRUCAO"})
                g = ch.groupby(G, sort=False)[V].sum()
                acc = g if acc is None else acc.add(g, fill_value=0)
        acc = acc.reset_index(); acc["ano"] = ano
        p = os.path.join(saida, f"perfil_agg_{ano}.parquet"); acc.to_parquet(p, index=False)
        print(p, len(acc), "turnos:", sorted(acc.NR_TURNO.unique()), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]])
