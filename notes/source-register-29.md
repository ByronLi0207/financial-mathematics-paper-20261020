# Source register 29 — conditional EVT paths and extreme risk corridors

**Selected primary-source reading, 20 October 2026.** Two principal entries consolidate completed selected reading. Formal references and actual author manuscripts are distinguished. Other references below are access-boundary records only. This administrative update adds no original-body reading, project data/results or selected design.

## 1. Conditional EVT and accumulated future losses

**Alexander J. McNeil and Rüdiger Frey(2000), “Estimation of tail-related risk measures for heteroscedastic financial time series: an extreme value approach,” Journal of Empirical Finance7(3–4),271–300.** [Formal DOI](https://doi.org/10.1016/S0927-5398(00)00012-8).

Actual body read: **[Frey's university-linked author manuscript](https://statmath.wu.ac.at/~frey/publications/evt-garch.pdf)**, title-page date **19June1999**,29physical pages. The formal2000body was not version-compared.

**Source synthesis — 139 words.**

<!-- SYNTHESIS_1_START -->
McNeil and Frey combine volatility filtering with generalized-Pareto residual tails to estimate conditional financial risk. Their inspected1999manuscript distinguishes stationary marginal tails from next-period losses and accumulated future negative log returns. Rolling models and threshold choices retain dynamic-model and tail-approximation assumptions. Stock, currency and gold applications already examine one-day VaR and shortfall. For multi-day VaR, empirical-center/GPD-tail innovations drive fitted future paths, cumulative path losses are formed, and another tail fit estimates extreme quantiles. This approximates a fitted future-loss law rather than parameter-estimation confidence. The authors treat overlapping multi-day violation comparisons qualitatively, leave multi-day ES unimplemented in this edition, and retain rejections in some one-day ES checks. Selected passages and three page images were read. Unavailable text segments, outside likelihood/bootstrap proofs, formal-version equivalence, numerical reproduction and materials rights remain unverified. Neither model fitting nor favorable violation counts establish universal calibrated coverage.
<!-- SYNTHESIS_1_END -->

## 2. Extreme distortion risks and expectile confidence corridors

**Yannick Hoga(2022), “Limit Theory for Forecasts of Extreme Distortion Risk Measures and Expectiles,” Journal of Financial Econometrics20(1),18–44.** [Formal DOI](https://doi.org/10.1093/jjfinec/nbz032). Formal online publication20December2019 is distinct from the2022issue.

Actual body read: **[university author PDF](https://www.oek.wiwi.uni-due.de/fileadmin/fileupload/VWL-OEK/Limit_Theory_for_Forecasts_of_Extreme_Distortion_Risk_Measures_and_Expectiles.pdf)**, title-page date **5July2018**,26physical/printed pages. Equality with the formal2022body or supplement was not certified.

**Source synthesis — 142 words.**

<!-- SYNTHESIS_2_START -->
Hoga derives asymptotic intervals and level-indexed confidence corridors for extreme conditional distortion risks and expectiles. Filtered location-scale models combine Pareto extrapolation, second-order bias restrictions and residual-tail limit assumptions. First-stage parameter uncertainty becomes negligible only under the specified estimator rate, derivative envelopes and tail-count sequence. A shared leading quantile fluctuation supplies uniformity across a fixed compact range of tail-level multipliers at one forecast origin. This does not justify joining arbitrary point intervals or monitoring all future dates. Distortion integrability, expectile existence and maintained innovation moments remain separate conditions. Existing equity, index, volatility, oil and currency examples compare rolling extreme-value and empirical forecasts. Deeper extrapolation can worsen coverage, while score gains vary with sample size and significance. Selected July2018statements and local proof routes were read. Detailed numerical tables, external arguments, formal2022changes, implementation and materials permissions remain unverified. Forecast scores do not certify interval coverage.
<!-- SYNTHESIS_2_END -->

## Actual editions and recorded root scope

These are selected ranges, not complete-paper or complete-proof certification. Supporting records do not enlarge root's scope or hours.

| Source | Actual edition | Root selected reading | Remaining boundary |
|---|---|---|---|
|McNeil–Frey|29-page author manuscript,19June1999|Original reader text PDF1–19: definitions/model/tail methods1–11; one-day evaluation11–13; visible ES portions14–16; multi-day paths, overlap and conclusion16–19. Existing original-page images7,17and18visually inspected.|A paragraph onPDF5 and the latter portion ofPDF14were not fully available and were not reconstructed. Tables/figures not audited cell by cell; remaining pages, full references and external proofs not read; formal2000version not compared.|
|Hoga|26-page author manuscript,5July2018; physical/printed numbering coincide|Selected introduction, definitions, extrapolation, model, Assumptions1–5, Theorems1–2 and setup PDF1–11; selected simulation interpretation/application/conclusion16–20; local proof routes21–24; references25–26screened. Existing original-page images8,10,11,17and24visually inspected.|Simulation tables12–15 and their detailed results unread; table cells18–20displayed but not individually audited; external proofs, formal-version changes and implementation unverified.|

Unavailable paragraphs are a real reading boundary, not text reconstructed from later literature. Local proof routes do not imply that every invoked external lemma, entire article or formal edition was read.

## Original crosswalk of financial targets and inference

| Distinction | Boundary retained |
|---|---|
|Future-loss paths versus risk-estimator confidence|McNeil–Frey simulate a fitted law of accumulated future losses. Parameter confidence intervals concern uncertainty in an unknown risk value; future path draws at fitted coefficients do not automatically incorporate that estimation variation.|
|A future date versus a holding period|A future-date return differs from the sum of negative log returns over a holding period. Neither is automatically a drawdown or nonlinear portfolio-payoff law.|
|Forecast horizon versus probability index|Five-/ten-day loss horizons are time aggregation. Hoga's corridor multiplier indexes tail probabilities at one origin, not future calendar dates.|
|Overlapping outcomes versus independent trials|Daily-issued multi-day outcomes overlap. The source retains qualitative violation-count comparisons rather than treating them as exact independent single-day binomial trials.|
|Fixed fitted dynamics versus joint inference|Gaussian pseudo likelihood is an estimation device, not a normal-innovation truth assumption. It does not itself provide a joint GARCH/tail estimator confidence theorem.|
|First-stage negligibility versus known parameters|Hoga requires estimator-rate separation, derivative control and residual-tail limits. Fitting a model does not establish that filtering uncertainty is negligible.|
|Point intervals versus an indexed corridor|A shared uniform leading fluctuation supports the studied compact level-indexed corridor. Arbitrary pointwise intervals cannot inherit that argument by being plotted together.|
|Scores versus risk-interval coverage|Realized forecast scores, risk violations, tail-estimation MSE and confidence coverage are different evidence products. Improvement in one does not certify the others.|
|Tail-model classes|Threshold-excess GPD theory covers a broader maximum-domain-of-attraction setting. Hoga's selected extreme theory uses positive regular variation and explicit second-order restrictions; assumptions are not interchangeable.|
|Expectile level versus exceedance probability|An expectile is a distinct functional. A tail approximation does not turn its finite level into a quantile probability or make it identical to ES.|

These are established financial methods and interpretation limits. Changing an asset, a window or a horizon does not itself establish methodological novelty. Historical unimplemented extensions are not current absence findings.

## Conditions that remain substantive

McNeil–Frey's working conditional mean/scale model uses iid standardized innovations independent of the past. Classical threshold-excess and likelihood theory is invoked, with threshold approximation bias and sample variation retained. Its rolling implementation's historical window and tail count are source choices, not universal asymptotic verification for every financial series.

The innovation simulator combines an empirical center with fitted positive and negative tails. The future dynamics evolve along each path, and path losses are accumulated before extreme quantile estimation. Historical-length parameter refitting is a different procedure. The actual edition applies the path method to multi-day VaR and leaves multi-day ES unimplemented.

Its one-day ES diagnostic uses exceedance-day standardized residuals and a one-sided bootstrap mean comparison. Appropriate quantile/tail-mean and model premises remain relevant; this is not an ES-only procedure valid under arbitrary incorrect VaR or dependence. Outside bootstrap-test arguments were not read.

Hoga's distortion is fixed rather than selected over an unknown preference class. Its tail anchor and target levels both tend to the endpoint, with a diverging anchor count and a specified extreme target-count sequence. Second-order tail bias must vanish at the stated normalization. Distortion-specific integrability is separate from maintained mean-zero/unit-variance innovations and the expectile clause's existence restrictions.

The first-stage rate and fitted residual tail-index/order-statistic assumptions must be verified for the estimator actually used. Infinite-history truncation and some model verification are referred externally in this edition. A formal risk representation or root-n parameter estimate alone does not certify the entire chain. Ordinary conditional-risk asymptotics are not automatically full-history exact conditional coverage under the separate conditional-confidence framework.

The level corridor uses a fixed positive compact multiplier interval. It does not establish coverage over an expanding index set, arbitrarily selected distortions, opposite-tail ratios, many assets, repeated origins or stopping times. The later multi-level literature in register28uses different index ranges, regimes and bootstrap constructions.

## Existing applications and adverse evidence

The McNeil–Frey manuscript already applies filtering plus EVT to equity indices, an individual equity, an exchange rate and gold. Some one-day ES checks reject. Multi-day counts are explicitly interpreted qualitatively; closeness to expected counts is not converted into a significance or superiority claim.

The actual Hoga application uses rolling financial examples across equity, index, volatility, oil and currency series. Its abbreviation CVaR denotes conditional VaR in this source, rather than being silently relabelled expected shortfall. Forecast comparisons use target-appropriate scores and pairwise comparisons. Deeper extrapolation can harm finite-sample coverage; score advantages depend on sample size, and many extreme-level comparisons are not statistically separated. Estimated historical latent risk values are not directly observed, so application scores do not certify interval coverage.

No observation dataset, author program, preprocessing pipeline or current provider/redistribution permission was obtained or verified during this curation. Source computational examples are not project runs or resource measurements. Only original synthesis is delivered, without source PDFs or substantial third-party passages.

## External references: access boundaries only

The completed access records for the following direct dependencies do not establish body reading. They add no principal source synthesis or original-body credit:

| Reference identity | Evidence boundary |
|---|---|
|Feng Gao and Fengming Song(2008), Estimation Risk in GARCH VaR and ES Estimates; [DOI](https://doi.org/10.1017/S0266466608080559)|Formal metadata/abstract and author bibliographic record only. The stated PDF route returned abstract HTML, not a paper. No actual PDF page count, byte hash, theorem or proof reading.|
|Yannick Hoga(2019), Confidence Intervals for Conditional Tail Risk Measures in ARMA–GARCH Models; [DOI](https://doi.org/10.1080/07350015.2017.1401543)|Institutional bibliographic/abstract-level evidence only; original body and supplement unavailable in the completed check. No formal-page span is presented as pages actually read.|
|Abdelaati Daouia, Stéphane Girard and Gilles Stupfler(2018), Estimation of Tail Risk Based on Extreme Expectiles; [DOI](https://doi.org/10.1111/rssb.12254)|Bibliographic/indexed evidence and the fact of Hoga's citation only. Original article, cited corollary and supplement were not obtained. No specific manuscript edition or original PDF fingerprint is certified.|

Hoga also invokes distortion approximation/integrability, extreme-quantile and earlier residual/uniform results from outside sources. These were outside the recorded Hoga reading above; separately recorded follow-up reading does not enlarge that entry. No later paraphrase fills an unread original. Access limits are not evidence of a methodological gap, invalidity or nonexistence.

## De-duplication and retained original fingerprints

Registers01–28 were checked by exact titles, formal DOI identifiers and original-source identity. Neither principal source had a dedicated earlier entry. Prior McNeil spectral backtesting and Hoga measurement-error/systemic-risk records concern different papers. Unread access-boundary references above are not promoted to principal reading.

The two retained author PDFs were rehashed and matched recorded bytes/SHA-256. Fingerprints identify those actual manuscripts, not the unread formal editions, complete proof correctness, observation vintages or executable implementations. Curation adds zero source-body reading credit.

| Actual retained original PDF | Bytes | SHA-256 |
|---|---:|---|
|McNeil–Frey,19June1999author manuscript|489777|9ab9f1149fe5acb8e9e6502e245676a855c4c629e3207179d4c0090acc465e03|
|Hoga,5July2018author manuscript|447980|81a4470ea8a8fb71baf8289497819084b2811d2ee4f069c96003c57adbb1b4b9|

