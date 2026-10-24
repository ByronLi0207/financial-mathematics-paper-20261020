# v8 execution plan and ledger

Authority: 导师v8十小时任务-20261024.md (user supplied). Goal start 2026-10-24 00:22:56 America/Vancouver; target ten hours.

Only the new clone and revision-v8 are writable. revision-v7-final, its original local directory, main and PR #3 are protected. No PR or merge. The approved base is the local v7 commit5e35dba; remote/local mismatch is recorded, not silently repaired.

|Stage|Budget|150% stop|Deliverable|Status|
|---|---:|---:|---|---|
|B0|0.5h|0.75h|Clone, identity, PR3-v7 core-number reconciliation|complete|
|B1|4.5h|6.75h|Standalone design commit before computation; TDD DGP/oracle;2-rep pilot;24-cell MC; formal<=5400s; predictions and plot|complete:17/24,7failed;P1/P3not supported;P2/P4unassessable|
|B2|1h|1.5h|One-page simulation subsection and supplement; map support;main<=18pages|complete:18main/25supp;1-page subsection|
|B3|0.5h|0.75h|At most3 finding contributions, elementary properties demoted;five places aligned|complete:3findings/5places;17pages|
|B4|1.5h|2.25h|PR3 writing conventions, one-decimal prose percentages, <=8%/20words/no>40, eight limits concentrated|complete:53paras;1.12%/12.24words/zero>40;15pages|
|B5|1h|1.5h|3 simulated referees x5 concerns and response table; unresolved toTODO|complete:3roles/15responses;futureT1-T6|
|B6|0.5h|0.75h|One-pageJoF coverletter, ordinaryFigure1ticks, figurelabels, metadata/placeholders|complete:16/25/1/1;145packageassertionsPASS|
|B7|0.5h|0.75h|Alltests/numericchecks/threePDFcompile andpageQA;pushrevision-v8only;comparelink|QA complete:1025tests/1090subtests,5049numeric,145package;42pages inspected;publication next|

## Rulings fixed before simulation

- Constant-variance AR(1) levels can retain state-dependent peak information. D0 remains the requested calibrated constant-variance control, but P1 is a hypothesis, not a guaranteed null. Do not tune the DGP to make F win. A separate high-positive-anchor Gaussian random-walk fixture tests oracle/F agreement in a state-invariant limit and is not called stationary.
- The main grid couples frequency, DGP parameters and source-specific validation length. Within-DGP W/feature contrasts are controlled; main-grid differences do not separately identify the effect of frequency or validation length.
- Secondary grids are optional and are not planned under the core resource budget. The prespecified R100/500 -> R50/500 -> R50/300 timing ladder will be fixed by the two-repetition pilot; the formal run has a single5400s deadline and no adaptive rule changes or retries. The design will give exact safety margins and failure handling.
- Calibration is estimation of simulation parameters using only original pre-validation rows; no new forecast experiment is performed on real financial evaluation outcomes.
- Existing v7 generated-paper builders/checkers remain historical. v8 uses separate authoring/check artifacts so fixed old C-label/binding-count checks are not edited into passing.

## B0 completion

New clone created with git clone --no-hardlinks from the approved local v7 branch, then switched to revision-v8. Original directory only read. Before calibration, pinned FX/Treasury snapshots were copied into ignored paths in the new clone with matching byte hashes. No downloads.

Public identity: b0-baseline.json. Private immutability manifest: .scratch/v8/b0-identity-private.json. Reconciliation: pr3-v7-reconciliation.md.

## 待用户决定

1. Local v7 and the first observed remote v7 trees differ while the other upload proceeds. Work remains based on the expressly approved local HEAD; final compare may include unpublished baseline files.
2. D0 is a constant-variance control, not a proof of no conditional information; the main grid does not independently separate frequency and validation-length effects. These scientific scope choices are recorded and will be reported conservatively.
3. Only revision-v8 will be published. The final compare link will be supplied; opening or merging a PR is left to the user.

B1 pending author decision: numerical feasibility of the seven hourly cells requires a later design. No retry or solver change was made; no full simulation mechanism claim will enter the contribution list.
