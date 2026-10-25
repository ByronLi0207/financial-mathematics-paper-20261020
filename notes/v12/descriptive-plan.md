# F4 data-description table: execution plan

Prepared 2026-10-25. This note and the new script/tests prepare the analysis;
no actual financial descriptive statistics are computed in this subtask.
The root agent will inspect and explicitly run the script after F3 finishes.
No model fit, forecast score, source download, source write or Git command is
part of this script.

## Gate and entry point

Run `report_v12_descriptives.py --run` only after
`results/v12/tau/runtime.json` contains `experiment=F3` and a valid
`completed_utc` timestamp not earlier than `started_utc`. The existing driver
does not emit a status field. If a status is present, it must be `COMPLETE`.
This gate requires completion of the formal F3 attempt, including its retained
failures/resource omissions; it does not silently require every model to win
or every planned cell to finish. The script checks the gate before parsing
financial files or creating the output directory.

## Matched descriptive sample and statistics

Use the 31 pinned existing sources exposed by `v12_inputs.source_inventory`
and `load_series`, plus the deterministic daily transform of the same FX file.
Every size/SHA check remains in the input layer. Daily FX reuses
`v8_daily_fx.resample_closed_days` unchanged: last observed record in each
nonempty source-naive calendar day, with an issue time at that day's end;
there is no timezone conversion, missing-day fill, sorting or weekday filter.
Check the full resampling metadata/fingerprints against the existing archive
before computing daily statistics.

For each series of N aligned observations and H=6, use exactly the N-6 issue
origins `0..N-7`. For these same origins calculate B=|N_t|,
Y=max(|N_t|,...,|N_(t+6)|), including the anchor, and Z=Y-B. No end-of-series
partial targets are included. Report stable arithmetic mean, sample standard
deviation with denominator m-1, and the lower empirical/inverted-CDF 95th
percentile: one-based rank ceil(95*m/100), without interpolation. All nine
statistics therefore use the same m observations within a series.

FX hourly and daily values are displayed in USD millions, dividing native USD
by 1e6 before reporting. Treasury bills and the NY Fed panel are already in
USD millions. CFTC retains native contract counts, with no conversion into a
common dollar exposure.

Keep every source's native and display statistics. For the twelve-series NY Fed
panel and seventeen-contract CFTC panel, each displayed statistic is the median
of that statistic across the within-series summaries. These are nine separate
medians, not statistics of a pooled exposure vector. All counts and the related-
series/heterogeneous-contract-unit caveats remain explicit.

## Existing split/date sources checked read-only

* Hourly FX original: validation 10463–11902, dates 2015-10-08 00:00 through
  2015-12-30 23:00; evaluation 11927–18551, 2016-01-01 00:00 through
  2017-01-23 00:00. Existing early-2015 comparison: validation 7535–8974,
  2015-04-21 00:00 through 2015-07-13 23:00; evaluation 8999–10438,
  2015-07-15 00:00 through 2015-10-06 23:00. Both periods have already been
  inspected. Sources: `protocol/v12/tau-design.md` JSON and
  `protocol/supervisor-20261023/r6-design.md` Section 2. The script maps the
  stored indices directly to the verified source clock.
* Daily FX: `results/revision-v8/wp4/readout-bindings.json#/periods` records
  validation **2015-02-24T23:59:59.999999** through
  **2015-04-24T23:59:59.999999**, evaluation
  **2015-05-24T23:59:59.999999** through
  **2016-12-27T23:59:59.999999**. The archived daily N is 930; common evaluation
  indices are 405–905, 501 origins. Validation indices are 329–380. The old
  protocol intentionally retains the common H24 evaluation endpoint even for
  H6. Sources: `protocol/revision-v8/wp4-daily-fx-design.json`,
  `results/revision-v8/wp4/cells/W260_H6/cell-geometry.json`,
  `results/revision-v8/wp4/cells/W260_H6/worker-source.json`, and the readout
  bindings. The script checks the archived dates and resampling fingerprints.
* Treasury and the twelve aligned panel series use validation 329–380,
  2019-07-24 through 2020-07-15, and evaluation 405–681,
  2021-01-06 through 2026-04-22. The aligned N is 706; panel raw N is 707.
  Sources: F1 geometry, original Treasury specification and the saved panel
  selection manifest. The extra raw 2026-10-14 panel row is not included.
* CFTC uses validation 553–604, actual dates 2020-08-11 through 2021-08-03,
  and evaluation 611–870, 2021-09-21 through 2026-09-08. N is 877. Source:
  `results/v10/cftc/splits.json`; the script verifies both the Monday model
  clock and separately retained actual economic dates.

The N-6 descriptive origin counts implied by existing N metadata are hourly FX
18570, daily FX 924, Treasury/panel 700 per series, and CFTC 871 per contract.
These are full-series descriptive samples; the original validation/evaluation
grids are reported as design metadata, not used to select the descriptive sample.

## Outputs when explicitly invoked

The new `results/v12/descriptives/` directory must not already exist. Preserve
all source rows in `rawstats.json` and `rawstats.csv`; export the five displayed
rows in `summary.json` and `summary.csv`; save exact source dates/counts,
splits, units, source hashes and definitions in `metadata.json`.

`data-table.tex` contains one table with two panels: five metadata rows, then
five rows with nine numeric statistic columns. The labels describe the data;
there are no forecasting-method codes. The table is prepared for portrait
layout with short date stacks and three significant digits; root-owned final
compilation/render inspection is still required.

`number-bindings.json` binds every numeric JSON leaf and every numeric table
cell/date display to the saved source file's SHA-256, JSON pointer and a
definition/formatting rule. Input protocol/archival receipt hashes are retained
in metadata. Bindings do not treat related series as independent evidence.

## Toy verification scope

Use only constructed arrays to check H6 anchor inclusion, the shared complete
origin sample, sample SD, lower empirical p95, USD-million scaling and the
median of within-series statistics. A temporary-root gate test must fail before
financial input/protocol access when F3's completion record is absent. The
subtask does not launch the real CLI or create real descriptive outputs.

## Prepared implementation verification

The test-first red run observed five expected assertion failures while the new
module was absent. The final scoped run passed **5 tests in 0.14 seconds**
using the offline uv environment with NumPy 2.3.5 and pytest 9.1.1, bytecode and
pytest cache creation disabled. Both new Python files passed AST parsing.
No actual financial source was parsed and no real descriptive output was
generated. Final table rendering and real-output checks remain root-owned.

Read-only date/geometry source hashes at preparation:

* `results/revision-v8/wp4/readout-bindings.json`:
  `5fcb1a695be76914abb62485fddb4b7a8c3f58ea94e2d607449ad6bd32d88e7b`.
* `protocol/revision-v8/wp4-daily-fx-design.json`:
  `e1c00c57dea3c4a03e839bda34fef60046042876675d3612f005cddab277e5e3`.
* `results/revision-v8/wp4/cells/W260_H6/cell-geometry.json`:
  `6b4340f6f0066440f5b7d30516c9b26d39ba4595fdf786f27b0297217903eacb`.

Prepared code hashes:

* `report_v12_descriptives.py`:
  `1cd732784f666b78a53924ad1c16c3bd07a7ef400b01933cc8bd946c08bc09b6`.
* `test_v12_descriptives.py`:
  `c3610e42ae492a0584b330eaf52494cdb94dc83af6cd28d3ee85bf1756e5e526`.
