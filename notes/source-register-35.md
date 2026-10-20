# Source register 35: dynamic control and empirical-distribution uncertainty

20 October 2026. This follows the finite-horizon control and empirical-radius references already identified in the reading queue. It compares selected original passages and supplied proofs, not fully certified articles. Literature review continues; no final question, empirical specification or manuscript result is selected.

## Editions and reading depth

| Original source | Edition and actual scope |
|---|---|
| Ariel Neufeld and Julian Sester, *Non-concave stochastic optimal control in finite discrete time under model uncertainty* | **arXiv 2404.05230v2**, DOI 10.48550/arXiv.2404.05230. First deposit 8 April 2024; revision deposited 5 May 2025; PDF title 6 May 2025. Selected setup/results, comparison and financial application on physical 3–20, and supplied proof chain on 21–47. [Version record](https://arxiv.org/abs/2404.05230v2), [original PDF](https://arxiv.org/pdf/2404.05230v2). |
| Emmanuel Boissard and Thibaut Le Gouic, *On the mean speed of convergence of empirical and occupation measures in Wasserstein distance* | Published **2014**, Annales de l'IHP, Probabilites et Statistiques 50(2), 539–563, DOI **10.1214/12-AIHP517**. Selected physical 1–4 before Section 1.2, 7–15 before Section 3, Section 4 on 18–21, and Appendix A on 21–23 before Appendix B. [Official journal record](https://numdam.org/articles/10.1214/12-AIHP517/), [published PDF](https://www.numdam.org/item/10.1214/12-AIHP517.pdf). |
| Erhan Bayraktar and Tao Chen, *Nonparametric Adaptive Robust Control Under Model Uncertainty* | **arXiv 2202.10391v3**, DOI 10.48550/arXiv.2202.10391. First deposit 21 February 2022; revision deposited 21 March 2022; PDF title 23 March 2022. Selected introduction, learning state and formulation on 2–8, Section 2.3 supplied DPP arguments on 9–13, Section 2.4 and portfolio setup on 13–15. Proposition 2.3's proof and later numerics were not completed. [Version record](https://arxiv.org/abs/2202.10391v3), [original PDF](https://arxiv.org/pdf/2202.10391v3). |

Formula pages were also inspected visually. External foundations and every literal proof, constant and rate are not independently certified. The Gaussian section and Appendix B of Boissard–Le Gouic were not completed. The later [Bayraktar–Chen journal record](https://epubs.siam.org/doi/10.1137/22M1481609) verifies SIAM Journal on Control and Optimization 61(5), 2737–2760, online 12 September 2023; its body remains unread. No equivalence with the selected preprint is asserted. These are relevant sources, without an inferred popularity ranking.

## Dynamic ambiguity is part of the model

Neufeld–Sester permits non-concave payoffs and compact controls under substantial regularity and growth conditions. Its sequential family is constructed from admissible conditional kernels. The supplied local/global DPP arguments use measurable optimizers, backward induction and combination of those kernels; they preserve the max-control/min-law order. They do not establish unrestricted minimax interchange.

The Wasserstein example uses a higher moment order than the payoff-growth order, regular reference kernels and radii, and a convex local outcome domain. Those conditions support compactness, continuity and matching between nearby ambiguity sets. The separate parametric example requires a regular parameter-to-law map; a parameter ball is not the whole distributional ball.

Its stability comparison concerns optimized model values under specified conditional-law conditions. It is separate from realized performance of a computed hedge. The financial application uses bounded returns and positions and an asymmetric hedging objective; this does not automatically establish a multi-period mean–variance or cumulative-prospect-theory formulation. Reported short evaluation periods include overlapping hedge horizons. The source's numerical training procedure was not run here.

## Mean transport error and confidence have different premises

Boissard–Le Gouic first studies i.i.d. observations from one fixed law. Theorem 1.1 bounds expected empirical Wasserstein error through covering numbers. Its supplied argument combines multiscale transport geometry with cell-count fluctuations. The unbounded-support extension adds population moments and annular tail control; a finite sample maximum does not verify them.

The Markov section instead targets an invariant law through an occupation measure. Its operator variance-decay and initial-density assumptions support bounds for dependent cell counts. A return autocorrelation estimate does not verify the operator condition, and the invariant law is not a conditional next-return distribution. The unbounded Markov proof is partly an outline.

Appendix A explicitly treats independent sampling for concentration, including transport-entropy, bounded-support and polynomial-tail branches. The independent product structure is substantive. A dependent-data mean bound and an independent concentration result cannot simply be joined into one financial coverage theorem. Proposition 1.7's mixing extension is stated without its proof. No arbitrary estimated effective-sample-size substitution or simultaneous-over-time guarantee is added.

## Learning within control is already prior work

Bayraktar–Chen uses observable real-valued i.i.d. innovations with an unknown fixed law, a continuous controlled transition and compact actions. The empirical distribution joins the physical state; nature selects successive adverse laws within state-dependent sets. Its supplied DPP route uses measurable selectors and induced conditional kernels, with bounded-below loss used in the regularity argument. Existence is not a numerical approximation certificate.

The CLT-based radius is described as approximate confidence. It involves a law-dependent Brownian-bridge functional, approximated using order-statistic spacings and simulation. A separate concentration route invokes stronger exponential moments and population-dependent constants. Equal sample-size order does not equate the guarantees.

Section 2.4 invokes additional differentiability and sensitivity arguments. Its static/adaptive preference discussion is explicitly qualitative; it is not adopted here as universal policy or realized-profit dominance. The financial setup already covers self-financing bank/stock allocation with i.i.d. log returns, no short selling or leverage, and exponential utility. Merely changing the stock would not establish a new method.

## Implications for a later transfer

| Question to settle before design | Required distinction |
|---|---|
| What financial decision is new? | Allocation, derivative hedging, forecast coverage and backtest power have different objectives. |
| How may nature vary? | Statewise conditional choices, one fixed unknown law and one global uncertainty budget are different model restrictions. |
| What does a radius certify? | Expected transport error, concentration, asymptotic confidence and conditional or simultaneous coverage require separate evidence. |
| What is the observed comparison? | Model-value bounds, computed-policy errors and realized outcomes need different validation. |

The cited del Barrio–Gine–Matran 1999 Wasserstein CLT remains original-body unread. Only a partial indexed excerpt of its 2003 correction was accessible; the publisher security-check route was closed without bypass. No corrected formula or downstream guarantee is certified from that excerpt.

Original code/data availability, current reuse terms and numerical resource use were not established by this batch. Source PDFs remain private with fingerprints; no third-party PDF, raw data or program is redistributed. No financial observations, package installation, training, simulation or empirical result was produced for this register.
