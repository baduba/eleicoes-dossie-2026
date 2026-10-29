# Questões em aberto (resíduos)

> **Itens que os testes não conseguiram explicar nem confirmar. Não constituem evidência de manipulação; estão aqui para transparência e para investigação futura.**

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
- **Veredito pelo critério pré-registrado:** EXCESSO DETECTADO (teste de forma, sem conversao em votos) (ressalva de desenho: o envelope B (permutacao dentro da UF) e rejeitado nos quatro anos; a partir de 10% das secoes o desvio de 2026/T2 fica abaixo dos placebos (analise posterior))
- **Direção do efeito:** n/a
- **Estimativa central:** não convertível em votos (teste de forma)
- **Teto de pior caso:** n/d votos (n/d% da margem)
- **Explicações mundanas testadas:** o envelope é rejeitado em todos os anos; a partir de 10% das seções 2026/T2 fica abaixo dos placebos
- **Não testadas:** snapshots do site Resultados
- **O que resolveria:** série de divulgação com horário
- **Causa:** não identificada.

## A2: Frequência de seções em que o oponente perde votos absolutos (11,8% das seções; teste de forma)

- **Linha do registro:** oponente perde votos absolutos do T1 ao T2 em secao com comparecimento estavel ou crescente (% das secoes)
- **Veredito pelo critério pré-registrado:** EXCESSO DETECTADO (teste de forma, sem conversao em votos) (ressalva de desenho: o placebo por papel (oponente) e inadequado: em 2022 o PT, lider do T1, perdeu votos em 12,6% das secoes, espelho dos 11,8% do oponente em 2026 (analise posterior))
- **Direção do efeito:** n/a
- **Estimativa central:** não convertível em votos (teste de forma)
- **Teto de pior caso:** n/d votos (n/d% da margem)
- **Explicações mundanas testadas:** espelho: em 2022 o PT perdeu em 12,6%; por faixa de terceiros/candidato as frequências são parecidas
- **Não testadas:** por que o líder do 1º turno perde votos absolutos onde há poucos terceiros
- **O que resolveria:** pesquisa individual (painel)
- **Causa:** não identificada.

## A3: Coeficiente ecológico oponente no T1 → PT no T2 (2026 é o menos negativo; com EF de município, o mais negativo)

- **Linha do registro:** ecologica: fracao de eleitores do oponente no T1 que aparece como voto no PT no T2
- **Veredito pelo critério pré-registrado:** EXCESSO DETECTADO e relevante (pior caso >= 1% da margem) (ressalva de desenho: coeficientes negativos em todos os anos (nao medem conversao); com EF de municipio o coeficiente de 2026 e o mais negativo (analise posterior))
- **Direção do efeito:** a favor de Lula (diferença entre anos)
- **Estimativa central:** 1.276.379 votos de margem (IC95 635.578 a 1.917.180), contra o placebo mais exigente (2022)
- **Teto de pior caso:** 9.385.617 votos (211,86% da margem)
- **Explicações mundanas testadas:** efeito fixo de município; contabilidade por identidade
- **Não testadas:** conversão individual (sigilo)
- **O que resolveria:** painel de eleitores ou dados de pesquisa pós-eleitoral
- **Causa:** não identificada.

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
- **Veredito pelo critério pré-registrado:** excesso detectavel, magnitude irrelevante (<1% da margem) (ressalva de desenho: os placebos tem razao observado/esperado abaixo de 1 porque o estimador de p pelo T1 e inadequado onde ha terceiros relevantes no T1 (2018, 2014); o teste direto observado contra esperado em 2026 (z=1,33) nao e significativo (analise posterior))
- **Direção do efeito:** a favor de Lula
- **Estimativa central:** 566 votos de margem (IC95 216 a 916), contra o placebo mais exigente (2022)
- **Teto de pior caso:** 1.478 votos (0,03% da margem)
- **Explicações mundanas testadas:** esperado pelo voto da seção no T1 e pelos vizinhos do mesmo local
- **Não testadas:** n/a
- **O que resolveria:** n/a
- **Causa:** não identificada.

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

## Soma agregada

| sentido | itens_com_votos | soma_central | ic95 | soma_pior_caso | pct_margem_central | pct_margem_pior_caso |
|---|---|---|---|---|---|---|
| pró-Lula | 10 | -4.114.519 | -4.993.930 a -3.235.109 | 11.035.315 | -92,87% | 249,09% |
| pró-Flávio | 1 | 101.285 | 75.956 a 126.614 | 122.543 | 2,29% | 2,77% |

O intervalo da soma supõe independência entre os itens (aproximação declarada; os itens usam as mesmas seções, então o intervalo é aproximado). Os sentidos pró-Lula e pró-Flávio não se compensam. Itens de forma, sem conversão em votos, não entram na soma. Nenhum item, isolado ou somado, alcança a margem de 4.430.191 votos.

## Itens sem linha no registro

- **Comparecimento de idosos (A9):** o comparecimento de eleitores acima de 80 anos (voto facultativo) cresce mais que os aptos da faixa entre 2022 e 2026 no 1º turno. Não convertível em votos; causa não identificada; resolveria o perfil de 2026/2º turno e o histórico de cancelamentos de títulos.
- **Chegada dos BUs de 25/10/2026:** 99,6% dos BUs chegaram ao TSE depois das 19h, enquanto 98,2% das seções tinham fechado até 15 minutos depois das 17h. Explicado pela pausa documentada pela imprensa; a fonte oficial não foi aberta.
