# v8 calibration implementation and test log

This worker implemented only `v8_mc_calibrate.py` and `test_v8_mc_calibrate.py`, plus this log, against frozen design `protocol/v8/mc-design.md` (design commit supplied by the main owner: `b7e548df`). No real-data calibration was run by this worker. The root owner controls the actual call to `calibrate_all(root)` and the calibration receipt. All unit fixtures below contain synthetic data only. No data download, true-data experiment, parameter retry, or old-archive edit occurred.

## API and coordinate contract

`calibrate_all(root) -> dict` verifies both complete pinned snapshots with `conditional_sources.load_source`, their row counts, the actual last allowed date, and the first validation date. It then passes only `[:10463]` FX or `[:329]` weekly positions and clocks to estimation. Paths are fixed as `.scratch/data/1hourNetPositionsKaggle.csv` and `.scratch/revision-20261022/nyfed-PDPOSGS-B.csv`; there is no source search or fallback.

The result has `status`, `parameters`, `calibrations`, `sources`, `environment`, and the design path. Successful `parameters[D0/D1/D2]` mappings contain `dgp,c,phi,omega,alpha,beta,nu,shape,sigma,burnin`. Shape is a 24-element tuple in memory and a JSON array when serialized. Every parameter is in source-prefix standard-deviation units. Positions are divided by `prefix.std(ddof=0)` and are **not centered**; the AR intercept retains the mean. `calibrations[D*].source_scale` records the native-unit scale.

D0 uses Gaussian innovations, its estimated residual RMS as `sigma`, `nu=None`, and unused GARCH placeholders `omega=alpha=beta=0`. Its initialization variance is `sigma**2`. D1/D2 use fitted GARCH parameters and standardized Student-t innovations in the companion DGP module. D1 estimates RMS by the outcome hour of each AR residual and normalizes the hour shape by its observation-weighted mean square; GARCH sees residual/shape. D2 has unit shape.

AR slope restriction is fixed at [-0.995,0.995]. The unconstrained estimate, constrained estimate, binding flag, and reestimated intercept are retained. GARCH has one call to `arch_model(...,mean="Zero",vol="GARCH",p=1,o=0,q=1,dist="StudentsT",rescale=False).fit(disp="off",show_warning=False)`. Package defaults otherwise remain unchanged. Nonconvergence, invalid/nonfinite parameters, nonstationarity, missing/nonpositive hour RMS, and excessive burn-in yield terminal FAILED records. Failed DGPs have no usable entry in `parameters`. Nonfinite failed-fit estimates become JSON null with their terminal reason retained, so strict JSON output does not silently emit NaN. No fitted value is repaired.

Official API references were reopened: [arch introduction](https://arch.readthedocs.io/en/latest/univariate/introduction.html) and [standardized StudentsT](https://arch.readthedocs.io/en/latest/univariate/generated/arch.univariate.StudentsT.html). The retrieved documentation pages display version 7.2.0; actual fit behavior was exercised with the installed arch 8.0.0 on a fixed synthetic GARCH fixture.

## Test-first observations

1. Before the implementation existed, the 9 initial calibration contract tests were run and all failed with the explicit assertion `v8 calibration implementation is missing` (`Ran 9 tests in 0.002s; FAILED (failures=9)`).
2. The first implementation passed all 9 tests. The additional nonfinite-failure JSON regression test then demonstrated a real failure: strict JSON could not archive a terminal NaN estimate. It was converted to an assertion failure with message `terminal nonfinite calibration cannot be archived as strict JSON`, observed red, and only then the failure-record serialization was repaired.
3. Final calibration-only command:

```sh
PYTHONDONTWRITEBYTECODE=1 uv run --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch --with numpy==2.3.5 python -B -m unittest -v test_v8_mc_calibrate
```

Result: `Ran 10 tests in 0.797s`, `OK`.

The ten contracts check: constrained AR slope plus intercept reestimation; prefix-only scale and parameter invariance after future-value perturbation; known diurnal RMS recovery and unequal-hour weighting; missing/zero-hour failure without repair; degenerate-source failure; terminal one-attempt GARCH failure; invalid/nonstationary parameters and burn-in limit; strict JSON for a nonfinite failure; prefix bounds and JSON-safe successful D0 output; and an actual arch fit on a fixed synthetic Student-t GARCH path.

## Full-repository verification and dependency diagnosis

The first full-suite invocation in the supplied isolated uv environment stopped before collection because pytest was absent. Adding only `--with pytest` produced `1014 passed, 1090 subtests passed`, with **9 failures**, all `ModuleNotFoundError: No module named 'sklearn'`, in 111.00 seconds. Exact failing tests:

- `test_round2_baseline_worker.py::test_qrf_checkpoint_adapter_calls_strict_guard_without_diagnostic_keywords`
- `test_round2_qrf.py::test_constant_headroom_returns_current_floor_and_retains_mature_fit_receipt[0.0]`
- `test_round2_qrf.py::test_constant_headroom_returns_current_floor_and_retains_mature_fit_receipt[-12.5]`
- `test_round2_qrf.py::test_known_linear_path_has_exact_nonnegative_headroom_six`
- `test_round2_qrf.py::test_full_future_perturbation_cannot_change_reports_or_fit_fingerprints`
- `test_round2_qrf.py::test_fixed_forest_seed_gives_identical_reports_and_fit_receipts`
- `test_round2_qrf.py::test_checkpoint_failure_retains_only_issued_prefix_and_no_fallback`
- `test_round2_qrf.py::test_noncontiguous_origins_and_unavailable_training_features_fail_with_context`
- `test_round2_qrf.py::test_failed_forest_fit_retains_attempted_mature_pool_instead_of_a_fake_report`

The old archive `results/revision-20261023/round2/D1-runtime-versions.json` records scikit-learn 1.9.1. Adding that same version to uv resolved the missing test dependency without changing QRF or any old code. Final complete command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 uv run --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch --with numpy==2.3.5 --with pytest --with scikit-learn==1.9.1 python -B -m pytest -q -p no:cacheprovider
```

Final result: **1025 passed, 1090 subtests passed in 124.49s (0:02:04)**, exit 0. The test count changed during parallel development because companion v8 modules/tests had become available; this is a repository snapshot check, not the eventual B7 final package gate. No failed tests were skipped. The root owner was told the first failure cause, and that the first timed pilot overlapped this test run, making the timing projection conservative. No further heavy computation was started after the root's formal-run notice.

## Observed final test environment

- Python: `3.12.14 (main, Aug 25 2026, 13:50:33) [Clang 22.1.3 ]`
- Platform: `macOS-27.0.1-arm64-arm-64bit`
- arch: `8.0.0`
- numpy: `2.3.5`
- pytest: `9.1.1`
- scikit-learn: `1.9.1`
- scipy: `1.18.1`

Implementation was not modified after the final green calibration-only test. Subsequent work in this worker was the complete test run, read-only status/whitespace inspection, API handoff, and this log. The actual real-data calibration outcomes and formal Monte Carlo outcomes must be read from the root-owned results, not inferred from these synthetic tests.
