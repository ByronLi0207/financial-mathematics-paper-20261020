# Fresh-attempt AR diagnostic reproduction: bounded adapter design

This addition connects an explicitly chosen, already audited fresh AR attempt
to the existing eight floor and four paired-horizon diagnostics. It preserves
the retained-artifact audit and all of its rejection conditions. It does not
run an auditor, sources, models, repairs, or earlier replication phases. A
fresh version-two readback must already exist, produced through the separate
auditor's normal entry point. No receipt is copied or manufactured by this
adapter.

## Entry, scientific contract, and identities

The new standard-library-only entry is `reproduce_ar1_diagnostics.py`, with
mandatory `--replication-dir`, `--ar1-attempt-id`, `--readback`,
`--readback-sha256`, `--diagnostic-id`, and `--freeze` arguments. The last
argument pins the new independent code freeze at
`protocol/revision-20261022/ar1-diagnostics-reproduction-freeze.json`.

The freeze has exactly these fields: `version=1`, `status=FROZEN`, a
timezone-aware `created_utc`, `retained_freeze_path`,
`retained_freeze_sha256`, `design_path`, `design_sha256`, and a `files` mapping.
Its exact inventory is the retained diagnostic freeze's forty-six snapshots,
that retained freeze file itself, the new entry/test/design, and the four
reference artifacts in `results/revision-20261022/ar1-diagnostics/`:
`ar1-floor.csv`, `ar1-horizon.csv`, `ar1-diagnostics-audit.json`, and
`independent-readback.json`. Local Python imports are included conservatively
in the required closure. Main-paper files and the implementation note are not
runtime dependencies.

Initial bootstrap checks the new freeze hash and every snapshot before loading
any local helper. The retained builder then executes from its checked bytes,
verifies the unchanged retained freeze, and provides its unchanged snapshot
loader. Its canonical plan continues to bind the historical manifest and
readback; it is never patched, substituted in memory, or presented as proof of
the fresh attempt. Only its fixed scientific definitions and source contracts
are reused. The fresh binder is a distinct, explicit acceptance path.

The input readback is restricted to a task-owned state path, read from checked
bytes, and pinned by the mandatory readback hash. Its actual manifest hash,
version-two PASS/scope fields, auditor code hash, scientific spec/freeze, and
resource receipt must agree. Because this receipt does not independently name
the replica or new selection, actual `prepare_replica`/`verify_execution` and
the retained manifest/cell-receipt checks must bind those fields through the
manifest. A fresh timestamp, attempt ID or selection-receipt hash is allowed;
the original scientific contract and selected parameter matrix are unchanged.

Before numeric trace parsing, an exclusive new sibling
`ar1-diagnostics-reproduction-ID` is created inside the explicit replica. A
private input-binding record fixes the exact fresh readback/manifest bytes,
replica, AR attempt, original and new selection identities, and code freeze.
It records these identities without claiming that the adapter produced the
upstream PASS receipt. The reference audit's export hashes must match the two
reference CSV snapshots; its retained freeze/plan/manifest identities must
match the unchanged historical baseline.

## Small orchestration, unchanged statistics

Reuse the retained builder's snapshot loader, manifest/trace/receipt/vector
checks, summary inventory, `floor_row`, and `horizon_rows`; reuse its dependency
CSV and resource helpers. Do not call its fixed `execute`, `verify_context`,
or `validate_readback` on fresh inputs. The adapter adds only bootstrap, fresh
binding, and output orchestration. It requires all eight cells, full origins,
exact floor/refit pairing, finite floor-respecting reports and `P6<=P24`.
Unfavorable crossings and zero events remain valid.

Write both complete diagnostic CSVs and a separate comparison JSON using the
existing exact per-cell CSV comparison. Check reference and new table keys and
labels before comparison. `AR1_DIAGNOSTIC_REPRODUCTION_VERIFIED` means the new
input contract and computation passed; `exact_csv_byte_agreement` and
`exact_csv_scalar_agreement` report numerical agreement separately. Differences
never trigger a model rerun, a tolerance adjustment, or a repaired report.

Recheck old/new code snapshots, reference files, fresh readback, manifest,
consumed public/private artifacts, input-binding record and new output bytes
after the final resource checkpoint. Register created public outputs before
writing, quarantine partial files privately on ordinary failure, retain a
sanitized STOPPED receipt, and never overwrite an attempt. Hard kills or
unrecoverable storage failure can leave no complete postmortem receipt.

The adapter retains one process/one requested numerical thread, maximum two
observed OS threads, 540-second wall budget, 1.5 GiB RSS and 600-second alarm.
These are measured by the existing guard during real execution; artificial
test guards are not production resource evidence.

## Test and handoff boundary

Use only artificial full eight-cell fixtures under this task's `.scratch`.
Tests first demonstrate the missing entry and fresh-binding behavior, then
cover exact numerical reproduction with changed provenance, mismatch between
readback and manifest/context/selection, changed code or input snapshots,
complete 8/4 inventory, preserved adverse outcomes, independently changed CSV
cells, output collisions, cancellation and partial-write quarantine. Only the
preverified external-replica context and resource measurement may be injected;
actual snapshot/parser/label/alignment/output paths run. Preserve the old
entry's rejection of fresh identities in a regression test.

The root creates the new freeze and performs any later real execution. The
implementation task ends after bounded synthetic tests and an independent
same-model review; no real diagnostic counts or private vectors are inspected.
