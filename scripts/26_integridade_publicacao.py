#!/usr/bin/env python3
"""A26 (Fase 3): integridade da publicacao. Para cada arquivo de origem: tamanho, data de modificacao e hash oficial (.sha512/.sha1) HOJE x o primeiro download (arquivo local e hash baixado na epoca)
e capturas no Wayback Machine. Lista qualquer arquivo alterado depois da publicacao. Pre-registro: Adendo 8.
Limite declarado: nao re-baixa os zips (cerca de 8 GB); tamanho e hash oficial publicado sao comparados, e a reconferencia integral e `baixar_e_verificar.sh`.
Uso: python -I 26_integridade_publicacao.py data/urls_origem.txt DIR_ZIPS_LOCAIS... DIR_SAIDA   (os DIR_ZIPS_LOCAIS sao os diretorios do primeiro download)"""
import concurrent.futures as cf
import datetime as dt
import email.utils
import base64
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import pandas as pd

UA = {"User-Agent": "auditoria-independente (verificacao de integridade)"}


def head(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA, method="HEAD"), timeout=40)
        return r.status, int(r.headers.get("Content-Length", -1)), r.headers.get("Last-Modified", ""), r.headers.get("ETag", "")
    except Exception as e:                                         # noqa: BLE001
        return getattr(e, "code", 0), -1, "", str(e)[:60]


def texto(u):
    try:
        return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("latin-1").split()[0].lower()
    except Exception:                                              # noqa: BLE001
        return ""


def wayback(u):
    q = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode({"url": u, "output": "json", "limit": "20", "fl": "timestamp,statuscode,digest"})
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
        return d[1:]
    except Exception:                                              # noqa: BLE001
        return None


def digest_wayback(caminho):
    h = hashlib.sha1()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 22), b""):
            h.update(bloco)
    return base64.b32encode(h.digest()).decode()


def une(u, locais):
    nome = u.rsplit("/", 1)[-1]
    loc = next((os.path.join(d, nome) for d in locais if os.path.exists(os.path.join(d, nome))), None)
    st, tam, lm, et = head(u)
    r = dict(arquivo=nome, url=u, status_hoje=st, tamanho_hoje=tam, last_modified_hoje=lm, etag_hoje=et)
    if loc:
        r["tamanho_primeiro_download"] = os.path.getsize(loc)
        r["baixado_em"] = dt.datetime.fromtimestamp(os.path.getmtime(loc)).isoformat(timespec="seconds")
        for ext, alg in ((".sha512", "sha512"), (".sha1", "sha1")):
            antigo = loc + ext
            if os.path.exists(antigo):
                atual = texto(u + ext)
                r["algoritmo"] = alg
                r["hash_primeiro_download"] = open(antigo).read().split()[0].lower()
                r["hash_oficial_hoje"] = atual
                r["hash_igual"] = bool(atual) and atual == r["hash_primeiro_download"]
                break
        try:
            lmd = email.utils.parsedate_to_datetime(lm).replace(tzinfo=None) if lm else None
            r["modificado_depois_do_primeiro_download"] = bool(lmd and lmd > dt.datetime.fromtimestamp(os.path.getmtime(loc), dt.timezone.utc).replace(tzinfo=None))
        except Exception:                                          # noqa: BLE001
            r["modificado_depois_do_primeiro_download"] = None
    w = wayback(u)
    r["capturas_wayback"] = -1 if w is None else len(w)
    if w:
        r["primeira_captura_wayback"] = min(x[0] for x in w)
        ok200 = [x for x in w if x[1] == "200"]
        r["capturas_status_200"] = len(ok200)
        if ok200 and loc:
            dg = digest_wayback(loc)
            r["capturas_com_digest_igual_ao_arquivo_atual"] = sum(1 for x in ok200 if x[2] == dg)
    return r


def main(urls, locais, saida):
    os.makedirs(saida, exist_ok=True)
    us = [l.strip() for l in open(urls) if l.startswith("http")]
    with cf.ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(lambda u: une(u, locais), us))
    d = pd.DataFrame(rows)
    # o Wayback limita a taxa: repete as que falharam, 4 por vez
    def refaz(i):
        for _ in range(2):
            w = wayback(d.at[i, "url"])
            if w is not None:
                return i, w
            time.sleep(3)
        return i, None
    falhas = list(d.index[d.capturas_wayback < 0])
    with cf.ThreadPoolExecutor(4) as ex:
        for i, w in ex.map(refaz, falhas):
            if w is not None:
                d.at[i, "capturas_wayback"] = len(w)
                if w:
                    d.at[i, "primeira_captura_wayback"] = min(x[0] for x in w)
                    ok200 = [x for x in w if x[1] == "200"]
                    d.at[i, "capturas_status_200"] = len(ok200)
                    nome = d.at[i, "arquivo"]
                    loc = next((os.path.join(dd, nome) for dd in locais if os.path.exists(os.path.join(dd, nome))), None)
                    if ok200 and loc:
                        dg = digest_wayback(loc)
                        d.at[i, "capturas_com_digest_igual_ao_arquivo_atual"] = sum(1 for x in ok200 if x[2] == dg)
    d["tamanho_igual"] = d.tamanho_hoje == d.tamanho_primeiro_download
    d["alterado"] = ~d.tamanho_igual.fillna(False) | (d.hash_igual == False) | (d.modificado_depois_do_primeiro_download == True)   # noqa: E712
    d.to_csv(os.path.join(saida, "A26_integridade_publicacao.csv"), index=False)
    res = dict(arquivos=len(d), com_copia_local=int(d.tamanho_primeiro_download.notna().sum()), status_200=int((d.status_hoje == 200).sum()), tamanho_igual=int(d.tamanho_igual.sum()),
               hash_conferido=int(d.hash_igual.notna().sum()), hash_igual=int((d.hash_igual == True).sum()), hash_diferente=int((d.hash_igual == False).sum()),    # noqa: E712
               modificados_depois_do_primeiro_download=int((d.modificado_depois_do_primeiro_download == True).sum()), alterados=int(d.alterado.sum()),    # noqa: E712
               com_captura_no_wayback=int((d.capturas_wayback > 0).sum()), capturas_status_200_total=int(d.get("capturas_status_200", pd.Series(dtype=float)).fillna(0).sum()), capturas_com_digest_igual=int(d.get("capturas_com_digest_igual_ao_arquivo_atual", pd.Series(dtype=float)).fillna(0).sum()), capturas_com_digest_diferente=int((d.get("capturas_status_200", pd.Series(dtype=float)).fillna(0) - d.get("capturas_com_digest_igual_ao_arquivo_atual", pd.Series(dtype=float)).fillna(0)).sum()), wayback_indisponivel=int((d.capturas_wayback < 0).sum()), consultado_em=dt.datetime.now().isoformat(timespec="minutes"))
    pd.DataFrame([res]).to_csv(os.path.join(saida, "A26_resumo.csv"), index=False)
    d[d.alterado | (d.status_hoje != 200)].to_csv(os.path.join(saida, "A26_arquivos_alterados_ou_indisponiveis.csv"), index=False)
    print(res)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:-1], sys.argv[-1])
