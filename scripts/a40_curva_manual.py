#!/usr/bin/env python3
"""A40: participacao de Lula por faixa de liberacao manual. Painel (a) 2026 T2 x 2022 T2; (b) 2026 T2 com controles por tipo de local.
Dados: results/exploratorio/ALE_curva_manual_por_ano.csv e ALE_curva_manual_escola_2026t2.csv.
Uso: python a40_curva_manual.py RAIZ [m] [en|pt]"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos"))
import matplotlib.pyplot as plt
import pandas as pd
from common import AZUL, VERM, AMBAR, CINZA, TXT, salva

RAIZ = sys.argv[1]
MOVEL = len(sys.argv) > 2 and sys.argv[2] == "m"
EN = len(sys.argv) > 3 and sys.argv[3] == "en"
T = (lambda pt, en: en) if EN else (lambda pt, en: pt)

EX = os.path.join(RAIZ, "results", "exploratorio")
cur = pd.read_csv(os.path.join(EX, "ALE_curva_manual_por_ano.csv"))
esc = pd.read_csv(os.path.join(EX, "ALE_curva_manual_escola_2026t2.csv"))
FAIXAS = ["0-5%", "5-10%", "10-20%", "20-30%", ">30%"]
X = range(len(FAIXAS))

fig, ax = plt.subplots(1, 2, figsize=((4.6, 3.2) if MOVEL else (9.2, 3.4)), sharey=True)
if MOVEL:
    fig, ax = plt.subplots(2, 1, figsize=(4.6, 6.0), sharex=True)

def serie(df, rot, cor, a, estilo="o-"):
    d = df.set_index("faixa").reindex(FAIXAS)
    a.plot(X, d.lula_pct_validos, estilo, color=cor, lw=1.6, ms=4, label=rot)

a, b = (ax[0], ax[1]) if not MOVEL else (ax[0], ax[1])
serie(cur[(cur.ano == 2026) & (cur.turno == 2)], "2026 " + T("2º turno", "runoff"), AZUL, a)
serie(cur[(cur.ano == 2022) & (cur.turno == 2)], "2022 " + T("2º turno", "runoff"), VERM, a)
serie(cur[(cur.ano == 2018) & (cur.turno == 2)], "2018 " + T("2º turno", "runoff"), CINZA, a, estilo="o--")
serie(cur[(cur.ano == 2026) & (cur.turno == 1)], "2026 " + T("1º turno", "1st round"), AMBAR, a, estilo="o--")
a.set_title(T("curva por faixa de liberação manual", "curve by manual-clearance band"), fontsize=10, color=TXT)
a.legend(fontsize=7.5 if MOVEL else 8.5, frameon=False, loc="upper left")

geral = cur[(cur.ano == 2026) & (cur.turno == 2)].set_index("faixa").reindex(FAIXAS)
b.plot(X, geral.lula_pct_validos, "o-", color=AZUL, lw=1.6, ms=4, label=T("todas as seções", "all sections"))
for flag, rot, cor in ((True, T("em escolas", "in schools"), VERM), (False, T("fora de escolas", "outside schools"), CINZA)):
    d = esc[esc.escola == flag].set_index("faixa").reindex(FAIXAS)
    b.plot(X, d.lula_pct_validos, "o--", color=cor, lw=1.6, ms=4, label=rot)
b.set_title(T("2026 T2 com controle por tipo de local", "2026 runoff by location type"), fontsize=10, color=TXT)
b.legend(fontsize=7.5 if MOVEL else 8.5, frameon=False, loc="upper left")

for a_ in (a, b):
    a_.set_xticks(list(X)); a_.set_xticklabels(FAIXAS, fontsize=8)
a.set_ylabel(T("Lula (% dos votos válidos)", "Lula (% of valid votes)"))
fig.tight_layout(pad=0.6)

if EN:
    d = os.path.join(RAIZ, "docs", "img", "en"); os.makedirs(d, exist_ok=True)
    nome = "a40_curva_manual" + ("_m" if MOVEL else "")
    fig.savefig(os.path.join(d, nome + ".png"), dpi=170, bbox_inches="tight",
                metadata={"Title": "A40: Lula share by manual-clearance band", "Description": "Left: Lula share of valid votes by manual-clearance band, 2026 runoff vs 2022 and 2018 runoffs and 2026 first round. Right: 2026 runoff, all sections vs in schools vs outside schools."})
    fig.savefig(os.path.join(d, nome + ".svg"), bbox_inches="tight", metadata={"Title": "A40: Lula share by manual-clearance band", "Date": None})
    plt.close(fig)
else:
    salva(fig, RAIZ, "a40_curva_manual", "A40: participação de Lula por faixa de liberação manual",
          "Painel esquerdo: participação de Lula nos votos válidos por faixa de liberação manual, 2026 segundo turno contra 2022 e 2018 segundo turno e 2026 primeiro turno; 2026 não passa de 61%. Painel direito: 2026 segundo turno, todas as seções contra seções em escolas e fora de escolas.")
print("a40_curva_manual" + ("_en" if EN else "") + ("_m" if MOVEL else ""), "salvo")
