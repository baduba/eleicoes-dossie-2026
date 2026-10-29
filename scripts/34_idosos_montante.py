#!/usr/bin/env python3
"""A20b-idosos, item 2 do pedido de 29/10/2026 (exploratorio, Adendo 9e): quantos eleitores de cada faixa etaria votaram em 2018, 2022 (fim do governo anterior) e 2026,
e o teto em votos de margem do teste de monotonicidade de coortes (votantes 95+ sobre aptos 90+ quatro anos antes).
Uso: python -I 34_idosos_montante.py DIR_PARQUET2 DIR_FASE3 DIR_SAIDA"""
import importlib.util
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import MARGEM, Z95, votos_max

spec = importlib.util.spec_from_file_location("a20b", os.path.join(AQUI, "31_a20b_idosos.py"))
a20b = importlib.util.module_from_spec(spec); spec.loader.exec_module(a20b)

GRUPOS = {"60 a 69 anos (voto obrigatorio)": ["60 a 64 anos", "65 a 69 anos"], "70 a 79 anos": ["70 a 74 anos", "75 a 79 anos"], "80 a 89 anos": ["80 a 84 anos", "85 a 89 anos"],
          "90 a 94 anos": ["90 a 94 anos"], "95 a 99 anos": ["95 a 99 anos"], "100 anos ou mais": ["100 anos ou mais"]}


def main(pq2, f3, saida):
    os.makedirs(saida, exist_ok=True)
    linhas = []
    for ano, turno in ((2018, 1), (2018, 2), (2022, 1), (2022, 2), (2026, 1)):
        p = pd.read_parquet(os.path.join(pq2, f"perfil_agg_{ano}.parquet"))
        p = p[(p.NR_TURNO == turno) & (p.SG_UF != "ZZ")].copy(); p["faixa"] = p.DS_FAIXA_ETARIA.str.strip()
        for nome, fx in GRUPOS.items():
            q = p[p.faixa.isin(fx)]
            linhas.append(dict(ano=ano, turno=turno, grupo=nome, aptos=int(q.QT_APTOS.sum()), votantes=int(q.QT_COMPARECIMENTO.sum()), comparecimento_pct=100 * q.QT_COMPARECIMENTO.sum() / q.QT_APTOS.sum()))
        for nome, fx in (("70 anos ou mais", GRUPOS["70 a 79 anos"] + GRUPOS["80 a 89 anos"] + ["90 a 94 anos", "95 a 99 anos", "100 anos ou mais"]), ("95 anos ou mais", ["95 a 99 anos", "100 anos ou mais"]), ("90 anos ou mais", ["90 a 94 anos", "95 a 99 anos", "100 anos ou mais"])):
            q = p[p.faixa.isin(fx)]
            linhas.append(dict(ano=ano, turno=turno, grupo=nome, aptos=int(q.QT_APTOS.sum()), votantes=int(q.QT_COMPARECIMENTO.sum()), comparecimento_pct=100 * q.QT_COMPARECIMENTO.sum() / q.QT_APTOS.sum()))
        linhas.append(dict(ano=ano, turno=turno, grupo="todos os eleitores", aptos=int(p.QT_APTOS.sum()), votantes=int(p.QT_COMPARECIMENTO.sum()), comparecimento_pct=100 * p.QT_COMPARECIMENTO.sum() / p.QT_APTOS.sum()))
    T = pd.DataFrame(linhas)
    T["votantes_pct_margem"] = 100 * T.votantes / MARGEM
    T.to_csv(os.path.join(saida, "A20b_montante_votantes_por_faixa.csv"), index=False)

    # teto do teste 95+ (votantes 2026 / aptos 90+ em 2022): diferenca de razao x denominador, fator 1 (um voto a mais muda a margem em 1)
    m = pd.read_csv(os.path.join(f3, "A20b_2a_monotonicidade.csv"))
    r = m[(m.banda.str.startswith("95+")) & (m.medida == "votantes")].set_index("par")
    R6, s6, R2, s2 = r.loc["2026 contra 2022", "R_nacional"], r.loc["2026 contra 2022", "ep_R"], r.loc["2022 contra 2018", "R_nacional"], r.loc["2022 contra 2018", "ep_R"]
    perf = {a: a20b.perfil_mun(pq2, a, 1) for a in (2022, 2026)}
    d = perf[2026][["SG_UF", "CD_MUNICIPIO", "comp95"]].merge(perf[2022][["SG_UF", "CD_MUNICIPIO", "apt90"]], on=["SG_UF", "CD_MUNICIPIO"]); d = d[d.apt90 >= 10]
    den = float(d.apt90.sum()); num = float(d.comp95.sum())
    diff = R6 - R2; sed = float(np.hypot(s6, s2)); z = diff / sed; p1 = float(stats.norm.sf(z))
    central = diff * den; teto = votos_max(diff, sed, den, fator_margem=1.0)
    esp22 = R2 * den
    out = dict(votantes_95mais_2026_T1=int(num), aptos_90mais_2022_T1_denominador=int(den), R_2026=R6, R_2022=R2, diferenca_R=diff, ep_diferenca=sed, z=z, p_unilateral=p1,
               votantes_a_mais_que_pela_razao_de_2022=central, votantes_a_mais_ic95_sup_unilateral=teto, teto_votos_de_margem_pior_caso=teto, teto_pct_margem=100 * teto / MARGEM,
               votantes_esperados_pela_razao_de_2022=esp22, nota="exploratorio (Adendo 9e); fator 1: cada votante a mais, se fosse de um so candidato, muda a margem em 1; teto de pior caso, nao estimativa")
    pd.DataFrame([out]).to_csv(os.path.join(saida, "A20b_95mais_teto.csv"), index=False)
    pd.set_option("display.width", 220)
    print(T[T.grupo.isin(["60 a 69 anos (voto obrigatorio)", "70 anos ou mais", "90 anos ou mais", "95 anos ou mais", "100 anos ou mais", "todos os eleitores"])].round(2).to_string())
    print(pd.DataFrame([out]).T.to_string())


if __name__ == "__main__":
    main(*sys.argv[1:4])
