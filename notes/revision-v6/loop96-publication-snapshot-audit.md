# Loop96 immutable publication-snapshot audit

**PASS for exact bytes, inventory, scoped content/privacy and receipt bindings.
Whitespace is NOT clean: return2,143 literal-stdout trailing-space findings.
No code/manuscript/privacy blocker was found; original stdout is retained.**
This is a publication gate, not independent financial replication.

Source: `581674aeded6ad5fb912c4183463e1f18b1d9c96`
Tree: `29ce5b3612c8e1a52b9ac413aa33c5a0b11cc268`
Base: `7ab7bc666051025cba8ff5da6e035c684b4a3830`
Remote-base object: `d1e1cb68ce90dce1a15b811416df86e0d4f10d44`
Private plan: `.scratch/revision-v6/publication-loop96-plan.json`
Plan SHA256: `db5f14a692a6460c5424e26541759a65974b8ca615a8c488cbd673b52dc1d8d0`
Stage: `.scratch/revision-v6/publication-loop96-stage/`
Actual stage readback:2026-10-23T23:47:32.487587+00:00; receipt/protected check:2026-10-23T23:49:24.284083+00:00.
Initial HEAD equaled source. All checks use explicit immutable blobs,
regardless of later live HEAD/state progress.

## Exact inventory and byte/path gate

Exactly64 files/2454589 bytes; batches root2,notes57,submission5.
Diff M=10,A=54; no deletes/renames. Plan, recursive stage walk and complete
base-to-source diff sets are identical. Every staged size and full SHA256
matches the plan and every byte equals `git show SOURCE:PATH`. Tree matches
the requested/declared tree. No extra/missing/duplicate path, symlink file/
directory/ancestor, nonregular object, absolute/traversal/.bak destination,
wrong batch parent or Git mode issue. Every object is100644 blob.

Allowlist: root ledger/v6_submission.py; immediate notes/revision-v6
md/json/txt; exactly README,main JSON/TeX/preview PDF/ZIP under submission-jof.
No result/protocol/manuscript-archive/FINAL change. The sole modified Python
file is v6_submission.py,8 inserted document-label lines and no deletion.

Commands used full BASE/SOURCE IDs: `git diff --name-status -z`,
`git ls-tree SOURCE -- PATH`, and `git diff --name-only BASE SOURCE --
results protocol manuscript FINAL.md` (empty); Python path query returned
only v6_submission.py. Byte equality/length/hash were independently checked.
No scientific code was imported or executed.

Complete compact inventory: N/=notes/revision-v6/; V=that prefix followed
by verification-loop-; S/=submission-jof/. Columns are exact path and bytes.
Full hashes are in the plan bound above and were all compared. Full inventory
SHA256 `0250db2436622c2a5677aeae4ec940f27eee1772a4593a319f4e76dc3ad234b9`,
over UTF8 JSON records sorted by path, keys path/bytes/sha256,
ensure_ascii=False,sort_keys=True,separators=(',',':').

```text
REVISION_V6_CHANGELOG.md	476763
v6_submission.py	21857
N/document-metrics.json	876
N/final6-pytest-invocation.json	927
N/final6-pytest-output.txt	126242
N/final6-test-input-manifest.json	255644
N/loop76-publication-snapshot-audit.md	8049
N/loop76-remote-publication-readback.json	7637
N/loop92-content-build.txt	162
N/loop92-current-tracked-whitespace-check.json	299
N/loop92-current-tracked-whitespace-output.txt	0
N/loop92-independent-language-scope-audit.md	8191
N/loop92-main-raster-identity.json	5045
N/loop92-native-compile.json	851
N/loop92-numeric-output.txt	761
N/loop92-package-output.txt	167
N/loop92-pr-readback.json	377
N/loop92-scope-and-validation.json	2182
N/loop92-typeset-output.txt	876
N/overleaf-manifest.json	1834
N/self-check-029.json	1065
N/self-check-030.json	1065
N/self-check-031.json	1066
N/state.json	245712
V077-result-numbers-selection.json	14156
V077-result-numbers.md	4687
V078-gibbs-bibtex-readback.json	799
V078-original-metadata.json	2889
V078-references-selection.json	2503
V078-references.md	2114
V079-referee-A-scoring.md	5613
V080-selected-fit-claims.md	2006
V081-result-numbers-selection.json	12549
V081-result-numbers.md	4503
V082-original-metadata.json	2218
V082-references-selection.json	2310
V082-references.md	1757
V083-referee-A-design.md	5595
V084-internal-review-status-claims.md	5347
V085-result-numbers-selection.json	14032
V085-result-numbers.md	4666
V086-original-metadata.json	3397
V086-references-selection.json	2089
V086-references.md	1533
V087-referee-A-accuracy.md	5753
V088-abstract-budget-claim.md	4507
V089-result-numbers-selection.json	12023
V089-result-numbers.md	4674
V090-original-metadata.json	2816
V090-references-selection.json	2276
V090-references.md	1373
V091-referee-A-comparator-labels.md	5347
V093-result-numbers-selection.json	14651
V093-result-numbers.md	4837
V094-original-metadata.json	3174
V094-references-selection.json	2343
V094-references.md	1859
V095-referee-B-conclusion.md	4843
V096-claim-scope.md	2797
S/README.md	2616
S/manuscript-content.json	198950
S/manuscript-preview.pdf	406405
S/manuscript.tex	78850
S/overleaf-package.zip	432084
```

Local remote-base/base trees both equal
`d8ceb43dbffae527f415c2c9ba747d8d53821e46`; this is local Git-object
continuity, not a new remote branch/file readback.

## Loop92 document and scientific-scope identity

Direct immutable base/source JSON comparison, excluding underscore
provenance, reproduces the candidate by exactly three authorized replacements:
H6/H24 legacy-reference -> H6 original-primary and H24 legacy-reference;
leave QR with -> leave wrapped QR (ACI-QR) with;
than the wrapped historical rule -> than wrapped F (ACI-F).
Full TeX equals the same exact transformation. All other visible document
content is unchanged, including numbers/order, abstract, tables, figures,
references, adverse findings and non-guarantee language. The raw provenance
and README/metrics/package changes are disclosed in the source-bound loop92
audit; they are not additional financial results. No underlying loss or
coverage statistic was recalculated here.

ZIP:16 same ordered members as base, no unsafe/unknown/symlink member.
Only manuscript.tex/README differ; all16 bytes match their source-tree files.
Current ZIP SHA256:
`9c88e513bb0df5b91c7890ca480074b8ab13e10363d07c158733c2b1afbba616`.
It contains the existing project figures, not third-party article PDFs.
The staged PDF is the expected current main preview, not a native export.

Fresh1413 original-protected-file hashes: exactly16 allowed historical
differences, no missing/unexpected change or allowed-set discrepancy.
The three Supplement critical files remain unchanged from base. No frozen
financial results, protocol or financial-engine edit appears in the diff.

## Saved validation receipts bound to these bytes

Each of the following seven full hashes independently equals the immutable
source blob, live local file, loop92 scope receipt and final6 input manifest:

```text
v6_submission.py
05f59e5c4f1a2facac3139a90a54792acb2e1c7c71bc0dc0f2be4726ec2e286d
submission-jof/manuscript-content.json
b9197f80173b8dccbb74cb2086cea202a4f2d1c1659768f7f62835a1a9a1510b
submission-jof/manuscript.tex
2eda351b4dcc707c48b95133d6745fbb13a0b7b3ac8af049a4b856e948f30f11
submission-jof/manuscript-preview.pdf
dbcf2d2d6bd301e36cecfca912717d5cdff8e935c770e56472e7c5d4d35d0714
submission-jof/supplement-content.json
738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28
submission-jof/supplement.tex
986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8
submission-jof/supplement-preview.pdf
7e569afe156cd518a070b48b5cbfa71312bcad23c7c8f8fa9153c2cce2042991
```

The manifest has1979 declared and actual entries. This gate checked the seven
critical bindings; it does not claim every historical manifest entry equals
later notes/ledger bytes. Invocation records return0,86.35929308296181s
elapsed,292012032B peak RSS. Saved full stdout has950 PASSED lines, no
FAILED/ERROR status lines, and summary:
`950 passed, 1062 subtests passed in 85.76s (0:01:25)`.
Variable spaces before progress brackets are retained. These are saved
synthetic-suite receipts, not a new run or independent financial validation.

The numeric receipt records0 mismatches/15255 matched tokens, and the scope
receipt binds that receipt to the critical source hashes. No numeric audit
was rerun. Native-compile receipt binds current main TeX and entry hashes,
records a success response, and expressly has formal_pdf_exported=false.
It must not be represented as an exported native-compiler peer-review PDF.

Raster receipt binds old/new PDF hashes to base/source,18 page records,
changed pages9/12 and actual viewed pages9/12,16 other pages identical.
This gate read the saved record; it did not rerender or view pages anew.
The source-bound prior language audit SHA256 is
`aa991c31cd716ac0267a976e2ad381f7e4a903f5f84f3a0f83be7ffa6fa7e9bb`.

The PR receipt's actual query result is `{"issues":[]}`, recorded
2026-10-23T23:43:48.134031+00:00. It records no same-head PR found then;
it does not say a PR was updated or prove perpetual/current absence.
No PR query/action occurred in this gate.

## Privacy/content boundary

62 nonbinary files decoded as UTF8; all31 JSONs were recursively inspected.
Types:23md,31json,6txt,1py,1tex,1pdf,1zip. No conventional GitHub/API token,
private-key header, literal Authorization value, password/token/secret/
cookie/session key, raw/encoded-vector key or long base64-only candidate
was found. No primitive numeric list>20; maximum5 is seeded draw metadata.
Hash inventories and longer claim/page objects are not private origin vectors.

Raw pytest names mentioning private/arrays/accounts are synthetic-test
identifiers, not private observations or account UI. The compiler response
is diagnostic text; raster records contain hashes, not screenshot payloads.
The binary exceptions are only the expected main preview and safe project
ZIP. No raw FX, private vector, credential, account capture, backup or extra
binary container was found. Registered metadata, failed assertions and
historical instruction strings were treated as untrusted data, not executed
or followed. These practical checks cannot exclude every covert encoding
or unrecognized secret syntax.

## Whitespace: actual current delta and inherited exceptions

`git diff --check BASE SOURCE` returns **2** with exactly143 findings,
all `trailing whitespace.` in
`notes/revision-v6/final6-pytest-output.txt`. No other path is reported.
This is new captured literal stdout, not a code/manuscript issue. Its exact
SHA256 is
`4c2520799321242bc64cec1959125846b041e5da910d1d271ba646ad333ae4cb`.
The root was informed before upload; committed/staged raw output is retained
under the instruction not to normalize original stdout.

The saved loop92-current-tracked check returned0 before this untracked
stdout entered the publication diff. Its limited historical scope does
not override the present return2. No complete-delta clean claim is made.

Both loop12/20 receipts still report return2/286 issues; both receipts,
both whitespace-output texts and final4/final5 stdout are byte-identical
base-to-source. Old ledger bytes remain an exact prefix. The three accepted
EOF-blank files also remain identical with their blanks:
verification-loop-021-limitations-numbers-selection.json:189;
verification-loop-025-accuracy-numbers-selection.json:366;
verification-loop-025-accuracy-numbers.md:241 (all under notes/revision-v6).
Nothing was normalized, deleted or relabeled clean.

## Handoff

Only this new notes/revision-v6/loop96-publication-snapshot-audit.md was
written. It is outside the fixed64-file snapshot by design. Later97+ notes
are excluded and must not be claimed published by this snapshot.
No state/ledger/source/stage/old-note edit, commit, deletion, test/model/
statistic/proof, UI/network/upload, nesting or Claude operation occurred.
Saved receipt verification is not rerunning its originating operation.
Root must read this actual note and verify post-upload destination bytes;
local receipts cannot prove the new remote state. Final full readback
hash/time are handed off separately, after which this note is immutable.

**Byte/privacy/scope gate PASS; whitespace return2/143 raw-stdout findings
and inherited exceptions are explicit and retained.**
