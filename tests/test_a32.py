"""A32 e A12b: funcoes puras (rajadas, esperado exato por permutacao, sequencias do log, Poisson-binomial)."""
import importlib.util
import os
import numpy as np

AQ = os.path.join(os.path.dirname(__file__), "..", "scripts")


def carrega(nome):
    spec = importlib.util.spec_from_file_location(nome[:2], os.path.join(AQ, nome))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


a32 = carrega("41_a32_rajadas.py")
ext = carrega("38_a32_extrai_logs.py")
a12b = carrega("36_a12b_zero_brancos_nulos.py")


def test_rajada_simples():
    ts = [0, 100, 105, 110, 300, 400, 405, 410, 415]
    tp = list("BMMMBMMMM")
    # p5 = 10: M em 1..3 com intervalos 5 e 5 (rajada de 3); M em 5..8 com intervalos 5, 5, 5 (rajada de 4)
    assert a32.rajadas(ts, tp, 10, 3) == (2, 7)
    assert a32.rajadas(ts, tp, 10, 4) == (1, 4)
    assert a32.rajadas(ts, tp, 2, 3) == (0, 0)             # intervalos nao ficam abaixo do p5


def test_rajada_interrompida_por_biometrica():
    ts = [0, 5, 10, 15, 20]
    assert a32.rajadas(ts, list("MMBMM"), 10, 3) == (0, 0)


def test_esperado_exato_contra_monte_carlo():
    rng = np.random.default_rng(5)
    n, m = 200, 30
    ts = np.cumsum(rng.integers(5, 60, size=n)); g = np.diff(ts); p5 = np.percentile(g, 25)
    tp = np.array(["M"] * m + ["B"] * (n - m))
    mc = np.mean([a32.rajadas(ts, list(rng.permutation(tp)), p5, 2)[0] for _ in range(8000)])
    assert abs(a32.esperado_exato(g < p5, n, m, 2) - mc) < 0.05 * max(mc, 1)


def test_sequencias_do_log_classifica_manual_e_biometrica():
    linhas = []
    def l(h, msg):
        return f"04/10/2026 {h}\tINFO\tX\tY\t{msg}"
    linhas += [l("08:00:00", "Tipo de habilitação do eleitor [biométrica]"), l("08:00:01", "Eleitor foi habilitado"),
               l("08:05:00", "Solicitação de dado pessoal do eleitor para habilitação manual"), l("08:05:30", "Mesário 000 habilitou o eleitor"), l("08:05:31", "Eleitor foi habilitado"),
               l("08:09:00", "Eleitor foi habilitado")]
    seq, n = ext.sequencias(linhas, 2026)
    ts, tp = seq[1]
    assert "".join(tp) == "BMO" and ts == [8 * 3600 + 1, 8 * 3600 + 5 * 60 + 31, 8 * 3600 + 9 * 60]
    assert seq[2] == ([], [])


def test_poisson_binomial_cauda():
    assert abs(a12b.pb_cauda(np.array([0.5, 0.5]), 1) - 0.75) < 1e-12
    assert abs(a12b.pb_cauda(np.array([0.5, 0.5]), 2) - 0.25) < 1e-12
    assert abs(a12b.pb_cauda(np.array([0.1] * 10), 0) - 1.0) < 1e-12
