# Source register 08: path risk, scores and forecast combinations

Updated 20 October 2026. Primary-source literature record. Each entry distinguishes publication metadata, the version actually read and its reading scope. This is working literature documentation; no final topic, empirical result or completed-duration claim follows. Source PDFs and financial observations are not redistributed.

## 1. Conditional Drawdown and its optimization object

**Alexei Chekhlov, Stanislav Uryasev and Michael Zabarankin, “Drawdown Measure in Portfolio Optimization.”** *International Journal of Theoretical and Applied Finance* **8(1), 13–58 (2005)**. [DOI:10.1142/S0219024905002767](https://doi.org/10.1142/S0219024905002767). Actual source: [author-hosted journal-typeset copy](https://www.math.columbia.edu/~chekhlov/IJTheoreticalAppliedFinance.8.1.2005.pdf), January 2005 production marking; no byte comparison with a separate publisher file.

**Reading:** selected definitions, convexity/LP construction and portfolio application; no full numerical audit or external-proof reconstruction.

CDD averages tail drawdowns over scenario-by-date outcomes, with scenario probabilities divided across the observation grid. It is not the tail mean of one maximum per path. The optimization uses additive cumulative returns and linear exposure restrictions. A familiar LP epigraph computes that finite-model quantity; this does not certify population risk, independent scenarios or dynamic time consistency. The application uses leveraged strategy exposures and synchronized block resampling, rather than an unlevered asset simplex. Its empirical stability results are source-reported, without replication here. Changing wealth compounding, percentages or rebalancing requires a separate mapping check.

**Actual-PDF SHA-256:** `f87a95d160c343970f5c09dbac32b5b8fabf985003dd6c19abc6f970aee6eea9`.

## 2. Conditional Expected Drawdown

**Lisa R. Goldberg and Ola Mahmoud, “Drawdown: from practice to theory and back again.”** *Mathematics and Financial Economics* **11(3), 275–297 (2017)**; online 28 September 2016. [DOI:10.1007/s11579-016-0181-9](https://doi.org/10.1007/s11579-016-0181-9). Actual full text: [arXiv:1404.7493v5](https://arxiv.org/abs/1404.7493v5), submitted 21 September 2016, PDF dated 22 September 2016. Its earlier 2014 title belongs to the same version chain.

**Reading:** selected definitions/proofs, attribution, empirical discussion and AppendixA; final-journal correspondence and every derivative/tie condition not audited.

CED applies a tail mean to the maximum absolute peak-to-trough decline from each path. Its quantile-integral definition handles atoms; strict-exceedance conditional means require the stated continuity. Convexity concerns linear whole-path mixtures, not arbitrary percentage drawdown or compounded weight mappings. Constant-path shift invariance is not monetary cash additivity. The actual author version treats optimization as a theoretical consequence of existing machinery. Equity–bond attribution and dependence sensitivity are established applications. Empirical maxima come from overlapping windows using commercial index data, without an iid uncertainty theorem. A different asset or horizon alone is not a new method.

**Actual-PDF SHA-256:** `f0eaea3619753ef25eb06cd0e6aedefc72c3f5fd7ba4a67d7755ba6f04593517`.

## 3. Score choice for imperfect forecasts

**Andrew J. Patton, “Comparing Possibly Misspecified Forecasts.”** *Journal of Business & Economic Statistics* **38(4), 796–809 (2020)**; online 31 May 2019. [DOI:10.1080/07350015.2019.1585256](https://doi.org/10.1080/07350015.2019.1585256). Actual source: [author-hosted final journal PDF](https://public.econ.duke.edu/~ap172/Patton_JBES_2020.pdf) and directly linked supplement dated 26 January 2019. The 2016 working-paper reference is not the formal publication year.

**Reading:** principal definitions/propositions, selected counterexample discussions, actual application and necessary supplement proofs; not all auxiliary derivations.

Nested information, ideal conditional functionals, negligible estimation error and integrable scores support a common population ranking. Relaxing a condition permits sensitivity, rather than forcing every pair to reverse. Misspecification can also change the best parameter projection when the score changes. Homogeneity preserves a fixed score's response to unit conversion; it does not make all homogeneous scores agree. Financial quantile/distribution illustrations are simulations. The actual inflation-survey application shows sample score sensitivity, with the stated lack of fixed-shape DM rejection for the consensus comparisons. These are expected-score results, without simultaneous or anytime inference.

**Final-PDF SHA-256:** `8174685431b6789c3cb387781a449daccd18f59bc74c51d4407a6566c6e0f26a`.

## 4. ES score-family dominance: early manuscript boundary

**Johanna F. Ziegel, Fabian Krüger, Alexander Jordan and Fernando Fasciati, “Robust Forecast Evaluation of Expected Shortfall.”** *Journal of Financial Econometrics* **18(1), 95–120 (2020)**; online 4 February 2019. [DOI:10.1093/jjfinec/nby035](https://doi.org/10.1093/jjfinec/nby035). Actual full text: **“Murphy Diagrams: Forecast Evaluation of Expected Shortfall,” [arXiv:1705.04537v1](https://arxiv.org/abs/1705.04537v1)**, submitted 12 May 2017, PDF dated 15 May 2017. Formal body not obtained.

**Reading:** v1 §§2–4/6 and necessary AppendixA/B/D passages; selected figure checked. No claim about unobserved final revisions.

Nonnegative elementary-score mixtures characterize the stated joint-score class. The main S2 subclass omits the separate quantile-only component but still uses VaR. Population dominance over every threshold differs from one score's ranking or a finite sample curve. The v1 main test assumes temporally independent score differences and uses finite-grid sign relabeling; it expressly discusses unresolved exchangeability/size issues. Those qualifications are not claims about the unread final edition. Figure 2 intervals are pointwise. Existing S&P500/DAX applications compare HEAVY, GARCH and historical simulation; repeating those diagrams on another index does not establish novelty.

**Actual-v1 SHA-256:** `a8156a9af6deca08972e7abfaa1fab325d8c290d64510dc88dc7079299ceca0d`.

## 5. ES forecast encompassing and pseudo-true targets

**Timo Dimitriadis and Julie Schnaitmann, “Forecast encompassing tests for the expected shortfall.”** *International Journal of Forecasting* **37(2), 604–621 (2021)**. [DOI:10.1016/j.ijforecast.2020.07.008](https://doi.org/10.1016/j.ijforecast.2020.07.008). Actual sources: [DNB/KOPS formal article](https://d-nb.info/1232176745/34) and selected internal supplement in [arXiv:1908.04569v3](https://arxiv.org/abs/1908.04569v3), submitted 28 August 2020, PDF dated 31 August 2020.

**Reading:** formal §§2–4 and AppendixA, selected supplement proof passages and author code-entry descriptions; no execution or complete 65-page audit.

Joint, auxiliary and strict tests restrict combination parameters minimizing joint FZ0 expected loss. Strict restricts inputs, not the strength of a dominance claim. Misspecification-robust covariance concerns sampling around a pseudo-true target; it does not restore a different estimand. Main practical restrictions leave intercepts free. Density, identification, moment and interiority conditions exceed ES existence; classical convex-weight boundary testing is explicitly excluded from this theory. IBM/S&P500/DAX applications and author-provided replication entrances already exist. Code versions, raw-data licensing and successful execution remain unverified. This method is distinct from equal raw forecast loss and whole-score-family dominance.

**Formal-PDF SHA-256:** `a28d0f638bb241419c8c04c7e8bde52bc84e04ca8d600affedde7da331b64ecb`.

## 6. Multistep encompassing and boundary inference already exist

**Timo Dimitriadis, Xiaochun Liu and Julie Schnaitmann, “Encompassing Tests for Value at Risk and Expected Shortfall Multistep Forecasts Based on Inference on the Boundary.”** *Journal of Financial Econometrics* **21(2), 412–444 (2023)**; online 28 November 2021. [DOI:10.1093/jjfinec/nbab004](https://doi.org/10.1093/jjfinec/nbab004). Actual full text: [arXiv:2009.07341v1](https://arxiv.org/abs/2009.07341v1), submitted 15 September 2020, PDF dated 17 September 2020. Formal 2023 body not obtained.

**Reading:** v1 definitions, constrained links, main theorems, AppendixA, selected HAC supplement and financial discussion; not all 73 pages.

Convex/no-crossing weights can place encompassing parameters on a boundary. The estimator has a cone-projected Gaussian limit, producing nonstandard Wald critical values. Untested nuisance blocks cannot generally be discarded. Fixed-h ahead and aggregate forecasts have different targets; stationarity, beta mixing, conditional densities, moments and HAC restrictions remain substantive. This v1 uses correctly represented conditional VaR–ES relations and describes misspecification extensions separately. Its S&P500 application already includes one-day, ten-day-ahead and ten-day-aggregate forecasts, with reported finite-sample limitations at longer aggregate horizons. Combining previous robustness with this boundary result requires an actual joint argument, not two citations.

**Actual-v1 SHA-256:** `8724fb889f52a4f70462d9ca9432b347defb9cc8f5087c9176ffba6fdc03f98c`.

## 7. Density-free CVaR endpoints with one-sided support

**Philip S. Thomas and Erik Learned-Miller, “Concentration Inequalities for Conditional Value at Risk.”** *ICML 2019, PMLR 97:6225–6233*. [Official record and final PDF](https://proceedings.mlr.press/v97/thomas19a.html). The inspected official record provides no DOI; no unverified identifier is substituted.

**Reading:** final definitions, Theorems 3–4 and displayed CDF-envelope proofs, discussion and selected synthetic-comparison setup; no full comparison-proof or numerical audit.

For one fixed loss law sampled iid, a genuine upper support cap supplies an upper CVaR confidence endpoint; a lower support endpoint supplies the lower direction. Discrete/mixed distributions are allowed without a density condition. Alpha denotes worst-tail mass, unlike quantile-confidence conventions elsewhere. The observed maximum legitimately occurs in the lower formula without being a population support cap. The fixed-sample DKW envelope is an existing distributional-confidence method; it is not automatically uniform over calendar looks, changing conditional laws or selected portfolios. A valid bound can be uninformative in small samples. Experiments are synthetic interval comparisons, without a financial portfolio implementation.

**Final-PDF SHA-256:** `ee63754468562a6433c350cc292f7517857d9d53bfe469f3bc926c65d5dcdbd7`.

## 8. Exact Monte Carlo ranks and nuisance parameters

**Jean-Marie Dufour, “Monte Carlo tests with nuisance parameters: A general approach to finite-sample inference and nonstandard asymptotics.”** *Journal of Econometrics* **133(2), 443–477 (2006)**; online 30 August 2005. [DOI:10.1016/j.jeconom.2005.06.007](https://doi.org/10.1016/j.jeconom.2005.06.007). Actual source: [author-hosted journal-typeset PDF](https://jeanmariedufour.research.mcgill.ca/Dufour_2006_JE_MCT.pdf), retaining ARTICLE IN PRESS markings. The 2000 draft was not obtained.

**Reading:** selected rank/nuisance/set/plug-in propositions and necessary appendix proofs; auxiliary continuity lemmas not fully audited.

Finite-sample ranks require exchangeability including the observed statistic. Independent uniform labels handle ties; plus-one p-values have a finite simulation grid. Full nuisance-supremum p-values control level, potentially conservatively. Restriction to a random set with coverage tending to one yields an asymptotic result; its proof retains exclusion probability. A finite grid maximum or fitted-null simulation does not automatically inherit full-domain validity. Working alternative likelihoods can define statistics, while correct null simulation and matching failure/selection rules remain necessary. Simulating an asymptotic boundary law is a different guarantee. These are mature methods, without a new financial experiment here.

**Actual-PDF SHA-256:** `e97415409de226701c1fec5d3e039f246f5e86d057bb26355ff86088cd1784dd`.

## Working status

These sources establish close existing methods and applications. No paper count or elapsed clock substitutes for the required active reading. The next stage remains literature review until its actual duration and timing conditions are met. No holdout results, selected specification, finalized paper or empirical success is claimed.
