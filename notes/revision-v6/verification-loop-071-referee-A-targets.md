# Loop 071 — internal referee A: main target and methods

Audit window: 2026-10-23T23:14:24Z to 2026-10-23T23:16:15Z (UTC). Branch: `revision-v4-jof`; observed HEAD: `8d6f6279b8e6f411cdaec360d2ae6dbb653fc1f0`. This is a bounded same-model internal textual/static review, not external peer review. The parent goal remains active to 2026-10-24T00:31:50Z.

## Actual current scope and fingerprints

Read current main JSON section index 3, **4. Target and forecasting methods**: all 20 prose, 11 equation and 3 subheading blocks (34 non-table blocks), plus Table 2 caption at block 1, within the confirmed 35-block section. Read corresponding article TeX lines 88–183 with table body excluded. No table-cell validation or PDF rendering review; the PDF hash identifies the candidate only.

Static context: `conditional-baseline-design.md` lines 1–32 and `wp2-aci-sav.md` lines 1–37, used only for the definitions below. Historical design/status text is specification, not new execution evidence. Previous verdicts were not evidence.

SHA-256, freshly checked:

- `submission-jof/manuscript-content.json`: `324adad8bb9e71158614b36692f96de9b78228e3a3c7e6aa6eac7c73abf4c186`
- `submission-jof/manuscript.tex`: `57b2915d29c0ec84334097bca5ddfd125f46b9429fe07fabf0b168d9391c2ade`
- `submission-jof/manuscript-preview.pdf`: `c1c55699b53bb1a7ab3f1c4e131b4d45bc88965c6f22571ebc02c2ab7cd351d6`
- `protocol/revision-20261022/conditional-baseline-design.md`: `bdede74b2394a8dfb149c0671015bbb419609229779ca31b664f9b1756629725`
- `protocol/revision-v6/wp2-aci-sav.md`: `4d1115663011753ad85c41a9b5f6bf50b100e186d9a1c6d3c8b622fa996ac2e7`

## Findings

1. **Maturity, indexing and known floor (blocks 0–12).** Including h=0 makes B=|N_t| the observed floor and G=P−B nonnegative. The training interval ends at kappa−H, so labels complete by refit. Frozen pools/transforms/scales/coefficients are separated from the updating issue anchor; rolling controls refresh completed labels per issue. Historical peaks retain original starts; translation uses current signed position. These are forecasts, not allocations. Past-only features/training-only scaling and unequal feature lookbacks despite matched response origins agree with the static definition.

2. **F, S, K and QR are distinct (blocks 6–19, 34).** F adds historical headroom to current magnitude; S translates entire signed historical episodes; K floors historical peaks. The common pool/rank convention does not identify those constructions or their objectives. QR fits normalized headroom with an unpenalized intercept and ridge slopes, then projects only for issue/validation and evaluates in native units. Adding a known B translates a conditional quantile/loss; it does not make an arbitrary peak-level ridge fit equivalent. The cited static definition gives the corresponding shifted penalty: with B=mu_b+s_b*z_b, alpha=mu_b+a*beta0 and theta=a*beta+s_b*e_b, the native objective has penalty lambda/(2a)*||theta−s_b*e_b||². Main block 16 points to Supplement S4 instead of claiming equivalence to every zero-centered peak ridge model. Plain full-pool KNN is identified with frozen F only under the common rank; scaled full-pool KNN still changes responses.

3. **Rank versus future coverage (blocks 19–23).** The section distinguishes ordinary empirical pinball minimizers from the corrected order rank, including the W52 distinction and integer-probability-times-pool-size minimizer intervals. It states unavailable ranks fail. Those finite-sample conventions are not presented as future calibration guarantees. Proposition 1 separates the pointwise floor-loss result from the true conditional inverse-quantile tail statement; atoms can prevent equality, and fitted reports do not inherit the population statement. Equality-based coverage tests are explicitly diagnostics of their stated nulls. Displayed rank examples were read as definitions/examples, not independently recomputed.

4. **Finite ACI/SAV attribution (Table 2 caption; contextual protocol).** The caption calls later procedures finite adaptations defined in S16. The static protocol identifies delayed, state-projected ACI-style calibration as a modification of Gibbs–Candès, with no inherited long-run or conditional guarantee; headroom SAV adapts Engle–Manganelli dynamics with a completed G_(t−H) shock and finite bounded fitting, not the entire CAViaR class or literal return-VaR replication. No conflict was found with the limited wording actually present here. This audit did not reread S16 or table cells and therefore does not claim a complete current supplemental implementation audit.

5. **Population bounds and empirical controls (blocks 24–32).** The endpoint bound is attributed to classical Levy maximal inequality under independent symmetric increments; conditional use adds conditional premises and the corresponding conditional population quantile. Operational L is explicitly an empirical absolute-displacement plug-in on the frozen mature pool, without inherited coverage or loss ordering. The common-pool distance result requires the same available rank and is expressly deterministic, neither accuracy nor coverage. Proof paragraphs were read for their stated scope, not newly proved or executed.

6. **Horizon ordering and conditioning (blocks 33–34).** Population target/conditional-quantile ordering is distinguished from independently fitted reports. Raise-only repair, total-loss sorting and per-horizon improvement are not conflated. Crossing is a coherence diagnostic, not sufficient evidence of calibration failure. The final paragraph correctly acknowledges that historical controls already use current anchors. The displayed crossing count was encountered but not retraced or recalculated.

## Verdict and limits

No necessary scientific-conclusion issue found within this exact textual/static scope; no author-pending correction identified. Optional clarity only: block 16 could locally name the “shifted penalty” when directing readers to S4, but its existing statement and static definition already preserve the distinction. No source change is proposed or made.

Only this note was written. No models/tests/statistics/proofs/aggregates were run or recomputed; no raw/private vectors, new search/network/UI/Claude/Cloud, nesting, source/state/ledger edit or commit. This is bounded wording/specification consistency, not fresh empirical validation. Final full readback, SHA-256 and time are reported on delivery; no edit follows.
