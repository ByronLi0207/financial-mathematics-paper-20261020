# Loop76 publication-snapshot audit

**PASS for exact immutable bytes, inventory, path/privacy and protected-file
scope; no publication blocker found.** This is not scientific validation.
Stage readback: 2026-10-23T23:20:41.722662+00:00.
Protected-file check: 2026-10-23T23:21:41.843277+00:00.
Only `.scratch/revision-v6/publication-loop76-plan.json` and
`publication-loop76-stage/` were audited; later77+ work is excluded.

Source: `7ab7bc666051025cba8ff5da6e035c684b4a3830`
Tree: `d8ceb43dbffae527f415c2c9ba747d8d53821e46`
Base: `fc83ee23cf1d8b431efb2fe88c284060615e3b63`
Remote-base object: `ad5b5b0c9b486d8ada8081e30679b679a4522304`
Plan SHA256: `33839fa2263aca7ecc72e8d1173e875c1e60cbf807e62f8610932c25643e7716`

Initial HEAD equaled source. Every candidate comparison uses that explicit
commit; later live HEAD/state/ledger progress does not alter this snapshot.

## Full stage and diff evidence

Exactly **33 files / 857015 bytes**, one root ledger +32 notes/state:
18 Markdown,15 JSON, all UTF8. Diff M=2 (ledger/state), A=31, no deletes,
renames or other statuses. Plan path set = actual stage walk = complete
base-to-source diff. Every stage size and full SHA256 equals the plan;
every actual byte equals `git show SOURCE:PATH`. The tree equals the plan.
No duplicate/extra/missing file, wrong absolute destination, batch-parent
mismatch, nonregular object, symlink file/directory/ancestor or Git mode
issue. All source objects are100644 blobs. Allowlist is only the ledger
and immediate notes/revision-v6/*.md|*.json, with no absolute/traversal/.bak
or other destination.

Commands: `git diff --name-status -z BASE SOURCE`; `git ls-tree SOURCE -- PATH`;
`git diff --name-only BASE SOURCE -- submission-jof results protocol manuscript '*.py' FINAL.md`.
The last query was empty. Stage/source equality, length and full SHA256
were independently compared. No project module was imported/run.

Complete compact inventory follows. N/=notes/revision-v6/;
V=notes/revision-v6/verification-loop-. Columns: destination, bytes,
first12 SHA256. Full hashes were compared, not merely these prefixes.
The full plan is bound above. Complete canonical inventory SHA256:
`c553963b5f2b1964d07e01c49ba03958ddfec2f5289f6477b9edf9dd0bb9bb30`.
Canonical form: records sorted by path, keys path/bytes/sha256, UTF8 JSON
ensure_ascii=False,sort_keys=True,separators=(',',':').

```text
REVISION_V6_CHANGELOG.md	469202	355407c9a5a6
N/loop60-publication-snapshot-audit.md	8174	ca640dcf8442
N/loop60-remote-publication-readback.json	6880	232883f5a230
N/self-check-028.json	1065	ad9352add01c
N/state.json	237169	9881491ded7f
V061-result-numbers-selection.json	8127	ec02bdd933a8
V061-result-numbers.md	3884	969c10ed452f
V062-original-metadata.json	3951	6b3fb2d819db
V062-references-selection.json	2164	be81af951439
V062-references.md	2341	731f800ec9fb
V063-referee-A-menus.md	6118	d3b61f53b9ee
V064-solver-convention-claims.md	2701	1f7dfb59e8e8
V065-result-numbers-selection.json	10620	5e5537a669d6
V065-result-numbers.md	4518	6cb1cad4e3ba
V066-original-metadata.json	6315	ace786e78f32
V066-references-selection.json	2256	9bea54f421f2
V066-references.md	2050	6d5b65b670cb
V067-referee-B-data.md	5071	dcf54c2396c1
V068-historical-evidence-claims.md	1694	d891fb6c9f67
V069-result-numbers-selection.json	10284	952789959e14
V069-result-numbers.md	4437	ed9b7ac2a2e2
V070-original-metadata.json	2719	07ed22c69729
V070-references-selection.json	2258	2a50949308ec
V070-references.md	1856	1f0f83a41cb6
V071-referee-A-targets.md	6509	5bc9ea15a29c
V072-submission-claims.md	5556	117491968fca
V073-result-numbers-selection.json	13110	da3150aeee08
V073-result-numbers.md	4504	9d73d7575bfb
V074-original-metadata.json	6064	950c77290c76
V074-references-selection.json	2344	e4a3fdb43f1e
V074-references.md	1919	a7d2045c1310
V075-referee-B-transport.md	5641	ed79082a7418
V076-journal-cap-claim.md	5514	8bb73413ad91
```

Locally available remote-base object and base have identical tree
`61019cb16a0d3e1ae3f4310c330d7732eb8bf4f4`.
That is local object continuity, not a live remote-branch readback.

## Protected files and seven artifact fingerprints

Fresh streaming SHA256 against the immutable state's1413 historical
protected_v5_sha256 entries: missing0, changed16, allowed16, unauthorized0,
allowed-set difference0. The changed set equals committed allowed_v6_changes exactly. Those are
historical v6 differences, not new changes in this delta. Streaming hashes
did not interpret observations or repeat a scientific process.

All seven files below have identical base/source/local bytes. Names are
relative to submission-jof/; full fresh SHA256 follows. PDFs and ZIP were
fingerprinted only, without rendering, compilation or extraction.

```text
manuscript-content.json	324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186
manuscript.tex	57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade
manuscript-preview.pdf	c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6
supplement-content.json	738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28
supplement.tex	986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8
supplement-preview.pdf	7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991
overleaf-package.zip	e3d8f10cc65f1a6ce326d7041fc4fe3ecb95a98058154eecc9f4b62af7f2e5a6
```

## Privacy and inert source data

All files decoded as UTF8; all15 JSONs were recursively scanned. No common
GitHub/API-token, private-key header, literal Authorization bearer/basic
value or conventional password/token/secret/cookie/session key was found.
No conventional raw/encoded-vector key, numeric list>20 or long base64-only
payload. Maximum numeric list6 is loop061 actual_formatter.lines metadata;
claim-object frames and path/hash dictionaries are provenance.

No raw FX/private per-origin vector container, credential/session payload,
account UI transcript/capture, image, PDF, archive or backup destination
was found. Public repository commit/tree/file/PR receipts are metadata;
synthetic "private" names and boundary prose do not embed private vectors.
These bounded allowlist/schema/encoding/conventional-secret checks do not
guarantee detection of every possible secret syntax or covert encoding.

Bibliographic fields, scope failures and historical action/instruction
strings are untrusted data: no eval, code import, shell interpolation or
follow-on task. Their byte identity does not validate prior conclusions.
Loop076's cap/access-gap note is unchanged; no web/policy recheck occurred.

## Actual whitespace and inherited exceptions

`git diff --check BASE SOURCE` returned **0, no output** for this exact
new delta. It does not relabel any historical check as clean.

Both loop12/20 whitespace receipt JSONs still record return2 and286
stdout/ledger issues. Those receipts, both whitespace-output texts and
final4/final5 stdout files are byte-identical base-to-source; old ledger
bytes remain an exact prefix. No stdout normalization occurred.

Fresh rerun `git diff --check f193fbff35e2474f4266d8c12a777b242287f33c
ed4bfc26850af5564b8fe8047693196e15975d99` returned2 with exactly:
```text
verification-loop-021-limitations-numbers-selection.json:189
verification-loop-025-accuracy-numbers-selection.json:366
verification-loop-025-accuracy-numbers.md:241
```
All three paths are under notes/revision-v6/; each finding is "new blank
line at EOF". Files remain byte-identical base-to-source with the blank
line retained. Their accepted note-only nonblocking exception is explicit,
not normalized or conflated with the new-delta return0.

## Handoff boundary

Only this audit note was written, outside the33-file plan. No other edit,
staging/commit, cleanup, analysis/test/model/statistic/proof, UI/network/
upload, nesting or Claude/cross-model action occurred. Root must read this
note and verify post-upload destination bytes; local receipts do not prove
live remote state. Final hash/time follow full readback; no later rewrite.

**Exact candidate PASS; no blocker found; historical exceptions retained.**
