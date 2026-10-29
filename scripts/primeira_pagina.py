"""Blocos da primeira pagina (A29) e da secao de lacunas (A30), gerados dos CSVs. Usado por 03e_paginas_finais.py (portal e README) e portado ao PDF pelo portal.
Regras: nada de 'probabilidade de fraude', 'provavel', 'suspeito', adjetivos ou nomes de pessoas; todo teto vem com 'teto de pior caso, nao estimativa' na mesma linha;
a secao de perguntas em aberto nunca aparece sem o bloco 'Resultado verificado' antes."""
import os
import pandas as pd

MARGEM = 4_430_191
SITE = "https://baduba.github.io/eleicoes-dossie-2026/"


def n(x, d=0):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def imagem(base, ext, alt, readme):
    """README: imagem simples do desktop. Portal: <picture> com versao estreita (legivel a 380 px)."""
    if readme:
        return f"![{alt}](docs/img/{base}.{ext})\n"
    alt = alt.replace('"', "'")
    return f'<picture><source media="(max-width: 640px)" srcset="img/{base}_m.{ext}"><img src="img/{base}.{ext}" alt="{alt}"></picture>\n'


def link(pagina, readme):
    return (SITE + pagina) if readme else pagina


def carrega(raiz):
    g = os.path.join(raiz, "results", "graficos")
    return pd.read_csv(os.path.join(g, "itens_em_aberto.csv"), keep_default_na=False, na_values=[""]), pd.read_csv(os.path.join(g, "bu_conferidos.csv")).iloc[0]


def resultado(raiz):
    f2 = os.path.join(raiz, "results", "fase2")
    rs = pd.read_csv(os.path.join(f2, "residuos_soma.csv")).iloc[0]
    a5 = pd.read_csv(os.path.join(f2, "A5_a5_estimativa_nacional_votos_apos_nominal.csv")).iloc[0]
    a4 = pd.read_csv(os.path.join(f2, "A4_a4_resumo.csv")); a4 = a4[a4.ano == 2026].iloc[0]
    pl, pf = rs.excesso_medido_pro_Lula_votos_de_margem, rs.excesso_medido_pro_Flavio_votos_de_margem
    L = ["## O que sabemos e o que ainda não sabemos\n", "### Resultado verificado\n",
         f"- **Cadeia RDV, BU, BWeb e total:** 0 divergências nos testes executados ({n(a4.secoes)} seções de {n(a4.UFs)} UFs com arquivos de urna; BWeb contra totalização por seção, município e zona).",
         f"- **Excesso medido somado:** cerca de {n(round(pl, -3) / 1000)} mil pró-Lula e {n(round(pf, -3) / 1000)} mil pró-Flávio (votos de margem), em sentidos opostos, contra a margem de {n(MARGEM)} votos.",
         f"- **Votos depois das 17h:** cerca de {n(round(a5.estimativa_total, -3) / 1000)} mil (contagem de votos, não votos de margem).",
         "- **Limite:** esses testes comparam arquivos que o próprio TSE publica; não excluem uma alteração coerente feita antes da publicação nem verificam se o voto registrado é o digitado (ver as perguntas abaixo).",
         "- **Nenhum teste executado encontrou efeito capaz de alterar o resultado.**\n"]
    return "\n".join(L)


def cartao(r, readme):
    if pd.notna(r.teto_pior_caso):
        med = f"excesso medido: {n(r.excesso_medido)} votos de margem; " if pd.notna(r.excesso_medido) and r.excesso_medido > 0 else ""
        teto = f"{med}**teto de pior caso, não estimativa: {n(r.teto_pior_caso)} votos de margem ({n(r.pct_margem_teto, 2) if r.pct_margem_teto >= 0.01 else 'menos de 0,01'}% da margem)**" + (f" ({r.nota})" if isinstance(r.nota, str) and r.nota else "")
    else:
        base = "sem número ainda (teste não executado)" if r.situacao == "NÃO TESTADO" else ("sem número (teste de forma, não convertível em votos)" if r.situacao == "TESTADO-INCONCLUSIVO" else "não mensurável com dados públicos")
        teto = base + (f" ({r.nota})" if isinstance(r.nota, str) and r.nota else "")
    return (f"> **{r.pergunta}**  \n> Situação: **{r.situacao}** · Direção: {r.direcao}  \n> Teto: {teto}  \n> O que fecharia: {r.fechar}  \n"
            f"> [Página técnica]({link(r.pagina, readme)}) · [Abrir issue]({r.issue.replace(' ', '%20')}%20{r.id})\n")


def perguntas(raiz, readme=False):
    D, _ = carrega(raiz)
    L = ["## Perguntas em aberto: o que os testes não conseguiram explicar nem confirmar\n",
         "**Não são evidências de manipulação. São lacunas. Se você tem dados ou método para fechar alguma, contribua.**\n",
         "Cada cartão traz a pergunta, a situação, a direção do efeito (a favor de quem, se houver), o teto em votos de margem com a ressalva na mesma linha e o que fecharia a questão. Dentro de cada bloco, a ordem é pelo tamanho do que a resposta poderia mudar (maior teto ou maior ponto cego primeiro). Os tetos são limites superiores sob o pior caso; a margem é de 4.430.191 votos de margem.\n"]
    for b, t in (("a", "a) Resíduos sem causa identificada (testes executados, inconclusivos)"), ("b", "b) Hipóteses ainda não testadas (Fase 3, A20 a A28)"), ("c", "c) Pontos cegos estruturais (A18, A19)")):
        L.append(f"### {t}\n")
        for r in D[D.bloco == b].itertuples():
            L.append(cartao(r, readme))
    return "\n".join(L)


def contribuir(raiz, readme=False):
    _, bu = carrega(raiz)
    L = ["## Como contribuir\n",
         f"- **Fotos de boletins impressos:** [página de coleta]({link('boletins-impressos.html', readme)}). Conferidos até {pd.to_datetime(bu.data).strftime('%d/%m/%Y')}: {int(bu.n_conferidos)}.",
         "- **Listas de seções com fiscal** (partidos e coligações): formato em [A23]" + f"({link('fase3.html#a23', readme)}).",
         "- **Respostas de pedidos LAI:** textos prontos em [`lai/`](https://github.com/baduba/eleicoes-dossie-2026/tree/main/lai); envie a resposta por issue.",
         "- **Código ou método alternativo:** abra uma issue ou um PR com um script reproduzível.",
         "- **Contestação de qualquer número:** abra uma issue com o script e o valor esperado.\n"]
    return "\n".join(L)


def lacunas(raiz, readme=False, nao_testado=""):
    p = (lambda x: f"docs/img/{x}") if readme else (lambda x: f"img/{x}")
    mm = open(os.path.join(raiz, "docs", "img", "g1_cadeia.mmd"), encoding="utf-8").read()
    L = ["## Onde uma falha poderia passar despercebida\n",
         "Esta seção mostra, com números, onde a verificação pública termina e de que tamanho uma falha precisaria ser para mudar o resultado. Todo valor em votos está em votos de margem (variação da diferença Lula menos Flávio; trocar um voto muda a margem em 2).\n",
         "### G1. Mapa da cadeia do voto\n"]
    if readme:
        L += ["```mermaid", mm.strip(), "```\n"]
    else:
        L += [imagem("g1_cadeia", "svg", "Mapa da cadeia do voto, de doze etapas, do cadastro à divulgação. Cada etapa tem um status: verificado pelos testes, verificado parcialmente ou não verificável com dados públicos. O elo entre voto digitado e voto registrado está destacado como não verificável, conferido só por amostragem no teste de integridade.", False)]
    L += ["**Em palavras simples:** o voto passa por doze etapas; os testes cobrem as etapas depois do registro; as etapas anteriores e as que ocorrem fora dos arquivos públicos ficam parcialmente verificadas ou não verificadas. **Técnico:** status por etapa a partir de A4, H9, A5, A18, A19, A20, A26; o elo voto digitado → voto registrado só é verificado por amostragem (teste de integridade). Como fechar esta lacuna: [boletins impressos]" + f"({link('boletins-impressos.html', readme)}) e [chave oficial da assinatura]({link('a18-alteracao-no-meio.html#2', readme)}).\n",
          "### G2. Curvas de detecção\n",
          imagem("g2_deteccao", "png", "Curvas da chance de detectar ao menos uma urna ou seção alterada conforme a fração alterada, de 0,1% a 20% em escala logarítmica. O teste de integridade com todas as urnas detecta frações pequenas; usando só as urnas com biometria, é preciso uma fração bem maior. Boletins impressos com 100, 300 e 1.000 conferidos aparecem como outras curvas. Linhas verticais marcam as frações de seções necessárias para mudar a margem com 200 e 50 trocas por seção.", readme),
          "**Em palavras simples:** quanto maior o pedaço alterado, mais fácil é ver; os boletins impressos e o teste de integridade enxergam alterações pequenas que os testes estatísticos não enxergam. **Técnico:** probabilidade hipergeométrica de ver ao menos uma urna alterada; premissas: amostra aleatória; em (b), software que se comporta normalmente no teste sem biometria. Não descreve como um ataque seria feito. Como fechar esta lacuna: [enviar fotos de boletins]" + f"({link('boletins-impressos.html', readme)}), [pedido LAI 03]" + f"({link('fase3.html#a28', readme)}).\n",
          "### G3. Tamanho do impacto dos itens em aberto\n",
          imagem("g3_impacto", "png", "Barras horizontais, em votos de margem, para cada item em aberto que tem número: barra sólida é excesso medido, barra hachurada é teto de pior caso, não estimativa. Uma linha vertical fixa marca a margem de 4.430.191 votos. Dois painéis: escala linear, em que todas as barras são pequenas diante da margem, e escala logarítmica, em que os itens pequenos ficam visíveis. Itens sem número aparecem só na legenda como não mensuráveis.", readme),
          "**Em palavras simples:** cada item em aberto, desenhado ao lado da margem; o maior teto de pior caso é menor que a margem, e vários itens não têm número porque faltam dados. **Técnico:** barra sólida = excesso medido (estimativa central positiva); barra hachurada = teto de pior caso (placebo mais frouxo), em votos de margem; não há soma. Como fechar esta lacuna: [pedidos LAI]" + f"({link('fase3.html#a28', readme)}) e [lista de fiscais]({link('fase3.html#a23', readme)}).\n",
          "### G4. Quantas seções precisariam ser alteradas\n",
          imagem("g4_secoes", "png", "Curva do número de seções necessárias para mudar a margem em função dos votos trocados por seção, de 1 a 300, em escala logarítmica nos dois eixos. Com 5 trocas por seção seriam 443.020 seções; com 50, 44.302; com 200, 11.076. A faixa à direita de 13 trocas por seção marca onde uma seção alterada já apareceria como valor atípico no local; à esquerda, só aparece em conjunto, em boletins impressos ou no teste de integridade.", readme),
          "**Em palavras simples:** quanto menos votos se trocam por seção, mais seções seriam necessárias, e mais difícil é ver uma seção sozinha. **Técnico:** seções = ⌈2.215.096 / trocas⌉; limiar de 13 trocas por seção = 3 desvios padrão do resíduo local (1,67 p.p.) com 256 votos válidos. Como fechar esta lacuna: [boletins impressos]" + f"({link('boletins-impressos.html', readme)}) e [comparação com outros cargos, A22]({link('fase3.html#a22', readme)}).\n",
          "> **Estes gráficos mostram onde a verificação pública termina. Não indicam que houve falha; indicam onde uma falha não seria vista pelos dados disponíveis e o que seria preciso para vê-la.**\n"]
    if nao_testado:
        L += ["### O que não foi testado\n", nao_testado + "\n"]
    return "\n".join(L)
