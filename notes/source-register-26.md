# Source register 26 — future-value prediction, risk parameters and survey definitions

**Selected primary-source reading, 20 October 2026.** Sections 1–2 are research-paper records; section 3 is official source/method documentation. This update consolidates completed selected reading, without project empirical results, a selected design or new original-body reading credit.

## 1. Research paper — GARCH bootstrap future distributions

**Lorenzo Pascual, Juan Romo and Esther Ruiz (2006), “Bootstrap prediction for returns and volatilities in GARCH models.” Computational Statistics & Data Analysis 50(9), 2293–2312, May 2006.** [Formal DOI](https://doi.org/10.1016/j.csda.2004.12.008).

Actual body: *Forecasting returns and volatilities in GARCH processes using the bootstrap*, **UC3M Working Paper 00-68, Statistics and Econometrics Series 31, 2000**, [institutional original](https://e-archivo.uc3m.es/rest/api/core/bitstreams/685bbe47-2992-473c-af81-e51afd17602e/content), 50 physical pages. The cover supplies the year, not a precise day/month. Neither the related 2001 manuscript nor the final 2006 body was obtained or version-compared.

**Source synthesis — 142 words.**

<!-- SYNTHESIS_1_START -->
Pascual, Romo and Ruiz generate bootstrap predictive laws for future GARCH returns and volatilities. Pseudo histories produce refitted parameters; original observations then determine the forecast-origin state before future innovations are drawn. Holding coefficients fixed omits that estimation variation. The inspected working paper reports fixed-horizon conditional weak convergence under stationarity, parameter-space, innovation-shape and strong moment conditions, including a finite 32nd innovation moment. This differs from exact finite-sample coverage, current risk-estimator confidence intervals or growing-horizon inference. A future-date return is also different from cumulative holding-period loss. The IBEX35 illustration estimates on earlier observations and evaluates a short later period, using intraday variation as a volatility proxy. Selected 2000 institutional methods, theorem routes and application were read. Later-version equivalence, external QML/bootstrap proofs, complete numerical evidence, implementation and current data permissions remain unverified. Simulation behavior does not remove the stated theoretical assumptions or provide anytime guarantees.
<!-- SYNTHESIS_1_END -->

## 2. Research paper — risk-parameter estimation and joint limits

**Christian Francq and Jean-Michel Zakoïan (2015), “Risk-parameter estimation in volatility models.” Journal of Econometrics 184(1), 158–173, January 2015.** [Formal DOI](https://doi.org/10.1016/j.jeconom.2014.06.019).

Actual body: [author-deposited MPRA 41713](https://mpra.ub.uni-muenchen.de/41713/1/MPRA_paper_41713.pdf), cover **4 October 2012**, posted **4 October 2012, 10:43 UTC**,43physical pages. Later repository modification dates are not assigned as body revisions. The final 2015 article was not obtained or version-compared.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_2_START -->
Francq and Zakoïan absorb a positively homogeneous innovation-risk functional into volatility-model parameters. Direct risk-parameter estimation differs from fitting volatility and then estimating residual tail functionals. Joint limits retain covariance between scale estimates and residual quantiles or shortfall, rather than treating estimated residuals as raw iid observations. Symmetric one-step VaR results use their quantile, density and derivative conditions; two-step Gaussian-QML limits require finite innovation fourth moments and additional regularity. The asymmetric one-step extension has consistency, with its limit law left open in this edition. ES receives a separate two-step analysis. A delta-method VaR accuracy interval concerns estimation error, not a prediction interval for future returns. Stock-index applications illustrate risk parameters and accuracy bands. Selected October 2012 working-paper statements and supplied proof routes were read. Deferred external proofs, final-version identity, implementation and financial-data rights remain unverified. These asymptotic results do not establish finite-sample or anytime coverage.
<!-- SYNTHESIS_2_END -->

## 3. Official source/method documentation — ECB SPF

**European Central Bank, SPF dataset description**, actual reader edition **February 2026**, 9 pages, [official dictionary](https://www.ecb.europa.eu/stats/prices/indic/forecast/shared/files/SPF_dataset_description.pdf). The original dictionary file was not retained: its PDF-byte count and SHA-256 are **unknown**. A separately labelled original paraphrase records only selected method passages.

Other official sources selected earlier: [SPF round-date calendar](https://www.ecb.europa.eu/stats/prices/indic/forecast/shared/files/SPF_rounds_dates.pdf), 2 pages ending 2026 Q3 in the checked response; [ESCB statistical reuse policy](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html); [ECB copyright conditions](https://www.ecb.europa.eu/services/using-our-site/disclaimer/html/index.en.html); and the methodological passages of [“Twenty years of the ECB Survey of Professional Forecasters,” Economic Bulletin 1/2019](https://www.ecb.europa.eu/press/economic-bulletin/articles/2019/html/ecb.ebart201901_01~8300a24082.en.html). This section is documentation/source-method work, not a new research-paper entry.

**Source synthesis — 146 words.**

<!-- SYNTHESIS_3_START -->
ECB SPF documentation distinguishes calendar averages from rolling targets tied to the latest observations. Probability intervals and horizons change historically, while outer bins remain open. Aggregate histograms average respondent probabilities and differ from disagreement among point forecasts. Dispatch, response deadline and aggregate publication are separate dates; current round labels do not establish original-release availability or outcome vintages. Existing official methodology discusses interpolation and endpoint choices when constructing continuous summaries from bins. Qualifying public statistics have conditional free-reuse terms, with attribution, integrity and third-party restrictions. Selected dictionary text, calendar metadata and method/policy passages were read; no observation archive was retrieved. Original dictionary bytes remain unknown, and no visual inspection is claimed. Incidental numerical examples or results displayed by the reader were not retained, compared or analysed. The calendar has its own original-PDF fingerprint; the dictionary record is a paraphrase, not an original-file hash or complete source copy.
<!-- SYNTHESIS_3_END -->

## Actual editions and root selected scope

Selected ranges do not certify every line, table cell, graph or outside proof. Supporting records do not enlarge root scope or hours.

| Source/category | Actual retained edition | Root selected reading | Remaining boundary |
|---|---|---|---|
| PRR research paper | 50-page UC3M 2000 working paper; printed page = PDF page − 2 from PDF 3 |Selected main prose/displays PDF 1–31, especially method 8–11, assumptions/proofs 12–21, application 27–31; references 32–34 screened; visual checks 9, 12, 18, 20, 25, 29, 31 |Tables 35–41 and figures 42–50 only page-mapped; external proofs, executable implementation and later editions unreviewed |
| Francq–Zakoïan research paper | 43-page October 2012 MPRA edition; printed page = PDF page − 1 |Selected PDF 1–29, 34–41; stated assumptions, principal risk-parameter results and supplied two-step proof routes; visual checks 13–14, 20, 26, 28, 38, 40 |PDF 30–33 and references 42–43 briefly mapped; deferred/external proofs and complete numerical results unreviewed; final 2015 body unread |
| ECB official documentation |February 2026 dictionary viewed through official reader; separate original calendar PDF |Dictionary selected definitions 1–4, Annex 3 p7, Annex 5 p8, one policy sentence p5 and calendar-average coding sentence p9; calendar column definitions, early/recent records and access-history notes; selected policy text and 2019 §4/Box 5 methods |No original dictionary bytes/hash; no inspected screenshot pixels or visual claim; full historical maps/calendar, observation files, numerical examples and article results not analysed |

The ECB methods reader incidentally exposed numerical context. No such values are reproduced here or preserved as observations. Its dictionary and 2019 article were not stored wholesale. Screenshot-reference responses without inspectable pixels are not treated as visual reading.

## Original crosswalk of risk and information objects

| Distinction | Boundary retained |
|---|---|
| Future-value distribution versus estimation accuracy | Prediction of a future return/volatility differs from uncertainty in the current conditional risk parameter. Adding parameter refits does not equate the two inferential targets. |
| Risk definition versus inference assumptions | A homogeneous risk functional and a scale representation do not supply all moments, symmetry, derivatives or identifiability conditions required by an estimator's limit theorem. |
| Residuals versus innovations | Innovations may be iid under a model; estimated residuals depend on fitted parameters, and their joint influence can matter for tail-functional inference. |
| Histogram event versus continuous distribution | Open-ended bins identify event probabilities without determining unique within-bin densities, endpoints or tail means. |
| Survey label versus availability | A target/round code, original public release and later outcome vintage are separate evidence products, with potentially shared annual settlement outcomes. |
| Limit result versus repeated monitoring | Fixed-horizon weak convergence and asymptotic accuracy intervals do not automatically provide finite-sample, simultaneous or arbitrary-stopping guarantees. |

These are existing source methods and interpretation boundaries. No study question, financial series, experiment or project result is selected.

## Materials, access and rights

PRR's IBEX35 and intraday inputs, preprocessing, current vintage, executable materials and redistribution rights remain unverified. Francq–Zakoïan's nine-index 1991–2011 examples and previous 500-observation accuracy figures are source applications, not data obtained or calculations reproduced here. Their present source data/code access and permissions remain unverified.

ECB CSV/ZIP, round observations and outcome-vintage files were not requested. Conditional free reuse applies to qualifying public statistics under its stated conditions; copyright rules and authored-publication exceptions remain separate. No confidential material, respondent identification or unrestricted raw redistribution is inferred. File-specific notices inside unopened archives remain unverified.

Public reader access is not an original-file acquisition. Original calendar bytes, original research-paper bytes and a paraphrased selected-reader record are separately labelled below. No original article, survey observations, executable program or substantial third-party passage is delivered.

## De-duplication and retained fingerprints

Registers 01–25 were checked by author/title/identifier and institution/source terms. Neither paper nor the ECB official dictionary/calendaring source had a prior dedicated principal entry. Prior ECB applications or unrelated ECB financial sources are not this documentation reading. The official-method section does not increase a research-paper count. Curation used completed notes and existing fingerprints, without new search or original-body reading.

The retained research PDFs, calendar PDF and dictionary paraphrase were rehashed and matched their recorded bytes/SHA-256. Hashes identify these specific evidence types, not unread final-version equivalence, observation vintages or complete proof correctness.

| Evidence type and actual edition | Bytes | SHA-256 |
|---|---:|---|
| Original PDF: PRR UC3M Working Paper 00-68 |603403|`a6659d75b6300afd17be73857ce3b841e807decac5c774d99b5bc13725aa0d1c`|
| Original PDF: Francq–Zakoïan MPRA October 2012 |519593|`3d8e32e337761c39775e589984f5a9effa01efed758a1cb802cd4971863234a0`|
| Original calendar PDF: ECB SPF round dates |132151|`d5a7a8301aef9afab30d91562d205f658fd7758b04fe4af1dd03cf14f819d58d`|
| Derived original paraphrase: selected ECB dictionary-reader record |3134|`380618c64cd57c6e676989e1032466da15619ad5483a3476e3499c9df46c5ca2`|
| Original ECB dictionary PDF, not locally obtained |Unknown|Unknown; no original-file hash claimed|
