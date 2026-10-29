#!/usr/bin/env python3
"""A21 (Fase 3): forense temporal dos logs de urna, com as medidas ja extraidas por 08_arquivos_urna.py (intervalos curtos entre habilitacoes, horario do ultimo voto).
Compara 2022 e 2026 nas mesmas secoes da amostra e a associacao com o voto (efeito fixo de local, controle do 1o turno). Pre-registro: Adendo 8.
NAO EXECUTADO: distribuicao completa dos intervalos, rajadas por ano de nascimento e concentracao na ultima hora (as medidas nao foram extraidas; exigem reler os logs).
Uso: python -I 21_forense_logs.py DIR_PARQUET DIR_URNA_OUT DIR_SAIDA"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_auditoria import KEY, Registro, carrega, fe_ols
from f2_a4_a5 import _carrega, _junta


def prepara(D, ud, ano):
    m = _junta(D, _carrega(ud, ano), ano)
    m = m[m.QT_COMPARECIMENTO.notna() & (m.n_computado > 0)].copy()
    t1 = D[(ano, 1)][KEY + ["lula_sh", "turnout"]].rename(columns={"lula_sh": "lula_sh_t1", "turnout": "turnout_t1"})
    m = m.merge(t1, on=KEY, how="left")
    m["turnout"] = m.QT_COMPARECIMENTO / m.QT_APTOS
    m["gap5_por_100"] = 100 * m.n_gap_lt_5s / m.n_computado
    m["gap10_por_100"] = 100 * m.n_gap_lt_10s / m.n_computado
    m["ultimo_voto_apos_nominal_min"] = m.ultimo_voto_s / 60 - (m.ab_nominal_min + 540)
    m["votos_apos_nominal_por_100"] = 100 * m.votos_apos_nominal / m.n_computado
    return m[m.valid2 >= 30].copy()


def main(pq, ud, saida):
    os.makedirs(saida, exist_ok=True)
    D = carrega(pq, (2022, 2026))
    M = {a: prepara(D, ud, a) for a in (2026, 2022)}
    feats = {"gap5_por_100": "intervalos < 5 s entre habilitacoes, por 100 votos", "gap10_por_100": "intervalos < 10 s entre habilitacoes, por 100 votos",
             "ultimo_voto_apos_nominal_min": "minutos do ultimo voto depois do horario nominal de fechamento", "votos_apos_nominal_por_100": "votos depois do horario nominal, por 100 votos"}
    # (i) descritivo e pareado
    ch = set(map(tuple, M[2026][KEY].values)) & set(map(tuple, M[2022][KEY].values))
    desc = []
    for f, nome in feats.items():
        a = M[2026].set_index(KEY)[f]; b = M[2022].set_index(KEY)[f]
        j = pd.concat([a.rename("a26"), b.rename("a22")], axis=1, join="inner").dropna()
        dif = j.a26 - j.a22
        desc.append(dict(medida=nome, secoes_pareadas=len(j), media_2026=float(j.a26.mean()), media_2022=float(j.a22.mean()), diferenca_media=float(dif.mean()), ep=float(dif.std(ddof=1) / np.sqrt(len(j))),
                         pct_secoes_com_valor_positivo_2026=float(100 * (j.a26 > 0).mean()), pct_secoes_com_valor_positivo_2022=float(100 * (j.a22 > 0).mean())))
    pd.DataFrame(desc).to_csv(os.path.join(saida, "A21_descritivo_pareado.csv"), index=False)
    # (ii) associacao com o voto
    reg = Registro(); linhas = []
    for f, nome in feats.items():
        res = {}
        for ano in (2026, 2022):
            m = M[ano]
            try:
                r = fe_ols(m, "lula_sh", [f, "lula_sh_t1", "turnout"], "uf_local")
                res[ano] = (float(r.loc[f, "coef"]), float(r.loc[f, "se"]), int(r.n.iloc[0]))
            except ValueError as e:
                res[ano] = None; linhas.append(dict(medida=f, ano=ano, erro=str(e)))
        for ano, v in res.items():
            if v:
                linhas.append(dict(medida=f, ano=ano, coef_lula_sh_por_unidade=v[0], ep=v[1], n=v[2]))
        if res[2026] and res[2022]:
            reg.add("A21", f"associacao com a participacao de Lula (T2, EF de local, controle T1): {nome}", res[2026][0], res[2026][1], [("2022/T2 (mesmas secoes)", res[2022][0], res[2022][1])], sentido="PT",
                    nota="amostra de arquivos de urna (nao nacional); sem conversao em votos")
    pd.DataFrame(linhas).to_csv(os.path.join(saida, "A21_associacao_com_voto.csv"), index=False)
    fr = reg.frame()
    fr.to_csv(os.path.join(saida, "A21_testes.csv"), index=False)
    print(pd.DataFrame(desc).round(4).to_string()); print(pd.DataFrame(linhas).round(5).to_string()); print(fr[["teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "veredito"]].to_string())


if __name__ == "__main__":
    main(*sys.argv[1:4])
