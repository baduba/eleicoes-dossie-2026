#!/usr/bin/env python3
"""A36, canal 2: importa o CSV exportado do formulario Jotform (https://form.jotform.com/263017066351047) e aplica o pipeline do canal 1.
Passos: (1) mapeia as colunas pelo TEXTO da pergunta, nao pela posicao; (2) exclui submissoes de teste (Observacoes com "TESTE"); (3) resolve os anexos exportados, remove EXIF e todo metadado
(a imagem e recomposta so com os pixels; o original nunca e copiado nem publicado); (4) tenta ler o QR Code (OpenCV, se instalado); (5) confere a transcricao com o BWeb
(`04_cruza_bu_impresso.compara`); (6) grava os resultados com origem "formulario" e o ID da submissao.
Uso: python -I importa_formulario.py EXPORT.csv DIR_PARQUET DIR_SAIDA [--anexos DIR] [--mapa A20_mapa_tse_ibge.csv]
Saidas em DIR_SAIDA: formulario_resultados.csv, formulario_comparacao.csv, formulario_resumo.csv, mapeamento_colunas.csv, fotos/<id>_<n>.jpg (sem metadados).
Nao publica: texto livre das observacoes, IP, e-mail, nome ou qualquer coluna fora do mapeamento."""
import argparse
import csv
import hashlib
import importlib.util
import io
import os
import re
import sys
import unicodedata
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bu04", os.path.join(AQUI, "04_cruza_bu_impresso.py"))
bu04 = importlib.util.module_from_spec(spec); spec.loader.exec_module(bu04)

# campo canonico -> padroes (texto da pergunta sem acento, minusculo); a primeira coluna livre que casa fica com o campo
CAMPOS = [
    ("id", [r"^submission id$", r"\bid da submiss", r"^id$", r"^id do envio$"]),
    ("data", [r"^submission date$", r"data (e hora )?do envio", r"^data$"]),
    ("observacoes", [r"observ", r"coment"]),
    ("uf", [r"\buf\b", r"\bestado\b", r"unidade da federa"]),
    ("municipio", [r"munic", r"cidade"]),
    ("zona", [r"\bzona\b"]),
    ("secao", [r"\bsecao\b", r"numero da secao", r"\bsecao\b"]),
    ("turno", [r"\bturno\b"]),
    ("origem_declarada", [r"origem", r"quem (esta )?envia", r"voce e", r"\bpapel\b", r"\bfuncao\b"]),
    ("aptos", [r"\baptos\b", r"eleitores aptos", r"eleitorado apto"]),
    ("comparecimento", [r"comparec", r"\bvotantes\b"]),
    ("lula", [r"lula"]),
    ("oponente", [r"oponente", r"flavio", r"candidato 2"]),
    ("brancos", [r"branc"]),
    ("nulos", [r"\bnul"]),
]
EXT_IMG = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff")
RX_ARQ = re.compile(r"(?:\.(?:jpe?g|png|webp|bmp|gif|tiff?|heic|heif|pdf))(?:\?|$|\s|;|,)", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()


def mapeia(colunas, df=None):
    """Retorna ({campo: coluna}, [colunas de anexo], [colunas nao mapeadas])."""
    livre = {c: norm(c) for c in colunas}
    mp = {}
    for campo, pads in CAMPOS:
        for c, n in list(livre.items()):
            if any(re.search(p, n) for p in pads):
                mp[campo] = c; del livre[c]; break
    anexos = []
    if df is not None:
        for c in list(livre):
            if df[c].astype(str).str.contains(RX_ARQ).any() or re.search(r"foto|anexo|arquivo|imagem|upload|boletim|\bqr\b", livre[c]):
                anexos.append(c); del livre[c]
    return mp, anexos, list(livre)


def eh_teste(v):
    return bool(re.search(r"\bteste\b", norm(v)))


def refs_anexo(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return []
    return [x.strip() for x in re.split(r"[\n;,]\s*(?=\S)", str(v)) if RX_ARQ.search(x + " ")]


def acha_arquivo(ref, indice, sid):
    base = os.path.basename(ref.split("?")[0]).strip()
    cand = indice.get(base.lower(), [])
    if len(cand) > 1:
        pref = [c for c in cand if str(sid) in c]
        cand = pref or cand
    return cand[0] if cand else None


def indexa(dirp):
    idx = {}
    for r, _, fs in os.walk(dirp):
        for f in fs:
            idx.setdefault(f.lower(), []).append(os.path.join(r, f))
    return idx


def sanitiza(caminho, destino):
    """Recompoe a imagem so com os pixels (sem EXIF, GPS, ICC, XMP, comentarios). Retorna (ok, motivo)."""
    from PIL import Image, ImageOps
    if not caminho.lower().endswith(EXT_IMG):
        return False, "formato nao suportado (HEIC/PDF): converter para JPEG antes de enviar; o arquivo original nao e publicado"
    try:
        with Image.open(caminho) as im:
            im = ImageOps.exif_transpose(im)               # respeita a orientacao antes de descartar o EXIF
            im = im.convert("RGB")
            limpo = Image.frombytes("RGB", im.size, im.tobytes())
        limpo.save(destino, "JPEG", quality=90, optimize=True)
        with Image.open(destino) as chk:
            if len(chk.getexif()) or any(k in chk.info for k in ("exif", "icc_profile", "xmp", "comment")):
                os.remove(destino); return False, "falha ao remover metadados"
        return True, ""
    except Exception as e:                                  # noqa: BLE001
        return False, f"imagem ilegivel ({type(e).__name__})"


def le_qr(caminho):
    """Texto do QR Code, se o OpenCV estiver instalado e achar um; senao None."""
    try:
        import cv2
    except ImportError:
        return None, "opencv ausente"
    im = cv2.imread(caminho)
    if im is None:
        return None, "imagem nao aberta"
    det = cv2.QRCodeDetector()
    for esc in (1, 2):
        x = im if esc == 1 else cv2.resize(im, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        try:
            txt, _, _ = det.detectAndDecode(x)
        except Exception:                                   # noqa: BLE001
            txt = ""
        if txt:
            return txt, "lido"
    return None, "nenhum QR legivel"


ALIAS_QR = {"ZONA": "zona", "SECA": "secao", "SECAO": "secao", "TURN": "turno", "TURNO": "turno"}


def campos_qr(txt):
    """Campos de identificacao reconhecidos no texto do QR (zona, secao, turno). Layout do QR do BU nao validado contra uma amostra real: so cruza identificacao."""
    out = {}
    for k, v in re.findall(r"\b([A-Z]{3,5}):(\d+)\b", txt or ""):
        if k in ALIAS_QR:
            out[ALIAS_QR[k]] = int(v)
    return out


def num(v):
    try:
        s = str(v).strip().replace(".", "").replace(" ", "")
        return int(float(s.replace(",", "."))) if s not in ("", "nan", "None") else None
    except ValueError:
        return None


def carrega_municipios(mapa):
    m = pd.read_csv(mapa, dtype=str)
    m["n"] = m.NM_MUNICIPIO.map(norm)
    return {(r.SG_UF, r.n): int(r.CD_MUNICIPIO) for r in m.itertuples()}, set(zip(m.SG_UF, m.CD_MUNICIPIO.astype(int)))


def le_csv(caminho):
    raw = open(caminho, "rb").read().decode("utf-8-sig", errors="replace")
    try:
        d = csv.Sniffer().sniff(raw[:5000], delimiters=",;\t").delimiter
    except csv.Error:
        d = ","
    return pd.read_csv(io.StringIO(raw), sep=d, dtype=str, keep_default_na=False)


def importa(caminho_csv, pq, saida, anexos_dir=None, mapa=None):
    os.makedirs(os.path.join(saida, "fotos"), exist_ok=True)
    df = le_csv(caminho_csv)
    mp, col_anexos, sem_map = mapeia(list(df.columns), df)
    pd.DataFrame([dict(campo=k, coluna=v) for k, v in mp.items()] + [dict(campo="anexo", coluna=c) for c in col_anexos] + [dict(campo="(nao usada e nao publicada)", coluna=c) for c in sem_map]).to_csv(os.path.join(saida, "mapeamento_colunas.csv"), index=False)
    idx = indexa(anexos_dir or os.path.dirname(os.path.abspath(caminho_csv)))
    mun, codigos = carrega_municipios(mapa or os.path.join(AQUI, "..", "results", "fase3", "A20_mapa_tse_ibge.csv"))
    linhas, entrada, n_teste = [], [], 0
    for i, r in df.iterrows():
        g = lambda k: r[mp[k]] if k in mp else ""
        sid = (g("id") or f"linha{i + 2}").strip()
        if eh_teste(g("observacoes")):
            n_teste += 1; continue
        uf = norm(g("uf")).split(" ")[0].upper() if g("uf") else ""
        mtxt = str(g("municipio")).strip()
        cd = int(mtxt) if mtxt.isdigit() else mun.get((uf, norm(mtxt)))
        zona, secao, turno = num(g("zona")), num(g("secao")), num(g("turno"))
        nums = {k: num(g(k)) for k in ("aptos", "comparecimento", "lula", "oponente", "brancos", "nulos")}
        fotos, motivos_foto, qr_estado, qr_ids = [], [], "", {}
        for c in col_anexos:
            for k, ref in enumerate(refs_anexo(r[c]), 1):
                orig = acha_arquivo(ref, idx, sid)
                if not orig:
                    motivos_foto.append(f"anexo nao encontrado na exportacao ({os.path.basename(ref)})"); continue
                dest = os.path.join(saida, "fotos", f"{re.sub(r'[^A-Za-z0-9_-]', '', sid)}_{len(fotos) + 1}.jpg")
                ok, mot = sanitiza(orig, dest)
                if not ok:
                    motivos_foto.append(mot); continue
                fotos.append(os.path.relpath(dest, saida))
                if not qr_estado or qr_estado != "lido":
                    txt, qr_estado = le_qr(dest); qr_ids = campos_qr(txt) if txt else qr_ids
        base = dict(canal="formulario", id_submissao=sid, data_envio=g("data"), origem_declarada=str(g("origem_declarada")).strip(), uf=uf, municipio=mtxt, cd_municipio=cd, zona=zona, secao=secao, turno=turno,
                    fotos_publicadas=";".join(fotos), qr=qr_estado or "sem foto", tem_observacao=bool(str(g("observacoes")).strip()))
        ident = all(v is not None for v in (cd, zona, secao, turno)) and uf != ""
        if qr_ids:
            dif = [k for k, v in (("zona", zona), ("secao", secao), ("turno", turno)) if k in qr_ids and qr_ids[k] != v]
            if dif:
                base["qr"] = "diverge do formulario em " + ",".join(dif)
        if not ident:
            linhas.append({**base, "status": "descartada: sem identificacao da secao (UF, municipio reconhecido, zona, secao, turno)", "campos_divergentes": ""}); continue
        if any(v is None for v in nums.values()):
            linhas.append({**base, "status": "recebida, sem transcricao dos numeros: pendente de leitura da foto" if fotos else "descartada: sem numeros e sem foto legivel", "campos_divergentes": "; ".join(motivos_foto)}); continue
        entrada.append(dict(ano=2026, turno=turno, uf=uf, cd_municipio=cd, zona=zona, secao=secao, **nums, _sid=sid))
        linhas.append({**base, "status": "A_CONFERIR", "campos_divergentes": "; ".join(motivos_foto)})
    R = pd.DataFrame(linhas)
    comp = pd.DataFrame()
    if entrada:
        E = pd.DataFrame(entrada)
        comp = bu04.compara(pq, E.drop(columns="_sid"))
        comp["id_submissao"] = comp.apply(lambda x: E[(E.uf == x.uf) & (E.zona == x.zona) & (E.secao == x.secao) & (E.turno == x.turno)]._sid.iloc[0], axis=1)
        comp["canal"] = "formulario"
        for sid, g_ in comp.groupby("id_submissao"):
            dv = g_[g_.diverge]
            m = R.id_submissao == sid
            R.loc[m, "status"] = "conferida sem divergencia" if dv.empty else f"DIVERGENCIA em {len(dv)} campo(s)"
            R.loc[m, "campos_divergentes"] = R.loc[m, "campos_divergentes"] + ("; " if (R.loc[m, "campos_divergentes"] != "").any() and len(dv) else "") + ", ".join(dv.campo.astype(str))
    R.to_csv(os.path.join(saida, "formulario_resultados.csv"), index=False)
    comp.to_csv(os.path.join(saida, "formulario_comparacao.csv"), index=False)
    S = pd.DataFrame([dict(submissoes_no_csv=len(df), teste_excluidas=n_teste, recebidas=len(R), conferidas_sem_divergencia=int((R.status == "conferida sem divergencia").sum()) if len(R) else 0,
                           com_divergencia=int(R.status.str.startswith("DIVERGENCIA").sum()) if len(R) else 0, pendentes_de_leitura=int(R.status.str.startswith("recebida").sum()) if len(R) else 0,
                           descartadas=int(R.status.str.startswith("descartada").sum()) if len(R) else 0)])
    S.to_csv(os.path.join(saida, "formulario_resumo.csv"), index=False)
    return R, comp, S, mp, col_anexos, sem_map


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("csv"); ap.add_argument("parquet"); ap.add_argument("saida"); ap.add_argument("--anexos", default=None); ap.add_argument("--mapa", default=None)
    a = ap.parse_args()
    R, comp, S, mp, ca, sm = importa(a.csv, a.parquet, a.saida, a.anexos, a.mapa)
    print("colunas mapeadas:", {k: v for k, v in mp.items()}, "| anexos:", ca, "| nao usadas:", sm)
    print(S.to_string(index=False))
    if len(R):
        print(R[["id_submissao", "uf", "municipio", "zona", "secao", "turno", "origem_declarada", "status"]].to_string(index=False))
