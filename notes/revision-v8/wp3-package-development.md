# WP3 public-driver packaging development

This is delivery packaging inside WP3, not publication or a new financial analysis. Development used small constructed files only. No live/formal study directory was inspected, no DGP or model was run, and no existing research file was changed or deleted.

## Preconditions and exact scope

The actual command refuses to proceed until `study-termination.json` declares `all_workers_terminated=true`, `summary.json` exists, and an independent `independent-wp3-audit-1` receipt reports PASS, zero differences, measured-resource PASS, and current matching hashes for manifest/inventory/summary/support/termination.

It includes exactly these original top-level driver files:

- manifest.json
- inventory.json
- progress.jsonl
- summary.csv
- summary.json
- support.json
- study-termination.json

It also includes every regular public driver file below `units/`, including empty process logs and failure/interruption receipts. Unit file extensions are restricted to the driver's JSON/JSONL/log outputs. Symlinks, private/cache/scratch paths, raw Kaggle/FX names, foreign extensions and external member paths are refused. Figures, package artifacts and unrelated top-level files are excluded. Original unit files and inventory remain in place.

## Determinism and verification

- Sort member paths lexicographically.
- Stream gzip at compression level 9 with mtime=0 and no original filename header.
- Normalize tar regular-file metadata: uid/gid=0, uname/gname empty, mtime=0, mode=0644, PAX format.
- Create `wp3-driver-output-members.csv` containing path, original byte size and SHA-256 for every member.
- Re-open the finished compressed archive, stream and hash every member, check its normalized metadata, refuse duplicates/unlisted/missing members, and force reading the gzip trailer/CRC.
- Re-enumerate and hash every source after packaging. Any difference blocks public delivery; no source is repaired.
- Enforce a hard 24 MiB compressed archive cap. The CLI has no cap override. The test-only function option may lower the cap but cannot raise it.
- Build the archive, index and receipt in a fresh task `.scratch/revision-v8/wp3-package/<unique-id>/` directory; only after all checks pass copy all three by exclusive creation to the formal output directory, verify copied hashes/archive contents again, recheck original sources, and publish the PASS receipt last.
- All scratch/original files survive failures. The tool never splits, overwrites or deletes an archive, and never changes git ignore rules or publishes anything.

The receipt records actual member/source/compressed counts, hashes, audit bindings, tool hash and runtime versions. Its integrity status describes packaging, not successful scientific results: failed or incomplete driver output is retained intact.

## Test evidence

Initial command, actual subprocess exit 1:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_package.py -q
12 failed, 1 passed in 0.09s
```

The implementation stub existed; the 12 initial failures were explicit NotImplementedError failures. The one initial passing test verified a stdlib-only import. Full output/exit: `wp3-package-unit-red-output.txt`, `wp3-package-unit-red-receipt.json`.

Final command, actual exit 0:

```text
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_package.py -q
...............                                                          [100%]
15 passed in 0.12s
WARN `--no-project` was provided, but no project was found
```

Final full output, UTC, exit and output hash: `wp3-package-unit-final-output.txt`, `wp3-package-unit-final-receipt.json`.

Tests include deterministic bytes despite changed source timestamps/permissions; empty-log preservation; exact inclusion/exclusion; symlink/private/raw-source rejection; stale/non-PASS audit rejection; gzip/tar metadata and complete member readback; duplicate/wrong-hash refusal; oversize no-public-output behavior; original mutation detection; exclusive publication-file preservation; and no numeric/study imports.

`python3 -B notes/revision-v8/package_wp3.py --help` was executed successfully without result reads.

## Root's later actual packaging command

From the repository root, only after study termination, summary and independent audit PASS:

```text
python3 -B notes/revision-v8/package_wp3.py --audit notes/revision-v8/wp3-independent-audit.json
```

The formal deliverables are:

- results/revision-v8/wp3/wp3-driver-output.tar.gz
- results/revision-v8/wp3/wp3-driver-output-members.csv
- results/revision-v8/wp3/wp3-package-receipt.json

If the command fails, retain the actual failure and scratch output; do not change a limit, delete a source, split automatically, or silently retry with changed scope. Root retains responsibility for the single actual invocation and any exact git-ignore publication policy.
