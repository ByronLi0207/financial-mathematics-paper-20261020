# Aggregate vector figures

The three original PDFs remain unchanged. `study_report.py` produces them from original public aggregates; their exact byte/hash identities are in `results/run-manifest.json` at the repository root:

1. `within-cell-paired-means.pdf`: every original within-setting F-minus-S mean, retained in the revised paper as Figure 1.
2. `primary-monthly-paired-means.pdf`: every original inclusive primary calendar-month mean and origin count.
3. `primary-resampling-ranges.pdf`: all four original descriptive ranges, the observed mean and replicate averages.

The revision adds two figures from the separately accepted extension aggregates:

4. `revision-retrieval-contrasts.pdf`: every one of the 12 nearest-minus-recent loss means, in fixed H/count/method order. Only H6/m360/K is marked primary. Common axes and direct signed USD-million values retain all comparisons.
5. `revision-retrieval-monthly.pdf`: all 13 monthly primary K contrasts at both horizons, all origin counts and the adverse positive January 2016 means. Calendar groups remain descriptive.

`build_revision_figures.py` constructs only the two new figures. It pins the accepted manifest and aggregate table identities, validates every row and writes to a new direct `.scratch/revision-figure-*` directory. It reads no source observations, private paths or per-origin forecasts. The new PDFs are standalone one-page A4 landscape vectors, using Helvetica / Helvetica-Bold without image objects. Their approved SHA-256 hashes are:

```
revision-retrieval-contrasts.pdf
41e068e629688413bf385e7192ed97af29b5f4fb8f490fa49b848127e2a6507c

revision-retrieval-monthly.pdf
cfcb2f8f84edcd804844b57357242cd31ae67a67f9ca9fd49e73377c5c54f798
```

All money is source-reported USD millions with factor 1e-6. Negative values favor the left-named rule within the stated common objective. The new comparisons are exploratory on an inspected interval, with no uncertainty intervals or significance claims. The original resampling ranges remain descriptive. No smoothing, favorable-month selection, jitter or across-preference winner is introduced. All plots are original, without copied third-party figures or redistributed source data.
