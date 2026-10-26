# WP4 independent readback development

The audit uses only NumPy and the Python standard library. It never imports production resampling, forecasting, score, or aggregation helpers, never fits QR, never calls a new statistical test, and never changes input files. All development used constructed scalar/array/CSV/NPZ fixtures in temporary test directories. No accepted raw FX CSV, private formal array, or running formal result was read during development.

## Actual schema coordination

The runner and daily-primitives authors confirmed these fields and the auditor then read their source implementations (without running them):

- Public `manifest.json`, `inventory.json` (12 rows), `summary.json` (cells/contrasts/classifications), `classification.json`, `study-termination.json`, `summary.csv`, and `contrasts.csv`.
- Four cell folders `cells/W52_H6`, `W52_H24`, `W260_H6`, `W260_H24` with `worker-source.json`, `cell-geometry.json`, parent/worker receipts, and public trace fingerprints.
- Private `daily-series.npz`: position/times/selected_indices/selected_raw_times. Positions are float64, selected indices int64, clocks datetime64[us].
- Private candidate/evaluation traces: origins/refit_indices/capacity/peak/floor/pinball/strict_breach. The exact filename stem is `<cell>_<method>_validation-<menu-index>` or `<cell>_<method>_evaluation`; public same-stem `.trace.json` binds NPZ SHA-256 and origin count.
- Candidate scalar means/counts, original distinct QR33/QR4 menus and tie/failure policies, exact fit diagnostics and maturity summaries. Legitimate interrupted INELIGIBLE selection receipts remain FAILED methods with no selected penalty.
- Procedure-specific classifications have planned/complete/missing counts, historical/conditional/tie counts, all four comparison cases, and literal-hourly descriptive counterexamples.

The actual entry point refuses a live study before reading source/private arrays. It requires termination with `all_workers_terminated=true` and complete summary files. Outputs are exclusive-create, never overwrite, and contain aggregate counts, scalar comparison results and hashes only; selected-index vectors, raw positions and per-issue values stay private.

## Independent checks

- Pin the source by exact bytes/SHA/row count and fixed five-column header; independently parse strictly ordered source-naive microsecond timestamps.
- Select each nonempty source day's last row independently via a forward day-to-last-index mapping, set issue time to ended-day23:59:59.999999, retain partial boundary days, leave empty days absent, and verify every private mapping array and all four public canonical fingerprints against the same source.
- Use the exact original little-endian byte vectors and `v8-daily-v1` plus zero-byte combined prefix; verify all cell fingerprints are identical to the independently reconstructed daily record.
- Keep validation329–380 (52 origins), evaluation405 through n−25, common complete-H24 tail, mature history, refit13 and declared NA cases. No truncation, moved cut, fill or sample repair.
- Independently compute the sampled peak including current, floor, tau19/20 pinball and strict breach counts/rates from each saved complete trace. Independently replay only deterministic F with corrected own-anchor headroom rank and frozen refit blocks. QR capacity vectors are read and scored, never refitted.
- Check every completed candidate and evaluation's trace fingerprints, full issue/refit grids, aggregate metrics, fit maturity/window and saved convergence conditions. Available traces surviving failed reports are checked without relabelling those procedures complete.
- Preserve all12 method and32 candidate slots, unavailable denominators and original selection policies. Independently rebuild all eight contrasts and each regression's own four-comparison classification; another regression's failure cannot contaminate it.
- Compare JSON and CSV payloads; verify current source/code/protocol hashes and the actual design commit predates run start. Rehash input files/arrays after readback.
- Verify actual resource receipts/checkpoint samples, observed threads<=2, RSS<=2GiB, worker600/global1800-second bounds plus a fixed5-second receipt/termination allowance. Missing measurements become UNVERIFIED rather than declared-budget stand-ins. Process COMPLETE is not method success.

This is deterministic saved-result arithmetic/provenance verification, not independent-dealer validation, prospective validation, or independent QR replication. Old empirical result archives are outside this checker; it does not claim to have re-audited them.

## RED/GREEN evidence

Initial command, actual exit1:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with numpy python -B -m pytest -p no:cacheprovider test_v8_wp4_audit.py -q
12 failed in 0.12s
```

All12 initial failures were explicit NotImplementedError assertions after the module stub existed. Full output/receipt: `wp4-audit-unit-red-output.txt`, `wp4-audit-unit-red-receipt.json`.

An added constant-mean fixture then exposed the original constant-preservation policy before correction:

```text
FAILED test_v8_wp4_audit.py::test_scalar_score_mean_preserves_exact_constant_as_declared_in_original
assert 0.10000000000000002 == 0.1
1 failed, 12 passed in 0.15s
```

The independent scorer was corrected to preserve exact constant loss vectors, matching the stated original arithmetic instead of changing its tolerance. No scientific result was observed or altered.

The constructed whole-bundle test also initially demonstrated absent CSV-value checking: changing a fixture CSV status token was not detected (`1 failed, 13 passed in0.25s`). Exact saved CSV serialization checking was added. A separate test-only privacy assertion was corrected to reject actual vector keys rather than allowed hash-key substrings.

Final command, actual exit0:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest --with numpy python -B -m pytest -p no:cacheprovider test_v8_wp4_audit.py -q
..................                                                       [100%]
18 passed in 0.35s
WARN `--no-project` was provided, but no project was found
```

Final full output, command, UTC, exit and SHA: `wp4-audit-unit-final-output.txt`, `wp4-audit-unit-final-receipt.json`.

The whole-bundle fixture contains a hand-constructed monotone source of500 rows, four independently checkable F traces, unavailable regressions,12 method slots and32 unavailable candidate slots. It is not an AR/GARCH draw, financial simulation, QR fit or actual source result.

The CLI `--help` was executed successfully without source/result reads.

## Root invocation after termination and summary

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy python -B notes/revision-v8/audit_wp4.py --output notes/revision-v8/wp4-independent-audit.json
```

Use a new output name if a prior receipt exists. FAIL/UNVERIFIED results remain evidence; do not change source numbers, parameters or sample boundaries to force PASS.
