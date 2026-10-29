#!/usr/bin/env python3
"""docs/index.md, docs/regua-historica.md, docs/dados-reproducao.md e README.md.
Uso: python -I 03e_paginas_finais.py DIR_FASE2 RAIZ"""
import os
import sys, re, sys
import pandas as pd

R, RAIZ = sys.argv[1], sys.argv[2]
rd = lambda f: pd.read_csv(os.path.join(R, f)) if os.path.exists(os.path.join(R, f)) else None


def n(x, d=0):
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")


reg = rd("registro_testes.csv"); nao = rd("nao_executados.csv")
tot = rd("H2_h2_totais_absolutos.csv").set_index(["ano", "turno"])
h3 = rd("H3_h3_recontagem_relogio_cru.csv"); a5n = rd("A5_a5_estimativa_nacional_votos_apos_nominal.csv"); a4 = rd("A4_a4_resumo.csv")
a12c = rd("A12_a12_contagens.csv"); h10 = rd("H10_h10_agregado.csv")
c1d = rd("C1_c1_demonstracao_original.csv"); c12d = rd("C12_c12_demonstracao_original.csv")
c = lambda a, t, col: int(h3[(h3.ano == a) & (h3.turno == t) & (h3.recorte == "com exterior")][col].iloc[0])
z26 = a12c[(a12c.ano == 2026) & (a12c.turno == 2) & (a12c.definicao == "todas as apuradas")].iloc[0]
agg2 = h10[h10.criterio != "como registrado"].set_index("sentido")
a4_26 = a4[a4.ano == 2026].iloc[0]
rs = rd("residuos_soma.csv")

# ------------------------------------------------------------------------------------------------ regua historica
dos = open(os.path.join(RAIZ, "dossie.md"), encoding="utf-8").read()
m = re.search(r"### 3\.13 Régua histórica.*?(?=\n## 4\.)", dos, re.S)
reg_txt = "# Régua histórica (2014, 2018, 2022, 2026)\n\n" + (m.group(0).replace("### 3.13 Régua histórica (2014, 2018, 2022, 2026)", "").strip() if m else "_(seção não encontrada no dossiê)_") + "\n"
open(os.path.join(RAIZ, "docs", "regua-historica.md"), "w", encoding="utf-8").write(reg_txt)

# ------------------------------------------------------------------------------------------------ primeira pagina (A29) e lacunas (A30)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import primeira_pagina as pp
NT = ("Ver [Questões em aberto](residuos.md), [Pontos cegos](pontos-cegos.md), [Fase 3](fase3.md) e a lista de **NÃO EXECUTADO**: cruzamento com boletins impressos (0 conferidos; sem insumo), assinatura criptográfica da urna "
      "(certificado lido, assinatura 0% verificada), curva de divulgação do site Resultados, perfil de comparecimento de 2026/2º turno, 2014 na curva de apuração, as \"472 urnas\" do vídeo, e os testes A21 (parcial), A22, A23, A24 e A25 (parcial) da Fase 3.")
P1 = pp.hero(RAIZ) + "\n" + pp.resultado(RAIZ) + "\n" + pp.resumo_perguntas(RAIZ)
CONTRIB = pp.contribuir(RAIZ)
P1R = pp.resultado(RAIZ) + "\n" + pp.perguntas(RAIZ, True) + "\n" + pp.contribuir(RAIZ, True)

# pagina propria das perguntas em aberto (a secao saiu da pagina inicial; bloco 'Resultado verificado' vem antes, como la)
PG = pp.perguntas(RAIZ).split("\n")
PG[0] = PG[0][1:]
PG.insert(1, "\n> **Antes das lacunas, o resultado verificado:** 0 divergências na cadeia RDV–BU–BWeb–totalização; o excesso medido somado é pequeno diante da margem. Os testes cobrem o que o TSE publica; uma alteração nos elos não publicados (voto digitado, boletim impresso, transmissão) nenhum teste deste dossiê veria. Números na [página inicial](index.md).\n")
open(os.path.join(RAIZ, "docs", "perguntas-em-aberto.md"), "w", encoding="utf-8").write("\n".join(PG) + "\n")
LAC = pp.lacunas(RAIZ, False, NT)
LACR = pp.lacunas(RAIZ, True, NT.replace("](residuos.md)", "](docs/residuos.md)").replace("](pontos-cegos.md)", "](docs/pontos-cegos.md)").replace("](fase3.md)", "](docs/fase3.md)"))

# ------------------------------------------------------------------------------------------------ index
IDX = f"""# Auditoria independente reproduzível: 2º turno presidencial de 2026

Esta é uma **auditoria independente**. Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou. Foi construída para que qualquer perito, de qualquer lado, repita cada número e conteste o que discordar.

> **Versão preliminar (v0.9.3).** A v1.0 sai depois do relatório consolidado do TCU sobre os testes de integridade (prazo até 24/11/2026), da verificação da assinatura criptográfica e de um lote inicial de boletins impressos conferidos ([como enviar](boletins-impressos.md)).

{P1}

{LAC}

{CONTRIB}

## O que foi feito
Análise estatística dos dados oficiais do TSE por seção (BWeb de 2014, 2018, 2022 e 2026, com hash conferido), mais os arquivos de urna (BU, RDV, assinatura e log) de uma amostra de {n(a4_26.secoes)} seções do 2º turno de 2026 e as mesmas seções em 2022 como placebo. Previsões foram registradas antes de cada bloco de análises ([Pré-registro](preregistro.md)); todo teste tem placebo e é simétrico; resultados nulos têm o mesmo destaque que os positivos.

## Resumo dos resultados (números sem adjetivos)
- **Totais e consistência:** Lula 64.256.232, Flávio 59.826.041, margem 4.430.191. O BWeb coincide com `votacao_secao` e com a totalização por zona em 2026.
- **Cadeia da urna (A4):** em {n(a4_26.secoes)} seções de {n(a4_26.UFs)} UFs, o BU digital coincide com o BWeb, o RDV recontado coincide com o BU e os hashes de BU, RDV, imagem e log constam na lista assinada pela urna: {n(a4_26.bu_diferente_do_bweb + a4_26.rdv_diferente_do_bu + a4_26.hash_nao_vinculado)} divergências. **Isso verifica consistência entre arquivos que o TSE publica e não exclui uma alteração coerente feita antes da publicação** ([A18](a18-alteracao-no-meio.md)). A assinatura criptográfica em si **não foi verificada** (0% das seções; NÃO EXECUTADO PARCIAL: falta a chave oficial acessível).
- **Alteração no meio e voto digitado x registrado (A18, A19):** os atrasos documentados (1 hora no 1º turno; recebimento retido até as 19h no 2º) foram testados pela janela de relógio contra placebos, sem excesso detectado, mas esses testes não excluem uma alteração coerente. A correspondência entre voto digitado e voto registrado só é verificada por amostragem no teste de integridade, e o modelo atual não possui registro conferido pelo eleitor ([A19](a19-voto-digitado.md)). Fotos de boletins impressos podem ser enviadas por qualquer pessoa ([como enviar](boletins-impressos.md)).
- **Relatório original:** a tabela de fechamento ({n(c(2026,2,'de_17h01_a_17h15'))} seções entre 17h01 e 17h15), as 8,6 milhões de liberações manuais ({n(tot.loc[(2026,2),'biom_nh_total'])}) e os percentuais da Bahia reproduzem; as conclusões não se sustentam ([página](relatorio-original.md)).
- **Votos depois das 17h (A5):** estimativa a partir dos logs de {n(a5n.estimativa_total.iloc[0])} votos (contagem, não votos de margem) em todo o país (IC95 {n(a5n.ic95_total_inf.iloc[0])} a {n(a5n.ic95_total_sup.iloc[0])}), {n(100*a5n.estimativa_total.iloc[0]/4430191,2)}% da margem de 4.430.191 (comparação direta da contagem com a margem); muitas das seções que fecharam tarde ficaram abertas sem registrar voto depois das 17h.
- **Liberação manual:** caiu 14% de 2022 para 2026; a associação com o voto em Lula existe nos dois turnos de 2026 e não é específica do 2º turno.
- **Curva de apuração, conversão e zero voto (A1, A2, A3, A11, A12, A13, A14):** a curva real e seus trechos lineares ficam dentro da faixa das ordens geográficas simuladas; nenhuma conversão do oponente para o PT é necessária para explicar o resultado nacional; o "109 seções com zero voto" não reproduz (são {n(z26.zero_oponente)} no 2º turno; 143 em 2022, 328 em 2018); às 19h34 só 7,8% dos BUs tinham sido recebidos, não 70%.
- **Linhas com ressalva de desenho (A1, A2, A3, A12):** pelos critérios pré-registrados, saíram com rótulo de excesso, mas **o mesmo teste acusa excesso em séries ou anos sem manipulação** (A1: {int(c1d.iloc[0].simulacoes_que_saem_do_envelope_B_por_20_pontos_ou_mais)} de {int(c1d.iloc[0].simulacoes_sem_manipulacao)} simulações limpas; A2: o PT de 2022; A3: coeficientes negativos em todos os anos; A12: {n(c12d.iloc[0].pct_acusadas,0)}% de simulações limpas). As versões corrigidas não mostram excesso. Resultado original e corrigido, lado a lado, em [Resultados da Fase 2](resultados-fase2.md) e [Questões em aberto](residuos.md).
- **Excesso medido, todos os resíduos somados** (votos de margem): **cerca de {n(rs.excesso_medido_pro_Lula_votos_de_margem.iloc[0])} pró-Lula e {n(rs.excesso_medido_pro_Flavio_votos_de_margem.iloc[0])} pró-Flávio**, {n(100*rs.excesso_medido_pro_Lula_votos_de_margem.iloc[0]/4430191,1)}% e {n(100*rs.excesso_medido_pro_Flavio_votos_de_margem.iloc[0]/4430191,1)}% da margem de 4.430.191, em sentidos opostos ([soma e leitura](residuos.md)).
- **Impacto agregado** (só testes sem ressalva de desenho; unidade: votos de margem; teto de pior caso, não estimativa): {n(agg2.loc['PT','soma_votos_sobreviventes_pior_caso'])} votos de margem pró-Lula e {n(agg2.loc['OPO','soma_votos_sobreviventes_pior_caso'])} pró-Flávio, tetos de pior caso; com as versões corrigidas no lugar das originais, o resultado é o mesmo (nenhuma das quatro versões corrigidas mostra excesso). A margem é 4.430.191.
## Autoria
{{{{AUTORIA}}}}
"""
open(os.path.join(RAIZ, "docs", "index.md"), "w", encoding="utf-8").write(IDX)

# ------------------------------------------------------------------------------------------------ dados e reproducao
DR = """# Dados e reprodução

## Requisitos
Python 3.12; `pip install -r requirements.txt`. Espaço: ~9 GB para os dados de BWeb e demais produtos, mais ~3 GB se baixar os arquivos de urna da amostra (por requisições parciais; baixar todas as UFs inteiras exigiria dezenas de GB). Tempo aproximado em máquina de 16 GB e 8 núcleos: download 10 a 20 minutos; preparação 25 minutos; análises 15 minutos; coleta dos arquivos de urna 1 a 2 horas.

## Ordem de execução
```bash
# dados: lista com URL e hash oficial em data/ (baixar_e_verificar.sh confere os 224 zips do BWeb)
python scripts/01_prepara_bweb.py bu parquet --anos 2022 2026
python scripts/01_prepara_bweb.py bu_hist parquet --anos 2014 2018
python scripts/01b_locais.py dados_tse parquet 2022 2026
python scripts/01c_modelo_urna.py dados_tse parquet 2022 2026
python scripts/05_extras_bweb.py bu parquet2 --anos 2022 2026 ; python scripts/05_extras_bweb.py bu_hist parquet2 --anos 2018
python scripts/06_ordem_totalizacao.py dados_tse parquet 2018 2022 2026
python scripts/07_perfil_agrega.py perfil parquet2 2018 2022 2026
python scripts/12_candidatos_t1.py bu parquet2 2026 ; (idem 2022; bu_hist 2018)
python scripts/09_amostra_urna.py parquet amostra
python scripts/08_arquivos_urna.py local|remoto ...   # ver docstring; uma saida por UF e ano
python scripts/02_executa.py parquet results/fase2 --anos 2014 2018 2022 2026 --zips dados_tse --parquet2 parquet2 --cesp cesp --urna urna_out
python scripts/10_figuras.py parquet results/fase2 docs/figs
python scripts/16_figuras_en.py parquet results/fase2 docs/figs/en en   # versões em inglês de a1, a2, a5, a14 e Klimek; G0 a G4 em inglês: GRAF_LANG=en python scripts/graficos/g1_cadeia.py . [m] (idem g2, g3, g4 e scripts/g0_hero_verificacao.py)
python scripts/03b_monta_fase2.py results/fase2 results/fase1 .   # e 03c, 03d, 03e, 03f (A18, A19, boletins); 13_cert_urna.py e 14_poder_estatistico.py geram as tabelas de assinatura e de poder
python scripts/build_site.py --saida site --pdf relatorio/auditoria-independente-v0.9.3.pdf
```
O código de saída 2 de `02_executa.py` indica testes NÃO EXECUTADOS (lista em `nao_executados.csv`).

## Testes de consistência (CI)
`pytest tests`: valida a consistência interna do BWeb em uma amostra (AP, 2022 e 2026), a regressão com efeito fixo contra um coeficiente conhecido, o registro de testes (interseção-união, Holm) e o leitor de BU e RDV com um boletim real de Roraima.

## Hashes e versões
SHA-512 oficial de cada zip do BWeb em `data/manifest_hash_oficial.csv` (224 de 224 conferidos); SHA-256 dos arquivos como baixados em `data/sha256_entradas.txt`.
"""
open(os.path.join(RAIZ, "docs", "dados-reproducao.md"), "w", encoding="utf-8").write(DR)

# ------------------------------------------------------------------------------------------------ README
RD = f"""# Auditoria independente reproduzível: 2º turno presidencial de 2026

Repositório com scripts, previsões pré-registradas, resultados e documentação de uma auditoria estatística dos dados oficiais do TSE sobre o 2º turno de 25/10/2026 (Lula x Flávio Bolsonaro). **Não é laudo, perícia oficial nem documento homologado.**

Portal: https://baduba.github.io/eleicoes-dossie-2026/ (após a publicação) · PDF: `relatorio/` e release v0.9.3 (versão preliminar).

**Versão preliminar (v0.9.3).** A v1.0 sai depois do relatório consolidado do TCU (até 24/11/2026), da verificação da assinatura e de um lote inicial de boletins impressos.

{P1R}

## Objetivo
Permitir que qualquer perito, de qualquer lado, reproduza cada número e conteste o que discordar. Só entra o que sai de script versionado sobre dado oficial com hash conferido, ou afirmação com fonte citada. Todo código e dado estão no repositório para verificação independente. (Os arquivos de origem do TSE entram por URL e hash SHA-512 conferido, em `data/`, e não como cópia; scripts, previsões, resultados e tabelas completos estão no repositório.)

## O que foi e o que não foi testado
- **Testado:** consistência BWeb x `votacao_secao` x totalização; BU digital x BWeb; RDV x BU; vínculo de hash dos arquivos de urna; log x BU e votos depois das 17h (amostra); estatística de seção com placebos (2014, 2018, 2022, 1º turno de 2026); curva de apuração; transições entre turnos; zero voto; modelo de urna; coerência entre cargos; alegações do relatório original.

## Resumo dos vereditos
Nenhum achado, isolado ou somado, alcança a margem de 4.430.191 votos. Esse zero vale para o que o TSE publica; o que não é publicado (voto digitado, boletim impresso, transmissão) nenhum teste deste dossiê veria, e por isso permanece aberto. Itens sem causa identificada estão em [Questões em aberto](docs/residuos.md). Detalhes em [`dossie.md`](dossie.md) (Fase 1) e [`docs/resultados-fase2.md`](docs/resultados-fase2.md).

{LACR}

## Estrutura
`00_preregistro.md` (previsões e adendos), `dossie.md` (Fase 1), `docs/` (portal), `scripts/`, `results/fase1` e `results/fase2` (tabelas e figuras), `data/` (URLs e hashes), `tests/`, `CHANGELOG.md`, `LICENSE`.

## Como reproduzir
Ver [Dados e reprodução](docs/dados-reproducao.md): requisitos, comandos na ordem, tempo e espaço.

## Como contestar
Abra uma *issue* com o número ou a tabela contestada, o script que reproduz a sua versão e o dado de origem.

## Licença
Código: MIT. Texto, tabelas e figuras: CC BY 4.0. Os dados de origem são do TSE e não são redistribuídos aqui.

## Autoria
{{{{AUTORIA}}}}
"""
open(os.path.join(RAIZ, "README.md"), "w", encoding="utf-8").write(RD)
print("paginas finais escritas")
