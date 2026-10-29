#!/usr/bin/env python3
"""docs/a18-alteracao-no-meio.md, docs/a19-voto-digitado.md e docs/boletins-impressos.md, gerados dos resultados.
Uso: python -I 03f_paginas_a18_a19.py DIR_FASE2 RAIZ"""
import os
import sys
import pandas as pd

R, RAIZ = sys.argv[1], sys.argv[2]
DOCS = os.path.join(RAIZ, "docs")
REPO = "https://github.com/baduba/eleicoes-dossie-2026"
FORM_BU = "https://form.jotform.com/263017066351047"
rd = lambda f: pd.read_csv(os.path.join(R, f))


def n(x, d=0):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "n/d"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


ROT = {"votos_central": "votos_central (votos de margem)", "votos_ic95_inf": "votos_ic95_inf (votos de margem)", "votos_ic95_sup": "votos_ic95_sup (votos de margem)",
       "votos_max_margem": "votos_max_margem (votos de margem)", "votos_max_pior_caso": "votos_max_pior_caso (teto de pior caso, votos de margem)", "votos_margem": "votos_margem (votos de margem)",
       "soma_votos_sobreviventes_exigente": "soma_votos_sobreviventes_exigente (votos de margem)", "soma_votos_sobreviventes_pior_caso": "soma_votos_sobreviventes_pior_caso (teto de pior caso, votos de margem)",
       "maximo_individual_pior_caso": "maximo_individual_pior_caso (teto de pior caso, votos de margem)", "soma_de_todos_exigente": "soma_de_todos_exigente (votos de margem)",
       "votos_perdidos": "votos_perdidos (votos, contagem)", "votos_perdidos_liquidos_somados": "votos_perdidos_liquidos_somados (votos, contagem)", "ganho_liquido_nacional": "ganho_liquido_nacional (votos, contagem)"}


def tab(df, fmts=None):
    fmts = fmts or {}
    cols = list(df.columns)
    L = ["| " + " | ".join(ROT.get(c, c) for c in cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.astype(object).iterrows():
        L.append("| " + " | ".join(((fmts[c](r[c]) if c in fmts else str(r[c])).replace("|", "/")) for c in cols) + " |")
    return "\n".join(L)


a18 = rd("a18_testes.csv")
a18a, a18b, var = rd("A18_a18a_resumo.csv"), rd("A18_a18b_resumo.csv"), rd("A18_a18b_variancia_do_horario.csv")
cons, h30 = rd("A18_a18a_consistencia.csv"), rd("A18_a18a_recebimento_por_30min_2026T1.csv")
cert = rd("cert_RR_2026.csv")
t1r, t1c, t1u, t1j, t1p = rd("A1T1_resumo.csv").iloc[0], rd("A1T1_corridas.csv"), rd("A1T1_ufs.csv"), rd("A1T1_ufs_janela.csv"), rd("A1T1_pontos.csv")
pbu, pinv = rd("poder_bu_impresso.csv"), rd("secoes_para_inverter_margem.csv")
uf, pint, prem = rd("teste_integridade_por_uf_regra.csv"), rd("poder_teste_integridade.csv"), rd("poder_teste_integridade_premissas.csv").iloc[0]

# ------------------------------------------------------------------------------------------------ A18
L = []
A = L.append
A("# A18. Hipótese \"alteração no meio\" (entre o fechamento da urna e a publicação)\n")
A("**Hipótese.** Alguém altera os resultados depois que a urna fecha e antes de os dados serem publicados (na transmissão, na recepção, na totalização ou na publicação), de modo coerente em todos os arquivos.\n")
A("> **O que A4 e H9 verificam e o que não verificam.** Verificam **consistência entre arquivos publicados pelo TSE** (BU, RDV, imagem do BU, log, BWeb, totalização por zona e município) e o vínculo de hash entre eles. Esses arquivos nascem do mesmo software e do mesmo fluxo. Por isso **não excluem uma alteração coerente feita antes da publicação**. Só uma verificação que não dependa dos arquivos publicados exclui essa hipótese: a **assinatura criptográfica** conferida com a chave oficial, e a **comparação com boletins impressos** fotografados nas seções.\n")
A("## 1. Os atrasos, com fonte\n")
A("| turno | o que foi dito ou decidido | fonte | o que os dados mostram |\n|---|---|---|---|")
rec26 = h30.set_index("inicio")
A(f"| 1º turno (04/10/2026) | O presidente do TSE confirmou atraso de cerca de 1 hora na divulgação do total, que atribuiu a congestionamento no sistema de dados da Corte (\"fluxo de dados acima do normal\"). Por volta das 19h o total nacional de presidente ficou parado em 64%; por volta das 20h voltou a andar, já em 84%. O TSE disse não saber ainda se havia causa além do congestionamento. | [JB, 05/10/2026](https://www.jb.com.br/brasil/politica/2026/10/1061122-tse-confirma-atraso-na-totalizacao-dos-votos-e-explica-causa.html) (imprensa; paráfrase da declaração; a fonte oficial não pôde ser aberta) | Entre 19:30 e 19:59 só {n(rec26.loc['19:30','pct'],1)}% das seções tiveram o BU recebido, contra {n(rec26.loc['19:00','pct'],1)}% entre 19:00 e 19:29 e {n(rec26.loc['20:00','pct'],1)}% entre 20:00 e 20:29 (tabela abaixo). |")
A("| 2º turno (25/10/2026) | A votação foi prorrogada por duas horas por decisão do ministro Cristiano Zanin, a pedido da campanha de Lula (falta de ônibus na Bahia); o TSE informou que a votação continuaria só nas seções ainda abertas às 17h. O recebimento de BUs, a totalização e a divulgação foram retomados às 19h; antes da pausa, 1.225 das 499.248 seções (cerca de 0,25%) estavam contabilizadas. | [Times Brasil](https://timesbrasil.com.br/brasil/decisao-2026-tse-anuncia-retomada-da-totalizacao-e-divulgacao-dos-votos-apos-as-19h/) e [Correio da Manhã](https://www.correiodamanha.com.br/politica/2026/10/329719-tse-retoma-contagem-dos-votos-as-19h-apos-suspensao-provocada-por-decisao-de-zanin.html) (imprensa; o comunicado oficial não foi aberto) | 99,6% dos BUs têm horário de recebimento depois das 19h (A14). |")
A("\nRecebimento de BUs no 1º turno de 2026, por meia hora (todas as seções com horário de recebimento):\n")
A(tab(h30, {"secoes": lambda x: n(x), "pct": lambda x: n(x, 1)}))
A("\nO horário de recebimento é o campo `DT_RECEBIMENTO_BU_HOR_TSE` publicado pelo TSE. A queda das 19:30 às 20:00 é compatível com a paralisação descrita; os dados não dizem a causa.\n")
A("## 2. Assinatura criptográfica (prioridade máxima): NÃO EXECUTADO PARCIAL\n")
A(f"- **Lido e conferido:** o certificado X.509 de cada seção de Roraima em 2026: {n(len(cert))} lidos, 0 erros. CN = `UEAO` + número da urna do BWeb em {n(cert.cn_confere_com_urna.sum())} de {n(len(cert))}; validade cobre a data da eleição em {n(cert.valido_na_eleicao.sum())} de {n(len(cert))}; emissores " + ", ".join(f"`{k}` ({n(v)})" for k, v in cert.emissor_cn.value_counts().items()) + ".")
A(f"- **Verificado:** **0% das assinaturas** (0 de {n(len(cert))} seções lidas; 0 falhas porque nenhuma foi testada). O OID do algoritmo é `{cert.cert_alg_chave.iloc[0]}`, com chave de {int(cert.cert_chave_bytes.iloc[0])} bytes e assinatura de {int(cert.cert_assinatura_emissor_bytes.iloc[0])} bytes.")
A("- **O que falta:** o certificado raiz e a chave pública oficiais, e a especificação do algoritmo, obtidos de fonte oficial. O site do TSE responde HTTP 403 a automação, e **não foi usada nenhuma chave de fonte não oficial**. Uma apresentação do TSE de 2021 (vista só em resultado de busca) cita EdDSA sobre Curve25519 para o QR code do BU e curvas de 256 bits para outras assinaturas; isso não foi confirmado nem verificado aqui.")
A("- **Como destravar:** um perito ou fiscal com acesso à ferramenta oficial de verificação do TSE roda o script `scripts/13_cert_urna.py` e a ferramenta nos mesmos arquivos e publica o resultado por *issue*.\n")
A("## 3. Testes pré-registrados (Adendo 7)\n")
A("Janela e testes foram fixados no [Adendo 7](preregistro.md) antes de rodar. Os testes comparam o 2026 com a mesma janela de relógio em anos sem congestionamento (placebos), com efeito fixo de local de votação. **Previsão sem alteração:** nenhuma diferença além da composição.\n")
t = a18[["H", "teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "veredito"]].copy()
A(tab(t, {"est_2026T2": lambda x: n(float(x), 5), "p_excesso": lambda x: n(float(x), 3), "p_holm": lambda x: n(float(x), 3)}))
A("\n**Leitura.** Na janela de 19h às 20h do 1º turno, as seções do mesmo local que tiveram o BU recebido durante o congestionamento têm participação de Lula " + n(100 * a18.est_2026T2.iloc[0], 2) + " p.p. maior que as demais (e a do oponente, " + n(100 * abs(a18.est_2026T2.iloc[1]), 2) + " p.p. menor). Contra os placebos o p unilateral bruto é " + n(a18.p_excesso.iloc[0], 3) + " (2022 e 2018, o maior); com a correção de Holm para os quatro testes, " + n(a18.p_holm.iloc[0], 3) + ". **Não atinge o critério de excesso.** O veredito pela regra pré-registrada é inconclusivo porque o teto de pior caso passa de 1% da margem, e não porque haja excesso. No 2º turno não há diferença além dos placebos. Os tetos desta tabela são limites superiores sob a convenção de exposição do Adendo 7 e dependem da incerteza dos placebos; **não medem votos alterados**. Estes testes **não excluem** uma alteração coerente; eles buscam apenas uma assinatura temporal específica.\n")
A("Estimativas por ano (coeficiente da janela, em participação nos válidos; o erro padrão é agrupado por local):\n")
A(tab(a18a, {"secoes": n, "secoes_na_janela": n, "pct_na_janela": lambda x: n(x, 1), "coef_janela": lambda x: n(x, 5), "ep": lambda x: n(x, 5)}))
A("\nSeções com nominais + brancos + nulos diferentes do comparecimento no 1º turno de 2026 (previsão: zero nos dois grupos): janela = 1, dentro da janela de 19h às 20h; janela = 0, demais.\n")
A(tab(cons, {"secoes": n, "com_inconsistencia": n}))
A("\n**2º turno: ordem de recebimento depois das 19h.** Coeficiente por hora de atraso do recebimento:\n")
A(tab(a18b, {"secoes_apos_19h": n, "coef_por_hora": lambda x: n(x, 5), "ep": lambda x: n(x, 5)}))
A("\nParcela da variância do horário de recebimento explicada por UF e por município (descritivo, não é teste):\n")
A(tab(var, {"secoes_apos_19h": n, "r2_horario_por_UF": lambda x: n(x, 2), "r2_horario_por_municipio": lambda x: n(x, 2), "horas_mediana_apos_19h": lambda x: n(x, 2)}))
A("\nNo 2º turno de 2026 o horário de recebimento depois das 19h tem mais estrutura geográfica (por UF) do que nos anos de comparação. Isso é o esperado quando o recebimento é retido até um horário e liberado por ordem de transmissão; não distingue essa explicação de outra.\n")
A("## 3b. A1 corrigido no 1º turno de 2026 e a janela do congestionamento (análise posterior)\n")
A("> Análise **posterior** (pedida depois de ver o resultado; não pré-registrada). Ela não muda o veredito do A1 corrigido, cujo alvo pré-registrado é o 2º turno.\n")
mx = t1p.iloc[100:].loc[t1p.iloc[100:].desvio_pp.abs().idxmax()]
big = t1c.sort_values("n_pontos", ascending=False).iloc[0]
A(f"A curva do 1º turno de 2026, contra o nulo corrigido (municípios em ordem aleatória dentro de cada UF), fica fora do envelope em {int(t1r.pontos_fora)} dos 900 pontos avaliados, quase todos numa única corrida de {int(big.n_pontos)} pontos consecutivos, de {n(big.pct_secoes_de,1)}% a {n(big.pct_secoes_ate,1)}% das seções, das {big.horario_de[11:16]} às {big.horario_ate[11:16]} do dia 04/10.\n")
A(f"- **Coincide com a janela de 19h às 20h?** Em parte. A corrida **começa** dentro da janela ({big.horario_de[11:16]}) e {int(t1r.pontos_fora_na_janela)} dos {int(t1r.pontos_fora)} pontos fora do envelope ({n(t1r.pct_fora_dentro_da_janela,0)}%) caem entre 19h e 20h, contra {n(t1r.pct_pontos_na_janela,1)}% de todos os pontos da curva nessa janela. Mas a corrida **continua** até as {big.horario_ate[11:16]}, bem depois da retomada.\n- **O desvio não cresce na janela.** A curva fica abaixo da mediana do nulo (menos participação de Lula) em todo o trecho; o maior desvio é de {n(mx.desvio_pp,2)} p.p., com {n(mx.pct_secoes,1)}% das seções ({mx.horario[11:16]}), **antes** da janela. A partir daí o desvio diminui até zero ({n(t1p.iloc[757].desvio_pp,2)} p.p. aos 76%, {n(t1p.iloc[839].desvio_pp,2)} p.p. aos 84%, {n(t1p.iloc[950].desvio_pp,2)} p.p. aos 95%). O trecho \"fora do envelope\" é a parte final da curva, em que o envelope do nulo se estreita porque a curva acumulada converge para o total; ali um desvio pequeno já sai do envelope.\n")
top = t1u.sort_values("pct_das_secoes_nas_corridas", ascending=False).head(6)
A("- **Quais UFs chegaram nesse trecho.** As seções que chegaram na corrida vêm sobretudo de " + ", ".join(f"{r.SG_UF} ({n(r.pct_da_UF_nas_corridas,0)}% da UF)" for r in top.itertuples()) + "; BA, RJ, CE, PE, MA e AL pesam mais no trecho que no país (colunas abaixo). Nas seções cuja primeira totalização caiu entre 19h e 20h, as maiores contribuições são " + ", ".join(f"{r.SG_UF} ({n(r.pct_das_secoes_da_janela,1)}%)" for r in t1j.head(5).itertuples()) + ".\n")
A("Seções por UF no trecho fora do envelope (todas as UFs em `results/fase2/A1T1_ufs.csv`):\n")
A(tab(t1u.head(10), {"secoes": n, "nas_corridas": n, "pct_da_UF_nas_corridas": lambda x: n(x, 1), "pct_das_secoes_nas_corridas": lambda x: n(x, 1), "pct_das_secoes_do_pais": lambda x: n(x, 1)}))
A("\nSeções cuja primeira totalização caiu entre 19h e 20h, por UF (todas em `results/fase2/A1T1_ufs_janela.csv`):\n")
A(tab(t1j.head(10), {"secoes": n, "na_janela": n, "pct_da_UF_na_janela": lambda x: n(x, 1), "pct_das_secoes_da_janela": lambda x: n(x, 1), "lula_pct_validos_na_janela": lambda x: n(x, 1)}))
A("\n**Conclusão.** A janela do congestionamento **não explica** o trecho fora do envelope: ele começa dentro dela, mas continua depois e o desvio é decrescente. A composição por UF (nordeste e sudeste chegando depois) é compatível com o desvio, mas a explicação não foi demonstrada. O item vai para [Questões em aberto](residuos.md). Nada aqui indica alteração de votos; é uma forma da curva que o nulo usado não reproduz.\n")
A("## 4. Poder de detecção dos boletins impressos\n")
A("Quantos boletins impressos de seções sorteadas ao acaso seriam necessários para detectar, com 95% e 99% de probabilidade, ao menos uma seção alterada, se uma fração das seções tivesse sido alterada (população de 499.248 seções, amostra sem reposição):\n")
A(tab(pbu, {"secoes_alteradas": n, "n_para_95": n, "n_para_99": n}))
A("\nQuantas seções seriam necessárias para inverter a margem de 4.430.191 votos, se cada seção alterada tivesse 5, 50 ou 200 votos trocados (cada voto trocado muda a margem em 2) e quantos boletins sorteados bastariam para flagrar ao menos uma delas:\n")
A(tab(pinv, {"secoes_necessarias_para_inverter_a_margem": n, "pct_das_secoes": lambda x: n(x, 1), "n_para_95": n, "n_para_99": n}))
A("\nO cálculo vale para amostra aleatória de seções. Fotos enviadas voluntariamente não são aleatórias e reduzem o poder; o que vale é o total conferido sem divergência, publicado em [Boletins impressos](boletins-impressos.md). Para inverter a margem com 50 trocas por seção, a alteração teria de atingir " + n(pinv.pct_das_secoes.iloc[1], 1) + "% das seções, e uma amostra de " + n(pinv.n_para_99.iloc[1]) + " boletins a detectaria com 99% de probabilidade.\n")
A("## 5. Coleta\n")
A("O cruzamento direto com boletins impressos continua **NÃO EXECUTADO** por falta de insumo. A página [Boletins impressos](boletins-impressos.md) explica como enviar fotos, e o script `04_cruza_bu_impresso.py` está pronto para ser rodado a cada lote.\n")
A("## 6. Janela dos atrasos: o que ainda falta\n")
A("- **1º turno:** o teste usa a janela de relógio do Adendo 7 e a comparação dentro do local. Uma janela baseada no log do Sistot (não público) seria mais precisa.\n- **2º turno:** o teste compara a ordem de recebimento depois das 19h com a participação de Lula dentro do local, controlando o 1º turno. A comparação com a geografia é a tabela de variância acima.\n")
open(os.path.join(DOCS, "a18-alteracao-no-meio.md"), "w", encoding="utf-8").write("\n".join(L))

# ------------------------------------------------------------------------------------------------ boletins impressos
L = []
A = L.append
cur = pd.read_csv(os.path.join(RAIZ, "results", "graficos", "curvas_deteccao.csv")) if os.path.exists(os.path.join(RAIZ, "results", "graficos", "curvas_deteccao.csv")) else None

def prob(col, fracao):
    r = cur.iloc[(cur.fracao - fracao).abs().idxmin()]
    return n(100 * r[col]) + "%"

A("# Boletins de urna impressos: como enviar fotos\n")
A("**Por que.** O boletim de urna impresso é a única cópia dos resultados de uma seção que **não passa** pelos arquivos que o TSE publica. Todo o resto (RDV, BU digital, BWeb, totalização) nasce do mesmo software da urna: se esse software registrasse diferente do digitado, todos esses arquivos concordariam entre si — e com o erro. A foto do boletim afixado na seção é a **única verificação independente** desse elo cego. Comparar o que está impresso com o BWeb exclui, para as seções conferidas, uma alteração coerente feita depois do fechamento da urna. Nenhuma foto foi recebida até agora; o teste direto permanece **NÃO EXECUTADO** ([A18](a18-alteracao-no-meio.md)).\n")
A("**Quem pode enviar.** Mesários, eleitores, imprensa e fiscais de qualquer partido ou coligação. Pela lei, o presidente da mesa receptora é obrigado a entregar cópia do boletim aos partidos e coligações que a requeiram até uma hora após a expedição (Lei 9.504/1997, art. 68, § 1º, [texto no Planalto](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm)); o boletim também fica afixado na seção e pode ser fotografado por qualquer pessoa. Não é preciso identificar-se publicamente.\n")
A("## O que fotografar\n")
A("1. O **boletim inteiro, de frente e legível**, sem cortar o **cabeçalho** (onde estão UF, município, zona e seção) nem as linhas de votos do fim. Se não couber tudo, vale uma foto do cabeçalho e outra das linhas de votos.\n2. Ou, em vez da foto inteira, o **QR Code** do boletim, nítido e sem reflexo.\n3. Anote **UF, município, zona, seção e turno** (estão no boletim) e a **origem** da foto: mesário, eleitor, imprensa ou fiscal (e de qual partido, se quiser dizer). A origem é registrada junto com a foto.\n4. Nenhum dado pessoal de eleitor. O boletim não os contém; não envie fotos de outros documentos.\n")
A("## Como enviar: dois canais\n")
A("Os dois canais levam à mesma conferência (BWeb, divergência publicada uma a uma). **Canal 1** exige conta no GitHub; o **canal 2** não.\n")
A(f"[**Enviar sem conta no GitHub**]({FORM_BU})  ·  [**Enviar pelo GitHub**]({REPO}/issues/new?template=envio-bu.yml)\n")
A("### Canal 2: sem conta no GitHub (formulário)\n")
A(f"1. Abra o [formulário]({FORM_BU}).\n2. Preencha UF, município, zona, seção, turno e origem (mesário, eleitor, imprensa ou fiscal), anexe a foto do boletim inteiro ou o QR Code nítido e, se puder, transcreva os números.\n3. Envie. Não é preciso conta no GitHub.\n")
A("**O que acontece com a foto no canal 2.** As respostas são exportadas e importadas periodicamente (não é em tempo real) por `scripts/importa_formulario.py`, que remove o **EXIF e todo metadado** (local, data, aparelho): a imagem publicada é recomposta só com os pixels e **o arquivo original nunca é publicado**. O texto livre do campo Observações, o endereço IP e qualquer dado que o serviço do formulário guarde não são publicados. A foto passa pelo mesmo pipeline do canal 1 (leitura do QR Code quando legível, conferência com o BWeb, tabela de resultados), com a origem registrada como \"formulario\" e o ID da submissão. Envios de teste (campo Observações com a palavra TESTE) são excluídos dos resultados.\n")
A("### Canal 1: com conta no GitHub (passo a passo)\n")
A(f"1. Abra o formulário: [{REPO}/issues/new?template=envio-bu.yml]({REPO}/issues/new?template=envio-bu.yml).\n2. O título já vem com o prefixo \"BU: \"; complete com UF, zona, seção e turno (ex.: \"BU: SP-123-456-2\").\n3. Preencha UF, município, zona, seção, turno e origem nos campos do formulário.\n4. **Arraste a foto para a caixa de texto do corpo da issue** — o formulário não tem campo de anexo; a foto entra como anexo do comentário. Confira na pré-visualização que ela abre legível.\n5. Se preferir, transcreva os números no formato abaixo (uma linha por boletim), no campo próprio do formulário.\n6. Envie. Não é preciso conta verificada nem identificação além da conta do GitHub.\n")
A("```\nano;turno;uf;cd_municipio;zona;secao;aptos;comparecimento;lula;oponente;brancos;nulos\n```\n")
A("## O que acontece com cada lote\n")
A("1. Cada lote recebido é conferido automaticamente com o BWeb por `scripts/04_cruza_bu_impresso.py`, que reporta **qualquer** divergência, de um voto que seja.\n2. **Cada divergência é publicada individualmente**, com a foto, a seção e a origem, e com o que o BWeb mostra.\n3. O **total conferido sem divergência** é publicado a cada lote, junto com o poder estatístico abaixo.\n4. Fotos ilegíveis ou sem os dados de identificação da seção são listadas como descartadas, com o motivo.\n")
A("## Situação\n")
A("| lotes recebidos | BUs conferidos | divergências | origem das fotos |\n|---|---|---|---|\n| 0 | 0 | 0 | n/a |\n")
A("## Meta de coleta: o que cada total de boletins enxerga\n")
if cur is not None:
    A("Chance de flagrar **ao menos uma** seção alterada, em função do total de boletins conferidos e da fração de seções alteradas no país (amostra aleatória; cálculo hipergeométrico de [G2](index.md#g2)):\n")
    A("| fração de seções alteradas | 100 boletins | 300 boletins | 1.000 boletins |\n|---|---|---|---|")
    for f, rot in ((0.001, "0,1% (500 seções)"), (0.01, "1% (4.993 seções)"), (0.02, "2% (9.985 seções)"), (0.05, "5% (24.963 seções)")):
        A(f"| {rot} | {prob('bu_100', f)} | {prob('bu_300', f)} | {prob('bu_1000', f)} |")
    A("")
A("Para amostras aleatórias de seções (as fotos voluntárias não são aleatórias; ver ressalva em [A18](a18-alteracao-no-meio.md)), quantos boletins seriam necessários para detectar, com 95% e 99% de probabilidade, ao menos uma seção alterada:\n")
A(tab(pbu, {"secoes_alteradas": n, "n_para_95": n, "n_para_99": n}))
open(os.path.join(DOCS, "boletins-impressos.md"), "w", encoding="utf-8").write("\n".join(L))

# ------------------------------------------------------------------------------------------------ A19
L = []
A = L.append
A("# A19. Ponto cego central: voto digitado x voto registrado\n")
A("> Os dados públicos verificam a cadeia do registro da urna até o total. A correspondência entre o voto digitado e o voto registrado é verificada apenas por amostragem no teste de integridade. O modelo atual não possui registro conferido pelo eleitor.\n")
A("## 1. O que os dados públicos não verificam\n")
A("O RDV (registro digital do voto), o BU digital, o BU impresso e a totalização são gerados pelo **mesmo software da urna** (a lei prevê que a urna registre digitalmente cada voto e assine digitalmente o arquivo de votos: Lei 9.504/1997, art. 59, §§ 4º a 6º, [texto no Planalto](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm); os arquivos de saída da urna constam no leiame oficial dos arquivos de urna e no Glossário de TI do TSE). Portanto **A4, H9 e o cruzamento com o BU impresso não verificam se o voto registrado corresponde ao voto que o eleitor digitou**. Eles verificam que os artefatos da urna são coerentes entre si e com o total.\n")
A("## 2. Teste de integridade de 2026\n")
A("O teste de integridade é uma votação simulada, com cédulas de papel preenchidas e depois digitadas na urna, em urnas sorteadas, para comparar o voto digitado com o registrado. É a **única** verificação, no modelo atual, da correspondência entre voto digitado e voto registrado.\n")
A("**O que a regra estabelece.** Pelo art. 58 da Res. TSE 23.673/2021 (conforme relatórios de auditoria externa publicados pelos TREs, [exemplo: TRE-SC 2022](https://www.tre-sc.jus.br/eleicoes/arquivos_eleicoes/eleicoes-2022/audit_ele2022_2t_relatorio_auditoria_externa)), são sorteadas 23, 35 ou 43 urnas por UF (conforme tenha até 15.000, de 15.001 a 30.000 ou mais de 30.000 seções), das quais 20, 27 ou 33 vão ao teste de integridade; o teste com biometria abrange de 5% a 10% das urnas do teste de integridade (relatórios de auditoria externa de 2024). A Res. TSE 23.758/2026 formalizou o teste de integridade com biometria em todas as UFs (indicação por resultado de busca; texto não aberto). As seções são definidas na véspera, com a participação de instituições habilitadas e, quando necessário, por sorteio (TCU); a apresentação do TRE-MG indica uma seção por zona eleitoral e ao menos uma da capital.\n")
A(f"**Total nacional.** Aplicando a regra à contagem de seções por UF do BWeb 2026, o teste de integridade teria **{int(prem.total_teste_integridade_pela_regra)} urnas** no 1º turno ({int(prem.biometria_5pct)} a {int(prem.biometria_10pct)} com biometria). **Este total foi calculado pela regra; não é um número publicado.** Confirmação em um caso: o TRE-SP informou 33 urnas no teste do 1º turno de 2026, três delas com biometria ([TRE-SP](https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-teste-de-integridade-confirma-pleno-funcionamento-das-urnas-eletronicas); lido em resultado de busca). Para 2022, a imprensa registrou 641 urnas, 58 delas com biometria (declaração atribuída ao ministro Moraes).\n")
A(tab(uf, {"secoes_apuradas_bweb_2026": n, "urnas_no_teste_de_integridade_pela_regra": n}))
A("\n**Quem acompanhou.** Segundo o TCU, equipes do tribunal acompanharam os testes nas 27 UFs no 1º turno e, nas UFs com 2º turno, também nele, com e sem biometria; o relatório consolidado será enviado ao TSE em até 30 dias corridos depois do 2º turno (processo TC 020.282/2026-5; [TCU](https://portal.tcu.gov.br/imprensa/noticias/eleicoes-2026-tcu-acompanha-testes-de-integridade-das-urnas-eletronicas)). O TSE informou 55 auditores do TCU em todo o país no 1º turno e dois equipamentos testados na sede do TSE ([TSE](https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-no-tse-confirma-correspondencia-entre-cedulas-e-votos-registrados-nas-urnas), título lido em resultado de busca; [Portal de Prefeitura, 04/10/2026](https://portaldeprefeitura.com.br/bastidores-da-politica/tse/tse-informa-auditores-tcu-acompanham-integridade-brasil/633457/)).\n")
A("**Resultado relatado.** Até a manhã de 04/10/2026, o TSE informou que nenhuma irregularidade de integridade havia sido registrada nesses procedimentos. Nenhuma divergência foi relatada nas fontes lidas.\n")
A("**NÃO EXECUTADO / não localizado:** (i) o número real de urnas por UF e por turno, com e sem biometria, além do caso de São Paulo; (ii) quem escolheu ou sorteou as seções em cada UF; (iii) quem acompanhou em cada UF; (iv) os relatórios de auditoria externa publicados por TRE para 2026 (os de 2024 estão publicados no site do TSE, por exemplo [MG, 1º turno](https://www.tse.jus.br/eleicoes/eleicoes-2024-content/arquivos-teste-de-integridade/arquivos-primeiro-turno/mg-relatorio-auditoria-externa-2024-1-turno-assinado)); (v) o relatório consolidado do TCU, devido até 24/11/2026. Insumo que falta: os relatórios dos TREs e do TCU de 2026. Esta página será atualizada quando forem publicados.\n")
A("## 3. Poder estatístico do teste de integridade\n")
A("Probabilidade de o teste observar **ao menos uma** divergência, se uma fração das urnas do país registrasse voto diferente do digitado:\n")
A(tab(pint, {c: (lambda x: n(100 * float(x), 1) + "%") for c in pint.columns if c != "fracao_de_urnas_alteradas"}))
A(f"\n**Premissa (a).** A urna que registrasse voto diferente do digitado faria isso também no teste: o comportamento no teste é igual ao da eleição, e as urnas do teste são uma amostra aleatória das {n(int(prem.urnas_de_votacao))} urnas de votação (n = {int(prem.total_teste_integridade_pela_regra)}). **Premissa (b).** O software distingue o teste sem biometria da votação real, e o único teste indistinguível da votação real é o **com biometria**; só essas urnas contam (n = {int(prem.biometria_5pct)} a {int(prem.biometria_10pct)}). As duas colunas (b) mostram o limite de 5% e o de 10%. Os cálculos supõem amostra aleatória simples sem reposição; o sorteio real (uma seção por zona, ao menos uma da capital) não é exatamente assim, então os números são aproximações. Esta seção descreve apenas a capacidade de detecção do teste; não descreve como uma alteração seria construída.\n")
A("## 4. Voto impresso: contexto legal e histórico (fontes primárias)\n")
A("| data | fato | fonte |\n|---|---|---|")
A("| 2009 | A Lei 12.034/2009, art. 5º, instituía o voto impresso a partir de 2014. | [STF, 2013](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=252858) |")
A("| 06/11/2013 | O STF (ADI 4543, relatora ministra Cármen Lúcia) declarou, por unanimidade, a inconstitucionalidade do art. 5º, por comprometer o sigilo e a inviolabilidade do voto (art. 14 da Constituição), além do risco de coação. | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=252858), [voto da relatora](https://noticias.stf.jus.br/postsnoticias/integra-do-voto-da-ministra-carmen-lucia-na-adi-do-voto-impresso/) |")
A("| 2015 | A Lei 13.165/2015 incluiu o art. 59-A na Lei 9.504/1997, exigindo o registro impresso de cada voto. | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=451785) |")
A("| 06/06/2018 | Liminar do STF suspendeu a regra (ADI 5889, proposta pela PGR). | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=380571) |")
A("| 14/09/2020 | O STF confirmou a liminar por unanimidade e declarou inconstitucional o art. 59-A e seu parágrafo único (relator ministro Gilmar Mendes): a impressão do registro do voto \"põe em risco sigilo e liberdade de voto\". O texto compilado da lei indica: \"Declarado inconstitucional pela ADI nº 5.889\". | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=451785), [Lei 9.504 compilada](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm) |")
A("| 05 e 06/08/2021 | Na Câmara, a comissão especial da PEC 135/2019 (voto impresso obrigatório) rejeitou o substitutivo por 23 a 11 e recomendou ao Plenário a rejeição da PEC por 22 a 11. | [Câmara](https://www.camara.leg.br/noticias/790507-comissao-especial-rejeita-por-23-a-11-o-voto-impresso-obrigatorio/), [Câmara](https://www.camara.leg.br/noticias/791064-comissao-recomenda-por-22-a-11-a-rejeicao-da-pec-do-voto-impresso/) |")
A("\nO resultado da votação em Plenário não foi confirmado nas fontes primárias lidas; verificar na tramitação da PEC 135/2019 no portal da Câmara.\n")
A("**Duas coisas diferentes.** (1) **Registro conferido pelo eleitor que fica na urna:** a urna imprimiria o voto, o eleitor o conferiria e o papel ficaria depositado na urna, sem sair com ele. Foi o que previram o art. 5º da Lei 12.034/2009 e o art. 59-A da Lei 9.504/1997; ambos foram declarados inconstitucionais. (2) **Comprovante entregue ao eleitor:** um papel que sai da seção com o eleitor, que provaria em quem ele votou. A lei vigente prevê o registro digital assinado de cada voto (art. 59, §§ 4º a 6º) e a urna que \"contabilizará cada voto, assegurando-lhe o sigilo e inviolabilidade\" (art. 61), e não prevê comprovante em papel ao eleitor. O motivo legal apontado pelo STF para vedar o registro impresso é o **sigilo e a liberdade do voto** (risco de coação e de prova do voto; inclusive, na ADI 5889, a regra de o processo depender da conferência pelo eleitor). A leitura de que o motivo do comprovante é impedir prova de voto, e portanto compra de voto, decorre dessa fundamentação do STF; ela é uma inferência desta página, não um trecho citado.\n")
A("## 5. Recontagem\n")
A("Não existe cédula física de votação no modelo atual; portanto não há \"recontagem de papel\". A \"recontagem\" possível é **reprocessar o RDV e os BUs** e compará-los com a totalização. Isso foi feito em [A4](resultados-fase2.md) (RDV recontado contra o BU, Lula, oponente, brancos e total, em 14.067 seções de 2026) e em H9 (BWeb contra `votacao_secao` e totalização por zona e município), sem divergências em 2026. **Esse reprocessamento usa arquivos gerados pela própria urna** e, por isso, não mede a correspondência entre o voto digitado e o registrado (ver seção 1).\n")
A("## 6. Conclusão desta seção\n")
A("Os dados públicos verificam a cadeia do registro da urna até o total. A correspondência entre o voto digitado e o voto registrado é verificada apenas por amostragem no teste de integridade. O modelo atual não possui registro conferido pelo eleitor.\n")
open(os.path.join(DOCS, "a19-voto-digitado.md"), "w", encoding="utf-8").write("\n".join(L))
print("escritos a18, boletins-impressos e a19")
