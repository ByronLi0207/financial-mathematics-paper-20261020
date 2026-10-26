# v12 editorial independent read-only check

Checked 2026-10-25 against the current main source and the generated low-frequency subsection after it arrived. Supporting reads used only existing public F1/F2/F3/M2 result files, source/number bindings, generated tables, cover letter, title page and editorial notes. No manuscript/core edit, experiment, accuracy evaluation, statistical/test run, Git operation, Claude or cross-model review occurred. Only this note is written. A separate rendered-page inspection follows this source audit.

## Outcome

No remaining scientific contradiction was found in the current F1/F2/F3 statements or the three-finding narrative. Several concrete wording concerns were sent to the root during review and were corrected by the source owner before this final snapshot:

1. The default quantile now begins “Unless otherwise stated,” avoiding a literal conflict with the .90/.99 sensitivity checks.
2. The 52-origin validation sentence now specifies “Original weekly comparisons,” avoiding a conflict with the156-week arm.
3. The new decomposition paragraph explicitly names full regression for the41/29/27 primary counts, defines the selected-report-versus-best-finite and best-finite-versus-history differences, and excludes the ordinary empirical option from the finite oracle.
4. The tau.99 paragraph now states28/34 CFTC wins and the one failure that leaves the29-win threshold unresolved, while both required FX comparisons remain unavailable.
5. Both long-history FX horizons' negative finite-menu gaps are now acknowledged, without claiming information is absent from all other conditional models.

The root's corrections resolve the initial P2 concerns about primary-method ambiguity and undefined decomposition components. They also make the missing-data outcome understandable rather than presenting only an internal status label.

## Saved result consistency

| Comparison | Saved evidence and present interpretation |
|---|---|
| F1 primary finite-menu gap |29/41 W52 weekly cells, all41 complete, positive gap; SUPPORTED. This is a majority finite-menu result for full regression, not every cell or every possible conditional model. |
| F1 primary selection component |27/41 satisfy E>0 and S>E/2; SUPPORTED. Nonpositive actual excess remains nonsupport; negative selection is retained. |
| F1 component medians | Actual19.44%, selection18.32%, gap4.37% after rounding. The text expressly says separate component medians need not add. |
| F1 FX check | Original W2880 H6 gap -14.917351765503492%, H24 -3.7577697957958254%; both negative and complete. Current text acknowledges both. |
| F2 W52 | QR33 median19.33471575756462% to4.030683382999826%; infinity4/17 to10/17; all17 primary pairs complete. |
| F2 W260 | QR33 median10.348281789464425% to0.5250886760200655%; infinity4/17 to5/17; all17 primary pairs complete. |
| F2 interpretation | Both primary windows support V1/V2. The text correctly describes differences between across-contract medians, not a typical paired contract improvement or causal effect; secondary four-feature failures remain unavailable. |
| F3 tau.99 CFTC |28 wins,5 completed nonsupports (including4 ties),1 failed/unknown; support fraction bounds28/34..29/34; UNDETERMINED. |
| F3 tau.99 FX | Both required period rows are FAILED; Q2 remains UNDETERMINED. No tau.90 result is substituted. |
| F3 table | Incomplete W260 CFTC tau.99 displays NA rather than its successful-subset median86.51422565201239%; both FX tau.99 entries display NA. Complete tau.90 and short-history tau.99 values match the saved full-group rows. |
| M2 | Constant median0.2069371499562489%, switching -0.22777914491914353%, difference -0.43471629487539243pp versus a+5pp criterion. The current “no observed median loss” statement is descriptive and limited to that short-history/calibrated comparison. It does not assert population equivalence or no switching loss in every source. |

The abstract/introduction/conclusion/cover letter retain the same three findings: reference-dependent matched FX gains; competitive weekly historical benchmarks with both finite-menu and selection limitations; and preference-dependent CFTC limit-cost rankings. New finite-menu and validation results enrich the second finding without creating an additional unsupported headline. Higher-quantile numerical failures are not recast as confirmation.

The paper-number binding file was read independently: all source SHA-256 values,54 bound JSON values/operands, and the generated TeX output hash agree. The five-penalty cardinality binding is an explicit count of the five declared identities, not an evaluation-outcome calculation. No scientific summary was rebuilt.

## F4 eleven-item application checklist

| Item | Current source evidence / remaining verification |
|---|---|
|1 Data table | Five source rows present, metadata plus nine statistics; USD millions and heterogeneous CFTC contract units distinguished; matched complete H6 sample and separate within-series medians explicit. Table numbering, readability and fit are checked in the separate rendered pass. |
|2 Method formulas | Historical corrected rank and saturation, training-scaled ridge objective with unpenalized intercept and six-point menu, and DM/Newey–West statistic are present. |
|3 Low-frequency section | Integrated after RQ2/MCS; F1 signed decomposition, F2 and tau results joined with the old simulation finding. Primary procedure and finite-oracle definition are now clear. The1.5-page limit needs the rendered-page check. |
|4 Reader language | Main T1–T3 labels, frozen-threshold wording, “F or I,” mean-unused-allowance language and literal sole-membership wording are removed. Main method names are descriptive; mathematical F remains where requested for formulas. M2 qualifiers are retained. |
|5 Literature Table1 | Four-column/eight-row checked replacement is applied; no unverified/partial/input-byte disclaimer remains. `notes/v12/table1-check.md` records the primary-source retrieval performed by the literature subtask. This check verifies application, not a duplicate external-source review. |
|6 Propositions | Proposition1 has3 sentences and Proposition2 has4. Classical Lévy naming is retained without Sussman or an unverified textbook/page claim; proofs and qualifications point to the supplement. |
|7 Misplaced FX paragraph | The adverse+31.5%/924-versus427 case is under RQ1 and now explicitly limits generalization beyond the matched long-history result. |
|8 Limitations | Seven single-sentence items cover the required dealer/inspection, retrospective periods, related aggregate/survivor, vintage, causal/coverage, cost and post-result diagnostic boundaries. Old technical details are retained in S36 with an explicit historical qualifier around the previously untested-validation statement. The.6-page cap needs the rendered-page check. |
|9 Code availability | One clean revision-v12 link; version-history prose removed from the paragraph. |
|10 Connected prose | Most result paragraphs now connect facts with implications. The current low-frequency display record reports307 words/18 sentences, mean17.0556, maximum24 and zero>40. Global final writing metrics remain root-owned. |
|11 Length / relocation | Source compression and moved detail are present. The owning native-build record reports20/37 main/supplement pages; that receipt alone is not visual acceptance. The separate image pass checks current visible layout and section spans. |

## Nonblocking remaining prose opportunities

These suggestions identify exact sentences and their reasons; they are not factual defects or requests to change already frozen results.

* `manuscript.tex:254` — The paragraph ends with the worst conservative-selection case. A short interpretation such as “Thus conservative selection does not uniformly protect short weekly comparisons” would make its final implication explicit.
  Current sentence/paragraph: Stronger regularization narrows weekly panel losses but leaves historical rules ahead, with conservative selection choosing the intercept-only report in 17 of 26 earlier cells (Table~\ref{tab:weekly}). Its largest relative loss increase occurs in the Treasury-bill short-history, 24-step comparison, despite conservative selection.

* `manuscript.tex:326` — The paragraph correctly limits the weight reversal to its horizon/reference. It could close with “Score preferences therefore need to be reported with the horizon and reference procedure.”
  Current sentence/paragraph: Elementary-score rankings cross for both original main comparisons (Supplement Figures S1--S2, Section S33). A separate 24-step FX comparison against rolling translated paths reverses near 20.6:1. Both six-step FX comparisons reduce mean underprediction and mean overprediction, so the weight reversal belongs specifically to the 24-step reference.

* `manuscript.tex:342` — The three cost-grid counts are followed by a scope disclaimer. A brief implication such as “Changing reserve and breach prices can therefore alter a score-based ranking” would connect the numbers to the validation decision.
  Current sentence/paragraph: At $c=1$, regression is strictly cheaper in $5/34$ comparisons at the center of the sorted grid $(\kappa,\beta)=(.1,.25)$, $32/34$ at $(1,0)$, and $1/34$ at the opposite corner $(.01,5)$.

* `manuscript.tex:355` — The final36.5% adverse fact could be connected to implementation: “The empirical rank convention therefore also matters when implementing the historical benchmark.”
  Current sentence/paragraph: \textbf{Use historical headroom by default when validation evidence is short.} Expanded penalties and longer validation reduce losses, but short-sample selection, including one-standard-error selection, still fails to protect the historical benchmark consistently. Historical reports also survive in most CFTC model confidence sets, supporting their retention until a conditional procedure has sufficient validation evidence. The ordinary empirical quantile is up to 36.5\% worse than corrected headroom in the earlier weekly grid.

The audit does not demand a new explanatory sentence after every transition or supplement cross-reference. The author can retain the current readable form if these additions would crowd the page budget.

## AI declaration and placeholders

The AI declaration is absent from current main/title/cover/supplement sources, consistent with the latest direct user instruction recorded in the edit log. Unfilled author information, ORCID, funding and competing-interests placeholders remain in the main; title-page author/affiliation/corresponding-contact/ORCID/funding/conflict placeholders and the cover signature remain unfilled. No personal details were inferred or inserted.

## Snapshot identity

The source changed during this audit as the root applied the above fixes; hashes below identify the final read snapshot. Later edits require targeted readback. This note makes no full-test, remote-publication or completed PDF visual-review claim.

| File | SHA-256 |
|---|---|
| `submission-v10/manuscript.tex` | `309ca6700d06cdc2cb1f8459e3d384463ec81d000cca7da3139e6be523326f3d` |
| `submission-v10/generated/v12-low-frequency.tex` | `ffe2a05bd4c553bb81aa7a68765fb594a49825325eadc88ec9650f0dbbcbf26c` |
| `results/v12/decomposition/predictions.json` | `551ec9f4ab05e38b28c436a7a2c765c095f29ac96a49c4fc6dd0ec18ba4977e4` |
| `results/v12/validation-length/predictions.json` | `03dc2326fb208f73c9b4a464f0e53799a8dee822af997861420d862d05f69520` |
| `results/v12/tau/predictions.json` | `a9adbb6d4e939df9ce596b7dbc2355b8c0a94435c9e65da01047a1723a23f654` |
| `results/v10/menu/summary.json` | `e1ac79325e2f8ef60ede05378c70dbbe5f2fedfdbe5ff021d2ec1e58826689d5` |
| `notes/v12/new-paper-number-bindings.json` | `1e61af23c2d04cbcea0e05c0dbd12caf1c653370ede2fabb0fd467cd88b7336c` |
