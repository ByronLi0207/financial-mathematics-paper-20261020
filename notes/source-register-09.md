# Primary-source reading register 09

Accessed 20 October 2026. This register records selected original passages and source documentation. Exact versions and unread material remain explicit. No new empirical result, replication success, final topic or methodological novelty is claimed.

## 1. Ehm, Gneiting, Jordan and Krüger — quantile/expectile score mixtures

**Citation:** Werner Ehm, Tilmann Gneiting, Alexander Jordan and Fabian Krüger, *Of Quantiles and Expectiles: Consistent Scoring Functions, Choquet Representations and Forecast Rankings*, JRSS B 78(3), 505–562 (2016), [DOI](https://doi.org/10.1111/rssb.12154).

**Actual body:** [arXiv:1503.08195v2](https://arxiv.org/abs/1503.08195v2), submitted 17 April 2015; PDF dated 20 April. Selected methods, empirical comparisons and proofs read; journal body unread.

Nonnegative, locally finite mixtures represent regular scalar quantile/expectile scores; the measures need not be probabilities. Normalized extreme-point statements have separate restrictions. Corollaries 2a/2b already provide exact empirical breakpoint checks; expectiles also require forecast-point left limits. This is distinct from population dominance, simultaneous inference and arbitrary grids. Time-series examples use pointwise DM/HAC intervals. Applications concern inflation, recession probabilities and wind speed; joint VaR–ES representation belongs to separate work. Author documentation links murphydiagram and construction programs, not executed here.

**PDF SHA-256:** `3c48c237ea778158664915bcf7b35e205562d9a52ca628372b433b21bcb3546f`.

## 2. Giacomini and Komunjer — conditional quantile forecast combination

**Citation:** Raffaella Giacomini and Ivana Komunjer, *Evaluation and Combination of Conditional Quantile Forecasts*, JBES 23(4), 416–431 (2005), [DOI](https://doi.org/10.1198/073500105000000018).

**Actual body:** [UCL-listed June 2003 author manuscript](https://centreforfinance.org/researchdetail.htm?research=294), 43 pages; selected setup, assumptions, encompassing and application passages. Formal 2005 body unread. Visual checks also covered manuscript pp.12,14,15,20; p.20 concerns simulation/setup.

The framework retains fixed finite estimation memory as evaluation grows; expanding-window fitting is excluded. A recursively updated forecast state differs from an expanding parameter-fit window. Finite instrument orthogonality needs additional information/equivalence assumptions to represent a full conditional target. HAC covariance does not supply those assumptions. Free intercepts can permit bias correction, so improvement from recalibration differs from incremental information in another forecast. Existing S&P500 VaR comparisons are direct financial predecessors. The paper's two-direction testing is not an anytime guarantee; no application code or observations were obtained.

**PDF SHA-256:** `41b57c4f3097bf3b98093c8aa28ab8df6335fb9b00e665fd2771fc290af72793`.

## 3. Proietti — drawdown measurement and prediction

**Citation:** Tommaso Proietti, *Ups and (draw) downs*, International Journal of Forecasting 42(2), 457–473 (2026), [DOI](https://doi.org/10.1016/j.ijforecast.2025.07.008).

**Actual body:** [CEIS Research Paper 576, May 2024](https://www-2020.ceistorvergata.it/public/files/Research_Papers/RP576.pdf), selected definitions, assumptions, measurement and prediction sections. Final body unread; final metadata and indexed excerpts checked.

The object is fixed-window current-endpoint log-price drawdown, distinct from maximum-per-path CED. Assumptions include stationarity, strong mixing, a moment above order two and fixed window length. High/low brackets concern measurement; GARCH path simulations concern a fitted model's conditional prediction. Neither is automatically a finite-sample confidence interval for a population tail mean. The paper directly cites Chekhlov and Goldberg–Mahmoud and already studies stocks, denoising and rolling S&P500 forecasts. The author repository README was read; its MATLAB/toolbox/runtime statements were not reproduced, and market-data rights were not certified. One selected neighbor cannot establish a literature gap.

**PDF SHA-256:** `e442c8fff07d5c2705f3aa9fb3ff2f09f4c24b7019cef514be15f83e005a1f89`.

## 4. Krohn, Mueller and Whelan — FX fixings and execution

**Citation:** Ingomar Krohn, Philippe Mueller and Paul Whelan, *Foreign Exchange Fixings and Returns around the Clock*, Journal of Finance 79(1), 541–578 (2024), [official article](https://doi.org/10.1111/jofi.13306).

**Actual body:** selected final publisher HTML: benchmarks, data, return definitions, transaction robustness, inventory interpretation, liquidity-role calculations and main Appendix. Internet Appendix and replication package unread.

Indicative bid/ask quotes differ from transactions and order flow. Hypothetical client reversal estimates become negative after quoted execution costs, while dealer liquidity-provision estimates are positive; not every individual coefficient is significant. Historical fixing clocks, DST and return-window definitions matter. Contemporaneous postfix flow in explanatory regressions is not an available prefix predictor. These are existing microstructure/execution applications, not a VaR/ES confidence theorem. Spot price changes also require separate funding/cost accounting before becoming an investment payoff. A replication link and article-level license do not establish vendor-data access or redistribution rights.

**Selected-reader extraction SHA-256:** `363649e53613288e8f998c9de7ee6a132e481396d38d0d69448e81b683aa6f49`; this identifies extracted prose, not original publisher bytes.

## 5. Bollerslev — conditional variance and higher moments

**Citation:** Tim Bollerslev, *Generalized autoregressive conditional heteroskedasticity*, Journal of Econometrics 31(3), 307–327 (April 1986), [DOI](https://doi.org/10.1016/0304-4076(86)90063-1); [author-hosted journal PDF](https://public.econ.duke.edu/~boller/Published_Papers/joe_86.pdf).

**Actually read:** journal pp.307–313,315–319,321–326, selected Appendix A1/A2; pp.311,313,326 visually checked. All external asymptotic proofs and plots were not audited.

Under the conditional-Gaussian specification, finite-variance stationarity and higher even moments require different coefficient restrictions. Gaussian standardized innovations do not make unconditional returns Gaussian or provide every return moment. The likelihood discussion separates conditional moment correctness and sandwich covariance; it does not validate arbitrary normal-based tail forecasts. Generic GARCH testing can encounter singular identification. The empirical example concerns historical U.S. inflation and asymptotic one-step forecast-error intervals. No finite-sample distribution-free tail-risk guarantee, mixing rate or known fitted-model moment envelope is inferred. Nelson's separate strict-stationarity theorem was located only at metadata/abstract depth; its original proof remains unread.

**PDF SHA-256:** `60353d437aadda9179df4e7cfcc55f0dd343840b04c6ee7d83285eb33fa17e1a`.

## 6. Ehm and Krüger — forecast dominance via randomization

**Citation:** Werner Ehm and Fabian Krüger, *Forecast dominance testing via sign randomization*, Electronic Journal of Statistics 12(2), 3758–3793 (2018), [DOI](https://doi.org/10.1214/18-EJS1495).

**Actual body:** [arXiv:1707.03035v3](https://arxiv.org/abs/1707.03035v3), submitted 22 October 2018, footer 23 October; selected nulls, convergence, discussion and applications. Formal body unread.

The principal null controls evaluation-period conditional expected score differences at all thresholds; unconditional mean dominance is weaker. A date's same external sign acts across thresholds. Exact sign invariance is stronger than conditional mean equality. In this version, general one-sided size reasoning explicitly depends on a conjectured Anderson inequality; stepwise equality and specified contiguous cases have separate arguments. This is not a claim about the conjecture's current status. Threshold-process convergence, DGP-class uniformity and anytime validity differ. Existing DJIA five-percent quantile comparisons are direct financial predecessors. Code documentation was read; implementation and observations were not obtained or run.

**PDF SHA-256:** `fc0f780b95891eeaf565141258a2ae1e9954cb093b9a5eaee0d48b2cc6a856d7`.

## 7. ALFRED — release dates, vintages and ingestion

**Sources:** official [ALFRED Help](https://alfred.stlouisfed.org/help) and [Download Data Help](https://alfred.stlouisfed.org/help/downloaddata), accessed 20 October 2026; selected explanatory documentation, not observation downloads.

The documented release-date hierarchy prioritizes original-source dates, then provider dates, then first availability in FRED. Database ingestion is not an original-source intraday timestamp guarantee. Download options distinguish full snapshots, changed values, real-time periods and initial-release output. A release without recorded changes can be absent from a vintage list.

These mechanisms do not establish complete first-release DEXUSEU coverage or a successfully retrieved vintage dataset. Displayed metadata-attribute date ranges do not establish observation start dates or rate revisions. Observation/fixing time, source publication, database ingestion and a date-level vintage are separate objects. Current corrected histories cannot automatically stand in for each historical forecast-origin information set. Source-specific reuse rights remain separate from database availability. No observation values, historical features or analysis split were selected.

## 8. murphydiagram — documented data and provenance

**Sources:** official [CRAN reference manual](https://cran.r-project.org/web/packages/murphydiagram/refman/murphydiagram.html), [author Code page](https://sites.google.com/site/fk83research/code) and [Michigan agreement](https://data.sca.isr.umich.edu/agreement.php), accessed 20 October 2026.

CRAN/author documentation identifies version 0.12.2, dated 6 December 2019, with package-level GPL-3. Two quarterly objects document inflation and recession forecasts/realizations, with Philadelphia, Michigan and FRED provenance. Revision warnings do not establish exact historical vintages or row-level reconstruction. The construction ZIP was not requested; no package or observations were downloaded.

The selected documentation does not complete every upstream raw-data permission chain. Michigan's current agreement links CC BY-NC-ND and separately addresses redistribution/commercialization inquiries. Both texts are retained without a legal determination or retrospective allegation about author permissions. Current terms are not historical permissions. The manual also distinguishes relevant sample thresholds from an auxiliary grid and exposes autocorrelation-lag settings; defaults do not justify inference for a new dependent dataset.

## Reading-stage decisions

Keep deterministic empirical comparisons, model-conditional predictions and population statistical guarantees distinct. Preserve source versions, financial decision objects, information timing and source-specific data rights. Continue closest-application reading before selecting a question. No private research appendix, third-party PDF, raw market observations or fabricated result is included.
