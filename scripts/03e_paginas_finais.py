#!/usr/bin/env python3
"""docs/index.md, docs/regua-historica.md, docs/dados-reproducao.md e README.md.
Uso: python -I 03e_paginas_finais.py DIR_FASE2 RAIZ"""
import os, re, sys
import pandas as pd

R, RAIZ = sys.argv[1], sys.argv[2]
rd = lambda f: pd.read_csv(os.path.join(R, f)) if os.path.exists(os.path.join(R, f)) else None


def n(x, d=0):
    s = f"{x:,.{d}f}"; return s.replace(",", "X").replace(".", ",").replace("X", ".")


reg = rd("registro_testes.csv"); nao = rd("nao_executados.csv")
tot = rd("H2_h2_totais_absolutos.csv").set_index(["ano", "turno"])
h3 = rd("H3_h3_recontagem_relogio_cru.csv"); a5n = rd("A5_a5_estimativa_nacional_votos_apos_nominal.csv"); a4 = rd("A4_a4_resumo.csv")
a12c = rd("A12_a12_contagens.csv"); h10 = rd("H10_h10_agregado.csv")
c = lambda a, t, col: int(h3[(h3.ano == a) & (h3.turno == t) & (h3.recorte == "com exterior")][col].iloc[0])
z26 = a12c[(a12c.ano == 2026) & (a12c.turno == 2) & (a12c.definicao == "todas as apuradas")].iloc[0]
agg = h10[h10.criterio == "como registrado"].set_index("sentido") if "criterio" in h10 else h10.set_index("sentido")
agg2 = h10[h10.criterio != "como registrado"].set_index("sentido") if "criterio" in h10 else agg
a4_26 = a4[a4.ano == 2026].iloc[0]

# ------------------------------------------------------------------------------------------------ regua historica
dos = open(os.path.join(RAIZ, "dossie.md"), encoding="utf-8").read()
m = re.search(r"### 3\.13 Régua histórica.*?(?=\n## 4\.)", dos, re.S)
reg_txt = "# Régua histórica (2014, 2018, 2022, 2026)\n\n" + (m.group(0).replace("### 3.13 Régua histórica (2014, 2018, 2022, 2026)", "").strip() if m else "_(seção não encontrada no dossiê)_") + "\n"
open(os.path.join(RAIZ, "docs", "regua-historica.md"), "w", encoding="utf-8").write(reg_txt)

# ------------------------------------------------------------------------------------------------ index
IDX = f"""# Auditoria independente reproduzível: 2º turno presidencial de 2026

Esta é uma **auditoria independente**. Não é laudo, perícia oficial nem documento homologado: nenhum órgão homologou. Foi construída para que qualquer perito, de qualquer lado, repita cada número e conteste o que discordar.

## O que foi feito
Análise estatística dos dados oficiais do TSE por seção (BWeb de 2014, 2018, 2022 e 2026, com hash conferido), mais os arquivos de urna (BU, RDV, assinatura e log) de uma amostra de {n(a4_26.secoes)} seções do 2º turno de 2026 e as mesmas seções em 2022 como placebo. Previsões foram registradas antes de cada bloco de análises ([Pré-registro](preregistro.md)); todo teste tem placebo e é simétrico; resultados nulos têm o mesmo destaque que os positivos.

## Resumo dos resultados (números sem adjetivos)
- **Totais e consistência:** Lula 64.256.232, Flávio 59.826.041, margem 4.430.191. O BWeb coincide com `votacao_secao` e com a totalização por zona em 2026.
- **Cadeia da urna (A4):** em {n(a4_26.secoes)} seções de {n(a4_26.UFs)} UFs, o BU digital coincide com o BWeb, o RDV recontado coincide com o BU e os hashes de BU, RDV, imagem e log constam na lista assinada pela urna: {n(a4_26.bu_diferente_do_bweb + a4_26.rdv_diferente_do_bu + a4_26.hash_nao_vinculado)} divergências. A assinatura criptográfica em si **não foi verificada** (falta a especificação do TSE).
- **Relatório original:** a tabela de fechamento ({n(c(2026,2,'de_17h01_a_17h15'))} seções entre 17h01 e 17h15), as 8,6 milhões de liberações manuais ({n(tot.loc[(2026,2),'biom_nh_total'])}) e os percentuais da Bahia reproduzem; as conclusões não se sustentam ([página](relatorio-original.md)).
- **Votos depois das 17h (A5):** estimativa a partir dos logs de {n(a5n.estimativa_total.iloc[0])} votos em todo o país (IC95 {n(a5n.ic95_total_inf.iloc[0])} a {n(a5n.ic95_total_sup.iloc[0])}), {n(100*a5n.estimativa_total.iloc[0]/4430191,2)}% da margem; muitas das seções que fecharam tarde ficaram abertas sem registrar voto depois das 17h.
- **Liberação manual:** caiu 14% de 2022 para 2026; a associação com o voto em Lula existe nos dois turnos de 2026 e não é específica do 2º turno.
- **Curva de apuração, conversão e zero voto (A1, A2, A3, A11, A12, A13, A14):** a curva real e seus trechos lineares ficam dentro da faixa das ordens geográficas simuladas; nenhuma conversão do oponente para o PT é necessária para explicar o resultado nacional; o "109 seções com zero voto" não reproduz (são {n(z26.zero_oponente)} no 2º turno; 143 em 2022, 328 em 2018); às 19h34 só 7,8% dos BUs tinham sido recebidos, não 70%.
- **Pelos critérios pré-registrados**, A1, A2 e A3 saem como "excesso detectado" e A12 como "excesso detectável, magnitude irrelevante". Cada uma tem **ressalva de desenho** documentada (o controle posterior mostrou que o desenho media outra coisa: geografia de chegada, espelho entre 2022 e 2026, coeficientes negativos em todos os anos, estimador inadequado nos placebos). As linhas foram mantidas como saíram; ver [Resultados da Fase 2](resultados-fase2.md) e [Questões em aberto](residuos.md).
- **Impacto agregado:** a soma dos tetos dos testes com excesso detectado, sem as linhas com ressalva de desenho, é {n(agg2.loc['PT','soma_votos_sobreviventes_pior_caso'])} votos pró-Lula e {n(agg2.loc['OPO','soma_votos_sobreviventes_pior_caso'])} pró-Flávio; com todas as linhas, {n(agg.loc['PT','soma_votos_sobreviventes_pior_caso'])} e {n(agg.loc['OPO','soma_votos_sobreviventes_pior_caso'])}; a diferença vem da linha A3, cujo teto de pior caso não tem interpretação causal (coeficientes ecológicos negativos em todos os anos; ver ressalva). A margem é 4.430.191.

## O que não foi testado
Ver [Questões em aberto](residuos.md), [Pontos cegos](pontos-cegos.md) e a lista de **NÃO EXECUTADO**: cruzamento com boletins impressos (sem insumo), assinatura criptográfica da urna, curva de divulgação do site Resultados, perfil de comparecimento de 2026/2º turno, 2014 na curva de apuração, as "472 urnas" do vídeo.

## Autoria
[a preencher por Julio antes da publicação]
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
python scripts/03b_monta_fase2.py results/fase2 results/fase1 .   # e 03c, 03d, 03e
python scripts/build_site.py --saida site --pdf relatorio/auditoria-independente-v1.0.pdf
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

Portal: https://baduba.github.io/eleicoes-dossie-2026/ (após a publicação) · PDF: `relatorio/` e release v1.0.

## Objetivo
Permitir que qualquer perito, de qualquer lado, reproduza cada número e conteste o que discordar. Só entra o que sai de script versionado sobre dado oficial com hash conferido, ou afirmação com fonte citada.

## O que foi e o que não foi testado
- **Testado:** consistência BWeb x `votacao_secao` x totalização; BU digital x BWeb; RDV x BU; vínculo de hash dos arquivos de urna; log x BU e votos depois das 17h (amostra); estatística de seção com placebos (2014, 2018, 2022, 1º turno de 2026); curva de apuração; transições entre turnos; zero voto; modelo de urna; coerência entre cargos; alegações do relatório original.
- **Não testado / NÃO EXECUTADO:** cruzamento com boletins impressos (sem insumo); assinatura criptográfica da urna (sem a especificação); curva de divulgação (sem snapshots); perfil de comparecimento de 2026/2º turno; curva de 2014; as "472 urnas". Lista completa e motivos em [`results/fase2/nao_executados.csv`](results/fase2/nao_executados.csv).

## Resumo dos vereditos
Nenhum achado, isolado ou somado, alcança a margem de 4.430.191 votos. Itens sem causa identificada estão em [Questões em aberto](docs/residuos.md). Detalhes em [`dossie.md`](dossie.md) (Fase 1) e [`docs/resultados-fase2.md`](docs/resultados-fase2.md).

## Estrutura
`00_preregistro.md` (previsões e adendos), `dossie.md` (Fase 1), `docs/` (portal), `scripts/`, `results/fase1` e `results/fase2` (tabelas e figuras), `data/` (URLs e hashes), `tests/`, `CHANGELOG.md`, `LICENSE`.

## Como reproduzir
Ver [Dados e reprodução](docs/dados-reproducao.md): requisitos, comandos na ordem, tempo e espaço.

## Como contestar
Abra uma *issue* com o número ou a tabela contestada, o script que reproduz a sua versão e o dado de origem.

## Licença
Código: MIT. Texto, tabelas e figuras: CC BY 4.0. Os dados de origem são do TSE e não são redistribuídos aqui.

## Autoria
[a preencher por Julio antes da publicação]
"""
open(os.path.join(RAIZ, "README.md"), "w", encoding="utf-8").write(RD)
print("paginas finais escritas")
