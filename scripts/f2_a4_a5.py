"""Fase 2: A4 (cadeia da urna: BU, RDV, hashes, software) e A5 (logs de urna). Pre-registro: Adendo 4.
Entrada: parquets de 08_arquivos_urna.py (urna_out/*) + amostra_estratos.parquet + BWeb."""
import glob
import os
import numpy as np
import pandas as pd
from scipy import stats
from lib_auditoria import KEY, MARGEM, NaoExecutado, base, fe_ols
from h1_h4 import tenta


def _carrega(urna_dir, ano):
    fs = sorted(glob.glob(os.path.join(urna_dir, f"*_{ano}_t2.parquet")))
    if not fs:
        raise NaoExecutado(f"A4/A5: nenhum parquet de arquivos de urna de {ano} em {urna_dir} (rodar 08_arquivos_urna.py)")
    d = pd.concat([pd.read_parquet(f) for f in fs], ignore_index=True)
    return d.rename(columns={"uf": "SG_UF", "cd_municipio": "CD_MUNICIPIO", "zona": "NR_ZONA", "secao": "NR_SECAO"})


def _junta(D, u, ano):
    b = D[(ano, 2)]
    cols = KEY + ["QT_APTOS", "QT_COMPARECIMENTO", "lula", "dir", "branco", "nulo", "biom_nh", "atraso_min", "DT_EMISSAO_BU", "uf_local", "valid2", "lula_sh", "ab_nominal_min"]
    return u.merge(b[cols], on=KEY, how="left")


def a4(D, reg, out):
    ud = out.get("_urna")
    if not ud:
        raise NaoExecutado("A4: informe --urna com o diretorio dos parquets de arquivos de urna")
    linhas, divs = [], []
    ms = {}
    for ano in (2026, 2022):
        u = _carrega(ud, ano); m = _junta(D, u, ano)
        err = [c for c in m.columns if c.startswith("erro")]
        com_erro = int(m[err].notna().any(axis=1).sum()) if err else 0
        m = m[m.QT_COMPARECIMENTO.notna()]
        def _enum3(x):
            for kv in str(x or "").split(";"):
                if kv.startswith("3:"):
                    return int(kv.split(":")[1])
            return 0
        m["rdv_branco"] = m.rdv_enum_sem_numero.map(_enum3)      # tipo 3 sem numero = branco (validado em RR: soma igual ao BU); nulos = total - lula - oponente - brancos
        ok = lambda a, b: (m[a] == m[b])
        d_bu = ~(ok("bu_lula", "lula") & ok("bu_dir", "dir") & ok("bu_branco", "branco") & ok("bu_nulo", "nulo") & ok("bu_total_cargo1", "QT_COMPARECIMENTO"))
        d_rdv = ~(ok("rdv_lula", "bu_lula") & ok("rdv_dir", "bu_dir") & ok("rdv_total", "bu_total_cargo1") & ok("rdv_branco", "bu_branco"))
        d_hash = ~(m.lista_hash_ok & m.bu_hash_na_lista & m.rdv_hash_na_lista & m.imgbu_hash_na_lista & m.log_hash_na_lista)
        linhas.append(dict(ano=ano, secoes=len(m), secoes_com_erro_de_leitura=com_erro, UFs=m.SG_UF.nunique(),
                           bu_diferente_do_bweb=int(d_bu.sum()), rdv_diferente_do_bu=int(d_rdv.sum()), hash_nao_vinculado=int(d_hash.sum()),
                           versoes_software=";".join(f"{k} ({v})" for k, v in m.versao.value_counts().items()), assin_app_falhas_no_log=int(m.assin_app_falha.sum())))
        for r in m[d_bu | d_rdv | d_hash].itertuples():
            divs.append(dict(ano=ano, uf=r.SG_UF, cd_municipio=r.CD_MUNICIPIO, zona=r.NR_ZONA, secao=r.NR_SECAO, bu_diferente=bool(d_bu.loc[r.Index]), rdv_diferente=bool(d_rdv.loc[r.Index]), hash_nao_vinculado=bool(d_hash.loc[r.Index])))
        ms[ano] = (m, d_bu, d_rdv, d_hash)
    out["a4_resumo"] = pd.DataFrame(linhas)
    out["a4_divergencias"] = pd.DataFrame(divs, columns=["ano", "uf", "cd_municipio", "zona", "secao", "bu_diferente", "rdv_diferente", "hash_nao_vinculado"])
    # emissao do BU contra BWeb e carga (2026)
    m26 = ms[2026][0]
    em = pd.to_datetime(m26.bu_emissao, format="%Y%m%dT%H%M%S", errors="coerce")
    out["a4_emissao_igual_bweb"] = dict(secoes=int(len(m26)), iguais=int((em == m26.DT_EMISSAO_BU).sum()))
    out["a4_nota"] = ("Verificado: (c) BU digital = BWeb; (b) RDV recontado = BU (Lula, oponente, total, brancos); vinculo de integridade: SHA-512 de BU, RDV, imagem e log constam da lista assinada pela urna e o "
                      "SHA-512 da lista confere. NAO verificado: (a) a assinatura criptografica em si (a chave da urna usa a curva com OID 1.3.6.1.4.1.44588.2.1, sem suporte em bibliotecas padrao, e a "
                      "especificacao ASN.1 do TSE nao e acessivel por automacao: tse.jus.br responde 403) e (d) a identificacao do software contra a publicada na lacracao (so e possivel listar a versao registrada no log).")
    n26, n22 = len(ms[2026][0]), len(ms[2022][0])
    d26 = int((ms[2026][1] | ms[2026][2] | ms[2026][3]).sum()); d22 = int((ms[2022][1] | ms[2022][2] | ms[2022][3]).sum())
    p = 1.0 if d26 <= d22 * n26 / max(n22, 1) else float(stats.poisson.sf(d26 - 1, max(d22, 0.5) * n26 / max(n22, 1)))
    reg.add_raw("A4", "secoes com BU, RDV ou vinculo de hash divergentes (amostra de arquivos de urna, 2026/T2)", float(d26), 0.0, p, placebos=f"2022/T2 mesmas secoes: {d22} de {n22}",
                comp="2022/T2", nota=f"{d26} divergencias em {n26} secoes de 2026")


def a5(D, reg, out):
    ud = out.get("_urna")
    if not ud:
        raise NaoExecutado("A5: informe --urna")
    est = pd.read_parquet(os.path.join(os.path.dirname(os.path.normpath(ud)), "amostra", "amostra_estratos.parquet")) if os.path.exists(os.path.join(os.path.dirname(os.path.normpath(ud)), "amostra", "amostra_estratos.parquet")) else None
    ms = {}
    for ano in (2026, 2022):
        m = _junta(D, _carrega(ud, ano), ano)
        m = m[m.QT_COMPARECIMENTO.notna()].copy()
        m["cont"] = m.get("ev_contingencia_urna", 0)
        m["cont"] = m["cont"].fillna(0) > 0
        ms[ano] = m
    linhas, excecoes = [], []
    for ano, m in ms.items():
        igual = m.n_computado == m.QT_COMPARECIMENTO
        ex = m[~igual]
        linhas.append(dict(ano=ano, secoes=len(m), votos_computados_log_igual_comparecimento=int(igual.sum()), pct=100 * igual.mean(), divergentes=len(ex), divergentes_com_urna_de_contingencia=int(ex.cont.sum()),
                           divergentes_sem_contingencia=int((~ex.cont).sum()), habilitado_maior_que_comparecimento=int((m.n_habilitado > m.QT_COMPARECIMENTO).sum()),
                           habilitado_menor_que_comparecimento=int((m.n_habilitado < m.QT_COMPARECIMENTO).sum()), gap_minimo_entre_habilitacoes_s=float(m.min_gap_hab_s.min()),
                           secoes_com_gap_menor_10s=int((m.n_gap_lt_10s > 0).sum())))
        for r in ex[~ex.cont].itertuples():
            excecoes.append(dict(ano=ano, uf=r.SG_UF, cd_municipio=r.CD_MUNICIPIO, zona=r.NR_ZONA, secao=r.NR_SECAO, comparecimento=r.QT_COMPARECIMENTO, computado_log=r.n_computado, habilitado_log=r.n_habilitado))
    out["a5_log_x_bu"] = pd.DataFrame(linhas)
    out["a5_excecoes_sem_contingencia"] = pd.DataFrame(excecoes, columns=["ano", "uf", "cd_municipio", "zona", "secao", "comparecimento", "computado_log", "habilitado_log"])
    # votos depois do horario nominal, por estrato
    m26, m22 = ms[2026], ms[2022]
    if est is not None:
        m26 = m26.merge(est[KEY + ["estrato"]].drop_duplicates(KEY), on=KEY, how="left")
        m22 = m22.merge(est[KEY + ["estrato"]].drop_duplicates(KEY), on=KEY, how="left")
    rows = []
    for ano, m in ((2026, m26), (2022, m22)):
        for e, g in m.groupby(m.get("estrato", pd.Series("?", index=m.index)).fillna("RR_completo")):
            rows.append(dict(ano=ano, estrato=e, secoes=len(g), secoes_com_voto_apos_nominal=int((g.votos_apos_nominal > 0).sum()), votos_apos_nominal=int(g.votos_apos_nominal.sum()),
                             media_por_secao=float(g.votos_apos_nominal.mean()), max_por_secao=int(g.votos_apos_nominal.max()), comparecimento=int(g.QT_COMPARECIMENTO.sum())))
    out["a5_votos_apos_horario_nominal"] = pd.DataFrame(rows)
    # ultimo voto depois do horario nominal + 15 e + 60 minutos (por secao), por estrato
    for ano, m in ((2026, m26), (2022, m22)):
        m["atraso_ultimo_voto_min"] = m.ultimo_voto_s / 60 - (m.ab_nominal_min + 540)
    rr = []
    for ano, m in ((2026, m26), (2022, m22)):
        for e, g in m.groupby(m.get("estrato", pd.Series("?", index=m.index)).fillna("RR_completo")):
            rr.append(dict(ano=ano, estrato=e, secoes=len(g), ultimo_voto_mais_de_15min_apos=int((g.atraso_ultimo_voto_min > 15).sum()), ultimo_voto_mais_de_60min_apos=int((g.atraso_ultimo_voto_min > 60).sum()),
                           ultimo_voto_antes_do_horario_nominal=int((g.atraso_ultimo_voto_min <= 0).sum())))
    out["a5_ultimo_voto_apos_nominal"] = pd.DataFrame(rr)
    # estimativa nacional (2026): L (populacao completa) + RR completo + amostra aleatoria R fora de L por UF, bootstrap
    popn = D[(2026, 2)]; popn = popn[popn.DS_TIPO_URNA.str.upper().eq("APURADA") & (popn.SG_UF != "ZZ")]
    Lset = set(map(tuple, popn[popn.atraso_min >= 115][KEY].values))
    if est is not None:
        Rn = m26[(m26.estrato == "R") & ~m26[KEY].apply(tuple, axis=1).isin(Lset)]
        medido = m26[(m26.estrato == "L")]
        n_L_pop = len(Lset)
        faltam_L = n_L_pop - len(medido[~medido.SG_UF.eq("RR")])
        nonL = popn[~popn[KEY].apply(tuple, axis=1).isin(Lset)]
        n_nonL_uf = nonL.groupby("SG_UF").size()
        rng = np.random.default_rng(11)
        pool_mean = float(Rn.votos_apos_nominal.mean()) if len(Rn) else np.nan
        def estima(R_):
            tot = 0.0
            for uf, n in n_nonL_uf.items():
                g = R_[R_.SG_UF == uf]
                tot += n * (float(g.votos_apos_nominal.mean()) if len(g) >= 5 else float(R_.votos_apos_nominal.mean()))
            return tot
        pt = estima(Rn)
        bs = [estima(Rn.sample(len(Rn), replace=True, random_state=int(rng.integers(1e9)))) for _ in range(300)] if len(Rn) else [np.nan]
        L_tot = float(medido[~medido.SG_UF.eq("RR")].votos_apos_nominal.sum())
        out["a5_estimativa_nacional_votos_apos_nominal"] = pd.DataFrame([dict(
            secoes_L_medidas=int(len(medido)), secoes_L_populacao=n_L_pop, secoes_L_nao_medidas=int(max(faltam_L, 0)), votos_apos_nominal_em_L_medido=L_tot,
            estimativa_fora_de_L=pt, ic95_fora_de_L_inf=float(np.nanquantile(bs, .025)), ic95_fora_de_L_sup=float(np.nanquantile(bs, .975)), estimativa_total=L_tot + pt,
            ic95_total_inf=L_tot + float(np.nanquantile(bs, .025)), ic95_total_sup=L_tot + float(np.nanquantile(bs, .975)), referencia_externa_nao_verificada=34330,
            nota="votos com horario de computacao posterior ao horario nominal de fechamento (17h Brasilia equivalente); inclui votantes com senha na fila (Codigo Eleitoral, art. 153)")])
    L = m26[m26.get("estrato") == "L"]
    if len(L):
        total_L = int(L.votos_apos_nominal.sum())
        out["a5_resumo_L"] = dict(secoes_L_processadas=len(L), secoes_L_populacao=6714, votos_apos_nominal_em_L=total_L, media_por_secao=float(L.votos_apos_nominal.mean()),
                                  nota="L = seccoes que fecharam >= 115 min depois do horario nominal (populacao completa, exceto RR e exterior). Referencia externa nao verificada: 34.330 eleitores (imprensa).")
    # horario do ultimo voto nas secoes L
    if len(L):
        h = (L.ultimo_voto_s / 3600).dropna()
        out["a5_hora_ultimo_voto_L"] = pd.DataFrame({"hora_local_da_urna": pd.cut(h, [0, 15, 16, 17, 18, 19, 20, 24]).astype(str)}).value_counts().rename("secoes").reset_index()
    # liberacao manual total pelo log contra o campo do BWeb
    ht = [c for c in m26.columns if c.startswith("hab_")]
    t = m26.copy()
    t["hab_biometrica"] = t["hab_biométrica"].fillna(0) if "hab_biométrica" in t else 0
    t["manual_total_log"] = t.n_computado - t.hab_biometrica
    t = t[(t.n_computado == t.QT_COMPARECIMENTO) & ~t.cont]
    out["a5_liberacao_manual_total"] = pd.DataFrame([dict(secoes=len(t), manual_total_log=float(t.manual_total_log.sum()), bweb_biom_nh=float(t.biom_nh.sum()), razao=float(t.manual_total_log.sum() / t.biom_nh.sum()),
                                                          tipos_de_habilitacao=";".join(c for c in ht))])
    # associacao entre votos tardios e Lula% (mesmo local; placebo: mesmas secoes em 2022)
    est_rows, res = [], {}
    for ano, m in ((2026, m26), (2022, m22)):
        d = m[m.valid2 >= 30].copy(); d["tard"] = d.votos_apos_nominal / d.QT_COMPARECIMENTO
        b = D[(ano, 1)].set_index(KEY)[["lula_sh"]].rename(columns={"lula_sh": "lula_sh_t1"})
        d = d.join(b, on=KEY)
        d = d[d.lula_sh_t1.notna()]
        r = tenta(out, f"A5 {ano} tardio~Lula%", fe_ols, d, "lula_sh", ["tard", "lula_sh_t1"], "uf_local")
        if r is not None:
            res[ano] = (r, d)
            est_rows.append(dict(ano=ano, coef=float(r.loc["tard", "coef"]), ep=float(r.loc["tard", "se"]), secoes=int(r.n.iloc[0]), locais=int(r.grupos.iloc[0])))
    out["a5_tardio_x_lula"] = pd.DataFrame(est_rows)
    if 2026 in res and 2022 in res:
        r26, d26 = res[2026]; r22, _ = res[2022]
        reg.add("A5", "share de votos depois do horario nominal (log) e Lula% no T2 dado o T1, EF de local", float(r26.loc["tard", "coef"]), float(r26.loc["tard", "se"]),
                [("2022/T2 (mesmas secoes)", float(r22.loc["tard", "coef"]), float(r22.loc["tard", "se"]))], expo=float((d26.tard * d26.valid2).sum()), fator=2.0,
                nota="amostra: seccoes que fecharam tarde + controles no mesmo local + 639 com comparecimento >= 95% + 60 aleatorias por UF; RR completo")
    else:
        raise NaoExecutado("A5: associacao entre votos tardios e Lula% nao estimada")
