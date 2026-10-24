# B4 numerical-preservation review

**PASS. No numerical correction is requested for the reviewed B4 snapshot.** This worker changed only this report. No manuscript, supplement, result, source-data, model, calibration or Git change was made; no statistical evaluation or aggregation was run.

## Exact reviewed state

|File|SHA-256|
|---|---|
|`submission-jof/manuscript.tex`|`b0a2617ecfee8a1e112b173725d4155ad5834e42e6b094f4d07e20b2b4d7815a`|
|`.scratch/v8/manuscript-before-b4.tex`|`1b2126b159485544ceb944c28cfe5b4dd3ac731aafe59c7dc43f3c5a2eba8c7a`|
|`notes/v8/writing-numeric-bindings.json`|`6db223cdaa4d10a43102f4c5a73f08b275a1b08fd908341620854807acd88cac`|

The audit includes the two late clarifications reported by the main owner: explicit simulation prediction thresholds and the earlier weekly evaluation count. Table numbers in this source are Table 3=`tab:fx`, Table 4=`tab:weekly`, Table 5=`tab:diagnostics`.

All 18 body entries and 13 table-format entries in the writing ledger were routed through the v7 FX/panel evidence IDs to their native JSON pointers or unique CSV selectors. All 31 raw scalars agree with the actual archives. Every changed percentage display is the direct one-decimal formatting of its raw source value. Native Table 3 issue/breach counts and Table 4 panel/group counts were checked separately. The full numeric-token sequence of Table 5 is unchanged from the pre-B4 source.

## Core table readback

|Contrast / procedure|Archived raw percentage|Current display|Unchanged issues, hits or loss counts|
|---|---:|---:|---|
|Later FX versus rolling F720|−12.660126412969763|−12.7%|6625 issues; 376/332 hits|
|Later FX versus matched F2880|−14.766762552613885|−14.8%|6625 issues; 376/360 hits|
|Earlier FX versus rolling F720|+3.1681985293173343|+3.2%|1440 issues; adverse ranking retained|
|Earlier FX versus matched F2880|−16.62356533682211|−16.6%|1440 issues; 20/16 hits; original three-menu QR/R0, not R2|
|Delayed wrapped FX QR versus wrapped F|−14.99691078803782|−15.0%|6625 issues; 329/328 hits|
|Original Treasury H6/W260|+50.78571256749063|+50.8%|54/28 hits among 277 issues|
|Earlier Treasury H6/W52|+144.296201250835|+144.3%|Explicitly different history from original W260|
|Original full panel QR33 median|+92.62799824594052|+92.6%|45/48 losses|
|Four-predictor panel median|+9.90727239745182|+9.9%|37/48 losses|
|Expanded full panel QR33 median|+9.220703399904492|+9.2%|34/48 losses|
|Ordinary empirical I panel median|+0.5006801691981209|+0.5%|30/48 losses|
|Earlier R0 weekly median|+4.1510024714803695|+4.2%|26 earlier weekly groups|
|Earlier R2 weekly median|+5.374072481175762|+5.4%|26 earlier weekly groups|

The source objects are `results/revision-20261022/paired-comparisons.csv` (the named FX and Treasury contrast IDs), `results/supervisor-20261023/r6-writing-hac-20261023/comparisons.csv` and `results.json` (the two named earlier FX references), `results/revision-20261023/v6/wp2-findings.json /wrapped_pairs/1`, `results/supervisor-20261023/r6/primary-replication.csv` (`Treasury-W52-structural-analogue`), `results/supervisor-20261023/e5/descriptive-summary.json`, and `results/supervisor-20261023/r6/assessment.json`. Each writing-ledger raw value agrees with its native field.

Reference identities and signs are preserved. The 332 and 360 hit counts remain distinct historical references. Wrapped 329/328 is a separate delayed procedure. Replacing the label “primary” with “main comparison” does not replace the underlying forecast pair. The earlier Treasury comparison remains W52 rather than W260; the R2 worst cell remains the H24 bill case.

## Direct rounding, restored I result, and late clarifications

- **Lower-target FX:** `results/revision-20261023/v6/wp5-tau-summary.json /rows/1/mean_loss_change_percent` is `−10.145914078498173`. The main correctly says a **10.1% reduction**, directly from that raw field, rather than rounding the old displayed `−10.15%` again. The distinct original rolling-reference raw value `−9.204288754403045` remains a **9.2% reduction**.
- **Combinations:** native `wp3-findings.json` values `−3.9812983393045176` and `+2.7730553886759823` become a **4.0% reduction** for the median and a **2.8% increase** for the mean. The adverse mean is explicitly retained.
- **Restored ordinary empirical I:** `results/supervisor-20261023/r6/summary.csv`, selector `phase=retro, source=nyfed_weekly, series_key=PDPOSGSC-L2, horizon=24, window=52, report=I`, has `percent_vs_F=36.50893744342638`, correctly displayed as **36.5% worse**. The existing `notes/supervisor-20261023/r6-document-provenance.json` I summary stores this same worst value. This is a pre-existing PR3/v7 result, not a new evaluation and not R2's worst result.
- **R2 remains distinct:** native `r6/assessment.json /S1/worst_percent_vs_F=181.39452368014167` becomes **181.4%** in the main; the supplement retains 181.39 percent. `/S1/status`, `/S2/status`, and `/S3/status` remain `NOT_MET`.
- **Earlier weekly evaluation count:** the new Table 4 phrase “each have 52 evaluation points” matches `origin_count=52` in the bound native `r6/summary.csv` H24/W52 bill R2 row. The same `origin_count` field was checked across every earlier weekly native row; all are 52. This check only verifies source fields and does not generate a new score or summary.
- **Simulation prediction thresholds:** the main's **2.0%** maximum-gain and **5.0%** adverse-loss thresholds agree directly with `results/v8/mc/experiment-settings.json /preregistered_constants/prediction_thresholds/P1_maximum_gain_pct` and `/P3_minimum_excess_pct`. They remain frozen predictions, not fitted thresholds.
- **Remaining main simulation percentages:** existing `summary.json` D2/p33 raw medians `0.3528682097196367` (W52) and `−20.562859332263795` (W2880) directly support +0.4% and −20.6%. No simulation summary was recomputed.

## Adverse evidence retained in the main or detailed supplement

|Required adverse family|Retained presentation|
|---|---|
|Earlier FX reversal against rolling history|Main Table 3 and loss subsection retain +3.2%, separately from the matched gain.|
|Short-history H24 FX deterioration|Main line 222 retains +31.5% and 924/427 hits; the original horizon map remains available.|
|Treasury deterioration|Main +50.8%, 54/28 hits; Table 4 retains earlier W52 +144.3%.|
|Weekly panel losses after shrinkage|Table 4 retains all four procedure summaries and 45/48, 37/48, 34/48, 30/48; detailed panel cells remain in the supplement.|
|Conservative-rule failure|Main retains 181.4%; supplement lines 866–870 retain all three `NOT_MET` results, median 5.37 and worst 181.39.|
|R2 gives up part of the earlier FX gain|Supplement line 860 retains R0 −16.62 and R2 −6.28, with 20/20 versus F16 hits.|
|Mandatory validation failures|Supplement line 878 retains `REQUIRED_VALIDATION_CANDIDATE_FAILED` and its full row inventory.|
|Mean-combination and headroom-recursion losses|Main line 231 explicitly retains the mean increase and adverse recursion; detailed SAV and combination rows remain in the supplement.|
|Adverse/unavailable wrapped weekly comparisons|Supplement retains bill H6/W260 +7.89 and `VALIDATION_INELIGIBLE` rows.|
|Upper-target unavailable forecasts|Main line 201 keeps the qualification; supplement lines 1220–1222 retain FX/bill tau .99 NA results.|
|Simulation's unsuccessful mechanism check|Main keeps seven of eight hourly cells failed, P1/P3 unsupported and P2/P4 unassessable. The supplement retains every main-grid cell and failure. The short-history D0/p33 +1.1% omitted from the shortened main paragraph remains in its full simulation table.|

These are retained result families and explicit source locations; shortening the main does not turn surviving partial repetitions or missing upper-target forecasts into a completed favorable result. No negative sign, failed status or original comparison reference was changed by the reviewed writing pass.

## Display and terminology

All **33 explicit percentage literals** before the bibliography have one decimal place, including the two newly explicit simulation thresholds. All 13 changed Table 3/4 percentage entries likewise have one decimal. P-values and quantile levels remain in their appropriate formats rather than being rounded as percentages.

No `legacy` or `analogue` remains in the main. Remaining `primary` occurrences are primary-dealer terminology, the official Primary Dealer Statistics service, the official FR 2004 report title, the dataset title and its URL. None is a technical placeholder for the favored forecast. Official source names and titles are preserved.

The unchanged Table 5 numbers retain raw DM versus HLN references, original 72-contrast Holm, two-comparison Bonferroni, and the distinct full/nonoverlap hit grids. The writing change does not create prospective or selection-adjusted evidence.

This PASS is bound to the hashes above. Compilation, page inspection, global protected-file hashing and final package acceptance remain the main owner's separate checks.
