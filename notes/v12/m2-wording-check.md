# Archived M2 observed-median wording check for F4.4

Checked 2026-10-25T11:50:00.242563+00:00. Scope: saved v10 menu summary/operands and current TeX/Bib/letter occurrences. This note is the only file written. No financial fit, evaluation, simulation, fresh aggregation, paired-difference calculation or population test was run. F1 running code and outputs were not read or changed.

The saved M2 switching-minus-constant increment is **-0.43471629487539243 percentage points**, displayed as **-0.43 pp**. It is the difference between the two across-source arm medians for expanded-menu full regression QR33 at history 52. It is not the median of source-paired changes, a repetition-level median of differences, a percent change, an effect estimate with a confidence interval, or evidence of population equivalence.

## Exact saved source and operands

Primary artifact: `results/v10/menu/summary.json`, bytes 105699, SHA-256 `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5`.

| JSON pointer in primary artifact | Saved value | Meaning |
|---|---|---|
| `/predictions/M2/switching_minus_constant_pct_points` | `-0.43471629487539243` | Already saved observed contrast; no subtraction was recomputed for this check |
| `/predictions/M2/constant_median_pct` | `0.2069371499562489` | Expanded-menu constant-arm median excess loss, percent relative to F |
| `/predictions/M2/switching_median_pct` | `-0.22777914491914353` | Expanded-menu switching-arm median excess loss, percent relative to F |
| `/predictions/M2/minimum_inclusive_percentage_points` | `5.0` | Declared M2 increase threshold |
| `/predictions/M2/status` | `NOT_SUPPORTED` | Saved threshold decision, not a population non-effect result |
| `/across_sources/0/arm` | `constant` | Group identity for the first operand |
| `/across_sources/0/window` | `52` | History52 |
| `/across_sources/0/method` | `QR33` | Full regression |
| `/across_sources/0/median_pct` | `0.2069371499562489` | Same saved constant operand |
| `/across_sources/0/status` | `COMPLETE` | All-source aggregate available |
| `/across_sources/0/required_sources` and `/across_sources/0/complete_sources` | `13`, `13` | All declared sources present |
| `/across_sources/4/arm` | `switching` | Group identity for the second operand |
| `/across_sources/4/window` and `/across_sources/4/method` | `52`, `QR33` | Matching history/method |
| `/across_sources/4/median_pct` | `-0.22777914491914353` | Same saved switching operand |
| `/across_sources/4/status` | `COMPLETE` | All-source aggregate available |
| `/across_sources/4/required_sources` and `/across_sources/4/complete_sources` | `13`, `13` | All declared sources present |

Independent saved report/readback: `results/v10/menu/report-values.json`, bytes 22341, SHA-256 `3bfd9b354f411ca66967e972b9a9d95634a4360860d32cc0582344c60579ba43`.

- `/predictions/M2` contains exactly the same saved decision, operands and increment as summary.json; equality was checked without deriving a new statistic.
- `/registered_conditions/M2/window` is 52, `/registered_conditions/M2/method` is QR33, and `/registered_conditions/M2/difference` is the exact stored definition `switching across13 median minus constant across13 median`.
- `/rows/0/expanded/median_pct` and `/rows/4/expanded/median_pct` repeat the two arm medians.
- `/source_count` is 13 and `/formal/repetitions` is 32. The primary manuscript table already explains each source median uses all 32 matched repetitions; the displayed across-source medians are therefore summaries of source medians, not 416 independent observations.
- `/input_receipts/summary.json/sha256` equals the directly verified primary artifact SHA above.
- `/interpretation_boundary` explicitly identifies IQR as descriptive rather than an independent-source confidence interval, and excludes successful-only medians.

The saved precision supports rounded +0.21% constant, -0.23% switching, and a saved switching-minus-constant contrast of -0.43 **percentage points**. Do not infer the precise contrast by subtracting already rounded display entries.

## Recommended readable replacements

For the abstract, introduction highlights, conclusion and letter, replace the vague clause “the registered switching increment is unsupported” with an observed-value statement tied to this simulation setting:

> With the expanded menu at history 52, the switching arm's observed median excess loss was 0.43 percentage points lower than the constant arm's.

A fuller main-results version, preserving the exact estimand, is:

> At history 52, the expanded-menu full regression's observed median excess loss was -0.23% in the switching arm and +0.21% in the constant arm. The switching-minus-constant difference was -0.43 percentage points, below the predeclared increase of at least 5 percentage points.

Follow the detailed result with the boundary:

> This descriptive contrast between the arm-level medians across the thirteen calibrated sources does not establish population equivalence or identify the empirical frequency mechanism.

TeX-ready form for the detailed numerical clause:

```tex
At history 52, the expanded-menu full regression's observed median excess
loss was $-0.23\%$ in the switching arm and $+0.21\%$ in the constant arm.
The switching-minus-constant difference was $-0.43$ percentage points,
below the predeclared increase of at least five percentage points.
```

This wording preserves the saved M2 decision while making the observed contrast understandable. Keep the explicit population-equivalence boundary already present near manuscript line 292, or revise it to the clearer sentence above. Do not replace it with “switching has no effect”, “the arms are equivalent”, “there is no switching penalty”, or “the difference is statistically insignificant”: the archived scalar threshold screen does not supply those conclusions.

## Current occurrence locations; no source edits made

Locations are the current source snapshot at check time. Later F4 edits may move line numbers.

| Current source | Matching line(s) |
|---|---|
| `submission-v10/manuscript.tex` | 17, 45, 80, 284, 292, 347 |
| `submission-v10/supplement.tex` | 1494 |
| `submission-v10/cover-letter.tex` | 12 |
| `submission-v10/references.bib` | No M2/switching-increment occurrence |
| `manuscript/supervisor-revision/abstract.tex` | No M2/switching-increment occurrence |
| `manuscript/supervisor-revision/sections.tex` | No M2/switching-increment occurrence |
| `manuscript/supervisor-revision/appendices.tex` | No M2/switching-increment occurrence |
| `manuscript/supervisor-revision/references.tex` | No M2/switching-increment occurrence |

Specific edit routing:

- `submission-v10/manuscript.tex:17`: abstract; vague unsupported-increment clause.
- `submission-v10/manuscript.tex:45`: second-contribution paragraph; same vague clause.
- `submission-v10/manuscript.tex:80`: contribution/interpretation paragraph; “leave the registered switching increment unsupported” variant.
- `submission-v10/manuscript.tex:284`: main menu-result discussion; currently says the switching-minus-constant difference misses the five-point increase. This is the best place for the full observed medians and -0.43 pp contrast.
- `submission-v10/manuscript.tex:292`: existing “Absence of a five-point switching increment is not evidence of equivalence” boundary. Preserve the boundary, with optional clearer population wording.
- `submission-v10/manuscript.tex:347`: conclusion; vague unsupported-increment clause.
- `submission-v10/cover-letter.tex:12`: letter summary; same vague clause. Use the concise observed-median sentence.
- `submission-v10/supplement.tex:1494`: M2 criterion and “M2 fails” explanation; add or substitute the saved-operand contrast while retaining the declared threshold and history-260 failure restriction.

`submission-v10/references.bib` and the current supervisor-revision inline bibliography contain no M2/switching-increment wording. No bibliographic edit or new citation is needed to report an archived result of the present study. The supervisor-revision abstract/sections/appendices likewise contain none of the targeted M2 wording; the current submission sources above own the occurrences.

A related author checklist, `submission-v10/AUTHOR-TODO.md:33`, says the paired menu extension “misses the registered switching increment”. It is an ancillary synchronization location if the F4 pass updates that checklist; it is not the manuscript or bibliography.
