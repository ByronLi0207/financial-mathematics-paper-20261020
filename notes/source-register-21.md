# Source register 21 — tail-distribution inputs, estimation risk and event-time diagnostics

**Reading update — 20 October 2026.** This update consolidates completed selected reading. It reports no new project result or selected research design. The systemic-surveillance entry below is a scope upgrade to register03, not another principal entry. Administrative preparation adds no original-body reading credit.

## 1. Cumulative tail violations and parameter-estimation risk

**Zaichao Du and Juan Carlos Escanciano (2017), “Backtesting Expected Shortfall: Accounting for Tail Risk.” Management Science 63(4), 940–958, April 2017.** First online **10 March 2016**. [Formal DOI](https://doi.org/10.1287/mnsc.2015.2342); [actual UC3M institutional postprint](https://e-archivo.uc3m.es/bitstreams/8d7ae519-0cbc-40d9-85d0-bc6bfa0c39b7/download). The retained manuscript is dated **24 August 2015**, not the final issue year.

**Source synthesis — 146 words.**

<!-- SYNTHESIS_1_START -->
Du and Escanciano integrate quantile violations into a truncated probability transform. Correct conditional tail forecasts imply a centered martingale-difference restriction. Mean and finite-lag portmanteau tests distinguish basic limits from parameter-estimation adjustments. The fixed forecasting scheme uses earlier estimation observations and later evaluation observations; the limiting sample-size ratio and estimator influence expansion affect calibration. Stationarity, ergodicity, derivative regularity and negligible initialization effects remain substantive assumptions. A numerical ES report alone does not identify the required tail mapping. The appendix already extends the transform class. An established three-index application estimates a Student AR–GARCH model before evaluating crisis-period forecasts. Its historical rejection comparison does not establish universal forecast superiority. Selected institutional postprint methods and proof routes were read; the final journal body was not compared. Omitted or external empirical-process proofs, current implementation archives, financial observations and reuse permissions remain unverified. Selected autocorrelation restrictions do not certify complete conditional-tail correctness.
<!-- SYNTHESIS_1_END -->

## 2. Duration–severity diagnostics on the violation clock

**Sullivan Hué, Christophe Hurlin and Yang Lu (2024), “Backtesting Expected Shortfall: Accounting for both duration and severity with bivariate orthogonal polynomials.”** [Actual arXiv:2405.02012v3](https://arxiv.org/abs/2405.02012v3); [arXiv DOI](https://doi.org/10.48550/arXiv.2405.02012). Version history records v1 **3 May 2024**, v2 **9 May 2024**, and current checked v3 **12 May 2024, 08:20:37 UTC**. Its title page separately says **14 May 2024**. No final journal publication or body equivalence was verified.

**Source synthesis — 145 words.**

<!-- SYNTHESIS_2_START -->
Hué, Hurlin and Lu pair waiting times between violations with severity measured by tail PIT position. Geometric-duration Meixner moments and uniform-severity Legendre moments provide marginal and selected cross-dependence diagnostics. Ideal continuous conditional distributions motivate the reference law; fitting a financial model does not establish that null. Finite moment projections differ from the infinite characterization conditions. The Wald approximation takes the violation count to infinity, while reported power and application p-values use separate Monte Carlo correction. First-wait retention and final-censoring treatment belong to the event-time procedure. It requires daily PITs, not merely reported VaR and ES. Model-parameter estimation risk is explicitly outside its main implementation. Existing applications estimate Student AR–GARCH models in 2017–2019 and evaluate CAC40 and S&P500 in 2020; MES is already a direct extension. Selected versioned methods and application were read; external characterization proofs, numerical implementation, data provenance and current reuse permissions remain unverified.
<!-- SYNTHESIS_2_END -->

## Actual versions and root selected scope

These ranges identify selected passages, not every line, numerical cell or proof on each page. Auxiliary reading does not enlarge the root's recorded scope.

| Principal source | Actual retained body | Recorded root selected reading | Remaining boundary |
|---|---|---|---|
| Du–Escanciano | 46 physical pages: institutional cover plus45 numbered manuscript pages, dated24August2015; printed page = PDF page − 1 forPDF2–46 | PDF1–30, especially setup, Theorems1–2, Corollaries1–4, AppendicesA–C and empirical design; bibliography43–46 checked; visual checks2,8,10,11,13,23,24,27 | Tables31–41 and figures not comprehensively audited; LemmaA1 proof omitted/delegated; external proofs and final-edition identity unverified |
| Hué–Hurlin–Lu | 43-page arXivv3; physical and printed pages coincide | PDF1,3–18,20–21,25–32,37–38; visual checks1,12,14,17,26,31,32 | Full tables, external completeness/CLT/Monte Carlo arguments and every polynomial display not independently verified |

File-production or repository-modification dates are not assigned as additional scholarly revisions. The2015 postprint and2017 formal reference remain distinct. Tail probabilities, statistical test levels and the number of observed violations retain their separate meanings.

## Scope upgrade only — Systemic Risk Surveillance

**Timo Dimitriadis and Yannick Hoga, “Systemic Risk Surveillance,” [arXiv:2601.08598v1](https://arxiv.org/abs/2601.08598v1), submitted13 January 2026,14:40:30 UTC; title page14 January 2026.** [ArXiv DOI](https://doi.org/10.48550/arXiv.2601.08598). Previously registered in update03; no new principal summary is added.

New selected reading covers CoES/MES in AppendixB.1–B.2, AppendixC Algorithm3 and AppendixD Proposition3–4 proofs, plus the Theorem1 proof invoked by Theorem3. The null requires ideal reference VaR and a conditional CoVaR tail curve. The finite-window theorem and simulation/grid approximation remain distinct. Main bank evidence concerns CoVaR/reverse CoVaR; shortfall extensions have simulation evidence. Root selected PDF36–40,44–49,34–35 and revisited definitions/application pages; other numerical results and outside proofs remain unverified.

The author-linked [replication README](https://github.com/TimoDimi/replication_CoVaR_Monitoring/blob/main/README.md) and [LICENSE](https://github.com/TimoDimi/replication_CoVaR_Monitoring/blob/main/LICENSE) were inspected as documentation only. The repository declares **CC0 1.0 Universal**; this does not establish third-party raw-data rights, exact commit-to-paper mapping or runnable replication. No source program or observations were inspected.

## Original crosswalk of interpretation boundaries

| Question | Distinction retained |
|---|---|
| What forecast information is supplied? | A scalar shortfall forecast, a tail-quantile curve and a realized PIT provide different information. An integral alone does not identify its whole curve. |
| What uncertainty is included? | Testing a model with parameter-estimation adjustment differs from evaluating the issued forecasts as final outputs. Prior estimation and later evaluation blocks need not be independent merely because their dates do not overlap. |
| Which clock drives calibration? | Trading-day sample size, violation count and a prespecified monitoring window are different quantities. A pending censored duration is not a completed event observation. |
| What does nonrejection establish? | Passing selected moments is compatible with departures outside the tested projection; it does not certify the full conditional tail. |
| Which probability claim is available? | A fixed-statistic asymptotic reference, a Monte Carlo approximation and a finite-window known-law theorem retain their own assumptions; none is automatically indefinite monitoring validity. |

Duration VaR methods, PIT-based ES tests and systemic-tail surveillance are established financial predecessors. The recorded connections do not select a new method, application or empirical comparison.

## Access and retained fingerprints

De-duplication of registers01–20 found no prior principal entry for the two new entries. The existing systemic-surveillance entry is updated only in scope. No source search or original-body reading occurred during curation.

The UC3M cover retains an INFORMS copyright notice; public reading access is not redistribution permission. The Hué–Hurlin–Lu arXiv page links CC BY-NC-ND4.0 for the paper. These article notices and the systemic repository's declaration do not establish current financial-data or software rights. Du–Escanciano states an implementation route, but its present archive contents were not inspected. Other raw-data provenance and executable materials remain unverified. This register delivers no original article, observations, source program or substantial third-party passage.

All retained files below were rehashed during preparation and matched the recorded fingerprints. Documentation hashes identify saved web-page responses, not immutable repository commits or raw licence blobs.

| Retained evidence | Bytes | SHA-256 |
|---|---:|---|
| Du–Escanciano, UC3M2015 postprint |756237|`31c5f60eb2bb37cb3e5bd39e2e68ce4e06cbcf176f1135bfe07e935a96ed1e75`|
| Hué–Hurlin–Lu, arXivv3 |795614|`5332d4efdb031953353501fe40b0fe71472b193b1d2d9573404ca3493317de60`|
| Dimitriadis–Hoga, arXivv1, scope upgrade |1036148|`18971bc000e97946d754367d1e6348e3320b0c7a6223443248c6cf4abb311d7a`|
| Systemic-surveillance README web page |222444|`ee40f11a81f7d3dd094a5e61dc5c532a7e275a02729116e8b849c78659404574`|
| Systemic-surveillance LICENSE web page |311214|`5551f9df1472b2e90ac0d037bf9ae5c2ca7c71a46dcd52f66df9009366a57bce`|
