# Verification loop 019 — internal referee A: scoring and calibration

**Verdict: PASS for the bounded Section 7 reread and owning-definition/output correspondence below.** No necessary scientific-conclusion problem was identified. Author-pending scientific-conclusion items: **none identified in this scope**. The optional language concerns at the end are not implemented.

This is internal verification, not external peer review, independent financial validation, a new analysis or a new proof. Read-only shell/Python helpers parsed existing files/fields, computed source fingerprints and rendered the two existing figure PDFs in memory. No test, model, simulation, statistical procedure, preference-envelope calculation, Murphy calculation, forecast replay, scientific generator, UI action or commit was run. Only this note is written; no source, state, manuscript, result or archive is edited.

## Exact scope and time

- Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`; observed branch `revision-v4-jof`.
- Initial read at **2026-10-23 21:52:52.391796 UTC** (14:52:52 America/Vancouver): current `submission-jof/manuscript-content.json`, **`sections[6]`**, heading verified as **`7. Scoring and calibration (RQ2)`**, **all 9 blocks, indices 0–8**. Main source SHA-256 at that read: `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2`.
- Corresponding main TeX: `submission-jof/manuscript.tex`, **lines 264–303**, ending before Section 8. This includes Table 5, all prose, both figure blocks/captions and the additional-benchmark paragraph.
- Main figures array entries **2 and 3**, referenced by Section 7 blocks 6 and 7, were read. Both existing one-page PDF figure assets were rendered **in memory** and visually inspected using the PDF read-only workflow; no image or PDF output file was created. Their original-primary headings, fixed `τ=.95` labels and legends (`QR`/`Rolling F` for FX, `QR`/`Frozen F` for Treasury) agree with their claimed identities. Curve pixels are not used to establish full-breakpoint dominance.
- Owning supplement scope: current supplement JSON **S6, all 8 blocks**; **S9, all 5 blocks**, including the full-breakpoint summary and complete Holm table; the single **S7 Table S23 at `sections[6].blocks[3]`**; and **S16 blocks 0,1,3,6,17,26,31,39,40** for finite adaptations, inference limitations, combinations, state diagnostics and refitted-target availability. Supplement section labels were checked in TeX; the full supplement TeX was not reread or assigned a whole-document verdict.
- Owning saved outputs: targeted fields/rows in `inference/murphy-summary.csv`, `coverage.csv`, `dm.csv`, `holm.csv`; the existing numeric `family` fields in `recovery/holm-bandwidth-readback.json`; the three named FX contrasts in `paired-comparisons.csv`; existing preference `headline_comparisons` and group identities/winners, plus group 5's stored intervals/endpoints; selected existing WP2/WP3 primary-context summaries; the two WP4 primary state records; all six WP5 target-level summary slots; and the two `.99` validation records.
- Static definitions/presentation passages read: `preference_frontier.py` through its finite-envelope implementation; the relevant `inference_tests.py` HAC/coverage/DQ/Holm/Murphy definitions; `run_v3_inference.py` source/reference selection and output-generation passages; `v3_inference_presentation.py`; and relevant current `v6_submission.py`, `v6_wp2_findings.py`, `v6_wp3_findings.py` assembly passages. These functions were not imported or invoked.
- Source fingerprints below were captured at **2026-10-23 21:54:39 UTC**, with the existing Holm-readback fingerprint captured during the subsequent targeted read. The current main still matched its initial hash at **2026-10-23 21:55:28 UTC**. Post-write readback checks the recorded hashes again.
- HEAD initially observed: `9666d2d428e0893699f43c13dff0d5e0a47d7a7b`; a later observation at 21:55:28 UTC was `43ca27397ec3c58d399673cfc94ed59493819ed9`, reflecting concurrent coordinator work. This worker made no commit. Tracked working-tree and index diff listings at both observations were empty.

Search hits in older source prose and the reproduction guide were routing context only. Earlier-loop verdicts, historical claims of test success and other repeated main-section content are not evidence for this verdict. The numeric `family` fields of the already saved Holm bandwidth readback were read as existing aggregate data, not adopted as a previous review verdict. No conclusion is extended to another main section.

## Findings by Section 7 blocks

### Blocks 0–1: working-reference inference, identities and nulls

The coverage-table heading explicitly labels post-result/exploratory diagnostics, strict hits on the fixed `H+1` grid, chi-square references, the full-sample HAC DQ adaptation, and boundary/small-sample qualifications. Its seven row identities match the existing `coverage.csv` selectors:

| Main row | Exact saved `(source,H,W,method)` identity | Existing CSV data-row index |
|---|---|---:|
| FX QR H6 | `(fx_hourly,6,2880,QR)` | 3 |
| FX rolling F H6 | `(fx_hourly,6,720,rolling_F)` | 24 |
| FX matched F H6 | `(fx_hourly,6,2880,frozen_F)` | 36 |
| FX QR H24 | `(fx_hourly,24,2880,QR)` | 9 |
| FX legacy S H24 | `(fx_hourly,24,720,rolling_S)` | 40 |
| Treasury QR H6 | `(nyfed_weekly,6,260,QR)` | 15 |
| Treasury F H6 | `(nyfed_weekly,6,260,frozen_F)` | 66 |

The displayed `k/n`, POF, independence, CC and DQ fields correspond to those saved rows and their displayed rounding. The last row retains the stored boundary-reference qualification; no nonsignificant p-value is read as a certificate of conditional coverage.

The existing DM identities also distinguish the FX original primary `fx_hourly-h6-QR2880-minus-rolling_F720` from the matched `fx_hourly-h6-QR2880-minus-frozen_F2880`. Both saved statistics are negative; the Treasury primary `nyfed_weekly-h6-QR260-minus-frozen_F260` is positive. The H24 legacy remains separately identified as `fx_hourly-h24-QR2880-minus-rolling_S720`, with the stored DM/HLN values rounding to .839. The original FX cross-window contrasts are outside the fixed 72-member common-history Holm family; Treasury primary belongs to that family and is not counted again under a second identity.

The existing `recovery/holm-bandwidth-readback.json` numeric fields give `family_size=72`, `base_below_05=19`, `double_below_05=18`, and base directions `favorable=15`, `adverse=4`, `zero=0`. Its source hash binds the current saved `holm.csv`. These values were read, not recomputed by running Holm in this loop. The matched FX Holm value and Treasury value correspond to the saved rows, approximately `2.8626953e-07` and `.3196775`.

S9 and `inference-design.md` retain the important limits: valid component p-values are a premise for Holm control, adjustment does not repair an unverified DM reference or historical selection, sparse grids retain common-training dependence, and fixed-window overlapping-target pinball/HAC/HLN calculations are adaptations under working assumptions. Equality-based coverage moments differ from an upper-quantile inequality in the presence of atoms. The legacy CC is explicitly its archived full-grid POF plus transition-independence sum; S16's new transition-conditional CC has a separately stated definition. Section 7 does not conflate these conventions or infer conditional coverage from equal-loss testing or nonrejection.

### Blocks 2, 6 and 7: fixed quantile level, changing threshold, original primaries

The text and both figure captions fix `τ=.95` and vary the elementary-score threshold `θ`. This is distinct from changing shortfall/excess weights on fixed reports. The owning `murphy-summary.csv` contains exactly the two declared original-primary identities:

| Saved contrast | Existing breakpoint count | Existing difference range | Existing ranking |
|---|---:|---|---|
| FX `QR2880-minus-rolling_F720` | 16146 | negative minimum and positive maximum | CROSSING |
| Treasury `QR260-minus-frozen_F260` | 640 | negative minimum and positive maximum | CROSSING |

Each record separately states `tau=.95` and `display_grid_points=201`. The static Murphy implementation evaluates the unique union of predictions/outcomes with its stated floating arithmetic tolerance; `run_v3_inference.py` selects `declared_source_primary=True` before producing the 201-point display grid. This matches the main distinction between an all-breakpoint check and an aggregate display. It does not turn a display curve into a new population result.

Both current figure PDFs visibly identify the corresponding original-primary source and reference type. They are not the matched FX W2880 comparison or the additional fixed-combination Murphy diagrams. The conclusion is explicitly empirical sample non-dominance over the fixed-level consistent-score class; it is not a population calibration or all-cost dominance claim. The existing integral agreement remains an arithmetic identity check, not independent numerical validation. No elementary-score curve was recomputed here.

### Block 3: component means, strict hits and genuine costs

The existing named FX H6 `headline_comparisons[0]` and `[1]` in `preference-robustness/results.json` retain both reduced component means and larger strict-breach counts: original primary **376 versus 332** and matched comparison **376 versus 360**. Their saved U/V tokens and the `paired-comparisons.csv` difference fields distinguish unconditional mean underprediction/overprediction amounts from event frequency and method-specific breach-severity sets.

S6's already stated affine objective is `J_m(a)=a U_m+(1−a)V_m`, with `a=.95` recovering the stipulated score. Its coefficientwise statement is explicitly a **weak** comparison for constant nonnegative weights, with strictness only when a positively weighted component strictly decreases. Section 7 does not expand that statement into dominance under all consistent `.95` scores: the Murphy results directly document crossing for the original primaries.

The same paragraph expressly confines its empirical first-order stochastic-dominance comment to the distribution of **positive-part errors including zeros**. It does not assert reverse dominance, that positive-error magnitudes all increase, or that a smaller unconditional U implies fewer incidents. Its cost-per-breach/nonlinear-loss qualification keeps this separate from observed financing costs. No new dominance proof or cost experiment is supplied by this reread.

The H24 legacy remains the opposing-component case. Existing Table S23 records `dU=+0.167864`, `dV=−3.463190` in its stated FX-million display and the saved crossing ratio **20.630898**, matching the main's rounded **20.63**. This is a preference sensitivity of fixed reports against the rolling-S W720 reference, not a refitted quantile, a matched-history causal feature comparison, or an identified financing-cost ratio.

### Blocks 4–5: finite-menu lower envelopes and endpoints

The menu is explicitly the eight archived `.95` reports: QR, KNN, scaled KNN, matched frozen F/S/K, AR and I. The existing group method names agree; rolling, one-state and floor-only actions are excluded. Shared completed-response history length and refit schedule are not equated with identical feature lookbacks, model assumptions or all feasible decisions.

The text explicitly includes the feasible floor-only report `C=B` as a possible minimizer of the single-component `a=0` objective, while saying it is **absent from this menu**. Endpoint winners are therefore reported as finite-menu winners. S6 also preserves exact-decimal boundary/tie qualifications and separately evaluates endpoints rather than inferring them from rounded interior intervals. These restrictions agree with the existing static finite-envelope definition.

For the concrete Treasury H6 W260 full-origin claim, existing **`groups[5]`** in `preference-robustness/results.json` has 277 origins, `winners_at_095=[AR1_REPLAY]`, endpoint `a=0` winner AR1_REPLAY, endpoint `a=1` winner frozen_K, and open regions AR1_REPLAY/frozen_K with their shared boundary tie. QR is absent from all its saved regions/points. This supports only the stated “among these eight reports, including both endpoints” conclusion.

The saved full/sparse `winners_at_095` fields identify the stated four changed cells: FX H24 W720; Treasury H6 W52 and W260; Treasury H24 W52. Sparse Treasury H24 groups retain 12 origins. Section 7 labels these as dependent within-archive sensitivities and does not count them as independent replications, a deployable switching rule, a confidence set or global action optimization. Its S5/S6/S7/S10 pointers are navigation, not newly asserted guarantees for those supplements.

### Block 8: finite adaptations, matched references, state interpretation and target-level NA

The long-history H6 FX **matched** wrapper comparison comes from existing WP2 `wrapped_pairs[1]`: `source=fx_hourly`, `horizon=6`, `window=2880`, saved loss change `−14.996910788%`, and rates `329/6625=.0496603774` for wrapped QR versus `328/6625=.0495094340` for wrapped F. The main's **15.00%** phrasing and “observed breach frequencies close” concern those actual wrapped reports. They are not the original QR-versus-rolling-F primary, and no canonical ACI or conditional-coverage theorem is imported. S16 retains finite memory, delayed maturity, projected adaptation, coverage-first retrospective tuning, failures and the finite-rank domain.

The SAV direction remains adverse against matched F in both named H6 contexts. WP2's saved method/control rows give FX W2880 mean losses **456696.2217 versus 452692.9834**, and Treasury W260 **2892.2309 versus 2758.6653**. Numerical completion is not called forecasting superiority. The SAV definition remains a mature-headroom adaptation with a finite multi-start algorithm, retained failures and no claimed global optimum.

Existing WP3 `primary_context_rows[0:4]` distinguish combination constituents from original cross-window primary references. FX mean/median percentages versus QR are positive (**4.8725% / 4.2207%**), while the Treasury median is below matched F and QR (**−3.9813% / −36.3211%**) but retains a full hit rate **28/277=.1010830**, above .05. These are fixed aligned-constituent comparisons; the S16 definition does not infer a valid conditional quantile or calibration from floor preservation or a favorable mean score. Missing plain-KNN constituent cases remain NA rather than substituted.

The two saved WP4 rows retain **original-primary** references: FX QR W2880 versus rolling F W720, and Treasury QR W260 versus frozen F W260. FX low/middle/high saved means are all negative; Treasury saved means are all positive, with groups of 9/25/243 for Treasury. The paragraph correctly avoids a high-state-only, every-group-significance, causal-state or switching-policy conclusion. S16 and the saved file preserve the finite-instrument and HAC working-reference limits; a joint test can reflect an unconditional mean rather than a state effect.

The existing WP5 summary has exactly three available `.90` named H6 contrasts and three `.99` NA slots. At `.90`, FX primary and matched comparisons are separately named; Treasury primary/matched coincide and count once. Saved directions do not reverse relative to their own `.95` references. At `.99`, the two FX comparison slots inherit whole-menu validation failure (`failed_candidates=[0.01]`); Treasury inherits the declared tail-information screen. The saved Treasury screen retains validation tail fraction **13/25** and W260 tail fraction **13/5**, below the minimum 5. Raw-p NA is not converted into a genuine p-value by `bookkeeping_p=1`/Holm accounting. S16 explicitly calls the tail screen a minimum-information convention rather than a calibration theorem. No `.99` unavailable comparison is interpreted as evaluated robustness evidence, and scores across different target levels are not treated as the unchanged `.95` objective or actual funding costs.

## Optional language concerns — not edits or author-pending scientific problems

1. Block 3's exact current phrase is **“their sample-average improvement persists under every constant nonnegative linear weighting of those components.”** Its frozen empirical scope is the two named H6 FX comparisons on the same 6,625 origins. The stored QR-minus-reference differences are `dU=−10408.03273273336` and `dV=−920830.4090531879` USD for QR W2880 versus original rolling F W720; and `dU=−29549.203192461686`, `dV=−775527.0985049764` USD for QR W2880 versus matched frozen F W2880. Both components decrease in both saved comparisons. S6 already calls the comparison weak for every constant nonnegative weighting and strict when a positively weighted component strictly decreases. Thus the optional precision change could say **“weak improvement”**, or explicitly require **at least one positive weight** when retaining strict-improvement language. This handles the all-zero objective without changing the saved component directions, forecast result, empirical scope or scientific conclusion. No new proof is developed or manuscript wording changed here.
2. In block 8, the “lower”/“upper” target-level sentence could name **`.90` / `.99` and the three named H6 comparisons** directly. S16 and the existing summary already bound that scope. This would help a reader keep refitted-target sensitivity separate from fixed-report reweighting and avoid reading the summary as evidence for every history/horizon.

Neither option is applied. No necessary conclusion problem was found that requires author decision in this bounded reread.

## Source fingerprints

These SHA-256 values bind the actual inspected sources. Hashing a full file does not imply a full-file scientific audit where the read scope above is narrower. Current figure bytes were visually inspected in memory; no plot generation or all-breakpoint calculation was rerun.

| Source | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2` |
| `submission-jof/manuscript.tex` | `6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |
| `submission-jof/figures/murphy-fx_hourly.pdf` | `cb468b67cada0035d12a097893bd0daeb8a7011fb63574c3d32f1b54d6726cb0` |
| `submission-jof/figures/murphy-nyfed_weekly.pdf` | `20769ff90e7bf5171b4b290a5204ad4479243168374f28b6756a35dfbb32f871` |
| `results/revision-20261023/inference/murphy-summary.csv` | `0ad8e0b96b4af14b2de460b9eab92fb9aa47a7d7f655aa64372dad93de7ccac1` |
| `results/revision-20261023/inference/coverage.csv` | `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419` |
| `results/revision-20261023/inference/dm.csv` | `0e8aa499fab31a5928be0ccb9198d5f6ee2833a01410a17fc965985bb65f5e41` |
| `results/revision-20261023/inference/holm.csv` | `976affb08867b6e1c821f6ce5d9491a3b8087f427f0af9296763872863d2c8b3` |
| `results/revision-20261023/recovery/holm-bandwidth-readback.json` | `ce50ff20822ccda76e67d179695bfc406f2624f9fe0763bb3f4ee6b5dc4ef714` |
| `results/revision-20261023/inference-design.md` | `31353e0470d744c9adccb7a5130935542cdce1ccc4f993fc09951a2a5e8d59cf` |
| `results/revision-20261022/paired-comparisons.csv` | `a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9` |
| `results/revision-20261022/preference-robustness/results.json` | `5c644543f6461f94050e0049c94f092ae6ad8358adb277944ece4dc8bcdba418` |
| `preference_frontier.py` | `72680f65671a7b7cf4408946b4208a57a9166e4cda253b22aabd8f0f61ba71b5` |
| `inference_tests.py` | `2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c` |
| `run_v3_inference.py` | `f54ff54dcbc8db5c7446f0fc885bce1d5408cb329d0545ba7021699f1301a527` |
| `v3_inference_presentation.py` | `a508760fc79630130fe22bc96dd7a8018f8ab478cec7eca112261d5a6308bf63` |
| `v6_submission.py` | `6f96167d21ea915b7c71a0a2a80d9bab5d4beb96075e67d43ddf4db56c7f46f2` |
| `v6_wp2_findings.py` | `447483b14ebab89b9e082d971e3e550735073269d9262d8895e9116e477bc974` |
| `v6_wp3_findings.py` | `a8229f40a151ba2415a7c34f9f05227073e98f50ec9aa2c62b7239454d1c8725` |
| `results/revision-20261023/v6/wp2-findings.json` | `8841a9258bae71c4c162afc6c5efd91ff4fa2a323621db637b7f012cf1623972` |
| `results/revision-20261023/v6/wp2-summary.json` | `44beea32857e5f13233178e014c4ed4737918f523b61790e42d2c94ee763f98c` |
| `results/revision-20261023/v6/wp3-findings.json` | `abe27d8f1ef08ba50680b6f3e1a9207f7271cdb4270f92437fbaa1746ad523e9` |
| `results/revision-20261023/v6/wp4-states.json` | `63a89756ba5a97e9a4454701708ff12972e2d23cfd24c238b25b490a531e833d` |
| `results/revision-20261023/v6/wp5-tau-summary.json` | `085d2dbf7a94a13f3b1557d966848cf5f58382fa4f330dc8e221235427c71501` |
| `results/revision-20261023/v6/wp5-v2/validation-fx_hourly-tau99.json` | `acc80821319024ee04437c960cc3cb1b9792c223b88255bed5469edc8bb2f8fa` |
| `results/revision-20261023/v6/wp5-v2/validation-nyfed_weekly-tau99.json` | `b47909d0fee75aea6c0e2cbc3124b6fba38be4fab65f678e1536505e6a272926` |

The bounded PASS above concerns the language and its correspondence to these existing definitions/outputs. It does not establish validity of the component reference distributions, remove inspected-sample selection, validate every source field independently, or certify conditional coverage or decision-cost relevance.
