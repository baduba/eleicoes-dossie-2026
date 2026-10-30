#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro) — Investigacao A: empates e margens de +-1 voto, 2026 x 2022.

A) Tamanho dos conjuntos (secoes, validos, votos de margem necessarios para criar o empate artificialmente).
B) Nulo por secao: margem ~ Binomial(n = validos, p = share de Lula estimado pela ZONA, leave-one-out).
   Esperado de secoes com |margem| <= 1 (e distribuicao |margem| 0..10) = soma das probabilidades.
   Observado x esperado nos dois anos; razao 2026/2022 normalizada pelo numero de secoes.
C) Simetria das secoes decididas por 1 voto (teste binomial).
D) Composicao: comparecimento das secoes de empate vs geral.
E) Troca de urna (CESP, NR_URNA_ESPERADA != efetivada) nas secoes de empate/+-1 vs taxa nacional (A6).

Universo: secoes apuradas, Brasil sem exterior (definicao do dossiê). Se a contagem do dono (2.155/1.940
empates; 4.525/3.821 de +-1) nao reproduzir nessa definicao, testa variantes e documenta.
Uso: venv/bin/python scripts/exploratorio/06_empates_margem1.py results/exploratorio
"""
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from scipy import stats

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
MARGEM = 4_430_191


def base(ano):
    d = pd.read_parquet(f"parquet/bu_{ano}_t2.parquet")
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.valid2 > 0)].copy()


def p_zona_loo(d):
    """Share de Lula da zona, leave-one-out, cortado em [0.001, 0.999]."""
    g = d.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])
    sl = g.lula.transform("sum") - d.lula
    sv = g.valid2.transform("sum") - d.valid2
    p = np.where(sv > 0, sl / sv, 0.5)
    return np.clip(p, 0.001, 0.999)


def esperado_leq(d, kmax):
    """Esperado de secoes com |margem| <= kmax, por secao e somado; retorna matriz (secoes x kmax+1) de prob de cada |margem|=m."""
    p = p_zona_loo(d)
    n = d.valid2.to_numpy()
    prob = np.zeros((len(d), kmax + 1))
    for m in range(kmax + 1):
        ks = [(n + s) / 2 for s in (-m, m)] if m > 0 else [n / 2]
        pm = np.zeros(len(d))
        for k in ks:
            ok = (np.abs(k - np.round(k)) < 1e-9)  # k inteiro so quando n e m tem mesma paridade
            pm += np.where(ok, stats.binom.pmf(np.round(k), n, p), 0.0)
        prob[:, m] = pm
    return prob


def cesp_subst(ano):
    """NR_URNA_ESPERADA por secao a partir dos zips CESP (mesma logica de f2_a6_a10._cesp)."""
    rows = []
    for fn in sorted(os.listdir("cesp")):
        if not fn.endswith(".zip"):
            continue
        z = zipfile.ZipFile(os.path.join("cesp", fn))
        for name in z.namelist():
            if not name.lower().endswith(".csv"):
                continue
            try:
                d = pd.read_csv(z.open(name), sep=";", encoding="latin-1",
                                usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_URNA_ESPERADA"], dtype=str)
            except ValueError:
                continue
            rows.append(d)
    d = pd.concat(rows, ignore_index=True)
    for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_URNA_ESPERADA"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d.dropna().astype({"NR_URNA_ESPERADA": int}).drop_duplicates(KEY)


def main(saida):
    os.makedirs(saida, exist_ok=True)
    KMAX = 10
    resumo, dist_linhas, saidas = [], [], {}
    for ano in (2026, 2022):
        d = base(ano)
        d["margem"] = d.lula - d["dir"]
        d["am"] = d.margem.abs()
        emp = d[d.margem == 0]
        um = d[d.am == 1]
        # A) tamanhos
        resumo.append(dict(ano=ano, secoes=len(d), empates=len(emp), validos_nas_secoes_empate=int(emp.valid2.sum()),
                           votos_a_mover_para_criar_cada_empate="ceil((|margem|)/2)+1 votos movidos viram empate; soma minima = 1 voto por secao de +-1",
                           decididas_por_1=int(len(um)), validos_nas_secoes_1=int(um.valid2.sum()),
                           lula_mais1=int((um.margem == 1).sum()), opo_mais1=int((um.margem == -1).sum())))
        # B) nulo
        prob = esperado_leq(d, KMAX)
        esp = prob.sum(axis=0)
        obs = [(d.am == m).sum() for m in range(KMAX + 1)]
        for m in range(KMAX + 1):
            z = (obs[m] - esp[m]) / np.sqrt(esp[m] * (1 - esp[m] / len(d)) + 1e-9)
            dist_linhas.append(dict(ano=ano, margem_abs=m, observado=int(obs[m]), esperado_nulo=round(float(esp[m]), 1),
                                    razao_obs_esp=round(obs[m] / esp[m], 3) if esp[m] > 0 else None, z_aprox=round(float(z), 2)))
        esp_emp, esp_um = esp[0], esp[1]
        resumo[-1].update(empates_esperados_nulo=round(float(esp_emp), 1), razao_empate_obs_esp=round(len(emp) / esp_emp, 3),
                          um_esperado_nulo=round(float(esp_um), 1), razao_um_obs_esp=len(um) / esp_um if esp_um else None)
        # C) simetria
        n1, k1 = len(um), int((um.margem == 1).sum())
        resumo[-1]["p_simetria_binomial"] = round(float(stats.binomtest(k1, n1, 0.5).pvalue), 4)
        # D) composicao
        resumo[-1].update(mediana_comparecimento_empate=float(emp.QT_COMPARECIMENTO.median()),
                          mediana_comparecimento_geral=float(d.QT_COMPARECIMENTO.median()),
                          mediana_comparecimento_1voto=float(um.QT_COMPARECIMENTO.median()))
        saidas[ano] = d
    r = pd.DataFrame(resumo)
    r["razao_empates_2026_2022_por_secao"] = None
    pd.DataFrame(dist_linhas).to_csv(os.path.join(saida, "A_distribuicao_margem_obs_esp.csv"), index=False)
    # razao normalizada por crescimento de secoes
    e26, e22 = resumo[0], resumo[1]
    r.loc[0, "razao_empates_2026_2022_por_secao"] = round((e26["empates"] / e26["secoes"]) / (e22["empates"] / e22["secoes"]), 3)
    r.loc[1, "razao_empates_2026_2022_por_secao"] = round((e26["decididas_por_1"] / e26["secoes"]) / (e22["decididas_por_1"] / e22["secoes"]), 3)
    r.to_csv(os.path.join(saida, "A_empates_resumo.csv"), index=False)

    # E) troca de urna (CESP) nas secoes de empate/+-1, 2026 e 2022
    # NOTA: o cruzamento CESP x BWeb reproduz A6 em 2026 (0,606% ~= 0,60%), mas em 2022 da ~95% de
    # "substituicao" — incompativel com o 1,72% de A6: a numeracao de urna do CESP-2022 nao casa com a do
    # BWeb-2022 nesta juncao rapida. So 2026 e reportado; para 2022 vale o numero de A6.
    lin = []
    for ano in (2026,):
        d = saidas[ano]
        ce = cesp_subst(ano)
        w = d.merge(ce, on=KEY, how="left")
        w["subst"] = (w.NR_URNA_ESPERADA.astype("Int64") != w.NR_URNA.astype("Int64")) & w.NR_URNA_ESPERADA.notna()
        for nome, m in [("empate", w.margem == 0), ("margem1", w.am == 1), ("todas", w.am >= 0)]:
            g = w[m]
            lin.append(dict(ano=ano, conjunto=nome, secoes=len(g), com_subst=int(g.subst.sum()),
                            pct_subst=round(100 * g.subst.mean(), 3)))
    pd.DataFrame(lin).to_csv(os.path.join(saida, "A_empates_troca_urna.csv"), index=False)
    print(r.to_string(index=False))
    print(pd.DataFrame(dist_linhas).to_string(index=False))
    print(pd.DataFrame(lin).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
