# Source register 45 — functional classes, optimization objects and special riskmetrics

**20 October 2026. Literature phase. Zero new principals or versions.** 210 revisits four articles; 211 extends a fifth. Only these frozen records supply content; nothing is backdated into 41–44. No final topic, design or experiment is selected.

## 1. Cross-source interpretive revisits

| Existing article and recorded actual edition | Selected revisit in 210 |
|---|---|
| Jouini–Schachermayer–Touzi, *Optimal risk sharing for law invariant monetary utility functions*, [19 April 2007 Vienna preprint](https://www.mat.univie.ac.at/~schachermayer/pubs/preprnts/prpr0122.pdf), 28 pages | **4–9**: monetary utility, duality, law invariance, comonotonicity and sup-convolution. |
| Liu–Cai–Lemieux–Wang, *Convex risk functionals: representation and applications*, [24 October 2019 author manuscript](https://www.math.uwaterloo.ca/~wang/papers/2019Liu-Cai-Lemieux-Wang-IME.pdf), 31 pages | **2–6**: class, representation, translation-affinity and monotonicity distinctions. |
| Pesenti–Qiuqi Wang–Ruodu Wang, *Optimizing distortion riskmetrics with distributional uncertainty*, [5 July 2024 author manuscript](https://sas.uwaterloo.ca/~wang/papers/2024Pesenti-Wang-Wang-MP.pdf), 52 pages | **4–6** objective/law classes; **26–27** portfolio and preference/distribution ambiguity propositions. |
| Barrieu–El Karoui, *Inf-convolution of risk measures and optimal risk transfer*, [undated LSE author copy](https://stats.lse.ac.uk/barrieu/Publications/Finance_Stochastics.pdf), 25 pages | **16–18**: market-modified risk, price baseline, common/different market access. |

**Interpretive revisits; no new images or complete proofs.** Earlier edition/imported-proof limits remain. No internal date or final identity is assigned to the LSE copy.

**Original cross-source synthesis — 113 words.**

<!-- SYNTHESIS_1_START -->
These revisits compare four existing functional classes and their optimization objects. Monetary utility for shared wealth, capital risk for wealth, general translation-affine loss functionals and bounded-variation distortion metrics have different sign, monotonicity and cash-response premises. Risk sharing reallocates a fixed endowment; market hedging changes opportunity-adjusted risk; distributional optimization varies plausible laws. Conditional averaging and quantile concentration do not become statistical confidence merely because similar operators appear. An opportunity-adjusted criterion cannot inherit another theorem's law invariance, duality or existence assumptions without checking them. Joint preference/distribution ambiguity and asymmetric market access are already prior work. The passages were interpretive revisits, not new proofs, research design or empirical evidence. Previous edition and external-proof boundaries remain unchanged.
<!-- SYNTHESIS_1_END -->

### Classes and operations that remain distinct

| Class | Variable and cash response | Conditions that cannot be dropped |
|---|---|---|
| JST monetary utility | Wealth/payoff; cash increases utility | Concavity, monotonicity, cash invariance, bounded endowment, law-invariance/duality. |
| Barrieu–El Karoui convex risk | Wealth/payoff; cash reduces risk/capital | Sign, admissible opportunities, properness, pricing baseline. |
| Liu et al. convex functional | Loss; general translation affinity | Cash-additive risk versus cash-insensitive deviation. Convexity/continuity/law invariance do not imply monotonicity. |
| PWW distortion riskmetric | Loss; bounded-variation distortion | May be non-monotone/non-convex; not automatically monetary capital or utility. |

**Sharing** preserves aggregate endowment while changing allocations. **Hedging** uses admissible terminal-gain opportunities to transform risk. **Distributional optimization** varies a law within moment/shape/transport restrictions. Similar notation does not equate these objects or information.

JST averaging is static measurability; PWW concentration averages quantile intervals inside a feasible law family; market gains require admissibility. None is automatically conditional forecasting or same-sample confidence.

A law-invariant starting criterion does not verify every sharing-theorem premise after opportunity adjustment. Exact moments/upper budgets and unrestricted transfers/monotone contracts differ. This is **assumption matching**, not a new obstruction theorem or design.

## 2. LVXY: later selected special-corollary routes

**Peng Liu, Steven Vanduffel, Yi Xia and Jing Yao, “Robust Distortion Risk Metrics with Wasserstein and Unimodal Constraints,” [arXiv:2511.08662v2](https://arxiv.org/pdf/2511.08662v2).** Same **47-page** original: first deposit 11 November 2025; v2 deposit 27 September 2026; PDF title 29 September 2026. No new/current-latest claim.

**Original incremental synthesis — 124 words.**

<!-- SYNTHESIS_2_START -->
The new LVXY routes specialize envelope constructions for particular distortion metrics and a covariance-based multiplier relation. The corollaries retain interior-radius, positive-variance, integrability and nonconstant-normalization conditions. Their piecewise candidates are not universal two-step laws under every Wasserstein constraint. Continuity uses almost-everywhere derivative convergence together with uniform integrability, not pointwise convergence alone. GlueVaR restrictions support specified nonnegative VaR/ES weights, rather than arbitrary preference mixtures. Equal supremum values do not certify attainment for the original discontinuous metric. Proposition 1 supplies an algebraic route to a scalar quadratic relation, without certifying coefficients, root branches or degenerate cases. Selected appendix passages and main conditions were revisited; only image 39 was newly inspected. No formula implementation, numerical root search, complete Appendix A certificate, calibrated radius or observed capital/performance result follows.
<!-- SYNTHESIS_2_END -->

| Accepted 211 scope | Reading and exclusion |
|---|---|
| Appendix A **lower 34–upper 36 before Proof of Theorem 2** | Corollary 1 special-distortion/envelope route. |
| **Lower 38–39** | Corollary 2 continuity/specialmetric routes. |
| **Upper 40 before Appendix B** | Proposition 1 covariance/multiplier route. |
| Main revisits | **11–15** Corollaries 1/2/Proposition 1; **13** Theorem 2 continuity; **15** attainment discussion. |
| Visual / located-only | Original **image 39** inspected. Physical **16** definition and Appendix B on **40** incidentally extracted, not accepted as new detailed reading. Earlier unimodality scope is not restarted. |

Corollary 1 uses affine/flat envelope pieces for concave distortions, upper-quantile VaR, interquantile dispersion and an ES–VaR difference, then invokes Theorem 1. No universal two-step law follows.

Corollary 2 retains endpoint/uniform-integrability control and GlueVaR height/slope restrictions. Equal modified values do not ensure original-criterion attainment.

The covariance/normalizing-variance step is a **supplied route**, not a solver. **Coefficients, breakpoint limits, normalization, strict inequalities, multiplier signs/root branches and executable identities remain uncertified.** Minimum-radius, threshold/large-radius, zero-variance and linear cases cannot inherit an interior formula.

Earlier scope remains unchanged; no full Appendix A certificate. Formal Pesenti/2024 author equivalence remains unverified; no new external-proof reading.

## Evidence limits and recorded fingerprints

Observed tables do not verify population support/regularity or continuum attainment. No moments, radii or preferences were estimated.

Model ES–VaR values are not observed capital changes or time-valid inference. No hypothesis, data or test design is frozen.

| Recorded existing original | Bytes | SHA-256 |
|---|---:|---|
| JST, 19 April 2007, 28 pages | 288223 | 372b80e4bd67d43b914da7a8ad2a556f72f18ff3ceb1c9b81d2f80317c944774 |
| Liu et al., 24 October 2019, 31 pages | 458630 | bfa6e74699e8af4cbf2a568fba434fd69706685baeef267126327c7340db24d0 |
| PWW, 5 July 2024, 52 pages | 884783 | 8be8abe30fdb6dba33f0981a943d30b1b3d18e1004cd77b8f9a56431264136a8 |
| Barrieu–El Karoui, undated LSE copy, 25 pages | 264566 | 8eaaf577d7ac675b6f83c1920d1e87e945346bce04e316da03e69fc98eff2952 |
| LVXY, arXiv2511.08662v2, 47 pages | 787124 | 2c9e58bd80400d7143cdb9138fa12c641c51a4b6476fd14f20c0044e81cad8ff |

Frozen fingerprints are retained without PDF reading/rehashing. **Zero new principals/versions; zero administrative body/root credit.** No observations, programs, solver output, price/profit or experiment obtained/produced. Data/code rights unknown; no contacts, PDFs/images or substantial passages redistributed.
