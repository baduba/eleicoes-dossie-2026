# Pre-registration of hypotheses (written before opening any BWeb file)

Written on: 2026-10-28, before downloading the `bweb_*` files.

Transparency about what was already known at the time of writing: the totals, the unanimity, the Benford analysis, the turnout jump,
the count of sections with turnout >= 95% (639 in T2/2026) and the proxy by BU (poll-receipt) receipt time (+1,1 p.p.
against +1,7 to +1,9 in the placebos) came from the `detalhe_votacao_secao`/`votacao_secao` datasets. Nothing about manual voter release,
opening/closing times or vote type had been seen yet.

Notation: M = official margin = 4.430.191 votes. "Effect" = votes that the phenomenon could explain, at most.
General verdict criterion: a hypothesis is only SUSTAINED if (a) the effect in 2026/T2 is statistically distinct from the
three placebos (2022 T1, 2022 T2, 2026 T1), (b) it survives Holm/BH, (c) it survives the geographic control and (d) it is not
explained by any tested mundane explanation. Otherwise: REFUTED (estimated effect within the noise and/or
equal to the placebos) or INCONCLUSIVE (insufficient data or low power).

| H | If there is fraud, I expect | If there is none, I expect |
|---|---|---|
| H1 manual release x Lula vote | positive coefficient in 2026/T2, larger than in the placebos, increasing dose-response curve in the high bands, absent for a symmetric Flávio | coefficient with the same sign and similar magnitude in the 4 placebos (manual release correlates with rural/poor profile), no dose-response specific to 2026/T2 |
| H2 increase in manual release | manual rate rises from 2022 to 2026 in the same sections and the rise predicts the T1->T2 change in the Lula vote only in 2026 | diffuse rise linked to the biometrics change (voter registry), predicts the T1->T2 change equally in 2022 or nothing |
| H3 closing | large mass of sections closes after 7 p.m. or a relevant share of votes after 5 p.m. concentrated in few sections | almost all sections close at 7 p.m. or shortly after (general extension), logs/times consistent with the TSE's decision; the report's table not reproducible from this source |
| H4 closed after 7 p.m. | Lula vote and T1->T2 change larger in those sections in 2026, not in 2022 in the same sections | difference equal to the placebo (sections that close late are rural/large/with queues and already voted differently) |
| H5 639 sections >= 95% | majority old, with low 2022 turnout, high manual release, atypical closing, Lula-skew only in T2 | majority new, small, atypical venue (indigenous, prison, hospital, quilombo), already visible in T1/2026, skew from the local stronghold |
| H6 new sections | vote/turnout deviates from the old sections of the same venue | equal to the old sections of the same venue (venue fixed effect absorbs it) |
| H7 local outliers | excess of positive outliers for Lula in 2026/T2, with no mirror | count of |z|>3 outliers in both directions close to 2022 and symmetric |
| H8 digits | non-uniform last digit / excess of round percentages in 2026/T2 | uniform (corrected p > 0,05) as in 2022; caveat: small sections generate natural rounding |
| H9 consistency | sum of sections != official tabulation | exact sum of sections = 64.256.232 and 59.826.041 (already confirmed in the voting CSVs); municipality-by-municipality comparison only if the TSE publishes it |
| H10 aggregate impact | sum of the maximum excesses that survive >= order of the margin | small sum (< 1% of M) or zero |

Global prediction: null for H1, H2, H4, H6, H7, H8; H3 and H5 are characterizations, not fraud tests.
If any of these predictions fails, that is reported as is.

---

# Addendum 1: historical ruler (written before downloading or opening any 2014 and 2018 data)

Scope: H5 (Klimek), H7 (local outliers) and H8 (digits) in 2014, 2018, 2022 and 2026, T1 and T2.
Candidate mapping (prior knowledge, to be confirmed in the data): column `lula` = candidate no. 13 (PT:
Dilma 2014, Haddad 2018, Lula 2022 and 2026); column `dir` = the runoff opponent (Aécio no. 45 in 2014,
Bolsonaro no. 17 in 2018, Bolsonaro no. 22 in 2022, Flávio no. 22 in 2026).

## Metrics fixed before looking (per year x round x candidate)
- M5a: fraction of sections (>= 30 valid votes) in the corner turnout >= 90% and candidate vote >= 90%.
- M5b: correlation between turnout and candidate vote, within the polling place (residual of the fixed effect).
- M5c: number of sections with turnout >= 95% per 100,000 sections.
- M7a: rate per 10,000 sections of |z| > 3 upward and downward (z = deviation of the section from the mean of the other
  sections of the same venue, adjusted for binomial variance and for overdispersion estimated within the election itself).
- M7b: ratio between upward and downward outliers (symmetry).
- M8a: chi-square of the last digit (counts of each candidate with >= 20 votes) and Cramér's V.
- M8b: observed/expected ratio of sections with an exactly round percentage.

## Criterion for "similar" (fixed now, arbitrary but declared)
Two elections are "similar" on a metric if the ratio between them (M5a, M5c, M7a, M8b) is in [0,8; 1,25]
or, for M5b, M7b and Cramér's V, the absolute difference is < 0,02 (M5b), ratio in [0,8; 1,25] (M7b)
and < 0,005 (V). A historical hypothesis is assessed by the majority (>= 2/3) of the metrics, per PT candidate and opponent.

## Predictions (which pattern each one implies)
- A "deviation always, except 2018": 2014, 2022 and 2026 similar to each other and 2018 different from the three.
- B "deviation starting in 2022": 2014 and 2018 similar to each other, 2022 and 2026 similar to each other, the two pairs different.
- C "no deviation": the four years similar to each other, after adjusting for geography (venue fixed effect).
I am required to record that my expectation is C, with the caveat that the criterion above may classify as
"different" years that changed for mundane reasons (average section size, biometrics, redistricting); that is why
I also report the numeric ratios, not only the A/B/C verdict. If none of the three patterns fits
(e.g., only 2014 different), I report "none of the three" and do not force a fit.

## Biometrics (protocol)
The comparison of manual release between years uses only sections in municipalities with biometrics in both years, defined as
a municipality with a sum of `QT_ELEI_BIOM_SEM_HABILITACAO` (or the year's synonym) > 0 in both. The measure is, by definition of
the TSE data dictionary, "voters with registered biometrics who were not enabled through it", not the total of manual voter
releases. I also report the unfiltered version.

## Direct test with printed poll-receipts
It will only be run if photos/PDFs of BUs are provided. Procedure: identify zone/section/round (QR code or
transcription), cross-check against BWeb and report every discrepancy in votes, registered voters, turnout, opening and closing.
Without input, the test ends with an explicit ERROR "no printed poll-receipts provided" and is listed as NOT EXECUTED.

---

# Addendum 2: method corrections made AFTER seeing the first results of H1 to H4 (2022/2026)

Written on 2026-10-28, after the first round of H1-H4 and BEFORE running H5-H8 and any 2014/2018 data.

1. My error in the first version: the "2026/T2 vs placebos" contrast used the inverse-variance-weighted mean of the three
   placebos. Since the placebos are heterogeneous (the manual x Lula association is 0,074 in 2026/T1 and ~0 in 2022), the mean was
   dominated by the 2022 placebos and hid the most relevant placebo (2026/T1), producing a false line
   ("21,8% of the margin"). Corrected to an intersection-union test: the effect only counts if it exceeds EACH placebo.
2. The p-values used in the Holm/BH correction are now one-sided for EXCESS (2026/T2 greater than the placebo, in the direction of the
   allegation). A negative difference is not evidence of anything. The two-sided p remains reported.
3. Each test reports two vote ceilings: against the most demanding placebo and against the loosest one (worst case).
4. Operational verdict rule (fixed before H5-H8): "SUSTAINED" = p_holm < 0,05 AND worst-case ceiling >= 1% of the margin;
   "detectable, irrelevant magnitude" = p_holm < 0,05 and ceiling < 1%; "REFUTED" = p_holm >= 0,05 and ceiling < 1%;
   "INCONCLUSIVE" = p_holm >= 0,05 and ceiling >= 1%.
5. H3: the bound "votes after 5 p.m. = maximum rate x delay" was discarded for being absurdly loose; BWeb has no vote
   log, so the number of votes after the nominal time is not measurable from this source.
6. A reading correction of mine, from the previous round: the 2026/T2 BUs reached the TSE after 7 p.m. in 99,6% of cases,
   but 98,2% of sections closed within 15 minutes of the nominal time. The receipt time reflects the TSE holding back the
   intake, not the closing of the section. The "BU time" proxy used before does not measure closing.

---

# Addendum 3: later analyses and corrections (written after seeing the results of H1 to H10 and of the historical ruler)

Everything below was decided after seeing results and must be read as exploratory, not pre-registered.

1. Red team added after the first results: voting machine model (H1 S0), T1 composition with all candidates and blank/null votes
   (H1 S1 per candidate), turnout as outcome (H1), interaction and size controls (H6), standardization by venue type and
   size (H5), rate by size in all years (H5), numerator against denominator (H5). None enters the registry of 23 tests.
2. Reading by three-year sets in the historical ruler (2018+2022+2026 homogeneous in 9 of 12 metrics; sets with 2014 in 5 of 12): later analysis.
   `M5b_OPO` and `M8b_OPO` repeat `M5b_PT` and `M8b_PT` by construction; without the repetitions there are 10 independent metrics.
3. Errors of mine corrected along the way: (a) the reading of "BU time" as a closing proxy (Addendum 2, item 6); (b) the claim
   that the report's closing table could not be checked: it reproduces exactly (339.593) with the voting machine's raw clock;
   (c) the official 2018/T1 totals quoted from memory were swapped: the TSE reported Haddad 31.342.005 and Bolsonaro 49.276.990,
   equal to BWeb; the one with 66 extra votes in one section (MA/8591/zone 17/section 25) is `votacao_secao`.
4. Result contrary to my registered expectation (C): none of the patterns A, B or C fit under the fixed criterion.
5. Test with printed poll-receipts: not executed (no input).

---

# Addendum 4: Phase 2 (A1 to A10), written on 2026-10-28 BEFORE running any new analysis

What had already been seen before this registration, for transparency: (a) the Phase 1 results; (b) the structure of the voting machine files of ONE
section in Roraima (2026 runoff): the BU header, the shape of the log and the existence of "Voto confirmado para [Presidente]" (Vote confirmed for [President]) events with a timestamp.
No result of the analyses below had been computed.

Verdict criterion: the same as Addendum 2, item 4 (SUSTAINED / detectable excess, irrelevant magnitude / REFUTED / INCONCLUSIVE),
with excess p-values corrected by Holm and BH over the complete Phase 2 family (the new test lines enter the Phase 1 registry).
Fixed placebos: 2014/T2, 2018/T2, 2022/T2 and 2026/T1 (and, for voting machine data, 2022/T2). Every analysis is symmetric (PT and opponent).
A test that cannot be run: explicit ERROR and a line in "NOT EXECUTED" with the missing input.

## Predictions

| A | If there is manipulation, I expect | If there is none, I expect | Numeric criterion fixed now |
|---|---|---|---|
| A1 counting curve | the real curve leaves the envelope of permutations within UF (state), keeping the sequence of UFs, or has discontinuous jumps | real curve inside envelope B (permutation within UF) at all points with >= 1% of sections; identical final sum | maximum deviation (p.p. of share) between the real curve and the median of B; "excess" only if it exceeds that of the four placebos AND leaves the simultaneous 95% envelope for >= 20 consecutive points; effect on the final sum is 0 by construction |
| A2 T1->T2 transitions | excess of sections in which the opponent loses absolute votes with stable turnout, and a different shape of the swing distribution | frequency and shape within the range of the placebo years | KS (and AD) distance of the 2026 residual swing against each placebo; "different" only if the SMALLEST distance to a placebo exceeds the LARGEST distance between pairs of placebos; frequency of opponent loss outside the [min, max] range of the placebos |
| A3 origin of the votes | net loss of the opponent in number of sections and of votes larger than in the placebos; coefficient "opponent T1 -> PT T2" outside the placebos | the accounting closes (identity: dPT + dOPO = dTurnout + ThirdParties_T1 - dBlankNull); frequency of net opponent loss within the placebo range | frequency (weighted by votes) and ecological coefficient with 95% CI against [min, max] of the placebos |
| A4 voting machine chain | divergence between digital BU, RDV, BWeb or signature | 0 divergences in the whole sample | a divergence of ONE vote is reported; sample: entire small UFs + stratified in the large ones + all sections >= 7 p.m. of the downloaded UFs |
| A5 logs | votes recorded after the nominal time in number or pattern incompatible with turnout; impossible events | confirmed votes in the log = BU turnout in >= 99,9% of sections; votes after the nominal time concentrated in the sections that closed late; intervals between votes >= physical minimum | (i) log x BU; (ii) votes after 5 p.m. nominal per section and total; (iii) association between late votes and Lula% (within venue) against 2022; (iv) shortest interval between votes |
| A6 contingency | sections with a replaced voting machine vote differently from their neighbors in the same venue | equal, within error | coefficient of the replacement indicator with venue FE, against 2022 if data exists |
| A7 polls | n/a (context) | n/a | only with registration number and source; otherwise NOT EXECUTED. No verdict |
| A8 coherence between offices | sections in which the total of some office differs from turnout | 0 sections outside the office's rule, same as 2018 and 2022 | rule per office estimated in the placebos (modal); any deviation listed |
| A9 turnout profile | turnout > 100% of registered voters in some band; atypical jumps in optional-voting bands | no cell > 100%; T1->T2 variations per band similar to 2022 | count of cells > 100%; correlation of per-band variations 2026 x 2022; cells outside [Q1-3 IQR, Q3+3 IQR] of the placebos |
| A10 model and software | excess of outliers, >=95% or digit deviation concentrated in one model or version | rates per model and version within the placebo interval; overseas and special venues explain the extremes | Poisson per model and version against the overall rate, Holm |

Non-statistical sections (blind-spot matrix, legal basis, literature, analysis of the original report) use only cited sources;
any claim without a verifiable source is removed and listed.

---

# Addendum 5: A11, A12 and A13 (written on 2026-10-29 BEFORE running any of the three)

Already seen before this registration: the results of A1 to A10 and, in A1, the arrival order by UF. Nothing of A11, A12 or A13 had been computed.
Verdict criterion: that of Addendum 2, item 4. Placebos: 2018 and 2022 (and 2014 where per-candidate data exists). PT and opponent symmetry.

## A11. Transfer of votes from the candidates defeated in the 1st round
- Context to cite with source: endorsements by Zema, Caiado, Cury and Clariana for Flávio; by Hertz Dias, Edmilson Costa and Samara Martins for Lula (critical); null by Rui Costa Pimenta; release (no endorsement) by Renan Santos. Each one's votes confirmed in BWeb.
- National accounting: third parties + drop in blank and null votes + drop in abstention = Lula's gain + Flávio's gain, term by term.
- Per section: Lula's and Flávio's gain (T2 minus T1, per registered voter) against each bloc's share in T1 (Zema+Caiado+Cury+Clariana; left; Renan Santos; PCO; blank and null; abstention), with municipality fixed effect. Transfer rates by ecological regression (Goodman), declaring the ecological fallacy; the 2022 and 2018 pattern computed with the same specification, with each year's third parties as same-sized blocs (without inferring endorsements without a source).
- Without manipulation: Flávio's gain grows with the share of the bloc that endorsed him; stable rates across UFs; pattern similar to the placebo years.
- With manipulation: Lula's gain grows with the share of the pro-Flávio bloc, concentrated in some UFs or section types, and different from the placebos.
- Numeric criterion: coefficient "pro-Flávio bloc to Lula" outside [min, max] of the analogous placebo coefficients (each year's largest third-party bloc to Lula) AND heterogeneity across UFs larger than that of the placebos (standard deviation of per-UF coefficients).

## A12. Sections with zero votes for a candidate
- Count sections with zero votes for Flávio and for Lula in 2026 T1 and T2; the same for the opponents of 2022, 2018 and 2014. Check whether the number 109 reproduces (the origin of the 109 was not provided: I report all reasonable definitions, with and without a minimum turnout).
- Per section: UF, municipality, venue (name and type), registered voters, turnout, result in T1/2026, result in the same section in 2022 and 2018, manual voter release rate, closing and voting machine model.
- P(zero) = (1 - p)^n with p estimated in two ways: (i) the section's own vote in T1; (ii) neighboring sections of the same venue (leave-one-out), with smoothing. Expected number = sum of P(zero); comparison with the observed by ratio and by an approximate Poisson-binomial test.
- Without manipulation: small sections in homogeneous venues (villages, communities), with zero or near zero also in previous years; observed close to expected.
- With manipulation: large or urban sections, which had opponent votes in 2022 and in T1/2026, and observed far above expected.
- Ceiling in votes: sum of the valid votes of those sections, against the margin.

## A13. Allegation of the "Prof. Marcelo Trindade" video about the counting curve
- The video and the data of the "472 voting machines" were not provided to this session; the allegation is treated as it was summarized to the author of this audit. Without the authors' data and code: **NOT REPRODUCIBLE** for the specific part.
- Source of the series: tabulation order by section (TSE's first partial tabulation); snapshots of the Resultados website are not public (to be verified).
- Count of lead reversals in the real order, in 1.000 random orders and in 1.000 realistic geographic orders (shuffle within the UF keeping the sequence of UFs). Linear stretches by windowed regression (high R2) in the real curve and in the simulated ones, attributed to the UFs that arrived in the interval. "Video method": interpretation declared here, before running: sum only the positive increments of the margin curve (splice the rising stretches) and compare with the same procedure on clean simulated series.
- Final total independent of the order and equal to the sum of the BUs.
- Without manipulation: the single reversal and the linear stretches appear in the realistic geographic orders and are explained by the arriving region; the rise-splicing method produces a false "victory" also in clean series.
- Numeric criterion: real reversals and linearity within the 95% interval of the simulated geographic orders.

## A13 (supplement). Historical lead reversals
- Count lead reversals in the reconstructed tabulation order (first partial tabulation per section) in the runoffs of 2018, 2022 and 2026 (and 2026 T1). 2014: no tabulation time in the 2014 product, **NOT EXECUTED**; 2002 to 2010: no per-section data with time in the open catalog, **NOT EXECUTED**.
- The lead is considered measured from 1% of tabulated sections (before that the sample is too small). Report how many elections had a single reversal.
- Prediction without manipulation: the observed number of reversals falls within the interval of the simulated geographic orders in each year; a single reversal occurs when the final margin is small and the last-arriving region favors the winner.

## A14. Receipt x tabulation x publication on Oct 25, 2026
- Allegation: "70% of the voting machines counted by 7:34 p.m., released gradually"; the screenshot suggests 7,28%. The original video was not provided to this session; the displayed percentage cannot be checked.
- Per-minute curves: % of BUs received (`DT_RECEBIMENTO_BU_HOR_TSE`) and % with first tabulation (`DT_PRIM_TOT_PARCIAL_HOR_TSE`), 2026/T2, 2022/T2 and 2026/T1. The publication curve requires snapshots of the Resultados website or public records with timestamps; if there is no source, **NOT EXECUTED** for that curve and for the tabulated-to-published delay.
- Without damming: tabulation tracks receipt with a short and stable delay (median of a few minutes); no accumulation of received but not tabulated sections. With damming: a large share received long before being tabulated.
- Document the official explanation of the pause with a source (press, if the official one is not accessible).

## A15. Voting machine model in 2022 (allegation of the PL report / Cerimedo)
- Replicate: UE2009 and UE2010 against UE2020 in 2022, and the 2026 models, within the same venue, in two specifications: (a) cross-sectional, without T1 control (what the allegation presupposes); (b) with the section's T1 vote as control. Effect in votes and in % of the margin per year, with a 95% normal interval.
- Without manipulation: effect of (a) explained by composition (old models in sections with a different profile) and effect of (b) null; in 2026, no difference by model.

## A16. Allegation inventory
- Dedicated page with: allegation, who made it, date, link, testable?, test used, result, verdict. Allegation without testable content: NOT TESTABLE, with what would make it testable. Neutral language, in the author's terms, no adjectives about the person. Only allegations whose content was provided or has a source are included; the rest remain as "content not verified".

## A17. Open questions
- Included: every INCONCLUSIVE, "detectable excess" or "EXCESS DETECTED" result, and every residual without an identified cause. For each: description, direction, central estimate in votes, 95% interval (normal approximation over the contrast's standard error; not bootstrap), worst-case ceiling, % of the margin, mundane explanations tested and not tested, and what would resolve it. Aggregated sum with interval (independence approximation, declared). Forbidden to assign "probability of fraud" or labels such as "likely"; probabilities only about measured quantities.

---

# Addendum 6: POST-REGISTRATION (Phase 2.1), design flaws of A1, A2, A3 and A12 and corrected tests

Written on 2026-10-29, **after** seeing the original results and **before** running the corrected versions. Numbering: the Phase 2.1 briefing asked for an "Addendum 4 post-registration"; since Addendum 4 was already the Phase 2 pre-registration, this is Addendum 6. **Nothing of the original results is altered or deleted**: the four lines remain in the registry with the verdict that the pre-registered criterion produced. The corrected versions are published alongside, with their own verdict, and are labeled "post-registration".

## A1. Counting curve
- **Design flaw.** The null "permutation within the UF, keeping the sequence of UFs" assumes that the arrival order of sections within each UF is random. It is not: municipalities and zones arrive in blocks. That is why the criterion "leave the envelope for 20 consecutive points" is satisfied by **any** election, and the comparison of the maximum deviation with that of the placebos is dominated by the first 1 to 5% of sections, where the sample is small and the 2026 publication pause altered the composition of the beginning of the queue.
- **Demonstration (to run):** (i) the original test flags envelope exit in 4 of 4 elections (2018, 2022, 2026 T1 and T2); (ii) in **simulated series without manipulation** (same UF sequence, municipalities in random and contiguous order within the UF, sections shuffled within the municipality), the fraction flagged by the original criterion is measured.
- **Corrected test.** Null D: keeps the arrival sequence of UFs, shuffles the order of the **municipalities** within each UF (contiguous blocks) and the sections within the municipality. Statistic: maximum deviation of the real curve against the median of D from 10% of sections onward (cutoff fixed now). Comparison with the placebos by the same intersection-union test.

## A2. T1 to T2 transitions
- **Design flaw.** The "by role" placebo (opponent) assumes that the opponent behaves the same in all years. The frequency of absolute vote loss depends on who led the 1st round and on how many third-party votes there are to distribute (2014 and 2018: ~26 million; 2022 and 2026: 9 to 10 million).
- **Demonstration (to run):** the original test applied to the **PT of 2022** (which led the 1st round) also flags excess against the other years.
- **Corrected test.** Compares the **1st-round leader** of each year, with direct standardization by the ratio (third-party votes) / (leader's votes) in the section, with the 2026 weights. Placebos: the leaders of 2014, 2018 and 2022.

## A3. Origin of Lula's new votes
- **Design flaw.** Ecological coefficients "opponent in T1 to PT in T2" are negative in all years and reflect geography; the comparison "2026 against the largest placebo coefficient" flags excess in the year with the largest coefficient in **any** set of four years (an ordering artifact), and the derived vote ceiling has no causal meaning.
- **Demonstration (to run):** the original test applied to each of the four years against the others (flags exactly one: the one with the largest coefficient).
- **Corrected test.** Opponent-to-PT transition rate estimated with a 0 to 1 constraint (bounded least squares, weighted by registered voters), interval by municipality bootstrap (200 replicates); same estimation in the placebos; ceiling = upper limit of the 95% CI of the rate x opponent votes in T1 x 2.

## A12. Sections with zero votes
- **Design flaw.** The observed/expected ratio with p estimated from the 1st round is biased in years with relevant third parties (2018, 2014: ratios of 0,27 to 0,72), and comparing the 2026 ratio with those ratios "flags excess" even without a difference.
- **Demonstration (to run):** in 200 simulations **without manipulation** of 2026 (opponent votes binomial with p equal to the venue's in the runoff itself), the ratio by the 1st-round estimator and the fraction of simulations flagged by the original test.
- **Corrected test.** p estimated from the neighboring sections of the same venue in the runoff itself (leave-one-out), same estimate in the placebos, comparison by ratio and by a direct z of 2026.

Verdict of the corrected versions: rule of Addendum 2, item 4, with Holm over the four corrected lines.

## Addendum 7: A18 (mid-process alteration) and A19 (typed vote x recorded vote), written before running A18

Registered on 29/10/2026, before any execution of A18. The sources for the delays are in [A18](a18-alteracao-no-meio.md).

### A18a. Congestion window in the 2026 1st round
- **Fixed window (by the clock, from the public statement):** BUs with `DT_RECEBIMENTO_BU_HOR_TSE` between 19:00:00 and 19:59:59 on election day (the press reports the national total stalled at 64% around 7 p.m. and resumed around 8 p.m.).
- **Test:** coefficient of the window on Lula's share (and, symmetrically, the opponent's) of the section's valid votes, with **polling-place fixed effect**, controlling turnout, log of registered voters and minutes of closing delay. Placebos: the same clock window in 2022/T1 and 2018/T1.
- **Prediction without alteration:** the 2026/T1 coefficient falls within the placebos; the within-venue difference attributable only to composition (the window selects sections by transmission pace). Excess only if it exceeds **each** placebo (intersection-union), with Holm over the complete family.
- **Robustness (descriptive, outside the family):** same estimate with the window defined by the receipt→tabulation lag above the day's 90th percentile; count of sections with nominal + blank + null votes different from turnout, inside and outside the window (prediction: zero in both groups).

### A18b. Receipt order after 7 p.m. in the 2026 runoff
- **Variable:** t = hours since 19:00 of BU receipt (only sections received after 19:00).
- **Test:** coefficient of t on Lula's share (and the opponent's) in the runoff, with venue fixed effect, controlling the 1st-round share, turnout and closing delay. Placebos: the same t in 2022/T2, 2018/T2 and 2026/T1. Exposure convention: effect of a 1-hour difference in receipt on the valid votes of the sections received after 19:00 (declared as a convention).
- **Descriptive:** share of the variance of receipt time explained by UF and by municipality in 2026/T2 against the placebos.
- **Prediction without alteration:** no difference beyond composition, that is, the 2026/T2 coefficient within the placebos.

### A19. Typed vote x recorded vote
No statistical test on voting machine data. The power tables (probability of detecting alteration in 0,1%, 0,5%, 1%, 2%, 5%, 9% of the machines) are a closed-form calculation and do not enter the test registry. The integrity-test numbers by UF are only published when there is a source; anything not located remains NOT EXECUTED.

## Addendum 8: Phase 3 (A20 to A28, adversarial hypotheses), written on 29/10/2026 before running any test of the phase

Neutral language: each test describes the **class of failure** it covers and the **expected trace** in the public data, not how to produce the failure. The verdict rule of Addendum 2 applies. Unit of every ceiling: margin votes. Shape tests have no vote ceiling. Tests that depend on input we do not have are registered as **NOT EXECUTED**, with the input and instructions on how to provide it.

| test | failure class covered | expected trace in the data | prediction without manipulation | planned status |
|---|---|---|---|---|
| A20 Registry | inflated registered electorate (voter IDs added with no corresponding voter) | registered-voters/population 16+ ratio above 1 in municipalities, excess among the oldest (80+, 90+, 100+) | fraction of municipalities with ratio > 1 and ratio in the 80+, 90+ and 100+ bands in 2026 within the interval of 2018 and 2022 (after removing the national level difference) | execute (IBGE 2022 Census; electorate profile by zone) |
| A20b profile of new sections | sections created to receive votes | age and sex profile of a new section different from that of the old sections of the same venue | equal | NOT EXECUTED: the public profile is by zone, not by section |
| A21 Temporal forensics of logs | votes recorded outside the pace of the real voting | shorter intervals between votes, bursts, concentration in the last hour; association with the vote | identical patterns in 2022 and 2026, with no association with the vote (venue FE, T1 control) | execute only with the measures already extracted from the logs (short intervals, first and last vote, votes after the nominal time); full distribution and year of birth NOT EXECUTED |
| A22 Coherence between offices | uniform deviation restricted to the office of president (invisible to outlier tests) | systematic displacement of the president x non-presidential offices residual | 2026 residual equal to 2022 and 2018 | NOT EXECUTED in this round: the coalition map by state is missing (gubernatorial candidate aligned with each presidential candidate). Design fixed below |
| A23 Observation | different behavior where a party observer is or is not present | sections with an observer differ from those without after controls | no difference | NOT EXECUTED: no list of sections with an observer |
| A24 Natural experiment of the integrity test | a voting machine that behaves differently when it is not the test | sections that voted on a spare machine because of the test differ from their neighbors in the same venue | no difference | NOT EXECUTED: the list of affected sections is not public |
| A25 Replaced voting machines | machine replacement as an intervention point | vote before and after the replacement; sections with a replacement differ from their neighbors | no difference | sections with replacement x neighbors already in A6; vote before x after from the logs NOT EXECUTED (log of the original machine not published) |
| A26 Publication integrity | published file altered afterwards | current file hash different from the hash of the first download; later modification date | all files identical to the first download | execute: official hash published today x hash of the first download; current size and date; Wayback Machine captures |
| A27 Fabricated sections | sections without real voters | venue address with no structure, atypical profile, venue history | new sections with turnout >= 95% explained by venue type and size | execute with what we already have (venue type, size, 1st round); origin of transfers NOT EXECUTED |
| A28 LAI requests (access-to-information law requests) | data that only the government has | responses or refusals | n/a | draft and save in `lai/`; filing and deadline remain NOT EXECUTED until the author files them |

**A22, fixed design (for when the input exists).** In the states with a gubernatorial runoff, per section: the presidential candidate's share in the runoff against the aligned gubernatorial candidate's share in the same round, with UF fixed effect and 1st-round control; statistic: mean displacement of the residual in 2026; placebos: 2022 and 2018 in the same states with a runoff. Prediction without manipulation: the 2026 displacement within the interval of the placebos. This is the test for uniform deviation restricted to the president.

**Criterion for A20.** Statistic: (i) fraction of municipalities with registered voters > population 16+ (and by band); (ii) national registered-voters/population ratio by band. The population is that of the 2022 Census (IBGE, SIDRA 9514) in all years; therefore 2018 and 2026 use an outdated denominator and the comparison is made **after dividing each municipal ratio by the national ratio of the same year**. Shape test, no vote ceiling; excess if the 2026 fraction exceeds that of each comparison year by more than 2 binomial standard errors.

---

## Addendum 9: Phase 3.1 (A20b-elderly, A22, A24, A28), written on 29/10/2026 before running any test of this phase

What had already been seen before this registration, for transparency: (a) the results of A20 from Addendum 8 (registered voters 80+ and 90+, ratios by band, turnout by band); (b) only the **header and columns** of the new files (electorate profile by section, coalition tables) and the existence of the BWebs of 2018, 2022 and 2026. No result of the tests below had been computed. The verdict criterion of Addendum 2, item 4, applies, and the unit "margin votes" (in favor of one candidate, one added vote changes the margin by 1; a switched vote changes it by 2). A shape test has no vote ceiling. Every ceiling is a "worst-case ceiling, not an estimate".

**Name.** The request uses the label A20b for the elderly registry. The line "A20b profile of new sections" of Addendum 8 remains as is (NOT EXECUTED at the time). This addendum uses **A20b-elderly** so as not to collide with it.

### A20b-elderly. Elderly registry

**Input sources (all public).** Population of the 2022 Census (IBGE, SIDRA 9514, already in `results/fase3/ibge_pop_9514_2022.csv`); turnout and abstention profile by municipality, zone and age band (TSE; 2018 and 2022 with both rounds, 2026 only with the 1st round published up to 29/10/2026, last modified 21/10/2026); electorate profile by section (TSE, `perfil_eleitor_secao_{2018,2022,2026}`, with registered voters and registered biometrics by age band; 2026 generated on 14/07/2026, 2022 on 26/08/2022).

**1. Legal rule (citation, not a test).** The cancellation for absence from three consecutive elections is in the Electoral Code, art. 7, § 3 (cancellation of the registration of whoever does not vote in three consecutive elections, does not pay the fine or does not justify) and in art. 71, V; TSE Resolution 23.659/2021, art. 130, counts each round as an election (§ 1) and exempts those whose vote is optional (§ 2): people over 70, illiterate voters and voters aged 16 and 17. Cancellation by death is art. 71, IV, with the monthly notification by the Civil Registry offices (art. 71, § 3). Consequence for the test: under optional voting, absence does not cancel the voter ID, so **registered voters 90+ and 100+ above the Census do not indicate votes**; only actual voters do. Declared verification pending: the full text of Resolution 23.659 is on a site that blocks automated access (403); the cited paragraphs come from a search summary and need to be checked against the official link; the article of the Resolution dealing with death was not confirmed.

**2. Voters 90+ and 100+ against the Census.** Per municipality and per available year/round (2018 T1, T2; 2022 T1, T2; 2026 T1; **2026 T2: NOT EXECUTED, profile not published**). Statistics: (i) number and fraction of municipalities with voters > band population (minimum band population: 10 for 90+, 5 for 100+; below that, the municipality enters only the complete list, not the fraction); (ii) national voters/population ratio; (iii) list of municipalities with voters > population, with both values. To compare years, each municipal ratio is divided by the national ratio of the same year (same treatment as A20, because the Census is from 2022). Prediction without manipulation: national ratio of voters 100+ below 1, and fraction of municipalities with voters > population in 2026 not exceeding that of 2022 and 2018 by more than 2 binomial standard errors. Worst-case ceiling (not an estimate): sum, over the municipalities in the list, of (voters − band population), all attributed to one candidate, in margin votes (factor 1); reported for 2026 T1 and, as reference, for 2022 T1 and 2018 T1. Voters above the Census in 2022 and 2018 show how much of this is a method difference between registry and Census.

**3. Biometrics by age band.** The turnout profile **does not include** biometrics; the electorate profile by section includes **registered biometrics**, which is not the same as "manual voter release" on the day (the latter comes from the BU, per section, not per age). Fixed: (3a) fraction of registered voters with registered biometrics by band (90+, 100+, 16 to 89) and year; (3b) per section and round, regression of the BU manual release rate (`manual_rate`) on the section's fractions of registered voters 90+ and 100+, with the section's fraction of registered voters **without registered biometrics** as a control and polling-place fixed effect; estimated in 2026 T2 and in the placebos 2026 T1, 2022 T2 and 2018 T2. Prediction without manipulation: the coefficient of 90+ and 100+ in 2026 T2 does not exceed that of any placebo (intersection-union test, one-sided excess p, Holm). No vote ceiling (shape test). Manual voter release by **individual** age band is not observable with public data; (3b) is an ecological proxy per section and may not reflect behavior by age.

**4. Sections with a high fraction of registered voters 80+.** Fraction of registered voters 80+ of the section from the same year's per-section profile. Outcomes (runoff): Lula's and Flávio's share of valid votes, and turnout. Estimator: polling-place fixed effect; controls: the same outcome in the section's 1st round (and, for the share, turnout); standard error clustered by venue; coefficient per unit of the 80+ fraction. Placebos: 2022 T2 and 2018 T2 (same design with the year's per-section profile), and 2026 T1 only for turnout. Additional description, without a test: the top decile of the 80+ fraction against the rest, within the UF. Prediction without manipulation: 2026 T2 coefficients within the placebos (do not exceed them). Conversion: share, expo = Σ (valid votes × 80+ fraction) per section, factor 2; turnout, expo = Σ (registered voters × 80+ fraction), factor 1 (every extra vote for the same candidate). The tests enter the A20b-elderly registry (own family `_reg_a20b`, Holm within it), without changing the main family.

### A22. Coherence between offices (execute)

**Input.** TSE coalition tables (`consulta_coligacao_{2018,2022,2026}`), with the composition (party abbreviations; federations expanded to the parties that form them), and the runoff BWebs of 2018, 2022 and 2026 (votes per candidate and section for president and governor).

**Alignment rule (fixed now).** For each year, P_A and P_B are the sets of parties of the presidential coalitions of the two runoff candidates (Lula or Haddad, and the opponent); Q is the set of parties of the coalition of the 1st-round gubernatorial candidate (or the party, if it ran alone). Alignment to A = |Q ∩ P_A| / |Q|; aligned to A if > 0,5 and to B < 0,5; symmetric for B; the rest (including no coalition with a presidential party) are left out and listed. **Only UFs with a gubernatorial runoff in which the two finalists are aligned with different presidential candidates enter.**

**Statistic.** Per section, d = share of the PT candidate (Lula 2026 and 2022, Haddad 2018) of valid votes for president minus the share of the governor aligned with him of valid votes for governor (runoff). S = mean of d weighted by valid votes, in the year's eligible UFs; standard error clustered by municipality. Positive S = PT president ahead of the aligned governor. **Placebos:** 2022 and 2018, in the year's eligible UFs (if there are 3 or more UFs in common with 2026, the 2026 estimate is recomputed on the common UFs and is the main one; otherwise, each year uses its own UFs). Version with 1st-round control (secondary, outside the family): d regressed on the 1st round's `lula_sh` with UF fixed effect, and adjusted S = mean, weighted by UF valid votes, of the fixed effects evaluated at 1st-round `lula_sh` = 0,5. Symmetric: the opponent's side is −S by construction (two candidates). Conversion: expo = Σ valid votes of 2026 in the eligible UFs, factor 2. **Prediction without manipulation:** S of 2026 within the [min, max] interval of S in 2022 and 2018 (intersection-union test, excess p, Holm). **Declared limit:** the test only covers the UFs with a gubernatorial runoff with finalists of opposite alignments; the ceiling applies **only** to those votes, not to the country.

### A24. Natural experiment of the integrity test (execute with the available UFs)

**Input.** List of sections whose voting machines were drawn for the integrity test (and the authenticity test, in a separate column), built **from the TREs' publications**, one source per UF (URL and access date), in `data/a24_secoes_teste_integridade.csv` (UF, municipality, zone, section, round, test type, with/without biometrics, source). Inclusion rule: a section only enters if its UF, municipality, zone and section are **written in the publication**; a news summary without the list does not enter. The TRE sites respond 403 to automated access; the project does **not** disguise the agent to bypass the block. If a UF's list cannot be read without that, the UF is registered as NOT OBTAINED, with the reason, and the file accepts manual filling with the source.

**Test (fixed).** For each listed section and round, compare with the other sections of the same polling place not in the list: Lula's share (valid votes), turnout and manual voter release rate, with the same 1st-round outcome as control and venue fixed effect. Placebos: the same sections in the 2026 1st round and in the 2022 runoff (the section exists in both years). Prediction without manipulation: difference equal to that of the placebos. Conversion: expo = national valid votes of 2026 T2 (worst-case ceiling, extrapolation without random sampling, only as an upper bound). Power: the number of sections is small (≈ 20 to 30 per UF and round); with a deviation of 1,67 p.p. per section, the test only sees mean differences above about 1 p.p. with 100 sections; the smallest detectable effect will be reported. If fewer than 10 sections are obtained, the test remains NOT EXECUTED (insufficient power) and the survey result is published in `docs/fase3.md`.

### A28. LAI requests (leave ready, do not file)

The six texts remain in `lai/`. This phase's deliverable: `lai/canais.csv` with, for each request, the **agency**, the **channel** (name, URL), the channel's normative basis and the channel verification status; and the decision of **who receives each request** (TSE, and the TREs only when only the TRE has the data). Channels that cannot be verified because the site blocks automated access are marked "to be confirmed at filing". The project does not file; the registry (`registro.csv`) remains NOT FILED until the author files them.

### Addendum 9a: design correction of A20b-elderly, written on 29/10/2026 after Addendum 9 and BEFORE running any test

**My error in Addendum 9, item 2.** Comparing voters 90+ and 100+ of 2018 and 2026 with the 90+ and 100+ population of the **2022** Census mixes cohorts: whoever is 90+ in 2026 was 86+ in 2022 (a cohort larger than the Census's for 90+), and whoever is 90+ in 2018 was 94+ in 2022 (a smaller cohort, only survivors). Normalization by the year's national ratio (Addendum 8, A20) corrects the level, not the per-municipality shape. Therefore:

1. Item 2 remains as registered (voters/Census ratio, fraction of municipalities with voters > population, list, ceiling), but **only 2022 compares the same cohort**; 2018 and 2026 are reported with the cohort-mismatch warning and **the formal verdict of item 2 is not used as a conclusion**: test 2a below applies.
2. **2a. Cohort monotonicity (no Census).** A person does not get younger: the 2026 registry at 95+ can only come from the 2022 registry at 91+ (4 years earlier), hence it is contained in the 2022 registry at 90+; and 100+ in 2026 comes from 96+ in 2022, contained in 95+ in 2022. Statistic, per municipality (and national), with T1 of each year: R(95+) = registered voters 95+ in 2026 / registered voters 90+ in 2022; R(100+) = registered voters 100+ in 2026 / registered voters 95+ in 2022; and the versions with **voters** in the numerator. Placebo: the same pair 4 years earlier (2022 against 2018): registered voters 95+ in 2022 / registered voters 90+ in 2018, etc. Prediction without manipulation: national R of 2026 not exceeding that of 2022 by more than 2 standard errors (municipality bootstrap, 1.000 resamples, seed 20261029), and fraction of municipalities with R > 1 (denominator ≥ 10) of 2026 not exceeding that of 2022 by more than 2 binomial standard errors. Migration between municipalities can generate local R > 1 in any year; that is why the test is comparative. Worst-case ceiling (not an estimate): Σ over municipalities with R > 1 of (2026 voters in the numerator − 2022 registered voters in the denominator), all attributed to one candidate, in margin votes (factor 1), with the same calculation of 2022 against 2018 alongside.
3. Items 3 and 4 of Addendum 9 do not change.

### Addendum 9b: declared deviation in A22, written on 29/10/2026 after running ONLY the 2026 alignment and BEFORE computing any governor vote

**What I saw.** When running the alignment rule of Addendum 9, **no 2026 UF was eligible**: in the six UFs with a gubernatorial runoff (AC, AM, DF, ES, RN, TO) no pair of finalists was aligned with different presidential candidates. Cause seen in the composition, without looking at votes: the PT's opponent ran for president under a single party (a one-party coalition, PL), so a governor's coalition rarely has more than 50% of parties in common with it; in AM the PT candidate's coalition has exactly 50% (the rule requires more than 50%). Under the registered rule, **A22 in 2026 is NOT EXECUTABLE**, and that is the official A22 line. No governor vote was read for this deviation.

**Variant 9b (exploratory, outside the main family).** Alternative rule fixed now: a finalist is aligned with presidential candidate X if **X's party** is in the composition of the finalist's coalition (or federation), and the other presidential candidate's party is not; the UF enters if one finalist is aligned with the PT and the other with the opponent. Statistic, placebos (2022 and 2018, same rule), clustered standard error, conversion into votes and verdict rule: those of Addendum 9. Two UFs are expected in 2026 (AM and DF, by the composition), which gives very low power; the ceiling will be large for that reason, and the likely verdict is INCONCLUSIVE. The 9b result is published as **exploratory** and does not replace the official NOT EXECUTABLE line.

### Addendum 9c: clarification of A24, written on 29/10/2026 before any section list was read

A test of the code with a **synthetic** list of 80 randomly drawn sections (discarded; not project data) showed that comparing an estimate **with 1st-round control** (2026/T2) against a placebo **without** control (2026/T1) fabricates a false excess. The design is now: the comparator of the intersection-union test is only **2022/T2 with the same 1st-round control**; the 2026 1st-round difference, without control, is reported as **pre-treatment balance** and does not enter the verdict. This corrects Addendum 9 ("placebos: 2026/T1 and 2022/T2") in A24. No real A24 data exists so far (no list read).

### Addendum 9d: clarification of A20b-elderly, written on 29/10/2026 AFTER seeing the results of the first run

The results of the first run (`A20b_testes.csv`) **remain as they came out**; what follows is added alongside.

1. **Comparator without control in A20b-4, turnout.** Addendum 9 included 2026/T1 as a placebo for turnout. That comparator has no 1st-round control (there is no 1st round before the 1st round) and is a different specification from the main estimate (2026/T2 with `turnout_t1`). Its coefficient is -0,69, against +0,04 of the main estimate and ~0 of the controlled placebos; it becomes the "loosest placebo" and produces a ceiling of 4,07 million margin votes (91,9% of the margin) that comes from the specification difference, not from the data. It is the same defect corrected in A24 (Addendum 9c). **Supplementary line, published alongside, does not replace the original:** turnout with only the controlled placebos (2022/T2 and 2018/T2). The original line remains in the registry with its verdict.
2. **Implementation.** A20b-2a lines with no municipality with R > 1 had p = NaN (zero standard error); they become p = 1,0 (no excess by construction). It does not change the other lines.
3. **Reading of A20b-4 and 3b fixed now**, before writing the page: the share coefficients (Lula, Flávio) fall within the placebo interval and the worst-case ceiling comes from the dispersion between the comparison years, not from a measured effect; in 3b the coefficient grows in all years (0,35; 0,64; 0,71 and 0,80) and the excess label is formal, a trend one, with no conversion into votes.

### Addendum 9e: exploration requested on 29/10/2026 about the oldest voters, written AFTER seeing the A20b-elderly results and BEFORE running this exploration

**Exploratory, outside the pre-registered family.** Author's request: give a ceiling in margin votes and in % of the margin for the voters 95+ line (which has z and Holm), and measure how many voters of each age band voted in 2018, 2022 (the last general election of the government before 2026, as context, without judgment) and 2026. Fixed now: (i) table of registered voters, voters and turnout by band (60 to 69, 70 to 79, 80 to 89, 90 to 94, 95 to 99, 100+ and aggregates) per available year and round, and voters as % of the margin; (ii) ceiling of the voters 95+ test = (ratio difference between 2026 and 2022 + 1,645 standard error) x 2022 registered voters 90+ in the test's municipalities, **factor 1** (one extra voter, if all for a single candidate, changes the margin by 1); central estimate = ratio difference x denominator. Worst-case ceiling, not an estimate. Voters have neither age nor vote associated in the public data; the table does **not** say whom they voted for.

## Addendum 10: A31, extreme municipalities in the T1 -> T2 transfer (Silva Jardim/RJ allegation), written on 29/10/2026 BEFORE computing any test statistic

**Order declaration.** Before this addendum I only checked, without looking at results, that the per-section BWeb covers 2014, 2018, 2022 and 2026 (T1 and T2), that Silva Jardim/RJ is TSE municipality 59110 and that 2026 has 5.571 (UF, municipality) keys where the other years have 5.570 (the difference is investigated and recorded in the script, not chosen). No vote of Silva Jardim, no fraction f and no residual had been computed.

**Allegation.** In Silva Jardim, in the 2026 runoff against the 1st round, "Flávio +1, Lula +964, -104 voters" would be impossible without manipulation. This test (i) checks whether the numbers reproduce, (ii) places the municipality in the distribution of all municipalities in four elections and (iii) uses a null model that respects heterogeneity between municipalities, instead of independent coins.

**Definitions (per municipality, sum of the BWeb sections, overseas excluded).** PT = PT candidate (Lula in 2026, 2022; Haddad in 2018; Dilma in 2014), OPO = opposite finalist (Flávio, Bolsonaro, Bolsonaro, Aécio). dL = PT(T2) - PT(T1); dF = OPO(T2) - OPO(T1). ThirdParties(T1) = T1 nominal votes minus PT and OPO. BN = blank + null. dC = turnout(T2) - turnout(T1). **Stock** E = ThirdParties(T1) + BN(T1) + dC. **Pool** P = dL + dF, which by the Phase 2 identity (A3/A11) equals E - BN(T2); the identity is verified municipality by municipality and the script stops if it fails. **Fraction captured by the PT** f = dL / P, defined for P >= 20 (municipalities with P < 20 or P <= 0 are left out and counted). f may leave [0, 1] when a candidate loses votes between rounds; this is kept, not truncated.

**Part 1: checking the allegation (Silva Jardim).** Table with T1 and T2: registered voters, turnout, PT, OPO, each third party, blank, null, and the differences dL, dF, dC, d(registered voters), d(BN). Record whether "+1, +964, -104" reproduces and **what the -104 is** (dC, d(registered voters) or another quantity); if no quantity gives -104 that is stated.

**Part 2: distribution and position.** For 2026, 2022, 2018 and 2014: distribution of f (deciles, minimum, maximum, fraction outside [0, 1]) and the position (percentile and value) of Silva Jardim in each year.

**Part 3: null model (null hypothesis = typical behavior of municipalities with the same 1st-round profile).**
1. Weighted regression, per year, f_i = alfa_UF + sum(beta_j x profile_ji) + e_i, with UF fixed effect (27) and profile from the **1st round** only, as a fraction of T1 turnout: PT, OPO, blank and null, abstention (1 - turnout/registered voters) and the composition of third parties. Third-party composition: 2026, the A11 blocs (pro-Flávio = Zema, Caiado, Cury, Clariana; Renan Santos; others); 2022 and 2018, the largest third party, the second largest and the rest (without inferring endorsements, as in A11); 2014, only the third-party total (the 2014 T1 per-candidate file is not in the project). **The T1->T2 turnout change does not enter** the profile: it is a runoff outcome and, if there were an anomaly, it could be absorbed by it.
2. Variance: Var(f_i) = f_hat(1 - f_hat)/P_i + tau2, with f_hat clipped to [0,02; 0,98]. tau2 (real heterogeneity between municipalities, which the coin model does not have) is chosen by bisection so that the robust scale (1,4826 x MAD) of the standardized residual z_i = e_i / dp_i is 1. Weights 1/Var, 20 iterations.
3. Tail: **Student's t** with the degrees of freedom estimated by maximum likelihood over the z's of the **other three years** (each year is compared with the other three; scale 1 after calibration). Two-sided p, **Holm** correction for the number of eligible municipalities of the year and, in a separate line, for **5.570** comparisons (the figure in the request).
4. **Empirical precedent**: for each flagged municipality, how many municipalities of the other three years have |z| >= its own.
5. **Verdict for Silva Jardim in 2026 (fixed now):** WITHIN THE EXPECTED TAIL if Holm p >= 0,05; OUTSIDE THE MODEL TAIL, WITH PRECEDENT if Holm p < 0,05 and some other year has a municipality with |z| >= its own; OUTSIDE THE TAIL, WITHOUT PRECEDENT if Holm p < 0,05 and no other year has one. **Prediction without manipulation: WITHIN THE EXPECTED TAIL.** Label: "outside the tail" measures shape, not manipulation.
6. **Ceiling in margin votes (worst-case ceiling, not an estimate), factor 2** (one pool vote attributed to the PT that would be the OPO's changes the margin by 2): (a) per municipality, 2 x P x max(0, |f - f_hat| - zc x dp), with zc the Holm critical value of item 3, that is, only what goes beyond the expected tail; (b) unconditional, 2 x P x |f - f_hat|, everything the model does not explain, attributed to manipulation. Summed for Silva Jardim and for the 20 most extreme, in votes and in % of the margin (4.430.191).

**Part 4: demonstration of the independent-coins model.** Each voter in the pool goes to the PT with probability p0, independent of the others. Three p0 variants: 0,5; the municipality's own PT/(PT+OPO) ratio in T1; the national T1 ratio. Statistic: z_coin = (dL - p0 P)/sqrt(P p0 (1-p0)) in the national total of each year and municipality by municipality. Report the national z, the p and, per municipality, the fraction rejected with Holm at 0,05. **Prediction:** the coin model rejects the national result of **all** elections, 2022 included, and rejects a large fraction of municipalities in all years; this disqualifies it as a reference, because it rejects what no party contests as impossible. (This shows the criterion is inadequate; it neither validates nor invalidates the result of any election.) What the allegation implies under the coin model for Silva Jardim is also computed (probability of dF <= the observed given P), to show the order of magnitude that model would assign.

**Part 5: the 20 most extreme municipalities of 2026 (largest |z|, either direction, among the eligible).** For each: f, z, Holm p, P, f_hat; per-section decomposition: number of sections, share of the 3 sections with the largest dL in the total dL (C3_dL) against the share of the 3 sections with the largest pool in the total pool (C3_P), fraction of sections with f_s on the same side as the municipality; dominant third party of T1 (largest among non-PT/OPO), its share of turnout and **declared endorsement** (classification already documented in `docs/resultados-fase2.md`, A11, with sources; 2026 only); and the **same calculation in 2022**: the municipality's f and z in 2022 and whether it was among the 5% most extreme. Concentration rule fixed now: "concentrated gain" if C3_dL > 0,5 and C3_dL > 1,5 x C3_P; otherwise "spread".

**Part 6: Silva Jardim, check with printed poll-receipts.** `results/fase3/A31_silva_jardim_secoes.csv`: all sections, with registered voters, turnout, PT, OPO, each third party, blank and null of T1 and T2, in the columns of `scripts/04_cruza_bu_impresso.py`, plus empty columns for the printed value, for whoever collects the BU (local directories and party observers, via the `boletins-impressos` page). The project has no printed BU from Silva Jardim; this check remains NOT EXECUTED until someone provides BUs.

**Prediction without manipulation (joint).** Silva Jardim within the expected tail after the correction; gain spread across the sections; explained by the 1st-round profile (f_hat close to f). If that fails, the result comes out as it came out.

**What this test does not do.** It does not identify whom each voter voted for; it neither proves nor rules out manipulation in any municipality; the verdict applies to the shape of the distribution across municipalities. Each ceiling is a worst-case ceiling, not an estimate.

### Addendum 10a: municipality-year with a section counted in one round and not in the other, written on 29/10/2026 after the first execution stopped at the identity check and BEFORE any test statistic

**What I saw.** The P = E - BN(T2) check of Addendum 10 stopped in 2018, in 1 municipality (BA, TSE code 38490). Cause, seen in the raw data and without computing f: in the 2018 T1 two sections of that municipality have type "Anulada e apurada em separado" (annulled and counted separately), with recorded turnout (363 and 383) and zeroed votes; in T2 the same sections were counted. They put 746 votes into the municipality's pool that do not exist in T1, which breaks the identity and would inflate dL and P in that municipality. This applies to any section with a different counting status between rounds, even when the identity passes by chance (for example, zero turnout at both ends).

**Added rule (applies to the four years, fixed now).** A municipality-year is **left out** of the test if any section (paired by the key UF, municipality, zone, section) has a different voting machine type between T1 and T2, or exists in only one of the rounds. Sections "Não instalada" (not installed) in both rounds, with everything zero, do not distort and remain. The municipalities excluded by this rule are listed in `results/fase3/A31_excluidos.csv`, with the reason. The identity remains mandatory for all the others: if it fails, the script stops. The number of excluded municipalities goes into the page text.

### Addendum 10b: post-hoc supplementary analysis of A31, written on 29/10/2026 AFTER seeing the main model result and BEFORE running the supplementary one

**What the main model showed (remains as it came out).** Silva Jardim: z = 1,13, Holm p = 1, WITHIN THE EXPECTED TAIL. But the estimated tail is very heavy (Student's t with about 2,4 to 2,8 degrees of freedom in the four years), and the Bonferroni critical value for 5.570 comparisons falls at |z| of 83 to 135. Cause seen in the result: f = dL / (dL + dF) is unstable when the pool is small and the gross flows are large and of opposite signs (for example, dL = +1.114 and dF = -1.059 with a pool of 55), and the binomial variance presupposes f in [0, 1]. **The main test has almost no power to reject small municipalities.** This does not change the Silva Jardim verdict (a |z| of 1,13 is common under any reference), but it changes what can be said about the other 19 extreme ones, and is declared on the page.

**Supplementary S1 (exploratory, outside the verdict).** Well-conditioned statistic: yL = dL / registered voters(T1) and yF = dF / registered voters(T1), each regressed (least squares weighted by T1 registered voters) on the same 1st-round regressors and UF fixed effect of the main model. Residual standardized by the robust scale (1,4826 x MAD) within deciles of the year's T1 registered voters. Tail: Student's t with df estimated on the other three years, as in the main one. Report for Silva Jardim in the four years (zL, zF, p, Holm p) and, in 2026, the 10 largest |zL| and the 10 largest |zF|, with the ceiling in margin votes (factor 2) of the part beyond the Bonferroni critical value of 5.570 comparisons. Reading fixed now: Silva Jardim is said to be "common in the supplementary statistic" if both Holm p's are >= 0,05.

**Supplementary S2 (descriptive).** Number and % of municipalities with dF <= 1 (the opponent gained no more than 1 vote between rounds) in each year, among all eligible ones and among those with dL >= 500; and how many had dL >= 900 together with dF <= 1.

**Supplementary S3 (descriptive).** Column `fluxo_bruto_sobre_P` = (|dL| + |dF|) / |P| in the 20 most extreme of the main model, to show which extremes come from a small pool with large gross flows.

**Disclosure.** These lines are marked "post-hoc, exploratory" on the page and do not replace the main line.

## Addendum 11: A32, manual voter release as a channel for local abuse, written on 29/10/2026 BEFORE reading any new log or computing any A32 statistic

**Order declaration.** What I had already seen before this addendum: (i) the A21 result (short intervals between voter enablings, time of the last vote, association with the vote, in the section sample), (ii) the result of H1, H2 and A20b-3b (manual voter release rate per section, BWeb), (iii) the format of the log of one Roraima voting machine (messages "Eleitor foi habilitado", "Tipo de habilitação do eleitor [biométrica]", "Solicitação de dado pessoal do eleitor para habilitação manual", "Mesário ... habilitou o eleitor"). I had not seen any burst count, any fraction of manual release in the last hour or any section with extreme manual release by age.

**Unit and sources.** Section-day (each section, in 2022 and 2026, T1 and T2). Source of the per-section manual release: (a) BWeb, `biom_nh / comparecimento` (rate already used in H1, H2 and A20b), all sections, 2022 and 2026, T1 and T2; (b) the voting machine log, per enabling, in the section sample already defined in A4/A5/A21 and in all Roraima sections. **The runoff log contains the events of both days** (the 1st-round one carries dates of 04/10/2026 and 02/10/2022 in the runoff file): each log read provides T1 and T2 of the same machine, and the section is flagged when the log's enabling count does not match the BU turnout. **NOT EXECUTED:** the logs of all sections in both years (about 1 million files; the public per-UF zips weigh tens of GB each). Coverage is declared as in A24 ("N sections out of 499.205, partial").

**Item 1: complete A21 (logs).**
1. **Year of birth: NOT EXECUTABLE.** The log does not record the date of birth or the voter's identifier in a usable form, and the project **neither extracts nor stores** voter ID, CPF or poll-worker identification (personal data). The time sequence is by **type** of enabling (biometric or manual) and by time.
2. **Event.** Enabling = line "Eleitor foi habilitado". Type: **manual** if, between the previous enabling and this one, there is "Solicitação de dado pessoal do eleitor para habilitação manual" and "habilitou o eleitor"; **biometric** if there is "Tipo de habilitação do eleitor [biométrica]"; **other** in the remaining cases (reported, not discarded).
3. **Burst.** k or more **consecutive manual** enablings (no biometric in between) in which each interval between consecutive enablings is shorter than the **5th percentile of the section-day's own intervals** (all intervals between consecutive enablings of the section on the day). k = 3 (main) and k = 5 (sensitivity). A section-day with fewer than 100 enablings does not enter the burst test (unstable p5); it enters the other measures. Measures per section-day: number of bursts, fraction of manual enablings inside bursts, **fraction of manual enablings in the last hour** (60 minutes before nominal closing) and, alongside, the fraction of **all** enablings in the last hour (reference).
4. **Association with turnout and vote.** Per-section models, polling-place fixed effect, standard error clustered by venue (`fe_ols`/`Registro` from `lib_auditoria.py`): (M1) T2 turnout ~ T2 burst indicator + T1 turnout; (M2) Lula's share (valid votes) in T2 ~ T2 burst indicator + T1 share; (M3) 2022 -> 2026 turnout change (T2) ~ 2026 burst indicator, in the sections that exist in both years. Placebo of each M1 and M2: the same regression in 2022. Verdict by the rules already used (intersection-union against the placebos, Holm over the A32 family, worst-case ceiling in margin votes, factor 2 for Lula's share and factor 1 for turnout, exposure = T2 valid votes or registered voters). The comparison of the **frequency** of sections with bursts between 2026 and 2022 is done on the same sections, with section fixed effect and standard error clustered by municipality.
5. **Prediction with abuse:** bursts concentrated at the end of the day (manual fraction in the last hour above the fraction of all enablings in the last hour), in sections with a turnout jump, and more frequent in 2026 than in 2022. **Without abuse:** same frequency in both years and no association with turnout or vote. Objective criterion: the verdict of each line of the A32 family and the sign and order of magnitude of the frequency difference.

**Item 2: sections with extreme manual release (BWeb, all sections).** Extreme: manual rate > 30% and > 50% of voters (two cutoff lines, with turnout >= 30). For 2022 and 2026, T1 and T2: count, by UF, venue type (the same classification as A27), mean age of the section's electorate (midpoints of the bands of the per-section electorate profile, 100+ = 102; a section without a profile is left out and counted), turnout and Lula's share **against the other sections of the same venue** (mean difference within the venue, control of the same measure in T1 in T2).

**Item 3: ceiling in margin votes.** Model of the T2 manual rate **fitted on 2022** (least squares weighted by voters), regressors: fraction of registered voters by age band of the section profile (grouped into 16 to 29, 30 to 44, 45 to 59, 60 to 69, 70 to 79, 80 or more), fraction with registered biometrics and UF fixed effect; applied to the 2026 sections with the 2022 coefficients. Section excess = max(0, observed manual - predicted manual) in voters. **Worst-case ceiling, not an estimate (factor 1):** sum of the excesses in margin votes, assuming all in favor of a single side; and, alongside, (a) the same sum for 2022 within the sample (reference: how much the model overshoots in a year without the hypothesis), (b) the excess beyond 1,645 standard deviation of the 2022 residual (the part the model's noise does not explain) and (c) the excess after removing the national shift (median of the residual). The five numbers are published; the ceiling is the largest of them and is labeled as such.

**Item 4: log integrity.** Record, in the read sample, the fraction of sections whose log hash appears in the list signed by the voting machine (A4) in 2022 and in 2026, and that **signature verification** (pending, A18/A29) is what closes the hypothesis of log alteration after the machine; while pending, the result holds as "the log is what the machine listed", not as "the log is authentic".

**Item 5: paper documents.** Draft (i) an LAI request and (ii) a template request for parties, asking, for the 50 sections with the largest manual release excess in 2026 T2 (item 3; sections with bursts enter if item 1 finds them, and the final list carries each one's criterion), a copy of the poll-workers' minutes and of the voting sheet or book. **Fixed test** (to be executed when the documents exist; **NOT EXECUTED** until then): signatures and voters of the minutes x BU turnout x log enablings; checking script `scripts/37_confere_ata.py` with CSV input. No request is filed by the project.

**What A32 does not do.** It identifies neither voters nor poll workers; manual voter release has legitimate uses (unrecognized fingerprint, voter without biometrics, elderly); the excess over the age model is not fraud, it is only what the 2022 model does not predict.

## Addendum 12: A12b, allegation "106 voting machines with 100% for Lula and 0% blank, null and Flávio", written on 29/10/2026 BEFORE computing the probabilities

**Order declaration.** A12 has already published the counts of sections with zero votes for the opponent (106 in 2026/T2 by the "all counted" definition, 81 in T1; 143, 328 and 192 in 2022, 2018 and 2014 in T2) and the list of the 106 sections (`A12_a12_secoes_zero_2026.csv`). I had **not seen** how many of those 106 also have zero blank and zero null, nor the expected value of that coincidence.

**Definitions.** Universe: counted sections, overseas included (the definition that gives 106 in A12). **Zero opponent** = Flávio votes (Bolsonaro, Aécio) = 0. **Zero BN** = blank = 0 and null = 0. **Triple zero** = both.

**Expected.** For each section with zero opponent, the probability of zero blank and null given turnout n and the blank-and-null rate r of the **other sections of the same polling place** (if the venue has only one section, those of the municipality): p0 = (1 - r)^n. Sensitivity variant: r of the whole municipality. Expected = sum of p0; observed = count of triple zeros; exact p by the Poisson-binomial distribution (upper tail). The same calculation for the series 2014, 2018, 2022 and 2026 (T1 and T2). **Prediction without manipulation:** the observed stays close to the expected. Design observation: sections with zero votes for the opponent are small or very unanimous sections; that is why the expected uses the section's own turnout, not a general rate.

**For each of the 106:** UF, municipality, venue type, registered voters, turnout, Lula votes, blank, null, result in T1/2026 and in the same section in 2022 (T2 and T1); list in `results/fase3/A12b_106_secoes.csv`.

**Ceiling in margin votes (worst-case ceiling, not an estimate).** (i) If all Lula votes in those 106 sections were invalid (as in A27): sum of Lula votes, factor 1. (ii) If those votes were switched: expected opponent votes in those sections from the opponent's share in the other sections of the venue (T2) x valid votes, factor 2. Both are published, neither is an estimate.

**Allegation inventory.** New line: the image claims "0% blank and null" and 106 voting machines; the original report said "100% of valid votes" for unanimous sections (with at least 30 valid votes; 103 for the PT in 2026 T2 by the original report's count, A12/H). The difference is recorded: 100% of valid votes admits blank and null above zero; "0% blank and null" is a stronger claim; and 106 (zero opponent, any size) is not the same set as 103 (unanimous with at least 30 valid votes).

### Addendum 11a: additions to A32 written on 29/10/2026 after validating the log extractor and BEFORE computing any burst or last-hour fraction

**What I saw.** Only the extractor validation on Roraima 2026: the log's enabling count matches the BU turnout in 97,8% of sections, and the log's manual fraction has a 0,994 correlation with BWeb's `manual_rate` (4,18% against 4,14%). No burst had been counted.

1. **Comparison base by permutation (new, for the bursts).** In each section-day, the type labels (M, B, O) are shuffled keeping the timestamps and the count of each type (200 permutations, seed 20261029); the expected number of bursts and the probability of at least one burst come from that distribution. Reason: with few manual releases, chance bursts depend on the number of manual ones; the observed/expected ratio is the measure comparable across years. The raw frequency remains published alongside.
2. **Sample selection.** The A4/A5/A21 section sample is stratified (L: late closing; C: same-venue control; H: turnout of 95% or more; R: random 60 per UF), plus **all** Roraima sections. A32's M1 and M2 models use the sample by stratum with a selection problem on the outcome (H chooses sections by turnout). **Main:** stratum R plus all of Roraima (selection independent of the outcome). **Sensitivity:** all strata, labeled "selection on the outcome".
3. **Log consistency.** A section-day enters the models if the log's enabling count is within 5% of the BU turnout and has at least 100 enablings; the rest go into a separate table.
4. **M3 (2022 -> 2026 turnout change)** has no placebo (there is no second pair of elections with logs); it is **descriptive** (coefficient and standard error), outside the Holm family.
5. **Day 1 (1st round).** The same measures are computed for the 1st round (the runoff log carries both days) and published as descriptive; the association models use the runoff (which decides the margin) and the 1st round as control.

### Addendum 11b: how to compute the expected by permutation, written on 29/10/2026 BEFORE computing any burst

The expected of Addendum 11a (permuting the type labels keeping timestamps and counts) is computed in **exact form**, not by 200 draws: within each chain of consecutive enablings linked by intervals shorter than the section-day's p5 (length Lc), the expected number of bursts of k or more is the sum, over the start positions, of f(k) (chain start) or f(k) - f(k+1) (other positions), with f(s) = product of (m - i)/(n - i), i from 0 to s-1, for m manual in n enablings. This is the expectation over all permutations. The probability of at least one burst is approximated by 1 - exp(-expected) (Poisson approximation, declared). Nothing else changes in the design.

### Addendum 11c: reading of the A32 ceiling (item 3), written on 29/10/2026 AFTER seeing the item 3 result and BEFORE running item 1 (bursts)

**What I saw.** The 2022 model predicts **more** manual release in 2026 (11,6 million voters) than observed (8,63 million): the manual rate fell, and the median residual is -2,7 percentage points. The "(c) after removing the national shift" variant of Addendum 11, written with an upward shift in mind, **adds 2,7 points to each section** when the shift is downward, and becomes the largest of the four numbers (1,85 million margin votes, 41,8% of the margin) by construction, not by real excess. The registered rule ("the ceiling is the largest of the numbers") is followed and that value is published as the registered ceiling; **alongside**, with the label "post-result reading", enter: (a) sum of positive excesses, (b) beyond 1,645 standard deviation of the 2022 residual and (d) the same sum of (a) for 2022 within the sample. The shift variant only makes sense when the shift is positive; in 2026 it is not. Nothing in the registered lines is altered.

### Addendum 11d: supplementary measure of A32 (item 1), written on 29/10/2026 AFTER seeing the result of the registered bursts and BEFORE running the supplementary one

**What I saw.** With the registered definition (k or more consecutive manual releases with all intervals below the 5th percentile of the section's own intervals), **no section-day has a burst**, in any year, day or k (3 or 5), in about 13 thousand section-days per year and day, with a permutation-expected of 0,03% to 0,1% of sections. Without variation, the association models with turnout and vote **are not estimable** (NOT EXECUTABLE, official line) and the frequency difference between years is 0 against 0. The fraction of manual releases in the last hour is **lower** than the fraction of all enablings in the last hour in both years. This stands as the registered result.

**Why.** A manual release requires typing a voter's data and the poll worker's biometrics; it takes tens of seconds, and the p5 of the intervals of all the section's enablings falls below that. The registered definition cannot detect bursts by construction, and that is stated.

**Supplementary measure (post-hoc, exploratory, outside the main family's Holm).** **Clustering of manual releases, with no time condition:** sequence of k or more consecutive manual enablings, with no biometric enabling in between (k = 3 and 5), with the exact expected by permutation (the same calculation as Addendum 11b, with all intervals considered linked). It measures whether manual ones cluster into blocks in arrival order more than chance. Also published are the quantiles of the interval that **precedes** each manual and each biometric enabling (aggregated by year, without identifying the section), to show the typical duration of each type. Association models (M1, M2, M3, frequency 2026 against 2022) repeated with the indicator "at least one cluster of k = 5" (and k = 3 as sensitivity), in a separate family "A32-sup" with its own Holm, labeled post-hoc.

## Addendum 13: A31b, the municipalities with dFlávio <= +1, written on 29/10/2026 BEFORE running any simulation or profile of this stage

**Order declaration.** I have already seen, in A31 (S2), that 748 of the 5.357 eligible municipalities (14,0%) of 2026 have the opponent's gain between rounds less than or equal to +1, against 0,15% (2022), 1,6% (2018) and 1,2% (2014). I had not seen the profile of those 748 (UF, region, size, 1st-round composition, turnout, manual release, voting machine model), nor the simulation below, nor the decomposition by turnout change.

**Universe.** The eligible municipalities of 2026 (T1 -> T2 pool of at least 20 votes, A31) with dF <= 1 (dF = opponent's vote in T2 minus in T1).

**1. Expected fraction under the national shift.** For each comparison year y (2022, 2018, 2014): g(i,y) = dF(i,y) / opponent's T1 vote (i,y), per municipality. G(UF,y) = sum of dF / sum of the opponent's T1 vote in the UF's eligible municipalities in year y, and G(UF,2026) the same in 2026. Shift per UF: d(UF,y) = G(UF,2026) - G(UF,y) (additive). **Main simulation (paired):** for each eligible 2026 municipality that exists in year y, dF' = (g(i,y) + d(UF,y)) x the municipality's opponent T1 vote in 2026; expected fraction = proportion with dF' <= 1 among those municipalities. **Sensitivity (resampling):** for each 2026 municipality, g is drawn from a municipality of the same year y and the same UF (200 draws, seed 20261029), d(UF,y) is added, and the fraction is computed; mean and 2,5% to 97,5% interval are reported. **Comparison:** the observed fraction (14,0%) against the three expected fractions and the intervals. **Prediction without anomaly:** the observed fraction falls within the interval of the expected ones (from the smallest to the largest of the three years, or within one of the resampling intervals); above all = ABOVE EXPECTED; below all = BELOW. Declared limitation: the shift only equalizes the mean growth per UF; it does not reproduce the shape of the 2026 distribution.

**2. Profile.** For the 748 and for the other eligible ones: UF and region (IBGE; UF -> region), size (T1 registered voters: up to 5 thousand, 5 to 20 thousand, 20 to 100 thousand, over 100 thousand), opponent's and third parties' share of T1 turnout, T1 -> T2 turnout change (% of T1 turnout), runoff manual release rate (BWeb, municipal weighted), fraction of sections per voting machine model (UE2009 to UE2022). Comparison by ratio (group fraction / fraction of the rest) for categories and by median for continuous measures. **Descriptive, confounded by region and size; no p-value is the conclusion.**

**3. Decomposition.** Among the 748: (a) turnout fell (dC < 0), compatible with selective abstention; (b) turnout rose or stayed equal (dC >= 0), in which a stalled opponent would require new voters going to the PT or vote switching. Lower bound of vote switching by net balance: S(i) = max(0, -dF - max(0, -dC) - max(0, BN(T2) - BN(T1))), how much of the opponent's loss does **not** fit into a net turnout drop nor into an increase in blank and null votes; count and sum. **The net balance does not distinguish vote switching from selective abstention** (one opponent voter who abstains and one new PT voter cancel out in the net); the sentence goes on the card.

**4. The 20 with the largest absolute opponent loss** (most negative dF among all 2026 municipalities, with turnout of at least 1.000 in T1): list of **all sections** with T1 and T2 and empty columns for the printed BU (format of `04_cruza_bu_impresso.py`), in `results/fase3/A31b_20_secoes.csv`.

**5. Ceiling in margin votes (worst-case ceiling, not an estimate), factor 2.** (A) Sum, over the 748, of max(0, G(UF,2026) x opponent's T1 vote - dF), assuming all is vote switching. (B) Excess of (A) over the mean of (A) in the paired simulations of the three years (floor zero): the part of the missing gain that the national shift does not reproduce. Both are published; what enters the G3 chart is (B) (display rule of Addendum 14, below).

**Card** on the first page, block a, with the ceiling (B) and the sentence "does not distinguish vote switching from selective abstention".

**Municipality TSE 73709.** Name and installation-date check, recorded in the CHANGELOG with the sources: the TSE municipality table used in A20 gives BOA ESPERANÇA DO NORTE; the 13 sections of 2026 include 5 sections that in 2022 belonged to Sorriso, 4 to Nova Ubiratã and 4 new ones; installation date from a secondary source, to be checked against an official source.

## Addendum 14: A32b (bursts with an absolute threshold) and the G3 display rule, written on 29/10/2026 BEFORE running A32b

**Display rule (G3).** The G3 chart does not plot ceilings inflated by construction. For A32, the bar is the excess **beyond the 2022 model's noise** (55.862 margin votes); the registered ceiling of 1.852.233 (Addendum 11c) appears **only as text**, with the reference to Addendum 11c. General rule: when a registered ceiling is mechanically inflated, the chart shows the corrected variant and the text carries the registered one, with the reason.

**A32b: bursts redesigned with an absolute threshold (requested item).** Addendum 11d showed that the p5 of the section's intervals cannot see bursts because a manual release takes longer than that. New definition, fixed now: in each section-day with at least 10 manual releases, the threshold is **1,5 x the median of the interval preceding the section-day's own manual releases**; **burst of k** = k or more consecutive manual releases, **with no biometric enabling between them**, with all intervals between consecutive enablings **less than or equal to the threshold**. k = 3 main, k = 5 sensitivity. Expected: the same exact permutation calculation of Addendum 11b, with the links given by the intervals <= threshold (declared approximation: the threshold comes from the observed labels and is kept in the permutations). Threshold sensitivity: 1,5 x the **national** median of the interval preceding the manual ones of the year and day (instead of the section median). 2022 x 2026 comparison: frequency of sections with bursts on the same sections (section fixed effect, standard error clustered by municipality), observed/expected ratio and fraction of manual ones inside bursts; association with turnout and Lula's share (M1, M2: main sample = stratum R plus all of Roraima; sensitivity: all strata; venue fixed effect, 1st-round control; 2022 placebo; "A32b" family with its own Holm; ceiling in margin votes by the rules already used) and descriptive M3. **Prediction with abuse:** more bursts in 2026 than in 2022, above expected, with positive association with turnout or with Lula only in 2026. **Without abuse:** equal frequency and ratio between years and no association.

## Addendum 15: A33, manual voter release at the polling place (school) level, written on 29/10/2026 BEFORE running any item of this stage

**Motivation (from the request).** The per-venue fixed effect, used in H1, A32 and others, eliminates any effect common to all sections of a school; a scheme at the school level would be invisible to those tests.

**Unit.** Polling place (key UF + municipality + zone + venue number of the BWeb), summing the counted sections. Schools with turnout of at least 100 in each round used. School manual release rate = sum of `biom_nh` / sum of the runoff turnout.

**1. Descriptive (2026 T2 and 2022 T2).** Bands of the school manual rate: up to 5%, 5 to 10%, 10 to 20%, 20 to 30%, 30 to 50%, over 50%. Per band: schools, sections, voters, Lula votes (PT's in 2022) and Flávio votes (opponent's), and in how many schools the PT had more valid votes. **Descriptive, confounded by age and region.**

**2. Test.** Unit = school. Outcomes: change in Lula's share of valid votes (T2 - T1), change in turnout (T2 - T1); symmetry for the opponent: change in the opponent's vote per registered voter and of the PT per registered voter. Regressor: the school's manual rate in T2; and, in the excess variant, the 2026 rate minus the 2022 rate of the same school (schools in both years). Fixed effect of **electoral zone** (standard error clustered by zone) and, as robustness, of **municipality** (clustered by municipality). Controls: mean age of the school's electorate (per-section electorate profile, weighted by registered voters) and the PT's T1 share. **Placebo: the same model in 2022 and 2018** (excess variant: 2022 against 2018, for 2022). Verdict by the `Registro` rules (intersection-union against the placebos, Holm over the A33 family, worst-case ceiling in margin votes: factor 2 for share, factor 1 for turnout). For 2018 the age profile needs to be re-aggregated (local zips); if unavailable, 2018 goes without the age control and that is declared.

**3. Extreme schools.** Each school's manual release excess over the age-expected: observed rate in 2026 T2 minus the one predicted by a model fitted **on 2022** at the school level (manual rate ~ age composition, registered biometrics and UF fixed effect, weighted by voters). **Top 1% of the excess**, among schools with 100 or more voters; if the school exists in 2022, an excess over the same school's 2022 rate greater than zero is also required (schools absent in 2022 enter only by the first criterion and are flagged). List with UF, municipality, zone, venue, sections, voters, T1/T2 result of 2026 and of 2022. **Worst-case ceiling, not an estimate (factor 1):** sum of the voter excesses in the extreme schools; and the part beyond 1,645 deviation of the 2022 residual.

**4. Synchrony in the logs (available sample).** Schools with 3 or more sections with a consistent log on the same day (in practice, mostly Roraima, where all sections were read; the stratified sample of the other UFs rarely has 3 sections of the same school; coverage is declared). Statistic: number of pairs of manual releases from different sections of the same school with timestamps within 60 s (sensitivity: 180 s), divided by the number of possible pairs. **Main null (N1):** in each section, the "manual" labels are drawn among the section's own enablings (preserves each section's timestamps and pace and the day's pattern), 500 permutations, seed 20261029. **Sensitivity (N2), which corresponds to the request's "shuffle the timestamps between sections":** pair sections of **different** schools of the same UF, same year and day, with the same number of pairs. Compare the observed/expected ratio of 2022 and 2026.

**5. Most extreme schools and paper.** The 20 most extreme schools (the first 20 of item 3) enter LAI request 07 (all their sections, in both rounds) and a list of printed BUs to collect (`results/fase3/A33_20_escolas_secoes.csv`, empty columns for the printed one).

**Prediction without a scheme:** association at the school level equal to the placebos', no synchrony above chance, extreme ones explained by age. **With a scheme:** excess of Lula gain and of turnout in the schools with manual release excess **only in 2026**, and synchrony above chance.

### Addendum 15a: exposure of the A33 ceiling, written on 29/10/2026 AFTER seeing the first execution (with an error of mine) and BEFORE running the corrected version

**My error.** In the first execution I converted the A33 coefficients into margin votes using as exposure **all** valid votes (and all registered voters) of 2026/T2. Since the regressor is the manual release **rate** (from 0 to 1, mean near 0,07), that overestimates the ceiling by about 14 times: it produced ceilings of 74% to 116% of the margin that mean nothing. The project already had the right convention in H1 (`h1_exposicao_votos_manuais_equiv`): exposure = sum of (section manual rate x valid votes) for share, and sum of (section manual rate x registered voters) for turnout. That convention now applies in A33 and it is recorded that the first execution was wrong. The lines of the first execution are not published.
