# WP7 English, terminology and cross-reference review

Read-only review of the current main article and Supplement; no scientific source, generated document, result or method file was edited. The sole output of this pass is this note. No private financial arrays, fitting, actual replay preparation or new financial analysis was used.

## Scope and reviewed snapshot

- Main article: all twelve sections, abstract, 110 prose/equation/subheading blocks after the already-known duplicate research-design heading was removed, all six table captions, four figure captions, and the descriptive literature/method/decision-map table text.
- Supplement: all sixteen sections, 177 prose/equation/subheading blocks, all 68 table captions and seven figure captions. Financial table rows were not independently re-audited. Descriptive notation, method/status labels and internal-reference-bearing cells were inspected; original-source page locators in S15 were distinguished from internal article cross-references.
- Current JSON and generated standard TeX were both inspected. Unique caption inventories are main Tables 1–6 / Figures 1–4 and Supplement Tables S1–S68 / Figures S1–S7. No duplicate caption labels or genuinely nonexistent numbered internal targets were found. Two references exist numerically but route readers to the wrong or incomplete content, as detailed below.
- No PDF visual inspection, full test suite, external-source retrieval or new bibliography verification was performed in this pass; those remain separate checks owned by the root task.

Snapshot fingerprints at the end of source inspection:

```text
manuscript-content.json 6aaaa33af16e0c910ea0b01dcbf6585608459a261d98b5310c372873f401e057
manuscript.tex          6c7dc105c1e4e4f795684e93c938d908b9ced846c0c050e59306d3e8eff297f2
supplement-content.json d64a871c9f1b3f604830b2365c578121841366a699d4d59d2a17ac6e776cdbc9
supplement.tex          2d7290cb974189a9c9e6a7a6c2ae03e59b6fabf621f1bfb60d99757b61ab998b
```

## Actionable findings

1. **[P2: misdirected cross-reference] Main Table 6, first row.** The evidence cell says “Tables 3, 5 and S16.” Table S16 is the retained fixed-terminal e-value table, not the additional ACI/SAV/combination analyses. The intended locator is the section: “Tables 3 and 5; Supplement S16,” or exact relevant new table numbers. The current text is also present in `manuscript.tex`, line 331.

2. **[P2: incomplete menu routing] Main Table 2 caption.** “Parameter menus and fitted choices are retained in Supplement Table S2” no longer covers the whole overview after the ACI/SAV/combination rows were appended. Table S2 contains the original selected QR/KNN penalties/neighborhood counts; new validation and method inventories are in S16. Scope the caption to the original QR/KNN choices and route the added methods to S16. The individual new rows already point there correctly. Current TeX locator: line 92.

3. **[P2: missing operational definition, correct implementation] S16 ACI definition.** The paragraph specifies matured scores, projection, corrected rank and gamma selection, but not the initial state or feedback update itself. Consequently the prose alone does not tell the reader how a matured hit changes the state. Add the frozen initial alpha of .05 and the sequential update by gamma times (.05 minus the strict wrapped hit), followed by projection using the current calibration count. The implemented loop performs this for each matured feedback item in origin order. This is a prose-completeness correction, not a request to change or rerun ACI.

4. **[P2: incomplete normalizer definition, correct implementation] S16 state/GW definition.** The text calls a0 and v0 “initial-training constants” but does not give their construction. Define a0 as the positive QR response scale from the initial mature training pool and v0 as max(mean initial-training short increment RMS, 1e−12). Table S59 displays their values but is not a procedural definition. These rules are already fixed in the WP4 protocol and implementation. No new calculation or financial rerun is needed.

5. **[P3: first-use terminology] RMS, ACI, SAV and panel aliases.** RMS is mathematically specified in main Section 4, but “root-mean-square” never appears in either document. The main related-literature paragraph gives “adaptive conformal inference,” yet neither document explicitly introduces “(ACI)”; the standalone Supplement does not give that expansion. SAV appears in the main overview before any full name, and S16 mentions “symmetric absolute-value” only after using SAV. Use explicit first-use names, preferably “past position-increment root-mean-square (RMS),” “adaptive conformal inference (ACI)” and “symmetric absolute-value (SAV).” Similarly introduce C2 as the four-predictor parsimonious QR alias and QR33 as the original 33-predictor QR when the panel aliases first appear. This is a reader-definition issue; it does not indicate an undefined computation.

6. **[P3: misleading fallback wording] Main Section 6, plain KNN paragraph.** “These rows use the complete pool, so they show the full-pool fallback” describes a validation-selected k=W identity as a fallback. No fit failure or substitution occurred. “Selected full-pool identity” or “selected full-pool special case” expresses the actual procedure and agrees with S16's explicit no-substitution treatment of missing panel KNN.

7. **[P3: labeling consistency] Main research-design dagger legend versus S16 tables.** The main legend says a dagger marks post-result analyses in tables/figure captions and applies throughout the Supplement. New Tables S38–S68 have no dagger, although the S16 opening correctly and explicitly labels the entire section post-result/exploratory, and Figures S6–S7 carry daggers. Either qualify the legend to recognize the section-wide S16 label or consistently mark those new captions. Their exploratory status is substantively stated already; this is a legend-consistency issue.

8. **[P3: small English/typography fixes, no numerical change].** S5 title “Explicitly report diagnostics” is an imperative rather than a section noun phrase; “Issued-report diagnostics” would fit the content. S7 subheads “Ar estimation definition” and “Ar annual and sparse-grid sensitivity” should retain the established uppercase AR. S10/S13 begin with lowercase “selected-fit”/“mature-baseline,” unlike the section sentence case. S15's exact-bridge paragraph begins lowercase “main-article Table 4.” Fix the missing spaces in “bandwidth,72-family,” “40 or12” and Table S32's “on277.” “All new paths use the prerecord of two independent random streams” in S11 is unclear English; state that streams/seeds were recorded before execution. None requires a number, method, source or result change.

9. **[Author completion, not an inferred answer] Declarations still contain three author placeholders.** Author/ORCID, funding and conflict-of-interest fields remain “[TO BE COMPLETED BY AUTHOR].” They should remain visible until the author supplies those facts; this review does not invent them or treat the local revision as submission-complete.

## Sensitive definitions and claims checked without finding another mismatch

- **S16 mathematical presentation:** the completed-H ACI score, maturity inequality, finite projected state/rank, normalized SAV recursion and multiplication by the held response scale, full-axis group influence/SE, delayed GW instruments/moments and exact target-level tail screens have correct Unicode/subscript/superscript HTML and full standard-LaTeX forms. The generated S16 TeX contains the scaled SAV report. A scan excluding legitimate `\\tau`/`\\lceil` commands finds no remaining raw `tau=`, `ceil(`, `beta0`, `q_(`, `d_(`, `RMS_t` or `>=` core-formula remnants.
- **Reference identities:** original FX QR W2880 versus rolling F W720 remains separate from matched W2880 frozen F; Treasury original QR/F W260 remains named. Main Figures 3–4 and Supplement S4–S5 concern the original primary pairs, whereas S6–S7 concern fixed combinations against matched constituents. The Table 4 gain bridge is distinguished from Table 5 coverage diagnostics after the table-order remapping.
- **Diagnostic meaning:** legacy mixed-initialization CC and new transition-conditional CC remain explicitly different. Original and new Holm families are separately named; raw NA is not called a valid observed p=1. GW joint rejection is not called a state effect or a deployed switching result. Position-increment RMS is not described as price/yield volatility. ACI/SAV are identified as adaptations rather than inherited guarantees or literal original-method replications.
- **Selection and scope:** new methods, gamma/lambda choices, states, combinations and target-level checks remain retrospective/post-result/exploratory. The lower target's retained directions do not become an upper-target robustness result; the upper target remains unavailable for stated full-menu or tail-information causes. Missing plain panel KNN is not replaced with C2 or L. Shared Treasury tasks are not called independent dealers or independent trials.
- **Public information and economic interpretation:** main Section 3 and S12/S16 retain downloaded-vintage economic-date replay, unavailable reconstructed release vintages, dealer aggregation/netting and valuation/composition limitations. The prospective protocol remains pending and its live adapter is explicitly unimplemented. Forecast envelopes and stipulated scoring weights are not converted into observed funding, margin, inventory-policy or causal economic savings claims.

No source edits were made. Findings 1–4 concern reader routing/definitions; the remaining items are terminology, label consistency, English polish or explicit author-supplied completion.
