#!/usr/bin/env python3
"""A20b-idosos (Fase 3.1): cadastro e comparecimento dos mais idosos. Pre-registro: Adendos 9 e 9a (29/10/2026, antes de rodar).
Item 2: votantes 90+ e 100+ contra o Censo 2022 (aviso de descompasso de coortes). Item 2a: monotonicidade de coortes (sem Censo).
Item 3: biometria cadastrada por faixa (3a) e liberacao manual por secao contra a fracao 90+/100+ (3b). Item 4: secoes com alta fracao de aptos 80+.
Uso: python -I 31_a20b_idosos.py DIR_PARQUET DIR_PARQUET2 DIR_PARQUET3 DIR_FASE3 DIR_SAIDA
  DIR_PARQUET: bu_*.parquet; DIR_PARQUET2: perfil_agg_*.parquet; DIR_PARQUET3: perfil_secao_*.parquet (30_perfil_secao.py);
  DIR_FASE3: results/fase3 (A20_mapa_tse_ibge.csv)."""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_auditoria import KEY, Registro, carrega, base, par_ano, fe_ols, NaoExecutado
from scipy import stats

SEMENTE = 20261029
B90 = ["90 a 94 anos", "95 a 99 anos", "100 anos ou mais"]
B95 = ["95 a 99 anos", "100 anos ou mais"]
B100 = ["100 anos ou mais"]
BANDAS = {"90": B90, "95": B95, "100": B100}
MINPOP = {"90": 10, "100": 5}


def perfil_mun(pq2, ano, turno):
    p = pd.read_parquet(os.path.join(pq2, f"perfil_agg_{ano}.parquet"))
    p = p[(p.NR_TURNO == turno) & (p.SG_UF != "ZZ")].copy()
    p["faixa"] = p.DS_FAIXA_ETARIA.str.strip()
    out = None
    for k, fx in BANDAS.items():
        q = p[p.faixa.isin(fx)].groupby(["SG_UF", "CD_MUNICIPIO"]).agg(**{f"apt{k}": ("QT_APTOS", "sum"), f"comp{k}": ("QT_COMPARECIMENTO", "sum")})
        out = q if out is None else out.join(q, how="outer")
    return out.fillna(0).reset_index()


def item2(pq2, mapa, saida):
    pops = {"90": "pop90+", "100": "pop100+"}
    base_ = {}
    for ano, turno in ((2018, 1), (2018, 2), (2022, 1), (2022, 2), (2026, 1)):
        base_[(ano, turno)] = perfil_mun(pq2, ano, turno).merge(mapa[["SG_UF", "CD_MUNICIPIO", "pop90+", "pop100+"]], on=["SG_UF", "CD_MUNICIPIO"], how="inner")
    linhas, listas, tetos = [], [], []
    nat22 = {k: base_[(2022, 1)][f"comp{k}"].sum() / base_[(2022, 1)][pops[k]].sum() for k in ("90", "100")}
    for (ano, turno), d in base_.items():
        for k in ("90", "100"):
            e = d[d[pops[k]] >= MINPOP[k]]
            r = e[f"comp{k}"] / e[pops[k]]
            r_nat = e[f"comp{k}"].sum() / e[pops[k]].sum()
            linhas.append(dict(ano=ano, turno=turno, faixa=k + "+", municipios_elegiveis=len(e), votantes=int(e[f"comp{k}"].sum()), populacao_censo_2022=int(e[pops[k]].sum()), razao_nacional=r_nat,
                               municipios_votantes_maior_que_populacao=int((r > 1).sum()), fracao_bruta=float((r > 1).mean()), fracao_na_escala_de_2022=float(((r * nat22[k] / r_nat) > 1).mean()),
                               aviso="mesma coorte" if ano == 2022 else "descompasso de coortes (Adendo 9a)"))
            lst = d[d[f"comp{k}"] > d[pops[k]]].copy()
            lst["excesso"] = lst[f"comp{k}"] - lst[pops[k]]
            tetos.append(dict(ano=ano, turno=turno, faixa=k + "+", municipios_na_lista=len(lst), votantes_acima_da_populacao=int(lst.excesso.sum()), votos_de_margem_pior_caso=int(lst.excesso.sum())))
            if (ano, turno) == (2026, 1):
                listas.append(lst.assign(faixa=k + "+", ano=ano, turno=turno)[["ano", "turno", "faixa", "SG_UF", "CD_MUNICIPIO", f"comp{k}", pops[k], "excesso"]].rename(columns={f"comp{k}": "votantes", pops[k]: "populacao_censo_2022"}))
    pd.DataFrame(linhas).to_csv(os.path.join(saida, "A20b_item2_razoes.csv"), index=False)
    pd.DataFrame(tetos).to_csv(os.path.join(saida, "A20b_item2_tetos_pior_caso.csv"), index=False)
    L = pd.concat(listas).sort_values(["faixa", "excesso"], ascending=[True, False])
    L.to_csv(os.path.join(saida, "A20b_item2_lista_municipios_2026T1.csv"), index=False)
    return pd.DataFrame(linhas), pd.DataFrame(tetos), L


def boot_razao(num, den, B=1000):
    rng = np.random.default_rng(SEMENTE)
    n = len(num)
    idx = rng.integers(0, n, size=(B, n))
    return float(np.std(num[idx].sum(axis=1) / den[idx].sum(axis=1), ddof=1))


def item2a(pq2, saida, reg):
    pares = ((2026, 2022), (2022, 2018))
    perf = {a: perfil_mun(pq2, a, 1) for a in (2018, 2022, 2026)}
    # pares: (banda tarde, banda cedo, minimo do denominador)
    defs = [("95+ em y2 / 90+ em y1", "95", "90"), ("100+ em y2 / 95+ em y1", "100", "95")]
    linhas, listas, res = [], [], {}
    for nome, kt, kc in defs:
        for y2, y1 in pares:
            d = perf[y2][["SG_UF", "CD_MUNICIPIO", f"apt{kt}", f"comp{kt}"]].merge(perf[y1][["SG_UF", "CD_MUNICIPIO", f"apt{kc}"]], on=["SG_UF", "CD_MUNICIPIO"], how="inner")
            e = d[d[f"apt{kc}"] >= 10]
            for medida, col in (("aptos", f"apt{kt}"), ("votantes", f"comp{kt}")):
                num, den = e[col].values.astype(float), e[f"apt{kc}"].values.astype(float)
                R = num.sum() / den.sum(); se = boot_razao(num, den)
                viol = num > den; fr = float(viol.mean()); sef = float(np.sqrt(fr * (1 - fr) / len(e)))
                linhas.append(dict(banda=nome, par=f"{y2} contra {y1}", medida=medida, municipios=len(e), R_nacional=R, ep_R=se, fracao_municipios_R_maior_1=fr, ep_fracao=sef,
                                   municipios_R_maior_1=int(viol.sum())))
                res[(nome, y2, medida)] = (R, se, fr, sef)
            # lista e teto: todos os municipios (qualquer denominador) em que votantes de y2 > aptos de y1 na banda anterior
            lst = d[d[f"comp{kt}"] > d[f"apt{kc}"]].copy(); lst["excesso"] = lst[f"comp{kt}"] - lst[f"apt{kc}"]
            res[(nome, y2, "teto")] = (int(lst.excesso.sum()), len(lst))
            if y2 == 2026:
                listas.append(lst.assign(banda=nome)[["banda", "SG_UF", "CD_MUNICIPIO", f"comp{kt}", f"apt{kc}", "excesso"]].rename(columns={f"comp{kt}": "votantes_2026", f"apt{kc}": "aptos_2022_banda_anterior"}))
    T = pd.DataFrame(linhas)
    T.to_csv(os.path.join(saida, "A20b_2a_monotonicidade.csv"), index=False)
    pd.concat(listas).sort_values("excesso", ascending=False).to_csv(os.path.join(saida, "A20b_2a_lista_municipios_2026.csv"), index=False)
    tt = []
    for nome, kt, kc in defs:
        for medida in ("aptos", "votantes"):
            R6, s6, f6, sf6 = res[(nome, 2026, medida)]; R2, s2, f2, sf2 = res[(nome, 2022, medida)]
            zR = (R6 - R2) / np.hypot(s6, s2); zf = (f6 - f2) / np.hypot(sf6, sf2) if np.hypot(sf6, sf2) > 0 else 0.0
            tt.append(dict(banda=nome, medida=medida, R_2026=R6, R_2022=R2, z_R=zR, frac_2026=f6, frac_2022=f2, z_fracao=zf, excesso_formal=bool(zR > 2 or zf > 2)))
        # registro: so a medida 'votantes' (a regra do cadastro nao cancela facultativo; o aptos fica descritivo)
        R6, s6, f6, sf6 = res[(nome, 2026, "votantes")]; R2, s2, f2, sf2 = res[(nome, 2022, "votantes")]
        teto6, n6 = res[(nome, 2026, "teto")]; teto2, n2 = res[(nome, 2022, "teto")]
        zR = (R6 - R2) / np.hypot(s6, s2); zf = (f6 - f2) / np.hypot(sf6, sf2) if np.hypot(sf6, sf2) > 0 else 0.0
        pf1 = 1.0 if f6 <= f2 else float(stats.norm.sf(zf))
        reg.add_raw("A20b-2a", f"monotonicidade de coortes, votantes {nome}: razao nacional 2026 contra 2022", R6, s6, float(stats.norm.sf(zR)), p_bruto=float(2 * stats.norm.sf(abs(zR))), votos=np.nan, votos_pior=float(teto6),
                    nota=f"teto = soma do excesso de votantes sobre os aptos da banda anterior em {n6} municipios (2022: {teto2} votantes em {n2} municipios); gross, sem descontar migracao", comp="2022 contra 2018",
                    placebos=f"2022: R {R2:.4f} (ep {s2:.4f})", sentido="PT+OPO")
        reg.add_raw("A20b-2a", f"monotonicidade de coortes, votantes {nome}: fracao de municipios com R>1, 2026 contra 2022", f6, sf6, pf1, p_bruto=float(2 * stats.norm.sf(abs(zf))), comp="2022 contra 2018",
                    placebos=f"2022: {f2:.4f} (ep {sf2:.4f})", sentido="PT+OPO")
    pd.DataFrame(tt).to_csv(os.path.join(saida, "A20b_2a_veredito_formal.csv"), index=False)
    return T, pd.DataFrame(tt)


def item3a(pq3, saida):
    linhas = []
    for ano in (2018, 2022, 2026):
        f = pd.read_parquet(os.path.join(pq3, f"perfil_faixas_{ano}.parquet"))
        f = f[f.SG_UF != "ZZ"]
        grupo = np.where(f.faixa.isin(B100), "100+", np.where(f.faixa.isin(B90), "90+ (inclui 100+)", "outras"))
        f["grupo"] = grupo
        for g_ in ("100+", "90+ (inclui 100+)"):
            sub = f[(f.faixa.isin(B100) if g_ == "100+" else f.faixa.isin(B90))]
            linhas.append(dict(ano=ano, grupo=g_, aptos=int(sub.apt.sum()), com_biometria=int(sub.bio.sum()), pct_biometria=100 * sub.bio.sum() / sub.apt.sum()))
        ok = f[~f.faixa.isin(B90) & f.faixa.str.contains("anos", na=False)]
        linhas.append(dict(ano=ano, grupo="16 a 89 anos", aptos=int(ok.apt.sum()), com_biometria=int(ok.bio.sum()), pct_biometria=100 * ok.bio.sum() / ok.apt.sum()))
    R = pd.DataFrame(linhas)
    R.to_csv(os.path.join(saida, "A20b_3a_biometria_cadastrada_por_faixa.csv"), index=False)
    return R


def junta_perfil(d, pq3, ano):
    s = pd.read_parquet(os.path.join(pq3, f"perfil_secao_{ano}.parquet")).drop(columns=["NR_LOCAL_VOTACAO"])
    m = d.merge(s, on=KEY, how="inner")
    m = m[m.apt > 0].copy()
    m["share80"] = m.apt80 / m.apt; m["share90"] = m.apt90 / m.apt; m["share100"] = m.apt100 / m.apt; m["share_sem_bio"] = 1 - m.bio / m.apt
    return m, len(m) / max(len(d), 1)


def item3b_4(D, pq3, saida, reg, reg_pos):
    amostras = {}
    cobertura = []
    for ano in (2026, 2022, 2018):
        w = par_ano(D, ano)
        w["dir_sh"] = 1 - w.lula_sh
        w["dir_sh_t1"] = w.dir_t1 / w.valid2_t1
        m, cob = junta_perfil(w, pq3, ano)
        amostras[(ano, 2)] = m; cobertura.append(dict(ano=ano, turno=2, secoes_base=len(w), secoes_com_perfil=len(m), pct=100 * cob))
        b1 = base(D[(ano, 1)]).copy()
        m1, cob1 = junta_perfil(b1, pq3, ano)
        amostras[(ano, 1)] = m1; cobertura.append(dict(ano=ano, turno=1, secoes_base=len(b1), secoes_com_perfil=len(m1), pct=100 * cob1))
    pd.DataFrame(cobertura).to_csv(os.path.join(saida, "A20b_cobertura_perfil_secao.csv"), index=False)
    # item 3b
    def reg_(m, y, xs):
        try:
            r = fe_ols(m, y, xs, "uf_local")
            return r
        except ValueError as e:
            print("falha:", y, xs, e); return None
    linhas = []
    X3 = ["share90", "share100", "share_sem_bio"]
    rr = {k: reg_(amostras[k], "manual_rate", X3) for k in ((2026, 2), (2026, 1), (2022, 2), (2018, 2))}
    for k, r in rr.items():
        if r is not None:
            for x in ("share90", "share100"):
                linhas.append(dict(item="3b", desfecho="manual_rate", termo=x, ano=k[0], turno=k[1], coef=float(r.loc[x, "coef"]), ep=float(r.loc[x, "se"]), n=int(r.n.iloc[0]), locais=int(r.grupos.iloc[0])))
    if rr[(2026, 2)] is not None and all(rr[k] is not None for k in ((2026, 1), (2022, 2), (2018, 2))):
        for x, nome in (("share90", "aptos 90+ (inclui 100+)"), ("share100", "aptos 100+ (adicional)")):
            reg.add("A20b-3b", f"liberacao manual do BU contra a fracao de {nome} da secao (EF de local, controle de biometria cadastrada)", float(rr[(2026, 2)].loc[x, "coef"]), float(rr[(2026, 2)].loc[x, "se"]),
                    [(n_, float(rr[k].loc[x, "coef"]), float(rr[k].loc[x, "se"])) for n_, k in (("2026/T1", (2026, 1)), ("2022/T2", (2022, 2)), ("2018/T2", (2018, 2)))], sentido="PT+OPO",
                    nota="proxy ecologico por secao (a idade individual de quem foi liberado manualmente nao e publica); sem conversao em votos")
    # item 4
    m26 = amostras[(2026, 2)]
    desfechos = [("lula_sh", ["share80", "lula_sh_t1", "turnout"], "PT", 2.0, lambda m: float((m.valid2 * m.share80).sum()), "participacao de Lula nos votos validos"),
                 ("dir_sh", ["share80", "dir_sh_t1", "turnout"], "OPO", 2.0, lambda m: float((m.valid2 * m.share80).sum()), "participacao de Flavio nos votos validos"),
                 ("turnout", ["share80", "turnout_t1"], "PT+OPO", 1.0, lambda m: float((m.QT_APTOS * m.share80).sum()), "comparecimento")]
    for y, xs, sent, fator, expf, nome in desfechos:
        r26 = reg_(m26, y, xs)
        plac = []
        for k in ((2022, 2), (2018, 2)):
            r = reg_(amostras[k], y, xs)
            if r is not None:
                plac.append((f"{k[0]}/T{k[1]}", float(r.loc["share80", "coef"]), float(r.loc["share80", "se"])))
        if y == "turnout":
            r1 = reg_(amostras[(2026, 1)], "turnout", ["share80"])
            if r1 is not None:
                plac.append(("2026/T1 (sem controle)", float(r1.loc["share80", "coef"]), float(r1.loc["share80", "se"])))
        for n_, b_, s_ in plac:
            linhas.append(dict(item="4", desfecho=y, termo="share80", ano=int(n_[:4]), turno=int(n_[6]), coef=b_, ep=s_, n=np.nan, locais=np.nan))
        if r26 is not None:
            linhas.append(dict(item="4", desfecho=y, termo="share80", ano=2026, turno=2, coef=float(r26.loc["share80", "coef"]), ep=float(r26.loc["share80", "se"]), n=int(r26.n.iloc[0]), locais=int(r26.grupos.iloc[0])))
        if r26 is not None and len(plac) >= 2:
            reg.add("A20b-4", f"{nome} contra a fracao de aptos 80+ da secao (EF de local, controle do 1o turno)", float(r26.loc["share80", "coef"]), float(r26.loc["share80", "se"]), plac, expo=expf(m26), fator=fator, sentido=sent,
                    nota="coeficiente por unidade de fracao 80+; teto = efeito restrito as secoes de 2026 da amostra, atribuindo a diferenca ao oponente do placebo mais frouxo; nao e estimativa")
            if y == "turnout":     # Adendo 9d: linha suplementar sem o comparador sem controle (2026/T1)
                ctrl = [p_ for p_ in plac if "sem controle" not in p_[0]]
                reg_pos.add("A20b-4-suplementar", f"{nome} contra a fracao de aptos 80+ da secao, so placebos controlados (2022/T2 e 2018/T2)", float(r26.loc["share80", "coef"]), float(r26.loc["share80", "se"]), ctrl, expo=expf(m26), fator=fator, sentido=sent,
                            nota="Adendo 9d: suplementar, nao substitui a linha pre-registrada; Soma de aptos 80+ nas secoes da amostra = expo; nao e estimativa")
    pd.DataFrame(linhas).to_csv(os.path.join(saida, "A20b_3b_4_coeficientes.csv"), index=False)
    # descritivo: decil superior da fracao 80+ dentro da UF
    desc = []
    for (ano, t), m in amostras.items():
        m = m.copy()
        m["top"] = m.share80 >= m.groupby("SG_UF").share80.transform(lambda s: s.quantile(.9))
        for flag, g in m.groupby("top"):
            w = g.valid2
            desc.append(dict(ano=ano, turno=t, grupo="decil superior de aptos 80+ dentro da UF" if flag else "demais secoes", secoes=len(g), aptos=int(g.QT_APTOS.sum()), share80_medio=float(g.share80.mean()),
                             comparecimento_pct=100 * float(g.QT_COMPARECIMENTO.sum() / g.QT_APTOS.sum()), lula_pct_validos=100 * float((g.lula_sh * w).sum() / w.sum()),
                             manual_rate_medio=float(g.manual_rate.mean())))
    pd.DataFrame(desc).to_csv(os.path.join(saida, "A20b_4_descritivo_decil_superior.csv"), index=False)
    return pd.DataFrame(linhas), pd.DataFrame(desc)


def main(pq, pq2, pq3, f3, saida):
    os.makedirs(saida, exist_ok=True)
    mapa = pd.read_csv(os.path.join(f3, "A20_mapa_tse_ibge.csv"), dtype={"cod_ibge": str}).dropna(subset=["cod_ibge"])
    for a in (2018, 2022, 2026):
        if not os.path.exists(os.path.join(pq3, f"perfil_secao_{a}.parquet")):
            raise NaoExecutado(f"falta perfil_secao_{a}.parquet (rodar 30_perfil_secao.py)")
    D = carrega(pq, (2018, 2022, 2026))
    reg = Registro(); reg_pos = Registro()
    R2, T2, L2 = item2(pq2, mapa, saida)
    T2a, V2a = item2a(pq2, saida, reg)
    R3 = item3a(pq3, saida)
    C4, DD = item3b_4(D, pq3, saida, reg, reg_pos)
    fr = reg.frame()
    fr.to_csv(os.path.join(saida, "A20b_testes.csv"), index=False)
    fp = reg_pos.frame(); fp.to_csv(os.path.join(saida, "A20b_4_suplementar_adendo9d.csv"), index=False)
    print(fp[["H", "teste", "est_2026T2", "placebos", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].to_string())
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(R2.round(4).to_string()); print(T2.to_string()); print(T2a.round(4).to_string()); print(V2a.round(3).to_string()); print(R3.round(2).to_string())
    print(C4.round(5).to_string()); print(DD.round(3).to_string())
    print(fr[["H", "teste", "est_2026T2", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].to_string())


if __name__ == "__main__":
    main(*sys.argv[1:6])
