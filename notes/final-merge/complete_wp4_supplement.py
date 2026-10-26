"""Add existing analytic qualifications and the saved new CFTC readout."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'submission-final'
EXTENDED='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/EXTENDED_RESULTS.md'


def main():
    main=DEST/'manuscript.tex';m=main.read_text()
    assert 'final-analytic-qualifications.tex' not in (DEST/'supplement.tex').read_text()
    # Restore A's precise interpretation contracts to the new combined text.
    floor='This finite-sample reporting convention supplies no coverage guarantee under the observed dependence.'
    assert floor in m
    m=m.replace(floor,floor+' In weekly replays, the current floor is known under the stipulated economic-date information set of the downloaded vintage. Historical first-release availability is not reconstructed.')
    old='Separately fitted horizons can violate peak-quantile ordering, so Supplement Section S36 retains the original crossing diagnostic alongside the floor and nesting checks.'
    assert old in m
    m=m.replace(old,'Separately fitted horizons can violate the ordering of a common lower-inverse peak quantile under the same information law. Sorting crossed reports weakly improves equally weighted aggregate pinball loss when units and quantile levels coincide. This aggregate statement supplies neither a per-horizon loss guarantee nor a coverage guarantee. The Supplement retains the original crossing diagnostic and the precise analytic qualifications.')
    wrapper='Calibration therefore changes breach frequency, while the distinct score and hit rankings persist on the common comparison grid.'
    assert wrapper in m
    m=m.replace(wrapper,wrapper+' Each wrapper has a higher saved mean score than its own unwrapped base, so the retained relative ranking coexists with an absolute score cost. The headroom-SAV recursion refits on its evaluation training pools, whereas the selected ACI wrapper carries its delayed calibration state.')
    methods='this table retains the executed menus.'
    m=m.replace(methods,methods+' The CFTC mechanism extension adds the longer history described in Section~\\ref{sec:history-mechanism}.')
    main.write_text(m)
    source=ROOT/'submission-jof/generated/v9-substantive-qualifications.tex'
    target=DEST/'generated/final-analytic-qualifications.tex';target.write_bytes(source.read_bytes())
    supplemental=DEST/'supplement.tex';s=supplemental.read_text()
    old='Repairing a long-horizon report upward can worsen pinball loss; target ordering\nalone does not identify a universally beneficial repair.'
    assert old in s
    s=s.replace(old,'Raising only the long-horizon report can worsen its marginal pinball loss.\nAt a common level and in common units, sorting crossed reports instead weakly\nimproves the equally weighted aggregate pinball score. The retained analytic\nqualification below gives the exact samplewise identity and its limitations.')
    s=s.replace('The complete 204 method cells finish without a numerical retry.',
        'The original six-procedure, two-history study has 204 complete method cells without a numerical retry. The separate registered extension below adds only the three named procedures at the longer history.')
    s=s.replace(r'Sections~\ref{sup:ar} and~\ref{sup:rank}',
        r'\href{'+EXTENDED+r'}{the extended AR-residual section} and Section~\ref{sup:rank}')
    s=s.replace(r'\end{document}',r'''
\paragraph{Scope of the retained analytic source.}
The following note is copied byte-for-byte from the accepted A-line analytic
source. References to the earlier or protected Supplement identify that
historical package. The current combined text adopts the corrected sorting,
quantile-selection, information-set and calibration qualifications.
\input{generated/final-analytic-qualifications.tex}

\input{generated/final-cftc-extension.tex}
\end{document}
''')
    supplemental.write_text(s)
    summary=json.loads((ROOT/'results/final-merge/wp2-cftc-mechanism/summary.json').read_text())
    lines=[r'\section{Registered CFTC history extension and complete long-history diagnostics}\label{sup:final-cftc}',
        r'The extension retains the original market universe, downloaded arrays and chronological split. Only the new history is fitted; the two older histories reuse their byte-identical saved predictions. The '+r'\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/protocol/final-merge/wp2-cftc-mechanism.md}{fixed protocol}'+' was locally committed before the new calculations. This is not a claim of external public preregistration or an untouched CFTC holdout.',
        r'At $W=520$ and $H=6$, the first validation training origin is $28$. Its last completed training label ends at the refit. The unchanged validation indices are $553$--$604$ and evaluation indices are $611$--$870$. Every validation label ends before evaluation begins. Both model menus and their distinct original failure policies remain fixed.',
        r'P1 uses separate method-specific low-region counts; both must pass. P2 uses sparse regression in the high region; the full procedure has no eligible high-region cell. The primary verdict is PARTLY. P3 is a secondary strict decrease at both successive history steps and is NOT\_SUPPORT. Ties meet neither a strict win nor a strict loss. Planned denominators retain unknown cells, although none occurs here.',
        r'The two tables show every new long-history conditional-versus-F comparison. Loss is in each contract\textquotesingle s own count units and is never pooled across contracts. Strict breach counts use the complete common evaluation axis. Raw normal HAC probabilities retain the fixed Bartlett bandwidth and are descriptive dependent diagnostics; no new family-adjusted significance claim follows.',
        r'The '+r'\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/notes/final-merge/wp2-cftc-mechanism-results.md}{complete result readout}'+r' contains every shorter-history cell, all candidate/status receipts and the full counterexample list. Each cell has a trace SHA-256 in the '+r'\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/results/final-merge/wp2-cftc-mechanism/cells.csv}{cell inventory}'+'. No unfavorable market is omitted from either the plot or the reported counts.']
    bindings=[]
    def f(x):return 'NA' if x is None else format(x,'.6g')
    for method,label in [('QR33','Full regression'),('QR4','Four-predictor regression')]:
        lines += [r'\begingroup\footnotesize\setlength{\tabcolsep}{3pt}',r'\begin{longtable}{llrrrrrl}',
            r'\caption{'+label+r' at the added CFTC history. Positive loss changes favor historical F.}\label{tab:final-cftc-'+method+r'}\\',
            r'\toprule Code & $F$ loss & Model loss & Change (\%) & Breaches $F$/model & HAC $t$ & Raw $p$ & Penalty\\\midrule\endfirsthead',
            r'\caption[]{Continued.}\\\toprule Code & $F$ loss & Model loss & Change (\%) & Breaches $F$/model & HAC $t$ & Raw $p$ & Penalty\\\midrule\endhead\bottomrule\endfoot']
        for i,row in enumerate(summary['comparisons']):
            if row['window']!=520 or row['method']!=method:continue
            fields=['code','reference_loss','model_loss','relative_loss_percent','reference_breach_count','model_breach_count','dm/dm_t','dm/dm_p','selected_penalty']
            for field in fields:
                value=row
                for part in field.split('/'):value=value[part]
                bindings.append(dict(table_method=method,code=row['code'],pointer=f'/comparisons/{i}/'+field,value=value))
            penalty=r'$\infty$' if row['selected_penalty']=='inf' else f(row['selected_penalty'])
            lines.append(' & '.join([row['code'],f(row['reference_loss']),f(row['model_loss']),f(row['relative_loss_percent']),str(row['reference_breach_count'])+'/'+str(row['model_breach_count']),f(row['dm']['dm_t']),f(row['dm']['dm_p']),penalty])+r' \\')
        lines += [r'\end{longtable}\endgroup']
    lines += [r'The seven sparse-procedure high-region counterexamples are codes 044601, 043602, 042601, 045601, 099741, 095741 and 232741. The full list also retains every short-region exception and all failures of strict history improvement. Separate scalar scoring, HAC, selection and maturity implementations give zero mismatches under the predeclared floating-point tolerance; integer and input-hash identities are exact. This is algorithmic checking by one executor, not independent data replication or a second finite-penalty solver.',
        r'Aggregate dealer markets, prior inspection of shorter histories, differing menus, a selected simulation coordinate and broad fixed-grid intervals all limit transport. A score improvement does not identify a causal estimation-cost mechanism or a safe trading policy.']
    # ASCII apostrophe avoids an additional package dependency in this copied preamble.
    text='\n\n'.join(lines).replace(r'\textquotesingle s',"'s")+'\n'
    (DEST/'generated/final-cftc-extension.tex').write_text(text)
    report=dict(status='GENERATED_PENDING_COMPILE',analytic_source=str(source.relative_to(ROOT)),analytic_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),analytic_destination_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),analytic_copy_byte_identical=source.read_bytes()==target.read_bytes(),long_history_rows=34,bound_fields=len(bindings),bindings=bindings,source='results/final-merge/wp2-cftc-mechanism/summary.json',source_sha256=hashlib.sha256((ROOT/'results/final-merge/wp2-cftc-mechanism/summary.json').read_bytes()).hexdigest(),new_model_fits=0)
    (ROOT/'notes/final-merge/wp4-supplement-additions.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='bindings'},indent=2))


if __name__=='__main__':main()
