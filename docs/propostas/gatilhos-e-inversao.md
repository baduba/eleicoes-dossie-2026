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
| boletim impresso fotografado | BU impresso ≠ BU digital na mesma seção | 0 conferidos; infra pronta (`04_cruza_bu_impresso.py`, listas A31/A31b/A33) | 0,83 (n=100) a ≈1 (n=300) — **o gargalo é coleta, não poder**. **CORREÇÃO (29/10, cenário de inversão total):** o BU é impresso pelo mesmo software que inverteria; a foto bate com o BWeb mesmo sob inversão **a montante** (no ato do registro). BU só detecta inversão/alteração **a jusante** do papel (transmissão, totalização, republicação — A18). O detector do elo digitado→registrado é o teste de integridade e as âncoras externas — ver seção "Cenário de inversão total" |
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

1. **Boletins impressos (limitado à inversão a jusante).** Para cada BU fotografado recebido (via página
   `boletins-impressos` ou coleta dirigida às listas A31b_20, A33_20 e A32_50): divergência de **um voto** em
   qualquer candidato entre impresso e BWeb é reportada individualmente. Regra: f̂ = divergências de troca 13↔22 /
   votos conferidos; IC95 por Wilson. **Refuta a inversão de magnitude m** se o limite superior do IC95 < m com n
   calculado pela tabela de poder já versionada (`poder_bu_impresso.csv`: n=298 para refutar 1% com 95%; n=149
   para 2%). Convenção de sentido: troca em qualquer direção conta; desequilíbrio de sentido é reportado à parte.
   **Escopo corrigido (29/10):** este braço cobre só a inversão/alteração **a jusante do BU** (depois da impressão:
   transmissão, totalização, republicação — hipótese A18). Ele **não** cobre a inversão **a montante** (no
   registro, antes do BU), porque o papel é impresso pelo mesmo software que inverteria; para a montante valem os
   braços 2 e 4 e o pré-registro A37b (seção "Cenário de inversão total").
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

---

# PARTE 1b — CENÁRIO DE INVERSÃO TOTAL (o resultado publicado é o espelho do real)

*Adicionado em 29/10/2026, a pedido do dono: a tese é de inversão em massa (13↔22 trocados nacionalmente), não de
uma fração pequena. EXPLORATÓRIO; as âncoras internas usadas abaixo são outputs já versionados (A2, A31, A7) —
reusá-los para esta pergunta é leitura posterior, não veredito pré-registrado, exceto onde indicado.*

## 1b.0. Correção analítica (registrada também em A37, braço 1)

**Boletim impresso NÃO detecta inversão no ato do registro.** O BU é impresso pelo mesmo software que faria a
inversão: sob inversão **a montante** (digitado → registrado), o papel sai já invertido e a foto do BU bate com o
BWeb. BU impresso detecta apenas alteração **a jusante** do papel (transmissão, recepção, totalização,
republicação — a hipótese A18). O detector do elo a montante é o **teste de integridade** (votação paralela
auditada, papel×registro) e **âncoras externas ao software da urna** (outros cargos na mesma cédula, outro turno,
pesquisas, boca de urna). A37 foi ajustado para deixar a distinção explícita.

## 1b.1. Taxonomia das variantes e assinatura detectável de cada uma

### a. Inversão total só no 2º turno vs. nos dois turnos

**Só no T2.** O 1º turno publicado seria o voto real. Duas assinaturas obrigatórias, ambas **já medidas**:

1. **Eixo T1→T2 por seção viraria de sinal.** Sob inversão só no T2, a margem publicada no T2 é o negativo da
   margem real, e a margem real seção-a-seção é fortemente correlacionada com a do T1; logo
   `margem_T2_publicada ~ margem_T1` teria coeficiente fortemente **negativo** (≈ −0,9). O coeficiente versionado
   (A2, `A2_a2_swing.csv`, EF de município) é **+0,940 em 2026 — o MAIS ALTO da série** (2014: 0,824; 2018: 0,758;
   2022: 0,915). Distância do valor esperado sob inversão: centenas de erros padrão. A forma da distribuição do
   swing também está dentro dos placebos (KS 2026×placebo mais próximo = 0,019 < maior KS entre placebos = 0,123;
   `A2_a2_criterio_forma.csv`).
2. **Herança do pool (A31).** Sob inversão só no T2, o PT herdaria a base do oponente e perderia a própria:
   o f nacional (fração do pool T1→T2 capturada pelo PT) sairia de perto de 0/negativo — e os municípios
   mostrariam transições absurdas em escala nacional, não só em Itacoatiara. O f nacional versionado é **0,737**
   (PT capturou 73,7% do pool), dentro da faixa histórica (2014: 0,411; 2018: 0,645; 2022: 0,302 — ano em que o
   pool era pequeno e o PT, líder do T1), e a identidade contábil A3/A11 fecha município a município em todos os
   anos. **Leitura explícita: o padrão nacional de transição é compatível com herança normal, e incompatível com
   inversão total só no T2.**

**Nos dois turnos.** A âncora do T1 some; a comparação pesquisa→resultado precisa errar nos dois turnos, e a
inversão passa a ser testável principalmente por (b) e pelas âncoras externas (§1b.2).

### b. Inversão só na presidência vs. em todos os cargos

**Só na presidência.** Os votos de deputado federal/estadual, senador e governador na **mesma cédula** não seriam
invertidos. A correlação seção-a-seção entre o share do candidato a presidente e o share dos deputados do seu
partido — altíssima em qualquer eleição normal — **desmoronaria** em 2026 contra 2022/2018/2014. Este é o teste
interno mais forte contra a variante, é **computável com dados públicos** (`votacao_secao` tem todos os cargos;
os parquets por cargo `cargos_*` são gerados por `05_extras_bweb.py`) e está **pendente de insumo nesta máquina**
(os parquets não estão aqui — script pronto: `scripts/exploratorio/05_a37b_presidente_x_deputado.py`, falha com
NãoExecutado explícito sem o diretório).

**PRÉ-REGISTRO A37b — alinhamento presidente × deputado (a revisar ANTES de rodar).**

- **Declaração de ordem (a preencher).** Antes deste adendo vi apenas os agregados de A22 e a existência dos
  parquets por cargo; nenhuma correlação presidente×deputado foi calculada.
- **H0.** Sem inversão: o alinhamento seção-a-seção presidente×deputado do mesmo campo partidário em 2026/T2 está
  dentro do envelope dos placebos.
- **Unidade e pares.** Seção apurada (sem exterior), 2º turno, 2014/2018/2022/2026. Pares: Lula × federação PT
  (PT+PCdoB+PV) e Flávio × PL em 2026 e 2022; Haddad × PT e Bolsonaro × PSL em 2018; Dilma × PT e Aécio × PSDB em
  2014 (T1 de 2014 para o par presidencial, com o T1 de 2026/2022/2018 como sensibilidade simétrica).
- **Métrica (fixada).** Por UF e par: correlação de Spearman entre share do presidente (válidos do cargo) e share
  do partido nos votos de deputado federal da seção; estatística nacional = mediana das 27 UFs, ponderada por
  seções. Métrica secundária: R² da regressão seção share_pres ~ share_dep com EF de município.
- **Regra de decisão.** Interseção-união: EXCESSO (compatível com inversão só-presidente) só se a estatística de
  2026 ficar **abaixo** do mínimo dos três placebos por mais de 2 erros padrão (bootstrap por município, 1.000
  reamostragens, semente 20261029), nos dois pares (PT e oponente). Dentro do envelope = inversão total
  só-presidente REFUTADA na magnitude nacional (qualquer inversão residual teria de ser pequena e localizada).
- **Teto em votos de margem se INCONCLUSIVO** (poder insuficiente ou dados faltantes): a menor inversão detectável
  dado o desvio padrão residual da regressão, convertida por fator 2 sobre os válidos; calculado ao rodar.
- **Limite declarado.** Não detecta inversão simultânea em todos os cargos (essa exige âncora externa), nem
  inversão só-presidente em escala muito pequena.

**Em todos os cargos e turnos.** Nenhuma âncora interna resta: RDV, BU, BWeb, totalização, correlações entre
cargos e entre turnos seriam todos coerentes por construção. Restam só âncoras externas ao software: teste de
integridade, boca de urna, pesquisas, e o custo político da operação (§1b.2 e §1b.3).

### c. Relação entre as três variantes

A37 (já registrado) cobre a inversão **parcial** (fração f dos votos, uniforme ou concentrada), detectável por
amostragem (teste de integridade; BU só a jusante). A inversão **total só no T2** é a variante mais fraca da tese
do dono — já contraindicada pelos eixos internos (a). A inversão **total só-presidente nos dois turnos** é a
variante testável restante — via A37b. A inversão **total em todos os cargos e turnos** é o ponto cego terminal
— só âncoras externas.

## 1b.2. Âncoras externas com poder real contra inversão total

**Pesquisas pré-eleitorais (A7, já versionado) — cálculo sob as duas hipóteses** (saída:
`results/exploratorio/inversao_total_ancoras.csv`). Margem oficial = 3,57 p.p. dos válidos; a inversão total
desloca cada share por 1× a margem (a distância entre os dois mundos é 2× = 7,14 p.p.).

| hipótese | erro esperado da pesquisa final contra o resultado publicado | erro observado 2026 |
|---|---|---|
| sem inversão | pequeno (série do repo: 0,13 p.p. em 2018; 1,1 p.p. em 2022) | **2,79 p.p. (Datafolha), 2,59 p.p. (AtlasIntel)** — os maiores da série, fora da margem declarada (já registrado em A7) |
| inversão total | ≈ 1× margem = **3,57 p.p.** contra o publicado (e ~0 contra o espelho) | 2,79 / 2,59 p.p. contra o publicado; **0,79 / 0,99 p.p. contra o espelho** |

**Leitura honesta (correção ao enunciado que eu mesmo faria):** a pesquisa pré-eleitoral **não decide** a
inversão total. Os erros observados são consistentes com as duas hipóteses — ou as duas pesquisas finais erraram
~2,7 p.p. na mesma direção (o maior erro da série do repo, fora da margem declarada), ou acertaram a realidade
espelhada. O que a pesquisa exclui é uma inversão total **com pesquisas corretas sobre o mundo publicado**: se
alguém afirma que "as pesquisas estavam certas e o resultado é real", o erro de 2,7 p.p. precisa ser explicado;
se afirma inversão total, o erro de 0,8–1,0 p.p. contra o espelho é compatível. A série histórica de erros de
boca de urna/Ibope (o "quanto seria o maior erro da história") **não está no repo** — insumo a coletar, com fonte
(registros TSE + arquivos dos institutos).

**Pesquisas pré-T1 × resultado do T1 (assinatura da variante "só no T2").** Se a inversão fosse só no T2, o T1
publicado bate com as pesquisas de boca de urna do T1. **Insumo a coletar:** resultados de boca de urna do 1º
turno de 2026 (Datafolha/Ibope publicam no dia) — não há no repo; as pesquisas registradas estão em
`data/pesquisas_registro_tse_24out2026.csv`, mas sem os resultados (A7 já registrou essa limitação).

**Boca de urna (exit poll) do T2.** Mede o voto real no dia, fora do software: sob inversão total, divergiria do
publicado por ~1× margem (3,6 p.p.) — muito além do erro típico de exit poll (1–2 p.p.). **Não há dado de boca
de urna no repo** — insumo a coletar com fonte (Datafolha/Ibope/publicações dos institutos; nada automatizável do
TSE).

**Teste de integridade (TCU).** Único detector direto do elo digitado→registrado. Contra inversão **total**, o
poder é ≈1 mesmo com dezenas de urnas (fração alterada ~100%). Resultado consolidado pendente; premissa declarada
de sempre (a inversão não evita urnas sorteadas; A24 segue NÃO EXECUTADO). Notícia pública de outubro/2026 já
citada no dossiê ("teste de integridade confirma correspondência entre cédulas e votos registrados") aponta zero
divergências parciais — a consolidar no relatório.

**Custo político-organizacional (não é teste, é contabilidade de exigências).** Inversão total em todos os cargos
e turnos exigiria silêncio simultâneo de: partidos e fiscais em 499 mil seções (o BU impresso bateria com o
publicado mesmo sob inversão, mas fiscais e mesários lembram do movimento, das parciais anotadas e das
zerésimas), mesários que registram ocorrências em ata, institutos de pesquisa (pré-eleitorais e boca de urna),
e as instituições do teste de integridade (TCU, MP, partidos, OAB, Forças Armadas). Não é prova de
impossibilidade; é a lista do que a tese precisa carregar.

## 1b.3. Síntese: variante × detector × cobertura × veredito provisório honesto

| variante | detector decisivo | cobertura atual | veredito provisório (exploratório) |
|---|---|---|---|
| parcial uniforme/concentrada (A37) | teste de integridade; BU só a jusante | TI pendente; 0 BUs | **NÃO FECHADO — janela de ~1,8% aberta** até TI/BUs |
| total só no 2º turno | eixo T1→T2 (A2), herança do pool (A31), identidade A3 | já medido | **fortemente contraindicada**: coef. swing 2026 = +0,940 (maior da série; sob inversão seria ≈ −0,9); f nacional 0,737 dentro da faixa histórica |
| total, dois turnos, só na presidência | **A37b** (correlação presidente×deputado) | script pronto; **pendente dos parquets por cargo** (ausentes nesta máquina) | **TESTÁVEL, não executado** — é o próximo teste a rodar |
| total, todos os cargos e turnos | teste de integridade; boca de urna; pesquisas (fracas); custo político | TI pendente; sem boca de urna no repo | **ponto cego quase filosófico** — não refutável por dados públicos de urna; carrega exigência de silêncio universal e a previsão pré-registrável de exit polls divergindo ~3,6 p.p. do publicado |

**Consequência prática para o projeto.** Ordem de trabalho sugerida: (1) rodar A37b assim que os parquets por
cargo estiverem disponíveis (fecha a variante testável restante); (2) coletar boca de urna do T1 e do T2 de 2026
com fonte (âncora externa barata); (3) registrar o resultado consolidado do TCU quando sair, com a regra dos três
já fixada em A37; (4) manter a coleta de BUs impressos para o braço a jusante (A18), sem vendê-lo como detector
da inversão a montante.

---

---

# PARTE 3 — RODADA COM DADOS BRUTOS (30/10/2026): empates/±1 e Nordeste sem-biometria × troca

*Dados brutos agora nesta máquina (`parquet/`, `parquet2/`, `cesp/`, `dados_locais/`). Tudo EXPLORATÓRIO, sem
veredito formal. Scripts: `scripts/exploratorio/06_empates_margem1.py` e `07_nordeste_biom_troca.py`; saídas:
`results/exploratorio/A_empates_resumo.csv`, `A_distribuicao_margem_obs_esp.csv`, `A_empates_troca_urna.csv`,
`B_nordeste_biom_troca.csv`.*

## 3.A. Investigação A — "aperto artificial"? Empates e margens de ±1 voto

**O que o dono quer dizer.** Se alguém "amarra" o placar — igualando urnas ou dando +1 — apareceriam empates e
vitórias por 1 voto em excesso, e assimetria no +1.

**Definição usada:** seções apuradas, sem exterior, com votos válidos > 0. As contagens do dono **reproduzem
quase exatamente**: empates 2.150 (ele achou 2.155 — 5 seções de diferença, provavelmente filtro de exterior ou
de válidos); ±1: 4.517 (ele: 4.525); 2022: 1.936 (ele: 1.940) e 3.805 (ele: 3.821). A leitura usa as minhas
contagens; a diferença é de definição de universo, documentada.

**A) Tamanho real dos conjuntos (respostas diretas às perguntas do dono).**

| conjunto | 2026 | 2022 |
|---|---|---|
| seções empatadas | 2.150 | 1.936 |
| **votos válidos nas seções de empate** | **517.768** | **467.950** |
| seções decididas por exatamente 1 voto | 4.517 (Lula+1: 2.268; Flávio+1: 2.249) | 3.805 (PT+1: 1.845; Bolsonaro+1: 1.960) |
| **votos válidos nas seções de ±1** | **1.087.289** | **926.697** |

Custo de fabricar um empate artificialmente: para uma seção com margem m, bastam ⌈m/2⌉+1 votos movidos (troca) ou
⌈m/2⌉ votos retirados — na mediana, seções têm ~260 comparecimento, então "amarrar" uma seção típica exigiria
dezenas de votos por seção, e 2.150 seções exigiriam coordenação em dezenas de milhares de votos **dentro de cada
zona eleitoral**, seção por seção, sem deixar rastro de fluxo (A31 mede exatamente isso e não achou).

**B) O teste nulo correto — observado vs. esperado sob acaso puro.** Nulo: em cada seção, votos dos finalistas ~
Binomial(n = válidos, p = share de Lula da zona eleitoral, leave-one-out). Esperado = soma das probabilidades de
|margem| = m, m = 0..10:

| ano | empates obs. | esperado | razão | ±1 obs. | esperado | razão |
|---|---|---|---|---|---|---|
| 2026 | 2.150 | 2.336,8 | **0,920** | 4.517 | 4.672,0 | **0,967** |
| 2022 | 1.936 | 2.028,3 | **0,954** | 3.805 | 4.037,6 | **0,942** |

O observado fica levemente **ABAIXO** do esperado sob o nulo nos dois anos e em todas as faixas |margem| = 0..10
(razões 0,92–0,98 em 2026; 0,94–0,97 em 2022). O déficit sistemático é o artefato conhecido do nulo binomial:
votos reais têm sobredispersão (o eleitorado de uma seção é mais homogêneo que a média da zona), o que afasta a
margem de zero. O ponto para o dono: **2026 não tem excesso de empates nem de ±1 — tem menos que o nulo e menos,
em razão obs/esp, que 2022**. Por seção, a frequência de empates cresceu 5,1% de 2022 para 2026 (razão 1,051),
praticamente o crescimento do número de seções (5,7%).

**C) Simetria do ±1 (2026).** Lula+1: 2.268 × Flávio+1: 2.249; teste binomial de simetria p = **0,789**
(2022: p = 0,065, levemente pró-oponente). Simetria quase perfeita: contra-evidência direta de "amarração
dirigida".

**D) Composição.** Empates não são fenômeno de urna minúscula: mediana de comparecimento 259 (empates) vs. 263
(geral); ±1: 258. São seções de tamanho típico — é aí que |margem| pequena é mais provável em massa.

**E) Troca de urna.** 2026 (juncão CESP validada: reproduz os 0,60% de A6 no geral): empates com urna trocada
0,84% (18 seções) vs. 0,61% no geral; ±1: 0,47% (21 seções) — **na taxa nacional ou abaixo**. (Para 2022 a
juncão rápida CESP×BWeb não é confiável — numeração divergente, dá 95% de "troca" contra 1,72% medido por A6; uso
o número de A6 como referência e registro a limitação.)

**O que os números sustentam.** Padrão compatível com acaso: sem excesso de empates/±1, sem assimetria, sem
sobrerrepresentação de troca de urna. Se as contagens do dono fossem sinal de amarração, o sinal teria de estar
**melhor** escondido em 2026 do que em 2022 — e 2026 é o ano com *menos* empates relativos ao nulo.

**O que fecharia.** Boletins impressos das seções de empate/±1 (lista exportável em 1 linha a partir de
`A_empates_*`) — cobrem o braço a jusante (A18); para o elo a montante, o teste de integridade (A37).

## 3.B. Investigação B — Nordeste: sem-biometria × troca de urna × domínio

**O que o dono quer dizer.** No NE, onde Lula domina, seções com muita habilitação sem biometria e urna trocada
seriam o canal dos votos "movíveis".

**A) Correlação por taxa, município a município (n = 1.794 municípios do NE, 2026/T2).** O olho vê "capitais têm
os dois" porque capital é grande; em **taxa**, a correlação quase não existe: Spearman ρ = **0,055** (CSV do dono)
e ρ = **0,059** (recomputado dos parquets + CESP), ambos p ≈ 0,01–0,02 só pelo tamanho da amostra. ρ ≈ 0,06 é
substantivamente zero: quem tem taxa alta de sem-biometria **não** tem mais troca de urna.

**B) Sobreposição (o "pulo do gato" quantificado).** NE, 2026/T2: seções com Lula ≥ 80% dos válidos = **31.506**.
Dessas, com urna trocada OU município no p90 de taxa sem-biometria (> 11,9%): **3.469 seções, 645.034 votos de
Lula, saldo líquido 537.354**; teto de pior caso (fator 2) = 1.074.708 votos de margem = **24,3% da margem**.

**C) O mesmo corte em 2022 (controle de forma — obrigatório).** 2022/T2, mesma regra (sem a flag de troca, cuja
juncão 2022 não é confiável — ou seja, comparação conservadora a favor de 2022): **3.766 seções, 703.521 votos de
Lula, saldo 602.222, teto 27,2% da margem**. O padrão é **igual ou maior em 2022** — eleição que o campo do dono
considera legítima. Conclusão sem cerimônia: o perfil NE (sem-biometria alta no interior, domínio eleitoral do PT)
é **estrutural**, não específico de 2026; ele prediz 2022 tão bem quanto 2026.

**D) Oponente com 0 a 10 votos, Brasil (confirmação do 3.042 do dono).**

| ano | seções | votos de Lula nelas | saldo | teto fator 2 | NE (seções) | NE (votos Lula) |
|---|---|---|---|---|---|---|
| 2026 | **3.029** (dono: 3.042; diferença de 13 = filtro de universo) | 394.960 | 376.149 (dono: 376.347 ✓) | 752.298 = 17,0% da margem | 1.968 (65%) | 256.695 |
| 2022 | **4.097** | 530.613 | 505.308 | 1.010.616 | 3.010 (73%) | 405.615 |

O conjunto **encolheu** de 2022 para 2026 (−26% nas seções, −26% no saldo), e em ambos os anos é dominado pelo
interior do NE e do Norte — seções pequenas, rurais, indígenas e quilombolas, o mesmo perfil documentado em A12,
A27 e A31b. Se o padrão fosse fraude de 2026, teria de ter sido *maior* na eleição de 2022.

**O que fecharia.** Listas de habilitação (folhas de votação) das seções do corte B — o pedido LAI 07 e o
modelo para partidos já existem (`lai/`, A32 item 5; e `dados_locais/ne_secoes_troca_e_alta_sem_biom.csv` já é a
lista das 190); atas de troca de urna das 190 seções (TREs); e boletins impressos dessas seções para o braço a
jusante. Enquanto isso, o padrão medido é o de 2022, só que menor.

## 3.C. Síntese da rodada

| investigação | o que o dono quer dizer | o que os números sustentam | o que fecharia |
|---|---|---|---|
| A. empates/±1 | fraude "amarrando" o placar | **acaso puro explica e sobra**: obs./esp. 0,92 (empates) e 0,97 (±1) em 2026, ambos abaixo do nulo e piores em 2022 que em 2026; simetria p=0,789; troca de urna na taxa nacional | BUs impressos das 6.667 seções (braço a jusante); TI (a montante) |
| B. NE biom × troca × domínio | canal de votos movíveis no NE | correlação por taxa ≈ 0 (ρ=0,06); sobreposição de 2026 **menor** que a de 2022 no mesmo corte; conjunto 0–10 votos encolheu 26% | folhas de votação das 190 seções (LAI 07), atas de troca, BUs |

Nenhum número novo aqui altera o mapa de pontos cegos: o elo aberto continua sendo digitado→registrado (A19/A37),
e o instrumento que o fecha é o teste de integridade consolidado + coleta de BUs. O que esta rodada adiciona é
**contra-evidência de forma**: os dois padrões propostos como "gatilho" aparecem em 2022 em igual ou maior
intensidade.

---

# PARTE 4 — A objeção dos 20 anos (H20: mecanismo estrutural de longa data)

*30/10/2026. A objeção do dono é analiticamente correta: constância 2022/2026 não refuta uma técnica antiga — pode
datá-la. Testada com a série completa disponível: **2014, 2018, 2022, 2026** (T2; `parquet/bu_{ano}_t2.parquet`).
EXPLORATÓRIO. Script: `scripts/exploratorio/08_h20_serie_historica.py`; saídas:
`results/exploratorio/H20_serie_indicadores.csv`, `H20_permanencia_municipios_extremos.csv`.*

## 4.1. H20a — constância: a tabela-ano

Todas as medidas com os pares corretos por ano (Dilma×Aécio 2014; Haddad×Bolsonaro 2018; Lula×Bolsonaro 2022;
Lula×Flávio 2026). "Razão" = observado/esperado sob o nulo binomial por seção (p da zona, leave-one-out).

| ano | empates razão | ±1 razão | seções oponente 0–10 | saldo nelas | % no NE | saldo em seções PT≥80% (NE) | taxa sem-biom NE | saldo PT nacional |
|---|---|---|---|---|---|---|---|---|
| 2014 | 0,901 | 0,926 | **6.324** | **670.512** | 77,2% | **6.024.408** | s/ dado* | +3,53 M (Dilma venceu) |
| 2018 | **1,030** | **1,041** | **7.606** | **928.308** | 75,5% | **6.377.075** | 9,49% | **−10,68 M (Haddad perdeu)** |
| 2022 | 0,954 | 0,942 | 4.097 | 505.308 | 73,5% | 5.581.970 | 9,38% | +2,13 M (Lula venceu) |
| 2026 | 0,920 | 0,967 | **3.029** | **376.149** | 65,0% | **4.967.243** | 7,19% | +4,40 M (Lula venceu) |

\* `biom_nh` vem zerado em 2014 (campo não populado naquele ano); série válida 2018→2026.

**Leitura H20a: confirmada como constância.** Todos os indicadores existem nos quatro anos com a mesma ordem de
grandeza. E mais: o padrão é **monotonicamente decrescente** — seções de domínio extremo caem a cada eleição
(7.606 → 4.097 → 3.029), o saldo concentrado no NE cai (6,4 M → 5,0 M), e a taxa sem-biometria do NE cai (9,5% →
7,2%) conforme a biometria expande. Se é uma "técnica", é uma técnica em **encolhimento há 8 anos**, inclusive no
período em que o PT perdeu.

## 4.2. H20b — mobilidade geográfica: ferramenta móvel ou estrutura fixa?

Municípios "extremos" = top 5% por saldo do candidato do PT por apto (T2). Permanência entre eleições:

| par | permanecem da anterior |
|---|---|
| 2014→2018 | 53,0% |
| 2018→2022 | 78,5% |
| 2022→2026 | 76,0% |
| 2026 ∩ as três anteriores | **38,7%** (sob independência seria ~0,01%) |

**Leitura H20b: fixidez geográfica.** Uma ferramenta "ativada onde a disputa aperta" trocaria de território a cada
eleição; o observado são os **mesmos municípios** (interior do NE/Norte) há 12 anos, com 3/4 de permanência entre
eleições consecutivas. Isso é o que demografia estável (interiorização, seções pequenas, homogeneidade local)
produz; e é o contrário do que uma ferramenta oportunista produziria.

## 4.3. H20c — discriminação de vencedor

2018 é o ano-teste: o PT perdeu por 10,68 milhões — e é **o ano com os maiores valores da série** nas medidas de
domínio extremo (7.606 seções com Bolsonaro 0–10 votos; saldo de 928 mil nelas; razões de empate/±1 levemente
**acima** do nulo, 1,03–1,04, as únicas acima de 1). Se esses padrões fossem o mecanismo que decide eleições,
2018 é inexplicável: o "mecanismo" estava no máximo histórico no ano em que o suposto beneficiário perdeu feio.
**Leitura H20c: o padrão não discrimina vencedor.**

## 4.4. Pesquisas × resultado (série do repo, A7 + ancoras da Parte 1b)

Erro absoluto da pesquisa final contra o resultado: **2018: 0,13 p.p.; 2022: 1,1 p.p.; 2026: 2,6–2,8 p.p.** (os
dois últimos fora da margem declarada). Sob a leitura "a técnica é antiga e os números publicados sempre batem com
a pesquisa", o erro deveria ser pequeno em todos os anos — e 2026 é o maior da série. Esse é o **único indicador
que aponta na direção do dono**: ou as duas pesquisas finais de 2026 erraram ~2,7 p.p. na mesma direção (o maior
erro da série), ou mediram uma realidade diferente da publicada. As duas leituras cabem nos dados; a Parte 1b já
mostrou por que a pesquisa sozinha não decide.

## 4.5. Síntese — o que cada número sustenta e o que não sustenta

| hipótese | veredito exploratório | base |
|---|---|---|
| H20a constância | **confirma-se como estrutura estável** — e em declínio há 8 anos | tabela 4.1 |
| H20b mobilidade | **refutada a ferramenta móvel; confirmada a estrutura fixa** (76–78% de permanência; 38,7% nos 4 anos) | 4.2 |
| H20c discrimina vencedor | **refutada**: máximos da série em 2018, ano da derrota do PT por 10,7 M | 4.1, 4.3 |
| "pesquisas sempre batem" | **único ponto a favor da atenção**: 2026 é o maior erro da série (2,6–2,8 p.p.) | 4.4 |

**A leitura mais parcimoniosa** dos quatro fatos juntos é demografia e estrutura eleitoral do interior do
NE/Norte, com biometria expandindo e o fenômeno encolhendo. Para sustentar a leitura contrária (técnica antiga),
seria necessário explicar (i) por que o mecanismo foi máximo em 2018 e falhou, (ii) por que encolhe
monotonicamente, e (iii) por que só a pesquisa de 2026 destoa. **O que fecharia a questão não existe em dado
público histórico**: folhas de votação de anos anteriores não são públicas; as âncoras possíveis são as de sempre,
só que agora — teste de integridade consolidado (A37) e BUs impressos (a jusante). Gatilho novo registrado: o erro
de pesquisa de 2026 (2,6–2,8 p.p., fora da margem) é o único desvio da série que aponta para 2026 — entra na fila
de verificação como "explicar o erro das pesquisas finais de 2026" (coleta das séries históricas de erro dos
institutos, com fonte, para saber quão atípico é 2,8 p.p. na história recente; insumo externo).

---

# PARTE 5 — Teoria da rotação (30/10/2026)

*A tese do dono: as práticas antigas são reduzidas gradativamente (para parecer melhora) enquanto novas técnicas
entram com jitter, e a SOMA controla o resultado. **Posição registrada desta auditoria, compartilhada com o dono:
na forma geral a teoria é não-falsificável com dados internos** — "o declínio é a estratégia" explica qualquer
padrão, e um texto público deve dizer isso explicitamente, porque é o que a protege de desmonte retórico. **Mas ela
tem um núcleo testável**: rotação prevê componentes encolhendo com o resíduo total se mantendo ou migrando de
lugar; estrutura benigna prevê o total sumindo junto com os componentes. É isso que se testa aqui. EXPLORATÓRIO.
Script: `scripts/exploratorio/09_rotacao_residuo.py`; saídas: `results/exploratorio/ROT_*.csv`.*

## 5.1. Resíduo total por ano

Componentes recomputados dos parquets com o **mesmo método nos 4 anos** (T2, apuradas, sem exterior): c1 = seções
com oponente 0–10 votos; c2 = PT ≥ 80% dos válidos; c3 = turnout ≥ 95% (corte H5); c4 = sem-biometria > 30%
(corte A32; **só 2018+** — `biom_nh` não é populado em 2014); c5 = excesso A31 versionado (teto incondicional por
ano, de `A31_municipios.csv` — é teto de modelo, não saldo bruto; cobertura declarada). c1–c4 se sobrepõem; por
isso o total usa a **união disjunta por seção**.

| ano | c1 saldo | c2 saldo | c3 saldo | c4 saldo | **união c1–c4 (disjunta)** | c5 excesso A31 |
|---|---|---|---|---|---|---|
| 2014 | 670.512 | 6.933.821 | 25.869 | s/ dado | **6.945.085** | 7.843.578 |
| 2018 | 928.308 | 7.108.559 | −16.311 | 126.043 | **7.077.808** | 2.975.220 |
| 2022 | 505.308 | 6.239.447 | 6.636 | 282.930 | **6.302.810** | 2.038.696 |
| 2026 | 376.149 | 5.604.858 | 37.737 | 13.840 | **5.614.724** | 2.193.368 |

**Leitura:** o resíduo total **cai junto com os componentes** (−21% do pico de 2018 para 2026 na união; o excesso
de A31 cai de 7,8 M para ~2,1–2,2 M e fica no nível de 2022). A previsão da rotação (total mantido enquanto
componentes encolhem) **não se observa**; a previsão da estrutura benigna, sim. Ressalvas honestas: (i) c1–c4 são
saldos brutos de conjuntos, não excessos sobre nulo — incluem votos legítimos de reduto; (ii) a cobertura de c4 é
só 2018+; (iii) c5 mede outra coisa (teto de modelo A31). Nada disso muda a direção: nenhuma leitura mostra o
total se sustentando enquanto as partes caem.

## 5.2. Estabilidade de onde a margem é construída

Por ano, distribuição municipal da contribuição à margem (saldo municipal, T2):

| ano | Gini da contribuição abs. | top-100 municípios (% do saldo abs.) | Spearman do ranking vs. eleição anterior |
|---|---|---|---|
| 2014 | 0,732 | 36,4% | — |
| 2018 | 0,725 | 35,4% | 0,932 |
| 2022 | 0,686 | 28,5% | 0,974 |
| 2026 | 0,676 | 27,6% | **0,986** |

**Leitura:** a geografia da margem fica **mais estável a cada eleição** (correlação de rankings 0,93 → 0,99) e
**menos concentrada** (Gini e top-100 caindo). A rotação prevê oscilação geográfica (a técnica migra para onde a
disputa aperta); o observado é o oposto — estende H20b da periferia (seções extremas) para a margem total.

## 5.3. O teste do jitter

Sinal das variações ano a ano por componente (2014→2018→2022→2026):

| componente | sinais | mudanças de sinal | leitura |
|---|---|---|---|
| c1, c2, união c1–c4 | **+ − −** | 1 | pico em 2018 (ano da derrota do PT), declínio depois — não é jitter, é o pico de 2018 |
| c3 (turnout ≥95%) | − + + | 1 | sobe depois de 2018, mas são centenas de seções e dezenas de milhares de votos — ordem pequena |
| c4 (sem-biom >30%) | + − | 1 | colapsa em 2026 (282.930 → 13.840 de saldo) com a biometria expandindo |
| c5 (excesso A31) | − − + | 1 | cai até 2022, leve alta em 2026 dentro do mesmo nível |

Nenhum componente oscila (+−+−); todos têm no máximo **uma** mudança de sinal, e o padrão dominante é "máximo em
2018, declínio desde então". Jitter (sobe-e-desce de compensação) **não aparece**.

## 5.4. O fio que sobrou: erro das pesquisas

Série (repo, A7 + Parte 1b): **2018: 0,13 p.p.; 2022: 1,1 p.p.; 2026: 2,6–2,8 p.p. (as duas finais, fora da
margem declarada)**. É o único desvio que aponta para 2026 e é compatível com a rotação ("2026 introduziu algo que
as pesquisas não capturaram") — mas também com um erro de pesquisa grande. Para virar teste: (i) série histórica
completa de erros das pesquisas finais Ibope/Datafolha/AtlasIntel (2002–2026) **com fonte** (registros TSE +
arquivos dos institutos; o repo hoje tem só 4 pontos); (ii) erro por UF/região se os institutos publicarem quebra
(a rotação geográfica implicaria erro concentrado onde a técnica atuou); (iii) boca de urna do T2 de 2026 (âncora
do dia, fora do software). Até lá: **INCONCLUSIVO, documentado, sem conversão em evidência**.

## 5.5. Síntese e redação para o portal

O que os números sustentam: (a) o resíduo total cai junto com os componentes (−21% do pico); (b) a geografia da
margem é cada vez mais estável (Spearman 0,93→0,99) e menos concentrada; (c) não há jitter — nenhuma oscilação
+−+− em seis componentes; (d) o único desvio a favor da tese é o erro das pesquisas de 2026, indecidível sem a
série histórica dos institutos.

O que não sustentam: não provam que nunca existiu nada — dados internos são à prova de inversão coerente por
construção (A19/Parte 1b), e a teoria da rotação **na forma geral não é falsificável com dados internos**: "o
declínio é a estratégia" acomoda qualquer série.

**Redação honesta sugerida para o portal** (a hipótese com previsão testável, o que a refutiria, e o aviso de
não-falsificabilidade):

> *"A hipótese de uma técnica rotativa de longa data não pode ser refutada com os arquivos que o próprio sistema
> publica: se a premissa é que os arquivos são coerentes por construção, nenhuma consistência interna a exclui.
> O que os dados internos permitem testar é o núcleo quantitativo da tese — e ele não se confirma: o total medido
> dos conjuntos apontados cai junto com as partes (−21% desde 2018), a geografia da margem é a mais estável da
> série, e não há oscilação compensatória. O que decidiria a questão está fora dos arquivos: o relatório
> consolidado do teste de integridade (TCU), boletins impressos fotografados contra o BWeb (alteração depois da
> impressão), e a série histórica de erros das pesquisas finais. Enquanto essas âncoras não forem trazidas, a
> posição desta auditoria é: hipótese aberta por construção, núcleo testável não confirmado."*

## Saídas desta rodada (30/10, rotação)

- `scripts/exploratorio/09_rotacao_residuo.py`
- `results/exploratorio/ROT_componentes_por_ano.csv`, `ROT_geografia_margem.csv`, `ROT_jitter.csv`

Da rodada (30/10, H20):

- `scripts/exploratorio/08_h20_serie_historica.py`
- `results/exploratorio/H20_serie_indicadores.csv`, `H20_permanencia_municipios_extremos.csv`

Da rodada anterior (30/10, empates/NE):

- `scripts/exploratorio/06_empates_margem1.py` → `results/exploratorio/A_empates_resumo.csv`,
  `A_distribuicao_margem_obs_esp.csv`, `A_empates_troca_urna.csv`
- `scripts/exploratorio/07_nordeste_biom_troca.py` → `results/exploratorio/B_nordeste_biom_troca.csv`

## Saídas das rodadas anteriores (29/10)

- `scripts/exploratorio/03_gatilhos_intersecoes.py`
- `results/exploratorio/empilhamento_nas_secoes_zero_voto.csv`
- `results/exploratorio/intersecoes_entre_conjuntos_secao.csv`
- `results/exploratorio/empilhamento_por_municipio_distribuicao.csv`
- `results/exploratorio/empilhamento_por_municipio_2mais.csv` (109 municípios com 2+ bandeiras, com as bandeiras)
- `results/exploratorio/empilhamento_por_uf.csv`
- `docs/propostas/gatilhos-e-inversao.md` (este memorando: tese da inversão + pré-registro A37 + empilhamento +
  esboço A38 + **PARTE 1b: cenário de inversão total, A37b**)

Rodada da inversão total (29/10):
- `scripts/exploratorio/04_inversao_total_ancoras.py` → `results/exploratorio/inversao_total_ancoras.csv`
  (eixo T1→T2 sob as duas hipóteses; erros de pesquisa contra o publicado e contra o espelho; escala da margem)
- `scripts/exploratorio/05_a37b_presidente_x_deputado.py` (pré-registrado, **pendente de insumo**: falha com
  NãoExecutado sem os parquets `cargos_*`)
- correção do braço "boletim impresso" de A37 e da tabela de âncoras (montante vs. jusante do BU)
