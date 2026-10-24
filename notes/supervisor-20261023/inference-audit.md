# E1, E2 and E4 audit for the supervisor revision

Audit date: 2026-10-23. Destination is the new supervisor checkout based on main `65feeee`. The previous v3 checkout was read only. No financial forecast was refitted, archived result changed, dependency installed, model reviewer called, or commit/push made by this audit.

## Deliverables and provenance

`results/supervisor-20261023/inference/tables3-4-ready.csv` and `.json` contain all 48 original table entries: four H/W cells per source, six methods per cell. Losses are displayed in USD millions for both sources; original Treasury values were already in those units, whereas FX values were divided by one million. Each row includes loss, loss relative to its own frozen F, strict breach count/rate, DM reference and fixed-family Holm reference where applicable, and three-decimal display strings.

The original `inference_tests.py` was imported exactly, SHA-256 `2678afca3d0b01e80712c39d8a4a06f47107fc7576d1ee9d867f08c2212cd88c`. Its only imports are `math` and NumPy; there are no file, subprocess, network, installation or top-level experiment actions. The prior orchestrator `run_v3_inference.py` was read but not imported: it depends on revision-specific ledger writers, refit guards and plotting helpers whose side effects are unnecessary here. New execution is confined to `supervisor_inference_audit.py` and outputs under the new inference directory.

The B5 queue hash is checked against its numerical-audit record, each cell receipt against its queue hash, and each private numeric trace against the receipt artifact hash. Repeated historical arrays must agree exactly. Every imported inference file and source module is hashed again after the read. Current main and prior v3 `paired-comparisons.csv`, `evaluation-summary.csv`, and `evaluation-nonoverlap.csv` agree exactly. Imported outputs remain under `inherited-exact/`, including the inherited CC convention.

## E1: paired loss inference

The paired primary means reproduced exactly from retained per-origin losses:

| Contrast, new minus reference | Paired mean in native units | DM t | Normal p | Holm p |
|---|---:|---:|---:|---:|
| FX H6 QR2880 minus rolling F720 | -55,929.151549 USD | -5.182010 | 2.195073e-7 | Outside family |
| FX H6 QR2880 minus frozen F2880 | -66,848.097958 USD | -5.865680 | 4.472961e-9 | 2.862695e-7 |
| FX H6 QR720 minus frozen F720 | -9,368.957482 USD | -0.615893 | 0.537965 | 1.000000 |
| FX H24 QR2880 minus rolling S720 | -13,688.469685 USD | -0.203789 | 0.838518 | Outside family |
| Treasury H6 QR260 minus frozen F260 | +1,401.007852 USD millions | +2.668840 | 0.007611 | 0.319678 |

All 74 DM rows match the inherited t/p values exactly. A separate scalar implementation uses `math.fsum` for every lagged product, independently of the inherited NumPy matrix HAC; the largest absolute t difference is 3.55e-15. The implementation uses centered sample autocovariances with denominator n, Bartlett weights `1-k/(L+1)`, and `L=max(H,floor(4(n/100)^(2/9)))` capped at n-1. Thus L is 10/24 for FX H6/H24 and 6/24 for Treasury H6/H24. The declared H convention is retained; this bandwidth is a working choice rather than proof that dependence ends at H.

HLN uses `sqrt((n+1-2H+H(H-1)/n)/n)` and Student n-1 tails. Thirty independent numerical integrations of the Student density, across df 1, 2, 3, 276 and 6624, agree with the inherited incomplete-beta tails within 3e-10 absolute error. HLN was developed for MSPE; applying its multiplier to overlapping pinball losses is an approximation. Report it as sensitivity, without claiming exact finite-sample size.

The unchanged 72-member Holm family is the 24 selected conditional cells (QR, KNN and scaled KNN across eight source/H/W cells), each compared with its own frozen F/S/K. It excludes both original cross-window FX comparisons. Treasury's primary is already one of the 72 and is counted once. The two full-pool Treasury KNN W52 identities have undefined DM statistics and use p=1 only for multiplicity bookkeeping. F self-comparisons and historical S/K versus F are outside this family; their table entries are dashes. No new historical-reference or E3 tests were silently added.

The number of Holm normal-reference p<.05 results is 19 at L, 18 at 2L; HLN-reference Holm gives 19. The Treasury primary remains descriptively worse, with raw p=.0076 and adjusted p=.320. It must not be described as significant after this adjustment. All tests were added after inspection, and the p-values remain exploratory references. Holm addresses only the stated family and does not repair selection from earlier inspection. Fixed finite training windows motivate a Giacomini–White unconditional forecasting-method interpretation, conditional on weak dependence, adequate moments, a positive limiting long-run variance and a suitable HAC estimator. These assumptions were not established for the two observed records.

## E2: grids, ties and finite-sample initialization

For every trace, origins are consecutive source indexes. The grid is exactly `first_origin+j(H+1)` across the entire evaluation segment, with no calendar-year reset: FX anchor 11927, Treasury anchor 405. Counts are FX 947/265 and Treasury 40/12 at H6/H24. The hit is strict `peak>capacity`; exact ties are non-breaches. Capacity and outcome both satisfy the current-position floor, and the stored per-origin losses agree with the corresponding .95 pinball formula.

The full-n Kupiec POF and conditional transition-independence likelihood calculations reproduce all inherited values. A finite-sample initialization mismatch was found in the inherited CC sum: full-n POF was added to an IND likelihood conditioned on the first hit. Christoffersen (1998), printed p.847, states that the additive identity conditions on the first observation in the UC term as well. The new CC output uses this internally consistent conditional likelihood. The inherited output is retained exactly rather than overwritten.

Let n_ij count adjacent hits, N=n-1, K=n01+n11, pi=K/N, and pi_i=n_i1/(n_i0+n_i1). With Bernoulli log likelihood l(k,N,p), define

- `LR_uc_cond=2[l(K,N,pi)-l(K,N,.05)]`;
- `LR_ind=2[sum_i l(n_i1,n_i0+n_i1,pi_i)-l(K,N,pi)]`;
- `LR_cc_direct=2[sum_i l(n_i1,n_i0+n_i1,pi_i)-l(K,N,.05)]`.

The helper checks `LR_cc_direct=LR_uc_cond+LR_ind` for every identified row. Full-n POF is reported separately. Independence uses chi-square one; joint CC uses chi-square two. Missing conditioning-state rows yield missing IND/CC. Zero transition cells retain boundary-reference labels. In this record all 90 rows have both conditioning states; 38 have at least one zero transition cell. Asymptotic references are especially coarse on Treasury grids.

| Original series | n | Hits | Breach rate | Full-n POF p | Conditional CC p | Inherited full-n-plus-IND CC p |
|---|---:|---:|---:|---:|---:|---:|
| FX H6 QR2880 | 947 | 50 | 5.280% | .695277 | .636152 | .638050 |
| Treasury H6 QR260 | 40 | 7 | 17.500% | .004126 | .013593 | .015695 |
| Treasury H6 frozen F260 | 40 | 4 | 10.000% | .198641 | .261900 | .276841 |

An independent fixture uses hits `00000001110`, with counts `(6,1,1,2)`. The direct Markov alternative likelihood is `(6/7)^6(1/7)(1/3)(2/3)^2`; the conditional null is `.95^7 .05^3`. This yields the direct CC statistic and independently verifies the additive identity. A second fixture starts with a hit and verifies that this hit is omitted from conditional UC.

These are diagnostics of exactly 5% iid hit probability. A correct .95 quantile at an atom requires inequalities: `Pr(Y<C)<=.95<=Pr(Y<=C)`, hence `Pr(Y>C)<=.05`, with equality requiring additional conditions at the issued quantile. A two-sided equality test can therefore reject a conservative yet valid upper quantile. The current-position floor creates target atoms; their existence alone does not force a tie at every issued forecast. For example, the Treasury primary grid has two issued-forecast ties; FX QR2880 has none. The output records ties, floor atoms and floor-issued forecasts separately.

H+1 spacing removes overlap among the target paths, but shared rolling estimation can retain dependence among hits. A large p-value is not a coverage guarantee. Under a hypothetical independent 5% hit process, Treasury's n=40 and n=12 grids expect only 2 and .6 hits respectively; their probabilities of zero hits are about .129 and .540. These small grids have low power, and some transition likelihoods are boundary cases.

## E4: every threshold, not only display samples

The inherited Murphy implementation was independently checked using integer endpoint counts and sorted searches, rather than weighted event accumulation. For each forecast, its score is `(1-tau)#(y<=theta<x)/n + tau#(x<=theta<y)/n`. All unique forecast/outcome breakpoints were evaluated: 16,146 for FX and 640 for Treasury. The score is constant between adjacent breakpoints and zero outside the joint support, so this checks the whole real threshold range, including exact ties. Both diagrams cross. Neither original primary empirically dominates its comparator across the entire class of regular .95-consistent scoring functions.

Integrating the exact step differences reproduces the paired pinball mean differences within numerical rounding. `murphy-two-primary-exact.pdf` draws every step, and its rendered PNG was visually inspected. It is a descriptive sample comparison without a population-dominance test or simultaneous uncertainty band. The previously published 201-point display CSVs remain only display summaries; the all-range ruling does not depend on them.

## Original-source methods check

Formal metadata and access scope are stored in `results/supervisor-20261023/inference/method-sources.json`.

- Diebold and Mariano (1995), *Journal of Business & Economic Statistics* 13(3), 253–263, DOI 10.1080/07350015.1995.10524599. Read the journal scan, printed pp.254–255: general losses, paired loss differential, denominator-n autocovariances and the stationarity/short-memory basis of the normal reference. [Published record](https://doi.org/10.1080/07350015.1995.10524599), [original article scan](https://www.ssc.wisc.edu/~bhansen/718/DieboldMariano1995.pdf).
- Newey and West (1987), *Econometrica* 55(3), 703–708, DOI 10.2307/1913610. Read the author-hosted journal scan, printed pp.704–705, equation (5) and Theorems 1–2: modified Bartlett weights, positive semidefiniteness, growing bandwidth and moment/mixing assumptions. [Author copy](https://www.ssc.wisc.edu/~kwest/publications/1980/A%20Simple%20PSD%20HAC%20Covariance%20Matrix.pdf).
- Harvey, Leybourne and Newbold (1997), *International Journal of Forecasting* 13(2), 281–291, DOI 10.1016/S0169-2070(96)00719-4. Publisher metadata and abstract verified; original full-body retrieval was blocked. The multiplier and Student n-1 reference were additionally checked against the official statsmodels implementation documentation. This is implementation-source verification, not a claim to have read the original derivation. [Publisher](https://www.sciencedirect.com/science/article/pii/S0169207096007194), [official implementation notes](https://www.statsmodels.org/devel/generated/statsmodels.tsa.stattools.diebold_mariano_test.html).
- Giacomini and White (2006), *Econometrica* 74(6), 1545–1578, DOI 10.1111/j.1468-0262.2006.00718.x. Read original article pp.1546–1553 and the unconditional-null discussion: finite-memory forecasting methods include estimation choices, and the unconditional case is nested in their framework. [Publisher](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2006.00718.x), [original article](https://economia.uc3m.es/jgonzalo/teaching/PhdTimeSeries/GiacominiWhite.pdf).
- Holm (1979), *Scandinavian Journal of Statistics* 6(2), 65–70, stable identifier 4615733. Publisher archive issue verifies title, author and pages. Original-body retrieval was unavailable; the ordered step-down arithmetic was independently reproduced and tested. [Publisher archive issue](https://www.jstor.org/stable/i412579), [article record](https://www.jstor.org/stable/4615733).
- Kupiec (1995), *The Journal of Derivatives* 3(2), 73–84, DOI 10.3905/jod.1995.407942. Publisher-deposited Crossref metadata verifies the journal entry and is saved locally; the official Federal Reserve archive also verifies FEDS 95-24 (May 1995). Original-body text did not load. The Bernoulli likelihood was independently calculated, and its UC counterpart was read in Christoffersen's original paper. [Journal DOI](https://doi.org/10.3905/jod.1995.407942), [publisher-deposited registry metadata](https://api.crossref.org/works/10.3905/jod.1995.407942), [Federal Reserve archive](https://fraser.stlouisfed.org/title/finance-economics-discussion-series-1491/techniques-verifying-accuracy-risk-measurement-models-717921).
- Christoffersen (1998), *International Economic Review* 39(4), 841–862, DOI 10.2307/2527341. Read the journal scan pp.844–847, §§2.2 and 3.1–3.3. Conditional-on-first-hit initialization is explicit on p.847. [Author bibliography](https://christoffersen.com/academic-papers/), [original article scan](https://users.ssc.wisc.edu/~bhansen/718/Christoffersen1998.pdf).
- Ehm, Gneiting, Jordan and Krüger (2016), *JRSS B* 78(3), 505–562, DOI 10.1111/rssb.12154. Institutional metadata verified; read author preprint Theorem 1a and Corollary 2a: elementary quantile scores and the finite-breakpoint sample check. [Institutional record](https://publikationen.bibliothek.kit.edu/1000055110), [author preprint](https://arxiv.org/pdf/1503.08195).

## Verification and limits

Seven independent statistical fixtures passed. The complete trace audit passed for 90 cells, 74 DM contrasts, the fixed 72-member family, all corrected coverage rows and both all-range Murphy diagrams. No raw source reload, fresh estimation, independent dataset validation, or confirmatory interpretation was performed. The selected source PDF copies are local reading material and are not a recommendation to redistribute third-party articles with a public release.
