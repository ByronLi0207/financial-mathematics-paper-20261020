# Source register 20 — strategy screening, covariance estimation and bounded-mean monitoring

**Reading update — 20 October 2026.** This register consolidates completed selected primary-source reading. It reports no new project result or selected research design. Curation adds no original-body reading credit.

## 1. StepM and a fixed family of financial strategies

**Joseph P. Romano and Michael Wolf (2005), “Stepwise Multiple Testing as Formalized Data Snooping.” Econometrica 73(4), 1237–1282, July 2005.** First online **13 June 2005**. [DOI](https://doi.org/10.1111/j.1468-0262.2005.00615.x); [official author publication list](https://www.econ.uzh.ch/en/people/faculty/wolf/publications.html); [actual formal copy linked there](https://www.econ.uzh.ch/dam/jcr:ffffffff-935a-b0d6-ffff-ffffa286d4d1/etca.pdf).

**Source synthesis — 139 words.**

<!-- SYNTHESIS_1_START -->
Romano and Wolf use stepwise joint confidence regions to identify strategies outperforming a benchmark while controlling familywise error asymptotically. The family is fixed as observations increase. A continuous joint limit and consistent centered bootstrap approximation are essential; studentization adds matching positive original and bootstrap scale limits. Mean-return differences, Sharpe differences and factor intercepts remain distinct parameters. Estimated-strategy and time-series scenarios delegate important primitive conditions to outside sources. Appendix B defines resampling schemes without proving universal bootstrap validity. Fitted-law block-size calibration carries no asymptotic-optimality claim. The financial application uses 105 complete-history hedge funds over 147 months, and forecast trimming is already a stated motivation. These are established financial uses. Selected formal methods, application and proof routes were read. The studentized theorem's proof is omitted in the source; external assumptions, full numerical results, executable materials, observations and current permissions remain unverified.
<!-- SYNTHESIS_1_END -->

## 2. Kernel HAC estimation and its loss criterion

**Donald W. K. Andrews (1991), “Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation.” Econometrica 59(3), 817–858, May 1991.** [DOI](https://doi.org/10.2307/2938229); [actual university-hosted formal scan](https://personal.utdallas.edu/~d.sul/Econo2/andrews91.pdf). An exact first-online day was not established.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_2_START -->
Andrews distinguishes long-run covariance consistency, convergence rates and asymptotic truncated weighted quadratic loss. Strong-mixing and moment assumptions supply covariance and fourth-cumulant summability; estimated scores require parameter and derivative regularity. Stronger premises support rates and loss comparisons. Quadratic-spectral optimality concerns a positive-semidefinite kernel class under comparable bandwidth normalization and the specified asymptotic loss. It does not optimize every confidence, forecast or investment criterion. Automatic bandwidth consistency can tolerate misspecification of the approximating dependence model, while optimality requires additional control of the relevant population constant. Section 8 extends designated consistency and rate results to uniformly controlled nonstationary processes, retaining a potentially changing covariance target. It separates that extension from stationary loss optimality. This is an existing foundation for financial standard errors, not a return-density model. Selected formal scan statements and proof passages were read; full operational rules, numerical tables, external proofs and executable behavior remain unvalidated.
<!-- SYNTHESIS_2_END -->

## 3. Prewhitening, recoloring and inferential coverage

**Donald W. K. Andrews and J. Christopher Monahan (1992), “An Improved Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimator.” Econometrica 60(4), 953–966, July 1992.** [DOI](https://doi.org/10.2307/2951574); [official university reading list](https://users.ssc.wisc.edu/~behansen/718/readings.htm); [actual formal scan linked there](https://users.ssc.wisc.edu/~behansen/718/AndrewsMonahan1992.pdf). The formal article's author form is retained; no exact first-online day is asserted.

**Source synthesis — 145 words.**

<!-- SYNTHESIS_3_START -->
Andrews and Monahan fit a finite-order vector autoregression to estimating-function vectors, smooth residual covariances and recolor at frequency zero. The working filter need not be the true model. Their consistency theorem requires covariance and fourth-cumulant summability, estimator regularity, controlled bandwidth growth, convergent fixed-order filter coefficients and a nonsingular limiting recoloring matrix. It refers primitive mixing conditions and underlying kernel arguments to Andrews 1991. Additional rate and truncated-MSE results refer to the earlier 1990 draft, whose body was not read. Positive semidefiniteness is separate from exact confidence coverage. Reported simulations distinguish bias, variance, mean squared error and coverage; improvements need not coincide. The target is estimator uncertainty, with input vectors determined by the estimator. Existing financial StepM applications use this covariance machinery. Selected formal scanned methods, results discussion and appendix were visually read; full tables, draft-only theory, software behavior, observations and present reuse permissions remain unverified.
<!-- SYNTHESIS_3_END -->

## 4. Bounded-mean change detection: validity and efficiency

**Ashwin Ram and Aaditya Ramdas (2026), “Asymptotically optimal sequential change detection for bounded means.”** [arXiv:2602.05272v1](https://arxiv.org/abs/2602.05272v1), submitted **5 February 2026, 03:54:04 UTC**; [arXiv DOI](https://doi.org/10.48550/arXiv.2602.05272). The checked official history listed only v1. No journal publication or acceptance was verified.

**Source synthesis — 144 words.**

<!-- SYNTHESIS_4_START -->
Ram and Ramdas study composite changepoint detection under an average-run-length constraint. Their sharp delay analysis assumes iid pre-change and post-change segments, independent across the change. For observations in a known bounded interval and a known mean baseline, they mix Shiryaev–Roberts betting recursions over a countable dense set with fixed positive weights. The authors report finite-threshold ARL validity, pointwise first-order Pollak conditional-delay optimality and uniform normalized optimality on alternatives with fixed positive mean separation. The ARL proof uses conditional factor expectations; the delay proof additionally uses iid log growth and independence from survival history. A practical finite grid does not automatically inherit the dense mixture's sharp constant. Selected setup and proof routes were read without certifying every assertion or external theorem. The selected text reports no financial application. Raw ES residuals, estimated support bounds and dependent financial alternatives do not automatically satisfy these stated premises.
<!-- SYNTHESIS_4_END -->

## Actual editions and recorded root reading

These ranges refer to selected passages, not every line or result on each page. Auxiliary reading does not enlarge the root's recorded scope, and page rendering alone is not counted as substantive reading.

| Source | Actual retained edition and page mapping | Recorded root selected scope | Remaining reading boundary |
|---|---|---|---|
| Romano–Wolf 2005 | 46-page formal article; printed page = PDF page + 1236 | PDF1–6,10–23,32–33,36–41; visual checks on 12,17,22,37,39 | Full simulations, Appendices C/D and outside primitive probability conditions not audited; Theorem 4.1 proof is omitted by the authors |
| Andrews 1991 | 43-page formal scan, including one archive cover; printed page = PDF page + 815 for PDF2–43 | Selected setup, definitions, assumptions, statements and proof passages across PDF1–14,22–25,35–43 | Full operational bandwidth section, numerical tables, every proof line and external inequalities not reviewed |
| Andrews–Monahan 1992 | 14-page formal scan; printed page = PDF page + 952 | Visual substantive reading of PDF1–7,12–14 and selected prose/captions across8–11; all14 pages viewed | Full table audit and the separate1990 draft absent; short appendix depends on Andrews1991 |
| Ram–Ramdas 2026 | 25-page arXiv v1; physical PDF numbering used | Selected setup/statements/proof arguments across PDF1–12,15–25; references13–15 inspected; visual checks4,9,11,22–24 | Remaining proof details and outside duality/sequential-detection references were not independently reviewed |

The archive cover on the Andrews 1991 scan and file-production dates are not scholarly revisions. The 1992 formal article and its 1990 discussion-paper predecessor remain separate editions. The bounded-mean entry is a versioned preprint rather than a verified journal article.

## Original crosswalk of inferential objects

| Distinction | Boundary retained in this register |
|---|---|
| Strategy selection versus covariance estimation | A performance parameter and the uncertainty of its estimator are different objects; a HAC estimate alone supplies neither the performance null nor its central limit theorem. |
| Finite matrix property versus sampling guarantee | A positive-semidefinite estimate does not establish exact finite-sample test size, confidence coverage or an anytime bound. |
| Steps versus observation dates | A stepdown sequence on a fixed dataset differs from a detector's stopping time on an expanding observation stream. |
| Asymptotic limits | A fixed testing family with sample size increasing differs from a changepoint threshold increasing; neither limit automatically covers an expanding family or changing alternatives. |
| Conditional validity versus iid efficiency | A conditional expectation premise used for null drift does not establish the iid survival-independence argument needed for sharp delay. |
| Financial targets | Mean payoff, factor alpha, estimator covariance, exceedance probability and tail-loss severity retain distinct economic meanings. |

The closest established connections here are StepM's own financial screening, its cited HAC standard errors, and betting-based sequential detection. These connections delimit existing methods; no new financial application, design or empirical finding is claimed.

## Provenance and retained evidence

Registers 01–19 were checked by title, DOI or arXiv identifier. None of these four sources was already a principal entry; earlier mentions of StepM and later generalized-error procedures are not treated as duplicate original-body entries. This update uses completed reading records and adds no new source search or original-body reading.

Normal author, university and arXiv sources supplied the recorded editions. Public availability does not establish current software, financial-data or article-redistribution permissions. Source observations and executable materials were not downloaded or reproduced, and none is delivered with this register.

The four retained source files were rehashed during preparation and matched their recorded fingerprints. A fingerprint identifies an edition; it does not certify every proof or unread version equivalence.

| Actual retained version | Bytes | SHA-256 |
|---|---:|---|
| Romano–Wolf 2005, formal article | 315991 | `70954e9cf3567018ab47e6f0d02c114e99f7e18a721569e331f97d9792651743` |
| Andrews 1991, formal university scan | 3713247 | `30f77e7e587e4ef93e5835d70f2fb68117e60498f6cee48eb1083726d4620d9d` |
| Andrews–Monahan 1992, formal university scan | 1287984 | `22c542987626080f51741b04340746c29c0b140df1d0e667e1bb19e188541b3b` |
| Ram–Ramdas 2026, arXiv v1 | 411293 | `f9107550c5444243e6e04d4121d8af165e1b845b0f372c11e507534c13fb3fee` |
