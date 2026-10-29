#!/usr/bin/env python3
"""Figuras do portal que ja existem em portugues (a1, a2, a5, a14, klimek_T2), redesenhadas com o mesmo codigo e os mesmos dados, com textos em ingles (docs/figs/en/).
Com LANG=pt redesenha a versao em portugues (usada so para conferir que o redesenho reproduz a figura original).
Uso: python -I 16_figuras_en.py PARQUET RESULTADOS_FASE2 SAIDA [en|pt]"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import base

pq, res, out = sys.argv[1:4]
LANG = sys.argv[4] if len(sys.argv) > 4 else "en"
os.makedirs(out, exist_ok=True)
EN = LANG == "en"
T = (lambda pt, en: en) if EN else (lambda pt, en: pt)
RODADA = (lambda t: f"round {t}") if EN else (lambda t: f"T{t}")


def salva(fig, nome):
    fig.tight_layout(); fig.savefig(os.path.join(out, nome), dpi=110); plt.close(fig)


# a1: curva de apuracao (A1_curvas_pontos.csv e exatamente o F desenhado em f2_a1_a3.py)
c = pd.read_csv(os.path.join(res, "A1_curvas_pontos.csv"))
chaves = []
for col in c.columns:
    if col.endswith("_x"):
        chaves.append(col[:-2])
fig, ax = plt.subplots(1, len(chaves), figsize=(4.6 * len(chaves), 4), squeeze=False)
for j, k in enumerate(chaves):
    a_ = ax[0][j]; x = c[f"{k}_x"].values; m = x >= 1
    a_.fill_between(x[m], c[f"{k}_loA"].values[m], c[f"{k}_hiA"].values[m], color="#cccccc", label=T("ordem aleatória (95%)", "random order (95%)"))
    a_.fill_between(x[m], c[f"{k}_loB"].values[m], c[f"{k}_hiB"].values[m], color="#9ecae1", alpha=.8, label=T("aleatória dentro da UF (envelope)", "random within the state (envelope)"))
    a_.plot(x[m], c[f"{k}_real"].values[m], color="#d62728", lw=1.4, label=T("curva real", "actual curve"))
    ano, t = k.split("T")
    a_.set_title(f"{ano} {RODADA(t)}", fontsize=9); a_.set_xlabel(T("% das seções totalizadas", "% of sections tabulated")); a_.set_ylabel(T("% acumulado do PT", "cumulative % for PT (Lula)"))
    if j == 0:
        a_.legend(fontsize=7)
salva(fig, "a1_curva_apuracao.png")

# a14: recebido x totalizado
cv = pd.read_csv(os.path.join(res, "A14_a14_curvas_5min.csv"))
fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
for a_, (ano, t) in zip(ax, ((2026, 2), (2022, 2), (2026, 1))):
    d = cv[(cv.ano == ano) & (cv.turno == t)]
    a_.plot(d.minuto_do_dia / 60, d.pct_recebido, label=T("BU recebido", "poll-receipt (BU) received")); a_.plot(d.minuto_do_dia / 60, d.pct_totalizado, ls="--", label=T("1ª totalização", "1st tabulation")); a_.set_title(f"{ano} {RODADA(t)}", fontsize=9)
    a_.set_xlabel(T("hora (Brasília)", "time (Brasília)")); a_.set_ylabel(T("% das seções", "% of sections")); a_.axvline(19, color="#999", lw=.8, ls=":")
ax[0].legend(fontsize=8)
salva(fig, "a14_recebido_totalizado.png")

# a2: espelho de perdas
p = os.path.join(res, "A2_a2_mecanismo_pool.csv")
t = pd.read_csv(p)
ordem = ["<0,1", "0,1-0,2", "0,2-0,4", "0,4-0,8", ">=0,8"]
t = t.set_index(["cand", "razao_terceiros_sobre_cand_T1"])
fig, ax = plt.subplots(figsize=(7.5, 4)); x = np.arange(len(ordem)); w = .2
rot = (("PT", 2022, T("PT 2022 (líder do T1)", "PT 2022 (round-1 leader)"), "#2ca02c"), ("OPO", 2026, T("oponente 2026 (líder do T1)", "opponent 2026 (round-1 leader)"), "#d62728"),
       ("OPO", 2022, T("oponente 2022", "opponent 2022"), "#98df8a"), ("PT", 2026, "PT 2026", "#ff9896"))
for i, (cand, ano, lab, cor) in enumerate(rot):
    ax.bar(x + (i - 1.5) * w, [t.loc[(cand, f), str(ano)] for f in ordem], w, label=lab, color=cor)
ax.set_xticks(x); ax.set_xticklabels(ordem if not EN else [o.replace(",", ".") for o in ordem])
ax.set_xlabel(T("votos de terceiros no T1 / votos do candidato no T1, na seção", "votes for other candidates in round 1 / the candidate's round-1 votes, in the section"))
ax.set_ylabel(T("% das seções em que o candidato perde votos absolutos", "% of sections where the candidate loses absolute votes"))
ax.legend(fontsize=8); ax.set_title(T("Quem perde votos do T1 ao T2 (comparecimento estável ou crescente)", "Who loses votes from round 1 to round 2 (stable or growing turnout)"), fontsize=10)
salva(fig, "a2_espelho_perdas.png")

# a5: votos depois do horario nominal
t = pd.read_csv(os.path.join(res, "A5_a5_votos_apos_horario_nominal.csv")); t = t[t.ano == 2026]
fig, ax = plt.subplots(figsize=(7.5, 3.8))
nomes = {"L": T("fecharam ≥115 min depois", "closed ≥115 min late"), "C": T("controles (mesmo local)", "controls (same location)"), "R": T("amostra aleatória", "random sample"),
         "H": T("comparecimento ≥95%", "turnout ≥95%"), "RR_completo": T("Roraima (todas)", "Roraima (all)")}
ax.bar([nomes.get(e, e) for e in t.estrato], t.media_por_secao, color="#1d4e89")
ax.set_ylabel(T("votos computados depois do horário nominal, por seção", "votes counted after the nominal time, per section"))
ax.set_title(T("Votos depois do horário nominal, 2º turno de 2026 (logs das urnas)", "Votes after the nominal time, 2026 runoff (voting-machine logs)"), fontsize=10)
plt.setp(ax.get_xticklabels(), rotation=20, ha="right", fontsize=8)
salva(fig, "a5_votos_apos_nominal.png")

# klimek T2 (comparecimento x voto, histograma 2D)
NOME_OPO = {2014: "Aecio", 2018: "Bolsonaro", 2022: "Bolsonaro", 2026: "Flavio"}
anos = [2014, 2018, 2022, 2026]
anos = [a for a in anos if os.path.exists(os.path.join(pq, f"bu_{a}_t2.parquet"))]
fig, ax = plt.subplots(2, len(anos), figsize=(3.6 * len(anos), 7), squeeze=False)
for j, a in enumerate(anos):
    x = base(pd.read_parquet(os.path.join(pq, f"bu_{a}_t2.parquet")))
    for i, (sh, nm) in enumerate((("lula_sh", "PT (13)"), ("dir_sh", NOME_OPO[a]))):
        ax[i][j].hist2d(x.turnout.clip(0, 1), x[sh], bins=[50, 50], range=[[0, 1], [0, 1]], norm=matplotlib.colors.LogNorm(), cmap="viridis")
        ax[i][j].set_title(f"{a} {RODADA(2)} {nm}", fontsize=9); ax[i][j].set_xlabel(T("comparecimento", "turnout")); ax[i][j].set_ylabel(T("voto no candidato", "vote for the candidate"))
salva(fig, "klimek_T2.png")
print("figuras", LANG, "em", out)
