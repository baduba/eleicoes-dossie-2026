# Auditoria independente reproduzível: 2º turno presidencial de 2026

Esta é uma **auditoria independente**. Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou. Foi construída para que qualquer perito, de qualquer lado, repita cada número e conteste o que discordar.

> **Versão preliminar (v0.9).** A v1.0 sai depois do relatório consolidado do TCU sobre os testes de integridade (prazo até 24/11/2026), da verificação da assinatura criptográfica e de um lote inicial de boletins impressos conferidos ([como enviar](boletins-impressos.md)).

## O que foi feito
Análise estatística dos dados oficiais do TSE por seção (BWeb de 2014, 2018, 2022 e 2026, com hash conferido), mais os arquivos de urna (BU, RDV, assinatura e log) de uma amostra de 14.067 seções do 2º turno de 2026 e as mesmas seções em 2022 como placebo. Previsões foram registradas antes de cada bloco de análises ([Pré-registro](preregistro.md)); todo teste tem placebo e é simétrico; resultados nulos têm o mesmo destaque que os positivos.

## Resumo dos resultados (números sem adjetivos)
- **Totais e consistência:** Lula 64.256.232, Flávio 59.826.041, margem 4.430.191. O BWeb coincide com `votacao_secao` e com a totalização por zona em 2026.
- **Cadeia da urna (A4):** em 14.067 seções de 27 UFs, o BU digital coincide com o BWeb, o RDV recontado coincide com o BU e os hashes de BU, RDV, imagem e log constam na lista assinada pela urna: 0 divergências. **Isso verifica consistência entre arquivos que o TSE publica e não exclui uma alteração coerente feita antes da publicação** ([A18](a18-alteracao-no-meio.md)). A assinatura criptográfica em si **não foi verificada** (0% das seções; NÃO EXECUTADO PARCIAL: falta a chave oficial acessível).
- **Alteração no meio e voto digitado x registrado (A18, A19):** os atrasos documentados (1 hora no 1º turno; recebimento retido até as 19h no 2º) foram testados pela janela de relógio contra placebos, sem excesso detectado, mas esses testes não excluem uma alteração coerente. A correspondência entre voto digitado e voto registrado só é verificada por amostragem no teste de integridade, e o modelo atual não possui registro conferido pelo eleitor ([A19](a19-voto-digitado.md)). Fotos de boletins impressos podem ser enviadas por qualquer pessoa ([como enviar](boletins-impressos.md)).
- **Relatório original:** a tabela de fechamento (339.593 seções entre 17h01 e 17h15), as 8,6 milhões de liberações manuais (8.632.488) e os percentuais da Bahia reproduzem; as conclusões não se sustentam ([página](relatorio-original.md)).
- **Votos depois das 17h (A5):** estimativa a partir dos logs de 23.094 votos em todo o país (IC95 16.895 a 29.704), 0,52% da margem; muitas das seções que fecharam tarde ficaram abertas sem registrar voto depois das 17h.
- **Liberação manual:** caiu 14% de 2022 para 2026; a associação com o voto em Lula existe nos dois turnos de 2026 e não é específica do 2º turno.
- **Curva de apuração, conversão e zero voto (A1, A2, A3, A11, A12, A13, A14):** a curva real e seus trechos lineares ficam dentro da faixa das ordens geográficas simuladas; nenhuma conversão do oponente para o PT é necessária para explicar o resultado nacional; o "109 seções com zero voto" não reproduz (são 106 no 2º turno; 143 em 2022, 328 em 2018); às 19h34 só 7,8% dos BUs tinham sido recebidos, não 70%.
- **Linhas com ressalva de desenho (A1, A2, A3, A12):** pelos critérios pré-registrados, saíram com rótulo de excesso, mas **o mesmo teste acusa excesso em séries ou anos sem manipulação** (A1: 20 de 20 simulações limpas; A2: o PT de 2022; A3: coeficientes negativos em todos os anos; A12: 44% de simulações limpas). As versões corrigidas não mostram excesso. Resultado original e corrigido, lado a lado, em [Resultados da Fase 2](resultados-fase2.md) e [Questões em aberto](residuos.md).
- **Impacto agregado** (só testes sem ressalva de desenho): 38.394 votos pró-Lula e 122.543 pró-Flávio, tetos de pior caso; com as versões corrigidas no lugar das originais, o resultado é o mesmo (nenhuma das quatro versões corrigidas mostra excesso). A margem é 4.430.191.
## O que não foi testado
Ver [Questões em aberto](residuos.md), [Pontos cegos](pontos-cegos.md) e a lista de **NÃO EXECUTADO**: cruzamento com boletins impressos (sem insumo), assinatura criptográfica da urna, curva de divulgação do site Resultados, perfil de comparecimento de 2026/2º turno, 2014 na curva de apuração, as "472 urnas" do vídeo.

## Autoria
{{AUTORIA}}
