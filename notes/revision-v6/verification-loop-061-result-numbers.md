# Loop061 — final five Table5 display-cell traces

First clock: 2026-10-23 23:04:17 UTC. Initial/latest HEAD: `fc83ee23cf1d8b431efb2fe88c284060615e3b63`. Freeze: `2026-10-23T23:04:38.908339+00:00`; field readback: `2026-10-23T23:05:03.528726+00:00`; note written: `2026-10-23T23:06:06.332557+00:00`. Main JSON/article/PDF hashes were rechecked unchanged at 23:05:19 UTC and are retained in the JSON. Parent goal remains active to 2026-10-24 00:31:50 UTC.

Current Table5 `/sections/6/blocks/0` has 35 actual result cells. Prior057 excluded25 plus selected5 gives 30 distinct prior selections. Exactly **5 remain**, no missing ID/frame issue. Full remaining frame and 30 excluded IDs are in the JSON. Seed **2026102361** drew order **[3,0,2,1,4]** before lookup. All five remaining cells are selected; randomness changes their order only. No definitions/settings, fallback or favorable replacement were used.

Prior exposure: displays and saved scalar fields were seen before. Not previously randomly selected does not mean unseen/blinded. Prior057 verdicts are not current source evidence.

Owning output: `results/revision-20261023/inference/coverage.csv`. Actual formatter `v3_additions.py:12,23–27` selects exact source/H/W/method, formats saved p fields with `.3g` (None/empty→NA), and joins saved `hits+'/'+n` for counts. The module is not run; no count, statistic or p-value is recalculated.

| Cell | Selector (source,H,W,method) | Saved fields → display | Sample |
| --- | --- | --- | --- |
| FX matched F H6 DQ p | fx_hourly,6,2880,frozen_F | dq_p=0.04071441106014318 → **0.0407** | DQ n6615, df6, bandwidth10 |
| FX QR H6 k/n | fx_hourly,6,2880,QR | hits=50,n=947 → **50/947** | stored strings, grid stride7 |
| FX rolling F H6 CC p | fx_hourly,6,720,rolling_F | cc_p=0.9067712932289955 → **0.907** | grid n947, stride7 |
| FX QR H6 DQ p | fx_hourly,6,2880,QR | dq_p=0.7361464566292177 → **0.736** | DQ n6615, df6, bandwidth10 |
| Treasury QR H6 k/n | nyfed_weekly,6,260,QR | hits=7,n=40 → **7/40** | stored strings, grid stride7 |

**All five match; lookup/frame/display failures and NA substitutions are zero.** Matched frozen F W2880 is not original rolling F W720. Counts are sparse-grid observations, not ranks/windows or full-origin counts. DQ n6615 is its full-sample HAC effective n, distinct from sparse n947. Archived CC is not the S16 likelihood or a DQ p-value.

Selected rows retain ind_status=OK/boundary=False; both DQ fields retain dq_status=OK. Missing/failed references would remain NA/status. Current flags do not erase earlier boundary warnings or validate reference laws. These are post-result/exploratory diagnostics, without coverage guarantees or selection-adjusted confirmation.

SHA-256:

- main JSON: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`
- coverage output: `58db76faaeb3250f66bbc90ab0be3f87f674e2022e3374961f73a27a935a2419`
- actual formatter: `f3984bd513758050fe9a37204e1693189e55676826bde57b53a1acc15c9a9525`
- final selection JSON: `ec02bdd933a8d16554d7a88d9390035d5147362f8843647b5345c45cdb3633a2`

Cumulative accounting closes **all 35 distinct Table5 displayed cells**, each individually source/formatter checked across the recorded loops. Earlier 30 traces are not re-estimated here. This is not comprehensive independent validation of statistical references or financial results, raw data, prospective performance or replication.

Read scope: current displayed Table5, prior057 IDs, four exact coverage rows and needed grid/DQ/status fields, formatter lines12/23–27, HEAD/hashes. PDF was hashed only. No private/raw vectors, network/UI/Claude/nesting, new statistic/count/model/test/proof, other edit, commit, state or ledger action occurred. Only paired loop061 files are written. After final readback/FINAL these files will not be edited further; overall goal completion is not claimed.
