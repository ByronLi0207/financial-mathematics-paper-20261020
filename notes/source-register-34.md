# Source register 34: coefficient uncertainty and baseline hedging

20 October 2026. This follows the drift/volatility-uncertainty reference in the preceding causal-sensitivity reading. One principal source is upgraded from reference-entry knowledge to selected original-body and supplied-proof reading. It is not a full independent certification of the article or its external theorem chain. Literature review continues; no final project question, empirical specification or manuscript result is selected.

## Original edition and actual reading

Daniel Bartl, Ariel Neufeld and Kyunghyun Park, *Sensitivity of robust optimization problems under drift and volatility uncertainty*, arXiv **2311.11248v2**, DOI **10.48550/arXiv.2311.11248**. First deposit 19 November 2023; selected revision deposited 24 February 2025; actual PDF date 25 February 2025. [Official version record](https://arxiv.org/abs/2311.11248v2), [original PDF](https://arxiv.org/pdf/2311.11248v2). The edition dates are distinguished. No journal identity, citation count or popularity signal is inferred.

| Original physical pages | Inspected scope |
|---|---|
| 1–11 before Section 3 | Positioning, coefficient/control spaces, main assumptions, adjoint representations and Theorems 2.13/2.14 |
| 11–13 before Section 4 | Mean-square hedging example and primal/dual characterization |
| 13–17 before Section 4.2 | Supplied uniform-moment, GKW and adjoint-input arguments |
| 17–23 before Section 4.4 | Supplied control/adjoint stability, optimizer existence and feasible first-order condition |
| 23–34 before Section 5 | Supplied linear representation, Taylor/support bounds, near-optimizer and sensitivity-limit arguments |
| 34–37 before references | Selected auxiliary conditions, smooth-state representation and separate envelope proof |

Original formula pages were also visually inspected. Every literal identity, all constants, exact remainder order and external foundational proofs are not independently certified. References were selectively followed rather than fully audited.

The retained 41-page official PDF is 621041 bytes, SHA256 `ec3f790ad98ba358126852943cfa102f4ced84be0cf39fc68d7db0c7b9cc2d2e`. It remains local; no source PDF or third-party figure is redistributed.

## Original synthesis

The source perturbs predictable drift and volatility coefficients on one fixed filtered probability space. Drift and volatility have separate moment-norm budgets, scaled by aversion weights. An admissible holding is evaluated across these coefficient alternatives before the outer optimization. This differs from an arbitrary path-law transport ball and does not automatically mean a feedback rule is recomputed under each alternative.

Its main assumptions include finite **p>3** coefficient moments, invertible baseline volatility, an appropriately integrable change-of-measure density, a uniformly bounded closed convex predictable holding class, and smooth controlled costs and terminal liability. Cost curvature and growth are tied to p. Introductory financial motivation does not waive this conjunction for a particular application.

The first-order coefficient uses two adjoint families. One reflects wealth and running marginal cost; the other reflects the terminal liability's dependence on the asset. A general filtration may retain a Brownian-orthogonal martingale. Conditional expectation/covariation representations are analytical objects, not fitted estimators or ready numerical algorithms. The additional smooth finite-state representation has stronger conditions.

The source states a local robust-value expansion with a quadratic-order remainder and a local value-gap result for retaining the exact reference optimal holding. Selected supplied proofs combine uniform moment estimates, Taylor expansion, an adjoint linear form, predictable perturbation directions and reference-optimizer stability. Reading the provided route does not yield an independently verified finite numerical error constant. Local value comparisons are separate from exact finite-radius optimality, closeness of computed holdings and realized market performance.

The mean-square hedging example minimizes squared terminal target error plus convex quadratic running cost. It is distinct from a mean–variance return portfolio frontier. A quadratic holding term is not automatically transaction cost or turnover. The example uses a constrained primal/dual stochastic-system characterization; no computational complexity or small-memory guarantee follows from that representation.

## Conditions that affect a financial transfer

| Issue | Source boundary retained |
|---|---|
| Information and decisions | Fixed filtered space and predictable holdings; a strategy perturbation and a coefficient perturbation are different operations. |
| Constraints | A feasible directional inequality remains important at a constrained optimum; unrestricted zero-gradient stationarity is not substituted. |
| Growth and stability | Uniform moment and boundedness conditions support the optimizer/adjoint passages. A low sample error does not verify population assumptions. |
| Time consistency | Remark 2.15 explicitly says the finite-p global-budget problem is not time-consistent. A proposed essentially-uniform extension is not adopted as a proved main result. |
| Nearest causal comparison | Jiang–Obloj compares a restricted deterministic-control setting and formally substitutes p=2 in an expression. The original main theorem here retains p>3; its range is not extended by that comparison. |
| Error sources | Model-radius approximation, statistical estimation and numerical approximation require separate evidence. The coefficient budget is not calibrated from observations by these theorems. |

Generic coefficient sensitivity, baseline-hedging envelopes and mean-square financial applications are therefore existing prior work. A different asset, liability or dataset would need a distinct question and verified conditions; substitution alone is not a methodological contribution.

Imported originals for Girsanov/Novikov, Benes and density moments, measurable correspondences, GKW/BSDE, predictable process-space duality, stochastic maximum principles and regularity remain outside this independently checked chain. Author code availability, data licensing and implementation resource use were not established by these passages. No absence or permission claim is inferred.

Only the official literature PDF was acquired for private reading. No financial observations, author program, package installation, stochastic simulation, solver result or measured experiment was produced for this register.
