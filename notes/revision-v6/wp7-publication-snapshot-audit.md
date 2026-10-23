# WP7 independent publication-snapshot audit

Status: scoped read-only content audit, followed only by creation of this new note at the root agent's request. No manuscript, result, archive, source code, existing note or publication plan was edited. No model was rerun, browser operated, file deleted, account changed or Claude review invoked.

Audit time: 2026-10-23T20:48:01.780019+00:00.

## Exact immutable snapshot

Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Branch under audit: `revision-v4-jof`.
Plan: `.scratch/revision-v6/publication-plan-v2.json`.
Exact source commit: `b895c67fcb719fcb5eef93b180d4e7757e2a3804`.
Remote comparison base: `a3481aa0d4ae6e393b7e60bb0dca8ddb633b15db`.
The staged copies are under `.scratch/revision-v6/publication-stage-b895c67/`. Their source paths, rather than their private staging paths, determine the remote destinations. This note audits those immutable bytes, not the live state file or later audit notes, and does not itself prove the uploaded remote branch has all of them.

The independent verifier read all 366 declared staged files, compared every byte with `git show SOURCE_COMMIT:REPO_PATH`, recomputed each SHA-256 and byte length, compared the plan set with the exact base-to-source Git diff, and checked uniqueness and staged-file symlinks. The actual invocation used the existing bundled Python and standard library; the central checks were:

```python
plan = json.loads(Path('.scratch/revision-v6/publication-plan-v2.json').read_text())
files = [f for batch in plan['batches'] for f in batch['files']]
for f in files:
    staged = Path(f['absolute_path']).read_bytes()
    committed = subprocess.check_output(['git', 'show',
        plan['local_source_commit'] + ':' + f['path']])
    assert staged == committed
    assert len(staged) == f['bytes']
    assert hashlib.sha256(staged).hexdigest() == f['sha256']
```

Literal summary output:

```text
EXACT_GIT_BLOB_AND_MANIFEST 366 mismatches []
UNIQUE_PATHS 366
DIFF_SET_MISSING [] EXTRA []
SYMLINK_STAGED []
```

Total snapshot bytes: **15,428,425**. There are 13 batches. The plan contains 40 Markdown, 133 JSON, 2 ZIP, 7 PDF, 130 text, 48 Python, 1 diff, 4 TeX and 1 BibTeX files. Root changes are README, the v6 changelog, v6 implementation/tests and the authorized v4 numeric-validator extension. Other paths are restricted to `protocol/revision-v6`, `results/revision-20261023/v6`, `notes/revision-v6` and `submission-jof`. No unrelated project path was included.

## Archive and original-file protection

The audit recomputed all 1,413 `protected_v5_sha256` entries in the goal state. Exactly the 16 paths explicitly listed in `allowed_v6_changes` differed. No other protected file was missing or modified. This is a current byte check, not an inference from a past test pass.

```text
PROTECTED_HASH_COUNT 1413
OLD_FILE_DIFF_COUNT 16
ALLOWED_SET_DIFFERENCE []
PROTECTED_OLD_UNEXPECTED_MISSING_OR_MODIFIED 0
ARCHIVE_AND_FINAL_COMMIT_DIFF []
```

The commit comparison command was:

```text
git diff --name-only a3481aa0d4ae6e393b7e60bb0dca8ddb633b15db b895c67fcb719fcb5eef93b180d4e7757e2a3804 -- FINAL.md results/revision-20261022 manuscript/revision-v3 manuscript/working-paper
```

It returned no paths. `FINAL.md`, old result archives and both older manuscript directories are unchanged. Existing untracked `.bak` files remain untouched and are absent from the publication plan.

## Public-content and diagnostic boundary

The public outputs should be described precisely as **aggregate results, fitted optimization diagnostics and fingerprints**. The 16 SAV validation/evaluation receipts include per-refit three-parameter fitted coefficients, their six optimization starts, scales, initialization quantiles and solver objectives. These are derived fitted-model diagnostics. They are not the protected raw FX observations or per-origin issued-capacity/outcome/loss vectors. They were retained unchanged; this audit did not strip fields or rewrite published results. In particular, a claim that every public JSON contains only aggregate means and hashes would be inaccurate.

Recursive inspection covered all 133 standalone JSON files and all 41 JSON members of the metadata ZIP. The longest primitive numeric list had length 4. Long arrays of table rows, refit diagnostic objects, filenames and test/contrast IDs are present, but no long numeric observation/forecast/target/loss array or encoded private-vector field was found. The encoded-content check inspected conventional base64/raw-array field names and long base64-alphabet string candidates; it did not infer privacy solely from a file extension.

```text
UNSAFE_PATH_CANDIDATES []
CREDENTIAL_PATTERN_HITS []
CREDENTIAL_JSON_KEYS []
JSON_AND_METADATA_SCAN {'json_files': 133, 'zip_json_members': 41}
MAX_PRIMITIVE_NUMERIC_LIST_JSON_AND_METADATA 4
ENCODED_PRIVATE_VECTOR_CANDIDATES []
```

No `.npz`, `.npy`, `.csv`, `.parquet`, screenshots, browser captures, private UI logs, database, credential file, `.bak`, or direct `.scratch` destination is in the publication plan. The seven standalone PDFs are this project's manuscript/title/supplement previews and its own two repeated figure files, not third-party source-paper PDFs. The only filename containing `guard` is `notes/revision-v6/replay-setup-output-guard-red.txt`, which is a synthetic filesystem output-guard test receipt, not a Claude/account guard log.

The metadata ZIP intentionally stores historical destination names beginning `.scratch/`; these are **41 JSON metadata members**, not copied private caches. They consist of the exact input inventory and 40 historical public phase manifests, containing identifiers, shapes, hashes, scalar scores and per-refit scalar diagnostics. It contains no raw or numerical trace container and no fitted coefficient or dual vector. It is 565,335 compressed bytes and 3,436,735 uncompressed bytes, SHA-256 `85cbfc25a45d9858641c4b47f78bd7d607f665ecfec8412d92dbceff925e20c9`.

The Overleaf package has 16 members: four TeX sources, references, three project Markdown files and eight project-generated vector figures. Across both ZIPs, all member names were checked for absolute paths and `..` traversal, and member contents were scanned for standard credential patterns. The metadata members were also checked for absolute user home fields.

```text
ZIP_EXTENSION_COUNT {'.json': 41, '.tex': 4, '.bib': 1, '.md': 3, '.pdf': 8}
ZIP_SAFETY_ISSUES []
```

The credential scan checked GitHub token prefixes, private-key headers, common API-key prefixes and literal Authorization bearer/basic patterns, plus conventional credential JSON keys. These pattern checks and schema inspection are practical evidence, **not a mathematical guarantee that arbitrary covert encodings or every possible secret format are absent**. No sensitive value was printed by the audit.

## GitHub upload constraints

The official [GitHub file-upload documentation](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) was actually opened during this audit. It states a browser limit of 25 MiB per file and up to 100 files per upload. The staged plan is below both limits:

```text
MAX_BATCH 80 MAX_FILE 1230328 MAX_NAME_BYTES 99
```

No planned filename or batch-count conflict with those documented limits was found. This does not certify repository-specific rulesets, push protection, line-ending transformations or successful remote publication. Each native upload still needs actual branch/commit/file-byte verification. No remote update or PR was performed by this auditor.
