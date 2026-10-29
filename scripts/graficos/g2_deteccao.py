#!/usr/bin/env python3
"""G2: curvas de deteccao. Uso: python -I scripts/graficos/g2_deteccao.py RAIZ"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
G = os.path.join(RAIZ, "results", "graficos")
c = pd.read_csv(os.path.join(G, "curvas_deteccao.csv")); p = pd.read_csv(os.path.join(G, "curvas_deteccao_premissas.csv")).iloc[0]
inv = pd.read_csv(os.path.join(G, "secoes_para_inverter.csv")); N = 499_248
M = MOVEL
fig, ax = plt.subplots(figsize=(4.7, 6.2) if M else (9.6, 5.8))
FS = 7 if M else 8.5
x = 100 * c.fracao
ax.fill_between(x, 100 * c.biometria_5pct, 100 * c.biometria_10pct, color=AMBAR, alpha=.18, lw=0)
ax.plot(x, 100 * c.teste_integridade, color=AZUL, lw=2, label=f"(a) teste de integridade, todas as urnas (n = {int(p.n_teste_integridade)})")
ax.plot(x, 100 * c.biometria_10pct, color=AMBAR, lw=2, label=f"(b) só urnas com biometria (n = {int(p.n_biometria_5pct)} a {int(p.n_biometria_10pct)}; faixa)")
ax.plot(x, 100 * c.biometria_5pct, color=AMBAR, lw=1)
for col, n, ls in (("bu_100", 100, ":"), ("bu_300", 300, "--"), ("bu_1000", 1000, "-.")):
    ax.plot(x, 100 * c[col], color=CINZA, lw=1.6, ls=ls, label=f"(c) boletins impressos conferidos, n = {n}")
nb = int(p.n_bu_conferidos)
ax.text(0.99, 0.085, f"(c) n real conferido em {pd.to_datetime(p.data_bu).strftime('%d/%m/%Y')}: {nb} boletins" + ("" if nb else " (sem curva)"), transform=ax.transAxes, ha="right", fontsize=7 if M else 9.5, color=TXT)
for k, ls, yy in ((200, "-", 35), (50, "--", 55)):
    sc = int(inv[inv.trocas_por_secao == k].secoes_necessarias.iloc[0]); fr = 100 * sc / N
    ax.axvline(fr, color=VERM, lw=1.4, ls=ls)
    ax.text(fr * (0.96 if (M and k == 50) else 1.04), yy, f"{k} trocas/seção:\nmudar a margem\nexige {str(round(fr, 1)).replace('.', ',')}% das seções" if M else f"{k} trocas por seção:\nmudar a margem exige\n{str(round(fr, 1)).replace('.', ',')}% das seções", color=TXT, fontsize=FS, va="bottom", ha="right" if (M and k == 50) else "left", bbox=dict(fc=FUNDO, ec="none", alpha=.9, pad=1.5))
ax.text(0.99, 0.035, "5 trocas/seção: 88,7% das seções (fora do gráfico)", transform=ax.transAxes, ha="right", fontsize=FS, color=TXT)
ax.set_xscale("log"); ax.set_xlim(0.1, 20); ax.set_ylim(0, 102)
ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20]); ax.set_xticklabels(["0,1%", "0,2%", "0,5%", "1%", "2%", "5%", "10%", "20%"])
ax.set_yticks(range(0, 101, 20)); ax.set_yticklabels([f"{v}%" for v in range(0, 101, 20)])
ax.set_xlabel("Fração das urnas ou seções alteradas (escala log)", fontsize=8 if M else 10); ax.set_ylabel("Chance de ver ao menos uma alterada", fontsize=8 if M else 10)
ax.set_title("Quanto cada verificação enxerga:\nchance de detectar ao menos uma urna alterada" if M else "Quanto cada verificação enxerga: probabilidade de detectar ao menos uma urna alterada", loc="left", fontsize=9 if M else 11.5)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1 if M else 2, frameon=False, fontsize=7 if M else 8.8)
fig.text(0.01, -0.36 if M else -0.24, ("Premissas: amostra aleatória; em (b), software que se\ncomporta normalmente no teste sem biometria. Não descreve\ncomo um ataque seria feito. As linhas verticais mostram a\nfração de seções que precisaria ser alterada para mudar a\nmargem de 4.430.191 votos.") if M else "Premissas: amostra aleatória; em (b), software que se comporta normalmente no teste sem biometria. Não descreve como um ataque seria feito.\nAs linhas verticais mostram a fração de seções que precisaria ser alterada para mudar a margem de 4.430.191 votos.", fontsize=7 if M else 8.5, color=SUAVE, ha="left")
salva(fig, RAIZ, "g2_deteccao", "Curvas de detecção", "Probabilidade de detectar ao menos uma urna ou seção alterada, em função da fração alterada, para o teste de integridade, para as urnas com biometria e para boletins impressos conferidos, com marcas da fração necessária para mudar a margem.")
print("g2 ok")
