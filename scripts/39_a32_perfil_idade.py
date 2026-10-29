#!/usr/bin/env python3
"""A32 (Adendo 11), itens 2 e 3: perfil do eleitorado por secao com a composicao por faixa etaria (a partir dos mesmos zips de 30_perfil_secao.py).
Saida: perfil_idade_{ano}.parquet com, por secao, aptos, biometria cadastrada, fracao de aptos nos grupos 16-29, 30-44, 45-59, 60-69, 70-79, 80+ e idade media (ponto medio das faixas; 100+ = 102).
Uso: python -I 39_a32_perfil_idade.py DIR_ZIPS DIR_SAIDA 2022 2026"""
import importlib.util
import os
import re
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("p30", os.path.join(AQUI, "30_perfil_secao.py")); p30 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p30)
GRUPOS = [("g16_29", 16, 29), ("g30_44", 30, 44), ("g45_59", 45, 59), ("g60_69", 60, 69), ("g70_79", 70, 79), ("g80p", 80, 200)]


def meio(f):
    f = str(f)
    if "100" in f and "mais" in f:
        return 102.0
    n = [int(x) for x in re.findall(r"\d+", f)]
    return float(np.mean(n)) if n else np.nan


def main(zdir, saida, anos):
    os.makedirs(saida, exist_ok=True)
    for ano in anos:
        partes = []
        for uf in p30.UFS:
            if uf == "ZZ":
                continue
            z = os.path.join(zdir, f"perfil_eleitor_secao_{ano}_{uf}.zip")
            d = p30.le(z, ano)
            d["ponto"] = d.faixa.map(meio)
            d = d[d.ponto.notna()]
            d["soma_idade"] = d.apt * d.ponto
            for nome, lo, hi in GRUPOS:
                d[nome] = np.where((d.ponto >= lo) & (d.ponto <= hi), d.apt, 0.0)
            agg = d.groupby(p30.KEY + ["NR_LOCAL_VOTACAO"], dropna=False).agg(apt=("apt", "sum"), bio=("bio", "sum"), soma_idade=("soma_idade", "sum"), **{n: (n, "sum") for n, _, _ in GRUPOS}).reset_index()
            partes.append(agg)
            print(ano, uf, len(agg), flush=True)
        s = pd.concat(partes, ignore_index=True)
        s["idade_media"] = s.soma_idade / s.apt.replace(0, np.nan)
        for n, _, _ in GRUPOS:
            s[n] = s[n] / s.apt.replace(0, np.nan)
        s["bio_frac"] = s.bio / s.apt.replace(0, np.nan)
        s.drop(columns="soma_idade").to_parquet(os.path.join(saida, f"perfil_idade_{ano}.parquet"), index=False)
        print("ok", ano, len(s))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]])
