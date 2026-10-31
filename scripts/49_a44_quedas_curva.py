#!/usr/bin/env python3
"""A44: quedas verticais na curva acumulada de apuração (Adendo 20, 31/10/2026).

Reproduz o "percentual acumulado de votos" do 2º turno de 2026 em três versões:
  (a) X = BUs recebidos (DT_RECEBIMENTO_BU_HOR_TSE), Y = % de Lula sobre os recebidos;
  (b) X = BUs totalizados (DT_PRIM_TOT_PARCIAL_HOR_TSE), Y = % sobre os totalizados;
  (c) mistas (X de uma contagem, Y da outra), nos dois sentidos.
Para cada descontinuidade (|delta| >= limiar entre minutos consecutivos): forense do lote
(horário, UF, municípios, nº de BUs, votos) e comparação efeito calculado x observado.
Reafirma H9: o total final é independente da ordem e bate com a soma dos BUs.

Saídas: results/fase5/A44_* e figura docs/img/a44_curva_3versoes.(png|svg) (+ _m com argv[2]="m").
Uso: ./venv/bin/python scripts/49_a44_quedas_curva.py RAIZ [m]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficos"))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common import AZUL, VERM, AMBAR, CINZA, TXT, MARGEM, salva

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
MOVEL = len(sys.argv) > 2 and sys.argv[2] == "m"
PQ = os.path.join(RAIZ, "parquet")
OUT = os.path.join(RAIZ, "results", "fase5")
os.makedirs(OUT, exist_ok=True)

LIMIAR = 0.02          # p.p. entre minutos consecutivos (regra operacional, ver memorando)
LIMIARES_SENS = [0.01, 0.05, 0.1]

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]

o = pd.read_parquet(os.path.join(PQ, "ordem_2026_t2.parquet"))
b = pd.read_parquet(os.path.join(PQ, "bu_2026_t2.parquet"),
                    columns=KEY + ["DS_TIPO_URNA", "lula", "dir", "valid2", "branco", "nulo", "QT_COMPARECIMENTO"])
b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")]   # inclui ZZ (exterior): o total oficial nacional inclui
d = o.merge(b, on=KEY, how="inner")
cobertura = dict(secoes_ordem=len(o), secoes_bu=len(b), secoes_pareadas=len(d))

# H9: total final independe da ordem e bate com a soma dos BUs
tot = dict(lula=int(d.lula.sum()), dir=int(d.dir.sum()), valid2=int(d.valid2.sum()),
           branco=int(d.branco.sum()), nulo=int(d.nulo.sum()), comparecimento=int(d.QT_COMPARECIMENTO.sum()))
tot["margem"] = tot["lula"] - tot["dir"]
tot["lula_pct_validos"] = 100 * tot["lula"] / tot["valid2"]
pd.DataFrame([{**cobertura, **tot}]).to_csv(os.path.join(OUT, "A44_h9_totais.csv"), index=False)

d["min_rec"] = d.DT_RECEBIMENTO_BU_HOR_TSE.dt.floor("min")
d["min_tot"] = d.DT_PRIM_TOT_PARCIAL_HOR_TSE.dt.floor("min")

t0 = min(d.min_rec.min(), d.min_tot.min())
t1 = max(d.min_rec.max(), d.min_tot.max())
idx = pd.date_range(t0, t1, freq="min")

gR = d.groupby("min_rec").agg(n=("lula", "size"), lula=("lula", "sum"), val=("valid2", "sum"))
gT = d.groupby("min_tot").agg(n=("lula", "size"), lula=("lula", "sum"), val=("valid2", "sum"))
m = pd.DataFrame(index=idx)
for g, p in ((gR, "rec"), (gT, "tot")):
    for c in ("n", "lula", "val"):
        m[f"{c}_{p}"] = g[c].reindex(idx).fillna(0)
m = m.fillna(0).cumsum()
m["share_rec"] = 100 * m.lula_rec / m.val_rec
m["share_tot"] = 100 * m.lula_tot / m.val_tot
m["x_rec"] = 100 * m.n_rec / len(d)
m["x_tot"] = 100 * m.n_tot / len(d)
m.index.name = "minuto"
m.to_csv(os.path.join(OUT, "A44_curva_minuto.csv"))

VERSOES = {
    "a_recebidos": ("x_rec", "share_rec", "rec"),
    "b_totalizados": ("x_tot", "share_tot", "tot"),
    "c1_xRec_yTot": ("x_rec", "share_tot", "tot"),
    "c2_xTot_yRec": ("x_tot", "share_rec", "rec"),
}

eventos, resumo = [], []
for nome, (xc, yc, fonte) in VERSOES.items():
    y = m[yc].values
    dy = np.diff(y)
    mascara = np.abs(dy) >= LIMIAR
    resumo.append(dict(versao=nome, pontos=len(y),
                       quedas_0p02=int((dy <= -LIMIAR).sum()), saltos_0p02=int((dy >= LIMIAR).sum()),
                       max_queda_pp=float(dy.min()), max_salto_pp=float(dy.max()),
                       **{f"eventos_{str(t).replace('.', 'p')}": int((np.abs(dy) >= t).sum()) for t in LIMIARES_SENS}))
    for i in np.where(mascara)[0]:
        minuto = m.index[i + 1]
        g = gT if fonte == "tot" else gR
        lote = g.loc[[minuto]] if minuto in g.index else None
        d_ant, d_dep = y[i], y[i + 1]
        obs = d_dep - d_ant
        # efeito calculado do lote: recomputar a media acumulada sem/com o lote do minuto
        if lote is not None and len(lote) > 0:
            nl, ll, vl = float(lote.n.iloc[0]), float(lote.lula.iloc[0]), float(lote.val.iloc[0])
            N1, L1, V1 = (m.loc[minuto, f"n_{fonte}"], m.loc[minuto, f"lula_{fonte}"], m.loc[minuto, f"val_{fonte}"])
            N0, L0, V0 = N1 - nl, L1 - ll, V1 - vl
            y_sem = 100 * L0 / V0 if V0 > 0 else np.nan
            y_com = 100 * L1 / V1 if V1 > 0 else np.nan
            efeito = y_com - y_sem
            share_lote = 100 * ll / vl if vl > 0 else np.nan
        else:
            nl, efeito, share_lote = 0, 0.0, np.nan
        # composicao do lote
        col = "min_tot" if fonte == "tot" else "min_rec"
        dd = d[d[col] == minuto]
        ufs = dd.SG_UF.value_counts().head(5)
        muns = dd.groupby(["SG_UF", "CD_MUNICIPIO"]).size().sort_values(ascending=False).head(5)
        eventos.append(dict(versao=nome, minuto=minuto, direcao="queda" if obs < 0 else "salto",
                            delta_obs_pp=float(obs), delta_calc_pp=float(efeito),
                            dif_abs_pp=float(abs(efeito - obs)),
                            bus=int(nl), lote_share_lula=float(share_lote),
                            share_antes=float(d_ant), share_depois=float(d_dep),
                            top_ufs="; ".join(f"{u}:{c}" for u, c in ufs.items()),
                            top_municipios="; ".join(f"{uf}/{mun}:{c}" for (uf, mun), c in muns.items())))

E = pd.DataFrame(eventos)
R = pd.DataFrame(resumo)
E.to_csv(os.path.join(OUT, "A44_eventos.csv"), index=False)
R.to_csv(os.path.join(OUT, "A44_resumo_versoes.csv"), index=False)

# placebo 2022 T2: mesmas versoes, mesmos limiares (contexto: quedas iniciais sao aritmetica de base pequena?)
o22 = pd.read_parquet(os.path.join(PQ, "ordem_2022_t2.parquet"))
b22 = pd.read_parquet(os.path.join(PQ, "bu_2022_t2.parquet"), columns=KEY + ["DS_TIPO_URNA", "lula", "dir", "valid2"])
b22 = b22[b22.DS_TIPO_URNA.str.upper().eq("APURADA")]
d22 = o22.merge(b22, on=KEY, how="inner")
d22["min_rec"] = d22.DT_RECEBIMENTO_BU_HOR_TSE.dt.floor("min")
d22["min_tot"] = d22.DT_PRIM_TOT_PARCIAL_HOR_TSE.dt.floor("min")
idx22 = pd.date_range(min(d22.min_rec.min(), d22.min_tot.min()), max(d22.min_rec.max(), d22.min_tot.max()), freq="min")
gR22 = d22.groupby("min_rec").agg(n=("lula", "size"), lula=("lula", "sum"), val=("valid2", "sum"))
gT22 = d22.groupby("min_tot").agg(n=("lula", "size"), lula=("lula", "sum"), val=("valid2", "sum"))
m22 = pd.DataFrame(index=idx22)
for g, p in ((gR22, "rec"), (gT22, "tot")):
    for c in ("n", "lula", "val"):
        m22[f"{c}_{p}"] = g[c].reindex(idx22).fillna(0)
m22 = m22.fillna(0).cumsum()
m22["share_rec"] = 100 * m22.lula_rec / m22.val_rec
m22["share_tot"] = 100 * m22.lula_tot / m22.val_tot
r22 = []
for nome, yc in (("a_recebidos", "share_rec"), ("b_totalizados", "share_tot")):
    dy = np.diff(m22[yc].values)
    dy = dy[~np.isnan(dy)]
    r22.append(dict(versao=nome, pontos=len(dy) + 1, quedas_0p02=int((dy <= -LIMIAR).sum()),
                    saltos_0p02=int((dy >= LIMIAR).sum()), max_queda_pp=float(dy.min()), max_salto_pp=float(dy.max()),
                    **{f"eventos_{str(t).replace('.', 'p')}": int((np.abs(dy) >= t).sum()) for t in LIMIARES_SENS}))
R22 = pd.DataFrame(r22)
R22.to_csv(os.path.join(OUT, "A44_resumo_versoes_2022.csv"), index=False)
print("\n== placebo 2022 T2 ==")
print(R22.to_string(index=False))

print("== cobertura e H9 ==")
print(cobertura)
print(tot)
print("\n== resumo por versao (limiar 0,02 p.p.) ==")
print(R.to_string(index=False))
if len(E):
    print("\n== eventos ==")
    print(E.to_string(index=False))
else:
    print("\nsem eventos acima do limiar em nenhuma versao")

# figura: eixo Y 0-100% (regra de exibicao), margem final marcada
fig, ax = plt.subplots(figsize=((4.2, 3.4) if MOVEL else (7.6, 3.6)))
x = m.index
ax.plot(x, m.share_rec, color=AZUL, lw=1.2, label="(a) recebidos / sobre recebidos")
ax.plot(x, m.share_tot, color=VERM, lw=1.2, label="(b) totalizados / sobre totalizados")
ax.plot(m.n_rec.index, m.share_tot.where(m.n_rec.diff().fillna(1) > 0), color=AMBAR, lw=0.8, alpha=0.8,
        label="(c) mista: X recebidos, Y totalizados")
ax.axhline(tot["lula_pct_validos"], color=TXT, lw=0.9, ls=":",
           label=f"final: {tot['lula_pct_validos']:.2f}% (margem {MARGEM:,} votos)".replace(",", "."))
ax.set_ylim(0, 100)
ax.set_ylabel("% acumulado de Lula (votos válidos)")
ax.set_xlabel("25/10/2026 (horário de Brasília, TSE)")
ax.legend(fontsize=7.5 if MOVEL else 8.5, frameon=False, loc="center right")
fig.tight_layout(pad=0.4)
salva(fig, RAIZ, "a44_curva_3versoes", "Curva acumulada de apuração, 2º turno de 2026, em três versões",
      "Percentual acumulado de Lula sobre os votos válidos em três versões: (a) boletins recebidos, (b) totalizados e (c) mista (eixo X de uma contagem e percentual da outra). Eixo Y de 0 a 100% com o resultado final marcado (51,78%, margem de 4.430.191 votos). Nenhuma versão apresenta queda vertical.")
print("figura a44_curva_3versoes" + ("_m" if MOVEL else "") + " salva")
