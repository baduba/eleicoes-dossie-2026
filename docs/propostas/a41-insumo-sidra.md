# A41 — Insumo IBGE/SIDRA baixado e versionado (31/10/2026)

Adendo 19 exigia, antes de rodar A41, o denominador oficial de população em `data/` com hash. Status:
**insumo pronto; o teste A41 NÃO foi rodado** (etapa seguinte, conforme o adendo).

## Download

- **SIDRA 4714** (Censo 2022, população residente total por município):
  `https://apisidra.ibge.gov.br/values/t/4714/n6/all/v/allxp/p/2022` — HTTP 200 (o endpoint de metadados
  `desctabapi.aspx` respondeu 403/Cloudflare, mas isso não bloqueou o endpoint de valores; nenhum contorno
  foi tentado nem necessário).
- **SIDRA 9514** (Censo 2022, população por município e idade, classificação c287 — idades individuais):
  `https://apisidra.ibge.gov.br/values/t/9514/n6/all/p/2022/c287/100362,93070,93084,93085,6572` — HTTP 200.
  Classes: Total (100362), 0 a 4 (93070), 5 a 9 (93084), 10 a 14 (93085) e 15 anos (6572); pop16 derivada
  como Total − (0–4) − (5–9) − (10–14) − (15). Sexo e forma de declaração: Total.

## Arquivo versionado

`data/ibge_populacao_municipios_2022.csv` — 5.570 municípios, colunas `cod_ibge, municipio, pop_total_2022,
pop16_2022`. Totais: população 203.080.756; população 16+ = 160.131.985.

- SHA-256: `292dbf32e8049d54eed7947ed96f2247b823889ffd599ed122bcf43efe9681eb` (registrado em
  `data/sha256_entradas.txt`; URLs em `data/urls_origem.txt`, padrão do diretório).

## Validação

- 5.570 municípios (merge 4714 × 9514: 5.570 `both`, 0 pendências).
- **pop16 derivada bate exatamente** com a que já estava em uso (`results/fase3/A20_mapa_tse_ibge.csv`):
  5.557/5.557 municípios cruzados com diferença zero. O mapa A20 usava a mesma fonte (Censo 2022); agora a
  fonte está versionada no repo com hash.

## Pendente para o teste A41 (Adendo 19)

1. Rodar o teste formal com o denominador versionado (razão comparecimento/pop16, excedente em votos, teto
   em votos de margem, controles por UF e envelhecimento, regra EXCEDENTE REAL / INCONCLUSIVO).
2. Ressalva obrigatória do adendo: citar a fonte IBGE sobre a subcontagem do Censo 2022 na saída.
3. (Opcional, recomendado) Acrescentar projeções IBGE 2022–2026 como segundo denominador para o braço de
   sensibilidade ("INCONCLUSIVO se depender da versão do denominador").
