"""A18 (alteracao no meio): janela de congestionamento do 1o turno de 2026 e ordem de recebimento apos as 19h no 2o turno. Pre-registro: Adendo 7.
Registro proprio (familia Holm propria), para nao alterar o registro principal ja fechado."""
import os
import numpy as np
import pandas as pd
from lib_auditoria import KEY, NaoExecutado, base, fe_ols
from h1_h4 import tenta


def _com_recebimento(D, out, ano, turno):
    p = os.path.join(out["_parquet"], f"ordem_{ano}_t{turno}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"A18: falta {p}")
    o = pd.read_parquet(p)[KEY + ["DT_RECEBIMENTO_BU_HOR_TSE", "DT_PRIM_TOT_PARCIAL_HOR_TSE"]]
    w = base(D[(ano, turno)]).merge(o, on=KEY, how="inner")
    w = w[w.DT_RECEBIMENTO_BU_HOR_TSE.notna()].copy()
    dia = w.DT_RECEBIMENTO_BU_HOR_TSE.dt.date.mode().iloc[0]
    w = w[w.DT_RECEBIMENTO_BU_HOR_TSE.dt.date == dia].copy()
    w["log_aptos"] = np.log(w.QT_APTOS)
    w["h_rec"] = w.DT_RECEBIMENTO_BU_HOR_TSE.dt.hour + w.DT_RECEBIMENTO_BU_HOR_TSE.dt.minute / 60
    w["lag_min"] = (w.DT_PRIM_TOT_PARCIAL_HOR_TSE - w.DT_RECEBIMENTO_BU_HOR_TSE).dt.total_seconds() / 60
    return w, dia


def _rsq(w, g):
    sst = ((w.t - w.t.mean()) ** 2).sum()
    return float(1 - ((w.t - w.groupby(g).t.transform("mean")) ** 2).sum() / sst)


def a18(D, reg, out):
    rega = out["_reg_a18"]
    # ----- A18a: janela 19:00 a 19:59 no 1o turno
    resa, resumo = {}, []
    for ano in (2026, 2022, 2018):
        w, dia = _com_recebimento(D, out, ano, 1)
        w["janela"] = ((w.h_rec >= 19) & (w.h_rec < 20)).astype(float)
        xs = ["janela", "turnout", "log_aptos", "atraso_min"]
        for y in ("lula_sh", "dir_sh"):
            r = tenta(out, f"A18a {ano} {y}", fe_ols, w, y, xs, "uf_local")
            resa[(ano, y)] = r
            if r is not None:
                resumo.append(dict(ano=ano, resposta=y, secoes=len(w), secoes_na_janela=int(w.janela.sum()), pct_na_janela=100 * w.janela.mean(),
                                   coef_janela=float(r.loc["janela", "coef"]), ep=float(r.loc["janela", "se"])))
        if ano == 2026:
            w26 = w
            # robustez: janela pela defasagem recepcao->totalizacao acima do p90 do dia
            p90 = w.lag_min.quantile(0.9)
            w["janela_lag"] = (w.lag_min > p90).astype(float)
            for y in ("lula_sh", "dir_sh"):
                r = tenta(out, f"A18a robustez lag {y}", fe_ols, w, y, ["janela_lag", "turnout", "log_aptos", "atraso_min"], "uf_local")
                if r is not None:
                    resumo.append(dict(ano=ano, resposta=y + " (robustez: defasagem > p90)", secoes=len(w), secoes_na_janela=int(w.janela_lag.sum()), pct_na_janela=100 * w.janela_lag.mean(),
                                       coef_janela=float(r.loc["janela_lag", "coef"]), ep=float(r.loc["janela_lag", "se"])))
            # consistencia: nominais + brancos + nulos = comparecimento
            w["incons"] = ((w.nominal + w.branco + w.nulo) != w.QT_COMPARECIMENTO).astype(int)
            out["a18a_consistencia"] = w.groupby("janela").agg(secoes=("incons", "size"), com_inconsistencia=("incons", "sum")).reset_index()
            h = w.DT_RECEBIMENTO_BU_HOR_TSE.dt.floor("30min").value_counts().sort_index()
            out["a18a_recebimento_por_30min_2026T1"] = pd.DataFrame({"inicio": h.index.strftime("%H:%M"), "secoes": h.values, "pct": 100 * h.values / len(w)})
    out["a18a_resumo"] = pd.DataFrame(resumo)
    for y, sent, nome in (("lula_sh", "PT", "Lula"), ("dir_sh", "OPO", "oponente")):
        if resa.get((2026, y)) is None:
            raise NaoExecutado(f"A18a: {y} 2026 nao estimado")
        pl = [(f"{a}/T1", float(resa[(a, y)].loc["janela", "coef"]), float(resa[(a, y)].loc["janela", "se"])) for a in (2022, 2018) if resa.get((a, y)) is not None]
        rega.add("A18a", f"1o turno 2026: BU recebido entre 19h e 20h: participacao de {nome} nos validos, EF de local", float(resa[(2026, y)].loc["janela", "coef"]),
                 float(resa[(2026, y)].loc["janela", "se"]), pl, expo=float(w26[w26.janela == 1].valid2.sum()), fator=2.0, sentido=sent,
                 nota="janela fixada pelo relogio (Adendo 7); placebos: mesma janela de relogio em 2022/T1 e 2018/T1")

    # ----- A18b: ordem de recebimento depois das 19h
    resb, linhas, var = {}, [], []
    specs = [(2026, 2), (2022, 2), (2018, 2), (2026, 1)]
    for ano, t in specs:
        w, dia = _com_recebimento(D, out, ano, t)
        w = w[w.h_rec >= 19].copy()
        w["t"] = w.h_rec - 19
        if t == 2:
            t1 = D[(ano, 1)][KEY + ["lula_sh", "dir_sh"]].rename(columns={"lula_sh": "lula_sh_t1", "dir_sh": "dir_sh_t1"})
            w = w.merge(t1, on=KEY, how="inner")
        for y in ("lula_sh", "dir_sh"):
            xs = ["t", "turnout", "log_aptos", "atraso_min"] + ([f"{y}_t1"] if t == 2 else [])
            r = tenta(out, f"A18b {ano}/T{t} {y}", fe_ols, w, y, xs, "uf_local")
            resb[(ano, t, y)] = (r, w)
            if r is not None:
                linhas.append(dict(ano=ano, turno=t, resposta=y, secoes_apos_19h=len(w), coef_por_hora=float(r.loc["t", "coef"]), ep=float(r.loc["t", "se"])))
        var.append(dict(ano=ano, turno=t, secoes_apos_19h=len(w), r2_horario_por_UF=_rsq(w, "SG_UF"), r2_horario_por_municipio=_rsq(w.assign(mun=w.SG_UF + "_" + w.CD_MUNICIPIO.astype(str)), "mun"),
                        horas_mediana_apos_19h=float(w.t.median())))
    out["a18b_resumo"] = pd.DataFrame(linhas)
    out["a18b_variancia_do_horario"] = pd.DataFrame(var)
    for y, sent, nome in (("lula_sh", "PT", "Lula"), ("dir_sh", "OPO", "oponente")):
        a = resb.get((2026, 2, y))
        if a is None or a[0] is None:
            raise NaoExecutado(f"A18b: {y} 2026/T2 nao estimado")
        r, w = a
        pl = [(f"{ano}/T{t}", float(resb[(ano, t, y)][0].loc["t", "coef"]), float(resb[(ano, t, y)][0].loc["t", "se"])) for ano, t in specs[1:] if resb.get((ano, t, y)) and resb[(ano, t, y)][0] is not None]
        rega.add("A18b", f"2o turno 2026: horas de atraso no recebimento depois das 19h: participacao de {nome} nos validos, EF de local", float(r.loc["t", "coef"]), float(r.loc["t", "se"]), pl,
                 expo=float(w.valid2.sum()), fator=2.0, sentido=sent, nota="exposicao: efeito de 1 hora de diferenca de recebimento sobre as secoes recebidas depois das 19h (convencao do Adendo 7)")
