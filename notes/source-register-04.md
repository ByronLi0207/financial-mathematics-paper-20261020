# Reading register 04 — financial meaning and joint-tail scoring

20 October 2026. Status: literature reading and synthesis. This project has not selected a final topic, run financial experiments or produced a completed manuscript. Reading scopes below refer to the actual versions obtained; the authors' reported empirical findings are not this project's results. Recent papers are described as recent, with no unsupported popularity claim.

## Financial evidence: what the statistic can establish

### Moreira and Muir (2017)

Alan Moreira and Tyler Muir, *Volatility-Managed Portfolios*, Journal of Finance **72(4), 1611–1644**, [DOI 10.1111/jofi.12513](https://doi.org/10.1111/jofi.12513), first online **6 April 2017**. [Author-hosted typeset PDF](https://amoreira2.github.io/alan-moreira.github.io/VolPortfolios_published.pdf). Its volume/issue placeholders differ from the final bibliographic record.

**Read:** introduction/§I.A–C, PDF pp. 1–7; §II.B–C,pp. 13–19; selected explanation/conclusion,pp. 30–31. Selected full text, not all theory, tables or Internet Appendix.

**Synthesis.** The rule scales next-month factor excess returns using lagged realized variance. Its motivation is the conditional mean–variance tradeoff. Spanning evidence, transaction costs and implementability are treated separately. Full-sample volatility normalization is innocuous for an unconstrained Sharpe ratio under positive constant scaling, but that does not automatically settle other decision criteria. The paper already examines market costs, leverage constraints, inverse-volatility alternatives and embedded leverage. Adding those features or another factor series would not alone distinguish a new contribution. Input sources vary across its examples; availability of some French factors does not establish access to every underlying dataset.

### Cederburg, O'Doherty, Wang and Yan (2020)

Scott Cederburg, Michael S. O'Doherty, Feifei Wang and Xuemin (Sterling) Yan, *On the performance of volatility-managed portfolios*, Journal of Financial Economics **138(1), 95–117**, [DOI 10.1016/j.jfineco.2020.04.015](https://doi.org/10.1016/j.jfineco.2020.04.015), online **1 May 2020**. [Author-hosted journal PDF](https://www.lehigh.edu/~xuy219/research/COWY.pdf).

**Read:** introduction/§2,pp. 1–4; selected §4.1–4.3.1,pp. 7–13; instability/conclusion,pp. 17–19; beginning of construction appendix,p. 19. Full tables and Internet Appendix were not audited.

**Synthesis.** Positive spanning alpha and a better standalone strategy answer different questions. Ex-post optimal combinations also differ from allocations constructed with only prior information. The authors examine real-time estimation of normalization, means and covariances, applying estimation risk to the augmented strategy and its benchmark. Training length, rolling versus expanding estimation, risk aversion, leverage and instability already have direct treatments. Their adverse results are part of the evidence. Some extended anomaly construction requires proprietary databases; a complete replication is not presumed possible from public French data alone. Reported test statistics and bootstrap outputs were not reproduced here.

### Ledoit and Wolf (2008)

Oliver Ledoit and Michael Wolf, *Robust performance hypothesis testing with the Sharpe ratio*, Journal of Empirical Finance **15(5), 850–859**, [DOI 10.1016/j.jempfin.2008.03.002](https://doi.org/10.1016/j.jempfin.2008.03.002), online **26 March 2008**. The printed first name is Oliver; the author's homepage uses Olivier. [Journal PDF on the UZH author page](https://www.econ.uzh.ch/dam/jcr:ffffffff-935a-b0d6-0000-00007214c2bc/jef_2008pdf.pdf).

**Read:** complete main text§§1–7,pp. 1–9; references screened. Bootstrap formulas/Algorithm 3.1,p. 5, visually checked. Cited asymptotic proofs were not independently audited.

**Synthesis.** The target is a population Sharpe-ratio difference for paired strictly stationary returns. HAC and a studentized circular block bootstrap accommodate specified nonnormality and time dependence, subject to moment, dependence and nondegeneracy conditions. Pairing must survive resampling, and each bootstrap sample needs its own standard error. Block-length calibration adds an estimation/simulation layer. First-order inference and higher-order improvements have different sufficient conditions. The article does not establish validity under arbitrary market drift or optional stopping. Official R/Matlab links were observed; code was not downloaded or run.

## Joint tail forecasts: score, test and numerical approximation

### Fissler and Ziegel (2016), read with the correction

Tobias Fissler and Johanna F. Ziegel, *Higher order elicitability and Osband's principle*, Annals of Statistics **44(4), 1680–1707**, [DOI 10.1214/16-AOS1439](https://doi.org/10.1214/16-AOS1439). Actual fixed source: [arXiv:1503.08123v3](https://arxiv.org/abs/1503.08123v3), submitted **30 September 2015**, PDF dated **1 October 2015**.

**Read:** definitions, Osband conditions, §5/Theorem5.2/Corollary5.5 and relevant proof portions, PDF pp. 4–6,11–14,17–21,26–30. Selected text; not a whole-paper label. Critical pp. 20–21 visually checked.

**Synthesis.** Joint VaR/ES scoring is established. Under the return convention ES is no greater than VaR. Unique quantiles, score integrability and the conditions for constructing a consistent score differ from the stronger density/smoothness/richness assumptions for a full characterization. Quantile uniqueness does not imply absence of atoms or exact exceedance probability. Consistency identifies an expected-loss minimizer; it does not itself prove a finite-sample test guarantee or rank two incorrect models independently of the selected score.

Tobias Fissler and Johanna F. Ziegel, *Supplement to “Erratum: Higher Order Elicitability and Osband's Principle”*, [arXiv:1901.08826v2](https://arxiv.org/abs/1901.08826v2), submitted **6 October 2020**; associated journal correction [DOI 10.1214/20-AOS2014](https://doi.org/10.1214/20-AOS2014), Annals of Statistics **49(1), 614 (2021)**.

**Read:** all 12 pages of the author supplement, including Proposition 2 and proof; p. 10 domain list visually checked. This is not a claim to have obtained the single-page journal correction PDF.

**Synthesis.** The general action-domain proof needs additional path conditions. The supplement explicitly retains the common VaR/ES action domain and negative-ES Cartesian domain. Convexity of a newly restricted report domain alone is insufficient to reuse the old argument. The correction does not retract joint elicitability.

### Fissler, Ziegel and Gneiting (2016)

Tobias Fissler, Johanna F. Ziegel and Tilmann Gneiting, *Expected Shortfall is jointly elicitable with Value at Risk – Implications for backtesting*, Risk, **January 2016, 58–61**. Actual source: [arXiv:1507.00244v2](https://arxiv.org/abs/1507.00244v2), submitted **12 July 2015**, PDF dated **14 July 2015**.

**Read:** entire 7-page author version, including all substantive text and references. Simulations were read, not reproduced.

**Synthesis.** Correctness backtests and comparative score tests have different nulls. Nonrejection is not proof of correctness or superiority. The proposed comparative statistic uses an estimated standard error and asymptotic Diebold–Mariano reasoning. First moments sufficient for a scoring result do not automatically justify a Gaussian approximation for the score difference. Financial joint-risk comparison is already a direct application of these scores.

### Casgrain, Larsson and Ziegel (2024)

Philippe Casgrain, Martin Larsson and Johanna Ziegel, *Sequential testing for elicitable functionals via supermartingales*, Bernoulli **30(2), 1347–1374**, [DOI 10.3150/23-BEJ1634](https://doi.org/10.3150/23-BEJ1634). Actual source: [arXiv:2204.05680v2](https://arxiv.org/abs/2204.05680v2), submitted **4 June 2023**, PDF dated **6 June 2023**. The arXiv record's title additionally starts with “Anytime-valid”. Journal/preprint byte-equality was not checked.

**Read:** selected §§2–4,pp. 3–22; confidence sequences and joint-tail example,pp. 25–27; selected appendices/point-null proofs,pp. 32–33. Not all algorithms, examples or proofs.

**Synthesis.** Fixed conditional-functional nulls yield betting tests from one-sided bounded score differences or suitable identification functions. Unbounded-score constructions need explicit conditional tail bounds. Predictable mixing preserves the shared-null guarantee; online optimization supplies power only with its additional regret, geometry and positive-growth conditions. Joint VaR/ES confidence inference on bounded data is already illustrated. These results are a mature foundation, not a first financial application. Broader set-valued-null wording is not used as a validated result in this register.

### Wang and Yu (2026): deeper proof follow-up

Ruodu Wang and Jingcheng Yu, *E-Backtesting Expected Shortfall without Value-at-Risk Forecasts under Time-series Models*, [arXiv:2610.17681v1](https://arxiv.org/abs/2610.17681v1), submitted **13 October 2026**, PDF dated **12 October 2026**. No journal reference verified.

**Read:** selected main sections/implementation; now all Appendix C proofs of Propositions 1–7,PDF pp. 32–37. Tables and all remaining appendices were not audited; no implementation was inspected.

**Synthesis.** Exact ideal-profile validity requires one fixed true feasible parameter–quantile pair and the positive report margin. The proof already handles the negative-infinite nuisance-quantile endpoint. Fixed-horizon grid convergence does not need bounded loss support. The continuous-quantile numerical bounds certify the chosen parameter grid, while the full-parameter guarantee is a limiting result. A finite grid is not made exact merely by being dense. Its NASDAQ example uses negative log returns; a simple-return support bound cannot be transferred numerically to that loss.

## Implications for continued reading

The eventual paper must identify the financial decision and target before selecting a test. A score ranking, calibration claim, real-time economic gain and sequential false-alarm guarantee each require their own evidence. The next reading checks conditional predictive ability, dynamic joint-tail estimation and sample-size planning, while the alternative ambiguity/preference literature remains under comparison. No final research question or novelty claim is made here.

Source PDFs remain local for reading; this register contains original notes and primary links. Public access has not been treated as permission to redistribute source PDFs or financial raw data. Active reading, source acquisition, publication administration and parallel overlap remain separate in the local time ledger.
