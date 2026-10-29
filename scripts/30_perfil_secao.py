#!/usr/bin/env python3
"""Fase 3.1 (A20b-idosos): baixa o perfil do eleitorado por secao (TSE) e agrega por secao: aptos, biometria cadastrada e aptos nas faixas 80+, 90+ e 100+.
Saidas em DIR_SAIDA: perfil_secao_{ano}.parquet (uma linha por secao) e perfil_faixas_{ano}.parquet (UF x faixa etaria: aptos e biometria cadastrada).
Os zips ficam em DIR_ZIPS (para o SHA-256 em data/sha256_entradas.txt). Pre-registro: Adendo 9.
Uso: python -I 30_perfil_secao.py DIR_ZIPS DIR_SAIDA 2018 2022 2026"""
import hashlib
import os
import sys
import time
import urllib.request
import zipfile
import pandas as pd

UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO ZZ".split()
BASE = "https://cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitor_secao/perfil_eleitor_secao_{ano}_{uf}.zip"
F80 = ["80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais"]
F90 = F80[2:]
F100 = F80[4:]
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]


def baixa(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return
    for t in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "auditoria-independente-reproduzivel"})
            with urllib.request.urlopen(req, timeout=300) as r, open(dest + ".part", "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            os.replace(dest + ".part", dest)
            return
        except Exception as e:
            time.sleep(5 * (t + 1))
            err = e
    raise SystemExit(f"ERRO ao baixar {url}: {err}")


def le(zpath, ano):
    z = zipfile.ZipFile(zpath)
    nome = [n for n in z.namelist() if n.lower().endswith(".csv")]
    if len(nome) != 1:
        raise SystemExit(f"ERRO {zpath}: csv {nome}")
    with z.open(nome[0]) as f:
        hdr = list(pd.read_csv(f, sep=";", encoding="latin-1", nrows=0).columns)
    qt = [c for c in ("QT_ELEITORES", "QT_ELEITORES_PERFIL") if c in hdr]
    bio = [c for c in ("QT_ELEITORES_BIOMETRIA",) if c in hdr]
    falta = [c for c in ("SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "DS_FAIXA_ETARIA") if c not in hdr]
    if not qt or not bio or falta:
        raise SystemExit(f"ERRO {zpath}: colunas ausentes {falta} qt={qt} bio={bio}")
    with z.open(nome[0]) as f:
        d = pd.read_csv(f, sep=";", encoding="latin-1", usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO", "DS_FAIXA_ETARIA", qt[0], bio[0]], dtype=str)
    d = d.rename(columns={qt[0]: "apt", bio[0]: "bio"})
    d["apt"] = pd.to_numeric(d.apt, errors="coerce").fillna(0)
    d["bio"] = pd.to_numeric(d.bio, errors="coerce").fillna(0)
    d["faixa"] = d.DS_FAIXA_ETARIA.str.strip()
    for c in ("CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO"):
        d[c] = pd.to_numeric(d[c], errors="coerce").astype("Int64")
    return d


def agrega(d):
    s = d.groupby(KEY + ["NR_LOCAL_VOTACAO"], dropna=False).agg(apt=("apt", "sum"), bio=("bio", "sum")).reset_index()
    for nome, fx in (("80", F80), ("90", F90), ("100", F100)):
        q = d[d.faixa.isin(fx)].groupby(KEY).agg(**{f"apt{nome}": ("apt", "sum"), f"bio{nome}": ("bio", "sum")}).reset_index()
        s = s.merge(q, on=KEY, how="left")
    s = s.fillna({c: 0 for c in s.columns if c.startswith(("apt", "bio"))})
    f = d.groupby(["SG_UF", "faixa"]).agg(apt=("apt", "sum"), bio=("bio", "sum")).reset_index()
    return s, f


def main(zdir, saida, anos):
    os.makedirs(zdir, exist_ok=True); os.makedirs(saida, exist_ok=True)
    shas = []
    for ano in anos:
        S, F = [], []
        for uf in UFS:
            url = BASE.format(ano=ano, uf=uf)
            dest = os.path.join(zdir, f"perfil_eleitor_secao_{ano}_{uf}.zip")
            baixa(url, dest)
            shas.append((hashlib.sha256(open(dest, "rb").read()).hexdigest(), os.path.basename(dest), url))
            s, f = agrega(le(dest, ano)); S.append(s); F.append(f)
            print(ano, uf, len(s), flush=True)
        S = pd.concat(S, ignore_index=True); F = pd.concat(F, ignore_index=True).groupby(["SG_UF", "faixa"], as_index=False)[["apt", "bio"]].sum()
        S.to_parquet(os.path.join(saida, f"perfil_secao_{ano}.parquet"), index=False)
        F.to_parquet(os.path.join(saida, f"perfil_faixas_{ano}.parquet"), index=False)
        print(ano, "secoes", len(S), "aptos", int(S.apt.sum()), flush=True)
    with open(os.path.join(saida, "sha256_perfil_secao.txt"), "w") as f:
        f.write("\n".join(f"{h}  {n}  {u}" for h, n, u in shas) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(a) for a in sys.argv[3:]])
