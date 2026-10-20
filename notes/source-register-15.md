# Source register 15 — regional scores, focused pools and financial use

**Compiled on 20 October 2026 from recorded selected-source reading.** Formal bibliographic records and the actual body versions read are distinguished below. This consolidation adds no reading-time credit and makes no final-topic, empirical-result or novelty claim.

## 1. Threshold and quantile weighting evaluate different tasks

**Tilmann Gneiting and Roopesh Ranjan (2011), “Comparing Density Forecasts Using Threshold- and Quantile-Weighted Scoring Rules.” Journal of Business & Economic Statistics 29(3), 411–422, July 2011.** [DOI](https://doi.org/10.1198/jbes.2010.08110); [University of Washington report record](https://stat.uw.edu/research/tech-reports/comparing-density-forecasts-using-threshold-and-quantile-weighted-scoring-rules).

**Actual body/scope:** [Technical Report 533, April 2008](https://stat.uw.edu/sites/default/files/files/reports/2008/tr533.pdf), 22 pages. Existing root reading covers selected PDF pp.1–20, including definitions, Theorem 2.1 and its displayed proof, comparison premises, application descriptions and the moment appendix; pp.6, 10 and 20 were visually inspected. References pp.21–22, the formal journal body and external comparison proofs were not independently read. An original first-online date for the formal article was not established.

<!-- SYNTHESIS_1_START -->
Gneiting and Ranjan distinguish weighting elementary prediction tasks from multiplying an ordinary score by the realized outcome's weight. Their technical report constructs proper comparisons by integrating or summing nonnegative contributions from threshold probabilities or quantile forecasts. Threshold weighting emphasizes locations measured in outcome units; quantile weighting emphasizes probability levels, so the two choices need not express the same preference. Identification is limited to the tasks receiving positive weight, especially on a finite grid. Integrable threshold weights bound the resulting score, whereas bounded weights over an unbounded threshold range need not do so. The report retains separate dependence, moment, covariance estimation and nondegeneracy conditions for comparative inference. Its Bank of England inflation and wind-resource applications demonstrate established regional evaluation across domains. Reported inflation comparisons differ by horizon. These constructions precede later focused financial density pools and transformed kernel scores; they do not themselves establish conditional calibration, tail-mean accuracy or optional-stopping validity. The final journal body, original observations and executable implementation remain unreviewed.
<!-- SYNTHESIS_1_END -->

**Conditions and closest work:** retain the report's stated finite-first-moment working class, nonnegative weighting and appropriate expected-score domain. Later focused equity pooling by Opschoor and colleagues is a direct financial use of related scores. Historical statements about requesting R code do not verify present availability or authorize contact; no original program or observation was obtained.

## 2. Focused density pooling already has a financial application

**Anne Opschoor, Dick van Dijk and Michel van der Wel (2017), “Combining density forecasts using focused scoring rules.” Journal of Applied Econometrics 32(7), 1298–1313, November 2017.** First online **29 May 2017**. [DOI](https://doi.org/10.1002/jae.2575); [Erasmus record](https://repub.eur.nl/pub/100109).

**Actual body/scope:** the [Erasmus public journal-typeset copy](https://repub.eur.nl/pub/100109/REPUB_100109-OA.pdf), 16 pages, identified by its institution as Final Version but retaining early-typeset pp.1–16. Existing root reading selected passages across PDF pp.1–16, especially pp.3–4, 7–9, 11–13 and 15–16; existing definition images were inspected. No correspondence to final issue page offsets is inferred. All result cells, external comparison/optimization proofs, source observations and executable implementation were not independently certified.

<!-- SYNTHESIS_2_START -->
Opschoor, van Dijk and van der Wel estimate density-pool weights using evaluation criteria focused on a common region. Censored likelihood evaluates the density inside that region and retains the probability assigned to its complement. Threshold-weighted CRPS supplies a different objective. Optimizing the mixture's historical score differs from weighting its components according to their individual historical performance, and neither scheme necessarily selects the same weights. The financial application already evaluates stock-index downside forecasts using returns, realized measures and rolling volatility models. Base models and combination weights use different layers of historical information. The regions used to learn the pool are broader than the final one-percent lower-tail VaR target. Reported density and risk comparisons vary across scores and schemes; calibration diagnostics and model-confidence-set membership do not establish uniform superiority. This is close precedent for financial focused pooling and complements the original conditional/censored-score theory. The accessible body has early typeset pagination. Original programs, observations, exact initialization, current data access and redistribution rights were not independently verified.
<!-- SYNTHESIS_2_END -->

**Conditions and closest work:** valid mixture densities/CDFs, a common issue-time evaluation region, defined score contributions and separate statistical-comparison assumptions remain necessary. The source uses rolling 750-day base estimation and a history of evaluated forecasts for pooling; 15%/25% learning regions differ from the final 1% VaR point. Diks and colleagues supply the likelihood-score foundation; a quantile from a density mixture is not generally the average of component quantiles.

## 3. Tail focus differs from selecting extreme verification cases

**Sebastian Lerch, Thordis L. Thorarinsdottir, Francesco Ravazzolo and Tilmann Gneiting (2017), “Forecaster’s Dilemma: Extreme Events and Forecast Evaluation.” Statistical Science 32(1), 106–127, February 2017.** [DOI](https://doi.org/10.1214/16-STS588); [actual arXiv version](https://arxiv.org/abs/1512.09244v1).

**Actual body/scope:** 30-page **arXiv:1512.09244v1**, submitted **31 December 2015, 09:27:14 UTC**, headed as a submission to Statistical Science. Existing root reading selected PDF pp.4–10, 11, 13, 15–17, 19–25 and 29. Plot captions/body were read without a visual audit of every curve. The formal 2017 journal body, external proofs, all tables and numerical reproduction remain unreviewed. A production timestamp is not treated as a new registered version.

<!-- SYNTHESIS_3_START -->
Lerch, Thorarinsdottir, Ravazzolo and Gneiting explain why selecting verification cases after extreme outcomes occur can reward forecasts that exaggerate those outcomes. Multiplying an ordinary proper score by an outcome weight generally evaluates a reweighted distribution. Proper regional alternatives retain all cases through conditional likelihood, censored likelihood or weighted threshold tasks. These constructions identify different information: normalized regional shape, regional probability mass or selected CDF behavior. Propriety does not ensure strong discrimination when extreme events provide little information, and the paper's likelihood-ratio optimality discussion concerns specified independent hypotheses. Its macroeconomic application uses real-time quarterly data and an explicit second-available-estimate convention. Horizon labels therefore depend on the last observed quarter, and current revised histories cannot automatically replace the original vintages. The work is foundational context for focused financial pooling, rather than evidence that one tail score uniformly dominates. The actual body is the 2015 preprint; the 2017 journal body, original programs, observations, external comparison proofs and numerical reproduction were not reviewed.
<!-- SYNTHESIS_3_END -->

**Conditions and closest work:** retain positive finite normalizers, defined score expectations and the comparison test's own dependence/variance assumptions. The GDP/inflation application uses quarterly outcomes rather than cumulative annual growth merely because horizons are longer. Diks's regional likelihood scores and Gneiting–Ranjan's weighted tasks are direct antecedents; the selected iid optimality argument is not a theorem for all misspecified financial forecasts.

## 4. Conditional shape and censored probability mass

**Cees Diks, Valentyn Panchenko and Dick van Dijk (2011), “Likelihood-based scoring rules for comparing density forecasts in tails.” Journal of Econometrics 163(2), 215–230, August 2011.** [DOI](https://doi.org/10.1016/j.jeconom.2011.04.001).

**Actual body/scope:** an earlier manuscript entitled **“Partial Likelihood-Based Scoring Rules for Evaluating Density Forecasts in Tails,” 19 May 2008, UNSW School of Economics Discussion Paper 2008/10**, [public university version](https://wwwdocs.fce.unsw.edu.au/economics/Research/WorkingPapers/2008_10.pdf). Its 31 PDF pages comprise a series cover, title/abstract and 29 printed article pages. Existing root reading selected PDF pp.2, 3, 5, 6, 9–16 and 22–27; pp.12 and 15 were visually inspected. The 2011 body remains unread after ordinary access failures. Neither theorem/equation numbering nor full version equivalence is transferred from the working paper.

<!-- SYNTHESIS_4_START -->
Diks, Panchenko and van Dijk construct regional density scores from partial observation experiments in their May 2008 discussion paper. Conditional likelihood compares the normalized density inside a common region while discarding its original probability. Censored likelihood also retains the event-frequency information, without identifying detailed density shape outside the region. A common Bernoulli selection mechanism extends these constructions to smooth weights between zero and one. Normalization and defined expected comparisons remain essential; smoothness alone supplies no moment or inference guarantee. The draft uses rewards, with larger scores preferred. Its financial application already compares Student and Laplace AR–GARCH forecasts for S&P 500 returns, using historical-window tail thresholds, rolling estimation and asymptotic variance estimation. Density comparisons, VaR checks and ES diagnostics are distinct assessments. These assessments do not establish universal calibration or trading-value results. This source underlies later local-propriety and focused-pooling work. The 2011 journal body remains unread, version correspondence is unverified, and original data and programs were not acquired.
<!-- SYNTHESIS_4_END -->

**Conditions and closest work:** the weight/region is common across candidates; conditional normalizers and censored complement probabilities must be valid, with the required support and expected-score domain. Finite rolling memory is one ingredient rather than the entire asymptotic comparison theorem. The existing Datastream sample was not acquired. Holzmann–Klar's local-propriety foundation is separately covered in register14.

## 5. Transformed inputs, normalized laws and rescaled kernels

**Sam Allen, David Ginsbourger and Johanna Ziegel (2023), “Evaluating Forecasts for High-Impact Events Using Transformed Kernel Scores.” SIAM/ASA Journal on Uncertainty Quantification 11(3), 906–940, September 2023.** First online **17 August 2023**. [DOI](https://doi.org/10.1137/22M1532184); [actual arXiv version](https://arxiv.org/abs/2202.12732v1).

**Actual body/scope:** 34-page **arXiv:2202.12732v1**, submitted **25 February 2022, 14:45:17 UTC**. Existing root reading selected PDF pp.2–15, 19–22, 24–26 and 29–33; pp.9–10 were visually inspected. The appendix was followed for its constructions without independently certifying all abstract-space or boundary cases. The formal 2023 body and supplement, external kernel proofs, full simulations and copula implementation remain unreviewed.

<!-- SYNTHESIS_5_START -->
Allen, Ginsbourger and Ziegel represent threshold-weighted CRPS as a kernel score after transforming forecasts and observations. Their preprint separates transformed inputs, normalized outcome weighting and vertical rescaling of a kernel. These operations assess different laws and require different definiteness, integrability and identification conditions. A transformation directly identifies its pushforward law; recovering the original law requires additional conditions. Normalized outcome weighting needs positive weighted probability mass and can fail to be defined for an ensemble with no selected member. Vertical rescaling of a conditionally negative-definite kernel includes the stated centering terms. Strictness is not inherited by every weighted energy or variogram score. A bounded inverse-multiquadric example has different moment requirements from unbounded distance scores. The precipitation application compares multivariate dependence constructions with common marginal ensembles, while later Cheng work supplies a direct financial application. Functional propriety and reported rankings do not certify temporal uncertainty or financial risk accuracy. The journal body, supplement, external proofs, observations and programs remain unreviewed.
<!-- SYNTHESIS_5_END -->

**Conditions and closest work:** retain the actual transformed-kernel moment domain and the distinct strictness conditions. Energy score's abbreviation ES is distinct from expected shortfall; variogram scoring does not strictly identify the full joint law. The weather case uses 2016–2017 training and 2018–2019 evaluation; precipitation thresholds are impact proxies, not monetary damage laws. Data/code reuse and observed resource use were not verified. Cheng is a direct existing financial successor.

## 6. Weighted multivariate scoring is already used for portfolio risk

**Jie Cheng (2024), “Evaluating Density Forecasts Using Weighted Multivariate Scores in a Risk Management Context.” Computational Economics 64(6), 3617–3643, December 2024.** First online **16 March 2024**. [DOI and official article](https://doi.org/10.1007/s10614-024-10571-y).

**Actual body/scope:** the formal 27-page open journal PDF and selected [official HTML](https://link.springer.com/article/10.1007/s10614-024-10571-y); printed page equals PDF page plus 3616. Existing root reading covers selected HTML introduction/method/inference/application/conclusion passages and PDF pp.4–6, 12–14, 18–19 and 21–23. Tables were inspected for their objects and reported interpretations rather than every cell; all recursions, appendices and operational lags were not certified. A later file-production modification date is not a scientific revision claim.

<!-- SYNTHESIS_6_START -->
Cheng applies weighted multivariate scores to financial density forecasts and portfolio risk assessment, explicitly following Allen and colleagues' transformed-kernel framework. The empirical study compares FTSE100 and S&P500 return models using rolling estimation, common historical thresholds and energy or variogram scoring. It evaluates fixed long-only and long-short portfolios through one-day one-percent and five-percent VaR forecasts, including recent-score-based dynamic model selection. The simulated return draws are next-day bivariate outcomes, rather than multiday path-dependent loss trajectories. Density rankings, coverage diagnostics and quantile-loss model-confidence sets address separate evaluation targets. Their reported advantages differ across quantiles and portfolios and do not establish universal calibration or profitable trading. The source is therefore an existing financial use of weighted multivariate scoring, not merely a weather-method analogy. Its discussion of future multistep forecasting or allocation is not evidence of an unresolved current research gap. Selected formal methods and application passages were read, while every model recursion, operational timing, program, original observation and numerical result was not independently verified.
<!-- SYNTHESIS_6_END -->

**Conditions and closest work:** the source uses rolling 1,000-observation estimation, moment-qualified scores, DM/HAC comparisons and distinct VaR diagnostics. These require their own information/dependence assumptions. The direct Allen citation and the earlier focused pooling paper materially limit a simple weather-to-finance novelty claim. Observations, code, current data access, redistribution rights and exact dynamic-selection timing remain unverified; no new design or experiment is proposed.

## Deduplication, provenance and remaining evidence

All six formal DOIs were checked against source-register01–14 and were absent as primary entries. Gneiting–Ranjan's **2013 “Combining predictive distributions”** is a distinct paper already in register13. Diks–Fang's **2020 portfolio-density comparison** and Holzmann–Klar's **2017 local-propriety paper** are distinct sources already in register14 and are not duplicated here.

This consolidation draws on the recorded weighted-CRPS, focused-pooling, forecaster-dilemma, partial-likelihood, transformed-kernel and financial-application reading sessions. Source links, actual scopes and retained-body fingerprints are supplied here. Preparing this register did not add original-paper reading or certify previously unread proofs.

These sources already cover regional distribution evaluation, focused financial pooling and weighted multivariate portfolio-risk evaluation. A changed asset, region or risk label alone does not establish a new method. Functional scoring, predictive calibration, sample-comparison inference and economic decisions remain separate targets.

Before any use of underlying observations or software, current access, vintage/processing details, licenses and redistribution rights still require their own verification. No paper PDF, raw dataset or executable program is delivered by this register. The unresolved version boundaries and inference qualifications are retained for review rather than silently filled in.

## Fingerprints of the actual retained bodies

The existing local files were rehashed during this administrative pass and all six matched their audited notes. Hashes identify the actual retained versions; they do not authenticate equivalence with unread editions.

| Actual body | Bytes | SHA-256 |
|---|---:|---|
| Gneiting–Ranjan, UW TR533, April 2008 | 301381 | `6714716548988b3aa6e5f3dd7413eb7937c76ed3d42d1739d3b5355604cd7c11` |
| Opschoor et al., public early-typeset 2017 copy | 1695426 | `9cbcc280bea95f74b789e022cc84c025f2ff7b423cfd6ec805f892a3da08c957` |
| Lerch et al., arXiv v1 | 666571 | `e15dde0b65fbd76d125d2193b33978b8b4a4dd6c9b7dde03920a930e3b488d77` |
| Diks et al., UNSW 2008/10 | 421083 | `c9d808128d6d348abc9b9387cf77abacf6f6dcea33bd8212a6e91c946162a172` |
| Allen et al., arXiv v1 | 669851 | `548b035ba8c2153f5edb4cd1fee852e17e6712fcc408e2cc010cabc7f7dc93c0` |
| Cheng, 2024 version of record | 1689330 | `97f813716617355b4a0dffc90ab6157770c4f807687214ecbbe659a2fe00841a` |

