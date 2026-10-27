# G1 editorial inventory (read-only)

Base: revision-v12 `8060807`. No manuscript, result, or model code changed.

## Table 2

- Owning native dependency: `submission-v10/generated/v12-data-table.tex`, immutable source `results/v12/descriptives/data-table.tex`; source statistics `results/v12/descriptives/summary.json`; provenance `number-bindings.json` and `metadata.json` in the same result directory.
- Five data-source rows; the hourly FX row currently contains two validation/evaluation periods. To preserve one-line cells at readable print size, use original period dates in the row and put earlier-period dates in the table note. The shared source remains one row, not two. All dates are formatting reductions to YYYY-MM; underlying dates remain archived exactly.
- Panel A columns: source (row identifier), frequency, series/records (compact `1 / 18,576`), unit, sample, validation, evaluation. Record counts per series; complete-peak counts move to a note rather than vanish.
- Panel B convert the existing three-significant-digit display values literally, e.g. `3.95 × 10^4` → `39,500`, `1.6 × 10^4` → `16,000`, `9` → `9.00`, `41` → `41.0`. Do not reround from raw full-precision numbers in a way that changes old rounding. A dedicated unit column repeats USD mn/contracts on every row.
- Before/after render the native table and compare all 45 statistics via Decimal, plus 5 source/row/peak counts and all reduced date endpoints.

## Prose hits

|Term|Visible text/table hits|
|---|---:|
|registered|16|
|frozen|20|
|unverified|1|
|T1/T2/T3|0|
|F or I|0|
|QR33|13|
|QR4|10|
|unused allowance|1|
|readback|1|
|audit|2|
|archive|22|

Nonprinting provenance comments are counted separately and preserved. Font encoding `T1` is technical LaTeX, not a response-design code. URL path components remain byte-identical; displayed link labels are edited. The allowed QR4 occurrence is in the methods table; QR33/QR4 elsewhere are replaced with reader-facing procedure names.

Full per-occurrence lines and SHA-bound statistics are in `editorial-inventory.json`.

## G4 reproduction feasibility (read-only)

- Existing entry point is `notes/v12/REPRODUCING.md`; there is no repository-root REPRODUCING.md. It contains conceptual instructions and v12 commands, but no clean-clone CFTC full re-estimation recipe.
- Eleven official raw ZIPs are already versioned at `data/cftc-tff/raw/` and SHA-bound by `data/cftc-tff/provenance.json`. No download is needed.
- CFTC table rows come from `results/v10/cftc/contract-summary.csv`, `summary.json`, `report-values.json`, and native `generated/v10-cftc-contracts.tex`. Raw ingestion helpers `v10_cftc_data.read_archive` and `select_universe` produce 17 eligible vectors; `v10_cftc_forecast.forecast_cell(position,times,design,window,output)` recomputes the six methods for each W52/W260 cell.
- Original `run_v10_cftc.py prepare/formal` commands are intentionally one-shot and tied to archived output directories and pre-publication historical design object IDs. Running them directly in a clone would overwrite or stop on existing attempts. G4 should call unchanged pure ingestion/forecast helpers into an empty temporary output directory, explicitly record source design bytes and original historical-object prerequisite, and compare every Table 5 value. No code alteration is needed.
- Full 17×2×6 method replay includes delayed wrappers and all candidate fits; forecast_cell output contains method JSONs plus trace arrays. Recompute table scalars through `v10_cftc_summary.summarize`, not by reading saved scores.
- T-bill +50.8% and one panel cell must use original comparison definitions and frozen five-point versus six-point menu identities; v12 diagnostics use different matching, so they cannot stand in for the old primary reproduction. Exact owning script/design remains to inspect at G4.
