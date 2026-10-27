# WP2 implementation clarifications, before new financial execution

- The SAV initialization quantile uses the finite inverse empirical CDF, `ceil(19*n/20)` (no +1). This resolves the empirical-quantile definition in the design. It does not alter the corrected rank of F or ACI.
- ACI warm start chooses the latest validation-grid refit that can supply W matured scores, `first - ceil((W+H-1)/step)*step`, subject to original full-window/feature availability. The original16 source/H/W/base initialization cases are unchanged by the exact-grid-boundary correction.
- Gamma eligibility uses complete `origin_count`, `hits` and `mean_loss`. Nonfinite/incomplete candidates remain explicitly ineligible; the rest of the fixed menu remains visible. Selection is coverage-first, loss-second, smaller-gamma-third.
- New tau scoring interprets the supplied finite decimal tau as its rational decimal value, so at .95 the two floating weights are exactly the immutable original float(19/20) and float(1/20). Historical scores are checked with the unchanged original scorer. Old result bytes remain untouched.
- Private ACI traces preserve exact state strings without fixed-width truncation, score quantiles, raw thresholds and floors. Rank0 has a private minus-infinite threshold and a finite floor report; public JSON includes only finite aggregates/statuses.
- One original source/H/W/base/phase is a declared worker cell. The same shared limits govern warm base fitting, all four gamma candidates, scoring and final admission. Validation eligibility and selected gamma receipts freeze before ANY WP2 evaluation worker.
- Public SAV receipts include scalar refit/start diagnostics. Vectors of training, shock, initialization and recursion rows stay private. Failed-start dataclasses are explicitly converted to scalar JSON records; failed cells have no accuracy summary.

These clarify executable semantics before new monetary outcomes are read. They do not create a coverage guarantee, global optimizer guarantee, fresh holdout, historical-release dataset or independent dealer sample.
