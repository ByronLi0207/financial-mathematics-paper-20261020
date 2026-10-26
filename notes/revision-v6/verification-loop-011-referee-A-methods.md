# Verification loop 011 — internal referee A: methods and guarantee boundaries

Status: **PASS for the bounded textual/definition verification below.** No necessary scientific-conclusion problem was identified within this read scope. This is an internal reread, not external peer review, independent numerical validation, a new proof, or an assessment of submission readiness.

## Identity, time and authority

- Repository: `/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023`.
- Observed branch: `revision-v4-jof`; observed HEAD: `5bc4c5cbd02757a6cb8841f4d8b513164a6691a8`.
- Authorized activity: verification loop 011 only; current main Section 4 and the existing owning proof/protocol/definition passages needed to check its language and logical boundaries. Optional language concerns are recorded without edits. A necessary scientific-conclusion problem, if found, would be author-pending only.
- First explicit clock observation during the reread: **2026-10-23 21:18:17 UTC** (14:18:17 America/Vancouver). Preliminary routing, repository-status reads and initial Section 4 extraction preceded that clock mark; no exact start time is inferred for those preliminary reads.
- Source hash capture: **2026-10-23 21:19:16.846615 UTC**. Completion/currentness check: **2026-10-23 21:20:00.647644 UTC** (14:20:00 America/Vancouver). Every source hash below was unchanged between those two captures. These timestamps bound the recorded hash checks, not an asserted duration for every preceding read.
- Only this note is written. No manuscript, supplement, code, result, conclusion, state file or commit is changed. No tests, model runs, replay, fresh financial calculation, new counterexample, new proof, broad literature search, Claude/Cloud review or cross-model review was performed.

## Actual read scope

The checked main object was `submission-jof/manuscript-content.json`, **`sections[3]`**, with its heading verified as **`4. Target and forecasting methods`** and **all 35 blocks, indices 0–34**, including Table 2, definitions, equations, three propositions, operational L, rank language and horizon-coherence qualification. Its corresponding `submission-jof/manuscript.tex` was read at lines **88–183**. The JSON and this TeX section express the same method definitions and guarantee boundaries in the inspected passages.

Existing owning material read for correspondence:

- `submission-jof/supplement-content.json`: non-table text/equation/subheading blocks in S2, S4, S5, S7, S11, S13, S15 and S16. This includes S2's common-set derivation and limits; S4's numerical/rank and shifted-penalty conventions; S5's rank-ablation definition and interval/tie qualification; S7's ordered-residual replay definition; S11's existing first-crossing proof and dependence/conditional-threshold qualifications; S13's already stated FHS/POT/QRF adaptations; S15's already stated mathematical illustrations; S16's ACI-style/SAV, combination and target-level definitions. Tables and reported result values encountered in this text were not independently recalculated or revalidated.
- `submission-jof/supplement.tex`: S2 lines 222–310, S4 lines 350–378, the rank definition/qualification at 444–450, AR definition at 585–601, existing Proposition 2 proof/premise counterexample at 748–752, S13 method definitions at 955–984, existing S15 illustrations at 1177–1187, and S16 method-definition paragraphs at lines 1228, 1656 and 2582. Some range endpoints include an adjacent heading or table boundary.
- `protocol/revision-20261022/study-spec.json`: retained target level, QR/neighbor menus, training-only transform/scale conventions, refit/source clocks, rank/tie rules and complete-cell policies.
- Static definition reads: `conditional_features.py` (feature construction, transform, mature indices, refit clock, response scale, neighbor selection); `conditional_study.py` lines 1–260 (fit/issue/historical/rank and scoring/selection definitions); `conditional_quantile.py` certificate/solver excerpts at 135–205 and 242–276 plus targeted search hits; `study_core.py` rank/order-statistic and label-cache excerpts at 60–93 and 229–252 plus targeted search hits; all of `round2_levy.py`; `v6_aci.py` lines 1–145; `v6_sav.py` training/issuance excerpts at 193–229 and 293–346 plus targeted search hits; `v6_combinations.py` lines 1–35; `v6_tau.py` opening definitions through line 70 and targeted search hits. These were read as definitions, not executed or treated as a comprehensive implementation audit.
- Ancillary search-only context: function/method hits in `parsimonious_v3.py` and `v5_theory.py`. These modules were not fully audited and their scientific routines were not run.

Scope disclosure: an initial incorrect TeX range extraction displayed main-manuscript lines **190–350**, outside Section 4, before the correct 88–183 range was read. The broad supplement text extraction also displayed existing result commentary and S15 positioning locators beyond the specific proof paragraphs. This incidental text was not used to extend the verdict to those sections, assess numerical results, or initiate new work. No earlier verification-loop verdict was used as evidence for this verdict. A brief memory-registry routing check was superseded by the current local sources; it supplies no scientific finding here.

The mature-practice check was limited to formulations already present in these sources: pointwise pinball projection, conditional lower-inverse-quantile strict tails, the classical Lévy first-crossing argument, finite order-statistic stability, training-only transforms, delayed label maturity and explicitly finite adaptations. No new literature-based claim is made.

## Findings against the existing owning statements

1. **Known floor: pointwise loss versus population tail.** Main blocks 2–3 include the origin observation in the sampled peak, so the stated response floor is the observed magnitude. Blocks 20–23 distinguish the pointwise report-projection identity from the true conditional inverse-quantile strict-tail statement. They allow strict inequality at atoms, explicitly say the floor need not itself create an atom, and decline to transfer the population conclusion to fitted reports. S4's equivalent peak parameterization and S15's existing floor example preserve those boundaries. The equality-based coverage diagnostics are explicitly limited to their stated nulls.

2. **Classical endpoint-to-peak bound and L.** Blocks 24–27 require independent, individually zero-symmetric real increments and the population quantile of **absolute endpoint displacement**. They do not impose identical distribution or finite moments. The displayed bound matches S11's existing strict-crossing argument, including atoms and zero thresholds. Conditional use additionally requires the premises and the endpoint quantile under the corresponding conditional law. Blocks 27 and 32 expressly withhold that guarantee from the empirical overlapping-label L construction and dependent mean-reverting data; they distinguish a generic signed one-sided endpoint VaR from the required absolute functional and promise no pinball ordering against F. `round2_levy.py` statically uses completed absolute endpoint displacements, the stated corrected 39/40 rank and the current magnitude. No simulation result was rechecked.

3. **Common-pool construction distances.** Blocks 28–31 require one nonempty pool, one available rank, and peaks including their starting observations. Their rowwise comparison, projection and same-rank order-statistic step correspond to S2.1. S2 explicitly states that changing one side's rows does not justify the bound; it also excludes an automatic extension to QR, scaled responses and the richer feature distance. Main blocks 17–19 separately define scaled KNN and retain its difference at the full-pool setting. Consequently the inspected language does not silently apply the F/S/K same-pool result to differing normalized scenario arrays or multivariate neighbor sets, and it does not convert distance stability into a signed accuracy/coverage claim.

4. **Mature labels, histories and refits.** The Section 4 training pool ends at `κ−H`, with the current anchor still updated at issue `t`. The corresponding feature and forecast definitions slice labels with ends no later than the refit; transforms, response scale and fitted coefficients are retained within the refit block. Frozen and rolling historical controls keep their stated distinct clocks. The text also preserves the extra past-only feature lookbacks rather than claiming that common response origins make all information sets identical. S16's ACI-style score pool and SAV mature-headroom recursion have their own explicitly stated updates; they do not assert access to immature future paths. These are definition checks only, not a causal replay or historical public-release validation.

5. **QR, numerical acceptance and empirical minimizer intervals.** Blocks 13–16 state the normalized headroom objective, unpenalized intercept, ridge slopes and issue/validation projection outside the fitting objective. S4 retains the scale-dependent shifted peak penalty rather than equating this with ordinary zero-centered ridge on peak responses. S4 also confines the feasible-dual/objective-gap and ADMM checks to numerical acceptance: no statistical law, issued-report-distance bound, unique minimizer or interval-arithmetic certificate is imported. The static solver excerpts are consistent with that stated scope.

6. **Ranks, repetitions and ties.** Block 19 and S4/S5 distinguish the noninteger `W=52` ordinary-versus-corrected rank from the integral `Wτ` minimizer-interval endpoints at W720, W2880 and W260. They allow ties to collapse a difference and do not label corrected F universally non-ERM. The static definitions preserve repeated values, use exact integer corrected ranks, and use more-recent origins for exact distance ties. The generic low-level order-statistic helper has an unavailable-rank infinity sentinel; the inspected method callers explicitly reject unavailable ranks, so the main method-level failure wording is consistent. Plain full-pool KNN and frozen F use the same completed headroom array/rank; scaled KNN changes the responses and need not share that identity. No forecast identity or sample result was newly recomputed.

7. **Additional method labels and guarantees.** Table 2's finite delayed ACI-style, headroom SAV and fixed combination descriptions correspond to S16's already stated finite procedures. ACI's score/hit maturity and projected rank are explicit and no original ACI guarantee is imported. SAV is a headroom adaptation with a finite multi-start algorithm and retained failure rule, without a global-optimum claim. Fixed combinations require aligned constituent histories, retain a missing-constituent NA and claim only floor preservation, without asserting conditional quantile validity or improvement over the best constituent. S13 likewise keeps the FHS/POT/QRF adaptations and their unverified assumptions distinct from canonical-method guarantees.

8. **Horizon wording.** Block 33 separates ordering of observed nested-horizon targets and their population conditional quantiles under the same information from independently fitted report ordering. It uses the existing S15 raise-only counterexample narrowly, while allowing the separately qualified total-loss sorting result. Crossing remains a coherence diagnostic. The displayed empirical crossing count was read as retained text and was not recalculated in this loop.

## Optional language concerns — no edits

- **Main block 16:** “Adding B to a headroom quantile translates it into a peak quantile” could explicitly repeat “conditional on the issue information” for a reader who has not yet reached Proposition 1. The existing known-origin setting and S4 already supply that qualification. This is a clarity option, not a discovered scientific-conclusion error.
- **Main blocks 4–5:** the refit paragraph could explicitly call its pool the “base fitted-model training pool” to help distinguish it from S16's per-issue mature calibration-score updates and SAV state propagation. The current detailed definitions already distinguish these mechanisms, so this is a presentation option only.

**Necessary scientific-conclusion items for author decision: none identified in this bounded reread.** No optional concern above is implemented or treated as permission for a manuscript change.

## Source fingerprints

SHA-256 values below were captured at both recorded hash-check times and matched. Fingerprints bind this note to the actual local sources; they do not establish execution, numerical correctness, independent replication or historical availability.

| Source | SHA-256 |
|---|---|
| `submission-jof/manuscript-content.json` | `3a13df3d818218b095f4a6a4c548221c1ce233ed4317e7a5b1784ca24095b28d` |
| `submission-jof/manuscript.tex` | `875516d3f7840e80f3b07de6783c68bc9efff248afff48ec280387d17c2bfab1` |
| `submission-jof/supplement-content.json` | `738bb71afab319e52b5296328858f890bf692692c97a3ab2a35a78f4d3ae6e28` |
| `submission-jof/supplement.tex` | `986b7db8aacc74002499924efe50877c064063c4225f419efb42778b0d967fb8` |
| `protocol/revision-20261022/study-spec.json` | `d1ecd6d3805e2546da2897bd76956dbdc661821da8f58bf86caeac642176e1b0` |
| `conditional_features.py` | `4ee667a84ca39c74457b3cd1b07dcb76d6832d3e51e6155353e00c298262d8f5` |
| `conditional_study.py` | `aec1803fcc8423760608882902db15642582cbb18a9c656870ac7c50092bd740` |
| `conditional_quantile.py` | `2cfe7f00872b6c97ac2558d5d3d79756db5061dfe7d5072b3a92d4d4ba338ff7` |
| `study_core.py` | `1619293cf09f18e56538bca6fa57660bc16795460ae4b10f14eb7d99794d81cf` |
| `round2_levy.py` | `36110d48f1e554b1ea202a61ed698f965229a9e5f8c8a46f22af8eacbe7a3885` |
| `v6_aci.py` | `e81005a25ca7b94dec86540981b890c945c280478b861e7416f7fb852f67b15a` |
| `v6_sav.py` | `a476828ee8818572a4b57e4b170ec4ee4ccecbef43c4babdf37138329ee586c1` |
| `v6_combinations.py` | `24adcb0db6272139301dff65529d91c53a9264b451b1bfd9e238610fbe333513` |
| `v6_tau.py` | `f221952df2b28fd6ded33bf74c17ae7652a929d0c49c3be284dc8fe142ef2b11` |
| `parsimonious_v3.py` (search-only) | `d330cf53c34b8cb8c9b6b182bf0c8ae21b40b92548e71644abfbf4ceb7e259e8` |
| `v5_theory.py` (search-only) | `8c04d58889599f55681f0b72dc62c132268406cc5105b69aa8247259151b17d9` |

At the recorded completion/currentness check, tracked working-tree and index diffs were empty. Pre-existing untracked backup files were observed and left untouched. No state update or commit is authorized by this internal-verification note.
