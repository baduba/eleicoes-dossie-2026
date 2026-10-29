"""Fase 2: A6 (urna substituida), A8 (coerencia entre cargos), A9 (perfil do comparecimento), A10 (modelo da urna, exterior). Pre-registro: Adendo 4."""
import glob
import os
import zipfile
import numpy as np
import pandas as pd
from scipy import stats
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, par_ano, fe_ols
from h1_h4 import tenta


# ------------------------------------------------------------------------------------------------------- A6
def _cesp(dirp, ano):
    zs = sorted(glob.glob(os.path.join(dirp, f"CESP_2t_*_*{ano}*.zip")))
    zs = [z for z in zs if (ano == 2026 and "_24102026" in z) or (ano == 2022 and "_30102022" in z)]
    if len(zs) != 28:
        raise NaoExecutado(f"A6: esperava 28 zips CESP de {ano}, achei {len(zs)} em {dirp}")
    partes = []
    for z in zs:
        zf = zipfile.ZipFile(z)
        nomes = [n for n in zf.namelist() if n.lower().endswith(".csv") and "contingen" not in n.lower()]
        if not nomes:
            raise NaoExecutado(f"A6: {z} sem CSV de correspondencia por secao: {zf.namelist()}")
        with zf.open(nomes[0]) as f:
            d = pd.read_csv(f, sep=";", encoding="latin-1", usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_URNA_ESPERADA"], dtype=str)
        partes.append(d)
    d = pd.concat(partes, ignore_index=True)
    for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_URNA_ESPERADA"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d.dropna().astype({"NR_URNA_ESPERADA": int}).drop_duplicates(KEY)


def a6(D, reg, out):
    cdir = os.path.join(out["_parquet"], "..", "cesp") if not os.path.exists(os.path.join(out["_parquet"], "cesp")) else os.path.join(out["_parquet"], "cesp")
    cdir = out.get("_cesp") or cdir
    res, linhas = {}, []
    for ano in (2026, 2022):
        ce = _cesp(cdir, ano)
        w = par_ano(D, ano, minvalid=30)
        w = w.merge(ce, on=KEY, how="left")
        n_sem = int(w.NR_URNA_ESPERADA.isna().sum())
        w = w[w.NR_URNA_ESPERADA.notna()].copy()
        w["subst"] = (w.NR_URNA_ESPERADA.astype(int) != w.NR_URNA.astype(int)).astype(float)
        linhas.append(dict(ano=ano, secoes=len(w), sem_correspondencia=n_sem, urna_diferente_da_esperada=int(w.subst.sum()), pct=100 * w.subst.mean()))
        r1 = tenta(out, f"A6 {ano} lula_sh|T1", fe_ols, w, "lula_sh", ["subst", "lula_sh_t1"], "uf_local")
        r2 = tenta(out, f"A6 {ano} turnout|T1", fe_ols, w, "turnout", ["subst", "turnout_t1"], "uf_local")
        r3 = tenta(out, f"A6 {ano} lula_sh T1 sem lag", fe_ols, w, "lula_sh_t1", ["subst"], "uf_local")
        res[ano] = (r1, r2, r3, w)
    out["a6_substituicao"] = pd.DataFrame(linhas)
    rows = []
    for ano, (r1, r2, r3, w) in res.items():
        for nome, r in (("Lula% T2 | T1", r1), ("comparecimento T2 | T1", r2), ("Lula% T1 (mesmas secoes, sem lag)", r3)):
            if r is not None:
                rows.append(dict(ano=ano, spec=nome, coef=float(r.loc["subst", "coef"]), ep=float(r.loc["subst", "se"]), secoes_substituidas=int(w.subst.sum()), n=int(r.n.iloc[0])))
    out["a6_coef"] = pd.DataFrame(rows)
    if res[2026][0] is None or res[2022][0] is None:
        raise NaoExecutado("A6: regressao nao estimada")
    b26, s26 = float(res[2026][0].loc["subst", "coef"]), float(res[2026][0].loc["subst", "se"])
    b22, s22 = float(res[2022][0].loc["subst", "coef"]), float(res[2022][0].loc["subst", "se"])
    pl = [("2022/T2", b22, s22)]
    if res[2026][2] is not None:
        pl.append(("2026/T1 (mesmas secoes)", float(res[2026][2].loc["subst", "coef"]), float(res[2026][2].loc["subst", "se"])))
    w26 = res[2026][3]
    reg.add("A6", "urna efetivada diferente da esperada: Lula% no T2 dado o T1, EF de local", b26, s26, pl, expo=float(w26[w26.subst == 1].valid2.sum()), fator=2.0,
            nota="urna esperada: CESP do TSE; efetivada: BWeb")


# ------------------------------------------------------------------------------------------------------- A8
def a8(D, reg, out):
    rows = []
    for ano in (2018, 2022, 2026):
        for t in (1, 2):
            p = os.path.join(out["_parquet2"], f"cargos_{ano}_t{t}.parquet")
            if not os.path.exists(p):
                raise NaoExecutado(f"A8: falta {p} (rodar 05_extras_bweb.py)")
            d = pd.read_parquet(p)
            d["tot"] = d[["t1", "t2", "t3", "t4", "t5", "tout"]].sum(axis=1)
            d["comp"] = pd.to_numeric(d.comp)
            d = d[d.comp > 0]
            for c, g in d.groupby("CD_CARGO_PERGUNTA"):
                r = (g.tot / g.comp).round(6); modo = float(r.mode().iloc[0])
                rows.append(dict(ano=ano, turno=t, cargo=c, secoes=len(g), razao_total_por_comparecimento_modal=modo, secoes_na_regra=int((r == modo).sum()), secoes_fora_da_regra=int((r != modo).sum())))
    tab = pd.DataFrame(rows); out["a8_cargos"] = tab
    f = lambda a: int(tab[(tab.ano == a)].secoes_fora_da_regra.sum())
    reg.add_raw("A8", "secoes com total de algum cargo diferente da regra (total = comparecimento x vagas), 2026 T1+T2", float(f(2026)), 0.0, 1.0 if f(2026) <= max(f(2018), f(2022)) else 0.0,
                nota="regra por cargo = razao modal (1 para cargos de um voto; 2 no Senado de 2018 e 2026); placebos 2018 e 2022", placebos=f"2018: {f(2018)} | 2022: {f(2022)}", comp="2018 e 2022")


# ------------------------------------------------------------------------------------------------------- A9
def a9(D, reg, out):
    ag = {}
    for ano in (2018, 2022, 2026):
        p = os.path.join(out["_parquet2"], f"perfil_agg_{ano}.parquet")
        if not os.path.exists(p):
            raise NaoExecutado(f"A9: falta {p} (rodar 07_perfil_agrega.py)")
        ag[ano] = pd.read_parquet(p)
    if 2 not in set(ag[2026].NR_TURNO.unique()):
        out.setdefault("nao_executados", []).append(("A9 T1->T2 2026", "o perfil de comparecimento e abstencao de 2026 foi publicado em 21/10/2026 e so tem o 1o turno; a variacao T1->T2 por faixa etaria nao pode ser calculada"))
        print("NAO EXECUTADO [A9 T1->T2 2026]: perfil de 2026 so tem o 1o turno", flush=True)
    cel, tot, out_rows, fac = [], [], [], []
    for ano, a in ag.items():
        for t, g in a.groupby("NR_TURNO"):
            cel.append(dict(ano=ano, turno=int(t), celulas=len(g), comparecimento_maior_que_aptos=int((g.QT_COMPARECIMENTO > g.QT_APTOS).sum()),
                            comp_mais_abst_diferente_de_aptos=int((g.QT_COMPARECIMENTO + g.QT_ABSTENCAO != g.QT_APTOS).sum()),
                            facultativo_obrigatorio_soma_diferente=int((g.QT_COMPAREC_FACULTATIVO + g.QT_COMPAREC_OBRIGATORIO != g.QT_COMPARECIMENTO).sum())))
            # consistencia com o BWeb por UF x municipio x zona
            b = D[(ano, int(t))] if (ano, int(t)) in D else None
            if b is not None:
                bz = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")].groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])[["QT_APTOS", "QT_COMPARECIMENTO"]].sum().reset_index()
                pz = g.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])[["QT_APTOS", "QT_COMPARECIMENTO"]].sum().reset_index()
                pz["CD_MUNICIPIO"] = pd.to_numeric(pz.CD_MUNICIPIO, errors="coerce")
                m = bz.merge(pz, on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA"], suffixes=("_bweb", "_perfil"), how="outer", indicator=True)
                amb = m[m._merge == "both"]
                tot.append(dict(ano=ano, turno=int(t), zonas_pareadas=len(amb), so_bweb=int((m._merge == "left_only").sum()), so_perfil=int((m._merge == "right_only").sum()),
                                zonas_comp_diferente=int((amb.QT_COMPARECIMENTO_bweb != amb.QT_COMPARECIMENTO_perfil).sum()), zonas_aptos_diferente=int((amb.QT_APTOS_bweb != amb.QT_APTOS_perfil).sum()),
                                soma_abs_dif_comp=int((amb.QT_COMPARECIMENTO_bweb - amb.QT_COMPARECIMENTO_perfil).abs().sum())))
            # taxa de comparecimento por faixa etaria (nacional)
            f = g.groupby("DS_FAIXA_ETARIA")[["QT_APTOS", "QT_COMPARECIMENTO"]].sum()
            f["taxa"] = f.QT_COMPARECIMENTO / f.QT_APTOS
            for k, r in f.iterrows():
                fac.append(dict(ano=ano, turno=int(t), faixa=k, aptos=int(r.QT_APTOS), taxa_comparecimento=float(r.taxa)))
    out["a9_celulas"] = pd.DataFrame(cel); out["a9_consistencia_bweb"] = pd.DataFrame(tot)
    ft = pd.DataFrame(fac)
    out["a9_taxa_por_faixa"] = ft.pivot_table(index="faixa", columns=["ano", "turno"], values="taxa_comparecimento").round(4).reset_index()
    # aptos e comparecimento por faixa etaria: 2026/T1 contra 2022/T1 e 2018/T1 (descritivo)
    comp_f = []
    for ano in (2018, 2022, 2026):
        g = ag[ano][ag[ano].NR_TURNO == 1].groupby("DS_FAIXA_ETARIA")[["QT_APTOS", "QT_COMPARECIMENTO"]].sum()
        g.columns = [f"aptos_{ano}", f"comp_{ano}"]; comp_f.append(g)
    cf = pd.concat(comp_f, axis=1).reset_index()
    cf["aptos_2026_sobre_2022"] = cf.aptos_2026 / cf.aptos_2022; cf["comp_2026_sobre_2022"] = cf.comp_2026 / cf.comp_2022
    out["a9_aptos_comp_por_faixa_T1"] = cf.round(4)
    # variacao T1->T2 por faixa nos placebos (contexto) e outliers de zona nos grupos facultativos (so T1, unico turno comparavel de 2026)
    var = {}
    for ano in (2018, 2022):
        p = ft[ft.ano == ano].pivot_table(index="faixa", columns="turno", values="taxa_comparecimento")
        var[ano] = (p[2] / p[1] - 1)
    out["a9_variacao_T1_T2_placebos"] = pd.DataFrame(var).round(4).reset_index()
    if 2018 in var and 2022 in var:
        out["a9_corr_variacao_2018_2022"] = float(np.corrcoef(var[2018].reindex(var[2022].index).fillna(0), var[2022].fillna(0))[0, 1])
    # zonas com comparecimento facultativo fora de [Q1-3IQR, Q3+3IQR] da referencia 2022/T1
    def taxa_fac(a, t):
        g = a[a.NR_TURNO == t].copy()
        z = g.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])[["QT_APTOS", "QT_COMPAREC_FACULTATIVO", "QT_ABST_FACULTATIVO"]].sum()
        z["fac_aptos"] = z.QT_COMPAREC_FACULTATIVO + z.QT_ABST_FACULTATIVO
        z = z[z.fac_aptos >= 30]
        return (z.QT_COMPAREC_FACULTATIVO / z.fac_aptos)
    ref = taxa_fac(ag[2022], 1); q1, q3 = ref.quantile([.25, .75]); lo, hi = q1 - 3 * (q3 - q1), q3 + 3 * (q3 - q1)
    ol = []
    for ano, t in ((2022, 1), (2022, 2), (2018, 1), (2018, 2), (2026, 1)):
        x = taxa_fac(ag[ano], t); ol.append(dict(ano=ano, turno=t, zonas=len(x), fora_do_intervalo=int(((x < lo) | (x > hi)).sum()), pct=100 * float(((x < lo) | (x > hi)).mean()),
                                                  acima=int((x > hi).sum()), abaixo=int((x < lo).sum()), limites=f"[{lo:.3f}, {hi:.3f}]"))
    out["a9_zonas_facultativo_outliers"] = pd.DataFrame(ol)
    o = pd.DataFrame(ol).set_index(["ano", "turno"])
    p26 = o.loc[(2026, 1), "pct"] / 100; n26 = o.loc[(2026, 1), "zonas"]
    pls = []
    for k in ((2022, 1), (2018, 1)):
        p = o.loc[k, "pct"] / 100; pls.append((f"{k[0]}/T{k[1]}", 100 * p, 100 * float(np.sqrt(p * (1 - p) / o.loc[k, "zonas"]))))
    reg.add("A9", "zonas com comparecimento facultativo fora de [Q1-3 IQR, Q3+3 IQR] de 2022/T1 (% das zonas), so 1o turno", 100 * p26, 100 * float(np.sqrt(p26 * (1 - p26) / n26)), pls,
            nota="so T1: o perfil de 2026/T2 nao foi publicado")


# ------------------------------------------------------------------------------------------------------- A10
def a10(D, reg, out):
    mod = {a: pd.read_parquet(os.path.join(out["_parquet"], f"modelo_urna_{a}.parquet")) for a in (2022, 2026)}
    rows = []
    for ano in (2022, 2026):
        w = par_ano(D, ano, minvalid=30)
        w = w.merge(mod[ano][mod[ano].NR_TURNO == 2][KEY + ["CD_MODELO_URNA"]], on=KEY, how="left")
        w = w[w.CD_MODELO_URNA.notna() & (w.CD_MODELO_URNA > 0)].copy()
        ref = 2020
        dums = []
        for m in sorted(w.CD_MODELO_URNA.unique()):
            if m != ref:
                w[f"m{int(m)}"] = (w.CD_MODELO_URNA == m).astype(float); dums.append(f"m{int(m)}")
        r2 = tenta(out, f"A10 {ano} T2|T1", fe_ols, w, "lula_sh", dums + ["lula_sh_t1"], "uf_local")
        r1 = tenta(out, f"A10 {ano} T1", fe_ols, w, "lula_sh_t1", dums, "uf_local")
        for dm in dums:
            for nome, r in (("Lula% T2 dado T1", r2), ("Lula% T1", r1)):
                if r is not None:
                    rows.append(dict(ano=ano, modelo=dm[1:], spec=nome, coef=float(r.loc[dm, "coef"]), ep=float(r.loc[dm, "se"]), secoes=int(w[dm].sum())))
        if ano == 2026:
            w26 = w
    out["a10_modelo_urna"] = pd.DataFrame(rows)
    t = out["a10_modelo_urna"]
    for m in ("2013", "2015", "2022"):
        a = t[(t.ano == 2026) & (t.modelo == m) & (t.spec == "Lula% T2 dado T1")]
        b = t[(t.ano == 2026) & (t.modelo == m) & (t.spec == "Lula% T1")]
        if len(a) and len(b):
            reg.add("A10", f"modelo de urna UE{m} contra UE2020, mesmo local: Lula% no T2 dado o T1", float(a.coef.iloc[0]), float(a.ep.iloc[0]),
                    [("2026/T1 (sem lag, mesmas secoes)", float(b.coef.iloc[0]), float(b.ep.iloc[0]))], expo=float(w26[w26[f"m{m}"] == 1].valid2.sum()), fator=2.0,
                    nota="UE2022 e modelo novo em 2026 (sem equivalente em 2022)")
    # exterior contra nacional (descritivo)
    ex = []
    for ano in (2018, 2022, 2026):
        for t_ in (1, 2):
            d = D[(ano, t_)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
            for rot, g in (("exterior (ZZ)", d[d.SG_UF == "ZZ"]), ("Brasil", d[d.SG_UF != "ZZ"])):
                ex.append(dict(ano=ano, turno=t_, recorte=rot, secoes=len(g), pt_pct_dos_dois=100 * g.lula.sum() / (g.lula.sum() + g["dir"].sum()), comparecimento=g.QT_COMPARECIMENTO.sum() / g.QT_APTOS.sum() * 100,
                               pct_secoes_comparecimento_ge95=100 * float((g.turnout >= .95).mean())))
    out["a10_exterior"] = pd.DataFrame(ex).round(3)
    out["a10_nota"] = ("A estacao de geracao da carga (CD_FLASHCARD) nao foi analisada nesta versao. "
                       "A versao de software por secao so existe no log da urna (amostra, ver A4/A5).")


# ------------------------------------------------------------------------------------------------------- A7
def a7(D, reg, out):
    """Contexto (sem veredito): erro das ultimas pesquisas publicadas contra o resultado. So entram resultados com fonte em data/pesquisas_fontes.csv."""
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "pesquisas_fontes.csv")
    if not os.path.exists(p):
        raise NaoExecutado(f"A7: falta {p}")
    pf = pd.read_csv(p)
    real = {}
    for ano in (2018, 2022, 2026):
        d = D[(ano, 2)]; d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
        real[ano] = 100 * d.lula.sum() / (d.lula.sum() + d["dir"].sum())
    pf["pt_pct_validos_resultado"] = pf.ano.map(real)
    pf["erro_pp_pt"] = pf.pt_pct_validos_pesquisa - pf.pt_pct_validos_resultado
    pf["fora_da_margem_declarada"] = pf.erro_pp_pt.abs() > pf.margem_erro_declarada_pp
    out["a7_pesquisas"] = pf.round(2)
    out.setdefault("nao_executados", []).append(("A7 2014 e demais institutos", "nao foi localizada, com fonte, uma pesquisa final de 2014 com data confirmada; Quaest e Paraná Pesquisas de 24/10/2026 nao foram localizadas com resultado; o TSE publica so o registro das pesquisas, sem resultados"))
    print("NAO EXECUTADO [A7 parcial]: so Datafolha 2018, 2022, 2026 e AtlasIntel 2026 tem resultado com fonte", flush=True)
