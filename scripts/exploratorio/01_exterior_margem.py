#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro): voto no exterior (ZZ) no 2o turno de 2026, por diferenca de totais versionados.

Ideia: o total oficial do BWeb (H9, soma das secoes apuradas, inclui ZZ) menos o total das secoes
apuradas do Brasil (A27, SG_UF != ZZ) isola o exterior. Nenhum dado novo e baixado; a leitura usa
apenas arquivos ja versionados em results/. Sem veredito formal (o projeto pre-registra antes de concluir).
Uso: venv/bin/python scripts/exploratorio/01_exterior_margem.py results/exploratorio
"""
import os
import sys

import pandas as pd

MARGEM = 4_430_191


def main(saida):
    os.makedirs(saida, exist_ok=True)
    tot = pd.read_csv("results/fase1/H9_h9_totais_2026_T2.csv")
    tot = tot[tot.fonte.str.startswith("BWeb")].iloc[0]
    a27 = pd.read_csv("results/fase3/A27_perfil.csv")
    br = a27[a27.grupo.str.startswith("todas")].iloc[0]
    a10 = pd.read_csv("results/fase2/A10_a10_exterior.csv")
    ext = a10[(a10.ano == 2026) & (a10.turno == 2) & a10.recorte.str.startswith("exterior")].iloc[0]

    lula_ext = int(tot.lula - br.votos_lula)
    opo_ext = int(tot.flavio - br.votos_oponente)
    valid2_ext = lula_ext + opo_ext
    linha = dict(
        fonte_lula_total=tot.fonte, lula_total=int(tot.lula), flavio_total=int(tot.flavio),
        lula_brasil_a27=int(br.votos_lula), flavio_brasil_a27=int(br.votos_oponente),
        lula_exterior=lula_ext, oponente_exterior=opo_ext, validos_dois_candidatos_exterior=valid2_ext,
        lula_sh_exterior_pct=round(100 * lula_ext / valid2_ext, 3),
        saldo_lula_exterior=lula_ext - opo_ext,
        saldo_pct_da_margem=round(100 * (lula_ext - opo_ext) / MARGEM, 3),
        validos_ext_pct_da_margem=round(100 * valid2_ext / MARGEM, 3),
        secoes_exterior_a10=int(ext.secoes), comparecimento_ext_pct_a10=float(ext.comparecimento),
        lula_sh_ext_a10_pct=float(ext.pt_pct_dos_dois),
        nota="EXPLORATORIO. Exterior isolado por diferenca de totais versionados (H9 menos A27). "
             "validos = soma dos dois finalistas; brancos e nulos do exterior nao constam em nenhum dos dois arquivos.",
    )
    pd.DataFrame([linha]).to_csv(os.path.join(saida, "exterior_2026_t2_por_diferenca.csv"), index=False)
    for k, v in linha.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
