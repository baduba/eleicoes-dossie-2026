#!/usr/bin/env python3
"""A33 (Adendo 15): liberacao manual no nivel do local de votacao (escola). Descritivo, teste com efeito fixo de zona (placebos 2022 e 2018), escolas extremas, sincronia nos logs e listas para o papel.
Uso: python -I 44_a33_escolas.py DIR_PARQUET DIR_PERFIL_IDADE DIR_AMOSTRA DIR_LOGS DIR_MAPA DIR_SAIDA"""
import glob
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, Registro, fe_ols, MARGEM

FAIXAS = [(0, .05, "ate 5%"), (.05, .10, "5 a 10%"), (.10, .20, "10 a 20%"), (.20, .30, "20 a 30%"), (.30, .50, "30 a 50%"), (.50, 9, "mais de 50%")]
GR = ["g30_44", "g45_59", "g60_69", "g70_79", "g80p"]
Z95 = 1.645
W1, W2 = 60, 180
NPERM = 500
SEMENTE = 20261029
CAMPOS = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"]


def robust(x):
    x = np.asarray(x, float); return 1.4826 * np.median(np.abs(x - np.median(x)))


def escolas(pq, pi, ano):
    """Uma linha por escola com T1 e T2."""
    out = {}
    for t in (1, 2):
        d = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{t}.parquet"), columns=KEY + ["NR_LOCAL_VOTACAO", "uf_local", "DS_TIPO_URNA", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "valid2", "biom_nh"])
        d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ")]
        g = d.groupby("uf_local").agg(SG_UF=("SG_UF", "first"), CD_MUNICIPIO=("CD_MUNICIPIO", "first"), NR_ZONA=("NR_ZONA", "first"), NR_LOCAL_VOTACAO=("NR_LOCAL_VOTACAO", "first"), secoes=("NR_SECAO", "size"),
                                      aptos=("QT_APTOS", "sum"), comp=("QT_COMPARECIMENTO", "sum"), lula=("lula", "sum"), opo=("dir", "sum"), valid=("valid2", "sum"), man=("biom_nh", "sum"))
        out[t] = g.add_suffix(f"_t{t}") if False else g
    a, b = out[1], out[2]
    e = b.join(a[["secoes", "aptos", "comp", "lula", "opo", "valid", "man"]].add_suffix("_t1"), how="inner")
    e = e.rename(columns={c: c + "_t2" for c in ("secoes", "aptos", "comp", "lula", "opo", "valid", "man")})
    e["uf_zona"] = e.SG_UF + "_" + e.CD_MUNICIPIO.astype(str) + "_" + e.NR_ZONA.astype(str) if False else e.SG_UF + "_" + e.NR_ZONA.astype(str)
    e["uf_mun"] = e.SG_UF + "_" + e.CD_MUNICIPIO.astype(str)
    e["manual"] = e.man_t2 / e.comp_t2.replace(0, np.nan)
    e["sh_t1"] = e.lula_t1 / e.valid_t1.replace(0, np.nan); e["sh_t2"] = e.lula_t2 / e.valid_t2.replace(0, np.nan)
    e["dsh"] = e.sh_t2 - e.sh_t1
    e["turn_t1"] = e.comp_t1 / e.aptos_t1.replace(0, np.nan); e["turn_t2"] = e.comp_t2 / e.aptos_t2.replace(0, np.nan); e["dturn"] = e.turn_t2 - e.turn_t1
    e["dopo_pa"] = (e.opo_t2 - e.opo_t1) / e.aptos_t1.replace(0, np.nan); e["dpt_pa"] = (e.lula_t2 - e.lula_t1) / e.aptos_t1.replace(0, np.nan)
    p = os.path.join(pi, f"perfil_idade_{ano}.parquet")
    if os.path.exists(p):
        pf = pd.read_parquet(p)
        pf["uf_local"] = pf.SG_UF + "_" + pf.CD_MUNICIPIO.astype(str) + "_" + pf.NR_ZONA.astype(str) + "_" + pf.NR_LOCAL_VOTACAO.astype(str)
        for c in ["idade_media", "bio_frac"] + GR:
            pf[c + "_w"] = pf[c] * pf.apt
        s = pf.groupby("uf_local").agg(apt_p=("apt", "sum"), **{c + "_w": (c + "_w", "sum") for c in ["idade_media", "bio_frac"] + GR})
        for c in ["idade_media", "bio_frac"] + GR:
            s[c] = s[c + "_w"] / s.apt_p.replace(0, np.nan)
        e = e.join(s[["idade_media", "bio_frac"] + GR], how="left")
    else:
        for c in ["idade_media", "bio_frac"] + GR:
            e[c] = np.nan
    e["ano"] = ano
    return e[(e.comp_t1 >= 100) & (e.comp_t2 >= 100)].copy()


def descritivo(E):
    L = []
    for ano in (2026, 2022):
        e = E[ano]
        for lo, hi, nome in FAIXAS:
            x = e[(e.manual >= lo) & (e.manual < hi)]
            L.append(dict(ano=ano, faixa=nome, escolas=len(x), secoes=int(x.secoes_t2.sum()), votantes=int(x.comp_t2.sum()), votos_PT=int(x.lula_t2.sum()), votos_oponente=int(x.opo_t2.sum()),
                          escolas_com_PT_na_frente=int((x.lula_t2 > x.opo_t2).sum()), pct_escolas_com_PT_na_frente=100 * float((x.lula_t2 > x.opo_t2).mean()) if len(x) else np.nan,
                          idade_media_mediana=float(x.idade_media.median()) if len(x) else np.nan))
    return pd.DataFrame(L)


def rodar_modelos(E, expo_v, expo_a):
    reg = Registro(); linhas = []
    xs0 = ["manual", "idade_media", "sh_t1"]
    desf = (("dsh", "variacao da participacao de Lula (T2 menos T1)", "PT", 2.0, expo_v), ("dturn", "variacao do comparecimento (T2 menos T1)", "PT+OPO", 1.0, expo_a))
    def est(e, y, xs, grupo):
        try:
            r = fe_ols(e, y, xs, grupo, grupo).iloc[0]
            return float(r.coef), float(r.se), int(r.n), int(r.grupos)
        except ValueError:
            return None
    # variante 1: taxa manual da escola
    for y, nome, sent, fator, expo in desf:
        res = {a: est(E[a].dropna(subset=["manual", "idade_media"] if a != 2018 or E[2018].idade_media.notna().any() else ["manual"]), y, xs0 if (a != 2018 or E[2018].idade_media.notna().any()) else ["manual", "sh_t1"], "uf_zona") for a in (2026, 2022, 2018)}
        for a, r in res.items():
            linhas.append(dict(variante="taxa manual da escola", desfecho=nome, ano=a, FE="zona", coef=r[0] if r else np.nan, ep=r[1] if r else np.nan, n=r[2] if r else np.nan, zonas=r[3] if r else np.nan))
        if res[2026] and res[2022] and res[2018]:
            sinais = [(1.0, sent, "PT")] + ([(-1.0, "OPO", "oponente (simetria)")] if y == "dsh" else [])
            for sg, st, rot in sinais:
                reg.add("A33", f"{nome}, {rot}: 2026 contra 2022 e 2018 (taxa manual da escola, EF de zona)", sg * res[2026][0], res[2026][1], [("2022/T2", sg * res[2022][0], res[2022][1]), ("2018/T2", sg * res[2018][0], res[2018][1])],
                        expo=expo, fator=fator, sentido=st, nota=f"{res[2026][2]} escolas, {res[2026][3]} zonas")
        # robustez: efeito fixo de municipio
        for a in (2026, 2022, 2018):
            e = E[a].dropna(subset=["manual", "idade_media"]) if E[a].idade_media.notna().any() else E[a]
            r = est(e, y, xs0 if E[a].idade_media.notna().any() else ["manual", "sh_t1"], "uf_mun")
            linhas.append(dict(variante="taxa manual da escola", desfecho=nome, ano=a, FE="municipio", coef=r[0] if r else np.nan, ep=r[1] if r else np.nan, n=r[2] if r else np.nan, zonas=r[3] if r else np.nan))
    # simetria em votos por apto (descritiva)
    for y, nome in (("dopo_pa", "variacao do voto do oponente por apto"), ("dpt_pa", "variacao do voto do PT por apto")):
        for a in (2026, 2022, 2018):
            e = E[a].dropna(subset=["manual", "idade_media"]) if E[a].idade_media.notna().any() else E[a]
            r = est(e, y, xs0 if E[a].idade_media.notna().any() else ["manual", "sh_t1"], "uf_zona")
            linhas.append(dict(variante="taxa manual da escola", desfecho=nome, ano=a, FE="zona", coef=r[0] if r else np.nan, ep=r[1] if r else np.nan, n=r[2] if r else np.nan, zonas=r[3] if r else np.nan))
    # variante 2: excesso sobre a mesma escola no ano anterior
    EX = {}
    for a, b in ((2026, 2022), (2022, 2018)):
        j = E[a].merge(E[b][["manual"]].rename(columns={"manual": "manual_ant"}), left_index=True, right_index=True, how="inner")
        j["excesso_vs_anterior"] = j.manual - j.manual_ant
        EX[a] = j
    for y, nome, sent, fator, expo in desf:
        r26 = est(EX[2026].dropna(subset=["idade_media"]), y, ["excesso_vs_anterior", "idade_media", "sh_t1"], "uf_zona")
        r22 = est(EX[2022].dropna(subset=["idade_media"]), y, ["excesso_vs_anterior", "idade_media", "sh_t1"], "uf_zona")
        for a, r in ((2026, r26), (2022, r22)):
            linhas.append(dict(variante="excesso sobre a mesma escola no ano anterior", desfecho=nome, ano=a, FE="zona", coef=r[0] if r else np.nan, ep=r[1] if r else np.nan, n=r[2] if r else np.nan, zonas=r[3] if r else np.nan))
        if r26 and r22:
            sinais = [(1.0, sent, "PT")] + ([(-1.0, "OPO", "oponente (simetria)")] if y == "dsh" else [])
            for sg, st, rot in sinais:
                reg.add("A33", f"{nome}, {rot}: 2026 contra 2022 (excesso da taxa manual sobre o ano anterior da mesma escola, EF de zona)", sg * r26[0], r26[1], [("2022/T2 (contra 2018)", sg * r22[0], r22[1])],
                        expo=expo, fator=fator, sentido=st, nota=f"{r26[2]} escolas, {r26[3]} zonas")
    return reg.frame(), pd.DataFrame(linhas)


def extremas(E, pq, saida, pi):
    e26, e22 = E[2026], E[2022]
    cols = ["manual", "bio_frac"] + GR
    d22 = e22.dropna(subset=cols).copy(); ufs = sorted(d22.SG_UF.unique())
    def X(d):
        return np.column_stack([pd.get_dummies(d.SG_UF).reindex(columns=ufs, fill_value=0).astype(float).values, d[GR].values, d.bio_frac.values])
    w = np.sqrt(d22.comp_t2.values)
    b, *_ = np.linalg.lstsq(X(d22) * w[:, None], d22.manual.values * w, rcond=None)
    d22["res"] = d22.manual - X(d22) @ b
    edges = np.unique(np.quantile(d22.comp_t2, np.linspace(0, 1, 11)))
    d22["bin"] = np.clip(np.searchsorted(edges, d22.comp_t2, side="right") - 1, 0, len(edges) - 2)
    sig = d22.groupby("bin").res.apply(robust)
    d = e26.dropna(subset=cols).copy()
    d["prev"] = X(d) @ b; d["excesso_idade"] = d.manual - d.prev
    d["bin"] = np.clip(np.searchsorted(edges, d.comp_t2, side="right") - 1, 0, len(edges) - 2); d["sig"] = d.bin.map(sig)
    d = d.join(e22[["manual", "lula_t1", "lula_t2", "opo_t1", "opo_t2", "comp_t2"]].add_suffix("_2022"), how="left")
    d["excesso_vs_2022"] = d.manual - d.manual_2022
    d["votantes_em_excesso"] = np.maximum(0, d.excesso_idade) * d.comp_t2
    d["votantes_alem_do_ruido"] = np.maximum(0, d.excesso_idade - Z95 * d.sig) * d.comp_t2
    corte = d.excesso_idade.quantile(0.99)
    cand = d[d.excesso_idade >= corte].copy()
    cand["ausente_em_2022"] = cand.manual_2022.isna()
    ext = cand[(cand.excesso_vs_2022 > 0) | cand.manual_2022.isna()].sort_values("excesso_idade", ascending=False)
    loc = pd.read_parquet(os.path.join(pq, "locais_2026.parquet"))
    nl = loc.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO"]).NM_LOCAL_VOTACAO.first().reset_index()
    ext = ext.reset_index().merge(nl, on=CAMPOS, how="left")
    mapa = pd.read_csv(os.path.join(sys.argv[5], "A20_mapa_tse_ibge.csv"), dtype=str); mapa["CD_MUNICIPIO"] = mapa.CD_MUNICIPIO.astype(int)
    ext = ext.merge(mapa[["SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO"]], on=["SG_UF", "CD_MUNICIPIO"], how="left")
    ext["rank"] = range(1, len(ext) + 1)
    out = ext[["rank", "uf_local", "SG_UF", "NM_MUNICIPIO", "CD_MUNICIPIO", "NR_ZONA", "NR_LOCAL_VOTACAO", "NM_LOCAL_VOTACAO", "secoes_t2", "comp_t2", "manual", "prev", "excesso_idade", "manual_2022", "excesso_vs_2022", "ausente_em_2022",
              "idade_media", "lula_t1", "opo_t1", "lula_t2", "opo_t2", "lula_t1_2022", "opo_t1_2022", "lula_t2_2022", "opo_t2_2022", "votantes_em_excesso", "votantes_alem_do_ruido"]].rename(columns={"secoes_t2": "secoes", "comp_t2": "votantes_t2", "prev": "manual_previsto_modelo_2022"})
    out.to_csv(os.path.join(saida, "A33_escolas_extremas.csv"), index=False, float_format="%.5g")
    res = dict(escolas_2026=len(d), corte_excesso_p99=float(corte), candidatas_top1pct=len(cand), extremas_listadas=len(ext), das_quais_ausentes_em_2022=int(ext.ausente_em_2022.sum()),
               secoes=int(ext.secoes_t2.sum()), votantes=int(ext.comp_t2.sum()), teto_votos_de_margem_fator1=float(ext.votantes_em_excesso.sum()), teto_pct=100 * float(ext.votantes_em_excesso.sum()) / MARGEM,
               alem_do_ruido=float(ext.votantes_alem_do_ruido.sum()), alem_do_ruido_pct=100 * float(ext.votantes_alem_do_ruido.sum()) / MARGEM, nota="teto de pior caso, nao estimativa: todos os excessos a favor de um so lado")
    pd.DataFrame([res]).to_csv(os.path.join(saida, "A33_escolas_extremas_resumo.csv"), index=False)
    por_uf = ext.groupby("SG_UF").size().rename("escolas").reset_index().sort_values("escolas", ascending=False); por_uf.to_csv(os.path.join(saida, "A33_escolas_extremas_por_UF.csv"), index=False)
    return ext, res


def secoes_top20(ext, pq, saida):
    """Item 5: todas as secoes das 20 escolas mais extremas, T1 e T2, com colunas vazias para o BU impresso (formato de 04_cruza_bu_impresso.py)."""
    top = ext.head(20)[["rank", "uf_local", "NM_MUNICIPIO", "NM_LOCAL_VOTACAO", "excesso_idade"]]
    cols = KEY + ["uf_local", "NR_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "biom_nh"]
    t = {k: pd.read_parquet(os.path.join(pq, f"bu_2026_t{k}.parquet"), columns=cols) for k in (1, 2)}
    t1 = t[1][t[1].uf_local.isin(top.uf_local)].set_index(KEY)
    t2 = t[2][t[2].uf_local.isin(top.uf_local)].set_index(KEY)
    r = {"QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento", "lula": "lula", "dir": "flavio", "branco": "brancos", "nulo": "nulos", "biom_nh": "liberacoes_manuais"}
    S = t2[["uf_local", "NR_LOCAL_VOTACAO"] + list(r)].rename(columns={c: f"{v}_T2" for c, v in r.items()}).join(t1[list(r)].rename(columns={c: f"{v}_T1" for c, v in r.items()}), how="left").reset_index()
    S = S.merge(top, on="uf_local", how="left").sort_values(["rank", "NR_SECAO"])
    for k in ("aptos", "comparecimento", "lula", "flavio", "brancos", "nulos"):
        for c in ("T1", "T2"):
            S[f"impresso_{k}_{c}"] = ""
    S = S.rename(columns={"rank": "posicao_A33", "NM_MUNICIPIO": "municipio", "NM_LOCAL_VOTACAO": "local_de_votacao"})
    ordem = ["posicao_A33", "SG_UF", "CD_MUNICIPIO", "municipio", "NR_ZONA", "NR_LOCAL_VOTACAO", "local_de_votacao", "NR_SECAO"] + [f"{v}_{c}" for c in ("T1", "T2") for v in r.values()] + [c for c in S.columns if c.startswith("impresso_")]
    S[ordem].to_csv(os.path.join(saida, "A33_20_escolas_secoes.csv"), index=False)
    return S


def sincronia(dl, pq, damostra, saida):
    L = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(dl, "*.parquet")))], ignore_index=True)
    L = L[L.dia.isin([1, 2]) & L.ts.notna()].rename(columns={"uf": "SG_UF", "cd_municipio": "CD_MUNICIPIO", "zona": "NR_ZONA", "secao": "NR_SECAO"})
    M = pd.read_parquet(os.path.join(damostra, "A32_medidas_secao_dia.parquet"))[KEY + ["ano", "turno", "consistente"]].rename(columns={"turno": "dia"})
    L = L.merge(M, on=KEY + ["ano", "dia"], how="left"); L = L[L.consistente.fillna(False)]
    keys = {}
    for a in (2022, 2026):
        d = pd.read_parquet(os.path.join(pq, f"bu_{a}_t2.parquet"), columns=KEY + ["uf_local"]); keys[a] = d
    L = pd.concat([g.merge(keys[a], on=KEY, how="left") for a, g in L.groupby("ano")], ignore_index=True)
    rng = np.random.default_rng(SEMENTE)
    def manuais(ts, tp):
        ts = np.asarray(ts); isM = np.frombuffer(tp.encode(), dtype="S1").astype(str) == "M"
        return ts, ts[isM]
    def conta(sa, sb, W):
        """eventos de sa com algum evento de sb a ate W s, mais o inverso"""
        if len(sa) == 0 or len(sb) == 0:
            return 0
        sb = np.sort(sb); sa = np.sort(sa)
        def f(x, y):
            i = np.searchsorted(y, x); lo = np.abs(x - y[np.clip(i - 1, 0, len(y) - 1)]); hi = np.abs(x - y[np.clip(i, 0, len(y) - 1)]); return int((np.minimum(lo, hi) <= W).sum())
        return f(sa, sb) + f(sb, sa)
    linhas, cob = [], []
    WS = (W1, W2)
    for (a, dia), g in L.groupby(["ano", "dia"]):
        grupos = [(u, h) for u, h in g.groupby("uf_local") if len(h) >= 3]
        cob.append(dict(ano=a, dia=dia, secoes_com_log_consistente=len(g), escolas_com_3_ou_mais_secoes=len(grupos), secoes_nessas_escolas=int(sum(len(h) for _, h in grupos)), ufs=int(g.SG_UF.nunique())))
        Cobs = {W: 0 for W in WS}; Cperm = {W: np.zeros(NPERM) for W in WS}; Cn = 0; nesc = 0
        for u, h in grupos:
            seq = [manuais(r.ts, r.tp) for r in h.itertuples()]
            if sum(len(m) for _, m in seq) < 6:
                continue
            nesc += 1
            idx = [(i, j) for i in range(len(seq)) for j in range(i + 1, len(seq))]
            for W in WS:
                Cobs[W] += sum(conta(seq[i][1], seq[j][1], W) for i, j in idx)
            Cn += sum(len(seq[i][1]) + len(seq[j][1]) for i, j in idx)
            ms = [len(man) for _, man in seq]
            for k in range(NPERM):
                sm = [np.sort(rng.choice(ts_all, size=m, replace=False)) if m else man for (ts_all, man), m in zip(seq, ms)]
                for W in WS:
                    Cperm[W][k] += sum(conta(sm[i], sm[j], W) for i, j in idx)
        for W in WS:
            if Cn:
                linhas.append(dict(ano=a, dia=dia, janela_s=W, nulo="N1: rotulos manuais sorteados entre as habilitacoes da propria secao", escolas=nesc, eventos_em_pares=Cn, observado=Cobs[W], esperado=float(Cperm[W].mean()),
                                   razao=Cobs[W] / Cperm[W].mean() if Cperm[W].mean() > 0 else np.nan, z=(Cobs[W] - Cperm[W].mean()) / Cperm[W].std(ddof=1) if Cperm[W].std(ddof=1) > 0 else np.nan, p_unilateral=float((Cperm[W] >= Cobs[W]).mean())))
        # N2: pares entre escolas diferentes da mesma UF
        for W in (W1, W2):
            within, cross = [], []
            sec = {r.Index: manuais(r.ts, r.tp)[1] for r in g.itertuples()}
            gg = g.reset_index(drop=True)
            for uf, h in gg.groupby("SG_UF"):
                esc = {u: list(x.index) for u, x in h.groupby("uf_local") if len(x) >= 1}
                for u, ix in esc.items():
                    if len(ix) < 3:
                        continue
                    for i in range(len(ix)):
                        for j in range(i + 1, len(ix)):
                            sa, sb = manuais(gg.ts[ix[i]], gg.tp[ix[i]])[1], manuais(gg.ts[ix[j]], gg.tp[ix[j]])[1]
                            n_ = len(sa) + len(sb)
                            if n_:
                                within.append(conta(sa, sb, W) / n_)
                    outros = [k for k in h.index if k not in ix]
                    for _ in range(len(ix) * (len(ix) - 1) // 2):
                        i, j = rng.choice(ix), rng.choice(outros)
                        sa, sb = manuais(gg.ts[i], gg.tp[i])[1], manuais(gg.ts[j], gg.tp[j])[1]
                        n_ = len(sa) + len(sb)
                        if n_:
                            cross.append(conta(sa, sb, W) / n_)
            if within and cross:
                linhas.append(dict(ano=a, dia=dia, janela_s=W, nulo="N2: pares de escolas diferentes da mesma UF", escolas=np.nan, eventos_em_pares=len(within), observado=float(np.mean(within)), esperado=float(np.mean(cross)),
                                   razao=float(np.mean(within) / np.mean(cross)) if np.mean(cross) > 0 else np.nan, z=np.nan, p_unilateral=np.nan))
    S = pd.DataFrame(linhas); S.to_csv(os.path.join(saida, "A33_sincronia.csv"), index=False)
    C = pd.DataFrame(cob); C.to_csv(os.path.join(saida, "A33_sincronia_cobertura.csv"), index=False)
    return S, C


def main(pq, pi, damostra, dl, dmapa, saida):
    os.makedirs(saida, exist_ok=True)
    E = {a: escolas(pq, pi, a) for a in (2026, 2022, 2018)}
    b26 = pd.read_parquet(os.path.join(pq, "bu_2026_t2.parquet"), columns=["SG_UF", "DS_TIPO_URNA", "valid2", "QT_APTOS", "manual_rate"])
    b26 = b26[b26.DS_TIPO_URNA.str.upper().eq("APURADA") & (b26.SG_UF != "ZZ") & b26.manual_rate.notna()]
    expo_v = float((b26.manual_rate * b26.valid2).sum())      # votos manuais equivalentes (convencao de H1, Adendo 15a)
    expo_a = float((b26.manual_rate * b26.QT_APTOS).sum())
    D = descritivo(E); D.to_csv(os.path.join(saida, "A33_descritivo.csv"), index=False)
    fam, mod = rodar_modelos(E, expo_v, expo_a)
    fam.to_csv(os.path.join(saida, "A33_testes.csv"), index=False); mod.to_csv(os.path.join(saida, "A33_modelos.csv"), index=False)
    ext, res = extremas(E, pq, saida, pi)
    S20 = secoes_top20(ext, pq, saida)
    if os.environ.get("A33_PULA_SINCRONIA") == "1":
        S, C = pd.read_csv(os.path.join(saida, "A33_sincronia.csv")), pd.read_csv(os.path.join(saida, "A33_sincronia_cobertura.csv"))
    else:
        S, C = sincronia(dl, pq, damostra, saida)
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
    print({a: len(E[a]) for a in E}, "com idade 2018:", int(E[2018].idade_media.notna().sum()))
    print(D.round(2).to_string()); print(mod.round(5).to_string()); print(fam[["teste", "est_2026T2", "ep", "comparador_exigente", "b_comp", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].round(4).to_string() if len(fam) else "sem familia")
    print(pd.DataFrame([res]).T.to_string()); print(ext[["rank", "SG_UF", "NM_MUNICIPIO", "NM_LOCAL_VOTACAO", "secoes_t2", "comp_t2", "manual", "manual_2022", "excesso_idade", "excesso_vs_2022", "idade_media"]].head(25).round(3).to_string())
    print(C.to_string()); print(S.round(3).to_string())


if __name__ == "__main__":
    main(*sys.argv[1:7])
