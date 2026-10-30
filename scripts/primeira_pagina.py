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
         "- **Limite:** esses testes comparam arquivos que o próprio TSE publica; não excluem uma alteração coerente feita antes da publicação nem verificam se o voto registrado é o digitado (ver as perguntas abaixo).\n",
         '<p class="destaque">Se uma alteração acontecesse nos elos que não são publicados (o voto digitado, o boletim impresso, a transmissão), <strong>nenhum teste deste dossiê a veria</strong>. É por isso que as perguntas abaixo continuam abertas.</p>\n']
    return "\n".join(L)


def hero(raiz, readme=False):
    """Medidor de verificacao da primeira pagina: cobertura da cadeia (numeros do mapa G1) e resultado agregado.
    Metrica honesta: cobertura de verificacao, nao 'chance de fraude'."""
    img = f"![Barra dos 12 elos da cadeia do voto: 4 verificados, 5 parciais, 3 não verificáveis; 100% dos votos atravessam ao menos um elo não verificável](docs/img/g0_verificacao.png)\n" if readme else \
        imagem("g0_verificacao", "png",
               "Barra empilhada dos 12 elos da cadeia do voto: 4 verificados (33%), 5 parcialmente verificados (42%) e 3 não verificáveis com dados públicos (25%). "
               "Abaixo, uma segunda barra indica que 100% dos votos atravessam pelo menos um elo não verificável.", False)
    L = ["## O quanto da cadeia do voto a verificação pública cobre\n",
         img,
         "- **33% da cadeia do voto totalmente verificada com dados públicos** (4 de 12 elos; [mapa completo, G1](#g1-mapa-da-cadeia-do-voto)).",
         "- **25% não verificáveis** (3 de 12: voto digitado → registrado, boletim impresso conferido, transmissão).",
         "- **100% dos votos atravessam pelo menos um elo não verificável.**",
         "- **0 testes encontraram efeito capaz de alterar o resultado**; o maior teto de pior caso, não estimativa, é 40,35% da margem ([A20b]" + f"({link('fase3.html#a20b', readme)})).\n",
         "Isto não é evidência de nada, nem de um lado nem do outro: é o mapa de onde uma alteração passaria invisível aos dados públicos.\n",
         f"**[Envie a foto do seu boletim]({link('boletins-impressos.html', readme)})**: pelo formulário de envio no GitHub.\n"]
    return "\n".join(L)


def padroes(raiz, readme=False):
    """Os dois gatilhos mais obvios, checados primeiro: empates e margens de 1 voto; Nordeste (sem biometria x troca de urna).
    Numeros da analise com os parquets por secao (out/2026); memorando em docs/propostas/gatilhos-e-inversao.md."""
    memo = "https://github.com/baduba/eleicoes-dossie-2026/blob/main/docs/propostas/gatilhos-e-inversao.md"
    perg = "https://github.com/baduba/eleicoes-dossie-2026/blob/main/docs/perguntas-em-aberto.md" if readme else "perguntas-em-aberto.html"
    L = ["## Os dois gatilhos mais óbvios, checados primeiro\n",
         "Estes dois padrões pareciam o lugar óbvio onde uma alteração passaria barato; por isso foram testados primeiro, com os dados por seção.\n",
         '<div class="duo">',
         "<div>",
         "<h3>Empates e margens de 1 voto</h3>",
         "<ul>",
         "<li><strong>2.150 seções com empate exato</strong> entre Lula e Flávio em 2026, com <strong>517.768 votos válidos</strong>; <strong>4.517 seções decididas por exatamente 1 voto</strong>, com <strong>1.087.289 votos</strong>.</li>",
         "<li>Contra o nulo binomial por seção: empates observados 2.150 contra 2.337 esperados (razão 0,92); margens de 1 voto: 4.517 contra 4.672 (0,97). Em todas as faixas de margem de 0 a 10, 2026 fica <strong>abaixo do nulo</strong>, como 2022. O crescimento dos empates (+5,1%) é o do próprio número de seções (+5,7%).</li>",
         "<li>Simetria das margens de 1 voto: 2.268 a favor de Lula e 2.249 a favor de Flávio (p = 0,789). Urna trocada nessas seções: na taxa nacional ou abaixo.</li>",
         "<li><strong>Leitura:</strong> 2.150 urnas empatadas e 4.517 decididas por 1 voto concentram 1,6 milhão de votos onde <strong>nenhum dos dois lados pode construir vantagem</strong>. Se a estratégia fosse amarrar o placar urna a urna, o campo de atuação seria exatamente este. Os números não mostram sobra estatística (0,92 do esperado) nem direção (2.268 a 2.249; p = 0,789); e é justamente a ausência de sobra que exige explicação, porque urna pequena empatada não deixa rastro em teste de agregado. <strong>O que fecha: o boletim impresso dessas urnas, um a um.</strong></li>",
         "</ul>",
         "</div>",
         "<div>",
         "<h3>Nordeste: habilitação sem biometria e troca de urna</h3>",
         "<ul>",
         "<li>Correlação município a município (1.794 municípios, por taxa): Spearman ρ = 0,06, substancialmente zero; \"as capitais têm os dois\" é efeito de tamanho.</li>",
         "<li>Seções com Lula ≥ 80% e (troca de urna ou município no top-10% de habilitação sem biometria): <strong>3.469 seções</strong> em 2026, saldo de 537.354 votos de margem, teto de 24,3% da margem; em 2022 o mesmo padrão era <strong>maior</strong> (3.766 seções, saldo 602.222, teto de 27,2%): é estrutural, não específico de 2026.</li>",
         "<li>Oponente entre 0 e 10 votos: 3.029 seções em 2026 (saldo 376.149; 65% no Nordeste), contra 4.097 em 2022 (saldo 505.308; 73% no NE): o conjunto encolheu 26%.</li>",
         "<li><strong>Leitura:</strong> o conjunto encolheu 26% desde 2022 e o padrão é maior em 2022. Pode ser estrutura; pode ser exatamente o que uma técnica em redução planejada deixaria. Com os dados internos não há como diferenciar uma coisa da outra; por isso estas seções seguem no topo da fila de verificação: <strong>as 190 com troca de urna e alta habilitação sem biometria pedem folha de votação e ata (pedido LAI 07 já protocolado)</strong>.</li>",
         "</ul>",
         "</div>",
         "</div>\n",
         "<h3>A hipótese que não dá para derrubar sozinha</h3>",
         "<p>Uma operação sofisticada reduziria as técnicas visíveis e introduziria outras, de propósito, de modo que cada teste isolado encontrasse \"estrutura\" ou \"declínio\". Com dados internos, essa hipótese não pode ser confirmada nem refutada: qualquer padrão observado é compatível com ela. O que a mantém em pé como pergunta, e o que a decidiria, são as âncoras externas: boletins impressos, teste de integridade, série histórica de pesquisas. <strong>Este cenário o dossiê não pode ver; só a verificação física pode.</strong></p>\n",
         f'<p class="destaque">Padrão refutado não fecha a pergunta; padrão estrutural, menos ainda. Quem quiser contestar os números tem os scripts e os dados aqui. Estes dois eram os gatilhos mais óbvios; os que restam abertos estão nas <a href="{perg}">Perguntas em aberto</a>.</p>\n',
         f"Detalhamento e contas: [memorando exploratório]({memo}).\n"]
    return "\n".join(L)


def eras(raiz, readme=False):
    """Narrativa em duas eras (1989-2010 x 2014-2026) e a hipotese do teto de ~10 milhoes de votos.
    A hipotese e apresentada rotulada como hipotese; numeros fixos conferidos na serie historica."""
    L = ["## Duas eras eleitorais\n",
         '<div class="duo">',
         "<div>",
         "<h3>Como se ganhava um 2º turno antes de 2014</h3>",
         "<ul>",
         "<li>De 1989 a 2010, nenhuma eleição direta foi decidida por menos de 6 pontos; a margem média foi de <strong>15,6 p.p.</strong> (1989: 6,06; 2002: 22,54; 2006: 21,66; 2010: 12,10).</li>",
         "<li>A aritmética era de herança: o vencedor herdava os eliminados que o endossavam, mais o comparecimento novo. 2002: Lula ganhou +13,3 milhões com o pool de Ciro e Garotinho. 2006: +11,6 milhões com Heloísa Helena e Cristovam, enquanto Alckmin perdeu votos.</li>",
         "<li>Margens grandes demais para qualquer ajuste pequeno mudar o resultado; e parte do processo ainda tinha rastro físico.</li>",
         "</ul>",
         "</div>",
         "<div>",
         "<h3>Desde 2014, o cenário mudou em três pontos</h3>",
         "<ul>",
         "<li><strong>Eleição apertada virou a norma.</strong> As quatro menores margens da história são 2022 (1,80 p.p.), 2014 (3,28) e 2026 (3,58), com 2018 (10,26) ainda abaixo da média antiga; média 2014-2026: <strong>4,7 p.p.</strong></li>",
         "<li><strong>O canal físico de verificação foi extinto no mesmo período.</strong> Registro impresso suspenso em 2013 e declarado inconstitucional em 2018: as quatro eleições mais apertadas da história ocorreram sem nenhuma via de recontagem independente.</li>",
         "<li><strong>2026 é o primeiro vira-vira da série.</strong> Pela primeira vez desde 1989, quem liderou o 1º turno perdeu o 2º.</li>",
         "</ul>",
         "</div>",
         "</div>\n",
         "<h3>A hipótese da fraude (o teto de cerca de 10 milhões de votos)</h3>",
         "<p>A leitura que organiza toda a série: uma <strong>fraude com teto de cerca de 10 milhões de votos</strong>. Sob ela, 2014 (margem de 3,46 milhões de votos), 2022 (2,14 milhões) e 2026 (4,43 milhões) seriam reversíveis; 2018 não foi (10,76 milhões, acima do teto, com a onda pós-facada e um adversário sem força própria). O teste de fechamento de fluxo deste dossiê mede um desvio sem fonte de +4,8 a +6,7 milhões em 2026, mais o espelho de cerca de 5 milhões do outro lado: a ordem de grandeza bate com o teto.</p>",
         "<p><strong>A hipótese não pode ser confirmada nem refutada com dados internos</strong>: \"o declínio seria a estratégia\" explica qualquer padrão. O que a sustenta em pé como pergunta é que 2018, a eleição fora do alcance do teto, é também a única fora da era apertada. O que a decide: pesquisa de transferência de voto, folha de votação, boletim impresso, teste de integridade.</p>\n",
         "<h3>A curva do declínio</h3>",
         imagem("g5_declinio", "png",
                "Cinco indicadores da série 2014 a 2026, normalizados a índice 2018 igual a 100: seções com 0 a 10 votos no oponente, saldo em seções com PT a 80% ou mais, habilitação sem biometria no Nordeste, empates sobre o nulo e resíduo total medido. Todos caem desde o pico de 2018.", readme),
         "| indicador | 2014 | 2018 | 2022 | 2026 |\n|---|---|---|---|---|\n"
         "| seções com oponente entre 0 e 10 votos | 6.324 | 7.606 | 4.097 | 3.029 (-60% do pico) |\n"
         "| saldo em seções com PT a 80% ou mais (mi) | 6,02 | 6,38 | 5,58 | 4,97 (-22%) |\n"
         "| habilitação sem biometria no Nordeste (%) | sem dado | 9,49 | 9,38 | 7,19 |\n"
         "| empates observados / nulo esperado | 0,90 | 1,03 | 0,95 | 0,92 |\n"
         "| resíduo total medido (mi de votos de margem) | 6,95 | 7,08 | 6,30 | 5,61 (-21%) |\n",
         "**Desde o pico de 2018, tudo que é mensurável caiu.** Há duas leituras para a mesma curva. A benigna: a biometria expandindo, os redutos se urbanizando, a estrutura amadurecendo; com ela, o declínio é progresso. A adversarial: com ela, o declínio é a técnica; cada sinal visível encolhe um pouco a cada ciclo, e um teste de regressão que procura crescimento não enxerga um esquema cujo sucesso é justamente não crescer. **Os dois cenários deixam a mesma curva; dados internos não os separam.**\n",
         "<h3>Como o esquema funcionaria</h3>",
         '<div class="ciclo">',
         "<div><b>1.</b> Uma técnica nova entra em ciclo de teste, com volume pequeno.</div>",
         "<div><b>2.</b> Se funciona, escala até o necessário, dentro do teto de cerca de 10 milhões de votos.</div>",
         "<div><b>3.</b> O escrutínio público cresce ao redor da técnica (auditorias, pedidos de dados, testes estatísticos como os desta página).</div>",
         "<div><b>4.</b> A técnica é reduzida gradualmente a cada eleição, até virar \"estrutura\" invisível nos testes.</div>",
         "<div><b>5.</b> Uma técnica nova já entrou no lugar, e o ciclo recomeça.</div>",
         "</div>\n",
         "Nenhum teste de agregado enxerga o ciclo completo: cada medição vê um ponto da curva, não a rotação. O que veria o ciclo inteiro: a soma das âncoras externas (boletim impresso, folha de votação, pesquisa de transferência, teste de integridade) comparada entre eleições.\n",
         '<p class="destaque">Esta página não afirma que a hipótese é verdadeira. Afirma algo mais incômodo: desde 2014, nenhuma eleição teve margem grande o bastante para que uma fraude desse tamanho fosse irrelevante, e nenhuma teve verificação física o bastante para que fosse impossível. As duas coisas nunca mais coincidiram.</p>\n']
    return "\n".join(L)


def fluxo(raiz, readme=False):
    """Fechamento de fluxo T1->T2 (analise exploratoria; script scripts/exploratorio/10_fechamento_fluxo.py, saidas results/exploratorio/FLX_*).
    Numeros fixos da analise publicada; reconciliacao com A31 (f 2026: 0,7360 x 0,7367 versionado)."""
    L = ["## A conta que não fecha: de onde vieram os votos do 2º turno\n",
         "Em todo 2º turno desde 2002, os votos que cada finalista ganha têm que vir de algum lugar: dos eliminados alinhados, de quem votou branco ou nulo no 1º turno e do comparecimento novo. Em 2026, essa conta não fecha sem sobra.\n",
         '<div class="duo">',
         "<div>",
         "<h3>O lado de Lula</h3>",
         "<ul>",
         "<li>Lula ganhou <strong>+10,38 milhões</strong> de votos entre o 1º e o 2º turno. As fontes naturalmente alinhadas explicam de 3,7 a 5,5 milhões. <strong>Sobram de +4,8 a +6,7 milhões sem fonte óbvia.</strong></li>",
         "<li>Para fechar a conta sem sobra, seria preciso que <strong>90 a 99%</strong> dos votos de Cury, Caiado e Zema (6,42 milhões, todos com endosso declarado a Flávio) tivessem ido para Lula. Na série histórica, quando um eliminado endossa um finalista, cerca de 73% dos votos seguem o endosso (2014). Cross-over nessa escala não tem precedente em 2002-2022.</li>",
         "</ul>",
         "</div>",
         "<div>",
         "<h3>O outro lado, e os controles honestos</h3>",
         "<ul>",
         "<li>Espelho: Flávio ganhou só <strong>+3,72 milhões</strong>, tendo um pool de direita endossado de cerca de 8,9 milhões.</li>",
         "<li>Desvios de 2 a 7 milhões entre esperado e observado aconteceram nas 7 eleições da série (2014 teve desvio maior ainda, contra o PT: -6,73 milhões). O que é sem precedente em 2026 não é o tamanho do desvio: é a <strong>direção e a composição</strong>. O finalista com o menor pool ganhou o maior volume, e o fechamento benigno exige comportamento eleitoral inédito.</li>",
         "</ul>",
         "</div>",
         "</div>\n",
         "Reconciliação com o teste municipal: as transições município a município já publicadas (A31) reproduzem exatamente nesta análise (f 2026: 0,7360 contra 0,7367 versionado). As duas leituras são consistentes; o fechamento nacional com pools ideológicos mede o que o municipal agnóstico não mede.\n",
         "**Status:** análise **exploratória**; pré-registro A39 proposto (cross-over implícito x pesquisas de transferência do 2º turno de 2026); dados e script em `results/exploratorio/FLX_*` e `scripts/exploratorio/10_fechamento_fluxo.py`.\n",
         '<p class="destaque">Uma conta que não fecha não é prova de nada: pode ser a maior onda eleitoral da série, e nenhum teste separa onda de operação com dados internos. Mas é a primeira vez que fechar a conta exige acreditar em algo que nunca aconteceu. O que decide não é este dossiê: é pesquisa de transferência de voto do 2º turno, folha de votação e boletim impresso. Enquanto isso não chega, a pergunta fica registrada.</p>\n']
    return "\n".join(L)


def cartao(r, readme):
    anc = "" if readme else f'<a id="{str(r.id).lower()}"></a>\n'
    if pd.notna(r.teto_pior_caso):
        med = f"excesso medido: {n(r.excesso_medido)} votos de margem; " if pd.notna(r.excesso_medido) and r.excesso_medido > 0 else ""
        teto = f"{med}**teto de pior caso, não estimativa: {n(r.teto_pior_caso)} votos de margem ({n(r.pct_margem_teto, 2) if r.pct_margem_teto >= 0.01 else 'menos de 0,01'}% da margem)**" + (f" ({r.nota})" if isinstance(r.nota, str) and r.nota else "")
    else:
        base = "sem número ainda (teste não executado)" if r.situacao == "NÃO TESTADO" else ("sem número (teste de forma, não convertível em votos)" if r.situacao == "TESTADO-INCONCLUSIVO" else "não mensurável com dados públicos")
        teto = base + (f" ({r.nota})" if isinstance(r.nota, str) and r.nota else "")
    return (anc + f"> **{r.pergunta}**  \n> Situação: **{r.situacao}** · Direção: {r.direcao}  \n> Teto: {teto}  \n> O que fecharia: {r.fechar}  \n"
            f"> [Página técnica]({link(r.pagina, readme)}) · [Abrir issue]({r.issue.replace(' ', '%20')}%20{r.id})\n")


def perguntas(raiz, readme=False):
    D, _ = carrega(raiz)
    L = ["## Perguntas em aberto: o que os testes não conseguiram explicar nem confirmar\n",
         "**Não são evidência de nada, nem de um lado nem do outro: são lacunas que só dados novos fecham. Se você tem dados ou método para fechar alguma, contribua.**\n",
         "Cada cartão traz a pergunta, a situação, a direção do efeito (a favor de quem, se houver), o teto em votos de margem com a ressalva na mesma linha e o que fecharia a questão. Dentro de cada bloco, a ordem é pelo tamanho do que a resposta poderia mudar (maior teto ou maior ponto cego primeiro). Os tetos são limites superiores sob o pior caso; a margem é de 4.430.191 votos de margem.\n"]
    for b, t in (("a", "a) Resíduos sem causa identificada (testes executados, inconclusivos)"), ("b", "b) Hipóteses ainda não testadas (Fase 3, A20 a A28)"), ("c", "c) Pontos cegos estruturais (A18, A19)")):
        L.append(f"### {t}\n")
        for r in D[D.bloco == b].itertuples():
            L.append(cartao(r, readme))
    return "\n".join(L)


def resumo_perguntas(raiz, readme=False):
    """Resumo de 3-4 linhas da pagina 'Perguntas em aberto', com link para a pagina propria."""
    D, _ = carrega(raiz)
    n_t = len(D)
    mai = D[D.pct_margem_teto.notna() & (D.pct_margem_teto != "") & ~D.nota.str.contains("inflado", na=False)].copy()
    topo = mai.sort_values("pct_margem_teto", ascending=False).iloc[0]
    L = ["## Perguntas em aberto (resumo)\n",
         f"Há **{n_t} perguntas em aberto**: resíduos sem causa identificada, hipóteses ainda não testadas e pontos cegos estruturais. "
         f"O maior teto de pior caso, não estimativa, é {n(topo.pct_margem_teto, 2)}% da margem ({topo.id.replace('A-', '').replace('-part', '')}). "
         "**Não são evidência de nada, nem de um lado nem do outro: são lacunas que só dados novos fecham.**\n",
         f"Lista completa, com situação, teto e o que fecharia cada uma: [Perguntas em aberto]({link('perguntas-em-aberto.html', readme)}).\n"]
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
