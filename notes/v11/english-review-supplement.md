# Read-only English review of the supplement

Review snapshot UTC: 2026-10-25T05:25:14.039550+00:00. Exact requested source: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/supplement.tex`.
Source SHA-256: `993a3927e7ffbc97f40bfef27f5f9a55bfd5916ddf87058e0fe758958b9fe71e`. Main-article source SHA-256 used for cross-references: `d85a6a83209ce8b1c00b0c3d8c1b1ceee93f6a946792f2bd2168b776f3031a7e`. The supplement contains 1605 source lines and 35 numbered sections in this snapshot.

This review reads the full supplement source, the included generated captions/notes, and the main article’s supplement pointers. The middle source range (511–1256) received a second read by a delegated same-model agent. No Claude/cross-model review was used. Only this review note is written; manuscript sources, generated tables, numbers, formulae, scientific conclusions, status codes, Git state and old directories are untouched.

Recommended items address grammar, comparative constructions, spacing or a stale navigation cue. Optional items improve clarity or consistency; they are not new scientific claims and should not be used to expand the argument. Line numbers are snapshot locations, so identify passages by the exact Before text if the root makes concurrent editorial edits.

## High-value findings and S35 result

- S35 is present with label `sup:v11-history`, title *Additional saved evidence on history length*. Its table label `tab:v11-confirmation` resolves to Table S47 in the inspected existing PDF. Its adverse universal-ordering and non-testable/left-censoring language is retained; no numeric or scientific edit is requested.
- The main article’s existing manual Supplement section pointers match the current section map. Its manual Table S46 pointer is also correct in the existing PDF. Do not renumber it from a count of caption commands: uncaptioned longtables can advance LaTeX table counters.
- The current main history paragraph does not explicitly point to Section S35. This is a navigation opportunity, not a broken numbered reference. An optional exact added sentence is supplied below.
- S9 still says that complete frontier tables are below although S10 now links those tables externally; E09 replaces the stale directional word.

## Before → after suggestions

### E01. Recommended: missing preposition

Location: `submission-v10/supplement.tex` — line(s) 797

**Before**
```text
The finite delayed ACI-style wrapper adapts past strict hits after their entire peak labels mature.
```

**After**
```text
The finite delayed ACI-style wrapper adapts to past strict hits after their entire peak labels mature.
```

Adapt to is the intended construction: the wrapper responds to past hits rather than modifying the hits themselves. The feedback maturity condition is unchanged.

### E02. Recommended: compare like quantities

Location: `submission-v10/supplement.tex` — line(s) 910

**Before**
```text
Combining floor-respecting reports preserves the floor, but does not guarantee a conditional quantile or a score below the best constituent.
```

**After**
```text
Combining floor-respecting reports preserves the floor, but does not guarantee a conditional quantile or a score below that of the best constituent.
```

A score is compared with the score of a constituent, not with the constituent itself. The absence of a guarantee is retained.

### E03. Recommended: comparative verb

Location: `submission-v10/supplement.tex` — line(s) 919

**Before**
```text
A report combination can improve one constituent while losing to the other.
```

**After**
```text
A report combination can outperform one constituent while losing to the other.
```

Improve a constituent means alter that constituent; outperform expresses the existing comparison between fixed reports.

### E04. Recommended: plural for two defined losses

Location: `submission-v10/supplement.tex` — line(s) 1288

**Before**
```text
be regression and matched-historical mean loss in repetition
```

**After**
```text
be regression and matched-historical mean losses in repetition
```

The two quantities A_j and B_j denote two mean losses. Only the noun number changes; the formula and estimand do not.

### E05. Recommended: missing of

Location: `submission-v10/supplement.tex` — line(s) 1306

**Before**
```text
and a strict-win fraction at least \(0.75\).
```

**After**
```text
and a strict-win fraction of at least \(0.75\).
```

Of at least completes the noun phrase while leaving the frozen threshold unchanged.

### E06. Recommended: parallel construction

Location: `submission-v10/supplement.tex` — line(s) 1517

**Before**
```text
Missing weeks, duplicates and changes disqualify rather than interpolate or splice a contract.
```

**After**
```text
Missing weeks, duplicates and changes disqualify a contract rather than trigger interpolation or splicing.
```

The original subject cannot interpolate or splice a contract. The revision states the existing rejection rule with parallel consequences and adds no eligibility condition.

### E07. Recommended: standard symmetry wording

Location: `submission-v10/supplement.tex` — line(s) 131

**Before**
```text
Conditional independence and zero symmetry cannot be inferred from unconditional marginals.
```

**After**
```text
Conditional independence and symmetry about zero cannot be inferred from unconditional marginals.
```

Symmetry about zero matches the explicit premise in Proposition 2. No mathematical assumption is added or relaxed.

### E08. Recommended: complete English sentence

Location: `submission-v10/supplement.tex` — line(s) 245

**Before**
```text
This is not demonstrated population failure.
```

**After**
```text
This does not demonstrate a population failure.
```

The revised sentence states the same non-demonstration without the missing article and awkward passive noun phrase. It does not say that failure is impossible.

### E09. Recommended: stale directional reference

Location: `submission-v10/supplement.tex` — line(s) 504

**Before**
```text
The complete frontiers below include every open region and every boundary tie.
```

**After**
```text
The linked complete frontiers include every open region and every boundary tie.
```

The complete frontier tables are now linked to the archive/v9 supplement in S10, rather than reproduced immediately below this S9 sentence. This is a navigation correction, not a change to frontier results.

### E10. Optional clarity: retain all three failed criteria

Location: `submission-v10/supplement.tex` — line(s) 750

**Before**
```text
All recorded success criteria are NOT\_MET, NOT\_MET and NOT\_MET, respectively.
```

**After**
```text
All three recorded success criteria are marked NOT\_MET.
```

The three repeated identical statuses lack an explicit ordered antecedent in this sentence. The revision retains the number of criteria and the adverse status; do not remove the underlying criterion records.

### E11. Optional clarity: awkward modifiers

Location: `submission-v10/supplement.tex` — line(s) 760

**Before**
```text
The complete noncomplete report inventory is below.
```

**After**
```text
The complete inventory of non-complete reports is below.
```

Separates complete inventory from non-complete reports. It does not equate every non-complete condition with a failed status or change any machine status code.

### E12. Optional consistency: adjective spelling

Location: `submission-v10/supplement.tex` — line(s) 769

**Before**
```text
All noncomplete fixed-rule report rows.
```

**After**
```text
All non-complete fixed-rule report rows.
```

Align with E11. FAILED, COMPLETE and REQUIRED_VALIDATION_CANDIDATE_FAILED remain literal identifiers and must not be edited.

### E13. Optional clarity: event rate versus probability

Location: `submission-v10/supplement.tex` — line(s) 862

**Before**
```text
A lower coverage distance measures closeness of empirical hits to the target probability, not conditional coverage or lower monetary loss.
```

**After**
```text
A lower coverage distance measures closeness of the empirical hit rate to the target probability, not conditional coverage or lower monetary loss.
```

A rate is the quantity compared with a probability; the distinction from conditional coverage and monetary loss is preserved. No coverage distance is recalculated.

### E14. Optional clarity: signed difference

Location: `submission-v10/supplement.tex` — line(s) 1033

**Before**
```text
The FX advantage remains negative in every group, while the weekly evidence remains adverse.
```

**After**
```text
The FX regression-minus-reference loss difference remains negative in every group, while the weekly evidence remains adverse.
```

Uses the existing table-header definition. Negative advantage can otherwise read as a disadvantage. Every sign and the adverse weekly conclusion are preserved.

### E15. Optional clarity: pronoun antecedent

Location: `submission-v10/supplement.tex` — line(s) 1215

**Before**
```text
The accepted solver records primal and dual residuals, objectives, feasibility and their gap.
```

**After**
```text
The accepted solver records primal and dual residuals, objectives, feasibility and the gap between the primal and dual objectives.
```

Their follows several nouns. The revision makes the existing objective-gap meaning explicit without changing a convergence criterion or certificate.

### E16. Optional clarity: rank product

Location: `submission-v10/supplement.tex` — line(s) 426

**Before**
```text
At integer probability-times-pool-size values, adjacent reports can be the two endpoints of the same empirical minimizer interval.
```

**After**
```text
When the product of the probability level and pool size is an integer, adjacent reports can be the two endpoints of the same empirical minimizer interval.
```

Replaces a compressed compound phrase with the same mathematical condition. The lower/upper empirical minimizer distinction is untouched.

### E17. Optional terminology: inspected record

Location: `submission-v10/supplement.tex` — line(s) 461

**Before**
```text
This ablation isolates a rank convention on the same viewed record;
```

**After**
```text
This ablation isolates a rank convention on the same inspected record;
```

Inspected matches the repeated period/inspection terminology in S26 and S35. It does not imply a new sample.

### E18. Optional grammar/clarity: state nouns

Location: `submission-v10/supplement.tex` — line(s) 1484

**Before**
```text
Level, innovation and variance state continue through each switch.
```

**After**
```text
The level, innovation and variance states continue through each switch.
```

Makes the parallel state nouns explicit. The continuation-through-switch claim remains unchanged.

### E19. Optional clarity: source identity article

Location: `submission-v10/supplement.tex` — line(s) 1359

**Before**
```text
Same recorded source identity is held fixed while physical history, horizon, update cadence, calendar predictors, sampled response and evaluation span change jointly.
```

**After**
```text
The recorded source identity is held fixed while physical history, horizon, update cadence, calendar predictors, sampled response and evaluation span change jointly.
```

Adds the definite article and removes an awkward Same at the start; every jointly changing quantity remains listed.

### E20. Optional clarity in generated caption

Location: `submission-v10/generated/v8-daily-results-table.tex` — line(s) 3

**Before**
```text
The isolated parsimonious score gain has more breaches than its historical reference.
```

**After**
```text
The parsimonious report yielding the isolated score gain has more breaches than its historical reference.
```

A report has breaches; a gain does not. The same isolated gain and adverse breach comparison remain. If accepted, make the corresponding editorial change in the owning display builder so regeneration preserves it; do not edit scientific source values.

### E21. Recommended typographic spacing in display prose

Location: `submission-v10/generated/v10-mcs-compact.tex` — line(s) 208, 210

**Before**
```text
Same-record dailyFX
```

**After**
```text
Same-record daily FX
```

Applies only to the natural-language heading and caption (two occurrences), not method IDs, source keys or paths.

### E22. Optional typographic spacing in display prose

Location: `submission-v10/generated/v10-mcs-compact.tex` — line(s) 68, 70

**Before**
```text
FX early2015
```

**After**
```text
FX early 2015
```

Applies only to the natural-language heading and caption (two occurrences); the displayed period remains 2015 and data identifiers remain unchanged.

### E23. Optional clarity in S35: antecedent and article

Location: `submission-v10/supplement.tex` — line(s) 1601

**Before**
```text
Local design commits precede the numerical runs; their later public file uploads are not public preregistration.
```

**After**
```text
The local design commits precede their numerical runs; the later public file uploads are not public preregistration.
```

Makes each run belong to its design and makes later uploads the direct subject. This retains the current distinction between original local design chronology and later public publication; it does not invent public preregistration.

### E24. Optional clarity in S35: avoid coined compound

Location: `submission-v10/supplement.tex` — line(s) 1603

**Before**
```text
so the original all-curve confirmation is not established.
```

**After**
```text
so the original confirmation across all curves is not established.
```

The same negative conclusion remains. Keep left-censored and not testable in the preceding clause; do not turn non-testability into support or a failure estimate.

### E25. Optional clarity in S35: align noun categories

Location: `submission-v10/supplement.tex` — line(s) 1603

**Before**
```text
These are inspected-period comparisons, not additional dealers or a fresh financial holdout.
```

**After**
```text
These comparisons use the inspected period and provide neither evidence from an additional dealer nor a fresh financial holdout.
```

Comparisons and dealers are different noun categories. The revision preserves both limitations: no additional-dealer evidence and no fresh holdout.

## Main article → supplement cross-reference checks

| Main pointer | Current destination | Result |
|---|---|---|
| Sections S1–S2; S3–S5 | Floor/endpoint propositions; original/corrected/secondary bound simulations | PASS |
| Section S30 | CFTC sources, eligibility, information dates and selected-code table | PASS |
| Sections S7 and S11–S18; S34 | AR replay, full panels/selection/calibration/combination evidence; retained archive routes | PASS |
| Sections S8 and S23 | Quantile ranks and implementation/inference conventions | PASS |
| Sections S14–S17, S19, S23, S29–S34 | Selection/calibration/Murphy families, implementation and new-study records | PASS |
| Sections S20–S21 and S26; Tables S19–S21 and S25–S26 | State groups/diagnostics, target-level sensitivity and full-prefix backcast | PASS |
| Sections S16–S18; Tables S14–S17 | Headroom/delayed wrappers and combinations | PASS |
| Sections S11–S15; Tables S9–S13 | Weekly panels, endpoint comparison, fixed selection and non-complete-rule inventory | PASS |
| Section S31 | Complete MCS membership, p-values, exact-loss classes and known unavailable methods | PASS |
| Figures S1–S2; Section S33 | Two moved original Murphy figures | PASS |
| Table S46; Section S33 | Accuracy and hit diagnostics | PASS — existing PDF labels this table S46 |
| Sections S27–S28; Tables S27–S32 | Earlier calibrated simulation/failures and stability/switching grids | PASS |
| Section S32 | Fixed limit-cost normalization and complete grid | PASS |
| New S35 | `sup:v11-history`; confirmation table `tab:v11-confirmation` = S47 | PASS; no main explicit S35 pointer currently found |

Existing PDF readback: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/supplement.pdf`, SHA-256 `8b615b44cab00e9a5bb92024ba22e857826352bc2eb7caae03b07261a7fa648c`, 33 pages. Text readback places S35 and Table S46 on PDF page 31, with Table S47 on PDF page 32; the contents also lists S35 at page 31. This was read-only extraction of the existing PDF, not compilation, layout approval or a new render. If that PDF is replaced later, rerun the root’s normal final document checks.

**Optional main-to-S35 navigation addition**

Before: the main history paragraph ends after its statement about sufficient history and a penalty menu permitting strong shrinkage.

After: retain that paragraph and append only:
```text
Supplement Section S35 retains the contrasts for both horizons and the saved confirmation criteria.
```

This adds a pointer to existing evidence without adding a citation, data, a result, a guarantee, or a new interpretation. The body should continue to identify the learning curve as retrospective and same-period.

## Consistency choices — apply only as a deliberate global copy-edit

1. **Four-feature / four-predictor.** Both labels refer to the existing four-input regression here. Neither is a grammatical error. The main article and supplement currently use both. Choose one reader-facing term globally; do not change QR4, method identities, file keys, source aliases or predictor counts. Example only: `the four-feature selector` → `the four-predictor selector` if four-predictor is selected as the global term; reverse the direction if four-feature is selected.

2. **p value / p-value.** Both occur in the current supplement. A global house-style choice can make prose consistent: e.g., `raw p values unavailable` → `raw p-values unavailable`. Keep code keys, source-native fields and exact p-values unchanged. No new adjustment or test is implied.

3. **Spelling variant.** Prose mixes American `centered`, `normalized` and `optimization` with British `favourable`, `favour` and `labelled`. If the manuscript’s American spelling is selected, the local replacements are `favourable` → `favorable`, `favour` → `favor`, and `labelled` → `labeled`; retain original spelling in quoted source titles and literal identifiers. These are optional house-style edits, not technical errors.

4. **History / window.** No forced replacement is recommended. History denotes training-history length; window also denotes inspected evaluation periods in S26. Replacing every occurrence with one word would erase a useful distinction.

5. **Strict hits / breaches.** Existing text defines the same strict threshold event. No wholesale synonym replacement is needed; preserve the existing distinction between event counts, empirical hit rates, and conditional-coverage claims. E13 only clarifies a rate–probability comparison.

## Current complete section map

| Number | Title | Label |
|---|---|---|
| S1 | Known-floor projection and strict quantile coverage | `sup:floor` |
| S2 | Classical endpoint-to-peak bound | `sup:levy` |
| S3 | Monte Carlo mechanisms: original increment persistence | `sup:simulation-original` |
| S4 | Mean-reverting levels and negative-increment sensitivities | `sup:simulation-primary` |
| S5 | All secondary simulation sensitivities | `sup:simulation-secondary` |
| S6 | Empirical endpoint plug-in: all original cells | `sup:levy-empirical` |
| S7 | AR residual replay and its adverse comparisons | `sup:ar` |
| S8 | Ordinary quantile ranks and minimizer endpoints | `sup:rank` |
| S9 | Fixed-report error preferences | `sup:preference` |
| S10 | Complete preference-frontier source | `sup:frontier-0` |
| S11 | Complete weekly panel: definitions and first half | `sup:panel` |
| S12 | Complete weekly panel: second half | `sup:panel-second` |
| S13 | Complete added-panel endpoint-plug-in comparison | `sup:panel-levy` |
| S14 | Earlier-period fixed selection rules | `sup:selection` |
| S15 | Selection failures and replication boundaries | `sup:selection-failures` |
| S16 | Finite delayed calibration and headroom SAV | `sup:wp2` |
| S17 | Wrapper comparisons, uncertainty and missing cells | `sup:wp2-pairs` |
| S18 | Untuned forecast combinations | `sup:wp3` |
| S19 | Combination Murphy diagrams and comparison families | `sup:wp3-murphy` |
| S20 | Training-defined position-change states | `sup:wp4` |
| S21 | Refitted target-level sensitivities | `sup:wp5` |
| S22 | Horizon coherence and late conditional-hit evidence | `sup:coherence` |
| S23 | Numerical implementation and inference conventions | `sup:implementation` |
| S24 | Frozen controlled comparison of inherited procedures | `sup:v8-mc` |
| S25 | Same-dealer completed-day aggregation | `sup:v8-daily` |
| S26 | Fixed-parameter full-prefix backcast and overlapping windows | `sup:v8-backcast` |
| S27 | Earlier calibrated simulation and numerical failures | `sup:v9-legacy-mc` |
| S28 | Pre-evaluation stability screen and switching stress simulation | `sup:v9-stability` |
| S29 | Paired menu isolation: full source inventory | `sup:v10-menu` |
| S30 | CFTC sources, eligibility and information dates | `sup:v10-cftc` |
| S31 | Complete model confidence sets | `sup:v10-mcs` |
| S32 | Fixed limit costs and full parameter regions | `sup:v10-cost` |
| S33 | Retained accuracy and hit diagnostics | `sup:v10-diagnostics` |
| S34 | Reproduction, availability and retained extended results | `sup:reproduction` |
| S35 | Additional saved evidence on history length | `sup:v11-history` |

## Review verification

- 25 itemized language/navigation suggestions; exact Before text found for 25/25 at the final snapshot. Not-found IDs: none.
- Each item’s numerical-literal sequence was checked unchanged between Before and After. Formulae, original constants, p-values, status identities, counterexamples, failure rows, censoring and retrospective-validation limits are preserved.
- All 35 section headings were parsed without assuming section commands occur at the start of a line. The newly added S35 was read in full, along with its generated confirmation caption and notes.
- No experiment, score, summary driver, fit, bootstrap, data acquisition, Git operation or old-directory access was performed. No edit is applied by this note.

## Latest PDF pagination and page-33 verification — appended 2026-10-25T05:26:32.955084+00:00

This append supersedes only the earlier PDF page-location snapshot. The earlier prose review and its reported PDF SHA/page locations remain preserved above. The root has added a FloatBarrier and recompiled; no PDF was edited or compiled by this verifier.

Latest absolute source: `/Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-v10/supplement.pdf`. SHA-256: `da9cc0f9f08bb22141a6915b06714f060166efcf341b30796ceb7d5b4d49245f`. Bytes: `290086`. Total pages: **33**. The SHA was rechecked unchanged after inspection.

| Element | Actual page in this latest PDF |
|---|---|
| Section S35 and its complete text | **33** |
| Table S47, its entire caption, all three rows and all three note lines | **33** |
| Table S46, accuracy and hit diagnostics | **31** |
| Figures S1–S2, Murphy diagrams | **32** |
| Contents entry for S35 | **33**, agrees with section location |

**Page-33 visual readback: PASS.** The page was rendered in memory at 150 dpi and inspected. The S35 heading, introduction, complete table, three explanatory note lines, provenance paragraph and final retrospective/holdout paragraph are all visible. Table headings and all row labels/numbers are legible. No clipping, overlap, missing line, displaced continuation or collision with the page footer was observed. The smaller note text is readable at the inspection resolution. This is page-33 visual QA only, not a fresh whole-document layout claim.

The following saved statements were also checked in the extracted page-33 text without recomputation:

- fixed pooled criteria: PASS.
- estimated threshold / no financial oracle: PASS.
- low-history counter and required fraction: PASS.
- high-history counter and required fraction: PASS.
- universal-order counter and failed result: PASS.
- earlier-threshold conditionality: PASS.
- different original menus / no isolated predictor dimension: PASS.
- counterexamples and candidate failures: PASS.
- local design / later upload boundary: PASS.
- both horizons and all tested histories: PASS.
- long-history reversals: PASS.
- left censoring and non-testability: PASS.
- all-curve non-confirmation: PASS.
- no extra dealers / no fresh holdout: PASS.

All source/provenance qualifications remain present: earlier method-specific threshold estimation; no financial oracle; original different penalty menus; no isolated predictor-dimension claim; failed universal ordering; complete counterexamples and candidate failures; local-design versus later-public-upload chronology; both horizons and every tested window; longest-history reversals; left censoring and non-testability; all-curve confirmation not established; inspected-period scope with no additional dealer or fresh financial holdout.

The three hyperlink annotations on page 33 are retained. Their targets are recorded below as document link identities only; no claim of remote publication/availability is made by this local PDF check.

- `https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v11/evidence/v11/pr5-v9`
- `https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v11/evidence/v11/pr5-v9/protocol/revision-v9/wp2-confirmatory.md`
- `https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v11/evidence/v11/pr5-v9/results/revision-v9/wp3/contrasts.json`

Read-only boundary: the PDF and all manuscript/generated sources remain unchanged. Only this appendix to the review note was written; the in-memory PNG was not saved to disk.
