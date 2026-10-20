# Source register 48 — Counter-monotonic improvement and bounded sharing equilibria

Literature record, 20 October 2026. One new principal, two selected reading blocks.

## Principal source and version record

**Jean-Gabriel Lauzier, Liyuan Lin, Peter Wakker and Ruodu Wang, “Optimal risk sharing, equilibria, and welfare with empirically realistic risk attitudes.”**

| Item | Recorded evidence and limit |
|---|---|
| Actual scientific edition | **arXiv2401.03328v6**, [fixed record](https://arxiv.org/abs/2401.03328v6) and [observed original PDF](https://arxiv.org/pdf/2401.03328v6). |
| Version date | v6 deposited **17 July 2026, 00:20:37 UTC**; PDF title date **July 2026**. |
| Original fingerprint | **64 physical pages**, **584,274 bytes**; SHA-256 **897a4febd761000066ace2f2f93b7adb813b9ce9a1680c2933fb42679531dc9a**. |
| Page-count distinction | Landing comments' **47 pages** do not replace the physical count, including online appendices. |
| Earlier versions | v1 deposit **6 January 2024, 23:13:49 UTC** is metadata only. Earlier bodies remain unread and uncompared. |
| Publication identity | [10.48550/arXiv.2401.03328](https://doi.org/10.48550/arXiv.2401.03328) is the arXiv identifier DOI. No formal body or journal DOI established here. |

GRW's unversioned 2024 reference is titled “Optimal sharing, equilibria, and welfare with empirically realistic risk attitudes.” It pins neither v1 nor v6. The omitted word “risk” establishes no title-change date or content/numbering equivalence.

### Original synthesis — 134 words

<!-- SYNTHESIS_1_START -->
Lauzier, Lin, Wakker and Wang study one-period sharing under risk attitudes that include strict risk seeking. Their counter-monotonic improvement preserves component means and raises components in convex order, under an independent-randomization condition. The supplied proof separates independence from total payoff from the stronger allocation-vector condition, using joint-law copies rather than statewise-identical contracts. Additional boundedness and continuity support compactness and existence results. Expected-utility results distinguish homogeneous, heterogeneous and mixed groups; subgroup structure does not imply a common global dependence pattern. Competitive equilibrium imposes bounded individual deviations beyond market clearance. Under homogeneous strict risk seeking and nontrivial endowments, normalized prices and utilities can be unique while allocations remain nonunique. These are established model results, not empirical calibration, trading implementation or statistical guarantees. Selected rank-dependent-utility motivation was screened, while its later theorems and proofs were not read.
<!-- SYNTHESIS_1_END -->

## Actual reading scope

Pages are physical v6 pages. The identity record adds metadata/header/reference screening, not body coverage.

| Reading block | Selected material | Boundary |
|---|---|---|
| **216: initial selected pass** | Introduction **1–5** screened. Main **5–15**: definitions/orders, jackpot/ER, Theorem 1/ER* sketch, Examples 1–2, Proposition 2 statement. **A33–34**, Lemmas 1–4 joint-law/compactness/IR routes; **B.1 on 35** through Proposition 2 before B.2; **O.2 lower 49–upper 50** before O.3. **Image 13** inspected separately. | Incidental B.2 on 35–36 and O.3 lower 50 located/extracted, not proof reading. No full topology/kernel/measurability/continuity certification. |
| **217: later continuation** | **16–24**: Theorem 2 equivalences/sketch; Example 3/Propositions 3–4; Proposition 5/Theorem 3 mixed-group statements, two-step description/Example 4; bounded choice/Theorems 4–5; Proposition 6/Theorem 6 uniqueness statements. | **25–26** RDU motivation/reference-outcome/model contrast screened, not later theorems/proofs. No new image. Detailed Appendix B beyond 216, including Proposition 5 separation, unread. |

No full-paper/all-proof certificate is supplied; examples and algebra were not recalculated. Endpoint, tie, zero-weight, normalization and uniqueness cases remain uncertified. External Lauzier 2023, randomization, Choquet-continuity and empirical-attitude originals remain unread.

## Improvement, randomization and existence conditions

**Convex order before preferences.** Theorem 1 takes nonnegative integrable components summing to total payoff. ER supplies a standard uniform independent of that total. The resulting counter-monotonic, optionally jackpot, allocation preserves total and means while increasing components in convex order. This is not greater expected payoff or lower statistical risk. Welfare needs preference/strictness assumptions. Proposition 2's constant-shift extension retains one-sided boundedness.

**ER versus ER*.** ER* in the main sketch requires independence from the whole allocation vector; ER requires it only from total payoff. A quantile uniform supplies neither automatically. Appendix A/B.1 use joint-law-equivalent copies before the stronger sketch, not statewise-identical original components. O.2 limits universal ER* on standard Borel spaces. The supplied route does not certify randomization for every vector or preservation of path-dependent, covariate or trading constraints.

**Dependence and compactness.** The resulting jackpot partition need not be independent of total payoff. Mixing jackpot laws differs from averaging payoffs statewise; three-plus-component counter-monotonicity has special structure. Appendix A additionally requires bounded nonnegative total, ER and continuous utility/weights, using weak joint-law limits realized at fixed total. Unbounded losses or arbitrary constraints do not inherit this route.

## Preference groups and the equilibrium question

The expected-utility model uses bounded nonnegative payoffs, strictly increasing continuous utilities, ER and common probability. Theorem 2 does not make every heterogeneous-utility jackpot Pareto optimal. Constant-total/homogeneous results need their own assumptions. Expected-utility mixing linearity is not a general RDU or nonconvex-optimization result.

Theorem 3 treats mixed groups: strict risk seekers have a jackpot suballocation, strict risk averters an internally comonotone one. The full allocation need not share either pattern. Utilities and weights determine the group split. The two-step description is an existing antecedent, not a computed solver.

Section 5 bounds **each individual's budget-feasible deviations between zero and total statewise supply**. Clearance does not make these constraints redundant. Theorem 4 retains this game; its converse needs ER and universal strict risk seeking. Model prices are not forecast, observed risk-neutral or confidence laws. Sufficient endowment choices do not cover arbitrary ones.

Theorem 5 adds a jackpot relation between risk seekers and the remaining aggregate; Pareto structure alone is insufficient. General mixed-equilibrium classification remains open in the source. Under homogeneous strict risk seeking, ER, boundedness and a **nontrivial endowment**, Proposition 6/Theorem 6 give unique normalized prices and utilities, **not necessarily allocations**. Trivial endowments differ. An independent jackpot is sufficient, not universally necessary.

## Financial interpretation and remaining boundaries

Common probability supplies no heterogeneous-belief/ambiguity guarantee. The screened RDU discussion has a genuine reference outcome; its gain-utility conventions cannot be imported into positive-loss distortion notation by name alone.

No prices, preferences or strategies were computed here; no data/code acquired. Reuse terms are unverified. The arXiv nonexclusive license is not CC BY or blanket republication permission. No PDF, image or substantial passage is reproduced.

Sharing improvements, mixed groups and bounded equilibria already coexist here. Implementation needs its own claims/budget conventions. No novelty, final topic, design or experiment is established.
