# Source register 13 — pooling distributions, intervals and information

Accessed 20 October 2026. Literature-stage synthesis of three selected original bodies and three explicitly limited abstract/preview screens. Historical findings below are the authors' results, not replications by this project. No financial observations, fitted models, final research question, experiments or manuscript are reported. Publication dates are not popularity measures.

## 1. Distribution pooling, information and calibration

**Tilmann Gneiting and Roopesh Ranjan (2013), “Combining predictive distributions.” Electronic Journal of Statistics 7, 1747–1782.** [DOI](https://doi.org/10.1214/13-EJS823), [actual arXiv v1](https://arxiv.org/abs/1106.1638v1).

Actual reading: selected calibration definitions, internal pooling arguments, transformation constructions and financial application from the 39-page v1. The archive registers v1 on 8 June 2011, while the currently served PDF displays 26 November 2024. A registered 2024 scientific revision or equivalence with the unread 2013 journal body is not inferred. Source SHA-256: `0729ae01b02a39f5cdc1f65879d7869b11ba5b53436363e1d93e2ece50e24f3d`.

An ideal forecast is conditional on a specified information field. Marginal, probabilistic and auto-calibration are different properties; atoms require randomized PITs. Fixed-weight linear pooling has dispersion consequences under the stated component conditions. Spread adjustment and beta transformation modify the pool, but attaining a chosen PIT variance is weaker than attaining uniform PIT or full-information conditional calibration. The source's flexibility result concerns a parameter family's attainability, rather than a finite-data guarantee for estimated parameters. Its S&P500 example already combines volatility and mean forecasts, with only small gains from nonlinear pooling and a stronger model combining the information directly. Historical log-score fitting, calibration diagnostics and uncertainty in fitted parameters remain distinct. A new return series or a beta transformation alone would not establish a new method. Selected internal arguments were read, but all technical boundary cases, external proofs, executable software and numerical results were not independently certified or reproduced.

## 2. Interval aggregation: the rule and its comparator

**Anil Gaba, Ilia Tsetlin and Robert L. Winkler (2017), “Combining Interval Forecasts.” Decision Analysis 14(1), 1–20.** [DOI](https://doi.org/10.1287/deca.2016.0340), [actual INSEAD working paper](https://flora.insead.edu/fichiersti_wp/inseadwp2016/2016-23.pdf).

Actual reading: selected methods, normal-signal model, applications and discussion through the official web reader of INSEAD working paper 2016/23/DSC, dated 22 March 2016, 30 PDF pages. The formal online date is 21 February 2017; the journal body was not separately read. Local PDF bytes were not obtained, so no PDF hash is claimed. Text-response fingerprints are recorded locally and are not PDF fingerprints.

The paper distinguishes endpoint averaging from probability averaging after reconstructing normal distributions. Its midpoint-adjusted probability method is another rule, rather than a synonym for the original probability pool. Separate endpoint trimming can retain different forecasters on each side; selecting whole paired intervals is different. Concavity of its reward score gives an exact advantage over the average component score, not over the best component, and does not preserve coverage automatically. In the homogeneous normal-signal model, pooling information improves location precision while endpoint averaging can retain the original reported width. Correlation and individual overconfidence therefore matter in different ways. The cross-sectional signal calculation is not a time-series independence theorem. Applications already include financial analyst intervals and repeated forecasts of annual macroeconomic outcomes. Multiple origins forecasting the same annual realization do not supply independent annual observations. Original tables, external proofs, observations and implementation were not reproduced.

## 3. Regularization addresses estimated density weights

**Francis X. Diebold, Minchul Shin and Boyuan Zhang (2023), “On the aggregation of probability assessments: Regularized mixtures of predictive densities for Eurozone inflation and real interest rates.” Journal of Econometrics 237(2), article 105321.** [DOI](https://doi.org/10.1016/j.jeconom.2022.06.008), [actual arXiv v3](https://arxiv.org/abs/2012.11649v3).

Actual reading: selected histogram-score definitions, simplex/ridge/log-barrier constructions, subset methods, internal optimization arguments and economic application from the 35-page v3. ArXiv records submission on 30 June 2022; its cover is dated 1 July 2022. The formal December 2023 journal body was not compared. Source SHA-256: `497f03711273c3a5a173f8e2fbc37b19b8ac2261010ce3d2593579009228cd50`.

Diebold, Shin and Zhang regularize linear opinion pools when forecast histories are short relative to the number of forecasters. Simplex weights receive ridge or log-barrier penalties toward equality; partial egalitarian and equal-weight subset constructions provide further alternatives. Fixed convex-penalty fitting has convex geometry, while subset search remains combinatorial. The mixture's realized score differs from an average of individual scores. Histogram forecasts require common bins and valid probabilities; logarithmic fitting requires positive probability for realized outcomes. Penalty geometry and a population or sample optimization objective do not establish future calibration, boundary-uniform uncertainty or anytime inference. The existing survey application already concerns inflation and derived real-interest-rate forecasts. Reported simulations, scores and PIT diagnostics motivate regularization without supplying a universal performance guarantee. ArXiv lists ancillary code and data, but those files and their reuse terms were not audited. No observation, program or computational result was reproduced here.

## 4. Limited screen: an earlier density-combination paper

**Stephen G. Hall and James Mitchell (2007), “Combining density forecasts.” International Journal of Forecasting 23(1), 1–13.** [DOI](https://doi.org/10.1016/j.ijforecast.2006.08.001), [Warwick institutional record](https://wrap.warwick.ac.uk/id/eprint/107711/).

**Reading depth: metadata, publisher abstract and selected indexed preview; zero complete body pages or proofs.** The accessible material describes KLIC-based weights for linear density combinations and a UK-inflation illustration including institutional fan charts. Combining is not reported to help in every case. Exact constraints, uncertainty theory, data chronology and implementation remain unread. The institutional record explicitly lacks a full-text file; a different 2005 article was not substituted. No article-PDF hash or certified theorem statement is available from this screen.

## 5. Limited screen: probability versus quantile averaging

**Kenneth C. Lichtendahl Jr., Yael Grushka-Cockayne and Robert L. Winkler (2013), “Is It Better to Average Probabilities or Quantiles?” Management Science 59(7), 1594–1611.** [DOI](https://doi.org/10.1287/mnsc.1120.1667), [Duke institutional abstract](https://scholars.duke.edu/publication/960692).

**Reading depth: metadata and abstract only; zero body pages or proofs.** The publisher gives 18 March 2013 online publication. The abstract reports equal means, lower predictive variance for quantile averaging, a role for distribution shape, and GDP-growth/inflation survey examples. Exact moment, support, shape, strictness and scoring conditions were not read. Lower predictive variance is not silently equated with better calibration or a uniformly better score. The ordinary PDF route returned an abstract page; no article-PDF hash or original proof is claimed.

## 6. Limited screen: survey-weight optimization

**Cristina Conflitti, Christine De Mol and Domenico Giannone (2015), “Optimal combination of survey forecasts.” International Journal of Forecasting 31(4), 1096–1103.** [DOI](https://doi.org/10.1016/j.ijforecast.2015.03.009), [CEPR DP9096 abstract](https://cepr.org/publications/dp9096).

**Reading depth: formal metadata and the discussion-paper abstract; zero body pages or proofs.** The abstract describes MSFE for point combinations, log scores for density combinations, and positive weights summing to one as shrinkage. This is mature prior work for later density-weight optimization. Exact zero-weight handling, multiplicative updates, convergence, stopping certificates and survey timing remain unverified. Neither the 2015 body nor the identified 2012 university working-paper body was obtained. Later papers' outlines do not substitute for the original convergence argument. No article-PDF hash is available.

## Distinctions carried forward

| Construction or result | What must remain explicit |
|---|---|
| Average CDFs, average quantiles, average endpoints | Different aggregation rules and information requirements |
| Predictive variance, PIT variance, coverage | Different dispersion and calibration objects |
| Fixed-pool analytical property | Its weight, support, information and comparator conditions |
| Fitted regularized weights | Estimation history, tuning and chronological evaluation |
| A convex objective | Its defined domain and the gap between optimization and prediction |
| Historical financial application | Already occupied territory, rather than novelty from a new dataset |

The next synthesis follows proper tail-focused scoring and its closest financial applications. Original body reading, metadata screening, access failures, repository administration and overlapping assistance are logged separately. No six-hour completion is inferred from elapsed clock time.
