# G3 independent read-only audit

Status: implementation/data-alignment PASS for the sealed actual G3 run. This is not a claim that the protocol passed its scientific criteria: **R1 SUPPORTED, R2 NOT_SUPPORTED, R3 SUPPORTED**. This review changed no design, implementation, source data, cache or numerical result and reran no forecast/fit.

## Precommitted procedure and timing

- Standalone G3 design:99a912ccf6911da2f54627a7b4b57fb7541b6673,2026-10-25T20:24:05−07:00. Execution seal:3c11a975ba7085d57ccf2a0b9e977ced5e808e0b. All current code bytes still match the recorded code-seal SHA values.
- Formal numerical run:2026-10-26T03:33:01.753154Z..03:35:29.808879Z,148.05624241707847 seconds. All62 geometries,60 weekly and2 FX, are eligible and COMPLETE for RP, ordinary regression and F. No resource reduction, failures or exclusions occurred.
- Weekly/source/horizon/history and both FX indices match the standalone design. FX long validation has5760 observations and ends at each unchanged original boundary; its earliest training origins3258/330 exceed168. All validation labels finish strictly before evaluation. The shorter ordinary selection and RP selection use distinct prespecified segments.

## Paired evidence and sealed evaluation

For all62 saved gates, independently loaded the SHA-checked selected-regression and F long-validation loss traces, checked exact common origin arrays, and reconstructed d=loss(QR)−loss(F) in chronological order. Independently computed the Bartlett/Newey–West covariance and the fixed bandwidth K=min(n−1,max(H,floor(4(n/100)^(2/9)))). The saved mean is exactly math.fsum(d)/n; the stored K, long-run variance, SE=sqrt(Omega/n), and route match independent calculations (within float-roundoff for covariance/SE). Every gate is AVAILABLE.

The decision is strict: choose QR only when mean(d)<0 and −mean(d)>SE. Equality returns F. The same validation data choose lambda and assess this evidence, so the one-SE rule is a retrospective heuristic, not a nominal test or risk-control guarantee. The HAC construction preserves overlap dependence within a source and does not treat related sources as independent samples.

Checked each private persisted choices.json against public choices/gate and choice_sealed_utc. Code order writes this seal before any evaluation-cache call. The3 new evaluation references (2 unique reports) have attempt timestamps strictly after their cell's seal; old evaluation reports have only been read after that seal in this driver. Ordinary and long-validation choices are both sealed before evaluation.

## Infinity, failures and concurrency

- All six candidates must complete before selection; exact ties favor the strongest penalty. A failed long-validation candidate or F-validation fit yields a failed RP method with no actual route, never a successful F fallback. Only a completely evaluated insufficient-evidence gate, or the explicitly predeclared unavailable-HAC case with completed fits, may select F. In the actual run all gates are finite and available.
-33 long selections use infinity. Their terminal forecast identity is I, whereas the paired benchmark's identity remains F. Infinity is never credited automatically as the corrected-rank benchmark:23 such selections fail the evidence gate and use F;10 pass and use I through the QR route.
- The four-worker actual grid has no shared unfinished new-cache write. Sources/horizons/histories separate weekly keys; G2's NY Fed long-validation candidates were complete before G3. Both FX periods use different full origin segments. An ordinary/RP evaluation reused within the same cell is sequential. Shared cache keys include all source/grid/code/geometry identity fields.
- Parent process groups are terminated/waited on at the2700-second study or300-second cell wall limit; workers additionally enforce deadline/RSS. These limits were not approached by the148.06-second run.

Independently hashed all960 saved candidate/reference records, spanning946 unique cache reports (708 v12,238 v13). Every terminal is COMPLETE, each trace retains its recorded size/SHA, each scalar trace-SHA matches, and every cache key equals the canonical hash of its full identity. The output-manifest byte counts/SHA and current source-code seal all pass. No cache repair or scientific rescoring was performed during this check.

## Fixed denominators and actual criteria

The summary uses all60 weekly cells; missing or duplicate slots cannot disappear from the denominator. R2 permits at most3 of60 cells above10%, not3 per data source. R3 checks each eligible FX period's ordinary-regression gain separately and requires RP relative loss<=half the negative ordinary relative loss. No pooled or best-period FX shortcut is used.

|Quantity|Independent check from saved rows|
|---|---:|
|Weekly complete/planned|60/60|
|Ordinary weekly median relative loss|+14.627467605779144%|
|RP weekly median relative loss|0%|
|RP weekly worst relative loss|+80.98396986931891%|
|RP weekly >+10%|8/60 (13.333333333333334%)|
|F fallback|32/60 (53.333333333333336%)|
|QR route|28/60 (46.666666666666664%)|
|Unknown route|0|

R1 is SUPPORTED because0<=1%. R2 is NOT_SUPPORTED because8>3. This failure must remain prominent; the median and fallback rate cannot support a statement that RP reliably protects every inventory limit or satisfies the task's whole protection target.

|Group|F fallback/planned|QR route/planned|
|---|---:|---:|
|T-bill H6 W52|1/1|0/1|
|NY Fed panel H6 W52|8/12|4/12|
|T-bill H24 W52|1/1|0/1|
|NY Fed panel H24 W52|10/12|2/12|
|CFTC H6 W52|6/17|11/17|
|CFTC H6 W260|6/17|11/17|
|FX original H6 W2880|0/1|1/1|
|FX early2015 H6 W2880|0/1|1/1|

NY Fed fallback20/26; CFTC12/34. Every row's F route has exact RP loss equal to reference loss and relative excess0, while a QR route has indicator1 and the selected long-validation model's result.

|FX period|Ordinary excess (%)|RP excess (%)|Half-gain cutoff (%)|Route|R3|
|---|---:|---:|---:|---|---|
|Original|−14.766762552613882|−14.766762552613882|−7.383381276306941|QR|SUPPORTED|
|Early2015|−16.623565336822104|−16.623565336822104|−8.311782668411052|QR|SUPPORTED|

Both periods select penalty0.01 on both validation lengths. Thus the FX gains are preserved by the unchanged selected models; this is not evidence of an extra FX improvement from the protocol. R3 is SUPPORTED separately in both periods.

## The8 adverse weekly cells, retained without retuning

|Source|H|W|Long selected penalty|RP excess (%)|
|---|---:|---:|---:|---:|
|PDPOSGSC-G2L3|6|52|1|25.50896356899675|
|1170E1|6|52|1|46.29642583531103|
|095741|6|52|1|19.33471575756462|
|232741|6|52|1|37.533419906829295|
|112741|6|52|10|10.051067649521562|
|044601|6|260|1|13.219806534642528|
|096742|6|260|0.001|62.68351682114846|
|112741|6|260|0.1|80.98396986931891|

All eight passed their validation evidence gates yet lost above10% in evaluation. They directly establish the limit of this retrospective one-SE procedure; do not change its thresholds or classify these as failed numerics.

Sources inspected: protocol/v13/recommended-protocol-design.md; v13_rp.py; v13_rp_runner.py; run_v13_rp.py; report_v13_rp.py; test_v13_rp.py; unchanged inference_tests.py; results/v13/recommended-protocol/{rows,candidates,references,selections,cell-results,summary,runtime,code-seal,output-manifest}.json and the corresponding SHA-bound private report files. Only this new independent-review note was written.
