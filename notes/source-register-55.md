# Source register 55 — Tail-GAN

One new principal. **Selected reading; no complete proof certification.**

## Formal identity and actual representation

**Rama Cont, Mihai Cucuringu, Renyuan Xu and Chao Zhang, “Tail-GAN: Learning to Simulate Tail Risk Scenarios.” Management Science 72(4), 2917–2936.** DOI: [10.1287/mnsc.2023.00936](https://doi.org/10.1287/mnsc.2023.00936).

| Field | Exact version / evidence boundary |
|---|---|
| Formal metadata | [Official INFORMS record](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2023.00936). Published online **11 August 2025**; assigned issue **April 2026**; publisher **Cite-as year 2025**. These fields are preserved separately. |
| Other formal dates | Received **5 April 2023**; accepted **11 March 2025**. |
| Formal-body boundary | Journal body and supplement **unread**; no equivalence with the repository version is certified. |
| Actual selected body | **arXiv:2203.01664v4**, [version-specific PDF](https://arxiv.org/pdf/2203.01664v4), [HTML](https://arxiv.org/html/2203.01664v4). PDF title date **11 May 2025**; v4 submitted **16 May 2025, 00:26:55 UTC**. |
| Actual fingerprint | **40 physical pages; 2,452,946 bytes; SHA-256 `73cf58ddc6a03031ac0fc800c2da09efd272cfa033e9c26f1effa3deff5649b5`.** This is the v4 PDF, not the formal article. |
| Article rights | Displayed arXiv license: **CC BY-NC-ND 4.0**; this does not establish market-data rights. |
| Code / data documentation | [Repository LICENSE](https://github.com/chaozhang-ox/Tail-GAN/blob/main/LICENSE): GPL version 3. [README](https://github.com/chaozhang-ox/Tail-GAN/blob/main/README.md) says LOBSTER market data require purchase. Main-branch documentation, not a pinned replication revision; data redistribution and paper/commit alignment unverified. No code/data package obtained or executed. |

## Science synthesis — 112 words

<!-- SYNTHESIS_1_START -->
Tail-GAN matches strategy tail features, but finite benchmarks do not identify all strategies or a full path law. Approximation retains Lipschitz PnLs, density/moment and quantile regularity; transport-gradient existence does not establish training success. Joint scoring retains action-domain and integrability conditions. The ideal population equivalence restricts D0 to a common feasible law and assumes expressive maps. Synthetic oracle comparisons, strategy holdouts and chronological market holdouts answer different questions. Market paths overlap heavily; historical simulation is a close comparator, with metric-dependent rankings. Reported numerical findings were not reproduced. Feature matching provides neither statistical confidence coverage nor novelty certification. The method and its financial evaluation are existing work, not a new contribution from changing assets.
<!-- SYNTHESIS_1_END -->

The manuscript uses lower-tail profit conventions.

## Actual selected scope

All page references identify the **40-page v4 PDF**, not the formal journal pagination. Selected passages and supplied proof routes are recorded below.

| Physical pages | Selected locations | Located only / reading boundary |
|---|---|---|
| **4–7** | Section 2; Propositions 2.1–2.2; lower 7. | Introductory claims partly screened; examples located. |
| **8–12** | Section 3; Assumptions 3.1–3.5; Theorems 3.4/3.7/3.8; Section 4.1. | Selected first pass. |
| **30–34; upper 35** | Appendix A / Theorem A.1; B.1–B.4. | C.1 / Table 10 on 35 located only. |
| **13–15** | Algorithm, evaluation and test-split passages. | Selected first pass. |
| **16–22** | Selected synthetic-study text and tables. | Figures/captions located; tables not recomputed. |
| **23–27** | Section 5.4 end; Section 6; conclusion. | Figures mostly located/captions. |
| **36–upper 38** | C.2–C.4. | Selected first pass. |

External foundational proofs and a complete numerical reproduction are outside this record. No source plots, tables, observations or code files are reproduced here.
