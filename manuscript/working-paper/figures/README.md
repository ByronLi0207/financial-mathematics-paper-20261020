# Aggregate vector figures

The three original PDFs remain unchanged. `study_report.py` produces them from original public aggregates; their exact byte/hash identities are in `results/run-manifest.json` at the repository root:

1. `within-cell-paired-means.pdf`: the archived original display of every within-setting F-minus-S mean. The current paper uses the separate restyled file listed below.
2. `primary-monthly-paired-means.pdf`: every original inclusive primary calendar-month mean and origin count.
3. `primary-resampling-ranges.pdf`: all four original descriptive ranges, the observed mean and replicate averages.

The revision adds three figures while preserving those original files:

4. `revision-retrieval-contrasts.pdf`: every one of the 12 nearest-minus-recent loss means, in fixed H/count/method order. Only H6/m360/K is marked primary. Its footer states that the contrast was fixed before extension execution and that all 12 comparisons use the already inspected interval. Common axes and direct signed USD-million values retain all comparisons.
5. `revision-retrieval-monthly.pdf`: all 13 monthly primary K contrasts at both horizons, all origin counts and the adverse positive January 2016 means. Calendar groups remain descriptive.

6. `revision-original-contrasts.pdf`: the current Figure 1, restyling all seven original direct paired means in their fixed setting order. It uses the original accepted manifest and paired table, not extension forecasts. Explicit H/n/tau columns, the common 6,625 issue origins, a signed zero axis, three-decimal tick labels and six-decimal direct USD-million values replace the original display's long decimal strings. The small positive tau=.90 value remains +0.000144. Neither point jitter nor numerical aggregation is introduced. F/S and the score units are explained on the standalone page.

`build_revision_figures.py` constructs only the two extension figures. `build_original_comparison_figure.py` constructs only the restyled original comparison and reuses the same rendering helpers. Each pins its accepted manifest and aggregate table identities, validates every displayed row and writes to a new direct `.scratch/revision-figure-*` directory. Neither reads source observations, private paths or per-origin forecasts. All three added PDFs are standalone one-page A4 landscape vectors, using Helvetica / Helvetica-Bold without image objects. Their approved SHA-256 hashes are:

```
revision-retrieval-contrasts.pdf
955a66245f7feae559c5232d79e2244881969d169a808a6f059d7665c99637f4

revision-retrieval-monthly.pdf
cfcb2f8f84edcd804844b57357242cd31ae67a67f9ca9fd49e73377c5c54f798

revision-original-contrasts.pdf
3aebc5716ca2c15b5c74cc61feec0b7461dbeef1e886767a34a279c1e531cc8f
```

All money is source-reported USD millions with factor 1e-6. Negative values favor the left-named rule within the stated common objective. The new comparisons are exploratory on an inspected interval, with no uncertainty intervals or significance claims. The original resampling ranges remain descriptive. No smoothing, favorable-month selection, jitter or across-preference winner is introduced. All plots are original, without copied third-party figures or redistributed source data.
