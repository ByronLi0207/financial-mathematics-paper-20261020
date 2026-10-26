# WP5 evidence-to-claim map and learning-curve source scope

Review completed 2026-10-24 23:51:24 UTC at HEAD `32ee58688bac260de322c31cb8945adbf3b53154`. This note reads existing evidence and one targeted literature source. It adds no statistic, model, experiment or manuscript edit. The appropriate writing branch is **partly supported**.

## Evidence-to-claim map

| Existing evidence | Supported wording | Boundary / wording to avoid | Owning evidence |
|---|---|---|---|
| Post hoc coordinate selection chose c=W/(H+1), with no p term. | A horizon-adjusted history coordinate organizes the compared cells. | It is not an identified effective sample size, effective degrees of freedom, or sample-per-parameter mechanism. Its classification score is resubstitution description. | `notes/revision-v9/wp1-breakeven.json`; `protocol/revision-v9/wp1-posthoc-design.json:146–160,168–191`. |
| New-DGP P1 and P2 pass their fixed pooled criteria; the saved method and DGP breakdowns also pass. | The prespecified short-history-loss / long-history-win pattern receives support on the new simulation grid. | A finite-grid screen is not a universal probability statement or an independent-cell significance test. It does not separately identify estimation cost. | `notes/revision-v9/wp2-readout.md:5–11`; `results/revision-v9/wp2/support.json`. |
| P3 satisfies 42 of 48 inequalities and fails its universal criterion. | The universal simplification prediction fails. | Do not replace “all” with “most,” call P3 supported, or assert that the parsimonious procedure always lowers loss at a common c. | `notes/revision-v9/wp2-readout.md:5–11`; `results/revision-v9/wp2/support.json:1918–1926`. |
| Three FX first cutpoints are identified and lie within their fixed ranges. | Three numerical cutpoint predictions are consistent with the retrospective FX curves. | Do not claim all-four confirmation, interval coverage, independent financial replication, or threshold stability across markets. | `notes/revision-v9/wp3-readout.md:7–14`; `results/revision-v9/wp3/curve-predictions.json`. |
| QR4/H6 already has a nonpositive relative loss at the smallest W; its first root is unidentified. | The remaining prediction is compatible but left-censored and NOT_TESTABLE. | A later downward crossing cannot replace the first cutpoint; compatibility is not confirmation or a statistical rejection. | `notes/revision-v9/wp3-readout.md:10,14`; `results/revision-v9/wp3/curve-predictions.json:32–60`. |
| Both H24 procedures have positive relative loss again at W5760. | The observed history-length pattern is nonmonotone. | The first downward cutpoint does not imply every larger W wins, and the reversal must remain visible beside earlier gains. | `notes/revision-v9/wp3-readout.md:16,39–43`. |
| Every W changes the regression fit and its same-W historical reference. | The curve compares complete procedures under matched histories. | Relative-loss movements do not isolate a regression's absolute learning curve against an unchanged control. | `notes/revision-v9/wp3-readout.md:16,20`; `protocol/revision-v9/wp3-learning-curve.md`. |
| QR33 and QR4 retain different penalty menus and candidate-failure/tie rules; there is no oracle-risk decomposition. | The experiment compares the specified full and parsimonious procedures. | Predictor count, regularization, model approximation, validation choice and finite-sample estimation have not been separated into causal components. | `protocol/revision-v9/wp2-confirmatory.md:17–19,33`; `protocol/revision-v9/wp3-learning-curve.md`, original-procedure section. |
| The FX period, original W720/W2880 cases and source family were already studied. | The new history grid tests fixed numerical predictions on a known period. | Pre-run registration of this grid does not restore an untouched financial holdout or add a second dealer. | `notes/revision-v9/wp3-readout.md:3,45`; `protocol/revision-v9/wp3-learning-curve.md`, opening paragraph. |

## One targeted mature source: metadata and actual reading

**Viering, Tom, and Marco Loog (2023). “The Shape of Learning Curves: A Review.” IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(6), 7799–7819. DOI: 10.1109/TPAMI.2022.3220744.** The author-institution record identifies the final published version. [TU Delft record](https://research.tudelft.nl/en/publications/the-shape-of-learning-curves-a-review/).

The checked author preprint is **arXiv:2103.10948v2**, revised **5 November 2022**; v1 was submitted **19 March 2021**. Its arXiv DOI is **10.48550/arXiv.2103.10948**, distinct from the journal DOI. Actual reading was partial: abstract/version history; v2 §§II-A/B/D/F/G (definition, estimation, summaries and complexity); and VI prelude/VI-B–D (nonmonotonicity and its qualifications). No claim is made to have checked every cited primary theorem. [Version record](https://arxiv.org/abs/2103.10948); [v2 body](https://arxiv.org/html/2103.10948v2).

The review separates expected generalization curves from individual curves and feature/complexity curves. Its standard definition uses i.i.d. training samples from a fixed distribution; it documents nonmonotone examples and warns that scalar summaries can conceal crossings. These are background facts, not a theorem about the present time-series procedure. [§§II-A/D/F/G and VI-B–D](https://arxiv.org/html/2103.10948v2).

## Novelty and interpretation boundary

Learning curves, sample/complexity interactions and nonmonotone performance are mature concepts. This source supplies background for displaying the complete curve; it neither makes the proposed history coordinate novel nor diagnoses the cause of the present reversals. Our dependent chronological windows, changing time spans and matched reference differ from the review's standard expected-risk object. The evidence here supports an application-specific empirical pattern and its failures, rather than a new general theory of learning or an identified estimation-cost channel.

The working contribution can remain the sampled peak-position response with its known floor, completed-label clock, matched references, explicit finite-grid predictions, and documented counterexamples. Claims about firstness or superiority over the closest financial literature require the existing task-specific source comparisons; this general review cannot establish them. No new computation is proposed to strengthen those claims during WP5.

## Candidate manuscript wording, to be fitted to the actual section

**Title:** “When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits.” The question form fits partial support; it should not be paired with an abstract promising a universal threshold or an identified estimation-cost explanation.

**Central claim:** “Training-history length helps organize when conditional peak forecasts improve on matched historical rules. New simulations support a prespecified short- versus long-history pattern, while the retrospective FX curves provide partial corroboration.”

**C2 / results continuation:** “Three FX cutpoints agree with their predicted ranges; a fourth remains left-censored. Long-horizon reversals and the failed simplification prediction make validation at the actual history, horizon and reference essential.”

**Literature bridge:** “Learning-curve research documents diverse, sometimes nonmonotone relationships between sample size and predictive performance (Viering and Loog, 2023). Our chronological comparisons examine relative loss against a historical reference that changes with the training window.” [Background source](https://doi.org/10.1109/TPAMI.2022.3220744).

Keep detailed limitations in their designated section, but preserve the v9-required post hoc coordinate selection, partial prediction status and retrospective provenance wherever needed for an accurate interpretation. A stylistic rewrite must not turn either NOT_SUPPORT or NOT_TESTABLE into SUPPORT.
