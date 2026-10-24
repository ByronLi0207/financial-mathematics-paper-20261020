# Registered v9 instability study

Protocol-only commit: `5decccb0a13ef1969629cfec695dd3459c412c4e`.
The original design, code seal, diagnostic/pilot receipts and timing-only
run plan are retained. No diagnostic, fit, forecast, candidate or random
path was retried. This is not a new real-data forecast evaluation.

## Results to read

- [Qualified diagnostics and full simulation tables](postrun/analysis/report.json)
- [Fifteen diagnostic rows](postrun/analysis/diagnostics.md)
- [All conditional cells](postrun/analysis/simulation-cells.md)
- [N1–N4](postrun/analysis/predictions.md)
- [Across-source QR33 summaries](postrun/analysis/qr33-across-sources.md)
- [Chinese memo](postrun/analysis/research-memo-zh.md)
- [ZIP integrity, complete inventory and F benchmarks](audit/summary.md)
- [Every failed candidate/cell](audit/failures.json)
- [Contradicted premise in the two earlier stationary designs](prior-stationary-reconciliation.md)

The full set of registered source medians is required for the hypotheses.
An unavailable cell has no substituted partial median. Completed-only
descriptions in the long table are labeled and do not replace N2/N3.

## Reporting failure retained

All formal worker tasks ended before the frozen runner's postrun writer
failed on a NumPy integer in `N1.holm_rejections`. The runner's exit status
was 1 at this reporting step, rather than a successful end-to-end exit.
The original complete `summary.json`, original code, units and ZIP remain
unchanged. The original partial `predictions.json` remains intact locally;
its exact bytes are public as
[original-predictions-write.txt](postrun/original-predictions-write.txt).
The [original error](postrun/original-reporting-error.txt) is also retained.

`finalize_v9_archive.py` reads saved receipts and calls the same frozen
pure prediction summarizer, converting NumPy scalars with `.item()` only.
It exclusively created `postrun/`, with no fitting, forecasting, altered
thresholds or rounding. [Provenance](postrun/provenance.json) binds original
and derived hashes. Copies of manifest/diagnostics/summary are byte-identical
to the original files. The report and separate ZIP audit check the results.
This known reporting defect was not patched in the sealed research driver.

## Lossless public archive

The intact `formal/units.zip` and all loose units remain locally. Public
transport uses the byte-for-byte parts and their index in `formal/` because
the complete archive exceeds the browser's per-file upload limit. Rejoin
with `python -B restore_v9_archive.py restore results/v9/nonstationarity/formal/archive-parts.json`; it verifies every part and the whole
SHA before exclusive creation, or verifies an already existing archive
without overwriting it. The original unit-manifest provides the individual
file hashes. No failed or unfinished receipt was removed by packaging.
