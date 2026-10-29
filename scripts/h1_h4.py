"""H1 a H4: liberacao manual (biometria), aumento da liberacao, encerramento e secoes tardias."""
import sys
import numpy as np
import pandas as pd
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, par_ano, fe_ols

BINS = [0, .05, .10, .20, .50, 1.01]
NOMES_BIN = ["0-5%", "5-10%", "10-20%", "20-50%", ">50%"]


def tenta(out, rotulo, fn, *a, **k):
    """Roda fn; se falhar, imprime erro em stderr, registra em out['nao_executados'] e devolve None (nunca em silencio)."""
    try:
        return fn(*a, **k)
    except (ValueError, NaoExecutado, KeyError) as e:
        msg = f"NAO EXECUTADO [{rotulo}]: {type(e).__name__}: {e}"
        print(msg, file=sys.stderr, flush=True)
        out.setdefault("nao_executados", []).append((rotulo, str(e)))
        return None


def _b(r, x):
    return float(r.loc[x, "coef"]), float(r.loc[x, "se"])


# ----------------------------------------------------------------------------------------------- H1
def h1(D, reg, out):
    W = {a: par_ano(D, a) for a in (2022, 2026)}
    W = {a: w[w.manual_rate.notna()] for a, w in W.items()}
    for a, w in W.items():
        if len(w) == 0 or w.manual_rate.isna().all():
            raise NaoExecutado(f"sem taxa de liberacao manual em {a}")
    # S1: T2 com defasagem (voto da propria secao no T1), EF de local
    s1 = {a: fe_ols(w, "lula_sh", ["manual_rate", "lula_sh_t1"], "uf_local") for a, w in W.items()}
    # S0: sem defasagem, 4 eleicoes
    s0 = {}
    for a in (2022, 2026):
        for t in (1, 2):
            d = base(D[(a, t)])
            d = d[d.manual_rate.notna()]
            s0[(a, t)] = fe_ols(d, "lula_sh", ["manual_rate"], "uf_local")
    # red team: a associacao S0 de 2026 sobrevive a controles de tamanho da secao e comparecimento?
    s0c = {}
    for a in (2022, 2026):
        for t in (1, 2):
            d = base(D[(a, t)]); d = d[d.manual_rate.notna()].assign(laptos=lambda z: np.log(z.QT_APTOS))
            s0c[(a, t)] = fe_ols(d, "lula_sh", ["manual_rate", "turnout", "laptos"], "uf_local")
    out["h1_s0_com_controles"] = pd.DataFrame([dict(ano=a, turno=t, coef_manual=r.loc["manual_rate", "coef"], ep=r.loc["manual_rate", "se"],
                                                    coef_turnout=r.loc["turnout", "coef"], coef_log_aptos=r.loc["laptos", "coef"]) for (a, t), r in s0c.items()])
    linhas = []
    for (a, t), r in s0.items():
        linhas.append(dict(spec="S0 sem defasagem", ano=a, turno=t, coef=r.coef.iloc[0], ep=r.se.iloc[0], p=r.p.iloc[0], n=r.n.iloc[0], locais=r.grupos.iloc[0]))
    for a, r in s1.items():
        linhas.append(dict(spec="S1 T2 com defasagem T1", ano=a, turno=2, coef=r.loc["manual_rate", "coef"], ep=r.loc["manual_rate", "se"],
                           p=r.loc["manual_rate", "p"], n=r.loc["manual_rate", "n"], locais=r.loc["manual_rate", "grupos"]))
    out["h1_coef"] = pd.DataFrame(linhas)

    w26 = W[2026]
    expo = float((w26.manual_rate * w26.valid2).sum()) * D[(2026, 2)].valid2.sum() / w26.valid2.sum()
    out["h1_exposicao_votos_manuais_equiv"] = expo

    b26, se26 = _b(s1[2026], "manual_rate"); b22, se22 = _b(s1[2022], "manual_rate")
    reg.add("H1", "S1 T2 com lag T1, Lula% ~ taxa manual", b26, se26, [("2022/T2", b22, se22)], expo,
            nota="coef = variacao do share de Lula por unidade de taxa manual, dado o voto da secao no T1")
    b26, se26 = _b(s0[(2026, 2)], "manual_rate")
    pl = [_b(s0[k], "manual_rate") for k in ((2022, 1), (2022, 2), (2026, 1))]
    reg.add("H1", "S0 sem lag, Lula% ~ taxa manual", b26, se26,
            [("2022/T1", *pl[0]), ("2022/T2", *pl[1]), ("2026/T1", *pl[2])], expo)

    b26c, se26c = _b(s0c[(2026, 2)], "manual_rate")
    reg.add("H1", "S0 sem lag + controles (comparecimento, log aptos)", b26c, se26c,
            [(f"{a}/T{t}", *_b(s0c[(a, t)], "manual_rate")) for (a, t) in ((2022, 1), (2022, 2), (2026, 1))], expo)
    # simetria: redutos de Flavio (<40% Lula no T1) e redutos de Lula (>60%)
    for nome, filt in (("reduto de Flavio (Lula T1<40%)", lambda w: w.lula_sh_t1 < .4),
                       ("reduto de Lula (Lula T1>60%)", lambda w: w.lula_sh_t1 > .6)):
        r26 = tenta(out, f"H1 {nome} 2026", fe_ols, W[2026][filt(W[2026])], "lula_sh", ["manual_rate", "lula_sh_t1"], "uf_local")
        r22 = tenta(out, f"H1 {nome} 2022", fe_ols, W[2022][filt(W[2022])], "lula_sh", ["manual_rate", "lula_sh_t1"], "uf_local")
        if r26 is not None and r22 is not None:
            b26, se26 = _b(r26, "manual_rate"); b22, se22 = _b(r22, "manual_rate")
            ww = W[2026][filt(W[2026])]
            reg.add("H1", f"S1 {nome}", b26, se26, [("2022/T2", b22, se22)], float((ww.manual_rate * ww.valid2).sum()))
    # simetria: votos por apto de cada candidato
    for nome, y, ylag, fator in (("Lula votos/apto", "lula_pa", "lula_pa_t1", 1.0), ("Flavio/Bolsonaro votos/apto", "dir_pa", "dir_pa_t1", 1.0)):
        r26 = fe_ols(W[2026], y, ["manual_rate", ylag], "uf_local"); r22 = fe_ols(W[2022], y, ["manual_rate", ylag], "uf_local")
        b26, se26 = _b(r26, "manual_rate"); b22, se22 = _b(r22, "manual_rate")
        ex = float((W[2026].manual_rate * W[2026].QT_APTOS).sum())
        reg.add("H1", f"S1 {nome}", b26, se26, [("2022/T2", b22, se22)], ex, fator=fator,
                nota="votos adicionais do candidato; efeito em margem <= esse valor", sentido="PT" if y == "lula_pa" else "OPO")

    _h1_redteam(D, W, out)

    # dose-resposta
    linhas = []
    for a, w in W.items():
        w = w.copy()
        for i, nm in enumerate(NOMES_BIN[1:], 1):
            w[f"b{i}"] = ((w.manual_rate >= BINS[i]) & (w.manual_rate < BINS[i + 1])).astype(float)
        w["b34"] = w[["b3", "b4"]].max(axis=1)
        xs = ["b1", "b2", "b3", "b4"]
        r = fe_ols(w, "lula_sh", xs + ["lula_sh_t1"], "uf_local")
        for i, x in enumerate(xs):
            linhas.append(dict(ano=a, faixa=NOMES_BIN[i + 1], coef_pp=100 * r.loc[x, "coef"], ep_pp=100 * r.loc[x, "se"], secoes_na_faixa=int(w[x].sum())))
        if a == 2026:
            r26x = fe_ols(w, "lula_sh", ["b34", "lula_sh_t1"], "uf_local")
        else:
            r22x = fe_ols(w, "lula_sh", ["b34", "lula_sh_t1"], "uf_local")
    out["h1_dose"] = pd.DataFrame(linhas)
    b26, se26 = _b(r26x, "b34"); b22, se22 = _b(r22x, "b34")
    n34 = W[2026][W[2026].manual_rate >= .20]
    reg.add("H1", "S1 dose: taxa manual >= 20% vs <20% (share de Lula)", b26, se26, [("2022/T2", b22, se22)],
            float(n34.valid2.sum()), nota=f"{len(n34)} secoes com >=20% em 2026/T2")


# ----------------------------------------------------------------------------------------------- H2
def _mun_bio(d):
    g = d.groupby(["SG_UF", "CD_MUNICIPIO"]).biom_nh.sum()
    return set(g[g > 0].index)


def h2(D, reg, out):
    ok = _mun_bio(D[(2022, 2)]) & _mun_bio(D[(2026, 2)])
    linhas = []
    for filtro, rotulo in ((False, "sem filtro"), (True, "so municipios com biometria nos 2 anos")):
        for t in (1, 2):
            a = base(D[(2022, t)]).set_index(KEY); b = base(D[(2026, t)]).set_index(KEY)
            m = b.join(a[["manual_rate", "QT_APTOS", "QT_COMPARECIMENTO", "biom_nh", "lula_sh", "valid2"]], rsuffix="_22", how="inner").reset_index()
            m = m[m.QT_APTOS_22 > 0]
            m = m[(m.QT_APTOS / m.QT_APTOS_22).between(.85, 1.15)]
            if filtro:
                m = m[[(u, c) in ok for u, c in zip(m.SG_UF, m.CD_MUNICIPIO)]]
            m = m[m.manual_rate.notna() & m.manual_rate_22.notna()]
            d = m.manual_rate - m.manual_rate_22
            linhas.append(dict(filtro=rotulo, turno=t, secoes=len(m), taxa_agregada_2022=m.biom_nh_22.sum() / m.QT_COMPARECIMENTO_22.sum(),
                               taxa_agregada_2026=m.biom_nh.sum() / m.QT_COMPARECIMENTO.sum(), media_delta_pp=100 * d.mean(), mediana_delta_pp=100 * d.median(),
                               pct_secoes_subiu_mais_5pp=100 * (d > .05).mean(), pct_secoes_caiu_mais_5pp=100 * (d < -.05).mean()))
    out["h2_descritivo"] = pd.DataFrame(linhas)
    tot = []
    for (a, t), d in sorted(D.items()):
        if a >= 2018:
            tot.append(dict(ano=a, turno=t, biom_nh_total=int(d.biom_nh.sum()), comparecimento_total=int(d.QT_COMPARECIMENTO.sum()),
                            taxa_agregada=d.biom_nh.sum() / d.QT_COMPARECIMENTO.sum(), secoes=len(d)))
    out["h2_totais_absolutos"] = pd.DataFrame(tot)
    # onde subiu: por UF (T2, secoes estaveis pareadas)
    a = base(D[(2022, 2)]).set_index(KEY); b = base(D[(2026, 2)]).set_index(KEY)
    m = b.join(a[["manual_rate", "QT_APTOS"]], rsuffix="_22", how="inner").reset_index()
    m = m[(m.QT_APTOS / m.QT_APTOS_22.replace(0, np.nan)).between(.85, 1.15) & m.manual_rate.notna() & m.manual_rate_22.notna()]
    m["delta_pp"] = 100 * (m.manual_rate - m.manual_rate_22)
    out["h2_por_uf"] = m.groupby("SG_UF").agg(secoes=("delta_pp", "size"), media_2022=("manual_rate_22", "mean"), media_2026=("manual_rate", "mean"),
                                              delta_medio_pp=("delta_pp", "mean")).round(4).sort_values("delta_medio_pp", ascending=False)
    # associacao com variacao de voto
    # (i) dentro do ano: delta(T1->T2) do share de Lula ~ delta da taxa manual
    est = {}
    for ano in (2022, 2026):
        w = par_ano(D, ano)
        w = w[w.manual_rate.notna() & w.manual_rate_t1.notna()].copy()
        w["d_lula"] = w.lula_sh - w.lula_sh_t1
        w["d_man"] = w.manual_rate - w.manual_rate_t1
        est[ano] = (fe_ols(w, "d_lula", ["d_man"], "uf_local"), w)
    (r26, w26), (r22, _) = est[2026], est[2022]
    b26, se26 = _b(r26, "d_man"); b22, se22 = _b(r22, "d_man")
    expo = float((w26.d_man.clip(lower=0) * w26.valid2).sum())
    reg.add("H2", "delta voto Lula (T1->T2) ~ delta taxa manual, dentro do ano", b26, se26, [("2022 (T1->T2)", b22, se22)], expo,
            nota="exposicao = soma(max(delta manual,0) x validos)")
    # (ii) entre anos (22->26), T2 contra T1 como placebo, secoes estaveis, municipios com biometria nos 2 anos
    res = {}
    for t in (2, 1):
        a = base(D[(2022, t)]).set_index(KEY); b = base(D[(2026, t)])
        m = b.join(a[["manual_rate", "QT_APTOS", "lula_sh"]], on=KEY, rsuffix="_22", how="inner")
        m = m[(m.QT_APTOS / m.QT_APTOS_22.replace(0, np.nan)).between(.85, 1.15) & m.manual_rate.notna() & m.manual_rate_22.notna()]
        m = m[[(u, c) in ok for u, c in zip(m.SG_UF, m.CD_MUNICIPIO)]].copy()
        m["d_lula"] = m.lula_sh - m.lula_sh_22
        m["d_man"] = m.manual_rate - m.manual_rate_22
        res[t] = (fe_ols(m, "d_lula", ["d_man"], "uf_local"), m)
    (r2, m2), (r1, _) = res[2], res[1]
    b2, s2 = _b(r2, "d_man"); b1, s1 = _b(r1, "d_man")
    expo = float((m2.d_man.clip(lower=0) * m2.valid2).sum())
    reg.add("H2", "delta voto Lula (2022->2026) ~ delta taxa manual, T2", b2, s2, [("mesmo teste no T1", b1, s1)], expo,
            nota="municipios com biometria nos 2 anos; T1 2026 tem outros candidatos, placebo imperfeito")


# ----------------------------------------------------------------------------------------------- H3
CATS = [("ate 5 min apos 17h", -1e9, 5), ("5 a 15 min (17h01-17h15)", 5, 15), ("15 a 115 min (17h16-18h54)", 15, 115), ("115+ min (>= ~19h)", 115, 1e9)]


def h3(D, reg, out):
    linhas = []
    for (a, t), d in sorted(D.items()):
        if a < 2018:
            continue
        for ext, rot in ((False, "Brasil sem exterior"), (True, "so exterior")):
            x = d[(d.SG_UF == "ZZ") == ext]
            x = x[x.atraso_min.notna()]
            for nome, lo, hi in CATS:
                s = x[(x.atraso_min > lo) & (x.atraso_min <= hi)] if lo > -1e8 else x[x.atraso_min <= hi]
                linhas.append(dict(ano=a, turno=t, recorte=rot, faixa=nome, secoes=len(s), pct_secoes=100 * len(s) / max(len(x), 1),
                                   aptos=int(s.QT_APTOS.sum()), comparecimento=int(s.QT_COMPARECIMENTO.sum())))
    out["h3_faixas"] = pd.DataFrame(linhas)
    # recontagem da tabela do relatorio: relogio CRU da urna (DT_ENCERRAMENTO hh:mm, sem ajustar fuso), com e sem exterior
    cru = []
    for (a, t), d in sorted(D.items()):
        if a < 2018:
            continue
        for ext, rot in ((True, "com exterior"), (False, "sem exterior")):
            x = d[d.DT_ENCERRAMENTO.notna()]
            if not ext:
                x = x[x.SG_UF != "ZZ"]
            m = x.DT_ENCERRAMENTO.dt.hour * 60 + x.DT_ENCERRAMENTO.dt.minute
            cru.append(dict(ano=a, turno=t, recorte=rot, antes_17h01=int((m < 17 * 60 + 1).sum()), de_17h01_a_17h15=int(((m >= 17 * 60 + 1) & (m <= 17 * 60 + 15)).sum()),
                            de_17h16_a_18h59=int(((m >= 17 * 60 + 16) & (m < 19 * 60)).sum()), a_partir_de_19h=int((m >= 19 * 60).sum()), total=len(x)))
    out["h3_recontagem_relogio_cru"] = pd.DataFrame(cru)
    d = D[(2026, 2)]; d = d[(d.SG_UF != "ZZ") & d.atraso_min.notna()]
    tard = d[d.atraso_min >= 115]
    out["h3_tardias_uf"] = tard.groupby("SG_UF").agg(secoes=("lula", "size"), comparecimento=("QT_COMPARECIMENTO", "sum")).assign(
        pct_das_secoes_da_uf=lambda x: 100 * x.secoes / d.groupby("SG_UF").size().reindex(x.index)).sort_values("secoes", ascending=False).round(2)
    # votos depois do horario nominal: o BWeb NAO tem log de voto, so da para limitar por cima.
    #  (a) extrapolacao: taxa media da secao (comparecimento/duracao) x minutos apos o fechamento nominal (menos 2 min do ultimo da fila)
    #      -> teto grosseiro, porque o fluxo no fim do dia e muito menor que a media
    #  (b) comparecimento total das secoes que fecharam >= 115 min depois (limite absoluto)
    est = []
    for (a, t) in ((2026, 2), (2022, 2), (2026, 1), (2022, 1)):
        x = D[(a, t)]; x = x[(x.SG_UF != "ZZ") & x.atraso_min.notna() & (x.dur_min > 0)]
        taxa = x.QT_COMPARECIMENTO / x.dur_min
        e = np.minimum(x.QT_COMPARECIMENTO, taxa * (x.atraso_min - 2).clip(lower=0))
        est.append(dict(ano=a, turno=t, teto_extrapolacao_taxa_media=int(e.sum()), teto_extrapolacao_secoes_ge_15min=int(e[x.atraso_min >= 15].sum()),
                        secoes_ge_115min=int((x.atraso_min >= 115).sum()), comparecimento_total_secoes_ge_115min=int(x.QT_COMPARECIMENTO[x.atraso_min >= 115].sum())))
    out["h3_votos_apos_horario_limite"] = pd.DataFrame(est)
    out["h3_nota_votos"] = ("Sem log de votacao no BWeb, o numero de votos depois das 17h nao e mensuravel aqui. Referencia externa (nao verificada): "
                            "34.330 eleitores apos 17h segundo levantamento da imprensa com dados do TSE.")
    # horario de recebimento do BU no TSE vs fechamento (corrige a leitura anterior)
    x = D[(2026, 2)]
    out["h3_recebimento"] = pd.DataFrame({"receb_antes_19h_pct": [100 * (x.receb_h < 19).mean()], "receb_apos_20h_pct": [100 * (x.receb_h >= 20).mean()],
                                          "fecham_ate_15min_pct": [100 * (x.atraso_min <= 15).mean()]})


# ----------------------------------------------------------------------------------------------- H4
def h4(D, reg, out):
    w26 = par_ano(D, 2026)
    w22 = par_ano(D, 2022)[KEY + ["lula_sh", "lula_sh_t1"]].rename(columns={"lula_sh": "lula_sh_22", "lula_sh_t1": "lula_sh_22_t1"})
    s = w26.merge(w22, on=KEY, how="inner")
    s = s[s.atraso_min.notna()].copy()
    out["h4_amostra"] = {"secoes_pareadas": int(len(s))}
    linhas = []
    for L in (15, 60, 115):
        s["tarde"] = (s.atraso_min >= L).astype(float)
        n = int(s.tarde.sum())
        if n < 100:
            print(f"NAO EXECUTADO [H4 atraso>={L}]: so {n} secoes", file=sys.stderr)
            out.setdefault("nao_executados", []).append((f"H4 atraso>={L}", f"{n} secoes"))
            continue
        rA = tenta(out, f"H4 L{L} 2026 c/ lag", fe_ols, s, "lula_sh", ["tarde", "lula_sh_t1"], "uf_local")
        rP1 = tenta(out, f"H4 L{L} placebo 2022", fe_ols, s, "lula_sh_22", ["tarde", "lula_sh_22_t1"], "uf_local")
        rA0 = tenta(out, f"H4 L{L} 2026 sem lag", fe_ols, s, "lula_sh", ["tarde"], "uf_local")
        rP2 = tenta(out, f"H4 L{L} placebo T1/2026", fe_ols, s, "lula_sh_t1", ["tarde"], "uf_local")
        rZ = tenta(out, f"H4 L{L} EF zona", fe_ols, s, "lula_sh", ["tarde", "lula_sh_t1"], "uf_zona")
        expo = float(s[s.tarde == 1].valid2.sum())
        if rA is not None and rP1 is not None:
            bA, sA = _b(rA, "tarde"); bP, sP = _b(rP1, "tarde")
            reg.add("H4", f"fecha >= {L} min apos 17h: Lula% (c/ lag, EF local)", bA, sA, [("mesmas secoes em 2022/T2", bP, sP)], expo,
                    nota=f"{n} secoes tardias na amostra pareada")
            linhas.append(dict(L=L, spec="2026 T2 c/ lag", coef_pp=100 * bA, ep_pp=100 * sA, secoes_tardias=n))
            linhas.append(dict(L=L, spec="placebo 2022 T2 c/ lag (mesmas secoes)", coef_pp=100 * bP, ep_pp=100 * sP, secoes_tardias=n))
        if rA0 is not None and rP2 is not None:
            bA, sA = _b(rA0, "tarde"); bP, sP = _b(rP2, "tarde")
            reg.add("H4", f"fecha >= {L} min apos 17h: Lula% (s/ lag, EF local)", bA, sA, [("mesmas secoes no T1/2026", bP, sP)], expo)
            linhas.append(dict(L=L, spec="2026 T2 s/ lag", coef_pp=100 * bA, ep_pp=100 * sA, secoes_tardias=n))
            linhas.append(dict(L=L, spec="placebo T1/2026 s/ lag (mesmas secoes)", coef_pp=100 * bP, ep_pp=100 * sP, secoes_tardias=n))
        if rZ is not None:
            linhas.append(dict(L=L, spec="2026 T2 c/ lag, EF zona", coef_pp=100 * rZ.loc["tarde", "coef"], ep_pp=100 * rZ.loc["tarde", "se"], secoes_tardias=n))
    out["h4_coef"] = pd.DataFrame(linhas)
    # efeito "natural" de fechar tarde dentro do proprio turno (fila), para contexto
    nat = []
    for (a, t) in ((2022, 1), (2022, 2), (2026, 1), (2026, 2)):
        d = base(D[(a, t)]); d = d[d.atraso_min.notna()].copy(); d["tarde"] = (d.atraso_min >= 15).astype(float)
        r = tenta(out, f"H4 natural {a}T{t}", fe_ols, d, "lula_sh", ["tarde"], "uf_local")
        if r is not None:
            nat.append(dict(ano=a, turno=t, coef_pp=100 * r.loc["tarde", "coef"], ep_pp=100 * r.loc["tarde", "se"], secoes_tardias=int(d.tarde.sum())))
    out["h4_natural"] = pd.DataFrame(nat)


def _h1_redteam(D, W, out):
    """Explicacoes mundanas para (a) a associacao manual x Lula de 2026 em S0 e (b) o excesso pro-Flavio em votos/apto."""
    import os
    rt = []
    # (a) modelo da urna: o parque mudou entre 2022 e 2026 (entrou a UE2022; sairam UE2009/2010/2011)
    mod = {a: pd.read_parquet(os.path.join(out["_parquet"], f"modelo_urna_{a}.parquet")) for a in (2022, 2026)}
    tabm = []
    for (a, t) in ((2022, 1), (2022, 2), (2026, 1), (2026, 2)):
        d = base(D[(a, t)]).merge(mod[a][mod[a].NR_TURNO == t][KEY + ["CD_MODELO_URNA"]], on=KEY, how="left")
        d = d[d.manual_rate.notna()]
        g = d.groupby("CD_MODELO_URNA").agg(secoes=("lula", "size"), taxa_manual=("manual_rate", "mean"), lula_sh=("lula_sh", "mean")).reset_index()
        g.insert(0, "turno", t); g.insert(0, "ano", a); tabm.append(g)
        dums = []
        for m in sorted(d.CD_MODELO_URNA.dropna().unique()):
            if m != 2020:
                d[f"m{int(m)}"] = (d.CD_MODELO_URNA == m).astype(float); dums.append(f"m{int(m)}")
        r = fe_ols(d, "lula_sh", ["manual_rate"] + dums, "uf_local")
        rt.append(dict(teste="S0 + dummies de modelo de urna", ano=a, turno=t, coef_manual=r.loc["manual_rate", "coef"], ep=r.loc["manual_rate", "se"]))
    out["h1_taxa_manual_por_modelo_urna"] = pd.concat(tabm, ignore_index=True)
    # (b) composicao do T1: de quem eram os votos dos eliminados e de brancos/nulos
    for a in (2022, 2026):
        w = W[a]
        for nome, y, ylag in (("Lula votos/apto", "lula_pa", "lula_pa_t1"), ("Flavio/Bolsonaro votos/apto", "dir_pa", "dir_pa_t1")):
            r0 = fe_ols(w, y, ["manual_rate", ylag], "uf_local")
            r1 = fe_ols(w, y, ["manual_rate", "lula_pa_t1", "dir_pa_t1", "outros_pa_t1", "bn_pa_t1"], "uf_local")
            rt.append(dict(teste=f"S1 {nome} (so lag proprio)", ano=a, turno=2, coef_manual=r0.loc["manual_rate", "coef"], ep=r0.loc["manual_rate", "se"]))
            rt.append(dict(teste=f"S1 {nome} + T1 de todos os candidatos e brancos/nulos", ano=a, turno=2, coef_manual=r1.loc["manual_rate", "coef"], ep=r1.loc["manual_rate", "se"]))
    for a in (2022, 2026):
        w = W[a]
        r = fe_ols(w, "turnout", ["manual_rate", "turnout_t1"], "uf_local")
        rt.append(dict(teste="comparecimento T2 ~ taxa manual + comparecimento T1", ano=a, turno=2, coef_manual=r.loc["manual_rate", "coef"], ep=r.loc["manual_rate", "se"]))
    out["h1_redteam"] = pd.DataFrame(rt)
