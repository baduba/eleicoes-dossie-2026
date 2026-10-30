#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro) — Investigacao B: Nordeste, sem-biometria x troca de urna x dominio.

A) Correlacao municipio a municipio no NE (2026/T2): taxa sem-biometria (biom_nh/comparecimento) vs
   percentual de secoes com urna trocada — Spearman sobre o CSV do dono (dados_locais/ne_municipios_biom_troca.csv)
   e, como checagem independente, recomputado dos parquets (NE = MA PI CE RN PB PE AL SE BA).
B) Sobreposicao no NE (2026/T2): secoes com lula_sh >= 0,80 E (urna trocada OU taxa sem-biom do municipio
   acima do p90 do NE). Contagem, votos de Lula, saldo (lula - dir) e teto em votos de margem (fator 2, pior caso).
C) Mesma medida em 2022/T2 (controle de forma: Lula tambem venceu; pergunta = o padrao e especifico de 2026?).
D) Secoes do Brasil com o oponente entre 0 e 10 votos, 2026 e 2022: contagem (confere o 3.042 do dono?),
   votos envolvidos, distribuicao por regiao.
Uso: venv/bin/python scripts/exploratorio/07_nordeste_biom_troca.py results/exploratorio
"""
import os
import sys
import zipfile

import numpy as np
import pandas as pd
from scipy import stats

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
NE = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]
REGIAO = {"N": ["AM", "RR", "PA", "AP", "TO", "RO", "AC"], "NE": NE,
          "CO": ["MT", "MS", "GO", "DF"], "SE": ["SP", "RJ", "MG", "ES"], "S": ["PR", "RS", "SC"]}
UF2REG = {u: r for r, ufs in REGIAO.items() for u in ufs}
MARGEM = 4_430_191


def base(ano):
    d = pd.read_parquet(f"parquet/bu_{ano}_t2.parquet")
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.valid2 > 0)].copy()


def cesp_subst(ano):
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
    out = []

    # A) correlacao por taxa — CSV do dono
    dono = pd.read_csv("dados_locais/ne_municipios_biom_troca.csv")
    sp = stats.spearmanr(dono.taxa_sem_biom, dono.pct_trocadas)
    out.append(dict(bloco="A correlacao NE (nivel municipal, taxa x taxa)", fonte="CSV do dono",
                    ano=2026, n=len(dono), estatistica=f"Spearman rho = {sp.statistic:.3f}, p = {sp.pvalue:.3g}",
                    leitura="sem correlacao por taxa" if sp.pvalue > 0.05 else f"correlacao {'positiva' if sp.statistic > 0 else 'negativa'} por taxa"))

    # recomputado dos parquets (troca via CESP 2026)
    d26 = base(2026)
    ce = cesp_subst(2026)
    d26 = d26.merge(ce, on=KEY, how="left")
    d26["troc"] = (d26.NR_URNA_ESPERADA.astype("Int64") != d26.NR_URNA.astype("Int64")) & d26.NR_URNA_ESPERADA.notna()
    ne26 = d26[d26.SG_UF.isin(NE)]
    mun = ne26.groupby(["SG_UF", "CD_MUNICIPIO"]).agg(comp=("QT_COMPARECIMENTO", "sum"), sem_biom=("biom_nh", "sum"),
                                                      troc=("troc", "mean")).reset_index()
    mun["taxa_sem_biom"] = 100 * mun.sem_biom / mun.comp
    sp2 = stats.spearmanr(mun.taxa_sem_biom, 100 * mun.troc)
    out.append(dict(bloco="A correlacao NE (nivel municipal, taxa x taxa)", fonte="recomputado dos parquets + CESP",
                    ano=2026, n=len(mun), estatistica=f"Spearman rho = {sp2.statistic:.3f}, p = {sp2.pvalue:.3g}",
                    leitura="sem correlacao por taxa" if sp2.pvalue > 0.05 else f"correlacao {'positiva' if sp2.statistic > 0 else 'negativa'} por taxa"))

    # B) sobreposicao NE 2026: lula_sh >= 0,80 E (troc OU municipio com taxa sem-biom > p90 do NE)
    p90 = mun.taxa_sem_biom.quantile(0.90)
    altas = set(map(tuple, mun[mun.taxa_sem_biom > p90][["SG_UF", "CD_MUNICIPIO"]].values))
    def sobre(d, ano, rotulo):
        ne = d[d.SG_UF.isin(NE)].copy()
        if "troc" not in ne.columns:
            ne["troc"] = np.nan  # juncao CESP-2022 nao confiavel: so a flag municipal entra em 2022
        mun_tx = ne.groupby(["SG_UF", "CD_MUNICIPIO"]).apply(
            lambda g: 100 * g.biom_nh.sum() / g.QT_COMPARECIMENTO.sum(), include_groups=False).rename("tx").reset_index()
        limiar = mun_tx.tx.quantile(0.90)
        alt = set(map(tuple, mun_tx[mun_tx.tx > limiar][["SG_UF", "CD_MUNICIPIO"]].values))
        ne["mun_alta"] = [t in alt for t in map(tuple, ne[["SG_UF", "CD_MUNICIPIO"]].values)]
        dom = ne.lula_sh >= 0.80
        sel = ne[dom & (ne.troc.fillna(False) | ne.mun_alta)]
        return dict(bloco="B sobreposicao NE: Lula >= 80% dos validos E (troca OU municipio no p90 sem-biom)",
                    ano=ano, secoes=len(sel), votos_lula=int(sel.lula.sum()), validos=int(sel.valid2.sum()),
                    saldo_lula_menos_opo=int((sel.lula - sel["dir"]).sum()),
                    teto_votos_margem_fator2=int(2 * (sel.lula - sel["dir"]).sum()),
                    teto_pct_margem=round(100 * 2 * (sel.lula - sel["dir"]).sum() / MARGEM, 2),
                    secoes_dominio_total=int(dom.sum()), secoes_dominio_sem_flag=int((dom & ~(ne.troc.fillna(False) | ne.mun_alta)).sum()),
                    leitura=f"p90 taxa sem-biom do ano = {limiar:.1f}%")
    out.append(sobre(d26, 2026, "2026"))

    # C) 2022 controle de forma (mesma regra; troca de urna 2022 indisponivel nesta juncao — so flag municipal)
    d22 = base(2022)
    b22 = sobre(d22, 2022, "2022")
    b22["leitura"] += "; sem a flag de troca (juncao CESP-2022 nao confiavel) — comparacao conservadora a favor de 2022"
    out.append(b22)

    # D) oponente com 0 a 10 votos, Brasil, 2026 e 2022
    for ano, d in ((2026, d26), (2022, d22)):
        z = d[d["dir"] <= 10]
        z = z.assign(regiao=z.SG_UF.map(UF2REG))
        por = z.groupby("regiao").agg(secoes=("lula", "size"), votos_lula=("lula", "sum"),
                                      saldo=("lula", lambda s: 0)).reset_index()
        saldos = z.groupby("regiao").apply(lambda g: int((g.lula - g["dir"]).sum()), include_groups=False)
        por["saldo"] = por.regiao.map(saldos)
        out.append(dict(bloco="D oponente com 0 a 10 votos", ano=ano, secoes=len(z), votos_lula=int(z.lula.sum()),
                        validos=int(z.valid2.sum()), saldo=int((z.lula - z["dir"]).sum()),
                        teto_votos_margem_fator2=int(2 * (z.lula - z["dir"]).sum()),
                        teto_pct_margem=round(100 * 2 * (z.lula - z["dir"]).sum() / MARGEM, 2),
                        leitura="; ".join(f"{r.regiao}: {r.secoes} secoes, {r.votos_lula} votos Lula" for r in por.itertuples())))
    pd.DataFrame(out).to_csv(os.path.join(saida, "B_nordeste_biom_troca.csv"), index=False)
    print(pd.DataFrame(out).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
