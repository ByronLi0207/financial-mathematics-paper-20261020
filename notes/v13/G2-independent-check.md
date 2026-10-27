# G2 independent read-only check

Status: PASS for the actual sealed G2 run; no material implementation or data-alignment defect found. This check performed no fitting, forecast generation, cache repair, or experiment rerun. It read the design, implementation, saved scalar results and file hashes only.

## Design and causal geometry

- Standalone design `d58464ee2bf87f01e7e2625b0888edcd2e442214` changes only `protocol/v13/nyfed-validation-length-design.md`. Sealed execution commit is `9111b4dcb04dfa4593b2e657a455e26b98458699`; working code hashes still match the recorded seal.
- Evaluation is the unchanged inclusive indices405..681,277 origins, dated2021-01-06..2026-04-22. Both short validation arms retain329..380,52 origins, dated2019-07-24..2020-07-15.
- Long H6 validation is243..398,156 origins, dated2017-11-29..2020-11-18. Long H24 validation is225..380,156 origins, dated2017-07-26..2020-07-15. Both latest labels end404 (2020-12-30), strictly before evaluation starts405.
- First W52 training origins are186 for H6 and150 for H24, so both exceed the26-observation causal feature requirement. The same geometry with W260 would start−22 and−58, explaining its prespecified exclusion. The actual source-date column independently matches these indices.
- No issue at or after405 enters validation labels. Refits and transforms use unchanged v12 completed-label logic. The six ordered penalties include ordinary empirical I at infinity; corrected-rank F remains a distinct reference.

## Whole cells, cached identity and process limits

- The saved inventory contains exactly52 unique geometries and104 unique method cells (13 sources ×2 horizons ×2 validation lengths ×2 regressions). All104 completed, each with all277 evaluation origins. The624 validation candidate rows cover exactly six ordered candidates per method cell;104 selected evaluation rows yield728 candidate records in total.
- Original reports are read only: `attempt_cached` uses `_read_cache` on prior v12 keys and calls `_attempt` only with the new v13 cache. Prior FAILED terminal records propagate and cannot cause a new fit. Source bytes/SHA, aligned time grid, feature/model code, horizon/history/quantile/refit step, full origin segment and trace SHA bind each cache identity. The implementation does not silently use a successful subset.
- The actual run reused312 old validation records and104 old selected evaluation records. All selected evaluation records read exact v12 reports. Independently checked381 distinct old caches (355 candidate keys plus26 distinct F-reference keys): every terminal was COMPLETE and every trace retained its terminal-recorded byte count and SHA-256. There were286 distinct new long-validation report keys, all COMPLETE.
- No simultaneous new-key collision occurs in this G2 inventory: within a method, only one long-validation report exists per source/horizon; its short arm reads old reports. Evaluation keys also read old reports. QR33 and QR4 run in separate parent phases, so their shared infinity/I long-validation key is produced before the second method reads it. Thus the inherited cache's immediate `folder exists` behavior does not turn a concurrent unfinished write into a false failure here. This is a statement about the actual fixed G2 grid, not a blanket concurrency guarantee.
- Parent starts workers in distinct process groups, checks both the1800-second study deadline and300-second per-cell cap, and kills/waits for each expired process group. Worker checkpoints independently enforce deadline and2GiB RSS. Resource omissions/failures retain planned rows. The observed numerical run finished in14.065626416355371 seconds (2026-10-26T03:22:14.775734Z..03:22:28.841297Z), far within both limits; no omissions or worker failures occurred.

## Independent scalar summary check

Recomputed the differences of arm medians and infinity counts directly from the saved104 rows, without new financial scoring. They exactly match summary.json. Fixed13-source denominators, missing/duplicate-slot handling, and both-horizon logical conjunction are preserved. Every output-manifest entry also passes current byte-count/SHA checks.

|Method|H|Median V52 (%)|Median V156 (%)|Difference of medians (pp)|Infinity V52→V156|V3|V4|
|---|---:|---:|---:|---:|---:|---|---|
|QR33|6|6.684852366728319|−1.128119388725638|−7.812971755453957|6→9|SUPPORTED|SUPPORTED|
|QR33|24|40.470336525635894|5.019413971270939|−35.45092255436495|3→9|SUPPORTED|SUPPORTED|
|QR4|6|3.261142455403745|−0.9538965507957784|−4.2150390061995235|5→7|NOT_SUPPORTED|SUPPORTED|
|QR4|24|24.88331399320492|6.213226757036931|−18.670087236167987|4→9|SUPPORTED|SUPPORTED|

The primary QR33 V3 and V4 are SUPPORTED under the unchanged prespecified thresholds. QR4 is separate sensitivity, not a substitute for the primary method.

## Interpretation limits that must survive writing

1. H6 long validation also shifts its endpoint by18 weeks and changes the segment-anchored refit phase. These outcomes cannot identify a causal length-only effect. The design and figure caption correctly state this.
2. V3 uses the difference of across-series arm medians. For H6 QR33 that difference is−7.81297pp while the median paired change is0. The paper must not translate the former into a claim that a typical individual series improved by7.8pp. H24 median paired change is−44.09888415118933pp, also a different estimand.
3. Neither median improvement nor increased infinity selection supplies a universal protection guarantee or an independence test across13 related dealer aggregates. H24 regression's long-validation median still exceeds F by5.019413971270939%; retain this adverse result.

Checked files: protocol/v13/nyfed-validation-length-design.md; v13_validation.py; v13_validation_runner.py; run_v13_validation.py; report_v13_validation.py; test_v13_validation.py; results/v13/nyfed-validation/{rows,candidates,cell-results,summary,runtime,code-seal,output-manifest}.json; and381 old/286 new terminal report records. No files outside this new note were edited by the independent review.
