# Fresh-attempt AR diagnostics: implementation evidence

This task implements only the separately designed adapter, its artificial
tests, the new design, and this note. It does not change the retained builder,
its forty-six-file freeze, canonical plan/readback, scientific model code,
data, manuscript, or historical results. It does not run an auditor, earlier
financial phases, real AR replay, or the actual diagnostic CLI. No real source,
private trace, or new financial count was read. Agent time is zero root credit.

## What is connected

`reproduce_ar1_diagnostics.py` accepts an explicit audited replica, AR attempt,
readback path and readback SHA-256, fresh diagnostic ID, and independent code
freeze hash. Bootstrap is standard-library-only. It verifies its own code and
actual local import closure before loading the retained builder from checked
bytes. That builder verifies its unchanged historical contract and supplies
the unchanged numeric snapshot loader and statistical/parser/identity helpers.
The old fixed `execute`, `verify_context`, and `validate_readback` are not used
to accept fresh provenance. No plan is replaced or patched, including in
memory.

The new readback must be a task-owned state JSON and match the explicitly
provided hash, version-two scope, original scientific identities and auditor
code hash. Its manifest hash is then checked against the actual chosen AR
manifest. Actual replica/execution verification and unchanged manifest/cell
checks bind the manifest to the replica, AR ID, new selection hash and
original parameter-selection matrix. The adapter does not generate or copy an
upstream PASS receipt. The new private input-binding record explicitly has
`role=INPUT_BINDING_ONLY` and `upstream_receipt_generated=False`.

Complete eight-cell trace loading, exact origins, floor/refit pairing, finite
floor-respecting reports and nested target ordering use the retained helpers.
The two complete diagnostic CSVs are compared against the frozen reference
tables, with exact keys, full ordered headers, units/status/origin labels and
fixed short/long horizon labels. Ordinary numerical differences remain public
comparison results. `AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED` does not imply
`exact_csv_byte_agreement` or `exact_csv_scalar_agreement`.

Final checks cover every code/reference snapshot, original replica inputs,
fresh readback, manifest, consumed public/private artifacts, input-binding
record and new output bytes. The success audit is written/read back last.
Created public files are registered before writing; an ordinary exception
quarantines partial CSV/comparison/audit files privately and retains a sanitized
STOPPED receipt. Output attempts are exclusive and never overwritten. A hard
kill or unrecoverable storage failure can prevent a complete postmortem;
missing success evidence is not a passed run.

## Tests, failures and independent review

The missing entry, execution API and help flags were observed failing before
implementation. The first full artificial binding suite passed fourteen
tests; additional compatibility/failure tests brought that to eighteen.
Independent same-model static review then identified that fixed
`short_horizon`/`long_horizon` labels were being treated as mere numerical
disagreement. A separate check found that dropping a reference numeric column
could similarly produce VERIFIED with incomplete comparison. Two artificial
fixtures deliberately updated the audit export hash and new freeze as well as
the bad CSV; both demonstrated the semantic omissions as RED tests. The
minimal fixed-label and full-header checks made both GREEN. Independent review
confirmed the final fix and found no material issue within that delta.

Tests build isolated artificial full eight-cell inputs under this task's
`.scratch/revision-20261022/ar1-diagnostic-reproduction-tests`; each cleanup
removes only its own `TemporaryDirectory`. The old artificial fixture supplies
the previously verified external original-replica context; measurement is the
other injected seam. Real snapshot loading, traces/headers, CSV identities,
labels, alignment and output/failure paths run. Artificial receipts are fixture
data, never substitutes for real receipts. The reference independent-readback
file is byte-pinned, not semantically re-audited by this adapter.

Coverage includes changed timestamps/AR IDs/new selection hashes with identical
diagnostics, continued rejection by the old fixed entry, wrong explicit
readback/code hashes before context access, readback-to-manifest mismatch,
wrong scientific/auditor identities, wrong replica/attempt/selection context,
resealed origin/refit/floor failures, reference duplicate keys, exact one-ULP
public scalar differences, retained unfavorable outcomes, final trace/readback/
binding changes, output collisions, resource stops, and partial CSV/comparison/
success-audit writes. The partial-write tests really write seventeen bytes
before throwing and verify private quarantine.

Final bounded verification used CPython 3.12.14, `-B`, all five numerical thread
environment variables set to one, and `unittest` on the new
`test_reproduce_ar1_diagnostics` plus retained `test_build_ar1_diagnostics`.
**42 tests passed in 29.769 seconds**: twenty new tests and twenty-two retained
tests. macOS `/usr/bin/time -l` measured 29.83 seconds wall time, maximum RSS
61,931,520 bytes and peak memory footprint 48,398,912 bytes. This is a bounded
synthetic compatibility run, not a full-repository or production-run claim.
Artificial guard readings do not establish actual production thread/RSS
acceptance. Production uses the existing measured guard with one requested
numerical thread, maximum two observed OS threads, 540-second wall budget,
1.5 GiB RSS and a 600-second alarm.

## Final identities and root handoff

- `reproduce_ar1_diagnostics.py`: 19,162 bytes,
  SHA-256 `0a3f20c3eea20f3b0b5785a47f97c1437783182a88ae89f3e7093fa2a87d9156`.
- `test_reproduce_ar1_diagnostics.py`: 17,767 bytes,
  SHA-256 `f4453b97c2a084c01f3f88500d68e453284fadca4a81dd76e02260884a8f1df5`.
- `notes/revision-20261022/ar1-diagnostics-reproduction-design.md`: 5,988 bytes,
  SHA-256 `74d74e31c49503055ea3e6d5b38c99b142b9edd0a452f0b4bf2694eb8db75937`.

A hash-only check confirmed all forty-six retained snapshots still match their
freeze. `required_freeze_paths()` returns fifty-four paths without numeric
imports: those forty-six plus the following eight:

```text
notes/revision-20261022/ar1-diagnostics-reproduction-design.md
protocol/revision-20261022/ar1-diagnostics-executable-freeze.json
reproduce_ar1_diagnostics.py
results/revision-20261022/ar1-diagnostics/ar1-diagnostics-audit.json
results/revision-20261022/ar1-diagnostics/ar1-floor.csv
results/revision-20261022/ar1-diagnostics/ar1-horizon.csv
results/revision-20261022/ar1-diagnostics/independent-readback.json
test_reproduce_ar1_diagnostics.py
```

Reference artifact SHA/length checks matched the root-provided identities;
their contents were not parsed for development. The root must create
`protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json` with
exact fields `version=1`, `status=FROZEN`, timezone-aware `created_utc`,
`retained_freeze_path`, `retained_freeze_sha256`, `design_path`,
`design_sha256`, and `files` mapping the fifty-four paths to exact SHA-256
values. The new freeze itself and this implementation note are not entries.

The implementation is stable and stopped at the synthetic-reviewable handoff.
No new freeze, genuine upstream readback, actual diagnostic output, publication
or new financial finding was produced by this task. Those steps belong to the
root under the authorized separate execution contract.
