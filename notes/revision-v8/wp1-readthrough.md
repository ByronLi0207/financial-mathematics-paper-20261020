# WP1 paragraph read-through and disposition

Scope: abstract; every Introduction paragraph including C1–C3; first paragraphs
of Results 7.1–7.3; every Conclusion paragraph. The original and revised
passages are in `wp1-before-after.md`. This is a textual human-style reading
pass, not an additional financial analysis or an audio artifact.

| Passage | Finding | Disposition |
|---|---|---|
| Abstract | Negative signed loss-change language; opaque coverage label; shorter-horizon scope implicit | Direction stated as lowers; one-decimal displays bound to original fields; ACI expanded; shorter-horizon scope explicit. All adverse claims and 34/48 remain. |
| Introduction opening | Concrete position-path motivation already works; ending reports an activity rather than posing the question | Motivation kept; last sentence asks whether conditioning improves historical rules. |
| Historical-competition motivation | Completed outcomes is premature terminology | Past peaks replaces it here; exact maturity condition stays in Evaluation. |
| Introduction data/method paragraph | Unit separation and the same completed response sound like a process report | Unit detail removed here and kept once in Data. Paragraph now states the comparison and its questions. |
| Repeated FX finding | Negative changes-by wording obscures the direction | Lowers and raises identify the direction; earlier rolling-reference failure remains explicit. |
| Scores/breaches motivation | Elementary-score wording unexplained; comparisons could be conflated | Murphy diagrams defined; separately named contrasts and distinct error-weight question preserved; matched breach counts kept. |
| C1 | Target, classical assumptions, one result, nearest literature and evidence location are required by the inherited contribution template | Kept. Removing its literature/evidence sentences would violate that template. No first/novel claim added. |
| C2 | Generic opening reports heterogeneity without stating the finding | Opens with weekly historical wins and long-history short-horizon FX gains; it describes observed source-frequency combinations, not an identified frequency effect. |
| C3 | Validation argument is useful, but elementary-score label adds jargon | Murphy diagrams replaces the label; the 20.6:1 statement remains tied to its distinct long-horizon legacy contrast. Required literature/evidence location kept. |
| Introduction roadmap | Four sentences dwell on paper organization | Two concise sentences retain the required roadmap and practical takeaway. |
| Results 7.1 opening | Repeated matched gains are clear; table-column description distracts | Explains the effect of holding history fixed and states the different rolling-reference comparison. |
| Results 7.2 opening | Commentary about making reversal a main result is editorial process | States the adverse operational-reference reversal directly. |
| Results 7.3 opening | Strict-hit indicator needs decoding | Defines a breach as the realized peak exceeding the forecast. Unadjusted 376/360 and adjusted 329/328 remain separate. |
| Conclusion first paragraph | First research question language sounds like a report | Ends with the specific successful setting and benchmark-dependent broader ranking. More frequent breaches and earlier reversal remain. |
| Conclusion second paragraph | Numbering research questions repeats structure rather than findings | Leads with failure to transport the FX configuration, then the distinct score/breach/stability requirements. It does not assert frequency causes the failure. |
| Conclusion future work | Concrete prospective/dealer and economic-value questions already follow from the evidence | Kept; no new prospective or independent-validation claim. |

## Numerical display correction caught before acceptance

The first coarse draft rounded the old two-decimal `10.15%` display again,
producing `10.2%`. The original saved field is `-10.145914078498173`, whose
direct one-decimal absolute display is `10.1%`. The saved-field checker failed
on this one draft mismatch (`wp1-rounding-red.json`), then passed on all 17
prose percentage occurrences (`wp1-rounding-green.json`). No saved outcome,
table cell, target, statistical test or underlying conclusion changed.

This is recorded as **MISMATCH-WP1-01**, a corrected intermediate display
error, not as a new empirical result or a contradiction in the source data.

## Wording decisions

- Delete the numerical-fit qualification instead of asserting convergence
  without checking individual solver receipts.
- Keep the original contribution evidence/nearest-literature structure.
- Keep adverse short-history, longer-horizon, weekly and conservative-selection
  outcomes explicit; do not turn partial gains into a universal ranking.
- Keep all original table blocks and mathematical blocks unchanged.
- V8 authoritative text is `submission-jof/manuscript.tex`; do not rerun the
  historical v7 assembly script and overwrite these revisions.

Same-model read-only reading suggestions informed this pass. No Claude or
cross-model review was invoked.
