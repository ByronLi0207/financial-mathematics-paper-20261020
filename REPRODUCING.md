# Reproducing submission-final

The current scientific sources are `submission-final/`; upload files are mapped in `submission-package/MANIFEST.md`. This round does not run experiments, refit models or change frozen results. All instructions below describe separate reproducibility operations, not evidence that they were executed in this round.

## A. Compile documents without financial data

The four PDFs in each journal package contain the manuscript, supplement, title page and cover letter. The `main-document-source.zip` and `supplement-document-source.zip` are independently compilable single-document uploads. Unpack into an empty directory, select the entry shown in `notes/submission/upload-source-archives.json`, and compile with an existing Tectonic or compatible LaTeX installation. No financial source data are needed. This task uses cached Tectonic resources (`-X compile -C`); network package downloads are disabled.

To regenerate from canonical sources, use an existing Python interpreter with uv's temporary dependencies. Run from the repository root; the scripts do not install into system Python:

```sh
python3 notes/submission/prepare_templates.py
uv run --offline --no-project --no-env-file --with pypdf python -B notes/submission/build_asmbi_package.py
uv run --offline --no-project --no-env-file --with pypdf python -B notes/submission/build_qf_package.py
uv run --offline --no-project --no-env-file --with pypdf python -B notes/submission/build_shared_materials.py
uv run --offline --no-project --no-env-file --with pypdf python -B notes/submission/build_editable_tables.py
```

`prepare_templates.py` verifies and extracts only the two already archived official template ZIPs. It performs no download. The builders document their local runtime and font requirements; change executable/cache paths for another machine. Chinese author-preparation attachments use an existing local font; their PDFs embed the font subset. Publisher source packages include their actual required fonts. ASMBI uses its permitted initial Free Format route because original NJDv5 dependencies are unavailable in the local cache; the original class was not claimed to compile.

After any edit, rebuild upload ZIPs, render PDFs, check every changed page and refresh the manifest. Use a fresh `--run` name with `build_upload_archives.py` and `render_packages.py`. Output receipts bind the actual bytes and commands. Rendering alone does not establish that a page was visually reviewed.

## B. Inspect saved evidence without fitting

Read `notes/submission/prediction-register.json` and its file-hash/JSON-pointer bindings. Read the original summaries under `results/` and imported WP2 evidence under `evidence/submission/final-jof/`. The import audit preserves design-before-run timing but does not turn a local design commit into an externally public registration. Unsupported, untestable and numerical-failure results remain in their original files.

The bounded release ZIP contains code, written protocols, aggregate results and reproduction instructions. It excludes all raw inputs, private per-issue vectors, unit traces and historical Git objects. It is suitable for code and aggregate inspection; it cannot by itself recreate every financial run or satisfy the full historical test suite.

## C. Run software tests separately

Use the exact pinned offline command and numerical-thread settings in `notes/submission/baseline-single-thread.json` and the final test receipt. Set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `BLIS_NUM_THREADS` and `NUMBA_NUM_THREADS` to `1` before imports. The existing tests use synthetic fixtures and archived evidence; they are not a new financial experiment. Some historical provenance tests require the original local design Git objects. A shallow public checkout lacking those objects is not equivalent to the audited task checkout.

## D. Re-estimate financial comparisons only as a separate future operation

The unmodified historical [v13 reproduction recipe](notes/submission/historical-reproducing-v13.md) gives the raw-input identities, original menus and commands used in the saved G4 check. It can re-estimate comparisons and is not executed by this final round. It additionally needs the exact restricted FX input, original panel CSV and documented historical objects; fresh public-vintage substitutes do not establish equality. Never overwrite saved `results/` directories.

The earlier G4 record describes same-data numerical reproduction by the same execution agent in a fresh clone. It does not establish independent dealers, prospective success or a separate investigator's replication. See `notes/v13/independent-reproduction.md` for that record and its limitations.

## Rights and versioning

No project software license has been selected. Source-data and publisher-template rights are separate. Follow `notes/submission/zenodo-steps.md` only after author approval and account access; no account, DOI or deposit has been created. Citation metadata are in `CITATION.cff`, with author identity intentionally left to the author.
