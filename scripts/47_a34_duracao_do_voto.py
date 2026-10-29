#!/usr/bin/env python3
"""A34 (Adendo 16, 16a): duracao do voto por eleitor (habilitacao ate o voto confirmado), por secao-dia. Metricas D1 a D6, comparacao pareada 2026/2o turno contra 2022/2o turno nas mesmas secoes,
regra do percentil 99, faixa dos placebos, modelos M1 a M4 (EF de local, placebo 2022), placebo de forma (lado errado), teto.
Uso: python -I 47_a34_duracao_do_voto.py DIR_LOGS_F34 DIR_PARQUET DIR_AMOSTRA DIR_SAIDA"""
import glob
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, Registro, fe_ols, MARGEM

NMIN = 100
HAB = "A34"
PRINC = ("R", "RR_completo")


def metricas(L):
    def f(r):
        d = np.asarray(r.dur, float); g = np.asarray(r.gap, float)
        out = dict(D1=np.median(d) if len(d) else np.nan, D2=np.percentile(d, 1) if len(d) else np.nan, D3=(d < 20).mean() if len(d) else np.nan, D4=d.std(ddof=1) if len(d) > 1 else np.nan,
                   D5=r.n_sem_voto / r.n_hab if r.n_hab else np.nan, D6=(d <= 3).mean() if len(d) else np.nan, n_dur=len(d),
                   W1=np.median(g) if len(g) else np.nan, W3=(g < 20).mean() if len(g) else np.nan, W6=(g <= 3).mean() if len(g) else np.nan)
        return pd.Series(out)
    return pd.concat([L.reset_index(drop=True), L.apply(f, axis=1).reset_index(drop=True)], axis=1)


def carrega(dl, damostra, pq):
    L = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(dl, "*.parquet")))], ignore_index=True)
    L = L[L.dia.isin([1, 2]) & L.dur.notna()].rename(columns={"uf": "SG_UF", "cd_municipio": "CD_MUNICIPIO", "zona": "NR_ZONA", "secao": "NR_SECAO", "dia": "turno"})
    M = pd.read_parquet(os.path.join(damostra, "A32_medidas_secao_dia.parquet"))[KEY + ["ano", "turno", "consistente", "estrato"]]
    L = L.merge(M, on=KEY + ["ano", "turno"], how="left")
    cobertura = L.groupby(["ano", "turno"]).agg(secoes_dia_com_log=("secao" if "secao" in L else "NR_SECAO", "size"), consistentes=("consistente", "sum")).reset_index()
    L = L[L.consistente.fillna(False) & (L.n_hab >= NMIN)].copy()
    L = metricas(L)
    L["sec"] = L.SG_UF + "_" + L.CD_MUNICIPIO.astype(str) + "_" + L.NR_ZONA.astype(str) + "_" + L.NR_SECAO.astype(str)
    L["mun"] = L.SG_UF + "_" + L.CD_MUNICIPIO.astype(str)
    cobertura["incluidas_100_hab_ou_mais"] = [int(((L.ano == a) & (L.turno == t)).sum()) for a, t in zip(cobertura.ano, cobertura.turno)]
    return L, cobertura


def dif_pareada(L, a1, t1, a0, t0, col):
    x = L[(L.ano == a1) & (L.turno == t1)].set_index("sec"); y = L[(L.ano == a0) & (L.turno == t0)].set_index("sec")
    j = x[[col, "mun"]].join(y[[col]], rsuffix="_0", how="inner").dropna()
    d = (j[col] - j[col + "_0"])
    g = d.groupby(j.mun).agg(["sum", "size"]); n = int(g["size"].sum()); m = float(d.mean())
    res = d - m; sc = res.groupby(j.mun).sum(); G = len(sc)
    se = float(np.sqrt((sc ** 2).sum() * G / (G - 1)) / n) if G > 1 else np.nan
    return dict(secoes_pareadas=n, municipios=G, media_2026_menos_2022=m, ep=se, z=m / se if se else np.nan)


def main(dl, pq, damostra, saida):
    os.makedirs(saida, exist_ok=True)
    L, cob = carrega(dl, damostra, pq); cob.to_csv(os.path.join(saida, "A34_cobertura.csv"), index=False)
    # --- descritivo por ano e turno
    desc = []
    for (a, t), g in L.groupby(["ano", "turno"]):
        row = dict(ano=a, turno=t, secoes_dia=len(g), duracoes=int(g.n_dur.sum()), pct_habilitacoes_sem_voto=100 * float(g.n_sem_voto.sum() / g.n_hab.sum()))
        for m in ("D1", "D2", "D3", "D4", "D6", "W1", "W3"):
            for q in (5, 50, 95, 99):
                row[f"{m}_p{q}"] = float(g[m].quantile(q / 100))
            row[f"{m}_media"] = float(g[m].mean())
        desc.append(row)
    DS = pd.DataFrame(desc); DS.to_csv(os.path.join(saida, "A34_descritivo.csv"), index=False)
    # --- comparacao pareada 2026/T2 contra 2022/T2 e, como referencia, 2026/T1 contra 2022/T1
    par = []
    for m in ("D1", "D2", "D3", "D4", "D5", "D6", "W1", "W3"):
        for (t, rot) in ((2, "2026/2o turno contra 2022/2o turno"), (1, "2026/1o turno contra 2022/1o turno (referencia)")):
            par.append(dict(metrica=m, comparacao=rot, **dif_pareada(L, 2026, t, 2022, t, m)))
    PAR = pd.DataFrame(par); PAR.to_csv(os.path.join(saida, "A34_pareada.csv"), index=False)
    # --- regra do percentil 99 (D3, D6) e placebo de forma (W3, W6)
    p99 = []
    for m in ("D3", "D6", "W3", "W6"):
        ref = L[(L.ano == 2022) & (L.turno == 2)][m].dropna()
        lim = float(ref.quantile(0.99))
        for (a, t) in ((2026, 2), (2026, 1), (2022, 1), (2022, 2)):
            x = L[(L.ano == a) & (L.turno == t)][m].dropna()
            fr = float((x > lim).mean()); n = len(x); ep = float(np.sqrt(0.01 * 0.99 / n))
            p99.append(dict(metrica=m, ano=a, turno=t, limiar_p99_2022T2=lim, secoes=n, fracao_acima=fr, esperado=0.01, ep_binomial=ep, excesso=bool((fr - 0.01) > 2 * ep) if (a, t) == (2026, 2) else np.nan))
    P99 = pd.DataFrame(p99); P99.to_csv(os.path.join(saida, "A34_regra_p99.csv"), index=False)
    # --- faixa dos placebos (quantis de 2026/T2 dentro de [min, max] dos tres placebos)
    faixa = []
    for m in ("D1", "D3", "D6", "D4"):
        for q in (50, 90, 99):
            v = {(a, t): float(L[(L.ano == a) & (L.turno == t)][m].quantile(q / 100)) for a, t in ((2026, 2), (2022, 1), (2022, 2), (2026, 1))}
            pl = [v[(2022, 1)], v[(2022, 2)], v[(2026, 1)]]
            faixa.append(dict(metrica=m, quantil=q, v_2026T2=v[(2026, 2)], placebo_min=min(pl), placebo_max=max(pl), dentro_da_faixa=bool(min(pl) <= v[(2026, 2)] <= max(pl))))
    FX = pd.DataFrame(faixa); FX.to_csv(os.path.join(saida, "A34_faixa_placebos.csv"), index=False)
    # --- modelos M1, M2, M4 (EF de local) e M3 (descritivo)
    bw = {(a, t): pd.read_parquet(os.path.join(pq, f"bu_{a}_t{t}.parquet"), columns=KEY + ["turnout", "lula_sh", "uf_local", "valid2", "QT_APTOS", "manual_rate", "lula", "dir", "DS_TIPO_URNA"]) for a in (2022, 2026) for t in (1, 2)}
    def junta(a, t=2):
        w = L[(L.ano == a) & (L.turno == t)]
        b2 = bw[(a, t)]; b1 = bw[(a, 1)][KEY + ["turnout", "lula_sh"]].rename(columns={"turnout": "turnout_t1", "lula_sh": "lula_sh_t1"})
        w = w.merge(b2, on=KEY, how="left").merge(b1, on=KEY, how="left")
        d1 = L[(L.ano == a) & (L.turno == 1)][KEY + ["D1"]].rename(columns={"D1": "D1_t1"})
        w = w.merge(d1, on=KEY, how="left")
        return w[w.DS_TIPO_URNA.str.upper().eq("APURADA") & (w.valid2 >= 30)]
    A = {a: junta(a) for a in (2022, 2026)}
    b26 = bw[(2026, 2)]; b26 = b26[b26.SG_UF != "ZZ"]
    expo_v, expo_a = float(b26.valid2.sum()), float(b26.QT_APTOS.sum())
    reg = Registro(); mod = []
    for amostra, filtro in (("principal: R + Roraima completa", lambda w: w[w.estrato.isin(PRINC)]), ("sensibilidade: todos os estratos (rotulada, selecao no desfecho)", lambda w: w)):
        for (nome, y, xs, sinal, fator, expo, sent) in (("M1 participacao de Lula ~ D3", "lula_sh", ["D3", "lula_sh_t1"], 1, 2.0, expo_v, "PT"),
                                                        ("M2 comparecimento ~ D3", "turnout", ["D3", "turnout_t1"], 1, 1.0, expo_a, "PT+OPO"),
                                                        ("M4 D1 ~ taxa de liberacao manual do BU (excesso = D1 mais curto)", "D1", ["manual_rate", "D1_t1"], -1, 1.0, np.nan, "PT+OPO")):
            try:
                r26 = fe_ols(filtro(A[2026]).dropna(subset=[xs[0]]), y, xs, "uf_local").iloc[0]; r22 = fe_ols(filtro(A[2022]).dropna(subset=[xs[0]]), y, xs, "uf_local").iloc[0]
            except ValueError as e:
                mod.append(dict(amostra=amostra, modelo=nome, erro=str(e))); continue
            mod.append(dict(amostra=amostra, modelo=nome, coef_2026=float(r26.coef), ep_2026=float(r26.se), coef_2022_placebo=float(r22.coef), ep_2022=float(r22.se), n_2026=int(r26.n), locais_2026=int(r26.grupos)))
            if amostra.startswith("principal"):
                reg.add(HAB, f"{nome}: 2026/T2 contra 2022/T2 (EF de local, controle do T1)", sinal * float(r26.coef), float(r26.se), [("2022/T2", sinal * float(r22.coef), float(r22.se))], expo=expo, fator=fator, sentido=sent,
                        nota=f"{int(r26.n)} secoes, {int(r26.grupos)} locais; teto = extrapolacao do coeficiente para todo o pais, so limite superior")
    MOD = pd.DataFrame(mod); MOD.to_csv(os.path.join(saida, "A34_modelos.csv"), index=False)
    fam = reg.frame(); fam.to_csv(os.path.join(saida, "A34_testes.csv"), index=False)
    # M3 descritivo: variacao de D1 2022 -> 2026
    w = A[2026].merge(A[2022][KEY + ["D1"]].rename(columns={"D1": "D1_2022"}), on=KEY, how="inner"); w["dD1"] = w.D1 - w.D1_2022
    m3 = pd.DataFrame([dict(secoes=len(w), media_dD1_s=float(w.dD1.mean()), mediana_dD1_s=float(w.dD1.median()), p5=float(w.dD1.quantile(.05)), p95=float(w.dD1.quantile(.95)))]); m3.to_csv(os.path.join(saida, "A34_M3_descritiva.csv"), index=False)
    # --- teto
    x = A[2026]; lim = float(L[(L.ano == 2022) & (L.turno == 2)].D3.quantile(0.99)); fl = x[x.D3 > lim]
    b = bw[(2026, 2)].copy(); b["loc_l"] = b.groupby("uf_local").lula.transform("sum") - b.lula; b["loc_v"] = b.groupby("uf_local").valid2.transform("sum") - b.valid2
    fl = fl.merge(b[KEY + ["loc_l", "loc_v"]], on=KEY, how="left"); fl["s_viz"] = fl.loc_l / fl.loc_v.where(fl.loc_v > 0)
    n26 = len(x); frac = len(fl) / n26 if n26 else np.nan
    teto = dict(limiar_D3_p99_2022T2=lim, secoes_amostra_2026T2=n26, secoes_acima=len(fl), fracao_acima=frac,
                a_fator1_votos_validos_das_secoes_acima=float(fl.valid2.sum()), b_fator2_ganho_de_lula_sobre_a_vizinhanca=float((np.maximum(0, fl.lula_sh - fl.s_viz.fillna(fl.lula_sh)) * fl.valid2 * 2).sum()),
                extrapolacao_nacional_excesso_sobre_1pct_fator1=float(max(0, frac - 0.01) * 497_897 * (fl.valid2.mean() if len(fl) else 0)), pct_da_margem_extrapolacao=100 * float(max(0, frac - 0.01) * 497_897 * (fl.valid2.mean() if len(fl) else 0)) / MARGEM,
                nota="teto de pior caso, nao estimativa; (a) e (b) valem so para a amostra de logs; a extrapolacao vale so para o excesso acima de 1%")
    pd.DataFrame([teto]).to_csv(os.path.join(saida, "A34_teto.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(cob.to_string()); print(DS[["ano", "turno", "secoes_dia", "duracoes", "D1_p5", "D1_p50", "D1_p95", "D3_p50", "D3_p99", "D6_p50", "D6_p99", "W1_p50", "W3_p50", "pct_habilitacoes_sem_voto"]].round(3).to_string())
    print(PAR.round(4).to_string()); print(P99.round(4).to_string()); print(FX.round(4).to_string()); print(MOD.round(5).to_string())
    print(fam[["teste", "est_2026T2", "ep", "b_comp", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].round(4).to_string() if len(fam) else "sem familia"); print(m3.round(2).to_string()); print(pd.Series(teto).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
