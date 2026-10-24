# WP8 packaging and design-history audit (read only)

Scope: review of WP8–9 and the owning v7 delivery receipts, current submission
files and local Git objects. This note is the only file created by the auditor.
No bundle, archive, source, sealed study, ledger, final report, commit or remote
state was changed. The root agent is refreshing delivery concurrently, so the
stale-file observations below describe the audit snapshot rather than its final
package.

## Delivery issues already handed to the root

- `submission-jof/README.md` still says v7, 17/20 pages, and recommends the v7
  builders as current. Running those builders would overwrite v8 text.
- `submission-jof/AUTHOR-TODO.md` still says this revision adds no model,
  financial sample or statistical test. Replace that dated assertion with the
  actual v8 studies and their limitations; retain the prospective-binding limit.
- Both `*-content.json` files are `v7-latex-snapshot`, with stale source hashes,
  stale embedded LaTeX and bindings pointing only to notes/v7. Regenerate them as
  clearly labelled v8 LaTeX snapshots, retaining the historical-v6 pointer.
- Main and supplement canonical PDFs had been refreshed, while the corresponding
  `*-preview.pdf` aliases were still byte-identical to the old v7 PDFs. Title
  canonical/preview bytes were equal and unchanged from v7.
- The Overleaf ZIP still contained the 11 v7 members. Its manuscript, supplement,
  bibliography, cover letter and all three current v7-named figure PDFs differed
  from the working files. The package lacked all five `generated/v8-*.tex` inputs
  and both v8 MC figure inputs. Preserve figure filenames if already referenced;
  membership and exact bytes, rather than a filename's version prefix, control
  currency.
- Root README still leads with v7 and links the v7 ledger. Its preserved historical
  v6 paragraph links current aliases while giving obsolete 18/94-page ReportLab
  claims. Correct the routing to `manuscript/revision-v6-preserved/` or label that
  prose as historical; do not relabel preserved historical PDFs as native v8.

Minimal release sequence: settle all TeX/generated/figure/reference/cover bytes;
compile the actual canonical targets; render and review those exact PDFs; copy
native PDFs to compatibility aliases; update version/page/route statements and
JSON snapshots; build the ZIP from explicit transitive inputs; extract it into a
new isolated directory and compile all three targets using only its members;
record member hashes, source/alias equality, page counts and log diagnostics.
Retain the 1645 protected original paths and all sealed v8 study paths unchanged.

## Design identity survives only if local Git objects are retained

Local v7 `b571f324a253480b4e39bc8a8096775ddbcc7017` and browser-published v7
`d119a1fb30c48ceab9000552057882938cfa57a4` have the same complete tree,
`168620f47712c84a22878e77f540a4d151e08fdb`, but different histories. A browser
upload of the v8 working tree similarly does not deliver local design commits.

The three unchanged drivers use `git rev-parse` and `git show` to compare design
bytes to the exact pre-result commits:

- WP3: `039f6f1b49d46610697bed5300cab687b37951df`.
- WP4: `1427dc0b943ee77a82ee03a67ec9281c20e2cdf5`.
- WP5: `467a995b16a1c6446b5927992faec26b7f5f6276`.

All three are ancestors of the audited local WP7 tip
`d1367200a056a9e7e17a3918c7d026b7af462645`. The exact remote main prerequisite
`65feeee801b6b228a608ca3200e0678bb5f62b1c` is also an ancestor. The local range
main..WP7 contains 388 commits. Do not substitute the tree-equivalent browser v7
commit for any frozen design commit, rewrite sealed driver constants, or require
the recipient to possess unpublished local b571f324 as a prerequisite.

Proposed creation command for the root (NOT executed by the auditor):

```text
git bundle create .scratch/revision-v8/wp8/design-history.bundle refs/heads/revision-v8-goal ^65feeee801b6b228a608ca3200e0678bb5f62b1c
git bundle verify .scratch/revision-v8/wp8/design-history.bundle
git bundle list-heads .scratch/revision-v8/wp8/design-history.bundle
```

The command above is conditional and must not be published as-is: the additional
identity check below found one previously unpublished machine-local identity.
Preserve a private bundle if needed, but do not publish new private metadata
solely to supply design objects. An incomplete public history route must be
documented as such rather than silently weakening the sealed gates.

Use the named branch as the positive reference; record its exact tip before
creation. Avoid `--all`, which adds unrelated branches and remote refs. A bundle
created before the WP8 packaging commit intentionally proves the sealed design
history through its recorded tip, rather than claiming to contain the later
packaging commit or itself. Keep this distinction in its manifest.

The actual generated pack stream was measured without writing a bundle or file:

| Included tip, with remote-main exclusion | Pack bytes | MiB |
|---|---:|---:|
| WP5 design freeze 467a995 | 37,340,117 | 35.6103 |
| WP7 tip d136720 | 38,839,868 | 37.0406 |

These are pack-stream measurements, not final bundle byte counts; a small bundle
header is additional. Both exceed GitHub's 25 MiB browser-file cap. If publishing
through the authorized browser route, retain the complete generated bundle in
scratch and publish ordered binary parts of at most 20 MiB, plus a manifest with
each part's exact name, bytes and SHA-256, the whole bundle's SHA-256/bytes,
advertised ref/tip, prerequisite and three required design IDs. Do not publish an
unimportable truncated bundle or put these history parts inside the Overleaf ZIP.
The restore helper must reject missing/extra/reordered/changed parts and existing
output destinations, reconstruct the exact original byte stream, then verify
the whole digest before invoking Git. No dependency install is needed.

Proposed recipient commands after reconstruction, from the current v8 clone:

```text
git cat-file -e 65feeee801b6b228a608ca3200e0678bb5f62b1c^{commit}
git bundle verify /absolute/path/design-history.bundle
git fetch /absolute/path/design-history.bundle refs/heads/revision-v8-goal:refs/heads/v8-sealed-history
git cat-file -e 039f6f1b49d46610697bed5300cab687b37951df^{commit}
git cat-file -e 1427dc0b943ee77a82ee03a67ec9281c20e2cdf5^{commit}
git cat-file -e 467a995b16a1c6446b5927992faec26b7f5f6276^{commit}
```

A normal full GitHub clone includes the main prerequisite. A shallow clone may
need to fetch/unshallow its main history first. An exported source ZIP has no
Git object database and is therefore not this route. Import the archival ref
without checking it out: keep the current v8 document/source tree. Then call
only each driver's read-only `verify_design()` to establish gate availability;
do not run `--run`, `--summarize`, fitting or simulation in a packaging check.
Test these instructions in a fresh isolated repository that initially has only
the exact main prerequisite and its ancestry, rather than trusting a verify
performed in the already-complete working repository.

## History and path privacy findings

The proposed main..WP7 object set contains 5324 objects, including 3308 blobs;
aggregate logical object size is 268,750,487 bytes. There are 2714 distinct
changed path names. No historical changed path was an actual tracked `.scratch`,
`.env`, `.ssh`, raw FX, NPZ/NPY/parquet/pickle-style path under the checked
heuristic. Of 3161 text blob versions scanned with bounded standard OpenAI,
GitHub, AWS and private-key shapes, no credential-shaped candidate remained.
These checks are bounded screening, not proof that every possible secret is
absent.

808 historical text blob versions contain `/Users/` provenance paths; commit
metadata has three distinct author/committer email strings. A history bundle
preserves those historical personal/machine identifiers. Do not claim anonymous
or fully sanitized history. Redacting historical blobs changes identities and
would break the design-proof purpose, so no protected object was altered.

A later comparison used all seven fetched `refs/remotes/origin/*` histories.
The set of three local author/committer identities is **not** a subset of the
two identities already in those remote histories. Exactly one identity is
missing from all origin histories; its domain class is `local_machine`.
Local domain classes are `local_machine: 1`, `other_domain: 2`. Comparing only
origin/main, origin/revision-v7-final and
origin/codex/supervisor-revision-20261023 yields the same false/one-missing result.
No exact address was printed or copied to this note. Therefore the proposed
unmodified ancestry bundle would add a previously unpublished machine-local
identity. The root was informed immediately; public bundle creation/publication
is not recommended under its no-new-private-identity requirement.

Archive observations:

- Existing v6 `replay-metadata.zip` has 41 historical `.scratch/...` member labels.
  All members are public JSON metadata, not current scratch files. The ZIP hash
  and every member size/hash were rechecked against its immutable manifest:
  41 checked, zero mismatches. Its owning v7 adjudication is
  `notes/v7/s10-prepush-check.json`; preserve it unchanged.
- WP3 driver archive has 38,599 JSON/CSV/JSONL/log members, with no checked
  absolute/traversal/link/private-array path candidate.
- The existing protected nested `round2-execution-history.bundle` advertises
  c6332bb97d91b4861c975410f4376baab77b9580 with a2020e68... as its prerequisite.
  Its tip is absent from the current object database, so its packed payload was
  not recursively decoded in this read-only audit. Retain this limit or consult
  the owning historical audit; do not claim this audit exhaustively decoded
  every binary nested history payload.

## Follow-up: exact design objects without ancestor history

For each of the exact three design commits separately, both booleans
`author_identity_already_in_origin_history` and
`committer_identity_already_in_origin_history` are **false**. No address was
printed. Thus even a parent-free object pack of the exact design commits would
newly publish the same machine-local identity: it is in each commit object's
own bytes, not only in older ancestors. Redacting that field changes the exact
design commit ID. This blocks the proposed privacy-preserving public route.

Technical feasibility is a separate, conditional finding, not an implemented
or accepted public package. All three current `verify_design()` guards run only
`git rev-parse SHORT^{commit}` and `git show FULL:path` for their design files,
then compare file bytes and the declared code/specification/parameter hashes.
They do not run `git log`, `merge-base`, `rev-list` or a chronology/ancestor gate.
Consequently exact commit objects with their complete recursive trees/blobs
should suffice for these direct lookups, with omitted parents explicitly
unavailable; that inference was not tested by creating/importing a pack here.

The union of the three exact commit objects, their root trees and all objects
listed by `git ls-tree -r -t COMMIT` is 3 commits, 180 trees and 2800 blobs.
No immediate parent object is in this proposed set. Logical object bytes are
97,062,549; current existing compressed disk bytes total 35,576,240, which is
not a new pack size measurement.

If a private or separately authorized partial-object route were later chosen,
the mature plumbing sequence is: enumerate and freeze exactly that object-ID
set; feed it directly (without `--revs`, `--all` or `--thin`) to
`git pack-objects --stdout --no-reuse-delta`; index/verify the resulting pack;
compare `git verify-pack -v`'s complete object inventory with the manifest;
then import with `git index-pack --stdin --fsck-objects --keep=v8-design-objects`
in a fresh isolated recipient repository and exercise only the existing
read-only design guards. `--fsck-objects` checks object validity without
rejecting deliberately absent parent links. This must be labelled a partial
design-object set, not a bundle, complete Git history, independently certified
preregistration chronology or connected-history proof. A full `--strict`/
connectivity check will object to the intentionally omitted parents. No
`.promisor` marker or invented ancestry is appropriate. Preserve the imported
pack from garbage collection (a keep marker serves this purpose) and retain
all sealed source/constants unchanged.

Sources: <https://git-scm.com/docs/git-pack-objects>,
<https://git-scm.com/docs/git-index-pack>,
<https://git-scm.com/docs/git-verify-pack>.

## Prospective mapping statement to retain

`protocol/revision-20261023/prospective-parameter-binding.json` still marks
`historical_panel_only=true` and `prospective_results_pending=true`. Its expected
`round2_panel_run.py` hash is
`e3c0575dc50e3c9dc51395a43b1bd7daf06972395a4aaf4552713967146d76e9`.
The current canonical supervisor runner does not match that old binding;
`legacy_round2_panel_run.py` does. This is the deliberate v7 canonical/legacy
mapping recorded in `notes/v7/s1-conflict-resolution.json`, not a new corruption
to repair during delivery.

Retain: historical contracts and exact old-protocol replay remain tied to their
recorded source commits; the current legacy mapping does not activate, rebind or
prove execution of a future-data prospective protocol. The current supplement
already says this at its version-specific entry-points paragraph; preserve it
in the refreshed checklist and reproduction guide.

## Mature practice references

- Git bundle documentation: <https://git-scm.com/docs/git-bundle> — named refs,
  exclusion prerequisites, verification and importing to a separate ref.
- GitHub file upload documentation:
  <https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository>
  — 25 MiB per browser-uploaded file, at most 100 files per upload; browser
  uploads ignore `.gitattributes`, so exact byte readback remains necessary.

