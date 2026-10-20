# Source register 33: continuous causal sensitivity and martingale hedging

Reading update, 20 October 2026. This register adds selected proof and application depth for two previously encountered sources. It does not count them as newly discovered papers or certify either entire article. The project remains in literature review; no final question, experimental specification or empirical result is selected.

## 1. Jiang–Obłój: continuous scaling, derivatives and information

Yifan Jiang and Jan Obłój, *Sensitivity of causal distributionally robust optimization*, arXiv **2408.17109v2**, DOI **10.48550/arXiv.2408.17109**. First deposit 30 August 2024; selected revision 27 May 2025. [Official version record](https://arxiv.org/abs/2408.17109v2), [original PDF](https://arxiv.org/pdf/2408.17109v2). No journal identity or popularity claim is inferred.

The preceding register covered selected discrete results and the generic sensitivity argument. This update reads the continuous constructions and selected supplied dependencies:

| Original physical pages | Newly inspected scope |
|---|---|
| 8–10, 13–15 | Derivative domains, hyperbolic scaling, Theorem 4.11 and examples |
| 15–17 | Parabolic martingale sensitivity, Theorem 4.17 and examples |
| 23–29 | Selected supplied continuous upper/lower arguments and forward-integral correction |
| 30–33 | Derivative-extension and selected stochastic-Fubini auxiliary proofs |
| 17–19 | Section 4.3 extension discussion, with its stated and omitted proof boundaries |

Hyperbolic scaling controls absolutely continuous displacement energy. The parabolic construction instead uses quadratic-variation cost, a Wiener reference and regular martingale alternatives. Their derivative domains, payoff growth and moment/integral-interchange conditions differ. A grid becoming finer does not alone verify either theorem or make their limits interchangeable.

The parabolic coefficient retains a diagonal correction associated with the stochastic-integral integrand. Selected supplied proofs explain why forward integrability and stochastic Fubini appear. Reading those arguments does not establish numerical discretization rates or remove their regularity assumptions.

The extension discussion changes information sets, conditional-law objectives and drift/martingale budget geometry. Separate budgets and a shared quadratic budget produce different coefficient combinations in the source's setting. Some extension details are omitted; external original calculus, weak-transport and coefficient-ambiguity results were not independently established here. A source statement about a question open in this revision is not a current universal novelty certificate.

The 37-page local source fingerprint is SHA256 `2af2a563210d3fd846cc8fbff0fff6a7d8b31249b78ec9750f8e2c13e20a490a`. The PDF and third-party figures are not redistributed.

## 2. Sauldubois–Touzi: local model risk and available hedges

Nathan Sauldubois and Nizar Touzi, *First order Martingale model risk and semi-static hedging* in the record; *First-order Martingale model risk and semi-static hedging* on the PDF. arXiv **2410.06906v3**, DOI **10.48550/arXiv.2410.06906**. First deposit 9 October 2024; selected revision deposited 21 September 2026; PDF title date 23 September 2026. [Official version record](https://arxiv.org/abs/2410.06906v3), [original PDF](https://arxiv.org/pdf/2410.06906v3). These dates are distinguished; no attention or venue claim is made.

Earlier selected main-text reading is consolidated with the following local proof depth:

| Original physical pages | Inspected scope |
|---|---|
| 3–9, 18–25 | Setup; adapted and ordinary martingale sensitivity; selected supplied linearization, projection, density-deformation and approximation proofs |
| 9, 25–27 before Section 6.5 | One-dimensional quadratic Fredholm characterization and supplied local proof |
| 10–11, 27 Sections 6.5–6.6 | Exact first-marginal constraints, static/dynamic hedges and stopping extension |
| 12–14 before Section 5 | Optimized law-functional and convex-concave game examples with supplied envelope arguments |
| 14–18 before Section 6 | Model illustrations and original Figures 1–9, inspected rather than reproduced |

The reference is a two-date martingale law with finite moments. The criterion may be a differentiable functional of that law. The adapted first-order hedge minimizes an adjusted adapted-gradient norm. The supplied lower construction uses a martingale perturbation and an imported bicausal approximation. The result matches robust upper/lower derivatives at zero; it is not finite-radius equality or an empirical trading-performance guarantee.

The ordinary-distance result retains density, support, weighted-space and approximation assumptions. The hedge controls both holdings and their derivative. An empirical discrete distribution does not itself meet the density condition. The Fredholm characterization adds one-dimensional quadratic specialization, compact support, positive weights and a separate nondegeneracy condition for its representation. Continuous solvability does not establish discretization or estimation stability.

The first-marginal extension assumes exact distributional calibration and a rich static-payoff class. Finite option quotes are a different information set. The stopping extension retains smooth adapted costs and a unique reference optimizer; its supplied short proof imports an earlier stopping argument. The source's optimized-value examples also distinguish robustification order: first-order agreement does not silently exchange finite-radius decision and distribution optimization.

The option examples use stylized Black–Scholes/Bachelier references. Vega and transport sensitivity have different perturbation units. No market observations, underlying numerical output, author code, confidence-band procedure or runtime were independently reproduced. Imported original functional-analysis, approximation, stopping and minimax foundations remain outside the independently checked chain.

The 29-page source fingerprint is SHA256 `80868f3d986402454ef4d33f99ed173999dc65ef6f62aff867c0a165e6f6b804`. Source PDFs and figures stay local.

## 3. Consequences for the literature comparison

| Object | Distinction retained for any later application |
|---|---|
| Transport cost | Jiang–Obłój's discrete increment cost and Sauldubois–Touzi's price-level cost do not share numerical radius units automatically. |
| Local robustness | A derivative at zero is separate from a finite-radius worst-case value, estimated-law uncertainty and realized hedging performance. |
| Reference law | A historical return distribution is not automatically a pricing martingale; accurate estimation alone does not identify a pricing measure. |
| Financial prior work | Sauldubois–Touzi explicitly acknowledges Jiang–Obłój as an independent direct neighbor for the linear-functional adapted result. Generic first-order projection is established prior work. |
| Potential transfer | A different payoff, asset or dataset must satisfy the actual source conditions and answer a distinct financial question. Substitution alone is not a new method. |

This register records primary-source understanding and its limits. It supplies no project theorem, repaired proof, calibrated radius, measured experiment or completed manuscript. Raw observations and software were not acquired for these readings; source and data reuse permissions are not inferred from free access.
