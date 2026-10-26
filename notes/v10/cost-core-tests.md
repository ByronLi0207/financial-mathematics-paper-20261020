# E4 pure cost core — artificial tests only

The frozen design is `protocol/v10/cost-design.md`, sole-file design commit
`a112e458500b5dd34e0536074dff77091ab39ed1`, created
`2026-10-24T23:45:53.195815+00:00`. It was read before implementation.

Only `v10_cost.py`, `test_v10_cost.py`, and this note were written for this
subtask. No real financial vector, private NPZ, actual cost run, forecasting,
calibration, MCS calculation, or real-input materialization was performed.
No commit or full suite was run; the coordinating agent owns those gates.

## API and numerical contract

`evaluate_costs(capacities, target, floor, reference_id, grid,
primary_method_id)` is a pure function. Its COMPLETE return contains
`mean_F_headroom`, a `methods` mapping of primitive scalar statistics, and
`rows` with exactly the driver's method/parameter/cost/comparison fields.
It also records the fixed primary ID and whether it is present, without
selecting any replacement. Every supplied complete method enters every
Cartesian parameter point; there is no minimum-cost selection or MCS filter.

Primitive method fields are `n`, `mean_headroom`,
`normalized_mean_headroom`, `strict_breach_count`, `strict_breach_rate`,
`mean_excess`, and `normalized_mean_excess`. Normalization uses only
`mF = mean(C_F-B)`. A missing F or nonpositive mF yields whole-comparison
UNAVAILABLE, with no epsilon denominator. Nonfinite/empty/non-vector/unequal
length data, any `C<B` or `Y<B`, or an invalid coefficient yields
UNAVAILABLE with a reason, empty methods and empty rows. No partial grid or
partial method deletion is returned. Every result is native JSON data, with
no arrays or nonfinite numeric values.

The scalar formula is
`kappa*mean(C-B)/mF + beta*mean(Y>C) + c*mean(max(Y-C,0))/mF`.
Breaches use strict `Y>C`; cheaper uses exact `difference<0`; ties use exact
`difference==0`. No tolerance is introduced. Shared-axis matching and
permitted frozen-floor recovery belong to the input adapter, before this
single-floor API.

## Observed RED → GREEN

Twenty artificial cases were written before the implementation. The first
run produced **20 failed in 0.19s**, each with the expected
`ModuleNotFoundError: No module named 'v10_cost'`. After implementation the
same file produced **20 passed in 0.10s** (exit 0). The only launcher notice
was uv's `--no-project` notice; pytest emitted no warnings.

The cases cover hand-calculated reserve, F normalization, breach and excess
statistics, three exact method costs, positive common-scale invariance,
all-zero coefficients, absent fixed primary without substitution, exact
ties, next-representable-float strict breach and cost comparison, all
methods at every Cartesian point, whole-cell invalid-data failures,
nonnegative finite coefficients, and the tau=.95 pinball identity at
`kappa=.05, beta=0, c=1`.

The hand calculation uses floor `[10,10,10,10]`, target `[10,12,15,18]`,
F capacity `[12,12,12,12]` and Q capacity `[11,13,15,17]`. Thus mF=2,
F reserve/excess are 2 and 2.25 with two breaches, and Q reserve/excess
are 4 and .25 with one breach. At `kappa=.5,beta=2,c=3`, costs are
4.875 for F and 1.875 for Q, giving difference -3. These are artificial
expected values, not new study results.

Command used for both runs:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest==9.1.1 python -B -m pytest -q -p no:cacheprovider --tb=short test_v10_cost.py
```

Both files were also parsed with `ast.parse` without importing study code.

| File | Bytes | SHA256 |
|---|---:|---|
| v10_cost.py | 4647 | 015b0fe5c546d9c7bc38b69948ec1862eef5ac3dbdafb838ac6bd20b38ee3843 |
| test_v10_cost.py | 6196 | d099329a2a9a4476c7c963488539ed5aa5fca1921ae17cd642c1c1b31ed170a6 |
