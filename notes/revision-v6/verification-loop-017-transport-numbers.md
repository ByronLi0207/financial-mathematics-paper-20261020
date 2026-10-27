# Verification loop 017 — Section 8 semantic numeric trace

**Verdict: PASS, 5/5 selected semantic numeric claims match their existing owning fields and static display/composition paths.** No financial-result conclusion issue was found in this bounded trace; author-pending items: none. This is an internal numeric readback, not external peer review or independent numerical validation.

## Selection fixed before output lookup

- Main source: `submission-jof/manuscript-content.json`, `sections[7]`, heading verified as **`8. Transport and robustness (RQ3)`**, six blocks indexed 0–5.
- Initial current-main read: **2026-10-23 21:44:17.066104 UTC**; SHA-256 `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2`.
- Selection record: `notes/revision-v6/verification-loop-017-transport-numbers-selection.json`, created **2026-10-23 21:44:53.888305 UTC**, before any owning result-output or generator-content lookup in this loop. Its SHA-256 is `885fb7bb690dc65201ef7d3436a54f4d9337c1cd7c583d75d95545ee82e4afc2`.
- Frame: 18 explicit semantic numeric claims, indexed in order of appearance. A range is one claim; a complete lower/higher/denominator partition is one compound claim. The rate, nominal excess and Monte Carlo SE are separate quantities. Citation years, supplement/section locators, method-name digits and horizon/window identity labels are excluded as standalone claims. The complete frame and exclusions are preserved in the immutable selection JSON.
- Seed: **2026102317**; selection rule: `random.Random(seed).sample(range(18), 5)` without replacement. Draw order: **[16, 9, 1, 8, 3]**. Verification/presentation order: **[1, 3, 8, 9, 16]**.
- The selection JSON's `output_lookup_started: false` records its state when frozen. It was not rewritten after seeing outputs.

Only the authorized note and same-prefix selection JSON are written by this loop. No scientific routine or generator was executed. Work was limited to reading saved JSON/CSV/text, checking identities/counts/signs, reproducing display formatting from stored scalars, and hashing files. No new analysis, test, model, simulation, proof, source/state/manuscript/archive edit, UI action or commit was performed.

## Selected claims and exact traces

### 1. Negative-increment AR reaches 5.032%

- Selected frame index **1**; current main pointer **`/sections/7/blocks/0/html`**; corresponding TeX line **305**.
- Owning frozen result: `results/revision-20261023/round2/levy-ar-correction/simulation.json`, **`/results/33/max_exceedance_rate = 0.05032`**. Exact row identity: `model="increment"`, `primary_design=true`, `horizon=24`, `phi=-0.6`, `anchor="zero"`, `q_information="stationary_increment_endpoint"`, `seed=20585233`, `paths=100000`. The same row records **`max_exceedances=5032`**.
- Static numeric generator: `round2_levy_ar_manuscript.py`, `augment_ar_correction`, lines 11–18. It filters primary increment rows and selects the greatest saved `max_exceedance_rate`; the four selected-family result indices are **15, 16, 32, 33**, with stored rates **0.03563, 0.04439, 0.04281, 0.05032**, respectively. No new simulation or rate estimate is made here.
- Display rule: `format(100 * stored_rate, '.4g')` returns **`5.032`**; the paragraph adds `%`. This is an observed simulated strict peak-breach frequency, not a financial-source breach rate or a forecast-loss percentage.
- Reference identity/context: the nominal comparison is the **5% oracle-threshold mechanism**, not F or QR. The owning row records `independence_premise=false`, `post_result=true`, `exploratory=true`. The main text retains its excess and SE context and explicitly withholds an empirical-coverage guarantee. No population violation is inferred from this observed maximum.
- **Result: PASS.**

### 2. Monte Carlo SE is 0.06913 percentage points

- Selected frame index **3**; current main pointer **`/sections/7/blocks/0/html`**; corresponding TeX line **305**.
- Owning frozen field: the **same precisely identified result row 33** as claim 1, **`/results/33/monte_carlo_standard_error = 0.0006912879110761304`**.
- Static generator: the same `worst` row in `round2_levy_ar_manuscript.py`, with `pct(worst, 'monte_carlo_standard_error')`. It multiplies the stored probability-scale SE by 100 and applies four significant digits. The unrounded displayed-unit value is **0.06912879110761304 percentage points**, which formats to **`0.06913`**.
- The SE is paired with the rate selected by the generator; it is not the maximum SE over another family, an endpoint-exceedance SE, or a financial magnitude. The same row's saved excess from 5% is `rate_minus_five_percentage_points=0.03199999999999939`, displayed as 0.032 in the surrounding sentence. That already reported excess remains smaller than the displayed SE; neither is turned into a new test or theorem in this loop.
- **Result: PASS.** The stored SE was read and its display conversion checked; its estimation formula was not newly evaluated.

### 3. Every included series uses the original 706-date economic grid

- Selected frame index **8**; current main pointer **`/sections/7/blocks/1/html`**; corresponding TeX line **307**.
- Owning frozen record: `results/revision-20261023/round2/panel/selection-manifest.json`. The exact eligible-record selector is **`series[status == "ELIGIBLE"].aligned_observations`**: each of the 12 values is **706**. Raw array indices are **0,1,2,3,4,5,6,9,10,11,12,13**. Each records `aligned_first_date="2013-04-03"`, `aligned_last_date="2026-10-07"`, and `missing_required_dates=0`.
- Reference identity: manifest **`economic_grid_source="original immutable PDPOSGS-B dates"`**. Eligible keys are `PDPOSMBS-TOT`, `PDPOSCS-TOT`, `PDPOSFGS-TOT`, `PDPOSTIPS-L2`, `PDPOSTIPS-G11`, `PDPOSTIPS-G2`, `PDPOSTIPS-G6L11`, `PDPOSGSC-L2`, `PDPOSGSC-G2L3`, `PDPOSGSC-G3L6`, `PDPOSGSC-G6L7`, and `PDPOSGSC-G7L11`.
- The frozen panel protocol `protocol/revision-20261023/round2-D3-panel.json` states the original 706-date calendar as its `selection_rule`. The already existing `round2_panel_run.py` line 28 obtains that calendar from the original `PDPOSGS-B.csv` dates and aligns the selected source to it. This is a static definition read; no raw-source download, alignment rerun or model run was performed.
- Static paragraph generator: `round2_panel_manuscript.py`, `augment_panel`, line 22, contains the literal original-706-date description. This claim is therefore supported by the saved alignment fields and frozen rule; it is not presented as a dynamically inferred output of `facts['rows']`.
- Adverse/skip context: manifest `series[7]` and `series[8]` are the retained `PDPOSGSC-G11L21` and `PDPOSGSC-G21` skips, each with reason **`missing required economic dates: 457`**. They are outside “every included series.” The broader raw responses have 707 observations for eligible keys, while the specified aligned calendar has 706; those are distinct counts. This is an economic-date downloaded-vintage calendar claim, not proof of historical public-release availability or measurement invariance.
- **Result: PASS.**

### 4. All 192 procedure-cell outputs complete

- Selected frame index **9**; current main pointer **`/sections/7/blocks/1/html`**; corresponding TeX line **307**.
- Owning frozen scalar: `results/revision-20261023/round2/panel/descriptive-counts.json`, **`/rows = 192`**. The static paragraph generator at `round2_panel_manuscript.py` line 22 inserts `str(facts['rows'])`.
- Direct saved-record identity check: `results/revision-20261023/round2/panel/summary.csv` has **192 records and 192 distinct `(series_key,horizon,window,method)` identities**, all with `status="COMPLETE"`. Existing axes are 12 included keys, H6/H24, W52/W260 and four procedures. Each procedure has 48 COMPLETE records: **frozen_F 48; Levy_L 48; QR33 48; C2_QR4 48**.
- Reference identity: **192 includes the 48 frozen-F reference outputs**; it does not mean 192 new conditional-model fits or 192 independent replications. The named comparison field in this archive is `percent_vs_frozen_F`, with same series/H/W identity, and the frozen protocol uses the same scheduled refits.
- Adverse context is retained in the existing `descriptive-counts.json`: QR33 has **3 lower / 45 higher** loss cells, C2_QR4 **11 lower / 37 higher**, Levy_L **19 lower / 29 higher**, each over 48. Numerical completion is not a favorable result. The two calendar skips remain in the selection manifest; they are not failed procedure rows silently counted COMPLETE.
- **Result: PASS.** The count/status/identity check reads existing rows; it computes no new financial score.

### 5. PEAK_POT: 1 lower-loss and 3 higher-loss out of 4 complete comparisons

- Selected frame index **16**; current main pointer **`/sections/7/blocks/4/html`**; corresponding TeX line **313**, where the method label is escaped as `PEAK\_POT`.
- Owning frozen comparisons: `results/revision-20261023/round2/baselines/paired-tests.csv`, exact selector **`left_method == "PEAK_POT" AND right_method == "frozen_F" AND status == "OK"`**. The zero-based CSV data-row indices are **8,20,32,44**. The reference identity is matching **source, horizon and window**, with the frozen F clock; negative `relative_loss_percent` means lower PEAK_POT loss than that F.

| Exact contrast identity | Pair status | Saved `relative_loss_percent` | Direction |
|---|---|---:|---|
| `fx_hourly-h6-w2880-PEAK_POT-minus-frozen_F` | OK | 3.2685047964041343 | Higher loss |
| `fx_hourly-h24-w2880-PEAK_POT-minus-frozen_F` | OK | 10.607749231842803 | Higher loss |
| `nyfed_weekly-h6-w260-PEAK_POT-minus-frozen_F` | OK | -10.348774383704525 | Lower loss |
| `nyfed_weekly-h24-w260-PEAK_POT-minus-frozen_F` | OK | 32.08988277479678 | Higher loss |

- Static generator: `round2_baselines_manuscript.py`, lines 50–53, filters exactly those method/reference/status fields and counts `<0`, `>0` and the selected row total. The saved signs are one negative, three positive and no equality among these four rows. `baselines/summary.json` independently records **`/method_counts/PEAK_POT = 4`** complete method cells; this is consistent with the selected pair denominator.
- The other four planned PEAK_POT/F rows remain **NA_CELL**, not favorable, adverse or zero-loss observations: data-row indices **2 and 14** are FX W720 H6/H24 with the retained GARCH convergence/admissibility failure; indices **26 and 38** are Treasury W52 H6/H24 with the retained minimum-tail-size exclusion. Corresponding `baselines/summary.csv` PEAK_POT row indices **1,7,13,19** retain `status="NA"`, blank full-sample loss, and issued-before-failure counts **240,240,0,0**. Partial outputs are not used in the four-comparison denominator.
- The complete adverse cells above are all retained. The source units are FX USD and Treasury USD millions; only directions/counts are summarized here, not pooled losses. The main text calls the counts descriptive across related histories/targets and does not treat failed cells as evidence of predictive inferiority.
- **Result: PASS.**

## Current static composition and source continuity

The current `v6_submission.py` composition starts by deep-copying `notes/revision-v6/v5-manuscript-before.json`; it preserves untouched old source bindings. The selected Section 8 blocks retain `_source` pointers to `manuscript/revision-v3/paper-content.json` **`sections[7].blocks[16]`**, **`[18]`**, and **`[24]`**, whose current file hash matches their embedded `3a355…` source binding.

The current V5 and V4 snapshots contain the same selected numeric text at Section 8 blocks 0,1,4. The static V4 composition explicitly maps robustness source blocks 16,18,20,23,24 into its transport section (`v4_submission.py` lines 114–117); the V5 composition copies its frozen V4 snapshot; the V6 composition copies its frozen V5 snapshot. The owning original numeric paragraph generators are the three `round2_*_manuscript.py` functions identified above. This trace distinguishes the current snapshot-preserving composition from the original numeric insertion/formatting functions. None of these functions was invoked in this loop.

The current JSON and corresponding TeX retain the five selected values/quantities and their directions. No claim is made here about unselected Section 8 values, the paper's scientific adequacy, the validity of a simulation mechanism, independent replication, or prospective performance.

## Time, currentness and fingerprints

Repository branch was observed as `revision-v4-jof`. HEAD at selection was `14262bd68ac5e18c5daaf961c0730a43442e4957`; another coordinator's concurrent work advanced observed HEAD to `543e9ad71cd76b098c44a5c161305f095c43e8c5` by **2026-10-23 21:46:43 UTC**. This numeric-verification worker made no commit. The initially observed tracked `notes/revision-v6/state.json` modification was pre-existing/concurrent; it was not read for evidence or modified here. The final tracked diff listing at that time was empty.

The main source still matched the pre-output-lookup selection hash at **2026-10-23 21:46:28 UTC**. Owning-source and generator fingerprints were captured at **2026-10-23 21:46:09–21:46:28 UTC**; a post-write readback checks them again. Hashes bind this note to saved local evidence only.

| Source | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `6b5c15d930f88431140fb84f7042ec83d55d63e72620a5ac18b4796ea606ded2` |
| `submission-jof/manuscript.tex` | `6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72` |
| `notes/revision-v6/v5-manuscript-before.json` | `2134c14e0b7e9ab3a3c20683251cb99d89bae64541d30ea804296bccd6f10ac7` |
| `notes/revision-v5-novelty/v4-manuscript-before.json` | `6aeb3b36ffc23a9218670b708cc85a3bcc02d8882822ea8b922869fed487f646` |
| `manuscript/revision-v3/paper-content.json` | `3a35590321c752186ab6dbfb46d115b725cdad3528b0dae73cf2c209f555dcb7` |
| `v6_submission.py` | `6f96167d21ea915b7c71a0a2a80d9bab5d4beb96075e67d43ddf4db56c7f46f2` |
| `v5_submission.py` | `cd37ce62a266c86d0491ce3dd8b84f745e62c7f7de5f0014a15cfe0f0dd66252` |
| `v4_submission.py` | `11725bfe7c8922fb08ad8c6acb579bf53f890ab82967c52368c5f1f589022852` |
| `round2_levy_ar_manuscript.py` | `0cd6591b5e762075a07da8b24d756e6f93ca93126374b833517bac7970a5a89a` |
| `round2_panel_manuscript.py` | `bf765d3f35d0f20d600a3118d62b9e89452325a0a67a5bec089ac9a428b0d06f` |
| `round2_baselines_manuscript.py` | `f340e2024957f01cb111a52d9769fca1ff43d97e02a97cf6c2bc4fd965c67b29` |
| `results/revision-20261023/round2/levy-ar-correction/simulation.json` | `99c1ce198dcdb15e88ec30eccb7b9ece936042a630886e65c7a03dd412fc2a3d` |
| `results/revision-20261023/round2/panel/selection-manifest.json` | `c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858` |
| `results/revision-20261023/round2/panel/descriptive-counts.json` | `d4d3f1ebe5d6851f72f321d2a00c2c599f4903415f66580b1524a36e0b66b649` |
| `results/revision-20261023/round2/panel/summary.csv` | `34134445a00354dcce3dc43de4c2adada7f2ea5403212558f90ef3480ee810f9` |
| `results/revision-20261023/round2/baselines/summary.json` | `cf3681e1e44758a5d239c2f1a871bf97238e566c7f7e3105cd96754c14632dce` |
| `results/revision-20261023/round2/baselines/summary.csv` | `dc10cdb68d54810dd9b457eac5d948a733fbc7e79948571e84e8e255c135de95` |
| `results/revision-20261023/round2/baselines/paired-tests.csv` | `c243137ebaf54eb4acb1ae421b0051981bcfbd30f8f83fd7a6982cca4b2bb0f5` |
| `protocol/revision-20261023/round2-D3-panel.json` | `bd992316d679080c792acfcf4069610613774e7ce8727eef6f8944ed18812500` |
| `round2_levy_ar_correction.py` (static excerpts/search only) | `bbe4730e9cf02a599b9f2f6510e83250a14d9ac09306b56f653e14a04d1aceec` |
| `round2_panel_sources.py` (alignment route search only) | `cfadcade45ce726c4f19f691ac515e966294f8afffaca9332d129419545464a6` |
| `round2_panel_run.py` (static definition excerpts only) | `e3c0575dc50e3c9dc51395a43b1bd7daf06972395a4aaf4552713967146d76e9` |

The numeric checks above use existing fields and exact selectors, with display arithmetic/counting only. The 5/5 match verdict does not convert hash integrity or source continuity into independent scientific validation.
