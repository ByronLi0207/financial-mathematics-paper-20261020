# Source register 49 — Rank-dependent sharing extensions and the formal peer-sharing edition

Literature record, 20 October 2026. **Zero new principals:** an existing v6 article gains selected scope; an existing peer-sharing article gains a selected formal edition. Registers 48 and 47 are not backfilled.

## 1. Lauzier–Lin–Wakker–Wang: later selected v6 material

**Jean-Gabriel Lauzier, Liyuan Lin, Peter Wakker and Ruodu Wang, “Optimal risk sharing, equilibria, and welfare with empirically realistic risk attitudes.”** [arXiv 2401.03328v6](https://arxiv.org/abs/2401.03328v6), [original PDF](https://arxiv.org/pdf/2401.03328v6). Title date **July 2026**; deposit **17 July 2026, 00:20:37 UTC**. **64 physical pages, 584,274 bytes**, SHA-256 **897a4febd761000066ace2f2f93b7adb813b9ce9a1680c2933fb42679531dc9a**. Earlier editions unread/uncompared; no new version here.

### Original synthesis — 118 words

<!-- SYNTHESIS_1_START -->
Lauzier, Lin, Wakker and Wang extend their sharing model to homogeneous rank-dependent utility on nonnegative gains. Small-payoff results use a linear-utility range, a concave weighting majorant and a feasible independent equal-probability jackpot. Large-payoff and local-gamble comparisons have different hypotheses and can favor different allocations. Selected appendices supply envelope and attainment routes, utility-ratio relaxations, nonpositive expected-utility counterparts, and randomized utility-frontier and subgroup computation arguments. Expected-utility mixture convexity does not extend automatically to rank-dependent preferences. Pointwise optimization still needs measurability, and the subgroup split need not be globally convex or concave. Satiation examples differ from strictly increasing-utility results. These are later selected additions to the same v6 article, with external proofs, literal boundary cases, numerical certification and financial implementability unverified.
<!-- SYNTHESIS_1_END -->

### Actual later scope

Physical v6 pages. These later readings do not expand the earlier screening record.

| Reading | Selected scope | Excluded or more limited evidence |
|---|---|---|
| **218** | Section 6 **26–31**, assumptions/statements/discussion; conclusion **31–32**; **image 29**. | No proofs here. External RDU/preference/reduction originals unread. |
| **219** | **B.4 lower 40–upper 42**, supplied Theorem 7(i)–(iv)/Proposition 7 proofs before References; **27–30** revisited. | Theorem 6 tail upper 40 and references 43 located only. No new image. |
| **220** | **O.6 lower 60–upper 62**, extensions/order route; **O.7 lower 62–63**, assumptions and Theorems O.2–O.4/Propositions O.6–O.8 statements. | O.5 on 60/references 64 located only; O.7 proofs not reconstructed. No new image. |
| **221** | **B.2 on 37**, Proposition 5 proof; **O.3.1 lower 50–upper 52** before O.3.2; **O.3.3 lower 52–upper 53** before O.4, satiation route. | Pages 36/38, Theorem 3 tail 37, O.3.2 first-welfare proof 52, O.4 lower 53–54 located only. No new image. |

### Assumptions and mature comparisons retained

Section 6 uses **nonnegative gains relative to a genuine zero reference**, not positive-loss capital-risk notation. Homogeneous RDU assumes bounded total payoff, normalized concave increasing utility linear over a small-payoff interval, continuous weighting concave first/convex later, and concave-majorant contact on **[0,1/n]**. Agent count and contact range matter.

The small-payoff proof separates an **upper bound** from **attainment by one feasible allocation**: an independent equal-probability jackpot works across thresholds. This is not free interchange of optimization and integration. Strict comparison with proportional sharing needs extra curvature/contact/positive-payoff conditions. General RDU Pareto characterization or utility-set convexity is not established.

The opposite large-payoff comparison needs uniform weighting-ratio and utility-asymptotic conditions, with payoff above a large threshold **state by state**, not merely in expectation. Local shifted gambles need separate differentiability, positive utility slope and weighting conditions. A dominated pure jackpot can coexist with an improving shared gamble. These are source comparisons, not new counterexamples or computed thresholds.

Proposition 7 gives a **special constant-supply equilibrium** within the linear interval, with endowment means in the contact range, not arbitrary-endowment or heterogeneous-RDU existence. O.6 already relaxes linearity using utility-to-payoff ratios and emphasizes majorant contact. O.7's bounded nonpositive EU counterparts use scapegoat structures, not general mixed-sign RDU or arbitrary short selling.

Proposition 5 mixes joint-law copies through an independent event: **EU is affine in probability mixtures**, unlike general RDU or statewise averaging. Its zero-weight route retains normalized strictly increasing preferences, feasible nonnegative transfers and total conservation. O.3.1 retains measurable-selection qualifications. Combining a subgroup envelope with a concave resource value may yield neither convexity nor concavity in their aggregate split. Source endpoint/interior examples certify no general local solver. O.3.3's satiation case differs from strictly increasing utility. Social weighted utility is not automatically cash welfare.

No full-paper/all-proof certificate: external order, Choquet, separation, selection and empirical originals remain unread. Boundary/strictness/randomization details and numerical constructions remain uncertified. No source example, curve, threshold or solver was recomputed.

## 2. Ghossoub–Zhu–Chong: selected formal body, new edition of an existing principal

**Mario Ghossoub, Michael B. Zhu and Wing Fung Chong, “Pareto-optimal peer-to-peer risk sharing with robust distortion risk measures.” ASTIN Bulletin 55(3), 537–563 (2025)**, [DOI 10.1017/asb.2025.6](https://doi.org/10.1017/asb.2025.6). [Actual Cambridge PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F04D6A2C302019B2063196B49C4819D0/S0515036125000066a.pdf/div-class-title-pareto-optimal-peer-to-peer-risk-sharing-with-robust-distortion-risk-measures-div.pdf): **27 physical pages, 878,381 bytes**, SHA-256 **7aa8fe9635d3801117d2a546e540918ac10b3f8bb4c4a86dbb318877ed0f4096**.

Title page: received **24 September 2024**, revised **31 January 2025**, accepted **11 February 2025**, online **11 March 2025**; issue September 2025. This new selected formal-body evidence does not rewrite the earlier v1 record or certify edition equivalence.

### Original synthesis — 107 words

<!-- SYNTHESIS_2_START -->
The formal article retains bounded, comonotone peer-to-peer contracts and distinguishes fixed participant beliefs from distortion-family ambiguity. Theorem 3.3 gives necessary conditions, while the ordinary singleton Corollary 3.4 gives an equivalence. Its centralized-market Proposition 4.3 adds robust closed, convex and pointwise-compact distortion families, an ES insurer, a joint worst-case existence result and necessary optimality conditions. This differs from the ordinary-distortion equivalence recorded for the preprint passage. The formal numerical section explicitly does not investigate robustness: it retains ordinary distortions, historical equally weighted monthly states and parameter-dependent welfare comparisons with reversals. Selected formal statements now have body evidence, without certifying full proofs, version equivalence, numerical reproduction or out-of-sample performance.
<!-- SYNTHESIS_2_END -->

### Actual formal scope and logical boundaries

**222:** physical **1** identity/dates/license screened; **4–8** model/IR/Pareto, Proposition 2.6/Definition 3.1/Lemma 3.2 statements, Theorem 3.3/commentary, Corollary 3.4/short proof; **lower 11–13** motivation/Proposition 4.3 statement/Remark 4.4/scenario assumptions; **17** Table 3/comparison/conclusion located and inspected. **No new image.** A separate identity/location record documents images **1, 6, 8, 13, 17**, distinct from 222's reading record.

Comonotone admissible contracts and cash constants remain. Fixed beliefs are not an estimated law-ambiguity set. **Theorem 3.3(ii) remains necessary**; its worst tuple has no general closed form. **Corollary 3.4 is iff for ordinary singleton measures**, not arbitrary robust families or unrestricted contracts.

**Proposition 4.3 differs in the selected statements.** The v1 passage concerned ordinary preferences and an iff. Formal **12–13** assumes policyholder families **closed, convex and compact under pointwise topology**, with an ES insurer: joint worst-case existence and a **necessary condition for optimal contracts**, for every solving tuple. Remark 4.4 adds compactness discussion/a finite-family convex-hull example. Formal proof unread; existence is not a computed tuple, contract or sufficient numerical certificate.

Formal **lower 11–upper 12 explicitly does not explore numerical robustness**: the illustration uses ordinary distortions/Corollary 3.4. Page 13 retains **553 equally weighted monthly states, January 1978–January 2024**, with specified preferences. Table 3 on 17 retains ranking reversals. This is not an ambiguity-set evaluation, holdout or trading return. Tables were inspected, not reproduced; cells, schema, data/license, code and calculations remain unverified.

Other formal body, Appendix A and external proofs remain unread/uncertified. This is no comprehensive edition comparison. Title-page **CC BY 4.0** does not establish third-party data/code rights. No source PDF, image, substantial passage, observations or programs are redistributed. No new principal, final topic or design is established; no empirical result was reproduced here.
