"""Leitor minimo de arquivos de urna do TSE (BU, RDV, log).

O BU e o RDV sao ASN.1 BER. A especificacao oficial (ASN.1) nao pode ser baixada por automacao (tse.jus.br responde 403), entao este leitor
e GENERICO (TLV) e o mapeamento de campos e VALIDADO empiricamente contra o BWeb (ver 08_a4_cadeia_urna.py): so se usa o campo cujo valor decodificado
coincide com o BWeb em 100% das secoes validadas. Nenhum campo e inferido sem essa checagem."""
import io
import os
import zipfile


class Node:
    __slots__ = ("cls", "cons", "tag", "val", "kids")

    def __init__(self, cls, cons, tag, val, kids):
        self.cls, self.cons, self.tag, self.val, self.kids = cls, cons, tag, val, kids

    def __repr__(self):
        return f"N(c{self.cls}{'C' if self.cons else 'P'}{self.tag} {self.val[:6].hex() if self.val is not None else ''} k={len(self.kids) if self.kids else 0})"


def parse(buf, off=0, end=None):
    """Decodifica TLVs BER (comprimento definido) em arvore. Levanta ValueError em estrutura invalida."""
    end = len(buf) if end is None else end
    out = []
    while off < end:
        b0 = buf[off]; off += 1
        cls, cons, tag = b0 >> 6, bool(b0 & 0x20), b0 & 0x1F
        if tag == 0x1F:
            tag = 0
            while True:
                b = buf[off]; off += 1
                tag = (tag << 7) | (b & 0x7F)
                if not b & 0x80:
                    break
        l = buf[off]; off += 1
        if l & 0x80:
            n = l & 0x7F
            if n == 0:
                raise ValueError("comprimento indefinido nao suportado")
            l = int.from_bytes(buf[off:off + n], "big"); off += n
        if off + l > end:
            raise ValueError("TLV excede o buffer")
        if cons:
            out.append(Node(cls, True, tag, None, parse(buf, off, off + l)))
        else:
            out.append(Node(cls, False, tag, bytes(buf[off:off + l]), None))
        off += l
    return out


def to_int(n):
    return int.from_bytes(n.val, "big")


def walk(nodes):
    for n in nodes:
        yield n
        if n.kids:
            yield from walk(n.kids)


def bu_interno(buf):
    """Devolve a arvore do BU interno (o OCTET STRING do envelope contem o BU assinado)."""
    t = parse(buf)
    env = t[0]
    octs = [k for k in env.kids if not k.cons and k.tag == 4]
    if not octs:
        raise ValueError("envelope do BU sem OCTET STRING")
    return parse(octs[0].val)[0]


def votos_bu(inner):
    """Todas as entradas de votos do BU interno: lista de (cargo, indice, qtd, partido, numero, tipo_ctx1).
    Entrada = SEQUENCE com filhos [1] prim, [2] prim, [3] cons opcional, INTEGER, OCTET STRING(64)."""
    res = []

    def rec(n, cargo):
        if not n.kids:
            return
        # bloco de cargo: SEQUENCE com [1] prim (cargo) e INTEGER e SEQUENCE de entradas
        for k in n.kids:
            if k.kids:
                rec(k, cargo)
        tags = [(k.cls, k.cons, k.tag) for k in n.kids]
        if (2, False, 1) in tags and (2, False, 2) in tags and (0, False, 4) in tags:
            d = {(k.cls, k.cons, k.tag): k for k in n.kids}
            q = to_int(d[(2, False, 2)])
            t1 = to_int(d[(2, False, 1)])
            pn = None
            if (2, True, 3) in d:
                ks = d[(2, True, 3)].kids
                pn = tuple(to_int(x) for x in ks)
            idx = to_int(d[(0, False, 2)]) if (0, False, 2) in d else None
            res.append((t1, q, pn, idx))
    rec(inner, None)
    return res


def cargos_bu(inner):
    """Agrupa as entradas por bloco de cargo: SEQUENCE que contem [1] prim (codigo do cargo) seguido de SEQUENCE de entradas."""
    out = []
    for n in walk([inner]):
        if n.kids:
            cod = [k for k in n.kids if k.cls == 2 and not k.cons and k.tag == 1]
            ents = [k for k in n.kids if k.cons and k.tag == 16 and k.cls == 0]
            if cod and ents and any(x.kids and any(y.cls == 2 and y.tag == 2 for y in x.kids) for x in ents):
                out.append((to_int(cod[0]), n))
    return out


def ler_log(zbytes):
    """Log da urna: 2026 = zip com logd.dat; 2022 = 7z com logd.dat."""
    if zbytes[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(zbytes))
        nome = [x for x in z.namelist() if x.lower().endswith(".dat")]
        return z.read(nome[0]).decode("latin-1").splitlines()
    if zbytes[:2] == b"7z":
        import py7zr, tempfile
        with tempfile.TemporaryDirectory() as td:
            with py7zr.SevenZipFile(io.BytesIO(zbytes)) as z:
                z.extractall(td)
            nome = [x for x in os.listdir(td) if x.lower().endswith(".dat")]
            return open(os.path.join(td, nome[0]), "rb").read().decode("latin-1").splitlines()
    raise ValueError("log em formato desconhecido (nem zip nem 7z)")


# ---------------------------------------------------------------------------------------------- Fase 2: extracao por secao
import hashlib
import re
from collections import Counter

NUMERIC_STRING = 18


def bu_cargos(inner):
    """{cargo: [(tipo, qtd, (partido, numero)|None), ...]} do BU interno. Bloco de cargo = no com filho [1] primitivo (codigo) e SEQUENCE de entradas."""
    out = {}
    for n in walk([inner]):
        if not n.kids:
            continue
        cod = [k for k in n.kids if k.cls == 2 and not k.cons and k.tag == 1]
        seqs = [k for k in n.kids if k.cls == 0 and k.cons and k.tag == 16]
        if cod and seqs:
            ents = []
            for e in seqs[-1].kids:
                if e.kids and any(c.cls == 2 and not c.cons and c.tag == 2 for c in e.kids):
                    d = {(c.cls, c.cons, c.tag): c for c in e.kids}
                    q = to_int(d[(2, False, 2)]); t1 = to_int(d[(2, False, 1)])
                    pn = tuple(to_int(x) for x in d[(2, True, 3)].kids) if (2, True, 3) in d else None
                    ents.append((t1, q, pn))
            if ents:
                out[to_int(cod[0])] = ents
    return out


def bu_campos(buf):
    """Campos do BU: aptos, comparecimento, urna, carga (24 digitos), encerramento/emissao (texto), cargos."""
    inner = bu_interno(buf)
    gs = [n for n in walk([inner]) if not n.cons and n.tag == 27]
    ints = [n for n in inner.kids if not n.cons and n.tag == 2]
    emissao = next((g.val.decode("latin-1") for g in inner.kids if not g.cons and g.tag == 27 and re.fullmatch(rb"\d{8}T\d{6}", g.val)), None)
    cg = next((g.val.decode("latin-1") for g in gs if re.fullmatch(rb"\d{24}", g.val)), None)
    # aptos: segundo INTEGER do bloco que comeca com o codigo da eleicao
    aptos = None
    for n in walk([inner]):
        if n.kids and len(n.kids) >= 4 and all((not k.cons and k.tag == 2) for k in n.kids[:4]):
            aptos = to_int(n.kids[1]); break
    urna = next((to_int(n) for n in walk([inner]) if not n.cons and n.tag == 2 and n.val and len(n.val) == 3 and False), None)
    return dict(comparecimento=to_int(ints[0]) if ints else None, aptos=aptos, emissao=emissao, carga24=cg, cargos=bu_cargos(inner))


def rdv_cargos(buf):
    """{cargo: Counter((enum, numero_str))} do RDV."""
    root = parse(buf)[0]
    out = {}
    for n in walk([root]):
        if not n.kids:
            continue
        cod = [k for k in n.kids if k.cls == 2 and not k.cons and k.tag == 1]
        seqs = [k for k in n.kids if k.cls == 0 and k.cons and k.tag == 16]
        if cod and seqs:
            c = Counter()
            ok = False
            for e in seqs[-1].kids:
                if e.kids and e.kids[0].tag == 10 and (len(e.kids) == 1 or (len(e.kids) == 2 and e.kids[1].tag == NUMERIC_STRING)):
                    c[(to_int(e.kids[0]), e.kids[1].val.decode("latin-1") if len(e.kids) == 2 else "")] += 1; ok = True
            if ok:
                out[to_int(cod[0])] = c
    return out


def vsc_checa(vsc, arquivos):
    """Vinculo de integridade: o SHA-512 de cada arquivo entregue aparece na lista assinada da urna e o SHA-512 da lista confere com o hash do bloco.
    NAO verifica a assinatura criptografica (chave de curva de 521 bits com OID 1.3.6.1.4.1.44588.2.1, sem suporte e sem a especificacao do TSE)."""
    t = parse(vsc)[0]
    blk = t.kids[1]
    octs = [k for k in blk.kids if not k.cons and k.tag == 4]
    lista = octs[0].val if octs else b""
    h64 = next((o.val for o in walk([blk]) if not o.cons and o.tag == 4 and len(o.val) == 64), None)
    res = {"lista_hash_ok": bool(h64) and hashlib.sha512(lista).digest() == h64}
    for nome, b in arquivos.items():
        res[f"{nome}_hash_na_lista"] = hashlib.sha512(b).digest() in lista
    return res


PAT_HAB = "Eleitor foi habilitado"
PAT_CONF = "Voto confirmado para [Presidente]"
PAT_COMP = "O voto do eleitor foi computado"


def log_metricas(linhas, nominal_min, dia):
    """Metricas do log. nominal_min = minuto do dia (relogio local da urna) do fechamento nominal. dia = 'dd/mm/aaaa' da eleicao."""
    ts_hab, ts_comp, ts_pres = [], [], []
    ev = Counter(); versao = None; sucesso = 0; falha_ass = 0; tipos = Counter(); modo = None
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5:
            continue
        data, hora = p[0][:10], p[0][11:19]
        msg = p[4]
        if msg.startswith("Versão da aplicação"):
            versao = msg.split(":", 1)[1].strip()
        elif msg.startswith("Iniciando aplicação"):
            modo = msg
        if msg.startswith("Verificação de assinatura de aplicação"):
            if "[SUCESSO]" in msg:
                sucesso += 1
            else:
                falha_ass += 1
        if data != dia:
            continue
        hh, mm, ss = int(hora[:2]), int(hora[3:5]), int(hora[6:8])
        sec = hh * 3600 + mm * 60 + ss
        if msg == PAT_HAB:
            ts_hab.append(sec)
        elif msg == PAT_COMP:
            ts_comp.append(sec)
        elif msg == PAT_CONF:
            ts_pres.append(sec)
        elif msg.startswith("Tipo de habilitação do eleitor"):
            tipos[msg.split("[", 1)[1].rstrip("]") if "[" in msg else msg] += 1
        elif "habilitação manual" in msg:
            ev["solicita_dado_habilitacao_manual"] += 1
        elif p[1] == "ALERTA":
            ev["alerta"] += 1
        elif p[1] not in ("INFO",):
            ev["outro_nivel_" + p[1]] += 1
        if "Urna de contingência" in msg:
            ev["contingencia_urna"] += 1
        low = msg.lower()
        for k in ("contingên", "substitu", "reinici", "reiniciad", "interrup", "falha", "erro"):
            if k in low:
                ev["kw_" + k] += 1
    ts_hab.sort(); ts_comp.sort()
    gaps = [b - a for a, b in zip(ts_hab, ts_hab[1:])]
    nominal_s = nominal_min * 60
    apos = [t for t in ts_comp if t > nominal_s]
    return dict(n_habilitado=len(ts_hab), n_voto_presidente=len(ts_pres), n_computado=len(ts_comp), primeiro_voto_s=ts_comp[0] if ts_comp else None,
                ultimo_voto_s=ts_comp[-1] if ts_comp else None, votos_apos_nominal=len(apos), min_gap_hab_s=min(gaps) if gaps else None,
                n_gap_lt_10s=sum(1 for g in gaps if g < 10), n_gap_lt_5s=sum(1 for g in gaps if g < 5), versao=versao, modo=modo,
                assin_app_sucesso=sucesso, assin_app_falha=falha_ass, **{f"ev_{k}": v for k, v in ev.items()}, **{f"hab_{k}": v for k, v in tipos.items()})
