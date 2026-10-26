from pathlib import Path
p=Path('submission-v10/manuscript.tex');s=p.read_text();a=s.index(r'\section{RQ3: limit-cost regions}');b=s.index(r'\begin{figure}',a)
# All method definitions/grid remain in the Supplement, with one compact displayed definition here.
s=s[:a]+r'''\section{RQ3: limit-cost regions}\label{sec:cost}

\[
J_m(\kappa,\beta,c)=\kappa\frac{\overline{C_m-B}}{m_F}
+\beta\,\overline{\mathbf 1\{Y>C_m\}}
+c\frac{\overline{(Y-C_m)_+}}{m_F},\qquad
m_F=\overline{C_F-B}>0,\quad\beta=b/m_F.
\]

For CFTC, higher reserve coefficients and lower fixed-breach coefficients generally favor expanded-menu regression over matched historical headroom, although the grid is not monotone (Figure~\ref{fig:v10-cost}).
At $c=1$, regression is cheaper in $5/34$ comparisons at $(\kappa,\beta)=(.1,.25)$, $32/34$ at $(1,0)$, and $1/34$ at $(.01,5)$.
These are illustrative costs, not observed operating costs; the Supplement gives the normalization, fixed grid and complete-method results.

''' +s[b:]
s=s.replace(r'\caption{Complete registered reserve/fixed-breach regions at $c=1$. Color is the planned-comparison fraction where the fixed conditional procedure costs less than F. Each panel retains its source, horizon and history grids with equal comparison weights. These fractions are not probability estimates. All comparisons complete, so lower and upper fractions coincide.}',r'\caption{Fixed reserve and breach-charge regions with the exceedance coefficient held at unity. Color shows the fraction of related comparisons where the stated conditional procedure costs less than corrected historical headroom, with each source group retaining its own histories and horizons. These are descriptive fractions; all comparisons complete and the lower and upper fractions coincide.}')
s=s.replace(r'\caption{Paired penalty-menu isolation on unchanged calibrated paths. The expanded menu removes the large short-history full-regression loss in both arms. Longer-history full-regression summaries remain unavailable because one required source repetition fails in each arm. No successful subset replaces them.}',r'\caption{Paired penalty-menu isolation on unchanged calibrated paths. The expanded menu removes the large short-history full-regression loss in both arms. Longer-history full-regression summaries remain unavailable because a required repetition fails in each arm, with no successful-subset replacement.}')
p.write_text(s)
# Two substantive paragraphs, native editable letter, existing author placeholder retained.
p=Path('submission-v10/cover-letter.tex');s=p.read_text();a=s.index('Dear Editors,');b=s.index('Sincerely,',a)
s=s[:a]+r'''\textbf{Submission:} Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits

Dear Editors,

Matched FX gains remain reference-dependent, weekly historical controls remain competitive, and CFTC expanded regression is generally cheaper under higher reserve and lower fixed-breach charges, with local exceptions.

The paper suits Journal of Forecasting through its comparison of complete forecast procedures under matched histories and update schedules. Calibrated simulations link large short-history losses to narrow penalty menus; the registered switching increment is unsupported. Model confidence sets and cost-preference regions connect forecast evaluation to limit validation across related aggregate series. The methods are established, and the evidence remains retrospective. The accompanying materials provide native sources, complete adverse and unavailable results, official CFTC source records and \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/revision-v10b}{versioned code and public aggregate results}. Restricted FX observations and private prediction vectors remain excluded; author details and declarations await completion in the supplied templates.

''' +s[b:];p.write_text(s)
p=Path('submission-v10/title-page.tex');s=p.read_text().replace('/tree/revision-v10}', '/tree/revision-v10b}');p.write_text(s)
