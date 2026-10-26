# Verification loop 13: five randomly selected abstract numeric claims

**Status: PASS for existing-output transcription, identity, direction and formatting. No conclusion-changing problem identified.**

Recorded verification time: 2026-10-23T21:39:20.908675+00:00.
Audited source commit: `d1888c0a89fafbe3f36e194ff5a467ef9a3f6902`.
Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.

## Scope and reproducible selection

This is verification of the current main abstract against already frozen script outputs and static generation code. It is not independent replication or new evidence of forecast performance. No analysis, fitted model, test, diagnostic, compilation, PDF rendering, UI operation, state edit, source/result/manuscript edit or commit was performed. The only new files written for this round are this note and its same-prefix selection JSON. A delegated read-only check independently located the two ratio claims; it wrote no file.

Prior rounds were read before selecting: loop1 sampled main Table3 cells; loop5 sampled Table4 decomposition cells; loop9 sampled Table5 coverage p-values. This round samples abstract claims, not those table cells. The same underlying frozen output may legitimately support both a table and its abstract description.

The sampling frame has six empirical numeric claims in abstract order:

| Index | Semantic claim | Current display |
|---:|---|---|
| 0 | Original FX primary mean-loss reduction | 12.660% |
| 1 | Separate matched-history FX mean-loss reduction | 14.77% |
| 2 | Matched-history FX breach-count increase | 360 to 376 |
| 3 | Short-history FX QR horizon-report crossings | 640/6625 |
| 4 | Treasury primary mean-loss increase | 50.79% |
| 5 | Additional aggregate-panel QR33 lower-loss cells | 3/48 |

A paired count phrase or ratio is one semantic claim. The rhetorical phrase “Three findings” is not an empirical numeric-result claim. The actual deterministic selection was:

```python
random.Random(2026102313).sample(range(6), 5)
# [5, 4, 2, 3, 0]
```

This selects five claims without replacement and omits 14.77%, which had already appeared in the loop1 Table3 sample. The complete frame, ordering and selection are retained in `verification-loop-013-abstract-number-trace-selection.json`.

## Five exact traces

### 1. Additional aggregate panel: 3/48

Current abstract: “the additional aggregate panel yields only 3/48 lower-loss original-regression cells.”

Direct owning output: `results/revision-20261023/round2/panel/descriptive-counts.json`.

```text
/QR33/lower_loss_than_F = 3
/QR33/total_cells = 48
/QR33/complete = 48
```

The label “original-regression” maps to `QR33`, not `C2_QR4` or `Levy_L`. The claim means 3 lower-loss QR33 cells among 48 H/W cells of the additional aggregate panel. Each reference is frozen F from the **same series, horizon and window**. These are related aggregate tasks, not 48 independent trials.

The frozen authoring intermediary `notes/revision-v5-novelty/v4-supplement-before.json`, pointer `/sections/0/blocks/19`, is Table S9. In its QR33 column, `PDPOSFGS-TOT` contributes `1/4`, `PDPOSTIPS-G6L11` contributes `2/4`, and the ten other series contribute `0/4`. The original source pointer retained by that table is `manuscript/revision-v3/paper-content.json` → `/sections/7/blocks/19`.

`v5_submission.py:29` sums the existing table's numerator strings and denominator strings; this exact display arithmetic gives 3/48. It does not fit a model or calculate a new loss. `v5_submission.py:60` writes `wins[0]/cells` into the abstract, and `v6_submission.py:55` through line 62 preserves those numbers.

Additional exact output selectors are available in `results/revision-20261023/round2/panel/summary.csv`: `method=="QR33"` identifies the 48 complete rows. Its three existing negative `percent_vs_frozen_F` records are CSV lines 40, 104 and 112 (header is line 1), with these selectors:

| CSV line | series_key | horizon | window | Stored percent_vs_frozen_F |
|---:|---|---:|---:|---:|
| 40 | PDPOSFGS-TOT | 6 | 260 | -1.080927477978298 |
| 104 | PDPOSTIPS-G6L11 | 6 | 260 | -5.716797263767824 |
| 112 | PDPOSTIPS-G6L11 | 24 | 260 | -26.42400809091829 |

Static ownership: `round2_panel_run.py:20`–21 routes QR33 to the original QR forecast; lines 35–36 create same-cell frozen F; lines 49–51 define the saved signed percentage against that F. Lines 57–64 flatten the existing cell records to the summary CSV. `round2_panel_manuscript.py:8`–15 reads these outputs and forms each series' existing lower-loss count and cell count; line 24 reads the direct QR33 count fields. These scripts were read, not executed.

**Result: exact numerator, denominator, model identity, adverse-cell retention and reference identity agree.**

### 2. Adverse Treasury primary: loss raises by 50.79%

Current abstract: “The separately fitted Treasury regression primary raises loss by 50.79%.”

Direct output: `results/revision-20261022/paired-comparisons.csv`, unique selector:

```text
contrast_id = nyfed_weekly-h6-QR260-minus-frozen_F260
CSV line = 64
source = nyfed_weekly
horizon = 6
left_method = QR
left_window = 260
right_method = frozen_F
right_window = 260
declared_source_primary = True
relative_mean_loss_difference_percent = 50.78571256749063
```

The raw percentage is positive. `v5_submission.py:22`–23 formats `Decimal(str(x))` with two decimal places, and line 60 uses this Treasury field in the “raises loss” clause:

```python
f'{Decimal("50.78571256749063"):.2f}'  # "50.79"
```

This is **QR W260 versus frozen F W260**, both fitted separately for the Treasury source. The row is both a common-history comparison and the declared source primary. It is not a pooled FX/Treasury calculation. The higher-loss direction is retained explicitly; no sign reversal, favorable substitution or new loss calculation was made.

**Result: stored direction and exact two-decimal display agree.**

### 3. Matched-history FX: breaches increase from 360 to 376

Current abstract: “Its separately identified matched-history short-horizon regression ... increases breaches from 360 to 376.”

Direct output: `results/revision-20261022/paired-comparisons.csv`, unique selector:

```text
contrast_id = fx_hourly-h6-QR2880-minus-frozen_F2880
CSV line = 14
source = fx_hourly
horizon = 6
left_method = QR
left_window = 2880
right_method = frozen_F
right_window = 2880
declared_source_primary = False
strict_breach_count_right = 360
strict_breach_count_left = 376
```

`v5_submission.py:60` inserts the right-side F count first and left-side QR count second. Both are direct integer strings from the owning row; no rates, rounding, inference or subtraction is needed to display them.

This is the **matched-history** contrast against frozen F W2880. It must not be substituted for the distinct original FX primary against rolling F W720. Static `conditional_study.py:288`–289 names left and right strict-breach counts; `build_conditional_results.py:292`–307 binds source, horizon, left/right window/method and the common origins to each saved comparison row.

**Result: exact count order, count identity and “increases” direction agree.**

### 4. Short-history FX QR: 640/6625 horizon-report crossings

Current abstract: “Horizon-specific short-history FX regression reports cross on 640/6625 origins despite ordered realized targets.”

Direct output: `results/revision-20261022/post-result-horizon.csv`, unique selector:

```text
CSV line = 2
source = fx_hourly
window = 720
method = QR
short_horizon = 6
long_horizon = 24
strict_crossing_count = 640
origin_count = 6625
target_order_violation_count = 0
```

The display directly concatenates the stored integer numerator and denominator. The frozen intermediary `notes/revision-v5-novelty/v4-supplement-before.json`, pointer `/sections/4/blocks/1/rows/0`, is Table S15's row `["FX","720","QR","640","6625","9.660","18.742"]`. Its original source pointer is `manuscript/revision-v3/paper-content.json` → `/sections/13/blocks/1`. `v5_submission.py:28` selects this exact source/window/method row, and line 60 writes `cr[3]/cr[4]`.

The actual historical owning script is the frozen `results/revision-20261022/post-result-builder-v01.py`. Lines 46–55 define a strict crossing as stored `C(H6)>C(H24)`, with denominator `len(c6)`; lines 48–49 check realized target ordering. Lines 95–103 pair the same source/window/method and require identical origins/floors; lines 106–108 write the CSV. The audit `post-result-diagnostics-audit.json` records a builder hash and an exported CSV hash, both freshly matched in this round.

This is the **W720 across-horizon QR coherence diagnostic**, distinct from the preceding abstract claim's W2880 matched-history loss comparison. The count is not proof of calibration failure. The current `build_conditional_diagnostics.py` is a later version; it must not be represented as the unchanged historical executable. This trace cites the audit-bound frozen builder.

**Result: exact count, denominator, short-history setting, horizon pairing and target-order qualification agree.**

### 5. Original FX primary: mean loss lowers by 12.660%

Current abstract: “The original FX primary lowers mean loss by 12.660% on the previously inspected record.”

Direct output: `results/revision-20261022/paired-comparisons.csv`, unique selector:

```text
contrast_id = fx_hourly-h6-QR2880-minus-rolling_F720
CSV line = 50
source = fx_hourly
horizon = 6
left_method = QR
left_window = 2880
right_method = rolling_F
right_window = 720
declared_source_primary = True
relative_mean_loss_difference_percent = -12.660126412969763
```

The archived signed loss percentage is negative. `v6_submission.py:57`–60 selects this exact original-primary row. Its formatter at line 21 takes the magnitude and prints three decimal places because the prose already says “lowers”:

```python
f'{abs(float("-12.660126412969763")):.3f}'  # "12.660"
```

This comparison has **unequal reference windows**: QR W2880 versus rolling F W720. It is not the matched-history contrast against frozen F W2880. The frozen `study-spec.json` primary_contrast metadata records the same identities. No re-estimation or recomputation of the mean-loss percentage was needed.

**Result: exact original-primary identity, negative direction and three-decimal magnitude agree.**

## Direction, ownership and provenance checks

The frozen paired-output convention is defined in `conditional_study.py:274`–289: the signed quantity is left minus right relative to the right-side mean loss. `build_conditional_results.py:292`–323 constructs the exact contrast IDs/metadata and writes the CSV. The current `conditional_study.py` hash matches the original `protocol/revision-20261022/executable-freeze.json`; its hash and that of the aggregate builder also match the retained AR diagnostics executable-freeze inventory. These static checks establish the named convention; none of the scientific code was imported or executed.

The abstract's current JSON text equals the current TeX abstract after removing TeX percent escaping. All 12 current `_abstract_bindings` hashes freshly match their source files. All 20 fingerprinted files below freshly equal the exact audited source-commit blobs. The PDF was only fingerprinted in this round, not opened or rendered.

Literal verification summary:

```text
SEED 2026102313
SELECTED_INDICES [5, 4, 2, 3, 0]
FIVE_DISPLAY_AND_DIRECTION_CHECKS PASS
SOURCE_SELECTORS_UNIQUE true
FROZEN_TABLE_RATIO_STRINGS ["3/48", "640/6625"]
CURRENT_ABSTRACT_BINDINGS_MATCH 12
JSON_TEX_ABSTRACT_TEXT_IDENTICAL true
ALL_20_FINGERPRINTED_FILES_EQUAL_SOURCE_COMMIT_BLOBS true
CONCLUSION_CHANGING_ISSUE_FOUND false
```

## Exact current fingerprints

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2` |
| `submission-jof/manuscript.tex` | `6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72` |
| `submission-jof/manuscript-preview.pdf` | `9e4f54f02fe3ce1a1ff105a05b0cdf9805dbf149fd8053d0e23ccd02b530eece` |
| `v6_submission.py` | `6f96167d21ea915b7c71a0a2a80d9bab5d4beb96075e67d43ddf4db56c7f46f2` |
| `v5_submission.py` | `cd37ce62a266c86d0491ce3dd8b84f745e62c7f7de5f0014a15cfe0f0dd66252` |
| `v4_submission.py` | `11725bfe7c8922fb08ad8c6acb579bf53f890ab82967c52368c5f1f589022852` |
| `conditional_study.py` | `aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740` |
| `build_conditional_results.py` | `9f87c689dd20027e223a423f427380cba7179f78565c0cf4fc896274be1776ab` |
| `results/revision-20261022/paired-comparisons.csv` | `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9` |
| `results/revision-20261022/post-result-horizon.csv` | `59bc82949da1642daed554ed0fcc2f9d16f989773a988cb11ecbd297fa6a5a5a` |
| `results/revision-20261022/post-result-builder-v01.py` | `d491761af3c79a2cbda18589b07b516f44a73be9f06342cecded948042e60e1c` |
| `results/revision-20261022/post-result-diagnostics-audit.json` | `af898abaa70e9f047b252c9ed28fd86b896670731f9a366bf8a8f7331bd63606` |
| `results/revision-20261023/round2/panel/descriptive-counts.json` | `d4d3f1ebe5d6851f72f321d2a00c2c599f4903415f66580b1524a36e0b66b649` |
| `results/revision-20261023/round2/panel/summary.csv` | `34134445a00354dcce3dc43de4c2adada7f2ea5403212558f90ef3480ee810f9` |
| `results/revision-20261023/round2/panel/selection-manifest.json` | `c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858` |
| `round2_panel_run.py` | `e3c0575dc50e3c9dc51395a43b1bd7daf06972395a4aaf4552713967146d76e9` |
| `round2_panel_manuscript.py` | `bf765d3f35d0f20d600a3118d62b9e89452325a0a67a5bec089ac9a428b0d06f` |
| `notes/revision-v6/v5-manuscript-before.json` | `2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7` |
| `notes/revision-v5-novelty/v4-supplement-before.json` | `7c2d48db924aa6e8de73138462839268600ef301b8acbd2e084e9edf6b20fcc9` |
| `protocol/revision-20261022/study-spec.json` | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |

## Verification limits and disposition

The only arithmetic used in this round was formatting already stored percentages and reproducing the manuscript generator's sum of existing table count strings. No new loss, forecast, test statistic, empirical model, population assertion, independent validation or scientific conclusion was produced. The additional CSV row/count inspection is a readback of existing output, not a rerun from observations.

Every selected abstract number has an exact owning field and agrees with the frozen output at its stated display precision. The adverse Treasury percentage remains adverse. Original versus matched FX references, the W720 crossing setting, and the panel's same-cell F references remain distinct.

No author-pending conclusion-changing issue was found. No fix or source change is proposed by this verification. Source/document/state hashes were not rewritten, and no commit was made.
