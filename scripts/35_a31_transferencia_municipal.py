#!/usr/bin/env python3
"""A31 (Adendo 10): municipios extremos na transferencia T1 -> T2 (alegacao Silva Jardim/RJ).
Uso: python -I 35_a31_transferencia_municipal.py DIR_PARQUET DIR_PARQUET2 DIR_MAPA DIR_SAIDA
  DIR_PARQUET  = bu_{ano}_t{1,2}.parquet     DIR_PARQUET2 = cand_t1_{ano}.parquet (2018, 2022, 2026)
  DIR_MAPA     = results/fase3 (A20_mapa_tse_ibge.csv, nomes)       DIR_SAIDA = results/fase3
Tudo o que o script faz esta fixado no Adendo 10 de 00_preregistro.md (escrito antes da primeira execucao)."""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats, optimize
from scipy.special import logsumexp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import MARGEM, KEY

ANOS = (2026, 2022, 2018, 2014)
SJ = ("RJ", 59110)
PMIN = 20
M_PEDIDO = 5570
BLOCOS_2026 = {"pro_flavio": [30, 55, 70, 27], "renan": [14]}
NOMES_2026 = {13: "Lula", 22: "Flávio Bolsonaro", 30: "Zema", 55: "Caiado", 70: "Cury", 27: "Clariana Barão", 16: "Hertz Dias", 21: "Edmilson Costa", 80: "Samara Martins", 14: "Renan Santos",
              29: "Rui Costa Pimenta", 35: "Wilson Grassi", 28: "Leonardo Alves"}
# apoio declarado no 2o turno, conforme docs/resultados-fase2.md (A11), com as fontes de la
APOIO_2026 = {30: "apoiou Flavio", 55: "apoiou Flavio", 70: "apoiou Flavio", 27: "apoiou Flavio", 16: "voto critico em Lula", 21: "voto critico em Lula", 14: "neutro (liberou eleitores)",
              35: "nao se posicionou", 80: "orientacao do partido (UP): vote 13", 28: "nao consta", 29: "sem posicao definida (O Povo, 10/10/2026); voto nulo nao verificado"}
NUM_PT = {2026: 13, 2022: 13, 2018: 13, 2014: 13}
NUM_OP = {2026: 22, 2022: 22, 2018: 17, 2014: 45}
EXCLUIDOS = []
SOMA = ["lula", "dir", "nominal", "branco", "nulo", "QT_APTOS", "QT_COMPARECIMENTO"]


def le_secoes(pq, ano, turno, tipo=False):
    d = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{turno}.parquet"), columns=KEY + SOMA + (["DS_TIPO_URNA"] if tipo else []))
    return d[d.SG_UF != "ZZ"]


def municipios_excluidos(pq, ano):
    """Adendo 10a: municipio-ano com secao de status de apuracao diferente entre T1 e T2 (ou presente so em um turno)."""
    a, b = (le_secoes(pq, ano, t, True).set_index(KEY).DS_TIPO_URNA.str.upper() for t in (1, 2))
    j = pd.concat([a.rename("t1"), b.rename("t2")], axis=1)
    ruim = j[(j.t1 != j.t2) | j.t1.isna() | j.t2.isna()].reset_index()
    ruim["motivo"] = np.where(ruim.t1.isna() | ruim.t2.isna(), "secao so em um turno", "tipo de urna diferente: " + ruim.t1.fillna("") + " -> " + ruim.t2.fillna(""))
    ruim["ano"] = ano
    return ruim


def agrega(pq, ano):
    a = {}
    for t in (1, 2):
        s = le_secoes(pq, ano, t)
        a[t] = s.groupby(["SG_UF", "CD_MUNICIPIO"], as_index=False)[SOMA].sum()
    c1, c2 = set(zip(a[1].SG_UF, a[1].CD_MUNICIPIO)), set(zip(a[2].SG_UF, a[2].CD_MUNICIPIO))
    if c1 != c2:
        raise SystemExit(f"ERRO: {ano}: municipios diferentes entre T1 e T2: {sorted(c1 ^ c2)[:10]}")
    m = a[1].merge(a[2], on=["SG_UF", "CD_MUNICIPIO"], suffixes=("1", "2"))
    ex = municipios_excluidos(pq, ano)
    chaves = set(zip(ex.SG_UF, ex.CD_MUNICIPIO))
    m = m[[(u, c) not in chaves for u, c in zip(m.SG_UF, m.CD_MUNICIPIO)]].reset_index(drop=True)
    EXCLUIDOS.append(ex)
    m["ano"] = ano
    m["PT1"], m["OP1"], m["PT2"], m["OP2"] = m.lula1, m.dir1, m.lula2, m.dir2
    m["BN1"], m["BN2"] = m.branco1 + m.nulo1, m.branco2 + m.nulo2
    m["COMP1"], m["COMP2"], m["APT1"], m["APT2"] = m.QT_COMPARECIMENTO1, m.QT_COMPARECIMENTO2, m.QT_APTOS1, m.QT_APTOS2
    m["T1terc"] = m.nominal1 - m.PT1 - m.OP1
    m["dL"], m["dF"], m["dC"] = m.PT2 - m.PT1, m.OP2 - m.OP1, m.COMP2 - m.COMP1
    m["E"] = m.T1terc + m.BN1 + m.dC
    m["P"] = m.dL + m.dF
    ident = m.P - (m.E - m.BN2)
    if (ident != 0).any():
        raise SystemExit(f"ERRO: identidade P = E - BN(T2) falha em {int((ident != 0).sum())} municipios de {ano} (comp != nominal + branco + nulo?); ver Adendo 10")
    m["f"] = np.where(m.P >= PMIN, m.dL / m.P.where(m.P > 0), np.nan)
    return m.drop(columns=[c for c in m.columns if c.startswith(("lula", "dir", "nominal", "branco", "nulo", "QT_"))])


def perfil(m, ano, pq2):
    """Covariaveis do 1o turno (fracao do comparecimento do T1) e terceiros por bloco."""
    X = pd.DataFrame(index=m.index)
    X["sPT"], X["sOP"], X["sBN"] = m.PT1 / m.COMP1, m.OP1 / m.COMP1, m.BN1 / m.COMP1
    X["sABS"] = 1 - m.COMP1 / m.APT1
    dom = None
    if ano in (2026, 2022, 2018):
        c = pd.read_parquet(os.path.join(pq2, f"cand_t1_{ano}.parquet"))
        c = c[c.SG_UF != "ZZ"]
        vcols = [x for x in c.columns if x.startswith("v")]
        g = c.groupby(["SG_UF", "CD_MUNICIPIO"], as_index=False)[vcols].sum()
        g = m[["SG_UF", "CD_MUNICIPIO"]].merge(g, on=["SG_UF", "CD_MUNICIPIO"], how="left").fillna(0)
        num = {int(x[1:]): x for x in vcols}
        terc = [n for n in num if n not in (NUM_PT[ano], NUM_OP[ano])]
        if ano == 2026:
            for nome, ns in BLOCOS_2026.items():
                X["s_" + nome] = g[[num[n] for n in ns]].sum(axis=1).values / m.COMP1.values
        else:
            tot = g[[num[n] for n in terc]].sum().sort_values(ascending=False)
            top = [int(k[1:]) for k in tot.index[:2]]
            for i, n in enumerate(top):
                X[f"s_terc{i + 1}"] = g[num[n]].values / m.COMP1.values
        gt = g[[num[n] for n in terc]]
        dom = pd.DataFrame({"terc_dom_num": [terc[i] for i in gt.values.argmax(axis=1)], "terc_dom_votos": gt.values.max(axis=1)}, index=m.index)
        dom["terc_dom_pct_comp1"] = 100 * dom.terc_dom_votos / m.COMP1
        dom["terc_dom_nome"] = dom.terc_dom_num.map(NOMES_2026) if ano == 2026 else dom.terc_dom_num.astype(str)
        dom["terc_dom_apoio"] = dom.terc_dom_num.map(APOIO_2026) if ano == 2026 else ""
    return X, dom


def robust_scale(z):
    return 1.4826 * np.median(np.abs(z - np.median(z)))


def ajusta(m, X):
    """WLS com efeito fixo de UF, variancia f_hat(1-f_hat)/P + tau2 com tau2 pela escala robusta de z = 1. Retorna m com f_hat, dp, z e (tau2, n)."""
    e = m[m.f.notna() & (m.P > 0)].copy()
    ufd = pd.get_dummies(e.SG_UF).astype(float)
    D = np.column_stack([ufd.values, X.loc[e.index].values])
    y, P = e.f.values, e.P.values
    tau2 = 0.0025
    fh = np.full(len(e), np.average(y, weights=P))
    for _ in range(20):
        v = np.clip(fh, 0.02, 0.98) * (1 - np.clip(fh, 0.02, 0.98)) / P + tau2
        sw = 1 / np.sqrt(v)
        b, *_ = np.linalg.lstsq(D * sw[:, None], y * sw, rcond=None)
        fh = D @ b
        r = y - fh
        fc = np.clip(fh, 0.02, 0.98)

        def gap(t):
            return robust_scale(r / np.sqrt(fc * (1 - fc) / P + t)) - 1
        if gap(0.0) <= 0:
            tau2 = 0.0
        else:
            tau2 = optimize.brentq(gap, 0.0, 1.0)
    fc = np.clip(fh, 0.02, 0.98)
    dp = np.sqrt(fc * (1 - fc) / P + tau2)
    e["f_hat"], e["dp"], e["resid"] = fh, dp, y - fh
    e["z"] = e.resid / e.dp
    return e, dict(tau2=tau2, n=len(e), escala_robusta_z=robust_scale(e.z.values), colunas_perfil=";".join(X.columns))


def fit_df(z):
    z = np.asarray(z)
    nll = lambda lg: -stats.t.logpdf(z, df=np.exp(lg)).sum()
    r = optimize.minimize_scalar(nll, bounds=(np.log(1.2), np.log(500)), method="bounded")
    return float(np.exp(r.x))


def holm(p, m=None):
    p = np.asarray(p, float)
    n = len(p)
    m = n if m is None else m
    order = np.argsort(p)
    adj = np.empty(n)
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, max(m - k, 1) * p[i]))
        adj[i] = run
    return adj


def suplementar(m, X):
    """Adendo 10b, S1: yL = dL/aptos(T1) e yF = dF/aptos(T1), WLS (peso = aptos T1) nos regressores do T1 e efeito fixo de UF; z pela escala robusta dentro de decis de aptos."""
    ufd = pd.get_dummies(m.SG_UF).astype(float)
    D = np.column_stack([ufd.values, X.loc[m.index].values])
    w = m.APT1.values.astype(float)
    sw = np.sqrt(w)
    dec = pd.qcut(m.APT1, 10, labels=False, duplicates="drop")
    out = m[["SG_UF", "CD_MUNICIPIO", "APT1", "dL", "dF"]].copy()
    for nome, num in (("L", m.dL), ("F", m.dF)):
        y = (num / m.APT1).values
        b, *_ = np.linalg.lstsq(D * sw[:, None], y * sw, rcond=None)
        r = y - D @ b
        esc = pd.Series(r).groupby(dec.values).transform(lambda v: robust_scale(v.values)).values
        out["r" + nome], out["z" + nome] = r, r / esc
        out["esc" + nome] = esc
    return out


def moedas(m):
    """Modelo de moedas independentes: cada eleitor do pool vai ao PT com prob p0. Nacional = todos os municipios do ano (pool total, P > 0); municipal = P >= PMIN."""
    nac, mun = [], []
    for ano, gall in m.groupby("ano"):
        r_nac = gall.PT1.sum() / (gall.PT1.sum() + gall.OP1.sum())
        g_n = gall[gall.P > 0]
        for nome, p0n in (("p0 = 0,5", lambda g: np.full(len(g), 0.5)), ("p0 = razao PT/(PT+OPO) do municipio no T1", lambda g: (g.PT1 / (g.PT1 + g.OP1)).values),
                          ("p0 = razao PT/(PT+OPO) nacional no T1", lambda g: np.full(len(g), r_nac))):
            P, dL, p0 = g_n.P.values.astype(float), g_n.dL.values.astype(float), p0n(g_n)
            ez, vz = (P * p0).sum(), (P * p0 * (1 - p0)).sum()
            z = (dL.sum() - ez) / np.sqrt(vz)
            nac.append(dict(ano=ano, variante=nome, municipios=len(g_n), pool=int(P.sum()), dL_observado=int(dL.sum()), dL_esperado_moedas=ez, desvio_padrao_moedas=float(np.sqrt(vz)), z_moedas=z,
                            log10_p_bilateral=float(np.log10(2) + stats.norm.logsf(abs(z)) / np.log(10)), rejeita_nacional_5pct=bool(abs(z) > 1.96)))
            g = gall[gall.P >= PMIN]
            P, dL, p0 = g.P.values.astype(float), g.dL.values.astype(float), p0n(g)
            zi = (dL - P * p0) / np.sqrt(P * p0 * (1 - p0))
            pi_ = 2 * stats.norm.sf(np.abs(zi))
            hh = holm(pi_)
            mun.append(dict(ano=ano, variante=nome, municipios=len(g), rejeitados_holm_5pct=int((hh < 0.05).sum()), pct_rejeitados_holm=100 * float((hh < 0.05).mean()), pct_rejeitados_sem_correcao=100 * float((pi_ < 0.05).mean())))
    return pd.DataFrame(nac), pd.DataFrame(mun)


def concentracao(pq, ano, uf, cd, f_hat, f):
    s = secoes_mun(pq, ano, uf, cd).dropna(subset=["lula1", "lula2"])
    s["dL_s"], s["dF_s"] = s.lula2 - s.lula1, s.dir2 - s.dir1
    s["P_s"] = s.dL_s + s.dF_s
    top3_dl = s.dL_s.sort_values(ascending=False).head(3).sum() / s.dL_s.sum() if s.dL_s.sum() > 0 else np.nan
    top3_p = s.P_s.sort_values(ascending=False).head(3).sum() / s.P_s.sum() if s.P_s.sum() > 0 else np.nan
    pos = lambda x: x.clip(lower=0)
    top3_dl_pos = pos(s.dL_s).sort_values(ascending=False).head(3).sum() / pos(s.dL_s).sum() if pos(s.dL_s).sum() > 0 else np.nan
    top3_p_pos = pos(s.P_s).sort_values(ascending=False).head(3).sum() / pos(s.P_s).sum() if pos(s.P_s).sum() > 0 else np.nan
    fs = (s.dL_s / s.P_s.where(s.P_s > 0)).dropna()
    lado = float(((fs > f_hat) == (f > f_hat)).mean()) if len(fs) else np.nan
    if np.isnan(top3_dl) or np.isnan(top3_p):
        ganho = "nao se aplica (soma de dL ou do pool <= 0)"
    else:
        ganho = "concentrado" if (top3_dl > 0.5 and top3_dl > 1.5 * top3_p) else "espalhado"
    return dict(secoes=len(s), C3_dL=top3_dl, C3_P=top3_p, C3_dL_so_positivos=top3_dl_pos, C3_P_so_positivos=top3_p_pos, pct_secoes_do_mesmo_lado=100 * lado, ganho=ganho)


def secoes_mun(pq, ano, uf, cd):
    s = {}
    for t in (1, 2):
        d = le_secoes(pq, ano, t)
        s[t] = d[(d.SG_UF == uf) & (d.CD_MUNICIPIO == cd)].set_index(KEY)
    return s[1].add_suffix("1").join(s[2].add_suffix("2"), how="outer")


def main(pq, pq2, dmapa, saida):
    os.makedirs(saida, exist_ok=True)
    mapa = pd.read_csv(os.path.join(dmapa, "A20_mapa_tse_ibge.csv"), dtype=str)
    mapa["CD_MUNICIPIO"] = mapa.CD_MUNICIPIO.astype(int)
    nome = {(r.SG_UF, r.CD_MUNICIPIO): r.NM_MUNICIPIO for r in mapa.itertuples()}
    M, X, DOM = {}, {}, {}
    for a in ANOS:
        M[a] = agrega(pq, a)
        X[a], DOM[a] = perfil(M[a], a, pq2)
        print(a, "municipios:", len(M[a]), "com P>=20:", int((M[a].P >= PMIN).sum()), "P<=0:", int((M[a].P <= 0).sum()))

    # Parte 1: conferencia da alegacao
    r26 = M[2026]
    sj = r26[(r26.SG_UF == SJ[0]) & (r26.CD_MUNICIPIO == SJ[1])].iloc[0]
    sj_c = pd.read_parquet(os.path.join(pq2, "cand_t1_2026.parquet"))
    sj_c = sj_c[(sj_c.SG_UF == SJ[0]) & (sj_c.CD_MUNICIPIO == SJ[1])]
    terc_cols = [c for c in sj_c.columns if c.startswith("v") and int(c[1:]) not in (13, 22)]
    linhas = [("aptos", sj.APT1, sj.APT2), ("comparecimento", sj.COMP1, sj.COMP2), ("Lula (13)", sj.PT1, sj.PT2), ("Flavio Bolsonaro (22)", sj.OP1, sj.OP2)]
    linhas += [(f"{NOMES_2026.get(int(c[1:]), c)} ({c[1:]}), 1o turno", int(sj_c[c].sum()), np.nan) for c in terc_cols]
    linhas += [("terceiros (soma)", sj.T1terc, 0), ("brancos e nulos", sj.BN1, sj.BN2)]
    conf = pd.DataFrame(linhas, columns=["grandeza", "T1", "T2"])
    conf["T2_menos_T1"] = conf.T2 - conf.T1
    conf.loc[conf.T2.isna(), "T2_menos_T1"] = np.nan
    conf.to_csv(os.path.join(saida, "A31_sj_conferencia.csv"), index=False)
    res_sj = dict(municipio="Silva Jardim/RJ", dL=int(sj.dL), dF=int(sj.dF), dC=int(sj.dC), d_aptos=int(sj.APT2 - sj.APT1), d_BN=int(sj.BN2 - sj.BN1), d_terceiros_zerados=int(-sj.T1terc),
                  pool=int(sj.P), estoque=int(sj.E), f=sj.dL / sj.P)
    print(res_sj)

    # Parte 3: modelo nulo por ano (z) e cauda t com df dos outros tres anos
    E, cal = {}, []
    for a in ANOS:
        E[a], c = ajusta(M[a], X[a])
        cal.append(dict(ano=a, **c))
    cal = pd.DataFrame(cal)
    for a in ANOS:
        zo = np.concatenate([E[b].z.values for b in ANOS if b != a])
        df = fit_df(zo)
        e = E[a]
        n = len(e)
        e["df_t"] = df
        e["p"] = 2 * stats.t.sf(np.abs(e.z), df)
        e["p_holm"] = holm(e.p.values)
        e["p_holm_5570"] = holm(e.p.values, M_PEDIDO)
        e["zc_bonf"] = stats.t.isf(0.05 / (2 * M_PEDIDO), df)
        cal.loc[cal.ano == a, "df_t_dos_outros_anos"] = df
        cal.loc[cal.ano == a, "zc_Bonferroni_5570"] = stats.t.isf(0.05 / (2 * M_PEDIDO), df)
        # precedente: quantos municipios dos outros anos tem |z| >= |z| de cada um
        zabs = np.sort(np.abs(zo))
        e["outros_anos_com_z_ao_menos_igual"] = len(zabs) - np.searchsorted(zabs, np.abs(e.z.values), side="left")
        for b in ANOS:
            if b != a:
                zb = np.sort(np.abs(E[b].z.values))
                e[f"n_ano_{b}"] = len(zb) - np.searchsorted(zb, np.abs(e.z.values), side="left")
        # custo em votos
        e["teto_incond_votos_margem"] = 2 * e.P * np.abs(e.resid)
        e["teto_alem_cauda_votos_margem"] = 2 * e.P * np.maximum(0, np.abs(e.resid) - e.zc_bonf * e.dp)
        e["nome"] = [nome.get((u, c), "(sem nome no mapa)") for u, c in zip(e.SG_UF, e.CD_MUNICIPIO)]
        e["perc_f"] = 100 * e.f.rank(pct=True)
        cal.loc[cal.ano == a, "municipios_com_p_holm_menor_5pct"] = int((e.p_holm < 0.05).sum())
    cal.to_csv(os.path.join(saida, "A31_modelo_calibracao.csv"), index=False)
    ex = pd.concat(EXCLUIDOS, ignore_index=True)
    ex["nome"] = [nome.get((u, c), "(sem nome no mapa)") for u, c in zip(ex.SG_UF, ex.CD_MUNICIPIO)]
    ex.to_csv(os.path.join(saida, "A31_excluidos.csv"), index=False)
    print("municipios-ano excluidos (Adendo 10a):", ex.groupby("ano").apply(lambda g: g[["SG_UF", "CD_MUNICIPIO"]].drop_duplicates().shape[0]).to_dict())

    cols_mun = ["ano", "SG_UF", "CD_MUNICIPIO", "nome", "P", "E", "dL", "dF", "dC", "f", "f_hat", "dp", "z", "p", "p_holm", "p_holm_5570", "outros_anos_com_z_ao_menos_igual", "teto_incond_votos_margem",
                "teto_alem_cauda_votos_margem"]
    allm = pd.concat([E[a][cols_mun] for a in ANOS], ignore_index=True)
    allm.to_csv(os.path.join(saida, "A31_municipios.csv"), index=False, float_format="%.6g")

    # Parte 2: distribuicao e posicao de Silva Jardim
    dist, vered = [], []
    for a in ANOS:
        e = E[a]
        f = e.f
        s = e[(e.SG_UF == SJ[0]) & (e.CD_MUNICIPIO == SJ[1])]
        d = dict(ano=a, municipios_elegiveis=len(e), excluidos_P_menor_20=int((M[a].P < PMIN).sum()), min=f.min(), p01=f.quantile(.01), p10=f.quantile(.1), p25=f.quantile(.25), mediana=f.median(),
                 p75=f.quantile(.75), p90=f.quantile(.9), p99=f.quantile(.99), max=f.max(), pct_fora_de_0_1=100 * float(((f < 0) | (f > 1)).mean()), f_nacional=M[a].dL.sum() / M[a].P.sum())
        if len(s):
            s = s.iloc[0]
            d.update(sj_f=s.f, sj_percentil=s.perc_f, sj_f_hat=s.f_hat, sj_z=s.z, sj_P=int(s.P), sj_dL=int(s.dL), sj_dF=int(s.dF), sj_p_holm=s.p_holm, sj_p_holm_5570=s.p_holm_5570,
                     sj_municipios_com_f_mais_extremo=int((np.abs(f - f.median()) >= abs(s.f - f.median())).sum()))
        dist.append(d)
        if a == 2026:
            tetoS = float(s.teto_incond_votos_margem), float(s.teto_alem_cauda_votos_margem)
            hs = s.p_holm
            if hs >= 0.05:
                v = "DENTRO DA CAUDA ESPERADA"
            elif s.outros_anos_com_z_ao_menos_igual >= 1:
                v = "FORA DA CAUDA DO MODELO, COM PRECEDENTE"
            else:
                v = "FORA DA CAUDA, SEM PRECEDENTE"
            vered.append(dict(municipio="Silva Jardim/RJ", ano=2026, f=s.f, f_hat=s.f_hat, z=s.z, df_t=s.df_t, p_bilateral=s.p, p_holm=s.p_holm, p_holm_5570=s.p_holm_5570,
                              outros_anos_com_z_ao_menos_igual=int(s.outros_anos_com_z_ao_menos_igual), veredito=v, teto_incondicional_votos_margem=tetoS[0],
                              teto_incondicional_pct_margem=100 * tetoS[0] / MARGEM, teto_alem_da_cauda_votos_margem=tetoS[1], teto_alem_da_cauda_pct_margem=100 * tetoS[1] / MARGEM,
                              nota="forma da distribuicao entre municipios; teto de pior caso, nao estimativa"))
    sj26 = E[2026][(E[2026].SG_UF == SJ[0]) & (E[2026].CD_MUNICIPIO == SJ[1])].iloc[0]
    res_sj.update(concentracao(pq, 2026, SJ[0], SJ[1], sj26.f_hat, sj26.f))
    res_sj.update(f_hat=sj26.f_hat, z=sj26.z, erro_do_modelo_f_menos_f_hat=sj26.f - sj26.f_hat)
    pd.DataFrame([res_sj]).to_csv(os.path.join(saida, "A31_sj_resumo.csv"), index=False)
    pd.DataFrame(dist).to_csv(os.path.join(saida, "A31_distribuicao_f.csv"), index=False)
    pd.DataFrame(vered).to_csv(os.path.join(saida, "A31_veredito_silva_jardim.csv"), index=False)
    print(pd.DataFrame(vered).T.to_string())

    # Suplementar S1, S2, S3 (Adendo 10b, pos-hoc, exploratorio)
    SUP = {a: suplementar(M[a].reset_index(drop=True), X[a].reset_index(drop=True)) for a in ANOS}
    supl, sup_ext = [], []
    for a in ANOS:
        S_ = SUP[a]
        for k in ("L", "F"):
            zo = np.concatenate([SUP[b]["z" + k].values for b in ANOS if b != a])
            df = fit_df(zo)
            S_["df" + k] = df
            S_["p" + k] = 2 * stats.t.sf(np.abs(S_["z" + k]), df)
            S_["pholm" + k] = holm(S_["p" + k].values)
            zc = stats.t.isf(0.05 / (2 * M_PEDIDO), df)
            S_["teto" + k] = 2 * S_.APT1 * np.maximum(0, np.abs(S_["r" + k]) - zc * S_["esc" + k])
            S_["zc" + k] = zc
        s_ = S_[(S_.SG_UF == SJ[0]) & (S_.CD_MUNICIPIO == SJ[1])].iloc[0]
        supl.append(dict(ano=a, municipios=len(S_), sj_dL=int(s_.dL), sj_dF=int(s_.dF), sj_zL=s_.zL, sj_zF=s_.zF, df_L=s_.dfL, df_F=s_.dfF, zc_Bonferroni_5570_L=s_.zcL, zc_Bonferroni_5570_F=s_.zcF,
                         sj_p_holm_L=s_.pholmL, sj_p_holm_F=s_.pholmF, sj_comum=bool(s_.pholmL >= 0.05 and s_.pholmF >= 0.05),
                         n_mun_com_zL_ao_menos_igual=int((np.abs(S_.zL) >= abs(s_.zL)).sum()), n_mun_com_zF_ao_menos_igual=int((np.abs(S_.zF) >= abs(s_.zF)).sum()),
                         mun_com_pholm_menor_5pct_L=int((S_.pholmL < 0.05).sum()), mun_com_pholm_menor_5pct_F=int((S_.pholmF < 0.05).sum())))
    pd.DataFrame(supl).to_csv(os.path.join(saida, "A31_suplementar_S1_silva_jardim.csv"), index=False)
    S26 = SUP[2026]
    S26["nome"] = [nome.get((u, c), "(sem nome no mapa)") for u, c in zip(S26.SG_UF, S26.CD_MUNICIPIO)]
    S26[["SG_UF", "CD_MUNICIPIO", "nome", "APT1", "dL", "dF", "rL", "rF", "zL", "zF", "pL", "pF", "pholmL", "pholmF", "tetoL", "tetoF"]].to_csv(os.path.join(saida, "A31_suplementar_S1_2026.csv"), index=False, float_format="%.6g")
    ext = pd.concat([S26.reindex(S26.zL.abs().sort_values(ascending=False).index).head(10).assign(eixo="zL (ganho do PT)"),
                     S26.reindex(S26.zF.abs().sort_values(ascending=False).index).head(10).assign(eixo="zF (ganho do oponente)")])
    ext[["eixo", "SG_UF", "CD_MUNICIPIO", "nome", "APT1", "dL", "dF", "zL", "zF", "pholmL", "pholmF", "tetoL", "tetoF"]].to_csv(os.path.join(saida, "A31_suplementar_S1_extremos_2026.csv"), index=False, float_format="%.6g")
    tl, tf = float(S26.tetoL.sum()), float(S26.tetoF.sum())
    pd.DataFrame([dict(escopo="todos os municipios de 2026", teto_alem_cauda_zL_votos_margem=tl, pct_margem_L=100 * tl / MARGEM, teto_alem_cauda_zF_votos_margem=tf, pct_margem_F=100 * tf / MARGEM,
                       nota="soma dos tetos por municipio, cada eixo separado; teto de pior caso, nao estimativa; pos-hoc")]).to_csv(os.path.join(saida, "A31_suplementar_S1_tetos.csv"), index=False)
    s2 = []
    for a in ANOS:
        e_ = E[a]
        for escopo, mask in (("todos os elegiveis", e_.P > -10**9), ("dL >= 500", e_.dL >= 500)):
            g = e_[mask]
            s2.append(dict(ano=a, escopo=escopo, municipios=len(g), com_dF_menor_ou_igual_1=int((g.dF <= 1).sum()), pct=100 * float((g.dF <= 1).mean()) if len(g) else np.nan,
                           com_dL_ao_menos_900_e_dF_menor_ou_igual_1=int(((g.dL >= 900) & (g.dF <= 1)).sum())))
    pd.DataFrame(s2).to_csv(os.path.join(saida, "A31_suplementar_S2_dF_menor_igual_1.csv"), index=False)
    print(pd.DataFrame(supl).T.to_string()); print(pd.DataFrame(s2).to_string()); print(ext[["eixo", "nome", "SG_UF", "APT1", "dL", "dF", "zL", "zF", "pholmL", "pholmF", "tetoL", "tetoF"]].round(3).to_string()); print("teto S1:", tl, tf)

    # Parte 4: moedas
    allM = pd.concat([M[a] for a in ANOS], ignore_index=True)
    nac, mun = moedas(allM)
    nac.to_csv(os.path.join(saida, "A31_moedas_nacional.csv"), index=False)
    mun.to_csv(os.path.join(saida, "A31_moedas_municipios.csv"), index=False)
    p_sj = {}
    for nm, p0 in (("p0 = 0,5", 0.5), ("p0 = razao PT/(PT+OPO) do municipio no T1", sj.PT1 / (sj.PT1 + sj.OP1)), ("p0 = razao PT/(PT+OPO) nacional no T1", M[2026].PT1.sum() / (M[2026].PT1.sum() + M[2026].OP1.sum()))):
        q = 1 - p0
        lp = float(logsumexp([stats.binom.logpmf(k, int(sj.P), q) for k in range(int(sj.dF) + 1)])) / np.log(10)
        p_sj[nm] = (p0, lp)
    pd.DataFrame([dict(variante=k, p0=v[0], log10_prob_dF_menor_ou_igual_observado=v[1]) for k, v in p_sj.items()]).to_csv(os.path.join(saida, "A31_moedas_silva_jardim.csv"), index=False)
    print(nac.round(3).to_string()); print(mun.round(2).to_string()); print(p_sj)

    # Parte 5: 20 mais extremos de 2026
    e = E[2026].copy()
    e = e.reindex(e.z.abs().sort_values(ascending=False).index).head(20).copy()
    e["rank_abs_z"] = range(1, 21)
    dm = DOM[2026].loc[e.index]
    e = e.join(dm)
    e22 = E[2022].set_index(["SG_UF", "CD_MUNICIPIO"])
    lim22 = np.quantile(np.abs(E[2022].z), 0.95)
    conc = []
    for r in e.itertuples():
        conc.append(concentracao(pq, 2026, r.SG_UF, r.CD_MUNICIPIO, r.f_hat, r.f))
    e = e.reset_index(drop=True).join(pd.DataFrame(conc))
    e["z_2022"] = [e22.z.get((u, c), np.nan) for u, c in zip(e.SG_UF, e.CD_MUNICIPIO)]
    e["f_2022"] = [e22.f.get((u, c), np.nan) for u, c in zip(e.SG_UF, e.CD_MUNICIPIO)]
    e["entre_5pct_mais_extremos_2022"] = np.abs(e.z_2022) > lim22
    e["veredito_modelo"] = np.where(e.p_holm >= 0.05, "DENTRO DA CAUDA ESPERADA", np.where(e.outros_anos_com_z_ao_menos_igual >= 1, "FORA DA CAUDA DO MODELO, COM PRECEDENTE", "FORA DA CAUDA, SEM PRECEDENTE"))
    e["fluxo_bruto_sobre_P"] = (e.dL.abs() + e.dF.abs()) / e.P.abs()
    out = e[["rank_abs_z", "SG_UF", "CD_MUNICIPIO", "nome", "P", "dL", "dF", "dC", "f", "f_hat", "z", "p_holm", "p_holm_5570", "outros_anos_com_z_ao_menos_igual", "veredito_modelo", "fluxo_bruto_sobre_P", "secoes", "C3_dL", "C3_P", "C3_dL_so_positivos", "C3_P_so_positivos", "pct_secoes_do_mesmo_lado", "ganho",
             "terc_dom_nome", "terc_dom_pct_comp1", "terc_dom_apoio", "f_2022", "z_2022", "entre_5pct_mais_extremos_2022", "teto_incond_votos_margem", "teto_alem_cauda_votos_margem"]]
    out.to_csv(os.path.join(saida, "A31_top20_2026.csv"), index=False, float_format="%.6g")
    tt = dict(grupo="20 mais extremos de 2026", teto_incondicional_votos_margem=float(out.teto_incond_votos_margem.sum()), teto_incondicional_pct_margem=100 * float(out.teto_incond_votos_margem.sum()) / MARGEM,
              teto_alem_da_cauda_votos_margem=float(out.teto_alem_cauda_votos_margem.sum()), teto_alem_da_cauda_pct_margem=100 * float(out.teto_alem_cauda_votos_margem.sum()) / MARGEM)
    ts = dict(grupo="Silva Jardim", teto_incondicional_votos_margem=tetoS[0], teto_incondicional_pct_margem=100 * tetoS[0] / MARGEM, teto_alem_da_cauda_votos_margem=tetoS[1], teto_alem_da_cauda_pct_margem=100 * tetoS[1] / MARGEM)
    pd.DataFrame([ts, tt]).to_csv(os.path.join(saida, "A31_tetos.csv"), index=False)
    print(pd.DataFrame([ts, tt]).T.to_string())
    pd.set_option("display.width", 250)
    print(out.drop(columns=["terc_dom_apoio"]).round(3).to_string())

    # Parte 6: secoes de Silva Jardim, T1 e T2, com colunas vazias para o BU impresso
    cs = pd.read_parquet(os.path.join(pq2, "cand_t1_2026.parquet"))
    cs = cs[(cs.SG_UF == SJ[0]) & (cs.CD_MUNICIPIO == SJ[1])].set_index(KEY)
    ss = secoes_mun(pq, 2026, *SJ)
    ss = ss.join(cs[[c for c in cs.columns if c.startswith("v")]])
    ss = ss.rename(columns={"QT_APTOS1": "aptos_T1", "QT_COMPARECIMENTO1": "comparecimento_T1", "lula1": "lula_T1", "dir1": "flavio_T1", "branco1": "brancos_T1", "nulo1": "nulos_T1",
                            "QT_APTOS2": "aptos_T2", "QT_COMPARECIMENTO2": "comparecimento_T2", "lula2": "lula_T2", "dir2": "flavio_T2", "branco2": "brancos_T2", "nulo2": "nulos_T2"})
    ss["terceiros_T1"] = ss.nominal1 - ss.lula_T1 - ss.flavio_T1
    ss["dL"], ss["dF"], ss["dC"] = ss.lula_T2 - ss.lula_T1, ss.flavio_T2 - ss.flavio_T1, ss.comparecimento_T2 - ss.comparecimento_T1
    for c in ("T1", "T2"):
        for k in ("aptos", "comparecimento", "lula", "flavio", "brancos", "nulos"):
            ss[f"impresso_{k}_{c}"] = ""
    ss = ss.reset_index()
    ordem = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "aptos_T1", "comparecimento_T1", "lula_T1", "flavio_T1", "terceiros_T1"] + [c for c in ss.columns if c.startswith("v") and c[1:].isdigit()] + \
            ["brancos_T1", "nulos_T1", "aptos_T2", "comparecimento_T2", "lula_T2", "flavio_T2", "brancos_T2", "nulos_T2", "dL", "dF", "dC"] + [c for c in ss.columns if c.startswith("impresso_")]
    ss[ordem].to_csv(os.path.join(saida, "A31_silva_jardim_secoes.csv"), index=False)
    print("secoes de Silva Jardim:", len(ss), "| soma dL", int(ss.dL.sum()), "soma dF", int(ss.dF.sum()), "soma dC", int(ss.dC.sum()))
    print(cal.round(4).to_string()); print(pd.DataFrame(dist).T.to_string())
    print(conf.to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
