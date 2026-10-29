# Régua histórica (2014, 2018, 2022, 2026)

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
