# Methodology

## Principles
1. Only numbers produced by a versioned script over official data with a verified hash, or claims with a cited source, are admitted.
2. Hypothesis before data: "if there is manipulation I expect X / if there is not I expect Y" predictions are in [Pre-registration](preregistro.md), written before each analysis block was run (Phase 1; Addenda 1 to 3) and before the Phase 2 analyses (Addendum 4).
3. Every test has a placebo (2014, 2018, 2022, the 2026 first round) and is symmetric (PT and opponent).
4. Null results receive the same prominence as positive results. A test that could not be run is listed as NOT EXECUTED, with the reason and the missing input.
5. Changes made after seeing results are published as such (addenda and [Changelog](changelog.md)).

## Data
- **BWeb** (poll-receipt per station section) for 2014, 2018, 2022 and 2026, first and second rounds, 224 zips per UF (state). SHA-512 hash (2018 to 2026) or SHA-1 (2014) verified against the one published by the TSE.
- `votacao_secao`, `detalhe_votacao_secao`, `votacao_candidato_munzona`, turnout and abstention profiles, expected matchings, registered polls.
- **Voting machine files** (BU, RDV, image, signature and log) from the "files transmitted for tabulation" set: sample per section (see A4 and A5).
- Full list with URL and hash in `data/`.

## Units (read before the numbers)
- **Margin votes** is the unit of every ceiling, central estimate and vote aggregate in this audit. It is the change in the Lula-minus-Flávio difference: moving one vote from one candidate to the other changes the margin by 2; one additional vote for a candidate, without taking it from the other, changes it by 1. The ceiling formula already includes the factor 2 (parameter `fator`), and the official margin, 4,430,191, is in the same unit. To overturn the result, the margin would have to fall by at least 4,430,191, equivalent to 2,215,096 switched votes.
- **Votes (count)** is the plain number of votes (for example, the 23 thousand votes after 5 p.m. in A5 or the 8.6 million manual voter releases). Every table and every headline figure carries the unit label. Counts and margin votes **must not** be added or compared without conversion.
- The H10 aggregate (38,394 pro-Lula and 122,543 pro-Flávio) and the sums in Open Questions are in the **same unit** (margin votes), because both come from the `votos_max_pior_caso` and `votos_central` columns of the test registry.

## Statistics
- **Polling-place fixed effect** (school): the comparison is between sections at the same polling place, which absorbs geography, population and the profile of the location.
- **First-round control:** when the outcome is the second round, the section's own first-round vote enters as a control.
- **Intersection-union test against the placebos:** an effect counts as excess only if it exceeds **each** placebo. The "excess" p-value is one-sided. Holm and Benjamini-Hochberg correction across all tests in the registry.
- **Ceiling in votes:** `fator x max(0, difference + 1.645 x standard error) x exposure`, the maximum number of margin votes the phenomenon could explain if it were causal. Two ceilings: against the most demanding placebo and against the loosest one (worst case).
- **Verdict rule:** *excess detected and relevant* (Holm < 0.05 and worst case >= 1% of the 4,430,191 margin); *detectable excess, irrelevant magnitude* (Holm < 0.05 and < 1%); *refuted* (Holm >= 0.05 and < 1%); *inconclusive* (Holm >= 0.05 and >= 1%). Form tests, with no conversion to votes, are labeled separately.
- **Design caveat:** when a later control shows that the pre-registered design was inadequate, the line is kept as it came out and flagged; the aggregate impact (H10) is published with and without those lines.

## What this audit is not
It is not an official expert report, an official forensic examination, or a certified document: no authority has certified it. It is an independent, reproducible audit, made so that any expert, on any side, can repeat and challenge it.

## How to challenge
Open an *issue* in the repository with the contested figure or table, the script that reproduces your version, and the source data. Accepted corrections go into the [Changelog](changelog.md).
