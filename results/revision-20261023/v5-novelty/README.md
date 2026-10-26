# V5 novelty analyses: immutable exploratory results

All newly computed diagnostics are **post-result / exploratory**. Original primary comparisons and archived results are unchanged. No stochastic selection, retuning, imputation, fallback fit or outcome-based subset choice is used.

`analysis-design.md` in `notes/revision-v5-novelty/` was frozen before the first financial-data fit; its SHA-256 is bound in each new financial-data receipt. `v5_analysis.py` is the source script and `test_v5_analysis.py` its tests. Test-first failures, the one pre-data resource-probe failure, and its tested repair remain in `attempt-history.txt`.

## Additive bridge

The original FX H6 comparison is bridged through matched-history frozen F. All additive percentages below use the original rolling F W720 mean-loss denominator. The combined history/update bridge is descriptive, with no causal identification of its two components.

- Original R loss: 441774.03703851684 USD.
- Matched F loss: 452692.9834478481 USD.
- QR loss: 385844.8854897607 USD.
- Combined history/update bridge: 2.47161343 percentage points of R.
- Estimator bridge: -15.13173984 percentage points of R.
- Total: -12.66012641 percent of R.
- Separate matched-reference percentage: -14.76676255%; this has a different denominator and must not be added to the preceding percentages.

## Deliberate training-label leakage

Clean training ends at r−H; deliberately illegal oracle training ends at r. Each original refit therefore has H labels unavailable at its fit time. First, floor-middle and last complete refit blocks were chosen solely from the original clock interval. Both modes and all methods share the selected issues. These are clock slices, not the full evaluation record, and no inferential p-value is claimed. Negative changes mean apparently optimistic loss, while positive changes mean deterioration.

| Source | Issues | Method | Clean loss | Oracle loss | Change % | Clean/oracle breaches |
|---|---:|---|---:|---:|---:|---:|
| fx_hourly | 72 | QR | 254757.369210 | 254920.239898 | +0.06393169 | 2/2 |
| fx_hourly | 72 | KNN | 294045.707972 | 297278.423087 | +1.09939204 | 2/3 |
| fx_hourly | 72 | F | 259673.056354 | 259673.056354 | +0.00000000 | 0/0 |
| nyfed_weekly | 39 | QR | 3128.675515 | 2083.734631 | -33.39882577 | 5/6 |
| nyfed_weekly | 39 | KNN | 1759.683333 | 1713.746154 | -2.61053672 | 0/0 |
| nyfed_weekly | 39 | F | 1615.698718 | 1640.832051 | +1.55557054 | 2/2 |

The observed distortion has mixed signs; this demonstration does **not** establish that leakage always improves apparent accuracy. The original Treasury QR example simultaneously lowers pinball loss and increases strict breaches. All results, including unchanged or adverse leakage effects, remain visible.

## Motivating window

`motivating-window-final.json` is the final-code receipt. The original downloaded-vintage NYFed bill series gives its first qualifying original evaluation origin 408: 2021-01-27, horizon 6 sampled records. The issued clean historical F report is 73139 USD millions, the sampled peak is 74397, and the absolute endpoint is 48144. Dates denote economic dates, not original public release timestamps. This deterministic illustration is not evidence of typicality, a new holdout, or an intrarecord peak. The earlier `motivating-window.json` is retained with its actual pre-resource-repair code hash; its scientific fields agree.

## Verification and resources

- fx_hourly: 0.394082 seconds, peak RSS 63537152 bytes, maximum observed native threads 1.
- nyfed_weekly: 0.265573 seconds, peak RSS 41500672 bytes, maximum observed native threads 1.

`independent-readback.json` verifies clean forecasts against the hash-pinned original private trace artifacts: six source/method matches and 36 scalar checks, all exactly equal; it also verifies the additive bridge with rational arithmetic and reconstructs the earliest motivating report with direct sorted order statistics. The verifier requires the private original reproduction cache and never publishes it. `pytest-green-full-output.txt` contains the complete final test run.

## Reproduction without overwriting archived outputs

Use the existing runtime with numerical-thread environment variables set to 1. Supply source CSVs at the original `study-spec.json` locations and verify their original hashes; FX raw data is intentionally excluded. Run the normal CLI only in an empty output location. For an existing checkout, this wrapper selects a new output directory without editing the script:

```python
from pathlib import Path
import v5_analysis as v
v.OUT = Path('.scratch/v5-independent-replay')  # choose a previously unused directory
v.main(['decomposition'])
v.main(['motivating-window'])
v.main(['leakage', '--source', 'fx_hourly'])
v.main(['leakage', '--source', 'nyfed_weekly'])
```

All output opens are exclusive. Compare scientific fields, not timestamps, measured timing, or code-identity changes introduced by later wrappers. Do not delete earlier outputs or claim that this deliberately illegal control is a deployable method.
