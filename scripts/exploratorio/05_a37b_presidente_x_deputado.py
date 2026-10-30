#!/usr/bin/env python3
"""A37b (PRE-REGISTRADO em docs/propostas/gatilhos-e-inversao.md; PENDENTE DE INSUMO nesta maquina):
alinhamento presidente x deputado federal do mesmo partido/federacao, por secao.

Tese testada: inversao total de votos SOMENTE na presidencia faria a correlacao secao-a-secao entre
share do candidato a presidente e share dos deputados do seu partido DESMORONAR em 2026 contra
2014/2018/2022 (os votos de deputado nao seriam invertidos). Sob H0 (sem inversao), a correlacao de
2026 fica dentro do envelope dos placebos.

PENDENTE DE INSUMO: precisa dos parquets por cargo (parquet2/cargos_*), ausentes nesta maquina.
O script aceita o diretorio como argumento e falha com NaoExecutado explicito se nao houver.
Uso: venv/bin/python scripts/exploratorio/05_a37b_presidente_x_deputado.py DIR_PARQUET2 results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib_auditoria import KEY, NaoExecutado

# partido do presidente por ano (PT e oponente do T2): numero do partido no voto proporcional
PARTIDO = {2026: ("PT/Federacao (13)", "PL (22)"), 2022: ("PT/Federacao (13)", "PL (22)"),
           2018: ("PT (13)", "PSL (17)"), 2014: ("PT (13)", "PSDB (45)")}
FED_PT_2022_2026 = {13, 12, 40}  # PT, PCdoB, PV (federacao BRASIL DA ESPERANCA)


def carrega_cargos(pq2, ano, turno):
    p = os.path.join(pq2, f"cargos_{ano}_t{turno}.parquet")
    if not os.path.exists(p):
        raise NaoExecutado(f"falta {p} (parquets por cargo ausentes nesta maquina)")
    return pd.read_parquet(p)


def main(pq2, saida):
    os.makedirs(saida, exist_ok=True)
    linhas = []
    for ano in (2026, 2022, 2018, 2014):
        t = 2
        d = carrega_cargos(pq2, ano, t)  # esperado: KEY + CD_CARGO_PERGUNTA + NR_PARTIDO + QT_VOTOS (+validos do cargo)
        pres = d[d.CD_CARGO_PERGUNTA == 1].groupby(KEY)["QT_VOTOS"].sum()  # ajustar ao schema real de cargos_*
        dep = d[d.CD_CARGO_PERGUNTA == 6]
        raise NaoExecutado("schema de cargos_* a confirmar na maquina com os parquets; ajustar mapeamento cargo/partido e rodar")
    pd.DataFrame(linhas).to_csv(os.path.join(saida, "a37b_presidente_x_deputado.csv"), index=False)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
