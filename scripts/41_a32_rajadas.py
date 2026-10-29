#!/usr/bin/env python3
"""A32 (Adendo 11 e 11a), item 1: rajadas de liberacao manual, fracao na ultima hora e associacao com comparecimento e voto, a partir das sequencias de habilitacao extraidas por 38_a32_extrai_logs.py.
Uso: python -I 41_a32_rajadas.py DIR_LOGS DIR_PARQUET DIR_AMOSTRA DIR_URNA_OUT DIR_SAIDA"""
import glob
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, Registro, fe_ols, MARGEM

NMIN = 100
TOL = 0.05
KS = (3, 5)


def rajadas(ts, tp, p5, k):
    """Numero de rajadas (k ou mais manuais consecutivas, todos os intervalos < p5) e manuais dentro delas."""
    nb = inb = 0
    run = 0
    n = len(tp)
    for i in range(n):
        if tp[i] == "M" and (run == 0 or (ts[i] - ts[i - 1]) < p5):
            run += 1
        elif tp[i] == "M":
            if run >= k:
                nb += 1; inb += run
            run = 1
        else:
            if run >= k:
                nb += 1; inb += run
            run = 0
    if run >= k:
        nb += 1; inb += run
    return nb, inb


def esperado_exato(gaps_ligados, n, m, k):
    """Esperanca do numero de rajadas de k ou mais sobre todas as permutacoes dos rotulos (Adendo 11b)."""
    def f(sz):
        if m < sz:
            return 0.0
        r = 1.0
        for i in range(sz):
            r *= (m - i) / (n - i)
        return r
    fk, fk1 = f(k), f(k + 1)
    esp = 0.0
    lc = 1
    for lig in list(gaps_ligados) + [False]:
        if lig:
            lc += 1
        else:
            if lc >= k:
                esp += fk + (lc - k) * (fk - fk1)
            lc = 1
    return esp


def medidas(ts, tp, close_s):
    ts = np.asarray(ts); n = len(ts)
    gaps = np.diff(ts)
    p5 = float(np.percentile(gaps, 5)) if len(gaps) else np.nan
    tpl = np.frombuffer(tp.encode(), dtype="S1").astype(str) if tp else np.array([])
    isM = tpl == "M"
    out = dict(n_hab=n, n_m=int(isM.sum()), n_b=int((tpl == "B").sum()), n_o=int((tpl == "O").sum()), p5_gap_s=p5)
    ult = ts > close_s - 3600
    out["manual_ultima_hora"] = float(ult[isM].mean()) if isM.sum() else np.nan
    out["hab_ultima_hora"] = float(ult.mean()) if n else np.nan
    if n < NMIN:
        return out
    arr = list(tp)
    lig = gaps < p5
    m = int(isM.sum())
    for k in KS:
        nb, inb = rajadas(ts, arr, p5, k)
        out[f"b{k}"], out[f"in_b{k}"] = nb, inb
        e = esperado_exato(lig, n, m, k)
        out[f"esp_b{k}"] = e; out[f"p_ge1_b{k}"] = 1 - float(np.exp(-e))
    return out


def carrega_logs(dl, pq):
    L = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(dl, "*.parquet")))], ignore_index=True)
    L = L[L.dia.isin([1, 2]) & L.ts.notna()].rename(columns={"uf": "SG_UF", "cd_municipio": "CD_MUNICIPIO", "zona": "NR_ZONA", "secao": "NR_SECAO"})
    bw = {}
    for a in (2022, 2026):
        for t in (1, 2):
            d = pd.read_parquet(os.path.join(pq, f"bu_{a}_t{t}.parquet"), columns=KEY + ["QT_APTOS", "QT_COMPARECIMENTO", "turnout", "lula_sh", "valid2", "lula", "ab_nominal_min", "uf_local", "manual_rate", "DS_TIPO_URNA"])
            bw[(a, t)] = d.rename(columns={c: f"{c}" for c in d.columns})
    linhas = []
    for (a, t), g in L.groupby(["ano", "dia"]):
        b = bw[(a, t)][KEY + ["QT_COMPARECIMENTO", "ab_nominal_min"]]
        g = g.merge(b, on=KEY, how="left")
        for r in g.itertuples():
            close = (r.ab_nominal_min + 540) * 60 if r.ab_nominal_min == r.ab_nominal_min else 17 * 3600
            m = medidas(r.ts, r.tp, close)
            linhas.append(dict(SG_UF=r.SG_UF, CD_MUNICIPIO=r.CD_MUNICIPIO, NR_ZONA=r.NR_ZONA, NR_SECAO=r.NR_SECAO, ano=a, turno=t, comparecimento_bu=r.QT_COMPARECIMENTO, **m))
    return pd.DataFrame(linhas), bw


def main(dl, pq, damostra, durna, saida):
    os.makedirs(saida, exist_ok=True)
    M, bw = carrega_logs(dl, pq)
    est = pd.read_parquet(os.path.join(damostra, "amostra_estratos.parquet"))[KEY + ["estrato"]]
    est = est.groupby(KEY).estrato.agg(lambda s: "".join(sorted(set(s)))).reset_index()
    M = M.merge(est, on=KEY, how="left")
    M["estrato"] = M.estrato.fillna("RR_completo")
    M["consistente"] = ((M.n_hab - M.comparecimento_bu).abs() <= TOL * M.comparecimento_bu.clip(lower=1)) & (M.n_hab >= NMIN)
    M["share_manual"] = M.n_m / M.n_hab
    for k in KS:
        M[f"ind{k}"] = (M[f"b{k}"] >= 1).astype(float).where(M[f"b{k}"].notna())
    M.to_parquet(os.path.join(damostra, "A32_medidas_secao_dia.parquet"), index=False)
    # --- prevalencia por ano e dia
    pv = []
    for (a, t), g in M[M.consistente].groupby(["ano", "turno"]):
        for estr, gg in (("todos", g), ("R + RR completo (principal)", g[g.estrato.str.contains("R")]), ):
            row = dict(ano=a, turno=t, amostra=estr, secoes_dia=len(gg), mediana_hab=float(gg.n_hab.median()), pct_manual=100 * float(gg.n_m.sum() / gg.n_hab.sum()),
                       manual_ultima_hora_media=float(gg.manual_ultima_hora.mean()), hab_ultima_hora_media=float(gg.hab_ultima_hora.mean()),
                       dif_manual_menos_todas_ultima_hora=float((gg.manual_ultima_hora - gg.hab_ultima_hora).mean()), ep_dif=float((gg.manual_ultima_hora - gg.hab_ultima_hora).std(ddof=1) / np.sqrt(gg.manual_ultima_hora.notna().sum())))
            for k in KS:
                row[f"pct_secoes_com_rajada_k{k}"] = 100 * float(gg[f"ind{k}"].mean()); row[f"rajadas_k{k}_total"] = int(gg[f"b{k}"].sum())
                row[f"esperado_pct_com_rajada_k{k}_permutacao"] = 100 * float(gg[f"p_ge1_b{k}"].mean())
                row[f"razao_obs_esp_rajadas_k{k}"] = float(gg[f"b{k}"].sum() / gg[f"esp_b{k}"].sum()) if gg[f"esp_b{k}"].sum() > 0 else np.nan
            pv.append(row)
    PV = pd.DataFrame(pv); PV.to_csv(os.path.join(saida, "A32_rajadas_prevalencia.csv"), index=False)
    cons = M.groupby(["ano", "turno"]).agg(secoes_dia=("n_hab", "size"), consistentes=("consistente", "sum"), n_hab_menor_100=("n_hab", lambda s: int((s < NMIN).sum()))).reset_index(); cons.to_csv(os.path.join(saida, "A32_logs_cobertura.csv"), index=False)

    # --- frequencia 2026 x 2022 nas mesmas secoes (efeito fixo de secao)
    reg = Registro(); fr = []
    for t in (1, 2):
        w = M[M.consistente & (M.turno == t)]
        for k in KS:
            x = w[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "ano", f"ind{k}"]].dropna()
            x["a26"] = (x.ano == 2026).astype(float); x["sec"] = x.SG_UF + "_" + x.CD_MUNICIPIO.astype(str) + "_" + x.NR_ZONA.astype(str) + "_" + x.NR_SECAO.astype(str); x["mun"] = x.SG_UF + "_" + x.CD_MUNICIPIO.astype(str)
            both = x.groupby("sec").ano.transform("nunique") == 2
            try:
                r = fe_ols(x[both], f"ind{k}", ["a26"], "sec", "mun").iloc[0]
                fr.append(dict(turno=t, k=k, secoes_nos_dois_anos=int(x[both].sec.nunique()), diferenca_2026_menos_2022_em_pontos_de_proporcao=float(100 * r.coef), ep=float(100 * r.se), z=float(r.coef / r.se), p=float(r.p)))
            except ValueError as e:
                fr.append(dict(turno=t, k=k, erro=str(e)))
    pd.DataFrame(fr).to_csv(os.path.join(saida, "A32_rajadas_frequencia_2026_vs_2022.csv"), index=False)

    # --- associacao com comparecimento e voto (2o turno), amostra principal e sensibilidade
    def junta(a):
        w = M[M.consistente & (M.turno == 2) & (M.ano == a)]
        t2 = bw[(a, 2)][KEY + ["turnout", "lula_sh", "uf_local", "valid2", "DS_TIPO_URNA"]]; t1 = bw[(a, 1)][KEY + ["turnout", "lula_sh"]].rename(columns={"turnout": "turnout_t1", "lula_sh": "lula_sh_t1"})
        w = w.merge(t2, on=KEY, how="left").merge(t1, on=KEY, how="left")
        return w[w.DS_TIPO_URNA.str.upper().eq("APURADA") & (w.valid2 >= 30)]
    A = {a: junta(a) for a in (2022, 2026)}
    expo_v = float(bw[(2026, 2)].loc[bw[(2026, 2)].SG_UF != "ZZ", "valid2"].sum()); expo_a = float(bw[(2026, 2)].loc[bw[(2026, 2)].SG_UF != "ZZ", "QT_APTOS"].sum())
    mod = []
    for amostra, filtro in (("principal: R + Roraima completa", lambda w: w[w.estrato.str.contains("R")]), ("sensibilidade: todos os estratos (selecao no desfecho)", lambda w: w)):
        for k in KS:
            for y, xs, nome, sent, fator, expo in (("turnout", [f"ind{k}", "turnout_t1"], "comparecimento", "PT+OPO", 1.0, expo_a), ("lula_sh", [f"ind{k}", "lula_sh_t1"], "participacao de Lula", "PT", 2.0, expo_v)):
                try:
                    r26 = fe_ols(filtro(A[2026]).dropna(subset=[f"ind{k}"]), y, xs, "uf_local").iloc[0]
                    r22 = fe_ols(filtro(A[2022]).dropna(subset=[f"ind{k}"]), y, xs, "uf_local").iloc[0]
                except ValueError as e:
                    mod.append(dict(amostra=amostra, k=k, desfecho=nome, erro=str(e))); continue
                mod.append(dict(amostra=amostra, k=k, desfecho=nome, coef_2026=float(r26.coef), ep_2026=float(r26.se), coef_2022_placebo=float(r22.coef), ep_2022=float(r22.se), n_2026=int(r26.n), locais_2026=int(r26.grupos)))
                if amostra.startswith("principal") and k == 3:
                    reg.add("A32", f"rajada de liberacao manual (k = {k}) e {nome}: 2026/T2 contra 2022/T2 (EF de local, controle do T1)", float(r26.coef), float(r26.se), [("2022/T2", float(r22.coef), float(r22.se))], expo=expo, fator=fator, sentido=sent,
                            nota=f"{int(r26.n)} secoes, {int(r26.grupos)} locais; amostra principal (R + Roraima); teto = extrapolacao do coeficiente para todo o pais, so limite superior")
    pd.DataFrame(mod).to_csv(os.path.join(saida, "A32_rajadas_modelos.csv"), index=False)
    fam = reg.frame(); fam.to_csv(os.path.join(saida, "A32_rajadas_testes.csv"), index=False)

    # M3 (descritiva): variacao 2022 -> 2026 do comparecimento do T2 contra a rajada de 2026
    a26, a22 = A[2026], A[2022][KEY + ["turnout"]].rename(columns={"turnout": "turnout_2022"})
    w = a26.merge(a22, on=KEY, how="inner"); w["dturn"] = w.turnout - w.turnout_2022
    m3 = []
    for amostra, filtro in (("principal: R + Roraima completa", lambda x: x[x.estrato.str.contains("R")]), ("todos os estratos (selecao no desfecho)", lambda x: x)):
        for k in KS:
            try:
                r = fe_ols(filtro(w).dropna(subset=[f"ind{k}", "dturn"]), "dturn", [f"ind{k}"], "uf_local").iloc[0]
                m3.append(dict(amostra=amostra, k=k, coef=float(r.coef), ep=float(r.se), p=float(r.p), n=int(r.n)))
            except ValueError as e:
                m3.append(dict(amostra=amostra, k=k, erro=str(e)))
    pd.DataFrame(m3).to_csv(os.path.join(saida, "A32_rajadas_M3_descritiva.csv"), index=False)

    # --- item 4: hash do log na lista assinada (amostra de A4/A5)
    hs = []
    for a in (2022, 2026):
        d = pd.concat([pd.read_parquet(f) for f in glob.glob(os.path.join(durna, f"*_{a}_t2.parquet"))], ignore_index=True)
        d = d[d.get("erro_arquivos").isna()] if "erro_arquivos" in d else d
        v = d.log_hash_na_lista.dropna()
        hs.append(dict(ano=a, secoes_lidas=len(d), log_hash_na_lista_verdadeiro=int(v.sum()), log_hash_na_lista_falso=int((~v.astype(bool)).sum()), pct=100 * float(v.astype(bool).mean()),
                       lista_hash_ok=int(d.lista_hash_ok.sum()) if "lista_hash_ok" in d else np.nan))
    pd.DataFrame(hs).to_csv(os.path.join(saida, "A32_hash_log_na_lista.csv"), index=False)
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 50)
    print(cons.to_string()); print(PV.round(3).T.to_string()); print(pd.DataFrame(fr).round(3).to_string()); print(pd.DataFrame(mod).round(4).to_string()); print(fam.T.to_string() if len(fam) else "sem familia"); print(pd.DataFrame(m3).round(4).to_string()); print(pd.DataFrame(hs).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:6])
