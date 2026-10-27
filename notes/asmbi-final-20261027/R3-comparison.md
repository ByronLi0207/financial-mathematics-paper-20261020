# R3 局限与结论前后对照

## 改前

```tex
\section{Limitations}\label{sec:limitations}

\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
\item FX comes from one market maker, and its original evaluation period was inspected before conditional methods were specified.
\item The earlier-period comparison and full-prefix backcast are retrospective, with no previously unseen prospective financial evaluation.
\item Weekly reports aggregate positions across dealers; related categories and the CFTC survivor universe do not provide independent dealer replications. Net-position peaks summarize exposure; gross portfolios, hedging arrangements and economic capital requirements remain unidentified.
\item Downloaded economic-date vintages omit historical first-release information, reporting delays and unrecorded within-interval excursions.
\item The comparisons identify neither causal effects nor individual-feature effects, and fitted limits receive no coverage guarantee under this dependence.
\item Costs illustrate fixed preferences; trading returns, funding gains and institutional intervention costs are not measured.
\item The finite-penalty hindsight bound is diagnostic only; validation-length and quantile-sensitivity checks are post-result analyses with numerical failures retained.
\item Only 6 of 10 high-quantile compatibility fits pass, so the rejected repair leaves both FX comparisons unavailable.
\end{itemize}
Supplement Section S36 retains the original technical qualifications on simulations, aggregation and forecast comparison. A consolidated register in Supplement Section S40 retains supported, unsupported and untestable prewritten screens.

\FloatBarrier

\section{Conclusion}\label{sec:conclusion}

Historical rules are hard to beat. For RQ1, matched FX regression gains recur across periods, but a shorter rolling reference changes the ranking (Table~\ref{tab:fx}). The learning curve also gives back part of its gain at the longest history, linking conditional performance to available history rather than universal model advantage (Figure~\ref{fig:v11-history}).

For RQ2, longer validation reduces full regression medians in both weekly reporting systems, but across-arm differences need not describe typical paired improvements (Table~\ref{tab:v13-validation}). These dealer aggregates remain related tasks, and the horizon-six New York Fed extension also moves the validation endpoint. The benchmark-default protocol cuts weekly median excess to 0.00\% and preserves FX gains, yet 8 of 60 cases still lose by over ten percent, with a worst excess of 80.98\% (Section~\ref{sec:v13-rp}). This failed tail criterion limits the protocol's risk-management recommendation, and the rejected high-quantile repair leaves its original judgments unresolved.

For RQ3, higher reserve charges and lower fixed breach charges generally favor expanded regression in CFTC, with local exceptions (Figure~\ref{fig:v10-cost}). Lower pinball scores can therefore coexist with more breaches and different cost rankings, requiring joint reporting of reserve amounts, breach counts and exceedance amounts. The costs are stipulated preferences rather than observed institutional costs, and the financial evidence remains retrospective.

\FloatBarrier


```

## 改后

```tex
\section{Limitations}\label{sec:limitations}

The FX evidence comes from one market maker, while the weekly reports combine positions across dealers. Related categories and contracts selected for continuous coverage remain dependent aggregate tasks, not independent dealer replications. Reported net-position peaks leave gross portfolios, hedging arrangements and economic capital requirements unmeasured. Downloaded economic dates omit historical first releases, reporting delays and unrecorded excursions between observations.

The original FX evaluation period was inspected before conditional models were specified, and all earlier-period comparisons are retrospective. The comparisons identify predictive performance, leaving causal effects and the contributions of individual features unresolved. Dependence between observations prevents a coverage guarantee for fitted limits. Choosing among the tested penalties after observing evaluation losses provides a diagnostic comparison, not an implementable selection rule. Validation-length and high-quantile checks were designed after the initial results, with numerical failures retained. Only 6 of 10 high-quantile compatibility fits pass, leaving both FX comparisons unavailable under the rejected repair.

The cost comparisons apply specified reserve, breach and exceedance prices to fixed reported limits. Realized trading returns, funding gains, intervention costs and the effect of imposing those limits on subsequent trading remain unmeasured.

\FloatBarrier

\section{Conclusion}\label{sec:conclusion}

Historical rules are hard to beat, and short training or validation histories favor them in the weekly comparisons. Matched FX gains depend on the historical reference, answering RQ1 (Table~\ref{tab:fx}). Longer validation narrows weekly median loss gaps, answering RQ2 (Table~\ref{tab:v13-validation}). The tested selection rule has 0.00\% median weekly excess, yet 8 of 60 cases lose by over ten percent, reaching 80.98\% at worst (Section~\ref{sec:v13-rp}). Long histories support the larger FX gains but do not by themselves secure an advantage (Figure~\ref{fig:v11-history}). For RQ3, higher reserve charges and lower fixed breach charges generally favor regression, so cost structure determines the preferred rule (Figure~\ref{fig:v10-cost}).

Use historical headroom when the available validation history is short, and require convincing comparative evidence before adopting conditional forecasts. Compare methods with the same training observations and update times, and identify shorter rolling references separately. Report forecast scores, breach counts and cost profiles together, since a lower score can favor a limit with more breaches. This joint report lets users select limits according to their own reserve and breach charges.

\FloatBarrier


```
