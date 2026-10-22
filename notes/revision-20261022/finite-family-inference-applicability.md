# Finite-family inference routes for the sampled-peak comparison

22 October 2026. This is a primary-reading and applicability note, not a newly executed test. No Reality Check, SPA, bootstrap, financial covariance, confidence interval or p-value is calculated. The accepted 22-page / 26-reference main paper and all financial forecasts remain unchanged. These background sources are not silently added to the main reference count.

## The actual originals and reading boundary

| Source | Consulted body and fingerprint | Actual root scope |
|---|---|---|
| Halbert White (2000), *A Reality Check for Data Snooping*, *Econometrica* 68(5):1097–1126, September; [DOI](https://doi.org/10.1111/1468-0262.00152) | [University of Wisconsin faculty teaching copy](https://users.ssc.wisc.edu/~behansen/718/White2000.pdf), publisher-formatted, 30 pages / 259,584 bytes; SHA-256 `675eb3226dee3af4dfa8089410f9bbf0a2798c7b58985c8334c42fb4983a9743` | Extracted main text and selected appendix routes across physical 1–28; mathematical glyph corruption limits literal formula certification. Physical 3, 5, 9, 12, 21 and 23 were additionally rendered and viewed in full. References and external proofs were not certified. |
| Peter Reinhard Hansen (2005), *A Test for Superior Predictive Ability*, *Journal of Business & Economic Statistics* 23(4):365–380, October; [DOI](https://doi.org/10.1198/073500105000000063) | [Kevin Sheppard public teaching copy](https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Hansen.pdf), publisher-formatted rather than author-hosted, 16 pages / 382,192 bytes; SHA-256 `fb5ada1987f86b1f07d721d6fb1707cf9029c1fa0271d5532dfb791ff8790761` | Main text 1–14, appendix 15, references 16 as locators; physical 3, 4, 8, 13 and 14 rendered and viewed in full. Source simulations, tables and outside proofs were not independently reproduced. |

White's body was unavailable in the earlier access-only reading 78. This ordinary public institutional acquisition supplies genuine new body reading; it does not rewrite that old zero-page record. Hansen restores the exact hash already consulted in reading 17, so it is a directed rereading, not a newly discovered article. Source PDFs remain private, with no redistribution license inferred from access. The acquisition helper's metadata work and root's reading are separate activities.

White studies a finite comparison family and dependent bootstrap approximation, including estimated-parameter and finite-window routes. The growing-estimation branch has additional rate/estimation conditions; the rolling-window discussion on physical 12 treats a fixed-history estimate as part of a transformed process. Hansen uses a stationary, sufficiently mixing relative-loss vector with moments above order two; studentization and data-dependent null centering reduce sensitivity to poor alternatives. Its stated framework does not cover general growing recursive estimation. Those are different scopes, not a universal ban on updating forecasts. Neither paper establishes the present data's assumptions by citation.

Hansen's original Table 6 and following discussion make the family issue concrete: the subsequently considered 352-alternative universe has reported consistent SPA p-value .048; including the earlier 3,304 alternatives produces a 3,656-alternative universe and p-value .100. These are the source's historical outcomes, not recomputed numbers for this project and not a claim that every additional alternative raises every implementation's p-value.

## A coherent question, if a later protocol chooses it

Within a declared source, target, issue-origin set and scoring contract, one possible relative-loss vector is

\[
d_{k,t}=\rho_{.95}(P_{t,H}-C^{\rm ref}_{t,H})
       -\rho_{.95}(P_{t,H}-C^k_{t,H}),
\qquad k=1,\ldots,m.
\]

Positive mean relative performance favors the alternative. Rewriting that expectation as the difference of two separate expected losses requires those expectations to be well defined; finite relative-loss moments alone do not resolve an infinity-minus-infinity expression. A finite-family null would be that every component's expected improvement is nonpositive. Rejecting that null would support the existence of an improvement within the specified universe and population model. It would not say every candidate improves, identify a universally best family, establish conditional coverage, show a causal feature effect, or price an actual financing intervention.

The existing 90 summary means are not the required time-series input. Their sources, issue counts, horizons and units differ, and they discard serial and cross-model information. A later implementation needs aligned per-origin loss differences and the full declared family, with common resampling time indices where a joint bootstrap is used. Independent resampling of each method would destroy cross-model dependence. An alias does not create a new distinct forecasting rule; dependence across genuine alternatives is allowed and must not be confused with an independence requirement.

Restricting one test to a single source/H is a convenient scientific contract, not a universal mathematical requirement. A deliberately formulated multivariate hypothesis can encompass different prespecified targets, provided its vector, alignment, scaling, references and joint assumptions are defined. Concatenating the current heterogeneous summary table does not perform that construction. Studentizing components does not itself make incompatible observations synchronous or restore information that was discarded.

## What does and does not block a transfer

1. **Floor atoms and nonsmooth loss are not an automatic rejection.** A loss-series comparison is different from a test of estimated quantile coefficients. For any fixed target P and reports a,b, the classical pinball loss obeys

   \[
   |\rho_\tau(P-a)-\rho_\tau(P-b)|
   \le \max(\tau,1-\tau)|a-b|.
   \]

   This follows by integrating its two report-wise slopes, −tau and 1−tau, including the kink by continuity. Thus suitable report-difference moments are one sufficient route to relative-loss moments, even with atoms. The inequality proves no actual population moment bound, mixing rate or variance condition. White's growing-estimation parameter-expansion branch additionally invokes local differentiability and derivative domination in Assumption A.1; Lipschitz loss alone does not verify those premises. Treating a fixed finite-window predictor as part of the relative-loss process is a distinct route. A conditional-quantile parameter theorem's positive-density assumption should likewise not be imported indiscriminately into every loss-based comparison.

2. **Finite memory helps specify a route; it does not finish the argument.** Under appropriate primitive-process conditions, a fixed finite-history function can inherit short-memory properties. This study's relevant history includes target maturity, older raw features, update state and the issue query, not merely W rows. Deterministic calendar/refit phase and permanently retained validation choices also require a stated stochastic treatment. The current finite saved vectors neither establish strict stationarity nor refute every suitable heterogeneous-process alternative. The [conditional-predictive-ability note](peak-comparison-inference-transfer.md) records one distinct mature route and its actual indexing conditions.

3. **Estimation and research selection remain different.** A forecast may causally refit using genuinely mature past outcomes under a fixed update rule. A fully specified online family selector may also update from mature earlier losses without requiring a separate validation split. Neither permission validates an investigator's later choice of which research family, score, horizon or bandwidth to emphasize. The [whole-procedure note](whole-procedure-selection-and-unseen-evidence.md) distinguishes those choices and the custody record for an untouched evaluation.

4. **The bootstrap contract needs actual conditions.** White's displayed stationary-bootstrap route and Hansen's route have different rate/estimation conditions; their settings cannot be combined into a theorem assembled from convenient pieces. Hansen's Lemma 1 uses q_n tending to zero with n*q_n^2 diverging, not just a chosen finite block length. Its recommended variance estimate and joint resampling are not the same operation as resampling independent sparse-grid means. More resamples improve Monte Carlo resolution, not the number of financial observations or the truth of a population assumption. No block parameter is selected here.

5. **Identical reports need deliberate handling.** The Treasury full-pool KNN/F identities have exactly zero difference and cannot be studentized by dividing by a positive variance invented from two method labels. This does not mean every joint covariance matrix must be invertible, or that every maximum statistic is invalid in the presence of correlated/duplicate alternatives. The selected method's precise nondegeneracy conditions matter; a fixed exact identity can instead be recognized as such before formulating a genuine comparison.

6. **Overlap and horizon are not interchangeable with a dependence model.** Targets share future records, while report state can retain older observations. H+1 spacing removes shared outcome records on the stated record clock, but does not establish iid losses or an effective sample size equal to the number of sparse starts. Under a fully conditional zero-mean null a particular covariance cutoff can follow from maturity and the tower property; unconditional equal mean alone does not give that cutoff. The owning conditional-predictive-ability note supplies the elementary counterexample and its distinct assumptions.

## Decision for the present package

Mature finite-family inference is a possible route to stronger research; sample reuse does not make all statistical inference impossible. Applying it responsibly would require a specific estimand/null, admissible comparison universe, selection treatment, loss alignment, population working assumptions, resampling/variance rule, multiplicity and stopping/reporting contract. These are scientific choices, not a demand that a finite dataset prove every population assumption. None is automatically supplied by changing a bibliography entry or naming a familiar test.

This batch therefore preserves the existing descriptive findings. The numerical freeze and actual reproduction remain useful execution evidence; later exploratory additions remain labeled. The fixed-procedure coverage derivation and its inspected-sample calculation are kept distinct, and none of its 52 noncrossings becomes a calibration PASS. No new Reality Check/SPA result is appended to rescue a favorable historical ranking. The present limits also do not annul the original chronological definitions or turn every causal update into leakage.

A subsequent study can choose a properly specified inferential route, obtain compatible genuinely unseen records, or evaluate an actual financial decision. These are distinct ways of adding substantive evidence; they are not all simultaneous requirements, and none guarantees publication. The current package remains a bounded mature-method application/model-validation benchmark with modest originality.
