#!/usr/bin/env python3
"""A20 (Fase 3): eleitorado apto x populacao residente (Censo 2022, IBGE SIDRA 9514) por municipio e faixa etaria; 2018, 2022 e 2026 (1o turno). Pre-registro: Adendo 8.
Uso: python -I 20_cadastro_ibge.py DIR_PARQUET2 PERFIL_2026.zip DIR_SAIDA
O denominador e a populacao do Censo 2022 em todos os anos; por isso 2018 e 2026 usam denominador defasado e a comparacao normaliza a razao pela razao nacional (ver Adendo 8)."""
import io
import json
import os
import re
import sys
import unicodedata
import urllib.request
import zipfile
import numpy as np
import pandas as pd

TOT, G0004, G0509, G1014, A15, G8084, G8589, G9094, G9599, G100 = "100362", "93070", "93084", "93085", "6572", "49108", "49109", "60040", "60041", "6653"
IDS = [[TOT, G0004, G0509, G1014, A15], [G8084, G8589, G9094, G9599, G100]]
FAIXAS = {"80+": ["80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais"], "90+": ["90 a 94 anos", "95 a 99 anos", "100 anos ou mais"], "100+": ["100 anos ou mais"]}
POP = {"80+": [G8084, G8589, G9094, G9599, G100], "90+": [G9094, G9599, G100], "100+": [G100]}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9]", "", s)


def ibge(saida):
    p = os.path.join(saida, "ibge_pop_9514_2022.csv")
    if os.path.exists(p):
        return pd.read_csv(p, dtype={"cod_ibge": str})
    rows = []
    for ids in IDS:
        u = f"https://apisidra.ibge.gov.br/values/t/9514/n6/all/v/93/p/2022/c2/6794/c287/{','.join(ids)}/c286/113635"
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "auditoria-independente"}), timeout=180))
        rows += [(r["D1C"], r["D1N"], r["D5C"], int(r["V"]) if r["V"].isdigit() else 0) for r in d[1:]]
    d = pd.DataFrame(rows, columns=["cod_ibge", "nome_uf", "faixa", "pop"]).pivot_table(index=["cod_ibge", "nome_uf"], columns="faixa", values="pop", aggfunc="sum").reset_index()
    d.columns = [str(c) for c in d.columns]
    d.to_csv(p, index=False)
    return d


def tse_nomes(zip26):
    partes = []
    z = zipfile.ZipFile(zip26)
    for n in z.namelist():
        if n.endswith(".csv") and not n.endswith("_ZZ.csv") and not n.endswith("_BR.csv"):
            with z.open(n) as f:
                partes.append(pd.read_csv(f, sep=";", encoding="latin-1", usecols=["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"], dtype=str).drop_duplicates())
    d = pd.concat(partes).drop_duplicates(["SG_UF", "CD_MUNICIPIO"])
    d["CD_MUNICIPIO"] = d.CD_MUNICIPIO.astype(int)
    return d


def main(pq2, zip26, saida):
    os.makedirs(saida, exist_ok=True)
    pop = ibge(saida)
    pop["uf"] = pop.nome_uf.str[-2:]
    pop["chave"] = pop.uf + "|" + pop.nome_uf.str[:-5].map(norm)
    pop["pop16"] = pop[TOT] - pop[G0004] - pop[G0509] - pop[G1014] - pop[A15]
    for k, ids in POP.items():
        pop["pop" + k] = pop[ids].sum(axis=1)
    nm = tse_nomes(zip26)
    nm["chave"] = nm.SG_UF + "|" + nm.NM_MUNICIPIO.map(norm)
    m = nm.merge(pop[["chave", "cod_ibge", "pop16", "pop80+", "pop90+", "pop100+"]], on="chave", how="left")
    sem = m[m.cod_ibge.isna()]
    m.drop(columns=["chave"]).to_csv(os.path.join(saida, "A20_mapa_tse_ibge.csv"), index=False)
    linhas, por_mun = [], []
    for ano in (2018, 2022, 2026):
        p = pd.read_parquet(os.path.join(pq2, f"perfil_agg_{ano}.parquet"))
        p = p[(p.NR_TURNO == 1) & (p.SG_UF != "ZZ")]
        a = p.groupby(["SG_UF", "CD_MUNICIPIO"]).QT_APTOS.sum().rename("apt16").to_frame()
        c = p.groupby(["SG_UF", "CD_MUNICIPIO"]).QT_COMPARECIMENTO.sum().rename("comp16")
        a = a.join(c)
        for k, fx in FAIXAS.items():
            q = p[p.DS_FAIXA_ETARIA.isin(fx)].groupby(["SG_UF", "CD_MUNICIPIO"])
            a["apt" + k] = q.QT_APTOS.sum(); a["comp" + k] = q.QT_COMPARECIMENTO.sum()
        a = a.fillna(0).reset_index().merge(m[["SG_UF", "CD_MUNICIPIO", "cod_ibge", "pop16", "pop80+", "pop90+", "pop100+"]], on=["SG_UF", "CD_MUNICIPIO"], how="inner").dropna(subset=["cod_ibge"])
        a["ano"] = ano
        por_mun.append(a)
    A = pd.concat(por_mun)
    grupos = {"16+": ("apt16", "pop16"), "80+": ("apt80+", "pop80+"), "90+": ("apt90+", "pop90+"), "100+": ("apt100+", "pop100+")}
    minpop = {"16+": 100, "80+": 30, "90+": 10, "100+": 1}
    nat22 = {g: A[A.ano == 2022][a].sum() / A[A.ano == 2022][p].sum() for g, (a, p) in grupos.items()}
    for g, (a, p) in grupos.items():
        for ano, d in A.groupby("ano"):
            d = d[d[p] >= minpop[g]]
            r_nat = d[a].sum() / d[p].sum()
            r = d[a] / d[p]
            raw = float((r > 1).mean())
            ajust = float(((r * (nat22[g] / r_nat)) > 1).mean())
            linhas.append(dict(grupo=g, ano=ano, municipios=len(d), razao_nacional=r_nat, aptos=int(d[a].sum()), populacao_2022=int(d[p].sum()), fracao_municipios_razao_gt1_bruta=raw, fracao_razao_gt1_na_escala_de_2022=ajust,
                               mediana_razao=float(r.median()), p95_razao=float(r.quantile(.95)), municipios_razao_gt1_bruta=int((r > 1).sum())))
    R = pd.DataFrame(linhas)
    # teste: a fracao de 2026 (escala de 2022) supera CADA ano de comparacao por mais de 2 erros padrao binomiais?
    ver = []
    for g in grupos:
        x = R[R.grupo == g].set_index("ano")
        f26, n26 = x.loc[2026, "fracao_razao_gt1_na_escala_de_2022"], x.loc[2026, "municipios"]
        exc = True; det = []
        for ano in (2022, 2018):
            f0, n0 = x.loc[ano, "fracao_razao_gt1_na_escala_de_2022"], x.loc[ano, "municipios"]
            se = np.sqrt(f26 * (1 - f26) / n26 + f0 * (1 - f0) / n0)
            z = (f26 - f0) / se if se > 0 else 0.0
            det.append(f"{ano}: dif {100*(f26-f0):.2f} p.p. (z {z:.1f})")
            exc &= z > 2
        ver.append(dict(grupo=g, fracao_2026=f26, comparacao=" | ".join(det), veredito="EXCESSO DETECTADO (teste de forma, sem conversao em votos)" if exc else "SEM EXCESSO (teste de forma, sem conversao em votos)"))
    V = pd.DataFrame(ver)
    R.to_csv(os.path.join(saida, "A20_razoes_por_ano.csv"), index=False)
    V.to_csv(os.path.join(saida, "A20_veredito.csv"), index=False)
    # municipios com razao > 1 em 2026 (16+), ordenados
    d = A[(A.ano == 2026) & (A.pop16 >= 100)].copy(); d["razao_16mais"] = d.apt16 / d.pop16
    d = d.merge(m[["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"]], on=["SG_UF", "CD_MUNICIPIO"])
    d.sort_values("razao_16mais", ascending=False).head(30)[["SG_UF", "NM_MUNICIPIO", "apt16", "pop16", "razao_16mais"]].to_csv(os.path.join(saida, "A20_maiores_razoes_2026.csv"), index=False)
    pd.DataFrame([dict(municipios_tse=len(nm), sem_correspondencia_ibge=len(sem), exemplos=";".join((sem.SG_UF + ":" + sem.NM_MUNICIPIO).head(8)))]).to_csv(os.path.join(saida, "A20_cobertura_do_mapa.csv"), index=False)
    # comparecimento por faixa (80+): taxa por faixa em cada ano e teto de pior caso do aumento de 2026 sobre as taxas de 2022
    bandas = ["70 a 74 anos", "75 a 79 anos", "80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais"]
    cb = []
    for ano in (2018, 2022, 2026):
        p = pd.read_parquet(os.path.join(pq2, f"perfil_agg_{ano}.parquet"))
        q = p[(p.NR_TURNO == 1) & (p.SG_UF != "ZZ") & p.DS_FAIXA_ETARIA.isin(bandas)].groupby("DS_FAIXA_ETARIA")[["QT_APTOS", "QT_COMPARECIMENTO"]].sum()
        q["pct_comparecimento"] = 100 * q.QT_COMPARECIMENTO / q.QT_APTOS; q["ano"] = ano; cb.append(q.reset_index())
    CB = pd.concat(cb).rename(columns={"DS_FAIXA_ETARIA": "faixa", "QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento"})[["ano", "faixa", "aptos", "comparecimento", "pct_comparecimento"]]
    CB.to_csv(os.path.join(saida, "A20_comparecimento_idosos_por_faixa.csv"), index=False)
    a26, a22 = CB[CB.ano == 2026].set_index("faixa"), CB[CB.ano == 2022].set_index("faixa")
    exc = (a26.aptos * (a26.pct_comparecimento - a22.pct_comparecimento) / 100).clip(lower=0)
    tt = pd.DataFrame({"comparecimento_acima_das_taxas_de_2022": exc.round(0)})
    tt["no_grupo_80mais"] = tt.index.isin(bandas[2:])
    tt.to_csv(os.path.join(saida, "A20_comparecimento_acima_das_taxas_2022.csv"))
    print(R.round(3).to_string()); print(V.to_string()); print("sem correspondencia:", len(sem), "de", len(nm))


if __name__ == "__main__":
    main(*sys.argv[1:4])
