# CFTC data helpers — artificial RED→GREEN evidence

Scope: `v10_cftc_data.py`, `test_v10_cftc_data.py`, and this note only. No commit. No network requests, no real CFTC ZIP reads, no actual eligibility/ranking, and no forecast/study execution occurred in this task. All archive bytes were constructed in memory by the tests. Production settings remain in the independently committed `protocol/v10/cftc-design.md` (`acd567c1f58fbe7fbb4194be70ff7bebbdfb2baf`).

## API

- `read_archive(raw_bytes, ownership, design) -> (rows, audit)`: exactly one TXT/CSV payload is decoded in memory; no filesystem extraction. Only the frozen full-date header aliases are cross-checked. Rows retain literal string code/name/exchange/units, ISO position date and Monday week, integer OI/long/short/net and explicit count errors. Missing/invalid/future/inconsistent dates, missing code or malformed required schema raise a dataset-wide `CFTCDataError` (a `ValueError`). Bad counts remain attached to a named code, so no bad row silently disappears.
- Ownership exclusions retain file/payload/record and start/end CSV line pointers, position date and reason. Combined with the caller's hash-bound retained raw ZIP, every exclusion can be reconstructed without copying all original fields into a large JSON file. Audit also records bytes/hash, encoding, headers, raw/retained/excluded counts, invalid-count rows and observed optional report-type markers. No unregistered marker alias or report-type value is invented.
- `select_universe(rows, design) -> dict`: returns `status`, `calendar`, `selected`, `contracts`, `arrays_by_code`, `N`, `before_start_rows`. Full generated Monday calendar ends at the latest legal date/code before numeric/scope eligibility filtering. Identical duplicates and Monday/Tuesday same-week pairs disqualify the whole code; nothing is deduplicated or imputed. Entire known prefixes, stable normalized exchange/units, complete history and ancillary initialization are checked before mean-OI ranking. Common calendar length makes exact integer total OI ordering equivalent to mean ordering, avoiding float-induced ties. Equal totals use literal code order. Fewer than twenty stays fewer; zero is UNAVAILABLE.
- Per-code metadata contains `code`, `eligible`, `selected`, `reasons`, `mean_open_interest`, `observations`, `required_weeks`, `missing_weeks`, `duplicate_weeks`, `exchanges`, `normalized_units`, `name_spans`, `first_position_date`, `last_position_date`. Only selected codes receive arrays of float net positions, actual economic dates and canonical Monday model dates.
- `split_indices(N, H=6)` gives the four frozen inclusive indices and `validation_n=52`, `evaluation_n=260`, `unissued_gap_n=H`. Training eligibility uses the inherited pure `v6_aci.initialization_grid`, including nineteen mature initial scores by default. The model/ancillary functions are never fitted or simulated here.

## RED and GREEN

1. Before creating the production module, ran `python3 -B -m unittest -q test_v10_cftc_data`. It executed 23 test methods and failed as expected because `v10_cftc_data` did not exist; the assertion was `CFTC data module is missing` (52 failure instances including subtests). This was a missing-feature RED, not a dependency/import error.
2. Implemented the bytes-only parser, whole-code selection and exact split helpers. With the pinned project runtime, the artificial test file passed: **23 passed, 36 subtests passed**.
3. Extended the invalid-week regression to include a nonhashable malformed week. It first failed with `TypeError: unhashable type: 'list'`, demonstrating that an identifiable malformed-week record could abort selection instead of disqualifying its code. Fixed the audit counter to count string week keys only while preserving every row and retaining `INVALID_WEEK` for the whole code. No corrected model row is manufactured.
4. Re-ran the artificial file: **23 passed, 40 subtests passed in 0.19 s**, exit 0. Only the existing benign uv warning appeared: `--no-project was provided, but no project was found`.

The test command uses the exact offline dependency versions and thread environment recorded in `notes/v10/baseline-tests.json`, with only `test_v10_cftc_data.py` appended to its pytest arguments. No new packages or system interpreter changes were needed.

## Behavioral coverage

Artificial tests cover canonical net/leading-zero codes; both frozen date aliases and cross-check failure; decode-only cp1252 fallback; fatal dates and missing codes even outside an owned year; retained invalid counts; malformed required schema and duplicate headers; one payload requirement; holiday Monday preservation; ownership pointers; full calendar rather than observed-week union; latest week determined before excluded/invalid-count code filtering; no duplicate resolution; stable exchange and units; entire-prefix exclusion; literal code tie order; common-calendar OI ranking; all-code name/date-span audit; short history; fewer than twenty; empty/zero eligible outputs; no input mutation; invalid week disqualification; exact 52/260/6 split and endpoint maturity; JSON-native outputs.

## Full-suite verification

The pinned complete test suite passed: **1596 passed, 1130 subtests passed in 118.85 s**, exit 0. Wrapper start UTC was `2026-10-24T22:52:18.334475+00:00`; end UTC was `2026-10-24T22:54:17.726817+00:00`; measured wrapper elapsed time was `119.388763542 s`. The exact command, thread overrides, returned output and scope are retained in `notes/v10/cftc-pre-run-tests.json`.

This is the root-authorized unified E2 pre-run full suite, not a second study execution. All four new CFTC test files (data, driver, forecast, summary) existed before its default full-directory collection started. Their mtimes are recorded in the JSON. The quiet pytest output does not give per-node collection timestamps, so no exact per-node time or atomic at-collection code snapshot is asserted. Any later implementation change requires focused rechecking; root will run the next full suite at E7.

The focused and complete checks were run with the existing offline pinned runtime. The only stderr warning was the pre-existing uv `--no-project` notice; there were no test failures.

## Delivered module/test SHA-256

- `v10_cftc_data.py`: `97ee191ba4e6bc81a48a4bf9061f44bf53dd8793fc639967b86df5a1526afd78`.
- `test_v10_cftc_data.py`: `4e5f0ca1648c8c611a43ee16ed2c541f64fca8e868c02712c82b82719a3fc578`.
