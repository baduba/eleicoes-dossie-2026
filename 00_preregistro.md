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
