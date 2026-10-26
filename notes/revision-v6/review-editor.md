# WP1 — Internal editor self-review

**Status: internal self-review by the project assistant. This is not an external editor report, an external peer review, a journal decision, or independent scientific validation. No Claude/Cloud review was invoked.**

Reviewed on 23 October 2026, branch `revision-v4-jof`. Scope: current `submission-jof/` manuscript, supplement, title page, cover letter, author checklist and package README; v5 contribution/positioning source and evidence records; the authorized v6 plan. Other WP1 reviewer files were not consulted. No scientific source, code, experiment or manuscript was changed during this review. Line locators below refer to this inspected source snapshot and must be refreshed after integration.

## Editorial assessment and verified journal context

The paper has a plausible Journal of Forecasting application/evaluation fit: it studies a clearly defined forecast functional, compares mature procedures, and preserves failures and unfavorable results. Its strongest editorial story is the contrast between a favorable inspected FX score comparison and adverse separately fitted aggregate-task results, with explicit information timing and measurement boundaries. The present title, abstract and contribution paragraphs distribute attention across too many secondary findings before that story is established. These are concerns about evidence hierarchy, interpretation and reader navigation; they do not establish that any reported numerical result is wrong.

Fresh official-source checks support the following boundaries:

- The [official journal scope](https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/productinformation.html) describes a broad forecasting journal and emphasizes modelling and connections to decisions. The direct page request timed out; its current official-domain search result supplied the scope text. Fit here is an editorial inference, not a promise of review or acceptance.
- The [official Author Guidelines](https://onlinelibrary.wiley.com/page/journal/1099131x/homepage/forauthors.html), retrieved successfully in this review, allow consistent initial Free Format references, require a peer-review PDF alongside LaTeX and supporting sources, and request a brief informative title, fewer than 40 characters for the running title and up to six keywords. They state single-blind review and expect data sharing. No numerical body/abstract word limit or page cap was found in the inspected guidelines. The project's 9,000-word/six-table/four-figure budget is a working constraint, not a verified journal limit.

Mature editorial practice for this task is to declare the target and primary comparisons first, separate descriptive accuracy from calibration tests and decision value, compare credible alternatives on the same information clock, give the reader usable cross-references, and distinguish frozen retrospective evidence from genuinely new validation. The manuscript already implements many of these practices; the issues below identify where presentation or the remaining menu weakens them.

## Issues and proposed disposition

### E01 — Major: the title/abstract/contribution hierarchy obscures the primary empirical question

**Passages/routes:** `submission-jof/manuscript.tex:12–16`, `:34–38`; `title-page.tex:7`; `cover-letter.md:3–5`. The abstract foregrounds three elementary construction properties, then the **matched** FX loss reduction of 14.77%, original-primary elementary-score crossing, W720 horizon crossing, Treasury +50.79%, a 3/48 panel count and an invalid-label experiment. It does not report the original FX primary's 12.66% reduction, although that primary anchors RQ1. The current title gives the classical bound and the floor the same prominence as the empirical forecasting question.

**Why it matters:** The numbers are explicitly distinguished in the text, but a new reader must reconstruct which result answers which question. A title about construction bounds can also set an expectation of a principal theoretical advance that the paper correctly disclaims.

**Disposition: NOW, with final synchronization in WP6–7.** Keep the application/model-validation contribution and both original primaries as the main contract. Lead the abstract with the target, comparison design and two original-primary outcomes; give the matched-history FX contrast as a clearly labeled control. Retain one concise qualification on retrospective inspection/vintage and one on absent prospective/unseen-dealer validation. Leave the timing oracle and detailed crossing/panel counts in the supplement unless new WP results materially change the conclusion. Consider the already recorded question-led title; author confirmation of the final title remains in `AUTHOR-TODO.md`. No priority claim or numerical outcome should be upgraded.

### E02 — Major: the benchmark menu remains incomplete at exactly the points the positioning discussion makes salient

**Passages/routes:** `manuscript.tex:63–71`, `:345`, `:360`; `supplement.tex:1111`. The closest endpoint lineage is conformal, CAViaR is named as a relevant mature alternative, and the conclusion still lists these as future work. Fixed forecast combinations are absent from the executed main menu.

**Why it matters:** An application paper can use established methods, but its conclusions about the comparative value of conditional reports are harder to interpret when a directly adjacent calibration method and simple combinations have not been evaluated. The existing text honestly limits the menu; this is a substantive evidence gap rather than a citation omission.

**Disposition: WP2–3.** Execute the predeclared ACI, SAV-CAViaR and fixed-combination comparisons on the original mature-label clock and retain failures. Update the method overview, complete supplement results, cover letter and the remaining-alternatives sentence only after actual outputs exist. ACI-CAViaR evidence must remain exploratory; it does not replace the original primaries or establish a universal winner. If a method is NA, retain that explicit limitation instead of saying it was successfully benchmarked.

### E03 — Major: matched-history score claims route to original-primary score diagrams

**Passages/routes:** `manuscript.tex:36` gives the matched-history 14.77%, 376/360 and Holm result with the route “Tables 3–4 and Figures 3–4.” However, Figure 3 (`:293`) and Figure 4 (`:298`) are explicitly **original-primary** diagrams. Table 6 (`:327`) likewise places long-history matched QR/KNN score evidence next to “crossed score curves … Figure 3.” Supplement Table S24 (`supplement.tex:618–625`) confirms that the full-breakpoint audit is for the two original primaries.

**Why it matters:** The source says “distinct original primary,” but the route still permits a reader to attach the crossing finding to the matched pair or KNN. Crossing has not been established for those other pairs by the cited diagrams. This is a comparison-attribution problem, not a demonstrated numerical error.

**Disposition: NOW.** Split the contribution paragraph into separately routed claims: matched-history score and hit counts → Tables 3–4; original-primary score-class sensitivity → Figure 3/Table S24; Treasury original-primary sensitivity → Figure 4. Qualify the Table 6 caution explicitly as the **original-primary QR comparison**. Do not silently generalize the diagrams to matched controls or KNN; a new diagram would need its own authorized analysis/binding.

### E04 — Major: increased hit frequency must remain distinct from demonstrated calibration deterioration

**Passages/routes:** title `manuscript.tex:12`, abstract `:16`, contribution `:36`, discussion `:282–288`; Table 4 (`:270–272`) shows FX H6 QR POF p=0.695 and DQ p=0.736, while rolling and matched F have DQ p=0.00798 and p=0.0407. The title's “Score–Coverage Disagreement” and repeated “more breaches” can be read more strongly than this evidence warrants.

**Why it matters:** More observed breaches is an exact descriptive statement; it does not by itself show worse conditional calibration or a conflict between a proper score and a coverage theorem. The paper already explains this correctly in Sections 4, 7 and 9. The high-visibility framing should preserve the same distinction, especially because the diagnostics do not uniformly favor F.

**Disposition: NOW + WP2.** Prefer “score and breach-frequency trade-offs” where the evidence is only descriptive; retain calibration as a separate diagnostic object. Add one clear statement near the headline example that more breaches alone do not establish calibration deterioration. WP2 should then answer the genuinely new question of whether the score ranking persists after online calibration. Keep nonrejection qualified; it is not proof of correct calibration.

### E05 — Major: the decision map lacks evidence on issue-known states and quantile-level sensitivity

**Passages/routes:** `manuscript.tex:316–330`, especially “Use frequency, history and the measurement definition to frame validation comparisons”; `:339–351`. Current Table 6 organizes findings mainly by source/history, and the main analysis fixes the .95 quantile. The text correctly avoids causal frequency and switching-policy claims.

**Why it matters:** Readers looking for guidance on when the fitted procedure helps can presently identify archive settings, but cannot infer an issue-known state rule or robustness across tail preferences. These limitations constrain the practical contribution even after the forecasting functional is clearly stated.

**Disposition: WP4–5, then explicit limitation.** Add only the predeclared known-at-issue volatility groups, conditional predictive-ability calculation and .90/.99 fits. Update the map if those outputs support a state or quantile distinction, including null results and direction reversals. Retain the sentences that the analysis does not identify a causal frequency effect, a deployable switch, independent dealers, or prospective calibration. These work packages cannot repair the absent unseen-dealer/prospective validation.

### E06 — Minor: the evaluation sample and refit budget are too remote from the core design

**Passages/routes:** `manuscript.tex:78–86`, `:112–115`, `:187–189`; `supplement.tex:1142–1149` (Table S36). Main text gives exact boundary dates and an algebraic refit rule, but the concise source-specific validation/evaluation counts, W values and cadence are relegated to the last supplement section. Several early results use 6,625 or 277 origins before that budget has been presented together.

**Why it matters:** These are the basic denominators and learning schedules needed to understand the primary comparison, not merely reproduction internals.

**Disposition: NOW.** Add one compact design sentence or source-budget panel using existing S36 values: FX validation/evaluation 1,440/6,625 and refit d=24; Treasury 52/277 and d=13, with the existing W values. Explain H as source-record transitions and keep sparse-grid counts separate. Reuse existing output values; no new calculation is needed.

### E07 — Minor: main-table numbering is out of reading order

**Passages/routes:** Table 3 at `manuscript.tex:207`, Table 5 at `:223`, Table 4 at `:264`, Table 6 at `:321`. Physical source order is 1, 2, 3, 5, 4, 6.

**Why it matters:** The bridge was integrated after numbering was settled. Hard-coded table numbers make a correct route harder to follow and increase the risk of a partial renumbering during WP6.

**Disposition: NOW / WP7 cross-reference check.** Either move the bridge after the coverage table or renumber the bridge and coverage tables in order of first appearance. Update every main, supplement, caption and decision-map reference together, including `supplement.tex:1175`. Confirm the rendered order after the rebuild; do not change archival table numbers in original result records.

### E08 — Minor: repeated qualifications and archival detail displace the main forecast narrative

**Passages/routes:** duplicate section/subsection heading at `manuscript.tex:181–182`; intercept/normalization explanation repeated at `:134` and `:142`; finite-menu floor qualification repeated at `:286` and `:288`; selected-fit shrinkage internals at `:347`. Recorded v5 metrics are 6,721 main prose words, six tables and four figures, plus 8,313 supplement prose words/37 tables; these are recorded metrics, not a new formal-TeX page measurement.

**Why it matters:** There is no verified journal cap breach. The concern is cognitive load: the main result is repeatedly interrupted by extensive historical and numerical qualifications, while the supplement also starts by replaying a substantial article-like narrative.

**Disposition: NOW / WP6–7.** Remove literal duplication, merge adjacent statements with the same meaning, and keep detailed selected-fit/numerical history in its existing supplement route. Preserve qualifications once at the relevant claim and in a focused limitations paragraph. Put WP2–5 full outputs in the planned supplement section; mention a new result in the main text only when it materially changes the conclusion. Recount the project's stated word/table/figure budget after integration without relabeling that budget a JoF rule.

### E09 — Minor: the supplement contains machine pointers and revision labels that are weak reader-facing locators

**Passages/routes:** `supplement.tex:1139` (“S15. V5 post-result analyses…”), `:1205` includes `THIS_STUDY, ['sections', 3, 'blocks', 2]` and `sections[7].blocks[5]`; `:1207` routes source IDs generally to a repository register. Compare the readable article locators elsewhere in the same subsection.

**Why it matters:** These are useful audit bindings, but a journal reader cannot reliably navigate a printed paper using JSON offsets or an unnamed repository log. Revision labels also make the supplement look like an internal project history instead of a stable research document.

**Disposition: NOW / WP7.** Replace printed JSON offsets with current article section/proposition/table locators. Give the source register a specific repository-relative path or stable link, retaining machine pointers there for audit. Rename S15 by its analytical contents, retaining the post-result label and the original evidence files. Use consistent capitalization for “AR,” “FHS,” “POT” and supplement headings.

### E10 — Minor: bibliography inclusion and citation routing are not fully consistent

**Passages/routes:** `manuscript.tex:434` lists Sussman (2023), Proposition 3.4, but no author–date invocation appears in the manuscript or supplement; the Lévy result is named at `:160–165` without a linked source invocation. `submission-jof/README.md` says each document displays only its own cited references. The main reference list also puts Lindsay (`:390`) before Diebold (`:392`), interrupting author order. `AUTHOR-TODO.md:11` explicitly retains unresolved metadata checks.

**Why it matters:** The present package does not yet fulfill its own one-to-one citation claim. This review does not certify all reference metadata and does not infer that the listed end pages or names are wrong.

**Disposition: NOW / WP7.** If Sussman is the consulted source for the classical inequality, add the appropriate author–date/proposition citation where it supports that statement; otherwise remove the uncited entry from that document while retaining the source register. Sort and format consistently, and perform a cited-work ↔ displayed-entry audit separately for the main and standalone supplement. Verify the explicitly pending fields against primary metadata before clearing the author checklist. Initial Free Format flexibility is not a reason to claim an audit that has not been completed.

### E11 — Minor: availability wording blurs access restrictions with local trace handling

**Passages/routes:** `manuscript.tex:363–365`; `supplement.tex:606–611`; `cover-letter.md:9`; `AUTHOR-TODO.md:9`. The public Kaggle acquisition route and non-assumed redistribution rights are stated, followed by “Private raw FX observations and private per-origin forecast traces are not redistributed.” The supplement says accepted forecasts are preserved but origin-level traces remain private.

**Why it matters:** A reader may interpret “private raw FX observations” as a nonpublic proprietary input rather than a locally held copy of a source with stated third-party rights. They also need to distinguish publicly archived aggregates from regenerable local forecasts and unavailable original dealer books.

**Disposition: NOW, retaining the explicit data limitation.** Describe the actual access route and redistribution boundary of raw inputs, then separately state whether origin-level traces are obtainable or must be regenerated and point to the exact reproduction instructions. Do not imply redistribution permission, independent audit, permanent anonymous access, or access to original dealer books. Preserve the actual source/vintage limitations and the author's permission check.

### E12 — Major for submission readiness: preview PDFs and personal declarations are still preparatory artifacts

**Passages/routes:** `submission-jof/README.md` states that all preview PDFs were independently typeset with ReportLab and source compilation returned diagnostics rather than an exported TeX PDF; `AUTHOR-TODO.md:8` requires formal output and page review. `title-page.tex:8–14`, `manuscript.tex:367–373` and `cover-letter.md:11–14` retain author/disclosure placeholders.

**Why it matters:** A successful diagnostic compile and a separately generated preview do not establish that the peer-review PDF is the actual output of the submitted sources. Author identity, approval and declarations cannot be inferred from the scientific package. These are explicit current boundaries, not evidence that the underlying source fails to compile or that declarations were omitted dishonestly.

**Disposition: explicit submission limitation / AUTHOR-TODO; technical artifact checks in WP7.** Bind the final sources, figures and package to the formal TeX-generated peer-review PDF and inspect it after final integration. Keep preview provenance explicit until that exists. Leave personal fields for the author, and do not make a journal submission, approval or disclosure on their behalf. An internal v6 completion report should distinguish completed preparation from submission readiness.

## Disposition ledger

| ID | Severity | Primary route | Completion evidence required |
|---|---|---|---|
| E01 | major | now; synchronize WP6–7 | abstract/title/contributions and cover letter express one comparison hierarchy |
| E02 | major | WP2–3 | complete fixed-menu outputs, failures and revised remaining-work sentence |
| E03 | major | now | each score-diagram claim names its actual pair and routes to its own caption/audit |
| E04 | major | now + WP2 | breach-frequency wording kept separate from calibration inference; actual ACI outcomes |
| E05 | major | WP4–5 + limitation | complete planned state/quantile outputs and bounded decision-map update |
| E06 | minor | now | original sample/refit budget readable beside design |
| E07 | minor | now / WP7 | sequential displayed numbering and consistent cross-document routes |
| E08 | minor | now / WP6–7 | redundancy reduced; project metrics refreshed without invented JoF cap |
| E09 | minor | now / WP7 | readable printed locators and specifically linked audit register |
| E10 | minor | now / WP7 | per-document citation audit and retained unresolved metadata boundaries |
| E11 | minor | now + limitation | source access and trace regeneration/availability stated separately |
| E12 | major | WP7 + author-controlled limitation | actual final-source PDF binding; personal declarations remain author actions |

**Count: 12 issues, 6 major and 6 minor.** These are proposed dispositions for the integrating agent; this reviewer did not execute them. The absent compatible unseen-dealer sample, unexecuted prospective protocol, source-vintage limitations and missing decision-cost mapping remain explicit scientific limitations after WP2–5.

## Inspected-source fingerprints

```text
902de0569b6e2ec9aff225f33941f02b0194c4cfbfc079bf634d04d3eb91f873  submission-jof/manuscript.tex
656e87821d822fdaec9b9ef10ead6590e83f83348afc9d1058cef50abf0e0d89  submission-jof/supplement.tex
fa0990c364597a4b22cbf6b3e6cc92b525b2743c76712731dff85b55bc34083e  submission-jof/title-page.tex
566cb41ab8405617666d000bb53bd6c76e953e7a9e251e91faa3b256232a0465  submission-jof/cover-letter.md
97fb9ac619b1e51e220f6668ec83dd470b99fd949cecec6d075640cff99b079c  submission-jof/AUTHOR-TODO.md
93067bde6be00cc1eee2b654630a6aa3df43be52fb2dbfc3dddd08cee2f5c8d9  notes/revision-v5-novelty/contributions-proposal.md
bf4033ba651c8db57c56e4c32dca4ca8130cd7331f400efd629eedcb2e883508  notes/revision-v5-novelty/positioning-source.json
```

Memory was used only for orientation and the instruction to reopen current sources, not as evidence for present scientific findings. Current findings above come from the inspected sources and fresh official guidance. No tests, experiments, compilation or independent statistical validation were performed by this editor self-review.
