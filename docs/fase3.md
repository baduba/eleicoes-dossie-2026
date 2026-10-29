# Fase 3: hipóteses adversariais (A20 a A31)

> **Unidade: votos de margem** (variação da diferença Lula menos Flávio; trocar um voto muda a margem em 2; definição em [Metodologia](metodologia.md)). Margem oficial: 4.430.191. Todo teto é **teto de pior caso, não estimativa**. Os testes de forma não têm teto em votos.

Previsões, critérios e o que cada teste cobre foram registrados no [Adendo 8](preregistro.md) **antes** de rodar. Cada teste descreve a **classe de falha** que cobre e o **rastro esperado** nos dados públicos, não como produzir a falha. Quando falta insumo, o teste fica **NÃO EXECUTADO**, com o insumo e como fornecê-lo.

| teste | classe de falha coberta | resultado | teto em votos de margem | veredito |
|---|---|---|---|---|
| [A20](#a20) Cadastro x Censo | eleitorado apto inflado | 80+ e 90+: fração de municípios com mais aptos que habitantes acima de 2018 e 2022 (formal; ver ressalva); 16+ e 100+: sem excesso | comparecimento 80+ acima das taxas de 2022: 459.099 votos de margem (teto de pior caso, não estimativa; 10,4% da margem) | EXCESSO DETECTADO (forma) em 80+ e 90+, **com ressalva de desenho**; TESTADO-INCONCLUSIVO |
| [A20b-idosos](#a20b) Cadastro de idosos | votantes muito idosos que não existem; liberação manual desigual | votantes 100+ ≈ 5% do Censo, nenhum município com salto de coorte; fração 90+ x liberação manual cresce de 2018 a 2026 (forma); comparecimento nas seções com mais 80+ sobe (forma) | até 241.008 votos de margem (teto de pior caso, não estimativa; 5,4% da margem) no comparecimento | TESTADO-INCONCLUSIVO; EXCESSO DETECTADO (forma) em duas medidas, **com ressalva** |
| [A21](#a21) Logs, ritmo dos votos | registro de votos fora do ritmo real | intervalos < 10 s: nenhum, em nenhum ano; último voto depois do horário nominal explicado pela prorrogação de 25/10 | sem conversão em votos (amostra) | parcial; EXCESSO DETECTADO (forma) em uma medida, **com ressalva** |
| [A22](#a22) Coerência entre cargos | desvio uniforme só no presidente | **NÃO EXECUTÁVEL com a regra registrada** (nenhuma UF de 2026 elegível). Variante exploratória (Adendo 9b), só AM e DF: INCONCLUSIVA | até 548.671 votos de margem (teto de pior caso, não estimativa; 12,4% da margem), **só nos votos de AM e DF** | NÃO EXECUTADO (oficial); INCONCLUSIVA (exploratória) |
| [A23](#a23) Fiscalização | comportamento diferente onde há ou não fiscal | **NÃO EXECUTADO** (sem lista de seções com fiscal) | n/a | NÃO EXECUTADO |
| [A24](#a24) Experimento natural do teste de integridade | urna que se comporta diferente fora do teste | **NÃO EXECUTADO**: nenhuma lista de seções lida das publicações dos TREs (sites bloqueiam acesso automatizado); script e arquivo de entrada prontos | n/a | NÃO EXECUTADO |
| [A25](#a25) Urnas substituídas | troca de urna como ponto de intervenção | seção com troca x vizinhas: ver A6 (sem efeito); antes x depois da troca: NÃO EXECUTADO | n/a (A6: teto abaixo de 1% da margem) | parcial |
| [A26](#a26) Integridade da publicação | arquivo publicado alterado depois | 233 arquivos: tamanho igual em 233; hash oficial igual em 224 de 224; nenhum modificado depois do primeiro download | n/a | SEM ALTERAÇÃO DETECTADA |
| [A27](#a27) Seções fabricadas | seções sem eleitores reais | 427 seções novas com comparecimento ≥ 95%: perfil abaixo | 44.735 votos de margem (teto de pior caso, não estimativa; 1,0% da margem): todos os votos de Lula nas 427 seções, suposto inválidos | TESTADO-INCONCLUSIVO |
| [A28](#a28) Pedidos LAI | dados que só o poder público tem | 6 pedidos prontos em `lai/`, com órgão e canal de cada um; **nenhum protocolado** | n/a | NÃO EXECUTADO |

| [A31](#a31) Municípios extremos na transferência T1 → T2 (Silva Jardim) | transferência de votos entre turnos fora do que os municípios fazem | Silva Jardim: Flávio +1 e comparecimento -104 reproduzem; Lula é +984, não +964. Dentro da cauda esperada (z = 1,13, Holm 1,00); 14,0% dos municípios de 2026 têm oponente com +1 voto ou menos. Três municípios pequenos saem da cauda do modelo principal | Silva Jardim: 207 votos de margem (teto de pior caso, não estimativa; 0,005% da margem). 20 mais extremos: 1.151 além da cauda, 13.327 se tudo o que o modelo não explica fosse manipulação (0,30% da margem) | Silva Jardim: DENTRO DA CAUDA ESPERADA; 3 municípios sinalizados, TESTADO-INCONCLUSIVO |
<a id="a20"></a>

## A20. Cadastro: eleitorado apto x população do Censo 2022

**Pergunta.** Há mais eleitores aptos do que habitantes, por município e faixa etária, e isso mudou entre 2018, 2022 e 2026? **Classe de falha coberta:** eleitorado apto inflado. **Rastro esperado:** razão aptos/população acima de 1 em municípios, concentrada nos mais idosos. **Previsão sem manipulação:** fração de municípios com razão > 1 em 2026 dentro do intervalo de 2018 e 2022, depois de remover o nível nacional.

**Método.** População: Censo 2022 (IBGE, SIDRA 9514), a mesma em todos os anos; por isso 2018 e 2026 têm denominador defasado e cada razão municipal é reescalada pela razão nacional do ano para a escala de 2022 (Adendo 8). Aptos: perfil do eleitorado por zona e faixa etária (1º turno). Mapa TSE x IBGE por nome e UF: 5.557 de 5.757 municípios (200 sem correspondência de nome ficam fora). Municípios com população da faixa abaixo de 100 (16+), 30 (80+), 10 (90+) ou 1 (100+) ficam fora de cada faixa.

| grupo | ano | municipios | razao_nacional | aptos | populacao_2022 | fracao_municipios_razao_gt1_bruta | fracao_razao_gt1_na_escala_de_2022 |
|---|---|---|---|---|---|---|---|
| 16+ | 2018 | 5.557 | 0,917 | 146.677.285 | 160.008.643 | 52,1% | 70,2% |
| 16+ | 2022 | 5.557 | 0,973 | 155.621.019 | 160.008.643 | 68,3% | 68,3% |
| 16+ | 2026 | 5.557 | 0,985 | 157.684.580 | 160.008.643 | 72,1% | 68,4% |
| 80+ | 2018 | 5.544 | 0,892 | 4.089.634 | 4.583.484 | 35,6% | 56,5% |
| 80+ | 2022 | 5.544 | 1,122 | 5.140.993 | 4.583.484 | 65,7% | 66,3% |
| 80+ | 2026 | 5.544 | 1,201 | 5.503.440 | 4.583.484 | 75,4% | 68,4% |
| 90+ | 2018 | 5.237 | 1,278 | 997.035 | 780.045 | 38,1% | 50,2% |
| 90+ | 2022 | 5.237 | 1,775 | 1.384.465 | 780.045 | 57,1% | 59,0% |
| 90+ | 2026 | 5.237 | 1,659 | 1.294.142 | 780.045 | 58,9% | 63,6% |
| 100+ | 2018 | 4.385 | 1,006 | 38.021 | 37.779 | 33,6% | 65,7% |
| 100+ | 2022 | 4.385 | 4,775 | 180.404 | 37.779 | 51,5% | 61,2% |
| 100+ | 2026 | 4.385 | 7,767 | 293.432 | 37.779 | 43,8% | 35,4% |

**Resultado pelo critério pré-registrado (forma, sem teto em votos):**

| grupo | fracao_2026 | comparacao | veredito |
|---|---|---|---|
| 16+ | 68,4% | 2022: dif 0.11 p.p. (z 0.1) / 2018: dif -1.85 p.p. (z -2.1) | SEM EXCESSO (teste de forma, sem conversao em votos) |
| 80+ | 68,4% | 2022: dif 2.11 p.p. (z 2.4) / 2018: dif 11.83 p.p. (z 13.0) | EXCESSO DETECTADO (teste de forma, sem conversao em votos) |
| 90+ | 63,6% | 2022: dif 4.62 p.p. (z 4.9) / 2018: dif 13.39 p.p. (z 14.0) | EXCESSO DETECTADO (teste de forma, sem conversao em votos) |
| 100+ | 35,4% | 2022: dif -25.86 p.p. (z -25.1) / 2018: dif -30.33 p.p. (z -29.8) | SEM EXCESSO (teste de forma, sem conversao em votos) |

> **Ressalva de desenho (leia junto com o veredito).** A fração de municípios com razão > 1 sobe de modo contínuo de 2018 para 2022 e para 2026 em 80+ e 90+, e o teste de interseção-união contra cada ano anterior acusa o último ano de uma série crescente. O salto de 2022 para 2026 (80+: 2,1 p.p.; 90+: 4,6 p.p.) é menor que o de 2018 para 2022 (9,8 e 8,8 p.p.). O rótulo de excesso é formal e **não indica manipulação**; a linha não foi alterada.

**O que chama atenção, sem interpretação causal.** (i) A razão nacional 80+ é 0,89 (2018), 1,12 (2022) e 1,20 (2026) contra o Censo 2022; a 90+ é 1,28, 1,78 e 1,66; a 100+ é 1,0, 4,8 e 7,8: 297.977 aptos com 100 anos ou mais em 2026 contra 37.779 pessoas dessa idade no Censo. A idade dos eleitores vem do cadastro, a do Censo é declarada; uma parte pode ser data de nascimento padrão ou título não cancelado, e o comparecimento nessas faixas é pequeno (0,7% em 100+). (ii) O comparecimento facultativo sobe **em todas as faixas de 70 anos ou mais** de 2022 para 2026:

| faixa | 2018 | 2022 | 2026 |
|---|---|---|---|
| 70 a 74 anos | 55,3% | 61,1% | 68,9% |
| 75 a 79 anos | 37,5% | 41,8% | 52,3% |
| 80 a 84 anos | 24,1% | 27,0% | 37,2% |
| 85 a 89 anos | 13,3% | 15,7% | 24,3% |
| 90 a 94 anos | 4,9% | 6,7% | 13,5% |
| 95 a 99 anos | 1,9% | 1,6% | 4,3% |
| 100 anos ou mais | 3,9% | 0,9% | 0,7% |

Se o comparecimento de 2026 nas faixas de 80 anos ou mais tivesse ficado nas taxas de 2022, haveria 459.099 votantes a menos. **Teto de pior caso, não estimativa:** 459.099 votos de margem (10,4% da margem), se todo esse aumento fosse voto adicional de um só candidato, o que os dados não indicam: o aumento aparece também em 70 a 74 e 75 a 79 anos, o que aponta para um fenômeno geral da faixa facultativa. **Situação:** TESTADO-INCONCLUSIVO. **O que fecharia:** cruzamento do cadastro com o registro civil de óbitos por entidade fiscalizadora, e perfil por seção.

**Linha A20b do Adendo 8 (perfil de idade e sexo das seções novas).** Continua NÃO EXECUTADO. O registro dizia que o perfil público é só por zona; **isso estava errado**: o TSE publica o perfil do eleitorado por seção (`perfil_eleitor_secao`), que passou a ser usado na seção seguinte. O teste das seções novas com esse insumo não foi feito nesta rodada.

<a id="a20b"></a>

## A20b-idosos. Cadastro e comparecimento dos mais idosos (Fase 3.1)

Registro: [Adendos 9, 9a e 9d](preregistro.md). O rótulo é A20b-idosos para não colidir com a linha A20b do Adendo 8. **Previsão sem manipulação:** votantes 100+ compatíveis com o Censo; liberação manual nessas faixas igual entre anos; comparecimento e voto sem associação com a fração de idosos da seção.

### 1. Regra legal do cancelamento

- **Ausência a três eleições consecutivas:** [Código Eleitoral](https://www.planalto.gov.br/ccivil_03/leis/l4737compilado.htm), art. 71, V, e art. 7º, § 3º (cancelamento de quem não vota em três eleições consecutivas, não paga a multa ou não se justifica). A [Resolução TSE 23.659/2021](https://www.tse.jus.br/legislacao/compilada/res/2021/resolucao-no-23-659-de-26-de-outubro-de-2021), art. 130, conta cada turno como uma eleição (§ 1º) e **afasta a regra de quem tem voto facultativo** (§ 2º): maiores de 70 anos, analfabetos e eleitores de 16 e 17 anos (Constituição, art. 14, § 1º, II). Em 2025 a Justiça Eleitoral cancelou cerca de 5 milhões de títulos de faltosos (imprensa, a partir de dados do TSE); **eleitor facultativo ausente não entra nessa conta**.
- **Óbito:** Código Eleitoral, art. 71, IV (falecimento do eleitor), com comunicação **mensal** dos cartórios de Registro Civil para cancelamento das inscrições (art. 71, § 3º).
- **Consequência para o teste:** como a ausência não cancela o título do eleitor facultativo, **aptos acima do Censo nas faixas mais velhas não indicam voto**; só os votantes indicam. Títulos de falecidos ainda não comunicados permanecem no cadastro.
- **Limite da verificação:** o Código Eleitoral foi lido no texto do Planalto; a Resolução 23.659 está em site que bloqueia acesso automatizado, e os parágrafos citados vêm de resumo de busca e de páginas de TREs; confira no link oficial. O artigo da Resolução sobre óbito não foi confirmado.

### 2. Votantes 90+ e 100+ contra o Censo 2022, por município

> **Aviso de desenho (Adendo 9a).** O Censo é de 2022: só 2022 compara a mesma coorte. Em 2026 a faixa 90+ é a coorte de 86+ em 2022 e em 2018 é a de 94+, então as razões de 2018 e 2026 não são comparáveis em forma. Por isso o veredito formal deste item não é usado como conclusão; vale o teste 2a.

| ano | turno | faixa | votantes | populacao_censo_2022 | razao_nacional | municípios (pop. mínima) com votantes > população | municípios na lista completa | votantes acima da população | aviso |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | 1 | 90+ | 39.984 | 779.711 | 5,1% | 0 | 1 | 1 | descompasso de coortes (Adendo 9a) |
| 2018 | 1 | 100+ | 1.178 | 32.492 | 3,6% | 0 | 47 | 50 | descompasso de coortes (Adendo 9a) |
| 2018 | 2 | 90+ | 41.139 | 779.711 | 5,3% | 0 | 1 | 2 | descompasso de coortes (Adendo 9a) |
| 2018 | 2 | 100+ | 1.170 | 32.492 | 3,6% | 0 | 48 | 53 | descompasso de coortes (Adendo 9a) |
| 2022 | 1 | 90+ | 58.582 | 779.993 | 7,5% | 0 | 1 | 2 | mesma coorte |
| 2022 | 1 | 100+ | 1.314 | 32.492 | 4,0% | 0 | 40 | 41 | mesma coorte |
| 2022 | 2 | 90+ | 75.302 | 779.993 | 9,7% | 0 | 1 | 1 | mesma coorte |
| 2022 | 2 | 100+ | 1.663 | 32.492 | 5,1% | 0 | 44 | 45 | mesma coorte |
| 2026 | 1 | 90+ | 105.442 | 780.012 | 13,5% | 4 | 20 | 46 | descompasso de coortes (Adendo 9a) |
| 2026 | 1 | 100+ | 1.624 | 32.492 | 5,0% | 1 | 83 | 91 | descompasso de coortes (Adendo 9a) |

Os votantes são uma pequena fração da população da faixa (cerca de 14% em 90+ e 5% em 100+ em 2026). Em 2026 (1º turno), 20 municípios têm mais votantes 90+ que habitantes 90+ no Censo (46 votantes a mais no total) e 83 municípios têm mais votantes 100+ que habitantes 100+ (91 votantes a mais), quase todos municípios de população minúscula na faixa. Em 2022 e 2018 a lista de 100+ tem tamanho parecido (40 a 48 municípios) e a de 90+ tem 1 município; os 20 de 2026 em 90+ são o efeito esperado do descompasso de coortes (a faixa de 2026 inclui quem tinha 86 a 89 anos no Censo), não uma conclusão. **Teto de pior caso, não estimativa:** 137 votos de margem se todos esses votantes fossem votos de um só candidato (menos de 0,01% da margem). Lista completa: `results/fase3/A20b_item2_lista_municipios_2026T1.csv`. **2º turno de 2026: NÃO EXECUTADO** (o perfil de comparecimento do 2º turno de 2026 não foi publicado; o arquivo no CDN do TSE traz só o 1º turno, última modificação em 21/10/2026).

### 2a. Monotonicidade de coortes (sem Censo)

Uma pessoa não fica mais jovem: o cadastro de 2026 com 95+ vem do cadastro de 2022 com 91+, contido em 90+; e 100+ em 2026 vem de 96+ em 2022, contido em 95+. R = numerador de 2026 / aptos da faixa anterior em 2022; o placebo é o mesmo par quatro anos antes (2022 contra 2018). 1º turno.

| numerador / denominador | par | medida | municipios | R_nacional | ep_R | fração de municípios com R > 1 | municípios com R > 1 |
|---|---|---|---|---|---|---|---|
| 95+ em y2 / 90+ em y1 | 2026 contra 2022 | aptos | 5.147 | 0,4573 | 0,0448 | 0,02% | 1 |
| 95+ em y2 / 90+ em y1 | 2026 contra 2022 | votantes | 5.147 | 0,0120 | 0,0010 | 0,00% | 0 |
| 95+ em y2 / 90+ em y1 | 2022 contra 2018 | aptos | 4.411 | 0,6522 | 0,0098 | 0,11% | 5 |
| 95+ em y2 / 90+ em y1 | 2022 contra 2018 | votantes | 4.411 | 0,0090 | 0,0007 | 0,00% | 0 |
| 100+ em y2 / 95+ em y1 | 2026 contra 2022 | aptos | 3.296 | 0,4593 | 0,0509 | 0,00% | 0 |
| 100+ em y2 / 95+ em y1 | 2026 contra 2022 | votantes | 3.296 | 0,0029 | 0,0004 | 0,00% | 0 |
| 100+ em y2 / 95+ em y1 | 2022 contra 2018 | aptos | 2.530 | 0,5967 | 0,0034 | 0,08% | 2 |
| 100+ em y2 / 95+ em y1 | 2022 contra 2018 | votantes | 2.530 | 0,0047 | 0,0005 | 0,00% | 0 |

**Leitura.** (i) Nenhum município tem R > 1 para votantes (nenhum votante 95+ ou 100+ de 2026 acima dos aptos da faixa anterior de 2022 no mesmo município), e para aptos há 1 caso em 2026 contra 7 em 2022. (ii) A razão nacional de aptos **cai** (95+/90+: 45,7% em 2026 contra 65,2% em 2022), compatível com mortalidade e com limpeza do cadastro por óbitos (não investigado; o cancelamento por ausência não alcança o eleitor facultativo). (iii) A razão nacional de **votantes** 95+ sobre aptos 90+ anteriores sobe de 0,90% para 1,20% (z = 2,42; p unilateral 0,0077; p corrigido por Holm 0,054): pelo corte de 2 erros padrão do Adendo 9a é "excesso formal"; pelo critério de veredito do Adendo 2 (Holm) não passa de 0,05 por pouco. **Os dois ficam registrados.** São cerca de 17 mil votantes 95+ em 2026 contra cerca de 9 mil em 2022, e a diferença acompanha o aumento geral do comparecimento facultativo (A20). Para 100+ não há excesso. **Teto de pior caso, não estimativa:** pela soma municipal (municípios com R > 1), 0 votos de margem em 95+ e 2 em 100+. **Pela diferença de razão** (exploração do Adendo 9e, fator 1: um votante a mais, se fosse de um só candidato, muda a margem em 1): estimativa central de 4.205 votantes 95+ a mais do que a razão de 2022 daria (de 16.659 votantes), e **teto de pior caso, não estimativa, de 7.059 votos de margem (0,16% da margem)**, ao lado de z = 2,42 e Holm 0,054.

### 3. Biometria por faixa etária

O perfil de comparecimento **não traz biometria**. O perfil do eleitorado por seção traz a **biometria cadastrada** por faixa (não é a liberação manual do dia, que vem do boletim, por seção, sem idade).

| ano | grupo | aptos | com_biometria | pct_biometria |
|---|---|---|---|---|
| 2018 | 100+ | 39.026 | 4.348 | 11,1% |
| 2018 | 90+ (inclui 100+) | 1.000.128 | 103.892 | 10,4% |
| 2018 | 16 a 89 anos | 145.802.513 | 87.237.302 | 59,8% |
| 2022 | 100+ | 184.330 | 11.385 | 6,2% |
| 2022 | 90+ (inclui 100+) | 1.389.277 | 253.406 | 18,2% |
| 2022 | 16 a 89 anos | 154.365.669 | 117.767.701 | 76,3% |
| 2026 | 100+ | 297.977 | 23.834 | 8,0% |
| 2026 | 90+ (inclui 100+) | 1.299.595 | 471.039 | 36,2% |
| 2026 | 16 a 89 anos | 156.525.783 | 140.607.027 | 89,8% |

**3b. Liberação manual do boletim contra a fração de aptos 90+ da seção** (efeito fixo de local, controle da fração sem biometria cadastrada; coeficiente por unidade de fração; erro padrão agrupado por local):

| ano | turno | coef | ep | n | locais |
|---|---|---|---|---|---|
| 2018 | 2 | 0,346 | 0,020 | 426.320 | 66.691 |
| 2022 | 2 | 0,638 | 0,009 | 447.114 | 68.546 |
| 2026 | 1 | 0,706 | 0,009 | 475.668 | 72.402 |
| 2026 | 2 | 0,797 | 0,009 | 475.662 | 72.400 |

Resultado pelo critério pré-registrado: **EXCESSO DETECTADO (teste de forma, sem conversao em votos)**, p corrigido 9.8e-13. **Ressalva de tendência (Adendo 9d):** o coeficiente cresce em todos os anos, de 0,35 (2018) a 0,64 (2022), 0,71 (2026, 1º turno) e 0,80 (2026, 2º turno); de um ciclo eleitoral para o seguinte o aumento já era grande antes (+0,29 de 2018 para 2022 e +0,16 de 2022 para 2026, ambos no 2º turno), e entre os dois turnos de 2026 é de +0,09. Quer dizer que, dentro do mesmo local, onde há mais eleitores de 90+ há mais liberação manual, e isso vem aumentando. O rótulo é formal, **não indica manipulação** e não tem conversão em votos. Para 100+ o coeficiente adicional é negativo (sem excesso). A idade de quem foi liberado manualmente **não é observável com dados públicos**; é um proxy ecológico por seção.

### 4. Seções com alta fração de aptos 80+

Resultados do 2º turno, dentro do mesmo local de votação, com o desfecho do 1º turno como controle. Coeficiente por unidade de fração de aptos 80+ da seção (a fração média é 3%; o decil superior dentro da UF tem 11%).

| desfecho | comparador | coef | ep |
|---|---|---|---|
| dir_sh | 2026/T2 | 0,0279 | 0,0013 |
| dir_sh | 2022/T2 | -0,0622 | 0,0014 |
| dir_sh | 2018/T2 | 0,2317 | 0,0043 |
| lula_sh | 2026/T2 | -0,0279 | 0,0013 |
| lula_sh | 2022/T2 | 0,0622 | 0,0014 |
| lula_sh | 2018/T2 | -0,2317 | 0,0043 |
| turnout | 2026/T2 | 0,0378 | 0,0018 |
| turnout | 2026/T1 | -0,6925 | 0,0029 |
| turnout | 2022/T2 | -0,0003 | 0,0018 |
| turnout | 2018/T2 | -0,0015 | 0,0019 |

(a linha 2026/T1 de comparecimento é o comparador sem controle; ver abaixo.)

Descrição, sem teste (2º turno de 2026, decil superior de fração 80+ dentro da UF contra as demais seções): comparecimento 77,1% contra 81,4%; Lula 52,9% contra 51,7% dos votos válidos; liberação manual média 9,2% contra 6,6%. Tabela completa por ano e turno em `results/fase3/A20b_4_descritivo_decil_superior.csv`.

| H | teste | est_2026T2 | p_holm | votos_max_pior_caso | pct_pior_caso | veredito |
|---|---|---|---|---|---|---|
| A20b-4 | participacao de Lula nos votos validos contra a fracao de aptos 80+ da secao (EF de local, controle do 1o turno) | -0,0279 | 1.0e+00 | 1.787.533 | 40,3% | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| A20b-4 | participacao de Flavio nos votos validos contra a fracao de aptos 80+ da secao (EF de local, controle do 1o turno) | 0,0279 | 1.0e+00 | 790.398 | 17,8% | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| A20b-4 | comparecimento contra a fracao de aptos 80+ da secao (EF de local, controle do 1o turno) | 0,0378 | 9.3e-52 | 4.070.526 | 91,9% | EXCESSO DETECTADO e relevante (pior caso >= 1% da margem) |
| A20b-4-suplementar | comparecimento contra a fracao de aptos 80+ da secao, so placebos controlados (2022/T2 e 2018/T2) | 0,0378 | 1.0e-52 | 241.008 | 5,4% | EXCESSO DETECTADO e relevante (pior caso >= 1% da margem) |

**Leitura.** (i) **Participação:** os coeficientes de Lula (-0,028) e de Flávio (+0,028) ficam **dentro do intervalo dos placebos** (Lula: +0,062 em 2022 e -0,232 em 2018); não há excesso medido. Os tetos de 1.787.533 (a favor de Lula) e 790.398 (a favor de Flávio) votos de margem são **teto de pior caso, não estimativa** e vêm da dispersão entre os anos de comparação (os idosos votaram de modo muito diferente em 2018 e 2022), não de um efeito medido. (ii) **Comparecimento:** nas seções com mais aptos 80+ o comparecimento de 2026 (2º turno) sobe mais, dado o do 1º turno, do que em 2022 e 2018 (+0,038 contra cerca de zero); é **excesso formal**. Com todos os comparadores do Adendo 9 o teto sai em 4.070.526 votos de margem (91,9%), mas o comparador 2026/T1 não tem o controle do 1º turno e é de outra especificação; **a linha suplementar do Adendo 9d**, só com os placebos controlados, dá **241.008 votos de margem (5,4% da margem), teto de pior caso, não estimativa**, se todo o comparecimento adicional fosse voto de um só candidato. Os dados não indicam isso: o coeficiente de participação de Lula nessas mesmas seções é negativo. (iii) Combina com o achado de A20 (comparecimento facultativo sobe em todas as faixas de 70 anos ou mais), mas aqui dentro do mesmo local e por seção. **Situação: TESTADO-INCONCLUSIVO.** **O que fecharia:** listas assinadas de habilitação das seções com mais idosos e o cruzamento do cadastro com o registro civil de óbitos, por entidade fiscalizadora.

### 5. Quantos eleitores mais velhos votaram (exploração, Adendo 9e)

Votantes e comparecimento por faixa, 1º turno (comparável entre os três anos). Até os 69 anos o voto é **obrigatório**; a partir dos 70 é **facultativo**. Os dados públicos dizem quantos votaram, não em quem.

| faixa | votantes 2018 | comparecimento 2018 | votantes 2022 | comparecimento 2022 | votantes 2026 | comparecimento 2026 | 2026 contra 2022 (votantes) |
|---|---|---|---|---|---|---|---|
| 60 a 69 anos (obrigatório) | 13.154.983 | 83,9% | 15.395.122 | 85,8% | 17.552.428 | 87,3% | 2.157.306 (+14%) |
| 70 anos ou mais | 4.480.899 | 37,3% | 6.120.350 | 41,2% | 8.755.306 | 50,9% | 2.634.956 (+43%) |
| 90 anos ou mais | 40.270 | 4,0% | 59.011 | 4,2% | 106.332 | 8,2% | 47.321 (+80%) |
| 95 anos ou mais | 6.588 | 2,1% | 9.266 | 1,4% | 16.802 | 2,6% | 7.536 (+81%) |
| 100 anos ou mais | 1.506 | 3,9% | 1.675 | 0,9% | 2.141 | 0,7% | 466 (+28%) |

**Leitura.** (i) Quem tem 60 a 69 anos vota: 84%, 86% e 87% de comparecimento em 2018, 2022 e 2026. A abstenção grande está a partir dos 70, quando o voto é facultativo. (ii) De 2018 para 2022 (a eleição geral anterior à de 2026) os votantes de 70 anos ou mais sobem de 4.480.899 para 6.120.350 e de 2022 para 2026 sobem para 8.755.306; o comparecimento dessa faixa vai de 37% a 41% e a 51%. O aumento é **geral na faixa facultativa nos três anos**, e maior de 2022 para 2026 (isso já aparece em A20). (iii) Em 90+, os votantes sobem 80% de 2022 para 2026 (59.011 para 106.332) enquanto o cadastro 90+ cai (1,39 milhão para 1,30 milhão): o comparecimento passa de 4,2% para 8,2% (1º turno). Em 100+ os votantes são 2.141 em 2026. (iv) **Em votos de margem:** os votantes 95+ de 2026 equivalem a 0,38% da margem se todos votassem no mesmo candidato (um voto a mais muda a margem em 1); o teste de 95+ acima dá o teto sobre o **excesso** em relação ao de 2022. Não há idade nem voto associados no dado público, então nada disso diz em quem votaram. Tabela completa, com 2º turno de 2018 e 2022: `results/fase3/A20b_montante_votantes_por_faixa.csv`.

Dados: `results/fase3/A20b_*.csv`; scripts `scripts/30_perfil_secao.py` e `scripts/31_a20b_idosos.py`.

<a id="a21"></a>

## A21. Forense temporal dos logs de urna (parcial)

**Pergunta.** O ritmo dos votos ao longo do dia é igual ao de 2022 e não tem relação com o voto? **Classe de falha coberta:** registro de votos fora do ritmo da votação real. **Rastro esperado:** intervalos muito curtos entre votos, rajadas, concentração na última hora. **Previsão sem manipulação:** padrões iguais em 2022 e 2026, sem associação com o voto.

**Executado** com as medidas já extraídas dos logs da amostra de arquivos de urna (seções pareadas entre 2022 e 2026). **NÃO EXECUTADO:** distribuição completa dos intervalos, rajadas por ano de nascimento (o ano de nascimento não consta nos logs públicos) e concentração na última hora; exigem reler os logs.

| medida | secoes_pareadas | media_2026 | media_2022 | diferenca_media | ep | pct_secoes_com_valor_positivo_2026 | pct_secoes_com_valor_positivo_2022 |
|---|---|---|---|---|---|---|---|
| intervalos < 5 s entre habilitacoes, por 100 votos | 12.456 | 0,000 | 0,000 | 0,000 | 0,000 | 0,0 | 0,0 |
| intervalos < 10 s entre habilitacoes, por 100 votos | 12.456 | 0,000 | 0,000 | 0,000 | 0,000 | 0,0 | 0,0 |
| minutos do ultimo voto depois do horario nominal de fechamento | 12.456 | 5,625 | -8,022 | 13,646 | 0,309 | 28,0 | 13,0 |
| votos depois do horario nominal, por 100 votos | 12.456 | 0,215 | 0,091 | 0,124 | 0,030 | 28,0 | 13,0 |

Nenhuma seção, em nenhum dos dois anos, tem dois votos com intervalo menor que 10 segundos. O último voto vem depois do horário nominal em 28,0% das seções em 2026 contra 13,0% em 2022, o que é compatível com a prorrogação do 2º turno decidida em 25/10/2026 ([A18](a18-alteracao-no-meio.md), [A5](resultados-fase2.md)).

| teste | est_2026T2 | placebos | p_excesso | p_holm | veredito |
|---|---|---|---|---|---|
| associacao com a participacao de Lula (T2, EF de local, controle T1): minutos do ultimo voto depois do horario nominal de fechamento | 0,00001 | 2022/T2 (mesmas secoes): -0.00006 (ep 0.00003, p_exc 0.00548) | 0,005 | 0,011 | EXCESSO DETECTADO (teste de forma, sem conversao em votos) |
| associacao com a participacao de Lula (T2, EF de local, controle T1): votos depois do horario nominal, por 100 votos | -0,00002 | 2022/T2 (mesmas secoes): 0.00009 (ep 0.00010, p_exc 0.837) | 0,837 | 0,837 | SEM EXCESSO (teste de forma, sem conversao em votos) |

> **Ressalva.** Na medida "minutos do último voto depois do horário nominal" o coeficiente de 2026 é indistinguível de zero (0,00001 por minuto); a diferença para o critério vem do coeficiente negativo de 2022 (-0,00006), único placebo. Na seção média, 5,6 minutos de atraso somam cerca de 0,04 ponto percentual. O rótulo é formal e **não indica manipulação**. A amostra é de arquivos de urna, não nacional, então não há teto em votos.

<a id="a22"></a>

## A22. Coerência entre cargos

**Classe de falha coberta:** desvio uniforme restrito ao cargo de presidente, invisível a testes de valor atípico. **Rastro esperado:** deslocamento sistemático entre a participação do candidato presidencial e a do governador alinhado a ele na mesma seção. **Previsão sem manipulação:** deslocamento de 2026 igual ao de 2022 e 2018. **Insumo usado:** tabelas de coligações do TSE (2018, 2022, 2026) e os BWebs de 2º turno dos três anos (votos por candidato e seção, presidente e governador). **Regra de alinhamento** (Adendo 9), decidida só pela composição das coligações, antes de olhar votos: o finalista a governador é alinhado a um candidato presidencial se mais da metade dos partidos da sua coligação (federações expandidas) está na coligação presidencial dele e menos da metade na do outro.

**Resultado pela regra registrada: NÃO EXECUTÁVEL em 2026.** Das seis UFs com 2º turno de governador, nenhuma ficou com os dois finalistas alinhados a candidatos presidenciais diferentes. Motivo visível na composição: o oponente do PT concorreu à presidência por partido isolado (coligação de um só partido), então a coligação de um governador raramente passa de 50% em comum com ele; em AM a coligação do candidato do PT tem exatamente 50%, e a regra pede mais de 50%.

| SG_UF | cand1 | alinhamento 1 | cand2 | alinhamento 2 | elegivel |
|---|---|---|---|---|---|
| AC | MAILZA ASSIS (PP) | nenhum | ALAN RICK (REPUBLICANOS) | nenhum | False |
| AM | OMAR AZIZ (PSD) | nenhum | PROFESSORA MARIA DO CARMO (PL) | nenhum | False |
| DF | CELINA LEÃO (PP) | nenhum | LEANDRO GRASS (PT) | PT | False |
| ES | LORENZO PAZOLINI (REPUBLICANOS) | nenhum | RICARDO FERRAÇO (MDB) | nenhum | False |
| RN | CADU DE LULA (PT) | PT | ALLYSON (UNIÃO) | nenhum | False |
| TO | VICENTINHO JÚNIOR (PSDB) | nenhum | PROFESSORA DORINHA (UNIÃO) | nenhum | False |

> **Desvio declarado (Adendo 9b), escrito depois de ver só a tabela acima e antes de ler qualquer voto de governador.** Variante exploratória: o finalista é alinhado a um candidato presidencial se o **partido** dele está na coligação ou federação do finalista e o do outro não está. Fica **fora da família principal** e **não substitui** a linha oficial NÃO EXECUTÁVEL.

**Variante 9b.** Deslocamento S = média, ponderada por votos válidos presidenciais, de (participação do candidato do PT para presidente) menos (participação do governador alinhado a ele); positivo quer dizer presidente à frente do governador. Erro padrão agrupado por município.

| ano | UFs_elegiveis | secoes | votos_validos_pres | S | ep | municipios |
|---|---|---|---|---|---|---|
| 2026 | AM,DF | 15.081 | 3.917.365 | -2,58 p.p. | 2,77 p.p. | 63 |
| 2022 | AM,ES,SC,SP | 133.926 | 34.306.139 | -0,16 p.p. | 0,27 p.p. | 1.080 |
| 2018 |  | 0 | 0 | nenhuma UF elegível |  |  |

Por UF (mesma estatística):

| ano | SG_UF | secoes | votos_validos_pres | S |
|---|---|---|---|---|
| 2026 | AM | 8.115 | 2.112.664 | -7,24 p.p. |
| 2026 | DF | 6.966 | 1.804.701 | 2,88 p.p. |
| 2022 | AM | 7.427 | 1.962.447 | 7,90 p.p. |
| 2022 | ES | 9.237 | 2.208.871 | -11,85 p.p. |
| 2022 | SC | 16.228 | 4.399.210 | 1,37 p.p. |
| 2022 | SP | 101.034 | 25.735.611 | -0,03 p.p. |

| teste | est_2026T2 | placebos | p_excesso | p_holm | votos_max_pior_caso | pct_pior_caso | veredito |
|---|---|---|---|---|---|---|---|
| participacao do candidato do PT para presidente menos a do governador alinhado, 2o turno | -2,58 p.p. | 2022/T2: -0.00158 (ep 0.00266, p_exc 0.808) | 0,808 | 0,808 | 169.390 | 3,8% | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| participacao do oponente para presidente menos a do governador alinhado a ele (lado simetrico), 2o turno | 2,58 p.p. | 2022/T2: 0.00158 (ep 0.00266, p_exc 0.192) | 0,192 | 0,385 | 548.671 | 12,4% | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |

> **Leitura e limites.** (1) São só duas UFs em 2026 (AM e DF), e o desvio entre UFs é grande nos dois sentidos: no placebo de 2022 o deslocamento por UF vai de -11,8 a +7,9 p.p., e em 2026 vai de -7,2 a +2,9 p.p. O erro padrão agrupado por município (63 municípios em 2026) **não captura essa variação entre UFs**; com duas UFs ela não é estimável. Os valores de 2026 ficam dentro do intervalo de 2022 por UF, mas isso é descrição, não teste pré-registrado. (2) Os tetos valem **apenas** para os 3.917.365 votos válidos de AM e DF; **não** cobrem o país. São **teto de pior caso, não estimativa**, e saem grandes porque o teste tem pouco poder. (3) O sinal de S em 2026 é negativo (candidato do PT atrás do governador alinhado), o que não é o sentido de uma inflação a favor dele. (4) Resultado: **INCONCLUSIVA**; a linha oficial de A22 continua **NÃO EXECUTADO** (regra registrada sem UF elegível). **O que fecharia:** os votos por candidato em todos os cargos por seção para as 27 UFs, com uma regra de alinhamento definida por quem conhece as alianças locais (por exemplo, partidos que declararam apoio formal); ou deputados federais por partido nas UFs sem 2º turno de governador.

Dados: `results/fase3/A22_*.csv`; script `scripts/32_a22_coerencia_cargos.py`; tabelas de coligações em `data/urls_origem.txt` com SHA-256 em `data/sha256_entradas.txt`.

<a id="a23"></a>

## A23. Fiscalização: NÃO EXECUTADO

**Classe de falha coberta:** comportamento diferente onde há ou não fiscal. **Previsão sem manipulação:** sem diferença entre seções com e sem fiscal, dentro do mesmo local, com controle do 1º turno e de 2022. **Como fornecer o insumo (partidos e coligações):** uma planilha CSV com as colunas `uf;cd_municipio;zona;secao;turno;partido_ou_coligacao;fiscal_presente` (`sim` ou `nao`), sem nome nem documento de pessoa, enviada por issue. O script comparará seções com e sem fiscal e publicará o resultado, inclusive se for nulo.

<a id="a24"></a>

## A24. Experimento natural do teste de integridade: NÃO EXECUTADO

**Classe de falha coberta:** urna que se comporta diferente quando não é o teste. **Desenho** (Adendos 8, 9 e 9c): seções cuja urna foi sorteada para o teste (votaram em urna reserva) contra as demais seções do mesmo local, com efeito fixo de local e controle do 1º turno; comparador: 2022/T2 com o mesmo controle; a diferença do 1º turno de 2026 sem controle é balanço pré-tratamento. **O que foi feito:** a lista de seções deve vir das **publicações dos TREs**, uma fonte por UF. O levantamento está em `data/a24_fontes_por_uf.csv`: foram localizadas páginas de 9 TREs (SP, SE, SC, PB, MA, MG, MT, ES, DF) com notícia do sorteio; **nenhuma lista de zona e seção foi lida**, porque os sites dos TREs respondem 403 a acesso automatizado (o projeto não disfarça o agente para contornar o bloqueio) e os resumos de busca trazem a quantidade de urnas, não a tabela. Para as demais UFs a página não foi localizada nesta rodada.

**Resultado:** NÃO EXECUTADO (regra do Adendo 9: menos de 10 seções lidas). O script `scripts/33_a24_teste_integridade.py` está pronto e foi testado com uma lista sintética de 80 seções ao acaso, descartada, que serviu para achar e corrigir um defeito de desenho (Adendo 9c). **Como fornecer o insumo:** preencher `data/a24_secoes_teste_integridade.csv` (UF, município, zona, seção, turno, tipo de teste, biometria, URL da publicação do TRE e data de acesso; uma linha por seção) e rodar o script; ou enviar a planilha por issue. **Poder esperado:** com 20 a 30 seções por UF e turno e desvio local de 1,67 p.p., o teste só vê diferenças médias acima de cerca de 1 p.p. com 100 seções; o script informa o menor efeito detectável. **Pedido LAI relacionado:** `lai/03_teste_de_integridade.md`.

**Cobertura atual: 0 de 27 UFs.** O teste roda com as UFs disponíveis e marca a cobertura como parcial; o autor começará por SP, MG, RJ, BA, PR, RS, PE e CE.

<a id="a25"></a>

## A25. Urnas substituídas (parcial)

**Classe de falha coberta:** troca de urna como ponto de intervenção. **Feito:** seções com urna diferente da esperada contra vizinhas do mesmo local ([A6](resultados-fase2.md)): urna efetivada diferente da esperada: Lula% no T2 dado o T1, EF de loc... REFUTADA (sem excesso, teto <1% da margem). **NÃO EXECUTADO:** voto antes x depois da troca pelos logs, porque o registro da urna original não é público. O total de 1.543 trocas no 1º turno citado ao autor não tem fonte localizada; a imprensa registra 421 até as 10h de 04/10/2026. **Insumo:** pedido LAI 01.

<a id="a26"></a>

## A26. Integridade da publicação

**Classe de falha coberta:** arquivo publicado alterado depois da publicação. **Rastro esperado:** hash oficial, tamanho ou data de modificação diferentes dos do primeiro download. **Previsão sem manipulação:** todos idênticos.

**Resultado (2026-10-29):** dos 233 arquivos de origem, 233 seguem disponíveis; o tamanho de 233 é igual ao do primeiro download; o hash oficial publicado hoje é igual ao do primeiro download em 224 de 224 conferidos (0 diferentes); 0 têm data de modificação posterior ao primeiro download. **Arquivos alterados após a publicação: 0.** Capturas no Wayback Machine: 41 arquivos têm captura; 151 não puderam ser consultados (limite de taxa do serviço). Das 63 capturas com resposta 200, 54 têm o mesmo resumo (SHA-1) do arquivo que baixei e 9 têm resumo diferente (arquivos que o TSE republicou depois da captura, ou capturas parciais; cada caso está em `A26_integridade_publicacao.csv`).

**Limite:** os zips (cerca de 8 GB) não foram baixados de novo; foram comparados tamanho e hash oficial publicado. A reconferência integral é `data/baixar_e_verificar.sh`. Isso verifica que o que está publicado hoje é o que foi baixado; **não** verifica o que o TSE publicou antes do primeiro download. Dados em `results/fase3/A26_integridade_publicacao.csv`.

### Arquivos republicados depois da captura no Wayback Machine

Em 9 capturas de 4 arquivos o resumo (SHA-1) da captura é diferente do arquivo que baixei. Em todos eles a data de modificação publicada hoje é posterior à captura, o que indica **republicação pelo TSE depois da captura**, e não alteração depois do meu primeiro download (o tamanho de hoje é o do meu download e a data de modificação é anterior ao meu download; esses arquivos não têm hash oficial publicado). Para saber se a republicação mudou números, comparei seção a seção (cargo de Presidente) a captura com o arquivo atual:

| arquivo | modificado_em (GMT) | meu_download | capturas | primeira_captura |
|---|---|---|---|---|
| detalhe_votacao_secao_2026.zip | Mon, 26 Oct 2026 15:35:35 GMT | 2026-10-28T20:05:19 | 3 | 20261007 |
| detalhe_votacao_secao_2022.zip | Fri, 31 Jul 2026 19:47:56 GMT | 2026-10-28T20:05:17 | 2 | 20221105 |
| detalhe_votacao_secao_2018.zip | Thu, 09 Apr 2026 16:48:22 GMT | 2026-10-28T20:39:57 | 3 | 20221105 |
| votacao_candidato_munzona_2026.zip | Wed, 28 Oct 2026 23:14:43 GMT | 2026-10-28T20:40:10 | 1 | 20261010 |

- **detalhe_votacao_secao_2022 (captura de 01/11/2022 contra o arquivo atual):** 944.150 seções em comum, 0 só na captura, 0 só no arquivo atual. Colunas de votos e comparecimento (`QT_*`): **0 diferenças em 8 colunas**. Colunas com diferença: `NM_TIPO_ELEICAO` (944.150), `DS_ELEICAO` (944.150), `DS_CARGO` (944.150), `NR_LOCAL_VOTACAO` (12.246), `NM_LOCAL_VOTACAO` (404), `DS_LOCAL_VOTACAO_ENDERECO` (32.565). Colunas acrescentadas no arquivo atual: `DT_RECEBIMENTO_BU_HOR_TSE`, `DT_PRIM_TOT_PARCIAL_HOR_TSE`, `DS_ORIGEM_VOTO`, `ST_SECAO_INSTALADA`, `ST_SECAO_ANULADA`, `CD_MODELO_URNA`, `DS_MODELO_URNA`.
- **detalhe_votacao_secao_2018 (captura de 14/07/2021 contra o arquivo atual):** 908.980 seções em comum, 0 só na captura, 0 só no arquivo atual. Colunas de votos e comparecimento (`QT_*`): **0 diferenças em 8 colunas**. Colunas com diferença: `NR_LOCAL_VOTACAO` (29.538). Colunas acrescentadas no arquivo atual: `NM_LOCAL_VOTACAO`, `DS_LOCAL_VOTACAO_ENDERECO`, `DT_RECEBIMENTO_BU_HOR_TSE`, `DT_PRIM_TOT_PARCIAL_HOR_TSE`, `DS_ORIGEM_VOTO`, `ST_SECAO_INSTALADA`, `ST_SECAO_ANULADA`, `CD_MODELO_URNA`, `DS_MODELO_URNA`.
- **detalhe_votacao_secao_2026 (captura de 05/10/2026 contra o arquivo atual):** 499.248 seções em comum, 0 só na captura, 499.248 só no arquivo atual. Colunas de votos e comparecimento (`QT_*`): **0 diferenças em 8 colunas**. Colunas com diferença: `NR_LOCAL_VOTACAO` (421), `NM_LOCAL_VOTACAO` (400), `DS_LOCAL_VOTACAO_ENDERECO` (409). Colunas acrescentadas no arquivo atual: nenhuma.

Leitura: os números de votação e comparecimento da captura de novembro de 2022 e do arquivo de hoje são **iguais**; a republicação mudou rótulos, a identificação dos locais de votação e acrescentou colunas (inclusive os horários de recebimento do boletim, que por isso **não têm captura contemporânea** para 2018 e 2022). Para 2026, a captura de 07/10/2026 cobre só o 1º turno. Limite: só o cargo de Presidente foi comparado, e só os arquivos com captura no Wayback.

<a id="a27"></a>

## A27. As 427 seções novas com comparecimento de 95% ou mais

**Classe de falha coberta:** seções sem eleitores reais. **Rastro esperado:** local sem estrutura, perfil atípico, histórico do local. **Previsão sem manipulação:** explicadas pelo tipo de local e pelo porte (já em [H5](resultados-fase1.md)). **Definição:** das 639 seções do 2º turno com comparecimento ≥ 95%, 427 não existiam em 2022.

| grupo | secoes | aptos_mediana | pct_local_ja_existia_em_2022 | secoes_no_local_mediana | turnout_t1_medio | turnout_t2_medio | comparecimento | margem_liquida_lula_menos_oponente | pct_lula_validos |
|---|---|---|---|---|---|---|---|---|---|
| novas com comparecimento >= 95% (as 427) | 427 | 139 | 49,9% | 2 | 94,9% | 96,5% | 68.351 | 22.836 | 67,1% |
| novas com comparecimento < 95% | 37.180 | 295 | 80,9% | 7 | 79,6% | 80,1% | 8.288.463 | 668.229 | 54,2% |
| antigas com comparecimento >= 95% | 212 | 216 | 99,5% | 1 | 93,4% | 96,0% | 42.419 | 14.901 | 68,1% |
| todas as secoes apuradas | 497.897 | 327 | 96,1% | 10 | 79,3% | 81,0% | 127.854.631 | 4.401.534 | 51,8% |

Tipo de local, pelo nome e endereço (% das seções de cada grupo):

| tipo_de_local_pelo_nome_e_endereco | pct_427 | pct_novas_abaixo_95 | pct_todas |
|---|---|---|---|
| escola | 36.5 | 51.5 | 50.1 |
| outro | 33.7 | 39.5 | 43.5 |
| rural_ou_comunidade | 23.7 | 8.2 | 6.2 |
| indigena | 5.9 | 0.6 | 0.2 |
| prisional | 0.2 | 0.2 | 0.0 |
| saude_ou_asilo | 0.0 | 0.1 | 0.0 |

**Leitura.** As 427 seções são pequenas (mediana de 139 aptos contra 327 no país), ficam em locais com poucas seções, e o comparecimento de 95% já aparece no 1º turno (média de 95%). Locais rurais, de comunidade e indígenas estão sobre-representados (23,7% e 5,9% contra 6,2% e 0,2% no país). Metade delas está em locais que já existiam em 2022. Lula tem 67,1% dos votos válidos nelas.

**Teto.** Contribuição líquida das 427 seções à margem: 22.836 votos de margem. **Teto de pior caso, não estimativa:** 44.735 votos de margem (1,0% da margem), se todos os votos de Lula nessas seções fossem inválidos. **Situação:** TESTADO-INCONCLUSIVO. **NÃO EXECUTADO:** origem das transferências de eleitores para essas seções (exige o cadastro nominal) e histórico detalhado dos locais. **O que fecharia:** a lista de transferências por seção, pela Justiça Eleitoral. Tabelas em `results/fase3/A27_*.csv`.

<a id="a28"></a>

## A28. Pedidos de acesso à informação (LAI)

Seis pedidos prontos, em `lai/`, com texto neutro, sem dados pessoais e sem acusação, cada um com **órgão e canal** definidos. **Nenhum foi protocolado**; o registro de protocolos, prazos (20 dias, prorrogáveis por 10), respostas e negativas fica em `lai/registro.csv`. Quem recebe cada pedido e por quê está em `lai/canais.csv`; os 27 TREs estão em `lai/canais_tres.csv`.

| pedido | assunto | órgão | canal |
|---|---|---|---|
| `01_urnas_substituidas.md` | Urnas substituídas em 2026 | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `02_codigo_de_carga.md` | Código de carga por urna | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `03_teste_de_integridade.md` | Testes de integridade e de autenticidade de 2026 | TSE; TRE de cada UF | Formulário Eletrônico da Ouvidoria do TSE e e-SIC de cada TRE |
| `04_logs_de_totalizacao.md` | Registros de recepção e totalização de 04/10 e 25/10/2026 | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `05_fiscais_credenciados.md` | Credenciamento de fiscais por seção (dados agregados) | TRE de cada UF; TSE | Formulário Eletrônico da Ouvidoria do TSE e e-SIC de cada TRE |
| `06_assinatura_e_chaves.md` | Verificação independente da assinatura digital dos arquivos de urna | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |

**Estado da verificação dos canais.** O TSE e os TREs bloqueiam acesso automatizado (403). O canal do TSE (Formulário Eletrônico da Ouvidoria, Resolução TSE 23.435/2015, alterada pela 23.583/2018) foi conferido em resultado de busca, não abrindo o formulário; para os TREs há página de SIC vista em resultado de busca para 6 UFs (SP, BA, AM, GO, RJ, AP) e as outras 21 estão como **a confirmar no protocolo**. A identificação de quem pede é exigida (Resolução CNJ 215/2015, art. 11, § 2º, segundo o TRE-SP); o projeto não tem autor nominal, então quem protocola assina o pedido. Confirme o canal, os campos e o prazo no sistema na hora de protocolar.


<a id="a31"></a>

## A31. Municípios extremos na transferência do 1º para o 2º turno (alegação Silva Jardim/RJ)

**Alegação.** Em Silva Jardim/RJ, no 2º turno de 2026 contra o 1º, "Flávio +1, Lula +964, -104 eleitores" seria impossível sem manipulação. **Pergunta.** Isso reproduz nos dados? E, comparado com todos os municípios em quatro eleições, é fora do comum? **Pré-registro:** [Adendo 10, 10a e 10b](preregistro.md); o 10b (análise suplementar) foi escrito depois de ver o resultado do modelo principal e está marcado como pós-hoc.

**1. A alegação reproduz em parte.** Dados do BWeb de Silva Jardim (61 seções). O ganho do oponente (**+1**) e a variação do comparecimento (**-104**: é o comparecimento do 2º turno menos o do 1º; os aptos mudam +3, não -104) reproduzem. O ganho de Lula nos dados é **+984**, não +964: diferença de 20 votos que não consegui explicar (pode ser erro de digitação na alegação ou outra fonte). Os votos de terceiros do 1º turno (897) e os brancos e nulos (630 no 1º turno, 438 no 2º) fecham a conta: o **pool** (ganho de Lula mais ganho do oponente) é 985, igual a terceiros mais brancos e nulos do 1º turno, mais a variação do comparecimento, menos os brancos e nulos do 2º.

| grandeza | T1 | T2 | T2 menos T1 |
|---|---|---|---|
| aptos | 18.674 | 18.677 | 3 |
| comparecimento | 14.909 | 14.805 | -104 |
| Lula (13) | 4.450 | 5.434 | 984 |
| Flavio Bolsonaro (22) | 8.932 | 8.933 | 1 |
| terceiros (soma) | 897 | 0 | -897 |
| brancos e nulos | 630 | 438 | -192 |

_Terceiros do 1º turno no município (votos):_ Renan Santos (14) 209; Hertz Dias (16) 5; Edmilson Costa (21) 2; Clariana Barão (27) 8; Zema (30) 20; Wilson Grassi (35) 3; Caiado (55) 290; Cury (70) 353; Samara Martins (80) 7.


**2. Distribuição da fração do pool que vai ao PT** (f = ganho do PT / (ganho do PT + ganho do oponente), municípios com pool de pelo menos 20 votos; f sai de [0, 1] quando um dos dois perde votos entre os turnos, o que é comum).

| ano | municípios | f nacional | mediana | decil 1 | decil 9 | % fora de [0, 1] | Silva Jardim: f | percentil | municípios com f mais distante da mediana |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | 5.357 | 0,737 | 0,734 | 0,540 | 1,066 | 13,7% | 0,999 | 86 | 948 |
| 2022 | 5.255 | 0,302 | 0,243 | -0,070 | 0,545 | 12,9% | 0,370 | 73 | 2.788 |
| 2018 | 5.491 | 0,645 | 0,596 | 0,397 | 0,872 | 2,7% | 0,716 | 69 | 3.030 |
| 2014 | 5.505 | 0,411 | 0,369 | 0,011 | 0,630 | 10,7% | 0,456 | 66 | 3.755 |

Em 2026 há 5.571 municípios, um a mais que nos outros anos (5.570): o código TSE 73709, de MT, só aparece em 2026 (não existe nos dados de 2022; não conferi o nome). Ficam fora da distribuição os municípios com pool abaixo de 20 votos (214 em 2026) e, pelo Adendo 10a, os municípios com seção apurada em só um dos turnos (2018: 6; 2014: 1; 2022 e 2026: nenhum; lista em `results/fase3/A31_excluidos.csv`).

**O que a tabela mostra.** Silva Jardim está no percentil 86 em 2026 e 948 municípios têm f mais distante da mediana que o dele. Mais importante: **o padrão "o oponente quase não ganha entre os turnos" é comum em 2026 e raro nos outros anos.** Dos 5.357 municípios elegíveis, 748 (14,0%) tiveram oponente com +1 voto ou menos, e 149 deles com PT ganhando 900 votos ou mais; em 2022 foram 8 (0,15%), em 2018 90 (1,6%) e em 2014 64 (1,2%) (S2, descritiva, pós-hoc). A fração nacional do pool que foi ao PT foi 0,737 em 2026, 0,302 em 2022, 0,645 em 2018 e 0,411 em 2014. A eleição de 2026 tem a forma de 2018 (PT captura a maior parte do pool), com a diferença de que em 2026 o oponente perdeu votos absolutos em mais municípios. Isto descreve a eleição, não explica por quê; a contabilidade nacional (queda de 1,82 milhão de brancos e nulos e de 2,96 milhões de abstenção, que somam mais que a captura de terceiros) está em [Fase 2, A3 e A11](resultados-fase2.md).

**3. Modelo nulo.** Por ano, regressão de f nos regressores do **1º turno** (fração do comparecimento para PT, oponente, brancos e nulos, abstenção e a composição dos terceiros: em 2026 o bloco que apoiou Flávio e Renan Santos; em 2022 e 2018 o maior e o segundo maior terceiro, sem inferir apoios; em 2014 só o total) com efeito fixo de UF, ponderada pela variância (binomial do pool mais uma heterogeneidade real entre municípios, calibrada pela escala robusta do resíduo). A cauda vem de uma distribuição t de Student com graus de liberdade estimados nos **outros três anos**; correção de Holm. **A variação do comparecimento entre os turnos não entra no perfil**, porque é desfecho do 2º turno.

| ano | municípios | heterogeneidade (tau²) | graus de liberdade (t) | valor crítico de z (módulo) para 5.570 comparações | municípios com Holm < 0,05 |
|---|---|---|---|---|---|
| 2026 | 5.357 | 0,0086 | 2,76 | 83 | 3 |
| 2022 | 5.255 | 0,0199 | 2,73 | 86 | 0 |
| 2018 | 5.491 | 0,0085 | 2,43 | 135 | 0 |
| 2014 | 5.505 | 0,0366 | 2,52 | 116 | 0 |

**Limite do teste, dito com todas as letras.** As caudas estimadas são muito pesadas (cerca de 2,4 a 2,8 graus de liberdade), porque f é instável quando o pool é pequeno e os fluxos brutos são grandes e de sinais opostos. O valor crítico fica em |z| de 83 a 135: **o modelo principal quase não tem poder para rejeitar municípios pequenos.** Por isso a conclusão sobre Silva Jardim não se apoia no corte de Holm, e sim em z: o dele é 1,13, comum sob qualquer referência.

**Silva Jardim, resultado pré-registrado: DENTRO DA CAUDA ESPERADA.** f = 0,999; o modelo, com o perfil do 1º turno do município, prevê 0,894; o resíduo é 0,105 (z = 1,13); p bilateral 0,35; Holm 1,00 (também com 5.570 comparações: 1,00). **Ganho espalhado entre as seções:** as 3 seções com maior ganho de Lula têm 8,8% do ganho total (as 3 de maior pool têm 8,9% do pool); a regra de concentração do Adendo 10 classifica como **espalhado**. **Teto de pior caso, não estimativa:** 207 votos de margem (0,005% da margem), se tudo o que o modelo não explica em Silva Jardim fosse manipulação (fator 2); além da cauda esperada: 0. A previsão sem manipulação do Adendo 10 (dentro da cauda, ganho espalhado, explicado pelo perfil do 1º turno) **se cumpre**.

_Leitura de f_hat: no 1º turno, Flávio teve 60% do comparecimento de Silva Jardim e o bloco que o apoiou no 2º turno (Zema, Caiado, Cury, Clariana) teve 4,5%. O modelo não prevê um f baixo para esse perfil: estima 0,89, porque em 2026 f é alto na maioria dos municípios (mediana 0,73). É uma leitura da distribuição, não uma explicação do comportamento dos eleitores._

**4. Modelo de moedas independentes: demonstração de que é inadequado.** Cada eleitor do pool vai ao PT com probabilidade p0, independentemente. Em três variantes de p0 (0,5; razão PT/(PT+oponente) do município no 1º turno; razão nacional):

| ano | pool nacional | PT observado | PT esperado (p0 = 0,5) | z das moedas | rejeita o resultado nacional? | municípios rejeitados (Holm 5%, p0 = 0,5) |
|---|---|---|---|---|---|---|
| 2026 | 14.095.433 | 10.339.213 | 7.047.716 | 1.753 | sim | 85% |
| 2022 | 10.246.841 | 3.144.361 | 5.123.420 | -1.236 | sim | 82% |
| 2018 | 23.759.956 | 15.334.145 | 11.879.978 | 1.417 | sim | 70% |
| 2014 | 27.340.477 | 11.251.847 | 13.670.238 | -925 | sim | 78% |

**Resultado.** O modelo de moedas rejeita o resultado nacional de **todas** as eleições, 2022 inclusa, em todas as variantes (|z| de 925 a 3.237), e rejeita de 70% a 93% dos municípios em todos os anos e variantes (pool positivo; municípios em que um dos candidatos perdeu votos, 14% em 2026, nem cabem no modelo). Um critério que declara "impossível" o resultado de uma eleição que ninguém contesta como impossível não distingue o normal do anormal. Isto mostra que o critério é inadequado; **não** valida nem invalida o resultado de nenhuma eleição. Pelo modelo de moedas, a chance de o oponente ter +1 voto ou menos em Silva Jardim seria entre 10^-294 e 10^-468, conforme a variante. Esse é o tipo de probabilidade que o modelo calcula para a maioria dos municípios (de 70% a 93% são rejeitados), de modo que ela não separa Silva Jardim dos demais.

**5. Os 20 municípios mais extremos de 2026** (maior |z| do modelo principal, em qualquer direção).

| # | município | UF | pool | dL | dF | f | f_hat | z | Holm | veredito do modelo | ganho | terceiro dominante no 1º turno |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ITACOATIARA | AM | 55 | 1.114 | -1.059 | 20,25 | 2,46 | 188 | 0,005 | FORA DA CAUDA, SEM PRECEDENTE | espalhado | Cury |
| 2 | SANTO ANTÔNIO DE LISBOA | PI | 48 | -350 | 398 | -7,29 | 1,00 | -87 | 0,041 | FORA DA CAUDA DO MODELO, COM PRECEDENTE | não se aplica (soma de dL ou do pool <= 0) | Renan Santos |
| 3 | RAFAEL GODEIRO | RN | 34 | 314 | -280 | 9,24 | 1,16 | 84 | 0,045 | FORA DA CAUDA DO MODELO, COM PRECEDENTE | espalhado | Renan Santos |
| 4 | ITAMARATI | AM | 27 | 210 | -183 | 7,78 | 2,47 | 55 | 0,148 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 5 | RUY BARBOSA | RN | 30 | 183 | -153 | 6,10 | 1,11 | 52 | 0,173 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 6 | ORIXIMINÁ | PA | 270 | 1.575 | -1.305 | 5,83 | 1,19 | 50 | 0,193 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 7 | BELO MONTE | AL | 136 | -304 | 440 | -2,24 | 1,15 | -36 | 0,471 | DENTRO DA CAUDA ESPERADA | não se aplica (soma de dL ou do pool <= 0) | Cury |
| 8 | ACORIZAL | MT | 23 | 119 | -96 | 5,17 | 0,82 | 36 | 0,490 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 9 | PEDRO AVELINO | RN | 46 | 202 | -156 | 4,39 | 1,20 | 34 | 0,576 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 10 | LAGOA DA CONFUSÃO | TO | 57 | 257 | -200 | 4,51 | 1,45 | 32 | 0,638 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 11 | AFONSO BEZERRA | RN | 83 | 344 | -261 | 4,14 | 1,17 | 32 | 0,682 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 12 | MANGARATIBA | RJ | 367 | 1.397 | -1.030 | 3,81 | 0,93 | 31 | 0,739 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 13 | NINA RODRIGUES | MA | 74 | 294 | -220 | 3,97 | 1,34 | 28 | 0,952 | DENTRO DA CAUDA ESPERADA | espalhado | Caiado |
| 14 | PORTEL | PA | 176 | 637 | -461 | 3,62 | 1,24 | 26 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 15 | AXIXÁ DO TOCANTINS | TO | 50 | 195 | -145 | 3,90 | 1,51 | 25 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 16 | CACHOEIRA DO PIRIÁ | PA | 62 | 223 | -161 | 3,60 | 1,24 | 25 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 17 | TENENTE ANANIAS | RN | 70 | 243 | -173 | 3,47 | 1,19 | 24 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |
| 18 | SANTA ROSA DO TOCANTINS | TO | 30 | 115 | -85 | 3,83 | 1,52 | 24 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Caiado |
| 19 | NOVA IORQUE | MA | 27 | 97 | -70 | 3,59 | 1,36 | 23 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Caiado |
| 20 | AXIXÁ | MA | 54 | 185 | -131 | 3,43 | 1,31 | 22 | 1,000 | DENTRO DA CAUDA ESPERADA | espalhado | Cury |

**Leitura.** (i) **Três dos 20 saem da cauda do modelo principal** (Holm < 0,05): Itacoatiara/AM, Santo Antônio de Lisboa/PI, Rafael Godeiro/RN. Itacoatiara/AM é o único sem precedente nos outros anos; os outros dois têm 1 município comparável nos outros três anos. (ii) **Todos os 20 têm pool pequeno (até 367 votos) e fluxos brutos de 5,5 a 39,5 vezes o pool**: um ganho grande de um candidato e uma perda quase igual do outro, e f vira uma razão de números pequenos. Em Itacoatiara, por exemplo, Lula +1.114, Flávio -1.059 e comparecimento -2.783, com pool de 55; f = 20,3 é artefato da divisão. Na estatística suplementar por apto (item 7), Itacoatiara fica comum. (iii) **Ganho espalhado entre seções** em 18 dos 20; nos outros 0 a soma de dL ou do pool é negativa e a regra não se aplica. Nenhum município tem ganho concentrado em poucas seções. (iv) **Terceiro dominante do 1º turno:** Cury em 15, Caiado em 3, Renan Santos em 2. Apoio declarado no 2º turno: Cury e Caiado apoiaram Flávio; Renan Santos liberou os eleitores ([fontes e conferência nome a nome em A11](resultados-fase2.md)). **O que estes 20 têm em comum:** o comparecimento caiu entre os turnos em todos (de -59 a -2.783 votos) e, em 18 deles, o PT ganhou e o oponente perdeu um número parecido de votos; o pool pequeno é a diferença entre dois fluxos grandes. O que explica isso (abstenção seletiva, troca de voto ou outra coisa) **não está nos dados agregados**; é o que boletins impressos e listas de habilitação por seção poderiam esclarecer. (v) **Comparação com 2022:** 6 dos 20 também estavam entre os 5% mais extremos de 2022 (|z| acima do percentil 95), 4 deles no sentido oposto ao de 2026; 10 não eram elegíveis em 2022 (pool menor que 20). Municípios com fluxo bruto grande e pool pequeno aparecem como extremos em eleições diferentes; isto é volatilidade desses municípios, não característica de 2026.

**Teto de pior caso, não estimativa (fator 2), 20 mais extremos:** 1.151 votos de margem além da cauda esperada (0,026% da margem); 13.327 votos de margem (0,30% da margem) se **tudo** o que o modelo não explica nesses 20 municípios fosse manipulação, sem descontar a variação normal. Nenhum cenário com esses municípios aproxima a margem de 4.430.191 votos.

**6. Conferência com boletins impressos.** `results/fase3/A31_silva_jardim_secoes.csv` lista as 61 seções de Silva Jardim com aptos, comparecimento, Lula, Flávio, cada terceiro, brancos e nulos no 1º e no 2º turno, mais colunas vazias para o valor impresso, no formato aceito por `scripts/04_cruza_bu_impresso.py`. Para conferir com BUs impressos, peça aos diretórios partidários locais e aos fiscais pela [página de coleta](boletins-impressos.md). **NÃO EXECUTADO:** o projeto não tem nenhum BU impresso de Silva Jardim.

**7. Análise suplementar (pós-hoc, exploratória, Adendo 10b; não substitui a linha principal).** Como f é instável com pool pequeno, repetida com estatísticas bem condicionadas: o ganho de cada candidato por apto do 1º turno, com os mesmos regressores e efeito fixo de UF, resíduo padronizado dentro de decis de tamanho. Silva Jardim em 2026: z do PT = 0,01 e z do oponente = -2,13; Holm 1,00 e 1,00: **comum**, nos quatro anos (z do oponente de -2,17 a -0,29). Cauda mais leve (cerca de 6 a 8 graus de liberdade; valor crítico de |z| de 10 a 13). Em 2026, 1 município sai da cauda por essa medida: Marechal Thaumaturgo/AC (z do oponente -10,4: o oponente perdeu 1.352 votos); teto de pior caso além da cauda: 136 votos de margem (0,003% da margem). Itacoatiara/AM, o primeiro do modelo principal, tem z de -1,97 e -1,60 nesta medida: comum.

**Situação.** Silva Jardim: TESTADO, DENTRO DA CAUDA ESPERADA (nos dois métodos). Três municípios pequenos saem da cauda do modelo principal por artefato da razão com pool pequeno (fluxos brutos de 15 a 40 vezes o pool); na medida suplementar um outro município (Marechal Thaumaturgo/AC) sai da cauda, com teto abaixo de 0,01% da margem: **TESTADO-INCONCLUSIVO** para esses, porque a explicação (municípios com forte queda de comparecimento entre os turnos) não pode ser conferida sem os boletins impressos e as listas de habilitação. **O que fecharia:** BUs impressos de Silva Jardim, Itacoatiara, Santo Antônio de Lisboa e Rafael Godeiro; a variação de comparecimento por seção entre os turnos nesses municípios. **O que o teste não faz:** não identifica em quem cada eleitor votou, não prova nem descarta manipulação em nenhum município; vale para a forma da distribuição entre municípios. Tabelas em `results/fase3/A31_*.csv`; código em `scripts/35_a31_transferencia_municipal.py`.
