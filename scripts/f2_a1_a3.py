"""Fase 2: A1 (curva de apuracao), A2 (transicoes T1->T2), A3 (origem dos votos). Pre-registro: Adendo 4.

Convencao: PT = candidato 13 (coluna lula); OPO = oponente do 2o turno (coluna dir)."""
import os
import numpy as np
import pandas as pd
from scipy import stats
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, par_ano, fe_ols
from h1_h4 import tenta

NOME_OPO = {2014: "Aecio", 2018: "Bolsonaro", 2022: "Bolsonaro", 2026: "Flavio"}


# ----------------------------------------------------------------------------------------------------- A1
def _curva(D, out, ano, turno, reps, seed=7, K=1000):
    p = os.path.join(out["_parquet"], f"ordem_{ano}_t{turno}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"A1 {ano}/T{turno}: falta {p} (o produto detalhe_votacao_secao de {ano} nao traz horario de totalizacao)")
    o = pd.read_parquet(p)
    b = D[(ano, turno)]
    b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")].merge(o, on=KEY, how="left")
    if b.DT_PRIM_TOT_PARCIAL_HOR_TSE.isna().any():
        raise NaoExecutado(f"A1 {ano}/T{turno}: {int(b.DT_PRIM_TOT_PARCIAL_HOR_TSE.isna().sum())} secoes sem horario de primeira totalizacao")
    rng = np.random.default_rng(seed)
    b = b.assign(_r=rng.random(len(b))).sort_values(["DT_PRIM_TOT_PARCIAL_HOR_TSE", "DT_RECEBIMENTO_BU_HOR_TSE", "_r"]).reset_index(drop=True)
    l = b.lula.values.astype(np.float64); d = b["dir"].values.astype(np.float64)
    N = len(b)
    uf = pd.factorize(b.SG_UF)[0]
    idx = np.ceil(np.arange(1, K + 1) * N / K).astype(int) - 1
    def share(lv, dv):
        cl, cd = np.cumsum(lv), np.cumsum(dv)
        return (cl[idx] / (cl[idx] + cd[idx]))
    real = share(l, d)
    # nulo A: ordem aleatoria total
    A = np.empty((reps, K))
    for r in range(reps):
        o_ = rng.permutation(N); A[r] = share(l[o_], d[o_])
    # nulo B: mantem a sequencia de UFs, embaralha as secoes dentro de cada UF
    slots = [np.flatnonzero(uf == u) for u in range(uf.max() + 1)]
    Bm = np.empty((reps, K))
    for r in range(reps):
        order = np.empty(N, dtype=np.int64)
        for s in slots:
            order[s] = rng.permutation(s)
        Bm[r] = share(l[order], d[order])
    k0 = max(1, int(0.01 * K))                       # a partir de 1% das secoes
    medA, medB = np.median(A, axis=0), np.median(Bm, axis=0)
    sdB = Bm.std(axis=0, ddof=1)
    zB = np.abs(Bm[:, k0:] - medB[k0:]) / sdB[k0:]
    c95 = float(np.quantile(zB.max(axis=1), 0.95))
    dev = np.abs(real - medB)[k0:]
    z_real = dev / sdB[k0:]
    out_run, cur = 0, 0
    for v in (z_real > c95):
        cur = cur + 1 if v else 0; out_run = max(out_run, cur)
    maxdev_pp = 100 * float(dev.max())
    k10 = int(0.10 * K)
    maxdev10 = 100 * float(np.abs(real - medB)[k10:].max())                 # POSTERIOR (nao pre-registrado): a partir de 10% das secoes
    maxdev10_reps = 100 * np.abs(Bm[:, k10:] - medB[k10:]).max(axis=1)
    maxdev_reps = 100 * np.abs(Bm[:, k0:] - medB[k0:]).max(axis=1)
    kj = max(2, int(0.05 * K))
    J = lambda s: np.abs(np.diff(s[kj - 1:])).max()
    J_real = float(J(real)); J_B = np.array([J(x) for x in Bm])
    explicada = 1 - float(np.sum((real[k0:] - medB[k0:]) ** 2) / np.sum((real[k0:] - medA[k0:]) ** 2))
    t = b.DT_PRIM_TOT_PARCIAL_HOR_TSE
    res = dict(ano=ano, turno=turno, secoes=N, share_final=float(real[-1]), maxdev_vs_B_pp=maxdev_pp, maxdev_vs_B_pp_posterior_ge10pct=maxdev10, maxdev_B_nulo_p95_pp=float(np.quantile(maxdev_reps, .95)),
               maxdev_vs_A_pp=100 * float(np.abs(real - medA)[k0:].max()), maior_sequencia_fora_envelope=out_run, c95_simultaneo=c95,
               salto_max_real=J_real, salto_max_B_p95=float(np.quantile(J_B, .95)), p_salto=float((J_B >= J_real).mean()), fracao_explicada_por_geografia=explicada,
               pct_secoes_totalizadas_antes_das_19h=100 * float((t.dt.hour < 19).mean()), primeira=str(t.min()), ultima=str(t.max()))
    fig = dict(x=100 * (idx + 1) / N, real=100 * real, medA=100 * medA, loA=100 * np.quantile(A, .025, axis=0), hiA=100 * np.quantile(A, .975, axis=0),
               medB=100 * medB, loB=100 * (medB - c95 * sdB), hiB=100 * (medB + c95 * sdB))
    # ordem de chegada por UF
    b["pos"] = (np.arange(N) + 1) / N
    uf_tab = b.groupby("SG_UF").agg(secoes=("lula", "size"), posicao_mediana=("pos", "median"), p10=("pos", lambda s: s.quantile(.1)), p90=("pos", lambda s: s.quantile(.9)),
                                    share_pt=("lula", "sum"), opo=("dir", "sum"))
    uf_tab["share_pt"] = uf_tab.share_pt / (uf_tab.share_pt + uf_tab.opo)
    uf_tab = uf_tab.drop(columns="opo").sort_values("posicao_mediana")
    return res, fig, uf_tab, maxdev_reps


def a1(D, reg, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    reps = int(os.environ.get("AUDITORIA_REPS", "1000"))
    cfg = [(2026, 2), (2026, 1), (2022, 2), (2018, 2)]
    R, F, U, MD = {}, {}, {}, {}
    for (a, t) in cfg:
        r = tenta(out, f"A1 {a}/T{t}", _curva, D, out, a, t, reps)
        if r is not None:
            R[(a, t)], F[(a, t)], U[(a, t)], MD[(a, t)] = r
    if (2014, 2) not in R:
        out.setdefault("nao_executados", []).append(("A1 2014/T2", "o produto detalhe_votacao_secao de 2014 nao tem DT_RECEBIMENTO_BU_HOR_TSE nem DT_PRIM_TOT_PARCIAL_HOR_TSE; o BWeb de 2014 so tem a data (sem hora) de recebimento"))
        print("NAO EXECUTADO [A1 2014/T2]: sem horario de totalizacao em 2014", flush=True)
    out["a1_resumo"] = pd.DataFrame(R.values())
    if (2026, 2) not in R:
        raise NaoExecutado("A1: 2026/T2 nao calculado")
    for k, u in U.items():
        out[f"a1_ordem_por_uf_{k[0]}_T{k[1]}"] = u.reset_index()
    figdir = os.path.join(out["_saida"], "figs"); os.makedirs(figdir, exist_ok=True)
    fig, ax = plt.subplots(1, len(R), figsize=(4.6 * len(R), 4), squeeze=False)
    for j, (k, f) in enumerate(F.items()):
        a_ = ax[0][j]; x = f["x"]; m = x >= 1
        a_.fill_between(x[m], f["loA"][m], f["hiA"][m], color="#cccccc", label="ordem aleatória (95%)")
        a_.fill_between(x[m], f["loB"][m], f["hiB"][m], color="#9ecae1", alpha=.8, label="aleatória dentro da UF (envelope)")
        a_.plot(x[m], f["real"][m], color="#d62728", lw=1.4, label="curva real")
        a_.set_title(f"{k[0]} T{k[1]}", fontsize=9); a_.set_xlabel("% das seções totalizadas"); a_.set_ylabel("% acumulado do PT")
        if j == 0:
            a_.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(figdir, "a1_curva_apuracao.png"), dpi=110); plt.close(fig)
    pd.DataFrame({f"{k[0]}T{k[1]}_{c}": v for k, f in F.items() for c, v in f.items()}).round(4).to_csv(os.path.join(out["_saida"], "A1_curvas_pontos.csv"), index=False)
    est = R[(2026, 2)]["maxdev_vs_B_pp"]; ep = float(np.std(MD[(2026, 2)], ddof=1))
    pl = [(f"{a}/T{t}", R[(a, t)]["maxdev_vs_B_pp"], float(np.std(MD[(a, t)], ddof=1))) for (a, t) in R if (a, t) != (2026, 2)]
    reg.add("A1", "curva de apuracao: desvio maximo da curva real contra permutacao dentro da UF (p.p. do PT)", est, ep, pl,
            nota="efeito na soma final: 0 por construcao (a ordem nao muda o total); teste de forma, sem conversao em votos",
            ressalva="o envelope B (permutacao dentro da UF) e rejeitado nos quatro anos; a partir de 10% das secoes o desvio de 2026/T2 fica abaixo dos placebos (analise posterior)")
    out["a1_nota"] = ("Nao executado: comparacao numerica com o grafico 'Evolucao da apuracao' do g1 (25/10/2026), porque o grafico nao foi fornecido como dado. "
                      "A pausa da divulgacao a 0,25% das secoes e a retomada apos 19h estao documentadas so por imprensa (ver docs).")


# ----------------------------------------------------------------------------------------------------- A2
def _pares(D, ano):
    w = par_ano(D, ano, minvalid=1)
    w["comp"], w["comp_t1"] = w.QT_COMPARECIMENTO, w.QT_COMPARECIMENTO_t1
    return w


def a2(D, reg, out):
    anos = [a for a in (2014, 2018, 2022, 2026) if a in out["anos"]]
    linhas, resid = [], {}
    for a in anos:
        w = _pares(D, a)
        est = (w.comp >= 0.98 * w.comp_t1) & (w.comp_t1 >= 30)
        for cand, col, col1 in (("OPO", "dir", "dir_t1"), ("PT", "lula", "lula_t1")):
            perda = (w[col] < w[col1]) & est
            lost = float((w[col1] - w[col]).clip(lower=0)[perda].sum())
            n = int(est.sum())
            linhas.append(dict(ano=a, cand=cand, secoes_estaveis_ou_crescentes=n, secoes_com_perda=int(perda.sum()), pct_secoes=100 * perda.mean() / est.mean() if est.mean() else np.nan,
                               votos_perdidos=lost, pct_dos_votos_T1_do_cand_nessas_secoes=100 * lost / max(float(w[col1][est].sum()), 1),
                               pct_secoes_perda_acima_de_20pct_do_T1=100 * float(((w[col1] - w[col]) > 0.2 * w[col1])[est & (w[col1] >= 30)].mean())))
        # compressao: secoes em que o oponente venceu o T1; modelo de swing proporcional por municipio (EF de municipio, margem T1 como regressor)
        x = w[(w.valid2 >= 100) & (w.valid2_t1 >= 100)].copy()
        x["m1"] = (x.dir_t1 - x.lula_t1) / x.valid2_t1; x["m2"] = (x["dir"] - x.lula) / x.valid2
        x["mun"] = x.SG_UF + "_" + x.CD_MUNICIPIO.astype(str)
        r = tenta(out, f"A2 swing {a}", fe_ols, x, "m2", ["m1"], "mun")
        if r is None:
            continue
        g = x.groupby("mun")
        res = (x.m2 - g.m2.transform("mean")) - r.loc["m1", "coef"] * (x.m1 - g.m1.transform("mean"))
        resid[a] = res.values
        win = x[x.dir_t1 > x.lula_t1]
        lin_ = dict(ano=a, spec="margem T2 ~ margem T1 | municipio", coef_m1=r.loc["m1", "coef"], ep=r.loc["m1", "se"], n=int(r.n.iloc[0]), municipios=int(r.grupos.iloc[0]))
        linhas.append(lin_)
    tab = pd.DataFrame([l for l in linhas if "cand" in l]); out["a2_perdas"] = tab
    out["a2_swing"] = pd.DataFrame([l for l in linhas if "spec" in l])
    # forma do swing residual: KS e AD, criterio pre-registrado
    ks = {}
    ys = [a for a in anos if a in resid]
    for i, a in enumerate(ys):
        for b_ in ys[i + 1:]:
            ks[(a, b_)] = stats.ks_2samp(resid[a], resid[b_]).statistic
    rng = np.random.default_rng(3)
    ad = {}
    for i, a in enumerate(ys):
        for b_ in ys[i + 1:]:
            s1, s2 = rng.choice(resid[a], 20000, replace=False), rng.choice(resid[b_], 20000, replace=False)
            ad[(a, b_)] = stats.anderson_ksamp([s1, s2]).statistic
    out["a2_forma_ks_ad"] = pd.DataFrame([dict(par=f"{a} x {b}", ks=v, ad_subamostra_20k=ad[(a, b)]) for (a, b), v in ks.items()])
    out["a2_momentos"] = pd.DataFrame([dict(ano=a, assimetria=float(stats.skew(resid[a])), curtose_excesso=float(stats.kurtosis(resid[a])), dp=float(np.std(resid[a])),
                                             pct_acima_3dp=100 * float((np.abs(resid[a]) > 3 * np.std(resid[a])).mean())) for a in ys])
    if 2026 in ys:
        pl = [a for a in ys if a != 2026]
        d26 = {a: ks[tuple(sorted((a, 2026)))] for a in pl}
        pp = [ks[tuple(sorted((a, b)))] for i, a in enumerate(pl) for b in pl[i + 1:]]
        regra = dict(menor_ks_2026_vs_placebo=min(d26.values()), maior_ks_entre_placebos=max(pp) if pp else np.nan,
                     criterio_diferente=bool(min(d26.values()) > max(pp)) if pp else None)
        out["a2_criterio_forma"] = pd.DataFrame([regra])
    # POSTERIOR (nao pre-registrado): a frequencia de perda depende da razao (votos de terceiros no T1) / (votos do candidato no T1) da secao?
    mec = []
    bins_ = [0, .1, .2, .4, .8, 1e9]
    for a in anos:
        w = _pares(D, a)
        est = (w.comp >= 0.98 * w.comp_t1) & (w.comp_t1 >= 30)
        w = w.assign(terc1=w.nominal_t1 - w.lula_t1 - w.dir_t1)
        for cand, col, col1 in (("OPO", "dir", "dir_t1"), ("PT", "lula", "lula_t1")):
            x = w[est & (w[col1] >= 30)].copy()
            x["razao"] = pd.cut(x.terc1 / x[col1], bins_, right=False, labels=["<0,1", "0,1-0,2", "0,2-0,4", "0,4-0,8", ">=0,8"])
            for fx, g in x.groupby("razao", observed=True):
                mec.append(dict(ano=a, cand=cand, razao_terceiros_sobre_cand_T1=str(fx), secoes=len(g), pct_com_perda=100 * float((g[col] < g[col1]).mean())))
        tot = dict(ano=a, PT_T1=float(w.lula_t1.sum()), OPO_T1=float(w.dir_t1.sum()), TERC_T1=float(w.terc1.sum()))
    out["a2_mecanismo_pool"] = pd.DataFrame(mec).pivot_table(index=["cand", "razao_terceiros_sobre_cand_T1"], columns="ano", values="pct_com_perda").round(2).reset_index()
    # frequencia de perda do oponente (2026 vs placebos), teste de proporcao com IUT via registro
    t = tab[tab.cand == "OPO"].set_index("ano")
    if 2026 in t.index:
        def pe(a):
            p = t.loc[a, "pct_secoes"] / 100; n = t.loc[a, "secoes_estaveis_ou_crescentes"]
            return 100 * p, 100 * float(np.sqrt(p * (1 - p) / n))
        e26 = pe(2026); pls = [(f"{a} (Aecio/Bolsonaro)", *pe(a)) for a in anos if a != 2026]
        reg.add("A2", "oponente perde votos absolutos do T1 ao T2 em secao com comparecimento estavel ou crescente (% das secoes)", e26[0], e26[1], pls,
                nota="sem teto em votos: a perda do oponente nao e, por si, voto inserido; ver A3 para a contabilidade",
                ressalva="o placebo por papel (oponente) e inadequado: em 2022 o PT, lider do T1, perdeu votos em 12,6% das secoes, espelho dos 11,8% do oponente em 2026 (analise posterior)")


# ----------------------------------------------------------------------------------------------------- A3
def a3(D, reg, out):
    anos = [a for a in (2014, 2018, 2022, 2026) if a in out["anos"]]
    cont, coefs = [], []
    for a in anos:
        t1, t2 = D[(a, 1)], D[(a, 2)]
        t1, t2 = t1[t1.DS_TIPO_URNA.str.upper().eq("APURADA")], t2[t2.DS_TIPO_URNA.str.upper().eq("APURADA")]
        c = dict(ano=a, PT_T1=t1.lula.sum(), PT_T2=t2.lula.sum(), OPO_T1=t1["dir"].sum(), OPO_T2=t2["dir"].sum(),
                 TERCEIROS_T1=(t1.nominal - t1.lula - t1["dir"]).sum(), BN_T1=(t1.branco + t1.nulo).sum(), BN_T2=(t2.branco + t2.nulo).sum(),
                 COMP_T1=t1.QT_COMPARECIMENTO.sum(), COMP_T2=t2.QT_COMPARECIMENTO.sum())
        c["dPT"] = c["PT_T2"] - c["PT_T1"]; c["dOPO"] = c["OPO_T2"] - c["OPO_T1"]
        c["dCOMP"] = c["COMP_T2"] - c["COMP_T1"]; c["dBN"] = c["BN_T2"] - c["BN_T1"]
        c["pool"] = c["dCOMP"] + c["TERCEIROS_T1"] - c["dBN"]
        c["identidade_ok"] = abs((c["dPT"] + c["dOPO"]) - c["pool"]) <= 0.001 * c["pool"]
        c["pt_pct_do_pool"] = 100 * c["dPT"] / c["pool"]; c["opo_pct_do_pool"] = 100 * c["dOPO"] / c["pool"]
        cont.append(c)
        w = par_ano(D, a, minvalid=1)
        ap = w.QT_APTOS_t1.replace(0, np.nan)
        w = w.assign(mun=w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str), pt1=w.lula_t1 / ap, op1=w.dir_t1 / ap, te1=w.outros_pa_t1, bn1=w.bn_pa_t1,
                     ab1=1 - w.QT_COMPARECIMENTO_t1 / ap, pt2=w.lula / ap, op2=w.dir / ap)
        w = w.replace([np.inf, -np.inf], np.nan).dropna(subset=["pt1", "op1", "te1", "bn1", "ab1", "pt2", "op2"])
        X = w[["pt1", "op1", "te1", "bn1", "ab1"]].values
        wts = np.sqrt(w.QT_APTOS_t1.values)
        for desf, nome in (("pt2", "PT"), ("op2", "OPO")):
            y = w[desf].values
            b, *_ = np.linalg.lstsq(X * wts[:, None], y * wts, rcond=None)
            e = (y - X @ b) * wts
            cl = pd.factorize(w.mun)[0]; o = np.argsort(cl, kind="stable"); cs = cl[o]; st = np.r_[0, np.flatnonzero(cs[1:] != cs[:-1]) + 1]
            sc = np.add.reduceat((X * wts[:, None])[o] * e[o, None], st, axis=0)
            br = np.linalg.inv((X * wts[:, None]).T @ (X * wts[:, None])); V = br @ (sc.T @ sc) @ br
            for g, nm in enumerate(["PT_T1", "OPO_T1", "TERCEIROS_T1", "BRANCOS_NULOS_T1", "ABSTENCAO_T1"]):
                coefs.append(dict(ano=a, destino_T2=nome, origem_T1=nm, coef=float(b[g]), ep=float(np.sqrt(V[g, g]))))
    lb = []
    for a in anos:
        w = par_ano(D, a, minvalid=0)
        t1, t2 = D[(a, 1)].set_index(KEY), D[(a, 2)].set_index(KEY)
        j = t2.join(t1[["lula", "dir"]], rsuffix="_t1", how="inner")
        j = j[j.DS_TIPO_URNA.str.upper().eq("APURADA")]
        for cand, c2, c1 in (("OPO", "dir", "dir_t1"), ("PT", "lula", "lula_t1")):
            d_ = (j[c2] - j[c1])
            lb.append(dict(ano=a, cand=cand, secoes=len(j), secoes_com_perda_liquida=int((d_ < 0).sum()), pct_secoes=100 * float((d_ < 0).mean()), votos_perdidos_liquidos_somados=float((-d_).clip(lower=0).sum()),
                           ganho_liquido_nacional=float(d_.sum())))
    out["a3_perda_liquida_minima"] = pd.DataFrame(lb)
    out["a3_contabilidade"] = pd.DataFrame(cont)
    out["a3_ecologica"] = pd.DataFrame(coefs)
    fe = []
    for a in anos:
        w = par_ano(D, a, minvalid=1)
        ap = w.QT_APTOS_t1.replace(0, np.nan)
        w = w.assign(mun=w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str), pt1=w.lula_t1 / ap, op1=w.dir_t1 / ap, te1=w.outros_pa_t1, bn1=w.bn_pa_t1, pt2=w.lula / ap).replace([np.inf, -np.inf], np.nan).dropna(subset=["pt1", "op1", "te1", "bn1", "pt2"])
        r = fe_ols(w, "pt2", ["pt1", "op1", "te1", "bn1"], "mun")
        for x_ in ["pt1", "op1", "te1", "bn1"]:
            fe.append(dict(ano=a, origem_T1=x_, coef=float(r.loc[x_, "coef"]), ep=float(r.loc[x_, "se"]), municipios=int(r.grupos.iloc[0]), nota="relativo a abstencao T1; EF de municipio"))
    out["a3_ecologica_EF_municipio"] = pd.DataFrame(fe)
    out["a3_nota"] = ("Regressao ecologica (soma de pesos sem intercepto, ponderada por raiz de aptos, EP agrupado por municipio). Os coeficientes sao taxas de transicao "
                      "aparentes entre agregados de secao, nao comportamento individual (falacia ecologica); valores fora de [0,1] indicam limite do modelo.")
    ce = pd.DataFrame(coefs)
    g = lambda a: ce[(ce.ano == a) & (ce.destino_T2 == "PT") & (ce.origem_T1 == "OPO_T1")].iloc[0]
    if 2026 not in anos:
        raise NaoExecutado("A3: 2026 ausente")
    e = g(2026)
    pls = [(f"{a}", float(g(a).coef), float(g(a).ep)) for a in anos if a != 2026]
    c26 = [c for c in cont if c["ano"] == 2026][0]
    reg.add("A3", "ecologica: fracao de eleitores do oponente no T1 que aparece como voto no PT no T2", float(e.coef), float(e.ep), pls, expo=c26["OPO_T1"], fator=2.0,
            nota="coeficiente ecologico (falacia ecologica); teto = 2 x max(0, excesso) x votos do oponente no T1",
            ressalva="coeficientes negativos em todos os anos (nao medem conversao); com EF de municipio o coeficiente de 2026 e o mais negativo (analise posterior)")
