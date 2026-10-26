# E9 selected-C2 shrinkage readback — post-result / exploratory

Frozen before diagnostic outcomes at 2026-10-23T09:48:02.507254+00:00.

Replay only the already selected Treasury C2 penalty for H={6,24}, W={52,260}; no validation retuning or replacement of any original result. Use the original source fingerprint, evaluation405..681, refit13 anchored405, accepted ridge solver, per-pool transforms and response scales. Temporarily wrap the original solver only to copy its returned coefficients; original prediction arithmetic unchanged. Require exact capacity equality to retained private C2 traces and exact F equality to retained frozen-F traces. Any failure is retained, not patched into an original result.

For every refit save slopes in standardized/response-normalized coordinates, L2 norm, max absolute slope, intercept, training transform and response scale, query count, signed/absolute/max native slope contribution and the corresponding projection-aware capacity difference against the same fitted intercept with slopes removed. Weight aggregate contributions by actual query count. This fitted-intercept counterfactual is not a refitted intercept-only model.

I/F use empirical_headroom.predict on identical mature pools and refit schedule. I is the lower empirical minimizer rank ceil(19W/20); F uses ceil(19(W+1)/20). For C2–I and C2–F report max/mean absolute native capacity difference, signed mean, capacity and headroom correlation, strict breach counts/intersection/union/Jaccard/xor, mean pinball difference and percentage. Undefined constant-array correlation or empty-union Jaccard is null with a reason.

No data-dependent collapse threshold or new significance test is introduced. A menu-boundary λ or high capacity correlation alone cannot prove intercept-only equivalence or zero feature value. Interpret actual slope/native effects and observed I/F losses, explicitly descriptive. Keep all adverse comparisons. Original primaries and archives remain immutable. Single numeric process, one numerical thread, each cell<=590s, measured RSS/threads, source<=100MiB. No installation/deletion/push.
