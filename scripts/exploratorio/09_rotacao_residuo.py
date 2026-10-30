#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro) — Teoria da rotacao (o dono): tecnicas antigas encolhem, novas entram
com jitter, e a SOMA controla o resultado. Nucleo testavel: rotacao preve componentes encolhendo com o
residuo total se mantendo/migrando; estrutura benigna preve o total sumindo junto.

1) RESIDUO TOTAL POR ANO: soma, por ano, dos saldos (votos PT - oponente) medidos em conjuntos ja usados
   como componentes nesta auditoria, todos recomputados dos parquets com o MESMO metodo nos 4 anos:
   (c1) secoes com oponente 0-10 votos; (c2) secoes com PT >= 80% dos validos; (c3) secoes com turnout >= 95%
   (corte de H5); (c4) secoes com taxa sem-biometria > 30% (corte de A32; 2014 sem dado: biom_nh vem zerado);
   (c5) excesso A31 versionado (soma de teto_incond_votos_margem por ano, de results/fase3/A31_municipios.csv).
   c1-c4 se sobrepoem (somam votos das mesmas secoes as vezes); por isso reporto cada um E a soma dos
   conjuntos DISJUNTOS por uniao de secoes (uma secao entra uma vez). Cobertura: identica nos 4 anos para
   c1-c3; c4 so 2018+; c5 usa o teto versionado (metodo A31, nao e saldo bruto) — declarado.
2) GEOGRAFIA DA MARGEM: por ano, Gini da contribuicao municipal |saldo|/|saldo nacional|, top-100 como % do
   saldo absoluto nacional, e Spearman do ranking municipal de saldo/apto entre eleicoes consecutivas.
3) JITTER: sinal da variacao ano-a-ano de cada componente; quantos mudam de sinal vs monotonicos.
Uso: venv/bin/python scripts/exploratorio/09_rotacao_residuo.py results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

NE = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]
ANOS = (2014, 2018, 2022, 2026)
KEYM = ["SG_UF", "CD_MUNICIPIO"]


def base(ano):
    d = pd.read_parquet(f"parquet/bu_{ano}_t2.parquet")
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.valid2 > 0)].copy()


def gini(x):
    x = np.sort(np.abs(np.asarray(x, dtype=float)))
    n = len(x)
    if x.sum() == 0:
        return np.nan
    return float((2 * np.arange(1, n + 1) - n - 1) @ x / (n * x.sum()))


def main(saida):
    os.makedirs(saida, exist_ok=True)
    comp_rows, geo_rows, mun_series = [], [], {}
    for ano in ANOS:
        d = base(ano)
        d["saldo"] = d.lula - d["dir"]
        c = {}
        c["c1_opo_0a10"] = d["dir"] <= 10
        c["c2_dom80"] = d.lula_sh >= 0.80
        c["c3_turnout95"] = d.QT_COMPARECIMENTO >= 0.95 * d.QT_APTOS
        tem_biom = d.biom_nh.sum() > 0
        c["c4_sem_biom_30"] = (d.biom_nh / d.QT_COMPARECIMENTO > 0.30) if tem_biom else pd.Series(False, index=d.index)
        for nome, m in c.items():
            if tem_biom or nome != "c4_sem_biom_30":
                comp_rows.append(dict(ano=ano, componente=nome, secoes=int(m.sum()), saldo=int(d.saldo[m].sum())))
        uniao = c["c1_opo_0a10"] | c["c2_dom80"] | c["c3_turnout95"] | c["c4_sem_biom_30"]
        comp_rows.append(dict(ano=ano, componente="UNIAO c1-c4 (disjunta por secao)", secoes=int(uniao.sum()),
                              saldo=int(d.saldo[uniao].sum())))
        # geografia da margem
        mun = d.groupby(KEYM).agg(saldo=("saldo", "sum"), apt=("QT_APTOS", "sum")).reset_index()
        mun["saldo_pa"] = mun.saldo / mun.apt
        tot = mun.saldo.abs().sum()
        top100 = mun.saldo.abs().nlargest(100).sum()
        geo_rows.append(dict(ano=ano, municipios=len(mun), saldo_nacional=int(d.saldo.sum()),
                             gini_contribuicao_abs=round(gini(mun.saldo), 4),
                             top100_pct_do_saldo_abs=round(100 * top100 / tot, 2),
                             saldo_top100_positivo=int(mun.nlargest(100, "saldo").saldo.sum())))
        mun_series[ano] = mun.set_index(KEYM).saldo_pa
    pd.DataFrame(comp_rows).to_csv(os.path.join(saida, "ROT_componentes_por_ano.csv"), index=False)
    g = pd.DataFrame(geo_rows)
    for a, b in ((2018, 2014), (2022, 2018), (2026, 2022)):
        j = pd.concat([mun_series[a].rename("x"), mun_series[b].rename("y")], axis=1, join="inner")
        g.loc[g.ano == a, "spearman_ranking_vs_anterior"] = round(float(stats.spearmanr(j.x, j.y).statistic), 4)
        g.loc[g.ano == a, "municipios_pareados"] = len(j)
    g.to_csv(os.path.join(saida, "ROT_geografia_margem.csv"), index=False)

    # c5: excesso A31 versionado por ano
    a31 = pd.read_csv("results/fase3/A31_municipios.csv")
    c5 = a31.groupby("ano").teto_incond_votos_margem.sum().round(0)
    # jitter: sinal das variacoes por componente
    comp = pd.DataFrame(comp_rows)
    jit = []
    for nome, grp in comp.groupby("componente"):
        s = grp.set_index("ano").saldo.reindex(ANOS).dropna()
        if len(s) < 3:
            continue
        diffs = np.sign(np.diff(s.values))
        flips = int((diffs[1:] * diffs[:-1] < 0).sum())
        jit.append(dict(componente=nome, anos=len(s), serie=" / ".join(f"{int(v):,}" for v in s.values),
                        sinais_das_variacoes="".join("+" if x > 0 else "-" if x < 0 else "0" for x in diffs),
                        mudancas_de_sinal=flips, monotonico=bool((np.diff(s.values) > 0).all() or (np.diff(s.values) < 0).all())))
    v5 = c5.reindex(ANOS).values
    d5 = np.sign(np.diff(v5))
    jit.append(dict(componente="c5 excesso A31 (teto versionado)", anos=len(c5),
                    serie=" / ".join(f"{int(v):,}" for v in v5),
                    sinais_das_variacoes="".join("+" if x > 0 else "-" if x < 0 else "0" for x in d5),
                    mudancas_de_sinal=int((d5[1:] * d5[:-1] < 0).sum()),
                    monotonico=bool((np.diff(v5) > 0).all() or (np.diff(v5) < 0).all())))
    pd.DataFrame(jit).to_csv(os.path.join(saida, "ROT_jitter.csv"), index=False)
    print(comp.to_string(index=False)); print(g.to_string(index=False)); print(pd.DataFrame(jit).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
