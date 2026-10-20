# Source register 31 — Selection proofs and structural risk assumptions

20 October 2026. This update deepens two sources already introduced in register 03. It adds selected proof and application reading, not two newly discovered papers. Literature review continues; no project topic, empirical specification or result is selected here.

## 1. Sequential coverage-constrained selection

Jing Li and Haibin Zhu, *Sequential Confidence Sets for Coverage-Constrained Conformal Model Selection*. [Official record](https://arxiv.org/abs/2609.28522v1), [versioned original](https://arxiv.org/pdf/2609.28522v1), arXiv 2609.28522v1, submitted 22 September 2026; DOI 10.48550/arXiv.2609.28522.

**Additional actual scope:** Appendix B.2–B.4, physical PDF pages 29–34 before B.5; main pages 10–11 rechecked for assumptions. Images 29 and 32 inspected. Earlier B.1/B.5 and delayed-feedback reading is not counted again.

**Original synthesis:** The inspected proofs distinguish rectangular-set geometry from statistical independence. A common confidence event retains the true constrained optimum over time, but membership in the possible set does not certify feasibility. The finite-stopping statement controls a joint failure event, rather than failure conditional on stopping. Identification additionally needs persistent exposure and feasibility margins or suitably cheaper strictly feasible competitors. The target is prefix-average conditional miscoverage with predictable costs; an unbounded financial loss target does not follow automatically. Financial assets, horizons and delayed feedback alone therefore do not establish a new generic method. External confidence-boundary foundations, complete empirical implementation and full proof correctness were not independently certified in this follow-up.

## 2. Wasserstein and unimodal distortion risk

Peng Liu, Steven Vanduffel, Yi Xia and Jing Yao, *Robust Distortion Risk Metrics with Wasserstein and Unimodal Constraints*. [Official record](https://arxiv.org/abs/2511.08662v2), [versioned original](https://arxiv.org/pdf/2511.08662v2), arXiv 2511.08662v2; DOI 10.48550/arXiv.2511.08662. First deposit 11 November 2025; revision deposit 27 September 2026; PDF title date 29 September 2026.

**Additional actual scope:** Selected main pages 16–29; Appendix B pages 40–46 from Proposition 2 through Proposition 5, and Appendix C's Proposition 6 route. Selected original images inspected. Appendix A, external projection/lifting proofs and formula-level numerical implementation remain outside this follow-up.

**Original synthesis:** Fixed-shape projection requires nonconstant projected weights; normalization stability is distinct from weight approximation. Exact moments and shape determine a feasibility floor before a Wasserstein multiplier problem becomes meaningful. Unknown turning probabilities form a nonconvex union already treated in the paper. Its separate portfolio application uses prescribed moments and reference laws, with two-asset synthetic illustrations. Elliptical simplification retains nonconvex optimization subproblems. These structural results do not calibrate financial sampling uncertainty or establish realized investment gains. The supplied local proof routes were read without independently certifying all external premises or numerical global convergence. Changing assets or repeating a radius sweep alone would not establish methodological novelty.

## Source fingerprints and reading status

| Retained original | Physical pages | Bytes | SHA-256 |
|---|---:|---:|---|
| 2609.28522v1 | 71 | 2,868,037 | `6515bff1162b088ce941fde5d208b79822da3463c2ef49a8657bb99bda4ee91f` |
| 2511.08662v2 | 47 | 787,124 | `2c9e58bd80400d7143cdb9138fa12c641c51a4b6476fd14f20c0044e81cad8ff` |

The originals are retained locally for provenance and are not redistributed here. Selected passages and supplied proof routes are distinguished from complete-paper reading, independent proof verification and executed computations. No market observations, packages, experiments or author code were obtained in this batch; data/code redistribution permission has not been inferred from public reading access. Recent versions are described by their verified dates, without unsupported popularity claims.

## Consequence for this research

The next comparison must separate the financial decision being studied, the population assumptions, the statistical guarantee and the computation actually required. A source's existing application or proposed future-work sentence is evidence to investigate, not sufficient evidence of an open contribution. Potential transfers remain candidates until their closest work, assumptions and accessible data have been checked. No experiment has been used to select a favorable specification.
