"""H9 (consistencia entre produtos do TSE), H10 (impacto agregado) e teste direto com boletins impressos."""
import glob
import os
import zipfile
import numpy as np
import pandas as pd
from lib_auditoria import KEY, MARGEM, NaoExecutado
from h1_h4 import tenta

OPO = {2014: 45, 2018: 17, 2022: 22, 2026: 22}
OFICIAL_2026_T2 = {"lula": 64_256_232, "flavio": 59_826_041}   # numeros divulgados (confirmados na leitura de votacao_secao na fase 1)


def _le_votacao_secao(zdir, ano):
    z = glob.glob(os.path.join(zdir, f"votacao_secao_{ano}_BR.zip"))
    if len(z) != 1:
        raise NaoExecutado(f"falta votacao_secao_{ano}_BR.zip em {zdir}")
    zf = zipfile.ZipFile(z[0]); nome = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
    partes = []
    with zf.open(nome) as f:
        for ch in pd.read_csv(f, sep=";", encoding="latin-1", usecols=KEY + ["NR_TURNO", "CD_CARGO", "NR_VOTAVEL", "QT_VOTOS"], chunksize=1_000_000, low_memory=False):
            ch = ch[(ch.CD_CARGO == 1) & ch.NR_VOTAVEL.isin([13, OPO[ano]])]
            partes.append(ch)
    d = pd.concat(partes)
    d["cand"] = np.where(d.NR_VOTAVEL == 13, "lula", "dir")
    return d.pivot_table(index=KEY + ["NR_TURNO"], columns="cand", values="QT_VOTOS", aggfunc="sum", fill_value=0).reset_index()


def h9(D, reg, out):
    zdir = out.get("zips")
    if not zdir:
        raise NaoExecutado("H9: informe --zips com a pasta dos votacao_secao_*.zip")
    linhas = []
    div_det, so_bweb = [], []
    for ano in sorted(out["anos"]):
        vs = tenta(out, f"H9 votacao_secao {ano}", _le_votacao_secao, zdir, ano)
        if vs is None:
            continue
        for t in (1, 2):
            b = D[(ano, t)]
            b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")]
            v = vs[vs.NR_TURNO == t]
            m = b.merge(v[KEY + ["lula", "dir"]], on=KEY, how="outer", suffixes=("", "_vs"), indicator=True)
            amb = m[m._merge == "both"]
            dif = (amb.lula != amb.lula_vs) | (amb["dir"] != amb.dir_vs)
            d_ = amb[dif]
            for _, r in d_.iterrows():
                div_det.append(dict(ano=ano, turno=t, uf=r.SG_UF, cd_municipio=r.CD_MUNICIPIO, zona=r.NR_ZONA, secao=r.NR_SECAO, aptos_bweb=r.QT_APTOS,
                                    comparecimento_bweb=r.QT_COMPARECIMENTO, nominais_bweb=r.nominal, lula_bweb=r.lula, lula_votacao_secao=r.lula_vs,
                                    oponente_bweb=r["dir"], oponente_votacao_secao=r.dir_vs, soma_candidatos_votacao_secao=r.lula_vs + r.dir_vs))
            for _, r in m[m._merge == "left_only"].iterrows():
                so_bweb.append(dict(ano=ano, turno=t, uf=r.SG_UF, cd_municipio=r.CD_MUNICIPIO, zona=r.NR_ZONA, secao=r.NR_SECAO, aptos=r.QT_APTOS,
                                    comparecimento=r.QT_COMPARECIMENTO, votos_lula=r.lula, votos_oponente=r["dir"]))
            linhas.append(dict(ano=ano, turno=t, secoes_bweb=len(b), secoes_votacao_secao=len(v), so_bweb=int((m._merge == "left_only").sum()),
                               so_votacao_secao=int((m._merge == "right_only").sum()), pareadas=len(amb), pareadas_com_diferenca=int(dif.sum()),
                               soma_abs_dif_votos=int((amb.lula - amb.lula_vs).abs().sum() + (amb["dir"] - amb.dir_vs).abs().sum()),
                               lula_bweb=int(b.lula.sum()), lula_votacao_secao=int(v.lula.sum()), dir_bweb=int(b["dir"].sum()), dir_votacao_secao=int(v["dir"].sum())))
    out["h9_bweb_vs_votacao_secao"] = pd.DataFrame(linhas)
    out["h9_divergencias_secao"] = pd.DataFrame(div_det)
    out["h9_secoes_so_no_bweb"] = pd.DataFrame(so_bweb)
    # consistencia interna de cada BU
    ic = []
    for (a, t), d in sorted(D.items()):
        x = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
        ic.append(dict(ano=a, turno=t, secoes=len(x), comparecimento_maior_que_aptos=int((x.QT_COMPARECIMENTO > x.QT_APTOS).sum()),
                       soma_votos_diferente_de_comparecimento=int((x.nominal + x.branco + x.nulo != x.QT_COMPARECIMENTO).sum()),
                       validos_maior_que_comparecimento=int((x.valid2 > x.QT_COMPARECIMENTO).sum()), mais_de_uma_urna=int((x.n_urnas > 1).sum())))
    out["h9_consistencia_interna"] = pd.DataFrame(ic)
    # totais contra os numeros divulgados e contra a totalizacao por municipio/zona (2026)
    t2 = D[(2026, 2)]
    out["h9_totais_2026_T2"] = pd.DataFrame([dict(fonte="BWeb (soma das secoes apuradas)", lula=int(t2[t2.DS_TIPO_URNA.str.upper().eq("APURADA")].lula.sum()),
                                                  flavio=int(t2[t2.DS_TIPO_URNA.str.upper().eq("APURADA")]["dir"].sum())),
                                             dict(fonte="divulgado (referencia externa)", lula=OFICIAL_2026_T2["lula"], flavio=OFICIAL_2026_T2["flavio"])])
    _munzona(D, out, zdir)


def _munzona(D, out, zdir):
    p = os.path.join(zdir, "votacao_candidato_munzona_2026.zip")
    if not os.path.exists(p):
        raise NaoExecutado(f"falta {p}: sem a totalizacao por municipio/zona a comparacao do H9 nao pode ser feita")
    zf = zipfile.ZipFile(p); nome = [n for n in zf.namelist() if n.upper().endswith("_BR.CSV")][0]
    partes = []
    with zf.open(nome) as f:
        for ch in pd.read_csv(f, sep=";", encoding="latin-1", chunksize=500_000, low_memory=False,
                              usecols=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "CD_CARGO", "NR_CANDIDATO", "QT_VOTOS_NOMINAIS", "QT_VOTOS_NOMINAIS_VALIDOS"]):
            partes.append(ch[(ch.CD_CARGO == 1) & ch.NR_CANDIDATO.isin([13, 22])])
    mz = pd.concat(partes)
    mz["cand"] = np.where(mz.NR_CANDIDATO == 13, "lula", "dir")
    mzw = mz.pivot_table(index=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA"], columns="cand", values="QT_VOTOS_NOMINAIS_VALIDOS", aggfunc="sum", fill_value=0).reset_index()
    linhas = []
    for t in (1, 2):
        b = D[(2026, t)]; b = b[b.DS_TIPO_URNA.str.upper().eq("APURADA")]
        bz = b.groupby(["SG_UF", "CD_MUNICIPIO", "NR_ZONA"])[["lula", "dir"]].sum().reset_index()
        m = bz.merge(mzw[mzw.NR_TURNO == t].drop(columns="NR_TURNO"), on=["SG_UF", "CD_MUNICIPIO", "NR_ZONA"], how="outer", suffixes=("", "_mz"), indicator=True)
        amb = m[m._merge == "both"]
        dif = (amb.lula != amb.lula_mz) | (amb["dir"] != amb.dir_mz)
        linhas.append(dict(turno=t, zonas_bweb=len(bz), zonas_munzona=int((mzw.NR_TURNO == t).sum()), so_bweb=int((m._merge == "left_only").sum()),
                           so_munzona=int((m._merge == "right_only").sum()), pareadas=len(amb), com_diferenca=int(dif.sum()),
                           soma_abs_dif_votos=int((amb.lula - amb.lula_mz).abs().sum() + (amb["dir"] - amb.dir_mz).abs().sum()),
                           lula_bweb=int(bz.lula.sum()), lula_munzona=int(mzw[mzw.NR_TURNO == t].lula.sum()),
                           flavio_bweb=int(bz["dir"].sum()), flavio_munzona=int(mzw[mzw.NR_TURNO == t]["dir"].sum())))
    out["h9_bweb_vs_totalizacao_munzona"] = pd.DataFrame(linhas)


def h10(D, reg, out):
    df = reg.frame()
    if df.empty:
        raise NaoExecutado("H10: registro de testes vazio")
    if "ressalva" not in df:
        df["ressalva"] = ""
    df["ressalva"] = df["ressalva"].fillna("")
    df = df[df.votos_max_margem.notna()]
    surv_all = df[df.veredito.str.startswith(("EXCESSO DETECTADO e relevante", "excesso detectavel"))]
    linhas = []
    for crit, surv in (("como registrado", surv_all), ("excluindo linhas com ressalva de desenho", surv_all[surv_all.ressalva == ""])):
        for sentido in ("PT", "OPO"):
            s = surv[surv.sentido == sentido]; a = df[df.sentido == sentido]
            linhas.append(dict(criterio=crit, sentido=sentido, n_testes_com_votos=len(a), n_sobreviventes=len(s),
                               soma_votos_sobreviventes_exigente=float(s.votos_max_margem.sum()), soma_votos_sobreviventes_pior_caso=float(s.votos_max_pior_caso.sum()),
                               maximo_individual_pior_caso=float(a.votos_max_pior_caso.max()) if len(a) else 0.0, soma_de_todos_exigente=float(a.votos_max_margem.sum())))
    r = pd.DataFrame(linhas)
    r["pct_margem_sobreviventes_pior_caso"] = 100 * r.soma_votos_sobreviventes_pior_caso / MARGEM
    r["pct_margem_soma_todos_exigente"] = 100 * r.soma_de_todos_exigente / MARGEM
    out["h10_agregado"] = r
    out["h10_sobreviventes"] = surv_all[["H", "teste", "sentido", "p_holm", "votos_max_margem", "votos_max_pior_caso", "pct_pior_caso", "veredito", "ressalva"]]
    out["h10_nota"] = ("Tetos nao sao aditivos independentes: os testes usam as mesmas secoes. 'soma_de_todos' e um teto frouxo e redundante; "
                       "'sobreviventes' soma so os testes com excesso detectado apos Holm. Sentidos PT e OPO nao se compensam. "
                       "'Ressalva de desenho' marca linhas cuja metodologia pre-registrada se mostrou inadequada em controle posterior; os dois criterios sao publicados.")


def bu_impresso(D, reg, out):
    pasta = out.get("bu_dir")
    raise NaoExecutado("teste direto com boletins impressos: nenhuma foto/PDF de BU foi fornecido (nem em Downloads, nem no projeto). "
                       "Envie imagens com o QR code visivel ou uma planilha zona;secao;turno;votos para o cruzamento com o BWeb. "
                       "Divergencia de qualquer tamanho sera reportada.")
