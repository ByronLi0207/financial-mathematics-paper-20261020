# WP2 provenance reconciliation

**Final import gate: PASS for static editorial reuse of the pinned, already-computed WP2 evidence.** This append-only reconciliation resolves the provenance gap in the first audit. It does not rerun or alter scientific results.

The first `wp2-import-audit.json` remains unchanged at SHA-256 `509d8f8fc05c2cd538300a1ff53c918961a0ae3a4afa94dfc5b3f99332c365b4` and retains its historical UNVERIFIED decision. The Markdown audit also remains unchanged.

The parent root task captured read-only original Git object queries in `original-commit-proofs.json` and `original-blob-proofs.json`. This subagent did not access the old repository. I independently rebuilt the Git object header and SHA-1 of both supplied raw commit strings, obtaining their exact original IDs; I also rebuilt each pinned-source blob OID and SHA-256 and checked all seven WP2 mappings against the original-object records.

## Chronology and design boundary

- Original design commit `f2ce438ccb2fcf671c849a83032ac700ac6007c6`: author and committer **2026-10-24 22:19:50 UTC**.
- Fixed-source manifest formal start: **2026-10-24 22:25:19.696709 UTC**.
- Fixed-source saved study end: **2026-10-24 22:50:26.787681 UTC**.
- Original completion commit `1a535efe289254ced5b163361fefee357d13d583`: author and committer **2026-10-24 22:59:15 UTC**; its direct parent is the design commit.
- The design-stage commit contains six paths: the two protocols, design/preflight checks, the ancillary WP1 whitespace log and the changelog. It contains no result path. Therefore it is a separate design-stage commit, not a two-file-only commit.
- Public protocol/results uploads still occurred later. They establish publication, not pre-run public preregistration. The earlier FAIL for using public uploads as pre-run proof remains correct; original local Git provenance now supplies the required gate.

## Exact byte binding

| Original stage | Fixed-source path | Git blob OID | SHA-256 |
|---|---|---|---|
| Design | `protocol/revision-v9/wp2-confirmatory.json` | `f8efb043d2bffc2171a5fefd717ce4a0db22330b` | `11fc89b38b8691b91965abf5f3a284f1391576812650e1129ff31fc8e2342083` |
| Design | `protocol/revision-v9/wp2-confirmatory.md` | `fde0d8c214b28ab89bfe2ccd476f5446a682f1fe` | `b0efeec38100e62a245a8cc1d7a67365f51a526bd971bc11cbb59a922ab2fb6d` |
| Completion | `protocol/revision-v9/wp2-confirmatory.json` | `f8efb043d2bffc2171a5fefd717ce4a0db22330b` | `11fc89b38b8691b91965abf5f3a284f1391576812650e1129ff31fc8e2342083` |
| Completion | `protocol/revision-v9/wp2-confirmatory.md` | `fde0d8c214b28ab89bfe2ccd476f5446a682f1fe` | `b0efeec38100e62a245a8cc1d7a67365f51a526bd971bc11cbb59a922ab2fb6d` |
| Completion | `results/revision-v9/wp2/manifest.json` | `87aac16ac8945084292042df384621691f694d4e` | `9b749e73ed2757c6b3fb58e3ce0249a707fbc9f7d57eb5747e505c836b074ec2` |
| Completion | `results/revision-v9/wp2/summary.json` | `9286ed24eb5a11d45981e5a89755f1ebc45487b1` | `ab77dade64a67751f8e93b1bb18bc9a491c22a6efb2b5292840748e8a6b636bc` |
| Completion | `results/revision-v9/wp2/support.json` | `8b9bf77431a77f968462459b966e04f8b039c91b` | `11d65f6b2c05f7c752ff544aad9d474450d3af4723994f247dbc42f0ddaa1cf5` |

Both protocol files are identical at original design, original completion and pinned source. The completion manifest, summary and support files also match the pinned source exactly. This combines with the initial audit’s full own-receipt/member verification; no replacement financial data or changed scientific summary was admitted.

## Import recommendation and retained adverse evidence

| Saved criterion | Successes / fixed denominator | Missing | Saved screen |
|---|---:|---:|---|
| P1 | 47/48 | 0 | SUPPORT |
| P2 | 21/24 | 0 | SUPPORT |
| P3 | 42/48 | 0 | NOT_SUPPORT |

The reconciliation JSON carries the exact path/SHA/JSON-pointer bindings for this three-row minimum table and every method/DGP backing row. The first audit retains all ten prediction counterexamples, including all six failed P3 inequalities, and both QR4 penalty 0.001 NONCONVERGENCE candidate records. Do not hide these failures or convert P3 into a majority criterion.

Suggested scope language: “A finite-grid pooled synthetic screen under a locally committed pre-run design.” The index excludes parameter count and penalty menus differ; no oracle identifies an estimation-cost channel. This pass does not support a universal sample-size rule, a causal mechanism, independent dealer replication or pre-run public registration.

The allowed action is to import the small saved-results table with these bounds and failures. No experiment, original summary program, fit, score, bootstrap or driver was run; no scientific result was recomputed. No Claude/cross-model review was used.
