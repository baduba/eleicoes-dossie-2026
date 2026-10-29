#!/usr/bin/env python3
"""Reproduz com os dados as alegacoes testaveis do 'Relatorio Pericial Independente' (conforme o resumo disponivel; o PDF original nao foi fornecido).
Uso: python -I 11_alegacoes_relatorio.py PARQUET SAIDA_DIR"""
import os, sys
import numpy as np
import pandas as pd

pq, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
sh = lambda g: 100 * g.lula.sum() / (g.lula.sum() + g["dir"].sum())
d = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet"))
d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
h = d.DT_ENCERRAMENTO.dt.hour
d = d.assign(tarde_cru=(h >= 19), tarde_115=(d.atraso_min >= 115))
# 1) Lula% nas secoes com encerramento >= 19h (relogio cru) contra o estado, por UF
rows = []
for uf, g in d[d.SG_UF != "ZZ"].groupby("SG_UF"):
    l = g[g.tarde_cru]
    if len(l) >= 20:
        rows.append(dict(uf=uf, secoes_tardias_relogio_cru=len(l), lula_pct_nas_tardias=sh(l), lula_pct_no_estado=sh(g), diferenca_pp=sh(l) - sh(g)))
pd.DataFrame(rows).sort_values("diferenca_pp").round(2).to_csv(os.path.join(out, "ALEG_tardias_por_uf.csv"), index=False)
# 2) o que a soma de eleitorado apto das secoes tardias representa: aptos x comparecimento
l = d[(d.SG_UF != "ZZ") & d.tarde_cru]
pd.DataFrame([dict(secoes=len(l), aptos=int(l.QT_APTOS.sum()), comparecimento=int(l.QT_COMPARECIMENTO.sum()), pct_comparecimento_sobre_aptos=100 * l.QT_COMPARECIMENTO.sum() / l.QT_APTOS.sum())]).round(2).to_csv(os.path.join(out, "ALEG_aptos_secoes_tardias.csv"), index=False)
# 3) secoes unanimes (>=30 validos)
rows = []
for a in (2018, 2022, 2026):
    x = pd.read_parquet(os.path.join(pq, f"bu_{a}_t2.parquet")); x = x[x.DS_TIPO_URNA.str.upper().eq("APURADA") & (x.valid2 >= 30) & (x.SG_UF != "ZZ")]
    rows.append(dict(ano=a, secoes_ge30_validos=len(x), pt_ge90=int((x.lula_sh >= .9).sum()), oponente_ge90=int((x.dir_sh >= .9).sum()), pt_100=int((x.lula_sh == 1).sum()), oponente_100=int((x.dir_sh == 1).sum())))
pd.DataFrame(rows).to_csv(os.path.join(out, "ALEG_unanimes.csv"), index=False)
print("ok", out)
