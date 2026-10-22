# Separate AR replay diagnostics: implementation and synthetic acceptance

Prepared 2026-10-22. This note records implementation evidence only. The author
did not load either real source, inspect retained real AR vectors, compute real
new coherence counts, fit a model, run the production CLI, create the new
executable freeze, or publish results. Agent time is not credited to the root's
active research hours.

## Fixed scope and owned changes

Only `build_ar1_diagnostics.py`, `test_build_ar1_diagnostics.py`, and this new
note were written in this implementation task. The accepted plan remains
`protocol/revision-20261022/ar1-diagnostics-plan.json`, SHA-256
`ce909c660a6c838c236e21aaf6a2f5ee20c8ca916380d59f657e00f3b889ef30`.
Its NY unit token was corrected by the root to the original specification's
`USD millions` before any new diagnostic freeze or counts. This implementation
does not modify the original sixteen-file freeze, AR seventeen-file freeze,
original sixty-nine-file archive, prior ninety-row and forty-five-row diagnostic tables,
canonical manuscript, sources, old attempts, or existing readback receipts.

The production entry requires explicit `--replication-dir`, `--ar1-attempt-id`,
`--readback`, `--diagnostic-id`, and `--freeze`. It creates an exclusively owned
new sibling `ar1-diagnostics-ID` under the chosen replica. The outputs are eight
floor rows, four same-source/window paired-horizon rows, and a bounded audit.
There is no refit, hyperparameter choice, repaired capacity, rearrangement,
additional performance metric, or new inference. Existing pure floor/horizon
functions supply the same exact-equality and strict-inequality definitions.

## Identity and execution boundary

Import and help use the standard library only. Before numeric helper imports,
preflight verifies the mandatory separate freeze hash, its exact file inventory,
all file snapshots, plan/design identities, accepted version-two readback and
its auditor code identity, both prior scientific freeze maps, original
selection identity, source units/ranges/windows/cadences, and the exact resource
contract. The current conservative AST closure contains forty-six paths listed
below. It includes lazy local imports and test fixture imports, even when these
modules are not needed in the diagnostic path. An unbound new local import is
rejected. Imported local helpers execute from already verified byte snapshots;
the loader does not reopen Python sources for execution. This is not a claim
that the entry script validates itself before its initial Python execution.

The existing replica context preparation and AR execution-contract checks are
read-only. Production rejects an already imported local/numeric context; the
synthetic seam restores preloaded local modules after using isolated copies.
The program never invokes an existing helper's `main`, source loader, fitting,
prediction, or repair entry point. The accepted prior audit is a dependency,
not a claim that this supplement repeats its source-label, Fraction-OLS, or
recursive replay oracles.

The retained AR manifest must be the exact plan-bound manifest. Its eight cell
inventory, fourteen public exports, sixteen private artifacts, all labels and
receipt identities are checked. Traces are parsed from the same checked bytes
with `allow_pickle=False` and exact six-array headers. Every source uses its
full declared contiguous origin vector: 6,625 FX or 277 NY origins. Capacity,
peak and floor must be finite and respect `C>=B>=0`, `P>=B`; refit indices must
equal the fixed declared schedule. Each cross-horizon pair requires exact
origin/floor/refit equality and `P6<=P24`; there is no intersection, truncation,
or repair. Summary rows must have exactly eight unique source/H/window keys
and the fixed unit/method/status/count/cadence labels. Floor and nonfloor
breaches reconcile to the retained summary's strict breach count.

Checks repeat after aggregation and at the final checkpoint, including all
frozen snapshots, the original replica's inputs, all retained AR public/private
artifact identities, the AR manifest, and the exact newly exported CSV bytes.
The audit is written last and read back byte for byte. Ordinary exceptions
quarantine any already created CSV or success-audit file in the new attempt's
private directory and produce a sanitized STOPPED receipt and private partial
aggregates. Hard process termination, unrecoverable storage failure, or a kill
can prevent a complete postmortem receipt; absence of an audit is not success.

## Synthetic evidence and meaningful failures

The new suite uses artificial eight-cell traces with the full declared index
ranges. Temporary fixture roots are created only below this task's
`.scratch/revision-20261022/ar1-diagnostic-tests` and each test removes only its
own `TemporaryDirectory`. The fixture constructs fresh trace/receipt/manifest,
summary, accepted-audit and freeze identities. It does not copy real private
vectors or the bodies of the old diagnostic tables. Its external previously
verified original-replica context and measurement guard are injected; the new
loader, snapshots, NPZ/CSV parsing, inventory, alignment and output paths are
real. Consequently artificial guard measurements are not production resource
evidence.

The initial missing-module/API failures preceded implementation. Later genuine
RED-to-GREEN checks established that a resealed plan could otherwise redeclare
resource limits, that changing a retained input or exported CSV at the last
checkpoint could otherwise escape verification, and that a partial CSV or
success-audit write followed by `OSError` could otherwise remain in public.
These are fixed by the exact resource contract, final snapshot/artifact/output
checks, and registering every created output before writing its bytes. The
last two tests actually write seventeen bytes before raising; both failed
against the prior implementation and pass after the minimal fix. Independent
read-only review identified the partial-write issue. An early artificial
context integration error was corrected in the fixture's external-context
seam, not by disabling production input verification.

Other tests check complete 8/4 inventory and independent scalar counts,
same-snapshot module execution, invalid freezes before helper execution,
missing closure entries, hash changes, nonfinite/below-floor reports,
permuted origins, cross-horizon floor/target incompatibility, duplicate summary
keys, exact near-floor equality, empty subgroup null reasons, output collision,
resource cancellation, and preservation of failed artifacts. Unfavorable
crossings and zero events are valid outcomes; invalid target ordering fails
the supplement.

Final bounded command: CPython 3.12.14, `-B`, all five numerical-thread
environment variables set to one, `unittest` over
`test_build_ar1_diagnostics`, `test_conditional_diagnostics`, and
`test_verify_ar1_output`. **49 tests passed in 9.370 seconds**, comprising 22
new tests and 27 prior pure-synthetic compatibility tests. macOS `/usr/bin/time
-l` measured 9.48 seconds wall time and 62,324,736 bytes maximum RSS for this
test command; peak memory footprint was 49,349,184 bytes. This is not a whole
repository regression claim or a measured production diagnostic run. No
continuous OS-thread count was measured for this test command. Production
uses the existing measured `RunGuard`, one numerical thread, maximum two
observed OS threads, 1.5 GiB RSS, 540-second soft wall budget and 600-second
hard timer. Actual production measurements remain pending.

## Final identities and required freeze paths

- `build_ar1_diagnostics.py`: 28,444 bytes;
  SHA-256 `32fb5afc9d6b0ce3f520692cc8e75f38415cce7c0622f0d8cf7f4f2ca0f3c964`.
- `test_build_ar1_diagnostics.py`: 23,246 bytes;
  SHA-256 `304747d8635b7e3213fd2aeb38fc2dbc1687d3167d54d3e533641420b240fcab`.

The root must create
`protocol/revision-20261022/ar1-diagnostics-executable-freeze.json` with exactly
`version=1`, `status=FROZEN`, timezone-aware `created_utc`, `plan_path`,
`plan_sha256`, and `files` mapping the following forty-six paths to current
SHA-256 values. The separate freeze itself is not a self-hashed entry.
`required_freeze_paths()` returns this inventory without numeric imports or
private-data access.

```text
ar1_replay.py
build_ar1_diagnostics.py
build_conditional_diagnostics.py
build_conditional_results.py
conditional_features.py
conditional_quantile.py
conditional_sources.py
conditional_study.py
notes/revision-20261022/ar1-diagnostic-design-agent.md
protocol/revision-20261022/ar1-diagnostics-plan.json
protocol/revision-20261022/ar1-replay-design.md
protocol/revision-20261022/ar1-replay-executable-freeze.json
protocol/revision-20261022/ar1-replay-spec.json
protocol/revision-20261022/conditional-baseline-design.md
protocol/revision-20261022/executable-freeze.json
protocol/revision-20261022/selection-freeze.json
protocol/revision-20261022/study-spec.json
reconcile_conditional_replication.py
reproduce_conditional.py
reproduce_conditional_diagnostics.py
results/revision-20261022/ar1-replay/inventory-readback.json
results/revision-20261022/audit-builder-v01.py
results/revision-20261022/post-result-floor.csv
results/revision-20261022/post-result-horizon.csv
revision_selection.py
run_ar1_replay.py
run_conditional_study.py
run_study.py
study_core.py
study_data.py
study_report.py
test_ar1_replay.py
test_build_ar1_diagnostics.py
test_build_conditional_results.py
test_conditional_diagnostics.py
test_conditional_features.py
test_conditional_quantile.py
test_conditional_sources.py
test_conditional_study.py
test_core.py
test_reproduce_conditional_diagnostics.py
test_run_ar1_replay.py
test_run_conditional_study.py
test_runner.py
test_verify_ar1_output.py
verify_ar1_output.py
```

Implementation is handed back at the synthetic-reviewable stage. Real
execution, its measured receipt, independent numerical readback of the new
8/4 tables, interpretation, and publication belong to the root after the new
freeze is created. No new financial finding is asserted here.
