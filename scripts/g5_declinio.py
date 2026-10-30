#!/usr/bin/env python3
"""G5: curva do declinio desde o pico de 2018 (secao "Duas eras eleitorais" do index).
Cinco indicadores normalizados (indice 2018 = 100), serie 2014-2026, de results/exploratorio.
Uso: python g5_declinio.py RAIZ [m] [en|pt]   ('m': versao estreita _m; 'en': textos em ingles em docs/img/en/)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos"))
import matplotlib.pyplot as plt
from common import AZUL, VERM, AMBAR, CINZA, TXT, salva

RAIZ = sys.argv[1]
MOVEL = len(sys.argv) > 2 and sys.argv[2] == "m"
EN = len(sys.argv) > 3 and sys.argv[3] == "en"
T = (lambda pt, en: en) if EN else (lambda pt, en: pt)

ANOS = [2014, 2018, 2022, 2026]
# valores por indicador (None = sem dado); normalizados a 2018 = 100
SERIES = [
    (T("seções com 0-10 votos no oponente", "sections with 0-10 votes for the opponent"), [6324, 7606, 4097, 3029], VERM),
    (T("saldo em seções PT ≥ 80% (mi)", "net in sections PT ≥ 80% (mi)"), [6.02, 6.38, 5.58, 4.97], AZUL),
    (T("habilitação sem biometria no NE (%)", "no-biometrics clearance in the NE (%)"), [None, 9.49, 9.38, 7.19], AMBAR),
    (T("empates observados / nulo", "observed ties / null"), [0.90, 1.03, 0.95, 0.92], "#009E73"),
    (T("resíduo total medido (mi)", "total measured residual (mi)"), [6.95, 7.08, 6.30, 5.61], CINZA),
]

fig, ax = plt.subplots(figsize=((4.2, 3.4) if MOVEL else (7.6, 3.6)))
for rot, vals, cor in SERIES:
    base = vals[1]  # 2018 = 100 (todas as series tem 2018)
    idx = [None if v is None else 100 * v / base for v in vals]
    x = [a for a, v in zip(ANOS, idx) if v is not None]
    y = [v for v in idx if v is not None]
    ax.plot(x, y, marker="o", ms=4, lw=1.6, color=cor, label=rot)
ax.axhline(100, color=TXT, lw=0.8, ls=":")
ax.set_xticks(ANOS)
ax.set_ylabel(T("índice (2018 = 100)", "index (2018 = 100)"))
ax.set_ylim(0, 115)
leg = ax.legend(loc="lower left", fontsize=7.5 if MOVEL else 8.5, frameon=False)
fig.tight_layout(pad=0.4)

if EN:
    d = os.path.join(RAIZ, "docs", "img", "en"); os.makedirs(d, exist_ok=True)
    nome = "g5_declinio" + ("_m" if MOVEL else "")
    fig.savefig(os.path.join(d, nome + ".png"), dpi=170, bbox_inches="tight",
                metadata={"Title": "The decline curve since the 2018 peak", "Description": "Five indicators of the series 2014-2026 normalized to index 2018=100, all falling from the 2018 peak."})
    fig.savefig(os.path.join(d, nome + ".svg"), bbox_inches="tight",
                metadata={"Title": "The decline curve since the 2018 peak", "Date": None})
    plt.close(fig)
else:
    salva(fig, RAIZ, "g5_declinio", "A curva do declínio desde o pico de 2018",
          "Cinco indicadores da série 2014-2026 normalizados a índice 2018=100: seções com 0 a 10 votos no oponente, saldo em seções com PT a 80% ou mais, habilitação sem biometria no Nordeste, empates sobre o nulo e resíduo total medido. Todos caem desde o pico de 2018.")
print("g5_declinio" + ("_en" if EN else "") + ("_m" if MOVEL else ""), "salvo")
