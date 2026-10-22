# Historical Response Selection for Sampled FX Net-Position Peaks

An English working paper comparing mature empirical-quantile constructions and historical episode selection for a sampled FX net-position peak. The response is the largest absolute source-reported USD net position over the current and next H records. It is an aggregate client-flow proxy from one market maker; a recorded netted position does not reconstruct its complete hedged book, gross currency exposures or funding needs.

Read the [16-page paper](manuscript/working-paper/paper.pdf), [compilable TeX source](manuscript/working-paper/main.tex), [shared structured content](manuscript/working-paper/paper-content.json) and [document verification](manuscript/working-paper/rendering-verification.json). The current revision adds an explicitly exploratory historical-selection comparison and finite construction bounds. It reports an application result, without claiming a new quantile estimator, first financial peak forecast or coverage theorem.

## Two design histories and their results

The original specification was frozen at **2026-10-21 05:46:37 UTC**, before its target-specific forecasts and losses, and published in commit `6dd404d6e700ff031793d68be209e8f783b22582`. It fixes seven one-factor settings and five methods, with **6,625 common issue origins**. The original 24-hour window and completed reading/design gates are documented in the [historical research-window audit](RESEARCH_WINDOW_AUDIT.md). This is a retrospective specification exercise with prior source-literature knowledge, rather than external preregistration or prospective collection.

The extension was designed **after the original evaluation interval had been inspected**. Its [protocol](protocol/revision-20261021-exploratory-protocol.md) and [machine specification](protocol/revision-20261021-exploratory-spec.json) were publicly recorded in commits `63703b911ee165a6057b0e80c36fd39c72cbcc4a` and `69d5bb67c6ca1e3c1509e29c14400462ce2a1130` before the added forecasts. It retains the same issue origins and evaluates all three response representations on five fixed historical sets at H=6 and 24. This before-execution freeze does **not** make the inspected interval an unseen holdout.

The primary rows use a .95 pinball score: a dollar of underprediction receives nineteen times the weight of a dollar of overprediction. The score retains the source's USD units but does not measure an observed funding payment or financial saving. Other consistent scores can target the same quantile while valuing errors differently; the reported rankings concern the chosen pinball score.

| Analysis | Fixed primary comparison | Paired mean loss difference | Interpretation |
|---|---|---:|---|
| Original | F minus S; H=6, n=720, tau=.95 | −USD 9,374.86; −2.08% of S loss | F has lower score, with 332 versus 254 breaches and greater mean positive overrun. H=24 favors S; tau=.90 also favors S, by only USD 144.23, without establishing equivalence. |
| Exploratory extension | nearest360K minus recent360K; H=6, tau=.95 | −USD 277,704.47; −31.83% of recent360K loss | Matching signed starting positions improves this weaker native-peak reference. Its loss remains above the original full720 F and S. |

All **12** fixed nearest-minus-recent score contrasts are negative. No added configuration beats the better original full720 F/S rule at the same horizon. This precise claim retains the exception that nearest360S at H=6 slightly improves its own full720S counterpart. Every matched S retrieval comparison has more breaches and greater mean positive overrun. Every matched F comparison has a larger conditional mean overrun, even with fewer breaches and smaller unconditional overrun. Primary K also has a larger conditional overrun despite fewer breaches; these conditional means describe different event sets. January 2016 is adverse for the primary K retrieval contrast at both horizons.

The paper reports these tradeoffs alongside selected age and anchor radii. Nearest membership guarantees a weakly smaller maximum signed-anchor distance at a fixed count; the observed representation gaps and score changes are separate results. The contrast compares two complete membership rules, without separating proximity from accompanying changes in age, regime, scale and dependence composition. No population test, confidence interval or bootstrap is attached to the new contrasts. The four original resampled-mean profiles remain descriptive and concern only original full720 F/S.

## What is being transferred

F retains a historical peak's headroom above its own starting magnitude. S translates each historical increment envelope to the current signed position. K takes a native-peak quantile subject to the current known floor; K is original method L, relabeled. Every representation already uses current information. The extension adds fixed one-dimensional signed-state nearest-neighbor membership, compared with an equal number of recent episodes from the same 720 completed candidates. There is no fitted volatility filter, dynamics model, adaptive neighbor-count search or new conditional-coverage method.

For a common selected set and available rank, elementary finite-array bounds relate F/K and S/K report differences to absolute and signed starting-position distances. Exact signed-anchor matches make all three reports agree in real arithmetic. Coherent counterexamples and a known-dynamics replay identity explain why construction agreement and exact raw revaluation do not establish forecast accuracy or the appropriate conditional envelope law.

The closest empirical lineage is [Wisniewski, Lindsay and Lindsay (2020)](https://proceedings.mlr.press/v128/wisniewski20a.html) and the same-source doctoral thesis, which study signed endpoint forecasts with richer features. The 2020 paper already evaluates nearest-neighbor quantile, conformal and normalized-conformal variants on these observations; this revision does not introduce nearest neighbors to that financial source. Their reported interval scores are not benchmarks for this absolute multi-record peak. Financial peak-risk, filtered historical simulation and nearest-neighbor quantile methods also have established precedents. The [14-reference source evidence map](notes/revision-20261021/paper-evidence-map.md) identifies exact consulted editions, actual reading scopes and claim boundaries. The [original nine-reference map](notes/paper-evidence-map.md) remains a historical record.

The [additional method comparison](notes/revision-20261021/method-transfer-comparison.md) explains how mature conditional-quantile models, residual calibration, historical scenario models, active hedging and forecast-evaluation theory relate to this response. It records eight consulted works and their actual reading scopes, including CAViaR and SPCI now cited in the paper and six other neighbors, including two 2026 preprints. These are method and evaluation neighbors; their published outcomes are not extra same-target benchmark results.

## Files

- [Original results](results/README.md): all 35 method/setting rows, seven paired comparisons, four resampling profiles, complete diagnostics and the original manifest. These original scientific outputs are preserved.
- [Extension results](results/revision-20261021/README.md): 30 summary, 10 geometry, 22 comparison and 26 monthly rows, plus the accepted manifest.
- `study_data.py`, `study_core.py`, `study_report.py`, `run_study.py`: original bounded acquisition, issue-time construction, reporting and execution.
- `revision_selection.py`, `run_revision_selection.py`: fixed historical selection and the separately frozen extension runner.
- `test_data.py`, `test_core.py`, `test_report.py`, `test_runner.py`, `test_revision_selection.py`, `test_revision_runner.py`: scientific and runner checks using synthetic cases.
- `build_revision_figures.py`, `test_revision_figures.py`: aggregate-only construction and validation of the two new vector figures.
- `build_original_comparison_figure.py`, `test_original_comparison_figure.py`: aggregate-only restyling and checks for all seven original paired means.
- `build_paper.py`, `build_tex.py`, `test_paper_figure_inventory.py`, `test_paper_metadata.py`, `test_paper_caption_layout.py`: document rebuilding and bounded figure-inventory/metadata checks.
- [Working-paper folder](manuscript/working-paper/): paper, source, structured text, approved figures and document verification.

A scientific `COMPLETE` manifest is separate from source compilation, PDF inspection and remote-file verification. The only published operational-state file required for extension replication is the [sanitized public-freeze receipt](state/revision-20261021-protocol-publication.json), containing public repository metadata. Private operational state, raw observations and origin-level traces are excluded.

## Data identity and access

Use version 2 of the [Net Position Time Series Dataset](https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset), one-hour member `1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv`; the accepted one-file archive has a flat CSV member. The CSV has **1,286,391 bytes**, **18,576 records** and SHA-256:

```
b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa
```

Only `datetime` and `NetPosUsd` enter the calculation. Source timestamps span 5 February 2014 to 24 January 2017. The 18,420 one-hour and 155 forty-nine-hour adjacent gaps remain intact; H counts records, rather than elapsed hours. The timezone and historical field-release convention are unverified. Completed-label timing uses an explicit retrospective issue convention, and overlapping labels remain dependent.

The anonymous one-file route was exercised on 21 October 2026. A separate fresh-cache acquisition accepted the identical CSV and reproduced the original tables/figures byte for byte; see [acquisition verification](results/acquisition-verification.json). This establishes reproducibility on the same source, not another independent market record. The extension used the accepted local cache and made no download.

The observed rights label is “Data files © Original Authors”; raw redistribution permission remains unverified. The repository supplies original code, aggregates, source fingerprints and acquisition instructions, without the source CSV/ZIP or third-party paper PDFs. Access availability and reuse conditions can change.

## Reproduction in the recorded environment

The recorded environment is CPython 3.12.14, NumPy 2.3.5 and ReportLab 4.4.9 on macOS arm64. Document assembly additionally uses pypdf 6.10.0. The two requirement files record the existing versions. Use an environment where these are available; the resource monitor is macOS-specific and stops on unsupported platforms. No software was installed for this study.

After the original comparison was restyled, its exact figure inventory added and caption pagination corrected, the combined suite passed **173 tests**. It included synthetic scientific cases, runner boundaries, aggregate figure checks and document inventory/metadata checks. It ran in 8.087 seconds by unittest's clock; the separate process measurement was 8.369 seconds with child maximum RSS 115,621,888 bytes. These are validation measurements, not financial experiment measurements.

From the repository root:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -m unittest discover -v
```

The explicit anonymous source route also executes the **original** analysis:

```
python3 -B run_study.py --fetch --attempt-dir .scratch/original-replication-01
```

It acquires only the fixed cache `.scratch/data/1hourNetPositionsKaggle.csv`, if absent, with bounded anonymous requests and exact archive/member/hash validation. Existing mismatched input is rejected, never replaced. To run the original study on an independently obtained matching file:

```
python3 -B run_study.py --input /path/to/1hourNetPositionsKaggle.csv --attempt-dir .scratch/original-replication-manual-01
```

The two original commands are alternative source routes; each attempt directory must be new. The `--input` route validates and reads its selected file but does not populate the fixed cache. If you obtained the CSV independently, place the matching snapshot at `.scratch/data/1hourNetPositionsKaggle.csv` before running the extension. Verify the documented 1,286,391-byte size and SHA-256; preserve and investigate an existing mismatched cache rather than replace it.

The extension expects that exact fixed cache, the frozen protocol/specification and the public-freeze receipt. It does not fetch, accept an alternate file or override the frozen menu. Use a new output path:

```
python3 -B run_revision_selection.py --output .scratch/revision-replication-01
```

Both scientific runners write exclusive attempt directories. For the anonymous original example, inspect `.scratch/original-replication-01/public/results/run-manifest.json`; the manual example uses the analogous `original-replication-manual-01` attempt. Original tables and figures are inside that attempt’s `public/` tree. The extension example writes its four CSVs and `manifest.json` directly in `.scratch/revision-replication-01/public/`. These attempt outputs do not overwrite the accepted root `results/` or manuscript figures. Inspect each manifest, its scope and every check before accepting a reproduction. Private diagnostic output is not automatically publication material. The original eight scientific code/test files and original result tables remain unchanged by this revision.

The extension's sole accepted computation recorded **10.307238 seconds**, sampled process high-water RSS **64,602,112 bytes (61.61 MiB)** and a maximum observed **one OS thread over 675 snapshots**. The completed-process measurement displayed **10.35 real seconds** and RSS **64,634,880 bytes**. The original primary calculation recorded 8.02145 seconds and RSS 80,936,960 bytes (77.19 MiB). Different checkpoint scopes and displayed precision are retained in their receipts.

The implementation requests one numerical thread, stops early at 540 seconds or 1.5 GiB, has a 600-second alarm and rejects more than two observed OS threads. Source/download/array sizes are bounded. RSS/thread snapshots are observations with limits, rather than an OS hard memory sandbox or a continuously observed thread maximum.

## Document and figure rebuilding

The current TeX source compiled successfully with the desktop editor's built-in compiler. That interface supplied diagnostics without exporting a standalone PDF. The supplied PDF is independently typeset from the same structured content using ReportLab, then appends the three approved vector pages through pypdf. It is **not an export of that TeX compiler**. Pagination and fonts can differ in an external TeX build. The shared scientific text, explicit equations and approved figure files remain available.

All 17 supplied PDF pages were rendered and inspected. The document audit checked 635 source text/table/caption blocks, font coverage, page character bounds, metadata, reference links and exact embedded figure streams. Two unsupported collection symbols were replaced by explicit English before the accepted build. See the [manuscript README](manuscript/working-paper/README.md) and [verification receipt](manuscript/working-paper/rendering-verification.json).

Document-only commands refuse to overwrite existing outputs:

```
python3 -B build_tex.py --output .scratch/main-rebuilt.tex
python3 -B build_paper.py --output .scratch/paper-rebuilt.pdf
python3 -B build_revision_figures.py --output .scratch/revision-figure-rebuild-01
python3 -B build_original_comparison_figure.py --output .scratch/revision-figure-original-rebuild-01
```

The PDF builder reads only approved text and one of three exact three-figure inventories: original, earlier revision, or current restyled revision. Its body requires the four existing macOS Times New Roman files under `/System/Library/Fonts/Supplemental/`; missing fonts stop the build, and font files are not distributed. All three current standalone vector figures use built-in Helvetica and read only fixed accepted aggregates. The original-comparison renderer pins the original run manifest and paired table; the retrieval renderer pins the separately accepted extension aggregates. These document commands do not recalculate financial experiments. The three original scientific figure files remain unchanged and available. The current first figure restyles all seven original paired means, including the small positive tau=.90 difference, with direct signed values rounded to six decimal USD millions for display.
