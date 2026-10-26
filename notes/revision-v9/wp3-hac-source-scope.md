# WP3 DM/HAC: source scope and interpretation

Source/code reading completed at 2026-10-24 23:28:23 UTC. This note records a bounded methodological check during the already running WP3 experiment. No financial array values were loaded, no forecasts or tests were run, and no code, frozen protocol, or result was changed. This is partial source reading, not a claim to have read either paper in full.

## Original sources and actual reading scope

**Diebold, Francis X., and Roberto S. Mariano (1995).** “Comparing Predictive Accuracy.” *Journal of Business & Economic Statistics* **13**(3), July, 253–263. DOI: **10.1080/07350015.1995.10524599**. Read: publisher metadata/abstract and indexed original pp. 253–254, including §1.1 only; not full proofs or simulations. The scan's tool extraction was limited. The publisher's 2012 online date is not the publication year. [Publisher](https://doi.org/10.1080/07350015.1995.10524599); [original scan](https://users.ssc.wisc.edu/~bhansen/718/DieboldMariano1995.pdf); [indexed original text](https://citeseerx.ist.psu.edu/document?doi=92e3c28c74f028caacd76835f6dc976b50a93875&repid=rep1&type=pdf).

The asymptotic test concerns zero mean loss differential, including asymmetric losses, under covariance-stationary short-memory conditions and consistent LRV estimation. Its k−1 dependence benchmark may fail in practice. The paper's separate exact tests do not make our normal statistic exact. [Original §1.1, printed p. 254](https://citeseerx.ist.psu.edu/document?doi=92e3c28c74f028caacd76835f6dc976b50a93875&repid=rep1&type=pdf).

**Newey, Whitney K., and Kenneth D. West (1987).** “A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix.” *Econometrica* **55**(3), May, 703–708. DOI: **10.2307/1913610**. Read: author metadata/PDF identity, indexed original p. 703, equations (1)–(4), and the abstract of the distinct April 1986 NBER Technical Working Paper 0055, DOI **10.3386/t0055**; not Theorem 2 or its proof. [Author list](https://users.ssc.wisc.edu/~kdwest/publications/publications.htm); [author-hosted journal PDF](https://www.ssc.wisc.edu/~kwest/publications/1980/A%20Simple%20PSD%20HAC%20Covariance%20Matrix.pdf); [original p. 703 text](https://users.ssc.wisc.edu/~behansen/718/NeweyWest1987.pdf); [working-paper record](https://www.nber.org/papers/t0055).

The source establishes a covariance estimator that is positive semidefinite by construction, with consistency under regularity conditions. Neither that construction nor the abstract establishes finite-sample test size for the present financial loss series. The particular bandwidth below is the already frozen study convention; this note does not attribute its numerical rule or optimality to the 1987 paper. [Newey–West source](https://www.nber.org/papers/t0055).

## Static implementation comparison

The following statements describe the inspected code, not new numerical findings:

- `inference_tests.py::bandwidth` fixes L = min(n−1, max(H, floor(4(n/100)^(2/9)))). No data-selected bandwidth or extra lag experiment is introduced.
- `inference_tests.py::hac` centers each series by its sample mean, uses denominator n for each sample autocovariance, and adds lag pairs with Bartlett weights 1−k/(L+1), k=1,…,L. In one dimension this is γ̂₀ + 2∑ₖ(1−k/(L+1))γ̂ₖ. This is a static algebraic description of the existing code.
- `v9_learning_curve.py::dm_hac_only` uses the paired difference QR pinball minus matched-F pinball, its arithmetic mean, the existing HAC long-run variance, statistic mean/√(LRV/n), and the two-sided normal probability via `erfc`. It does not call the existing `dm_test` wrapper, which also computes HLN statistics.
- Constant/identical differences and nonpositive or nonfinite LRV retain explicit NA statuses; they are not assigned a fabricated p-value. The wrapper does not delete pairs, tune L, or run coverage, bootstrap, or multiple-testing procedures.

## Boundaries for the manuscript

Overlapping peak horizons and repeated fits on overlapping training histories can create loss dependence beyond a horizon-only benchmark. This is an inference from the study's forecast construction, not a measured dependence result. L≥H does not establish that the chosen L captures all relevant dependence; the original DM discussion itself cautions against treating forecast-horizon dependence as universal. [Diebold–Mariano §1.1](https://citeseerx.ist.psu.edu/document?doi=92e3c28c74f028caacd76835f6dc976b50a93875&repid=rep1&type=pdf).

Use **pointwise, nominal, post-result diagnostics conditional on the fixed specification**. Stationarity/short memory, the moments needed for the limit theory, and positive long-run variance are working premises, not consequences of a small p-value. The implementation supplies no finite-sample guarantee, familywise guarantee across W/H/methods, correction for earlier specification exploration, untouched-holdout claim, or causal confirmation of the mechanism. These are limitations of this design and implementation; no additional test or protocol change is proposed here.
