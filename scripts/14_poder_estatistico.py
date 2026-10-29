#!/usr/bin/env python3
"""Tabelas de poder estatistico (calculo fechado, sem dado de urna) para A18 (boletins impressos) e A19 (teste de integridade).
Uso: python -I 14_poder_estatistico.py BU_2026_T1.parquet DIR_SAIDA
Premissas: N = 499.248 secoes (urnas de votacao); amostra sem reposicao (hipergeometrica); K = ceil(f x N) secoes alteradas."""
import math
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import hypergeom

N = 499_248
MARGEM = 4_430_191


def n_necessario(f, p, N=N):
    """Menor n tal que P(ao menos 1 alterada na amostra) >= p."""
    K = math.ceil(f * N)
    lo, hi = 1, N
    while lo < hi:
        m = (lo + hi) // 2
        if hypergeom.pmf(0, N, K, m) <= 1 - p:
            hi = m
        else:
            lo = m + 1
    return lo


def prob(n, f, N=N):
    return float(hypergeom.sf(0, N, math.ceil(f * N), n))


def regra_art58(secoes_por_uf):
    """Res. TSE 23.673/2021, art. 58 (conforme relatorios de auditoria dos TREs): urnas no teste de integridade por UF."""
    return {uf: (20 if n <= 15_000 else 27 if n <= 30_000 else 33) for uf, n in secoes_por_uf.items()}


def main(bu, saida):
    os.makedirs(saida, exist_ok=True)
    # --- A18: boletins impressos
    fr = [0.001, 0.01, 0.02, 0.05, 0.09]
    a = pd.DataFrame([dict(fracao_alterada=f"{100*f:g}%", secoes_alteradas=math.ceil(f * N), n_para_95=n_necessario(f, .95), n_para_99=n_necessario(f, .99)) for f in fr])
    a.to_csv(os.path.join(saida, "poder_bu_impresso.csv"), index=False)
    # n: com K secoes alteradas, nao ha sorteio que ajude se f for menor do que 1/N; a tabela vale para amostra aleatoria simples de BUs (fotos nao aleatorias reduzem o poder)
    rows = []
    for k in (5, 50, 200):
        s = math.ceil(math.ceil((MARGEM + 1) / 2) / k)         # cada troca de 1 voto muda a margem em 2; precisa reduzir a margem a menos de zero
        rows.append(dict(trocas_por_secao=k, secoes_necessarias_para_inverter_a_margem=s, pct_das_secoes=100 * s / N,
                         n_para_95=n_necessario(s / N, .95), n_para_99=n_necessario(s / N, .99)))
    pd.DataFrame(rows).to_csv(os.path.join(saida, "secoes_para_inverter_margem.csv"), index=False)
    # --- A19: teste de integridade
    d = pd.read_parquet(bu, columns=["SG_UF"])
    s = d[d.SG_UF != "ZZ"].groupby("SG_UF").size()
    reg = regra_art58(s.to_dict())
    uf = pd.DataFrame(dict(UF=s.index, secoes_apuradas_bweb_2026=s.values, urnas_no_teste_de_integridade_pela_regra=[reg[u] for u in s.index])).sort_values("UF")
    uf.to_csv(os.path.join(saida, "teste_integridade_por_uf_regra.csv"), index=False)
    tot = int(uf.urnas_no_teste_de_integridade_pela_regra.sum())
    bio_lo, bio_hi = round(0.05 * tot), round(0.10 * tot)
    fr2 = [0.001, 0.005, 0.01, 0.02, 0.05, 0.09]
    rows = []
    for f in fr2:
        rows.append({"fracao_de_urnas_alteradas": f"{100*f:g}%", f"(a) n={tot} (todo o teste)": prob(tot, f), f"(b) n={bio_hi} (so biometria, 10%)": prob(bio_hi, f), f"(b) n={bio_lo} (so biometria, 5%)": prob(bio_lo, f)})
    pd.DataFrame(rows).to_csv(os.path.join(saida, "poder_teste_integridade.csv"), index=False)
    pd.DataFrame([dict(total_teste_integridade_pela_regra=tot, biometria_5pct=bio_lo, biometria_10pct=bio_hi, urnas_de_votacao=N)]).to_csv(os.path.join(saida, "poder_teste_integridade_premissas.csv"), index=False)
    print(a.to_string(), "\n", pd.DataFrame(rows).round(4).to_string(), "\n", tot, bio_lo, bio_hi)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
