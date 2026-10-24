# Loop 36 publication-snapshot audit

**Verdict: PASS for the exact immutable byte, inventory, path, privacy and protected-file gate. No publication blocker was found in this scope.** The new delta's whitespace check returns 0; inherited nonzero stdout receipts and the prior three accepted note-only EOF blank-line findings remain explicit and unchanged. This is not a claim that all historical whitespace checks are clean.

Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
Private plan: `.scratch/revision-v6/publication-loop36-plan.json`.
Plan SHA-256: `aa83b4ab97e423559c64e555bcb2bb1b28de2ae6a285ec7848455c74461f6e8a`.
Stage directory: `.scratch/revision-v6/publication-loop36-stage/`.
Immutable candidate: `4c0ea516b6c50199c4ce41a4affa22b62adc426e`.
Candidate tree: `d6c87b7e0129f83d20fc19449da8bc7d6bf0b5ff`.
Comparison source base: `ed4bfc26850af5564b8fe8047693196e15975d99`.
Plan's remote base: `b208a1e5da8f4ac047f3f293d72fa9140a0857f4`.

The first complete stage readback was at `2026-10-23T22:39:46.361367+00:00`; the protected-file check was at `2026-10-23T22:40:40.955163+00:00`. Work elsewhere in the shared repository subsequently advanced live HEAD to `b6a20cdabeec5af76b5cf7e9ba1066cd2c4c7172`. All candidate comparisons in this audit use the explicit immutable candidate above, rather than assuming live HEAD or live ledger/state bytes are the upload candidate. Later loop37+ work, backups, private scratch files and this new audit note are outside the 20-file plan.

## Exact candidate and staged-byte inventory

All declared sizes and SHA-256 values were independently recalculated from the actual staged files. Every staged byte was compared to `git show 4c0ea516b6c50199c4ce41a4affa22b62adc426e:PATH`; all matched. The candidate tree hash equals the plan. The declared paths, actual stage walk and base-to-candidate Git diff are exactly the same set.

The delta contains one root ledger and 19 files under `notes/revision-v6/`, including the immutable state receipt. It contains 11 Markdown and 9 JSON files, all UTF-8 text. There are three modifications (ledger, internal response, state) and 17 additions, with no deletions, renames or other statuses.

```text
DECLARED_FILES 20
UNIQUE_DESTINATIONS 20
TOTAL_STAGED_BYTES 835726
BATCH_COUNTS [1, 19]
GIT_DELTA_STATUSES {M: 3, A: 17}
PLANNED_HASH_OR_LENGTH_MISMATCHES []
STAGE_VS_GIT_BLOB_MISMATCHES []
STAGE_EXTRA []
STAGE_MISSING []
DIFF_EXTRA []
DIFF_MISSING []
SYMLINK_PATHS_OR_ANCESTORS []
BAD_DESTINATIONS_OR_BATCH_PARENTS []
GIT_MODE_ISSUES []
```

Every file and ancestor was checked for a symlink, including stage and scratch ancestry. Each staged object is a regular file; every source Git object has mode `100644` and type `blob`. Absolute staging paths equal the declared path under the expected stage root. Destination checks accept only `REVISION_V6_CHANGELOG.md` and immediate `notes/revision-v6/*.md` / `*.json` files, reject absolute/traversal/backup destinations, and require each batch directory to equal the destination parent.

| Exact staged destination | Bytes | Fresh staged SHA-256 |
| --- | ---: | --- |
| `REVISION_V6_CHANGELOG.md` | 455921 | `80125c60a3a3a4e952cc00cebbba5cce7d29fa75684cf39473433f79df0a96d8` |
| `notes/revision-v6/loop28-publication-snapshot-audit.md` | 9440 | `4f29ee5586825cfd6d72b0ae7cc4310b683b9b8a313c0a06a132ce50a2391d93` |
| `notes/revision-v6/loop28-remote-publication-readback.json` | 7422 | `734a654bf1ef9d99d41a1cd4bf8bd718c4cbaf5ff2e5b58879c0a7af6c3ac659` |
| `notes/revision-v6/loop36-response-snapshot-scope.json` | 1062 | `1d955915d73616491ce15abf6b948032d00806d1058d0968410126472803b04b` |
| `notes/revision-v6/response-to-internal-review.md` | 8141 | `86d6f8c3e37036bcf5c92e4f5cafc1a1af0c7a38e2e9683603555b344b8cb5b2` |
| `notes/revision-v6/self-check-023.json` | 1065 | `d96e61ceb1bf3e879b2e525ac01277a16f2eb488644539549d9c09c36a42ce9c` |
| `notes/revision-v6/state.json` | 220733 | `28323c7c6f5b7b3d1925fe9811390b1e65aa30eefaea6ae9ea0fb28556b4c094` |
| `notes/revision-v6/verification-loop-029-conclusion-numbers-selection.json` | 19745 | `dce4f7e8234f6501a700e1c6ffed809dc8be1f5261aa981f200e3198c4b8408d` |
| `notes/revision-v6/verification-loop-029-conclusion-numbers.md` | 10939 | `f7dbe9e1e656f00ea812f48a00d754173127d3043d94835eb7c0c5f70e09d755` |
| `notes/revision-v6/verification-loop-030-references-selection.json` | 2066 | `47f8dcceece0a7867ea8f77937a496aac458d7d240f08b35f7c3ed8d1002825f` |
| `notes/revision-v6/verification-loop-030-references.md` | 3083 | `82e06ddc16bafcc01f363242bc00aab91afb517605a7872017e5346df7a04675` |
| `notes/revision-v6/verification-loop-031-referee-B-limitations.md` | 14128 | `f2ad874dfa3b0ec15918edfff17d25e280f2559796646727adc475cff452597c` |
| `notes/revision-v6/verification-loop-032-conclusion-claims.md` | 3687 | `9d3492c095991384edd54fdcae42ea46b442098330043b0d614afb2455b27109` |
| `notes/revision-v6/verification-loop-033-design-numbers-selection.json` | 41330 | `75a2567289ed71cd5aa55bb552985fdcb5dd5092d97398c207f9b9f29821e743` |
| `notes/revision-v6/verification-loop-033-design-numbers.md` | 12864 | `100e8d83641f53207f09ae34c1cd6b81fa041ca59e23ccc989dfa2f6848ebd51` |
| `notes/revision-v6/verification-loop-034-gneiting-registered-metadata.json` | 1124 | `d0cd2687f62d7611d3258028e7711eddf93461a3421d51fe8c6044f8e818412a` |
| `notes/revision-v6/verification-loop-034-references-selection.json` | 2179 | `474271f2dafa3557e70dce895d567d7b2b90453fb9205e933c46efb2498f287c` |
| `notes/revision-v6/verification-loop-034-references.md` | 3632 | `0ff9944a951584a2bc2eaeb1d5548b7878824f11bc5fbcd667c9e72cdb735985` |
| `notes/revision-v6/verification-loop-035-referee-A-adaptations.md` | 13565 | `65475ade3b6184e8192d49a35903db2df0b27c4c7cce9705ed90ac5743f9317d` |
| `notes/revision-v6/verification-loop-036-internal-status-claims.md` | 3600 | `76266d370404fa1609044c2b3705a3038fd80c55491a132f82acb91696086ed6` |

Actual static scope commands included:

```text
git diff --name-status ed4bfc26850af5564b8fe8047693196e15975d99 4c0ea516b6c50199c4ce41a4affa22b62adc426e
git diff --name-only ed4bfc26850af5564b8fe8047693196e15975d99 4c0ea516b6c50199c4ce41a4affa22b62adc426e -- submission-jof results protocol manuscript '*.py' FINAL.md
git merge-base --is-ancestor ed4bfc26850af5564b8fe8047693196e15975d99 4c0ea516b6c50199c4ce41a4affa22b62adc426e
```

The scientific/code/manuscript/result/protocol path query returned no path. The ancestry query returned 0. The central actual byte check was:

```python
staged = (stage / item["path"]).read_bytes()
committed = subprocess.check_output(
    ["git", "show", source_commit + ":" + item["path"]], cwd=repo
)
staged == committed
len(staged) == item["bytes"]
hashlib.sha256(staged).hexdigest() == item["sha256"]
```

The locally available remote-base commit object `b208a1e5da8f4ac047f3f293d72fa9140a0857f4` and source-base `ed4bfc2…` both resolve to tree `3e213cc3f7d04a7564c60c8cdd6f796ebf9181e6`. This verifies the local object/tree relationship, not the current state of a live remote branch. No network or account action was performed.

## E08 historical-snapshot qualifier

The actual `git diff BASE SOURCE -- notes/revision-v6/response-to-internal-review.md` contains one changed E08 line. Independently reading both blobs confirms that replacing the single exact old sentence from `loop36-response-snapshot-scope.json` with its exact new sentence produces the entire new response byte content. Each sentence occurs once. The ordered numeric token sequence of the complete response, extracted with `\d+(?:\.\d+)?`, is identical.

The old wording begins “Final main7093prosewords/6tables/4figures passes project budget.” The replacement identifies those values as “The original integration snapshot” and routes current language-only counts to `document-metrics.json`. The limitations about an unverified numerical journal cap and the absence of a submission-ready guarantee remain. No scientific value, result claim, manuscript field or source code is changed.

- Base response SHA-256: `8c005442d8338db2f3a186eb38d58acc3583ca67b0851f6c77b9b687861b66d4`.
- Candidate response SHA-256: `86d6f8c3e37036bcf5c92e4f5cafc1a1af0c7a38e2e9683603555b344b8cb5b2`.
- Scope receipt SHA-256: `1d955915d73616491ce15abf6b948032d00806d1058d0968410126472803b04b`.

The historical source proof was read directly from commit `b895c67fcb719fcb5eef93b180d4e7757e2a3804` (resolved from `b895`), not inferred from a previous review verdict. Its `notes/revision-v6/document-metrics.json` has SHA-256 `2a71ec2902a99c7b561f31d4af7fc882815ca84e89fa3dd2daf240c695b99fc7` and records 7,093 main prose words excluding abstract/references/tables/captions, 18 pages, 211 abstract words, 6 tables and 4 figures. Its recorded TeX hash `875516d3f7840e80f3b07de6783c68bc9efff248afff48ec280387d17c2bfab1` and PDF hash `0e538ae5dc16592ff30362151fb37005294187810ec240dbbc0305554cb52e9d` equal fresh hashes of those historical commit blobs.

The current saved metrics receipt has SHA-256 `c7e48a5c4ef9586b4e917dc66ca01ace56b501a2f26aacd1db0283658a81e738`, is byte-identical across base, candidate and local file, and records 7,103 main prose words with the same saved page/abstract/table/figure counts. Its saved TeX and PDF hashes equal fresh candidate blob hashes below. These are receipt/provenance checks only; no word count, compilation, page rendering or new analysis was run. The existing receipt limits the budget to the project's own budget and does not claim a verified journal numerical cap.

## Main-document and historical protected-file checks

The three main-document files are identical across comparison base, immutable candidate and freshly hashed local files:

| Current main artifact | Fresh SHA-256 | Base / candidate / local equal |
| --- | --- | --- |
| `submission-jof/manuscript-preview.pdf` | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` | yes |
| `submission-jof/manuscript.tex` | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` | yes |
| `submission-jof/manuscript-content.json` | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` | yes |

The PDF was fingerprinted only. No layout, scientific validity, compilation or submission readiness is inferred from those hashes.

The protected manifest and allowlist were taken from the **immutable candidate's committed state blob**, not the concurrently edited live state. All 1,413 historical `protected_v5_sha256` entries were freshly hashed locally using streaming SHA-256, without interpreting observations. None was missing. Exactly the 16 declared allowed paths differ from their historical fingerprints; no other protected path differs, and no declared allowed path is absent from that changed set.

```text
PROTECTED_COUNT 1413
ALLOWED_COUNT 16
CHANGED_COUNT 16
MISSING []
UNEXPECTED_CHANGED []
ALLOWED_NOT_CHANGED []
```

The exact historical allowlist/change set is:

- `README.md`
- `submission-jof/AUTHOR-TODO.md`
- `submission-jof/README.md`
- `submission-jof/cover-letter.md`
- `submission-jof/main.tex`
- `submission-jof/manuscript-content.json`
- `submission-jof/manuscript-preview.pdf`
- `submission-jof/manuscript.tex`
- `submission-jof/overleaf-package.zip`
- `submission-jof/references.bib`
- `submission-jof/supplement-content.json`
- `submission-jof/supplement-preview.pdf`
- `submission-jof/supplement.tex`
- `submission-jof/title-page-preview.pdf`
- `submission-jof/title-page.tex`
- `v4_numeric.py`

These 16 are historical v6 changes relative to the original protected baseline; they are not new changes introduced by this notes-only publication delta. No source change, deletion or cleanup was performed by this gate.

## Public-content and privacy boundary

All 20 staged files were decoded as UTF-8; all 9 JSON documents were recursively inspected for schema-level credential/vector payloads. Markdown headings and JSON root fields are consistent with audit/selection/metadata receipts, bibliographic metadata, internal-response text, state fingerprints and the ledger. The prior publication readback JSON contains public repository commit/tree/file/PR metadata and hashes; it is not an account screenshot or a cookie/session capture.

No destination is a raw financial data container, private per-origin vector file, source-paper PDF, manuscript PDF, image, archive, credential file, browser/account capture, `.bak` backup, or `.scratch` publication destination. The staged state contains path-to-hash provenance, not those protected files' contents. Mentions of private vectors and synthetic test identifiers containing “private” do not themselves embed those private vectors.

The content scan checked common GitHub-token/API-key forms, private-key headers, literal Authorization bearer/basic values, and conventional password/access/refresh-token/API/client-secret/private-key/cookie/session-token JSON keys. It also checked conventional encoded/raw-vector JSON keys, long primitive numeric lists and long base64-only strings/lines. It returned:

```text
UTF8_FAILURES []
JSON_DOCUMENTS 9
CREDENTIAL_PATTERN_LOCATIONS []
CREDENTIAL_JSON_KEY_LOCATIONS []
RAW_OR_ENCODED_VECTOR_KEY_LOCATIONS []
MAX_PRIMITIVE_NUMERIC_LIST 5
PRIMITIVE_NUMERIC_LISTS_OVER20 []
LONG_BASE64_ONLY_CANDIDATES []
BINARY_OR_ACCOUNT_CAPTURE_DESTINATIONS []
```

The longest primitive numeric lists are five seeded-selection indices in loop029/033. Larger object lists, selected-claim frames and dictionaries of filenames/hashes are not observation/forecast/target/loss vectors. No raw/private source content was interpreted or republished. This bounded allowlist, encoding, schema and conventional-secret scan supports the publication gate; it does not guarantee detection of every possible secret syntax or covert encoding.

## Whitespace findings retained explicitly

The exact current-delta command:

```text
git diff --check ed4bfc26850af5564b8fe8047693196e15975d99 4c0ea516b6c50199c4ce41a4affa22b62adc426e
```

returned **0 with no output**. This says only that Git reports no new whitespace issue in this exact delta. It does not overwrite historical check results.

The prior delta check was separately rerun:

```text
git diff --check f193fbff35e2474f4266d8c12a777b242287f33c ed4bfc26850af5564b8fe8047693196e15975d99
```

It still returns **2** and reports exactly:

```text
notes/revision-v6/verification-loop-021-limitations-numbers-selection.json:189: new blank line at EOF.
notes/revision-v6/verification-loop-025-accuracy-numbers-selection.json:366: new blank line at EOF.
notes/revision-v6/verification-loop-025-accuracy-numbers.md:241: new blank line at EOF.
```

Those three files remain byte-identical from the present base to candidate and still end with their EOF blank line. Their previously accepted note-only nonblocking formatting disposition remains intact. No immutable source or staged bytes were normalized.

The existing loop12 and loop20 whitespace receipts each retain return code **2** and **286** reported issues concerning captured pytest stdout and its ledger duplicate. Both receipts, both saved whitespace-output texts and both final4/final5 stdout files are byte-identical across the present base and candidate. Their exact retained hashes, together with the three EOF-exception files, were freshly checked:

| Retained exception/evidence file | SHA-256 | Base / candidate equal |
| --- | --- | --- |
| `notes/revision-v6/loop12-whitespace-check.json` | `cc9f57cd9551b621aa827f3eb95a1bf7b9f729b33022b4628b117f46c6631e96` | yes |
| `notes/revision-v6/loop20-whitespace-check.json` | `2a02482d2eceb45e85ec1a4aae4b83e7e73104a00ce2e9b1503153b42e214f0b` | yes |
| `notes/revision-v6/loop12-whitespace-output.txt` | `44e3b88d28ca4702efbe6b3521339f225590c89b328b8031cf4648b8787dcb44` | yes |
| `notes/revision-v6/loop20-whitespace-output.txt` | `8832826b69bde164632e183f3c018be7f29430a7af9cf4d365e875a312ebba4e` | yes |
| `notes/revision-v6/final4-pytest-output.txt` | `07d6f3320d6af575bbaac096c6765542390c40c29b9f174df0ef06e296313572` | yes |
| `notes/revision-v6/final5-pytest-output.txt` | `4d4917400f179cfecd42a0dead5b59451cfbb1edc70007ada8acbe634a248ad0` | yes |
| `notes/revision-v6/verification-loop-021-limitations-numbers-selection.json` | `f84db855d51e8d064cb9dbcbd46c70abe52b5614869f0dcea6aecc304d4b6405` | yes |
| `notes/revision-v6/verification-loop-025-accuracy-numbers-selection.json` | `4ff224d778ab69c143b502277c75849660ae5f194e5ebea493dae80ba09ab1c3` | yes |
| `notes/revision-v6/verification-loop-025-accuracy-numbers.md` | `bd7130a35f3685b66cb00d5ad496261bcdc28562f36158a77039a3eb43d4212a` | yes |

No stdout, ledger, existing note or state was rewritten to conceal an exception; no test suite was rerun.

## Handoff and limits

This gate clears only the exact **20 staged files / 835,726 bytes** identified by the immutable plan. Later loop37+ notes and live ledger/state progress do not alter this fixed candidate and were not silently added to the stage. This new audit note is outside that 20-file plan unless a later authorized publication separately includes it.

The only write by this task is `notes/revision-v6/loop36-publication-snapshot-audit.md`. No source, manuscript, saved result, protocol, state, ledger or already committed note was edited; no cleanup, deletion, staging, commit, model, statistical analysis, test suite, proof, simulation, UI, upload, network action or nested agent was invoked. No Claude/Cloud or cross-model review was invoked.

The authorizing publication agent must still verify the actual destination branch/commit/file bytes after native upload. Local prior remote receipts and local commit objects are not a fresh authenticated remote readback.

**Publication scope/content/privacy blocker: none found. Exact new-delta whitespace: return 0. Inherited stdout return-2 receipts and prior three accepted EOF exceptions: retained, not relabeled as clean.**
