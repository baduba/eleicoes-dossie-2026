#!/usr/bin/env python3
"""A35 (Adendo 17): extremos no universo geral de secoes: E1 zero brancos+nulos em secao grande, E2 comparecimento de 100% dos aptos, E3 100% dos votos nominais em um candidato.
Esperado de E1 = o mesmo estimador de A12b (taxa de brancos+nulos das outras secoes do local, fallback municipio), agora para todas as secoes; cauda de Poisson-binomial por convolucao
de binomiais em faixas de p (DFT; aproximacao declarada). Erro padrao por bootstrap de municipios (1.000, semente 20261029).
Uso: python -I 46_a35_extremos_universo.py DIR_PARQUET DIR_MAPA DIR_SAIDA"""
import importlib.util
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, MARGEM
from h5_h8 import tipo_local

spec = importlib.util.spec_from_file_location("a12b", os.path.join(AQUI, "36_a12b_zero_brancos_nulos.py"))
a12b = importlib.util.module_from_spec(spec); spec.loader.exec_module(a12b)

SEMENTE = 20261029
NBOOT = 1000
LIMS = (100, 200, 400)
PLACEBOS = ((2014, 2), (2018, 2), (2022, 2), (2026, 1))
ALVO = (2026, 2)


def pb_cauda(p, k):
    """P(X >= k), Poisson-binomial: p agrupado em 1.500 faixas de mesma contagem, produto das funcoes caracteristicas, DFT."""
    p = np.sort(np.asarray(p, float)); p = p[p > 1e-12]
    if len(p) == 0:
        return 1.0 if k <= 0 else 0.0
    mu, var = p.sum(), (p * (1 - p)).sum()
    if k > mu + 12 * np.sqrt(var) + 60:
        return 0.0
    nb = min(1500, len(p)); idx = np.array_split(np.arange(len(p)), nb)
    pm = np.array([p[i].mean() for i in idx]); m = np.array([len(i) for i in idx])
    M = int(mu + 12 * np.sqrt(var) + 60)
    w = 2 * np.pi * np.arange(M + 1) / (M + 1)
    lg = np.zeros(M + 1, complex)
    for pj, mj in zip(pm, m):
        lg += mj * np.log(1 - pj + pj * np.exp(1j * w))
    pmf = np.real(np.fft.fft(np.exp(lg)) / (M + 1))
    pmf = np.clip(pmf, 0, None); pmf /= pmf.sum()
    return float(pmf[k:].sum()) if k <= M else 0.0


def prepara(pq, ano, turno):
    d = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{turno}.parquet"), columns=KEY + ["DS_TIPO_URNA", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "nominal", "branco", "nulo", "valid2", "uf_local"])
    d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ")].copy()
    d["bn"] = d.branco + d.nulo
    d["uf_mun"] = d.SG_UF + "_" + d.CD_MUNICIPIO.astype(str)
    viz, _ = a12b.taxas_vizinhas(d)
    d = d.join(viz)
    # comparecimento das outras secoes do local (fallback municipio)
    for nome, g in (("local", "uf_local"), ("mun", "uf_mun")):
        a = d.groupby(g).QT_APTOS.transform("sum") - d.QT_APTOS; c = d.groupby(g).QT_COMPARECIMENTO.transform("sum") - d.QT_COMPARECIMENTO
        d[f"t_{nome}"] = (c / a.where(a > 0)); d[f"med_{nome}"] = d.groupby(g).QT_COMPARECIMENTO.transform("median")
    ok = d.t_local.notna() & (d.groupby("uf_local").QT_APTOS.transform("size") > 1)
    d["t_viz"] = np.where(ok, d.t_local, d.t_mun).clip(0, 1); d["med_viz"] = np.where(ok, d.med_local, d.med_mun)
    return d


def e1(d, lim):
    x = d[d.QT_COMPARECIMENTO >= lim]
    p0 = (1 - x.r_bn.fillna(0).clip(0, 1)) ** x.QT_COMPARECIMENTO
    flag = x.bn == 0
    return x, p0, flag


def boot(mun, obs, exp, rng):
    """Erro padrao de obs/exp por bootstrap de municipios."""
    g = pd.DataFrame({"m": mun.values, "o": obs, "e": exp}).groupby("m").sum()
    O, E = g.o.values, g.e.values; n = len(g)
    r = np.empty(NBOOT)
    for b in range(NBOOT):
        i = rng.integers(0, n, n); r[b] = O[i].sum() / max(E[i].sum(), 1e-12)
    return float(r.std(ddof=1))


def main(pq, dmapa, saida):
    os.makedirs(saida, exist_ok=True)
    rng = np.random.default_rng(SEMENTE)
    D = {k: prepara(pq, *k) for k in set(PLACEBOS) | {ALVO}}
    # ---- E1
    linhas = []
    for (ano, t), d in sorted(D.items()):
        for lim in LIMS:
            x, p0, flag = e1(d, lim)
            k, mu = int(flag.sum()), float(p0.sum())
            linhas.append(dict(ano=ano, turno=t, limiar_comparecimento=lim, secoes_no_universo=len(x), zero_bn_observado=k, esperado=mu, razao=k / mu if mu > 0 else np.nan,
                               ep_bootstrap=boot(x.uf_mun, flag.values.astype(float), p0.values, rng), p_cauda_superior=pb_cauda(p0.values, k)))
    E1 = pd.DataFrame(linhas); E1.to_csv(os.path.join(saida, "A35_E1_serie.csv"), index=False)
    # ---- decisao E1: alvo contra cada placebo
    dec = []
    for lim in LIMS:
        a = E1[(E1.ano == ALVO[0]) & (E1.turno == ALVO[1]) & (E1.limiar_comparecimento == lim)].iloc[0]
        res = {}
        for (ano, t) in PLACEBOS:
            b = E1[(E1.ano == ano) & (E1.turno == t) & (E1.limiar_comparecimento == lim)].iloc[0]
            z = (a.razao - b.razao) / np.sqrt(a.ep_bootstrap ** 2 + b.ep_bootstrap ** 2)
            res[f"{ano}T{t}"] = (b.razao, z, stats.norm.sf(z))
        excesso = all(v[1] > 2 for v in res.values())
        dec.append(dict(limiar_comparecimento=lim, razao_2026T2=a.razao, ep=a.ep_bootstrap, p_cauda_2026T2=a.p_cauda_superior,
                        **{f"razao_{k}": v[0] for k, v in res.items()}, **{f"z_contra_{k}": v[1] for k, v in res.items()}, **{f"p_unilateral_contra_{k}": v[2] for k, v in res.items()},
                        veredito=("EXCESSO" if excesso else "dentro do esperado (nao supera todos os placebos por mais de 2 EP)")))
    DEC = pd.DataFrame(dec)
    # Holm sobre a familia {E1 (limiar principal 100)}: E2 e descritivo e E3 e contagem; o p de E1 e o do pior placebo (maior p)
    pw = DEC.loc[DEC.limiar_comparecimento == 100, [c for c in DEC.columns if c.startswith("p_unilateral_contra")]].max(axis=1).iloc[0]
    DEC["p_holm_familia_E1"] = np.where(DEC.limiar_comparecimento == 100, min(1.0, pw * 1), np.nan)
    DEC.to_csv(os.path.join(saida, "A35_E1_decisao.csv"), index=False)
    # ---- E2 (descritivo) e E3 (contagem)
    l2, l3 = [], []
    for (ano, t), d in sorted(D.items()):
        n, p = d.QT_APTOS.values, d.t_viz.fillna(0).values
        obs = int(((d.QT_COMPARECIMENTO == d.QT_APTOS) & (d.QT_APTOS > 0)).sum()); exp = float((p ** n).sum())
        k995 = np.ceil(0.995 * n)
        obs995 = int(((d.QT_COMPARECIMENTO / d.QT_APTOS.where(d.QT_APTOS > 0)) >= 0.995).sum()); exp995 = float(stats.binom.sf(k995 - 1, n, p).sum())
        big = d.QT_APTOS >= 100
        l2.append(dict(ano=ano, turno=t, secoes=len(d), comparecimento_igual_aptos=obs, esperado=exp, razao=obs / exp if exp > 0 else np.nan, comp_100pc_aptos_100mais=int(((d.QT_COMPARECIMENTO == d.QT_APTOS) & big).sum()),
                       compar_995_ou_mais=obs995, esperado_995=exp995, razao_995=obs995 / exp995 if exp995 > 0 else np.nan, **{"nota": "descritivo: abstencao nao e independente; sem p"}))
        for lado, col in (("Lula", "lula"), ("oponente", "dir")):
            m = (d.nominal > 0) & (d.QT_COMPARECIMENTO >= 30) & (d[col] == d.nominal)
            l3.append(dict(ano=ano, turno=t, lado=lado, secoes_100pc_nominais_comparecimento_30mais=int(m.sum()), votos_nessas_secoes=int(d.loc[m, col].sum())))
    pd.DataFrame([dict(ano=a, turno=t, secoes=len(d), taxa_brancos_nulos_pct=100 * float(d.bn.sum() / d.QT_COMPARECIMENTO.sum())) for (a, t), d in sorted(D.items())]).to_csv(os.path.join(saida, "A35_taxa_brancos_nulos.csv"), index=False)
    pd.DataFrame(l2).to_csv(os.path.join(saida, "A35_E2_descritivo.csv"), index=False); pd.DataFrame(l3).to_csv(os.path.join(saida, "A35_E3_contagem.csv"), index=False)
    # ---- teto (2026T2 e 2022T2 lado a lado)
    tt = []
    for (ano, t) in ((2026, 2), (2022, 2)):
        d = D[(ano, t)]
        x, p0, f1 = e1(d, 100); s1 = x[f1]
        e3 = lambda col: d[(d.nominal > 0) & (d.QT_COMPARECIMENTO >= 30) & (d[col] == d.nominal)]
        s3 = pd.concat([e3("lula"), e3("dir")])
        def fator2(s):
            pt = np.maximum(0, (s.lula / s.valid2.where(s.valid2 > 0) - s.s_pt)).fillna(0) * s.valid2 * 2
            op = np.maximum(0, (s["dir"] / s.valid2.where(s.valid2 > 0) - s.s_op)).fillna(0) * s.valid2 * 2
            return float(max(pt.sum(), op.sum()))
        s2 = d[(d.QT_COMPARECIMENTO == d.QT_APTOS) & (d.QT_APTOS > 0)]
        tt.append(dict(ano=ano, turno=t, E1_fator1_votos_do_majoritario=float(s1[["lula", "dir"]].max(axis=1).sum()), E1_fator2_troca_pela_vizinhanca=fator2(s1),
                       E3_fator1=float(s3[["lula", "dir"]].max(axis=1).sum()), E3_fator2=fator2(s3), E2_fator1_comparecimento_acima_da_mediana_do_local=float(np.maximum(0, s2.QT_COMPARECIMENTO - s2.med_viz).sum())))
    T = pd.DataFrame(tt)
    T["maior_teto_2026"] = T.iloc[0, 2:].max() if False else np.nan
    T.to_csv(os.path.join(saida, "A35_teto.csv"), index=False)
    # ---- caracterizacao das E1 sinalizadas (2026T2, limiar principal)
    d = D[ALVO]; x, p0, f1 = e1(d, 100); s = x[f1].copy(); s["p0"] = p0[f1]
    loc = pd.read_parquet(os.path.join(pq, "locais_2026.parquet"))
    loc["tipo_local"] = tipo_local(loc.NM_LOCAL_VOTACAO)
    s = s.merge(loc[KEY + ["tipo_local", "NM_LOCAL_VOTACAO"]].drop_duplicates(KEY), on=KEY, how="left")
    mapa = pd.read_csv(os.path.join(dmapa, "A20_mapa_tse_ibge.csv"), dtype=str); mapa["CD_MUNICIPIO"] = mapa.CD_MUNICIPIO.astype(int)
    s = s.merge(mapa[["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"]], on=["SG_UF", "CD_MUNICIPIO"], how="left")
    for ano, t in ((2022, 2), (2018, 2)):
        h = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{t}.parquet"), columns=KEY + ["QT_APTOS", "QT_COMPARECIMENTO", "branco", "nulo"]).rename(columns={"QT_APTOS": f"aptos_{ano}", "QT_COMPARECIMENTO": f"comparecimento_{ano}", "branco": f"brancos_{ano}", "nulo": f"nulos_{ano}"})
        s = s.merge(h, on=KEY, how="left")
    cols = KEY + ["NM_MUNICIPIO", "tipo_local", "NM_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "r_bn", "p0"] + [c for c in s.columns if c.endswith(("_2022", "_2018"))]
    s[cols].to_csv(os.path.join(saida, "A35_E1_sinalizadas_2026T2.csv"), index=False, float_format="%.5g")
    e2 = D[ALVO][(D[ALVO].QT_COMPARECIMENTO == D[ALVO].QT_APTOS) & (D[ALVO].QT_APTOS > 0)].merge(loc[KEY + ["tipo_local", "NM_LOCAL_VOTACAO"]].drop_duplicates(KEY), on=KEY, how="left").merge(mapa[["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"]], on=["SG_UF", "CD_MUNICIPIO"], how="left")
    e2[KEY + ["NM_MUNICIPIO", "tipo_local", "NM_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "t_viz"]].to_csv(os.path.join(saida, "A35_E2_secoes_2026T2.csv"), index=False, float_format="%.5g")
    pt = s.groupby(["tipo_local"]).size().rename("secoes").reset_index().sort_values("secoes", ascending=False); pt.to_csv(os.path.join(saida, "A35_E1_por_tipo_local.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(E1.round(4).to_string()); print(DEC.round(4).T.to_string()); print(pd.DataFrame(l2).round(3).to_string()); print(pd.DataFrame(l3).to_string()); print(T.round(0).to_string()); print(pt.to_string())


if __name__ == "__main__":
    main(*sys.argv[1:4])
