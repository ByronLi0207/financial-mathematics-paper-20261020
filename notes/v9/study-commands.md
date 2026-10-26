# C2 execution commands and software fixture

All commands run only in the new v9 clone. Every numerical thread limit below
is set to one. uv provides temporary pinned packages; no system package is
installed. The input/design hashes are checked inside the driver before work.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with arch==8.0.0 --with numpy==2.3.5 --with scikit-learn==1.9.1 --with pytest==9.1.1 --with matplotlib==3.11.2 --with pypdf --with pillow python -B run_v9_nonstationarity.py diagnose
```

The next stages use the identical environment and replace `diagnose` with
`pilot`, then `formal`. A separate commit containing the timing-only
`results/v9/nonstationarity/run-plan.json` must occur after pilot and before
formal. A study phase cannot overwrite an existing output directory.

The first study calculation is the `diagnose` launch, recorded by its
manifest's UTC and monotonic clocks. The pilot and formal receipts each
record their own times; all phases remain inside the global 5,400-second
ceiling. Software checks on invented coefficients are separate fixtures,
not a pilot or an examined financial source.

## Original-engine software smoke test

`test_v9_pipeline_smoke.py` passes an invented AR–GARCH–t parameter vector
and an invented source ID to the same new driver and unchanged WP3 forecast
engine. It uses the registered H/W, burn, origins, menus and solvers, with a
software-only source/stream namespace. Both arms have exactly one identical
parameter vector. The check requires eight comparison reports, all F
reports to have 72 points, and exact arm identity for scores, choices and
failure status. It does not require QR numerical success by suppressing
its failure contract.

Observed output: **1 passed in 2.55s**, retained in
`.scratch/v9/engine-smoke.txt`. No actual input series was opened or fitted.
This fixture is rerun with the repaired driver before the study is sealed.
