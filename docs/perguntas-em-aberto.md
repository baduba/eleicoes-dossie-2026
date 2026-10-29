# Perguntas em aberto: o que os testes não conseguiram explicar nem confirmar

> **Antes das lacunas, o resultado verificado:** 0 divergências na cadeia RDV–BU–BWeb–totalização; o excesso medido somado é pequeno diante da margem e nenhum teste encontrou efeito capaz de alterar o resultado. Números na [página inicial](index.md).


**Não são evidências de manipulação. São lacunas. Se você tem dados ou método para fechar alguma, contribua.**

Cada cartão traz a pergunta, a situação, a direção do efeito (a favor de quem, se houver), o teto em votos de margem com a ressalva na mesma linha e o que fecharia a questão. Dentro de cada bloco, a ordem é pelo tamanho do que a resposta poderia mudar (maior teto ou maior ponto cego primeiro). Os tetos são limites superiores sob o pior caso; a margem é de 4.430.191 votos de margem.

### a) Resíduos sem causa identificada (testes executados, inconclusivos)

<a id="a-a20b-part"></a>
> **Nas seções com mais eleitores de 80 anos ou mais, a participação de Lula e de Flávio difere da dos anos anteriores?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula (teto) ou de Flávio (lado simétrico)  
> Teto: **teto de pior caso, não estimativa: 1.787.533 votos de margem (40,35% da margem)** (o coeficiente de 2026 fica dentro do intervalo dos placebos e a estimativa central é negativa para Lula; o teto vem da dispersão entre os anos de comparação; o lado a favor de Flávio tem teto de 790.398)  
> O que fecharia: Mais anos de comparação com o perfil do eleitorado por seção e as listas de habilitação das seções com mais idosos.  
> [Página técnica](fase3.html#a20b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-part%20A-A20b-part)

<a id="a-h1-s0"></a>
> **Onde há mais liberação manual de eleitor, Lula vai melhor? O teste não tem precisão para responder.**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula  
> Teto: **teto de pior caso, não estimativa: 1.337.198 votos de margem (30,18% da margem)** (teto vem da imprecisão do teste, sem efeito medido)  
> O que fecharia: Listas assinadas de habilitação por seção (folhas de votação) e o log de todas as seções, não só da amostra.  
> [Página técnica](residuos.html) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H1-S0%20A-H1-S0)

<a id="a-a22"></a>
> **O voto para presidente combina com o voto para governador na mesma seção, como em 2022 e 2018?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Flávio ou de Lula (lados simétricos)  
> Teto: **teto de pior caso, não estimativa: 548.671 votos de margem (12,38% da margem)** (variante exploratória (Adendo 9b), só AM e DF, pouco poder; vale só para os votos dessas duas UFs; o lado a favor de Lula tem teto de 169.390; a linha oficial de A22 é NÃO EXECUTÁVEL (nenhuma UF elegível pela regra registrada))  
> O que fecharia: Os votos por candidato em todos os cargos por seção nas 27 UFs, com uma regra de alinhamento definida por quem conhece as alianças locais; ou deputados federais por partido nas UFs sem 2º turno de governador.  
> [Página técnica](fase3.html#a22) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A22%20A-A22)

<a id="a-a20"></a>
> **Há mais eleitores muito idosos aptos e votando do que a população do Censo comportaria?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 459.099 votos de margem (10,36% da margem)** (o teto é o comparecimento 80+ acima das taxas de 2022; o mesmo aumento aparece nas faixas de 70 a 79 anos)  
> O que fecharia: Cruzamento do cadastro com o registro civil de óbitos, por entidade fiscalizadora; perfil do eleitorado por seção, não só por zona.  
> [Página técnica](fase3.html#a20) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20%20A-A20)

<a id="a-a20b"></a>
> **Nas seções com mais eleitores de 80 anos ou mais, o comparecimento do 2º turno sobe mais do que em 2022 e 2018?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 241.008 votos de margem (5,44% da margem)** (linha suplementar do Adendo 9d (só placebos com o mesmo controle); a linha original, com um comparador de outra especificação, dá 4,07 milhões; o coeficiente de participação de Lula nessas seções é negativo)  
> O que fecharia: Listas assinadas de habilitação das seções com mais idosos e o cruzamento do cadastro com o registro civil de óbitos, por entidade fiscalizadora.  
> [Página técnica](fase3.html#a20b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b%20A-A20b)

<a id="a-a31b"></a>
> **Por que 748 dos 5.357 municípios (14,0%) tiveram o ganho de Flávio entre os turnos de +1 voto ou menos, quase todos no Nordeste e no Norte?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 234.746 votos de margem (5,30% da margem)** (a fração de 14,0% é compatível com o crescimento nacional do oponente em 2026 (esperado de 13,2% a 15,4% com 2018 e 2022 deslocados); 70,6% desses municípios tiveram queda de comparecimento; o teto é todo o déficit de Flávio em relação ao crescimento da UF atribuído a troca de voto, e o excedente sobre o que o deslocamento nacional reproduz é 0; **o teste não distingue troca de voto de abstenção seletiva**)  
> O que fecharia: Boletins impressos das seções dos 20 municípios com maior perda de Flávio (lista em `results/fase3/A31b_20_secoes.csv`) e as listas de habilitação.  
> [Página técnica](fase3.html#a31b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A31b%20A-A31b)

<a id="a-a10"></a>
> **Urnas do modelo mais novo (UE2022) votam diferente das demais dentro do mesmo local?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula  
> Teto: excesso medido: 56.317 votos de margem; **teto de pior caso, não estimativa: 137.809 votos de margem (3,11% da margem)**  
> O que fecharia: Mais seções com o modelo novo em 2022 para servir de comparação, ou o código de carga por urna (pedido LAI 02).  
> [Página técnica](resultados-fase2.html#a10) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A10%20A-A10)

<a id="a-h1-fl"></a>
> **Onde há mais liberação manual, Flávio vai melhor do que no 1º turno prevê?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Flávio  
> Teto: excesso medido: 101.285 votos de margem; **teto de pior caso, não estimativa: 122.543 votos de margem (2,77% da margem)**  
> O que fecharia: Folhas de votação assinadas por seção e relatos de fiscais.  
> [Página técnica](residuos.html) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H1-FL%20A-H1-FL)

<a id="a-h6"></a>
> **As seções criadas depois de 2022 votam diferente das antigas do mesmo local?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula  
> Teto: **teto de pior caso, não estimativa: 92.023 votos de margem (2,08% da margem)** (estimativa central negativa: nenhum excesso medido)  
> O que fecharia: A lista de seções criadas, com data e motivo de criação, e o endereço de cada local (pedido ao TSE).  
> [Página técnica](residuos.html) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H6%20A-H6)

<a id="a-a32"></a>
> **Por que 348 seções têm mais de 30% de liberação manual no 2º turno, 97 delas com mais de 50%, sobretudo na Bahia e no Rio Grande do Sul?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 55.862 votos de margem (1,26% da margem)** (teto = o que passa do ruído do modelo de 2022; o teto registrado de 1.852.233 votos de margem aparece só aqui, como texto, porque é inflado por construção (Adendo 11c, deslocamento nacional negativo); a liberação manual caiu de 2022 para 2026 (3.995 seções acima de 30% em 2022); sem rajadas e sem associação com comparecimento ou voto)  
> O que fecharia: Ata da mesa receptora e folha de votação das 50 seções de maior excesso do A32 (`lai/07_secoes.csv`; pedido `lai/07_ata_e_folha_de_votacao.md`), os logs de todas as seções e a verificação da assinatura dos logs.  
> [Página técnica](fase3.html#a32) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A32%20A-A32)

<a id="a-h5"></a>
> **Por que 639 seções tiveram comparecimento de 95% ou mais, 427 delas novas?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula  
> Teto: excesso medido: 11.266 votos de margem; **teto de pior caso, não estimativa: 44.735 votos de margem (1,01% da margem)** (teto: todos os votos de Lula nas 427 seções novas, suposto inválido)  
> O que fecharia: Origem das transferências de eleitores para essas seções e o histórico dos locais (cadastro nominal, pela Justiça Eleitoral).  
> [Página técnica](fase3.html#a27) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H5%20A-H5)

<a id="a-a12b"></a>
> **Por que 29 das 106 seções com zero voto para Flávio também têm zero brancos e nulos, mais do que as vizinhas indicam (e também em 2022 e 2018)?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: a favor de Lula (teto) ou de Flávio (lado simétrico)  
> Teto: **teto de pior caso, não estimativa: 14.860 votos de margem (0,34% da margem)** (a alegação "0% de brancos e nulos" vale para 29 de 106; o excesso sobre o esperado existe em todas as eleições (razão de 1,4 em 2026, 1,4 em 2022 e 2,2 em 2018); teto: todos os votos de Lula nas 106 seções, se fossem inválidos)  
> O que fecharia: Boletins impressos e listas de habilitação dessas 106 seções (lista em `results/fase3/A12b_106_secoes.csv`) e as dos conjuntos equivalentes de 2022 e 2018.  
> [Página técnica](fase3.html#a12b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A12b%20A-A12b)

<a id="a-a33"></a>
> **Por que 661 escolas têm muito mais liberação manual do que a idade do eleitorado e o ano de 2022 indicam, e elas ganharam ou perderam voto de Lula entre os turnos?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 8.125 votos de margem (0,18% da margem)** (teto = o excesso de liberação manual além do ruído do modelo, lido como voto a favor de um só lado (fator 1); sem esse corte, o teto é 29.654 votos de margem; na escola, mais liberação manual se associa a **menos** ganho de Lula e a menos comparecimento em 2026 (placebos sem excesso); a sincronia nos logs é igual à de 2022; 92% das escolas extremas têm 3 seções ou menos)  
> O que fecharia: Ata, folha de votação e boletim impresso das 20 escolas mais extremas (`results/fase3/A33_20_escolas_secoes.csv`, 40 seções; pedido `lai/07_ata_e_folha_de_votacao.md`) e os logs de todas as seções.  
> [Página técnica](fase3.html#a33) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A33%20A-A33)

<a id="a-a20b-95"></a>
> **Por que os eleitores de 95 anos ou mais que votaram em 2026 são mais do que a razão de 2022 prevê?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 7.059 votos de margem (0,16% da margem)** (z = 2,42, Holm 0,054: passa no corte de 2 erros padrão e não passa no Holm; cerca de 4.205 votantes a mais, de 16.659)  
> O que fecharia: Cruzamento do cadastro de 95+ com o registro civil de óbitos e as listas assinadas de habilitação dessa faixa.  
> [Página técnica](fase3.html#a20b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-95%20A-A20b-95)

<a id="a-a31"></a>
> **Por que três municípios pequenos (Itacoatiara/AM, Santo Antônio de Lisboa/PI, Rafael Godeiro/RN) saem da cauda esperada da transferência do 1º para o 2º turno?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: **teto de pior caso, não estimativa: 1.151 votos de margem (0,03% da margem)** (Silva Jardim (a alegação) fica dentro da cauda; nos 3 municípios o pool é pequeno e o oponente perdeu votos quase na mesma quantidade em que o PT ganhou, com queda do comparecimento; se tudo o que o modelo não explica nos 20 mais extremos fosse manipulação, seriam 13.327 votos de margem)  
> O que fecharia: Boletins impressos e listas de habilitação por seção desses municípios, e a variação do comparecimento por seção entre os turnos.  
> [Página técnica](fase3.html#a31) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A31%20A-A31)

<a id="a-a5-2022"></a>
> **Por que uma seção de 2022 tem um voto a menos no log do que no boletim?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: excesso medido: 1 votos de margem; **teto de pior caso, não estimativa: 1 votos de margem (menos de 0,01% da margem)** (uma seção de 2022: 348 comparecimentos no boletim, 347 votos no log)  
> O que fecharia: O registro da urna daquela seção (RJ, zona 7, seção 479) e a ata de votação.  
> [Página técnica](resultados-fase2.html#a5) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A5-2022%20A-A5-2022)

<a id="a-a1t1"></a>
> **Por que a curva de apuração do 1º turno de 2026 sai do envelope esperado entre 76% e 99,9% das seções?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: sem número (teste de forma, não convertível em votos) (teste de forma; a soma final não depende da ordem)  
> O que fecharia: O registro de recepção do sistema de totalização (pedido LAI 04) e a ordem real de transmissão por município.  
> [Página técnica](a18-alteracao-no-meio.html#3b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A1T1%20A-A1T1)

<a id="a-a20b-3b"></a>
> **Onde há mais eleitores de 90 anos ou mais, há mais liberação manual, e isso cresce a cada eleição. Por quê?**  
> Situação: **TESTADO-INCONCLUSIVO** · Direção: sem direção identificável  
> Teto: sem número (teste de forma, não convertível em votos) (teste de forma; o coeficiente sobe de 0,35 (2018) a 0,80 (2026, 2º turno))  
> O que fecharia: A idade de quem foi liberado manualmente (lista de habilitação por seção) e a biometria cadastrada por eleitor, de forma agregada.  
> [Página técnica](fase3.html#a20b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-3b%20A-A20b-3b)

### b) Hipóteses ainda não testadas (Fase 3, A20 a A28)

<a id="a-a20b-t2"></a>
> **O comparecimento dos eleitores de 80 anos ou mais no 2º turno de 2026 repete o do 1º turno?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado) (o arquivo público de 2026 traz só o 1º turno; o do 2º turno de 2018 e 2022 foi publicado)  
> O que fecharia: Fecha quando o TSE publicar o perfil de comparecimento do 2º turno de 2026 (conferência semanal: `scripts/verifica_perfil_t2.sh`, rodada toda segunda-feira por uma ação do GitHub).  
> [Página técnica](fase3.html#a20b) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-T2%20A-A20b-T2)

<a id="a-a24"></a>
> **As urnas que foram para o teste de integridade e foram substituídas nas seções votaram diferente das vizinhas?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado) (script pronto; nenhuma lista lida)  
> O que fecharia: A lista de zona e seção publicada por cada TRE, em `data/a24_secoes_teste_integridade.csv` (os sites dos TREs bloqueiam acesso automatizado), ou o pedido LAI 03.  
> [Página técnica](fase3.html#a24) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A24%20A-A24)

<a id="a-a25"></a>
> **As seções em que a urna foi trocada votaram diferente antes e depois da troca?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado)  
> O que fecharia: Horário e motivo de cada troca e o registro da urna original (pedido LAI 01). A comparação seção com troca x vizinhas já foi feita (A6) e não achou efeito.  
> [Página técnica](fase3.html#a25) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A25%20A-A25)

<a id="a-a23"></a>
> **Onde houve fiscal de partido o voto foi diferente de onde não houve?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado)  
> O que fecharia: Lista de seções com fiscal, fornecida por partidos e coligações (formato na página).  
> [Página técnica](fase3.html#a23) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A23%20A-A23)

<a id="a-a21"></a>
> **O ritmo dos votos ao longo do dia (rajadas, concentração na última hora) é igual ao de 2022?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado) (só as medidas já extraídas foram testadas)  
> O que fecharia: Reler os registros das urnas com a distribuição completa dos intervalos; o ano de nascimento não consta nos logs públicos.  
> [Página técnica](fase3.html#a21) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A21%20A-A21)

<a id="a-a28"></a>
> **O que o TSE e os TREs respondem aos pedidos de acesso à informação?**  
> Situação: **NÃO TESTADO** · Direção: n/a  
> Teto: sem número ainda (teste não executado)  
> O que fecharia: Protocolar os sete pedidos prontos em `lai/` (órgão e canal de cada um em `lai/canais.csv`) e registrar protocolo, prazo e resposta, inclusive a negativa.  
> [Página técnica](fase3.html#a28) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A28%20A-A28)

### c) Pontos cegos estruturais (A18, A19)

<a id="a-a18"></a>
> **Alguém poderia alterar os resultados depois da urna fechar e antes de os arquivos serem publicados, de modo coerente?**  
> Situação: **NÃO TESTÁVEL COM DADOS PÚBLICOS** · Direção: n/a  
> Teto: não mensurável com dados públicos  
> O que fecharia: Verificar a assinatura de cada boletim com a chave oficial e conferir boletins impressos nas seções.  
> [Página técnica](a18-alteracao-no-meio.html) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A18%20A-A18)

<a id="a-a19a"></a>
> **O voto que o eleitor digita é o mesmo que a urna registra?**  
> Situação: **NÃO TESTÁVEL COM DADOS PÚBLICOS** · Direção: n/a  
> Teto: não mensurável com dados públicos  
> O que fecharia: Só o teste de integridade, por amostragem; a lista de seções, os relatórios e os vídeos por UF (pedido LAI 03).  
> [Página técnica](a19-voto-digitado.html) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19a%20A-A19a)

<a id="a-a19b"></a>
> **Por que o eleitor não confere um registro do próprio voto?**  
> Situação: **NÃO TESTÁVEL COM DADOS PÚBLICOS** · Direção: n/a  
> Teto: não mensurável com dados públicos  
> O que fecharia: Decisão legislativa: o registro impresso foi declarado inconstitucional pelo STF (ADI 4543 e ADI 5889). Sem mudança na lei, não há como fechar.  
> [Página técnica](a19-voto-digitado.html#4) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19b%20A-A19b)

<a id="a-a19c"></a>
> **O teste de integridade enxerga uma alteração pequena?**  
> Situação: **NÃO TESTÁVEL COM DADOS PÚBLICOS** · Direção: n/a  
> Teto: não mensurável com dados públicos  
> O que fecharia: Mais urnas no teste (e mais com biometria) e a publicação do resultado por UF; a curva de detecção está no gráfico G2.  
> [Página técnica](a19-voto-digitado.html#3) · [Abrir issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19c%20A-A19c)

