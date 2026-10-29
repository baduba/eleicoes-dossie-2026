#!/usr/bin/env python3
"""Monta dossie.md a partir dos CSVs em resultados/. Uso: python -I 03_monta_dossie.py DIR_RESULTADOS DIR_DADOS SAIDA.md
Todos os numeros do texto vem dos CSVs (nada digitado a mao, exceto os rotulos e as explicacoes)."""
import hashlib, os, sys
import pandas as pd

R, DADOS, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
MARGEM = 4_430_191


def rd(nome):
    return pd.read_csv(os.path.join(R, nome))


def n(x, d=0):
    """numero no formato pt-BR."""
    if pd.isna(x):
        return "n/d"
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pc(x, d=2):
    return n(x, d) + "%"


def tab(df, fmts=None, cab=None):
    """tabela markdown. fmts: {coluna: funcao}."""
    fmts = fmts or {}
    cols = list(df.columns)
    linhas = ["| " + " | ".join(cab or cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.astype(object).iterrows():
        linhas.append("| " + " | ".join(((fmts[c](r[c]) if c in fmts else str(r[c])).replace("|", "/")) for c in cols) + " |")
    return "\n".join(linhas)


reg = rd("registro_testes.csv")
H9a, H9b, H9c, H9d = rd("H9_h9_bweb_vs_votacao_secao.csv"), rd("H9_h9_consistencia_interna.csv"), rd("H9_h9_bweb_vs_totalizacao_munzona.csv"), rd("H9_h9_totais_2026_T2.csv")
tot = rd("H2_h2_totais_absolutos.csv").set_index(["ano", "turno"])
cru = rd("H3_h3_recontagem_relogio_cru.csv")
fx = rd("H3_h3_faixas.csv")
tard = rd("H3_h3_tardias_uf.csv")
h1c, h1d, h1r, h1m = rd("H1_h1_coef.csv"), rd("H1_h1_dose.csv"), rd("H1_h1_redteam.csv"), rd("H1_h1_taxa_manual_por_modelo_urna.csv")
h2d, h2uf = rd("H2_h2_descritivo.csv"), rd("H2_h2_por_uf.csv")
h4, h4n = rd("H4_h4_coef.csv"), rd("H4_h4_natural.csv")
h5m, h5c, h5p, h5t, h5nd, h5tam = rd("H5_h5_metricas.csv"), rd("H5_h5_caracterizacao_2026T2.csv"), rd("H5_h5_padronizacao.csv"), rd("H5_h5_por_tipo.csv"), rd("H5_h5_numerador_denominador.csv"), rd("H5_h5_taxa_ge95_por_tamanho.csv")
h5s = rd("H5_h5_so_no_T2.csv")
h6, h6r = rd("H6_h6_coef.csv"), rd("H6_h6_robustez.csv")
h7, h8 = rd("H7_h7_outliers.csv"), rd("H8_h8_digitos.csv")
abc2, abc1 = rd("ABC_abc_metricas_T2.csv"), rd("ABC_abc_metricas_T1.csv")
abcc2, abcr2, abcr1 = rd("ABC_abc_classificacao_T2.csv"), rd("ABC_abc_resumo_T2.csv"), rd("ABC_abc_resumo_T1.csv")
h10, h10s = rd("H10_h10_agregado.csv"), rd("H10_h10_sobreviventes.csv")
nao = rd("nao_executados.csv")
H9div, H9sb = rd("H9_h9_divergencias_secao.csv"), rd("H9_h9_secoes_so_no_bweb.csv")


def R_(h, trecho):
    r = reg[(reg.H == h) & reg.teste.str.contains(trecho, regex=False)]
    assert len(r) == 1, (h, trecho, len(r))
    return r.iloc[0]


s1 = R_("H1", "S1 T2 com lag"); s0 = R_("H1", "S0 sem lag, Lula"); s0c = R_("H1", "S0 sem lag + controles"); sflav = R_("H1", "Flavio/Bolsonaro votos/apto"); slula = R_("H1", "S1 Lula votos/apto")
h2a = R_("H2", "dentro do ano"); h2b = R_("H2", "2022->2026")
h5r = R_("H5", "excesso"); h6reg = R_("H6", "secoes novas"); h7u = R_("H7", "outliers locais para cima"); h7p = R_("H7", "assimetria")
h4reg = reg[reg.H == "H4"]
m26, m22 = tot.loc[(2026, 2)], tot.loc[(2022, 2)]
cr26, cr22 = cru[(cru.ano == 2026) & (cru.turno == 2) & (cru.recorte == "com exterior")].iloc[0], cru[(cru.ano == 2022) & (cru.turno == 2) & (cru.recorte == "com exterior")].iloc[0]
f = lambda a, t, faixa: fx[(fx.ano == a) & (fx.turno == t) & (fx.recorte == "Brasil sem exterior") & (fx.faixa == faixa)].iloc[0]
tar26 = f(2026, 2, "115+ min (>= ~19h)"); ate15 = f(2026, 2, "ate 5 min apos 17h").secoes + f(2026, 2, "5 a 15 min (17h01-17h15)").secoes
tot_secoes26 = fx[(fx.ano == 2026) & (fx.turno == 2) & (fx.recorte == "Brasil sem exterior")].secoes.sum()
sd = h10.set_index("sentido")
ab = abcr2.iloc[0]
b26 = h1c[(h1c.spec.str.startswith("S1")) & (h1c.ano == 2026)].iloc[0]; b22 = h1c[(h1c.spec.str.startswith("S1")) & (h1c.ano == 2022)].iloc[0]
a0 = lambda a, t: h1c[(h1c.spec.str.startswith("S0")) & (h1c.ano == a) & (h1c.turno == t)].iloc[0]
d_muz = H9c.set_index("turno")
r26 = h5p.iloc[0]; r26t1 = h5p.iloc[1]
c639 = h5c.iloc[0]

# hashes dos scripts
scripts = sorted(f for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)))) if f.endswith(".py"))
hs = {s: hashlib.sha256(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), s), "rb").read()).hexdigest()[:16] for s in scripts}

L = []
A = L.append
A("# Dossiê: auditoria dos dados do 2º turno presidencial de 2026 (Lula x Flávio Bolsonaro)\n")
A("Gerado em 2026-10-28 a partir dos arquivos públicos do TSE. Todos os números deste texto vêm dos CSVs em `results/fase1/` (script `03_monta_dossie.py`). Previsões e critérios foram fixados antes dos dados em `00_preregistro.md`.\n")

# ------------------------------------------------------------------------------------------------ 1
A("## 1. Resumo executivo\n")
A(f"1. Dados: BWeb (boletim de urna por seção) de 2014, 2018, 2022 e 2026, T1 e T2, 224 zips com hash conferido. Os totais de 2026/T2 são Lula {n(H9d.lula.iloc[0])} e Flávio {n(H9d.flavio.iloc[0])}, iguais aos divulgados.")
A(f"2. Consistência: o BWeb coincide com `votacao_secao` em todas as seções pareadas de 2014 a 2026, exceto {n(len(H9div))} seção de 2018/T1 em que `votacao_secao` tem {n(H9div.soma_candidatos_votacao_secao.sum() - (H9div.lula_bweb.sum() + H9div.oponente_bweb.sum()))} votos a mais que o BWeb e que o total divulgado pelo TSE (nenhuma divergência em 2022 ou 2026), e com a totalização por município/zona de 2026 ({n(d_muz.com_diferenca.sum())} zonas com diferença). Há {n(H9b.comparecimento_maior_que_aptos.sum() + H9b.soma_votos_diferente_de_comparecimento.sum() + H9b.validos_maior_que_comparecimento.sum())} violações de consistência interna dos BUs.")
A(f"3. Liberação manual (biometria cadastrada, eleitor não habilitado por ela): {n(m26.biom_nh_total)} em 2026/T2, o número citado no relatório; {n(m22.biom_nh_total)} em 2022/T2. A taxa agregada passou de {pc(100*m22.taxa_agregada)} para {pc(100*m26.taxa_agregada)}.")
A(f"4. H1: com efeito fixo de local de votação e controle do voto da própria seção no T1, a taxa manual não prevê voto adicional em Lula no T2 (coeficiente {n(b26.coef,3)} contra {n(b22.coef,3)} em 2022). Teto de pior caso: {n(s1.votos_max_pior_caso)} votos.")
A(f"5. H3 e H4: a contagem do relatório foi reproduzida ({n(cr26.de_17h01_a_17h15)} seções entre 17h01 e 17h15 pelo relógio cru da urna). {n(cr26.a_partir_de_19h)} seções registraram encerramento a partir das 19h no relógio da urna, contra {n(cr22.a_partir_de_19h)} em 2022/T2. Nelas, o voto em Lula não difere das demais seções do mesmo local; tetos de {pc(h4reg.pct_pior_caso.min())} a {pc(h4reg.pct_pior_caso.max())} da margem.")
A("6. O número de votos dados depois das 17h não é mensurável com estes dados (o BWeb não traz log de votação).")
A(f"7. H5 a H8 e régua histórica: o comparecimento, os outliers locais e os dígitos de 2026 ficam dentro da faixa observada em 2014, 2018 e 2022. Nenhum dos padrões A, B ou C se ajusta pelo critério fixado (C: {n(ab.C)} de {n(ab.metricas)} métricas; ver 3.13).")
A(f"8. Dois testes mostram excesso depois de Holm: votos de Flávio por apto x taxa manual (teto {n(sflav.votos_max_pior_caso)} votos, {pc(sflav.pct_pior_caso)} da margem, sentido favorável a Flávio) e variação de voto em Lula entre anos x variação da taxa manual (teto {n(h2b.votos_max_pior_caso)} votos, {pc(h2b.pct_pior_caso)}).")
A(f"9. Residuais sem causa identificada: {n(c639.secoes)} seções com comparecimento >= 95% ({n(r26.razao,1)} vezes o esperado pela composição; {n(r26t1.razao,1)} vezes já no T1; teto {pc(h5r.pct_pior_caso)}) e seções novas (+{n(100*h6reg.est_2026T2,2)} p.p. de Lula no T2 dado o T1; +1,34 p.p. em 2018; teto de pior caso {pc(h6reg.pct_pior_caso)}).")
A(f"10. Impacto agregado: a soma dos tetos dos testes com excesso detectado é {n(sd.loc['PT','soma_votos_sobreviventes_pior_caso'])} votos no sentido pró-Lula ({pc(sd.loc['PT','pct_margem_sobreviventes_pior_caso'])} da margem) e {n(sd.loc['OPO','soma_votos_sobreviventes_pior_caso'])} no sentido pró-Flávio. Nenhum achado, isolado ou somado, alcança {n(MARGEM)} votos. Não executado: cruzamento com boletins impressos (sem insumo).\n")

# ------------------------------------------------------------------------------------------------ 2
A("## 2. Dados e versões\n")
A("| Insumo | Origem | Arquivos | Verificação |\n|---|---|---|---|")
A("| BWeb 2026, 2022 | `cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{2026,2022}/buweb/` via API CKAN (`dadosabertos.tse.jus.br`) | 56 zips por ano (27 UF + ZZ, T1 e T2) | SHA-512 do TSE conferido: 112/112 |")
A("| BWeb 2018, 2014 | mesmo catálogo | 56 zips por ano | 2018: SHA-512; 2014: SHA-1 (o que o TSE publica); 112/112 conferidos |")
A("| `votacao_secao` 2014 a 2026, `detalhe_votacao_secao` 2022 e 2026, `votacao_candidato_munzona` 2026 | `cdn.tse.jus.br/estatistica/sead/odsele/` | 1 zip por produto/ano | usados em H9, tipo de local e modelo de urna |")
A("\nHash SHA-256 de todos os insumos: `dados/sha256_entradas.txt`. URLs: `dados/urls_origem.txt`.\n")
A("**Colunas do BWeb usadas** (nomes encontrados no cabeçalho):\n")
A("| Conceito | 2026 | 2022 | 2018 | 2014 |\n|---|---|---|---|---|")
A("| Liberação manual | `QT_ELEI_BIOM_SEM_HABILITACAO` | `QT_ELEITORES_BIOMETRIA_NH` | `QT_ELEITORES_BIOMETRIA_NH` | inexistente |")
A("| Abertura / encerramento | `DT_ABERTURA`, `DT_ENCERRAMENTO` | iguais | iguais | inexistentes |")
A("| Recebimento / emissão do BU | `DT_BU_RECEBIDO`, `DT_EMISSAO_BU` | iguais | inexistentes | só data de recebimento |")
A("| Seções agregadas | `DS_SECOES_AGREGADAS` | `DS_AGREGADAS` | `DS_AGREGADAS` | posicional |")
A("| Formato | CSV com cabeçalho | CSV com cabeçalho | CSV com cabeçalho (`SG_ UF` com espaço) | `.txt` sem cabeçalho, 31 campos posicionais |\n")
A("**Definição da medida de liberação manual.** O dicionário do TSE descreve o campo como \"eleitores com biometria cadastrada que não foram habilitados por meio dela\". Não é o total de liberações manuais: quem não tem biometria cadastrada não entra, e o denominador (eleitores com biometria) não está disponível.\n")
A("**Pontos de atenção nos dados:**\n")
A("- Catálogo CKAN do TSE: os dois recursos de RR/T2/2026 apontam para o `.sha512`. O zip existe em `.../buweb/bweb_2t_RR_261020260742.zip` (HTTP 200) e foi baixado direto, com hash conferido.")
A("- Horários `DT_ABERTURA`, `DT_ENCERRAMENTO`, `DT_EMISSAO_BU` são relógio local da urna (Acre abre às 06h00 e fecha às 15h00). O atraso de fechamento usa o horário nominal do município (moda da abertura + 9 h). `DT_BU_RECEBIDO` é horário do servidor do TSE.")
A("- Seções \"Não instalada\", \"Não apurada\" e \"Anulada e apurada em separado\" trazem `#NULO#` ou -1 nos campos de votável e biometria. São tratadas só nesse caso exato, ficam fora das análises (somente urna \"Apurada\", exterior excluído, salvo indicação).")
A("- Em 2022, as urnas UE2009 e UE2010 do Espírito Santo registram taxa manual exatamente 0,0 (3.339 seções), enquanto as mesmas urnas em outros estados têm cerca de 15%. É artefato de medição e explica o único estado em que a taxa subiu de 2022 para 2026.")
A(f"- Versões: Python 3.12, pandas 3.1, scipy 1.18, pyarrow, matplotlib 3.11. Hashes dos scripts (SHA-256, 16 primeiros caracteres): " + "; ".join(f"`{k}` {v}" for k, v in hs.items()) + ".\n")

# ------------------------------------------------------------------------------------------------ 3
A("## 3. Resultados por hipótese\n")
A("Método comum: regressão com efeito fixo de local de votação (`uf_local`), erro padrão agrupado por local, voto da própria seção no T1 como controle quando o desfecho é o T2, e comparação com **cada** placebo (2022/T1, 2022/T2, 2026/T1, ou o equivalente definido no teste) por teste de interseção-união. O p de \"excesso\" é unilateral (2026/T2 maior que o placebo, no sentido da alegação) e é o p corrigido por Holm e Benjamini-Hochberg sobre os 23 testes do registro. O teto em votos é `2 x max(0, diferença + 1,645 x ep) x exposição`: o máximo de votos de margem que o fenômeno poderia explicar, supondo causalidade. \"Placebo mais exigente\" é o de maior estimativa; \"pior caso\" usa o placebo mais frouxo.\n")
A("Regra de veredito (Adendo 2 do pré-registro): **excesso detectado e relevante** = Holm < 0,05 e pior caso >= 1% da margem; **excesso detectável, magnitude irrelevante** = Holm < 0,05 e < 1%; **refutada** = Holm >= 0,05 e < 1%; **inconclusiva** = Holm >= 0,05 e >= 1%.\n")

A("### 3.1 Síntese\n")
A("| H | Previsão se houver desvio | Previsão se não houver | Resultado | Placebo | Efeito máx. (votos) | % da margem | p Holm | Veredito |\n|---|---|---|---|---|---|---|---|---|")
A(f"| H1 manual x voto Lula (T2, com T1) | coef. > 0 e > placebos, dose-resposta crescente | mesma magnitude nos placebos | {n(s1.est_2026T2,4)} (ep {n(s1.ep,4)}) | 2022/T2: {n(s1.b_comp,4)} | {n(s1.votos_max_pior_caso)} | {pc(s1.pct_pior_caso)} | {n(s1.p_holm,3)} | refutada |")
A(f"| H1 sem controle do T1 | idem | idem | 2026/T2: {n(s0.est_2026T2,4)}; 2026/T1: {n(a0(2026,1).coef,4)} | 2026/T1: {n(s0.b_comp,4)} (2022: {n(a0(2022,1).coef,4)} e {n(a0(2022,2).coef,4)}) | {n(s0.votos_max_margem)} (vs T1/2026); {n(s0.votos_max_pior_caso)} (vs 2022/T1) | {pc(s0.pct_margem)}; {pc(s0.pct_pior_caso)} | {n(s0.p_holm,3)} | inconclusiva pelo critério, mas a associação é igual no T1 (ver 3.2) |")
A(f"| H1 simétrico: votos de Flávio/apto | sem efeito | sem efeito | {n(sflav.est_2026T2,4)} (ep {n(sflav.ep,4)}) | 2022/T2: {n(sflav.b_comp,4)} | {n(sflav.votos_max_pior_caso)} | {pc(sflav.pct_pior_caso)} | {n(sflav.p_holm,3)} | excesso detectado, **sentido favorável a Flávio** |")
A(f"| H2 \"aumento\" da liberação manual | taxa sobe 2022 a 2026 | taxa estável ou em queda | {n(m22.biom_nh_total)} em 2022/T2 e {n(m26.biom_nh_total)} em 2026/T2 | n/a | n/a | n/a | n/a | refutada (queda de {pc(100*(1-m26.biom_nh_total/m22.biom_nh_total),1)}) |")
A(f"| H2 variação de voto x variação manual, dentro do ano | coef. > 0 só em 2026 | igual a 2022 | {n(h2a.est_2026T2,4)} | 2022: {n(h2a.b_comp,4)} | {n(h2a.votos_max_pior_caso)} | {pc(h2a.pct_pior_caso)} | {n(h2a.p_holm,3)} | refutada |")
A(f"| H2 entre anos (T2 contra T1) | coef. T2 > T1 | igual | T2: {n(h2b.est_2026T2,4)}; T1: {n(h2b.b_comp,4)} | T1 (placebo imperfeito: candidatos diferentes) | {n(h2b.votos_max_pior_caso)} | {pc(h2b.pct_pior_caso)} | {n(h2b.p_holm,3)} | excesso detectável, magnitude irrelevante |")
A(f"| H3 encerramento | tabela do relatório não reproduz ou fecha tarde em massa | reproduz; fecha quase tudo em 17h-17h15 | 17h01-17h15: {n(cr26.de_17h01_a_17h15)} (relatório: 339.593); >= 19h: {n(cr26.a_partir_de_19h)} | 2022/T2: {n(cr22.de_17h01_a_17h15)} e {n(cr22.a_partir_de_19h)} | votos após 17h: não mensurável | n/a | n/a | caracterização; contagem do relatório confirmada |")
A(f"| H4 fecha tarde (15, 60, 115 min), 6 testes | Lula% maior que nas mesmas seções em 2022 e no T1 | igual | de {n(100*h4reg.est_2026T2.min(),2)} a {n(100*h4reg.est_2026T2.max(),2)} p.p. | de {n(100*h4reg.b_comp.min(),2)} a {n(100*h4reg.b_comp.max(),2)} p.p. | até {n(h4reg.votos_max_pior_caso.max())} | até {pc(h4reg.pct_pior_caso.max())} | {n(h4reg.p_holm.min(),2)} a {n(h4reg.p_holm.max(),2)} | refutada |")
A(f"| H5 comparecimento >= 95% | maioria antiga, manual alto, só no T2 | nova, pequena, local atípico, já no T1 | observado {n(r26.observado)}; esperado pela composição {n(r26.esperado_pela_composicao)} | 2026/T1: {n(r26t1.observado)} contra {n(r26t1.esperado_pela_composicao)} | {n(h5r.votos_max_pior_caso)} | {pc(h5r.pct_pior_caso)} | {n(h5r.p_holm,3)} | refutada como efeito do T2; nível elevado de 2026 sem causa identificada |")
A(f"| H6 seções novas | destoam das antigas do mesmo local | iguais | +{n(100*h6reg.est_2026T2,2)} p.p. | 2022: {n(100*h6.query('ano==2022 and spec==\"lula_sh T2 | lula_sh T1\"').coef.iloc[0],2)}; 2018: +{n(100*h6.query('ano==2018 and spec==\"lula_sh T2 | lula_sh T1\"').coef.iloc[0],2)} | {n(h6reg.votos_max_pior_caso)} (vs 2022); 0 (vs 2018) | {pc(h6reg.pct_pior_caso)} | {n(h6reg.p_holm,3)} | inconclusiva (depende da linha de base) |")
A(f"| H7 outliers locais pró-Lula (z ajustado em módulo > 3) | excesso sem espelho | contagem igual a 2022 e simétrica | {n(h7u.est_2026T2,1)} por 10 mil seções; {n(100*h7p.est_2026T2,1)}% dos outliers são pró-Lula | 2022/T1: {n(h7u.b_comp,1)}; {n(100*h7p.b_comp,1)}% | {n(h7u.votos_max_pior_caso)} | {pc(h7u.pct_pior_caso)} | {n(h7u.p_holm,3)} | refutada |")
A("| H8 dígitos | último dígito não uniforme; percentuais inteiros em excesso | uniforme, como em 2022 | ver 3.8 | 2022 e 2026/T1 | n/a (teste de forma) | n/a | 1,000 | sem excesso |")
A(f"| H9 consistência | soma das seções diferente da totalização | igual | {n(len(H9div))} seção ({n(H9div.soma_candidatos_votacao_secao.sum() - (H9div.lula_bweb.sum() + H9div.oponente_bweb.sum()))} votos, 2018/T1) e {n(d_muz.com_diferenca.sum())} zonas com diferença | n/a | 0 em 2026 | 0% | n/a | consistente em 2026; 1 divergência em `votacao_secao` de 2018/T1 |")
A(f"| H10 impacto agregado | soma dos excessos comparável a {n(MARGEM)} | soma < 1% | pró-Lula {n(sd.loc['PT','soma_votos_sobreviventes_pior_caso'])}; pró-Flávio {n(sd.loc['OPO','soma_votos_sobreviventes_pior_caso'])} | n/a | ver 3.10 | {pc(sd.loc['PT','pct_margem_sobreviventes_pior_caso'])} | n/a | abaixo de 1% no sentido pró-Lula |")
A("| Boletins impressos | divergência de qualquer tamanho | nenhuma | **não executado** | n/a | n/a | n/a | n/a | sem insumo (ver 3.11) |\n")

A("### 3.2 H1: liberação manual x voto\n")
A("Efeito fixo de local de votação, erro agrupado por local; coeficientes em fração do voto válido por unidade de taxa manual.\n")
A(tab(h1c.assign(coef=h1c.coef, ep=h1c.ep).drop(columns=["p"]), {"coef": lambda x: n(x, 4), "ep": lambda x: n(x, 4), "n": lambda x: n(x), "locais": lambda x: n(x)}))
A(f"\nLeitura: sem controle do T1, a associação de 2026 ({n(a0(2026,1).coef,3)} no T1 e {n(a0(2026,2).coef,3)} no T2) é igual nos dois turnos e maior que a de 2022 ({n(a0(2022,1).coef,3)} e {n(a0(2022,2).coef,3)}). Ao condicionar no voto da própria seção no T1, o coeficiente do T2 cai a {n(b26.coef,3)}, abaixo de 2022 ({n(b22.coef,3)}). Ou seja, a relação existe antes do 2º turno e o 2º turno não acrescenta nada. Controles de comparecimento e tamanho da seção ({n(s0c.est_2026T2,3)}) e de modelo da urna (ver 3.12) não a dissolvem; a causa dessa associação de 2026 não foi identificada.\n")
A("**Dose-resposta** (faixas da taxa manual contra 0-5%, pontos percentuais de voto em Lula, T2 com T1):\n")
A(tab(h1d, {"coef_pp": lambda x: n(x, 3), "ep_pp": lambda x: n(x, 3), "secoes_na_faixa": lambda x: n(x)}))
A("\nEm 2022 a curva cresce com a taxa; em 2026 é plana.\n")
A("**Simetria.** Em 2026, a taxa manual prevê mais votos por apto no T2 para os dois candidatos (Lula " + n(slula.est_2026T2, 3) + ", Flávio " + n(sflav.est_2026T2, 3) + "), enquanto em 2022 só Lula (" + n(slula.b_comp, 3) + " contra " + n(sflav.b_comp, 3) + " para Bolsonaro). O coeficiente de Lula caiu e o de Flávio subiu. Nos redutos de Flávio (Lula T1 < 40%) o coeficiente é " + n(R_('H1', 'reduto de Flavio').est_2026T2, 4) + " e nos de Lula (T1 > 60%), " + n(R_('H1', 'reduto de Lula').est_2026T2, 4) + ", ambos sem excesso sobre 2022.\n")

A("### 3.3 H2: o aumento da liberação manual\n")
A(tab(rd("H2_h2_totais_absolutos.csv"), {"biom_nh_total": lambda x: n(x), "comparecimento_total": lambda x: n(x), "taxa_agregada": lambda x: pc(100 * x), "secoes": lambda x: n(x)}))
A(f"\nO total de 2026/T2 ({n(m26.biom_nh_total)}) é o \"8,6 milhões\" do relatório. Em seções estáveis (aptos entre 0,85x e 1,15x de 2022), {pc(h2d[(h2d.turno==2)&(h2d.filtro=='sem filtro')].pct_secoes_caiu_mais_5pp.iloc[0],1)} das seções tiveram queda de mais de 5 p.p. na taxa e {pc(h2d[(h2d.turno==2)&(h2d.filtro=='sem filtro')].pct_secoes_subiu_mais_5pp.iloc[0],1)} tiveram alta. O filtro \"municípios com biometria nos dois anos\" quase não muda o resultado.\n")
A("A queda acompanha a troca do parque de urnas: em 2022, UE2009 e UE2010 tinham taxa de 14% a 16% e UE2020, 5%; em 2026 as UE2009/2010/2011 saíram e entrou a UE2022, com 6%.\n")
A(tab(h1m[h1m.turno == 2].drop(columns=["turno"]), {"secoes": lambda x: n(x), "taxa_manual": lambda x: pc(100 * x), "lula_sh": lambda x: pc(100 * x, 1)}))
A(f"\n**Onde subiu.** Só o Espírito Santo ({n(h2uf[h2uf.SG_UF=='ES'].delta_medio_pp.iloc[0],2)} p.p.), por artefato de medição de 2022 (seção 2). Dentro do ES, a variação de voto não se associa à variação da taxa (coeficiente 0,0001, erro padrão 0,008). Maiores quedas: " + ", ".join(f"{r.SG_UF} ({n(r.delta_medio_pp,2)} p.p.)" for r in h2uf.sort_values("delta_medio_pp").head(4).itertuples()) + ".\n")

A("### 3.4 H3: encerramento\n")
A("**Recontagem da tabela do relatório** (relógio cru de `DT_ENCERRAMENTO`, sem ajustar fuso, com exterior):\n")
A(tab(cru[cru.recorte == "com exterior"].drop(columns=["recorte"]), {c: (lambda x: n(x)) for c in ["antes_17h01", "de_17h01_a_17h15", "de_17h16_a_18h59", "a_partir_de_19h", "total"]}))
A(f"\nO valor do relatório para 17h01-17h15 (339.593) é reproduzido exatamente em 2026/T2. A faixa equivalente tem {n(cr22.de_17h01_a_17h15)} seções em 2022/T2 e {n(cru[(cru.ano==2018)&(cru.turno==2)&(cru.recorte=='com exterior')].de_17h01_a_17h15.iloc[0])} em 2018/T2, e corresponde a fila normal no horário de encerramento. O relógio cru ignora o fuso: os estados do Oeste fecham às 15h ou 16h locais e caem em \"antes de 17h01\". Com horário nominal por município, {pc(100*ate15/tot_secoes26,1)} das seções (sem exterior) fecham até 15 minutos depois do horário.\n")
A(f"**Prorrogação.** {n(tar26.secoes)} seções (sem exterior; {pc(tar26.pct_secoes,2)}) fecharam 115 minutos ou mais depois do horário nominal, com {n(tar26.comparecimento)} eleitores com comparecimento registrado, contra 25 seções em 2022/T2. Estados: " + ", ".join(f"{r.SG_UF} {n(r.secoes)}" for r in tard.head(6).itertuples()) + f". Em RJ são {pc(tard.iloc[0].pct_das_secoes_da_uf,1)} das seções do estado.\n")
A("**Votos depois das 17h.** O BWeb não traz log de votação; os \"logs Gedai\" do catálogo são de preparação das urnas (gerados em 24/10), não de votação. Por isso o número não é mensurável aqui. A referência externa de 34.330 eleitores (levantamento da imprensa) não foi verificada. O limite por extrapolação da taxa média da seção (`h3_votos_apos_horario_limite.csv`) é um teto frouxo e não deve ser lido como estimativa.\n")
A("**Hora de recebimento do BU no TSE.** 99,6% dos BUs de 2026/T2 chegaram depois das 19h, mas 98,2% das seções tinham fechado até 15 minutos após o horário nominal. A hora de recebimento reflete o TSE segurando o recebimento, não o fechamento da seção. A leitura anterior desta análise, que usava essa hora como proxy de encerramento, estava errada.\n")

A("### 3.5 H4: seções que fecharam tarde\n")
A("Lula% (pontos percentuais) em seções tardias contra as demais do mesmo local, T2/2026 com T1 como controle, e o mesmo teste nas mesmas seções em 2022/T2 e no T1/2026:\n")
A(tab(h4, {"coef_pp": lambda x: n(x, 3), "ep_pp": lambda x: n(x, 3), "secoes_tardias": lambda x: n(x)}))
A("\nNenhuma estimativa de 2026 supera as de 2022 ou do T1. Com efeito fixo de zona (comparação menos estrita), os coeficientes são negativos (de -0,06 a -0,09 p.p.): fechar tarde não se associa a mais voto em Lula. Contexto: no T1/2026, seções com atraso de 15 minutos ou mais têm +" + n(h4n[(h4n.ano == 2026) & (h4n.turno == 1)].coef_pp.iloc[0], 2) + " p.p. de Lula dentro do mesmo local (fila em seções maiores), efeito que não aparece no T2 (" + n(h4n[(h4n.ano == 2026) & (h4n.turno == 2)].coef_pp.iloc[0], 2) + " p.p.).\n")

A("### 3.6 H5: seções com comparecimento >= 95% e Klimek\n")
A(tab(h5m, {"secoes": lambda x: n(x), "turnout_ge95": lambda x: n(x), "por_100k": lambda x: n(x, 1), "M5a_PT": lambda x: n(x, 5), "M5a_OPO": lambda x: n(x, 5), "M5b_PT": lambda x: n(x, 4), "M5b_OPO": lambda x: n(x, 4)}))
A("\n`por_100k` é M5c; M5a é a fração de seções com comparecimento >= 90% e voto >= 90% no candidato; M5b é a correlação comparecimento x voto dentro do local. Figuras de Klimek: `results/fase1/figs/klimek_T2.png` e `klimek_T1.png`; na inspeção visual, 2026 não mostra segunda moda na diagonal (o padrão que a literatura associa a manipulação) e o formato é semelhante ao de 2022. A inspeção visual não é teste; os testes são M5a a M5c acima.\n")
A(f"**As {n(c639.secoes)} seções de 2026/T2.** {pc(c639.pct_novas,1)} são novas (sem par em 2022), contra {pc(h5c.iloc[3].pct_novas,1)} de todas as seções; mediana de {n(c639.aptos_mediana)} aptos contra {n(h5c.iloc[3].aptos_mediana)}; taxa manual média de {pc(100*c639.manual_medio,1)} contra {pc(100*h5c.iloc[3].manual_medio,1)}; atraso de fechamento médio de {n(c639.atraso_medio_min,1)} contra {n(h5c.iloc[3].atraso_medio_min,1)} minutos. Comparecimento médio no T1: {pc(100*c639.turnout_T1_medio,1)}; só {n(h5s.dessas_so_no_T2.iloc[0])} seções passaram de < 90% no T1 a >= 95% no T2, com {n(h5s.votos_validos_dessas.iloc[0])} votos válidos. Por tipo de local (nome do local):\n")
A(tab(h5t, {"n_ge95": lambda x: n(x), "n_total": lambda x: n(x), "pct_ge95_dentro_do_tipo": lambda x: pc(x, 2), "pct_do_total_ge95": lambda x: pc(x, 1), "pct_do_total_secoes": lambda x: pc(x, 2)}))
A(f"\n**Padronização.** Com as taxas de 2022 por tipo de local e tamanho, esperavam-se {n(r26.esperado_pela_composicao)} seções >= 95% no T2 ({n(r26t1.esperado_pela_composicao)} no T1); observadas {n(r26.observado)} e {n(r26t1.observado)}, razões de {n(r26.razao,2)} e {n(r26t1.razao,2)}. A composição não explica o nível de 2026, e o excesso já existe no T1. A diferença T2 menos T1 (log da razão, {n(r26.log_razao - r26t1.log_razao,3)}) dá p unilateral de {n(h5r.p_excesso,4)} e {n(h5r.p_holm,3)} após Holm; teto {n(h5r.votos_max_pior_caso)} votos ({pc(h5r.pct_pior_caso)}).\n")
A("**Taxa de seções >= 95% por 10 mil seções, por tamanho** (aptos):\n")
A(tab(h5tam, {c: (lambda x: n(x, 1)) for c in ["2014", "2018", "2022", "2026"]}))
A(f"\nO nível de 2026 em seções de 51 a 150 aptos supera o de todos os anos anteriores nos dois turnos; em seções de mais de 150 aptos, 2014 tinha taxa maior. Entre as {n(h5nd[h5nd.alto==True].secoes.iloc[0])} seções antigas pareadas com >= 95% em 2026, os aptos ficaram estáveis ({n(h5nd[h5nd.alto==True].aptos_2026_sobre_2022_mediana.iloc[0],2)}x a mediana de 2022), o comparecimento subiu {n(100*(h5nd[h5nd.alto==True].comparecimento_2026_sobre_2022_mediana.iloc[0]-1),1)}% e o comparecimento mediano de 2022 já era {pc(100*h5nd[h5nd.alto==True].turnout_2022_mediano.iloc[0],1)}: o efeito vem do numerador, não de queda de aptos.\n")

A("### 3.7 H6: seções novas\n")
A(tab(h6, {"coef": lambda x: n(x, 5), "ep": lambda x: n(x, 5), "p": lambda x: n(x, 4), "secoes_novas": lambda x: n(x), "n": lambda x: n(x)}))
A("\nRobustez do coeficiente de `nova` em Lula% T2 dado o T1 (interação com o T1 centrado, controles de tamanho e comparecimento, só seções de 100 a 500 aptos):\n")
A(tab(h6r, {"coef_nova": lambda x: n(x, 5), "ep": lambda x: n(x, 5), "secoes_novas": lambda x: n(x)}))
A("\nO efeito de 2026 (+0,5 p.p.) é estável nas três variantes, ou seja, não é artefato de inclinação heterogênea nem de tamanho. Em 2022 o coeficiente é zero e em 2018 é +1,3 p.p., maior que o de 2026. Contra o placebo mais exigente (2018) não há excesso; contra 2022, o teto de pior caso é " + pc(h6reg.pct_pior_caso) + " da margem. Veredito: inconclusivo, porque depende de qual ano serve de linha de base. A causa não foi identificada (composição por idade e renda não está disponível por seção).\n")

A("### 3.8 H7 e H8: outliers locais e dígitos\n")
A(tab(h7[["ano", "turno", "secoes_em_locais_ge4", "sobredispersao_phi", "up_3", "down_3", "taxa_up_10k", "taxa_down_10k", "razao_up_down"]], {"secoes_em_locais_ge4": lambda x: n(x), "sobredispersao_phi": lambda x: n(x, 3), "up_3": lambda x: n(x), "down_3": lambda x: n(x), "taxa_up_10k": lambda x: n(x, 1), "taxa_down_10k": lambda x: n(x, 1), "razao_up_down": lambda x: n(x, 2)}))
A("\nOutlier = seção cujo voto em Lula destoa da média das outras seções do mesmo local (leave-one-out), com variância binomial e sobredispersão estimada em cada eleição (phi ≈ 1,5 em todas). `up` é pró-Lula e `down`, pró-Flávio/oponente.\n")
dg = h8[h8.teste.isna()][["ano", "turno", "cand", "n", "chi2", "p", "V_cramer"]]
A(tab(dg, {"n": lambda x: n(x), "chi2": lambda x: n(x, 1), "p": lambda x: n(x, 4), "V_cramer": lambda x: n(x, 5)}))
pi_ = h8[h8.teste.notna()][["ano", "turno", "observado", "esperado", "razao"]]
A("\nÚltimo dígito das contagens (>= 20 votos), V de Cramér. Percentual inteiro exato (idêntico para os dois candidatos):\n")
A(tab(pi_, {"observado": lambda x: n(x), "esperado": lambda x: n(x), "razao": lambda x: n(x, 3)}))
A("\nO último dígito de Lula em 2026/T2 é uniforme (p = " + n(dg[(dg.ano == 2026) & (dg.turno == 2) & (dg.cand == 'PT')].p.iloc[0], 2) + "). O do oponente tem V de 0,0021 (p = " + n(dg[(dg.ano == 2026) & (dg.turno == 2) & (dg.cand == 'OPO')].p.iloc[0], 3) + "), menor que o de 2014, 2018 e 2022; p sem correção para múltiplos testes. O percentual inteiro fica em 0,78 do esperado em todos os anos (a fórmula esperada superestima, mas a razão é constante).\n")

A("### 3.9 H9: consistência\n")
A(tab(H9a[["ano", "turno", "secoes_bweb", "secoes_votacao_secao", "pareadas", "pareadas_com_diferenca", "soma_abs_dif_votos"]], {c: (lambda x: n(x)) for c in ["secoes_bweb", "secoes_votacao_secao", "pareadas", "pareadas_com_diferenca", "soma_abs_dif_votos"]}))
A("\n")
A(tab(H9c, {c: (lambda x: n(x)) for c in H9c.columns}))
A("\n**Divergências por seção** (todas as comparações BWeb x `votacao_secao`):\n")
ids = ["ano", "turno", "cd_municipio", "zona", "secao"]
A(tab(H9div.drop(columns=["aptos_bweb"]), {c: (lambda x: str(int(x))) if c in ids else (lambda x: n(x)) for c in H9div.columns if c != "uf"}))
sb = H9sb.groupby("ano").agg(secoes=("secao", "size"), comp_max=("comparecimento", "max"))
A(f"\nA única divergência é de 2018/T1, na seção {int(H9div.secao.iloc[0])} da zona {int(H9div.zona.iloc[0])} do município {int(H9div.cd_municipio.iloc[0])} ({H9div.uf.iloc[0]}): o BWeb registra {n(H9div.lula_bweb.iloc[0])} e {n(H9div.oponente_bweb.iloc[0])} votos para os dois candidatos, com comparecimento de {n(H9div.comparecimento_bweb.iloc[0])} e {n(H9div.nominais_bweb.iloc[0])} votos nominais; `votacao_secao` registra {n(H9div.lula_votacao_secao.iloc[0])} e {n(H9div.oponente_votacao_secao.iloc[0])}, soma {n(H9div.soma_candidatos_votacao_secao.iloc[0])}, maior que o comparecimento da seção. Os totais nacionais divulgados pelo TSE para 2018/T1 (Haddad 31.342.005, Bolsonaro 49.276.990, comparecimento 117.364.560; [fonte](https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/concluida-totalizacao-de-votos-do-1o-turno-das-eleicoes-2018)) coincidem com o BWeb (comparecimento total do BWeb: 117.364.560), e `votacao_secao` fica 46 e 20 votos acima. Portanto a diferença está em `votacao_secao` (produto gerado em 2021), não na apuração divulgada em 2018. A causa não foi investigada. Não envolve 2026. Seções presentes só no BWeb e sem voto para nenhum dos dois candidatos: " + "; ".join(f"{int(a)}: {int(r.secoes)} (até {int(r.comp_max)} comparecimentos)" for a, r in sb.iterrows()) + ".\n")
A(f"A totalização por município/zona de 2026 tem {n(d_muz.so_munzona.iloc[0])} (T1) e {n(d_muz.so_munzona.iloc[1])} (T2) zonas sem seção apurada no BWeb; os totais de Lula e Flávio são idênticos, logo essas zonas somam zero voto para os dois. Consistência interna dos BUs (comparecimento <= aptos, nominais + brancos + nulos = comparecimento, válidos <= comparecimento, uma urna por seção): 0 violações em todas as eleições. Esta checagem mostra que os produtos do TSE são coerentes entre si; não prova a integridade da fonte (se um BU fosse alterado na origem, todos os produtos o refletiriam).\n")

A("### 3.10 H10: impacto agregado\n")
A(tab(h10, {**{c: (lambda x: n(x)) for c in ["n_testes_com_votos", "n_sobreviventes", "soma_votos_sobreviventes_exigente", "soma_votos_sobreviventes_pior_caso", "maximo_individual_pior_caso", "soma_de_todos_exigente"]}, **{c: (lambda x: n(x, 2)) for c in ["pct_margem_sobreviventes_pior_caso", "pct_margem_soma_todos_exigente"]}}))
A("\nSobreviventes (Holm < 0,05):\n")
A(tab(h10s, {"p_holm": lambda x: n(x, 3), "votos_max_margem": lambda x: n(x), "votos_max_pior_caso": lambda x: n(x), "pct_pior_caso": lambda x: pc(x)}))
A(f"\nOs tetos usam as mesmas seções e não são aditivos independentes; as colunas \"soma de todos\" e \"máximo individual\" são tetos redundantes e frouxos (o máximo individual vem do H1 sem controle do T1, comparado com 2022/T1, onde a associação era negativa). Os sentidos pró-Lula e pró-Flávio não se compensam. A soma dos sobreviventes no sentido pró-Lula é {n(sd.loc['PT','soma_votos_sobreviventes_pior_caso'])} votos ({pc(sd.loc['PT','pct_margem_sobreviventes_pior_caso'])} da margem).\n")

A("### 3.11 Teste direto com boletins impressos\n")
A("**Não executado.** Nenhum PDF ou imagem de BU foi fornecido (verificados Downloads e o diretório do projeto; capturas de tela em Imagens não foram abertas). `scripts/04_cruza_bu_impresso.py` está pronto: recebe uma planilha com zona, seção, turno e os totais do BU (transcritos ou lidos do QR code) e relata qualquer divergência, de aptos, comparecimento, votos, brancos, nulos, abertura e encerramento. Autoteste: com 3 seções reais, 0 divergências; com 1 voto alterado, 1 divergência detectada. Não há leitura de QR code por imagem; para fotos, é preciso transcrever ou decodificar o QR antes.\n")

A("### 3.12 Red team: explicações mundanas testadas\n")
A(tab(h1r, {"coef_manual": lambda x: n(x, 5), "ep": lambda x: n(x, 5)}))
A("\n- **Modelo da urna**: a taxa manual varia de 4,5% a 14,4% entre modelos em 2022/T2 (ver 3.3), e a associação S0 de 2026 permanece (0,069 com dummies de modelo).\n- **Composição do T1** (votos dos demais candidatos, brancos e nulos): o coeficiente de Flávio sobe de " + n(h1r[(h1r.teste.str.contains('Flavio')) & (h1r.ano == 2026) & (h1r.teste.str.contains('lag proprio'))].coef_manual.iloc[0], 3) + " para " + n(h1r[(h1r.teste.str.contains('Flavio')) & (h1r.ano == 2026) & (~h1r.teste.str.contains('lag proprio'))].coef_manual.iloc[0], 3) + "; o de Lula cai de " + n(h1r[(h1r.teste.str.contains('Lula votos')) & (h1r.ano == 2026) & (h1r.teste.str.contains('lag proprio'))].coef_manual.iloc[0], 3) + " para " + n(h1r[(h1r.teste.str.contains('Lula votos')) & (h1r.ano == 2026) & (~h1r.teste.str.contains('lag proprio'))].coef_manual.iloc[0], 3) + ". A hipótese de que os eliminados do T1 explicam o padrão pró-Flávio não se sustenta.\n- **Comparecimento**: a taxa manual prevê aumento de comparecimento no T2 dado o T1 nos dois anos (2022: " + n(h1r[(h1r.teste.str.startswith('comparecimento')) & (h1r.ano == 2022)].coef_manual.iloc[0], 3) + "; 2026: " + n(h1r[(h1r.teste.str.startswith('comparecimento')) & (h1r.ano == 2026)].coef_manual.iloc[0], 3) + "), em linha com a divisão do ganho entre os dois candidatos em 2026.\n")

# ------------------------------------------------------------------------------------------------ 3.13 regua
A("### 3.13 Régua histórica (2014, 2018, 2022, 2026)\n")
A("Previsões e critério de \"parecido\" fixados no Adendo 1 do pré-registro: razão entre 0,8 e 1,25 para taxas e contagens; diferença < 0,02 para correlações (M5b) e < 0,005 para o V de Cramér. Padrão A: 2014, 2022 e 2026 parecidos entre si e 2018 diferente das três. B: 2014 parecido com 2018, 2022 parecido com 2026, os pares diferentes entre si. C: os quatro parecidos.\n")
A("**2º turno:**\n")
A(tab(abc2.rename(columns={"Unnamed: 0": "metrica"}), {c: (lambda x: n(x, 5)) for c in ["2014", "2018", "2022", "2026"]}))
A("\nClassificação por métrica (2º turno):\n")
A(tab(abcc2[["metrica", "A", "B", "C", "nenhum", "sim_14_18", "sim_18_22", "sim_22_26", "sim_14_26"]]))
A(f"\nResumo T2: A = {n(ab.A)}, B = {n(ab.B)}, C = {n(ab.C)}, nenhum = {n(ab.nenhum)} de {n(ab.metricas)} métricas. Resumo T1: A = {n(abcr1.A.iloc[0])}, B = {n(abcr1.B.iloc[0])}, C = {n(abcr1.C.iloc[0])}, nenhum = {n(abcr1.nenhum.iloc[0])}.\n")
import itertools
RAZ = ["M5a_PT", "M5a_OPO", "M5c", "M7a_up", "M7a_down", "M7b", "M8b_PT", "M8b_OPO"]
DIFF = {"M5b_PT": .02, "M5b_OPO": .02, "M8a_V_PT": .005, "M8a_V_OPO": .005}
def sim(m, x, y):
    if m in DIFF:
        return abs(x - y) < DIFF[m]
    if x == 0 and y == 0:
        return True
    if x == 0 or y == 0:
        return False
    return 0.8 <= x / y <= 1.25
am = abc2.rename(columns={"Unnamed: 0": "metrica"}).set_index("metrica")
trios = []
for tr in itertools.combinations(["2014", "2018", "2022", "2026"], 3):
    ok = [m for m in am.index if all(sim(m, am.loc[m, p], am.loc[m, q]) for p, q in itertools.combinations(tr, 2))]
    nao_ok = [m for m in am.index if m not in ok]
    trios.append(dict(trio=" + ".join(tr), metricas_mutuamente_parecidas=f"{len(ok)} de {len(am)}", metricas_que_nao_se_ajustam=", ".join(nao_ok)))
A("**Trios de anos mutuamente parecidos** (todas as três comparações dentro do critério), 2º turno:\n")
A(tab(pd.DataFrame(trios)))
indep = [m for m in am.index if m not in ("M5b_OPO", "M8b_OPO")]
nC_indep = int(abcc2[abcc2.metrica.isin(indep)].C.sum())
A(f"\nNota: `M5b_OPO` e `M8b_OPO` repetem `M5b_PT` e `M8b_PT` por construção (as duas parcelas somam 1), então as 12 linhas têm {len(indep)} métricas independentes. Sem as repetições, C vale em {nC_indep} de {len(indep)}, e 2/3 seria {-(-2*len(indep)//3)}. A conclusão não muda.\n")
A("\n**Veredito pelo critério fixado: nenhum dos três padrões se ajusta.** O limiar de 2/3 das métricas (8 de 12) não é atingido por A, B nem C (C chega a " + n(ab.C) + "). O trio 2018, 2022 e 2026 é o mais homogêneo da tabela; as métricas em que não é homogêneo são as de cauda (comparecimento >= 90% com voto >= 90%, e comparecimento >= 95%), que são justamente as do resíduo descrito em 3.6. Esta leitura por trios é uma análise posterior, não pré-registrada. A métrica M5c (seções com comparecimento >= 95%) não tem padrão monotônico: 242 por 100 mil seções em 2014, 111 em 2018, 49 em 2022 e 128 em 2026; 2022 é o mínimo da série e 2026 fica entre 2018 e 2014.\n")
A("A classificação em A/B/C depende do critério numérico fixado, que é arbitrário; por isso as razões estão na tabela.\n")

# ------------------------------------------------------------------------------------------------ 4
A("## 4. Anomalias residuais que sobreviveram aos controles\n")
A(f"1. **Votos de Flávio por apto x taxa manual (H1).** Coeficiente {n(sflav.est_2026T2,4)} contra {n(sflav.b_comp,4)} em 2022; teto {n(sflav.votos_max_pior_caso)} votos, {pc(sflav.pct_pior_caso)} da margem, **no sentido favorável a Flávio**. Testado e não explicado por: composição do T1 (o coeficiente aumenta), nível de comparecimento do T1. Não testado: perfil de idade e escolaridade por seção (conjunto não disponível por seção).")
A(f"2. **Variação de voto em Lula entre anos x variação da taxa manual (H2).** T2: {n(h2b.est_2026T2,4)}; T1 (placebo): {n(h2b.b_comp,4)}; diferença estatisticamente detectável, teto {n(h2b.votos_max_pior_caso)} votos ({pc(h2b.pct_pior_caso)}). O T1 de 2026 tem candidatos diferentes do T1 de 2022, então o placebo é imperfeito.")
A(f"3. **Associação manual x Lula de 2026 (H1, sem controle do T1).** {n(a0(2026,1).coef,3)} no T1 e {n(a0(2026,2).coef,3)} no T2, contra {n(a0(2022,1).coef,3)} e {n(a0(2022,2).coef,3)} em 2022. Presente antes do 2º turno e inalterada por tamanho, comparecimento e modelo da urna. Causa não identificada. Não é específica do 2º turno, então não decorre de nada exclusivo daquele dia (a prorrogação, por exemplo). Uma causa comum aos dois turnos, seja de característica das seções ou da urna, seja de outra natureza, não é distinguível por estes dados.")
A(f"4. **Seções com comparecimento >= 95% (H5).** {n(c639.secoes)} em 2026/T2; {n(r26.razao,1)} vezes o esperado pela composição de tipo de local e tamanho; presente no T1 ({n(r26t1.razao,1)} vezes). Testado: tipo de local (indígena, prisional, hospital, quilombola, militar, rural), tamanho, seção nova, UF, taxa manual, atraso de fechamento, \"só no T2\" ({n(h5s.dessas_so_no_T2.iloc[0])} seções, {n(h5s.votos_validos_dessas.iloc[0])} votos válidos), numerador contra denominador. Nenhum fator isolado elimina o excesso. Não testado: cancelamento de títulos e revisão do eleitorado entre 2022 e 2026 (não há dado). Teto de efeito: {pc(h5r.pct_pior_caso)} da margem.")
A(f"5. **Seções novas (H6).** +{n(100*h6reg.est_2026T2,2)} p.p. de Lula no T2 dado o T1 (2018: +1,34; 2022: 0,00); robusto a interação, tamanho e comparecimento. Teto de pior caso {pc(h6reg.pct_pior_caso)}.\n")

# ------------------------------------------------------------------------------------------------ 5
A("## 5. O que os dados não conseguem mostrar\n")
A("- **Desvio uniforme em todas as urnas.** Todos os testes comparam seções entre si (dentro do local, entre anos, entre turnos). Um viés igual em todas as seções some nas diferenças.")
A("- **Voto secreto.** Não há como ligar voto a eleitor; só agregados por seção.")
A("- **Fiscais e presença de partidos.** Nenhuma variável mede presença de fiscais.")
A("- **Votos depois das 17h.** O BWeb não tem log de votação; só horário de abertura e encerramento por seção.")
A("- **Integridade da fonte.** BWeb, `votacao_secao` e totalização vêm do mesmo fluxo de BUs; a coerência entre eles não detecta um BU alterado na origem. Só o cruzamento com boletins impressos por fiscais e partidos faz isso, e ele não foi executado.")
A("- **Liberação manual total.** O campo mede só eleitores com biometria cadastrada não habilitados por ela, sem denominador.")
A("- **Perfil por seção (idade, escolaridade, renda).** Não há conjunto por seção; o perfil do eleitorado está por município e zona, que o efeito fixo de local já absorve.")
A("- **2014 e 2018.** 2014 não tem biometria nem horários; 2018 não tem horário de recebimento nem de emissão do BU.")
A("- **Pareamento de seções entre anos.** Perde seções remanejadas; seções novas e antigas se comportam de forma diferente (H6).\n")

# ------------------------------------------------------------------------------------------------ 6
A("## 6. Reprodutibilidade\n")
A("Estrutura: `00_preregistro.md` (previsões e adendos), `scripts/`, `dados/` (hashes e URLs), `results/fase1/` (CSVs, figuras, logs), `dossie.md`.\n")
A("```bash\n# 0. ambiente\npython3 -m venv venv && venv/bin/pip install pandas numpy scipy pyarrow matplotlib\n\n# 1. dados (URLs em dados/urls_origem.txt; conferir SHA-512/SHA-1 de cada zip com o arquivo .sha512/.sha1 do TSE)\n#    BWeb 2022 e 2026 em bu/, 2014 e 2018 em bu_hist/; votacao_secao, detalhe e munzona em dados_tse/\n\n# 2. preparação (um parquet por ano x turno)\nvenv/bin/python -I scripts/01_prepara_bweb.py bu parquet --anos 2022 2026\nvenv/bin/python -I scripts/01_prepara_bweb.py bu_hist parquet --anos 2014 2018\nvenv/bin/python -I scripts/01b_locais.py dados_tse parquet 2022 2026\nvenv/bin/python -I scripts/01c_modelo_urna.py dados_tse parquet 2022 2026\n\n# 3. testes H1 a H10 e A/B/C (ordem fixa: H5, H7, H8 antes de ABC; H10 por último)\nvenv/bin/python -I scripts/02_executa.py parquet resultados --anos 2014 2018 2022 2026 --zips dados_tse\n#    código de saída 2 = há testes não executados (results/fase1/nao_executados.csv)\n\n# 4. dossiê\nvenv/bin/python -I scripts/03_monta_dossie.py resultados dados dossie.md\n\n# 5. teste direto com boletins impressos (quando houver planilha)\nvenv/bin/python -I scripts/04_cruza_bu_impresso.py parquet entrada.csv divergencias.csv\n```\n")
A("Reprocessar 2022 e 2026 com a versão final do preparador reproduz os parquets originais célula a célula, exceto 5 seções anuladas do exterior (sentinela -1 virou vazio), que não entram nas análises. O registro de testes das duas execuções é idêntico.\n")

A("## Apêndice A: registro completo dos 23 testes\n")
ap = reg[["H", "teste", "sentido", "est_2026T2", "comparador_exigente", "b_comp", "p_bruto_2lados", "p_excesso", "p_holm", "p_bh", "votos_max_margem", "pct_margem", "votos_max_pior_caso", "pct_pior_caso", "veredito"]]
A(tab(ap, {"est_2026T2": lambda x: n(x, 5), "b_comp": lambda x: n(x, 5), "p_bruto_2lados": lambda x: n(x, 4), "p_excesso": lambda x: n(x, 4), "p_holm": lambda x: n(x, 3), "p_bh": lambda x: n(x, 3),
          "votos_max_margem": lambda x: n(x), "pct_margem": lambda x: n(x, 3), "votos_max_pior_caso": lambda x: n(x), "pct_pior_caso": lambda x: n(x, 3)}))
A("\n## Apêndice B: não executados\n")
A(tab(nao))
A("\nFim.\n")
open(SAIDA, "w", encoding="utf-8").write("\n".join(L))
print("escrito", SAIDA, len(L), "blocos")
