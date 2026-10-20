# Source register 11: constrained prediction and nonparametric tail risk

20 October 2026. This batch checks foundations and direct financial predecessors of the risk-estimation methods under review. Literature reading continues; no final topic, empirical specification or result is selected.

## 1. Tail-constrained prediction already has a financial application

**A. Alexandre Trindade, Stan Uryasev, Alexander Shapiro and Grigory Zrazhevsky (2007), “Financial prediction with constrained tail risk.”** *Journal of Banking & Finance* 31(11), 3524–3538. DOI [10.1016/j.jbankfin.2007.04.014](https://doi.org/10.1016/j.jbankfin.2007.04.014). November issue; actual journal copy says online 29 April 2007. Source: [Georgia Tech author-hosted journal copy](https://bpb-us-e1.wpmucdn.com/sites.gatech.edu/dist/4/1470/files/2021/03/TUSZ-07.pdf), 15 pages; SHA-256 `ee58ad074c16c9bda7d6cd5e9cd65d19e049e3eab466a4aaa504ed0c56ea41ef`.

**Depth:** selected full text and displayed internal proofs; external stochastic-program results and fitted-residual inference not independently certified. Regression minimizes fitting loss subject to empirical residual CVaR. Absolute-error fitting gives an LP; squared-error fitting gives a QP. A tighter cap can intentionally change the population prediction target. Separate fixed-loss iid CVaR asymptotics distinguish singleton quantiles from quantile intervals. The financial example predicts NDX/SPX intraday returns from overnight returns, using interleaved historical validation rather than chronological forecasting. Residual error risk differs from investment loss. Existing constraints and examples do not establish finite-sample confidence for an arbitrarily selected strategy. Another asset alone would not make this a new method.

## 2. Marginal portfolio ES and component risk

**Olivier Scaillet (2004), “Nonparametric estimation and sensitivity analysis of expected shortfall.”** *Mathematical Finance* 14(1), 115–129. DOI [10.1111/j.0960-1627.2004.00184.x](https://doi.org/10.1111/j.0960-1627.2004.00184.x). January issue; online 24 December 2003. Actual source: [UNIGE published-version record](https://archive-ouverte.unige.ch/unige:41799), 17 PDF pages including repository cover and terminal blank; SHA-256 `c469cc0b94bb2604ee1c7e60a5ed73750ffa877216534cc2b469d5bda30e5a86`.

**Depth:** selected definitions, assumptions, gradient argument, estimation proof and applications; external CLTs and every covariance term not independently certified. The target is stationary marginal portfolio loss, not risk conditioned on a market-predictor vector. A scalar portfolio projection is kernel-smoothed; Gaussian kernel weights do not impose a Gaussian return law. Allocation sensitivities and Euler risk contributions are mature components. Their inference retains quantitative mixing, moment, smooth-density, quantile and bandwidth premises; the printed asymptotic formulas are not supplied as operationally certified confidence formulas here. Two French equities and Danish fire losses already illustrate the method. Smooth historical risk surfaces do not establish simultaneous confidence over selected portfolios or current raw-data reuse rights.

## 3. Conditional ES given lagged returns

**Olivier Scaillet (2005), “Nonparametric Estimation of Conditional Expected Shortfall.”** *Assurances et gestion des risques / Insurance and Risk Management* 72(4), 639–660, January. DOI [10.7202/1106844ar](https://doi.org/10.7202/1106844ar). The [journal's issue list](https://www.fsa.ulaval.ca/faculte/departements-ecole/fai/revue-assurance-gestion-risques/publications/) resolves a conflicting repository volume field; 2023 registry dates are not the original year. Actual body: [UNIGE public accepted manuscript](https://archive-ouverte.unige.ch/unige:41796), **“This version: May 2004,”** 25 PDF pages; SHA-256 `977bc12d4f2f4e46d23eb4212d1b189a026ebf3220ade0060cba119cb204dbc8`. Formal typeset body unread.

**Depth:** selected page-image reading of definitions, estimators, assumptions, propositions, application and appendix. Product kernels estimate conditional quantiles and ES given finitely many lagged returns. The stated normal approximation concerns fixed finite conditioning points under stationarity, mixing, moments, density and bandwidth conditions. Full-history conditioning and simultaneous or anytime guarantees require separate arguments. Five stock indices already supply one-/two-lag illustrations and nominal pointwise bootstrap bands. The author leaves further statistical validation for later work. No observations, code, bands or trading results were reproduced; external proof and exact covariance details remain unverified.

## 4. Generalized risk-tuned regression: abstract screen only

**R. Tyrrell Rockafellar, Stan Uryasev and Michael Zabarankin (2008), “Risk Tuning with Generalized Linear Regression.”** *Mathematics of Operations Research* 33(3), 712–729. DOI [10.1287/moor.1080.0313](https://doi.org/10.1287/moor.1080.0313). [Publisher record](https://pubsonline.informs.org/doi/abs/10.1287/moor.1080.0313) gives online 1 August 2008.

**Depth:** official metadata and abstract only; no original body or theorem read in this batch. The abstract already coordinates regression error, deviation, risk and statistics, including factor-model and finance motivations. A separate author-site draft surfaced, but was not silently substituted for the journal body. This broad predecessor prevents treating the general idea of adapting regression loss to a risk-management purpose as new. Exact definitions, assumptions, equivalences, examples and proofs remain unread.

## Reading distinctions retained

| Existing target | What must be specified before transfer |
| --- | --- |
| A predictor chosen under a residual-tail cap | Which error direction and cap, and whether the intended target changes |
| Marginal portfolio ES and component contributions | The holding-to-loss map and the stationary sampling law |
| Conditional ES given finite lag information | The conditioning variables, local sample support and smoothing assumptions |
| Statistical uncertainty for any of these quantities | The actual theorem's sampling, estimation, selection and time scope |

These are literature distinctions, not a selected research protocol. A new dataset or index does not by itself establish new methodology. Further reading will check original sources and closest applications before a question and chronological evaluation are fixed. Third-party PDFs and financial observations are retained outside the public repository; no rights to redistribute them are inferred from free access.
