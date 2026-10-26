# v12 supplement migration record

Only `submission-v10/supplement.tex` and this new record were written. No main manuscript, model, archived result, data, Git ref or experiment changed. Compilation/rendering and the final page acceptance check remain with the parent.

## Exact source and destination

- Earlier main source: `452064866c2bdc4166b89d09d67b0cb2bc0ae415:submission-v10/manuscript.tex` (read-only Git object).
- Supplied relocation snapshot: `notes/v12/original-relocation-text.json`, SHA-256 `2f1e349f20e7b7e2966e640e10295c98dfbdfcba21e441ed9539deff2f60f2c5`.
- Supplement before edit SHA-256: `05b8beb8adfe26ad181d029e53f8f681aa0e57f63864579b859cbf9a569ea827`.
- Supplement after edit SHA-256: `41f70e1de4bca724df38cbb6e511a1f9fc9acf9975e2d93dbe2215b6e6733913`.
- Snapshot `/menu` is copied verbatim at line 1493, within existing S29 (`sup:v10-menu`), including its subsection, table input, figure/caption and original labels. Only its trailing FloatBarrier wrapper is omitted; the existing S29 clearpage already flushes its floats. `sec:extensions`, `tab:v10-menu-isolation` (in the unchanged generated input) and `fig:mechanism` remain the original labels.
- The existing S29 complete-source input remains once. Its technical/failure/threshold paragraphs remain after the migrated discussion. One redundant sentence without numbers was removed: “Old and expanded arms use identical source calibration, random streams, path geometry and forecasting clocks.” The copied passage already states that condition. A new scope sentence confines the old non-identification qualification to the paired simulated intervention.
- Snapshot `/limitations` supplies seven paragraphs copied verbatim into new S36 (`sup:v12-details`, line 1612); only its old main-section heading/label and trailing FloatBarrier are omitted. A historical-scope introduction precedes all seven paragraphs. Immediately after the paragraph saying longer weekly validation was untested, a new clarification states that the added CFTC experiment now tests longer validation windows on unchanged evaluation origins; prospective tuning stability remains unestablished.
- The requested three-sentence consistency paragraph is copied verbatim at line 1634; its source is the baseline main paragraph beginning “Separately fitted horizon forecasts”.

## Existing evidence not duplicated

- S7 (`sup:ar`, original lines 373–420) already contains the exact replay identity, mature scenario pool, fitted-coefficient convention, full comparisons/adverse results and original archive link.
- S8 (`sup:rank`, original lines 420–461) already contains the lower-minimizer/corrected-rank distinction, integer-rank endpoint qualification, full ablation and original archive link.
- S22 (`sup:coherence`, original lines 1115 onward) already contains the complete horizon-coherence table, including 640/140/91/80 crossings. Only the specifically requested main prose is copied; there is no second table.
- S28 already explains fitted dwell lengths, continuous state through switches, artificial last-to-first wrapping and plug-in calibration limits. Those existing source lines stay unchanged; the related old Limitations prose is also retained as explicitly requested historical scope.

## Other authorized edits and new-result evidence

- S2: only the Sussman attribution tail was removed. The strict-events/atoms proof and subsequent S2 discussion remain byte-identical. Preserved block SHA-256: `615fa84b42700e8c1c86c06a79ffb801b1119f090170416360de4ff48ec1b269`.
- S34: one current reproduction entry now points to revision-v12. The introduction identifies the v12 manuscript. Every prior versioned archive URL is unchanged.
- S36: added links to all `results/v12/decomposition`, `results/v12/validation-length` and `results/v12/tau` records, plus a 152-word source paragraph on method scope, finite-oracle interpretation, rank sensitivity and whole-cell failures. No new empirical point estimate is introduced. The unresolved highest-level CFTC/FX statement is supported directly by saved `results/v12/tau/predictions.json` and failed entries in `results/v12/tau/rows.json`.
- No AI declaration exists in this supplement source; none needed removal.

## Verification and pages

Passed structural checks: old S1–S35 titles/order retained, only S36 appended; all seven Limitations paragraphs and the complete menu body copied verbatim; consistency paragraph occurs once; original proof block identical; old archive URLs retained; menu summary and full-source inputs each occur once; original moved figure label occurs once; no new FloatBarrier or clearpage command.

Baseline: 34 pages as reported by parent. Edited page count: **pending parent compilation**. Visual QA and the maximum 38-page check remain **pending**. This record does not claim a successful compile or page count.

Actual diff review completed after the structural checks: `git diff --check -- submission-v10/supplement.tex` passed. The inspected diff contains 53 added and 3 removed source lines; the removals are the manuscript-version identifier, the authorized Sussman attribution tail, and the number-free repeated matching sentence replaced by the verbatim relocation block. Main-file search confirms the moved `sec:extensions` and `fig:mechanism` labels no longer occur there. No compilation was inferred from these source checks.
