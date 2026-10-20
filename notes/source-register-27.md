# Source register 27 — fixed-history risk bootstrap and conditional confidence

**Selected primary-source reading, 20 October 2026.** This register consolidates completed selected reading of three research papers. It adds no new original-body reading, project result or selected design. Formal bibliographic identity and the actual preprints read remain separate.

## 1. Conditional VaR bootstrap with a moving historical state

**Eric Beutner, Alexander Heinemann and Stephan Smeekes(2024), “A residual bootstrap for conditional Value-at-Risk,” Journal of Econometrics238(2),105554.** [Formal DOI](https://doi.org/10.1016/j.jeconom.2023.105554). The formal body was not obtained or version-compared.

Actual body: **[arXiv1808.09125v4](https://arxiv.org/pdf/1808.09125v4)**,117physical pages; official revision record15August2023, displayed title-page date16August2023. These distinct dates are preserved.

**Source synthesis — 142 words.**

<!-- SYNTHESIS_1_START -->
Beutner, Heinemann and Smeekes develop fixed-design residual-bootstrap inference for two-step conditional VaR estimation. Pseudo observations use scales filtered from original returns; refitted parameters and residual quantiles vary jointly, while the terminal risk calculation retains the observed forecast history. Their theorem requires a correctly specified stationary scale model, iid innovations independent of past returns, finite fourth innovation moments, local quantile density and stronger scale-derivative conditions. Joint bootstrap convergence is in probability; the parameter-only result has a separate almost-sure statement. A moving historical state is addressed through merging and additional conditional-inference premises. The recursive design is a comparison procedure whose general validity is not proved here. Rolling CAC40 intervals already supply a financial application. Selected2023preprint statements and proof routes were read; the formal2024body, full auxiliary proofs, executable implementation and materials permissions remain unverified. The result supplies neither finite-sample exact coverage nor indefinite monitoring validity.
<!-- SYNTHESIS_1_END -->

## 2. Conditional ES, threshold estimation and tail influence

**Alexander Heinemann and Sean Telg, “A Residual Bootstrap for Conditional Expected Shortfall.”** Actual body: **[arXiv1811.11557v1](https://arxiv.org/pdf/1811.11557v1)**,36physical pages; submission record26November2018, title page29November2018. [arXiv DOI](https://doi.org/10.48550/arXiv.1811.11557). A matching formal journal article or journal DOI was not verified within the bounded source chain; this is not a nonpublication finding.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_2_START -->
Heinemann and Telg extend fixed-design residual-bootstrap inference to a two-step conditional ES estimator. Estimated volatility parameters and the innovation tail mean vary together, with current scales reconstructed from original observations. The fitted quantile determines tail membership and contributes to the proof even though the final covariance requires no density estimate. The assumptions still include a correct stationary scale model, iid innovations with finite fourth moment, positive local quantile density and local scale-ratio, derivative and initialization controls. The theorem approximates estimation uncertainty through a joint bootstrap law and a historical-state-dependent normal comparison. It does not predict the next realized loss or test issued forecasts for calibration. The inspected2018preprint has GARCH simulations, without a separate market-data application, and retains small-tail undercoverage and interval-ranking qualifications. Selected statements and supplied proof routes were read. A formal edition, external framework, complete numerical evidence, implementation and materials rights remain unverified.
<!-- SYNTHESIS_2_END -->

## 3. Conditional confidence through separated information and merging

**Eric Beutner, Alexander Heinemann and Stephan Smeekes(2021), “A justification of conditional confidence intervals,” Electronic Journal of Statistics15(1),2517–2565.** [Formal DOI](https://doi.org/10.1214/21-EJS1833). The protected formal body was not obtained or version-compared.

Actual body: **[arXiv1710.00643v2](https://arxiv.org/pdf/1710.00643v2)**,54physical pages; official version record19January2019, displayed title-page date23January2019. The actual-v2 theorem numbers are not equated with the unread2021formal edition.

**Source synthesis — 146 words.**

<!-- SYNTHESIS_3_START -->
Beutner, Heinemann and Smeekes justify confidence intervals for unknown conditional prediction functions by separating estimation from recent conditioning information. An independent replicate supplies a conceptual comparison, while sample splitting uses an earlier estimation block and a later prediction block under rate, fading-memory and weak-dependence conditions. Moving conditional laws are compared through bounded-Lipschitz merging. Coverage additionally needs consistent distribution estimation and stochastic continuity; a weak-metric approximation alone does not supply quantile coverage. The specified estimator-rate equivalence restricts admissible split sequences, and a growing mixing gap is only a sufficient dependence argument. The actual2019preprint states unscaled location closeness and separate scaled-length conclusions for standard versus split intervals. It does not provide arbitrary splitting, exact every-history coverage or repeated-monitoring validity. Selected statements and supplied proof routes were read. Detailed model checks are recorded separately; formal2021identity, external proofs and implementation remain unverified. Future innovation uncertainty remains distinct from parameter uncertainty.
<!-- SYNTHESIS_3_END -->

## Actual editions and recorded root scope

Selected ranges do not certify every inequality, numerical cell, plot or external dependency. Supporting records do not enlarge the original reader's scope or hours.

| Research source | Actual edition | Root selected reading | Remaining boundary |
|---|---|---|---|
|Conditional VaR residual bootstrap|117-page arXiv1808.09125v4,August2023|Title/introduction PDF1–4; model, assumptions and main inference5–25; simulation setup26–27; selected application/conclusion prose34–39; main proof routes46–49; end of96–100 for Lemma7/parameter expansion; end of114–115 for recursive design. Existing original-page images17and22 visually inspected.|Other auxiliary proofs and extra simulations unread; tables/figures not audited cell by cell; formal2024body unreviewed.|
|Conditional ES residual bootstrap|36-page arXiv1811.11557v1,November2018|Selected model, assumptions, bootstrap and interval passages PDF1–16; selected interpretation/conclusion17–22; AppendixA.1 supplied proof routes23–31; references35–36 screened. Existing original-page image13visually inspected.|AppendixA.2 pages32–34 only mapped for standardized-Student expressions; no independent derivation validation, external proof reading, real-data application or executable reproduction.|
|Conditional-confidence framework|54-page arXiv1710.00643v2,January2019; printed page=PDFpage−1 after the cover|Title PDF1; selected prediction/model/conditioning6–8; selected inference chain12–30, including re-extracted17–21; main theorem/proof routes35–42 and auxiliary routes43–54. Coverage/quantile passages39–40and48–51 followed. Existing original-page images20and23visually inspected.|Main2–5/9–11 and references/setup31–34 not read in full; external mixing/model-verification and measure-theory proofs unreviewed; formal2021body unread.|

## Original crosswalk of targets and conditions

| Distinction | Boundary retained |
|---|---|
|Innovations versus fitted residuals|An iid innovation premise does not make estimated residuals raw independent data. Shared parameter error enters quantile/tail influence and covariance.|
|Bootstrap design versus forecast-origin history|Fixed-design refitting uses original-history regressors. A recursive historical pseudo path differs, although a recursive comparator can still return to observed history for terminal risk.|
|Finite parameters versus current conditional risk|A fixed parameter/innovation-tail vector can have a conventional limit while the risk's derivative weight varies with the observed prediction state.|
|Conditional bootstrap versus exact conditional coverage|A conditional asymptotic approximation, including merging with a moving normal law, does not establish exact coverage at every history or after arbitrary stopping.|
|Split conditioning versus full observed history|The split coverage statement conditions on the recent prediction block, rather than every observation used in parameter estimation. A finite gap does not make time-series blocks exactly independent.|
|Split rate versus a generic holdout fraction|The actual framework requires asymptotically equivalent estimator scaling. With square-root scaling this entails the estimation-block fraction tending to one; a fixed half split is not the stated construction.|
|Location versus scaled length|Actual-v2Theorem3 gives unscaled location convergence in probability, with separate scaled-length/quantile conclusions. No root-n location equivalence is added.|
|Tail level versus confidence error|The fixed risk probability differs from the interval error probability. The statements are not shrinking-tail asymptotics.|
|One-period forecast versus one-step estimator|The ES paper estimates a next-period risk functional with a two-step estimator. Its historical future-work statement does not itself establish a present-day methodological gap.|
|Density-free covariance versus no density assumption|The ES covariance avoids density estimation, while local positive continuous density remains part of the proof conditions.|
|Fourth innovation moment versus derivative moments|The higher powers12and6 apply to local scale/derivative envelopes, not innovation twelfth moments. Tail-mean existence alone is insufficient.|

Correct scale specification, interior parameters, identification, initialization forgetting and theorem-specific regularity remain substantive restrictions. The VaR paper's misspecified-model suggestion is conjectural in the read edition, and dependent-innovation or boundary extensions are not silently supplied.

The conditional-confidence framework additionally requires valid estimator-law approximation, tight prediction derivatives, rate-scaled forgetting, consistent distribution estimation and the stated continuity/nondegeneracy conditions. Strong mixing is a sufficient route to its dependence premise, not a substitute for the remaining assumptions. Its scalar time-series prediction-function setting is not automatically a multistep cumulative-loss, high-dimensional or arbitrary-drift framework.

A new index, a renamed resampling rule, a changed risk label or an interval graph would not by itself establish a new method or sufficient financial novelty.

## Financial materials and evidence limits

The VaR preprint includes an earlier CAC40 fit and130rolling windows with1146observations per window. These are source sample descriptions, not observations acquired here. Diagnostic nonrejection does not certify innovation iid, and average simulated coverage does not certify each historical state or all repeated reports.

The ES paper contains model-based simulations and no distinct real-asset application section. Its small-tail undercoverage and absence of one uniformly preferred interval must be retained. A favorable VaR interval comparison is not automatically an ES ranking result.

The conditional-confidence source uses prediction functions including AR/GARCH examples. A parameter-function confidence interval is distinct from a prediction interval requiring future innovation uncertainty. Detailed model verification and current runnable materials were not certified.

No financial observations, author programs or implementation packages were obtained in this curation. Current source data/code access, preprocessing and redistribution permissions remain unverified. Public access to a paper does not license unseen observations or software. No original article or substantial third-party passage is delivered.

## De-duplication and original-source fingerprints

Registers01–26 were checked by exact paper titles, author combinations and arXiv/formal identifiers. None of the three assigned papers had an earlier dedicated principal entry. Prior entries on conditional-risk estimation, risk-parameter inference or unrelated conditional tests are related methods, not these sources.

Existing retained original PDFs were rehashed and matched recorded bytes/SHA-256. This verifies evidence identity, not final-version equivalence, full proof correctness, numerical implementation or financial-data rights. Curation itself adds no source-body reading credit.

| Actual original PDF edition | Bytes | SHA-256 |
|---|---:|---|
|Beutner–Heinemann–Smeekes,arXiv1808.09125v4|1146997|8a73af9351d3c7e7013992c9ef60411ca2c81cd74c3ac03ff2d6fa71a955e938|
|Heinemann–Telg,arXiv1811.11557v1|554188|ea0b1f0c3757a35743acf2e922fdb89465d18d202207aff8037277009ce6c5ed|
|Beutner–Heinemann–Smeekes,arXiv1710.00643v2|470997|5098556f0a5a48f2344b0fce68393d7f68dde3390dfa88ca822bcdf42996df38|

