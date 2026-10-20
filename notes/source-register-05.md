# Reading register 05 — calibration, tail confidence and forecast instability

Checked on 20 October 2026. This is a literature-stage record, not a manuscript or a report of new empirical results. Reading depth is stated separately for every source. Recent publication and popularity are different claims; no citation or download rankings are asserted here.

The central comparison in this batch is the **object being controlled**: realized miss frequency, calibration-level regret, a fixed distribution's tail functional, or a historical path of forecast performance. These objects cannot be exchanged merely because all appear in financial forecasting.

## 1. Adaptive conformal inference

**Isaac Gibbs and Emmanuel J. Candès (2021), “Adaptive Conformal Inference Under Distribution Shift.” Advances in Neural Information Processing Systems 34, 1660–1672.**

Primary source: [official NeurIPS article and supplements](https://papers.neurips.cc/paper_files/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html). Actual sources are the 13-page conference paper and its 12-page supplement; the separate arXiv version is not silently substituted.

**Actual reading:** selected main text, including the update and endpoint conventions, Proposition 4.1 and its short proof, the hidden-Markov analysis and discussion; selected supporting proofs in the supplement. This is not a claim that every supplement argument was independently re-proved. The main proof page was also visually checked.

**Summary.** A constant-step feedback update adjusts the nominal miscoverage level after observing errors. With the stated full/empty prediction-set conventions, telescoping gives a pathwise long-run bound on realized error frequency for an arbitrary sequence. That result does not require iid observations, but it also does not give exact conditional coverage at every date, useful interval width, or control of loss severity after a miss. Stronger hidden-Markov results use additional stationarity, state-transition and score assumptions. A financial volatility application is already present, so adapting the feedback idea to stock returns alone is not a new application class. The discussion also distinguishes immediate feedback from delayed or batch outcomes.

**Transfer boundary:** choose the financial risk target before invoking this guarantee. A long-run hit-rate identity cannot by itself certify tomorrow's conditional VaR or the expected size of a tail loss.

## 2. Online aggregation under distribution shifts

**Isaac Gibbs and Emmanuel J. Candès (2024), “Conformal Inference for Online Prediction with Arbitrary Distribution Shifts.” Journal of Machine Learning Research 25(162), 1–36. Published May 2024.**

Primary source: [formal JMLR article, PDF and code links](https://jmlr.org/papers/v25/22-1218.html). The actual 36-page journal PDF is distinguished from arXiv:2208.08401v3 of October 2023.

**Actual reading:** selected definitions, Algorithms 1–2, local-regret theorem and assumptions, tracking/frequency statements and relevant proofs, financial application and diagnostic conventions. Original pages 9 and 11–13 were separately checked when comparing the claims. This is selected full-text reading, not a complete audit of every experiment or code file.

**Summary.** The method aggregates adaptive-conformal experts with different step sizes and measures regret through pinball loss in calibration-level space. Its local dynamic-regret theorem has explicit expert-grid and parameter conditions. Converting regret to parameter tracking requires additional distributional regularity. The exact long-run frequency result concerns the specified randomized procedure with decaying tuning parameters; the deterministic aggregate and practical fixed choices must be matched to the statements they actually satisfy. The paper already evaluates stock volatility forecasts, distinguishes raw and normalized scores, and uses centered coverage curves as retrospective diagnostics. Its bootstrap error bars are not presented as universally valid under arbitrary nonstationarity.

**Transfer boundary:** regret, parameter tracking, realized coverage and monetary tail loss require separate evaluation. A practical implementation needs its exact algorithm, parameter schedule and outcome timing recorded.

## 3. Confidence for heavy-tailed risk measures

**Shubhada Agrawal, Wouter M. Koolen and Sandeep Juneja (2021), “Optimal Best-Arm Identification Methods for Tail-Risk Measures.” Advances in Neural Information Processing Systems 34, 25578–25590.**

Primary source: [official NeurIPS article and supplement](https://proceedings.neurips.cc/paper_files/paper/2021/hash/d69c7ebb6a253532b266151eac6591af-Abstract.html).

**Actual reading:** selected main text through the statistical construction and identification result; supporting confidence/correctness passages in Appendix F, the auxiliary mixture argument, and the computational caveats in Appendix L. The downloaded 13-page main paper and 57-page supplement were version-fingerprinted locally. This is not a reproduction of the numerical experiments or a complete supplement reading.

**Summary.** The paper develops time-uniform confidence constructions for CVaR and other risk measures, then uses them for fixed-confidence best-arm identification. CVaR results maintain a known moment class with specified positive moment excess and moment bound. Arm observations come from fixed iid distributions, although the arm sampled next may be selected adaptively. The proof controls optimized likelihood criteria through mixtures with explicit penalties; hindsight maximization is not itself declared a safe capital process. The reported computational section also uses a smaller experimental threshold for which the stated general guarantee is not proved. This is an important distinction between a theoretical threshold and a practical numerical choice.

**Transfer boundary:** observing several correlated financial assets at once is different from updating one sampled bandit arm per round. An empirical tail-moment estimate cannot simply replace the known population-class bound.

## 4. Forecast comparisons in unstable environments

**Raffaella Giacomini and Barbara Rossi (2010), “Forecast comparisons in unstable environments.” Journal of Applied Econometrics 25(4), 595–620. DOI [10.1002/jae.1177](https://doi.org/10.1002/jae.1177).**

Formal metadata is checked against the publisher record. Actual full text is the **August 2008 author manuscript**, 34 pages, linked from the [Centre for Finance research entry](https://centreforfinance.org/researchdetail.htm?research=289). The final 2010 typeset text was not obtained or assumed identical.

**Actual reading:** selected Sections 3.1–3.3 and their assumptions, complete displayed proofs of Propositions 1 and 3, selected empirical discussion and critical-value table. The proof page was visually inspected because the extracted PDF font loses some mathematical symbols.

**Summary.** The paper studies forecast comparisons whose relative performance can vary over the evaluation period. A full-period average can hide local differences. Its fluctuation and reversal procedures use functional limit theory, specified window fractions or trimming, and appropriate long-run variance assumptions. The null concerns date-by-date unconditional expected loss differences rather than a universal conditional martingale restriction. Centered historical windows and full-sample variance estimation are retrospective objects. A simultaneous finite-horizon test should be distinguished from repeatedly applying a fixed pointwise test or extending monitoring indefinitely. Exchange-rate forecasts against benchmark models are already an empirical application.

**Transfer boundary:** rejecting stable equality does not alone identify a profitable switching date, establish a causal live signal, or give an anytime guarantee. The evaluation endpoint, scan family, window choices and information available at each forecast date matter.

## Cross-source implications

| Literature object | What it measures | What remains separate |
|---|---|---|
| ACI error-frequency identity | Realized average misses under specified feedback/endpoints | Conditional coverage, width and severity |
| Online calibration regret | Pinball performance against a changing calibration-level comparator | Economic value and tail-capital adequacy |
| Tail-risk identification | Confidence about fixed arm distributions under a known moment class | Changing conditional market laws and correlated simultaneous streams |
| Instability scan | Relative historical expected-score behavior across a specified scan | Live model selection, transaction costs and unbounded-horizon monitoring |

These are mature precedents and applicability checks. They narrow what can responsibly count as a method transfer; they do not establish an unoccupied research question. No final topic, frozen design, financial experiment or completed manuscript is claimed. The six-hour reading requirement remains governed by the separately recorded active-work ledger, not by elapsed clock time or paper counts.
