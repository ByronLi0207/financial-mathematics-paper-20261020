# Consolidated final-jof extended results

The current manuscript is in `submission-final/`. This index preserves exact overflow source blocks from the v12 backbone while the compact Supplement is prepared. The original complete [v12 Supplement](submission-v10/supplement.pdf) and [editable source](submission-v10/supplement.tex) remain unchanged. These are retained historical evidence, not additional analyses.

## Original-to-compact section map

| Original section | Topic | Current location |
|---|---|---|
| S1 | Known-floor projection and strict quantile coverage | Compact Supplement S1 |
| S2 | Classical endpoint-to-peak bound | Compact Supplement S2 |
| S3 | Monte Carlo mechanisms: original increment persistence | [Exact overflow source](notes/final-merge/wp4-relocation/original-S03.tex) |
| S4 | Mean-reverting levels and negative-increment sensitivities | [Exact overflow source](notes/final-merge/wp4-relocation/original-S04.tex) |
| S5 | All secondary simulation sensitivities | [Exact overflow source](notes/final-merge/wp4-relocation/original-S05.tex) |
| S6 | Empirical endpoint plug-in: all original cells | [Exact overflow source](notes/final-merge/wp4-relocation/original-S06.tex) |
| S7 | AR residual replay and its adverse comparisons | [Exact overflow source](notes/final-merge/wp4-relocation/original-S07.tex) |
| S8 | Ordinary quantile ranks and minimizer endpoints | Compact Supplement S3 |
| S9 | Fixed-report error preferences | [Exact overflow source](notes/final-merge/wp4-relocation/original-S09.tex) |
| S10 | Complete preference-frontier source | [Exact overflow source](notes/final-merge/wp4-relocation/original-S10.tex) |
| S11 | Complete weekly panel: definitions and first half | [Exact overflow source](notes/final-merge/wp4-relocation/original-S11.tex) |
| S12 | Complete weekly panel: second half | [Exact overflow source](notes/final-merge/wp4-relocation/original-S12.tex) |
| S13 | Complete added-panel endpoint-plug-in comparison | [Exact overflow source](notes/final-merge/wp4-relocation/original-S13.tex) |
| S14 | Earlier-period fixed selection rules | [Exact overflow source](notes/final-merge/wp4-relocation/original-S14.tex) |
| S15 | Selection failures and replication boundaries | [Exact overflow source](notes/final-merge/wp4-relocation/original-S15.tex) |
| S16 | Finite delayed calibration and headroom SAV | [Exact overflow source](notes/final-merge/wp4-relocation/original-S16.tex) |
| S17 | Wrapper comparisons, uncertainty and missing cells | [Exact overflow source](notes/final-merge/wp4-relocation/original-S17.tex) |
| S18 | Untuned forecast combinations | [Exact overflow source](notes/final-merge/wp4-relocation/original-S18.tex) |
| S19 | Combination Murphy diagrams and comparison families | [Exact overflow source](notes/final-merge/wp4-relocation/original-S19.tex) |
| S20 | Training-defined position-change states | [Exact overflow source](notes/final-merge/wp4-relocation/original-S20.tex) |
| S21 | Refitted target-level sensitivities | [Exact overflow source](notes/final-merge/wp4-relocation/original-S21.tex) |
| S22 | Horizon coherence and late conditional-hit evidence | Compact Supplement S4 |
| S23 | Numerical implementation and inference conventions | Compact Supplement S5 |
| S24 | Frozen controlled comparison of inherited procedures | Compact Supplement S6 |
| S25 | Same-dealer completed-day aggregation | Compact Supplement S7 |
| S26 | Fixed-parameter full-prefix backcast and overlapping windows | Compact Supplement S8 |
| S27 | Earlier calibrated simulation and numerical failures | [Exact overflow source](notes/final-merge/wp4-relocation/original-S27.tex) |
| S28 | Pre-evaluation stability screen and switching stress simulation | [Exact overflow source](notes/final-merge/wp4-relocation/original-S28.tex) |
| S29 | Paired menu isolation: full source inventory | Compact Supplement S9 |
| S30 | CFTC sources, eligibility and information dates | Compact Supplement S10 |
| S31 | Complete model confidence sets | Compact Supplement S11 |
| S32 | Fixed limit costs and full parameter regions | Compact Supplement S12 |
| S33 | Retained accuracy and hit diagnostics | [Exact overflow source](notes/final-merge/wp4-relocation/original-S33.tex) |
| S34 | Reproduction, availability and retained extended results | Compact Supplement S13 |
| S35 | Additional saved evidence on history length | Compact Supplement S14 |
| S36 | Retained scope details and additional empirical checks | Compact Supplement S15 |

## Exact relocated section sources

The linked editable .tex copies are byte-identical to their original sections in the v12 Supplement. The code fences below reproduce that content with trailing blank lines normalized for Markdown. Hashes refer to the exact editable copies. Generated table/figure dependencies remain in the original package; no result is recalculated.

### Original Supplement S3: Monte Carlo mechanisms: original increment persistence

Original source: `submission-v10/supplement.tex`; SHA-256 `e52841805a0af5fb56920e6221f7f84cff7f870b46bbe1a8d5bb0cba3ed5b343`.

```latex
\section{Monte Carlo mechanisms: original increment persistence}\label{sup:simulation-original}

These are the existing fixed-seed Gaussian experiments, not newly run
simulations or calibrated replicas of either financial source. Every reported
rate is a probability, not a percentage. The peak includes the initial level;
the endpoint event concerns absolute displacement from that initial level.
Each path cell has 100000 paths.
L/Stat starts the level AR in stationarity; L/Abs fixes its absolute-level
tail anchor; L/Sig is the separate signed-level tail-anchor sensitivity.
I/Zero accumulates stationary AR increments from a zero position.
M denotes a stationary-marginal endpoint threshold; C denotes a distinct
fixed-start conditional endpoint oracle. Threshold partners sharing a seed use
the same paths, not independent repetitions.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrrrr}
\caption{Original increment-autoregression simulation, unchanged. Serial persistence here concerns increments, not fitted position levels.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endhead
\bottomrule
\endfoot
6 & 0.00 & I/Zero & 20267023 & 5.490 & 3035 & 0.03035 & 0.00054 & 0.02454 \\
6 & 0.70 & I/Zero & 20267093 & 10.092 & 2597 & 0.02597 & 0.00050 & 0.02573 \\
6 & 0.85 & I/Zero & 20267108 & 11.634 & 2550 & 0.02550 & 0.00050 & 0.02550 \\
6 & 0.98 & I/Zero & 20267121 & 13.190 & 2557 & 0.02557 & 0.00050 & 0.02557 \\
24 & 0.00 & I/Zero & 20285023 & 10.981 & 3819 & 0.03819 & 0.00061 & 0.02504 \\
24 & 0.70 & I/Zero & 20285093 & 24.599 & 2772 & 0.02772 & 0.00052 & 0.02475 \\
24 & 0.85 & I/Zero & 20285108 & 33.394 & 2619 & 0.02619 & 0.00051 & 0.02525 \\
24 & 0.98 & I/Zero & 20285121 & 49.784 & 2572 & 0.02572 & 0.00050 & 0.02572 \\
\end{longtable}
\endgroup

The independent-increment rows satisfy the classical premise.
Positive increment coefficients violate independence without necessarily causing
a numerical breach of the bound. Their favorable rates are not a general
result for serial dependence.
```

### Original Supplement S4: Mean-reverting levels and negative-increment sensitivities

Original source: `submission-v10/supplement.tex`; SHA-256 `d86e012addc74c19a521ad3e1a6df4d67d4a9885ff8a0ea8968d91ad9d97970b`.

```latex
\section{Mean-reverting levels and negative-increment sensitivities}\label{sup:simulation-primary}

The corrected level process is
\(N_h=\phi N_{h-1}+\varepsilon_h\), with independent Gaussian innovations
of variance \(1-\phi^2\) and unit stationary level variance. Its stationary
increments have lag correlation
\(\rho_X(k)=-(1-\phi)\phi^{k-1}/2\), so this mechanism differs from a
positively persistent increment AR. The fitted financial coefficient describes
levels, making the level equation the relevant illustrative mechanism.
The negative-increment family is a separate sensitivity, with stationary
increments and nonstationary cumulative levels.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrrrr}
\caption{All corrected primary cases. Mean-reverting level rates are conservative in these finite cases; the negative-increment result must also be retained.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endhead
\bottomrule
\endfoot
6 & 0.68 & L/Stat/M & 20567123 & 3.009 & 175 & 0.00175 & 0.00013 & 0.02462 \\
6 & 0.68 & L/Abs/M & 20567124 & 3.009 & 0 & 0.00000 & 0.00000 & 0.10447 \\
6 & 0.85 & L/Stat/M & 20567133 & 2.502 & 300 & 0.00300 & 0.00017 & 0.02553 \\
6 & 0.85 & L/Abs/M & 20567134 & 2.502 & 14 & 0.00014 & 0.00004 & 0.08227 \\
6 & 0.98 & L/Stat/M & 20567143 & 1.071 & 913 & 0.00913 & 0.00030 & 0.02434 \\
6 & 0.98 & L/Abs/M & 20567144 & 1.071 & 372 & 0.00372 & 0.00019 & 0.03623 \\
6 & -0.30 & I/Zero/M & 20567223 & 4.244 & 3563 & 0.03563 & 0.00059 & 0.02524 \\
6 & -0.60 & I/Zero/M & 20567233 & 3.127 & 4439 & 0.04439 & 0.00065 & 0.02558 \\
24 & 0.68 & L/Stat/M & 20585123 & 3.170 & 636 & 0.00636 & 0.00025 & 0.02495 \\
24 & 0.68 & L/Abs/M & 20585124 & 3.170 & 1 & 0.00001 & 0.00001 & 0.11416 \\
24 & 0.85 & L/Stat/M & 20585133 & 3.138 & 402 & 0.00402 & 0.00020 & 0.02520 \\
24 & 0.85 & L/Abs/M & 20585134 & 3.138 & 1 & 0.00001 & 0.00001 & 0.11159 \\
24 & 0.98 & L/Stat/M & 20585143 & 1.965 & 768 & 0.00768 & 0.00028 & 0.02468 \\
24 & 0.98 & L/Abs/M & 20585144 & 1.965 & 85 & 0.00085 & 0.00009 & 0.06201 \\
24 & -0.30 & I/Zero/M & 20585223 & 8.167 & 4281 & 0.04281 & 0.00064 & 0.02476 \\
24 & -0.60 & I/Zero/M & 20585233 & 5.701 & 5032 & 0.05032 & 0.00069 & 0.02516 \\
\end{longtable}
\endgroup

All saved level cases have peak rates below the nominal threshold.
The largest negative-increment point estimate occurs at the longer horizon and
the more negative coefficient. Its rate is 0.05032,
with a saved excess of 0.032
percentage points and Monte Carlo SE 0.00069.
This does not demonstrate a population failure. General dependence invalidates the
classical premise regardless of the observed direction. Zero observed counts
also do not establish zero population probability.
```

### Original Supplement S5: All secondary simulation sensitivities

Original source: `submission-v10/supplement.tex`; SHA-256 `bc7ff7c23a1090c1b52f0080c205620bcc40a812fda05c93a1505ab128e3798a`.

```latex
\section{All secondary simulation sensitivities}\label{sup:simulation-secondary}

For stationary random starts, absolute endpoint displacement has
variance \(2(1-\phi^H)\). At a fixed start \(x\), its conditional Gaussian
mean and variance are \((\phi^H-1)x\) and \(1-\phi^{2H}\). Thus holding the
stationary-marginal endpoint threshold across starts does not condition on a
large anchor. The conditional-oracle sensitivities below are distinct thresholds
on shared paths; neither is an oracle for the maximum.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrrrr}
\caption{All secondary anchor and conditional-threshold sensitivities. Conditional and marginal endpoint calibration remain distinct.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Horizon & \shortstack{Persistence\\\(\phi\)} & Process & Seed & \shortstack{Endpoint\\threshold} & \shortstack{Peak\\breaches} & \shortstack{Peak breach\\probability} & \shortstack{Monte Carlo\\standard error} & \shortstack{Endpoint breach\\probability} \\
\midrule
\endhead
\bottomrule
\endfoot
6 & 0.68 & L/Abs/C & 20567124 & 3.717 & 0 & 0.00000 & 0.00000 & 0.02411 \\
6 & 0.68 & L/Sig/M & 20567125 & 3.009 & 2 & 0.00002 & 0.00001 & 0.06261 \\
6 & 0.68 & L/Sig/C & 20567125 & 3.433 & 1 & 0.00001 & 0.00001 & 0.02476 \\
6 & 0.85 & L/Abs/C & 20567134 & 3.036 & 0 & 0.00000 & 0.00000 & 0.02488 \\
6 & 0.85 & L/Sig/M & 20567135 & 2.502 & 21 & 0.00021 & 0.00005 & 0.05689 \\
6 & 0.85 & L/Sig/C & 20567135 & 2.840 & 4 & 0.00004 & 0.00002 & 0.02607 \\
6 & 0.98 & L/Abs/C & 20567144 & 1.146 & 215 & 0.00215 & 0.00015 & 0.02503 \\
6 & 0.98 & L/Sig/M & 20567145 & 1.071 & 464 & 0.00464 & 0.00021 & 0.03184 \\
6 & 0.98 & L/Sig/C & 20567145 & 1.117 & 340 & 0.00340 & 0.00018 & 0.02521 \\
24 & 0.68 & L/Abs/C & 20585124 & 3.920 & 0 & 0.00000 & 0.00000 & 0.02567 \\
24 & 0.68 & L/Sig/M & 20585125 & 3.170 & 9 & 0.00009 & 0.00003 & 0.06486 \\
24 & 0.68 & L/Sig/C & 20585125 & 3.605 & 1 & 0.00001 & 0.00001 & 0.02514 \\
24 & 0.85 & L/Abs/C & 20585134 & 3.880 & 0 & 0.00000 & 0.00000 & 0.02495 \\
24 & 0.85 & L/Sig/M & 20585135 & 3.138 & 3 & 0.00003 & 0.00002 & 0.06306 \\
24 & 0.85 & L/Sig/C & 20585135 & 3.571 & 0 & 0.00000 & 0.00000 & 0.02484 \\
24 & 0.98 & L/Abs/C & 20585144 & 2.298 & 20 & 0.00020 & 0.00004 & 0.02518 \\
24 & 0.98 & L/Sig/M & 20585145 & 1.965 & 146 & 0.00146 & 0.00012 & 0.04607 \\
24 & 0.98 & L/Sig/C & 20585145 & 2.179 & 56 & 0.00056 & 0.00007 & 0.02556 \\
\end{longtable}
\endgroup

The complete correction contains 34 threshold rows on 22 initialized path samples.
The retained CSV and portable readback provide exact endpoint moments,
deviations from the nominal probability, and the single-prespecified-row bound
for zero counts. None estimates financial innovation laws, changing fitted
parameters or empirical-quantile uncertainty.
```

### Original Supplement S6: Empirical endpoint plug-in: all original cells

Original source: `submission-v10/supplement.tex`; SHA-256 `d560aba02ece539795d3af8d990a4287ffc578124162424656dd9d10f0e51427`.

```latex
\section{Empirical endpoint plug-in: all original cells}\label{sup:levy-empirical}

The endpoint plug-in uses each completed historical episode's
absolute endpoint displacement and adds its specified empirical quantile to
the actual current-position floor. It shares the historical rule's completed
origin pool and fixed refit schedule, with no fitted tuning parameter.
The operational empirical rank and overlapping financial history are distinct
from the known population quantile in the classical proposition. The report
therefore has to earn its financial coverage and score performance empirically.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrr}
\caption{Every original-cell endpoint plug-in comparison. A population bound does not imply a lower empirical pinball score.}\\
\toprule
Source & \shortstack{Horizon /\\history} & \shortstack{Endpoint vs\\historical (\%)} & \shortstack{Endpoint vs\\regression (\%)} & \shortstack{Breaches\\endpoint / historical} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Horizon /\\history} & \shortstack{Endpoint vs\\historical (\%)} & \shortstack{Endpoint vs\\regression (\%)} & \shortstack{Breaches\\endpoint / historical} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6/720 & 30.93 & 33.76 & 101/332 \\
FX & 6/2880 & 30.39 & 52.98 & 75/360 \\
FX & 24/720 & 10.85 & -15.71 & 136/427 \\
FX & 24/2880 & 7.94 & 12.16 & 174/357 \\
Bills & 6/52 & 3.37 & -43.62 & 10/11 \\
Bills & 6/260 & -11.77 & -41.49 & 15/28 \\
Bills & 24/52 & 26.32 & -61.42 & 42/33 \\
Bills & 24/260 & 9.87 & -47.64 & 22/12 \\
\end{longtable}
\endgroup

\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrr}
\caption{All separate endpoint-plug-in working-reference contrasts. Adverse score comparisons remain alongside lower-breach reports.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Reference & \shortstack{Loss-test\\statistic} & \shortstack{Normal\\p-value} & \shortstack{Small-sample\\p-value} & \shortstack{Holm-adjusted\\p-value} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Reference & \shortstack{Loss-test\\statistic} & \shortstack{Normal\\p-value} & \shortstack{Small-sample\\p-value} & \shortstack{Holm-adjusted\\p-value} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6/720 & F & 7.891 & 2.988e-15 & 3.658e-15 & 4.483e-14 \\
FX & 6/720 & QR & 6.608 & 3.908e-11 & 4.37e-11 & 5.081e-10 \\
FX & 6/2880 & F & 7.790 & 6.695e-15 & 8.123e-15 & 9.373e-14 \\
FX & 6/2880 & QR & 12.832 & 1.089e-37 & 3.451e-37 & 1.743e-36 \\
FX & 24/720 & F & 1.848 & 0.06462 & 0.06562 & 0.5169 \\
FX & 24/720 & QR & -1.673 & 0.09434 & 0.09556 & 0.6604 \\
FX & 24/2880 & F & 2.058 & 0.03958 & 0.04032 & 0.3958 \\
FX & 24/2880 & QR & 1.530 & 0.1259 & 0.1273 & 0.7002 \\
Bills & 6/52 & F & 0.971 & 0.3317 & 0.3422 & 0.7002 \\
Bills & 6/52 & QR & -2.778 & 0.005471 & 0.006887 & 0.06018 \\
Bills & 6/260 & F & -1.345 & 0.1785 & 0.1884 & 0.7002 \\
Bills & 6/260 & QR & -3.031 & 0.002441 & 0.003236 & 0.02929 \\
Bills & 24/52 & F & 1.569 & 0.1167 & 0.1522 & 0.7002 \\
Bills & 24/52 & QR & -1.991 & 0.04645 & 0.06948 & 0.418 \\
Bills & 24/260 & F & 1.092 & 0.2746 & 0.3183 & 0.7002 \\
Bills & 24/260 & QR & -1.516 & 0.1294 & 0.1664 & 0.7002 \\
\end{longtable}
\endgroup

The family and its doubled-bandwidth sensitivities are separate
from the original regression family. The complete tables keep every adverse
direction; no negative comparison is removed by describing the population
inequality as conservative. The linked records preserve source-reported mean
error amounts and every numerical status.
```

### Original Supplement S7: AR residual replay and its adverse comparisons

Original source: `submission-v10/supplement.tex`; SHA-256 `1321ed878d3da763d4a8da2a73b5129b05c31c96d9dde06a50d99a5efc21b909`.

```latex
\section{AR residual replay and its adverse comparisons}\label{sup:ar}

At each original refit, estimate an intercept-bearing level recursion
using each unique mature adjacent transition once. Replaying a historical ordered
residual block from the current position gives the exact algebraic identity
\[
M_{i,h}(x)=N_{i+h}+\widehat\phi^{\,h}(x-N_i),\qquad M_{i,0}(x)=x.
\]
The empirical peak uses the same completed scenario origins, response rank,
floor and refit schedule as its matched historical controls. Finite negative or
above-unit coefficients were eligible, not clipped; all observed fitted
coefficients in the archived run happened to lie inside the unit interval.
Their descriptive means are not identified data-generating parameters.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrr}
\caption{Complete original autoregressive replay comparison. Lower scores can accompany more strict breaches.}\\
\toprule
Source & Horizon & History & \shortstack{Mean fitted\\\(\widehat\phi\)} & \shortstack{Replay vs\\translated (\%)} & \shortstack{Replay vs\\regression (\%)} & \shortstack{Breaches\\replay / translated} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & Horizon & History & \shortstack{Mean fitted\\\(\widehat\phi\)} & \shortstack{Replay vs\\translated (\%)} & \shortstack{Replay vs\\regression (\%)} & \shortstack{Breaches\\replay / translated} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6 & 720 & 0.981 & -1.54 & 2.45 & 282/255 \\
FX & 6 & 2880 & 0.985 & -0.55 & 16.20 & 338/268 \\
FX & 24 & 720 & 0.981 & 2.39 & -25.32 & 401/289 \\
FX & 24 & 2880 & 0.985 & 5.15 & 8.68 & 444/292 \\
Bills & 6 & 52 & 0.676 & -13.44 & -52.66 & 22/11 \\
Bills & 6 & 260 & 0.847 & -18.89 & -47.21 & 31/28 \\
Bills & 24 & 52 & 0.711 & 35.13 & -59.43 & 56/33 \\
Bills & 24 & 260 & 0.850 & -24.12 & -63.86 & 59/12 \\
\end{longtable}
\endgroup

The replay improves on original regression in every original Treasury
cell but loses in most FX cells. Its comparisons with the translated-path rule
have mixed directions, while strict breaches increase in every row above.
Sparse-grid and annual signs can reverse. The full paired, annual and fixed-grid
tables remain in \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261022/ar1-replay/README.md}{the AR archive}.
These are post-result / exploratory same-data calculations, not independent
validation.
```

### Original Supplement S9: Fixed-report error preferences

Original source: `submission-v10/supplement.tex`; SHA-256 `f53fa3bc33267b2e86ccb8291bf2b1e6f566b8888892234957632f278da9ef3c`.

```latex
\section{Fixed-report error preferences}\label{sup:preference}

For a fixed report, changing the loss weight traces a line
\(R_a=aU+(1-a)V\). Here, \(U=\operatorname{mean}(P-C)_+\) is mean underprediction and
\(V=\operatorname{mean}(C-P)_+\) is mean unused allowance. These are passive error amounts over all
origins, not observed funding costs. Breach frequency averages an indicator and
need not rank reports like either amount. The following source-reported monetary
values are never pooled across FX and weekly aggregates.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{2.50}
\begin{longtable}{p{30mm}rrrrp{32mm}}
\caption{The four fixed headline comparisons. The longer-horizon FX result is sensitive to error weights.}\\
\toprule
Comparison & \shortstack{Under-\\prediction\\left} & \shortstack{Under-\\prediction\\right} & \shortstack{Unused\\allowance\\left} & \shortstack{Unused\\allowance\\right} & \shortstack{Equal-loss\\weight \(a\)} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Comparison & \shortstack{Under-\\prediction\\left} & \shortstack{Under-\\prediction\\right} & \shortstack{Unused\\allowance\\left} & \shortstack{Unused\\allowance\\right} & \shortstack{Equal-loss\\weight \(a\)} \\
\midrule
\endhead
\bottomrule
\endfoot
fx\_h6\_primary & 156123.03 & 166531.06 & 4750560.18 & 5671390.59 & none \\
fx\_h6\_matched & 156123.03 & 185672.23 & 4750560.18 & 5526087.27 & none \\
fx\_h24\_legacy & 317678.12 & 149813.88 & 8658017.18 & 12121206.97 & \(\dfrac{86579744869851975}{90776350660766843}\) \\
treasury\_h6\_primary & 3131.86 & 1395.64 & 23688.09 & 28656.17 & \(\dfrac{24840389716843550}{33521504184965797}\) \\
\end{longtable}
\endgroup

The equality column gives exact saved rational boundaries for the mixture
weight defined above, not newly estimated costs. The short-horizon FX primary reduces both mean error amounts;
its elementary-score curves can nevertheless cross because a Murphy diagram
varies the elementary score threshold, a different comparison from reweighting
these two unconditional amounts. The longer-horizon FX legacy pair reverses
near the loss-weight ratio reported in the main text. Actual decision costs
were not observed.

The linked complete frontiers include every open region and every boundary tie.
The full and sparse samples remain separate, and feasible reports outside the
specified menu are not part of these menu-relative envelopes. All pairwise
relations, dominated labels and exact arithmetic are additionally preserved in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261022/preference-robustness/README.md}{the preference archive}.
```

### Original Supplement S10: Complete preference-frontier source

Original source: `submission-v10/supplement.tex`; SHA-256 `4e1d56dea791cd4c3f07097d09d4d320b4d6fe3d6d3c1b86ebea0a81c7cb808f`.

```latex
\section{Complete preference-frontier source}\label{sup:frontier-0}\label{sup:frontier-8}
The complete full-sample and fixed sparse-grid frontiers retain every boundary tie and open region. Their unchanged tables appear in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/0d2526cc69092c5158437a0509613bac5e86d47f/submission-jof/supplement.pdf}{v9 Supplement, Tables S9--S10}, and the exact rational source fields remain in the linked preference results. This supplement retains the error amounts and reversal above, while allocating the full new-method comparison tables below. No preference result was recomputed or removed from the repository.
```

### Original Supplement S11: Complete weekly panel: definitions and first half

Original source: `submission-v10/supplement.tex`; SHA-256 `8795b9f2a2563c96f3e5a17538cbdbb1c9867fe066a91956fa500fb2442415a2`.

```latex
\section{Complete weekly panel: definitions and first half}\label{sup:panel}

Each cell compares the same peak target, completed-label pool,
origin sequence, fixed refit schedule and native monetary units. The original
full regression, smaller predictor regression, expanded-ridge full regression
and ordinary empirical report all remain visible. The additional series are
related weekly aggregates, not independent individual-dealer replications.
Changes in predictors and changes in the ridge menu are distinct interventions.
Every listed comparison is post-result / exploratory.

The historical column gives mean pinball loss and strict hits. Other columns
give the saved percentage loss difference against that same historical rule and
strict hits; negative percentages favor the column method. Original full
regression, four-feature regression and expanded-menu full regression are
distinct fitted procedures (result codes QR33, QR4 and QR33+, respectively).
I is the ordinary
empirical-quantile report, with the endpoint qualification in Section~\ref{sup:rank}.
Across the archived panel, expanded full-regression median excess
loss is 9.22 percent,
compared with 92.63 percent for the original menu. Expanded regression still loses in 34 cells.
This improvement does not erase the remaining failures or identify a causal
feature effect.\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{p{26mm}rrrrrr}
\caption{Complete panel, first half. Additional regularization leaves substantial adverse cases.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Historical\\loss / breaches} & \shortstack{Original\\regression\\\% / hits} & \shortstack{Four-feature\\regression\\\% / hits} & \shortstack{Expanded-menu\\regression\\\% / hits} & \shortstack{Empirical\\\% / breaches} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Historical\\loss / breaches} & \shortstack{Original\\regression\\\% / hits} & \shortstack{Four-feature\\regression\\\% / hits} & \shortstack{Expanded-menu\\regression\\\% / hits} & \shortstack{Empirical\\\% / breaches} \\
\midrule
\endhead
\bottomrule
\endfoot
PDPOSMBS-TOT & 6/52 & 921.7 / 21 & 170.97 / 101 & 3.24 / 27 & 5.82 / 28 & 3.26 / 27 \\
PDPOSMBS-TOT & 6/260 & 945.6 / 26 & 7.36 / 19 & 1.17 / 27 & 7.36 / 19 & 1.96 / 27 \\
PDPOSMBS-TOT & 24/52 & 1753.7 / 39 & 215.55 / 145 & 5.09 / 43 & 66.24 / 104 & 3.49 / 42 \\
PDPOSMBS-TOT & 24/260 & 1611.9 / 25 & 26.79 / 29 & 1.04 / 26 & 0.72 / 24 & 1.14 / 26 \\
PDPOSCS-TOT & 6/52 & 530.3 / 16 & 52.75 / 48 & -5.79 / 23 & -4.70 / 23 & -6.28 / 23 \\
PDPOSCS-TOT & 6/260 & 399.7 / 6 & 1.90 / 15 & -1.10 / 6 & -0.95 / 8 & -1.56 / 7 \\
PDPOSCS-TOT & 24/52 & 579.4 / 16 & 73.78 / 63 & 1.85 / 24 & 2.97 / 25 & 2.12 / 23 \\
PDPOSCS-TOT & 24/260 & 569.9 / 6 & 27.46 / 3 & -3.38 / 6 & -3.06 / 5 & -4.68 / 6 \\
PDPOSFGS-TOT & 6/52 & 400.7 / 16 & 107.22 / 77 & -4.15 / 24 & -4.29 / 20 & -4.98 / 18 \\
PDPOSFGS-TOT & 6/260 & 358.3 / 6 & -1.08 / 14 & 4.88 / 9 & -6.04 / 6 & -1.54 / 6 \\
PDPOSFGS-TOT & 24/52 & 476.2 / 36 & 128.67 / 64 & 13.36 / 37 & 10.67 / 37 & 4.52 / 38 \\
PDPOSFGS-TOT & 24/260 & 354.0 / 9 & 30.02 / 21 & 72.24 / 26 & -0.97 / 10 & -1.50 / 9 \\
PDPOSTIPS-L2 & 6/52 & 287.3 / 26 & 217.18 / 125 & 6.74 / 29 & 2.64 / 28 & 1.69 / 26 \\
PDPOSTIPS-L2 & 6/260 & 269.3 / 24 & 66.28 / 45 & 1.78 / 25 & 66.28 / 45 & 1.63 / 25 \\
PDPOSTIPS-L2 & 24/52 & 641.0 / 48 & 307.36 / 181 & 24.88 / 69 & 152.16 / 146 & 1.88 / 49 \\
PDPOSTIPS-L2 & 24/260 & 532.2 / 47 & 226.91 / 147 & 11.41 / 59 & 226.91 / 147 & 1.84 / 51 \\
PDPOSTIPS-G11 & 6/52 & 42.3 / 23 & 196.70 / 118 & 1.71 / 29 & 6.68 / 41 & -1.13 / 26 \\
PDPOSTIPS-G11 & 6/260 & 41.8 / 14 & 90.31 / 38 & 63.18 / 29 & -1.52 / 13 & -2.53 / 14 \\
PDPOSTIPS-G11 & 24/52 & 80.8 / 61 & 218.69 / 123 & 135.59 / 103 & 64.63 / 78 & -0.01 / 63 \\
PDPOSTIPS-G11 & 24/260 & 51.2 / 9 & 98.59 / 33 & 37.18 / 30 & 98.59 / 33 & -1.09 / 10 \\
PDPOSTIPS-G2 & 6/52 & 181.3 / 16 & 208.61 / 96 & 8.58 / 21 & 35.47 / 41 & 3.33 / 19 \\
PDPOSTIPS-G2 & 6/260 & 179.4 / 19 & 63.47 / 36 & 10.78 / 24 & 63.47 / 36 & -0.29 / 19 \\
PDPOSTIPS-G2 & 24/52 & 377.9 / 31 & 277.81 / 131 & 11.77 / 42 & 40.47 / 60 & -3.63 / 33 \\
PDPOSTIPS-G2 & 24/260 & 286.0 / 23 & 109.33 / 66 & 120.12 / 58 & 109.33 / 66 & 0.29 / 23 \\
\end{longtable}
\endgroup
```

### Original Supplement S12: Complete weekly panel: second half

Original source: `submission-v10/supplement.tex`; SHA-256 `15dfda3a560bcff24399746d5fbc9189da2a66ebb73ad1eb6d3c80144ee57597`.

```latex
\section{Complete weekly panel: second half}\label{sup:panel-second}

The second half follows the identical convention. All original
and expanded results remain unchanged. Cross-series dependence, aggregation
offsets, native-unit differences and overlapping economic positions preclude
treating these cells as independent replications. Forecasts are fitted
separately; observations and losses are not pooled into a single financial
population.\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{p{26mm}rrrrrr}
\caption{Complete panel, second half. The enlarged penalty menu is not uniformly better than historical rules.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Historical\\loss / breaches} & \shortstack{Original\\regression\\\% / hits} & \shortstack{Four-feature\\regression\\\% / hits} & \shortstack{Expanded-menu\\regression\\\% / hits} & \shortstack{Empirical\\\% / breaches} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Historical\\loss / breaches} & \shortstack{Original\\regression\\\% / hits} & \shortstack{Four-feature\\regression\\\% / hits} & \shortstack{Expanded-menu\\regression\\\% / hits} & \shortstack{Empirical\\\% / breaches} \\
\midrule
\endhead
\bottomrule
\endfoot
PDPOSTIPS-G6L11 & 6/52 & 133.6 / 9 & 59.30 / 73 & -1.65 / 12 & -2.52 / 13 & -0.79 / 12 \\
PDPOSTIPS-G6L11 & 6/260 & 114.9 / 4 & -5.72 / 14 & -1.11 / 4 & -1.17 / 4 & -1.00 / 4 \\
PDPOSTIPS-G6L11 & 24/52 & 147.0 / 10 & 76.48 / 92 & -0.97 / 16 & -2.43 / 17 & 0.44 / 15 \\
PDPOSTIPS-G6L11 & 24/260 & 133.8 / 2 & -26.42 / 1 & -1.30 / 2 & -1.33 / 2 & -0.55 / 2 \\
PDPOSGSC-L2 & 6/52 & 1232.9 / 15 & 215.90 / 129 & -3.85 / 23 & 215.90 / 129 & -2.12 / 19 \\
PDPOSGSC-L2 & 6/260 & 1247.4 / 15 & 64.40 / 40 & 9.04 / 20 & 2.20 / 20 & 0.61 / 17 \\
PDPOSGSC-L2 & 24/52 & 2270.8 / 46 & 276.55 / 165 & 182.80 / 96 & 131.63 / 93 & 5.02 / 55 \\
PDPOSGSC-L2 & 24/260 & 2918.7 / 33 & 41.60 / 55 & -0.19 / 33 & 0.12 / 32 & 0.14 / 34 \\
PDPOSGSC-G2L3 & 6/52 & 792.4 / 24 & 121.15 / 93 & 145.25 / 112 & 25.51 / 40 & 3.86 / 28 \\
PDPOSGSC-G2L3 & 6/260 & 1004.0 / 28 & 21.31 / 44 & 22.62 / 59 & 21.31 / 44 & 0.23 / 30 \\
PDPOSGSC-G2L3 & 24/52 & 2101.9 / 47 & 112.95 / 135 & 129.55 / 151 & 112.95 / 135 & 1.78 / 54 \\
PDPOSGSC-G2L3 & 24/260 & 2677.0 / 55 & 11.60 / 64 & 39.73 / 91 & -2.06 / 52 & 1.93 / 55 \\
PDPOSGSC-G3L6 & 6/52 & 764.9 / 12 & 87.61 / 82 & 75.44 / 72 & 10.10 / 29 & -4.25 / 15 \\
PDPOSGSC-G3L6 & 6/260 & 699.1 / 20 & 0.79 / 15 & 1.91 / 21 & 0.79 / 15 & 2.27 / 22 \\
PDPOSGSC-G3L6 & 24/52 & 977.4 / 38 & 544.34 / 137 & 299.12 / 120 & 19.44 / 47 & 9.23 / 45 \\
PDPOSGSC-G3L6 & 24/260 & 931.0 / 20 & 15.52 / 37 & 0.13 / 20 & -5.76 / 17 & 0.56 / 20 \\
PDPOSGSC-G6L7 & 6/52 & 542.3 / 16 & 253.66 / 142 & 89.00 / 79 & 48.88 / 63 & -1.24 / 24 \\
PDPOSGSC-G6L7 & 6/260 & 564.9 / 20 & 31.61 / 42 & 71.05 / 49 & 31.61 / 42 & 0.43 / 21 \\
PDPOSGSC-G6L7 & 24/52 & 993.4 / 43 & 264.80 / 217 & 264.77 / 215 & 264.80 / 217 & 11.08 / 47 \\
PDPOSGSC-G6L7 & 24/260 & 699.0 / 22 & 146.41 / 77 & 142.57 / 67 & 146.41 / 77 & 0.98 / 23 \\
PDPOSGSC-G7L11 & 6/52 & 505.7 / 25 & 175.62 / 83 & 15.72 / 34 & 86.69 / 55 & 14.85 / 34 \\
PDPOSGSC-G7L11 & 6/260 & 506.2 / 25 & 8.34 / 31 & -0.06 / 25 & 8.34 / 31 & 0.44 / 26 \\
PDPOSGSC-G7L11 & 24/52 & 1653.9 / 36 & 94.95 / 105 & 62.40 / 91 & -0.51 / 39 & 2.38 / 36 \\
PDPOSGSC-G7L11 & 24/260 & 1002.9 / 32 & 229.96 / 94 & 202.78 / 99 & 229.96 / 94 & 8.62 / 35 \\
\end{longtable}
\endgroup

The expanded-menu selection precedes its evaluation, as documented in \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/supervisor-20261023/e5/README.md}{the E5 archive}. The original panel's entire candidate/status inventory remains in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/round2/panel/summary.csv}{the original panel archive},
and the fitted expanded-menu predictions are not substitutes for unavailable
methods or independent dealer data.
```

### Original Supplement S13: Complete added-panel endpoint-plug-in comparison

Original source: `submission-v10/supplement.tex`; SHA-256 `9bc13b5cfc80e10bd5a3157481fe0d2825b4b238a32592d4dcc3a0846a6d66c8`.

```latex
\section{Complete added-panel endpoint-plug-in comparison}\label{sup:panel-levy}

The original added-panel endpoint plug-in was evaluated on the
same task grids as the historical and regression reports. Each entry gives
the saved loss percentage against the historical rule, followed by strict
hits for the endpoint plug-in and historical report. These are all related
aggregate tasks, not independent replications or source-pooled monetary losses.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{p{30mm}rrrr}
\caption{Every additional-panel endpoint-plug-in result. Fewer breaches do not guarantee a better score.}\\
\toprule
Series & \shortstack{Horizon 6\\history 52} & \shortstack{Horizon 6\\history 260} & \shortstack{Horizon 24\\history 52} & \shortstack{Horizon 24\\history 260} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Series & \shortstack{Horizon 6\\history 52} & \shortstack{Horizon 6\\history 260} & \shortstack{Horizon 24\\history 52} & \shortstack{Horizon 24\\history 260} \\
\midrule
\endhead
\bottomrule
\endfoot
PDPOSMBS-TOT & 7.17; 11/21 & 7.33; 5/26 & -17.87; 27/39 & -3.92; 22/25 \\
PDPOSCS-TOT & 18.28; 11/16 & 17.56; 2/6 & -5.06; 11/16 & 19.63; 4/6 \\
PDPOSFGS-TOT & -4.74; 13/16 & 16.77; 0/6 & -3.72; 37/36 & -4.06; 12/9 \\
PDPOSTIPS-L2 & -1.89; 12/26 & -7.42; 19/24 & -34.60; 30/48 & -4.52; 46/47 \\
PDPOSTIPS-G11 & 13.93; 3/23 & 27.71; 1/14 & -16.39; 16/61 & 27.11; 0/9 \\
PDPOSTIPS-G2 & 19.45; 4/16 & 23.00; 4/19 & 6.36; 27/31 & 2.09; 20/23 \\
PDPOSTIPS-G6L11 & 9.67; 5/9 & 36.27; 0/4 & 5.03; 4/10 & 12.63; 0/2 \\
PDPOSGSC-L2 & 20.65; 6/15 & -2.64; 6/15 & 0.93; 27/46 & -22.23; 24/33 \\
PDPOSGSC-G2L3 & 17.31; 15/24 & -14.81; 12/28 & 22.35; 49/47 & -9.35; 40/55 \\
PDPOSGSC-G3L6 & 20.57; 9/12 & 3.66; 8/20 & -11.37; 20/38 & -5.73; 17/20 \\
PDPOSGSC-G6L7 & 0.95; 12/16 & -10.15; 15/20 & 1.69; 49/43 & 5.19; 21/22 \\
PDPOSGSC-G7L11 & 4.92; 11/25 & 1.05; 12/25 & -20.33; 26/36 & 1.88; 26/32 \\
\end{longtable}
\endgroup

The complete original panel CSV also preserves every original
regression candidate, selection result, native-unit mean error amount and
failure status. This table adds no refit or parameter selection and does not
extend the independent-increment population guarantee to these financial
series.
```

### Original Supplement S14: Earlier-period fixed selection rules

Original source: `submission-v10/supplement.tex`; SHA-256 `9f45c380b80f342342385196b52653f97b19e99ddc7dc5e68ec228c909dae951`.

```latex
\section{Earlier-period fixed selection rules}\label{sup:selection}

The earlier-period experiment applies the saved fixed selection rules
to familiar historical data. These origins already have validation and
evaluation roles in the current archive, including actual rolling-fold
scoring. They cannot now be treated as untouched evidence for the expanded
backcast. The experiment remains retrospective, not external or prospective
validation. R0 denotes the fixed minimum-validation-loss rule. R2 is the predesignated main one-standard-error selection rule,
not a result-dependent replacement chosen for its subsequent performance.
The rule design precedes its calculations but follows earlier research results.

R1 adds the ordinary empirical quantile to the finite regression candidates.
R2 compares each candidate's validation losses with the same best-mean
candidate, using the paired-difference Bartlett-HAC standard error. Candidates
within that tolerance qualify, and the fixed rule prefers the strongest
shrinkage, including the empirical report. This paired HAC tolerance is a
time-series adaptation of a one-standard-error preference, not the textbook
formula, a significance test or a noninferiority guarantee. It does not account
for the whole uncertainty from selecting the best candidate on that segment.

R3 applies the same preference to prespecified earlier rolling folds and the
outer validation segment, with origin-equal weighting and maturity gaps.
Its HAC pairs use actual source-index distances rather than compressing gaps.
Without an eligible earlier fold, the saved design makes it identical to R2;
this is not a numerical fallback. Earlier-period results were sealed before
the already-inspected-period calculations that could reuse those origins.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{p{35mm}rrrrr}
\caption{Every earlier-period minimum-loss and one-standard-error comparison. The one-standard-error rule misses the recorded success conditions.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Minimum-loss\\rule (\%)} & \shortstack{One-standard-\\error rule (\%)} & \shortstack{Breaches\\minimum-loss /\\one-standard-error} & \shortstack{Historical\\breaches} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Series & \shortstack{Horizon /\\history} & \shortstack{Minimum-loss\\rule (\%)} & \shortstack{One-standard-\\error rule (\%)} & \shortstack{Breaches\\minimum-loss /\\one-standard-error} & \shortstack{Historical\\breaches} \\
\midrule
\endhead
\bottomrule
\endfoot
PDPOSGS-B & 6/52 & 11.22 & 7.43 & 10/10 & 7 \\
PDPOSGS-B & 24/52 & 181.39 & 181.39 & 27/27 & 8 \\
PDPOSMBS-TOT & 6/52 & -4.11 & 3.83 & 7/6 & 4 \\
PDPOSMBS-TOT & 24/52 & 48.55 & 26.55 & 14/13 & 10 \\
PDPOSCS-TOT & 6/52 & -11.56 & -11.56 & 0/0 & 0 \\
PDPOSCS-TOT & 24/52 & -4.12 & 1.02 & 4/4 & 2 \\
PDPOSFGS-TOT & 6/52 & -27.32 & -27.32 & 6/6 & 0 \\
PDPOSFGS-TOT & 24/52 & -3.87 & -3.60 & 4/3 & 2 \\
PDPOSTIPS-L2 & 6/52 & -7.06 & -7.06 & 2/2 & 1 \\
PDPOSTIPS-L2 & 24/52 & -23.33 & -1.55 & 4/1 & 1 \\
PDPOSTIPS-G11 & 6/52 & -5.55 & -5.79 & 5/5 & 4 \\
PDPOSTIPS-G11 & 24/52 & 5.67 & -0.87 & 15/15 & 15 \\
PDPOSTIPS-G2 & 6/52 & 15.16 & 15.16 & 8/8 & 0 \\
PDPOSTIPS-G2 & 24/52 & 30.27 & 30.27 & 14/14 & 10 \\
PDPOSTIPS-G6L11 & 6/52 & 283.88 & 28.58 & 17/6 & 0 \\
PDPOSTIPS-G6L11 & 24/52 & -4.03 & -2.70 & 2/1 & 0 \\
PDPOSGSC-L2 & 6/52 & 48.04 & 16.09 & 17/15 & 14 \\
PDPOSGSC-L2 & 24/52 & 40.77 & 40.77 & 34/34 & 30 \\
PDPOSGSC-G2L3 & 6/52 & 1.40 & 11.14 & 12/13 & 8 \\
PDPOSGSC-G2L3 & 24/52 & -11.22 & 15.48 & 15/20 & 15 \\
PDPOSGSC-G3L6 & 6/52 & 2.63 & 2.35 & 11/11 & 10 \\
PDPOSGSC-G3L6 & 24/52 & 15.62 & 6.92 & 29/28 & 26 \\
PDPOSGSC-G6L7 & 6/52 & 19.03 & 19.03 & 6/6 & 1 \\
PDPOSGSC-G6L7 & 24/52 & 2.05 & 1.82 & 20/19 & 19 \\
PDPOSGSC-G7L11 & 6/52 & 19.18 & 12.77 & 13/13 & 10 \\
PDPOSGSC-G7L11 & 24/52 & 8.48 & 2.70 & 29/29 & 27 \\
fx\_hourly & 6/720 & 2.44 & 0.62 & 79/73 & 63 \\
fx\_hourly & 6/2880 & -16.62 & -6.28 & 20/20 & 16 \\
fx\_hourly & 24/720 & -4.36 & -4.36 & 47/47 & 32 \\
fx\_hourly & 24/2880 & -1.42 & -1.40 & 1/1 & 0 \\
\end{longtable}
\endgroup

All three recorded success criteria are marked NOT\_MET.
R2's worst weekly excess is 181.39 percent,
and its weekly median is 5.37 percent.
The long-history FX gain also fails the prewritten retention criterion.
This adverse result remains a robustness finding rather than a contribution
claim. Complete inspected-period and all-rule rows remain linked in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/supervisor-20261023/r6/README.md}{the R6 archive}.
```

### Original Supplement S15: Selection failures and replication boundaries

Original source: `submission-v10/supplement.tex`; SHA-256 `c442e569b2dba5d992645c35af2f30f360c143e1fad10080a42fdab6fcaad271`.

```latex
\section{Selection failures and replication boundaries}\label{sup:selection-failures}

Required validation-candidate failure blocks the dependent rule;
it is neither retried nor replaced by a shorter mean. The complete inventory of non-complete reports is below. Every listed row has the saved reason
\texttt{REQUIRED\_VALIDATION\_CANDIDATE\_FAILED}. Those failures remain part of
the evidence even though other rules in the same task can complete.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lp{35mm}rrl}
\caption{All non-complete fixed-rule report rows. Failed mandatory candidates remain failures.}\\
\toprule
Phase & Series & \shortstack{Horizon /\\history} & Rule & Status \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Phase & Series & \shortstack{Horizon /\\history} & Rule & Status \\
\midrule
\endhead
\bottomrule
\endfoot
retro & fx\_hourly & 6/720 & R3 & FAILED \\
retro & fx\_hourly & 24/720 & R3 & FAILED \\
inspected & fx\_hourly & 6/720 & R3 & FAILED \\
inspected & fx\_hourly & 24/720 & R3 & FAILED \\
\end{longtable}
\endgroup

The Treasury earlier-period structural comparison uses a shorter
history than the original primary. It is explicitly an analogue, not an exact
earlier replication of the long-history primary. The source-reported comparison
and its definition are preserved in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/supervisor-20261023/r6/primary-replication.csv}{the primary-structure table}.
All original primary values remain unchanged. Reclassifying the analogue as an
exact primary replication, or calling familiar retrospective FX data an unseen
dealer, would change the scientific claim without adding evidence.
```

### Original Supplement S16: Finite delayed calibration and headroom SAV

Original source: `submission-v10/supplement.tex`; SHA-256 `631474a2de8809f9b7334067cea72da118c96daf35681bf89df371bc31774db2`.

```latex
\section{Finite delayed calibration and headroom SAV}\label{sup:wp2}

The finite delayed ACI-style wrapper adapts to past strict hits after their entire peak labels mature. Its score pool contains only completed residual
scores and uses the specified finite memory. The base-plus-score quantile is
projected onto the known floor. The adaptive alpha state is projected to the
current feasible range; the rank-zero convention issues the floor. Gamma was
selected by coverage distance, then pinball loss and the fixed tie rule, a
coverage-first selection criterion distinct from original regression fitting.
No canonical ACI theorem is imported to this modified procedure.

The headroom SAV method adapts a CAViaR recursion, rather than replicating a
return-VaR model. The completed headroom response is normalized by its
training-only scale; the recursive report is multiplied back by that same
scale and then floor-projected. Its fixed bounded optimizer and starts retain
all eligibility and convergence failures; a complete fit is not a proof of a
global optimum. Selection state carries across the unissued chronological gap.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrlrrl}
\caption{Complete delayed-wrapper and headroom-recursion inventory. Two long-horizon wrapper cells remain unavailable.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Method & Mean loss & Breaches & Status \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Method & Mean loss & Breaches & Status \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6/720 & ACI\_F & 472677.77 & 331 & COMPLETE \\
FX & 6/720 & ACI\_QR & 439672.91 & 352 & COMPLETE \\
FX & 6/720 & SAV & 449237.37 & 349 & COMPLETE \\
FX & 6/2880 & ACI\_F & 463271.47 & 328 & COMPLETE \\
FX & 6/2880 & ACI\_QR & 393795.06 & 329 & COMPLETE \\
FX & 6/2880 & SAV & 456696.22 & 364 & COMPLETE \\
FX & 24/720 & ACI\_F & 921402.08 & 322 & COMPLETE \\
FX & 24/720 & ACI\_QR & 1020220.09 & 393 & COMPLETE \\
FX & 24/720 & SAV & 781586.36 & 439 & COMPLETE \\
FX & 24/2880 & ACI\_F & 791441.18 & 323 & COMPLETE \\
FX & 24/2880 & ACI\_QR & 755982.70 & 294 & COMPLETE \\
FX & 24/2880 & SAV & 756811.00 & 333 & COMPLETE \\
Bills & 6/52 & ACI\_F & 3818.40 & 18 & COMPLETE \\
Bills & 6/52 & ACI\_QR & 3489.82 & 29 & COMPLETE \\
Bills & 6/52 & SAV & 2974.32 & 16 & COMPLETE \\
Bills & 6/260 & ACI\_F & 2792.91 & 7 & COMPLETE \\
Bills & 6/260 & ACI\_QR & 3013.16 & 6 & COMPLETE \\
Bills & 6/260 & SAV & 2892.23 & 29 & COMPLETE \\
Bills & 24/52 & ACI\_F & 4368.10 & 38 & COMPLETE \\
Bills & 24/52 & ACI\_QR & 6250.53 & 47 & COMPLETE \\
Bills & 24/52 & SAV & 4182.40 & 35 & COMPLETE \\
Bills & 24/260 & ACI\_F & NA & NA & NA \\
Bills & 24/260 & ACI\_QR & NA & NA & NA \\
Bills & 24/260 & SAV & 3100.97 & 25 & COMPLETE \\
\end{longtable}
\endgroup

The NA wrapper rows have the saved reason
\texttt{VALIDATION\_INELIGIBLE}; no test is substituted for the absent forecasts.
All losses are in each source's native units and must not be pooled.
```

### Original Supplement S17: Wrapper comparisons, uncertainty and missing cells

Original source: `submission-v10/supplement.tex`; SHA-256 `7936b43eb5a5f8d82d0d062508cbf093d776b3afc0abc468a11cb131f481e723`.

```latex
\section{Wrapper comparisons, uncertainty and missing cells}\label{sup:wp2-pairs}

Comparing wrapped regression with wrapped historical reports is a
different question from comparing either wrapper with its unwrapped base.
The following table retains every within-cell comparison. A lower coverage distance measures closeness of the empirical hit rate to the target probability, not conditional coverage or lower monetary loss.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrr}
\caption{Every paired wrapper comparison. Calibration adjustment preserves the long-history short-horizon FX score gain but does not produce universal dominance.}\\
\toprule
Source & \shortstack{Horizon /\\history} & \shortstack{Regression vs\\historical (\%)} & \shortstack{Breaches\\regression / historical} & \shortstack{Regression\\adjustment} & \shortstack{Historical\\adjustment} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Horizon /\\history} & \shortstack{Regression vs\\historical (\%)} & \shortstack{Breaches\\regression / historical} & \shortstack{Regression\\adjustment} & \shortstack{Historical\\adjustment} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6/720 & -6.98 & 352/331 & 0.00313 & 0.00004 \\
FX & 6/2880 & -15.00 & 329/328 & 0.00034 & 0.00049 \\
FX & 24/720 & 10.72 & 393/322 & 0.00932 & 0.00140 \\
FX & 24/2880 & -4.48 & 294/323 & 0.00562 & 0.00125 \\
Bills & 6/52 & -8.61 & 29/18 & 0.05469 & 0.01498 \\
Bills & 6/260 & 7.89 & 6/7 & 0.02834 & 0.02473 \\
Bills & 24/52 & 43.09 & 47/38 & 0.11968 & 0.08718 \\
Bills & 24/260 & NA & NA & NA & NA \\
\end{longtable}
\endgroup

The working-reference comparison inventory contains 56 fixed slots,
with 5 raw p values unavailable.
The reported Holm bookkeeping keeps those slots; mapping an NA component to a
bookkeeping value does not create an observed p value or validate failed
reference assumptions. HLN references remain separately identified.
Exact update equations, gamma candidates, selection freezes,
numerical receipts and all comparisons remain in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/protocol/revision-v6/REPLAY.md}{the v6 replay guide} and
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp2-summary.json}{the complete WP2 inventory}.
The original primaries are not overwritten by these post-result / exploratory
extensions. The upper-horizon NA rows and adverse SAV comparisons remain
visible rather than becoming a favorable subset.
```

### Original Supplement S18: Untuned forecast combinations

Original source: `submission-v10/supplement.tex`; SHA-256 `da3050e401dde73a44cdffd4b23df9bde315a647d7cce083a1f5ec5bfc5d48aa`.

```latex
\section{Untuned forecast combinations}\label{sup:wp3}

The median combination lowers Treasury-bill loss by 4.0\%, while the mean combination raises it by 2.8\%.

Fixed report combinations use the matched historical and original
regression reports at identical origins. Their arithmetic mean is untuned.
The median also requires the original selected plain local-quantile report;
neither a smaller predictor model nor the endpoint plug-in substitutes for
that missing constituent. Combining floor-respecting reports preserves the floor, but does not guarantee a conditional quantile or a score below that of the best constituent. Identical reports generate an NA equal-loss p value rather
than a manufactured significance result.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrr}
\caption{All original-cell combination comparisons. A report combination can outperform one constituent while losing to the other.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Rule & \shortstack{vs historical\\(\%)} & \shortstack{vs regression\\(\%)} & Breaches \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Horizon /\\history} & Rule & \shortstack{vs historical\\(\%)} & \shortstack{vs regression\\(\%)} & Breaches \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 6/720 & Mean & -6.91 & -4.90 & 338 \\
FX & 6/720 & Median & -4.81 & -2.75 & 325 \\
FX & 6/2880 & Mean & -10.61 & 4.87 & 330 \\
FX & 6/2880 & Median & -11.17 & 4.22 & 327 \\
FX & 24/720 & Mean & 5.50 & -19.77 & 533 \\
FX & 24/720 & Median & 5.00 & -20.15 & 514 \\
FX & 24/2880 & Mean & -8.94 & -5.39 & 345 \\
FX & 24/2880 & Median & -3.74 & 0.01 & 416 \\
Bills & 6/52 & Mean & -3.15 & -47.18 & 26 \\
Bills & 6/52 & Median & 0.00 & -45.46 & 11 \\
Bills & 6/260 & Mean & 2.77 & -31.84 & 40 \\
Bills & 6/260 & Median & -3.98 & -36.32 & 28 \\
Bills & 24/52 & Mean & 18.87 & -63.69 & 54 \\
Bills & 24/52 & Median & 0.00 & -69.46 & 33 \\
Bills & 24/260 & Mean & -5.32 & -54.88 & 28 \\
Bills & 24/260 & Median & -11.51 & -57.83 & 14 \\
\end{longtable}
\endgroup

\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrrrrr}
\caption{Complete combination counts including the added panel. Missing median constituents remain NA.}\\
\toprule
Rule & Total & Complete & Unavailable & \shortstack{Lower loss\\than both} & \shortstack{Lower loss\\than historical} & \shortstack{Lower loss\\than regression} & \shortstack{Equal loss\\to historical} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Rule & Total & Complete & Unavailable & \shortstack{Lower loss\\than both} & \shortstack{Lower loss\\than historical} & \shortstack{Lower loss\\than regression} & \shortstack{Equal loss\\to historical} \\
\midrule
\endhead
\bottomrule
\endfoot
Mean & 56 & 56 & 0 & 14 & 16 & 54 & 0 \\
Median & 56 & 8 & 48 & 3 & 5 & 6 & 2 \\
\end{longtable}
\endgroup

The added panel lacks the specified plain local-quantile
constituent, so all its median rows remain unavailable. Mean combinations are
complete, but lower loss than regression alone does not imply lower loss than
the historical rule. All panel-specific values and every comparison remain in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp3-combinations.json}{the complete combination record}.
```

### Original Supplement S19: Combination Murphy diagrams and comparison families

Original source: `submission-v10/supplement.tex`; SHA-256 `6dd9b8238a8b10c5839878ec1b2e240ec19583e4d5a6168416718e3800e39de1`.

```latex
\section{Combination Murphy diagrams and comparison families}\label{sup:wp3-murphy}

Elementary-score comparisons vary the score threshold while
keeping the quantile level fixed. Exact integer-event signs at every unique
breakpoint determine sample crossing before display interpolation. A picture
is not used to select favorable thresholds. These matched combination
contexts are distinct from the original FX primary with its shorter rolling
reference.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lp{34mm}p{18mm}lrr}
\caption{Every combination Murphy comparison in the original-primary contexts. Crossing prevents threshold-uniform sample dominance.}\\
\toprule
Source & \shortstack{Left-hand\\method} & \shortstack{Right-hand\\method} & Ranking & \shortstack{Positive\\breakpoints} & \shortstack{Negative\\breakpoints} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Left-hand\\method} & \shortstack{Right-hand\\method} & Ranking & \shortstack{Positive\\breakpoints} & \shortstack{Negative\\breakpoints} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & MEAN\_F\_QR & F & CROSSING & 217 & 15628 \\
FX & MEAN\_F\_QR & QR & CROSSING & 13562 & 2343 \\
FX & MEDIAN\_F\_QR\_KNN & F & CROSSING & 909 & 13572 \\
FX & MEDIAN\_F\_QR\_KNN & QR & CROSSING & 10827 & 2575 \\
Bills & MEAN\_F\_QR & F & CROSSING & 336 & 291 \\
Bills & MEAN\_F\_QR & QR & CROSSING & 179 & 454 \\
Bills & MEDIAN\_F\_QR\_KNN & F & CROSSING & 262 & 274 \\
Bills & MEDIAN\_F\_QR\_KNN & QR & CROSSING & 147 & 446 \\
\end{longtable}
\endgroup

The complete normal-DM comparison family has 224 slots,
of which 98 have NA raw p values.
The family adjustment is bookkeeping for those saved working references, not
error control over the complete historical analysis search. The inspected
record, overlapping labels, repeated fitting and related aggregate series
remain common to the methods. All original and adverse rows remain in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp3-findings.json}{the combination findings}.
Exact breakpoint signs support only the stated finite-sample score comparison;
they do not certify general forecast dominance, optimal funding, or a causal
benefit from acting on the limits.
```

### Original Supplement S20: Training-defined position-change states

Original source: `submission-v10/supplement.tex`; SHA-256 `b9047c67370b713b2de73495e7bc0dfa343781d39e45384074de6754cd6bfb66`.

```latex
\section{Training-defined position-change states}\label{sup:wp4}

The states are low, middle and high issue-known RMS position-change
states, not price volatility or yield regimes. Cutpoints come only from the
training history. Reports and original primary means stay unchanged; the
diagnostic divides the already viewed evaluation record without estimating a
switching policy. Source-native group differences are not pooled.
\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrrrr}
\caption{All three state groups for each original primary. The FX regression-minus-reference loss difference remains negative in every group, while the weekly evidence remains adverse.}\\
\toprule
Source & State & Issues & \shortstack{Regression minus\\reference loss} & \shortstack{Dependence-adjusted\\standard error} \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & State & Issues & \shortstack{Regression minus\\reference loss} & \shortstack{Dependence-adjusted\\standard error} \\
\midrule
\endhead
\bottomrule
\endfoot
FX & low & 1593 & -58761.27 & 16492.94 \\
FX & middle & 1816 & -27839.43 & 16257.70 \\
FX & high & 3216 & -70387.91 & 17895.89 \\
Bills & low & 9 & 6696.66 & 1705.21 \\
Bills & middle & 25 & 5230.59 & 2608.15 \\
Bills & high & 243 & 810.88 & 466.48 \\
\end{longtable}
\endgroup

\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lp{35mm}rrl}
\caption{Complete state diagnostic reference family. A joint rejection need not identify a useful state rule.}\\
\toprule
Source & Diagnostic & \shortstack{Unadjusted\\p-value} & \shortstack{Holm-adjusted\\p-value} & Status \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & Diagnostic & \shortstack{Unadjusted\\p-value} & \shortstack{Holm-adjusted\\p-value} & Status \\
\midrule
\endhead
\bottomrule
\endfoot
FX & joint\_GW & 1.46298e-06 & 5.8519e-06 & OK \\
FX & group\_heterogeneity & 0.159383 & 0.159383 & OK \\
Bills & joint\_GW & 0.0484878 & 0.0969756 & OK \\
Bills & group\_heterogeneity & 0.000426772 & 0.00128032 & OK \\
\end{longtable}
\endgroup

These finite-instrument and group-mean HAC references require
unverified moment, dependence and covariance assumptions. A joint conditional-moment rejection can be driven by an unconditional mean difference; it is not
evidence that a state-dependent trading or limit-selection policy works.
The source-level reconstruction and all cutpoints remain in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp4-states.json}{the complete state record}.
```

### Original Supplement S21: Refitted target-level sensitivities

Original source: `submission-v10/supplement.tex`; SHA-256 `fca0690651712e8060421910f61a1028ce85fb0493a734a5a15a45dec17239a7`.

```latex
\section{Refitted target-level sensitivities}\label{sup:wp5}

Changing the target quantile requires fitting the specified target-level procedure; it is different from reweighting the errors of a fixed report.
The following saved sensitivities keep the original horizon and reference
structure. The weekly primary and matched reference coincide and count once.
All unavailable upper-target rows remain NA with
\texttt{VALIDATION\_INELIGIBLE}, rather than being replaced by a lower target
or a favorable subset. Absolute loss values across different quantile levels
measure different objectives.
\begingroup
\footnotesize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.12}
\begin{longtable}{lrp{20mm}rrrl}
\caption{Complete target-level sensitivity. The lower-target directions recur, but upper-target evidence remains unavailable.}\\
\toprule
Source & \shortstack{Target\\\(\tau\)} & Reference & \shortstack{Mean loss\\difference} & \shortstack{Regression\\breaches} & \shortstack{Reference\\breaches} & Status \\
\midrule
\endfirsthead
\caption[]{Continued.}\\
\toprule
Source & \shortstack{Target\\\(\tau\)} & Reference & \shortstack{Mean loss\\difference} & \shortstack{Regression\\breaches} & \shortstack{Reference\\breaches} & Status \\
\midrule
\endhead
\bottomrule
\endfoot
FX & 0.90 & primary & -60715.44 & 686 & 620 & OK \\
FX & 0.90 & matched & -67628.17 & 686 & 667 & OK \\
Bills & 0.90 & primary & 1175.03 & 73 & 55 & OK \\
FX & 0.99 & primary & NA & NA & NA & NA \\
FX & 0.99 & matched & NA & NA & NA & NA \\
Bills & 0.99 & primary & NA & NA & NA & NA \\
\end{longtable}
\endgroup

The complete family contains 6 slots,
with 3 raw p values unavailable.
The fixed target-specific selections precede their evaluation; full settings
and results remain in \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v7-final/results/revision-20261023/v6/wp5-tau-summary.json}{the target-level inventory}.
The saved lower-target directions do not establish robustness to an arbitrary
tail level, actual shortage costs, or a new economic decision rule. Failed
eligibility is a result of the specified procedure and remains part of the
paper's boundary.
```

### Original Supplement S27: Earlier calibrated simulation and numerical failures

Original source: `submission-v10/supplement.tex`; SHA-256 `d9c215f90ffc5b953be4aab5eea0023fb4e0e80bde9fa530fb1308d1c5164ea8`.

```latex
\section{Earlier calibrated simulation and numerical failures}\label{sup:v9-legacy-mc}

This distinct calibrated design uses constant-variance AR(1) levels, where the
peak depends on the current position (D0), an hourly AR--GARCH--t law with a
known hour shape (D1), and a weekly AR--GARCH--t law (D2).
D0/D2 share the original pre-validation Treasury calibration; D1 uses the
original pre-validation FX prefix. Levels are divided by the prefix standard
deviation without demeaning. The frozen calibration, clocks, origin geometry,
parameters and numerical rules are retained in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v10/results/v9/legacy-calibrated}{the imported calibrated archive}.
The weekly clock, validation span, refit schedule and six-candidate menu,
including the intercept-only limit, differ from Section~\ref{sup:v8-mc}.
Their short-history outcomes cannot be treated as replications of one design.

Each completed cell reports repetition medians and quartiles of the
within-repetition relative loss against F. These differ from the ratio of
across-repetition mean losses in Section~\ref{sup:v8-mc}.
Quartiles describe dispersion under fixed fitted laws, not confidence limits.
The known-state oracle is a finite future-path approximation; its realized
score need not beat F in every repetition. Ordinary-rank I, oracle results,
strict breaches and intercept-only selections remain separate diagnostics.

\input{generated/v9-legacy-simulation-table.tex}

A required numerical failure blocks the whole cell. Partial repetitions do
not supply a replacement median, quartile, win rate or breach rate.
The retained nonconvergence exceptions mean that the unchanged solver did not
obtain its joint residual-and-gap acceptance certificate within its iteration
budget. They establish neither nonexistence of an optimum nor poor predictive
accuracy of an unavailable report. Final residuals and gaps were not retained;
the four-feature exceptions also lack exact refit context. These quantities
remain unknown. The original constant-variance and short-weekly predictions
are unsupported; the hourly and history-order predictions are unassessable.
These outcomes identify neither the financial loss mechanism nor a pure
frequency effect.
```

### Original Supplement S28: Pre-evaluation stability screen and switching stress simulation

Original source: `submission-v10/supplement.tex`; SHA-256 `d8072daded429844d4775ac5cb4165667bb860551549b3a108c1b4971bec7ac8`.

```latex
\section{Pre-evaluation stability screen and switching stress simulation}\label{sup:v9-stability}

The separately frozen
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v9/protocol/v9/nonstationarity-design.md}{stability-study protocol}
uses only pre-evaluation prefixes. Its joint OLS score includes intercept,
AR slope and centered residual-square channels (Hansen, 1992).
Each qualified whole-prefix AR--GARCH--t fit generates a plug-in parametric
bootstrap reference. OLS and the score statistic are re-estimated on each
bootstrap path; the generator is fitted once. Published iid critical values
are not used. With the registered \(B=999\) bootstrap paths, the p value is
\((1+\#\{H_b\ge H_{\rm obs}\})/(B+1)\); the registered draw count and
all exceedances remain in the archive. The table retains the observed statistic,
bootstrap p value, Holm adjustment, moment qualification and descriptive cuts.
Qualified fitted nulls require \(\nu>4\) and
\(q_4=\alpha^2\{3(\nu-2)/(\nu-4)\}+2\alpha\beta+\beta^2<1-10^{-8}\).
A successful fit and this fourth-moment gate do not prove that the real law
has those moments. The plug-in calibration supplies no exact finite-sample
size guarantee; rejection can also reflect misspecification or outliers.

\input{generated/v9-stability-diagnostics-table.tex}

Candidate cuts minimize a separate-variance Gaussian AR quasi-likelihood
criterion with penalty \((3+4k)\log M\), where \(M\) counts transitions.
The fixed search allows at most two cuts and requires each segment to contain
at least \(\max\{104,\lceil .20M\rceil\}\) transitions.
These are descriptive calibration partitions, not individually significant
breaks. Whole-prefix scaling is shared by every segment without demeaning;
the first target in a segment keeps its preceding observed lag.
The constrained AR and GARCH fits have one declared start and no retry.
The daily nonregular null and hourly optimization failure retain unavailable
primary p values; neither is evidence of stability.

The constant control retains the whole-prefix parameters. The stress arm
cycles the fitted regimes with their original transition dwell lengths and a
fixed repetition-phase grid. Level, innovation and variance state continue
through each switch. The last-to-first wrap is artificial, rather than an
observed historical break. Common uniforms are transformed through each arm's
own standardized t law; a no-cut source reuses the identical whole-fit path.
Both arms retain the forecasting procedures of Section~\ref{sup:v8-mc}.
The following complete grids retain failed conditional cells and all F cells.

\input{generated/v9-stability-W52-table.tex}
\input{generated/v9-stability-W260-table.tex}
\input{generated/v9-stability-F-table.tex}

Loss summaries are medians across repetitions within each source, then equal-weight medians across every required source. They are not the controlled
grid's ratio-of-means estimand. A required repetition failure makes its whole
cell unavailable; successful subsets do not replace missing full-grid results.
The raw weekly screening threshold is met, while multiplicity adjustment
retains fewer rejections. The near-parity constant-control prediction is
unsupported. The two-history switching prediction and the daily/hourly
comparison are unassessable. Constant controls themselves generate large
losses, so instability is not necessary for losses in these procedures.
The empirical low-frequency mechanism remains unidentified.
```

### Original Supplement S33: Retained accuracy and hit diagnostics

Original source: `submission-v10/supplement.tex`; SHA-256 `c014d6ae300213cbaa273503361e6b5033fcf17d3a704e802ebf54db813f8cd2`.

```latex
\section{Retained accuracy and hit diagnostics}\label{sup:v10-diagnostics}
These are the unchanged earlier tests and Murphy plots moved from the main article. The p-values retain their original named adjustment families; no MCS adjustment is retroactively assigned to them.
\input{generated/v10-moved-diagnostics.tex}
```


---

# Earlier extended-results index, retained verbatim

# Current v9 evidence and exact technical overflow

The new substantive review is documented in the [issue register](notes/revision-v9/substantive-20261025-findings.md), [analytic evidence](notes/revision-v9/substantive-20261025-analytic-note.md) and [primary-source reading log](notes/revision-v9/substantive-20261025-primary-reading.md). The diagnostic addendum now explicitly qualifies horizon sorting, the lower-inverse quantile convention, the per-method rescaling limit, pooled discovery roots and weekly information availability. These changes preserve the original experimental values and negative outcomes. They do not certify ten effective research hours or independent financial reproduction.


The [unified history figure](results/revision-v9/wp4/render-v5/unified-history.pdf), [complete simulation summaries](results/revision-v9/wp2/summary.csv), [all prediction-screen outcomes](results/revision-v9/wp2/support.json) and [all fixed-grid FX contrasts](results/revision-v9/wp3/README.md) accompany the partly supported history-length interpretation. The universal simplification prediction fails, an FX first cutpoint is left-censored, and both longer-horizon curves reverse at the largest history. The known FX period is reused; these are not independent unseen-dealer replications.

The [complete saved simulation records](results/revision-v9/wp2/wp2-driver-output.tar.gz) and [member index](results/revision-v9/wp2/wp2-driver-output-members.csv) retain candidate and repetition evidence. The [complete financial contrast fields](results/revision-v9/wp3/contrasts.csv) include the saved HAC bandwidth, mean difference, long-run variance, statistic and nominal probability. The [diagnostic addendum](submission-jof/diagnostic-addendum.pdf) exposes every exception to the two primary simulation screens and all saved paired-loss fields without refitting or changing a result. It explicitly corrects the compact Supplement's description of its summary columns as complete diagnostics; the protected Supplement and original linked technical material retain their accepted bytes.

To keep the compact Supplement within its page budget, the complete unchanged full/sparse preference-frontier sections and full numerical conventions are copied verbatim into [extended-v9-technical.tex](submission-jof/extended-v9-technical.tex), with a [separate readable PDF](submission-jof/extended-v9-technical.pdf). Every frontier region, tie, adverse outcome and implementation qualification remains accessible. The exact relocation proof is [wp5-supplement-relocation.json](notes/revision-v9/wp5-supplement-relocation.json).

The earlier index below is preserved as historical guidance.

---

# Complete result archive: current v8 index

The current manuscript and Supplement add the [full controlled grid and failure archive](results/revision-v8/wp3/README.md), [all same-dealer daily comparisons](results/revision-v8/wp4/README.md) and [complete fixed-prefix/backcast tables](results/revision-v8/wp5/README.md). Their frozen designs, run receipts, exact source bindings and acceptance records are in `protocol/revision-v8/` and `notes/revision-v8/`. These post-result / exploratory additions retain a failed mechanism criterion, a daily conditional exception and longer-horizon gains; none supplies independent dealer validation. The expanded prefix contains the earlier backcast and previously scored target paths.

The following index is retained as the earlier v7 archive guide. Its claims of “no new experiment” and “current” presentation refer to that historical revision. Every linked earlier favorable, adverse, failed or unavailable result remains intact.

---

# Extended results and complete historical records

The compact v7 manuscript and Online Supplement select presentation material; every earlier outcome remains available below. These are related retrospective comparisons, with their original source definitions, denominators, failed fits and adverse results. This index does not add an experiment or validate a new sample.

## Complete earlier documents

- [Complete v6 Online Supplement (94 pages)](manuscript/revision-v6-preserved/supplement-preview.pdf), [source](manuscript/revision-v6-preserved/supplement.tex), [structured content](manuscript/revision-v6-preserved/supplement-content.json), and [exact preservation manifest](manuscript/revision-v6-preserved/PRESERVATION.json). All original v6 submission files are preserved from the recorded source commit.
- [Complete supervisor manuscript](manuscript/supervisor-revision/main.pdf) and [source/guide](manuscript/supervisor-revision/README.md), including its own unsuccessful selection research.
- [v3 source guide](manuscript/revision-v3/README.md) and [earlier working paper](manuscript/working-paper/README.md). Their version labels refer to those dated milestones.

## Full numerical inventories

| Topic | Complete original source | Scope to preserve |
|---|---|---|
| Original conditional comparisons | [Immutable original archive guide](results/revision-20261022/README.md) | Complete candidates, failed cells, original primaries, all paired contrasts and sparse/annual sensitivities |
| Endpoint/ordinary rank | [Rank ablation](results/revision-20261022/rank-ablation/README.md) | Corrected rank versus ordinary empirical minimizer endpoint; no replacement of original reports |
| Autoregressive replay | [Replay](results/revision-20261022/ar1-replay/README.md), [diagnostics](results/revision-20261022/ar1-diagnostics/README.md) | Every adverse comparison and dependence qualification |
| Coverage e-values | [Original output](results/revision-20261022/coverage-evalues/README.md) | Late diagnostics, original numerical conventions and limits |
| Full error-weight frontier | [Preference archive](results/revision-20261022/preference-robustness/README.md) | Complete envelopes, boundary ties and distinct H24 legacy reversal |
| Compact-model sensitivity | [All four-predictor rows](results/revision-20261023/parsimonious/summary.csv) | Feature and penalty-menu changes are joint |
| Lévy empirical benchmark | [All benchmark rows](results/revision-20261023/round2/levy/summary.csv) | Every adverse score and breach change, separate from theorem |
| Lévy simulations | [Original cases](results/revision-20261023/round2/levy/simulation.json), [corrected cases](results/revision-20261023/round2/levy-ar-correction/README.md) | Positive/negative increment cases, mean-reverting levels, threshold and initialization distinctions |
| Original additional panel | [Complete procedure rows](results/revision-20261023/round2/panel/summary.csv) | Related aggregate categories, every original result and skip |
| Expanded regression panel | [Full E5 results](results/supervisor-20261023/e5/summary.csv), [fixed predictions](results/supervisor-20261023/e5/prediction-assessment.json) | Expanded menu narrows losses but leaves failures and unmet criteria |
| Common-menu and feature contrasts | [E3 results](results/supervisor-20261023/e3/README.md), [E6 table](results/supervisor-20261023/e6/table6.csv) | No causal isolation of a feature effect |
| Additional mature benchmarks | [All results](results/revision-20261023/round2/baselines/summary.csv) | Filtered paths, peak-tail and quantile forest: failures remain failures |
| Earlier-period selection | [R6 guide](results/supervisor-20261023/r6/README.md), [complete summary](results/supervisor-20261023/r6/summary.csv), [primary structures](results/supervisor-20261023/r6/primary-replication.csv) | One-SE failures; short-history Treasury analogue is not exact original-primary replay |
| Two fixed early FX comparisons | [HAC readback](results/supervisor-20261023/r6-writing-hac-20261023/README.md) | Descriptive unadjusted later readback, not new fitting or confirmation |
| All wrappers and headroom SAV | [WP2 summaries](results/revision-20261023/v6/wp2-summary.json), [comparisons](results/revision-20261023/v6/wp2-comparisons.json) | Original source cells only, finite delayed adaptation and all NA |
| All forecast combinations | [WP3 results](results/revision-20261023/v6/wp3-combinations.json) | Broader context inventory; missing constituent stays unavailable |
| State and conditional diagnostics | [WP4](results/revision-20261023/v6/wp4-states.json) | Position-increment RMS groups, not price volatility; no causal switching rule |
| Target levels and failed validation | [WP5](results/revision-20261023/v6/wp5-tau-summary.json) | Lower-target direction and upper-target NA both remain |
| Test-family versions and hit likelihoods | [Original corrected inference](results/supervisor-20261023/inference/audit-receipt.json), [later reporting family](results/supervisor-20261023/w3/summary.json) | Original Holm family and later separation remain distinct; conditional likelihood conditions on initial hit |

## Reproduction boundaries

The public aggregate files permit result readback without private FX observations or private forecast vectors. Exact financial replay requires the original compatible inputs and the version-specific protocol/code, which this v7 presentation revision does not re-run. The [current evidence table](notes/v7/evidence-table.md) binds presentation values to saved fields. Original frozen result files and historical declarations are not rewritten. Prospective evaluation remains a future author decision, with a new unviewed sample and a separately fixed information clock.


# Exact tables relocated from the v12 main article

## literature-matrix

SHA-256 `546a76b5515f0e4af9d7417d9c07d48f2305a18cec1ed7ad7353a1ac82da46e3`. The original source is retained without changing its numerical rows.

```latex
\begin{table}[htbp]\centering\footnotesize
\caption{Related studies: reported targets, data units and evaluation approaches.}\label{tab:literature}
\begin{tabular}{>{\raggedright\arraybackslash}p{2.3cm}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{3.9cm}>{\raggedright\arraybackslash}p{4.2cm}}\toprule
Study & Response & Data unit & Evaluation\\\midrule
\shortstack[l]{Wisniewski\\et al. (2020)} & Next-hour signed-position interval & One market maker's hourly FX positions & Pinball and interval scores; coverage tests\\
\shortstack[l]{Boudoukh\\et al. (2004)} & Worst cumulative portfolio-return quantile & Fixed portfolio under a lognormal diffusion & MaxVaR/VaR ratios; discrete-monitoring simulation\\
\shortstack[l]{van den\\Hoogen (2017)} & Conditional quantile of cumulative payment-deficit peak & ABN AMRO transaction accounts & Coverage and independence backtests\\
\shortstack[l]{Duffie\\et al. (2023)} & Capacity, Treasury illiquidity and PnL tail quantiles & Dealer positions, transactions and PnL & Illiquidity regressions; out-of-sample PnL pseudo-$R^2$\\
\shortstack[l]{Engle and\\Manganelli\\(2004)} & Conditional return quantile & GM, IBM and S\&P 500 daily returns & Quantile objective, exception rates and DQ tests\\
\shortstack[l]{Ehm et al.\\(2016)} & Quantile and expectile forecast comparison & Economic and wind-speed forecasts & Elementary-score curves and score differences\\
\shortstack[l]{Meinshausen\\(2006)} & Conditional response quantile & Regression datasets & Cross-validated quantile loss\\
This study & Sampled absolute-position peak & FX positions; weekly position aggregates & Pinball loss, breaches, model confidence sets and costs\\
\bottomrule\end{tabular}
\end{table}
```

## tail-sensitivity-table

SHA-256 `a892a8900e88212238264a5c9ac185c02d6491ae4637d1dbe3ef4f310dd6f4ea`. The original source is retained without changing its numerical rows.

```latex
\begin{table}[htbp]\centering\small
\caption{Full-regression relative excess loss (\%) at alternative quantile levels. Positive values favor matched historical headroom; NA retains any failed required comparison.}\label{tab:v12-tau}
\begin{tabular}{lrr}\toprule
Source / training history & 90\% & 99\% \\\midrule
CFTC, 52 weeks & +3.45 & +15.05 \\
CFTC, 260 weeks & +1.58 & \textsc{NA} \\
FX, original period & -10.15 & \textsc{NA} \\
FX, earlier period & -17.85 & \textsc{NA} \\
Treasury bills & +0.67 & +44.22 \\
\bottomrule\end{tabular}
\par\vspace{2pt}\begin{minipage}{.95\linewidth}\footnotesize
Contract rows report full-group medians. FX uses 2,880-hour training histories; Treasury uses 260 weeks. Successful subsets never replace a required full group.
\end{minipage}\end{table}
```

## individual-CFTC-table

SHA-256 `1cf73d627c41657cb9e59551ff03d3e399f7acd66c5884ac00f7fe40fd2f0373`. The original source is retained without changing its numerical rows.

```latex
\begin{table}[t]\centering\scriptsize
\setlength{\tabcolsep}{2pt}
\caption{CFTC dealer-category futures: relative loss versus matched historical headroom (\%). All 17 selected literal contract codes are retained.}
\label{tab:v10-cftc-contracts}
\resizebox{\linewidth}{!}{%
\begin{tabular}{l*{10}{r@{.}l}}\toprule
Contract & \multicolumn{10}{c}{History 52} & \multicolumn{10}{c}{History 260} \\
\cmidrule(lr){2-11}\cmidrule(lr){12-21}
code & \multicolumn{2}{c}{\shortstack{Intercept\\only}} & \multicolumn{2}{c}{\shortstack{Four-\\feature}} & \multicolumn{2}{c}{\shortstack{Full\\regression}} & \multicolumn{2}{c}{\shortstack{Calibrated\\history}} & \multicolumn{2}{c}{\shortstack{Calibrated\\regression}} & \multicolumn{2}{c}{\shortstack{Intercept\\only}} & \multicolumn{2}{c}{\shortstack{Four-\\feature}} & \multicolumn{2}{c}{\shortstack{Full\\regression}} & \multicolumn{2}{c}{\shortstack{Calibrated\\history}} & \multicolumn{2}{c}{\shortstack{Calibrated\\regression}} \\ \midrule
044601 & 5 & 26 & 128 & 00 & 41 & 38 & 15 & 01 & 18 & 80 & 0 & 51 & 7 & 82 & 43 & 88 & 13 & 87 & 42 & 41 \\
043602 & 3 & 37 & 9 & 35 & 3 & 37 & 37 & 79 & 24 & 64 & 2 & 30 & 8 & 95 & 20 & 97 & -11 & 22 & -12 & 64 \\
042601 & 4 & 64 & 9 & 48 & 35 & 65 & 26 & 69 & 41 & 21 & -0 & 15 & 74 & 23 & 16 & 63 & 1 & 46 & 9 & 39 \\
045601 & -2 & 04 & 0 & 31 & -2 & 04 & 21 & 83 & 6 & 14 & 1 & 85 & 1 & 85 & 1 & 85 & 2 & 40 & 2 & 58 \\
020601 & 4 & 77 & 79 & 72 & 111 & 12 & 25 & 66 & -5 & 34 & 0 & 92 & 43 & 38 & 29 & 70 & -15 & 12 & -12 & 32 \\
099741 & 0 & 69 & 13 & 97 & 14 & 56 & 77 & 33 & -13 & 28 & 0 & 22 & 0 & 22 & 0 & 22 & 27 & 72 & 27 & 73 \\
1170E1 & 6 & 42 & 6 & 82 & 46 & 30 & -0 & 22 & 12 & 77 & 0 & 92 & -28 & 44 & -16 & 22 & -1 & 12 & 1 & 00 \\
097741 & -0 & 83 & 23 & 76 & 68 & 71 & 29 & 77 & 33 & 79 & 0 & 53 & -6 & 54 & 14 & 69 & -0 & 41 & -5 & 43 \\
096742 & 2 & 93 & 3 & 41 & 6 & 13 & 49 & 54 & 30 & 46 & 5 & 30 & 4 & 82 & 62 & 68 & 37 & 12 & -0 & 49 \\
095741 & 7 & 39 & 19 & 55 & 19 & 33 & 41 & 27 & 42 & 98 & -0 & 70 & 2 & 13 & 10 & 35 & 19 & 30 & 55 & 39 \\
090741 & 4 & 03 & 10 & 28 & 4 & 03 & 15 & 58 & 13 & 13 & 3 & 28 & -5 & 35 & -3 & 60 & -2 & 02 & -5 & 66 \\
232741 & 0 & 11 & 123 & 33 & 37 & 53 & 63 & 84 & 36 & 35 & 1 & 94 & -3 & 35 & 7 & 68 & -0 & 65 & -3 & 86 \\
33874A & 6 & 95 & 88 & 57 & 38 & 30 & 30 & 15 & 44 & 07 & -2 & 38 & -3 & 21 & -4 & 78 & 6 & 98 & 9 & 52 \\
240743 & -3 & 04 & -7 & 32 & 183 & 12 & 33 & 14 & 49 & 77 & -2 & 28 & -2 & 28 & -2 & 28 & 32 & 91 & 26 & 37 \\
092741 & 0 & 54 & 0 & 54 & 0 & 54 & -1 & 74 & -0 & 68 & 0 & 17 & -6 & 98 & 26 & 22 & 5 & 58 & 13 & 94 \\
098662 & -0 & 44 & -0 & 44 & 0 & 90 & 44 & 89 & 38 & 90 & 2 & 45 & -39 & 44 & 2 & 45 & 15 & 12 & 20 & 45 \\
112741 & 11 & 06 & 38 & 76 & 10 & 05 & 33 & 72 & 24 & 10 & 2 & 24 & 2 & 82 & 80 & 98 & 8 & 36 & 16 & 37 \\
\bottomrule\end{tabular}}
\par\vspace{2pt}\begin{minipage}{.98\linewidth}\footnotesize
Entries are percentage loss differences from matched corrected historical headroom; positive values mean higher loss, and unavailable entries retain failed or incomplete comparisons.
The pre-specified conditions require historical superiority in at least 60\% of all 34 comparisons, full-regression medians within ten percent at both histories, and a strictly smaller four-feature median with longer history.
Full-precision results determine the comparisons, with all scores, breaches, selections and failures retained in Supplement Section S30.
\end{minipage}\end{table}

```

