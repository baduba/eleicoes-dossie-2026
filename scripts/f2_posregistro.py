"""Fase 2.1: versoes CORRIGIDAS (pos-registro, Adendo 6) de A1, A2, A3 e A12, e demonstracao de que o teste ORIGINAL acusa excesso sem manipulacao.
As linhas originais nao sao alteradas: as versoes corrigidas vao para um registro separado (posregistro_testes.csv)."""
import os
import numpy as np
import pandas as pd
from scipy import stats, optimize
from lib_auditoria import KEY, MARGEM, NaoExecutado, Registro, base, par_ano
from h1_h4 import tenta
from f2_a11_a15 import _serie, _lineares
from f2_a1_a3 import _pares


def _pos(out):
    return out["_reg_pos"]


# ------------------------------------------------------------------------------------------------------- A1
def _grupos_mun(b):
    uf = pd.factorize(b.SG_UF)[0]
    mun = pd.factorize(b.SG_UF + "_" + b.CD_MUNICIPIO.astype(str))[0]
    slots, grupos = [], []
    for u in range(uf.max() + 1):
        s = np.flatnonzero(uf == u)
        m = mun[s]; ordem = np.argsort(m, kind="stable"); ms = m[ordem]
        cortes = np.r_[0, np.flatnonzero(ms[1:] != ms[:-1]) + 1, len(ms)]
        slots.append(s); grupos.append([s[ordem[cortes[i]:cortes[i + 1]]] for i in range(len(cortes) - 1)])
    return slots, grupos


def _ordem_D(slots, grupos, N, rng):
    order = np.empty(N, dtype=np.int64)
    for s, gs in zip(slots, grupos):
        idx = rng.permutation(len(gs))
        order[s] = np.concatenate([rng.permutation(gs[i]) for i in idx])
    return order


def _run(sig):
    n_out = 0; best = 0
    for v in sig:
        n_out = n_out + 1 if v else 0; best = max(best, n_out)
    return best


def c1(D, reg, out):
    reps = int(os.environ.get("AUDITORIA_REPS_POS", "500")); K = 1000; k0 = 10; k10 = 100
    res, maxdevD = [], {}
    series = {}
    for ano, t in ((2026, 2), (2026, 1), (2022, 2), (2018, 2)):
        r = tenta(out, f"C1 {ano}/T{t}", _serie, D, out, ano, t, reps)
        if r is None:
            continue
        b, l, d, N, uf, idx, marg, share, slots, rng = r
        sl, gr = _grupos_mun(b)
        real = share(l, d)
        Dm = np.empty((reps, K))
        for i in range(reps):
            o = _ordem_D(sl, gr, N, rng); Dm[i] = share(l[o], d[o])
        med = np.median(Dm, axis=0); sd = Dm.std(axis=0, ddof=1)
        zD = np.abs(Dm[:, k10:] - med[k10:]) / sd[k10:]; c95 = float(np.quantile(zD.max(axis=1), .95))
        dev = np.abs(real - med)[k10:]
        mdr = 100 * np.abs(Dm[:, k10:] - med[k10:]).max(axis=1)
        res.append(dict(ano=ano, turno=t, maxdev_vs_D_pp_ge10pct=100 * float(dev.max()), maxdev_D_nulo_p95_pp=float(np.quantile(mdr, .95)), maior_sequencia_fora_envelope_D=_run(dev / sd[k10:] > c95),
                        secoes=N, pontos_ge10pct=K - k10))
        maxdevD[(ano, t)] = (100 * float(dev.max()), float(np.std(mdr, ddof=1)))
        series[(ano, t)] = (b, l, d, N, slots, sl, gr, share, rng)
    out["c1_corrigido_nulo_D"] = pd.DataFrame(res)
    # demonstracao: o teste ORIGINAL acusa saida do envelope B em series simuladas SEM manipulacao
    if (2026, 2) not in series:
        raise NaoExecutado("C1: 2026/T2 nao calculado")
    b, l, d, N, slots, sl, gr, share, rng = series[(2026, 2)]
    nsim, repsB = 20, 100
    dem = []
    for s in range(nsim):
        o = _ordem_D(sl, gr, N, rng); ls, ds = l[o], d[o]
        real = share(ls, ds)
        Bm = np.empty((repsB, K))
        for i in range(repsB):
            order = np.empty(N, dtype=np.int64)
            for sl_ in slots:
                order[sl_] = rng.permutation(sl_)
            Bm[i] = share(ls[order], ds[order])
        med = np.median(Bm, axis=0); sdB = Bm.std(axis=0, ddof=1)
        c95 = float(np.quantile((np.abs(Bm[:, k0:] - med[k0:]) / sdB[k0:]).max(axis=1), .95))
        dem.append(dict(simulacao=s, maxdev_vs_B_pp=100 * float(np.abs(real - med)[k0:].max()), maior_sequencia_fora_envelope_B=_run((np.abs(real - med)[k0:] / sdB[k0:]) > c95)))
    dm = pd.DataFrame(dem)
    orig = pd.read_csv(os.path.join(out["_saida"], "A1_a1_resumo.csv"))
    out["c1_demonstracao_original"] = pd.DataFrame([dict(
        eleicoes_reais_que_saem_do_envelope_B_por_20_pontos_ou_mais=f"{int((orig.maior_sequencia_fora_envelope >= 20).sum())} de {len(orig)}",
        simulacoes_sem_manipulacao=nsim, simulacoes_que_saem_do_envelope_B_por_20_pontos_ou_mais=int((dm.maior_sequencia_fora_envelope_B >= 20).sum()),
        maxdev_simulacoes_mediana_pp=float(dm.maxdev_vs_B_pp.median()), maxdev_simulacoes_max_pp=float(dm.maxdev_vs_B_pp.max()),
        maxdev_real_2026T2_pp=float(orig[(orig.ano == 2026) & (orig.turno == 2)].maxdev_vs_B_pp.iloc[0]), maxdev_placebos_pp=str([round(x, 2) for x in orig[~((orig.ano == 2026) & (orig.turno == 2))].maxdev_vs_B_pp]))])
    est, ep = maxdevD[(2026, 2)]
    pl = [(f"{a}/T{t}", v[0], v[1]) for (a, t), v in maxdevD.items() if (a, t) != (2026, 2)]
    _pos(out).add("A1-corrigida", "curva de apuracao: desvio maximo contra nulo D (municipios em ordem aleatoria dentro da UF), a partir de 10% das secoes (p.p. do PT)", est, ep, pl,
                  nota="teste de forma; sem conversao em votos; efeito na soma final e zero por construcao")


# ------------------------------------------------------------------------------------------------------- A2
BINS = [0, .1, .2, .4, .8, 1e9]


def _std_lider(D, ano, pesos=None):
    w = _pares(D, ano)
    est = (w.comp >= 0.98 * w.comp_t1) & (w.comp_t1 >= 30)
    lider = "lula" if w.lula_t1.sum() > w.dir_t1.sum() else "dir"; col1 = lider + "_t1"
    x = w[est & (w[col1] >= 30)].copy()
    x["terc1"] = x.nominal_t1 - x.lula_t1 - x.dir_t1
    x["bin"] = pd.cut(x.terc1 / x[col1], BINS, right=False, labels=False)
    x["perda"] = (x[lider] < x[col1]).astype(float)
    g = x.groupby("bin").perda.agg(["sum", "size"]).reindex(range(5)).fillna(0)
    return lider, g


def c2(D, reg, out):
    anos = (2026, 2022, 2018, 2014)
    est = {a: _std_lider(D, a) for a in anos}
    w26 = est[2026][1]["size"] / est[2026][1]["size"].sum()
    rows, std = [], {}
    for a in anos:
        lid, g = est[a]
        p = (g["sum"] / g["size"].replace(0, np.nan)).fillna(0); n = g["size"]
        e = float((w26 * p).sum()); v = float(((w26 ** 2) * p * (1 - p) / n.replace(0, np.nan)).fillna(0).sum())
        std[a] = (100 * e, 100 * np.sqrt(v))
        rows.append(dict(ano=a, lider_do_T1="PT" if lid == "lula" else "oponente", secoes_lider_estaveis=int(n.sum()), pct_bruto=100 * float(g["sum"].sum() / n.sum()), pct_padronizado_pelos_pesos_de_2026=std[a][0], ep=std[a][1]))
    out["c2_corrigido_lider_padronizado"] = pd.DataFrame(rows)
    # demonstracao: o teste original (papel fixo) aplicado ao PT de 2022 tambem acusa excesso
    pt = {}
    for a in anos:
        w = _pares(D, a); e_ = (w.comp >= 0.98 * w.comp_t1) & (w.comp_t1 >= 30)
        p = float(((w.lula < w.lula_t1) & e_).sum() / e_.sum()); pt[a] = (100 * p, 100 * np.sqrt(p * (1 - p) / e_.sum()))
    tmp = Registro()
    tmp.add("demo", "teste original (papel fixo) aplicado ao PT de 2022", pt[2022][0], pt[2022][1], [(f"{a}", *pt[a]) for a in (2026, 2018, 2014)])
    f = tmp.frame().iloc[0]
    out["c2_demonstracao_original"] = pd.DataFrame([dict(alvo="PT em 2022 (lider do T1)", pct_perde_votos=pt[2022][0], placebos_PT_2026_2018_2014=str([round(pt[a][0], 2) for a in (2026, 2018, 2014)]), p_excesso=float(f.p_excesso), veredito_do_teste_original=f.veredito)])
    pl = [(f"{a}", *std[a]) for a in (2022, 2018, 2014)]
    _pos(out).add("A2-corrigida", "lider do 1o turno perde votos absolutos (% das secoes, padronizado pela razao terceiros/lider com pesos de 2026)", std[2026][0], std[2026][1], pl,
                  nota="teste de forma; lideres: 2014 PT, 2018 oponente, 2022 PT, 2026 oponente")


# ------------------------------------------------------------------------------------------------------- A3
def _mun_agregado(D, ano):
    w = par_ano(D, ano, minvalid=1)
    w = w[w.QT_APTOS_t1 > 0]
    w = w.assign(mun=w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str), ap=w.QT_APTOS_t1.astype(float))
    for c_, v in (("pt1", w.lula_t1), ("op1", w.dir_t1), ("te1", w.nominal_t1 - w.lula_t1 - w.dir_t1), ("bn1", w.branco_t1 + w.nulo_t1), ("ab1", w.QT_APTOS_t1 - w.QT_COMPARECIMENTO_t1), ("pt2", w.lula)):
        w[c_] = v
    g = w.groupby("mun")[["ap", "pt1", "op1", "te1", "bn1", "ab1", "pt2"]].sum()
    return g, float(w.dir_t1.sum())


def _taxa(g, idx=None):
    x = g if idx is None else g.iloc[idx]
    X = x[["pt1", "op1", "te1", "bn1", "ab1"]].values / x.ap.values[:, None]; y = x.pt2.values / x.ap.values
    sw = np.sqrt(x.ap.values)
    r = optimize.lsq_linear(X * sw[:, None], y * sw, bounds=(0, 1))
    return r.x


def c3(D, reg, out):
    anos = (2026, 2022, 2018, 2014)
    rng = np.random.default_rng(31)
    res, pt = {}, {}
    for a in anos:
        g, op_votos = _mun_agregado(D, a)
        b0 = _taxa(g)[1]
        bs = np.array([_taxa(g, rng.integers(0, len(g), len(g)))[1] for _ in range(300)])
        res[a] = (float(b0), float(bs.std(ddof=1)), (float(np.quantile(bs, .025)), float(np.quantile(bs, .975))), op_votos)
    out["c3_corrigido_taxa_restrita"] = pd.DataFrame([dict(ano=a, taxa_oponente_para_PT=v[0], ep_bootstrap=v[1], ic95_inf=v[2][0], ic95_sup=v[2][1], votos_do_oponente_no_T1=v[3], municipios=len(_mun_agregado(D, a)[0])) for a, v in res.items()])
    # demonstracao: o teste original (coeficiente ecologico sem restricao) acusa exatamente o ano de maior coeficiente em qualquer conjunto de 4 anos
    ce = pd.read_csv(os.path.join(out["_saida"], "A3_a3_ecologica.csv"))
    ce = ce[(ce.destino_T2 == "PT") & (ce.origem_T1 == "OPO_T1")].set_index("ano")
    dem = []
    for a in anos:
        tmp = Registro()
        tmp.add("demo", f"{a}", float(ce.loc[a, "coef"]), float(ce.loc[a, "ep"]), [(str(o), float(ce.loc[o, "coef"]), float(ce.loc[o, "ep"])) for o in anos if o != a])
        f = tmp.frame().iloc[0]
        dem.append(dict(ano_alvo=a, coef_ecologico=float(ce.loc[a, "coef"]), p_excesso=float(f.p_excesso), acusado_pelo_teste_original=bool(f.p_excesso < 0.05)))
    out["c3_demonstracao_original"] = pd.DataFrame(dem)
    est, ep, ic, ov = res[2026]
    pl = [(str(a), res[a][0], res[a][1]) for a in anos if a != 2026]
    _pos(out).add("A3-corrigida", "taxa de transicao oponente (T1) para PT (T2), restrita a [0,1], por municipio, com bootstrap", est, ep, pl, expo=ov, fator=2.0,
                  nota="teto = 2 x max(0, diferenca + 1,645 ep) x votos do oponente no T1; falacia ecologica")


# ------------------------------------------------------------------------------------------------------- A12
def _zeros(D, ano):
    t1 = D[(ano, 1)].set_index(KEY)[["lula", "dir", "valid2"]].add_suffix("_t1")
    d = D[(ano, 2)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.valid2 >= 1) & (d.SG_UF != "ZZ")].join(t1, on=KEY)
    d = d.assign(n=d.valid2, p_t1=((d.dir_t1 + 0.5) / (d.valid2_t1 + 1)).clip(1e-6, 1 - 1e-6))
    g = d.groupby("uf_local"); C = g["dir"].transform("sum"); V = g.valid2.transform("sum"); k = g["dir"].transform("size")
    d["p_viz"] = (((C - d["dir"]) + 0.5) / ((V - d.valid2) + 1)).where(k >= 3).clip(1e-6, 1 - 1e-6)
    return d


def c12(D, reg, out):
    rows, razao = [], {}
    for a in (2026, 2022, 2018, 2014):
        d = _zeros(D, a); z = d[d.p_viz.notna()]
        P = (1 - z.p_viz) ** z.n; obs = int((z["dir"] == 0).sum()); esp = float(P.sum()); var = float((P * (1 - P)).sum())
        razao[a] = (obs / esp if esp else np.nan, float(np.sqrt(max(obs, 1)) / max(esp, 1e-9)))
        rows.append(dict(ano=a, secoes=len(z), observado=obs, esperado_pelos_vizinhos=esp, razao=obs / esp, z=(obs - esp) / np.sqrt(var), p_excesso_unilateral=float(stats.norm.sf((obs - esp) / np.sqrt(var)))))
    out["c12_corrigido_vizinhos"] = pd.DataFrame(rows)
    # demonstracao: 200 simulacoes SEM manipulacao em 2026 (votos do oponente binomiais com p = vizinhos no proprio T2)
    d = _zeros(D, 2026); z = d[d.p_viz.notna()]
    rng = np.random.default_rng(12); n = z.n.values; pv = z.p_viz.values
    E_t1 = float(((1 - z.p_t1) ** z.n).sum()); E_viz = float(((1 - z.p_viz) ** z.n).sum())
    orig = pd.read_csv(os.path.join(out["_saida"], "A12_a12_esperado_vs_observado.csv"))
    pl = []
    for a in (2022, 2018, 2014):
        r_ = orig[(orig.ano == a) & (orig.candidato_com_zero == "oponente") & (orig.estimador_de_p == "p da propria secao no T1")].iloc[0]
        pl.append((str(a), float(r_.razao), float(np.sqrt(max(int(r_.observado), 1)) / float(r_.esperado))))
    flag, rs = 0, []
    for s in range(200):
        obs = int((rng.binomial(n, pv) == 0).sum()); r = obs / E_t1; rs.append(r)
        tmp = Registro(); tmp.add("demo", "sim", r, np.sqrt(max(obs, 1)) / E_t1, pl); flag += int(tmp.frame().iloc[0].p_excesso < 0.05)
    out["c12_demonstracao_original"] = pd.DataFrame([dict(simulacoes_sem_manipulacao=200, esperado_pelo_estimador_do_T1=E_t1, esperado_verdadeiro_dos_vizinhos=E_viz, razao_media_simulada_pelo_T1=float(np.mean(rs)),
                                                          razoes_dos_placebos=str([round(p[1], 3) for p in pl]), simulacoes_acusadas_pelo_teste_original=flag, pct_acusadas=100 * flag / 200)])
    est, ep = razao[2026]
    pls = [(str(a), *razao[a]) for a in (2022, 2018, 2014)]
    zero_votos = float(d[d["dir"] == 0].lula.sum())
    zero_votos = float(d[d["dir"] == 0].lula.sum()); obs26 = rows[0]["observado"]; esp26 = rows[0]["esperado_pelos_vizinhos"]
    _pos(out).add("A12-corrigida", "secoes com zero voto para o oponente no T2: razao observado/esperado (p dos vizinhos do mesmo local, leave-one-out)", est, ep, pls,
                  expo=zero_votos / max(obs26, 1) * esp26, fator=1.0,
                  nota="teto = votos medios do PT por secao zero x secoes esperadas x max(0, diferenca de razao)")
