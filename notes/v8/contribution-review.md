# B3 contribution review and numeric bindings

Scope: authoring support only. Only CONTRIBUTIONS.md and this review are written. No source archive, existing note, manuscript, builder, Git state, real-data experiment or simulated result is changed. Numbers below were checked by exact CSV selector/JSON pointer or exact existing README passage against notes/v7/evidence-parts; only display rounding is applied.

## Findings and existing evidence

|Finding|Display|v7 numeric ID|Native value|Source and selector|
|---|---|---|---|---|
|First|14.8% decrease|`FX_LATE_MATCHED_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT`|-14.766762552613885|`results/revision-20261022/paired-comparisons.csv`; {"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=relative_mean_loss_difference_percent|
|First|16.6% decrease|`FX_EARLY_MATCHED_H6_RATIO_CHANGE_PERCENT`|-16.62356533682211|`results/supervisor-20261023/r6-writing-hac-20261023/results.json`; /comparisons/0/ratio_change_percent|
|First|15.0% decrease|`FX_ACI_H6_W2880_QR_MINUS_F_LOSS_PERCENT`|-14.99691078803782|`results/revision-20261023/v6/wp2-findings.json`; /wrapped_pairs/1/qr_minus_f_loss_percent|
|First|329|`FX_ACI_H6_W2880_QR_HITS`|329|`results/revision-20261023/v6/wp2-findings.json`; /wrapped_pairs/1/qr_hits|
|First|328|`FX_ACI_H6_W2880_F_HITS`|328|`results/revision-20261023/v6/wp2-findings.json`; /wrapped_pairs/1/f_hits|
|First|12.7% decrease, distinct rolling reference|`FX_LATE_PRIMARY_H6_RELATIVE_MEAN_LOSS_DIFFERENCE_PERCENT`|-12.660126412969763|`results/revision-20261022/paired-comparisons.csv`; {"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}; field=relative_mean_loss_difference_percent|
|First|3.2% increase, distinct rolling reference|`FX_EARLY_PRIMARY_H6_RATIO_CHANGE_PERCENT`|3.1681985293173343|`results/supervisor-20261023/r6-writing-hac-20261023/results.json`; /comparisons/1/ratio_change_percent|
|Second|50.8% increase|`PANEL_BILL_QR_H6_W260_LOSS_PERCENT`|50.78571256749063|`results/revision-20261022/paired-comparisons.csv`; {"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=relative_mean_loss_difference_percent|
|Second|34 losses|`PANEL_E5_QR33_EXPANDED_LOSSES`|34|`results/supervisor-20261023/e5/descriptive-summary.json`; /QR33_plus/losing_to_F|
|Second|48 planned cells|`PANEL_E5_PLANNED`|48|`results/supervisor-20261023/e5/descriptive-summary.json`; /planned_cells|
|Second|181.4% worst excess|`PANEL_R6_R2_RETRO_WORST`|181.39452368014167|`results/supervisor-20261023/r6/assessment.json`; /S1/worst_percent_vs_F|
|Third|376|`FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_LEFT`|376|`results/revision-20261022/paired-comparisons.csv`; {"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_left|
|Third|360|`FX_LATE_MATCHED_H6_STRICT_BREACH_COUNT_RIGHT`|360|`results/revision-20261022/paired-comparisons.csv`; {"contrast_id": "fx_hourly-h6-QR2880-minus-frozen_F2880"}; field=strict_breach_count_right|
|Third|CROSSING, original FX rolling F720 reference|`FX_MURPHY_H6_RANKING`|CROSSING|`results/supervisor-20261023/inference/murphy-verified.csv`; {"contrast_id": "fx_hourly-h6-QR2880-minus-rolling_F720"}; field=ranking|
|Third|CROSSING, original Treasury F260 reference|`PANEL_BILL_PRIMARY_MURPHY`|CROSSING|`results/supervisor-20261023/inference/murphy-verified.csv`; {"contrast_id": "nyfed_weekly-h6-QR260-minus-frozen_F260"}; field=ranking|
|Optional appendix only|20.6:1, H24 rolling S720 reference|`FX_PREFERENCE_H24_REVERSAL_RATIO`|20.6308977263|`results/revision-20261022/preference-robustness/README.md`; existing exact text passage|

All 16 selected numeric/status IDs matched the original saved source. No percentage, median, win count, p-value or forecast was recalculated. The 34/48, 181.4% and 20.6 fields retain their distinct source-native scopes.

## Closest-literature audit: existing v7 evidence only

|Prior work|Verified scope from existing reading evidence|Useful distinction for this paper|Forbidden inference|
|---|---|---|---|
|Wisniewski et al. (2020); Wisniewski (2024), Chapter 6|Signed next-hour endpoint intervals; one hourly FX dealer/source family; ordered endpoint training/calibration/test; pinball and coverage tests. Existing literature-a evidence locates W20 §§2–3.5 and W24 §§6.2–6.3.5/6.4.3.|This paper compares completed multi-record absolute peak reports and explicit historical controls; the empirical contribution is the saved comparative finding.|Do not call ordered evaluation, score-plus-coverage reporting, known current information, or endpoint model classes novel; shared family does not establish byte-identical input data.|
|Boudoukh et al. (2004), MaxVaR|Worst cumulative portfolio return under a fixed portfolio and diffusion assumptions; initial portfolio value and endpoint-to-path conversion already appear. Existing literature-a records full six-page journal-layout body.|Different path-risk response and empirical comparison task.|Do not claim to introduce path-risk maxima or known initial information. Current-position floor details not reported in consulted passages remain —, not absent from all literature.|
|van den Hoogen (2017)|Historical selected-original receipt supports a payment-deficit peak/EVT precursor. Existing v5/v7 notes explicitly say no fresh complete-body reading succeeded.|Retain a narrative precursor only.|Exact issue-time floor: —; completed multi-record label maturity: —; detailed validation comparator: —; cross-source transfer: —. Do not fill these from inference or treat missing verification as absence.|
|Ehm et al. (2016)|Consistent quantile/expectile scores and elementary-score/Murphy comparisons are established tools. Existing literature-b records partial reading of the 2015 author-v2 body, §§3.2–3.4, 4, 5, with published 2016 metadata kept separate.|The contribution is the observed comparison-specific score/breach/preference disagreement for these peak forecasts.|No new scoring representation, Murphy method or general joint-evaluation principle is claimed.|

Literature provenance: `notes/revision-v5-novelty/literature-a.json`/`.md`, `literature-b.json`/`.md`, `positioning-source.json`, and `notes/v7/references-verified.json`. This B3 audit reopens those existing records; it does not claim a new full-body reading or a fresh web search. No speculative “first”, “unique” or “unprecedented” priority claim is needed.

## Reference separation required in all five manuscript locations

- First finding: later matched QR2880 versus frozen F2880, not original rolling F720; early matched gain is original-three-menu QR, not R2. Both QR and F are wrapped in the 15.0% /329/328 comparison. A finite delayed wrapper result is an observed comparison, not a coverage guarantee.
- Second finding: 50.8% belongs to original bill H6/W260/d13; 34/48 belongs to the additional 12-series expanded-menu panel; 181.4% is the worst earlier W52 R2 weekly excess, not a panel median or a universal bound. Say “no protection was observed in this exercise”, not “one-SE can never protect”.
- Third finding: 376/360 is matched unwrapped H6. Figure 2 elementary curves belong to the original FX QR2880 versus rolling F720 contrast (whose breaches are376/332); Figure 3 is original Treasury QR260 versus frozen F260. Crossing these original curves does not assert a Murphy crossing for the matched 376/360 pair.
- Optional 20.6:1 belongs only to the H24 FX comparison against rolling translated-path S720; it is a score-weight reversal, not an observed economic cost ratio and not an H6 threshold. It is omitted from the short contribution sentences to keep the main claim focused.
- Section 3 definitions, floor projection and strict-tail property are elementary; Lévy is classical. They are background, not one of the three contributions. Use the supplied Section 3 sentence without C1/C2/C3 labels.
- The new simulation is retained in Section 7/Supplement as a bounded mechanism exercise. Saved `results/v8/mc/predictions.json` says P1/P3 NOT_SUPPORTED and P2/P4 UNASSESSABLE; saved summary has seven FAILED D1 cells. Do not relabel that result as a confirmed empirical mechanism or a successful third contribution.

## Root integration checklist

|Location owned by root|Required final alignment|Audit state here|
|---|---|---|
|Abstract|FX repeated matched gain; weekly adverse result; score/breach qualification; MC status honestly stated or omitted from novelty claim|Draft support supplied; root final readback pending|
|Introduction contribution paragraph|At most three First/Second/Third findings, each numerical and located by table/figure|Draft support supplied; root final readback pending|
|End of Section 2|Closest prior endpoints/path-risk/scoring tools acknowledged; elementary properties positioned as background|Draft support supplied; root final readback pending|
|Conclusion|Same three empirical findings, no added general causal/coverage/trading-value promise|Draft support supplied; root final readback pending|
|Cover letter|Same empirical contribution; forecast evaluation, demanding benchmarks and practical validation explain journal fit|Draft support supplied; root final readback pending|

No manuscript integration is claimed by this delegated audit. Author/ORCID/funding/conflict/AI placeholders remain owned by the existing submission sources and untouched.

## B3 first source readback of root's five locations

Read `notes/v8/b3-prose.json`, current `submission-jof/manuscript.tex` and `submission-jof/cover-letter.md` after root's initial rewrite. This supersedes the earlier draft-pending state for that source snapshot; no main-source edit is performed here.

|Location|Readback|Residual action for root|
|---|---|---|
|Abstract|Same three empirical themes; later wrapper correctly identified; no methodological/fourth contribution;132 words/9 numeric occurrences reported by root|Original writing brief allows<=170 words and<=10 numbers, so9 is within that rule. The v7 metric's older5-number target does not apply.|
|Introduction contributions|First/Second/Third, numerical findings with table/figure locations; theory properties become roadmap/background; correct later/earlier matched numbers and distinct original Murphy comparisons|The First heading is read with its following sentences; only the later-period wrapper was evaluated. Avoid shortening it to a claim of two wrapped periods.|
|End Section2|Same three themes and explicit statement that methods are standard|Change “gains ... recur across periods and survive calibration” to “gains ... recur across periods; the later gain survives calibration”. Change “...matched376/360..., and elementary-score rankings cross” to explicitly name the two original comparisons for the curves.|
|Conclusion|Restates FX/weekly/score-breach findings; the final simulation sentence is negative qualification, not a fourth contribution|For B4, move detailed mechanism uncertainty/failed-grid discussion to Limitations if centralizing limitations; keep a brief observed-record scope sentence at the end. Current negative sentence need not be removed to preserve honesty.|
|Cover letter|Empirical finding first; forecast evaluation/simple benchmarks/practical limit choice explain JoF fit; three findings stay aligned and target properties are explicitly supporting background|No contribution contradiction found; preserve author placeholders and later-period wrapper scope.|

The only substantive disambiguations identified are the two Section2 phrases above. No speculative novelty or fourth contribution was found. The current Conclusion's simulation caveat does not claim a discovered mechanism: it says the hourly mechanism is unresolved and weekly losses were not reproduced. B4's later concentration of limitations should not change that result.

## B3 draft alignment closed after root disambiguation

All five locations are **已读草稿，对齐** for the root's current B3 source/JSON snapshot. Readback confirms the end of Section2 now limits calibration survival to the later gain and attributes crossing curves explicitly to the two original comparisons; the Introduction First heading also specifies the later gain. Abstract, Section2 and Conclusion are present in the current manuscript, and the cover letter matches b3-prose.json. No contribution contradiction or fourth contribution remains in this draft.

CONTRIBUTIONS.md's single English First sentence now also says “calibration retains the later-period15.0% gain”. Its existing untracked contents were copied to CONTRIBUTIONS.md.bak before replacement. B4 still owns moving the longer Conclusion simulation qualification to Limitations; this pending editorial relocation does not change the three contribution findings. No main source, generated prose, JSON, Git state or scientific archive was edited by this review.
