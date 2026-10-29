"""Fase 2: A11 (transferencia de votos), A12 (zero voto), A13 (inversoes e trechos lineares), A14 (recebimento x totalizacao), A15 (modelo de urna 2022).
Pre-registro: Adendo 5."""
import os
import numpy as np
import pandas as pd
from scipy import stats, optimize
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, par_ano, fe_ols
from h1_h4 import tenta


# ------------------------------------------------------------------------------------------------------- A11
BLOCOS_2026 = {"pro_Flavio": [30, 55, 70, 27], "esquerda": [16, 21, 80], "Renan": [14], "PCO": [29], "outros": [35, 28]}
NOMES_2026 = {30: "Zema", 55: "Caiado", 70: "Cury", 27: "Clariana", 16: "Hertz Dias", 21: "Edmilson Costa", 80: "Samara Martins", 14: "Renan Santos", 29: "Rui Costa Pimenta", 35: "Wilson Grassi", 28: "Leonardo Alves"}


def _cand(out, ano):
    p = os.path.join(out["_parquet2"], f"cand_t1_{ano}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"A11: falta {p} (rodar 12_candidatos_t1.py)")
    return pd.read_parquet(p)


def _prep(D, out, ano, blocos):
    c = _cand(out, ano)
    w = par_ano(D, ano, minvalid=1).merge(c, on=KEY, how="left")
    ap = w.QT_APTOS_t1.replace(0, np.nan)
    for nome, lst in blocos.items():
        w[f"x_{nome}"] = sum(w.get(f"v{n}", 0) for n in lst) / ap
    pt = 13
    w["x_PT"] = w.lula_t1 / ap; w["x_OPO"] = w.dir_t1 / ap
    w["x_BN"] = w.bn_pa_t1; w["x_ABS"] = 1 - w.QT_COMPARECIMENTO_t1 / ap
    w["y_PT"] = w.lula / ap; w["y_OPO"] = w["dir"] / ap
    w["mun"] = w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str)
    return w.replace([np.inf, -np.inf], np.nan).dropna(subset=["y_PT", "y_OPO", "x_PT", "x_OPO", "x_BN", "x_ABS"])


def a11(D, reg, out):
    c26 = _cand(out, 2026)
    # contabilidade nacional por termo (2026) e votos de cada candidato do bloco (confirmacao no BWeb)
    t1 = D[(2026, 1)]; t2 = D[(2026, 2)]
    t1 = t1[t1.DS_TIPO_URNA.str.upper().eq("APURADA")]; t2 = t2[t2.DS_TIPO_URNA.str.upper().eq("APURADA")]
    vot = {n: float(c26.get(f"v{n}", pd.Series([0])).sum()) for n in list(NOMES_2026) + [13, 22]}
    out["a11_votos_t1_por_candidato"] = pd.DataFrame([dict(numero=n, candidato=NOMES_2026[n] if n in NOMES_2026 else ("Lula" if n == 13 else "Flavio Bolsonaro"), votos_t1=v) for n, v in vot.items()])
    bl = {k: sum(vot[n] for n in lst) for k, lst in BLOCOS_2026.items()}
    bn1, bn2 = float((t1.branco + t1.nulo).sum()), float((t2.branco + t2.nulo).sum())
    a1_, a2_ = float((t1.QT_APTOS - t1.QT_COMPARECIMENTO).sum()), float((t2.QT_APTOS - t2.QT_COMPARECIMENTO).sum())
    terc = float((t1.nominal - t1.lula - t1["dir"]).sum())
    dpt, dop = float(t2.lula.sum() - t1.lula.sum()), float(t2["dir"].sum() - t1["dir"].sum())
    rows = [dict(termo=f"terceiros no T1: bloco {k}", votos=v) for k, v in bl.items()]
    rows += [dict(termo="terceiros no T1: total (inclui outros nao listados)", votos=terc), dict(termo="queda de brancos e nulos (T1 menos T2)", votos=bn1 - bn2),
             dict(termo="queda de abstencao (T1 menos T2; aptos quase constantes)", votos=a1_ - a2_), dict(termo="mudanca no total de aptos (T2 menos T1)", votos=float(t2.QT_APTOS.sum() - t1.QT_APTOS.sum())),
             dict(termo="SOMA dos termos (pool)", votos=terc + (bn1 - bn2) + (a1_ - a2_) + 0.0), dict(termo="ganho de Lula (T2 menos T1)", votos=dpt), dict(termo="ganho de Flavio (T2 menos T1)", votos=dop),
             dict(termo="ganho de Lula + ganho de Flavio", votos=dpt + dop), dict(termo="residuo (pool menos ganhos)", votos=terc + (bn1 - bn2) + (a1_ - a2_) - (dpt + dop))]
    out["a11_contabilidade"] = pd.DataFrame(rows)
    # regressao ecologica com EF de municipio (abstencao omitida)
    res = []
    W = {}
    for ano, blocos in ((2026, BLOCOS_2026),):
        w = _prep(D, out, ano, blocos); W[ano] = w
        xs = [f"x_{k}" for k in blocos] + ["x_PT", "x_OPO", "x_BN"]
        for y in ("y_PT", "y_OPO"):
            r = fe_ols(w, y, xs, "mun")
            for x in xs:
                res.append(dict(ano=ano, destino=y[2:], origem=x[2:], coef=float(r.loc[x, "coef"]), ep=float(r.loc[x, "se"]), municipios=int(r.grupos.iloc[0])))
    # placebos: maior e segundo maior terceiro de cada ano (sem inferir apoios)
    plac = {}
    for ano in (2022, 2018):
        c = _cand(out, ano)
        tot = c.drop(columns=KEY).sum().sort_values(ascending=False)
        pt_num, op_num = 13, (22 if ano == 2022 else 17)
        terceiros = [int(k[1:]) for k in tot.index if int(k[1:]) not in (pt_num, op_num)][:2]
        blocos = {f"terc{i+1}_n{n}": [n] for i, n in enumerate(terceiros)}
        blocos["outros_terc"] = [int(k[1:]) for k in tot.index if int(k[1:]) not in [pt_num, op_num] + terceiros]
        w = par_ano(D, ano, minvalid=1).merge(c, on=KEY, how="left"); ap = w.QT_APTOS_t1.replace(0, np.nan)
        for nome, lst in blocos.items():
            w[f"x_{nome}"] = sum(w.get(f"v{n}", 0) for n in lst) / ap
        w["x_PT"] = w.lula_t1 / ap; w["x_OPO"] = w.dir_t1 / ap; w["x_BN"] = w.bn_pa_t1; w["y_PT"] = w.lula / ap; w["y_OPO"] = w["dir"] / ap
        w["mun"] = w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str); w = w.replace([np.inf, -np.inf], np.nan).dropna(subset=["y_PT", "y_OPO", "x_PT", "x_OPO", "x_BN"] + [f"x_{k}" for k in blocos])
        xs = [f"x_{k}" for k in blocos] + ["x_PT", "x_OPO", "x_BN"]
        W[ano] = (w, blocos)
        for y in ("y_PT", "y_OPO"):
            r = fe_ols(w, y, xs, "mun")
            for x in xs:
                res.append(dict(ano=ano, destino=y[2:], origem=x[2:], coef=float(r.loc[x, "coef"]), ep=float(r.loc[x, "se"]), municipios=int(r.grupos.iloc[0])))
        plac[ano] = (f"x_terc1_n{terceiros[0]}", w)
    cf = pd.DataFrame(res)
    out["a11_ecologica_EF_municipio"] = cf
    # Goodman com restricoes (0<=b<=1) por minimos quadrados, sem EF, ponderado: 2026
    w = W[2026]; xs = [f"x_{k}" for k in BLOCOS_2026] + ["x_PT", "x_OPO", "x_BN", "x_ABS"]
    sw = np.sqrt(w.QT_APTOS_t1.values)
    gl = []
    for y in ("y_PT", "y_OPO"):
        r = optimize.lsq_linear(w[xs].values * sw[:, None], w[y].values * sw, bounds=(0, 1))
        for x, b in zip(xs, r.x):
            gl.append(dict(destino=y[2:], origem=x[2:], taxa_restrita_0_1=float(b)))
    out["a11_goodman_restrito_2026"] = pd.DataFrame(gl)
    # heterogeneidade por UF: coeficiente "pro_Flavio -> Lula" (2026) e "terceiro 1 -> PT" (placebos)
    het = []
    for ano, (xcol, w_) in ((2026, ("x_pro_Flavio", W[2026])), (2022, plac[2022]), (2018, plac[2018])):
        xs_ = [c for c in w_.columns if c.startswith("x_") and c not in ("x_ABS",)]
        coefs = []
        for uf, g in w_.groupby("SG_UF"):
            if len(g) < 500 or g.mun.nunique() < 5:
                continue
            r = tenta(out, f"A11 UF {ano} {uf}", fe_ols, g, "y_PT", xs_, "mun")
            if r is not None:
                coefs.append((uf, float(r.loc[xcol, "coef"]), float(r.loc[xcol, "se"]), len(g)))
        c_ = np.array([x[1] for x in coefs]); wt = np.array([x[3] for x in coefs], float)
        mu = float((c_ * wt).sum() / wt.sum())
        het.append(dict(ano=ano, regressor=xcol[2:], ufs=len(coefs), media_ponderada=mu, dp_entre_ufs=float(np.sqrt((wt * (c_ - mu) ** 2).sum() / wt.sum())), min=float(c_.min()), max=float(c_.max())))
        out[f"a11_por_uf_{ano}"] = pd.DataFrame(coefs, columns=["uf", "coef", "ep", "secoes"])
    out["a11_heterogeneidade_por_uf"] = pd.DataFrame(het)
    # registro: bloco pro-Flavio -> Lula (2026) contra maior terceiro -> PT (2022, 2018)
    g26 = cf[(cf.ano == 2026) & (cf.destino == "PT") & (cf.origem == "pro_Flavio")].iloc[0]
    pls = []
    for ano in (2022, 2018):
        nome = plac[ano][0][2:]
        r = cf[(cf.ano == ano) & (cf.destino == "PT") & (cf.origem == nome)].iloc[0]
        pls.append((f"{ano}: maior terceiro ({nome})", float(r.coef), float(r.ep)))
    votos_bloco = bl["pro_Flavio"]
    reg.add("A11", "bloco pro-Flavio no T1 (Zema, Caiado, Cury, Clariana) -> votos do PT no T2 por apto, EF de municipio", float(g26.coef), float(g26.ep), pls, expo=votos_bloco, fator=2.0,
            nota="coeficiente ecologico (falacia ecologica); placebos = maior terceiro de 2022 e 2018, sem inferir apoios",
            ressalva="o desenho compara blocos de composicao diferente entre anos; coeficientes ecologicos nao medem conversao individual")
    r2 = cf[(cf.ano == 2026) & (cf.destino == "OPO") & (cf.origem == "pro_Flavio")].iloc[0]
    out["a11_nota"] = (f"Taxa aparente do bloco pro-Flavio para Flavio no T2: {r2.coef:.3f} (ep {r2.ep:.3f}); para Lula: {g26.coef:.3f} (ep {g26.ep:.3f}). Falacia ecologica: coeficientes entre agregados nao sao comportamento individual. "
                       "Apoios declarados pelos candidatos: ver a pagina de contexto (com fonte).")


# ------------------------------------------------------------------------------------------------------- A12
def a12(D, reg, out):
    linhas = []
    for ano in (2026, 2022, 2018, 2014):
        for t in (1, 2):
            if (ano, t) not in D:
                continue
            d = D[(ano, t)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
            for rot, x in (("todas as apuradas", d), ("comparecimento >= 1", d[d.QT_COMPARECIMENTO >= 1]), ("comparecimento >= 30", d[d.QT_COMPARECIMENTO >= 30]), ("sem exterior, comparecimento >= 1", d[(d.SG_UF != "ZZ") & (d.QT_COMPARECIMENTO >= 1)])):
                linhas.append(dict(ano=ano, turno=t, definicao=rot, secoes=len(x), zero_oponente=int((x["dir"] == 0).sum()), zero_PT=int((x.lula == 0).sum()),
                                   votos_PT_nas_zero_oponente=int(x.lula[x["dir"] == 0].sum()), votos_oponente_nas_zero_PT=int(x["dir"][x.lula == 0].sum())))
    out["a12_contagens"] = pd.DataFrame(linhas)
    # P(zero): p do T1 (propria secao) e p dos vizinhos do mesmo local (leave-one-out), por candidato
    res, det = [], None
    for ano in (2026, 2022, 2018, 2014):
        if (ano, 1) not in D or (ano, 2) not in D:
            continue
        t1 = D[(ano, 1)].set_index(KEY)[["lula", "dir", "valid2"]].add_suffix("_t1")
        d = D[(ano, 2)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.valid2 >= 1) & (d.SG_UF != "ZZ")]
        d = d.join(t1, on=KEY)
        for cand, col, col1 in (("oponente", "dir", "dir_t1"), ("PT", "lula", "lula_t1")):
            x = d.copy()
            x["n"] = x.valid2
            x["p_t1"] = ((x[col1] + 0.5) / (x.valid2_t1 + 1)).clip(1e-6, 1 - 1e-6)
            g = x.groupby("uf_local")
            C = g[col].transform("sum"); V = g.valid2.transform("sum"); k = g[col].transform("size")
            x["p_viz"] = (((C - x[col]) + 0.5) / ((V - x.valid2) + 1)).where(k >= 3).clip(1e-6, 1 - 1e-6)
            for rot, pc in (("p da propria secao no T1", "p_t1"), ("p das secoes vizinhas do local", "p_viz")):
                z = x[x[pc].notna()]
                P = (1 - z[pc]) ** z.n
                obs = int((z[col] == 0).sum()); esp = float(P.sum()); var = float((P * (1 - P)).sum())
                res.append(dict(ano=ano, candidato_com_zero=cand, estimador_de_p=rot, secoes=len(z), observado=obs, esperado=esp, razao=obs / esp if esp else np.nan, z=(obs - esp) / np.sqrt(var) if var else np.nan,
                                p_excesso=float(stats.norm.sf((obs - esp) / np.sqrt(var))) if var else np.nan))
    out["a12_esperado_vs_observado"] = pd.DataFrame(res)
    # lista detalhada (2026 T2 e T1): secoes com zero para o oponente e para o PT
    L26 = pd.read_parquet(os.path.join(out["_parquet"], "locais_2026.parquet")) if os.path.exists(os.path.join(out["_parquet"], "locais_2026.parquet")) else None
    mod = pd.read_parquet(os.path.join(out["_parquet"], "modelo_urna_2026.parquet"))
    from h5_h8 import tipo_local
    linhas = []
    for t in (2, 1):
        d = D[(2026, t)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.QT_COMPARECIMENTO >= 1)]
        z = d[(d["dir"] == 0) | (d.lula == 0)].copy()
        z["quem_zero"] = np.where((z["dir"] == 0) & (z.lula == 0), "ambos", np.where(z["dir"] == 0, "oponente", "PT")); z["turno"] = t
        if L26 is not None:
            L26["tipo_local"] = tipo_local(L26.NM_LOCAL_VOTACAO)
            z = z.merge(L26[KEY + ["NM_LOCAL_VOTACAO", "tipo_local"]], on=KEY, how="left")
        z = z.merge(mod[mod.NR_TURNO == t][KEY + ["CD_MODELO_URNA"]], on=KEY, how="left")
        for a_, col in ((2022, "2022"), (2018, "2018")):
            o = D[(a_, 2)].set_index(KEY)[["lula", "dir", "valid2"]].add_suffix(f"_{col}")
            z = z.join(o, on=KEY)
        t1 = D[(2026, 1)].set_index(KEY)[["lula", "dir"]].add_suffix("_T1_2026")
        z = z.join(t1, on=KEY)
        linhas.append(z)
    det = pd.concat(linhas)
    keep = [c for c in ["turno", "quem_zero", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NM_LOCAL_VOTACAO", "tipo_local", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "lula_T1_2026", "dir_T1_2026",
                                  "lula_2022", "dir_2022", "lula_2018", "dir_2018", "manual_rate", "DT_ENCERRAMENTO", "CD_MODELO_URNA"] if c in det.columns]
    out["a12_secoes_zero_2026"] = det[keep].round(4)
    z2 = det[det.turno == 2]
    zo = z2[z2.quem_zero.isin(["oponente", "ambos"])]
    out["a12_perfil_zero_oponente_T2"] = pd.DataFrame([dict(secoes=len(zo), comparecimento_mediano=float(zo.QT_COMPARECIMENTO.median()), aptos_mediano=float(zo.QT_APTOS.median()),
                                                           pct_com_oponente_no_T1=float((zo.dir_T1_2026 > 0).mean() * 100), pct_com_oponente_em_2022=float((zo.dir_2022.fillna(-1) > 0).mean() * 100),
                                                           pct_com_oponente_em_2018=float((zo.dir_2018.fillna(-1) > 0).mean() * 100), votos_do_PT_nessas_secoes=int(zo.lula.sum()),
                                                           pct_da_margem=float(100 * zo.lula.sum() / MARGEM), **({"tipo_mais_comum": str(zo.tipo_local.value_counts().index[0])} if "tipo_local" in zo else {}))])
    if "tipo_local" in zo:
        out["a12_zero_oponente_por_tipo"] = zo.tipo_local.value_counts().rename("secoes").reset_index()
    # registro: observado vs esperado (p da propria secao no T1), oponente de 2026 contra placebos (razao obs/esp)
    r = out["a12_esperado_vs_observado"]
    f = lambda ano, c, e: r[(r.ano == ano) & (r.candidato_com_zero == c) & (r.estimador_de_p == e)].iloc[0]
    e0 = "p da propria secao no T1"
    a = f(2026, "oponente", e0)
    pls = [(f"{ano}", float(f(ano, "oponente", e0).razao), float(np.sqrt(max(f(ano, "oponente", e0).observado, 1)) / max(f(ano, "oponente", e0).esperado, 1e-9))) for ano in (2022, 2018, 2014) if ((r.ano == ano) & (r.candidato_com_zero == "oponente")).any()]
    reg.add("A12", "secoes com zero voto para o oponente no T2: razao observado/esperado (p do T1)", float(a.razao), float(np.sqrt(max(a.observado, 1)) / max(a.esperado, 1e-9)), pls,
            expo=float(zo.lula.sum()) / max(a.observado, 1) * max(a.observado - a.esperado, 0) if len(zo) else 0.0, fator=1.0,
            nota="teto = votos do PT nas secoes em excesso sobre o esperado; o total nas secoes zero e publicado em a12_perfil_zero_oponente_T2",
            ressalva="os placebos tem razao observado/esperado abaixo de 1 porque o estimador de p pelo T1 e inadequado onde ha terceiros relevantes no T1 (2018, 2014); o teste direto observado contra esperado em 2026 (z=1,33) nao e significativo (analise posterior)")


# ------------------------------------------------------------------------------------------------------- A13
def _serie(D, out, ano, turno, reps, K=1000, seed=5):
    p = os.path.join(out["_parquet"], f"ordem_{ano}_t{turno}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"A13 {ano}/T{turno}: sem horario de totalizacao (produto detalhe_votacao_secao de {ano} nao traz)")
    o = pd.read_parquet(p)
    b = D[(ano, turno)]; b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")].merge(o, on=KEY, how="left")
    rng = np.random.default_rng(seed)
    b = b.assign(_r=rng.random(len(b))).sort_values(["DT_PRIM_TOT_PARCIAL_HOR_TSE", "DT_RECEBIMENTO_BU_HOR_TSE", "_r"]).reset_index(drop=True)
    l = b.lula.values.astype(float); d = b["dir"].values.astype(float); N = len(b); uf = pd.factorize(b.SG_UF)[0]
    idx = np.ceil(np.arange(1, K + 1) * N / K).astype(int) - 1

    def marg(lv, dv):
        return np.cumsum(lv)[idx] - np.cumsum(dv)[idx]

    def share(lv, dv):
        cl, cd = np.cumsum(lv)[idx], np.cumsum(dv)[idx]
        return cl / (cl + cd)
    slots = [np.flatnonzero(uf == u) for u in range(uf.max() + 1)]
    return b, l, d, N, uf, idx, marg, share, slots, rng


def _inv(m, k0=10):
    s = np.sign(m[k0:]); s = s[s != 0]
    return int((np.diff(s) != 0).sum())


def _lineares(sh, w=50, r2min=0.99, min_delta_pp=0.15):
    """Trechos lineares: janelas de w pontos com R2 >= r2min e variacao >= min_delta_pp; devolve o numero de janelas e de trechos (corridas)."""
    x = np.arange(w); n_ok = [];
    for i in range(0, len(sh) - w):
        y = sh[i:i + w] * 100
        if abs(y[-1] - y[0]) < min_delta_pp:
            n_ok.append(False); continue
        r = np.corrcoef(x, y)[0, 1]
        n_ok.append(bool(r ** 2 >= r2min))
    n_ok = np.array(n_ok); runs = int(((n_ok[1:] & ~n_ok[:-1]).sum()) + (1 if n_ok[:1].any() else 0))
    return int(n_ok.sum()), runs, n_ok


def _emenda(sh):
    """'Metodo do video' (interpretacao declarada no pre-registro): somar so os incrementos positivos (ou so os negativos) da curva de share."""
    ds = np.diff(sh)
    return float(sh[0] + ds[ds > 0].sum()), float(sh[0] + ds[ds < 0].sum())


def a13(D, reg, out):
    reps = int(os.environ.get("AUDITORIA_REPS", "1000"))
    cfg = [(2026, 2), (2026, 1), (2022, 2), (2018, 2)]
    linhas, lin_uf = [], []
    for ano, t in cfg:
        r = tenta(out, f"A13 {ano}/T{t}", _serie, D, out, ano, t, reps)
        if r is None:
            continue
        b, l, d, N, uf, idx, marg, share, slots, rng = r
        m_real = marg(l, d); s_real = share(l, d)
        inv_real = _inv(m_real)
        invA, invB, linA, linB, emA, emB = [], [], [], [], [], []
        for _ in range(reps):
            o_ = rng.permutation(N); mA = marg(l[o_], d[o_]); sA = share(l[o_], d[o_]); invA.append(_inv(mA)); linA.append(_lineares(sA)[0]); emA.append(_emenda(sA)[0])
            order = np.empty(N, dtype=np.int64)
            for s in slots:
                order[s] = rng.permutation(s)
            mB = marg(l[order], d[order]); sB = share(l[order], d[order]); invB.append(_inv(mB)); linB.append(_lineares(sB)[0]); emB.append(_emenda(sB)[0])
        nl, runs, ok = _lineares(s_real)
        up, down = _emenda(s_real)
        q = lambda a_: (float(np.quantile(a_, .025)), float(np.quantile(a_, .975)))
        linhas.append(dict(ano=ano, turno=t, secoes=N, inversoes_real=inv_real, inversoes_A_ic95=str(q(invA)), inversoes_B_ic95=str(q(invB)), inversoes_B_media=float(np.mean(invB)),
                           janelas_lineares_real=nl, janelas_lineares_A_ic95=str(q(linA)), janelas_lineares_B_ic95=str(q(linB)), trechos_lineares_real=runs,
                           emenda_subidas_share_final_real=up, emenda_subidas_B_ic95=str(tuple(round(v, 3) for v in q(emB))), emenda_subidas_A_ic95=str(tuple(round(v, 3) for v in q(emA))), share_final=float(s_real[-1]),
                           lider_final="PT" if m_real[-1] > 0 else "oponente"))
        # atribuicao de trechos lineares reais a UFs: UF dominante na faixa de posicoes de cada corrida
        pos = (idx + 1) / N; i = 0
        while i < len(ok):
            if ok[i]:
                j = i
                while j < len(ok) and ok[j]:
                    j += 1
                lo, hi = int(idx[i]), int(idx[min(j + 49, len(idx) - 1)])
                ufs = b.SG_UF.iloc[lo:hi + 1].value_counts(normalize=True)
                lin_uf.append(dict(ano=ano, turno=t, de_pct_secoes=100 * pos[i], ate_pct_secoes=100 * pos[min(j + 49, len(pos) - 1)], variacao_share_pp=100 * (s_real[min(j + 49, len(s_real) - 1)] - s_real[i]),
                                   ufs_dominantes=", ".join(f"{u} {100*v:.0f}%" for u, v in ufs.head(3).items())))
                i = j
            else:
                i += 1
    out["a13_inversoes_e_trechos"] = pd.DataFrame(linhas)
    out["a13_trechos_lineares_reais_por_uf"] = pd.DataFrame(lin_uf)
    out.setdefault("nao_executados", []).extend([
        ("A13 2014/T2 e 2002-2010", "o produto detalhe_votacao_secao de 2014 nao tem horario de totalizacao e nao ha dado por secao com horario para 2002 a 2010 no catalogo aberto"),
        ("A13 video 'Prof. Marcelo Trindade' (472 urnas, 60-65%)", "NAO REPRODUZIVEL: o video, os dados e o codigo das '472 urnas' nao foram fornecidos"),
        ("A13/A14 snapshots do site Resultados", "nao ha serie publica de snapshots do site Resultados com horario; so o horario de totalizacao por secao"),
    ])
    out["a13_nota"] = "Metodo do video: interpretacao declarada (somar so incrementos positivos da curva de share). O total final e a soma dos BUs, independe da ordem (identico em todas as permutacoes) e coincide com H9."


# ------------------------------------------------------------------------------------------------------- A14
def a14(D, reg, out):
    rows, curvas = [], []
    for ano, t in ((2026, 2), (2022, 2), (2026, 1)):
        p = os.path.join(out["_parquet"], f"ordem_{ano}_t{t}.parquet")
        if not os.path.exists(p):
            raise NaoExecutado(f"A14: falta {p}")
        o = pd.read_parquet(p)
        o = o.dropna(subset=["DT_RECEBIMENTO_BU_HOR_TSE", "DT_PRIM_TOT_PARCIAL_HOR_TSE"])
        dia = o.DT_PRIM_TOT_PARCIAL_HOR_TSE.dt.normalize().mode().iloc[0]
        mrec = ((o.DT_RECEBIMENTO_BU_HOR_TSE - dia).dt.total_seconds() / 60).values
        mtot = ((o.DT_PRIM_TOT_PARCIAL_HOR_TSE - dia).dt.total_seconds() / 60).values
        N = len(o)
        grade = np.arange(17 * 60, 24 * 60, 1)
        rec = np.searchsorted(np.sort(mrec), grade, side="right") / N * 100
        tot = np.searchsorted(np.sort(mtot), grade, side="right") / N * 100
        for h, m in ((17, 30), (18, 0), (19, 0), (19, 34), (20, 0), (21, 0), (22, 0)):
            i = h * 60 + m - 17 * 60
            rows.append(dict(ano=ano, turno=t, hora=f"{h:02d}:{m:02d}", pct_bu_recebido=float(rec[i]), pct_totalizado=float(tot[i])))
        atraso = mtot - mrec
        rows.append(dict(ano=ano, turno=t, hora="atraso recebimento -> 1a totalizacao (min): mediana / p95 / max", pct_bu_recebido=float(np.median(atraso)), pct_totalizado=float(np.quantile(atraso, .95)), max=float(atraso.max())))
        curvas.append(pd.DataFrame({"ano": ano, "turno": t, "minuto_do_dia": grade[::5], "pct_recebido": rec[::5], "pct_totalizado": tot[::5]}))
    out["a14_pontos_chave"] = pd.DataFrame(rows).round(3)
    out["a14_curvas_5min"] = pd.concat(curvas).round(3)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir = os.path.join(out["_saida"], "figs"); os.makedirs(figdir, exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for a_, (ano, t) in zip(ax, ((2026, 2), (2022, 2), (2026, 1))):
        c = out["a14_curvas_5min"]; c = c[(c.ano == ano) & (c.turno == t)]
        a_.plot(c.minuto_do_dia / 60, c.pct_recebido, label="BU recebido"); a_.plot(c.minuto_do_dia / 60, c.pct_totalizado, ls="--", label="1ª totalização"); a_.set_title(f"{ano} T{t}", fontsize=9)
        a_.set_xlabel("hora (Brasília)"); a_.set_ylabel("% das seções"); a_.axvline(19, color="#999", lw=.8, ls=":")
    ax[0].legend(fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(figdir, "a14_recebido_totalizado.png"), dpi=110); plt.close(fig)
    out.setdefault("nao_executados", []).append(("A14 curva de divulgacao e atraso totalizado->divulgado", "nao ha snapshots publicos do site Resultados com horario; e o video original, onde a captura sugere 7,28%, nao foi fornecido"))
    out["a14_nota"] = "Curva de divulgacao NAO EXECUTADA (sem snapshots). Recebido e totalizado vem do detalhe_votacao_secao."


# ------------------------------------------------------------------------------------------------------- A15
def a15(D, reg, out):
    mod = {a: pd.read_parquet(os.path.join(out["_parquet"], f"modelo_urna_{a}.parquet")) for a in (2022, 2026)}
    rows = []
    for ano in (2022, 2026):
        w = par_ano(D, ano, minvalid=30)
        w = w.merge(mod[ano][mod[ano].NR_TURNO == 2][KEY + ["CD_MODELO_URNA"]], on=KEY, how="left")
        w = w[w.CD_MODELO_URNA.notna() & (w.CD_MODELO_URNA > 0)].copy()
        dums = []
        for m in sorted(w.CD_MODELO_URNA.unique()):
            if m != 2020:
                w[f"m{int(m)}"] = (w.CD_MODELO_URNA == m).astype(float); dums.append(f"m{int(m)}")
        specs = {"T2 sem controle do T1 (corte transversal)": ("lula_sh", dums), "T2 com voto do T1 como controle": ("lula_sh", dums + ["lula_sh_t1"]), "T1 (corte transversal)": ("lula_sh_t1", dums)}
        for nome, (y, xs) in specs.items():
            r = tenta(out, f"A15 {ano} {nome}", fe_ols, w, y, xs, "uf_local")
            if r is None:
                continue
            for dm in dums:
                v = float(w[w[dm] == 1].valid2.sum())
                b, se = float(r.loc[dm, "coef"]), float(r.loc[dm, "se"])
                rows.append(dict(ano=ano, modelo=f"UE{dm[1:]}", especificacao=nome, coef_pp=100 * b, ep_pp=100 * se, secoes=int(w[dm].sum()), votos_margem=2 * b * v, votos_ic95_inf=2 * (b - 1.96 * se) * v,
                                 votos_ic95_sup=2 * (b + 1.96 * se) * v, pct_margem=100 * 2 * b * v / MARGEM))
    t = pd.DataFrame(rows); out["a15_modelo_urna"] = t.round(3)
    for m in ("UE2009", "UE2010"):
        a = t[(t.ano == 2022) & (t.modelo == m) & (t.especificacao == "T2 com voto do T1 como controle")]
        b = t[(t.ano == 2022) & (t.modelo == m) & (t.especificacao == "T1 (corte transversal)")]
        if len(a) and len(b):
            mm = D[(2022, 2)][D[(2022, 2)].SG_UF != "ZZ"].merge(mod[2022][mod[2022].NR_TURNO == 2][KEY + ["CD_MODELO_URNA"]], on=KEY)
            v = float(mm[mm.CD_MODELO_URNA == int(m[2:])].valid2.sum())
            reg.add("A15", f"2022: {m} contra UE2020, mesmo local: Lula% no T2 dado o T1", float(a.coef_pp.iloc[0] / 100), float(a.ep_pp.iloc[0] / 100),
                    [("2022/T1 (corte transversal)", float(b.coef_pp.iloc[0] / 100), float(b.ep_pp.iloc[0] / 100))], expo=v, fator=2.0,
                    nota="o efeito transversal do T1 e composicao; o que importa e se o T2 acrescenta algo dado o T1")
