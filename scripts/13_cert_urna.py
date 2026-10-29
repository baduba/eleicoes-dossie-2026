#!/usr/bin/env python3
"""Fase 2.1 (A4, parte da assinatura): inspeciona o certificado da urna embutido no arquivo de assinatura de cada secao.
Verifica o que e verificavel SEM a especificacao do TSE: estrutura X.509, CN do certificado = numero da urna do BWeb, emissor, validade cobrindo a data da eleicao,
OID do algoritmo, tamanhos de chave e de assinatura. NAO verifica a assinatura criptografica nem a cadeia ate a raiz.
Uso: python -I 13_cert_urna.py ZIP_ARQURNATOT ANO TURNO BWEB_PARQUET SAIDA.csv"""
import base64, os, re, sys, zipfile
from datetime import datetime
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import urna_parse as U

OIDN = {"2.5.4.3": "CN", "2.5.4.10": "O", "2.5.4.11": "OU", "2.5.4.7": "L", "2.5.4.8": "ST", "2.5.4.6": "C"}


def oid(b):
    a = [b[0] // 40, b[0] % 40]; v = 0
    for x in b[1:]:
        v = (v << 7) | (x & 0x7F)
        if not x & 0x80:
            a.append(v); v = 0
    return ".".join(map(str, a))


def nome(seq):
    d = {}
    for rdn in seq.kids:
        for atv in rdn.kids:
            d[OIDN.get(oid(atv.kids[0].val), oid(atv.kids[0].val))] = atv.kids[1].val.decode("utf-8", "replace")
    return d


def cert_info(vsc):
    t = U.parse(vsc)[0]; blk = t.kids[1]
    pem = [k for k in blk.kids if k.cls == 2 and k.tag == 1][0].val
    der = base64.b64decode(re.sub(rb"-----[^-]+-----|\s", b"", pem))
    c = U.parse(der)[0]; tbs = c.kids[0]
    k = [x for x in tbs.kids if not (x.cls == 2)]          # serial, sigalg, issuer, validity, subject, spki
    sigalg, issuer, valid, subject, spki = oid(k[1].kids[0].val), nome(k[2]), k[3], nome(k[4]), k[5]
    f = lambda n: datetime.strptime(n.val.decode(), "%y%m%d%H%M%SZ")
    return dict(cert_alg_assinatura=sigalg, cert_alg_chave=oid(spki.kids[0].kids[0].val), cert_chave_bytes=len(spki.kids[1].val) - 1, cert_assinatura_emissor_bytes=len(c.kids[2].val) - 1,
                emissor_cn=issuer.get("CN"), emissor_o=issuer.get("O"), sujeito_cn=subject.get("CN"), valido_de=f(valid.kids[0]), valido_ate=f(valid.kids[1]))


def main(zp, ano, turno, bweb, saida):
    uf = os.path.basename(zp).split("_")[-1][:2].upper()
    b = pd.read_parquet(bweb); b = b[b.SG_UF == uf].set_index(["CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"])
    z = zipfile.ZipFile(zp); rows = []
    dia = {(2026, 2): datetime(2026, 10, 25), (2022, 2): datetime(2022, 10, 30)}[(ano, turno)]
    for n in z.namelist():
        m = re.search(r"o\d{5}%s(\d{5})(\d{4})(\d{4})-vota\.vsc$" % uf.lower(), n) if ano == 2026 else re.search(r"o\d{5}-(\d{5})(\d{4})(\d{4})\.vscmr$", n)
        if not m:
            continue
        key = tuple(int(x) for x in m.groups())
        r = dict(uf=uf, cd_municipio=key[0], zona=key[1], secao=key[2])
        try:
            r.update(cert_info(z.read(n)))
            urna = int(b.loc[key].NR_URNA) if key in b.index else None
            r["urna_bweb"] = urna
            r["cn_confere_com_urna"] = urna is not None and r["sujeito_cn"] == f"UEAO{urna:08d}"
            r["valido_na_eleicao"] = r["valido_de"] <= dia <= r["valido_ate"]
        except Exception as e:                                   # noqa: BLE001
            r["erro"] = f"{type(e).__name__}: {e}"
        rows.append(r)
    d = pd.DataFrame(rows); d.to_csv(saida, index=False)
    if "erro" in d and d.erro.notna().all():
        print("ERRO em todas as secoes:", d.erro.value_counts().head(3).to_dict()); return
    print(saida, len(d), "| erros:", int(d.get("erro", pd.Series(dtype=object)).notna().sum()), "| CN confere:", int(d.cn_confere_com_urna.sum()), "| valido:", int(d.valido_na_eleicao.sum()),
          "| emissores:", d.emissor_cn.value_counts().to_dict(), "| algoritmos:", d.cert_alg_chave.value_counts().to_dict())


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5])
