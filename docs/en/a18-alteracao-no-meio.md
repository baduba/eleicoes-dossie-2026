# A18. "Alteration in the middle" hypothesis (between the closing of the voting machine and publication)

**Hypothesis.** Someone alters the results after the voting machine closes and before the data are published (during transmission, reception, tallying, or publication), in a way that is consistent across all files.

> **What A4 and H9 check and what they do not check.** They check **consistency among files published by the TSE** (poll-receipt (BU), RDV, BU image, log, BWeb, tally by zone and municipality) and the hash linkage between them. These files are born from the same software and the same flow. For that reason they **do not rule out a coherent alteration made before publication**. Only a verification that does not depend on the published files rules out this hypothesis: the **cryptographic signature** checked with the official key, and the **comparison with printed poll-receipts** photographed at the sections.

## 1. The delays, with sources

| round | what was said or decided | source | what the data show |
|---|---|---|---|
| 1st round (Oct 4, 2026) | The president of the TSE confirmed a delay of about 1 hour in releasing the total, which he attributed to congestion in the Court's data system ("data flow above normal"). Around 7pm the national presidential total stalled at 64%; around 8pm it resumed, already at 84%. The TSE said it did not yet know whether there was a cause beyond the congestion. | [JB, Oct 5, 2026](https://www.jb.com.br/brasil/politica/2026/10/1061122-tse-confirma-atraso-na-totalizacao-dos-votos-e-explica-causa.html) (press; paraphrase of the statement; the official source could not be opened) | Between 19:30 and 19:59 only 1.5% of sections had their BU received, versus 23.8% between 19:00 and 19:29 and 5.6% between 20:00 and 20:29 (table below). |
| 2nd round (Oct 25, 2026) | Voting was extended by two hours by decision of Justice Cristiano Zanin, at the request of the Lula campaign (bus shortages in Bahia); the TSE stated that voting would continue only in sections still open at 5pm. BU reception, tallying, and publication resumed at 7pm; before the pause, 1,225 of the 499,248 sections (about 0.25%) had been tallied. | [Times Brasil](https://timesbrasil.com.br/brasil/decisao-2026-tse-anuncia-retomada-da-totalizacao-e-divulgacao-dos-votos-apos-as-19h/) and [Correio da Manhã](https://www.correiodamanha.com.br/politica/2026/10/329719-tse-retoma-contagem-dos-votos-as-19h-apos-suspensao-provocada-por-decisao-de-zanin.html) (press; the official notice was not opened) | 99.6% of BUs have a reception time after 7pm (A14). |

BU reception in the 2026 1st round, per half hour (all sections with a reception time):

| inicio | secoes | pct |
|---|---|---|
| 17:00 | 11.122 | 2,2 |
| 17:30 | 63.099 | 12,7 |
| 18:00 | 103.584 | 20,8 |
| 18:30 | 124.799 | 25,1 |
| 19:00 | 118.591 | 23,8 |
| 19:30 | 7.651 | 1,5 |
| 20:00 | 27.737 | 5,6 |
| 20:30 | 32.746 | 6,6 |
| 21:00 | 5.311 | 1,1 |
| 21:30 | 1.917 | 0,4 |
| 22:00 | 725 | 0,1 |
| 22:30 | 300 | 0,1 |
| 23:00 | 102 | 0,0 |
| 23:30 | 24 | 0,0 |

The reception time is the `DT_RECEBIMENTO_BU_HOR_TSE` field published by the TSE. The drop from 19:30 to 20:00 is compatible with the stoppage described; the data do not state the cause.

## 2. Cryptographic signature (highest priority): NOT EXECUTED — PARTIAL

- **Read and checked:** the X.509 certificate of every Roraima section in 2026: 1,519 read, 0 errors. CN = `UEAO` + voting-machine number from BWeb in 1,519 of 1,519; validity covers the election date in 1,519 of 1,519; issuers `AC UE2020` (922), `AC UE2022` (597).
- **Verified:** **0% of the signatures** (0 of 1,519 sections read; 0 failures because none were tested). The algorithm OID is `1.3.6.1.4.1.44588.2.1`, with a 66-byte key and a 132-byte signature.
- **What is missing:** the official root certificate and public key, and the algorithm specification, obtained from an official source. The TSE website responds with HTTP 403 to automation, and **no key from a non-official source was used**. A 2021 TSE presentation (seen only in a search result) cites EdDSA over Curve25519 for the BU QR code and 256-bit curves for other signatures; this was neither confirmed nor verified here.
- **How to unblock:** an expert or party observer with access to the TSE's official verification tool runs the script `scripts/13_cert_urna.py` and the tool on the same files and publishes the result via *issue*.

## 3. Pre-registered tests (Addendum 7)

The window and the tests were fixed in [Addendum 7](preregistro.md) before running. The tests compare 2026 with the same clock window in years without congestion (placebos), with polling-place fixed effects. **Prediction without alteration:** no difference beyond composition.

| H | test | est_2026T2 | placebos | p_excesso | p_holm | verdict |
|---|---|---|---|---|---|---|
| A18a | 1o turno 2026: BU recebido entre 19h e 20h: participacao de Lula nos validos, EF de local | 0,00090 | 2022/T1: -0.00001 (ep 0.00034, p_exc 0.0398) / 2018/T1: -0.00030 (ep 0.00039, p_exc 0.0157) | 0,040 | 0,159 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| A18a | 1o turno 2026: BU recebido entre 19h e 20h: participacao de oponente nos validos, EF de local | -0,00090 | 2022/T1: 0.00001 (ep 0.00034, p_exc 0.96) / 2018/T1: 0.00030 (ep 0.00039, p_exc 0.984) | 0,984 | 1,000 | REJECTED (no excess, ceiling <1% of the margin) |
| A18b | 2o turno 2026: horas de atraso no recebimento depois das 19h: participacao de Lula nos validos, EF de local | 0,00025 | 2022/T2: 0.00033 (ep 0.00051, p_exc 0.555) / 2018/T2: 0.00295 (ep 0.00136, p_exc 0.974) / 2026/T1: -0.00205 (ep 0.00058, p_exc 0.000207) | 0,974 | 1,000 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| A18b | 2o turno 2026: horas de atraso no recebimento depois das 19h: participacao de oponente nos validos, EF de local | -0,00025 | 2022/T2: -0.00033 (ep 0.00051, p_exc 0.445) / 2018/T2: -0.00295 (ep 0.00136, p_exc 0.026) / 2026/T1: 0.00205 (ep 0.00058, p_exc 1) | 1,000 | 1,000 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |

**Reading.** In the 19:00–20:00 window of the 1st round, sections at the same polling place whose BU was received during the congestion show a Lula share of valid votes 0.09 p.p. higher than the others (and the opponent's share 0.09 p.p. lower). Against the placebos the raw one-sided p is 0.040 (the largest of 2022 and 2018); with the Holm correction for the four tests, 0.159. **It does not meet the excess criterion.** The verdict under the pre-registered rule is inconclusive because the worst-case ceiling exceeds 1% of the margin, not because there is an excess. In the 2nd round there is no difference beyond the placebos. The ceilings in this table are upper bounds under the exposure convention of Addendum 7 and depend on the uncertainty of the placebos; **they do not measure altered votes**. These tests **do not rule out** a coherent alteration; they only search for a specific temporal signature.

Estimates by year (window coefficient, in share of valid votes; the standard error is clustered by polling place):

| ano | resposta | secoes | secoes_na_janela | pct_na_janela | coef_janela | ep |
|---|---|---|---|---|---|---|
| 2026 | lula_sh | 497.708 | 126.242 | 25,4 | 0,00090 | 0,00039 |
| 2026 | dir_sh | 497.708 | 126.242 | 25,4 | -0,00090 | 0,00039 |
| 2026 | lula_sh (robustez: defasagem > p90) | 497.708 | 49.580 | 10,0 | -0,00009 | 0,00031 |
| 2026 | dir_sh (robustez: defasagem > p90) | 497.708 | 49.580 | 10,0 | 0,00009 | 0,00031 |
| 2022 | lula_sh | 470.437 | 203.627 | 43,3 | -0,00001 | 0,00034 |
| 2022 | dir_sh | 470.437 | 203.627 | 43,3 | 0,00001 | 0,00034 |
| 2018 | lula_sh | 452.479 | 123.685 | 27,3 | -0,00030 | 0,00039 |
| 2018 | dir_sh | 452.479 | 123.685 | 27,3 | 0,00030 | 0,00039 |

Sections with candidate votes + blank + null differing from turnout in the 2026 1st round (prediction: zero in both groups): window = 1, within the 19:00–20:00 window; window = 0, the rest.

| janela | secoes | com_inconsistencia |
|---|---|---|
| 0.0 | 371.466 | 0 |
| 1.0 | 126.242 | 0 |

**2nd round: order of reception after 7pm.** Coefficient per hour of reception delay:

| ano | turno | resposta | secoes_apos_19h | coef_por_hora | ep |
|---|---|---|---|---|---|
| 2026 | 2 | lula_sh | 496.651 | 0,00025 | 0,00029 |
| 2026 | 2 | dir_sh | 496.651 | -0,00025 | 0,00029 |
| 2022 | 2 | lula_sh | 74.569 | 0,00033 | 0,00051 |
| 2022 | 2 | dir_sh | 74.569 | -0,00033 | 0,00051 |
| 2018 | 2 | lula_sh | 38.975 | 0,00295 | 0,00136 |
| 2018 | 2 | dir_sh | 38.975 | -0,00295 | 0,00136 |
| 2026 | 1 | lula_sh | 195.104 | -0,00205 | 0,00058 |
| 2026 | 1 | dir_sh | 195.104 | 0,00205 | 0,00058 |

Share of the variance in reception time explained by state (UF) and by municipality (descriptive, not a test):

| ano | turno | secoes_apos_19h | r2_horario_por_UF | r2_horario_por_municipio | horas_mediana_apos_19h |
|---|---|---|---|---|---|
| 2026 | 2 | 496.651 | 0,39 | 0,71 | 1,43 |
| 2022 | 2 | 74.569 | 0,06 | 0,50 | 0,22 |
| 2018 | 2 | 38.975 | 0,19 | 0,64 | 0,30 |
| 2026 | 1 | 195.104 | 0,09 | 0,42 | 0,32 |

In the 2026 2nd round, reception time after 7pm has more geographic structure (by UF) than in the comparison years. This is expected when reception is held until a given time and released in transmission order; it does not distinguish this explanation from another.

## 3b. Corrected A1 in the 2026 1st round and the congestion window (post-hoc analysis)

> **Post-hoc** analysis (requested after seeing the result; not pre-registered). It does not change the verdict of the corrected A1, whose pre-registered target is the 2nd round.

The 2026 1st-round curve, against the corrected null (municipalities in random order within each UF), falls outside the envelope at 241 of the 900 points evaluated, almost all in a single run of 240 consecutive points, from 76.0% to 99.9% of sections, from 19:18 to 22:28 on Oct 4.

- **Does it coincide with the 19:00–20:00 window?** In part. The run **starts** inside the window (19:18) and 91 of the 241 out-of-envelope points (38%) fall between 7pm and 8pm, versus 26.5% of all curve points in that window. But the run **continues** until 22:28, well after the resumption.
- **The deviation does not grow in the window.** The curve stays below the null median (lower Lula share) throughout the stretch; the largest deviation is -1.67 p.p., at 19.5% of sections (18:13), **before** the window. From there the deviation shrinks to zero (-0.86 p.p. at 76%, -0.63 p.p. at 84%, -0.25 p.p. at 95%). The "out of envelope" stretch is the final part of the curve, where the null envelope narrows because the cumulative curve converges to the total; there, even a small deviation exits the envelope.

- **Which UFs arrived in that stretch.** The sections arriving during the run come mainly from SP (20% of the UF), BA (44% of the UF), MG (30% of the UF), RJ (41% of the UF), CE (45% of the UF), PE (38% of the UF); BA, RJ, CE, PE, MA and AL weigh more in the stretch than in the country (columns below). In the sections whose first tally fell between 7pm and 8pm, the largest contributions are SP (26.8%), MG (12.1%), RJ (10.4%), BA (7.7%), CE (5.8%).

Sections by UF in the out-of-envelope stretch (all UFs in `results/fase2/A1T1_ufs.csv`):

| SG_UF | secoes | nas_corridas | pct_da_UF_nas_corridas | pct_das_secoes_nas_corridas | pct_das_secoes_do_pais |
|---|---|---|---|---|---|
| SP | 103.656 | 20.782 | 20,1 | 17,3 | 20,8 |
| BA | 35.476 | 15.627 | 44,0 | 13,0 | 7,1 |
| MG | 52.062 | 15.619 | 30,0 | 13,0 | 10,4 |
| RJ | 37.675 | 15.430 | 41,0 | 12,8 | 7,5 |
| CE | 23.765 | 10.693 | 45,0 | 8,9 | 4,8 |
| PE | 21.418 | 8.108 | 37,9 | 6,7 | 4,3 |
| MA | 18.093 | 6.283 | 34,7 | 5,2 | 3,6 |
| PA | 20.827 | 5.388 | 25,9 | 4,5 | 4,2 |
| AL | 7.101 | 4.035 | 56,8 | 3,4 | 1,4 |
| SC | 17.326 | 2.549 | 14,7 | 2,1 | 3,5 |

Sections whose first tally fell between 7pm and 8pm, by UF (all in `results/fase2/A1T1_ufs_janela.csv`):

| SG_UF | secoes | na_janela | pct_da_UF_na_janela | pct_das_secoes_da_janela | lula_pct_validos_na_janela |
|---|---|---|---|---|---|
| SP | 103.656 | 35.470 | 34,2 | 26,8 | 43,9 |
| MG | 52.062 | 16.037 | 30,8 | 12,1 | 47,3 |
| RJ | 37.675 | 13.808 | 36,6 | 10,4 | 42,3 |
| BA | 35.476 | 10.245 | 28,9 | 7,7 | 69,4 |
| CE | 23.765 | 7.749 | 32,6 | 5,8 | 66,2 |
| PE | 21.418 | 6.883 | 32,1 | 5,2 | 67,2 |
| SC | 17.326 | 5.257 | 30,3 | 4,0 | 25,9 |
| RS | 27.547 | 5.204 | 18,9 | 3,9 | 39,7 |
| MA | 18.093 | 5.051 | 27,9 | 3,8 | 67,0 |
| PA | 20.827 | 4.791 | 23,0 | 3,6 | 51,6 |

**Conclusion.** The congestion window **does not explain** the out-of-envelope stretch: it starts inside it, but continues afterwards and the deviation is decreasing. The UF composition (Northeast and Southeast arriving later) is compatible with the deviation, but the explanation was not demonstrated. The item goes to [Open questions](residuos.md). Nothing here indicates vote alteration; it is a shape of the curve that the null used does not reproduce.

## 4. Detection power of printed poll-receipts

How many printed poll-receipts from randomly drawn sections would be needed to detect, with 95% and 99% probability, at least one altered section, if a fraction of the sections had been altered (population of 499,248 sections, sampling without replacement):

| fracao_alterada | secoes_alteradas | n_para_95 | n_para_99 |
|---|---|---|---|
| 0.1% | 500 | 2.981 | 4.575 |
| 1% | 4.993 | 298 | 458 |
| 2% | 9.985 | 149 | 228 |
| 5% | 24.963 | 59 | 90 |
| 9% | 44.933 | 32 | 49 |

How many sections would be needed to overturn the margin of 4,430,191 votes, if each altered section had 5, 50, or 200 switched votes (each switched vote changes the margin by 2), and how many drawn receipts would suffice to flag at least one of them:

| trocas_por_secao | secoes_necessarias_para_inverter_a_margem | pct_das_secoes | n_para_95 | n_para_99 |
|---|---|---|---|---|
| 5 | 443.020 | 88,7 | 2 | 3 |
| 50 | 44.302 | 8,9 | 33 | 50 |
| 200 | 11.076 | 2,2 | 134 | 206 |

The calculation applies to a random sample of sections. Voluntarily submitted photos are not random and reduce power; what counts is the total checked without discrepancy, published in [Printed poll-receipts](boletins-impressos.md). To overturn the margin with 50 switches per section, the alteration would have to reach 8.9% of sections, and a sample of 50 receipts would detect it with 99% probability.

## 5. Collection

The direct cross-check against printed poll-receipts remains **NOT EXECUTED** for lack of input. The page [Printed poll-receipts](boletins-impressos.md) explains how to submit photos, and the script `04_cruza_bu_impresso.py` is ready to be run on each batch.

## 6. The delay window: what is still missing

- **1st round:** the test uses the Addendum 7 clock window and the within-polling-place comparison. A window based on the Sistot log (not public) would be more precise.
- **2nd round:** the test compares the order of reception after 7pm with the Lula share within the polling place, controlling for the 1st round. The comparison with geography is the variance table above.
