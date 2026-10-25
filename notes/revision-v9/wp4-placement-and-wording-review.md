# WP4 figure placement and WP5 writing checklist

Read-only review at 2026-10-24 23:41:00 UTC, HEAD `bfd0493f4237b6b99ca4370a2e6cf2195f653b28`. Paths and line numbers below refer to that snapshot. This review inspected source text and existing readouts; it did not render figures, modify the manuscript, calculate statistics, or add analysis.

## Placement recommendation

The current four main figures are:

| Source location | Figure / purpose | Recommendation |
|---|---|---|
| `submission-jof/manuscript.tex:27–29`; cited at lines 21 and 90 | `fig:example`, endpoint-contained but peak-breaching Treasury path | Keep: it explains why the response differs from an endpoint forecast. |
| `submission-jof/manuscript.tex:283–285`; cited at line 255 | `fig:murphyfx`, FX primary elementary-score comparison | Keep: it supports a separate scoring-preference issue. |
| `submission-jof/manuscript.tex:287–289`; cited at line 255 | `fig:murphybill`, distinct Treasury primary comparison | Keep unless later space pressure requires relocation; its evidence remains distinct from FX. |
| `submission-jof/manuscript.tex:297–299`; cited at line 295 | `fig:mechanism`, v8 QR33-only controlled-grid heatmap | **Replace with the WP4 unified plot.** Its QR33-only display is narrower than the new figure, which also carries QR4, the new simulations, and financial comparisons. |

Keep the displaced QR33 heatmap file and its complete numerical annotations. Place it in the Supplement beside the existing QR4 heatmap at `submission-jof/supplement.tex:1471–1479`, with a distinct label. The complete v8 tables and adverse narrow-regime screen are already discussed at supplement lines 1444–1469 and must remain. Replacing a main figure does not authorize deleting its unfavorable evidence.

If `fig:mechanism` is reused for the unified plot, update its line-295 introduction: the present sentence promises a cell heatmap with Monte Carlo standard-error annotations. It would misdescribe a unified scatter unless those annotations are actually present. Preserve the original narrow-regime counts in the surrounding prose or Supplement. WP4 itself should change only this placement, its citation, and its caption; the substantive WP5 rewrite follows its own gate.

## Caption and interpretation guardrails

Necessary evidence anchors:

- Coordinate c=W/(H+1) excludes p: `protocol/revision-v9/wp1-posthoc-design.json:168–191` and `notes/revision-v9/wp1-breakeven.json`.
- New-simulation pooled P1/P2 pass is distinct from universal simplification P3 failure: `results/revision-v9/wp2/support.json:1918–1926` records P3 as NOT_SUPPORT, with 42 of 48 inequalities satisfied rather than all.
- Three identified FX cutpoints are consistent; QR4/H6 remains left-censored and NOT_TESTABLE, so all-four confirmation is unmet: `notes/revision-v9/wp3-readout.md:7–16` and `results/revision-v9/wp3/curve-predictions.json:32–60`.
- Both long-horizon regressions lose again at W5760: `notes/revision-v9/wp3-readout.md:39–43`. Increasing W changes both the regression and its matched historical reference; it does not hold F fixed (readout line 16).
- Financial evidence reuses the previously studied period and is retrospective: readout lines 3 and 45. No fresh dealer or untouched holdout was added.

Suggested caption, conditional on the actual marker/band design:

> Relative quantile loss against same-history historical headroom, on a logarithmic c=W/(H+1) axis that excludes coefficient count. Light markers distinguish the original and new simulations; dark markers distinguish the financial tasks and both regression procedures. Bands are the original simulation's post hoc first-cutpoint envelopes, conditional on its selected coordinate and process grid. The new simulation passes the pooled loss-pattern screen but fails the universal simplification prediction. Three FX cutpoints are consistent with their prespecified bands; the remaining case is left-censored, and both long-horizon curves reverse at the largest history. The financial observations reuse an earlier studied period, so the combined evidence supports a partial, nonmonotone history-length pattern.

Do not use the plan's illustrative “effective sample per parameter” or “only after” language: c omits p, the simplification prediction fails, and the largest-history reversals directly qualify a permanent threshold rule. Point tracing should identify method, source, H, W, original result row and the exact matched reference. The caption must describe the bands actually plotted, not turn them into universal confidence bands or operating-limit cutoffs.

## Actual v7 S6 checklist for WP5

The governing passage is `revision-plan-v7-final.md:123–148` in the user-provided plan directory; this checklist transcribes it without running its statistics. Its stated exclusion is **the “Research design and transparency” subsection and table notes** (line 125), not a blanket exclusion of figure captions or all limitations.

- Abstract: at most 180 words and at most five numbers (line 128).
- Mean sentence length: 18–24 words; sentences above 35 words: at most 8% (line 129).
- Each sentence: at most two numbers, with remaining numerical detail moved to tables (line 130).
- Sentences containing `not / no / neither / nor / cannot`: at most 8% (line 131).
- Zero counts for the exact banned list: `retained`, `declared`, `frozen`, `receipt`, `archive(d)`, `byte`, `hash`, `post-result`, `exploratory`, `inspected`, `stipulated`, `issued`, `admissible`, `source-specific`, “no … is claimed”, “does not establish” (line 132).
- Each paragraph: at most six sentences, beginning with its topic sentence (line 133).
- Qualitative checks: active voice; meaning before numerical detail; a limit-manager implication in the Introduction, Results/section 7, and Conclusion; general disclaimers consolidated in Limitations; each section ends with a takeaway (lines 135–140).
- Acceptance evidence: a before/after table covering every numerical writing measure, and the actual before/after abstract and first Introduction paragraph in CHANGELOG (line 148).

`post hoc` is not among the S6 banned strings. The later v9 requirement to label the WP1 selection post hoc and to state the real-data evidence boundary must remain truthful; stylistic cleanup must not remove those distinctions. Put detailed execution vocabulary in the specifically excluded transparency subsection/table notes, while retaining concise scientific provenance where v9 requires it.
