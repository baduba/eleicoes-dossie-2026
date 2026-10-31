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
- O vídeo e os dados das "472 urnas" não foram fornecidos a esta sessão; a alegação é tratada como foi resumida ao autor desta auditoria. Sem os dados e o código dos autores: **NÃO REPRODUZÍVEL** para a parte específica.
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

---

# Adendo 6: PÓS-REGISTRO (Fase 2.1), falhas de desenho de A1, A2, A3 e A12 e testes corrigidos

Escrito em 2026-10-29, **depois** de ver os resultados originais e **antes** de rodar as versões corrigidas. Numeração: o briefing da Fase 2.1 pediu um "Adendo 4 pós-registro"; como o Adendo 4 já era o pré-registro da Fase 2, este é o Adendo 6. **Nada dos resultados originais é alterado ou apagado**: as quatro linhas continuam no registro com o veredito que o critério pré-registrado produziu. As versões corrigidas são publicadas ao lado, com seu próprio veredito, e são rotuladas "pós-registro".

## A1. Curva de apuração
- **Falha de desenho.** O nulo "permutação dentro da UF, mantida a sequência de UFs" supõe que a ordem de chegada das seções dentro de cada UF seja aleatória. Não é: municípios e zonas chegam em blocos. Por isso o critério "sair do envelope por 20 pontos consecutivos" é satisfeito por **qualquer** eleição, e a comparação do desvio máximo com o dos placebos é dominada pelos primeiros 1 a 5% das seções, onde a amostra é pequena e a pausa da divulgação de 2026 alterou a composição do começo da fila.
- **Demonstração (a rodar):** (i) o teste original acusa saída do envelope em 4 de 4 eleições (2018, 2022, 2026 T1 e T2); (ii) em séries **simuladas sem manipulação** (mesma sequência de UFs, municípios em ordem aleatória e contíguos dentro da UF, seções embaralhadas dentro do município), a fração acusada pelo critério original é medida.
- **Teste corrigido.** Nulo D: mantém a sequência de UFs de chegada, embaralha a ordem dos **municípios** dentro de cada UF (blocos contíguos) e as seções dentro do município. Estatística: desvio máximo da curva real contra a mediana de D a partir de 10% das seções (corte fixado agora). Comparação com os placebos pelo mesmo teste de interseção-união.

## A2. Transições T1 para T2
- **Falha de desenho.** O placebo "por papel" (oponente) assume que o oponente se comporta igual em todos os anos. A frequência de perda de votos absolutos depende de quem liderou o 1º turno e de quantos votos de terceiros há para repartir (2014 e 2018: ~26 milhões; 2022 e 2026: 9 a 10 milhões).
- **Demonstração (a rodar):** o teste original aplicado ao **PT de 2022** (que liderou o 1º turno) também acusa excesso contra os demais anos.
- **Teste corrigido.** Compara o **líder do 1º turno** de cada ano, com padronização direta pela razão (votos de terceiros) / (votos do líder) na seção, com os pesos de 2026. Placebos: o líder de 2014, 2018 e 2022.

## A3. Origem dos votos novos de Lula
- **Falha de desenho.** Coeficientes ecológicos "oponente no T1 para PT no T2" são negativos em todos os anos e refletem geografia; a comparação "2026 contra o maior coeficiente dos placebos" acusa excesso no ano de maior coeficiente em **qualquer** conjunto de quatro anos (artefato de ordenação), e o teto em votos derivado não tem sentido causal.
- **Demonstração (a rodar):** o teste original aplicado a cada um dos quatro anos contra os demais (acusa exatamente um: o de maior coeficiente).
- **Teste corrigido.** Taxa de transição oponente para PT estimada com restrição 0 a 1 (mínimos quadrados limitados, ponderados por aptos), intervalo por bootstrap por município (200 réplicas); mesma estimação nos placebos; teto = limite superior do IC95 da taxa x votos do oponente no T1 x 2.

## A12. Seções com zero voto
- **Falha de desenho.** A razão observado/esperado com p estimado pelo 1º turno é enviesada nos anos com terceiros relevantes (2018, 2014: razões de 0,27 a 0,72), e comparar a razão de 2026 com essas razões "acusa excesso" mesmo sem diferença.
- **Demonstração (a rodar):** em 200 simulações **sem manipulação** de 2026 (votos do oponente binomiais com p igual ao do local no próprio 2º turno), a razão pelo estimador do 1º turno e a fração de simulações acusadas pelo teste original.
- **Teste corrigido.** p estimado pelas seções vizinhas do mesmo local no próprio 2º turno (leave-one-out), mesma estimativa nos placebos, comparação por razão e por z direto de 2026.

Veredito das versões corrigidas: regra do Adendo 2, item 4, com Holm sobre as quatro linhas corrigidas.

## Adendo 7: A18 (alteração no meio) e A19 (voto digitado x voto registrado), escrito antes de rodar A18

Registrado em 29/10/2026, antes de qualquer execução do A18. As fontes dos atrasos estão em [A18](a18-alteracao-no-meio.md).

### A18a. Janela de congestionamento no 1º turno de 2026
- **Janela fixada (pelo relógio, a partir da declaração pública):** BUs com `DT_RECEBIMENTO_BU_HOR_TSE` entre 19:00:00 e 19:59:59 do dia da eleição (a imprensa reporta o total nacional parado em 64% por volta das 19h e retomado por volta das 20h).
- **Teste:** coeficiente da janela na participação de Lula (e, simetricamente, do oponente) entre os votos válidos da seção, com **efeito fixo de local de votação**, controlando comparecimento, log dos aptos e minutos de atraso do fechamento. Placebos: a mesma janela de relógio em 2022/T1 e 2018/T1.
- **Previsão sem alteração:** o coeficiente de 2026/T1 fica dentro dos placebos; diferença dentro do local atribuível apenas à composição (a janela seleciona seções por ritmo de transmissão). Excesso apenas se superar **cada** placebo (interseção-união), com Holm sobre a família completa.
- **Robustez (descritiva, fora da família):** mesma estimativa com a janela definida pela defasagem recepção→totalização acima do percentil 90 do dia; contagem de seções com nominais + brancos + nulos diferente do comparecimento, dentro e fora da janela (previsão: zero nos dois grupos).

### A18b. Ordem de recebimento após as 19h no 2º turno de 2026
- **Variável:** t = horas desde 19:00 do recebimento do BU (somente seções recebidas depois das 19:00).
- **Teste:** coeficiente de t na participação de Lula (e do oponente) no 2º turno, com efeito fixo de local, controlando a participação do 1º turno, comparecimento e atraso do fechamento. Placebos: o mesmo t em 2022/T2, 2018/T2 e 2026/T1. Convenção de exposição: efeito de 1 hora de diferença de recebimento sobre os votos válidos das seções recebidas depois das 19:00 (declarada como convenção).
- **Descritivo:** parcela da variância do horário de recebimento explicada por UF e por município em 2026/T2 contra os placebos.
- **Previsão sem alteração:** nenhuma diferença além da composição, isto é, coeficiente de 2026/T2 dentro dos placebos.

### A19. Voto digitado x voto registrado
Sem teste estatístico sobre dados de urna. As tabelas de poder (probabilidade de detectar alteração em 0,1%, 0,5%, 1%, 2%, 5%, 9% das urnas) são cálculo fechado e não entram no registro de testes. Os números do teste de integridade por UF só são publicados quando há fonte; o que não for localizado fica como NÃO EXECUTADO.

## Adendo 8: Fase 3 (A20 a A28, hipóteses adversariais), escrito em 29/10/2026 antes de rodar qualquer teste da fase

Linguagem neutra: cada teste descreve a **classe de falha** que cobre e o **rastro esperado** nos dados públicos, não como produzir a falha. Vale a regra de veredito do Adendo 2. Unidade de todo teto: votos de margem. Os testes de forma não têm teto em votos. Testes que dependem de insumo que não temos são registrados como **NÃO EXECUTADO**, com o insumo e a instrução de como fornecê-lo.

| teste | classe de falha coberta | rastro esperado nos dados | previsão sem manipulação | estado planejado |
|---|---|---|---|---|
| A20 Cadastro | eleitorado apto inflado (inclusão de títulos sem eleitor correspondente) | razão aptos/população 16+ acima de 1 em municípios, excesso entre os mais idosos (80+, 90+, 100+) | fração de municípios com razão > 1 e razão nas faixas 80+, 90+ e 100+ em 2026 dentro do intervalo de 2018 e 2022 (após remover a diferença nacional de nível) | executar (Censo 2022 do IBGE; perfil do eleitorado por zona) |
| A20b perfil das seções novas | seções criadas para receber votos | perfil de idade e sexo de seção nova diferente do das seções antigas do mesmo local | iguais | NÃO EXECUTADO: o perfil público é por zona, não por seção |
| A21 Forense temporal dos logs | registro de votos fora do ritmo da votação real | intervalos entre votos mais curtos, rajadas, concentração na última hora; associação com o voto | padrões iguais em 2022 e 2026, sem associação com o voto (EF de local, controle do T1) | executar só com as medidas já extraídas dos logs (intervalos curtos, primeiro e último voto, votos após o horário nominal); distribuição completa e ano de nascimento NÃO EXECUTADO |
| A22 Coerência entre cargos | desvio uniforme restrito ao cargo de presidente (invisível a testes de outlier) | deslocamento sistemático do resíduo presidente x cargos não presidenciais | resíduo de 2026 igual ao de 2022 e 2018 | NÃO EXECUTADO nesta rodada: falta o mapa de coligações por estado (candidato a governador alinhado a cada candidato presidencial). Desenho fixado abaixo |
| A23 Fiscalização | diferença de comportamento onde há ou não fiscal | seções com fiscal diferem das sem fiscal depois dos controles | sem diferença | NÃO EXECUTADO: sem lista de seções com fiscal |
| A24 Experimento natural do teste de integridade | urna que se comporta diferente quando não é o teste | seções que votaram em urna reserva por causa do teste diferem das vizinhas do mesmo local | sem diferença | NÃO EXECUTADO: a lista de seções afetadas não é pública |
| A25 Urnas substituídas | troca de urna como ponto de intervenção | voto antes e depois da troca; seções com troca diferem das vizinhas | sem diferença | seções com troca x vizinhas já em A6; voto antes x depois pelos logs NÃO EXECUTADO (log da urna original não publicado) |
| A26 Integridade da publicação | arquivo publicado alterado depois | hash atual do arquivo diferente do hash do primeiro download; data de modificação posterior | todos os arquivos idênticos ao primeiro download | executar: hash oficial publicado hoje x hash do primeiro download; tamanho e data atuais; capturas no Wayback Machine |
| A27 Seções fabricadas | seções sem eleitores reais | endereço do local sem estrutura, perfil atípico, histórico do local | seções novas de comparecimento >= 95% explicadas por tipo de local e porte | executar com o que já temos (tipo de local, tamanho, 1º turno); origem das transferências NÃO EXECUTADO |
| A28 Pedidos LAI | dados que só o poder público tem | respostas ou negativas | n/a | redigir e salvar em `lai/`; protocolo e prazo ficam como NÃO EXECUTADO até o autor protocolar |

**A22, desenho fixado (para quando houver o insumo).** Nos estados com 2º turno para governador, por seção: participação do candidato presidencial no 2º turno contra a participação do candidato a governador aliado no mesmo turno, com efeito fixo de UF e controle do 1º turno; estatística: deslocamento médio do resíduo em 2026; placebos: 2022 e 2018 nos mesmos estados com 2º turno. Previsão sem manipulação: deslocamento de 2026 dentro do intervalo dos placebos. Este é o teste para desvio uniforme restrito ao presidente.

**Critério para A20.** Estatística: (i) fração de municípios com aptos > população 16+ (e por faixa); (ii) razão nacional aptos/população por faixa. A população é a do Censo 2022 (IBGE, SIDRA 9514) em todos os anos; por isso 2018 e 2026 usam denominador defasado e a comparação é feita **depois de dividir cada razão municipal pela razão nacional do mesmo ano**. Teste de forma, sem teto em votos; excesso se a fração de 2026 superar a de cada ano de comparação por mais de 2 erros padrão binomiais.

---

## Adendo 9: Fase 3.1 (A20b-idosos, A22, A24, A28), escrito em 29/10/2026 antes de rodar qualquer teste desta fase

O que já foi visto antes deste registro, para transparência: (a) os resultados de A20 do Adendo 8 (aptos 80+ e 90+, razões por faixa, comparecimento por faixa); (b) apenas o **cabeçalho e as colunas** dos arquivos novos (perfil do eleitorado por seção, tabelas de coligações) e a existência dos BWebs de 2018, 2022 e 2026. Nenhum resultado dos testes abaixo foi calculado. Vale o critério de veredito do Adendo 2, item 4, e a unidade "votos de margem" (a favor de um candidato, um voto acrescentado muda a margem em 1; uma troca de voto muda em 2). Teste de forma não tem teto em votos. Todo teto é "teto de pior caso, não estimativa".

**Nome.** O pedido usa o rótulo A20b para o cadastro de idosos. A linha "A20b perfil das seções novas" do Adendo 8 permanece como está (NÃO EXECUTADO na época). Este adendo usa **A20b-idosos** para não colidir com ela.

### A20b-idosos. Cadastro de idosos

**Fontes de insumo (todas públicas).** População do Censo 2022 (IBGE, SIDRA 9514, já em `results/fase3/ibge_pop_9514_2022.csv`); perfil de comparecimento e abstenção por município, zona e faixa etária (TSE; 2018 e 2022 com os dois turnos, 2026 só com o 1º turno publicado até 29/10/2026, última modificação 21/10/2026); perfil do eleitorado por seção (TSE, `perfil_eleitor_secao_{2018,2022,2026}`, com aptos e biometria cadastrada por faixa etária; 2026 gerado em 14/07/2026, 2022 em 26/08/2022).

**1. Regra legal (citação, não teste).** O cancelamento por ausência a três eleições consecutivas está no Código Eleitoral, art. 7º, § 3º (cancelamento da inscrição de quem não vota em três eleições consecutivas, não paga a multa ou não se justifica) e no art. 71, V; a Resolução TSE 23.659/2021, art. 130, conta cada turno como uma eleição (§ 1º) e afasta a regra de quem tem voto facultativo (§ 2º): maiores de 70 anos, analfabetos e eleitores de 16 e 17 anos. O cancelamento por óbito é o art. 71, IV, com a comunicação mensal dos cartórios de Registro Civil (art. 71, § 3º). Consequência para o teste: no voto facultativo a ausência não cancela o título, de modo que **aptos 90+ e 100+ acima do Censo não indicam voto**; só os votantes indicam. Pendência de verificação, declarada: o texto integral da Resolução 23.659 está em site que bloqueia acesso automatizado (403); os parágrafos citados vêm de resumo de busca e precisam ser conferidos no link oficial; o artigo da Resolução que trata de óbito não foi confirmado.

**2. Votantes 90+ e 100+ contra o Censo.** Por município e por ano/turno disponível (2018 T1, T2; 2022 T1, T2; 2026 T1; **2026 T2: NÃO EXECUTADO, perfil não publicado**). Estatísticas: (i) número e fração de municípios com votantes > população da faixa (mínimo de população da faixa: 10 para 90+, 5 para 100+; abaixo disso, o município entra apenas na lista completa, não na fração); (ii) razão nacional votantes/população; (iii) lista dos municípios com votantes > população, com ambos os valores. Para comparar anos, cada razão municipal é dividida pela razão nacional do mesmo ano (mesmo tratamento de A20, porque o Censo é de 2022). Previsão sem manipulação: razão nacional de votantes 100+ abaixo de 1, e fração de municípios com votantes > população em 2026 não superior à de 2022 e 2018 por mais de 2 erros padrão binomiais. Teto de pior caso (não estimativa): soma, nos municípios da lista, de (votantes − população da faixa), todos atribuídos a um candidato, em votos de margem (fator 1); reportado para 2026 T1 e, como referência, para 2022 T1 e 2018 T1. Votantes acima do Censo em 2022 e 2018 mostram quanto disso é diferença de método entre cadastro e Censo.

**3. Biometria por faixa etária.** O perfil de comparecimento **não traz** biometria; o perfil do eleitorado por seção traz **biometria cadastrada**, que não é o mesmo que "liberação manual" no dia (esta vem do BU, por seção, não por idade). Fixo: (3a) fração de aptos com biometria cadastrada por faixa (90+, 100+, 16 a 89) e ano; (3b) por seção e turno, regressão da taxa de liberação manual do BU (`manual_rate`) sobre as frações de aptos 90+ e 100+ da seção, com a fração de aptos **sem biometria cadastrada** da seção como controle e efeito fixo de local de votação; estimada em 2026 T2 e nos placebos 2026 T1, 2022 T2 e 2018 T2. Previsão sem manipulação: o coeficiente de 90+ e 100+ em 2026 T2 não supera o de nenhum placebo (teste de interseção-união, p unilateral de excesso, Holm). Sem teto em votos (teste de forma). A liberação manual por faixa etária **individual** não é observável com dados públicos; (3b) é um proxy ecológico por seção e pode não refletir o comportamento por idade.

**4. Seções com alta fração de aptos 80+.** Fração de aptos 80+ da seção a partir do perfil por seção do mesmo ano. Desfechos (2º turno): participação de Lula e de Flávio nos votos válidos, e comparecimento. Estimador: efeito fixo de local de votação; controles: o mesmo desfecho no 1º turno da seção (e, para a participação, o comparecimento); erro padrão agrupado por local; coeficiente por unidade de fração 80+. Placebos: 2022 T2 e 2018 T2 (mesmo desenho com o perfil por seção do ano), e 2026 T1 só para o comparecimento. Descrição adicional, sem teste: o decil superior da fração 80+ contra o resto, dentro da UF. Previsão sem manipulação: coeficientes de 2026 T2 dentro dos placebos (não os superam). Conversão: participação, expo = Σ (votos válidos × fração 80+) por seção, fator 2; comparecimento, expo = Σ (aptos × fração 80+), fator 1 (todo voto a mais para o mesmo candidato). Os testes entram no registro de A20b-idosos (família própria `_reg_a20b`, Holm dentro dela), sem alterar a família principal.

### A22. Coerência entre cargos (executar)

**Insumo.** Tabelas de coligações do TSE (`consulta_coligacao_{2018,2022,2026}`), com a composição (siglas; federações expandidas para os partidos que as formam), e os BWebs de 2º turno de 2018, 2022 e 2026 (votos por candidato e seção para presidente e governador).

**Regra de alinhamento (fixada agora).** Para cada ano, P_A e P_B são os conjuntos de partidos das coligações presidenciais dos dois candidatos do 2º turno (Lula ou Haddad, e o oponente); Q é o conjunto de partidos da coligação do candidato a governador no 1º turno (ou o partido, se concorreu isolado). Alinhamento a A = |Q ∩ P_A| / |Q|; alinhado a A se > 0,5 e a B < 0,5; simétrico para B; os demais (inclusive sem coligação com partido presidencial) ficam fora e são listados. **Entram só as UFs com 2º turno de governador em que os dois finalistas estão alinhados a candidatos presidenciais diferentes.**

**Estatística.** Por seção, d = participação do candidato do PT (Lula 2026 e 2022, Haddad 2018) nos votos válidos para presidente menos a participação do governador alinhado a ele nos votos válidos para governador (2º turno). S = média de d ponderada por votos válidos, nas UFs elegíveis do ano; erro padrão agrupado por município. S positivo = presidente do PT à frente do governador alinhado. **Placebos:** 2022 e 2018, nas UFs elegíveis do ano (se houver 3 ou mais UFs em comum com 2026, a estimativa de 2026 é recalculada nas UFs em comum e é a principal; senão, cada ano usa as suas UFs). Versão com controle do 1º turno (secundária, fora da família): d regredido em `lula_sh` do 1º turno com efeito fixo de UF, e S ajustado = média, ponderada por votos válidos da UF, dos efeitos fixos avaliados em `lula_sh` do 1º turno = 0,5. Simétrico: o lado do oponente é −S por construção (dois candidatos). Conversão: expo = Σ votos válidos de 2026 nas UFs elegíveis, fator 2. **Previsão sem manipulação:** S de 2026 dentro do intervalo [mín, máx] de S em 2022 e 2018 (teste de interseção-união, p de excesso, Holm). **Limite declarado:** o teste só cobre as UFs com 2º turno de governador com finalistas de alinhamentos opostos; o teto vale **apenas** para esses votos, não para o país.

### A24. Experimento natural do teste de integridade (executar com as UFs disponíveis)

**Insumo.** Lista de seções cujas urnas foram sorteadas para o teste de integridade (e de autenticidade, em coluna separada), montada **a partir das publicações dos TREs**, uma fonte por UF (URL e data de acesso), em `data/a24_secoes_teste_integridade.csv` (UF, município, zona, seção, turno, tipo de teste, com/sem biometria, fonte). Regra de inclusão: só entra seção cuja UF, município, zona e seção estão **escritos na publicação**; resumo de notícia sem a lista não entra. Os sites dos TREs respondem 403 a acesso automatizado; o projeto **não** disfarça o agente para contornar o bloqueio. Se a lista de uma UF não puder ser lida sem isso, a UF fica registrada como NÃO OBTIDA, com o motivo, e o arquivo aceita preenchimento manual com a fonte.

**Teste (fixado).** Para cada seção da lista e turno, comparar com as demais seções do mesmo local de votação que não estão na lista: participação de Lula (votos válidos), comparecimento e taxa de liberação manual, com o mesmo desfecho do 1º turno como controle e efeito fixo de local. Placebos: as mesmas seções no 1º turno de 2026 e no 2º turno de 2022 (a seção existe nos dois anos). Previsão sem manipulação: diferença igual à dos placebos. Conversão: expo = votos válidos nacionais de 2026 T2 (teto de pior caso, extrapolação sem amostragem aleatória, só como limite superior). Poder: o número de seções é pequeno (≈ 20 a 30 por UF e turno); com desvio de 1,67 p.p. por seção, o teste só vê diferenças médias acima de cerca de 1 p.p. com 100 seções; será reportado o menor efeito detectável. Se menos de 10 seções forem obtidas, o teste fica NÃO EXECUTADO (poder insuficiente) e o resultado do levantamento é publicado em `docs/fase3.md`.

### A28. Pedidos LAI (deixar prontos, não protocolar)

Os seis textos permanecem em `lai/`. Entrega desta fase: `lai/canais.csv` com, para cada pedido, o **órgão**, o **canal** (nome, URL), a base normativa do canal e o estado da verificação do canal; e a decisão de **quem recebe cada pedido** (TSE, e os TREs apenas quando só o TRE tem o dado). Canais que não puderem ser verificados porque o site bloqueia acesso automatizado são marcados "a confirmar no protocolo". O projeto não protocola; o registro (`registro.csv`) continua com NÃO PROTOCOLADO até o autor protocolar.

### Adendo 9a: correção de desenho de A20b-idosos, escrita em 29/10/2026 depois do Adendo 9 e ANTES de rodar qualquer teste

**Erro meu no Adendo 9, item 2.** Comparar votantes 90+ e 100+ de 2018 e 2026 com a população 90+ e 100+ do Censo **2022** mistura coortes: quem tem 90+ em 2026 tinha 86+ em 2022 (coorte maior que a do Censo para 90+), e quem tem 90+ em 2018 tinha 94+ em 2022 (coorte menor, só sobreviventes). A normalização pela razão nacional do ano (Adendo 8, A20) corrige o nível, não a forma por município. Por isso:

1. O item 2 permanece como registrado (razão votantes/Censo, fração de municípios com votantes > população, lista, teto), mas **só 2022 compara a mesma coorte**; 2018 e 2026 são reportados com o aviso de descompasso de coortes e **o veredito formal do item 2 não é usado como conclusão**: vale o teste 2a abaixo.
2. **2a. Monotonicidade de coortes (sem Censo).** Uma pessoa não fica mais jovem: o cadastro de 2026 em 95+ só pode vir do cadastro de 2022 em 91+ (4 anos antes), logo está contido no cadastro de 2022 em 90+; e 100+ em 2026 vem de 96+ em 2022, contido em 95+ em 2022. Estatística, por município (e nacional), com T1 de cada ano: R(95+) = aptos 95+ em 2026 / aptos 90+ em 2022; R(100+) = aptos 100+ em 2026 / aptos 95+ em 2022; e as versões com **votantes** no numerador. Placebo: o mesmo par 4 anos antes (2022 contra 2018): aptos 95+ em 2022 / aptos 90+ em 2018, etc. Previsão sem manipulação: R nacional de 2026 não superior à de 2022 por mais de 2 erros padrão (bootstrap por município, 1.000 reamostragens, semente 20261029), e fração de municípios com R > 1 (denominador ≥ 10) de 2026 não superior à de 2022 por mais de 2 erros padrão binomiais. Migração entre municípios pode gerar R > 1 local em qualquer ano; por isso o teste é comparativo. Teto de pior caso (não estimativa): Σ nos municípios com R > 1 de (votantes 2026 no numerador − aptos 2022 no denominador), todos atribuídos a um candidato, em votos de margem (fator 1), com o mesmo cálculo de 2022 contra 2018 ao lado.
3. Os itens 3 e 4 do Adendo 9 não mudam.

### Adendo 9b: desvio declarado em A22, escrito em 29/10/2026 depois de rodar SÓ o alinhamento de 2026 e ANTES de calcular qualquer voto de governador

**O que vi.** Ao rodar a regra de alinhamento do Adendo 9, **nenhuma UF de 2026 ficou elegível**: nas seis UFs com 2º turno de governador (AC, AM, DF, ES, RN, TO) nenhum par de finalistas ficou alinhado a candidatos presidenciais diferentes. Causa vista na composição, sem olhar votos: o oponente do PT concorreu à presidência por partido isolado (coligação de um só partido, PL), de modo que a coligação de um governador raramente tem mais de 50% de partidos em comum com ele; em AM a coligação do candidato do PT tem exatamente 50% (a regra pede mais de 50%). Pela regra registrada, **A22 em 2026 é NÃO EXECUTÁVEL**, e essa é a linha oficial de A22. Nenhum voto de governador foi lido para este desvio.

**Variante 9b (exploratória, fora da família principal).** Regra alternativa fixada agora: o finalista é alinhado ao candidato presidencial X se o **partido de X** está na composição da coligação (ou federação) do finalista, e não está o partido do outro candidato presidencial; entra a UF em que um finalista é alinhado ao PT e o outro ao oponente. Estatística, placebos (2022 e 2018, mesma regra), erro padrão agrupado, conversão em votos e regra de veredito: os do Adendo 9. Espera-se 2 UFs em 2026 (AM e DF, pela composição), o que dá poder muito baixo; o teto será grande por isso, e o veredito provável é INCONCLUSIVA. O resultado da 9b é publicado como **exploratório** e não substitui a linha oficial NÃO EXECUTÁVEL.

### Adendo 9c: esclarecimento de A24, escrito em 29/10/2026 antes de qualquer lista de seções ser lida

Um teste do código com uma lista **sintética** de 80 seções sorteadas ao acaso (descartada; não é dado do projeto) mostrou que comparar uma estimativa **com controle do 1º turno** (2026/T2) contra um placebo **sem** controle (2026/T1) fabrica um falso excesso. O desenho fica assim: o comparador do teste de interseção-união é só **2022/T2 com o mesmo controle do 1º turno**; a diferença do 1º turno de 2026, sem controle, é reportada como **balanço pré-tratamento** e não entra no veredito. Isto corrige o Adendo 9 ("placebos: 2026/T1 e 2022/T2") em A24. Nenhum dado real de A24 existe até agora (nenhuma lista lida).

### Adendo 9d: esclarecimento de A20b-idosos, escrito em 29/10/2026 DEPOIS de ver os resultados do primeiro run

Os resultados do primeiro run (`A20b_testes.csv`) **permanecem como saíram**; o que segue é acrescentado ao lado.

1. **Comparador sem controle em A20b-4, comparecimento.** O Adendo 9 incluiu 2026/T1 como placebo do comparecimento. Esse comparador não tem o controle do 1º turno (não existe um 1º turno anterior ao 1º turno) e é outra especificação que a estimativa principal (2026/T2 com `turnout_t1`). O coeficiente dele é -0,69, contra +0,04 da estimativa principal e ~0 dos placebos controlados; ele vira o "placebo mais frouxo" e produz um teto de 4,07 milhões de votos de margem (91,9% da margem) que vem da diferença de especificação, não dos dados. É o mesmo defeito corrigido em A24 (Adendo 9c). **Linha suplementar, publicada junto, não substitui a original:** comparecimento com só os placebos controlados (2022/T2 e 2018/T2). A linha original continua no registro com seu veredito.
2. **Implementação.** Linhas de A20b-2a sem nenhum município com R > 1 tinham p = NaN (erro padrão zero); passam a p = 1,0 (sem excesso por construção). Não altera as demais linhas.
3. **Leitura de A20b-4 e 3b fixada agora**, antes de escrever a página: os coeficientes de participação (Lula, Flávio) ficam dentro do intervalo dos placebos e o teto de pior caso vem da dispersão entre os anos de comparação, não de um efeito medido; em 3b o coeficiente cresce em todos os anos (0,35; 0,64; 0,71 e 0,80) e o rótulo de excesso é formal, de tendência, sem conversão em votos.

### Adendo 9e: exploração pedida em 29/10/2026 sobre os votantes mais idosos, escrita DEPOIS de ver os resultados de A20b-idosos e ANTES de rodar esta exploração

**Exploratório, fora da família pré-registrada.** Pedido do autor: dar teto em votos de margem e em % da margem para a linha de votantes 95+ (que tem z e Holm), e medir quantos eleitores de cada faixa de idade votaram em 2018, 2022 (última eleição geral do governo anterior ao de 2026, como contexto, sem juízo) e 2026. Fixo agora: (i) tabela de aptos, votantes e comparecimento por faixa (60 a 69, 70 a 79, 80 a 89, 90 a 94, 95 a 99, 100+ e agregados) por ano e turno disponível, e votantes como % da margem; (ii) teto do teste de votantes 95+ = (diferença de razão entre 2026 e 2022 + 1,645 erro padrão) x aptos 90+ de 2022 nos municípios do teste, **fator 1** (um votante a mais, se fosse de um só candidato, muda a margem em 1); estimativa central = diferença de razão x denominador. Teto de pior caso, não estimativa. Os votantes não têm idade nem voto associados nos dados públicos; a tabela **não** diz em quem votaram.

## Adendo 10: A31, municípios extremos na transferência T1 -> T2 (alegação Silva Jardim/RJ), escrito em 29/10/2026 ANTES de calcular qualquer estatística do teste

**Declaração de ordem.** Antes deste adendo só conferi, sem olhar resultado, que o BWeb por seção cobre 2014, 2018, 2022 e 2026 (T1 e T2), que Silva Jardim/RJ é o município 59110 do TSE e que 2026 tem 5.571 chaves (UF, município) onde os outros anos têm 5.570 (a diferença é investigada e registrada no script, não escolhida). Nenhum voto de Silva Jardim, nenhuma fração f e nenhum resíduo foi calculado.

**Alegação.** Em Silva Jardim, no 2º turno de 2026 contra o 1º, "Flávio +1, Lula +964, -104 eleitores" seria impossível sem manipulação. Este teste (i) confere se os números reproduzem, (ii) coloca o município na distribuição de todos os municípios em quatro eleições e (iii) usa um modelo nulo que respeita a heterogeneidade entre municípios, em vez de moedas independentes.

**Definições (por município, soma das seções do BWeb, exterior fora).** PT = candidato do PT (Lula em 2026, 2022; Haddad em 2018; Dilma em 2014), OPO = finalista oposto (Flávio, Bolsonaro, Bolsonaro, Aécio). dL = PT(T2) - PT(T1); dF = OPO(T2) - OPO(T1). Terceiros(T1) = votos nominais do T1 menos PT e OPO. BN = brancos + nulos. dC = comparecimento(T2) - comparecimento(T1). **Estoque** E = Terceiros(T1) + BN(T1) + dC. **Pool** P = dL + dF, que pela identidade da Fase 2 (A3/A11) é igual a E - BN(T2); a identidade é verificada município a município e o script para se falhar. **Fração capturada pelo PT** f = dL / P, definida para P >= 20 (municípios com P < 20 ou P <= 0 ficam fora e são contados). f pode sair de [0, 1] quando um candidato perde votos entre os turnos; isso é mantido, não truncado.

**Parte 1: conferência da alegação (Silva Jardim).** Tabela com T1 e T2: aptos, comparecimento, PT, OPO, cada terceiro, brancos, nulos, e as diferenças dL, dF, dC, d(aptos), d(BN). Registrar se "+1, +964, -104" reproduz e **o que é o -104** (dC, d(aptos) ou outra grandeza); se nenhuma grandeza dá -104 isso é dito.

**Parte 2: distribuição e posição.** Para 2026, 2022, 2018 e 2014: distribuição de f (decis, mínimo, máximo, fração fora de [0, 1]) e a posição (percentil e valor) de Silva Jardim em cada ano.

**Parte 3: modelo nulo (hipótese nula = comportamento típico dos municípios com o mesmo perfil de 1º turno).**
1. Regressão ponderada, por ano, f_i = alfa_UF + soma(beta_j x perfil_ji) + e_i, com efeito fixo de UF (27) e perfil só do **1º turno**, em fração do comparecimento do T1: PT, OPO, brancos e nulos, abstenção (1 - comparecimento/aptos) e a composição dos terceiros. Composição dos terceiros: 2026, os blocos de A11 (pró-Flávio = Zema, Caiado, Cury, Clariana; Renan Santos; demais); 2022 e 2018, o maior terceiro, o segundo maior e os demais (sem inferir apoios, como em A11); 2014, só o total de terceiros (o arquivo por candidato do T1 de 2014 não está no projeto). **A variação de comparecimento T1->T2 não entra** no perfil: é desfecho do 2º turno e, se houvesse anomalia, poderia ser absorvida por ele.
2. Variância: Var(f_i) = f_hat(1 - f_hat)/P_i + tau2, com f_hat cortado em [0,02; 0,98]. tau2 (heterogeneidade real entre municípios, que o modelo de moedas não tem) é escolhido por bissecção para que a escala robusta (1,4826 x MAD) do resíduo padronizado z_i = e_i / dp_i seja 1. Pesos 1/Var, 20 iterações.
3. Cauda: **t de Student** com os graus de liberdade estimados por máxima verossimilhança sobre os z dos **três outros anos** (cada ano é comparado com os outros três; escala 1 após a calibração). p bilateral, correção de **Holm** para o número de municípios elegíveis do ano e, em linha separada, para **5.570** comparações (a cifra do pedido).
4. **Precedente empírico**: para cada município sinalizado, quantos municípios dos outros três anos têm |z| >= o dele.
5. **Veredito para Silva Jardim em 2026 (fixado agora):** DENTRO DA CAUDA ESPERADA se o p de Holm >= 0,05; FORA DA CAUDA DO MODELO, COM PRECEDENTE se p de Holm < 0,05 e algum outro ano tem município com |z| >= o dele; FORA DA CAUDA, SEM PRECEDENTE se p de Holm < 0,05 e nenhum outro ano tem. **Previsão sem manipulação: DENTRO DA CAUDA ESPERADA.** Rótulo: "fora da cauda" mede forma, não manipulação.
6. **Teto em votos de margem (teto de pior caso, não estimativa), fator 2** (um voto do pool atribuído ao PT que seria do OPO muda a margem em 2): (a) por município, 2 x P x max(0, |f - f_hat| - zc x dp), com zc o valor crítico de Holm do item 3, ou seja, só o que passa da cauda esperada; (b) incondicional, 2 x P x |f - f_hat|, tudo o que o modelo não explica, atribuído a manipulação. Somados para Silva Jardim e para os 20 mais extremos, em votos e em % da margem (4.430.191).

**Parte 4: demonstração do modelo de moedas independentes.** Cada eleitor do pool vai ao PT com probabilidade p0, independente dos demais. Três variantes de p0: 0,5; a razão PT/(PT+OPO) do próprio município no T1; a razão nacional do T1. Estatística: z_moeda = (dL - p0 P)/raiz(P p0 (1-p0)) no total nacional de cada ano e município a município. Reportar o z nacional, o p e, por município, a fração rejeitada com Holm em 0,05. **Previsão:** o modelo de moedas rejeita o resultado nacional de **todas** as eleições, 2022 inclusa, e rejeita fração grande dos municípios em todos os anos; isso o desqualifica como referência, porque rejeita o que nenhuma parte contesta como impossível. (Isto mostra que o critério é inadequado; não valida nem invalida o resultado de nenhuma eleição.) Também é calculado o que a alegação implica pelo modelo de moedas para Silva Jardim (probabilidade de dF <= o observado dado P), para mostrar a ordem de grandeza que esse modelo atribuiria.

**Parte 5: os 20 municípios mais extremos de 2026 (maior |z|, qualquer direção, entre os elegíveis).** Para cada um: f, z, p de Holm, P, f_hat; decomposição por seção: número de seções, fatia das 3 seções com maior dL no dL total (C3_dL) contra a fatia das 3 seções com maior pool no pool total (C3_P), fração de seções com f_s do mesmo lado que o município; terceiro dominante do T1 (maior entre os que não são PT/OPO), sua fatia do comparecimento e **apoio declarado** (classificação já documentada em `docs/resultados-fase2.md`, A11, com fontes; 2026 apenas); e a **mesma conta em 2022**: f e z do município em 2022 e se estava entre os 5% mais extremos. Regra de concentração fixada agora: "ganho concentrado" se C3_dL > 0,5 e C3_dL > 1,5 x C3_P; senão "espalhado".

**Parte 6: Silva Jardim, conferência com boletins impressos.** `results/fase3/A31_silva_jardim_secoes.csv`: todas as seções, com aptos, comparecimento, PT, OPO, cada terceiro, brancos e nulos de T1 e T2, nas colunas de `scripts/04_cruza_bu_impresso.py`, mais colunas vazias para o valor impresso, para quem coletar o BU (diretórios locais e fiscais, pela página `boletins-impressos`). O projeto não tem BU impresso de Silva Jardim; essa conferência fica NÃO EXECUTADA até alguém fornecer BUs.

**Previsão sem manipulação (conjunta).** Silva Jardim dentro da cauda esperada após a correção; ganho espalhado entre as seções; explicado pelo perfil do 1º turno (f_hat próximo de f). Se isso falhar, o resultado sai como saiu.

**O que este teste não faz.** Não identifica em quem cada eleitor votou; não prova nem descarta manipulação em nenhum município; o veredito vale para a forma da distribuição entre municípios. Cada teto é teto de pior caso, não estimativa.

### Adendo 10a: município-ano com seção apurada em um turno e não no outro, escrito em 29/10/2026 depois da primeira execução parar na verificação da identidade e ANTES de qualquer estatística do teste

**O que vi.** A verificação P = E - BN(T2) do Adendo 10 parou em 2018, em 1 município (BA, código TSE 38490). Causa, vista nos dados brutos e sem calcular f: no T1 de 2018 duas seções desse município têm tipo "Anulada e apurada em separado", com comparecimento registrado (363 e 383) e votos zerados; no T2 as mesmas seções foram apuradas. Entram no pool do município 746 votos que não existem no T1, o que quebra a identidade e inflaria dL e P naquele município. Isto vale para qualquer seção com status de apuração diferente entre os turnos, mesmo quando a identidade passa por acaso (por exemplo, comparecimento zero nas duas pontas).

**Regra acrescentada (vale para os quatro anos, fixada agora).** Um município-ano fica **fora** do teste se alguma seção (pareada pela chave UF, município, zona, seção) tem tipo de urna diferente entre T1 e T2, ou existe só em um dos turnos. Seções "Não instalada" nos dois turnos, com tudo zero, não distorcem e permanecem. Os municípios excluídos por essa regra são listados em `results/fase3/A31_excluidos.csv`, com o motivo. A identidade continua obrigatória para todos os demais: se falhar, o script para. O número de excluídos entra no texto da página.

### Adendo 10b: análise suplementar pós-hoc de A31, escrita em 29/10/2026 DEPOIS de ver o resultado do modelo principal e ANTES de rodar a suplementar

**O que o modelo principal mostrou (fica como saiu).** Silva Jardim: z = 1,13, p de Holm = 1, DENTRO DA CAUDA ESPERADA. Mas a cauda estimada é muito pesada (t de Student com cerca de 2,4 a 2,8 graus de liberdade nos quatro anos), e o valor crítico de Bonferroni para 5.570 comparações fica em |z| de 83 a 135. Causa vista no resultado: f = dL / (dL + dF) é instável quando o pool é pequeno e os fluxos brutos são grandes e de sinais opostos (por exemplo, dL = +1.114 e dF = -1.059 com pool de 55), e a variância binomial pressupõe f em [0, 1]. **O teste principal quase não tem poder para rejeitar municípios pequenos.** Isso não muda o veredito de Silva Jardim (|z| de 1,13 é comum sob qualquer referência), mas muda o que se pode dizer dos outros 19 extremos, e é declarado na página.

**Suplementar S1 (exploratória, fora do veredito).** Estatística bem condicionada: yL = dL / aptos(T1) e yF = dF / aptos(T1), cada uma regredida (mínimos quadrados ponderados por aptos do T1) nos mesmos regressores do 1º turno e efeito fixo de UF do modelo principal. Resíduo padronizado pela escala robusta (1,4826 x MAD) dentro de decis de aptos do T1 do ano. Cauda: t de Student com df estimado nos três outros anos, como no principal. Reportar para Silva Jardim nos quatro anos (zL, zF, p, p de Holm) e, em 2026, os 10 maiores |zL| e os 10 maiores |zF|, com o teto em votos de margem (fator 2) da parte que passa do valor crítico de Bonferroni de 5.570 comparações. Leitura fixada agora: Silva Jardim é dito "comum na estatística suplementar" se os dois p de Holm forem >= 0,05.

**Suplementar S2 (descritiva).** Número e % de municípios com dF <= 1 (o oponente não ganhou mais que 1 voto entre os turnos) em cada ano, entre todos os elegíveis e entre os que têm dL >= 500; e quantos tiveram dL >= 900 junto com dF <= 1.

**Suplementar S3 (descritiva).** Coluna `fluxo_bruto_sobre_P` = (|dL| + |dF|) / |P| nos 20 mais extremos do modelo principal, para mostrar quais dos extremos vêm de pool pequeno com fluxos brutos grandes.

**Divulgação.** Estas linhas são marcadas "pós-hoc, exploratória" na página e não substituem a linha principal.

## Adendo 11: A32, liberação manual como canal de abuso local, escrito em 29/10/2026 ANTES de ler qualquer log novo ou calcular qualquer estatística de A32

**Declaração de ordem.** O que eu já tinha visto antes deste adendo: (i) o resultado de A21 (intervalos curtos entre habilitações, horário do último voto, associação com o voto, na amostra de seções), (ii) o resultado de H1, H2 e A20b-3b (taxa de liberação manual por seção, BWeb), (iii) o formato do log de uma urna de Roraima (mensagens "Eleitor foi habilitado", "Tipo de habilitação do eleitor [biométrica]", "Solicitação de dado pessoal do eleitor para habilitação manual", "Mesário ... habilitou o eleitor"). Não vi nenhuma contagem de rajadas, nenhuma fração de liberação manual na última hora e nenhuma seção com liberação manual extrema por idade.

**Unidade e fontes.** Seção-dia (cada seção, em 2022 e 2026, T1 e T2). Fonte da liberação manual por seção: (a) BWeb, `biom_nh / comparecimento` (taxa já usada em H1, H2 e A20b), todas as seções, 2022 e 2026, T1 e T2; (b) log da urna, por habilitação, na amostra de seções já definida em A4/A5/A21 e em todas as seções de Roraima. **O log do 2º turno contém os eventos dos dois dias** (o do 1º turno traz data de 04/10/2026 e 02/10/2022 no arquivo do 2º turno): cada log lido fornece T1 e T2 da mesma urna, e a seção é marcada quando o número de habilitações do log não fecha com o comparecimento do BU. **NÃO EXECUTADO:** os logs de todas as seções nos dois anos (cerca de 1 milhão de arquivos; os zips públicos por UF pesam dezenas de GB cada). A cobertura é declarada como a de A24 ("N seções de 499.205, parcial").

**Item 1: A21 completo (logs).**
1. **Ano de nascimento: NÃO EXECUTÁVEL.** O log não registra a data de nascimento nem o identificador do eleitor em forma útil, e o projeto **não extrai nem guarda** título, CPF ou identificação de mesário (dados pessoais). A sequência temporal é por **tipo** de habilitação (biométrica ou manual) e por horário.
2. **Evento.** Habilitação = linha "Eleitor foi habilitado". Tipo: **manual** se, entre a habilitação anterior e esta, há "Solicitação de dado pessoal do eleitor para habilitação manual" e "habilitou o eleitor"; **biométrica** se há "Tipo de habilitação do eleitor [biométrica]"; **outra** nos demais casos (reportada, não descartada).
3. **Rajada.** k ou mais habilitações **manuais consecutivas** (nenhuma biométrica no meio) em que cada intervalo entre habilitações consecutivas é menor que o **percentil 5 dos intervalos da própria seção-dia** (todos os intervalos entre habilitações consecutivas da seção no dia). k = 3 (principal) e k = 5 (sensibilidade). Seção-dia com menos de 100 habilitações não entra no teste de rajadas (p5 instável); entra nas demais medidas. Medidas por seção-dia: número de rajadas, fração das habilitações manuais dentro de rajadas, **fração das habilitações manuais na última hora** (60 minutos antes do fechamento nominal) e, ao lado, a fração de **todas** as habilitações na última hora (referência).
4. **Associação com comparecimento e voto.** Modelos por seção, efeito fixo de local de votação, erro padrão agrupado por local (`fe_ols`/`Registro` de `lib_auditoria.py`): (M1) comparecimento do T2 ~ indicador de rajada no T2 + comparecimento do T1; (M2) participação de Lula (votos válidos) no T2 ~ indicador de rajada no T2 + participação no T1; (M3) variação do comparecimento 2022 -> 2026 (T2) ~ indicador de rajada de 2026, nas seções que existem nos dois anos. Placebo de cada M1 e M2: a mesma regressão em 2022. Veredito pelas regras já usadas (interseção-união contra os placebos, Holm sobre a família de A32, teto de pior caso em votos de margem, fator 2 para participação de Lula e fator 1 para comparecimento, exposição = votos válidos ou aptos do T2). A comparação de **frequência** de seções com rajada entre 2026 e 2022 é feita nas mesmas seções, com efeito fixo de seção e erro padrão agrupado por município.
5. **Previsão com abuso:** rajadas concentradas no fim do dia (fração manual na última hora acima da fração de todas as habilitações na última hora), em seções com salto de comparecimento, e mais frequentes em 2026 do que em 2022. **Sem abuso:** mesma frequência nos dois anos e sem associação com o comparecimento ou com o voto. Critério objetivo: o veredito de cada linha da família de A32 e o sinal e a ordem de grandeza da diferença de frequência.

**Item 2: seções com liberação manual extrema (BWeb, todas as seções).** Extremas: taxa manual > 30% e > 50% dos votantes (duas linhas de corte, com comparecimento >= 30). Para 2022 e 2026, T1 e T2: contagem, por UF, tipo de local (a mesma classificação de A27), idade média do eleitorado da seção (pontos médios das faixas do perfil do eleitorado por seção, 100+ = 102; seção sem perfil fica fora e é contada), comparecimento e participação de Lula **contra as demais seções do mesmo local** (diferença média dentro do local, controle da mesma medida no T1 no T2).

**Item 3: teto em votos de margem.** Modelo da taxa manual do T2 **ajustado em 2022** (mínimos quadrados ponderados por votantes), regressores: fração dos aptos por faixa etária do perfil da seção (agrupadas em 16 a 29, 30 a 44, 45 a 59, 60 a 69, 70 a 79, 80 ou mais), fração com biometria cadastrada e efeito fixo de UF; aplicado às seções de 2026 com os coeficientes de 2022. Excesso da seção = max(0, manual observado - manual previsto) em votantes. **Teto de pior caso, não estimativa (fator 1):** soma dos excessos em votos de margem, supondo todos a favor de um só lado; e, ao lado, (a) a mesma soma para 2022 dentro da amostra (referência: o quanto o modelo erra para cima em um ano sem a hipótese), (b) o excesso além de 1,645 desvio padrão do resíduo de 2022 (a parte que o ruído do modelo não explica) e (c) o excesso depois de remover o deslocamento nacional (mediana do resíduo). Os cinco números são publicados; o teto é o maior deles e é rotulado como tal.

**Item 4: integridade dos logs.** Registrar, na amostra lida, a fração de seções cujo hash do log consta da lista assinada pela urna (A4) em 2022 e em 2026, e que a **verificação da assinatura** (pendente, A18/A29) é o que fecha a hipótese de alteração do log depois da urna; enquanto pendente, o resultado vale como "o log é o que a urna listou", não como "o log é autêntico".

**Item 5: documentos em papel.** Redigir (i) pedido LAI e (ii) modelo de requerimento para partidos, pedindo, para as 50 seções com maior excesso de liberação manual em 2026 T2 (item 3; seções com rajada entram se o item 1 as achar, e a lista final traz o critério de cada uma), cópia da ata da mesa receptora e da folha ou caderno de votação. **Teste fixado** (a executar quando houver os documentos; **NÃO EXECUTADO** até lá): assinaturas e votantes da ata x comparecimento do BU x habilitações do log; script de conferência `scripts/37_confere_ata.py` com entrada em CSV. Nenhum pedido é protocolado pelo projeto.

**O que A32 não faz.** Não identifica eleitores nem mesários; a liberação manual tem usos legítimos (digital não reconhecida, eleitor sem biometria, idoso); o excesso sobre o modelo de idade não é fraude, é só o que o modelo de 2022 não prevê.

## Adendo 12: A12b, alegação "106 urnas com 100% para Lula e 0% de brancos, nulos e Flávio", escrito em 29/10/2026 ANTES de calcular as probabilidades

**Declaração de ordem.** A12 já publicou as contagens de seções com zero voto para o oponente (106 em 2026/T2 pela definição "todas as apuradas", 81 no T1; 143, 328 e 192 em 2022, 2018 e 2014 no T2) e a lista das 106 seções (`A12_a12_secoes_zero_2026.csv`). **Não vi** quantas dessas 106 também têm zero branco e zero nulo, nem o esperado dessa coincidência.

**Definições.** Universo: seções apuradas, exterior incluído (a definição que dá 106 em A12). **Zero oponente** = votos de Flávio (Bolsonaro, Aécio) = 0. **Zero BN** = brancos = 0 e nulos = 0. **Tripla zero** = os dois.

**Esperado.** Para cada seção com zero oponente, a probabilidade de zero brancos e nulos dado o comparecimento n e a taxa de brancos e nulos r das **outras seções do mesmo local de votação** (se o local tem só uma seção, as do município): p0 = (1 - r)^n. Variante de sensibilidade: r do município inteiro. Esperado = soma de p0; observado = contagem de tripla zero; p exato pela distribuição Poisson-binomial (cauda superior). A mesma conta para a série 2014, 2018, 2022 e 2026 (T1 e T2). **Previsão sem manipulação:** o observado fica próximo do esperado. Observação de desenho: seções com zero voto para o oponente são seções pequenas ou muito unânimes; por isso o esperado usa o comparecimento da própria seção, não uma taxa geral.

**Para cada uma das 106:** UF, município, tipo de local, aptos, comparecimento, votos de Lula, brancos, nulos, resultado no T1/2026 e na mesma seção em 2022 (T2 e T1); lista em `results/fase3/A12b_106_secoes.csv`.

**Teto em votos de margem (teto de pior caso, não estimativa).** (i) Se todos os votos de Lula nessas 106 seções fossem inválidos (como em A27): soma dos votos de Lula, fator 1. (ii) Se esses votos fossem trocados: votos esperados do oponente nessas seções pela participação do oponente nas outras seções do local (T2) x votos válidos, fator 2. Os dois são publicados, nenhum é estimativa.

**Inventário de alegações.** Nova linha: a imagem afirma "0% de brancos e nulos" e 106 urnas; o relatório original dizia "100% dos votos válidos" para seções unânimes (com pelo menos 30 votos válidos; 103 do PT em 2026 T2 pela contagem do relatório original, A12/H). A diferença é registrada: 100% dos válidos admite brancos e nulos acima de zero; "0% de brancos e nulos" é afirmação mais forte; e 106 (zero oponente, qualquer tamanho) não é o mesmo conjunto que 103 (unânimes com pelo menos 30 válidos).

### Adendo 11a: acréscimos de A32 escritos em 29/10/2026 depois de validar o extrator de logs e ANTES de calcular qualquer rajada ou fração na última hora

**O que vi.** Só a validação do extrator em Roraima 2026: o número de habilitações do log fecha com o comparecimento do BU em 97,8% das seções, e a fração manual do log tem correlação 0,994 com `manual_rate` do BWeb (4,18% contra 4,14%). Nenhuma rajada foi contada.

1. **Base de comparação por permutação (nova, para as rajadas).** Em cada seção-dia, os rótulos de tipo (M, B, O) são embaralhados mantendo os horários e a contagem de cada tipo (200 permutações, semente 20261029); o esperado de rajadas e a probabilidade de pelo menos uma rajada vêm dessa distribuição. Motivo: com poucas liberações manuais, rajadas por acaso dependem do número de manuais; a razão observado/esperado é a medida comparável entre anos. A frequência bruta continua publicada ao lado.
2. **Seleção da amostra.** A amostra de seções de A4/A5/A21 é estratificada (L: fechamento tardio; C: controle do mesmo local; H: comparecimento de 95% ou mais; R: aleatória de 60 por UF), mais **todas** as seções de Roraima. Os modelos M1 e M2 de A32 usam a amostra por estrato com um problema de seleção no desfecho (H escolhe seções pelo comparecimento). **Principal:** estrato R mais Roraima inteira (seleção independente do desfecho). **Sensibilidade:** todos os estratos, rotulada "seleção no desfecho".
3. **Consistência do log.** Seção-dia entra nos modelos se o número de habilitações do log está a até 5% do comparecimento do BU e tem pelo menos 100 habilitações; as demais ficam em tabela à parte.
4. **M3 (variação 2022 -> 2026 do comparecimento)** não tem placebo (não há um segundo par de eleições com logs); é **descritiva** (coeficiente e erro padrão), fora da família com Holm.
5. **Dia 1 (1º turno).** As mesmas medidas são calculadas para o 1º turno (o log do 2º turno traz os dois dias) e publicadas como descritivas; os modelos de associação usam o 2º turno (o que decide a margem) e o 1º turno como controle.

### Adendo 11b: forma de calcular o esperado por permutação, escrita em 29/10/2026 ANTES de calcular qualquer rajada

O esperado do Adendo 11a (permutar os rótulos de tipo mantendo horários e contagens) é calculado em **forma exata**, não por 200 sorteios: dentro de cada cadeia de habilitações consecutivas ligadas por intervalos menores que o p5 da seção-dia (comprimento Lc), o número esperado de rajadas de k ou mais é a soma, sobre as posições de início, de f(k) (início da cadeia) ou f(k) - f(k+1) (demais posições), com f(s) = produto de (m - i)/(n - i), i de 0 a s-1, para m manuais em n habilitações. Isto é a esperança sobre todas as permutações. A probabilidade de pelo menos uma rajada é aproximada por 1 - exp(-esperado) (aproximação de Poisson, declarada). Nada muda no resto do desenho.

### Adendo 11c: leitura do teto de A32 (item 3), escrita em 29/10/2026 DEPOIS de ver o resultado do item 3 e ANTES de rodar o item 1 (rajadas)

**O que vi.** O modelo de 2022 prevê **mais** liberação manual em 2026 (11,6 milhões de votantes) do que a observada (8,63 milhões): a taxa manual caiu, e a mediana do resíduo é -2,7 pontos percentuais. A variante "(c) depois de remover o deslocamento nacional" do Adendo 11, escrita pensando num deslocamento para cima, **soma 2,7 pontos a cada seção** quando o deslocamento é para baixo, e vira o maior dos quatro números (1,85 milhão de votos de margem, 41,8% da margem) por construção, não por excesso real. A regra registrada ("o teto é o maior dos números") é cumprida e esse valor é publicado como o teto registrado; **ao lado**, com rótulo "leitura posterior ao resultado", entram: (a) soma dos excessos positivos, (b) além de 1,645 desvio padrão do resíduo de 2022 e (d) a mesma soma de (a) para 2022 dentro da amostra. A variante com deslocamento só tem sentido quando o deslocamento é positivo; em 2026 não é. Nada nas linhas registradas é alterado.

### Adendo 11d: medida suplementar de A32 (item 1), escrita em 29/10/2026 DEPOIS de ver o resultado das rajadas registradas e ANTES de rodar a suplementar

**O que vi.** Com a definição registrada (k ou mais liberações manuais consecutivas com todos os intervalos abaixo do percentil 5 dos intervalos da própria seção), **nenhuma seção-dia tem rajada**, em nenhum ano, dia ou k (3 ou 5), em cerca de 13 mil seções-dia por ano e dia, com esperado por permutação de 0,03% a 0,1% das seções. Sem variação, os modelos de associação com comparecimento e voto **não são estimáveis** (NÃO EXECUTÁVEL, linha oficial) e a diferença de frequência entre anos é 0 contra 0. A fração das liberações manuais na última hora é **menor** que a fração de todas as habilitações na última hora nos dois anos. Fica como o resultado registrado.

**Por quê.** Uma liberação manual exige digitar um dado do eleitor e a biometria do mesário; leva dezenas de segundos, e o p5 dos intervalos de todas as habilitações da seção fica abaixo disso. A definição registrada não consegue detectar rajadas por construção, e isso é dito.

**Medida suplementar (pós-hoc, exploratória, fora do Holm da família principal).** **Agrupamento de liberações manuais, sem condição de tempo:** sequência de k ou mais habilitações manuais consecutivas, sem habilitação biométrica no meio (k = 3 e 5), com o esperado exato por permutação (o mesmo cálculo do Adendo 11b, com todos os intervalos considerados ligados). Mede se as manuais se juntam em blocos em ordem de chegada mais do que o acaso. Também são publicados os quantis do intervalo que **precede** cada habilitação manual e cada biométrica (agregado por ano, sem identificar seção), para mostrar a duração típica de cada tipo. Modelos de associação (M1, M2, M3, frequência 2026 contra 2022) repetidos com o indicador "pelo menos um agrupamento de k = 5" (e k = 3 como sensibilidade), em família separada "A32-sup" com Holm próprio, rotulada pós-hoc.

## Adendo 13: A31b, os municípios com dFlávio <= +1, escrito em 29/10/2026 ANTES de rodar qualquer simulação ou perfil desta etapa

**Declaração de ordem.** Já vi, em A31 (S2), que 748 de 5.357 municípios elegíveis (14,0%) de 2026 têm o ganho do oponente entre os turnos menor ou igual a +1, contra 0,15% (2022), 1,6% (2018) e 1,2% (2014). Não vi o perfil desses 748 (UF, região, porte, composição do 1º turno, comparecimento, liberação manual, modelo de urna), nem a simulação abaixo, nem a decomposição por variação de comparecimento.

**Universo.** Os municípios elegíveis de 2026 (pool T1 -> T2 de pelo menos 20 votos, A31) com dF <= 1 (dF = voto do oponente no T2 menos no T1).

**1. Fração esperada sob o deslocamento nacional.** Para cada ano de comparação y (2022, 2018, 2014): g(i,y) = dF(i,y) / voto do oponente no T1 (i,y), por município. G(UF,y) = soma de dF / soma do voto do oponente no T1 nos municípios elegíveis da UF no ano y, e G(UF,2026) o mesmo em 2026. Deslocamento por UF: d(UF,y) = G(UF,2026) - G(UF,y) (aditivo). **Simulação principal (pareada):** para cada município elegível de 2026 que existe no ano y, dF' = (g(i,y) + d(UF,y)) x voto do oponente no T1 de 2026 do município; fração esperada = proporção com dF' <= 1 entre esses municípios. **Sensibilidade (reamostragem):** para cada município de 2026, sorteia-se g de um município do mesmo ano y e da mesma UF (200 sorteios, semente 20261029), soma-se d(UF,y), e calcula-se a fração; reporta-se média e intervalo de 2,5% a 97,5%. **Comparação:** a fração observada (14,0%) contra as três frações esperadas e os intervalos. **Previsão sem anomalia:** a fração observada fica dentro do intervalo dos esperados (do menor ao maior dos três anos, ou dentro de um dos intervalos da reamostragem); acima de todos = ACIMA DO ESPERADO; abaixo de todos = ABAIXO. Limitação declarada: o deslocamento só iguala o crescimento médio por UF; ele não reproduz a forma da distribuição de 2026.

**2. Perfil.** Para os 748 e para os demais elegíveis: UF e região (IBGE; UF -> região), porte (aptos do T1: até 5 mil, 5 a 20 mil, 20 a 100 mil, mais de 100 mil), fatia do oponente e de terceiros no comparecimento do T1, variação do comparecimento T1 -> T2 (% do comparecimento do T1), taxa de liberação manual do 2º turno (BWeb, municipal ponderada), fração de seções por modelo de urna (UE2009 a UE2022). Comparação por razão (fração do grupo / fração dos demais) em categorias e por mediana nas medidas contínuas. **Descritivo, confundido por região e porte; nenhum valor-p é a conclusão.**

**3. Decomposição.** Entre os 748: (a) comparecimento caiu (dC < 0), compatível com abstenção seletiva; (b) comparecimento subiu ou ficou igual (dC >= 0), em que o oponente parado exigiria novos votantes irem ao PT ou troca de voto. Limite inferior de troca de voto por balanço líquido: S(i) = max(0, -dF - max(0, -dC) - max(0, BN(T2) - BN(T1))), o quanto da perda do oponente **não** cabe em queda líquida de comparecimento nem em aumento de brancos e nulos; contagem e soma. **O balanço líquido não distingue troca de voto de abstenção seletiva** (um eleitor do oponente que se abstém e um novo eleitor do PT cancelam no líquido); a frase vai no cartão.

**4. Os 20 com maior perda absoluta do oponente** (dF mais negativo entre todos os municípios de 2026, com comparecimento de pelo menos 1.000 no T1): lista de **todas as seções** com T1 e T2 e colunas vazias para o BU impresso (formato de `04_cruza_bu_impresso.py`), em `results/fase3/A31b_20_secoes.csv`.

**5. Teto em votos de margem (teto de pior caso, não estimativa), fator 2.** (A) Soma, nos 748, de max(0, G(UF,2026) x voto do oponente no T1 - dF), supondo tudo troca de voto. (B) Excesso de (A) sobre a média de (A) nas simulações pareadas dos três anos (piso zero): a parte da falta de ganho que o deslocamento nacional não reproduz. Os dois são publicados; o que entra no gráfico G3 é (B) (regra de exibição do Adendo 14, abaixo).

**Cartão** na primeira página, bloco a, com o teto (B) e a frase "não distingue troca de voto de abstenção seletiva".

**Município TSE 73709.** Conferência de nome e data de instalação, registrada no CHANGELOG com as fontes: a tabela de municípios do TSE usada em A20 dá BOA ESPERANÇA DO NORTE; as 13 seções de 2026 têm 5 seções que em 2022 eram de Sorriso, 4 de Nova Ubiratã e 4 novas; data de instalação por fonte secundária, a conferir em fonte oficial.

## Adendo 14: A32b (rajadas com limiar absoluto) e regra de exibição do G3, escritos em 29/10/2026 ANTES de rodar A32b

**Regra de exibição (G3).** O gráfico G3 não plota tetos inflados por construção. Para A32, a barra é o excesso **além do ruído do modelo de 2022** (55.862 votos de margem); o teto registrado de 1.852.233 (Adendo 11c) aparece **só como texto**, com a referência ao Adendo 11c. Regra geral: quando um teto registrado é mecanicamente inflado, o gráfico mostra a variante corrigida e o texto traz a registrada, com o motivo.

**A32b: rajadas redesenhadas com limiar absoluto (item pedido).** O Adendo 11d mostrou que o p5 dos intervalos da seção não consegue ver rajadas porque uma liberação manual leva mais tempo que isso. Definição nova, fixada agora: em cada seção-dia com pelo menos 10 liberações manuais, o limiar é **1,5 x a mediana do intervalo que precede as liberações manuais da própria seção-dia**; **rajada de k** = k ou mais liberações manuais consecutivas, **sem habilitação biométrica entre elas**, com todos os intervalos entre habilitações consecutivas **menores ou iguais ao limiar**. k = 3 principal, k = 5 sensibilidade. Esperado: o mesmo cálculo exato por permutação do Adendo 11b, com as ligações dadas pelos intervalos <= limiar (aproximação declarada: o limiar vem dos rótulos observados e é mantido nas permutações). Sensibilidade do limiar: 1,5 x a mediana **nacional** do intervalo anterior às manuais do ano e dia (em vez da mediana da seção). Comparação 2022 x 2026: frequência de seções com rajada nas mesmas seções (efeito fixo de seção, erro padrão agrupado por município), razão observado/esperado e fração das manuais dentro de rajadas; associação com comparecimento e participação de Lula (M1, M2: amostra principal = estrato R mais Roraima inteira; sensibilidade: todos os estratos; efeito fixo de local, controle do 1º turno; placebo 2022; família "A32b" com Holm próprio; teto em votos de margem pelas regras já usadas) e M3 descritivo. **Previsão com abuso:** mais rajadas em 2026 do que em 2022, acima do esperado, com associação positiva com o comparecimento ou com Lula só em 2026. **Sem abuso:** frequência e razão iguais entre os anos e sem associação.

## Adendo 15: A33, liberação manual no nível do local de votação (escola), escrito em 29/10/2026 ANTES de rodar qualquer item desta etapa

**Motivação (do pedido).** O efeito fixo por local, usado em H1, A32 e outros, elimina qualquer efeito comum a todas as seções de uma escola; um esquema no nível da escola seria invisível a esses testes.

**Unidade.** Local de votação (chave UF + município + zona + número do local do BWeb), somando as seções apuradas. Escolas com comparecimento de pelo menos 100 em cada turno usado. Taxa de liberação manual da escola = soma de `biom_nh` / soma do comparecimento do 2º turno.

**1. Descritivo (2026 T2 e 2022 T2).** Faixas da taxa manual da escola: até 5%, 5 a 10%, 10 a 20%, 20 a 30%, 30 a 50%, mais de 50%. Por faixa: escolas, seções, votantes, votos de Lula (do PT em 2022) e de Flávio (do oponente), e em quantas escolas o PT teve mais votos válidos. **Descritivo, confundido por idade e região.**

**2. Teste.** Unidade = escola. Desfechos: variação da participação de Lula nos válidos (T2 - T1), variação do comparecimento (T2 - T1); simetria para o oponente: variação do voto do oponente por apto e do PT por apto. Regressor: taxa manual da escola no T2; e, na variante de excesso, taxa 2026 menos taxa 2022 da mesma escola (escolas nos dois anos). Efeito fixo de **zona eleitoral** (erro padrão agrupado por zona) e, como robustez, de **município** (agrupado por município). Controles: idade média do eleitorado da escola (perfil do eleitorado por seção, ponderado por aptos) e participação do PT no T1. **Placebo: o mesmo modelo em 2022 e 2018** (variante de excesso: 2022 contra 2018, para 2022). Veredito pelas regras do `Registro` (interseção-união contra os placebos, Holm sobre a família de A33, teto de pior caso em votos de margem: fator 2 para participação, fator 1 para comparecimento). Para 2018 o perfil de idade precisa ser agregado de novo (zips locais); se não houver, 2018 fica sem o controle de idade e isso é declarado.

**3. Escolas extremas.** Excesso de liberação manual de cada escola sobre o esperado pela idade: taxa observada em 2026 T2 menos a prevista por um modelo ajustado **em 2022** no nível da escola (taxa manual ~ composição etária, biometria cadastrada e efeito fixo de UF, ponderado por votantes). **Top 1% do excesso**, entre escolas com 100 votantes ou mais; se a escola existe em 2022, exige-se também excesso sobre a taxa de 2022 da mesma escola maior que zero (escolas ausentes em 2022 entram só pelo primeiro critério e são marcadas). Lista com UF, município, zona, local, seções, votantes, resultado T1/T2 de 2026 e de 2022. **Teto de pior caso, não estimativa (fator 1):** soma dos excessos de votantes nas escolas extremas; e a parte além de 1,645 desvio do resíduo de 2022.

**4. Sincronia nos logs (amostra disponível).** Escolas com 3 ou mais seções com log consistente no mesmo dia (na prática, sobretudo Roraima, onde todas as seções foram lidas; a amostra estratificada das outras UFs raramente tem 3 seções da mesma escola; a cobertura é declarada). Estatística: número de pares de liberações manuais de seções diferentes da mesma escola com horários a até 60 s (sensibilidade: 180 s), dividido pelo número de pares possíveis. **Nulo principal (N1):** em cada seção, os rótulos "manual" são sorteados entre as habilitações da própria seção (preserva os horários e o ritmo de cada seção e o padrão do dia), 500 permutações, semente 20261029. **Sensibilidade (N2), que corresponde ao "embaralhar os horários entre seções" do pedido:** emparelhar seções de escolas **diferentes** da mesma UF, mesmo ano e dia, com o mesmo número de pares. Comparar a razão observado/esperado de 2022 e 2026.

**5. Escolas mais extremas e papel.** As 20 escolas mais extremas (as 20 primeiras do item 3) entram no pedido LAI 07 (todas as suas seções, nos dois turnos) e numa lista de BUs impressos a coletar (`results/fase3/A33_20_escolas_secoes.csv`, colunas vazias para o impresso).

**Previsão sem esquema:** associação no nível da escola igual à dos placebos, sem sincronia acima do acaso, extremas explicadas pela idade. **Com esquema:** excesso de ganho de Lula e de comparecimento nas escolas com excesso de liberação manual **só em 2026**, e sincronia acima do acaso.

### Adendo 15a: exposição do teto de A33, escrita em 29/10/2026 DEPOIS de ver a primeira execução (com um erro meu) e ANTES de rodar a versão corrigida

**Erro meu.** Na primeira execução converti os coeficientes de A33 em votos de margem usando como exposição **todos** os votos válidos (e todos os aptos) de 2026/T2. Como o regressor é a **taxa** de liberação manual (de 0 a 1, média perto de 0,07), isso superestima o teto em cerca de 14 vezes: gerou tetos de 74% a 116% da margem que não significam nada. O projeto já tinha a convenção certa em H1 (`h1_exposicao_votos_manuais_equiv`): exposição = soma de (taxa manual da seção x votos válidos) para participação, e soma de (taxa manual da seção x aptos) para comparecimento. Passa a valer essa convenção em A33 e fica registrado que a primeira execução estava errada. As linhas da primeira execução não são publicadas.

## Adendo 16: A34, duração do voto por eleitor (habilitação até a confirmação), escrito em 29/10/2026 ANTES de calcular qualquer duração

**Declaração de ordem.** Antes deste adendo vi apenas: o formato do log (eventos "Eleitor foi habilitado" e "Voto confirmado para [Presidente]" com horário, na mesma urna), os intervalos agregados de A21, A32 e A32b e os resultados de A5. **Não vi nenhuma duração** de habilitação até confirmação, por seção ou agregada. O texto-base está em `docs/propostas/novos-pontos-cegos.md`; as escolhas abaixo foram fixadas aqui.

**Pergunta.** O ato de votar leva, em cada seção, um tempo compatível com um eleitor presente? Votação "expressa" em massa (mediana de poucos segundos na seção inteira) seria incompatível com o ato físico de votar. Todos os testes temporais anteriores medem **intervalos entre eventos**; nenhum mede a **duração do ato**.

**Unidade e amostra.** Seção-dia, a mesma amostra de A4, A5, A21 e A32 (estrato aleatório mais Roraima inteira), 2022 e 2026, 1º e 2º turnos (o log do 2º turno traz os dois dias). A seção-dia entra se o log é consistente com o comparecimento do BU (a mesma marca `consistente` de A32) e tem **100 habilitações ou mais**.

**Definições.** Duração de um voto = tempo entre "Eleitor foi habilitado" e o **primeiro** "Voto confirmado para [Presidente]" posterior a ele no mesmo log, desde que não haja outra habilitação no meio. Habilitação sem voto posterior fica sem duração e é contada à parte. Métricas por seção-dia: **D1** mediana da duração; **D2** percentil 1; **D3** fração de durações menores que 20 s; **D4** desvio padrão (um voto "de máquina" teria dispersão quase nula); **D5** fração de habilitações sem voto.

**Hipótese nula.** D1 a D5 de 2026/2º turno são iguais às de 2022/2º turno nas mesmas seções (efeito fixo de seção, erro padrão agrupado por município), e a fração de seções com D3 acima do percentil 99 de 2022/2º turno não passa de 1% por mais de 2 erros padrão binomiais.

**Modelos de associação (simétricos para Lula e oponente).** (M1) participação de Lula no 2º turno em D3 mais a participação no 1º turno, efeito fixo de local, erro padrão agrupado por local; placebo: a mesma regressão em 2022. (M2) comparecimento do 2º turno em D3 mais o comparecimento do 1º turno, idem. (M3, descritivo, sem placebo) variação de D1 de 2022 para 2026. (M4) D1 da seção na taxa de liberação manual do BU mais D1 do 1º turno, efeito fixo de local, placebo 2022. Amostra principal: estrato aleatório mais Roraima (seleção independente do desfecho); sensibilidade com todos os estratos, **rotulada**.

**Regra de decisão.** As do `Registro`: interseção-união contra cada placebo, p unilateral de excesso, Holm sobre a família A34. **Previsão sem manipulação:** D1 mediana entre cerca de 40 s e 2 min, D3 próximo de zero nos dois anos, coeficientes de M1 e M2 dentro dos placebos.

**Teto (teto de pior caso, não estimativa).** Seções de 2026/2º turno com D3 acima do limiar do percentil 99 de 2022: (a) todos os votos válidos dessas seções atribuídos a um lado, fator 1; (b) saldo líquido, fator 2. Ao lado, a mesma conta em 2022 como referência de ruído. Quando o teto de uma associação vier só da falta de poder (erro padrão grande), vale a regra de exibição do Adendo 14: **não é plotado no G3**.

**Placebos.** 2022/1º turno, 2022/2º turno e 2026/1º turno nas mesmas seções. Placebo de forma: o mesmo teste na duração do **lado errado** (do voto confirmado até a próxima habilitação, que inclui fila e deve ser longa e igual nos dois anos); se acusar excesso ali, o desenho está quebrado e o resultado de A34 é descartado.

**Limites.** O pareamento só é determinístico porque há uma urna por seção; voto não concluído fica censurado (D5). Cobertura = a dos logs coletados (parcial; logs de todas as seções: NÃO EXECUTADO). Não identifica eleitores.

## Adendo 17: A35, extremos no universo geral (zero brancos e nulos em seção grande; comparecimento de 100%), escrito em 29/10/2026 ANTES de contar qualquer seção do universo geral

**Declaração de ordem.** Antes deste adendo vi: A12 e A12b (106 seções com zero voto para o oponente), H5 (comparecimento de 95% ou mais) e, em exploração, que dentro das 106 há 12 seções com zero brancos e nulos e comparecimento de 100 votantes ou mais (8 indígenas, a maior com 365 votantes) e 1 seção com comparecimento igual aos aptos. **Não vi as contagens análogas no universo geral** das 497.897 seções.

**Definições (2026/2º turno, seções apuradas, sem exterior).** **E1:** seções com brancos mais nulos igual a zero e comparecimento de 100 ou mais (sensibilidade: 200 e 400). **E2:** seções com comparecimento igual a `QT_APTOS` (sensibilidade: comparecimento/aptos de 0,995 ou mais). **E3:** seções com 100% dos votos **nominais** em um candidato e comparecimento de 30 ou mais.

**Esperado.** E1: Poisson-binomial com, para cada seção, p0 = (1 menos r) elevado a n, r = taxa de brancos mais nulos das demais seções do mesmo local (sem a própria seção; local de seção única usa o município) e n = comparecimento; **o mesmo estimador de A12b**, agora para todas as seções. E2: binomial com p = taxa de comparecimento do local e n = aptos, como aproximação declarada (abstenção não é independente: infla p0); por isso **E2 é descritivo**, só com razão observado/esperado, sem p. E3: contagem pura, sem teste.

**Regra de decisão.** Razão observado/esperado de 2026/2º turno que supera **cada** placebo (2014, 2018 e 2022, 1º e 2º turnos) por mais de 2 erros padrão (bootstrap por município, 1.000 reamostragens, semente 20261029) = EXCESSO; dentro da faixa histórica = dentro do esperado. Holm sobre {E1, E2, E3}. As seções sinalizadas ganham caracterização obrigatória: UF, município, tipo de local (classificação de A27), aptos e o histórico da mesma seção em 2018 e 2022.

**Teto (pior caso, não estimativa).** E1 e E3: votos do candidato majoritário nessas seções, fator 1; troca esperada pela vizinhança, fator 2. E2: (comparecimento menos a mediana do local), fator 1. Os três ao lado do mesmo cálculo para 2022/2º turno.

**Placebos.** 2014/2º turno, 2018/2º turno, 2022/2º turno e 2026/1º turno com o mesmo estimador; placebo de simetria: as mesmas contagens para o lado do oponente.

**Limites.** O esperado de E1 herda o viés de A12b em anos com terceiros relevantes (corrigido pelo placebo do mesmo ano, não pelo de 2026); local de seção única usa o município (menos preciso); E2 é fraco por desenho.

### Adendo 16a: previsão errada e métrica acrescentada em A34, escritas em 29/10/2026 DEPOIS de ver a distribuição das durações de Roraima em 2026 e ANTES de comparar com 2022 ou rodar qualquer modelo

**O que vi.** Só o extrator rodado nos logs de Roraima 2026 (1.519 seções): duração mediana de **9 s** no 2º turno (percentis 5, 25, 75, 95 e 99: 5, 7, 12, 20 e 34 s), 95% das durações abaixo de 20 s; no lado errado (voto confirmado até a próxima habilitação), mediana de 73 s. Nada de 2022 e nenhum resultado por seção ou por modelo.

**Erro meu na previsão do Adendo 16.** Escrevi que a mediana de D1 ficaria entre 40 s e 2 min, tirando a conta dos intervalos entre habilitações (que incluem a fila). A duração do ato, no 2º turno com dois candidatos, é de poucos segundos. **A previsão não se cumpre e fica registrada como não cumprida;** ela era irrelevante para o veredito, que sempre foi relativo a 2022 e aos placebos.

**Consequência para D3.** O limiar absoluto de 20 s deixa de separar nada (95% das durações já ficam abaixo). A regra de decisão **não muda**: D3 de 2026 contra o **percentil 99 de D3 de 2022** (relativo, como registrado). Acrescento, rotulada como pós-hoc e sem substituir D3, a métrica **D6** = fração de durações de 3 s ou menos (digitar o número do candidato e confirmar leva mais que isso; o percentil 1 em Roraima é de 4 s), com a mesma regra de excesso (fração de seções com D6 acima do percentil 99 de 2022/2º turno).

### Adendo 16b: diagnóstico de composição da cédula em A34, escrito em 29/10/2026 DEPOIS de ver o resultado completo dos testes registrados e ANTES de rodar qualquer estratificação

**O que vi (resultado dos testes do Adendo 16, sem alteração).** (i) Regra do percentil 99 (D3 e D6): **2,06% das seções de 2026/2º turno** têm D3 acima do percentil 99 de 2022/2º turno, e 2,43% têm D6 acima, contra 1% esperado, por mais de 2 erros padrão: pela regra registrada, **EXCESSO DETECTADO (forma)**. (ii) Diferença pareada de D1, 2026 menos 2022, nas mesmas seções: **-3,1 s no 2º turno** (z de -3,1) e **+4,2 s no 1º turno** (z de 10,6), isto é, em sentidos opostos. (iii) Placebo de forma (lado errado): sem excesso. (iv) Modelos M1, M2 e M4: sem excesso sobre o placebo de 2022 (p de excesso de 0,27, 0,90 e 0,42); os tetos dos modelos vêm da falta de poder. (v) Mediana de D1 por UF no 2º turno: em 2022 é de 15 a 17 s em AL, AM, BA, ES, MS, PB, PE, RO, RS, SC, SE e SP e de 9 a 11 s nas demais; em 2026 é de 15 a 16 s em AC, AM, DF, ES, RN e TO e de 9 a 10 s nas demais. Nas UFs com a mesma mediana nos dois anos, a diferença é de 0 a 1 s.

**Hipótese de trabalho (não é conclusão).** A duração do ato depende de **quantos cargos o eleitor vota na mesma sessão**. Nos 2º turnos de 2022 e de 2026 há segundo turno de governador em UFs diferentes (as medianas de 15 a 17 s ficam justamente nas UFs com esse segundo turno). A comparação nacional 2026 contra 2022 mistura composições diferentes; a regra do percentil 99 usa o percentil 99 nacional de 2022, que é uma mistura. Isso **não foi previsto** no Adendo 16.

**Diagnóstico (pós-hoc, rotulado, não substitui o veredito registrado).** (1) Classificar cada UF-ano pelo tipo de cédula do 2º turno com uma regra **fixada aqui**: "dois cargos" se a mediana de D1 da UF no 2º turno daquele ano for de **14 s ou mais**; "um cargo" se for menor. (2) Repetir a regra do percentil 99 (D3 e D6) **só nas UFs de 2026 que tinham a mesma classificação em 2022**, com o percentil 99 de 2022 calculado dentro de cada classe. (3) Repetir a diferença pareada de D1 nesse subconjunto. **Previsão sem manipulação:** a fração acima do percentil 99 volta a cerca de 1% e a diferença pareada de D1 fica perto de zero; se continuar acima de 1% por mais de 2 erros padrão no subconjunto, o excesso de forma **não** se explica por composição e o item fica em aberto.

**Limite.** A classe vem da própria duração (mediana por UF), não de uma lista externa de UFs com segundo turno de governador; a coincidência com as UFs com segundo turno estadual em 2022 é conferência de plausibilidade, não critério.

## Adendo 18: A43, série temporal dos votos a cada 15 minutos (limite físico, picos, filas, voto contínuo, silêncio e rajada), escrito em 31/10/2026 ANTES de ler qualquer carimbo de tempo de voto e ANTES de contar qualquer voto por janela

**Declaração de ordem.** Antes deste adendo vi: (i) as durações por habilitação (A34, amostra de seções e Roraima inteira) e as rajadas de liberação manual (A32, A32b), que usam intervalos entre habilitações mas **não** contagens de voto por janela de 15 minutos; (ii) no BWeb, as horas de abertura e encerramento por UF: a mediana de `DT_ABERTURA` é **06:00 no AC, 07:00 em AM, MS, MT, RO e RR e 08:00 nas demais UFs e no exterior**, em 2022 e 2026, T1 e T2, e o encerramento mediano fica entre 17:01 e 17:05 no T2 e entre 17:01 e 17:32 no T1 (fila no fim do dia incluída) nas UFs de 08:00, ou seja, o BWeb traz o **relógio local da urna**; (iii) os quantis de `QT_APTOS` (2026: P5 204, P10 233, P25 281, P50 327; 2022: P5 211, P10 242, P25 292, P50 340). **Não vi** nenhuma contagem de votos por janela, nenhum intervalo entre votos consecutivos e nenhuma curva de horário de 2026 ou 2022. O enunciado do A43 diz que depende da leitura completa dos logs do **A42, que não existe neste repositório**; trato a leitura completa como **não disponível** e registro duas etapas (abaixo).

**Etapas.** **Etapa A:** a amostra de seções já definida em A4/A5/A21/A34 (cerca de 67 seções por UF) mais Roraima inteira, com 2026 T1, 2026 T2, 2022 T1 e 2022 T2. **Etapa B (universo):** só se a leitura completa dos logs for feita por outro item ou autorizada (os zips de 2026 T1/T2 e 2022 T1/T2 somam cerca de 387 GB; os logs são lidos por requisição de faixa, sem baixar imagens do BU, mas o volume não foi medido). **Nenhum resultado da Etapa A vale como resultado do universo;** cada saída traz a etapa no cabeçalho.

**Preparação (horário).** (1) O horário único (votação das 08:00 às 17:00 **de Brasília** em todas as UFs) é a regra a **confirmar em fonte oficial do TSE antes de rodar**; enquanto não houver fonte citada, a saída traz "regra de horário não confirmada em fonte". (2) Verificação do relógio do log: para cada seção, diferença entre o primeiro carimbo do log e `DT_ABERTURA` do BWeb; se a mediana por UF estiver dentro de 5 minutos, o log usa o mesmo relógio do BWeb (local); se for um número inteiro de horas, desloca-se esse número de horas e o fato é registrado. (3) Normalização para Brasília: soma de 2 h no AC e de 1 h em AM, MS, MT, RO e RR (UFs de fuso diferente, a registrar na saída); exterior (ZZ) **fica fora** das métricas de horário. (4) Janela: 15 minutos ancorados em 08:00 de Brasília, 36 janelas até 17:00; votos depois das 17:00 ficam em janelas 37 em diante (fila no encerramento). Janela anterior à abertura efetiva da seção ou posterior ao último voto + 15 min é **não aplicável**, não é vazia.

**Contagem.** Voto computado = linha "Voto confirmado para [Presidente]" (a mesma de A34). Tipo da habilitação do voto (biométrica ou manual) pelas regras do Adendo 11. Nenhum título, CPF, nome ou identificação de mesário é lido ou gravado.

**Agregados.** Curvas de votos por janela e comparecimento acumulado: nacional, por região, UF e município, 2026 T1, 2026 T2, 2022 T1, 2022 T2. Aceleração ou desaceleração por região: diferença da participação da região no total de votos entre janelas consecutivas, contra 2022 do mesmo turno. Descritivo, sem veredito.

**M1 (limite físico).** Para cada voto, o ciclo = tempo entre o voto confirmado anterior e este. Calcula-se o **percentil 0,1 dos ciclos** (`m_bio` para ciclos de habilitação biométrica e `m_man` para manual), nas seções de **2022** (ano de referência); e o **mínimo absoluto** observado nos quatro anos. Limite de uma janela com `k_bio` e `k_man` ciclos: `k_bio*m_bio + k_man*m_man <= 900 s + 1 ciclo` (folga de fronteira). **Violação branda** = acima do limite com o percentil 0,1; **violação dura** = acima do limite com o mínimo absoluto. Toda violação é listada individualmente (seção, janela, contagem, tipo). Sem teste: qualquer violação dura é um achado; violação branda é reportada com sua frequência em 2022.

**M2 (pico anômalo).** Janela com contagem acima do percentil 99,9 da referência **e** acima de 3 vezes a mediana das vizinhas na mesma janela (mínimo de 2 vizinhas). Referência = seções de 2022 do mesmo turno, mesmo quintil de aptos, mesma janela e mesma região. Vizinhas = demais seções do mesmo local de votação no mesmo dia.

**M3 (fila longa anômala).** Sequência de **8 ou mais janelas consecutivas** (2 h) com contagem de pelo menos **70% do limite de M1 branda** quando a mediana das vizinhas nessas janelas está **abaixo de 50%** desse limite.

**M4 (voto contínuo).** Seção com **menos de X = 120 aptos** e **nenhuma janela vazia** entre a abertura efetiva e as 17:00. Origem de X: com chegada uniforme em 36 janelas e comparecimento de 75%, a probabilidade de nenhuma janela vazia cai a 5% ou menos com cerca de 91 votos, ou seja, cerca de 121 aptos (cálculo de Poisson; fixo aqui, não ajustado depois). Esperado: simulação por seção (10.000 sorteios) com o **perfil horário empírico da UF no mesmo dia**, o mesmo número de votos e as janelas aplicáveis; seção sinalizada se a probabilidade de nenhuma janela vazia for menor que 0,001, e fração sinalizada comparada com a esperada.

**M5 (silêncio e rajada).** **4 ou mais janelas vazias seguidas (60 minutos ou mais)** seguidas de janela com pelo menos 70% do limite de M1 branda; contagem separada para a última hora (16:00 a 17:00) e para janelas depois das 17:00.

**M6 (liberação manual por janela).** Fração de habilitações manuais nas janelas sinalizadas por M1 a M5 contra o resto do dia da mesma seção; diferença com intervalo por bootstrap por local (1.000 reamostragens).

**Regra de decisão (M2 a M5).** A fração de seções sinalizadas em 2026 (T2, e T1 separado) é comparada com os placebos 2022 T1, 2022 T2 e, para o T2, 2026 T1; **EXCESSO** só se superar **cada** placebo por mais de 2 erros padrão (bootstrap por município, 1.000 reamostragens, semente 20261029); Holm sobre {M2, M3, M4, M5}; M1 não tem teste. Sem poder (menos de 30 seções sinalizadas em algum ano) o resultado é "sem poder", não "dentro do esperado".

**Ligação com o resultado (só depois de fechar as métricas).** Para as seções sinalizadas por M1 a M5 contra as vizinhas (mesmo local, não sinalizadas): variação de voto T1 para T2 pelo mesmo modelo de A6 e A32 (`fe_ols`, efeito fixo de local, controle T1, erro agrupado por local; interseção-união com o placebo 2022 pelo `Registro`), para **Lula e para o oponente** (simetria). **Teto em votos de margem (pior caso, não estimativa):** fator 1 = votos do candidato majoritário nas seções sinalizadas; fator 2 = troca esperada pela vizinhança. Regra do G3 (Adendo 14): teto inflado por construção ou sem poder aparece só como texto.

**Saídas.** Mapa de calor UF x janela de 15 minutos, 2026 T2 e 2022 T2 lado a lado; lista das 100 seções mais anômalas por métrica, com colunas vazias para BU impresso e ata (alimenta a coleta e o pedido LAI 07). Etapa A traz o rótulo "amostra".

**Previsão sem manipulação (declarada agora).** Nenhuma violação dura de M1; picos (M2) e filas (M3) concentrados em grandes centros e em horários de abertura, almoço e fim do dia, explicados pelas vizinhas e pela frequência de 2022; M4 com fração sinalizada igual à simulada; M5 concentrado em seções pequenas e rurais; sem associação com o voto e com a mesma frequência em 2022. **Com manipulação:** violações duras de M1, M3 e M5 mais frequentes que em 2022, na última hora, em seções com liberação manual alta (M6) e associadas a variação de voto em um só sentido.

**Limites.** O log só vale como "o que a urna listou": a verificação da assinatura segue pendente (A18/A29). Seções pequenas têm poucas janelas (baixo poder). O limite físico de M1 usa o percentil 0,1 de 2022 e pode ser menor ou maior em 2026 por mudança de software; por isso há a violação dura e a comparação com 2022. A hora de chegada à seção não é observada (só o voto), logo fila e ritmo se confundem. **Nada deste adendo foi calculado.** Qualquer mudança de definição será registrada em adendo 18a, com a data e o que eu tinha visto.

## Adendo 19: A41, comparecimento acima da população de 16 anos ou mais (reescreve a alegação "23 municípios da Bahia com mais eleitores do que habitantes"), escrito em 31/10/2026 ANTES de entrar o denominador oficial do IBGE e ANTES de rodar qualquer teste formal

**Declaração de ordem.** Antes deste adendo vi, em verificação exploratória (30/10/2026, `scripts/exploratorio/11_verifica_alegacoes_fase5.py`, saídas `results/exploratorio/ALE_*`, commit "verificacao Fase 5"): (i) aptos acima da população de 16+ é **estrutural e nacional** (2.889 de 5.557 municípios em 2018 T2; 3.978, ou 72%, em 2026 T2; na Bahia 236 de 417 em 2018 e 334 em 2026) e já foi documentado em A20 (razão nacional aptos/pop16 de 0,985), logo não é anomalia de 2026 nem da Bahia; (ii) o achado real foi o **comparecimento** acima de toda a população de 16+: Brasil 232 (2018 T2), 593 (2022 T2), 1.020 (2026 T1) e 1.087 (2026 T2); Bahia 3, 17, 34 e 51; (iii) a aproximação "aptos acima da população **total**" (razão aptos/pop16 acima de 1,25) dá 11, 33, 39 e 39 municípios baianos, ordem de grandeza compatível com os "23" da alegação, mas o número exato depende do denominador. **Não vi** nenhum denominador de população total, nenhuma projeção IBGE 2022-2026 e nenhum teste formal.

**Contexto.** Alegação recebida (imagem): "23 municípios da Bahia com mais eleitores do que habitantes". A verificação exploratória mostrou que a forma original é estrutural; o item que merece teste é o salto de **comparecimento acima da população de 16+** entre 2022 e 2026. Este adendo pré-registra esse teste.

**Dados.** Comparecimento por seção e município do BWeb (já local, `parquet/bu_*_t*.parquet`, base APURADA, sem exterior). População de 16+ por município: hoje só a aproximação de A20 (`results/fase3/A20_mapa_tse_ibge.csv`, Censo 2022). **INSUMO EXTERNO PENDENTE:** população municipal total e população de 16+ do Censo 2022 e das revisões/projeções do IBGE (SIDRA, tabelas 4714 e 9605 ou equivalente), a entrar em `data/` com hash **antes** de qualquer teste. **NÃO RODAR o teste formal enquanto esse insumo não entrar.** Ressalva obrigatória, com fonte IBGE citada na saída: o Censo 2022 teve subcontagem reconhecida pelo próprio IBGE; município pequeno é onde ela mais pesa.

**Métrica.** Por município e ano/turno: razão comparecimento/pop16; excedente em votos = max(0, comparecimento menos pop16); teto em votos de margem (pior caso, não estimativa) = margem Lula menos oponente somada nos municípios excedentes, com fator 1 (bruta) e fator 2 (troca esperada pelo perfil do entorno, mesma convenção de A31/A32). Tudo recalculado com o denominador IBGE revisado quando entrar.

**Controles e placebos.** Taxa nacional e por UF (a alegação original era Bahia-específica: testar se a BA está acima do esperado dado o seu perfil de envelhecimento e razão cadastro/população); envelhecimento por coorte (A20/A20b: a população 16+ cresce mais devagar que o cadastro); série 2014, 2018, 2022, T1 e T2, com o mesmo estimador; sensibilidade ao denominador (Censo 2022 contra projeção IBGE para 2026).

**Regra de decisão.** **EXCEDENTE REAL:** município com razão acima de 1 sob a população IBGE revisada **e** diferença não explicada pela projeção demográfica 2022-2026; o veredito sai com o teto em votos de margem dos municípios excedentes. **INCONCLUSIVO:** se a classificação depender da versão do denominador (Censo contra projeção), com as duas listas publicadas. **DENTRO DO ESPERADO:** se o salto de 2026 se explicar por envelhecimento mais crescimento do cadastro na escala de 2022, medido pelos placebos.

**O que fecha.** Folha de votação e listas de habilitação dos municípios excedentes (pedido LAI); cruzamento com óbitos (óbitos por município/idade contra o cadastro); para os municípios excedentes, histórico da razão em 2014-2022 e comparação com o perfil de A27.

**Limites.** A população municipal é o denominador e ele mesmo é disputado (subcontagem do Censo 2022, fonte IBGE a citar); domicílio eleitoral não é residência (o eleitor pode votar onde não mora, e A20 já mediu o descompasso estrutural); sem o denominador oficial, todo número deste item fica em "aproximação", como no exploratório. **Nenhum teste deste adendo foi rodado.**

## Adendo 20: A44, quedas verticais na curva acumulada de apuração (alegação do vídeo "Prof. Trindade", Inventário de alegações A13/A16), escrito em 31/10/2026 ANTES de refazer qualquer curva com o relógio de recebimento e ANTES de qualquer forense por lote

**Declaração de ordem.** Antes deste adendo vi: A1 (curva de apuração 2026 T2), A14 (recebimento x totalização x divulgação em 25/10/2026), A1-T1 (a mesma curva no 1º turno) e A18 (alteração de arquivo no meio da apuração). Esses itens **mediram a curva e as janelas**, mas **não fizeram forense lote a lote**: nenhum deles decompôs cada queda ou salto nos boletins que chegaram naquele intervalo. **Não vi** nenhuma decomposição por lote, nenhuma curva com o eixo Y de 0 a 100% e a margem final marcada, e nenhuma comparação entre as três versões de curva definidas abaixo.

**Contexto e hipótese.** A alegação (vídeo, Inventário de alegações): a curva de "percentual acumulado de votos" do candidato teria **quedas verticais**, impossíveis numa soma acumulada. **H0 (explicação benigna):** as quedas são artefato de mistura de contagens — o percentual é calculado sobre o **totalizado** (números que o TSE consolida) enquanto o denominador ou a base do eixo X usa o **recebido** (BUs que chegaram); quando o totalizado anda mais devagar que o recebido, ou quando um lote grande de urnas de perfil diferente entra de uma vez, a razão acumulada pode cair sem que voto algum seja retirado. Sob a hipótese adversarial, haveria lotes cujo efeito calculado não fecha com a variação observada.

**Dados.** BWeb por seção com os dois carimbos: hora de recebimento do BU no TSE (`DT_RECEBIMENTO_BU_HOR_TSE`) e hora de totalização/divulgação, quando distinta e disponível no dado público. **Plano B (declarado agora):** se os dois relógios não existirem no dado público ou forem idênticos em mais de 99% das seções, a versão (c) fica **NÃO EXECUTÁVEL**, com a justificativa e a cobertura efetiva registradas na saída.

**Etapa 1 (reprodução).** Refazer o gráfico do vídeo em três versões: (a) eixo X = BUs **recebidos**, percentual calculado sobre os recebidos; (b) eixo X = BUs **totalizados**, percentual sobre os totalizados; (c) **mista** (a combinação que o portal efetivamente publicou, se identificável). Regra fixa: se a versão que reproduz as quedas for a mista — e as versões (a) e (b) forem monótonas —, a alegação fica explicada como artefato de mistura de contagens e o item encerra com esse veredito.

**Etapa 2 (forense de lote).** Para cada queda ou salto na versão que os tiver: identificar o lote do intervalo (BUs com `DT_RECEBIMENTO_BU_HOR_TSE` na janela): número de BUs, votos por candidato, UF, municípios e horário; calcular o efeito esperado do lote sobre o percentual acumulado (o lote entra com o seu próprio share e desloca a média acumulada) e comparar com a variação observada. Listar todos os eventos, não uma amostra.

**Escala (regra de exibição, como no G3 do Adendo 14).** Todo gráfico deste item usa eixo Y de 0 a 100% com a margem final marcada; reafirmar no texto que o total final é independente da ordem de apuração (H9) e bate com a soma dos BUs.

**Regra de decisão.** Evento **EXPLICADO** se o efeito calculado do lote fechar com a variação observada em ± 0,1 ponto percentual (lotes grandes, mais de 1.000 BUs) ou em ± 2 erros padrão (lotes pequenos, erro padrão da média acumulada por bootstrap por município, 1.000 reamostragens, semente 20261029). Veredito do item: **EXPLICADO** se pelo menos 95% dos eventos fecharem; senão **INCONCLUSIVO**, com os eventos residuais listados individualmente (horário, UF, municípios, BUs, votos, efeito calculado contra observado).

**O que fecha.** Para eventos residuais: os arquivos de log e a cadeia de publicação do intervalo (A26/A26b medem alteração de arquivos; A14 mede os atrasos), e conferência contra os dados de divulgação minuto a minuto do TSE, se disponíveis.

**Limites.** A versão (c) pode ser NÃO EXECUTÁVEL (plano B); a curva pública do portal pode não ser reconstruível em retrospecto (o que o portal mostrou ao vivo não está arquivado no repo); um evento explicado contabilmente não exclui fraude na origem dos votos do lote — A44 mede a **contagem**, não a **origem** (origem é H9/A19/A37). **Nada deste adendo foi calculado.** Qualquer mudança de definição será registrada em adendo 20a, com a data e o que eu tinha visto.

## Adendo 21: A42, leitura completa dos logs de urna (etapa B do A43), escrito em 31/10/2026 ANTES de baixar qualquer zip novo e ANTES de medir o volume dos logs em qualquer UF

**Declaração de ordem.** Antes deste adendo vi: (i) os extratores já escritos e rodados em amostra (A21, A32, A34: duração do voto e rajadas de liberação manual em cerca de 67 seções por UF e em Roraima inteira, 2026 T2 e 2022 T2); (ii) a estimativa de votos após as 17h (A5, feita por amostra e por intervalos, não por contagem); (iii) o Adendo 18 (A43), que declarou a leitura completa dos logs como "não disponível" e registrou a Etapa A (amostra) e a Etapa B (universo, dependente de A42); (iv) os dois zips de urna de Roraima (2022 e 2026, 2º turno) já baixados e verificados. **Não vi** nenhuma contagem de votos por janela no universo de seções, nenhum placar horário exato e nenhuma medição de volume total dos logs.

**Escopo.** Todas as seções com log, **2026 T2 e 2022 T2 primeiro**, depois 2026 T1 e 2022 T1. Uma UF por vez, em processamento de streaming.

**Processamento (por UF, parametrizável).** Script com parâmetros (UF, ano, turno), para rodar em VM na nuvem: (1) baixar o zip da fonte oficial (URL registrada em `data/urls_origem.txt`); (2) conferir o hash contra `data/manifest_hash_oficial.csv` (hash oficial TSE) e registrar o SHA-256 do baixado em `data/sha256_entradas.txt`; (3) extrair **só os logs** (sem imagens de BU); (4) processar em streaming, seção a seção, sem carregar o zip inteiro em memória; (5) **apagar o zip** ao final, mantendo só as saídas versionadas. O reuso do parser existente (`scripts/urna_parse.py`, o mesmo de A21/A32/A34) é obrigatório; qualquer alteração nele entra em commit separado e antes da corrida.

**Saídas versionadas por UF** (em `results/fase5/A42_{UF}_{ano}_t{turno}_*.csv`): (a) votos por janela de 15 minutos por seção (a contagem do Adendo 18, mesma definição de evento: linha "Voto confirmado para [Presidente]"); (b) **votos exatos após as 17h** por seção — substitui a estimativa do A5, que fica com **nota de superação** apontando para A42; (c) **placar acumulado às 17h, 18h e 19h por limites exatos**: seções sem nenhum voto após o horário de corte entram com o placar exato; as demais entram com o intervalo [placar_seco, placar_seco + votos_restantes], porque o log não permite ordenar os votos de uma mesma seção dentro da janela (ver proibição abaixo); (d) **cobertura por UF**: seções com e sem log, falhas de leitura, logs vazios ou truncados, com a lista das seções afetadas.

**Proibição explícita (do dono).** **Não associar horário a candidato voto a voto.** O RDV não guarda horário e embaralha a ordem dos votos (sigilo do voto); o carimbo do log marca o evento "voto confirmado", não o conteúdo. Toda agregação é de **contagem de votos por janela**, nunca de voto em candidato por janela. Este limite vale para A42, A43 e qualquer item que use os carimbos.

**Medição de escala (parte da Etapa A de A43, prévia à corrida).** Antes de qualquer corrida em escala: medir, numa UF pequena, o tamanho do zip, o tamanho dos logs extraídos e o tempo de processamento; projetar para 27 UFs + ZZ × 2 anos × 2 turnos (tempo e disco); publicar a estimativa no memorando da Etapa A **antes** de autorizar a corrida em VM, com a estimativa de custo.

**Regra de decisão (preliminar — A SER FIXADA; o dono revisa antes de assinar).** Perguntas propostas: **Q1 (placar às 17h):** o placar acumulado às 17h, por UF e nacional, calculado por limites exatos, contém o placar reconstruível do BWeb na primeira janela de totalização? Se o intervalo [seco, seco+restantes] não contiver o valor observado em alguma UF com mais de 100 mil votos, INCONSISTENTE; se contiver em todas, COMPATÍVEL. **Q2 (superação do A5):** votos exatos após as 17h contra a estimativa do A5: diferença maior que 10% da estimativa em valor absoluto = A5 REVISADO, com nota; caso contrário, A5 CONFIRMADO. **Q3 (horários anômalos):** fração de seções com primeiro voto antes da abertura legal ou último voto após o encerramento (sem prorrogação documentada) em 2026 contra o placebo de 2022: excesso de mais de 2 erros padrão (bootstrap por município, 1.000 reamostragens, semente 20261029) = EXCESSO. **Nenhuma das três está fixada:** a assinatura do dono neste parágrafo é condição para a corrida.

**O que fecha.** Inconsistência em Q1: os logs brutos da UF afetada (já versionados por seção) e a cadeia de publicação (A14, A18, A26). Excesso em Q3: lista de seções para conferência com BU impresso e ata (alimenta a coleta e os pedidos LAI).

**Limites.** A cobertura é a dos logs publicados pelo TSE (seções sem log ficam fora e entram na tabela de cobertura); o log vale como "o que a urna listou" — a verificação da assinatura segue pendente (A18/A29, ver ambiguidade em `REGISTRO_IDS.md`); o volume total estimado antes da medição (cerca de 387 GB de zips por ciclo completo) é ordem de grandeza, não medição. **Nada deste adendo foi calculado.** Qualquer mudança de definição será registrada em adendo 21a, com a data e o que eu tinha visto.
