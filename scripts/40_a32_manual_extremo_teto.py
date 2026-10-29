#!/usr/bin/env python3
"""A32 (Adendo 11), itens 2 e 3: secoes com liberacao manual extrema (> 30% e > 50% dos votantes) e teto em votos de margem do excesso de liberacao manual sobre o esperado pela idade do eleitorado
(modelo ajustado em 2022). Fonte: BWeb (`manual_rate = biom_nh / comparecimento`) e perfil do eleitorado por secao com faixas etarias.
Uso: python -I 40_a32_manual_extremo_teto.py DIR_PARQUET DIR_PERFIL_IDADE DIR_SAIDA"""
import os
import sys
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from lib_auditoria import KEY, MARGEM
from h5_h8 import tipo_local

CORTES = (0.30, 0.50)
GR = ["g30_44", "g45_59", "g60_69", "g70_79", "g80p"]            # g16_29 omitido (referencia)
Z95 = 1.645


def robust(x):
    x = np.asarray(x, float)
    return 1.4826 * np.median(np.abs(x - np.median(x)))


def carrega(pq, pi, ano, turno):
    d = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{turno}.parquet"), columns=KEY + ["DS_TIPO_URNA", "QT_APTOS", "QT_COMPARECIMENTO", "valid2", "lula", "lula_sh", "turnout", "manual_rate", "uf_local", "biom_nh"])
    d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA") & (d.SG_UF != "ZZ") & (d.QT_COMPARECIMENTO >= 30) & d.manual_rate.notna()].copy()
    p = pd.read_parquet(os.path.join(pi, f"perfil_idade_{ano}.parquet")).drop(columns=["NR_LOCAL_VOTACAO"])
    d = d.merge(p, on=KEY, how="left")
    loc = pd.read_parquet(os.path.join(pq, f"locais_{ano}.parquet"))[KEY + ["NM_LOCAL_VOTACAO"]]
    loc["tipo_local"] = tipo_local(loc.NM_LOCAL_VOTACAO)
    d = d.merge(loc, on=KEY, how="left")
    d["ano"], d["turno"] = ano, turno
    return d


def contraste_local(d, col, peso):
    """Valor da secao menos a media ponderada das OUTRAS secoes do mesmo local (NaN se o local tem uma secao so)."""
    w = d[peso]
    g = (d[col] * w).groupby(d.uf_local).transform("sum") - d[col] * w
    ws = w.groupby(d.uf_local).transform("sum") - w
    return d[col] - g / ws.where(ws > 0)


def main(pq, pi, saida):
    os.makedirs(saida, exist_ok=True)
    D = {(a, t): carrega(pq, pi, a, t) for a in (2022, 2026) for t in (1, 2)}
    # variacao do T1 para o T2 (mesma secao) para o contraste com controle do T1
    for a in (2022, 2026):
        t1 = D[(a, 1)].set_index(KEY)[["lula_sh", "turnout"]].add_suffix("_t1")
        D[(a, 2)] = D[(a, 2)].merge(t1, left_on=KEY, right_index=True, how="left")
    linhas, por_uf, por_tipo = [], [], []
    for (a, t), d in D.items():
        d = d.copy()
        d["c_turnout"] = contraste_local(d, "turnout", "QT_APTOS")
        d["c_lula"] = contraste_local(d, "lula_sh", "valid2")
        if t == 2:
            d["dturn"] = d.turnout - d.turnout_t1; d["dlula"] = d.lula_sh - d.lula_sh_t1
            d["c_dturn"] = contraste_local(d, "dturn", "QT_APTOS"); d["c_dlula"] = contraste_local(d, "dlula", "valid2")
        for corte in CORTES:
            e = d[d.manual_rate > corte]
            row = dict(ano=a, turno=t, corte=f"> {int(corte * 100)}%", secoes_validas=len(d), extremas=len(e), pct=100 * len(e) / len(d), votantes_extremas=int(e.QT_COMPARECIMENTO.sum()),
                       comparecimento_mediano_extremas=float(e.QT_COMPARECIMENTO.median()) if len(e) else np.nan, idade_media_mediana_extremas=float(e.idade_media.median()) if len(e) else np.nan,
                       idade_media_mediana_todas=float(d.idade_media.median()), sem_perfil_de_idade=int(e.idade_media.isna().sum()), ufs_com_extremas=int(e.SG_UF.nunique()))
            for nome in (("c_turnout", "c_lula") + (("c_dturn", "c_dlula") if t == 2 else ())):
                x = e.dropna(subset=[nome])
                if len(x) >= 5:
                    loc = x.groupby("uf_local")[nome].mean()
                    row[f"{nome}_media"] = float(x[nome].mean()); row[f"{nome}_ep_por_local"] = float(loc.std(ddof=1) / np.sqrt(len(loc))); row[f"{nome}_n"] = len(x)
            linhas.append(row)
            if corte == 0.30:
                u = e.groupby("SG_UF").size().rename(f"{a}_T{t}")
                por_uf.append(u)
                por_tipo.append(pd.concat([e.groupby("tipo_local").size().rename("extremas"), d.groupby("tipo_local").size().rename("todas")], axis=1).assign(ano=a, turno=t).reset_index())
    R = pd.DataFrame(linhas)
    R.to_csv(os.path.join(saida, "A32_extremas_resumo.csv"), index=False)
    pu = pd.concat(por_uf, axis=1).fillna(0).astype(int).reset_index(); pu.to_csv(os.path.join(saida, "A32_extremas_por_UF_30pct.csv"), index=False)
    pt = pd.concat(por_tipo, ignore_index=True); pt["pct_do_tipo"] = 100 * pt.extremas / pt.todas; pt.to_csv(os.path.join(saida, "A32_extremas_por_tipo_30pct.csv"), index=False)

    # item 3: modelo de 2022 (T2), WLS por votantes, regressores de idade e biometria cadastrada, efeito fixo de UF
    def desenho(d, ufs):
        d = d.dropna(subset=GR + ["bio_frac"])
        X = np.column_stack([pd.get_dummies(d.SG_UF).reindex(columns=ufs, fill_value=0).astype(float).values, d[GR].values, d.bio_frac.values])
        return d, X
    ufs = sorted(D[(2022, 2)].SG_UF.unique())
    d22, X22 = desenho(D[(2022, 2)], ufs)
    w = np.sqrt(d22.QT_COMPARECIMENTO.values)
    b, *_ = np.linalg.lstsq(X22 * w[:, None], d22.manual_rate.values * w, rcond=None)
    d22 = d22.assign(pred=X22 @ b); d22["res"] = d22.manual_rate - d22.pred
    edges = np.unique(np.quantile(d22.QT_COMPARECIMENTO, np.linspace(0, 1, 11)))
    d22["bin"] = np.clip(np.searchsorted(edges, d22.QT_COMPARECIMENTO, side="right") - 1, 0, len(edges) - 2)
    sig = d22.groupby("bin").res.apply(robust)
    coef = pd.DataFrame({"termo": ufs + GR + ["bio_frac"], "coef": b}); coef.to_csv(os.path.join(saida, "A32_modelo_2022_coeficientes.csv"), index=False)
    out, tops = [], None
    for (ano, tag) in ((2022, "2022 (dentro da amostra, referencia)"), (2026, "2026")):
        d, X = desenho(D[(ano, 2)], ufs)
        d = d.assign(pred=X @ b); d["res"] = d.manual_rate - d.pred
        d["bin"] = np.clip(np.searchsorted(edges, d.QT_COMPARECIMENTO, side="right") - 1, 0, len(edges) - 2); d["sig"] = d.bin.map(sig)
        n = d.QT_COMPARECIMENTO
        shift = float(d.res.median())
        d["exc_a"] = np.maximum(0, d.res) * n
        d["exc_c"] = np.maximum(0, d.res - Z95 * d.sig) * n
        d["exc_net"] = np.maximum(0, d.res - shift) * n
        d["exc_net_c"] = np.maximum(0, d.res - shift - Z95 * d.sig) * n
        out.append(dict(ano=tag, secoes=len(d), manual_observado_total=float((d.manual_rate * n).sum()), manual_previsto_total=float((d.pred * n).sum()), deslocamento_nacional_mediana_residuo=shift,
                        a_soma_excessos_positivos=float(d.exc_a.sum()), c_alem_de_1_645_sigma=float(d.exc_c.sum()), net_sem_deslocamento_nacional=float(d.exc_net.sum()), net_e_alem_de_1_645_sigma=float(d.exc_net_c.sum()),
                        secoes_com_excesso_alem_de_1_645_sigma=int((d.res > Z95 * d.sig).sum())))
        if ano == 2026:
            tops = d
    T = pd.DataFrame(out)
    teto = max(T.loc[T.ano == "2026", ["a_soma_excessos_positivos", "c_alem_de_1_645_sigma", "net_sem_deslocamento_nacional", "net_e_alem_de_1_645_sigma"]].iloc[0])
    T["maior_dos_quatro_votos_de_margem_fator_1"] = np.where(T.ano == "2026", teto, np.nan)
    T["maior_pct_margem"] = 100 * T.maior_dos_quatro_votos_de_margem_fator_1 / MARGEM
    T.to_csv(os.path.join(saida, "A32_teto_excesso_manual.csv"), index=False)
    top = tops.sort_values("exc_a", ascending=False).head(50).copy(); top["rank_excesso"] = range(1, 51)
    top[["rank_excesso", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NM_LOCAL_VOTACAO", "tipo_local", "QT_APTOS", "QT_COMPARECIMENTO", "manual_rate", "pred", "res", "exc_a", "idade_media"]].rename(
        columns={"manual_rate": "manual_observado", "pred": "manual_previsto_modelo_2022", "res": "residuo", "exc_a": "excesso_votantes"}).to_csv(os.path.join(saida, "A32_50_secoes_excesso_2026T2.csv"), index=False, float_format="%.5g")
    tops[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "manual_rate", "pred", "res", "exc_a", "exc_c"]].to_parquet(os.path.join(pi, "A32_excesso_por_secao_2026T2.parquet"), index=False)
    pd.set_option("display.width", 250)
    print(R.round(3).to_string()); print(T.T.to_string()); print(coef.tail(7).to_string()); print(top.head(10)[["SG_UF", "NM_LOCAL_VOTACAO", "QT_COMPARECIMENTO", "manual_rate", "pred", "exc_a"]].to_string())


if __name__ == "__main__":
    main(*sys.argv[1:4])
