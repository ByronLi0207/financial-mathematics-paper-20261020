# English review — numbered Sections 1–9 and cover letter

Reviewed UTC: 2026-10-25T05:25:23.444557+00:00. Manuscript snapshot SHA-256: `d85a6a83209ce8b1c00b0c3d8c1b1ceee93f6a946792f2bd2168b776f3031a7e`. Cover-letter snapshot SHA-256: `0f0863a806b1342ed373f1ebf99f9224546d92f0afa054d5aa33548d780581bb`. Line numbers below refer to these snapshots; exact before-text anchors permit relocation while the parent continues editing.

Scope: numbered Sections 1–9 of the current manuscript and `cover-letter.tex`. The source currently has eleven numbered sections. The abstract, Section 10 (Limitations), Section 11 (Conclusion) and declarations were read only to check alignment and preserve boundaries; no replacements are proposed for Sections 10–11 or placeholders. References are excluded from this pass and have their own APA report. Only this review file was written. No manuscript, cover letter, reference, scientific number, result, data, protocol, source code, figure or Git state was modified; no Git command, experiment, score, summary, fit or Claude call was run.

The strongest direct language repairs are E01–E06. Other items are optional clarity/terminology recommendations. H02, H05–H07 and C02–C03 concern existing conclusion boundaries and should receive editorial judgment; they are deliberately distinguished from pure grammar. Applying all suggestions wholesale is not required and could create unnecessary prose churn.

## Specific before → after suggestions

### E01 — Pure language: logical comparison

Location: `submission-v10/manuscript.tex:195`.

**Before**

```latex
Its breach count remains slightly higher than wrapped historical headroom on common origins
```

**After**

```latex
Its breach count remains slightly higher than that of wrapped historical headroom on common origins
```

Reason: Compare a count with a count, rather than with a procedure. Direction and common-origin qualification remain unchanged.

### E02 — Pure language: missing verb

Location: `submission-v10/manuscript.tex:309`.

**Before**

```latex
These are descriptive fractions; all comparisons complete and the lower and upper fractions coincide.
```

**After**

```latex
These are descriptive fractions; all comparisons are complete, and the lower and upper fractions coincide.
```

Reason: The COMPLETE-status clause needs a finite verb. This preserves the equality of the lower and upper fractions.

### E03 — Pure language: frequency/interval terminology

Location: `submission-v10/manuscript.tex:132`.

**Before**

```latex
Refit frequency is thirteen records; histories are 52 and 260.
```

**After**

```latex
Refits occur every thirteen records; history lengths are 52 and 260.
```

Reason: A number of records is an interval. The cadence and both numerical history lengths remain identical.

### E04 — Pure language: loss referent

Location: `submission-v10/manuscript.tex:148`.

**Before**

```latex
Conservative selection favors the strongest shrinkage within one paired HAC standard error of the validation winner.
```

**After**

```latex
Conservative selection favors the strongest shrinkage whose validation loss is within one paired HAC standard error of the winner's loss.
```

Reason: The standard-error neighborhood applies to validation loss, rather than directly to a shrinkage parameter or procedure.

### E05 — Pure language: benchmark name

Location: `submission-v10/manuscript.tex:318`.

**Before**

```latex
Retain corrected-rank history as a matched benchmark in these comparisons.
```

**After**

```latex
Retain corrected-rank historical headroom as a matched benchmark in these comparisons.
```

Reason: Historical headroom is the F benchmark; history alone denotes the training window. This aligns the recommendation with the method definition.

### E06 — Pure language: idiomatic preposition

Location: `submission-v10/manuscript.tex:183`.

**Before**

```latex
it does not adjust earlier research-stage model development.
```

**After**

```latex
it does not account for earlier research-stage model development.
```

Reason: The nominal interpretation does not account for earlier model development. The inferential caution is unchanged.

### E07 — Pure language: physical referent

Location: `submission-v10/manuscript.tex:28`.

**Before**

```latex
A selected Treasury-bill path whose endpoint returns within the historical report after an intervening breach.
```

**After**

```latex
A selected Treasury-bill path that returns within the reported historical limit at its endpoint after an intervening breach.
```

Reason: A path returns within a limit, not within a report document. Within is retained, so no strict below-limit claim is introduced.

### E08 — Pure language: redundant crossing phrase

Location: `submission-v10/manuscript.tex:117`.

**Before**

```latex
Short-history FX regression crosses across horizons on 640 evaluation origins.
```

**After**

```latex
Short-history FX regression produces horizon crossings on 640 evaluation origins.
```

Reason: Removes crosses/across repetition while preserving the exact count and short-history scope.

### E09 — Pure language: first-use abbreviation

Location: `submission-v10/manuscript.tex:144`.

**Before**

```latex
The four-feature variant uses current magnitude, signed level and two increment RMS measures.
```

**After**

```latex
The four-feature variant uses current magnitude, signed level and two root mean square (RMS) measures of increments.
```

Reason: RMS is not expanded before this main-text occurrence. Expanding it once does not change the features or the number of measures.

### E10 — Pure language: time index

Location: `submission-v10/manuscript.tex:171`.

**Before**

```latex
At refit \(r\), training labels are eligible only when \(i+H\le r\).
```

**After**

```latex
At refit time \(r\), training labels are eligible only when \(i+H\le r\).
```

Reason: Adds the noun time to the refit index; the eligibility inequality stays untouched.

### E11 — Pure language: articles and fixed-control wording

Location: `submission-v10/manuscript.tex:173`.

**Before**

```latex
Matched comparisons fix completed-response history and refit schedule for regression and historical headroom.
```

**After**

```latex
Matched comparisons hold the completed-response history and refit schedule fixed for regression and historical headroom.
```

Reason: Uses standard hold fixed wording for the shared comparison controls.

### E12 — Pure language: label restoration

Location: `submission-v10/manuscript.tex:185`.

**Before**

```latex
Exact duplicate loss columns enter the bootstrap once and their procedure labels are unfolded afterward.
```

**After**

```latex
Exact duplicate loss columns enter the bootstrap once, and their procedure labels are restored afterward.
```

Reason: Restored is clearer than unfolded for reattached duplicate-procedure labels. The one-entry bootstrap treatment remains explicit.

### E13 — Pure language: noun-stack simplification

Location: `submission-v10/manuscript.tex:291`.

**Before**

```latex
Both whole thirteen-source summaries remain unavailable.
```

**After**

```latex
Both summaries across all thirteen sources remain unavailable.
```

Reason: Preserves complete-summary scope and unavailable status without implying a successful-subset substitute.

### E14 — Pure language: American-English spelling

Location: `submission-v10/manuscript.tex:305`.

**Before**

```latex
at the sorted-grid centre
```

**After**

```latex
at the center of the sorted grid
```

Reason: General prose predominantly uses American English (behavior, color, standardization). Preserve the adjacent numerical grid coordinates and counts exactly. Published titles with British spelling must stay source-faithful.

### E15 — Pure language: application and parallel nouns

Location: `submission-v10/manuscript.tex:80`.

**Before**

```latex
In CFTC, higher reserve and lower fixed breach charges generally favor regression, with local exceptions.
```

**After**

```latex
In the CFTC comparisons, higher reserve charges and lower fixed breach charges generally favor regression, with local exceptions.
```

Reason: Names the application rather than the agency as the setting, and makes reserve charges parallel with fixed breach charges. Keep generally and local exceptions.

### E16 — Pure language: missing final noun

Location: `submission-v10/manuscript.tex:31`.

**Before**

```latex
CFTC dealer-category futures.
```

**After**

```latex
CFTC dealer-category futures positions.
```

Reason: Makes the data unit clear: these are positions in futures markets. The source and exposure type remain unchanged.

### H01 — Existing-scope clarification

Location: `submission-v10/manuscript.tex:214`.

**Before**

```latex
The fixed-period learning curve shows that more history helps only over part of the tested range
```

**After**

```latex
The fixed-period, short-horizon learning curve shows that more history helps only over part of the tested range
```

Reason: The figure caption already limits the display to the short horizon. Carry that boundary into the opening sentence; do not generalize it to all horizons.

### H02 — Result-boundary wording; no result change

Location: `submission-v10/manuscript.tex:214`.

**Before**

```latex
Part of that gain reverses at the longest history, while the four-feature curve also changes sign.
```

**After**

```latex
The gain is smaller at the longest history, while the four-feature curve changes sign within the tested range.
```

Reason: Part of a gain reverses can be mistaken for a full-regression sign reversal. The replacement preserves the smaller longest-history gain and QR4 sign changes, without implying that QR4 changes sign at the longest history.

### H03 — Existing matched-reference clarification

Location: `submission-v10/manuscript.tex:214`.

**Before**

```latex
each history changes the regression and its matched historical reference.
```

**After**

```latex
regression is compared with its own matched historical reference at each history length.
```

Reason: Keeps the crucial fact that the reference changes with history length and is not held fixed.

### H04 — Pure language: history-caption punctuation

Location: `submission-v10/manuscript.tex:217`.

**Before**

```latex
Both methods retain their original, different penalty menus, and every tested history is shown against its own matched historical headroom.
```

**After**

```latex
The methods retain their distinct original penalty menus. Every tested history is shown against its own matched historical headroom.
```

Reason: Distinct original is less awkward than original, different. The unequal original menus and each-history matched reference remain explicit.

### H05 — Optional scope of question

Location: `submission-v10/manuscript.tex:212`.

**Before**

```latex
How much history does FX regression need?
```

**After**

```latex
How does FX regression vary with history length?
```

Reason: The current question is readable, but need can invite a universal threshold interpretation. This alternative describes the plotted comparison without asserting an optimal history.

### H06 — Existing legacy-table scope qualifier

Location: `submission-v10/manuscript.tex:154`.

**Before**

```latex
FX histories \{720,2880\}; weekly \{52,260\}
```

**After**

```latex
Original FX histories \{720,2880\}; weekly \{52,260\}
```

Reason: The new curve uses additional history lengths. Original scopes this inherited table row without adding or editing numerical entries. This is a label suggestion, not a new experiment inventory.

### H07 — Conclusion boundary — root editorial judgment required

Location: `submission-v10/manuscript.tex:214`.

**Before**

```latex
In these comparisons, conditional gains depend on sufficient history and a penalty menu that permits strong shrinkage.
```

**After**

```latex
Together, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.
```

Reason: Retains the requested two-factor link to the menu-isolation comparisons. Depend on sufficient history may read as a general necessary condition or causal claim; link describes the association in these comparisons. This affects inferential force, so it is not an automatic grammar correction.

### C01 — Pure language: journal-fit idiom

Location: `submission-v10/cover-letter.tex:12`.

**Before**

```latex
The paper suits Journal of Forecasting through its comparison of complete forecast procedures under matched histories and update schedules.
```

**After**

```latex
The paper is suited to the Journal of Forecasting because it compares complete forecast procedures under matched histories and update schedules.
```

Reason: Suited to is the natural idiom. The reason for fit remains the comparison design; no new-method or acceptance claim is added.

### C02 — Existing cost boundary and procedure terminology

Location: `submission-v10/cover-letter.tex:10`.

**Before**

```latex
Matched FX gains remain reference-dependent, weekly historical controls remain competitive, and CFTC expanded regression is generally cheaper under higher reserve and lower fixed-breach charges, with local exceptions.
```

**After**

```latex
Matched FX gains remain reference-dependent, weekly historical controls remain competitive, and expanded-menu regression has generally lower illustrative limit costs in the CFTC comparisons under higher reserve and lower fixed-breach charges, with local exceptions.
```

Reason: Expanded-menu names the actual procedure. Illustrative limit costs carries the manuscript’s existing cost-accounting qualification into the self-contained letter. Generally and local exceptions remain; no observed operating-cost claim is introduced.

### C03 — Existing history-result referent

Location: `submission-v10/cover-letter.tex:12`.

**Before**

```latex
The original-period FX learning curve shows that intermediate histories improve the matched comparison, while the longest history gives back part of the gain.
```

**After**

```latex
The original-period FX learning curve shows that full regression gains at intermediate history lengths and gives back part of the gain at the longest history.
```

Reason: A history length changes forecast performance rather than the quality of the comparison. Full regression avoids assigning the identical shape to the four-feature curve; original-period remains.

### C04 — Pure language: standard section term

Location: `submission-v10/cover-letter.tex:12`.

**Before**

```latex
Model confidence sets and cost-preference regions connect forecast evaluation to limit validation across related aggregate series.
```

**After**

```latex
Model confidence sets and limit-cost regions connect forecast evaluation to limit validation across related aggregate series.
```

Reason: Limit-cost regions matches the main section title. Related aggregate series remains unchanged.

### C05 — Pure language: supplied-material description

Location: `submission-v10/cover-letter.tex:12`.

**Before**

```latex
The accompanying materials provide native sources, complete adverse and unavailable results, official CFTC source records and
```

**After**

```latex
The accompanying materials provide editable manuscript sources, complete records of adverse and unavailable outcomes, official CFTC source records and
```

Reason: Native sources is software shorthand. Complete records of unavailable outcomes avoids calling an unavailable result complete. Keep the following hyperlink and author-declaration sentence unchanged.

## History-subsection boundary check

The existing paragraph/caption already preserve: the original FX evaluation period; original and different menus; each history length’s own matched historical reference; all tested histories in the display; retrospective status; and no universally optimal history. Those qualifications should remain. H01 repeats the existing short-horizon display boundary in the opening sentence. H02 avoids implying a full-regression or QR4 longest-history sign reversal. H03–H04 retain the fact that both the regression history and the historical reference vary, while each method retains its own menu.

H07 is the preferred conclusion-boundary recommendation sent to the root: it explicitly connects **the history comparisons and menu comparisons** to both **history length and the availability of strong shrinkage**, while replacing the general necessary-condition flavor of depend on sufficient history. The history curve by itself does not isolate a causal history-by-menu interaction. This is a bounded wording choice for the existing empirical interpretation, not a new score or scientific conclusion; the parent should decide whether its intended inferential force is preserved.

H06 flags a scope-label issue introduced by the new figure: a reader might mistake the methods table’s inherited FX histories for an exhaustive list of the new curve’s tested histories. Qualifying the row with Original is an available wording fix that leaves every number untouched. No new numerical list is supplied here.

The short-horizon full-regression gain remains favorable at the longest history, while the four-feature curve changes sign elsewhere within the tested range. The separate adverse longer-horizon comparisons retain their own scope. Do not delete adverse points, failed cells, unavailable summaries, left-censoring qualifiers, the unsupported switching increment or the retrospective qualification when tightening language.

## Three-finding consistency check

| Finding | Main-text anchors | Read-only conclusion / cover-letter comparison | Assessment |
|---|---|---|---|
| 1. Matched FX gains recur but rankings against the shorter rolling reference change | Introduction first finding; Results RQ1; new history subsection | Conclusion RQ1 and cover letter retain the reference distinction and nonmonotone history shape | PASS. Identify full regression/short horizon when describing the new curve, and retain original-period scope. No universal minimum history, optimal history or independent FX holdout follows. |
| 2. Weekly historical controls remain competitive; penalty-menu expansion addresses large calibrated-simulation losses | Introduction second finding; weekly/CFTC/MCS subsections; penalty-menu experiment | Conclusion RQ2 and cover letter retain historical competitiveness and the unsupported registered switching increment | PASS. Menu-isolation evidence concerns the calibrated laws. Empirical frequency causation remains unresolved; near-parity does not establish incremental feature value. |
| 3. Higher reserve and lower fixed-breach preferences generally favor expanded-menu regression in CFTC, with local exceptions | Introduction third finding; Section 8 cost regions; Section 9 implications | Conclusion RQ3 and cover letter have the same direction | PASS. Use expanded-menu consistently and retain illustrative costs in the self-contained letter. Lower score need not mean lower cost. |

The manuscript describes three empirical findings and explicitly calls the methods established; the cover letter agrees. The added history subsection extends finding 1 rather than introducing an unqualified fourth contribution. This pass proposes no theoretical-novelty or new-method claim.

## Terminology and protected forms

- Keep historical headroom for the F benchmark; history alone denotes the training window. Keep the matched reference distinct from the shorter rolling reference.
- Current source uses both four-feature and four-predictor. They name the same QR4 model here; choose one consistently in the final prose. This pass keeps the latest source’s four-feature form in H02 and E09 rather than imposing a cross-agent rename. Preserve QR4 file/code identifiers.
- Use expanded-menu regression when the penalty grid is expanded. Do not confuse an expanded penalty menu with a larger predictor set or a larger data universe.
- Preserve strict breach, mean overrun/underprediction and unused-headroom distinctions. A score gain does not imply fewer breaches or lower illustrative costs.
- Preserve common-origin, completed-label, source-unit, related-task, unavailable-result and non-elimination qualifications. MCS membership does not mean equal predictive risk or certified future coverage.
- General prose mainly uses American English; E14 suggests center. Preserve the spelling and diacritics of published titles and names rather than performing a global spelling replacement.
- Retain mathematical expressions, numerical strings, inequalities, reference labels, citation keys and URL targets exactly when applying a wording-only suggestion.
- Preserve all `[TO BE COMPLETED BY AUTHOR]` entries, including the AI statement, and the cover-letter signature. No declaration of originality, funding, conflicts or author approval is invented here.

## Review integrity

Every listed before-text anchor was found in the source snapshot. Each proposed replacement retains the identical sequence of literal numerical tokens as its before-text. This is a static editorial integrity check, not a scientific test or recomputation. H07 and the other boundary-sensitive items are segregated from automatic language fixes. No edits were applied by this reviewer.
