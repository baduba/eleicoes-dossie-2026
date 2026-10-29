# Phase 2 Results (A1 to A10)

Forecasts, criteria and placebos were recorded in [Addendum 4 of the pre-registration](preregistro.md) **before** running the analyses. The test register is combined with that of Phase 1 (38 tests); the corrected p-value (Holm and Benjamini-Hochberg) is over the full family. Verdict: rule of [Addendum 2](preregistro.md). Official margin: 4,430,191 votes. Ceilings in votes are upper bounds under causality, not estimates.

**Quick read.** Four analyses (A1, A2, A3 and A12) left the pre-registered criterion with an excess label and carry a **design caveat**: the same test flags excess in series or years without manipulation. The original result was kept and the corrected version is shown alongside (next section). No excess label in these rows indicates manipulation.

## Rows with a design caveat (read first)

> **Four rows (A1, A2, A3 and A12) left the pre-registered criterion with the "excess" label. In all of them, the pre-registered design had a flaw that produces this label without manipulation.** Below, for each one: the flaw, the demonstration (the same original test flagging "excess" in series or years without manipulation) and the corrected version, published **alongside** the original result, which was neither altered nor deleted. The correction is **post-registration**: [Addendum 6](preregistro.md), written before running the corrected versions.

| test | design flaw | demonstration (original test without manipulation) | pre-registered (kept) | corrected (post-registration) |
|---|---|---|---|---|
| A1 count curve | the "permutation within the state (UF)" null assumes a random order within the state; municipalities arrive in blocks | 4 of 4 real elections leave the envelope, and 20 of 20 simulations without manipulation do as well | EXCESS DETECTED (shape test, no conversion to votes) (**design caveat**) | NO EXCESS (shape test, no conversion to votes) |
| A2 T1→T2 transitions | the per-role placebo (opponent) ignores who led the first round and how many third-party votes there were | the same test applied to the **2022 PT** (first-round leader; loses votes in 12.6% of sections) also flags: EXCESS DETECTED (shape test, no conversion to votes) | EXCESS DETECTED (shape test, no conversion to votes) (**design caveat**) | NO EXCESS (shape test, no conversion to votes) |
| A3 origin of the votes | all ecological coefficients are negative; the test flags the year with the largest coefficient in any set of four; the vote ceiling has no causal meaning | the original test flags 1 of the 4 years, the one with the largest coefficient (2026); the others it does not | EXCESS DETECTED and relevant (worst case >= 1% of the margin) (**design caveat**; ceiling without causal interpretation) | REFUTED (no excess, ceiling <1% of the margin) |
| A12 zero vote | the estimator of p from the first round is biased where there were relevant third parties (ratios 0.27 to 0.72 in the placebos) | in 200 simulations of 2026 without manipulation, the original test flags excess in 44% (up to 5% would be expected) | detectable excess, irrelevant magnitude (<1% of the margin) (**design caveat**) | REFUTED (no excess, ceiling <1% of the margin) |

The corrected A3 estimates the opponent→PT transition rate with a 0-to-1 constraint and gives 0 in all four years: the constraint is binding and the bootstrap at the boundary underestimates the uncertainty. The honest reading is that the aggregate data **do not identify** a positive transition from the opponent to the PT, not that it is provably zero.

One point that the A1 correction makes visible: in the 2026 first round, the curve stays outside the corrected null envelope for 240 consecutive points (deviation of 1.67 p.p., near the 1.76 limit). This was **not** in the pre-registered target (the target is the second round), so it does not enter the verdict; it is recorded here for transparency and is consistent with the irregular arrival order of the first round (A18).

## Summary table

| A | analysis | result | p_holm | pct_margin_worst_case | verdict |
|---|---|---|---|---|---|
| A1 | count curve | maximum deviation vs permutation within the state: 2.65 p.p. (2026/T2) against 1.76 (2026/T1), 1.17 (2022/T2), 1.33 (2018/T2) | 0,000 | n/a (see caveat) | WITH DESIGN CAVEAT. Pre-registered: EXCESS DETECTED (shape test, no conversion to votes). Corrected: NO EXCESS (shape test, no conversion to votes) |
| A2 | T1→T2 transitions | opponent loses votes in 11.8% of sections (2022: PT 12.6%); swing shape does not differ from placebos | 0,000 | n/a (see caveat) | WITH DESIGN CAVEAT. Pre-registered: EXCESS DETECTED (shape test, no conversion to votes). Corrected: NO EXCESS (shape test, no conversion to votes) |
| A3 | origin of the votes | the accounting closes by identity; the ecological coefficient does not measure conversion | 0,002 | n/a (see caveat) | WITH DESIGN CAVEAT. Pre-registered: EXCESS DETECTED and relevant (worst case >= 1% of the margin). Corrected: REFUTED (no excess, ceiling <1% of the margin) |
| A4 | voting machine chain | 14,067 sections in 2026: 0 BU/RDV/hash divergences | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A5 | voting machine logs | votes after the nominal closing time: national estimate 23,094 (95% CI 16,895 to 29,704) | 1,000 | 0.09% | REFUTED (no excess, ceiling <1% of the margin) |
| A6 | replaced voting machine | machine ≠ expected in 0.60% of sections; no effect on the vote | 1,000 | 0.00% | REFUTED (no excess, ceiling <1% of the margin) |
| A7 | polls (context) | no verdict; see section | n/a | n/a | context, no verdict |
| A8 | consistency across offices | 0 sections outside the rule in 2018, 2022 and 2026 | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A9 | turnout profile | first round only; 2026 T1→T2 NOT RUN | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A10 | voting machine model, abroad | voting machine model has no effect on the vote within the polling place | 1,000 | 3.11% | see section |

All numbers below come from the CSVs in `results/fase2/`; scripts in `scripts/`.

## A1. Count curve

> **Design caveat (read first).** The pre-registered test compares the real curve with permutations of the sections within each state. That order is not random in any election, so the test flags envelope exit in all of them, and also in simulated series without manipulation. Demonstration and corrected version at the top of this page. The "excess" label on this row **does not indicate manipulation**.

**Claim tested:** "the curve should rise and fall in blocks; straight lines indicate manipulation".

**Recorded forecast.** Without manipulation: the real curve stays within the envelope of permutations of the sections within each state (keeping the arrival sequence of states), and the final total is identical under any order. Criterion: the maximum deviation (from 1% of sections on) only counts as excess if it exceeds that of the placebos and leaves the simultaneous 95% envelope for 20 consecutive points.

**Method.** Real order = time of the first partial tally per section (`DT_PRIM_TOT_PARCIAL_HOR_TSE`). 1,000 fully random orders (null A) and 1,000 permutations within each state preserving the state sequence (null B), over ~500 thousand sections.

| year | round | sections | final_share | maxdev_vs_B_pp | maxdev_vs_B_pp_later_ge10pct | maxdev_vs_A_pp | longest_run_outside_envelope | fraction_explained_by_geography | pct_sections_tallied_before_7pm |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | 2 | 499.205 | 0,5179 | 2,65 | 0,61 | 2,32 | 861 | 0,828 | 0,37 |
| 2026 | 1 | 499.206 | 0,4899 | 1,76 | 1,74 | 4,73 | 942 | 0,881 | 58,43 |
| 2022 | 2 | 472.027 | 0,5090 | 1,17 | 0,74 | 7,65 | 988 | 0,914 | 83,01 |
| 2018 | 2 | 454.447 | 0,4487 | 1,33 | 1,12 | 10,21 | 957 | 0,913 | 88,47 |

![Real count curve against nulls A and B](figs/a1_curva_apuracao.png)

**Pre-registered result.** The maximum deviation of 2026/T2 against null B is 2.65 p.p., larger than that of the placebos (1.76, 1.17, 1.33), and the curve leaves the envelope for 861 consecutive points. By the fixed criterion (kept, **with the design caveat above**), the row comes out as excess detected (shape test), with no effect on the final total.

**Demonstration and correction.** (1) Null B is rejected in all four years (longest run outside the envelope: 861, 942, 988, 957 out of 990 points): the arrival order within the state is not random in any election, because municipalities and zones arrive in blocks. (2) In 2026/T2 the maximum deviation occurs in the first 1 to 5% of sections; from 10% of sections on it falls to 0.61 p.p., below the placebos (1.74, 0.74, 1.12); this is a **post hoc** analysis, not pre-registered. (3) Geography explains 83% of the deviation against the fully random order. The effect on the final total is zero by construction.

**Publication pause.** In 2026/T2, only 0.37% of sections had a first tally before 7pm, against 83.0% in 2022 and 88.5% in 2018. This is compatible with the pause described by the press (see [Legal basis](base-legal.md)); the official source could not be opened.

**Arrival order by state (2026/T2, median position):** ZZ 0.00, DF 0.08, TO 0.10, PB 0.11, AM 0.14, MS 0.18 (first); MG 0.56, PI 0.59, SP 0.66, BA 0.67, SE 0.84, RJ 0.88 (last). The PT has SP 46%, BA 71%, SE 70%, RJ 47% among the last: states with different profiles arrive at different times, and the curve reflects that.

**NOT RUN:** (i) 2014/T2: the 2014 `detalhe_votacao_secao` product does not include a tally timestamp and the 2014 BWeb only has the receipt date; (ii) numerical comparison with the "Vote-count evolution" chart from g1 of 10/25/2026: the chart was not provided as data.

## A2. Section-by-section transitions, 1st to 2nd round

> **Design caveat (read first).** The "per-role" placebo (opponent) does not take into account who led the first round. Applied to the 2022 PT, the same test also flags excess. The corrected version compares the **first-round leader** of each year, standardizing by the third-parties/leader ratio. The "excess" label on this row **does not indicate manipulation**.

**Claim tested:** conversion of opponent voters to the PT; margin compression ('113x30 becomes 77x70'); swing shape different from the historical record.

**Recorded forecast.** Without manipulation: frequency of absolute vote loss by the opponent and swing shape within the range of the placebo years. Criterion: frequency outside [min, max] of the placebos, or shape 'different' if the smallest KS distance from 2026 to a placebo exceeds the largest distance between placebo pairs.

**Absolute vote loss** in sections with stable or rising turnout (≥ 98% of T1):

| year | cand | sections_stable_or_rising | sections_with_loss | pct_sections | votes_lost (votes, count) | pct_of_cand_T1_votes_in_those_sections | pct_sections_loss_above_20pct_of_T1 |
|---|---|---|---|---|---|---|---|
| 2014 | OPO | 219.370 | 2.428 | 1,11 | 9.604 | 0,049 | 0,043 |
| 2014 | PT | 219.370 | 7.368 | 3,36 | 36.618 | 0,174 | 0,054 |
| 2018 | OPO | 289.233 | 3.027 | 1,05 | 7.649 | 0,023 | 0,008 |
| 2018 | PT | 289.233 | 1.511 | 0,52 | 6.837 | 0,037 | 0,005 |
| 2022 | OPO | 391.919 | 4.938 | 1,26 | 11.131 | 0,025 | 0,005 |
| 2022 | PT | 391.919 | 49.243 | 12,56 | 187.733 | 0,398 | 0,018 |
| 2026 | OPO | 450.760 | 53.194 | 11,80 | 186.977 | 0,363 | 0,085 |
| 2026 | PT | 450.760 | 1.272 | 0,28 | 3.252 | 0,007 | 0,000 |

**Pre-registered result:** the opponent loses votes in 11.8% of sections in 2026, outside the range of the opponent placebos (2014, 2018, 2022: 1.1%, 1.0%, 1.3%). By the pre-registered criterion (kept, **with the design caveat above**): excess detected (shape test).

**Demonstration and correction.** The "per-role" placebo (opponent) is inadequate: in 2022 it was the **PT**, which led the first round, that lost absolute votes in 12.6% of sections, almost the mirror image of the opponent's 11.8% in 2026 (which led the first round). In both years there were few third-party votes to distribute (about 10 million and 9 million, against 26 million in 2014 and 2018). By band of "third-party votes / candidate's T1 votes" in the section, the frequencies are similar:

| cand | thirdparties_over_cand_T1_ratio | 2014 | 2018 | 2022 | 2026 |
|---|---|---|---|---|---|
| OPO | 0,1-0,2 | 3.29 | 1.51 | 0.9 | 11.71 |
| OPO | 0,2-0,4 | 0.83 | 0.81 | 0.58 | 6.48 |
| OPO | 0,4-0,8 | 0.21 | 0.61 | 0.32 | 3.69 |
| OPO | <0,1 | 13.55 | 5.04 | 1.94 | 19.68 |
| OPO | >=0,8 | 0.03 | 0.53 | 0.21 | 0.0 |
| PT | 0,1-0,2 | 10.02 | 3.5 | 15.72 | 0.12 |
| PT | 0,2-0,4 | 4.22 | 1.07 | 6.84 | 0.05 |
| PT | 0,4-0,8 | 1.02 | 0.22 | 1.59 | 0.04 |
| PT | <0,1 | 17.29 | 8.14 | 21.64 | 0.89 |
| PT | >=0,8 | 0.11 | 0.01 | 0.31 | 0.0 |

![Mirror of losses by band](figs/a2_espelho_perdas.png)

**Swing shape** (residual of the T2 margin on the T1 margin, with municipality fixed effect):

| pair | ks | ad_subsample_20k |
|---|---|---|
| 2014 x 2018 | 0,0210 | 12,8 |
| 2014 x 2022 | 0,1233 | 817,5 |
| 2014 x 2026 | 0,1097 | 638,6 |
| 2018 x 2022 | 0,1155 | 653,7 |
| 2018 x 2026 | 0,1018 | 491,3 |
| 2022 x 2026 | 0,0187 | 12,8 |

| smallest_ks_2026_vs_placebo | largest_ks_between_placebos | different_criterion |
|---|---|---|
| 0,0187 | 0,1233 | False |

Shape criterion: **2026 does not differ** (the smallest distance, against 2022, is smaller than the largest distance between placebos). The years cluster into two pairs, {2014, 2018} and {2022, 2026}, and 2026 falls in the 2022 pair.

**Margin compression:** coefficient of the T2 margin on the T1 margin (with municipality):

| year | spec | coef_m1 | se | n | municipalities |
|---|---|---|---|---|---|
| 2014 | T2 margin ~ T1 margin / municipality | 0,8242 | 0,0069 | 402.378 | 5.569 |
| 2018 | T2 margin ~ T1 margin / municipality | 0,7577 | 0,0050 | 427.448 | 5.568 |
| 2022 | T2 margin ~ T1 margin / municipality | 0,9146 | 0,0055 | 464.029 | 5.570 |
| 2026 | T2 margin ~ T1 margin / municipality | 0,9396 | 0,0025 | 491.114 | 5.571 |


## A3. Origin of Lula's new votes

> **Design caveat (read first).** The ecological coefficients are negative in all years and the test flags the year with the largest coefficient in any set of four. The vote ceiling on this row **does not measure manipulated votes**. The corrected version (rate constrained to 0 to 1) gives 0 in all four years. The "excess" label **does not indicate manipulation**.

**National accounting (identity).** Since there are no third parties in the second round, `ΔPT + ΔOPO = Δturnout + third parties in T1 − Δ(blank and null)`. The identity closes in every election:

| year | PT_T1 | PT_T2 | OPO_T1 | OPO_T2 | THIRDPARTIES_T1 | BN_T1 | BN_T2 | dPT | dOPO | dCOMP | pool | identity_ok | pt_pct_of_pool | opo_pct_of_pool |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2014 | 43.267.668 | 54.501.118 | 34.897.211 | 51.041.155 | 25.858.923 | 11.098.775 | 7.141.606 | 11.233.450 | 16.143.944 | -2.438.698 | 27.377.394 | True | 41,0 | 59,0 |
| 2018 | 31.342.005 | 47.040.906 | 49.276.990 | 57.797.847 | 26.431.678 | 10.312.562 | 11.094.439 | 15.698.901 | 8.520.857 | -1.430.043 | 24.219.758 | True | 64,8 | 35,2 |
| 2022 | 57.259.504 | 60.345.999 | 51.072.345 | 58.206.354 | 9.897.870 | 5.452.648 | 5.700.443 | 3.086.495 | 7.134.009 | 570.429 | 10.220.504 | True | 30,2 | 69,8 |
| 2026 | 53.879.538 | 64.256.232 | 56.104.503 | 59.826.041 | 9.321.993 | 5.969.801 | 4.153.801 | 10.376.694 | 3.721.538 | 2.960.239 | 14.098.232 | True | 73,6 | 26,4 |

In 2026, Lula gained 10,376,694 votes and the opponent 3,721,538 (positive net): the sum of the two (14,098,232) is exactly the set of available votes (14,098,232 = 2,960,239 of turnout + 9,321,993 of third parties − -1,816,000 of change in blank and null). Nationally, **no conversion from the opponent to the PT is needed** to explain the result.

**Minimum net loss per section** (how many of each candidate's T1 votes 'vanished' within sections where he lost absolute votes; it is a lower bound of voters who did not repeat their vote, due to switching, abstention or another cause, not of conversion):

| year | cand | sections | sections_with_net_loss | pct_sections | net_votes_lost_summed (votes, count) | national_net_gain (votes, count) |
|---|---|---|---|---|---|---|
| 2014 | OPO | 428.854 | 8.366 | 1,95 | 38.639 | 16.143.944 |
| 2014 | PT | 428.854 | 33.361 | 7,78 | 254.395 | 11.233.450 |
| 2018 | OPO | 454.447 | 16.611 | 3,66 | 62.162 | 8.521.166 |
| 2018 | PT | 454.447 | 11.910 | 2,62 | 90.077 | 15.699.286 |
| 2022 | OPO | 472.027 | 14.700 | 3,11 | 52.955 | 7.134.009 |
| 2022 | PT | 472.027 | 88.977 | 18,85 | 458.860 | 3.086.495 |
| 2026 | OPO | 499.205 | 82.180 | 16,46 | 383.008 | 3.721.538 |
| 2026 | PT | 499.205 | 9.590 | 1,92 | 58.933 | 10.376.696 |

The 2026 opponent (16.5% of sections, 383 thousand votes) and the 2022 PT (18.9%, 459 thousand) are of the same magnitude: the pattern is mirrored across the years and does not identify manipulation.

**Ecological regression** (apparent transition rates; ecological fallacy: these are correlations between aggregates, not individual behavior). Coefficient of "opponent in T1" on the PT in T2:

| year | destination_T2 | origin_T1 | coef | se |
|---|---|---|---|---|
| 2014 | PT | OPO_T1 | -0,070 | 0,006 |
| 2014 | PT | THIRDPARTIES_T1 | 0,393 | 0,017 |
| 2014 | PT | BLANK_NULL_T1 | 0,430 | 0,052 |
| 2018 | PT | OPO_T1 | -0,098 | 0,012 |
| 2018 | PT | THIRDPARTIES_T1 | 0,703 | 0,029 |
| 2018 | PT | BLANK_NULL_T1 | 0,288 | 0,041 |
| 2022 | PT | OPO_T1 | -0,045 | 0,002 |
| 2022 | PT | THIRDPARTIES_T1 | 0,433 | 0,011 |
| 2022 | PT | BLANK_NULL_T1 | 0,256 | 0,020 |
| 2026 | PT | OPO_T1 | -0,034 | 0,002 |
| 2026 | PT | THIRDPARTIES_T1 | 0,465 | 0,011 |
| 2026 | PT | BLANK_NULL_T1 | 0,756 | 0,016 |

With municipality fixed effect (relative to T1 abstention):

| year | origin_T1 | coef | se | municipalities | note |
|---|---|---|---|---|---|
| 2014 | op1 | -0,042 | 0,005 | 5570 | relative to T1 abstention; municipality FE |
| 2018 | op1 | -0,065 | 0,005 | 5570 | relative to T1 abstention; municipality FE |
| 2022 | op1 | -0,069 | 0,003 | 5570 | relative to T1 abstention; municipality FE |
| 2026 | op1 | -0,127 | 0,004 | 5571 | relative to T1 abstention; municipality FE |

**Result by the pre-registered criterion (kept, with the caveat above):** the 2026 coefficient (-0.034) is the least negative of the four years and the row comes out as excess; the vote ceiling computed for this row is in Appendix B, without causal interpretation. **Demonstration and correction:** all coefficients are negative (none measures conversion); the difference between years reflects geography; with municipality fixed effect the 2026 coefficient is the **most negative** (−0.127 against −0.042 to −0.070). The vote ceiling derived from this difference has no causal interpretation (Appendix B).

**Limits:** ecological fallacy; the 2026 second round has voters of candidates different from those of 2022; the identity uses the BWeb, which is the same data being audited.

## A4. Voting machine chain up to the TSE

**Input:** the set "files transmitted for tallying" (BU, BU image, RDV, log and signature per section). The TSE catalog lists only the first round; the 2026 second-round files and those of 2022 exist at the same paths and were downloaded per section (partial requests).

**Recorded forecast.** 0 divergences between digital BU, RDV, BWeb and hash binding across the whole sample; a one-vote divergence is reported individually.

**Sample:** all of Roraima; the sections that closed ≥115 min after the scheduled time (complete population outside Roraima and abroad); 1:1 controls in the same polling place; the sections with turnout ≥95%; 60 random per state; and the same sections in 2022 as placebo.

| year | sections | sections_with_read_error | states | bu_differs_from_bweb | rdv_differs_from_bu | hash_not_bound | software_versions | app_signature_failures_in_log |
|---|---|---|---|---|---|---|---|---|
| 2026 | 14.067 | 0 | 27 | 0 | 0 | 0 | 10.23.0.0 - Praia da Barra do Cahy (14067) | 0 |
| 2022 | 12.554 | 0 | 27 | 0 | 0 | 0 | 8.26.0.0 - Onça-pintada (12554) | 0 |

**What was verified:** (c) the digital BU matches the BWeb in Lula, opponent, blank, null and turnout; (b) the recounted RDV matches the BU (Lula, opponent, blank and total; nulls by residual); integrity binding: the SHA-512 of BU, RDV, image and log appears in the list signed by the voting machine and the SHA-512 of the list matches the hash of the signed block. The BU issuance matches that of the BWeb in 14,067 of 14,067 sections.

**Cryptographic signature: PARTIALLY NOT RUN.** *Verified:* the X.509 certificate embedded in the signature file of each Roraima section in 2026 (1,519 sections read, 0 errors): the certificate CN is `UEAO` + the machine number from the BWeb in 1,519 of 1,519; the validity covers the election date in 1,519 of 1,519; the issuers are `AC UE2020` (922), `AC UE2022` (597) (organization `TSE`); the algorithm OID is `1.3.6.1.4.1.44588.2.1`, with a 66-byte key and a 132-byte signature (sizes compatible with a 521-bit curve; the OID does not match any standard-library algorithm). *Not verified:* the signature itself (**0% of sections verified**) and the chain up to the root, because the root certificate, the official public key and the specification could not be obtained from an official source (the TSE site returns HTTP 403 to automation). **No key from an unofficial source was used.** A 2021 TSE presentation (seen only in a search result, without opening the document) mentions 256-bit elliptic-curve signatures and EdDSA/Curve25519 for the BU QR code; that is a different artifact and was also not verified here. Script: `scripts/13_cert_urna.py`; result: `results/fase2/cert_RR_2026.csv`. The 2022 files were not read (different file layout). Missing input: accessible official root certificates and specification.

**NOT verified:** (d) the software identification against the one published at the sealing ceremony: it was only possible to list the version recorded in the log (2026: 10.23.0.0; 2022: 8.26.0.0) and the per-step application signature verification (6 steps, all "SUCESSO" in every log read). Missing input: sealing hashes to compare.

> **What A4 and H9 verify and what they do not verify.** They verify **consistency among files that the TSE itself publishes** (BU, RDV, BU image, log, BWeb, tallying) and the hash binding among them. These files are generated by the same voting machine software and the same tallying flow. Therefore they **do not rule out a coherent alteration made before publication** (one that altered all artifacts consistently), nor do they verify whether the recorded vote corresponds to the vote typed by the voter. See [A18](a18-alteracao-no-meio.md) and [A19](a19-voto-digitado.md).

**Individual divergences:**

None in 2026 or 2022.

The BU and RDV reader is generic (BER decoder) and each field was validated against the BWeb before being used (in Roraima: 1,519 of 1,519 sections).

## A5. Voting machine logs (votes after the scheduled time)

**What the logs record** (confirmed in the files): per voter, "Eleitor foi habilitado" (voter enabled), "Tipo de habilitação" (biometric or manual, with "Dado digitado confere" — typed data matches), "Voto confirmado para [office]" (vote confirmed for [office]) and "O voto do eleitor foi computado" (the voter's vote was recorded), each with date and time; contingency events and signature-verification events.

**Recorded forecast.** Votes recorded in the log = BU turnout in ≥99.9% of sections; votes after the nominal closing time concentrated in the sections that closed late; intervals between votes above the physical minimum; no association between late vote and Lula% in the same polling place beyond the 2022 placebo.

**Log against BU:**

| year | sections | log_recorded_votes_equal_turnout | pct | divergent | divergent_with_contingency_machine | divergent_without_contingency | enabled_greater_than_turnout | enabled_less_than_turnout | min_gap_between_enablings_s | sections_with_gap_under_10s |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026 | 14.067 | 14.005 | 99,56 | 62 | 62 | 0 | 256 | 62 | 18.0 | 0 |
| 2022 | 12.554 | 12.462 | 99,27 | 92 | 91 | 1 | 585 | 91 | 13.0 | 0 |

The pre-registered 99.9% threshold is **not met** (see `pct`), and all divergences with contingency explain the difference: contingency machines took over mid-day (log: "Seção informada pelo operador: 0000 - Urna de contingência" — section reported by the operator: 0000 - Contingency machine), and the BU consolidates the votes recovered from the previous machine, which are not in the replacement machine's log. Exceptions **without** contingency (reported individually):

| year | state | municipality_code | zone | section | turnout | recorded_log | enabled_log |
|---|---|---|---|---|---|---|---|
| 2022 | RJ | 60011 | 7 | 479 | 348 | 347 | 348 |

**Votes recorded after the nominal closing time** (5pm Brasília time, converted to each machine's local clock), by stratum:

| year | stratum | sections | sections_with_vote_after_nominal | votes_after_nominal | mean_per_section | max_per_section | turnout |
|---|---|---|---|---|---|---|---|
| 2026 | C | 3.675 | 378 | 429 | 0,117 | 4 | 1.064.563 |
| 2026 | H | 619 | 21 | 34 | 0,055 | 14 | 105.661 |
| 2026 | L | 6.714 | 3.169 | 4.710 | 0,702 | 39 | 1.970.400 |
| 2026 | R | 1.540 | 69 | 76 | 0,049 | 2 | 381.492 |
| 2026 | RR_completo | 1.519 | 133 | 143 | 0,094 | 2 | 308.597 |
| 2022 | C | 3.414 | 478 | 539 | 0,158 | 6 | 1.039.604 |
| 2022 | H | 209 | 8 | 57 | 0,273 | 46 | 40.515 |
| 2022 | L | 6.268 | 901 | 1.098 | 0,175 | 14 | 1.940.256 |
| 2022 | R | 1.395 | 96 | 119 | 0,085 | 5 | 351.855 |
| 2022 | RR_completo | 1.268 | 145 | 169 | 0,133 | 4 | 286.269 |

![Votes after the nominal time by stratum](figs/a5_votos_apos_nominal.png)

**Last vote per section, after the nominal closing time:**

| year | stratum | sections | last_vote_more_than_15min_after | last_vote_more_than_60min_after | last_vote_before_nominal_time |
|---|---|---|---|---|---|
| 2026 | C | 3675 | 0 | 0 | 3297 |
| 2026 | H | 619 | 1 | 0 | 598 |
| 2026 | L | 6714 | 2599 | 1629 | 3542 |
| 2026 | R | 1540 | 0 | 0 | 1471 |
| 2026 | RR_completo | 1519 | 0 | 0 | 1386 |
| 2022 | C | 3414 | 1 | 0 | 2935 |
| 2022 | H | 209 | 1 | 1 | 200 |
| 2022 | L | 6268 | 3 | 0 | 5365 |
| 2022 | R | 1395 | 2 | 0 | 1299 |
| 2022 | RR_completo | 1268 | 0 | 0 | 1123 |

**National estimate (2026/T2).** In the 6,714 sections that closed ≥115 min late (complete population outside Roraima and abroad; 6,714 measured, 0 without files), 4,710 votes after the nominal time were measured. In the remaining sections, the random sample (60 per state) estimates 18,384 votes (95% CI 12,185 to 24,994). **Total estimated: 23,094 votes (95% CI 16,895 to 29,704)**, or 0.52% of the margin. The external reference of 34,330 voters (press, unverified) is within the same order of magnitude. These votes include those of voters already in line at 5pm, provided for in art. 153 of the Electoral Code ([Legal basis](base-legal.md)); most are outside the sections that closed late.

**Reading.** Many of the sections that "closed late" kept the machine open until close to 7pm **without recording any vote after 5pm**: the "last vote before nominal time" column shows how many. Late closing, by itself, does not measure late voting.

**Total manual voter release from the log** (turnout minus biometric enablings), against the BWeb field (which only measures those with registered biometrics):

| sections | manual_total_log | bweb_biom_nh | ratio | enabling_types |
|---|---|---|---|---|
| 13.986 | 464.424 | 242.091 | 1,92 | hab_biometric |

**Association between late vote and Lula% in the same polling place** (fraction of votes after the nominal time; T1 control; placebo: same sections in 2022):

| year | coef | se | sections | places |
|---|---|---|---|---|
| 2026 | 0,060 | 0,068 | 11.403 | 1.822 |
| 2022 | -0,093 | 0,122 | 10.410 | 1.692 |

Verdict: REFUTED (no excess, ceiling <1% of the margin).

**Limits:** sample, not the whole election (the sections of states without files and the controls are not random); the machine clock is local; the log does not allow linking vote to voter. Minimum gap between enablings: 13 s.

## A6. Replaced or contingency voting machine

Compares the **expected** machine (TSE expected correspondence, 10/24/2026) with the **actual** one (BWeb). There is no open set of "occurrences" in the TSE catalog; this is the available measure.

| year | sections | no_match | machine_differs_from_expected | pct |
|---|---|---|---|---|
| 2026 | 497.696 | 12 | 3.005 | 0,60 |
| 2022 | 470.843 | 23 | 8.078 | 1,72 |

| year | spec | coef | se | replaced_sections | n |
|---|---|---|---|---|---|
| 2026 | Lula% T2 / T1 | -0,0007 | 0,0004 | 3.005 | 475.772 |
| 2026 | turnout T2 / T1 | -0,0003 | 0,0004 | 3.005 | 475.772 |
| 2026 | Lula% T1 (same sections, no lag) | 0,0003 | 0,0008 | 3.005 | 475.772 |
| 2022 | Lula% T2 / T1 | 0,0001 | 0,0002 | 8.078 | 447.198 |
| 2022 | turnout T2 / T1 | -0,0006 | 0,0002 | 8.078 | 447.198 |
| 2022 | Lula% T1 (same sections, no lag) | 0,0006 | 0,0005 | 8.078 | 447.198 |

Sections with a machine different from the expected one do not vote differently from their neighbors in the same polling place, in 2026 or in 2022.

## A7. Polls and result (context, no verdict)

The TSE publishes the **registration** of the polls (protocol, institute, dates, sample, cost), not the results; the results below come from the press, with links. Poll error is not evidence of manipulation, and the converse also holds.

| year | institute | published | pt_pct_valid_poll | opponent_pct_valid_poll | declared_margin_of_error_pp | source | pt_pct_valid_result | error_pp_pt | outside_declared_margin |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | Datafolha | 2018-10-27 | 45.0 | 55.0 | 2 | https://www.jornalopcao.com.br/ultimas-noticias/datafolha-bolsonaro-tem-55-e-haddad-45-dos-votos-validos-145482/ | 44,87 | 0,13 | False |
| 2022 | Datafolha | 2022-10-29 | 52.0 | 48.0 | 2 | https://www.opovo.com.br/eleicoes-2022/2022/10/29/pesquisa-datafolha-lula-52-bolsonaro-48-no-2-turno.html | 50,90 | 1,10 | False |
| 2026 | Datafolha | 2026-10-24 | 49.0 | 51.0 | 2 | https://www.jornalopcao.com.br/ultimas-noticias/flavio-bolsonaro-tem-51-dos-votos-validos-contra-49-de-lula-no-segundo-turno-aponta-datafolha-879307/ | 51,79 | -2,79 | True |
| 2026 | AtlasIntel | 2026-10-24 | 49.2 | 50.8 | 1 | https://www.bloomberglinea.com.br/brasil/flavio-bolsonaro-tem-508-dos-votos-validos-contra-492-de-lula-aponta-atlasintel/ | 51,79 | -2,59 | True |

TSE registrations with publication on 10/24/2026 (Datafolha and AtlasIntel) are in `data/pesquisas_registro_tse_24out2026.csv`; the link between each result and each registration number was **not verified**.

**NOT RUN:** historical error of the same institutes in 2014 (no election-eve poll with a confirmed date was located, with a source) and of Quaest and Paraná Pesquisas in 2026 (result not located).

## A8. Consistency across offices in the same poll-receipt

In each section, the total of each office (nominal + party-list + blank + null + annulled) must equal the turnout (times the number of seats: 2 in the 2018 and 2026 Senate races).

| year | round | offices | sections_x_offices | outside_the_rule |
|---|---|---|---|---|
| 2018 | 1 | 10 | 2.270.038 | 0 |
| 2018 | 2 | 2 | 732.741 | 0 |
| 2022 | 1 | 7 | 2.356.075 | 0 |
| 2022 | 2 | 2 | 721.067 | 0 |
| 2026 | 1 | 7 | 2.490.804 | 0 |
| 2026 | 2 | 2 | 538.944 | 0 |

Zero sections outside the rule in 2018, 2022 and 2026 (first round with all offices; second round with president and governor in the states with a runoff). An insertion affecting a single office would break the equality.

## A9. Turnout profile

**NOT RUN (part):** the change from the 1st to the 2nd round by age band in 2026 cannot be computed: the 2026 turnout and abstention profile dataset was published on 10/21/2026 and only covers the 1st round. Missing input: the 2026/2nd-round profile.

**Run:** consistency of cells and totals; comparison of the 2026 first round with 2022 and 2018; T1→T2 change in 2018 and 2022 (context).

| year | round | cells | turnout_greater_than_eligible | turnout_plus_abstention_differs_from_eligible | optional_plus_mandatory_sum_differs |
|---|---|---|---|---|---|
| 2018 | 1 | 1.625.513 | 0 | 0 | 0 |
| 2018 | 2 | 1.625.513 | 0 | 0 | 0 |
| 2022 | 1 | 1.667.245 | 0 | 0 | 0 |
| 2022 | 2 | 1.667.245 | 0 | 0 | 0 |
| 2026 | 1 | 1.648.478 | 0 | 0 | 0 |

| year | round | paired_zones | bweb_only | profile_only | zones_turnout_differs | zones_eligible_differs | sum_abs_turnout_diff |
|---|---|---|---|---|---|---|---|
| 2018 | 1 | 6.240 | 0 | 33 | 5.475 | 5.520 | 114.415 |
| 2018 | 2 | 6.240 | 0 | 33 | 5.426 | 5.511 | 106.841 |
| 2022 | 1 | 6.240 | 0 | 43 | 6.093 | 6.097 | 363.117 |
| 2022 | 2 | 6.241 | 0 | 42 | 6.077 | 6.108 | 316.643 |
| 2026 | 1 | 6.251 | 0 | 41 | 6.099 | 6.097 | 325.657 |

No cell with turnout greater than eligible voters. The per-zone difference between profile and BWeb comes from voters who vote outside their registration zone; the national total matches (difference of a few thousand in ~125 million).

**Zones with optional-voter turnout outside [Q1−3 IQR, Q3+3 IQR] of 2022/T1:**

| year | round | zones | outside_interval | pct | above | below | limits |
|---|---|---|---|---|---|---|---|
| 2022 | 1 | 6169 | 1 | 0.016210082671421624 | 0 | 1 | [0.016, 1.059] |
| 2022 | 2 | 6169 | 1 | 0.016210082671421624 | 0 | 1 | [0.016, 1.059] |
| 2018 | 1 | 6162 | 0 | 0.0 | 0 | 0 | [0.016, 1.059] |
| 2018 | 2 | 6162 | 0 | 0.0 | 0 | 0 | [0.016, 1.059] |
| 2026 | 1 | 6188 | 0 | 0.0 | 0 | 0 | [0.016, 1.059] |

The interval is wide (the test is not very sensitive). **Eligible voters and turnout by age band, 1st round** (2026 against 2022):

| AGE_BAND | eligible_2018 | turnout_2018 | eligible_2022 | turnout_2022 | eligible_2026 | turnout_2026 | eligible_2026_over_2022 | turnout_2026_over_2022 |
|---|---|---|---|---|---|---|---|---|
| 16 years | 403.683 | 345.012 | 815.063 | 682.824 | 606.603 | 539.705 | 1 | 1 |
| 17 years | 996.934 | 819.501 | 1.301.718 | 1.071.822 | 1.027.641 | 887.283 | 1 | 1 |
| 60 to 64 years | 8.907.997 | 7.645.176 | 9.995.705 | 8.728.897 | 11.164.875 | 9.801.480 | 1 | 1 |
| 70 to 74 years | 4.763.343 | 2.630.591 | 5.885.358 | 3.591.058 | 6.968.531 | 4.792.544 | 1 | 1 |
| 75 to 79 years | 3.170.195 | 1.188.659 | 3.858.345 | 1.613.326 | 4.767.219 | 2.489.816 | 1 | 2 |
| 80 to 84 years | 1.972.721 | 475.944 | 2.424.573 | 654.036 | 2.748.727 | 1.020.461 | 1 | 2 |
| 85 to 89 years | 1.121.775 | 148.709 | 1.334.866 | 209.870 | 1.466.444 | 356.317 | 1 | 2 |
| 90 to 94 years | 689.078 | 33.697 | 738.761 | 49.783 | 665.199 | 89.557 | 1 | 2 |

Turnout of voters over 80 (optional vote) grows more than the eligible population in the band between 2022 and 2026 in the 1st round. Cause not identified (untested hypotheses: registry review and voter-registration cancellations). It is a plausible mundane hypothesis for part of the increase in sections with turnout ≥95% (see [Residuals](residuos.md)).

## A10. Voting machine model, abroad and special polling places

**Machine model, within the same polling place** (coefficients of Lula% in T2 given T1, against the UE2020; UE2022 is a new model in 2026):

| year | model | spec | coef | se | sections |
|---|---|---|---|---|---|
| 2022 | 2009 | Lula% T2 given T1 | -0,0009 | 0,0011 | 46.159 |
| 2022 | 2010 | Lula% T2 given T1 | -0,0008 | 0,0011 | 92.781 |
| 2022 | 2011 | Lula% T2 given T1 | -0,0008 | 0,0011 | 26.432 |
| 2022 | 2013 | Lula% T2 given T1 | -0,0008 | 0,0012 | 24.294 |
| 2022 | 2015 | Lula% T2 given T1 | -0,0007 | 0,0011 | 85.159 |
| 2026 | 2013 | Lula% T2 given T1 | 0,0007 | 0,0015 | 11.421 |
| 2026 | 2015 | Lula% T2 given T1 | -0,0000 | 0,0014 | 87.179 |
| 2026 | 2022 | Lula% T2 given T1 | 0,0000 | 0,0002 | 198.670 |

No machine model changes the vote within the same polling place. The manual voter release rate varies a lot by model (see Phase 1, section 3.3), but not the vote.

**Abroad (ZZ) against Brazil:**

| year | round | subset | sections | pt_pct_of_two | turnout | pct_sections_turnout_ge95 |
|---|---|---|---|---|---|---|
| 2018 | 1 | abroad (ZZ) | 744 | 14,67 | 40,6 | 0,000 |
| 2018 | 1 | Brazil | 453.702 | 38,92 | 79,8 | 0,211 |
| 2018 | 2 | abroad (ZZ) | 744 | 28,98 | 40,2 | 0,000 |
| 2018 | 2 | Brazil | 453.703 | 44,90 | 78,8 | 0,111 |
| 2022 | 1 | abroad (ZZ) | 1.014 | 53,13 | 43,9 | 0,000 |
| 2022 | 1 | Brazil | 471.010 | 52,85 | 79,2 | 0,056 |
| 2022 | 2 | abroad (ZZ) | 1.017 | 51,28 | 44,6 | 0,000 |
| 2022 | 2 | Brazil | 471.010 | 50,90 | 79,6 | 0,049 |
| 2026 | 1 | abroad (ZZ) | 1.309 | 52,24 | 37,3 | 0,000 |
| 2026 | 1 | Brazil | 497.897 | 48,98 | 79,2 | 0,112 |
| 2026 | 2 | abroad (ZZ) | 1.308 | 53,85 | 41,6 | 0,000 |
| 2026 | 2 | Brazil | 497.897 | 51,78 | 81,0 | 0,128 |

Abroad has 0 sections with turnout ≥95% in every election; the mundane causes of the ≥95% in Brazil (Indigenous, prison, quilombola polling places, small and new sections) are in section 3.6 of Phase 1. Load-generation station (`CD_FLASHCARD`) was **not analyzed**.

## A11. Vote transfer from candidates defeated in the 1st round

**Context with sources.** Zema, Caiado and Cury endorsed Flávio in the 2nd round and Renan Santos released his voters ([A Crítica](https://acritica.net/eleicoes-2026/caiado-zema-e-cury-apoiam-flavio-no-2o-turno-renan-santos-libera-eleitores/); Caiado: [Diário do Nordeste](https://diariodonordeste.verdesmares.com.br/pontopoder/ronaldo-caiado-anuncia-apoio-a-flavio-bolsonaro-no-2-turno-das-eleicoes-2026-1.3796893)). Name-by-name check in [O Povo, 10/10/2026](https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/10/quem-os-candidatos-a-presidente-derrotados-apoiam-no-2-turno.html): Zema, Caiado, Cury and Clariana Barão declared support for Flávio; Hertz Dias and Edmilson Costa announced a critical vote for Lula; Renan Santos stayed neutral; Wilson Grassi did not take a position. **Divergences from the reported classification:** Samara Martins appears only as party guidance (UP: "vote 13"); Leonardo Alves does not appear. **Rui Costa Pimenta, two positions on record:** (i) O Povo, 10/10/2026: **no defined position** (the PCO would hold a conference); (ii) Space Money (source indicated to the author): **null vote**, **unverified**, because the site returns HTTP 403 to automation. The A11 block follows the reported classification (null vote) and this is declared; both positions and the dates are kept here for anyone who wants to check. The blocks follow the reported classification for Samara Martins and Rui Costa Pimenta, and this is declared.

**Each candidate's votes in the 1st round, confirmed in the BWeb:**

| number | candidate | votes_t1 |
|---|---|---|
| 30 | Zema | 326.488 |
| 55 | Caiado | 2.605.148 |
| 70 | Cury | 3.448.569 |
| 27 | Clariana | 40.043 |
| 16 | Hertz Dias | 43.103 |
| 21 | Edmilson Costa | 22.693 |
| 80 | Samara Martins | 122.911 |
| 14 | Renan Santos | 2.675.887 |
| 29 | Rui Costa Pimenta | 15.024 |
| 35 | Wilson Grassi | 16.881 |
| 28 | Leonardo Alves | 5.246 |
| 13 | Lula | 53.879.538 |
| 22 | Flavio Bolsonaro | 56.104.503 |

**National accounting, term by term** (identity: Lula's gain + Flávio's gain = third parties + drop in blank and null + drop in abstention + change in eligible voters):

| term | votes |
|---|---|
| third parties in T1: pro_Flavio block | 6.420.248 |
| third parties in T1: left block | 188.707 |
| third parties in T1: Renan block | 2.675.887 |
| third parties in T1: PCO block | 15.024 |
| third parties in T1: others block | 22.127 |
| third parties in T1: total (includes others not listed) | 9.321.993 |
| drop in blank and null (T1 minus T2) | 1.816.000 |
| drop in abstention (T1 minus T2; eligible nearly constant) | 2.960.269 |
| change in total eligible (T2 minus T1) | -30 |
| SUM of terms (pool) | 14.098.262 |
| Lula's gain (T2 minus T1) | 10.376.694 |
| Flavio's gain (T2 minus T1) | 3.721.538 |
| Lula's gain + Flavio's gain | 14.098.232 |
| residual (pool minus gains) | 30 |

The identity closes with zero residual. The first-round third parties (9.32 million), the drop in blank and null (1.82 million) and the drop in abstention (2.96 million) add up to 14.10 million, and the two candidates gained 14.10 million. The block that endorsed Flávio totaled 6,420,248 votes in the 1st round, and Flávio's **net** gain was 3,721,538.

**Ecological regression with municipality fixed effect** (vote per eligible voter in T2 on each block's share in T1; abstention omitted; ecological fallacy: these are apparent rates between aggregates):

| year | destination | origin | coef | se | municipalities |
|---|---|---|---|---|---|
| 2026 | PT | pro_Flavio | 0,305 | 0,013 | 5.571 |
| 2026 | PT | left | 0,683 | 0,021 | 5.571 |
| 2026 | PT | Renan | 0,236 | 0,007 | 5.571 |
| 2026 | PT | PCO | 0,068 | 0,080 | 5.571 |
| 2026 | PT | others | 0,275 | 0,050 | 5.571 |
| 2026 | PT | PT | 0,896 | 0,008 | 5.571 |
| 2026 | PT | OPO | -0,128 | 0,004 | 5.571 |
| 2026 | PT | BN | 0,506 | 0,019 | 5.571 |
| 2026 | OPO | pro_Flavio | 0,397 | 0,008 | 5.571 |
| 2026 | OPO | left | 0,000 | 0,020 | 5.571 |
| 2026 | OPO | Renan | 0,286 | 0,008 | 5.571 |
| 2026 | OPO | PCO | 0,384 | 0,049 | 5.571 |
| 2026 | OPO | others | 0,221 | 0,039 | 5.571 |
| 2026 | OPO | PT | -0,062 | 0,005 | 5.571 |
| 2026 | OPO | OPO | 0,947 | 0,002 | 5.571 |
| 2026 | OPO | BN | 0,025 | 0,017 | 5.571 |

**Goodman with 0-to-1 constraint** (no fixed effect, weighted; 2026):

| destination | origin | constrained_rate_0_1 |
|---|---|---|
| PT | pro_Flavio | 0,357 |
| PT | left | 0,994 |
| PT | Renan | 0,357 |
| PT | PCO | 0,563 |
| PT | others | 0,484 |
| PT | PT | 1,000 |
| PT | OPO | 0,000 |
| PT | BN | 0,792 |
| PT | ABS | 0,067 |
| OPO | pro_Flavio | 0,455 |
| OPO | left | 0,037 |
| OPO | Renan | 0,368 |
| OPO | PCO | 0,493 |
| OPO | others | 0,140 |
| OPO | PT | 0,000 |
| OPO | OPO | 1,000 |
| OPO | BN | 0,000 |
| OPO | ABS | 0,000 |

**Heterogeneity across states** of the "origin block → PT" coefficient (2026: pro-Flávio block; 2022 and 2018: largest third party, without inferring endorsements):

| year | regressor | states | weighted_mean | sd_between_states | min | max |
|---|---|---|---|---|---|---|
| 2026 | pro_Flavio | 24 | 0,313 | 0,072 | 0,232 | 0,567 |
| 2022 | terc1_n15 | 24 | 0,405 | 0,061 | 0,270 | 0,579 |
| 2018 | terc1_n12 | 24 | 0,708 | 0,102 | 0,514 | 0,848 |

**Pre-registered result:** REFUTED (no excess, ceiling <1% of the margin) (2026 coefficient 0.305 against 2022: largest third party (terc1_n15): 0.42089 (se 0.00686, p_exc 1) | 2018: largest third party (terc1_n12): 0.70891 (se 0.01825, p_exc 1)). **Design caveat:** the 2026 blocks and the largest third parties of 2022 and 2018 have different composition, and ecological coefficients do not measure individual conversion; the verdict indicates when the coefficient leaves the placebo range, not that there is undue transfer. The forecast "Flávio's gain grows with the share of the block that endorsed him" is tested by the pro-Flávio block → Flávio coefficient in the table above.

## A12. Sections with zero votes for a candidate

> **Design caveat (read first).** The pre-registered row compares the 2026 observed/expected ratio with ratios of years in which the estimator of p from the first round is biased. In simulations without manipulation, the original test flags excess in a large share of the series. The corrected version (p from the neighbors of the same polling place) shows no excess. The "detectable excess" label **does not indicate manipulation**.

**Claim tested:** "109 sections with zero votes". The origin of the number was not provided and no news report was located; therefore I report all reasonable definitions.

| year | round | definition | sections | zero_opponent | zero_PT | PT_votes_in_zero_opponent | opponent_votes_in_zero_PT |
|---|---|---|---|---|---|---|---|
| 2026 | 1 | all tallied | 499.206 | 81 | 8 | 9.549 | 507 |
| 2026 | 1 | excluding abroad, turnout >= 1 | 497.897 | 79 | 8 | 9.542 | 507 |
| 2026 | 2 | all tallied | 499.205 | 106 | 4 | 14.860 | 296 |
| 2026 | 2 | excluding abroad, turnout >= 1 | 497.897 | 106 | 4 | 14.860 | 296 |
| 2022 | 1 | all tallied | 472.024 | 161 | 1 | 17.531 | 58 |
| 2022 | 1 | excluding abroad, turnout >= 1 | 471.010 | 160 | 1 | 17.527 | 58 |
| 2022 | 2 | all tallied | 472.027 | 143 | 4 | 16.455 | 124 |
| 2022 | 2 | excluding abroad, turnout >= 1 | 471.010 | 141 | 2 | 16.418 | 118 |
| 2018 | 1 | all tallied | 454.446 | 674 | 32 | 72.102 | 1.223 |
| 2018 | 1 | excluding abroad, turnout >= 1 | 453.702 | 674 | 28 | 72.102 | 1.147 |
| 2018 | 2 | all tallied | 454.447 | 328 | 4 | 36.608 | 315 |
| 2018 | 2 | excluding abroad, turnout >= 1 | 453.703 | 328 | 3 | 36.608 | 275 |
| 2014 | 1 | all tallied | 428.853 | 709 | 17 | 64.924 | 197 |
| 2014 | 1 | excluding abroad, turnout >= 1 | 427.937 | 709 | 16 | 64.924 | 190 |
| 2014 | 2 | all tallied | 428.854 | 194 | 13 | 15.103 | 199 |
| 2014 | 2 | excluding abroad, turnout >= 1 | 427.936 | 192 | 10 | 15.103 | 192 |

**The 109 does not reproduce** under any tested definition: in 2026/T2 there are 106 sections with zero votes for Flávio and 4 for Lula; in the first round, 81 and 8. For comparison, the opponent had zero votes in 143 sections in 2022 (Bolsonaro), 328 in 2018 and 192 in 2014 (2nd round).

**Expected number of sections with zero** = sum of P(zero) = (1 − p)^n, with p estimated in two ways:

| year | candidate_with_zero | p_estimator | sections | observed | expected | ratio | z | p_excess |
|---|---|---|---|---|---|---|---|---|
| 2026 | opponent | p from the section itself in T1 | 497.897 | 106 | 95,7 | 1,11 | 1,33 | 0,092 |
| 2026 | opponent | p from neighboring sections of the polling place | 450.683 | 14 | 13,2 | 1,06 | 0,31 | 0,377 |
| 2026 | PT | p from the section itself in T1 | 497.897 | 4 | 7,2 | 0,56 | -1,59 | 0,944 |
| 2026 | PT | p from neighboring sections of the polling place | 450.683 | 0 | 0,0 | 0,00 | -0,03 | 0,512 |
| 2022 | opponent | p from the section itself in T1 | 471.010 | 141 | 196,8 | 0,72 | -5,02 | 1,000 |
| 2022 | opponent | p from neighboring sections of the polling place | 422.400 | 10 | 8,7 | 1,16 | 0,54 | 0,295 |
| 2022 | PT | p from the section itself in T1 | 471.010 | 2 | 1,9 | 1,03 | 0,05 | 0,478 |
| 2022 | PT | p from neighboring sections of the polling place | 422.400 | 0 | 0,0 | 0,00 | -0,07 | 0,528 |
| 2018 | opponent | p from the section itself in T1 | 453.703 | 328 | 625,8 | 0,52 | -15,57 | 1,000 |
| 2018 | opponent | p from neighboring sections of the polling place | 401.664 | 29 | 30,1 | 0,96 | -0,26 | 0,603 |
| 2018 | PT | p from the section itself in T1 | 453.703 | 3 | 33,8 | 0,09 | -6,21 | 1,000 |
| 2018 | PT | p from neighboring sections of the polling place | 401.664 | 0 | 0,9 | 0,00 | -1,08 | 0,859 |
| 2014 | opponent | p from the section itself in T1 | 427.936 | 192 | 722,3 | 0,27 | -25,29 | 1,000 |
| 2014 | opponent | p from neighboring sections of the polling place | 371.997 | 2 | 7,0 | 0,29 | -2,20 | 0,986 |
| 2014 | PT | p from the section itself in T1 | 427.936 | 10 | 8,4 | 1,19 | 0,63 | 0,266 |
| 2014 | PT | p from neighboring sections of the polling place | 371.997 | 0 | 0,3 | 0,00 | -0,56 | 0,712 |

In 2026 the observed value for the opponent (106) is close to the expected value from the section's own T1 vote and from the neighbors of the same polling place, with no significant excess; in 2022, 2018 and 2014 the observed value was **below** the expected value from the T1 estimator (in 2018 and 2014 the presence of relevant third parties in T1 makes that estimator poorly suited).

**Profile of the 106 sections with zero votes for Flávio in the 2nd round:** median turnout 128, median eligible 161; 53% had a Flávio vote in the 1st round, 36% had a Bolsonaro vote in 2022 and 25% in 2018 (for the sections that existed). **Ceiling:** the PT votes in these sections total 14,860, or 0.34% of the margin. Polling place type:

| place_type | sections |
|---|---|
| school_other | 55 |
| indigenous | 41 |
| rural_community | 7 |
| prison | 2 |
| quilombola | 1 |

The section-by-section list (state, municipality, polling place, type, eligible, turnout, results in 2026 T1, 2022 and 2018, manual voter release, closing, machine model) is in `results/fase2/A12_a12_secoes_zero_2026.csv`.

**Pre-registered verdict (kept, with the design caveat above):** detectable excess, irrelevant magnitude (<1% of the margin). **Corrected (post-registration):** REFUTED (no excess, ceiling <1% of the margin).

## A13. Count curve: inversions, linear stretches and the "video method"

The video by Prof. Marcelo Trindade, the data and the code of the "472 voting machines" were **not provided**; no source about him was located. For this part: **NOT REPRODUCIBLE**. What is tested is the general claim about the shape of the curve, with the series reconstructed from the tally order. As a precedent, a 2014 video with a similar argument was examined by [Agência Pública (O Truco)](https://apublica.org/2018/10/video-falso-diz-eleicoes-2014-fora-fraudadas/) and [Aos Fatos](https://www.aosfatos.org/noticias/bolsonaro-promete-provas-de-fraude-mas-apresenta-alegacoes-ja-desmentidas-sobre-urnas-eletronicas/); the fact-check noted that the stretch used had 0.13% of the votes counted.

**Method.** Leadership inversion = sign change of the accumulated margin between points from 1% of sections on. Linear stretch = window of 5% of sections with R² ≥ 0.99 and variation ≥ 0.15 p.p. of the share. Comparison with 1,000 random orders (A) and 1,000 realistic geographic orders (B: shuffles within the state keeping the state sequence). "Video method" (interpretation declared in the pre-registration): summing only the positive increments of the share curve.

| measure | 2026 T2 | 2026 T1 | 2022 T2 | 2018 T2 |
|---|---|---|---|---|
| year | 2026 | 2026 | 2022 | 2018 |
| round | 2 | 1 | 2 | 2 |
| sections | 499205 | 499206 | 472027 | 454447 |
| inversions_real | 2 | 0 | 3 | 0 |
| inversions_A_ci95 | (0.0, 0.0) | (0.0, 0.0) | (0.0, 0.0) | (0.0, 0.0) |
| inversions_B_ci95 | (3.0, 15.049999999999955) | (0.0, 0.0) | (1.0, 5.0) | (0.0, 0.0) |
| inversions_B_mean | 7.876 | 0.0 | 3.598 | 0.0 |
| linear_windows_real | 41 | 172 | 0 | 0 |
| linear_windows_A_ci95 | (0.0, 0.0) | (0.0, 0.0) | (0.0, 0.0) | (0.0, 0.0) |
| linear_windows_B_ci95 | (22.0, 65.0) | (154.0, 195.0) | (0.0, 0.0) | (0.0, 0.0) |
| linear_stretches_real | 4 | 6 | 0 | 0 |
| spliced_rises_final_share_real | 0.6469425603523131 | 0.5397041884725373 | 0.6814467158844435 | 0.9051426023024175 |
| spliced_rises_B_ci95 | (0.588, 0.606) | (0.52, 0.538) | (0.63, 0.662) | (0.8, 0.825) |
| spliced_rises_A_ci95 | (0.532, 0.55) | (0.505, 0.524) | (0.524, 0.542) | (0.468, 0.491) |
| final_share | 0.517851828842626 | 0.4898850552326951 | 0.5090240511717216 | 0.44869768719969416 |
| final_leader | PT | opponent | PT | opponent |

**Leadership inversions:** 2026 T2: 2 (geographic orders: (3.0, 15.049999999999955)); 2026 T1: 0 (geographic orders: (0.0, 0.0)); 2022 T2: 3 (geographic orders: (1.0, 5.0)); 2018 T2: 0 (geographic orders: (0.0, 0.0)). None of the available elections had exactly one comeback, and 2026/T2 had fewer comebacks than the mean of the simulated geographic orders. In a fully random order there is no comeback at all (the curve stays at the final value), which shows that the comebacks come from arrival geography.

**Real linear stretches of 2026 and the states that arrived in that interval:**

| year | round | from_pct_sections | to_pct_sections | share_variation_pp | dominant_states |
|---|---|---|---|---|---|
| 2026 | 2 | 61,3 | 67,8 | 0,31 | SP 30%, BA 12%, MG 11% |
| 2026 | 2 | 69,5 | 75,3 | 0,19 | SP 33%, MG 13%, BA 10% |
| 2026 | 2 | 88,3 | 94,7 | 0,19 | SP 29%, RJ 27%, BA 12% |
| 2026 | 2 | 89,9 | 94,9 | 0,15 | RJ 30%, SP 27%, BA 12% |
| 2026 | 1 | 66,8 | 72,1 | 0,30 | SP 27%, MG 13%, RJ 11% |
| 2026 | 1 | 70,8 | 76,3 | 0,31 | SP 28%, MG 13%, RJ 10% |
| 2026 | 1 | 72,0 | 77,3 | 0,31 | SP 26%, MG 13%, RJ 10% |
| 2026 | 1 | 73,0 | 78,5 | 0,38 | SP 24%, MG 13%, RJ 11% |
| 2026 | 1 | 75,2 | 80,7 | 0,33 | SP 25%, MG 14%, RJ 12% |
| 2026 | 1 | 79,8 | 99,3 | 1,91 | SP 17%, RJ 13%, BA 13% |

The real linear stretches are within the simulated range (real linear windows against the interval of geographic orders, in the table) and coincide with the arrival of SP, BA, MG and RJ.

**The spliced-rises method** produces a "victory" also in series without manipulation: in 2026/T2 it gives 64.7% to the PT in the real series and (0.588, 0.606) (fraction) in the geographic orders without manipulation, against the result of 51.8%; in 2018 it gives 90.5% to Haddad, who lost with 44.9%.

**The final total is independent of the order** (identical in all permutations) and matches the sum of the BUs and the official tally (H9).

**NOT RUN:** 2014 (no tally timestamp in the 2014 product) and 2002 to 2010 (no per-section data with timestamp in the open catalog); snapshots of the Results site; the video's "472 voting machines".

## A14. Receipt, tallying and publication on 10/25/2026

**Claim:** "70% of the voting machines tallied by 7:34pm, released gradually". The original video was not provided; the mentioned screenshot suggests 7.28%.

| year | round | time | pct_bu_received | pct_tallied | max |
|---|---|---|---|---|---|
| 2026 | 2 | 17:30 | 0,38 | 0,38 | n/a |
| 2026 | 2 | 18:00 | 0,38 | 0,38 | n/a |
| 2026 | 2 | 19:00 | 0,38 | 0,38 | n/a |
| 2026 | 2 | 19:34 | 7,77 | 7,74 | n/a |
| 2026 | 2 | 20:00 | 22,44 | 22,29 | n/a |
| 2026 | 2 | 21:00 | 88,63 | 88,25 | n/a |
| 2026 | 2 | 22:00 | 99,98 | 99,98 | n/a |
| 2026 | 2 | receipt -> 1st tally delay (min): median / p95 / max | 0,40 | 0,77 | 112,6 |
| 2022 | 2 | 17:30 | 8,04 | 7,65 | n/a |
| 2022 | 2 | 18:00 | 28,72 | 28,25 | n/a |
| 2022 | 2 | 19:00 | 84,14 | 83,04 | n/a |
| 2022 | 2 | 19:34 | 97,30 | 97,23 | n/a |
| 2022 | 2 | 20:00 | 98,98 | 98,96 | n/a |
| 2022 | 2 | 21:00 | 99,89 | 99,89 | n/a |
| 2022 | 2 | 22:00 | 99,99 | 99,99 | n/a |
| 2022 | 2 | receipt -> 1st tally delay (min): median / p95 / max | 0,60 | 1,15 | 940,1 |
| 2026 | 1 | 17:30 | 2,39 | 2,34 | n/a |
| 2026 | 1 | 18:00 | 15,04 | 13,15 | n/a |
| 2026 | 1 | 19:00 | 60,83 | 58,46 | n/a |
| 2026 | 1 | 19:34 | 85,15 | 84,94 | n/a |
| 2026 | 1 | 20:00 | 86,14 | 84,96 | n/a |
| 2026 | 1 | 21:00 | 98,30 | 98,21 | n/a |
| 2026 | 1 | 22:00 | 99,75 | 99,75 | n/a |
| 2026 | 1 | receipt -> 1st tally delay (min): median / p95 / max | 1,92 | 7,38 | 34,0 |

In 2026/T2, at 7:34pm, **7.77%** of the BUs had been received and **7.74%** had a first tally (the screenshot with 7.28% is of the same magnitude). The 70% mark was only reached after 8pm (around 8:45pm). The delay between receipt and first tally is short and stable (median under 1 minute; p95 under 1 minute in 2026/T2), that is, **there is no backlog of received and untallied BUs**. In 2022/T2, 84% of the BUs had already been received by 7pm, and in 2026/T1, 61%.

![Received and tallied](figs/a14_recebido_totalizado.png)

**Official explanation of the pause:** the STF decision was published at 5:03pm, the TSE memo to the TREs went out at 5:49pm, and publication was interrupted with 0.25% of sections tallied and resumed after 7pm (press; see [Legal basis](base-legal.md)). The data are compatible: 0.38% of sections tallied before 7pm.

**NOT RUN:** the **publication** curve (and the tallied → published delay): there are no public snapshots of the Results site with timestamps. Missing input: timestamped screenshots of the Results site or data from the system itself.

## A15. Voting machine model in 2022 (claim from the PL report / Cerimedo)

The report text was not provided; the claim is replicated as summarized (older models favored Lula). Against UE2020, within the same polling place, in 2022:

| year | model | specification | coef_pp | se_pp | sections | margin_votes (margin votes) | votes_ci95_low (margin votes) | votes_ci95_high (margin votes) | pct_margin |
|---|---|---|---|---|---|---|---|---|---|
| 2022 | UE2009 | T2 without T1 control (cross-section) | 0,208 | 0,295 | 46.159 | 46.479 | -82.288 | 175.246 | 1,05 |
| 2022 | UE2010 | T2 without T1 control (cross-section) | 0,208 | 0,294 | 92.781 | 92.445 | -163.287 | 348.178 | 2,09 |
| 2022 | UE2011 | T2 without T1 control (cross-section) | 0,171 | 0,298 | 26.432 | 21.411 | -51.977 | 94.800 | 0,48 |
| 2022 | UE2013 | T2 without T1 control (cross-section) | 0,287 | 0,300 | 24.294 | 33.113 | -34.757 | 100.983 | 0,75 |
| 2022 | UE2015 | T2 without T1 control (cross-section) | 0,235 | 0,293 | 85.159 | 97.518 | -140.529 | 335.565 | 2,20 |
| 2022 | UE2009 | T2 with T1 vote as control | -0,088 | 0,113 | 46.159 | -19.629 | -69.185 | 29.927 | -0,44 |
| 2022 | UE2010 | T2 with T1 vote as control | -0,079 | 0,113 | 92.781 | -35.085 | -133.155 | 62.985 | -0,79 |
| 2022 | UE2011 | T2 with T1 vote as control | -0,081 | 0,114 | 26.432 | -10.161 | -38.294 | 17.972 | -0,23 |
| 2022 | UE2013 | T2 with T1 vote as control | -0,081 | 0,117 | 24.294 | -9.359 | -35.726 | 17.008 | -0,21 |
| 2022 | UE2015 | T2 with T1 vote as control | -0,069 | 0,113 | 85.159 | -28.735 | -120.288 | 62.818 | -0,65 |
| 2022 | UE2009 | T1 (cross-section) | 0,353 | 0,301 | 46.159 | 78.700 | -53.044 | 210.445 | 1,78 |
| 2022 | UE2010 | T1 (cross-section) | 0,342 | 0,301 | 92.781 | 151.822 | -110.736 | 414.381 | 3,43 |
| 2022 | UE2011 | T1 (cross-section) | 0,300 | 0,306 | 26.432 | 37.586 | -37.696 | 112.869 | 0,85 |
| 2022 | UE2013 | T1 (cross-section) | 0,438 | 0,307 | 24.294 | 50.562 | -18.941 | 120.066 | 1,14 |
| 2022 | UE2015 | T1 (cross-section) | 0,362 | 0,300 | 85.159 | 150.302 | -93.540 | 394.143 | 3,39 |

Without the first-round control (the specification the claim assumes), the effect of UE2009 and UE2010 is positive for Lula, but small and **indistinguishable from zero** (the 95% interval includes zero); the same occurs in the first round itself (cross-section), which indicates composition of the sections that use each model. **With the first-round vote as control, the effect is negative and not significant** (−0.09 p.p.). In 2026:

| year | model | specification | coef_pp | se_pp | sections | margin_votes (margin votes) | votes_ci95_low (margin votes) | votes_ci95_high (margin votes) | pct_margin |
|---|---|---|---|---|---|---|---|---|---|
| 2026 | UE2013 | T2 without T1 control (cross-section) | 0,906 | 0,312 | 11.421 | 51.143 | 16.579 | 85.708 | 1,15 |
| 2026 | UE2015 | T2 without T1 control (cross-section) | 0,679 | 0,305 | 87.179 | 298.507 | 35.526 | 561.488 | 6,74 |
| 2026 | UE2022 | T2 without T1 control (cross-section) | -0,041 | 0,043 | 198.670 | -40.671 | -124.497 | 43.154 | -0,92 |
| 2026 | UE2013 | T2 with T1 vote as control | 0,071 | 0,148 | 11.421 | 4.026 | -12.393 | 20.445 | 0,09 |
| 2026 | UE2015 | T2 with T1 vote as control | -0,000 | 0,145 | 87.179 | -142 | -125.019 | 124.734 | -0,00 |
| 2026 | UE2022 | T2 with T1 vote as control | 0,003 | 0,021 | 198.670 | 3.230 | -37.374 | 43.834 | 0,07 |
| 2026 | UE2013 | T1 (cross-section) | 1,009 | 0,334 | 11.421 | 56.977 | 19.966 | 93.987 | 1,29 |
| 2026 | UE2015 | T1 (cross-section) | 0,822 | 0,328 | 87.179 | 361.143 | 78.437 | 643.849 | 8,15 |
| 2026 | UE2022 | T1 (cross-section) | -0,054 | 0,046 | 198.670 | -53.087 | -141.287 | 35.112 | -1,20 |

In 2026 no model differs from the UE2020 within the same polling place.

## Aggregate impact (H10 combined)

Only tests without a design caveat enter here. Sum of the worst-case ceilings of the tests with detected excess (Holm < 0.05) in each direction:

| aggregate | pro-Lula (margin votes) | % of margin | pro-Flávio (margin votes) | % of margin |
|---|---|---|---|---|
| excluding the rows with a design caveat (A1, A2, A3, A12) | 38.394 | 0,87% | 122.543 | 2,77% |
| with the corrected versions in place of the originals (0 of the 4 corrected versions show excess) | 38.394 | 0,87% | 122.543 | 2,77% |

Survivors (Holm < 0.05) without a design caveat:

| H | test | direction | p_holm | max_margin_votes (margin votes) | max_worst_case_votes (worst-case ceiling, margin votes) | pct_worst_case | verdict |
|---|---|---|---|---|---|---|---|
| H1 | S1 Flavio/Bolsonaro votes/eligible | OPO | 0,000 | 122.543 | 122.543 | 2,77% | EXCESS DETECTED and relevant (worst case >= 1% of the margin) |
| H2 | delta Lula vote (2022->2026) ~ delta manual rate, T2 | PT | 0,000 | 38.394 | 38.394 | 0,87% | detectable excess, irrelevant magnitude (<1% of the margin) |

The ceilings are not independent additive quantities and the PT and opponent directions do not offset each other. The margin is 4,430,191 votes.

## NOT RUN (summary)

| test | reason |
|---|---|
| A1/A1 2014/T2 | the 2014 detalhe_votacao_secao product has neither DT_RECEBIMENTO_BU_HOR_TSE nor DT_PRIM_TOT_PARCIAL_HOR_TSE; the 2014 BWeb only has the receipt date (no time) |
| A7/A7 2014 and other institutes | no final 2014 poll with a confirmed date was located, with a source; Quaest and Paraná Pesquisas of 10/24/2026 were not located with results; the TSE publishes only the poll registrations, without results |
| A9/A9 T1->T2 2026 | the 2026 turnout and abstention profile was published on 10/21/2026 and only covers the 1st round; the T1->T2 change by age band cannot be computed |
| A11/A11 state 2026 AP | insufficient sample for y_PT ~ ['x_pro_Flavio', 'x_esquerda', 'x_Renan', 'x_PCO', 'x_outros', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1914 |
| A11/A11 state 2026 RR | insufficient sample for y_PT ~ ['x_pro_Flavio', 'x_esquerda', 'x_Renan', 'x_PCO', 'x_outros', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1519 |
| A11/A11 state 2022 AP | insufficient sample for y_PT ~ ['x_terc1_n15', 'x_terc2_n12', 'x_outros_terc', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1740 |
| A11/A11 state 2022 RR | insufficient sample for y_PT ~ ['x_terc1_n15', 'x_terc2_n12', 'x_outros_terc', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1268 |
| A11/A11 state 2018 AP | insufficient sample for y_PT ~ ['x_terc1_n12', 'x_terc2_n45', 'x_outros_terc', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1632 |
| A11/A11 state 2018 RR | insufficient sample for y_PT ~ ['x_terc1_n12', 'x_terc2_n45', 'x_outros_terc', 'x_PT', 'x_OPO', 'x_BN'] / mun: n=1171 |
| A13/A13 2014/T2 and 2002-2010 | the 2014 detalhe_votacao_secao product has no tally timestamp and there is no per-section data with timestamps for 2002 to 2010 in the open catalog |
| A13/A13 video 'Prof. Marcelo Trindade' (472 voting machines, 60-65%) | NOT REPRODUCIBLE: the video, the data and the code of the '472 voting machines' were not provided |
| A13/A13/A14 snapshots of the Results site | there is no public series of timestamped snapshots of the Results site; only the per-section tally timestamp |
| A14/A14 publication curve and tallied->published delay | there are no public timestamped snapshots of the Results site; and the original video, in which the screenshot suggests 7.28%, was not provided |
| BU | NotRun: direct test with printed poll-receipts: no BU photo/PDF was provided (neither in Downloads nor in the project). Send images with the QR code visible or a zone;section;round;votes spreadsheet for cross-checking against the BWeb. A divergence of any size will be reported. |


## Appendix A: full register, with the caveat on the same row

| H | test | p_holm | pct_worst_case | verdict |
|---|---|---|---|---|
| H1 | S1 T2 with T1 lag, Lula% ~ manual rate | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| H1 | S0 without lag, Lula% ~ manual rate | 1,000 | 30,18% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| H1 | S0 without lag + controls (turnout, log eligible) | 1,000 | 29,99% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| H1 | S1 Flavio stronghold (Lula T1<40%) | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| H1 | S1 Lula stronghold (Lula T1>60%) | 1,000 | 0,13% | REFUTED (no excess, ceiling <1% of the margin) |
| H1 | S1 Lula votes/eligible | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| H1 | S1 Flavio/Bolsonaro votes/eligible | 0,000 | 2,77% | EXCESS DETECTED and relevant (worst case >= 1% of the margin) |
| H1 | S1 dose: manual rate >= 20% vs <20% (Lula share) | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| H2 | delta Lula vote (T1->T2) ~ delta manual rate, within the year | 1,000 | 0,04% | REFUTED (no excess, ceiling <1% of the margin) |
| H2 | delta Lula vote (2022->2026) ~ delta manual rate, T2 | 0,000 | 0,87% | detectable excess, irrelevant magnitude (<1% of the margin) |
| H4 | closes >= 15 min after 5pm: Lula% (w/ lag, place FE) | 1,000 | 0,03% | REFUTED (no excess, ceiling <1% of the margin) |
| H4 | closes >= 15 min after 5pm: Lula% (w/o lag, place FE) | 1,000 | 0,13% | REFUTED (no excess, ceiling <1% of the margin) |
| H4 | closes >= 60 min after 5pm: Lula% (w/ lag, place FE) | 1,000 | 0,09% | REFUTED (no excess, ceiling <1% of the margin) |
| H4 | closes >= 60 min after 5pm: Lula% (w/o lag, place FE) | 1,000 | 0,19% | REFUTED (no excess, ceiling <1% of the margin) |
| H4 | closes >= 115 min after 5pm: Lula% (w/ lag, place FE) | 1,000 | 0,09% | REFUTED (no excess, ceiling <1% of the margin) |
| H4 | closes >= 115 min after 5pm: Lula% (w/o lag, place FE) | 1,000 | 0,18% | REFUTED (no excess, ceiling <1% of the margin) |
| H5 | sections with turnout >=95% in T2/2026: excess over the expectation from composition (type x size, 2022 rates) | 0,270 | 0,43% | REFUTED (no excess, ceiling <1% of the margin) |
| H6 | new vs old sections of the same polling place: Lula% in T2 given T1 | 1,000 | 2,08% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| H7 | local upward outliers (pro-PT), /adjusted z/ > 3, per 10 thousand sections | 1,000 | 0,46% | REFUTED (no excess, ceiling <1% of the margin) |
| H7 | asymmetry: share of outliers that are pro-PT | 1,000 | 0,19% | REFUTED (no excess, ceiling <1% of the margin) |
| H8 | last digit: Cramer's V of PT in T2/2026 | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| H8 | last digit: Cramer's V of OPO in T2/2026 | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| H8 | exact whole percentage (PT and OPO, symmetric): obs/expected in T2/2026 | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A1 | count curve: maximum deviation of the real curve against permutation within the state (p.p. of the PT) | 0,000 | n/a (see caveat) | EXCESS DETECTED (shape test, no conversion to votes) (WITH DESIGN CAVEAT; no causal interpretation) |
| A2 | opponent loses absolute votes from T1 to T2 in sections with stable or rising turnout (% of sections) | 0,000 | n/a (see caveat) | EXCESS DETECTED (shape test, no conversion to votes) (WITH DESIGN CAVEAT; no causal interpretation) |
| A3 | ecological: fraction of the opponent's T1 voters that appears as PT votes in T2 | 0,002 | n/a (see caveat) | EXCESS DETECTED and relevant (worst case >= 1% of the margin) (WITH DESIGN CAVEAT; no causal interpretation) |
| A4 | sections with divergent BU, RDV or hash binding (voting machine file sample, 2026/T2) | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A5 | share of votes after the nominal time (log) and Lula% in T2 given T1, place FE | 1,000 | 0,09% | REFUTED (no excess, ceiling <1% of the margin) |
| A6 | actual machine differs from expected: Lula% in T2 given T1, place FE | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| A8 | sections with some office's total outside the rule (total = turnout x seats), 2026 T1+T2 | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A9 | zones with optional-voter turnout outside [Q1-3 IQR, Q3+3 IQR] of 2022/T1 (% of zones), 1st round only | 1,000 | n/a | NO EXCESS (shape test, no conversion to votes) |
| A10 | machine model UE2013 against UE2020, same polling place: Lula% in T2 given T1 | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| A10 | machine model UE2015 against UE2020, same polling place: Lula% in T2 given T1 | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| A10 | machine model UE2022 against UE2020, same polling place: Lula% in T2 given T1 | 1,000 | 3,11% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |
| A11 | pro-Flavio block in T1 (Zema, Caiado, Cury, Clariana) -> PT votes in T2 per eligible voter, municipality FE | 1,000 | 0,00% | REFUTED (no excess, ceiling <1% of the margin) |
| A12 | sections with zero votes for the opponent in T2: observed/expected ratio (p from T1) | 0,025 | n/a (see caveat) | detectable excess, irrelevant magnitude (<1% of the margin) (WITH DESIGN CAVEAT; no causal interpretation) |
| A15 | 2022: UE2009 against UE2020, same polling place: Lula% in T2 given T1 | 1,000 | 0,45% | REFUTED (no excess, ceiling <1% of the margin) |
| A15 | 2022: UE2010 against UE2020, same polling place: Lula% in T2 given T1 | 1,000 | 1,09% | INCONCLUSIVE (no excess, but ceiling >=1% of the margin) |

Corrected versions (post-registration, [Addendum 6](preregistro.md)):

| H | test | p_holm | verdict |
|---|---|---|---|
| A1-corrected | count curve: maximum deviation against null D (municipalities in random order within the state), from 10% of sections on (p.p. of the PT) | 1,000 | NO EXCESS (shape test, no conversion to votes) |
| A2-corrected | first-round leader loses absolute votes (% of sections, standardized by the third-parties/leader ratio with 2026 weights) | 1,000 | NO EXCESS (shape test, no conversion to votes) |
| A3-corrected | opponent (T1) to PT (T2) transition rate, constrained to [0,1], by municipality, with bootstrap | 1,000 | REFUTED (no excess, ceiling <1% of the margin) |
| A12-corrected | sections with zero votes for the opponent in T2: observed/expected ratio (p from the neighbors of the same polling place, leave-one-out) | 1,000 | REFUTED (no excess, ceiling <1% of the margin) |

## Appendix B: Aggregate without causal interpretation

> **This table does not measure manipulated votes.** It sums the worst-case ceilings of every row in the register, including A3, whose ceiling comes from an ecological coefficient that is negative in all years, multiplied by a factor and by the opponent's first-round votes. The ceiling grows with the size of the universe and **not** with any evidence of vote switching. It is here only so that anyone doing the naive sum finds the number with the explanation. For the aggregate impact use the "Aggregate impact (H10 combined)" section.

| direction | sum of the ceilings of all register rows (votes) | % of margin | what enters |
|---|---|---|---|
| pro-Lula | 9.425.488 | 212,76% | no causal interpretation: includes A3 |
| pro-Flávio | 122.543 | 2,77% | same as the aggregate without caveats |

Why the A3 row inflates the total: the ceiling is factor × max(0, difference + 1.645·se) × opponent's first-round votes. Since all coefficients in the four years are negative (none measures conversion), the "difference" between 2026 and the placebo is a difference between negative numbers from different geographies, and the product by the opponent's 56 million votes yields millions of votes without a single switched vote. The corrected version (rate constrained to 0 to 1) gives 0 in all four years.
