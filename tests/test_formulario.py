"""A36 canal 2: importa_formulario.py com uma exportacao sintetica (colunas em outra ordem, TESTE, EXIF, divergencia, pendente, descartada)."""
import os
import sys
import pandas as pd
import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import importa_formulario as imp


def foto_com_exif(caminho):
    im = Image.new("RGB", (64, 48), (200, 30, 30))
    ex = Image.Exif(); ex[0x010F] = "CameraDoFulano"; ex[0x0132] = "2026:10:25 17:30:00"
    im.save(caminho, "JPEG", exif=ex.tobytes())
    assert len(Image.open(caminho).getexif()) > 0


@pytest.fixture()
def cenario(tmp_path):
    bw = pd.DataFrame([dict(SG_UF="RR", CD_MUNICIPIO=14060, NR_ZONA=1, NR_SECAO=7, QT_APTOS=300, QT_COMPARECIMENTO=250, lula=120, dir=100, branco=10, nulo=20, DT_ABERTURA="x", DT_ENCERRAMENTO="y"),
                       dict(SG_UF="RR", CD_MUNICIPIO=14060, NR_ZONA=1, NR_SECAO=8, QT_APTOS=310, QT_COMPARECIMENTO=260, lula=130, dir=110, branco=5, nulo=15, DT_ABERTURA="x", DT_ENCERRAMENTO="y")])
    pq = tmp_path / "pq"; pq.mkdir(); bw.to_parquet(pq / "bu_2026_t2.parquet")
    mapa = tmp_path / "mapa.csv"; pd.DataFrame([dict(SG_UF="RR", CD_MUNICIPIO=14060, NM_MUNICIPIO="BOA VISTA")]).to_csv(mapa, index=False)
    ex = tmp_path / "export"; ex.mkdir()
    foto_com_exif(ex / "bu1.jpg"); foto_com_exif(ex / "bu2.jpg"); (ex / "doc.pdf").write_bytes(b"%PDF-1.4 fake")
    cols = ["Foto do boletim", "Observações", "Nº da seção", "Município", "UF", "Zona eleitoral", "Turno", "Quem está enviando?", "Eleitores aptos", "Comparecimento", "Votos Lula", "Votos do oponente", "Brancos", "Nulos", "Submission ID", "Submission Date", "IP"]
    linhas = [
        ["bu1.jpg", "", "7", "Boa Vista", "RR", "1", "2", "mesário", "300", "250", "120", "100", "10", "20", "S1", "2026-10-29", "1.2.3.4"],        # confere
        ["bu2.jpg", "", "8", "boa vista", "RR", "1", "2", "fiscal", "310", "260", "131", "110", "5", "15", "S2", "2026-10-29", "1.2.3.4"],         # lula diverge
        ["bu1.jpg", "TESTE do formulário", "7", "Boa Vista", "RR", "1", "2", "mesário", "300", "250", "120", "100", "10", "20", "S3", "2026-10-29", ""],   # teste
        ["bu1.jpg", "", "7", "Boa Vista", "RR", "1", "2", "eleitor", "", "", "", "", "", "", "S4", "2026-10-29", ""],                              # pendente
        ["bu1.jpg", "", "7", "Cidade Inexistente", "RR", "1", "2", "eleitor", "300", "250", "120", "100", "10", "20", "S5", "2026-10-29", ""],       # descartada
        ["doc.pdf", "", "7", "Boa Vista", "RR", "1", "2", "eleitor", "", "", "", "", "", "", "S6", "2026-10-29", ""],                                # pdf nao publicado
    ]
    csvp = ex / "export.csv"; pd.DataFrame(linhas, columns=cols).to_csv(csvp, index=False)
    return csvp, pq, tmp_path / "saida", ex, mapa


def test_pipeline(cenario):
    csvp, pq, saida, ex, mapa = cenario
    R, comp, S, mp, anexos, nao_usadas = imp.importa(str(csvp), str(pq), str(saida), str(ex), str(mapa))
    assert mp["secao"] == "Nº da seção" and mp["id"] == "Submission ID" and mp["origem_declarada"] == "Quem está enviando?"
    assert anexos == ["Foto do boletim"] and "IP" in nao_usadas
    assert "S3" not in set(R.id_submissao) and int(S.teste_excluidas.iloc[0]) == 1
    st = R.set_index("id_submissao").status
    assert st["S1"] == "conferida sem divergencia"
    assert st["S2"].startswith("DIVERGENCIA em 1")
    assert st["S4"].startswith("recebida, sem transcricao")
    assert st["S5"].startswith("descartada")
    assert (R.canal == "formulario").all()
    assert set(comp[comp.diverge].campo) == {"lula"}


def test_exif_removido_e_original_nao_publicado(cenario):
    csvp, pq, saida, ex, mapa = cenario
    R, *_ = imp.importa(str(csvp), str(pq), str(saida), str(ex), str(mapa))
    fotos = sorted(os.listdir(saida / "fotos"))
    assert fotos and all(f.endswith(".jpg") for f in fotos) and "bu1.jpg" not in fotos and "doc.pdf" not in fotos
    for f in fotos:
        with Image.open(saida / "fotos" / f) as im:
            assert len(im.getexif()) == 0 and not {"exif", "icc_profile", "xmp", "comment"} & set(im.info)
    s6 = R.set_index("id_submissao").loc["S6"]
    assert s6.fotos_publicadas == "" and "formato nao suportado" in s6.campos_divergentes
    saidas = " ".join(open(saida / f, encoding="utf-8").read() for f in ("formulario_resultados.csv", "formulario_comparacao.csv", "formulario_resumo.csv", "mapeamento_colunas.csv"))
    assert "1.2.3.4" not in saidas and "TESTE do formul" not in saidas


def test_mapeamento_por_texto_independe_da_ordem():
    mp, anexos, nao = imp.mapeia(["Zona", "Seção", "Turno", "Foto", "Campo qualquer"])
    assert mp["zona"] == "Zona" and mp["secao"] == "Seção" and mp["turno"] == "Turno" and "Campo qualquer" in nao
