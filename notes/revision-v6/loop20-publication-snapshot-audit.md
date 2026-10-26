# Loop 20 static pre-upload snapshot audit

**Gate: PASS for the exact frozen upload-stage snapshot and source commit below, with the explicitly retained whitespace exception. This is not an all-green whitespace result.** No blocker was identified in the requested static scope. This audit makes no remote-publication, new test-run, fresh compilation, fresh rendering or fresh visual-review claim.

## Snapshot identity and boundary

- Plan: `.scratch/revision-v6/publication-loop20-plan.json`.
- Plan SHA-256: `994264e132ae8dd38bbee88409ccc04e993abb44a33ae533a2012e589eb74bb7`.
- Source commit: `f193fbff35e2474f4266d8c12a777b242287f33c`; source tree: `c39a32d33adef6289c9bb353b665cabf74c48ed2`.
- Base source commit: `9666d2d428e0893699f43c13dff0d5e0a47d7a7b`.
- Recorded remote-base commit, checked only as a locally available Git object: `d0d26662b903bcec1adab8ebde29881c870152c8`.
- Both base objects have tree `4d2b8b6a5b8f0678fd54c5c54e3ae5468486859e`. This local tree equality is not a live remote check or proof of upload.
- Frozen upload directory: `.scratch/revision-v6/publication-loop20-stage/`.
- Exact change/upload set: **26 regular files**, **2,285,150 bytes**, in batches **2 / 19 / 5**, under `.`, `notes/revision-v6`, and `submission-jof`.

At 2026-10-23 22:03:32 UTC, every planned upload file was independently compared by exact relative/absolute path, file length, SHA-256, source-commit blob bytes, independently computed Git blob identity, file mode, current working-file bytes and Git-index bytes. All 26 matched; the base-to-source changed-path set equaled the planned path set, without omissions or extras. The upload-stage paths resolve to the prescribed stage directory and are regular files, not symlinks or traversal paths. “Staged” here means the frozen upload-stage directory; no Git staging or index mutation was performed.

Concurrent coordinator commits subsequently advanced HEAD to `ae67d36edc8dad9f9112b709b05d21cb665d6b5d`. At the repeated check **2026-10-23 22:05:44 UTC**, all 26 upload-stage files still matched the plan and the fixed `f193…` source commit exactly. The moving working tree/index differed from the frozen stage only in `REVISION_V6_CHANGELOG.md` and `notes/revision-v6/state.json`. This gate therefore applies to the explicitly staged `f193…` snapshot, not the moving HEAD or a new copy of those two current files. No later coordinator state is silently substituted into this plan.

## Main-document change scope

An independent recursive comparison of base/source manuscript JSON found exactly one visible changed pointer:

`/sections/6/blocks/3/html`

The exact changed clause is:

- Before: “their sample-average improvement persists under every constant nonnegative linear weighting of those components.”
- After: “their sample-average loss is lower under every constant nonnegative linear weighting of those components with at least one positive weight.”

The remainder of that paragraph is identical. The TeX diff contains the same single clause replacement. The static generator diff adds the corresponding unique-anchor replacement and fails if the old anchor is not unique; no financial estimation or result-generation code changes are present in that diff.

The only additional JSON differences are the expected provenance keys on that same block: `_source` is removed, `_generator` becomes `v6:block:manuscript:6:3`, and `_bindings` is added. All **12** new binding hashes independently match the named files in the fixed source commit. No other JSON field changes.

After removing underscore-prefixed provenance fields, all **1,153 visible numeric substrings** occur in the identical ordered sequence. All **six main tables**, abstract, references, figure metadata, title, subtitle and date are identical. This is a text/object comparison, not a new scientific analysis or numerical validation.

The entire supplement JSON, TeX and preview PDF are byte-identical to the base; both title-page files are byte-identical; and all eight tracked `submission-jof/figures/*.pdf` assets are byte-identical. The unchanged bibliography and other tracked package assets are not introduced as new content. No empirical number, table, result direction, abstract or scientific conclusion is changed by this language candidate.

## Current preview, compilation and retained visual receipts

- Main TeX SHA-256: `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`.
- Main JSON SHA-256: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`.
- Main preview PDF SHA-256: `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`; **18 pages**, independently counted by parsing the existing staged PDF, without rendering. It is unencrypted.
- The retained `loop20-native-compile.json` reports desktop compiler `kind=success` for `submission-jof/main.tex` and binds the exact current manuscript TeX hash above plus wrapper hash `f67dee42ce85e43ee99337e09a1550892006b57b52017f6044edcb85068e0407`. It expressly says `formal_pdf_exported=false`; it is not misrepresented as an exported compiler PDF.
- The retained raster-identity receipt binds the base preview hash `9e4f54f02fe3ce1a1ff105a05b0cdf9805dbf149fd8053d0e23ccd02b530eece` and the current preview hash. Those hashes independently match their actual base/source PDFs. Its 18 stored page records mark 17 identical and page 11 changed, at 110 dpi. The scope-and-validation receipt records the earlier page-11 view. This gate reads those retained records; it does not regenerate rasters or renew that visual review.
- `document-metrics.json` binds the same current TeX/preview, records main 18 pages / 6 tables / 4 figures and unchanged supplement 94 pages. Its budget statement remains a project budget, not a newly verified journal word/page rule.

## Retained final5 tests and input identity

The original `final5-pytest-invocation.json` was read, not executed. It records return code **0**, start `2026-10-23T21:59:22.272715+00:00`, elapsed **86.14735804102384 s**, and its isolated-copy command. The retained stdout has exactly **950 PASSED lines** and ends:

`950 passed, 1062 subtests passed in 85.57s (0:01:25)`

No standalone `FAILED`/`ERROR` summary appears in that saved output. The **1062 count is subtests**, not an additional number of ordinary collected tests. The receipt describes synthetic fixtures in an isolated tracked-file copy; this static gate does not turn that historical receipt into a fresh test run or independent financial validation.

`final5-test-input-manifest.json` records **1817** input-file hashes, consistent with the map length, copied at `2026-10-23T21:59:22.251705+00:00`. The following seven critical entries were independently matched across that input manifest, the scope-and-validation receipt, current fixed-source bytes and frozen upload bytes where uploaded:

1. `v6_submission.py`.
2. `submission-jof/manuscript-content.json`.
3. `submission-jof/manuscript.tex`.
4. `submission-jof/manuscript-preview.pdf`.
5. `submission-jof/supplement-content.json`.
6. `submission-jof/supplement.tex`.
7. `submission-jof/supplement-preview.pdf`.

All seven match. This is deliberately not a claim that all 1817 test-copy entries match later administrative logs/state written after that copy.

The retained numeric-output record reports 15,255 matched numeric tokens and zero mismatches, under its explicit archived-consistency scope. That record was inspected and hash-bound; its validator was not rerun, and it is not treated as independent replication.

## Whitespace exception remains visible

The saved whitespace receipt records command `git show --format= --check 9811ad4`, **return code 2**, and **286 trailing-whitespace issues**. The saved output and issue inventory identify exactly:

- **143** lines in `notes/revision-v6/final5-pytest-output.txt`.
- **143** lines in `REVISION_V6_CHANGELOG.md`, which contains the literal complete stdout duplicate.

Each referenced saved line was independently checked to end in spaces/tabs. The full stdout byte sequence is present verbatim in the changelog. All recorded issue types are `trailing whitespace.`; their paths are the two literal-evidence files above. The disposition retains the captured evidence without normalization. No whitespace-clean claim is made, and the nonzero return code is not hidden or relabeled as success. This gate does not run a new whitespace command or treat the retained check as fresh testing.

## ZIP contents and source binding

`submission-jof/overleaf-package.zip` has SHA-256 `e3d8f10cc65f1a6ce326d7041fc4fe3ecb95a98058154eecc9f4b62af7f2e5a6` and exactly **16** unique regular-file members. Every member is relative, has no traversal/backslash/symlink entry, and exactly matches the corresponding **current fixed-source tracked asset bytes**. All 16 hashes also match `notes/revision-v6/overleaf-manifest.json`.

Exact member inventory:

- `main.tex`, `manuscript.tex`, `supplement.tex`, `title-page.tex`.
- `references.bib`, `README.md`, `cover-letter.md`, `AUTHOR-TODO.md`.
- `figures/conditional-annual-primary.pdf`.
- `figures/conditional-common-history.pdf`.
- `figures/conditional-primary-tradeoffs.pdf`.
- `figures/endpoint-peak-example.pdf`.
- `figures/murphy-fx_hourly.pdf`.
- `figures/murphy-nyfed_weekly.pdf`.
- `figures/wp3-murphy-fx_hourly.pdf`.
- `figures/wp3-murphy-nyfed_weekly.pdf`.

The author TODO and cover-letter draft remain their existing tracked drafts; this is not a signed declaration, journal submission or publication-approval claim.

## Privacy and excluded material

The exact 26-path upload set contains no raw FX source file, private per-origin vector, third-party paper PDF, UI capture, credential file, `.bak`, `.env` or private-scratch payload. The ZIP contains only the specified manuscript/supporting text and the eight authored figure assets above, not data arrays or paper-source PDFs. The stage tree's absolute local prefix does not become a ZIP member path.

The text artifacts were scanned for private-key headers and recognizable GitHub/OpenAI/Bearer credential signatures; no hits were found. The test input manifest is a path/hash inventory rather than a copy of those input bytes, and contains no `.bak` or private `.scratch/` entry. Reference URLs, local source paths and aggregate hashes in existing audit records are not mistaken for copied raw data or vectors. No credential or UI operation was performed by this gate. Pre-existing untracked backups and another worker's notes are outside this exact plan and were not opened or added.

## Exact planned file bindings

Each row below independently matched planned length/SHA-256, frozen-stage bytes and the source commit's regular-file Git blob. The first verification also matched the then-current worktree/index; the two later administrative differences are disclosed above. The audit note itself is not one of these 26 planned uploads.

| Planned relative path | Bytes | SHA-256 | Source Git blob |
|---|---:|---|---|
| `REVISION_V6_CHANGELOG.md` | 446052 | `0916331d35fd9e9765eb34dd61dea57f46a555693e08f265b2840ad2e0f9d3f1` | `da36ec9b9cdb430eb3733206c08fa1cc92d97701` |
| `v6_submission.py` | 21164 | `9f4984fc802f8a2e1375760d78cbe59ae04aa814bb83114d6707b70ac01b61c8` | `7b512f0a5ccaf8c31be715ab80a2ef789a813673` |
| `notes/revision-v6/document-metrics.json` | 876 | `c7e48a5c4ef9586b4e917dc66ca01ace56b501a2f26aacd1db0283658a81e738` | `d311be6bfd2a8d27658d117bbb0803345fb0adea` |
| `notes/revision-v6/final5-pytest-invocation.json` | 927 | `5fb34159716a8f20740d0ef3af98eb7d0d06f4e0fc0906da906e700140666137` | `9e76e301427e79490ac5a83f58239605f0604af0` |
| `notes/revision-v6/final5-pytest-output.txt` | 126242 | `4d4917400f179cfecd42a0dead5b59451cfbb1edc70007ada8acbe634a248ad0` | `f0b00c45a31190270f294d44ca89d57515aab4a5` |
| `notes/revision-v6/final5-test-input-manifest.json` | 233814 | `de7ced7be3bfca080d117dc97165f958cd183bc29bf2beb9e07fe6df01e9f7e9` | `2e0df01cc6a03d5837c6cfbeb69bc10c781a86aa` |
| `notes/revision-v6/loop18-remote-publication-readback.json` | 4138 | `f5a5299cc6a304af61762e1053d30fc32e03dcee6a1f72248f2b19142e0f14a8` | `0b8dcbff50b1d4f0664796506faf232012ef708f` |
| `notes/revision-v6/loop20-content-build.txt` | 162 | `9d240d72fd238ccef68734aa03ea184dc458de61d8fe9e51ab3ab3382f2a8887` | `a0040c4271897b09d7d83783b00c12f533eab21c` |
| `notes/revision-v6/loop20-main-raster-identity.json` | 5241 | `a4bd059dad495061acc9467d54dbdeac1dba6d3a7e83d93031201a071dd43795` | `be48d3f48be482dc3e7f99646b343275837c50b7` |
| `notes/revision-v6/loop20-native-compile.json` | 840 | `df6405b0174a346bf6ee181ada98c3228587f3bd309f7b6130ca0d9ef17b32fa` | `f5c93766cca64887024857e66e32dfecbc17c246` |
| `notes/revision-v6/loop20-numeric-output.txt` | 761 | `af767f7a2044fc0c8ff9ec55a4906d26c61e999e9899636563234f62d690893e` | `e0fa84179748b6863a8ec2371828dc879c75a587` |
| `notes/revision-v6/loop20-package-output.txt` | 167 | `f049895c54ff4a23c524d640729d1161e198d72397336308d29376a9fe506258` | `3ab229351aa82d57292d2214020e78dc24999a1a` |
| `notes/revision-v6/loop20-scope-and-validation.json` | 2059 | `51bbf743aa5ccb2832351638b46f2643716e551776c73dff55de0f84eece0893` | `e13c84bfb84e0f528f9b4b49b046cde35b28e9a9` |
| `notes/revision-v6/loop20-scope-check.json` | 2072 | `07cd64a983b6da040b7368bc4c4359abb3182255a5a159e820ab6843e4e90be5` | `5c79976d7131ab434ddb23ab8046161802148a20` |
| `notes/revision-v6/loop20-typeset-output.txt` | 876 | `c7e48a5c4ef9586b4e917dc66ca01ace56b501a2f26aacd1db0283658a81e738` | `d311be6bfd2a8d27658d117bbb0803345fb0adea` |
| `notes/revision-v6/loop20-whitespace-check.json` | 35095 | `2a02482d2eceb45e85ec1a4aae4b83e7e73104a00ce2e9b1503153b42e214f0b` | `6898cb333c679c7f9b7b206427797825f99a50a4` |
| `notes/revision-v6/loop20-whitespace-output.txt` | 49188 | `8832826b69bde164632e183f3c018be7f29430a7af9cf4d365e875a312ebba4e` | `cdcc7cbb504eb83d03c3083c775c96a26a801e58` |
| `notes/revision-v6/overleaf-manifest.json` | 1834 | `d367793c165c848e501749edba077fbfe061152e6ce45ca4b808d4912fbbbcae` | `ac8dd382c5a831b6826517efda0f85bcad12d956` |
| `notes/revision-v6/self-check-021.json` | 1066 | `67928c4882ae8ef92b0b058584871a4fa9cff0cf1b350854684145b060dc1cd3` | `e5ab6f316ce78cdf005de15e9393ad7623f1e071` |
| `notes/revision-v6/state.json` | 214147 | `e48ff696b977e3848720eb2647ee339978ca386cf166c8fc471f4b72d37e4ecf` | `971f6597a4e2a3681cf16f8718d24b5566ca51f5` |
| `notes/revision-v6/verification-loop-019-referee-A-scoring.md` | 21689 | `f81b89b41138e34c60cda8197f70d47c764d32504db0b94269e5f6edb72233fa` | `3a9e20516cbf9f0970b7d1ad22e2c452ba23fb87` |
| `submission-jof/README.md` | 2616 | `8fe118d94c1c6437ac8530b3cd61d650360aee5d116939b0766e7776e9577373` | `b72be555e252566ecb1d50c1d8a573770f6fdbfb` |
| `submission-jof/manuscript-content.json` | 196850 | `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186` | `99b94f37aaf7437eaace1685a9159353b150df57` |
| `submission-jof/manuscript-preview.pdf` | 406379 | `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6` | `a5e3300731b6ca71a031f8d59b6b0503f4fe1ff2` |
| `submission-jof/manuscript.tex` | 78822 | `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade` | `97362ac75063f2dfff07fb82ec86101733319f8c` |
| `submission-jof/overleaf-package.zip` | 432073 | `e3d8f10cc65f1a6ce326d7041fc4fe3ecb95a98058154eecc9f4b62af7f2e5a6` | `bdbd66fd035128f9a103a44d233b4a4b392b99f5` |

Recorded at **2026-10-23T22:07:00.883693+00:00**. Only this Markdown audit note is written. The gate is a static pre-upload identity/scope check of the frozen plan, not proof that any remote mutation has occurred.
