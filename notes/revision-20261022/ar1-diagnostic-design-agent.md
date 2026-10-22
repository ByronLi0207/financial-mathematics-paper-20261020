# Design only: separate AR floor and horizon diagnostics

22 October 2026. This is a bounded, explicitly post-result descriptive addition. The assigned purpose is to close the later AR report's omission from the original floor/coherence scope, without changing forecasts, choosing another model, repairing crossings, or expanding the original diagnostic files. This note is the only output of this design pass. No real AR trace, raw financial source, or new AR coherence result was read; no diagnostic computation, model fit or implementation was executed. Agent work credits zero root research time.

## Recommended minimum and alternatives

Use a new read-only wrapper with **eight floor rows and four H6/H24 pairs**, on the complete previously declared evaluation origins. Reuse the existing pure event functions after verifying their code identity and import dependencies. The wrapper should consume one explicitly named successful AR attempt and its accepted version-2 independent-readback receipt; it should not call either old diagnostic main or the AR runner/verifier main.

Appending AR into the existing 90/45 tables would blur their historical scope and alter protected artifacts, so reject that approach. Independently rewriting the event kernels would add definition drift without a scientific benefit; reserve an independently implemented scalar count oracle for synthetic verification. The recommended wrapper therefore adds provenance, inventory and alignment, while retaining the original event definitions.

Scope is fixed before reading the new counts:

| Source | Complete issue origins, inclusive | H | W | Refit spacing |
| --- | --- | --- | --- | --- |
| FX |11927–18551; 6,625 origins|6 and 24 records|720 and 2880|24 records|
| NYFed aggregate |405–681; 277 origins|6 and 24 records|52 and 260|13 records|

Floor keys are exactly `(source,H,W,AR1_REPLAY)`, eight unique keys. Horizon-pair keys are exactly `(source,W,AR1_REPLAY)`, four unique keys. H denotes record steps. Do not reindex by elapsed hours, reinterpret NYFed as live publication dates, pool sources, use only the 24 independently sampled reports, replace the full grid with a sparse grid, or add annual selection. Zero and unfavorable event counts must remain.

## Reusable interfaces and frozen evidence

The current pure functions are `floor_diagnostics(peak,capacity,floor)` in `build_conditional_diagnostics.py:39–52` and `horizon_diagnostics(short_capacity,long_capacity,short_peak,long_peak)` at lines55–64. `_vectors` checks aligned finite nonempty vectors. The horizon function deliberately leaves origin/floor pairing to its caller; the new wrapper must supply that missing boundary. Importing this module must not execute its `main()` or its output-writing functions.

Current helper identities, inspected without executing them:

| File | SHA-256 |
| --- | --- |
| `build_conditional_diagnostics.py` | `175f18df69989af096bfe0df32f7b4cc43065c89c59a55dd39141197b9b53b04` |
| `build_conditional_results.py` (import dependency) | `9f87c689dd20027e223a423f427380cba7179f78565c0cf4fc896274be1776ab` |
| `verify_ar1_output.py` | `c74461cc2d06455cc7504547cfc02824e6e80235dc8e9e7127bd39678f4bbf92` |
| `run_ar1_replay.py` | `82b6ce9502931a7b81a7974558d61657ce28172a19ba08f97bd0fbc9b87f4cb3` |

The AR specification hash is `e9f40722e4b012b57a0eb0158d101b5bf6cd327586ced6e270d822adf4f8a9a2`; its executable freeze is `57a880384d1a978f4f37b18eeaed1716b21db1f48b88c1375a7b5348c5421261`. The original 16-file scientific freeze remains `e88dfe0d53eb00a8210cb6c3b1203a16f5dfa22d928d4c3b3e2090e1cd0513cb`, and original selection remains `531bdc287da634a4a09b9cb3311882c2f005baf2b89f2b62523aca4d955c76d7`.

Add a separate before-diagnostic execution manifest binding this plan, the new wrapper/tests, the pure helper and its actual import closure. Existing frozen scientific identities can be referenced and reverified; none may be edited. A normal Python import must have all executed dependencies covered by those identities, including `build_conditional_results.py`; hashing only the named event function's enclosing file is insufficient. Where a custom byte loader is used, execute/parse the already verified snapshot instead of reopening a path. This is a diagnostic execution contract fixed after the original outcomes, not a confirmatory pre-analysis plan.

## Input identity, target and pairing boundary

Require explicit replica path, existing AR attempt ID, accepted v2 readback path plus its expected SHA-256, and a fresh diagnostic output ID. Resolve them with the existing symlink-safe task boundary. No automatic search for a favorable successful attempt or fallback to an older readback is allowed.

1. Verify the existing replica context and AR execution identity using the non-running `prepare_replica`/`verify_execution` interfaces. Require all eight AR cells complete. A source need not be loaded again: this supplement diagnoses the retained, already verified realized target and report vectors. It does not claim an additional independent source-label reconstruction or additional OLS/replay oracle.
2. Verify the accepted readback bytes, `version==2`, `AR1_INDEPENDENT_READBACK_PASS`, eight cells, its manifest/spec/freeze hashes and its exact-inventory flags. Its `code_sha256` must identify the accepted verifier. Bind the actual readback byte hash into the new audit; a generic PASS string is insufficient. Preserve its distinction between whole-record metadata checks and only 24 sampled Fraction fits/24 scalar reports.
3. Read the original AR manifest from the explicit attempt. Its hash must equal that named in the accepted readback. Check the complete eight-cell receipt inventory, specification, original/new selection and source identities. Reuse `verify_export_inventory`, `verified_bytes`, `check_output_headers` and `verify_cell_receipt` as appropriate; do not silently accept undeclared or duplicate artifact names. Parse JSON/CSV/NPZ from the same checked bytes, with `allow_pickle=False` and the existing exact six-array NPZ schema.
4. For each cell require `origins` to equal the entire fixed contiguous vector, in order and without duplicates. Check expected `int64`/`float64` types, finite arrays, expected length, `B>=0`, `P>=B`, `C>=B`, and the declared refit schedule. Read the existing hash-bound AR summary and reconcile its source/H/W/method labels, origin count and strict breaches with the new floor partition. This is an arithmetic consistency check, not new accuracy selection.
5. For each of the four pairs require exact matching source, W, method, ordered origin vector and floor vector, with short H6 and long H24. Their refit schedule is the same; their H-specific mature training sets and fitted coefficients need not be the same. Never use an inner join, reorder one side, truncate to a shared prefix or substitute a different W.
6. Verify `P6<=P24` at every paired issue before counting report crossings. Such target order follows from nested recorded windows even when source timestamps have gaps. An order violation is an integrity failure, not a model result. Check the input plan, code, manifest, accepted readback, consumed artifact identities and protected archive identities again before accepting final output.

## Published aggregate definitions

The floor CSV should use source, native unit, H, W, method, status and an explicitly empty tuning-parameter field, then the existing kernel fields: total count, `zero_headroom_outcome_count` (`P==B`), exact `floor_binding_count/rate` (`C==B`), binding-group breach count/denominator/rate/reason, and other-group breach count/denominator/rate/reason. Optional first/last source indices and an origin-vector hash give bounded public provenance without exporting any observation or forecast.

Use strict `P>C`; equality is not a breach. Binding uses exact stored equality, not `isclose`. The two denominators partition the complete n; their breach counts sum to the accepted total. If the binding denominator is zero, retain null rate and `NO_FLOOR_BINDING_ISSUES`; if the other denominator is zero, retain null rate and `NO_OTHER_ISSUES`. A nonempty group with zero breaches has rate zero and no undefined reason. Binding forecasts and outcomes with `P==B` are different events.

The horizon CSV should use source, native unit, W, method, both horizons and empty parameter labels, then total paired count, `strict_crossing_count/rate`, `maximum_positive_crossing`, `mean_positive_crossing`, and target-order-violation count. Define the positive difference as `(C6-C24)+`. Its mean divides by **all n paired origins**, not only crossing cases; the maximum and mean are zero when no crossing occurs. Monetary magnitudes stay in the source's native units. No cross-source mean, hypothesis test, confidence interval, reconciliation or favorable subset is added.

Report all four rows regardless of sign/frequency. A high crossing count is a valid diagnostic result. The fixed helper raises if any target order is invalid, so a VERIFIED output has zero target-order violations; never publish nonzero target-order violations as if they were empirical forecast incoherence.

## Output, failure and resource rules

Create a new sibling task-owned directory such as `<explicit-replica>/ar1-diagnostics-SAFEID/{public,private}` with exclusive creation. Do not write inside the original AR attempt, overwrite a prior diagnostic, touch the original 69-file core, or change the original 90/45 files. Proposed new public files are `ar1-floor.csv`, `ar1-horizon.csv`, and `ar1-diagnostics-audit.json`; canonical publication can copy those new aggregate files into a separate `results/revision-20261022/ar1-diagnostics/` directory after verification.

The audit binds the accepted readback, original AR manifest, all eight cell receipts/private trace hashes, summary, source/spec/selection identities, new plan/helper/wrapper/test identities, exact eight/four key sets, origin counts/hashes, output bytes/hashes, actual resource measurements and explicitly post-result/no-refit/no-repair flags. It must not claim execution independence, new unobserved validation or a stronger numerical oracle than its input readback actually performed.

Any missing/incomplete input, wrong identity/schema, alignment failure, invalid floor/target, unexpected exception or resource stop makes the entire supplement STOPPED. Preserve a sanitized failure receipt and any partial work privately; do not label a subset eight/four-complete or score a shortened segment. No retry with looser equality, thresholds or selected origins is allowed. Conversely, crossings, floor binding and adverse partitions never trigger failure or report adjustment.

Use one process, one requested numerical thread, at most two observed OS threads, the existing internal 540-second/1.5GiB budget and 600-second hard stop. Import numeric modules only after the requested environment and dependency preflight. No source fetch, original forecast fit, residual replay or scenario cube is necessary. Retain only the validated one-dimensional arrays needed for the four pairings; memory should be small, but actual elapsed time/RSS/thread snapshots must still be recorded. Import/help and synthetic tests must not locate real private data.

Protected existing CSV identities are floor `c874905a9fcc454cf08aec69738d2bc61dc5364716c940a94f5c7211bf4e0863` and horizon `59bc82949da1642daed554ed0fcc2f9d16f989773a988cb11ecbd297fa6a5a5a`. They were only hashed during this design pass; no new AR diagnostic result was inspected.

## Meaningful synthetic acceptance before implementation is accepted

- Hand-count mixed events: `B=[1,1,1,1]`, `P=[1,2,1,2]`, `C=[1,1,2,2]` gives two binding reports, two zero-headroom outcomes, binding breaches1/2 and other breaches0/2. Add exact equality and `nextafter(B,+inf)` to distinguish strict breach, outcome equality and stored binding.
- All-binding, no-binding and all-zero cases exercise both null denominators and the difference between no events and zero observed risk within a nonempty event group.
- `C6=[3,1,3,2]`, `C24=[1,2,3,2]` gives one crossing, rate1/4, maximum2 and all-origin mean0.5 under valid nested targets. Also test zero crossings. Count positive report crossings normally, but reject a single `P6>P24`.
- Reject nonfinite/empty/misaligned arrays, negative floors, `C<B`, `P<B`, wrong typed NPZ headers, missing origins, permutations, unequal floors, wrong source/W/H and complete-length substitutions from another cell.
- Keep row counts unchanged while duplicating one key and omitting another; reject both output-inventory and input-cell substitutions. Check all eight/four rows, including zero-event cases, against an independent scalar-loop oracle.
- Reject missing/duplicate export entries, changed consumed bytes, a PASS receipt for another manifest, incorrect source/selection identity, and file changes after first reading. A changing-file fixture must demonstrate snapshot parsing rather than a hash-then-reopen race.
- Run one complete artificial eight-cell wrapper fixture with real new guards and exact file identities. Assert no calls to fitting, `predict`, replay, forecast repair, old diagnostic main or source loading. Verify unchanged input bytes and protected outputs, exclusive output refusal, and a stopped-phase receipt without VERIFIED partial tables.

An independent design reader checked the event/denominator/alignment traps from the same interfaces and reached the same eight/four recommendation without reading traces or executing diagnostics. This design does not predict whether AR will cross, whether it will bind its floor, or whether either phenomenon explains its loss. Exact stored binding cannot recover unprojected scenarios or conditional outcome atoms; separately fitted horizon reports need not inherit the realized target's monotonicity. A forecast H6 report is not a known lower bound for P24, so this supplement supplies no automatic pinball-improving horizon repair and no novelty or coverage claim.
