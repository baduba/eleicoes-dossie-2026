"""Estilo comum dos graficos G1 a G4: paleta validada (Okabe-Ito: azul e vermelhao, CVD ok), fundo claro explicito, textos em cor de texto, linhas finas, sem eixo truncado."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AZUL, VERM, CINZA = "#0072B2", "#D55E00", "#595959"      # pro-Lula, pro-Flavio, sem direcao / nao verificavel
AMBAR = "#9A6700"                                          # parcial (texto escuro sobre fundo claro)
TXT, SUAVE, FUNDO, GRADE = "#1c1c1e", "#5a5f66", "#fcfcfb", "#d9dce1"
MARGEM = 4_430_191
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": SUAVE, "axes.labelcolor": TXT, "text.color": TXT, "xtick.color": SUAVE, "ytick.color": SUAVE,
                     "axes.facecolor": FUNDO, "figure.facecolor": FUNDO, "savefig.facecolor": FUNDO, "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6, "axes.spines.top": False,
                     "axes.spines.right": False, "svg.fonttype": "none", "hatch.linewidth": 1.0})


MOVEL = len(__import__("sys").argv) > 2 and __import__("sys").argv[2] == "m"


EN = os.environ.get("GRAF_LANG", "pt") == "en"      # GRAF_LANG=en: mesma figura, textos em ingles, saida em docs/img/en/ (tradutor: traducao_en.py)


def salva(fig, raiz, nome, titulo, descricao):
    nome = nome + ("_m" if MOVEL else "")
    d = os.path.join(raiz, "docs", "img", "en" if EN else ""); os.makedirs(d, exist_ok=True)
    if EN:
        from traducao_en import traduz_figura, META
        traduz_figura(fig)
        titulo, descricao = META.get(nome.removesuffix("_m"), (titulo, descricao))
    fig.savefig(os.path.join(d, nome + ".png"), dpi=170, bbox_inches="tight", metadata={"Title": titulo, "Description": descricao})
    fig.savefig(os.path.join(d, nome + ".svg"), bbox_inches="tight", metadata={"Title": titulo, "Description": descricao, "Date": None})
    plt.close(fig)


def milhar(x, _=None):
    return f"{x:,.0f}".replace(",", ".")
