#!/usr/bin/env python3
"""Gera o portal estatico (docs/*.md -> site/*.html) e, opcionalmente, o PDF. Sem rastreadores, sem scripts externos.
Uso: python scripts/build_site.py --saida site [--pdf relatorio.pdf]"""
import argparse, html, os, re, shutil, subprocess, sys
import markdown

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VERSAO = "v0.9.1"
REPO = "https://github.com/baduba/eleicoes-dossie-2026"
AUTORIA = os.environ.get("AUTORIA_TEXTO", "{{AUTORIA}}")      # marcador ate o autor confirmar; ver scripts/15_aplica_autoria.py
NAV = [("index", "Início"), ("metodologia", "Metodologia"), ("preregistro", "Pré-registro"), ("resultados-fase1", "Resultados: Fase 1 (H1 a H10)"),
       ("resultados-fase2", "Resultados: Fase 2 (A1 a A10)"), ("regua-historica", "Régua histórica"), ("alegacoes", "Inventário de alegações"), ("relatorio-original", "O relatório original"),
       ("pontos-cegos", "Pontos cegos"), ("a18-alteracao-no-meio", "A18: alteração no meio"), ("a19-voto-digitado", "A19: voto digitado x registrado"), ("boletins-impressos", "Boletins impressos"), ("base-legal", "Base legal e histórico"), ("dados-reproducao", "Dados e reprodução"), ("residuos", "Questões em aberto"),
       ("changelog", "Changelog e correções"), ("referencias", "Referências")]
CSS = """
:root{--bg:#fff;--fg:#1c1c1e;--mut:#5a5f66;--bd:#d9dce1;--ac:#1d4e89;--cd:#f5f6f8}
@media(prefers-color-scheme:dark){:root{--bg:#15171a;--fg:#e6e8eb;--mut:#a0a6ae;--bd:#32363c;--ac:#7fb0ea;--cd:#1d2024}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{border-bottom:1px solid var(--bd);padding:.8rem 16px;position:sticky;top:0;background:var(--bg);z-index:5}
header b{font-size:1.05rem}nav{display:flex;flex-wrap:wrap;gap:.3rem .9rem;margin-top:.4rem;font-size:.88rem}nav a{color:var(--mut);text-decoration:none}nav a.on,nav a:hover{color:var(--ac)}
main{max-width:980px;margin:0 auto;padding:1rem 16px 4rem;overflow-wrap:anywhere}h1{font-size:1.7rem;line-height:1.25}h2{margin-top:2rem;border-bottom:1px solid var(--bd);padding-bottom:.2rem}h3{margin-top:1.6rem}
a{color:var(--ac)}table{border-collapse:collapse;width:100%;font-size:.85rem;display:block;overflow-x:auto}th,td{border:1px solid var(--bd);padding:.3rem .5rem;vertical-align:top}th{background:var(--cd);text-align:left}
code,pre{background:var(--cd);border-radius:4px;font-size:.88em}code{padding:.1em .3em}pre{padding:.7rem;overflow-x:auto}img{max-width:100%;height:auto}
footer{border-top:1px solid var(--bd);color:var(--mut);font-size:.82rem;padding:1rem 16px;text-align:center}
.aviso{border-left:4px solid var(--ac);background:var(--cd);padding:.6rem .9rem;margin:1rem 0}
"""


def commit():
    try:
        return subprocess.check_output(["git", "-C", RAIZ, "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return os.environ.get("GITHUB_SHA", "dev")[:7] or "dev"


def md(texto):
    h = markdown.markdown(texto, extensions=["tables", "fenced_code", "toc", "attr_list"], output_format="html5")
    return re.sub(r'href="([A-Za-z0-9_\-]+)\.md(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', h)


def fonte(nome):
    cand = [os.path.join(RAIZ, "docs", nome + ".md")]
    esp = {"preregistro": "00_preregistro.md", "resultados-fase1": "dossie.md", "changelog": "CHANGELOG.md"}
    if nome in esp:
        cand.insert(0, os.path.join(RAIZ, esp[nome]))
    for c in cand:
        if os.path.exists(c):
            return open(c, encoding="utf-8").read()
    return None


def pagina(nome, titulo, corpo, c):
    nav = " ".join(f'<a href="{n}.html"{" class=on" if n == nome else ""}>{html.escape(t)}</a>' for n, t in NAV)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)} | Auditoria independente reproduzível</title><meta name="description" content="Auditoria independente reproduzível do 2º turno presidencial de 2026"><style>{CSS}</style></head>
<body><header><b>Auditoria independente reproduzível: 2º turno presidencial de 2026</b><nav>{nav}</nav></header>
<main>{corpo}</main><footer>Versão {VERSAO} · commit {c} · <a href="{REPO}">{REPO}</a> · Auditoria independente: não é laudo, perícia oficial nem documento homologado.</footer></body></html>"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--saida", default="site"); ap.add_argument("--pdf", default=None)
    a = ap.parse_args()
    out = os.path.join(RAIZ, a.saida)
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    c = commit(); paginas = []
    for nome, titulo in NAV:
        t = fonte(nome)
        if t is None:
            print(f"AVISO: sem fonte para a pagina {nome}", file=sys.stderr); continue
        corpo = md(t)
        paginas.append((nome, titulo, corpo))
        open(os.path.join(out, nome + ".html"), "w", encoding="utf-8").write(pagina(nome, titulo, corpo, c))
    for pasta in ("figs",):
        for orig in (os.path.join(RAIZ, "docs", pasta), os.path.join(RAIZ, "results", pasta)):
            if os.path.isdir(orig):
                shutil.copytree(orig, os.path.join(out, pasta), dirs_exist_ok=True)
    for extra in glob_pdf():
        shutil.copy(extra, out)
    if a.pdf:
        gera_pdf(paginas, os.path.join(RAIZ, a.pdf), c)
    print(f"portal em {out} ({len(paginas)} paginas, commit {c})")


def glob_pdf():
    d = os.path.join(RAIZ, "relatorio")
    return [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".pdf")] if os.path.isdir(d) else []


def resumo_capa():
    """Impacto agregado para a capa: so testes sem ressalva de desenho (numeros do CSV do H10)."""
    import pandas as pd
    h = pd.read_csv(os.path.join(RAIZ, "results", "fase2", "H10_h10_agregado.csv"))
    h = h[h.criterio != "como registrado"].set_index("sentido")
    f = lambda x: f"{x:,.0f}".replace(",", ".")
    return (f"Impacto agregado (somente testes sem ressalva de desenho; unidade: votos de margem; tetos de pior caso, não estimativas): {f(h.loc['PT', 'soma_votos_sobreviventes_pior_caso'])} votos de margem pró-Lula e {f(h.loc['OPO', 'soma_votos_sobreviventes_pior_caso'])} pró-Flávio, contra uma margem de 4.430.191 votos de margem. "
            "As análises A1, A2, A3 e A12 têm ressalva de desenho: o mesmo teste acusa excesso em séries ou anos sem manipulação; resultado original e corrigido estão lado a lado nos Resultados da Fase 2.")


def gera_pdf(paginas, saida, c):
    from weasyprint import HTML
    css = f"""@page{{size:A4;margin:22mm 16mm 20mm 16mm;@bottom-left{{content:"Auditoria independente reproduzível {VERSAO} · commit {c} · {REPO}";font-size:7.5pt;color:#555}}@bottom-right{{content:"p. " counter(page);font-size:8pt;color:#555}}}}
body{{font:10pt/1.45 serif;color:#111}}h1{{font-size:17pt;page-break-before:always}}h2{{font-size:13pt}}h3{{font-size:11pt}}table{{border-collapse:collapse;font-size:7.5pt;width:100%;table-layout:auto}}th,td{{border:.5pt solid #999;padding:1.5pt 3pt;vertical-align:top}}th{{background:#eee}}
code{{font-size:8pt;word-break:break-all}}pre{{font-size:7.5pt;white-space:pre-wrap}}img{{max-width:100%}}.capa{{text-align:center;margin-top:60mm}}.capa h1{{page-break-before:avoid;font-size:24pt}}a{{color:#111;text-decoration:none}}"""
    capa = (f'<div class="capa"><h1>Auditoria independente reproduzível</h1><h2>2º turno presidencial de 2026 (Lula x Flávio Bolsonaro)</h2>'
            f'<p>Versão {VERSAO} · commit {c}</p><p>{REPO}</p><p><b>Autoria e contato:</b> {html.escape(AUTORIA)}</p>'
            f'<p style="margin-top:12mm;font-size:9.5pt">{resumo_capa()}</p>'
            f'<p style="margin-top:20mm;font-size:9pt">Esta é uma auditoria independente. Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou.</p></div>')
    sumario = "<h1>Sumário</h1><ol>" + "".join(f"<li>{html.escape(t)}</li>" for _, t, _ in paginas) + "</ol>"
    corpo = "".join(f'<section>{cb}</section>' for _, _, cb in paginas)
    HTML(string=f"<html lang='pt-BR'><head><meta charset='utf-8'><title>Auditoria independente reproduzível: 2º turno presidencial de 2026</title><style>{css}</style></head><body>{capa}{sumario}{corpo}</body></html>", base_url=os.path.join(RAIZ, "docs")).write_pdf(saida)
    print("pdf:", saida)


if __name__ == "__main__":
    main()
