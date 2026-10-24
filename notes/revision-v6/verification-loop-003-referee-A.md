# Verification loop 003 — internal referee A

- Role: internal language/logic referee A; no real external review and no Claude/Cloud or cross-model review.
- Actual evidence-review start: 2026-10-23T20:59:48Z (2026-10-23 13:59:48 America/Vancouver).
- Actual evidence-review end: 2026-10-23T21:02:00Z.
- Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
- Branch observed: `revision-v4-jof`.
- Authorized scope: one reread of current main-article `sections[4]` and its generated TeX source, with targeted owning-protocol checks. No full-paper reread is claimed. Search excerpts outside the section served only to locate the actual heading; no verdict is offered on those sections.
- Actual heading: **5. Research design and transparency**, not “Forecast evaluation”. The scope is JSON `sections[4].blocks[0:10]`, rendered-source `submission-jof/manuscript.tex:184–205`; `submission-jof/main.tex` delegates to that source. No PDF layout or compilation is certified by this review.

## Verdict and disposition

**PASS for this section's current language/logic, with two optional clarity suggestions. No necessary scientific-conclusion change was identified.** No manuscript, result, protocol, source, archive, or conclusion was modified. No financial analysis, model, numerical experiment, test suite, replay, or new result calculation was run. Source hashing, text extraction and provenance checks were the only computations. Only this new note was written.

| Exact paragraph route | TeX location | Language/logic assessment | Disposition |
|---|---:|---|---|
| `sections[4].blocks[0].html` | 185 | Explicitly distinguishes before-execution design/parameter freezing from an already-inspected FX evaluation interval and later post-result analyses. “Working-reference diagnostics”, “not selection-adjusted confirmation”, and the local/public-registration distinction prevent a confirmatory significance claim. This is a reading of the disclosure; public-timestamp publication was not independently re-established here. | Retain. |
| `sections[4].blocks[1].html` | 187 | Ending a clean pool at `r-H` is consistent with labels ending by `r`; moving its endpoint to `r` admits the H most recent immature origins. The stated six labels is consistent with an H6 control. Mixed Treasury/FX directions and the limited first/middle/last-block scope explicitly rule out inevitable optimism and all-sample generalization. Numerical figures were not recalculated in this language-only loop. | Retain. Optional clarity: call it the **H6 label-timing control**, so the reader need not infer why the immature count is six. This adds no scientific conclusion. |
| `sections[4].blocks[2].html` | 189 | Names both primary procedures, horizons, histories and updates, and identifies the FX H24 reference as legacy selected on a previously inspected study. The FX primary is transparently a complete-procedure contrast with unequal histories/update schedules, not an isolated conditioning effect. | Retain. |
| `sections[4].blocks[3].html` | 191 | Matching source/horizon/history against frozen F/S/K, retaining update controls, and preserving primaries are fair comparison disclosures. They do not assert equal fitting objectives or independent replications. | Retain. |
| `sections[4].blocks[4].html`, `blocks[5].latex` | 193, 196 | Defines left-minus-right loss and therefore the sign convention before inferential statistics. The .95/.05 pinball preference is explicit. | Retain. |
| `sections[4].blocks[6].html` | 198 | Keeps mean magnitude, method-specific strict-event severity, headroom and observed financial cost separate; explicitly says lower score and fewer breach occasions are different outcomes and prohibits pooling source units. No calibration/operational-cost overclaim found. | Retain. |
| `sections[4].blocks[7].html`, `blocks[8].latex` | 200, 203 | Bartlett HAC, fixed and doubled bandwidths, HLN's approximate application to pinball loss, finite-window unconditional predictive-ability interpretation, moment/mixing/LRV assumptions and dependence from shared training are disclosed. Neither H-based bandwidth nor doubling is claimed to remove all overlap/training dependence; the theorem assumptions remain working assumptions. The prose does not claim exact finite-sample size or validated selection-adjusted p-values. | Retain. |
| `sections[4].blocks[9].html` (original diagnostics) | 205 | Original sparse-grid POF plus transition-independence LR is identified as the archived CC convention. Issue-known capacity and matured `H+1` through `H+4` hit lags do not introduce look-ahead in the stated DQ adaptation. NA statuses are explicit. A fixed sparse grid itself does not prove independence; the paragraph makes no such claim. | Retain. |
| `sections[4].blocks[9].html` (multiplicity) | 205 | Fixed 72-member common-history adjustment, exact-identity p=1 bookkeeping and separate frozen new ranking families are not represented as a correction for all investigator/model selection. The nearby coverage discussion leaves a small possible scope ambiguity about which p-values enter 72. | Retain. Optional clarity: write **“The fixed 72-member common-history equal-loss ranking family receives Holm adjustment”**. This should not alter any family, value, archive or conclusion. |
| `sections[4].blocks[9].html` (new versus old CC) | 205 | Separately states S16's adjacent sparse-pair transition-conditional likelihood, conditioning on the initial hit, and says it does not replace the archived convention. Old full-grid-hit POF and transition-only likelihood use different finite-sample counts; the prose preserves that distinction rather than claiming equality. NA multiplicity bookkeeping remains distinct from an observed p-value. | Retain. Do not harmonize archived CC values in this loop. |

## Owning-protocol checks and mature-practice reference boundary

- `protocol/revision-20261022/study-spec.json`: source-specific primary and H24 legacy definitions, source-native units, complete-family failure policy, fixed H+1 grids and common-procedure/update comparisons match the section's named design.
- `protocol/revision-20261022/conditional-baseline-design.md`, selected lines 19, 25–27, 37, 41, 49: confirms mature refit pool, actual-query time, common histories/update controls and the limitation that the unequal-history FX primary does not isolate conditioning. Only selected protocol text was read.
- `protocol/revision-v6/common-contract.md`, full 15-line document, especially lines 7, 11–15: confirms mature labels, working-reference DM/HAC/HLN limits, unchanged old CC, transition-conditional new CC, separate family sizes, NA-versus-bookkeeping distinction and no historical-selection guarantee. The main section is consistent with this boundary. It need not repeat every family count because it names their separate freezing and points to S16; no S16 completeness audit is claimed here.
- `protocol/revision-20261023/round2-D1-mature-baselines.md`, selected lines 15, 20, 22, 30–31: mature same-target additions remain separate, exploratory, fixed-family comparisons.
- `protocol/revision-20261022/post-result-diagnostics.md` was inspected after protocol-name discovery; it concerns stored floor/horizon diagnostics rather than the original DM/CC definitions and was not used to certify the old CC implementation.
- Limited primary-source cross-check: the [Giacomini–White publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2006.00718.x) distinguishes finite-estimator predictive-ability testing and conditional versus unconditional objectives. The [Christoffersen 1998 original paper, institutional mirror](https://users.ssc.wisc.edu/~bhansen/718/Christoffersen1998.pdf) was consulted through its indexed section excerpt concerning transition likelihoods and conditioning on the first observation. This was a targeted primary-source check, not a full-paper reread; no claim is based on a third-party synopsis. It supports keeping the two finite-sample CC conventions explicit. No new scientific result or additional literature conclusion is inferred.

## Source fingerprints

All following source hashes were rechecked immediately before writing the note and matched their observed values during this review. These hashes identify the reviewed bytes, not independent validation of the numerical results.

- `submission-jof/manuscript-content.json`: `3a13df3d818218b095f4a6a4c548221c1ce233ed4317e7a5b1784ca24095b28d`
- `submission-jof/manuscript.tex`: `875516d3f7840e80f3b07de6783c68bc9efff248afff48ec280387d17c2bfab1`
- `submission-jof/main.tex`: `f67dee42ce85e43ee99337e09a1550892006b57b52017f6044edcb85068e0407`
- `protocol/revision-20261022/study-spec.json`: `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0`
- `protocol/revision-20261022/conditional-baseline-design.md`: `bdede74b2394a8dfb149c0671015bbb419609229779ca31b664f9b1756629725`
- `protocol/revision-v6/common-contract.md`: `6795bc1e59d1b5e245c601ff55d77abbbb121bb2700affefa02a89b884a7f7e8`
- `protocol/revision-20261023/round2-D1-mature-baselines.md`: `cec3a4df77c2d7f749361bdcb1a1e5e87be1f4aec460696959831a968ab873db`
- `protocol/revision-20261022/post-result-diagnostics.md`: `d9a533ceb0e9db035f866f4c2d7516f14c8959fd6355332d39b231b1565592eb`

## Scope exclusions and author decision rule

No owning computation, result array, supplementary numerical table, archive/public freeze timestamp, PDF rendering, all-paper language, or test outcome is certified here. No result significance/calibration conclusion needs to be changed on the evidence from this section-only read. Any later proposal to replace a CC convention, change a ranking family, revise p-values or promote retrospective diagnostics to confirmation requires author decision and a separately authorized scientific change; it is outside this audit.
