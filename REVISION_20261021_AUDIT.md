# Revision window and evidence

This revision concerns *Historical Response Selection for Sampled FX Net-Position Peaks*. It follows the original study and its separate [research-window audit](RESEARCH_WINDOW_AUDIT.md). The present request required two hours of primary-paper research, followed by four hours of writing and refinement. Completion of the earlier study does not satisfy these additional hours.

## Order and time accounting

The revision was initialized at 2026-10-21 16:36:34 UTC. The recorded research intervals reached 7,200 credited seconds at 20:12:26 UTC. Writing began at 20:12:59 UTC. The private ledger separates active research and authorial refinement from setup, publication, tool waits, interruptions, source handling and uncertain attention. Parallel assistance is never added to the root duration. The elapsed calendar window is longer than the credited work, and the records are an accounting trail rather than an independent measurement of attention.

The recorded writing total reached 14,400 credited seconds at 2026-10-22 06:09:45 UTC, giving 21,600 credited seconds across the two phases. The separate time audit checks interval arithmetic, ordering and evidence links; it does not independently measure second-by-second attention. Source checks undertaken to correct prose during writing receive at most one credit in that writing phase; they are not counted again toward the completed research phase.

## What the close reading changed

Wisniewski, Lindsay and Lindsay's 2020 study and the associated thesis already apply nearest-neighbor and conformal variants to signed endpoints on the same source. This revision therefore makes no claim to introducing those methods to the data. Its different response is the largest absolute sampled position over the current and next H records. The known current floor, multi-record label completion and potential dependence from overlapping outcomes are consequences of that response change.

The manuscript's [source evidence map](notes/revision-20261021/paper-evidence-map.md) records fourteen reference entries, including the dataset. The [method companion](notes/revision-20261021/method-transfer-comparison.md) maps nine method and evaluation works; CAViaR and SPCI also occur in the manuscript, leaving seven other mapped neighbors. The [financial-target note](notes/revision-20261021/direction-endpoint-peak-comparison.md) distinguishes flow direction, signed endpoints and sampled peaks. These counts are not claims to nine additional fitted benchmarks, fourteen distinct papers, a new work on every reread, or an exhaustive priority search. The linked notes identify exact consulted editions and separate all-text reading from selected passages and unaudited material.

The synthesis separates historical membership, response transformation, fitted conditional models, calibration and active intervention. Label completion follows the chosen response: a recursion driven by peak news may need completed H-record outcomes even when earlier forecasts and one-record transitions are already known. Raw reanchoring is not a fitted volatility filter. An order-statistic construction bound does not establish forecast accuracy. A chronological split does not establish exchangeability, independence or live release availability. Unimplemented calibration and delayed-aggregation illustrations spell out the additional assumptions; they provide neither forecasts nor empirical results for this source.

Three routes were compared: sharpen the original study, add a small conditional-selection comparison, or obtain independent inventory validation. The selected extension tests fixed-count membership based on one signed starting position. No equivalent independent dealer record was verified; price returns and weekly positioning reports were not relabeled as one.

## Design history and retained findings

The extension [protocol](protocol/revision-20261021-exploratory-protocol.md) and [machine specification](protocol/revision-20261021-exploratory-spec.json) were publicly recorded before execution, in commits `63703b911ee165a6057b0e80c36fd39c72cbcc4a` and `69d5bb67c6ca1e3c1509e29c14400462ce2a1130`. Its accepted calculation began at 2026-10-21 20:43:44 UTC. The evaluation interval had already been inspected in the original study; the freeze constrained later choices but did not create an unseen holdout.

The extension reports thirty summary rows, ten geometry rows, twenty-two comparison rows and twenty-six monthly rows. It evaluates three representations on five historical sets at H=6 and 24, using 6,625 common origins: F pools historical headrooms, S reanchors raw increment envelopes, and K takes native peak quantiles subject to the known current floor. K is the original L rule, relabeled. The complete menu, eligibility, tie rule and primary contrast were fixed before the added outcomes.

The original H=6 F-minus-S mean remains −USD 9,374.86, or −2.08% of S loss, with more breaches and greater mean positive overrun. H=24 reverses the ordering. The added primary nearest360 K-minus-recent360 K mean is −USD 277,704.47, or −31.83% of the weaker recent360 K reference. No added configuration beats the better original full720 F/S rule at its horizon. The narrower exception that H=6 nearest360 S improves its own full720 S is retained.

The .95 pinball score weights a dollar of underprediction nineteen times as heavily as a dollar of overprediction; that preference is stipulated, not an observed cost ratio. All twelve fixed nearest-minus-recent score differences are negative, but they share outcomes and histories. The matched S comparisons have more breaches and greater mean positive overrun. The matched F comparisons and primary K have larger conditional overrun means on different breach sets. January 2016 is adverse for the primary K contrast at both horizons. Reducing the nearest count from 360 to 180 reduces the mean absolute F/S report gap while increasing both methods' mean losses at both horizons. That sensitivity concerns these F/S rows; it is neither a universal rule nor a statement that every K loss worsens.

The evidence has three distinct scopes:

| Statement | Evidence and interpretation |
|---|---|
| Common-set reports satisfy elementary anchor-distance bounds | Appendix A gives finite-array arguments for the same paired rows and rank, in real arithmetic. This is a construction statement, not a future-law or coverage result. |
| Nearest retrieval lowers the declared score relative to equal-count recent retrieval | The accepted [paired comparisons](results/revision-20261021/comparisons.csv) record the realized differences. They do not isolate proximity from the other membership changes or establish superiority to the original leaders. |
| A smaller nearest count gives a smaller mean absolute F/S gap but larger F/S losses | The fixed [geometry](results/revision-20261021/geometry.csv) and [summary](results/revision-20261021/summary.csv) rows support this record-specific sensitivity. K is not included in that worsening claim. |

The empirical findings describe comparisons on the realized record. The four original resampling ranges remain descriptive, and no uncertainty analysis is attached to the added nearest-state contrasts. Neither construction agreement nor a lower chosen score establishes uniform risk reduction, population superiority or a policy benefit. The common issue origins align evaluation dates; changing H still changes both the future response and which historical origins have completed. A cross-horizon contrast therefore does not isolate the maximum operator alone.

## Resource use and reproducibility

The extension recorded 10.307238 seconds internally, sampled peak process RSS 64,602,112 bytes and one observed thread over 675 snapshots. A separate completed-process measurement reported 10.35 seconds and 64,634,880 bytes. It reused the accepted 1,286,391-byte source CSV and made no download. These are measured scopes; snapshots are not a continuous hard resource limit. The [result package](results/revision-20261021/README.md) retains the full aggregates and accepted manifest.

The seventeen-page [paper](manuscript/working-paper/paper.pdf), [TeX source](manuscript/working-paper/main.tex), structured content and approved vector figures are delivered together. The TeX source compiled successfully. The supplied PDF is independently typeset from the shared content and assets, rather than exported by that TeX compiler. Content and rendering checks establish document consistency, not scientific superiority.

The earlier combined suite passed 173 tests. A later correction made the figure subprocess use the active interpreter, after which its twelve existing targeted tests passed. These are distinct validations; the later check is not another full-suite run. The extension has one accepted calculation; subsequent document revisions reuse its recorded aggregates.

Scoped cleanup removed 510 explicitly listed, consumed scratch files, totaling 123,432,867 apparent bytes. The designated protected baseline, source fingerprints and reading copies, accepted results, current manuscript and required evidence passed preservation checks. No other research directory was cleaned, and physical disk-space recovery was not measured.

## Publication boundary and scientific limits

Publication identity is established separately by the immutable commit and changed-file raw bytes, with unchanged-file history and the resulting public-tree inventory defining verification coverage. A source compilation, a local PDF inspection and a remote-byte check are different pieces of evidence. The accompanying completion report identifies the actual final commit; this document does not use a self-referential commit hash as proof of its own publication.

The public package contains original code, permitted aggregates, source fingerprints and acquisition instructions. Raw observations, third-party paper PDFs, origin-level traces and private operational records remain excluded. The source's observed rights label does not establish raw redistribution permission.

The defensible contribution is a bounded application comparison and reproducible construction-sensitivity study. It introduces neither a new quantile estimator nor nearest neighbors to the financial source. A stronger fitted same-target conditional comparison, independent dealer evaluation and applicable uncertainty analysis remain absent. The scalar record does not identify a complete hedged book, gross currency exposure, funding cash, profit or intervention effects. Work-time completion and artifact verification do not certify journal competitiveness or acceptance.
