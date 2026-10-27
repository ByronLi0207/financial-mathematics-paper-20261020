> **Final protocol supersedes preliminary suggestions below:** all six validation candidates are required for both regression methods; D3 is the conjunction of both original FX W2880 horizons H6 and H24. See protocol/v12/loss-decomposition-design.md at9679e15. Earlier audit proposals are retained as chronology, not execution settings.

# v12 split and diagnostic design audit

Audit date: 2026-10-25. Scope: F1–F3 in `notes/v12/supervisor-task.md`.
This is a read-only source/design audit, not the three executable protocols.
Each final protocol must be committed separately before its pilot or formal
run. No new fit, forecast, target construction, loss evaluation, data download,
branch mutation or old-v3 write was performed for this audit. Timestamp arrays,
existing metadata and saved scalar means were read. The only output is this
file. No Claude or cross-model review was used.

## 1. Existing inputs and exact clocks

All intervals below are zero-based and inclusive. Define the known issue
magnitude `B_t=|N_t|`, sampled peak
`Y_t=max(|N_t|,...,|N_(t+H)|)`, and own-anchor headroom `Z_t=Y_t-B_t`.
At a refit `r`, the mature training origins are
`r-H-W+1,...,r-H`, so the last training label ends exactly at `r`.
Within each declared segment beginning at `a`, the original schedule is
`r(t)=a+d*floor((t-a)/d)`. Validation and evaluation start separate refit grids.
Preserving only `W` and `H` without preserving `a` and `d` would change the
comparison.

The implementation sources are `conditional_features.py:35,94,102`,
`study_core.py:229`, `v8_mechanism_mc.py:95`,
`empirical_headroom.py:36`, and `v10_menu.py:22`.

### Input ownership and loaders

| Family | Exact existing input | Reader/alignment | Model clock and features |
|---|---|---|---|
| CFTC | `results/v10/cftc/sources/s00.npz` through `s16.npz`, indexed by `results/v10/cftc/sources.json` | `run_v10_cftc.py` worker reads `position` and `model_dates`; retain `actual_dates` for display | Monday 00:00 weekly labels; `short_scale=6`, `long_scale=26`, nominal gap 604800 s; feature `valid_from=26`; `d=13` |
| Treasury bills | `data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv` in the current root | `conditional_sources.load_source(...,'nyfed_weekly',expected_sha256=...,expected_bytes=...)` | Original economic dates, unchanged order; same weekly feature settings and `d=13` |
| Additional NY Fed panel | Existing v9 copies `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/<key>.csv` | `round2_panel_sources.align_source(raw,key,grid)` with the 706 dates from the Treasury-bill CSV | Restrict to the unchanged 706-date Treasury grid; same weekly feature settings and `d=13` |
| Hourly FX | Existing v9 copy `/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/1hourNetPositionsKaggle.csv` | `conditional_sources.load_source(...,'fx_hourly',expected_sha256=...,expected_bytes=...)` | Original source-naive timestamps and gaps; `short_scale=24`, `long_scale=168`, nominal gap 3600 s; feature `valid_from=168`; `d=24` |

The current root's old configured FX/private-panel raw locations do not exist.
Use the already documented v9 copies above, or make new private copies after
the protocol commits; do not invoke an old acquisition/preparation driver.
`notes/v10/loss-input-inventory.json#/raw_sources` enumerates all 14 existing
raw files. Its 407 `minimum_core_private_copy_manifest` mappings point to the
current `.scratch/v10/loss-inputs/` copies for existing trace reuse. Their old
original-path fields do not require reopening or writing v3. The date audit
independently verified FX, Treasury and all 12 panel file hashes against the
original source specification/selection manifest.

FX has 18,576 rows, from `2014.02.05T01:00:00.000` to
`2017.01.24T00:00:00.000`; 1,286,391 bytes; SHA-256
`b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`.
Treasury has 706 rows, `2013-04-03` through `2026-10-07`; 23,315 bytes;
SHA-256 `9f9f942ea8775a15f2e839cfe489f2e5113659ac37b375282d93bd6379be7cdb`.
Panel raw files contain 707 rows through `2026-10-14`, but the frozen analysis
uses only the 706 Treasury dates through `2026-10-07`. Do not silently extend
the panel sample by one week.

The 12 panel keys, in the saved selection-manifest order, are:

```text
PDPOSMBS-TOT, PDPOSCS-TOT, PDPOSFGS-TOT,
PDPOSTIPS-L2, PDPOSTIPS-G11, PDPOSTIPS-G2, PDPOSTIPS-G6L11,
PDPOSGSC-L2, PDPOSGSC-G2L3, PDPOSGSC-G3L6,
PDPOSGSC-G6L7, PDPOSGSC-G7L11
```

Do not add the two previously skipped keys `PDPOSGSC-G11L21` and
`PDPOSGSC-G21`. The owning selection file is
`results/supervisor-20261023/e5/inputs/panel/selection-manifest.json`.
Its alignment policy requires every original economic date exactly once, with
finite numeric values; it does not splice, fill or impute.

CFTC has the same `N=877` complete weekly observations in each saved array.
The first actual date is `2010-01-05`, the last `2026-10-20`; corresponding
model dates are `2010-01-04` and `2026-10-19`. Source order is fixed:

```text
s00 044601; s01 043602; s02 042601; s03 045601; s04 020601;
s05 099741; s06 1170E1; s07 097741; s08 096742; s09 095741;
s10 090741; s11 232741; s12 33874A; s13 240743; s14 092741;
s15 098662; s16 112741
```

Each source array's size and SHA-256 were checked against `sources.json`.
Only its stored timestamp arrays were decoded for the new F2 date mapping;
no financial labels or losses were computed.

### Existing segment grids to retain

| Family/period | H | W | Validation origins / dates | Evaluation origins / dates | n evaluation |
|---|---|---|---|---|---:|
| CFTC, all 17 | 6 | 52,260 | 553–604; actual `2020-08-11`–`2021-08-03` | 611–870; actual `2021-09-21`–`2026-09-08` | 260 |
| Treasury, original | 6,24 | 52,260 | 329–380; `2019-07-24`–`2020-07-15` | 405–681; `2021-01-06`–`2026-04-22` | 277 |
| Panel, each of 12 | 6,24 | 52,260 | Same 329–380 / Treasury dates | Same 405–681 / Treasury dates | 277 |
| FX, original | 6,24 | 720,2880 | 10463–11902; `2015-10-08 00:00`–`2015-12-30 23:00` | 11927–18551; `2016-01-01 00:00`–`2017-01-23 00:00` | 6625 |
| FX, early 2015, for F3 | 6 | 2880 | 7535–8974; `2015-04-21 00:00`–`2015-07-13 23:00` | 8999–10438; `2015-07-15 00:00`–`2015-10-06 23:00` | 1440 |

The original Treasury/panel and FX grids preserve the common `H*=24` buffer
even for `H=6`: 24 issue origins are omitted between segments. CFTC instead
preserves its original six-origin buffer. Do not replace any of these with
a newly H-specific split.

Exact latest label dates in the preserved grids:

| Family/period | Last validation label, H6 / H24 | Last evaluation label, H6 / H24 |
|---|---|---|
| CFTC | `2021-09-14` / outside scope | `2026-10-20` / outside scope |
| Treasury/panel | `2020-08-26` / `2020-12-30` | `2026-06-03` / `2026-10-07` |
| FX original | `2015-12-31 05:00` / `2015-12-31 23:00` | `2017-01-23 06:00` / `2017-01-24 00:00` |
| FX early 2015 | `2015-07-14 05:00` / not used in F3 | `2015-10-07 05:00` / not used in F3 |

Owning sources: `protocol/revision-20261022/study-spec.json`,
`round2_panel_run.py:33–46`, `results/v10/cftc/splits.json`,
`protocol/supervisor-20261023/r6-design.md` Section 2, and the date mappings in
`notes/v10/loss-input-inventory.json`. Raw timestamp readback agrees.

## 2. Method behavior that must remain fixed

Use six candidates `{0.001,0.01,0.1,1,10,inf}` for both QR33 and QR4.
`inf` is a string dispatch to the exact ordinary empirical quantile `I`, not
an infinite numeric value passed into the ridge solver. In the inherited
v10 selector, exact equal validation means favor the stronger penalty,
including `inf`; QR33 requires all six completed validation candidates;
QR4 selects among completed candidates while retaining every failed one.
The F1 decomposition still requires all five finite evaluation candidates to
be complete, because its oracle is the minimum over that complete finite menu.
Do not silently replace it with a minimum over successful candidates.

Finite QR33 uses all 33 training-standardized predictors. QR4 uses columns
`[25,0,26,27]`, with its inherited training mean/population-SD arithmetic.
Both fit training headroom divided by
`s=max(mean(Z_train),1e-6*mean(|N_train|),1e-12)`; the intercept is unpenalized.
The solver minimizes

```text
(1/W) sum_i rho_tau(Z_i/s - beta0 - X_i' beta)
    + (lambda/2) ||beta||_2^2.
```

The issue capacity is `B_t+max(0,s*(beta0+X_t'beta))`.
Do not replace the QR4 transform with a new reduction, pool normalization
across segments, warm-start a different design, change numerical tolerances,
or fit on unfinished labels.

Relevant exact paths: `v10_menu.py:19,22,66`,
`v8_mechanism_mc.py:95–173`, `conditional_quantile.py:1–10,166`, and
`conditional_study.py:205` (the original score is hard-coded to 19/20).
Generic-tau work therefore needs an isolated v12 adapter for both forecasts
and scoring; passing a tau only to the final score is insufficient.

## 3. F1 grid, decomposition and prediction denominators

Full F1 scope is 90 source/H/W geometries:

| Family | Geometries | Two-method decomposition rows |
|---|---:|---:|
| CFTC: 17 contracts × H6 × W52,W260 | 34 | 68 |
| Panel: 12 series × H6,H24 × W52,W260 | 48 | 96 |
| Treasury: H6,H24 × W52,W260 | 4 | 8 |
| FX original: H6,H24 × W720,W2880 | 4 | 8 |
| Total | 90 | 180 |

For one geometry and one method, let `L_F` be mean evaluation loss of matched
F, `L_A` be mean evaluation loss of the validation-selected candidate, and
`L_O=min_{lambda in {.001,.01,.1,1,10}} L_lambda` using the five complete finite
evaluation means. Evaluation oracle exact ties favor the stronger finite
penalty for a unique recorded ID, without changing `L_O`.

```text
E = L_A - L_F                 actual excess loss
S = L_A - L_O                 selection component
G = L_O - L_F                 finite-menu diagnostic gap
E = S + G.
```

Keep the native-unit means and differences. Where `L_F>0`, display percentage
points `100*E/L_F`, `100*S/L_F`, `100*G/L_F`; they add to the same relative
actual loss. Where `L_F=0`, these percentages are undefined, but raw differences
remain defined. Do not manufacture infinities or delete the row.
Use the same trace/mean for the selected evaluation candidate as for its menu
entry; do not refit it a second time. An infinity-selected actual candidate can
beat every finite candidate, so `S<0` is legitimate. It must remain signed in
the table and figure. If the actual selected candidate is finite and all five
evaluation candidates are complete, `S>=0` follows from the definition; a
negative value there indicates a trace/mean identity problem, not a quantity
to clamp away.

The oracle uses evaluation outcomes. It is an infeasible diagnostic benchmark,
not a selectable forecasting procedure and not a test of whether every possible
conditional model lacks information. A negative finite-menu gap only establishes
that one of these five fitted candidates beats this matched F on this period.
A positive gap establishes the opposite for this finite fitted menu. The term
"signal gap" must carry this limited interpretation.

Primary D1 and D2 use QR33 only. QR4 repeats the screen as a separately labelled
sensitivity. The fixed primary denominator is 41: 17 CFTC W52/H6 cells plus
12 panel series × two horizons at W52. Treasury is deliberately outside this
specified prediction denominator; it remains in all reporting. Do not pool
QR33/QR4 into 82 primary observations or add W260 after seeing outcomes.

* D1 cell support: `G>0`, strict. Overall support requires at least 21 of 41.
* D2 cell support: `E>0 and S>E/2`, both strict. `E=0` or `E<0` is a completed
  non-supporting cell, not a zero denominator to delete. Report `S/E` only for
  `E>0`; leave it undefined otherwise. Negative `S` remains visible and cannot
  support D2 when `E>0`.
* Missing/failed cells remain in denominator 41. If `s` completed cells support
  and `u` are unknown, the support fraction is bounded by `[s/41,(s+u)/41]`.
  `s>=21` supports; `s+u<=20` does not support; otherwise indeterminate.
  Always print `s`, completed non-supporting count, `u`, and both bounds.
* D3 primary is QR33 on FX original H6/W2880: `G<0`, strict. QR4 and H24/W2880
  are separate sensitivities. Missing primary input makes D3 indeterminate;
  it cannot be rescued by the other method/horizon. Do not write that a
  causal or generally exploitable conditional signal has been established.

Per-source summaries must first express each complete cell relative to its
own matched F. CFTC medians are per W and method across the same fixed 17
contracts; panel medians are per H/W/method across the same fixed 12 series.
If presenting a 24-cell W52 panel median or a 41-cell primary screen, label it
as an equal-cell descriptive aggregation. Never pool raw contract counts,
USD and USD millions, or treat related series/methods as independent samples.
Use signed stacks for `S` and `G`, with negative components extending below
zero and an explicit total marker; an ordinary positive-only stacked bar can
visually hide cancellation. Preserve failed/not-run rows as labelled slots.

## 4. F2 validation length with unchanged final evaluation

Let `N` be the number of existing common weekly records, `H=6`, `E_n=260`,
and `V` either 52 or 156. Freeze

```text
evaluation_first = N-H-260
evaluation_last  = N-H-1
validation_last  = evaluation_first-H-1
validation_first = validation_last-V+1.
```

This retains the original H6 maturity gap. "Immediately before evaluation"
means the latest permissible validation block before this fixed gap, not a
block ending the week before evaluation with unfinished validation labels.
With `N=877`:

| Quantity | V52 | V156 |
|---|---|---|
| Validation indices | 553–604 | 449–604 |
| Model dates | `2020-08-10`–`2021-08-02` | `2018-08-13`–`2021-08-02` |
| Actual position dates | `2020-08-11`–`2021-08-03` | `2018-08-14`–`2021-08-03` |
| Last validation target ends | 610, actual `2021-09-14` | Same |
| Initial W52 training origins | 496–547 | 392–443 |
| Initial W260 training origins | 288–547 | 184–443 |
| Evaluation | 611–870; 260 origins | Identical |

The validation starts differ by 104=8×13 records, so their overlapping
validation refit clocks agree exactly. Evaluation always restarts at 611
with `d=13`; different choices of V affect lambda selection, not the
evaluation refit clock or labels.

Whole-contract eligibility must be determined before fits from input identity,
finite observations, chronology, complete H6 labels and history for *both* W
values and *both* validation lengths, for both QR procedures. The binding
condition is the earliest V156/W260 training origin:

```text
v156_first-H-Wmax+1 >= feature_valid_from=26
N-693 >= 26, equivalently N>=719.
```

All 17 saved arrays have N877 and earliest origin184>=26; none is excluded by
this geometry. If any source fails the complete predeclared input check,
exclude that entire contract from all F2 W/V/method comparisons, report its
reason before fitting, and freeze the remaining fixed K. Do not exclude a
contract because its solver or forecast later fails. Later failures are
failed cells and remain in denominators. No original contract is replaced.

There are `K*2W*2V*2methods=8K` selected conditional method cells (136 when
K17); F has only `K*2W` distinct evaluation traces, because V does not change
F. Reuse exact-identical evaluation predictions by W/method/lambda, and
reuse overlapping validation reports only when the complete segment/refit
schedule and all transforms are demonstrably identical. Reuse is a byte/clock
identity optimization, not a successful-result fallback.

Proposed conservative V1/V2 specification, to make explicit in the final
protocol: primary QR33, QR4 sensitivity; assess each W separately and require
both W screens for an overall positive statement. For V1, let
`M_(V,W)=median_k[100*(L_(A,V,k,W)/L_(F,k,W)-1)]`; require
`M_(156,W)<=M_(52,W)-5` percentage points at each W. This is a difference of
cross-contract medians, not the median of paired differences; show the latter
only as a separate diagnostic. For V2, require the count selecting `inf` under
V156 to be strictly larger than under V52 at each W, each count divided by the
same K. Missing required means/selection receipts do not produce a complete
median or a positive screen. Print the failed slots rather than use a
successful-subset denominator. Resource/solver failures do not alter K.

## 5. F3 tau grids and saturated historical rank

Use exact rational tau values 9/10 and 99/100. Only F and QR33 are requested;
QR33 retains the six-point menu and exact stronger-penalty tie rule, including
ordinary I at `inf`. Retune lambda at each tau on that tau's unchanged
validation segment, then freeze before evaluating it. Do not reuse a .95
selected penalty as though it were a .99 validation choice.

Freeze the v12 historical convention as

```text
j_F(m,tau)=min(m, ceil((m+1)*tau)),
j_I(m,tau)=ceil(m*tau).
```

The cap at m is an explicit v12 sensitivity convention. The old
`empirical_headroom.py`, `study_core.CellSpec` and
`v6_tau.historical_f_tau` reject an unavailable corrected rank instead;
leave those archived engines unchanged and implement the declared convention
only in the v12 adapter. All .95 requested windows have available ranks, so
this saturation leaves their historical F reports unchanged. No distribution-
free coverage guarantee follows from saturation.

| m | tau | corrected raw rank | v12 F rank | ordinary I rank |
|---:|---:|---:|---:|---:|
| 52 | .90 | 48 | 48 | 47 |
| 52 | .99 | 53 | 52 (historical maximum) | 52 |
| 260 | .90 | 235 | 235 | 234 |
| 260 | .99 | 259 | 259 | 258 |
| 2880 | .90 | 2593 | 2593 | 2592 |
| 2880 | .99 | 2853 | 2853 | 2852 |

At W52/tau.99, F and the `inf` candidate I are identical under this explicit
convention. Strict wins then exclude exact ties. Do not use an old rank-
availability/tail-count admission screen to suppress these requested cells:
the user specifically requests the small-window .99 maximum rule. Report
the limited nominal tail information as a limitation, not an outcome-based
exclusion. The old v6 tau worker used a different menu/admission design and
cannot simply be replayed as the v12 experiment.

F3 contains, per tau, 34 CFTC geometries, one Treasury primary H6/W260 geometry,
and two matched FX H6/W2880 periods. Thus 37 comparisons per tau, 74 across
both tau values, and 148 distinct F/QR33 selected-method rows before accounting
for exact shared traces. Preserve the same original/early FX segments in
Section 1, including their original 24-record buffer and d24.

"Matched FX" here means F/W2880/d24 against QR33/W2880/d24. It does not mean
the old primary's rolling F/W720/d1. The original primary and the early-2015
replication using that shorter rolling reference remain separate, unchanged
results. The overlapping full-prefix backcast beginning at index3071 is not
a third independent period and is outside this requested F3 grid.

* Q1: at tau.99, at least 29 of the fixed 34 CFTC contract×W cells must have
  `L_F<L_QR33`, strict, to meet the suggested 29/34 benchmark. Missing cells
  retain the denominator; use lower/upper count bounds for supported,
  not-supported or indeterminate status. The .90 fraction is descriptive.
* The saved .95 `results/v10/cftc/summary.json#/predictions/T1` reports 29/34
  for `min(F,I)`. Reading the saved scalar means confirms that F itself also
  strictly beats QR33 in exactly the same 29 cells; there are no differing
  cells. This is a saved-scalar comparison, not new evaluation.
* Q2: QR33 must have strictly lower .99 evaluation mean than its matched F in
  each of the two specified FX periods. State both contrasts separately;
  either missing result makes the combined screen indeterminate, and a
  reversal in either completed period prevents an overall positive claim.

## 6. Predetermined resource decisions and failure handling

The final committed protocols, not the present audit, must freeze the exact
projection formula, pilot scope, thresholds, task ordering and degrade ladder.
The following is a conservative implementable recommendation that avoids
outcome-based choice:

1. F1 pilot: use the first saved CFTC source `044601`, both W values, both QR
   methods, all six candidates, and the complete existing segments. The pilot
   begins only after F1's separate design commit. Inspect timing and completion
   only for resource planning; do not choose scope from estimated accuracy.
   Preserve the pilot as the first once-attempted cells, and reuse its complete
   reports in the formal inventory so "pilot" does not become a numerical
   retry. State whether its elapsed time is included in the formal cap; the
   stricter recommendation is one 3600-second budget from the first pilot fit.
2. Before launch, fix a timing projection such as 1.5 times the pilot's measured
   per-refit costs, weighted by planned QR33/QR4 finite refits and source clock,
   plus a fixed 60-second reserve. The factor/reserve are design choices and
   must not be changed after timing is observed. Five finite candidates require
   actual QR fits; inf/F are empirical reports, not additional ridge fits.
3. F1 ladder, in the user's order: full 90 geometries → omit all FX (86) → also
   omit all panel W260 (62). Retain every omitted planned row with a
   `NOT_RUN_RESOURCE_PLAN` reason. Do not omit a particular poorly performing
   contract, method, horizon, or lambda. If even the 62-geometry core projects
   over budget, run the fixed queue to the deadline, report all unfinished
   cells, and allow prediction status to become indeterminate; do not invent
   a further outcome-driven scope reduction.
4. Recommended F1 queue after the saved pilot: remaining CFTC in saved source
   order, panel W52 in saved-key/H order, Treasury in H/W order, panel W260,
   then FX. Within a geometry use QR33 then QR4; finite lambdas ascend, then
   inf. The ladder decision is recorded before remaining formal cells begin.
5. F2 cap is 2400 seconds; F3 cap is 1500 seconds. To protect F4 as requested,
   any planned scope compression should be recorded before the relevant run.
   A defensible F2 fallback keeps all K contracts and both W/V values for
   primary QR33, and marks the entire QR4 sensitivity block not run. A
   defensible F3 fallback first omits the entire .90 block, preserving .99
   CFTC and both FX periods for Q1/Q2. Retain all original planned slots and
   reasons. No alternative reduction should be selected from observed losses.
6. At a runtime deadline, stop unfinished work and retain complete earlier
   cells. A numerical failure makes the entire required decomposition/selected
   method cell failed; no partial mean, second attempt, changed tolerance,
   substitute lambda or successful-subset oracle. Cache both failed and
   complete segment attempts so sharing cannot silently retry failures.

For an implementation cost check, the full F1 design has 35,160 finite ridge
refits if both methods evaluate all five finite candidates on both segments:
CFTC 8,160; panel 12,480; Treasury 1,040; FX 13,480. These are geometry counts,
not observed timings. They follow `ceil(n_validation/d)+ceil(n_evaluation/d)`
per finite candidate/method. This makes the fixed resource ladder material.
It is inappropriate to time only the old selected-candidate evaluation and
multiply by the number of source cells.

## 7. Source seals and implementation cautions

These input identities were read in this audit:

| Path | SHA-256 |
|---|---|
| `protocol/revision-20261022/study-spec.json` | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |
| `results/v10/cftc/sources.json` | `f15fae76ccccaec4c7831f259a19ac15c977a301d20ab95a16f1eac6a0bf0b87` |
| `results/v10/cftc/splits.json` | `0d2fd6175b049f49d06a5fa845dabaaa5ad4bda43760eb82529255e434b28198` |
| `results/v10/cftc/eligibility.json` | `0bacfb63a09a43f3f80832afafce403bdd824a6b48279bcf698d842d389943bf` |
| `results/supervisor-20261023/e5/inputs/panel/selection-manifest.json` | `c31f1452e31b5470ff99122418d6ba08d7d3e9c83fca0d19f116c179eb252858` |
| `notes/v10/loss-input-inventory.json` | `2f10465195e774540d9a49079de37d4e6a56d0e22be634241b1d2a315b08abb2` |

The present note does not authorize experiments before the separate design
commits. No result here establishes independent replication or a new financial
holdout. F1 is a post-result finite-menu diagnosis; F2 and F3 are post-result
sensitivity checks. Existing FX inspection, related panel series, economic-date
downloaded-vintage replay and surviving complete-history CFTC selection remain
limitations regardless of the new screens.
