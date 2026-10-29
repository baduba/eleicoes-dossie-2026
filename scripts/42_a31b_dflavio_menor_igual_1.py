#!/usr/bin/env python3
"""A31b (Adendo 13): os municipios de 2026 com dF (ganho do oponente entre os turnos) <= +1: fracao esperada sob o deslocamento nacional, perfil, decomposicao, 20 maiores perdas e teto.
Uso: python -I 42_a31b_dflavio_menor_igual_1.py DIR_PARQUET DIR_PARQUET2 DIR_MAPA DIR_SAIDA"""
import importlib.util
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, MARGEM
spec = importlib.util.spec_from_file_location("a31", os.path.join(AQUI, "35_a31_transferencia_municipal.py"))
a31 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a31)

PMIN = a31.PMIN
REGIAO = {**{u: "Norte" for u in "AC AM AP PA RO RR TO".split()}, **{u: "Nordeste" for u in "AL BA CE MA PB PE PI RN SE".split()}, **{u: "Centro-Oeste" for u in "DF GO MS MT".split()},
          **{u: "Sudeste" for u in "ES MG RJ SP".split()}, **{u: "Sul" for u in "PR RS SC".split()}}
PORTES = [(0, 5000, "ate 5 mil"), (5000, 20000, "5 a 20 mil"), (20000, 100000, "20 a 100 mil"), (100000, 10**9, "mais de 100 mil")]
NSORT = 200
SEMENTE = 20261029


def porte(a):
    for lo, hi, n in PORTES:
        if lo <= a < hi:
            return n


def simula_pareado(E26, My, G26, Gy, ano):
    j = E26.merge(My[["SG_UF", "CD_MUNICIPIO", "dF", "OP1"]].rename(columns={"dF": "dF_y", "OP1": "OP1_y"}), on=["SG_UF", "CD_MUNICIPIO"], how="inner")
    j = j[j.OP1_y > 0].copy()
    j["g"] = j.dF_y / j.OP1_y
    j["delta"] = j.SG_UF.map(G26) - j.SG_UF.map(Gy)
    j["dFp"] = (j.g + j.delta) * j.OP1
    j["gUF26"] = j.SG_UF.map(G26)
    return j


def teto_A(df, dfcol):
    m = df[dfcol] <= 1
    return 2.0 * float(np.maximum(0, df.gUF26[m] * df.OP1[m] - df[dfcol][m]).sum())


def main(pq, pq2, dmapa, saida):
    os.makedirs(saida, exist_ok=True)
    M = {a: a31.agrega(pq, a) for a in (2026, 2022, 2018, 2014)}
    mapa = pd.read_csv(os.path.join(dmapa, "A20_mapa_tse_ibge.csv"), dtype=str); mapa["CD_MUNICIPIO"] = mapa.CD_MUNICIPIO.astype(int)
    nome = {(r.SG_UF, r.CD_MUNICIPIO): r.NM_MUNICIPIO for r in mapa.itertuples()}
    E = {a: M[a][M[a].P >= PMIN].copy() for a in M}
    E26 = E[2026].copy()
    obs = E26[E26.dF <= 1]
    frac_obs = len(obs) / len(E26)
    G = {a: E[a].groupby("SG_UF").apply(lambda g: g.dF.sum() / g.OP1.sum()) for a in M}
    G26 = G[2026]
    # 1. simulacao
    sim, ts = [], []
    rng = np.random.default_rng(SEMENTE)
    for y in (2022, 2018, 2014):
        j = simula_pareado(E26, M[y], G26, G[y], y)
        fr = float((j.dFp <= 1).mean())
        Ap = teto_A(j, "dFp")
        # reamostragem dentro da UF
        g_uf = {u: (g.dF / g.OP1.where(g.OP1 > 0)).dropna().values for u, g in M[y].groupby("SG_UF")}
        fr_s, A_s = [], []
        for _ in range(NSORT):
            dFs = np.empty(len(E26))
            for u in E26.SG_UF.unique():
                ix = np.where(E26.SG_UF.values == u)[0]
                dFs[ix] = (rng.choice(g_uf[u], size=len(ix)) + (G26[u] - G[y][u])) * E26.OP1.values[ix]
            tmp = E26[["SG_UF", "OP1"]].copy(); tmp["gUF26"] = tmp.SG_UF.map(G26); tmp["dFs"] = dFs
            fr_s.append(float((dFs <= 1).mean())); A_s.append(teto_A(tmp, "dFs"))
        sim.append(dict(ano_de_comparacao=y, municipios_pareados=len(j), fracao_observada_2026=frac_obs, fracao_esperada_pareada=fr, fracao_esperada_reamostragem_media=float(np.mean(fr_s)),
                        reamostragem_p025=float(np.percentile(fr_s, 2.5)), reamostragem_p975=float(np.percentile(fr_s, 97.5)), teto_A_pareado_simulado=Ap, teto_A_reamostragem_media=float(np.mean(A_s)),
                        fracao_sem_deslocamento_nos_dados_do_ano=float((E[y].dF <= 1).mean())))
    SIM = pd.DataFrame(sim); SIM.to_csv(os.path.join(saida, "A31b_simulacao.csv"), index=False)
    lo, hi = SIM.fracao_esperada_pareada.min(), SIM.fracao_esperada_pareada.max()
    inside = bool(((frac_obs >= lo) & (frac_obs <= hi)) or ((SIM.reamostragem_p025 <= frac_obs) & (frac_obs <= SIM.reamostragem_p975)).any())
    veredito = "COMPATIVEL COM O DESLOCAMENTO NACIONAL" if inside else ("ACIMA DO ESPERADO" if frac_obs > max(hi, SIM.reamostragem_p975.max()) else "ABAIXO DO ESPERADO")
    # 2. perfil
    b = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet"), columns=KEY + ["DS_TIPO_URNA", "QT_COMPARECIMENTO", "biom_nh"])
    b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA") & (b.SG_UF != "ZZ")]
    man = b.groupby(["SG_UF", "CD_MUNICIPIO"]).apply(lambda g: g.biom_nh.sum() / g.QT_COMPARECIMENTO.sum()).rename("manual_t2").reset_index()
    mu = pd.read_parquet(os.path.join(pq, "modelo_urna_2026.parquet")); mu = mu[(mu.NR_TURNO == 2) & (mu.SG_UF != "ZZ")]
    mod = pd.crosstab([mu.SG_UF, mu.CD_MUNICIPIO], mu.CD_MODELO_URNA, normalize="index").add_prefix("urna_").reset_index()
    P = E26.merge(man, on=["SG_UF", "CD_MUNICIPIO"], how="left").merge(mod, on=["SG_UF", "CD_MUNICIPIO"], how="left")
    P["regiao"] = P.SG_UF.map(REGIAO); P["porte"] = P.APT1.map(porte)
    P["fatia_oponente_t1"] = P.OP1 / P.COMP1; P["fatia_terceiros_t1"] = P.T1terc / P.COMP1; P["fatia_pt_t1"] = P.PT1 / P.COMP1; P["var_comparecimento_pct"] = 100 * P.dC / P.COMP1
    P["grupo"] = np.where(P.dF <= 1, "dF <= 1", "demais")
    cat = []
    for col in ("regiao", "porte", "SG_UF"):
        t = P.groupby([col, "grupo"]).size().unstack(fill_value=0)
        t["pct_do_grupo"] = 100 * t["dF <= 1"] / t["dF <= 1"].sum(); t["pct_dos_demais"] = 100 * t["demais"] / t["demais"].sum(); t["razao"] = t.pct_do_grupo / t.pct_dos_demais
        t["pct_dos_municipios_da_categoria_com_dF_menor_igual_1"] = 100 * t["dF <= 1"] / (t["dF <= 1"] + t["demais"])
        t = t.reset_index().rename(columns={col: "categoria"}); t.insert(0, "variavel", col); cat.append(t)
    pd.concat(cat).to_csv(os.path.join(saida, "A31b_perfil_categorias.csv"), index=False)
    cont = []
    urnas = [c for c in P.columns if c.startswith("urna_")]
    for col in ["fatia_oponente_t1", "fatia_terceiros_t1", "fatia_pt_t1", "var_comparecimento_pct", "manual_t2", "APT1"] + urnas:
        g1, g0 = P[P.grupo == "dF <= 1"][col], P[P.grupo == "demais"][col]
        cont.append(dict(variavel=col, mediana_dF_menor_igual_1=g1.median(), mediana_demais=g0.median(), media_dF_menor_igual_1=g1.mean(), media_demais=g0.mean()))
    pd.DataFrame(cont).to_csv(os.path.join(saida, "A31b_perfil_continuas.csv"), index=False)
    # 3. decomposicao
    O = P[P.dF <= 1].copy()
    O["S_min"] = np.maximum(0, -O.dF - np.maximum(0, -O.dC) - np.maximum(0, O.BN2 - O.BN1))
    dec = pd.DataFrame([
        dict(grupo="comparecimento caiu (dC < 0)", municipios=int((O.dC < 0).sum()), pct=100 * float((O.dC < 0).mean()), perda_liquida_do_oponente_votos=int(-O.dF[(O.dC < 0) & (O.dF < 0)].sum()), dC_soma=int(O.dC[O.dC < 0].sum())),
        dict(grupo="comparecimento subiu ou igual (dC >= 0)", municipios=int((O.dC >= 0).sum()), pct=100 * float((O.dC >= 0).mean()), perda_liquida_do_oponente_votos=int(-O.dF[(O.dC >= 0) & (O.dF < 0)].sum()), dC_soma=int(O.dC[O.dC >= 0].sum())),
        dict(grupo="limite inferior de troca de voto por balanco liquido > 0", municipios=int((O.S_min > 0).sum()), pct=100 * float((O.S_min > 0).mean()), perda_liquida_do_oponente_votos=int(O.S_min.sum()), dC_soma=np.nan)])
    dec.to_csv(os.path.join(saida, "A31b_decomposicao.csv"), index=False)
    extra = dict(municipios_dF_menor_igual_1=len(O), dF_negativo=int((O.dF < 0).sum()), dF_entre_0_e_1=int(((O.dF >= 0) & (O.dF <= 1)).sum()), dF_menor_ou_igual_menos_1=int((O.dF <= -1).sum()), soma_dF=int(O.dF.sum()), soma_dL=int(O.dL.sum()), soma_dC=int(O.dC.sum()),
                 votos_oponente_t1_nos_municipios=int(O.OP1.sum()), fracao_observada=frac_obs, veredito_simulacao=veredito, G26_nacional=float(E26.dF.sum() / E26.OP1.sum()))
    # 5. teto
    A_obs = teto_A(O.assign(gUF26=O.SG_UF.map(G26)), "dF")
    A_sim = float(SIM.teto_A_pareado_simulado.mean()); B = max(0.0, A_obs - A_sim)
    extra.update(teto_A_votos_margem=A_obs, teto_A_pct=100 * A_obs / MARGEM, A_esperado_pelo_deslocamento_pareado_media=A_sim, teto_B_votos_margem=B, teto_B_pct=100 * B / MARGEM)
    pd.DataFrame([extra]).to_csv(os.path.join(saida, "A31b_resumo.csv"), index=False)
    # 4. 20 maiores perdas
    A26 = M[2026]
    top = A26[A26.COMP1 >= 1000].sort_values("dF").head(20).copy()
    top["nome"] = [nome.get((u, c), "?") for u, c in zip(top.SG_UF, top.CD_MUNICIPIO)]
    top["fatia_oponente_t1_pct"] = 100 * top.OP1 / top.COMP1
    top[["SG_UF", "CD_MUNICIPIO", "nome", "COMP1", "OP1", "OP2", "dF", "PT1", "PT2", "dL", "dC", "T1terc", "BN1", "BN2", "fatia_oponente_t1_pct"]].to_csv(os.path.join(saida, "A31b_20_maiores_perdas.csv"), index=False)
    cs = pd.read_parquet(os.path.join(pq2, "cand_t1_2026.parquet")).set_index(KEY)
    vc = [c for c in cs.columns if c.startswith("v")]
    partes = []
    for r in top.itertuples():
        ss = a31.secoes_mun(pq, 2026, r.SG_UF, r.CD_MUNICIPIO)
        ss = ss.join(cs[vc], how="left")
        ss = ss.rename(columns={"QT_APTOS1": "aptos_T1", "QT_COMPARECIMENTO1": "comparecimento_T1", "lula1": "lula_T1", "dir1": "flavio_T1", "branco1": "brancos_T1", "nulo1": "nulos_T1", "QT_APTOS2": "aptos_T2",
                                "QT_COMPARECIMENTO2": "comparecimento_T2", "lula2": "lula_T2", "dir2": "flavio_T2", "branco2": "brancos_T2", "nulo2": "nulos_T2"})
        ss["terceiros_T1"] = ss.nominal1 - ss.lula_T1 - ss.flavio_T1
        ss["dL"], ss["dF"], ss["dC"] = ss.lula_T2 - ss.lula_T1, ss.flavio_T2 - ss.flavio_T1, ss.comparecimento_T2 - ss.comparecimento_T1
        ss = ss.reset_index(); ss.insert(4, "municipio", r.nome)
        partes.append(ss)
    S = pd.concat(partes, ignore_index=True)
    for c in ("T1", "T2"):
        for k in ("aptos", "comparecimento", "lula", "flavio", "brancos", "nulos"):
            S[f"impresso_{k}_{c}"] = ""
    ordem = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "municipio", "aptos_T1", "comparecimento_T1", "lula_T1", "flavio_T1", "terceiros_T1"] + [c for c in S.columns if c.startswith("v") and c[1:].isdigit()] + \
            ["brancos_T1", "nulos_T1", "aptos_T2", "comparecimento_T2", "lula_T2", "flavio_T2", "brancos_T2", "nulos_T2", "dL", "dF", "dC"] + [c for c in S.columns if c.startswith("impresso_")]
    S[ordem].to_csv(os.path.join(saida, "A31b_20_secoes.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(SIM.round(4).T.to_string()); print(pd.DataFrame([extra]).T.to_string()); print(dec.to_string()); print(pd.concat(cat).round(2).to_string()); print(pd.DataFrame(cont).round(3).to_string())
    print(top[["SG_UF", "nome", "COMP1", "OP1", "dF", "dL", "dC"]].to_string()); print(len(S), "secoes")


if __name__ == "__main__":
    main(*sys.argv[1:5])
