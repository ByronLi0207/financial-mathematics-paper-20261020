# Exact Supplement references for the v10b main article

Native Tectonic development compile: `.scratch/v10b/supp-dev/supplement.pdf`, 32 pages. Section numbering S1–S34 and the existing table counter through S46 are preserved; the two Murphy figures are now Figures S1–S2. Use fixed Supplement section/table/figure numbers in the separate main document. A main-document `\ref` or `\hyperref` cannot resolve these labels without external auxiliary-file machinery.

Main-article lines may move during concurrent editing; the quoted text identifies the intended occurrence. The original `main.tex` only inputs `manuscript.tex`. All prose occurrences of Supplement/Supplementary in that source and the main MCS generated note were reviewed.

| Main passage or purpose | Exact replacement reference | Supplement source label / evidence |
|---|---|---|
| “The Supplement proves both statements” (known floor and endpoint bound) | Supplement Sections S1–S2; simulations in Sections S3–S5 | `sup:floor`, `sup:levy`, `sup:simulation-original`, `sup:simulation-primary`, `sup:simulation-secondary` |
| “The Supplement lists every selected code and exclusion reason” (CFTC) | Supplement Section S30 lists selected codes and eligibility rules | `sup:v10-cftc`; the selected-universe longtable has no printed caption. Prefer “selected codes and eligibility rules”: the printed supplement does not enumerate an individual rejection reason for every excluded code. The S30 screening paragraph now links `revision-v10b/results/v10/cftc/eligibility.json` with label "complete code-level eligibility and exclusions", so the main article can accurately say that complete code-level exclusions are linked there. |
| “The Supplement lists complete results and numerical or structural failures” (benchmark paragraph) | Supplement Sections S7 and S11–S18, with retained extended results linked in Section S34 | `sup:ar`, `sup:panel` through `sup:wp3`, `sup:reproduction`. Some legacy filtered-path, forest and tail details are linked through archives, rather than all printed here; avoid implying all legacy benchmark tables are printed in the PDF. |
| Local-quantile row in the method table | Supplement Sections S8 and S23 | `sup:rank`, `sup:implementation` |
| Further-benchmark row in the method table | Supplement Sections S7 and S34 | AR recursion/results are in S7; longer legacy benchmark records route through S34. |
| “Quantile and normalization conventions are detailed in the Supplement” (method table note) | Supplement Sections S8 and S23 | `sup:rank`, `sup:implementation` |
| “The Supplement records comparison families, execution chronology and complete failure inventories” | Supplement Sections S14–S17, S19, S23 and S29–S34 | Retain scientific freeze/selection/acquisition chronology in these sections. Administrative audit/run records route through the explicit v10b link in S34. |
| State, target-level and full-prefix results | Supplement Sections S20–S21 and S26; Tables S19–S21 and S25–S26 | `sup:wp4`, `sup:wp5`, `sup:v8-backcast`, `tab:v8-backcast`, `tab:v8-backcast-complete`. Target-level table is S21; the state result/reference tables are S19–S20. |
| Weekly combination and headroom-recursion results | Supplement Sections S16–S18; Tables S14–S17 | `sup:wp2`, `sup:wp2-pairs`, `sup:wp3` |
| Panel and one-standard-error selection results in main table note | Supplement Sections S11–S15; Tables S9–S13 | `sup:panel`, `sup:panel-second`, `sup:panel-levy`, `sup:selection`, `sup:selection-failures` |
| “Every set, method p-value, equivalence class and prior unavailable method appears in the Supplement” | Supplement Section S31, Tables S35–S44 and its complete method legend | `sup:v10-mcs`; S35–S44 are the visible membership/p-value blocks; the complete method/classification legend is uncaptioned. Loss-class superscripts and NA/dash distinctions are retained. |
| “Supplementary Murphy diagrams” | Supplement Figures S1–S2 in Section S33 | `fig:murphyfx`, `fig:murphybill`, `sup:v10-diagnostics` |
| “the Supplementary diagnostics” | Supplement Table S46 in Section S33 | `sup:old-diagnostics`, `sup:v10-diagnostics` |
| Earlier calibrated simulations and stability grids | Supplement Sections S27–S28, Tables S27–S32 | `sup:v9-legacy-mc`, `sup:v9-stability`, `tab:v9-legacy-mc`, `tab:v9-legacy-failures`, `tab:v9-stability-diagnostics`, `tab:v9-stability-w52`, `tab:v9-stability-w260`, `tab:v9-stability-f` |
| Paired-menu full inventory (if needed near the new mechanism result) | Supplement Section S29 and Table S33 | `sup:v10-menu`, `tab:v10-menu-full`. Table S33 spans two pages; the generated continuation currently repeats its label, but its printed number is stable. |
| “The Supplement and zipped table retain all methods and coefficient combinations” | Supplement Section S32 and its linked full cost grid | `sup:v10-cost`; exact formula, native units, positive matched-F scale, beta/b relation, 7×9×3 coefficients, fixed primary method, complete rows and missing-floor matching are all present. |
| Main MCS table generated note: “The Supplement retains every set, p-value, loss class, secondary membership measure and availability record” | Supplement Section S31, Tables S35–S44 and its complete method legend | `sup:v10-mcs` |

The earlier controlled Monte Carlo numerical grids in S24 are explicitly linked to v9 Tables S26–S27 rather than reprinted. Preference frontier S10 similarly links v9 Tables S9–S10; the article must keep the version qualifier if referring to those historical table numbers. The current supplement's Table S26 is the full-prefix backcast, not the controlled Monte Carlo grid.

Complete current section/page and label/number mappings are machine-readable in `supplement-check.json`. Page numbers are development-pagination evidence; section/table/figure numbers are the publication cross-reference targets.

Counter caution: the uncaptioned CFTC universe and complete MCS method legend consume table counters S34 and S45 internally but do not display those numbers. Cite their section and description. No new caption was injected into either generated scientific display.

Post-development-compile edit: one public eligibility-record link was added to S30 at the root editor's request. The native 32-page development PDF precedes that URL-only addition; the root final native build will verify the final pagination.

Readable-header follow-up preserves all section, figure and table numbers and labels. Table S33 continuation duplication was repaired by the generated-table editor; no mapping change follows.
