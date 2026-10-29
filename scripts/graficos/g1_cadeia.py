#!/usr/bin/env python3
"""G1: mapa da cadeia do voto, com status por etapa. Gera PNG/SVG (portal e PDF) e o texto Mermaid (README). Uso: python -I scripts/graficos/g1_cadeia.py RAIZ"""
import os, sys, textwrap
import pandas as pd
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
c = pd.read_csv(os.path.join(RAIZ, "results", "graficos", "cadeia.csv"))
ROT = {"verificado": ("✓ verificado pelos testes", AZUL, "", "#e5f0f8"), "parcial": ("◐ verificado parcialmente", AMBAR, "..", "#f7efdc"), "nao_verificavel": ("✕ não verificável com dados públicos", CINZA, "xx", "#ececec")}
M = MOVEL
if M:
    fig, ax = plt.subplots(figsize=(4.7, 10.2)); ax.set_xlim(0, 2); ax.set_ylim(-.1, 7.6); ax.axis("off")
    pos = [(i % 2, 5.75 - (i // 2) * 1.15) for i in range(12)]
else:
    fig, ax = plt.subplots(figsize=(13, 5.3)); ax.set_xlim(0, 6); ax.set_ylim(.1, 2.9); ax.axis("off")
    pos = [(i % 6, 1.85 if i < 6 else 0.55) for i in range(12)]
for i, (r, (x, y)) in enumerate(zip(c.itertuples(), pos)):
    rot, cor, hat, fundo = ROT[r.status]
    destaque = "voto digitado" in r.etapa.lower()
    ax.add_patch(FancyBboxPatch((x + .06, y), .88, .78, boxstyle="round,pad=0.01,rounding_size=.05", fc=fundo, ec=VERM if destaque else cor, lw=3.4 if destaque else 1.6, hatch=hat, zorder=2))
    ax.text(x + .5, y + .66, "\n".join(textwrap.wrap(f"{i + 1}. " + r.etapa, 17 if M else 21)), ha="center", va="top", fontsize=7.4 if M else 8.6, fontweight="bold", zorder=3, bbox=dict(fc=fundo, ec="none", pad=1.6))
    ax.text(x + .5, y + .2, r.testes, ha="center", va="center", fontsize=7 if M else 8.2, color=TXT, zorder=3, bbox=dict(fc=fundo, ec="none", pad=1.2))
    ax.text(x + .5, y - .04, "\n".join(textwrap.wrap(r.nota, 28 if M else 26)), ha="center", va="top", fontsize=5.6 if M else 7.2, color=SUAVE, zorder=3)
    ax.text(x + .5, y + .02, rot.split(" ")[0], ha="center", va="bottom", fontsize=10, color=cor, zorder=3) if False else None
    if (not M) and i not in (5, 11):
        ax.add_patch(FancyArrowPatch((x + .95, y + .39), (x + 1.05, y + .39), arrowstyle="-|>", mutation_scale=12, color=SUAVE, zorder=1))
ax.add_patch(FancyArrowPatch((5.5, 1.78), (.5, 1.33), connectionstyle="arc3,rad=0", arrowstyle="-|>", mutation_scale=12, color=SUAVE, zorder=1, ls=":", alpha=0))
ax.text(.0, 1.45, "A cadeia continua na linha de baixo", fontsize=8, color=SUAVE, ha="left") if not M else ax.text(1, 7.55, "Leia da esquerda para a direita, de cima para baixo (1 a 12).", fontsize=6.6, color=SUAVE, ha="center")
ax.text(1 if M else 2.5, 7.3 if M else 2.88, "Elo 3, em vermelhão: o voto digitado e o\nvoto registrado só são conferidos por amostragem,\nno teste de integridade." if M else "Elo destacado em vermelhão: o voto digitado e o voto registrado só são conferidos por amostragem, no teste de integridade.", fontsize=6.8 if M else 9.4, color=TXT, ha="center", va="top", fontweight="bold")
leg = [Patch(fc=ROT[k][3], ec=ROT[k][1], hatch=ROT[k][2], label=ROT[k][0]) for k in ROT]
fig.legend(handles=leg, loc="lower center", ncol=1 if M else 3, frameon=False, fontsize=7 if M else 9, bbox_to_anchor=(.5, -.04 if M else -.02))
fig.suptitle("Mapa da cadeia do voto:\no que os testes verificam e não verificam" if M else "Mapa da cadeia do voto: o que os testes verificam e o que não verificam", x=0.01, ha="left", fontsize=9.5 if M else 12.5, y=1.0)
salva(fig, RAIZ, "g1_cadeia", "Mapa da cadeia do voto", "Doze etapas do voto, do cadastro à divulgação, cada uma com o status de verificação (verificado, parcial ou não verificável com dados públicos) e o teste correspondente; o elo entre voto digitado e voto registrado aparece destacado como não verificável com dados públicos.")
# Mermaid (README)
cls = {"verificado": "ok", "parcial": "parc", "nao_verificavel": "nao"}
L = ["flowchart TB"]
for i, r in enumerate(c.itertuples()):
    L.append(f'  E{i}["{r.etapa}<br/><i>{r.testes}</i><br/>{ROT[r.status][0]}"]:::{cls[r.status]}')
L.append("  " + " --> ".join(f"E{i}" for i in range(len(c))))
L += ["  classDef ok fill:#e5f0f8,stroke:#0072B2,stroke-width:2px,color:#1c1c1e",
      "  classDef parc fill:#f7efdc,stroke:#9A6700,stroke-width:2px,stroke-dasharray:4 3,color:#1c1c1e",
      "  classDef nao fill:#ececec,stroke:#595959,stroke-width:2px,stroke-dasharray:2 2,color:#1c1c1e",
      "  style E2 stroke:#D55E00,stroke-width:5px"]
if not M:
    open(os.path.join(RAIZ, "docs", "img", "g1_cadeia.mmd"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("g1 ok")
