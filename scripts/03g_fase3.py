#!/usr/bin/env python3
"""docs/fase3.md (A20 a A28), gerado dos resultados. Uso: python -I 03g_fase3.py DIR_FASE2 DIR_FASE3 RAIZ"""
import os
import sys
import pandas as pd

R2, R3, RAIZ = sys.argv[1:4]
MARGEM = 4_430_191
rd = lambda d, f: pd.read_csv(os.path.join(d, f))


def n(x, d=0):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "n/d"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tab(df, fm=None):
    fm = fm or {}
    cols = list(df.columns)
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.astype(object).iterrows():
        L.append("| " + " | ".join(((fm[c](r[c]) if c in fm else str(r[c])).replace("|", "/")) for c in cols) + " |")
    return "\n".join(L)


L = []
A = L.append
A("# Fase 3: hipóteses adversariais (A20 a A28)\n")
A("> **Unidade: votos de margem** (variação da diferença Lula menos Flávio; trocar um voto muda a margem em 2; definição em [Metodologia](metodologia.md)). Margem oficial: 4.430.191. Todo teto é **teto de pior caso, não estimativa**. Os testes de forma não têm teto em votos.\n")
A("Previsões, critérios e o que cada teste cobre foram registrados no [Adendo 8](preregistro.md) **antes** de rodar. Cada teste descreve a **classe de falha** que cobre e o **rastro esperado** nos dados públicos, não como produzir a falha. Quando falta insumo, o teste fica **NÃO EXECUTADO**, com o insumo e como fornecê-lo.\n")
A("| teste | classe de falha coberta | resultado | teto em votos de margem | veredito |\n|---|---|---|---|---|")
v20 = rd(R3, "A20_veredito.csv"); a21 = rd(R3, "A21_testes.csv"); a26 = rd(R3, "A26_resumo.csv").iloc[0]; a27 = rd(R3, "A27_perfil.csv").iloc[0]
ido = rd(R3, "A20_comparecimento_acima_das_taxas_2022.csv"); ido80 = float(ido[ido.no_grupo_80mais].comparecimento_acima_das_taxas_de_2022.sum())
A(f"| [A20](#a20) Cadastro x Censo | eleitorado apto inflado | 80+ e 90+: fração de municípios com mais aptos que habitantes acima de 2018 e 2022 (formal; ver ressalva); 16+ e 100+: sem excesso | comparecimento 80+ acima das taxas de 2022: {n(ido80)} votos de margem (teto de pior caso, não estimativa; {n(100 * ido80 / MARGEM, 1)}% da margem) | EXCESSO DETECTADO (forma) em 80+ e 90+, **com ressalva de desenho**; TESTADO-INCONCLUSIVO |")
A(f"| [A21](#a21) Logs, ritmo dos votos | registro de votos fora do ritmo real | intervalos < 10 s: nenhum, em nenhum ano; último voto depois do horário nominal explicado pela prorrogação de 25/10 | sem conversão em votos (amostra) | parcial; EXCESSO DETECTADO (forma) em uma medida, **com ressalva** |")
A("| [A22](#a22) Coerência entre cargos | desvio uniforme só no presidente | **NÃO EXECUTADO** (falta a tabela de coligações) | n/a | NÃO EXECUTADO |")
A("| [A23](#a23) Fiscalização | comportamento diferente onde há ou não fiscal | **NÃO EXECUTADO** (sem lista de seções com fiscal) | n/a | NÃO EXECUTADO |")
A("| [A24](#a24) Experimento natural do teste de integridade | urna que se comporta diferente fora do teste | **NÃO EXECUTADO** (lista de seções não pública) | n/a | NÃO EXECUTADO |")
A("| [A25](#a25) Urnas substituídas | troca de urna como ponto de intervenção | seção com troca x vizinhas: ver A6 (sem efeito); antes x depois da troca: NÃO EXECUTADO | n/a (A6: teto abaixo de 1% da margem) | parcial |")
A(f"| [A26](#a26) Integridade da publicação | arquivo publicado alterado depois | {int(a26.arquivos)} arquivos: tamanho igual em {int(a26.tamanho_igual)}; hash oficial igual em {int(a26.hash_igual)} de {int(a26.hash_conferido)}; nenhum modificado depois do primeiro download | n/a | SEM ALTERAÇÃO DETECTADA |")
A(f"| [A27](#a27) Seções fabricadas | seções sem eleitores reais | 427 seções novas com comparecimento ≥ 95%: perfil abaixo | {n(a27.votos_lula)} votos de margem (teto de pior caso, não estimativa; {n(100 * a27.votos_lula / MARGEM, 1)}% da margem): todos os votos de Lula nas 427 seções, suposto inválidos | TESTADO-INCONCLUSIVO |")
A("| [A28](#a28) Pedidos LAI | dados que só o poder público tem | 6 pedidos redigidos em `lai/`; **nenhum protocolado** | n/a | NÃO EXECUTADO |\n")

# ---------------------------------------------------------------- A20
A('<a id="a20"></a>\n\n## A20. Cadastro: eleitorado apto x população do Censo 2022\n')
A("**Pergunta.** Há mais eleitores aptos do que habitantes, por município e faixa etária, e isso mudou entre 2018, 2022 e 2026? **Classe de falha coberta:** eleitorado apto inflado. **Rastro esperado:** razão aptos/população acima de 1 em municípios, concentrada nos mais idosos. **Previsão sem manipulação:** fração de municípios com razão > 1 em 2026 dentro do intervalo de 2018 e 2022, depois de remover o nível nacional.\n")
A("**Método.** População: Censo 2022 (IBGE, SIDRA 9514), a mesma em todos os anos; por isso 2018 e 2026 têm denominador defasado e cada razão municipal é reescalada pela razão nacional do ano para a escala de 2022 (Adendo 8). Aptos: perfil do eleitorado por zona e faixa etária (1º turno). Mapa TSE x IBGE por nome e UF: 5.557 de 5.757 municípios (200 sem correspondência de nome ficam fora). Municípios com população da faixa abaixo de 100 (16+), 30 (80+), 10 (90+) ou 1 (100+) ficam fora de cada faixa.\n")
r = rd(R3, "A20_razoes_por_ano.csv")
A(tab(r[["grupo", "ano", "municipios", "razao_nacional", "aptos", "populacao_2022", "fracao_municipios_razao_gt1_bruta", "fracao_razao_gt1_na_escala_de_2022"]], {"municipios": n, "razao_nacional": lambda x: n(float(x), 3), "aptos": n, "populacao_2022": n, "fracao_municipios_razao_gt1_bruta": lambda x: n(100 * float(x), 1) + "%", "fracao_razao_gt1_na_escala_de_2022": lambda x: n(100 * float(x), 1) + "%"}))
A("\n**Resultado pelo critério pré-registrado (forma, sem teto em votos):**\n")
A(tab(v20, {"fracao_2026": lambda x: n(100 * float(x), 1) + "%"}))
A("\n> **Ressalva de desenho (leia junto com o veredito).** A fração de municípios com razão > 1 sobe de modo contínuo de 2018 para 2022 e para 2026 em 80+ e 90+, e o teste de interseção-união contra cada ano anterior acusa o último ano de uma série crescente. O salto de 2022 para 2026 (80+: 2,1 p.p.; 90+: 4,6 p.p.) é menor que o de 2018 para 2022 (9,8 e 8,8 p.p.). O rótulo de excesso é formal e **não indica manipulação**; a linha não foi alterada.\n")
A("**O que chama atenção, sem interpretação causal.** (i) A razão nacional 80+ é 0,89 (2018), 1,12 (2022) e 1,20 (2026) contra o Censo 2022; a 90+ é 1,28, 1,78 e 1,66; a 100+ é 1,0, 4,8 e 7,8: 297.977 aptos com 100 anos ou mais em 2026 contra 37.779 pessoas dessa idade no Censo. A idade dos eleitores vem do cadastro, a do Censo é declarada; uma parte pode ser data de nascimento padrão ou título não cancelado, e o comparecimento nessas faixas é pequeno (0,7% em 100+). (ii) O comparecimento facultativo sobe **em todas as faixas de 70 anos ou mais** de 2022 para 2026:\n")
cb = rd(R3, "A20_comparecimento_idosos_por_faixa.csv").pivot(index="faixa", columns="ano", values="pct_comparecimento").round(1)
A("| faixa | 2018 | 2022 | 2026 |\n|---|---|---|---|")
for f in ["70 a 74 anos", "75 a 79 anos", "80 a 84 anos", "85 a 89 anos", "90 a 94 anos", "95 a 99 anos", "100 anos ou mais"]:
    A(f"| {f} | {n(cb.loc[f, 2018], 1)}% | {n(cb.loc[f, 2022], 1)}% | {n(cb.loc[f, 2026], 1)}% |")
A(f"\nSe o comparecimento de 2026 nas faixas de 80 anos ou mais tivesse ficado nas taxas de 2022, haveria {n(ido80)} votantes a menos. **Teto de pior caso, não estimativa:** {n(ido80)} votos de margem ({n(100 * ido80 / MARGEM, 1)}% da margem), se todo esse aumento fosse voto adicional de um só candidato, o que os dados não indicam: o aumento aparece também em 70 a 74 e 75 a 79 anos, o que aponta para um fenômeno geral da faixa facultativa. **Situação:** TESTADO-INCONCLUSIVO. **O que fecharia:** cruzamento do cadastro com o registro civil de óbitos por entidade fiscalizadora, e perfil por seção.\n")
A("**A20b, perfil de idade e sexo das seções novas:** NÃO EXECUTADO. O perfil público é por zona, não por seção. Insumo: perfil do eleitorado por seção (pedido ao TSE).\n")

# ---------------------------------------------------------------- A21
A('<a id="a21"></a>\n\n## A21. Forense temporal dos logs de urna (parcial)\n')
A("**Pergunta.** O ritmo dos votos ao longo do dia é igual ao de 2022 e não tem relação com o voto? **Classe de falha coberta:** registro de votos fora do ritmo da votação real. **Rastro esperado:** intervalos muito curtos entre votos, rajadas, concentração na última hora. **Previsão sem manipulação:** padrões iguais em 2022 e 2026, sem associação com o voto.\n")
A("**Executado** com as medidas já extraídas dos logs da amostra de arquivos de urna (seções pareadas entre 2022 e 2026). **NÃO EXECUTADO:** distribuição completa dos intervalos, rajadas por ano de nascimento (o ano de nascimento não consta nos logs públicos) e concentração na última hora; exigem reler os logs.\n")
A(tab(rd(R3, "A21_descritivo_pareado.csv"), {"secoes_pareadas": n, "media_2026": lambda x: n(float(x), 3), "media_2022": lambda x: n(float(x), 3), "diferenca_media": lambda x: n(float(x), 3), "ep": lambda x: n(float(x), 3), "pct_secoes_com_valor_positivo_2026": lambda x: n(float(x), 1), "pct_secoes_com_valor_positivo_2022": lambda x: n(float(x), 1)}))
A("\nNenhuma seção, em nenhum dos dois anos, tem dois votos com intervalo menor que 10 segundos. O último voto vem depois do horário nominal em 28,0% das seções em 2026 contra 13,0% em 2022, o que é compatível com a prorrogação do 2º turno decidida em 25/10/2026 ([A18](a18-alteracao-no-meio.md), [A5](resultados-fase2.md)).\n")
t = a21[["teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "veredito"]].copy()
A(tab(t, {"est_2026T2": lambda x: n(float(x), 5), "p_excesso": lambda x: n(float(x), 3), "p_holm": lambda x: n(float(x), 3)}))
A("\n> **Ressalva.** Na medida \"minutos do último voto depois do horário nominal\" o coeficiente de 2026 é indistinguível de zero (0,00001 por minuto); a diferença para o critério vem do coeficiente negativo de 2022 (-0,00006), único placebo. Na seção média, 5,6 minutos de atraso somam cerca de 0,04 ponto percentual. O rótulo é formal e **não indica manipulação**. A amostra é de arquivos de urna, não nacional, então não há teto em votos.\n")

# ---------------------------------------------------------------- A22 a A25
A('<a id="a22"></a>\n\n## A22. Coerência entre cargos: NÃO EXECUTADO\n')
A("**Classe de falha coberta:** desvio uniforme restrito ao cargo de presidente, invisível a testes de valor atípico. **Rastro esperado:** deslocamento sistemático do resíduo entre o voto presidencial e os votos em cargos não presidenciais da mesma seção. **Previsão sem manipulação:** resíduo de 2026 igual ao de 2022 e 2018. **Desenho fixado** (Adendo 8): nos estados com 2º turno para governador, participação do candidato presidencial contra a do candidato a governador aliado no mesmo turno, com efeito fixo de UF e controle do 1º turno; estatística: deslocamento médio do resíduo; placebos: 2022 e 2018 nos mesmos estados.\n")
A("**Por que não rodou:** falta a tabela de coligações por estado (qual candidato a governador está aliado a qual candidato presidencial) e a leitura dos votos por candidato em todos os cargos por seção. Sem isso, qualquer mapeamento seria suposição. **Como fornecer:** o arquivo de candidatos e coligações do TSE (consulta de candidaturas, 2018, 2022, 2026) com a composição de cada coligação; quem o obtiver anexa por issue. É o teste que cobre o desvio uniforme; por isso é o primeiro da lista de tarefas.\n")
A('<a id="a23"></a>\n\n## A23. Fiscalização: NÃO EXECUTADO\n')
A("**Classe de falha coberta:** comportamento diferente onde há ou não fiscal. **Previsão sem manipulação:** sem diferença entre seções com e sem fiscal, dentro do mesmo local, com controle do 1º turno e de 2022. **Como fornecer o insumo (partidos e coligações):** uma planilha CSV com as colunas `uf;cd_municipio;zona;secao;turno;partido_ou_coligacao;fiscal_presente` (`sim` ou `nao`), sem nome nem documento de pessoa, enviada por issue. O script comparará seções com e sem fiscal e publicará o resultado, inclusive se for nulo.\n")
A('<a id="a24"></a>\n\n## A24. Experimento natural do teste de integridade: NÃO EXECUTADO\n')
A("**Classe de falha coberta:** urna que se comporta diferente quando não é o teste. **Desenho:** seções cuja urna foi para o teste (votaram em urna reserva) contra vizinhas do mesmo local, com controle do 1º turno e de 2022. **Por que não rodou:** a lista de seções afetadas não é pública. **Insumo:** pedido LAI 03 (`lai/03_teste_de_integridade.md`).\n")
A('<a id="a25"></a>\n\n## A25. Urnas substituídas (parcial)\n')
a6 = rd(R2, "registro_testes.csv"); a6 = a6[a6.H == "A6"]
A("**Classe de falha coberta:** troca de urna como ponto de intervenção. **Feito:** seções com urna diferente da esperada contra vizinhas do mesmo local ([A6](resultados-fase2.md)): " + "; ".join(f"{r.teste[:70]}... {r.veredito}" for r in a6.itertuples()) + ". **NÃO EXECUTADO:** voto antes x depois da troca pelos logs, porque o registro da urna original não é público. O total de 1.543 trocas no 1º turno citado ao autor não tem fonte localizada; a imprensa registra 421 até as 10h de 04/10/2026. **Insumo:** pedido LAI 01.\n")

# ---------------------------------------------------------------- A26
A('<a id="a26"></a>\n\n## A26. Integridade da publicação\n')
A("**Classe de falha coberta:** arquivo publicado alterado depois da publicação. **Rastro esperado:** hash oficial, tamanho ou data de modificação diferentes dos do primeiro download. **Previsão sem manipulação:** todos idênticos.\n")
A(f"**Resultado ({a26.consultado_em[:10]}):** dos {int(a26.arquivos)} arquivos de origem, {int(a26.status_200)} seguem disponíveis; o tamanho de {int(a26.tamanho_igual)} é igual ao do primeiro download; o hash oficial publicado hoje é igual ao do primeiro download em {int(a26.hash_igual)} de {int(a26.hash_conferido)} conferidos ({int(a26.hash_diferente)} diferentes); {int(a26.modificados_depois_do_primeiro_download)} têm data de modificação posterior ao primeiro download. **Arquivos alterados após a publicação: {int(a26.alterados)}.** Capturas no Wayback Machine: {int(a26.com_captura_no_wayback)} arquivos têm captura; {int(a26.wayback_indisponivel)} não puderam ser consultados (limite de taxa do serviço). " + (f"Das {int(a26.capturas_status_200_total)} capturas com resposta 200, {int(a26.capturas_com_digest_igual)} têm o mesmo resumo (SHA-1) do arquivo que baixei e {int(a26.capturas_com_digest_diferente)} têm resumo diferente (arquivos que o TSE republicou depois da captura, ou capturas parciais; cada caso está em `A26_integridade_publicacao.csv`)." if "capturas_status_200_total" in a26.index else "") + "\n")
A("**Limite:** os zips (cerca de 8 GB) não foram baixados de novo; foram comparados tamanho e hash oficial publicado. A reconferência integral é `data/baixar_e_verificar.sh`. Isso verifica que o que está publicado hoje é o que foi baixado; **não** verifica o que o TSE publicou antes do primeiro download. Dados em `results/fase3/A26_integridade_publicacao.csv`.\n")

A("### Arquivos republicados depois da captura no Wayback Machine\n")
a26d = rd(R3, "A26_integridade_publicacao.csv")
rep = a26d[(a26d.capturas_status_200.fillna(0) > a26d.capturas_com_digest_igual_ao_arquivo_atual.fillna(0))]
A(f"Em {int(a26.capturas_com_digest_diferente)} capturas de {len(rep)} arquivos o resumo (SHA-1) da captura é diferente do arquivo que baixei. Em todos eles a data de modificação publicada hoje é posterior à captura, o que indica **republicação pelo TSE depois da captura**, e não alteração depois do meu primeiro download (o tamanho de hoje é o do meu download e a data de modificação é anterior ao meu download; esses arquivos não têm hash oficial publicado). Para saber se a republicação mudou números, comparei seção a seção (cargo de Presidente) a captura com o arquivo atual:\n")
A(tab(rep[["arquivo", "last_modified_hoje", "baixado_em", "capturas_status_200", "primeira_captura_wayback"]].rename(columns={"last_modified_hoje": "modificado_em (GMT)", "baixado_em": "meu_download", "capturas_status_200": "capturas", "primeira_captura_wayback": "primeira_captura"}).assign(primeira_captura=lambda d: d.primeira_captura.astype("int64").astype(str).str[:8], capturas=lambda d: d.capturas.astype(int))))
A("")
for ano in (2022, 2018, 2026):
    f = os.path.join(R3, f"A26b_{ano}_resumo.csv")
    if not os.path.exists(f):
        continue
    r = rd(R3, f"A26b_{ano}_resumo.csv").iloc[0]; dc = rd(R3, f"A26b_{ano}_diferencas_por_coluna.csv")
    qt = dc[dc.coluna.str.startswith("QT_")]
    dif = dc[dc.secoes_diferentes > 0]
    A(f"- **detalhe_votacao_secao_{ano} (captura de {r.data_geracao_captura} contra o arquivo atual):** {n(r.secoes_comuns)} seções em comum, {n(r.secoes_so_na_captura)} só na captura, {n(r.secoes_so_no_atual)} só no arquivo atual. Colunas de votos e comparecimento (`QT_*`): **{n(int(qt.secoes_diferentes.sum()))} diferenças em {n(len(qt))} colunas**. Colunas com diferença: " + (", ".join(f"`{c}` ({n(int(k))})" for c, k in zip(dif.coluna, dif.secoes_diferentes)) if len(dif) else "nenhuma") + ". Colunas acrescentadas no arquivo atual: " + (", ".join(f"`{c}`" for c in str(r.colunas_so_no_atual).split(";")) if isinstance(r.colunas_so_no_atual, str) else "nenhuma") + ".")
A("\nLeitura: os números de votação e comparecimento da captura de novembro de 2022 e do arquivo de hoje são **iguais**; a republicação mudou rótulos, a identificação dos locais de votação e acrescentou colunas (inclusive os horários de recebimento do boletim, que por isso **não têm captura contemporânea** para 2018 e 2022). Para 2026, a captura de 07/10/2026 cobre só o 1º turno. Limite: só o cargo de Presidente foi comparado, e só os arquivos com captura no Wayback.\n")
# ---------------------------------------------------------------- A27
A('<a id="a27"></a>\n\n## A27. As 427 seções novas com comparecimento de 95% ou mais\n')
A("**Classe de falha coberta:** seções sem eleitores reais. **Rastro esperado:** local sem estrutura, perfil atípico, histórico do local. **Previsão sem manipulação:** explicadas pelo tipo de local e pelo porte (já em [H5](resultados-fase1.md)). **Definição:** das 639 seções do 2º turno com comparecimento ≥ 95%, 427 não existiam em 2022.\n")
pf = rd(R3, "A27_perfil.csv")[["grupo", "secoes", "aptos_mediana", "pct_local_ja_existia_em_2022", "secoes_no_local_mediana", "turnout_t1_medio", "turnout_t2_medio", "comparecimento", "margem_liquida_lula_menos_oponente", "pct_lula_validos"]]
A(tab(pf, {"secoes": n, "aptos_mediana": lambda x: n(float(x), 0), "pct_local_ja_existia_em_2022": lambda x: n(float(x), 1) + "%", "secoes_no_local_mediana": lambda x: n(float(x), 0), "turnout_t1_medio": lambda x: n(100 * float(x), 1) + "%", "turnout_t2_medio": lambda x: n(100 * float(x), 1) + "%", "comparecimento": n, "margem_liquida_lula_menos_oponente": n, "pct_lula_validos": lambda x: n(float(x), 1) + "%"}))
A("\nTipo de local, pelo nome e endereço (% das seções de cada grupo):\n")
tt = rd(R3, "A27_tipo_de_local.csv")
A(tab(tt))
A(f"\n**Leitura.** As 427 seções são pequenas (mediana de {n(pf.aptos_mediana.iloc[0], 0)} aptos contra {n(pf.aptos_mediana.iloc[3], 0)} no país), ficam em locais com poucas seções, e o comparecimento de 95% já aparece no 1º turno (média de {n(100 * pf.turnout_t1_medio.iloc[0], 0)}%). Locais rurais, de comunidade e indígenas estão sobre-representados ({n(tt.loc[tt.tipo_de_local_pelo_nome_e_endereco == 'rural_ou_comunidade', 'pct_427'].iloc[0], 1)}% e {n(tt.loc[tt.tipo_de_local_pelo_nome_e_endereco == 'indigena', 'pct_427'].iloc[0], 1)}% contra {n(tt.loc[tt.tipo_de_local_pelo_nome_e_endereco == 'rural_ou_comunidade', 'pct_todas'].iloc[0], 1)}% e {n(tt.loc[tt.tipo_de_local_pelo_nome_e_endereco == 'indigena', 'pct_todas'].iloc[0], 1)}% no país). Metade delas está em locais que já existiam em 2022. Lula tem {n(pf.pct_lula_validos.iloc[0], 1)}% dos votos válidos nelas.\n")
A(f"**Teto.** Contribuição líquida das 427 seções à margem: {n(pf.margem_liquida_lula_menos_oponente.iloc[0])} votos de margem. **Teto de pior caso, não estimativa:** {n(a27.votos_lula)} votos de margem ({n(100 * a27.votos_lula / MARGEM, 1)}% da margem), se todos os votos de Lula nessas seções fossem inválidos. **Situação:** TESTADO-INCONCLUSIVO. **NÃO EXECUTADO:** origem das transferências de eleitores para essas seções (exige o cadastro nominal) e histórico detalhado dos locais. **O que fecharia:** a lista de transferências por seção, pela Justiça Eleitoral. Tabelas em `results/fase3/A27_*.csv`.\n")

# ---------------------------------------------------------------- A28
A('<a id="a28"></a>\n\n## A28. Pedidos de acesso à informação (LAI)\n')
A("Seis pedidos redigidos, em `lai/`, com texto neutro, sem dados pessoais e sem acusação: urnas substituídas (horário e motivo), código de carga por urna, testes de integridade por UF, registros de recepção e totalização de 04/10 e 25/10, fiscais credenciados (agregado) e a documentação para verificar a assinatura. **Nenhum foi protocolado**; o registro de protocolos, prazos (20 dias, prorrogáveis por 10), respostas e negativas fica em `lai/registro.csv`.\n")
A(tab(pd.read_csv(os.path.join(RAIZ, "lai", "registro.csv"))[["arquivo", "destinatario", "assunto", "status"]]))
A("")
open(os.path.join(RAIZ, "docs", "fase3.md"), "w", encoding="utf-8").write("\n".join(L))
print("escrito docs/fase3.md")
