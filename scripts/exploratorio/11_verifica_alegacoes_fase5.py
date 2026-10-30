#!/usr/bin/env python3
"""EXPLORATORIO — verificacao factual rapida de duas alegacoes externas (rodada 30/10/2026).

NAO e teste pre-registrado: e checagem de alegacao, numeros descritivos.

ALEGACAO 1 (candidata a A41): "23 municipios da Bahia com mais eleitores do que habitantes".
  - Populacao local disponivel: results/fase3/A20_mapa_tse_ibge.csv (pop16, Censo 2022, por municipio TSE).
  - Populacao TOTAL municipal NAO esta local -> o corte exato da alegacao (aptos > pop total) nao fecha;
    cortes possiveis: aptos > pop16 (mais forte que a alegacao) e comparecimento > pop16.
  - Saidas: ALE_municipios_aptos_vs_pop16.csv, ALE_ba_aptos_maior_pop16_lista.csv, ALE_resumo_aptos_vs_pop16.csv

ALEGACAO 2 (candidata a A40): "em secoes com alta taxa manual, o voto no incumbente sobe linearmente acima de 61%".
  - Curva: share de Lula (pooled, lula/valid2) por faixa de manual_rate, 2026 T2; controles 2026 T1, 2022 T2, 2018 T2;
    por UF (BA, SP); e 2026 T2 escola vs nao-escola (nome do local, locais_2026).
  - Saidas: ALE_curva_manual_por_ano.csv, ALE_curva_manual_por_uf_2026t2.csv, ALE_curva_manual_escola_2026t2.csv

Uso: ./venv/bin/python scripts/exploratorio/11_verifica_alegacoes_fase5.py results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd

PQ = "parquet"
F3 = "results/fase3"

FAIXAS = [(0.0, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, 0.30), (0.30, 1.01)]
ROTULOS = ["0-5%", "5-10%", "10-20%", "20-30%", ">30%"]


def base_bu(ano, turno, colunas):
    if "DS_TIPO_URNA" not in colunas:
        colunas = colunas + ["DS_TIPO_URNA"]
    d = pd.read_parquet(os.path.join(PQ, f"bu_{ano}_t{turno}.parquet"), columns=colunas)
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ")].copy()


def alegacao1(saida):
    mapa = pd.read_csv(os.path.join(F3, "A20_mapa_tse_ibge.csv")).dropna(subset=["pop16"])
    resumo, detalhe = [], []
    for ano, turno in [(2018, 2), (2022, 2), (2026, 1), (2026, 2)]:
        d = base_bu(ano, turno, ["SG_UF", "CD_MUNICIPIO", "QT_APTOS", "QT_COMPARECIMENTO"])
        g = d.groupby(["SG_UF", "CD_MUNICIPIO"], as_index=False).agg(aptos=("QT_APTOS", "sum"), comp=("QT_COMPARECIMENTO", "sum"))
        m = g.merge(mapa[["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO", "pop16"]], on=["SG_UF", "CD_MUNICIPIO"], how="inner")
        m["razao_aptos_pop16"] = m.aptos / m.pop16
        m["razao_comp_pop16"] = m.comp / m.pop16
        m["ano"], m["turno"] = ano, turno
        detalhe.append(m)
        for uf in ["BR", "BA"]:
            e = m if uf == "BR" else m[m.SG_UF == "BA"]
            resumo.append(dict(ano=ano, turno=turno, recorte=uf, municipios=len(e),
                               aptos_maior_pop16=int((e.razao_aptos_pop16 > 1).sum()),
                               fracao_aptos_maior_pop16=float((e.razao_aptos_pop16 > 1).mean()),
                               comp_maior_pop16=int((e.razao_comp_pop16 > 1).sum()),
                               mediana_razao=float(e.razao_aptos_pop16.median()),
                               p95_razao=float(e.razao_aptos_pop16.quantile(0.95)),
                               max_razao=float(e.razao_aptos_pop16.max())))
    T = pd.concat(detalhe, ignore_index=True)
    T.to_csv(os.path.join(saida, "ALE_municipios_aptos_vs_pop16.csv"), index=False)
    R = pd.DataFrame(resumo)
    R.to_csv(os.path.join(saida, "ALE_resumo_aptos_vs_pop16.csv"), index=False)
    ba26 = T[(T.ano == 2026) & (T.turno == 2) & (T.SG_UF == "BA") & (T.razao_aptos_pop16 > 1)].sort_values("razao_aptos_pop16", ascending=False)
    ba26.to_csv(os.path.join(saida, "ALE_ba_aptos_maior_pop16_lista.csv"), index=False)
    return R, ba26


def curva(d, grupo_cols):
    d = d.dropna(subset=["manual_rate"])
    d = d[d.manual_rate.between(0, 1)]
    d["faixa"] = pd.cut(d.manual_rate, bins=[-1e-9] + [b for _, b in FAIXAS], labels=ROTULOS)
    g = d.groupby(grupo_cols + ["faixa"], observed=True)
    out = g.agg(secoes=("valid2", "size"), validos=("valid2", "sum"), lula=("lula", "sum"),
                manual_medio=("manual_rate", "mean")).reset_index()
    out["lula_pct_validos"] = 100 * out.lula / out.validos
    return out


def alegacao2(saida):
    cols = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO",
            "DS_TIPO_URNA", "QT_COMPARECIMENTO", "valid2", "lula", "manual_rate"]
    curvas = []
    for ano, turno in [(2026, 2), (2026, 1), (2022, 2), (2018, 2)]:
        d = base_bu(ano, turno, cols)
        d = d[d.QT_COMPARECIMENTO >= 30]
        c = curva(d, []).assign(ano=ano, turno=turno)
        curvas.append(c)
    C = pd.concat(curvas, ignore_index=True)[["ano", "turno", "faixa", "secoes", "validos", "lula_pct_validos", "manual_medio"]]
    C.to_csv(os.path.join(saida, "ALE_curva_manual_por_ano.csv"), index=False)

    d26 = base_bu(2026, 2, cols)
    d26 = d26[d26.QT_COMPARECIMENTO >= 30]
    cu = curva(d26[d26.SG_UF.isin(["BA", "SP"])], ["SG_UF"])
    cu.to_csv(os.path.join(saida, "ALE_curva_manual_por_uf_2026t2.csv"), index=False)

    loc = pd.read_parquet(os.path.join(PQ, "locais_2026.parquet"))
    loc["escola"] = loc.NM_LOCAL_VOTACAO.str.upper().str.contains("ESCOLA|COLEGIO", regex=True, na=False)
    d26e = d26.merge(loc[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "escola"]],
                     on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"], how="left")
    ce = curva(d26e.dropna(subset=["escola"]), ["escola"])
    ce.to_csv(os.path.join(saida, "ALE_curva_manual_escola_2026t2.csv"), index=False)

    # linearidade: correlacao ponderada entre manual_rate e lula_sh (secao), por ano
    lin = []
    for ano, turno in [(2026, 2), (2026, 1), (2022, 2), (2018, 2)]:
        d = base_bu(ano, turno, cols)
        d = d[(d.QT_COMPARECIMENTO >= 30) & d.manual_rate.notna() & d.manual_rate.between(0, 1) & (d.valid2 > 0)]
        w = d.valid2.values.astype(float)
        x, y = d.manual_rate.values, (d.lula / d.valid2).values
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        cov = np.average((x - mx) * (y - my), weights=w)
        r = cov / (np.sqrt(np.average((x - mx) ** 2, weights=w)) * np.sqrt(np.average((y - my) ** 2, weights=w)))
        lin.append(dict(ano=ano, turno=turno, secoes=len(d), r_ponderado_manual_x_share=float(r)))
    L = pd.DataFrame(lin)
    L.to_csv(os.path.join(saida, "ALE_linearidade_manual.csv"), index=False)
    return C, cu, ce, L


def main():
    saida = sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio"
    os.makedirs(saida, exist_ok=True)
    R, ba26 = alegacao1(saida)
    print("== ALEGACAO 1: aptos x pop16 (Censo 2022) ==")
    print(R[R.recorte == "BA"].to_string(index=False))
    print("\nBR (nacional):")
    print(R[R.recorte == "BR"].to_string(index=False))
    print(f"\nBA 2026 T2: municipios com aptos>pop16: {len(ba26)} (alegacao fala em 23 com aptos>pop TOTAL)")
    print(ba26[["NM_MUNICIPIO", "aptos", "pop16", "razao_aptos_pop16"]].head(30).to_string(index=False))
    C, cu, ce, L = alegacao2(saida)
    print("\n== ALEGACAO 2: curva share Lula x faixa de taxa manual ==")
    print(C.pivot_table(index="faixa", columns=["ano", "turno"], values="lula_pct_validos").round(2).to_string())
    print("\nn de secoes por faixa:")
    print(C.pivot_table(index="faixa", columns=["ano", "turno"], values="secoes").to_string())
    print("\n2026 T2 por UF (BA, SP):")
    print(cu.pivot_table(index="faixa", columns="SG_UF", values="lula_pct_validos").round(2).to_string())
    print("\n2026 T2 escola vs nao-escola:")
    print(ce.pivot_table(index="faixa", columns="escola", values="lula_pct_validos").round(2).to_string())
    print("\nlinearidade (r ponderado manual x share):")
    print(L.to_string(index=False))


if __name__ == "__main__":
    main()
