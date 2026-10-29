#!/usr/bin/env python3
"""A26 (continuacao): compara o `detalhe_votacao_secao` de uma captura antiga do Wayback Machine com o arquivo atual do TSE, secao a secao, para o cargo de Presidente.
Responde: o arquivo que o TSE publica hoje contem os mesmos numeros de votacao e os mesmos horarios que a captura de novembro de 2022?
Uso: python -I 26b_comparar_capturas.py ANO CAPTURA.zip ATUAL.zip DIR_SAIDA"""
import io
import os
import sys
import zipfile
import numpy as np
import pandas as pd

CH = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_TURNO"]


def le(zpath, ano):
    z = zipfile.ZipFile(zpath)
    nomes = [n for n in z.namelist() if n.endswith(".csv")]
    br = [n for n in nomes if "BRASIL" in n.upper() or n.endswith("_BR.csv")]
    partes = []
    for n in (br or nomes):
        with z.open(n) as f:
            for ch in pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, chunksize=400_000):
                partes.append(ch[ch["CD_CARGO"] == "1"] if "CD_CARGO" in ch else ch)
    d = pd.concat(partes, ignore_index=True)
    for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_TURNO"):       # a captura de 2022 tem zeros a esquerda; so a forma muda
        if c in d:
            d[c] = d[c].str.strip().str.lstrip("0")
    return d, z.namelist()


def main(ano, antiga, atual, saida):
    os.makedirs(saida, exist_ok=True)
    a, na = le(antiga, ano); b, nb = le(atual, ano)
    comuns = [c for c in a.columns if c in b.columns and c not in ("DT_GERACAO", "HH_GERACAO")]
    chave = [c for c in CH if c in comuns]
    a = a.drop_duplicates(chave).set_index(chave); b = b.drop_duplicates(chave).set_index(chave)
    so_a, so_b = a.index.difference(b.index), b.index.difference(a.index)
    j = a.index.intersection(b.index)
    A, B = a.loc[j], b.loc[j]
    linhas = []
    for c in comuns:
        if c in chave:
            continue
        x, y = A[c].fillna("").str.strip(), B[c].fillna("").str.strip()
        if c.startswith(("NR_", "QT_", "CD_")):
            x, y = x.str.lstrip("0"), y.str.lstrip("0")
        dif = int((x != y).sum())
        linhas.append(dict(ano=ano, coluna=c, secoes_comparadas=len(j), secoes_diferentes=dif))
    R = pd.DataFrame(linhas)
    R.to_csv(os.path.join(saida, f"A26b_{ano}_diferencas_por_coluna.csv"), index=False)
    resumo = dict(ano=ano, colunas_so_na_captura=";".join(c for c in a.columns if c not in b.columns), colunas_so_no_atual=";".join(c for c in b.columns if c not in a.columns),
                  secoes_na_captura=len(a), secoes_no_atual=len(b), secoes_so_na_captura=len(so_a), secoes_so_no_atual=len(so_b), secoes_comuns=len(j),
                  colunas_com_diferenca=";".join(R[R.secoes_diferentes > 0].coluna), data_geracao_captura=str(pd.read_csv(io.BytesIO(zipfile.ZipFile(antiga).read([n for n in na if n.endswith('.csv')][0])), sep=";", encoding="latin-1", nrows=1, dtype=str).get("DT_GERACAO", pd.Series([""])).iloc[0]))
    pd.DataFrame([resumo]).to_csv(os.path.join(saida, f"A26b_{ano}_resumo.csv"), index=False)
    print(pd.DataFrame([resumo]).T.to_string()); print(R[R.secoes_diferentes > 0].to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
