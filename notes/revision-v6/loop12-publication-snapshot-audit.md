# Loop 12 publication-snapshot audit

Audit time: 2026-10-23T21:32:10.311608+00:00 (initial immutable-snapshot pass), with follow-up read-only checks completed in this audit session.

Verdict: **No blocker found for uploading the exact 34-file plan from the commit below.** This is a local publication-snapshot gate. It is not a claim of remote publication, journal submission, independent financial replication, or fresh visual review.

## Scope and method

Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Plan: `.scratch/revision-v6/publication-loop12-plan.json`.
Exact source: `d1888c0a89fafbe3f36e194ff5a467ef9a3f6902`.
Comparison base: `984e2320dc53a5c74d563feb1cbbb8d338d7830c`.
Observed HEAD at the byte audit: the exact source commit.
Staged files: `.scratch/revision-v6/publication-loop12-stage/`.

The audit used immutable Git blobs, an exact destination-set comparison, recomputed byte lengths and SHA-256 hashes, structural document comparison, archive member inspection, and practical public-content/credential-format checks. These checks follow the repository's existing snapshot-audit pattern. No test, model, financial analysis, compilation, rasterization, browser action, account action, cross-model review or Claude review was run. The sole write by this auditor is this new note; no state file, source, archive, result, existing note or plan was changed, and no commit was created.

## Snapshot identity and allowed paths

All 34 declared staged files were independently read and compared byte-for-byte to `git show SOURCE:PATH`. Their lengths and SHA-256 hashes match the plan. No staged symlink or symlinked parent was found. The destination set exactly equals the base-to-source Git diff.

```text
PLAN_FILES 34
UNIQUE_FILES 34
BATCH_COUNTS [2, 27, 5]
TOTAL_BYTES 2173465
MAX_FILE_BYTES 432072
EXACT_BLOB_HASH_LENGTH_MISMATCHES []
STAGED_SYMLINKS []
DIFF_MISSING []
DIFF_EXTRA []
UNSAFE_DESTINATION_PATHS []
```

The two root destinations are `REVISION_V6_CHANGELOG.md` and `v6_submission.py`. The other destinations are 27 files under `notes/revision-v6/` and the five expected files under `submission-jof/`: README, main content JSON, main preview PDF, main TeX, and Overleaf ZIP. No `.bak`, direct `.scratch` destination, raw numerical trace container, image capture, database, account-UI capture or credential file is included.

The actual read-only Git comparison was:

```text
git diff --name-status 984e232 d1888c0
git diff --name-only 984e232 d1888c0 -- FINAL.md results protocol manuscript 'test_*.py'
```

The second command returned no paths. In addition, all 1,413 entries in `protected_v5_sha256` were freshly checked against current local files: none was missing, the changed set was exactly the 16 entries in `allowed_v6_changes`, and no unexpected change was found. Existing untracked backups remain outside the plan and were not touched.

The central byte-check logic actually executed with the bundled Python was:

```python
for f in files:
    staged = Path(f["absolute_path"]).read_bytes()
    committed = subprocess.check_output(
        ["git", "show", source_commit + ":" + f["path"]]
    )
    assert staged == committed
    assert len(staged) == f["bytes"]
    assert hashlib.sha256(staged).hexdigest() == f["sha256"]
```

## Exact document change and structure

A full recursive comparison of base and source main content JSON found exactly these two altered fields:

```text
/sections/4/blocks/1/html
/sections/4/blocks/9/html
```

Section index 4 is titled `5. Research design and transparency`. The changes add `H6` to the deliberately invalid label-timing-control description and `equal-loss ranking` to the fixed common-history Holm-family description. No other JSON value changed. This establishes that all table cells, the abstract, references, figure content and remaining text are unchanged relative to the base.

The entire Supplement content JSON, TeX and preview PDF are byte-identical across the base commit, source commit and live local files. Main and Supplement structural counts were read directly from their content JSON:

```text
MAIN_TABLE_BLOCKS 6
MAIN_FIGURE_BLOCKS 4
SUPPLEMENT_TABLE_BLOCKS 68
SUPPLEMENT_FIGURE_BLOCKS 7
SUPPLEMENT_JSON_TEX_PDF_UNCHANGED true
FIGURE_DIRECTORY_DIFF []
```

Fresh hashes of the current local main files match the source blobs, staged files, plan, document metrics and scope receipt:

```text
manuscript.tex
6c6ee36e505165dde0a3d3f4d27fbcfe5d20642929e37ac2316ed6e87b10af72

manuscript-preview.pdf
9e4f54f02fe3ce1a1ff105a05b0cdf9805dbf149fd8053d0e23ccd02b530eece
```

PDF structure was read using `pypdf.PdfReader` from the bundled runtime, without rendering or editing. The main has 18 pages and the Supplement 94 pages; both are unencrypted, and every page has an A4 media box `(0, 0, 595.2756, 841.8898)`.

The existing raster-identity receipt is internally consistent: its old PDF hash matches the base blob, its new PDF hash matches the source blob, page IDs are exactly 1 through 18, identity flags agree with the recorded PNG hashes, and the recorded changed pages are exactly [7, 8]. **This auditor did not recreate PNGs or visually inspect those pages.** The receipt binds to the correct PDFs but its earlier visual observations remain prior execution evidence.

## Retained synthetic-test receipts and input fingerprints

No tests were rerun. The retained stdout contains `collecting ... collected 950 items`, exactly 950 individual `PASSED` lines, and this literal final line:

```text
============= 950 passed, 1062 subtests passed in 85.08s (0:01:25) =============
```

The invocation receipt records return code 0, elapsed time 85.68902579206042 seconds, child peak RSS 308396032 bytes and one requested numerical thread. Those are retained execution receipts, not measurements generated by this audit.

Every one of the 1,788 path/hash entries in `final4-test-input-manifest.json` was recomputed against its retained `.scratch/revision-v6/final-suite-4/` input copy, with **zero mismatch**. This inventory describes the exact copied inputs before final4, not every file added afterward. Comparing the same inventory to the final source commit finds only two different hashes: the later-appended `REVISION_V6_CHANGELOG.md` and later-updated `notes/revision-v6/state.json`. All 1,786 other listed files, including the current source and document inputs, match the final source commit.

The stdout is present as an exact literal substring in the changelog. It includes 25 lines whose test identifiers contain `private`; these are synthetic test names and contain no actual private observation/forecast/target/loss vectors. The retained suite directory also has 12 post-copy synthetic output files; these are outside the manifest and outside the upload plan. They were not uploaded or modified by this audit.

The corrected whitespace-tolerant count used was:

```python
len(re.findall(r"^\\S.* PASSED\\s+\\[\\s*\\d+%\\]$", stdout, re.M))  # 950
```

The exact retained-input check used:

```python
for path, expected_sha256 in manifest["files"].items():
    copied = retained_suite / path
    assert copied.is_file()
    assert hashlib.sha256(copied.read_bytes()).hexdigest() == expected_sha256
```

## Whitespace exception is explicit and narrow

The exact command recorded in `loop12-whitespace-check.json` was rerun as a read-only Git check:

```text
git show --format= --check e490e7b
```

It returned **2**, as recorded. Its stdout exactly matches `loop12-whitespace-output.txt`, and all 286 parsed issue records exactly match the JSON receipt. There are 143 reports in `final4-pytest-output.txt` and 143 in `REVISION_V6_CHANGELOG.md`. Each reported line was independently verified to be a literal original stdout line or its exact changelog duplicate; no other path or line was reported.

This check is **not clean** and must not be described as clean. Retaining original stdout preserves the execution evidence. The scoped exception does not conceal a source, mathematical, manuscript, or financial-result whitespace issue.

## Archive and sensitive-content boundary

The Overleaf ZIP passes its CRC check. It has 16 members and 769,846 uncompressed bytes. Member names are unique in the inspected list, contain no absolute paths or `..` traversal, and no backup or numerical trace container. Every member byte matches its own tracked `submission-jof/` source at the exact source commit.

The member set is unchanged from the base. Only `manuscript.tex` and `README.md` changed inside the archive. Its eight PDF members are the same existing project figure PDFs; there is no added third-party source-paper PDF or account screenshot.

Recursive inspection covered all 16 planned standalone JSON files. The longest primitive numeric list had length 4 (e.g. a pixel bounding box). No long numeric observation/forecast/target/loss list, suspicious encoded-private-vector field or long base64-only payload candidate was found. The manifest stores file paths and hashes, not copied raw inputs.

Credential-format scanning covered all planned files and every ZIP member, checking common GitHub token prefixes, private-key headers, common API-key forms, literal Authorization bearer/basic patterns, and conventional secret JSON keys. It produced no credential-pattern or credential-key location. These are practical pattern/schema checks, **not a guarantee against every possible secret format, arbitrary covert encoding or steganographic payload**.

## English-language scope

A fresh CJK-character scan of manuscript and Supplement JSON/TeX, title-page TeX, cover letter and submission README found no hit. The main and Supplement remain English in this scoped sense.

The unchanged internal `submission-jof/AUTHOR-TODO.md`, which is retained inside the Overleaf ZIP, contains Chinese author-completion instructions. Local machine paths in evidence receipts can also contain Chinese directory names. Therefore the supported description is **English manuscript-facing content**, not an assertion that every support file or archive member is English. This pre-existing author-only note was unchanged and is not a blocker for the scoped language candidate.

## Limits and handoff

This audit clears the exact declared staged bytes for the authorized upload scope. It did not upload anything, inspect an authenticated remote branch, open a PR, validate remote bytes, run financial models, independently reproduce empirical findings, rerun tests, recompile TeX or re-review PDF layout. Remote publication still requires actual destination-branch/commit/file-byte readback by the publishing agent.

No local snapshot blocker was identified. The nonzero whitespace result, pre-test manifest timing and narrow language scope above must remain explicit in any completion report.
