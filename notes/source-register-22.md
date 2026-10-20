# Source register22 — joint systemic-risk reports and spectral distribution diagnostics

**Selected primary-source reading, 20 October 2026.** This register consolidates completed selected primary-source reading. It reports no project empirical result or selected research design. Administrative curation adds no new original-body reading credit.

## 1. Joint systemic-risk identification and ordered forecast comparison

**Tobias Fissler and Yannick Hoga (2024), “Backtesting Systemic Risk Forecasts using Multi-Objective Elicitability.” Journal of Business & Economic Statistics 42(2), 485–498.** [Formal DOI](https://doi.org/10.1080/07350015.2023.2200514); [formal institutional record](https://research.wu.ac.at/en/publications/backtesting-systemic-risk-forecasts-using-multi-objective-elicita-7/). DOI metadata records online **30 May 2023**, separately from the2024 issue.

Actual primary edition: [arXiv:2104.10673v4](https://arxiv.org/abs/2104.10673v4), revision posted **6 February 2022, 18:05:57 UTC**; title page **8 February 2022**. It contains53 physical pages with the integrated author supplement. The publisher route was access-limited; the final journal body and supplement were not obtained or compared. This reading does not certify final-version equivalence.

**Source synthesis — 147 words.**

<!-- SYNTHESIS_1_START -->
Fissler and Hoga jointly identify systemic-risk reports by adding reference VaR under specified quantile and integrability conditions. Standalone nonidentifiability results concern rich distribution classes, not every restricted model. Vector scores use lexicographic priority: reference VaR first, then the systemic component. This ordering is neither a scalar weighted score nor a multiple-testing criterion. Their comparison tests require a score-difference central limit theorem, consistent covariance estimation and stated moment/dependence conditions. These inference premises are stronger than moments needed merely to define shortfall. Finite instruments constrain fewer implications than full conditional calibration, while a finite joint report contains less information than a complete conditional tail curve. The rolling S&P500/DAX application changes marginal and copula specifications together. Selected 2022 manuscript methods and supplement passages were read; final-edition identity, outside proofs, numerical implementation, observations and current data/code permissions remain unverified. Population identification and score consistency do not provide finite-sample or anytime inference.
<!-- SYNTHESIS_1_END -->

## 2. Spectral backtests of reported predictive distributions

**Michael B. Gordy and Alexander J. McNeil (2020), “Spectral backtests of forecast distributions with application to risk management.” Journal of Banking & Finance 116, article 105817, July 2020.** First online **16 May 2020**. [Formal DOI](https://doi.org/10.1016/j.jbankfin.2020.105817); [institutional record](https://eprints.whiterose.ac.uk/id/eprint/159163/).

Actual primary edition: the institution's [accepted manuscript with Online Supplement](https://eprints.whiterose.ac.uk/id/eprint/159163/1/spectraltest20200330_combined.pdf), title pages **30 March 2020**,52 physical pages. Acceptance is recorded as24March2020; that event and the manuscript date are distinct. The accepted file is not a verified typeset version of record or the separate2018 working-paper body.

**Source synthesis — 150 words.**

<!-- SYNTHESIS_2_START -->
Gordy and McNeil weight reported PITs across probability levels to target selected regions of a predictive distribution. Bounded transformed values have tractable null moments; point masses recover exceedance indicators. The selected transformed-report null uses past reported PIT information and is weaker than full-information ideal forecasting. Finite lag instruments test selected necessary moment implications. Unconditional and conditional tests use asymptotic reference laws, not exact finite-sample or anytime guarantees. Additional kernels can reveal missed directions but may create redundant coordinates and singular covariance. Evaluation concerns issued forecasts without correcting an unknown bank model's estimation error. The confidential US-bank application includes missing and inconsistent reports; displayed p-values are for individual tests and require separate multiplicity treatment. Selected accepted-body methods, proof passages and supplement were read. The author repository declares GPL-3 for its package, but implementation, paper-matched release, financial-data rights and full numerical reproduction remain unverified. Kernel priorities are external to observed rejection results.
<!-- SYNTHESIS_2_END -->

## Actual editions and recorded root scope

Selected ranges do not mean every line, numerical cell or outside proof was read. Auxiliary reading does not enlarge root scope or time.

| Source | Retained edition and page mapping | Root selected reading | Unread boundary |
|---|---|---|---|
| Fissler–Hoga |53-page arXivv4; main numbering matches physical pages; supplement startsPDF29, with supplement printed page = PDF page − 28 |PDF1–10, partial excerpt11,12–26,29,31–35,39–41,47–48; visual checks13,14,18,20,29,35,40 |Remaining nonelicitability arguments, simulation derivations, external proofs and executable implementation not certified; final journal body/supplement unreviewed |
| Gordy–McNeil |52-page accepted combined edition: cover1; main printed1–41=PDF2–42; supplement title43 and printed1–9=PDF44–52 |Selected prose/displays acrossPDF2–39; cover1, references40–42; supplement43–45,48–50,52; visual checks10,11,12,24,28,37,45,48,52 |Numerical tables viewed/contextualized rather than fully audited; remaining supplemental constructions and outside CLT/regression/special-function proofs unreviewed |

File-production dates and repository updates are not assigned as scholarly revisions. The formal citation, actual manuscript and actual selected reading remain separate provenance fields.

## Original crosswalk of inferential objects

| Distinction | Boundary retained |
|---|---|
| Finite-dimensional joint report versus tail distribution | A vector of VaR/CoVaR/CoES or VaR/MES reports targets finite functionals. A PIT-based distribution diagnostic requires different probability-level information; neither input can be silently substituted for the other. |
| Lexicographic order versus multiplicity | Priority among score coordinates defines a forecast-comparison order. It does not control FDR, familywise error or repeated examination of many assets/models. |
| Selected information versus all information | The transformed-report null relative to PIT history and finitely instrumented moment tests do not certify ideal forecasts relative to every available predictor. |
| Model uncertainty versus issued forecasts | Inference on a fitted model family and evaluation of issued predictions need different estimation-error conventions. A model's having the right functional form does not establish its finite-history forecasts as ideal. |
| Population property versus sampling law | Identification and consistent scoring do not supply a central limit theorem, covariance consistency or a stopping-time bound. |
| Single evaluation versus ongoing monitoring | Fixed-sample asymptotic comparisons and distribution diagnostics retain their own premises; bounded transforms and multiple score coordinates do not create an anytime guarantee. |

The financial exercises are historical source applications. They do not supply project results, a new study design or a claim of methodological novelty.

## Materials, permissions and access boundary

Fissler–Hoga reports online computational materials, but no archive, program or observation was retrieved. Its WSJ-sourced index observations and code/data reuse terms remain unverified. The arXiv paper licence was not inspected, so none is assigned here.

Gordy–McNeil's supplement links [spectralBacktest](https://github.com/ajmcneil/spectralBacktest). Completed documentation inspection covered its README and [DESCRIPTION](https://github.com/ajmcneil/spectralBacktest/blob/master/DESCRIPTION), recording version0.5.6 and a GPL-3 package declaration. No source implementation or data directory was inspected. Current repository documentation is not a frozen2020 replication release. White Rose identifies the accepted article as CC BY-NC-ND2.5; that article licence and the package declaration concern different objects. Neither establishes rights to redistribute the confidential bank samples.

No original article, raw observations, executable program or substantial third-party passage is delivered. Public reading access is not treated as data or software permission. Existing access-limited routes were not retried during preparation.

## De-duplication and retained fingerprints

Registers01–21 were checked by authors, titles, DOI/article number and arXiv identifier. Neither source had a prior principal entry. This preparation used only completed reading records and retained-file fingerprints, with no new paper search or body reading.

The two retained bodies and two repository-documentation responses were rehashed and matched their recorded fingerprints. Documentation hashes identify captured web-page responses, not immutable commits or tested software. File identity does not certify unread proofs or final-version equivalence.

| Retained evidence | Bytes | SHA-256 |
|---|---:|---|
| Fissler–Hoga, arXivv4 |841712|`263ef4b69eca9fd41a086edd2b5d3269268c7531ba25274b2ca543eb5245a672`|
| Gordy–McNeil, accepted 30March2020 combined edition |822098|`cd47c07dd75f58120461780c8227d534581846b03ac30448941fabd63faf9743`|
| Spectral repository README landing response |254400|`8a22aaf7fd2e66434acdfa19c8448293438922361ede3b5aea79fa15be139a30`|
| Spectral repository DESCRIPTION web-page response |222861|`02bb4b308deb89af35920c033250cc7ad7cfe98f096376cd8c1e0d3f97e3bf19`|
