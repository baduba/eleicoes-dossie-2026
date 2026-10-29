# Pré-registro das hipóteses (escrito antes de abrir qualquer arquivo BWeb)

Data de escrita: 2026-10-28, antes do download dos arquivos `bweb_*`.

Transparência sobre o que já era conhecido ao escrever: os totais, a unanimidade, o Benford, o salto de comparecimento,
a contagem de seções com comparecimento >= 95% (639 no T2/2026) e o proxy por hora de recebimento do BU (+1,1 p.p.
contra +1,7 a +1,9 nos placebos) vieram do conjunto `detalhe_votacao_secao`/`votacao_secao`. Nada de liberação manual,
horário de abertura/encerramento ou tipo de voto foi visto ainda.

Notação: M = margem oficial = 4.430.191 votos. "Efeito" = votos que o fenômeno poderia explicar, no máximo.
Critério geral de veredito: uma hipótese só é SUSTENTADA se (a) o efeito em 2026/T2 for estatisticamente distinto dos
três placebos (2022 T1, 2022 T2, 2026 T1), (b) sobreviver a Holm/BH, (c) sobreviver ao controle geográfico e (d) não
for explicado por nenhuma explicação mundana testada. Caso contrário: REFUTADA (efeito estimado dentro do ruído e/ou
igual aos placebos) ou INCONCLUSIVA (dados insuficientes ou poder baixo).

| H | Se houver fraude, espero | Se não houver, espero |
|---|---|---|
| H1 liberação manual x voto Lula | coef. positivo em 2026/T2, maior que nos placebos, curva dose-resposta crescente nas faixas altas, ausente para Flávio simétrico | coef. com o mesmo sinal e magnitude parecida nos 4 placebos (manual correlaciona com perfil rural/pobre), sem dose-resposta específica de 2026/T2 |
| H2 aumento da liberação manual | taxa manual sobe de 2022 para 2026 nas mesmas seções e a subida prevê variação T1->T2 do voto Lula só em 2026 | subida difusa ligada a mudança de biometria (cadastro), prevê variação T1->T2 igualmente em 2022 ou nada |
| H3 encerramento | grande massa de seções fecha após 19h ou parcela relevante de votos após 17h concentrada em poucas seções | quase todas as seções fecham em 19h ou logo depois (prorrogação geral), logs/horários coerentes com a decisão do TSE; tabela do relatório não reproduzível por esta fonte |
| H4 encerradas após 19h | voto Lula e variação T1->T2 maiores nessas seções em 2026, não em 2022 nas mesmas seções | diferença igual ao placebo (seções que fecham tarde são rurais/grandes/com fila e já votavam diferente) |
| H5 639 seções >= 95% | maioria antiga, com comparecimento 2022 baixo, manual alto, fechamento atípico, Lula-skew só no T2 | maioria nova, pequena, local atípico (indígena, presídio, hospital, quilombo), já visível no T1/2026, skew pelo reduto local |
| H6 seções novas | voto/comparecimento destoa das antigas do mesmo local | iguais às antigas do mesmo local (efeito fixo de local absorve) |
| H7 outliers locais | excesso de outliers positivos para Lula em 2026/T2, sem espelho | contagem de outliers |z|>3 em ambos os sentidos próxima de 2022 e simétrica |
| H8 dígitos | último dígito não uniforme / percentuais inteiros em excesso em 2026/T2 | uniforme (p corrigido > 0,05) como 2022; ressalva: seções pequenas geram arredondamento natural |
| H9 consistência | soma das seções != totalização oficial | soma exata das seções = 64.256.232 e 59.826.041 (já confirmado nos CSVs de votação); comparação município a município só se o TSE publicar |
| H10 impacto agregado | soma dos excessos máximos que sobrevivem >= ordem da margem | soma pequena (< 1% de M) ou zero |

Previsão global: nulo para H1, H2, H4, H6, H7, H8; H3 e H5 são caracterizações, não testes de fraude.
Se alguma dessas previsões falhar, isso é reportado como está.

---

# Adendo 1: régua histórica (escrito antes de baixar ou abrir qualquer dado de 2014 e 2018)

Escopo: H5 (Klimek), H7 (outliers locais) e H8 (dígitos) em 2014, 2018, 2022 e 2026, T1 e T2.
Mapeamento de candidatos (conhecimento prévio, a confirmar nos dados): coluna `lula` = candidato nº 13 (PT:
Dilma 2014, Haddad 2018, Lula 2022 e 2026); coluna `dir` = oponente do 2º turno (Aécio nº 45 em 2014,
Bolsonaro nº 17 em 2018, Bolsonaro nº 22 em 2022, Flávio nº 22 em 2026).

## Métricas fixadas antes de olhar (por ano x turno x candidato)
- M5a: fração das seções (>= 30 votos válidos) no canto comparecimento >= 90% e voto do candidato >= 90%.
- M5b: correlação comparecimento x voto do candidato, dentro do local de votação (resíduo do efeito fixo).
- M5c: nº de seções com comparecimento >= 95% por 100.000 seções.
- M7a: taxa por 10.000 seções de |z| > 3 para cima e para baixo (z = desvio da seção contra a média das outras
  seções do mesmo local, ajustado por variância binomial e por sobredispersão estimada na própria eleição).
- M7b: razão entre outliers para cima e para baixo (simetria).
- M8a: qui-quadrado do último dígito (contagens de cada candidato com >= 20 votos) e V de Cramér.
- M8b: razão observado/esperado de seções com percentual inteiro exato.

## Critério de "parecido" (fixado agora, arbitrário mas declarado)
Duas eleições são "parecidas" numa métrica se a razão entre elas (M5a, M5c, M7a, M8b) está em [0,8; 1,25]
ou, para M5b, M7b e V de Cramér, a diferença absoluta é < 0,02 (M5b), razão em [0,8; 1,25] (M7b)
e < 0,005 (V). Uma hipótese histórica é avaliada pela maioria (>= 2/3) das métricas, por candidato PT e oponente.

## Previsões (qual padrão cada uma implica)
- A "desvio sempre, exceto 2018": 2014, 2022 e 2026 parecidas entre si e 2018 diferente das três.
- B "desvio a partir de 2022": 2014 e 2018 parecidas entre si, 2022 e 2026 parecidas entre si, os dois pares diferentes.
- C "sem desvio": os quatro anos parecidos entre si, depois de ajustar por geografia (efeito fixo de local).
Sou obrigado a registrar que a minha expectativa é C, com ressalva de que o critério acima pode classificar como
"diferentes" anos que mudaram por razões mundanas (tamanho médio de seção, biometria, remanejamento); por isso
reporto também as razões numéricas, não só o veredito A/B/C. Se nenhum dos três padrões se ajustar
(ex.: só 2014 diferente), reporto "nenhum dos três" e não forço o encaixe.

## Biometria (protocolo)
A comparação de liberação manual entre anos usa só seções em municípios com biometria nos dois anos, definidos como
município com soma de `QT_ELEI_BIOM_SEM_HABILITACAO` (ou o sinônimo do ano) > 0 em ambos. A medida é, por definição do
dicionário do TSE, "eleitores com biometria cadastrada que não foram habilitados por ela", não o total de liberações
manuais. Reporto também a versão sem filtro.

## Teste direto com boletins impressos
Só será executado se houver fotos/PDFs de BUs fornecidos. Procedimento: identificar zona/seção/turno (QR code ou
transcrição), cruzar com BWeb e reportar toda divergência de votos, aptos, comparecimento, abertura e encerramento.
Sem insumo, o teste termina com ERRO explícito "sem boletins impressos fornecidos" e consta como NÃO EXECUTADO.

---

# Adendo 2: correcoes de metodo feitas DEPOIS de ver os primeiros resultados de H1 a H4 (2022/2026)

Escrito em 2026-10-28, depois da primeira rodada de H1-H4 e ANTES de rodar H5-H8 e qualquer dado de 2014/2018.

1. Erro meu na primeira versao: o contraste "2026/T2 vs placebos" usava a media ponderada pelo inverso da variancia dos tres
   placebos. Como os placebos sao heterogeneos (a associacao manual x Lula em 2026/T1 e 0,074 e em 2022 e ~0), a media era
   dominada pelos placebos de 2022 e escondia o placebo mais relevante (2026/T1), produzindo uma linha falsa
   ("21,8% da margem"). Corrigido para teste de intersecao-uniao: o efeito so conta se superar CADA placebo.
2. Os p-valores usados na correcao Holm/BH passam a ser unilaterais de EXCESSO (2026/T2 maior que o placebo, no sentido da
   alegacao). Diferenca negativa nao e evidencia de nada. O p bilateral continua reportado.
3. Cada teste reporta dois tetos de votos: contra o placebo mais exigente e contra o mais frouxo (pior caso).
4. Regra operacional de veredito (fixada antes de H5-H8): "SUSTENTADA" = p_holm < 0,05 E teto de pior caso >= 1% da margem;
   "detectavel, magnitude irrelevante" = p_holm < 0,05 e teto < 1%; "REFUTADA" = p_holm >= 0,05 e teto < 1%;
   "INCONCLUSIVA" = p_holm >= 0,05 e teto >= 1%.
5. H3: o limite "votos apos 17h = taxa maxima x atraso" foi descartado por ser absurdamente frouxo; o BWeb nao tem log
   de voto, entao o numero de votos depois do horario nominal nao e mensuravel com esta fonte.
6. Correcao de leitura minha, da rodada anterior: os BUs de 2026/T2 chegaram ao TSE depois das 19h em 99,6% dos casos,
   mas 98,2% das secoes fecharam ate 15 min depois do horario nominal. A hora de recebimento reflete o TSE segurando o
   recebimento, nao o fechamento da secao. O proxy "hora do BU" usado antes nao mede encerramento.

---

# Adendo 3: análises posteriores e correções (escrito depois de ver os resultados de H1 a H10 e da régua histórica)

Tudo abaixo foi decidido depois de ver resultados e deve ser lido como exploratório, não pré-registrado.

1. Red team adicionado depois dos primeiros resultados: modelo da urna (H1 S0), composição do T1 com todos os candidatos e brancos/nulos
   (H1 S1 por candidato), comparecimento como desfecho (H1), interação e controles de tamanho (H6), padronização por tipo de local e
   tamanho (H5), taxa por tamanho em todos os anos (H5), numerador contra denominador (H5). Nenhum entra no registro de 23 testes.
2. Leitura por trios de anos na régua histórica (2018+2022+2026 homogêneo em 9 de 12 métricas; trios com 2014 em 5 de 12): análise posterior.
   `M5b_OPO` e `M8b_OPO` repetem `M5b_PT` e `M8b_PT` por construção; sem as repetições são 10 métricas independentes.
3. Erros meus corrigidos no caminho: (a) a leitura de "hora do BU" como proxy de encerramento (Adendo 2, item 6); (b) a afirmação
   de que a tabela de fechamento do relatório não podia ser conferida: reproduz exatamente (339.593) com o relógio cru da urna;
   (c) os totais oficiais de 2018/T1 citados de memória estavam trocados: o TSE divulgou Haddad 31.342.005 e Bolsonaro 49.276.990,
   iguais ao BWeb; quem tem 66 votos a mais em uma seção (MA/8591/zona 17/seção 25) é `votacao_secao`.
4. Resultado contrário à minha expectativa registrada (C): nenhum dos padrões A, B ou C se ajustou pelo critério fixado.
5. Teste com boletins impressos: não executado (sem insumo).

---

# Adendo 4: Fase 2 (A1 a A10), escrito em 2026-10-28 ANTES de rodar qualquer análise nova

O que já foi visto antes deste registro, para transparência: (a) os resultados da Fase 1; (b) a estrutura dos arquivos de urna de UMA
seção de Roraima (2º turno de 2026): cabeçalho do BU, forma do log e existência de eventos "Voto confirmado para [Presidente]" com horário.
Nenhum resultado das análises abaixo foi calculado.

Critério de veredito: o mesmo do Adendo 2, item 4 (SUSTENTADA / excesso detectável, magnitude irrelevante / REFUTADA / INCONCLUSIVA),
com p-valores de excesso corrigidos por Holm e BH sobre a família completa da Fase 2 (as linhas de teste novas entram no registro da Fase 1).
Placebos fixos: 2014/T2, 2018/T2, 2022/T2 e 2026/T1 (e, para dados de urna, 2022/T2). Toda análise é simétrica (PT e oponente).
Teste que não puder rodar: ERRO explícito e linha em "NÃO EXECUTADO" com o insumo que faltou.

## Previsões

| A | Se houver manipulação, espero | Se não houver, espero | Critério numérico fixado agora |
|---|---|---|---|
| A1 curva de apuração | a curva real sai do envelope de permutações dentro de UF (mantida a sequência de UFs), ou tem saltos descontínuos | curva real dentro do envelope B (permutação dentro de UF) em todos os pontos com >= 1% das seções; soma final idêntica | desvio máximo (p.p. de share) entre curva real e mediana de B; "excesso" só se superar o dos quatro placebos E sair do envelope 95% simultâneo por >= 20 pontos consecutivos; efeito na soma final é 0 por construção |
| A2 transições T1->T2 | excesso de seções em que o oponente perde votos absolutos com comparecimento estável, e forma da distribuição do swing diferente | frequência e forma dentro da faixa dos anos placebo | distância KS (e AD) do swing residual de 2026 contra cada placebo; "diferente" só se a MENOR distância a um placebo superar a MAIOR distância entre pares de placebos; frequência de perda do oponente fora da faixa [mín, máx] dos placebos |
| A3 origem dos votos | perda líquida do oponente em número de seções e de votos maior que nos placebos; coeficiente "oponente T1 -> PT T2" fora dos placebos | contabilidade fecha (identidade: dPT + dOPO = dComparecimento + Terceiros_T1 - dBrancosNulos); frequência de perda líquida do oponente na faixa dos placebos | frequência (ponderada por votos) e coeficiente ecológico com IC 95% contra [mín, máx] dos placebos |
| A4 cadeia da urna | divergência entre BU digital, RDV, BWeb ou assinatura | 0 divergências em toda a amostra | divergência de UM voto é reportada; amostra: UFs inteiras pequenas + estratificada nas grandes + todas as seções >= 19h das UFs baixadas |
| A5 logs | votos registrados depois do horário nominal em número ou padrão incompatível com o comparecimento; eventos impossíveis | votos confirmados no log = comparecimento do BU em >= 99,9% das seções; votos após o horário nominal concentrados nas seções que fecharam tarde; intervalos entre votos >= mínimo físico | (i) log x BU; (ii) votos após 17h nominal por seção e total; (iii) associação entre votos tardios e Lula% (dentro do local) contra 2022; (iv) menor intervalo entre votos |
| A6 contingência | seções com urna substituída votam diferente das vizinhas do mesmo local | iguais, dentro do erro | coeficiente do indicador de substituição com EF de local, contra 2022 se houver dado |
| A7 pesquisas | n/a (contexto) | n/a | só com número de registro e fonte; senão NÃO EXECUTADO. Sem veredito |
| A8 coerência entre cargos | seções em que o total de algum cargo difere do comparecimento | 0 seções fora da regra do cargo, igual a 2018 e 2022 | regra por cargo estimada nos placebos (modal); qualquer desvio listado |
| A9 perfil do comparecimento | comparecimento > 100% de aptos em alguma faixa; saltos atípicos em faixas facultativas | nenhuma célula > 100%; variações T1->T2 por faixa parecidas com 2022 | contagem de células > 100%; correlação das variações por faixa 2026 x 2022; células fora de [Q1-3 IQR, Q3+3 IQR] dos placebos |
| A10 modelo e software | excesso de outliers, ≥95% ou desvio de dígitos concentrado num modelo ou versão | taxas por modelo e versão dentro do intervalo dos placebos; exterior e locais especiais explicam os extremos | Poisson por modelo e versão contra a taxa geral, Holm |

Seções não estatísticas (matriz de pontos cegos, base legal, literatura, análise do relatório original) só usam fonte citada;
afirmação sem fonte verificável é retirada e listada.

---

# Adendo 5: A11, A12 e A13 (escrito em 2026-10-29 ANTES de rodar qualquer uma das três)

Já visto antes deste registro: os resultados de A1 a A10 e, em A1, a ordem de chegada por UF. Nada de A11, A12 ou A13 foi calculado.
Critério de veredito: o do Adendo 2, item 4. Placebos: 2018 e 2022 (e 2014 onde houver dado por candidato). Simetria PT e oponente.

## A11. Transferência de votos dos derrotados no 1º turno
- Contexto a citar com fonte: apoio de Zema, Caiado, Cury e Clariana ao Flávio; de Hertz Dias, Edmilson Costa e Samara Martins ao Lula (crítico); nulo de Rui Costa Pimenta; liberação de Renan Santos. Votos de cada um confirmados no BWeb.
- Contabilidade nacional: terceiros + queda de brancos e nulos + queda de abstenção = ganho de Lula + ganho de Flávio, termo a termo.
- Por seção: ganho de Lula e de Flávio (T2 menos T1, por apto) contra a fatia de cada bloco no T1 (Zema+Caiado+Cury+Clariana; esquerda; Renan Santos; PCO; brancos e nulos; abstenção), com efeito fixo de município. Taxas de transferência por regressão ecológica (Goodman), declarando a falácia ecológica; padrão de 2022 e 2018 calculado com a mesma especificação, com os terceiros de cada ano como blocos de mesmo tamanho (sem inferir apoios sem fonte).
- Sem manipulação: o ganho de Flávio cresce com a fatia do bloco que o apoiou; taxas estáveis entre UFs; padrão parecido com os anos-placebo.
- Com manipulação: o ganho de Lula cresce com a fatia do bloco pró-Flávio, concentrado em algumas UFs ou tipos de seção, e diferente dos placebos.
- Critério numérico: coeficiente "bloco pró-Flávio para Lula" fora de [mín, máx] dos coeficientes análogos dos placebos (maior bloco de terceiros de cada ano para Lula) E heterogeneidade entre UFs maior que a dos placebos (desvio padrão dos coeficientes por UF).

## A12. Seções com zero voto para um candidato
- Contar seções com zero voto para Flávio e para Lula em 2026 T1 e T2; o mesmo para os oponentes de 2022, 2018 e 2014. Conferir se o número 109 reproduz (a origem do 109 não foi informada: reporto todas as definições razoáveis, com e sem mínimo de comparecimento).
- Por seção: UF, município, local (nome e tipo), aptos, comparecimento, resultado no T1/2026, resultado na mesma seção em 2022 e 2018, taxa de liberação manual, encerramento e modelo de urna.
- P(zero) = (1 - p)^n com p estimado de duas formas: (i) voto da própria seção no T1; (ii) seções vizinhas do mesmo local (leave-one-out), com suavização. Número esperado = soma de P(zero); comparação com o observado por razão e por teste de Poisson-binomial aproximado.
- Sem manipulação: seções pequenas em locais homogêneos (aldeias, comunidades), com zero ou quase zero também em anos anteriores; observado próximo do esperado.
- Com manipulação: seções grandes ou urbanas, que tinham votos do oponente em 2022 e no T1/2026, e observado muito acima do esperado.
- Teto em votos: soma dos votos válidos dessas seções, contra a margem.

## A13. Alegação do vídeo "Prof. Marcelo Trindade" sobre a curva de apuração
- O vídeo e os dados das "472 urnas" não foram fornecidos a esta sessão; a alegação é tratada como foi resumida pelo Julio. Sem os dados e o código dos autores: **NÃO REPRODUZÍVEL** para a parte específica.
- Fonte da série: ordem de totalização por seção (primeira totalização parcial do TSE); snapshots do site Resultados não são públicos (a verificar).
- Contagem de inversões de liderança na ordem real, em 1.000 ordens aleatórias e em 1.000 ordens geográficas realistas (embaralhar dentro da UF mantendo a sequência de UFs). Trechos lineares por regressão em janela (R2 alto) na curva real e nas simuladas, atribuídos às UFs que chegaram no intervalo. "Método do vídeo": interpretação declarada aqui, antes de rodar: somar só os incrementos positivos da curva de margem (emendar os trechos de subida) e comparar com o mesmo procedimento em séries simuladas limpas.
- Total final independente da ordem e igual à soma dos BUs.
- Sem manipulação: a inversão única e os trechos lineares aparecem nas ordens geográficas realistas e são explicados pela região que chega; o método de emendar subidas produz "vitória" falsa também em séries limpas.
- Critério numérico: inversões e linearidade reais dentro do intervalo 95% das ordens geográficas simuladas.

## A13 (complemento). Inversões de liderança históricas
- Contar viradas de liderança na ordem de totalização reconstruída (primeira totalização parcial por seção) nos 2º turnos de 2018, 2022 e 2026 (e 2026 T1). 2014: sem horário de totalização no produto de 2014, **NÃO EXECUTADO**; 2002 a 2010: sem dado por seção com horário no catálogo aberto, **NÃO EXECUTADO**.
- Considera-se a liderança medida a partir de 1% das seções totalizadas (antes disso a amostra é pequena demais). Reportar quantas eleições tiveram uma única virada.
- Previsão sem manipulação: o número de viradas observado fica dentro do intervalo das ordens geográficas simuladas em cada ano; uma única virada ocorre quando a margem final é pequena e a região que chega por último favorece o vencedor.

## A14. Recebimento x totalização x divulgação em 25/10/2026
- Alegação: "70% das urnas apuradas às 19h34, liberadas aos poucos"; a captura sugere 7,28%. O vídeo original não foi fornecido a esta sessão; o percentual exibido não pode ser conferido.
- Curvas por minuto: % de BUs recebidos (`DT_RECEBIMENTO_BU_HOR_TSE`) e % com primeira totalização (`DT_PRIM_TOT_PARCIAL_HOR_TSE`), 2026/T2, 2022/T2 e 2026/T1. A curva de divulgação exige snapshots do site Resultados ou registros públicos com horário; se não houver fonte, **NÃO EXECUTADO** para essa curva e para o atraso totalizado a divulgado.
- Sem represamento: totalização acompanha o recebimento com atraso curto e estável (mediana de poucos minutos); sem acúmulo de seções recebidas e não totalizadas. Com represamento: grande parcela recebida muito antes de ser totalizada.
- Documentar a explicação oficial da pausa com fonte (imprensa, se a oficial não abrir).

## A15. Modelo de urna em 2022 (alegação do relatório do PL / Cerimedo)
- Replicar: UE2009 e UE2010 contra UE2020 em 2022, e os modelos de 2026, dentro do mesmo local, em duas especificações: (a) corte transversal, sem controle do T1 (o que a alegação pressupõe); (b) com o voto da seção no T1 como controle. Efeito em votos e em % da margem por ano, com intervalo de 95% normal.
- Sem manipulação: efeito de (a) explicado por composição (modelos antigos em seções com perfil diferente) e efeito de (b) nulo; em 2026, sem diferença por modelo.

## A16. Inventário de alegações
- Página própria com: alegação, quem fez, data, link, testável?, teste usado, resultado, veredito. Alegação sem conteúdo testável: NÃO TESTÁVEL, com o que a tornaria testável. Linguagem neutra, nos termos do autor, sem adjetivos sobre a pessoa. Só entram alegações cujo conteúdo foi fornecido ou tem fonte; as demais ficam como "conteúdo não verificado".

## A17. Questões em aberto
- Entram todo resultado INCONCLUSIVO, "excesso detectável" ou "EXCESSO DETECTADO", e todo resíduo sem causa identificada. Para cada: descrição, direção, estimativa central em votos, intervalo de 95% (aproximação normal sobre o erro padrão do contraste; não é bootstrap), teto de pior caso, % da margem, explicações mundanas testadas e não testadas, e o que resolveria. Soma agregada com intervalo (aproximação por independência, declarada). Proibido atribuir "probabilidade de fraude" ou rótulos como "provável"; probabilidades só sobre quantidades medidas.
