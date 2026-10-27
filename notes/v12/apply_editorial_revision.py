"""Apply the specified v12 prose/structure edits; no financial computations."""
from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parents[2];D=R/'submission-v10';p=D/'manuscript.tex';s=p.read_text();old=s
records=[]
def change(before,after,item):
 global s
 assert before in s,(item,before[:100]);s=s.replace(before,after,1);records.append(dict(item=item,before=before,after=after))
# Preserve the exact source text of moves before editing.
menu=s[s.index(r'\subsection{Isolating the penalty menu}'):s.index(r'\section{RQ3: limit-cost regions}')]
limits=s[s.index(r'\section{Limitations}'):s.index(r'\section{Conclusion}')]
relocated='Beyond the matched long-history case, short-history FX regression performs poorly at the longer horizon. Loss rises by 31.5\\% against matched historical headroom. Regression records 924 breaches against 427 for the reference; the full horizon map retains the other adverse comparisons.'
assert relocated in s
change(relocated+'\n\n','',7)
anchor='Delayed calibration retains the later matched FX gain.'
pos=s.index(anchor);s=s[:pos]+relocated+'\n\n'+s[pos:];records.append(dict(item=7,before=relocated,after='Moved verbatim to RQ1 before delayed calibration.'))
# Verified literature table with four consistently documented columns.
a=s.index(r'\begin{table}[htbp]\centering\footnotesize');b=s.index(r'\end{table}',a)+len(r'\end{table}')
table=r'''\begin{table}[htbp]\centering\footnotesize
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
\end{table}'''
change(s[a:b],table,5)
# Three/four sentence proposition statements, preserving mathematical displays.
a=s.index('Suppose \\(Y\\ge B\\) almost surely',s.index(r'\textbf{Proposition'))
b=s.index('\n\n',a)
change(s[a:b],r'Suppose \(Y\ge B\) almost surely and the issue information contains \(B\). Projecting any forecast \(c\) to \(\max\{B,c\}\) weakly improves pinball loss for every outcome, with the gain shown below. The true conditional lower inverse quantile at level \(1-\alpha\) has strict exceedance probability at most \(\alpha\), including at atoms.',6)
a=s.index('Let future increments be independent',s.index(r'\label{prop:levy}'));b=s.index('\n\n',a)
change(s[a:b],r'Let future real increments be independent and individually symmetric about zero, with partial sums \(S_h\). Fix a starting position \(x\), set \(B=|x|\), and let \(q\) be the population \((1-\alpha/2)\) quantile of \(|S_H|\). The triangle inequality and the classical L\'evy maximal inequality imply the bound below. A conditional application requires these assumptions and the endpoint quantile under the law given issue-time information.',6)
change('Supplement Sections S1--S2 prove both statements and distinguish population quantiles from their empirical plug-ins; Sections S3--S5 give the bound simulations. A conditional application requires independence, symmetry and the stated endpoint quantile under the law given issue information. The separate bound simulations distinguish mean-reverting levels from serially correlated increments.', 'Supplement Sections S1--S2 retain the proofs and empirical qualifications, while Sections S3--S5 distinguish mean-reverting levels from serially correlated increments.',6)
change('Separately fitted horizon forecasts can violate the ordering of true peak quantiles. Short-history FX regression produces horizon crossings on 640 evaluation origins. Label nesting, floor coverage and strict-breach definitions provide additional checks on the issued reports.', 'Separately fitted horizons can violate peak-quantile ordering, so Supplement Section S36 retains the original crossing diagnostic alongside the floor and nesting checks.',11)
# Data table2 follows source descriptions, and naturally moves methods table to3.
change('Every method within a comparison uses identical peak labels, current floors and issue origins. Source units and histories remain distinct across series. The same-record aggregation holds dealer identity fixed while changing the measurement clock.', r'Table~\ref{tab:v12-data} describes the aligned source records and complete six-record peaks, with monetary series expressed in USD millions. Panel summaries take medians of within-series statistics, preserving heterogeneous exposures rather than pooling levels across categories or contracts. Within each forecasting comparison, every method uses identical peak labels, current floors and issue origins. The same-record FX aggregation holds dealer identity fixed while changing its measurement clock and sampled response.'+'\n\n'+r'\input{generated/v12-data-table.tex}',1)
# Formal historical report and ridge objective.
needle='Historical headroom uses the corrected empirical rank of completed headrooms and adds its report to the current magnitude.'
rep=r'''Historical headroom adds a corrected empirical quantile of completed headrooms to the observed magnitude:
\[
F_{t,H}=B_t+Q_j\{Z_{i,H}:i\in\mathcal T_r\},\qquad
j=\lceil(m+1)\tau\rceil,\quad m=|\mathcal T_r|.
\]
Here \(Q_j\) is the \(j\)th order statistic, and the training set contains only labels completed by refit time \(r\).
At the sensitivity level where this rank exceeds the sample size, the rank is capped at \(m\), producing the historical maximum.
This finite-sample reporting convention supplies no coverage guarantee under the observed dependence.'''
change(needle,rep,2)
needle='Expanded-menu full regression changes only the penalty grid.'
rep=r'''Expanded-menu full regression changes only the penalty grid, using the following training-scaled objective:
\[
(\hat a,\hat b)=\arg\min_{a,b}\left\{
\frac1m\sum_{i\in\mathcal T_r}\rho_\tau\!\left(\frac{Z_{i,H}}s-a-x_i^\top b\right)
+\frac\lambda2\|b\|_2^2\right\},\qquad
\lambda\in\{0.001,0.01,0.1,1,10,\infty\}.
\]
The intercept is unpenalized; training rows alone determine the feature transform and response scale \(s\).
Reports are \(B_t+s\max\{0,\hat a+x_t^\top\hat b\}\), while infinite shrinkage gives the ordinary empirical headroom quantile.
The original menus and scale definitions remain in Table~\ref{tab:methods} and Supplement Sections S8 and S23.'''
change(needle,rep,2)
needle='Tables identify the small-sample adjustment and named multiplicity families'
s=s.replace(needle,'Tables identify the small-sample adjustment and named multiplicity families',1)
a=s.index('Hit diagnostics use a fixed spaced grid');b=s.index('\n\n',a)
dm=r'''
For paired loss differences \(d_t\), the comparison statistic and its existing bandwidth are
\[
\mathrm{DM}=\frac{\sqrt n\,\bar d}{\sqrt{\widehat\Omega_K}},\qquad
K=\min\{n-1,\max[H,\lfloor4(n/100)^{2/9}\rfloor]\},
\]
where \(\widehat\Omega_K\) is the Newey--West long-run variance estimate with Bartlett weights.
'''
s=s[:b]+dm+s[b:];records.append(dict(item=2,before='DM described only in prose.',after=dm))
# Reader-oriented design and multiple-method explanation.
a=s.index('The original protocol fixes the two main comparisons');b=s.index('\n\n',a)
change(s[a:b],r'The original protocol fixes the two main comparisons and their reference procedures; the original FX evaluation period had already been inspected. Each new analysis states its prediction thresholds before computation (Supplement Section S36), with chronological records retained separately from the results. These later checks remain retrospective, and their descriptive fractions do not treat related markets as independent replications.',4)
change('Matched F/I aliases merge only after full forecast and target equality. Rolling references remain distinct. Literal sole membership differs from a sole surviving loss class containing several procedures.', 'Historical reports are merged only after their full forecasts and targets match, while rolling references remain distinct. Several methods can produce identical losses, so one surviving loss pattern need not mean that only one method survives.',4)
# Remove vague unsupported facts; give scope and implication instead.
change('Simpler conditional reports and fixed combinations also give mixed weekly results. The headroom recursion is also worse. Supplement Sections S16--S18 retain the combination and headroom-recursion results, including completed losses and failures (Tables S14--S17).', 'Neither simpler conditioning nor fixed combinations establish a uniform weekly improvement, reinforcing the need to retain the historical benchmark in each comparison. Supplement Sections S16--S18 retain their complete losses and failures, including the headroom-recursion results (Tables S14--S17).',10)
a=s.index('The independent reporting system gives a similar overall ranking:');b=s.index('\n\n',a)
change(s[a:b],r'The independent reporting system gives a similar overall ranking: a historical headroom rule has lower loss in 29 of 34 contract/history comparisons. This meets the pre-specified 60\% threshold, using the better realized score of corrected and ordinary empirical historical reports rather than an executable selector. Corrected historical headroom remains the fixed matched reference, with the ordinary empirical version reported separately. Both full-regression medians exceed the pre-specified ten-percent tolerance, whereas four-feature regression moves closer to history with the longer window. These comparisons extend the benchmark pattern to a separate reporting system while retaining substantial contract-level variation.',4)
s=s.replace('Expanded-menu regression relative loss versus matched F','Expanded-menu regression relative loss versus matched historical headroom')
s=s.replace('mean unused allowance','mean overprediction')
change('Table~\\ref{tab:v10-mcs-main} distinguishes literal membership from exact observed-loss equality.', 'Table~\\ref{tab:v10-mcs-main} reports surviving methods, with identical observed-loss patterns explained separately in Supplement Section S31.',4)
# New section immediately after RQ2 and its MCS evidence.
change(menu,'',3)
anchor=r'\subsection{Scores and breach behavior answer different questions}'
s=s.replace(anchor,r'\input{generated/v12-low-frequency.tex}'+'\n\n'+anchor,1)
records.append(dict(item=3,before=menu,after='Replaced original menu-only subsection with new generated low-frequency subsection after RQ2; old text relocated verbatim in Supplement S36.'))
# Required short limitations; extra original technical wording moves verbatim.
newlimits=r'''\section{Limitations}\label{sec:limitations}

\begin{itemize}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}
\item FX comes from one market maker, and its original evaluation period was inspected before conditional methods were specified.
\item The earlier-period comparison and full-prefix backcast are retrospective, with no previously unseen prospective financial evaluation.
\item Weekly reports aggregate positions across dealers; related categories and the CFTC survivor universe do not provide independent dealer replications.
\item Downloaded economic-date vintages omit historical first-release information, reporting delays and unrecorded within-interval excursions.
\item The comparisons identify neither causal effects nor individual-feature effects, and fitted limits receive no coverage guarantee under this dependence.
\item Costs illustrate fixed preferences; trading returns, funding gains and institutional intervention costs are not measured.
\item The finite-penalty hindsight bound is diagnostic only; validation-length and quantile-sensitivity checks are post-result analyses with numerical failures retained.
\end{itemize}
Supplement Section S36 retains the original technical qualifications on simulations, aggregation and forecast comparison.

\FloatBarrier

'''
change(limits,newlimits,8)
# Clean code statement / latest user override on active AI declaration.
a=s.index(r'\paragraph{Code availability.}');b=s.index('\n\n',a)
change(s[a:b],r'\paragraph{Code availability.} Code, results and reproduction instructions are available at \url{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v12}.',9)
s=s.replace('AI statement: [TO BE COMPLETED BY AUTHOR].\n','')
s=re.sub(r'\\bibitem\[Sussman\(2023\)\]\{sussman2023\}[^\n]*\n\n','',s)
p.write_text(s)
for n in ['title-page.tex','AUTHOR-TODO.md']:
 f=D/n;t=f.read_text();t='\n'.join(x for x in t.split('\n')if not re.search(r'AI statement:|AI disclosure|AI statement|AI 声明',x,re.I));t=t.replace('/tree/revision-v11','/tree/revision-v12');f.write_text(t)
f=D/'references.bib';t=f.read_text();t=re.sub(r'@article\{sussman2023,.*?\n\}\n?', '',t,flags=re.S);f.write_text(t)
out=R/'notes/v12/editorial-structural-changes.json';assert not out.exists();out.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
# Original passages are stored before active editing for exact-move verification.
f=R/'notes/v12/original-relocation-text.json';assert not f.exists();f.write_text(json.dumps(dict(menu=menu,limitations=limits,short_history_fx=relocated),indent=2)+'\n')
print('Applied',len(records),'specified structural changes; original relocations saved.')
