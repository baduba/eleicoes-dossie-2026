# Fase 3: hipóteses adversariais (A20 a A28)

> **Unidade: votos de margem** (variação da diferença Lula menos Flávio; trocar um voto muda a margem em 2; definição em [Metodologia](metodologia.md)). Margem oficial: 4.430.191. Todo teto é **teto de pior caso, não estimativa**. Os testes de forma não têm teto em votos.

Previsões, critérios e o que cada teste cobre foram registrados no [Adendo 8](preregistro.md) **antes** de rodar. Cada teste descreve a **classe de falha** que cobre e o **rastro esperado** nos dados públicos, não como produzir a falha. Quando falta insumo, o teste fica **NÃO EXECUTADO**, com o insumo e como fornecê-lo.

| teste | classe de falha coberta | resultado | teto em votos de margem | veredito |
|---|---|---|---|---|
| [A20](#a20) Cadastro x Censo | eleitorado apto inflado | 80+ e 90+: fração de municípios com mais aptos que habitantes acima de 2018 e 2022 (formal; ver ressalva); 16+ e 100+: sem excesso | comparecimento 80+ acima das taxas de 2022: 459.099 votos de margem (teto de pior caso, não estimativa; 10,4% da margem) | EXCESSO DETECTADO (forma) em 80+ e 90+, **com ressalva de desenho**; TESTADO-INCONCLUSIVO |
| [A21](#a21) Logs, ritmo dos votos | registro de votos fora do ritmo real | intervalos < 10 s: nenhum, em nenhum ano; último voto depois do horário nominal explicado pela prorrogação de 25/10 | sem conversão em votos (amostra) | parcial; EXCESSO DETECTADO (forma) em uma medida, **com ressalva** |
| [A22](#a22) Coerência entre cargos | desvio uniforme só no presidente | **NÃO EXECUTADO** (falta a tabela de coligações) | n/a | NÃO EXECUTADO |
| [A23](#a23) Fiscalização | comportamento diferente onde há ou não fiscal | **NÃO EXECUTADO** (sem lista de seções com fiscal) | n/a | NÃO EXECUTADO |
| [A24](#a24) Experimento natural do teste de integridade | urna que se comporta diferente fora do teste | **NÃO EXECUTADO** (lista de seções não pública) | n/a | NÃO EXECUTADO |
| [A25](#a25) Urnas substituídas | troca de urna como ponto de intervenção | seção com troca x vizinhas: ver A6 (sem efeito); antes x depois da troca: NÃO EXECUTADO | n/a (A6: teto abaixo de 1% da margem) | parcial |
| [A26](#a26) Integridade da publicação | arquivo publicado alterado depois | 233 arquivos: tamanho igual em 233; hash oficial igual em 224 de 224; nenhum modificado depois do primeiro download | n/a | SEM ALTERAÇÃO DETECTADA |
| [A27](#a27) Seções fabricadas | seções sem eleitores reais | 427 seções novas com comparecimento ≥ 95%: perfil abaixo | 44.735 votos de margem (teto de pior caso, não estimativa; 1,0% da margem): todos os votos de Lula nas 427 seções, suposto inválidos | TESTADO-INCONCLUSIVO |
| [A28](#a28) Pedidos LAI | dados que só o poder público tem | 6 pedidos redigidos em `lai/`; **nenhum protocolado** | n/a | NÃO EXECUTADO |

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

**A20b, perfil de idade e sexo das seções novas:** NÃO EXECUTADO. O perfil público é por zona, não por seção. Insumo: perfil do eleitorado por seção (pedido ao TSE).

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

## A22. Coerência entre cargos: NÃO EXECUTADO

**Classe de falha coberta:** desvio uniforme restrito ao cargo de presidente, invisível a testes de valor atípico. **Rastro esperado:** deslocamento sistemático do resíduo entre o voto presidencial e os votos em cargos não presidenciais da mesma seção. **Previsão sem manipulação:** resíduo de 2026 igual ao de 2022 e 2018. **Desenho fixado** (Adendo 8): nos estados com 2º turno para governador, participação do candidato presidencial contra a do candidato a governador aliado no mesmo turno, com efeito fixo de UF e controle do 1º turno; estatística: deslocamento médio do resíduo; placebos: 2022 e 2018 nos mesmos estados.

**Por que não rodou:** falta a tabela de coligações por estado (qual candidato a governador está aliado a qual candidato presidencial) e a leitura dos votos por candidato em todos os cargos por seção. Sem isso, qualquer mapeamento seria suposição. **Como fornecer:** o arquivo de candidatos e coligações do TSE (consulta de candidaturas, 2018, 2022, 2026) com a composição de cada coligação; quem o obtiver anexa por issue. É o teste que cobre o desvio uniforme; por isso é o primeiro da lista de tarefas.

<a id="a23"></a>

## A23. Fiscalização: NÃO EXECUTADO

**Classe de falha coberta:** comportamento diferente onde há ou não fiscal. **Previsão sem manipulação:** sem diferença entre seções com e sem fiscal, dentro do mesmo local, com controle do 1º turno e de 2022. **Como fornecer o insumo (partidos e coligações):** uma planilha CSV com as colunas `uf;cd_municipio;zona;secao;turno;partido_ou_coligacao;fiscal_presente` (`sim` ou `nao`), sem nome nem documento de pessoa, enviada por issue. O script comparará seções com e sem fiscal e publicará o resultado, inclusive se for nulo.

<a id="a24"></a>

## A24. Experimento natural do teste de integridade: NÃO EXECUTADO

**Classe de falha coberta:** urna que se comporta diferente quando não é o teste. **Desenho:** seções cuja urna foi para o teste (votaram em urna reserva) contra vizinhas do mesmo local, com controle do 1º turno e de 2022. **Por que não rodou:** a lista de seções afetadas não é pública. **Insumo:** pedido LAI 03 (`lai/03_teste_de_integridade.md`).

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

Seis pedidos redigidos, em `lai/`, com texto neutro, sem dados pessoais e sem acusação: urnas substituídas (horário e motivo), código de carga por urna, testes de integridade por UF, registros de recepção e totalização de 04/10 e 25/10, fiscais credenciados (agregado) e a documentação para verificar a assinatura. **Nenhum foi protocolado**; o registro de protocolos, prazos (20 dias, prorrogáveis por 10), respostas e negativas fica em `lai/registro.csv`.

| arquivo | destinatario | assunto | status |
|---|---|---|---|
| 01_urnas_substituidas.md | TSE e TREs | Urnas substituídas em 2026 | NAO PROTOCOLADO |
| 02_codigo_de_carga.md | TSE | Código de carga por urna | NAO PROTOCOLADO |
| 03_teste_de_integridade.md | TSE e TREs | Testes de integridade e de autenticidade de 2026 | NAO PROTOCOLADO |
| 04_logs_de_totalizacao.md | TSE | Registros de recepção e totalização de 04/10 e 25/10/2026 | NAO PROTOCOLADO |
| 05_fiscais_credenciados.md | TSE e TREs | Credenciamento de fiscais por seção (dados agregados) | NAO PROTOCOLADO |
| 06_assinatura_e_chaves.md | TSE | Verificação independente da assinatura digital dos arquivos de urna | NAO PROTOCOLADO |
