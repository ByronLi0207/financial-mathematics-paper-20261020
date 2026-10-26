# WP6 econometric review: exactly seven substantive issues

Review basis: WP5 end commit `d44364c6aa5ca5a9a043f33b9173f0864b771159`, current main, compact Supplement, extended technical text, accepted WP1–WP3 readouts and their frozen protocols. This is a same-model internal critique, not external or cross-model review. Only existing public source text and saved outputs were read; no model, test, financial array, calculation or new literature search was run. Severity concerns the strength of scientific interpretation, not an allegation that the saved arithmetic is wrong. Line locations below refer to this snapshot.

## 1. Post hoc coordinate selection remains discovery, and the tie does not establish a unique organizing statistic

**Severity: major remaining design limitation; transparency substantially resolved.**

**Exact locations.** `submission-jof/manuscript.tex:188–190,305,362–364`; `submission-jof/supplement.tex:1362`; `protocol/revision-v9/wp1-posthoc-design.json:7–9,66–76,146–160,178–191`; `submission-jof/generated/v9-evidence-tables.tex:12–17`; `notes/revision-v9/wp1-acceptance.json:56`.

**Current evidence.** The source results were already known. Candidate metrics were compared by training-set classification accuracy on the same discovery cells; the chosen coordinate ties the parameter-adjusted candidate on that criterion and is selected by the written tie order. The rank correlations do not uniquely favor the chosen coordinate. Its bootstrap fixes the selected coordinate and grid, excluding metric-selection uncertainty and earlier research choices. The complete candidate table, conditional-bootstrap wording and `POST_HOC_NOT_CONFIRMATION` label correctly disclose those facts; they resolve a hidden-search allegation. They do not convert the selection score into held-out evidence or show that the selected coordinate dominates alternatives outside this finite design.

**Bounded response.** Retain the full candidate table and call the index an organizing coordinate selected by the stated descriptive rule. Keep “post hoc” attached when the coordinate first enters a result or standalone caption. Do not interpret its accuracy as prediction accuracy, its envelope as selection-adjusted confidence, or a tie-selected index as the uniquely supported explanation. No new selection method, resampling analysis or alternative winner is requested. **Remaining gap:** independent comparison of the candidate coordinates is absent and must stay absent from the claim.

## 2. Innovation-law robustness does not separate estimation cost from DGP, menu, reference and failure-policy effects

**Severity: major remaining identification limitation.**

**Exact locations.** `submission-jof/manuscript.tex:144–150,305–307,362`; `submission-jof/supplement.tex:1364–1372`; `submission-jof/extended-v9-technical.tex:187–207`; `protocol/revision-v9/wp2-confirmatory.md:7–19,25–27`; `protocol/revision-v9/wp3-learning-curve.md:13–17`.

**Current evidence.** WP2 changes innovation laws and streams, but all new processes retain the same mean-reverting level form, the same compact persistence grid and the inherited validation/evaluation clock. The richer and smaller regressions retain different penalty menus, exact-tie conventions and candidate-eligibility contracts. The historical rule has its own empirical-quantile estimation error, and WP3 changes that rule's history together with the regression's history. The selected coordinate omits parameter count. Current prose correctly says “implemented procedures,” rejects an oracle-risk decomposition, and acknowledges approximation and regularization confounding. Thus the execution is a legitimate fixed-procedure stress comparison; it is not a controlled estimate of a per-parameter estimation-cost channel.

**Bounded response.** Describe WP2 as robustness across innovation laws **within the specified level-process family**. At `manuscript.tex:305`, “test against new procedures and data conditions” is potentially misleading because WP2 deliberately retains the old forecasting procedures; prefer “test under changed innovation laws and additional history lengths.” Keep the explicit no-channel-identification qualification near the positive synthesis, rather than implying that changing heavy tails, switching and jumps has isolated the mechanism. **Remaining gap:** an oracle or an orthogonal conditioning/regularization/failure-policy design is unavailable; do not invent one or infer its answer.

## 3. Passing the fixed pooled loss-sign screens is narrower than confirming the proposed mechanism

**Severity: major interpretive risk; adverse-result preservation resolved.**

**Exact locations.** `submission-jof/manuscript.tex:26,309,371`; `submission-jof/supplement.tex:1372`; `submission-jof/generated/v9-evidence-tables.tex:29–40,47–68`; `protocol/revision-v9/wp2-confirmatory.md:27–33`; `notes/revision-v9/wp2-acceptance.json:7–44`.

**Current evidence.** The primary screens meet their prewritten count criteria, and the method/DGP breakdowns also meet their corresponding reported screens. The universal smaller-model inequality fails, with every counterexample displayed. That failure is genuine evidence against the universal simplification claim, not a missing result. At the same time, each success indicator is the sign of a finite-repetition cell mean ratio, the cells share innovation streams, and the screen is a deterministic finite-grid classification rule—not a calibrated significance test, a confidence statement about a population of financial settings, or a causal mechanism test. No missing cells or outcome-dependent rule changes are hidden in the accepted output.

**Bounded response.** Keep the P1/P2 decision distinct from P3 and use “met the pre-run loss-sign screens” when a short phrase could otherwise imply statistical confirmation of the whole mechanism. In the generated table title at `v9-evidence-tables.tex:30`, “Pre-run simulation criteria” is less liable to be mistaken for a prospective financial validation or external preregistration than “Prospective simulation criteria.” This changes only scope wording, not the rule or its result. Do not replace the failed all-cell P3 criterion with its favorable majority. **Remaining gap:** the screen does not identify or statistically certify a universal estimation-cost mechanism.

## 4. Financial cutpoint consistency is weakly discriminating, retrospective and compatible with reversals

**Severity: major remaining threshold-identification limitation; censoring treatment resolved.**

**Exact locations.** `submission-jof/manuscript.tex:190,305,311–314,336,362`; `submission-jof/supplement.tex:1374–1376`; `submission-jof/generated/v9-evidence-tables.tex:24–28,77–86,109–115`; `protocol/revision-v9/wp3-learning-curve.md:31–43`; `notes/revision-v9/wp3-acceptance.json:13–55`.

**Current evidence.** The mapped discovery envelopes are broad. Three identified first crossings lie inside their bands; the remaining first crossing is left-censored and explicitly untestable. All-four numerical confirmation is false. Both longer-horizon curves return to positive relative loss at the largest history. Raw-history interpolation across the prescribed sparse grid supplies a convention-defined first crossing, not a directly observed transition at that precise history or a stable lower bound on adequate sample size. Changing the historical reference with history also means the curve is relative performance against a moving comparator, not the model's absolute expected-risk learning curve. The manuscript and complete table already resolve censoring substitution, later-root cherry-picking and universal-cutoff allegations.

**Bounded response.** Preserve “three identified consistent; one untestable; all-four not confirmed” as the complete prediction assessment, with “consistent” distinguished from precise or sustained forecast success. Keep the largest-history reversals adjacent to the positive crossing statement and the first-cutpoint convention in the caption. Do not sell the question-form title as a deployable minimum-history answer. **Remaining gap:** precise and persistent financial threshold identification is absent; no finer grid, alternative crossing, narrower interval or out-of-grid extrapolation is justified in this revision.

## 5. Nominal HAC and hit-test references do not repair the selection history or establish financial dependence conditions

**Severity: major remaining inferential limitation; computational/reference conventions disclosed.**

**Exact locations.** `submission-jof/manuscript.tex:180,185,190,267–286,364`; `submission-jof/extended-v9-technical.tex:209–217`; `submission-jof/generated/v9-evidence-tables.tex:86,91,115`; `protocol/revision-v9/wp3-learning-curve.md:45–49`.

**Current evidence.** The new financial diagnostics use the fixed original Bartlett bandwidth, a two-sided normal reference and no new family adjustment. Shared fitting can induce dependence beyond the overlapping response horizon; stationarity/mixing, moments and positive long-run variance remain working premises. The broader research path includes already inspected periods, alternative models, references, penalties and diagnostics. The old named adjustments and sensitivities remain visible, but cannot retroactively adjust that entire sequence. The hit-test table correctly warns that a spaced grid does not create independence and that nonrejection differs from calibrated coverage. Source agreement and numerical certificates do not establish these statistical assumptions.

**Bounded response.** Keep “nominal/working-reference” attached to new DM reporting and keep cutpoint classifications independent of p-value selection. Consider naming the generated column “Nominal DM p” so a standalone table retains the intended scope. Do not use a small p-value to strengthen the mechanism claim, or nonrejection to claim operational calibration. No additional bandwidth search, correction family or coverage test is requested. **Remaining gap:** valid selection-adjusted, dependence-justified financial inference is not supplied; this limits evidential strength even when saved arithmetic is exact.

## 6. Broader tasks and byte agreement do not supply independent dealer validation or a historical information-vintage backtest

**Severity: major remaining external-validity/data-availability limitation; source distinctions resolved.**

**Exact locations.** `submission-jof/manuscript.tex:123–131,188–190,317–319,356–359,383–387`; `submission-jof/supplement.tex:1374–1376`; `protocol/revision-v9/wp3-learning-curve.md:3,7–9,19–29`; `notes/revision-v9/wp3-acceptance.json:10–12,104–114`.

**Current evidence.** The learning curves reuse the previously inspected FX record and period. Daily aggregation reuses the same dealer and changes several features of the forecasting task at once. The weekly position categories are independently compiled aggregate tasks but share a reporting system, components and economic timing; they are neither unseen individual dealers nor independent replications. Economic dates in a downloaded version do not reconstruct the values available at each issue time, and FX timestamps have unknown authenticated timezone and preserved gaps. The exact old-output gate and independent arithmetic readback are valuable reproducibility controls, explicitly distinct from independent scientific replication. The manuscript currently makes these distinctions correctly.

**Bounded response.** Keep “retrospective,” “same dealer” and “related aggregate tasks” in summaries that span data sources. Preserve the future independent-dealer/prospective protocol as a required next evidential step, rather than implying it has been partly filled by data aggregation or byte agreement. The code/data availability section should continue separating publicly checkable aggregate evidence from the private licensed vectors. **Remaining gap:** compatible independent dealer, historical release-vintage reconstruction and untouched prospective financial outcomes are all unavailable; none can be repaired by prose or an additional same-period diagnostic.

## 7. The defensible originality is a bounded comparative forecasting application, with elementary theory and unmeasured operating value

**Severity: moderate-to-major positioning limitation; no arithmetic or proof defect identified by this review.**

**Exact locations.** `submission-jof/manuscript.tex:42–46,56–62,78,99–113,138,333–336,364,377`; `submission-jof/extended-v9-technical.tex:219–235`; `submission-jof/supplement.tex:84–114,1174–1177`.

**Current evidence.** The peak target and label-maturity/floor constraints differ substantively from the closest signed-endpoint FX task, while prior portfolio and payment studies already establish within-period path-risk precedents. Conditional quantile methods, learning curves, score diagrams and the maximal inequality are mature tools. The floor projection is elementary and the endpoint-to-peak result is a stated classical application, not a new estimator or a new maximal-inequality theorem. The recent contribution is the matched comparative evidence, adverse-case map and pre-run checks of an explicitly post hoc pattern. The chosen asymmetric loss preference is hypothetical, and there is no measured inventory/funding/hedging policy value or deployment fallback evaluation. Current text largely avoids overstating these points.

**Bounded response.** Keep C1 as target formalization plus elementary/classical applications, and C2/C3 as comparative validation findings. State the useful empirical lesson concretely—history, reference, score and breach trade-offs must be evaluated together—without claiming a new general theory, new quantile engine, causal mechanism or demonstrated operating value. Preserve the exact nearest-neighbor task distinctions and partial-reading qualifications rather than broad novelty assertions. **Remaining gap:** wider generality and measured economic usefulness remain unestablished. Stronger wording cannot supply a higher publication level; journal fit must rest on whether this bounded empirical/application contribution is sufficient for that readership.
