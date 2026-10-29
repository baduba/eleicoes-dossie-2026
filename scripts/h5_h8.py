"""H5 a H8 + classificacao A/B/C da regua historica (2014, 2018, 2022, 2026).

Convencao: PT = candidato 13 (coluna lula), OPO = oponente do 2o turno (coluna dir). share = share entre os dois.
As metricas pre-registradas (00_preregistro.md, Adendo 1) sao acumuladas em METRICAS e usadas por abc()."""
import os
import re
import unicodedata
from math import gcd
import numpy as np
import pandas as pd
from scipy import stats
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, par_ano, fe_ols
from h1_h4 import tenta

METRICAS = {}          # (ano, turno) -> dict de metricas pre-registradas
NOME_OPO = {2014: "Aecio", 2018: "Bolsonaro", 2022: "Bolsonaro", 2026: "Flavio"}


def _m(a, t):
    return METRICAS.setdefault((a, t), {})


def _apuradas(d):
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.QT_APTOS > 0)]


def within_corr(x, a, b, g):
    """Correlacao entre a e b depois de remover a media do grupo (local de votacao)."""
    y = x[[a, b, g]].dropna()
    y = y[y.groupby(g)[a].transform("size") > 1]
    da = y[a] - y.groupby(g)[a].transform("mean")
    db = y[b] - y.groupby(g)[b].transform("mean")
    return float(np.corrcoef(da, db)[0, 1]), len(y)


# ----------------------------------------------------------------------------------------------- tipo de local
def _ascii(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


TIPOS = [("indigena", r"ALDEIA|INDIGENA|TERRA IND|POSTO IND"), ("prisional", r"PRESIDIO|PENITENCIARIA|CADEIA|DETENCAO|PRISIONAL|SOCIOEDUCATIVO|RESSOCIALIZ|CASE "),
         ("hospital_asilo", r"HOSPITAL|ASILO|LAR DE IDOSOS|CLINICA|SANTA CASA|ABRIGO"), ("quilombola", r"QUILOMB"),
         ("militar", r"QUARTEL|BATALHAO|BASE AEREA|BRIGADA|EXERCITO"), ("rural_comunidade", r"ASSENTAMENTO|FAZENDA|POVOADO|COMUNIDADE|SITIO|ZONA RURAL|VILA |LINHA ")]


def tipo_local(nomes):
    u = nomes.map(_ascii)
    out = pd.Series("escola_outro", index=nomes.index)
    for nome, rx in reversed(TIPOS):
        out[u.str.contains(rx, regex=True)] = nome
    return out


def _locais(D, ano, dirp):
    p = os.path.join(dirp, f"locais_{ano}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"falta {p} (rodar 01b_locais.py)")
    return pd.read_parquet(p)


# ----------------------------------------------------------------------------------------------- H5
def h5(D, reg, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    linhas = []
    for (a, t), d in sorted(D.items()):
        x0 = _apuradas(d)
        x = x0[x0.valid2 >= 30]
        hi = x0[x0.turnout >= .95]
        met = _m(a, t)
        met["M5c"] = 1e5 * len(hi) / len(x0)
        for cand, sh in (("PT", "lula_sh"), ("OPO", "dir_sh")):
            met[f"M5a_{cand}"] = float(((x.turnout >= .9) & (x[sh] >= .9)).mean())
            r, n = within_corr(x, "turnout", sh, "uf_local")
            met[f"M5b_{cand}"] = r
        linhas.append(dict(ano=a, turno=t, secoes=len(x0), turnout_ge95=len(hi), por_100k=met["M5c"],
                           ge95_PT90=int((hi.lula_sh >= .9).sum()), ge95_OPO90=int((hi.dir_sh >= .9).sum()),
                           M5a_PT=met["M5a_PT"], M5a_OPO=met["M5a_OPO"], M5b_PT=met["M5b_PT"], M5b_OPO=met["M5b_OPO"]))
    out["h5_metricas"] = pd.DataFrame(linhas)
    # figuras Klimek (T2 e T1)
    figdir = os.path.join(out["_saida"], "figs"); os.makedirs(figdir, exist_ok=True)
    for t in (2, 1):
        anos = [a for a in (2014, 2018, 2022, 2026) if (a, t) in D]
        fig, ax = plt.subplots(2, len(anos), figsize=(3.6 * len(anos), 7), squeeze=False)
        for j, a in enumerate(anos):
            x = base(D[(a, t)])
            for i, (cand, sh, nm) in enumerate((("PT", "lula_sh", "PT (13)"), ("OPO", "dir_sh", NOME_OPO[a]))):
                h = ax[i][j].hist2d(x.turnout.clip(0, 1), x[sh], bins=[50, 50], range=[[0, 1], [0, 1]], norm=matplotlib.colors.LogNorm(), cmap="viridis")
                ax[i][j].set_title(f"{a} T{t} {nm}", fontsize=9); ax[i][j].set_xlabel("comparecimento"); ax[i][j].set_ylabel("voto no candidato")
        fig.tight_layout(); fig.savefig(os.path.join(figdir, f"klimek_T{t}.png"), dpi=110); plt.close(fig)
    out["h5_figuras"] = "figs/klimek_T1.png, figs/klimek_T2.png"
    tt = []
    for (a, t), d in sorted(D.items()):
        x0 = _apuradas(d); x0 = x0[x0.QT_APTOS >= 20]
        for tam, g in x0.groupby(_tam(x0.QT_APTOS)):
            tt.append(dict(ano=a, turno=t, tamanho=tam, secoes=len(g), ge95=int((g.turnout >= .95).sum()), taxa_ge95_por_10k=1e4 * (g.turnout >= .95).mean()))
    out["h5_taxa_ge95_por_tamanho"] = pd.DataFrame(tt).pivot_table(index=["tamanho", "turno"], columns="ano", values="taxa_ge95_por_10k").round(2).reset_index()

    return _h5_carac(D, reg, out)     # caracterizacao das secoes com comparecimento >= 95% no T2/2026


def _tam(a):
    return pd.cut(a, [0, 50, 150, 300, 1e9], labels=["<=50", "51-150", "151-300", ">300"]).astype(str)


def _h5_carac(D, reg, out):
    L26 = _locais(D, 2026, out["_parquet"]); L22 = _locais(D, 2022, out["_parquet"])
    L26["tipo"] = tipo_local(L26.NM_LOCAL_VOTACAO); L22["tipo"] = tipo_local(L22.NM_LOCAL_VOTACAO)
    def prep(a, t, L):
        x = _apuradas(D[(a, t)]); x = x[x.QT_APTOS >= 20].merge(L[KEY + ["tipo"]], on=KEY, how="left")
        x["tipo"] = x.tipo.fillna("desconhecido"); x["tam"] = _tam(x.QT_APTOS)
        return x
    x26, x22 = prep(2026, 2, L26), prep(2022, 2, L22)
    t1_26, t1_22 = prep(2026, 1, L26), prep(2022, 1, L22)
    # nova = sem par no mesmo turno da eleicao anterior (2026 vs 2022)
    k22 = set(map(tuple, D[(2022, 2)][KEY].values))
    x26["nova"] = [tuple(r) not in k22 for r in x26[KEY].values]
    hi = x26[x26.turnout >= .95].copy()
    t1 = D[(2026, 1)].set_index(KEY)[["turnout", "manual_rate", "atraso_min"]].add_suffix("_t1")
    hi = hi.join(t1, on=KEY)
    ant = D[(2022, 2)].set_index(KEY)[["QT_APTOS", "turnout"]].add_suffix("_22")
    hi = hi.join(ant, on=KEY)
    hi["so_no_T2"] = hi.turnout_t1 < .90
    car = []
    for nome, mask in (("todas >=95%", slice(None)), ("PT>=90%", hi.lula_sh >= .9), ("OPO>=90%", hi.dir_sh >= .9)):
        s = hi[mask] if not isinstance(mask, slice) else hi
        car.append(dict(grupo=nome, secoes=len(s), pct_novas=100 * s.nova.mean(), aptos_mediana=s.QT_APTOS.median(), manual_medio=s.manual_rate.mean(),
                        atraso_medio_min=s.atraso_min.mean(), turnout_T1_medio=s.turnout_t1.mean(), pct_so_no_T2=100 * s.so_no_T2.mean(),
                        pct_aptos_caiu_vs_2022=100 * (s.QT_APTOS < s.QT_APTOS_22).mean()))
    car.append(dict(grupo="TODAS as secoes (referencia)", secoes=len(x26), pct_novas=100 * x26.nova.mean(), aptos_mediana=x26.QT_APTOS.median(),
                    manual_medio=x26.manual_rate.mean(), atraso_medio_min=x26.atraso_min.mean()))
    out["h5_caracterizacao_2026T2"] = pd.DataFrame(car)
    out["h5_por_tipo"] = pd.DataFrame({"n_ge95": hi.tipo.value_counts(), "n_total": x26.tipo.value_counts()}).fillna(0).assign(
        pct_ge95_dentro_do_tipo=lambda z: 100 * z.n_ge95 / z.n_total, pct_do_total_ge95=lambda z: 100 * z.n_ge95 / z.n_ge95.sum(),
        pct_do_total_secoes=lambda z: 100 * z.n_total / z.n_total.sum()).round(3)
    out["h5_por_tamanho_nova"] = hi.groupby(["tam", "nova"]).size().unstack(fill_value=0)
    out["h5_por_uf"] = hi.SG_UF.value_counts().head(10).to_frame("secoes_ge95")
    # numerador x denominador: nas secoes antigas com >=95% em 2026, o que mudou desde 2022: aptos (denominador) ou comparecimento (numerador)?
    ant2 = D[(2022, 2)].set_index(KEY)[["QT_APTOS", "QT_COMPARECIMENTO"]].add_suffix("_22")
    ve = x26.join(ant2, on=KEY, how="inner")
    ve = ve[(ve.QT_APTOS_22 >= 20) & (ve.QT_APTOS / ve.QT_APTOS_22).between(.5, 1.5)]
    ve["alto"] = ve.turnout >= .95
    out["h5_numerador_denominador"] = ve.groupby("alto").apply(lambda g: pd.Series(dict(
        secoes=len(g), aptos_2026_sobre_2022_mediana=float((g.QT_APTOS / g.QT_APTOS_22).median()),
        comparecimento_2026_sobre_2022_mediana=float((g.QT_COMPARECIMENTO / g.QT_COMPARECIMENTO_22.replace(0, np.nan)).median()),
        turnout_2022_mediano=float((g.QT_COMPARECIMENTO_22 / g.QT_APTOS_22).median()))), include_groups=False).reset_index()
    out["h5_so_no_T2"] = pd.DataFrame([dict(secoes_ge95_no_T2=len(hi), dessas_so_no_T2=int(hi.so_no_T2.sum()),
                                           votos_validos_dessas=int(hi[hi.so_no_T2].valid2.sum()), lula_sh_dessas=hi[hi.so_no_T2].lula.sum() / max(1, hi[hi.so_no_T2].valid2.sum()))])
    # padronizacao indireta: quantas secoes >=95% em 2026 seriam esperadas se as taxas de 2022 por estrato (tipo x tamanho) valessem?
    def taxa(x):
        g = x.assign(hi=(x.turnout >= .95)).groupby(["tipo", "tam"])
        return g.hi.agg(["sum", "size"])
    res = []
    for rot, (xa, xb) in {"T2 (2026 vs taxas 2022/T2)": (x26, x22), "T1 (2026 vs taxas 2022/T1)": (t1_26, t1_22)}.items():
        tb, ta = taxa(xb), taxa(xa)
        tb["r"] = tb["sum"] / tb["size"]
        m = ta.join(tb[["r", "size"]].rename(columns={"size": "n_base"}), how="left").fillna({"r": 0.0, "n_base": 1})
        esp = float((m["size"] * m.r).sum()); obs = int(m["sum"].sum())
        var = float((m["size"] ** 2 * m.r * (1 - m.r) / m.n_base).sum())
        lr = np.log(obs / esp); se = float(np.sqrt(1 / obs + var / esp ** 2))
        res.append(dict(comparacao=rot, observado=obs, esperado_pela_composicao=esp, razao=obs / esp, log_razao=lr, ep_log_razao=se))
    out["h5_padronizacao"] = pd.DataFrame(res)
    r2, r1 = res
    mv = float(hi.valid2.mean())
    reg.add("H5", "secoes com comparecimento >=95% no T2/2026: excesso sobre o esperado pela composicao (tipo x tamanho, taxas 2022)",
            r2["log_razao"], r2["ep_log_razao"], [("mesmo teste no T1/2026", r1["log_razao"], r1["ep_log_razao"])],
            expo=r2["esperado_pela_composicao"] * mv, fator=1.0,
            nota="expo = secoes esperadas x votos validos medios; fator 1 (todos os votos extras para PT)")


# ----------------------------------------------------------------------------------------------- H6
ANTERIOR = {2026: 2022, 2022: 2018, 2018: 2014}


def h6(D, reg, out):
    linhas, ests = [], {}
    for a in (2026, 2022, 2018):
        if a not in out["anos"] or ANTERIOR[a] not in out["anos"]:
            continue
        w = par_ano(D, a)
        prev = set(map(tuple, D[(ANTERIOR[a], 2)][KEY].values))
        w["nova"] = [float(tuple(r) not in prev) for r in w[KEY].values]
        for nome, y, xs in (("lula_sh T2 | lula_sh T1", "lula_sh", ["nova", "lula_sh_t1"]), ("turnout T2 | turnout T1", "turnout", ["nova", "turnout_t1"]),
                            ("lula_sh T1 (sem lag)", "lula_sh_t1", ["nova"]), ("turnout T1 (sem lag)", "turnout_t1", ["nova"])):
            r = tenta(out, f"H6 {a} {nome}", fe_ols, w, y, xs, "uf_local")
            if r is not None:
                linhas.append(dict(ano=a, spec=nome, coef=r.loc["nova", "coef"], ep=r.loc["nova", "se"], p=r.loc["nova", "p"], secoes_novas=int(w.nova.sum()), n=int(r.n.iloc[0])))
                if nome.startswith("lula_sh T2"):
                    ests[a] = (r.loc["nova", "coef"], r.loc["nova", "se"], float(w[w.nova == 1].valid2.sum()))
    # robustez: (i) interacao nova x T1 centrado (inclinacao heterogenea), (ii) controles de tamanho e comparecimento, (iii) so secoes de 100 a 500 aptos
    rob = []
    for a in (2026, 2022, 2018):
        if a not in out["anos"] or ANTERIOR[a] not in out["anos"]:
            continue
        w = par_ano(D, a)
        prev = set(map(tuple, D[(ANTERIOR[a], 2)][KEY].values))
        w["nova"] = [float(tuple(r) not in prev) for r in w[KEY].values]
        w["t1c"] = w.lula_sh_t1 - w.lula_sh_t1.mean(); w["nova_x_t1"] = w.nova * w.t1c
        w["laptos"] = np.log(w.QT_APTOS)
        for nome, ww, xs in (("interacao nova x T1 (efeito no T1 medio)", w, ["nova", "t1c", "nova_x_t1"]),
                             ("controles log aptos e comparecimento T1", w, ["nova", "lula_sh_t1", "laptos", "turnout_t1"]),
                             ("so secoes de 100 a 500 aptos", w[w.QT_APTOS.between(100, 500)], ["nova", "lula_sh_t1"])):
            r = tenta(out, f"H6 robustez {a} {nome}", fe_ols, ww, "lula_sh", xs, "uf_local")
            if r is not None:
                rob.append(dict(ano=a, variante=nome, coef_nova=r.loc["nova", "coef"], ep=r.loc["nova", "se"], secoes_novas=int(ww.nova.sum())))
    out["h6_robustez"] = pd.DataFrame(rob)
    out["h6_coef"] = pd.DataFrame(linhas)
    if 2026 not in ests:
        raise NaoExecutado("H6: sem estimativa para 2026")
    pl = [(f"{a}/T2", ests[a][0], ests[a][1]) for a in (2022, 2018) if a in ests]
    if not pl:
        raise NaoExecutado("H6: placebos 2022 e 2018 indisponiveis (precisa de 2018/2014 carregados)")
    reg.add("H6", "secoes novas vs antigas do mesmo local: Lula% no T2 dado o T1", ests[2026][0], ests[2026][1], pl, expo=ests[2026][2],
            nota="nova = sem par no T2 da eleicao anterior; placebos = secoes novas de 2022 (vs 2018) e 2018 (vs 2014)")


# ----------------------------------------------------------------------------------------------- H7
def outliers(d, minsec=4, corte=3.0):
    """z de cada secao contra as OUTRAS secoes do mesmo local (leave-one-out), ajustado por binomial e sobredispersao."""
    x = base(d)
    g = x.groupby("uf_local")
    L = g.lula.transform("sum"); V = g.valid2.transform("sum"); n = g.lula.transform("size")
    Vo = V - x.valid2
    p = (L - x.lula) / Vo.replace(0, np.nan)
    ok = (n >= minsec) & (Vo > 0) & p.between(.03, .97)
    z = (x.lula - x.valid2 * p) / np.sqrt(x.valid2 * p * (1 - p))
    z = z[ok]; x = x[ok]; p = p[ok]
    phi = float(np.median(z ** 2) / 0.4549)
    zs = z / np.sqrt(phi)
    excesso = x.lula - x.valid2 * p
    return x.assign(z=z, zs=zs, excesso=excesso), phi


def h7(D, reg, out):
    linhas = []; dados = {}
    for (a, t), d in sorted(D.items()):
        x, phi = outliers(d)
        n = len(x)
        up, dn = x[x.zs > 3], x[x.zs < -3]
        up5, dn5 = x[x.z > 5], x[x.z < -5]
        met = _m(a, t)
        met["M7a_up"] = 1e4 * len(up) / n; met["M7a_down"] = 1e4 * len(dn) / n
        met["M7b"] = (len(up) / max(len(dn), 1))
        linhas.append(dict(ano=a, turno=t, secoes_em_locais_ge4=n, sobredispersao_phi=phi, up_3=len(up), down_3=len(dn), taxa_up_10k=met["M7a_up"],
                           taxa_down_10k=met["M7a_down"], razao_up_down=met["M7b"], up_5_sem_ajuste=len(up5), down_5_sem_ajuste=len(dn5),
                           excesso_votos_up=float(up.excesso.sum()), excesso_votos_down=float(-dn.excesso.sum())))
        dados[(a, t)] = (n, len(up), len(dn), float(up.excesso.mean()) if len(up) else 0.0)
    out["h7_outliers"] = pd.DataFrame(linhas)
    if (2026, 2) not in dados:
        raise NaoExecutado("H7: sem 2026/T2")
    n26, u26, d26, ex26 = dados[(2026, 2)]
    pls = [(k, dados[k]) for k in ((2022, 1), (2022, 2), (2026, 1))]
    # (i) taxa de outliers para cima (Poisson)
    r26 = 1e4 * u26 / n26; s26 = 1e4 * np.sqrt(max(u26, 1)) / n26
    pl = [(f"{a}/T{t}", 1e4 * u / n, 1e4 * np.sqrt(max(u, 1)) / n) for (a, t), (n, u, dd, _) in pls]
    reg.add("H7", "outliers locais para cima (pro-PT), |z ajustado| > 3, por 10 mil secoes", r26, s26, pl, expo=(n26 / 1e4) * ex26, fator=2.0,
            nota="expo = (secoes/10 mil) x excesso medio de votos por outlier; excesso relativo as outras secoes do mesmo local")
    # (ii) assimetria: proporcao de outliers que sao para cima
    f26 = u26 / (u26 + d26); sf26 = np.sqrt(f26 * (1 - f26) / (u26 + d26))
    pl2 = [(f"{a}/T{t}", u / (u + dd), np.sqrt((u / (u + dd)) * (1 - u / (u + dd)) / (u + dd))) for (a, t), (n, u, dd, _) in pls]
    reg.add("H7", "assimetria: proporcao de outliers que sao pro-PT", f26, sf26, pl2, expo=(u26 + d26) * ex26, fator=2.0,
            nota="expo = total de outliers x excesso medio")


# ----------------------------------------------------------------------------------------------- H8
def _digit_stats(counts, B=200, seed=1):
    dig = (counts % 10).astype(int).values
    obs = np.bincount(dig, minlength=10)
    n = obs.sum(); exp = n / 10
    chi = float(((obs - exp) ** 2 / exp).sum())
    V = np.sqrt(chi / (n * 9))
    rng = np.random.default_rng(seed)
    vs = []
    for _ in range(B):
        b = np.bincount(rng.choice(dig, size=len(dig), replace=True), minlength=10)
        vs.append(np.sqrt((((b - exp) ** 2 / exp).sum()) / (n * 9)))
    return obs, chi, float(stats.chi2.sf(chi, 9)), float(V), float(np.std(vs))


def h8(D, reg, out):
    linhas = []; V = {}; R = {}
    for (a, t), d in sorted(D.items()):
        x = base(d); met = _m(a, t)
        for cand, col, k in (("PT", "lula", "M8a_V_PT"), ("OPO", "dir", "M8a_V_OPO")):
            c = x[col][x[col] >= 20]
            obs, chi, p, v, sv = _digit_stats(c)
            met[k] = v; V[(a, t, cand)] = (v, sv)
            linhas.append(dict(ano=a, turno=t, cand=cand, n=len(c), chi2=chi, p=p, V_cramer=v, ep_V_boot=sv, **{f"d{i}": int(obs[i]) for i in range(10)}))
        # percentual inteiro exato (Kobak 2016): P(100*k/n inteiro) ~ (gcd(n,100)+1)/(n+1) se k varia suavemente
        n = x.valid2.astype(int).values
        gcdv = np.gcd(n, 100)
        esp = float(((gcdv + 1) / (n + 1)).sum())
        # simetrico: se 100*lula % n == 0 entao 100*dir % n == 0 (lula+dir=n); um unico teste serve aos dois candidatos
        obs_i = int(((100 * x["lula"].astype(int).values) % n == 0).sum())
        met["M8b_PT"] = met["M8b_OPO"] = obs_i / esp
        R[(a, t)] = (obs_i / esp, np.sqrt(max(obs_i, 1)) / esp)
        linhas.append(dict(ano=a, turno=t, cand="PT=OPO", teste="percentual inteiro", observado=obs_i, esperado=esp, razao=obs_i / esp))
    out["h8_digitos"] = pd.DataFrame(linhas)
    for cand in ("PT", "OPO"):
        v26, s26 = V[(2026, 2, cand)]
        reg.add("H8", f"ultimo digito: V de Cramer de {cand} no T2/2026", v26, s26,
                [(f"{a}/T{t}", *V[(a, t, cand)]) for (a, t) in ((2022, 1), (2022, 2), (2026, 1))], nota="teste de forma; V=0 e uniforme; sem conversao em votos")
    r26, sr26 = R[(2026, 2)]
    reg.add("H8", "percentual inteiro exato (PT e OPO, simetrico): obs/esperado no T2/2026", r26, sr26,
            [(f"{a}/T{t}", *R[(a, t)]) for (a, t) in ((2022, 1), (2022, 2), (2026, 1))], nota="teste de forma; razao 1 = esperado")


# ----------------------------------------------------------------------------------------------- A/B/C
RAZAO = ["M5a_PT", "M5a_OPO", "M5c", "M7a_up", "M7a_down", "M7b", "M8b_PT", "M8b_OPO"]
DIF = {"M5b_PT": .02, "M5b_OPO": .02, "M8a_V_PT": .005, "M8a_V_OPO": .005}


def _sim(m, x, y):
    if m in DIF:
        return abs(x - y) < DIF[m]
    if x == 0 and y == 0:
        return True
    if x == 0 or y == 0:
        return False
    return 0.8 <= x / y <= 1.25


def abc(D, reg, out):
    anos = [a for a in (2014, 2018, 2022, 2026)]
    faltam = [a for a in anos if a not in out["anos"]]
    if faltam:
        raise NaoExecutado(f"A/B/C precisa dos anos {faltam} (rode com todos os anos carregados)")
    ms = RAZAO + list(DIF)
    for t in (2, 1):
        if any(m not in METRICAS.get((a, t), {}) for a in anos for m in ms):
            raise NaoExecutado("A/B/C: metricas de H5, H7 e H8 ainda nao calculadas neste processo (rode H5 H7 H8 antes, na mesma execucao)")
    for t in (2, 1):
        tab = pd.DataFrame({a: {m: METRICAS[(a, t)][m] for m in ms} for a in anos})
        out[f"abc_metricas_T{t}"] = tab.round(5)
        res = []
        for m in ms:
            v = {a: tab.loc[m, a] for a in anos}
            s = lambda p, q: _sim(m, v[p], v[q])
            A = s(2014, 2022) and s(2022, 2026) and s(2014, 2026) and not s(2018, 2014) and not s(2018, 2022) and not s(2018, 2026)
            B = s(2014, 2018) and s(2022, 2026) and not s(2014, 2022) and not s(2014, 2026) and not s(2018, 2022) and not s(2018, 2026)
            C = all(s(p, q) for i, p in enumerate(anos) for q in anos[i + 1:])
            res.append(dict(metrica=m, **{f"{a}": v[a] for a in anos}, A=A, B=B, C=C, nenhum=not (A or B or C),
                            sim_22_26=s(2022, 2026), sim_14_18=s(2014, 2018), sim_14_26=s(2014, 2026), sim_18_22=s(2018, 2022)))
        r = pd.DataFrame(res)
        out[f"abc_classificacao_T{t}"] = r
        out[f"abc_resumo_T{t}"] = pd.DataFrame([dict(turno=t, metricas=len(r), A=int(r.A.sum()), B=int(r.B.sum()), C=int(r.C.sum()), nenhum=int(r.nenhum.sum()),
                                                   sim_22_26=int(r.sim_22_26.sum()), sim_14_18=int(r.sim_14_18.sum()), sim_18_22=int(r.sim_18_22.sum()), sim_14_26=int(r.sim_14_26.sum()))])
