# Verification loop 025: five seeded predictive-accuracy prose claims

**Status: PASS for the five selected traces. Necessary conclusion-changing issue / author pending: none identified.**

Initial Section6 frame read: 2026-10-23T22:12:56.653964+00:00.
Selection frozen before output lookup: 2026-10-23T22:14:17.755105+00:00.
Field/display verification observed: 2026-10-23T22:16:35.366426+00:00.
Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Observed source commit: `1c0c1d1b2e5c9b55a3236d1f45b1537accb910d5`.

## Current document and sampling scope

The sampling frame was built from current `submission-jof/manuscript-content.json` → `/sections/5`, headed **6. Predictive accuracy (RQ1)**, all 15 blocks in order. The corresponding section occupies TeX lines207–263. Table3/Table4 cells were excluded. The directly repeated bridge prose in block3 was excluded to avoid the already-sampled Table4 scope; repeated numeric statements were represented only at their first eligible occurrence, with the previously sampled Table3 QR Holm cell omitted. Navigation-only prose and the figure-reference block are not numerical-prose sampling units.

The retained frame has **50** unique semantic numerical statements. A before/after metric comparison with its counts/rates, or native/percentage forms of the same difference, stays together. Different horizon/control comparisons remain distinct. The full frame and explicit exclusions were saved before lookup in `verification-loop-025-accuracy-numbers-selection.json` (10,049 bytes; SHA-256 `4ff224d778ab69c143b502277c75849660ae5f194e5ebea493dae80ba09ab1c3`).

```python
random.Random(2026102325).sample(range(50), 5)
# [21, 34, 48, 40, 25]
```

There was no replacement draw or result-based selection. The five selected claims are:

| Index | JSON block / TeX line | Current claim |
|---:|---|---|
| 21 | 6 / 243 | FX H24 legacy-reference improvement of 33.007% in partial2017 |
| 34 | 9 / 249 | Treasury short-history H24 QR breaches132 of277 responses |
| 48 | 14 / 262 | Short-history FX QR DM p=0.538 |
| 40 | 10 / 251 | Treasury H24 KNN W260 all-origin loss reduction of8.964% |
| 25 | 6 / 243 | FX H24 legacy-reference fixed-grid loss change of−8.027% |

Canonical Section6 identity (UTF-8 JSON, ensure_ascii=False, sorted keys, compact separators):
`dbcc570fcefea80953d7b2cd09b71da45d1efcbb6cba0cdf9f5ea78fed6a0a9b`.

The current main JSON, TeX, PDF and generator hashes below were measured directly. In particular the actual PDF is `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`, and current main JSON is `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`. At the verification observation, all16 fingerprinted files matched the exact observed commit. The PDF was fingerprinted only; it was not opened, rendered or visually certified.

## 1. Partial2017 FX H24 improvement:33.007%

Direct output: `results/revision-20261022/paired-annual.csv`, CSV line101 (header=line1), unique selector:

```text
contrast_id = fx_hourly-h24-QR2880-minus-rolling_S720
calendar_year = 2017
```

Relevant original fields:

```text
source = fx_hourly
horizon = 24
left_method = QR
left_window = 2880
right_method = rolling_S
right_window = 720
contrast_category = h24_legacy_contrast
declared_source_primary = False
origin_count = 363
first_source_index = 18189
last_source_index = 18551
relative_mean_loss_difference_percent = -33.00749704770835
```

Display-only magnitude formatting:

```text
format(abs(float("-33.00749704770835")), ".3f") = 33.007
```

The negative signed loss difference agrees with the word “improves.” This is **QR W2880 versus original rolling S W720**, a legacy H24 sensitivity with unequal windows. It is not the original H6 FX primary against rolling F or a matched frozen-F comparison.

The inherited prose route is `manuscript/working-paper/paper-content.json` → `/sections/5/blocks/4`; the current source-bound paragraph preserves this number and the partial-year qualification. The static owner `conditional_study.py:291`–292 groups by the **issue dates** supplied by `build_conditional_results.py:300`; it is not grouping by target-end date. The existing row has363 origins and remains the partial2017 tail described in the manuscript. No new source-calendar reconstruction was performed.

This claim is an annual relative loss change, **not** the percentage of total score reduction contributed by that period. No annual percentages or full-sample means were averaged/recomputed. The paragraph retains the same-inspected-record and no-retrospective-switching qualifications.

**Result: PASS.**

## 2. Treasury H24 short-history QR:132/277 strict breaches

Direct output: `results/revision-20261022/evaluation-summary.csv`, CSV line20, unique selector:

```text
source = nyfed_weekly
horizon = 24
window = 52
method = QR
```

Relevant original fields:

```text
native_unit = USD millions
parameter = 0.001
refit_step = 13
origin_count = 277
strict_breach_count = 132
```

The manuscript copies the two integer fields directly as “132 of277 responses.” No rate calculation, statistical test or interval estimate is required to display the selected claim.

The exact inherited paragraph route is `manuscript/revision-v3/paper-content.json` → `/sections/6/blocks/2`. It describes **Treasury QR W52 at H24**, not W260 or the H6 declared primary. The adverse interpretation remains in the present prose. This is an all-origin count and must not be substituted for a sparse-grid hit denominator.

**Result: PASS.**

## 3. Short-history FX QR DM p-value:0.538

The current static manuscript generator uses `v5_submission.py:63`–65. Its `qs` is selected from the saved **Holm table**, and the displayed DM component is its `dm_p` field, not its adjusted `holm_p` field:

```text
File = results/revision-20261023/inference/holm.csv
CSV line = 2
contrast_id = fx_hourly-h6-QR720-minus-frozen_F720
dm_p = 0.5379650233773263
holm_p = 1.0
n = 6625
```

The same exact `dm_p` token is also present in `results/revision-20261023/inference/dm.csv`, line2, for that contrast. That is a cross-file identity check of retained fields, not a fresh inference computation.

```text
format(float("0.5379650233773263"), ".3g") = 0.538
```

This is **H6 QR W720 versus matched frozen F W720** on6625 original forecast origins. It is distinct from the original FX primary QR W2880 versus rolling F W720. The source-bound generator explicitly says post-result, working-reference, same inspected sample and not selection-adjusted confirmation.

The exact field matters because the saved HLN p-value is a different quantity even though a coarse three-digit display may look similar. This check uses the generator's DM component and does not recalculate DM, HLN, bandwidth or multiplicity adjustment, or infer equivalence/calibration from a large p-value.

**Result: PASS.**

## 4. Secondary Treasury H24 KNN W260 all-origin reduction:8.964%

Direct output: `results/revision-20261022/paired-comparisons.csv`, CSV line91, unique selector:

```text
contrast_id = nyfed_weekly-h24-KNN260-minus-frozen_F260
```

Relevant original fields:

```text
source = nyfed_weekly
native_unit = USD millions
horizon = 24
left_method = KNN
left_window = 260
right_method = frozen_F
right_window = 260
contrast_category = common_history
declared_source_primary = False
origin_count = 277
relative_mean_loss_difference_percent = -8.964334715557507
```

Display-only magnitude formatting:

```text
format(abs(float("-8.964334715557507")), ".3f") = 8.964
```

The negative saved percentage supports the prose “loss reduction.” This is **plain KNN**, a secondary comparison against same-window frozen F on all277 origins. It does not replace the adverse declared Treasury QR primary.

The inherited prose is retained in `manuscript/revision-v3/paper-content.json` → `/sections/6/blocks/3`; the current text explicitly says “secondary all-origin.” The following current paragraph still records its sparse-grid reversal and dependence limitations. The all-origin reduction is not represented as uniform across sampling grids, independent validation or a deployed model-selection recommendation.

**Result: PASS.**

## 5. FX H24 fixed-grid legacy-reference change:−8.027%

Direct output: `results/revision-20261022/paired-nonoverlap.csv`, CSV line51, unique selector:

```text
contrast_id = fx_hourly-h24-QR2880-minus-rolling_S720
```

Relevant original fields:

```text
horizon = 24
left_method = QR
left_window = 2880
right_method = rolling_S
right_window = 720
contrast_category = h24_legacy_contrast
declared_source_primary = False
stride_records = 25
origin_count = 265
first_source_index = 11927
last_source_index = 18527
relative_mean_loss_difference_percent = -8.027306386874764
```

Display-only signed formatting:

```text
format(float("-8.027306386874764"), ".3f") = -8.027
# the manuscript uses the Unicode minus sign: −8.027%
```

The current prose's second H6/H24 legacy-reference entry is thus the H24 value. It is **not** the partial2017 annual value or the all-origin H24 score change.

The static grid owner `conditional_study.py:252`–255 fixes the first origin and stride `H+1`; lines293–295 attach that exact grid to a paired comparison. `build_conditional_results.py:292`–309 preserves its source/H/W/control identity and writes the nonoverlap comparison with the same metadata. At H24 the saved stride is25 and the count265. No origin vector was loaded, enumerated, shifted or resampled.

The inherited current prose route is the same working-paper paragraph as claim1. It preserves the warning that these sensitivities are decompositions of the same inspected record, not independent validation. Removing shared recorded label observations does not remove common training histories or possible time dependence.

**Result: PASS.**

## Display and generation boundary

For the newly generated significance paragraph, the exact live formatter and owning field are explicit in `v5_submission.py:63`–65. The other selected paragraphs are inherited source-bound prose; their original JSON pointers were read and their displayed precision was reproduced from the exact owning CSV field. This audit does not invent an unobserved historical authoring command or claim that those inherited sentences are regenerated numerically at every current build.

The paired-output convention is defined by static `conditional_study.py:274`–289: left-minus-right loss difference, relative to the named right/reference mean. The code and result-building routes were read, never executed. No loss, mean, rate, p-value, annual contribution, regression or forecast was recomputed. Display formatting and exact field/selector/hash comparisons are the only computations in this round.

All five selected statements agree at their displayed precision. Annual tail, full-origin, sparse-grid, original/legacy and matched-control meanings remain distinct. The current adverse Treasury statements and secondary/same-inspected-sample qualifications were retained; unselected claims are not assigned a new numeric-verification verdict.

## Actual current hashes

All16 files below freshly matched their bytes at the observed source commit. These hashes identify the current evidence and do not constitute independent financial replication.

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `v6_submission.py` | `9f4984fc802f8a2e1375760d78cbe59ae04aa814bb83114d6707b70ac01b61c8` |
| `v5_submission.py` | `cd37ce62a266c86d0491ce3dd8b84f745e62c7f7de5f0014a15cfe0f0dd66252` |
| `conditional_study.py` | `aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740` |
| `build_conditional_results.py` | `9f87c689dd20027e223a423f427380cba7179f78565c0cf4fc896274be1776ab` |
| `run_v3_inference.py` | `f54ff54dcbc8db5c7446f0fc885bce1d5408cb329d0545ba7021699f1301a527` |
| `results/revision-20261022/paired-annual.csv` | `5b0727af566cbfa935fba95c25cf2a7918dc073baa2daf8558d84984161bce40` |
| `results/revision-20261022/evaluation-summary.csv` | `2988f6239b02c0c5d4637df8ef0881de78a3d52a845c38b3c8e3726871d8be15` |
| `results/revision-20261023/inference/dm.csv` | `0e8aa499fab31a5928be0ccb9198d5f6ee2833a01410a17fc965985bb65f5e41` |
| `results/revision-20261023/inference/holm.csv` | `976affb08867b6e1c821f6ce5d9491a3b8087f427f0af9296763872863d2c8b3` |
| `results/revision-20261022/paired-comparisons.csv` | `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9` |
| `results/revision-20261022/paired-nonoverlap.csv` | `b050007b8ddffc5ba5865ccad90960740d94f55d7dd7a814e88665aa3d55677d` |
| `manuscript/working-paper/paper-content.json` | `6d06f8cb3fa429601967d7ab847da975f04d262b97e5091b4ec72d01faa2927f` |
| `manuscript/revision-v3/paper-content.json` | `3a35590321c752186ab6dbfb46d115b725cdad3528b0dae73cf2c209f555dcb7` |

## Action receipt and disposition

Only this new note and its already frozen same-prefix selection JSON were written. No new analysis, test suite, diagnostic, model, proof, simulation, raw-source/private-vector read, UI operation, source/state/document/result change, commit, publication or nested agent was performed. No original plot or PDF was rerendered. No Claude/Cloud or cross-model review was invoked.

**Author pending: none identified by the five selected traces.** This is correct-output/correct-format verification of current manuscript claims, not an independent rerun, a validity certificate for component inference, or a review of unselected table cells and the rest of the paper.

