# Data and reproduction

## Requirements
Python 3.12; `pip install -r requirements.txt`. Disk space: ~9 GB for the BWeb data and other products, plus ~3 GB if you download the voting machine files for the sample (via partial requests; downloading all states (UFs) in full would require tens of GB). Approximate time on a 16 GB, 8-core machine: download 10 to 20 minutes; preparation 25 minutes; analyses 15 minutes; collection of voting machine files 1 to 2 hours.

## Execution order
```bash
# data: list with official URL and hash in data/ (baixar_e_verificar.sh checks the 224 BWeb zips)
python scripts/01_prepara_bweb.py bu parquet --anos 2022 2026
python scripts/01_prepara_bweb.py bu_hist parquet --anos 2014 2018
python scripts/01b_locais.py dados_tse parquet 2022 2026
python scripts/01c_modelo_urna.py dados_tse parquet 2022 2026
python scripts/05_extras_bweb.py bu parquet2 --anos 2022 2026 ; python scripts/05_extras_bweb.py bu_hist parquet2 --anos 2018
python scripts/06_ordem_totalizacao.py dados_tse parquet 2018 2022 2026
python scripts/07_perfil_agrega.py perfil parquet2 2018 2022 2026
python scripts/12_candidatos_t1.py bu parquet2 2026 ; (same for 2022; bu_hist 2018)
python scripts/09_amostra_urna.py parquet amostra
python scripts/08_arquivos_urna.py local|remoto ...   # see docstring; one output per state (UF) and year
python scripts/02_executa.py parquet results/fase2 --anos 2014 2018 2022 2026 --zips dados_tse --parquet2 parquet2 --cesp cesp --urna urna_out
python scripts/10_figuras.py parquet results/fase2 docs/figs
python scripts/16_figuras_en.py parquet results/fase2 docs/figs/en en   # English versions of a1, a2, a5, a14 and Klimek; G0 to G4 in English: GRAF_LANG=en python scripts/graficos/g1_cadeia.py . [m] (same for g2, g3, g4 and scripts/g0_hero_verificacao.py)
python scripts/03b_monta_fase2.py results/fase2 results/fase1 .   # and 03c, 03d, 03e, 03f (A18, A19, poll-receipts); 13_cert_urna.py and 14_poder_estatistico.py generate the signature and statistical power tables
python scripts/build_site.py --saida site --pdf relatorio/auditoria-independente-v0.9.3.pdf
```
Exit code 2 from `02_executa.py` indicates tests NOT EXECUTED (listed in `nao_executados.csv`).

## Consistency tests (CI)
`pytest tests`: validates the internal consistency of BWeb on a sample (AP, 2022 and 2026), the fixed-effect regression against a known coefficient, the test registry (intersection-union, Holm), and the BU and RDV reader with a real poll-receipt from Roraima.

## Hashes and versions
Official SHA-512 for each BWeb zip in `data/manifest_hash_oficial.csv` (224 of 224 verified); SHA-256 of the files as downloaded in `data/sha256_entradas.txt`.
