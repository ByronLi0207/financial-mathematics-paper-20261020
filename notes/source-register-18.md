# Source register 18 — evidence combination, FDR estimation and financial selection

**Reading update dated 20 October 2026.** This register consolidates completed selected-source reading, with formal records distinguished from actual versions. It adds no original-paper reading credit. It selects no topic, design, financial rule or experiment and reports no replicated result.

## 1. Combining evidence and protecting a hypothesis family

**Vladimir Vovk and Ruodu Wang (2021), “E-values: Calibration, combination and applications.” The Annals of Statistics 49(3), 1736–1754, June 2021.** [DOI](https://doi.org/10.1214/20-AOS2020). Actual source: [48-page author manuscript, 21 September 2020](https://sas.uwaterloo.ca/~wang/papers/2020Vovk-Wang-AOS.pdf).

**Source synthesis — 147 words.**

<!-- SYNTHESIS_1_START -->
The recorded reading selects author-manuscript PDF pp.1–3, 5–15 and 36–42, including merging, closure and selected proof routes; it is not a whole-paper review. Valid e-values are nonnegative with null expectation at most one. Fixed convex averages preserve validity under arbitrary dependence. The arithmetic mean essentially dominates symmetric mergers where their output exceeds one; this qualification differs from pointwise dominance everywhere. The admissible symmetric class uses fixed mixtures of the mean and constant one. Products instead need independence or suitable sequential conditional expectations. Closure adjusts a specified hypothesis family through subset merges, with a common true-null merger supplying family-wise validity. Sorting and subset minimization implement that fixed mapping rather than unrestricted post-outcome optimization. These results require valid input evidence and do not turn fixed-time validity into a stopped-process guarantee. Financial comparisons must establish those inputs separately. Formal-edition equivalence, external technical proofs, empirical examples and executable implementation remain unreviewed.
<!-- SYNTHESIS_1_END -->

## 2. FDR from valid e-values and an existing financial predecessor

**Ruodu Wang and Aaditya Ramdas (2022), “False Discovery Rate Control with E-values.” Journal of the Royal Statistical Society: Series B 84(3), 822–852, July 2022.** First online **11 January 2022**. [DOI](https://doi.org/10.1111/rssb.12489). Actual source: [32-page author manuscript, 14 December 2021](https://sas.uwaterloo.ca/~wang/papers/2021Wang-Ramdas-JRSSB.pdf).

**Source synthesis — 148 words.**

<!-- SYNTHESIS_2_START -->
The recorded reading selects author PDF pp.1–15, 22–25 and 27–32, including the base guarantee, selected boosting proofs and financial application; final-edition equivalence is unverified. Base e-BH controls expected false-discovery proportion for arbitrarily dependent valid e-values through self-consistency and their null expectation bounds. Its threshold is data dependent within the specified rule. Screening an original family retains its original size through the amended level; changing the family retrospectively is a different operation. Optional boosting needs additional null-distribution or dependence information, and its transformed inputs need not remain ordinary e-values. Such inputs cannot automatically be reused in mergers requiring null expectation bounds. Stopping-time use requires genuinely valid stopped processes in the relevant filtration. The paper already includes conditional gross-return no-skill tests and cryptocurrency wealth evidence, ignores transaction costs and expressly avoids future-price prediction. Financial screening itself is therefore established precedent. External proofs, observations, archive contents and empirical reproduction remain unreviewed.
<!-- SYNTHESIS_2_END -->

## 3. Estimated mutual-fund skill proportions and forward holding

**Laurent Barras, Olivier Scaillet and Russ Wermers (2010), “False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas.” The Journal of Finance 65(1), 179–216, February 2010.** First online **13 January 2010**. [DOI](https://doi.org/10.1111/j.1540-6261.2009.01527.x). Actual source: [38-page author-hosted published copy](https://terpconnect.umd.edu/~wermers/FDR_published.pdf).

**Source synthesis — 144 words.**

<!-- SYNTHESIS_3_START -->
The recorded reading selects published PDF pp.1–3, 5–11, 14–18 and 26–29, covering estimation, dependence qualifications and portfolio formation; the Internet Appendix remains unread. Barras, Scaillet and Wermers estimate negative, zero and positive model-alpha proportions after expenses. Two-sided alpha p-values identify a zero-null mixture component through high p-values and adjust significant-tail counts for luck. That component cannot simply be relabeled as the composite nonpositive-alpha population. Residual bootstrap p-values, HAC studentization and dependence checks retain their own assumptions; the discussion does not establish universal finite-sample arbitrary-dependence control. The forward exercise estimates over preceding five-year windows, selects at year end and holds during the following year. Requested FDR labels can differ from achieved estimated formation-period proportions, which are not observed true error rates. Subsequent portfolio alpha is a separate outcome. This is mature financial selection precedent. Proprietary linked observations, current programs, permissions and full reproduction remain unverified.
<!-- SYNTHESIS_3_END -->

## 4. Fixed-region error estimation

**John D. Storey (2002), “A direct approach to false discovery rates.” Journal of the Royal Statistical Society: Series B 64(3), 479–498, August 2002.** Online **12 August 2002**. [DOI](https://doi.org/10.1111/1467-9868.00346). Actual source: [20-page author-lab published copy](https://genomics.princeton.edu/storeylab/papers/directfdr.pdf), read with the companion assumption note below.

**Source synthesis — 146 words.**

<!-- SYNTHESIS_4_START -->
The recorded reading selects published PDF pp.1–7 and 9–19, including definitions, fixed-region estimators, selected internal proofs, q-values and tuning; external proofs remain unread. Storey distinguishes FDR from pFDR, which conditions on at least one rejection. High p-values estimate the null fraction under the maintained independent mixture and calibration assumptions. For fixed rejection and tuning thresholds, the untruncated estimators have conservative expectation results. These are estimator-bias statements, not realized confidence bounds or unrestricted guarantees for thresholds selected from the observed curve. Large-family limits can remain conservative because alternative p-values contribute to the high-p-value region. Additional shape and tail conditions govern stronger limiting recovery. Population q-values, their estimates and individual posterior probabilities are different objects. Bootstrap tuning estimates an MSE criterion rather than supplying known optimal tuning. The original dependence discussion points elsewhere. This foundation informs mutual-fund proportion estimation without certifying arbitrary financial dependence, implementation or data permissions.
<!-- SYNTHESIS_4_END -->

**Companion version note — John D. Storey, one-page author update, as of 16 April 2003.** [Actual author-lab note](https://genomics.princeton.edu/storeylab/papers/directfdr_corrections.pdf). No separate journal article or DOI is asserted.

**Source synthesis — 74 words.**

<!-- SYNTHESIS_5_START -->
The complete one-page author note was read solely to retain the 2002 article's maintained assumptions and tuning interpretation. It specifies independent identically distributed p-value/null-status pairs, uniform null p-values and a continuous alternative density. It also distinguishes estimation of an MSE-minimizing tuning choice from knowledge of that optimum. The note is a companion version qualification, not a separately established dependence, adaptive-control or financial-selection theorem. No additional source audit or implementation conclusion is drawn from it.
<!-- SYNTHESIS_5_END -->

## 5. Additional theory for threshold selection and weak dependence

**John D. Storey, Jonathan E. Taylor and David Siegmund (2004), “Strong control, conservative point estimation and simultaneous conservative consistency of false discovery rates: a unified approach.” Journal of the Royal Statistical Society: Series B 66(1), 187–205, February 2004.** First online **22 December 2003**. [DOI](https://doi.org/10.1111/j.1467-9868.2004.00439.x). Actual source: [19-page author-lab published copy](https://genomics.princeton.edu/storeylab/papers/623.pdf), stating final revision June 2003.

**Source synthesis — 155 words.**

<!-- SYNTHESIS_6_START -->
The recorded reading selects published PDF pp.1–10 and 12–19, including procedures, assumptions and selected proof routes; numerical reproduction and external foundations remain unreviewed. Storey, Taylor and Siegmund add conditions connecting error estimation to adaptive-threshold FDR control. Their modified finite-sample procedure uses a plus-one high-p-value count and restricts thresholds to the tuning region under its independent-uniform-null framework. Dependent-data results instead require almost-sure convergence of null and alternative empirical p-value distributions and a limiting null fraction. Weak dependence is defined by those limits rather than a small observed average correlation. Simultaneous conservative consistency concerns thresholds bounded away from zero as the number of tests grows, not repeated calendar-time monitoring. Specified asymptotic tuning results extend to a fixed finite candidate set; this does not extend every finite-sample theorem to unrestricted tuning. Financial applications must validate individual tests separately and distinguish more tested assets from more observations per asset. Historical software references do not establish current access or permissions.
<!-- SYNTHESIS_6_END -->

## Cross-source distinctions

This table compares the recorded targets and assumptions; it adds no theorem or proposed procedure.

| Dimension | Distinction retained |
|---|---|
| Evidence at one analysis versus over time | An e-value's null expectation bound and an e-process's stopped validity have different quantifiers and information requirements. |
| Averaging versus multiplication | Fixed convex means allow dependent inputs valid under a common null; products require independence or the relevant sequential conditional bounds. |
| Error metric versus observed outcome | FDR is an expectation, realized FDP depends on unknown null labels, and estimated FDR is a statistical estimate. |
| Family size m versus history length T | Cross-test empirical-distribution limits as m grows do not follow merely by lengthening every asset's return history T. |
| Formation alpha versus subsequent alpha | Historical model-alpha selection and following-period portfolio performance answer different questions; neither certifies future profits. |
| Data-dependent calculation versus an altered rule | Sorting, screening and thresholding require their stated valid construction; favorable retrospective choices do not inherit that validity automatically. |

The closest financial uses already include mutual-fund proportion estimation, forward fund selection and wealth-based asset screening. Adopting an established method or changing the financial dataset is not by itself a new method. No financial null, candidate family, threshold, holdout or implementation is selected here.

## Provenance, access and fingerprints

These entries were checked against registers 01–17; references elsewhere were not promoted to repeated principal-body entries. This preparation uses only completed reading records, retained metadata and existing source fingerprints. Actual reading was selected, not whole-paper certification. Source copies are linked for identification, without distributing a PDF, dataset or program.

Current observation access, program versions, archive contents and separate reuse permissions remain unverified where not explicitly established in the recorded scope. A readable article, historical software pointer or author attachment does not settle those separate questions. No license is inferred here.

The following existing evidence files were rehashed during preparation and matched the recorded values. Fingerprints identify the actual versions, without certifying unread final-edition equivalence.

| Actual retained version | Bytes | SHA-256 |
|---|---:|---|
| Vovk–Wang, author manuscript 21 September 2020 | 918296 | `c47b5ecd4ce725222a7ac669f207dd11102c86ef8da428347b1ba0969343a4c5` |
| Wang–Ramdas, author manuscript 14 December 2021 | 509525 | `b47e68ff570fc32b779ba57e069daba92b3594f2b192c788bd990d7afef291b9` |
| Barras–Scaillet–Wermers, published 2010 copy | 826187 | `17a1354458bbfbe712307fdd45d3cebba03c072956252124d5656a921dda6c72` |
| Storey, published 2002 copy | 311416 | `8cc0f701ade632acd4864d3456d3a13889b38bec60fb55160b2328c7384e773f` |
| Storey, one-page author note 16 April 2003 | 39044 | `cc48df118e79959a8bb1170a3855d1cc87cd34ae9a52605552a8aa5398389d6c` |
| Storey–Taylor–Siegmund, published 2004 copy | 201967 | `4de8c455d6e5b096cc3303ac6888ab97eef8d97e171588a16fe7c724bc08bab0` |
