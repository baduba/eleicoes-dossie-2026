"""Leitor de arquivos de urna: BU e RDV reais de uma secao de RR (2o turno de 2026, dados publicos agregados, sem dado pessoal)."""
import os
import urna_parse as U

FX = os.path.join(os.path.dirname(__file__), "fixtures")


def test_bu_decodifica_votos():
    bu = U.bu_campos(open(os.path.join(FX, "rr_secao_bu.dat"), "rb").read())
    c1 = bu["cargos"][1]
    assert sum(q for t, q, pn in c1 if t == 1 and pn and pn[1] == 13) == 42
    assert sum(q for t, q, pn in c1 if t == 1 and pn and pn[1] == 22) == 166
    assert sum(q for t, q, pn in c1 if t == 2) == 1
    assert sum(q for t, q, pn in c1 if t == 3) == 3
    assert sum(q for t, q, pn in c1) == 212


def test_rdv_recontagem_igual_ao_bu():
    rd = U.rdv_cargos(open(os.path.join(FX, "rr_secao_rdv.dat"), "rb").read())[1]
    assert sum(rd.values()) == 212
    assert sum(v for (e, n), v in rd.items() if n == "13") == 42
    assert sum(v for (e, n), v in rd.items() if n == "22") == 166
    assert sum(v for (e, n), v in rd.items() if e == 3 and n == "") == 1
