# Source register 53: minimum-divergence scenario aggregation

Literature record, 20 October 2026. **One new principal.** Formal publication metadata are separated from the original-author representation actually selected for reading. No new theorem, empirical result or research design is established.

## Principal: Cambou and Filipović

**Mathieu Cambou and Damir Filipović.** *Model Uncertainty and Scenario Aggregation*. **Mathematical Finance 27(2), 534–567, April 2017.** DOI: [10.1111/mafi.12097](https://doi.org/10.1111/mafi.12097). The publisher records first online publication on **19 June 2015**.

| Identity / access field | Evidence and version boundary |
|---|---|
| Formal record | [Wiley article metadata](https://onlinelibrary.wiley.com/doi/10.1111/mafi.12097). Formal journal body remains unread; metadata access is not formal-body reading. |
| Author-institution record | [EPFL CSF publications](https://www.epfl.ch/labs/csf/publications/), exact 2017 paper entry. |
| Actual author paper | Paper A, displaying **15 May 2015**, inside *Essays on Capital Calculation in Insurance*, **EPFL thesis 7269 (2016)**, presented **18 November 2016**. |
| Actual public source entry | [EPFL institutional container](https://infoscience.epfl.ch/bitstreams/8047fe2b-5639-4462-8d5f-68dd5e02ad96/download), retrieved through its already observed ordinary public link. No temporary redirect query is retained here. |
| Container fingerprint | **155 physical PDF pages; 2,956,212 bytes; SHA-256 `96a01cf863b7bc4e5f4b69f321552a1e7866d7056e0df13ec784ed5a75af448f`.** This identifies the whole container, not a separately hashed chapter. |
| Chapter extent | Paper A cover: physical **14**, printed **12**. Body: physical **15–46**, printed **13–44**. Paper B cover at physical 47 is outside scope. |
| Edition correspondence | The chapter date, thesis date, online publication date and issue date are distinct. No whole-version equivalence with the formal 2017 article is certified. |

### Source synthesis

Cambou and Filipović study how external scenario views can adjust an internal probabilistic risk model. They minimize divergence from a reference law subject to probability floors on specified events, keeping the loss mapping fixed. Conditional averaging over the finite scenario field yields an established finite-cell reduction. The selected author manuscript develops feasibility, uniqueness, robustness and special-solution results, and illustrates capital effects in insurance risk management. Its robustness claims retain topology, quantile and integrability conditions; supplied views do not create a statistical confidence region. Overlapping constraints, point-mass alternatives and capital reductions are already discussed in the source. This register records selected first-pass body and proof-route reading of a dated chapter in a thesis container, not the formal journal body or a complete proof audit. Reweighting a simulation model, changing the divergence or adding scenarios alone does not establish a new method.

### Actual selected reading

All page numbers below are **physical pages of the 155-page container**. Scope is bounded by the completed root reading record; chapter length is not used as a reading-depth proxy.

| Scope | Actual selection and limit |
|---|---|
| 15–17 | Header, introduction, internal-model object and loss/quantile conventions; introductory material partly screened. |
| 18–23 | ES definition, historical Swiss Solvency Test motivation, scenario constraints, divergence, finite-cell reduction, Theorem 5.1 and feasibility/uniqueness boundaries. |
| 24–29 | Selected robustness, KKT and disjoint-scenario results, stress/tail illustrations; page 29 overlap setup only. |
| Lower 32–35 | Selected algebra-of-scenarios convergence, point-mass alternative and conclusion. Case formulas on 30–upper 32 were located, not certified. |
| 42–46 | Selected supplied reduction, feasibility, VaR/ES continuity, disjoint-KKT, algebra-convergence and point-mass proof routes. External foundational proofs were not read. |
| Supplementary selected inspection | Lower 41: supplied Lemmas 3.1/4.2 proofs inspected; Table 2 values only located. Page 26 / printed 24: visual inspection of Theorem 6.4 / Corollary 6.5 and topology distinctions. These passages were inspected separately from the principal reading blocks. |
| Outside the claim | Unrelated thesis material, detailed review of other figures/tables on 36–41, a complete proof audit, executable case certification and independent numerical reproduction. |

### Conditions and financial interpretation

| Object / result | Conditions and limits retained from the selected reading |
|---|---|
| Minimum change | The probability law is adjusted for a fixed loss mapping and horizon. The objective finds a closest feasible law; it does not maximize risk over a divergence ball. |
| Scenario views | Lower probability constraints may overlap. They are supplied views, not estimated confidence bounds. Joint feasibility and absolute continuity matter; positive reference probability for each event alone does not ensure feasibility. |
| Finite cells | Convexity and conditional averaging preserve view probabilities while reducing divergence. A nonempty feasible simplex supports existence; strict divergence convexity has a separate uniqueness role. Binary memberships may generate exponentially many cells. |
| VaR / ES continuity | The source's density-perturbation topology is retained. VaR requires coincident left/right target quantiles. ES under an Lp perturbation retains conjugate loss integrability; the selected entropy/Hellinger consequences use bounded losses. No unrestricted weak-topology or finite-sample guarantee follows. |
| Special cases | Differentiability, positivity and constraint qualification remain relevant to KKT arguments. Disjoint-partition solutions and overlapping entropy/L2 examples are already source results; their literal branch formulas were not certified for execution. |
| Increasing information | The selected limit uses auxiliary-law probabilities, absolute continuity and nested algebras exhausting the information. More selected scenarios or observations alone do not supply these premises, a sampling rate or a confidence statement. |
| Existing illustrations | Simulation-model reweighting, an overlapping-constraint feasibility example, capital decreases from a non-tail view, and a point-mass alternative already occur in the source. Its Gaussian illustrations are not this project's market observations or out-of-sample results. |

The point-mass comparison restricts its total-variation problem to a finite mixture class and can add mass at reference-null points. Its weights and the resulting risk measure have different sensitivities to the chosen points. It is not certified equivalent to unrestricted total-variation optimization. These distinctions constrain transfer; they do not constitute a proposed extension.

### Closest work, resources and access boundary

Liebrich's heterogeneous-belief sharing construction is a direct citation neighbor, but its sharing objective and belief conditions differ from this law-adjustment problem. A distortion-ambiguity sharing problem instead varies preferences while holding participant beliefs fixed. These objects cannot be interchanged without checking their respective domains and assumptions.

The insurance/internal-model setting and historical regulatory discussion are existing applications. Current regulation was not verified. The source's examples, tables and figures were not recomputed; no financial observations or code package was obtained. Data/code availability and reuse rights remain unverified. An article/chapter-specific redistribution license was not established. This register provides bibliographic links and source fingerprints, not source PDFs, images or data.
