# G4 independent reproduction plan (not executed)

Prepared from the v13 source tree after G1; actual clone is deferred until G3 is completed and committed. No model, validation, scoring or financial computation was launched during this preparation.

## Fixed scope and inputs

1. Clone the current `revision-v13` commit into a newly allocated temporary directory using `git clone --no-local --no-hardlinks --single-branch --branch revision-v13 <current-repository> <new-directory>`. Record original and clone HEAD/tree, clone creation time, and an empty initial untracked inventory. Do not clone or enter the old v3 directory.
2. All source and saved result comparisons come from the clone. CFTC forecasting inputs are reconstructed from **all eleven original raw ZIPs** under `data/cftc-tff/raw/`; never use `results/v10/cftc/sources/*.npz`, old trace arrays, private caches or v12 prediction segments as inputs.
3. The Treasury-bill raw CSV is already versioned at `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv`.
4. The fixed panel check is `PDPOSCS-TOT`, H6, W52, original 277 evaluation origins 405..681. Its original CSV is not in the public repository. Supply the **raw** 707-row CSV from `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSCS-TOT.csv`, 24,713 bytes, SHA256 `169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade`. This additional raw-only input is explicitly disclosed; it is not an intermediate or derived vector. Align to the versioned bill date grid with the unchanged `round2_panel_sources.align_source`.
5. Supply the private FX original CSV through `V13_FX_RAW`, verify its `study-spec.json` bytes/SHA, and do not read its previous models/caches. No FX forecast is part of G4. No source acquisition or download is allowed.
6. Use an isolated uv environment with numpy==2.3.5 and all numerical thread variables set to 1, plus pypdf for page/text inspection. Outputs go exclusively to a fresh path under the temporary clone, e.g. `.scratch/v13-independent/`. The original repository is read-only except the final G4 notes and documentation.

## A. Compile from native source

From the fresh clone, run the existing Tectonic binary on `submission-v10/main.tex`, output to a new temporary directory, keeping logs and auxiliary files. This compiles native TeX and the clone's transitive figure/table dependencies, not a saved PDF. Capture command, elapsed time, return code, page count and unresolved/overfull/duplicate-reference diagnostics. The main source is the wrapper; compiling a differently named old manuscript is not equivalent.

## B. CFTC Table 5: all 17 contracts × two histories × six methods

Table 5 owner: `submission-v10/generated/v10-cftc-contracts.tex`. Its 170 printed percentages are five non-reference columns (ordinary intercept-only, four-feature regression, full regression, calibrated history, calibrated regression) at each W52/W260. **There is no three-penalty CFTC regression in this table.** Both regressions use the six-point menu. The corrected historical rule is the denominator and is re-estimated too, giving all 204 method cells.

Read the JSON object embedded in `protocol/v10/cftc-design.md`, attach the unchanged JSON objects from `cftc-ingestion-clarification.md` as `ingestion_clarification` and `cftc-count-notation-clarification.md` as `count_notation_clarification`. Check raw ZIP bytes against `data/cftc-tff/provenance.json` before parsing. Call unchanged functions:

```python
from v10_cftc_data import read_archive, select_universe
from v10_cftc_forecast import forecast_cell
from v10_cftc_summary import summarize
rows = []
for ownership, raw in ordered_pinned_raw_archives:
    parsed, audit = read_archive(raw, ownership, design)
    rows.extend(parsed)
universe = select_universe(rows, design)
assert universe['selected'] == original_selected_literal_codes
records = []
for code in universe['selected']:
    arrays = universe['arrays_by_code'][code]
    for window in (52, 260):
        outcome = forecast_cell(
            np.asarray(arrays['position'], dtype=float),
            np.asarray(arrays['model_dates'], dtype='datetime64[us]'),
            design, window, new_output / code / f'W{window}',
            checkpoint=wall_limit_checkpoint)
        records.extend(dict(row, code=code, window=window)
                       for row in outcome['methods'])
recomputed = summarize(records, universe['selected'], design)
```

The `arrays_by_code` values come only from ZIP parsing. Original `run_v10_cftc.prepare/formal` commands must **not** be used: they are one-shot writers bound to the old output directories and three original local design commits, which a public clone may not contain. Calling their pure helpers into a new directory preserves these guards and changes no source code.

Compare all 204 complete/status identities, 204 absolute F/method mean losses, strict breach counts, selected penalties and calibration parameters to `results/v10/cftc/summary.json`; retain maximum full-precision difference and exact-equality counts. Parse each printed Table 5 decimal-pair cell and require exact equality of all 170 formatted values. If numerical differences occur, report them rather than altering solvers, settings or archived numbers. Do not retry failed methods.

## C. Treasury-bill original primary and one original panel cell

Treasury bill: use `conditional_sources.load_source` with the frozen bytes/SHA in `protocol/revision-20261022/study-spec.json`. Construct `StudyConfig(6,260,13,6,26,604800)`. Refit all **three** original full-regression candidates `(0.001,0.01,0.1)` on validation origins 329..380 using unchanged `conditional_study.conditional_forecast`, score with `score_predictions/summarize_scores`, choose with `select_parameter(..., expected_count=52)`, then forecast selected penalty on evaluation 405..681. Recompute corrected fixed historical F from `historical_forecasts(...)['frozen_F']` or `empirical_headroom.predict(...)['F']`, preserving the exact inherited arithmetic. Compare the +50.8% displayed primary, selected penalty, every saved score summary and hit counts to original `evaluation-nyfed_weekly-h6-w260-QR.json`, `references-nyfed_weekly-h6-w260.json`, `evaluation-summary.csv` and `paired-comparisons.csv` (verify owning paired filename). Expanded-menu diagnostics cannot replace this original primary.

Panel: hash-check raw source, align its dates to the bill grid, then call the same original full-regression pipeline at H6/W52. Recompute all four original cell methods if feasible: corrected historical F; endpoint plug-in (`round2_levy.predict`); original full regression (three penalties); original four-feature regression (`parsimonious_v3.features4/forecast`, five penalties). Whole-candidate eligibility and original exact tie conventions must remain those of the original cell, not later v12 strictness. The original `legacy_round2_panel_run.py` establishes the original cell semantics but its writer entry point must not be called. Compare the entire scalar `records` inventory and all candidates against `results/revision-20261023/round2/panel/cells/PDPOSCS-TOT-h6-w52.json`.

A failure in one task does not justify reading a saved numeric trace as a forecast. Keep the failure and list the missing prerequisite.

## Documentation gaps to repair after the actual check

- Repository root has no REPRODUCING.md; `notes/v12/REPRODUCING.md` mainly documents one-shot v12 study runners and final checking, not the requested re-estimation. Add a root entry point referencing the actual clean-clone recipe and retained version-specific instructions.
- State that CFTC official raw ZIPs are already versioned; do not tell users to redownload.
- Explicitly distinguish the 170 displayed relative percentages from 204 absolute method cells and their historical denominator.
- Document original three-/five-/six-point menu identity separately; original bill +50.8% is not v12 QR33.
- Document both external raw inputs, their provenance, bytes and SHA; FX and panel raw availability differs from intermediate prediction availability.
- Explain missing original historical Git objects only for old archival guards/tests; do not alter them or describe a clean public clone as passing the full historical suite without those prerequisites.
- Provide reproducible raw-to-forecast helper commands into new output directories and a numerical reconciliation report, with actual timings.
