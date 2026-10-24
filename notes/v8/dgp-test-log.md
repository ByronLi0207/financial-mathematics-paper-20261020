# v8 DGP/oracle test-first implementation log

Scope: `v8_mc_dgp.py` and `test_v8_mc_dgp.py`, following the separately committed `protocol/v8/mc-design.md` (b7e548df). Only synthetic unit fixtures were run. No source calibration, financial fit, pilot, formal Monte Carlo experiment, source-file write or Git mutation was performed by this subtask.

Runtime: `/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, with `-B` to avoid bytecode writes.

## Initial RED, before implementation

Command:

```text
/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest test_v8_mc_dgp -v
```

Observed exit code 1:

```text
Ran 15 tests in 0.001s
FAILED (failures=15)
AssertionError: unexpectedly None : v8_mc_dgp implementation is missing
```

All failures were assertions on the absent implementation, not import/collection errors. Tests fixed their independent moment bounds, 12% oracle/F fixture bound, current-state contrasts, calendar literals and seed behavior before production implementation.

One arithmetic equality assertion was changed before the first implementation test run to an absolute 1e-15 comparison: binary float `.7**2` need not exactly equal the decimal literal `.49`. This is a float representation issue; the statistical fixture bounds were not changed.

## First GREEN

Same command, observed exit code 0:

```text
Ran 15 tests in 0.431s
OK
```

Covered: negative-index burn-in clock and weekend gaps; retained index zero calendar; seed reproducibility and distinct streams; stationary AR mean/variance; unit-variance standardized Student-t; GARCH unconditional variance; diurnal RMS recovery; invalid parameters; floor inclusion; known current latent residual/variance; realized-future perturbation and truncated-prefix invariance; bitwise batch-size invariance; next hour across weekend; the explicitly nonstationary high-positive-level random-walk oracle/F boundary fixture.

## D0 calibration representation RED -> GREEN

The calibration subtask represents unused D0 parameters as `omega=alpha=beta=0, nu=None`. Added `test_gaussian_calibration_omits_unused_garch_and_t_parameters` before accommodating this interface.

RED command:

```text
/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest test_v8_mc_dgp.DGPContractTests.test_gaussian_calibration_omits_unused_garch_and_t_parameters -v
```

Observed exit code 1, expected interface incompatibility:

```text
ValueError: invalid nu
Ran 1 test in 0.000s
FAILED (errors=1)
```

The implementation now accepts omitted t parameters and a zero unused GARCH intercept for Gaussian D0, while requiring positive omega, nu>2 and alpha+beta<1 for D1/D2. No draws or scientific thresholds changed.

GREEN command: full DGP test file as above. Observed exit code 0:

```text
Ran 16 tests in 0.307s
OK
```

## Focused existing-component regression

Command:

```text
/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B -m unittest test_v8_mc_dgp test_empirical_headroom test_conditional_features -v
```

Observed exit code 0:

```text
Ran 38 tests in 0.324s
OK
```

The root task owns the final repository-wide test run and formal execution receipts. This focused subtask does not claim that the entire repository suite or any pilot/formal experiment has run.

## Interface and numerical meanings

- `DGPParams(dgp,c,phi,omega=1,alpha=0,beta=0,nu=8,shape=(1,)*24,sigma=1,burnin=10000)` is immutable. The calibrator supplies the protocol-derived burn-in. Stationary simulation rejects abs(phi)>=1; phi=1 is allowed in the parameter container only so the explicitly nonstationary oracle/F fixture can use a manually supplied path.
- `simulate(params,n,seed)` returns exactly `position,variance,residual,times`. Residual means latent unseasonalized u_t, variance means v_t. Burn-in uses integer clock indices -burnin,...,-1 and retained observations use 0,...,n-1, preserving the fixed retained calendar anchor.
- `clock(dgp,indices)` accepts integer arrays, including negative indices. D1 uses the frozen 120-record trading-week formula. D0/D2 use seven-day Wednesday clocks.
- `oracle_reports(params,path,origins,horizon=6,paths=2000,seed=20261024,batch_size=32)` returns capacities. It reads only each current state and deterministic future calendar, recursively updates variance before the first shock, includes the current absolute floor, and uses the lower empirical .95 quantile rank ceil(.95*paths).
- Each oracle origin receives a SeedSequence child keyed by its actual origin index. These independent random streams preserve bitwise output when only batch size changes. No worker-order or Python-hash seed is used.
