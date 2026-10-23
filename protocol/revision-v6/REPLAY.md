# V6 reproduction routes and their limits

There are separate document, aggregate-integrity and financial-replay routes. Successful document regeneration is not independent financial validation.

## Public document and aggregate route

The current manuscript/supplement composition reads the retained v5 document snapshots, original specification and public aggregate JSON/CSV outputs. It does not load private observations or refit a financial model. With the documented existing runtime, run `v6_submission.py`, `v6_typeset.py`, `v4_numeric.py`, then `v6_package.py`. This writes only the current submission package and v6 audit notes. The older builders describe their dated releases and should not be used to overwrite the current package.

The extended numerical audit checks source-bound displayed content against its owning aggregate fields. It is an integrity check on the archived study, not a newly collected dataset or an independent replication. The ReportLab PDFs are separate previews; the three saved TeX targets also require native compilation diagnostics and formal export before submission.

## Exact historical metadata

`replay-metadata.zip` contains the exact frozen inventory and the historical phase receipts referenced by it. `replay-metadata-manifest.json` records every member's byte count and SHA-256. These JSON receipts include scalar/refit scales, convergence diagnostics and hashes, but no raw observation arrays, per-origin prediction vectors, fitted coefficient vectors, credentials or private UI records. The original member bytes are preserved; newly generated receipts are not relabelled as historical receipts.

Private raw FX and per-origin traces are deliberately absent. Follow the repository acquisition and source-term instructions. Access to a dataset does not establish permission to redistribute it. The precise historical panel vintages and trace containers are still required; downloading an updated series does not reproduce the pinned historical file.

## Read-only admission and isolated preparation

Use an existing Python interpreter; this standard-library helper installs and fetches nothing:

```text
python -B v6_replay_setup.py --check --private-input-root /path/to/exact-private-input-tree
python -B v6_replay_setup.py --prepare --target /path/to/new-isolated-tree --private-input-root /path/to/exact-private-input-tree
```

Check mode hashes bytes without decoding observations/arrays or running a model. It verifies the metadata ZIP, frozen inventory, every historical manifest, actual source/trace files and all six reproduced CSVs. `REPLICATION_AUDITED` alone is insufficient: the actual six CSV hashes must agree. NPZ admission is whole-container SHA-256 and byte size; equivalent arrays inside a differently serialized container do not pass the historical gate.

Preparation requires a nonexistent target with an existing parent. It first admits all required inputs, then copies tracked public files, exact metadata and admitted private inputs. It excludes the existing v6 result subtree so the original workers' exclusive output slots start empty. It rejects unsafe paths, symlink inputs, conflicting destinations, reserved outputs and metadata drift. It does not overwrite/delete an existing target, edit freezes, install dependencies, fetch data or execute financial workers. An I/O failure can leave a partial new target, which is retained rather than automatically cleaned or reused.

The current local admission receipt is in `notes/revision-v6/replay-admission-check.json`; synthetic tests cover the path/hash/output protections. A prepared tree is only an input/setup check, not proof of a completed financial replay. Use the original pinned numerical runtime and the exact frozen worker commands/phase order in the v6 ledger. Validation must precede selection and evaluation; the target-level canonical wrapper is `v6_tau_worker_v2.py`. Preserve new attempt receipts separately. Do not substitute them for old hash identities or disable gates to obtain a result.

If exact private inputs are unavailable or fail a hash, the financial route stops. The public document/aggregate route remains usable, but unconditional turnkey fresh-clone financial reproducibility and independent dealer validation are not claimed.
