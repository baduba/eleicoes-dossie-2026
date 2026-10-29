#!/usr/bin/env python3
"""Teste direto: cruza boletins de urna impressos (transcritos ou lidos do QR code) com o BWeb e reporta QUALQUER divergencia.

Uso: python -I 04_cruza_bu_impresso.py DIR_PARQUET entrada.csv [saida.csv]

entrada.csv (separador ';'), colunas obrigatorias:
  ano;turno;uf;cd_municipio;zona;secao;aptos;comparecimento;lula;oponente;brancos;nulos
colunas opcionais (comparadas se existirem): abertura;encerramento   (horario LOCAL da urna, 'AAAA-MM-DD HH:MM:SS')
cd_municipio e o codigo TSE do municipio (o BU impresso traz o nome; use a tabela do TSE para obter o codigo).
Sem cd_municipio unico (uf+zona+secao ambiguos) o script ERRA em vez de escolher uma linha."""
import sys, os
import pandas as pd

OBRIG = ["ano", "turno", "uf", "cd_municipio", "zona", "secao", "aptos", "comparecimento", "lula", "oponente", "brancos", "nulos"]
KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]


def main(pq, entrada, saida):
    e = pd.read_csv(entrada, sep=";")
    falt = [c for c in OBRIG if c not in e.columns]
    if falt:
        raise SystemExit(f"ERRO: colunas obrigatorias ausentes na entrada: {falt}")
    linhas = []
    for (ano, turno), g in e.groupby(["ano", "turno"]):
        p = os.path.join(pq, f"bu_{ano}_t{turno}.parquet")
        if not os.path.exists(p):
            raise SystemExit(f"ERRO: falta {p}")
        b = pd.read_parquet(p)
        for _, r in g.iterrows():
            m = b[(b.SG_UF == r.uf) & (b.CD_MUNICIPIO == r.cd_municipio) & (b.NR_ZONA == r.zona) & (b.NR_SECAO == r.secao)]
            if len(m) != 1:
                linhas.append(dict(ano=ano, turno=turno, uf=r.uf, zona=r.zona, secao=r.secao, campo="SECAO", impresso="", bweb="", diverge=True,
                                   obs=f"{len(m)} linhas no BWeb para a chave (esperado 1)"))
                continue
            m = m.iloc[0]
            comp = [("aptos", r.aptos, m.QT_APTOS), ("comparecimento", r.comparecimento, m.QT_COMPARECIMENTO), ("lula", r.lula, m.lula),
                    ("oponente", r.oponente, m["dir"]), ("brancos", r.brancos, m.branco), ("nulos", r.nulos, m.nulo)]
            if "abertura" in e.columns and pd.notna(r.get("abertura")):
                comp.append(("abertura", str(r.abertura), str(m.DT_ABERTURA)))
            if "encerramento" in e.columns and pd.notna(r.get("encerramento")):
                comp.append(("encerramento", str(r.encerramento), str(m.DT_ENCERRAMENTO)))
            for campo, imp, bw in comp:
                linhas.append(dict(ano=ano, turno=turno, uf=r.uf, zona=r.zona, secao=r.secao, campo=campo, impresso=imp, bweb=bw, diverge=str(imp) != str(bw), obs=""))
    out = pd.DataFrame(linhas)
    if saida:
        out.to_csv(saida, index=False)
    dv = out[out.diverge]
    print(f"{out[['ano','turno','uf','zona','secao']].drop_duplicates().shape[0]} boletins, {len(out)} campos comparados, {len(dv)} divergencias")
    if len(dv):
        print(dv.to_string(index=False))
    sys.exit(1 if len(dv) else 0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
