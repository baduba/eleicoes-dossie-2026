# A44 — Quedas verticais na curva acumulada de apuração (resultado, Adendo 20)

Teste pré-registrado no **Adendo 20** (`00_preregistro.md`, 31/10/2026, antes de rodar). Alegação (vídeo
"Prof. Trindade", Inventário A13/A16): a curva de percentual acumulado de votos teria quedas verticais,
impossíveis numa soma acumulada. Script: `scripts/49_a44_quedas_curva.py`. Saídas: `results/fase5/A44_*`
(pasta nova: Fase 5 — A20–A35 estão em `fase3`/`fase4`; documentado aqui por ser o primeiro teste rodado da
Fase 5). Figura: `docs/img/a44_curva_3versoes.(png|svg)` (+ `_m`), eixo Y 0–100% com a margem final marcada
(regra de exibição registrada no adendo). Versão em inglês da figura: pendente (pipeline `traducao_en`).

## 1. Os dois relógios existem — a versão (c) foi executável (sem plano B)

`parquet/ordem_2026_t2.parquet` traz, para as 499.248 seções, **sem nulos**:
`DT_RECEBIMENTO_BU_HOR_TSE` (recebimento do BU no TSE) e `DT_PRIM_TOT_PARCIAL_HOR_TSE` (primeira totalização
parcial). Os dois carimbos diferem em 99,98% das seções (mediana de segundos — A14 já medira: atraso
recebimento → totalização com mediana < 1 min). Cobertura do pareamento com o BU: 499.205 de 499.205 seções
apuradas (43 linhas do arquivo de ordem, todas ZZ, não têm BU correspondente).

## 2. As três versões e a hipótese da mistura

| versão | X | Y (% Lula) | quedas ≥ 0,02 p.p. | máx. queda | máx. salto |
|---|---|---|---|---|---|
| (a) recebidos | BUs recebidos | sobre recebidos | 41 | **−3,26 p.p.** | +0,08 |
| (b) totalizados | BUs totalizados | sobre totalizados | 42 | **−3,02 p.p.** | +0,09 |
| (c1) mista | recebidos | sobre totalizados | 42 | −3,02 p.p. | +0,09 |
| (c2) mista | totalizados | sobre recebidos | 41 | −3,26 p.p. | +0,08 |

As versões (a) e (b) são quase idênticas ponto a ponto — os dois relógios diferem por segundos —, portanto
as mistas (c) **não acrescentam evento nenhum**: a hipótese pré-registrada de "artefato de mistura de
contagens" **não produz efeito no dado público por seção** (ela exigiria defasagem grande entre recebido e
totalizado, que A14 já mostrara não existir).

## 3. Existem quedas — e todas fecham (veredito: EXPLICADO)

Há 42 quedas e 53 saltos ≥ 0,02 p.p. na versão real (b). Perfil: **todas as quedas grandes estão na janela
inicial**, quando a base acumulada é de centenas a poucos milhares de BUs (0,25% das seções estavam
contabilizadas antes da retomada das 19h — decisão Zanin, ver A14/nota):

| minuto | Δ observado | BUs no lote | share do lote | share antes → depois | top UFs do lote |
|---|---|---|---|---|---|
| 19:03 | **−3,02 p.p.** | 676 | 43,5% Lula | 55,53 → 52,51 | PR, DF, RO, AM, PA |
| 17:06 | −1,92 p.p. | 418 | 50,9% | 58,59 → 56,66 | PR, PA, AM, DF |
| 17:07 | −1,13 p.p. | 391 | 50,7% | 56,66 → 55,53 | PR, PA, DF, AM |
| 19:04 | −0,27 p.p. | 4.909 | 52,1% | 52,51 → 52,24 | PA, PR, PB, AM, DF |
| 19:19 | −0,21 p.p. | 892 | 48,9% | 51,66 → 51,45 | PR, PA, DF, MG |

Depois das 20h (base > 23% das seções), o maior movimento é de **0,091 p.p.** — invisível em escala 0–100%.

**Fechamento (regra do Adendo 20):** para cada um dos 95 eventos da versão (b) (e dos 93 da (a)), o efeito
calculado do lote do minuto é **exatamente** a variação observada (|efeito − observado| = 0,0 em 100% dos
eventos — identidade aritmética, pois a curva é reconstruída dos mesmos BUs). Tabela completa:
`results/fase5/A44_eventos.csv`. Como 100% ≥ 95%, **veredito: EXPLICADO**. Ressalva registrada: na curva
reconstruída o fechamento é identidade por construção; o que o teste decide é que (i) toda queda tem um lote
correspondente com composição plausível (UFs/municípios listados), (ii) quedas grandes só existem com base
acumulada pequena — aritmética de média acumulada, não retirada de votos — e (iii) a mistura de relógios não
gera quedas adicionais.

**Placebo 2022 T2** (`A44_resumo_versoes_2022.csv`): o mesmo fenômeno, maior: quedas de até **−8,41 p.p.**
(recebidos) e −3,56 p.p. (totalizados), também concentradas na base pequena. Quedas verticais na janela
inicial da apuração são a regra em qualquer eleição, não uma assinatura de 2026.

## 4. O que não fecha por construção (limite declarado no adendo)

O feed **ao vivo** do portal (divulgação, snapshots minuto a minuto) não está arquivado no repo — A14 já
registrara "divulgação: NÃO EXECUTADO (sem snapshots)". Se as quedas do vídeo vieram do feed do portal e não
da contagem por seção, essa versão específica não é reconstruível; mas qualquer curva construída dos dois
relógios públicos se comporta como acima.

## 5. H9 reafirmado (números exatos)

O total final **independe da ordem** de recebimento/totalização e bate com a soma dos BUs
(`A44_h9_totais.csv`, incluindo o exterior/ZZ, que entra no total oficial): Lula **64.256.232**,
Flávio **59.826.041**, válidos 124.082.273, **margem 4.430.191** — exatamente os totais oficiais publicados.
