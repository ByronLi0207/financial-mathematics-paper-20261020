# F2 independent saved-result check

Checked 2026-10-25T12:15:35.999768+00:00. Read-only scope: fixed protocol, public F2/F1 scalar receipts, and cache attempt/terminal metadata. No raw observations, trace vectors, fits, forecasts, rescoring, bootstrap or new financial statistic was used. This note was newly created; science code, results and manuscript were unchanged.

The saved F2 experiment is consistent with its fixed scientific inventory and failure policy. All 17 contracts passed the full input preflight with N877; eligible K stayed 17, no source was excluded, no resource trim occurred, and all 136 planned method cells remain. The public rows contain 132 COMPLETE and four FAILED entries. All 68 full-regression cells complete; the four failures belong to the separate four-feature sensitivity.

Validation52 stays 553..604 and validation156 stays 449..604, both inclusive. Every evaluation is 611..870 with 260 origins, H6 and d13. Each method/arm has all six declared validation candidates in order; completed candidates have the declared count. A COMPLETE selected method has exactly its sealed candidate evaluation with 260 origins. Failed selection cells have no substitute evaluation. Runtime receipts confirm the frozen full-regression W52/W260 waves precede four-feature W52/W260 waves; none timed out.

## Cache reuse and terminal failures

The F2 candidate inventory contains 408 validation references and 132 evaluation references with keys already present in F1. For each, stored status, mean and count agree with a matching F1 record. These are 540 references to 467 distinct cache keys; the underlying STARTED timestamps all precede F2's recorded start, and terminal identities equal their attempt identities. No private trace was reopened or rescored for this check. Identical selected evaluation reports are reused across the two validation arms, rather than refitted.

Two short-validation failures were already terminal F1 cache entries and remain failed in F2. The corresponding long-validation segments are different declared identities; each has its own failure receipt. Four reported failed cells therefore do not imply four unrelated failure mechanisms.

## Four retained failed method cells

All are four-feature regression with the weakest finite penalty failing validation. The saved method status/reason is FAILED/NONCONVERGENCE, with null selection and unavailable relative loss. No successful subset replaces any failed method cell.

| Contract | History | Validation length | Reason | Pointer in F2 rows.json |
|---|---:|---:|---|---|
| `042601` | 52 | 52 | `NONCONVERGENCE` | `/9` |
| `042601` | 52 | 156 | `NONCONVERGENCE` | `/11` |
| `240743` | 260 | 52 | `NONCONVERGENCE` | `/121` |
| `240743` | 260 | 156 | `NONCONVERGENCE` | `/123` |

Candidate pointers in `candidates.json` are `/63`, `/76`, `/845`, and `/858`. The two validation52 cached failures retain exactly the F1 key/status. Predicted four-feature validation comparisons remain UNDETERMINED for both histories, with planned denominator 17 and 16 usable pairs in each history; the saved 16-pair medians are explicitly descriptive.

## Interpretation and wording risks

The primary saved medians change 19.33471575756462 to 4.030683382999826 percent at history52 and 10.348281789464425 to 0.5250886760200655 percent at history260. Infinity counts change 4 to 10 of 17 and 4 to 5 of 17. Both declared full-regression screens are SUPPORTED. These values are at `/methods/QR33/by_window/{52,260}` in predictions.json, with fields `median_relative_loss_by_validation` and `known_infinity_count_by_validation`.

The V1 contrast is a difference between two across-contract medians, not the median of paired contract changes. The latter saved descriptive changes are -1.3632221880984783 and -4.328369835284372 percentage points; they must not be presented as the primary V1 estimand. The validation span extends backwards on the same inspected period, with the same final evaluation labels and clocks. These are retrospective procedure sensitivities, not a causal intervention, new holdout or independent replication. More infinity selections show how this menu behaves; they do not identify a general low-frequency mechanism. Retain the failed sensitivity slots and do not promote successful 16-contract subsets into full-population medians.

## Source seals

| Public scalar artifact | SHA-256 |
|---|---|
| `results/v12/validation-length/rows.json` | `5f2be6709ba16f3128d3e813b5c476ce935529159ba9e046db0d72f9ae9c10b2` |
| `results/v12/validation-length/candidates.json` | `003afde15d1024984ec3c3a656f017ef7c3265d056097067535662453d3a0ab4` |
| `results/v12/validation-length/predictions.json` | `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520` |
| `results/v12/validation-length/input-preflight.json` | `1b9f8501c9cb5c2ccada51b3010b513b8427e9a75904e0bf5bb58a59cc9b12a7` |
| `results/v12/validation-length/resource-plan.json` | `06b943c2a00938215af5149969faf2e7945d897d0d15feec8a90ca582043ee24` |
| `results/v12/validation-length/runtime.json` | `8cd46e1815685e668f214167adc08cde3b98e024d687f4592e113aa3179b896e` |
| `results/v12/validation-length/code-seal.json` | `638e8518e1a88c75f38ff1255789e58eccb0e3e7cc54aa9b2709a03ec9ffb919` |
