#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro) — H20: "mecanismo estrutural de longa data" (objecao do dono:
constancia 2022/2026 nao refuta; pode datar a tecnica). Serie completa disponivel: 2014, 2018, 2022, 2026 (T2).

H20a constancia: mesmos indicadores nos 4 anos.
H20b mobilidade: permanencia dos municipios extremos entre eleicoes (top 5% por saldo PT por apto).
H20c discriminacao de vencedor: 2018 (Bolsonaro venceu) incluido; cortes refeitos com os pares corretos
     (2014 Dilma x Aecio; 2018 Haddad x Bolsonaro; 2022 Lula x Bolsonaro; 2026 Lula x Flavio).

Indicadores por ano (T2, secoes apuradas, sem exterior, validos > 0):
(i)   empates: observado / esperado pelo nulo binomial (p da zona, leave-one-out); idem +-1 voto;
(ii)  secoes com oponente do PT entre 0 e 10 votos: n, saldo, % no NE;
(iii) saldo do PT concentrado em secoes com PT >= 80% dos validos (Brasil e NE);
(iv)  mediana de comparecimento das secoes do indicador (ii);
(v)   taxa sem-biometria no NE (biom_nh / comparecimento);
(vi)  permanencia geografica: % dos municipios extremos (top 5% saldo PT por apto) que eram extremos na
      eleicao anterior (e em todas as anteriores).

Uso: venv/bin/python scripts/exploratorio/08_h20_serie_historica.py results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

NE = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]
ANOS = (2014, 2018, 2022, 2026)


def base(ano):
    d = pd.read_parquet(f"parquet/bu_{ano}_t2.parquet")
    return d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.valid2 > 0)].copy()


def prob_margens(d, kmax=1):
    g = d.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])
    sl = g.lula.transform("sum") - d.lula
    sv = g.valid2.transform("sum") - d.valid2
    p = np.clip(np.where(sv > 0, sl / sv, 0.5), 0.001, 0.999)
    n = d.valid2.to_numpy()
    prob = np.zeros((len(d), kmax + 1))
    for m in range(kmax + 1):
        ks = [(n + s) / 2 for s in (-m, m)] if m > 0 else [n / 2]
        pm = np.zeros(len(d))
        for k in ks:
            ok = np.abs(k - np.round(k)) < 1e-9
            pm += np.where(ok, stats.binom.pmf(np.round(k), n, p), 0.0)
        prob[:, m] = pm
    return prob


def main(saida):
    os.makedirs(saida, exist_ok=True)
    linhas, extremos = [], {}
    for ano in ANOS:
        d = base(ano)
        d["margem"] = d.lula - d["dir"]
        am = d.margem.abs()
        prob = prob_margens(d, 1)
        obs_emp, obs_um = int((am == 0).sum()), int((am == 1).sum())
        esp_emp, esp_um = float(prob[:, 0].sum()), float(prob[:, 1].sum())
        ne = d[d.SG_UF.isin(NE)]
        z = d[d["dir"] <= 10]                      # oponente do PT com 0-10 votos
        z_ne = z[z.SG_UF.isin(NE)]
        dom = d[d.lula_sh >= 0.80]
        dom_ne = ne[ne.lula_sh >= 0.80]
        linhas.append(dict(
            ano=ano, secoes=len(d),
            empates_obs=obs_emp, empates_esp_nulo=round(esp_emp, 1), empates_razao=round(obs_emp / esp_emp, 3),
            um_obs=obs_um, um_esp_nulo=round(esp_um, 1), um_razao=round(obs_um / esp_um, 3),
            opo_0a10_secoes=len(z), opo_0a10_saldo=int((z.lula - z["dir"]).sum()),
            opo_0a10_pct_NE=round(100 * len(z_ne) / len(z), 1),
            opo_0a10_mediana_comp=float(z.QT_COMPARECIMENTO.median()),
            dom80_secoes=len(dom), dom80_saldo=int((dom.lula - dom["dir"]).sum()),
            dom80_NE_secoes=len(dom_ne), dom80_NE_saldo=int((dom_ne.lula - dom_ne["dir"]).sum()),
            taxa_sem_biom_NE=round(100 * ne.biom_nh.sum() / ne.QT_COMPARECIMENTO.sum(), 2),
            saldo_PT_nacional=int((d.lula - d["dir"]).sum()),
        ))
        mun = d.groupby(["SG_UF", "CD_MUNICIPIO"]).agg(s=("lula", "sum"), o=("dir", "sum"),
                                                       apt=("QT_APTOS", "sum")).reset_index()
        mun["saldo_pa"] = (mun.s - mun.o) / mun.apt
        corte = mun.saldo_pa.quantile(0.95)
        extremos[ano] = set(map(tuple, mun[mun.saldo_pa >= corte][["SG_UF", "CD_MUNICIPIO"]].values))

    t = pd.DataFrame(linhas)
    t.to_csv(os.path.join(saida, "H20_serie_indicadores.csv"), index=False)
    print(t.to_string(index=False))

    # permanencia geografica
    pl = []
    for a, b in ((2018, 2014), (2022, 2018), (2026, 2022)):
        inter = len(extremos[a] & extremos[b])
        pl.append(dict(par=f"{b}->{a}", extremos_no_ano=len(extremos[a]), permanecem_da_anterior=inter,
                       pct_permanencia=round(100 * inter / len(extremos[a]), 1)))
    pl.append(dict(par="2026 vs TODAS as anteriores", extremos_no_ano=len(extremos[2026]),
                   permanecem_da_anterior=len(extremos[2026] & extremos[2022] & extremos[2018] & extremos[2014]),
                   pct_permanencia=round(100 * len(extremos[2026] & extremos[2022] & extremos[2018] & extremos[2014]) / len(extremos[2026]), 1)))
    pd.DataFrame(pl).to_csv(os.path.join(saida, "H20_permanencia_municipios_extremos.csv"), index=False)
    print(pd.DataFrame(pl).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
