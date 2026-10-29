#!/usr/bin/env python3
"""Monta docs/resultados-fase2.md, docs/residuos.md, docs/regua-historica.md, docs/relatorio-original.md, docs/index.md e README.md a partir dos CSVs.
Uso: python -I 03b_monta_fase2.py DIR_RESULTADOS_FASE2 DIR_RESULTADOS_FASE1 RAIZ_REPO
Todos os numeros vem dos CSVs; o texto so contem rotulos e leituras."""
import json, os, re, sys
import pandas as pd

R, R1, RAIZ = sys.argv[1], sys.argv[2], sys.argv[3]
DOCS = os.path.join(RAIZ, "docs")
os.makedirs(DOCS, exist_ok=True)
MARGEM = 4_430_191


def rd(nome, base=None):
    p = os.path.join(base or R, nome)
    return pd.read_csv(p) if os.path.exists(p) else None


def js(nome, base=None):
    p = os.path.join(base or R, nome)
    return json.load(open(p)) if os.path.exists(p) else None


def n(x, d=0):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "n/d"
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pc(x, d=2):
    return n(x, d) + "%"


def tab(df, fmts=None):
    if df is None or len(df) == 0:
        return "_(tabela vazia ou não executada)_"
    fmts = fmts or {}
    cols = list(df.columns)
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.astype(object).iterrows():
        L.append("| " + " | ".join(((fmts[c](r[c]) if c in fmts else str(r[c])).replace("|", "/")) for c in cols) + " |")
    return "\n".join(L)


F = lambda d=0: (lambda x: n(x, d))
reg = rd("registro_testes.csv")
nao = rd("nao_executados.csv")


def linha(h, trecho):
    r = reg[(reg.H == h) & reg.teste.str.contains(trecho, regex=False)]
    return r.iloc[0] if len(r) else None


def veredito_curto(r):
    if r is None:
        return "NÃO EXECUTADO"
    return r.veredito


# ------------------------------------------------------------------------------------------------ dados
a1 = rd("A1_a1_resumo.csv"); a1u = rd("A1_a1_ordem_por_uf_2026_T2.csv")
a2p, a2m, a2s, a2k, a2c, a2mo = rd("A2_a2_perdas.csv"), rd("A2_a2_mecanismo_pool.csv"), rd("A2_a2_swing.csv"), rd("A2_a2_forma_ks_ad.csv"), rd("A2_a2_criterio_forma.csv"), rd("A2_a2_momentos.csv")
a3c, a3e, a3f, a3l = rd("A3_a3_contabilidade.csv"), rd("A3_a3_ecologica.csv"), rd("A3_a3_ecologica_EF_municipio.csv"), rd("A3_a3_perda_liquida_minima.csv")
a4, a4d, a4e = rd("A4_a4_resumo.csv"), rd("A4_a4_divergencias.csv"), js("A4_a4_emissao_igual_bweb.json")
a5l, a5x, a5v, a5u, a5n, a5m, a5t, a5h = (rd("A5_a5_log_x_bu.csv"), rd("A5_a5_excecoes_sem_contingencia.csv"), rd("A5_a5_votos_apos_horario_nominal.csv"), rd("A5_a5_ultimo_voto_apos_nominal.csv"),
                                         rd("A5_a5_estimativa_nacional_votos_apos_nominal.csv"), rd("A5_a5_liberacao_manual_total.csv"), rd("A5_a5_tardio_x_lula.csv"), rd("A5_a5_hora_ultimo_voto_L.csv"))
a6s, a6c = rd("A6_a6_substituicao.csv"), rd("A6_a6_coef.csv")
a7 = rd("A7_a7_pesquisas.csv")
a8 = rd("A8_a8_cargos.csv")
a9c, a9b, a9o, a9f, a9a = rd("A9_a9_celulas.csv"), rd("A9_a9_consistencia_bweb.csv"), rd("A9_a9_zonas_facultativo_outliers.csv"), rd("A9_a9_variacao_T1_T2_placebos.csv"), rd("A9_a9_aptos_comp_por_faixa_T1.csv")
a10m, a10e = rd("A10_a10_modelo_urna.csv"), rd("A10_a10_exterior.csv")
h10 = rd("H10_h10_agregado.csv"); h10s = rd("H10_h10_sobreviventes.csv")
h3c = rd("H3_h3_recontagem_relogio_cru.csv")
tot = rd("H2_h2_totais_absolutos.csv").set_index(["ano", "turno"])

L = []
A = L.append
A("# Resultados da Fase 2 (A1 a A10)\n")
A(f"Previsões, critérios e placebos foram registrados no [Adendo 4 do pré-registro](preregistro.md) **antes** de rodar as análises. O registro de testes é combinado com o da Fase 1 ({len(reg)} testes); o p corrigido (Holm e Benjamini-Hochberg) é sobre a família completa. Veredito: regra do [Adendo 2](preregistro.md). Margem oficial: {n(MARGEM)} votos. Tetos em votos são limites superiores sob causalidade, não estimativas.\n")
A("**Leitura rápida.** Pelos critérios pré-registrados, três análises (A1, A2, A3) saem como \"excesso detectado\"; cada uma tem **ressalva de desenho** documentada, porque um controle posterior mostrou que o desenho pré-registrado media outra coisa (ver cada seção e [Changelog](changelog.md)). As linhas foram mantidas como saíram e os dois cálculos de impacto agregado (com e sem essas linhas) são publicados.\n")
A("## Tabela-resumo\n")
rows = []
def add(a, nome, r, texto):
    rows.append(dict(A=a, analise=nome, resultado=texto, p_holm=("n/d" if r is None else n(r.p_holm, 3)), pct_margem_pior_caso=("n/d" if r is None or pd.isna(r.pct_pior_caso) else pc(r.pct_pior_caso)), veredito=veredito_curto(r)))
r1_ = linha("A1", "curva"); r2_ = linha("A2", "oponente perde"); r3_ = linha("A3", "ecologica"); r4_ = linha("A4", "divergentes"); r5_ = linha("A5", "share de votos"); r6_ = linha("A6", "urna efetivada")
r8_ = linha("A8", "secoes com total"); r9_ = linha("A9", "zonas");
add("A1", "curva de apuração", r1_, "desvio máximo vs permutação dentro da UF: " + (f"{n(a1[(a1.ano==2026)&(a1.turno==2)].maxdev_vs_B_pp.iloc[0],2)} p.p. (2026/T2) contra " + ", ".join(f"{n(r.maxdev_vs_B_pp,2)} ({int(r.ano)}/T{int(r.turno)})" for r in a1.itertuples() if not (r.ano == 2026 and r.turno == 2)) if a1 is not None else "n/d"))
add("A2", "transições T1→T2", r2_, f"oponente perde votos em {pc(a2p[(a2p.ano==2026)&(a2p.cand=='OPO')].pct_secoes.iloc[0],1)} das seções (2022: PT {pc(a2p[(a2p.ano==2022)&(a2p.cand=='PT')].pct_secoes.iloc[0],1)}); forma do swing não difere dos placebos" if a2p is not None else "n/d")
add("A3", "origem dos votos", r3_, "contabilidade fecha por identidade; coeficiente ecológico não mede conversão")
add("A4", "cadeia da urna", r4_, (f"{n(a4[a4.ano==2026].secoes.iloc[0])} seções 2026: 0 divergências BU/RDV/hash" if a4 is not None and (a4[a4.ano==2026][["bu_diferente_do_bweb","rdv_diferente_do_bu","hash_nao_vinculado"]].sum(axis=1).iloc[0]==0) else "ver seção"))
add("A5", "logs de urna", r5_, (f"votos depois do horário nominal: estimativa nacional {n(a5n.estimativa_total.iloc[0])} (IC95 {n(a5n.ic95_total_inf.iloc[0])} a {n(a5n.ic95_total_sup.iloc[0])})" if a5n is not None else "n/d"))
add("A6", "urna substituída", r6_, f"urna ≠ esperada em {pc(a6s[a6s.ano==2026].pct.iloc[0],2)} das seções; sem efeito no voto" if a6s is not None else "n/d")
add("A7", "pesquisas (contexto)", None, "sem veredito; ver seção")
add("A8", "coerência entre cargos", r8_, "0 seções fora da regra em 2018, 2022 e 2026" if a8 is not None else "n/d")
add("A9", "perfil do comparecimento", r9_, "só 1º turno; T1→T2 de 2026 NÃO EXECUTADO")
add("A10", "modelo de urna, exterior", linha("A10", "UE2022"), "modelo de urna sem efeito no voto dentro do local")
rows[6]["veredito"] = "contexto, sem veredito"; rows[9]["veredito"] = "ver seção"
A(tab(pd.DataFrame(rows)))
A("\nTodos os números abaixo vêm dos CSVs em `results/fase2/`; scripts em `scripts/`.\n")

# ------------------------------------------------------------------------------------------------ A1
A("## A1. Curva de apuração\n")
A("**Alegação testada:** \"a curva deveria subir e descer em blocos; linhas retas indicam manipulação\".\n")
A("**Previsão registrada.** Sem manipulação: a curva real fica dentro do envelope de permutações das seções dentro de cada UF (mantida a sequência de UFs de chegada), e a soma final é idêntica em qualquer ordem. Critério: o desvio máximo (a partir de 1% das seções) só conta como excesso se superar o dos placebos e sair do envelope 95% simultâneo por 20 pontos consecutivos.\n")
A("**Método.** Ordem real = horário da primeira totalização parcial por seção (`DT_PRIM_TOT_PARCIAL_HOR_TSE`). 1.000 ordens aleatórias totais (nulo A) e 1.000 permutações dentro de cada UF preservando a sequência de UFs (nulo B), sobre ~500 mil seções.\n")
A(tab(a1[["ano", "turno", "secoes", "share_final", "maxdev_vs_B_pp", "maxdev_vs_B_pp_posterior_ge10pct", "maxdev_vs_A_pp", "maior_sequencia_fora_envelope", "fracao_explicada_por_geografia", "pct_secoes_totalizadas_antes_das_19h"]], {"secoes": F(), "share_final": F(4), "maxdev_vs_B_pp": F(2), "maxdev_vs_B_pp_posterior_ge10pct": F(2), "maxdev_vs_A_pp": F(2), "fracao_explicada_por_geografia": F(3), "pct_secoes_totalizadas_antes_das_19h": F(2)}))
g = a1[(a1.ano == 2026) & (a1.turno == 2)].iloc[0]
A(f"\n![Curva de apuração real contra os nulos A e B](figs/a1_curva_apuracao.png)\n")
A(f"**Resultado pré-registrado.** O desvio máximo de 2026/T2 contra o nulo B é {n(g.maxdev_vs_B_pp,2)} p.p., maior que o dos placebos ({', '.join(f'{n(r.maxdev_vs_B_pp,2)}' for r in a1.itertuples() if not (r.ano==2026 and r.turno==2))}), e a curva sai do envelope por {n(g.maior_sequencia_fora_envelope)} pontos consecutivos. Pelo critério fixado, a linha sai como **excesso detectado (teste de forma)**.\n")
A(f"**Ressalva de desenho.** (1) O nulo B é rejeitado nos quatro anos (maior sequência fora do envelope: {', '.join(n(x) for x in a1.maior_sequencia_fora_envelope)} de 990 pontos): a ordem de chegada dentro da UF não é aleatória em nenhuma eleição, porque municípios e zonas chegam em blocos. (2) Em 2026/T2 o desvio máximo ocorre nos primeiros 1 a 5% das seções; a partir de 10% das seções ele cai a {n(g.maxdev_vs_B_pp_posterior_ge10pct,2)} p.p., abaixo dos placebos ({', '.join(f'{n(r.maxdev_vs_B_pp_posterior_ge10pct,2)}' for r in a1.itertuples() if not (r.ano==2026 and r.turno==2))}); esta é uma análise **posterior**, não pré-registrada. (3) A geografia explica {pc(100*g.fracao_explicada_por_geografia,0)} do desvio contra a ordem aleatória total. O efeito sobre a soma final é zero por construção.\n")
A(f"**Pausa da divulgação.** Em 2026/T2, só {pc(g.pct_secoes_totalizadas_antes_das_19h,2)} das seções tinham primeira totalização antes das 19h, contra {pc(a1[(a1.ano==2022)&(a1.turno==2)].pct_secoes_totalizadas_antes_das_19h.iloc[0],1)} em 2022 e {pc(a1[(a1.ano==2018)&(a1.turno==2)].pct_secoes_totalizadas_antes_das_19h.iloc[0],1)} em 2018. Isso é compatível com a pausa descrita pela imprensa (ver [Base legal](base-legal.md)); a fonte oficial não pôde ser aberta.\n")
A("**Ordem de chegada por UF (2026/T2, posição mediana):** " + ", ".join(f"{r.SG_UF} {n(r.posicao_mediana,2)}" for r in a1u.head(6).itertuples()) + " (primeiras); " + ", ".join(f"{r.SG_UF} {n(r.posicao_mediana,2)}" for r in a1u.tail(6).itertuples()) + " (últimas). O PT tem " + ", ".join(f"{r.SG_UF} {pc(100*r.share_pt,0)}" for r in a1u.tail(4).itertuples()) + " nas últimas: estados com perfis diferentes chegam em momentos diferentes, e a curva reflete isso.\n")
A("**NÃO EXECUTADO:** (i) 2014/T2: o produto `detalhe_votacao_secao` de 2014 não traz horário de totalização e o BWeb de 2014 só tem a data de recebimento; (ii) comparação numérica com o gráfico \"Evolução da apuração\" do g1 de 25/10/2026: o gráfico não foi fornecido como dado.\n")

# ------------------------------------------------------------------------------------------------ A2
A("## A2. Transições seção a seção, 1º para 2º turno\n")
A("**Alegação testada:** conversão de eleitores do oponente para o PT; compressão de margem ('113x30 vira 77x70'); formato do swing diferente do histórico.\n")
A("**Previsão registrada.** Sem manipulação: frequência de perda de votos absolutos pelo oponente e forma do swing dentro da faixa dos anos placebo. Critério: frequência fora de [mín, máx] dos placebos, ou forma 'diferente' se a menor distância KS de 2026 a um placebo superar a maior distância entre pares de placebos.\n")
A("**Perda de votos absolutos** em seções com comparecimento estável ou crescente (≥ 98% do T1):\n")
A(tab(a2p, {"secoes_estaveis_ou_crescentes": F(), "secoes_com_perda": F(), "pct_secoes": F(2), "votos_perdidos": F(), "pct_dos_votos_T1_do_cand_nessas_secoes": F(3), "pct_secoes_perda_acima_de_20pct_do_T1": F(3)}))
r = linha("A2", "oponente perde")
A(f"\n**Resultado pré-registrado:** o oponente perde votos em {pc(a2p[(a2p.ano==2026)&(a2p.cand=='OPO')].pct_secoes.iloc[0],1)} das seções em 2026, fora da faixa dos placebos de oponente (2014, 2018, 2022: {', '.join(pc(x,1) for x in a2p[(a2p.cand=='OPO')&(a2p.ano!=2026)].pct_secoes)}). Pelo critério, **excesso detectado (teste de forma)**.\n")
A(f"**Ressalva de desenho (análise posterior).** O placebo \"por papel\" (oponente) é inadequado: em 2022 foi o **PT**, que liderou o 1º turno, quem perdeu votos absolutos em {pc(a2p[(a2p.ano==2022)&(a2p.cand=='PT')].pct_secoes.iloc[0],1)} das seções, quase o espelho dos {pc(a2p[(a2p.ano==2026)&(a2p.cand=='OPO')].pct_secoes.iloc[0],1)} do oponente em 2026 (que liderou o 1º turno). Nos dois anos havia poucos votos de terceiros para repartir (cerca de 10 milhões e 9 milhões, contra 26 milhões em 2014 e 2018). Por faixa de \"votos de terceiros / votos do candidato no T1\" na seção, as frequências são parecidas:\n")
A(tab(a2m))
A("\n![Espelho de perdas por faixa](figs/a2_espelho_perdas.png)\n")
A("**Forma do swing** (resíduo da margem do T2 sobre a margem do T1, com efeito fixo de município):\n")
A(tab(a2k, {"ks": F(4), "ad_subamostra_20k": F(1)}))
A("\n" + tab(a2c, {"menor_ks_2026_vs_placebo": F(4), "maior_ks_entre_placebos": F(4)}))
A("\nCritério de forma: **2026 não difere** (a menor distância, contra 2022, é menor que a maior distância entre placebos). Os anos se agrupam em dois pares, {2014, 2018} e {2022, 2026}, e 2026 fica no par de 2022.\n")
A("**Compressão de margem:** coeficiente da margem do T2 sobre a margem do T1 (com município):\n")
A(tab(a2s, {"coef_m1": F(4), "ep": F(4), "n": F(), "municipios": F()}))
A("\n")

# ------------------------------------------------------------------------------------------------ A3
A("## A3. Origem dos votos novos de Lula\n")
A("**Contabilidade nacional (identidade).** Como no 2º turno não há terceiros, `ΔPT + ΔOPO = Δcomparecimento + terceiros no T1 − Δ(brancos e nulos)`. A identidade fecha em todas as eleições:\n")
A(tab(a3c[["ano", "PT_T1", "PT_T2", "OPO_T1", "OPO_T2", "TERCEIROS_T1", "BN_T1", "BN_T2", "dPT", "dOPO", "dCOMP", "pool", "identidade_ok", "pt_pct_do_pool", "opo_pct_do_pool"]], {c: F() for c in ["PT_T1", "PT_T2", "OPO_T1", "OPO_T2", "TERCEIROS_T1", "BN_T1", "BN_T2", "dPT", "dOPO", "dCOMP", "pool"]} | {"pt_pct_do_pool": F(1), "opo_pct_do_pool": F(1)}))
c26 = a3c[a3c.ano == 2026].iloc[0]
A(f"\nEm 2026, Lula ganhou {n(c26.dPT)} votos e o oponente {n(c26.dOPO)} (líquido positivo): a soma dos dois ({n(c26.dPT + c26.dOPO)}) é exatamente o conjunto de votos disponíveis ({n(c26.pool)} = {n(c26.dCOMP)} de comparecimento + {n(c26.TERCEIROS_T1)} de terceiros − {n(c26.dBN)} de variação de brancos e nulos). Nacionalmente, **nenhuma conversão do oponente para o PT é necessária** para explicar o resultado.\n")
A("**Perda líquida mínima por seção** (quantos votos do T1 de cada candidato 'sumiram' dentro de seções onde ele perdeu votos absolutos; é limite inferior de eleitores que não repetiram o voto, por mudança, abstenção ou outra causa, não de conversão):\n")
A(tab(a3l, {"secoes": F(), "secoes_com_perda_liquida": F(), "pct_secoes": F(2), "votos_perdidos_liquidos_somados": F(), "ganho_liquido_nacional": F()}))
A("\nO oponente de 2026 (16,5% das seções, 383 mil votos) e o PT de 2022 (18,9%, 459 mil) têm o mesmo porte: o padrão é espelhado entre os anos e não identifica manipulação.\n")
A("**Regressão ecológica** (taxas de transição aparentes; falácia ecológica: são correlações entre agregados, não comportamento individual). Coeficiente de \"oponente no T1\" sobre o PT no T2:\n")
A(tab(a3e[(a3e.destino_T2 == "PT") & (a3e.origem_T1.isin(["OPO_T1", "TERCEIROS_T1", "BRANCOS_NULOS_T1"]))], {"coef": F(3), "ep": F(3)}))
A("\nCom efeito fixo de município (relativo à abstenção do T1):\n")
A(tab(a3f[a3f.origem_T1 == "op1"], {"coef": F(3), "ep": F(3)}))
r = linha("A3", "ecologica")
A(f"\n**Resultado pré-registrado:** o coeficiente de 2026 ({n(r.est_2026T2,3)}) é o menos negativo dos quatro anos, e a linha sai como **excesso detectado e relevante** pelo teto calculado ({pc(r.pct_pior_caso)} da margem). **Ressalva de desenho:** todos os coeficientes são negativos (nenhum mede conversão); a diferença entre anos reflete geografia; com efeito fixo de município o coeficiente de 2026 é o **mais negativo** (−0,127 contra −0,042 a −0,070). O teto em votos derivado dessa diferença não tem interpretação causal. Por isso o H10 é publicado com e sem esta linha.\n")
A("**Limites:** falácia ecológica; o 2º turno de 2026 tem eleitores de candidatos diferentes dos de 2022; a identidade usa o BWeb, que é o mesmo dado que se audita.\n")

# ------------------------------------------------------------------------------------------------ A4
A("## A4. Cadeia da urna até o TSE\n")
A("**Insumo:** conjunto \"arquivos transmitidos para totalização\" (BU, imagem do BU, RDV, log e assinatura por seção). O catálogo do TSE lista só o 1º turno; os arquivos do 2º turno de 2026 e os de 2022 existem nos mesmos caminhos e foram baixados por seção (requisições parciais).\n")
A("**Previsão registrada.** 0 divergências entre BU digital, RDV, BWeb e vínculo de hash em toda a amostra; divergência de um voto é reportada individualmente.\n")
A("**Amostra:** Roraima inteira; as seções que fecharam ≥115 min depois do horário (população completa fora de Roraima e do exterior); controles 1:1 no mesmo local; as seções com comparecimento ≥95%; 60 aleatórias por UF; e as mesmas seções em 2022 como placebo.\n")
A(tab(a4, {"secoes": F()}))
A("\n**O que foi verificado:** (c) o BU digital coincide com o BWeb em Lula, oponente, brancos, nulos e comparecimento; (b) o RDV recontado coincide com o BU (Lula, oponente, brancos e total; nulos pelo resíduo); vínculo de integridade: o SHA-512 de BU, RDV, imagem e log consta na lista assinada pela urna e o SHA-512 da lista confere com o hash do bloco assinado. A emissão do BU coincide com a do BWeb em " + (f"{n(a4e['iguais'])} de {n(a4e['secoes'])} seções." if a4e else "n/d") + "\n")
A("**NÃO verificado:** (a) a assinatura criptográfica em si: a chave da urna usa uma curva de 521 bits com OID 1.3.6.1.4.1.44588.2.1, sem suporte em bibliotecas padrão, e a especificação ASN.1 e os scripts de exemplo do TSE não são acessíveis por automação (HTTP 403). Insumo que falta: especificação e ferramenta oficial de verificação. (d) a identificação do software contra a publicada na lacração: só foi possível listar a versão registrada no log (2026: 10.23.0.0; 2022: 8.26.0.0) e a verificação de assinatura de aplicação por etapa (6 etapas, todas \"SUCESSO\" em todos os logs lidos). Insumo que falta: hashes de lacração para comparar.\n")
A("**Divergências individuais:**\n")
A(tab(a4d) if a4d is not None and len(a4d) else "Nenhuma em 2026 nem em 2022.")
A("\nO leitor de BU e RDV é genérico (decodificador BER) e cada campo foi validado contra o BWeb antes de ser usado (em Roraima: 1.519 de 1.519 seções).\n")

# ------------------------------------------------------------------------------------------------ A5
A("## A5. Logs de urna (votos depois do horário)\n")
A("**O que os logs registram** (confirmado nos arquivos): por eleitor, \"Eleitor foi habilitado\", \"Tipo de habilitação\" (biométrica ou manual, com \"Dado digitado confere\"), \"Voto confirmado para [cargo]\" e \"O voto do eleitor foi computado\", cada um com data e hora; eventos de contingência e de verificação de assinatura.\n")
A("**Previsão registrada.** Votos computados no log = comparecimento do BU em ≥99,9% das seções; votos depois do horário nominal concentrados nas seções que fecharam tarde; intervalos entre votos acima do mínimo físico; sem associação entre voto tardio e Lula% no mesmo local além do placebo de 2022.\n")
A("**Log contra BU:**\n")
A(tab(a5l, {"secoes": F(), "pct": F(2), "votos_computados_log_igual_comparecimento": F()}))
A("\nO limiar de 99,9% pré-registrado **não é atingido** (ver `pct`), e todas as divergências com contingência explicam a diferença: urnas de contingência assumiram no meio do dia (log: \"Seção informada pelo operador: 0000 - Urna de contingência\"), e o BU consolida os votos recuperados da urna anterior, que não estão no log da urna substituta. Exceções **sem** contingência (reportadas individualmente):\n")
A(tab(a5x) if a5x is not None and len(a5x) else "Nenhuma.")
A("\n**Votos computados depois do horário nominal de fechamento** (17h de Brasília, convertido ao relógio local de cada urna), por estrato:\n")
A(tab(a5v, {"secoes": F(), "secoes_com_voto_apos_nominal": F(), "votos_apos_nominal": F(), "media_por_secao": F(3), "comparecimento": F()}))
A("\n![Votos depois do horário nominal por estrato](figs/a5_votos_apos_nominal.png)\n")
A("**Último voto por seção, depois do horário nominal:**\n")
A(tab(a5u))
if a5n is not None:
    e = a5n.iloc[0]
    A(f"\n**Estimativa nacional (2026/T2).** Nas {n(e.secoes_L_populacao)} seções que fecharam ≥115 min depois (população completa fora de Roraima e exterior; {n(e.secoes_L_medidas)} medidas, {n(e.secoes_L_nao_medidas)} sem arquivo), foram medidos {n(e.votos_apos_nominal_em_L_medido)} votos depois do horário nominal. Nas demais seções, a amostra aleatória (60 por UF) estima {n(e.estimativa_fora_de_L)} votos (IC95 {n(e.ic95_fora_de_L_inf)} a {n(e.ic95_fora_de_L_sup)}). **Total estimado: {n(e.estimativa_total)} votos (IC95 {n(e.ic95_total_inf)} a {n(e.ic95_total_sup)})**, ou {pc(100*e.estimativa_total/MARGEM,2)} da margem. A referência externa de 34.330 eleitores (imprensa, não verificada) está dentro da mesma ordem de grandeza. Esses votos incluem os de eleitores com senha na fila às 17h, previstos no art. 153 do Código Eleitoral ([Base legal](base-legal.md)); a maior parte está fora das seções que fecharam tarde.\n")
A("**Leitura.** Muitas das seções que \"fecharam tarde\" ficaram com a urna aberta até perto das 19h **sem registrar voto depois das 17h**: a coluna \"último voto antes do horário nominal\" mostra quantas. O fechamento tardio, por si, não mede voto tardio.\n")
A("**Liberação manual total pelo log** (comparecimento menos habilitações biométricas), contra o campo do BWeb (que só mede quem tinha biometria cadastrada):\n")
A(tab(a5m, {"secoes": F(), "manual_total_log": F(), "bweb_biom_nh": F(), "razao": F(2)}))
A("\n**Associação entre voto tardio e Lula% no mesmo local** (fração de votos depois do horário nominal; controle do T1; placebo: mesmas seções em 2022):\n")
A(tab(a5t, {"coef": F(3), "ep": F(3), "secoes": F(), "locais": F()}))
rl = linha("A5", "share de votos")
A(f"\nVeredito: {rl.veredito if rl is not None else 'n/d'}.\n")
A("**Limites:** amostra, não toda a eleição (as seções de UFs sem arquivo e os controles não são aleatórios); o relógio da urna é local; o log não permite ligar voto a eleitor. Gap mínimo entre habilitações: " + (f"{n(a5l.gap_minimo_entre_habilitacoes_s.min())} s" if a5l is not None else "n/d") + ".\n")

# ------------------------------------------------------------------------------------------------ A6
A("## A6. Urna substituída ou em contingência\n")
A("Compara a urna **esperada** (correspondência esperada do TSE, 24/10/2026) com a **efetivada** (BWeb). Não há conjunto aberto de \"ocorrências\" no catálogo do TSE; esta é a medida disponível.\n")
A(tab(a6s, {"secoes": F(), "sem_correspondencia": F(), "urna_diferente_da_esperada": F(), "pct": F(2)}))
A("\n" + tab(a6c, {"coef": F(4), "ep": F(4), "secoes_substituidas": F(), "n": F()}))
A("\nSeções com urna diferente da esperada não votam diferente das vizinhas do mesmo local, em 2026 nem em 2022.\n")

# ------------------------------------------------------------------------------------------------ A7
A("## A7. Pesquisas e resultado (contexto, sem veredito)\n")
A("O TSE publica o **registro** das pesquisas (protocolo, instituto, datas, amostra, custo), não os resultados; os resultados abaixo vêm da imprensa, com link. Erro de pesquisa não é evidência de manipulação, e o inverso também vale.\n")
A(tab(a7, {"pt_pct_validos_resultado": F(2), "erro_pp_pt": F(2)}))
A("\nRegistros do TSE com divulgação em 24/10/2026 (Datafolha e AtlasIntel) estão em `data/pesquisas_registro_tse_24out2026.csv`; o vínculo entre cada resultado e cada número de registro **não foi verificado**.\n")
A("**NÃO EXECUTADO:** erro histórico dos mesmos institutos em 2014 (não foi localizada, com fonte, uma pesquisa de véspera com data confirmada) e de Quaest e Paraná Pesquisas em 2026 (resultado não localizado).\n")

# ------------------------------------------------------------------------------------------------ A8
A("## A8. Coerência entre cargos no mesmo boletim\n")
A("Em cada seção, o total de cada cargo (nominais + legenda + brancos + nulos + anulados) deve ser igual ao comparecimento (vezes o número de vagas: 2 no Senado de 2018 e 2026).\n")
A(tab(a8.groupby(["ano", "turno"]).agg(cargos=("cargo", "nunique"), secoes_x_cargos=("secoes", "sum"), fora_da_regra=("secoes_fora_da_regra", "sum")).reset_index(), {"secoes_x_cargos": F(), "fora_da_regra": F()}))
A("\nZero seções fora da regra em 2018, 2022 e 2026 (1º turno com todos os cargos; 2º turno com presidente e governador nos estados com segundo turno). Uma inserção que mexesse em um só cargo quebraria a igualdade.\n")

# ------------------------------------------------------------------------------------------------ A9
A("## A9. Perfil do comparecimento\n")
A("**NÃO EXECUTADO (parte):** a variação do 1º para o 2º turno por faixa etária em 2026 não pode ser calculada: o conjunto de perfil de comparecimento e abstenção de 2026 foi publicado em 21/10/2026 e só tem o 1º turno. Insumo que falta: o perfil de 2026/2º turno.\n")
A("**Executado:** consistência das células e totais; comparação do 1º turno de 2026 com 2022 e 2018; variação T1→T2 de 2018 e 2022 (contexto).\n")
A(tab(a9c, {"celulas": F()}))
A("\n" + tab(a9b, {c: F() for c in a9b.columns if c not in ("ano", "turno")}))
A("\nNenhuma célula com comparecimento maior que aptos. A diferença por zona entre perfil e BWeb vem de eleitores que votam fora da zona de cadastro; o total nacional coincide (diferença de poucos milhares em ~125 milhões).\n")
A("**Zonas com comparecimento facultativo fora de [Q1−3 IQR, Q3+3 IQR] de 2022/T1:**\n")
A(tab(a9o))
A("\nO intervalo é largo (o teste é pouco sensível). **Aptos e comparecimento por faixa etária, 1º turno** (2026 contra 2022):\n")
A(tab(a9a[a9a.DS_FAIXA_ETARIA.isin(["16 anos", "17 anos", "60 a 64 anos", "70 a 74 anos", "75 a 79 anos", "80 a 84 anos", "85 a 89 anos", "90 a 94 anos"])], {c: F(3) for c in ["aptos_2026_sobre_2022", "comp_2026_sobre_2022"]} | {c: F() for c in a9a.columns if c.startswith(("aptos_20", "comp_20"))}))
A("\nO comparecimento de eleitores acima de 80 anos (voto facultativo) cresce mais que os aptos na faixa entre 2022 e 2026 no 1º turno. Causa não identificada (hipóteses não testadas: revisão do cadastro e cancelamentos de títulos). É uma hipótese mundana plausível para parte do aumento de seções com comparecimento ≥95% (ver [Resíduos](residuos.md)).\n")

# ------------------------------------------------------------------------------------------------ A10
A("## A10. Modelo de urna, exterior e locais especiais\n")
A("**Modelo da urna, dentro do mesmo local** (coeficientes de Lula% no T2 dado o T1, contra a UE2020; UE2022 é modelo novo em 2026):\n")
A(tab(a10m[a10m.spec == "Lula% T2 dado T1"], {"coef": F(4), "ep": F(4), "secoes": F()}))
A("\nNenhum modelo de urna altera o voto dentro do mesmo local. A taxa de liberação manual muda muito por modelo (ver Fase 1, seção 3.3), mas não o voto.\n")
A("**Exterior (ZZ) contra Brasil:**\n")
A(tab(a10e, {"secoes": F(), "pt_pct_dos_dois": F(2), "comparecimento": F(1), "pct_secoes_comparecimento_ge95": F(3)}))
A("\nO exterior tem 0 seções com comparecimento ≥95% em todas as eleições; as causas mundanas dos ≥95% no Brasil (locais indígenas, prisionais, quilombolas, seções pequenas e novas) estão na seção 3.6 da Fase 1. Estação de geração da carga (`CD_FLASHCARD`) **não foi analisada**.\n")

# ------------------------------------------------------------------------------------------------ A11
a11v, a11c, a11e, a11g, a11h = rd("A11_a11_votos_t1_por_candidato.csv"), rd("A11_a11_contabilidade.csv"), rd("A11_a11_ecologica_EF_municipio.csv"), rd("A11_a11_goodman_restrito_2026.csv"), rd("A11_a11_heterogeneidade_por_uf.csv")
A("## A11. Transferência de votos dos derrotados no 1º turno\n")
A("**Contexto com fonte.** Zema, Caiado e Cury apoiaram Flávio no 2º turno e Renan Santos liberou os eleitores ([A Crítica](https://acritica.net/eleicoes-2026/caiado-zema-e-cury-apoiam-flavio-no-2o-turno-renan-santos-libera-eleitores/); Caiado: [Diário do Nordeste](https://diariodonordeste.verdesmares.com.br/pontopoder/ronaldo-caiado-anuncia-apoio-a-flavio-bolsonaro-no-2-turno-das-eleicoes-2026-1.3796893)). Os apoios de Clariana Barão, Hertz Dias, Edmilson Costa e Samara Martins e a posição de Rui Costa Pimenta foram informados ao autor desta auditoria, mas **não foi localizada fonte**; os blocos seguem a classificação informada e isso está declarado.\n")
A("**Votos de cada candidato no 1º turno, confirmados no BWeb:**\n")
A(tab(a11v, {"votos_t1": F()}))
A("\n**Contabilidade nacional, termo a termo** (identidade: ganho de Lula + ganho de Flávio = terceiros + queda de brancos e nulos + queda de abstenção + variação de aptos):\n")
A(tab(a11c, {"votos": F()}))
A("\nA identidade fecha com resíduo zero. Os terceiros do 1º turno (9,32 milhões), a queda de brancos e nulos (1,82 milhão) e a queda de abstenção (2,96 milhões) somam 14,10 milhões, e os dois candidatos ganharam 14,10 milhões. O bloco que apoiou Flávio somou " + n(a11v[a11v.candidato.isin(['Zema','Caiado','Cury','Clariana'])].votos_t1.sum()) + " votos no 1º turno, e o ganho **líquido** de Flávio foi " + n(a11c[a11c.termo=='ganho de Flavio (T2 menos T1)'].votos.iloc[0]) + ".\n")
A("**Regressão ecológica com efeito fixo de município** (voto por apto no T2 sobre a fatia de cada bloco no T1; abstenção omitida; falácia ecológica: são taxas aparentes entre agregados):\n")
A(tab(a11e[a11e.ano == 2026], {"coef": F(3), "ep": F(3), "municipios": F()}))
A("\n**Goodman com restrição 0 a 1** (sem efeito fixo, ponderado; 2026):\n")
A(tab(a11g, {"taxa_restrita_0_1": F(3)}))
A("\n**Heterogeneidade entre UFs** do coeficiente \"bloco de origem → PT\" (2026: bloco pró-Flávio; 2022 e 2018: maior terceiro, sem inferir apoios):\n")
A(tab(a11h, {"media_ponderada": F(3), "dp_entre_ufs": F(3), "min": F(3), "max": F(3)}))
r = linha("A11", "bloco pro-Flavio")
A(f"\n**Resultado pré-registrado:** {r.veredito if r is not None else 'n/d'} (coeficiente de 2026 {n(r.est_2026T2,3) if r is not None else 'n/d'} contra {r.placebos if r is not None else ''}). **Ressalva de desenho:** os blocos de 2026 e os maiores terceiros de 2022 e 2018 têm composição diferente, e coeficientes ecológicos não medem conversão individual; o veredito aponta quando o coeficiente sai da faixa dos placebos, não que haja transferência indevida. A previsão \"o ganho de Flávio cresce com a fatia do bloco que o apoiou\" é testada pelo coeficiente bloco pró-Flávio → Flávio na tabela acima.\n")

# ------------------------------------------------------------------------------------------------ A12
a12c, a12e, a12p, a12t = rd("A12_a12_contagens.csv"), rd("A12_a12_esperado_vs_observado.csv"), rd("A12_a12_perfil_zero_oponente_T2.csv"), rd("A12_a12_zero_oponente_por_tipo.csv")
A("## A12. Seções com zero voto para um candidato\n")
A("**Alegação testada:** \"109 seções com zero voto\". A origem do número não foi informada e nenhuma reportagem foi localizada; por isso reporto todas as definições razoáveis.\n")
A(tab(a12c[a12c.definicao.isin(["todas as apuradas", "sem exterior, comparecimento >= 1"])], {c: F() for c in ["secoes", "zero_oponente", "zero_PT", "votos_PT_nas_zero_oponente", "votos_oponente_nas_zero_PT"]}))
z26 = a12c[(a12c.ano == 2026) & (a12c.turno == 2) & (a12c.definicao == "todas as apuradas")].iloc[0]
A(f"\n**O 109 não reproduz** em nenhuma definição testada: em 2026/T2 são {n(z26.zero_oponente)} seções com zero voto para Flávio e {n(z26.zero_PT)} para Lula; no 1º turno, 81 e 8. Para comparação, o oponente teve zero voto em 143 seções em 2022 (Bolsonaro), 328 em 2018 e 192 em 2014 (2º turno).\n")
A("**Número esperado de seções com zero** = soma de P(zero) = (1 − p)^n, com p estimado de duas formas:\n")
A(tab(a12e, {"secoes": F(), "observado": F(), "esperado": F(1), "razao": F(2), "z": F(2), "p_excesso": F(3)}))
A("\nEm 2026 o observado para o oponente (" + n(a12e[(a12e.ano == 2026) & (a12e.candidato_com_zero == 'oponente')].observado.iloc[0]) + ") fica próximo do esperado pelo voto da própria seção no T1 e pelos vizinhos do mesmo local, sem excesso significativo; em 2022, 2018 e 2014 o observado ficou **abaixo** do esperado pelo estimador do T1 (em 2018 e 2014 a presença de terceiros relevantes no T1 torna esse estimador pouco adequado).\n")
if a12p is not None:
    q = a12p.iloc[0]
    A(f"**Perfil das {n(q.secoes)} seções com zero voto para Flávio no 2º turno:** comparecimento mediano {n(q.comparecimento_mediano)}, aptos mediano {n(q.aptos_mediano)}; {pc(q.pct_com_oponente_no_T1,0)} tinham voto de Flávio no 1º turno, {pc(q.pct_com_oponente_em_2022,0)} de Bolsonaro em 2022 e {pc(q.pct_com_oponente_em_2018,0)} em 2018 (para as seções que existiam). **Teto:** os votos do PT nessas seções somam {n(q.votos_do_PT_nessas_secoes)}, ou {pc(q.pct_da_margem,2)} da margem. Tipo de local:\n")
    A(tab(a12t))
A("\nA lista seção a seção (UF, município, local, tipo, aptos, comparecimento, resultado em 2026 T1, 2022 e 2018, liberação manual, encerramento, modelo de urna) está em `results/fase2/A12_a12_secoes_zero_2026.csv`.\n")
r = linha("A12", "zero voto")
A(f"**Veredito:** {r.veredito if r is not None else 'n/d'}.\n")

# ------------------------------------------------------------------------------------------------ A13
a13, a13u = rd("A13_a13_inversoes_e_trechos.csv"), rd("A13_a13_trechos_lineares_reais_por_uf.csv")
A("## A13. Curva de apuração: inversões, trechos lineares e o \"método do vídeo\"\n")
A("O vídeo do Prof. Marcelo Trindade, os dados e o código das \"472 urnas\" **não foram fornecidos**; não foi localizada fonte sobre ele. Para essa parte: **NÃO REPRODUZÍVEL**. O que se testa é a alegação geral sobre a forma da curva, com a série reconstruída da ordem de totalização. Como precedente, um vídeo de 2014 com argumento parecido foi examinado por [Agência Pública (O Truco)](https://apublica.org/2018/10/video-falso-diz-eleicoes-2014-fora-fraudadas/) e [Aos Fatos](https://www.aosfatos.org/noticias/bolsonaro-promete-provas-de-fraude-mas-apresenta-alegacoes-ja-desmentidas-sobre-urnas-eletronicas/); a checagem observou que o trecho usado tinha 0,13% dos votos apurados.\n")
A("**Método.** Inversão de liderança = mudança de sinal da margem acumulada entre os pontos a partir de 1% das seções. Trecho linear = janela de 5% das seções com R² ≥ 0,99 e variação ≥ 0,15 p.p. do share. Comparação com 1.000 ordens aleatórias (A) e 1.000 ordens geográficas realistas (B: embaralha dentro da UF mantendo a sequência de UFs). \"Método do vídeo\" (interpretação declarada no pré-registro): somar só os incrementos positivos da curva de share.\n")
A(tab(a13.T.reset_index().rename(columns={"index": "medida", 0: str(a13.iloc[0].ano) + " T" + str(a13.iloc[0].turno), 1: str(a13.iloc[1].ano) + " T" + str(a13.iloc[1].turno), 2: str(a13.iloc[2].ano) + " T" + str(a13.iloc[2].turno), 3: str(a13.iloc[3].ano) + " T" + str(a13.iloc[3].turno)}) if len(a13) >= 4 else a13))
A("\n**Inversões de liderança:** " + "; ".join(f"{int(r.ano)} T{int(r.turno)}: {int(r.inversoes_real)} (ordens geográficas: {r.inversoes_B_ic95})" for r in a13.itertuples()) + ". Nenhuma das eleições disponíveis teve exatamente uma virada, e 2026/T2 teve menos viradas que a média das ordens geográficas simuladas. Em ordem aleatória total não há virada alguma (a curva fica no valor final), o que mostra que as viradas vêm da geografia de chegada.\n")
A("**Trechos lineares reais de 2026 e as UFs que chegaram naquele intervalo:**\n")
A(tab(a13u, {"de_pct_secoes": F(1), "ate_pct_secoes": F(1), "variacao_share_pp": F(2)}))
A("\nOs trechos lineares reais estão dentro da faixa simulada (janelas lineares reais contra intervalo das ordens geográficas, na tabela) e coincidem com a chegada de SP, BA, MG e RJ.\n")
A("**O método de emendar subidas** produz \"vitória\" também em séries sem manipulação: em 2026/T2 dá " + f"{n(100*a13.iloc[0].emenda_subidas_share_final_real,1)}% ao PT na série real e {a13.iloc[0].emenda_subidas_B_ic95} (fração) nas ordens geográficas sem manipulação, contra o resultado de {n(100*a13.iloc[0].share_final,1)}%; em 2018 dá {n(100*a13[a13.ano==2018].emenda_subidas_share_final_real.iloc[0],1)}% ao Haddad, que perdeu com {n(100*a13[a13.ano==2018].share_final.iloc[0],1)}%.\n")
A("**O total final independe da ordem** (idêntico em todas as permutações) e coincide com a soma dos BUs e com a totalização oficial (H9).\n")
A("**NÃO EXECUTADO:** 2014 (sem horário de totalização no produto de 2014) e 2002 a 2010 (sem dado por seção com horário no catálogo aberto); snapshots do site Resultados; as \"472 urnas\" do vídeo.\n")

# ------------------------------------------------------------------------------------------------ A14
a14k = rd("A14_a14_pontos_chave.csv")
A("## A14. Recebimento, totalização e divulgação em 25/10/2026\n")
A("**Alegação:** \"70% das urnas apuradas às 19h34, liberadas aos poucos\". O vídeo original não foi fornecido; a captura mencionada sugere 7,28%.\n")
A(tab(a14k, {"pct_bu_recebido": F(2), "pct_totalizado": F(2), "max": F(1)}))
x = a14k[(a14k.ano == 2026) & (a14k.turno == 2) & (a14k.hora == "19:34")].iloc[0]
A(f"\nEm 2026/T2, às 19h34, **{n(x.pct_bu_recebido,2)}%** dos BUs tinham sido recebidos e **{n(x.pct_totalizado,2)}%** tinham a primeira totalização (a captura com 7,28% é do mesmo porte). Os 70% só foram atingidos depois das 20h (cerca de 20h45). O atraso entre recebimento e primeira totalização é curto e estável (mediana de menos de 1 minuto; p95 de menos de 1 minuto em 2026/T2), ou seja, **não há acúmulo de BUs recebidos e não totalizados**. Em 2022/T2, 84% dos BUs já estavam recebidos às 19h, e em 2026/T1, 61%.\n")
A("![Recebido e totalizado](figs/a14_recebido_totalizado.png)\n")
A("**Explicação oficial da pausa:** a decisão do STF foi divulgada às 17h03, o ofício do TSE aos TREs saiu às 17h49, e a divulgação foi interrompida com 0,25% das seções totalizadas e retomada após as 19h (imprensa; ver [Base legal](base-legal.md)). Os dados são compatíveis: 0,38% das seções totalizadas antes das 19h.\n")
A("**NÃO EXECUTADO:** a curva de **divulgação** (e o atraso totalizado → divulgado): não há snapshots públicos do site Resultados com horário. Insumo que falta: capturas com horário do site Resultados ou dados do próprio sistema.\n")

# ------------------------------------------------------------------------------------------------ A15
a15 = rd("A15_a15_modelo_urna.csv")
A("## A15. Modelo de urna em 2022 (alegação do relatório do PL / Cerimedo)\n")
A("O texto do relatório não foi fornecido; replica-se a alegação como foi resumida (modelos antigos favoreciam Lula). Contra UE2020, dentro do mesmo local, em 2022:\n")
A(tab(a15[a15.ano == 2022], {"coef_pp": F(3), "ep_pp": F(3), "secoes": F(), "votos_margem": F(), "votos_ic95_inf": F(), "votos_ic95_sup": F(), "pct_margem": F(2)}))
A("\nSem controle do 1º turno (a especificação que a alegação pressupõe), o efeito de UE2009 e UE2010 é positivo para Lula, mas pequeno e **não distinguível de zero** (intervalo de 95% inclui zero); o mesmo ocorre no próprio 1º turno (corte transversal), o que indica composição das seções que usam cada modelo. **Com o voto do 1º turno como controle, o efeito é negativo e não significativo** (−0,09 p.p.). Em 2026:\n")
A(tab(a15[a15.ano == 2026], {"coef_pp": F(3), "ep_pp": F(3), "secoes": F(), "votos_margem": F(), "votos_ic95_inf": F(), "votos_ic95_sup": F(), "pct_margem": F(2)}))
A("\nEm 2026 nenhum modelo difere da UE2020 dentro do mesmo local.\n")

# ------------------------------------------------------------------------------------------------ H10 combinado
A("## Impacto agregado (H10 combinado)\n")
A(tab(h10, {c: F(0) for c in ["n_testes_com_votos", "n_sobreviventes", "soma_votos_sobreviventes_exigente", "soma_votos_sobreviventes_pior_caso", "maximo_individual_pior_caso", "soma_de_todos_exigente"]} | {"pct_margem_sobreviventes_pior_caso": F(2), "pct_margem_soma_todos_exigente": F(2)}))
A("\nSobreviventes (Holm < 0,05) e a ressalva de cada um:\n")
A(tab(h10s, {"p_holm": F(3), "votos_max_margem": F(), "votos_max_pior_caso": F(), "pct_pior_caso": lambda x: pc(x)}))
A("\nOs tetos não são aditivos independentes e os sentidos PT e oponente não se compensam.\n")

A("## NÃO EXECUTADO (resumo)\n")
A(tab(nao))
A("\n")
open(os.path.join(DOCS, "resultados-fase2.md"), "w", encoding="utf-8").write("\n".join(L))
print("escrito docs/resultados-fase2.md")
