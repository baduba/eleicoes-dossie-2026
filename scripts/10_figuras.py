#!/usr/bin/env python3
"""Fase 2: figuras do portal, geradas dos parquets e CSVs de resultados. Uso: python -I 10_figuras.py PARQUET RESULTADOS SAIDA_FIGS"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pq, res, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
COR = {2018: "#7f7f7f", 2022: "#2ca02c", 2026: "#d62728"}

# 1) H3: atraso de fechamento (minutos apos o horario nominal), 2o turno, sem exterior
fig, ax = plt.subplots(figsize=(7.5, 4))
bins = np.r_[-5, np.arange(0, 20, 1), 20, 40, 60, 90, 115, 125, 150]
for a in (2018, 2022, 2026):
    d = pd.read_parquet(os.path.join(pq, f"bu_{a}_t2.parquet"))
    d = d[(d.SG_UF != "ZZ") & d.atraso_min.notna() & d.DS_TIPO_URNA.str.upper().eq("APURADA")]
    h, e = np.histogram(d.atraso_min.clip(-5, 149), bins=bins)
    ax.step(e[:-1], np.maximum(h / len(d) * 100, 1e-4), where="post", label=f"{a} T2", color=COR[a])
ax.set_yscale("log"); ax.set_xlabel("minutos depois do horário nominal de fechamento (17h Brasília equivalente)"); ax.set_ylabel("% das seções (escala log)")
ax.axvline(15, color="#999", lw=.8, ls=":"); ax.axvline(115, color="#999", lw=.8, ls=":"); ax.legend(); ax.set_title("Fechamento das seções: 2018, 2022 e 2026", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(out, "h3_atraso_fechamento.png"), dpi=110); plt.close(fig)

# 2) A2: frequencia de perda de votos absolutos por faixa de terceiros/candidato (espelho 2022 PT x 2026 oponente)
p = os.path.join(res, "A2_a2_mecanismo_pool.csv")
if os.path.exists(p):
    t = pd.read_csv(p)
    ordem = ["<0,1", "0,1-0,2", "0,2-0,4", "0,4-0,8", ">=0,8"]
    t = t.set_index(["cand", "razao_terceiros_sobre_cand_T1"])
    fig, ax = plt.subplots(figsize=(7.5, 4)); x = np.arange(len(ordem)); w = .2
    for i, (cand, ano, lab, cor) in enumerate((("PT", 2022, "PT 2022 (líder do T1)", "#2ca02c"), ("OPO", 2026, "oponente 2026 (líder do T1)", "#d62728"), ("OPO", 2022, "oponente 2022", "#98df8a"), ("PT", 2026, "PT 2026", "#ff9896"))):
        ax.bar(x + (i - 1.5) * w, [t.loc[(cand, f), str(ano)] for f in ordem], w, label=lab, color=cor)
    ax.set_xticks(x); ax.set_xticklabels(ordem); ax.set_xlabel("votos de terceiros no T1 / votos do candidato no T1, na seção"); ax.set_ylabel("% das seções em que o candidato perde votos absolutos")
    ax.legend(fontsize=8); ax.set_title("Quem perde votos do T1 ao T2 (comparecimento estável ou crescente)", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(out, "a2_espelho_perdas.png"), dpi=110); plt.close(fig)

# 3) A5: votos depois do horario nominal por estrato e hora do ultimo voto nas secoes tardias
p = os.path.join(res, "A5_a5_votos_apos_horario_nominal.csv")
if os.path.exists(p):
    t = pd.read_csv(p); t = t[t.ano == 2026]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    nomes = {"L": "fecharam ≥115 min depois", "C": "controles (mesmo local)", "R": "amostra aleatória", "H": "comparecimento ≥95%", "RR_completo": "Roraima (todas)"}
    ax.bar([nomes.get(e, e) for e in t.estrato], t.media_por_secao, color="#1d4e89")
    ax.set_ylabel("votos computados depois do horário nominal, por seção"); ax.set_title("Votos depois do horário nominal, 2º turno de 2026 (logs das urnas)", fontsize=10)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right", fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(out, "a5_votos_apos_nominal.png"), dpi=110); plt.close(fig)
print("figuras em", out)
