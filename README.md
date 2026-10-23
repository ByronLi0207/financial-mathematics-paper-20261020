# Historical and Conditional Forecasts of Sampled Net-Position Peaks

An English working paper comparing established forecasting methods for the largest absolute source-reported net position at issue and over the next H records. It uses an individual-market-maker FX record and a separately fitted weekly Treasury-bill position aggregate. The contribution is a bounded retrospective benchmark on a common target, with complete favorable and adverse results.

Read the revised [19-page paper](manuscript/supervisor-revision/main.pdf), [editable TeX](manuscript/supervisor-revision/main.tex), [revision guide](manuscript/supervisor-revision/README.md) and [Chinese change inventory](REVISION_SUPERVISOR_20261023.md). The new PDF is the actual Tectonic/XeTeX output: 14 pages including references plus five appendix pages, authored as Byron.

## Second supervisor revision on 23 October 2026

The [E6 table](results/supervisor-20261023/e6/table6.csv) adds ordinary empirical-quantile I and expanded-regression breaches, and [fixed ridge paths](results/supervisor-20261023/e6/lambda-path.csv) preserve every diagnostic point without changing selection. The intercept-only minimizer can be an interval; I is not universally the exact corrected-rank historical F.

The [E5 prediction](protocol/supervisor-20261023/e5-panel-prediction.md) was committed alone before new fitting. All [48 panel cells](results/supervisor-20261023/e5/summary.csv) completed. P1=30/45 and P2=24/48 are unsupported; P3=33/48 is supported. The full regression's median excess loss falls from +92.6% to +9.2%, but 34/48 cells still lose to F. This is a post-result extension using twelve archived series with shared dealer reporting and overlapping positions, not independent replication.

The paper now centers its contribution on shrinkage and remaining failures, adds practical implications, and [reports the two original primaries separately from the remaining 71 Holm contrasts](results/supervisor-20261023/w3/summary.json). This reporting division was chosen after results; the previous 72-member archive is preserved. The Treasury primary has raw HAC p=.007611 and two-primary Bonferroni p=.015223. [AR comparisons](results/supervisor-20261023/w4/ar-comparison.csv) distinguish original and expanded QR. The [full rewritten abstract, contribution paragraph and conclusion](manuscript/supervisor-revision/round2-rewritten-passages.md) and [current verification](results/supervisor-20261023/round2/document-verification.json) accompany the paper.

## First supervisor revision archive

The revision reorganizes the paper around three empirical contributions, adds checked predictive-ability and coverage diagnostics, and separates predictor changes from the ridge-menu change. The exploratory [E3 results](results/supervisor-20261023/e3/README.md) retain every original comparison: expanding the full regression's penalty menu changes Treasury H6/W260 excess loss from +50.786% to +3.434%, while all four FX forecasts remain identical to the originals. The common-menu full-versus-four-predictor difference is only +1.242% in that Treasury cell (unadjusted DM p=.685); this does not establish equivalence or a causal feature effect.

The checked [inference archive](results/supervisor-20261023/inference/) reports the fixed 72-member Holm family, separate unadjusted FX cross-window comparisons, HLN and bandwidth sensitivity. The original Treasury adverse comparison has raw p=.007611 and Holm p=.319678. Coverage diagnostics consistently condition the Christoffersen joint likelihood on the initial hit while retaining full-grid Kupiec separately. All inference is retrospective and exploratory.

The original [24-page paper](manuscript/working-paper/paper.pdf), [TeX](manuscript/working-paper/main.tex), [structured content](manuscript/working-paper/paper-content.json), [reference catalog](manuscript/working-paper/references.bib) and [document guide](manuscript/working-paper/README.md) remain unchanged. That older supplied PDF uses a separate ReportLab/pypdf route; the new revision uses real TeX compilation.

## Earlier critical review of the original working paper

The [review and corrections](REVIEW_20261023.md) explain the substantive changes. The revision clarifies that Treasury models are fitted separately, exposes the downloaded-vintage economic-date convention in the abstract, and limits the loss-weight envelopes to eight archived .95 reports. It separates mean underprediction and overprediction amounts from breach frequency and actual resource allocation. It also distinguishes the stronger short-horizon FX finding from the long-horizon gain concentrated in a short tail segment.

All **15 numerical tables, 21 equation blocks, three vector figure inputs, declared primaries and adverse financial outcomes** are retained. The current citation list has 25 used entries; the unused Liao–Theodosopoulos record remains in historical evidence. No financial model was refitted or new source acquired. The small added annual decomposition reads only three hash-bound public aggregate CSVs.

## Findings and their limits

The response is the sampled peak P=max|N|, including the current known floor B=|N|. Historical F/K rules already use current magnitude and S uses the signed anchor. Direct conditional methods comprise ridge quantile regression (QR), multivariate local quantiles (KNN) and a scale-adjusted local variant. Training uses completed responses, training-only transforms and source-specific chronological selection. Matched controls share the completed-label pool and refit schedule, without isolating a causal feature effect.

| Fixed comparison | Mean pinball loss change | Strict breaches | Interpretation |
|---|---:|---:|---|
| FX H6 primary: QR W2880 minus original rolling F W720 | −12.660% | 376 vs 332 of 6625 | Both mean error components fall; breach occasions increase. History and update schedule also change. |
| FX H6 matched context: QR W2880 minus frozen F W2880 | −14.767% | 376 vs 360 of 6625 | Same completed-response history and refit schedule; both mean error components fall. |
| FX H24 legacy sensitivity: QR W2880 minus original rolling S W720 | −1.829% | 531 vs 287 of 6625 | Underprediction amount more than doubles; 70.83% of the small net gain comes from the partial 2017 tail. |
| Treasury H6 primary: QR W260 minus frozen F W260 | +50.786% | 54 vs 28 of 277 | Adverse score and underprediction results from numerically accepted fits. |

The FX H6 tail contribution is only 8.64% for the primary and 6.87% for the matched comparison. Their mean underprediction and overprediction amounts both fall in each existing issue-year group and on the fixed 947-origin grid. The [aggregate decomposition](notes/revision-20261023/annual-decomposition.json) supports this distinction without creating a new validation sample.

Every original-menu Treasury QR and scaled-KNN cell loses to its own frozen F control. Short-history plain KNN selects the whole pool and equals F; this is a selected identity, rather than a failure fallback. Later exploratory AR replay improves on original QR in all four Treasury cells and loses in three of four FX cells. Against matched S, AR lowers loss in five of eight cells while breaches increase in all eight. The original primaries remain unchanged.

The .95 score is .95 U+.05 V, where U=mean(P−C)₊ and V=mean(C−P)₊. These are passive forecast errors under stipulated weights, rather than observed financing costs. The [eight-report loss-weight supplement](results/revision-20261022/preference-robustness/README.md) shows that the FX H24 legacy gain reverses above ratio **20.630898**, near the stipulated 19. Full/sparse menu minimizers at .95 differ in four dependent cells; Treasury H24 grids contain only 12 origins. The envelope excludes feasible reports such as C=B, so its endpoint winners are menu-relative.

The FX evaluation archive had already been inspected before the conditional extension. Treasury uses a downloaded snapshot indexed by economic date, without historical first-release reconstruction. Overlapping labels, shared histories, source-specific measurement and post-result analysis choices limit inference. The paper establishes no new estimator, population or conditional-coverage guarantee, compatible unseen dealer validation, or observed benefit from changing quotes, hedges, funding or risk limits.

## Complete evidence

- [Conditional design](protocol/revision-20261022/conditional-baseline-design.md), [machine specification](protocol/revision-20261022/study-spec.json), [executable freeze](protocol/revision-20261022/executable-freeze.json) and [selection freeze](protocol/revision-20261022/selection-freeze.json) identify the declared procedures and their execution chronology.
- [Complete conditional archive](results/revision-20261022/README.md) retains all candidates, 90 procedure summaries, 98 declared contrasts, annual/sparse sensitivities and 56 phase receipts. Its immutable README describes its dated checkpoint; later manuscript and Treasury-archive delivery are linked here.
- [AR replay](results/revision-20261022/ar1-replay/README.md) retains every cell and all 24 comparisons; [fresh-attempt reproduction](results/revision-20261022/ar1-fresh-reproduction/README.md) preserves the original manifest-bound diagnostic route.
- [Floor/horizon diagnostics](results/revision-20261022/POST_RESULT_DIAGNOSTICS.md), [AR diagnostics](results/revision-20261022/ar1-diagnostics/README.md), [ordinary-rank sensitivity](results/revision-20261022/rank-ablation/README.md) and [late conditional-breach evidence](results/revision-20261022/coverage-evalues/README.md) are explicitly post-result and do not repair forecasts or replace primaries.
- [Original construction results](results/README.md) and [one-state retrieval extension](results/revision-20261021/README.md) preserve the earlier complete menus and adverse outcomes.
- [Source evidence map](notes/revision-20261022/paper-evidence-map.md) records actual consulted editions and reading scopes. Wisniewski et al.'s endpoint work, financial path-extrema and liquidity-buffer precedents prevent first-method or first-peak-forecast claims.

## Sources and availability

FX uses the one-hour member of the [Net Position Time Series Dataset, version 2](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset): 18,576 records and 1,286,391 bytes, SHA-256:

```
b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa
```

Obtain only `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv` from version 2. The complete collection is much larger and is unnecessary. If delivered as a ZIP, inspect the member list and extract only that CSV. Require the exact hash and byte count before using `.scratch/data/1hourNetPositionsKaggle.csv`. Preserve a mismatching existing file; do not substitute another frequency or derived-feature member. FX redistribution permission remains unverified, so raw observations and private forecast vectors are not included here.

Treasury uses [NYFed Primary Dealer Statistics](https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics), series PDPOSGS-B: 706 weekly Treasury-bill long-minus-short market-value records, 3 April 2013–7 October 2026, in USD millions. The accepted 23,315-byte CSV has SHA-256:

```
9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb
```

The [unchanged Treasury snapshot](data/nyfed-pdposgs-b-20261022/README.md) is archived with attribution and continuing NYFed terms. Its aggregate permits cross-dealer cancellation; FR 2004A uses trade-date accounting, specified settlement-date buyback treatment and eligible forward/when-issued positions. It does not measure settled cash holdings or individual gross exposures. The [external data guide](results/revision-20261022/EXTERNAL_DATA.md) gives routes, definitions and release limitations. A current download can revise or extend the series; a matching label is not a matching snapshot. Source-native monetary values are never pooled.

## Verification and reproduction

Choose a compatible existing interpreter. Core archive verification uses the standard library. The preference-envelope scripts require **Python 3.10+**. The pinned [NumPy 2.3.5](https://numpy.org/doc/stable/release/2.3.5-notes.html) financial environment supports **Python 3.11–3.14**. Current document and aggregate checks used Python 3.12.14; the annual helper was also checked with system Python 3.9.6. No installation was needed.

The default command is read-only and requires no raw data:

```bash
python3 -B reproduce_conditional.py
```

Its successful status is `ARCHIVE_VERIFIED`, with `accuracy_recomputed=false`, `raw_sources_read=false` and all 69 core files verified. This is an integrity check, rather than recomputed accuracy.

Document rebuilding is separate:

```bash
mkdir -p .scratch
python3 -B build_tex.py --output .scratch/main-NEW_ID.tex
python3 -B build_paper.py --output .scratch/paper-NEW_ID.pdf
python3 -B notes/revision-20261023/annual-decomposition.py --output .scratch/annual-NEW_ID.json
```

All outputs must be new. The [document guide](manuscript/working-paper/README.md) gives fonts, source compilation, the separate PDF route and actual visual/text checks. Compile the supplied TeX from `manuscript/working-paper` with its adjacent `figures`, rather than treating a scratch source file as a standalone compilation package.

An explicit full financial replay requires macOS, the pinned compatible NumPy environment and both accepted snapshots as regular files, with regular nonsymlinked ancestors:

```
.scratch/data/1hourNetPositionsKaggle.csv
.scratch/revision-20261022/nyfed-PDPOSGS-B.csv
```

Prepare the second path from the archived Treasury CSV. Verify and preserve existing inputs rather than overwriting a different version. Then:

```bash
python3 -B reproduce_conditional.py replicate --attempt-id NEW_UNIQUE_ID
```

The replay creates a new attempt, reruns 24 validation, 24 evaluation and eight reference phases serially under one total 540-second deadline, and checks all selected cells before evaluation. It preserves old results and records every aggregate difference, including small floating differences. Failures remain failures, without shortened means or favorable replacement choices. The standing limits are 2 GiB RSS, two observed threads, 100 MiB raw sources and 25 MiB per download, with stricter phase checks; recorded snapshots are not a continuous OS sandbox.

The [recorded prior full replay](results/revision-20261022/reproduction-check-20261022.json) reproduced all six aggregate CSVs and selections. It is same-data numerical reproduction, rather than independent scientific replication. Optional [diagnostic reproduction](results/revision-20261022/diagnostic-reproduction-check-20261022.json) uses a successful new attempt and does not refit models.

The [current rendering receipt](manuscript/working-paper/rendering-verification.json) identifies the 24-page artifact and its checks. Earlier [24-hour](RESEARCH_WINDOW_AUDIT.md), [21 October](REVISION_20261021_AUDIT.md) and [22 October](REVISION_20261022_AUDIT.md) work audits cover their own dated windows; their credited time and manuscript counts are not extended by this revision. No journal submission or journal-tier guarantee is represented.
