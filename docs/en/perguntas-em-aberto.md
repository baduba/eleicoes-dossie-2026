# Open questions: what the tests could neither explain nor confirm

> **Before the gaps, the verified result:** 0 discrepancies across the RDV–BU–BWeb–tabulation chain; the summed measured excess is small next to the margin. The tests cover what the TSE publishes; an alteration in the links that are not published (typed vote, printed receipt, transmission) is something no test in this dossier would see. Figures on the [home page](index.md).


**They are not evidence of anything, on either side: they are gaps that only new data can close. If you have data or a method to close any of them, contribute.**

Each card presents the question, the status, the direction of the effect (in whose favor, if any), the worst-case ceiling in margin votes with the caveat on the same line, and what would close the question. Within each block, the order follows the size of what an answer could change (largest ceiling or largest blind spot first). Ceilings are upper bounds under the worst case; the margin is 4,430,191 margin votes.

### a) Residuals with no identified cause (tests run, inconclusive)

<a id="a-a20b-part"></a>
> **In sections with the most voters aged 80 or older, does the vote share of Lula and of Flávio differ from previous years?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula (ceiling) or Flávio (symmetric side)  
> Ceiling: **worst-case ceiling, not an estimate: 1,787,533 margin votes (40.35% of the margin)** (the 2026 coefficient falls within the placebo interval and the central estimate is negative for Lula; the ceiling comes from dispersion across the comparison years; the side in favor of Flávio has a ceiling of 790,398)  
> What would close it: More comparison years with the voter profile by section and the voter-check-in lists of the sections with the most elderly voters.  
> [Technical page](fase3.html#a20b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-part%20A-A20b-part)

<a id="a-h1-s0"></a>
> **Where there is more manual voter release, does Lula do better? The test lacks the precision to answer.**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula  
> Ceiling: **worst-case ceiling, not an estimate: 1,337,198 margin votes (30.18% of the margin)** (ceiling comes from the test's imprecision, with no measured effect)  
> What would close it: Signed check-in lists by section (voting sheets) and the log of all sections, not only the sample.  
> [Technical page](residuos.html) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H1-S0%20A-H1-S0)

<a id="a-a22"></a>
> **Does the presidential vote match the gubernatorial vote in the same section, as in 2022 and 2018?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Flávio or Lula (symmetric sides)  
> Ceiling: **worst-case ceiling, not an estimate: 548,671 margin votes (12.38% of the margin)** (exploratory variant (Addendum 9b), AM and DF only, low power; valid only for the votes of those two states; the side in favor of Lula has a ceiling of 169,390; the official A22 line is NOT RUNNABLE (no state eligible under the recorded rule))  
> What would close it: Votes per candidate in every office by section across the 27 states, with an alignment rule defined by someone who knows the local alliances; or federal deputies by party in the states without a gubernatorial runoff.  
> [Technical page](fase3.html#a22) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A22%20A-A22)

<a id="a-a20"></a>
> **Are there more very elderly voters registered and voting than the Census population would support?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 459,099 margin votes (10.36% of the margin)** (the ceiling is 80+ turnout above the 2022 rates; the same increase appears in the 70-to-79 age brackets)  
> What would close it: Cross-matching the voter registry with the civil death registry, by an oversight body; voter profile by section, not only by electoral zone.  
> [Technical page](fase3.html#a20) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20%20A-A20)

<a id="a-a34"></a>
> **Is the duration of the vote, from check-in to confirmation, compatible with a voter being present in each section? The 99th-percentile rule shows excess in 2026, but ballot composition explains almost all of it.**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 339,311 margin votes (7.66% of the margin)** (ceiling extrapolated from the excess of 0.24 percentage point over 1% (about 16 sections out of 6,667 in states with the same ballot composition) to the 497,897 sections, with every vote read as belonging to one side: **inflated by construction, not plotted in G3**; in factor 1 of the sample it is 23,093 margin votes; under the registered rule, 2.06% of the 2026/2nd-round sections have D3 above the 99th percentile of 2022 against 1% expected (form excess), which falls to 1.24% in states with the same composition (post hoc diagnostic); the pre-registered prediction for the median (40 s to 2 min) was wrong (the median is 9 s); median and association models with no excess)  
> What would close it: Logs of all sections (power), an official list of the states with a state runoff in each year (to fix the ballot composition without using the outcome) and the log with all offices.  
> [Technical page](fase3.html#a34) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A34%20A-A34)

<a id="a-a20b"></a>
> **In sections with the most voters aged 80 or older, does runoff turnout rise more than in 2022 and 2018?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 241,008 margin votes (5.44% of the margin)** (supplementary line of Addendum 9d (only placebos with the same control); the original line, with a comparator from a different specification, yields 4.07 million; Lula's vote-share coefficient in those sections is negative)  
> What would close it: Signed check-in lists of the sections with the most elderly voters and cross-matching of the registry with the civil death registry, by an oversight body.  
> [Technical page](fase3.html#a20b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b%20A-A20b)

<a id="a-a31b"></a>
> **Why did 748 of the 5,357 municipalities (14.0%) have a Flávio gain between rounds of +1 vote or less, almost all of them in the Northeast and North?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 234,746 margin votes (5.30% of the margin)** (the 14.0% fraction is compatible with the national growth of the opponent in 2026 (expected 13.2% to 15.4% with 2018 and 2022 shifted); 70.6% of these municipalities had a drop in turnout; the ceiling is the whole deficit of Flávio relative to the growth of the state attributed to vote switching, and the excess over what the national shift reproduces is 0; **the test does not distinguish vote switching from selective abstention**)  
> What would close it: Printed bulletins of the sections of the 20 municipalities with the largest loss for Flávio (list in `results/fase3/A31b_20_secoes.csv`) and the check-in lists.  
> [Technical page](fase3.html#a31b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A31b%20A-A31b)

<a id="a-a33-placebo"></a>
> **Why is the 2026 coefficient of the school's manual release on Lula's gain (-0.017) more negative than the 2022 placebo's (-0.002)?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 221,830 margin votes (5.01% of the margin)** (**cause not identified**; the sign is the opposite of the pre-registered scheme (more manual release, less Lula gain and lower turnout), the 2018 placebo has the same negative sign, and no excess test passes Holm; the ceiling comes from the coefficient's uncertainty times exposure, not from a measured effect, and so **it is not plotted in G3** (display rule, CHANGELOG))  
> What would close it: Abstention by age group and by section for the 2nd round (TSE product not yet published) and the composition of the schools (rural, age), to separate a composition effect from an effect of manual release.  
> [Technical page](fase3.html#a33) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A33-placebo%20A-A33-placebo)

<a id="a-a10"></a>
> **Do voting machines of the newest model (UE2022) vote differently from the others within the same polling place?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula  
> Ceiling: measured excess: 56,317 margin votes; **worst-case ceiling, not an estimate: 137,809 margin votes (3.11% of the margin)**  
> What would close it: More sections with the new model in 2022 to serve as comparison, or the load code per voting machine (LAI request 02).  
> [Technical page](resultados-fase2.html#a10) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A10%20A-A10)

<a id="a-h1-fl"></a>
> **Where there is more manual voter release, does Flávio do better than the first round predicts?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Flávio  
> Ceiling: measured excess: 101,285 margin votes; **worst-case ceiling, not an estimate: 122,543 margin votes (2.77% of the margin)**  
> What would close it: Signed voting sheets by section and reports from party observers.  
> [Technical page](residuos.html) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H1-FL%20A-H1-FL)

<a id="a-h6"></a>
> **Do sections created after 2022 vote differently from the older ones in the same polling place?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula  
> Ceiling: **worst-case ceiling, not an estimate: 92,023 margin votes (2.08% of the margin)** (negative central estimate: no measured excess)  
> What would close it: The list of created sections, with date and reason for creation, and the address of each polling place (request to the TSE).  
> [Technical page](residuos.html) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H6%20A-H6)

<a id="a-a32"></a>
> **Why do 348 sections have more than 30% manual voter release in the runoff, 97 of them with more than 50%, mostly in Bahia and Rio Grande do Sul?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 55,862 margin votes (1.26% of the margin)** (ceiling = what lies beyond the noise of the 2022 model; the recorded ceiling of 1,852,233 margin votes appears only here, as text, because it is inflated by construction (Addendum 11c, negative national shift); manual voter release fell from 2022 to 2026 (3,995 sections above 30% in 2022); no bursts and no association with turnout or vote)  
> What would close it: The polling-station minutes and voting sheet of the 50 sections with the largest excess in A32 (`lai/07_secoes.csv`; request `lai/07_ata_e_folha_de_votacao.md`), the logs of all sections, and verification of the log signatures.  
> [Technical page](fase3.html#a32) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A32%20A-A32)

<a id="a-h5"></a>
> **Why did 639 sections have turnout of 95% or more, 427 of them new?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula  
> Ceiling: measured excess: 11,266 margin votes; **worst-case ceiling, not an estimate: 44,735 margin votes (1.01% of the margin)** (ceiling: all of Lula's votes in the 427 new sections, an invalid assumption)  
> What would close it: Origin of the voter transfers into those sections and the history of the polling places (nominal registry, by the Electoral Court).  
> [Technical page](fase3.html#a27) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-H5%20A-H5)

<a id="a-a35"></a>
> **Are there more large sections without blank and null votes, or with turnout of 100% of registered voters, than chance gives?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 41,614 margin votes (0.94% of the margin)** (ceiling = switch expected from the neighborhood (factor 2); in factor 1 (all votes of the majority candidate in those sections) it would be 403,773 margin votes, inflated by construction; the observed count is **below** the expected one in every year (ratio 0.69 in 2026 and 0.70 in 2022), within expectation under the pre-registered rule; 12 sections with turnout equal to registered voters (descriptive, no p))  
> What would close it: Printed poll-receipts of the flagged sections (list in `results/fase4/A35_E1_sinalizadas_2026T2.csv`, 2,989 sections with 100 voters or more and zero blank and null; and the 12 with turnout equal to registered voters in `results/fase4/A35_E2_secoes_2026T2.csv`).  
> [Technical page](fase3.html#a35) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A35%20A-A35)

<a id="a-a12b"></a>
> **Why do 29 of the 106 sections with zero votes for Flávio also have zero blank and null votes, more than their neighbors indicate (and also in 2022 and 2018)?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: in favor of Lula (ceiling) or Flávio (symmetric side)  
> Ceiling: **worst-case ceiling, not an estimate: 14,860 margin votes (0.34% of the margin)** (the "0% blank and null" claim holds for 29 of 106; the excess over expected exists in every election (ratio of 1.4 in 2026, 1.4 in 2022, and 2.2 in 2018); ceiling: all of Lula's votes in the 106 sections, if they were invalid)  
> What would close it: Printed poll-receipts (BUs) and check-in lists of those 106 sections (list in `results/fase3/A12b_106_secoes.csv`) and of the equivalent sets of 2022 and 2018.  
> [Technical page](fase3.html#a12b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A12b%20A-A12b)

<a id="a-a33"></a>
> **Why do 661 schools have much more manual voter release than the age of the electorate and the year 2022 indicate, and did they gain or lose Lula votes between rounds?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 8,125 margin votes (0.18% of the margin)** (ceiling = the excess of manual voter release beyond the noise of the model, read as votes for one side only (factor 1); without that cut, the ceiling is 29,654 margin votes; at school level, more manual release is associated with **less** Lula gain and lower turnout in 2026 (placebos show no excess); synchrony in the logs is the same as in 2022; 92% of the extreme schools have 3 sections or fewer)  
> What would close it: Minutes, voting sheet and printed bulletin of the 20 most extreme schools (`results/fase3/A33_20_escolas_secoes.csv`, 40 sections; request `lai/07_ata_e_folha_de_votacao.md`) and the logs of all sections.  
> [Technical page](fase3.html#a33) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A33%20A-A33)

<a id="a-a33-idade"></a>
> **Why are the schools with extreme manual release not explained by the age of the electorate, as the A33 pre-registration predicted?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 8,125 margin votes (0.18% of the margin)** (**the pre-registered prediction (extremes explained by age) was not fulfilled**: in the first 20, the mean age is 32 to 59 years, the predicted rate is 6% to 15% and the observed 30% to 82%; ceiling = the excess of manual release beyond the noise of the model, read as votes for one side only (factor 1); without that cut, 29,654 margin votes; 92% have 3 sections or fewer; on average, Lula gained less in them (+1.5 point) than nationwide (+3.0); already described in card A-A33)  
> What would close it: Minutes, voting sheet and printed poll-receipt of the 20 most extreme schools (`results/fase3/A33_20_escolas_secoes.csv`, 40 sections) and the logs of all sections; the operational cause (a faulty biometric reader, for example) is only confirmed or ruled out with the section's log and minutes.  
> [Technical page](fase3.html#a33) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A33-idade%20A-A33-idade)

<a id="a-a20b-95"></a>
> **Why did voters aged 95 or older who voted in 2026 exceed what the 2022 ratio predicts?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 7,059 margin votes (0.16% of the margin)** (z = 2.42, Holm 0.054: passes the 2-standard-error cut and fails Holm; about 4,205 extra voters, out of 16,659)  
> What would close it: Cross-matching the 95+ registry with the civil death registry and the signed check-in lists for that age bracket.  
> [Technical page](fase3.html#a20b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-95%20A-A20b-95)

<a id="a-a31"></a>
> **Why do three small municipalities (Itacoatiara/AM, Santo Antônio de Lisboa/PI, Rafael Godeiro/RN) fall outside the expected tail of first-to-runoff vote transfer?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: **worst-case ceiling, not an estimate: 1,151 margin votes (0.03% of the margin)** (Silva Jardim (the claim) falls within the tail; in the 3 municipalities the pool is small and the opponent lost votes in nearly the same amount as the PT gained, with falling turnout; if everything the model does not explain in the 20 most extreme were manipulation, it would be 13,327 margin votes)  
> What would close it: Printed poll-receipts (BUs) and check-in lists by section for those municipalities, and the section-level turnout variation between rounds.  
> [Technical page](fase3.html#a31) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A31%20A-A31)

<a id="a-a5-2022"></a>
> **Why does one 2022 section have one fewer vote in the log than in the poll-receipt (BU)?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: measured excess: 1 margin vote; **worst-case ceiling, not an estimate: 1 margin vote (less than 0.01% of the margin)** (one 2022 section: 348 turnouts in the poll-receipt, 347 votes in the log)  
> What would close it: The voting machine record for that section (RJ, zone 7, section 479) and the voting record.  
> [Technical page](resultados-fase2.html#a5) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A5-2022%20A-A5-2022)

<a id="a-a1t1"></a>
> **Why does the 2026 first-round counting curve leave the expected envelope between 76% and 99.9% of sections?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: no figure (shape test, not convertible into votes) (shape test; the final sum does not depend on the order)  
> What would close it: The reception log of the tabulation system (LAI request 04) and the actual transmission order by municipality.  
> [Technical page](a18-alteracao-no-meio.html#3b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A1T1%20A-A1T1)

<a id="a-a20b-3b"></a>
> **Where there are more voters aged 90 or older, there is more manual voter release, and it grows with each election. Why?**  
> Status: **TESTED-INCONCLUSIVE** · Direction: no identifiable direction  
> Ceiling: no figure (shape test, not convertible into votes) (shape test; the coefficient rises from 0.35 (2018) to 0.80 (2026, runoff))  
> What would close it: The age of those released manually (check-in list by section) and registered biometrics per voter, in aggregate form.  
> [Technical page](fase3.html#a20b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-3b%20A-A20b-3b)

### b) Hypotheses not yet tested (Phase 3, A20 to A28)

<a id="a-a20b-t2"></a>
> **Does turnout among voters aged 80 or older in the 2026 runoff match that of the first round?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run) (the public 2026 file contains only the first round; the 2018 and 2022 runoff files were published)  
> What would close it: It closes when the TSE publishes the turnout profile for the 2026 runoff (weekly check: `scripts/verifica_perfil_t2.sh`, run every Monday by a GitHub action).  
> [Technical page](fase3.html#a20b) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A20b-T2%20A-A20b-T2)

<a id="a-a24"></a>
> **Did the voting machines that went to the integrity test and were replaced in their sections vote differently from their neighbors?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run) (script ready; no list read)  
> What would close it: The list of zone and section published by each TRE (regional electoral court), in `data/a24_secoes_teste_integridade.csv` (the TRE websites block automated access), or LAI request 03.  
> [Technical page](fase3.html#a24) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A24%20A-A24)

<a id="a-a25"></a>
> **Did sections where the voting machine was swapped vote differently before and after the swap?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run)  
> What would close it: Time and reason for each swap and the record of the original voting machine (LAI request 01). The comparison of swapped sections versus neighbors has already been done (A6) and found no effect.  
> [Technical page](fase3.html#a25) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A25%20A-A25)

<a id="a-a23"></a>
> **Where a party observer was present, was the vote different from where there was none?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run)  
> What would close it: List of sections with a party observer, provided by parties and coalitions (format on the page).  
> [Technical page](fase3.html#a23) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A23%20A-A23)

<a id="a-a21"></a>
> **Is the pace of votes over the day (bursts, concentration in the last hour) the same as in 2022?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run) (only the measures already extracted were tested)  
> What would close it: Re-reading the voting machine logs with the full distribution of intervals; year of birth is not in the public logs.  
> [Technical page](fase3.html#a21) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A21%20A-A21)

<a id="a-a28"></a>
> **How do the TSE and the TREs respond to freedom-of-information requests?**  
> Status: **NOT TESTED** · Direction: n/a  
> Ceiling: no figure yet (test not run)  
> What would close it: Filing the seven ready-made requests in `lai/` (body and channel for each in `lai/canais.csv`) and recording protocol number, deadline, and response, including refusals.  
> [Technical page](fase3.html#a28) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A28%20A-A28)

### c) Structural blind spots (A18, A19)

<a id="a-a18"></a>
> **Could someone alter the results after the voting machine closes and before the files are published, in a coherent way?**  
> Status: **NOT TESTABLE WITH PUBLIC DATA** · Direction: n/a  
> Ceiling: not measurable with public data  
> What would close it: Verifying the signature of each poll-receipt (BU) with the official key and checking printed poll-receipts at the sections.  
> [Technical page](a18-alteracao-no-meio.html) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A18%20A-A18)

<a id="a-a19a"></a>
> **Is the vote the voter types the same one the voting machine records?**  
> Status: **NOT TESTABLE WITH PUBLIC DATA** · Direction: n/a  
> Ceiling: not measurable with public data  
> What would close it: Only the integrity test, by sampling; the list of sections, the reports, and the videos by state (LAI request 03).  
> [Technical page](a19-voto-digitado.html) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19a%20A-A19a)

<a id="a-a19b"></a>
> **Why doesn't the voter check a record of their own vote?**  
> Status: **NOT TESTABLE WITH PUBLIC DATA** · Direction: n/a  
> Ceiling: not measurable with public data  
> What would close it: A legislative decision: the printed record was declared unconstitutional by the STF (ADI 4543 and ADI 5889). Without a change in the law, there is no way to close this.  
> [Technical page](a19-voto-digitado.html#4) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19b%20A-A19b)

<a id="a-a19c"></a>
> **Can the integrity test detect a small alteration?**  
> Status: **NOT TESTABLE WITH PUBLIC DATA** · Direction: n/a  
> Ceiling: not measurable with public data  
> What would close it: More voting machines in the test (and more with biometrics) and publication of the result by state; the detection curve is in chart G2.  
> [Technical page](a19-voto-digitado.html#3) · [Open an issue](https://github.com/baduba/eleicoes-dossie-2026/issues/new?title=A-A19c%20A-A19c)

