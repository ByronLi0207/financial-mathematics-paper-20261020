# Loop 28 publication-snapshot audit

**Verdict: PASS for the exact immutable byte, path, content/privacy and protected-file gate.** Three note-only EOF blank-line findings are an explicitly accepted nonblocking formatting exception; the whitespace check is **not clean**.

Audit observation: 2026-10-23T22:20:45.575001+00:00.
Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Private plan: `.scratch/revision-v6/publication-loop28-plan.json`.
Plan SHA-256: `dd2b1c5536089d4356483b28bf493e16cbf4b5a6df969edceddbc0fd6a00a45b`.
Staging root: `.scratch/revision-v6/publication-loop28-stage/`.
Immutable source: `ed4bfc26850af5564b8fe8047693196e15975d99`.
Immutable source tree: `3e213cc3f7d04a7564c60c8cdd6f796ebf9181e6`.
Comparison source base: `f193fbff35e2474f4266d8c12a777b242287f33c`.
The plan also labels remote base `0e87792d8bf2dc452941e55ad2b2ce50de60579a`; this local audit does not independently verify current remote state.

## Exact inventory and source bytes

The source tree hash matches the plan, and observed HEAD at the audit was the exact immutable source. Every declared staged file was independently read, its byte length and SHA-256 recomputed, and every byte compared to `git show SOURCE:PATH`. No staged file or ancestor was a symlink. Each absolute staging path resolves to exactly the declared destination under the expected staging root.

The declared path set, actual staged-file inventory and exact base-to-source Git diff are identical. Batch directory labels agree with destination parents. There is one root ledger and 17 files under `notes/revision-v6/`, including the committed state receipt. There are 10 Markdown and 8 JSON files, no binaries or archives.

```text
DECLARED_FILES 18
UNIQUE_DESTINATIONS 18
TOTAL_STAGED_BYTES 783294
BATCH_COUNTS [1, 17]
GIT_DELTA_STATUSES {M: 2, A: 16}
BLOB_HASH_LENGTH_MISMATCHES []
SYMLINK_PATHS []
BAD_STAGING_PATHS []
BATCH_DIRECTORY_ISSUES []
DIFF_MISSING []
DIFF_EXTRA []
STAGE_EXTRA []
STAGE_MISSING []
DELETIONS_OR_NON_ADD_MODIFY []
UNSAFE_DESTINATIONS []
```

The two modified files are `REVISION_V6_CHANGELOG.md` and `notes/revision-v6/state.json`; the other16 files are added audit/selection/metadata notes. **There are no deletions, renames, code changes, manuscript changes, result changes or protocol changes in this publication delta.**

Actual read-only scope commands included:

```text
git diff --name-status f193fbf ed4bfc26850af5564b8fe8047693196e15975d99
git diff --name-only f193fbf ed4bfc26850af5564b8fe8047693196e15975d99 -- submission-jof results protocol manuscript '*.py' FINAL.md
```

The second command returned no path. The central actual byte check was equivalent to:

```python
for item in planned_files:
    staged = Path(item["absolute_path"]).read_bytes()
    committed = subprocess.check_output(
        ["git", "show", source_commit + ":" + item["path"]]
    )
    assert staged == committed
    assert len(staged) == item["bytes"]
    assert hashlib.sha256(staged).hexdigest() == item["sha256"]
```

No scientific process or test was run by these checks.

## Current manuscript and old-file protection

The main files are byte-identical across the comparison base, immutable source and live local files. Fresh hashes match the requested current candidate:

| Current file | Fresh SHA-256 |
|---|---|
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` |
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` |

The PDF was fingerprinted only, not rendered or visually reviewed in this gate.

The immutable committed state receipt supplies1,413 historical `protected_v5_sha256` entries and16 allowed v6 changes. Every protected current local file was freshly hashed without interpreting raw observations. None was missing. Exactly the16 allowed paths differ from their historical v5 fingerprints, with no additional changed file and no allowed-set discrepancy.

```text
PROTECTED_COUNT 1413
MISSING []
CHANGED_COUNT 16
ALLOWED_COUNT 16
UNEXPECTED_CHANGED []
ALLOWED_SET_DIFFERENCE []
```

Existing untracked backups and private scratch material were not copied, edited or removed. The audit's original-file hash check is distinct from reprocessing or interpreting financial data.

## Public-content and privacy boundary

All18 staged files decode as UTF-8 text. The destination allowlist permits only the ledger and `notes/revision-v6/` Markdown/JSON. No `.bak`, direct `.scratch` destination, raw financial data container, private per-origin vector file, credential file, browser/account capture, image, ZIP or PDF is present. In particular, this delta contains neither the manuscript PDF nor a third-party source-paper PDF; manuscript hashes and source links in text are metadata, not PDF payloads.

Recursive inspection covered all8 planned JSON files. The longest primitive numeric list has5 elements (e.g. seeded selection indices); there is no long primitive observation/forecast/target/loss list. Long lists of claim/metadata objects, paths and hash dictionaries are structurally different from such a numeric vector. No conventional encoded-private-vector field or long base64-only payload candidate was found.

Credential-format scanning covered every planned file, checking common GitHub-token/API-key forms, private-key headers and literal Authorization bearer/basic patterns. The JSON schema scan also checked conventional password/access/refresh token, API/client-secret, private-key, cookie and session-token keys. It found no credential value/key location.

```text
UTF8_FAILURES []
PLANNED_JSON_FILES 8
CREDENTIAL_PATTERN_LOCATIONS []
CREDENTIAL_JSON_KEY_LOCATIONS []
MAX_PRIMITIVE_NUMERIC_LIST 5
PRIMITIVE_NUMERIC_LISTS_OVER20 []
ENCODED_PRIVATE_VECTOR_CANDIDATES []
BINARY_PDF_IMAGE_TRACE_DESTINATIONS []
```

The notes contain public aggregate/scalar result traces, fingerprints, selected bibliographic metadata, recorded public repository readback metadata and limitations. References to private traces or synthetic test identifiers containing “private” do not embed the corresponding private observations. No account credentials or account-UI transcript is included.

These practical allowlist, UTF-8, schema and credential-format checks are evidence of the inspected content; they do not guarantee detection of every possible secret syntax, arbitrary covert encoding or steganographic construction.

## Whitespace: new note-only exception and unchanged stdout receipts

The actual current-delta command was:

```text
git diff --check f193fbff35e2474f4266d8c12a777b242287f33c ed4bfc26850af5564b8fe8047693196e15975d99
```

It returned **2**, with exactly three lines:

```text
notes/revision-v6/verification-loop-021-limitations-numbers-selection.json:189: new blank line at EOF.
notes/revision-v6/verification-loop-025-accuracy-numbers-selection.json:366: new blank line at EOF.
notes/revision-v6/verification-loop-025-accuracy-numbers.md:241: new blank line at EOF.
```

These are three **new note-formatting findings**, not the historical raw-stdout exceptions. They were surfaced to the publishing root before upload. The root explicitly directed that they be recorded as a **nonblocking formatting exception**, retaining the already committed immutable source/stage and making no source edits. No code, manuscript, formula or financial result is affected. This audit follows that disposition and does not call the delta whitespace check clean.

The prior loop12 and loop20 whitespace receipts remain byte-identical from base to source. Both record return code2 and286 issues concerning retained original pytest stdout and its exact ledger duplicate. The `final4-pytest-output.txt`, `final5-pytest-output.txt`, and both saved whitespace-output files are also byte-identical across base/source. These historical nonzero checks remain explicit; they have not been rewritten, normalized or relabeled as clean.

No log, note under audit, ledger or state file was changed to erase any whitespace finding.

## Handoff and action receipt

This gate clears **only the exact18 staged files /783,294 bytes** identified by the immutable plan above. Its findings permit the authorized upload under the root's explicitly accepted note-formatting exception. This new audit note is outside that immutable18-file plan unless the publishing root separately stages it in a later authorized publication.

No upload, authenticated browser action, remote file readback or branch update was performed by this auditor. A previously recorded remote receipt is itself a committed note in this delta; carrying its bytes does not independently prove current remote contents. The publishing agent must still verify the actual destination branch/commit/file bytes after native upload.

The only write is this new `notes/revision-v6/loop28-publication-snapshot-audit.md`. No state, ledger, source, manuscript, result, protocol or existing log was edited. No financial analysis, model, test suite, proof, simulation, UI action, cleanup, deletion, commit or nested agent was run. No Claude/Cloud or cross-model review was invoked.

**Content/privacy/scope blocker: none found. Whitespace: return2, three explicitly accepted note-only EOF findings; prior stdout exceptions retained.**
