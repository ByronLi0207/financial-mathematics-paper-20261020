# Loop057 — five remaining actual Table5 results

First real clock: 2026-10-23 22:59:56 UTC. Initial/latest HEAD: `06d82e5d50f7ba0b66a926f9e52e9ef66a39c8f5`. Freeze: `2026-10-23T23:00:10.188140+00:00`. Field readback: `2026-10-23T23:00:34.072818+00:00`. Note written: `2026-10-23T23:01:09.632571+00:00`. Parent goal remains active to 2026-10-24 00:31:50 UTC.

Scope is current main Table5 `/sections/6/blocks/0`. Loop053 excluded20 plus selected5 gives 25 unique previously sampled cells; removing them from 35 actual results leaves the expected **10**, with no missing exclusion ID/frame issue. Full ordered frame and excluded IDs are in the JSON. Seed **2026102357** drew **[5,9,3,1,7]** before owning-field/formatter lookup. No definitions/settings, fallback or favorable replacements fill the sample.

Prior exposure is explicit: displayed results and saved scalar rows/fields have been read in earlier loops. Remaining means not previously randomly selected, not unseen/blinded. Prior053 verdicts are not current evidence.

Owning output: `results/revision-20261023/inference/coverage.csv`. Actual static formatter `v3_additions.py:12,23–27` selects exact source/H/W/method rows, uses `NA` for None/empty or otherwise `.3g` on saved p fields, and joins saved `hits+'/'+n` for count cells. The module is not run. Only those display operations are applied.

| Cell | Exact selector (source,H,W,method) | Saved fields → display | Sample meaning |
| --- | --- | --- | --- |
| FX rolling F H6 DQ p | fx_hourly,6,720,rolling_F | dq_p=0.007981716318991423 → **0.00798** | DQ n=6615, df6, bandwidth10 |
| Treasury F H6 k/n | nyfed_weekly,6,260,frozen_F | hits=4,n=40 → **4/40** | stored count strings, sparse stride7 |
| FX rolling F H6 Ind p | fx_hourly,6,720,rolling_F | ind_p=0.7124307933754886 → **0.712** | sparse n947, stride7 |
| FX QR H6 Ind p | fx_hourly,6,2880,QR | ind_p=0.3879860137718663 → **0.388** | sparse n947, stride7 |
| FX legacy S H24 DQ p | fx_hourly,24,720,rolling_S | dq_p=0.029901111117702456 → **0.0299** | DQ n=6597, df6, bandwidth24 |

**All five match.** Lookup/frame/display failures and NA substitutions: zero. No coverage count, statistic or p-value was recalculated. Original rolling F W720 remains distinct from matched frozen F W2880. Legacy rolling S H24 remains distinct from QR H24, even where another report/test displays the same rounded string. The count is an observed sparse-grid result, not a rank/window setting.

Both DQ rows retain `dq_status=OK`; their full-sample HAC effective n=6615/6597 is distinct from sparse-grid n=947/265. Treasury frozen F retains **ind_status=BOUNDARY_REFERENCE, boundary=True**; the observed count match does not erase this reference-law warning. Other selected rows retain ind_status=OK/boundary=False. Missing/failed reference fields would remain NA/status rather than trigger replacement. These post-result/exploratory diagnostic displays do not certify coverage, reference assumptions or selection-adjusted inference.

SHA-256 (target hashes rechecked unchanged at 23:00:49 UTC):

- main JSON: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`
- article TeX: `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`
- PDF: `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`
- coverage output: `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419`
- actual formatter: `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525`
- final selection JSON: `512d8001ad2e00c5f2e1837a191eeb47de783951721bb7344e91b9e41167abf7`

The JSON retains prior053/freeze/source hashes, complete 10-cell frame, 25 excluded IDs, draw, five direct fields/selectors/formats, statuses and failure list, without copying an old JSON/table. The freeze flag remains a historical snapshot; evidence is appended later.

Read scope: current displayed Table5, prior053 exclusion/selection IDs, four exact coverage rows and needed grid/DQ/status fields, formatter lines12/23–27, HEAD and hashes. PDF was hashed only. No raw/private vectors, new statistic/model/proof/test/coverage count, network/UI/Claude/nesting, other file edit, commit, state or ledger action occurred. Only the two authorized loop057 files are written. No numerical correction is indicated by this sample; no overall completion or independent/prospective validation is claimed.
