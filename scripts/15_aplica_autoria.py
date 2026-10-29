#!/usr/bin/env python3
"""Substitui o marcador {{AUTORIA}} (README.md, LICENSE, docs/*.md) pelo bloco de autoria escolhido. Rodar so depois que o autor confirmar.
Uso: python -I 15_aplica_autoria.py a "Nome Completo" "contato pessoal"   (opcao a: autor nominal)
     python -I 15_aplica_autoria.py b                                       (opcao b: projeto sem autor nominal, contato por issues)
Para o PDF: AUTORIA_TEXTO="<mesmo texto>" python scripts/build_site.py --saida site --pdf relatorio/auditoria-independente-v0.9.3.pdf"""
import glob
import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = "https://github.com/baduba/eleicoes-dossie-2026"


def bloco(op, nome=None, contato=None):
    if op == "a":
        return f"{nome}. Contato: {contato}. Correções e contestações também por *issue* em {REPO}/issues."
    return f"Projeto sem autoria nominal, mantido pela conta baduba no GitHub. Contato, correções e contestações por *issue* em {REPO}/issues."


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("a", "b") or (sys.argv[1] == "a" and len(sys.argv) != 4):
        raise SystemExit(__doc__)
    txt = bloco(*sys.argv[1:])
    alvos = [os.path.join(RAIZ, "README.md"), os.path.join(RAIZ, "LICENSE")] + glob.glob(os.path.join(RAIZ, "docs", "*.md"))
    for p in alvos:
        s = open(p, encoding="utf-8").read()
        if "{{AUTORIA}}" in s:
            open(p, "w", encoding="utf-8").write(s.replace("{{AUTORIA}}", txt)); print("atualizado:", os.path.relpath(p, RAIZ))
    print("texto usado:", txt)


if __name__ == "__main__":
    main()
