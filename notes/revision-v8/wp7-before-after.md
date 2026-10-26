# V7 to integratedV8 first-passages comparison

These are exact source passages, not reconstructed quotations. Original result tables and mathematical display blocks remain unchanged. V8 corrects the evidential scope and integrates the accepted extensions; it does not claim mechanism support, causal frequency identification or a fresh independent third period.

## Abstract

### Before
```tex
Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. Long-history FX regression changes matched loss by -14.77\% and -16.62\% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction. Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.
```

### After
```tex
Risk limits on dealer positions concern the largest magnitude reached before a review horizon ends, rather than the position at its endpoint. We compare historical and conditional quantile forecasts of sampled absolute-position peaks for an FX market maker and weekly primary-dealer position aggregates. Simple historical rules prove difficult to beat. At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the previously reported later and earlier windows. Its later advantage survives a delayed adaptive coverage adjustment (ACI). Before correction, however, regression breaches more frequently, while its ranking against a shorter-history rolling rule changes across periods. After stronger regularization, regression still loses 34 of 48 additional-panel comparisons. We formalize the known-floor target and apply a classical endpoint-to-peak bound under explicit assumptions. The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series. A controlled simulation rejects a universal narrow-regime explanation, while aggregation and the overlapping backcast further qualify the empirical pattern.
```

## Introduction first paragraph

### Before
```tex
A position can finish inside its limit after exceeding that limit during the intervening period, as Figure~\ref{fig:example} illustrates. For a market maker, the relevant forecast therefore concerns the largest exposure before the next review, rather than the endpoint alone. The distinction changes the response variable, the observations available for training, and the interpretation of successful prediction. We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.
```

### After
```tex
A dealer's recorded net position can finish inside its limit after exceeding it earlier in the monitoring period, as Figure~\ref{fig:example} illustrates. The forecasting question concerns the largest sampled exposure before the next review, rather than the endpoint alone. This changes the response and when its training label becomes available. We ask whether additional conditioning improves that peak forecast once historical information is matched, and whether the gain survives alternative references and breach assessment.
```

