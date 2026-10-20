# Source register 06: distributional ambiguity, tail risk and dynamic consistency

Updated 20 October 2026. This register continues the primary-source reading record. It reports selected full-text reading with exact version boundaries; none of these entries represents a new empirical result or a finalized topic. Third-party PDFs and market data are not included.

## 1. Wasserstein uncertainty sets and statistical coverage

**Peyman Mohajerin Esfahani and Daniel Kuhn, “Data-driven distributionally robust optimization using the Wasserstein metric: performance guarantees and tractable reformulations.”** *Mathematical Programming* 171, 115–166 (2018). [DOI:10.1007/s10107-017-1172-1](https://doi.org/10.1007/s10107-017-1172-1). Online 7 July 2017; issue September 2018. Actual source: [published 52-page PDF](https://link.springer.com/content/pdf/10.1007/s10107-017-1172-1.pdf).

**Reading:** selected statistical setup, Theorems3.4–3.6 and necessary proof passages, printed pp120–128; calibration discussion pp155–161 and selected AppendixA. Earlier optimization reading is recorded separately. This is not whole-paper verification.

The empirical distribution is built from iid observation vectors; assets within a vector may be dependent. A stated exponential norm-moment condition supports a conservative distribution-ball coverage radius. On that common event the robust expected-cost bound covers feasible decisions, including the optimizer chosen from the same sample. This is a training-sample confidence statement about expected cost of a fresh draw. Practical holdout, cross-validation and bootstrap radius calibration already appear in the paper. Arbitrarily smaller tuned radii, changing conditional laws and dependent returns need their own justification. Unknown concentration constants are not automatically calibrated by a sample estimate.

## 2. Where empirical transport rates come from

**Nicolas Fournier and Arnaud Guillin, “On the rate of convergence in Wasserstein distance of the empirical measure.”** *Probability Theory and Related Fields* 162, 707–738 (2015). [DOI:10.1007/s00440-014-0583-7](https://doi.org/10.1007/s00440-014-0583-7). Online 18 October 2014; issue August 2015. Actual source: [published 32-page PDF](https://link.springer.com/content/pdf/10.1007/s00440-014-0583-7.pdf).

**Reading:** selected statements and proof passages in §§1–6, including the complete displayed Theorem1 proof; selected dependence results in §7.1–7.2. No complete external-proof or constant audit is claimed.

The paper distinguishes expected transportation cost from probability bounds and separates dimensional, polynomial-tail and exponential-tail regimes. Its transport cost equals the powered Wasserstein distance for orders above one; a cost budget must be rooted before calling it a distance radius. The critical dimension introduces logarithmic terms. Specified mixing and Markov assumptions also yield expected-cost extensions, which must not be called the iid exponential concentration theorem. Moment and dependence constants remain substantive inputs. An expected-cost bound can give a conservative probability statement through Markov's inequality, but an effective sample-size substitution alone does not establish a theorem for financial returns.

## 3. CVaR with atoms and optimization

**R. Tyrrell Rockafellar and Stanislav Uryasev, “Conditional value-at-risk for general loss distributions.”** *Journal of Banking & Finance* 26(7), 1443–1471 (July2002). [DOI:10.1016/S0378-4266(02)00271-6](https://doi.org/10.1016/S0378-4266(02)00271-6). Actual source: [author manuscript dated 28 November 2001](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf), 34 pages; final typeset text was not line-compared.

**Reading:** selected definitions and variational results pp2–6, threshold/constraint and convexity passages pp8–10, and selected finite-scenario/index-replication analysis pp12–26. No full numerical replication.

CVaR retains the required fraction of mass at a quantile. Consequently a strict or weak exceedance average need not equal CVaR for an atomic distribution. An auxiliary-threshold minimization provides the exact functional and supports convex or finite-scenario linear-programming reductions under the stated conditions. The paper already studies chronological index replication and reports out-of-sample limitations. Exact optimization of empirical scenario CVaR does not supply a population confidence interval, prove independence of returns or certify future conditional risk.

## 4. Multiperiod risk and Bellman's principle

**Philippe Artzner, Freddy Delbaen, Jean-Marc Eber, David Heath and Hyejin Ku, “Coherent multiperiod risk adjusted values and Bellman's principle.”** *Annals of Operations Research* 152, 5–22 (2007). [DOI:10.1007/s10479-006-0132-6](https://doi.org/10.1007/s10479-006-0132-6). Online 14 November 2006; issue July2007. Actual source: [ETH author draft dated 16 November 2004](https://people.math.ethz.ch/~delbaen/ftp/preprints/adehk-or.pdf), 20 pages, not the final journal edition.

**Reading:** selected §§1–5, including the short main equivalence proofs and the six-leaf example. Final-edition theorem numbering was not assumed identical.

For bounded claims, a fixed filtration and a closed convex dominated probability family, conditional continuation pasting supports recursive worst-case valuation and the stated time-consistency/Bellman equivalences. Conditional coherence alone is insufficient. Updating one fixed static ES family, constructing fresh local TVaR constraints, and nesting a tail criterion can yield different values and different admissible law families. The source's finite-tree example already shows why a blanket claim that same-level nesting is always more conservative needs qualification. Risk-assessment probability families are not automatically pricing-martingale families.

## 5. The stable-family foundation

**Freddy Delbaen, “The Structure of m–Stable Sets and in Particular of the Set of Risk Neutral Measures.”** In *In Memoriam Paul-André Meyer: Séminaire de Probabilités XXXIX*, Lecture Notes in Mathematics1874, 215–258 (2006). [DOI:10.1007/978-3-540-35513-7_17](https://doi.org/10.1007/978-3-540-35513-7_17). Actual source: [ETH preliminary version, May2003](https://people.math.ethz.ch/~delbaen/ftp/preprints/Stablesets.pdf), 36 pages, rather than the 44-page final chapter.

**Reading:** selected stability, conditional valuation, recursion and hull passages supporting the preceding paper. This is not a full chapter or complete version comparison.

Multiplicative stability of dominated densities permits event-dependent continuation pasting under the stated closure and initial-information conditions. Finite closed horizons and infinite/open horizons need different qualifications. A continuous-martingale-filtration stable-hull result cannot be transplanted to every discrete tree. Local martingale measures provide a financial example, while arbitrary stress probabilities need not have that pricing interpretation. The filtration, terminal claim, numeraire and law family must be specified before transferring a dynamic optimization argument.

## 6. Regression-based ES diagnostics

**Sebastian Bayer and Timo Dimitriadis, “Regression-Based Expected Shortfall Backtesting.”** *Journal of Financial Econometrics* 20(3), 437–471 (2022). [DOI:10.1093/jjfinec/nbaa013](https://doi.org/10.1093/jjfinec/nbaa013). Advance Access27 September 2020. Actual source: [published 35-page text hosted by the German National Library](https://d-nb.info/1261739701/34).

**Reading:** selected model, assumption, theorem and implementation text pp439–453, empirical discussion pp461–463 and main appendices pp464–468. The separate technical online supplement was not obtained.

Strict and Intercept ESR accept external ES forecasts alone but retain an internal quantile regression. Under misspecification the asymptotic target is a pseudo-true parameter. The final paper explicitly distinguishes this target from conventional ES null restrictions and studies approximations near scale models. A misspecification-aware covariance does not itself repair a wrong null center. Predictability, density, moments, identification and dependence conditions are material. The tests are fixed-window asymptotic diagnostics; they do not supply arbitrary-stopping false-alarm control.

## Implications for later method transfer

| Intended statement | Required distinction |
|---|---|
| A robust optimizer has a statistical guarantee | Specify the sampling law, calibrated uncertainty set and expected-cost target. |
| Empirical tail risk was computed exactly | Keep optimization accuracy separate from population uncertainty. |
| A dynamic risk criterion is time-consistent | Specify the law family and verify the appropriate pasting/recursion condition. |
| An ES-only diagnostic is valid | State the internal quantile model, pseudo-true center and sampling assumptions. |

These are existing foundations. They guide the comparison of candidate financial questions; a replacement dataset alone will not be presented as a new method. No experiment, result, final topic or completed-duration claim is introduced by this register.

## Version fingerprints

The SHA-256 values fix the actual locally read bytes; PDFs are retained locally and are not redistributed here.

| Source copy | SHA-256 |
|---|---|
| Esfahani–Kuhn published2018 | `f432383cc1fce8b7b00badd686eb67fbcf90ce5c67c7558244e42750f6c98c43` |
| Fournier–Guillin published2015 | `b012cbad9334e2494edcdf0b48e1317d8db51c60c866719395283123ea764fdf` |
| Rockafellar–Uryasev author20011128 | `3787172ff2065c0ca3d233b4aa31b503dff7c327745bd079e0a0d9c17ff4f4ab` |
| ADEHK author20041116 | `5c72bca6aa62db193dde15fbd430458243ac6f32db549e03ba02662947430b62` |
| Delbaen preliminary200305 | `f8a80332d1c70ff98c0a0339807a4e216ed132076865bf2bfdb6e0a4f76bc8e2` |
| Bayer–Dimitriadis published2022 | `85541237f783d272712e7c8d649a84de8ddd6e6f4f24396fe7f19cd75cbe841e` |
