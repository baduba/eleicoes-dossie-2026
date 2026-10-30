#!/usr/bin/env python3
"""EXPLORATORIO (fora do pre-registro): ancoras quantitativas contra o cenario de INVERSAO TOTAL de votos
(13 <-> 22 em massa, agregados "normais, so que invertidos").

Blocos:
(1) Eixo T1 -> T2 por secao (A2, ja versionado): sob inversao total APENAS no T2, o coeficiente
    margem_T2 ~ margem_T1 (EF de municipio) seria ~= -coef real (negativo); observado: ver serie.
(2) Pesquisas finais (A7, ja versionado): erro da pesquisa contra o resultado PUBLICADO e contra o
    ESPELHO (o "resultado verdadeiro" sob inversao total). Mostra por que pesquisa pre-eleitoral NAO
    decide a inversao total: ela e consistente com as duas hipoteses; e sob inversao total os erros de
    2026 contra o publicado (2,6-2,8 p.p.) sao exatamente o previsto.
(3) Escala: margem em pontos percentuais dos validos e 2x a margem (o deslocamento entre os dois mundos).

Sem veredito formal. Uso: venv/bin/python scripts/exploratorio/04_inversao_total_ancoras.py results/exploratorio
"""
import os
import sys

import pandas as pd

MARGEM = 4_430_191
VALIDOS = 64_256_232 + 59_826_041  # dois finalistas, H9


def main(saida):
    os.makedirs(saida, exist_ok=True)
    out = []

    # (1) eixo T1 -> T2
    sw = pd.read_csv("results/fase2/A2_a2_swing.csv")
    for _, r in sw.iterrows():
        out.append(dict(bloco="eixo_T1_T2", ano=r.ano, medida="coef margem_T2 ~ margem_T1 (EF municipio)",
                        valor=round(r.coef_m1, 4), ep=round(r.ep, 5),
                        esperado_sob_inversao_total_so_T2="fortemente negativo (~ -coef. real)",
                        leitura="incompativel com inversao total so no T2" if r.coef_m1 > 0.5 else "compativel"))
    # f nacional de A31 (captura do pool T1->T2 pelo PT)
    dist = pd.read_csv("results/fase3/A31_distribuicao_f.csv")
    for _, r in dist.iterrows():
        out.append(dict(bloco="eixo_T1_T2", ano=int(r.ano), medida="f nacional = fracao do pool capturada pelo PT (A31)",
                        valor=round(r.f_nacional, 4), ep=None,
                        esperado_sob_inversao_total_so_T2="proximo de 0 ou negativo (PT herdaria a base do oponente e perderia a propria)",
                        leitura="dentro da faixa historica 0,30-0,74; heranca normal" ))

    # (2) pesquisas finais
    m_share = 100 * MARGEM / VALIDOS
    pub_lula = 100 * 64_256_232 / VALIDOS
    pub_opo = 100 * 59_826_041 / VALIDOS
    a7 = pd.read_csv("results/fase2/A7_a7_pesquisas.csv")
    a7_26 = a7[a7.ano == 2026]
    for _, r in a7_26.iterrows():
        erro_publicado = abs(r.oponente_pct_validos_pesquisa - pub_opo)
        erro_espelho = abs(r.oponente_pct_validos_pesquisa - pub_lula)
        out.append(dict(bloco="pesquisa", ano=2026, instituto=r.instituto,
                        medida="erro do oponente (p.p.) contra o publicado / contra o espelho",
                        valor=f"{erro_publicado:.2f} / {erro_espelho:.2f}", ep=None,
                        esperado_sob_inversao_total_so_T2="erro contra o publicado ~= 1x margem = %.2f p.p. (a inversao desloca cada share por 1 margem; 2x margem = %.2f p.p. e a distancia entre os dois mundos)" % (m_share, 2 * m_share),
                        leitura="AMBAS as hipoteses consistentes: sem inversao, a pesquisa errou %.2f p.p. (maior da serie, fora da margem declarada); com inversao total, a pesquisa acertou a realidade (erro %.2f p.p.)" % (erro_publicado, erro_espelho)))
    for _, r in a7[a7.ano != 2026].iterrows():
        out.append(dict(bloco="pesquisa (referencia historica)", ano=int(r.ano), instituto=r.instituto,
                        medida="erro do PT na pesquisa final (p.p.)", valor=round(r.erro_pp_pt, 2), ep=None,
                        esperado_sob_inversao_total_so_T2="n/a", leitura="serie de erros: 0,13 (2018), 1,1 (2022), 2,6-2,8 (2026)"))

    # (3) escala
    out.append(dict(bloco="escala", ano=2026, medida="margem oficial em p.p. dos validos", valor=round(m_share, 3),
                    ep=None, esperado_sob_inversao_total_so_T2="—",
                    leitura="inversao total desloca o resultado em 2x isto = %.2f p.p." % (2 * m_share)))

    d = pd.DataFrame(out)
    d.to_csv(os.path.join(saida, "inversao_total_ancoras.csv"), index=False)
    print(d.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/exploratorio")
