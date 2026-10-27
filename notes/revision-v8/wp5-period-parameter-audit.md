# WP5 period, parameter and archived-comparison audit

Scope: read-only source/protocol/public-result metadata audit after WP4 PASS.
No original CSV values, private financial arrays or source timestamps were read;
no resampling, financial fitting, new loss/DM computation or parameter selection
was performed. The only file written by this assignment is this note. A parallel
read-only sub-audit checked the old scalar/DM inventory; its findings below were
cross-checked against the identified original files. All indices are zero-based
and inclusive. No claim about absent external/deleted historical work is made.

## Decision before any WP5 design or computation

**MISMATCH / BLOCKED for an entirely previously unscored third hourly prefix.**
The v8 instruction, lines109–112, describes approximately mid-2014 to2015-10 as
training-only, never evaluated. Existing R6 records contradict that description:
there is already an earlier evaluation8999–10438, outer validation7535–8974,
and actual rolling-prefix validation scoring as early as911–934 (W720) and
3071–3094 (W2880). These are hourly roles, independently of WP4's daily proxy.
Do not execute a new financial backcast, declare an unseen third period, or
silently choose gaps after inspecting their results under this description.
The controlling plan's evidence-priority rule requires recording the mismatch.

There is no mechanically feasible full W2880/H6,H24 prefix whose target paths
precede every known hourly validation/scoring target: the common first eligible
issue is3071, while a target ending strictly before the earliest old score911
requires the last new issue+24<911, hence last issue<=886. This is index/timing
arithmetic, not a financial computation. Even considering only W2880's own
scoring beginning3071, a new full target preceding that boundary would require
last issue<=3046, still before its first eligible issue3071.

## 1. Existing hourly roles and their evidence

| Procedure/role | Inclusive issue interval | Evidence |
|---|---|---|
| Original historical F/S/K evaluation |11927–18551; date cutoff2016-01-01|`protocol/study-spec.json:223–234`; `protocol/revision-20261021-exploratory-spec.json:21–23`|
| Original QR33 (and conditional families) validation |10463–11902|`protocol/revision-20261022/study-spec.json:33–53`; `conditional-baseline-design.md:25`|
| Original QR33, F2880/d24 and rollingF720/d1 evaluation |11927–18551; 2016-01-01 through2017-01-23|same spec39–53; R6 design31–32|
| QR4 original validation/evaluation |same original chronology and all evaluation origins|`results/revision-20261023/parsimonious-design.md:1–3`; each W2880 JSON has origin_count6625, lines33–41|
| R6 retro outer validation, W720/W2880,H6/H24 |7535–8974; 2015-04-21 through2015-07-13|`protocol/supervisor-20261023/r6-design.md:29–30`|
| R6 retro evaluation, same four cells |8999–10438; 2015-07-15 through2015-10-06|same29–30; `r6-memo.md:11–15`|
| R6 retro R3 prefix scoring,W720,H6/H24 |first911–934, then24-origin blocks at48-index spacing, last7487–7510, then outer7535–8974|`retro-cells.json` groups[].r3_fold_bounds; earliest first entries19077–19081 and21264–21268; source `supervisor_r6.py:299–308`|
| R6 retro R3 prefix scoring,W2880,H6/H24 |first3071–3094; same spacing; last7487–7510; then outer7535–8974|`retro-cells.json:20244–20248,22629–22633`; R6 design55–59|
| R6 inspected R3 prefix scoring,W720,H6/H24 |first911–934; last10415–10438; then outer10463–11902|`inspected-cells.json:37772–37776,40403–40407`, groups[].r3_fold_bounds|
| R6 inspected R3 prefix scoring,W2880,H6/H24 |first3071–3094; last10415–10438; then outer10463–11902|`inspected-cells.json:39189–39193,42012–42016`, groups[].r3_fold_bounds|
| R6 inspected evaluation |11927–18551|R6 design31–32|

R6's five finite QR candidates plus I are scored on prefix folds, not merely
trained there. `supervisor_r6.py:275–291` calls the forecast, then scores its
complete segment;299–308 explicitly loops over every prefix fold/candidate.
`supervisor_r6_rules.py:200–226` fixes these folds. W720/R3 final status FAILED
does **not** undo already calculated fold scores or turn those source records
back into training-only data. There are archived complete files for these
origins, not just a design aspiration: `private-archive-manifest.json:81129–81136`
lists the retro H24/W720 lambda.001 JSON and NPZ911–934; NPZ2579bytes SHA256
`25a04f71a2faa1dd842dd91bd1d7bef010547d37dd9ac6e522885c7db8faa486`.
Only the public archive manifest was opened, not those private arrays.

For H24, a24-origin scoring block[a,a+23] uses target source indices[a,a+47].
The next block starts a+48. Thus their target paths abut, although their issue
origins have purge gaps. Existing H24 prefix blocks and outer/evaluation blocks
therefore rule out using those gaps as wholly unscored target paths. This
mechanical statement concerns exposure/inspection, not probabilistic dependence.
Exact dates for911/3071 were not rederived from raw timestamps in this audit.

The earlier R6 design11 bounded its then-current claim to no prior *evaluation*
role found before that run; it did not promise future untouched validation.
It expressly acknowledged familiar raw/training history. R6 design59 also says
inspected R3 later uses some retro evaluation origins. Its historical wording
must not be transplanted into a current never-scored claim.

## 2. Mature-history boundary and limits of any future design

The original FX feature-valid index is168 (24/168 increment RMS), not24:
`conditional_features.py:35–65`; `conditional-baseline-design.md:11–15`.
At refit r, the exact W-origin training pool is
`[r-H-W+1,...,r-H]`, checked by `conditional_features.py:94–99` and
`conditional_study.py:103–114`; training labels end no later than r.
Therefore common H*=24,W2880 first eligibility is168+2880+24-1=3071,
the same explicit formula in R6 design55 and `supervisor_r6_rules.py:216`.
Refits start at each declared segment and advance24 observed source records
(`conditional_features.py:102–105`; original study-spec45).

A valid *unseen-prefix* mechanical design would need simultaneously:

1. first issue>=3071 for the unshortened original QR33/QR4,W2880 and H24;
2. last issue+24<earliest prior validation/scoring/assessment issue;
3. full source-index target disjointness against all old validation and
   evaluation target paths, not just no identical issue index;
4. immutable later-validation selected penalties with no earlier-period tuning;
5. explicit pseudo-out-of-sample/backcast status because those parameters were
   chosen later than the backcast issue dates.

The observed earliest scoring911 makes1 and2 mutually incompatible. No new
period is recommended. Dropping W2880, deleting H24, calling old scoring
training, changing the source, retuning, or evaluating an inspected overlap
would be a different scientific scope; this audit does not authorize it.

## 3. WP4 daily roles are a separate task

WP4 uses the same familiar raw dealer but selects each ended source-naive day's
last record and issues at23:59:59.999999. Its targets sample daily positions and
exclude intraday excursions (`protocol/revision-v8/wp4-daily-fx-design.md:10–28`).
Daily validation329–380/evaluation405…n_daily-25 are **daily indices**
(same file32–49), not hourly indices329/405 or a new dealer. Do not mistake its
index values or different sampled target for new hourly independence. The
current audit does not read the private selected-row vector to map every daily
role to an hourly row. Raw-source familiarity, hourly score exposure and daily
sampled-target exposure are three different statements. WP4 cannot repair the
older hourly R3 exposure or certify an unseen backcast.

## 4. Frozen old parameter identities

| Procedure | Parameter source / exact role |
|---|---|
| Original QR33,H6/W2880 |`protocol/revision-20261022/selection-freeze.json:49–61`, parameter.01, original3-point menu|
| Original QR33,H24/W2880 |same133–145, parameter.001, original3-point menu|
| QR4,H6 and H24/W2880 |`results/revision-20261023/parsimonious/fx_hourly-h{6,24}-w2880.json:33`, both.01; original QR4 five-point menu|
| Retro H6 original QR33 structure |`r6/primary-replication.csv:3`, selected_id.01; source `supervisor_r6.py:309–311` explicitly selects FINITE_IDS[:3]; same choice happens to equal R0|
| Retro H24 R0 |`r6/retro-selection.csv:118`, selected_id.01 from **five-point** menu; not an archived original-three-menu primary selection|

R6 source309–311 constructs the original-three-menu primary selection only for
retro H6/W2880. Its335 constructs rollingF720/d1 only for that declared primary.
Do not label H24 R0 or R2 as the original QR33 procedure, and do not synthesize
an absent old H24 comparison by recomputing a private trace.

Current parameter file SHA256:

```text
531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7  protocol/revision-20261022/selection-freeze.json
b32541cb18e3ee149e68932affbfb0c02026dd8fa79625066a198493bf567d87  results/revision-20261023/parsimonious/fx_hourly-h6-w2880.json
6e6d18e979e1fdc2b6ba6bc1fe78bb0821ee83701c0973b0b959fcb2ae6d34b9  results/revision-20261023/parsimonious/fx_hourly-h24-w2880.json
b0cfb90cca0aa2b286444786b2a6dc8155eb21f3da177954065222a1d8ebe5a3  results/supervisor-20261023/r6/retro-selection.csv
```

## 5. Existing scalar, breach and DM inventory; absence stays absent

| Period/model | matched frozenF2880/d24 | rollingF720/d1 |
|---|---|---|
| Retro8999–10438,H6 original QR33 |scalar/breaches in `r6/retro-summary.csv:164–166`; paired DM in `r6-writing-hac-20261023/comparisons.csv:2`|scalar/DM same comparisons.csv:3; primary scalar identity `r6/primary-replication.csv:3`; public primary table has no rolling breach count|
| Retro,H24 QR33 |`r6/retro-summary.csv:176–178` has **R0 five-menu** scalar/breaches only|no existing original-three-menu H24 rolling scalar/DM located|
| Retro QR4,H6/H24 |not in R6 method family; no old third-party/retro QR4 result located|not located|
| Inspected11927–18551,H6 QR33 |`revision-20261022/evaluation-summary.csv:5,26`; `supervisor-20261023/inference/dm-verified.csv:11`|evaluation-summary.csv:11; dm-verified.csv:38|
| Inspected,H24 QR33 |evaluation-summary.csv:38,53; dm-verified.csv:29|evaluation-summary.csv:41 scalar/breaches; no corresponding existing QR33-vs-rollingF720 DM located (H24 legacy primary instead references S)|
| Inspected,H6/H24 QR4 |`revision-20261023/parsimonious/summary.csv:7,9`; `supervisor-20261023/e3/paired-dm.csv:17,23`|F rolling scalar exists in original table; no paired QR4-vs-rollingF720 DM located|

Representative original values (copied, not recomputed):

| Period/H/model/reference | QR mean loss | F mean loss | Percent change | DM statistic | normal p | L |
|---|---:|---:|---:|---:|---:|---:|
|retro/H6/QR33/matchedF|286562.4725431636|343697.20137447916|-16.62356533682211|-4.178271978163359|2.937322779608827e-05|7|
|retro/H6/QR33/rollingF720|286562.4725431636|277762.40801736113|3.1681985293173343|0.5627820958725974|0.5735832734537913|7|
|inspected/H6/QR33/matchedF|385844.8854897607|452692.9834478481|see original table|-5.865679844214457|4.472961414014163e-09|10|
|inspected/H6/QR33/rollingF720|385844.8854897607|441774.03703851684|see original table|-5.182010163255102|2.1950725127844084e-07|10|
|inspected/H24/QR33/matchedF|734695.0685732415|763381.1758251915|see original table|-0.5040894639524137|0.6141985104549805|24|

Retro matched H6 breach counts areF16/QR20; retro H24 R0 matched countsF0/R01.
Inspected H6 counts QR376/matchedF360/rollingF332; H24 QR531/matchedF357/rollingF415.
QR4 inspected H6/H24 losses433275.30347718514/741291.4299639979,
breaches399/508, matched changes-4.2893706508927965%/-2.8936718065277542%.
Those QR4 matched paired p-values are.010051999322709181/.6172773677048984;
their E3 family is28 comparisons, not the original72-comparison family.

`comparisons.csv` fields are explicit: comparison,phase,source,horizon,
conditional_report,selected_lambda,QR_window,QR_refit_step,F_window,F_refit_step,
n,H,L,origin_first,origin_last,exact_shared_origins,QR_mean_loss,F_mean_loss,
mean_loss_difference_QR_minus_F,ratio_change_percent,raw_LRV,HAC_statistic,
two_sided_normal_HAC_p,status,reference_distribution,covariance,
multiplicity_adjustment,QR_trace_sha256,F_trace_sha256.
Negative QR-minus-F differences favor QR. The retro readback has only2
comparisons, standard-normal two-sided p-values, Bartlett NW/divisor n and no
multiplicity adjustment or HLN extension (`results.json:66–77`; README3–5).

The common implementation is `inference_tests.py:65–86`: bandwidth
min(n-1,max(H,floor(4(n/100)^(2/9)))), centered Bartlett NW with divisor n;
mean difference uses math.fsum/n; nonpositive LRV or constant differences leave
statistics NA with status, without epsilon repair. The normal DM is two-sided;
HLN multiplier and Student t(n-1) are separately reported in the original
inference procedure, with2L sensitivity (`inference-design.md:5`). These later
post-result references do not control the full inspection/selection process.
Do not substitute a different reference, p-value family or statistic for a
missing archive cell, and do not run old-period missing DM as an audit step.

## 6. Metadata-only commands and observed output

Successful source reads used `nl -ba ... | sed -n ...` for the exact line ranges
above. Public JSON metadata was parsed with standard-library json only, selecting
groups[].group, r3_fold_bounds and selections.R3.status; no financial vectors
were accessed. The observed role output was:

```text
retro H6 W720 FIRST[911,934] PENULTIMATE[7487,7510] OUTER[7535,8974] FOLDS139 R3_FAILED
retro H6 W2880 FIRST[3071,3094] PENULTIMATE[7487,7510] OUTER[7535,8974] FOLDS94 R3_SELECTED
retro H24 W720 FIRST[911,934] PENULTIMATE[7487,7510] OUTER[7535,8974] FOLDS139 R3_FAILED
retro H24 W2880 FIRST[3071,3094] PENULTIMATE[7487,7510] OUTER[7535,8974] FOLDS94 R3_SELECTED
inspected H6 W720 FIRST[911,934] PENULTIMATE[10415,10438] OUTER[10463,11902] FOLDS200 R3_FAILED
inspected H6 W2880 FIRST[3071,3094] PENULTIMATE[10415,10438] OUTER[10463,11902] FOLDS155 R3_SELECTED
inspected H24 W720 FIRST[911,934] PENULTIMATE[10415,10438] OUTER[10463,11902] FOLDS200 R3_FAILED
inspected H24 W2880 FIRST[3071,3094] PENULTIMATE[10415,10438] OUTER[10463,11902] FOLDS155 R3_SELECTED
```

A second metadata-only regex inspection selected complete NPZ filenames from
the public private-archive-manifest, keyed by phase/H/groupW/actualW/d; it
independently found earliest911–934 for both W720 groups and3071–3094 for both
W2880 groups, in both phases. The additional retro H6/W2880 rolling reference
first occurs8999–10438, actualW720/d1. Files were hashed with standard-library
hashlib.sha256(Path(...).read_bytes()); current provenance hashes are:

```text
926747a8d140b78112bf00793f1c42a2c4914883e93401d1c14fb265d5af9b9e  results/supervisor-20261023/r6/private-archive-manifest.json
360734e167597656f234365e1d259b67d2c2c445d9871972b706b93d133f6e60  results/supervisor-20261023/r6/retro-cells.json
dba22bc7bafa3ad606cb20649343c120d44b668fef24e0a040a1de6ae070a47c  results/supervisor-20261023/r6/inspected-cells.json
46c86122b04bdb5ccbfbefd305c7eb0b8fe95e7423ae8be888d3758348d61159  results/supervisor-20261023/r6-writing-hac-20261023/comparisons.csv
39abe844f7a81875bfcda717a5d6d3634aa58e1e55e4a956b3f4cf2a2f269b20  results/supervisor-20261023/inference/dm-verified.csv
776e0856bce9e529156f279fc9b1790a498b59207abd76c4631737e98af13475  results/supervisor-20261023/e3/paired-dm.csv
```

Preliminary nonauthoritative searches encountered absent local AGENTS.md/src/code
paths, unmatched zsh globs, and overly broad output truncation. None altered a
file or established a scientific fact; the conclusions rely on the successful
bounded reads and metadata fields above. No general hidden/external-use absence
was inferred from failed searches.
