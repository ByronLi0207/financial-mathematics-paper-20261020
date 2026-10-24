# Current v8 Journal of Forecasting revision

The authoritative v8 authoring sources are `main.tex` (which inputs `manuscript.tex`), `supplement.tex`, and `title-page.tex` in this directory. The selected title is **Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits**. This is a retrospective comparison of peak forecasts, supplemented by the prespecified calibrated simulation.

The exported v8 package contains a **15-page main manuscript, 25-page Online Supplement, one-page title template and one-page cover letter**. All are native LaTeX PDFs. The compilation receipt and package manifest in `notes/v8/` bind the exact source, PDF and ZIP bytes; the final verification and page-review records identify the completed checks. Compatibility previews contain the same bytes as the current native PDFs.

## Compile the current documents directly

From the repository root, with an existing compatible Tectonic installation:

```sh
cd submission-jof
tectonic main.tex
tectonic supplement.tex
tectonic title-page.tex
tectonic cover-letter.tex
```

XeLaTeX is the alternative supported source route; resolve references with the usual repeat compile if required. `main.tex` is only the main entry point and does not compile the other two documents. Compile the supplement and title page separately. The main source carries its author-year bibliography; `references.bib` supplies matching structured reference metadata. This route does not require running BibTeX or downloading a project-specific journal style.

**Keep the edited v8 TeX as the source of truth.** The v7 builders `notes/v7/build_main_v7.py` and `notes/v7/build_supplement_v7.py`, the v6 builders, older `*-content.json` schemas and the historical `build_tex.py`/`build_paper.py` routes describe earlier versions. Do not run them over the v8 manuscript or supplement: they would regenerate historical text. The v8 simulation fragment helper, `notes/v8/build_mc_supplement.py`, produces only its own fragment and binding ledger; it is not a full-supplement authoring builder.

## Current package map

|Item|Role|
|---|---|
|`main.tex`, `manuscript.tex`|Current editable main manuscript and its entry point|
|`supplement.tex`|Current editable Online Supplement, including every simulation cell and failure inventory|
|`title-page.tex`|Title and personal-information template, with author placeholders|
|`references.bib`|Structured reference metadata accompanying the native author-year bibliography|
|`cover-letter.md`, `cover-letter.tex`, `cover-letter.pdf`, `AUTHOR-TODO.md`|One-page cover-letter source/proof and personal submission actions|
|`manuscript.pdf`, `supplement.pdf`, `title-page.pdf`|Native review exports; compilation receipt records their current hashes/pages|
|`overleaf-package.zip`|Self-contained source/review package with a member-hash manifest|
|`*-preview.pdf`, `*-content.json`|Current source snapshots and byte-identical PDF aliases|

The final v8 figure set is:

- `figures/v8-endpoint-peak-example.pdf` — Figure 1, with ordinary readable y-axis numbers; the formatting change does not change the financial results or example data.
- `figures/v7-murphy-fx_hourly.pdf` — the retained FX elementary-score comparison.
- `figures/v7-murphy-nyfed_weekly.pdf` — the retained Treasury elementary-score comparison.
- `figures/v8-calibrated-mc.pdf` — the archived calibrated-simulation figure.

The package check verifies that figure files, active source references, compiled PDFs and ZIP agree. Earlier figure files remain historical resources and need not be deleted. All author, affiliation/contact, ORCID, funding, competing-interest/conflict and AI-use fields remain `[TO BE COMPLETED BY AUTHOR]` for personal completion.

## Simulation record and chronology

The main grid uses **100 repetitions and 500 evaluation origins** per complete cell, with **2,000 oracle paths** per origin. It retains all **24 cells: 17 complete and 7 failed**. P1/P3 are not supported; P2/P4 are unassessable because required hourly cells failed. The failed cells have no substitute partial-repetition summary. This bounded mechanism check does not reproduce the persistent weekly financial losses and does not establish the long-history hourly mechanism. All original adverse, failed and unavailable financial outcomes remain in the full record.

- [Frozen design](../protocol/v8/mc-design.md): committed alone as `b7e548df39bc2d5dc0108a01ec8a7c2ccfbb99d4` at **2026-10-24 00:37:44 PDT / 07:37:44 UTC**, before calibration and pilot computation.
- [Frozen run plan](../results/v8/mc/run-plan.json): committed as `c66fc9d71fa4009214537a0e128ec53288dd9191` at **00:46:17 PDT / 07:46:17 UTC**, before the formal run.
- [Formal receipt](../results/v8/mc/formal/receipt.json): formal start **2026-10-24 07:46:22.956722 UTC**. [Completion](../results/v8/mc/formal/completion.json) records **1209.614 seconds**, with no unfinished jobs. The simulation ran once; failed candidates were not retried.
- [All cell summaries](../results/v8/mc/summary.csv), [predictions](../results/v8/mc/predictions.json), [calibration](../results/v8/mc/calibration.json), [environment](../results/v8/mc/environment.json), [repetition records](../results/v8/mc/formal/replicates.json), and [analysis/failure contexts](../results/v8/mc/analysis-facts.json) identify the executed procedures and results.
- [Chronology ledger](../notes/v8/commit-chronology.json), [field bindings](../notes/v8/mc-supplement-bindings.json), [writing-number review](../notes/v8/writing-numeric-review.md), and [internal simulated-review responses](../notes/v8/mock-referees.md) document the readback and revision.

These internal simulated reviews were generated by the same model. They are not external referee reports or cross-model approval.

## Document reproduction versus financial replay

Direct TeX compilation renders the supplied sources and figures; it reads no raw FX input and reruns no forecasting experiment. Source-field checks and regeneration of the simulation fragment likewise differ from calibration, Monte Carlo execution and financial replay. A successfully compiled document is not proof that restricted-input forecast results have been independently reproduced.

Raw FX observations and private financial per-issue vectors are **not redistributed**. The FX metadata says “Data files © Original Authors”; obtain the exact compatible input through the owning source and verify its recorded fingerprint before any authorized replay. The unchanged accepted New York Fed snapshot retains its attribution and continuing source terms. Related weekly categories share a reporting system and economic components, and the downloaded economic-date vintage is not reconstructed first-release information.

The [version-specific reproduction guide](../protocol/revision-v6/REPLAY.md), [original source guide](../results/revision-20261022/EXTERNAL_DATA.md), and [extended-results index](../EXTENDED_RESULTS.md) describe their historical data/commit requirements. The v8 simulation's actual environment, calibration, settings, design and immutable run plan are linked above. Full replay requires compatible exact inputs, the relevant frozen implementation and a separately intended new attempt; it is not part of document compilation. Preserve the approved results rather than overwriting them. Calibration cannot be reproduced from a public archive that excludes its raw FX prefix.

## Branch comparison and author decisions

v8 starts from frozen local v7 commit `5e35dba21ea5ced708dad47cbee29fe12e4c6936`. The initial remote v7 tree differed while another chat was uploading; [the B0 record](../notes/v8/b0-baseline.json) and [numerical reconciliation](../notes/v8/pr3-v7-reconciliation.md) retain that observation. v8 continues from the local base rather than silently incorporating the moving upload.

B7 publishes only `revision-v8` and checks the [v7-to-v8 compare view](https://github.com/ByronLi0207/financial-mathematics-paper-20261020/compare/revision-v7-final...revision-v8). Link availability and the final branch head remain a B7 check. The compare view uses the remote branch tips; the frozen local starting identity above remains the revision's provenance. A PR, merge, journal upload, author declaration or further incorporation of v7 is a later author decision. See [AUTHOR-TODO.md](AUTHOR-TODO.md) and [v8 author decisions](../notes/v8/author-decisions.md).
