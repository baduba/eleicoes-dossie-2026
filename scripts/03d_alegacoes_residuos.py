#!/usr/bin/env python3
"""docs/alegacoes.md (A16) e docs/residuos.md (A17), gerados dos resultados.
Uso: python -I 03d_alegacoes_residuos.py DIR_FASE2 RAIZ"""
import os, sys
import numpy as np
import pandas as pd

R, RAIZ = sys.argv[1], sys.argv[2]
MARGEM = 4_430_191
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
    dict(alegacao="Vídeo do \"Prof. Marcelo Trindade\": curva de apuração com trechos lineares, uma única inversão de liderança, \"472 urnas\" com 60-65%", quem="Marcelo Trindade (como informado)", data="n/d", link="n/d (vídeo não fornecido; nenhuma fonte localizada)", testavel="a forma da curva, sim; as \"472 urnas\", não",
         teste="A13 e A1", resultado=f"inversões reais: 2026/T2 {int(inv.loc[(2026,2),'inversoes_real'])}, 2022/T2 {int(inv.loc[(2022,2),'inversoes_real'])}, 2018/T2 {int(inv.loc[(2018,2),'inversoes_real'])}, 2026/T1 {int(inv.loc[(2026,1),'inversoes_real'])} (ordens geográficas de 2026/T2: {inv.loc[(2026,2),'inversoes_B_ic95']}); trechos lineares dentro da faixa simulada; o método de emendar subidas dá \"vitória\" falsa em séries sem manipulação (Haddad 2018: {n(100*inv.loc[(2018,2),'emenda_subidas_share_final_real'],1)}%). \"472 urnas\": NÃO REPRODUZÍVEL sem os dados e o código", veredito="forma da curva: dentro do esperado; \"472 urnas\": NÃO REPRODUZÍVEL"),
    dict(alegacao="\"O TSE tinha 70% das urnas apuradas às 19h34 e liberava aos poucos\"", quem="como informado (a captura sugere 7,28%)", data="25/10/2026", link="n/d", testavel="recebimento e totalização, sim; divulgação, não",
         teste="A14", resultado=f"às 19h34: {n(x1934.pct_bu_recebido,2)}% dos BUs recebidos e {n(x1934.pct_totalizado,2)}% totalizados; 70% só depois das 20h; atraso recebimento → totalização de menos de 1 minuto. Divulgação: NÃO EXECUTADO (sem snapshots)", veredito="70% às 19h34 não reproduz; represamento recebido → totalizado não aparece; divulgação NÃO TESTÁVEL sem snapshots"),
    dict(alegacao="\"Nenhuma oscilação de liderança\" na apuração", quem="como informado", data="n/d", link="n/d", testavel="sim", teste="A13", resultado=f"houve {int(inv.loc[(2026,2),'inversoes_real'])} inversões na ordem real de 2026/T2 (a partir de 1% das seções), {int(inv.loc[(2022,2),'inversoes_real'])} em 2022/T2 e 0 em 2018/T2 e 2026/T1", veredito="não reproduz como formulada; a contagem depende do limiar de 1% das seções"),
    dict(alegacao="Conversão de eleitores de Flávio para Lula entre os turnos", quem="como informado", data="n/d", link="n/d", testavel="só por agregado (falácia ecológica)", teste="A2, A3, A11",
         resultado="nacionalmente, nenhuma conversão é necessária (Lula +10,38 milhões, Flávio +3,72 milhões; a soma é exatamente o conjunto de votos disponíveis); a perda líquida do oponente por seção (383 mil votos) tem espelho em 2022 (PT, 459 mil)", veredito="não sustentada pelos dados agregados; individual NÃO TESTÁVEL (sigilo)"),
    dict(alegacao="109 seções com zero voto para Flávio", quem="como informado", data="n/d", link="n/d (nenhuma reportagem localizada)", testavel="sim", teste="A12",
         resultado=f"em 2026/T2: {n(z26.zero_oponente)} seções (1º turno: 81); o 109 não reproduz em nenhuma definição; o oponente teve zero voto em 143 (2022), 328 (2018) e 192 (2014) seções; observado próximo do esperado", veredito="109 não reproduz; contagem real não excede o esperado"),
    dict(alegacao="Apoios do 1º turno (Zema, Caiado, Cury, Clariana a Flávio; esquerda a Lula, crítico; Rui Costa Pimenta nulo; Renan Santos liberou)", quem="como informado", data="outubro de 2026", link="Zema, Caiado, Cury e Renan: [A Crítica](https://acritica.net/eleicoes-2026/caiado-zema-e-cury-apoiam-flavio-no-2o-turno-renan-santos-libera-eleitores/); demais: fonte não localizada", testavel="o efeito, só por agregado", teste="A11",
         resultado="ver [Resultados da Fase 2](resultados-fase2.md), seção A11 (contabilidade termo a termo e taxas aparentes, com a ressalva de falácia ecológica)", veredito="ver A11"),
    dict(alegacao="Modelos de urna antigos favoreciam Lula em 2022", quem="relatório do PL / Cerimedo (como informado)", data="n/d", link="n/d (texto não fornecido)", testavel="sim", teste="A15 e A10",
         resultado="UE2009 e UE2010 contra UE2020, mesmo local: sem controle do T1, efeito de ~+0,2 p.p. não distinguível de zero (como já no 1º turno); com o T1 como controle, −0,09 p.p., não significativo", veredito="não sustentada"),
    dict(alegacao="\"Fraude no processo\" (Suano)", quem="Suano (como informado)", data="n/d", link="n/d (conteúdo não fornecido; nenhuma fonte localizada)", testavel="NÃO TESTÁVEL como formulada",
         teste="nenhum", resultado="sem conteúdo específico a testar", veredito="NÃO TESTÁVEL. Ficaria testável se indicasse etapa do processo, local ou seções, dado ou documento e um critério verificável (por exemplo, um conjunto de boletins impressos para cruzar com o BWeb)"),
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
     "> **Itens que os testes não conseguiram explicar nem confirmar. Não constituem evidência de manipulação; estão aqui para transparência e para investigação futura.**\n",
     "Entram nesta página todo resultado classificado como inconclusivo, \"excesso detectável\" ou \"excesso detectado\" e todo resíduo sem causa identificada. As estimativas centrais e os intervalos de 95% usam aproximação normal sobre o erro padrão do contraste contra o placebo mais exigente (não são bootstrap nem bayesianos). O **teto de pior caso** usa o placebo mais frouxo. Nenhuma probabilidade é atribuída a hipóteses sobre o processo; só aparecem quantidades medidas (votos em excesso, diferença entre anos). Margem oficial: 4.430.191 votos.\n"]
agg = {"PT": [], "OPO": []}
for h, trecho, titulo, direcao, testadas, nao_testadas, resolve in ITENS:
    r = reg[(reg.H == h) & reg.teste.str.contains(trecho, regex=False)]
    if not len(r):
        continue
    r = r.iloc[0]
    L.append(f"## {h}: {titulo}\n")
    L.append(f"- **Linha do registro:** {r.teste}")
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
L.append("## Soma agregada\n")
rows = []
for sent, nome in (("PT", "pró-Lula"), ("OPO", "pró-Flávio")):
    v = agg[sent]
    if v:
        cen = sum(x[0] for x in v); dp = np.sqrt(sum(((x[2] - x[0]) / 1.96) ** 2 for x in v)); pw = sum(max(x[3], 0) for x in v if pd.notna(x[3]))
        rows.append(dict(sentido=nome, itens_com_votos=len(v), soma_central=n(cen), ic95=f"{n(cen - 1.96 * dp)} a {n(cen + 1.96 * dp)}", soma_pior_caso=n(pw), pct_margem_central=n(100 * cen / MARGEM, 2) + "%", pct_margem_pior_caso=n(100 * pw / MARGEM, 2) + "%"))
L.append(tab(rows, ["sentido", "itens_com_votos", "soma_central", "ic95", "soma_pior_caso", "pct_margem_central", "pct_margem_pior_caso"]))
L.append("\nO intervalo da soma supõe independência entre os itens (aproximação declarada; os itens usam as mesmas seções, então o intervalo é aproximado). Os sentidos pró-Lula e pró-Flávio não se compensam. Itens de forma, sem conversão em votos, não entram na soma. Nenhum item, isolado ou somado, alcança a margem de 4.430.191 votos.\n")
L.append("## Itens sem linha no registro\n")
L.append("- **Comparecimento de idosos (A9):** o comparecimento de eleitores acima de 80 anos (voto facultativo) cresce mais que os aptos da faixa entre 2022 e 2026 no 1º turno. Não convertível em votos; causa não identificada; resolveria o perfil de 2026/2º turno e o histórico de cancelamentos de títulos.")
L.append("- **Chegada dos BUs de 25/10/2026:** 99,6% dos BUs chegaram ao TSE depois das 19h, enquanto 98,2% das seções tinham fechado até 15 minutos depois das 17h. Explicado pela pausa documentada pela imprensa; a fonte oficial não foi aberta.\n")
open(os.path.join(RAIZ, "docs", "residuos.md"), "w", encoding="utf-8").write("\n".join(L))
print("escritos docs/alegacoes.md e docs/residuos.md")
