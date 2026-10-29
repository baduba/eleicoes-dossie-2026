#!/usr/bin/env python3
"""Fase 2 (A4/A5): monta a amostra de secoes para baixar os arquivos de urna.
Estratos: (L) seccoes que fecharam >= 115 min apos o horario nominal (2026/T2); (C) controle 1:1 no mesmo local (atraso < 15 min);
(H) secoes com comparecimento >= 95% no T2; (R) amostra aleatoria de 60 por UF. Semente fixa. Uso: python -I 09_amostra_urna.py PARQUET SAIDA_DIR"""
import os, sys
import numpy as np
import pandas as pd
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]


def main(pq, saida):
    os.makedirs(saida, exist_ok=True)
    d = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet"))
    d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.SG_UF != "RR")]
    rng = np.random.default_rng(20261028)
    L = d[d.atraso_min >= 115].assign(estrato="L")
    ctrl = d[(d.atraso_min < 15) & d.atraso_min.notna()]
    cs = []
    for loc, g in L.groupby("uf_local"):
        cand = ctrl[ctrl.uf_local == loc]
        if len(cand) == 0:
            cand = ctrl[ctrl.uf_zona == g.uf_zona.iloc[0]]
        if len(cand):
            cs.append(cand.sample(min(len(g), len(cand)), random_state=int(rng.integers(1e9))))
    C = pd.concat(cs).assign(estrato="C") if cs else d.iloc[0:0]
    H = d[(d.turnout >= .95) & (d.QT_APTOS >= 20)].assign(estrato="H")
    R = pd.concat([g.sample(min(60, len(g)), random_state=int(rng.integers(1e9))) for _, g in d.groupby("SG_UF")]).assign(estrato="R")
    A = pd.concat([L, C, H, R]).drop_duplicates(KEY + ["estrato"])
    allk = A.drop_duplicates(KEY)
    for uf, g in allk.groupby("SG_UF"):
        g[["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]].rename(columns={"CD_MUNICIPIO": "cd_municipio", "NR_ZONA": "zona", "NR_SECAO": "secao"}).to_csv(os.path.join(saida, f"amostra_{uf}.csv"), index=False)
    A[KEY + ["estrato", "atraso_min", "turnout", "uf_local"]].to_parquet(os.path.join(saida, "amostra_estratos.parquet"), index=False)
    print("secoes unicas:", len(allk), "| por estrato:", A.estrato.value_counts().to_dict(), "| UFs:", allk.SG_UF.nunique())
    print(allk.SG_UF.value_counts().head(8).to_dict())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
