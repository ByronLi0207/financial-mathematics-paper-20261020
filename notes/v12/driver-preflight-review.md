# v12 parent/worker preflight review

Snapshot reviewed: 2026-10-25T11:25:04.263593+00:00. Scope: read-only integration review of `run_v12_studies.py` and `v12_runner.py` against frozen F1/F2/F3. `v12_summaries.py` and the existing toy tests were read to verify row consumers. Only this note was added. No actual financial input, fit, prediction, label score, pilot, or experiment run was launched.

**Current snapshot has prelaunch integration issues.** Existing tests pass, but do not cover the method-reduction integration or hard-stop result recovery. Findings were sent to the coordinating task immediately. This note records the reviewed snapshot; later edits need targeted readback before treating a finding as resolved.

## Findings

### 1. F2 QR4 omission is declared but ignored by the worker (P1)

`run_v12_studies.py:108-111` records `methods=['QR33']` when resource planning omits QR4. `v12_runner.py:166` nevertheless fixes every F2 geometry to `('QR33','QR4')`, without reading the cell's methods field. The parent then prefers any actual worker row at lines290-293, so an omitted QR4 will be fitted, reported COMPLETE, and charged against the same budget. This invalidates the predeclared method-reduction plan.

Reproduced on the existing constructed local fixture, without financial data:

```text
cell, cache, out = test_v12_runner.fixture(temp_directory, 'F2')
cell['methods'] = ['QR33']
result = v12_runner.compute_cell(cell, 'F2', cache, out)
requested_methods: ['QR33']
actual_methods: ['QR33', 'QR4']
statuses: ['COMPLETE', 'COMPLETE']
```

Required correction: honor and validate a declared method subset in the worker, and keep omitted methods as resource-omitted planned public slots. The protocol permits whole QR4 omission; it does not permit claiming that omission while still fitting it.

### 2. F2 method execution order is inconsistent with the frozen queue (P1)

Frozen F2 runtime order is all eligible W52 QR33, then all W260 QR33, then QR4 W52, then QR4 W260 (`protocol/v12/validation-length-design.md:438`). The parent groups by source/W at `run_v12_studies.py:136-143`, and each worker processes both methods for both V arms before the next queued source/W group. Thus QR4 starts before all primary QR33 slots have had their declared opportunity. Under a hard cap this can consume the primary-method/F4 reserve on the secondary method.

The V52-before-V156 order inside a group is correct: `group_jobs` sorts by validation_n and `worker_job` does the same. The error is cross-source/cross-method phase order, not the nested V ordering.

Required correction: make the scheduler's method phases explicit while retaining the V52/V156 same-source/W identity reuse and terminal failed-cache policy. Merely changing `compute_cell` to honor a method subset does not fix the full-scope ordering unless jobs are separated by method.

### 3. F2 whole-source exclusions are recorded but not removed from execution (P2)

`run_v12_studies.py:239-246` performs full-source prechecks. Lines247-252 set `eligible=False` for a failed source, but cells was already built at line237 and is not filtered using the finalized eligibility before forming `remaining` at line272 or launching at line280. Excluded source cells therefore still enter the worker queue. The eligibility record's old `status='ELIGIBLE'` also remains while `eligible=False`, producing contradictory public metadata.

Frozen F2 requires whole-contract exclusion before any model and a fixed remaining K (`protocol/v12/validation-length-design.md:429`). Filter execution using the finalized eligible source_keys, preserve explicit excluded inventory outside the comparison denominator, and update the eligibility status as well as its Boolean/reason. Also handle an eligibility entry missing from source_status (possible for a metadata/history exclusion that was filtered by cells_for), rather than indexing it unconditionally at line251.

The current pinned N877 sources are all history-eligible, so the missing-key case is a code-path robustness issue; no claim is made that an actual source currently fails. The missing execution filter itself is present in the reviewed code.

### 4. Hard-killed jobs discard completed earlier scalar results (P1)

`v12_runner.py:256-262` accumulates results in memory and emits one JSON only after every grouped cell returns. The parent reads only final stdout at `run_v12_studies.py:184-192`. If a grouped F2 job completes V52 and is then killed while V156 is active, the completed V52 result is not recoverable through the parent path. A hard-killed F1 job can likewise lose an already completed method while the other method is active. The parent substitutes failed rows for every absent result at lines286-301.

Cooperative ResourceStop usually returns a terminal JSON, and trace caches/selections are durable. However, the parent explicitly implements SIGTERM/SIGKILL fallback at lines171-178 and201-208, so the hard-stop path must retain already completed method cells too. Frozen runtime/failure policy requires retaining complete earlier cells; a grouped process must not become the scientific completion unit.

Required correction: persist scalar per-cell/per-method receipts as each completes and have the parent salvage verified completed receipts after hard termination. This must reuse existing results, without rerunning a fit or replacing a failed attempt. Terminal candidate caches alone do not currently materialize the lost public rows.

### 5. F2/F3 relative arithmetic can be nonfinite while row remains COMPLETE (P2)

`v12_runner.py:219-222` checks only that F is positive before setting COMPLETE and calculating relative excess. Finite positive F and finite actual loss can still overflow the ratio; `_clean` serializes the resulting infinity as a string at lines33-38 while status remains COMPLETE. `v12_summaries._usable` then rejects it, so predictions treat it as unavailable but parent runtime counts it complete (`run_v12_studies.py:320`). F1's `decompose` already checks finite relative components.

Required correction: validate the computed F2/F3 relative quantity before marking the row COMPLETE, retaining raw means and a failed relative-decomposition reason on failure. This is a numerical contract fix, not a threshold change. No assertion is made that actual financial means attain such extremes.

## Confirmed integration alignment

- Worker job schema matches the parent: `spec.cells`, `cache_root`, `output_root`, cap_seconds, cell_cap_seconds and expected_code_sha256 are read; output supplies `cells`, flattened `rows`, and `candidates`. Parent reads `data.cells` only after checking flattened rows is present.
- Each worker constructs full consecutive validation/evaluation origins from cell endpoints, verifies declared counts, compares forecast origins/refit_indices with those exact vectors, and scores aligned full vectors (`v12_runner.py:131-140,179-182`). The prior review's uniformly truncated-segment boundary is now covered at the worker boundary.
- Both validation selections are based on the v12 all-six selector and are durably sealed before any reference/candidate evaluation (`v12_runner.py:184-203`). F1 evaluates all six candidates; F2/F3 evaluate only the sealed selected candidate. No successful-subset fallback was observed.
- Failed or stale candidate caches are terminal; cache identity includes source hash, aligned grid, H/W/d, scales, tau, forecast code and the full origin fingerprint. Trace hash/vector/refit/score summaries are validated before completed reuse. Infinity aliases exact I consistently.
- F1 complete rows include signed actual_excess_pct, selection_component_pct and signal_gap_pct; F2/F3 assign relative_loss_pct at line229, matching the summary consumer identity and validity checks. F2/F3 do not invent oracle components.
- Parent F1 prediction receives only F1 rows. F2 uses finalized eligibility dictionaries, and F3 supplies source_key fx_hourly/PDPOSGS-B conventions from the inputs module, matching expected summary slots.
- F1 scheduling prioritizes CFTC, panelW52, bill, panelW260, FX. F3 prioritizes .99 CFTC, both FX periods, bill, then .90. The parent queue contains a finite precomputed inventory and starts at most four normal workers; hard deadlines terminate active children. Worker caps are explicitly finite and positive before computation (`v12_runner.py:247-248`). No protocol mutation call appears in either driver.
- Protocol readback, standalone-ancestor check, frozen inherited-code hashes, committed v12 code checks and worker code-seal checks occur before the first model. The parent source preflight is before start_jobs.

## Toy verification

Existing suites executed with the authorized offline cached uv environment:

```text
python -B -m pytest -q -p no:cacheprovider test_v12_studies.py test_v12_runner.py
```

Observed: **19 passed in36.21s**, exit0. Separately, the constructed F2 methods=['QR33'] reproduction above exited0 while demonstrating the incorrect extra QR4 work. No actual source/evaluation call was made by the reviewer. The passing tests do not resolve the findings.

## Reviewed source hashes

| Path | SHA-256 |
|---|---|
| `run_v12_studies.py` | `eccac3f32bd0526274fbb52eac1fcb75095ed92d73b7b3445aa2af16c84ecff6` |
| `v12_runner.py` | `3b8032a6cf8289f1c1a9f49189a37bc36f07a322a603c9d1fca1634f67494890` |
| `v12_summaries.py` | `78caf8e4ccbe27e98d04311a94a747500b1c6acab5ad73144c9e31323cd70893` |
| `protocol/v12/loss-decomposition-design.md` | `cf8a38f734fc22ffa0e8895c2ea34d698ec26c92c31a2835888c464161b858d1` |
| `protocol/v12/validation-length-design.md` | `14192e8ccb8cf8cde9b53e65d20c871b93c537deb9cfdd39cac09e5cf6578819` |
| `protocol/v12/tau-design.md` | `366c56a57983cbe8c9569abf626f2d5947166b66fd0a2ca2fa23a444dcd8943c` |


## Static remediation readback — 2026-10-25T11:34:03.668633+00:00

This is an append-only follow-up on the parent/worker fixes. No tests were repeated and no financial run was launched. The coordinating task reports parent11 and worker26 toy tests passing; those numbers are reported evidence from the coordinator, not reruns by this reviewer. The static findings below refer to the hashes at the end of this appendix.

| Original finding | Readback disposition | Current evidence |
|---|---|---|
| 1. F2 QR4 trim ignored | RESOLVED | `v12_runner.py:181-186` reads and validates declared method subsets before source loading. F2 permits QR33-only/QR4-only, while F1/F3 retain their declared full method scope. `run_v12_studies.py:150-155` creates jobs only for permitted methods. |
| 2. F2 method order | RESOLVED | F2 groups are built QR33 before QR4, with W52 before W260 and V52 before V156. `start_ordered_jobs` at parent lines276-288 waits for an entire method/window batch before the next. Actual run now calls it at line355. `merge_cell_results` at lines158-169 preserves both method rows and rejects duplicate method results. |
| 3. Source exclusion not applied | RESOLVED | `preflight_cells` at parent lines172-181 filters all geometry cells of each excluded source and updates failed-source eligibility status to EXCLUDED_ENTIRE_CONTRACT. It handles preexisting ineligible declarations without indexing an absent source_status entry. Run uses eligible_cells for pilot/remaining work at lines335,347, with excluded public rows at lines371-375. |
| 4. Hard kill loses completed rows | PARTIALLY RESOLVED; follow-ups below | Worker now writes per-method results, references, evaluation candidate receipts and a final cell receipt at `v12_runner.py:162-174,224,229,238,256`. Parent salvage is called on failed stdout and hard-stop cleanup at lines253,269. Valid completed receipts can survive without final stdout. Two boundary issues remain in the reviewed snapshot. |
| 5. Nonfinite relative loss COMPLETE | RESOLVED | Worker lines245-248 compute excess and require math.isfinite before setting COMPLETE; invalid relative output retains a failure reason and unavailable relative fields. |

### Follow-up A: partial JSON must not prevent recovery (P1)

`salvage_job` at `run_v12_studies.py:189-200` parses any existing cell-result.json and method/candidate receipts without handling malformed JSON. Worker `_write` opens a target and streams JSON directly (`v12_runner.py:41-45`); it does not atomically publish a fully written receipt. A hard stop can therefore leave an empty/truncated final cell-result.json after valid per-method receipts already exist. Parent salvage then raises instead of falling back to those completed methods. A truncated current candidate receipt can have the same effect.

Required follow-up: atomically publish receipts, or make salvage tolerate incomplete/corrupt current receipts per file and retain valid prior method receipts. Do not refit or convert an incomplete record to COMPLETE. A complete-file hard-kill test does not cover a partially written current receipt.

### Follow-up B: method-split queue state must remain method-specific (P2)

F2 now splits one geometry into method-specific jobs. Parent still builds omitted_ids and launched_ids from geometry cell_id only (`run_v12_studies.py:359-360`), and uses geometry-only omission at line370. If QR33 for a geometry was started and hard-stopped without a receipt while its QR4 job remained queued, the QR4 unstarted entry puts the same cell_id into omitted_ids. The missing QR33 row is consequently classified NOT_RUN_RESOURCE_LIMIT, masking its attempted FAILED_RESOURCE state.

Required follow-up: distinguish launched and omitted status by (cell_id, method) after method splitting. Keep source-level exclusions whole-contract and geometry-level planned inventory unchanged. Already present complete method rows are handled first and remain intact; this finding concerns absent result rows at a deadline.

Both follow-ups were sent to the coordinator immediately. No protocol or threshold alteration is needed.

| Readback file | SHA-256 |
|---|---|
| `run_v12_studies.py` | `9537ed6c7536ffbb1f4fc4b51a4dc29efaab562578ca37ddcf1e44dcf041e4ae` |
| `v12_runner.py` | `714ab36d47cee56947b131661ab2f9afb9f23529cea9f5b59f0424f2ad293e3b` |
