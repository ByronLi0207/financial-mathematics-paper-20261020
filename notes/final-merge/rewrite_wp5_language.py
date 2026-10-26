"""Apply WP5 prose edits to the WP4 cut; saved results and protocols are read-only."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'submission-final/manuscript.tex'
text=p.read_text()
def change(old,new):
    global text
    # Whitespace is typographical, while every substantive source phrase must
    # match exactly once. This also makes a second application fail closed.
    pattern=r'\s+'.join(re.escape(s) for s in old.split())
    matches=list(re.finditer(pattern,text))
    if len(matches)!=1:raise ValueError((len(matches),old[:130]))
    m=matches[0];text=text[:m.start()]+new+text[m.end():]

abstract="""Position limits concern the largest sampled absolute net position during a review period, which an endpoint forecast can miss. We compare historical and conditional quantile forecasts using one FX market maker's positions and aggregate dealer records from the New York Fed and CFTC. Historical rules are difficult to beat across these records, while longer-history FX gains coexist with adverse weekly outcomes and important exceptions. Simulations, learning curves and the partly supported CFTC check are consistent with estimation costs varying with history and shrinkage, while causal attribution remains unresolved. Practical validation should compare scores, breaches and stated limit costs against matched historical benchmarks, since different charges can favor different procedures."""
text=re.sub(r'(?<=\\begin\{abstract\}).*?(?=\\end\{abstract\})',lambda m:abstract,text,flags=re.S)

change(r'''Position limits must cover exposure between reviews. A position that finishes
inside a limit can still breach it earlier, so an endpoint forecast answers a
different question from a forecast of the intervening peak. We study the largest
sampled absolute net position and compare all procedures on that same response.''',r'''Position limits must cover exposure between reviews, since a position that finishes inside a limit can still breach it earlier.
An endpoint forecast therefore answers a different question from a peak forecast, motivating comparisons on the largest sampled absolute net position.''')
change(r'''A selected Treasury-bill path that returns within the reported historical limit at its endpoint after an intervening breach. The rule chooses the earliest eligible original evaluation window. Endpoint containment can conceal a peak breach.''',r'''This Treasury-bill path returns within its reported historical limit at the endpoint, although an earlier position breaches that same limit.
The example follows the earliest eligible original evaluation window, illustrating why endpoint containment can conceal exposure during the review period.''')
change(r'''Conditional models can use recent position states and calendar information to
adapt a limit. Estimating those relationships also uses a finite history, while
a historical rule can be competitive without estimating many slopes. The
practical question is when the extra conditioning improves on an explicit
historical benchmark, rather than whether a complex model fits the past well.''',r'''Conditional models use recent position states and calendar information to adapt a limit, but their estimated relationships consume a finite history.
A historical rule estimates fewer relationships and can remain competitive, making improvement over an explicit historical benchmark the relevant practical question.''')
change(r'''We examine one market maker's FX record and two official dealer reporting
systems. New York Fed reports describe government-securities positions, while
CFTC categories describe aggregate dealer positions in futures markets. Their
economic units and information dates differ, so comparisons keep their own
targets, scales and historical references. Neither weekly system provides a
collection of independent individual dealers.''',r'''We examine one market maker's FX record alongside two official reporting systems that describe different segments of aggregate dealer activity.
New York Fed reports cover government securities, while CFTC categories cover futures markets, requiring distinct targets, scales and historical references.
Both weekly systems report dealer aggregates rather than independent individual dealers, and their economic units and information dates remain distinct.''')
change(r'''The central finding is conditional: history, the tested penalty menu and stated
limit costs organize the comparisons, but they do not establish a universally
sufficient history or a uniquely causal explanation. Matched FX gains coexist
with adverse weekly comparisons and with reversals at the longest tested
histories. Historical rules remain a demanding benchmark across these records.''',r'''History, the tested penalty menu and stated limit costs organize the comparisons, while a universal history requirement and causal explanation remain unidentified.
Matched FX gains coexist with adverse weekly comparisons and reversals at the longest tested histories, keeping historical rules a demanding benchmark.''')
change(r'''The first contribution is to connect the history-length evidence with an
additional reporting system. Earlier simulations support the registered
short-history and long-history loss-sign predictions, while their universal
simplification claim fails. FX learning curves give a similarly qualified
pattern. The new CFTC extension agrees with the short-history counts but misses
the registered long-history win target and the strict-improvement target.
The combined CFTC verdict is partial agreement, not validation of a universal
history threshold.''',r'''The first contribution connects simulation and FX history patterns with an additional reporting system, extending their comparison while retaining their limits.
Earlier simulations support the registered short-history and long-history loss-sign predictions, while their universal simplification claim fails and FX curves retain reversals.
The new CFTC extension agrees with the short-history counts but misses the registered long-history win target and strict-improvement target.
Its combined verdict is partial agreement, leaving the broader history pattern qualified and a universally sufficient history threshold still unestablished.''')
change(r'''The second contribution is to distinguish history from the available procedures.
An expanded penalty menu removes much of a short-history simulation loss, while
financial diagnostics retain both selection errors and losses within the finite
menu. Access to an ordinary historical quantile is part of that expanded menu,
so near-parity performance alone does not establish the value of extra
predictors. Related forecast comparisons leave historical methods alongside
many uneliminated alternatives.''',r'''The second contribution distinguishes the amount of history from the available procedures, separating candidate performance from the effects of their selection.
An expanded penalty menu removes much of a short-history simulation loss, while financial diagnostics retain selection errors and losses within the finite menu.
The expanded menu includes an ordinary historical quantile, leaving the value of extra predictors unidentified by near-parity performance alone.
Related forecast comparisons leave historical methods alongside many uneliminated alternatives, showing why a single reported winner gives an incomplete account.''')
change(r'''The third contribution is to connect forecast comparisons to stated limit
costs. Reserve amounts, breach frequency and exceedance magnitude enter
separately. Their weights can change which tested report is cheaper, and local
exceptions remain. These are hypothetical preferences rather than measured
funding gains or an evaluated trading intervention.''',r'''The third contribution connects forecast comparisons to stated limit costs, with reserve amounts, breach frequency and exceedance magnitude entering separately.
Their weights can change which tested report is cheaper, although local exceptions persist within the evaluated grid of hypothetical preferences.
The cost comparison illustrates this dependence on preferences, leaving realized funding gains and the effects of trading interventions outside its scope.''')
change(r'''Matching training-label histories and refit schedules makes the benchmark
explicit. It does not equalize every feature's raw history or every validation
calculation, and it does not isolate a causal feature effect. All observed
failures, unavailable comparisons and inspected-period qualifications remain
part of the evidence.''',r'''Matching training-label histories and refit schedules makes the benchmark explicit, while feature construction and validation can still use different information.
Causal feature effects therefore remain unidentified, and all observed failures, unavailable comparisons and inspected-period qualifications remain part of the evidence.''')
change(r'''Section~\ref{sec:target} defines the response, and Section~\ref{sec:results}
reports the forecasting comparisons. Section~\ref{sec:history-mechanism}
connects history, simulation and the CFTC extension. Section~\ref{sec:cost}
adds the stated cost preferences before the validation implications.''',r'''Section~\ref{sec:target} defines the response and Section~\ref{sec:results} reports the forecasting comparisons, separating matched conditional gains from changes in the reference procedure.
Section~\ref{sec:history-mechanism} connects the history evidence across simulations, FX and CFTC, before Section~\ref{sec:cost} relates these forecast comparisons to stated cost preferences.''')

change(r'''Path-risk forecasts address within-period extremes. MaxVaR studies the worst cumulative portfolio return under fixed holdings and diffusion assumptions \citep{boudoukh2004}. The payment-liquidity thesis forecasts conditional maximum deficits from confidential transactions \citep{hoogen2017}. Settlement studies examine tail liquidity needs and collateral requirements \citep{petrunia2019,arjani2020}. Duffie and colleagues study dealer capacity and Treasury-market functioning, including PnL quantile forecasts \citep{duffie2023}. These responses differ from the sampled absolute-position peak.''',r'''Path-risk forecasts address within-period extremes, including MaxVaR's worst cumulative portfolio return under fixed holdings and diffusion assumptions \citep{boudoukh2004}.
The payment-liquidity thesis forecasts conditional maximum deficits from confidential transactions, while settlement studies examine tail liquidity needs and collateral requirements \citep{hoogen2017,petrunia2019,arjani2020}.
Duffie and colleagues study dealer capacity and Treasury-market functioning, including PnL quantile forecasts; these responses differ from the sampled absolute-position peak \citep{duffie2023}.''')
change(r'''Consistent scores and elementary-score representations permit comparison across evaluation preferences \citep{gneiting2011,ehm2016}. The extended literature matrix contrasts the present peak response, completed labels and matched historical controls.''',r'''Consistent scores and elementary-score representations permit comparisons across evaluation preferences, rather than selecting a forecast solely from its apparent coverage \citep{gneiting2011,ehm2016}.
The extended literature matrix compares these earlier responses with the present sampled peak, its completed labels and matched historical controls.''')
change(r'''Expanded simulation menus remove large short-history losses, with parameter switching adding no observed median loss in that comparison.''',r'''Expanded simulation menus remove large short-history losses, while parameter switching misses its registered extra-loss criterion, leaving that switching effect unidentified.''')
change(r'''Paired tests support these forecast comparisons \citep{dm1995,gw2006,mcs2011}, while inventory-sensitive quoting motivates exposure monitoring \citep{avellaneda2008}.''',r'''Paired tests provide the statistical framework for these forecast comparisons, while inventory-sensitive quoting motivates the underlying problem of monitoring exposure \citep{dm1995,gw2006,mcs2011,avellaneda2008}.''')

change(r'''This aggregate statement supplies neither a per-horizon loss guarantee nor a coverage guarantee. The Supplement retains the original crossing diagnostic and the precise analytic qualifications.''',r'''The guarantee concerns aggregate pinball loss under those conditions; individual horizons, other weighting schemes and coverage retain their separate qualifications.
The Supplement preserves the original crossing diagnostic and precise analytic conditions, including the requirement for a common lower-inverse quantile convention.''')
change(r'''The weekly data are New York Fed Primary Dealer Statistics \citep{nyfeddata}. Reporting definitions follow the government-securities dealer framework and position-accounting instructions \citep{fr2004_2013,fr2004_2024}.''',r'''The weekly data are New York Fed Primary Dealer Statistics, whose reporting definitions follow the government-securities dealer framework and position-accounting instructions \citep{nyfeddata,fr2004_2013,fr2004_2024}.''')
change(r'''Daily aggregation takes the last recorded position on each nonempty source-naive calendar day. It retains partial boundary days, yielding 930 days and 501 common evaluation issues, with the completed day's end serving as the issue clock. The resulting target is a peak over subsequent daily records.''',r'''Daily aggregation takes the last recorded position on each nonempty source-naive calendar day, retaining partial boundary days in the observed series.
It yields 930 days and 501 common evaluation dates, with each completed day's end serving as the time of the forecast.
The resulting daily target is a peak over subsequent daily records, so aggregation changes both the measurement clock and the sampled response.''')
change(r'''The CFTC application retrospectively evaluates forecasts for a survivor universe using downloaded economic dates. It uses futures-only Dealer/Intermediary long positions minus short positions \citep{cftcTFF}.''',r'''The CFTC application retrospectively evaluates a survivor universe using downloaded economic dates and futures-only Dealer/Intermediary long positions minus short positions \citep{cftcTFF}.''')
change(r'''There are 877 weekly positions through 20 October 2026. Validation uses 52 origins; evaluation uses the last 260 eligible origins with horizon six. The evaluation position dates run from 21 September 2021 to 8 September 2026, with the final peak label completing on 20 October 2026. Refits occur every thirteen records with histories of 52 and 260, using downloaded economic dates; first-release vintages remain unobserved. The registered mechanism extension adds a 520-week history on the same evaluation dates, while retaining the two older histories unchanged. Positions usually refer to Tuesday and are released Friday, so the recorded position clock differs from the public information clock.''',r'''The retained CFTC series contains 877 weekly positions, with a common observation grid used to align forecasts across every selected contract.
Its final position date is 20 October 2026, which also completes the final sampled peak used in the evaluation.
Validation uses 52 forecast dates, while evaluation retains the last 260 eligible dates under the inherited chronological design and market universe.
The horizon spans six subsequent records, maintaining the same target across the older comparisons and the new mechanism extension.
The evaluation position grid begins on 21 September 2021, after the validation labels have completed under the stipulated information convention.
Its final forecast position date is 8 September 2026, leaving the required future records for completion of the peak label.
Refits occur every thirteen records, using downloaded economic dates and preserving the distinction between recorded positions and historical public availability.
The original training histories contain 52 and 260 records, while first-release vintages remain unobserved throughout these retrospective comparisons.
The registered extension adds a 520-week history on the same evaluation dates, retaining the older histories and their saved reports unchanged.
Positions usually refer to Tuesday and are released Friday, so the recorded position clock differs from the public information clock.''')
change(r'''Within each forecasting comparison, every method uses identical peak labels, current floors and issue origins.''',r'''Within each forecasting comparison, every method uses identical peak labels, current floors and forecast dates, keeping its reported target and comparison grid aligned.''')
change(r'''This finite-sample reporting convention supplies no coverage guarantee under the observed dependence.''',r'''Coverage under the observed dependence remains unguaranteed by this finite-sample reporting convention, even though its completed-label ranking is precisely defined.''')
change(r'''Historical first-release availability is not reconstructed. Translated paths reanchor historical signed paths, while historical-peak quantiles are projected to the observed floor.''',r'''Historical first-release availability remains unreconstructed, qualifying the information interpretation separately from the mathematical guarantee for a floor already known at issue time.
Translated paths reanchor historical signed paths before computing their peaks, while historical-peak quantiles are projected to the same observed floor.''')
change(r'''Full regression uses 33 predictors plus an unpenalized intercept, whereas its four-feature variant uses magnitude, signed level and two root mean square (RMS) increment measures. Standardization uses only training rows with completed labels.''',r'''Full regression uses 33 predictors plus an unpenalized intercept, allowing position states and calendar variables to enter the conditional report.
Its four-feature variant uses magnitude, signed level and paired short- and long-window root mean square (RMS) increment measures of recent changes.
Standardization uses only training rows with completed labels, keeping the feature transformation tied to the data available for that fit.''')
change(r'''Local quantiles use neighboring historical states, with an increment-scaled variant. Filtered paths simulate positions from GARCH-standardized empirical innovations drawn independently with replacement \citep{hull1998,barone1999}. Quantile forests use leaf distributions; tail methods fit volatility-scaled headroom \citep{meinshausen2006,mcneilfrey2000}.''',r'''Local quantiles use neighboring historical states, with an increment-scaled variant, while quantile forests use the training observations represented in their leaves \citep{meinshausen2006}.
Filtered paths simulate positions from GARCH-standardized empirical innovations drawn independently with replacement, and tail methods fit volatility-scaled headroom \citep{hull1998,barone1999,mcneilfrey2000}.''')
change(r'''A headroom CAViaR recursion and calibration wrappers follow existing methods \citep{engle2004,gibbs2021}. Calibration parameters update after outcomes mature. Fixed mean and median combinations use predefined members.''',r'''A headroom CAViaR recursion and calibration wrappers follow existing methods, with calibration parameters updating only after the corresponding outcomes mature \citep{engle2004,gibbs2021}.
Fixed mean and median combinations use predefined members, preserving their original composition separately from the rules that select a single procedure.''')
change('Same completed-label pools; fixed-window and rolling-window controls','Same completed training targets; fixed-window and rolling-window controls')
change(r'''Forecast definitions and executed menus. Codes occur here to connect with the result files. Matched histories and update schedules make the reference explicit.''',r'''Forecast definitions and executed menus retain the original procedure codes, connecting each reported comparison to its saved result files.
Matched training-label histories and update schedules make the reference explicit, while the Supplement preserves the full normalization and parameter conventions.''')
change(r'''Training histories count completed labels. Fixed-window models refit every 24 FX records or 13 weekly records.''',r'''Training histories count completed labels, and fixed-window models refit every 24 FX records or 13 weekly records under their original schedules.''')
change(r'''The range statistic uses 1,000 stationary-bootstrap replications in arch 8.0.0, with block length $\max\{H,\lceil n^{1/3}\rceil\}$.''',r'''The range statistic uses 1,000 stationary-bootstrap replications, retaining the original implementation and its approximation to dependence among the paired losses.
Its recorded software version is arch 8.0.0, with the precise implementation retained alongside the saved comparison results and execution records.
The block length is $\max\{H,\lceil n^{1/3}\rceil\}$, preserving the inherited dependence convention rather than selecting a new setting after observing these comparisons.''')
change(r'''The nominal level presumes suitable loss dependence; it does not account for earlier research-stage model development.''',r'''The nominal level presumes suitable loss dependence and leaves earlier research-stage model development outside the stated uncertainty calculation for each comparison.''')
change(r'''Several methods can produce identical losses, so one surviving loss pattern need not mean that only one method survives. The fractions summarize related tasks, with no independent cross-market pooled test.''',r'''Several methods can produce identical losses, allowing a surviving loss pattern to represent multiple distinct procedures whose labels remain explicitly listed.
The reported fractions summarize related tasks descriptively, with independent cross-market significance outside the scope of the fixed bootstrap exercise.''')

for old,new in [('RQ1: matched accuracy and reference stability','Matched FX gains depend on the reference'),('History gains depend on the tested range','FX history gains reverse within the tested range'),('RQ2: daily, weekly and independently reported positions','Historical rules remain competitive across reporting clocks'),('CFTC: independent reporting-system evidence','CFTC repeats the benchmark pattern across markets'),('Model confidence sets','Historical methods remain in most joint comparison sets'),('Why does regression lose at low frequency?','Weekly losses reflect both the menu and its selection'),('A descriptive coordinate organizes the simulation evidence','A descriptive ratio organizes the simulation evidence'),('RQ3: limit-cost regions','Limit-cost rankings depend on the stated charges')]:
    change('{'+old+'}','{'+new+'}')

change(r'''This distinction makes the reference procedure part of the substantive finding, since a conditioning gain alone does not determine the overall ranking.''',r'''The reference procedure is therefore part of the substantive finding, with a matched conditioning gain leaving the ranking against other historical rules unresolved.''')
change(r'''This adverse case shows why the matched long-history gain cannot be generalized across horizons and training-window lengths.''',r'''This adverse case confines the interpretation of the matched long-history gain to its evaluated horizon and training-window setting, retaining the broader failures.''')
change(r'''Long-history short-horizon FX regression under two references and periods. Negative percentages favor regression. Matched gains recur while the rolling-reference direction changes.''',r'''Long-history short-horizon FX regression is compared under two references across the earlier and later evaluation periods retained in the study.
Negative percentages favor regression, revealing recurring matched gains alongside a reversal in its comparison with the shorter rolling historical reference.''')
change(r'''Regression uses history 2880 and horizon 6; the original rolling reference uses 720. The earlier matched comparison is the original three-penalty regression, not the later one-standard-error selection rule. The wrapper comparison is a separate finite projected delayed ACI-style exercise.''',r'''Regression uses history 2880 and horizon 6, retaining the original comparison grid for each period reported in this table.
The original rolling reference uses 720 observations, making its available history shorter than the matched historical headroom reference used alongside regression.
The earlier matched comparison uses the original three-penalty regression, while the later one-standard-error rule remains a separate selection exercise.
The wrapper comparison is a separate finite projected delayed ACI-style exercise, using its common evaluation dates and inherited calibration design.''')
change(r'''History sensitivity within the original FX record is not monotone. The full regression improves over part of the grid and gives back some gain at the longest history.''',r'''History sensitivity within the original FX record reverses across the tested grid, as full regression gives back gains at the longest history.''')
change(r'''Neither simpler conditioning nor fixed combinations establish a uniform weekly improvement, reinforcing the need to retain the historical benchmark in each comparison.''',r'''Simpler conditioning and fixed combinations retain adverse weekly comparisons, reinforcing the importance of an explicit historical benchmark for each forecast setting.''')
change(r'''Returning to the same FX record, historical headroom wins seven of eight daily comparisons; the exception uses four predictors, history 260 and horizon 6, reducing loss by 3.0\%. It records 37 breaches versus 30 for matched headroom. Daily aggregation therefore preserves the score--breach disagreement while changing the leading forecast in most comparisons.''',r'''Returning to the same FX record, historical headroom wins seven of eight daily comparisons, retaining a demanding reference after changing the measurement clock.
The exception uses four predictors, with its complete specification and matched historical comparison retained alongside the adverse cases in the Supplement.
Its training history is 260 and its horizon is 6, maintaining common completed targets and forecast dates across the matched procedures.
The regression loss falls by 3.0\%, although this accuracy gain accompanies a worse breach count than the matched historical report.
Regression records 37 breaches versus 30 for headroom, preserving the score--breach disagreement while aggregation changes the leading method in most comparisons.''')
change(r'''Weekly evidence across the original main comparison, added panel and earlier-period comparisons. Counts refer to related tasks rather than independent dealers. Stronger regularization narrows losses while leaving substantial failures.''',r'''Weekly evidence combines the original main comparison, added panel and earlier-period comparisons, with counts referring to related tasks rather than independent dealers.
Stronger regularization narrows the losses of conditional procedures while leaving substantial failures, including the adverse bill comparison under conservative selection.''')
change(r'''The original bill main comparison has 54 versus 28 strict breaches among 277 issues.''',r'''The original bill main comparison has 54 versus 28 strict breaches, favoring the historical report alongside its lower mean loss.
Its evaluation contains 277 forecast dates, with the complete paired results retained under the original chronological design and target definition.''')
change(r'''Non-elimination does not establish equal predictive risk. Table~\ref{tab:v10-mcs-main} reports surviving methods, with identical observed-loss patterns explained separately in Supplement Section S11. Supplement Section S11 retains every set, method p-value, equivalence class and prior unavailable method.''',r'''Surviving procedures remain statistically unseparated under the specified comparison, while equality of their predictive risks remains a stronger, unestablished proposition.
Table~\ref{tab:v10-mcs-main} reports surviving methods, and Supplement Section S11 retains every set, method p-value, identical-loss class and prior unavailable method.''')
change(r'''For full regression, the finite-menu gap is positive in 29 of 41 short-history weekly cells; selection exceeds half of positive actual excess in 27. Both criteria hold, so benchmark advantages and selection losses coexist within this menu. Separate component medians need not add: actual excess is 19.44\%, selection 18.32\%, and the diagnostic gap 4.37\%.''',r'''For full regression, the finite-menu gap is positive in 29 of 41 short-history weekly cells, retaining a disadvantage even after retrospective selection.
Selection exceeds half of positive actual excess in 27 cells, so benchmark advantages and selection losses coexist within this finite menu.
The median actual excess is 19.44\%, while the median selection component is 18.32\%, with each statistic summarizing its own component distribution.
The median diagnostic gap is 4.37\%; separate component medians generally differ from the median of their sum across the same comparisons.''')
change(r'''This retrospective finite oracle is diagnostic, cannot guide deployment, and cannot rule out information in other conditional models.''',r'''Choosing the best candidate after evaluation makes this a retrospective diagnostic, leaving deployment performance and information in other conditional models unresolved.''')
change(r'''Extending validation from 52 to 156 weeks keeps the CFTC evaluation period, training histories, and refitting clock fixed. Median excess falls from 19.33\% to 4.03\% with 52-week training histories, and from 10.35\% to 0.53\% with 260-week histories. Infinite-penalty selections rise from 4 to 10 of 17 contracts, and from 4 to 5 of 17, respectively. These differences between across-contract medians need not match typical paired improvements and do not identify a causal effect. Four-feature failures remain unavailable in the complete inventory (Supplement Section S15).''',r'''Extending validation from 52 to 156 weeks keeps the CFTC evaluation period, training histories and refitting clock fixed in the saved sensitivity exercise.
Consider first the 52-week training history, which retains its own historical reference and forecast dates when the validation period is extended.
Its median excess falls from 19.33\% to 4.03\%, showing a narrower loss disadvantage under the longer validation period in this comparison.
For the 260-week training history, the same exercise again holds the evaluated targets, historical benchmark and refitting schedule fixed.
Its median excess falls from 10.35\% to 0.53\%, while the complete results retain the variation among contracts around these separate medians.
Infinite-penalty selections rise from 4 to 10 contracts under the shorter training history, favoring the ordinary empirical quantile more often.
Under the longer training history, these selections rise from 4 to 5 contracts, again retaining the full market universe in the denominator.
Each comparison covers 17 contracts; differences between their separate medians leave typical paired improvements and a causal interpretation unresolved.
Four-feature failures remain unavailable in the complete inventory, preserving the distinction between a successful subset and its planned comparison (Supplement Section S15).''')
change(r'''At 99\%, historical headroom wins 28 of 34 CFTC comparisons; one failure leaves the 29-win threshold unresolved. Both FX periods remain unavailable at 99\%, leaving the combined improvement criterion undetermined. Unavailable planned comparisons are retained, and successful subsets never replace a missing full-group median.''',r'''Consider the 99\% target separately, retaining the originally planned comparisons and the numerical failure recorded under that quantile sensitivity design.
Historical headroom wins 28 of 34 CFTC comparisons, while the remaining numerical failure prevents classification of the complete planned group.
The registered threshold requires 29 wins, leaving its verdict unresolved until the failed comparison can be determined under an authorized analysis.
Both FX periods remain unavailable at 99\%, leaving the combined improvement criterion undetermined and their failed planned comparisons explicitly retained.
Successful subsets remain distinct from a missing full-group median, preserving the original uncertainty instead of replacing it with a favorable partial summary.''')
change(r'''A separate 24-step FX comparison against rolling translated paths reverses near 20.6:1. Both six-step FX comparisons reduce mean underprediction and mean overprediction, so the weight reversal belongs specifically to the 24-step reference.''',r'''A separate 24-step FX comparison against rolling translated paths changes ranking as the relative penalty on underprediction rises across the evaluated preferences.
Its reversal occurs near 20.6:1, reflecting the weighting of underprediction against overprediction in that particular comparison of the saved reports.
Both six-step FX comparisons reduce mean underprediction and mean overprediction, confining this weight reversal to the longer-horizon translated-path reference.''')

change(r'''The earlier discovery study selected the ratio
\[
c=\frac{W}{H+1}
\]
as a descriptive coordinate on its fixed simulation grid. This ratio excludes
the number of coefficients. It is neither a dependence-adjusted effective
sample size nor an identified normalization by model complexity.''',r'''The earlier discovery study selected the following ratio as a descriptive coordinate on its fixed simulation grid, leaving model complexity outside its definition:
\[
c=\frac{W}{H+1}.
\]
It excludes the number of coefficients, so an interpretation as dependence-adjusted information or an identified complexity normalization remains unsupported by this design.''')
change(r'''The discovery first crossing is approximately $106.5$ for full regression.
For four-predictor regression it is approximately $27.3$. The full-regression
fixed-grid interval runs from $27.89$ to $110.71$. The sparse-regression interval
runs from $13.27$ to $107.11$. These ranges condition on the selected coordinate
and simulation grid, omitting uncertainty from choosing that coordinate.
The sparse curve crosses downward more than once, so its first crossing cannot
be a permanently sufficient history bound.''',r'''The discovery first crossing is approximately $106.5$ for full regression, locating the initial change in sign on the selected simulation coordinate.
For the sparse regression it is approximately $27.3$, with the underlying curve retaining further changes in direction across the tested grid.
The full-regression fixed-grid interval runs from $27.89$ to $110.71$, summarizing the original resampling uncertainty conditional on the selected coordinate.
The sparse-regression interval runs from $13.27$ to $107.11$, under the same restriction to the selected coordinate and simulation grid.
Uncertainty from choosing that coordinate remains outside these ranges, and repeated downward crossings invalidate a permanently sufficient history interpretation.''')
change(r'''The subsequent registered simulation checks meet the short-history prediction
in $47$ of $48$ cells. The long-history prediction holds in $21$ of $24$ cells.
Those are finite-grid descriptive successes under the declared laws and menus,
rather than independent-cell significance tests. The simpler procedure satisfies
the universal-ordering inequality in $42$ of $48$ cells. All six counterexamples
remain, so the universal simplification claim is not supported.''',r'''The subsequent registered simulation checks meet the short-history prediction in $47$ of $48$ cells under the declared simulation laws and menus.
The long-history prediction holds in $21$ of $24$ cells, retaining the exceptions and the original fixed denominators in its descriptive count.
These are finite-grid descriptive successes rather than independent-cell significance tests, because the experiments share their designed laws and comparison structure.
The simpler procedure satisfies the universal-ordering inequality in $42$ of $48$ cells, falling short of the all-cell requirement for that claim.
All six counterexamples remain in the evidence, so the universal simplification claim fails despite its inequality holding across most tested cells.''')
change(r'''Their agreement does not identify a horizon-invariant financial threshold.''',r'''Their agreement leaves a horizon-invariant financial threshold unidentified, since the transported simulation summary and the individual financial curve represent different objects.''')
change(r'''They establish neither another dealer replication nor an untouched financial holdout.''',r'''Their reuse supports a within-record history comparison, leaving replication across individual dealers and validation on an untouched financial holdout unresolved.''')
change(r'''Shading summarizes the original simulation crossings conditional on the chosen grid and coordinate, without accounting for coordinate selection. History alone does not guarantee a gain.''',r'''Shading summarizes the original simulation crossings conditional on the chosen grid and coordinate, with uncertainty from selecting that coordinate omitted.
History alone leaves gains unguaranteed, as the complete curves retain adverse comparisons, left censoring and reversals at the longest histories.''')
change(r'''The CFTC extension fixes the earlier thresholds before adding a training
history of $520$ weeks. Both shorter-history predictions reuse their unchanged
saved reports. The universe, validation period, evaluation dates, candidate
menus and refit schedule remain the inherited design. Completed training labels
end no later than each refit, and every validation label finishes before the
evaluation begins. Downloaded economic-date vintages remain distinct from
historically available first releases.''',r'''The CFTC extension fixes the earlier thresholds before adding a training history of $520$ weeks, while reusing the unchanged shorter-history reports.
The universe, validation period, evaluation dates, candidate menus and refit schedule remain inherited, confining the new computation to the registered extension.
Training labels have completed by each refit and every validation label finishes before evaluation, under the stipulated downloaded economic-date information convention.
Historical first-release information remains distinct and unreconstructed, preserving the difference between a valid completed-label schedule and actual public availability.''')
change(r'''For the full procedure, the low-history region contains $34$ planned
market-history comparisons. It loses to matched historical headroom in $29$.
The sparse procedure loses in $15$ of $17$ low-history comparisons. Both meet
their registered eighty-percent targets. The sparse procedure wins in $10$ of
$17$ long-history markets. That fraction misses its registered sixty-percent
target. Only $6$ of $17$ sparse-regression curves improve strictly at both steps
of the history grid, missing the secondary seventy-percent target.''',r'''For the full procedure, the low-history region contains $34$ planned market-history comparisons, all retained under the registered classification and denominator.
It loses to matched historical headroom in $29$ comparisons, meeting the registered disadvantage criterion within this low-history region of the grid.
The sparse procedure loses in $15$ of $17$ low-history comparisons, retaining the same fixed historical reference in each paired comparison.
Both meet their registered eighty-percent targets, supporting the short-history sign pattern under these particular menus and transported simulation thresholds.
The sparse procedure wins in $10$ of $17$ long-history markets, leaving a substantial set of adverse contracts in the same region.
That fraction misses its registered sixty-percent target, making the primary verdict partial agreement despite the successful short-history disadvantage counts.
Only $6$ of $17$ sparse-regression curves improve strictly at both steps of the history grid, retaining every reversal or tie.
This misses the secondary seventy-percent target, which remains separate from the primary verdict and preserves the failure of strict improvement.''')
change(r'''P3 is secondary and cannot upgrade that verdict. Ties count as neither wins nor
losses. Unknowns retain planned denominators; none occurs in this run.''',r'''P3 is secondary and leaves that verdict unchanged; ties enter a separate category outside both the win and loss counts.
Unknowns retain planned denominators under the registered classification bounds, although all planned reports complete in this particular run.''')
change(r'''No market, failed criterion or unfavorable curve was removed to obtain
the primary verdict.''',r'''The primary verdict retains every market, failed criterion and unfavorable curve, with the full denominators fixed by the registered design.''')

change(r'''For CFTC full regression, higher reserve coefficients and lower fixed-breach coefficients generally favor the expanded-menu procedure over matched historical headroom, although the grid is not monotone (Figure~\ref{fig:decision}).
At $c=1$, regression is strictly cheaper in $5/34$ comparisons at the center of the sorted grid $(\kappa,\beta)=(.1,.25)$, $32/34$ at $(1,0)$, and $1/34$ at the opposite corner $(.01,5)$.
These are illustrative costs, not observed operating costs; Supplement Section S12 gives the normalization, fixed grid and complete-method results.''',r'''For CFTC full regression, higher reserve coefficients and lower fixed-breach coefficients generally favor the expanded-menu procedure, although the fixed grid retains local reversals (Figure~\ref{fig:decision}).
The exceedance-magnitude coefficient is fixed at $c=1$, separating this charge from the reserve and breach-event preferences varied across the grid.
At the center of the sorted grid, the reserve and breach-event coefficients are $(\kappa,\beta)=(.1,.25)$ under the stated normalization.
Regression is strictly cheaper in $5/34$ comparisons there, retaining the same matched historical report and the original histories for each contract.
At the reserve-heavy corner the coefficients are $(1,0)$, so reserve amounts and exceedance magnitude entirely determine these illustrative costs.
Regression is cheaper in $32/34$ comparisons there, illustrating how a different balance of stated costs can change the preferred report.
At the opposite corner the coefficients are $(.01,5)$, placing greater weight on breach events relative to the reported reserve amount.
Regression is cheaper in $1/34$ comparisons there, with the complete grid retaining the intervening outcomes and any local exceptions.
These costs express hypothetical preferences rather than observed operating expenses, and Supplement Section S12 retains their normalization and complete-method results.''')
change(r'''\textbf{Use historical headroom by default when validation evidence is short.}''',r'''\textbf{Retain historical headroom as a demanding validation benchmark.}''')
change(r'''Historical reports also survive in most CFTC model confidence sets, supporting their retention until a conditional procedure has sufficient validation evidence.''',r'''Historical reports also survive in most CFTC model confidence sets, supporting their retention as benchmarks while a conditional procedure undergoes application-specific validation.''')
change(r'''The earlier-period comparison and full-prefix backcast are retrospective, with no previously unseen prospective financial evaluation.''',r'''The earlier-period comparison and full-prefix backcast are retrospective, leaving a previously unseen prospective financial evaluation outside the completed evidence.''')
change(r'''Weekly reports aggregate positions across dealers; related categories and the CFTC survivor universe do not provide independent dealer replications.''',r'''Weekly reports aggregate positions across dealers, making related categories and the CFTC survivor universe comparisons of reporting aggregates rather than independent dealer replications.''')
change(r'''The comparisons identify neither causal effects nor individual-feature effects, and fitted limits receive no coverage guarantee under this dependence.''',r'''Causal effects, individual-feature effects and coverage guarantees remain unidentified by these dependent forecast comparisons, even when completed training-label histories match.''')
change(r'''Costs illustrate fixed preferences; trading returns, funding gains and institutional intervention costs are not measured.''',r'''Costs illustrate fixed preferences under the recorded position paths, leaving trading returns, funding gains and institutional intervention costs unmeasured by these experiments.''')
change(r'''The finite-penalty hindsight bound is diagnostic only; validation-length and quantile-sensitivity checks are post-result analyses with numerical failures retained.''',r'''Choosing the best finite candidate after evaluation is diagnostic only; validation-length and quantile-sensitivity checks are post-result analyses with numerical failures retained.''')
change(r'''The original evaluation period was inspected,
and related reporting categories do not provide independent dealer replications.''',r'''The original evaluation period was inspected, and related reporting categories remain aggregate comparisons with individual-dealer replication outside their scope.''')
change(r'''Longer history therefore cannot
serve as an automatic deployment rule.''',r'''An automatic deployment rule based only on longer history therefore remains unsupported by these completed comparisons and their retained exceptions.''')
change(r'''Access to a historical
candidate helps explain why menu expansion alone does not identify predictor
value.''',r'''Access to a historical candidate leaves predictor value unidentified by menu expansion alone, since near-parity can result from selecting that historical option.''')
p.write_text(text)
print('WP5 prose edits applied; saved results/protocols untouched')
