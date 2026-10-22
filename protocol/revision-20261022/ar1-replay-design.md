# Exploratory AR(1) residual-block replay: design before implementation

Design opened22October2026 after the conditional-study results had already been inspected, then settled through numerical and integration review. **A separate public executable freeze is required before financial execution; this document is not an executed result.** The original sixteen-file freeze, parameter selections,69-file core archive and declared primary comparisons remain unchanged. This is a closed secondary question, with no claim to recover an unseen holdout.

## Question and reason for this one addition

Raw historical translation S preserves the initial difference between a historical anchor and the issue level at every subsequent step. AppendixA.4 already explains how a fixed linear recursion instead propagates that difference by `phi^h`. The unexecuted gap is a fitted comparison on the same peak response. The question is whether a historically estimated propagation coefficient changes the realized loss/breach/overreporting tradeoff relative to the same-pool, same-refit S rule.

This is a comparison of specified path transformations, not identification of a causal mean-reversion mechanism. It is more targeted than adding a model menu: one first-order mean filter, no new order, penalty, volatility filter, residual weighting, calibration or post-result reconciliation. An unfavorable, near-identical, nonidentified or numerically failed outcome must remain. The experiment will not replace the original QR primaries or select a new winner for the paper.

Historical filtering and innovation-path generation are established operations. Pritsker, _The Hidden Dangers of Historical Simulation_, FEDS2001-27,19June2001, official62-page [paper](https://www.federalreserve.gov/pubs/feds/2001/200127/200127pap.pdf), §4.1–4.3, discusses conditional filtering, empirical innovations and limitations of finite historical tails. The proposed mean-only ordered-block replay is **not** his GARCH/FHS procedure. Barone-Adesi, Giannopoulos and Vosper, _VaR Without Correlations for Portfolios of Derivative Securities_, USI Quaderno99-04 (body title page revised March1999), [institutional copy](https://folia.unifr.ch/documents/318043/files/wp9904.pdf), physical pp.4–6, also explicitly combine mean/residual filtering with recursive conditional variance and sampled innovation paths. Root inspected those selected text/rendered pages and the title pages in the cached29-page PDF, SHA-256 `787964528e645ecdf2c6bbf494f8dac345e69b2fcfc1a38c1777251708807d30`; this does not establish full-paper reading or method identity. Its model adequacy and the representativeness of residual blocks for the current conditional future remain unproved. The source-family endpoint methods in W20/thesis already use dynamic history, and this design makes no first-use or new-estimator claim.

## Frozen scientific inputs to reuse

Use the exact existing FX and Treasury snapshots, units and evaluation origins. Require the original executable freeze SHA-256 `e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb` and selection SHA-256 `531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7`. Before new computation, an explicit successful fresh-replication directory must supply its own accepted receipts, selection, references and numerical audit. References are read from that verified replica, not refitted or silently copied from old private paths.

| Source | Evaluation origins, inclusive | H | Mature scenario count W | Refit spacing |
| --- | --- | --- | --- | --- |
| FX hourly record |11927–18551,6625origins |6,24 |720,2880 |24records |
| Treasury weekly aggregate |405–681,277origins |6,24 |52,260 |13records |

The complete Cartesian inventory contains **eight cells**. All units, nominal gaps, retained source gaps, issue-known economic-date convention and last-label dates are the original source contracts. No source is pooled, fetched, truncated, relabelled or retrospectively made as-released. Both samples have now been inspected; all new comparisons are exploratory.

## Causal fitting and matched historical information

For issue `t`, use the original refit time `r=first+d*floor((t-first)/d)`. Define

```
a = r-H-W+1,
J = {a,...,r-H}.
```

These are W completed H-record scenario origins. Their unique union of levels is `N_a,...,N_r`. Fit one intercept-bearing OLS recursion `N_s=c_r+phi_r*N_(s-1)+e_s` using **each unique adjacent transition once**, for `s=a+1,...,r`: exactly `W+H-1` pairs. Do not repeat transitions because they appear in overlapping scenario windows. W is a scenario count, not an OLS-pair count. No transition later than r may enter this fit. Freeze the estimated coefficients and historical pool until the next declared refit; the query uses the actually observed current `x=N_t`.

Estimate the intercept and slope directly; do not compute `mu=c/(1-phi)`. A common positive scale on the observed union may be used for centered float64 OLS to avoid avoidable overflow. The exact numerical implementation, synthetic checks and acceptance thresholds must be settled and hash-frozen before execution. Strictly constant regressors, lost scaled dispersion, nonfinite parameters or unsupported numeric operations are failures, not reasons to substitute another coefficient. Finite negative or above-one phi values remain eligible. Do not clip to `[0,1]` or force mean reversion.

The settled numerical contract uses a common binary scale. For `m=max(abs(N_a),...,abs(N_r))`, let `e=min(frexp(m).exponent,1023)` and `s=2**e`, which remains finite and positive for eligible inputs. Set `u=x/s`, `v=y/s`; form offsets `u-u[0]`, `v-v[0]` before subtracting their respective means for cross-products. Do not center by subtracting a reconstructed large-offset mean. Reconstruct the scaled intercept by a correctly rounded sum of the anchor and mean terms, then return c in original units. An exactly constant vector's mean is its repeated value; other means use a correctly rounded sum of entries divided by their count. Both the centered regressor sum of squares and its population variance must be finite and strictly positive; no small-positive cutoff is used. For the actual returned coefficients, let `residual=v-phi*u-c/s`. Require `abs(mean(residual))` and `abs(mean(u*residual))` no larger than `1e-10*max(1,mean(abs(v)),mean(abs(phi*u)),abs(c/s))`. This is a numerical normal-equation check, not a guarantee of relative coefficient accuracy under arbitrary conditioning or statistical fit. Finite power underflow during replay is permitted; nonfinite powers, paths, reports or scores fail. These choices were fixed with synthetic inputs before any AR financial fit. Independent exact represented-input tests exposed and repaired a large-offset defect in an earlier unexecuted max-absolute-scale implementation; that rejected implementation is not silently treated as accepted.

## Ordered innovation replay and report

At a refit, define all residuals with that same `(c_r,phi_r)`. Preserve each historical block's order and keep its original weight. Starting from x, recursively replay that block's residuals with those same coefficients. Subtracting the original and replayed recursions gives the algebraic identity

```
M(i,h;x) = N_(i+h) + phi_r**h * (x-N_i),  0<=h<=H.
```

The implementation may use this identity after independent recursion checks. Set the h=0 element explicitly to x. At exact `phi_r==1`, use the same arithmetic construction as the frozen S helper, to preserve the unit-propagation identity in floating arithmetic; this is not a failed-fit fallback. Near-one values must not be rounded to one. Phi0 does not generally reproduce K, whose native historical peak also includes the historical issue observation.

For each query, form W scenario peaks `max_h|M(i,h;x)|`. Use the original corrected rank `ceil((W+1)*19/20)`, duplicate values retained, no interpolation, and a report at least `B_t=|N_t|`. Do not independently resample steps, recenter residuals, replace their order, scale them, mix residuals from different fitted models or introduce new Monte Carlo randomness. Retaining ordered blocks does not establish their conditional representativeness or a95% coverage guarantee.

## Complete comparisons and output

For each of the eight cells retain the new report and score on every original evaluation origin, or mark the whole cell failed/incomplete without a shortened mean. The direct contrast is **AR replay minus same-W/H/refit frozen S**, eight rows. Context contrasts against matching frozen F and the already selected matching QR add eight rows each: **24 comparisons total**. No new primary is selected from them.

Use exactly the original native-unit pinball score, strict breach count, all-origin positive overrun, report and unused/extra-allowance quantities. Preserve full-origin means, original global H+1 sparse grids and calendar-issue groups, with counts and null denominators explicit. These remain descriptive; no confidence interval, significance test, cross-source average or population superiority claim is added.

Retain per-refit `(r,a,transition_count,c_r,phi_r)`, numerical acceptance and method/source/code identities; predeclare finite phi summaries and counts below0/equal1/above1 as fitted-parameter descriptions, not evidence of a true data-generating process. Do not inspect the resulting coefficient or loss distributions to change the fit window or numerical rule. Per-origin source values, forecasts and parameter traces stay private; original-code, design, aggregate results and sanitized resource/failure receipts may be published.

## Verification and resource contract before executable freeze

Independent synthetic oracles must check intercept-bearing OLS against exact small rational cases; the direct-versus-recursive replay identity; phi0/exact1/near1/negative/above1; actual issue versus refit timing; completed historical pools; duplicate/corrected ranks; query-floor inclusion; future-perturbation resistance; constants, nonfinite values and overflow; every all-origin failure rule; and exact S identity at unit propagation. An independent reader must inspect the real integration path, not only mocked helpers.

Use one financial process and one requested numerical thread, at most two observed OS threads, internal540-second/1.5GiB stops and600-second hard timeout. Eight cells execute serially under one bounded overall attempt. During forecast loops, resource/array checks occur at every refit and every128issues, with additional audit, cell-end and final readback checks; do not fork a thread-probe process and rescan growing scalar lists at every single query. The gaps are bounded and every query still executes the same forecast. Maximum working scenario matrix is `2880x25` float64 (576000data bytes); never allocate the `6625x2880x25` evaluation cube. Existing exact snapshots fit the standing raw-data budget; there is no new download, install, GPU, broad search or persistent service. Measure real RSS/time/threads rather than treating matrix arithmetic as a measured resource result.

After review resolves exact numerical, dependency, audit and failure details, bind this design, a small executable specification and all newly used code to a separate public before-execution freeze. Only then execute. Preserve every original file and unfavorable new result. At the end of this closed addition, do not extend the AR order or add volatility fitting in response to outcomes.
