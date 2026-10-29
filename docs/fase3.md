# Fase 3: hipóteses adversariais (A20 a A33)

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
| [A32](#a32) Liberação manual como canal de abuso local | habilitações manuais em rajadas, no fim do dia ou em excesso para a idade | nenhuma rajada pela definição registrada (que não consegue vê-las); manuais não se concentram no fim do dia; seções com mais de 30% de manual: 3.995 em 2022 e 348 em 2026; sem associação com comparecimento ou voto | registrado 1.852.233 (inflado por deslocamento negativo, Adendo 11c); além do ruído do modelo de 2022: 55.862 votos de margem (teto de pior caso, não estimativa; 1,26% da margem) | TESTADO-INCONCLUSIVO (logs parciais) |
| [A31b](#a31b) Municípios com oponente +1 voto ou menos | troca de voto ou abstenção seletiva concentrada | 748 municípios (14,0%), compatíveis com o deslocamento nacional; perfil regional e de eleitorado PT forte; a maioria com queda de comparecimento | teto A de 234.746 votos de margem (teto de pior caso, não estimativa), e **zero** além do que o deslocamento nacional simulado já dá | TESTADO-INCONCLUSIVO |
| [A32b](#a32b) Rajadas de liberação manual (limiar absoluto) | habilitações manuais em sequência | razão observado/esperado de 1,0 a 1,2 nos dois anos; rajadas menos frequentes em 2026 que em 2022; coeficientes de 2026 indistinguíveis de zero | teto sem poder (extrapolado), **não plotado** | TESTADO-INCONCLUSIVO |
| [A33](#a33) Liberação manual por escola | manual concentrada em locais de votação, com ganho de Lula ou comparecimento | sem associação positiva entre taxa manual da escola e ganho de Lula T1 → T2 (coeficiente de 2026 negativo, -0,017); placebos 2022 e 2018 sem excesso; sincronia nos logs igual à de 2022 | 29.654 votos de margem pelas 661 escolas extremas (teto de pior caso, não estimativa; 0,67% da margem); além do ruído do modelo: 8.125 | TESTADO-INCONCLUSIVO |
| [A28](#a28) Pedidos LAI | dados que só o poder público tem | 7 pedidos prontos em `lai/` (o 07, da ata e da folha de votação, é do A32), com órgão e canal de cada um, e um modelo de requerimento para partidos; **nenhum protocolado** | n/a | NÃO EXECUTADO |

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

Sete pedidos prontos, em `lai/` (o 07 é do A32; o 08 é um modelo de requerimento para partidos, não um pedido LAI), com texto neutro, sem dados pessoais e sem acusação, cada um com **órgão e canal** definidos. **Nenhum foi protocolado**; o registro de protocolos, prazos (20 dias, prorrogáveis por 10), respostas e negativas fica em `lai/registro.csv`. Quem recebe cada pedido e por quê está em `lai/canais.csv`; os 27 TREs estão em `lai/canais_tres.csv`.

| pedido | assunto | órgão | canal |
|---|---|---|---|
| `01_urnas_substituidas.md` | Urnas substituídas em 2026 | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `02_codigo_de_carga.md` | Código de carga por urna | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `03_teste_de_integridade.md` | Testes de integridade e de autenticidade de 2026 | TSE; TRE de cada UF | Formulário Eletrônico da Ouvidoria do TSE e e-SIC de cada TRE |
| `04_logs_de_totalizacao.md` | Registros de recepção e totalização de 04/10 e 25/10/2026 | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `05_fiscais_credenciados.md` | Credenciamento de fiscais por seção (dados agregados) | TRE de cada UF; TSE | Formulário Eletrônico da Ouvidoria do TSE e e-SIC de cada TRE |
| `06_assinatura_e_chaves.md` | Verificação independente da assinatura digital dos arquivos de urna | TSE | Formulário Eletrônico da Ouvidoria do TSE (SIC) |
| `07_ata_e_folha_de_votacao.md` | Ata da mesa receptora e folha de votação de 83 seções (A32 e A33) | TRE de cada UF | e-SIC de cada TRE |

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

Em 2026 há 5.571 municípios, um a mais que nos outros anos (5.570): o código TSE 73709, de MT, só aparece em 2026 (não existe nos dados de 2022). **Confirmado:** é **Boa Esperança do Norte/MT**, criado pela Lei estadual 7.264, de 29/03/2000, desmembrado de Sorriso e Nova Ubiratã (13 seções: 5 vieram de Sorriso, 4 de Nova Ubiratã e 4 são novas), com criação validada pelo STF em 06/10/2023 (ADPF 819, 8 votos a 3) e instalação em 01/01/2025, com primeiro prefeito eleito em 2024. O nome vem da tabela do TSE usada no A20; a lei e a instalação, de fontes secundárias (Assembleia Legislativa de MT e imprensa), **sem conferir a data de instalação em ato primário**. Ficam fora da distribuição os municípios com pool abaixo de 20 votos (214 em 2026) e, pelo Adendo 10a, os municípios com seção apurada em só um dos turnos (2018: 6; 2014: 1; 2022 e 2026: nenhum; lista em `results/fase3/A31_excluidos.csv`).

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

<a id="a12b"></a>

## A12b. A alegação "106 urnas com 100% para Lula e 0% de brancos, nulos e Flávio"

**Pré-registro:** [Adendo 12](preregistro.md), escrito antes de calcular as probabilidades. **Alegação.** A imagem afirma que 106 urnas deram 100% a Lula e 0% de brancos, nulos e Flávio.

**1. Contagem.** Das **106** seções com zero voto para Flávio em 2026/T2 (a contagem de A12; nenhuma tem comparecimento zero), **29** (27%) têm também zero brancos e zero nulos. As outras 77 têm brancos ou nulos. No conjunto das 106: 24 brancos e 338 nulos, 2,4% do comparecimento de 15.222 votantes. **"0% de brancos e nulos" não vale para o conjunto das 106**, só para 29. São seções pequenas (comparecimento mediano 128; aptos medianos 161); as 29 com tripla zero são ainda menores (mediana 56 votantes, contra 139).

**2. Onde estão.** Por tipo de local (classificação de A27 pelo nome do local) e por UF:

| tipo de local | seções | com zero brancos e nulos | comparecimento mediano |
|---|---|---|---|
| escola_outro | 55 | 11 | 103,0 |
| indigena | 41 | 15 | 145,0 |
| prisional | 2 | 1 | 21,5 |
| quilombola | 1 | 1 | 54,0 |
| rural_comunidade | 7 | 1 | 68,0 |

| UF | seções | com zero brancos e nulos | votos de Lula |
|---|---|---|---|
| AC | 3 | 0 | 386 |
| AM | 30 | 1 | 6.477 |
| BA | 4 | 1 | 215 |
| CE | 2 | 1 | 86 |
| ES | 1 | 1 | 41 |
| MA | 20 | 4 | 2.068 |
| MG | 2 | 0 | 116 |
| MS | 1 | 1 | 56 |
| MT | 5 | 3 | 813 |
| PA | 16 | 10 | 1.733 |
| PB | 1 | 1 | 10 |
| PE | 1 | 0 | 227 |
| PI | 1 | 1 | 16 |
| PR | 1 | 0 | 314 |
| RO | 1 | 0 | 104 |
| RR | 8 | 4 | 1.207 |
| RS | 2 | 1 | 104 |
| TO | 7 | 0 | 887 |

As 106 estão em 18 UFs, com concentração em AM (30), MA (20) e PA (16); 41 são em locais indígenas. Para cada uma: UF, município, tipo de local, aptos, comparecimento, votos de Lula, brancos, nulos, resultado no 1º turno de 2026 e na mesma seção em 2022: `results/fase3/A12b_106_secoes.csv`.

**3. Esperado.** Para cada seção, a probabilidade de zero brancos e zero nulos é (1 - r)^n, com n o comparecimento da própria seção e r a taxa de brancos e nulos das **outras seções do mesmo local** (do município, se o local tem só uma seção ou poucos votantes). O número esperado é a soma; o p exato vem da distribuição Poisson-binomial. Série, com as seções de zero oponente de cada eleição (definição "todas as apuradas" de A12):

| ano | turno | seções com zero oponente | tripla zero observada | esperada (taxa do local) | p (observado ou mais) | esperada (taxa do município) | observado / esperado |
|---|---|---|---|---|---|---|---|
| 2014 | 1 | 709 | 23 | 19,9 | 0,219 | 19,7 | 1,15 |
| 2014 | 2 | 194 | 28 | 22,6 | 0,084 | 22,8 | 1,24 |
| 2018 | 1 | 674 | 61 | 27,2 | < 0,001 | 16,9 | 2,24 |
| 2018 | 2 | 328 | 42 | 19,2 | < 0,001 | 16,0 | 2,19 |
| 2022 | 1 | 161 | 39 | 23,2 | < 0,001 | 16,9 | 1,68 |
| 2022 | 2 | 143 | 29 | 20,8 | 0,018 | 18,9 | 1,39 |
| 2026 | 1 | 81 | 28 | 17,0 | < 0,001 | 10,1 | 1,65 |
| 2026 | 2 | 106 | 29 | 20,4 | 0,009 | 17,0 | 1,42 |

**Leitura.** A previsão do Adendo 12 (observado próximo do esperado) **não se cumpre ao pé da letra**: em 2026/T2 há 29 seções com tripla zero contra 20,4 esperadas (p = 0,009; com a taxa do município, p < 0,001). **Mas o excesso sobre o esperado existe em todas as eleições e tem razão parecida em 2022 (T2 1,39) e maior em 2018 (T2 2,19) do que em 2026 (1,42)**, inclusive nos 1º turnos. Uma explicação possível, **não testada aqui**: seções com zero voto para o oponente são locais pequenos e unânimes, onde brancos e nulos podem ser menos frequentes do que nas vizinhas; se for isso, é limitação do esperado, não característica de 2026. O que a série mostra é só que o excesso não é específico de 2026.

**4. Unânimes e a diferença entre as afirmações.**

| ano | turno | conjunto (seções com 30 votos válidos ou mais) | seções | com zero brancos e nulos | % com zero brancos e nulos | mediana de brancos e nulos (% do comparecimento) |
|---|---|---|---|---|---|---|
| 2026 | 2 | 100% dos válidos para o PT | 103 | 26 | 25,2 | 1,52 |
| 2026 | 2 | 100% dos válidos para o oponente | 4 | 1 | 25,0 | 1,87 |
| 2022 | 2 | 100% dos válidos para o PT | 130 | 23 | 17,7 | 1,88 |
| 2022 | 2 | 100% dos válidos para o oponente | 2 | 0 | 0,0 | 3,08 |

O relatório original dizia "100% dos votos válidos" (seções unânimes com 30 votos válidos ou mais, [página do relatório](relatorio-original.md)): 103 seções do PT em 2026/T2. **"100% dos válidos" admite brancos e nulos acima de zero; "0% de brancos e nulos" é uma afirmação mais forte.** E 106 (zero voto para Flávio, qualquer tamanho) não é o mesmo conjunto que 103 (unânimes com 30 válidos ou mais). Entre as 103, 26 têm zero brancos e nulos.

**5. Teto, em votos de margem (teto de pior caso, não estimativa).** Votos de Lula nas 106 seções: **14.860**. (i) Se todos fossem inválidos (como em A27, fator 1): **14.860 votos de margem (0,34% da margem)**. (ii) Se esses votos fossem trocados, pelo que as seções vizinhas dariam ao oponente (2.700 votos esperados; fator 2): **5.401 votos de margem (0,12% da margem)**. Nenhum cenário com essas seções se aproxima da margem de 4.430.191 votos.

**Situação.** TESTADO: a alegação "0% de brancos e nulos" não reproduz para o conjunto (só para parte); o excesso de tripla zero sobre o esperado é geral e não específico de 2026. **O que o teste não faz:** não mostra por que seções pequenas e unânimes têm menos brancos e nulos (sigilo do voto, perfil dos locais, ou outra coisa); só mostra que isso ocorre em todas as eleições. Código: `scripts/36_a12b_zero_brancos_nulos.py`; tabelas: `results/fase3/A12b_*.csv`.

<a id="a32"></a>

## A32. Liberação manual como canal de abuso local

**Pré-registro:** [Adendo 11, 11a, 11b, 11c e 11d](preregistro.md). O 11a e o 11b foram escritos antes de contar qualquer rajada; o **11c e o 11d foram escritos depois de ver resultados** (o do item 3 e o das rajadas registradas) e estão marcados como pós-hoc onde aparecem.

**Cobertura (declarada).** Logs de urna lidos: **53.242 seções-dia** (12.554 seções com log de 2022 e 14.067 de 2026, cada log com os dois dias), a amostra de seções de A4/A5/A21 mais **todas** as seções de Roraima; o log do 2º turno contém os eventos do 1º. **NÃO EXECUTADO:** os logs de todas as seções dos dois anos (cerca de 1 milhão de arquivos, em zips públicos de dezenas de GB por UF); ano de nascimento: **NÃO EXECUTÁVEL** (o log não registra data de nascimento e o projeto não extrai identificadores de eleitores ou mesários). Seção-dia só entra nas medidas se o log fecha com o comparecimento do BU (a até 5%) e tem 100 habilitações ou mais (51.829 de 53.242). Validação do extrator: a fração manual do log tem correlação de 0,994 com a taxa manual do BWeb em Roraima.

### 1. A21 completo: sequência das habilitações, rajadas e última hora

**Quanto tempo leva cada tipo de habilitação** (intervalo, em segundos, que **precede** cada habilitação; agregado nacional da amostra, sem identificar seção):

| ano | turno | tipo de habilitação | n | p1 | p5 | p25 | mediana | p75 | p95 |
|---|---|---|---|---|---|---|---|---|---|
| 2022 | 1º turno | manual | 222.269 | 93 | 104 | 128 | 153 | 192 | 326 |
| 2022 | 1º turno | biométrica | 2.612.759 | 51 | 59 | 74 | 91 | 119 | 223 |
| 2022 | 2º turno | manual | 220.651 | 67 | 77 | 97 | 121 | 169 | 390 |
| 2022 | 2º turno | biométrica | 2.695.045 | 31 | 36 | 48 | 65 | 108 | 328 |
| 2026 | 1º turno | manual | 226.947 | 97 | 108 | 131 | 156 | 197 | 329 |
| 2026 | 1º turno | biométrica | 3.220.613 | 54 | 62 | 78 | 95 | 125 | 247 |
| 2026 | 2º turno | manual | 242.710 | 66 | 76 | 97 | 123 | 179 | 410 |
| 2026 | 2º turno | biométrica | 3.325.892 | 29 | 34 | 46 | 63 | 116 | 358 |

**Rajadas pela definição registrada (Adendo 11).** k ou mais liberações manuais consecutivas, com todos os intervalos abaixo do percentil 5 dos intervalos da própria seção-dia (k = 3 e 5).

| ano | turno | seções-dia | % manual | rajadas k=3 | % seções com rajada k=3 | % esperado k=3 (permutação) | rajadas k=5 | % esperado k=5 (permutação) |
|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | 12.022 | 6,3 | 0 | 0,0 | 0,11 | 0 | 0,00 |
| 2022 | 2 | 12.375 | 6,1 | 0 | 0,0 | 0,09 | 0 | 0,00 |
| 2026 | 1 | 13.644 | 6,2 | 0 | 0,0 | 0,05 | 0 | 0,00 |
| 2026 | 2 | 13.788 | 6,4 | 0 | 0,0 | 0,06 | 0 | 0,00 |

**Resultado: nenhuma rajada, em nenhum ano, dia ou k.** **Mas isso não é um achado de ausência de abuso: o desenho registrado não consegue ver rajadas por construção** (Adendo 11d). Uma liberação manual leva uma mediana de 121 a 156 s (o menor intervalo que precede uma manual, no percentil 1, é de 66 s), contra 63 a 95 s da biométrica; o percentil 5 dos intervalos de todas as habilitações da seção fica abaixo do tempo mínimo de uma manual. A permutação, que ignora esse limite físico, esperaria de 7 a 13 seções-dia com rajada k = 3 por ano e dia contra 0 observadas; essa diferença mede o limite físico, não o acaso nem o abuso. Por isso os modelos de associação das rajadas com comparecimento e voto **não são estimáveis** (sem variação): **NÃO EXECUTÁVEL**, linha oficial. A previsão "sem abuso" (mesma frequência entre anos, sem associação) não pode ser contrariada nem confirmada por essa medida.

**Fração das liberações manuais na última hora** (60 minutos antes do fechamento nominal), contra a fração de **todas** as habilitações na última hora:

| ano | turno | manuais na última hora | todas as habilitações na última hora | diferença (manual menos todas) | erro padrão |
|---|---|---|---|---|---|
| 2022 | 1 | 10,3% | 12,8% | -2,5 p.p. | 0,1 p.p. |
| 2022 | 2 | 4,8% | 5,7% | -0,9 p.p. | 0,1 p.p. |
| 2026 | 1 | 9,7% | 11,7% | -2,0 p.p. | 0,1 p.p. |
| 2026 | 2 | 4,4% | 5,2% | -0,9 p.p. | 0,1 p.p. |

As liberações manuais **não se concentram no fim do dia**: a fração delas na última hora é menor que a das habilitações em geral, nos dois anos e nos dois turnos. Isto contraria a previsão "com abuso" (concentração no fim do dia).

**Medida suplementar pós-hoc (Adendo 11d): agrupamento de liberações manuais**, k ou mais manuais consecutivas na ordem de chegada, sem condição de tempo, contra o esperado exato por permutação dos rótulos (a probabilidade de pelo menos um agrupamento usa a aproximação de Poisson, declarada).

| ano | turno | % seções com agrupamento k=3 | % esperado k=3 | observado/esperado k=3 | % seções com agrupamento k=5 | % esperado k=5 | observado/esperado k=5 |
|---|---|---|---|---|---|---|---|
| 2022 | 1 | 15,13 | 12,22 | 1,20 | 1,42 | 0,79 | 1,66 |
| 2022 | 2 | 13,33 | 11,45 | 1,14 | 1,00 | 0,72 | 1,27 |
| 2026 | 1 | 10,00 | 8,23 | 1,19 | 0,25 | 0,14 | 1,35 |
| 2026 | 2 | 10,72 | 9,11 | 1,14 | 0,25 | 0,16 | 1,23 |

**Frequência de 2026 contra 2022, nas mesmas seções** (efeito fixo de seção, erro padrão agrupado por município; diferença em pontos de proporção de seções com agrupamento):

| turno | k | seções nos dois anos | 2026 menos 2022 (p.p.) | erro padrão | z | p |
|---|---|---|---|---|---|---|
| 1º turno | 3 | 11.762 | -5,19 | 3,71 | -1,40 | 0,163 |
| 1º turno | 5 | 11.762 | -1,16 | 0,38 | -3,01 | 0,003 |
| 2º turno | 3 | 12.240 | -2,60 | 3,61 | -0,72 | 0,472 |
| 2º turno | 5 | 12.240 | -0,76 | 0,29 | -2,65 | 0,008 |

Os agrupamentos são **menos** frequentes em 2026 do que em 2022 (diferença de z de -3,0 e -2,65 para k = 5, ainda significativa com Holm sobre as quatro linhas; não significativa para k = 3), e a razão observado/esperado é parecida nos dois anos (de 1,1 a 1,7): as manuais chegam um pouco mais juntas do que na ordem aleatória, nos dois anos. A previsão "com abuso" (mais em 2026 do que em 2022) **não se cumpre**.

**Associação do agrupamento com comparecimento e voto** (2º turno, efeito fixo de local, controle do 1º turno; placebo: 2022). **Principal (k = 5, amostra aleatória R mais Roraima): NÃO EXECUTÁVEL**, porque quase não há agrupamento de 5 nessa amostra (variação insuficiente). Sensibilidade, k = 3:

| amostra | desfecho | coeficiente 2026 | erro padrão 2026 | coeficiente 2022 (placebo) | erro padrão 2022 | seções |
|---|---|---|---|---|---|---|
| principal: R + Roraima completa | comparecimento | 0,0031 | 0,0040 | -0,0006 | 0,0036 | 1.467 |
| principal: R + Roraima completa | participação de Lula | 0,0002 | 0,0031 | -0,0010 | 0,0041 | 1.467 |
| sensibilidade: todos os estratos (seleção no desfecho) | comparecimento | 0,0025 | 0,0006 | 0,0027 | 0,0006 | 11.318 |
| sensibilidade: todos os estratos (seleção no desfecho) | participação de Lula | -0,0003 | 0,0006 | 0,0006 | 0,0007 | 11.318 |

Nenhum coeficiente se distingue de zero nem do placebo de 2022 (um coeficiente de 0,003 é 0,3 ponto percentual). Sem família principal, **não há teto em votos de margem nem veredito de Holm para o item 1**. **M3, descritiva** (variação 2022 → 2026 do comparecimento do 2º turno contra o agrupamento de 2026, efeito fixo de local):

| amostra | k | coeficiente | erro padrão | p | seções |
|---|---|---|---|---|---|
| principal: R + Roraima completa | 3 | 0,0004 | 0,0054 | 0,946 | 1.144 |
| todos os estratos (seleção no desfecho) | 3 | -0,0012 | 0,0010 | 0,234 | 10.217 |
| todos os estratos (seleção no desfecho) | 5 | -0,0116 | 0,0057 | 0,041 | 10.217 |

A única linha com p < 0,05 (k = 5, todos os estratos, seleção no desfecho, poucos agrupamentos) tem coeficiente **negativo** (-1,2 p.p. de comparecimento), o oposto do que a hipótese de abuso preveria, e sem correção para comparações múltiplas.

### 2. Seções com liberação manual extrema (BWeb, todas as seções)

| ano | turno | corte | seções válidas | extremas | % das seções | votantes nelas | comparecimento mediano | idade média do eleitorado (mediana), extremas | idem, todas as seções | UFs |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | > 30% | 470.914 | 6.056 | 1,286 | 1.268.638 | 217 | 47,5 | 44,4 | 26 |
| 2022 | 1 | > 50% | 470.914 | 595 | 0,126 | 134.653 | 239 | 45,1 | 44,4 | 24 |
| 2022 | 2 | > 30% | 470.896 | 3.995 | 0,848 | 844.612 | 216 | 47,6 | 44,4 | 25 |
| 2022 | 2 | > 50% | 470.896 | 317 | 0,067 | 71.512 | 241 | 46,1 | 44,4 | 24 |
| 2026 | 1 | > 30% | 497.769 | 391 | 0,079 | 79.917 | 223 | 48,3 | 46,0 | 21 |
| 2026 | 1 | > 50% | 497.769 | 138 | 0,028 | 32.196 | 238 | 45,5 | 46,0 | 17 |
| 2026 | 2 | > 30% | 497.750 | 348 | 0,070 | 73.003 | 223 | 49,2 | 46,0 | 20 |
| 2026 | 2 | > 50% | 497.750 | 97 | 0,019 | 23.050 | 234 | 46,3 | 46,0 | 16 |

**Contagem e leitura.** Liberação manual acima de 30% dos votantes: **3.995 seções no 2º turno de 2022 e 348 no de 2026**; acima de 50%, 317 contra 97. **O fenômeno é muito menor em 2026 do que em 2022**, e o eleitorado dessas seções é cerca de 3 anos mais velho que o das demais (idade média, mediana: 47,6 contra 44,4 em 2022; 49,2 contra 46,0 em 2026). Por UF (corte de 30%, 2º turno), as maiores contagens:

| UF | 2022 T1 | 2022 T2 | 2026 T1 | 2026 T2 |
|---|---|---|---|---|
| BA | 1348 | 922 | 75 | 80 |
| RS | 959 | 499 | 58 | 61 |
| CE | 427 | 344 | 37 | 25 |
| PI | 498 | 302 | 18 | 23 |
| SP | 270 | 148 | 32 | 23 |
| MG | 356 | 264 | 22 | 20 |
| PA | 98 | 40 | 18 | 17 |
| PR | 188 | 115 | 35 | 16 |

Por tipo de local (corte de 30%, 2º turno; classificação de A27 pelo nome): escola_outro 3778 em 2022 e 331 em 2026; indigena 5 em 2022 e 0 em 2026; rural_comunidade 212 em 2022 e 17 em 2026. Nenhuma seção em locais indígenas, prisionais, quilombolas, hospitalares ou militares tem liberação manual extrema em 2026.

**Comparecimento e voto contra as demais seções do mesmo local (2º turno, extremas > 30%).** Comparecimento: 0,01 p.p. (erro padrão por local 0,24) em 2026 contra -0,48 p.p. (0,09) em 2022. Participação de Lula (válidos): 0,38 p.p. (0,28) em 2026 contra 0,34 p.p. (0,08) em 2022; com o controle do 1º turno (variação T1 → T2), Lula 0,11 p.p. (0,13) em 2026 e 0,18 p.p. (0,04) em 2022. Diferenças de décimos de ponto percentual, **sem diferença entre os anos no voto**. A variação do comparecimento T1 → T2 dessas seções contra os vizinhos é +0,89 p.p. em 2026 (erro padrão 0,17) e +0,49 p.p. em 2022 (0,05): um excesso pequeno (menos de 1 ponto sobre um comparecimento de cerca de 80%) e sem contrapartida na participação de Lula.

### 3. Teto em votos de margem do excesso de liberação manual sobre o esperado pela idade

Modelo da taxa manual do 2º turno **ajustado em 2022** (mínimos quadrados ponderados por votantes; regressores: composição etária do eleitorado da seção, biometria cadastrada e efeito fixo de UF), aplicado a 2026. **O modelo de 2022 prevê mais liberação manual em 2026 do que a observada**: 11.615.994 votantes previstos contra 8.629.826 observados (8,63 milhões, o mesmo "8,6 milhões" que o relatório original cita); a taxa manual **caiu**, não subiu. Excesso por seção = max(0, observado - previsto) x votantes.

| ano | seções | manuais observadas | manuais previstas | (a) soma dos excessos positivos | (b) além de 1,645 desvio de 2022 | (c) após remover o deslocamento nacional | (c) e além de 1,645 desvio |
|---|---|---|---|---|---|---|---|
| 2022 (dentro da amostra, referencia) | 470.651 | 10.009.455 | 10.009.455 | 2.679.836 | 564.492 | 3.363.368 | 750.129 |
| 2026 | 497.474 | 8.629.826 | 11.615.994 | 709.152 | 55.862 | 1.852.233 | 123.866 |

**Teto registrado (o maior dos quatro números do Adendo 11, fator 1, teto de pior caso, não estimativa): 1.852.233 votos de margem (41,8% da margem).** **Leitura posterior ao resultado (Adendo 11c): esse número é inflado por construção.** A variante (c) remove o deslocamento nacional (mediana do resíduo: -2,7 p.p.), e como o deslocamento é para **baixo** em 2026, remover o deslocamento **soma** 2,7 p.p. a cada seção. As leituras que fazem sentido aqui: (a) 709.152 votos de margem (16,0% da margem), que inclui o ruído do modelo (a mesma soma dentro da amostra de 2022, em que o modelo foi ajustado, é 2.679.836, **3,8 vezes maior**); (b) o que passa de 1,645 desvio do resíduo de 2022: **55.862 votos de margem (1,26% da margem)**, em 5.818 seções, contra 564.492 em 2022. Nenhuma das leituras é estimativa: supõem todos os excessos a favor de um só lado.

As **50 seções com maior excesso** em 2026/2º turno (liberação manual observada de 64% a 99%, prevista de 6% a 15%; 26 na Bahia, 5 em SP, 5 em RJ e 5 em PR; locais de votação em escolas, uma em comunidade rural) somam 10.612 votantes de excesso (0,24% da margem). Lista, com o critério de cada uma: `lai/07_secoes.csv` (que também traz, depois delas, as 33 seções das 20 escolas extremas do A33, 83 no total). Não há explicação nos dados para esses valores; **tampouco há associação com o voto** (seções com mais de 50% de manual: Lula 0,05 p.p., erro padrão 0,21, contra os vizinhos do mesmo local, com controle do 1º turno).

### 4. Integridade dos logs

Na amostra lida, o hash do log **consta da lista assinada pela urna** (A4) em **12.554 de 12.554 seções de 2022 e 14.067 de 14.067 de 2026** (100%). Isto diz que o log é o que a urna listou; **a verificação da assinatura da lista (pendente, A18)** é o que fecha a hipótese de alteração do log depois da urna. Enquanto pendente, vale "o log é o que a urna listou", não "o log é autêntico".

### 5. Documentos em papel

Textos prontos, **nenhum protocolado**: pedido LAI aos TREs ([`lai/07_ata_e_folha_de_votacao.md`](https://github.com/baduba/eleicoes-dossie-2026/blob/main/lai/07_ata_e_folha_de_votacao.md)) para as 50 seções acima (cópia da ata da mesa receptora e da folha de votação **com dados pessoais tarjados**, ou, se não for possível, as contagens de assinaturas, de anotações de habilitação manual e de votantes da ata), e modelo de requerimento de partido ao cartório eleitoral (`lai/08_modelo_requerimento_partidos.md`, para revisão por advogado eleitoral; o prazo de guarda dos documentos de seção está **a confirmar**). **Teste fixado, NÃO EXECUTADO até haver documentos:** assinaturas da folha x votantes da ata x comparecimento do BU x habilitações do log, por seção, com `scripts/37_confere_ata.py`, que lista qualquer divergência (incluídas as banais, como erro de contagem).

**Situação.** TESTADO-INCONCLUSIVO (item 1 sem medida capaz de ver rajadas; item 3 com teto registrado de 1.852.233 votos de margem, inflado, e 55.862 além do ruído). **Resumo do que os dados mostram:** a liberação manual **caiu** de 2022 para 2026, as seções extremas são **muito menos** numerosas em 2026, as manuais **não** se concentram no fim do dia, **não** há mais agrupamentos em 2026 e **não** há associação com comparecimento ou voto. **O que fecharia:** logs de todas as seções (para a distribuição nacional), a verificação da assinatura dos logs, e a ata e a folha de votação das seções listadas. **O que o teste não faz:** não identifica eleitores nem mesários; a liberação manual tem usos legítimos (digital não reconhecida, eleitor sem biometria cadastrada, idoso); o excesso sobre o modelo de idade não é fraude, é só o que o modelo de 2022 não prevê. Código: `scripts/38` a `scripts/41` e `scripts/37_confere_ata.py`; tabelas: `results/fase3/A32_*.csv`.

<a id="a31b"></a>

## A31b. Os municípios em que o oponente ganhou +1 voto ou menos entre os turnos

**Pré-registro:** [Adendo 13](preregistro.md), escrito antes de rodar a simulação e o perfil. **Pergunta.** Em A31 vimos que 748 de 5.357 municípios de 2026 (14,0%) tiveram o ganho do oponente entre os turnos menor ou igual a +1 voto, contra 0,15% em 2022, 1,6% em 2018 e 1,2% em 2014. Isso é o que se esperaria do crescimento nacional do oponente em 2026 (6,8%, contra 14%, 17% e 46% nos anos de comparação)?

**1. Fração esperada sob o deslocamento nacional.** Para cada ano de comparação, o crescimento de cada município do oponente (ganho / voto do 1º turno) é deslocado, por UF, para a taxa de crescimento da mesma UF em 2026 e aplicado à base de 2026. Fração de municípios com ganho menor ou igual a +1:

| ano de comparação | municípios pareados | fração no próprio ano, sem deslocar | esperada (pareada) | esperada (reamostragem, média) | reamostragem 2,5% | reamostragem 97,5% |
|---|---|---|---|---|---|---|
| 2022 | 5.356 | 0,2% | 14,7% | 15,4% | 14,6% | 16,1% |
| 2018 | 5.350 | 1,6% | 13,2% | 13,9% | 13,1% | 14,6% |
| 2014 | 5.356 | 1,2% | 55,0% | 54,9% | 53,4% | 56,1% |

**Observado em 2026: 14,0%.** O deslocamento por UF com 2022 dá 14,7% (reamostragem 14,6% a 16,1%) e com 2018, 13,2% (13,1% a 14,6%). **Veredito pré-registrado: COMPATÍVEL COM O DESLOCAMENTO NACIONAL.** A fração de 14,0% é a que 2018 e 2022 produziriam se o oponente tivesse crescido em cada UF o que cresceu em 2026; o 55% obtido com 2014 mostra apenas que o crescimento de 46% daquele ano é distante demais para servir de comparação (a extrapolação é grande). **Limitação:** o deslocamento iguala o crescimento médio de cada UF; não garante que a forma da distribuição de 2018 e 2022 seja a de 2026. Isto mostra que **o número de 748 não é, por si, anomalia**; não diz por que o oponente cresceu pouco em 2026.

**2. Perfil dos 748** (descritivo, confundido por região e porte):

| região | municípios com dF <= 1 | demais | % do grupo | % dos demais | razão | % dos municípios da região com dF <= 1 |
|---|---|---|---|---|---|---|
| Centro-Oeste | 21 | 443 | 2,8 | 9,6 | 0,3 | 4,5 |
| Nordeste | 547 | 1191 | 73,1 | 25,8 | 2,8 | 31,5 |
| Norte | 157 | 141 | 21,0 | 3,1 | 6,9 | 52,7 |
| Sudeste | 19 | 1647 | 2,5 | 35,7 | 0,1 | 1,1 |
| Sul | 4 | 1187 | 0,5 | 25,8 | 0,0 | 0,3 |

| porte (aptos) | municípios com dF <= 1 | demais | % dos municípios do porte com dF <= 1 |
|---|---|---|---|
| 20 a 100 mil | 152 | 959 | 13,7 |
| 5 a 20 mil | 418 | 2249 | 15,7 |
| ate 5 mil | 175 | 1183 | 12,9 |
| mais de 100 mil | 3 | 218 | 1,4 |

UFs com 15 ou mais desses municípios (% dos municípios da UF): AM 23 (79%); TO 69 (77%); MA 146 (76%); AL 70 (71%); RN 77 (47%); PA 58 (47%); PI 95 (47%); PB 65 (29%); CE 48 (26%); SE 17 (23%); MT 17 (12%); PE 17 (9%). **94% dos 748 estão no Nordeste e no Norte; praticamente nenhum no Sul, Sudeste e Centro-Oeste.**

Medidas contínuas (mediana dos 748 contra a dos demais): fatia do oponente no 1º turno **26,2% contra 49,0%**; fatia do PT **65,1% contra 39,1%**; terceiros 3,8% contra 5,9%; variação do comparecimento T1 → T2 **-1,2% contra 2,7%**; liberação manual no 2º turno 6,9% contra 7,7%; aptos 9.172 contra 9.415. Por modelo de urna (fração média das seções do município): UE2022 47% contra 36%, UE2020 42% contra 41%, UE2015 9% contra 20%; diferenças moderadas, sem padrão claro e confundidas pela região. **Leitura (descrição, não explicação):** são municípios do Nordeste e do Norte, onde o PT era forte no 1º turno, o oponente tinha fatia pequena e o comparecimento caiu entre os turnos; este teste não mostra por que o oponente cresceu pouco ali.

**3. Decomposição por variação de comparecimento.**

| grupo | municípios | % | perda líquida do oponente (votos) | soma da variação do comparecimento |
|---|---|---|---|---|
| comparecimento caiu (dC < 0) | 528 | 70,6 | 57.376 | -157.683 |
| comparecimento subiu ou igual (dC >= 0) | 220 | 29,4 | 12.683 | 37.322 |
| limite inferior de troca de voto por balanço liquido > 0 | 290 | 38,8 | 15.635 |  |

Dos 748, **528 (70,6%) tiveram queda de comparecimento** (compatível com abstenção seletiva) e **220 (29,4%) tiveram comparecimento igual ou maior** (o oponente parado exigiria novos votantes irem ao PT ou troca de voto). Em soma, o oponente perdeu 70.048 votos líquidos (de 3.001.176 do 1º turno), Lula ganhou 498.842 e o comparecimento caiu 120.361. O **limite inferior de troca de voto por balanço líquido** (a perda do oponente que não cabe em queda líquida de comparecimento nem em aumento de brancos e nulos) é positivo em 290 municípios e soma **15.635 votos**. **O balanço líquido não distingue troca de voto de abstenção seletiva:** um eleitor do oponente que se abstém e um novo eleitor do PT cancelam no líquido.

**4. Os 20 municípios com maior perda absoluta do oponente** (comparecimento de 1.000 ou mais no 1º turno):

| UF | município | comparecimento T1 | oponente T1 | oponente T2 menos T1 | PT T2 menos T1 | comparecimento T2 menos T1 |
|---|---|---|---|---|---|---|
| AP | MACAPÁ | 270.534 | 124.378 | -3.785 | 11.300 | -19.220 |
| AC | SENA MADUREIRA | 24.661 | 16.640 | -2.292 | -293 | -3.773 |
| AC | TARAUACÁ | 22.603 | 12.435 | -2.135 | -370 | -3.491 |
| AC | CRUZEIRO DO SUL | 51.482 | 34.218 | -2.069 | 694 | -4.200 |
| RR | RORAINÓPOLIS | 19.054 | 13.503 | -1.389 | 241 | -2.254 |
| RJ | CAMPOS DOS GOYTACAZES | 290.458 | 160.859 | -1.389 | 24.822 | -3.898 |
| AM | MANACAPURU | 64.079 | 27.295 | -1.354 | 902 | -3.088 |
| AC | MARECHAL THAUMATURGO | 9.352 | 5.369 | -1.352 | -659 | -2.301 |
| AP | SANTANA | 73.177 | 35.791 | -1.350 | 2.786 | -5.320 |
| PA | ORIXIMINÁ | 39.198 | 17.678 | -1.305 | 1.575 | -2.096 |
| AC | FEIJÓ | 18.156 | 9.069 | -1.257 | -58 | -1.966 |
| RR | CARACARAÍ | 12.452 | 8.598 | -1.226 | -106 | -2.032 |
| RR | CANTÁ | 14.635 | 10.037 | -1.209 | 248 | -1.742 |
| AM | COARI | 38.141 | 14.023 | -1.190 | 961 | -1.379 |
| PA | BREVES | 61.897 | 20.877 | -1.136 | 808 | -4.505 |
| AM | ITACOATIARA | 58.385 | 20.163 | -1.059 | 1.114 | -2.783 |
| RJ | MANGARATIBA | 34.080 | 20.418 | -1.030 | 1.397 | -1.882 |
| AC | RODRIGUES ALVES | 10.218 | 7.154 | -997 | -162 | -1.477 |
| RR | ALTO ALEGRE | 11.347 | 7.951 | -989 | 91 | -1.517 |
| AP | MAZAGÃO | 18.989 | 6.402 | -983 | -1.135 | -3.393 |

Todas as seções desses 20 municípios, com T1 e T2 e colunas vazias para o BU impresso: `results/fase3/A31b_20_secoes.csv` (formato de `scripts/04_cruza_bu_impresso.py`); peça aos diretórios partidários locais e aos fiscais pela [página de coleta](boletins-impressos.md). **NÃO EXECUTADO:** o projeto não tem nenhum BU impresso desses municípios. Itacoatiara/AM, Marechal Thaumaturgo/AC, Oriximiná/PA e Mangaratiba/RJ já apareceram em A31.

**5. Teto, em votos de margem (teto de pior caso, não estimativa, fator 2).** (A) Se todo o déficit dos 748 em relação ao crescimento do oponente na UF fosse troca de voto de Flávio para Lula: **234.746 votos de margem (5,30% da margem)**. (B) O excesso de (A) sobre o que o deslocamento nacional reproduziria: **0**, porque o déficit simulado com 2022 (289.343) e com 2018 (669.527) é maior que o observado. Pela regra de exibição do Adendo 14, o G3 não plota (A) (é só o limite do déficit total, sem descontar o que o crescimento nacional explica) nem (B), que é zero.

**Situação.** TESTADO-INCONCLUSIVO. A fração é compatível com o deslocamento nacional; o perfil é regional e de eleitorado PT forte; a maior parte tem queda de comparecimento. **O teste não distingue troca de voto de abstenção seletiva.** **O que fecharia:** BUs impressos e listas de habilitação dos 20 municípios, ou a abstenção por faixa e seção dos mesmos. Código: `scripts/42_a31b_dflavio_menor_igual_1.py`; tabelas: `results/fase3/A31b_*.csv`.

<a id="a32b"></a>

## A32b. Rajadas de liberação manual com limiar absoluto

**Pré-registro:** [Adendo 14](preregistro.md), escrito antes de rodar. **Motivo.** O Adendo 11d mostrou que a definição registrada de rajada (intervalos abaixo do percentil 5 da seção) não consegue ver rajadas, porque uma liberação manual leva mais tempo que isso. **Definição nova, fixada antes:** em cada seção-dia com 10 liberações manuais ou mais, o limiar é **1,5 vezes a mediana do intervalo que precede as liberações manuais da própria seção-dia**; **rajada de k** = k ou mais manuais consecutivas, **sem habilitação biométrica entre elas**, com todos os intervalos entre habilitações consecutivas dentro do limiar. k = 3 (principal) e k = 5 (sensibilidade). Esperado: o mesmo cálculo exato por permutação dos rótulos (a aproximação de Poisson para a probabilidade de pelo menos uma rajada é a do Adendo 11b).

**Cobertura.** Seções-dia com log consistente e 10 manuais ou mais: 2022 T1: 9.200 de 12.022 (limiar mediano 225 s); 2022 T2: 9.011 de 12.375 (limiar mediano 178 s); 2026 T1: 10.814 de 13.644 (limiar mediano 234 s); 2026 T2: 11.071 de 13.788 (limiar mediano 186 s).

| ano | turno | seções-dia | % com rajada k=3 | % esperado k=3 | observado/esperado k=3 | % com rajada k=5 | % esperado k=5 | observado/esperado k=5 |
|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | 12.022 | 15,80 | 14,76 | 1,00 | 1,16 | 0,84 | 1,29 |
| 2022 | 2 | 12.375 | 15,21 | 12,93 | 1,15 | 0,92 | 0,68 | 1,19 |
| 2026 | 1 | 13.644 | 9,33 | 9,34 | 0,97 | 0,18 | 0,14 | 1,12 |
| 2026 | 2 | 13.788 | 10,46 | 8,81 | 1,16 | 0,16 | 0,13 | 1,18 |

(percentuais sobre todas as seções-dia com log consistente; as sem 10 manuais não têm limiar e contam como sem rajada.)

**Frequência de 2026 contra 2022, nas mesmas seções** (efeito fixo de seção, erro padrão agrupado por município):

| turno | k | seções nos dois anos | 2026 menos 2022 (p.p.) | erro padrão | z | p |
|---|---|---|---|---|---|---|
| 1º turno | 3 | 7.868 | -6,67 | 4,02 | -1,66 | 0,097 |
| 1º turno | 5 | 7.868 | -1,00 | 0,35 | -2,88 | 0,004 |
| 2º turno | 3 | 7.965 | -4,12 | 4,14 | -0,99 | 0,320 |
| 2º turno | 5 | 7.965 | -0,80 | 0,28 | -2,84 | 0,005 |

**Leitura.** A razão observado/esperado é de 1,0 a 1,2 em 2022 e em 2026 para k = 3 (de 0,9 a 1,4 na amostra principal): as manuais chegam com a frequência de agrupamento que a ordem aleatória dá, nos dois anos. **As rajadas são menos frequentes em 2026 do que em 2022** (menos 4 a 7 pontos de proporção no k = 3, sem significância; menos 0,8 a 1,0 no k = 5, z de -2,8). A previsão "com abuso" (mais rajadas em 2026, acima do esperado) **não se cumpre**.

**Associação com comparecimento e voto** (2º turno; efeito fixo de local; controle do 1º turno; placebo 2022; amostra principal = estrato aleatório mais Roraima inteira; família A32b com Holm próprio):

| teste | coef. 2026 | ep 2026 | coef. 2022 (placebo) | ep 2022 | p (excesso) | p (Holm) | teto, votos de margem | % da margem | veredito |
|---|---|---|---|---|---|---|---|---|---|
| rajada de liberação manual (k = 3) e comparecimento: 2026/T2 contra 2022/T2 (EF de local, controle do T1) | 0,0000 | 0,0043 | -0,0088 | 0,0064 | 0,127 | 0,127 | 3.391.360 | 76,6 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| rajada de liberação manual (k = 3) e participação de Lula: 2026/T2 contra 2022/T2 (EF de local, controle do T1) | -0,0024 | 0,0034 | -0,0120 | 0,0037 | 0,027 | 0,055 | 4.405.076 | 99,4 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |

**Os coeficientes de 2026 são indistinguíveis de zero** (comparecimento 0,0000, erro padrão 0,0043; participação de Lula -0,0024, 0,0034) ; o teste de excesso sobre o placebo de 2022 fica em Holm de 0,055 (participação de Lula) e 0,13 (comparecimento), e a diferença vem de o placebo de 2022 ser **negativo** (-0,009 e -0,012), não de um coeficiente positivo em 2026. **Mas o teto é inútil:** a amostra principal com 10 manuais ou mais tem só 523 seções, o erro padrão é grande e o teto extrapolado (3.391.360 a 4.405.076 votos de margem, 77% a 99% da margem) vem da falta de poder, não de um efeito; por isso **não é plotado no G3** (regra de exibição, CHANGELOG) e fica só aqui. Na variante com a mediana nacional como limiar (sensibilidade), a família dá o mesmo veredito (INCONCLUSIVA, tetos de 88% a 90% da margem). Na amostra com todos os estratos (seleção no desfecho, rotulada), os coeficientes de k = 3 são 0,0024 (comparecimento) e -0,0003 (Lula), com erro padrão de 0,0007, e o placebo de 2022 é parecido: **sem associação**.

**Situação.** TESTADO-INCONCLUSIVO por falta de poder na associação; no que o teste mede (frequência e agrupamento), **não há excesso em 2026**: há menos rajadas do que em 2022. **O que fecharia:** logs de todas as seções (para ter poder) e a verificação da assinatura dos logs. **O que o teste não faz:** a definição absoluta mede agrupamento no tempo, não o que cada liberação foi. Código: `scripts/43_a32b_rajadas_limiar_absoluto.py`; tabelas: `results/fase3/A32_rajadas_*_abs*.csv`.

<a id="a33"></a>

## A33. Liberação manual no nível da escola (local de votação)

**Pré-registro:** [Adendo 15](preregistro.md) e [Adendo 15a](preregistro.md) (correção da exposição do teto, escrita depois de ver a primeira execução, que tinha um erro meu, e antes de rodar a versão corrigida). **Pergunta.** A liberação manual, olhada por escola e não por seção ou município, se associa a ganho de Lula ou de comparecimento entre os turnos, mais em 2026 do que nos placebos? Unidade: escola (UF, município, zona e local), o que dá massa a locais com várias seções.

**1. Descritivo por faixa de taxa manual (rotulado como descritivo e confundido: a taxa manual depende da idade e do modelo de urna, e escolas pequenas variam mais).**

| ano | taxa manual | escolas | secoes | votantes | votos Lula | votos Flávio | escolas com Lula na frente | % com Lula na frente | idade média (mediana) |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | ate 5% | 21.939 | 130.433 | 35.324.187 | 17.658.216 | 16.465.233 | 12.957 | 59,1 | 42,9 |
| 2026 | 5 a 10% | 51.170 | 302.518 | 77.680.090 | 38.403.418 | 36.775.545 | 28.771 | 56,2 | 45,8 |
| 2026 | 10 a 20% | 16.983 | 59.989 | 14.293.276 | 7.656.070 | 6.210.757 | 10.622 | 62,5 | 47,5 |
| 2026 | 20 a 30% | 917 | 1.386 | 282.320 | 170.264 | 104.013 | 568 | 61,9 | 48,8 |
| 2026 | 30 a 50% | 56 | 96 | 19.616 | 12.065 | 6.918 | 37 | 66,1 | 49,7 |
| 2026 | mais de 50% | 4 | 5 | 780 | 593 | 168 | 3 | 75,0 | 45,8 |
| 2022 | ate 5% | 24.404 | 159.428 | 45.414.479 | 21.457.140 | 21.761.820 | 13.144 | 53,9 | 42,5 |
| 2022 | 5 a 10% | 29.410 | 165.281 | 43.209.827 | 20.376.049 | 20.840.131 | 15.917 | 54,1 | 44,4 |
| 2022 | 10 a 20% | 27.411 | 124.291 | 30.955.977 | 15.590.124 | 14.049.283 | 16.460 | 60,0 | 44,9 |
| 2022 | 20 a 30% | 6.244 | 16.640 | 3.759.218 | 2.356.958 | 1.242.890 | 4.720 | 75,6 | 45,7 |
| 2022 | 30 a 50% | 1.078 | 1.547 | 315.038 | 227.385 | 74.548 | 889 | 82,5 | 46,2 |
| 2022 | mais de 50% | 30 | 39 | 7.384 | 4.811 | 2.275 | 20 | 66,7 | 45,8 |

Escolas com mais de 20% de liberação manual: **977 em 2026 contra 7.352 em 2022**. A distribuição de 2026 é bem mais comprimida na faixa de 5% a 10%.

**2. Teste com unidade = escola** (efeito fixo de zona; controles de idade média e de voto do PT no 1º turno; placebos 2022 e 2018; simetria com o oponente; variante com efeito fixo de município como robustez):

| variante | desfecho | ano | FE | coef | ep | n |
|---|---|---|---|---|---|---|
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2026 | zona | -0,0168 | 0,0030 | 90.986 |
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2022 | zona | -0,0019 | 0,0020 | 88.519 |
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2018 | zona | -0,0209 | 0,0047 | 88.354 |
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2026 | municipio | -0,0071 | 0,0031 | 90.798 |
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2022 | municipio | -0,0027 | 0,0021 | 88.297 |
| taxa manual da escola | variacao da participacao de Lula (T2 menos T1) | 2018 | municipio | -0,0162 | 0,0068 | 88.130 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2026 | zona | -0,0235 | 0,0042 | 90.986 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2022 | zona | 0,0029 | 0,0028 | 88.519 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2018 | zona | 0,0113 | 0,0038 | 88.354 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2026 | municipio | -0,0110 | 0,0043 | 90.798 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2022 | municipio | 0,0046 | 0,0030 | 88.297 |
| taxa manual da escola | variacao do comparecimento (T2 menos T1) | 2018 | municipio | 0,0053 | 0,0033 | 88.130 |
| taxa manual da escola | variacao do voto do oponente por apto | 2026 | zona | -0,0026 | 0,0032 | 90.986 |
| taxa manual da escola | variacao do voto do oponente por apto | 2022 | zona | -0,0007 | 0,0020 | 88.519 |
| taxa manual da escola | variacao do voto do oponente por apto | 2018 | zona | 0,0220 | 0,0034 | 88.354 |
| taxa manual da escola | variacao do voto do PT por apto | 2026 | zona | -0,0370 | 0,0042 | 90.986 |
| taxa manual da escola | variacao do voto do PT por apto | 2022 | zona | -0,0048 | 0,0026 | 88.519 |
| taxa manual da escola | variacao do voto do PT por apto | 2018 | zona | 0,0053 | 0,0067 | 88.354 |
| excesso sobre a mesma escola no ano anterior | variacao da participacao de Lula (T2 menos T1) | 2026 | zona | -0,0007 | 0,0019 | 84.275 |
| excesso sobre a mesma escola no ano anterior | variacao da participacao de Lula (T2 menos T1) | 2022 | zona | -0,0006 | 0,0018 | 83.911 |
| excesso sobre a mesma escola no ano anterior | variacao do comparecimento (T2 menos T1) | 2026 | zona | 0,0022 | 0,0026 | 84.275 |
| excesso sobre a mesma escola no ano anterior | variacao do comparecimento (T2 menos T1) | 2022 | zona | -0,0013 | 0,0025 | 83.911 |

Família de testes de excesso (2026 contra o placebo mais exigente; Holm sobre a família):

| teste | coef. 2026 | ep 2026 | placebo | coef. placebo | p (excesso) | p (Holm) | teto, votos de margem | % da margem | veredito |
|---|---|---|---|---|---|---|---|---|---|
| variação da participação de Lula (T2 menos T1), PT: 2026 contra 2022 e 2018 (taxa manual da escola, EF de zona) | -0,0168 | 0,0030 | 2022/T2 | -0,0019 | 1,000 | 1,000 | 221.830 | 5,0 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| variação da participação de Lula (T2 menos T1), oponente (simetria): 2026 contra 2022 e 2018 (taxa manual da escola, EF de zona) | 0,0168 | 0,0030 | 2018/T2 | 0,0209 | 0,770 | 1,000 | 346.914 | 7,8 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| variação do comparecimento (T2 menos T1), PT: 2026 contra 2022 e 2018 (taxa manual da escola, EF de zona) | -0,0235 | 0,0042 | 2018/T2 | 0,0113 | 1,000 | 1,000 | 0 | 0,0 | REFUTADA (sem excesso, teto <1% da margem) |
| variação da participação de Lula (T2 menos T1), PT: 2026 contra 2022 (excesso sobre 2022 da mesma escola, EF de zona) | -0,0007 | 0,0019 | 2022/T2 (contra 2018) | -0,0006 | 0,521 | 1,000 | 68.414 | 1,5 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| variação da participação de Lula (T2 menos T1), oponente (simetria): 2026 contra 2022 (excesso sobre 2022 da mesma escola, EF de zona) | 0,0007 | 0,0019 | 2022/T2 (contra 2018) | 0,0006 | 0,479 | 1,000 | 72.911 | 1,6 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| variação do comparecimento (T2 menos T1), PT: 2026 contra 2022 (excesso sobre 2022 da mesma escola, EF de zona) | 0,0022 | 0,0026 | 2022/T2 (contra 2018) | -0,0013 | 0,167 | 1,000 | 98.984 | 2,2 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |

**Leitura.** Em 2026, quanto maior a taxa manual da escola, **menor** o ganho de Lula entre os turnos (coeficiente negativo, mesmo sinal do placebo de 2018 e distinto do de 2022, que é próximo de zero) e menor o comparecimento. A previsão "com esquema" (excesso de ganho de Lula e de comparecimento só em 2026) **não se cumpre**; o menor p de excesso é 0,17, antes do Holm, e a simetria com o oponente tem o sinal oposto, como a identidade impõe. Os tetos desta tabela (de 0 a 8% da margem) vêm da incerteza do coeficiente multiplicada pela exposição, não de um efeito, e por isso **não são plotados no G3** (regra de exibição, CHANGELOG). A leitura mais simples do sinal negativo é de composição: escolas com muita liberação manual são mais rurais e mais velhas, e o controle de idade média não esgota isso. Uma associação negativa não prova ausência de manipulação em um subconjunto menor; ela só é incompatível com o padrão amplo pré-registrado.

**3. Escolas extremas** (top 1% em excesso de liberação manual sobre o esperado pela idade e pelo modelo de urna ajustado em 2022, e acima da própria escola em 2022 ou ausente em 2022):

910 escolas no top 1% (corte de excesso de 9,2 pontos percentuais); 661 listadas depois do filtro de 2022 (das quais 87 sem local equivalente em 2022), com 1.079 seções e 225.927 votantes. Lista completa: `results/fase3/A33_escolas_extremas.csv`. **Teto** (todo o excesso de liberação manual lido como voto a favor de um só lado, fator 1): 29.654 votos de margem (0,67% da margem); acima do ruído do modelo (1,645 sigma): 8.125 votos de margem (0,18%). **Teto de pior caso, não estimativa.**

| pos. | SG_UF | município | local | seções | votantes T2 | manual 2026 | previsto pela idade | manual 2022 | idade média | Lula T1 | Flávio T1 | Lula T2 | Flávio T2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MA | ANAJATUBA | ESCOLA MUNICIPAL PAULO DE JESUS PEREIRA | 1 | 129 | 82% | 9% | 9% | 41 | 124 | 11 | 118 | 9 |
| 2 | BA | GLÓRIA | (sem nome na tabela do TSE) | 1 | 155 | 74% | 10% | 5% | 43 | 126 | 9 | 142 | 11 |
| 3 | CE | JAGUARIBE | CENTRO SOCIAL MARIETA CALS | 2 | 388 | 62% | 14% | 32% | 59 | 263 | 58 | 309 | 68 |
| 4 | CE | CAMOCIM | CENTRO DE ESPECIALIDADES ODONTOLOGICAS - CEO | 2 | 373 | 47% | 9% | 21% | 42 | 193 | 139 | 217 | 144 |
| 5 | PR | TOMAZINA | SECRETARIA MUNICIPAL DE EDUCAÇÃO | 3 | 610 | 46% | 8% | 5% | 46 | 187 | 342 | 240 | 357 |
| 6 | BA | TANQUE NOVO | PRÉDIO ESCOLAR JOSÉ ONÓRIO | 3 | 709 | 48% | 11% | 10% | 42 | 561 | 70 | 606 | 79 |
| 7 | RS | NOVA BOA VISTA | SALAO DA COMUNIDADE LINHA MIRIM | 1 | 108 | 51% | 15% | 14% | 49 | 16 | 74 | 24 | 80 |
| 8 | RS | OSÓRIO | E E F METODISTA NEHYTA RAMOS | 3 | 654 | 40% | 11% | 11% | 54 | 263 | 266 | 324 | 306 |
| 9 | BA | BOM JESUS DA SERRA | CRECHE MUNICIPAL FONTE DO SABER | 2 | 427 | 37% | 10% | n/d | 32 | 317 | 76 | 334 | 88 |
| 10 | SP | PEDREGULHO | EMEI LEIDE EMÍLIA COMODARO DE OLIVEIRA | 3 | 802 | 35% | 8% | 3% | 45 | 314 | 342 | 412 | 342 |
| 11 | BA | PARATINGA | IGREJA DA BARAUNAS | 1 | 138 | 36% | 9% | 2% | 41 | 102 | 19 | 112 | 24 |
| 12 | RS | COTIPORÃ | ESCOLA ESTADUAL JACINTO SILVA | 4 | 1.194 | 37% | 11% | 14% | 48 | 200 | 802 | 273 | 891 |
| 13 | MA | SÃO JOSÉ DE RIBAMAR | ESCOLA MUNICIPAL SÃO FRANCISCO | 1 | 122 | 32% | 7% | n/d | 35 | 56 | 38 | 68 | 49 |
| 14 | PR | TOMAZINA | CENTRO MUNICIPAL DE EDUCAÇÃO INFANTIL | 4 | 773 | 35% | 10% | 6% | 50 | 262 | 412 | 294 | 450 |
| 15 | RS | VISTA GAÚCHA | SALÃO DA COMUNIDADE DE TIRADENTES | 1 | 118 | 31% | 6% | 29% | 50 | 45 | 59 | 50 | 65 |
| 16 | MA | VIANA | ESCOLA MUNICIPAL BEIJAMIM COSTA | 1 | 129 | 30% | 7% | n/d | 42 | 104 | 14 | 118 | 11 |
| 17 | MG | SÃO GONÇALO DO RIO ABAIXO | ESCOLA MUNICIPAL DE SÃO JOSÉ | 2 | 486 | 33% | 10% | 4% | 49 | 244 | 173 | 284 | 186 |
| 18 | SC | CERRO NEGRO | NUCLEO MUNICIPAL ORIVAL DE OLIVEIRA BRANCO | 1 | 197 | 31% | 8% | 24% | 49 | 95 | 85 | 112 | 82 |
| 19 | RS | HULHA NEGRA | CÂMARA DE VEREADORES DE HULHA NEGRA | 1 | 260 | 31% | 8% | 9% | 43 | 107 | 125 | 119 | 131 |
| 20 | BA | SÃO FRANCISCO DO CONDE | LUZIENE AMÁLIA SANTOS ROCHA | 3 | 713 | 31% | 9% | n/d | 45 | 578 | 52 | 637 | 56 |

**Leitura.** As extremas **não são explicadas pela idade** (idade média de 32 a 59 anos nas 20 primeiras, previsto de 6% a 15%, observado de 30% a 82%): o excesso existe, mas é pequeno em votos, porque **92% têm 3 seções ou menos** e a mediana é de 1 seção. Elas estão em estados dos dois lados (BA, MA e CE; RS, SC, PR e SP), e a mudança média da fatia de Lula entre os turnos nelas é de +1,5 pontos, **menos** que os +3,0 pontos da média nacional por escola. Uma única seção com 82% de liberação manual e T1 e T2 quase iguais (Anajatuba/MA) lembra defeito do leitor biométrico, hipótese operacional que o log da urna e o BU impresso confirmam ou descartam; **não é conclusão**. Todas as seções das 20 primeiras, com T1 e T2 e colunas vazias para o BU impresso: `results/fase3/A33_20_escolas_secoes.csv` (40 seções); elas entram no pedido LAI 07 e na [coleta de BUs](boletins-impressos.md).

**4. Sincronia nos logs** (escolas com 3 ou mais seções com log consistente; fração de eventos manuais de seções da mesma escola que caem na mesma janela de 60 s e de 180 s, contra o nulo N1 = rótulos manuais embaralhados dentro da própria seção, preservando o ritmo, e N2 = pares de escolas diferentes da mesma UF; 2022 contra 2026):

Cobertura (logs parciais, ver A32): 2022 T1: 1.182 escolas (27 UFs); 2022 T2: 1.197 escolas (27 UFs); 2026 T1: 1.261 escolas (27 UFs); 2026 T2: 1.263 escolas (27 UFs).

| ano | turno | janela (s) | escolas | pares coincidentes | esperado (N1) | razão | z |
|---|---|---|---|---|---|---|---|
| 2022 | 1 | 60 | 1.182 | 129.408 | 123.671 | 1,05 | 12,3 |
| 2022 | 1 | 180 | 1.182 | 350.319 | 330.667 | 1,06 | 25,2 |
| 2022 | 2 | 60 | 1.196 | 156.635 | 141.255 | 1,11 | 29,6 |
| 2022 | 2 | 180 | 1.196 | 399.575 | 367.310 | 1,09 | 38,1 |
| 2026 | 1 | 60 | 1.261 | 127.026 | 121.023 | 1,05 | 13,1 |
| 2026 | 1 | 180 | 1.261 | 353.485 | 332.400 | 1,06 | 27,0 |
| 2026 | 2 | 60 | 1.263 | 177.252 | 160.785 | 1,10 | 29,3 |
| 2026 | 2 | 180 | 1.263 | 460.970 | 426.752 | 1,08 | 34,2 |

**Leitura.** Há uma sincronia pequena em **os dois anos** (razão de 1,05 a 1,11 em 2022; de 1,05 a 1,10 em 2026), com z alto porque são milhões de eventos. Ela é do mesmo tamanho nos dois anos (em 2026 é igual ou menor), e o nulo N2 dá razões de 1,04 a 1,08 nos dois anos: seções da mesma escola compartilham fila, horário de pico e mesários, o que explica uma sincronia pequena. **Não há sincronia de 2026 acima da de 2022**, que era a previsão "com esquema".

**Situação.** TESTADO-INCONCLUSIVO. Três das quatro previsões "sem esquema" se cumprem (sem excesso sobre os placebos, ainda que o coeficiente de 2026 seja mais negativo que o de 2022; sem sincronia acima de 2022; extremas pequenas em votos). A quarta, "extremas explicadas pela idade", **não** se cumpre, e isso fica aberto. O teste não vê o que cada liberação manual foi. **O que fecharia:** BU impresso, lista de habilitação e ata das 20 escolas (LAI 07), e os logs de todas as seções. Código: `scripts/44_a33_escolas.py`; tabelas: `results/fase3/A33_*.csv`.
