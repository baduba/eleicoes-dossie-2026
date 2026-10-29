#!/usr/bin/env python3
"""A34, Adendo 16b (pos-hoc): regra do percentil 99 e diferenca pareada de D1 so nas UFs cuja classe de cedula (um ou dois cargos, pela mediana de D1 da UF no 2o turno >= 14 s) e a mesma em 2022 e 2026.
Uso: python -I 48_a34_diagnostico_composicao.py DIR_LOGS_F34 DIR_PARQUET DIR_AMOSTRA DIR_SAIDA"""
import importlib.util
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("a34", os.path.join(AQUI, "47_a34_duracao_do_voto.py"))
a34 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a34)
LIM_DOIS = 14.0


def main(dl, pq, damostra, saida):
    L, _ = a34.carrega(dl, damostra, pq)
    t2 = L[L.turno == 2]
    med = t2.groupby(["SG_UF", "ano"]).D1.median().unstack()
    cls = (med >= LIM_DOIS).replace({True: "dois cargos", False: "um cargo"})
    tab = pd.DataFrame({"mediana_D1_2022": med[2022], "mediana_D1_2026": med[2026], "classe_2022": cls[2022], "classe_2026": cls[2026]})
    tab["mesma_classe"] = tab.classe_2022 == tab.classe_2026
    tab["secoes_2026"] = t2[t2.ano == 2026].groupby("SG_UF").size(); tab["secoes_2022"] = t2[t2.ano == 2022].groupby("SG_UF").size()
    tab.reset_index().to_csv(os.path.join(saida, "A34_diag_classe_por_UF.csv"), index=False)
    L = L.merge(tab[["classe_2022", "mesma_classe"]].reset_index(), on="SG_UF", how="left")
    res, pares = [], []
    for classe in ("um cargo", "dois cargos", "todas as UFs de mesma classe"):
        sub = L[L.mesma_classe & (L.classe_2022 == classe)] if classe != "todas as UFs de mesma classe" else L[L.mesma_classe]
        for m in ("D3", "D6"):
            if classe == "todas as UFs de mesma classe":
                # p99 de 2022 calculado DENTRO de cada classe e aplicado as secoes da mesma classe
                acima, tot = 0, 0
                for c in ("um cargo", "dois cargos"):
                    s = L[L.mesma_classe & (L.classe_2022 == c)]
                    lim = float(s[(s.ano == 2022) & (s.turno == 2)][m].quantile(.99)); x = s[(s.ano == 2026) & (s.turno == 2)][m].dropna()
                    acima += int((x > lim).sum()); tot += len(x)
                fr, n_, lim = acima / tot, tot, np.nan
            else:
                lim = float(sub[(sub.ano == 2022) & (sub.turno == 2)][m].quantile(.99)); x = sub[(sub.ano == 2026) & (sub.turno == 2)][m].dropna()
                fr, n_ = float((x > lim).mean()), len(x)
            ep = float(np.sqrt(0.01 * 0.99 / n_))
            res.append(dict(classe=classe, metrica=m, ufs=int(sub.SG_UF.nunique()), secoes_2026T2=n_, limiar_p99_2022T2=lim, fracao_acima=fr, esperado=0.01, ep_binomial=ep, excesso=bool(fr - 0.01 > 2 * ep)))
        for met in ("D1", "D3", "D6"):
            r = a34.dif_pareada(sub, 2026, 2, 2022, 2, met); pares.append(dict(classe=classe, metrica=met, **r))
    # teto no subconjunto de mesma classe (limiar de cada classe), mesma conta do Adendo 16
    from lib_auditoria import KEY, MARGEM
    b = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet"), columns=KEY + ["valid2", "lula", "lula_sh", "uf_local", "DS_TIPO_URNA"])
    b["loc_l"] = b.groupby("uf_local").lula.transform("sum") - b.lula; b["loc_v"] = b.groupby("uf_local").valid2.transform("sum") - b.valid2
    fls, ntot = [], 0
    for c in ("um cargo", "dois cargos"):
        sc = L[L.mesma_classe & (L.classe_2022 == c)]
        lim = float(sc[(sc.ano == 2022) & (sc.turno == 2)].D3.quantile(.99)); x = sc[(sc.ano == 2026) & (sc.turno == 2)]
        ntot += len(x); fls.append(x[x.D3 > lim])
    fl = pd.concat(fls).merge(b[KEY + ["valid2", "lula", "lula_sh", "loc_l", "loc_v"]], on=KEY, how="left"); fl["s_viz"] = fl.loc_l / fl.loc_v.where(fl.loc_v > 0)
    frac = len(fl) / ntot; exc = max(0.0, frac - 0.01)
    teto = dict(secoes_amostra_mesma_classe=ntot, secoes_acima=len(fl), fracao_acima=frac, a_fator1_votos_validos_das_secoes_acima=float(fl.valid2.sum()),
                b_fator2_ganho_de_lula_sobre_a_vizinhanca=float((np.maximum(0, fl.lula_sh - fl.s_viz.fillna(fl.lula_sh)) * fl.valid2 * 2).sum()),
                extrapolacao_nacional_excesso_sobre_1pct_fator1=float(exc * 497_897 * fl.valid2.mean()), pct_da_margem_extrapolacao=100 * float(exc * 497_897 * fl.valid2.mean()) / MARGEM,
                nota="teto de pior caso, nao estimativa; (a) e (b) valem so para a amostra de logs; a extrapolacao vale so para o excesso acima de 1% (D3); inflado por construcao")
    pd.DataFrame([teto]).to_csv(os.path.join(saida, "A34_diag_teto.csv"), index=False); print(pd.Series(teto).to_string())
    pd.DataFrame(res).to_csv(os.path.join(saida, "A34_diag_regra_p99_por_classe.csv"), index=False)
    pd.DataFrame(pares).to_csv(os.path.join(saida, "A34_diag_pareada_por_classe.csv"), index=False)
    pd.set_option("display.width", 220)
    print(tab.round(1).to_string()); print(pd.DataFrame(res).round(4).to_string()); print(pd.DataFrame(pares).round(3).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
