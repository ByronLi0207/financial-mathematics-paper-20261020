# Initial literature register — 20 October 2026

**Status: initial screening and selected full-text reading.** This register is not a completed six-hour review, a final novelty assessment, or an empirical result. No final research question has been selected. Exact versions are retained because titles and claims change across revisions.

## Recent methods and nearest applications

### 1. Causal distributionally robust optimization

Yifan Jiang, *Duality of causal distributionally robust optimization*, [arXiv:2401.16556v3](https://arxiv.org/abs/2401.16556v3), revised 17 August 2026. Initial work has inspected selected mathematical sections; a complete proof audit remains pending. The framework respects information flow through adapted transport and treats worst-case expectation, expected shortfall and stopping problems. A possible transfer must preserve the filtration and ambiguity-set assumptions. Replacing a dynamic causal problem with ordinary static Wasserstein robustness is not an automatic equivalent. Next: compare the discrete-time construction, tractability and the exact uncertainty constraint with the candidate financial decision.

### 2. Distortion riskmetrics under Wasserstein ambiguity

Yang Liu, Qiuqi Wang and Yihan Wang, *Robust distortion riskmetrics under Wasserstein ambiguity*, [arXiv:2610.09622v1](https://arxiv.org/abs/2610.09622v1), 7 October 2026. Metadata and abstract verified; selected full-text methods are under review. The paper addresses objectives beyond continuous convex distortion functions and studies robust portfolio decisions. It is a close prior for any proposed Wasserstein VaR/Range-VaR extension. Its approximation and error-control conditions must be read before proposing a supposedly new risk objective. Recent publication alone supplies no evidence of popularity or correctness.

### 3. Nonstationary portfolio VaR calibration

Marc Schmitt, *Taming Tail Risk in Financial Markets: Conformal Calibration for Nonstationary Portfolio VaR*, [arXiv:2602.03903v3](https://arxiv.org/abs/2602.03903v3), revised 3 August 2026. Selected full-text sections 4–7 were inspected. Earlier v2 has a different title; this register cites v3. The study already combines state/time weighting, effective-sample-size diagnostics, French portfolio applications, modern conformal baselines and cost-sensitive evaluation. Therefore, adding state weights to French portfolio VaR is not by itself a new contribution. The theorem assumptions and the distinction between retrospective coverage and conditional forecasting require further checking. The paper's own stated future work is not evidence that the entire field lacks those extensions.

### 4. Sequential comparison of risk forecasts

Zhanyi Jiao, Qiuqi Wang and Yimiao Zhao, *Comparative e-backtests for general risk measures*, [arXiv:2511.05840v2](https://arxiv.org/abs/2511.05840v2), revised 5 March 2026. Selected v1 HTML passages in sections 2–4 were read; the current v2 version has been identified but its full text still needs a version-specific audit. The inspected construction uses predictable forecasts and bets, nonnegative factors, and conditional null hypotheses to obtain sequential validity. “Allows dependence” does not remove those conditions. Standard calibration and comparative forecast quality are different targets. Next: use v2, check scoring-function bounds, and compare the empirical setup with any proposed monitoring problem. Do not silently cite the earlier title as the current title.

### 5. Expected-shortfall backtesting without VaR reports

Ruodu Wang and Jingcheng Yu, *E-Backtesting Expected Shortfall without Value-at-Risk Forecasts under Time-series Models*, [arXiv:2610.17681v1](https://arxiv.org/abs/2610.17681v1), 13 October 2026. Metadata and abstract were verified, with selected method passages under review. The time-series proposal relies on a fixed parameter–quantile representation of the conditional VaR path and a positive reporting margin. A proposal to eliminate auxiliary VaR forecasts must compare against this direct prior. Its continuous profiling and numerical-grid bounds also matter for the small-compute constraint. No claim of a fully model-free ES-only extension is supported at this stage.

## Evidence of attention

The [SIAM September 2025 prize spotlight](https://www.siam.org/publications/siam-news/articles/september-2025-prize-spotlight/) supplies an official attention signal for martingale optimal transport, signature calculus and diffusion/factor modeling. The prize is evidence of professional recognition, not proof that a particular paper is the most cited or that a method will work here. These subjects remain in the reading queue; expensive generative-model training is outside the present computational budget.

## Small-data feasibility

The initial source audit has checked official French portfolio, ECB yield-curve and BIS exchange-rate sources using only very small requests. The objects differ: constructed portfolio returns, fitted yields and reference FX levels cannot be treated as interchangeable tradable returns. Full datasets have not been analyzed. Raw-data redistribution permission must be checked separately from download access. Source-linked detail and revision limitations remain in the local research notes pending further review.

## Questions for continued reading

1. Which distinct financial decision genuinely needs causal or path-dependent robustness, and can a useful small discrete-time case be solved and validated?
2. Which aspect of sequential risk evaluation remains different from existing standard/comparative e-backtests, and can its assumptions hold for observable financial data?
3. Can a carefully delimited diagnostic or robustness result reveal a practically important failure or trade-off without claiming a new forecasting wrapper?

These are literature-search questions, not an approved experiment or a novelty claim. The next stage remains primary-paper reading, theorem-condition checks, citation-chain searches and comparison with stronger near-neighbors.
