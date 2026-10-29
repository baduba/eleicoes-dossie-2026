#!/usr/bin/env python3
"""A12b (Adendo 12): das secoes com zero voto para o oponente, quantas tem tambem zero brancos e zero nulos, contra o esperado pela taxa de brancos e nulos das vizinhas.
Uso: python -I 36_a12b_zero_brancos_nulos.py DIR_PARQUET DIR_SAIDA"""
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, MARGEM
from h5_h8 import tipo_local


def pb_cauda(p, k):
    """P(X >= k) para soma de Bernoulli independentes (Poisson-binomial), convolucao exata."""
    dist = np.zeros(len(p) + 1)
    dist[0] = 1.0
    for q in p:
        dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q
        dist[0] *= (1 - q)
    return float(dist[k:].sum())


def prepara(pq, ano, turno):
    d = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{turno}.parquet"), columns=KEY + ["DS_TIPO_URNA", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "valid2", "uf_local"])
    d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")].copy()
    d["bn"] = d.branco + d.nulo
    d["uf_mun"] = d.SG_UF + "_" + d.CD_MUNICIPIO.astype(str)
    return d


def taxas_vizinhas(d):
    """Taxa de brancos+nulos e participacao do oponente nas OUTRAS secoes do mesmo local (fallback: municipio)."""
    out = {}
    for nome, g in (("local", "uf_local"), ("municipio", "uf_mun")):
        s = d.groupby(g).agg(bn=("bn", "sum"), comp=("QT_COMPARECIMENTO", "sum"), op=("dir", "sum"), val=("valid2", "sum"), pt=("lula", "sum"))
        j = d[[g, "bn", "QT_COMPARECIMENTO", "dir", "valid2", "lula"]].join(s.add_suffix("_g"), on=g)
        comp_o = j.comp_g - j.QT_COMPARECIMENTO
        val_o = j.val_g - j.valid2
        out[nome] = pd.DataFrame({"r_bn": (j.bn_g - j.bn) / comp_o.where(comp_o > 0), "s_op": (j.op_g - j["dir"]) / val_o.where(val_o > 0), "s_pt": (j.pt_g - j.lula) / val_o.where(val_o > 0), "comp_viz": comp_o}, index=d.index)
    r = out["local"].copy()
    falta = r.r_bn.isna() | (r.comp_viz < 30)
    r.loc[falta] = out["municipio"].loc[falta]
    r["fonte_taxa"] = np.where(falta, "municipio", "local")
    return r, out["municipio"]


def analisa(d):
    viz, viz_mun = taxas_vizinhas(d)
    d = d.join(viz)
    z = d[d["dir"] == 0].copy()
    z["zero_bn"] = z.bn == 0
    n = z.QT_COMPARECIMENTO
    z["p0"] = np.where(n > 0, (1 - z.r_bn.fillna(0).clip(0, 1)) ** n, 1.0)
    z["p0_mun"] = np.where(n > 0, (1 - viz_mun.loc[z.index, "r_bn"].fillna(0).clip(0, 1)) ** n, 1.0)
    return d, z


def linha(ano, turno, z, rotulo):
    k = int(z.zero_bn.sum())
    return dict(ano=ano, turno=turno, universo=rotulo, secoes_zero_oponente=len(z), tripla_zero_observado=k, esperado_pela_taxa_vizinha=float(z.p0.sum()), p_cauda_superior=pb_cauda(z.p0.values, k) if len(z) else np.nan,
                esperado_taxa_do_municipio=float(z.p0_mun.sum()), p_cauda_superior_municipio=pb_cauda(z.p0_mun.values, k) if len(z) else np.nan, observado_sobre_esperado=k / z.p0.sum() if z.p0.sum() > 0 else np.nan)


def main(pq, saida):
    os.makedirs(saida, exist_ok=True)
    serie, extra = [], {}
    for ano in (2014, 2018, 2022, 2026):
        for turno in (1, 2):
            d, z = analisa(prepara(pq, ano, turno))
            serie.append(linha(ano, turno, z, "todas as apuradas (definicao de A12)"))
            serie.append(linha(ano, turno, z[z.QT_COMPARECIMENTO >= 1], "comparecimento >= 1"))
            serie.append(linha(ano, turno, z[z.QT_COMPARECIMENTO >= 30], "comparecimento >= 30"))
            extra[(ano, turno)] = (d, z)
    S = pd.DataFrame(serie)
    S.to_csv(os.path.join(saida, "A12b_serie.csv"), index=False)

    # unanimes (>= 30 validos) x tripla zero em 2026 T2 e 2022 T2 (contraste com o relatorio original)
    un = []
    for ano in (2026, 2022):
        d = extra[(ano, 2)][0]
        v = d[d.valid2 >= 30]
        for nome, m in (("100% dos validos para o PT", v.lula == v.valid2), ("100% dos validos para o oponente", v["dir"] == v.valid2)):
            un.append(dict(ano=ano, turno=2, conjunto=nome, secoes=int(m.sum()), com_zero_brancos_e_nulos=int((v[m].bn == 0).sum()), pct_com_zero_bn=100 * float((v[m].bn == 0).mean()) if m.sum() else np.nan,
                           mediana_bn_pct_do_comparecimento=100 * float((v[m].bn / v[m].QT_COMPARECIMENTO).median()) if m.sum() else np.nan))
    pd.DataFrame(un).to_csv(os.path.join(saida, "A12b_unanimes_x_zero_bn.csv"), index=False)

    # as 106 de 2026 T2
    d, z = extra[(2026, 2)]
    loc = pd.read_parquet(os.path.join(pq, "locais_2026.parquet"))[KEY + ["NM_LOCAL_VOTACAO"]]
    loc["tipo_local"] = tipo_local(loc.NM_LOCAL_VOTACAO)
    z = z.merge(loc, on=KEY, how="left")
    prev = {}
    for ano, t in ((2026, 1), (2022, 2), (2022, 1)):
        p = prepara(pq, ano, t)[KEY + ["QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo"]]
        p = p.rename(columns={c: f"{c}_{ano}T{t}" for c in ("QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo")})
        z = z.merge(p, on=KEY, how="left")
    z["votos_validos"] = z.lula + z["dir"]
    z["oponente_esperado_pela_vizinhanca"] = z.s_op * z.valid2
    cols = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "tipo_local", "NM_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "zero_bn", "r_bn", "fonte_taxa", "p0", "s_op",
            "oponente_esperado_pela_vizinhanca", "QT_COMPARECIMENTO_2026T1", "lula_2026T1", "dir_2026T1", "branco_2026T1", "nulo_2026T1", "QT_COMPARECIMENTO_2022T2", "lula_2022T2", "dir_2022T2", "branco_2022T2", "nulo_2022T2",
            "lula_2022T1", "dir_2022T1"]
    z[cols].to_csv(os.path.join(saida, "A12b_106_secoes.csv"), index=False, float_format="%.6g")
    res = dict(secoes=len(z), com_zero_brancos_e_nulos=int(z.zero_bn.sum()), com_comparecimento_zero=int((z.QT_COMPARECIMENTO == 0).sum()), votos_lula=int(z.lula.sum()), votos_oponente=int(z["dir"].sum()),
               brancos=int(z.branco.sum()), nulos=int(z.nulo.sum()), comparecimento=int(z.QT_COMPARECIMENTO.sum()), aptos=int(z.QT_APTOS.sum()), mediana_comparecimento=float(z.QT_COMPARECIMENTO.median()),
               mediana_aptos=float(z.QT_APTOS.median()), bn_pct_do_comparecimento=100 * float((z.branco.sum() + z.nulo.sum()) / z.QT_COMPARECIMENTO.sum()),
               teto_a_todos_os_votos_de_lula_invalidos_votos_de_margem=float(z.lula.sum()), teto_a_pct_margem=100 * float(z.lula.sum()) / MARGEM,
               oponente_esperado_vizinhanca=float(z.oponente_esperado_pela_vizinhanca.sum()), teto_b_troca_votos_de_margem=2 * float(z.oponente_esperado_pela_vizinhanca.sum()),
               teto_b_pct_margem=100 * 2 * float(z.oponente_esperado_pela_vizinhanca.sum()) / MARGEM, nota="teto de pior caso, nao estimativa")
    pd.DataFrame([res]).to_csv(os.path.join(saida, "A12b_resumo_106.csv"), index=False)
    por_uf = z.groupby("SG_UF").agg(secoes=("lula", "size"), tripla_zero=("zero_bn", "sum"), votos_lula=("lula", "sum")).reset_index()
    por_uf.to_csv(os.path.join(saida, "A12b_106_por_uf.csv"), index=False)
    por_tipo = z.groupby("tipo_local").agg(secoes=("lula", "size"), tripla_zero=("zero_bn", "sum"), comparecimento_mediano=("QT_COMPARECIMENTO", "median")).reset_index()
    por_tipo.to_csv(os.path.join(saida, "A12b_106_por_tipo.csv"), index=False)
    pd.set_option("display.width", 220)
    print(S.round(3).to_string()); print(pd.DataFrame(un).round(2).to_string()); print(pd.DataFrame([res]).T.to_string()); print(por_uf.to_string()); print(por_tipo.to_string())


if __name__ == "__main__":
    main(*sys.argv[1:3])
