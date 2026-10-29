# Gatilhos combinados e a tese da inversão de voto (memorando exploratório)

Data: 2026-10-29. **Tudo aqui é EXPLORATÓRIO**: números calculados depois de ver os dados, sem veredito formal.
Continuação de `docs/propostas/novos-pontos-cegos.md`. Scripts novos em `scripts/exploratorio/`, saídas em
`results/exploratorio/`. Restrição de ambiente declarada lá vale aqui: sem os parquets por seção nesta máquina,
as interseções usam os agregados versionados em `results/`.

---

# PARTE 1 — A tese da INVERSÃO de voto (eleitor vota 13, registra 22, e vice-versa)

## 1.1. Enquadramento: é uma instância do ponto cego A19

A inversão é a forma mais parcimoniosa da falha "voto digitado ≠ voto registrado" (elo A19 da matriz de pontos
cegos): em vez de criar ou apagar votos, o software **troca** o destino de uma fração dos votos entre os dois
finalistas. Comparecimento, brancos, nulos, RDV, BU, BWeb e totalização permanecem todos consistentes, e os
agregados ficam próximos do esperado — apenas rotacionados.

**Por que os testes internos são à prova de inversão, em 3 linhas:** RDV, BU, imagem do BU, log e BWeb nascem do
mesmo software que faria a troca; compará-los entre si (A4, H9) mede coerência interna de um fluxo único, não
correspondência com o que o eleitor digitou. Uma inversão coerente passa por todos esses testes com zero
divergências — exatamente o que A4/H9 mediram.

## 1.2. Quantificação

Inverter um voto move a margem em **2** (um a menos de um lado, um a mais do outro). Para anular a margem oficial
M = 4.430.191:

| grandeza | valor | fonte |
|---|---|---|
| votos a inverter | **2.215.096** (= M/2) | cálculo |
| denominador (válidos dos dois finalistas, 2026/T2) | **124.082.273** | `H9_h9_totais_2026_T2.csv` |
| fração dos válidos | **1,785%** | cálculo (confirma o "~1,7%" do pedido) |
| seções necessárias se a inversão fosse total dentro de cada urna | ~8.900 a 22.200 seções (1,8%–4,4%), conforme trocas/seção (tabela já versionada: `results/graficos/secoes_para_inverter.csv`, que reproduz a identidade) | G2 |

**Poder de detecção existente** (`results/graficos/curvas_deteccao.csv`, fração de urnas alteradas ≈ 1,7–1,8%,
inversão uniforme):

| instrumento | n | P(detectar inversão de ~1,8%) | estado atual |
|---|---|---|---|
| teste de integridade completo | 648 urnas | **≈ 1,000** | relatório consolidado do TCU pendente (prazo ~30 dias após o T2); A19 |
| teste com biometria (10% das urnas) | 65 | 0,68 | idem |
| teste com biometria (5%) | 32 | 0,43 | idem |
| boletins impressos conferidos | 100 | 0,83 | **0 conferidos** (`results/graficos/bu_conferidos.csv`) |
| boletins impressos conferidos | 300 | **0,995** | 0 conferidos |
| boletins impressos conferidos | 1.000 | ≈ 1,000 | 0 conferidos |

Leitura: uma inversão de 1,8% das urnas é **grande o bastante para ser vista** pelo teste de integridade completo
e por 300 boletins impressos. O elo está aberto **hoje** não por impossibilidade, mas por cobertura zero de BU
impresso e relatório do TCU ainda não consolidado. Com 1% de urnas alteradas (~2,47 milhões de votos, mais que a
margem), o teste de integridade ainda vê (P≈1), mas 100 BUs só veem com P≈0,56 (interpolando a curva: em 1%,
n=298 para 95% — `poder_bu_impresso.csv`).

## 1.3. Âncoras de detecção que existem ou existiriam

| âncora | o que veria uma inversão | cobertura no dossiê | poder contra inversão de 1,8% |
|---|---|---|---|
| boletim impresso fotografado | BU impresso ≠ BU digital na mesma seção | 0 conferidos; infra pronta (`04_cruza_bu_impresso.py`, listas A31/A31b/A33) | 0,83 (n=100) a ≈1 (n=300) — **o gargalo é coleta, não poder** |
| teste de integridade (TCU) | voto de papel ≠ voto registrado na urna sorteada | levantamento de poder feito (A19); resultado consolidado pendente | ≈1,0 se a inversão for uniforme; cai se a inversão evitar urnas sorteadas (por isso A24 importa) |
| coerência presidente × governador (A22) | presidente "destoando" do governador alinhado na mesma seção | NÃO EXECUTÁVEL em 2026 (nenhuma UF elegível pela regra; variante 9b com 2 UFs, poder muito baixo) | baixo em 2026; cobriria só inversão restrita ao cargo de presidente |
| transições T1→T2 (A31) | inversão concentrada apareceria como f extremo | executado; Silva Jardim dentro da cauda; 20 extremos caracterizados | inversão **uniforme** é invisível (se confunde com transferência legítima); concentrada, parcialmente visível |
| pesquisas eleitorais/boca de urna | resultado fora do intervalo das pesquisas finais | A7 limitado (registro de pesquisas, sem série completa) | **fraco**: erro típico de pesquisa final ±2 p.p. cobre 1,8%; só detecta inversões ≥ ~4 p.p. |
| listas de fiscais (A23) | comportamento diferente onde há fiscal | NÃO EXECUTADO (lista não é pública) | desconhecido; LAI pendente |
| voto digitado↔registrado por eleitor | o próprio ato | **não testável com nenhum dado público** (sigilo) | nulo — por isso a âncora é sempre amostral (BU, teste de integridade) |

## 1.4. PRÉ-REGISTRO A37 — inversão de voto (texto pronto para revisão ANTES de rodar)

*Estilo dos adendos de `00_preregistro.md`. A37 não é um teste estatístico novo sobre os agregados — é a
formalização da pergunta e das regras de evidência, porque a única evidência decisiva é externa (BU impresso,
teste de integridade). Registrar a regra ANTES desses dados chegarem é o que impede mover a trave depois.*

**Declaração de ordem (a preencher na assinatura).** Antes deste adendo vi: os resultados de A4, A19, A22, A31 e
as curvas de poder (G2). Não vi nenhum boletim impresso (0 conferidos) nem o relatório consolidado do TCU.

**Pergunta.** Uma fração f dos votos dos dois finalistas foi trocada entre eles pelo software da urna (inversão
13↔22), mantendo todos os totais internamente coerentes?

**Hipótese nula (H0).** f = 0: o voto registrado é o voto digitado em todas as urnas.

**Métricas e regras de decisão (cada uma pré-compromissada).**

1. **Boletins impressos (principal).** Para cada BU fotografado recebido (via página `boletins-impressos` ou
   coleta dirigida às listas A31b_20, A33_20 e A32_50): divergência de **um voto** em qualquer candidato entre
   impresso e BWeb é reportada individualmente. Regra: f̂ = divergências de troca 13↔22 / votos conferidos;
   IC95 por Wilson. **Refuta a inversão de magnitude m** se o limite superior do IC95 < m com n calculado pela
   tabela de poder já versionada (`poder_bu_impresso.csv`: n=298 para refutar 1% com 95%; n=149 para 2%).
   Convenção de sentido: troca em qualquer direção conta; desequilíbrio de sentido é reportado à parte.
2. **Teste de integridade (TCU).** Quando o relatório consolidado sair: se o número de urnas com divergência
   papel×registro para presidente for 0 em n urnas, o limite superior de f é 3/n (regra dos três), e A37 registra
   "inversão ≥ 3/n REFUTADA pelo teste de integridade, **sob a premissa de que a inversão não evita urnas
   sorteadas**" (premissa declarada; A24 é o teste da premissa e segue NÃO EXECUTADO por falta das listas dos TREs).
3. **Agregados (fracos, já corridos — não reabrir).** A22 (NÃO EXECUTÁVEL em 2026), A31 (distribuição de f
   municipal) e A7 (pesquisas) **não** têm poder para f < ~2% e não entram no veredito de A37; são citados como
   contexto. Uma inversão **concentrada** em poucos territórios apareceria em A31 como f extremo sem perfil de 1º
   turno que o explique; o único município FORA DA CAUDA SEM PRECEDENTE (Itacoatiara/AM) já tem lista de seções
   para coleta de BU (`A31_top20_2026.csv` + fluxo bruto documentado).
4. **O que REFUTARIA a tese da inversão na magnitude da margem (f ≈ 1,8%).** Qualquer um de: (a) ≥300 BUs
   impressos conferidos com zero divergências de troca (P de erro ≈ 0,5%); (b) relatório do TCU com zero
   divergências em ≥ 170 urnas sorteadas (limite 3/n < 1,8%), sob a premissa declarada; (c) ambos parciais
   combinados pela regra dos três sobre o total de urnas independentes conferidas.
5. **O que NÃO refutaria.** Consistência interna (A4/H9/A5) — é à prova de inversão por construção; pesquisas
   dentro do intervalo — poder insuficiente; ausência de rajadas nos logs (A32) — inversão não deixa rastro
   temporal.
6. **Veredito.** Enquanto (4) não for satisfeito: **NÃO FECHADO — cobertura insuficiente** (não "refutado" e não
   "sustentado"; hoje: 0 BUs, TCU pendente → a janela de 1,8% está inteiramente aberta). Proibido converter
   "janela aberta" em "evidência de inversão": a ausência de verificação não mede f.

---

# PARTE 2 — GATILHOS COMBINADOS (empilhamento de bandeiras)

## 2.1. Inventário de bandeiras e disponibilidade local

| bandeira | origem | por seção/município local? |
|---|---|---|
| crescimento 80+/90+/100+ (aptos e votantes vs. Censo e vs. coorte) | A20, A20b-idosos | município: sim (`A20_maiores_razoes_2026.csv`, 30 mun.; `A20b_2a_lista_municipios_2026.csv`, 2 mun.) |
| liberação manual extrema / excesso sobre modelo 2022 | A32 (itens 2–3), A33 | seção: top-50 (`A32_50_secoes_excesso_2026T2.csv`); escola: 661 (`A33_escolas_extremas.csv`) |
| seções novas pós-2022 com comparecimento ≥95% | H5/A27 | só agregado; município: `A27_maiores_municipios.csv` (15 mun.) |
| zero voto no oponente / zero BN | A12, A12b | seção: sim (200 linhas A12, 106 A12b, com manual_rate, modelo, encerramento) |
| turnout ≥95% | H5 | só agregado (lista das 639 não versionada) |
| modelo de urna UE2022 | A10/A15 | só dentro de arquivos de seções sinalizadas |
| rajadas de log / duração do voto | A32/A32b; A34 | agregado por ano; A34 não rodado (sem `urna_out/` local) |
| município extremo T1→T2 (f, z) | A31, A31b | município: sim (`A31_municipios.csv`, 5.357 elegíveis 2026, com dL/dF/dC/z/p_holm) |
| seção apurada por ata | — | **não existe** (nunca computada; ver candidato 2 do memorando anterior) |

## 2.2. Interseções computadas (números reais, exploratório)

Script: `scripts/exploratorio/03_gatilhos_intersecoes.py`. Saídas: `results/exploratorio/empilhamento_*.csv`,
`intersecoes_entre_conjuntos_secao.csv`.

**Nível seção** — dentro do conjunto A12 zero-voto (106 zero-oponente + 94 zero-PT, 2026/T2), bandeiras
{zero-oponente, manual > 30%, turnout ≥ 95%, urna UE2022, fechamento ≥ 19h}:

| nº de bandeiras | seções | votos Lula | comparecimento |
|---|---|---|---|
| 0 | 1 | 0 | 118 |
| 1 | 33 | 3.065 | 3.314 |
| 2 | 71 | 10.987 | 11.250 |
| 3 | 5 | 808 | 842 |
| 4+ | 0 | — | — |

Interseções entre conjuntos distintos: A12b (106 zero-oponente) ∩ A32 top-50 excesso manual = **0 seções**;
A12 zero-voto ∩ A33 escola extrema (mesma zona+município) = **23 seções**.

**Nível município** (5.357 elegíveis de A31, 2026) — 8 bandeiras {A31 fora da cauda (p_holm<0,05), A31b dF≤+1,
A20 razão aptos/pop16 alta, A20b idosos R>1, A27 seções novas ≥95%, A33 escola extrema, A32 top-50 manual,
A12 seção zero-voto}:

| nº de bandeiras | municípios |
|---|---|
| 0 | 4.211 |
| 1 | 1.037 |
| 2 | 101 |
| 3 | 8 |
| 4+ | **0** |

Os 8 com 3 bandeiras: Atalaia do Norte/AM, Santa Helena/MA, Viana/MA, Alenquer/PA, Novo Repartimento/PA,
Oriximiná/PA, Jatobá do Piauí/PI (todos: dF≤1 + escola extrema + seção zero-voto) e **Santos/SP** (seções novas
≥95% + escola extrema + top-50 manual — o único empilhamento **urbano**, sem a bandeira dF≤1). Concentração por UF
(municípios 2+, % dos elegíveis): AM 31,0%, PA 15,5%, MA 10,4%, PI 5,9%, CE 4,9%; SP 0,47%, RS 0,40%.

## 2.3. Discernindo fraude organizada de concentração benigna

O empilhamento observado tem **assinatura benigna dominante**: as bandeiras não são independentes — seções
pequenas, rurais, indígenas e remotas geram simultaneamente zero-voto (poucos eleitores, unanimidade local),
liberação manual alta (sem biometria cadastrada, idosos), seção "nova" (remanejamento) e dF≤1 (pool pequeno;
A31b mostrou a concentração Nordeste/Amazônia e que 70,6% dos 748 tiveram queda de comparecimento). Por isso a
razão de chance **não** é o produto das frequências marginais, e o teste honesto do empilhamento exige um nulo de
permutação que preserve a estrutura rural/pequena (ver §2.4).

Três achados que NÃO se encaixam na leitura benigna e merecem prioridade de verificação documental:
1. **Santos/SP**: único município grande e urbano com 3 bandeiras, e numa combinação diferente (seções novas
   ≥95% + escola com excesso de manual + seção top-50 de excesso manual) — não explicável por "remoto e sem
   biometria". Alvo natural de coleta de BUs impressos e atas.
2. **Itacoatiara/AM** — o município mais extremo do modelo A31 (z = 188, FORA DA CAUDA SEM PRECEDENTE) — **não
   acumula nenhuma outra bandeira** do painel. Se o desenho de fraude fosse o "sombra" que o dono suspeita
   (idosos + manual + urnas isoladas somando), o pior município deveria empilhar; ele não empilha. Isso enfraquece
   a hipótese de soma organizada e fortalece a leitura de cauda estatística (Adendo 10b: o modelo tem pouco poder
   em municípios pequenos com fluxos brutos grandes).
3. A interseção **vazia** A12b ∩ A32-top50: as seções mais unânimes e as de maior excesso de liberação manual são
   conjuntos **disjuntos** — uma operação única que produzisse ambos os sinais nas mesmas seções não existe nos
   dados.

## 2.4. Índice de exposição por seção — metodologia e pré-registro esboçado

**ADVERTÊNCIA CENTRAL (obrigatória em qualquer página que publique o índice).** Um índice composto de bandeiras
**não é uma medida de probabilidade de fraude**: as bandeiras são parcialmente causais entre si e todas têm
explicações benignas concentradas nos mesmos territórios. O índice serve **apenas para ordenar onde gastar
verificação cara e escassa** (coleta de boletim impresso, pedido de ata, folha de votação). Publicar o ranking
sem essa moldura é data dredging: com 8+ bandeiras e 499 mil seções, sempre haverá uma ponta extrema. Qualquer
uso inferencial exige pré-registro **antes** de olhar o ranking — incluído abaixo.

**Esboço de pré-registro (A38 — índice de exposição, a revisar pelo dono ANTES de computar o ranking).**

- **Unidade:** seção (2026/T2), exterior fora; escola como unidade secundária.
- **Fontes (todas já versionadas ou deriváveis dos parquets):** manual_rate e excesso sobre o modelo 2022 (A32
  item 3); turnout (H5); zero-oponente e zero-BN (A12/A12b); seção nova (A27); modelo de urna (A10); fração de
  aptos 80+ (A20b-4); distância ao centro do município ou indicador rural/indígena pelo tipo de local (A27); z de
  A31 do município; duração mediana do voto (A34, se rodado).
- **Normalização e pesos (fixados agora):** cada bandeira vira um escore de cauda empírico = posição percentil da
  seção **dentro do placebo 2022/T2** (não dentro de 2026), de modo que o escore mede "o quão incomum seria em
  2022", não "o quão incomum é em 2026". Pesos: 1 para cada bandeira primária; 0,5 para bandeiras derivadas da
  mesma fonte (ex.: zero-BN dado zero-oponente); índice = soma ponderada dos escores. **Sem otimização de pesos**:
  qualquer ajuste posterior exige novo adendo.
- **Nulo e regra de decisão sobre o ranking:** o índice é computado também para 2022/T2 com as mesmas bandeiras
  (as que existem no ano) e para **1.000 permutações** que embaralham os rótulos de bandeira **dentro de estratos**
  (porte da seção × tipo de local × UF), preservando a concentração benigna. Regra: o topo do ranking de 2026 só
  é declarado "empilhamento além da estrutura" se o índice do percentil 99,9 de 2026 superar o de 2022 e o das
  permutações. Se não superar (previsão: não supera, dado o §2.3), o índice é publicado **só como fila de
  verificação**, com a frase-moldura.
- **Uso declarado (único):** ordenar a coleta de BUs impressos e os pedidos LAI de atas/folhas, em blocos de N
  seções; cada bloco verificado atualiza a fila (amostragem adaptativa declarada).
- **O que NÃO se pode concluir dele:** probabilidade ou quantidade de fraude; que uma seção do topo "é suspeita";
  qualquer teto de votos de margem (o índice não tem unidade causal); comparação com a margem de 4.430.191.

---

## Saídas desta rodada

- `scripts/exploratorio/03_gatilhos_intersecoes.py`
- `results/exploratorio/empilhamento_nas_secoes_zero_voto.csv`
- `results/exploratorio/intersecoes_entre_conjuntos_secao.csv`
- `results/exploratorio/empilhamento_por_municipio_distribuicao.csv`
- `results/exploratorio/empilhamento_por_municipio_2mais.csv` (109 municípios com 2+ bandeiras, com as bandeiras)
- `results/exploratorio/empilhamento_por_uf.csv`
- `docs/propostas/gatilhos-e-inversao.md` (este memorando: tese da inversão + pré-registro A37 + empilhamento +
  esboço A38)
