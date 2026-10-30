#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro) — Fechamento de fluxo T1 -> T2, 2002 a 2026.

Pergunta: o ganho bruto de cada finalista entre os turnos fecha com as fontes disponiveis
(eliminados ponderados por campo ideologico, migracao de brancos+nulos, variacao de comparecimento)?

Fontes de votos: parquets locais (2014, 2018, 2022, 2026: cand_t1_* por candidato + bu_*_t* para totais,
B+N e comparecimento; 2014 so tem agregados PT/oponente/terceiros). 2002/2006/2010: NAO ha parquet;
usa dados_locais/eleicoes-presidenciais-1989-2026.md (Wikipedia/TSE) — marcado como fonte secundaria.
O md e VALIDADO contra os parquets para 2014/2018/2022/2026 e as divergencias sao reportadas.

CLASSIFICACAO IDEOLOGICA CONGELADA (fixada aqui, antes de calcular qualquer desvio; 2026 segue os blocos
documentados de A11 em docs/resultados-fase2.md: pro-Flavio = Cury, Caiado, Zema, Clariana; esquerda = UP,
PSTU, PCB, PCO; neutro = Renan Santos, Grassi, Leonardo):
  ESQ/CESQ -> PT com taxa tE; CEN -> 50/50; DIR/CDIR -> OPO com taxa tD (PT fica com 1-tD = cross-over).
Faixas de sensibilidade (largas, fixadas aqui): tESQ in [0.80, 0.95]; tCESQ in [0.55, 0.80];
centro para o PT in [0.40, 0.60]; cross-over do PT sobre o pool de direita in [0.05, 0.15];
B+N migrado para o PT in [0.40, 0.60]; novos comparecentes (dComp) para o PT = share do PT no T2 +- 5 p.p.

Reconciliacao com A31: f_nacional = dPT/(dPT+dOPO) deve reproduzir o 0,7367 versionado (identidade de A3/A31).
Uso: venv/bin/python scripts/exploratorio/10_fechamento_fluxo.py results/exploratorio
"""
import os
import sys

import numpy as np
import pandas as pd

SAIDA = "results/exploratorio"

# ---- tabela congelada por ano: (PT_t1, OPO_t1, pool_esq, pool_cesq, pool_cen, pool_dir, BN_t1, comp_t1) ----
# 2002/2006/2010: do md do dono (fonte secundaria, sem parquet). 2014+: validado contra parquet abaixo.
MD = {
    2002: dict(pt=39_455_233, opo=19_705_445, esq=402_236 + 38_619, cesq=15_180_097 + 10_170_882, cen=0, dir=0,
               pt2=52_793_364, opo2=33_370_739, bn1=None, comp1=None, fonte="md (Wikipedia/TSE), sem parquet"),
    2006: dict(pt=46_662_365, opo=39_968_369, esq=6_575_393, cesq=2_538_844, cen=126_404 + 63_294 + 62_064, dir=0,
               pt2=58_295_042, opo2=37_543_178, bn1=None, comp1=None, fonte="md (Wikipedia/TSE), sem parquet"),
    2010: dict(pt=47_651_434, opo=33_132_283, esq=886_816 + 84_609 + 39_136 + 12_206, cesq=19_636_359,
               cen=57_960, dir=89_350, pt2=55_752_529, opo2=43_711_388, bn1=None, comp1=None,
               fonte="md (Wikipedia/TSE), sem parquet"),
    2014: dict(pt=43_267_668, opo=34_897_211, esq=1_612_186 + 91_209 + 47_845 + 12_324, cesq=22_176_619 + 630_099,
               cen=446_878, dir=780_513 + 61_250, pt2=54_501_118, opo2=51_041_155, bn1=4_420_488 + 6_678_580,
               comp1=None, fonte="md validado contra parquet (agregados)"),
    2018: dict(pt=31_342_005, opo=49_276_990, esq=617_122 + 55_762, cesq=13_344_366 + 1_069_577, cen=1_288_948 + 30_176,
               dir=5_096_349 + 2_679_744 + 1_348_323 + 859_601 + 41_710, pt2=47_040_906, opo2=57_797_847,
               bn1=3_106_936 + 7_206_205, comp1=None, fonte="parquet cand_t1/bu"),
    2022: dict(pt=57_259_504, opo=51_072_345, esq=53_519 + 45_620 + 25_625, cesq=3_599_287, cen=4_915_423,
               dir=600_955 + 559_708 + 81_129 + 16_604, pt2=60_345_999, opo2=58_206_354, bn1=1_964_779 + 3_487_874,
               comp1=None, fonte="parquet cand_t1/bu"),
    2026: dict(pt=53_879_538, opo=56_104_503, esq=122_911 + 43_103 + 22_693 + 15_024, cesq=0, cen=2_675_887 + 16_881 + 5_246,
               dir=3_448_569 + 2_605_148 + 326_488 + 40_043, pt2=64_256_232, opo2=59_826_041, bn1=2_300_798 + 3_669_003,
               comp1=None, fonte="parquet cand_t1/bu (blocos de A11)"),
}

T_E, T_CE, CEN_PT, CROSS_D, BN_PT = (0.80, 0.95), (0.55, 0.80), (0.40, 0.60), (0.05, 0.15), (0.40, 0.60)


def totais_parquet(ano):
    """Totais nacionais (com exterior) por turno: PT, oponente, brancos+nulos, comparecimento."""
    r = {}
    for t in (1, 2):
        d = pd.read_parquet(f"parquet/bu_{ano}_t{t}.parquet")
        d = d[d.DS_TIPO_URNA.str.upper().eq("APURADA")]
        r[t] = dict(pt=int(d.lula.sum()), opo=int(d["dir"].sum()), bn=int((d.branco + d.nulo).sum()),
                    comp=int(d.QT_COMPARECIMENTO.sum()))
    return r


def main(saida=SAIDA):
    os.makedirs(saida, exist_ok=True)
    val = []
    for ano in (2014, 2018, 2022, 2026):
        tp = totais_parquet(ano)
        m = MD[ano]
        val.append(dict(ano=ano, pt_t1_md=m["pt"], pt_t1_parquet=tp[1]["pt"], dif_pt_t1=tp[1]["pt"] - m["pt"],
                        opo_t1_md=m["opo"], opo_t1_parquet=tp[1]["opo"], dif_opo_t1=tp[1]["opo"] - m["opo"],
                        pt_t2_md=m["pt2"], pt_t2_parquet=tp[2]["pt"], dif_pt_t2=tp[2]["pt"] - m["pt2"],
                        opo_t2_md=m["opo2"], opo_t2_parquet=tp[2]["opo"], dif_opo_t2=tp[2]["opo"] - m["opo2"],
                        bn_t1_md=m["bn1"], bn_t1_parquet=tp[1]["bn"],
                        bn_t2_parquet=tp[2]["bn"], comp_t1=tp[1]["comp"], comp_t2=tp[2]["comp"]))
    v = pd.DataFrame(val)
    v.to_csv(os.path.join(saida, "FLX_validacao_md_vs_parquet.csv"), index=False)
    print("== validacao md x parquet ==\n", v.to_string(index=False))

    linhas = []
    for ano in (2002, 2006, 2010, 2014, 2018, 2022, 2026):
        m = MD[ano]
        if ano >= 2014:
            tp = totais_parquet(ano)
            bn1, bn2, comp1, comp2 = tp[1]["bn"], tp[2]["bn"], tp[1]["comp"], tp[2]["comp"]
            pt_t1, opo_t1, pt_t2, opo_t2 = tp[1]["pt"], tp[1]["opo"], tp[2]["pt"], tp[2]["opo"]
            fonte = "parquet"
        else:
            pt_t1, opo_t1, pt_t2, opo_t2 = m["pt"], m["opo"], m["pt2"], m["opo2"]
            bn1 = bn2 = comp1 = comp2 = None
            fonte = m["fonte"]
        dPT, dOPO = pt_t2 - pt_t1, opo_t2 - opo_t1
        pool = dPT + dOPO  # identidade A3/A31: = terceiros + dComp + BN1 - BN2
        f_nac = dPT / pool
        # fechamento esperado para o PT (banda larga)
        sh_pt_t2 = pt_t2 / (pt_t2 + opo_t2)
        if bn1 is not None:
            dbn = bn1 - bn2
            dcomp = comp2 - comp1
            lo = (T_E[0] * m["esq"] + T_CE[0] * m["cesq"] + CEN_PT[0] * m["cen"] + CROSS_D[0] * m["dir"]
                  + BN_PT[0] * dbn + (sh_pt_t2 - 0.05) * dcomp)
            hi = (T_E[1] * m["esq"] + T_CE[1] * m["cesq"] + CEN_PT[1] * m["cen"] + CROSS_D[1] * m["dir"]
                  + BN_PT[1] * dbn + (sh_pt_t2 + 0.05) * dcomp)
            mid = (lo + hi) / 2
        else:
            dbn = dcomp = None
            # sem BN/comparecimento por turno: esperado so dos pools de eliminados (faixa), resto reportado a parte
            lo = T_E[0] * m["esq"] + T_CE[0] * m["cesq"] + CEN_PT[0] * m["cen"] + CROSS_D[0] * m["dir"]
            hi = T_E[1] * m["esq"] + T_CE[1] * m["cesq"] + CEN_PT[1] * m["cen"] + CROSS_D[1] * m["dir"]
            mid = (lo + hi) / 2
        desv = dPT - mid
        margem = abs(pt_t2 - opo_t2)
        linhas.append(dict(ano=ano, fonte=fonte, dPT=dPT, dOPO=dOPO, pool_total=pool, f_nacional_PT=round(f_nac, 4),
                           pool_esq=m["esq"], pool_cesq=m["cesq"], pool_cen=m["cen"], pool_dir=m["dir"],
                           dBN=dbn, dComp=dcomp,
                           esperado_PT_lo=round(lo), esperado_PT_mid=round(mid), esperado_PT_hi=round(hi),
                           desvio_PT_votos=round(desv), desvio_min=round(dPT - hi), desvio_max=round(dPT - lo),
                           desvio_pct_margem=round(100 * desv / margem, 1),
                           dentro_da_faixa=bool(lo <= dPT <= hi)))
    r = pd.DataFrame(linhas)
    r.to_csv(os.path.join(saida, "FLX_fechamento_por_ano.csv"), index=False)
    print("\n== fechamento por ano ==\n", r.to_string(index=False))

    # reconciliacao com A31 (f versionado por ano)
    a31 = pd.read_csv("results/fase3/A31_distribuicao_f.csv")
    rec = a31[["ano", "f_nacional"]].merge(r[["ano", "f_nacional_PT"]], on="ano", how="outer")
    rec["dif"] = (rec.f_nacional_PT - rec.f_nacional).round(4)
    rec.to_csv(os.path.join(saida, "FLX_reconciliacao_A31.csv"), index=False)
    print("\n== reconciliacao com A31 (f nacional) ==\n", rec.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SAIDA)
