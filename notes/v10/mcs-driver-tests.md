# E3 driver — artificial persistence and input-binding tests

Implemented only `run_v10_mcs.py`, `test_v10_mcs_driver.py` and this note. The E3 design remains the sole-file commit `78ea93493379ab3a93459d28e1bab84200f01539`, `protocol/v10/mcs-design.md`. No wrapper, helper, E1 or E2 numerical file was edited. No real `build_registry` call, real NPZ load, loss derivation, bootstrap, MCS, prepare/seal/formal command, commit or full-suite run was performed during this work.

Only public metadata/schema and source code were inspected. All loaded NPZs in these tests were constructed beneath pytest temporary directories. Upstream hash tests use artificial byte files and never open an original financial file.

## RED → GREEN evidence

1. Six artificial persistence/input tests were written first. Before the driver existed: exit1, **6 failed in0.27s**, all the expected assertion `MCS driver is missing`.
2. Initial implementation: exit0, **6 passed in0.18s**.
3. Root's timestamp/private-permission clarification retained GREEN: **6 passed in0.17s**.
4. Independent source review identified the need to bind CFTC splits to its committed E2 seal before materialization. A new artificial regression first failed with **1 failed,6 deselected in0.13s**, `DID NOT RAISE ValueError`, against the earlier driver.
5. After that source-binding correction: exit0, **7 passed in0.12s**.

Focused command:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMBA_NUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pytest==9.1.1 python -B -m pytest -q -p no:cacheprovider --tb=short test_v10_mcs_driver.py
```

The source-binding RED used the same command with `-k cftc_axis`. There was only uv's `--no-project was provided, but no project was found` notice; no pytest warning/error in GREEN runs.

## Artificial behavior verified

- `persist_registry(registry,public,private,root)` writes only metadata to public `input-index.json`. Real artificial vectors are stored exclusively in private NPZ. Public index text contains no vector values.
- READY methods are sorted by literal `method_id`. `column_index` connects each descriptor to the corresponding loss/capacity matrix column. Full `origins`, shared `peak`, matrices, per-array shape/dtype/SHA, NPZ bytes/SHA and exact origin endpoints are recorded and checked on reload.
- Existing floor is stored at `floor_000` for its sorted method column. A method with `floor=None` has `floor_key=None` and no invented array. Private reload returns exactly the provided floor inventory.
- A FAILED_INPUT group retains every planned method ID/class, aliases/provenance, errors and known unavailable methods, without writing a matrix. Original `planned_methods` is retained separately, while summary-facing `methods` has unique literal IDs.
- Changed private NPZ bytes, changed expected array shape, and changed per-array digest are rejected before use. Changed artificial copied-core or public-CFTC bytes are likewise rejected.
- CFTC augmentation preserves literal code including leading zeros/plus signs, uses `family=CFTC`, the frozen period and `normalized_source='cftc:'+code`, and obtains H/count/first/last from supplied split metadata without accessing any capacity/loss array.
- Before reading splits, both CFTC `splits.json` and E2 `manifest.json` must pass committed-file validation; actual splits SHA must equal E2 manifest `prepared_sha256['splits.json']`. The artificial mismatch is rejected before materialization.

## Driver execution contract (implemented; not run on financial data here)

Commands are `prepare`, `seal`, `formal`, `worker`. The parent imports stdlib and existing generic file helpers only; new numerical/data modules are imported inside their relevant command.

`prepare` checks the E3 sole-file design and frozen old loss/combination modules, then requires all new E3 numerical scripts and support scripts to match current committed HEAD before importing/calling `build_registry`. It verifies the frozen inventory/CFTC metadata, all407 NEW copied-core file fingerprints and204 public CFTC trace fingerprints. Expected file and comparison counts come from the frozen design; a wrong98-group inventory stops preparation.

The materialization marker is named `materialization_started_utc`, with `timing_semantics='entry before build_registry; lower bound for first derived-loss call'`. It is a conservative entry marker, not a fabricated timestamp of the first individual pinball calculation. The formal plan separately records exact driver-launch UTC/monotonic time. CFTC start split SHA is saved before the helper call and must remain identical after materialization/persistence; the end receipt stores that same pinned value rather than merely recording a newly observed hash.

Private registry directory is created exclusively with mode0700, NPZs exclusively and then mode0600. Persisted private files live under new `.scratch/v10/mcs-inputs/cNNN.npz`. Public metadata retains provenance/aliases, method class, column and floor key for root/E4; no floor recovery or cost/headroom statistic is performed.

`seal` requires committed code and committed input-index, checks private group files and upstream inputs, and records code/data/index/preparation/copy-manifest/CFTC-axis hashes. The manifest itself must be committed before workers/formal accept it. Upstream copied/public inputs and private group fingerprints are checked before/after the formal phase; worker reload verifies exact private file and per-array hashes, shape, dtype, complete common origin axis and column mapping.

Formal has four one-thread workers, global1800s, inherited internal540s and hard600s limits. READY groups alone reach `compute_mcs`; known FAILED_INPUT groups get direct zero-library-attempt rows. Worker/resource/timeout failures retain planned method IDs/classes; unknown interrupted library-attempt counts are `null`, not falsely asserted to be zero. The wrapper's actual success/failure rows retain its precise attempt diagnostic when available. No retry or alternate configuration exists.

All planned unit rows, including failed/unstarted groups, are written under the formal units directory. Units ZIP and per-member SHA manifest are produced with loose files retained before report-only summary work. The summary API is `v10_mcs_summary.summarize(records,input_index['groups'],design)`; outputs are public summary, full native cell rows and CSV with nested membership/p-values serialized as JSON strings. No private array is printed or placed in public report rows.

These execution paths were source-reviewed and are ready for root's unified integration/full-suite verification and commit gate. The seven focused tests do not establish that real98-group preparation or formal inference has run.

## File fingerprints

| File | bytes | SHA-256 |
|---|---:|---|
| `run_v10_mcs.py` | 23124 | `341ff4258fc817d0a09733a8fd75c8eb9714914fdf428903970c9621d58d5aa6` |
| `test_v10_mcs_driver.py` | 7508 | `fc767d9dc390cbb296b74568ea37bc7b2f107816c5212cf63baa593c8d9f5993` |
