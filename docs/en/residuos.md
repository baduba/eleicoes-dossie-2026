# Open questions (residuals)

> **Items the tests could neither explain nor confirm. They are not evidence of anything, on either side: they are gaps that only new data can close, and they are here for transparency and for future investigation.**

This page collects every result classified as inconclusive, "detectable excess" or "excess detected", and every residual without an identified cause. The central estimates and 95% intervals use a normal approximation over the standard error of the contrast against the most demanding placebo (they are neither bootstrap nor Bayesian). The **worst-case ceiling** uses the loosest placebo. No probability is assigned to hypotheses about the process; only measured quantities appear (excess votes, year-over-year difference). Official margin: 4,430,191 votes.

## H1: Association between the manual voter release rate and Flávio's votes per eligible voter in the runoff, beyond the first round

- **Registry line:** S1 Flavio/Bolsonaro votos/apto
- **Verdict under the pre-registered criterion:** EXCESS DETECTED and relevant (worst case >= 1% of the margin)
- **Direction of the effect:** in favor of Flávio
- **Central estimate:** 101,285 margin votes (95% CI 75,956 to 126,614), against the most demanding placebo (2022/runoff)
- **Worst-case ceiling:** 122,543 votes (2.77% of the margin)
- **Mundane explanations tested:** voting machine model effect (A10); first-round composition with all candidates and blank/null ballots (the coefficient increases); turnout
- **Not tested:** age and education by section; profile of the voter who needs manual release
- **What would resolve it:** per-section profile (age, education) or the polling-station tally-sheet records
- **Cause:** not identified.

## H5: Sections with turnout ≥95%: 2.5 times the level expected from location-type and size composition; already present in the first round

- **Registry line:** secoes com comparecimento >=95% no T2/2026: excesso sobre o esperado pela composicao (tipo x tamanho, taxas 2022)
- **Verdict under the pre-registered criterion:** REFUTED (no excess, ceiling <1% of the margin)
- **Direction of the effect:** turnout (effect possible in either direction; ceiling computed as if every extra vote were for the PT)
- **Central estimate:** 11,266 margin votes (95% CI 2,023 to 20,508), against the most demanding placebo (same test in the 2026 first round)
- **Worst-case ceiling:** 19,023 votes (0.43% of the margin)
- **Mundane explanations tested:** location type, size, new section, state (UF), manual release rate, closing delay, numerator versus denominator (in older sections the numerator rises 6%)
- **Not tested:** voter-registration cancellations and the electoral-roll revision between 2022 and 2026; age composition by section (turnout among voters over 80 grows faster than eligible voters, A9)
- **What would resolve it:** per-section registration before and after the electoral-roll revision
- **Cause:** not identified.

## H6: New sections have +0.54 p.p. for Lula in the runoff given the first round (2018: +1.34; 2022: 0)

- **Registry line:** secoes novas vs antigas do mesmo local: Lula% no T2 dado o T1
- **Verdict under the pre-registered criterion:** INCONCLUSIVE (no excess, but ceiling >=1% of the margin)
- **Direction of the effect:** in favor of Lula
- **Central estimate:** -130,811 margin votes (95% CI -140,934 to -120,687), against the most demanding placebo (2018/runoff)
- **Worst-case ceiling:** 92,023 votes (2.08% of the margin)
- **Mundane explanations tested:** interaction with the first round, size and turnout (the coefficient is stable)
- **Not tested:** composition by age and income; origin of the voters transferred to the new sections
- **What would resolve it:** history of voter reassignment by section
- **Cause:** not identified.

## H1: Association between the manual release rate and the Lula vote within the same location, equal in the first and second rounds of 2026 (0.07) and higher than in 2022

- **Registry line:** S0 sem lag, Lula% ~ taxa manual
- **Verdict under the pre-registered criterion:** INCONCLUSIVE (no excess, but ceiling >=1% of the margin)
- **Direction of the effect:** in favor of Lula (association, not effect)
- **Central estimate:** -76,711 margin votes (95% CI -191,548 to 38,125), against the most demanding placebo (2026/first round)
- **Worst-case ceiling:** 1,337,198 votes (30.18% of the margin)
- **Mundane explanations tested:** controls for turnout, size and voting machine model: the association remains
- **Not tested:** per-section profile
- **What would resolve it:** per-section profile; causal model with an instrument for biometric failure
- **Cause:** not identified.

## H2: Year-over-year change in the Lula vote against the change in the manual release rate: runoff versus first round as an imperfect placebo

- **Registry line:** delta voto Lula (2022->2026) ~ delta taxa manual, T2
- **Verdict under the pre-registered criterion:** detectable excess, irrelevant magnitude (<1% of the margin)
- **Direction of the effect:** in favor of Lula
- **Central estimate:** 30,332 margin votes (95% CI 20,726 to 39,938), against the most demanding placebo (same test in the first round)
- **Worst-case ceiling:** 38,394 votes (0.87% of the margin)
- **Mundane explanations tested:** municipalities with biometrics in both years; the 2026 first round has different candidates from 2022
- **Not tested:** n/a
- **What would resolve it:** a placebo with comparable candidates
- **Cause:** not identified.

## A1: Deviation of the counting curve against within-state permutation (shape test; no vote conversion)

- **Registry line:** curva de apuracao: desvio maximo da curva real contra permutacao dentro da UF (p.p. do PT)
- **DESIGN CAVEAT (read first):** the pre-registered design of this line produces the excess label without manipulation (demonstration and correction in [Phase 2 Results](resultados-fase2.md)). The label below **does not indicate manipulation**.
- **Pre-registered (kept):** EXCESS DETECTED (shape test, no vote conversion), with the design caveat above (envelope B (within-state permutation) is rejected in all four years; from 10% of sections onward the 2026/runoff deviation falls below the placebos (post-hoc analysis))
- **Corrected (post-registration):** NO EXCESS (shape test, no vote conversion)
- **Direction of the effect:** n/a
- **Vote estimate:** no causal interpretation on this line; values in the Appendix "Aggregate without causal interpretation" of Phase 2 Results.
- **Mundane explanations tested:** the envelope is rejected in every year; from 10% of sections onward 2026/runoff falls below the placebos
- **Not tested:** snapshots of the Resultados website
- **What would resolve it:** the release series with timestamps
- **Cause:** the test design (see caveat); there is no residual to explain on this line.

## A2: Frequency of sections in which the opponent loses votes in absolute terms (11.8% of sections; shape test)

- **Registry line:** oponente perde votos absolutos do T1 ao T2 em secao com comparecimento estavel ou crescente (% das secoes)
- **DESIGN CAVEAT (read first):** the pre-registered design of this line produces the excess label without manipulation (demonstration and correction in [Phase 2 Results](resultados-fase2.md)). The label below **does not indicate manipulation**.
- **Pre-registered (kept):** EXCESS DETECTED (shape test, no vote conversion), with the design caveat above (the role-based placebo (opponent) is inadequate: in 2022 the PT, the first-round leader, lost votes in 12.6% of sections, a mirror image of the opponent's 11.8% in 2026 (post-hoc analysis))
- **Corrected (post-registration):** NO EXCESS (shape test, no vote conversion)
- **Direction of the effect:** n/a
- **Vote estimate:** no causal interpretation on this line; values in the Appendix "Aggregate without causal interpretation" of Phase 2 Results.
- **Mundane explanations tested:** mirror: in 2022 the PT lost in 12.6%; by third-party/candidate band the frequencies are similar
- **Not tested:** why the first-round leader loses absolute votes where there are few third parties
- **What would resolve it:** individual-level survey (panel)
- **Cause:** the test design (see caveat); there is no residual to explain on this line.

## A3: Ecological coefficient of opponent in the first round → PT in the runoff (2026 is the least negative; with municipality fixed effects, the most negative)

- **Registry line:** ecologica: fracao de eleitores do oponente no T1 que aparece como voto no PT no T2
- **DESIGN CAVEAT (read first):** the pre-registered design of this line produces the excess label without manipulation (demonstration and correction in [Phase 2 Results](resultados-fase2.md)). The label below **does not indicate manipulation**.
- **Pre-registered (kept):** EXCESS DETECTED and relevant (worst case >= 1% of the margin), with the design caveat above (coefficients negative in every year (they do not measure conversion); with municipality fixed effects the 2026 coefficient is the most negative (post-hoc analysis))
- **Corrected (post-registration):** REFUTED (no excess, ceiling <1% of the margin)
- **Direction of the effect:** in favor of Lula (year-over-year difference)
- **Vote estimate:** no causal interpretation on this line; values in the Appendix "Aggregate without causal interpretation" of Phase 2 Results.
- **Mundane explanations tested:** municipality fixed effects; accounting by identity
- **Not tested:** individual-level conversion (ballot secrecy)
- **What would resolve it:** a voter panel or post-election survey data
- **Cause:** the test design (see caveat); there is no residual to explain on this line.

## A10: New voting machine model (UE2022) with no counterpart in 2022, worst-case ceiling above 1% of the margin because it is imprecise

- **Registry line:** modelo de urna UE2022 contra UE2020, mesmo local: Lula% no T2 dado o T1
- **Verdict under the pre-registered criterion:** INCONCLUSIVE (no excess, but ceiling >=1% of the margin)
- **Direction of the effect:** n/a
- **Central estimate:** 56,317 margin votes (95% CI -40,780 to 153,414), against the most demanding placebo (2026/first round (no lag, same sections))
- **Worst-case ceiling:** 137,809 votes (3.11% of the margin)
- **Mundane explanations tested:** within the same location, the coefficient is 0.0000
- **Not tested:** n/a
- **What would resolve it:** more sections per model
- **Cause:** not identified.

## A11: Ecological coefficient of the bloc that supported Flávio toward PT votes, against the placebos

- **Registry line:** bloco pro-Flavio no T1 (Zema, Caiado, Cury, Clariana) -> votos do PT no T2 por apto, EF de municipio
- **Verdict under the pre-registered criterion:** REFUTED (no excess, ceiling <1% of the margin) (design caveat: the design compares blocs of different composition across years; ecological coefficients do not measure individual conversion)
- **Direction of the effect:** see A11
- **Central estimate:** -5,185,109 margin votes (95% CI -5,750,811 to -4,619,407), against the most demanding placebo (2018: largest third-party candidate (terc1_n12))
- **Worst-case ceiling:** 0 votes (0.00% of the margin)
- **Mundane explanations tested:** municipality fixed effects; restricted Goodman regression
- **Not tested:** composition of the blocs and endorsements without a source (left, Clariana, Rui Costa Pimenta)
- **What would resolve it:** a post-election survey
- **Cause:** not identified.

## A12: Sections with zero votes for the opponent (observed/expected ratio)

- **Registry line:** secoes com zero voto para o oponente no T2: razao observado/esperado (p do T1)
- **DESIGN CAVEAT (read first):** the pre-registered design of this line produces the excess label without manipulation (demonstration and correction in [Phase 2 Results](resultados-fase2.md)). The label below **does not indicate manipulation**.
- **Pre-registered (kept):** detectable excess, irrelevant magnitude (<1% of the margin), with the design caveat above (the placebos have an observed/expected ratio below 1 because the estimator of p from the first round is inadequate where there are relevant third parties in the first round (2018, 2014); the direct observed-versus-expected test in 2026 (z=1.33) is not significant (post-hoc analysis))
- **Corrected (post-registration):** REFUTED (no excess, ceiling <1% of the margin)
- **Direction of the effect:** in favor of Lula
- **Vote estimate:** no causal interpretation on this line; values in the Appendix "Aggregate without causal interpretation" of Phase 2 Results.
- **Mundane explanations tested:** expected from the section's first-round vote and from neighbors at the same location
- **Not tested:** n/a
- **What would resolve it:** n/a
- **Cause:** the test design (see caveat); there is no residual to explain on this line.

## A5: Association between votes cast after the nominal closing time and Lula% at the same location

- **Registry line:** share de votos depois do horario nominal (log) e Lula% no T2 dado o T1, EF de local
- **Verdict under the pre-registered criterion:** REFUTED (no excess, ceiling <1% of the margin)
- **Direction of the effect:** see A5
- **Central estimate:** 1,585 margin votes (95% CI -1,254 to 4,424), against the most demanding placebo (2022/runoff (same sections))
- **Worst-case ceiling:** 3,968 votes (0.09% of the margin)
- **Mundane explanations tested:** same test on the same sections in 2022
- **Not tested:** sections without a voting machine log file
- **What would resolve it:** the log for all sections
- **Cause:** not identified.

## A15: Voting machine model UE2009/UE2010 in 2022 versus UE2020

- **Registry line:** 2022: UE2009 contra UE2020, mesmo local: Lula% no T2 dado o T1
- **Verdict under the pre-registered criterion:** REFUTED (no excess, ceiling <1% of the margin)
- **Direction of the effect:** in favor of Lula
- **Central estimate:** -98,333 margin votes (95% CI -239,095 to 42,429), against the most demanding placebo (2022/first round (cross-section))
- **Worst-case ceiling:** 19,807 votes (0.45% of the margin)
- **Mundane explanations tested:** the effect without the first-round control is composition (it also appears in the first round); with the first round, it is null
- **Not tested:** n/a
- **What would resolve it:** n/a
- **Cause:** not identified.

## Corrected A1, 2026 first round: final stretch of the curve outside the envelope

- **What is observed:** the first-round curve stays outside the corrected null envelope for 240 consecutive points (from 76% to 100% of sections, from 19:18 to 22:28 on Oct 4, 2026). The pre-registered target of A1 is the runoff; this line is post-hoc analysis.
- **Direction of the effect:** Lula's share below the null median, with the deviation decreasing toward zero; largest deviation before the 19:00–20:00 window.
- **Vote estimate:** not convertible into votes (shape test; the final sum is identical under any ordering).
- **Mundane explanations tested:** coincidence with the 19:00–20:00 congestion window: partial (91 of the 241 points; the run starts within the window and continues after it); composition by state: compatible, not demonstrated. See [A18](a18-alteracao-no-meio.md).
- **Not tested:** the ordering of municipalities within each state by size and by voting profile.
- **What would resolve it:** the Sistot reception log (not public) and the actual transmission order by municipality.
- **Cause:** not identified.

## Aggregate sum: how many votes, all residuals together?

> **Unit: margin votes** (change in the Lula-minus-Flávio difference; switching one vote changes the margin by 2; definition in [Methodology](metodologia.md)). All numbers below must be read against the margin of 4,430,191. To overturn the result, the set of **pro-Lula** effects would have to sum to at least that amount; pro-Flávio effects run in the opposite direction and do not enter this account.

| sum | pro-Lula (margin votes) | % of the margin (pro-Lula) | pro-Flávio (margin votes) | % of the margin (pro-Flávio) |
|---|---|---|---|---|
| **(1) Measured excess: sum of the positive central estimates of the items on this page** (against the most demanding placebo; negative ones do not offset) | **99,499** | **2.25%** | **101,285** | **2.29%** |
| (2) Worst-case ceilings of the items on this page | 1,648,221 (worst-case ceiling, not an estimate) | 37.2% (worst-case ceiling, not an estimate) | 122,543 (worst-case ceiling, not an estimate) | 2.8% (worst-case ceiling, not an estimate) |
| (3) Same as (2), excluding the largest single item (ceiling dominated by imprecision, see below) | 311,023 (worst-case ceiling, not an estimate) | 7.0% (worst-case ceiling, not an estimate) | 122,543 (worst-case ceiling, not an estimate) | 2.8% (worst-case ceiling, not an estimate) |

**Reading.** Line (1) is the excess the data show: about 99,499 pro-Lula margin votes and 101,285 pro-Flávio, i.e., 2.2% and 2.3% of the margin. Lines (2) and (3) are **worst-case ceilings, not estimates**: they always use the loosest placebo and sum as if everything were independent. In (2), the item with the largest ceiling (1,337,198 margin votes) is a specification without a first-round control whose ceiling comes from the **imprecision** of the test (the verdict is inconclusive, not excess); without it, the total falls to 7.0% of the margin. No sum reaches 4,430,191. This limit holds for what the tests measure; what lies outside measurement (the unpublished links) remains open.

What this does **not** measure: a coherent alteration of votes across all published files, which these tests cannot detect (see [A18](a18-alteracao-no-meio.md) and [A19](a19-voto-digitado.md)). Also excluded is the aggregate of lines with a design caveat, which has no causal interpretation (Appendix B of [Phase 2 Results](resultados-fase2.md)). The naive sum of all registry lines appears only in the appendix below.

## Items without a registry line

- **Turnout among elderly voters (A9):** turnout of voters over 80 (optional voting) grows faster than eligible voters in that band between 2022 and 2026 in the first round. Not convertible into votes; cause not identified; the 2026/runoff profile and the history of voter-registration cancellations would resolve it.
- **Arrival of BUs (poll-receipts) on Oct 25, 2026:** 99.6% of BUs reached the TSE after 19:00, while 98.2% of sections had closed within 15 minutes after 17:00. Explained by the pause documented by the press; the official source was not released.

## Appendix: Naive sum with double counting, without interpretation

> **This sum does not measure altered votes.** It sums the worst-case ceilings of **all** 27 pro-Lula registry lines (excluding the four with a design caveat) that have a vote conversion, counting the same sections and the same specifications multiple times (for example, the manual release test in several specifications and the late-closing test in six). Unit: margin votes. Worst-case ceiling, not an estimate.

| sum | pro-Lula (margin votes) | % of the margin | pro-Flávio (margin votes) |
|---|---|---|---|
| Naive sum with double counting, without interpretation (worst-case ceiling, not an estimate) | 3,092,826 | 69.8% | 122,543 |

Even with double counting, the sum does not reach 4,430,191 margin votes.
