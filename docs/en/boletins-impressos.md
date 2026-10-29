# Printed poll-receipts: how to submit photos

**Why.** The printed poll-receipt (boletim de urna, BU) is the only copy of a section's results that does **not** pass through the files the TSE publishes. Everything else (RDV, digital BU, BWeb, tallying) originates from the same voting machine software: if that software recorded something different from what was typed in, all of those files would agree with each other — and with the error. A photo of the receipt posted at the section is the **only independent verification** of that blind link. Comparing what is printed with BWeb rules out, for the sections checked, a coherent alteration made after the voting machine closed. No photos have been received so far; the direct test remains **NOT EXECUTED** ([A18](a18-alteracao-no-meio.md)).

**Who can submit.** Poll workers, voters, the press, and party observers from any party or coalition. By law, the chair of the receiving board is required to hand a copy of the receipt to parties and coalitions that request it within one hour of its issuance (Law 9,504/1997, art. 68, § 1, [full text at Planalto](https://www.planalto.gov.br/ccivil_03/leis/l9504compilado.htm)); the receipt is also posted at the section and may be photographed by anyone. You do not need to identify yourself publicly.

## What to photograph

1. The **entire receipt, head-on and legible**, without cropping the **header** (which contains the state, municipality, electoral zone, and section) or the vote lines at the bottom. If it does not all fit, one photo of the header and another of the vote lines is acceptable.
2. Or, instead of the full photo, the receipt's **QR Code**, sharp and free of glare.
3. Note the **state, municipality, zone, section, and round** (all shown on the receipt) and the photo's **source**: poll worker, voter, press, or party observer (and which party, if you wish to say). The source is recorded together with the photo.
4. No personal voter data. The receipt contains none; do not send photos of other documents.

## How to submit (step by step)

1. Open the form: [https://github.com/baduba/eleicoes-dossie-2026/issues/new?template=envio-bu.yml](https://github.com/baduba/eleicoes-dossie-2026/issues/new?template=envio-bu.yml).
2. The title already comes with the prefix "BU: "; complete it with state, zone, section, and round (e.g., "BU: SP-123-456-2").
3. Fill in state, municipality, zone, section, round, and source in the form fields.
4. **Drag the photo into the issue body's text box** — the form has no attachment field; the photo is attached to the comment. Check in the preview that it opens legibly.
5. If you prefer, transcribe the numbers in the format below (one line per receipt) in the form's dedicated field.
6. Submit. No verified account or identification beyond a GitHub account is required.

```
ano;turno;uf;cd_municipio;zona;secao;aptos;comparecimento;lula;oponente;brancos;nulos
```

## What happens to each batch

1. Each received batch is automatically checked against BWeb by `scripts/04_cruza_bu_impresso.py`, which reports **any** divergence, down to a single vote.
2. **Each divergence is published individually**, with the photo, the section, and the source, alongside what BWeb shows.
3. The **total checked with no divergence** is published with each batch, together with the statistical power below.
4. Illegible photos or those missing the section identification data are listed as discarded, with the reason.

## Status

| batches received | BUs checked | divergences | photo sources |
|---|---|---|---|
| 0 | 0 | 0 | n/a |

## Collection target: what each receipt total can see

Chance of catching **at least one** altered section, as a function of the total receipts checked and the fraction of altered sections nationwide (random sample; hypergeometric calculation from [G2](index.md#g2)):

| fraction of altered sections | 100 receipts | 300 receipts | 1,000 receipts |
|---|---|---|---|
| 0.1% (500 sections) | 10% | 26% | 63% |
| 1% (4,993 sections) | 64% | 95% | 100% |
| 2% (9,985 sections) | 86% | 100% | 100% |
| 5% (24,963 sections) | 99% | 100% | 100% |

For random samples of sections (volunteer photos are not random; see the caveat in [A18](a18-alteracao-no-meio.md)), how many receipts would be needed to detect, with 95% and 99% probability, at least one altered section:

| fracao_alterada | secoes_alteradas | n_para_95 | n_para_99 |
|---|---|---|---|
| 0.1% | 500 | 2,981 | 4,575 |
| 1% | 4,993 | 298 | 458 |
| 2% | 9,985 | 149 | 228 |
| 5% | 24,963 | 59 | 90 |
| 9% | 44,933 | 32 | 49 |
