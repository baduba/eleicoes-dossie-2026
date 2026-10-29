# Auditoria independente reproduzível: 2º turno presidencial de 2026

Esta é uma **auditoria independente**. Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou. Foi construída para que qualquer perito, de qualquer lado, repita cada número e conteste o que discordar.

## O que foi feito
Análise estatística dos dados oficiais do TSE por seção (BWeb de 2014, 2018, 2022 e 2026, com hash conferido), mais os arquivos de urna (BU, RDV, assinatura e log) de uma amostra de 14.067 seções do 2º turno de 2026 e as mesmas seções em 2022 como placebo. Previsões foram registradas antes de cada bloco de análises ([Pré-registro](preregistro.md)); todo teste tem placebo e é simétrico; resultados nulos têm o mesmo destaque que os positivos.

## Resumo dos resultados (números sem adjetivos)
- **Totais e consistência:** Lula 64.256.232, Flávio 59.826.041, margem 4.430.191. O BWeb coincide com `votacao_secao` e com a totalização por zona em 2026.
- **Cadeia da urna (A4):** em 14.067 seções de 27 UFs, o BU digital coincide com o BWeb, o RDV recontado coincide com o BU e os hashes de BU, RDV, imagem e log constam na lista assinada pela urna: 0 divergências. A assinatura criptográfica em si **não foi verificada** (falta a especificação do TSE).
- **Relatório original:** a tabela de fechamento (339.593 seções entre 17h01 e 17h15), as 8,6 milhões de liberações manuais (8.632.488) e os percentuais da Bahia reproduzem; as conclusões não se sustentam ([página](relatorio-original.md)).
- **Votos depois das 17h (A5):** estimativa a partir dos logs de 23.094 votos em todo o país (IC95 16.895 a 29.704), 0,52% da margem; muitas das seções que fecharam tarde ficaram abertas sem registrar voto depois das 17h.
- **Liberação manual:** caiu 14% de 2022 para 2026; a associação com o voto em Lula existe nos dois turnos de 2026 e não é específica do 2º turno.
- **Curva de apuração, conversão e zero voto (A1, A2, A3, A11, A12, A13, A14):** a curva real e seus trechos lineares ficam dentro da faixa das ordens geográficas simuladas; nenhuma conversão do oponente para o PT é necessária para explicar o resultado nacional; o "109 seções com zero voto" não reproduz (são 106 no 2º turno; 143 em 2022, 328 em 2018); às 19h34 só 7,8% dos BUs tinham sido recebidos, não 70%.
- **Pelos critérios pré-registrados**, A1, A2 e A3 saem como "excesso detectado" e A12 como "excesso detectável, magnitude irrelevante". Cada uma tem **ressalva de desenho** documentada (o controle posterior mostrou que o desenho media outra coisa: geografia de chegada, espelho entre 2022 e 2026, coeficientes negativos em todos os anos, estimador inadequado nos placebos). As linhas foram mantidas como saíram; ver [Resultados da Fase 2](resultados-fase2.md) e [Questões em aberto](residuos.md).
- **Impacto agregado:** a soma dos tetos dos testes com excesso detectado, sem as linhas com ressalva de desenho, é 38.394 votos pró-Lula e 122.543 pró-Flávio; com todas as linhas, 9.425.488 e 122.543; a diferença vem da linha A3, cujo teto de pior caso não tem interpretação causal (coeficientes ecológicos negativos em todos os anos; ver ressalva). A margem é 4.430.191.

## O que não foi testado
Ver [Questões em aberto](residuos.md), [Pontos cegos](pontos-cegos.md) e a lista de **NÃO EXECUTADO**: cruzamento com boletins impressos (sem insumo), assinatura criptográfica da urna, curva de divulgação do site Resultados, perfil de comparecimento de 2026/2º turno, 2014 na curva de apuração, as "472 urnas" do vídeo.

## Autoria
[a preencher por Julio antes da publicação]
