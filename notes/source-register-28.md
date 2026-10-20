# Source register 28 — model verification, extreme-tail bands and systemic inference

**Selected primary-source reading, 20 October 2026.** This update consolidates completed selected reading of three research sources: two actual working papers and one formal article. It adds no new original-body reading credit, project empirical result or selected design. Source identity, version and scope remain separate.

## 1. Model verification for a conditional-variance prediction function

**Eric Beutner, Alexander Heinemann and Stephan Smeekes, “A General Framework for Prediction in Time Series Models.”** Actual source: **[arXiv1902.01622v1](https://arxiv.org/pdf/1902.01622v1)**,47physical pages; official record submitted5February2019, title page6February2019. [arXiv DOI](https://doi.org/10.48550/arXiv.1902.01622).

A separate formal journal identity was not verified. This source is not renamed as the distinct2021conditional-confidence article, and lack of a verified formal reference is not a nonpublication finding.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_1_START -->
Beutner, Heinemann and Smeekes verify prediction-function conditions in established dynamic models. Their selected GARCH analysis bounds current-variance derivatives and truncation errors using fractional return moments and geometric decay, while importing parameter asymptotics and mixing results. Logarithmic strict stationarity is distinct from finite unconditional return variance. Innovation fourth moments, interior identification and target-specific derivative restrictions retain their separate roles. The recent-history block must grow at a rate that removes old-history effects after estimator scaling. A nonzero intercept derivative and positive-definite parameter covariance establish nondegeneracy for the conditional-variance interval. These arguments do not certify every GARCH variant or prediction function. The closing VaR and ES representations add innovation-tail parameters but do not prove their joint estimation or bootstrap laws. Selected2019working-paper conditions and local proof routes were read. Other model sections, external proofs, formal publication identity and implementation remain unverified; finite-sample and repeated-monitoring guarantees are not supplied.
<!-- SYNTHESIS_1_END -->

## 2. Extreme-tail confidence bands indexed by risk probability

**Shuo Li, Liuhua Peng and Xiaojun Song(2023), “Simultaneous Confidence Bands for Conditional Value-at-Risk and Expected Shortfall,” Econometric Theory39(5),1009–1043,October2023.** [Formal DOI](https://doi.org/10.1017/S0266466622000275). First published online3August2022; the online date and2023issue date differ.

Actual source read: **[official formal Cambridge PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/36337B7E7E1CDC09EEC7045AD07965C7/S0266466622000275a.pdf/div-class-title-simultaneous-confidence-bands-for-conditional-value-at-risk-and-expected-shortfall-div.pdf)**,35physical pages, printed1009–1043. This is the formal article, not an unverified earlier author manuscript. The separate supplement was not obtained or read.

**Source synthesis — 143 words.**

<!-- SYNTHESIS_2_START -->
Li, Peng and Song develop conditional VaR and ES bands over a shrinking interval of tail probabilities at one forecast origin. Their filtered location-scale setting combines iid continuous innovations, regularly varying tails and second-order bias control. Estimator-rate, derivative, initialization, discarded-sample and tail-count restrictions make first-stage error negligible at the tail-estimation scale. Extreme extrapolation emphasizes tail-index uncertainty; intermediate estimation retains order-statistic variation. Multiplier constructions approximate the corresponding indexed limits, with additional normal components in the intermediate regime. The results also address specified upside, downside and relative risk types. Their simultaneous dimension is tail probability, rather than unrestricted dates, assets or repeated monitoring. The formal article's GARCH simulations retain ES undercoverage qualifications. Selected2023methods and supplied proof routes were read; numerical cells and plots were not exhaustively audited. The unavailable supplement, primitive-model proof dependencies, implementation and materials permissions remain unverified. These are established multiple-level risk-inference methods.
<!-- SYNTHESIS_2_END -->

## 3. Systemic-risk estimation through paired residual resampling

**Loïc Cantin, Christian Francq and Jean-Michel Zakoïan, “Estimating dynamic systemic risk measures,” CREST Working Paper2022-11.** Actual source: **[official institutional PDF](https://crest.science/RePEc/wpstorage/2022-11.pdf)**,49physical pages; coverMay2022, manuscript footers25May2022.

A distinct metadata record identifies **Christian Francq and Jean-Michel Zakoïan(2025), “Inference on dynamic systemic risk measures,” Journal of Econometrics247,105936**, [DOI](https://doi.org/10.1016/j.jeconom.2024.105936). Its differently titled two-author body was not obtained. No equality with the three-author2022working paper or final-version theorem identity is asserted.

**Source synthesis — 140 words.**

<!-- SYNTHESIS_3_START -->
Cantin, Francq and Zakoïan combine GARCH-type scales with conditional innovation quantiles to estimate dynamic CoVaR and its distress-versus-central-state comparison. The conditioning events use thresholds or intervals, rather than exact continuous quantile equalities. Paired residual resampling preserves contemporaneous innovation dependence, while parameter and quantile updates retain estimation effects and the observed forecast-origin history. Their joint-bootstrap theorem requires correct stationary scale dynamics, innovation moments, smooth positive target densities, local derivative conditions and consistent density estimates. Its single Newton update is computational, not one-step ES estimation. A Goldman Sachs–Dow Jones example already illustrates the financial risk estimator, without revealing true CoVaR or certifying interval coverage. Multi-asset consistency does not establish arbitrary-dimensional bootstrap inference. Selected2022statements and supplied proof routes were read. Full auxiliary arguments, implementation and data rights remain unverified. The distinct2025formal body remains unread and is not assigned this working paper's theorem numbering.
<!-- SYNTHESIS_3_END -->

## Actual editions and recorded root scope

These are selected ranges, not complete-paper or complete-proof certification. Supporting records do not enlarge root's page ranges, visual checks or reading credit.

| Source | Actual edition and pagination | Root selected reading | Remaining boundary |
|---|---|---|---|
|Prediction-function verification|47-page arXiv1902.01622v1; printed page=PDFpage−1 after cover|Title PDF1; framework assumptions/normalization4–6; GARCH conditional variance12–21; selected extension/risk mapping44–45. Existing original-page images12,13and21visually inspected.|AR/ARMA/T-GARCH sections and full references unread; direct local bounds followed, external QML/moment/mixing proofs not independently read; no separate formal identity certified.|
|Extreme-tail confidence bands|35-page formal2023article; printed page=PDFpage+1008|Selected introduction, model, estimation, assumptions/results PDF1–19; tuning/simulation prose20–22; selected interpretation/conclusion26–27; AppendixA–C selected routes28–34; references34–35screened. Existing original-page images9,11and14visually inspected.|Tables23–25 and figure panels27–28 not audited in full; separate supplement and its lemmas/model proofs unread. Original supplement bytes, pages and hash unknown.|
|Systemic-risk paired bootstrap|49-page CREST2022paper; printed page=PDFpage−1 after cover|Selected title/introduction1–4; target/model/estimation5–8; conditions9; asymptotic statements10–16; paired-bootstrap statement/proof17–20; multi-asset consistency21–22; numerical/application prose22–25/27; selected proof36–38and42–44; multi-asset proof47; references48screened. Existing original-page image17visually inspected.|Pages30–41 only mapped except36–38; Gaussian AppendixA27–29displayed/mapped without independent validation; full auxiliary empirical-process arguments unread; figures/table cells23–27not exhaustively audited;2025body unread.|

## Original crosswalk of assumptions, targets and indices

| Distinction | Applicability boundary |
|---|---|
|Strict stationarity versus ordinary return moments|The GARCH verification uses a logarithmic stationarity condition and fractional return moments for derivative tightness. Innovation fourth moments and a finite unconditional return variance are different claims.|
|One model's innovation assumptions versus another's|The selected GARCH verification assumes mean-zero innovations and density positivity near zero. These do not replace the differently stated assumptions in the fixed-level VaR bootstrap or establish positivity at a remote tail quantile.|
|Representing a risk target versus proving inference|Adding an innovation quantile or tail mean to a prediction-function vector expresses VaR/ES. Joint estimator laws, derivative bounds, covariance consistency and bootstrap validity still require their own verification.|
|Fixed risk level versus shrinking tail level|Fixed-alpha scale/tail inference and the extreme-value paper's shrinking-probability asymptotics use different rates and premises. Conditions cannot be transferred solely because both report VaR or ES.|
|First-stage covariance versus negligible first stage|Fixed-level methods can retain fitted-scale/tail covariance. The extreme-tail band simplification instead requires rates and tail counts making first-stage error asymptotically smaller.|
|Simultaneous tail index versus monitoring time|A supremum across the stated tail-probability interval for a specified risk type is not a general familywise guarantee across origins, assets, strategies or arbitrary stopping dates.|
|Extreme versus intermediate tail regimes|Order-statistic uncertainty is negligible in the leading extreme regime but retained in the intermediate regime. Sharing a leading limit is not equality of finite-sample VaR and ES uncertainty.|
|Time-independent innovation vectors versus independent assets|Paired residual draws preserve contemporaneous dependence relevant to systemic distress. Componentwise independent resampling is not the studied construction.|
|Distress event versus observed future information|CoVaR is defined under a contemporaneous distress event and prior history. The event is part of the target, not an ex ante observed predictor.|
|Computational update versus estimator or forecast horizon|A single Newton bootstrap update is distinct from a one-step ES estimator and from one-period-ahead risk.|
|Bivariate inference versus multi-asset consistency|The supplied bivariate joint-bootstrap theorem does not follow automatically for every multi-asset consistency extension, ES/MES functional or growing-dimensional system.|

The conditional-variance nondegeneracy argument is specific to its gradient and parameter covariance. The extreme-value article's primitive-model restrictions are not replaced with weaker fractional-moment bounds from a different paper. Conditional bootstrap asymptotics and indexed bands likewise do not remove the separate historical-conditioning framework's premises.

These methods and applications constrain broad transfer claims. A new series, another risk grid, another institution pair or a relabelled resampling rule does not by itself establish a distinct method. No project question, financial dataset, tuning choice or experimental design is selected.

## Financial examples, materials and access limits

The prediction-function paper supplies model-verification arguments and financial risk mappings, not a newly obtained empirical dataset. Long-memory and highly persistent extensions retain their own stated difficulties.

The extreme-tail article motivates upper/lower and relative risks through long/short exposure. Its selected numerical evidence is GARCH Monte Carlo, without a separate historical financial empirical chapter found in the selected body. Its ES undercoverage evidence remains part of the record. The formal article bears CC BY4.0; this does not automatically establish licences for source data, software or other incorporated material.

The CRESTpaper's Goldman Sachs–Dow Jones illustration uses an earlier calibration period and later displayed risk paths. Estimated risk paths and observed violations do not expose the true CoVaR or certify bootstrap coverage. Its2022future-work wording does not establish a current absence of later inference or backtesting methods.

No financial observations, executable programs or software packages were obtained during curation. Source simulation settings are not project runs or resource measurements. Current code/data versions, preprocessing and redistribution permissions remain unverified. No original article or substantial third-party passage is delivered.

## De-duplication and original-source fingerprints

Registers01–27 were checked by exact titles, author combinations, arXiv/formal identifiers and CRESTsource identity. No earlier dedicated principal entry was found for these three assigned sources. Related conditional-confidence, risk-parameter and fixed-level bootstrap records are distinct sources, not duplicate principal entries.

The three retained original PDFs were rehashed and matched recorded bytes/SHA-256. This verifies specific retained evidence, not complete-proof correctness, numerical implementation, final-version equality or underlying data rights. Source-body reading credit from this administration is zero.

| Actual retained original PDF | Bytes | SHA-256 |
|---|---:|---|
|Beutner–Heinemann–Smeekes,arXiv1902.01622v1|347576|4bff16b823ae07b58a02fc398282566ed1e4565b0b4351890f3b1b5e003d8a4c|
|Li–Peng–Song,formal2023Cambridge article|564076|f3ae318ab68f57967143a6ac606ef9fc60a2132507873fae8d0590e981bc17d2|
|Cantin–Francq–Zakoïan,CREST2022-11|1182808|602cf9aba0723992a98ab7cd61b29488f91b686bf519c928834accfbf91f8bd9|

