#!/usr/bin/env python3
"""
Etapa 1: le os zips BWeb (boletim de urna) de 2014, 2018, 2022 e 2026 (T1 e T2), filtra Presidente e grava
um parquet por (ano, turno) no nivel de secao.

Uso: python -I 01_prepara_bweb.py DIR_ZIPS DIR_SAIDA --anos 2022 2026 [--procs 6]

Convencao de colunas (nomes herdados da primeira fase da analise):
  lula = candidato nº 13 (PT: Dilma 2014, Haddad 2018, Lula 2022 e 2026)
  dir  = oponente do 2º turno (45 Aecio 2014, 17 Bolsonaro 2018, 22 Bolsonaro 2022, 22 Flavio 2026)

Regras:
  * falta de coluna obrigatoria (para aquele ano) => ERRO (nunca pula em silencio)
  * 2014: arquivo .txt sem cabecalho, 31 campos posicionais (layout do LEIAME_BUWEB): nao tem abertura,
    encerramento nem biometria; essas colunas ficam NaN e quem precisa delas deve falhar com erro.
  * 2018: sem DT_BU_RECEBIDO e DT_EMISSAO_BU; cabecalho tem "SG_ UF" (com espaco).
  * horarios DT_ABERTURA/DT_ENCERRAMENTO/DT_EMISSAO_BU sao horario LOCAL DA URNA (ex.: AC abre 06:00, fecha 15:00).
    O atraso de fechamento e medido contra o horario nominal do municipio (moda de DT_ABERTURA + 9h).
  * DT_BU_RECEBIDO e horario do servidor do TSE (Brasilia).
"""
import argparse, glob, os, re, sys, zipfile
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd

OPONENTE = {2014: 45, 2018: 17, 2022: 22, 2026: 22}
SIN = {
    "biom_nh": ["QT_ELEI_BIOM_SEM_HABILITACAO", "QT_ELEITORES_BIOMETRIA_NH"],
    "agregadas": ["DS_SECOES_AGREGADAS", "DS_AGREGADAS"],
}
OBRIG_BASE = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "CD_CARGO_PERGUNTA",
              "QT_APTOS", "QT_COMPARECIMENTO", "DS_TIPO_URNA", "CD_TIPO_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS",
              "NR_URNA_EFETIVADA"]
OBRIG_HORARIOS = ["DT_ABERTURA", "DT_ENCERRAMENTO"]               # 2018, 2022, 2026
OBRIG_BU_TSE = ["DT_BU_RECEBIDO", "DT_EMISSAO_BU"]                 # 2022, 2026
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
DATAS = ["DT_ABERTURA", "DT_ENCERRAMENTO", "DT_EMISSAO_BU", "DT_BU_RECEBIDO"]

# layout posicional 2014 (31 campos) conforme LEIAME_BUWEB_1T/2T
COLS_2014 = ["DT_GERACAO", "HH_GERACAO", "CD_PLEITO", "CD_ELEICAO", "SG_UF", "CD_CARGO_PERGUNTA", "DS_CARGO",
             "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "NR_PARTIDO", "SG_PARTIDO", "CD_MUNICIPIO", "NM_MUNICIPIO",
             "DT_BU_RECEBIDO", "QT_APTOS", "QT_ABSTENCOES", "QT_COMPARECIMENTO", "CD_TIPO_ELEICAO", "CD_TIPO_URNA",
             "DS_TIPO_URNA", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS", "CD_TIPO_VOTAVEL", "NR_URNA_EFETIVADA",
             "CD_CARGA_1", "CD_CARGA_2", "DT_CARGA", "CD_FLASHCARD", "DS_CARGO_PERGUNTA_SECAO"]
NUM = ["NR_TURNO", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "QT_APTOS", "QT_COMPARECIMENTO",
       "CD_TIPO_VOTAVEL", "NR_VOTAVEL", "QT_VOTOS"]
NOME_ZIP = re.compile(r"(?i)^bweb_(\d)t_([A-Z]{2})_\d{4}(\d{4})\d{4,6}\.zip$")


def info_zip(path):
    m = NOME_ZIP.match(os.path.basename(path))
    if not m:
        raise SystemExit(f"ERRO: nome de zip fora do padrao: {path}")
    return int(m.group(3)), int(m.group(1)), m.group(2).upper()  # ano, turno, uf


def resolve_cols(hdr, ano, path):
    obrig = OBRIG_BASE + (OBRIG_HORARIOS if ano >= 2018 else []) + (OBRIG_BU_TSE if ano >= 2022 else [])
    faltam = [c for c in obrig if c not in hdr and c != "NR_TURNO"]
    if "NR_TURNO" not in hdr:
        faltam.append("NR_TURNO")
    if faltam:
        raise SystemExit(f"ERRO {path}: colunas obrigatorias ausentes para {ano}: {faltam}. Colunas: {list(hdr)}")
    usecols, ren = list(obrig), {}
    for canon, syns in SIN.items():
        achou = [s for s in syns if s in hdr]
        if achou:
            usecols.append(achou[0]); ren[achou[0]] = canon
        elif ano >= 2018:
            raise SystemExit(f"ERRO {path}: nenhuma das colunas {syns} existe (obrigatoria em {ano}).")
    return usecols, ren


def le_zip(zpath, ano, turno):
    partes = []
    with zipfile.ZipFile(zpath) as z:
        nomes = [n for n in z.namelist() if n.lower().endswith((".csv", ".txt"))]
        if len(nomes) != 1:
            raise SystemExit(f"ERRO {zpath}: esperava 1 csv/txt, achei {nomes}")
        if ano == 2014:
            with z.open(nomes[0]) as f:
                for ch in pd.read_csv(f, sep=";", encoding="latin-1", header=None, dtype=str, chunksize=400_000):
                    if ch.shape[1] != len(COLS_2014):
                        raise SystemExit(f"ERRO {zpath}: 2014 deveria ter {len(COLS_2014)} campos, tem {ch.shape[1]}")
                    ch.columns = COLS_2014
                    ch["NR_TURNO"] = str(turno)
                    ch = ch[ch["CD_CARGO_PERGUNTA"] == "1"]
                    if len(ch):
                        partes.append(ch)
        else:
            with z.open(nomes[0]) as f:
                hdr = [c.replace(" ", "") for c in pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns]
            usecols, ren = resolve_cols(hdr, ano, zpath)
            with z.open(nomes[0]) as f:
                for ch in pd.read_csv(f, sep=";", encoding="latin-1", dtype=str, chunksize=400_000, header=0,
                                      names=hdr, usecols=usecols):
                    ch = ch[ch["CD_CARGO_PERGUNTA"] == "1"].rename(columns=ren)
                    if len(ch):
                        partes.append(ch)
    if not partes:
        raise SystemExit(f"ERRO {zpath}: nenhuma linha de Presidente")
    return pd.concat(partes, ignore_index=True)


def processa(zpath):
    ano, turno, uf = info_zip(zpath)
    d = le_zip(zpath, ano, turno)
    if "biom_nh" not in d:
        d["biom_nh"] = np.nan
    if "agregadas" not in d:
        d["agregadas"] = None
    # secoes "Nao instalada"/"Nao apurada" (2014/2018) trazem '#NULO#' ou vazio em CD_TIPO_VOTAVEL/NR_VOTAVEL, com votos=0
    # e comparecimento=0. So esse caso exato vira placeholder -1; qualquer outro valor nao numerico continua dando erro.
    ph = ~d["NR_VOTAVEL"].str.fullmatch(r"\d+", na=False) | ~d["CD_TIPO_VOTAVEL"].str.fullmatch(r"\d+", na=False)
    if ph.any():
        ok = ph & (pd.to_numeric(d["QT_VOTOS"], errors="coerce") == 0) & (pd.to_numeric(d["QT_COMPARECIMENTO"], errors="coerce") == 0)
        if (ph & ~ok).any():
            raise SystemExit(f"ERRO {zpath}: votavel nao numerico fora do caso 'secao sem comparecimento': {int((ph & ~ok).sum())} linhas")
        d.loc[ph, ["NR_VOTAVEL", "CD_TIPO_VOTAVEL"]] = "-1"
    d["_ph"] = ph
    # secoes anuladas/nao apuradas trazem '#NULO#' na biometria: ausente (NaN) so se a urna nao for "Apurada"; senao, erro
    if "biom_nh" in d and ano >= 2018:
        nb = ~d["biom_nh"].str.fullmatch(r"\d+", na=False)
        if nb.any():
            if (nb & d["DS_TIPO_URNA"].str.upper().eq("APURADA")).any():
                raise SystemExit(f"ERRO {zpath}: biometria nao numerica em secao APURADA")
            d.loc[nb, "biom_nh"] = np.nan
    for c in NUM + (["biom_nh"] if ano >= 2018 else []):
        conv = pd.to_numeric(d[c], errors="coerce")
        ruim = conv.isna() & d[c].notna()
        if c == "biom_nh":
            d[c] = conv
            continue
        if ruim.any() or (conv.isna() & d[c].isna()).any():
            n = int((conv.isna()).sum())
            raise SystemExit(f"ERRO {zpath}: coluna {c} com {n} valores nao numericos, ex.: {list(d.loc[conv.isna(), c].astype(str).unique()[:5])}")
        d[c] = conv
    d["ano"] = ano
    opo = OPONENTE[ano]
    d["lula"] = np.where((d.CD_TIPO_VOTAVEL == 1) & (d.NR_VOTAVEL == 13), d.QT_VOTOS, 0)
    d["dir"] = np.where((d.CD_TIPO_VOTAVEL == 1) & (d.NR_VOTAVEL == opo), d.QT_VOTOS, 0)
    d["nominal"] = np.where(d.CD_TIPO_VOTAVEL == 1, d.QT_VOTOS, 0)
    d["branco"] = np.where(d.CD_TIPO_VOTAVEL == 2, d.QT_VOTOS, 0)
    d["nulo"] = np.where(d.CD_TIPO_VOTAVEL == 3, d.QT_VOTOS, 0)
    for c in DATAS:
        if c not in d:
            d[c] = None
    k = ["ano", "NR_TURNO"] + KEY
    soma = d.groupby(k, sort=False)[["lula", "dir", "nominal", "branco", "nulo"]].sum()
    attr = d.groupby(k, sort=False).agg(
        NR_LOCAL_VOTACAO=("NR_LOCAL_VOTACAO", "first"), QT_APTOS=("QT_APTOS", "first"),
        QT_COMPARECIMENTO=("QT_COMPARECIMENTO", "first"), biom_nh=("biom_nh", "first"),
        DS_TIPO_URNA=("DS_TIPO_URNA", "first"), NR_URNA=("NR_URNA_EFETIVADA", "first"),
        agregadas=("agregadas", "first"), n_urnas=("NR_URNA_EFETIVADA", "nunique"),
        DT_ABERTURA=("DT_ABERTURA", "first"), DT_ENCERRAMENTO=("DT_ENCERRAMENTO", "first"),
        DT_EMISSAO_BU=("DT_EMISSAO_BU", "first"), DT_BU_RECEBIDO=("DT_BU_RECEBIDO", "first"))
    return soma.join(attr).reset_index()


def parse_datas(df):
    """Converte as datas ano a ano. Coluna inexistente no ano (2014: tudo; 2018: DT_BU_RECEBIDO/DT_EMISSAO_BU) => NaT explicito.
    Coluna que existe no ano mas tem > 2% de datas invalidas (ignorando secoes nao apuradas) => ERRO."""
    obrigatorias = {"DT_ABERTURA": 2018, "DT_ENCERRAMENTO": 2018, "DT_EMISSAO_BU": 2022, "DT_BU_RECEBIDO": 2022}
    apurada = df["DS_TIPO_URNA"].str.upper().eq("APURADA")
    for c in DATAS:
        s = df[c]
        iso = pd.to_datetime(s, format="%Y-%m-%d %H:%M:%S", errors="coerce")
        br = pd.to_datetime(s, format="%d/%m/%Y %H:%M:%S", errors="coerce")
        so_data = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")   # 2014: DT_BU_RECEBIDO sem hora
        df[c] = iso.fillna(br).fillna(so_data)
        for ano, g in df.groupby("ano"):
            if ano < obrigatorias[c]:
                continue
            ap = g[apurada.loc[g.index]]
            n_nat = int(ap[c].isna().sum())
            print(f"  {c} {ano}: {n_nat} sem data valida de {len(ap)} secoes apuradas ({100*n_nat/max(len(ap),1):.3f}%)", flush=True)
            if n_nat / max(len(ap), 1) > 0.02:
                raise SystemExit(f"ERRO: mais de 2% de datas invalidas em {c} ({ano})")
    return df


def finaliza(df):
    df = parse_datas(df)
    tod = df.DT_ABERTURA.dt.hour * 60 + df.DT_ABERTURA.dt.minute + df.DT_ABERTURA.dt.second / 60
    df["_ab_min"] = tod.round(0)
    if df["_ab_min"].notna().any():
        moda = (df.dropna(subset=["_ab_min"]).groupby(["ano", "NR_TURNO", "SG_UF", "CD_MUNICIPIO"])["_ab_min"]
                .agg(lambda s: s.mode().iloc[0]).rename("ab_nominal_min"))
        df = df.join(moda, on=["ano", "NR_TURNO", "SG_UF", "CD_MUNICIPIO"])
    else:
        df["ab_nominal_min"] = np.nan
    enc = df.DT_ENCERRAMENTO.dt.hour * 60 + df.DT_ENCERRAMENTO.dt.minute + df.DT_ENCERRAMENTO.dt.second / 60
    df["atraso_min"] = enc - (df.ab_nominal_min + 9 * 60)
    df["dur_min"] = (df.DT_ENCERRAMENTO - df.DT_ABERTURA).dt.total_seconds() / 60
    df["abre_atraso_min"] = df._ab_min - df.ab_nominal_min
    df["receb_h"] = df.DT_BU_RECEBIDO.dt.hour + df.DT_BU_RECEBIDO.dt.minute / 60
    df["valid2"] = df.lula + df["dir"]
    df["lula_sh"] = df.lula / df.valid2.replace(0, np.nan)
    df["dir_sh"] = df["dir"] / df.valid2.replace(0, np.nan)
    df["turnout"] = df.QT_COMPARECIMENTO / df.QT_APTOS.replace(0, np.nan)
    df["manual_rate"] = df.biom_nh / df.QT_COMPARECIMENTO.replace(0, np.nan)
    df["uf_local"] = (df.SG_UF + "_" + df.CD_MUNICIPIO.astype(str) + "_" + df.NR_ZONA.astype(str) + "_" +
                      df.NR_LOCAL_VOTACAO.astype(str))
    df["uf_zona"] = df.SG_UF + "_" + df.CD_MUNICIPIO.astype(str) + "_" + df.NR_ZONA.astype(str)
    return df.drop(columns=["_ab_min"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zips"); ap.add_argument("saida")
    ap.add_argument("--anos", type=int, nargs="+", required=True)
    ap.add_argument("--procs", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    zips = [z for z in glob.glob(os.path.join(a.zips, "*.zip")) if NOME_ZIP.match(os.path.basename(z))
            and info_zip(z)[0] in a.anos]
    zips.sort(key=os.path.getsize, reverse=True)
    esperado = 56 * len(a.anos)          # 28 UF (27 + ZZ) x 2 turnos por ano
    if len(zips) != esperado:
        raise SystemExit(f"ERRO: esperava {esperado} zips para {a.anos}, achei {len(zips)}")
    with ProcessPoolExecutor(a.procs) as ex:
        partes = []
        for i, r in enumerate(ex.map(processa, zips), 1):
            partes.append(r); print(f"[{i}/{esperado}] ok", flush=True)
    bruto = pd.concat(partes, ignore_index=True)
    df = finaliza(bruto)
    for (ano, t), g in df.groupby(["ano", "NR_TURNO"]):
        p = os.path.join(a.saida, f"bu_{ano}_t{t}.parquet")
        g.to_parquet(p, index=False)
        print(p, len(g), "secoes | lula, dir:", int(g.lula.sum()), int(g['dir'].sum()))


if __name__ == "__main__":
    main()
