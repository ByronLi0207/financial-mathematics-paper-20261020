# Source register 14 — forecast targets and financial decisions

Verified on **20 October 2026**. This batch follows established references rather than making a recent-popularity claim. It records selected primary-body reading and original synthesis. Literature review remains open: no final topic, empirical results or manuscript is claimed. Reading time is audited separately from publication and elapsed time.

## 1. Distribution fit, predictive usefulness and asset-allocation value

**Andrew J. Patton (2004), “On the Out-of-Sample Importance of Skewness and Asymmetric Dependence for Asset Allocation.” Journal of Financial Econometrics 2(1), 130–168.** [DOI](https://doi.org/10.1093/jjfinec/nbh006); [author-hosted journal-layout PDF](https://public.econ.duke.edu/~ap172/asset_alloc_final.pdf).

**Actual body/scope:** the 39-page journal-layout copy, selected PDF pp.1–8, 10–16, 20–23 and 27–34, including the short optimization appendix; pp.6, 7, 28 and 34 visually inspected. Full copula appendix, external proofs and numerical reproduction remain unreviewed. An exact first-online day was not established.

Patton studies skewness and asymmetric dependence for a CRRA investor allocating between stock portfolios and a risk-free asset. Conditional marginal and copula models use historical information for one-period choices. Specifications are selected before evaluation, while parameters are recursively reestimated. The paper distinguishes distribution fit, predictive usefulness and realized decision value. Comparisons include simple portfolios, short-sale constraints, utility-based fee equivalents and dependence-aware bootstrap procedures. Reported gains from flexible dependence modeling shrink materially under short-sale constraints, and some comparisons with simple alternatives remain inconclusive. The utility objective requires attention to the positive-wealth domain and the source's special numerical tail handling; those choices are not a universal population-integrability guarantee. Forecast-integration draws are distinct from historical verification observations. A utility-indifference fee is also distinct from actual trading costs or profits. Original CRSP observations, executable code and computations were not acquired or reproduced. This is mature precedent for making the financial decision explicit, not evidence of a new strategy here.

## 2. Joint density, portfolio projection and direct univariate forecasts

**Cees Diks and Hao Fang (2020), “Comparing density forecasts in a risk management context.” International Journal of Forecasting 36(2), 531–551.** [DOI](https://doi.org/10.1016/j.ijforecast.2019.07.006); [university working paper, CeNDEF 16-02](https://cendef.uva.nl/binaries/content/assets/subsites/amsterdam-school-of-economics/amsterdam-school-of-economics-research-institute/cendef/working-papers-2016/comparing-density-forecasts.pdf).

**Actual body/scope:** the **5 August 2016**, 50-page working paper, selected pp.1–2, 5–10, 16–25 and 33–34. The formal 2020 journal body was not obtained or compared. Remaining skew-distribution derivations, external proofs and all numerical tables were not independently certified.

Diks and Fang distinguish scoring a joint predictive law, scoring its portfolio-return projection and fitting the portfolio density directly. Rankings among misspecified joint forecasts need not survive projection. Elliptical and selected skew families make portfolio densities tractable. Conditional, censored and penalized weighted likelihood scores emphasize a common region specified using forecast-time information. The application uses a fixed three-stock portfolio, rolling estimation and separate density and VaR assessments. Multivariate modeling does not uniformly improve the reported portfolio forecasts. Dynamic comparisons use overlapping windows and pointwise bands; these are not simultaneous or anytime guarantees. The draft's short appendix relates penalized weighted likelihood to normalized regional shape discrepancy and a mass penalty. That argument was read in this draft; the separately cited original Pelenis paper was not obtained. This is precedent for evaluating the financial object actually required. Observations and programs were not obtained, and neither a new specification nor an experiment has been selected here.

## 3. Regional shape and regional mass

**Hajo Holzmann and Bernhard Klar (2017), “Focusing on regions of interest in forecast evaluation.” The Annals of Applied Statistics 11(4), 2404–2431.** [DOI](https://doi.org/10.1214/17-AOAS1088); [KIT author manuscript](https://publikationen.bibliothek.kit.edu/1000134022/168163681).

**Actual body/scope:** **14 July 2017**, 26-page manuscript, selected definitions/constructions, financial application and full short proofs of Theorems 1, 2 and 4; PDF pp.8 and 26 visually inspected. Theorem 3's general-measure proof in separate supplementary material and the formal journal body remain unread. A later repository posting is not a new scientific revision.

Holzmann and Klar construct locally proper weighted scores. Normalizing a common nonnegative weight produces a law whose strict base score first identifies proportional shape inside the region of interest. Adding an appropriate binary score identifies the weighted mass, yielding stronger local identification. For smooth weights this mass is an expected weight, not necessarily the probability of the weight's positive-support region. Positive normalizing constants, admissible weighted laws and the required finite expected comparisons matter. A single point risk forecast generally does not supply the full weighted law required by these constructions. The paper includes rolling GARCH density forecasts for S&P 500 and Deutsche Bank returns, so regional financial evaluation is already established. Its fixed-weight population arguments, selected iid testing-power discussion and asymptotic forecast comparisons should not be merged into a general adaptive temporal guarantee. Original observations, implementation code and supplementary proofs were not acquired. The reading clarifies what a regional comparison identifies, without selecting a new financial problem.

## 4. Asymptotic tail classification is a different target

**Jonas Brehmer and Kirstin Strokorb (2019), “Why scoring functions cannot assess tail properties.” Electronic Journal of Statistics 13(2), 4015–4034.** [DOI](https://doi.org/10.1214/19-EJS1622); [actual arXiv:1905.04233v2](https://arxiv.org/abs/1905.04233v2), registered **7 October 2019, 07:53:15 UTC**.

**Actual body/scope:** 18-page v2, selected pp.1–16 and the displayed core proofs; references screened. Formal journal equivalence and external proofs were not checked.

Brehmer and Strokorb study max-functionals, whose value on every nontrivial distribution mixture is the larger endpoint value. Examples include specific asymptotic tail descriptors on restricted law classes; fixed quantiles and Expected Shortfall should not be conflated with them. A finite expected-score sign argument proves non-elicitability for nonconstant max-functionals. Infinite-complexity results additionally restrict admissible intermediate functionals and retain an exception when the target image contains its supremum. For entire-distribution reports, a mixture-continuity inequality shows that a fixed proper score can be arbitrarily close to optimal while an available larger max-functional value persists. This is not exact equality for fixed distinct forecasts, a uniform result over all scores, or a finite-sample power or sequential guarantee. The paper separates regional distribution accuracy from asymptotic tail classification. Its discussion preserves the practical relevance of high quantiles and tail expectations, whose evaluation properties differ. No data, empirical computation, new impossibility theorem or correction is produced here.

## 5. Local scale invariance and bounded-outcome robustness

**David Bolin and Jonas Wallin (2023), “Local scale invariance and robustness of proper scoring rules.” Statistical Science 38(1), 140–159.** [DOI](https://doi.org/10.1214/22-STS864); [actual arXiv:1912.05642v4](https://arxiv.org/abs/1912.05642v4), registered **26 March 2022, 17:38:20 UTC**.

**Actual body/scope:** 30-page v4, selected definitions, constructions, Theorems 3/5 arguments, stochastic-volatility illustration, discussion and Appendix C; PDF pp.7 and 14 visually inspected. The historical v1 title was separately checked. The formal 2023 journal body, complete Gaussian formulas and external proofs remain uncompared.

Bolin and Wallin distinguish local scale invariance from unit-change homogeneity. Their local definition concerns second-order expected penalties for small relative perturbations in a location–scale family under explicit regularity assumptions. A proper standardized kernel construction yields scaled CRPS; its logarithmic term and positive predictive spread are essential. Scaling an entire series uniformly preserves ordinary CRPS rankings, while heterogeneous predictive scales change the contributions of different cases to an average. The authors acknowledge that emphasizing absolute errors may be appropriate. Robustness is separately defined for each fixed predictive distribution. Untruncated scaled CRPS is not bounded in the outcome; bounded-kernel alternatives trade away strict local scale invariance, and a bound for each fixed forecast is not automatically common to a dynamic sequence. The stochastic-volatility illustration assumes the latent state is observed. It is not empirical return forecasting or dependence-robust inference. No new dataset, method, tuning rule or empirical result is claimed.

## 6. Point forecasts need a named target or an announced loss

**Tilmann Gneiting (2011), “Making and Evaluating Point Forecasts.” Journal of the American Statistical Association 106(494), 746–762.** [DOI](https://doi.org/10.1198/jasa.2011.r10138); [official Bundesbank record](https://www.bundesbank.de/en/bundesbank/research/making-and-evaluating-point-forecasts-635562); [official-hosted journal-layout PDF](https://www.bundesbank.de/resource/blob/635562/7d3de0f3fc003e5b4864828143f268cf/mL/2012-06-01-eltville-11-gneiting-paper-data.pdf).

**Actual body/scope:** 17-page formal layout, June 2011, selected core definitions, mean/quantile/expectile results, discussion and Appendix A. The hosting route's 2012 conference date is not the article year. External characterization proofs, all multivariate formulas and numerical reproduction remain unchecked.

Gneiting explains why point-forecast evaluation must name a target functional or announce the loss before forecasts are issued. Consistency links the requested report to its optimal decision: squared error targets a mean, absolute error a median, generalized piecewise-linear losses a quantile, and suitable asymmetric Bregman losses an expectile. The chosen score's moment domain must accompany elicitability claims. Outcome weighting generally changes the target to the functional of a normalized weighted law rather than preserving the original target. Strict consistency also permits set-valued quantiles, so it need not imply a unique report. This foundation separates comparisons within one target from comparisons of different decisions. The simulated heteroskedastic example and historical standalone CVaR discussion do not establish trading value, dynamic inference or impossibility of later joint VaR–ES evaluation. The corresponding later joint-risk literature is treated separately in earlier registers. No observations or code were downloaded or reproduced.

## Reading implications and remaining evidence

These sources distinguish a point risk report, a regional law, a full joint law, a projected portfolio law, an asymptotic tail descriptor and a decision made from a forecast. A successful transfer must preserve or explicitly change the object being evaluated and the information available when the forecast is issued. This is a compatibility map for further reading, not a selected design or a novelty claim.

Original observational data and programs for this batch were not acquired. Current raw-data access, versions and redistribution rights remain to be verified before any use. Public article access is not general permission to redistribute the separately referenced data or software. No third-party paper PDF or raw dataset is included in this repository update.

## Fingerprints of the actual bodies read

Hashes identify locally retained source versions; they do not assert equivalence to unread final editions.

| Actual body | Bytes | SHA-256 |
|---|---:|---|
| Patton author-hosted journal-layout PDF | 428643 | `755dde8cc21f464c59dc6078280dc1544435d837f09ba96489d8818991f9a87e` |
| Diks–Fang CeNDEF 16-02, 5 August 2016 | 834388 | `f3dcb6ddd42cddb9a820e2b9166e0ff1d3240a838c7ea01964aa6c64d9e9e8f0` |
| Holzmann–Klar, 14 July 2017 KIT manuscript | 404653 | `133f440ffc261befff979cce2a2d4dd1ffdd12d52f94c9bb1d385d5f4bea225e` |
| Brehmer–Strokorb arXiv v2 | 413373 | `0867065d68d6d13530837c88a7f758e35d641b4097cf894961ccc6b688c687a9` |
| Bolin–Wallin arXiv v4 | 9676879 | `7469022167a77e00972012162f29f5ce00396754fd7fa7c70513117d4fe91c04` |
| Gneiting 2011 official-hosted formal layout | 227162 | `70a05706f94d82ef1e59435a3c64e25a168815ba9a693c6f3ae2a95a4631c55b` |
