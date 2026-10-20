# Source register 30 — extreme distortion risk and fitted-filter tail inference

**Selected primary-source reading, 20 October 2026.** Two principal articles consolidate completed selected reading. Each article's main body and associated supplement form one entry. Actual editions, numbering and unread dependencies remain separate. This administrative curation adds no source-body reading, financial observations, computation or selected design.

## 1. Extreme Wang risk measures and their selected supplementary proofs

**Jonathan El Methni and Gilles Stupfler (2017), “Extreme Versions of Wang Risk Measures and Their Estimation for Heavy-Tailed Distributions,” Statistica Sinica 27(2), 907–930.** [Formal DOI](https://doi.org/10.5705/ss.202015.0460).

Actual sources read: the **[official journal main PDF](https://www3.stat.sinica.edu.tw/sstest/oldpdf/A27n221.pdf)**, 24 physical pages, and its **[official separate supplement](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A27n221s.pdf)**, 26 physical pages. The main source displays final pagination beginning at 907 alongside an older manuscript text layer; physical PDF pages govern the recorded scope. Received December 2015 and accepted May 2016 are manuscript-history dates. The exact online publication day and a distinct supplementary revision date were not verified.

**Source synthesis — 132 words.**

<!-- SYNTHESIS_1_START -->
El Methni and Stupfler estimate distorted risks above high quantiles in an iid, regularly varying heavy-tail model. Approximation-based and empirical-quantile estimators have distinct existence, consistency and Gaussian-inference requirements. Selected supplementary proofs retain second-order bias in population approximations and explain its estimator-specific cancellation or amplification. Extreme extrapolation shares a leading tail-index fluctuation across a fixed finite collection; it is not a calendar-time or continuous-level confidence corridor. Stronger integrability, a joint anchor/tail-index law and explicit extrapolation rates remain substantive. Poker-swing and automobile-insurance examples already illustrate the construction, with deterioration near moment boundaries and no universal superiority. Main statements, selected local proofs and application passages were read. A middle empirical-process proof segment, external originals, detailed numerical audits and materials rights remain unverified. Threshold-event conditioning is distinct from financial-history conditioning; fitted dependent residuals need additional theory.
<!-- SYNTHESIS_1_END -->

## 2. Tail inference after estimating a dependent-series filter

**Jonathan B. Hill (2015), “Tail Index Estimation for a Filtered Dependent Time Series,” Statistica Sinica 25(2), 609–629.** [Formal DOI](https://doi.org/10.5705/ss.2012.212).

Actual main source: the **[official formal PDF](https://www3.stat.sinica.edu.tw/statistica/oldpdf/A25n211.pdf)**, 21 physical pages, with printed page equal to 608 plus the physical PDF page. Received July 2012 and accepted March 2014 are manuscript-history dates; the exact online publication day was not verified.

The associated **[official linked technical appendix](https://www3.stat.sinica.edu.tw/sstest/oldpdf/A25N211s.pdf?art=11&num=2&sup=s&vol=25)** is titled *Technical Appendix for “Tail Index Estimation for a Filtered Dependent Time Series”* and explicitly headed **Statistica Sinica (2014): Preprint**. It has 20 physical pages. Its principal result is numbered Theorem 2.1 and its uniform-order-statistic result Lemma 2.2. Its exact revision day and line-by-line equivalence with the 2015 formal article were not certified. These are distinct actual editions associated with one principal article.

**Source synthesis — 139 words.**

<!-- SYNTHESIS_2_START -->
Hill studies tail-index inference after estimating a parametric filter while allowing the filtered process to remain dependent. Local uniform tail regularity, distributional smoothness, neighborhood beta-mixing and a restricted intermediate count control the approximation. Filtering error must vanish at the stipulated product rate; parameter consistency alone is insufficient. The Gaussian limit concerns the reciprocal tail exponent and retains a dependence-sensitive scale. Parameter-indexed order-statistic uniformity does not establish a band across dates or risk levels. GARCH examples distinguish estimator rates and retain an unverified second-order premise in one error-filter setting. Portfolio and volatility motivations are financial, but the inspected main evidence is simulation. Selected formal statements and separately labelled 2014 supplementary local proof routes were read. Formal-version equivalence, external dependencies and remaining model proofs remain unverified. This tail component alone supplies neither a complete conditional-risk confidence procedure nor general misspecification protection.
<!-- SYNTHESIS_2_END -->

## Actual editions and recorded root scope

These are selected ranges and supplied proof routes, not complete-paper reading or independent certification of every proof. Administrative consolidation does not enlarge the recorded root scope.

| Article and actual component | Recorded root selection | Remaining boundary |
|---|---|---|
| El Methni–Stupfler, 24-page formal main | Original PDF 1–13: motivation, distortion/threshold conditioning, iid framework, AE/PL constructions, Theorems 1–3 and intermediate/extreme distinctions. Selected numerical/application interpretation 16–21; end metadata/reference 24 screened. Original images 8, 12 and 16 visually inspected. | Numerical tables 14–15 and all cells/figures 16–20 were not individually audited. Extraction repeated adjacent manuscript layers; unavailable or truncated portions were not reconstructed. No complete 24-page claim. |
| Same article, 26-page official supplement | PDF 1–7: supplied local proofs of Theorems 1–3. PDF 8–11: Lemmas 1–3 and local proofs. PDF 12: Lemma 4 statement and initial setup. PDF 16: closing Gaussian-integral/covariance route and Lemma 5 opening. PDF 17–18: Lemma 5 statement/proof. Existing images 7, 10, 11 and 17 visually inspected. | Lemma 4's middle proof 13–15 and supplementary tables/figures 19–26 unread. External regular-variation and order-statistic/empirical-process originals unread. The selected routes do not certify the entire supplement. |
| Hill, 21-page formal main | PDF 1–2 and 4–9: motivation, tail convention, Assumptions 1–4, Theorem 1, variance discussion, Lemma 1 and Remark 9. Model examples 11–13; selected simulation setup/comparison interpretation 14–17; end metadata 21 screened. Original images 5, 7 and 8 visually inspected. | PDF 3 was only partly displayed. Main 10's ARMA example and later 18's results/table were not fully audited; plots 16–17 not visually interpreted. Full references and external model proofs unread. Main-paper scope is not silently expanded by its older appendix. |
| Same Hill article, associated 20-page 2014 preprint appendix | PDF 1–3: restated conditions/statements and setup. Selected supplied routes 3–10: filtered log-tail statistic, trimmed derivatives and Jacobian bounds. Theorem 2.1 closing reduction 10–11; Lemma 2.2 process/order-statistic route 11–12. Existing images 1, 2, 10, 11 and 12 visually inspected. | Image 3 was not inspected in depth. Model proofs 13–18, references and external originals unread. Exact equivalence with the formal 2015 conditions/numbering and independent correctness of all supplied arguments were not certified. No complete 20-page claim. |

## Conditions and mature proof components

El Methni–Stupfler work with an explicitly iid sample and a positive regularly varying tail index. Continuity and strict tail-quantile increase support the threshold-conditioned interpretation. The source's sufficient conditions distinguish integrability for population approximation from the stronger envelopes for its Gaussian results. Finite tail expectation alone does not verify their sufficient Gaussian-inference conditions.

The approximation-based estimator combines an intermediate order statistic with an estimated tail-index factor. Its distributional statement needs their joint law, not just a consistent tail-index estimate. Population second-order terms can remain nonzero. The selected plug-in proof cancels matching deterministic shifts when centered at its specified true risk; that is an estimator-specific argument, not permission to ignore bias elsewhere.

Extreme extrapolation requires a diverging anchor count, a rarer target level, negative second-order parameter and the stipulated remainder/rate conditions. Logarithmic amplification makes the leading tail-index error dominate the intermediate estimator's own error under those conditions. The inherited limit need not be centered Gaussian. The finite fixed collection of distortions is not an unrestricted family or a continuous-level band. The selected covariance route comes from an iid tail process, not an arbitrary financial long-run covariance.

Hill permits a filtered target to remain dependent but requires more than a tail at one true parameter. The formal conditions include stationarity/ergodicity, smooth distributions and derivatives, local uniform regular variation, suitable derivative envelopes and summable beta-mixing for the parameter-neighborhood process. The intermediate count and tail-bias rates are restricted. The parameter estimation error must be negligible after multiplication by the specified tail-count and logarithmic rate. Consistency alone does not establish that separation.

The 2014 appendix's selected supplied arguments account for changing both trimmed log-tail sums and their random order threshold when replacing the parameter by an estimate. The final reduction invokes a true-parameter Gaussian base law, parameter-local derivative control and a parameter-uniform order-statistic approximation. These routes were read as supplied author arguments. The base tail-statistic theorem, mixing empirical-process results and other external approximations were not independently read or proved. Their use does not supply a feasible variance estimator or every downstream risk-confidence requirement.

Hill's main GARCH examples distinguish estimator-specific rates. Heavy-tailed innovations can make ordinary Gaussian quasi-likelihood slower than root-n, which changes permissible tail-count restrictions. One error-filter example retains an imposed general second-order premise that was unresolved in that discussion. The selected older appendix does not enlarge verification of those uninspected model proofs or resolve that premise. A historical boundary is not evidence of a current methodological gap.

## Crosswalk of objects, indices and financial inference

| Distinction | Interpretation retained |
|---|---|
| Threshold event versus financial history | Conditioning a loss distribution on exceeding a quantile does not condition on the information available at a financial forecast origin. An iid threshold-risk theorem is not automatically a conditional time-series risk theorem. |
| Tail-exponent convention | Hill uses a power-law exponent whose reciprocal is the extreme-value index used in the Wang-risk framework. Definitions must be translated before comparing rates or variances. |
| Intermediate versus extrapolated risk | The estimators have different scales, bias terms and integrability demands. Sharing an extrapolated leading fluctuation does not establish equal finite-sample accuracy or universal estimator dominance. |
| Integration coordinate versus time | The covariance's quantile-integration coordinates are not dates or serial lags. An iid covariance calculation does not establish serial-dependence validity. |
| Fixed distortion vector versus uniform corridor | A finite-dimensional joint limit is different from simultaneous inference over a compact continuum of risk levels, many assets, future dates or stopping times. |
| Parameter uniformity versus risk-level uniformity | Hill's local parameter index controls substitution of an estimated filter. It is distinct from the tail-probability index in the previously recorded conditional-risk corridor framework. |
| Marginal tail component versus complete risk interval | Filtered-tail inference alone does not provide current forecast-state error control, infinite-history truncation, distortion integrability, extreme extrapolation bias and a chosen confidence-coverage formulation. |
| Misspecified filter versus correct forecast law | Inference for a resulting filtered target satisfying Hill's premises does not certify that an arbitrary misspecified model gives the true conditional VaR/ES law. |
| Known-parameter reduction versus ignored estimation | A rate-based negligibility result applies only in its stated regime. It cannot discard first-stage uncertainty under different tail counts, estimator rates or downstream targets. |

The conditional-risk material already recorded separately adds its own model, bias and indexed-coverage requirements. Neither source here establishes their conjunction by using similar terminology. Changing an asset, filter or dataset alone does not establish a new method.

## Existing applications, adverse evidence and materials

The Wang-risk paper already illustrates its construction using alternating poker-result swings, including a detrended version, and inflation-adjusted large automobile claims from Secura Belgian Re. Diagnostics and threshold choices do not prove iid sampling after construction or detrending. Selected numerical prose retains worsening accuracy with heavier tails or poorer tail approximation and instability near integrability boundaries. The approximation-based estimator does not universally dominate the empirical-quantile estimator. Historical samples do not observe the true tail functional or certify interval coverage.

Hill motivates estimated portfolio weights, volatility processes and residual-tail inference. The inspected main evidence consists of AR/GARCH simulations rather than a verified historical financial empirical chapter. Dependence-aware variance estimates can matter in the reported comparisons. Simulation counts optimized against known truth are not a feasible threshold-selection guarantee for historical observations. Detailed table cells, source programs and simulations were not reproduced.

No observation dataset, author program, preprocessing workflow or current data/code redistribution permission was obtained or verified in this curation. Public readability of the journal main files and supplements does not establish a blanket materials licence. Source calculations are not project runs or measured resource budgets. This register provides original synthesis and source identifiers, without redistributing the source PDFs or substantial source passages.

## De-duplication and original fingerprints

Registers 01–29 were checked by exact titles, DOI identifiers and original-source identity. Neither principal article had a dedicated earlier entry. Related conditional-risk, distortion and tail-inference references concern different sources; an earlier citation alone is not prior body reading. The main/supplement pair for each article remains one principal entry.

The four retained original PDFs were rehashed and matched the recorded byte counts and SHA-256 values. These hashes identify the actual files, not equality across their editions, complete proof correctness, observation vintages or executable implementations. This administrative curation adds zero source-body reading credit.

| Actual retained original | Physical pages | Bytes | SHA-256 |
|---|---:|---:|---|
| El Methni–Stupfler, official main | 24 | 552395 | 74036d43003930af594368089dae51ed42aaf9ec972b62f033a062a508fec581 |
| Same article, official supplement | 26 | 188847 | 40850ce363a07f0b23f9a43fcc9c05f595319968ff7661c08b3039f0256faa5b |
| Hill, formal 2015 main | 21 | 1174604 | 20200ce6b0659aa14cd1dcd38fea61a198f46b9721574b5fc4f28a67554b820a |
| Same Hill article, associated 2014 preprint appendix | 20 | 280149 | b6d7c22fb251b68a39139d73d1f736a2729784ff9c1fb8abcdb8a4fe1e90e474 |
