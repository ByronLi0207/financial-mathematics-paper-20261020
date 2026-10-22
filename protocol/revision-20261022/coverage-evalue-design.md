# Late fixed-time one-sided coverage diagnostic

Design opened22October2026 after the financial forecasts, scores and breach summaries had been inspected. **Before-computation specification.** A separate executable closure binds this document and must be published and verified before computing the new evidence values. A frozen design is not a completed calculation; actual execution and independent readback require their own genuine receipts. Existing forecasts, selected parameters, original comparisons and result files remain immutable.

## Purpose and status

The question is whether existing issued reports are compatible with a datewise conditional upper bound on strict breach probability. This is distinct from testing equality of unconditional mean losses, producing a confidence interval, selecting a superior procedure or certifying operational safety. It is a mature e-value application and a late exploratory diagnostic on inspected records. The new freeze will establish before-computation choices; it cannot restore an unseen holdout or erase the earlier selection of methods and this diagnostic.

The existing matched family is complete at eight source/H/window configurations crossed with seven report labels: `QR`, `KNN`, `SCALED_KNN`, `frozen_F`, `frozen_S`, `frozen_K`, `AR1_REPLAY`. This is56report cells, deliberately excluding24rolling and18one-state reports from the full98-report archive. Eligibility follows the matched completed-label/refit question, not a computed e-value. Structural aliases remain separate labels in the56-cell multiplicity count; they are not independent replications.

No new source, forecast, model fit, scoring preference, volatility filter, resampling, covariance estimate, instrument search, annual subtest or running-maximum plot is authorized by this diagnostic. All56cells and all their phases must be retained, including adverse and uninformative outcomes. Do not expand the menu or change the prior/spacing/terminal after seeing these evidence values.

## Null, information and event

Use alpha=1/20 for the nominal strict-breach bound; use delta=1/20 separately for a fixed-family error budget. For each report cell, the null is

\[
E[I_t\mid\mathcal F_t]\le\alpha\quad\text{a.s. at every declared issue},
\qquad I_t=1\{P_{t,H}>C_{t,H}\}.
\]

The entire report procedure must be issue-information measurable. The full target resolves by t+H. Prior training and validation choices enter the issued method only under their existing causal replay convention. For Treasury, this is the economic-date downloaded-vintage filtration; it is not a recovered historical public-release filtration. Fixed code and historical inputs alone do not remove the researcher's inspected-sample choices.

Known-floor atoms are compatible with this one-sided null: an upper quantile can have strict breach probability below alpha. Equality `P=C` is a nonbreach. A feasible floor and an issue-known report do not themselves prove coverage. Rejection concerns the datewise conditional upper-bound null, not a specific observed cause/date or population mean-loss ordering. Nonrejection does not certify coverage, tail severity, sharpness or financial value.

## Fixed-terminal construction and elementary proof

For a fixed alternative probability u in[alpha,1], let

\[
L_t(u)=\begin{cases}u/\alpha,&I_t=1,\\(1-u)/(1-\alpha),&I_t=0.\end{cases}
\]

Writing `q_t=E[I_t|F_t]`, direct calculation gives

\[
E[L_t(u)\mid\mathcal F_t]
=1+\frac{(u-\alpha)(q_t-\alpha)}{\alpha(1-\alpha)}\le1.
\]

Partition original issue indices by `(t-first_issue) mod (H+1)` over the entire evaluation interval, without year resets. Same-phase successive issues are at least H+1 records apart, so all earlier same-phase factors are known before the next issue. Iterated conditional expectation makes each fixed-phase terminal product have expectation at most1. No independence, stationarity, mixing rate or moment bound on position magnitudes is required for this calculation; report causality, the stated conditional null and label maturity remain essential.

For phase r, mix its whole product over the fixed uniform probability measure on[alpha,1], then average **all H+1 phases with weight1/(H+1)**. Nonnegativity/Tonelli and expectation linearity preserve expectation at most1. Empty phases have empty-product value1 and retain their fixed weight. Do not multiply phase e-values, choose the most favorable phase, adapt weights after future outcomes or trim unfavorable issues.

Each source's entire existing evaluation issue set and last-label terminal are fixed. This construction is a **fixed-time e-value**. No full-filtration supermartingale, arbitrary stopping, optional continuation, running maximum, anytime p-value or simultaneous conditional-coverage guarantee is claimed. Observations can partially reveal a not-yet-mature factor, which is why a full-information anytime claim would require a different argument.

## Exact count-level calculation

If a phase has n observations and k strict breaches, its uniform-mixture value is

\[
E_{n,k}=\frac{1}{1-\alpha}\int_\alpha^1
 (u/\alpha)^k\{(1-u)/(1-\alpha)\}^{n-k}\,du.
\]

Production will evaluate it as an exact positive rational sum. With `r=(1-alpha)/alpha`, start `term=1/(n-k+1)`; for j=0,...,k-1 replace `term` by `term*(k-j)*r/(n-k+j+2)` and accumulate all k+1terms. At alpha1/20, r=19. This follows by substituting u=alpha+(1-alpha)v and integrating the binomial expansion, with no floating product, finite alternative grid or numerical quadrature.

An independent implementation will check the equivalent integer formula

\[
E_{n,k}=\frac{\sum_{j=0}^{k}{n+1\choose j}19^{k-j}}
 {(n+1){n\choose k}}.
\]

Small artificial tests will also use direct polynomial integration and exact enumeration under a boundary Bernoulli law; these are implementation fixtures, not a financial simulation or a power study. The averaged final value and comparisons with thresholds use exact rational arithmetic. Numerator/denominator may be serialized in hexadecimal to avoid decimal conversion limits. Log/scientific displays are approximate labels and must never decide a threshold crossing.

For the fixed56-cell family, the declared per-cell threshold is `56/delta=1120`. Markov and a union bound control erroneous flags among true nulls for a genuinely fixed procedure family, without assuming cell independence. This is a formal fixed-procedure statement. The inspected-sample choice of methods, diagnostic and family does **not** obtain a retrospective5% familywise error guarantee from that division; widening the correction to the98archived reports would not automatically cover the wider research search either. In empirical output, a crossing is named `adjusted_reference_threshold_crossed`, rather than a significance, rejection or coverage-PASS certificate. No unadjusted significance badge or inversion into an anytime p-value will be added.

The fixed uniform prior is a declared evidence construction, not a proven most-powerful choice. The small per-phase record counts at longer horizons and the prior mass assigned to distant alternatives can limit sensitivity. Absence of a threshold crossing supplies no power calculation, equivalence test or reliability certificate. No prior or phase menu will be retuned after the values are inspected.

Evidence magnitude is not a ranking of financial risk, loss quality or calibrated quantile accuracy. Counts, dependence, record horizons and phase sizes differ across cells; large monetary overrun need not produce a larger value. Retain the declared configuration/method order rather than choosing reports by this diagnostic.

## Input and integrity contract

Read only the already successful conditional replica and the explicitly named fresh AR attempt. Use the metadata inventory in `notes/revision-20261022/coverage-input-feasibility-agent.md`:24conditional NPZs, eight reference NPZs and eight fresh AR NPZs,40containers/588headers. Do not treat header inspection as payload verification.

The runner must verify the original16-file closure and selection agreement, AR17-file closure/specification, successful replica/queues/phase receipts, the fresh AR manifest and genuine version2readback, and every consumed container's expected bytes/hash. Use nonsymlink bounded task paths, header inventories before `np.load(allow_pickle=False)`, and rehash consumed/frozen inputs before accepting output. Reuse read-only `run_ar1_replay.prepare_replica`/verification boundaries as appropriate; do not bypass the old diagnostic output lock, remove output folders or forge a replacement PASS.

After headers and hashes pass, verify exact56semantic keys; source/H/W/method/parameter/unit agreement; complete chronological issue arrays; finite one-dimensional float64 targets, floors and reports; floor inequalities; expected refit indices; same source/H target/floor binding across windows and methods; and declared maturity. Strict hits must be computed from those exact saved target/report bytes. Pinball values are not an eligibility or tuning channel. The source/output ranges are FX11927..18551,n6625 and Treasury405..681,n277, for H6/24 and their frozen histories. Do not merge native monetary units across sources.

Any missing, duplicate, altered, nonfinite or incomplete cell stops the closed-family calculation. Do not shrink M, substitute another AR attempt, silently reorder malformed issues, repair a report or discard a failed phase. Partial/failed attempts remain explicit and do not receive a complete-family PASS.

## Implementation, verification and resources

- Root owns `coverage_evalues.py`, `test_coverage_evalues.py`, this design/specification and final integration. The pure kernel uses standard-library exact arithmetic and no financial files.
- A separate implementation task may own `run_coverage_evalues.py` and `test_run_coverage_evalues.py`; tests use synthetic fixtures, not current financial breach values. The runner creates an exclusive attempt directory and aggregate-only public output, with manifest, exact key/phase inventory and execution evidence.
- Before financial computation: finish relevant synthetic tests, independent mathematical/contract review, create a new executable freeze without changing old freezes, publish it and verify actual remote bytes/commit. No forecast replay is needed.
- A single bounded diagnostic pass will produce56summary rows and896phase rows. Each of the eight configurations has H+1phases for each of seven methods; phase counts sum back to every cell's complete issue count. All outputs retain exact rational identities and adjusted-threshold flags.
- An independent scalar readback must recompute every hit/phase count and exact value with the distinct integer formula, without importing the production statistical kernels; preserve its genuine input/manifest bindings and any failure history. No accepted receipt may be borrowed from another attempt.
- One numerical worker; request one thread and observe at most two. Internal stops540seconds/1.5GiB, hard600seconds, RSS ceiling2GiB. No installation, raw download, model fit or parameter search. Measure actual wall/RSS/thread snapshots and distinguish them from limits and root research hours.

Only after the closed-family output and independent readback agree will scientific integration be considered. If evidence is weak or adverse, keep it without widening the prior/menu or changing hypotheses. Main-document changes would then require their own content, source compilation, PDF and public-identity checks. This diagnostic cannot fill compatible unseen-dealer, release-vintage, financial-decision-value or methodological-originality gaps.

## Primary precedent and reading boundary

Henzi and Ziegel, *Valid sequential inference on probability forecast performance*, consulted [arXiv2103.08402v3](https://arxiv.org/abs/2103.08402v3), revision1July2022. Root reread selected physical pp4–13 and the versioned HTML §§2.2,3.1–3.2, particularly Theorem3.3 and Propositions3.4–3.5. The additional pp9–13 cover the delayed stopping distinction, source simulation setup and the weather-forecast application; plotted simulation values were not independently reproduced or visually certified in this revisit. The v3PDF has26pages/901,729bytes, SHA-256 `2e259a65ddca593a95dbe014297f4bdf3d9ceb25cbe6f551fc6230d62c8de886`. It supplies mature binary likelihood-ratio and delayed fixed-terminal combination precedents; the exact one-sided coverage/tower argument above is stated explicitly rather than importing every source claim. Its optional-stopping correction and source simulations were not independently reproduced. This is a revisit of an existing literature line, not new-method credit.

Casgrain, Larsson and Ziegel, *Anytime-valid sequential testing for elicitable functionals via supermartingales*, [arXiv2204.05680v2](https://arxiv.org/abs/2204.05680v2), revision4June2023, is an additional established foundation already recorded in source-register04. Root reread selected physical pp3–14; p10 was visually checked. The36-page/544,188-bytePDF has SHA-256 `909b76d5653633847c072a7aac655333ac2c8265c4370edf6455a9b2ae54878e`. The relevant passages distinguish static mixtures, predictable mixing, bounded moment functions and their null hypotheses. The quantile-identification example states continuity conditions at the quantile. We do not import an equality-identification null at atoms: the present test explicitly uses the weaker one-sided bounded moment `E[I_t-alpha|F_t]<=0` and the displayed direct proof. That bounded hit needs no moment bound on financial magnitudes. Source anytime/power results, OCO algorithms and empirical examples are not inherited or independently reproduced here. The final journal-body equivalence was not checked in this revisit.
