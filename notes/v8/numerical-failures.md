# v8 numerical failure audit during the formal run

Scope: read-only inspection of four reported D1/p4 failure records and their existing call path. No fit, regeneration, numerical replay, solver change, tolerance change, retry or Git action was performed. Other formal tasks continue. This is an audit of numerical completion, not an accuracy interpretation of unfinished formal results.

## Recorded failures

Repetition numbers below are zero-based, matching the frozen seed keys and worker filenames. Each row belongs to a different factorial cell.

|DGP|p|W|Repetition|Stage|Lambda|Saved reason|Evidence|
|---|---:|---:|---:|---|---:|---|---|
|D1|4|2880|1|evaluation|0.001|QuantileFitError:NONCONVERGENCE|`results/v8/mc/formal/D1-r001.jsonl`, line 7|
|D1|4|720|3|validation|0.001|QuantileFitError:NONCONVERGENCE|`results/v8/mc/formal/D1-r003.jsonl`, line 5|
|D1|4|260|4|validation|0.001|QuantileFitError:NONCONVERGENCE|`results/v8/mc/formal/D1-r004.jsonl`, line 3|
|D1|4|52|10|validation|0.001|QuantileFitError:NONCONVERGENCE|`results/v8/mc/formal/D1-r010.jsonl`, line 1|

The W2880 record retains six complete validation candidates before the evaluation failure and shows that lambda0.001 was selected. The other failures occurred while attempting the first declared validation candidate, lambda0.001; an empty completed-candidate list is consequently expected and does not mean the fit was never attempted. Later `NOT_RUN_CELL_FAILED` rows preserve the prior terminal reason rather than replacing the failed candidate or restarting its cell.

## Call-path check

`v8_mc.py:180-184` passes the four-feature call as:

```text
forecast(x, feature, valid, cache, ids, 6, w, refit_step, lam, guard)[0]
```

This matches `parsimonious_v3.forecast(x,feature,valid,cache,origins,h,w,step,lam,guard)` exactly. For D1, geometry supplies refit_step24. The four features are obtained from the existing `features4` selector, with hourly short/long RMS24/168 and nominal gap3600 seconds. The existing forecast function obtains precisely W completed labels, standardizes only that mature pool, computes the existing positive response scale, and calls:

```text
fit_quantile_ridge(column_stack([ones(w),train]), y/scale,
                   tau=.95, penalty=lam, checkpoint=progress)
```

Thus the design has W rows, an intercept and four slope columns, and the failing lambda is the positive finite scalar0.001. No swapped argument, inappropriate infinity call, feature-count mismatch, wrong horizon or modified solver option was found. The old parsimonious `cell()` wrapper is not called.

## Meaning and evidence limit of NONCONVERGENCE

`conditional_quantile.fit_quantile_ridge` retains the original defaults: max_iter10000, atol1e-6, rtol1e-5 and gap_rtol1e-6. It returns a fit only when both ADMM residual conditions and the feasible-dual Fenchel-gap condition pass. The sole `NONCONVERGENCE` raise is after exhausting this iteration loop. Invalid inputs, invalid options, initialization failures, nonfinite iterates, certificate failures and caller deadline cancellation have distinct exception paths or codes.

The saved exception therefore supports a genuine failure to obtain the original solver's joint numerical acceptance certificate within10000 iterations. The integration inspected above does not explain it as an argument mismatch. This does not prove that the mathematical ridge-quantile problem lacks a solution, that a fitted conditional model has poor statistical accuracy, or that the duality gap alone was the failed condition.

There is a retained-diagnostics limitation: the worker serializes the exception type/message, stage, lambda and `failure_context`, but does not serialize `QuantileFitError.diagnostics`. The unchanged four-feature forecast also does not attach a refit `failure_context`, so the four records have null context. Consequently the existing artifacts cannot identify the exact failed refit or its final primal residual, dual residual and gap. Those quantities must not be invented or reconstructed by an unauthorized replay. The distinction between residual failure and gap failure is not recoverable from these records.

## Consequences under the frozen rules

All four D1/p4 factorial cells remain FAILED for the entire formal experiment. The aggregator gives any recorded FAILED repetition precedence over completed repetitions and leaves complete-cell medians, IQRs, win frequencies and breach summaries null. Completed partial repetitions are diagnostic only; they must not be pooled into a substitute complete-cell result. Solver tolerances, iteration budget, feature set and lambda menu remain unchanged, and no failed candidate is replaced by I or another finite lambda.

P2 requires both feature sets at D1/W2880 and P4 requires all four D1/D2 feature-history sequences. These recorded failures make P2 and P4 UNASSESSABLE under the prespecified rules, regardless of how the remaining cells finish. This is a numerical-completion limitation of the declared procedure, not a failed statistical inequality. Other predictions must await their own required complete cells. Any eventual mechanism claim must distinguish completed simulation evidence from these unavailable comparisons.

## Final run update

All seven failures are recorded in results/v8/mc/analysis-facts.json. The initial four-variable audit above remains valid; three later33-variable failures were in validation at lambda0.001, with available refit context. No failure was retried.

|DGP|W|p|rep|stage|lambda|reason|
|---|---:|---:|---:|---|---:|---|
|D1|2880|4|1|evaluation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|720|4|3|validation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|260|4|4|validation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|52|4|10|validation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|720|33|17|validation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|2880|33|32|validation|0.001|QuantileFitError:NONCONVERGENCE|
|D1|260|33|56|validation|0.001|QuantileFitError:NONCONVERGENCE|
