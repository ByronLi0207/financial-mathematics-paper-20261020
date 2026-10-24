# Verification loop 015: internal financial referee B — transport and robustness

**Verdict: PASS for the bounded Section 8 interpretive verification. Necessary scientific-conclusion change / author pending: none identified.**

Review role: internal financial measurement, transport and target-relevance referee B. This is not external peer review or independent replication.

First complete Section 8 read observed: 2026-10-23T21:41:31.679721+00:00.
Fingerprint/source read observed: 2026-10-23T21:44:11.129588+00:00.
Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Observed branch: `revision-v4-jof`.
Audited source commit: `14262bd68ac5e18c5daaf961c0730a43442e4957`.

## Exact manuscript scope

The authorized manuscript sample is exactly `submission-jof/manuscript-content.json` → `/sections/7`, headed **8. Transport and robustness (RQ3)**. All six blocks, `/blocks/0` through `/blocks/5`, were read in full. All six are paragraphs: **there is no table in this section**. The corresponding current TeX is `submission-jof/manuscript.tex`, lines **304–316**, including its heading and paragraph separators.

Other main sections, the abstract and the conclusions were not reread or given a verdict in this round. The previous loop7 referee-B note was read only to preserve role/scope separation from its Section3 review.

The method was source-first interpretive reconciliation: preserve the named financial target and reference identity, distinguish related aggregate tasks from independent dealer samples, distinguish an inspected economic-date replay from a prior-issued prospective forecast, and keep missing/failed output separate from an observed adverse score. The owning protocol/result reads below concern existing metadata, aggregate scores, statuses and source routes only. No raw observations or private per-origin traces were opened.

Canonical section identity (UTF-8 JSON, ensure_ascii=False, sorted keys, compact separators):
`b708b3478db7f3ef72cd8430c52212cafa0b1bd4dd7cc8785403866606bcf13e`.

Exact UTF-8 TeX lines 304–316 with original line endings:
`e90aadf07926e500c4516e71b58525fc4857c450588e77d22dfb2b6521039312`.

## Block-by-block assessment

| Main block / TeX line | Interpretive identity checked | Assessment |
|---|---|---|
| 0 / 305 | Classical-bound plug-in L directions and oracle-threshold simulations | The L-versus-F archive selects `left_method=Levy_L`, `right_method=frozen_F`, with exact source/H/W identities. All four FX loss changes are adverse while their stored L hit counts are below F. Both Treasury H24 loss changes and hit-count changes are adverse; Treasury H6/W260 loss is lower. The paragraph therefore correctly rejects a uniform conservativeness or accuracy ordering. The corrected simulation archive retains the stated level/increment mechanisms, known thresholds and Monte Carlo uncertainty; it does not certify finite-sample empirical coverage for fitted financial reports. |
| 1 / 307 | Additional panel selection, completeness and independence | The metadata/calendar protocol and selection manifest identify 12 eligible series and retain the two longer-maturity coupon skips for incomplete original dates. The descriptive-count output records 192 procedure-cell rows, all 48 cells complete per procedure. A freeze before these panel-model outcomes does not undo prior inspection of the original sample. The paragraph correctly calls the series related aggregate tasks with shared dealers/reporting/balance-sheet components and explicitly declines independent-institution replication. |
| 2 / 309 | Panel loss signs and adverse findings | Existing `/QR33/lower_loss_than_F=3`, `/C2_QR4/lower_loss_than_F=11` and `/Levy_L/lower_loss_than_F=19` use 48 cells each. The archived positive upper loss changes support the retained adverse QR33/C2 descriptions. These are comparisons against same-cell frozen F, not pooled currencies/units or a common independent-dealer effect. The paragraph's limited conclusion does not turn the panel into proof that all conditional models fail. |
| 3 / 311 | Identities of mature benchmark adaptations | The D1 protocol owns the original origins, mature-label windows and refit grids. Its fixed definitions are recursive simulated signed-position paths for FHS, GARCH-scaled mature peak-headroom exceedances for POT, and conditional training-response leaf distributions for QRF. The current wording identifies peak POT as an adaptation, not a literal return-innovation McNeil–Frey implementation, and does not substitute quantiles of tree means for QRF. Resource-bounded fixed choices are not asserted to cover all tuning choices or entire method families. This was a protocol/text identity check, not a new implementation or literature-theorem validation. |
| 4 / 313 | Complete-cell denominators, comparison signs and failed-cell semantics | The saved summary gives 6 complete FHS, 4 complete PEAK_POT and 8 complete QRF cells, 18 complete and 6 NA of 24 planned cells. Existing paired rows against `right_method=frozen_F` agree with the paragraph's loss directions: FHS 3 lower/3 higher, POT 1 lower/3 higher, QRF 2 lower/6 higher. NA rows have no observed full-cell loss. The paragraph correctly labels counts across related settings as descriptive and says failed cells limit method coverage rather than establish predictive inferiority. |
| 5 / 315 | Archive navigation and unseen-dealer boundary | The owning Supplement captions/routes retain the complete menu/L/panel/mature-baseline records, failures, original positive-increment mechanism and corrected sensitivities. The explicit final sentence denies independent unseen-dealer validation. It does not transform an added benchmark, a corrected simulation or an enlarged aggregate panel into external validation. |

No paragraph requires a numerical sign correction, a change in the primary comparison, a broader scientific claim or removal of an adverse/failed result.

## Limited owning-output routes

The following routes were read for interpretive identity, not rescored:

- `results/revision-20261023/round2/levy/paired-tests.csv`: all existing rows with `left_method=Levy_L` and `right_method=frozen_F`; their `source`, `horizon`, `window`, `relative_loss_percent` and `reference_strict_breaches`. The matched `levy/summary.csv` provides the L `strict_breach_count`. No DM/HLN statistic, p-value or ranking family was recomputed.
- `round2/levy-ar-correction/simulation.json`: existing `/results` labels and recorded rates for level versus increment processes, anchor and threshold-information variants. The level rate endpoint cited by the paragraph is the stored `model=level,horizon=6,phi=.98,anchor=stationary,q_information=stationary_marginal_endpoint` row, `max_exceedance_rate=.00913`; zero counts are also retained. The negative-increment row `model=increment,horizon=24,phi=-.6,anchor=zero` records `max_exceedance_rate=.05032`, `rate_minus_five_percentage_points=.03199999999999939` and `monte_carlo_standard_error=.0006912879110761304`. These are stored outputs and units, not freshly simulated or estimated quantities.
- `round2/panel/selection-manifest.json`: `status=SELECTION_FROZEN_BEFORE_MODELS`, its fixed calendar rule, eligible keys and retained skip reasons. Raw paths recorded in metadata were not opened.
- `round2/panel/descriptive-counts.json`: the three named procedure count/status/max-change summaries, `series_count=12`, `skipped_count=2`, `rows=192`, and `all_post_result=true`.
- `round2/baselines/summary.json`: `planned_cells=24`, `complete_cells=18`, `NA_cells=6`, `method_counts={FHS:6,PEAK_POT:4,QRF:8}`, and the unchanged-primary flag. `baselines/paired-tests.csv`: only saved comparison fields/statuses against frozen F were interpreted; no inference was rerun.

The Supplement was a routing/support source, not another full review sample. An initial structural inventory displayed selected headings, table captions/row counts and prose excerpts (up to 400 characters per block) within S1, S11, S12 and S13. No proof was derived, extended or independently certified from the incidentally displayed existing proof/equation summaries. Material relied on was limited to:

- S1: Table S8's same-W L comparison convention, Table S9's panel count convention and Table S10's complete-cell/NA convention.
- S11: mechanism/threshold qualifications and retained primary/secondary simulation captions and prose.
- S12: fixed-calendar panel and prospective-protocol/as-captured-path qualifications.
- S13: the named benchmark definitions, complete versus failed-cell captions and failure semantics.

The exact owning D1/D3 and prospective protocols were read for the corresponding boundaries, not as authority to execute their historical implementation checklists.

## Same inspected sample versus prospective evidence

The v6 common contract explicitly states that the evaluation archive has already been inspected, new work is post-result/exploratory, and the work is not prospective preregistration, an independent dealer validation or a new guarantee. The D3 panel protocol states that additional published aggregates share the reporting system and overlapping dealers/assets and permits no pooled independence-based inference.

The prospective-public-release protocol remains a **plan**: its lines 3 and 25 state that no prospective result is available and results require future releases plus prior report issuance. Its information-clock paragraphs distinguish economic dates from actual capture/report timestamps. The vintage amendment describes a first-actually-captured measurement path and a declared join across vintages; it expressly does not reconstruct historical publisher first-release truth, repair the historical replay or complete independent-dealer validation. Its future missed-issue/refit-NA rules are not represented here as executed functionality.

Section8 does not explicitly claim that any prospective reports have been issued or that the panel is an unseen prospective holdout. Its direct statement that none of these exercises supplies independent unseen-dealer validation is consistent with these owning records. This audit did not poll an official site, operate a capture adapter, inspect current account activity or verify whether future acquisitions later occur.

## Tau=.99 and finite ACI/SAV boundary check

**Scope distinction:** none of the six Section8 paragraphs mentions ACI, SAV, tau or .99. Their absence is not a failed result or a new finding. The following narrow owning-record check was requested as an interpretive guard; it is not a reread of other main sections or a verdict on the whole S16 appendix.

The existing `wp5-tau-summary.json` rows 3–5 are the FX primary, FX matched and Treasury primary tau=.99 slots. All are `status=NA`, `forecast_status=NA`, with `mean_difference=null` and `raw_p=null`. Their `bookkeeping_p=1` values are Holm-family placeholders, not observed null p-values or complete zero-effect tests.

The owning validation receipts distinguish the causes:

| Source / tau | Existing receipt/status | Interpretive boundary |
|---|---|---|
| FX / .99 | `wp5-v2/validation-fx_hourly-tau99.json`: `DECLARED_VALIDATION_MENU_INELIGIBLE`; candidate .01 failed with `NONCONVERGENCE`; selection is `INELIGIBLE`, failed_candidates=[.01] | The prescribed complete validation menu failed. Surviving candidates do not license a replacement/partial comparison or a financial performance conclusion. |
| Treasury / .99 | `wp5-v2/validation-nyfed_weekly-tau99.json`: `PREDECLARED_TAIL_INFORMATION`; candidates are `NOT_ATTEMPTED_TAIL_INFORMATION` | This is the predeclared minimum nominal-tail-information gate from the original validation/window sizes, not an observed loss-based exclusion or evidence of predictive failure. |

`wp5-quantile-levels.md` also fixes original versus matched F reference identities and forbids mixing absolute losses across different target levels. Nothing in Section8 overrides these NA boundaries or makes an upper-target success claim.

The existing WP2 protocol calls the wrapper **finite delayed ACI-style calibration**, with delayed/projected state updates, and explicitly imports no canonical ACI long-run or conditional-coverage guarantee. It defines headroom SAV as a maturity/target adaptation rather than literal return VaR or the full CAViaR class; bounded deterministic starts do not certify global optimality. Whole-cell validation/refit failure remains NA. The saved WP2 findings remain labeled post-result/exploratory. These limits are consistent with Section8's finite benchmark language and provide no route to universal claims.

No additional sentence or scientific-conclusion change is required within the reviewed section to preserve these boundaries.

## Fresh source identities

The 22 files below all freshly matched their blobs at the exact audited source commit. These hashes identify the current bytes consulted; they do not establish raw-data correctness, independent replication or successful remote publication.

| Source | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2` |
| `submission-jof/manuscript.tex` | `6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `v6_submission.py` | `6f96167d21ea915b7c71a0a2a80d9bab5d4beb96075e67d43ddf4db56c7f46f2` |
| `protocol/revision-v6/common-contract.md` | `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8` |
| `protocol/revision-20261023/round2-D3-panel.md` | `f2460d4302f6b49d3cef8af532aa019f051f0bdc6d5bab8957c71843e392f858` |
| `protocol/revision-20261023/round2-D1-mature-baselines.md` | `cec3a4df77c2d7f749361bdcb1a1e5e87be1f4aec460696959831a968ab873db` |
| `protocol/revision-20261023/prospective-public-release-protocol.md` | `cb5b654a7c21467b126352408b141ece781cd547b6b15b03447a5a2ef9b1c3f1` |
| `protocol/revision-20261023/prospective-vintage-amendment-20261023.md` | `299dbdd29401628cacff36186c1584c5e92d621dabe3367a7472aac0f45fd29a` |
| `results/revision-20261023/round2/panel/selection-manifest.json` | `c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858` |
| `results/revision-20261023/round2/panel/descriptive-counts.json` | `d4d3f1ebe5d6851f72f321d2a00c2c599f4903415f66580b1524a36e0b66b649` |
| `results/revision-20261023/round2/baselines/summary.json` | `cf3681e1e44758a5d239c2f1a871bf97238e566c7f7e3105cd96754c14632dce` |
| `results/revision-20261023/round2/baselines/paired-tests.csv` | `c243137ebaf54eb4acb1ae421b0051981bcfbd30f8f83fd7a6982cca4b2bb0f5` |
| `results/revision-20261023/round2/levy/summary.csv` | `d779705c3717e19f67c44ae44629fd172d09887eb0d2bd5eebcb7eb7bd010a23` |
| `results/revision-20261023/round2/levy/paired-tests.csv` | `8bbf83abefba40969e9cf78e174bd71688e57d578ca039fa1b0fce8daeb01eb5` |
| `results/revision-20261023/round2/levy-ar-correction/simulation.json` | `99c1ce198dcdb15e88ec30eccb7b9ece936042a630886e65c7a03dd412fc2a3d` |
| `protocol/revision-v6/wp5-quantile-levels.md` | `aa2bb6adf76e643818126e3ee01322c102b2b238f95cf5f62d4449a9e51bef32` |
| `results/revision-20261023/v6/wp5-tau-summary.json` | `085d2dbf7a94a13f3b1557d966848cf5f58382fa4f330dc8e221235427c71501` |
| `results/revision-20261023/v6/wp5-v2/validation-fx_hourly-tau99.json` | `acc80821319024ee04437c960cc3cb1b9792c223b88255bed5469edc8bb2f8fa` |
| `results/revision-20261023/v6/wp5-v2/validation-nyfed_weekly-tau99.json` | `b47909d0fee75aea6c0e2cbc3124b6fba38be4fab65f678e1536505e6a272926` |
| `protocol/revision-v6/wp2-aci-sav.md` | `4d1115663011753ad85c41a9b5f6bf50b100e186d9a1c6d3c8b622fa996ac2e7` |
| `results/revision-20261023/v6/wp2-findings.json` | `8841a9258bae71c4c162afc6c5efd91ff4fa2a323621db637b7f012cf1623972` |

## Action receipt and limits

The only write by this reviewer is this new `verification-loop-015-referee-B-transport.md`. No raw FX/Treasury observations, private NPZ, per-origin forecast/loss vector or account UI was opened. No analysis, statistical diagnostic, model, test, proof, simulation, source repair, manuscript/conclusion edit, protocol/state update, compilation, commit, push or publication was performed. No Claude/Cloud or cross-model review was invoked.

A previously completed loop13 helper was briefly asked for narrow record support before the parent requested no further nesting; it was interrupted and told to stop without writing. No helper output is used as evidence for this verdict. This final section review and the source reads reported here were completed by the assigned referee.

Clock observations are recorded as observations, not as a claim that idle or parallel time was spent reading. This is a bounded internal section review; it does not certify the rest of the manuscript, historical public-information availability, calibrated component reference distributions, externally valid performance, or readiness for journal submission.

**Author pending: none identified from Section8.** Existing adverse results, failed-cell meanings, prospective-plan status and independent-validation limits are retained. No fix was performed or requested.
