# Propostas de novos pontos cegos e testes (memorando exploratório)

Data: 2026-10-29. Autor: sessão exploratória (subagente). **Tudo neste documento é exploratório**: os números
calculados abaixo foram produzidos depois de ver os dados e **não têm veredito formal** — o projeto pré-registra
antes de concluir. Scripts novos em `scripts/exploratorio/`, saídas em `results/exploratorio/`.

## Restrição de ambiente (declarada)

Nesta máquina **não existem** os diretórios de dados preparados (`parquet/`, `parquet2/`, `urna_out/`, `dados_tse/`,
`bu*/`); só há os agregados versionados em `results/` e os arquivos pequenos de `data/`. Por isso vários candidatos
ficam na classe **TESTÁVEL COM OS DADOS DO PROJETO, BLOQUEADO NESTA MÁQUINA**: o teste roda sem nenhum dado externo
assim que os parquets estiverem presentes, e o pré-registro abaixo já deixa hipótese nula, métrica, regra de decisão
e placebos fixados **antes** da execução.

## Tabela-resumo

| # | candidato | status | teto em votos de margem |
|---|---|---|---|
| 1 | duração do voto por eleitor (habilitação → confirmação) | TESTÁVEL COM DADOS DO PROJETO, bloqueado nesta máquina (faltam `urna_out/`); viabilidade do insumo confirmada; **virou pré-registro A34** | a definir pelo desenho (seções com mediana anômala × votos) |
| 2 | seções apuradas por ata/recuperação | TESTÁVEL COM DADOS DO PROJETO (cruzamento BWeb × arquivos de urna), bloqueado nesta máquina; parte documental: LAI | a medir |
| 3 | voto no exterior e em trânsito | **RODADO (exploratório)** sobre agregados versionados; elo cego de cadeia de papel delimitado | saldo exterior pró-Lula = 28.657 votos = **0,65% da margem**; universo 371.651 válidos = 8,4% da margem |
| 4 | verificação da assinatura digital dos BUs | **QUANTIFICADO** sobre `cert_RR_2026.csv`; vira plano de trabalho, não teste estatístico | cobre os 12 elos de G1; não é mensurável em votos |
| 5 | extremos novos (zero BN em seção grande; comparecimento 100%; unanimidade) | parcialmente **RODADO** dentro do conjunto A12b; universo geral bloqueado nesta máquina; **virou pré-registro A35** | dentro das 106 zero-oponente: troca ≤ 5.401 votos de margem (0,12%) |
| 6 | municípios com TODAS as seções novas | TESTÁVEL COM DADOS DO PROJETO, bloqueado nesta máquina; caso análogo já documentado (TSE 73709, A31) | a medir |
| 7 | liberação manual × duração/horário do voto | depende do item 1 (A34); incorporado ao pré-registro A34 como modelo M4 | — |
| 8 | cobertura demográfica (A20/A20b sem LAI) | PRECISA DE DADO EXTERNO/LAI — especificado | — |

---

## 1. Duração da sessão de voto por eleitor (habilitação → confirmação)

**Pergunta.** Qual a distribuição, por seção-dia, do tempo entre "Eleitor foi habilitado" e "Voto confirmado para
[Presidente]" do mesmo eleitor? Votação "expressa" em massa (mediana de poucos segundos por seção inteira) seria
incompatível com o ato físico de votar e indicaria registro de votos sem eleitor.

**Por que importa.** Todos os testes temporais existentes medem **intervalos entre eventos** (A21: intervalos entre
habilitações e último voto; A32/A32b: intervalos que precedem liberações manuais e rajadas). Nenhum mede a **duração
do ato de votar**. Uma urna operada por alguém que digita votos sem eleitor produziria durações muito curtas e
homogêneas — padrão diferente de fila rápida (que encurta intervalos, não durações).

**Dados.** Os logs públicos têm os dois eventos com horário (`urna_parse.py`: `PAT_HAB = "Eleitor foi habilitado"`,
`PAT_CONF = "Voto confirmado para [Presidente]"`, ambos com timestamp; já parseados por `08_arquivos_urna.py`).
Como cada seção tem uma urna, o pareamento habilitação → próximo voto confirmado do mesmo log identifica a duração
do eleitor (ambíguo apenas em habilitações sem voto — 256 seções com mais habilitações que votos, já medidas em A5).
Bloqueio local: os parquets de log (`urna_out/`) não estão nesta máquina.

**Método e status.** Pré-registro **A34** abaixo. Mediana nacional conhecida de contexto (A32, intervalo que
**precede** cada habilitação): 123–156 s para manual e 63–95 s para biométrica — ou seja, o ciclo completo de um
eleitor leva ~1–2,5 min; durações medianas de voto abaixo de ~20–30 s em massa destoariam desse ritmo.

**Teto.** Seções com mediana de duração abaixo do limiar × votos válidos (fator 2, se atribuídos a troca), contra os
placebos. Só é calculável após rodar.

## 2. Seções apuradas por ata / recuperação (não transmitidas no dia)

**Pergunta.** Quantas seções de 2026/T2 entraram na totalização por digitação de ata no TRE (urna não transmitiu),
quantos votos somam, e o efeito líquido contra a margem?

**Por que importa.** É o único caminho em que o número que entra no Sistot **não** vem do arquivo assinado da urna:
passa por papel (ata) e digitação manual no TRE. O dossiê trata contingência (A6, urna substituída) mas não delimita
a apuração por ata como elo separado.

**Dados.** TESTÁVEL COM DADOS DO PROJETO: seção apurada por ata deve aparecer no BWeb **sem** arquivo de urna
correspondente no zip público da UF (o BU digital não existe). O cruzamento cobertura BWeb × arquivos de urna já foi
parcialmente feito em A4/A5 (as 62 divergências log × BU eram todas urnas de contingência — que **transmitiram**;
não é a mesma coisa que ata). O produto TSE "seções totalizadas por ata" (publicado por TRE em 2022) e as atas
digitalizadas são o dado confirmatório: LAI ao TSE (espelho do `lai/`) ou publicação dos TREs. Bloqueio local: sem
`dados_tse/` e `urna_out/`. Registro empírico já existente: seções "Anulada e apurada em separado" são raríssimas
(2 em Salvador/2018, `A31_excluidos.csv`).

**Teto.** Soma dos votos válidos dessas seções (fator 1) e saldo líquido (fator 2 se troca). A medir.

## 3. Voto no exterior e em trânsito — RODADO (exploratório)

**Pergunta.** Quantos votos válidos para presidente no exterior em 2026/T2, como % da margem de 4.430.191, e qual o
saldo líquido?

**Por que importa.** A cadeia do exterior é outra: sem BU de urna eletrônica na maioria dos países (voto em cédula,
contagem manual e digitação), nenhum dos testes A4/A5/A21/A32 (arquivos de urna, logs) se aplica a ZZ; A10 trata o
exterior só como recorte descritivo. É um elo cego separado que o dossiê não delimita.

**Dados e método.** Por diferença de totais versionados: total oficial BWeb 2026/T2 (H9, inclui ZZ) **menos** total
das seções apuradas do Brasil (A27, `SG_UF != ZZ`). Script: `scripts/exploratorio/01_exterior_margem.py`; saída:
`results/exploratorio/exterior_2026_t2_por_diferenca.csv`.

**Resultado (exploratório, sem veredito).**

| grandeza | valor |
|---|---|
| seções no exterior (A10, 2026/T2) | 1.308 |
| válidos dos dois finalistas no exterior | **371.651** (8,4% da margem) |
| Lula | 200.154 (53,855%) |
| Flávio | 171.497 |
| saldo líquido pró-Lula | **28.657 votos = 0,65% da margem** |
| comparecimento exterior | 41,6% (vs. 81,0% Brasil) |

Conferência interna: o share 53,855% obtido por diferença **bate exatamente** com o recorte exterior de A10
(calculado por outro script, de outro arquivo) — os dois caminhos concordam. Brancos e nulos do exterior não
constam em nenhum dos dois arquivos-fonte.

**Leitura de ponto cego.** Mesmo que **todos** os 371.651 válidos do exterior mudassem de lado (irreal), o efeito
seria 8,4% da margem; o saldo real é 0,65%. O exterior **não fecha** a margem de 2026 — mas o elo continua cego:
nenhum artefato público (BU, RDV, log, assinatura) cobre ZZ, e a verificação depende de atas de contagem manual por
país (LAI ao TSE: atas de apuração do exterior; os TREs não têm jurisdição). Voto em trânsito é urna comum
(transmissão normal), já coberto pelos elos G1.

## 4. Verificação da assinatura digital dos BUs — QUANTIFICADO

**Pergunta.** Quantos BUs, quantos certificados distintos, e o que exatamente falta para verificar a assinatura?

**Estado medido** (`results/fase2/cert_RR_2026.csv`, produzido por `scripts/13_cert_urna.py`):

| item | valor |
|---|---|
| seções com certificado lido | 1.519 (todas as de Roraima, 2026/T2) = 0,30% das 499.205 |
| certificados com CN = urna do BWeb | 1.519 (100%) |
| validade cobrindo o dia da eleição | 1.519 (100%) |
| autoridades emissoras distintas | **2** (`AC UE2022`, `AC UE2020`) |
| OID da chave | `1.3.6.1.4.1.44588.2.1` (OID privado TSE) em 100% |
| tamanho da chave pública | 66 bytes (curva de 521 bits) em 100% |
| assinatura criptográfica verificada | **0** (nenhuma) |

**O que falta, concretamente.** (i) A **especificação da curva** (parâmetros do primo, a, b, gerador) e do esquema
de assinatura sob o OID 1.3.6.1.4.1.44588.2.1 — documento TSE "ESPEC-UE" / scripts de exemplo do kit de
desenvolvimento da urna, hoje atrás de HTTP 403 para automação; (ii) o **certificado da AC emissora** (`AC UE2022`,
`AC UE2020`) com chave pública — publicável pelo TSE sem sigilo; (iii) implementação da curva (bibliotecas padrão
não suportam o OID; OpenSSL permite curva explícita custom).

**Plano com esforço estimado.** (a) LAI/pedido formal ao TSE: especificação criptográfica + certificados das ACs de
urna + scripts de verificação de exemplo — 1 pedido, sem custo técnico; (b) com a especificação em mãos: implementar
verificação ECDSA-sobre-curva-explícita em Python (`cryptography` aceita curva custom via `EllipticCurve`) —
~2–4 dias de trabalho; (c) rodar sobre as 1.519 seções de RR já baixadas (~1 hora) e estender à amostra A4/A5
(14.067 seções de 2026 já coletadas; os zips de UF inteira pesam dezenas de GB). **O que isso fecha:** os elos 6, 7
e 8 da cadeia G1 deixam de depender de confiança nos arquivos publicados; combinado com o hash-vínculo já conferido
(A4: lista assinada inclui BU, RDV, imagem e log), a assinatura verificada em uma amostra estratificada transforma
A18 de "NÃO EXECUTADO PARCIAL" em teste com cobertura declarável.

## 5. Valores extremos novos — PARCIALMENTE RODADO

**Pergunta.** Seções com zero brancos+nulos em seção grande, comparecimento = 100% dos aptos, e 100% dos válidos em
um candidato — o que a análise existente já cobre e o que falta?

**O que já existe.** A12 cobre zero voto no oponente (106 seções em 2026/T2, série histórica, esperado por
Poisson-binomial); A12b cobre a **tripla zero** (zero oponente **e** zero brancos+nulos) contra o esperado da
vizinhança (observado 29 vs. esperado 20,4; razão 1,42 — dentro da faixa histórica de 1,15–2,24); o relatório
original cobre unânimes ≥30 válidos. **Não coberto:** zero BN em seção grande **no universo geral** (não só nas
zero-oponente) e comparecimento exato de 100%.

**Rodado agora (exploratório)** — `scripts/exploratorio/02_extremos_zero_bn_turnout100.py`, saída
`results/exploratorio/zero_bn_por_tamanho_nas_106_zero_oponente.csv`: dentro das 106 seções zero-oponente de
2026/T2, **12 têm zero BN e comparecimento ≥ 100** — 8 indígenas (PA, MT, RR), 4 "escola_outro" rurais (MA, AM,
MT); a maior tem 365 votantes; **nenhuma** tem comparecimento = 100% dos aptos (só 1 das 106 tem, e não é
zero-BN). Teto de pior caso (troca) dentro das 106: 5.401 votos de margem = 0,12% (já publicado por A12b; aqui
reconfirmado por tamanho: cai para 0,043% acima de 200 votantes). O conjunto "zero BN grande" dentro das
zero-oponente é pequeno, remoto e coerente com o perfil histórico. **Bloqueio:** a pergunta simétrica e geral
(zero BN em seção ≥100 votantes em **todas** as 497.897 seções; turnout exato 100%) exige o parquet — **virou
pré-registro A35**.

## 6. Municípios onde TODAS as seções são novas

**Pergunta.** Quantos municípios de 2026 têm 100% das seções criadas pós-2022, qual o perfil e o efeito?

**Por que importa.** H5/A27 tratam seção nova individualmente e local novo; um município **inteiro** sem seção
antiga não tem controle histórico nenhum — nem o efeito fixo de local salva.

**Dados e status.** TESTÁVEL COM DADOS DO PROJETO (BWeb 2022 × 2026 por seção, mesmo insumo de A27), bloqueado nesta
máquina. Já há um caso análogo documentado: município TSE 73709 (BOA ESPERANÇA DO NORTE/MT, instalado entre 2022 e
2026), com 13 seções — 5 vindas de Sorriso, 4 de Nova Ubirãta e 4 novas (Adendo 13 de `00_preregistro.md`). O teste
novo é o **censo completo** desses municípios + comparação com municípios vizinhos da mesma UF (perfil do T1,
comparecimento, swing). Teto: soma dos válidos (fator 2 se troca).

## 7. Liberação manual × duração/horário do voto

Depende do insumo do item 1. Incorporado ao pré-registro A34 como modelo M4 (duração mediana ~ taxa manual da seção,
EF de local, controle do T1, placebo 2022). Sem os logs nesta máquina, nada a calcular agora. O que já existe: A21
(intervalos × voto) e A5 (tardio × Lula) — não medem duração nem cruzam manual × duração.

## 8. Cobertura demográfica — o que falta para A20/A20b sem LAI

**Falta exata e órgão:**
1. **Perfil de comparecimento/abstenção por faixa etária do 2º turno de 2026** (TSE — o produto público saiu em
   21/10/2026 só com o T1; A9 T1→T2 2026 está NÃO EXECUTADO por isso). Órgão: TSE/SEAD; basta a **publicação do
   produto**, nem LAI precisa — o prazo histórico é poucas semanas após o turno.
2. **Perfil do eleitorado por seção com data de corte pós-T2 2026** (TSE; o atual é de 14/07/2026) — para A20b-idosos
   com o cadastro efetivo do 2º turno. Órgão: TSE.
3. **Ano de nascimento do votante por seção** — NÃO EXISTE em dado público por desenho (sigilo); A21 registrou como
   NÃO EXECUTÁVEL. Nenhum LAI pode entregar isso sem quebrar sigilo; a aproximação legal é o item 1.
4. Comunicação de óbitos ao cadastro (Registro Civil × TSE, art. 71, §3º CE) — só auditável por entidade
   fiscalizadora; ponto cego permanente (já declarado na matriz, elo 3).

---

## PRÉ-REGISTRO A34 — duração do voto por eleitor (habilitação → confirmação)

*Texto pronto para o dono do repo revisar ANTES de rodar. Estilo dos adendos de `00_preregistro.md`.*

**Declaração de ordem (a preencher na assinatura do adendo).** Antes deste adendo vi apenas: o formato do log
(eventos "Eleitor foi habilitado" e "Voto confirmado para [Presidente]" com horário, na mesma urna), os intervalos
agregados de A21/A32/A32b e os resultados de A5. **Não vi** nenhuma duração habilitação→confirmação, por seção ou
agregada.

**Unidade e fontes.** Seção-dia, na mesma amostra de A4/A5/A21/A32 (estratificada + Roraima inteira), 2022 e 2026,
T1 e T2 (o log do T2 traz os dois dias). Seção-dia entra se o log fecha com o comparecimento do BU a até 5% e tem
≥100 habilitações (mesma regra do Adendo 11a, item 3).

**Definições.** Duração de um voto = tempo entre o evento "Eleitor foi habilitado" e o **primeiro** "Voto
confirmado para [Presidente]" posterior a ele no mesmo log. Habilitação sem voto posterior (a urna registra 256
seções com mais habilitações que votos, A5) fica sem duração e é contada à parte. Métricas por seção-dia: **D1**
mediana da duração; **D2** percentil 1 da duração; **D3** fração de durações < 20 s; **D4** desvio-padrão da
duração (homogeneidade: voto "de máquina" teria dispersão quase nula); **D5** fração de habilitações sem voto.

**Hipótese nula.** As métricas D1–D5 de 2026/T2 são iguais às de 2022/T2 nas mesmas seções (teste pareado com efeito
fixo de seção, erro padrão agrupado por município) e a distribuição de D3 por seção de 2026 está dentro do intervalo
[mín, máx] dos placebos (2022/T1, 2022/T2, 2026/T1).

**Modelos de associação (simétricos PT/oponente).** (M1) participação de Lula no T2 ~ D3 da seção + participação no
T1, EF de local, EP agrupado por local; placebo: mesma regressão em 2022/T2. (M2) comparecimento T2 ~ D3 +
comparecimento T1, idem. (M3, descritivo, sem placebo) variação 2022→2026 de D1. (M4 — incorpora o candidato 7)
D1 da seção ~ taxa de liberação manual do BU + D1 do T1, EF de local; placebo 2022. Amostra principal: estrato R +
Roraima (seleção independente do desfecho); sensibilidade: todos os estratos, rotulada.

**Regra de decisão.** Veredito pelas regras do `Registro` (interseção-união contra cada placebo, p unilateral de
excesso, Holm sobre a família A34). "Excesso" para D3 = fração de seções de 2026/T2 com D3 acima do percentil 99 de
2022/T2 **superior** a 1% por mais de 2 erros padrão binomiais. **Previsão sem manipulação:** D1 mediana entre ~40 s
e ~2 min (coerente com os intervalos de A32: ciclo completo 1–2,5 min), D3 ≈ 0 nos dois anos, coeficientes de M1/M2
dentro dos placebos.

**Teto em votos de margem (teto de pior caso, não estimativa).** Seções de 2026/T2 com D3 acima do limiar do
percentil 99 de 2022: (a) todos os votos válidos dessas seções atribuídos a um lado, fator 1; (b) saldo líquido × 2.
Ao lado, a mesma conta em 2022/T2 como referência de ruído.

**Lugarbos.** 2022/T1, 2022/T2 e 2026/T1 nas mesmas seções (o log do T2 traz o T1). Lugarbo de forma: aplicar o
mesmo teste à duração medida do **lado errado** (tempo do voto confirmado até a próxima habilitação — inclui fila,
deve ser longo e igual nos dois anos; se o teste acusar excesso aí, o desenho está quebrado).

**Limites declarados.** O pareamento habilitação→próxima confirmação é determinístico só porque há uma urna por
seção; em seções com voto não concluído a duração fica censurada (contada em D5). Cobertura = a de A24 ("N seções
de 499.205, parcial"); extrapolação nacional só como teto, com o aviso de sempre. Não identifica eleitores.

## PRÉ-REGISTRO A35 — extremos no universo geral (zero BN em seção grande; comparecimento exato de 100%)

**Declaração de ordem.** Antes deste adendo vi: A12, A12b (tripla zero nas zero-oponente, 106 seções), H5 (≥95%) e,
em exploração, que dentro das 106 há 12 seções com zero BN e comparecimento ≥100 (8 indígenas, máx. 365 votantes) e
1 seção com comparecimento ≥ aptos. **Não vi** as contagens análogas no universo geral das 497.897 seções.

**Definições (2026/T2, seções apuradas, sem exterior).** E1: seções com brancos+nulos = 0 e comparecimento ≥ 100
(limiares de sensibilidade: ≥ 200, ≥ 400). E2: seções com comparecimento = QT_APTOS (turnout exato de 100%, tolerância
0; sensibilidade: comparecimento/aptos ≥ 0,995). E3: seções com 100% dos **votos nominais** (não só válidos) em um
candidato, comparecimento ≥ 30.

**Hipótese nula.** A razão observado/esperado de E1 em 2026/T2 está dentro do intervalo dos placebos (2014, 2018,
2022 — T1 e T2), com esperado por Poisson-binomial: para cada seção, p0 = (1 − r)^n, r = taxa de brancos+nulos das
demais seções do mesmo local (leave-one-out; local de uma seção → município), n = comparecimento — **o mesmo
estimador de A12b**, agora aplicado a todas as seções, não só às zero-oponente. Para E2, o esperado vem do modelo de
comparecimento da própria seção: binomial com p = taxa de comparecimento do local vizinho e n = aptos (declarado
como aproximação; abstenção não é i.i.d. — por isso E2 é secundário e reportado só por razão obs/esp, sem p). E3 já
é coberto por A12/A12b para válidos; a extensão a nominais é contagem pura, sem teste.

**Regra de decisão.** Interseção-união: razão obs/esp de 2026/T2 supera **cada** placebo por mais de 2 erros padrão
(bootstrap por município, 1.000 reamostragens, semente 20261029) = EXCESSO; dentro da faixa histórica = dentro do
esperado. Holm sobre a família {E1, E2, E3}. Caracterização obrigatória das seções sinalizadas: UF, município, tipo
de local (classificação de A27), aptos, histórico 2018/2022 da mesma seção.

**Teto em votos de margem (pior caso, não estimativa).** E1/E3: votos do candidato majoritário nessas seções, fator
1; troca esperada pela vizinhança × 2, fator 2. E2: (comparecimento − mediana do local) × 1. Os três ao lado do
mesmo cálculo para 2022/T2.

**Lugarbos.** 2014/T2, 2018/T2, 2022/T2 e 2026/T1 com o mesmo estimador. Lugarbo de simetria: as mesmas contagens
para o lado do oponente (E3 já é simétrico por construção).

**Limites.** O esperado de E1 herda o viés conhecido de A12b em anos com terceiros relevantes (corrigido pelo
placebo de mesmo ano, não pelo de 2026); locais de seção única usam r do município (menos preciso). E2 é fraco por
desenho (abstenção correlacionada dentro do local infla p0) e entra só como descritivo com razão.

---

## O que não virou pré-registro, e por quê

- **Candidato 2 (atas):** falta primeiro o censo de cobertura BWeb × arquivos de urna (caracterização, não teste de
  hipótese); o pré-registro faz sentido depois de saber quantas seções são — se forem dezenas, teste de associação;
  se forem milhares, teste + teto. Rascunho: contagem nacional por UF e TRE, votos somados, comparação do saldo
  líquido dessas seções contra seções vizinhas do mesmo município (EF de município, controle do T1, placebo 2022).
- **Candidato 6 (municípios 100% novos):** mesma lógica — primeiro o censo; pré-registro depois da contagem.
- **Candidato 3 (exterior):** já tem número; como elo cego, o fechamento é documental (atas do exterior via LAI),
  não estatístico.
- **Candidato 4 (assinatura):** é plano de engenharia + pedido de documento, não hipótese estatística.
