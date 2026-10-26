# G5 new main-text scientific check

Status: PASS for the reviewed source snapshot. No material numerical or scientific contradiction found in the new Section7.4, new validation table, retained tau table/repair paragraph, or Section9.1 RP paragraph. Read-only comparison used the592-scalar catalog and its actual JSON sources; no data/model/score calculation or manuscript edit occurred.

Scope: submission-v10/manuscript.tex Section7.4 and9.1, plus generated/v13-validation-main.tex. Abstract/contributions/conclusion synchronization belongs to G6 and is not flagged as a present gap. Supplement numbering is pending the owning compiled aux and remains root's final check.

## Section7.4, sentence-level findings

1. “Penalty selection dominates positive excess loss in27 of41” matches F1 D2 exactly: E>0 and S>E/2 in27 of the41 fixed CFTC/panel W52 comparisons. It does not claim all41 lose or that selection is the sole cause. “Dominates” here means the per-cell >one-half criterion, not a ratio of marginal medians. For maximum reviewer clarity, spelling out “exceeds half of positive excess loss” would be an optional precision edit, not a required numerical correction.
2. CFTC medians19.33→4.03 and10.35→0.53 exactly round the preserved F2 arm medians. The first history is52 and second260, and the new table makes this explicit. No paired-median interpretation is used.
3. NY Fed6.68→−1.13 at H6 and40.47→5.02 at H24 exactly round G2's complete13-source arm medians. The adverse H24 long-validation median remains explicit.
4. The evaluation-hindsight finite-menu winner still loses in29/41, matching D1. The next sentence limits the interpretation to the tested features and finite menu, rather than all conditional models.
5. The decomposition correctly separates E−G selection and finite-menu G, identifies the five-penalty oracle as retrospective/nondeployable, and excludes ordinary I. Marginal medians19.44,18.32,4.37 match the source. The text explicitly says they need not add, avoiding the false18.32-of19.44 share claim.
6. The negative selection-component possibility when I beats every finite candidate is mathematically correct, as are the negative long-history FX gaps for both horizons. No prospective selection claim follows.
7. Increased intercept-only selections are correctly supported by CFTC4→10/4→5 and NY Fed6→9/3→9. The text explicitly retains H6's18-week endpoint/refit-phase change and the zero median paired change; it does not confuse this with the lower arm median.
8. Four-feature sensitivity and old CFTC numerical failures remain pointed to supplementary detail. The statement connecting history, validation evidence and shrinkage should remain a bounded empirical interpretation: near-parity from a menu including I does not prove added conditional-feature value or a universal necessary condition. The preceding tested-feature/menu and hindsight limitations provide that boundary; no new such guarantee is currently asserted.

## New validation table

All four rows and counts are correct: CFTC histories52/260 use17 series; NY Fed H6/H24 uses13. The displayed medians and infinity counts match exact JSON values in the catalog. Validation52/156 and unchanged evaluation periods are correctly stated. The note independently retains the H6 endpoint shift and warns that arm medians do not measure typical paired changes. “Intercept-only limit” means ordinary I; it is not relabelled as corrected-rank F.

## Tau sensitivity and repair

The tabular numerical body is byte-identical to the v12 baseline8060807: CFTC W52 +3.45/+15.05; W260 +1.58/NA; FX original−10.15/NA; early−17.85/NA; bill+.67/+44.22. No16/17 CFTC subset median is promoted to a complete-group value.

The paragraph correctly says28 known CFTC wins out of34, one unavailable cell and unresolved29-win threshold; both FX99% outcomes remain unavailable. **Six of ten** are forecast-compatibility passes, not failures. The rejected repair was designed after failure and stopped before any of the three failed cells was re-estimated; old unknown judgments/NA entries remain intact. The repeated table note is consistent with the paragraph and the source gate failure.

## Section9.1: RP definition and actual failure

- Six-point menu,156 weekly/5760 FX validation records, corrected-rank default and paired one-HAC-SE gate match the sealed design. A strict positive improvement exceeding a nonnegative SE implies the separately required strict lower validation mean.
- Weekly ordinary median14.63→RP0.00 rounds the60-cell summary. The median criterion passes, but the paragraph prominently states **8** outcomes above10%, violating the5% ceiling (at most3/60), and retains the80.98% worst loss. This accurately reports R1 supported and R2 not supported; it makes no claim of general protection.
- Both FX gains are retained, matching per-period R3; it does not claim extra FX improvement. The figure caption's34 CFTC/26 NY Fed/2 FX complete/planned counts are exact.
- The definition is fixed after prior findings and evaluated on inspected periods. The final sentence states its retrospective character. A future title or discussion must not turn “benchmark-protected” into a proved risk guarantee; the present numerical failure prevents such a reading.

Catalog source SHA verification passed for all16 referenced files. Snapshot manuscript SHA: 4f78f4dde754793e20e88128e7187c6d1428bc02f488c5f94b93047c8b1c3b3a. Snapshot generated-table SHA: c65020a455267ce5a8ed86cb18a304c64a142b2628b6ab03d7f9bc5402208494. Checked UTC: 2026-10-26T04:05:26.366066+00:00.
