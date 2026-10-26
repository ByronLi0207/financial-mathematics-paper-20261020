# WP1 original/revised passages

All changes concern prose. Original tables, mathematics and results remain unchanged. Coarser percentage displays are checked directly against raw saved fields.

## Edit 1

Reason: Natural reduction language, one-decimal display of unchanged saved results; define the coverage adjustment at first appearance.

Before:

```tex
Long-history FX regression changes matched loss by -14.77\% and -16.62\% in the later and earlier periods. Its later advantage survives the evaluated finite delayed coverage correction.
```

After:

```tex
At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the later and earlier periods. Its later advantage survives a delayed adaptive coverage adjustment (ACI).
```

## Edit 2

Reason: Lead with the research question; remove unit-handling process detail from Introduction and explain the forecast target directly.

Before:

```tex
Our empirical comparison joins an hourly FX market-maker record with weekly U.S. primary-dealer position-category aggregates, using a common forecasting objective. The methods predict source-native peaks separately for each series, so monetary magnitudes from different reporting systems remain separate throughout evaluation. We compare regression, local quantiles, historical rules, and additional conditional benchmarks on the same completed response within each comparison. The evidence asks where added conditioning helps, whether that advantage survives a change of reference, and how scores relate to breaches.
```

After:

```tex
We study an hourly FX market-maker record and weekly U.S. primary-dealer position aggregates, asking where conditioning improves peak forecasts. Historical rules, regression and local quantiles compete to predict the same peak within each series, using only information available at issue. These comparisons reveal whether gains persist across reference rules and periods, and whether better scores also mean fewer breaches.
```

## Edit 3

Reason: Express the direction in words; round only prose display.

Before:

```tex
Against a historical headroom rule with the same history, its later-period loss changes by -14.77\%. The earlier-period matched comparison changes loss by -16.62\%, and the evaluated coverage correction preserves the later advantage.
```

After:

```tex
Against a historical headroom rule with the same history, it lowers later-period loss by 14.8\%. The earlier-period reduction is 16.6\%, and the delayed coverage adjustment preserves the later advantage.
```

## Edit 4

Reason: Define Murphy diagrams on first appearance and state the finding rather than the reporting procedure.

Before:

```tex
Elementary-score curves and error-weight comparisons show why these assessments can disagree, with the relevant comparison stated explicitly in each case.
```

After:

```tex
Murphy diagrams plot mean elementary quantile scores across thresholds, showing how rankings vary across consistent scoring rules. Together with error-weight comparisons, they explain why better average scores can coexist with more breaches.
```

## Edit 5

Reason: C2 opens with the observed judgment, without asserting an identified frequency effect before WP4.

Before:

```tex
We find that conditional-model gains vary across the observed frequency, training-history and forecast-horizon settings.
```

After:

```tex
We find that historical rules win most weekly comparisons; repeated regression gains appear in long-history FX data at the shorter horizon.
```

## Edit 6

Reason: Replace jargon and explain the purpose of the comparisons.

Before:

```tex
We compare same-history controls with the original shorter-history rolling controls, examine two periods, and assess elementary-score curves alongside error-weight preferences.
```

After:

```tex
We compare same-history and shorter-history rolling controls across two periods, using Murphy diagrams and error-weight preferences to interpret the rankings.
```

## Edit 7

Reason: Replace process-oriented positioning language with a direct account of the literature distinction.

Before:

```tex
The positioning in Table~\ref{tab:literature} locates the substantive comparison in the peak response, completed labels and explicitly matched reference rules.
```

After:

```tex
Table~\ref{tab:literature} shows how the peak response, mature training labels and matched reference rules distinguish the present forecasting comparison.
```

## Edit 8

Reason: Use natural language for favorable loss changes and one-decimal prose.

Before:

```tex
The later-period matched loss change is -14.77\%, while the earlier-period matched change is -16.62\%.
```

After:

```tex
It lowers matched loss by 14.8\% in the later period and 16.6\% in the earlier period.
```

## Edit 9

Reason: Explain why the reference matters before describing table layout.

Before:

```tex
Table~\ref{tab:fx} shows that these gains refer to the same-history controls, with separate columns for the original shorter-history rolling reference. The distinction matters because model choice and the amount of historical information answer different comparative forecasting questions.
```

After:

```tex
The same-history comparison holds the amount of training information fixed, whereas the shorter-history rolling reference also changes the available history. The matched gains in Table~\ref{tab:fx} therefore isolate a different comparison from the original rolling-reference result.
```

## Edit 10

Reason: Replace wrapper jargon; preserve the finite-procedure scope and both breach counts.

Before:

```tex
The evaluated calibration wrappers preserve the long-history matched FX advantage while bringing the two observed breach frequencies close together. Wrapped regression changes mean loss by -15.00\% against the wrapped historical reference on their common evaluation grid. Their strict breach counts are 329 and 328, respectively. This result gives a concrete calibration comparison for the actual finite delayed procedures rather than treating the unwrapped score gain as a coverage result.
```

After:

```tex
The delayed ACI adjustment preserves the matched FX score advantage while bringing the two observed breach frequencies close together. Adjusted regression lowers mean loss by 15.0\% against the adjusted historical reference on their common evaluation grid. Their strict breach counts are 329 and 328, respectively. This comparison shows that the score gain survives the adjustment, with nearly equal breach frequencies for these two implemented procedures.
```

## Edit 11

Reason: Natural direction and one-decimal prose; underlying result files and tables unchanged.

Before:

```tex
At the lower target, the matched relative loss change is -10.15\%, and the original-primary reference gives -9.20\%.
```

After:

```tex
At the lower target, regression lowers loss by 10.1\% against matched headroom and by 9.2\% against the original rolling reference.
```

## Edit 12

Reason: Keep the unfavorable reversal explicit, with positive direction in words.

Before:

```tex
Against the original shorter-history rolling rule, the later loss change is -12.66\%, whereas the earlier-period change is 3.17\%.
```

After:

```tex
Against the original shorter-history rolling rule, it lowers later-period loss by 12.7\% but raises earlier-period loss by 3.2\%.
```

## Edit 13

Reason: Replace commentary about presentation with the substantive adverse finding.

Before:

```tex
Table~\ref{tab:fx} makes that reversal part of the main result instead of treating it as a secondary qualification.
```

After:

```tex
The reversal in Table~\ref{tab:fx} shows that a matched-history gain can coexist with failure against the simpler operational reference.
```

## Edit 14

Reason: One-decimal prose; adverse finding preserved.

Before:

```tex
The short-history FX regression at the longer horizon raises mean loss by 31.50\% relative to its matched historical headroom rule.
```

After:

```tex
The short-history FX regression at the longer horizon raises mean loss by 31.5\% relative to its matched historical headroom rule.
```

## Edit 15

Reason: Use converged fits and clear adverse language without suggesting numerical convergence proves financial usefulness.

Before:

```tex
The original Treasury-bill primary is adverse in both its score and its breach count, despite numerically accepted regression fits. Its relative loss increase is 50.79\%, with 54 regression breaches on the evaluation grid.
```

After:

```tex
The original Treasury-bill primary loses on both score and breach count. Its loss increase is 50.8\%, with 54 regression breaches on the evaluation grid.
```

## Edit 16

Reason: Natural favorable/adverse directions and one-decimal prose; no unfavorable procedure removed.

Before:

```tex
The fixed median combination improves on the bill historical reference by a relative loss change of -3.98\%. The fixed mean combination instead changes that loss by 2.77\%, and the headroom quantile recursion is also worse than the reference in that primary context.
```

After:

```tex
The fixed median combination lowers loss against the bill historical reference by 4.0\%. The fixed mean combination instead raises loss by 2.8\%, and the headroom quantile recursion also performs worse than that reference.
```

## Edit 17

Reason: Define the breach event directly instead of naming an internal indicator.

Before:

```tex
Pinball loss accounts for the magnitudes of underprediction and overprediction, whereas the strict-hit indicator records only the occurrence of an exceedance.
```

After:

```tex
Pinball loss measures the sizes of underprediction and overprediction; a strict breach records whether the realized peak exceeds its forecast.
```

## Edit 18

Reason: Use the established label and lead with its meaning.

Before:

```tex
Elementary-score comparisons show a further dependence on the evaluation question even when the quantile level and the two reports stay fixed.
```

After:

```tex
Murphy diagrams reveal that forecast rankings can depend on the scoring rule even when the quantile level and reports stay fixed.
```

## Edit 19

Reason: Replace internal hit-sequence wording with the observable event.

Before:

```tex
A loss-difference test concerns average relative accuracy, while coverage tests concern the frequency and temporal behavior of the strict-hit sequence.
```

After:

```tex
A loss-difference test concerns average relative accuracy, while coverage tests concern the frequency and temporal pattern of forecast breaches.
```

## Edit 20

Reason: Directly state the measurement distinction in Data, where unit handling belongs.

Before:

```tex
We preserve the distinction between a single market maker's FX record and signed weekly position aggregates compiled across primary dealers.
```

After:

```tex
The FX record describes one market maker, while the weekly series combine signed positions across primary dealers.
```

## Edit 21

Reason: Conclusion answers the question through a finding, without reporting the order of questions.

Before:

```tex
These findings answer the first research question through a specific successful setting rather than a broad ranking of conditional models.
```

After:

```tex
The useful gain is therefore specific: long-history short-horizon FX regression beats matched headroom, while its broader ranking depends on the reference.
```

## Edit 22

Reason: State the unfavorable transport finding, without attributing it causally to frequency.

Before:

```tex
The second research question concerns stability across related tasks, and the weekly evidence gives a predominantly adverse answer for the evaluated regressions.
```

After:

```tex
The weekly comparisons show that the successful FX specification does not transport reliably to related peak-position tasks at the lower frequency.
```

## Edit 23

Reason: State the validation lesson directly.

Before:

```tex
The third question concerns validation: lower average quantile loss, fewer breaches, and stable rankings are different requirements with distinct empirical outcomes.
```

After:

```tex
Lower average quantile loss, fewer breaches and stable rankings impose different requirements, and these data frequently rank them differently.
```

## Edit 24

Reason: State the research question directly in the introduction opening.

Before:

```tex
We study how established historical and conditional forecasts perform when every method targets this same sampled absolute-position peak.
```

After:

```tex
We ask whether conditional forecasts can improve on historical rules for this sampled absolute-position peak.
```

## Edit 25

Reason: Use past peaks in the motivation; retain the exact mature-label condition in Evaluation design.

Before:

```tex
A conditional model must improve on that information while estimating additional relationships from a finite, changing sequence of completed outcomes.
```

After:

```tex
A conditional model must improve on that information while estimating additional relationships from a limited and changing sample of past peaks.
```

## Edit 26

Reason: Keep the Murphy, weight-sensitivity and matched-breach comparisons distinct instead of implying one identical contrast.

Before:

```tex
Murphy diagrams plot mean elementary quantile scores across thresholds, showing how rankings vary across consistent scoring rules. Together with error-weight comparisons, they explain why better average scores can coexist with more breaches.
```

After:

```tex
For the separately named comparisons, Murphy diagrams plot mean elementary quantile scores across thresholds, revealing where consistent scoring rules give different rankings. Error-weight comparisons show how preferences between fixed forecasts depend on the relative penalties on underprediction and overprediction.
```

## Edit 27

Reason: Keep the required article roadmap concise and end with the substantive takeaway.

Before:

```tex
The paper develops the forecast target before describing the data, methods, and chronological evaluation design used for the empirical comparisons. The results separate settings with conditional gains from settings with losses, then examine the differences between scores and breach behavior. A final validation checklist turns those findings into concrete controls for comparing candidate peak limits across reference rules, periods, and series. The central message is that complexity earns its place through a stable comparative advantage on the quantity that the limit actually monitors.
```

After:

```tex
The remaining sections define the peak target, describe the data and forecasts, and compare accuracy, breaches and stability before drawing implications for model validation. Complexity earns its place through a stable comparative advantage on the quantity that the limit actually monitors.
```

## Edit 28

Reason: Make the short-horizon scope explicit in the abstract.

Before:

```tex
Long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the later and earlier periods.
```

After:

```tex
At the shorter horizon, long-history FX regression lowers matched loss by 14.8\% and 16.6\% in the later and earlier periods.
```

## Edit 29

Reason: Remove the unneeded numerical-fit qualification rather than add an unverified convergence assertion.

Before:

```tex
The original Treasury-bill primary loses on both score and breach count, despite converged regression fits.
```

After:

```tex
The original Treasury-bill primary loses on both score and breach count.
```

## Edit 30

Reason: Use the established figure name consistently after its first definition.

Before:

```tex
Elementary quantile-score curves for the original short-horizon FX primary.
```

After:

```tex
Murphy diagram for the original short-horizon FX primary.
```

## Edit 31

Reason: Use the established figure name consistently after its first definition.

Before:

```tex
Elementary quantile-score curves for the original Treasury-bill primary.
```

After:

```tex
Murphy diagram for the original Treasury-bill primary.
```
