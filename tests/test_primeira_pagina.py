"""A29/A30: regras da primeira pagina (palavras proibidas, ressalva do teto na mesma linha, resultado antes das perguntas) e tabelas de poder."""
import math
import os
import re
import sys
import pytest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
pp = pytest.importorskip("primeira_pagina")
if not os.path.exists(os.path.join(RAIZ, "results", "graficos", "itens_em_aberto.csv")):
    pytest.skip("rode scripts/graficos/00_dados.py", allow_module_level=True)

PROIBIDAS = ["probabilidade de fraude", "provável", "provavel", "suspeit", "fraude"]


def pagina(readme):
    return pp.resultado(RAIZ) + pp.perguntas(RAIZ, readme) + pp.contribuir(RAIZ, readme)


@pytest.mark.parametrize("readme", [False, True])
def test_palavras_proibidas_e_travessao(readme):
    t = pagina(readme).lower()
    for p in PROIBIDAS:
        assert p not in t, p
    assert "—" not in t and "–" not in t


def test_todo_cartao_com_teto_traz_a_ressalva_na_mesma_linha():
    for linha in pagina(False).splitlines():
        if linha.startswith("> Teto:") and "votos de margem" in linha:
            assert "teto de pior caso, não estimativa" in linha, linha


def test_fraude_escopada_a_eras():
    """A palavra 'fraude' e permitida apenas na hipotese do teto (eras); nas demais secoes geradas, proibida."""
    assert "fraude" in pp.eras(RAIZ).lower()
    outros = (pp.hero(RAIZ) + pp.padroes(RAIZ) + pp.fluxo(RAIZ) + pp.resultado(RAIZ)
              + pp.perguntas(RAIZ) + pp.contribuir(RAIZ) + pp.resumo_perguntas(RAIZ))
    assert "fraude" not in outros.lower()
    assert "—" not in pp.eras(RAIZ) and "–" not in pp.eras(RAIZ)


def test_resultado_vem_antes_das_perguntas():
    t = pagina(False)
    assert t.index("Resultado verificado") < t.index("Perguntas em aberto")
    assert "nenhum teste deste dossiê a veria" in t
    assert "Não são evidência de nada, nem de um lado nem do outro" in t


def test_blocos_e_ordem_por_teto():
    import pandas as pd
    D, _ = pp.carrega(RAIZ)
    assert set(D.bloco) == {"a", "b", "c"}
    a = D[D.bloco == "a"].teto_pior_caso.dropna().tolist()
    assert a == sorted(a, reverse=True)


def test_inversao_de_margem_em_seções():
    # cada troca muda a margem em 2: 5, 50 e 200 trocas por seção
    f = lambda k: math.ceil(math.ceil((4_430_191 + 1) / 2) / k)
    assert (f(5), f(50), f(200)) == (443_020, 44_302, 11_076)
