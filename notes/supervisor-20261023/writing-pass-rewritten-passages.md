# Revised paper passages

## Abstract

Dealers monitor the largest absolute net position reached during a holding period. We ask whether conditional quantile methods forecast this peak better than historical rules. We compare hourly FX and weekly New York Fed dealer positions, matching training histories and update schedules. Historical rules are hard to beat. In FX, regression lowers loss against its matched rule by 14.8%, and by 16.6% in an earlier 2015 period not previously used for evaluation in this study. Its loss against the short-history rolling rule rises 3.2% in that earlier period. On weekly positions, Treasury-bill loss rises 50.8%; stronger regularization still leaves 34 of 48 cells across 12 further series behind historical headroom. Scores and breaches also diverge: the main FX gain accompanies breaches rising from 332 to 376. Peak-position comparisons should therefore report both scores and breaches. The evidence is retrospective, and the original FX evaluation period was inspected before the conditional methods were specified.

## Introduction: contribution paragraphs

The paper makes three empirical points. First, the historical benchmark matters for FX forecasts. Regression lowers matched loss by 14.8% in the original period and 16.6% in the earlier 2015 period. It beats the short-history rolling rule only in the original period (Tables 3 and 10).

Second, weekly regression struggles against historical headroom. The Treasury-bill main comparison loses 50.8%. Across 12 further weekly series, expanded-menu regression still loses in 34 of 48 cells (Figure 3). Conservative one-standard-error selection also leaves large weekly losses (Section 7).

Third, lower pinball loss need not mean fewer breaches. The main FX gain accompanies 376 breaches against 332 for its rolling reference. Neither main comparison dominates across consistent quantile scores (Table 8; Appendix A.6). All methods are standard; the contribution is this evidence for the sampled peak, extending the endpoint question studied by Wisniewski et al. (2020).

## Implications for position monitoring

**Benchmark against historical headroom.** Compare conditional reports with historical headroom on the same completed labels and update schedule. Original regression loses all Treasury-bill comparisons and most additional weekly panel cells.

**Default to corrected-rank headroom in short weekly samples.** Use the corrected-rank historical rule as the starting point for these short samples. Wider penalties and conservative one-standard-error selection leave large losses, while the ordinary empirical quantile's excess loss reaches +36.5%.

**Report breaches with the score.** Show underprediction amounts, overprediction amounts and breach counts alongside pinball loss. The main FX gain accompanies more breaches, so a lower score alone misses part of the monitoring outcome.

## Conclusion

Simple historical rules are hard to beat when forecasting peaks of dealer net positions. In hourly FX, regression improves on matched historical headroom in both evaluation periods (14.8% and 16.6%). Its gain over the short-history rolling rule appears only in the original period; earlier loss increases 3.2%.

On weekly positions, stronger regularization narrows regression's gap, but 34 of 48 panel cells still lose. Conservative one-standard-error selection also leaves large weekly losses. Lower pinball loss and fewer breaches diverge in the main FX comparison, and both main Murphy curves cross. Position-limit model selection should therefore compare historical rules and report both error amounts and breaches. These retrospective findings from two sources provide no conditional-coverage guarantee and measure no trading or funding benefit.
