# Dossier: audit of the 2026 presidential runoff data (Lula x Flávio Bolsonaro)

> **Units.** "Margin votes" is the change in the difference Lula minus Flávio: switching one vote changes the margin by 2. Every ceiling, central estimate, and aggregate in votes in this document is in margin votes and should be read against the official margin of 4.430.191. "Votes (count)" is a plain number of votes, and is labeled as such. Full definition in Methodology.

Generated on 2026-10-28 from public TSE files. All figures in this text come from the CSVs in `results/fase1/` (script `03_monta_dossie.py`). Predictions and criteria were fixed before the data in `00_preregistro.md`.

## 1. Executive summary

1. Data: BWeb (poll-receipt (BU) by section) for 2014, 2018, 2022 and 2026, T1 and T2, 224 zips with verified hash. The 2026/T2 totals are Lula 64.256.232 and Flávio 59.826.041, equal to those published.
2. Consistency: the BWeb matches `votacao_secao` in every paired section from 2014 to 2026, except 1 section in 2018/T1 where `votacao_secao` has 66 more votes than the BWeb and than the total published by the TSE (no discrepancy in 2022 or 2026), and matches the 2026 municipality/zone tabulation (0 zones with a difference). There are 0 violations of internal consistency of the BUs.
3. Manual voter release (registered biometrics, voter not enabled by them): 8.632.488 in 2026/T2, the figure cited in the report; 10.011.347 in 2022/T2. The aggregate rate went from 8,06% to 6,73%.
4. H1: with polling-place fixed effects and control for the section's own T1 vote, the manual rate does not predict additional votes for Lula in T2 (coefficient 0,002 versus 0,016 in 2022). Worst-case ceiling: 0 votes.
5. H3 and H4: the report's count was reproduced (339.593 sections between 5:01pm and 5:15pm by the voting machine's raw clock). 6.342 sections recorded closing at or after 7pm on the voting machine's clock, versus 20 in 2022/T2. In them, the Lula vote does not differ from the other sections of the same place; ceilings of 0,03% to 0,19% of the margin.
6. The number of votes cast after 5pm is not measurable with these data (the BWeb does not carry a voting log).
7. H5 to H8 and historical yardstick: turnout, local outliers, and 2026 digits fall within the range observed in 2014, 2018 and 2022. None of the patterns A, B or C fits by the fixed criterion (C: 5 of 12 metrics; see 3.13).
8. Two tests show excess after Holm: Flávio votes per eligible voter x manual rate (worst-case ceiling, not an estimate: 122.543 margin votes, 2,77% of the margin, in the direction favorable to Flávio) and change in Lula vote between years x change in manual rate (worst-case ceiling, not an estimate: 38.394 margin votes, 0,87%).
9. Residuals with no identified cause: 639 sections with turnout >= 95% (2,5 times the composition expectation; already 1,9 times in T1; ceiling 0,43%) and new sections (+0,54 p.p. of Lula in T2 given T1; +1,34 p.p. in 2018; worst-case ceiling 2,08%).
10. Aggregate impact: the sum of the worst-case ceilings (not estimates) of the tests with detected excess is 38.394 margin votes in the pro-Lula direction (0,87% of the margin) and 122.543 margin votes in the pro-Flávio direction. No finding, alone or summed, reaches 4.430.191 votes. Not executed: cross-check with printed poll-receipts (no input).

## 2. Data and versions

| Input | Source | Files | Verification |
|---|---|---|---|
| BWeb 2026, 2022 | `cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes{2026,2022}/buweb/` via CKAN API (`dadosabertos.tse.jus.br`) | 56 zips per year (27 UF + ZZ, T1 and T2) | TSE SHA-512 verified: 112/112 |
| BWeb 2018, 2014 | same catalog | 56 zips per year | 2018: SHA-512; 2014: SHA-1 (what the TSE publishes); 112/112 verified |
| `votacao_secao` 2014 to 2026, `detalhe_votacao_secao` 2022 and 2026, `votacao_candidato_munzona` 2026 | `cdn.tse.jus.br/estatistica/sead/odsele/` | 1 zip per product/year | used in H9, place type, and voting machine model |

SHA-256 hash of all inputs: `dados/sha256_entradas.txt`. URLs: `dados/urls_origem.txt`.

**BWeb columns used** (names found in the header):

| Concept | 2026 | 2022 | 2018 | 2014 |
|---|---|---|---|---|
| Manual voter release | `QT_ELEI_BIOM_SEM_HABILITACAO` | `QT_ELEITORES_BIOMETRIA_NH` | `QT_ELEITORES_BIOMETRIA_NH` | nonexistent |
| Opening / closing | `DT_ABERTURA`, `DT_ENCERRAMENTO` | same | same | nonexistent |
| BU receipt / issuance | `DT_BU_RECEBIDO`, `DT_EMISSAO_BU` | same | nonexistent | receipt date only |
| Aggregated sections | `DS_SECOES_AGREGADAS` | `DS_AGREGADAS` | `DS_AGREGADAS` | positional |
| Format | CSV with header | CSV with header | CSV with header (`SG_ UF` with space) | `.txt` without header, 31 positional fields |

**Definition of the manual voter release measure.** The TSE dictionary describes the field as "voters with registered biometrics who were not enabled by means of them". It is not the total of manual releases: those without registered biometrics are not included, and the denominator (voters with biometrics) is not available.

**Points of attention in the data:**

- TSE CKAN catalog: the two RR/T2/2026 resources point to the `.sha512`. The zip exists at `.../buweb/bweb_2t_RR_261020260742.zip` (HTTP 200) and was downloaded directly, with hash verified.
- The `DT_ABERTURA`, `DT_ENCERRAMENTO`, `DT_EMISSAO_BU` times are the voting machine's local clock (Acre opens at 06:00 and closes at 15:00). The closing delay uses the municipality's nominal time (mode of opening + 9 h). `DT_BU_RECEBIDO` is the TSE server time.
- Sections "Não instalada" (not installed), "Não apurada" (not counted), and "Anulada e apurada em separado" (voided and counted separately) carry `#NULO#` or -1 in the votable and biometrics fields. They are handled only in that exact case and stay out of the analyses (only "Apurada" (counted) voting machines, abroad excluded, unless otherwise indicated).
- In 2022, the UE2009 and UE2010 voting machines in Espírito Santo record a manual rate of exactly 0,0 (3.339 sections), while the same machines in other states have about 15%. This is a measurement artifact and explains the only state where the rate rose from 2022 to 2026.
- Versions: Python 3.12, pandas 3.1, scipy 1.18, pyarrow, matplotlib 3.11. Script hashes (SHA-256, first 16 characters): `01_prepara_bweb.py` dff9e63cf4b464f0; `01b_locais.py` 8becc04f2c1181bb; `01c_modelo_urna.py` 42745848343abc57; `02_executa.py` 88170a7d1413ff7a; `03_monta_dossie.py` 79d7b25ca185e76f; `03b_monta_fase2.py` b9759ac59c6f41fc; `03c_relatorio_original.py` cd6fc61424af0a14; `03d_alegacoes_residuos.py` 6e77253c9e9c16a1; `03e_paginas_finais.py` 0b98d4cce9b44457; `03f_paginas_a18_a19.py` ae003807fc79e499; `04_cruza_bu_impresso.py` c2fa12f3f5121b29; `05_extras_bweb.py` e8848c083265d890; `06_ordem_totalizacao.py` 9ff1bd0374c8d640; `07_perfil_agrega.py` f006fede9732dc6f; `08_arquivos_urna.py` 409c69a428c2bd6a; `09_amostra_urna.py` 7a71f4b221af0926; `10_figuras.py` 229dd164a20f7b12; `11_alegacoes_relatorio.py` 2abce2f1302b1b37; `12_candidatos_t1.py` d80be156b3d58791; `13_cert_urna.py` 44e708e9d71f5928; `14_poder_estatistico.py` 15aa579512568d93; `15_aplica_autoria.py` dea5193cb7cc8c98; `16_a1_t1_janela.py` 85ab8db2b4765da1; `build_site.py` 8e100dd52380393f; `f2_a11_a15.py` 565f08129358405e; `f2_a18.py` 1d94b201f4201ae8; `f2_a1_a3.py` adc5d4bb98d067bf; `f2_a4_a5.py` 5ce1fb27909924ec; `f2_a6_a10.py` 8525031d689c582b; `f2_posregistro.py` e552f42bc8df9775; `h1_h4.py` 6a505af697305755; `h5_h8.py` 19e7a158411206f7; `h9_h10.py` 97a07ba144207967; `lib_auditoria.py` abda03c1384bdabd; `urna_parse.py` 37fee987face98d5.

## 3. Results by hypothesis

Common method: regression with polling-place fixed effects (`uf_local`), standard error clustered by place, the section's own T1 vote as control when the outcome is T2, and comparison with **each** placebo (2022/T1, 2022/T2, 2026/T1, or the equivalent defined in the test) by intersection-union test. The "excess" p is one-sided (2026/T2 greater than the placebo, in the direction of the allegation) and is the p corrected by Holm and Benjamini-Hochberg over the 23 registered tests. The ceiling in votes is `2 x max(0, difference + 1,645 x se) x exposure`: the maximum margin votes the phenomenon could explain, assuming causality. "Most demanding placebo" is the one with the largest estimate; "worst case" uses the loosest placebo.

Verdict rule (Addendum 2 of the pre-registration): **excess detected and relevant** = Holm < 0,05 and worst case >= 1% of the margin; **detectable excess, irrelevant magnitude** = Holm < 0,05 and < 1%; **refuted** = Holm >= 0,05 and < 1%; **inconclusive** = Holm >= 0,05 and >= 1%.

### 3.1 Synthesis

| H | Prediction if there is a deviation | Prediction if there is not | Result | Placebo | Max effect (margin votes) | % of margin | p Holm | Verdict |
|---|---|---|---|---|---|---|---|---|
| H1 manual x Lula vote (T2, with T1) | coef. > 0 and > placebos, increasing dose-response | same magnitude in placebos | 0,0020 (se 0,0010) | 2022/T2: 0,0162 | 0 | 0,00% | 1,000 | refuted |
| H1 without T1 control | idem | idem | 2026/T2: 0,0696; 2026/T1: 0,0741 | 2026/T1: 0,0741 (2022: -0,0054 and 0,0137) | 19.670 (vs T1/2026); 1.337.198 (vs 2022/T1) | 0,44%; 30,18% | 1,000 | inconclusive by the criterion, but the association is the same in T1 (see 3.2) |
| H1 symmetric: Flávio votes/eligible voter | no effect | no effect | 0,0090 (se 0,0009) | 2022/T2: -0,0005 | 122.543 | 2,77% | 0,000 | excess detected, **direction favorable to Flávio** |
| H2 "increase" in manual voter release | rate rises 2022 to 2026 | rate stable or falling | 10.011.347 in 2022/T2 and 8.632.488 in 2026/T2 | n/a | n/a | n/a | n/a | refuted (13,8% drop) |
| H2 vote change x manual change, within year | coef. > 0 only in 2026 | equal to 2022 | -0,0025 | 2022: -0,0006 | 1.794 | 0,04% | 1,000 | refuted |
| H2 between years (T2 against T1) | coef. T2 > T1 | equal | T2: -0,0004; T1: -0,0110 | T1 (imperfect placebo: different candidates) | 38.394 | 0,87% | 0,000 | detectable excess, irrelevant magnitude |
| H3 closing | report's table not reproduced or mass late closing | reproduced; nearly everything closes at 5pm-5:15pm | 5:01pm-5:15pm: 339.593 (report: 339.593); >= 7pm: 6.342 | 2022/T2: 274.561 and 20 | votes after 5pm: not measurable | n/a | n/a | characterization; report's count confirmed |
| H4 late closing (15, 60, 115 min), 6 tests | Lula% higher than in the same sections in 2022 and in T1 | equal | from -0,10 to -0,03 p.p. | from -0,09 to 0,02 p.p. | up to 8.262 | up to 0,19% | 1,00 to 1,00 | refuted |
| H5 turnout >= 95% | mostly old, high manual, T2 only | new, small, atypical place, already in T1 | observed 639; expected by composition 259 | 2026/T1: 559 against 293 | 19.023 | 0,43% | 0,177 | refuted as a T2 effect; elevated 2026 level with no identified cause |
| H6 new sections | diverge from old ones of the same place | equal | +0,54 p.p. | 2022: 0,00; 2018: +1,34 | 92.023 (vs 2022); 0 (vs 2018) | 2,08% | 1,000 | inconclusive (depends on the baseline) |
| H7 local outliers pro-Lula (adjusted z in absolute value > 3) | excess without mirror | count equal to 2022 and symmetric | 44,8 per 10 thousand sections; 63,3% of outliers are pro-Lula | 2022/T1: 47,6; 64,5% | 20.301 | 0,46% | 1,000 | refuted |
| H8 digits | last digit non-uniform; excess exact integer percentages | uniform, as in 2022 | see 3.8 | 2022 and 2026/T1 | n/a (shape test) | n/a | 1,000 | no excess |
| H9 consistency | sum of sections differs from tabulation | equal | 1 section (66 votes, 2018/T1) and 0 zones with difference | n/a | 0 in 2026 | 0% | n/a | consistent in 2026; 1 discrepancy in `votacao_secao` of 2018/T1 |
| H10 aggregate impact | sum of excesses comparable to 4.430.191 | sum < 1% | pro-Lula 38.394; pro-Flávio 122.543 | n/a | see 3.10 | 0,87% | n/a | below 1% in the pro-Lula direction |
| Printed poll-receipts | discrepancy of any size | none | **not executed** | n/a | n/a | n/a | n/a | no input (see 3.11) |

### 3.2 H1: manual voter release x vote

Polling-place fixed effects, error clustered by place; coefficients in fraction of valid votes per unit of manual rate.

| spec | year | round | coef | se | n | places |
|---|---|---|---|---|---|---|
| S0 without lag | 2022 | 1 | -0,0054 | 0,0016 | 447.222 | 68.579 |
| S0 without lag | 2022 | 2 | 0,0137 | 0,0017 | 447.223 | 68.578 |
| S0 without lag | 2026 | 1 | 0,0741 | 0,0025 | 475.790 | 72.441 |
| S0 without lag | 2026 | 2 | 0,0696 | 0,0024 | 475.789 | 72.441 |
| S1 T2 with T1 lag | 2022 | 2 | 0,0162 | 0,0008 | 447.220 | 68.578 |
| S1 T2 with T1 lag | 2026 | 2 | 0,0020 | 0,0010 | 475.784 | 72.439 |

Reading: without T1 control, the 2026 association (0,074 in T1 and 0,070 in T2) is the same in both rounds and larger than 2022's (-0,005 and 0,014). Conditioning on the section's own T1 vote, the T2 coefficient falls to 0,002, below 2022 (0,016). That is, the relationship exists before the runoff and the runoff adds nothing. Controls for turnout and section size (0,067) and for voting machine model (see 3.12) do not dissolve it; the cause of this 2026 association was not identified.

**Dose-response** (manual-rate bands against 0-5%, percentage points of Lula vote, T2 with T1):

| year | band | coef_pp | se_pp | sections_in_band |
|---|---|---|---|---|
| 2022 | 5-10% | 0,086 | 0,008 | 153.587 |
| 2022 | 10-20% | 0,205 | 0,011 | 114.869 |
| 2022 | 20-50% | 0,340 | 0,019 | 28.566 |
| 2022 | >50% | 0,174 | 0,127 | 321 |
| 2026 | 5-10% | 0,005 | 0,007 | 238.172 |
| 2026 | 10-20% | 0,023 | 0,011 | 81.180 |
| 2026 | 20-50% | -0,023 | 0,042 | 4.046 |
| 2026 | >50% | -0,031 | 0,184 | 97 |

In 2022 the curve rises with the rate; in 2026 it is flat.

**Symmetry.** In 2026, the manual rate predicts more votes per eligible voter in T2 for both candidates (Lula 0,019, Flávio 0,009), while in 2022 only Lula (0,027 against -0,001 for Bolsonaro). Lula's coefficient fell and Flávio's rose. In Flávio strongholds (Lula T1 < 40%) the coefficient is -0,0049 and in Lula's (T1 > 60%), 0,0099, both without excess over 2022.

### 3.3 H2: the increase in manual voter release

| year | round | biom_nh_total | turnout_total | aggregate_rate | sections |
|---|---|---|---|---|---|
| 2018 | 1 | 8.166.806 | 117.364.560 | 6,96% | 454.490 |
| 2018 | 2 | 7.898.943 | 115.933.451 | 6,81% | 454.490 |
| 2022 | 1 | 10.780.979 | 123.682.372 | 8,72% | 472.028 |
| 2022 | 2 | 10.011.347 | 124.252.796 | 8,06% | 472.028 |
| 2026 | 1 | 8.342.249 | 125.275.835 | 6,66% | 499.206 |
| 2026 | 2 | 8.632.488 | 128.236.074 | 6,73% | 499.205 |

The 2026/T2 total (8.632.488) is the "8.6 million" of the report. In stable sections (eligible voters between 0,85x and 1,15x of 2022), 22,6% of sections had a drop of more than 5 p.p. in the rate and 8,6% had a rise. The filter "municipalities with biometrics in both years" barely changes the result.

The drop tracks the replacement of the voting machine fleet: in 2022, UE2009 and UE2010 had rates of 14% to 16% and UE2020, 5%; in 2026 the UE2009/2010/2011 left and the UE2022 entered, with 6%.

| year | CD_MODELO_URNA | sections | manual_rate | lula_sh |
|---|---|---|---|---|
| 2022 | -1 | 3.585 | 13,67% | 58,8% |
| 2022 | 2009 | 46.161 | 14,25% | 51,8% |
| 2022 | 2010 | 92.786 | 14,40% | 54,7% |
| 2022 | 2011 | 26.433 | 8,58% | 54,8% |
| 2022 | 2013 | 24.296 | 8,74% | 52,3% |
| 2022 | 2015 | 85.164 | 7,16% | 52,4% |
| 2022 | 2020 | 192.462 | 4,54% | 49,2% |
| 2026 | 2013 | 11.423 | 11,01% | 53,7% |
| 2026 | 2015 | 87.184 | 9,78% | 52,2% |
| 2026 | 2020 | 200.448 | 6,15% | 52,1% |
| 2026 | 2022 | 198.686 | 6,15% | 52,0% |

**Where it rose.** Only Espírito Santo (2,69 p.p.), due to a 2022 measurement artifact (section 2). Within ES, the vote change is not associated with the rate change (coefficient 0,0001, standard error 0,008). Largest drops: AL (-4,24 p.p.), RO (-3,85 p.p.), RN (-3,46 p.p.), AP (-3,22 p.p.).

### 3.4 H3: closing

**Recount of the report's table** (raw clock of `DT_ENCERRAMENTO`, without timezone adjustment, with abroad):

| year | round | before_5:01pm | from_5:01pm_to_5:15pm | from_5:16pm_to_6:59pm | at_or_after_7pm | total |
|---|---|---|---|---|---|---|
| 2018 | 1 | 84.349 | 275.592 | 87.851 | 6.508 | 454.300 |
| 2018 | 2 | 205.558 | 247.744 | 1.014 | 34 | 454.350 |
| 2022 | 1 | 88.485 | 252.498 | 119.360 | 11.565 | 471.908 |
| 2022 | 2 | 195.818 | 274.561 | 1.585 | 20 | 471.984 |
| 2026 | 1 | 70.057 | 311.284 | 109.891 | 7.944 | 499.176 |
| 2026 | 2 | 150.771 | 339.593 | 2.472 | 6.342 | 499.178 |

The report's value for 5:01pm-5:15pm (339.593) is reproduced exactly in 2026/T2. The equivalent band has 274.561 sections in 2022/T2 and 247.744 in 2018/T2, and corresponds to a normal queue at closing time. The raw clock ignores the timezone: the western states close at 3pm or 4pm local and fall into "before 5:01pm". With nominal time by municipality, 98,2% of sections (without abroad) close up to 15 minutes after the time.

**Extension.** 6.714 sections (without abroad; 1,35%) closed 115 minutes or more after the nominal time, with 1.970.400 voters with recorded turnout, versus 25 sections in 2022/T2. States: RJ 2.981, SP 1.649, BA 973, PE 691, PB 309, SE 53. In RJ this is 7,9% of the state's sections.

**Votes after 5pm.** The BWeb does not carry a voting log; the "Gedai logs" of the catalog are from voting machine preparation (generated on 10/24), not from voting. For this reason the number is not measurable here. The external reference of 34.330 voters (press survey) was not verified. The limit by extrapolation of the section's average rate (`h3_votos_apos_horario_limite.csv`) is a loose ceiling and should not be read as an estimate.

**BU receipt time at the TSE.** 99,6% of 2026/T2 BUs arrived after 7pm, but 98,2% of sections had closed up to 15 minutes after the nominal time. The receipt time reflects the TSE holding back receipt, not the section's closing. The previous reading of this analysis, which used that time as a proxy for closing, was wrong.

### 3.5 H4: sections that closed late

Lula% (percentage points) in late sections against the others of the same place, T2/2026 with T1 as control, and the same test in the same sections in 2022/T2 and in T1/2026:

| L | spec | coef_pp | se_pp | late_sections |
|---|---|---|---|---|
| 15 | 2026 T2 w/ lag | -0,050 | 0,037 | 8.373 |
| 15 | placebo 2022 T2 w/ lag (same sections) | 0,005 | 0,035 | 8.373 |
| 15 | 2026 T2 w/o lag | -0,030 | 0,073 | 8.373 |
| 15 | placebo T1/2026 w/o lag (same sections) | 0,025 | 0,079 | 8.373 |
| 15 | 2026 T2 w/ lag, zone FE | -0,061 | 0,032 | 8.373 |
| 60 | 2026 T2 w/ lag | -0,025 | 0,049 | 6.608 |
| 60 | placebo 2022 T2 w/ lag (same sections) | -0,024 | 0,045 | 6.608 |
| 60 | 2026 T2 w/o lag | -0,071 | 0,099 | 6.608 |
| 60 | placebo T1/2026 w/o lag (same sections) | -0,056 | 0,104 | 6.608 |
| 60 | 2026 T2 w/ lag, zone FE | -0,080 | 0,039 | 6.608 |
| 115 | 2026 T2 w/ lag | -0,028 | 0,051 | 6.268 |
| 115 | placebo 2022 T2 w/ lag (same sections) | -0,023 | 0,046 | 6.268 |
| 115 | 2026 T2 w/o lag | -0,101 | 0,101 | 6.268 |
| 115 | placebo T1/2026 w/o lag (same sections) | -0,090 | 0,105 | 6.268 |
| 115 | 2026 T2 w/ lag, zone FE | -0,091 | 0,040 | 6.268 |

No 2026 estimate exceeds those of 2022 or of T1. With zone fixed effects (less strict comparison), the coefficients are negative (from -0,06 to -0,09 p.p.): closing late is not associated with more Lula votes. Context: in T1/2026, sections with a delay of 15 minutes or more have +0,58 p.p. of Lula within the same place (queue in larger sections), an effect that does not appear in T2 (-0,03 p.p.).

### 3.6 H5: sections with turnout >= 95% and Klimek

| year | round | sections | turnout_ge95 | per_100k | ge95_PT90 | ge95_OPO90 | M5a_PT | M5a_OPO | M5b_PT | M5b_OPO |
|---|---|---|---|---|---|---|---|---|---|---|
| 2014 | 1 | 427.937 | 2.232 | 521,6 | 433 | 6 | 0,00767 | 0,00039 | -0,0244 | 0,0244 |
| 2014 | 2 | 427.938 | 1.036 | 242,1 | 74 | 2 | 0,00123 | 0,00012 | -0,0016 | 0,0016 |
| 2018 | 1 | 453.702 | 959 | 211,4 | 161 | 118 | 0,00319 | 0,00427 | -0,0725 | 0,0725 |
| 2018 | 2 | 453.703 | 503 | 110,9 | 62 | 38 | 0,00172 | 0,00048 | -0,0209 | 0,0209 |
| 2022 | 1 | 471.010 | 262 | 55,6 | 60 | 4 | 0,00128 | 0,00008 | -0,0398 | 0,0398 |
| 2022 | 2 | 471.010 | 232 | 49,3 | 44 | 7 | 0,00090 | 0,00013 | -0,0267 | 0,0267 |
| 2026 | 1 | 497.897 | 559 | 112,3 | 86 | 7 | 0,00114 | 0,00021 | -0,0357 | 0,0357 |
| 2026 | 2 | 497.897 | 639 | 128,3 | 117 | 9 | 0,00152 | 0,00018 | -0,0241 | 0,0241 |

`por_100k` is M5c; M5a is the fraction of sections with turnout >= 90% and vote >= 90% for the candidate; M5b is the turnout x vote correlation within the place. Klimek figures: `results/fase1/figs/klimek_T2.png` and `klimek_T1.png`; on visual inspection, 2026 shows no second mode on the diagonal (the pattern the literature associates with manipulation) and the shape is similar to 2022's. Visual inspection is not a test; the tests are M5a to M5c above.

**The 639 sections of 2026/T2.** 66,8% are new (no pair in 2022), against 7,6% of all sections; median of 161 eligible voters against 327; average manual rate of 7,9% against 6,9%; average closing delay of 4,0 against 4,1 minutes. Average turnout in T1: 94,4%; only 35 sections went from < 90% in T1 to >= 95% in T2, with 5.737 valid votes. By place type (place name):

| type | n_ge95 | n_total | pct_ge95_within_type | pct_of_total_ge95 | pct_of_total_sections |
|---|---|---|---|---|---|
| escola_outro | 554 | 490.606 | 0,11% | 86,7% | 98,54% |
| hospital_asilo | 0 | 113 | 0,00% | 0,0% | 0,02% |
| indigena | 32 | 838 | 3,82% | 5,0% | 0,17% |
| militar | 0 | 52 | 0,00% | 0,0% | 0,01% |
| prisional | 6 | 187 | 3,21% | 0,9% | 0,04% |
| quilombola | 4 | 227 | 1,76% | 0,6% | 0,05% |
| rural_comunidade | 43 | 5.874 | 0,73% | 6,7% | 1,18% |

**Standardization.** With 2022 rates by place type and size, 259 sections >= 95% were expected in T2 (293 in T1); 639 and 559 observed, ratios of 2,47 and 1,91. Composition does not explain the 2026 level, and the excess already exists in T1. The T2 minus T1 difference (log of the ratio, 0,258) gives a one-sided p of 0,0084 and 0,177 after Holm; ceiling 19.023 votes (0,43%).

**Rate of sections >= 95% per 10 thousand sections, by size** (eligible voters):

| size | round | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|
| 151-300 | 1 | 82,5 | 32,6 | 5,9 | 10,8 |
| 151-300 | 2 | 36,7 | 15,4 | 5,3 | 15,1 |
| 51-150 | 1 | 335,1 | 238,6 | 163,5 | 390,4 |
| 51-150 | 2 | 201,7 | 144,4 | 139,8 | 351,4 |
| <=50 | 1 | 886,5 | 850,5 | 500,0 | 846,1 |
| <=50 | 2 | 638,3 | 459,2 | 335,2 | 766,3 |
| >300 | 1 | 27,8 | 5,1 | 1,4 | 1,4 |
| >300 | 2 | 11,0 | 2,5 | 1,4 | 2,8 |

The 2026 level in sections of 51 to 150 eligible voters exceeds that of all previous years in both rounds; in sections of more than 150 eligible voters, 2014 had a higher rate. Among the 200 old paired sections with >= 95% in 2026, eligible voters stayed stable (1,01x the 2022 median), turnout rose 6,1%, and the 2022 median turnout was already 92,1%: the effect comes from the numerator, not from a drop in eligible voters.

### 3.7 H6: new sections

| year | spec | coef | se | p | new_sections | n |
|---|---|---|---|---|---|---|
| 2026 | lula_sh T2 / lula_sh T1 | 0,00536 | 0,00017 | 0,0000 | 37.513 | 475.784 |
| 2026 | turnout T2 / turnout T1 | -0,00652 | 0,00018 | 0,0000 | 37.513 | 475.784 |
| 2026 | lula_sh T1 (no lag) | 0,01409 | 0,00042 | 0,0000 | 37.513 | 475.784 |
| 2026 | turnout T1 (no lag) | 0,00448 | 0,00046 | 0,0000 | 37.513 | 475.784 |
| 2022 | lula_sh T2 / lula_sh T1 | 0,00004 | 0,00015 | 0,7811 | 33.757 | 447.220 |
| 2022 | turnout T2 / turnout T1 | -0,00129 | 0,00016 | 0,0000 | 33.757 | 447.220 |
| 2022 | lula_sh T1 (no lag) | 0,01717 | 0,00043 | 0,0000 | 33.757 | 447.220 |
| 2022 | turnout T1 (no lag) | 0,01618 | 0,00040 | 0,0000 | 33.757 | 447.220 |
| 2018 | lula_sh T2 / lula_sh T1 | 0,01344 | 0,00027 | 0,0000 | 103.372 | 426.397 |
| 2018 | turnout T2 / turnout T1 | -0,00291 | 0,00018 | 0,0000 | 103.372 | 426.397 |
| 2018 | lula_sh T1 (no lag) | 0,00160 | 0,00041 | 0,0001 | 103.372 | 426.397 |
| 2018 | turnout T1 (no lag) | 0,00537 | 0,00047 | 0,0000 | 103.372 | 426.397 |

Robustness of the `nova` (new) coefficient in Lula% T2 given T1 (interaction with centered T1, size and turnout controls, only sections of 100 to 500 eligible voters):

| year | variant | coef_nova | se | new_sections |
|---|---|---|---|---|
| 2026 | interaction new x T1 (effect at mean T1) | 0,00580 | 0,00017 | 37.513 |
| 2026 | controls log eligible voters and T1 turnout | 0,00528 | 0,00017 | 37.513 |
| 2026 | only sections of 100 to 500 eligible voters | 0,00540 | 0,00016 | 36.203 |
| 2022 | interaction new x T1 (effect at mean T1) | 0,00011 | 0,00015 | 33.757 |
| 2022 | controls log eligible voters and T1 turnout | 0,00005 | 0,00015 | 33.757 |
| 2022 | only sections of 100 to 500 eligible voters | 0,00000 | 0,00015 | 32.587 |
| 2018 | interaction new x T1 (effect at mean T1) | 0,01345 | 0,00027 | 103.372 |
| 2018 | controls log eligible voters and T1 turnout | 0,01410 | 0,00027 | 103.372 |
| 2018 | only sections of 100 to 500 eligible voters | 0,01356 | 0,00027 | 101.230 |

The 2026 effect (+0,5 p.p.) is stable across the three variants, i.e., it is not an artifact of heterogeneous slope nor of size. In 2022 the coefficient is zero and in 2018 it is +1,3 p.p., larger than 2026's. Against the most demanding placebo (2018) there is no excess; against 2022, the worst-case ceiling is 2,08% of the margin. Verdict: inconclusive, because it depends on which year serves as the baseline. The cause was not identified (composition by age and income is not available by section).

### 3.8 H7 and H8: local outliers and digits

| year | round | sections_in_places_ge4 | overdispersion_phi | up_3 | down_3 | rate_up_10k | rate_down_10k | up_down_ratio |
|---|---|---|---|---|---|---|---|---|
| 2014 | 1 | 345.046 | 1,551 | 1.022 | 1.127 | 29,6 | 32,7 | 0,91 |
| 2014 | 2 | 345.914 | 1,545 | 1.117 | 1.044 | 32,3 | 30,2 | 1,07 |
| 2018 | 1 | 374.992 | 1,550 | 1.366 | 847 | 36,4 | 22,6 | 1,61 |
| 2018 | 2 | 375.480 | 1,587 | 1.947 | 912 | 51,9 | 24,3 | 2,13 |
| 2022 | 1 | 396.419 | 1,536 | 1.886 | 1.040 | 47,6 | 26,2 | 1,81 |
| 2022 | 2 | 396.442 | 1,535 | 1.805 | 1.008 | 45,5 | 25,4 | 1,79 |
| 2026 | 1 | 423.321 | 1,551 | 1.697 | 1.071 | 40,1 | 25,3 | 1,58 |
| 2026 | 2 | 423.316 | 1,545 | 1.895 | 1.100 | 44,8 | 26,0 | 1,72 |

Outlier = section whose Lula vote diverges from the mean of the other sections of the same place (leave-one-out), with binomial variance and overdispersion estimated in each election (phi ≈ 1,5 in all). `up` is pro-Lula and `down`, pro-Flávio/opponent.

| year | round | cand | n | chi2 | p | V_cramer |
|---|---|---|---|---|---|---|
| 2014 | 1 | PT | 423.225 | 19,6 | 0,0208 | 0,00227 |
| 2014 | 1 | OPO | 380.553 | 156,4 | 0,0000 | 0,00676 |
| 2014 | 2 | PT | 426.168 | 8,8 | 0,4525 | 0,00152 |
| 2014 | 2 | OPO | 412.167 | 51,0 | 0,0000 | 0,00371 |
| 2018 | 1 | PT | 412.867 | 520,9 | 0,0000 | 0,01184 |
| 2018 | 1 | OPO | 426.922 | 108,6 | 0,0000 | 0,00532 |
| 2018 | 2 | PT | 450.305 | 13,2 | 0,1547 | 0,00180 |
| 2018 | 2 | OPO | 435.489 | 26,2 | 0,0019 | 0,00259 |
| 2022 | 1 | PT | 470.188 | 15,8 | 0,0704 | 0,00193 |
| 2022 | 1 | OPO | 456.501 | 47,5 | 0,0000 | 0,00340 |
| 2022 | 2 | PT | 470.245 | 12,3 | 0,1989 | 0,00170 |
| 2022 | 2 | OPO | 459.874 | 33,6 | 0,0001 | 0,00285 |
| 2026 | 1 | PT | 496.219 | 8,9 | 0,4445 | 0,00141 |
| 2026 | 1 | OPO | 489.405 | 18,8 | 0,0269 | 0,00207 |
| 2026 | 2 | PT | 496.878 | 4,2 | 0,8996 | 0,00097 |
| 2026 | 2 | OPO | 489.412 | 19,3 | 0,0225 | 0,00210 |

Last digit of the counts (>= 20 votes), Cramér's V. Exact integer percentage (identical for both candidates):

| year | round | observed | expected | ratio |
|---|---|---|---|---|
| 2014 | 1 | 12.468 | 15.998 | 0,779 |
| 2014 | 2 | 9.212 | 11.930 | 0,772 |
| 2018 | 1 | 13.148 | 17.343 | 0,758 |
| 2018 | 2 | 10.110 | 13.196 | 0,766 |
| 2022 | 1 | 10.449 | 13.422 | 0,779 |
| 2022 | 2 | 9.848 | 12.455 | 0,791 |
| 2026 | 1 | 11.224 | 14.588 | 0,769 |
| 2026 | 2 | 10.239 | 13.134 | 0,780 |

Lula's last digit in 2026/T2 is uniform (p = 0,90). The opponent's has V of 0,0021 (p = 0,022), smaller than in 2014, 2018 and 2022; p without correction for multiple testing. The integer percentage stays at 0,78 of expected in all years (the expected formula overestimates, but the ratio is constant).

### 3.9 H9: consistency

| year | round | sections_bweb | sections_votacao_secao | paired | paired_with_difference | sum_abs_vote_diff |
|---|---|---|---|---|---|---|
| 2014 | 1 | 428.853 | 428.850 | 428.850 | 0 | 0 |
| 2014 | 2 | 428.854 | 428.852 | 428.852 | 0 | 0 |
| 2018 | 1 | 454.446 | 454.445 | 454.445 | 1 | 66 |
| 2018 | 2 | 454.447 | 454.447 | 454.447 | 0 | 0 |
| 2022 | 1 | 472.024 | 472.024 | 472.024 | 0 | 0 |
| 2022 | 2 | 472.027 | 472.027 | 472.027 | 0 | 0 |
| 2026 | 1 | 499.206 | 499.206 | 499.206 | 0 | 0 |
| 2026 | 2 | 499.205 | 499.205 | 499.205 | 0 | 0 |


| round | zones_bweb | zones_munzona | bweb_only | munzona_only | paired | with_difference | sum_abs_vote_diff | lula_bweb | lula_munzona | flavio_bweb | flavio_munzona |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6.251 | 6.292 | 0 | 41 | 6.251 | 0 | 0 | 53.879.538 | 53.879.538 | 56.104.503 | 56.104.503 |
| 2 | 6.250 | 6.292 | 0 | 42 | 6.250 | 0 | 0 | 64.256.232 | 64.256.232 | 59.826.041 | 59.826.041 |

**Discrepancies by section** (all BWeb x `votacao_secao` comparisons):

| year | round | uf | cd_municipio | zone | section | turnout_bweb | nominal_bweb | lula_bweb | lula_votacao_secao | opponent_bweb | opponent_votacao_secao | sum_candidates_votacao_secao |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 1 | MA | 8591 | 17 | 25 | 70 | 65 | 45 | 91 | 15 | 35 | 126 |

The only discrepancy is from 2018/T1, in section 25 of zone 17 of municipality 8591 (MA): the BWeb records 45 and 15 votes for the two candidates, with turnout of 70 and 65 nominal votes; `votacao_secao` records 91 and 35, sum 126, greater than the section's turnout. The national totals published by the TSE for 2018/T1 (Haddad 31.342.005, Bolsonaro 49.276.990, turnout 117.364.560; [source](https://www.tse.jus.br/comunicacao/noticias/2018/Outubro/concluida-totalizacao-de-votos-do-1o-turno-das-eleicoes-2018)) match the BWeb (BWeb total turnout: 117.364.560), and `votacao_secao` is 46 and 20 votes above. Therefore the difference is in `votacao_secao` (a product generated in 2021), not in the tabulation published in 2018. The cause was not investigated. It does not involve 2026. Sections present only in the BWeb and with no vote for either candidate: 2014: 5 (up to 8 turnouts); 2018: 1 (up to 4 turnouts).

The 2026 municipality/zone tabulation has 41 (T1) and 42 (T2) zones with no counted section in the BWeb; the Lula and Flávio totals are identical, so those zones add up to zero votes for both. Internal consistency of the BUs (turnout <= eligible voters, nominal + blank + null = turnout, valid <= turnout, one voting machine per section): 0 violations in all elections. This check shows that the TSE products are coherent with each other; it does not prove the integrity of the source (if a BU were altered at the origin, all products would reflect it).

### 3.10 H10: aggregate impact

| direction | n_tests_with_votes | n_survivors | sum_survivor_votes_demanding (margin votes) | sum_survivor_votes_worst_case (worst-case ceiling, margin votes) | max_individual_worst_case (worst-case ceiling, margin votes) | sum_of_all_demanding (margin votes) | pct_margin_survivors_worst_case | pct_margin_sum_all_demanding |
|---|---|---|---|---|---|---|---|---|
| PT | 19 | 1 | 38.394 | 38.394 | 1.337.198 | 213.777 | 0,87 | 4,83 |
| OPO | 1 | 1 | 122.543 | 122.543 | 122.543 | 122.543 | 2,77 | 2,77 |

Survivors (Holm < 0,05):

| H | test | direction | p_holm | max_margin_votes (margin votes) | max_votes_worst_case (worst-case ceiling, margin votes) | pct_worst_case | verdict |
|---|---|---|---|---|---|---|---|
| H1 | S1 Flavio/Bolsonaro votes/eligible voter | OPO | 0,000 | 122.543 | 122.543 | 2,77% | EXCESS DETECTED and relevant (worst case >= 1% of margin) |
| H2 | delta Lula vote (2022->2026) ~ delta manual rate, T2 | PT | 0,000 | 38.394 | 38.394 | 0,87% | detectable excess, irrelevant magnitude (<1% of margin) |

The ceilings use the same sections and are not independently additive; the "sum of all" and "individual maximum" columns are redundant and loose ceilings (the individual maximum comes from H1 without T1 control, compared with 2022/T1, where the association was negative). The pro-Lula and pro-Flávio directions do not offset each other. The sum of survivors in the pro-Lula direction is 38.394 votes (0,87% of the margin).

### 3.11 Direct test with printed poll-receipts

**Not executed.** No BU PDF or image was provided (Downloads and the project directory were checked; screenshots in Pictures were not opened). `scripts/04_cruza_bu_impresso.py` is ready: it takes a spreadsheet with zone, section, round and the BU totals (transcribed or read from the QR code) and reports any discrepancy, of eligible voters, turnout, votes, blank, null, opening and closing. Self-test: with 3 real sections, 0 discrepancies; with 1 altered vote, 1 discrepancy detected. There is no QR code reading from images; for photos, one must transcribe or decode the QR beforehand.

### 3.12 Red team: mundane explanations tested

| test | year | round | coef_manual | se |
|---|---|---|---|---|
| S0 + voting machine model dummies | 2022 | 1 | -0,00583 | 0,00166 |
| S0 + voting machine model dummies | 2022 | 2 | 0,01451 | 0,00180 |
| S0 + voting machine model dummies | 2026 | 1 | 0,07386 | 0,00251 |
| S0 + voting machine model dummies | 2026 | 2 | 0,06929 | 0,00243 |
| S1 Lula votes/eligible voter (own lag only) | 2022 | 2 | 0,02671 | 0,00100 |
| S1 Lula votes/eligible voter + T1 of all candidates and blank/null | 2022 | 2 | 0,02504 | 0,00095 |
| S1 Flavio/Bolsonaro votes/eligible voter (own lag only) | 2022 | 2 | -0,00051 | 0,00075 |
| S1 Flavio/Bolsonaro votes/eligible voter + T1 of all candidates and blank/null | 2022 | 2 | -0,00009 | 0,00072 |
| S1 Lula votes/eligible voter (own lag only) | 2026 | 2 | 0,01915 | 0,00111 |
| S1 Lula votes/eligible voter + T1 of all candidates and blank/null | 2026 | 2 | 0,01717 | 0,00103 |
| S1 Flavio/Bolsonaro votes/eligible voter (own lag only) | 2026 | 2 | 0,00898 | 0,00095 |
| S1 Flavio/Bolsonaro votes/eligible voter + T1 of all candidates and blank/null | 2026 | 2 | 0,02041 | 0,00095 |
| turnout T2 ~ manual rate + turnout T1 | 2022 | 2 | 0,03090 | 0,00113 |
| turnout T2 ~ manual rate + turnout T1 | 2026 | 2 | 0,04434 | 0,00118 |

- **Voting machine model**: the manual rate varies from 4,5% to 14,4% between models in 2022/T2 (see 3.3), and the 2026 S0 association remains (0,069 with model dummies).
- **T1 composition** (votes of the other candidates, blank and null): Flávio's coefficient rises from 0,009 to 0,020; Lula's falls from 0,019 to 0,017. The hypothesis that the candidates eliminated in T1 explain the pro-Flávio pattern does not hold.
- **Turnout**: the manual rate predicts increased turnout in T2 given T1 in both years (2022: 0,031; 2026: 0,044), in line with the gain being split between the two candidates in 2026.

### 3.13 Historical yardstick (2014, 2018, 2022, 2026)

Predictions and "similar" criterion fixed in Addendum 1 of the pre-registration: ratio between 0,8 and 1,25 for rates and counts; difference < 0,02 for correlations (M5b) and < 0,005 for Cramér's V. Pattern A: 2014, 2022 and 2026 similar to each other and 2018 different from the three. B: 2014 similar to 2018, 2022 similar to 2026, the pairs different from each other. C: all four similar.

**Runoff:**

| metric | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|
| M5a_PT | 0,00123 | 0,00172 | 0,00090 | 0,00152 |
| M5a_OPO | 0,00012 | 0,00048 | 0,00013 | 0,00018 |
| M5c | 242,09114 | 110,86548 | 49,25585 | 128,33980 |
| M7a_up | 32,29126 | 51,85363 | 45,52999 | 44,76561 |
| M7a_down | 30,18091 | 24,28891 | 25,42617 | 25,98532 |
| M7b | 1,06992 | 2,13487 | 1,79067 | 1,72273 |
| M8b_PT | 0,77219 | 0,76611 | 0,79067 | 0,77957 |
| M8b_OPO | 0,77219 | 0,76611 | 0,79067 | 0,77957 |
| M5b_PT | -0,00156 | -0,02095 | -0,02672 | -0,02409 |
| M5b_OPO | 0,00156 | 0,02095 | 0,02672 | 0,02409 |
| M8a_V_PT | 0,00152 | 0,00180 | 0,00170 | 0,00097 |
| M8a_V_OPO | 0,00371 | 0,00259 | 0,00285 | 0,00210 |

Classification by metric (runoff):

| metric | A | B | C | none | sim_14_18 | sim_18_22 | sim_22_26 | sim_14_26 |
|---|---|---|---|---|---|---|---|---|
| M5a_PT | False | False | False | True | False | False | False | True |
| M5a_OPO | False | False | False | True | False | False | False | False |
| M5c | False | False | False | True | False | False | False | False |
| M7a_up | False | False | False | True | False | True | True | False |
| M7a_down | False | False | True | False | True | True | True | True |
| M7b | False | False | False | True | False | True | True | False |
| M8b_PT | False | False | True | False | True | True | True | True |
| M8b_OPO | False | False | True | False | True | True | True | True |
| M5b_PT | False | False | False | True | True | True | True | False |
| M5b_OPO | False | False | False | True | True | True | True | False |
| M8a_V_PT | False | False | True | False | True | True | True | True |
| M8a_V_OPO | False | False | True | False | True | True | True | True |

T2 summary: A = 0, B = 0, C = 5, none = 7 of 12 metrics. T1 summary: A = 3, B = 0, C = 3, none = 6.

**Trios of mutually similar years** (all three comparisons within the criterion), runoff:

| trio | mutually_similar_metrics | metrics_that_do_not_fit |
|---|---|---|
| 2014 + 2018 + 2022 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2018 + 2026 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2022 + 2026 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2018 + 2022 + 2026 | 9 of 12 | M5a_PT, M5a_OPO, M5c |

Note: `M5b_OPO` and `M8b_OPO` repeat `M5b_PT` and `M8b_PT` by construction (the two shares sum to 1), so the 12 rows have 10 independent metrics. Without the repetitions, C holds in 4 of 10, and 2/3 would be 7. The conclusion does not change.


**Verdict by the fixed criterion: none of the three patterns fits.** The 2/3-of-metrics threshold (8 of 12) is not reached by A, B or C (C reaches 5). The trio 2018, 2022 and 2026 is the most homogeneous in the table; the metrics in which it is not homogeneous are the tail ones (turnout >= 90% with vote >= 90%, and turnout >= 95%), which are precisely those of the residual described in 3.6. This reading by trios is a post-hoc analysis, not pre-registered. The M5c metric (sections with turnout >= 95%) has no monotonic pattern: 242 per 100 thousand sections in 2014, 111 in 2018, 49 in 2022 and 128 in 2026; 2022 is the series minimum and 2026 falls between 2018 and 2014.

The A/B/C classification depends on the fixed numeric criterion, which is arbitrary; that is why the ratios are in the table.

## 4. Residual anomalies that survived the controls

1. **Flávio votes per eligible voter x manual rate (H1).** Coefficient 0,0090 against -0,0005 in 2022; worst-case ceiling, not an estimate, 122.543 margin votes, 2,77% of the margin, **in the direction favorable to Flávio**. Tested and not explained by: T1 composition (the coefficient increases), T1 turnout level. Not tested: age and schooling profile by section (dataset not available by section).
2. **Change in Lula vote between years x change in manual rate (H2).** T2: -0,0004; T1 (placebo): -0,0110; statistically detectable difference, worst-case ceiling, not an estimate, 38.394 margin votes (0,87%). The 2026 T1 has different candidates from the 2022 T1, so the placebo is imperfect.
3. **Manual x Lula association of 2026 (H1, without T1 control).** 0,074 in T1 and 0,070 in T2, against -0,005 and 0,014 in 2022. Present before the runoff and unaltered by size, turnout and voting machine model. Cause not identified. It is not specific to the runoff, so it does not stem from anything exclusive to that day (the extension, for example). A cause common to both rounds, whether a characteristic of the sections or of the voting machine, whether of another nature, is not distinguishable with these data.
4. **Sections with turnout >= 95% (H5).** 639 in 2026/T2; 2,5 times the expectation by place-type and size composition; present in T1 (1,9 times). Tested: place type (indigenous, prison, hospital, quilombola, military, rural), size, new section, UF, manual rate, closing delay, "T2 only" (35 sections, 5.737 valid votes), numerator against denominator. No single factor eliminates the excess. Not tested: voter-registration cancellations and electorate review between 2022 and 2026 (no data). Effect ceiling: 0,43% of the margin.
5. **New sections (H6).** +0,54 p.p. of Lula in T2 given T1 (2018: +1,34; 2022: 0,00); robust to interaction, size and turnout. Worst-case ceiling 2,08%.

## 5. What the data cannot show

- **Uniform deviation in all voting machines.** All tests compare sections with each other (within the place, between years, between rounds). A bias equal in all sections vanishes in the differences.
- **Secret ballot.** There is no way to link a vote to a voter; only aggregates by section.
- **Party observers and party presence.** No variable measures the presence of party observers.
- **Votes after 5pm.** The BWeb has no voting log; only opening and closing time by section.
- **Source integrity.** BWeb, `votacao_secao` and the tabulation come from the same BU flow; coherence among them does not detect a BU altered at the origin. Only cross-checking with poll-receipts printed by party observers and parties does that, and it was not executed.
- **Total manual voter release.** The field measures only voters with registered biometrics not enabled by them, without a denominator.
- **Profile by section (age, schooling, income).** There is no by-section dataset; the electorate profile is by municipality and zone, which the place fixed effect already absorbs.
- **2014 and 2018.** 2014 has neither biometrics nor times; 2018 has neither receipt nor BU issuance time.
- **Section pairing between years.** It loses relocated sections; new and old sections behave differently (H6).

## 6. Reproducibility

Structure: `00_preregistro.md` (predictions and addenda), `scripts/`, `dados/` (hashes and URLs), `results/fase1/` (CSVs, figures, logs), `dossie.md`.

```bash
# 0. environment
python3 -m venv venv && venv/bin/pip install pandas numpy scipy pyarrow matplotlib

# 1. data (URLs in dados/urls_origem.txt; check SHA-512/SHA-1 of each zip against the TSE .sha512/.sha1 file)
#    BWeb 2022 and 2026 in bu/, 2014 and 2018 in bu_hist/; votacao_secao, detalhe and munzona in dados_tse/

# 2. preparation (one parquet per year x round)
venv/bin/python -I scripts/01_prepara_bweb.py bu parquet --anos 2022 2026
venv/bin/python -I scripts/01_prepara_bweb.py bu_hist parquet --anos 2014 2018
venv/bin/python -I scripts/01b_locais.py dados_tse parquet 2022 2026
venv/bin/python -I scripts/01c_modelo_urna.py dados_tse parquet 2022 2026

# 3. tests H1 to H10 and A/B/C (fixed order: H5, H7, H8 before ABC; H10 last)
venv/bin/python -I scripts/02_executa.py parquet resultados --anos 2014 2018 2022 2026 --zips dados_tse
#    exit code 2 = there are tests not executed (results/fase1/nao_executados.csv)

# 4. dossier
venv/bin/python -I scripts/03_monta_dossie.py resultados dados dossie.md

# 5. direct test with printed poll-receipts (when a spreadsheet is available)
venv/bin/python -I scripts/04_cruza_bu_impresso.py parquet entrada.csv divergencias.csv
```

Reprocessing 2022 and 2026 with the final version of the preparer reproduces the original parquets cell by cell, except 5 voided sections from abroad (sentinel -1 became empty), which do not enter the analyses. The test log of both runs is identical.

## Appendix A: full register of the 23 tests

| H | test | direction | est_2026T2 | demanding_comparator | b_comp | p_raw_2sided | p_excess | p_holm | p_bh | max_margin_votes (margin votes) | pct_margin | max_votes_worst_case (worst-case ceiling, margin votes) | pct_worst_case | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | S1 T2 with T1 lag, Lula% ~ manual rate | PT | 0,00195 | 2022/T2 | 0,01620 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTED (no excess, ceiling <1% of margin) |
| H1 | S0 no lag, Lula% ~ manual rate | PT | 0,06956 | 2026/T1 | 0,07413 | 0,1904 | 0,9048 | 1,000 | 1,000 | 19.670 | 0,444 | 1.337.198 | 30,184 | INCONCLUSIVE (no excess, but ceiling >=1% of margin) |
| H1 | S0 no lag + controls (turnout, log eligible voters) | PT | 0,06712 | 2026/T1 | 0,06712 | 0,9991 | 0,4995 | 1,000 | 1,000 | 96.014 | 2,167 | 1.328.747 | 29,993 | INCONCLUSIVE (no excess, but ceiling >=1% of margin) |
| H1 | S1 Flavio stronghold (Lula T1<40%) | PT | -0,00491 | 2022/T2 | 0,01392 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTED (no excess, ceiling <1% of margin) |
| H1 | S1 Lula stronghold (Lula T1>60%) | PT | 0,00995 | 2022/T2 | 0,01211 | 0,2889 | 0,8556 | 1,000 | 1,000 | 5.722 | 0,129 | 5.722 | 0,129 | REFUTED (no excess, ceiling <1% of margin) |
| H1 | S1 Lula votes/eligible voter | PT | 0,01915 | 2022/T2 | 0,02671 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTED (no excess, ceiling <1% of margin) |
| H1 | S1 Flavio/Bolsonaro votes/eligible voter | OPO | 0,00898 | 2022/T2 | -0,00051 | 0,0000 | 0,0000 | 0,000 | 0,000 | 122.543 | 2,766 | 122.543 | 2,766 | EXCESS DETECTED and relevant (worst case >= 1% of margin) |
| H1 | S1 dose: manual rate >= 20% vs <20% (Lula share) | PT | -0,00039 | 2022/T2 | 0,00163 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 0 | 0,000 | REFUTED (no excess, ceiling <1% of margin) |
| H2 | delta Lula vote (T1->T2) ~ delta manual rate, within year | PT | -0,00251 | 2022 (T1->T2) | -0,00064 | 0,2622 | 0,8689 | 1,000 | 1,000 | 1.794 | 0,040 | 1.794 | 0,040 | REFUTED (no excess, ceiling <1% of margin) |
| H2 | delta Lula vote (2022->2026) ~ delta manual rate, T2 | PT | -0,00044 | same test in T1 | -0,01103 | 0,0000 | 0,0000 | 0,000 | 0,000 | 38.394 | 0,867 | 38.394 | 0,867 | detectable excess, irrelevant magnitude (<1% of margin) |
| H4 | closes >= 15 min after 5pm: Lula% (w/ lag, place FE) | PT | -0,00050 | same sections in 2022/T2 | 0,00005 | 0,2797 | 0,8601 | 1,000 | 1,000 | 1.333 | 0,030 | 1.333 | 0,030 | REFUTED (no excess, ceiling <1% of margin) |
| H4 | closes >= 15 min after 5pm: Lula% (w/o lag, place FE) | PT | -0,00030 | same sections in T1/2026 | 0,00025 | 0,6143 | 0,6928 | 1,000 | 1,000 | 5.743 | 0,130 | 5.743 | 0,130 | REFUTED (no excess, ceiling <1% of margin) |
| H4 | closes >= 60 min after 5pm: Lula% (w/ lag, place FE) | PT | -0,00025 | same sections in 2022/T2 | -0,00024 | 0,9914 | 0,5043 | 1,000 | 1,000 | 4.055 | 0,092 | 4.055 | 0,092 | REFUTED (no excess, ceiling <1% of margin) |
| H4 | closes >= 60 min after 5pm: Lula% (w/o lag, place FE) | PT | -0,00071 | same sections in T1/2026 | -0,00056 | 0,9170 | 0,5415 | 1,000 | 1,000 | 8.262 | 0,186 | 8.262 | 0,186 | REFUTED (no excess, ceiling <1% of margin) |
| H4 | closes >= 115 min after 5pm: Lula% (w/ lag, place FE) | PT | -0,00028 | same sections in 2022/T2 | -0,00023 | 0,9453 | 0,5273 | 1,000 | 1,000 | 3.857 | 0,087 | 3.857 | 0,087 | REFUTED (no excess, ceiling <1% of margin) |
| H4 | closes >= 115 min after 5pm: Lula% (w/o lag, place FE) | PT | -0,00101 | same sections in T1/2026 | -0,00090 | 0,9361 | 0,5320 | 1,000 | 1,000 | 8.130 | 0,184 | 8.130 | 0,184 | REFUTED (no excess, ceiling <1% of margin) |
| H5 | sections with turnout >=95% in T2/2026: excess over composition expectation (type x size, 2022 rates) | PT | 0,90390 | same test in T1/2026 | 0,64612 | 0,0169 | 0,0084 | 0,177 | 0,065 | 19.023 | 0,429 | 19.023 | 0,429 | REFUTED (no excess, ceiling <1% of margin) |
| H6 | new vs old sections of the same place: Lula% in T2 given T1 | PT | 0,00536 | 2018/T2 | 0,01344 | 0,0000 | 1,0000 | 1,000 | 1,000 | 0 | 0,000 | 92.023 | 2,077 | INCONCLUSIVE (no excess, but ceiling >=1% of margin) |
| H7 | upward local outliers (pro-PT), /adjusted z/ > 3, per 10 thousand sections | PT | 44,76561 | 2022/T1 | 47,57592 | 0,6068 | 0,9693 | 1,000 | 1,000 | 0 | 0,000 | 20.301 | 0,458 | REFUTED (no excess, ceiling <1% of margin) |
| H7 | asymmetry: proportion of outliers that are pro-PT | PT | 0,63272 | 2022/T1 | 0,64457 | 0,4787 | 0,8286 | 1,000 | 1,000 | 1.782 | 0,040 | 8.336 | 0,188 | REFUTED (no excess, ceiling <1% of margin) |
| H8 | last digit: Cramér's V of PT in T2/2026 | PT | 0,00097 | 2022/T1 | 0,00193 | 0,4503 | 0,9474 | 1,000 | 1,000 | n/a | n/a | n/a | n/a | NO EXCESS (shape test, no conversion to votes) |
| H8 | last digit: Cramér's V of OPO in T2/2026 | PT | 0,00210 | 2022/T1 | 0,00340 | 0,9620 | 0,9810 | 1,000 | 1,000 | n/a | n/a | n/a | n/a | NO EXCESS (shape test, no conversion to votes) |
| H8 | exact integer percentage (PT and OPO, symmetric): obs/expected in T2/2026 | PT | 0,77957 | 2022/T2 | 0,79067 | 0,9236 | 0,8418 | 1,000 | 1,000 | n/a | n/a | n/a | n/a | NO EXCESS (shape test, no conversion to votes) |

## Appendix B: not executed

| test | reason |
|---|---|
| BU | NotExecuted: direct test with printed poll-receipts: no BU photo/PDF was provided (neither in Downloads nor in the project). Send images with the QR code visible or a spreadsheet zone;section;round;votes for the cross-check with the BWeb. Discrepancy of any size will be reported. |

End.
