# Source register 07: forecast information, proxies and robustness

Updated 20 October 2026. Primary-source literature record. Reading depths below distinguish selected passages, actual source versions and final publication metadata. This is not a finalized topic, an empirical result or a completed-duration claim. Third-party source documents and observations are not redistributed.

## 1. Sequential model confidence sets — formal-publication update

**Sebastian Arnold, Georgios Gavrilopoulos, Benedikt Schulz and Johanna Ziegel, “Sequential model confidence sets.”** *Journal of the Royal Statistical Society Series B*, article qkag066, published 13 May 2026. [DOI:10.1093/jrsssb/qkag066](https://doi.org/10.1093/jrsssb/qkag066). Actual source: [official final article HTML](https://oup.silverchair-cdn.com/article-minimal/8676743). This updates the previously recorded [arXiv:2404.18678v4](https://arxiv.org/abs/2404.18678v4); it is the same work, not another paper.

**Reading:** selected final §§1–3.4, case-study descriptions and availability; direct main-text Proposition 3.2 proof. Final technical supplements were not newly audited.

The article separates pointwise conditional dominance, all-prefix conditional-average dominance and current-prefix dominance. Sequential sets protect all true superior models in the declared family. Predictable score scaling can change the cumulative target; the paper explicitly treats this change. Predictable bounds suffice for its strong construction, while other constructions require uniform bounds or separately justified tails. Retention is not proof that every retained model is optimal. The reported cases concern COVID and wind-gust forecasts; a finance citation is not a finance experiment. [Companion repository](https://github.com/GGavrilos/SMCS) availability was checked, not executed.

## 2. Imperfect volatility proxies

**Andrew J. Patton, “Volatility forecast comparison using imperfect volatility proxies.”** *Journal of Econometrics* 160(1), 246–256 (January 2011). [DOI:10.1016/j.jeconom.2010.03.034](https://doi.org/10.1016/j.jeconom.2010.03.034). Actual source: [author-hosted journal PDF](https://public.econ.duke.edu/~ap172/Patton_vol_proxies_JoE_2011.pdf),11 pages; online 6 March 2010.

**Reading:** selected published pp. 247–255, loss characterization and displayed proposition proofs; empirical design/discussion, without numerical replication.

Conditional-unbiasedness of a proxy preserves expected rankings for a characterized loss class, including MSE and QLIKE. This robustness concerns a proxy substitution, not resistance to outliers. MSE and QLIKE can still disagree because they express different criteria. Squared returns target a second moment unless the conditional mean condition is satisfied. A common outcome-only term cancels in differences; normalized QLIKE levels and affine pairwise differences have different behavior at zero. The source already compares IBM volatility forecasts and intraday proxies. TAQ-based observations were not acquired; no dataset or code execution is claimed.

## 3. Risk-measure estimation and qualitative robustness

**Rama Cont, Romain Deguest and Giacomo Scandolo, “Robustness and sensitivity analysis of risk measurement procedures.”** *Quantitative Finance* 10(6), 593–606 (2010). [DOI:10.1080/14697681003685597](https://doi.org/10.1080/14697681003685597). Online 4 June 2010. Actual source: [author-hosted 14-page article copy](http://rama.cont.perso.math.cnrs.fr/pdf/RobustRisk.pdf).

**Reading:** selected pp. 593–604 and Appendix A.1 proof; remaining appendix details were not fully audited.

The paper distinguishes risk-functional axioms, estimator-law stability and influence functions. Historical VaR has qualitative robustness on the stated unique-quantile class. The negative ES result uses a broad finite-first-moment class and weak-topology perturbations; it is not a universal verdict against tail-restricted ES procedures. Historical ES influence grows in the adverse tail, while a parametric scale fit can target a different effective functional under misspecification. Spectral trimming is already studied. Its derivative-portfolio scenario example was not reproduced or obtained as public data; no new raw-data availability is asserted.

## 4. Tail-class refinements

**Volker Krätschmer, Alexander Schied and Henryk Zähle, “Comparative and qualitative robustness for law-invariant risk measures.”** *Finance and Stochastics* 18(2), 271–295 (2014). [DOI:10.1007/s00780-013-0225-4](https://doi.org/10.1007/s00780-013-0225-4). Online 16 January 2014. Actual source: [arXiv:1204.2458v6](https://arxiv.org/abs/1204.2458v6),14 January 2014, 23 pages; final journal text was not line-compared.

**Reading:** selected definitions/results in §2, statistical robustness proofs in §3.1, relevant §4 consistency/continuity proofs and Appendix A.

The refinement combines a stronger moment-sensitive topology with robustness on uniformly integrating perturbation subsets. The broad estimation domain includes empirical laws; the controlled generating-law subset need not contain every sample distribution. Individual moment existence is weaker than uniform tail control. ES has robustness indexone in the specified convex-risk framework, retaining this definition. Separately, stationary-ergodic plug-in consistency is established under Orlicz-heart assumptions. These are not finite-sample rates or uniform robustness over arbitrary dependent joint laws. This theoretical reading did not identify an empirical market dataset or validate a code package.

## 5. Heavy-tailed confidence sequences

**Hongjian Wang and Aaditya Ramdas, “Catoni-style confidence sequences for heavy-tailed mean estimation.”** *Stochastic Processes and their Applications* 163, 168–202 (September 2023). [DOI:10.1016/j.spa.2023.05.007](https://doi.org/10.1016/j.spa.2023.05.007). Actual source: [arXiv:2202.01250v6](https://arxiv.org/abs/2202.01250v6),7 February 2024, 33 pages; its title-page date remains 13 June 2023. Final/preprint differences were not exhaustively audited.

**Reading:** selected assumptions, §6, §§9–10 and necessary Appendix C/D passages, including the complete short Lemma 8 proof.

The main target is a common conditional mean with a known valid conditional variance bound. Catoni envelopes produce supermartingales without requiring light-tailed observations. Coverage permits predictable tuning; width theorems add restrictions. Extensions retain known predictable conditional p-moment bounds and distinguish weighted drifting-mean targets from path regions. Past empirical variance is not automatically a valid population envelope. The impossibility discussion concerns broad unrestricted mean classes, not all inference under support/structural restrictions. [Companion code](https://github.com/HJ-Wg/catoni-confseq) was identified but neither downloaded nor run; reported experiments are simulations.

## 6. More information and ideal financial forecasts

**Hajo Holzmann and Matthias Eulert, “The role of the information set for forecasting—with applications to risk management.”** *The Annals of Applied Statistics* 8(1), 595–621 (March 2014). [DOI:10.1214/13-AOAS709](https://doi.org/10.1214/13-AOAS709). Actual source: [arXiv:1404.7653v1](https://arxiv.org/abs/1404.7653v1),30 April 2014, 28-page IMS electronic reprint. It explicitly differs from original journal pagination/typography.

**Reading:** selected main definitions, Theorem 1/Corollary 2 and complete short proofs, VaR/ES discussion, inference conditions and financial applications; no full table audit.

Under nested information fields, the ideal forecast of the same elicitable scalar functional minimizes its strictly consistent expected score. Both forecasts must be evaluated on the same outcome and conditioning law. Equal quantiles need not identify equal distributions. Under integrability and continuous, strictly increasing conditional distributions, a special quantile-score identity supports conditional-averaged and ex ante ES interpretations, not independent ES backtesting or statewise risk reduction. Estimated models need not inherit ideal dominance: the paper already compares portfolio-history and component-history risk forecasts. Its 500-observation rolling GARCH/DCC application is reported source evidence; prices and modern code/reuse conditions were not independently acquired or verified.

## Implications for method transfer

| Question | Existing distinction to preserve |
|---|---|
| Does a volatility proxy preserve a ranking? | Conditional-unbiasedness and the selected loss matter. |
| Is an ES estimate robust? | Name the topology, tail class, estimator and sampling model. |
| Can a comparison be inspected continuously? | Match its conditional target, moment/bound assumptions and model-family adjustment. |
| Does additional information improve predictions? | Distinguish ideal conditional functionals from fitted model procedures. |

These sources already supply substantial financial and statistical foundations. A changed asset, score name or data file alone will not be presented as a new method. Current work remains primary reading and applicability checking.

## Actual-source fingerprints

| Actual source copy | SHA-256 |
|---|---|
| SMCS official final HTML | `c106a68a15f54163e6301e2e7451e40e0a090609dbf0a4cb941e92a329a01cb9` |
| Patton journal PDF | `bfcc630f931a01e5c678c77d0f98240aa538af0bc5d1153f657d45c12b0ab64a` |
| Cont–Deguest–Scandolo article copy | `c2bbfe5159f95dea2c35a73df3682fa523ee275bf549fd08fc73f43d97a7f2b5` |
| Krätschmer–Schied–Zähle v6 | `f65dff601a0496adaf65b890f9ff5ae92948df049ee5eafd8d14175750e9d3cf` |
| Wang–Ramdas v6 | `5bd09161af75511620fb2e5983d9ba59c2826a2b9eeac4c7b4e36ccad92b37d0` |
| Holzmann–Eulert v1 reprint | `605fb3af7bbd4b0591b197aeffd0e6a358096ebcaeb9d8359cdd3fe740af0cc0` |
