#!/usr/bin/env python3
"""A32b (Adendo 14): rajadas de liberacao manual com limiar absoluto. Rajada de k = k ou mais manuais consecutivas, sem biometrica entre elas, com intervalos entre habilitacoes consecutivas <= 1,5 x a mediana do
intervalo que precede as manuais da propria secao-dia (pelo menos 10 manuais). Variante: mediana nacional do ano e dia. Reusa a analise de 41_a32_rajadas.py.
Uso: python -I 43_a32b_rajadas_limiar_absoluto.py DIR_LOGS DIR_PARQUET DIR_AMOSTRA DIR_SAIDA"""
import glob
import importlib.util
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
spec = importlib.util.spec_from_file_location("r41", os.path.join(AQUI, "41_a32_rajadas.py")); r41 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r41)
KEY = r41.KEY
MIN_MANUAIS = 10
FATOR = 1.5


def medidas_abs(ts, tp, close_s, thr_nac):
    ts = np.asarray(ts); n = len(ts)
    gaps = np.diff(ts)
    tpl = np.frombuffer(tp.encode(), dtype="S1").astype(str) if tp else np.array([])
    isM = tpl == "M"; m = int(isM.sum())
    out = dict(n_hab=n, n_m=m, n_b=int((tpl == "B").sum()), n_o=int((tpl == "O").sum()), p5_gap_s=np.nan)
    ult = ts > close_s - 3600
    out["manual_ultima_hora"] = float(ult[isM].mean()) if m else np.nan
    out["hab_ultima_hora"] = float(ult.mean()) if n else np.nan
    if n < r41.NMIN or m < MIN_MANUAIS:
        return out
    arr = list(tp)
    pre = gaps[isM[1:]]
    for pref, thr in (("a", FATOR * float(np.median(pre))), ("h", FATOR * thr_nac)):
        lig = gaps <= thr
        out[f"thr_{pref}"] = thr
        for k in r41.KS:
            nb, inb = r41.rajadas(ts, arr, thr + 1e-9, k)
            out[f"{pref}{k}"], out[f"in_{pref}{k}"] = nb, inb
            e = r41.esperado_exato(lig, n, m, k)
            out[f"esp_{pref}{k}"] = e; out[f"p_ge1_{pref}{k}"] = 1 - float(np.exp(-e))
    return out


def main(dl, pq, damostra, saida):
    os.makedirs(saida, exist_ok=True)
    qq = pd.read_csv(os.path.join(saida, "A32_intervalos_por_tipo.csv"))
    nac = {(r.ano, r.turno): float(r.mediana) for r in qq[qq.tipo == "manual"].itertuples()}
    L = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(dl, "*.parquet")))], ignore_index=True)
    L = L[L.dia.isin([1, 2]) & L.ts.notna()].rename(columns={"uf": "SG_UF", "cd_municipio": "CD_MUNICIPIO", "zona": "NR_ZONA", "secao": "NR_SECAO"})
    bw = {}
    for a in (2022, 2026):
        for t in (1, 2):
            bw[(a, t)] = pd.read_parquet(os.path.join(pq, f"bu_{a}_t{t}.parquet"), columns=KEY + ["QT_APTOS", "QT_COMPARECIMENTO", "turnout", "lula_sh", "valid2", "lula", "ab_nominal_min", "uf_local", "manual_rate", "DS_TIPO_URNA"])
    linhas = []
    for (a, t), g in L.groupby(["ano", "dia"]):
        g = g.merge(bw[(a, t)][KEY + ["QT_COMPARECIMENTO", "ab_nominal_min"]], on=KEY, how="left")
        for r in g.itertuples():
            close = (r.ab_nominal_min + 540) * 60 if r.ab_nominal_min == r.ab_nominal_min else 17 * 3600
            m = medidas_abs(r.ts, r.tp, close, nac[(a, t)])
            linhas.append(dict(SG_UF=r.SG_UF, CD_MUNICIPIO=r.CD_MUNICIPIO, NR_ZONA=r.NR_ZONA, NR_SECAO=r.NR_SECAO, ano=a, turno=t, comparecimento_bu=r.QT_COMPARECIMENTO, **m))
    M = pd.DataFrame(linhas)
    est = pd.read_parquet(os.path.join(damostra, "amostra_estratos.parquet"))[KEY + ["estrato"]]
    est = est.groupby(KEY).estrato.agg(lambda s: "".join(sorted(set(s)))).reset_index()
    M = M.merge(est, on=KEY, how="left"); M["estrato"] = M.estrato.fillna("RR_completo")
    M["consistente"] = ((M.n_hab - M.comparecimento_bu).abs() <= r41.TOL * M.comparecimento_bu.clip(lower=1)) & (M.n_hab >= r41.NMIN)
    for pref in ("a", "h"):
        for k in r41.KS:
            M[f"ind{pref}{k}"] = (M[f"{pref}{k}"] >= 1).astype(float).where(M[f"{pref}{k}"].notna())
    M.to_parquet(os.path.join(damostra, "A32b_medidas_secao_dia.parquet"), index=False)
    c = M[M.consistente].groupby(["ano", "turno"]).agg(secoes_dia=("n_hab", "size"), com_10_manuais_ou_mais=("thr_a", lambda s: int(s.notna().sum())), limiar_mediano_s=("thr_a", "median"), limiar_nacional_s=("thr_h", "median")).reset_index()
    c.to_csv(os.path.join(saida, "A32b_cobertura.csv"), index=False)
    SAIDAS = {}
    r41.bloco_(M[M.thr_a.notna() | True], bw, "a", "_abs", "A32b", 3, saida, SAIDAS)
    r41.bloco_(M, bw, "h", "_abs_nac", "A32b-nac", 3, saida, SAIDAS)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    print(c.to_string())
    for pref, d in SAIDAS.items():
        print("=====", pref); print(d["PV"].round(3).T.to_string()); print(d["fr"].round(3).to_string()); print(d["mod"].round(4).to_string()); print(d["fam"].T.to_string() if len(d["fam"]) else "sem familia"); print(d["m3"].round(4).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:5])
