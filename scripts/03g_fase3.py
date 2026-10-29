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
a22t = rd(R3, "A22_testes_9b.csv"); a22r = rd(R3, "A22_resumo_9b.csv"); a22m = a22t.votos_max_pior_caso.max()
A(f"| [A22](#a22) Coerência entre cargos | desvio uniforme só no presidente | **NÃO EXECUTÁVEL com a regra registrada** (nenhuma UF de 2026 elegível). Variante exploratória (Adendo 9b), só AM e DF: INCONCLUSIVA | até {n(a22m)} votos de margem (teto de pior caso, não estimativa; {n(100 * a22m / MARGEM, 1)}% da margem), **só nos votos de AM e DF** | NÃO EXECUTADO (oficial); INCONCLUSIVA (exploratória) |")
A("| [A23](#a23) Fiscalização | comportamento diferente onde há ou não fiscal | **NÃO EXECUTADO** (sem lista de seções com fiscal) | n/a | NÃO EXECUTADO |")
A("| [A24](#a24) Experimento natural do teste de integridade | urna que se comporta diferente fora do teste | **NÃO EXECUTADO**: nenhuma lista de seções lida das publicações dos TREs (sites bloqueiam acesso automatizado); script e arquivo de entrada prontos | n/a | NÃO EXECUTADO |")
A("| [A25](#a25) Urnas substituídas | troca de urna como ponto de intervenção | seção com troca x vizinhas: ver A6 (sem efeito); antes x depois da troca: NÃO EXECUTADO | n/a (A6: teto abaixo de 1% da margem) | parcial |")
A(f"| [A26](#a26) Integridade da publicação | arquivo publicado alterado depois | {int(a26.arquivos)} arquivos: tamanho igual em {int(a26.tamanho_igual)}; hash oficial igual em {int(a26.hash_igual)} de {int(a26.hash_conferido)}; nenhum modificado depois do primeiro download | n/a | SEM ALTERAÇÃO DETECTADA |")
A(f"| [A27](#a27) Seções fabricadas | seções sem eleitores reais | 427 seções novas com comparecimento ≥ 95%: perfil abaixo | {n(a27.votos_lula)} votos de margem (teto de pior caso, não estimativa; {n(100 * a27.votos_lula / MARGEM, 1)}% da margem): todos os votos de Lula nas 427 seções, suposto inválidos | TESTADO-INCONCLUSIVO |")
A("| [A28](#a28) Pedidos LAI | dados que só o poder público tem | 6 pedidos prontos em `lai/`, com órgão e canal de cada um; **nenhum protocolado** | n/a | NÃO EXECUTADO |\n")

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
A('<a id="a22"></a>\n\n## A22. Coerência entre cargos\n')
A("**Classe de falha coberta:** desvio uniforme restrito ao cargo de presidente, invisível a testes de valor atípico. **Rastro esperado:** deslocamento sistemático entre a participação do candidato presidencial e a do governador alinhado a ele na mesma seção. **Previsão sem manipulação:** deslocamento de 2026 igual ao de 2022 e 2018. **Insumo usado:** tabelas de coligações do TSE (2018, 2022, 2026) e os BWebs de 2º turno dos três anos (votos por candidato e seção, presidente e governador). **Regra de alinhamento** (Adendo 9), decidida só pela composição das coligações, antes de olhar votos: o finalista a governador é alinhado a um candidato presidencial se mais da metade dos partidos da sua coligação (federações expandidas) está na coligação presidencial dele e menos da metade na do outro.\n")
al = rd(R3, "A22_alinhamento.csv"); al26 = al[al.ano == 2026]
A("**Resultado pela regra registrada: NÃO EXECUTÁVEL em 2026.** Das seis UFs com 2º turno de governador, nenhuma ficou com os dois finalistas alinhados a candidatos presidenciais diferentes. Motivo visível na composição: o oponente do PT concorreu à presidência por partido isolado (coligação de um só partido), então a coligação de um governador raramente passa de 50% em comum com ele; em AM a coligação do candidato do PT tem exatamente 50%, e a regra pede mais de 50%.\n")
A(tab(al26[["SG_UF", "cand1", "lado1", "cand2", "lado2", "elegivel"]].rename(columns={"lado1": "alinhamento 1", "lado2": "alinhamento 2"}).replace({"-": "nenhum", "A": "PT", "B": "oponente"}))); A("")
A("> **Desvio declarado (Adendo 9b), escrito depois de ver só a tabela acima e antes de ler qualquer voto de governador.** Variante exploratória: o finalista é alinhado a um candidato presidencial se o **partido** dele está na coligação ou federação do finalista e o do outro não está. Fica **fora da família principal** e **não substitui** a linha oficial NÃO EXECUTÁVEL.\n")
r9 = rd(R3, "A22_resumo_9b.csv"); u9 = rd(R3, "A22_deslocamento_por_UF_9b.csv")
A("**Variante 9b.** Deslocamento S = média, ponderada por votos válidos presidenciais, de (participação do candidato do PT para presidente) menos (participação do governador alinhado a ele); positivo quer dizer presidente à frente do governador. Erro padrão agrupado por município.\n")
A(tab(r9[["ano", "UFs_elegiveis", "secoes", "votos_validos_pres", "S", "ep", "municipios"]].fillna(""), {"secoes": lambda x: n(float(x)) if x != "" else "", "votos_validos_pres": lambda x: n(float(x)) if x != "" else "", "S": lambda x: n(100 * float(x), 2) + " p.p." if x != "" else "nenhuma UF elegível", "ep": lambda x: n(100 * float(x), 2) + " p.p." if x != "" else "", "municipios": lambda x: n(float(x)) if x != "" else ""}))
A("\nPor UF (mesma estatística):\n")
A(tab(u9[["ano", "SG_UF", "secoes", "votos_validos_pres", "S"]], {"secoes": n, "votos_validos_pres": n, "S": lambda x: n(100 * float(x), 2) + " p.p."}))
A("")
A(tab(a22t[["teste", "est_2026T2", "placebos", "p_excesso", "p_holm", "votos_max_pior_caso", "pct_pior_caso", "veredito"]], {"est_2026T2": lambda x: n(100 * float(x), 2) + " p.p.", "p_excesso": lambda x: n(float(x), 3), "p_holm": lambda x: n(float(x), 3), "votos_max_pior_caso": n, "pct_pior_caso": lambda x: n(float(x), 1) + "%"}))
A(f"\n> **Leitura e limites.** (1) São só duas UFs em 2026 (AM e DF), e o desvio entre UFs é grande nos dois sentidos: no placebo de 2022 o deslocamento por UF vai de {n(100 * u9[u9.ano == 2022].S.min(), 1)} a +{n(100 * u9[u9.ano == 2022].S.max(), 1)} p.p., e em 2026 vai de {n(100 * u9[u9.ano == 2026].S.min(), 1)} a +{n(100 * u9[u9.ano == 2026].S.max(), 1)} p.p. O erro padrão agrupado por município (63 municípios em 2026) **não captura essa variação entre UFs**; com duas UFs ela não é estimável. Os valores de 2026 ficam dentro do intervalo de 2022 por UF, mas isso é descrição, não teste pré-registrado. (2) Os tetos valem **apenas** para os {n(float(r9[r9.ano == 2026].votos_validos_pres.iloc[0]))} votos válidos de AM e DF; **não** cobrem o país. São **teto de pior caso, não estimativa**, e saem grandes porque o teste tem pouco poder. (3) O sinal de S em 2026 é negativo (candidato do PT atrás do governador alinhado), o que não é o sentido de uma inflação a favor dele. (4) Resultado: **INCONCLUSIVA**; a linha oficial de A22 continua **NÃO EXECUTADO** (regra registrada sem UF elegível). **O que fecharia:** os votos por candidato em todos os cargos por seção para as 27 UFs, com uma regra de alinhamento definida por quem conhece as alianças locais (por exemplo, partidos que declararam apoio formal); ou deputados federais por partido nas UFs sem 2º turno de governador.\n")
A("Dados: `results/fase3/A22_*.csv`; script `scripts/32_a22_coerencia_cargos.py`; tabelas de coligações em `data/urls_origem.txt` com SHA-256 em `data/sha256_entradas.txt`.\n")
A('<a id="a23"></a>\n\n## A23. Fiscalização: NÃO EXECUTADO\n')
A("**Classe de falha coberta:** comportamento diferente onde há ou não fiscal. **Previsão sem manipulação:** sem diferença entre seções com e sem fiscal, dentro do mesmo local, com controle do 1º turno e de 2022. **Como fornecer o insumo (partidos e coligações):** uma planilha CSV com as colunas `uf;cd_municipio;zona;secao;turno;partido_ou_coligacao;fiscal_presente` (`sim` ou `nao`), sem nome nem documento de pessoa, enviada por issue. O script comparará seções com e sem fiscal e publicará o resultado, inclusive se for nulo.\n")
A('<a id="a24"></a>\n\n## A24. Experimento natural do teste de integridade: NÃO EXECUTADO\n')
A("**Classe de falha coberta:** urna que se comporta diferente quando não é o teste. **Desenho** (Adendos 8, 9 e 9c): seções cuja urna foi sorteada para o teste (votaram em urna reserva) contra as demais seções do mesmo local, com efeito fixo de local e controle do 1º turno; comparador: 2022/T2 com o mesmo controle; a diferença do 1º turno de 2026 sem controle é balanço pré-tratamento. **O que foi feito:** a lista de seções deve vir das **publicações dos TREs**, uma fonte por UF. O levantamento está em `data/a24_fontes_por_uf.csv`: foram localizadas páginas de 9 TREs (SP, SE, SC, PB, MA, MG, MT, ES, DF) com notícia do sorteio; **nenhuma lista de zona e seção foi lida**, porque os sites dos TREs respondem 403 a acesso automatizado (o projeto não disfarça o agente para contornar o bloqueio) e os resumos de busca trazem a quantidade de urnas, não a tabela. Para as demais UFs a página não foi localizada nesta rodada.\n")
A("**Resultado:** NÃO EXECUTADO (regra do Adendo 9: menos de 10 seções lidas). O script `scripts/33_a24_teste_integridade.py` está pronto e foi testado com uma lista sintética de 80 seções ao acaso, descartada, que serviu para achar e corrigir um defeito de desenho (Adendo 9c). **Como fornecer o insumo:** preencher `data/a24_secoes_teste_integridade.csv` (UF, município, zona, seção, turno, tipo de teste, biometria, URL da publicação do TRE e data de acesso; uma linha por seção) e rodar o script; ou enviar a planilha por issue. **Poder esperado:** com 20 a 30 seções por UF e turno e desvio local de 1,67 p.p., o teste só vê diferenças médias acima de cerca de 1 p.p. com 100 seções; o script informa o menor efeito detectável. **Pedido LAI relacionado:** `lai/03_teste_de_integridade.md`.\n")
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
A("Seis pedidos prontos, em `lai/`, com texto neutro, sem dados pessoais e sem acusação, cada um com **órgão e canal** definidos. **Nenhum foi protocolado**; o registro de protocolos, prazos (20 dias, prorrogáveis por 10), respostas e negativas fica em `lai/registro.csv`. Quem recebe cada pedido e por quê está em `lai/canais.csv`; os 27 TREs estão em `lai/canais_tres.csv`.\n")
A("| pedido | assunto | órgão | canal |\n|---|---|---|---|")
reg_ = pd.read_csv(os.path.join(RAIZ, "lai", "registro.csv"))
for r_ in reg_.itertuples():
    A(f"| `{r_.arquivo}` | {r_.assunto} | {r_.destinatario} | " + ("Formulário Eletrônico da Ouvidoria do TSE (SIC)" if r_.destinatario == "TSE" else ("Formulário Eletrônico da Ouvidoria do TSE e e-SIC de cada TRE" if "TSE" in r_.destinatario and "TRE" in r_.destinatario else "e-SIC de cada TRE")) + " |")
A("\n**Estado da verificação dos canais.** O TSE e os TREs bloqueiam acesso automatizado (403). O canal do TSE (Formulário Eletrônico da Ouvidoria, Resolução TSE 23.435/2015, alterada pela 23.583/2018) foi conferido em resultado de busca, não abrindo o formulário; para os TREs há página de SIC vista em resultado de busca para 6 UFs (SP, BA, AM, GO, RJ, AP) e as outras 21 estão como **a confirmar no protocolo**. A identificação de quem pede é exigida (Resolução CNJ 215/2015, art. 11, § 2º, segundo o TRE-SP); o projeto não tem autor nominal, então quem protocola assina o pedido. Confirme o canal, os campos e o prazo no sistema na hora de protocolar.\n")
A("")
open(os.path.join(RAIZ, "docs", "fase3.md"), "w", encoding="utf-8").write("\n".join(L))
print("escrito docs/fase3.md")
