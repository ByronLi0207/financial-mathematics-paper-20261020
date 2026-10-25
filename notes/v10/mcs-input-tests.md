# E3 saved-loss registry — artificial RED→GREEN

Only the three assigned new files were created: `v10_loss_inputs.py`, `test_v10_loss_inputs.py`, and this note. E2 numerical code is unchanged. No commit, network request, real financial NPZ read, actual missing-loss derivation, real combination recovery, MCS or cost computation occurred in this task. Source inspection was limited to the committed E3 design, existing inventory metadata, and inherited helper source code. All NPZ/combination JSON exercised by tests was created beneath a temporary artificial root.

## Contract and private-data boundary

`build_registry(inventory, cftc_rows, design, root)` returns `groups` and `counts`. Comparison identities are `period`, `normalized_source`, `horizon`, `window`. Groups carry `group_label`, `status` (`READY`/`FAILED_INPUT`), `methods`, `planned_methods`, `unavailable_methods`, `errors`, `alias_discrepancies`, and `claimed_complete_method_count`.

Each complete method carries `method_id`, the frozen `method_class`, `aliases`, full `origins`, `capacity`, `target`, optional `floor`, complete `loss`, and JSON provenance. Old source-qualified paths/labels remain provenance only; the loader opens only the declared `minimum_core_private_copy_manifest` destination beneath the NEW root's `.scratch`. Size/SHA are checked before NPZ materialization, and the same files are rechecked after use. Escaping paths and missing/changed keys or fingerprints are errors, never permission to read the old directory. CFTC paths must also remain inside the NEW root and match their declared `trace_bytes` and `trace_sha256`.

Declared `origin_count`, `first_origin`, `last_origin` are required independently of NPZ contents. The full integer axis must equal the declared range, its length must match the frozen source/period grid, and period/H/W must belong to that grid. Complete methods in a comparison must have exactly identical target and origin vectors. There is no intersection, shortened vector, unregistered period, or dropped claimed-complete method. Such an error fails the whole group. Its `planned_methods` still lists every originally claimed-complete procedure for failed-comparison denominator bounds. Known prior NA/FAILED slots remain separately visible and their partial traces are never opened.

Stored losses are used unchanged. Only an explicitly absent stored loss key is derived by the unchanged `v6_inference.pinball_losses(tau=.95)` from complete saved target/capacity. A declared-but-missing loss key is a failed input, not a derivation fallback. Missing QR4/Levy floors stay `None`; E3 never executes `floor_recovery` metadata.

## Aliases and published combinations

Only the protocol's named F aliases, and separately its named I aliases, may become canonical `F`/`I`. Equality is exact on the complete origins, capacity, target, loss, and provided floor. A difference keeps every qualified procedure and records an alias discrepancy; no favourable version is chosen. Query-nearest `one_state_F/S/K` and all other distinct conditional procedures retain their frozen class even if their reports equal F or I. Literal method order after semantic handling is lexicographic.

The published combination JSON is checked by its design SHA and its entire declared inventory (including known NA rows) is reconciled by identity/status/original-context. Recovery uses unchanged `v6_combinations.combine_reports`; original sources bind to `original::frozen_F`, `original::QR` and original plain KNN. Panel mean binds to `panel_legacy::frozen_F` and `panel_legacy::QR33`, with no replacement by QR4 or QR33_plus. Only previously COMPLETE combinations receive vectors. Their recovered pinball mean must match published `scores.mean_loss` within absolute `1e-12` and relative `2e-14`; a failure marks the whole comparison FAILED_INPUT. Existing NA median combinations remain unavailable.

The production metadata contract expects 828 core alias rows/407 copied core trace files, 204 CFTC rows, 64 published complete combinations plus 48 published combination NA slots and 12 inherited NA/FAILED methods, across 98 requested comparisons. These are frozen inventory expectations, not results of real materialization in this task. The registry checks supplied expected counts and fails closed instead of accepting a successful subset.

## RED→GREEN evidence

- Wrote synthetic tests before the implementation. The initial run reported `18 failed, 1 passed` (including origin-axis subtest failure instances), with the intended `MCS input registry module is missing` assertion.
- First implementation passed the initial artificial set: `15 passed, 4 subtests passed`.
- A new regression deliberately removed a published NA row while keeping a valid published mean and bound source hash. It first failed because the group remained READY. Added full published-inventory reconciliation; this prevents metadata omission from silently changing the known unavailable inventory.
- A frozen H/W-grid regression first failed because an otherwise valid vector with undeclared H/W remained READY. Added explicit period/H/W membership checks before materialization.
- Final focused run: **19 passed, 6 subtests passed in 0.22 s**, exit 0. Start UTC `2026-10-24T23:32:06.500197+00:00`; end UTC `2026-10-24T23:32:07.014688+00:00`.

The command used the exact offline dependency and thread settings in `notes/v10/baseline-tests.json`, appending only `test_v10_loss_inputs.py` to its pytest arguments. The only stderr was the existing uv `--no-project` notice. Per root instruction no full suite was run here; root owns the unified E3 check after implementation integration.

## Artificial behaviors checked

Tests cover NEW-copy-only access with nonexistent old paths; stored loss preservation; exact inherited missing-loss derivation; absent floors; size/SHA rejection; independently declared full origins and count; common-target rejection; separate known NA inventory; exact F/I aliases and discrepancies including provided-floor differences; query-nearest/rolling/Levy classes; distinct periods/source aliases; CFTC byte/hash/axis validation; original rather than expanded QR combination constituents; published aggregate reconciliation; complete published/NA metadata reconciliation; negative/nonfinite stored losses; frozen H/W membership; global expected-count mismatch with no successful-subset acceptance.

## Delivered hashes

- `v10_loss_inputs.py`: `734ad662edb0d8b4e5c260caac562fa3a10c7afad1f82b01ab0f1ed1aa4a1d98`.
- `test_v10_loss_inputs.py`: `0c29bf1ba58d6f798686ed348b0f0794daa03520ac87f1a39bf5b8bbda790bcb`.

Real input materialization remains for the root-owned call after these code bytes are committed and sealed. Returned arrays are private inputs; this helper never writes them or publishes their contents.
