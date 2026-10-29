#!/usr/bin/env python3
"""G3: tamanho do impacto dos itens em aberto, em votos de margem, contra a margem. Uso: python -I scripts/graficos/g3_impacto.py RAIZ"""
import os, sys
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
d = pd.read_csv(os.path.join(RAIZ, "results", "graficos", "itens_em_aberto.csv"), keep_default_na=False, na_values=[""])
curto = {"A-H1-S0": "Liberação manual, 1º turno (sem controle do 1º turno)", "A-A20": "Cadastro: eleitores muito idosos (80+)", "A-A10": "Urna modelo UE2022", "A-H1-FL": "Flávio x liberação manual", "A-H6": "Seções novas",
         "A-H5": "639 seções com comparecimento ≥ 95%", "A-A5-2022": "Seção de 2022 com log divergente", "A-A22": "Presidente x governador (AM e DF)", "A-A20b": "Comparecimento x fração 80+ por seção", "A-A20b-part": "Voto x fração 80+ por seção"}
n = d[d.teto_pior_caso.notna() & (d.bloco == "a")].sort_values("teto_pior_caso", ascending=False).reset_index(drop=True)
sem = d[(d.teto_pior_caso.isna())]
cor = lambda s: AZUL if "Lula" in s else (VERM if "Flávio" in s else CINZA)
M = MOVEL
fig, axs = plt.subplots(2, 1, figsize=(4.7, 8.2), sharey=True) if M else plt.subplots(1, 2, figsize=(12.5, 4.9), sharey=True)
import textwrap
for ax, esc in zip(axs, ("linear", "log")):
    for i, r in n.iterrows():
        c = cor(r.direcao)
        ax.barh(i, r.teto_pior_caso, color=c, alpha=.28, hatch="///", edgecolor=c, lw=1, height=.62)
        if r.excesso_medido > 0:
            ax.barh(i, r.excesso_medido, color=c, height=.62)
        txt = f"teto, não estimativa: {milhar(r.teto_pior_caso)}" + (f" | medido: {milhar(r.excesso_medido)}" if r.excesso_medido > 0 else "")
        if esc == "linear":
            ax.text(r.teto_pior_caso + 60000, i, ("teto, não estimativa:\n" + milhar(r.teto_pior_caso) + (f"\nmedido: {milhar(r.excesso_medido)}" if r.excesso_medido > 0 else "")) if M else txt, va="center", fontsize=6.4 if M else 7.8, color=TXT)
        else:
            ax.text(1.4, i, ("teto, não estimativa:\n" + milhar(r.teto_pior_caso) + (f" | medido: {milhar(r.excesso_medido)}" if r.excesso_medido > 0 else "")) if M else txt, va="center", ha="left", fontsize=6.4 if M else 7.8, color=TXT, bbox=dict(fc=FUNDO, ec="none", alpha=.85, pad=1.5))
    ax.axvline(MARGEM, color=TXT, lw=2); ax.set_ylim(len(n) - .4, -.6)
    ax.set_yticks(range(len(n))); ax.set_yticklabels([("\n".join(textwrap.wrap(curto[i], 24)) if M else curto[i]) for i in n.id], fontsize=6.6 if M else 8.8)
    if esc == "linear":
        ax.set_xlim(0, 4_700_000 if not M else 5_000_000); ax.set_xticks([0, 1_000_000, 2_000_000, 3_000_000, 4_000_000]); ax.set_xticklabels(["0", "1 mi", "2 mi", "3 mi", "4 mi"])
        ax.set_title("Escala linear (proporção real)", loc="left", fontsize=8.5 if M else 10.5, pad=16); ax.text(MARGEM * .99, -.5, "Margem 4.430.191", ha="right", va="bottom", fontsize=7 if M else 8.5, fontweight="bold", bbox=dict(fc=FUNDO, ec="none", pad=1))
    else:
        ax.set_xscale("log"); ax.set_xlim(1, 3e7); ax.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000]); ax.set_xticklabels(["1", "10", "100", "1 mil", "10 mil", "100 mil", "1 mi"])
        ax.set_title("Escala logarítmica (itens pequenos visíveis)", loc="left", fontsize=8.5 if M else 10.5, pad=16); ax.text(MARGEM * .9, -.5, "Margem 4.430.191", ha="right", va="bottom", fontsize=7 if M else 8.5, fontweight="bold", bbox=dict(fc=FUNDO, ec="none", pad=1))
    ax.set_xlabel("Votos de margem", fontsize=8 if M else 10)
if M:
    fig.subplots_adjust(hspace=0.5)
fig.suptitle("Tamanho dos itens em aberto, em votos de margem,\ncontra a margem de 4.430.191" if M else "Tamanho dos itens em aberto, em votos de margem, contra a margem de 4.430.191", x=0.01, ha="left", fontsize=9 if M else 12, y=1.0 if not M else 0.995)
leg = [Patch(fc=AZUL, label="excesso medido, a favor de Lula"), Patch(fc=VERM, label="excesso medido, a favor de Flávio"), Patch(fc=CINZA, label="sem direção identificável"),
       Patch(fc="white", ec=CINZA, hatch="///", label="hachurado: teto de pior caso, não estimativa")]
fig.legend(handles=leg, loc="lower center", ncol=1 if M else 4, frameon=False, fontsize=6.8 if M else 8.6, bbox_to_anchor=(.5, -.08 if M else -.04))
nota = ("Não mensuráveis com os dados públicos (sem barra): curva de apuração do 1º turno; testes não executados (A21, A23 a A25, A28); voto digitado x voto registrado; alteração coerente antes da publicação.\n"
        "O que falta para medir cada um está na lista de perguntas em aberto. Cada barra é um item; não há soma. A escala linear começa em zero.")
if M:
    nota = "\n".join(textwrap.fill(par, 70) for par in nota.split("\n"))
fig.text(0.01, -0.2 if M else -0.13, nota, fontsize=6.4 if M else 8.4, color=SUAVE, ha="left")
salva(fig, RAIZ, "g3_impacto", "Tamanho dos itens em aberto", "Barras horizontais, em votos de margem, para cada item em aberto com número: excesso medido (sólida) e teto de pior caso (hachurada), contra a margem de 4.430.191 votos, em escala linear e logarítmica.")
print("g3 ok")
