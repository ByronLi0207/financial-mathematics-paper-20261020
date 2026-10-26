# Loop053 — five actual Table5 result-cell traces

First clock: 2026-10-23 22:54:19 UTC. Initial/latest HEAD: `809dcbf996451b3bf2104ffd928dfaf415e16ce8`. Freeze: `2026-10-23T22:54:45.573084+00:00`; saved-field readback: `2026-10-23T22:55:13.846033+00:00`; note written: `2026-10-23T22:56:14.069517+00:00`. Goal remains active to 2026-10-24 00:31:50 UTC.

The current Table5 frame is `/sections/6/blocks/0` in `submission-jof/manuscript-content.json`. From loop049's excluded IDs plus selected IDs, 20 unique previously sampled cells were removed from 35 actual results. Exactly 15 remain, with no changed display/frame issue. The full ordered frame and 20 excluded IDs are preserved in the JSON; no old selection/table is copied wholesale. Seed **2026102353** drew **[13,8,3,10,9]** before owning-field lookup. No fallback or favorable replacement occurred.

Prior exposure: table displays, the coverage file and several scalar rows were seen in earlier loops. Remaining means not previously randomly selected, not unseen/blinded. Prior49 verdicts are not current evidence.

Owning output: `results/revision-20261023/inference/coverage.csv`. Actual static formatter: `v3_additions.py:12,23–27`, with label-specific source/H/W/method selection; p fields use `NA` for None/empty, otherwise `format(float(x),'.3g')`; counts use saved `hits+'/'+n`. The module was read, not run. Only scalar formatting/string joining was applied.

| Sample | Exact selector (source,H,W,method) | Saved fields → displayed result | Meaning |
| --- | --- | --- | --- |
| Treasury QR H6 CC p | nyfed_weekly,6,260,QR | cc_p=0.015694656273894155 → **0.0157** | fixed stride7 grid, n=40 |
| FX QR H24 POF p | fx_hourly,24,2880,QR | pof_p=0.04331382313342323 → **0.0433** | stride25 grid, n=265 |
| FX rolling F H6 k/n | fx_hourly,6,720,rolling_F | hits=49,n=947 → **49/947** | stored count strings, stride7 |
| FX legacy S H24 k/n | fx_hourly,24,720,rolling_S | hits=10,n=265 → **10/265** | stored count strings, stride25 |
| FX QR H24 DQ p | fx_hourly,24,2880,QR | dq_p=0.10052276337793768 → **0.101** | full-sample HAC DQ, dq_n=6597, df=6, bandwidth=24 |

**All five match.** Frame/lookup/display failures and NA substitutions: zero. No counts, statistics or p-values were recomputed. The count `49/947` belongs to original rolling F W720, distinct from matched frozen F W2880 even though its display coincides. H24 QR and legacy rolling S retain their different methods/windows. DQ n=6597 is not the sparse-grid n=265. Legacy CC is the archived grid diagnostic, not a new S16 likelihood or paired-loss p-value.

All sampled rows retain `ind_status=OK`, `boundary=False`; the DQ row retains `dq_status=OK`. Missing/reference failures would remain NA/status, not trigger substitution. Display agreement does not validate reference assumptions or certify coverage. These remain post-result/exploratory diagnostics.

SHA-256 (target hashes unchanged at 22:55:43 UTC):

- main JSON: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`
- article TeX: `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`
- PDF: `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`
- coverage output: `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419`
- actual formatter: `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525`
- final selection JSON: `5844c1e97f34e838c8ab54a740cc5e5f80532706716e2a5925b98f2b2953ee75`

The JSON retains the prior49 hash, freeze-time file hash, complete remaining frame, excluded IDs, draw, five exact fields/selectors/formats, statuses and source hashes. Read scope was current displayed Table5, prior49 ID/display metadata, four selected coverage rows, formatter lines12/23–27, HEAD and hashes. PDF was hashed only. No raw/private vectors, network/UI/Claude/nesting, new model/statistic/proof/test/coverage count, other file edit, commit, state or ledger change occurred. Only the two authorized loop053 files were written. No numerical correction is indicated by this sample; the overall goal is not marked complete.
