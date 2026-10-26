# WP1: post-hoc breakeven description — rules frozen before new fitting

This is a post-hoc description, not a preregistration of discovery. The v8 results and the supervisor's interpretation were already known. No candidate correlation, logistic fit, selected metric or threshold has been calculated for this v9 task before this rule freeze. WP0 has passed at local commit `08170e7eca0fd260acdf87087fc81b6244e632d2`. The companion JSON is the exact numerical contract and input fingerprint list.

## Population and metrics

Use all 144 conditional-model cells (72 each for QR33 and QR4) in the sealed v8 WP3 grid, not the 72 F self-comparisons. Nominal coefficient counts including intercept are p=34 and p=5. Source p_index denotes volatility persistence, not coefficient count. Candidate a is W/p, b is W/((H+1)p), c is W/(H+1). All three are descriptive nominal indices, not measured independent sample sizes or effective regularized degrees of freedom.

Each cell ordinate is 100(mean QR evaluation loss / mean paired F evaluation loss - 1). Use final evaluation.mean_loss from 32 reports per cell, not candidate validation losses. The single archived failed candidate remains part of the old procedure history; it is not an incomplete selected evaluation report. Complete final F/QR reports and source bindings must be verified before fitting. Preserve failure/NA rather than rerunning old studies.

## Candidate scoring and selection

Pool the 144 cells with equal weight. Calculate Spearman's rank correlation using average ranks; do not add a correlation hypothesis test. Also report the same descriptive correlation separately by method. For each candidate, fit one binary logistic model to standardized natural log(metric). Win means loss change<0; exact zero remains no-win. This is training-set accuracy on the discovery cells, not held-out forecast accuracy.

Use cached scikit-learn 1.9.1 LogisticRegression(C=1,l1_ratio=0,solver=lbfgs,max_iter=10000,tol=1e-10,fit_intercept=True,class_weight=None,warm_start=False). l1_ratio=0 is its current L2 specification; the deprecated penalty argument is not passed. StandardScaler uses population standard deviation (ddof=0). Do not constrain the fitted slope. Select the largest integer number correct out of 144; exact ties prefer c, then a, then b. One-class/nonfinite/convergence failure blocks selection instead of triggering another solver or tuning menu. Report every candidate and the class counts.

## Curves, crossings and resampling

For each method separately, group equal values of the selected metric using exact rational keys and average cell percentage changes equally. Do not pool raw losses across different DGP conditions. In raw metric coordinates, linearly interpolate the earliest positive-to-nonpositive segment root; a zero right endpoint is an observed root. Retain all downward roots. If the smallest metric ordinate is nonpositive, mark the first root left-censored/unidentified; if no root is bracketed, mark unidentified. Never extrapolate. Multiple roots invalidate an interpretation that longer histories must always help.

Fix PCG64 seed entropy 2026102491 and 1999 bootstrap draws. Draw 32 replication indices with replacement once per bootstrap; reuse that exact cluster draw in every cell and both methods, preserving common v8 innovation streams and F/QR pairing. Recompute each cell's ratio of means, the curve and its primary root. Keep the selected metric fixed and retain all 1999 statuses and resampling-index hashes.

Report the finite-root 90% empirical percentile interval with its explicit effective denominator, conditional on identification. Also bound the endpoints over all draws: missing positive roots are completed by zero for the lower 5% endpoint and positive infinity for the upper 95% endpoint. Use sorted inverted empirical CDF ranks ceil(q*n)-1, not interpolation involving infinity. This is a worst-completion percentile envelope, not a guarantee of unconditional statistical coverage. Both summaries condition on the post-hoc metric choice and fixed simulation grid; neither accounts for discovery-model selection. The all-draw envelope is the fixed numerical interval for the later learning-curve prediction. Zero/unbounded endpoints make that prediction non-discriminating or NOT_TESTABLE; do not replace it with the narrower finite-only interval.

## Real observations and later interfaces

After selection and threshold calculation, overlay the original hourly FX/Treasury, parsimonious results, v8 daily FX and original 12-panel results listed in JSON. Match the same-window historical F; never substitute rolling_F or one_state_F. Do not include expanded-menu QR33_plus as original QR33. Real observations cannot tune the index, root, interpolation or uncertainty interval. Report agreement as descriptive consistency only.

Actual source implementations have nominal 34/5 coefficients, but Treasury has constant columns and daily issue times also make calendar features constant. No new rank calculation is authorized here. Together with different penalties and failure rules, this prevents interpreting QR33/QR4 differences as a clean causal effect of parameter count. If c wins, it does not contain p and cannot itself confirm a per-parameter mechanism.

For later conversion to W use p*r (a), (H+1)p*r (b), or (H+1)r (c), preserving real endpoints. The required discrete grid has no exact common a/b support across model sizes (factor 17); P3 must then be NOT_TESTABLE, not silently changed into a same-W or interpolated comparison. c permits direct matching. WP2 and WP3 must still receive their own committed numerical predictions and criteria after these post-hoc estimates exist.

## Scope, evidence and budget

One worker, one numerical thread, RSS<=2GiB, each analysis<=600s. Only saved outputs are read; no raw FX read, new financial DGP, old simulation rerun or installation is part of WP1. Keep raw logs, source hashes, failed checks, all candidate scores and all resampling statuses. The design is committed before new fitted effects; user-visible summaries remain post hoc.

Primary software sources checked before implementation: SciPy spearmanr documentation (rank statistic and undefined constant inputs); scikit-learn LogisticRegression documentation (L2 via l1_ratio=0, inverse regularization C, solver and convergence parameters); StandardScaler documentation (ddof=0). Their exact URLs are in JSON. Only brief method metadata are derived from these sources; no source text is reproduced.
