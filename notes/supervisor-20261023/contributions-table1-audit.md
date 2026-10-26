# Table 1: cell-by-cell original-source audit, 23 October 2026

Scope: all 25 cells in the current five-row, five-column Table 1. The two previous literature notes were used to locate URLs only. The original sources below were reopened for this check. No experiment, result file, table generator, generated TeX, or Git state was changed. This note is a recommendation for the manuscript owner to apply.

“Verified PDF” below means that the original PDF was accessible and the relevant cover/body sections were read; it does **not** mean that every page of the source was newly read. “Indexed original” means freshly retrieved passages from the institution-hosted thesis itself, with their printed page/section markers. It is not a secondary summary and is not a claim to have obtained the full thesis PDF. Any final cell without original-source support must be **—**. After the narrow replacements below, no proposed final cell remains unsupported.

## Recommended replacement matrix

| Study | Target | Data | Method | Evaluation |
|---|---|---|---|---|
| Boudoukh et al. (2004) | Quantile of worst portfolio loss by the horizon | Modeled lognormal portfolio paths | Brownian first passage; discrete simulation | Model-implied MaxVaR/VaR ratios; discrete monitoring |
| Petrunia et al. (2019) | Daily maximum net debit across ACSS participants | ACSS daily settlement balances | GEV block maxima; GPD exceedances | Fitted/empirical quantiles; monthly collateral shortfalls |
| van den Hoogen (2017) | Conditional quantile of maximum cumulative payment deficit | ABN AMRO transactions; details confidential | ACD/UHF-GARCH; Monte Carlo paths | Coverage/independence backtests; application details confidential |
| Wisniewski et al. (2020) | Next-hour signed-position interval | One market maker's hourly FX net positions | Quantile/conformal intervals; KNN and other regressions | Two endpoint pinball scores; interval and coverage diagnostics |
| This paper | Two-sided absolute sampled peak quantile | Hourly FX; weekly dealer-position series | Historical rules; QR/KNN on matched histories and updates | Pinball; paired DM; U/V, breaches and elementary scores |

The matrix is concise table wording, not an assertion that every study performs the same type of empirical evaluation. In particular, MaxVaR's evidence is model based. The proposed Wisniewski Data cell describes its own original data and avoids asserting equality between two studies' input files.

## Evidence for every cell

### 1. Boudoukh et al. (2004): verified original PDF

[Author-hosted JOIM original](https://pages.stern.nyu.edu/~rwhitela/papers/maxvar%20joim04.pdf). Page locators in this row refer to the PDF's local printed 1–6 numbering, not the publication-list pagination.

| Cell | Original evidence | Decision |
|---|---|---|
| Study | Cover, PDF p.1: four authors and 2004 volume/year. | Verified. |
| Target | §2, pp.2–3: loss exceeded on or before the horizon; minimum sample-path portfolio value and its distribution. | Verified; “quantile” makes the risk-report object explicit. |
| Data | §2, p.2: portfolio value follows a lognormal diffusion under stated drift/volatility parameters. | Verified; modeled paths, no observed financial dataset claimed. |
| Method | §2 theorem/proof, p.3: Brownian first passage; §3, p.4: simulated discrete monitoring. | Verified. |
| Evaluation | §3, Tables 1–2, p.4 and discussion pp.3–5: MaxVaR/VaR comparisons and discrete-monitoring illustration. | Verified; no realized forecasting-score backtest claimed. |

### 2. Petrunia et al. (2019): verified official PDF

[Payments Canada original, January 2019 update](https://www.paiements.ca/sites/default/files/tail_risk_in_the_automated_clearing_settlement_system_acss.pdf). Its printed page numbers equal the physical PDF page numbers here.

| Cell | Original evidence | Decision |
|---|---|---|
| Study | Cover p.1 and author page p.2: Petrunia, Sabetti, Voia; original September 2018, updated January 2019. | Verified; 2019 identifies the checked version. |
| Target | §2, p.8: daily maximum debit across Direct Clearers; §4(b), p.13 distinguishes this system maximum from participant-specific positions. | Verified; a cross-participant daily maximum, not an intraday path maximum. |
| Data | §2, p.8: ACSS final multilateral settlement balances, January 2002–March 2017. | Verified. |
| Method | §3(a), p.9 and §3(b), p.10: GEV block maxima and GPD threshold exceedances. | Verified. |
| Evaluation | §3(c), p.10: empirical/fitted diagnostics; §4, pp.12–13: quantile comparisons; §4(b), p.13: monthly updating and collateral shortfalls. | Verified. |

The source's contents lists §4 at p.13, but the actual section starts on p.12. The audit follows the body headings.

### 3. van den Hoogen (2017): indexed original cover and body only

[TU Delft institution-hosted original](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f) ([preview URL](https://repository.tudelft.nl/file/File_3c80dabb-c431-47ac-8622-c8709d473c6f?preview=1)). Direct original/preview, resolver, and record requests timed out; an independent direct download with a 20-second timeout also failed. No full thesis PDF was obtained. The following exact original sections were freshly returned by the web index, including their printed page labels.

| Cell | Original evidence | Decision |
|---|---|---|
| Study | Indexed original cover: Sofie van den Hoogen, August 2017. | Verified from original cover text. |
| Target | §5.2, p.59, equation (5.2); definition 5.1 / equation (5.3), p.60: largest within-interval cumulative negative position and its conditional quantile. | Verified from indexed body. |
| Data | Chapter 2, p.5 marks data-description sections confidential; §5.2, p.58 identifies transactions of two ABN AMRO accounts. | Verified; no inaccessible data details inferred. |
| Method | §5.3, p.60: ACD durations, UHF-GARCH net positions, Monte Carlo estimator. | Verified with the specific replacement above. The old generic “EVT” component is not needed for this checked cell. |
| Evaluation | §5.4, p.68, definitions 5.3–5.4 / equations (5.32)–(5.33): UC and IND; §5.5, p.76 marks application sections confidential. Chapter 7, p.92 publicly summarizes 30-day out-of-sample coverage/independence findings. | Verified with the narrower replacement; **reject “Backtesting outcomes withheld” as a blanket statement**. |

The distinction in the Evaluation cell is material. Confidential detailed application sections coexist with public qualitative results in the conclusion. This audit does not claim to have inspected the redacted application tables, numerical rejection counts, or the full thesis. If the owner retains an unsupported additional component instead of the checked Method wording, that component must be omitted or the cell changed to **—** under the user's rule.

### 4. Wisniewski et al. (2020): verified official PDF

[Official PMLR original PDF](https://proceedings.mlr.press/v128/wisniewski20a/wisniewski20a.pdf), [official proceedings metadata](https://proceedings.mlr.press/v128/wisniewski20a.html). Body locators use physical/local PDF pp.1–17; official proceedings pages are 285–301.

| Cell | Original evidence | Decision |
|---|---|---|
| Study | PDF cover p.1 and official proceedings record: Wisniewski, David Lindsay, Sian Lindsay; 2020. | Verified. |
| Target | Introduction, p.2: next-hour market-maker net position; §§2 and 3.4 provide the lower/upper interval constructions. | Verified; signed endpoint, not sampled path peak. |
| Data | §3.1, p.4: one market maker's client-flow positions, five liquid currency pairs, hourly USD observations. | Verified; use direct data description instead of “Same FX source family”. |
| Method | §2, pp.3–4 and §3.3, pp.7–8: CP/NCP/quantile constructions; KNN and other regression engines. | Verified. |
| Evaluation | §3.5, pp.9–10: averaged endpoint pinball scores, width, coverage, Winkler, UC/CC/IND tests; §4 begins p.11. | Verified. |

No equality between its input bytes and this paper's FX input is established by those original passages.

### 5. This paper: current manuscript and retained results, no new calculation

The owning sources are [main.tex](../../manuscript/supervisor-revision/main.tex), [sections.tex](../../manuscript/supervisor-revision/sections.tex), [the E5 manuscript paragraph](../../manuscript/supervisor-revision/generated/e5-summary.tex), [appendices.tex](../../manuscript/supervisor-revision/appendices.tex), [paired-comparisons.csv](../../results/revision-20261022/paired-comparisons.csv), [coverage-verified.csv](../../results/supervisor-20261023/inference/coverage-verified.csv), and [murphy-verified.csv](../../results/supervisor-20261023/inference/murphy-verified.csv), reopened for this check.

| Cell | Owning-source evidence | Decision |
|---|---|---|
| Study | Current manuscript title/author/date identifies this paper. | Verified. |
| Target | §3, target equation: maximum absolute position over recorded horizons including issue, with τ=.95 in §4.1. | Verified. |
| Data | §3: hourly FX client-flow record and NY Fed weekly PDPOSGS-B Treasury-bill aggregate; §6.3/E5 adds 12 archived weekly dealer-position series. | Verified; includes the panel without treating the 13 weekly series as independent replications. |
| Method | §§4.1–4.3: historical rules, ridge QR, KNN; common completed-label pools and refit schedules. | Verified. |
| Evaluation | §5: pinball, U/V, strict breaches and paired HAC/DM; Appendix A.6 and the Murphy CSV check elementary scores at fixed τ=.95. | Verified; no new experiment performed. |

The proposed evaluation wording includes E5's descriptive extension without implying that its panel receives a pooled independence-based DM test. Fixed-τ elementary-score comparisons are distinct from the separate H24 legacy U/V weight crossing. Existing coverage diagnostics remain in the paper even though the concise replacement cell does not list every diagnostic.

## Caption, footnote, and application instructions

Recommended caption:

> Related studies: targets, data, methods and evaluation evidence reported in original sources.

Recommended replacement footnote:

> Van den Hoogen (2017, Section 5.4) specifies coverage and independence backtests. Its detailed application sections (Section 5.5) are confidential, while Chapter 7 provides public qualitative out-of-sample findings.

Do not retain the blanket claim that its backtesting outcomes are withheld, or imply that all numerical or empirical information is inaccessible. Do not label the Delft row as newly verified from a complete PDF. No comparison cell above claims superior performance, clean external validation, source-byte equality, or a newly established theoretical contribution.

Only this new audit note was authored. The manuscript owner is responsible for applying the matrix and footnote to the canonical table data and generated TeX. No builder, tests, numerical analysis, or cross-model review was run for this audit.
