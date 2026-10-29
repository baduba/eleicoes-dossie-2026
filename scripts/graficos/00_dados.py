#!/usr/bin/env python3
"""Dados dos graficos G1 a G4 e dos cartoes da primeira pagina (A29/A30). Tudo sai dos CSVs de results/ ou de formulas declaradas; nenhum numero digitado a mao, exceto rotulos.
Unidade de todo numero em votos: VOTOS DE MARGEM (variacao da diferenca Lula menos Flavio; a troca de um voto muda a margem em 2).
Uso: python -I scripts/graficos/00_dados.py RAIZ_DO_REPOSITORIO"""
import math
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import hypergeom

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "."
F2, F3, OUT = (os.path.join(RAIZ, "results", d) for d in ("fase2", "fase3", "graficos"))
os.makedirs(OUT, exist_ok=True)
MARGEM = 4_430_191
N_URNAS = 499_248
ISSUE = "https://github.com/baduba/eleicoes-dossie-2026/issues/new?title="
R = pd.read_csv(os.path.join(F2, "registro_testes.csv"))


def linha(h, trecho):
    r = R[(R.H == h) & R.teste.str.contains(trecho, regex=False)]
    return r.iloc[0]


# ---------------------------------------------------------------- itens em aberto (cartoes e G3)
a27 = pd.read_csv(os.path.join(F3, "A27_perfil.csv")).iloc[0]
idosos = pd.read_csv(os.path.join(F3, "A20_comparecimento_acima_das_taxas_2022.csv"))
ido80 = float(idosos[idosos.no_grupo_80mais].comparecimento_acima_das_taxas_de_2022.sum())
a20b = pd.read_csv(os.path.join(F3, "A20b_4_suplementar_adendo9d.csv")).iloc[0]
a20bp = pd.read_csv(os.path.join(F3, "A20b_testes.csv")); a20bp = a20bp[a20bp.H == "A20b-4"]
a22 = pd.read_csv(os.path.join(F3, "A22_testes_9b.csv"))
a95 = pd.read_csv(os.path.join(F3, "A20b_95mais_teto.csv")).iloc[0]
h1f, h1s0, a10, h6 = linha("H1", "S1 Flavio/Bolsonaro votos/apto"), linha("H1", "S0 sem lag, Lula% ~ taxa manual"), linha("A10", "UE2022"), linha("H6", "secoes novas")
mil = lambda x: f"{x:,.0f}".replace(",", ".")
pos = lambda x: float(max(x, 0)) if pd.notna(x) else np.nan
I = []


def item(i, bloco, pergunta, situacao, direcao, medido, teto, pagina, fechar, nota="", grafico="auto"):
    """grafico: valor plotado no G3 (regra de exibicao, Adendo 14: nao plotar teto inflado por construcao; NaN = sem barra, o teto aparece so no texto)."""
    I.append(dict(id=i, bloco=bloco, pergunta=pergunta, situacao=situacao, direcao=direcao, excesso_medido=medido, teto_pior_caso=teto, teto_grafico=(teto if isinstance(grafico, str) else grafico), pct_margem_teto=(100 * teto / MARGEM if pd.notna(teto) else np.nan),
                  pagina=pagina, fechar=fechar, issue=ISSUE + i, nota=nota))


INC, NT, NTP = "TESTADO-INCONCLUSIVO", "NÃO TESTADO", "NÃO TESTÁVEL COM DADOS PÚBLICOS"
item("A-H1-S0", "a", "Onde há mais liberação manual de eleitor, Lula vai melhor? O teste não tem precisão para responder.", INC, "a favor de Lula", pos(h1s0.votos_central), float(h1s0.votos_max_pior_caso), "residuos.html",
     "Listas assinadas de habilitação por seção (folhas de votação) e o log de todas as seções, não só da amostra.", "teto vem da imprecisão do teste, sem efeito medido")
item("A-A20", "a", "Há mais eleitores muito idosos aptos e votando do que a população do Censo comportaria?", INC, "sem direção identificável", np.nan, ido80, "fase3.html#a20",
     "Cruzamento do cadastro com o registro civil de óbitos, por entidade fiscalizadora; perfil do eleitorado por seção, não só por zona.", "o teto é o comparecimento 80+ acima das taxas de 2022; o mesmo aumento aparece nas faixas de 70 a 79 anos")
item("A-A10", "a", "Urnas do modelo mais novo (UE2022) votam diferente das demais dentro do mesmo local?", INC, "a favor de Lula", pos(a10.votos_central), float(a10.votos_max_pior_caso), "resultados-fase2.html#a10",
     "Mais seções com o modelo novo em 2022 para servir de comparação, ou o código de carga por urna (pedido LAI 02).")
item("A-H6", "a", "As seções criadas depois de 2022 votam diferente das antigas do mesmo local?", INC, "a favor de Lula", pos(h6.votos_central), float(h6.votos_max_pior_caso), "residuos.html",
     "A lista de seções criadas, com data e motivo de criação, e o endereço de cada local (pedido ao TSE).", "estimativa central negativa: nenhum excesso medido")
item("A-H5", "a", "Por que 639 seções tiveram comparecimento de 95% ou mais, 427 delas novas?", INC, "a favor de Lula", pos(linha("H5", "excesso sobre o esperado").votos_central), float(a27.votos_lula), "fase3.html#a27",
     "Origem das transferências de eleitores para essas seções e o histórico dos locais (cadastro nominal, pela Justiça Eleitoral).", "teto: todos os votos de Lula nas 427 seções novas, suposto inválido")
item("A-H1-FL", "a", "Onde há mais liberação manual, Flávio vai melhor do que no 1º turno prevê?", INC, "a favor de Flávio", pos(h1f.votos_central), float(h1f.votos_max_pior_caso), "residuos.html",
     "Folhas de votação assinadas por seção e relatos de fiscais.")
item("A-A1T1", "a", "Por que a curva de apuração do 1º turno de 2026 sai do envelope esperado entre 76% e 99,9% das seções?", INC, "sem direção identificável", np.nan, np.nan, "a18-alteracao-no-meio.html#3b",
     "O registro de recepção do sistema de totalização (pedido LAI 04) e a ordem real de transmissão por município.", "teste de forma; a soma final não depende da ordem")
item("A-A5-2022", "a", "Por que uma seção de 2022 tem um voto a menos no log do que no boletim?", INC, "sem direção identificável", 1.0, 1.0, "resultados-fase2.html#a5",
     "O registro da urna daquela seção (RJ, zona 7, seção 479) e a ata de votação.", "uma seção de 2022: 348 comparecimentos no boletim, 347 votos no log")
item("A-A22", "a", "O voto para presidente combina com o voto para governador na mesma seção, como em 2022 e 2018?", INC, "a favor de Flávio ou de Lula (lados simétricos)", np.nan, float(a22.votos_max_pior_caso.max()), "fase3.html#a22",
     "Os votos por candidato em todos os cargos por seção nas 27 UFs, com uma regra de alinhamento definida por quem conhece as alianças locais; ou deputados federais por partido nas UFs sem 2º turno de governador.",
     f"variante exploratória (Adendo 9b), só AM e DF, pouco poder; vale só para os votos dessas duas UFs; o lado a favor de Lula tem teto de {mil(a22.votos_max_pior_caso.min())}"+ "; a linha oficial de A22 é NÃO EXECUTÁVEL (nenhuma UF elegível pela regra registrada)")
item("A-A20b", "a", "Nas seções com mais eleitores de 80 anos ou mais, o comparecimento do 2º turno sobe mais do que em 2022 e 2018?", INC, "sem direção identificável", np.nan, float(a20b.votos_max_pior_caso), "fase3.html#a20b",
     "Listas assinadas de habilitação das seções com mais idosos e o cruzamento do cadastro com o registro civil de óbitos, por entidade fiscalizadora.",
     "linha suplementar do Adendo 9d (só placebos com o mesmo controle); a linha original, com um comparador de outra especificação, dá 4,07 milhões; o coeficiente de participação de Lula nessas seções é negativo")
item("A-A20b-part", "a", "Nas seções com mais eleitores de 80 anos ou mais, a participação de Lula e de Flávio difere da dos anos anteriores?", INC, "a favor de Lula (teto) ou de Flávio (lado simétrico)", np.nan, float(a20bp.iloc[0].votos_max_pior_caso), "fase3.html#a20b",
     "Mais anos de comparação com o perfil do eleitorado por seção e as listas de habilitação das seções com mais idosos.",
     f"o coeficiente de 2026 fica dentro do intervalo dos placebos e a estimativa central é negativa para Lula; o teto vem da dispersão entre os anos de comparação; o lado a favor de Flávio tem teto de {mil(a20bp.iloc[1].votos_max_pior_caso)}")
item("A-A20b-3b", "a", "Onde há mais eleitores de 90 anos ou mais, há mais liberação manual, e isso cresce a cada eleição. Por quê?", INC, "sem direção identificável", np.nan, np.nan, "fase3.html#a20b",
     "A idade de quem foi liberado manualmente (lista de habilitação por seção) e a biometria cadastrada por eleitor, de forma agregada.", "teste de forma; o coeficiente sobe de 0,35 (2018) a 0,80 (2026, 2º turno)")
item("A-A20b-95", "a", "Por que os eleitores de 95 anos ou mais que votaram em 2026 são mais do que a razão de 2022 prevê?", INC, "sem direção identificável", np.nan, float(a95.teto_votos_de_margem_pior_caso), "fase3.html#a20b",
     "Cruzamento do cadastro de 95+ com o registro civil de óbitos e as listas assinadas de habilitação dessa faixa.",
     f"z = {str(round(a95.z, 2)).replace('.', ',')}, Holm 0,054: passa no corte de 2 erros padrão e não passa no Holm; cerca de {mil(a95.votantes_a_mais_que_pela_razao_de_2022)} votantes a mais, de {mil(a95.votantes_95mais_2026_T1)}")
a31t = pd.read_csv(os.path.join(F3, "A31_tetos.csv")).set_index("grupo")
a31s1 = pd.read_csv(os.path.join(F3, "A31_suplementar_S1_tetos.csv")).iloc[0]
item("A-A31", "a", "Por que três municípios pequenos (Itacoatiara/AM, Santo Antônio de Lisboa/PI, Rafael Godeiro/RN) saem da cauda esperada da transferência do 1º para o 2º turno?", INC, "sem direção identificável", np.nan, float(a31t.loc["20 mais extremos de 2026", "teto_alem_da_cauda_votos_margem"]), "fase3.html#a31",
     "Boletins impressos e listas de habilitação por seção desses municípios, e a variação do comparecimento por seção entre os turnos.",
     "Silva Jardim (a alegação) fica dentro da cauda; nos 3 municípios o pool é pequeno e o oponente perdeu votos quase na mesma quantidade em que o PT ganhou, com queda do comparecimento; se tudo o que o modelo não explica nos 20 mais extremos fosse manipulação, seriam "
     + f"{a31t.loc['20 mais extremos de 2026', 'teto_incondicional_votos_margem']:,.0f}".replace(",", ".") + " votos de margem")
a12b = pd.read_csv(os.path.join(F3, "A12b_resumo_106.csv")).iloc[0]
a32t = pd.read_csv(os.path.join(F3, "A32_teto_excesso_manual.csv")).set_index("ano").loc["2026"]
a31br = pd.read_csv(os.path.join(F3, "A31b_resumo.csv")).iloc[0]
a33r = pd.read_csv(os.path.join(F3, "A33_escolas_extremas_resumo.csv")).iloc[0]
item("A-A31b", "a", "Por que 748 dos 5.357 municípios (14,0%) tiveram o ganho de Flávio entre os turnos de +1 voto ou menos, quase todos no Nordeste e no Norte?", INC, "sem direção identificável", np.nan, float(a31br.teto_A_votos_margem), "fase3.html#a31b",
     "Boletins impressos das seções dos 20 municípios com maior perda de Flávio (lista em `results/fase3/A31b_20_secoes.csv`) e as listas de habilitação.",
     f"a fração de 14,0% é compatível com o crescimento nacional do oponente em 2026 (esperado de 13,2% a 15,4% com 2018 e 2022 deslocados); 70,6% desses municípios tiveram queda de comparecimento; o teto é todo o déficit de Flávio em relação ao crescimento da UF atribuído a troca de voto, e o excedente sobre o que o deslocamento nacional reproduz é {mil(a31br.teto_B_votos_margem)}; **o teste não distingue troca de voto de abstenção seletiva**", grafico=np.nan)
item("A-A12b", "a", "Por que 29 das 106 seções com zero voto para Flávio também têm zero brancos e nulos, mais do que as vizinhas indicam (e também em 2022 e 2018)?", INC, "a favor de Lula (teto) ou de Flávio (lado simétrico)", np.nan, float(a12b.teto_a_todos_os_votos_de_lula_invalidos_votos_de_margem), "fase3.html#a12b",
     "Boletins impressos e listas de habilitação dessas 106 seções (lista em `results/fase3/A12b_106_secoes.csv`) e as dos conjuntos equivalentes de 2022 e 2018.",
     "a alegação \"0% de brancos e nulos\" vale para 29 de 106; o excesso sobre o esperado existe em todas as eleições (razão de 1,4 em 2026, 1,4 em 2022 e 2,2 em 2018); teto: todos os votos de Lula nas 106 seções, se fossem inválidos")
item("A-A32", "a", "Por que 348 seções têm mais de 30% de liberação manual no 2º turno, 97 delas com mais de 50%, sobretudo na Bahia e no Rio Grande do Sul?", INC, "sem direção identificável", np.nan, float(a32t.c_alem_de_1_645_sigma), "fase3.html#a32",
     "Ata da mesa receptora e folha de votação das 50 seções de maior excesso do A32 (`lai/07_secoes.csv`; pedido `lai/07_ata_e_folha_de_votacao.md`), os logs de todas as seções e a verificação da assinatura dos logs.",
     f"teto = o que passa do ruído do modelo de 2022; o teto registrado de {mil(a32t.maior_dos_quatro_votos_de_margem_fator_1)} votos de margem aparece só aqui, como texto, porque é inflado por construção (Adendo 11c, deslocamento nacional negativo); a liberação manual caiu de 2022 para 2026 (3.995 seções acima de 30% em 2022); sem rajadas e sem associação com comparecimento ou voto")
item("A-A33", "a", "Por que 661 escolas têm muito mais liberação manual do que a idade do eleitorado e o ano de 2022 indicam, e elas ganharam ou perderam voto de Lula entre os turnos?", INC, "sem direção identificável", np.nan, float(a33r.alem_do_ruido), "fase3.html#a33",
     "Ata, folha de votação e boletim impresso das 20 escolas mais extremas (`results/fase3/A33_20_escolas_secoes.csv`, 40 seções; pedido `lai/07_ata_e_folha_de_votacao.md`) e os logs de todas as seções.",
     f"teto = o excesso de liberação manual além do ruído do modelo, lido como voto a favor de um só lado (fator 1); sem esse corte, o teto é {mil(a33r.teto_votos_de_margem_fator1)} votos de margem; na escola, mais liberação manual se associa a **menos** ganho de Lula e a menos comparecimento em 2026 (placebos sem excesso); a sincronia nos logs é igual à de 2022; 92% das escolas extremas têm 3 seções ou menos")
RAIZ_R4 = os.path.join(os.path.dirname(os.path.abspath(F3)), "fase4")
a33te = pd.read_csv(os.path.join(F3, "A33_testes.csv"))
item("A-A33-idade", "a", "Por que as escolas extremas em liberação manual não são explicadas pela idade do eleitorado, como o pré-registro do A33 previa?", INC, "sem direção identificável", np.nan, float(a33r.alem_do_ruido), "fase3.html#a33",
     "Ata, folha de votação e boletim impresso das 20 escolas mais extremas (`results/fase3/A33_20_escolas_secoes.csv`, 40 seções) e os logs de todas as seções; a causa operacional (leitor biométrico com defeito, por exemplo) só se confirma ou descarta com o log e a ata da seção.",
     f"**a previsão do pré-registro (extremas explicadas pela idade) não se cumpriu**: nas 20 primeiras, a idade média é de 32 a 59 anos, o previsto é de 6% a 15% e o observado de 30% a 82%; teto = excesso além do ruído do modelo, lido como voto a favor de um só lado (fator 1); sem esse corte, {mil(a33r.teto_votos_de_margem_fator1)} votos de margem; 92% têm 3 seções ou menos; na média, Lula ganhou menos nelas (+1,5 ponto) que no país (+3,0); já descrito no cartão A-A33", grafico=np.nan)
item("A-A33-placebo", "a", "Por que o coeficiente de 2026 da liberação manual da escola sobre o ganho de Lula (-0,017) é mais negativo que o do placebo de 2022 (-0,002)?", INC, "sem direção identificável", np.nan, float(a33te.votos_max_pior_caso.iloc[0]), "fase3.html#a33",
     "A abstenção por faixa etária e por seção do 2º turno (produto do TSE ainda não publicado) e a composição das escolas (rural, idade) para separar efeito de composição de efeito da liberação manual.",
     "**causa não identificada**; o sentido é o oposto ao do esquema pré-registrado (mais liberação manual, menos ganho de Lula e menos comparecimento), o placebo de 2018 tem o mesmo sinal negativo, e nenhum teste de excesso passa em Holm; o teto vem da incerteza do coeficiente multiplicada pela exposição, não de um efeito medido, e por isso **não é plotado no G3** (regra de exibição, CHANGELOG)", grafico=np.nan)
a35t = pd.read_csv(os.path.join(RAIZ_R4, "A35_teto.csv")).iloc[0]; a35d = pd.read_csv(os.path.join(RAIZ_R4, "A35_E1_decisao.csv")).iloc[0]
item("A-A35", "a", "Há mais seções grandes sem brancos e nulos, ou com comparecimento de 100% dos aptos, do que o acaso dá?", INC, "sem direção identificável", np.nan, float(a35t.E1_fator2_troca_pela_vizinhanca), "fase3.html#a35",
     "Boletins impressos das seções sinalizadas (lista em `results/fase4/A35_E1_sinalizadas_2026T2.csv`, 2.989 seções com 100 votantes ou mais e zero brancos e nulos; e as 12 com comparecimento igual aos aptos em `results/fase4/A35_E2_secoes_2026T2.csv`).",
     f"teto = troca esperada pela vizinhança (fator 2); no fator 1 (todos os votos do majoritário nessas seções) seriam {mil(a35t.E1_fator1_votos_do_majoritario)} votos de margem, inflado por construção; o observado fica **abaixo** do esperado em todos os anos (razão {str(round(float(a35d.razao_2026T2), 2)).replace('.', ',')} em 2026 e {str(round(float(a35d.razao_2022T2), 2)).replace('.', ',')} em 2022), dentro do esperado pela regra pré-registrada; 12 seções com comparecimento igual aos aptos (descritivo, sem p)")
a34t = pd.read_csv(os.path.join(RAIZ_R4, "A34_diag_teto.csv")).iloc[0]; a34p = pd.read_csv(os.path.join(RAIZ_R4, "A34_regra_p99.csv")); a34p3 = a34p[(a34p.metrica == "D3") & (a34p.ano == 2026) & (a34p.turno == 2)].iloc[0]
item("A-A34", "a", "A duração do voto, da habilitação à confirmação, é compatível com um eleitor presente em cada seção? A regra do percentil 99 acusa excesso em 2026, mas a composição da cédula explica quase tudo.", INC, "sem direção identificável", np.nan, float(a34t.extrapolacao_nacional_excesso_sobre_1pct_fator1), "fase3.html#a34",
     "Logs de todas as seções (poder), uma lista oficial das UFs com segundo turno estadual em cada ano (para fixar a composição da cédula sem usar o desfecho) e o log com todos os cargos.",
     f"teto extrapolado do excesso de 0,24 ponto percentual sobre 1% (cerca de 16 seções em 6.667 de UFs com a mesma composição de cédula) para as 497.897 seções, com todo o voto lido como de um lado: **inflado por construção, não plotado no G3**; no fator 1 da amostra são {mil(a34t.a_fator1_votos_validos_das_secoes_acima)} votos de margem; pela regra registrada, {str(round(100 * float(a34p3.fracao_acima), 2)).replace('.', ',')}% das seções de 2026/2º turno têm D3 acima do percentil 99 de 2022 contra 1% esperado (excesso de forma), que cai para {str(round(100 * float(a34t.fracao_acima), 2)).replace('.', ',')}% nas UFs de mesma composição (diagnóstico pós-hoc); a previsão do pré-registro para a mediana (40 s a 2 min) estava errada (a mediana é de 9 s); mediana e modelos de associação sem excesso", grafico=np.nan)
item("A-A20b-T2", "b", "O comparecimento dos eleitores de 80 anos ou mais no 2º turno de 2026 repete o do 1º turno?", NT, "n/a", np.nan, np.nan, "fase3.html#a20b",
     "Fecha quando o TSE publicar o perfil de comparecimento do 2º turno de 2026 (conferência semanal: `scripts/verifica_perfil_t2.sh`, rodada toda segunda-feira por uma ação do GitHub).",
     "o arquivo público de 2026 traz só o 1º turno; o do 2º turno de 2018 e 2022 foi publicado")
item("A-A24", "b", "As urnas que foram para o teste de integridade e foram substituídas nas seções votaram diferente das vizinhas?", NT, "n/a", np.nan, np.nan, "fase3.html#a24",
     "A lista de zona e seção publicada por cada TRE, em `data/a24_secoes_teste_integridade.csv` (os sites dos TREs bloqueiam acesso automatizado), ou o pedido LAI 03.", "script pronto; nenhuma lista lida")
item("A-A25", "b", "As seções em que a urna foi trocada votaram diferente antes e depois da troca?", NT, "n/a", np.nan, np.nan, "fase3.html#a25",
     "Horário e motivo de cada troca e o registro da urna original (pedido LAI 01). A comparação seção com troca x vizinhas já foi feita (A6) e não achou efeito.")
item("A-A23", "b", "Onde houve fiscal de partido o voto foi diferente de onde não houve?", NT, "n/a", np.nan, np.nan, "fase3.html#a23",
     "Lista de seções com fiscal, fornecida por partidos e coligações (formato na página).")
item("A-A21", "b", "O ritmo dos votos ao longo do dia (rajadas, concentração na última hora) é igual ao de 2022?", NT, "n/a", np.nan, np.nan, "fase3.html#a21",
     "Reler os registros das urnas com a distribuição completa dos intervalos; o ano de nascimento não consta nos logs públicos.", "só as medidas já extraídas foram testadas")
item("A-A28", "b", "O que o TSE e os TREs respondem aos pedidos de acesso à informação?", NT, "n/a", np.nan, np.nan, "fase3.html#a28",
     "Protocolar os sete pedidos prontos em `lai/` (órgão e canal de cada um em `lai/canais.csv`) e registrar protocolo, prazo e resposta, inclusive a negativa.")
item("A-A18", "c", "Alguém poderia alterar os resultados depois da urna fechar e antes de os arquivos serem publicados, de modo coerente?", NTP, "n/a", np.nan, np.nan, "a18-alteracao-no-meio.html",
     "Verificar a assinatura de cada boletim com a chave oficial e conferir boletins impressos nas seções.")
item("A-A19a", "c", "O voto que o eleitor digita é o mesmo que a urna registra?", NTP, "n/a", np.nan, np.nan, "a19-voto-digitado.html",
     "Só o teste de integridade, por amostragem; a lista de seções, os relatórios e os vídeos por UF (pedido LAI 03).")
item("A-A19b", "c", "Por que o eleitor não confere um registro do próprio voto?", NTP, "n/a", np.nan, np.nan, "a19-voto-digitado.html#4",
     "Decisão legislativa: o registro impresso foi declarado inconstitucional pelo STF (ADI 4543 e ADI 5889). Sem mudança na lei, não há como fechar.")
item("A-A19c", "c", "O teste de integridade enxerga uma alteração pequena?", NTP, "n/a", np.nan, np.nan, "a19-voto-digitado.html#3",
     "Mais urnas no teste (e mais com biometria) e a publicação do resultado por UF; a curva de detecção está no gráfico G2.")
D = pd.DataFrame(I)
D["ordem"] = D.groupby("bloco").teto_pior_caso.rank(ascending=False, method="first", na_option="bottom")
D.sort_values(["bloco", "ordem"]).drop(columns="ordem").to_csv(os.path.join(OUT, "itens_em_aberto.csv"), index=False)

# ---------------------------------------------------------------- G2: curvas de deteccao
def p_detecta(n, f):
    k = math.ceil(f * N_URNAS)
    return float(hypergeom.sf(0, N_URNAS, k, n))


prem = pd.read_csv(os.path.join(F2, "poder_teste_integridade_premissas.csv")).iloc[0]
n_int, n_bio_hi, n_bio_lo = int(prem.total_teste_integridade_pela_regra), int(prem.biometria_10pct), int(prem.biometria_5pct)
bu = pd.read_csv(os.path.join(OUT, "bu_conferidos.csv")) if os.path.exists(os.path.join(OUT, "bu_conferidos.csv")) else pd.DataFrame([dict(n_conferidos=0, data="2026-10-29", divergencias=0)])
bu.to_csv(os.path.join(OUT, "bu_conferidos.csv"), index=False)
n_bu = int(bu.n_conferidos.iloc[0])
fr = np.logspace(math.log10(0.001), math.log10(0.20), 120)
rows = []
for f in fr:
    rows.append(dict(fracao=f, teste_integridade=p_detecta(n_int, f), biometria_10pct=p_detecta(n_bio_hi, f), biometria_5pct=p_detecta(n_bio_lo, f), bu_100=p_detecta(100, f), bu_300=p_detecta(300, f),
                     bu_1000=p_detecta(1000, f), bu_conferidos=(p_detecta(n_bu, f) if n_bu > 0 else np.nan)))
pd.DataFrame(rows).to_csv(os.path.join(OUT, "curvas_deteccao.csv"), index=False)
pd.DataFrame([dict(n_teste_integridade=n_int, n_biometria_10pct=n_bio_hi, n_biometria_5pct=n_bio_lo, n_bu_conferidos=n_bu, data_bu=bu.data.iloc[0])]).to_csv(os.path.join(OUT, "curvas_deteccao_premissas.csv"), index=False)

# ---------------------------------------------------------------- G4: secoes necessarias x trocas por secao; limiar de visibilidade individual
ks = np.arange(1, 301)
secoes = np.ceil(math.ceil((MARGEM + 1) / 2) / ks)
sd_res = 0.0167       # desvio padrao do residuo local da participacao de Lula (2026/T2, EF de local, controle do T1), medido nesta auditoria: 1,67 p.p.; mediana de 256 votos validos por secao
k_visivel = math.ceil(3 * sd_res * 256)
pd.DataFrame(dict(trocas_por_secao=ks, secoes_necessarias=secoes, pct_das_secoes=100 * secoes / N_URNAS)).to_csv(os.path.join(OUT, "secoes_para_inverter.csv"), index=False)
pd.DataFrame([dict(sd_residuo_local_pp=100 * sd_res, mediana_votos_validos=256, limiar_z=3, trocas_por_secao_visiveis_como_outlier=k_visivel,
                   nota="com 475.784 secoes, cerca de 0,27% (1.284) passariam |z|>3 por acaso; abaixo do limiar, a alteracao nao aparece secao a secao")]).to_csv(os.path.join(OUT, "visibilidade_individual.csv"), index=False)

# ---------------------------------------------------------------- G1: cadeia do voto
V, P, X = "verificado", "parcial", "nao_verificavel"
cad = [("Cadastro de eleitores", P, "A20, A20b, A9", "fase3.html#a20", "comparado ao Censo; sem cruzamento nominal"),
       ("Habilitação (biometria / liberação manual)", P, "H1, H2, A5", "resultados-fase1.html", "o log registra, mas não prova quem era o eleitor"),
       ("Voto digitado → voto registrado (software)", X, "A19", "a19-voto-digitado.html", "verificado só por amostragem no teste de integridade"),
       ("RDV (registro digital do voto)", V, "A4", "resultados-fase2.html#a4", "recontado e igual ao boletim; mesmo software da urna"),
       ("BU digital", V, "A4, H9", "resultados-fase2.html#a4", "igual ao BWeb; mesmo software da urna"),
       ("BU impresso", X, "A18, boletins", "boletins-impressos.html", "0 boletins conferidos até agora"),
       ("Assinatura digital", P, "A4, A18", "a18-alteracao-no-meio.html#2", "certificado lido; assinatura 0% verificada"),
       ("Transmissão", X, "A18", "a18-alteracao-no-meio.html", "canal não público"),
       ("Recepção", P, "A14, A18", "a18-alteracao-no-meio.html#1", "horários públicos; sem o registro interno"),
       ("Totalização", V, "H9", "resultados-fase1.html", "igual por seção, município e zona; mesmo fluxo"),
       ("Publicação (BWeb)", V, "A26, H9", "fase3.html#a26", "hash e tamanho iguais ao primeiro download"),
       ("Divulgação ao vivo", P, "A1, A14", "resultados-fase2.html#a1", "curva analisada; sem capturas da época")]
pd.DataFrame(cad, columns=["etapa", "status", "testes", "pagina", "nota"]).to_csv(os.path.join(OUT, "cadeia.csv"), index=False)
print(D.sort_values(["bloco", "teto_pior_caso"], ascending=[True, False])[["id", "bloco", "excesso_medido", "teto_pior_caso", "pct_margem_teto"]].round(2).to_string())
print("k visivel:", k_visivel, "| n integridade", n_int, n_bio_lo, n_bio_hi)
