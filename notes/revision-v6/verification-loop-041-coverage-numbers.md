# Verification loop 041 — five current Table 5 coverage result cells

Status: **PASS within the saved-output transcription and display-format scope.** All five seeded cells match the exact archived CSV fields after the actual manuscript formatter. No conclusion-changing discrepancy was identified in this bounded trace. This is verification of existing outputs, not independent replication, recalculation of coverage statistics, reference-distribution validation, or certification of calibration.

## Scope and frozen selection

The inspected current main document is `submission-jof/manuscript-content.json`, Section 7 “Scoring and calibration (RQ2)”, zero-based `sections[6].blocks[0]`, current Table 5. It contains seven report rows and five result columns: `k/n`, `POF p`, `Ind p`, `CC p`, `DQ p`. All 35 cells are actual numerical results; report names, table numbers, horizons, windows and other navigation/parameter identifiers are outside the sampling frame. There is no rate column in this displayed table. Each `k/n` display is treated as one result cell; its numerator and denominator were not split into additional sampled claims, and no rate was computed.

The exact five identifiable prior loop009 row/column identities were read from `notes/revision-v6/verification-loop-009-numbers.json` and excluded:

- `Table5|FX QR H6|POF p`
- `Table5|FX matched F H6|Ind p`
- `Table5|FX QR H24|Ind p`
- `Table5|FX QR H24|CC p`
- `Table5|FX legacy S H24|Ind p`

The remaining 30 cells were ordered by displayed row, then by the five result columns in the order above. Seed `2026102341` was fixed and applied with `random.Random(2026102341).sample(range(30), 5)`, producing zero-based eligible-frame indices `[5, 21, 26, 29, 13]`. Selection order is retained below. The full ordered frame, exclusions, displayed values and draw are frozen in `verification-loop-041-coverage-numbers-selection.json`, SHA-256 `4e14512ca6b5252520f4b84f56fae94f0e36c43cdf903da6fa66c8c4b32edd04`.

The selection was written at `2026-10-23T22:36:20.113753+00:00`, before opening `coverage.csv` for loop41. The frame and its displayed manuscript values were visible before the draw; no claim is made that these values were previously unseen in this long-running project. Prior loop009 was used only to identify exclusions, not as evidence that the current numerical displays are correct.

Observed HEAD at selection and at source readback: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`. Evidence readback ended at `2026-10-23T22:36:56.617086+00:00`. Every input in the fingerprint table below was read from current bytes and independently compared byte-for-byte with its blob at this HEAD; all matched. No assumption was made that unrelated working files were clean.

## Exact saved-field traces

The owner is `results/revision-20261023/inference/coverage.csv`. CSV line numbers include its header as line 1; each selector below matched exactly one saved row. The table mappings are the literal `labels` and exact `next(...)` key comparison in `v3_additions.py:23–27`, not a match on rounded displayed values.

The actual p-value formatter in `v3_additions.py:12` is `'NA' if x in (None,'') else format(float(x),'.3g')`. The actual hit-count cell constructor in line 27 is `r['hits']+'/'+r['n']`. Only these display operations were applied. No rate, likelihood ratio, p-value, covariance, test or statistic was recalculated.

| Draw | Actual result-cell identity | CSV line | Exact saved row selector | Exact saved field token(s) | Formatted / concatenated result | Equals current JSON and TeX |
| --- | --- | ---: | --- | --- | --- | --- |
| 1 | `Table5|FX rolling F H6|POF p` | 26 | `source=fx_hourly, horizon=6, window=720, method=rolling_F` | `pof_p="0.8067032386212847"` | `0.807` | yes |
| 2 | `Table5|Treasury QR H6|POF p` | 17 | `source=nyfed_weekly, horizon=6, window=260, method=QR` | `pof_p="0.004126046248434382"` | `0.00413` | yes |
| 3 | `Table5|Treasury F H6|POF p` | 68 | `source=nyfed_weekly, horizon=6, window=260, method=frozen_F` | `pof_p="0.1986410814587244"` | `0.199` | yes |
| 4 | `Table5|Treasury F H6|DQ p` | 68 | `source=nyfed_weekly, horizon=6, window=260, method=frozen_F` | `dq_p="8.52462376410396e-05"` | `8.52e-05` | yes |
| 5 | `Table5|FX QR H24|k/n` | 11 | `source=fx_hourly, horizon=24, window=2880, method=QR` | `hits="21"`; `n="265"` | `21/265` | yes |

The current TeX keeps the same complete rows at `submission-jof/manuscript.tex:273`, `:275`, `:277` and `:278`; the selected Treasury F POF and DQ cells share line 278. The string `8.52e-05` is retained as emitted by the actual three-significant-digit formatter. `21/265` is direct string concatenation of saved `hits` and `n`, not a division or a derived rate.

The immutable v5 manuscript snapshot has one table at `sections[6].blocks[0]` with exactly the current headers and rows; its caption calls it Table 4. `v6_submission.py:23–32,44–48` maps that caption to current Table 5 while preserving these numerical row strings. The current block records `_generator="v6:block:manuscript:6:0"`. Its canonical whole-block SHA-256, using UTF-8 JSON with sorted keys and separators `(',', ':')`, is `4c7d79f23bbbeba2b8e52a18b9eae10dbdb5f493abc20e36214dfee4074774f9`. This composition identity was checked statically; no generator, compilation or PDF rendering was run.

## Statistical identity and limitations retained

`run_v3_inference.py:59–61` owns the existing strict hit definition `peak > capacity`. It sends only `hits[grid]`, with `grid=np.arange(0,len(hits),h+1)`, to `coverage_tests`; it separately sends the full hit sequence and issued capacity to `dq_hac`. The saved `first_origin` anchors the grid. These static lines were read, never executed, and no origin-level vectors were opened.

The saved scope fields for the selected rows are:

| Selected report | Method / history | Saved grid stride | Saved first origin | Saved grid hits / n | Saved independence status / boundary | Saved DQ status / n / df / bandwidth |
| --- | --- | ---: | ---: | --- | --- | --- |
| FX rolling F H6 | `rolling_F`, W=720 | 7 | 11927 | 49 / 947 | `OK` / `False` | `OK` / 6615 / 6 / 10 |
| Treasury QR H6 | `QR`, W=260 | 7 | 405 | 7 / 40 | `OK` / `False` | `OK` / 267 / 6 / 6 |
| Treasury F H6 | `frozen_F`, W=260 | 7 | 405 | 4 / 40 | `BOUNDARY_REFERENCE` / `True` | `OK` / 267 / 6 / 6 |
| FX QR H24 | `QR`, W=2880 | 25 | 11927 | 21 / 265 | `OK` / `False` | `OK` / 6597 / 6 / 24 |

These are direct saved fields, not newly derived sample counts. The FX rolling reference remains the original rolling F with W=720; it is not the matched frozen F W=2880 report. The Treasury F is the named frozen F with W=260, matched to the Treasury QR history in this table. No comparator was substituted and no adverse Treasury finding was changed.

The selected Treasury F DQ p-value is the saved full-origin HAC diagnostic after the instrument-lag rows are omitted, with saved `dq_n=267`; it is not a diagnostic on the 40 sparse grid observations. `inference_tests.py:110–122` statically defines the intercept, matured hit lags H+1 through H+4, and standardized issued-capacity instrument, together with rank/covariance failure statuses. The selected POF values and the selected hit-count cell belong to the fixed first-origin-plus-j(H+1) grid. The grid avoids overlap of those target paths; it does not remove shared training dependence or establish an independent sample.

All Table 5 p-values are raw working-reference diagnostic outputs, not Holm-adjusted ranking p-values. `v3_additions.py:27` reads `pof_p`, `ind_p`, `cc_p`, `dq_p` directly from coverage output; the Holm lookup in the same file concerns a separate paired-loss table. `protocol/revision-v6/common-contract.md:11–13` explicitly retains this distinction.

This archived coverage table retains the old CC convention: full-grid POF LR plus transition-independence LR (`inference_tests.py:97,104–107`). It must not be relabeled as the later v6 transition-conditional CC likelihood. No CC cell happened to be selected in this draw; describing its identity here does not add a sixth numerical trace. Likewise no independence cell happened to be selected. Both columns remained eligible except for the explicit loop009 exclusions.

The Treasury F row's saved `BOUNDARY_REFERENCE` flag pertains to its transition diagnostic, with the saved row retaining `n11=0`; it is not an NA code and does not invalidate the string trace, while it does preserve a boundary-reference qualification. Conversely an unidentified transition-state row leaves independence/CC values empty, and singular/nonpositive DQ covariance leaves DQ empty with a reason. The display formatter maps empty values to `NA`; none of the five selected cells was empty. NA is not an observed p-value of 1, and any separate multiplicity bookkeeping convention must not be imported into these cells. Small Treasury grids, target atoms, dependence and post-inspection reuse still limit the p-value interpretation. Matching saved values cannot establish those reference assumptions, population coverage, or prospective validation.

## Actual read-only operations and source fingerprints

The operations were bounded JSON/CSV reads; SHA-256 of existing files; byte comparisons with `git show HEAD:<path>`; `git rev-parse HEAD`; a working-tree inventory; and static line reads/searches. The relevant actual line-read commands were:

```text
nl -ba v3_additions.py | sed -n '1,100p'
rg -n 'coverage|pof_p|dq_p|def .*dq|HAC|grid|strict|transition|Holm|holm' run_v3_inference.py inference_tests.py
nl -ba inference_tests.py | sed -n '72,128p'
nl -ba run_v3_inference.py | sed -n '49,66p'
nl -ba v6_submission.py | sed -n '1,61p'
nl -ba v6_submission.py | sed -n '148,170p'
nl -ba submission-jof/manuscript.tex | sed -n '264,283p'
nl -ba protocol/revision-v6/common-contract.md | sed -n '9,13p'
```

The in-memory standard-library readback selected CSV rows by the four exact keys shown above, required selector uniqueness, and compared the saved-field display operation to the frozen manuscript string. Source modules were not imported or run. Hashes were computed from `Path.read_bytes()` with `hashlib.sha256`; HEAD equality compared these bytes with `subprocess.check_output(['git','show','HEAD:'+path])`. The seeded sampling and string formatting are the only numerical operations beyond count/inventory bookkeeping; no inference function was invoked.

| Current inspected input | Bytes | SHA-256 | Equals observed HEAD blob |
| --- | ---: | --- | --- |
| `submission-jof/manuscript-content.json` | 196850 | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` | yes |
| `submission-jof/manuscript.tex` | 78822 | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` | yes |
| `submission-jof/manuscript-preview.pdf` | 406379 | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` | yes |
| `results/revision-20261023/inference/coverage.csv` | 22500 | `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419` | yes |
| `v3_additions.py` | 18558 | `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525` | yes |
| `v6_submission.py` | 21164 | `9f4984fc802f8a2e1375760d78cbe59ae04aa814bb83114d6707b70ac01b61c8` | yes |
| `run_v3_inference.py` | 10276 | `f54ff54dcbc8db5c7446f0fc885bce1d5408cb329d0545ba7021699f1301a527` | yes |
| `inference_tests.py` | 7369 | `2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c` | yes |
| `notes/revision-v6/v5-manuscript-before.json` | 136666 | `2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7` | yes |
| `notes/revision-v6/verification-loop-009-numbers.json` | 2850 | `e0375f8b078f075a598e8207b66730a89bd43026302e81f895f0a82f8618e038` | yes |
| `protocol/revision-v6/common-contract.md` | 4044 | `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8` | yes |

Only the two authorized loop041 artifacts were created by this task. No source, manuscript, saved result, state, ledger, raw/private vector, figure, model, test, proof, UI or network operation was changed or executed; no commit or staging was performed. Existing unrelated working files were not cleaned up. The PDF was fingerprinted only; visual/page-layout correctness and compilation are outside this round. No author-pending conclusion change is raised by the five saved-output traces.
