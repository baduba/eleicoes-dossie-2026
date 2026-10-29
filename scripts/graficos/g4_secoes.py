#!/usr/bin/env python3
"""G4: quantas secoes precisariam ser alteradas. Uso: python -I scripts/graficos/g4_secoes.py RAIZ"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
G = os.path.join(RAIZ, "results", "graficos")
d = pd.read_csv(os.path.join(G, "secoes_para_inverter.csv")); v = pd.read_csv(os.path.join(G, "visibilidade_individual.csv")).iloc[0]; N = 499_248
kv = int(v.trocas_por_secao_visiveis_como_outlier)
M = MOVEL
fig, ax = plt.subplots(figsize=(4.7, 5.8) if M else (9.6, 5.6))
FS = 7 if M else 8.8
ax.axvspan(kv, 300, color=AZUL, alpha=.12, lw=0); ax.axvspan(1, kv, color=CINZA, alpha=.12, lw=0)
ax.plot(d.trocas_por_secao, d.secoes_necessarias, color=TXT, lw=2)
for k in (5, 50, 200):
    r = d[d.trocas_por_secao == k].iloc[0]
    ax.plot([k], [r.secoes_necessarias], "o", color=VERM, ms=8, mec=FUNDO, mew=2)
    ax.annotate(f"{k} trocas/seção:\n{milhar(r.secoes_necessarias)} seções ({str(round(r.pct_das_secoes, 1)).replace(".", ",")}%)", (k, r.secoes_necessarias), textcoords="offset points", xytext=(-8, 10) if (M and k == 200) else (10, 10), ha="right" if (M and k == 200) else "left", fontsize=FS)
ax.axhline(N, color=SUAVE, lw=1, ls=":"); ax.text(1.05, N * 1.15, "todas as 499.248 seções", fontsize=FS - .3, color=SUAVE)
ax.text(1.12, 1100, "só em conjunto,\nBUs impressos ou\nteste de integridade" if M else "só em conjunto, boletins impressos\nou teste de integridade", fontsize=FS, va="bottom", fontweight="bold")
ax.text(kv * 1.1, 1.9e6, "valor atípico no\nlocal (alcançada\npelos testes)" if M else "aparece como valor atípico no local\n(já alcançada pelos testes executados)", fontsize=FS, va="top", fontweight="bold")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(1, 300); ax.set_ylim(1000, 3_000_000)
ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200]); ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100", "200"])
ax.set_yticks([1000, 10000, 100000, 1000000]); ax.set_yticklabels(["1.000", "10.000", "100.000", "1.000.000"])
ax.set_xlabel("Votos trocados por seção (escala log)", fontsize=8 if M else 10); ax.set_ylabel("Seções necessárias para mudar a margem (log)", fontsize=8 if M else 10)
ax.set_title("Quantas seções precisariam ser alteradas\npara inverter a margem de 4.430.191 votos" if M else "Quantas seções precisariam ser alteradas para inverter a margem de 4.430.191 votos", loc="left", fontsize=9 if M else 11.5)
sd_txt = str(round(v.sd_residuo_local_pp, 2)).replace(".", ",")
nota = (f"Cada voto trocado muda a margem em 2. Limiar de {kv} trocas por seção: desvio padrão do resíduo local de {sd_txt} p.p. (medido nesta auditoria), {int(v.mediana_votos_validos)} votos válidos por seção, |z| > 3.\n"
        "Região à esquerda do limiar: uma seção alterada não se destaca das vizinhas; só aparece em conjunto (comparação com outros cargos, A22, não executada) ou conferindo boletins impressos e o teste de integridade.\n"
        "Premissas: amostra aleatória de seções; não descreve como uma alteração seria feita.")
if M:
    import textwrap
    nota = "\n".join(textwrap.fill(par, 66) for par in nota.split("\n"))
fig.text(0.01, -0.2 if M else -0.13, nota, fontsize=7 if M else 8.5, color=SUAVE, ha="left")
salva(fig, RAIZ, "g4_secoes", "Seções necessárias para inverter a margem", "Número de seções que precisariam ser alteradas para mudar a margem em função dos votos trocados por seção, com a região que os testes executados já alcançam e a região que só boletins impressos e o teste de integridade alcançam.")
print("g4 ok")
