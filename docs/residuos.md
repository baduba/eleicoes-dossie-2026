# Questões em aberto (resíduos)

> **Itens que os testes não conseguiram explicar nem confirmar. Não são evidência de nada, nem de um lado nem do outro: são lacunas que só dados novos fecham, e estão aqui para transparência e para investigação futura.**

Entram nesta página todo resultado classificado como inconclusivo, "excesso detectável" ou "excesso detectado" e todo resíduo sem causa identificada. As estimativas centrais e os intervalos de 95% usam aproximação normal sobre o erro padrão do contraste contra o placebo mais exigente (não são bootstrap nem bayesianos). O **teto de pior caso** usa o placebo mais frouxo. Nenhuma probabilidade é atribuída a hipóteses sobre o processo; só aparecem quantidades medidas (votos em excesso, diferença entre anos). Margem oficial: 4.430.191 votos.

## H1: Associação entre a taxa de liberação manual e votos de Flávio por apto no 2º turno, além do 1º turno

- **Linha do registro:** S1 Flavio/Bolsonaro votos/apto
- **Veredito pelo critério pré-registrado:** EXCESSO DETECTADO e relevante (pior caso >= 1% da margem)
- **Direção do efeito:** a favor de Flávio
- **Estimativa central:** 101.285 votos de margem (IC95 75.956 a 126.614), contra o placebo mais exigente (2022/T2)
- **Teto de pior caso:** 122.543 votos (2,77% da margem)
- **Explicações mundanas testadas:** efeito do modelo de urna (A10); composição do T1 com todos os candidatos e brancos/nulos (o coeficiente aumenta); comparecimento
- **Não testadas:** idade e escolaridade por seção; perfil do eleitor que precisa de liberação manual
- **O que resolveria:** perfil por seção (idade, escolaridade) ou o registro das folhas de votação
- **Causa:** não identificada.

## H5: Seções com comparecimento ≥95%: 2,5 vezes o esperado pela composição de tipo de local e tamanho; presente já no 1º turno

- **Linha do registro:** secoes com comparecimento >=95% no T2/2026: excesso sobre o esperado pela composicao (tipo x tamanho, taxas 2022)
- **Veredito pelo critério pré-registrado:** REFUTADA (sem excesso, teto <1% da margem)
- **Direção do efeito:** comparecimento (efeito possível em qualquer direção; teto calculado como se todos os votos extras fossem do PT)
- **Estimativa central:** 11.266 votos de margem (IC95 2.023 a 20.508), contra o placebo mais exigente (mesmo teste no T1/2026)
- **Teto de pior caso:** 19.023 votos (0,43% da margem)
- **Explicações mundanas testadas:** tipo de local, tamanho, seção nova, UF, taxa manual, atraso de fechamento, numerador contra denominador (nas seções antigas o numerador sobe 6%)
- **Não testadas:** cancelamento de títulos e revisão do eleitorado entre 2022 e 2026; composição etária por seção (o comparecimento de idosos cresce mais que os aptos, A9)
- **O que resolveria:** cadastro por seção antes e depois da revisão do eleitorado
- **Causa:** não identificada.

## H6: Seções novas têm +0,54 p.p. de Lula no T2 dado o T1 (2018: +1,34; 2022: 0)

- **Linha do registro:** secoes novas vs antigas do mesmo local: Lula% no T2 dado o T1
- **Veredito pelo critério pré-registrado:** INCONCLUSIVA (sem excesso, mas teto >=1% da margem)
- **Direção do efeito:** a favor de Lula
- **Estimativa central:** -130.811 votos de margem (IC95 -140.934 a -120.687), contra o placebo mais exigente (2018/T2)
- **Teto de pior caso:** 92.023 votos (2,08% da margem)
- **Explicações mundanas testadas:** interação com o T1, tamanho e comparecimento (o coeficiente é estável)
- **Não testadas:** composição por idade e renda; origem dos eleitores transferidos para as seções novas
- **O que resolveria:** histórico de remanejamento de eleitores por seção
- **Causa:** não identificada.

## H1: Associação entre taxa de liberação manual e voto em Lula dentro do mesmo local, igual no 1º e no 2º turno de 2026 (0,07) e maior que em 2022

- **Linha do registro:** S0 sem lag, Lula% ~ taxa manual
- **Veredito pelo critério pré-registrado:** INCONCLUSIVA (sem excesso, mas teto >=1% da margem)
- **Direção do efeito:** a favor de Lula (associação, não efeito)
- **Estimativa central:** -76.711 votos de margem (IC95 -191.548 a 38.125), contra o placebo mais exigente (2026/T1)
- **Teto de pior caso:** 1.337.198 votos (30,18% da margem)
- **Explicações mundanas testadas:** controles de comparecimento, tamanho e modelo de urna: a associação permanece
- **Não testadas:** perfil por seção
- **O que resolveria:** perfil por seção; modelo causal com instrumento para falha de biometria
- **Causa:** não identificada.

## H2: Variação do voto em Lula entre anos contra variação da taxa manual: T2 contra T1 como placebo imperfeito

- **Linha do registro:** delta voto Lula (2022->2026) ~ delta taxa manual, T2
- **Veredito pelo critério pré-registrado:** excesso detectavel, magnitude irrelevante (<1% da margem)
- **Direção do efeito:** a favor de Lula
- **Estimativa central:** 30.332 votos de margem (IC95 20.726 a 39.938), contra o placebo mais exigente (mesmo teste no T1)
- **Teto de pior caso:** 38.394 votos (0,87% da margem)
- **Explicações mundanas testadas:** municípios com biometria nos dois anos; o T1 de 2026 tem candidatos diferentes do de 2022
- **Não testadas:** n/a
- **O que resolveria:** placebo com candidatos comparáveis
- **Causa:** não identificada.

## A1: Desvio da curva de apuração contra a permutação dentro da UF (teste de forma; sem conversão em votos)

- **Linha do registro:** curva de apuracao: desvio maximo da curva real contra permutacao dentro da UF (p.p. do PT)
- **RESSALVA DE DESENHO (leia primeiro):** o desenho pré-registrado desta linha produz o rótulo de excesso sem manipulação (demonstração e correção em [Resultados da Fase 2](resultados-fase2.md)). O rótulo abaixo **não indica manipulação**.
- **Pré-registrado (mantido):** EXCESSO DETECTADO (teste de forma, sem conversao em votos), com a ressalva de desenho acima (o envelope B (permutacao dentro da UF) e rejeitado nos quatro anos; a partir de 10% das secoes o desvio de 2026/T2 fica abaixo dos placebos (analise posterior))
- **Corrigido (pós-registro):** SEM EXCESSO (teste de forma, sem conversao em votos)
- **Direção do efeito:** n/a
- **Estimativa em votos:** sem interpretação causal nesta linha; valores no Apêndice "Agregado sem interpretação causal" de Resultados da Fase 2.
- **Explicações mundanas testadas:** o envelope é rejeitado em todos os anos; a partir de 10% das seções 2026/T2 fica abaixo dos placebos
- **Não testadas:** snapshots do site Resultados
- **O que resolveria:** série de divulgação com horário
- **Causa:** o desenho do teste (ver ressalva); não há resíduo a explicar nesta linha.

## A2: Frequência de seções em que o oponente perde votos absolutos (11,8% das seções; teste de forma)

- **Linha do registro:** oponente perde votos absolutos do T1 ao T2 em secao com comparecimento estavel ou crescente (% das secoes)
- **RESSALVA DE DESENHO (leia primeiro):** o desenho pré-registrado desta linha produz o rótulo de excesso sem manipulação (demonstração e correção em [Resultados da Fase 2](resultados-fase2.md)). O rótulo abaixo **não indica manipulação**.
- **Pré-registrado (mantido):** EXCESSO DETECTADO (teste de forma, sem conversao em votos), com a ressalva de desenho acima (o placebo por papel (oponente) e inadequado: em 2022 o PT, lider do T1, perdeu votos em 12,6% das secoes, espelho dos 11,8% do oponente em 2026 (analise posterior))
- **Corrigido (pós-registro):** SEM EXCESSO (teste de forma, sem conversao em votos)
- **Direção do efeito:** n/a
- **Estimativa em votos:** sem interpretação causal nesta linha; valores no Apêndice "Agregado sem interpretação causal" de Resultados da Fase 2.
- **Explicações mundanas testadas:** espelho: em 2022 o PT perdeu em 12,6%; por faixa de terceiros/candidato as frequências são parecidas
- **Não testadas:** por que o líder do 1º turno perde votos absolutos onde há poucos terceiros
- **O que resolveria:** pesquisa individual (painel)
- **Causa:** o desenho do teste (ver ressalva); não há resíduo a explicar nesta linha.

## A3: Coeficiente ecológico oponente no T1 → PT no T2 (2026 é o menos negativo; com EF de município, o mais negativo)

- **Linha do registro:** ecologica: fracao de eleitores do oponente no T1 que aparece como voto no PT no T2
- **RESSALVA DE DESENHO (leia primeiro):** o desenho pré-registrado desta linha produz o rótulo de excesso sem manipulação (demonstração e correção em [Resultados da Fase 2](resultados-fase2.md)). O rótulo abaixo **não indica manipulação**.
- **Pré-registrado (mantido):** EXCESSO DETECTADO e relevante (pior caso >= 1% da margem), com a ressalva de desenho acima (coeficientes negativos em todos os anos (nao medem conversao); com EF de municipio o coeficiente de 2026 e o mais negativo (analise posterior))
- **Corrigido (pós-registro):** REFUTADA (sem excesso, teto <1% da margem)
- **Direção do efeito:** a favor de Lula (diferença entre anos)
- **Estimativa em votos:** sem interpretação causal nesta linha; valores no Apêndice "Agregado sem interpretação causal" de Resultados da Fase 2.
- **Explicações mundanas testadas:** efeito fixo de município; contabilidade por identidade
- **Não testadas:** conversão individual (sigilo)
- **O que resolveria:** painel de eleitores ou dados de pesquisa pós-eleitoral
- **Causa:** o desenho do teste (ver ressalva); não há resíduo a explicar nesta linha.

## A10: Modelo de urna novo (UE2022) sem equivalente em 2022, teto de pior caso acima de 1% da margem por ser pouco preciso

- **Linha do registro:** modelo de urna UE2022 contra UE2020, mesmo local: Lula% no T2 dado o T1
- **Veredito pelo critério pré-registrado:** INCONCLUSIVA (sem excesso, mas teto >=1% da margem)
- **Direção do efeito:** n/a
- **Estimativa central:** 56.317 votos de margem (IC95 -40.780 a 153.414), contra o placebo mais exigente (2026/T1 (sem lag, mesmas secoes))
- **Teto de pior caso:** 137.809 votos (3,11% da margem)
- **Explicações mundanas testadas:** dentro do mesmo local, o coeficiente é 0,0000
- **Não testadas:** n/a
- **O que resolveria:** mais seções por modelo
- **Causa:** não identificada.

## A11: Coeficiente ecológico do bloco que apoiou Flávio para votos do PT, contra os placebos

- **Linha do registro:** bloco pro-Flavio no T1 (Zema, Caiado, Cury, Clariana) -> votos do PT no T2 por apto, EF de municipio
- **Veredito pelo critério pré-registrado:** REFUTADA (sem excesso, teto <1% da margem) (ressalva de desenho: o desenho compara blocos de composicao diferente entre anos; coeficientes ecologicos nao medem conversao individual)
- **Direção do efeito:** ver A11
- **Estimativa central:** -5.185.109 votos de margem (IC95 -5.750.811 a -4.619.407), contra o placebo mais exigente (2018: maior terceiro (terc1_n12))
- **Teto de pior caso:** 0 votos (0,00% da margem)
- **Explicações mundanas testadas:** efeito fixo de município; Goodman restrito
- **Não testadas:** composição dos blocos e apoios sem fonte (esquerda, Clariana, Rui Costa Pimenta)
- **O que resolveria:** pesquisa pós-eleitoral
- **Causa:** não identificada.

## A12: Seções com zero voto para o oponente (razão observado/esperado)

- **Linha do registro:** secoes com zero voto para o oponente no T2: razao observado/esperado (p do T1)
- **RESSALVA DE DESENHO (leia primeiro):** o desenho pré-registrado desta linha produz o rótulo de excesso sem manipulação (demonstração e correção em [Resultados da Fase 2](resultados-fase2.md)). O rótulo abaixo **não indica manipulação**.
- **Pré-registrado (mantido):** excesso detectavel, magnitude irrelevante (<1% da margem), com a ressalva de desenho acima (os placebos tem razao observado/esperado abaixo de 1 porque o estimador de p pelo T1 e inadequado onde ha terceiros relevantes no T1 (2018, 2014); o teste direto observado contra esperado em 2026 (z=1,33) nao e significativo (analise posterior))
- **Corrigido (pós-registro):** REFUTADA (sem excesso, teto <1% da margem)
- **Direção do efeito:** a favor de Lula
- **Estimativa em votos:** sem interpretação causal nesta linha; valores no Apêndice "Agregado sem interpretação causal" de Resultados da Fase 2.
- **Explicações mundanas testadas:** esperado pelo voto da seção no T1 e pelos vizinhos do mesmo local
- **Não testadas:** n/a
- **O que resolveria:** n/a
- **Causa:** o desenho do teste (ver ressalva); não há resíduo a explicar nesta linha.

## A5: Associação entre votos depois do horário nominal e Lula% no mesmo local

- **Linha do registro:** share de votos depois do horario nominal (log) e Lula% no T2 dado o T1, EF de local
- **Veredito pelo critério pré-registrado:** REFUTADA (sem excesso, teto <1% da margem)
- **Direção do efeito:** ver A5
- **Estimativa central:** 1.585 votos de margem (IC95 -1.254 a 4.424), contra o placebo mais exigente (2022/T2 (mesmas secoes))
- **Teto de pior caso:** 3.968 votos (0,09% da margem)
- **Explicações mundanas testadas:** mesmo teste nas mesmas seções em 2022
- **Não testadas:** seções sem arquivo de urna
- **O que resolveria:** log de todas as seções
- **Causa:** não identificada.

## A15: Modelo de urna UE2009/UE2010 em 2022 contra UE2020

- **Linha do registro:** 2022: UE2009 contra UE2020, mesmo local: Lula% no T2 dado o T1
- **Veredito pelo critério pré-registrado:** REFUTADA (sem excesso, teto <1% da margem)
- **Direção do efeito:** a favor de Lula
- **Estimativa central:** -98.333 votos de margem (IC95 -239.095 a 42.429), contra o placebo mais exigente (2022/T1 (corte transversal))
- **Teto de pior caso:** 19.807 votos (0,45% da margem)
- **Explicações mundanas testadas:** o efeito sem controle do T1 é composição (também aparece no T1); com o T1, é nulo
- **Não testadas:** n/a
- **O que resolveria:** n/a
- **Causa:** não identificada.

## A1 corrigido, 1º turno de 2026: trecho final da curva fora do envelope

- **O que se observa:** a curva do 1º turno fica fora do envelope do nulo corrigido por 240 pontos consecutivos (dos 76% aos 100% das seções, das 19h18 às 22h28 de 04/10/2026). O alvo pré-registrado do A1 é o 2º turno; esta linha é análise posterior.
- **Direção do efeito:** participação de Lula abaixo da mediana do nulo, com desvio decrescente até zero; maior desvio antes da janela de 19h às 20h.
- **Estimativa em votos:** não convertível em votos (teste de forma; a soma final é idêntica em qualquer ordem).
- **Explicações mundanas testadas:** coincidência com a janela do congestionamento de 19h às 20h: parcial (91 dos 241 pontos; a corrida começa na janela e continua depois); composição por UF: compatível, não demonstrada. Ver [A18](a18-alteracao-no-meio.md).
- **Não testadas:** ordem dos municípios dentro de cada UF por porte e por perfil de voto.
- **O que resolveria:** o log de recepção do Sistot (não público) e a ordem real de transmissão por município.
- **Causa:** não identificada.

## Soma agregada: quantos votos, todos os resíduos juntos?

> **Unidade: votos de margem** (variação da diferença Lula menos Flávio; a troca de um voto muda a margem em 2; definição em [Metodologia](metodologia.md)). Todos os números abaixo devem ser lidos contra a margem de 4.430.191. Para inverter o resultado, o conjunto dos efeitos **pró-Lula** teria de somar ao menos esse valor; efeitos pró-Flávio andam no sentido contrário e não entram nessa conta.

| soma | pró-Lula (votos de margem) | % da margem (pró-Lula) | pró-Flávio (votos de margem) | % da margem (pró-Flávio) |
|---|---|---|---|---|
| **(1) Excesso medido: soma das estimativas centrais positivas dos itens desta página** (contra o placebo mais exigente; as negativas não compensam) | **99.499** | **2,25%** | **101.285** | **2,29%** |
| (2) Tetos de pior caso dos itens desta página | 1.648.221 (teto de pior caso, não estimativa) | 37,2% (teto de pior caso, não estimativa) | 122.543 (teto de pior caso, não estimativa) | 2,8% (teto de pior caso, não estimativa) |
| (3) Idem (2), sem o maior item isolado (teto dominado pela imprecisão, ver abaixo) | 311.023 (teto de pior caso, não estimativa) | 7,0% (teto de pior caso, não estimativa) | 122.543 (teto de pior caso, não estimativa) | 2,8% (teto de pior caso, não estimativa) |

**Leitura.** A linha (1) é o que os dados mostram de excesso: cerca de 99.499 votos de margem pró-Lula e 101.285 pró-Flávio, ou seja, 2,2% e 2,3% da margem. As linhas (2) e (3) são **tetos de pior caso, não estimativas**: usam sempre o placebo mais frouxo e somam como se tudo fosse independente. Em (2), o item de maior teto (1.337.198 votos de margem) é uma especificação sem controle do 1º turno cujo teto vem da **imprecisão** do teste (o veredito é inconclusivo, não de excesso); sem ele, o conjunto cai para 7,0% da margem. Nenhuma soma alcança 4.430.191. O limite vale para o que os testes medem; o que está fora da medição (os elos não publicados) segue aberto.

O que isso **não** mede: uma alteração de votos coerente em todos os arquivos publicados, que estes testes não conseguem enxergar (ver [A18](a18-alteracao-no-meio.md) e [A19](a19-voto-digitado.md)). Também fica de fora o agregado de linhas com ressalva de desenho, que não tem interpretação causal (Apêndice B de [Resultados da Fase 2](resultados-fase2.md)). A soma ingênua de todas as linhas do registro está só no apêndice abaixo.

## Itens sem linha no registro

- **Comparecimento de idosos (A9):** o comparecimento de eleitores acima de 80 anos (voto facultativo) cresce mais que os aptos da faixa entre 2022 e 2026 no 1º turno. Não convertível em votos; causa não identificada; resolveria o perfil de 2026/2º turno e o histórico de cancelamentos de títulos.
- **Chegada dos BUs de 25/10/2026:** 99,6% dos BUs chegaram ao TSE depois das 19h, enquanto 98,2% das seções tinham fechado até 15 minutos depois das 17h. Explicado pela pausa documentada pela imprensa; a fonte oficial não foi aberta.

## Apêndice: Soma ingênua com dupla contagem, sem interpretação

> **Esta soma não mede votos alterados.** Ela soma os tetos de pior caso de **todas** as 27 linhas pró-Lula do registro (sem as quatro com ressalva de desenho) que têm conversão em votos, contando várias vezes as mesmas seções e as mesmas especificações (por exemplo, o teste de liberação manual em várias especificações e o de fechamento tardio em seis). Unidade: votos de margem. Teto de pior caso, não estimativa.

| soma | pró-Lula (votos de margem) | % da margem | pró-Flávio (votos de margem) |
|---|---|---|---|
| Soma ingênua com dupla contagem, sem interpretação (teto de pior caso, não estimativa) | 3.092.826 | 69,8% | 122.543 |

Mesmo com a dupla contagem, a soma não alcança 4.430.191 votos de margem.
