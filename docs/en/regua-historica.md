# Historical benchmark (2014, 2018, 2022, 2026)

Forecasts and the "similar" criterion fixed in Addendum 1 of the pre-registration: ratio between 0.8 and 1.25 for rates and counts; difference < 0.02 for correlations (M5b) and < 0.005 for Cramér's V. Pattern A: 2014, 2022, and 2026 similar to each other and 2018 different from the three. B: 2014 similar to 2018, 2022 similar to 2026, the pairs different from each other. C: all four similar.

**Runoff (2nd round):**

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

Runoff summary: A = 0, B = 0, C = 5, none = 7 of 12 metrics. First-round summary: A = 3, B = 0, C = 3, none = 6.

**Trios of mutually similar years** (all three comparisons within the criterion), runoff:

| trio | mutually_similar_metrics | metrics_that_do_not_fit |
|---|---|---|
| 2014 + 2018 + 2022 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2018 + 2026 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2014 + 2022 + 2026 | 5 of 12 | M5a_PT, M5a_OPO, M5c, M7a_up, M7b, M5b_PT, M5b_OPO |
| 2018 + 2022 + 2026 | 9 of 12 | M5a_PT, M5a_OPO, M5c |

Note: `M5b_OPO` and `M8b_OPO` repeat `M5b_PT` and `M8b_PT` by construction (the two shares sum to 1), so the 12 rows contain 10 independent metrics. Excluding the repetitions, C holds in 4 of 10, and 2/3 would be 7. The conclusion does not change.


**Verdict under the fixed criterion: none of the three patterns fits.** The threshold of 2/3 of the metrics (8 of 12) is not reached by A, B, or C (C reaches 5). The 2018, 2022, and 2026 trio is the most homogeneous in the table; the metrics in which it is not homogeneous are the tail metrics (turnout >= 90% with vote share >= 90%, and turnout >= 95%), which are precisely those of the residue described in 3.6. This trio-based reading is a post-hoc analysis, not pre-registered. The M5c metric (sections with turnout >= 95%) has no monotonic pattern: 242 per 100 thousand sections in 2014, 111 in 2018, 49 in 2022, and 128 in 2026; 2022 is the series minimum and 2026 falls between 2018 and 2014.

The A/B/C classification depends on the fixed numeric criterion, which is arbitrary; that is why the ratios are shown in the table.
