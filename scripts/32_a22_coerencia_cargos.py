#!/usr/bin/env python3
"""A22 (Fase 3.1): coerencia entre cargos. Nas UFs com 2o turno de governador cujos finalistas estao alinhados a candidatos presidenciais diferentes,
compara a participacao do candidato do PT para presidente com a do governador alinhado a ele, secao a secao; 2026 contra os placebos 2022 e 2018.
Pre-registro: Adendo 8 (desenho) e Adendo 9 (regra de alinhamento, estatistica, placebos). O alinhamento e decidido so pela composicao das coligacoes, antes de olhar votos.
Uso: python -I 32_a22_coerencia_cargos.py DIR_BWEB_2026_2022 DIR_BWEB_2018 DIR_COLIGACAO DIR_PARQUET DIR_SAIDA
  DIR_COLIGACAO: consulta_coligacao_{2018,2022,2026}.zip (TSE dados abertos)."""
import glob
import os
import re
import sys
import unicodedata
import zipfile
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_auditoria import KEY, Registro, carrega

NOME = re.compile(r"(?i)^bweb_2t_([A-Z]{2})_\d{4}(\d{4})\d{4,6}\.zip$")
COLS = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "CD_TIPO_VOTAVEL", "NR_VOTAVEL", "NR_PARTIDO", "SG_PARTIDO", "NM_VOTAVEL", "QT_VOTOS", "DS_TIPO_URNA"]
SEMENTE = 20261029


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9]", "", s)


def partidos(texto):
    """Conjunto de siglas normalizadas de uma composicao ('PSB / FEDERACAO X (13-PT / 65-PC do B) / ...'); federacoes expandidas; '#NULO' vazio."""
    if not isinstance(texto, str) or texto.strip() in ("", "#NULO", "#NE"):
        return set()
    t = re.sub(r"(?i)federa[cç][aã]o[^(/]*\(", "(", texto)
    t = t.replace("(", "/").replace(")", "/")
    out = set()
    for p in t.split("/"):
        p = re.sub(r"^\s*\d+\s*-\s*", "", p.strip())
        if p:
            out.add(norm(p))
    return out


def le_coligacao(cdir, ano):
    z = zipfile.ZipFile(os.path.join(cdir, f"consulta_coligacao_{ano}.zip"))
    with z.open(f"consulta_coligacao_{ano}_BRASIL.csv") as f:
        d = pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, usecols=["SG_UF", "CD_CARGO", "NR_TURNO", "NR_PARTIDO", "SG_PARTIDO", "DS_COMPOSICAO_FEDERACAO", "SQ_COLIGACAO", "DS_COMPOSICAO_COLIGACAO"])
    return d[d.NR_TURNO == "1"]


def composicao(col, uf, cargo, nr_partido):
    """Partidos da coligacao (ou do partido isolado, com a federacao) do candidato de numero de partido nr_partido. None se nao ha linha."""
    r = col[(col.SG_UF == uf) & (col.CD_CARGO == str(cargo)) & (col.NR_PARTIDO == str(nr_partido))]
    if r.empty:
        return None
    r = r.iloc[0]
    q = partidos(r.DS_COMPOSICAO_COLIGACAO)
    q |= partidos(r.DS_COMPOSICAO_FEDERACAO)
    q.add(norm(r.SG_PARTIDO))
    return q


def extrai(dirs, ano, ufs, saida):
    p = os.path.join(saida, f"bweb_pres_gov_t2_{ano}.parquet")
    if os.path.exists(p):
        return pd.read_parquet(p)
    zips = []
    for d in dirs:
        for z in glob.glob(os.path.join(d, "*.zip")):
            m = NOME.match(os.path.basename(z))
            if m and int(m.group(2)) == ano and m.group(1).upper() in ufs:
                zips.append(z)
    if len(zips) != len(ufs):
        raise SystemExit(f"ERRO {ano}: esperava zips de {sorted(ufs)}, achei {len(zips)}")
    partes = []
    for z in zips:
        with zipfile.ZipFile(z) as zz:
            nome = [n for n in zz.namelist() if n.lower().endswith(".csv")][0]
            with zz.open(nome) as f:
                hdr = [c.replace(" ", "") for c in pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns]
            falt = [c for c in COLS if c not in hdr]
            if falt:
                raise SystemExit(f"ERRO {z}: colunas ausentes {falt}")
            with zz.open(nome) as f:
                for ch in pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, chunksize=500_000, header=0, names=hdr, usecols=COLS):
                    ch = ch[ch.CD_CARGO_PERGUNTA.isin(["1", "3"]) & (ch.CD_TIPO_VOTAVEL == "1") & ch.DS_TIPO_URNA.str.upper().eq("APURADA")]
                    ch = ch.assign(v=pd.to_numeric(ch.QT_VOTOS, errors="coerce").fillna(0))
                    partes.append(ch.groupby(KEY + ["CD_CARGO_PERGUNTA", "NR_VOTAVEL", "NR_PARTIDO", "SG_PARTIDO", "NM_VOTAVEL"], as_index=False).v.sum())
    d = pd.concat(partes, ignore_index=True)
    for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"):
        d[c] = pd.to_numeric(d[c])
    d = d.groupby(KEY + ["CD_CARGO_PERGUNTA", "NR_VOTAVEL", "NR_PARTIDO", "SG_PARTIDO", "NM_VOTAVEL"], as_index=False).v.sum()
    d.to_parquet(p, index=False)
    return d


def alinhamento(d, col, ano, regra="registrada"):
    """Classifica cada UF com 2o turno de governador. Nenhum voto e usado alem de identificar os dois finalistas.
    regra 'registrada' (Adendo 9): alinhamento > 0,5 a um lado e < 0,5 ao outro. Regra '9b' (Adendo 9b): o partido do candidato presidencial esta na composicao do finalista e o do outro nao."""
    pres = d[d.CD_CARGO_PERGUNTA == "1"].groupby(["NR_PARTIDO", "SG_PARTIDO", "NM_VOTAVEL"], as_index=False).v.sum().sort_values("v", ascending=False)
    pt = pres[pres.NR_PARTIDO == "13"]
    if len(pres) != 2 or len(pt) != 1:
        raise SystemExit(f"ERRO {ano}: esperava 2 candidatos a presidente no 2o turno incluindo o PT (13): {pres.to_dict('records')}")
    nA, nB = "13", pres[pres.NR_PARTIDO != "13"].NR_PARTIDO.iloc[0]
    sigA, sigB = norm("PT"), norm(pres[pres.NR_PARTIDO != "13"].SG_PARTIDO.iloc[0])
    PA, PB = composicao(col, "BR", 1, nA), composicao(col, "BR", 1, nB)
    linhas = []
    for uf, g in d[d.CD_CARGO_PERGUNTA == "3"].groupby("SG_UF"):
        fin = g.groupby(["NR_PARTIDO", "SG_PARTIDO", "NM_VOTAVEL"], as_index=False).v.sum().sort_values("v", ascending=False)
        if len(fin) != 2:
            linhas.append(dict(ano=ano, SG_UF=uf, elegivel=False, regra=regra, motivo=f"{len(fin)} candidatos a governador no 2o turno")); continue
        r = dict(ano=ano, SG_UF=uf, elegivel=False)
        lado = []
        for i, c in enumerate(fin.itertuples(), 1):
            Q = composicao(col, uf, 3, c.NR_PARTIDO)
            if Q is None:
                lado.append(None); r.update({f"cand{i}": f"{c.NM_VOTAVEL} ({c.SG_PARTIDO})", f"Q{i}": "SEM LINHA NA TABELA DE COLIGACOES"}); continue
            aA, aB = len(Q & PA) / len(Q), len(Q & PB) / len(Q)
            if regra == "9b":
                s = "A" if (sigA in Q and sigB not in Q) else ("B" if (sigB in Q and sigA not in Q) else "-")
            else:
                s = "A" if (aA > .5 and aB < .5) else ("B" if (aB > .5 and aA < .5) else "-")
            lado.append(s); r.update({f"cand{i}": f"{c.NM_VOTAVEL} ({c.SG_PARTIDO})", f"Q{i}": " / ".join(sorted(Q)), f"alinh_PT{i}": round(aA, 3), f"alinh_oponente{i}": round(aB, 3), f"lado{i}": s,
                                      f"NR_PARTIDO{i}": c.NR_PARTIDO})
        r["elegivel"] = sorted([x for x in lado if x]) == ["A", "B"] and None not in lado
        r["motivo"] = "" if r["elegivel"] else "finalistas nao estao alinhados a candidatos presidenciais diferentes (ou sem linha)"
        r["regra"] = regra
        linhas.append(r)
    return pd.DataFrame(linhas), PA, PB


def secoes(d, al, T1):
    """Uma linha por secao nas UFs elegiveis: participacao do candidato do PT para presidente e do governador alinhado a ele (2o turno)."""
    out = []
    for r in al[al.elegivel].itertuples():
        nr = r.NR_PARTIDO1 if r.lado1 == "A" else r.NR_PARTIDO2
        no = r.NR_PARTIDO2 if r.lado1 == "A" else r.NR_PARTIDO1
        g = d[(d.SG_UF == r.SG_UF)]
        pa = g[(g.CD_CARGO_PERGUNTA == "1") & (g.NR_VOTAVEL == "13")].set_index(KEY).v.rename("pres_A")
        pb = g[(g.CD_CARGO_PERGUNTA == "1") & (g.NR_VOTAVEL != "13")].groupby(KEY).v.sum().rename("pres_B")
        ga = g[(g.CD_CARGO_PERGUNTA == "3") & (g.NR_PARTIDO == nr)].groupby(KEY).v.sum().rename("gov_A")
        gb = g[(g.CD_CARGO_PERGUNTA == "3") & (g.NR_PARTIDO == no)].groupby(KEY).v.sum().rename("gov_B")
        s = pd.concat([pa, pb, ga, gb], axis=1).dropna().reset_index()
        out.append(s)
    if not out:
        return None
    s = pd.concat(out, ignore_index=True)
    s["pres_valid"] = s.pres_A + s.pres_B; s["gov_valid"] = s.gov_A + s.gov_B
    s = s[(s.pres_valid >= 30) & (s.gov_valid >= 30)].copy()
    s["pres_sh"] = s.pres_A / s.pres_valid; s["gov_sh"] = s.gov_A / s.gov_valid; s["d"] = s.pres_sh - s.gov_sh
    s = s.merge(T1[KEY + ["lula_sh"]].rename(columns={"lula_sh": "pres_sh_t1"}), on=KEY, how="left")
    return s


def estat(s):
    """Media ponderada por votos validos presidenciais e erro padrao agrupado por municipio."""
    w, d = s.pres_valid.values, s.d.values
    W = w.sum(); S = float((w * d).sum() / W)
    cl = s.SG_UF.astype(str) + "|" + s.CD_MUNICIPIO.astype(str)
    sc = pd.Series(w * (d - S)).groupby(cl.values).sum().values
    G = len(sc)
    se = float(np.sqrt(G / (G - 1) * (sc ** 2).sum()) / W)
    return S, se, G


def ajustado(s, B=200):
    """Secundaria (fora da familia): d regredido em pres_sh_t1 - 0,5 dentro de cada UF; S_aj = media ponderada dos interceptos."""
    x = s.dropna(subset=["pres_sh_t1"]).copy()
    def calc(df):
        tot, acc = 0.0, 0.0
        for uf, g in df.groupby("SG_UF"):
            w = g.pres_valid.values; X = np.column_stack([np.ones(len(g)), g.pres_sh_t1.values - .5]); y = g.d.values
            b = np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0]
            acc += w.sum() * b[0]; tot += w.sum()
        return acc / tot
    est = calc(x)
    rng = np.random.default_rng(SEMENTE)
    muns = x.groupby(["SG_UF", "CD_MUNICIPIO"]).ngroup().values
    idxs = pd.Series(np.arange(len(x))).groupby(muns).apply(np.array).values
    ests = []
    for _ in range(B):
        pick = rng.integers(0, len(idxs), len(idxs))
        ests.append(calc(x.iloc[np.concatenate([idxs[i] for i in pick])]))
    return est, float(np.std(ests, ddof=1))


def roda_regra(regra, ufs_gov, dirs, cdir, D, cache, saida):
    res, tab_al, tab_s = {}, [], []
    for ano in (2026, 2022, 2018):
        d = extrai(dirs, ano, ufs_gov[ano], cache)
        col = le_coligacao(cdir, ano)
        al, PA, PB = alinhamento(d, col, ano, regra)
        tab_al.append(al)
        s = secoes(d, al, D[(ano, 1)])
        if s is None:
            res[ano] = dict(n=0, ufs=[]); print(regra, ano, "nenhuma UF elegivel", flush=True); continue
        s["ano"] = ano
        S, se, G = estat(s)
        Sa, sea = ajustado(s)
        tab_s.append(s.groupby("SG_UF").apply(lambda g: pd.Series(dict(secoes=len(g), votos_validos_pres=int(g.pres_valid.sum()), S=float((g.pres_valid * g.d).sum() / g.pres_valid.sum())))).reset_index().assign(ano=ano))
        res[ano] = dict(S=S, se=se, G=G, Sa=Sa, sea=sea, expo=float(s.pres_valid.sum()), n=len(s), ufs=sorted(s.SG_UF.unique()))
        print(regra, ano, "UFs elegiveis:", res[ano]["ufs"], "secoes", len(s), "S", round(S, 4), "ep", round(se, 4), "S_aj", round(Sa, 4), "ep", round(sea, 4), flush=True)
    suf = "" if regra == "registrada" else "_9b"
    pd.concat(tab_al).to_csv(os.path.join(saida, f"A22_alinhamento{suf}.csv"), index=False)
    if tab_s:
        pd.concat(tab_s).to_csv(os.path.join(saida, f"A22_deslocamento_por_UF{suf}.csv"), index=False)
    R = pd.DataFrame([dict(regra=regra, ano=a, UFs_elegiveis=",".join(v["ufs"]), secoes=v["n"], votos_validos_pres=int(v.get("expo", 0)), S=v.get("S"), ep=v.get("se"), municipios=v.get("G"),
                           S_ajustado_T1=v.get("Sa"), ep_ajustado=v.get("sea")) for a, v in res.items()])
    R.to_csv(os.path.join(saida, f"A22_resumo{suf}.csv"), index=False)
    fr = None
    if res[2026]["n"] > 0 and any(res[a]["n"] > 0 for a in (2022, 2018)):
        reg = Registro()
        pl = [(f"{a}/T2", res[a]["S"], res[a]["se"]) for a in (2022, 2018) if res[a]["n"] > 0]
        nota = f"vale so para as UFs elegiveis de 2026 ({','.join(res[2026]['ufs'])}); cada ano usa as suas UFs ({', '.join(a_ + ': ' + ','.join(res[int(a_)]['ufs']) for a_ in ('2022', '2018'))}); {'EXPLORATORIO (Adendo 9b), nao substitui a linha oficial NAO EXECUTAVEL' if regra == '9b' else ''}"
        reg.add("A22" + suf, "participacao do candidato do PT para presidente menos a do governador alinhado, 2o turno", res[2026]["S"], res[2026]["se"], pl, expo=res[2026]["expo"], fator=2.0, sentido="PT", nota=nota)
        reg.add("A22" + suf, "participacao do oponente para presidente menos a do governador alinhado a ele (lado simetrico), 2o turno", -res[2026]["S"], res[2026]["se"], [(n, -b, s_) for n, b, s_ in pl], expo=res[2026]["expo"], fator=2.0, sentido="OPO",
                nota="simetrico por construcao (dois candidatos)")
        fr = reg.frame(); fr.to_csv(os.path.join(saida, f"A22_testes{suf}.csv"), index=False)
    pd.set_option("display.width", 250)
    print(R.round(4).to_string()); print(pd.concat(tab_al)[["ano", "SG_UF", "cand1", "lado1", "cand2", "lado2", "elegivel"]].to_string())
    if fr is not None:
        print(fr[["H", "teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].to_string())
    return res, fr


def main(d1, d2, cdir, pq, saida):
    os.makedirs(saida, exist_ok=True)
    D = carrega(pq, (2018, 2022, 2026))
    cache = os.path.join(saida, "_cache"); os.makedirs(cache, exist_ok=True)
    ufs_gov = {}
    for ano in (2018, 2022, 2026):
        c = pd.read_parquet(os.path.join(os.environ.get("PARQUET2", pq + "2"), f"cargos_{ano}_t2.parquet"), columns=["SG_UF", "CD_CARGO_PERGUNTA"])
        ufs_gov[ano] = set(c[c.CD_CARGO_PERGUNTA.astype(str) == "3"].SG_UF.unique())
    for regra in ("registrada", "9b"):
        roda_regra(regra, ufs_gov, [d1, d2], cdir, D, cache, saida)


if __name__ == "__main__":
    main(*sys.argv[1:6])
