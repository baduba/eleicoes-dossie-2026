# Dossiê: auditoria dos dados do 2º turno presidencial de 2026 (Lula x Flávio Bolsonaro)

Gerado em 2026-10-28 a partir dos arquivos públicos do TSE. Todos os números deste texto vêm dos CSVs em `results/fase1/` (script `03_monta_dossie.py`). Previsões e critérios foram fixados antes dos dados em `00_preregistro.md`.

## 1. Resumo executivo

1. Dados: BWeb (boletim de urna por seção) de 2014, 2018, 2022 e 2026, T1 e T2, 224 zips com hash conferido. Os totais de 2026/T2 são Lula 64.256.232 e Flávio 59.826.041, iguais aos divulgados.
2. Consistência: o BWeb coincide com `votacao_secao` em todas as seções pareadas de 2014 a 2026, exceto 1 seção de 2018/T1 em que `votacao_secao` tem 66 votos a mais que o BWeb e que o total divulgado pelo TSE (nenhuma divergência em 2022 ou 2026), e com a totalização por município/zona de 2026 (0 zonas com diferença). Há 0 violações de consistência interna dos BUs.
3. Liberação manual (biometria cadastrada, eleitor não habilitado por ela): 8.632.488 em 2026/T2, o número citado no relatório; 10.011.347 em 2022/T2. A taxa agregada passou de 8,06% para 6,73%.
4. H1: com efeito fixo de local de votação e controle do voto da própria seção no T1, a taxa manual não prevê voto adicional em Lula no T2 (coeficiente 0,002 contra 0,016 em 2022). Teto de pior caso: 0 votos.
5. H3 e H4: a contagem do relatório foi reproduzida (339.593 seções entre 17h01 e 17h15 pelo relógio cru da urna). 6.342 seções registraram encerramento a partir das 19h no relógio da urna, contra 20 em 2022/T2. Nelas, o voto em Lula não difere das demais seções do mesmo local; tetos de 0,03% a 0,19% da margem.
6. O número de votos dados depois das 17h não é mensurável com estes dados (o BWeb não traz log de votação).
7. H5 a H8 e régua histórica: o comparecimento, os outliers locais e os dígitos de 2026 ficam dentro da faixa observada em 2014, 2018 e 2022. Nenhum dos padrões A, B ou C se ajusta pelo critério fixado (C: 5 de 12 métricas; ver 3.13).
8. Dois testes mostram excesso depois de Holm: votos de Flávio por apto x taxa manual (teto 122.543 votos, 2,77% da margem, sentido favorável a Flávio) e variação de voto em Lula entre anos x variação da taxa manual (teto 38.394 votos, 0,87%).
9. Residuais sem causa identificada: 639 seções com comparecimento >= 95% (2,5 vezes o esperado pela composição; 1,9 vezes já no T1; teto 0,43%) e seções novas (+0,54 p.p. de Lula no T2 dado o T1; +1,34 p.p. em 2018; teto de pior caso 2,08%).
10. Impacto agregado: a soma dos tetos dos testes com excesso detectado é 38.394 votos no sentido pró-Lula (0,87% da margem) e 122.543 no sentido pró-Flávio. Nenhum achado, isolado ou somado, alcança 4.430.191 votos. Não executado: cruzamento com boletins impressos (sem insumo).

## 2. Dados e versões

| Insumo | Origem | Arquivos | Verificação |
|---|---|---|---|
| BWeb 2026, 2022 | `cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{2026,2022}/buweb/` via API CKAN (`dadosabertos.tse.jus.br`) | 56 zips por ano (27 UF + ZZ, T1 e T2) | SHA-512 do TSE conferido: 112/112 |
| BWeb 2018, 2014 | mesmo catálogo | 56 zips por ano | 2018: SHA-512; 2014: SHA-1 (o que o TSE publica); 112/112 conferidos |
| `votacao_secao` 2014 a 2026, `detalhe_votacao_secao` 2022 e 2026, `votacao_candidato_munzona` 2026 | `cdn.tse.jus.br/estatistica/sead/odsele/` | 1 zip por produto/ano | usados em H9, tipo de local e modelo de urna |

Hash SHA-256 de todos os insumos: `dados/sha256_entradas.txt`. URLs: `dados/urls_origem.txt`.

**Colunas do BWeb usadas** (nomes encontrados no cabeçalho):

| Conceito | 2026 | 2022 | 2018 | 2014 |
|---|---|---|---|---|
| Liberação manual | `QT_ELEI_BIOM_SEM_HABILITACAO` | `QT_ELEITORES_BIOMETRIA_NH` | `QT_ELEITORES_BIOMETRIA_NH` | inexistente |
| Abertura / encerramento | `DT_ABERTURA`, `DT_ENCERRAMENTO` | iguais | iguais | inexistentes |
| Recebimento / emissão do BU | `DT_BU_RECEBIDO`, `DT_EMISSAO_BU` | iguais | inexistentes | só data de recebimento |
| Seções agregadas | `DS_SECOES_AGREGADAS` | `DS_AGREGADAS` | `DS_AGREGADAS` | posicional |
| Formato | CSV com cabeçalho | CSV com cabeçalho | CSV com cabeçalho (`SG_ UF` com espaço) | `.txt` sem cabeçalho, 31 campos posicionais |

**Definição da medida de liberação manual.** O dicionário do TSE descreve o campo como "eleitores com biometria cadastrada que não foram habilitados por meio dela". Não é o total de liberações manuais: quem não tem biometria cadastrada não entra, e o denominador (eleitores com biometria) não está disponível.

**Pontos de atenção nos dados:**

- Catálogo CKAN do TSE: os dois recursos de RR/T2/2026 apontam para o `.sha512`. O zip existe em `.../buweb/bweb_2t_RR_261020260742.zip` (HTTP 200) e foi baixado direto, com hash conferido.
- Horários `DT_ABERTURA`, `DT_ENCERRAMENTO`, `DT_EMISSAO_BU` são relógio local da urna (Acre abre às 06h00 e fecha às 15h00). O atraso de fechamento usa o horário nominal do município (moda da abertura + 9 h). `DT_BU_RECEBIDO` é horário do servidor do TSE.
- Seções "Não instalada", "Não apurada" e "Anulada e apurada em separado" trazem `#NULO#` ou -1 nos campos de votável e biometria. São tratadas só nesse caso exato, ficam fora das análises (somente urna "Apurada", exterior excluído, salvo indicação).
- Em 2022, as urnas UE2009 e UE2010 do Espírito Santo registram taxa manual exatamente 0,0 (3.339 seções), enquanto as mesmas urnas em outros estados têm cerca de 15%. É artefato de medição e explica o único estado em que a taxa subiu de 2022 para 2026.
- Versões: Python 3.12, pandas 3.1, scipy 1.18, pyarrow, matplotlib 3.11. Hashes dos scripts (SHA-256, 16 primeiros caracteres): `01_prepara_bweb.py` dff9e63cf4b464f0; `01b_locais.py` 8becc04f2c1181bb; `01c_modelo_urna.py` 42745848343abc57; `02_executa.py` 34047bf625a3ec46; `03_monta_dossie.py` 2550c216238595fd; `04_cruza_bu_impresso.py` c2fa12f3f5121b29; `h1_h4.py` 6a505af697305755; `h5_h8.py` 19e7a158411206f7; `h9_h10.py` 21ae5413bb5c4750; `lib_auditoria.py` aba85ca5b1ac6bee.

## 3. Resultados por hipótese

Método comum: regressão com efeito fixo de local de votação (`uf_local`), erro padrão agrupado por local, voto da própria seção no T1 como controle quando o desfecho é o T2, e comparação com **cada** placebo (2022/T1, 2022/T2, 2026/T1, ou o equivalente definido no teste) por teste de interseção-união. O p de "excesso" é unilateral (2026/T2 maior que o placebo, no sentido da alegação) e é o p corrigido por Holm e Benjamini-Hochberg sobre os 23 testes do registro. O teto em votos é `2 x max(0, diferença + 1,645 x ep) x exposição`: o máximo de votos de margem que o fenômeno poderia explicar, supondo causalidade. "Placebo mais exigente" é o de maior estimativa; "pior caso" usa o placebo mais frouxo.

Regra de veredito (Adendo 2 do pré-registro): **excesso detectado e relevante** = Holm < 0,05 e pior caso >= 1% da margem; **excesso detectável, magnitude irrelevante** = Holm < 0,05 e < 1%; **refutada** = Holm >= 0,05 e < 1%; **inconclusiva** = Holm >= 0,05 e >= 1%.

### 3.1 Síntese

| H | Previsão se houver desvio | Previsão se não houver | Resultado | Placebo | Efeito máx. (votos) | % da margem | p Holm | Veredito |
|---|---|---|---|---|---|---|---|---|
| H1 manual x voto Lula (T2, com T1) | coef. > 0 e > placebos, dose-resposta crescente | mesma magnitude nos placebos | 0,0020 (ep 0,0010) | 2022/T2: 0,0162 | 0 | 0,00% | 1,000 | refutada |
| H1 sem controle do T1 | idem | idem | 2026/T2: 0,0696; 2026/T1: 0,0741 | 2026/T1: 0,0741 (2022: -0,0054 e 0,0137) | 19.670 (vs T1/2026); 1.337.198 (vs 2022/T1) | 0,44%; 30,18% | 1,000 | inconclusiva pelo critério, mas a associação é igual no T1 (ver 3.2) |
| H1 simétrico: votos de Flávio/apto | sem efeito | sem efeito | 0,0090 (ep 0,0009) | 2022/T2: -0,0005 | 122.543 | 2,77% | 0,000 | excesso detectado, **sentido favorável a Flávio** |
| H2 "aumento" da liberação manual | taxa sobe 2022 a 2026 | taxa estável ou em queda | 10.011.347 em 2022/T2 e 8.632.488 em 2026/T2 | n/a | n/a | n/a | n/a | refutada (queda de 13,8%) |
| H2 variação de voto x variação manual, dentro do ano | coef. > 0 só em 2026 | igual a 2022 | -0,0025 | 2022: -0,0006 | 1.794 | 0,04% | 1,000 | refutada |
| H2 entre anos (T2 contra T1) | coef. T2 > T1 | igual | T2: -0,0004; T1: -0,0110 | T1 (placebo imperfeito: candidatos diferentes) | 38.394 | 0,87% | 0,000 | excesso detectável, magnitude irrelevante |
| H3 encerramento | tabela do relatório não reproduz ou fecha tarde em massa | reproduz; fecha quase tudo em 17h-17h15 | 17h01-17h15: 339.593 (relatório: 339.593); >= 19h: 6.342 | 2022/T2: 274.561 e 20 | votos após 17h: não mensurável | n/a | n/a | caracterização; contagem do relatório confirmada |
| H4 fecha tarde (15, 60, 115 min), 6 testes | Lula% maior que nas mesmas seções em 2022 e no T1 | igual | de -0,10 a -0,03 p.p. | de -0,09 a 0,02 p.p. | até 8.262 | até 0,19% | 1,00 a 1,00 | refutada |
| H5 comparecimento >= 95% | maioria antiga, manual alto, só no T2 | nova, pequena, local atípico, já no T1 | observado 639; esperado pela composição 259 | 2026/T1: 559 contra 293 | 19.023 | 0,43% | 0,177 | refutada como efeito do T2; nível elevado de 2026 sem causa identificada |
| H6 seções novas | destoam das antigas do mesmo local | iguais | +0,54 p.p. | 2022: 0,00; 2018: +1,34 | 92.023 (vs 2022); 0 (vs 2018) | 2,08% | 1,000 | inconclusiva (depende da linha de base) |
| H7 outliers locais pró-Lula (z ajustado em módulo > 3) | excesso sem espelho | contagem igual a 2022 e simétrica | 44,8 por 10 mil seções; 63,3% dos outliers são pró-Lula | 2022/T1: 47,6; 64,5% | 20.301 | 0,46% | 1,000 | refutada |
| H8 dígitos | último dígito não uniforme; percentuais inteiros em excesso | uniforme, como em 2022 | ver 3.8 | 2022 e 2026/T1 | n/a (teste de forma) | n/a | 1,000 | sem excesso |
| H9 consistência | soma das seções diferente da totalização | igual | 1 seção (66 votos, 2018/T1) e 0 zonas com diferença | n/a | 0 em 2026 | 0% | n/a | consistente em 2026; 1 divergência em `votacao_secao` de 2018/T1 |
| H10 impacto agregado | soma dos excessos comparável a 4.430.191 | soma < 1% | pró-Lula 38.394; pró-Flávio 122.543 | n/a | ver 3.10 | 0,87% | n/a | abaixo de 1% no sentido pró-Lula |
| Boletins impressos | divergência de qualquer tamanho | nenhuma | **não executado** | n/a | n/a | n/a | n/a | sem insumo (ver 3.11) |

### 3.2 H1: liberação manual x voto

Efeito fixo de local de votação, erro agrupado por local; coeficientes em fração do voto válido por unidade de taxa manual.

| spec | ano | turno | coef | ep | n | locais |
|---|---|---|---|---|---|---|
| S0 sem defasagem | 2022 | 1 | -0,0054 | 0,0016 | 447.222 | 68.579 |
| S0 sem defasagem | 2022 | 2 | 0,0137 | 0,0017 | 447.223 | 68.578 |
| S0 sem defasagem | 2026 | 1 | 0,0741 | 0,0025 | 475.790 | 72.441 |
| S0 sem defasagem | 2026 | 2 | 0,0696 | 0,0024 | 475.789 | 72.441 |
| S1 T2 com defasagem T1 | 2022 | 2 | 0,0162 | 0,0008 | 447.220 | 68.578 |
| S1 T2 com defasagem T1 | 2026 | 2 | 0,0020 | 0,0010 | 475.784 | 72.439 |

Leitura: sem controle do T1, a associação de 2026 (0,074 no T1 e 0,070 no T2) é igual nos dois turnos e maior que a de 2022 (-0,005 e 0,014). Ao condicionar no voto da própria seção no T1, o coeficiente do T2 cai a 0,002, abaixo de 2022 (0,016). Ou seja, a relação existe antes do 2º turno e o 2º turno não acrescenta nada. Controles de comparecimento e tamanho da seção (0,067) e de modelo da urna (ver 3.12) não a dissolvem; a causa dessa associação de 2026 não foi identificada.

**Dose-resposta** (faixas da taxa manual contra 0-5%, pontos percentuais de voto em Lula, T2 com T1):

| ano | faixa | coef_pp | ep_pp | secoes_na_faixa |
|---|---|---|---|---|
| 2022 | 5-10% | 0,086 | 0,008 | 153.587 |
| 2022 | 10-20% | 0,205 | 0,011 | 114.869 |
| 2022 | 20-50% | 0,340 | 0,019 | 28.566 |
| 2022 | >50% | 0,174 | 0,127 | 321 |
| 2026 | 5-10% | 0,005 | 0,007 | 238.172 |
| 2026 | 10-20% | 0,023 | 0,011 | 81.180 |
| 2026 | 20-50% | -0,023 | 0,042 | 4.046 |
| 2026 | >50% | -0,031 | 0,184 | 97 |

Em 2022 a curva cresce com a taxa; em 2026 é plana.

**Simetria.** Em 2026, a taxa manual prevê mais votos por apto no T2 para os dois candidatos (Lula 0,019, Flávio 0,009), enquanto em 2022 só Lula (0,027 contra -0,001 para Bolsonaro). O coeficiente de Lula caiu e o de Flávio subiu. Nos redutos de Flávio (Lula T1 < 40%) o coeficiente é -0,0049 e nos de Lula (T1 > 60%), 0,0099, ambos sem excesso sobre 2022.

### 3.3 H2: o aumento da liberação manual

| ano | turno | biom_nh_total | comparecimento_total | taxa_agregada | secoes |
|---|---|---|---|---|---|
| 2018 | 1 | 8.166.806 | 117.364.560 | 6,96% | 454.490 |
| 2018 | 2 | 7.898.943 | 115.933.451 | 6,81% | 454.490 |
| 2022 | 1 | 10.780.979 | 123.682.372 | 8,72% | 472.028 |
| 2022 | 2 | 10.011.347 | 124.252.796 | 8,06% | 472.028 |
| 2026 | 1 | 8.342.249 | 125.275.835 | 6,66% | 499.206 |
| 2026 | 2 | 8.632.488 | 128.236.074 | 6,73% | 499.205 |

O total de 2026/T2 (8.632.488) é o "8,6 milhões" do relatório. Em seções estáveis (aptos entre 0,85x e 1,15x de 2022), 22,6% das seções tiveram queda de mais de 5 p.p. na taxa e 8,6% tiveram alta. O filtro "municípios com biometria nos dois anos" quase não muda o resultado.

A queda acompanha a troca do parque de urnas: em 2022, UE2009 e UE2010 tinham taxa de 14% a 16% e UE2020, 5%; em 2026 as UE2009/2010/2011 saíram e entrou a UE2022, com 6%.

| ano | CD_MODELO_URNA | secoes | taxa_manual | lula_sh |
|---|---|---|---|---|
| 2022 | -1 | 3.585 | 13,67% | 58,8% |
| 2022 | 2009 | 46.161 | 14,25% | 51,8% |
| 2022 | 2010 | 92.786 | 14,40% | 54,7% |
| 2022 | 2011 | 26.433 | 8,58% | 54,8% |
| 2022 | 2013 | 24.296 | 8,74% | 52,3% |
| 2022 | 2015 | 85.164 | 7,16% | 52,4% |
| 2022 | 2020 | 192.462 | 4,54% | 49,2% |
| 2026 | 2013 | 11.423 | 11,01% | 53,7% |
| 2026 | 2015 | 87.184 | 9,78% | 52,2% |
| 2026 | 2020 | 200.448 | 6,15% | 52,1% |
| 2026 | 2022 | 198.686 | 6,15% | 52,0% |

**Onde subiu.** Só o Espírito Santo (2,69 p.p.), por artefato de medição de 2022 (seção 2). Dentro do ES, a variação de voto não se associa à variação da taxa (coeficiente 0,0001, erro padrão 0,008). Maiores quedas: AL (-4,24 p.p.), RO (-3,85 p.p.), RN (-3,46 p.p.), AP (-3,22 p.p.).

### 3.4 H3: encerramento

**Recontagem da tabela do relatório** (relógio cru de `DT_ENCERRAMENTO`, sem ajustar fuso, com exterior):

| ano | turno | antes_17h01 | de_17h01_a_17h15 | de_17h16_a_18h59 | a_partir_de_19h | total |
|---|---|---|---|---|---|---|
| 2018 | 1 | 84.349 | 275.592 | 87.851 | 6.508 | 454.300 |
| 2018 | 2 | 205.558 | 247.744 | 1.014 | 34 | 454.350 |
| 2022 | 1 | 88.485 | 252.498 | 119.360 | 11.565 | 471.908 |
| 2022 | 2 | 195.818 | 274.561 | 1.585 | 20 | 471.984 |
| 2026 | 1 | 70.057 | 311.284 | 109.891 | 7.944 | 499.176 |
| 2026 | 2 | 150.771 | 339.593 | 2.472 | 6.342 | 499.178 |

O valor do relatório para 17h01-17h15 (339.593) é reproduzido exatamente em 2026/T2. A faixa equivalente tem 274.561 seções em 2022/T2 e 247.744 em 2018/T2, e corresponde a fila normal no horário de encerramento. O relógio cru ignora o fuso: os estados do Oeste fecham às 15h ou 16h locais e caem em "antes de 17h01". Com horário nominal por município, 98,2% das seções (sem exterior) fecham até 15 minutos depois do horário.

**Prorrogação.** 6.714 seções (sem exterior; 1,35%) fecharam 115 minutos ou mais depois do horário nominal, com 1.970.400 eleitores com comparecimento registrado, contra 25 seções em 2022/T2. Estados: RJ 2.981, SP 1.649, BA 973, PE 691, PB 309, SE 53. Em RJ são 7,9% das seções do estado.

**Votos depois das 17h.** O BWeb não traz log de votação; os "logs Gedai" do catálogo são de preparação das urnas (gerados em 24/10), não de votação. Por isso o número não é mensurável aqui. A referência externa de 34.330 eleitores (levantamento da imprensa) não foi verificada. O limite por extrapolação da taxa média da seção (`h3_votos_apos_horario_limite.csv`) é um teto frouxo e não deve ser lido como estimativa.

**Hora de recebimento do BU no TSE.** 99,6% dos BUs de 2026/T2 chegaram depois das 19h, mas 98,2% das seções tinham fechado até 15 minutos após o horário nominal. A hora de recebimento reflete o TSE segurando o recebimento, não o fechamento da seção. A leitura anterior desta análise, que usava essa hora como proxy de encerramento, estava errada.

### 3.5 H4: seções que fecharam tarde

Lula% (pontos percentuais) em seções tardias contra as demais do mesmo local, T2/2026 com T1 como controle, e o mesmo teste nas mesmas seções em 2022/T2 e no T1/2026:

| L | spec | coef_pp | ep_pp | secoes_tardias |
|---|---|---|---|---|
| 15 | 2026 T2 c/ lag | -0,050 | 0,037 | 8.373 |
| 15 | placebo 2022 T2 c/ lag (mesmas secoes) | 0,005 | 0,035 | 8.373 |
| 15 | 2026 T2 s/ lag | -0,030 | 0,073 | 8.373 |
| 15 | placebo T1/2026 s/ lag (mesmas secoes) | 0,025 | 0,079 | 8.373 |
| 15 | 2026 T2 c/ lag, EF zona | -0,061 | 0,032 | 8.373 |
| 60 | 2026 T2 c/ lag | -0,025 | 0,049 | 6.608 |
| 60 | placebo 2022 T2 c/ lag (mesmas secoes) | -0,024 | 0,045 | 6.608 |
| 60 | 2026 T2 s/ lag | -0,071 | 0,099 | 6.608 |
| 60 | placebo T1/2026 s/ lag (mesmas secoes) | -0,056 | 0,104 | 6.608 |
| 60 | 2026 T2 c/ lag, EF zona | -0,080 | 0,039 | 6.608 |
| 115 | 2026 T2 c/ lag | -0,028 | 0,051 | 6.268 |
| 115 | placebo 2022 T2 c/ lag (mesmas secoes) | -0,023 | 0,046 | 6.268 |
| 115 | 2026 T2 s/ lag | -0,101 | 0,101 | 6.268 |
| 115 | placebo T1/2026 s/ lag (mesmas secoes) | -0,090 | 0,105 | 6.268 |
| 115 | 2026 T2 c/ lag, EF zona | -0,091 | 0,040 | 6.268 |

Nenhuma estimativa de 2026 supera as de 2022 ou do T1. Com efeito fixo de zona (comparação menos estrita), os coeficientes são negativos (de -0,06 a -0,09 p.p.): fechar tarde não se associa a mais voto em Lula. Contexto: no T1/2026, seções com atraso de 15 minutos ou mais têm +0,58 p.p. de Lula dentro do mesmo local (fila em seções maiores), efeito que não aparece no T2 (-0,03 p.p.).

### 3.6 H5: seções com comparecimento >= 95% e Klimek

| ano | turno | secoes | turnout_ge95 | por_100k | ge95_PT90 | ge95_OPO90 | M5a_PT | M5a_OPO | M5b_PT | M5b_OPO |
|---|---|---|---|---|---|---|---|---|---|---|
| 2014 | 1 | 427.937 | 2.232 | 521,6 | 433 | 6 | 0,00767 | 0,00039 | -0,0244 | 0,0244 |
| 2014 | 2 | 427.938 | 1.036 | 242,1 | 74 | 2 | 0,00123 | 0,00012 | -0,0016 | 0,0016 |
| 2018 | 1 | 453.702 | 959 | 211,4 | 161 | 118 | 0,00319 | 0,00427 | -0,0725 | 0,0725 |
| 2018 | 2 | 453.703 | 503 | 110,9 | 62 | 38 | 0,00172 | 0,00048 | -0,0209 | 0,0209 |
| 2022 | 1 | 471.010 | 262 | 55,6 | 60 | 4 | 0,00128 | 0,00008 | -0,0398 | 0,0398 |
| 2022 | 2 | 471.010 | 232 | 49,3 | 44 | 7 | 0,00090 | 0,00013 | -0,0267 | 0,0267 |
| 2026 | 1 | 497.897 | 559 | 112,3 | 86 | 7 | 0,00114 | 0,00021 | -0,0357 | 0,0357 |
| 2026 | 2 | 497.897 | 639 | 128,3 | 117 | 9 | 0,00152 | 0,00018 | -0,0241 | 0,0241 |

`por_100k` é M5c; M5a é a fração de seções com comparecimento >= 90% e voto >= 90% no candidato; M5b é a correlação comparecimento x voto dentro do local. Figuras de Klimek: `results/fase1/figs/klimek_T2.png` e `klimek_T1.png`; na inspeção visual, 2026 não mostra segunda moda na diagonal (o padrão que a literatura associa a manipulação) e o formato é semelhante ao de 2022. A inspeção visual não é teste; os testes são M5a a M5c acima.

**As 639 seções de 2026/T2.** 66,8% são novas (sem par em 2022), contra 7,6% de todas as seções; mediana de 161 aptos contra 327; taxa manual média de 7,9% contra 6,9%; atraso de fechamento médio de 4,0 contra 4,1 minutos. Comparecimento médio no T1: 94,4%; só 35 seções passaram de < 90% no T1 a >= 95% no T2, com 5.737 votos válidos. Por tipo de local (nome do local):

| tipo | n_ge95 | n_total | pct_ge95_dentro_do_tipo | pct_do_total_ge95 | pct_do_total_secoes |
|---|---|---|---|---|---|
| escola_outro | 554 | 490.606 | 0,11% | 86,7% | 98,54% |
| hospital_asilo | 0 | 113 | 0,00% | 0,0% | 0,02% |
| indigena | 32 | 838 | 3,82% | 5,0% | 0,17% |
| militar | 0 | 52 | 0,00% | 0,0% | 0,01% |
| prisional | 6 | 187 | 3,21% | 0,9% | 0,04% |
| quilombola | 4 | 227 | 1,76% | 0,6% | 0,05% |
| rural_comunidade | 43 | 5.874 | 0,73% | 6,7% | 1,18% |

**Padronização.** Com as taxas de 2022 por tipo de local e tamanho, esperavam-se 259 seções >= 95% no T2 (293 no T1); observadas 639 e 559, razões de 2,47 e 1,91. A composição não explica o nível de 2026, e o excesso já existe no T1. A diferença T2 menos T1 (log da razão, 0,258) dá p unilateral de 0,0084 e 0,177 após Holm; teto 19.023 votos (0,43%).

**Taxa de seções >= 95% por 10 mil seções, por tamanho** (aptos):

| tamanho | turno | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|
| 151-300 | 1 | 82,5 | 32,6 | 5,9 | 10,8 |
| 151-300 | 2 | 36,7 | 15,4 | 5,3 | 15,1 |
| 51-150 | 1 | 335,1 | 238,6 | 163,5 | 390,4 |
| 51-150 | 2 | 201,7 | 144,4 | 139,8 | 351,4 |
| <=50 | 1 | 886,5 | 850,5 | 500,0 | 846,1 |
| <=50 | 2 | 638,3 | 459,2 | 335,2 | 766,3 |
| >300 | 1 | 27,8 | 5,1 | 1,4 | 1,4 |
| >300 | 2 | 11,0 | 2,5 | 1,4 | 2,8 |

O nível de 2026 em seções de 51 a 150 aptos supera o de todos os anos anteriores nos dois turnos; em seções de mais de 150 aptos, 2014 tinha taxa maior. Entre as 200 seções antigas pareadas com >= 95% em 2026, os aptos ficaram estáveis (1,01x a mediana de 2022), o comparecimento subiu 6,1% e o comparecimento mediano de 2022 já era 92,1%: o efeito vem do numerador, não de queda de aptos.

### 3.7 H6: seções novas

| ano | spec | coef | ep | p | secoes_novas | n |
|---|---|---|---|---|---|---|
| 2026 | lula_sh T2 / lula_sh T1 | 0,00536 | 0,00017 | 0,0000 | 37.513 | 475.784 |
| 2026 | turnout T2 / turnout T1 | -0,00652 | 0,00018 | 0,0000 | 37.513 | 475.784 |
| 2026 | lula_sh T1 (sem lag) | 0,01409 | 0,00042 | 0,0000 | 37.513 | 475.784 |
| 2026 | turnout T1 (sem lag) | 0,00448 | 0,00046 | 0,0000 | 37.513 | 475.784 |
| 2022 | lula_sh T2 / lula_sh T1 | 0,00004 | 0,00015 | 0,7811 | 33.757 | 447.220 |
| 2022 | turnout T2 / turnout T1 | -0,00129 | 0,00016 | 0,0000 | 33.757 | 447.220 |
| 2022 | lula_sh T1 (sem lag) | 0,01717 | 0,00043 | 0,0000 | 33.757 | 447.220 |
| 2022 | turnout T1 (sem lag) | 0,01618 | 0,00040 | 0,0000 | 33.757 | 447.220 |
| 2018 | lula_sh T2 / lula_sh T1 | 0,01344 | 0,00027 | 0,0000 | 103.372 | 426.397 |
| 2018 | turnout T2 / turnout T1 | -0,00291 | 0,00018 | 0,0000 | 103.372 | 426.397 |
| 2018 | lula_sh T1 (sem lag) | 0,00160 | 0,00041 | 0,0001 | 103.372 | 426.397 |
| 2018 | turnout T1 (sem lag) | 0,00537 | 0,00047 | 0,0000 | 103.372 | 426.397 |

Robustez do coeficiente de `nova` em Lula% T2 dado o T1 (interação com o T1 centrado, controles de tamanho e comparecimento, só seções de 100 a 500 aptos):

| ano | variante | coef_nova | ep | secoes_novas |
|---|---|---|---|---|
| 2026 | interacao nova x T1 (efeito no T1 medio) | 0,00580 | 0,00017 | 37.513 |
| 2026 | controles log aptos e comparecimento T1 | 0,00528 | 0,00017 | 37.513 |
| 2026 | so secoes de 100 a 500 aptos | 0,00540 | 0,00016 | 36.203 |
| 2022 | interacao nova x T1 (efeito no T1 medio) | 0,00011 | 0,00015 | 33.757 |
| 2022 | controles log aptos e comparecimento T1 | 0,00005 | 0,00015 | 33.757 |
| 2022 | so secoes de 100 a 500 aptos | 0,00000 | 0,00015 | 32.587 |
| 2018 | interacao nova x T1 (efeito no T1 medio) | 0,01345 | 0,00027 | 103.372 |
| 2018 | controles log aptos e comparecimento T1 | 0,01410 | 0,00027 | 103.372 |
| 2018 | so secoes de 100 a 500 aptos | 0,01356 | 0,00027 | 101.230 |

O efeito de 2026 (+0,5 p.p.) é estável nas três variantes, ou seja, não é artefato de inclinação heterogênea nem de tamanho. Em 2022 o coeficiente é zero e em 2018 é +1,3 p.p., maior que o de 2026. Contra o placebo mais exigente (2018) não há excesso; contra 2022, o teto de pior caso é 2,08% da margem. Veredito: inconclusivo, porque depende de qual ano serve de linha de base. A causa não foi identificada (composição por idade e renda não está disponível por seção).

### 3.8 H7 e H8: outliers locais e dígitos

| ano | turno | secoes_em_locais_ge4 | sobredispersao_phi | up_3 | down_3 | taxa_up_10k | taxa_down_10k | razao_up_down |
|---|---|---|---|---|---|---|---|---|
| 2014 | 1 | 345.046 | 1,551 | 1.022 | 1.127 | 29,6 | 32,7 | 0,91 |
| 2014 | 2 | 345.914 | 1,545 | 1.117 | 1.044 | 32,3 | 30,2 | 1,07 |
| 2018 | 1 | 374.992 | 1,550 | 1.366 | 847 | 36,4 | 22,6 | 1,61 |
| 2018 | 2 | 375.480 | 1,587 | 1.947 | 912 | 51,9 | 24,3 | 2,13 |
| 2022 | 1 | 396.419 | 1,536 | 1.886 | 1.040 | 47,6 | 26,2 | 1,81 |
| 2022 | 2 | 396.442 | 1,535 | 1.805 | 1.008 | 45,5 | 25,4 | 1,79 |
| 2026 | 1 | 423.321 | 1,551 | 1.697 | 1.071 | 40,1 | 25,3 | 1,58 |
| 2026 | 2 | 423.316 | 1,545 | 1.895 | 1.100 | 44,8 | 26,0 | 1,72 |

Outlier = seção cujo voto em Lula destoa da média das outras seções do mesmo local (leave-one-out), com variância binomial e sobredispersão estimada em cada eleição (phi ≈ 1,5 em todas). `up` é pró-Lula e `down`, pró-Flávio/oponente.

| ano | turno | cand | n | chi2 | p | V_cramer |
|---|---|---|---|---|---|---|
| 2014 | 1 | PT | 423.225 | 19,6 | 0,0208 | 0,00227 |
| 2014 | 1 | OPO | 380.553 | 156,4 | 0,0000 | 0,00676 |
| 2014 | 2 | PT | 426.168 | 8,8 | 0,4525 | 0,00152 |
| 2014 | 2 | OPO | 412.167 | 51,0 | 0,0000 | 0,00371 |
| 2018 | 1 | PT | 412.867 | 520,9 | 0,0000 | 0,01184 |
| 2018 | 1 | OPO | 426.922 | 108,6 | 0,0000 | 0,00532 |
| 2018 | 2 | PT | 450.305 | 13,2 | 0,1547 | 0,00180 |
| 2018 | 2 | OPO | 435.489 | 26,2 | 0,0019 | 0,00259 |
| 2022 | 1 | PT | 470.188 | 15,8 | 0,0704 | 0,00193 |
| 2022 | 1 | OPO | 456.501 | 47,5 | 0,0000 | 0,00340 |
| 2022 | 2 | PT | 470.245 | 12,3 | 0,1989 | 0,00170 |
| 2022 | 2 | OPO | 459.874 | 33,6 | 0,0001 | 0,00285 |
| 2026 | 1 | PT | 496.219 | 8,9 | 0,4445 | 0,00141 |
| 2026 | 1 | OPO | 489.405 | 18,8 | 0,0269 | 0,00207 |
| 2026 | 2 | PT | 496.878 | 4,2 | 0,8996 | 0,00097 |
| 2026 | 2 | OPO | 489.412 | 19,3 | 0,0225 | 0,00210 |

Último dígito das contagens (>= 20 votos), V de Cramér. Percentual inteiro exato (idêntico para os dois candidatos):

| ano | turno | observado | esperado | razao |
|---|---|---|---|---|
| 2014 | 1 | 12.468 | 15.998 | 0,779 |
| 2014 | 2 | 9.212 | 11.930 | 0,772 |
| 2018 | 1 | 13.148 | 17.343 | 0,758 |
| 2018 | 2 | 10.110 | 13.196 | 0,766 |
| 2022 | 1 | 10.449 | 13.422 | 0,779 |
| 2022 | 2 | 9.848 | 12.455 | 0,791 |
| 2026 | 1 | 11.224 | 14.588 | 0,769 |
| 2026 | 2 | 10.239 | 13.134 | 0,780 |

O último dígito de Lula em 2026/T2 é uniforme (p = 0,90). O do oponente tem V de 0,0021 (p = 0,022), menor que o de 2014, 2018 e 2022; p sem correção para múltiplos testes. O percentual inteiro fica em 0,78 do esperado em todos os anos (a fórmula esperada superestima, mas a razão é constante).

### 3.9 H9: consistência

| ano | turno | secoes_bweb | secoes_votacao_secao | pareadas | pareadas_com_diferenca | soma_abs_dif_votos |
|---|---|---|---|---|---|---|
| 2014 | 1 | 428.853 | 428.850 | 428.850 | 0 | 0 |
| 2014 | 2 | 428.854 | 428.852 | 428.852 | 0 | 0 |
| 2018 | 1 | 454.446 | 454.445 | 454.445 | 1 | 66 |
| 2018 | 2 | 454.447 | 454.447 | 454.447 | 0 | 0 |
| 2022 | 1 | 472.024 | 472.024 | 472.024 | 0 | 0 |
| 2022 | 2 | 472.027 | 472.027 | 472.027 | 0 | 0 |
| 2026 | 1 | 499.206 | 499.206 | 499.206 | 0 | 0 |
| 2026 | 2 | 499.205 | 499.205 | 499.205 | 0 | 0 |


| turno | zonas_bweb | zonas_munzona | so_bweb | so_munzona | pareadas | com_diferenca | soma_abs_dif_votos | lula_bweb | lula_munzona | flavio_bweb | flavio_munzona |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6.251 | 6.292 | 0 | 41 | 6.251 | 0 | 0 | 53.879.538 | 53.879.538 | 56.104.503 | 56.104.503 |
| 2 | 6.250 | 6.292 | 0 | 42 | 6.250 | 0 | 0 | 64.256.232 | 64.256.232 | 59.826.041 | 59.826.041 |

**Divergências por seção** (todas as comparações BWeb x `votacao_secao`):

| ano | turno | uf | cd_municipio | zona | secao | comparecimento_bweb | nominais_bweb | lula_bweb | lula_votacao_secao | oponente_bweb | oponente_votacao_secao | soma_candidatos_votacao_secao |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 1 | MA | 8591 | 17 | 25 | 70 | 65 | 45 | 91 | 15 | 35 | 126 |

A única divergência é de 2018/T1, na seção 25 da zona 17 do município 8591 (MA): o BWeb registra 45 e 15 votos para os dois candidatos, com comparecimento de 70 e 65 votos nominais; `votacao_secao` registra 91 e 35, soma 126, maior que o comparecimento da seção. Os totais nacionais divulgados pelo TSE para 2018/T1 (Haddad 31.342.005, Bolsonaro 49.276.990, comparecimento 117.364.560; [fonte](https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/concluida-totalizacao-de-votos-do-1o-turno-das-eleicoes-2018)) coincidem com o BWeb (comparecimento total do BWeb: 117.364.560), e `votacao_secao` fica 46 e 20 votos acima. Portanto a diferença está em `votacao_secao` (produto gerado em 2021), não na apuração divulgada em 2018. A causa não foi investigada. Não envolve 2026. Seções presentes só no BWeb e sem voto para nenhum dos dois candidatos: 2014: 5 (até 8 comparecimentos); 2018: 1 (até 4 comparecimentos).

A totalização por município/zona de 2026 tem 41 (T1) e 42 (T2) zonas sem seção apurada no BWeb; os totais de Lula e Flávio são idênticos, logo essas zonas somam zero voto para os dois. Consistência interna dos BUs (comparecimento <= aptos, nominais + brancos + nulos = comparecimento, válidos <= comparecimento, uma urna por seção): 0 violações em todas as eleições. Esta checagem mostra que os produtos do TSE são coerentes entre si; não prova a integridade da fonte (se um BU fosse alterado na origem, todos os produtos o refletiriam).

### 3.10 H10: impacto agregado

| sentido | n_testes_com_votos | n_sobreviventes | soma_votos_sobreviventes_exigente | soma_votos_sobreviventes_pior_caso | maximo_individual_pior_caso | soma_de_todos_exigente | pct_margem_sobreviventes_pior_caso | pct_margem_soma_todos_exigente |
|---|---|---|---|---|---|---|---|---|
| PT | 19 | 1 | 38.394 | 38.394 | 1.337.198 | 213.777 | 0,87 | 4,83 |
| OPO | 1 | 1 | 122.543 | 122.543 | 122.543 | 122.543 | 2,77 | 2,77 |

Sobreviventes (Holm < 0,05):

| H | teste | sentido | p_holm | votos_max_margem | votos_max_pior_caso | pct_pior_caso | veredito |
|---|---|---|---|---|---|---|---|
| H1 | S1 Flavio/Bolsonaro votos/apto | OPO | 0,000 | 122.543 | 122.543 | 2,77% | EXCESSO DETECTADO e relevante (pior caso >= 1% da margem) |
| H2 | delta voto Lula (2022->2026) ~ delta taxa manual, T2 | PT | 0,000 | 38.394 | 38.394 | 0,87% | excesso detectavel, magnitude irrelevante (<1% da margem) |

Os tetos usam as mesmas seções e não são aditivos independentes; as colunas "soma de todos" e "máximo individual" são tetos redundantes e frouxos (o máximo individual vem do H1 sem controle do T1, comparado com 2022/T1, onde a associação era negativa). Os sentidos pró-Lula e pró-Flávio não se compensam. A soma dos sobreviventes no sentido pró-Lula é 38.394 votos (0,87% da margem).

### 3.11 Teste direto com boletins impressos

**Não executado.** Nenhum PDF ou imagem de BU foi fornecido (verificados Downloads e o diretório do projeto; capturas de tela em Imagens não foram abertas). `scripts/04_cruza_bu_impresso.py` está pronto: recebe uma planilha com zona, seção, turno e os totais do BU (transcritos ou lidos do QR code) e relata qualquer divergência, de aptos, comparecimento, votos, brancos, nulos, abertura e encerramento. Autoteste: com 3 seções reais, 0 divergências; com 1 voto alterado, 1 divergência detectada. Não há leitura de QR code por imagem; para fotos, é preciso transcrever ou decodificar o QR antes.

### 3.12 Red team: explicações mundanas testadas

| teste | ano | turno | coef_manual | ep |
|---|---|---|---|---|
| S0 + dummies de modelo de urna | 2022 | 1 | -0,00583 | 0,00166 |
| S0 + dummies de modelo de urna | 2022 | 2 | 0,01451 | 0,00180 |
| S0 + dummies de modelo de urna | 2026 | 1 | 0,07386 | 0,00251 |
| S0 + dummies de modelo de urna | 2026 | 2 | 0,06929 | 0,00243 |
| S1 Lula votos/apto (so lag proprio) | 2022 | 2 | 0,02671 | 0,00100 |
| S1 Lula votos/apto + T1 de todos os candidatos e brancos/nulos | 2022 | 2 | 0,02504 | 0,00095 |
| S1 Flavio/Bolsonaro votos/apto (so lag proprio) | 2022 | 2 | -0,00051 | 0,00075 |
| S1 Flavio/Bolsonaro votos/apto + T1 de todos os candidatos e brancos/nulos | 2022 | 2 | -0,00009 | 0,00072 |
| S1 Lula votos/apto (so lag proprio) | 2026 | 2 | 0,01915 | 0,00111 |
| S1 Lula votos/apto + T1 de todos os candidatos e brancos/nulos | 2026 | 2 | 0,01717 | 0,00103 |
| S1 Flavio/Bolsonaro votos/apto (so lag proprio) | 2026 | 2 | 0,00898 | 0,00095 |
| S1 Flavio/Bolsonaro votos/apto + T1 de todos os candidatos e brancos/nulos | 2026 | 2 | 0,02041 | 0,00095 |
| comparecimento T2 ~ taxa manual + comparecimento T1 | 2022 | 2 | 0,03090 | 0,00113 |
| comparecimento T2 ~ taxa manual + comparecimento T1 | 2026 | 2 | 0,04434 | 0,00118 |

- **Modelo da urna**: a taxa manual varia de 4,5% a 14,4% entre modelos em 2022/T2 (ver 3.3), e a associação S0 de 2026 permanece (0,069 com dummies de modelo).
- **Composição do T1** (votos dos demais candidatos, brancos e nulos): o coeficiente de Flávio sobe de 0,009 para 0,020; o de Lula cai de 0,019 para 0,017. A hipótese de que os eliminados do T1 explicam o padrão pró-Flávio não se sustenta.
- **Comparecimento**: a taxa manual prevê aumento de comparecimento no T2 dado o T1 nos dois anos (2022: 0,031; 2026: 0,044), em linha com a divisão do ganho entre os dois candidatos em 2026.

### 3.13 Régua histórica (2014, 2018, 2022, 2026)

Previsões e critério de "parecido" fixados no Adendo 1 do pré-registro: razão entre 0,8 e 1,25 para taxas e contagens; diferença < 0,02 para correlações (M5b) e < 0,005 para o V de Cramér. Padrão A: 2014, 2022 e 2026 parecidos entre si e 2018 diferente das três. B: 2014 parecido com 2018, 2022 parecido com 2026, os pares diferentes entre si. C: os quatro parecidos.

**2º turno:**

| metrica | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|
| M5a_PT | 0,00123 | 0,00172 | 0,00090 | 0,00152 |
| M5a_OPO | 0,00012 | 0,00048 | 0,00013 | 0,00018 |
| M5c | 242,09114 | 110,86548 | 49,25585 | 128,33980 |
| M7a_up | 32,29126 | 51,85363 | 45,52999 | 44,76561 |
| M7a_down | 30,18091 | 24,28891 | 25,42617 | 25,98532 |
| M7b | 1,06992 | 2,13487 | 1,79067 | 1,72273 |
| M8b_PT | 0,77219 | 0,76611 | 0,79067 | 0,77957 |
| M8b_OPO | 0,77219 | 0,76611 | 0,79067 | 0,77957 |
| M5b_PT | -0,00156 | -0,02095 | -0,02672 | -0,02409 |
| M5b_OPO | 0,00156 | 0,02095 | 0,02672 | 0,02409 |
| M8a_V_PT | 0,00152 | 0,00180 | 0,00170 | 0,00097 |
| M8a_V_OPO | 0,00371 | 0,00259 | 0,00285 | 0,00210 |

Classificação por métrica (2º turno):

| metrica | A | B | C | nenhum | sim_14_18 | sim_18_22 | sim_22_26 | sim_14_26 |
|---|---|---|---|---|---|---|---|---|
| M5a_PT | False | False | False | True | False | False | False | True |
| M5a_OPO | False | False | False | True | False | False | False | False |
| M5c | False | False | False | True | False | False | False | False |
| M7a_up | False | False | False | True | False | True | True | False |
| M7a_down | False | False | True | False | True | True | True | True |
| M7b | False | False | False | True | False | True | True | False |
| M8b_PT | False | False | True | False | True | True | True | True |
| M8b_OPO | False | False | True | False | True | True | True | True |
| M5b_PT | False | False | False | True | True | True | True | False |
| M5b_OPO | False | False | False | True | True | True | True | False |
| M8a_V_PT | False | False | True | False | True | True | True | True |
| M8a_V_OPO | False | False | True | False | True | True | True | True |

Resumo T2: A = 0, B = 0, C = 5, nenhum = 7 de 12 métricas. Resumo T1: A = 3, B = 0, C = 3, nenhum = 6.

**Trios de anos mutuamente parecidos** (todas as três comparações dentro do critério), 2º turno:

| trio | metricas_mutuamente_parecidas | metricas_que_nao_se_ajustam |
|---|---|---|
| 2014 + 2018 + 2022 | 5 de 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2018 + 2026 | 5 de 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2022 + 2026 | 5 de 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2018 + 2022 + 2026 | 9 de 12 | M5a_PT, M5a_OPO, M5c |

Nota: `M5b_OPO` e `M8b_OPO` repetem `M5b_PT` e `M8b_PT` por construção (as duas parcelas somam 1), então as 12 linhas têm 10 métricas independentes. Sem as repetições, C vale em 4 de 10, e 2/3 seria 7. A conclusão não muda.


**Veredito pelo critério fixado: nenhum dos três padrões se ajusta.** O limiar de 2/3 das métricas (8 de 12) não é atingido por A, B nem C (C chega a 5). O trio 2018, 2022 e 2026 é o mais homogêneo da tabela; as métricas em que não é homogêneo são as de cauda (comparecimento >= 90% com voto >= 90%, e comparecimento >= 95%), que são justamente as do resíduo descrito em 3.6. Esta leitura por trios é uma análise posterior, não pré-registrada. A métrica M5c (seções com comparecimento >= 95%) não tem padrão monotônico: 242 por 100 mil seções em 2014, 111 em 2018, 49 em 2022 e 128 em 2026; 2022 é o mínimo da série e 2026 fica entre 2018 e 2014.

A classificação em A/B/C depende do critério numérico fixado, que é arbitrário; por isso as razões estão na tabela.

## 4. Anomalias residuais que sobreviveram aos controles

1. **Votos de Flávio por apto x taxa manual (H1).** Coeficiente 0,0090 contra -0,0005 em 2022; teto 122.543 votos, 2,77% da margem, **no sentido favorável a Flávio**. Testado e não explicado por: composição do T1 (o coeficiente aumenta), nível de comparecimento do T1. Não testado: perfil de idade e escolaridade por seção (conjunto não disponível por seção).
2. **Variação de voto em Lula entre anos x variação da taxa manual (H2).** T2: -0,0004; T1 (placebo): -0,0110; diferença estatisticamente detectável, teto 38.394 votos (0,87%). O T1 de 2026 tem candidatos diferentes do T1 de 2022, então o placebo é imperfeito.
3. **Associação manual x Lula de 2026 (H1, sem controle do T1).** 0,074 no T1 e 0,070 no T2, contra -0,005 e 0,014 em 2022. Presente antes do 2º turno e inalterada por tamanho, comparecimento e modelo da urna. Causa não identificada. Não é específica do 2º turno, então não decorre de nada exclusivo daquele dia (a prorrogação, por exemplo). Uma causa comum aos dois turnos, seja de característica das seções ou da urna, seja de outra natureza, não é distinguível por estes dados.
4. **Seções com comparecimento >= 95% (H5).** 639 em 2026/T2; 2,5 vezes o esperado pela composição de tipo de local e tamanho; presente no T1 (1,9 vezes). Testado: tipo de local (indígena, prisional, hospital, quilombola, militar, rural), tamanho, seção nova, UF, taxa manual, atraso de fechamento, "só no T2" (35 seções, 5.737 votos válidos), numerador contra denominador. Nenhum fator isolado elimina o excesso. Não testado: cancelamento de títulos e revisão do eleitorado entre 2022 e 2026 (não há dado). Teto de efeito: 0,43% da margem.
5. **Seções novas (H6).** +0,54 p.p. de Lula no T2 dado o T1 (2018: +1,34; 2022: 0,00); robusto a interação, tamanho e comparecimento. Teto de pior caso 2,08%.

## 5. O que os dados não conseguem mostrar

- **Desvio uniforme em todas as urnas.** Todos os testes comparam seções entre si (dentro do local, entre anos, entre turnos). Um viés igual em todas as seções some nas diferenças.
- **Voto secreto.** Não há como ligar voto a eleitor; só agregados por seção.
- **Fiscais e presença de partidos.** Nenhuma variável mede presença de fiscais.
- **Votos depois das 17h.** O BWeb não tem log de votação; só horário de abertura e encerramento por seção.
- **Integridade da fonte.** BWeb, `votacao_secao` e totalização vêm do mesmo fluxo de BUs; a coerência entre eles não detecta um BU alterado na origem. Só o cruzamento com boletins impressos por fiscais e partidos faz isso, e ele não foi executado.
- **Liberação manual total.** O campo mede só eleitores com biometria cadastrada não habilitados por ela, sem denominador.
- **Perfil por seção (idade, escolaridade, renda).** Não há conjunto por seção; o perfil do eleitorado está por município e zona, que o efeito fixo de local já absorve.
- **2014 e 2018.** 2014 não tem biometria nem horários; 2018 não tem horário de recebimento nem de emissão do BU.
- **Pareamento de seções entre anos.** Perde seções remanejadas; seções novas e antigas se comportam de forma diferente (H6).

## 6. Reprodutibilidade

Estrutura: `00_preregistro.md` (previsões e adendos), `scripts/`, `dados/` (hashes e URLs), `results/fase1/` (CSVs, figuras, logs), `dossie.md`.

```bash
# 0. ambiente
python3 -m venv venv && venv/bin/pip install pandas numpy scipy pyarrow matplotlib

# 1. dados (URLs em dados/urls_origem.txt; conferir SHA-512/SHA-1 de cada zip com o arquivo .sha512/.sha1 do TSE)
#    BWeb 2022 e 2026 em bu/, 2014 e 2018 em bu_hist/; votacao_secao, detalhe e munzona em dados_tse/

# 2. preparação (um parquet por ano x turno)
venv/bin/python -I scripts/01_prepara_bweb.py bu parquet --anos 2022 2026
venv/bin/python -I scripts/01_prepara_bweb.py bu_hist parquet --anos 2014 2018
venv/bin/python -I scripts/01b_locais.py dados_tse parquet 2022 2026
venv/bin/python -I scripts/01c_modelo_urna.py dados_tse parquet 2022 2026

# 3. testes H1 a H10 e A/B/C (ordem fixa: H5, H7, H8 antes de ABC; H10 por último)
venv/bin/python -I scripts/02_executa.py parquet resultados --anos 2014 2018 2022 2026 --zips dados_tse
#    código de saída 2 = há testes não executados (results/fase1/nao_executados.csv)

# 4. dossiê
venv/bin/python -I scripts/03_monta_dossie.py resultados dados dossie.md

# 5. teste direto com boletins impressos (quando houver planilha)
venv/bin/python -I scripts/04_cruza_bu_impresso.py parquet entrada.csv divergencias.csv
```

Reprocessar 2022 e 2026 com a versão final do preparador reproduz os parquets originais célula a célula, exceto 5 seções anuladas do exterior (sentinela -1 virou vazio), que não entram nas análises. O registro de testes das duas execuções é idêntico.

## Apêndice A: registro completo dos 23 testes

| H | teste | sentido | est_2026T2 | comparador_exigente | b_comp | p_bruto_2lados | p_excesso | p_holm | p_bh | votos_max_margem | pct_margem | votos_max_pior_caso | pct_pior_caso | veredito |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | S1 T2 com lag T1, Lula% ~ taxa manual | PT | 0,00195 | 2022/T2 | 0,01620 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTADA (sem excesso, teto <1% da margem) |
| H1 | S0 sem lag, Lula% ~ taxa manual | PT | 0,06956 | 2026/T1 | 0,07413 | 0,1904 | 0,9048 | 1,000 | 1,000 | 19.670 | 0,444 | 1.337.198 | 30,184 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| H1 | S0 sem lag + controles (comparecimento, log aptos) | PT | 0,06712 | 2026/T1 | 0,06712 | 0,9991 | 0,4995 | 1,000 | 1,000 | 96.014 | 2,167 | 1.328.747 | 29,993 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| H1 | S1 reduto de Flavio (Lula T1<40%) | PT | -0,00491 | 2022/T2 | 0,01392 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTADA (sem excesso, teto <1% da margem) |
| H1 | S1 reduto de Lula (Lula T1>60%) | PT | 0,00995 | 2022/T2 | 0,01211 | 0,2889 | 0,8556 | 1,000 | 1,000 | 5.722 | 0,129 | 5.722 | 0,129 | REFUTADA (sem excesso, teto <1% da margem) |
| H1 | S1 Lula votos/apto | PT | 0,01915 | 2022/T2 | 0,02671 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTADA (sem excesso, teto <1% da margem) |
| H1 | S1 Flavio/Bolsonaro votos/apto | OPO | 0,00898 | 2022/T2 | -0,00051 | 0,0000 | 0,0000 | 0,000 | 0,000 | 122.543 | 2,766 | 122.543 | 2,766 | EXCESSO DETECTADO e relevante (pior caso >= 1% da margem) |
| H1 | S1 dose: taxa manual >= 20% vs <20% (share de Lula) | PT | -0,00039 | 2022/T2 | 0,00163 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTADA (sem excesso, teto <1% da margem) |
| H2 | delta voto Lula (T1->T2) ~ delta taxa manual, dentro do ano | PT | -0,00251 | 2022 (T1->T2) | -0,00064 | 0,2622 | 0,8689 | 1,000 | 1,000 | 1.794 | 0,040 | 1.794 | 0,040 | REFUTADA (sem excesso, teto <1% da margem) |
| H2 | delta voto Lula (2022->2026) ~ delta taxa manual, T2 | PT | -0,00044 | mesmo teste no T1 | -0,01103 | 0,0000 | 0,0000 | 0,000 | 0,000 | 38.394 | 0,867 | 38.394 | 0,867 | excesso detectavel, magnitude irrelevante (<1% da margem) |
| H4 | fecha >= 15 min apos 17h: Lula% (c/ lag, EF local) | PT | -0,00050 | mesmas secoes em 2022/T2 | 0,00005 | 0,2797 | 0,8601 | 1,000 | 1,000 | 1.333 | 0,030 | 1.333 | 0,030 | REFUTADA (sem excesso, teto <1% da margem) |
| H4 | fecha >= 15 min apos 17h: Lula% (s/ lag, EF local) | PT | -0,00030 | mesmas secoes no T1/2026 | 0,00025 | 0,6143 | 0,6928 | 1,000 | 1,000 | 5.743 | 0,130 | 5.743 | 0,130 | REFUTADA (sem excesso, teto <1% da margem) |
| H4 | fecha >= 60 min apos 17h: Lula% (c/ lag, EF local) | PT | -0,00025 | mesmas secoes em 2022/T2 | -0,00024 | 0,9914 | 0,5043 | 1,000 | 1,000 | 4.055 | 0,092 | 4.055 | 0,092 | REFUTADA (sem excesso, teto <1% da margem) |
| H4 | fecha >= 60 min apos 17h: Lula% (s/ lag, EF local) | PT | -0,00071 | mesmas secoes no T1/2026 | -0,00056 | 0,9170 | 0,5415 | 1,000 | 1,000 | 8.262 | 0,186 | 8.262 | 0,186 | REFUTADA (sem excesso, teto <1% da margem) |
| H4 | fecha >= 115 min apos 17h: Lula% (c/ lag, EF local) | PT | -0,00028 | mesmas secoes em 2022/T2 | -0,00023 | 0,9453 | 0,5273 | 1,000 | 1,000 | 3.857 | 0,087 | 3.857 | 0,087 | REFUTADA (sem excesso, teto <1% da margem) |
| H4 | fecha >= 115 min apos 17h: Lula% (s/ lag, EF local) | PT | -0,00101 | mesmas secoes no T1/2026 | -0,00090 | 0,9361 | 0,5320 | 1,000 | 1,000 | 8.130 | 0,184 | 8.130 | 0,184 | REFUTADA (sem excesso, teto <1% da margem) |
| H5 | secoes com comparecimento >=95% no T2/2026: excesso sobre o esperado pela composicao (tipo x tamanho, taxas 2022) | PT | 0,90390 | mesmo teste no T1/2026 | 0,64612 | 0,0169 | 0,0084 | 0,177 | 0,065 | 19.023 | 0,429 | 19.023 | 0,429 | REFUTADA (sem excesso, teto <1% da margem) |
| H6 | secoes novas vs antigas do mesmo local: Lula% no T2 dado o T1 | PT | 0,00536 | 2018/T2 | 0,01344 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 92.023 | 2,077 | INCONCLUSIVA (sem excesso, mas teto >=1% da margem) |
| H7 | outliers locais para cima (pro-PT), /z ajustado/ > 3, por 10 mil secoes | PT | 44,76561 | 2022/T1 | 47,57592 | 0,6068 | 0,9693 | 1,000 | 1,000 | 0 | 0,000 | 20.301 | 0,458 | REFUTADA (sem excesso, teto <1% da margem) |
| H7 | assimetria: proporcao de outliers que sao pro-PT | PT | 0,63272 | 2022/T1 | 0,64457 | 0,4787 | 0,8286 | 1,000 | 1,000 | 1.782 | 0,040 | 8.336 | 0,188 | REFUTADA (sem excesso, teto <1% da margem) |
| H8 | ultimo digito: V de Cramer de PT no T2/2026 | PT | 0,00097 | 2022/T1 | 0,00193 | 0,4503 | 0,9474 | 1,000 | 1,000 | n/d | n/d | n/d | n/d | SEM EXCESSO (teste de forma, sem conversao em votos) |
| H8 | ultimo digito: V de Cramer de OPO no T2/2026 | PT | 0,00210 | 2022/T1 | 0,00340 | 0,9620 | 0,9810 | 1,000 | 1,000 | n/d | n/d | n/d | n/d | SEM EXCESSO (teste de forma, sem conversao em votos) |
| H8 | percentual inteiro exato (PT e OPO, simetrico): obs/esperado no T2/2026 | PT | 0,77957 | 2022/T2 | 0,79067 | 0,9236 | 0,8418 | 1,000 | 1,000 | n/d | n/d | n/d | n/d | SEM EXCESSO (teste de forma, sem conversao em votos) |

## Apêndice B: não executados

| teste | motivo |
|---|---|
| BU | NaoExecutado: teste direto com boletins impressos: nenhuma foto/PDF de BU foi fornecido (nem em Downloads, nem no projeto). Envie imagens com o QR code visivel ou uma planilha zona;secao;turno;votos para o cruzamento com o BWeb. Divergencia de qualquer tamanho sera reportada. |

Fim.
