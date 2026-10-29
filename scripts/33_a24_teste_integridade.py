#!/usr/bin/env python3
"""A24 (Fase 3.1): experimento natural do teste de integridade. Compara as secoes cujas urnas foram sorteadas (votaram com urna reserva) com as demais secoes do mesmo local de votacao.
Insumo: data/a24_secoes_teste_integridade.csv, preenchido SO com listas escritas nas publicacoes dos TREs (fonte e data por linha). Pre-registro: Adendo 9.
Regra: menos de 10 secoes lidas => NAO EXECUTADO (poder insuficiente). Nenhuma lista de noticia sem a tabela entra.
Uso: python -I 33_a24_teste_integridade.py LISTA.csv DIR_PARQUET DIR_FASE3 DIR_SAIDA"""
import os
import re
import sys
import unicodedata
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_auditoria import KEY, Registro, carrega, base, MARGEM

MINIMO = 10


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z0-9]", "", s)


def fe_pequeno(df, y, xs, group):
    """Como lib_auditoria.fe_ols, com limiares menores (poucos locais), erro padrao agrupado por local."""
    d = df[[y] + xs + [group]].replace([np.inf, -np.inf], np.nan).dropna()
    d = d[d.groupby(group)[y].transform("size") > 1]
    if len(d) < 30 or d[group].nunique() < 5:
        raise ValueError(f"amostra insuficiente: n={len(d)}, locais={d[group].nunique()}")
    g = d.groupby(group)
    Y = (d[y] - g[y].transform("mean")).values
    X = np.column_stack([(d[x] - g[x].transform("mean")).values for x in xs])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    e = Y - X @ b
    cl = d[group].values; order = np.argsort(cl, kind="stable"); cs = cl[order]
    starts = np.r_[0, np.flatnonzero(cs[1:] != cs[:-1]) + 1]
    sc = np.add.reduceat(X[order] * e[order, None], starts, axis=0)
    G, N, K = len(starts), len(d), X.shape[1]
    bread = np.linalg.inv(X.T @ X)
    V = bread @ (sc.T @ sc) @ bread * (G / (G - 1)) * ((N - 1) / (N - K))
    se = np.sqrt(np.diag(V))
    return b, se, N, G


def le_lista(path, mapa):
    L = pd.read_csv(path, dtype=str, keep_default_na=False)
    if L.empty:
        return L
    falt = [c for c in ("SG_UF", "municipio", "zona", "secao", "turno", "fonte_url", "data_acesso") if c not in L]
    if falt:
        raise SystemExit(f"ERRO: colunas ausentes {falt}")
    if (L.fonte_url == "").any():
        raise SystemExit("ERRO: toda linha precisa de fonte_url (regra do Adendo 9)")
    L["chave"] = L.SG_UF + "|" + L.municipio.map(norm)
    L = L.merge(mapa[["chave", "CD_MUNICIPIO"]], on="chave", how="left")
    if L.CD_MUNICIPIO.isna().any():
        raise SystemExit(f"ERRO: municipio sem codigo: {L[L.CD_MUNICIPIO.isna()][['SG_UF', 'municipio']].drop_duplicates().to_dict('records')}")
    L["NR_ZONA"] = L.zona.astype(int); L["NR_SECAO"] = L.secao.astype(int); L["CD_MUNICIPIO"] = L.CD_MUNICIPIO.astype(int); L["turno"] = L.turno.astype(int)
    return L


def roda(lista, pq, f3, saida):
    os.makedirs(saida, exist_ok=True)
    mapa = pd.read_csv(os.path.join(f3, "A20_mapa_tse_ibge.csv"), dtype=str)
    mapa["chave"] = mapa.SG_UF + "|" + mapa.NM_MUNICIPIO.map(norm); mapa["CD_MUNICIPIO"] = mapa.CD_MUNICIPIO.astype(int)
    L = le_lista(lista, mapa)
    n = 0 if L.empty else L[L.turno == 2].drop_duplicates(KEY).shape[0]
    por_uf = [] if L.empty else L.groupby("SG_UF").size().rename("secoes").reset_index().to_dict("records")
    if n < MINIMO:
        r = pd.DataFrame([dict(teste="A24", estado="NAO EXECUTADO", secoes_lidas_turno2=n, motivo=f"menos de {MINIMO} secoes lidas das publicacoes dos TREs; os sites dos TREs respondem 403 a acesso automatizado e as buscas devolvem so resumos sem a tabela",
                               como_fornecer="preencher data/a24_secoes_teste_integridade.csv (uma linha por secao, com a URL da publicacao do TRE e a data de acesso) e rodar scripts/33_a24_teste_integridade.py")])
        r.to_csv(os.path.join(saida, "A24_resumo.csv"), index=False)
        print(r.T.to_string()); return r
    D = carrega(pq, (2022, 2026))
    marca = L[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]].drop_duplicates().assign(listada=1)
    reg = Registro()
    w26 = par_ano_local(D, 2026)
    w22 = par_ano_local(D, 2022)
    bal = []
    for y, nome, sent, fator, expo_col in (("lula_sh", "participacao de Lula (votos validos)", "PT", 2.0, "valid2"), ("turnout", "comparecimento", "PT+OPO", 1.0, "QT_APTOS"), ("manual_rate", "liberacao manual", "PT+OPO", 1.0, None)):
        def so_locais_com_listada(w):
            w = w.merge(marca, on=KEY, how="left"); w["listada"] = w.listada.fillna(0)
            loc = w.groupby("uf_local").listada.agg(["sum", "size"]); ok = loc[(loc["sum"] >= 1) & (loc["size"] > loc["sum"])].index
            return w[w.uf_local.isin(ok)]
        xs = ["listada", y + "_t1"]
        try:
            b, se, N, G = fe_pequeno(so_locais_com_listada(w26), y, xs, "uf_local")
            bp, sep, *_ = fe_pequeno(so_locais_com_listada(w22), y, xs, "uf_local")
        except ValueError as e:
            print("falha", y, e); continue
        # balanco pre-tratamento (nao entra no veredito): a mesma diferenca no 1o turno de 2026, sem controle
        try:
            b1, se1, *_ = fe_pequeno(so_locais_com_listada(base(D[(2026, 1)])), y, ["listada"], "uf_local"); bal.append(dict(desfecho=y, diferenca_1o_turno_2026=float(b1[0]), ep=float(se1[0])))
        except ValueError:
            pass
        expo = float(base(D[(2026, 2)])[expo_col].sum()) if expo_col else np.nan
        reg.add("A24", f"{nome}: secoes de urna sorteada contra demais secoes do mesmo local (EF de local, controle do 1o turno)", float(b[0]), float(se[0]), [("2022/T2 (controle do T1)", float(bp[0]), float(sep[0]))], expo=expo, fator=fator, sentido=sent,
                nota=f"{G} locais, {N} secoes; teto = extrapolacao do coeficiente para todo o pais, sem amostragem aleatoria, so como limite superior; menor efeito detectavel ~ {2.8 * se[0]:.4f}")
    pd.DataFrame(bal).to_csv(os.path.join(saida, "A24_balanco_1o_turno_2026.csv"), index=False)
    fr = reg.frame(); fr.to_csv(os.path.join(saida, "A24_testes.csv"), index=False)
    pd.DataFrame([dict(teste="A24", estado="EXECUTADO", secoes_lidas_turno2=n, ufs=",".join(x["SG_UF"] for x in por_uf))]).to_csv(os.path.join(saida, "A24_resumo.csv"), index=False)
    print(fr[["teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]].to_string())
    return fr


def par_ano_local(D, ano):
    """T2 com o desfecho do T1 (lula_sh, turnout, manual_rate) e uf_local."""
    t1 = D[(ano, 1)].set_index(KEY)[["lula_sh", "turnout", "manual_rate"]].add_suffix("_t1")
    w = base(D[(ano, 2)]).set_index(KEY).join(t1, how="inner").reset_index()
    return w


if __name__ == "__main__":
    roda(*sys.argv[1:5])
