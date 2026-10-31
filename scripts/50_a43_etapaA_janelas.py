#!/usr/bin/env python3
"""A43, Etapa A (Adendo 18): votos por janela de 15 minutos e carimbos de primeiro/ultimo voto,
numa UF pequena, com medicao de escala (previa do A42, Adendo 21).

Regra de horario: votacao das 08:00 as 17:00, horario de Brasilia, em todo o pais (fonte: TRE-PE,
noticia de setembro/2026 — acesso automatizado negado, HTTP 403, 31/10/2026; recusa salva em
fontes/tre-pe/; confirmacao do texto oficial pendente com o autor — toda saida leva o rotulo
"regra de horario nao confirmada em fonte"). O log traz o relogio LOCAL da urna (descoberta do
Adendo 18); RR = Brasilia -1: soma-se 1h para normalizar.

Reuso obrigatorio: parser scripts/urna_parse.py e agrupador scripts/08_arquivos_urna.py (os mesmos de
A21/A32/A34). Nenhum identificador de eleitor ou mesario e lido; o carimbo marca o evento
"Voto confirmado para [Presidente]", nunca o conteudo do voto (proibicao do Adendo 21).

Saidas (results/fase5/): A43A_{UF}_{ano}_t2_janelas.csv (uma linha por secao com 36+ janelas e metricas),
A43A_{UF}_{ano}_t2_cobertura.csv, A43A_medicao_escala.csv.
Uso: ./venv/bin/python scripts/50_a43_etapaA_janelas.py ZIP UF ANO
"""
import importlib.util
import os
import sys
import time
import zipfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import urna_parse as U

spec = importlib.util.spec_from_file_location("au08", os.path.join(AQUI, "08_arquivos_urna.py"))
au = importlib.util.module_from_spec(spec); spec.loader.exec_module(au)

DIAS = {2026: {1: "04/10/2026", 2: "25/10/2026"}, 2022: {1: "02/10/2022", 2: "30/10/2022"}}
M_CONF = "Voto confirmado para [Presidente]"
FUSO = {"AC": 2, "AM": 1, "MS": 1, "MT": 1, "RO": 1, "RR": 1}   # horas a somar no relogio local -> Brasilia
JANELA, N_JANELAS = 900, 36                                     # 15 min, 08:00 as 17:00 de Brasilia

OUT = "results/fase5"
os.makedirs(OUT, exist_ok=True)


def janelas_secao(linhas, dia, desloc):
    """Retorna (contagens por janela, primeiro, ultimo, apos17, n_conf) com tempo normalizado p/ Brasilia."""
    cont = np.zeros(N_JANELAS + 3, dtype=int)   # 0..35 dentro do dia legal; 36 = antes das 08:00; 37+ = apos 17:00 (fila)
    ts = []
    for l in linhas:
        p = l.split("\t")
        if len(p) < 5 or p[4] != M_CONF or p[0][:10] != dia:
            continue
        s = int(p[0][11:13]) * 3600 + int(p[0][14:16]) * 60 + int(p[0][17:19]) + desloc * 3600
        ts.append(s)
        j = (s - 8 * 3600) // JANELA
        j = min(max(int(j), -1), N_JANELAS + 1)
        cont[j + 1] += 1                         # j=-1 -> indice 0 (antes das 08:00)
    if not ts:
        return cont, None, None, 0, 0
    apos = int(sum(1 for s in ts if s >= 17 * 3600))
    return cont, min(ts), max(ts), apos, len(ts)


def main():
    zp, uf, ano = sys.argv[1], sys.argv[2], int(sys.argv[3])
    dia = DIAS[ano][2]
    desloc = FUSO.get(uf, 0)
    t_ini = time.time()
    z = zipfile.ZipFile(zp)
    grupos = au.agrupa(z.namelist(), ano)
    log_mb = sum(i.file_size for i in z.infolist()
                 if i.filename.endswith("logjez") or i.filename.endswith("log.jez")) / 1e6

    linhas_out, cob = [], []
    for key, f in grupos.items():
        base = dict(uf=uf, cd_municipio=key[1], zona=key[2], secao=key[3], ano=ano, turno=2)
        if "log" not in f:
            cob.append({**base, "situacao": "sem log"}); continue
        try:
            cont, p0, p1, apos, n = janelas_secao(U.ler_log(z.read(f["log"])), dia, desloc)
            if n == 0:
                cob.append({**base, "situacao": "log sem voto confirmado no dia"}); continue
            linhas_out.append({**base, "primeiro_voto_bsb": p0, "ultimo_voto_bsb": p1,
                               "votos_apos_17h": apos, "n_votos_log": n,
                               **{f"j{k:02d}": int(cont[k + 1]) for k in range(-1, N_JANELAS + 1)}})
            cob.append({**base, "situacao": "ok"})
        except Exception as e:                                # noqa: BLE001
            cob.append({**base, "situacao": f"erro: {type(e).__name__}: {e}"})
    dt = time.time() - t_ini

    D = pd.DataFrame(linhas_out)
    C = pd.DataFrame(cob)
    stem = f"A43A_{uf}_{ano}_t2"
    D.to_csv(os.path.join(OUT, f"{stem}_janelas.csv"), index=False)
    C.to_csv(os.path.join(OUT, f"{stem}_cobertura.csv"), index=False)

    zip_mb = os.path.getsize(zp) / 1e6
    med = dict(uf=uf, ano=ano, turno=2, zip_mb=round(zip_mb, 1), logs_extraidos_mb=round(log_mb, 1),
               secoes=len(grupos), secoes_ok=int((C.situacao == "ok").sum()),
               tempo_s=round(dt, 1), s_por_secao=round(dt / max(len(grupos), 1), 3),
               mb_log_por_secao=round(log_mb / max(len(grupos), 1), 3))
    mpath = os.path.join(OUT, "A43A_medicao_escala.csv")
    pd.DataFrame([med]).to_csv(mpath, mode="a", header=not os.path.exists(mpath), index=False)

    print("== medicao ==")
    print(med)
    print("== cobertura ==")
    print(C.situacao.value_counts().to_string())
    if len(D):
        h = lambda s: f"{int(s // 3600):02d}:{int((s % 3600) // 60):02d}"
        print("\n== primeiro voto (Brasilia): quantis ==")
        print(D.primeiro_voto_bsb.quantile([0, 0.01, 0.5, 0.99, 1]).map(h).to_string())
        print("== ultimo voto (Brasilia): quantis ==")
        print(D.ultimo_voto_bsb.quantile([0, 0.01, 0.5, 0.99, 1]).map(h).to_string())
        print(f"\nvotos apos 17h (exato, log): {int(D.votos_apos_17h.sum())} de {int(D.n_votos_log.sum())} "
              f"({100 * D.votos_apos_17h.sum() / D.n_votos_log.sum():.2f}%)")
        print(f"secoes com voto apos 17h: {int((D.votos_apos_17h > 0).sum())} de {len(D)}")
        print(f"secoes com primeiro voto antes das 08:00 (Brasilia): {int((D.primeiro_voto_bsb < 8 * 3600).sum())}")
        tot = D[[f"j{k:02d}" for k in range(N_JANELAS)]].sum()
        print("\nvotos por janela (top 8):")
        print(tot.sort_values(ascending=False).head(8).to_string())
        print(f"\njanelas fora do dia legal: antes 08:00 = {int(D['j-1'].sum())}, apos 17h = {int(D['j37'].sum()) + int(D['j38'].sum())}")


if __name__ == "__main__":
    main()
