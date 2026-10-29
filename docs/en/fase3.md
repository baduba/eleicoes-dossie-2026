# Phase 3: adversarial hypotheses (A20 to A33)

> **Unit: margin votes** (change in the Lula-minus-Flávio difference; switching one vote changes the margin by 2; definition in [Methodology](metodologia.md)). Official margin: 4,430,191. Every ceiling is a **worst-case ceiling, not an estimate**. The form tests have no ceiling in votes.

Predictions, criteria, and what each test covers were registered in [Addendum 8](preregistro.md) **before** running. Each test describes the **failure class** it covers and the **expected trace** in the public data, not how to produce the failure. When an input is missing, the test is marked **NOT RUN**, with the input and how to supply it.

| test | failure class covered | result | ceiling in margin votes | verdict |
|---|---|---|---|---|
| [A20](#a20) Registry x Census | inflated eligible electorate | 80+ and 90+: fraction of municipalities with more eligible voters than inhabitants above 2018 and 2022 (formal; see caveat); 16+ and 100+: no excess | 80+ turnout above 2022 rates: 459,099 margin votes (worst-case ceiling, not an estimate; 10.4% of the margin) | EXCESS DETECTED (form) in 80+ and 90+, **with a design caveat**; TESTED-INCONCLUSIVE |
| [A20b-idosos](#a20b) Elderly registry | very elderly voters who do not exist; uneven manual voter release | 100+ voters ≈ 5% of the Census, no municipality with a cohort jump; 90+ fraction x manual voter release grows from 2018 to 2026 (form); turnout in the sections with the most 80+ rises (form) | up to 241,008 margin votes (worst-case ceiling, not an estimate; 5.4% of the margin) in turnout | TESTED-INCONCLUSIVE; EXCESS DETECTED (form) in two measures, **with a caveat** |
| [A21](#a21) Logs, vote pace | vote recording outside the real pace | intervals < 10 s: none, in any year; last vote after nominal closing time explained by the Oct 25 extension | no conversion into votes (sample) | partial; EXCESS DETECTED (form) in one measure, **with a caveat** |
| [A22](#a22) Cross-office coherence | uniform shift only in the presidential race | **NOT EXECUTABLE under the registered rule** (no 2026 state eligible). Exploratory variant (Addendum 9b), only AM and DF: INCONCLUSIVE | up to 548,671 margin votes (worst-case ceiling, not an estimate; 12.4% of the margin), **only in AM and DF votes** | NOT RUN (official); INCONCLUSIVE (exploratory) |
| [A23](#a23) Party observation | different behavior where a party observer is present or not | **NOT RUN** (no list of sections with observers) | n/a | NOT RUN |
| [A24](#a24) Natural experiment of the integrity test | voting machine that behaves differently outside the test | **NOT RUN**: no section list read from TRE publications (sites block automated access); script and input file ready | n/a | NOT RUN |
| [A25](#a25) Replaced voting machines | machine replacement as an intervention point | section with replacement x neighbors: see A6 (no effect); before x after replacement: NOT RUN | n/a (A6: ceiling below 1% of the margin) | partial |
| [A26](#a26) Publication integrity | published file altered afterwards | 233 files: same size in 233; official hash equal in 224 of 224; none modified after the first download | n/a | NO ALTERATION DETECTED |
| [A27](#a27) Fabricated sections | sections without real voters | 427 new sections with turnout ≥ 95%: profile below | 44,735 margin votes (worst-case ceiling, not an estimate; 1.0% of the margin): all Lula votes in the 427 sections, assumed invalid | TESTED-INCONCLUSIVE |
| [A32](#a32) Manual voter release as a channel for local abuse | manual authorizations in bursts, late in the day, or excessive for the age | no burst under the registered definition (which cannot see them); manual releases do not concentrate at the end of the day; sections with more than 30% manual release: 3,995 in 2022 and 348 in 2026; no association with turnout or vote | registered 1,852,233 (inflated by negative shift, Addendum 11c); beyond the 2022 model noise: 55,862 margin votes (worst-case ceiling, not an estimate; 1.26% of the margin) | TESTED-INCONCLUSIVE (partial logs) |
| [A28](#a28) LAI (Access to Information Law) requests | data only the government holds | 7 requests ready in `lai/` (07, for the tally sheet and the signature sheet, belongs to A32), with agency and channel for each, and a request template for parties; **none filed** | n/a | NOT RUN |
| [A31b](#a31b) Municipalities with the opponent at +1 vote or fewer | concentrated vote switching or selective abstention | 748 municipalities (14.0%), compatible with the national shift; regional profile with a strong PT electorate; most with a turnout drop | ceiling A of 234,746 margin votes (worst-case ceiling, not an estimate), and **zero** beyond what the simulated national shift already gives | TESTED-INCONCLUSIVE |
| [A32b](#a32b) Manual-release bursts (absolute threshold) | manual authorizations in sequence | observed/expected ratio of 1.0 to 1.2 in both years; bursts less frequent in 2026 than in 2022; 2026 coefficients indistinguishable from zero | powerless ceiling (extrapolated), **not plotted** | TESTED-INCONCLUSIVE |
| [A33](#a33) Manual release by school | manual release concentrated in polling locations, with Lula gain or turnout | no positive association between the school's manual rate and Lula's T1 → T2 gain (2026 coefficient negative, -0.017); 2022 and 2018 placebos with no excess; log synchrony equal to 2022's | 29,654 margin votes for the 661 extreme schools (worst-case ceiling, not an estimate; 0.67% of the margin); beyond the model noise: 8,125 | TESTED-INCONCLUSIVE |

| [A31](#a31) Municipalities extreme in the T1 → T2 transfer (Silva Jardim) | vote transfer between rounds beyond what municipalities do | Silva Jardim: Flávio +1 and turnout -104 reproduce; Lula is +984, not +964. Within the expected tail (z = 1.13, Holm 1.00); 14.0% of 2026 municipalities have the opponent with +1 vote or fewer. Three small municipalities fall outside the main model's tail | Silva Jardim: 207 margin votes (worst-case ceiling, not an estimate; 0.005% of the margin). 20 most extreme: 1,151 beyond the tail, 13,327 if everything the model does not explain were manipulation (0.30% of the margin) | Silva Jardim: WITHIN THE EXPECTED TAIL; 3 municipalities flagged, TESTED-INCONCLUSIVE |
<a id="a20"></a>

## A20. Registry: eligible electorate x 2022 Census population

**Question.** Are there more eligible voters than inhabitants, by municipality and age band, and did that change between 2018, 2022, and 2026? **Failure class covered:** inflated eligible electorate. **Expected trace:** eligible/population ratio above 1 in municipalities, concentrated among the oldest. **No-manipulation prediction:** fraction of municipalities with ratio > 1 in 2026 within the range of 2018 and 2022, after removing the national level.

**Method.** Population: 2022 Census (IBGE, SIDRA 9514), the same in all years; therefore 2018 and 2026 have an outdated denominator and each municipal ratio is rescaled by the year's national ratio to the 2022 scale (Addendum 8). Eligible: electorate profile by zone and age band (1st round). TSE x IBGE mapping by name and state: 5,557 of 5,757 municipalities (200 without a name match are left out). Municipalities with band population below 100 (16+), 30 (80+), 10 (90+), or 1 (100+) are left out of each band.

| group | year | municipios | razao_nacional | aptos | populacao_2022 | fracao_municipios_razao_gt1_bruta | fracao_razao_gt1_na_escala_de_2022 |
|---|---|---|---|---|---|---|---|
| 16+ | 2018 | 5.557 | 0,917 | 146.677.285 | 160.008.643 | 52,1% | 70,2% |
| 16+ | 2022 | 5.557 | 0,973 | 155.621.019 | 160.008.643 | 68,3% | 68,3% |
| 16+ | 2026 | 5.557 | 0,985 | 157.684.580 | 160.008.643 | 72,1% | 68,4% |
| 80+ | 2018 | 5.544 | 0,892 | 4.089.634 | 4.583.484 | 35,6% | 56,5% |
| 80+ | 2022 | 5.544 | 1,122 | 5.140.993 | 4.583.484 | 65,7% | 66,3% |
| 80+ | 2026 | 5.544 | 1,201 | 5.503.440 | 4.583.484 | 75,4% | 68,4% |
| 90+ | 2018 | 5.237 | 1,278 | 997.035 | 780.045 | 38,1% | 50,2% |
| 90+ | 2022 | 5.237 | 1,775 | 1.384.465 | 780.045 | 57,1% | 59,0% |
| 90+ | 2026 | 5.237 | 1,659 | 1.294.142 | 780.045 | 58,9% | 63,6% |
| 100+ | 2018 | 4.385 | 1,006 | 38.021 | 37.779 | 33,6% | 65,7% |
| 100+ | 2022 | 4.385 | 4,775 | 180.404 | 37.779 | 51,5% | 61,2% |
| 100+ | 2026 | 4.385 | 7,767 | 293.432 | 37.779 | 43,8% | 35,4% |

**Result under the pre-registered criterion (form, no ceiling in votes):**

| group | fracao_2026 | comparison | verdict |
|---|---|---|---|
| 16+ | 68,4% | 2022: dif 0.11 p.p. (z 0.1) / 2018: dif -1.85 p.p. (z -2.1) | NO EXCESS (form test, no conversion into votes) |
| 80+ | 68,4% | 2022: dif 2.11 p.p. (z 2.4) / 2018: dif 11.83 p.p. (z 13.0) | EXCESS DETECTED (form test, no conversion into votes) |
| 90+ | 63,6% | 2022: dif 4.62 p.p. (z 4.9) / 2018: dif 13.39 p.p. (z 14.0) | EXCESS DETECTED (form test, no conversion into votes) |
| 100+ | 35,4% | 2022: dif -25.86 p.p. (z -25.1) / 2018: dif -30.33 p.p. (z -29.8) | NO EXCESS (form test, no conversion into votes) |

> **Design caveat (read together with the verdict).** The fraction of municipalities with ratio > 1 rises continuously from 2018 to 2022 and to 2026 in 80+ and 90+, and the intersection-union test against each previous year flags the last year of an increasing series. The jump from 2022 to 2026 (80+: 2.1 p.p.; 90+: 4.6 p.p.) is smaller than from 2018 to 2022 (9.8 and 8.8 p.p.). The excess label is formal and **does not indicate manipulation**; the line was not changed.

**What stands out, without causal interpretation.** (i) The national 80+ ratio is 0.89 (2018), 1.12 (2022), and 1.20 (2026) against the 2022 Census; the 90+ ratio is 1.28, 1.78, and 1.66; the 100+ ratio is 1.0, 4.8, and 7.8: 297,977 eligible voters aged 100 or older in 2026 against 37,779 people of that age in the Census. Voter age comes from the registry, Census age is self-reported; part of it may be a default date of birth or an un-cancelled registration, and turnout in these bands is small (0.7% in 100+). (ii) Optional-voter turnout rises **in every band aged 70 or older** from 2022 to 2026:

| band | 2018 | 2022 | 2026 |
|---|---|---|---|
| 70 to 74 years | 55,3% | 61,1% | 68,9% |
| 75 to 79 years | 37,5% | 41,8% | 52,3% |
| 80 to 84 years | 24,1% | 27,0% | 37,2% |
| 85 to 89 years | 13,3% | 15,7% | 24,3% |
| 90 to 94 years | 4,9% | 6,7% | 13,5% |
| 95 to 99 years | 1,9% | 1,6% | 4,3% |
| 100 years or older | 3,9% | 0,9% | 0,7% |

If 2026 turnout in the bands aged 80 or older had stayed at 2022 rates, there would be 459,099 fewer voters. **Worst-case ceiling, not an estimate:** 459,099 margin votes (10.4% of the margin), if all of that increase were an additional vote for a single candidate, which the data do not indicate: the increase also appears at ages 70 to 74 and 75 to 79, pointing to a general phenomenon in the optional-voting band. **Status:** TESTED-INCONCLUSIVE. **What would close it:** cross-checking the registry against the civil death registry by an oversight entity, and a per-section profile.

**Addendum 8's A20b line (age and sex profile of the new sections).** Remains NOT RUN. The registration said the public profile is only per zone; **that was wrong**: the TSE publishes the electorate profile per section (`perfil_eleitor_secao`), which came to be used in the next section. The new-sections test with that input was not done in this round.

<a id="a20b"></a>

## A20b-idosos. Registry and turnout of the oldest voters (Phase 3.1)

Registration: [Addenda 9, 9a, and 9d](preregistro.md). The label is A20b-idosos to avoid colliding with Addendum 8's A20b line. **No-manipulation prediction:** 100+ voters compatible with the Census; manual voter release in these bands equal across years; turnout and vote without association with the section's fraction of elderly.

### 1. Legal rule for cancellation

- **Absence at three consecutive elections:** [Electoral Code](https://www.planalto.gov.br/ccivil_03/leis/l4737compilado.htm), art. 71, V, and art. 7, § 3 (cancellation of anyone who does not vote in three consecutive elections, does not pay the fine, or does not justify). [TSE Resolution 23.659/2021](https://www.tse.jus.br/legislacao/compilada/res/2021/resolucao-no-23-659-de-26-de-outubro-de-2021), art. 130, counts each round as an election (§ 1) and **exempts optional voters from the rule** (§ 2): those over 70 years old, illiterate voters, and voters aged 16 and 17 (Constitution, art. 14, § 1, II). In 2025 the Electoral Justice cancelled about 5 million registrations of absentees (press, from TSE data); **an absent optional voter is not counted in that figure**.
- **Death:** Electoral Code, art. 71, IV (death of the voter), with **monthly** notification by the Civil Registry offices for cancellation of registrations (art. 71, § 3).
- **Consequence for the test:** since absence does not cancel an optional voter's registration, **eligible voters above the Census in the oldest bands do not indicate voting**; only voters indicate voting. Registrations of deceased persons not yet notified remain in the registry.
- **Limit of the verification:** the Electoral Code was read in the Planalto text; Resolution 23.659 is on a site that blocks automated access, and the cited paragraphs come from a search summary and from TRE pages; check the official link. The Resolution's article on death was not confirmed.

### 2. 90+ and 100+ voters against the 2022 Census, by municipality

> **Design warning (Addendum 9a).** The Census is from 2022: only 2022 compares the same cohort. In 2026 the 90+ band is the 86+ cohort of 2022, and in 2018 it is the 94+ cohort, so the 2018 and 2026 ratios are not comparable in form. Therefore the formal verdict of this item is not used as a conclusion; test 2a governs.

| year | round | band | voters | populacao_censo_2022 | razao_nacional | municipalities (min. population) with voters > population | municipalities in the full list | voters above the population | warning |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | 1 | 90+ | 39.984 | 779.711 | 5,1% | 0 | 1 | 1 | cohort mismatch (Addendum 9a) |
| 2018 | 1 | 100+ | 1.178 | 32.492 | 3,6% | 0 | 47 | 50 | cohort mismatch (Addendum 9a) |
| 2018 | 2 | 90+ | 41.139 | 779.711 | 5,3% | 0 | 1 | 2 | cohort mismatch (Addendum 9a) |
| 2018 | 2 | 100+ | 1.170 | 32.492 | 3,6% | 0 | 48 | 53 | cohort mismatch (Addendum 9a) |
| 2022 | 1 | 90+ | 58.582 | 779.993 | 7,5% | 0 | 1 | 2 | same cohort |
| 2022 | 1 | 100+ | 1.314 | 32.492 | 4,0% | 0 | 40 | 41 | same cohort |
| 2022 | 2 | 90+ | 75.302 | 779.993 | 9,7% | 0 | 1 | 1 | same cohort |
| 2022 | 2 | 100+ | 1.663 | 32.492 | 5,1% | 0 | 44 | 45 | same cohort |
| 2026 | 1 | 90+ | 105.442 | 780.012 | 13,5% | 4 | 20 | 46 | cohort mismatch (Addendum 9a) |
| 2026 | 1 | 100+ | 1.624 | 32.492 | 5,0% | 1 | 83 | 91 | cohort mismatch (Addendum 9a) |

Voters are a small fraction of the band's population (about 14% in 90+ and 5% in 100+ in 2026). In 2026 (1st round), 20 municipalities have more 90+ voters than 90+ inhabitants in the Census (46 extra voters in total) and 83 municipalities have more 100+ voters than 100+ inhabitants (91 extra voters), nearly all municipalities with a minuscule band population. In 2022 and 2018 the 100+ list is of similar size (40 to 48 municipalities) and the 90+ list has 1 municipality; the 20 of 2026 in 90+ are the expected effect of the cohort mismatch (the 2026 band includes those who were 86 to 89 years old at the Census), not a conclusion. **Worst-case ceiling, not an estimate:** 137 margin votes if all those voters were votes for a single candidate (less than 0.01% of the margin). Full list: `results/fase3/A20b_item2_lista_municipios_2026T1.csv`. **2026 2nd round: NOT RUN** (the 2026 2nd-round turnout profile was not published; the file on the TSE CDN contains only the 1st round, last modified on 2026-10-21).

### 2a. Cohort monotonicity (no Census)

A person does not get younger: the 2026 registry aged 95+ comes from the 2022 registry aged 91+, contained in 90+; and 100+ in 2026 comes from 96+ in 2022, contained in 95+. R = 2026 numerator / eligible voters of the previous band in 2022; the placebo is the same pair four years earlier (2022 against 2018). 1st round.

| numerator / denominator | pair | measure | municipios | R_nacional | ep_R | fraction of municipalities with R > 1 | municipalities with R > 1 |
|---|---|---|---|---|---|---|---|
| 95+ in y2 / 90+ in y1 | 2026 against 2022 | eligible | 5.147 | 0,4573 | 0,0448 | 0,02% | 1 |
| 95+ in y2 / 90+ in y1 | 2026 against 2022 | voters | 5.147 | 0,0120 | 0,0010 | 0,00% | 0 |
| 95+ in y2 / 90+ in y1 | 2022 against 2018 | eligible | 4.411 | 0,6522 | 0,0098 | 0,11% | 5 |
| 95+ in y2 / 90+ in y1 | 2022 against 2018 | voters | 4.411 | 0,0090 | 0,0007 | 0,00% | 0 |
| 100+ in y2 / 95+ in y1 | 2026 against 2022 | eligible | 3.296 | 0,4593 | 0,0509 | 0,00% | 0 |
| 100+ in y2 / 95+ in y1 | 2026 against 2022 | voters | 3.296 | 0,0029 | 0,0004 | 0,00% | 0 |
| 100+ in y2 / 95+ in y1 | 2022 against 2018 | eligible | 2.530 | 0,5967 | 0,0034 | 0,08% | 2 |
| 100+ in y2 / 95+ in y1 | 2022 against 2018 | voters | 2.530 | 0,0047 | 0,0005 | 0,00% | 0 |

**Reading.** (i) No municipality has R > 1 for voters (no 95+ or 100+ voter of 2026 above the previous band's eligible voters of 2022 in the same municipality), and for eligible voters there is 1 case in 2026 against 7 in 2022. (ii) The national eligible-voter ratio **falls** (95+/90+: 45.7% in 2026 against 65.2% in 2022), compatible with mortality and with registry cleaning through deaths (not investigated; cancellation for absence does not reach the optional voter). (iii) The national ratio of **voters** 95+ to previous eligible 90+ rises from 0.90% to 1.20% (z = 2.42; one-sided p 0.0077; Holm-corrected p 0.054): under Addendum 9a's two-standard-error cut it is "formal excess"; under Addendum 2's verdict criterion (Holm) it just misses 0.05. **Both are recorded.** There are about 17 thousand 95+ voters in 2026 against about 9 thousand in 2022, and the difference tracks the general increase in optional-voter turnout (A20). For 100+ there is no excess. **Worst-case ceiling, not an estimate:** by the municipal sum (municipalities with R > 1), 0 margin votes in 95+ and 2 in 100+. **By the ratio difference** (Addendum 9e exploration, factor 1: one extra voter, if for a single candidate, changes the margin by 1): central estimate of 4,205 more 95+ voters than the 2022 ratio would give (out of 16,659 voters), and **worst-case ceiling, not an estimate, of 7,059 margin votes (0.16% of the margin)**, alongside z = 2.42 and Holm 0.054.

### 3. Biometrics by age band

The turnout profile **does not include biometrics**. The per-section electorate profile includes **registered biometrics** by band (not the same-day manual voter release, which comes from the poll-receipt, per section, without age).

| year | group | aptos | com_biometria | pct_biometria |
|---|---|---|---|---|
| 2018 | 100+ | 39.026 | 4.348 | 11,1% |
| 2018 | 90+ (includes 100+) | 1.000.128 | 103.892 | 10,4% |
| 2018 | 16 to 89 years | 145.802.513 | 87.237.302 | 59,8% |
| 2022 | 100+ | 184.330 | 11.385 | 6,2% |
| 2022 | 90+ (includes 100+) | 1.389.277 | 253.406 | 18,2% |
| 2022 | 16 to 89 years | 154.365.669 | 117.767.701 | 76,3% |
| 2026 | 100+ | 297.977 | 23.834 | 8,0% |
| 2026 | 90+ (includes 100+) | 1.299.595 | 471.039 | 36,2% |
| 2026 | 16 to 89 years | 156.525.783 | 140.607.027 | 89,8% |

**3b. Poll-receipt manual voter release against the section's fraction of 90+ eligible voters** (location fixed effect, control for the fraction without registered biometrics; coefficient per unit of fraction; standard error clustered by location):

| year | round | coef | ep | n | locations |
|---|---|---|---|---|---|
| 2018 | 2 | 0,346 | 0,020 | 426.320 | 66.691 |
| 2022 | 2 | 0,638 | 0,009 | 447.114 | 68.546 |
| 2026 | 1 | 0,706 | 0,009 | 475.668 | 72.402 |
| 2026 | 2 | 0,797 | 0,009 | 475.662 | 72.400 |

Result under the pre-registered criterion: **EXCESS DETECTED (form test, no conversion into votes)**, corrected p 9.8e-13. **Trend caveat (Addendum 9d):** the coefficient grows in every year, from 0.35 (2018) to 0.64 (2022), 0.71 (2026, 1st round), and 0.80 (2026, 2nd round); from one electoral cycle to the next the increase was already large before (+0.29 from 2018 to 2022 and +0.16 from 2022 to 2026, both in the 2nd round), and between the two rounds of 2026 it is +0.09. Meaning: within the same location, where there are more 90+ voters there is more manual voter release, and this has been increasing. The label is formal, **does not indicate manipulation**, and has no conversion into votes. For 100+ the additional coefficient is negative (no excess). The age of who was manually released **is not observable with public data**; it is an ecological proxy per section.

### 4. Sections with a high fraction of 80+ eligible voters

2nd-round results, within the same polling location, with the 1st-round outcome as control. Coefficient per unit of the section's fraction of 80+ eligible voters (the mean fraction is 3%; the top decile within the state has 11%).

| outcome | comparator | coef | ep |
|---|---|---|---|
| dir_sh | 2026/T2 | 0,0279 | 0,0013 |
| dir_sh | 2022/T2 | -0,0622 | 0,0014 |
| dir_sh | 2018/T2 | 0,2317 | 0,0043 |
| lula_sh | 2026/T2 | -0,0279 | 0,0013 |
| lula_sh | 2022/T2 | 0,0622 | 0,0014 |
| lula_sh | 2018/T2 | -0,2317 | 0,0043 |
| turnout | 2026/T2 | 0,0378 | 0,0018 |
| turnout | 2026/T1 | -0,6925 | 0,0029 |
| turnout | 2022/T2 | -0,0003 | 0,0018 |
| turnout | 2018/T2 | -0,0015 | 0,0019 |

(the 2026/T1 turnout row is the comparator without control; see below.)

Description, without a test (2026 2nd round, top decile of 80+ fraction within the state against the other sections): turnout 77.1% against 81.4%; Lula 52.9% against 51.7% of valid votes; mean manual voter release 9.2% against 6.6%. Full table by year and round in `results/fase3/A20b_4_descritivo_decil_superior.csv`.

| H | test | est_2026T2 | p_holm | votos_max_pior_caso | pct_pior_caso | verdict |
|---|---|---|---|---|---|---|
| A20b-4 | Lula share of valid votes against the section's fraction of 80+ eligible voters (location FE, 1st-round control) | -0,0279 | 1.0e+00 | 1.787.533 | 40,3% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| A20b-4 | Flavio share of valid votes against the section's fraction of 80+ eligible voters (location FE, 1st-round control) | 0,0279 | 1.0e+00 | 790.398 | 17,8% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| A20b-4 | turnout against the section's fraction of 80+ eligible voters (location FE, 1st-round control) | 0,0378 | 9.3e-52 | 4.070.526 | 91,9% | EXCESS DETECTED and relevant (worst case >= 1% of the margin) |
| A20b-4-supplementary | turnout against the section's fraction of 80+ eligible voters, controlled placebos only (2022/T2 and 2018/T2) | 0,0378 | 1.0e-52 | 241.008 | 5,4% | EXCESS DETECTED and relevant (worst case >= 1% of the margin) |

**Reading.** (i) **Share:** the Lula (-0.028) and Flávio (+0.028) coefficients fall **within the placebo range** (Lula: +0.062 in 2022 and -0.232 in 2018); there is no measured excess. The ceilings of 1,787,533 (in favor of Lula) and 790,398 (in favor of Flávio) margin votes are **worst-case ceilings, not estimates**, and come from the dispersion between the comparison years (the elderly voted very differently in 2018 and 2022), not from a measured effect. (ii) **Turnout:** in the sections with the most 80+ eligible voters, 2026 turnout (2nd round) rises more, given the 1st round, than in 2022 and 2018 (+0.038 against about zero); it is **formal excess**. With all Addendum 9 comparators the ceiling comes out at 4,070,526 margin votes (91.9%), but the 2026/T1 comparator lacks the 1st-round control and is of a different specification; **Addendum 9d's supplementary line**, with only the controlled placebos, gives **241,008 margin votes (5.4% of the margin), worst-case ceiling, not an estimate**, if all additional turnout were votes for a single candidate. The data do not indicate that: the Lula-share coefficient in those same sections is negative. (iii) It matches the A20 finding (optional-voter turnout rises in every band aged 70 or older), but here within the same location and per section. **Status: TESTED-INCONCLUSIVE.** **What would close it:** signed authorization lists of the sections with the most elderly and a cross-check of the registry against the civil death registry, by an oversight entity.

### 5. How many older voters voted (exploration, Addendum 9e)

Voters and turnout by band, 1st round (comparable across the three years). Up to age 69 voting is **mandatory**; from 70 on it is **optional**. The public data say how many voted, not for whom.

| band | voters 2018 | turnout 2018 | voters 2022 | turnout 2022 | voters 2026 | turnout 2026 | 2026 against 2022 (voters) |
|---|---|---|---|---|---|---|---|
| 60 to 69 years (mandatory) | 13.154.983 | 83,9% | 15.395.122 | 85,8% | 17.552.428 | 87,3% | 2.157.306 (+14%) |
| 70 years or older | 4.480.899 | 37,3% | 6.120.350 | 41,2% | 8.755.306 | 50,9% | 2.634.956 (+43%) |
| 90 years or older | 40.270 | 4,0% | 59.011 | 4,2% | 106.332 | 8,2% | 47.321 (+80%) |
| 95 years or older | 6.588 | 2,1% | 9.266 | 1,4% | 16.802 | 2,6% | 7.536 (+81%) |
| 100 years or older | 1.506 | 3,9% | 1.675 | 0,9% | 2.141 | 0,7% | 466 (+28%) |

**Reading.** (i) Those aged 60 to 69 vote: 84%, 86%, and 87% turnout in 2018, 2022, and 2026. The large abstention starts at 70, when voting is optional. (ii) From 2018 to 2022 (the general election before 2026) voters aged 70 or older rise from 4,480,899 to 6,120,350, and from 2022 to 2026 rise to 8,755,306; turnout in that band goes from 37% to 41% and to 51%. The increase is **general across the optional-voting band in all three years**, and larger from 2022 to 2026 (this already appears in A20). (iii) In 90+, voters rise 80% from 2022 to 2026 (59,011 to 106,332) while the 90+ registry falls (1.39 million to 1.30 million): turnout goes from 4.2% to 8.2% (1st round). In 100+ voters are 2,141 in 2026. (iv) **In margin votes:** the 95+ voters of 2026 amount to 0.38% of the margin if all voted for the same candidate (one extra vote changes the margin by 1); the 95+ test above gives the ceiling on the **excess** over 2022. There is no age nor vote associated in the public data, so none of this says whom they voted for. Full table, with the 2018 and 2022 2nd rounds: `results/fase3/A20b_montante_votantes_por_faixa.csv`.

Data: `results/fase3/A20b_*.csv`; scripts `scripts/30_perfil_secao.py` and `scripts/31_a20b_idosos.py`.

<a id="a21"></a>

## A21. Temporal forensics of voting machine logs (partial)

**Question.** Is the vote pace throughout the day the same as in 2022 and unrelated to the vote? **Failure class covered:** vote recording outside the pace of real voting. **Expected trace:** very short intervals between votes, bursts, concentration in the last hour. **No-manipulation prediction:** equal patterns in 2022 and 2026, with no association with the vote.

**Run** with the measures already extracted from the logs of the voting-machine-file sample (sections paired between 2022 and 2026). **NOT RUN:** full distribution of intervals, bursts by year of birth (year of birth is not in the public logs), and concentration in the last hour; they require re-reading the logs.

| measure | secoes_pareadas | media_2026 | media_2022 | diferenca_media | ep | pct_secoes_com_valor_positivo_2026 | pct_secoes_com_valor_positivo_2022 |
|---|---|---|---|---|---|---|---|
| intervals < 5 s between authorizations, per 100 votes | 12.456 | 0,000 | 0,000 | 0,000 | 0,000 | 0,0 | 0,0 |
| intervals < 10 s between authorizations, per 100 votes | 12.456 | 0,000 | 0,000 | 0,000 | 0,000 | 0,0 | 0,0 |
| minutes of the last vote after nominal closing time | 12.456 | 5,625 | -8,022 | 13,646 | 0,309 | 28,0 | 13,0 |
| votes after nominal time, per 100 votes | 12.456 | 0,215 | 0,091 | 0,124 | 0,030 | 28,0 | 13,0 |

No section, in either year, has two votes with an interval shorter than 10 seconds. The last vote comes after nominal time in 28.0% of sections in 2026 against 13.0% in 2022, which is compatible with the 2nd-round extension decided on 2026-10-25 ([A18](a18-alteracao-no-meio.md), [A5](resultados-fase2.md)).

| test | est_2026T2 | placebos | p_excesso | p_holm | verdict |
|---|---|---|---|---|---|
| association with Lula share (T2, location FE, T1 control): minutes of the last vote after nominal closing time | 0,00001 | 2022/T2 (same sections): -0.00006 (ep 0.00003, p_exc 0.00548) | 0,005 | 0,011 | EXCESS DETECTED (form test, no conversion into votes) |
| association with Lula share (T2, location FE, T1 control): votes after nominal time, per 100 votes | -0,00002 | 2022/T2 (same sections): 0.00009 (ep 0.00010, p_exc 0.837) | 0,837 | 0,837 | NO EXCESS (form test, no conversion into votes) |

> **Caveat.** In the "minutes of the last vote after nominal time" measure, the 2026 coefficient is indistinguishable from zero (0.00001 per minute); the difference for the criterion comes from the negative 2022 coefficient (-0.00006), the only placebo. In the average section, 5.6 minutes of delay add about 0.04 percentage point. The label is formal and **does not indicate manipulation**. The sample is of voting-machine files, not national, so there is no ceiling in votes.

<a id="a22"></a>

## A22. Cross-office coherence

**Failure class covered:** uniform shift restricted to the presidential race, invisible to outlier tests. **Expected trace:** systematic displacement between the presidential candidate's share and the aligned gubernatorial candidate's share in the same section. **No-manipulation prediction:** 2026 displacement equal to 2022 and 2018. **Input used:** TSE coalition tables (2018, 2022, 2026) and the three years' 2nd-round BWebs (votes by candidate and section, president and governor). **Alignment rule** (Addendum 9), decided solely from coalition composition, before looking at votes: a gubernatorial finalist is aligned with a presidential candidate if more than half of the parties in his or her coalition (federations expanded) are in that presidential candidate's coalition and fewer than half are in the other's.

**Result under the registered rule: NOT EXECUTABLE in 2026.** Of the six states with a gubernatorial 2nd round, none had both finalists aligned with different presidential candidates. Reason visible in the composition: the PT's opponent ran for president as a single-party ticket (a one-party coalition), so a governor's coalition rarely passes 50% overlap with his; in AM the PT candidate's coalition has exactly 50%, and the rule requires more than 50%.

| SG_UF | cand1 | alignment 1 | cand2 | alignment 2 | elegivel |
|---|---|---|---|---|---|
| AC | MAILZA ASSIS (PP) | none | ALAN RICK (REPUBLICANOS) | none | False |
| AM | OMAR AZIZ (PSD) | none | PROFESSORA MARIA DO CARMO (PL) | none | False |
| DF | CELINA LEÃO (PP) | none | LEANDRO GRASS (PT) | PT | False |
| ES | LORENZO PAZOLINI (REPUBLICANOS) | none | RICARDO FERRAÇO (MDB) | none | False |
| RN | CADU DE LULA (PT) | PT | ALLYSON (UNIÃO) | none | False |
| TO | VICENTINHO JÚNIOR (PSDB) | none | PROFESSORA DORINHA (UNIÃO) | none | False |

> **Declared deviation (Addendum 9b), written after seeing only the table above and before reading any governor vote.** Exploratory variant: the finalist is aligned with a presidential candidate if his or her **party** is in that finalist's coalition or federation and the other's is not. It stays **outside the main family** and **does not replace** the official NOT EXECUTABLE line.

**Variant 9b.** Displacement S = mean, weighted by presidential valid votes, of (the PT presidential candidate's share) minus (the aligned governor's share); positive means president ahead of governor. Standard error clustered by municipality.

| year | UFs_elegiveis | secoes | votos_validos_pres | S | ep | municipios |
|---|---|---|---|---|---|---|
| 2026 | AM,DF | 15.081 | 3.917.365 | -2,58 p.p. | 2,77 p.p. | 63 |
| 2022 | AM,ES,SC,SP | 133.926 | 34.306.139 | -0,16 p.p. | 0,27 p.p. | 1.080 |
| 2018 |  | 0 | 0 | no eligible state |  |  |

By state (same statistic):

| year | SG_UF | secoes | votos_validos_pres | S |
|---|---|---|---|---|
| 2026 | AM | 8.115 | 2.112.664 | -7,24 p.p. |
| 2026 | DF | 6.966 | 1.804.701 | 2,88 p.p. |
| 2022 | AM | 7.427 | 1.962.447 | 7,90 p.p. |
| 2022 | ES | 9.237 | 2.208.871 | -11,85 p.p. |
| 2022 | SC | 16.228 | 4.399.210 | 1,37 p.p. |
| 2022 | SP | 101.034 | 25.735.611 | -0,03 p.p. |

| test | est_2026T2 | placebos | p_excesso | p_holm | votos_max_pior_caso | pct_pior_caso | verdict |
|---|---|---|---|---|---|---|---|
| PT presidential candidate's share minus the aligned governor's, 2nd round | -2,58 p.p. | 2022/T2: -0.00158 (ep 0.00266, p_exc 0.808) | 0,808 | 0,808 | 169.390 | 3,8% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| opponent's presidential share minus the governor aligned with him (symmetric side), 2nd round | 2,58 p.p. | 2022/T2: 0.00158 (ep 0.00266, p_exc 0.192) | 0,192 | 0,385 | 548.671 | 12,4% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |

> **Reading and limits.** (1) There are only two states in 2026 (AM and DF), and the between-state spread is large in both directions: in the 2022 placebo the per-state displacement goes from -11.8 to +7.9 p.p., and in 2026 from -7.2 to +2.9 p.p. The municipality-clustered standard error (63 municipalities in 2026) **does not capture that between-state variation**; with two states it is not estimable. The 2026 values fall within the 2022 per-state range, but that is description, not a pre-registered test. (2) The ceilings apply **only** to the 3,917,365 valid votes of AM and DF; they do **not** cover the country. They are **worst-case ceilings, not estimates**, and come out large because the test has little power. (3) The sign of S in 2026 is negative (PT candidate behind the aligned governor), which is not the direction of an inflation in his favor. (4) Result: **INCONCLUSIVE**; the official A22 line remains **NOT RUN** (registered rule with no eligible state). **What would close it:** votes per candidate in all offices per section for the 27 states, with an alignment rule defined by someone who knows the local alliances (for example, parties that declared formal support); or federal-deputy votes by party in the states without a gubernatorial 2nd round.

Data: `results/fase3/A22_*.csv`; script `scripts/32_a22_coerencia_cargos.py`; coalition tables in `data/urls_origem.txt` with SHA-256 in `data/sha256_entradas.txt`.

<a id="a23"></a>

## A23. Party observation: NOT RUN

**Failure class covered:** different behavior where a party observer is present or not. **No-manipulation prediction:** no difference between sections with and without an observer, within the same location, with 1st-round and 2022 controls. **How to supply the input (parties and coalitions):** a CSV spreadsheet with the columns `uf;cd_municipio;zona;secao;turno;partido_ou_coligacao;fiscal_presente` (`sim` or `nao`), with no person's name or document, submitted via an issue. The script will compare sections with and without an observer and will publish the result, including if it is null.

<a id="a24"></a>

## A24. Natural experiment of the integrity test: NOT RUN

**Failure class covered:** a voting machine that behaves differently when it is not the test. **Design** (Addenda 8, 9, and 9c): sections whose machine was drawn for the test (voters voted on a backup machine) against the other sections of the same location, with location fixed effect and 1st-round control; comparator: 2022/T2 with the same control; the 2026 1st-round difference without control is the pre-treatment balance. **What was done:** the section list must come from **TRE publications**, one source per state. The survey is in `data/a24_fontes_por_uf.csv`: pages from 9 TREs (SP, SE, SC, PB, MA, MG, MT, ES, DF) were located with news of the draw; **no zone-and-section list was read**, because the TRE sites return 403 to automated access (the project does not disguise its agent to bypass the block) and search summaries give the number of machines, not the table. For the remaining states the page was not located in this round.

**Result:** NOT RUN (Addendum 9 rule: fewer than 10 sections read). The script `scripts/33_a24_teste_integridade.py` is ready and was tested with a synthetic list of 80 random sections, discarded, which served to find and fix a design flaw (Addendum 9c). **How to supply the input:** fill in `data/a24_secoes_teste_integridade.csv` (state, municipality, zone, section, round, test type, biometrics, URL of the TRE publication and access date; one row per section) and run the script; or send the spreadsheet via an issue. **Expected power:** with 20 to 30 sections per state and round and local spread of 1.67 p.p., the test only sees mean differences above about 1 p.p. with 100 sections; the script reports the minimum detectable effect. **Related LAI request:** `lai/03_teste_de_integridade.md`.

**Current coverage: 0 of 27 states.** The test runs with the available states and marks coverage as partial; the author will start with SP, MG, RJ, BA, PR, RS, PE, and CE.

<a id="a25"></a>

## A25. Replaced voting machines (partial)

**Failure class covered:** machine replacement as an intervention point. **Done:** sections with a machine different from the expected one against neighbors in the same location ([A6](resultados-fase2.md)): actual machine different from expected: Lula% in T2 given T1, location FE... REFUTED (no excess, ceiling <1% of the margin). **NOT RUN:** vote before x after the replacement from the logs, because the original machine's record is not public. The total of 1,543 replacements in the 1st round cited to the author has no located source; the press records 421 up to 10 a.m. on 2026-10-04. **Input:** LAI request 01.

<a id="a26"></a>

## A26. Publication integrity

**Failure class covered:** published file altered after publication. **Expected trace:** official hash, size, or modification date different from the first download's. **No-manipulation prediction:** all identical.

**Result (2026-10-29):** of the 233 source files, 233 remain available; the size of 233 equals the first download's; the official hash published today equals the first download's in 224 of 224 checked (0 different); 0 have a modification date later than the first download. **Files altered after publication: 0.** Wayback Machine captures: 41 files have a capture; 151 could not be queried (service rate limit). Of the 63 captures with a 200 response, 54 have the same digest (SHA-1) as the file I downloaded and 9 have a different digest (files the TSE republished after the capture, or partial captures; each case is in `A26_integridade_publicacao.csv`).

**Limit:** the zips (about 8 GB) were not downloaded again; size and published official hash were compared. The full re-check is `data/baixar_e_verificar.sh`. This verifies that what is published today is what was downloaded; it does **not** verify what the TSE published before the first download. Data in `results/fase3/A26_integridade_publicacao.csv`.

### Files republished after the Wayback Machine capture

In 9 captures of 4 files the capture's digest (SHA-1) differs from the file I downloaded. In all of them the modification date published today is later than the capture, which indicates **republication by the TSE after the capture**, and not alteration after my first download (today's size is my download's and the modification date is earlier than my download; these files have no published official hash). To learn whether the republication changed numbers, I compared section by section (President office) the capture with the current file:

| file | modificado_em (GMT) | meu_download | capturas | primeira_captura |
|---|---|---|---|---|
| detalhe_votacao_secao_2026.zip | Mon, 26 Oct 2026 15:35:35 GMT | 2026-10-28T20:05:19 | 3 | 20261007 |
| detalhe_votacao_secao_2022.zip | Fri, 31 Jul 2026 19:47:56 GMT | 2026-10-28T20:05:17 | 2 | 20221105 |
| detalhe_votacao_secao_2018.zip | Thu, 09 Apr 2026 16:48:22 GMT | 2026-10-28T20:39:57 | 3 | 20221105 |
| votacao_candidato_munzona_2026.zip | Wed, 28 Oct 2026 23:14:43 GMT | 2026-10-28T20:40:10 | 1 | 20261010 |

- **detalhe_votacao_secao_2022 (capture of 2022-11-01 against the current file):** 944,150 sections in common, 0 only in the capture, 0 only in the current file. Vote and turnout columns (`QT_*`): **0 differences in 8 columns**. Columns with differences: `NM_TIPO_ELEICAO` (944,150), `DS_ELEICAO` (944,150), `DS_CARGO` (944,150), `NR_LOCAL_VOTACAO` (12,246), `NM_LOCAL_VOTACAO` (404), `DS_LOCAL_VOTACAO_ENDERECO` (32,565). Columns added in the current file: `DT_RECEBIMENTO_BU_HOR_TSE`, `DT_PRIM_TOT_PARCIAL_HOR_TSE`, `DS_ORIGEM_VOTO`, `ST_SECAO_INSTALADA`, `ST_SECAO_ANULADA`, `CD_MODELO_URNA`, `DS_MODELO_URNA`.
- **detalhe_votacao_secao_2018 (capture of 2021-07-14 against the current file):** 908,980 sections in common, 0 only in the capture, 0 only in the current file. Vote and turnout columns (`QT_*`): **0 differences in 8 columns**. Columns with differences: `NR_LOCAL_VOTACAO` (29,538). Columns added in the current file: `NM_LOCAL_VOTACAO`, `DS_LOCAL_VOTACAO_ENDERECO`, `DT_RECEBIMENTO_BU_HOR_TSE`, `DT_PRIM_TOT_PARCIAL_HOR_TSE`, `DS_ORIGEM_VOTO`, `ST_SECAO_INSTALADA`, `ST_SECAO_ANULADA`, `CD_MODELO_URNA`, `DS_MODELO_URNA`.
- **detalhe_votacao_secao_2026 (capture of 2026-10-05 against the current file):** 499,248 sections in common, 0 only in the capture, 499,248 only in the current file. Vote and turnout columns (`QT_*`): **0 differences in 8 columns**. Columns with differences: `NR_LOCAL_VOTACAO` (421), `NM_LOCAL_VOTACAO` (400), `DS_LOCAL_VOTACAO_ENDERECO` (409). Columns added in the current file: none.

Reading: the vote and turnout numbers of the November 2022 capture and of today's file are **identical**; the republication changed labels, the identification of polling locations, and added columns (including the poll-receipt receipt timestamps, which therefore **have no contemporaneous capture** for 2018 and 2022). For 2026, the 2026-10-07 capture covers only the 1st round. Limit: only the President office was compared, and only the files with a Wayback capture.

<a id="a27"></a>

## A27. The 427 new sections with turnout of 95% or more

**Failure class covered:** sections without real voters. **Expected trace:** location without infrastructure, atypical profile, location history. **No-manipulation prediction:** explained by location type and size (already in [H5](resultados-fase1.md)). **Definition:** of the 639 2nd-round sections with turnout ≥ 95%, 427 did not exist in 2022.

| group | secoes | aptos_mediana | pct_local_ja_existia_em_2022 | secoes_no_local_mediana | turnout_t1_medio | turnout_t2_medio | comparecimento | margem_liquida_lula_menos_oponente | pct_lula_validos |
|---|---|---|---|---|---|---|---|---|---|
| new with turnout >= 95% (the 427) | 427 | 139 | 49,9% | 2 | 94,9% | 96,5% | 68.351 | 22.836 | 67,1% |
| new with turnout < 95% | 37.180 | 295 | 80,9% | 7 | 79,6% | 80,1% | 8.288.463 | 668.229 | 54,2% |
| old with turnout >= 95% | 212 | 216 | 99,5% | 1 | 93,4% | 96,0% | 42.419 | 14.901 | 68,1% |
| all counted sections | 497.897 | 327 | 96,1% | 10 | 79,3% | 81,0% | 127.854.631 | 4.401.534 | 51,8% |

Location type, by name and address (% of each group's sections):

| tipo_de_local_pelo_nome_e_endereco | pct_427 | pct_novas_abaixo_95 | pct_todas |
|---|---|---|---|
| escola | 36.5 | 51.5 | 50.1 |
| outro | 33.7 | 39.5 | 43.5 |
| rural_ou_comunidade | 23.7 | 8.2 | 6.2 |
| indigena | 5.9 | 0.6 | 0.2 |
| prisional | 0.2 | 0.2 | 0.0 |
| saude_ou_asilo | 0.0 | 0.1 | 0.0 |

**Reading.** The 427 sections are small (median 139 eligible voters against 327 nationwide), are in locations with few sections, and the 95% turnout already appears in the 1st round (mean 95%). Rural, community, and Indigenous locations are over-represented (23.7% and 5.9% against 6.2% and 0.2% nationwide). Half of them are in locations that already existed in 2022. Lula has 67.1% of the valid votes in them.

**Ceiling.** Net contribution of the 427 sections to the margin: 22,836 margin votes. **Worst-case ceiling, not an estimate:** 44,735 margin votes (1.0% of the margin), if all Lula votes in those sections were invalid. **Status:** TESTED-INCONCLUSIVE. **NOT RUN:** origin of the voter transfers into those sections (requires the nominal registry) and detailed history of the locations. **What would close it:** the per-section transfer list, from the Electoral Justice. Tables in `results/fase3/A27_*.csv`.

<a id="a28"></a>

## A28. Access to information requests (LAI)

Seven requests ready, in `lai/` (07 belongs to A32; 08 is a request template for parties, not an LAI request), with neutral text, no personal data, and no accusation, each with **agency and channel** defined. **None has been filed**; the record of filings, deadlines (20 days, extendable by 10), responses, and denials is in `lai/registro.csv`. Who receives each request and why is in `lai/canais.csv`; the 27 TREs are in `lai/canais_tres.csv`.

| request | subject | agency | channel |
|---|---|---|---|
| `01_urnas_substituidas.md` | Voting machines replaced in 2026 | TSE | TSE Ombudsman's Electronic Form (SIC) |
| `02_codigo_de_carga.md` | Loading code per voting machine | TSE | TSE Ombudsman's Electronic Form (SIC) |
| `03_teste_de_integridade.md` | 2026 integrity and authenticity tests | TSE; TRE of each state | TSE Ombudsman's Electronic Form and each TRE's e-SIC |
| `04_logs_de_totalizacao.md` | Reception and tallying records of 10/04 and 10/25/2026 | TSE | TSE Ombudsman's Electronic Form (SIC) |
| `05_fiscais_credenciados.md` | Accreditation of party observers per section (aggregated data) | TRE of each state; TSE | TSE Ombudsman's Electronic Form and each TRE's e-SIC |
| `06_assinatura_e_chaves.md` | Independent verification of the digital signature of voting-machine files | TSE | TSE Ombudsman's Electronic Form (SIC) |
| `07_ata_e_folha_de_votacao.md` | Tally sheet and signature sheet of 83 sections (A32 and A33) | TRE of each state | each TRE's e-SIC |

**State of channel verification.** The TSE and the TREs block automated access (403). The TSE channel (Ombudsman's Electronic Form, TSE Resolution 23.435/2015, amended by 23.583/2018) was checked in a search result, without opening the form; for the TREs there is a SIC page seen in a search result for 6 states (SP, BA, AM, GO, RJ, AP) and the other 21 are marked **to be confirmed at filing**. Identification of the requester is required (CNJ Resolution 215/2015, art. 11, § 2, according to TRE-SP); the project has no named author, so whoever files signs the request. Confirm the channel, the fields, and the deadline in the system when filing.


<a id="a31"></a>

## A31. Municipalities extreme in the 1st-to-2nd-round transfer (Silva Jardim/RJ allegation)

**Allegation.** In Silva Jardim/RJ, in the 2026 2nd round against the 1st, "Flávio +1, Lula +964, -104 voters" would be impossible without manipulation. **Question.** Does this reproduce in the data? And, compared with all municipalities in four elections, is it unusual? **Pre-registration:** [Addendum 10, 10a, and 10b](preregistro.md); 10b (supplementary analysis) was written after seeing the main model's result and is marked as post-hoc.

**1. The allegation reproduces in part.** Silva Jardim BWeb data (61 sections). The opponent's gain (**+1**) and the turnout change (**-104**: it is 2nd-round turnout minus 1st-round; eligible voters change +3, not -104) reproduce. Lula's gain in the data is **+984**, not +964: a 20-vote difference I could not explain (it may be a typo in the allegation or another source). The 1st-round third-party votes (897) and blank and null votes (630 in the 1st round, 438 in the 2nd) close the account: the **pool** (Lula's gain plus the opponent's gain) is 985, equal to third parties plus blank and null of the 1st round, plus the turnout change, minus blank and null of the 2nd.

| quantity | T1 | T2 | T2 minus T1 |
|---|---|---|---|
| aptos | 18.674 | 18.677 | 3 |
| turnout | 14.909 | 14.805 | -104 |
| Lula (13) | 4.450 | 5.434 | 984 |
| Flavio Bolsonaro (22) | 8.932 | 8.933 | 1 |
| third parties (sum) | 897 | 0 | -897 |
| blank and null | 630 | 438 | -192 |

_1st-round third parties in the municipality (votes):_ Renan Santos (14) 209; Hertz Dias (16) 5; Edmilson Costa (21) 2; Clariana Barão (27) 8; Zema (30) 20; Wilson Grassi (35) 3; Caiado (55) 290; Cury (70) 353; Samara Martins (80) 7.


**2. Distribution of the pool fraction that goes to the PT** (f = PT gain / (PT gain + opponent gain), municipalities with a pool of at least 20 votes; f leaves [0, 1] when one of the two loses votes between rounds, which is common).

| year | municipalities | national f | median | decile 1 | decile 9 | % outside [0, 1] | Silva Jardim: f | percentile | municipalities with f farther from the median |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | 5.357 | 0,737 | 0,734 | 0,540 | 1,066 | 13,7% | 0,999 | 86 | 948 |
| 2022 | 5.255 | 0,302 | 0,243 | -0,070 | 0,545 | 12,9% | 0,370 | 73 | 2.788 |
| 2018 | 5.491 | 0,645 | 0,596 | 0,397 | 0,872 | 2,7% | 0,716 | 69 | 3.030 |
| 2014 | 5.505 | 0,411 | 0,369 | 0,011 | 0,630 | 10,7% | 0,456 | 66 | 3.755 |

In 2026 there are 5,571 municipalities, one more than in the other years (5,570): TSE code 73709, in MT, appears only in 2026 (it does not exist in the 2022 data). **Confirmed:** it is **Boa Esperança do Norte/MT**, created by state Law 7,264, of 2000-03-29, split off from Sorriso and Nova Ubiratã (13 sections: 5 came from Sorriso, 4 from Nova Ubiratã, and 4 are new), with creation validated by the STF on 2023-10-06 (ADPF 819, 8 votes to 3) and installation on 2025-01-01, with the first mayor elected in 2024. The name comes from the TSE table used in A20; the law and the installation, from secondary sources (the MT Legislative Assembly and the press), **without checking the installation date in a primary act**. Left out of the distribution are municipalities with a pool below 20 votes (214 in 2026) and, per Addendum 10a, municipalities with a section counted in only one of the rounds (2018: 6; 2014: 1; 2022 and 2026: none; list in `results/fase3/A31_excluidos.csv`).

**What the table shows.** Silva Jardim is at the 86th percentile in 2026 and 948 municipalities have f farther from the median than its. More important: **the pattern "the opponent gains almost nothing between rounds" is common in 2026 and rare in the other years.** Of the 5,357 eligible municipalities, 748 (14.0%) had the opponent with +1 vote or fewer, and 149 of them with the PT gaining 900 votes or more; in 2022 there were 8 (0.15%), in 2018 90 (1.6%), and in 2014 64 (1.2%) (S2, descriptive, post-hoc). The national pool fraction that went to the PT was 0.737 in 2026, 0.302 in 2022, 0.645 in 2018, and 0.411 in 2014. The 2026 election has the shape of 2018 (the PT captures most of the pool), with the difference that in 2026 the opponent lost absolute votes in more municipalities. This describes the election; it does not explain why; the national accounting (a drop of 1.82 million blank and null votes and of 2.96 million in abstention, which add up to more than the third-party capture) is in [Phase 2, A3 and A11](resultados-fase2.md).

**3. Null model.** Per year, regression of f on **1st-round** regressors (turnout fraction for the PT, the opponent, blank and null, abstention, and the composition of the third parties: in 2026 the bloc that backed Flávio and Renan Santos; in 2022 and 2018 the largest and second-largest third party, without inferring endorsements; in 2014 only the total) with state fixed effect, weighted by the variance (binomial of the pool plus a real between-municipality heterogeneity, calibrated by the robust scale of the residual). The tail comes from a Student's t distribution with degrees of freedom estimated in the **other three years**; Holm correction. **The turnout change between rounds does not enter the profile**, because it is a 2nd-round outcome.

| year | municipalities | heterogeneity (tau²) | degrees of freedom (t) | critical z value (absolute) for 5,570 comparisons | municipalities with Holm < 0.05 |
|---|---|---|---|---|---|
| 2026 | 5.357 | 0,0086 | 2,76 | 83 | 3 |
| 2022 | 5.255 | 0,0199 | 2,73 | 86 | 0 |
| 2018 | 5.491 | 0,0085 | 2,43 | 135 | 0 |
| 2014 | 5.505 | 0,0366 | 2,52 | 116 | 0 |

**Limit of the test, stated plainly.** The estimated tails are very heavy (about 2.4 to 2.8 degrees of freedom), because f is unstable when the pool is small and the gross flows are large and of opposite signs. The critical value lands at |z| of 83 to 135: **the main model has almost no power to reject small municipalities.** That is why the conclusion about Silva Jardim does not rest on the Holm cut, but on z: its is 1.13, ordinary under any reference.

**Silva Jardim, pre-registered result: WITHIN THE EXPECTED TAIL.** f = 0.999; the model, with the municipality's 1st-round profile, predicts 0.894; the residual is 0.105 (z = 1.13); two-sided p 0.35; Holm 1.00 (also with 5,570 comparisons: 1.00). **Gain spread across sections:** the 3 sections with the largest Lula gain have 8.8% of the total gain (the 3 with the largest pool have 8.9% of the pool); Addendum 10's concentration rule classifies it as **spread**. **Worst-case ceiling, not an estimate:** 207 margin votes (0.005% of the margin), if everything the model does not explain in Silva Jardim were manipulation (factor 2); beyond the expected tail: 0. Addendum 10's no-manipulation prediction (within the tail, spread gain, explained by the 1st-round profile) **is fulfilled**.

_Reading of f_hat: in the 1st round, Flávio had 60% of Silva Jardim's turnout and the bloc that backed him in the 2nd round (Zema, Caiado, Cury, Clariana) had 4.5%. The model does not predict a low f for that profile: it estimates 0.89, because in 2026 f is high in most municipalities (median 0.73). This is a reading of the distribution, not an explanation of voter behavior._

**4. Independent-coin model: demonstration that it is inadequate.** Each pool voter goes to the PT with probability p0, independently. In three variants of p0 (0.5; the municipality's 1st-round PT/(PT+opponent) ratio; the national ratio):

| year | national pool | observed PT | expected PT (p0 = 0.5) | coin z | rejects the national result? | municipalities rejected (Holm 5%, p0 = 0.5) |
|---|---|---|---|---|---|---|
| 2026 | 14.095.433 | 10.339.213 | 7.047.716 | 1.753 | yes | 85% |
| 2022 | 10.246.841 | 3.144.361 | 5.123.420 | -1.236 | yes | 82% |
| 2018 | 23.759.956 | 15.334.145 | 11.879.978 | 1.417 | yes | 70% |
| 2014 | 27.340.477 | 11.251.847 | 13.670.238 | -925 | yes | 78% |

**Result.** The coin model rejects the national result of **every** election, 2022 included, in every variant (|z| from 925 to 3,237), and rejects 70% to 93% of municipalities in every year and variant (positive pool; municipalities where one of the candidates lost votes, 14% in 2026, do not even fit in the model). A criterion that declares "impossible" the result of an election no one contests as impossible does not distinguish the normal from the abnormal. This shows that the criterion is inadequate; it does **not** validate or invalidate the result of any election. Under the coin model, the chance of the opponent having +1 vote or fewer in Silva Jardim would be between 10^-294 and 10^-468, depending on the variant. That is the kind of probability the model computes for most municipalities (70% to 93% are rejected), so it does not separate Silva Jardim from the rest.

**5. The 20 most extreme municipalities of 2026** (largest |z| of the main model, in either direction).

| # | municipality | UF | pool | dL | dF | f | f_hat | z | Holm | model verdict | gain | dominant third party in the 1st round |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ITACOATIARA | AM | 55 | 1.114 | -1.059 | 20,25 | 2,46 | 188 | 0,005 | OUTSIDE THE TAIL, NO PRECEDENT | spread | Cury |
| 2 | SANTO ANTÔNIO DE LISBOA | PI | 48 | -350 | 398 | -7,29 | 1,00 | -87 | 0,041 | OUTSIDE THE MODEL TAIL, WITH PRECEDENT | not applicable (sum of dL or pool <= 0) | Renan Santos |
| 3 | RAFAEL GODEIRO | RN | 34 | 314 | -280 | 9,24 | 1,16 | 84 | 0,045 | OUTSIDE THE MODEL TAIL, WITH PRECEDENT | spread | Renan Santos |
| 4 | ITAMARATI | AM | 27 | 210 | -183 | 7,78 | 2,47 | 55 | 0,148 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 5 | RUY BARBOSA | RN | 30 | 183 | -153 | 6,10 | 1,11 | 52 | 0,173 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 6 | ORIXIMINÁ | PA | 270 | 1.575 | -1.305 | 5,83 | 1,19 | 50 | 0,193 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 7 | BELO MONTE | AL | 136 | -304 | 440 | -2,24 | 1,15 | -36 | 0,471 | WITHIN THE EXPECTED TAIL | not applicable (sum of dL or pool <= 0) | Cury |
| 8 | ACORIZAL | MT | 23 | 119 | -96 | 5,17 | 0,82 | 36 | 0,490 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 9 | PEDRO AVELINO | RN | 46 | 202 | -156 | 4,39 | 1,20 | 34 | 0,576 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 10 | LAGOA DA CONFUSÃO | TO | 57 | 257 | -200 | 4,51 | 1,45 | 32 | 0,638 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 11 | AFONSO BEZERRA | RN | 83 | 344 | -261 | 4,14 | 1,17 | 32 | 0,682 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 12 | MANGARATIBA | RJ | 367 | 1.397 | -1.030 | 3,81 | 0,93 | 31 | 0,739 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 13 | NINA RODRIGUES | MA | 74 | 294 | -220 | 3,97 | 1,34 | 28 | 0,952 | WITHIN THE EXPECTED TAIL | spread | Caiado |
| 14 | PORTEL | PA | 176 | 637 | -461 | 3,62 | 1,24 | 26 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 15 | AXIXÁ DO TOCANTINS | TO | 50 | 195 | -145 | 3,90 | 1,51 | 25 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 16 | CACHOEIRA DO PIRIÁ | PA | 62 | 223 | -161 | 3,60 | 1,24 | 25 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 17 | TENENTE ANANIAS | RN | 70 | 243 | -173 | 3,47 | 1,19 | 24 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Cury |
| 18 | SANTA ROSA DO TOCANTINS | TO | 30 | 115 | -85 | 3,83 | 1,52 | 24 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Caiado |
| 19 | NOVA IORQUE | MA | 27 | 97 | -70 | 3,59 | 1,36 | 23 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Caiado |
| 20 | AXIXÁ | MA | 54 | 185 | -131 | 3,43 | 1,31 | 22 | 1,000 | WITHIN THE EXPECTED TAIL | spread | Cury |

**Reading.** (i) **Three of the 20 fall outside the main model's tail** (Holm < 0.05): Itacoatiara/AM, Santo Antônio de Lisboa/PI, Rafael Godeiro/RN. Itacoatiara/AM is the only one without precedent in the other years; the other two have 1 comparable municipality in the other three years. (ii) **All 20 have a small pool (up to 367 votes) and gross flows of 5.5 to 39.5 times the pool**: a large gain by one candidate and a nearly equal loss by the other, and f becomes a ratio of small numbers. In Itacoatiara, for example, Lula +1,114, Flávio -1,059 and turnout -2,783, with a pool of 55; f = 20.3 is an artifact of the division. In the supplementary per-eligible-voter statistic (item 7), Itacoatiara becomes ordinary. (iii) **Gain spread across sections** in 18 of the 20; in the other 0 the sum of dL or of the pool is negative and the rule does not apply. No municipality has the gain concentrated in a few sections. (iv) **Dominant 1st-round third party:** Cury in 15, Caiado in 3, Renan Santos in 2. Declared 2nd-round endorsement: Cury and Caiado backed Flávio; Renan Santos released his voters ([sources and name-by-name check in A11](resultados-fase2.md)). **What these 20 have in common:** turnout fell between rounds in all of them (from -59 to -2,783 votes) and, in 18 of them, the PT gained and the opponent lost a similar number of votes; the small pool is the difference between two large flows. What explains this (selective abstention, vote switching, or something else) **is not in the aggregate data**; printed poll-receipts and per-section authorization lists could clarify it. (v) **Comparison with 2022:** 6 of the 20 were also among the 5% most extreme of 2022 (|z| above the 95th percentile), 4 of them in the opposite direction to 2026; 10 were not eligible in 2022 (pool smaller than 20). Municipalities with large gross flow and small pool appear as extreme in different elections; that is volatility of those municipalities, not a feature of 2026.

**Worst-case ceiling, not an estimate (factor 2), 20 most extreme:** 1,151 margin votes beyond the expected tail (0.026% of the margin); 13,327 margin votes (0.30% of the margin) if **everything** the model does not explain in those 20 municipalities were manipulation, without discounting normal variation. No scenario with these municipalities approaches the 4,430,191-vote margin.

**6. Check against printed poll-receipts.** `results/fase3/A31_silva_jardim_secoes.csv` lists Silva Jardim's 61 sections with eligible voters, turnout, Lula, Flávio, each third party, blank and null in the 1st and 2nd rounds, plus empty columns for the printed value, in the format accepted by `scripts/04_cruza_bu_impresso.py`. To check against printed BUs, ask the local party directories and party observers through the [collection page](boletins-impressos.md). **NOT RUN:** the project has no printed BU from Silva Jardim.

**7. Supplementary analysis (post-hoc, exploratory, Addendum 10b; does not replace the main line).** Since f is unstable with a small pool, repeated with well-conditioned statistics: each candidate's gain per 1st-round eligible voter, with the same regressors and state fixed effect, residual standardized within size deciles. Silva Jardim in 2026: PT z = 0.01 and opponent z = -2.13; Holm 1.00 and 1.00: **ordinary**, in all four years (opponent z from -2.17 to -0.29). Lighter tail (about 6 to 8 degrees of freedom; critical |z| of 10 to 13). In 2026, 1 municipality falls outside the tail by this measure: Marechal Thaumaturgo/AC (opponent z -10.4: the opponent lost 1,352 votes); worst-case ceiling beyond the tail: 136 margin votes (0.003% of the margin). Itacoatiara/AM, the first of the main model, has z of -1.97 and -1.60 in this measure: ordinary.

**Status.** Silva Jardim: TESTED, WITHIN THE EXPECTED TAIL (in both methods). Three small municipalities fall outside the main model's tail by the artifact of the ratio with a small pool (gross flows of 15 to 40 times the pool); in the supplementary measure another municipality (Marechal Thaumaturgo/AC) falls outside the tail, with a ceiling below 0.01% of the margin: **TESTED-INCONCLUSIVE** for those, because the explanation (municipalities with a strong turnout drop between rounds) cannot be checked without the printed poll-receipts and the authorization lists. **What would close it:** printed BUs of Silva Jardim, Itacoatiara, Santo Antônio de Lisboa, and Rafael Godeiro; the per-section turnout change between rounds in those municipalities. **What the test does not do:** it does not identify whom each voter voted for, does not prove or rule out manipulation in any municipality; it applies to the shape of the distribution across municipalities. Tables in `results/fase3/A31_*.csv`; code in `scripts/35_a31_transferencia_municipal.py`.

<a id="a12b"></a>

## A12b. The allegation "106 voting machines with 100% for Lula and 0% blank, null, and Flávio"

**Pre-registration:** [Addendum 12](preregistro.md), written before computing the probabilities. **Allegation.** The image claims that 106 voting machines gave 100% to Lula and 0% blank, null, and Flávio.

**1. Count.** Of the **106** sections with zero votes for Flávio in 2026/T2 (A12's count; none has zero turnout), **29** (27%) also have zero blank and zero null. The other 77 have blank or null votes. Across the 106: 24 blank and 338 null, 2.4% of the turnout of 15,222 voters. **"0% blank and null" does not hold for the set of 106**, only for 29. These are small sections (median turnout 128; median eligible voters 161); the 29 with triple zero are even smaller (median 56 voters, against 139).

**2. Where they are.** By location type (A27 classification by location name) and by state:

| location type | sections | with zero blank and null | median turnout |
|---|---|---|---|
| escola_outro | 55 | 11 | 103,0 |
| indigena | 41 | 15 | 145,0 |
| prisional | 2 | 1 | 21,5 |
| quilombola | 1 | 1 | 54,0 |
| rural_comunidade | 7 | 1 | 68,0 |

| UF | sections | with zero blank and null | Lula votes |
|---|---|---|---|
| AC | 3 | 0 | 386 |
| AM | 30 | 1 | 6.477 |
| BA | 4 | 1 | 215 |
| CE | 2 | 1 | 86 |
| ES | 1 | 1 | 41 |
| MA | 20 | 4 | 2.068 |
| MG | 2 | 0 | 116 |
| MS | 1 | 1 | 56 |
| MT | 5 | 3 | 813 |
| PA | 16 | 10 | 1.733 |
| PB | 1 | 1 | 10 |
| PE | 1 | 0 | 227 |
| PI | 1 | 1 | 16 |
| PR | 1 | 0 | 314 |
| RO | 1 | 0 | 104 |
| RR | 8 | 4 | 1.207 |
| RS | 2 | 1 | 104 |
| TO | 7 | 0 | 887 |

The 106 are in 18 states, concentrated in AM (30), MA (20), and PA (16); 41 are in Indigenous locations. For each one: state, municipality, location type, eligible voters, turnout, Lula votes, blank, null, result in the 2026 1st round and in the same section in 2022: `results/fase3/A12b_106_secoes.csv`.

**3. Expected.** For each section, the probability of zero blank and zero null is (1 - r)^n, with n the section's own turnout and r the blank-and-null rate of the **other sections of the same location** (of the municipality, if the location has only one section or few voters). The expected number is the sum; the exact p comes from the Poisson-binomial distribution. Series, with the zero-opponent sections of each election (A12's "all counted" definition):

| year | round | zero-opponent sections | observed triple zero | expected (location rate) | p (observed or more) | expected (municipality rate) | observed / expected |
|---|---|---|---|---|---|---|---|
| 2014 | 1 | 709 | 23 | 19,9 | 0,219 | 19,7 | 1,15 |
| 2014 | 2 | 194 | 28 | 22,6 | 0,084 | 22,8 | 1,24 |
| 2018 | 1 | 674 | 61 | 27,2 | < 0,001 | 16,9 | 2,24 |
| 2018 | 2 | 328 | 42 | 19,2 | < 0,001 | 16,0 | 2,19 |
| 2022 | 1 | 161 | 39 | 23,2 | < 0,001 | 16,9 | 1,68 |
| 2022 | 2 | 143 | 29 | 20,8 | 0,018 | 18,9 | 1,39 |
| 2026 | 1 | 81 | 28 | 17,0 | < 0,001 | 10,1 | 1,65 |
| 2026 | 2 | 106 | 29 | 20,4 | 0,009 | 17,0 | 1,42 |

**Reading.** Addendum 12's prediction (observed close to expected) **is not fulfilled literally**: in 2026/T2 there are 29 triple-zero sections against 20.4 expected (p = 0.009; with the municipality rate, p < 0.001). **But the excess over expected exists in every election and has a similar ratio in 2022 (T2 1.39) and a larger one in 2018 (T2 2.19) than in 2026 (1.42)**, including in the 1st rounds. One possible explanation, **not tested here**: sections with zero votes for the opponent are small and unanimous locations, where blank and null may be less frequent than among neighbors; if so, it is a limitation of the expected value, not a feature of 2026. What the series shows is only that the excess is not specific to 2026.

**4. Unanimous sections and the difference between the claims.**

| year | round | set (sections with 30 valid votes or more) | sections | with zero blank and null | % with zero blank and null | median blank and null (% of turnout) |
|---|---|---|---|---|---|---|
| 2026 | 2 | 100% of valid votes for the PT | 103 | 26 | 25,2 | 1,52 |
| 2026 | 2 | 100% of valid votes for the opponent | 4 | 1 | 25,0 | 1,87 |
| 2022 | 2 | 100% of valid votes for the PT | 130 | 23 | 17,7 | 1,88 |
| 2022 | 2 | 100% of valid votes for the opponent | 2 | 0 | 0,0 | 3,08 |

The original report said "100% of valid votes" (unanimous sections with 30 valid votes or more, [report page](relatorio-original.md)): 103 PT sections in 2026/T2. **"100% of valid votes" admits blank and null above zero; "0% blank and null" is a stronger claim.** And 106 (zero votes for Flávio, any size) is not the same set as 103 (unanimous with 30 valid or more). Among the 103, 26 have zero blank and null.

**5. Ceiling, in margin votes (worst-case ceiling, not an estimate).** Lula votes in the 106 sections: **14,860**. (i) If all were invalid (as in A27, factor 1): **14,860 margin votes (0.34% of the margin)**. (ii) If those votes were switched, by what neighboring sections would give the opponent (2,700 expected votes; factor 2): **5,401 margin votes (0.12% of the margin)**. No scenario with these sections approaches the 4,430,191-vote margin.

**Status.** TESTED: the "0% blank and null" allegation does not reproduce for the set (only for part of it); the triple-zero excess over expected is general and not specific to 2026. **What the test does not do:** it does not show why small, unanimous sections have fewer blank and null votes (vote secrecy, the profile of the locations, or something else); it only shows that this occurs in every election. Code: `scripts/36_a12b_zero_brancos_nulos.py`; tables: `results/fase3/A12b_*.csv`.

<a id="a32"></a>

## A32. Manual voter release as a channel for local abuse

**Pre-registration:** [Addendum 11, 11a, 11b, 11c, and 11d](preregistro.md). 11a and 11b were written before counting any burst; **11c and 11d were written after seeing results** (that of item 3 and that of the registered bursts) and are marked as post-hoc where they appear.

**Coverage (declared).** Voting-machine logs read: **53,242 section-days** (12,554 sections with a 2022 log and 14,067 with a 2026 log, each log containing both days), the A4/A5/A21 section sample plus **all** Roraima sections; the 2nd-round log contains the 1st round's events. **NOT RUN:** the logs of all sections of both years (about 1 million files, in public zips of tens of GB per state); year of birth: **NOT EXECUTABLE** (the log does not record date of birth and the project does not extract voter or poll-worker identifiers). A section-day enters the measures only if the log closes with the BU turnout (within 5%) and has 100 authorizations or more (51,829 of 53,242). Extractor validation: the log's manual fraction has a 0.994 correlation with the BWeb manual rate in Roraima.

### 1. Full A21: authorization sequence, bursts, and last hour

**How long each authorization type takes** (interval, in seconds, **preceding** each authorization; national aggregate of the sample, without identifying the section):

| year | round | authorization type | n | p1 | p5 | p25 | median | p75 | p95 |
|---|---|---|---|---|---|---|---|---|---|
| 2022 | 1st round | manual | 222.269 | 93 | 104 | 128 | 153 | 192 | 326 |
| 2022 | 1st round | biometric | 2.612.759 | 51 | 59 | 74 | 91 | 119 | 223 |
| 2022 | 2nd round | manual | 220.651 | 67 | 77 | 97 | 121 | 169 | 390 |
| 2022 | 2nd round | biometric | 2.695.045 | 31 | 36 | 48 | 65 | 108 | 328 |
| 2026 | 1st round | manual | 226.947 | 97 | 108 | 131 | 156 | 197 | 329 |
| 2026 | 1st round | biometric | 3.220.613 | 54 | 62 | 78 | 95 | 125 | 247 |
| 2026 | 2nd round | manual | 242.710 | 66 | 76 | 97 | 123 | 179 | 410 |
| 2026 | 2nd round | biometric | 3.325.892 | 29 | 34 | 46 | 63 | 116 | 358 |

**Bursts under the registered definition (Addendum 11).** k or more consecutive manual releases, with all intervals below the 5th percentile of the section-day's own intervals (k = 3 and 5).

| year | round | section-days | % manual | bursts k=3 | % sections with burst k=3 | % expected k=3 (permutation) | bursts k=5 | % expected k=5 (permutation) |
|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | 12.022 | 6,3 | 0 | 0,0 | 0,11 | 0 | 0,00 |
| 2022 | 2 | 12.375 | 6,1 | 0 | 0,0 | 0,09 | 0 | 0,00 |
| 2026 | 1 | 13.644 | 6,2 | 0 | 0,0 | 0,05 | 0 | 0,00 |
| 2026 | 2 | 13.788 | 6,4 | 0 | 0,0 | 0,06 | 0 | 0,00 |

**Result: no burst, in any year, day, or k.** **But this is not a finding of absence of abuse: the registered design cannot see bursts by construction** (Addendum 11d). A manual release takes a median of 121 to 156 s (the shortest interval preceding a manual one, at the 1st percentile, is 66 s), against 63 to 95 s for a biometric one; the 5th percentile of the intervals of all the section's authorizations falls below the minimum time of a manual one. The permutation, which ignores this physical limit, would expect 7 to 13 section-days with a k = 3 burst per year and day against 0 observed; that difference measures the physical limit, not chance nor abuse. Therefore the association models of bursts with turnout and vote **are not estimable** (no variation): **NOT EXECUTABLE**, official line. The "no abuse" prediction (same frequency between years, no association) can be neither contradicted nor confirmed by this measure.

**Fraction of manual releases in the last hour** (60 minutes before nominal closing), against the fraction of **all** authorizations in the last hour:

| year | round | manual in the last hour | all authorizations in the last hour | difference (manual minus all) | standard error |
|---|---|---|---|---|---|
| 2022 | 1 | 10,3% | 12,8% | -2,5 p.p. | 0,1 p.p. |
| 2022 | 2 | 4,8% | 5,7% | -0,9 p.p. | 0,1 p.p. |
| 2026 | 1 | 9,7% | 11,7% | -2,0 p.p. | 0,1 p.p. |
| 2026 | 2 | 4,4% | 5,2% | -0,9 p.p. | 0,1 p.p. |

Manual releases **do not concentrate at the end of the day**: their fraction in the last hour is smaller than that of authorizations in general, in both years and both rounds. This contradicts the "with abuse" prediction (end-of-day concentration).

**Post-hoc supplementary measure (Addendum 11d): clustering of manual releases**, k or more consecutive manual releases in arrival order, with no time condition, against the exact expectation by permutation of the labels (the probability of at least one cluster uses the Poisson approximation, declared).

| year | round | % sections with cluster k=3 | % expected k=3 | observed/expected k=3 | % sections with cluster k=5 | % expected k=5 | observed/expected k=5 |
|---|---|---|---|---|---|---|---|
| 2022 | 1 | 15,13 | 12,22 | 1,20 | 1,42 | 0,79 | 1,66 |
| 2022 | 2 | 13,33 | 11,45 | 1,14 | 1,00 | 0,72 | 1,27 |
| 2026 | 1 | 10,00 | 8,23 | 1,19 | 0,25 | 0,14 | 1,35 |
| 2026 | 2 | 10,72 | 9,11 | 1,14 | 0,25 | 0,16 | 1,23 |

**2026 frequency against 2022, in the same sections** (section fixed effect, standard error clustered by municipality; difference in proportion points of sections with a cluster):

| round | k | sections in both years | 2026 minus 2022 (p.p.) | standard error | z | p |
|---|---|---|---|---|---|---|
| 1st round | 3 | 11.762 | -5,19 | 3,71 | -1,40 | 0,163 |
| 1st round | 5 | 11.762 | -1,16 | 0,38 | -3,01 | 0,003 |
| 2nd round | 3 | 12.240 | -2,60 | 3,61 | -0,72 | 0,472 |
| 2nd round | 5 | 12.240 | -0,76 | 0,29 | -2,65 | 0,008 |

Clusters are **less** frequent in 2026 than in 2022 (z difference of -3.0 and -2.65 for k = 5, still significant with Holm over the four rows; not significant for k = 3), and the observed/expected ratio is similar in both years (1.1 to 1.7): manual releases arrive slightly closer together than in random order, in both years. The "with abuse" prediction (more in 2026 than in 2022) **is not fulfilled**.

**Association of clustering with turnout and vote** (2nd round, location fixed effect, 1st-round control; placebo: 2022). **Main (k = 5, random sample R plus Roraima): NOT EXECUTABLE**, because there is almost no cluster of 5 in that sample (insufficient variation). Sensitivity, k = 3:

| sample | outcome | coefficient 2026 | standard error 2026 | coefficient 2022 (placebo) | standard error 2022 | sections |
|---|---|---|---|---|---|---|
| main: R + full Roraima | turnout | 0,0031 | 0,0040 | -0,0006 | 0,0036 | 1.467 |
| main: R + full Roraima | Lula share | 0,0002 | 0,0031 | -0,0010 | 0,0041 | 1.467 |
| sensitivity: all strata (selected on the outcome) | turnout | 0,0025 | 0,0006 | 0,0027 | 0,0006 | 11.318 |
| sensitivity: all strata (selected on the outcome) | Lula share | -0,0003 | 0,0006 | 0,0006 | 0,0007 | 11.318 |

No coefficient is distinguishable from zero nor from the 2022 placebo (a coefficient of 0.003 is 0.3 percentage point). Without a main family, **there is no ceiling in margin votes nor a Holm verdict for item 1**. **M3, descriptive** (2022 → 2026 change in 2nd-round turnout against 2026 clustering, location fixed effect):

| sample | k | coefficient | standard error | p | sections |
|---|---|---|---|---|---|
| main: R + full Roraima | 3 | 0,0004 | 0,0054 | 0,946 | 1.144 |
| all strata (selected on the outcome) | 3 | -0,0012 | 0,0010 | 0,234 | 10.217 |
| all strata (selected on the outcome) | 5 | -0,0116 | 0,0057 | 0,041 | 10.217 |

The only row with p < 0.05 (k = 5, all strata, selected on the outcome, few clusters) has a **negative** coefficient (-1.2 p.p. of turnout), the opposite of what the abuse hypothesis would predict, and without multiple-comparison correction.

### 2. Sections with extreme manual voter release (BWeb, all sections)

| year | round | cut | valid sections | extreme | % of sections | voters in them | median turnout | mean electorate age (median), extreme | same, all sections | UFs |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | > 30% | 470.914 | 6.056 | 1,286 | 1.268.638 | 217 | 47,5 | 44,4 | 26 |
| 2022 | 1 | > 50% | 470.914 | 595 | 0,126 | 134.653 | 239 | 45,1 | 44,4 | 24 |
| 2022 | 2 | > 30% | 470.896 | 3.995 | 0,848 | 844.612 | 216 | 47,6 | 44,4 | 25 |
| 2022 | 2 | > 50% | 470.896 | 317 | 0,067 | 71.512 | 241 | 46,1 | 44,4 | 24 |
| 2026 | 1 | > 30% | 497.769 | 391 | 0,079 | 79.917 | 223 | 48,3 | 46,0 | 21 |
| 2026 | 1 | > 50% | 497.769 | 138 | 0,028 | 32.196 | 238 | 45,5 | 46,0 | 17 |
| 2026 | 2 | > 30% | 497.750 | 348 | 0,070 | 73.003 | 223 | 49,2 | 46,0 | 20 |
| 2026 | 2 | > 50% | 497.750 | 97 | 0,019 | 23.050 | 234 | 46,3 | 46,0 | 16 |

**Count and reading.** Manual release above 30% of voters: **3,995 sections in the 2022 2nd round and 348 in 2026's**; above 50%, 317 against 97. **The phenomenon is much smaller in 2026 than in 2022**, and the electorate of those sections is about 3 years older than the others' (mean age, median: 47.6 against 44.4 in 2022; 49.2 against 46.0 in 2026). By state (30% cut, 2nd round), the largest counts:

| UF | 2022 T1 | 2022 T2 | 2026 T1 | 2026 T2 |
|---|---|---|---|---|
| BA | 1348 | 922 | 75 | 80 |
| RS | 959 | 499 | 58 | 61 |
| CE | 427 | 344 | 37 | 25 |
| PI | 498 | 302 | 18 | 23 |
| SP | 270 | 148 | 32 | 23 |
| MG | 356 | 264 | 22 | 20 |
| PA | 98 | 40 | 18 | 17 |
| PR | 188 | 115 | 35 | 16 |

By location type (30% cut, 2nd round; A27 classification by name): escola_outro 3778 in 2022 and 331 in 2026; indigena 5 in 2022 and 0 in 2026; rural_comunidade 212 in 2022 and 17 in 2026. No section in Indigenous, prison, quilombola, hospital, or military locations has extreme manual release in 2026.

**Turnout and vote against the other sections of the same location (2nd round, extreme > 30%).** Turnout: 0.01 p.p. (location standard error 0.24) in 2026 against -0.48 p.p. (0.09) in 2022. Lula share (valid votes): 0.38 p.p. (0.28) in 2026 against 0.34 p.p. (0.08) in 2022; with the 1st-round control (T1 → T2 change), Lula 0.11 p.p. (0.13) in 2026 and 0.18 p.p. (0.04) in 2022. Differences of tenths of a percentage point, **with no difference between years in the vote**. The T1 → T2 turnout change of those sections against the neighbors is +0.89 p.p. in 2026 (standard error 0.17) and +0.49 p.p. in 2022 (0.05): a small excess (less than 1 point over a turnout of about 80%) and with no counterpart in Lula's share.

### 3. Ceiling in margin votes of the manual-release excess over what age predicts

Model of the 2nd-round manual rate **fitted on 2022** (weighted least squares by voters; regressors: age composition of the section's electorate, registered biometrics, and state fixed effect), applied to 2026. **The 2022 model predicts more manual release in 2026 than observed**: 11,615,994 predicted voters against 8,629,826 observed (8.63 million, the same "8.6 million" the original report cites); the manual rate **fell**, did not rise. Excess per section = max(0, observed - predicted) x voters.

| year | sections | observed manual | predicted manual | (a) sum of positive excesses | (b) beyond 1.645 of the 2022 deviation | (c) after removing the national shift | (c) and beyond 1.645 deviation |
|---|---|---|---|---|---|---|---|
| 2022 (in-sample, reference) | 470.651 | 10.009.455 | 10.009.455 | 2.679.836 | 564.492 | 3.363.368 | 750.129 |
| 2026 | 497.474 | 8.629.826 | 11.615.994 | 709.152 | 55.862 | 1.852.233 | 123.866 |

**Registered ceiling (the largest of Addendum 11's four numbers, factor 1, worst-case ceiling, not an estimate): 1,852,233 margin votes (41.8% of the margin).** **Post-result reading (Addendum 11c): this number is inflated by construction.** Variant (c) removes the national shift (median residual: -2.7 p.p.), and since the shift is **downward** in 2026, removing the shift **adds** 2.7 p.p. to each section. The readings that make sense here: (a) 709,152 margin votes (16.0% of the margin), which includes model noise (the same sum within the 2022 sample, on which the model was fitted, is 2,679,836, **3.8 times larger**); (b) what exceeds 1.645 of the 2022 residual deviation: **55,862 margin votes (1.26% of the margin)**, in 5,818 sections, against 564,492 in 2022. None of the readings is an estimate: they assume all excesses in favor of a single side.

The **50 sections with the largest excess** in 2026/2nd round (observed manual release of 64% to 99%, predicted of 6% to 15%; 26 in Bahia, 5 in SP, 5 in RJ, and 5 in PR; polling locations in schools, one in a rural community) add up to 10,612 excess voters (0.24% of the margin). List, with the criterion for each: `lai/07_secoes.csv` (which also includes, after them, the 33 sections of A33's 20 extreme schools, 83 in total). There is no explanation in the data for those values; **nor is there an association with the vote** (sections with more than 50% manual: Lula 0.05 p.p., standard error 0.21, against neighbors in the same location, with 1st-round control).

### 4. Log integrity

In the sample read, the log's hash **appears in the list signed by the voting machine** (A4) in **12,554 of 12,554 2022 sections and 14,067 of 14,067 2026 sections** (100%). This says the log is what the machine listed; **verifying the list's signature (pending, A18)** is what closes the hypothesis of log alteration after the machine. While pending, what holds is "the log is what the machine listed", not "the log is authentic".

### 5. Paper documents

Texts ready, **none filed**: LAI request to the TREs ([`lai/07_ata_e_folha_de_votacao.md`](https://github.com/baduba/eleicoes-dossie-2026/blob/main/lai/07_ata_e_folha_de_votacao.md)) for the 50 sections above (copy of the tally sheet and the signature sheet **with personal data redacted**, or, if that is not possible, the counts of signatures, of manual-authorization notes, and of voters from the tally sheet), and a party request template to the electoral registry office (`lai/08_modelo_requerimento_partidos.md`, to be reviewed by an election lawyer; the retention period of section documents is **to be confirmed**). **Fixed test, NOT RUN until there are documents:** signature-sheet signatures x tally-sheet voters x BU turnout x log authorizations, per section, with `scripts/37_confere_ata.py`, which lists any discrepancy (including trivial ones, such as a counting error).

**Status.** TESTED-INCONCLUSIVE (item 1 without a measure capable of seeing bursts; item 3 with a registered ceiling of 1,852,233 margin votes, inflated, and 55,862 beyond the noise). **Summary of what the data show:** manual voter release **fell** from 2022 to 2026, extreme sections are **far fewer** in 2026, manual releases do **not** concentrate at the end of the day, there are **no** more clusters in 2026, and there is **no** association with turnout or vote. **What would close it:** logs of all sections (for the national distribution), verification of the log signatures, and the tally sheet and signature sheet of the listed sections. **What the test does not do:** it does not identify voters or poll workers; manual release has legitimate uses (unrecognized fingerprint, voter without registered biometrics, elderly voter); the excess over the age model is not fraud, it is only what the 2022 model does not predict. Code: `scripts/38` to `scripts/41` and `scripts/37_confere_ata.py`; tables: `results/fase3/A32_*.csv`.

<a id="a31b"></a>

## A31b. The municipalities where the opponent gained +1 vote or fewer between rounds

**Pre-registration:** [Addendum 13](preregistro.md), written before running the simulation and the profile. **Question.** In A31 we saw that 748 of 5,357 2026 municipalities (14.0%) had the opponent's gain between rounds less than or equal to +1 vote, against 0.15% in 2022, 1.6% in 2018, and 1.2% in 2014. Is that what would be expected from the opponent's national growth in 2026 (6.8%, against 14%, 17%, and 46% in the comparison years)?

**1. Expected fraction under the national shift.** For each comparison year, each municipality's opponent growth (gain / 1st-round vote) is shifted, within the state, to the same state's growth rate in 2026 and applied to the 2026 base. Fraction of municipalities with gain less than or equal to +1:

| comparison year | paired municipalities | fraction in its own year, unshifted | expected (paired) | expected (resampling, mean) | resampling 2.5% | resampling 97.5% |
|---|---|---|---|---|---|---|
| 2022 | 5.356 | 0,2% | 14,7% | 15,4% | 14,6% | 16,1% |
| 2018 | 5.350 | 1,6% | 13,2% | 13,9% | 13,1% | 14,6% |
| 2014 | 5.356 | 1,2% | 55,0% | 54,9% | 53,4% | 56,1% |

**Observed in 2026: 14.0%.** The within-state shift with 2022 gives 14.7% (resampling 14.6% to 16.1%) and with 2018, 13.2% (13.1% to 14.6%). **Pre-registered verdict: COMPATIBLE WITH THE NATIONAL SHIFT.** The 14.0% fraction is what 2018 and 2022 would produce if the opponent had grown in each state what he grew in 2026; the 55% obtained with 2014 only shows that that year's 46% growth is too distant to serve as a comparison (the extrapolation is large). **Limitation:** the shift equalizes each state's mean growth; it does not guarantee that the distribution shape of 2018 and 2022 is that of 2026. This shows that **the number 748 is not, by itself, an anomaly**; it does not say why the opponent grew little in 2026.

**2. Profile of the 748** (descriptive, confounded by region and size):

| region | municipalities with dF <= 1 | others | % of the group | % of the others | ratio | % of the region's municipalities with dF <= 1 |
|---|---|---|---|---|---|---|
| Center-West | 21 | 443 | 2,8 | 9,6 | 0,3 | 4,5 |
| Northeast | 547 | 1191 | 73,1 | 25,8 | 2,8 | 31,5 |
| North | 157 | 141 | 21,0 | 3,1 | 6,9 | 52,7 |
| Southeast | 19 | 1647 | 2,5 | 35,7 | 0,1 | 1,1 |
| South | 4 | 1187 | 0,5 | 25,8 | 0,0 | 0,3 |

| size (eligible voters) | municipalities with dF <= 1 | others | % of the size's municipalities with dF <= 1 |
|---|---|---|---|
| 20 to 100 thousand | 152 | 959 | 13,7 |
| 5 to 20 thousand | 418 | 2249 | 15,7 |
| up to 5 thousand | 175 | 1183 | 12,9 |
| over 100 thousand | 3 | 218 | 1,4 |

States with 15 or more of these municipalities (% of the state's municipalities): AM 23 (79%); TO 69 (77%); MA 146 (76%); AL 70 (71%); RN 77 (47%); PA 58 (47%); PI 95 (47%); PB 65 (29%); CE 48 (26%); SE 17 (23%); MT 17 (12%); PE 17 (9%). **94% of the 748 are in the Northeast and North; practically none in the South, Southeast, and Center-West.**

Continuous measures (median of the 748 against the others'): opponent's 1st-round share **26.2% against 49.0%**; PT share **65.1% against 39.1%**; third parties 3.8% against 5.9%; T1 → T2 turnout change **-1.2% against 2.7%**; 2nd-round manual release 6.9% against 7.7%; eligible voters 9,172 against 9,415. By voting-machine model (mean fraction of the municipality's sections): UE2022 47% against 36%, UE2020 42% against 41%, UE2015 9% against 20%; moderate differences, with no clear pattern and confounded by region. **Reading (description, not explanation):** these are Northeast and North municipalities where the PT was strong in the 1st round, the opponent had a small share, and turnout fell between rounds; this test does not show why the opponent grew little there.

**3. Decomposition by turnout change.**

| group | municipalities | % | opponent's net loss (votes) | sum of turnout change |
|---|---|---|---|---|
| turnout fell (dC < 0) | 528 | 70,6 | 57.376 | -157.683 |
| turnout rose or unchanged (dC >= 0) | 220 | 29,4 | 12.683 | 37.322 |
| lower bound of vote switching by net balance > 0 | 290 | 38,8 | 15.635 |  |

Of the 748, **528 (70.6%) had a turnout drop** (compatible with selective abstention) and **220 (29.4%) had equal or higher turnout** (a stagnant opponent would require new voters to go to the PT or vote switching). In sum, the opponent lost 70,048 net votes (out of 3,001,176 in the 1st round), Lula gained 498,842, and turnout fell 120,361. The **lower bound of vote switching by net balance** (the opponent's loss that does not fit in a net turnout drop nor in an increase of blank and null) is positive in 290 municipalities and adds up to **15,635 votes**. **The net balance does not distinguish vote switching from selective abstention:** an opponent voter who abstains and a new PT voter cancel out in the net.

**4. The 20 municipalities with the largest absolute opponent loss** (1st-round turnout of 1,000 or more):

| UF | municipality | turnout T1 | opponent T1 | opponent T2 minus T1 | PT T2 minus T1 | turnout T2 minus T1 |
|---|---|---|---|---|---|---|
| AP | MACAPÁ | 270.534 | 124.378 | -3.785 | 11.300 | -19.220 |
| AC | SENA MADUREIRA | 24.661 | 16.640 | -2.292 | -293 | -3.773 |
| AC | TARAUACÁ | 22.603 | 12.435 | -2.135 | -370 | -3.491 |
| AC | CRUZEIRO DO SUL | 51.482 | 34.218 | -2.069 | 694 | -4.200 |
| RR | RORAINÓPOLIS | 19.054 | 13.503 | -1.389 | 241 | -2.254 |
| RJ | CAMPOS DOS GOYTACAZES | 290.458 | 160.859 | -1.389 | 24.822 | -3.898 |
| AM | MANACAPURU | 64.079 | 27.295 | -1.354 | 902 | -3.088 |
| AC | MARECHAL THAUMATURGO | 9.352 | 5.369 | -1.352 | -659 | -2.301 |
| AP | SANTANA | 73.177 | 35.791 | -1.350 | 2.786 | -5.320 |
| PA | ORIXIMINÁ | 39.198 | 17.678 | -1.305 | 1.575 | -2.096 |
| AC | FEIJÓ | 18.156 | 9.069 | -1.257 | -58 | -1.966 |
| RR | CARACARAÍ | 12.452 | 8.598 | -1.226 | -106 | -2.032 |
| RR | CANTÁ | 14.635 | 10.037 | -1.209 | 248 | -1.742 |
| AM | COARI | 38.141 | 14.023 | -1.190 | 961 | -1.379 |
| PA | BREVES | 61.897 | 20.877 | -1.136 | 808 | -4.505 |
| AM | ITACOATIARA | 58.385 | 20.163 | -1.059 | 1.114 | -2.783 |
| RJ | MANGARATIBA | 34.080 | 20.418 | -1.030 | 1.397 | -1.882 |
| AC | RODRIGUES ALVES | 10.218 | 7.154 | -997 | -162 | -1.477 |
| RR | ALTO ALEGRE | 11.347 | 7.951 | -989 | 91 | -1.517 |
| AP | MAZAGÃO | 18.989 | 6.402 | -983 | -1.135 | -3.393 |

All sections of these 20 municipalities, with T1 and T2 and empty columns for the printed BU: `results/fase3/A31b_20_secoes.csv` (format of `scripts/04_cruza_bu_impresso.py`); ask the local party directories and party observers through the [collection page](boletins-impressos.md). **NOT RUN:** the project has no printed BU from these municipalities. Itacoatiara/AM, Marechal Thaumaturgo/AC, Oriximiná/PA, and Mangaratiba/RJ already appeared in A31.

**5. Ceiling, in margin votes (worst-case ceiling, not an estimate, factor 2).** (A) If the entire 748's deficit relative to the opponent's growth in the state were vote switching from Flávio to Lula: **234,746 margin votes (5.30% of the margin)**. (B) The excess of (A) over what the national shift would reproduce: **0**, because the deficit simulated with 2022 (289,343) and with 2018 (669,527) is larger than observed. Under Addendum 14's display rule, G3 plots neither (A) (it is only the bound of the total deficit, without discounting what national growth explains) nor (B), which is zero.

**Status.** TESTED-INCONCLUSIVE. The fraction is compatible with the national shift; the profile is regional and of a strong-PT electorate; most have a turnout drop. **The test does not distinguish vote switching from selective abstention.** **What would close it:** printed BUs and authorization lists of the 20 municipalities, or abstention by band and section of the same. Code: `scripts/42_a31b_dflavio_menor_igual_1.py`; tables: `results/fase3/A31b_*.csv`.

<a id="a32b"></a>

## A32b. Manual-release bursts with an absolute threshold

**Pre-registration:** [Addendum 14](preregistro.md), written before running. **Reason.** Addendum 11d showed that the registered burst definition (intervals below the section's 5th percentile) cannot see bursts, because a manual release takes longer than that. **New definition, fixed in advance:** in each section-day with 10 manual releases or more, the threshold is **1.5 times the median of the interval preceding the section-day's own manual releases**; **burst of k** = k or more consecutive manual releases, **with no biometric authorization between them**, with all intervals between consecutive authorizations within the threshold. k = 3 (main) and k = 5 (sensitivity). Expected: the same exact calculation by permutation of the labels (the Poisson approximation for the probability of at least one burst is that of Addendum 11b).

**Coverage.** Section-days with a consistent log and 10 manual releases or more: 2022 T1: 9,200 of 12,022 (median threshold 225 s); 2022 T2: 9,011 of 12,375 (median threshold 178 s); 2026 T1: 10,814 of 13,644 (median threshold 234 s); 2026 T2: 11,071 of 13,788 (median threshold 186 s).

| year | round | section-days | % with burst k=3 | % expected k=3 | observed/expected k=3 | % with burst k=5 | % expected k=5 | observed/expected k=5 |
|---|---|---|---|---|---|---|---|---|
| 2022 | 1 | 12.022 | 15,80 | 14,76 | 1,00 | 1,16 | 0,84 | 1,29 |
| 2022 | 2 | 12.375 | 15,21 | 12,93 | 1,15 | 0,92 | 0,68 | 1,19 |
| 2026 | 1 | 13.644 | 9,33 | 9,34 | 0,97 | 0,18 | 0,14 | 1,12 |
| 2026 | 2 | 13.788 | 10,46 | 8,81 | 1,16 | 0,16 | 0,13 | 1,18 |

(percentages over all section-days with a consistent log; those without 10 manual releases have no threshold and count as having no burst.)

**2026 frequency against 2022, in the same sections** (section fixed effect, standard error clustered by municipality):

| round | k | sections in both years | 2026 minus 2022 (p.p.) | standard error | z | p |
|---|---|---|---|---|---|---|
| 1st round | 3 | 7.868 | -6,67 | 4,02 | -1,66 | 0,097 |
| 1st round | 5 | 7.868 | -1,00 | 0,35 | -2,88 | 0,004 |
| 2nd round | 3 | 7.965 | -4,12 | 4,14 | -0,99 | 0,320 |
| 2nd round | 5 | 7.965 | -0,80 | 0,28 | -2,84 | 0,005 |

**Reading.** The observed/expected ratio is 1.0 to 1.2 in 2022 and in 2026 for k = 3 (0.9 to 1.4 in the main sample): manual releases arrive with the clustering frequency that random order gives, in both years. **Bursts are less frequent in 2026 than in 2022** (minus 4 to 7 proportion points at k = 3, not significant; minus 0.8 to 1.0 at k = 5, z of -2.8). The "with abuse" prediction (more bursts in 2026, above expected) **is not fulfilled**.

**Association with turnout and vote** (2nd round; location fixed effect; 1st-round control; 2022 placebo; main sample = random stratum plus all of Roraima; A32b family with its own Holm):

| test | coef. 2026 | ep 2026 | coef. 2022 (placebo) | ep 2022 | p (excess) | p (Holm) | ceiling, margin votes | % of the margin | verdict |
|---|---|---|---|---|---|---|---|---|---|
| manual-release burst (k = 3) and turnout: 2026/T2 against 2022/T2 (location FE, T1 control) | 0,0000 | 0,0043 | -0,0088 | 0,0064 | 0,127 | 0,127 | 3.391.360 | 76,6 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| manual-release burst (k = 3) and Lula share: 2026/T2 against 2022/T2 (location FE, T1 control) | -0,0024 | 0,0034 | -0,0120 | 0,0037 | 0,027 | 0,055 | 4.405.076 | 99,4 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |

**The 2026 coefficients are indistinguishable from zero** (turnout 0.0000, standard error 0.0043; Lula share -0.0024, 0.0034); the excess test against the 2022 placebo lands at Holm of 0.055 (Lula share) and 0.13 (turnout), and the difference comes from the 2022 placebo being **negative** (-0.009 and -0.012), not from a positive coefficient in 2026. **But the ceiling is useless:** the main sample with 10 manual releases or more has only 523 sections, the standard error is large, and the extrapolated ceiling (3,391,360 to 4,405,076 margin votes, 77% to 99% of the margin) comes from lack of power, not from an effect; that is why **it is not plotted in G3** (display rule, CHANGELOG) and stays only here. In the variant with the national median as the threshold (sensitivity), the family gives the same verdict (INCONCLUSIVE, ceilings of 88% to 90% of the margin). In the sample with all strata (selected on the outcome, labeled), the k = 3 coefficients are 0.0024 (turnout) and -0.0003 (Lula), with standard error 0.0007, and the 2022 placebo is similar: **no association**.

**Status.** TESTED-INCONCLUSIVE for lack of power in the association; in what the test measures (frequency and clustering), **there is no excess in 2026**: there are fewer bursts than in 2022. **What would close it:** logs of all sections (to have power) and verification of the log signatures. **What the test does not do:** the absolute definition measures clustering in time, not what each release was. Code: `scripts/43_a32b_rajadas_limiar_absoluto.py`; tables: `results/fase3/A32_rajadas_*_abs*.csv`.

<a id="a33"></a>

## A33. Manual release at the school level (polling location)

**Pre-registration:** [Addendum 15](preregistro.md) and [Addendum 15a](preregistro.md) (correction of the ceiling's exposure, written after seeing the first run, which had an error of mine, and before running the corrected version). **Question.** Does manual release, looked at by school rather than by section or municipality, associate with a Lula gain or a turnout gain between rounds, more in 2026 than in the placebos? Unit: school (state, municipality, zone, and location), which gives mass to locations with several sections.

**1. Descriptive by manual-rate band (labeled as descriptive and confounded: the manual rate depends on age and on the voting-machine model, and small schools vary more).**

| year | manual rate | schools | secoes | voters | Lula votes | Flávio votes | schools with Lula ahead | % with Lula ahead | mean age (median) |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | up to 5% | 21.939 | 130.433 | 35.324.187 | 17.658.216 | 16.465.233 | 12.957 | 59,1 | 42,9 |
| 2026 | 5 to 10% | 51.170 | 302.518 | 77.680.090 | 38.403.418 | 36.775.545 | 28.771 | 56,2 | 45,8 |
| 2026 | 10 to 20% | 16.983 | 59.989 | 14.293.276 | 7.656.070 | 6.210.757 | 10.622 | 62,5 | 47,5 |
| 2026 | 20 to 30% | 917 | 1.386 | 282.320 | 170.264 | 104.013 | 568 | 61,9 | 48,8 |
| 2026 | 30 to 50% | 56 | 96 | 19.616 | 12.065 | 6.918 | 37 | 66,1 | 49,7 |
| 2026 | over 50% | 4 | 5 | 780 | 593 | 168 | 3 | 75,0 | 45,8 |
| 2022 | up to 5% | 24.404 | 159.428 | 45.414.479 | 21.457.140 | 21.761.820 | 13.144 | 53,9 | 42,5 |
| 2022 | 5 to 10% | 29.410 | 165.281 | 43.209.827 | 20.376.049 | 20.840.131 | 15.917 | 54,1 | 44,4 |
| 2022 | 10 to 20% | 27.411 | 124.291 | 30.955.977 | 15.590.124 | 14.049.283 | 16.460 | 60,0 | 44,9 |
| 2022 | 20 to 30% | 6.244 | 16.640 | 3.759.218 | 2.356.958 | 1.242.890 | 4.720 | 75,6 | 45,7 |
| 2022 | 30 to 50% | 1.078 | 1.547 | 315.038 | 227.385 | 74.548 | 889 | 82,5 | 46,2 |
| 2022 | over 50% | 30 | 39 | 7.384 | 4.811 | 2.275 | 20 | 66,7 | 45,8 |

Schools with more than 20% manual release: **977 in 2026 against 7,352 in 2022**. The 2026 distribution is much more compressed in the 5% to 10% band.

**2. Test with unit = school** (zone fixed effect; controls for mean age and 1st-round PT vote; 2022 and 2018 placebos; symmetry with the opponent; municipality-fixed-effect variant as robustness):

| variant | outcome | year | FE | coef | ep | n |
|---|---|---|---|---|---|---|
| school manual rate | change in Lula share (T2 minus T1) | 2026 | zona | -0,0168 | 0,0030 | 90.986 |
| school manual rate | change in Lula share (T2 minus T1) | 2022 | zona | -0,0019 | 0,0020 | 88.519 |
| school manual rate | change in Lula share (T2 minus T1) | 2018 | zona | -0,0209 | 0,0047 | 88.354 |
| school manual rate | change in Lula share (T2 minus T1) | 2026 | municipio | -0,0071 | 0,0031 | 90.798 |
| school manual rate | change in Lula share (T2 minus T1) | 2022 | municipio | -0,0027 | 0,0021 | 88.297 |
| school manual rate | change in Lula share (T2 minus T1) | 2018 | municipio | -0,0162 | 0,0068 | 88.130 |
| school manual rate | change in turnout (T2 minus T1) | 2026 | zona | -0,0235 | 0,0042 | 90.986 |
| school manual rate | change in turnout (T2 minus T1) | 2022 | zona | 0,0029 | 0,0028 | 88.519 |
| school manual rate | change in turnout (T2 minus T1) | 2018 | zona | 0,0113 | 0,0038 | 88.354 |
| school manual rate | change in turnout (T2 minus T1) | 2026 | municipio | -0,0110 | 0,0043 | 90.798 |
| school manual rate | change in turnout (T2 minus T1) | 2022 | municipio | 0,0046 | 0,0030 | 88.297 |
| school manual rate | change in turnout (T2 minus T1) | 2018 | municipio | 0,0053 | 0,0033 | 88.130 |
| school manual rate | change in opponent votes per eligible voter | 2026 | zona | -0,0026 | 0,0032 | 90.986 |
| school manual rate | change in opponent votes per eligible voter | 2022 | zona | -0,0007 | 0,0020 | 88.519 |
| school manual rate | change in opponent votes per eligible voter | 2018 | zona | 0,0220 | 0,0034 | 88.354 |
| school manual rate | change in PT votes per eligible voter | 2026 | zona | -0,0370 | 0,0042 | 90.986 |
| school manual rate | change in PT votes per eligible voter | 2022 | zona | -0,0048 | 0,0026 | 88.519 |
| school manual rate | change in PT votes per eligible voter | 2018 | zona | 0,0053 | 0,0067 | 88.354 |
| excess over the same school in the previous year | change in Lula share (T2 minus T1) | 2026 | zona | -0,0007 | 0,0019 | 84.275 |
| excess over the same school in the previous year | change in Lula share (T2 minus T1) | 2022 | zona | -0,0006 | 0,0018 | 83.911 |
| excess over the same school in the previous year | change in turnout (T2 minus T1) | 2026 | zona | 0,0022 | 0,0026 | 84.275 |
| excess over the same school in the previous year | change in turnout (T2 minus T1) | 2022 | zona | -0,0013 | 0,0025 | 83.911 |

Excess-test family (2026 against the most demanding placebo; Holm over the family):

| test | coef. 2026 | ep 2026 | placebo | coef. placebo | p (excess) | p (Holm) | ceiling, margin votes | % of the margin | verdict |
|---|---|---|---|---|---|---|---|---|---|
| change in Lula share (T2 minus T1), PT: 2026 against 2022 and 2018 (school manual rate, zone FE) | -0,0168 | 0,0030 | 2022/T2 | -0,0019 | 1,000 | 1,000 | 221.830 | 5,0 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| change in Lula share (T2 minus T1), opponent (symmetry): 2026 against 2022 and 2018 (school manual rate, zone FE) | 0,0168 | 0,0030 | 2018/T2 | 0,0209 | 0,770 | 1,000 | 346.914 | 7,8 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| change in turnout (T2 minus T1), PT: 2026 against 2022 and 2018 (school manual rate, zone FE) | -0,0235 | 0,0042 | 2018/T2 | 0,0113 | 1,000 | 1,000 | 0 | 0,0 | REFUTED (no excess, ceiling <1% of the margin) |
| change in Lula share (T2 minus T1), PT: 2026 against 2022 (excess over 2022 of the same school, zone FE) | -0,0007 | 0,0019 | 2022/T2 (against 2018) | -0,0006 | 0,521 | 1,000 | 68.414 | 1,5 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| change in Lula share (T2 minus T1), opponent (symmetry): 2026 against 2022 (excess over 2022 of the same school, zone FE) | 0,0007 | 0,0019 | 2022/T2 (against 2018) | 0,0006 | 0,479 | 1,000 | 72.911 | 1,6 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| change in turnout (T2 minus T1), PT: 2026 against 2022 (excess over 2022 of the same school, zone FE) | 0,0022 | 0,0026 | 2022/T2 (against 2018) | -0,0013 | 0,167 | 1,000 | 98.984 | 2,2 | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |

**Reading.** In 2026, the higher a school's manual rate, the **smaller** Lula's gain between rounds (negative coefficient, same sign as the 2018 placebo and distinct from 2022's, which is close to zero) and the smaller the turnout. The "with a scheme" prediction (excess Lula gain and turnout only in 2026) **is not fulfilled**; the smallest excess p is 0.17, before Holm, and the symmetry with the opponent has the opposite sign, as the identity requires. The ceilings in this table (0 to 8% of the margin) come from the coefficient's uncertainty multiplied by the exposure, not from an effect, and for that reason **are not plotted in G3** (display rule, CHANGELOG). The simplest reading of the negative sign is composition: schools with much manual release are more rural and older, and the mean-age control does not exhaust that. A negative association does not prove absence of manipulation in a smaller subset; it is only incompatible with the broad pre-registered pattern.

**3. Extreme schools** (top 1% in manual-release excess over what age and the 2022-fitted machine model predict, and above the school itself in 2022 or absent in 2022):

910 schools in the top 1% (excess cut of 9.2 percentage points); 661 listed after the 2022 filter (of which 87 with no equivalent location in 2022), with 1,079 sections and 225,927 voters. Full list: `results/fase3/A33_escolas_extremas.csv`. **Ceiling** (all manual-release excess read as votes in favor of a single side, factor 1): 29,654 margin votes (0.67% of the margin); above the model noise (1.645 sigma): 8,125 margin votes (0.18%). **Worst-case ceiling, not an estimate.**

| pos. | SG_UF | municipality | location | sections | voters T2 | manual 2026 | predicted by age | manual 2022 | mean age | Lula T1 | Flávio T1 | Lula T2 | Flávio T2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MA | ANAJATUBA | ESCOLA MUNICIPAL PAULO DE JESUS PEREIRA | 1 | 129 | 82% | 9% | 9% | 41 | 124 | 11 | 118 | 9 |
| 2 | BA | GLÓRIA | (no name in the TSE table) | 1 | 155 | 74% | 10% | 5% | 43 | 126 | 9 | 142 | 11 |
| 3 | CE | JAGUARIBE | CENTRO SOCIAL MARIETA CALS | 2 | 388 | 62% | 14% | 32% | 59 | 263 | 58 | 309 | 68 |
| 4 | CE | CAMOCIM | CENTRO DE ESPECIALIDADES ODONTOLOGICAS - CEO | 2 | 373 | 47% | 9% | 21% | 42 | 193 | 139 | 217 | 144 |
| 5 | PR | TOMAZINA | SECRETARIA MUNICIPAL DE EDUCAÇÃO | 3 | 610 | 46% | 8% | 5% | 46 | 187 | 342 | 240 | 357 |
| 6 | BA | TANQUE NOVO | PRÉDIO ESCOLAR JOSÉ ONÓRIO | 3 | 709 | 48% | 11% | 10% | 42 | 561 | 70 | 606 | 79 |
| 7 | RS | NOVA BOA VISTA | SALAO DA COMUNIDADE LINHA MIRIM | 1 | 108 | 51% | 15% | 14% | 49 | 16 | 74 | 24 | 80 |
| 8 | RS | OSÓRIO | E E F METODISTA NEHYTA RAMOS | 3 | 654 | 40% | 11% | 11% | 54 | 263 | 266 | 324 | 306 |
| 9 | BA | BOM JESUS DA SERRA | CRECHE MUNICIPAL FONTE DO SABER | 2 | 427 | 37% | 10% | n/d | 32 | 317 | 76 | 334 | 88 |
| 10 | SP | PEDREGULHO | EMEI LEIDE EMÍLIA COMODARO DE OLIVEIRA | 3 | 802 | 35% | 8% | 3% | 45 | 314 | 342 | 412 | 342 |
| 11 | BA | PARATINGA | IGREJA DA BARAUNAS | 1 | 138 | 36% | 9% | 2% | 41 | 102 | 19 | 112 | 24 |
| 12 | RS | COTIPORÃ | ESCOLA ESTADUAL JACINTO SILVA | 4 | 1.194 | 37% | 11% | 14% | 48 | 200 | 802 | 273 | 891 |
| 13 | MA | SÃO JOSÉ DE RIBAMAR | ESCOLA MUNICIPAL SÃO FRANCISCO | 1 | 122 | 32% | 7% | n/d | 35 | 56 | 38 | 68 | 49 |
| 14 | PR | TOMAZINA | CENTRO MUNICIPAL DE EDUCAÇÃO INFANTIL | 4 | 773 | 35% | 10% | 6% | 50 | 262 | 412 | 294 | 450 |
| 15 | RS | VISTA GAÚCHA | SALÃO DA COMUNIDADE DE TIRADENTES | 1 | 118 | 31% | 6% | 29% | 50 | 45 | 59 | 50 | 65 |
| 16 | MA | VIANA | ESCOLA MUNICIPAL BEIJAMIM COSTA | 1 | 129 | 30% | 7% | n/d | 42 | 104 | 14 | 118 | 11 |
| 17 | MG | SÃO GONÇALO DO RIO ABAIXO | ESCOLA MUNICIPAL DE SÃO JOSÉ | 2 | 486 | 33% | 10% | 4% | 49 | 244 | 173 | 284 | 186 |
| 18 | SC | CERRO NEGRO | NUCLEO MUNICIPAL ORIVAL DE OLIVEIRA BRANCO | 1 | 197 | 31% | 8% | 24% | 49 | 95 | 85 | 112 | 82 |
| 19 | RS | HULHA NEGRA | CÂMARA DE VEREADORES DE HULHA NEGRA | 1 | 260 | 31% | 8% | 9% | 43 | 107 | 125 | 119 | 131 |
| 20 | BA | SÃO FRANCISCO DO CONDE | LUZIENE AMÁLIA SANTOS ROCHA | 3 | 713 | 31% | 9% | n/d | 45 | 578 | 52 | 637 | 56 |

**Reading.** The extreme schools **are not explained by age** (mean age of 32 to 59 years in the top 20, predicted 6% to 15%, observed 30% to 82%): the excess exists, but it is small in votes, because **92% have 3 sections or fewer** and the median is 1 section. They are in states on both sides (BA, MA, and CE; RS, SC, PR, and SP), and the mean change in Lula's share between rounds in them is +1.5 points, **less** than the +3.0 points of the national per-school average. A single section with 82% manual release and nearly identical T1 and T2 (Anajatuba/MA) resembles a biometric-reader defect, an operational hypothesis that the machine log and the printed BU confirm or rule out; **it is not a conclusion**. All sections of the top 20, with T1 and T2 and empty columns for the printed BU: `results/fase3/A33_20_escolas_secoes.csv` (40 sections); they are included in LAI request 07 and in the [BU collection](boletins-impressos.md).

**4. Synchrony in the logs** (schools with 3 or more sections with a consistent log; fraction of manual events of sections of the same school falling in the same 60 s and 180 s window, against null N1 = manual labels shuffled within the section itself, preserving the pace, and N2 = pairs of different schools of the same state; 2022 against 2026):

Coverage (partial logs, see A32): 2022 T1: 1,182 schools (27 states); 2022 T2: 1,197 schools (27 states); 2026 T1: 1,261 schools (27 states); 2026 T2: 1,263 schools (27 states).

| year | round | window (s) | schools | coincident pairs | expected (N1) | ratio | z |
|---|---|---|---|---|---|---|---|
| 2022 | 1 | 60 | 1.182 | 129.408 | 123.671 | 1,05 | 12,3 |
| 2022 | 1 | 180 | 1.182 | 350.319 | 330.667 | 1,06 | 25,2 |
| 2022 | 2 | 60 | 1.196 | 156.635 | 141.255 | 1,11 | 29,6 |
| 2022 | 2 | 180 | 1.196 | 399.575 | 367.310 | 1,09 | 38,1 |
| 2026 | 1 | 60 | 1.261 | 127.026 | 121.023 | 1,05 | 13,1 |
| 2026 | 1 | 180 | 1.261 | 353.485 | 332.400 | 1,06 | 27,0 |
| 2026 | 2 | 60 | 1.263 | 177.252 | 160.785 | 1,10 | 29,3 |
| 2026 | 2 | 180 | 1.263 | 460.970 | 426.752 | 1,08 | 34,2 |

**Reading.** There is a small synchrony in **both years** (ratio of 1.05 to 1.11 in 2022; 1.05 to 1.10 in 2026), with high z because there are millions of events. It is the same size in both years (in 2026 it is equal or smaller), and null N2 gives ratios of 1.04 to 1.08 in both years: sections of the same school share queue, peak time, and poll workers, which explains a small synchrony. **There is no 2026 synchrony above 2022's**, which was the "with a scheme" prediction.

**Status.** TESTED-INCONCLUSIVE. Three of the four "no scheme" predictions are fulfilled (no excess over the placebos, even though the 2026 coefficient is more negative than 2022's; no synchrony above 2022; extreme schools small in votes). The fourth, "extremes explained by age", is **not** fulfilled, and that remains open. The test does not see what each manual release was. **What would close it:** printed BU, authorization list, and tally sheet of the 20 schools (LAI 07), and the logs of all sections. Code: `scripts/44_a33_escolas.py`; tables: `results/fase3/A33_*.csv`.
