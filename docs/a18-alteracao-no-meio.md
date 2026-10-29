# A18. Hipótese "alteração no meio" (entre o fechamento da urna e a publicação)

**Hipótese.** Alguém altera os resultados depois que a urna fecha e antes de os dados serem publicados (na transmissão, na recepção, na totalização ou na publicação), de modo coerente em todos os arquivos.

> **O que A4 e H9 verificam e o que não verificam.** Verificam **consistência entre arquivos publicados pelo TSE** (BU, RDV, imagem do BU, log, BWeb, totalização por zona e município) e o vínculo de hash entre eles. Esses arquivos nascem do mesmo software e do mesmo fluxo. Por isso **não excluem uma alteração coerente feita antes da publicação**. Só uma verificação que não dependa dos arquivos publicados exclui essa hipótese: a **assinatura criptográfica** conferida com a chave oficial, e a **comparação com boletins impressos** fotografados nas seções.

## 1. Os atrasos, com fonte

| turno | o que foi dito ou decidido | fonte | o que os dados mostram |
|---|---|---|---|
| 1º turno (04/10/2026) | O presidente do TSE confirmou atraso de cerca de 1 hora na divulgação do total, que atribuiu a congestionamento no sistema de dados da Corte ("fluxo de dados acima do normal"). Por volta das 19h o total nacional de presidente ficou parado em 64%; por volta das 20h voltou a andar, já em 84%. O TSE disse não saber ainda se havia causa além do congestionamento. | [JB, 05/10/2026](https://www.jb.com.br/brasil/politica/2026/10/1061122-tse-confirma-atraso-na-totalizacao-dos-votos-e-explica-causa.html) (imprensa; paráfrase da declaração; a fonte oficial não pôde ser aberta) | Entre 19:30 e 19:59 só 1,5% das seções tiveram o BU recebido, contra 23,8% entre 19:00 e 19:29 e 5,6% entre 20:00 e 20:29 (tabela abaixo). |
| 2º turno (25/10/2026) | A votação foi prorrogada por duas horas por decisão do ministro Cristiano Zanin, a pedido da campanha de Lula (falta de ônibus na Bahia); o TSE informou que a votação continuaria só nas seções ainda abertas às 17h. O recebimento de BUs, a totalização e a divulgação foram retomados às 19h; antes da pausa, 1.225 das 499.248 seções (cerca de 0,25%) estavam contabilizadas. | [Times Brasil](https://timesbrasil.com.br/brasil/decisao-2026-tse-anuncia-retomada-da-totalizacao-e-divulgacao-dos-votos-apos-as-19h/) e [Correio da Manhã](https://www.correiodamanha.com.br/politica/2026/10/329719-tse-retoma-contagem-dos-votos-as-19h-apos-suspensao-provocada-por-decisao-de-zanin.html) (imprensa; o comunicado oficial não foi aberto) | 99,6% dos BUs têm horário de recebimento depois das 19h (A14). |

Recebimento de BUs no 1º turno de 2026, por meia hora (todas as seções com horário de recebimento):

| inicio | secoes | pct |
|---|---|---|
| 17:00 | 11.122 | 2,2 |
| 17:30 | 63.099 | 12,7 |
| 18:00 | 103.584 | 20,8 |
| 18:30 | 124.799 | 25,1 |
| 19:00 | 118.591 | 23,8 |
| 19:30 | 7.651 | 1,5 |
| 20:00 | 27.737 | 5,6 |
| 20:30 | 32.746 | 6,6 |
| 21:00 | 5.311 | 1,1 |
| 21:30 | 1.917 | 0,4 |
| 22:00 | 725 | 0,1 |
| 22:30 | 300 | 0,1 |
| 23:00 | 102 | 0,0 |
| 23:30 | 24 | 0,0 |

O horário de recebimento é o campo `DT_RECEBIMENTO_BU_HOR_TSE` publicado pelo TSE. A queda das 19:30 às 20:00 é compatível com a paralisação descrita; os dados não dizem a causa.

## 2. Assinatura criptográfica (prioridade máxima): NÃO EXECUTADO PARCIAL

- **Lido e conferido:** o certificado X.509 de cada seção de Roraima em 2026: 1.519 lidos, 0 erros. CN = `UEAO` + número da urna do BWeb em 1.519 de 1.519; validade cobre a data da eleição em 1.519 de 1.519; emissores `AC UE2020` (922), `AC UE2022` (597).
- **Verificado:** **0% das assinaturas** (0 de 1.519 seções lidas; 0 falhas porque nenhuma foi testada). O OID do algoritmo é `1.3.6.1.4.1.44588.2.1`, com chave de 66 bytes e assinatura de 132 bytes.
- **O que falta:** o certificado raiz e a chave pública oficiais, e a especificação do algoritmo, obtidos de fonte oficial. O site do TSE responde HTTP 403 a automação, e **não foi usada nenhuma chave de fonte não oficial**. Uma apresentação do TSE de 2021 (vista só em resultado de busca) cita EdDSA sobre Curve25519 para o QR code do BU e curvas de 256 bits para outras assinaturas; isso não foi confirmado nem verificado aqui.
- **Como destravar:** um perito ou fiscal com acesso à ferramenta oficial de verificação do TSE roda o script `scripts/13_cert_urna.py` e a ferramenta nos mesmos arquivos e publica o resultado por *issue*.

## 3. Testes pré-registrados (Adendo 7)

Janela e testes foram fixados no [Adendo 7](preregistro.md) antes de rodar. Os testes comparam o 2026 com a mesma janela de relógio em anos sem congestionamento (placebos), com efeito fixo de local de votação. **Previsão sem alteração:** nenhuma diferença além da composição.

| H | teste | est_2026T2 | placebos | p_excesso | p_holm | veredito |
|---|---|---|---|---|---|---|
| A18a | 1o turno 2026: BU recebido entre 19h e 20h: participacao de Lula nos validos, EF de local | 0,00090 | 2022/T1: -0.00001 (ep 0.00034, p_exc 0.0398) / 2018/T1: -0.00030 (ep 0.00039, p_exc 0.0157) | 0,040 | 0,159 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| A18a | 1o turno 2026: BU recebido entre 19h e 20h: participacao de oponente nos validos, EF de local | -0,00090 | 2022/T1: 0.00001 (ep 0.00034, p_exc 0.96) / 2018/T1: 0.00030 (ep 0.00039, p_exc 0.984) | 0,984 | 1,000 | REFUTADA (sem excesso, teto <1% da margem) |
| A18b | 2o turno 2026: horas de atraso no recebimento depois das 19h: participacao de Lula nos validos, EF de local | 0,00025 | 2022/T2: 0.00033 (ep 0.00051, p_exc 0.555) / 2018/T2: 0.00295 (ep 0.00136, p_exc 0.974) / 2026/T1: -0.00205 (ep 0.00058, p_exc 0.000207) | 0,974 | 1,000 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| A18b | 2o turno 2026: horas de atraso no recebimento depois das 19h: participacao de oponente nos validos, EF de local | -0,00025 | 2022/T2: -0.00033 (ep 0.00051, p_exc 0.445) / 2018/T2: -0.00295 (ep 0.00136, p_exc 0.026) / 2026/T1: 0.00205 (ep 0.00058, p_exc 1) | 1,000 | 1,000 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |

**Leitura.** Na janela de 19h às 20h do 1º turno, as seções do mesmo local que tiveram o BU recebido durante o congestionamento têm participação de Lula 0,09 p.p. maior que as demais (e a do oponente, 0,09 p.p. menor). Contra os placebos o p unilateral bruto é 0,040 (2022 e 2018, o maior); com a correção de Holm para os quatro testes, 0,159. **Não atinge o critério de excesso.** O veredito pela regra pré-registrada é inconclusivo porque o teto de pior caso passa de 1% da margem, e não porque haja excesso. No 2º turno não há diferença além dos placebos. Os tetos desta tabela são limites superiores sob a convenção de exposição do Adendo 7 e dependem da incerteza dos placebos; **não medem votos alterados**. Estes testes **não excluem** uma alteração coerente; eles buscam apenas uma assinatura temporal específica.

Estimativas por ano (coeficiente da janela, em participação nos válidos; o erro padrão é agrupado por local):

| ano | resposta | secoes | secoes_na_janela | pct_na_janela | coef_janela | ep |
|---|---|---|---|---|---|---|
| 2026 | lula_sh | 497.708 | 126.242 | 25,4 | 0,00090 | 0,00039 |
| 2026 | dir_sh | 497.708 | 126.242 | 25,4 | -0,00090 | 0,00039 |
| 2026 | lula_sh (robustez: defasagem > p90) | 497.708 | 49.580 | 10,0 | -0,00009 | 0,00031 |
| 2026 | dir_sh (robustez: defasagem > p90) | 497.708 | 49.580 | 10,0 | 0,00009 | 0,00031 |
| 2022 | lula_sh | 470.437 | 203.627 | 43,3 | -0,00001 | 0,00034 |
| 2022 | dir_sh | 470.437 | 203.627 | 43,3 | 0,00001 | 0,00034 |
| 2018 | lula_sh | 452.479 | 123.685 | 27,3 | -0,00030 | 0,00039 |
| 2018 | dir_sh | 452.479 | 123.685 | 27,3 | 0,00030 | 0,00039 |

Seções com nominais + brancos + nulos diferentes do comparecimento no 1º turno de 2026 (previsão: zero nos dois grupos): janela = 1, dentro da janela de 19h às 20h; janela = 0, demais.

| janela | secoes | com_inconsistencia |
|---|---|---|
| 0.0 | 371.466 | 0 |
| 1.0 | 126.242 | 0 |

**2º turno: ordem de recebimento depois das 19h.** Coeficiente por hora de atraso do recebimento:

| ano | turno | resposta | secoes_apos_19h | coef_por_hora | ep |
|---|---|---|---|---|---|
| 2026 | 2 | lula_sh | 496.651 | 0,00025 | 0,00029 |
| 2026 | 2 | dir_sh | 496.651 | -0,00025 | 0,00029 |
| 2022 | 2 | lula_sh | 74.569 | 0,00033 | 0,00051 |
| 2022 | 2 | dir_sh | 74.569 | -0,00033 | 0,00051 |
| 2018 | 2 | lula_sh | 38.975 | 0,00295 | 0,00136 |
| 2018 | 2 | dir_sh | 38.975 | -0,00295 | 0,00136 |
| 2026 | 1 | lula_sh | 195.104 | -0,00205 | 0,00058 |
| 2026 | 1 | dir_sh | 195.104 | 0,00205 | 0,00058 |

Parcela da variância do horário de recebimento explicada por UF e por município (descritivo, não é teste):

| ano | turno | secoes_apos_19h | r2_horario_por_UF | r2_horario_por_municipio | horas_mediana_apos_19h |
|---|---|---|---|---|---|
| 2026 | 2 | 496.651 | 0,39 | 0,71 | 1,43 |
| 2022 | 2 | 74.569 | 0,06 | 0,50 | 0,22 |
| 2018 | 2 | 38.975 | 0,19 | 0,64 | 0,30 |
| 2026 | 1 | 195.104 | 0,09 | 0,42 | 0,32 |

No 2º turno de 2026 o horário de recebimento depois das 19h tem mais estrutura geográfica (por UF) do que nos anos de comparação. Isso é o esperado quando o recebimento é retido até um horário e liberado por ordem de transmissão; não distingue essa explicação de outra.

## 3b. A1 corrigido no 1º turno de 2026 e a janela do congestionamento (análise posterior)

> Análise **posterior** (pedida depois de ver o resultado; não pré-registrada). Ela não muda o veredito do A1 corrigido, cujo alvo pré-registrado é o 2º turno.

A curva do 1º turno de 2026, contra o nulo corrigido (municípios em ordem aleatória dentro de cada UF), fica fora do envelope em 241 dos 900 pontos avaliados, quase todos numa única corrida de 240 pontos consecutivos, de 76,0% a 99,9% das seções, das 19:18 às 22:28 do dia 04/10.

- **Coincide com a janela de 19h às 20h?** Em parte. A corrida **começa** dentro da janela (19:18) e 91 dos 241 pontos fora do envelope (38%) caem entre 19h e 20h, contra 26,5% de todos os pontos da curva nessa janela. Mas a corrida **continua** até as 22:28, bem depois da retomada.
- **O desvio não cresce na janela.** A curva fica abaixo da mediana do nulo (menos participação de Lula) em todo o trecho; o maior desvio é de -1,67 p.p., com 19,5% das seções (18:13), **antes** da janela. A partir daí o desvio diminui até zero (-0,86 p.p. aos 76%, -0,63 p.p. aos 84%, -0,25 p.p. aos 95%). O trecho "fora do envelope" é a parte final da curva, em que o envelope do nulo se estreita porque a curva acumulada converge para o total; ali um desvio pequeno já sai do envelope.

- **Quais UFs chegaram nesse trecho.** As seções que chegaram na corrida vêm sobretudo de SP (20% da UF), BA (44% da UF), MG (30% da UF), RJ (41% da UF), CE (45% da UF), PE (38% da UF); BA, RJ, CE, PE, MA e AL pesam mais no trecho que no país (colunas abaixo). Nas seções cuja primeira totalização caiu entre 19h e 20h, as maiores contribuições são SP (26,8%), MG (12,1%), RJ (10,4%), BA (7,7%), CE (5,8%).

Seções por UF no trecho fora do envelope (todas as UFs em `results/fase2/A1T1_ufs.csv`):

| SG_UF | secoes | nas_corridas | pct_da_UF_nas_corridas | pct_das_secoes_nas_corridas | pct_das_secoes_do_pais |
|---|---|---|---|---|---|
| SP | 103.656 | 20.782 | 20,1 | 17,3 | 20,8 |
| BA | 35.476 | 15.627 | 44,0 | 13,0 | 7,1 |
| MG | 52.062 | 15.619 | 30,0 | 13,0 | 10,4 |
| RJ | 37.675 | 15.430 | 41,0 | 12,8 | 7,5 |
| CE | 23.765 | 10.693 | 45,0 | 8,9 | 4,8 |
| PE | 21.418 | 8.108 | 37,9 | 6,7 | 4,3 |
| MA | 18.093 | 6.283 | 34,7 | 5,2 | 3,6 |
| PA | 20.827 | 5.388 | 25,9 | 4,5 | 4,2 |
| AL | 7.101 | 4.035 | 56,8 | 3,4 | 1,4 |
| SC | 17.326 | 2.549 | 14,7 | 2,1 | 3,5 |

Seções cuja primeira totalização caiu entre 19h e 20h, por UF (todas em `results/fase2/A1T1_ufs_janela.csv`):

| SG_UF | secoes | na_janela | pct_da_UF_na_janela | pct_das_secoes_da_janela | lula_pct_validos_na_janela |
|---|---|---|---|---|---|
| SP | 103.656 | 35.470 | 34,2 | 26,8 | 43,9 |
| MG | 52.062 | 16.037 | 30,8 | 12,1 | 47,3 |
| RJ | 37.675 | 13.808 | 36,6 | 10,4 | 42,3 |
| BA | 35.476 | 10.245 | 28,9 | 7,7 | 69,4 |
| CE | 23.765 | 7.749 | 32,6 | 5,8 | 66,2 |
| PE | 21.418 | 6.883 | 32,1 | 5,2 | 67,2 |
| SC | 17.326 | 5.257 | 30,3 | 4,0 | 25,9 |
| RS | 27.547 | 5.204 | 18,9 | 3,9 | 39,7 |
| MA | 18.093 | 5.051 | 27,9 | 3,8 | 67,0 |
| PA | 20.827 | 4.791 | 23,0 | 3,6 | 51,6 |

**Conclusão.** A janela do congestionamento **não explica** o trecho fora do envelope: ele começa dentro dela, mas continua depois e o desvio é decrescente. A composição por UF (nordeste e sudeste chegando depois) é compatível com o desvio, mas a explicação não foi demonstrada. O item vai para [Questões em aberto](residuos.md). Nada aqui indica alteração de votos; é uma forma da curva que o nulo usado não reproduz.

## 4. Poder de detecção dos boletins impressos

Quantos boletins impressos de seções sorteadas ao acaso seriam necessários para detectar, com 95% e 99% de probabilidade, ao menos uma seção alterada, se uma fração das seções tivesse sido alterada (população de 499.248 seções, amostra sem reposição):

| fracao_alterada | secoes_alteradas | n_para_95 | n_para_99 |
|---|---|---|---|
| 0.1% | 500 | 2.981 | 4.575 |
| 1% | 4.993 | 298 | 458 |
| 2% | 9.985 | 149 | 228 |
| 5% | 24.963 | 59 | 90 |
| 9% | 44.933 | 32 | 49 |

Quantas seções seriam necessárias para inverter a margem de 4.430.191 votos, se cada seção alterada tivesse 5, 50 ou 200 votos trocados (cada voto trocado muda a margem em 2) e quantos boletins sorteados bastariam para flagrar ao menos uma delas:

| trocas_por_secao | secoes_necessarias_para_inverter_a_margem | pct_das_secoes | n_para_95 | n_para_99 |
|---|---|---|---|---|
| 5 | 443.020 | 88,7 | 2 | 3 |
| 50 | 44.302 | 8,9 | 33 | 50 |
| 200 | 11.076 | 2,2 | 134 | 206 |

O cálculo vale para amostra aleatória de seções. Fotos enviadas voluntariamente não são aleatórias e reduzem o poder; o que vale é o total conferido sem divergência, publicado em [Boletins impressos](boletins-impressos.md). Para inverter a margem com 50 trocas por seção, a alteração teria de atingir 8,9% das seções, e uma amostra de 50 boletins a detectaria com 99% de probabilidade.

## 5. Coleta

O cruzamento direto com boletins impressos continua **NÃO EXECUTADO** por falta de insumo. A página [Boletins impressos](boletins-impressos.md) explica como enviar fotos, e o script `04_cruza_bu_impresso.py` está pronto para ser rodado a cada lote.

## 6. Janela dos atrasos: o que ainda falta

- **1º turno:** o teste usa a janela de relógio do Adendo 7 e a comparação dentro do local. Uma janela baseada no log do Sistot (não público) seria mais precisa.
- **2º turno:** o teste compara a ordem de recebimento depois das 19h com a participação de Lula dentro do local, controlando o 1º turno. A comparação com a geografia é a tabela de variância acima.
