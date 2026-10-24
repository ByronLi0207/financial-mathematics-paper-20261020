# Verification loop 021: five seeded Section 10 numerical claims

**Status: PASS for the five selected claim traces. Necessary conclusion-changing issue / author pending: none identified.**

Current main section first read: 2026-10-23T22:00:01.271069+00:00.
Selection frozen before result lookup: 2026-10-23T22:00:34.836674+00:00.
Display/source verification observed: 2026-10-23T22:02:16.663144+00:00.
Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.

## Actual working candidate and exact scope

This round reads the current main `submission-jof/manuscript-content.json` → `/sections/9`, headed **10. Interpretation and limitations**, all nine blocks for the sampling frame. Corresponding TeX: `submission-jof/manuscript.tex`, lines **340–358**. The five selected numerical claims occur in blocks 0 and 6. Other claims in the section provide context and are not represented as five additional successful checks.

Observed HEAD at initial and source verification reads:
`61a3e3c143d027f9c8b814ddf84cd711474db220`.

The current whole manuscript JSON, TeX and v6 generator are a **pending language-only working candidate** associated with the root's Section7 edit. Their actual hashes are recorded below. They are **not asserted to equal HEAD**; the direct whole-JSON equality check returned false. A separate structural comparison confirms that **Section10 itself is unchanged from the observed HEAD**.

Section10 canonical identity (UTF-8 JSON, ensure_ascii=False, sorted keys, compact separators):
`f3b34dd4bc355b72c8eba5588138500a2ceb224cfbc48c184411fb3911965029`.

Exact UTF-8 TeX lines 340–358, original line endings:
`953c146fc3d60ffbef96e7659506e52f09fb527544fd5be83254ced037086283`.

No manuscript/source/state/result was edited by this auditor. No analysis, test, proof, model, simulation, raw-vector read, project-code import/execution, UI operation, commit or nested subagent was used. The only permitted writes are this note and its selection JSON. This is a frozen-output/static-rule readback, not independent replication.

## Reproducible semantic sampling frame

The frame was built from all nine blocks in first-appearance order before looking up any output in this round. It contains 22 empirical/design/date/cardinality statements. A complete range, ratio or paired-dimension statement is one unit; its context/denominator is retained with it. Citation year 2008 and Supplement numbers are navigation/bibliography identifiers, not eligible result claims. The generic zero-crossing qualification does not assert a particular observed count.

The actual selector was:

```python
random.Random(2026102321).sample(range(22), 5)
# [0, 16, 4, 15, 3]
```

The full ordered frame was saved before result lookup in `verification-loop-021-limitations-numbers-selection.json` (5,488 bytes; SHA-256 `f84db855d51e8d064cb9dbcbd46c70abe52b5614869f0dcea6aecc304d4b6405`). There was no replacement draw.

| Selected frame index | Current block | Numerical claim |
|---:|---:|---|
| 0 | 0 | 25 level coordinates span current observation through 24 weeks |
| 16 | 6 | Mean absolute projected capacity change 136.8–832.3 source USD millions across four cells |
| 4 | 0 | At most 28 varying columns / 29 potentially predictive coefficients before other collinearity |
| 15 | 6 | Standardized response-normalized slope norm range 0.001497–0.01937 |
| 3 | 0 | 33 predictors plus intercept = 34 nominal coefficients |

## Exact five traces

### 1. Level-coordinate span: 25 coordinates through lag 24

Direct existing output: `results/revision-20261023/treasury-feature-audit.json`.

```text
/lagged_level_coordinates = 25
/max_lag_weeks = 24
```

Static owning feature rule: `conditional_features.py:44` allocates 33 coordinates; line 53 uses `for lag in range(25)` and stores the signed level at each lag. Thus the relevant coordinates are current level and lags 1 through 24, not 25 positive lags. The existing Treasury audit supplies the weekly-source unit interpretation.

Static manuscript connection: `v3_additions.py:40` reads this audit, and line 43 inserts the two exact field strings into the limitation paragraph. The current paragraph's inherited numerical fields agree.

**Display required:** direct integers only. **Result: PASS.**

### 2. Projected capacity-change range: 136.8–832.3

Direct source field in each of the four existing Treasury selected-fit receipts:

`/aggregate_projected_native_slope_contribution/mean_absolute`.

All four receipts identify `source=nyfed_weekly`, their exact H/W cell, `native_unit="USD millions"`, and `post_result=true, exploratory=true`. The existing aggregate scalar values are:

| Receipt | H | W | Stored mean_absolute |
|---|---:|---:|---:|
| `results/revision-20261023/round2/shrinkage/nyfed-h24-w260.json` | 24 | 260 | `452.9620095521541` |
| `results/revision-20261023/round2/shrinkage/nyfed-h24-w52.json` | 24 | 52 | `832.3438980144283` |
| `results/revision-20261023/round2/shrinkage/nyfed-h6-w260.json` | 6 | 260 | `136.7733897226244` |
| `results/revision-20261023/round2/shrinkage/nyfed-h6-w52.json` | 6 | 52 | `366.7195226518396` |

The minimum endpoint is `nyfed-h6-w260.json` at 136.7733897226244; the maximum endpoint is `nyfed-h24-w52.json` at 832.3438980144283.

Static display rule: `round2_manuscript.py:12`–15 loads precisely these four receipts and defines `format(float(x),'.4g')`; line 23 selects the extrema of these already stored aggregate means; line 25 inserts them. Applying only that display rule gives:

```text
format(136.7733897226244, ".4g") = 136.8
format(832.3438980144283, ".4g") = 832.3
```

The exact statistical object is the **projection-aware capacity change after removing slopes while holding each fitted intercept fixed**. It is not the raw unprojected slope contribution, a refitted empirical-intercept report I, a change in realized funding costs, or the maximum individual-origin difference. `round2_shrinkage.py:15`–18 defines this distinction; lines 59–62 store the existing per-query-derived aggregate. The protocol explicitly fixes this fitted-intercept counterfactual and weights aggregates by actual query count.

No underlying queries, coefficients, responses or per-origin capacity vectors were recomputed or inspected. No new mean was calculated: only existing aggregate endpoints were selected for the manuscript display.

**Result: PASS, with exact source units and counterfactual identity preserved.**

### 3. Varying-dimension upper bound: 28 / 29

Direct existing audit fields:

```text
/predictors = 33
/constant_columns_zero_based = [28, 29, 30, 31, 32]
```

The list contains coordinate identifiers, not financial observations. Static `conditional_features.py:58`–63 maps these five identifiers to the two hour, two weekday and one gap coordinate. Lines 68–79 use training-only centering and exact-constant handling; `transform_features` line 86 subtracts the retained training mean. No new data parse or constant-column experiment was run here.

Static display generator: `v3_additions.py:42` sets

```python
varying_upper_bound = facts["predictors"] - len(facts["constant_columns_zero_based"])
# 33 - 5 = 28
# plus the intercept = 29
```

Line 43 prints “at most” and “before other collinearity.” This is exactly the current sentence. It is an arithmetic **upper bound**, not a computed matrix rank, identifiable-parameter theorem, causal diagnosis of Treasury failure, or effective sample size. Further collinearity can reduce the usable dimension.

**Display required:** the generator's subtraction and addition only. **Result: PASS.**

### 4. Standardized slope-norm range: 0.001497–0.01937

The generator's range uses only the stored `/refits/*/slope_l2_norm` scalars across the same four selected Treasury C2 receipts. The exact endpoints are:

| Endpoint | Receipt | Exact JSON pointer | refit_index | Stored slope_l2_norm |
|---|---|---|---:|---:|
| Minimum | `results/revision-20261023/round2/shrinkage/nyfed-h24-w260.json` | `/refits/0/slope_l2_norm` | 405 | `0.0014966769207252154` |
| Maximum | `results/revision-20261023/round2/shrinkage/nyfed-h6-w52.json` | `/refits/1/slope_l2_norm` | 418 | `0.019372116912597822` |

`round2_manuscript.py:22` selects the extrema of those saved scalars, and line 25 applies the same four-significant-digit formatter:

```text
format(0.0014966769207252154, ".4g") = 0.001497
format(0.019372116912597822, ".4g") = 0.01937
```

Static `round2_shrinkage.py:60` names the stored statistic as the L2 norm of slopes, excluding the intercept. Its surrounding code and the frozen E9 protocol identify standardized feature / response-normalized coordinates. This norm is not a native-unit coefficient norm or proof of zero feature value. This audit read the saved norm scalars, not coefficient vectors, and did not reevaluate a norm or optimizer.

**Result: PASS, preserving coordinate/scale interpretation.**

### 5. Nominal dimension: 33 predictors and 34 coefficients

Direct existing output fields:

```text
/predictors = 33
/coefficients_with_intercept = 34
```

Static source confirms the convention: `conditional_features.py:44` allocates 33 predictor coordinates; lines 53–63 populate the level, magnitude, two RMS, hour, weekday and gap groups. `conditional_study.py:117` appends `np.ones(len(pool))` to the transformed feature matrix for the QR fit. The single appended intercept therefore gives 34 nominal coefficients.

`v3_additions.py:43` prints the two direct audit fields. The original feature/QR entry-point source hashes still match their owning executable freeze. The 34 nominal coefficients do not mean 34 independently varying predictors; the current sentence immediately supplies the 28/29 bound from claim 3.

**Display required:** direct integers, with the one-intercept convention made explicit. **Result: PASS.**

## Boundaries retained

The five successful traces do not identify a feature-only cause of the Treasury deterioration. The present paragraph still calls competing explanations unresolved. Its “at most” dimension and path-count language is not converted into an effective-sample-size or identification claim.

The selected-fit paragraph remains post-result/exploratory, keeps its distinction from refitted I and F, denies that boundary penalties or high correlation alone establish zero feature value, and retains the adverse statement that three of four C2 cells have higher loss than F. That adjacent loss-count statement was not independently resampled or rerun in this five-claim task. No negative result, small-sample qualification, uncertainty or noncausal boundary was changed.

The only arithmetic in this round was the existing display generator's dimension subtraction/addition, choosing extrema of saved summary scalars, and its four-significant-digit formatting. No financial statistic, mean, norm, fit, loss, raw vector or probability was recomputed. The static routines were read, never imported or called.

An existing post-correction semantic-audit file surfaced during routing; its historical observations were not used as current proof. The fresh evidence above is the selected owning output fields, static rules and actual current hashes.

## Current source fingerprints

These are actual current bytes observed during the pending candidate, **not a blanket claim that all bytes equal HEAD**. The source clock and whole-document inequality are reported above. Frozen-feature equality refers only to `conditional_features.py` and `conditional_study.py` against their original executable-freeze entries.

| File | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `v6_submission.py` | `9f4984fc802f8a2e1375760d78cbe59ae04aa814bb83114d6707b70ac01b61c8` |
| `results/revision-20261023/treasury-feature-audit.json` | `07ab8ac703948e574dc4a4b8d9941568d8e0fa7b03038f0475b2073574ca5423` |
| `conditional_features.py` | `4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5` |
| `conditional_study.py` | `aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740` |
| `v3_additions.py` | `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525` |
| `round2_manuscript.py` | `166984a03b8ed11a08b36de72d9775f643b0ed52414e7f0c0a5278897e169e73` |
| `round2_shrinkage.py` | `65261388db6264e120c1629647712c7bdb4d5ea4fea82ecb1859b5de27ee1405` |
| `protocol/revision-20261023/round2-E9-shrinkage.md` | `56244b173f7c27c7a974e4405fd350c6d1e08dfc0cccd271813118c05fc4d346` |
| `protocol/revision-20261022/executable-freeze.json` | `e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb` |
| `results/revision-20261023/round2/shrinkage/nyfed-h24-w260.json` | `a2f9b988049b8382cf1bf5e92aaae75938d1e46e8d5968d1be3ccf9ba536ec68` |
| `results/revision-20261023/round2/shrinkage/nyfed-h24-w52.json` | `118255073f126102afe03c1379e3138f3b098a6a1a9e63f61ba45adb25f46142` |
| `results/revision-20261023/round2/shrinkage/nyfed-h6-w260.json` | `6ce2bad122f8c6fb80e8e4c89445090316b021adb51a7aa6abb3504d0bd0e545` |
| `results/revision-20261023/round2/shrinkage/nyfed-h6-w52.json` | `5be64de712b309e47ed7216805e68c41daeb413de3f4b971ce7a3823e695484d` |

## Disposition and action receipt

Five selected traces: PASS. Required scientific-conclusion issue / author pending: none identified.

Only this new note and the already frozen same-prefix selection JSON were written. No test, statistical diagnostic, proof, model, simulation, raw-data/vector read, UI operation, source/state/manuscript/result change, commit, push, publication or nested agent was performed. The root owns any later commit of this separate round and verification of the eventual committed or remote candidate.

This is correct-field/correct-format verification of existing evidence. It does not supply independent scientific validation or certify unselected claims or the rest of the manuscript.
