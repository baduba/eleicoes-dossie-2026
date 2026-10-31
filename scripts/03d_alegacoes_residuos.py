#!/usr/bin/env python3
"""docs/alegacoes.md (A16) e docs/residuos.md (A17), gerados dos resultados.
Uso: python -I 03d_alegacoes_residuos.py DIR_FASE2 RAIZ"""
import os, sys
import numpy as np
import pandas as pd

R, RAIZ = sys.argv[1], sys.argv[2]
MARGEM = 4_430_191
F3 = os.path.join(RAIZ, 'results', 'fase3')
rd3 = lambda f: pd.read_csv(os.path.join(F3, f))
rd = lambda f: pd.read_csv(os.path.join(R, f)) if os.path.exists(os.path.join(R, f)) else None


def n(x, d=0):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "n/d"
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tab(rows, cols):
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for r in rows:
        L.append("| " + " | ".join(str(r.get(c, "")).replace("|", "/").replace("\n", " ") for c in cols) + " |")
    return "\n".join(L)


reg = rd("registro_testes.csv")
a12c, a12e = rd("A12_a12_contagens.csv"), rd("A12_a12_esperado_vs_observado.csv")
a13 = rd("A13_a13_inversoes_e_trechos.csv"); a14 = rd("A14_a14_pontos_chave.csv"); a15 = rd("A15_a15_modelo_urna.csv"); a2 = rd("A2_a2_perdas.csv")
a5n = rd("A5_a5_estimativa_nacional_votos_apos_nominal.csv"); h3 = rd("H3_h3_recontagem_relogio_cru.csv"); tot = rd("H2_h2_totais_absolutos.csv").set_index(["ano", "turno"])
b12 = rd3("A12b_resumo_106.csv").iloc[0]
s12 = rd3("A12b_serie.csv"); s12 = s12[s12.universo.str.startswith("todas")].set_index(["ano", "turno"])
u12 = rd3("A12b_unanimes_x_zero_bn.csv"); u26 = u12[(u12.ano == 2026) & u12.conjunto.str.contains("PT")].iloc[0]
a31 = rd3("A31_sj_resumo.csv").iloc[0]
z26 = a12c[(a12c.ano == 2026) & (a12c.turno == 2) & (a12c.definicao == "todas as apuradas")].iloc[0]
c = lambda a, t, col: int(h3[(h3.ano == a) & (h3.turno == t) & (h3.recorte == "com exterior")][col].iloc[0])
x1934 = a14[(a14.ano == 2026) & (a14.turno == 2) & (a14.hora == "19:34")].iloc[0]
inv = a13.set_index(["ano", "turno"])

# ------------------------------------------------------------------------------------------------ A16
A16 = ["# Inventário de alegações\n",
       "Cada alegação é descrita nos termos em que foi informada ao autor desta auditoria, sem adjetivos sobre quem a fez. \"Quem fez\" e \"data\" aparecem como foram informados; quando não foram informados ou não foi localizada fonte, está escrito. Alegação sem conteúdo testável entra como **NÃO TESTÁVEL**, com o que a tornaria testável.\n"]
linhas = [
    dict(alegacao="Relatório \"pericial independente\": seções que fecharam depois das 17h, 8,6 milhões de liberações manuais, correlação com voto em Lula, seções unânimes, Benford, caso da Bahia", quem="documento anônimo (autoria não informada)", data="2026-10 (data exata n/d)", link="n/d (texto não fornecido a esta sessão)", testavel="sim, as contagens e a Bahia",
         teste="H1 a H8, A5 e a página [O relatório original](relatorio-original.md)", resultado=f"as contagens reproduzem ({n(c(2026,2,'de_17h01_a_17h15'))} seções; {n(tot.loc[(2026,2),'biom_nh_total'])} liberações; Bahia 72,31% x 71,31%); as conclusões não se sustentam", veredito="contagens reproduzidas; inferências refutadas"),
    dict(alegacao="Vídeo do \"Prof. Marcelo Trindade\": curva de apuração com trechos lineares, uma única inversão de liderança, \"472 urnas\" com 60-65%", quem="Marcelo Trindade (como informado)", data="n/d", link="[Instagram (reel)](https://www.instagram.com/reel/DfAHZs9g4Ej/): a página não traz transcrição acessível; o arquivo de transcrição (`trindade_transcricao.txt`) ainda não foi fornecido, então a alegação segue nos termos em que foi informada ao autor, sem adjetivos e sem checagem contra a fala", testavel="a forma da curva, sim; as \"472 urnas\", não",
         teste="A13 e A1", resultado=f"inversões reais: 2026/T2 {int(inv.loc[(2026,2),'inversoes_real'])}, 2022/T2 {int(inv.loc[(2022,2),'inversoes_real'])}, 2018/T2 {int(inv.loc[(2018,2),'inversoes_real'])}, 2026/T1 {int(inv.loc[(2026,1),'inversoes_real'])} (ordens geográficas de 2026/T2: {inv.loc[(2026,2),'inversoes_B_ic95']}); trechos lineares dentro da faixa simulada; o método de emendar subidas dá \"vitória\" falsa em séries sem manipulação (Haddad 2018: {n(100*inv.loc[(2018,2),'emenda_subidas_share_final_real'],1)}%). \"472 urnas\": NÃO REPRODUZÍVEL sem os dados e o código", veredito="forma da curva: dentro do esperado; \"472 urnas\": NÃO REPRODUZÍVEL"),
    dict(alegacao="\"O TSE tinha 70% das urnas apuradas às 19h34 e liberava aos poucos\"", quem="como informado (a captura sugere 7,28%)", data="25/10/2026", link="n/d", testavel="recebimento e totalização, sim; divulgação, não",
         teste="A14", resultado=f"às 19h34: {n(x1934.pct_bu_recebido,2)}% dos BUs recebidos e {n(x1934.pct_totalizado,2)}% totalizados; 70% só depois das 20h; atraso recebimento → totalização de menos de 1 minuto. Divulgação: NÃO EXECUTADO (sem snapshots)", veredito="70% às 19h34 não reproduz; represamento recebido → totalizado não aparece; divulgação NÃO TESTÁVEL sem snapshots"),
    dict(alegacao="\"Nenhuma oscilação de liderança\" na apuração", quem="como informado", data="n/d", link="n/d", testavel="sim", teste="A13", resultado=f"houve {int(inv.loc[(2026,2),'inversoes_real'])} inversões na ordem real de 2026/T2 (a partir de 1% das seções), {int(inv.loc[(2022,2),'inversoes_real'])} em 2022/T2 e 0 em 2018/T2 e 2026/T1", veredito="não reproduz como formulada; a contagem depende do limiar de 1% das seções"),
    dict(alegacao="Conversão de eleitores de Flávio para Lula entre os turnos", quem="como informado", data="n/d", link="n/d", testavel="só por agregado (falácia ecológica)", teste="A2, A3, A11",
         resultado="nacionalmente, nenhuma conversão é necessária (Lula +10,38 milhões, Flávio +3,72 milhões; a soma é exatamente o conjunto de votos disponíveis); a perda líquida do oponente por seção (383 mil votos) tem espelho em 2022 (PT, 459 mil)", veredito="não sustentada pelos dados agregados; individual NÃO TESTÁVEL (sigilo)"),
    dict(alegacao="109 seções com zero voto para Flávio", quem="como informado", data="n/d", link="n/d (nenhuma reportagem localizada)", testavel="sim", teste="A12",
         resultado=f"em 2026/T2: {n(z26.zero_oponente)} seções (1º turno: 81); o 109 não reproduz em nenhuma definição; o oponente teve zero voto em 143 (2022), 328 (2018) e 192 (2014) seções; observado próximo do esperado", veredito="109 não reproduz; contagem real não excede o esperado"),
    dict(alegacao="Imagem: \"106 urnas com 100% para Lula e 0% de branco, nulo e Flávio\"", quem="como informado (imagem; autoria n/d)", data="n/d", link="n/d (imagem sem fonte localizada)", testavel="sim", teste="A12b",
         resultado=(f"das {n(b12['secoes'])} seções com zero voto para Flávio em 2026/T2, {n(b12['com_zero_brancos_e_nulos'])} também têm zero brancos e zero nulos; as outras {n(b12['secoes'] - b12['com_zero_brancos_e_nulos'])} têm {n(b12['brancos'] + b12['nulos'])} brancos e nulos ({n(b12['bn_pct_do_comparecimento'], 1)}% do comparecimento). "
                    f"Esperado de tripla-zero pela taxa das vizinhas: {n(s12.loc[(2026, 2), 'esperado_pela_taxa_vizinha'], 1)}; razão observado/esperado {n(s12.loc[(2026, 2), 'observado_sobre_esperado'], 2)} (2022/T2: {n(s12.loc[(2022, 2), 'observado_sobre_esperado'], 2)}; 2018/T2: {n(s12.loc[(2018, 2), 'observado_sobre_esperado'], 2)}; 2014/T2: {n(s12.loc[(2014, 2), 'observado_sobre_esperado'], 2)}). "
                    f"Votos de Lula nas 106: {n(b12['votos_lula'])} (teto de pior caso, não estimativa: {n(b12['teto_a_pct_margem'], 2)}% da margem, se todos fossem inválidos; {n(b12['teto_b_pct_margem'], 2)}% se fossem trocados). O relatório original dizia \"100% dos votos válidos\" (seções unânimes com 30 válidos ou mais: {n(u26['secoes'])}, das quais {n(u26['com_zero_brancos_e_nulos'])} com zero brancos e nulos): essa afirmação admite brancos e nulos acima de zero; \"0% de brancos e nulos\" é mais forte e vale só para uma fração das seções."),
         veredito=f"\"0% de brancos e nulos\" não reproduz (só {n(b12['com_zero_brancos_e_nulos'])} de {n(b12['secoes'])}); o excesso de tripla-zero sobre o esperado existe em todas as eleições, com razão parecida ou maior em 2022 e 2018; o conjunto é o de A12, de menos de 0,35% da margem no pior caso"),
    dict(alegacao="Silva Jardim/RJ: \"Flávio +1, Lula +964, -104 eleitores\" entre o 1º e o 2º turno", quem="como informado", data="n/d", link="n/d", testavel="sim", teste="A31",
         resultado=f"nos dados do BWeb, Flávio +{n(a31['dF'])}, comparecimento {n(a31['dC'])} (aptos +{n(a31['d_aptos'])}) e Lula +{n(a31['dL'])}, não +964. Dentro da cauda esperada de 5.357 municípios (z = {n(a31['z'], 2)}, Holm 1,00); em 2026, 14,0% dos municípios tiveram o oponente com +1 voto ou menos (2022: 0,15%)",
         veredito="reproduz em parte (Lula +984, não +964); não é incomum entre os municípios de 2026; ver A31"),
    dict(alegacao="Apoios do 1º turno (Zema, Caiado, Cury, Clariana a Flávio; esquerda a Lula, crítico; Rui Costa Pimenta nulo; Renan Santos liberou)", quem="como informado", data="outubro de 2026", link="Conferido nome a nome em [O Povo, 10/10/2026](https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/10/quem-os-candidatos-a-presidente-derrotados-apoiam-no-2-turno.html): Zema, Caiado, Cury e Clariana Barão a Flávio; Hertz Dias e Edmilson Costa com voto crítico em Lula; Renan Santos neutro; Wilson Grassi sem posição. Divergências: Samara Martins só por orientação do partido (UP, \"vote 13\"); Rui Costa Pimenta com duas posições registradas: sem posição definida (O Povo, 10/10/2026) e voto nulo (Space Money, fonte indicada ao autor, não verificada por HTTP 403). Segunda fonte indicada (Space Money) responde HTTP 403 e não foi aberta. Complemento: [A Crítica](https://acritica.net/eleicoes-2026/caiado-zema-e-cury-apoiam-flavio-no-2o-turno-renan-santos-libera-eleitores/)", testavel="o efeito, só por agregado", teste="A11",
         resultado="ver [Resultados da Fase 2](resultados-fase2.md), seção A11 (contabilidade termo a termo e taxas aparentes, com a ressalva de falácia ecológica)", veredito="ver A11"),
    dict(alegacao="Modelos de urna antigos favoreciam Lula em 2022", quem="relatório do PL / Cerimedo (como informado)", data="n/d", link="n/d (texto não fornecido)", testavel="sim", teste="A15 e A10",
         resultado="UE2009 e UE2010 contra UE2020, mesmo local: sem controle do T1, efeito de ~+0,2 p.p. não distinguível de zero (como já no 1º turno); com o T1 como controle, −0,09 p.p., não significativo", veredito="não sustentada"),
    dict(alegacao="\"Fraude no processo\" (Suano)", quem="Suano (como informado)", data="n/d", link="n/d (conteúdo não fornecido; nenhuma fonte localizada)", testavel="NÃO TESTÁVEL como formulada",
         teste="nenhum", resultado="sem conteúdo específico a testar", veredito="NÃO TESTÁVEL. Ficaria testável se indicasse etapa do processo, local ou seções, dado ou documento e um critério verificável (por exemplo, um conjunto de boletins impressos para cruzar com o BWeb)"),
    dict(alegacao="\"A participação de Lula sobe linearmente com a taxa de liberação manual e passa de 61% nas seções com mais manual\"", quem="como informado", data="n/d", link="n/d", testavel="sim",
         teste="A40 (verificação exploratória em `results/exploratorio/ALE_*`)",
         resultado=("em 2026/T2 a curva por faixa de manual sobe de 51,1% (0-5%) até o máximo de 59,8% (acima de 30%), sem passar de 61% em nenhuma faixa. Os outros anos são mais altos e mais inclinados: 2022/T2 chega a 67,5%, 2018/T2 a 61,9% e 2026/T1 a 55,1%. "
                    "A correlação ponderada entre taxa manual e voto em Lula é a mais fraca da série em 2026/T2 (0,064), contra 0,145 em 2022/T2, 0,174 em 2018/T2 (com o PT fora do governo e derrotado) e 0,049 em 2026/T1. "
                    "A curva reflete geografia: a Bahia fica acima de 61% em toda faixa (efeito regional, não de manual) e São Paulo cai até 38,6% na faixa de 20-30%. Controlando por tipo de local, em escolas a curva vai de 51,9% a 66,6% e fora de escolas de 50,7% a 54,0%. Figura: [2026 x 2022 e controles](img/a40_curva_manual.png)"),
         veredito="REFUTADA na forma causal: em 2026 a curva não é linear, não passa de 61% em nenhuma faixa, é a mais fraca da série e já aparecia em 2018 (PT não incumbente e derrotado) e no 1º turno de 2026; a estrutura geográfica por trás já está documentada em H1, A20b, A32 e A33"),
]
A16.append(tab(linhas, ["alegacao", "quem", "data", "link", "testavel", "teste", "resultado", "veredito"]).replace("| alegacao | quem | data | link | testavel | teste | resultado | veredito |", "| alegação | quem fez | data | link | testável? | teste usado | resultado | veredito |"))
A16.append("\nAs demais alegações de pessoas e eventos citados no relatório original (por exemplo, \"apagão de 72 horas\", passaportes, Banco Master, mídia chinesa) não foram avaliadas: sem conteúdo testável com estes dados e sem fonte.\n")
open(os.path.join(RAIZ, "docs", "alegacoes.md"), "w", encoding="utf-8").write("\n".join(A16))

# ------------------------------------------------------------------------------------------------ A17
ITENS = [
    ("H1", "Flavio/Bolsonaro votos/apto", "Associação entre a taxa de liberação manual e votos de Flávio por apto no 2º turno, além do 1º turno", "a favor de Flávio",
     "efeito do modelo de urna (A10); composição do T1 com todos os candidatos e brancos/nulos (o coeficiente aumenta); comparecimento", "idade e escolaridade por seção; perfil do eleitor que precisa de liberação manual", "perfil por seção (idade, escolaridade) ou o registro das folhas de votação"),
    ("H5", "excesso sobre o esperado", "Seções com comparecimento ≥95%: 2,5 vezes o esperado pela composição de tipo de local e tamanho; presente já no 1º turno", "comparecimento (efeito possível em qualquer direção; teto calculado como se todos os votos extras fossem do PT)",
     "tipo de local, tamanho, seção nova, UF, taxa manual, atraso de fechamento, numerador contra denominador (nas seções antigas o numerador sobe 6%)", "cancelamento de títulos e revisão do eleitorado entre 2022 e 2026; composição etária por seção (o comparecimento de idosos cresce mais que os aptos, A9)", "cadastro por seção antes e depois da revisão do eleitorado"),
    ("H6", "secoes novas", "Seções novas têm +0,54 p.p. de Lula no T2 dado o T1 (2018: +1,34; 2022: 0)", "a favor de Lula",
     "interação com o T1, tamanho e comparecimento (o coeficiente é estável)", "composição por idade e renda; origem dos eleitores transferidos para as seções novas", "histórico de remanejamento de eleitores por seção"),
    ("H1", "S0 sem lag, Lula% ~ taxa manual", "Associação entre taxa de liberação manual e voto em Lula dentro do mesmo local, igual no 1º e no 2º turno de 2026 (0,07) e maior que em 2022", "a favor de Lula (associação, não efeito)",
     "controles de comparecimento, tamanho e modelo de urna: a associação permanece", "perfil por seção", "perfil por seção; modelo causal com instrumento para falha de biometria"),
    ("H2", "2022->2026", "Variação do voto em Lula entre anos contra variação da taxa manual: T2 contra T1 como placebo imperfeito", "a favor de Lula",
     "municípios com biometria nos dois anos; o T1 de 2026 tem candidatos diferentes do de 2022", "n/a", "placebo com candidatos comparáveis"),
    ("A1", "curva de apuracao", "Desvio da curva de apuração contra a permutação dentro da UF (teste de forma; sem conversão em votos)", "n/a",
     "o envelope é rejeitado em todos os anos; a partir de 10% das seções 2026/T2 fica abaixo dos placebos", "snapshots do site Resultados", "série de divulgação com horário"),
    ("A2", "oponente perde", "Frequência de seções em que o oponente perde votos absolutos (11,8% das seções; teste de forma)", "n/a",
     "espelho: em 2022 o PT perdeu em 12,6%; por faixa de terceiros/candidato as frequências são parecidas", "por que o líder do 1º turno perde votos absolutos onde há poucos terceiros", "pesquisa individual (painel)"),
    ("A3", "ecologica", "Coeficiente ecológico oponente no T1 → PT no T2 (2026 é o menos negativo; com EF de município, o mais negativo)", "a favor de Lula (diferença entre anos)",
     "efeito fixo de município; contabilidade por identidade", "conversão individual (sigilo)", "painel de eleitores ou dados de pesquisa pós-eleitoral"),
    ("A10", "UE2022", "Modelo de urna novo (UE2022) sem equivalente em 2022, teto de pior caso acima de 1% da margem por ser pouco preciso", "n/a",
     "dentro do mesmo local, o coeficiente é 0,0000", "n/a", "mais seções por modelo"),
    ("A11", "bloco pro-Flavio", "Coeficiente ecológico do bloco que apoiou Flávio para votos do PT, contra os placebos", "ver A11",
     "efeito fixo de município; Goodman restrito", "composição dos blocos e apoios sem fonte (esquerda, Clariana, Rui Costa Pimenta)", "pesquisa pós-eleitoral"),
    ("A12", "zero voto", "Seções com zero voto para o oponente (razão observado/esperado)", "a favor de Lula",
     "esperado pelo voto da seção no T1 e pelos vizinhos do mesmo local", "n/a", "n/a"),
    ("A5", "share de votos", "Associação entre votos depois do horário nominal e Lula% no mesmo local", "ver A5",
     "mesmo teste nas mesmas seções em 2022", "seções sem arquivo de urna", "log de todas as seções"),
    ("A15", "UE2009", "Modelo de urna UE2009/UE2010 em 2022 contra UE2020", "a favor de Lula",
     "o efeito sem controle do T1 é composição (também aparece no T1); com o T1, é nulo", "n/a", "n/a"),
]
L = ["# Questões em aberto (resíduos)\n",
     "> **Itens que os testes não conseguiram explicar nem confirmar. Não são evidência de nada, nem de um lado nem do outro: são lacunas que só dados novos fecham, e estão aqui para transparência e para investigação futura.**\n",
     "Entram nesta página todo resultado classificado como inconclusivo, \"excesso detectável\" ou \"excesso detectado\" e todo resíduo sem causa identificada. As estimativas centrais e os intervalos de 95% usam aproximação normal sobre o erro padrão do contraste contra o placebo mais exigente (não são bootstrap nem bayesianos). O **teto de pior caso** usa o placebo mais frouxo. Nenhuma probabilidade é atribuída a hipóteses sobre o processo; só aparecem quantidades medidas (votos em excesso, diferença entre anos). Margem oficial: 4.430.191 votos.\n"]
agg = {"PT": [], "OPO": []}
FLAW = {"A1", "A2", "A3", "A12"}
pos = rd("posregistro_testes.csv")
for h, trecho, titulo, direcao, testadas, nao_testadas, resolve in ITENS:
    r = reg[(reg.H == h) & reg.teste.str.contains(trecho, regex=False)]
    if not len(r):
        continue
    r = r.iloc[0]
    L.append(f"## {h}: {titulo}\n")
    L.append(f"- **Linha do registro:** {r.teste}")
    if h in FLAW:
        pr = pos[pos.H == h + "-corrigida"].iloc[0] if pos is not None and (pos.H == h + "-corrigida").any() else None
        L.append("- **RESSALVA DE DESENHO (leia primeiro):** o desenho pré-registrado desta linha produz o rótulo de excesso sem manipulação (demonstração e correção em [Resultados da Fase 2](resultados-fase2.md)). O rótulo abaixo **não indica manipulação**.")
        L.append(f"- **Pré-registrado (mantido):** {r.veredito}, com a ressalva de desenho acima" + (f" ({r.ressalva})" if isinstance(r.get('ressalva', ''), str) and r.get('ressalva', '') else ""))
        L.append(f"- **Corrigido (pós-registro):** {pr.veredito if pr is not None else 'n/d'}")
        L.append(f"- **Direção do efeito:** {direcao}")
        L.append("- **Estimativa em votos:** sem interpretação causal nesta linha; valores no Apêndice \"Agregado sem interpretação causal\" de Resultados da Fase 2.")
        L.append(f"- **Explicações mundanas testadas:** {testadas}")
        L.append(f"- **Não testadas:** {nao_testadas}")
        L.append(f"- **O que resolveria:** {resolve}")
        L.append("- **Causa:** o desenho do teste (ver ressalva); não há resíduo a explicar nesta linha.\n")
        continue
    L.append(f"- **Veredito pelo critério pré-registrado:** {r.veredito}" + (f" (ressalva de desenho: {r.ressalva})" if isinstance(r.get('ressalva', ''), str) and r.get('ressalva', '') else ""))
    L.append(f"- **Direção do efeito:** {direcao}")
    if pd.notna(r.get("votos_central")):
        L.append(f"- **Estimativa central:** {n(r.votos_central)} votos de margem (IC95 {n(r.votos_ic95_inf)} a {n(r.votos_ic95_sup)}), contra o placebo mais exigente ({r.comparador_exigente})")
        agg[r.sentido].append((r.votos_central, r.votos_ic95_inf, r.votos_ic95_sup, r.votos_max_pior_caso))
    else:
        L.append("- **Estimativa central:** não convertível em votos (teste de forma)")
    L.append(f"- **Teto de pior caso:** {n(r.votos_max_pior_caso) if pd.notna(r.votos_max_pior_caso) else 'n/d'} votos ({n(r.pct_pior_caso,2) if pd.notna(r.pct_pior_caso) else 'n/d'}% da margem)")
    L.append(f"- **Explicações mundanas testadas:** {testadas}")
    L.append(f"- **Não testadas:** {nao_testadas}")
    L.append(f"- **O que resolveria:** {resolve}")
    L.append("- **Causa:** não identificada.\n")
t1r = rd("A1T1_resumo.csv")
if t1r is not None:
    t1r = t1r.iloc[0]
    L.append("## A1 corrigido, 1º turno de 2026: trecho final da curva fora do envelope\n")
    L.append(f"- **O que se observa:** a curva do 1º turno fica fora do envelope do nulo corrigido por {int(t1r.maior_corrida)} pontos consecutivos (dos 76% aos 100% das seções, das 19h18 às 22h28 de 04/10/2026). O alvo pré-registrado do A1 é o 2º turno; esta linha é análise posterior.")
    L.append(f"- **Direção do efeito:** participação de Lula abaixo da mediana do nulo, com desvio decrescente até zero; maior desvio antes da janela de 19h às 20h.")
    L.append(f"- **Estimativa em votos:** não convertível em votos (teste de forma; a soma final é idêntica em qualquer ordem).")
    L.append(f"- **Explicações mundanas testadas:** coincidência com a janela do congestionamento de 19h às 20h: parcial ({int(t1r.pontos_fora_na_janela)} dos {int(t1r.pontos_fora)} pontos; a corrida começa na janela e continua depois); composição por UF: compatível, não demonstrada. Ver [A18](a18-alteracao-no-meio.md).")
    L.append("- **Não testadas:** ordem dos municípios dentro de cada UF por porte e por perfil de voto.")
    L.append("- **O que resolveria:** o log de recepção do Sistot (não público) e a ordem real de transmissão por município.")
    L.append("- **Causa:** não identificada.\n")
L.append("## Soma agregada: quantos votos, todos os resíduos juntos?\n")
L.append("> **Unidade: votos de margem** (variação da diferença Lula menos Flávio; a troca de um voto muda a margem em 2; definição em [Metodologia](metodologia.md)). Todos os números abaixo devem ser lidos contra a margem de 4.430.191. Para inverter o resultado, o conjunto dos efeitos **pró-Lula** teria de somar ao menos esse valor; efeitos pró-Flávio andam no sentido contrário e não entram nessa conta.\n")
FLAWS = {"A1", "A2", "A3", "A12"}
regv = reg[~reg.H.isin(FLAWS) & reg.votos_max_pior_caso.notna()]
pt, op = regv[regv.sentido == "PT"], regv[regv.sentido == "OPO"]
res_pt = agg["PT"]; res_op = agg["OPO"]
pos_c = lambda v: sum(max(x[0], 0) for x in v)
pior = lambda v: sum(max(x[3], 0) for x in v if pd.notna(x[3]))
dom = max(res_pt, key=lambda x: x[3] if pd.notna(x[3]) else 0)
TETO = " (teto de pior caso, não estimativa)"
rows = [
    dict(soma="**(1) Excesso medido: soma das estimativas centrais positivas dos itens desta página** (contra o placebo mais exigente; as negativas não compensam)", pro_Lula=f"**{n(pos_c(res_pt))}**", pct_margem_Lula=f"**{n(100 * pos_c(res_pt) / MARGEM, 2)}%**", pro_Flavio=f"**{n(pos_c(res_op))}**", pct_margem_Flavio=f"**{n(100 * pos_c(res_op) / MARGEM, 2)}%**"),
    dict(soma="(2) Tetos de pior caso dos itens desta página", pro_Lula=n(pior(res_pt)) + TETO, pct_margem_Lula=n(100 * pior(res_pt) / MARGEM, 1) + "%" + TETO, pro_Flavio=n(pior(res_op)) + TETO, pct_margem_Flavio=n(100 * pior(res_op) / MARGEM, 1) + "%" + TETO),
    dict(soma="(3) Idem (2), sem o maior item isolado (teto dominado pela imprecisão, ver abaixo)", pro_Lula=n(pior(res_pt) - dom[3]) + TETO, pct_margem_Lula=n(100 * (pior(res_pt) - dom[3]) / MARGEM, 1) + "%" + TETO, pro_Flavio=n(pior(res_op)) + TETO, pct_margem_Flavio=n(100 * pior(res_op) / MARGEM, 1) + "%" + TETO),
]
pd.DataFrame([dict(excesso_medido_pro_Lula_votos_de_margem=pos_c(res_pt), excesso_medido_pro_Flavio_votos_de_margem=pos_c(res_op))]).to_csv(os.path.join(R, "residuos_soma.csv"), index=False)
L.append(tab(rows, ["soma", "pro_Lula", "pct_margem_Lula", "pro_Flavio", "pct_margem_Flavio"]).replace("| pro_Lula |", "| pró-Lula (votos de margem) |").replace("| pro_Flavio |", "| pró-Flávio (votos de margem) |").replace("| pct_margem_Lula |", "| % da margem (pró-Lula) |").replace("| pct_margem_Flavio |", "| % da margem (pró-Flávio) |"))
L.append(f"\n**Leitura.** A linha (1) é o que os dados mostram de excesso: cerca de {n(pos_c(res_pt), 0)} votos de margem pró-Lula e {n(pos_c(res_op), 0)} pró-Flávio, ou seja, {n(100 * pos_c(res_pt) / MARGEM, 1)}% e {n(100 * pos_c(res_op) / MARGEM, 1)}% da margem. As linhas (2) e (3) são **tetos de pior caso, não estimativas**: usam sempre o placebo mais frouxo e somam como se tudo fosse independente. Em (2), o item de maior teto ({n(dom[3])} votos de margem) é uma especificação sem controle do 1º turno cujo teto vem da **imprecisão** do teste (o veredito é inconclusivo, não de excesso); sem ele, o conjunto cai para {n(100 * (pior(res_pt) - dom[3]) / MARGEM, 1)}% da margem. Nenhuma soma alcança 4.430.191. O limite vale para o que os testes medem; o que está fora da medição (os elos não publicados) segue aberto.\n")
L.append("O que isso **não** mede: uma alteração de votos coerente em todos os arquivos publicados, que estes testes não conseguem enxergar (ver [A18](a18-alteracao-no-meio.md) e [A19](a19-voto-digitado.md)). Também fica de fora o agregado de linhas com ressalva de desenho, que não tem interpretação causal (Apêndice B de [Resultados da Fase 2](resultados-fase2.md)). A soma ingênua de todas as linhas do registro está só no apêndice abaixo.\n")
APX = ["## Apêndice: Soma ingênua com dupla contagem, sem interpretação\n",
       f"> **Esta soma não mede votos alterados.** Ela soma os tetos de pior caso de **todas** as {len(pt)} linhas pró-Lula do registro (sem as quatro com ressalva de desenho) que têm conversão em votos, contando várias vezes as mesmas seções e as mesmas especificações (por exemplo, o teste de liberação manual em várias especificações e o de fechamento tardio em seis). Unidade: votos de margem. Teto de pior caso, não estimativa.\n",
       f"| soma | pró-Lula (votos de margem) | % da margem | pró-Flávio (votos de margem) |\n|---|---|---|---|\n| Soma ingênua com dupla contagem, sem interpretação (teto de pior caso, não estimativa) | {n(pt.votos_max_pior_caso.sum())} | {n(100 * pt.votos_max_pior_caso.sum() / MARGEM, 1)}% | {n(op.votos_max_pior_caso.sum())} |\n",
       "Mesmo com a dupla contagem, a soma não alcança 4.430.191 votos de margem.\n"]
L.append("## Itens sem linha no registro\n")
L.append("- **Comparecimento de idosos (A9):** o comparecimento de eleitores acima de 80 anos (voto facultativo) cresce mais que os aptos da faixa entre 2022 e 2026 no 1º turno. Não convertível em votos; causa não identificada; resolveria o perfil de 2026/2º turno e o histórico de cancelamentos de títulos.")
L.append("- **Chegada dos BUs de 25/10/2026:** 99,6% dos BUs chegaram ao TSE depois das 19h, enquanto 98,2% das seções tinham fechado até 15 minutos depois das 17h. Explicado pela pausa documentada pela imprensa; a fonte oficial não foi aberta.\n")
L.extend(APX)
open(os.path.join(RAIZ, "docs", "residuos.md"), "w", encoding="utf-8").write("\n".join(L))
print("escritos docs/alegacoes.md e docs/residuos.md")
