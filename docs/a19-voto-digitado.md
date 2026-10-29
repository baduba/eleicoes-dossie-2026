# A19. Ponto cego central: voto digitado x voto registrado

> Os dados públicos verificam a cadeia do registro da urna até o total. A correspondência entre o voto digitado e o voto registrado é verificada apenas por amostragem no teste de integridade. O modelo atual não possui registro conferido pelo eleitor.

## 1. O que os dados públicos não verificam

O RDV (registro digital do voto), o BU digital, o BU impresso e a totalização são gerados pelo **mesmo software da urna** (a lei prevê que a urna registre digitalmente cada voto e assine digitalmente o arquivo de votos: Lei 9.504/1997, art. 59, §§ 4º a 6º, [texto no Planalto](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm); os arquivos de saída da urna constam no leiame oficial dos arquivos de urna e no Glossário de TI do TSE). Portanto **A4, H9 e o cruzamento com o BU impresso não verificam se o voto registrado corresponde ao voto que o eleitor digitou**. Eles verificam que os artefatos da urna são coerentes entre si e com o total.

## 2. Teste de integridade de 2026

O teste de integridade é uma votação simulada, com cédulas de papel preenchidas e depois digitadas na urna, em urnas sorteadas, para comparar o voto digitado com o registrado. É a **única** verificação, no modelo atual, da correspondência entre voto digitado e voto registrado.

**O que a regra estabelece.** Pelo art. 58 da Res. TSE 23.673/2021 (conforme relatórios de auditoria externa publicados pelos TREs, [exemplo: TRE-SC 2022](https://www.tre-sc.jus.br/eleicoes/arquivos_eleicoes/eleicoes-2022/audit_ele2022_2t_relatorio_auditoria_externa)), são sorteadas 23, 35 ou 43 urnas por UF (conforme tenha até 15.000, de 15.001 a 30.000 ou mais de 30.000 seções), das quais 20, 27 ou 33 vão ao teste de integridade; o teste com biometria abrange de 5% a 10% das urnas do teste de integridade (relatórios de auditoria externa de 2024). A Res. TSE 23.758/2026 formalizou o teste de integridade com biometria em todas as UFs (indicação por resultado de busca; texto não aberto). As seções são definidas na véspera, com a participação de instituições habilitadas e, quando necessário, por sorteio (TCU); a apresentação do TRE-MG indica uma seção por zona eleitoral e ao menos uma da capital.

**Total nacional.** Aplicando a regra à contagem de seções por UF do BWeb 2026, o teste de integridade teria **648 urnas** no 1º turno (32 a 65 com biometria). **Este total foi calculado pela regra; não é um número publicado.** Confirmação em um caso: o TRE-SP informou 33 urnas no teste do 1º turno de 2026, três delas com biometria ([TRE-SP](https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-teste-de-integridade-confirma-pleno-funcionamento-das-urnas-eletronicas); lido em resultado de busca). Para 2022, a imprensa registrou 641 urnas, 58 delas com biometria (declaração atribuída ao ministro Moraes).

| UF | secoes_apuradas_bweb_2026 | urnas_no_teste_de_integridade_pela_regra |
|---|---|---|
| AC | 2.270 | 20 |
| AL | 7.101 | 20 |
| AM | 8.157 | 20 |
| AP | 1.914 | 20 |
| BA | 35.476 | 33 |
| CE | 23.765 | 27 |
| DF | 6.969 | 20 |
| ES | 9.844 | 20 |
| GO | 15.686 | 27 |
| MA | 18.093 | 27 |
| MG | 52.062 | 33 |
| MS | 7.106 | 20 |
| MT | 8.287 | 20 |
| PA | 20.827 | 27 |
| PB | 10.712 | 20 |
| PE | 21.418 | 27 |
| PI | 10.225 | 20 |
| PR | 27.142 | 27 |
| RJ | 37.675 | 33 |
| RN | 8.115 | 20 |
| RO | 4.698 | 20 |
| RR | 1.519 | 20 |
| RS | 27.547 | 27 |
| SC | 17.326 | 27 |
| SE | 5.923 | 20 |
| SP | 103.656 | 33 |
| TO | 4.384 | 20 |

**Quem acompanhou.** Segundo o TCU, equipes do tribunal acompanharam os testes nas 27 UFs no 1º turno e, nas UFs com 2º turno, também nele, com e sem biometria; o relatório consolidado será enviado ao TSE em até 30 dias corridos depois do 2º turno (processo TC 020.282/2026-5; [TCU](https://portal.tcu.gov.br/imprensa/noticias/eleicoes-2026-tcu-acompanha-testes-de-integridade-das-urnas-eletronicas)). O TSE informou 55 auditores do TCU em todo o país no 1º turno e dois equipamentos testados na sede do TSE ([TSE](https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/teste-de-integridade-no-tse-confirma-correspondencia-entre-cedulas-e-votos-registrados-nas-urnas), título lido em resultado de busca; [Portal de Prefeitura, 04/10/2026](https://portaldeprefeitura.com.br/bastidores-da-politica/tse/tse-informa-auditores-tcu-acompanham-integridade-brasil/633457/)).

**Resultado relatado.** Até a manhã de 04/10/2026, o TSE informou que nenhuma irregularidade de integridade havia sido registrada nesses procedimentos. Nenhuma divergência foi relatada nas fontes lidas.

**NÃO EXECUTADO / não localizado:** (i) o número real de urnas por UF e por turno, com e sem biometria, além do caso de São Paulo; (ii) quem escolheu ou sorteou as seções em cada UF; (iii) quem acompanhou em cada UF; (iv) os relatórios de auditoria externa publicados por TRE para 2026 (os de 2024 estão publicados no site do TSE, por exemplo [MG, 1º turno](https://www.tse.jus.br/eleicoes/eleicoes-2024-content/arquivos-teste-de-integridade/arquivos-primeiro-turno/mg-relatorio-auditoria-externa-2024-1-turno-assinado)); (v) o relatório consolidado do TCU, devido até 24/11/2026. Insumo que falta: os relatórios dos TREs e do TCU de 2026. Esta página será atualizada quando forem publicados.

## 3. Poder estatístico do teste de integridade

Probabilidade de o teste observar **ao menos uma** divergência, se uma fração das urnas do país registrasse voto diferente do digitado:

| fracao_de_urnas_alteradas | (a) n=648 (todo o teste) | (b) n=65 (so biometria, 10%) | (b) n=32 (so biometria, 5%) |
|---|---|---|---|
| 0.1% | 47,8% | 6,3% | 3,2% |
| 0.5% | 96,1% | 27,8% | 14,8% |
| 1% | 99,9% | 48,0% | 27,5% |
| 2% | 100,0% | 73,1% | 47,6% |
| 5% | 100,0% | 96,4% | 80,6% |
| 9% | 100,0% | 99,8% | 95,1% |

**Premissa (a).** A urna que registrasse voto diferente do digitado faria isso também no teste: o comportamento no teste é igual ao da eleição, e as urnas do teste são uma amostra aleatória das 499.248 urnas de votação (n = 648). **Premissa (b).** O software distingue o teste sem biometria da votação real, e o único teste indistinguível da votação real é o **com biometria**; só essas urnas contam (n = 32 a 65). As duas colunas (b) mostram o limite de 5% e o de 10%. Os cálculos supõem amostra aleatória simples sem reposição; o sorteio real (uma seção por zona, ao menos uma da capital) não é exatamente assim, então os números são aproximações. Esta seção descreve apenas a capacidade de detecção do teste; não descreve como uma alteração seria construída.

## 4. Voto impresso: contexto legal e histórico (fontes primárias)

| data | fato | fonte |
|---|---|---|
| 2009 | A Lei 12.034/2009, art. 5º, instituía o voto impresso a partir de 2014. | [STF, 2013](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=252858) |
| 06/11/2013 | O STF (ADI 4543, relatora ministra Cármen Lúcia) declarou, por unanimidade, a inconstitucionalidade do art. 5º, por comprometer o sigilo e a inviolabilidade do voto (art. 14 da Constituição), além do risco de coação. | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=252858), [voto da relatora](https://noticias.stf.jus.br/postsnoticias/integra-do-voto-da-ministra-carmen-lucia-na-adi-do-voto-impresso/) |
| 2015 | A Lei 13.165/2015 incluiu o art. 59-A na Lei 9.504/1997, exigindo o registro impresso de cada voto. | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=451785) |
| 06/06/2018 | Liminar do STF suspendeu a regra (ADI 5889, proposta pela PGR). | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=380571) |
| 14/09/2020 | O STF confirmou a liminar por unanimidade e declarou inconstitucional o art. 59-A e seu parágrafo único (relator ministro Gilmar Mendes): a impressão do registro do voto "põe em risco sigilo e liberdade de voto". O texto compilado da lei indica: "Declarado inconstitucional pela ADI nº 5.889". | [STF](https://portal.stf.jus.br/noticias/verNoticiaDetalhe.asp?idConteudo=451785), [Lei 9.504 compilada](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm) |
| 05 e 06/08/2021 | Na Câmara, a comissão especial da PEC 135/2019 (voto impresso obrigatório) rejeitou o substitutivo por 23 a 11 e recomendou ao Plenário a rejeição da PEC por 22 a 11. | [Câmara](https://www.camara.leg.br/noticias/790507-comissao-especial-rejeita-por-23-a-11-o-voto-impresso-obrigatorio/), [Câmara](https://www.camara.leg.br/noticias/791064-comissao-recomenda-por-22-a-11-a-rejeicao-da-pec-do-voto-impresso/) |

O resultado da votação em Plenário não foi confirmado nas fontes primárias lidas; verificar na tramitação da PEC 135/2019 no portal da Câmara.

**Duas coisas diferentes.** (1) **Registro conferido pelo eleitor que fica na urna:** a urna imprimiria o voto, o eleitor o conferiria e o papel ficaria depositado na urna, sem sair com ele. Foi o que previram o art. 5º da Lei 12.034/2009 e o art. 59-A da Lei 9.504/1997; ambos foram declarados inconstitucionais. (2) **Comprovante entregue ao eleitor:** um papel que sai da seção com o eleitor, que provaria em quem ele votou. A lei vigente prevê o registro digital assinado de cada voto (art. 59, §§ 4º a 6º) e a urna que "contabilizará cada voto, assegurando-lhe o sigilo e inviolabilidade" (art. 61), e não prevê comprovante em papel ao eleitor. O motivo legal apontado pelo STF para vedar o registro impresso é o **sigilo e a liberdade do voto** (risco de coação e de prova do voto; inclusive, na ADI 5889, a regra de o processo depender da conferência pelo eleitor). A leitura de que o motivo do comprovante é impedir prova de voto, e portanto compra de voto, decorre dessa fundamentação do STF; ela é uma inferência desta página, não um trecho citado.

## 5. Recontagem

Não existe cédula física de votação no modelo atual; portanto não há "recontagem de papel". A "recontagem" possível é **reprocessar o RDV e os BUs** e compará-los com a totalização. Isso foi feito em [A4](resultados-fase2.md) (RDV recontado contra o BU, Lula, oponente, brancos e total, em 14.067 seções de 2026) e em H9 (BWeb contra `votacao_secao` e totalização por zona e município), sem divergências em 2026. **Esse reprocessamento usa arquivos gerados pela própria urna** e, por isso, não mede a correspondência entre o voto digitado e o registrado (ver seção 1).

## 6. Conclusão desta seção

Os dados públicos verificam a cadeia do registro da urna até o total. A correspondência entre o voto digitado e o voto registrado é verificada apenas por amostragem no teste de integridade. O modelo atual não possui registro conferido pelo eleitor.
