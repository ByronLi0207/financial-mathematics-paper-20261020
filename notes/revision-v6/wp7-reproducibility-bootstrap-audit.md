# WP7 metadata bootstrap and fresh-clone limitation audit

Date:23 October2026. Scope:read-only repository verification/tooling assessment, not a new analysis or financial reproduction. Only metadata JSON/schema, Git path tracking, frozen source code and existing reproduction documentation were inspected. No numeric NPZ, raw CSV, financial vector, model, UI context or financial worker was opened/executed. No freeze, guard, source, document or result was changed. This new note is the only written file.

## Disposition

**A public metadata restoration pack is feasible and useful, but metadata restoration alone does not establish a fresh-clone v6 financial replay.** The unchanged workers are bound to historical paths and exact container/receipt identities. A fresh independent attempt can be used with those workers only after its required NPZ files and all six CSVs have been independently shown to match the historical byte pins, while the genuinely new attempt receipts remain intact. Equal means, equal arrays, `REPLICATION_AUDITED`, or a new receipt with the same scientific fields is insufficient.

If exact private-input identity cannot be established, retain the honest limitation: public document/aggregate regeneration and synthetic checks are available; the frozen financial v6 execution remains dependent on its exact locally reconstructed inputs. A separately versioned fresh-replay admission and output namespace would be another explicit task; it must not be smuggled in by weakening the current gates or changing the old freeze.

## Actual missing metadata and public-safety finding

`.scratch/` is ignored by `.gitignore:1`. The following inventory and40 companion manifests exist locally but none is tracked in Git:

| Metadata | Count | Total bytes | Current tracking |
|---|---:|---:|---|
| `.scratch/revision-v6/input-inventory.json` |1|343149|untracked/ignored|
| Original replay `*/public/manifest.json` referenced by that inventory |40|3093586|0/40 tracked|
| Combined exact-byte metadata payload |41|3436735|not a fresh-clone input pack yet|

The inventory SHA-256 is **`c5bc2e7c518cbd60ef17d6d74dbfec867fff0fac6ed294cdcb76ee1635055340`**, identically pinned by the WP2,WP3,WP4 and WP5-v2 execution freezes. All40 referenced manifest bytes match their inventory hashes.

The inventory holds source paths/hashes/byte counts; original and panel cell identities; NPY shape/dtype/Fortran-order metadata and origin endpoints; public source/selection bindings; the six aggregate CSV pins; historical admission flags; and explicit limitations. Its own scope says headers/endpoints only. There are **no numerical observation/forecast arrays** in it and no long list of numeric vector values.

The40 original manifests hold historical source identity, timestamps/resource measurements, selection/freeze fingerprints, aggregate/candidate/year/nonoverlap scores, artifact hashes, and **per-refit scalar diagnostics** such as training bounds, response scale, solver residuals/objectives and coefficient/dual-vector hashes. They do not contain raw source observations, per-origin issued capacities/outcomes, coefficient vectors or dual vectors. Consequently these files should be described as *historical phase receipts and scalar/refit diagnostics*, not as only aggregate means. They use the original public-phase receipt schema.

A complete metadata-only scan found:

```text
INVENTORY: LONG_NUMERIC_LISTS []; ABSOLUTE_USER_PATH_FIELDS []; CREDENTIAL_LIKE_KEYS []
40 MANIFESTS: SECRET_LIKE_KEYS []; ABSOLUTE_USER_PATH_FIELDS []; UI_CONTEXT_FIELDS []; LONG_NUMERIC_LISTS []
```

No credential-like keys, user absolute home paths, screenshot/plugin/conversation links or other private UI context were found. Under the project's existing raw/trace publication boundary, these metadata copies are public-safe. No such copy or publication was performed by this audit.

There are already **61 tracked panel metadata files**, all matching the inventory's expected hashes:one selection manifest,12 source provenance JSONs and48 public cell JSONs. They need verification/documentation, not another duplicate archive. The six `archived_path` CSVs are all tracked; their six historical `reproduced_path` copies are not. Raw FX, the12 panel source CSVs,40 original trace containers and48 panel trace containers are separate private inputs, not part of the metadata pack.

## What the unchanged gates actually require

1. **Whole inventory and scientific source identity.** `v6_worker.py:146–154` hashes the inventory against the frozen SHA; hashes both historical reproduced and archived forms of each of six CSVs against the same expected digest; and verifies the frozen executable file set. `setup` at61–68 verifies the exact original source bytes and existing selected QR parameter.
2. **Original trace container and original receipt.** `trace_entry` at73–82 selects exactly one declared source/H/W and phase/family entry, then requires its NPZ total bytes/SHA and companion manifest SHA before loading arrays. `original_trace` at84–113 subsequently checks full origins, exact stored loss identity, source-derived target/floor when supplied, and corresponding original receipt summaries. Restoring JSON never makes these numerical gates optional.
3. **Panel identity and public scalar reproduction.** `v6_panel_admission.py:67–157` requires the canonical inventory entry, original availability (`F`,`QR` available, plain `KNN` absent), frozen panel selection, exact source and provenance bytes, original public source/selection binding, exact chronological bounds and QR selection/refit metadata. At159 onward it pins the private NPZ, checks common full arrays/origins/floors and recomputes public scalar summaries. `preexisting_public_trace_digest_present` must stay **false**:the V6 inventory fingerprint cannot become a claim of an older public NPZ binding. WP3 calls the original freeze check before panel loading (`v6_wp3.py:67–75`).
4. **Private sources remain required.** The public panel provenance includes official API routes and exact downloaded hashes. Current API availability does not imply current bytes equal the retained vintage. The loader accepts the exact raw-source digest, not an edited provenance record or a newly aligned substitute. Do not forge historical source hashes or alter the inventory's expected identities.

The original inventory has40 trace entries across8 original cells:8 historical-reference bundles,8 QR evaluations,8 plain-KNN evaluations,8 QR validations and8 plain-KNN validations. The current WP2–5 callers use32 of these manifests (QR validation/evaluation, KNN evaluation, references); retaining all40 in a metadata pack is a small, complete archive of every reference in the frozen inventory, including the reusable `original_trace` API's KNN-validation route. It is unnecessary to publish the16 scaled-KNN phase receipts not referenced by this inventory, or duplicate the24 byte-identical numerical-audit receipt copies.

## Existing documented replay is not a v6 input-restoration route

The root README:104 documents:

```text
python3 -B reproduce_conditional.py replicate --attempt-id NEW_UNIQUE_ID
```

That command creates a new `.scratch/revision-20261022/replication-<ID>` tree (`reproduce_conditional.py:305–307,363–369`). It emits a genuinely new selection receipt and phase manifests (`:398,424–431`), with fresh timestamps/resource fields and a new selection SHA. It neither changes nor rebinds `.scratch/revision-v6/input-inventory.json`; v6 has no original-attempt selector. `REPRODUCIBILITY_V3.md:24` correctly explains that new phase receipts have new identities and must not overwrite the old archive.

Two extra restrictions matter:

- **Whole-file NPZ identity remains stronger than semantic array agreement.** The original writer validates one-dimensional numeric arrays, then writes `np.savez` (`run_conditional_study.py:525–535`). V6 pins the entire container. This audit does not claim a newly saved NPZ necessarily changes its SHA, or necessarily retains it; equality must actually be verified. Identical arrays or six scalar exports cannot replace that check.
- **`REPLICATION_AUDITED` is not an exact-byte-success shortcut.** The reconciler compares all six exports and records differences (`reconcile_conditional_replication.py:323–330,348–361`); the controller sets `REPLICATION_AUDITED` after a completed audit even if exact CSV agreement flags are false (`reproduce_conditional.py:440–445`). Any path that feeds the historical v6 gate must require actual six-file SHA agreement, not only the audit status. The existing README already says differences are retained rather than suppressed.

`reproducibility_guide.py` manages marked generated prose regions; it is not an input restore/admission tool. The submission README describes document and public aggregate generation, but currently does not document the private inventory/receipt restoration prerequisite. This is a reproducibility limitation, not evidence of a failed scientific fit or a reason to rewrite a historical result.

## Minimal public metadata pack recommended for root assessment

Without changing any frozen worker or numerical choice:

1. Preserve exact public copies of the inventory plus the40 historical manifests in a clearly named new metadata-only archive. Keep their original bytes, timestamps and hashes. Do not reserialize them, sanitize by silently deleting fields, or relabel a newly generated manifest as one of these historical receipts.
2. Add a small public restoration index listing each archived source filename, exact original repository-relative destination, byte count, SHA-256, artifact kind and the fact that it is a historical restore. List the existing61 public panel metadata prerequisites and six archived public aggregate CSVs by path/hash without copying those again.
3. A separate **metadata-only restore helper** may verify every packed byte/hash, reject absolute/outside-root/symlink destinations, refuse mismatching existing files, and restore exact historical metadata into an explicitly chosen execution workspace. It should be idempotent only for already identical bytes, never overwrite a different artifact, never modify a freeze/guard, and never run a model or start a worker. Its own fresh restoration receipt must distinguish archival receipt bytes from a new execution's genuine receipts.
4. Treat private input staging/admission separately. If a new original replay is to supply trace files, preserve its whole attempt and genuine receipts; require the historical expected NPZ bytes/SHA and all six CSV hashes before placing exact matching inputs at the fixed admitted paths. Equal scientific results with a different NPZ hash fail this route. Do not copy an archived aggregate CSV into a new replay and then call it recomputed; a historical CSV restoration is an archival operation, never proof of a new replay.
5. Keep the panel condition explicit:all12 exact source snapshots and48 exact panel traces still need legitimate local recovery/regeneration and the existing public-source/selection/scalar checks. The metadata helper cannot synthesize missing values, replace plain KNN, relax a source pin, or upgrade the historical public-NPZ claim.

The restoration index and helper are recommendations only. No pack, helper or altered README was created by this audit; root is assessing the appropriate scope.

## Output namespaces and honest executable scope

Frozen v6 workers also hardcode output paths (`v6_worker.py:18–20,27–35`):public receipts use `x`, private containers use `xb`. The already published receipts in a fresh Git clone therefore prevent running the same execution directly over that published tree. WP4 and WP5 likewise use fixed exclusive outputs. The original conditional replay's `--attempt-id` does not solve this v6 namespace issue.

A non-destructive staging route could create a **new isolated execution tree**, copy the exact frozen executable/specification and admitted prerequisites there, and leave future output slots absent while preserving the published archive elsewhere. That staging must explicitly distinguish prerequisite selections/metadata from output artifacts; it is not permission to delete retained outcomes or edit frozen paths. If root does not implement and test such staging now, document the limitation plainly:the frozen scripts and public archives permit integrity/aggregate checks and exact-input historical execution, while a turnkey fresh-clone financial v6 replay is not yet supplied.

No new financial run is needed to state this limitation accurately. Synthetic tests for a future metadata helper should concern byte identity, safe paths, missing/mismatching inputs, idempotent exact restoration and no overwrite/no worker invocation; they must not simulate historical identity by editing source/trace pins.

## Captured fingerprints and literal metadata checks

```text
c5bc2e7c518cbd60ef17d6d74dbfec867fff0fac6ed294cdcb76ee1635055340 .scratch/revision-v6/input-inventory.json
c12878f4dd441b1d8bed05c8ada00fb370912ce8251a2c2b4e027217140efddc v6_worker.py
40a2ba77a89c4eb77598bd66e3dd0f779012479b13b23f43312ff5f1e0ab31a6 v6_panel_admission.py
ebd297391f53250fb8991dc33c5911638214749c06c38c67cef88e0ff5af50dd reproduce_conditional.py
e5f7d26e696a28202c7fd6e9422a2777f0e9e00dbb775732632feb5e2e576fcc reproducibility_guide.py
a4a7c4ca351df7f7b3af4855ef0d01333f0efb939c935d8a40179c596834d8e9 README.md
96de320647b6c1e3bedbb9375708cc925bb9f4974c0df5acabb9a6b03077e3aa submission-jof/README.md
```

The read-only checks were Python3 JSON/schema/hash reads and `git ls-files` path membership. They did not follow/open any NPZ/raw path listed in the inventory. Literal summary output:

```text
INVENTORY 343149 c5bc2e7c518cbd60ef17d6d74dbfec867fff0fac6ed294cdcb76ee1635055340
ORIGINAL_TRACE_COUNT 40
MANIFEST_COUNT 40 BYTES 3093586
TRACE_EXPECTED_MANIFEST_MATCHES 40
TRACKED_INVENTORY False
TRACKED_ORIGINAL_MANIFESTS 0 of 40
TRACKED_PANEL_METADATA 61 of 61
PANEL_METADATA_HASH_MATCHES 61 of 61
TRACKED_ARCHIVED_SIXCSV 6 of 6
TRACKED_REPRODUCED_SIXCSV 0
RESTORE_METADATA_TOTAL_BYTES 3436735
```
