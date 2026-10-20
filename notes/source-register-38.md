# Source register 38 — vector robust control and selected control-proof increments

**20 October 2026. Literature phase.** This register adds **one new principal article** and records additional selected reading of **two articles already registered**. Reading blocks and formal-publication metadata are not separate paper counts. An additional foundation is listed only as a metadata/access boundary. The note contains original synthesis, not a completed design, financial experiment or empirical result.

## 1. New principal: vector-valued robust stochastic control

**Igor Cialenco and Gabriela Kováčová, “Vector-valued robust stochastic control,” arXiv:2407.00266v1**, DOI [10.48550/arXiv.2407.00266](https://doi.org/10.48550/arXiv.2407.00266). The actual body read is the **[fixed v1 preprint](https://arxiv.org/pdf/2407.00266v1)**, 26 physical pages. The recorded [version check](https://arxiv.org/abs/2407.00266v1) identifies the first/only deposit as **29 June 2024**; the PDF says first circulated and this version **28 June 2024**. These are different date fields.

Separately verified formal metadata: **“Vector-Valued Robust Stochastic Control,” SIAM Journal on Financial Mathematics 17(3), 770–800 (2026), DOI [10.1137/24M1673930](https://doi.org/10.1137/24M1673930)**. The official publisher history reports submitted 3 July 2024, accepted 23 February 2026, online 14 July 2026, issue September 2026. The [official article metadata](https://epubs.siam.org/doi/abs/10.1137/24M1673930?journalCode=sjfmbj) and [issue contents](https://epubs.siam.org/toc/sjfmbj/17/3) establish publication, not body reading. The formal PDF, accepted manuscript and supplement were not obtained or compared. No formal-edition theorem numbers, assumptions, page scope or PDF fingerprint are certified.

**Original source synthesis — 141 words.**

<!-- SYNTHESIS_1_START -->
Cialenco and Kováčová formulate finite-horizon robust control with vector losses and preorder-compatible ideal points. A finite dominated model family, compact actions, integrability and explicit supremum existence are substantive premises. Coordinatewise worst losses may arise from different models, so an ideal vector need not be one attainable scenario. Weak Bellman statements give inclusions; the stronger relations require the stated rectangularity and order conditions. Componentwise upper-image results retain closure and the requirement that one policy serve every model. Selected definitions, supplied local arguments and finite-tree illustrations were read in the 2024v1 preprint. Portfolio criteria already motivate the framework, but detailed market-data implementation is expressly outside that edition. Neither a sampled model grid nor statistical confidence alone establishes rectangularity. External foundations and independent proof correctness remain unverified. The 2026 publication metadata is confirmed separately; its body, changed assumptions and correspondence with v1 remain unread.
<!-- SYNTHESIS_1_END -->

### Actual selected scope of the 2024v1 body

| Reading block | Selected physical pages and content | Visual and unread boundary |
|---|---|---|
| 182 | 1–11 through the feasible-image value definition, before the continuation of Remark 3.1: introduction, standing model, Sections 2.1–2.3, Definition 2.2, Lemmas 2.3/2.5/2.6/2.8/2.9 with supplied arguments, Example 2.4 and Assumption 1. | Source Figures 1 on page 6 and 2 on page 8 visually inspected. Conditional-cone details, all literal examples and external originals were not independently certified. |
| 183 | 12–18 before Section 4: Sections 3.1–3.2, Theorems 3.2/3.3 and 3.6/3.7/3.8 with supplied arguments, Definition 3.4 and Remark 3.5. | Selected statements and supplied proof routes, not independent certification of every literal proof or external theorem. No additional page-image inspection is claimed for this block. |
| 184 | Section 4, from its heading on 18 to before Section 5 on 21: Lemmas 4.1/4.4, Corollary 4.6, Definition 4.3 and Proposition 4.7 with supplied proof. | Closure, topology and attainment steps are not independently certified. The later example passages are recorded in the next block rather than counted twice. |
| 185 | Section 5 on 21–23 before Acknowledgment: Table 1/Figure 3, Table 2 and original-versus-recursive vectors, then Example 5.2's portfolio discussion. References 24–26 located for direct dependencies only. | Original pages 21 and 22 visually inspected. Tables 3/4 on 23 located in text; no recalculation or code execution. External reference bodies unread. |

The vector order is part of the model. A compatible preorder need not be antisymmetric, and even a finite model family does not ensure that every required ideal point exists under an arbitrary preference cone. The selected setup explicitly imposes existence. Uniqueness under a partial order and the source's sufficient geometric construction are separate qualifications. The feasible-image value is not asserted to contain only efficient controls.

The one-step construction uses actual future feasible-image values; the backward construction instead uses its own continuation sets. Weak relations are inclusions. The extra rectangularity relation concerns the relevant nested conditional expectations across the model family, rather than one observed path or one numerical model grid. It supplies the reverse relations; exact feasible-image equality additionally retains the stated antisymmetry condition. Replacing one fixed unknown path law with successive adverse conditional choices can change the model class.

For componentwise order, the ideal point takes coordinatewise maxima. Different coordinates may be worst under different laws. The upper image is a closure of feasible values plus the positive cone; limiting bounds must not be silently treated as attained objective vectors. The condition that one policy works for every candidate model differs from choosing a separate optimal policy for each model.

The finite-tree illustration already contrasts a rectangular eight-model family with a nonrectangular four-model subset. Its reported recursive and original values illustrate the distinction; they were not independently recomputed here, and the example omits controlled dynamics. The portfolio discussion already mentions multiple markets/currencies/preferences and possible trading constraints. It leaves detailed market-data numerical implementation outside the read 2024 edition. No claim about the unread 2026 edition's empirical content follows.

## 2. Increment to the portfolio article already in register 37

**Theerawat Bhudisaksang, Álvaro Cartea and Leandro Sánchez-Betancourt, “Adaptive-Robust Portfolio Optimisation,” Mathematics and Financial Economics 20, 171–202 (2026), DOI [10.1007/s11579-025-00411-4](https://doi.org/10.1007/s11579-025-00411-4).** The actual source remains the same **[published PDF](https://link.springer.com/content/pdf/10.1007/s11579-025-00411-4.pdf)**, 32 physical pages. The [publisher record](https://link.springer.com/article/10.1007/s11579-025-00411-4) identifies acceptance 4 December 2025, online/version of record 16 December 2025 and issue March 2026.

Register 37 had selected physical 1–22, including Appendices A–B, while leaving C–H uncompleted. Blocks 178–179 add the following selected appendix reading of that **same article and edition**. They do not create another principal entry or retroactively enlarge register 37's earlier scope.

**Original incremental synthesis — 137 words.**

<!-- SYNTHESIS_2_START -->
Additional reading completes selected appendices of an already registered two-asset adaptive-robust allocation paper. The supplied box-drift optimization separates nine control regions around a common learning-gradient shift. A central region therefore need not imply zero total holdings or a transaction-cost no-trade band. Gaussian truncated-moment calculations and differentiated transition expressions support the representation under known covariance and the stated unconstrained control model. The small-width expansion uses local, time/state-dependent integrable bounds; uniform accuracy across arbitrary states, correlations or finite widths is not inferred. Appendices C–H and the materials statements were selected-read, without independent certification of every case or boundary. Simulated datasets are offered through the corresponding author, rather than acquired here. The article's licence does not establish public code availability or independent rights to third-party materials. These are mature analytical tools, not historical profitability evidence or a new project method.
<!-- SYNTHESIS_2_END -->

| Added block | Actual selected scope | Visual and remaining boundary |
|---|---|---|
| 178 | Appendix C.1–C.3, physical 23–26: candidate cases, common learning shift, comparisons and reported nine-region forms. | Original images 23, 24, 25 and 26 inspected. Every case label, coefficient, algebraic identity and global verification premise was not independently certified. |
| 179 | Appendix D–H, physical 27–31 before Data Availability, followed by the actual materials/licensing statements. | Original images 27, 28, 29, 30 and 31 inspected. Literal rate/root/remainder claims and all boundary cases were not independently certified. Page 32 references were not audited; external 2021 verification/estimation foundations remain body-unread. |

The model already uses two risky assets, known covariance/loadings, unknown drifts and learning with exponential utility. Its unconstrained money controls allow shortselling and exclude transaction costs. The relevant sign regions involve a control together with the transformed value's learning gradient. They cannot be interpreted solely from the estimated excess-return sign. Altering holding constraints, imposing fees or clipping the unconstrained result requires a new justified control calculation.

The appendix calculations use Gaussian transition moments. They do not directly supply formulas for uncertain volatility, arbitrary heavy tails or an empirical conditional law. The small-uncertainty expansion specializes to zero correlation, as already recorded in register 37. Its time/state-dependent threshold and integrable envelopes are not a uniform finite-width approximation over all states and parameters. At the conditioning-time endpoint, transition variance degeneracy is a real qualification for an implementation, which was not undertaken.

The selected page 31 statement offers simulated datasets from the corresponding author; no request or acquisition occurred. The article states CC BY 4.0 with a separate condition for third-party material. This does not establish the availability of unprovided executable code or unrestricted rights to every underlying material. Source simulations remain author-reported evidence, not historical-market holdouts, net execution returns or project computations.

## 3. Increment to Bayraktar–Chen already in registers 35–36

**Erhan Bayraktar and Tao Chen, “Nonparametric Adaptive Robust Control Under Model Uncertainty,” arXiv:2202.10391v3**, DOI [10.48550/arXiv.2202.10391](https://doi.org/10.48550/arXiv.2202.10391). The actual source remains the **[fixed v3 preprint](https://arxiv.org/pdf/2202.10391v3)**, 24 physical pages: first deposit 21 February 2022, v3 deposit 21 March 2022 and PDF title date 23 March 2022.

Registers 35–36 already recorded this source and left Proposition 2.3's proof uncompleted. Block 181 adds selected physical **6–8**, focusing on Proposition 2.3's supplied proof, the surrounding Wasserstein topology/augmented transition statement, and feedback-control/path-law formulation immediately below. **No new preview was rendered.** Lemma 2.2 is contextual, not independently certified.

The previously verified [formal record](https://epubs.siam.org/doi/10.1137/22M1481609) is SIAM Journal on Control and Optimization 61(5), 2737–2760 (2023), DOI 10.1137/22M1481609, online 12 September 2023. Its body remains unread; this added proof scope belongs to v3, not the final article.

**Original incremental synthesis — 134 words.**

<!-- SYNTHESIS_3_START -->
This incremental reading addresses the previously uncompleted transition-kernel argument in Bayraktar–Chen's 2022v3 preprint. The state joins a physical coordinate with an empirical law in first-Wasserstein space. The supplied Proposition 2.3 route uses the continuous combined update and properties of innovation preimages to obtain the reported kernel measurability. Closed bounded innovation subsets in that argument do not make arbitrary Wasserstein balls compact. Feedback controls and model selectors subsequently use the kernel to define path laws. These are foundations for control formulation, not confidence calibration, numerical accuracy or investment-performance guarantees. The new selected scope is physical pages 6–8, with no new page rendering. An iid radius cannot inherit serial-dependence validity from kernel measurability, and a moment-compressed state needs separate justification. The final 2023 article remains body-unread; neither edition equivalence nor every literal proof step is certified.
<!-- SYNTHESIS_3_END -->

The empirical-law update matters to the supplied argument: restricting the updated law constrains the corresponding innovation preimages. This is not a maintained bounded-support condition on every shock. A well-defined kernel does not validate arbitrary distribution truncation, an iid confidence radius for serially dependent returns, or replacing the full empirical-law state by a few moments without further analysis. Earlier numerical moment compression remains an approximation, rather than an implication of Proposition 2.3.

## Metadata/access boundary only: the continuous-time foundation

**Theerawat Bhudisaksang and Álvaro Cartea, “Adaptive Robust Control in Continuous Time,” SIAM Journal on Control and Optimization 59(5), 3912–3945 (2021), DOI [10.1137/20M1336680](https://epubs.siam.org/doi/10.1137/20M1336680).** The saved official/indexed record identifies submission 7 May 2020, acceptance 19 July 2021 and online publication 21 October 2021. The recent portfolio article cites its Proposition 2.19.

Block 180 is **metadata/access evidence only, original body 0**. The targeted [Oxford repository record](https://ora.ox.ac.uk/objects/uuid%3Add9dc8fb-2c60-40bb-bab8-504e675e0d01) returned 403; that route was closed without retry, direct-file follow or mirror. An indexed first-page excerpt is not a theorem or proof reading. No original PDF was obtained, so no actual page scope or file fingerprint is supplied. Its DPP/HJB, verification assumptions, execution example and equivalence with an earlier edition remain unverified. This source is not confused with the different Chen–Ludkovski 2021 article.

## Mature methods and financial-transfer boundaries

| Distinction | Retained implication |
|---|---|
| Vector criterion versus scalar objective | A weighted scalarization, a preorder ideal point, a feasible image and an upper image represent different decisions. Relabelling one does not supply another formulation's guarantee. |
| Existence versus calibration | Existence of an ideal point, a measurable kernel or a Bellman representation does not calibrate a statistical uncertainty region. |
| Rectangularity versus finite model enumeration | A finite collection or a model grid is not automatically closed under the conditional combinations required by the source. |
| Learning adjustment versus a no-trade band | A thresholded component can coexist with a nonzero learning shift. Introducing trading costs or constraints changes the control problem. |
| Local expansion versus uniform approximation | State/time-dependent integrable control is not a uniform finite-width guarantee over unrestricted parameters or states. |
| Supplied proof versus complete verification | Selected local arguments retain external assumptions, edition boundaries and uninspected steps. They are not independent correctness certification or executable formulas. |
| Simulation or toy tree versus financial evaluation | Source examples do not establish historical profitability, market calibration, transaction-cost performance or a project replication. |

The articles already cover learning, robust allocation, vector criteria, geometric uncertainty and dynamic recursion. New assets, a different solver, a new label or another model grid alone do not establish a methodological contribution. Any later transfer still needs a specific financial target, the correct information sequence, compatible assumptions and a separate evaluation protocol. No such design is locked here.

## De-duplication, retained fingerprints and materials status

Registers 01–37 were checked by titles, authors and DOI/arXiv identifiers. The recent portfolio article is already in 37; Bayraktar–Chen is already in 35 with an increment in 36. Cialenco–Kováčová had no prior principal entry. Blocks 182–185 and its final-publication metadata check therefore add **one** article, not five. The similarly titled Bielecki–Chen–Cialenco–Cousin–Jeanblanc predecessor is a separate source and is not merged with the nonparametric paper.

The three retained original PDFs were rehashed and matched their saved records. Hashes identify actual editions, not equality with unread final versions, proof correctness, market-data vintages or executable implementations.

| Actual original body | Physical pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Cialenco–Kováčová, arXiv2407.00266v1 | 26 | 923929 | f01d1dca8fd918a2023013df54d53a815338ba900998f11d4b222165a988d1f9 |
| Adaptive-Robust Portfolio Optimisation, published version | 32 | 776708 | 96958b32db72730d9c9323f273683e32d2299df2799ff84d6bf5473093408d6c |
| Bayraktar–Chen, arXiv2202.10391v3 | 24 | 556492 | c8017e71cd0dc8384a51f1611eac8a63bf173a9a0d768385e997be185728cae5 |

This administrative curation adds zero original-body reading credit. It obtains no observation data, programs or software and creates no fitted model, simulation, financial experiment or measured computational result. Data/code availability and reuse rights not explicitly verified above remain unknown. No source PDF, figure, raw dataset or substantial source passage is redistributed.
