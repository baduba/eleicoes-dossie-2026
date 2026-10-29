#!/usr/bin/env python3
"""G0: barra de cobertura de verificacao da cadeia do voto (hero da primeira pagina).
Numeros derivados de results/graficos/cadeia.csv (mapa G1, 12 elos): 4 verificados, 5 parciais, 3 nao verificaveis.
Uso: python g0_hero_verificacao.py RAIZ [m]   ('m' gera a versao estreita _m)"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos"))
import matplotlib.pyplot as plt
from common import AZUL, VERM, AMBAR, TXT, SUAVE, salva

RAIZ = sys.argv[1]
MOVEL = len(sys.argv) > 2 and sys.argv[2] == "m"

SEG = [(4, "verificados", AZUL), (5, "parciais", AMBAR), (3, "não verificáveis", VERM)]

fig, ax = plt.subplots(figsize=((3.8, 2.9) if MOVEL else (8.2, 1.9)))
ax.grid(False)
ax.set_xlim(0, 12)
ax.set_ylim(-0.95, 1.62)
ax.axis("off")

x = 0
for k, rot, cor in SEG:
    ax.barh(1, k, left=x, height=0.62, color=cor, edgecolor="white", linewidth=1.2)
    pct = round(100 * k / 12)
    txt = f"{k}\n{pct}%" if MOVEL else f"{k} {rot}\n{pct}%"
    ax.text(x + k / 2, 1, txt, ha="center", va="center", color="white",
            fontsize=9 if MOVEL else 10, fontweight="bold", linespacing=1.15)
    x += k
ax.text(0, 1.52, "cadeia do voto: 12 elos", fontsize=9 if MOVEL else 10.5, color=TXT, fontweight="bold")
ax.text(6, 0.5, "azul: verificado · ocre: parcial · vermelho: não verificável — 33% totalmente verificada, 25% não verificável",
        fontsize=7.5 if MOVEL else 9, color=SUAVE, ha="center", va="center", wrap=True)

ax.barh(-0.15, 12, height=0.62, color=VERM, alpha=0.16, edgecolor=VERM, linewidth=1.0)
t100 = "100% dos votos atravessam\npelo menos um elo não verificável" if MOVEL else "100% dos votos atravessam pelo menos um elo não verificável"
ax.text(6, -0.15, t100, ha="center", va="center", color=TXT, fontsize=9 if MOVEL else 10, fontweight="bold", linespacing=1.2)
ax.text(0, -0.68, "todos os votos", fontsize=9 if MOVEL else 10.5, color=TXT, fontweight="bold")

fig.tight_layout(pad=0.3)
salva(fig, RAIZ, "g0_verificacao", "Cobertura de verificação da cadeia do voto",
      "Barra empilhada dos 12 elos da cadeia do voto: 4 verificados (33%), 5 parcialmente verificados (42%) e 3 não verificáveis com dados públicos (25%). "
      "Uma segunda barra indica que 100% dos votos atravessam pelo menos um elo não verificável.")
print("g0_verificacao" + ("_m" if MOVEL else ""), "salvo")
