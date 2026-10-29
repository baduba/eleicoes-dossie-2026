#!/usr/bin/env python3
"""Analise POSTERIOR (nao pre-registrada) do A1-corrigido no 1o turno de 2026: os pontos da curva fora do envelope do nulo D coincidem com a janela do congestionamento?
Reproduz a estimativa do C1 (mesma semente e mesmas replicas), localiza os pontos fora do envelope, converte cada ponto em horario de totalizacao e em UFs que chegaram no intervalo.
Uso: python -I 16_a1_t1_janela.py DIR_PARQUET DIR_SAIDA"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_auditoria import carrega
from f2_a11_a15 import _serie
from f2_posregistro import _grupos_mun, _ordem_D, _run


def main(pq, saida):
    os.makedirs(saida, exist_ok=True)
    reps = int(os.environ.get("AUDITORIA_REPS_POS", "500")); K = 1000; k10 = 100
    D = carrega(pq, (2026,))
    b, l, d, N, uf, idx, marg, share, slots, rng = _serie(D, {"_parquet": pq}, 2026, 1, reps)
    sl, gr = _grupos_mun(b)
    real = share(l, d)
    Dm = np.empty((reps, K))
    for i in range(reps):
        o = _ordem_D(sl, gr, N, rng); Dm[i] = share(l[o], d[o])
    med = np.median(Dm, axis=0); sd = Dm.std(axis=0, ddof=1)
    c95 = float(np.quantile((np.abs(Dm[:, k10:] - med[k10:]) / sd[k10:]).max(axis=1), .95))
    z = np.abs(real - med)[k10:] / sd[k10:]
    fora = np.zeros(K, bool); fora[k10:] = z > c95
    t = b.DT_PRIM_TOT_PARCIAL_HOR_TSE.values[idx]                  # horario da totalizacao da secao no ponto k
    tt = pd.to_datetime(t)
    pts = pd.DataFrame(dict(ponto=np.arange(K), pct_secoes=100 * (np.arange(K) + 1) / K, horario=tt, fora_do_envelope=fora, desvio_pp=100 * (real - med)))
    pts.to_csv(os.path.join(saida, "A1T1_pontos.csv"), index=False)
    # corridas de pontos fora do envelope
    runs, i = [], 0
    while i < K:
        if fora[i]:
            j = i
            while j + 1 < K and fora[j + 1]:
                j += 1
            runs.append((i, j)); i = j + 1
        else:
            i += 1
    j19 = (tt >= pd.Timestamp("2026-10-04 19:00:00")) & (tt < pd.Timestamp("2026-10-04 20:00:00"))
    jan = np.asarray(j19)
    out = []
    for a, c in runs:
        out.append(dict(ponto_inicial=a, ponto_final=c, n_pontos=c - a + 1, pct_secoes_de=100 * (a + 1) / K, pct_secoes_ate=100 * (c + 1) / K, horario_de=str(tt[a]), horario_ate=str(tt[c]),
                        pontos_na_janela_19_a_20h=int(jan[a:c + 1].sum())))
    pd.DataFrame(out).to_csv(os.path.join(saida, "A1T1_corridas.csv"), index=False)
    resumo = dict(pontos_fora=int(fora.sum()), maior_corrida=_run(fora[k10:]), pontos_na_janela_19_a_20h=int(jan.sum()), pontos_fora_na_janela=int((fora & jan).sum()),
                  pct_fora_dentro_da_janela=100 * float((fora & jan).sum()) / max(1, int(fora.sum())), pct_pontos_na_janela=100 * float(jan.mean()),
                  horario_primeiro_fora=str(tt[fora].min()) if fora.any() else "", horario_ultimo_fora=str(tt[fora].max()) if fora.any() else "")
    pd.DataFrame([resumo]).to_csv(os.path.join(saida, "A1T1_resumo.csv"), index=False)
    # UFs que chegaram nos pontos fora do envelope (secoes entre o ponto inicial e final de cada corrida) contra todas
    pos = np.arange(N)
    marc = np.zeros(N, bool)
    for a, c in runs:
        lo = idx[a - 1] + 1 if a > 0 else 0
        marc[lo:idx[c] + 1] = True
    bb = b.assign(dentro=marc)
    tab = bb.groupby("SG_UF").agg(secoes=("dentro", "size"), nas_corridas=("dentro", "sum"))
    tab["pct_da_UF_nas_corridas"] = 100 * tab.nas_corridas / tab.secoes
    tab["pct_das_secoes_nas_corridas"] = 100 * tab.nas_corridas / max(1, tab.nas_corridas.sum())
    tab["pct_das_secoes_do_pais"] = 100 * tab.secoes / tab.secoes.sum()
    tab.sort_values("nas_corridas", ascending=False).round(2).to_csv(os.path.join(saida, "A1T1_ufs.csv"))
    # UFs cujas secoes tiveram a primeira totalizacao entre 19:00 e 20:00 (janela do congestionamento declarado)
    bb["na_janela"] = (bb.DT_PRIM_TOT_PARCIAL_HOR_TSE >= pd.Timestamp("2026-10-04 19:00:00")) & (bb.DT_PRIM_TOT_PARCIAL_HOR_TSE < pd.Timestamp("2026-10-04 20:00:00"))
    tj = bb.groupby("SG_UF").agg(secoes=("na_janela", "size"), na_janela=("na_janela", "sum"), lula_na_janela=("lula", lambda x: float(x[bb.loc[x.index, "na_janela"]].sum())),
                                 dir_na_janela=("dir", lambda x: float(x[bb.loc[x.index, "na_janela"]].sum())))
    tj["pct_da_UF_na_janela"] = 100 * tj.na_janela / tj.secoes
    tj["pct_das_secoes_da_janela"] = 100 * tj.na_janela / tj.na_janela.sum()
    tj["lula_pct_validos_na_janela"] = 100 * tj.lula_na_janela / (tj.lula_na_janela + tj.dir_na_janela)
    tj.drop(columns=["lula_na_janela", "dir_na_janela"]).sort_values("na_janela", ascending=False).round(2).to_csv(os.path.join(saida, "A1T1_ufs_janela.csv"))
    print(pd.DataFrame(out).to_string(), "\n", resumo, "\n", tab.sort_values("nas_corridas", ascending=False).head(8).round(1).to_string())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
