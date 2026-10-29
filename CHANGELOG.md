# Changelog e correções

Erros meus corrigidos no caminho e mudanças feitas depois de ver resultados. Datas em 2026.

## Fase 2 (2026-10-28 e 2026-10-29)
- Pré-registro Adendo 4 escrito antes de qualquer análise nova.
- **A1:** o envelope "permutação dentro da UF" foi rejeitado nos quatro anos (a ordem de chegada dentro da UF não é aleatória em nenhuma eleição). Pelo critério pré-registrado, a linha sai como excesso; análise posterior (corte a partir de 10% das seções) mostra 2026/T2 abaixo de todos os placebos. Linha mantida com ressalva de desenho.
- **A2:** o placebo "por papel" (oponente) era inadequado. Em 2022 o PT, que liderou o 1º turno, perdeu votos absolutos em 12,6% das seções; em 2026 foi o oponente (11,8%). Linha mantida com ressalva.
- **A3:** os coeficientes ecológicos "oponente no T1 para PT no T2" são negativos em todos os anos; a diferença entre 2026 e 2022 não mede conversão. Com efeito fixo de município o coeficiente de 2026 é o mais negativo. Linha mantida com ressalva; a contabilidade por identidade e a perda líquida mínima por seção são publicadas ao lado.
- **A4:** meu primeiro critério de RDV acusava 10 seções por tratar votos nulos sem número como brancos; corrigido (tipo 3 sem número = branco, validado: soma igual ao BU).
- **Fontes:** os totais oficiais de 2018/T1 que citei de memória estavam trocados (o correto, divulgado pelo TSE, coincide com o BWeb). Corrigido na Fase 1.
- Tentativa de ler páginas do TSE e do STF por automação: HTTP 403. Itens que dependiam do texto oficial ficaram marcados como imprensa.

## Fase 1 (2026-10-28)
- Meu contraste inicial com placebos usava média ponderada pelo inverso da variância e escondia o placebo 2026/T1, gerando uma linha falsa de "21,8% da margem". Corrigido para interseção-união (Adendo 2).
- Interpretação errada minha: tomei a hora de recebimento do BU no TSE como proxy de encerramento. O TSE segurou o recebimento até as 19h.
- Eu disse que a tabela de fechamento do relatório original não podia ser conferida. Ela reproduz exatamente (339.593) com o relógio cru da urna.
- Rótulo "SUSTENTADA" renomeado para "excesso detectado" quando o sentido é favorável ao oponente.
- Seções "não instaladas", "anuladas" e a sentinela -1 tratadas explicitamente (Adendo 3).
