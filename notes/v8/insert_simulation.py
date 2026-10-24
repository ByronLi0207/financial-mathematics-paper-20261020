"""B2 document insertion using only archived v8 MC outputs, no model runs."""
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/v8/mc'
rows=json.loads((OUT/'summary.json').read_text())
settings=json.loads((OUT/'experiment-settings.json').read_text())
lookup={(r['dgp'],r['window'],r['features']):r for r in rows}
bindings=[]


def value(d,w,p,field='qr_median_pct'):
    r=lookup[d,w,p];assert r['status']=='COMPLETE'
    i=rows.index(r);text=f"{r[field]:+.1f}"
    bindings.append({'source':'results/v8/mc/summary.json','pointer':f'/{i}/{field}','raw':r[field],'rendered':text})
    return text


if __name__=='__main__':
    path=ROOT/'submission-jof/manuscript.tex';text=path.read_text()
    assert '\\label{sec:calibrated-mc}' not in text
    subsection=r'''
\subsection{Why historical rules are hard to beat: a calibrated simulation}\label{sec:calibrated-mc}

Longer histories help regression under the calibrated stationary weekly mechanisms, which differ from the persistent losses in the financial record. With 33 predictors, median loss changes from D0SHORT\% to D0LONG\% in the constant-variance process as history grows. The weekly GARCH process changes from D2SHORT\% to D2LONG\% (Figure~\ref{fig:calibrated-mc}). These histories contain WSHORT and WLONG completed responses. Constant variance leaves useful level-state information in an AR(1) peak target. The hourly GARCH design completes only one of its eight cells; seven fail the unchanged solver's acceptance criteria. Those entire cells remain failed, including their successful partial repetitions. The prespecified P1 and P3 predictions are unsupported; P2 and P4 are unassessable because required cells failed.

\begin{figure}[htbp]\centering\includegraphics[width=.98\linewidth]{figures/v8-calibrated-mc.pdf}
\caption{Calibrated simulation: median regression loss changes against F, with repetition IQRs shaded. Histories, feature groups and refit schedules are matched. There are RCOUNT repetitions with MCOUNT evaluation origins per complete cell; oracle quantiles use OPCOUNT future paths per origin. Dashed curves and black dots show the finite-path oracle. The hourly panel has seven failed cells; absent curves denote unavailable complete-cell statistics. The Supplement's calibrated-simulation section gives all cells, parameters and failure records.}\label{fig:calibrated-mc}
\end{figure}

'''
    replacements={'D0SHORT':value('D0',52,33),'D0LONG':value('D0',2880,33),
        'D2SHORT':value('D2',52,33),'D2LONG':value('D2',2880,33),
        'WSHORT':str(settings['windows'][0]),'WLONG':str(settings['windows'][-1]),
        'RCOUNT':str(settings['repetitions']),'MCOUNT':str(settings['evaluation_origins']),
        'OPCOUNT':format(settings['oracle_paths'],',')}
    for key,v in replacements.items():subsection=subsection.replace(key,v)
    marker='\\section{Implications for model validation}'
    assert text.count(marker)==1;text=text.replace(marker,subsection+'\\FloatBarrier\n\n'+marker)
    old=r'''\caption{Frequency, history and horizon as a validation decision map. Each entry describes executed comparisons rather than a causal frequency effect. Keep the historical rule until the named advantage survives joint validation.}\label{tab:map}
\begin{tabular}{>{\raggedright\arraybackslash}p{3.3cm}>{\raggedright\arraybackslash}p{3.7cm}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{3.2cm}}\toprule
Frequency / history & Horizon & Evidence & Validation action\\\midrule
Hourly / longer history & Short & Repeated matched score gains; separate wrapper check & Compare named control and breaches\\
Hourly / shorter history & Short & Small score gain with more breaches & Require stable joint performance\\
Hourly / either history & Longer & Losses or weaker gains; coherence and preference sensitivity & Check horizon order and loss preferences\\
Weekly / short or long history & Short or longer & Frequent regression losses despite expanded penalties & Keep historical and parsimonious controls\\
Any source / endpoint bound & Specified horizon & Population premises and plug-in behavior differ & Check absolute displacement and dependence\\
\bottomrule\end{tabular}'''
    new=r'''\caption{Frequency, history and horizon as a validation decision map. Financial outcomes and calibrated-simulation support are distinguished. The simulation does not identify a causal frequency effect.}\label{tab:map}
\begin{tabular}{>{\raggedright\arraybackslash}p{2.7cm}>{\raggedright\arraybackslash}p{3.8cm}>{\raggedright\arraybackslash}p{4.0cm}>{\raggedright\arraybackslash}p{3.2cm}}\toprule
Setting & Financial evidence & Simulation support & Validation action\\\midrule
Hourly / long history / short horizon & Repeated matched gains; separate wrapper check & Unresolved: corresponding hourly cells fail & Compare named control and breaches\\
Hourly / short history / short horizon & Small score gain with more breaches & Unresolved at the financial history length & Require stable joint performance\\
Hourly / either history / longer horizon & Losses or weaker gains; preference sensitivity & Not simulated at the longer horizon & Check horizon order and loss preferences\\
Weekly / either history / either horizon & Frequent losses despite expanded penalties & Short-horizon stationary DGP does not reproduce persistent losses & Retain historical and parsimonious controls\\
Endpoint bound / specified horizon & Population premises and plug-in behavior differ & Separate bound simulation in Supplement; not this calibrated grid & Check displacement and dependence\\
\bottomrule\end{tabular}'''
    assert old in text;text=text.replace(old,new)
    path.write_text(text)
    figure=ROOT/'submission-jof/figures/v8-calibrated-mc.pdf'
    assert not figure.exists();shutil.copyfile(OUT/'mc-main.pdf',figure)
    with (ROOT/'notes/v8/mc-main-bindings.json').open('x') as f:json.dump({'bindings':bindings,'settings_source':'results/v8/mc/experiment-settings.json','figure_source':'results/v8/mc/mc-main.pdf'},f,indent=2);f.write('\n')
