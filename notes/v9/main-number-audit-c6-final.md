# C6 final current-native numerical audit

**PASS_NATIVE_NUMBER_BINDINGS_WITH_RETAINED_PRECISION_NOTE**

- Main SHA256: `83c611692ecba07dd155d9792aa71870f9f9040f88cc9143c7ea639dd9278993`
- Supplement SHA256: `65b8ca7cb427c225a33d9ca2f52dcfecc62fcf22e5958065000455705ee14c22`
- Current tablebinding receipt SHA256: `c8b46442b414da8df05d3d014d066576bb1f8addbd19d67d476485f46bcee93c`

This final report inherits the already verified located C0/C3/C4 source bindings and revalidates current source identities and actual native table rows. It does not substitute global number membership or token counts for source mapping, and it does not rerun a study.

## Audit chain

- C0: `notes/v9/real-number-reconciliation.json`; SHA256 `1436b7058257913c96830e3cd171fdae7618e06681ff873b890dddeeb24fcfbc`
- C3_initial: `notes/v9/main-number-audit.json`; SHA256 `f857b958fd58d7845c368602e709292631a2224c745674a14cc2903b417a8fb3`
- C3_final: `notes/v9/main-number-audit-c3-final.json`; SHA256 `6e380aed9a700b20acdb08906ca423467f51dd27a84df83260a8127d1c6c1f0f`
- C4: `notes/v9/main-number-audit-c4.json`; SHA256 `ae416924f822197b62c41abcbce8d7c8e8ae33d2774a9b39f7d981b93e71c119`
- C5: `notes/v9/c5-document-check.json`; SHA256 `8e68b0b12fc1910d37772e06817d689258a804b0a28a5ef3201b741a7127c3af`

## C5 numbers remain unchanged from C4

Base commit: `e6a3c98b48f22f4ba4e2236c48444ef915af3661`; base main SHA256 `4d138febc2d3e9ee3176150eddce81a9a1405e3dac645ba16aca06fc08bd2431`.

Exact regex: `(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*`; direct readtext/gitshow text, no preprocessing. Both sources yield593tokens and their ordered lists are identical. Independent wider rules yield614and622tokens respectively and also agree in order. These counts include formatting/reference/identifier numerals under the stated tokenization;they are not empirical-estimate counts.

Only lines290,302,313,319 changed fromC4:benchmark phrasing is narrowed,and measurement/validation limitations are made explicit. None introduces a new numerical claim. Existing source-bound values andcomparators retain their contexts.

## Current native bindings

- 36 distinct files underlying the prior located main/figure/proof audits retain their expected SHA256 values.
- All27 owning sources underlying the2125 inherited supplementary bindings retain the C0 source identities.
- The five new tablefiles still match the C4 output hashes and are included exactly once in the current supplement.
- All150 native row objects were reread from current owning JSON pointers orunique CSV rows and compared with the existing locator ledger andcurrent binding receipt.
- All1269 actualTeXdisplay cells were reread and match the previously verified formats andreceipt. No tablegenerator orscientific code was run.

| Row group | Live rows |
|---|---:|
| legacy | 24 |
| legacy-failures | 7 |
| diagnostics | 15 |
| W52 | 26 |
| W260 | 26 |
| F | 52 |

## Three preserved finite-precision differences

| Source/method/arm/history | Original summary q25 | Independent report q25 | Difference | Same table display |
|---|---:|---:|---:|---|
| PDPOSTIPS-G11 / constant / 52 / QR4 | -4.21741795487213 | -4.217417954872129 | 8.8817841970012523e-16 | -4.2 |
| PDPOSTIPS-G11 / switching / 52 / QR4 | -4.21741795487213 | -4.217417954872129 | 8.8817841970012523e-16 | -4.2 |
| PDPOSTIPS-G6L11 / constant / 260 / QR33 | -3.7144837154752195 | -3.71448371547522 | -4.4408920985006262e-16 | -3.7 |

Maximum absolute difference is8.881784197001252e-16. The tableowner is the separately archived analysisreport and all tablebindings equal it exactly. No affected one-decimal display,median,status,predicate orconclusion changes. The originalsummary andindependentreport rawvalues are not described as bit-identical. No originalarchive was modified.

## Result and boundary

Within the audited numerical/source scope: **0 unmapped claims/rows and0 native binding/display mismatches**. The three original-summary-versus-report precision differences remain explicitly recorded. This is artifact/source consistency,not a newforecast result orindependent scientific replication. FullpagevisualQA,packagepublication andremote equality remain separate C7/C6 checks.

JSON report SHA256: `c787616f6c72f049f06f7100063916583326d00f0ef79d81cdfc962dc8146465`
