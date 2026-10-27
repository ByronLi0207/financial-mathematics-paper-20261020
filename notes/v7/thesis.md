# Final v7 thesis

Chosen title: **Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits**

Simple historical rules provide a demanding benchmark for forecasts of peak net-position limits. [T1; S2: PANEL_E5_QR33_LOSSES, PANEL_E5_QR33_EXPANDED_LOSSES, PANEL_E5_PLANNED]

The clearest repeated score gains arise for hourly FX positions with a long training history and a short horizon, where quantile regression improves on a historical headroom rule with the same history in both retrospective periods. [T2; S2: FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT, META_FX_HOURLY_PRIMARY_CONTRAST_HORIZON, META_FX_HOURLY_PRIMARY_CONTRAST_WINDOW]

The later-period gain also survives the evaluated coverage correction, while the regression breaches more often before correction. [T3; S2: FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT, FX_ACI_H6_W2880_QR_HITS, FX_ACI_H6_W2880_F_HITS, FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT, FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT, FX_EARLY_MATCHED_R0_STRICT_BREACH_COUNT, FX_EARLY_MATCHED_F_STRICT_BREACH_COUNT]

Against the original shorter-history rolling rule, its gain changes sign across the two periods. [T4; S2: FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT]

Other FX configurations show smaller score gains or losses and adverse breach frequencies, so the evidence supports a narrow comparative advantage rather than a universal claim about conditional models. [T5; S2: FX_LATE_SHORT_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_LATE_SHORT_H6_STRICT_BREACH_COUNT_LEFT, FX_LATE_SHORT_H6_STRICT_BREACH_COUNT_RIGHT, FX_LATE_SHORT_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_LEFT, FX_LATE_SHORT_H24_STRICT_BREACH_COUNT_RIGHT, FX_LATE_LONG_H24_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_LATE_LONG_H24_STRICT_BREACH_COUNT_LEFT, FX_LATE_LONG_H24_STRICT_BREACH_COUNT_RIGHT]

For weekly aggregate position categories, historical rules win most of the evaluated comparisons even after heavier regularization, and the earlier-period selection exercise preserves important failures. [T6; S2: PANEL_E5_QR33_EXPANDED_LOSSES, PANEL_E5_PLANNED, PANEL_R6_S1_STATUS, PANEL_R6_S3_STATUS, PANEL_SCOPE_BILL_PLUS_TWELVE, PANEL_SCOPE_NOT_INDEPENDENT_DEALERS]

Peak-limit models should therefore be evaluated jointly on forecast accuracy, breach frequency and stability across reference rules, periods and related series. [T7; S2: FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT, FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_LEFT, FX_LATE_PRIMARY_H6_STRICT_BREACH_COUNT_RIGHT, FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT, PANEL_E5_QR33_EXPANDED_LOSSES]

## Interpretation and revisions to the proposed thesis

We replace the unqualified universal “helps only” claim with a concentration of the clearest repeated evidence. Other cells can improve their score, but breach behavior, small gains and reference sensitivity remain visible. The repeated periods reuse the same market maker’s familiar history. The weekly series are related position-category aggregates; they are not separate dealers. The coverage-correction statement refers to the finite delayed projected wrappers actually evaluated. H24 preference reversal is reserved for that legacy comparison. These corrections follow notes/v7/mismatches.md (M1–M5), rather than a new calculation.

中文解释：历史规则是强对照；较清晰的重复收益出现在长历史、短期限的小时级 FX，但评分改善仍须与破线和对照依赖一起判断。周度证据属于相互关联的头寸类别加总序列，不能解释成独立交易商验证。不同参照、时期和序列下的稳定性共同决定结论。

## Alternative titles for the author

- When Do Conditional Quantiles Beat Simple Rules? Evidence from Dealer Peak Positions
- Forecasting Peak Net Positions: Narrow Gains from Conditional Quantile Models
