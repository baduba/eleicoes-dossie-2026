#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro): intersecoes de bandeiras ja medidas, usando so os agregados
versionados em results/ (os parquets por secao nao existem nesta maquina).

Duas escalas:
(a) SECAO (2026/T2): dentro dos conjuntos ja sinalizados (A12 zero-voto, A32 top-50 excesso manual,
    A33 escolas extremas), quantas acumulam 2+ bandeiras e quais bandeiras coexistem no mesmo local.
(b) MUNICIPIO (2026): bandeiras derivadas de A31 (extremo do modelo; dF <= 1), A20 (razao aptos/pop16
    alta), A20b (idosos R > 1), A27 (mais secoes novas >= 95%), A33 (escola extrema), A32 (secao top-50),
    A12 (secao zero-voto). Contagem de bandeiras por municipio e concentracao por UF.

Sem veredito formal: intersecoes sobre conjuntos ja sinalizados NAO sao um teste novo de fraude;
servem para priorizar verificacao documental. Razao de chance: os conjuntos sao parcialmente causais
entre si (ex.: secao pequena gera zero-voto e >= 95%), entao o empilhamento esperado sob ausencia de
fraude NAO e o produto das frequencias marginais - ver memorando.
Uso: venv/bin/python scripts/exploratorio/03_gatilhos_intersecoes.py results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd

R3 = "results/fase3"
R2 = "results/fase2"


def main(saida):
    os.makedirs(saida, exist_ok=True)

    # ---------- (a) nivel secao ----------
    a12 = pd.read_csv(f"{R2}/A12_a12_secoes_zero_2026.csv")
    a12 = a12[a12.turno == 2].copy()
    a12["b_zero_opo"] = a12.quem_zero.eq("oponente")
    a12["b_zero_pt"] = a12.quem_zero.eq("pt") if (a12.quem_zero == "pt").any() else False
    a12["b_manual30"] = a12.manual_rate > 0.30
    a12["b_turnout95"] = a12.QT_COMPARECIMENTO >= 0.95 * a12.QT_APTOS
    a12["b_ue2022"] = a12.CD_MODELO_URNA.astype(str).str.contains("2022")
    a12["b_fechou_tarde"] = pd.to_datetime(a12.DT_ENCERRAMENTO, errors="coerce").dt.hour >= 19
    bcols = ["b_zero_opo", "b_manual30", "b_turnout95", "b_ue2022", "b_fechou_tarde"]
    a12["n_bandeiras"] = a12[bcols].sum(axis=1)
    res_sec = (a12.groupby("n_bandeiras").agg(secoes=("SG_UF", "size"), votos_lula=("lula", "sum"),
                                              comparecimento=("QT_COMPARECIMENTO", "sum")).reset_index())
    res_sec.to_csv(os.path.join(saida, "empilhamento_nas_secoes_zero_voto.csv"), index=False)

    # intersecoes entre conjuntos distintos (mesma chave de secao)
    k = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    a12b = pd.read_csv(f"{R3}/A12b_106_secoes.csv")
    a32 = pd.read_csv(f"{R3}/A32_50_secoes_excesso_2026T2.csv")
    inter = []
    for nome, d1, d2 in [("A12b zero-oponente x A32 top-50 manual", a12b, a32)]:
        j = d1.merge(d2, on=k, how="inner")
        inter.append(dict(intersecao=nome, n=len(j)))
    # A12 x escolas extremas A33 (chave de local)
    a33 = pd.read_csv(f"{R3}/A33_escolas_extremas.csv")
    kl = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA"]
    j = a12.merge(a33, on=kl, how="inner")
    inter.append(dict(intersecao="A12 zero-voto x A33 escola extrema (mesma zona+municipio)", n=len(j)))
    pd.DataFrame(inter).to_csv(os.path.join(saida, "intersecoes_entre_conjuntos_secao.csv"), index=False)

    # ---------- (b) nivel municipio ----------
    a31 = pd.read_csv(f"{R3}/A31_municipios.csv")
    m = a31[a31.ano == 2026].copy()
    m["b_a31_extremo"] = m.p_holm < 0.05
    m["b_a31b_df1"] = m.dF <= 1
    mun = m[["SG_UF", "CD_MUNICIPIO", "nome", "P", "dL", "dF", "dC", "b_a31_extremo", "b_a31b_df1"]].copy()

    def marca(df, col, base_cols=("SG_UF", "CD_MUNICIPIO")):
        s = set(map(tuple, df[list(base_cols)].values))
        mun[col] = [t in s for t in map(tuple, mun[["SG_UF", "CD_MUNICIPIO"]].values)]

    a20 = pd.read_csv(f"{R3}/A20_maiores_razoes_2026.csv")
    mapa = pd.read_csv(f"{R3}/A20_mapa_tse_ibge.csv")
    a20 = a20.merge(mapa[["SG_UF", "NM_MUNICIPIO", "CD_MUNICIPIO"]], on=["SG_UF", "NM_MUNICIPIO"], how="left")
    marca(a20.dropna(subset=["CD_MUNICIPIO"]), "b_a20_razao_alta")
    marca(pd.read_csv(f"{R3}/A20b_2a_lista_municipios_2026.csv"), "b_a20b_idosos")
    marca(pd.read_csv(f"{R3}/A27_maiores_municipios.csv"), "b_a27_secoes_novas95")
    marca(a33[["SG_UF", "CD_MUNICIPIO"]].drop_duplicates(), "b_a33_escola_extrema")
    marca(a32[["SG_UF", "CD_MUNICIPIO"]].drop_duplicates(), "b_a32_top50_manual")
    marca(a12[["SG_UF", "CD_MUNICIPIO"]].drop_duplicates(), "b_a12_secao_zero_voto")

    bmun = [c for c in mun.columns if c.startswith("b_")]
    mun["n_bandeiras"] = mun[bmun].sum(axis=1)
    dist = (mun.groupby("n_bandeiras").agg(municipios=("SG_UF", "size")).reset_index())
    dist.to_csv(os.path.join(saida, "empilhamento_por_municipio_distribuicao.csv"), index=False)
    multi = mun[mun.n_bandeiras >= 2].sort_values(["n_bandeiras", "SG_UF"], ascending=[False, True])
    cols_out = ["SG_UF", "CD_MUNICIPIO", "nome", "n_bandeiras"] + bmun + ["P", "dL", "dF", "dC"]
    multi[cols_out].to_csv(os.path.join(saida, "empilhamento_por_municipio_2mais.csv"), index=False)
    uf = (multi.groupby("SG_UF").agg(municipios_2mais=("SG_UF", "size"),
                                     bandeiras_total=( "n_bandeiras", "sum")).reset_index()
          .sort_values("municipios_2mais", ascending=False))
    tot_mun = mun.groupby("SG_UF").size().rename("municipios_elegiveis")
    uf = uf.merge(tot_mun, on="SG_UF")
    uf["pct"] = (100 * uf.municipios_2mais / uf.municipios_elegiveis).round(2)
    uf.to_csv(os.path.join(saida, "empilhamento_por_uf.csv"), index=False)

    print("== nivel secao (conjunto A12 zero-voto, 2026/T2) ==")
    print(res_sec.to_string(index=False))
    print("\nintersecoes entre conjuntos:", pd.DataFrame(inter).to_dict("records"))
    print("\n== nivel municipio: distribuicao do numero de bandeiras ==")
    print(dist.to_string(index=False))
    print("\nmunicipios com 3+ bandeiras:", (mun.n_bandeiras >= 3).sum())
    print(multi[multi.n_bandeiras >= 3][cols_out].to_string(index=False))
    print("\nconcentracao por UF (municipios com 2+ bandeiras):")
    print(uf.head(12).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
