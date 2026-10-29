"""A34 e A35: extrator de duracoes (log sintetico) e cauda de Poisson-binomial por DFT contra a convolucao exata."""
import importlib.util
import os
import numpy as np

AQUI = os.path.join(os.path.dirname(__file__), "..", "scripts")


def carrega(nome, arq):
    import sys
    sys.path.insert(0, AQUI)
    spec = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, arq)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


a34 = carrega("a34x", "45_a34_extrai_duracoes.py")
a35 = carrega("a35x", "46_a35_extremos_universo.py")


def linha(hora, msg, dia="25/10/2026"):
    return f"{dia} {hora}\tINFO\t00000001\tSCUE\t{msg}\tAAAA"


def test_duracoes_pareia_habilitacao_com_o_proximo_voto():
    L = [linha("09:00:00", "Eleitor foi habilitado"), linha("09:00:09", "Voto confirmado para [Presidente]"),
         linha("09:01:00", "Eleitor foi habilitado"), linha("09:01:20", "Voto confirmado para [Presidente]"),
         linha("09:02:00", "Eleitor foi habilitado"), linha("09:02:30", "Eleitor foi habilitado"), linha("09:02:40", "Voto confirmado para [Presidente]")]
    o = a34.duracoes(L, 2026)[2]
    assert o["dur"] == [9, 20, 10] and o["n_hab"] == 4 and o["n_conf"] == 3 and o["n_sem_voto"] == 1
    assert o["gap"] == [51, 40] and o["n_neg"] == 0          # lado errado: voto confirmado ate a proxima habilitacao


def test_duracoes_separa_os_dias_e_ignora_outras_datas():
    L = [linha("09:00:00", "Eleitor foi habilitado", "04/10/2026"), linha("09:00:15", "Voto confirmado para [Presidente]", "04/10/2026"),
         linha("09:00:00", "Eleitor foi habilitado", "01/01/2000"), linha("09:00:05", "Voto confirmado para [Presidente]", "01/01/2000")]
    o = a34.duracoes(L, 2026)
    assert o[1]["dur"] == [15] and o[2]["dur"] == [] and o[2]["n_hab"] == 0


def test_poisson_binomial_dft_bate_com_a_convolucao_exata():
    rng = np.random.default_rng(3)
    p = rng.uniform(0.001, 0.3, 400)
    dist = np.zeros(len(p) + 1); dist[0] = 1.0
    for q in p:
        dist[1:] = dist[1:] * (1 - q) + dist[:-1] * q; dist[0] *= (1 - q)
    for k in (0, 20, int(p.sum()), int(p.sum()) + 15, 90):
        assert abs(a35.pb_cauda(p, k) - dist[k:].sum()) < 5e-3
