# Aggregate vector figures

The three original PDFs remain unchanged. `study_report.py` produces them from original public aggregates; their exact byte/hash identities are in `results/run-manifest.json` at the repository root:

1. `within-cell-paired-means.pdf`: the archived original display of every within-setting F-minus-S mean. The earlier revision paper used the separate restyled file listed below.
2. `primary-monthly-paired-means.pdf`: every original inclusive primary calendar-month mean and origin count.
3. `primary-resampling-ranges.pdf`: all four original descriptive ranges, the observed mean and replicate averages.

The earlier revision adds three figures while preserving those original files:

4. `revision-retrieval-contrasts.pdf`: every one of the 12 nearest-minus-recent loss means, in fixed H/count/method order. Only H6/m360/K is marked primary. Its footer states that the contrast was fixed before extension execution and that all 12 comparisons use the already inspected interval. Common axes and direct signed USD-million values retain all comparisons.
5. `revision-retrieval-monthly.pdf`: all 13 monthly nearest360 K-minus-recent360 K contrasts at each horizon, all origin counts and the adverse positive January 2016 means. H=6 is the primary comparison; H=24 is sensitivity evidence. Calendar groups remain descriptive.

6. `revision-original-contrasts.pdf`: the earlier revision Figure 1, restyling all seven original direct paired means in their fixed setting order. It uses the original accepted manifest and paired table, not extension forecasts. Explicit H/n/tau columns, the common 6,625 issue origins, a signed zero axis, three-decimal tick labels and six-decimal direct USD-million values replace the original display's long decimal strings. The small positive tau=.90 value remains +0.000144. Neither point jitter nor numerical aggregation is introduced. F/S and the score units are explained on the standalone page.

`build_revision_figures.py` constructs only the two extension figures. `build_original_comparison_figure.py` constructs only the restyled original comparison and reuses the same rendering helpers. Each pins its accepted manifest and aggregate table identities, validates every displayed row and writes to a new direct `.scratch/revision-figure-*` directory. Neither reads source observations, private paths or per-origin forecasts. All three added PDFs are standalone one-page A4 landscape vectors, using Helvetica / Helvetica-Bold without image objects. Their approved SHA-256 hashes are:

```
revision-retrieval-contrasts.pdf
955a66245f7feae559c5232d79e2244881969d169a808a6f059d7665c99637f4

revision-retrieval-monthly.pdf
cdb44a4c23ba3c513f65aeb13573bfcec088a21c94e55873bb5e1c67f2e3dc15

revision-original-contrasts.pdf
3aebc5716ca2c15b5c74cc61feec0b7461dbeef1e886767a34a279c1e531cc8f
```

In these six historical figures, all money is source-reported FX USD millions with factor 1e-6. Negative values favor the left-named rule within the stated common objective. The new comparisons are exploratory on an inspected interval, with no uncertainty intervals or significance claims. The original resampling ranges remain descriptive. No smoothing, favorable-month selection, jitter or across-preference winner is introduced. All plots are original, without copied third-party figures or redistributed source data.

## Current conditional-study figures (22 October 2026)

The current paper appends these three one-page vector PDFs, in this exact order:

1. `conditional-common-history.pdf`: all 24 selected QR/KNN/scaled configurations against own-source/H/W frozen F. Each source has an explicitly separate percent axis. Both full-pool NY W52 KNN zero differences remain marked.
2. `conditional-primary-tradeoffs.pdf`: the two declared source primaries and FX H24 legacy sensitivity, with loss/mean-overrun/unused percentages and strict-breach changes in percentage points. Unused allowance uses neutral gray; no aggregate monetary amount is pooled across sources.
3. `conditional-annual-primary.pdf`: all ten issue-year groups for those same three comparisons, with origin counts and the partial 2017/2026 years marked. Years are subdivisions of the same records, not replications or inference.

`build_conditional_figures.py` pins the exact accepted second audit and three aggregate CSV identities, checks all 90 evaluation/98 paired/388 annual rows and displays 24/12/10 points. Its pure tests cover missing, duplicate, mislabeled or mutated input; denominator/sign/percentage-point arithmetic; full-pool fallback; geometry; and exclusive output paths. It neither reads raw financial observations nor refits a model. Output is a new direct `.scratch/conditional-figure-*` staging directory, with a provenance/geometry/resource receipt.

Approved current identities:

```
conditional-common-history.pdf
e0db8635c2b3b38c7bdcc22808fa3a5b84ae74cd21f15ec01c3dd5f2e0326bcf

conditional-primary-tradeoffs.pdf
adb27aa81113ac47d1bfb8aaaa1b19a5b5d37bd47693f2f38056d1e885f641c6

conditional-annual-primary.pdf
a77090ef7af98f2376c186f8f837cd44a76c8871aca0d526be3b613376534644
```

These current displays use within-comparison relative values and explicit source-native units. Overlapping origins, no confidence intervals, the previously inspected FX interval, the adverse Treasury primary and incomplete calendar years are visible. Older figure files remain unchanged.
