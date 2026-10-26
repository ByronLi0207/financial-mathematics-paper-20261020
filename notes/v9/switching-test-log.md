# v9 switching primitives: test-first verification log

Scope: only `v9_switching.py`, `test_v9_switching.py`, and this new log. No commit was made by this agent. No real input was loaded, no diagnostic or calibration was run, and no pilot/formal study repetition was produced. The only generated paths were fixed artificial test fixtures. Existing forecast/solver files were not changed.

The full scientific contract `protocol/v9/nonstationarity-design.md`, committed alone as `5decccb0a13ef1969629cfec695dd3459c412c4e` at2026-10-24 11:38:37 PDT, was read before tests or implementation. Implementation and the checks below occurred after that commit and before2026-10-24 18:44:28 UTC. Exact RED/GREEN chronology is also present in the task's tool-call history and messages to root.

## RED observed before creating the production module

Created the artificial-input test file first. The production module did not yet exist. Ran the targeted command below with `--tb=short test_v9_switching.py`:

```text
37 failed in 0.93s
```

Exit code1. All37 failures were the intended assertion `v9_switching API not implemented`, rather than collection/import errors. The failing test inventory covered four public APIs, fixed quantiles and variance normalization, invalid inputs, phase/burn schedule, two-path GARCH recursion, switch-state carry, exact k=0 equality, forward/wrap boundary indices, stream reproducibility, retained shapes and checkpoint cancellation. Root received the RED status before the module was written.

Before the first implementation run, the boundary-parameter fixture's decimal result comparison was given absolute tolerance2e-16 to avoid asking floating-point addition to equal a decimal literal byte-for-byte. Exact byte equality remains required for the k=0 paired paths.

## GREEN observed after implementation

The first targeted implementation run returned exit0:

```text
.....................................                                    [100%]
37 passed in 0.85s
```

Then ran the new tests together with the existing constructed-input WP3 core and summary tests, returning exit0:

```text
........................................................................ [ 72%]
...........................                                              [100%]
99 passed in 0.98s
```

The only wrapper warning was uv's `--no-project was provided, but no project was found`; pytest reported no test warning or failure.

Exact environment/command prefix:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 \
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file \
--python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
--with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 \
--with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow \
python -B -m pytest -q -p no:cacheprovider --tb=short \
test_v9_switching.py test_v8_wp3_core.py test_v8_wp3_summary.py
```

The full repository suite was not run by this agent because root limited this implementation task to constructed artificial tests. These99 passes are a focused software gate, not a whole-suite, financial-reproduction or study-completion claim. Root owns the later integrated full-suite run.

## Implemented contract

- `standardized_t_shocks(uniforms,nu)` uses open uniforms and t inverse CDF, multiplied bysqrt((nu−2)/nu). Nonfinite/closed uniforms or nu<=2 fail.
- `regime_schedule(lengths,phase,burn_in,retained)` returns total integer IDs for `(phase+i−burn_in) mod sum(lengths)`; no parameter or state reset.
- `simulate_constant_paths(params,n,B,rng,burn_in=20000,checkpoint=None)` returns float64[B,n]. Each time step draws independent path-column `rng.standard_t(nu,size=B)` values. First variance1, preceding level0, states continuous through burn. Only the retained output matrix and B-vectors are stored.
- `generate_pair(...)` uses `PCG64(SeedSequence(entropy,spawn_key=(9,stream_tag,source_index,rep)))` and integer1..2^53−1 divided by2^53. It saves initial/final RNG state, canonical little-endian uniform SHA, registered phase, retained position/variance/innovation vectors and transition identities for both arms. Differentnu values transform the same U through their own inverse CDFs.
- Six parameter keys are exact: intercept,phi,omega,alpha,beta,nu. Finite-second-moment validity is checked; the already-fitted.999 restrictions are not imposed by clipping in generation.
- Forward transitions and last-to-first wraps are separated. When burn>0, a retained-index0 boundary is detected using the last burn regime. The constant arm always has no transitions. A single-regime k=0 switching arm also has no artificial wrap: only actual regime-ID changes count.
- Each generator calls checkpoint at step0, at most256 time steps apart, and at the final step. Cancellation propagates without returning partial success.

## Checked source identity

At the99-test gate:

| File | lines | SHA-256 |
|---|---:|---|
| `v9_switching.py` |232|`70309cfe6a055af8503fcb81e07d8a0240d115211f185740a68a1eec3d196731`|
| `test_v9_switching.py` |229|`afb7e81b49cf62a6e08da0164971eb1e91afbe27641c839aa7c4d7930475d06a`|

The source-diff check on `v8_mechanism_mc.py`, `conditional_features.py`, `conditional_quantile.py`, `conditional_study.py`, `study_core.py`, `run_v8_wp3.py`, and `v8_daily_fx.py` returned no changed path.
