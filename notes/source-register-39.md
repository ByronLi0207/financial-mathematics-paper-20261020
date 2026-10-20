# Source register 39 — time consistency of the mean–risk problem

**20 October 2026. Literature phase.** This is one new principal article, consolidated from reading blocks 186–189. Source-location and supplement-access records add no article or body-reading count. No final design, financial experiment or empirical result is claimed.

## Source and actual edition

**Gabriela Kováčová and Birgit Rudloff (2021), “Time Consistency of the Mean-Risk Problem,” Operations Research 69(4), 1100–1117.** [Formal DOI](https://doi.org/10.1287/opre.2020.2002).

| Evidence | Verified identity and boundary |
|---|---|
| [WU institutional record](https://research.wu.ac.at/en/publications/time-consistency-of-the-mean-risk-problem-12/) and [actual institution-hosted PDF](https://research.wu.ac.at/ws/portalfiles/portal/18317633/opre.2020.2002.pdf) | **Final published version / version of record**, not an arXiv body. Actual file: **20 physical pages**, including **two preliminary cover pages**. Physical 3–20 correspond to printed 1100–1117. |
| Actual article history | Received 28 June 2018; revised 27 February 2019; accepted 30 December 2019; online **19 March 2021**; issue **July–August 2021**. Manuscript-history dates are not the issue year. |
| [Separate arXiv record](https://arxiv.org/abs/1806.10981v2) | v1 deposited 28 June 2018; v2 deposited 16 January 2020. **Metadata only**: its body was not read or compared with the formal article. |

**Original source synthesis — 133 words.**

<!-- SYNTHESIS_1_START -->
Kováčová and Rudloff study dynamic mean–risk portfolios through upper-image recursion rather than repeatedly solving a fixed-weight scalar objective. The finite investor-believed market, self-financing positions, no transaction costs and a specified time-consistent convex risk measure are substantive inputs. Weak efficiency does not imply strong efficiency at every node. Coherence and conical restrictions support wealth scaling, while the implemented specialization adds positive prices, nonnegative positions and positive wealth. Selected main statements, Theorem 1's supplied proof, examples and main-appendix arguments were read in the 2021 version of record. Its recursive CVaR is distinguished from ordinary dynamic CVaR. Model-based frontiers and moving-weight policies already provide financial applications; they are not market holdouts, and reported mean/risk comparisons retain tradeoffs. The e-companion and forward Algorithm 3 remain unread. External proofs, complete correctness, code availability and numerical reproduction remain unverified.
<!-- SYNTHESIS_1_END -->

## Actual selected reading

All ranges below use the **20-page institutional PDF**, not an arXiv page map. They record selected statements and supplied arguments, not independent certification of every step.

| Block | Physical pages and selected material | Visual / unread boundary |
|---|---|---|
| 186 | 3–8 before Section 3: introduction, Sections 2.1–2.4, Assumption 1, dynamic convex/coherent risk, efficiency, upper images and Lemmas 1–3. | External originals and Lemma 3's e-companion proof unread. Cover/location checks do not add article-body scope. |
| 187 | 9–14 before Section 7: Sections 3–6.2; Theorem 1 supplied proof; Lemma 5 scalarization interpretation; Theorem 2 and Lemmas 6/7 statements; Lemma 8, Assumption 2, Algorithm 1 and Lemmas 9/10 statements/discussion. | Main-appendix proof scope is added in 189, not backdated. E-companion proofs of Lemmas 4/5/8/9/10 and Algorithm 3 unread. |
| 188 | Section 7 on 14–18 before Acknowledgments: both examples, Tables 1–3 and Figures 1–6. | Original images **14, 15, 16, 17** inspected. Source-reported values/plots were not recomputed or evaluated on market data. |
| 189 | Main Appendix on 18–20 before References: Lemmas 11/12; A.1 supplied proof of Lemma 6; A.2 supplied proof of Theorem 2; A.3 Lemma 13/proof of Lemma 7. | Original image **19** inspected. External foundations, every literal detail and the separate e-companion remain unverified. |

## Conditions and financial meaning

The market is a finite probability space under **one investor-believed price law whose distributions are treated as known for optimization**. That belief need not be the true market law. It is not statistical validation of a newly fitted model, and finite observations do not establish a finite-support market. Positions are asset units; trading is self-financing, without transaction costs, under closed conditionally convex restrictions.

The risk input is already normalized, cash-invariant, monotone, conditionally convex and time consistent. This input's recursion differs from time consistency of the portfolio problem. Variance or ordinary conditional VaR cannot simply be substituted while retaining those assumptions.

Theorem 1's supplied weak-efficiency route uses feasible continuation, recursive risk, strict conditional-mean monotonicity and a positive gap on the finite state space. It does not make every initially efficient policy efficient at every node or establish the same result for arbitrary continuous market states. The more specific strategy-construction statement under Assumptions 1/2 is distinct from a claim about every efficient-profile-attaining strategy; its e-companion proof remains unread.

Coherent risk and conical trading restrictions support positive-homogeneous wealth scaling. The implemented specialization further uses nonnegative holdings, positive prices and positive wealth. Fixed fees or lot restrictions do not automatically preserve that reduction. The main Appendix uses monotonicity, finite-space continuity, feasible continuation, cone addition and closure to preserve upper images; it is not permission for arbitrary convexification or removal of constraints.

## Existing examples and adverse comparison boundaries

The examples add iid returns and use **recursive CVaR**, explicitly distinguished from ordinary dynamic CVaR. One is a calibrated binomial model with 2,500 periods; the other generates correlated bond/seven-other-asset returns over 12 periods. These are model calculations using vector-optimization software, not chronological market holdouts or measured project resource use.

A fixed initial scalarization weight selects a dynamic efficient profile. Re-solving with the same fixed weight at every date is a different baseline. Supporting weights can move with time/state and need not be unique at frontier vertices.

Table 3 retains tradeoffs: the displayed myopic/fixed-0.5 mean values slightly exceed the dynamic-0.5 mean, alongside worse reported risk. No universal mean dominance, significance, fee-adjusted profit or historical superiority follows. At low CVaR levels the source describes worst-case-like behavior and reduced diversification tied to its market parameters. A model-based mean–risk frontier is neither a Sharpe comparison nor an ordinary one-step ES evaluation.

## Unread supplement and materials

The [official Supplemental Material landing](https://pubsonline.informs.org/doi/suppl/10.1287/opre.2020.2002) was normally visible and displayed **opre.2020.2002.sm1.pdf**. A separate ordinary request to inspect that landing's HTML for an absolute attachment href returned **403** and was closed. The filename is observed; the absolute file URL is **unverified and not reconstructed**.

The e-companion was not obtained: no attachment bytes, hash, page count, version comparison or proof reading. **EC.1/EC.2 and Algorithm 3 remain unread**; their contents are not filled from the main text or arXiv. This access boundary does not establish that every normal interface is unavailable.

The actual article/record identify CC BY 4.0. That article licence does not establish availability or unrestricted rights for unprovided code, example data or the unread attachment. No Bensolve bundle, author program, observation dataset or numerical reproduction was obtained. External theorem bodies remain separate dependencies.

## De-duplication and retained fingerprint

Registers 01–38 were checked by title, authors and DOI/arXiv identity. This article had no prior dedicated principal or body scope. Blocks 186–189 therefore add **one** principal. The earlier Cialenco–Kováčová source is a different article; metadata and the e-companion do not add another body edition.

| Exact retained original | Bytes | SHA-256 |
|---|---:|---|
| 20-page institution-hosted 2021 version of record | **2252331** | **43285164dcfd795a4fa27eaf94d2c8fe810a3d92d4d46204ae5caae35d92cd15** |

The retained bytes were rehashed and matched. This identifies the actual file, not complete proof correctness or equivalence with unread versions. This administrative curation adds **zero new source-body reading credit**. No source PDF, figure, raw data or substantial source passage is redistributed.
