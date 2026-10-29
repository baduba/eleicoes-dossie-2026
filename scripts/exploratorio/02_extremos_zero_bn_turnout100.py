#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro): dentro das 106 secoes com zero voto no oponente (A12b),
quantas tem tambem (i) zero brancos e nulos E secao grande, (ii) comparecimento = 100% dos aptos.

A12b ja calculou a tripla-zero contra o esperado da vizinhanca; isto aqui olha o que A12b nao cortou:
o tamanho das secoes com zero BN e o comparecimento exato de 100%. Cobre so o subconjunto zero-oponente;
"zero BN em secao grande" no universo geral exige o parquet por secao (ausente nesta maquina) e fica
registrado como bloqueio. Sem veredito formal.
Uso: venv/bin/python scripts/exploratorio/02_extremos_zero_bn_turnout100.py results/exploratorio
"""
import os
import sys

import pandas as pd

MARGEM = 4_430_191


def main(saida):
    os.makedirs(saida, exist_ok=True)
    d = pd.read_csv("results/fase3/A12b_106_secoes.csv")
    d["turnout100"] = d.QT_COMPARECIMENTO >= d.QT_APTOS
    resumo = []
    for corte in (1, 30, 100, 200):
        g = d[d.QT_COMPARECIMENTO >= corte]
        resumo.append(dict(
            corte_comparecimento=corte, secoes=len(g),
            com_zero_bn=int(g.zero_bn.sum()),
            com_turnout_100pct=int(g.turnout100.sum()),
            zero_bn_e_turnout100=int((g.zero_bn & g.turnout100).sum()),
            soma_lula=int(g.lula.sum()),
            oponente_esperado_vizinhanca=round(float(g.oponente_esperado_pela_vizinhanca.sum()), 1),
            mediana_aptos=float(g.QT_APTOS.median()) if len(g) else None,
            maior_comparecimento=int(g.QT_COMPARECIMENTO.max()) if len(g) else None,
        ))
    r = pd.DataFrame(resumo)
    r["teto_troca_votos_margem"] = (2 * r.oponente_esperado_vizinhanca).round(0)
    r["teto_pct_margem"] = (100 * r.teto_troca_votos_margem / MARGEM).round(3)
    r.to_csv(os.path.join(saida, "zero_bn_por_tamanho_nas_106_zero_oponente.csv"), index=False)
    print(r.to_string(index=False))
    # as secoes grandes com zero BN (o nucleo da pergunta do candidato 5)
    grandes = d[d.zero_bn & (d.QT_COMPARECIMENTO >= 100)]
    grandes.to_csv(os.path.join(saida, "zero_bn_grandes_dentro_das_106.csv"), index=False)
    print("\nsecoes com zero BN e comparecimento >= 100 dentro das 106:", len(grandes))
    if len(grandes):
        print(grandes[["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "tipo_local", "QT_APTOS", "QT_COMPARECIMENTO", "lula"]].to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
