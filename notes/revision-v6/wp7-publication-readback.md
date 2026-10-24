# WP7 publication readback

At 2026-10-23T20:56:34.350100Z the complete 366-file v6 snapshot was read back from actual public commit `9afff7ebe1e015907cdf22caf46c480ab8bcab5a`. Every file matched SHA-256 and byte length. The complete Git tree also matched source commit `b895c67fcb719fcb5eef93b180d4e7757e2a3804`: both trees are `1a9ec87a4f88f70047be09bbee6bddcc4e0ae8f6`. Distinct UI/native commit histories were preserved; no force push, main merge or credential/permission change was used.

Publication used the signed-in native GitHub UI in 13 whitelisted batches; exact public file/commit validation used Git fetch. See `publication-snapshot-verification.json` for all file hashes and `publication-batches.json` for actually observed batch commits. Public material consists of aggregate results, fitted optimization diagnostics, code, tests, manuscript sources/previews and input/code fingerprints; private per-origin vectors, raw FX, screenshots, user account/UI records and third-party paper PDFs were excluded.

Literal complete-snapshot output:

```text
remote_commit 9afff7ebe1e015907cdf22caf46c480ab8bcab5a
files_checked 366
total_bytes 15428425
mismatches []
full_tree_diff_from_source ""
source_tree 1a9ec87a4f88f70047be09bbee6bddcc4e0ae8f6
remote_tree 1a9ec87a4f88f70047be09bbee6bddcc4e0ae8f6
```

Live all-state GitHub PR query `repo:ByronLi0207/financial-mathematics-paper-20261020 head:revision-v4-jof` returned `issues: []`. The authorized branch is published; no same-head PR was found and no new PR or unrelated PR update is claimed. Whether to open a new PR is retained in AUTHOR-TODO. Remote main remained `65feeee801b6b228a608ca3200e0678bb5f62b1c`.

This completes WP7's content/validation/branch publication scope, with the PR-absence decision explicitly outstanding. It does not complete the six-hour goal before 2026-10-24T00:31:50Z. Later ten-minute self-checks and authorized audit-loop notes are supplemental records and are not falsely included in the earlier frozen snapshot identity. The current manuscript/PDF/result bytes remain unchanged.
