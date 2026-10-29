# Dados e reprodução

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
python scripts/03b_monta_fase2.py results/fase2 results/fase1 .   # e 03c, 03d, 03e, 03f (A18, A19, boletins); 13_cert_urna.py e 14_poder_estatistico.py geram as tabelas de assinatura e de poder
python scripts/build_site.py --saida site --pdf relatorio/auditoria-independente-v1.0.pdf
```
O código de saída 2 de `02_executa.py` indica testes NÃO EXECUTADOS (lista em `nao_executados.csv`).

## Testes de consistência (CI)
`pytest tests`: valida a consistência interna do BWeb em uma amostra (AP, 2022 e 2026), a regressão com efeito fixo contra um coeficiente conhecido, o registro de testes (interseção-união, Holm) e o leitor de BU e RDV com um boletim real de Roraima.

## Hashes e versões
SHA-512 oficial de cada zip do BWeb em `data/manifest_hash_oficial.csv` (224 de 224 conferidos); SHA-256 dos arquivos como baixados em `data/sha256_entradas.txt`.
