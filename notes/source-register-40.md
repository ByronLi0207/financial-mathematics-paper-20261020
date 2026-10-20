# Source register 40 — rectangular laws and Gaussian empirical transport

**20 October 2026. Literature phase.** One new principal plus one existing-article increment. Blocks, metadata and proof sections are not additional papers. No design or financial experiment is selected.

## 1. New principal: Shapiro's rectangular-law manuscript

**Alexander Shapiro, “Rectangular sets of probability measures.”** Actual body: [author manuscript](https://optimization-online.org/wp-content/uploads/2014/10/4613.pdf), **24 physical pages**; physical 1 is title, physical 2 starts printed 1. Internal manuscript date **unknown**.

| Source evidence | Exact identity and boundary |
|---|---|
| [Repository record](https://optimization-online.org/2014/10/4613/) | Posted **24 October 2014**, updated **13 October 2015**: record dates, not certified PDF dates/revisions. |
| [Formal DOI](https://doi.org/10.1287/opre.2015.1466) / [publisher metadata](https://pubsonline.informs.org/doi/abs/10.1287/opre.2015.1466) | *Rectangular Sets of Probability Measures*, Operations Research **64(2), 528–541 (2016)**. Received 1 December 2014; accepted 1 October 2015; online **15 February 2016**; issue **March–April 2016**. |
| Edition boundary | **2016 metadata only; final body unread.** Its pages, assumptions, numbering and equivalence are not the author-manuscript reading scope. |

**Original source synthesis — 132 words.**

<!-- SYNTHESIS_1_START -->
Shapiro studies when a family of probability laws admits a nested worst-expectation representation relative to a specified objective class. The representing set need not equal the original family; independent product laws are not automatically rectangular. Restricted convex objectives, bounded supports and prescribed means can change the conclusion. Selected author-manuscript arguments distinguish coherent risk representations, nested AVaR and law invariance, without establishing a universal static-versus-nested risk ordering. Stochastic-programming and control formulations use different decision-information timing, and controlled transitions can make law families policy dependent. The interchange result retains compactness, joint continuity, risk monotonicity/cash equivariance and an adequate approximate-selector class. Main passages, examples and supplied appendix routes were selected-read; imported duality, selection and probability results remain unread. The formal 2016 publication is metadata only. No financial data, implementation or complete proof/edition-equivalence certification is supplied.
<!-- SYNTHESIS_1_END -->

### Actual selected scope

| Block | Physical pages and selected material | Boundary |
|---|---|---|
| 191 | 1–10 before Section 3: Definition 2.1, Theorems 2.1/2.2 supplied routes, Theorem 2.3/Corollary 2.1, product/conditional constructions and Corollary 2.2. | Theorem 2.3 proof imported, not read. |
| 192 | Section 3, heading on 10–14 before Section 4: Examples 3/4, Definition 3.1, Propositions 3.1–3.3 and supplied transformation route. | Image **11** inspected; external originals unread. |
| 193 | Sections 4–5, 14–21 before Appendix 6: SP/control/MDP formulations, static/dynamic counterparts, policy-dependent laws. | External DPP and attainment/regularity details uncertified. |
| 194 | Appendix 6, 21–23 before Acknowledgment: Proposition 6.1 supplied proof, Remarks 3/4, finiteness branches. References 23–24 located. | External originals and literal topology/conditional-density/dual-space steps uncertified; no full-proof claim. |

### Conditions and financial interpretation

| Distinction | What remains substantive |
|---|---|
| Objective class / representing set | Representations may be nonunique. A representing set need not equal or contain the initial family; the maximal closed convex construction is distinct from self-rectangularity of the original set. |
| Independent product laws | Independence alone is insufficient for every objective. The common extremal product example needs known support intervals, prescribed means and restricted convex objectives. |
| Static / nested AVaR | Independent-product worst expectation and nested conditional AVaR are not generally ordinary terminal AVaR. Their inequality gives no universal nested-versus-terminal AVaR ordering. |
| Law invariance | Dual invariance retains transformation/reference-space/closure conditions. The restrictive result uses a particular finite equal-probability tree, branching and coherent conditional components, not every financial risk model. |
| Information timing | SP decisions can use current observations; the control action precedes the current innovation. Markov/independence reductions have their own premises. Financial signals must respect that lag. |
| Static / dynamic control | Conditional choices can enlarge a fixed-law/global-budget family. Action-dependent transitions yield policy-dependent laws. Bellman recursion does not grant unrestricted minimax interchange. |
| Interchange / finiteness | Compact scenario/action spaces, joint continuity, monotone cash-equivariant risk and uniform approximate pointwise selectors are substantive. Continuous-selector conditions and compact-continuous versus Lp/dual-density finiteness branches differ. |

Finite grids, bounded samples or clipped controls do not verify population support, selectors or dual-density bounds. Costs, holdings or learning may require additional state. No new reduction or financial implementation is supplied.

## 2. Gaussian increment to Boissard–Le Gouic, already in register 35

**Emmanuel Boissard and Thibaut Le Gouic (2014), “On the mean speed of convergence of empirical and occupation measures in Wasserstein distance,” Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 50(2), 539–563**, DOI [10.1214/12-AIHP517](https://doi.org/10.1214/12-AIHP517). Same **25-page published edition**: [official record](https://numdam.org/articles/10.1214/12-AIHP517/), [original PDF](https://www.numdam.org/item/10.1214/12-AIHP517.pdf). Received 22 July 2011; revised 16 February 2012; accepted 15 July 2012.

Blocks 152–157/register 35 covered independent error, tails, Markov and concentration arguments, leaving Gaussian gaps. Block 195 adds scope to **the same article/edition**, without rewriting earlier scope or adding a principal.

**Original incremental synthesis — 126 words.**

<!-- SYNTHESIS_2_START -->
The added Gaussian passages study empirical approximation of a fixed Banach-valued Gaussian law by iid draws, potentially entire paths. Theorem 1.4's infinite-dimensional rate requires its weak-variance and small-ball conditions, a sample-size threshold and distribution-dependent quantities. It is not a generic radius for an approximately Gaussian asset vector or a fitted financial model. The supplied route combines truncation, Gaussian isoperimetry and covering entropy. Lemma B.1 separately transfers a Gaussian transportation inequality through finite-dimensional maps and a weak limit. Independent concentration, expected approximation error and Markov occupation-measure bounds retain different premises. Selected statements and supplied routes were read; only page 5 received new visual inspection. External originals, usable numerical constants and full proof correctness remain unverified. Overlapping windows from one financial series are not automatically independent path draws.
<!-- SYNTHESIS_2_END -->

| New block 195 scope | Actual boundary |
|---|---|
| Section 1.2, lower physical 4–6, printed 542–544 | Theorem 1.4, quantization and process examples. |
| Section 3, from its heading on 15 through 17, printed 553–555 | Supplied truncation/entropy proof route. |
| Appendix B, lower 23 through 24 before Acknowledgments, printed 561–562 | Lemma B.1's Gaussian-series/pushforward/weak-limit route and alternative-proof remark. |
| Visual / external boundary | **Only original page 5** newly inspected visually. Page 25 references located only. External small-ball, isoperimetric, series, transport-stability and quantization proofs unread; constants, domains and literal algebra not independently certified. |

Theorem 1.4's infinite-dimensional premise is not established by an approximately Gaussian asset vector. Its threshold/constants depend on the small-ball function, doubling control and weak variance, not an automatically calibrated same-sample radius. Lemma B.1's transport inequality is distinct.

Whole-path iid sampling differs from overlapping windows. Parameter estimation, path discretization and approximation of a known law introduce different errors. Rate-optimal quantization is not optimal trading or exact optimal scenario weights.

Appendix A still needs independent sampling. Markov occupation bounds target an invariant/marginal law under separate premises; they do not inherit independent concentration or conditional/all-dates coverage.

## De-duplication, fingerprints and evidence limits

Registers 01–39 were checked by title/DOI. Shapiro is **one new principal**; Boissard–Le Gouic is already in 35. Block 195 does not retroactively complete earlier scope. Metadata adds no body credit.

| Actual retained original, rehash matched | Bytes | SHA-256 |
|---|---:|---|
| Shapiro, 24-page internally undated author manuscript | **366084** | **c6261700299a4a910b67e9efe86035387b3bbe2c9156dbd6e05f74d16e082841** |
| Boissard–Le Gouic, 25-page published edition | **292920** | **2eb3c92de6e111b23b2e280dc8d7dcbbc6cacc0e0774c72dcd47221d7cdbb531** |

Hashes identify files, not edition equivalence, proof correctness or executable formulas. No financial observations, programs, models or experiments were obtained/produced. Unchecked code/data rights remain unknown. No source PDF, figure, raw data or substantial passage is redistributed. Administrative **new body credit is zero**.
