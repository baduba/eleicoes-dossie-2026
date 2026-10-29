"""Testes de consistencia sobre uma amostra pequena (AP, 2022 e 2026) e funcoes puras."""
import os
import numpy as np
import pandas as pd
import pytest
from lib_auditoria import KEY, fe_ols, Registro, base, votos_max, MARGEM

FX = os.path.join(os.path.dirname(__file__), "fixtures")


def carrega(a, t):
    d = pd.read_csv(os.path.join(FX, f"bweb_ap_{a}_t{t}.csv"))
    return d


def test_totais_e_consistencia_interna():
    for a in (2022, 2026):
        for t in (1, 2):
            d = carrega(a, t)
            x = d[d.DS_TIPO_URNA.str.upper() == "APURADA"]
            assert (x.nominal + x.branco + x.nulo == x.QT_COMPARECIMENTO).all()
            assert (x.QT_COMPARECIMENTO <= x.QT_APTOS).all()
            assert (x.valid2 <= x.QT_COMPARECIMENTO).all()


def test_fe_ols_recupera_coeficiente_conhecido():
    rng = np.random.default_rng(0)
    g = np.repeat(np.arange(300), 4)
    x = rng.normal(size=len(g))
    y = 2.0 * x + rng.normal(size=300)[g] + rng.normal(scale=.1, size=len(g))
    df = pd.DataFrame({"y": y, "x": x, "g": g})
    r = fe_ols(df, "y", ["x"], "g")
    assert abs(r.loc["x", "coef"] - 2.0) < 0.05 and r.loc["x", "se"] < 0.05


def test_fe_ols_com_amostra_real():
    d = carrega(2026, 2)
    x = base(d)
    r = fe_ols(x, "lula_sh", ["turnout"], "uf_local")
    assert np.isfinite(r.loc["turnout", "coef"])


def test_registro_interseccao_uniao_e_votos():
    reg = Registro()
    reg.add("T", "x", 0.10, 0.01, [("a", 0.0, 0.01), ("b", 0.09, 0.01)], expo=1e6, fator=2.0)
    reg.add("T", "y", 0.0, 0.01, [("a", 0.0, 0.01)], expo=1e6, fator=2.0)
    df = reg.frame()
    # excesso so sobre 'a' nao basta: o placebo exigente 'b' e quase igual
    assert df.p_excesso.iloc[0] > 0.1
    assert df.p_excesso.iloc[1] > 0.4
    assert votos_max(0.0, 0.0, 1e6) == 0.0
    assert MARGEM == 4_430_191


def test_holm_nao_diminui_p():
    reg = Registro()
    for i, p in enumerate([0.001, 0.02, 0.5]):
        reg.add_raw("T", f"t{i}", 1.0, 0.1, p)
    df = reg.frame()
    assert (df.p_holm >= df.p_excesso - 1e-12).all()
