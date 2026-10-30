# Reproducible independent audit: 2026 presidential runoff

This is an **independent audit**. It is not an official report, expert examination, or homologated document: no authority has homologated it. It was built so that any expert, on any side, can reproduce every number and challenge whatever they disagree with.

> **Preliminary version (v0.9.3).** v1.0 will be released after the consolidated TCU (federal audit court) report on the integrity tests (deadline Nov 24, 2026), the verification of the cryptographic signature, and an initial batch of checked printed poll-receipts ([how to submit](boletins-impressos.md)).

## How much of the vote chain public verification covers

<picture><source media="(max-width: 640px)" srcset="img/en/g0_verificacao_m.png"><img src="img/en/g0_verificacao.png" alt="Stacked bar of the 12 links in the vote chain: 4 verified (33%), 5 partially verified (42%) and 3 not verifiable with public data (25%). Below, a second bar indicates that 100% of votes pass through at least one non-verifiable link."></picture>

- **33% of the vote chain fully verified with public data** (4 of 12 links; [full map, G1](#g1-map-of-the-vote-chain)).
- **25% not verifiable** (3 of 12: typed vote → recorded vote, checked printed poll-receipt, transmission).
- **100% of votes pass through at least one non-verifiable link.**
- **0 tests found an effect capable of altering the outcome**; the largest worst-case ceiling, not an estimate, is 40.35% of the margin ([A20b](fase3.html#a20b)).

This is not evidence of anything, on either side: it is a map of where an alteration would pass invisible to public data.

## The two most obvious triggers, checked first

These two patterns looked like the obvious place where an alteration would come cheap; that is why they were tested first, with section-level data.

<div class="duo">
<div>
<h3>Exact ties and 1-vote margins</h3>
<ul>
<li><strong>2,150 sections with an exact tie</strong> between Lula and Flávio in 2026, with <strong>517,768 valid votes</strong>; <strong>4,517 sections decided by exactly 1 vote</strong>, with <strong>1,087,289 votes</strong>.</li>
<li>Against the per-section binomial null: 2,150 ties observed vs 2,337 expected (ratio 0.92); 1-vote margins: 4,517 vs 4,672 (0.97). In every margin band from 0 to 10, 2026 sits <strong>below the null</strong>, as does 2022. The growth in ties (+5.1%) is the growth in the number of sections itself (+5.7%).</li>
<li>Symmetry of the 1-vote margins: 2,268 for Lula and 2,249 for Flávio (p = 0.789). Machine swapped in these sections: at or below the national rate.</li>
<li><strong>Reading:</strong> 2,150 tied machines and 4,517 decided by 1 vote concentrate 1.6 million votes where <strong>neither side can build an advantage</strong>. If the strategy were to tie the score machine by machine, this would be exactly the playing field. The numbers show no statistical surplus (0.92 of expected) and no direction (2,268 to 2,249; p = 0.789); and it is precisely the absence of surplus that demands explanation, because a small tied machine leaves no trace in aggregate tests. <strong>What closes this: the printed receipt of each of these machines, one by one.</strong></li>
</ul>
</div>
<div>
<h3>Northeast: no-biometrics clearance and machine swap</h3>
<ul>
<li>Municipality-by-municipality correlation (1,794 municipalities, by rate): Spearman ρ = 0.06, substantially zero; "capitals have both" is a size effect.</li>
<li>Sections with Lula ≥ 80% and (machine swap or top-10% no-biometrics municipality): <strong>3,469 sections</strong> in 2026, net 537,354 margin votes, ceiling of 24.3% of the margin; in 2022 the same pattern was <strong>larger</strong> (3,766 sections, net 602,222, ceiling 27.2%): it is structural, not specific to 2026.</li>
<li>Opponent between 0 and 10 votes: 3,029 sections in 2026 (net 376,149; 65% in the Northeast), vs 4,097 in 2022 (net 505,308; 73% in the NE): the set shrank by 26%.</li>
<li><strong>Reading:</strong> the set shrank by 26% since 2022 and the pattern is larger in 2022. It could be structure; it could be exactly what a deliberately scaled-down technique would leave. With internal data there is no way to tell one from the other; that is why these sections stay at the top of the verification queue: <strong>the 190 with machine swap and high no-biometrics clearance are asking for the voting sheet and the poll record (LAI request 07 already filed)</strong>.</li>
</ul>
</div>
</div>

<h3>The hypothesis that cannot be taken down on its own</h3>
<p>A sophisticated operation would scale back the visible techniques and introduce new ones, on purpose, so that each isolated test would find "structure" or "decline". With internal data, this hypothesis can be neither confirmed nor refuted: any observed pattern is compatible with it. What keeps it standing as a question, and what would settle it, are the external anchors: printed receipts, the integrity test, the historical series of polls. <strong>This scenario the dossier cannot see; only physical verification can.</strong></p>

<p class="destaque">A refuted pattern does not close the question; a structural one, even less. Anyone who wants to contest the numbers has the scripts and the data here. These two were the most obvious triggers; the ones still open are in <a href="perguntas-em-aberto.html">Open questions</a>.</p>

Details and calculations: [exploratory memo](https://github.com/baduba/eleicoes-dossie-2026/blob/main/docs/propostas/gatilhos-e-inversao.md) (in Portuguese).

## The count that doesn't add up: where did the runoff votes come from

In every runoff since 2002, the votes each finalist gains have to come from somewhere: from aligned eliminated candidates, from those who cast blank or null ballots in the first round, and from new turnout. In 2026, this count does not close without a remainder.

<div class="duo">
<div>
<h3>Lula's side</h3>
<ul>
<li>Lula gained <strong>+10.38 million</strong> votes between the first and the second round. Naturally aligned sources explain 3.7 to 5.5 million. <strong>An unaccounted +4.8 to +6.7 million remain.</strong></li>
<li>To close the count without a remainder, 90 to 99% of the votes of Cury, Caiado and Zema (6.42 million, all with declared endorsement of Flávio) would have had to go to Lula. In the historical series, when an eliminated candidate endorses a finalist, about 73% of their votes follow the endorsement (2014). Cross-over on this scale has no precedent in 2002-2022.</li>
</ul>
</div>
<div>
<h3>The other side, and the honest controls</h3>
<ul>
<li>Mirror: Flávio gained only <strong>+3.72 million</strong>, with an endorsed right-wing pool of about 8.9 million.</li>
<li>Deviations of 2 to 7 million between expected and observed happened in all 7 elections of the series (2014 had an even larger one, against the PT: -6.73 million). What is unprecedented in 2026 is not the size of the deviation: it is the <strong>direction and the composition</strong>. The finalist with the smaller pool gained the largest volume, and the benign closure requires unprecedented electoral behavior.</li>
</ul>
</div>
</div>

Reconciliation with the municipal test: the municipality-by-municipality transitions already published (A31) reproduce exactly in this analysis (f 2026: 0.7360 vs 0.7367 versioned). The two readings are consistent; the national closure with ideological pools measures what the agnostic municipal test does not.

**Status:** **exploratory** analysis; pre-registration A39 proposed (implicit cross-over vs runoff vote-transfer polls of 2026); data and script in `results/exploratorio/FLX_*` and `scripts/exploratorio/10_fechamento_fluxo.py`.

<p class="destaque">A count that doesn't add up is proof of nothing: it could be the largest electoral wave of the series, and no test separates wave from operation with internal data. But it is the first time that closing the count requires believing in something that has never happened. What decides is not this dossier: it is runoff vote-transfer polling, voting sheets and printed receipts. Until they arrive, the question stays on record.</p>

## What we know and what we do not yet know

### Verified result

- **RDV, BU, BWeb and total chain:** 0 discrepancies in the tests run (14,067 polling station sections in 27 states with voting-machine files; BWeb against tabulation by section, municipality and electoral zone).
- **Summed measured excess:** about 99 thousand pro-Lula and 101 thousand pro-Flávio (margin votes), in opposite directions, against a margin of 4,430,191 votes.
- **Votes after 5 p.m.:** about 23 thousand (vote count, not margin votes).
- **Limit:** these tests compare files that the TSE itself publishes; they do not rule out a coherent alteration made before publication, nor do they verify that the recorded vote is the typed vote (see the questions below).

<p class="destaque">If an alteration happened in the links that are not published (the typed vote, the printed receipt, the transmission), <strong>no test in this dossier would see it</strong>. That is why the questions below remain open.</p>

## Open questions (summary)

There are **26 open questions**: residues without an identified cause, hypotheses not yet tested, and structural blind spots. The largest worst-case ceiling, not an estimate, is 40.35% of the margin (A20b). **They are not evidence of anything, on either side: they are gaps that only new data can close.**

Full list, with status, ceiling, and what would close each one: [Open questions](perguntas-em-aberto.html).


## Where a failure could go unnoticed

This section shows, with numbers, where public verification ends and how large a failure would need to be to change the outcome. Every value in votes is in margin votes (the change in the Lula-minus-Flávio difference; switching one vote changes the margin by 2).

### G1. Map of the vote chain

<picture><source media="(max-width: 640px)" srcset="img/en/g1_cadeia_m.svg"><img src="img/en/g1_cadeia.svg" alt="Map of the twelve-step vote chain, from voter registration to results publication. Each step has a status: verified by the tests, partially verified, or not verifiable with public data. The link between typed vote and recorded vote is highlighted as not verifiable, checked only by sampling in the integrity test."></picture>

**In plain words:** the vote passes through twelve steps; the tests cover the steps after recording; the earlier steps and those occurring outside the public files remain partially verified or unverified. **Technical:** per-step status derived from A4, H9, A5, A18, A19, A20, A26; the typed vote → recorded vote link is verified only by sampling (integrity test). How to close this gap: [printed poll-receipts](boletins-impressos.html) and [official signature key](a18-alteracao-no-meio.html#2).

### G2. Detection curves

<picture><source media="(max-width: 640px)" srcset="img/en/g2_deteccao_m.png"><img src="img/en/g2_deteccao.png" alt="Curves of the chance of detecting at least one altered voting machine or section as a function of the altered fraction, from 0.1% to 20% on a logarithmic scale. The integrity test covering all machines detects small fractions; using only machines with biometrics, a much larger fraction is needed. Printed poll-receipts with 100, 300 and 1,000 checked appear as additional curves. Vertical lines mark the fractions of sections needed to change the margin with 200 and 50 switches per section."></picture>

**In plain words:** the larger the altered share, the easier it is to see; printed poll-receipts and the integrity test detect small alterations that statistical tests do not. **Technical:** hypergeometric probability of seeing at least one altered voting machine; assumptions: random sample; in (b), software that behaves normally in the non-biometric test. It does not describe how an attack would be carried out. How to close this gap: [submit photos of poll-receipts](boletins-impressos.html), [LAI (access-to-information law) request 03](fase3.html#a28).

### G3. Size of the impact of the open items

<picture><source media="(max-width: 640px)" srcset="img/en/g3_impacto_m.png"><img src="img/en/g3_impacto.png" alt="Horizontal bars, in margin votes, for each open item that has a number: solid bar is measured excess, hatched bar is worst-case ceiling, not an estimate. A fixed vertical line marks the margin of 4,430,191 votes. Two panels: linear scale, where all bars are small next to the margin, and logarithmic scale, where small items become visible. Items without a number appear only in the legend as not measurable."></picture>

**In plain words:** each open item, drawn next to the margin; the largest worst-case ceiling is smaller than the margin, and several items have no number because data are missing. **Technical:** solid bar = measured excess (positive central estimate); hatched bar = worst-case ceiling (loosest placebo), in margin votes; there is no summation. How to close this gap: [LAI requests](fase3.html#a28) and [party observer list](fase3.html#a23).

### G4. How many sections would need to be altered

<picture><source media="(max-width: 640px)" srcset="img/en/g4_secoes_m.png"><img src="img/en/g4_secoes.png" alt="Curve of the number of sections needed to change the margin as a function of votes switched per section, from 1 to 300, on a logarithmic scale on both axes. With 5 switches per section it would take 443,020 sections; with 50, 44,302; with 200, 11,076. The range to the right of 13 switches per section marks where an altered section would already appear as an outlier locally; to the left, it only shows up in aggregate, in printed poll-receipts or in the integrity test."></picture>

**In plain words:** the fewer votes switched per section, the more sections would be needed, and the harder it is to see a single section. **Technical:** sections = ⌈2,215,096 / switches⌉; the 13-switches-per-section threshold = 3 standard deviations of the local residual (1.67 p.p.) with 256 valid votes. How to close this gap: [printed poll-receipts](boletins-impressos.html) and [comparison with other offices, A22](fase3.html#a22).

> **These charts show where public verification ends. They do not indicate that a failure occurred; they indicate where a failure would not be seen by the available data and what would be needed to see it.**

### What was not tested

See [Open issues](residuos.md), [Blind spots](pontos-cegos.md), [Phase 3](fase3.md) and the **NOT RUN** list: cross-check against printed poll-receipts (0 checked; no input data), the voting machine's cryptographic signature (certificate read, signature 0% verified), the release curve of the Resultados website, the 2026 runoff turnout profile, 2014 in the counting curve, the "472 machines" from the video, and Phase 3 tests A21 (partial), A22, A23, A24 and A25 (partial).


## How to contribute

- **Photos of printed poll-receipts:** [collection page](boletins-impressos.html). Checked as of Oct 29, 2026: 0.
- **Lists of sections with a party observer** (parties and coalitions): format in [A23](fase3.html#a23).
- **Responses to LAI requests:** ready-made texts in [`lai/`](https://github.com/baduba/eleicoes-dossie-2026/tree/main/lai); send the response via an issue.
- **Alternative code or method:** open an issue or a PR with a reproducible script.
- **Challenging any number:** open an issue with the script and the expected value.


## What was done
Statistical analysis of official TSE data by section (BWeb for 2014, 2018, 2022 and 2026, with verified hash), plus the voting-machine files (BU, RDV, signature and log) from a sample of 14,067 sections of the 2026 runoff and the same sections in 2022 as placebo. Predictions were recorded before each analysis block ([Pre-registration](preregistro.md)); every test has a placebo and is symmetric; null results receive the same prominence as positive ones.

## Summary of results (numbers without adjectives)
- **Totals and consistency:** Lula 64,256,232, Flávio 59,826,041, margin 4,430,191. BWeb matches `votacao_secao` and the zone-level tabulation in 2026.
- **Voting-machine chain (A4):** in 14,067 sections across 27 states, the digital BU matches BWeb, the recounted RDV matches the BU, and the hashes of BU, RDV, image and log appear in the list signed by the machine: 0 discrepancies. **This verifies consistency among files that the TSE publishes and does not rule out a coherent alteration made before publication** ([A18](a18-alteracao-no-meio.md)). The cryptographic signature itself **was not verified** (0% of sections; PARTIAL NOT RUN: the accessible official key is missing).
- **Mid-chain alteration and typed vote vs. recorded vote (A18, A19):** the documented delays (1 hour in the first round; receipt withheld until 7 p.m. in the runoff) were tested through the clock window against placebos, with no excess detected, but these tests do not rule out a coherent alteration. The correspondence between typed vote and recorded vote is verified only by sampling in the integrity test, and the current model has no voter-verified record ([A19](a19-voto-digitado.md)). Photos of printed poll-receipts can be submitted by anyone ([how to submit](boletins-impressos.md)).
- **Original report:** the closing table (339,593 sections between 5:01 p.m. and 5:15 p.m.), the 8.6 million manual voter releases (8,632,488) and the Bahia percentages reproduce; the conclusions do not hold ([page](relatorio-original.md)).
- **Votes after 5 p.m. (A5):** estimate from the logs of 23,094 votes (count, not margin votes) nationwide (95% CI 16,895 to 29,704), 0.52% of the 4,430,191 margin (direct comparison of the count with the margin); many of the sections that closed late remained open without recording any vote after 5 p.m.
- **Manual voter release:** fell 14% from 2022 to 2026; the association with the Lula vote exists in both rounds of 2026 and is not specific to the runoff.
- **Counting curve, conversion and zero-vote (A1, A2, A3, A11, A12, A13, A14):** the real curve and its linear stretches fall within the range of simulated geographic orderings; no conversion from the opponent to the PT is needed to explain the national result; the "109 sections with zero votes" claim does not reproduce (there are 106 in the runoff; 143 in 2022, 328 in 2018); by 7:34 p.m. only 7.8% of BUs had been received, not 70%.
- **Lines with a design caveat (A1, A2, A3, A12):** under the pre-registered criteria, they came out labeled as excess, but **the same test flags excess in series or years without manipulation** (A1: 20 of 20 clean simulations; A2: the 2022 PT; A3: negative coefficients in every year; A12: 44% of clean simulations). The corrected versions show no excess. Original and corrected results, side by side, in [Phase 2 Results](resultados-fase2.md) and [Open issues](residuos.md).
- **Measured excess, all residues summed** (margin votes): **about 99,499 pro-Lula and 101,285 pro-Flávio**, 2.2% and 2.3% of the 4,430,191 margin, in opposite directions ([sum and reading](residuos.md)).
- **Aggregate impact** (only tests without design caveats; unit: margin votes; worst-case ceiling, not an estimate): 38,394 margin votes pro-Lula and 122,543 pro-Flávio, worst-case ceilings; with the corrected versions in place of the originals, the result is the same (none of the four corrected versions shows excess). The margin is 4,430,191.
## Authorship
Project with no named authorship, maintained by the baduba account on GitHub. Contact, corrections and challenges via *issue* at https://github.com/baduba/eleicoes-dossie-2026/issues.
