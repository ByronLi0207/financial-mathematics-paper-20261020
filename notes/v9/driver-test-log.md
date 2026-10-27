# v9 driver integration repair: RED/GREEN record

Task scope: repaired only `run_v9_nonstationarity.py` and `test_v9_nonstationarity_driver.py`, plus this new log and ignored test/backup artifacts. No repository commit, real-series read, actual diagnostic/calibration, pilot or formal study was performed by this repair. All new regressions use invented arrays or fixed fake boundary responses. The existing pipeline smoke fixture uses an invented six-parameter vector and namespace99 solely to exercise the unchanged forecast engine.

Work interval:2026-10-24 18:58–19:06 UTC. The scientific design remained the sole-file preregistration `5decccb0a13ef1969629cfec695dd3459c412c4e`; its file SHA-256 remained `76df3a3d2c2c5b90d4c3f4b225cc4f879b384c6f3d288b6732f488bda15a3894`.

## Retained pre-edit versions

Both current untracked files were backed up before editing, using exclusive creation:

| Backup in ignored scratch | SHA-256 |
|---|---|
| `.scratch/v9/retained-backups/run_v9_nonstationarity.py.bak.2` | `e5d1361e42a6f624f06a22b2052ecdf575f9934104a1ea29e76a7dccc9781dc1` |
| `.scratch/v9/retained-backups/test_v9_nonstationarity_driver.py.bak.2` | `6b0f769dd34d469ebb67a2f662f975cb6af92e4b77bff057a6f3970b7ed44862` |

## Observed test sequence

Every test output below was retained as a new file in `.scratch/v9/`.

| Output | Actual result | Meaning |
|---|---|---|
| `driver-repair-red.txt` | **9 failed,21 passed in2.25s** | Before implementation: reproduced partition/segment failure suppressing the valid constant arm, switching generation failure suppressing constant, lost completed comparison/RNG geometry on interruption, missing parent/worker source identity, missing daily break dates, and absent committed-plan gate. |
| `driver-repair-green-1.txt` | **30 passed in2.29s** | The first repair passed every targeted regression. |
| `driver-repair-integration-1.txt` | **1 failed,161 passed in3.54s** | The existing invented no-break pipeline fixture omitted explicit M. The driver required it instead of recovering the same registered period from valid segment dwell lengths. No scientific setting or data was changed. |
| `driver-repair-integration-green.txt` | **162 passed in5.19s** | After allowing that period-identity compatibility path, all selected new and old constructed checks passed. |
| `driver-diagnostic-failure-red.txt` | **1 failed,31 passed in2.39s** | New requested regression reproduced an outer worker resource failure leaving a valid top-level p-value in a FAILED row; a separate regression confirmed handled segment-fit failures already retained the completed global diagnostic. |
| `driver-repair-final-green.txt` | **164 passed in5.21s** | Final gate:32 driver tests,30 statistic/calibration tests,37 switching tests,2 exposure tests,1 fixed synthetic pipeline smoke fixture, and62 old WP3 core/summary tests. |

Final output SHA-256: `0c7806b1d871a225ee333ed0cd21807b779d8bc67026761a610cf5e15904f01b`.

Command prefix, using the already cached environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 \
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file \
--python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
--with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 \
--with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow \
python -B -m pytest -q -p no:cacheprovider --tb=short \
test_v9_nonstationarity_driver.py test_v9_nonstationarity.py test_v9_switching.py \
test_v9_exposure.py test_v9_pipeline_smoke.py test_v8_wp3_core.py test_v8_wp3_summary.py
```

Targeted RED/GREEN runs use only `test_v9_nonstationarity_driver.py` after the same prefix. The only wrapper warning was uv's `--no-project`/no-project message. This agent did not run or claim the whole repository suite; root owns that integrated gate.

## Repaired scientific/reporting behavior

1. A valid whole-prefix fit remains usable for the constant arm if descriptive partitioning or a segment fit fails. Only switching receives explicit failed comparison records in that case. Whole-fit failure still fails both arms. No no-break vector is substituted into a failed switching arm.
2. The constant arm is generated first under the same registered open-uniform stream. Actual switching generation happens separately; a switching numerical exception cannot erase completed constant reports. Both generation calls and geometry work are charged to `seconds_by_method.generation`. When needed by the old invented fixture, the period is recovered from its exact positive integer segment lengths, preserving M and the phase grid.
3. Every completed QR-versus-F comparison is written immediately as an immutable atomic receipt. Every successful arm's phase, uniform SHA, initial/final RNG states, regime ID list, forward/wrap indices and `describe_geometry` exposure counts are saved before its forecast calls. Evaluation-point vectors are saved per completed synthetic method as well. A mutable progress receipt is replaced atomically; final worker results become visible atomically.
4. Worker exceptions and parent-observed worker exits recover already saved comparisons rather than returning an empty inventory. Missing comparisons remain missing/FAILED in the predeclared full-cell reducer. No partial median or replacement parameter is introduced. Failed/missing workers obtain source identity from the sealed inventory, including workers that never wrote source identity themselves.
5. Formal launch now verifies that the exact `run-plan.json` bytes are already present at HEAD, originated in a sole-file commit ancestral to HEAD, and match the frozen design ID and manifest code hash dictionary. Formal plan metadata retains the verified commit/time/digest. The diagnostic/pilot manifest now seals `v9_exposure.py` too.
6. Valid partitions retain `break_dates` for daily and hourly rows as well as weekly rows, allowing the reporter to read dates without reopening raw data.
7. If an outer diagnostic-worker resource/technical failure happens after a completed bootstrap, the original global diagnostic subresult is retained in `completed_diagnostic_evidence` (status,p,statistic,bootstrap inventory,RNG,moment and available MC fields), while top-level status becomes FAILED and top-level p becomes null. It cannot count toward N1/N4. A normally handled segment `CalibrationError` does not erase a valid completed global p; a valid whole fit remains available for the constant stress arm.

## Final checked source identity

| File | lines | SHA-256 |
|---|---:|---|
| `run_v9_nonstationarity.py` |475|`48507b638a2a57a71ffb11e96e5a44bdf2279bfed596388e7d6ad9b8cb4e73fa`|
| `test_v9_nonstationarity_driver.py` |299|`e26e1095723cd34e06bc618d82ee9119978de81cee2aa3696e911a1433fe57ad`|

The final read-only diff check returned no change for the registered design or existing WP3 forecast/solver/features/scoring/daily modules. The source files were handed back to root after the164-test gate; later edits require their own verification.
