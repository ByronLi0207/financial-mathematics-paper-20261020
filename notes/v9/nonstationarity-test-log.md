# v9 statistical primitives: artificial-input RED/GREEN record

Completed initial implementation and verification on 2026-10-24, after the sole-file design commit `5decccb0a13ef1969629cfec695dd3459c412c4e`. This task wrote only `v9_nonstationarity.py`, `test_v9_nonstationarity.py` and this log. It did not load financial data, run the study driver, calibrate any actual source, run a real-series diagnostic or generate research/pilot/formal experiment results. All arrays used below were constructed inside the tests with declared fixed seeds.

The implementation follows `protocol/v9/nonstationarity-design.md`, current SHA-256 `76df3a3d2c2c5b90d4c3f4b225cc4f879b384c6f3d288b6732f488bda15a3894`. It does not edit that file or any frozen WP3/arch library file.

## Environment and command

The environment is the same pinned offline environment recorded in `notes/v9/baseline-tests.json`:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow python -B -m pytest -q -p no:cacheprovider test_v9_nonstationarity.py test_v9_switching.py
```

Only the two new artificial-input test files were run together. The study owner will perform the repository-wide integration suite; this subtask was expressly restricted to artificial inputs. No system Python package was installed. uv emits the harmless launcher message `--no-project was provided, but no project was found`; pytest emitted no test warnings.

## RED/GREEN sequence

| Step | Invocation suffix / receipt | Actual result |
|---|---|---|
| Initial RED, before any production module existed | `test_v9_nonstationarity.py -x`, receipt `8096b5` | Exit 1; `1 failed in 6.30s`; the explicit assertion was `v9 statistical implementation is absent` |
| Initial GREEN after implementation | `test_v9_nonstationarity.py -x`, receipt `4e748e` | Exit 0; `21 passed in 2.40s` |
| Extended artificial coverage | `test_v9_nonstationarity.py`, receipt `1b6844` | Exit 0; `28 passed in 2.50s` |
| Independent global-search tie regression RED | `test_v9_nonstationarity.py -k tie_tolerance`, receipt `9c6703` | Exit 1; `1 failed, 28 deselected in 2.34s`; expected complete-partition cuts `(11,20)`, old implementation returned `(11,19)` |
| Corrected global tie handling, initial joint GREEN | `test_v9_nonstationarity.py test_v9_switching.py`, receipt `001f32` | Exit 0; `66 passed in 2.56s` (29 statistical tests plus 37 switching tests) |

| Static-review regression RED for tiny positive RSS | `test_v9_nonstationarity.py -k near_deterministic`, receipt `1911f7` | Exit 1; `1 failed, 29 deselected in 2.34s`; an artificial AR series with genuine 1e-8 noise had incorrectly become NO_ADMISSIBLE_PARTITION |
| Direct-RSS cancellation fallback, final joint GREEN | `test_v9_nonstationarity.py test_v9_switching.py`, receipt `b06cac` | Exit 0; `67 passed in 2.71s` (30 statistical tests plus 37 switching tests) |

The tie fixture deliberately expands its test configuration tolerance to 1.0 so that tolerance accumulation is visible. The registered research tolerance remains exactly `1e-10`. The correction stores exact dynamic-programming minima, then applies the tie threshold once to complete partitions; it also applies the fewer-breaks rule against the global exact BIC minimum. No archived or prospective financial output was examined to choose that fixture.

## API and behavior

- `CalibrationError(reason, details)`: unavailable input/calibration/statistic. It is never silently mapped to stability/non-rejection.
- `fit_ar_garch(levels, design, start=0, stop=None)`: six-key normalized-level parameter dictionary plus diagnostics. The whole-prefix population SD is used for all segments; the level mean is preserved. start/stop select global transition rows, including the preceding observed lag for a segment's first target. AR slope is the exact solution of the profiled constrained least-squares problem. A GARCH subclass adds `alpha+beta<=.999` before optimization; one default-start fit only, no retry and no arch source edit. Omega is transformed back by residual-scale squared. Boundary fits, optimization status, scale factors and warnings are recorded.
- `hansen_statistic(levels, condition_max=1e12)`: unconstrained OLS AR(1), official Hansen statistic, independent score-correlation singularity/conditioning gate. The tabulated critical values are unused.
- `moment_qualification(params, margin=1e-8)`: finite-second-moment generation gate, nu>4, standardized-t kappa and unconditional GARCH q4 gate. nu<=4 has null kappa/q4 fields. This qualifies the fitted model only.
- `bootstrap_stability(levels, params, source_index, design, checkpoint=None)`: COMPLETE with plus-one p, all bootstrap H values, exceedances, Monte Carlo standard error and initial/final PCG64 states; NONREGULAR_NULL has no p and generates no bootstrap paths. The simulator is imported only for qualified nulls. Failed required path/statistic raises CalibrationError. Deadline cancellation propagates.
- `locate_breaks(levels, design)`: exact global k=0/1/2 AR separate-variance/BIC search with O(M) storage. Cuts are transition-row cuts. Returns all admissible per-k candidates, exact minima, chosen partition, segment lengths and intervals, cap status and descriptive-only flag. It does not inspect a diagnostic p-value.

## Artificial checks

Tests compare H to the independently invoked official installed `breaks_hansen`, verify scale invariance and fail-closed singular/ill-conditioned inputs. They distinguish finite variance from finite unconditional fourth moment, validate both parameter and moment boundaries, and check preservation of the nonzero level mean and global segment scale. A positive unit change leaves the normalized model unchanged; Omega/residual scale conversion is asserted explicitly.

The fit-failure test forces a nonconverged optimizer response and checks a single call with no custom starting values and the declared maxiter/ftol. Its inspection of the fitted volatility object's actual constraints distinguishes an a+b=.999 vector from an a+b=1 vector.

The locator is checked against an independent exhaustive integer-partition calculation, an inserted mean break, two inserted variance breaks, zero-variance/singular partitions and the full artificial matched-hourly length n=8109/M=8108 with minsegment=1622. The implementation holds one-dimensional sufficient-sum and DP arrays rather than an M-by-M matrix. The full-partition tie regression prevents local tolerance from accumulating across DP layers.

Artificial known-null parameters exercise the real switching module and bootstrap refitting of OLS on each path. The mean-break fixture rejects at the declared artificial-test precision B=39, and repeat calls reproduce every bootstrap statistic and RNG state. Tests separately inject a missing replicate, a nonfinite path and a singular path and require an unavailable result rather than a p-value. These B=3/19/39 and reduced-burn fixtures are software tests; formal diagnostic B=999/burn=20000 remain design-controlled.

## Initial verified file identities

At 2026-10-24T18:47:02.772432+00:00:

- `v9_nonstationarity.py`: `a645f94e464751e0aef1d2570eb40e8f2c7757cef09fbb645650564c620cb0b3`.
- `test_v9_nonstationarity.py`: `771f49d5e68330916e101793d932d2da942acaa2d4ca2af40230e5b413e475e1`.

These hashes identify the 66-pass implementation. Any later integration edit needs a fresh test receipt/hash. No commit was made by this subtask.

## Static review and final verification

A delegated same-model static review of these two source/test files and the frozen protocol found one important mismatch: the first implementation rejected tiny positive RSS values while guarding sufficient-sum cancellation. The added artificial positive-noise regression failed before the fix. Suspect sufficient-sum RSS now triggers direct segment residual/rank computation on locally centered original values; a positive direct RSS is retained without a variance floor or positive-variance rejection threshold. Exact linear zero-RSS fixtures remain inadmissible. The reviewer found no other important transition/scale/constraint/moment/bootstrap/tie issue. No Claude or cross-model review was used.

Final checks at 2026-10-24T18:49:21.743842+00:00:

- `v9_nonstationarity.py`: `ae73f11b508c47b9a213c524ffe9596a7ccc06c882c092427864674d84e72ddb`.
- `test_v9_nonstationarity.py`: `ae2f5f6506fd596236e9a5aa39bcc0f292d310ce69853aaf0b748cc0c673f39b`.

The final 67-pass receipt supersedes the initial 66-pass hashes above. The only study computations in this subtask were fixed artificial tests; no real-study clock was started here.
