# Independent WP3 readback development

This tool imports only the Python standard library. It does not import the study driver, statistical model modules, NumPy, SciPy, or any RNG. No formal study directory or live study result was read during development. All tests use constructed scalar records and temporary fixture files; the full 6,912-slot fixture consists solely of `NOT_ATTEMPTED` records, not simulated observations.

## Scope

- Independently reconstruct all planned inventory identities and the paired repetition summaries: ratio of mean losses, paired delta Monte Carlo SE (sample SD), breach frequencies/SEs, strict wins, undefined single-completion SEs, complete/failed/unattempted counts, and conditional-on-completion status.
- Check original QR33/QR4 mandatory-menu and exact-tie selection rules from saved candidate receipts, without running a candidate.
- Check available validation/evaluation refit diagnostics for mature labels and the specified window.
- Re-evaluate the frozen six-target / fully-evaluable-outside descriptive support rule; distinguish missing cells from zero performance.
- Check protocol bytes against the pre-result commit and commit time against actual run start; check sealed source bytes and inventory hash bindings; compare recorded common-random-number states within a repetition without creating an RNG.
- Aggregate actual worker resource receipts/checkpoint samples. Missing observations are `UNVERIFIED`, never replaced with configured limits. The small recorded termination/receipt allowance is fixed at 5 seconds; this is not a scientific design or budget extension.
- Preserve every difference. Inputs are read-only; output is exclusive-create. A study `COMPLETE` process label is explicitly not treated as complete method success.

This is an independent arithmetic and provenance audit of saved scalar results, not independent simulation replication or a new financial analysis.

## Test evidence

Initial command (actual exit 1):

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_audit.py -q
15 failed in 0.06s
```

The 15 initial failures were explicit `NotImplementedError` assertions after the module stub existed. Full output: `wp3-audit-unit-red-output.txt`; actual subprocess exit recorded in `wp3-audit-unit-red-receipt.json`.

Additional selection-rule tests then observed (before implementation):

```text
FAILED test_v8_wp3_audit.py::test_complete_qr33_cannot_hide_a_failed_mandatory_candidate
FAILED test_v8_wp3_audit.py::test_selection_ties_follow_distinct_original_menus
2 failed, 17 passed in 0.09s
```

Final command (actual exit 0), using only cached temporary pytest:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_audit.py -q
.....................                                                    [100%]
21 passed in 0.30s
WARN `--no-project` was provided, but no project was found
```

Full final output: `wp3-audit-unit-final-output.txt`; command, UTC, exit and output SHA-256: `wp3-audit-unit-final-receipt.json`.

`python3 -B notes/revision-v8/audit_wp3.py --help` was executed successfully without study reads.

## Root invocation after termination and summary

```text
python3 -B notes/revision-v8/audit_wp3.py --output notes/revision-v8/wp3-independent-audit.json
```

Requires actual `study-termination.json` with `all_workers_terminated=true`, `summary.json`, and `support.json`. If a prior audit output exists, choose a new output name; the tool refuses to overwrite it. A `FAIL` or `UNVERIFIED` output remains evidence and must be interpreted rather than repaired by changing scientific results.
