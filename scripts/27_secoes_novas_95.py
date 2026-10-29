#!/usr/bin/env python3
"""A27 (Fase 3): as 427 secoes novas de comparecimento >= 95% no 2o turno de 2026 (639 no total, 427 ausentes em 2022): endereco/tipo do local, porte, historico do local e contribuicao liquida a margem.
Nao executado: origem das transferencias de eleitores (exige o cadastro nominal). Pre-registro: Adendo 8.
Uso: python -I 27_secoes_novas_95.py DIR_PARQUET DIR_SAIDA"""
import os
import re
import sys
import numpy as np
import pandas as pd

K = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
TIPOS = {"prisional": r"PENITENCI|PRESIDI|PRISION|CADEIA|CENTRO DE DETENC|SOCIOEDUCA|UNIDADE PRISIONAL|CDP|PENAL",
         "indigena": r"ALDEIA|INDIGEN|TERRA IND|COMUNIDADE IND|POSTO INDIG",
         "saude_ou_asilo": r"HOSPITAL|ASILO|CASA DE REPOUSO|SANATORIO|CLINICA|LAR DE IDOSOS|UNIDADE DE SAUDE",
         "rural_ou_comunidade": r"FAZENDA|SITIO|ASSENTAMENTO|QUILOMBO|COMUNIDADE|POVOADO|VILA RURAL|RURAL",
         "escola": r"ESCOLA|COLEGIO|E\.?M\.?E\.?F|EMEF|EMEI|CEI |CRECHE|INSTITUTO|UNIVERSIDADE|FACULDADE"}


def tipo(nome, end):
    t = f"{nome} {end}".upper()
    for k, rx in TIPOS.items():
        if re.search(rx, t):
            return k
    return "outro"


def main(pq, saida):
    os.makedirs(saida, exist_ok=True)
    b26 = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet")); b22 = pd.read_parquet(os.path.join(pq, "bu_2022_t2.parquet")); t1 = pd.read_parquet(os.path.join(pq, "bu_2026_t1.parquet"))
    l26 = pd.read_parquet(os.path.join(pq, "locais_2026.parquet")); l22 = pd.read_parquet(os.path.join(pq, "locais_2022.parquet"))
    b = b26[b26.DS_TIPO_URNA.str.upper().eq("APURADA") & (b26.SG_UF != "ZZ") & (b26.QT_APTOS > 0)].copy()
    k22 = set(map(tuple, b22[K].values))
    b["nova"] = [tuple(x) not in k22 for x in b[K].values]
    b["turn"] = b.QT_COMPARECIMENTO / b.QT_APTOS
    b["t95"] = b.turn >= 0.95
    b = b.merge(l26[K + ["NM_LOCAL_VOTACAO", "DS_LOCAL_VOTACAO_ENDERECO"]], on=K, how="left")
    b["tipo_local"] = [tipo(a, c) for a, c in zip(b.NM_LOCAL_VOTACAO.fillna(""), b.DS_LOCAL_VOTACAO_ENDERECO.fillna(""))]
    # historico do local: o local (mesmo municipio e numero de local) existia em 2022? com quantas secoes?
    loc22 = l22.groupby(["SG_UF", "CD_MUNICIPIO", "NR_LOCAL_VOTACAO"]).size().rename("secoes_local_2022").reset_index()
    b = b.merge(loc22, on=["SG_UF", "CD_MUNICIPIO", "NR_LOCAL_VOTACAO"], how="left")
    b["local_ja_existia_em_2022"] = b.secoes_local_2022.notna()
    b["secoes_no_local_2026"] = b.groupby(["SG_UF", "CD_MUNICIPIO", "NR_LOCAL_VOTACAO"]).NR_SECAO.transform("size")
    b = b.merge(t1[K + ["QT_COMPARECIMENTO", "QT_APTOS"]].rename(columns={"QT_COMPARECIMENTO": "comp_t1", "QT_APTOS": "aptos_t1"}), on=K, how="left")
    b["turn_t1"] = b.comp_t1 / b.aptos_t1
    alvo = b[b.t95 & b.nova]
    ref_novas = b[b.nova & ~b.t95]
    ref_antigas95 = b[b.t95 & ~b.nova]
    def res(g, nome):
        return dict(grupo=nome, secoes=len(g), aptos_mediana=float(g.QT_APTOS.median()), pct_local_ja_existia_em_2022=float(100 * g.local_ja_existia_em_2022.mean()), secoes_no_local_mediana=float(g.secoes_no_local_2026.median()),
                    turnout_t1_medio=float(g.turn_t1.mean()), turnout_t2_medio=float(g.turn.mean()), comparecimento=int(g.QT_COMPARECIMENTO.sum()), votos_lula=int(g.lula.sum()), votos_oponente=int(g["dir"].sum()),
                    margem_liquida_lula_menos_oponente=int(g.lula.sum() - g["dir"].sum()), pct_lula_validos=float(100 * g.lula.sum() / (g.lula.sum() + g["dir"].sum())))
    R = pd.DataFrame([res(alvo, "novas com comparecimento >= 95% (as 427)"), res(ref_novas, "novas com comparecimento < 95%"), res(ref_antigas95, "antigas com comparecimento >= 95%"), res(b, "todas as secoes apuradas")])
    R.to_csv(os.path.join(saida, "A27_perfil.csv"), index=False)
    T = pd.concat([alvo.tipo_local.value_counts(normalize=True).rename("pct_427"), ref_novas.tipo_local.value_counts(normalize=True).rename("pct_novas_abaixo_95"), b.tipo_local.value_counts(normalize=True).rename("pct_todas")], axis=1).fillna(0).mul(100).round(1)
    T.index.name = "tipo_de_local_pelo_nome_e_endereco"; T.to_csv(os.path.join(saida, "A27_tipo_de_local.csv"))
    U = alvo.groupby("SG_UF").size().rename("secoes_427").to_frame().join(b[b.nova].groupby("SG_UF").size().rename("secoes_novas_na_UF")).assign(pct=lambda d: 100 * d.secoes_427 / d.secoes_novas_na_UF).sort_values("secoes_427", ascending=False)
    U.round(2).to_csv(os.path.join(saida, "A27_por_UF.csv"))
    M = alvo.groupby(["SG_UF", "CD_MUNICIPIO"]).agg(secoes=("NR_SECAO", "size"), aptos=("QT_APTOS", "sum"), margem_liquida=("lula", "sum")).reset_index()
    M["margem_liquida"] = alvo.groupby(["SG_UF", "CD_MUNICIPIO"]).apply(lambda g: int(g.lula.sum() - g["dir"].sum())).values
    M.sort_values("secoes", ascending=False).head(15).to_csv(os.path.join(saida, "A27_maiores_municipios.csv"), index=False)
    print(R.round(2).to_string()); print(T.to_string()); print(U.head(8).to_string())
    print("sem endereco:", int(alvo.DS_LOCAL_VOTACAO_ENDERECO.isna().sum()))


if __name__ == "__main__":
    main(*sys.argv[1:3])
