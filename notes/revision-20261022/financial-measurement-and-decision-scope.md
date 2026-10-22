# Financial measurement and decision scope

22 October 2026. Direction-first, post-result research note. This note changes no target, parameter, prediction, primary comparison or accepted result. Its elementary examples are constructed reasoning checks, not financial observations or a proposed new theorem.

## What the financial question currently supports

The paper studies a passive report for `P(t,H)=max_{0<=h<=H}|N(t+h)|`, where `N` is the source's signed position measurement and the issue record is included. An issued report can be assessed against subsequent recorded magnitudes. That is a definite forecasting task. Its usefulness for an actual risk limit, financing amount or quoting intervention is a further question requiring a measurement and decision link.

The first substantive revision supplied same-response conditional competitors and a second official source. Those additions permit stronger comparisons within each declared task. They cannot identify an unobserved economic objective merely because the reported numbers carry monetary units. The defensible direction is a bounded application and model-validation study; new financial mechanism, operational value and compatible dealer replication remain open.

## Primary-source reading that sharpens the distinction

**Basel Committee on Banking Supervision, _Monitoring tools for intraday liquidity management_, April 2013.** Consulted the official 26-page [PDF](https://www.bis.org/publications/201304-standards-monitoring-tools-intraday-liquidity-management.pdf): extracted introduction/definitions and selected monitoring passages, and visually read physical pp.11–12, printed pp.5–6, paragraphs13–19 and Figure1. This is selected reading, not a full-document or current-jurisdiction compliance review. The measure concerns settlement-account payments, their transaction timestamps and the largest negative cumulative balance. Positive balances represent available liquidity rather than the same funding need. The tool also distinguishes liquidity available at the day's opening. This differs from an absolute client-position or securities-value maximum. The owning record says the standard was consolidated; the historical document is used here only to clarify measurement.

**Duffie, Fleming, Keane, Nelson, Shachar and Van Tassel, _Dealer Capacity and U.S. Treasury Market Functionality_, Staff Report1070, revised October 2023.** Consulted the official 70-page [PDF](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1070.pdf), DOI [10.59576/sr.1070](https://doi.org/10.59576/sr.1070). In addition to earlier selected empirical passages, read AppendixA's opening model through the initial-price example, physical pp.44–45, printed pp.42–43, in extracted text and rendered pages. It connects inventory constraints to future shadow costs through dynamic dealer quotes and demand. The paper's passive forecasts do not estimate those choices or shadow costs. The assumed one-sided capacity and illustrative demand setting are not the current two-sided peak task's fitted economic model.

Downloaded source identities were 349,864 bytes / SHA-256 `7a4c06267ed84ccd789a802152a4c039eb97a1e5b2c5c3846e1da9b6023094a1` and 4,422,404 bytes / SHA-256 `fc0e4244a7c8dbd36656131b78b82711bf63cd2bd6396cf59b92e73e1dddc50e`, respectively. Copyrighted source PDFs and rendered pages remain outside the public repository.

## Three elementary measurement failures

**A net aggregate cannot bound an individual dealer's absolute peak.** For finite dealer paths `N(d,h)` over the same recorded horizon, the triangle inequality gives

```
max_h |sum_d N(d,h)| <= sum_d max_h |N(d,h)|.
```

There is no converse bound with a finite multiplicative constant, even for two dealers: take constant paths `N(1,h)=M` and `N(2,h)=-M`, for any `M>0`. The aggregate peak is zero and the two dealer peaks sum to `2M`. An accurate zero aggregate forecast therefore need not be an accurate report for either dealer. The same arithmetic distinguishes a signed netted book from its gross long-plus-short amount. It does not show that gross exposure is necessarily risky when hedges, prices and contractual netting are unobserved.

**Sampled peaks need not equal peaks between records.** Two continuous paths can agree at every observed timestamp, while one stays zero and the other makes a triangular excursion of arbitrary height between two adjacent records. Both sampled targets are zero. Without an additional rate-of-change or within-record-path restriction, the data impose no finite upper bound on the second path's continuous-time peak. Therefore the H-record response is a sampled measurement; an hourly label or a weekly maximum cannot be promoted to a transaction-time maximum. Keeping the observed gaps is preferable to inventing missing observations, but does not recover unobserved excursions.

**Absolute position and directional funding are different functionals.** As an illustration only, a cumulative cash path `[0,10,0]` has absolute peak10 and no negative net balance; `[0,-10,0]` has the same absolute peak and a negative balance of10. Applying an absolute-peak report to either path gives identical target values while a directional deficit measure differs. The FX `N` is not established to be a cumulative settlement cash balance in the first place. No funding inference follows from this example or from the paper's score.

## What the .95 score does and does not price

For a specified fixed realized path, let a passive allowance `C` have stipulated shortfall and excess losses

```
L(C,P) = c_short * max(P-C,0) + c_excess * max(C-P,0),
c_short > 0, c_excess > 0.
```

With `tau=c_short/(c_short+c_excess)`, this equals `(c_short+c_excess)*rho_tau(P-C)`. Under a specified conditional distribution with finite conditional expected loss (for example, a finite conditional first absolute moment of P), minimizing expected loss over reports gives an appropriate tau-quantile, including the usual possibly nonunique quantile set when atoms occur. The known constraint `C>=B` is coherent when `P>=B` is genuinely known at issue. Thus tau=.95 expresses a stipulated19:1 relative penalty in this simplified report problem.

The interpretation does not establish that a dealer actually faces those prices, that one dollar of overrun costs nineteen dollars of unused allowance, or that current position value equals reserve capital. Financing charges may depend on secured rates, haircuts, direction, duration and available credit. A reserve cost paid on all committed capacity would have to be modeled in its own objective rather than casually identified with `max(C-P,0)`. Nor does a fixed loss ratio establish conditional coverage.

If the report changes quotes, hedges or risk limits, subsequent positions may change too. A passive comparison observes outcomes under the recorded behavior; it does not observe positions under every alternative policy. Fitting a better conditional quantile does not by itself identify that policy effect. A dynamic decision study would require an explicit intervention, additional data or defensible structural assumptions; no such study has been executed here.

## Direction decision

Retain the current peak-response application, the adverse Treasury primary and the inspected-FX qualification. Do not rename the response liquidity usage, economic capacity or optimal funding. Do not add a funding backtest on price data that lack the source's cash flows and financing terms. New compatible dealer records, original-release vintages and measured decisions would answer substantial remaining questions; they cannot be fabricated by adding more algorithms to the existing two measurement processes.

These distinctions make the existing results interpretable and identify what a stronger financial paper would need. They do not turn elementary inequalities, better auditability or a different target into methodological novelty.
