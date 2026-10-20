# Source register 41 — distortion envelopes, feasible averaging and moment uncertainty

**20 October 2026. Literature phase.** Blocks 196–197 extend one existing principal; 198–200 form **one new principal**. Only those five frozen reading records are synthesized. A later brief Theorem 4 route review in block 201 is outside this register; unread labels below refer to blocks 198–200. No design or empirical result is claimed.

## 1. Increment: Liu–Vanduffel–Xia–Yao

**Peng Liu, Steven Vanduffel, Yi Xia and Jing Yao, “Robust Distortion Risk Metrics with Wasserstein and Unimodal Constraints,” arXiv:2511.08662v2**, DOI [10.48550/arXiv.2511.08662](https://doi.org/10.48550/arXiv.2511.08662). [Fixed version](https://arxiv.org/abs/2511.08662v2), [original PDF](https://arxiv.org/pdf/2511.08662v2): **47 physical pages**. First deposit 11 November 2025; v2 deposited 27 September 2026; PDF title date 29 September 2026. These fields are distinct.

**Original incremental synthesis — 130 words.**

<!-- SYNTHESIS_1_START -->
The added appendix routes concern a one-dimensional ordinary Wasserstein ball intersected with exact mean and standard-deviation constraints. Envelope derivatives, endpoint control and uniform integrability support the correlation and cross-moment limits; pointwise derivative convergence alone is insufficient. The radius argument distinguishes the moment-imposed minimum cost, an active constraint and a large-radius regime. For discontinuous distortions, the selected route compares supremum values using local quantile averaging, moment restoration and limits. An extra continuity condition remains in the interior-radius branch. Equal supremum values do not make an envelope optimizer an attained optimizer of the original criterion. Definitions and selected statements were revisited, but the whole appendix and executable formulas were not certified. These are deterministic calculations for specified distributions, moments and budgets, not same-sample confidence calibration, conditional forecast validation or a learned-policy guarantee.
<!-- SYNTHESIS_1_END -->

| Block | Actual selected scope | Visual / unread boundary |
|---|---|---|
| 196 | Appendix A **32–34**, Proof of Lemma 1 through Theorem 1, before Corollary 1. Definitions/Assumption A/statements on **6, 9–10** revisited. | Selected route, not full normalization/boundary/uniqueness certification; external results imported. |
| 197 | Appendix A **36–38**, Theorem 2 proof, before Corollary 2. Statement **13**, lower **14–upper 15** discussion revisited. | Images **36/38** inspected. Corollary 1 lower 34–upper 36, Corollary 2 lower 38–39 and Proposition 1 on 40 before Appendix B remain outside detailed scope. |

Finite second moments, positive reference/target standard deviations and Assumption A's square-integrable derivative/nonconstant normalization are substantive. The budget is **squared 2-Wasserstein distance**. Envelope, convex-order and endpoint uniform-integrability control are not established by a nonzero denominator on a finite grid.

The discontinuity route averages locally, preserves the mean and rescales standard deviation, with an enlarged budget before limits. Interior continuity remains required. Approximation, equal suprema and attained adversarial laws differ; discrete-law quantile conventions matter.

Appendix A is not complete. The imported Pesenti journal result is not certified identical to the author-manuscript routes below.

## 2. New principal: optimizing distortion riskmetrics

**Silvana M. Pesenti, Qiuqi Wang and Ruodu Wang, “Optimizing distortion riskmetrics with distributional uncertainty.”**

| Edition evidence | Actual boundary |
|---|---|
| [Waterloo author manuscript](https://sas.uwaterloo.ca/~wang/papers/2024Pesenti-Wang-Wang-MP.pdf) | **Title date 5 July 2024; 52 physical pages; 884783 bytes.** This is the actual body selected-read. |
| Formal [DOI 10.1007/s10107-024-02128-6](https://doi.org/10.1007/s10107-024-02128-6) | Mathematical Programming **213, 51–106 (2025)**, verified metadata only. Final publisher body unread; no equivalence, numbering or assumption correspondence certified. |
| [arXiv:2011.04889v2](https://arxiv.org/abs/2011.04889v2) | Revised **23 February 2022**, metadata only. Its 46-page body was not acquired, read or version-compared. |

**Original source synthesis — 141 words.**

<!-- SYNTHESIS_2_START -->
Pesenti and coauthors optimize distortion riskmetrics over specified distribution families through envelope replacement and feasible quantile averaging. Their concentration operation is not a statistical concentration inequality. Equivalence requires the appropriate averaging closure, with additional distinctions for discontinuities and infinite interval collections. Equality of suprema, existence and optimizer-set necessity remain separate claims. Fixed-mean central-moment upper bounds support key closure arguments; exact-moment restrictions cannot simply replace them. Moment reductions, portfolio objectives and joint preference/distribution ambiguity already appear in the manuscript, including Proposition 8. Selected statements, supplied argument routes and numerical comparisons were read in the July 2024 author edition. The numerical examples are synthetic/model illustrations, and a rearrangement calculation is explicitly a lower bound. No market holdout, independent reproduction or universal solver accuracy follows. The formal 2025 and older arXiv bodies remain unread; external proofs, literal formulas and edition equivalence are not certified.
<!-- SYNTHESIS_2_END -->

### Actual selected first-pass and argument-route scope

| Block | Selected physical pages | Remaining boundary |
|---|---|---|
| 198 | **1–3 screened**; selected **4–10** definitions/envelope/Definition 1/Theorems 1–2; **14–20** Propositions 2–5, Examples 7/11–14, grid conditions/Theorem 3; **21–23** multivariate/marginal setting/Theorem 4. | Image **8** inspected. Conditions/contrasts, not all formulas or proofs. |
| 199 | Appendix A **39–40**, Example 11/Remark 3/Examples 12–13; A.2 **41**, Remarks 6–8; B.1–B.2 **41–48**, selected Proposition 1/Theorems 1–2/Propositions 2–3 routes. Theorem 3 Jensen route **48–upper49**. | Example 7 display only located. Theorem 4 proof **49–50 unread**; external convex-order/projection originals unread. |
| 200 | Main **23–27**, Theorem 5/Proposition 6/Corollary 1, Examples 17/18, portfolio/Propositions 7–8; selected numerics **28–34**. B.4 **lower50–52**, Lemmas A.1–A.2 and Theorem 5/Proposition 6/Corollary 1 routes. | Image **24** inspected; not every table cell or optimizer. References **35–38** and external Liu2020 theorem unread. |

### Conditions and existing applications

“Concentration” replaces a quantile interval by its conditional mean. The averaged law must remain **inside the uncertainty set**; topological closedness is insufficient. Upper-semicontinuous distortions use specified envelope-disagreement intervals; general discontinuities need stronger closure. Conditional-expectation closure is sufficient, without an automatic converse or finite-to-countable extension.

Bounded-variation metrics need not be monotone risk measures; domain/finiteness restrictions remain. Necessity concerns a **nonempty optimizer set**, not every initial law. Attainment transfers only through the stated feasible operation, not equality of suprema alone.

The moment family fixes mean and **bounds** a central pth moment, p>1. Exact moments are a separate case. Envelope/conjugate-norm reductions retain linear/zero-norm, finiteness and attainment clauses; they are not confidence intervals for estimated moments.

Other premises include interval-constant reference quantiles for the special Wasserstein route, grid alignment/closure for equiprobable spaces, and multivariate loss-shape/monotonicity/marginal closure. Finite-support laws, fixed equiprobable spaces and historical tables differ.

**Joint ambiguity is existing prior work.** Section 6.2/Proposition 8 combines distribution and risk-preference sets under structural conditions. One chosen riskmetric difference with known mean/covariance and long-only simplex weights reduces to scaled minimum variance; another illustration uses inverse-S preferences and a benchmark penalty. Combining those labels or changing assets is not a new construction.

Chosen matrices and Pareto/normal/exponential laws, MATLAB/fmincon and preference grids generate model illustrations. For fixed marginals, the rearrangement-algorithm **RA lower bound** is not an exact finite-dimensional worst case; reported gaps are not universal error bounds. Solver accuracy/runtime were not verified. No financial observations, code or reproduction were obtained.

## Counts, fingerprints and retained limits

The five records identify LVXY as an existing principal and Pesenti–Wang–Wang as one new principal. Proof blocks and metadata do not add articles. The 2024 author manuscript's labels do not certify the formal2025 implications imported by LVXY.

| Recorded exact original | Bytes | SHA-256 |
|---|---:|---|
| LVXY, 47-page arXiv2511.08662v2 | **787124** | **2c9e58bd80400d7143cdb9138fa12c641c51a4b6476fd14f20c0044e81cad8ff** |
| Pesenti–Wang–Wang, 5 July 2024 author manuscript | **884783** | **8be8abe30fdb6dba33f0981a943d30b1b3d18e1004cd77b8f9a56431264136a8** |

Fingerprints are preserved from frozen records, without source-body recheck or version comparison. Optimization equivalence does not establish statistical radii, time-series/all-date coverage or trading performance. Data/code rights remain unverified. No contacts, source PDFs, figures, raw data or substantial passages are redistributed. Administrative **new body/root credit is zero**.
