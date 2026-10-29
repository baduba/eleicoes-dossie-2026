#!/usr/bin/env python3
"""A32 (Adendo 11), item 5: confere ata da mesa receptora e folha de votacao com o BU (BWeb) e com as habilitacoes do log da urna, secao por secao, e reporta QUALQUER divergencia.
Uso: python -I 37_confere_ata.py DIR_PARQUET entrada.csv [MEDIDAS_LOG.parquet] [saida.csv]

entrada.csv (separador ';'), colunas obrigatorias:
  ano;turno;uf;cd_municipio;zona;secao;votantes_ata;assinaturas_folha
colunas opcionais: manuais_anotados_folha (eleitores com anotacao de habilitacao manual na folha), comparecimento_bu_impresso
Testes por secao: assinaturas da folha = votantes da ata = comparecimento do BU (BWeb) = habilitacoes do log; manuais anotados na folha = habilitacoes manuais do log.
Nenhum dado pessoal e lido: so contagens por secao. MEDIDAS_LOG.parquet e a saida de 41_a32_rajadas.py (A32_medidas_secao_dia.parquet), opcional."""
import os
import sys
import pandas as pd

KEY = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
OBRIG = ["ano", "turno", "uf", "cd_municipio", "zona", "secao", "votantes_ata", "assinaturas_folha"]


def main(pq, entrada, log=None, saida="A32_confere_ata.csv"):
    e = pd.read_csv(entrada, sep=";")
    falt = [c for c in OBRIG if c not in e.columns]
    if falt:
        raise SystemExit(f"ERRO: colunas obrigatorias ausentes: {falt}")
    m = pd.read_parquet(log) if log and os.path.exists(log) else None
    linhas = []
    for (ano, turno), g in e.groupby(["ano", "turno"]):
        b = pd.read_parquet(os.path.join(pq, f"bu_{ano}_t{turno}.parquet"), columns=KEY + ["QT_COMPARECIMENTO", "QT_APTOS"])
        for r in g.itertuples():
            x = b[(b.SG_UF == r.uf) & (b.CD_MUNICIPIO == r.cd_municipio) & (b.NR_ZONA == r.zona) & (b.NR_SECAO == r.secao)]
            if len(x) != 1:
                linhas.append(dict(ano=ano, turno=turno, uf=r.uf, zona=r.zona, secao=r.secao, campo="SECAO", ata_ou_folha="", outro="", diverge=True, obs=f"{len(x)} linhas no BWeb para a chave (esperado 1)")); continue
            comp = int(x.iloc[0].QT_COMPARECIMENTO)
            pares = [("assinaturas_folha x votantes_ata", r.assinaturas_folha, r.votantes_ata), ("votantes_ata x comparecimento BU (BWeb)", r.votantes_ata, comp), ("assinaturas_folha x comparecimento BU (BWeb)", r.assinaturas_folha, comp)]
            if hasattr(r, "comparecimento_bu_impresso") and pd.notna(r.comparecimento_bu_impresso):
                pares.append(("BU impresso x BWeb", r.comparecimento_bu_impresso, comp))
            if m is not None:
                l = m[(m.SG_UF == r.uf) & (m.CD_MUNICIPIO == r.cd_municipio) & (m.NR_ZONA == r.zona) & (m.NR_SECAO == r.secao) & (m.ano == ano) & (m.turno == turno)]
                if len(l) == 1:
                    l = l.iloc[0]
                    pares.append(("assinaturas_folha x habilitacoes do log", r.assinaturas_folha, int(l.n_hab)))
                    if hasattr(r, "manuais_anotados_folha") and pd.notna(r.manuais_anotados_folha):
                        pares.append(("manuais anotados na folha x manuais do log", r.manuais_anotados_folha, int(l.n_m)))
                else:
                    linhas.append(dict(ano=ano, turno=turno, uf=r.uf, zona=r.zona, secao=r.secao, campo="LOG", ata_ou_folha="", outro="", diverge=False, obs="secao sem log lido (NAO CONFERIDO)"))
            for nome, v1, v2 in pares:
                linhas.append(dict(ano=ano, turno=turno, uf=r.uf, zona=r.zona, secao=r.secao, campo=nome, ata_ou_folha=v1, outro=v2, diverge=int(v1) != int(v2), obs=""))
    out = pd.DataFrame(linhas); out.to_csv(saida, index=False)
    print(f"{len(e)} secoes, {int(out.diverge.sum())} divergencias em {len(out)} comparacoes; saida: {saida}")
    print(out[out.diverge].to_string(index=False) if out.diverge.any() else "nenhuma divergencia")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], a[2] if len(a) > 2 else None, a[3] if len(a) > 3 else "A32_confere_ata.csv")
