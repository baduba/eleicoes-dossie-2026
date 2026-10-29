"""A31: funcoes puras do teste de transferencia T1 -> T2 (Holm, escala robusta, moedas independentes, modelo ajustado em dados sinteticos)."""
import importlib.util
import os
import numpy as np
import pandas as pd

spec = importlib.util.spec_from_file_location("a31", os.path.join(os.path.dirname(__file__), "..", "scripts", "35_a31_transferencia_municipal.py"))
a31 = importlib.util.module_from_spec(spec); spec.loader.exec_module(a31)


def test_holm_monotono_e_limitado():
    p = np.array([0.001, 0.04, 0.03, 0.5])
    h = a31.holm(p)
    assert np.all(h >= p) and np.all(h <= 1)
    assert abs(h[0] - 0.004) < 1e-12            # menor p x numero de testes
    assert h[1] >= h[2]                         # Holm preserva a ordem


def test_holm_com_m_maior_que_n():
    h = a31.holm(np.array([1e-5]), m=5570)
    assert abs(h[0] - 0.0557) < 1e-9


def test_escala_robusta_de_normal_padrao():
    z = np.random.default_rng(1).normal(size=20000)
    assert abs(a31.robust_scale(z) - 1) < 0.05


def test_modelo_nulo_nao_acusa_dados_sem_efeito():
    """Dados sinteticos de Bernoulli com heterogeneidade: o modelo calibrado nao deve rejeitar quase ninguem (Holm)."""
    rng = np.random.default_rng(7)
    n = 3000
    P = rng.integers(30, 3000, size=n)
    p_true = np.clip(rng.normal(0.6, 0.1, size=n), 0.05, 0.95)
    dL = rng.binomial(P, p_true)
    m = pd.DataFrame(dict(SG_UF=rng.choice(["AA", "BB", "CC"], size=n), P=P, dL=dL, f=dL / P))
    X = pd.DataFrame(index=m.index)
    X["x"] = rng.normal(size=n)
    e, cal = a31.ajusta(m, X)
    assert abs(cal["escala_robusta_z"] - 1) < 1e-6
    p = 2 * (1 - __import__("scipy.stats", fromlist=["norm"]).norm.cdf(np.abs(e.z)))
    assert (a31.holm(p) < 0.05).sum() <= 3


def test_moedas_rejeitam_resultado_com_heterogeneidade():
    rng = np.random.default_rng(3)
    n = 500
    P = rng.integers(200, 2000, size=n)
    p_true = np.clip(rng.normal(0.5, 0.15, size=n), 0.05, 0.95)
    m = pd.DataFrame(dict(ano=2026, SG_UF="AA", PT1=100, OP1=100, P=P, dL=rng.binomial(P, p_true)))
    nac, mun = a31.moedas(m)
    assert mun.pct_rejeitados_holm.max() > 30    # heterogeneidade real faz as moedas rejeitarem muitos municipios
