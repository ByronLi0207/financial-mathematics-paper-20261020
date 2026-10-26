"""Integrate only verified saved WP3–5 outputs into the accepted main source.

No forecast, target, model selection or statistical test is executed here.
Existing table/math numeric bytes remain unchanged. New prose values are read
from exact saved fields and recorded with source pointers for independent QA.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
BASELINE='642d6af'
TARGET=ROOT/'submission-jof/manuscript.tex'
BASE=subprocess.check_output(['git','show',BASELINE+':submission-jof/manuscript.tex'],cwd=ROOT).decode()
if TARGET.read_text()!=BASE:raise ValueError('Main source differs from accepted WP6 input; do not overwrite edits')
text=BASE;edits=[];bindings=[]

def replace(old,new,why):
    global text
    if text.count(old)!=1:raise ValueError('Expected unique main-source anchor: '+old[:100])
    text=text.replace(old,new)
    edits.append(dict(before=old,after=new,reason=why))

def load(path):return json.loads((ROOT/path).read_text())

def bound(path,pointer,fmt=None,absolute=False):
    val=load(path)
    for part in pointer.strip('/').split('/'):
        val=val[int(part)] if isinstance(val,list) else val[part]
    display=format(abs(val) if absolute else val,fmt) if fmt else str(val)
    bindings.append(dict(source=path,source_sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pointer=pointer,raw_value=val,display=display,absolute_display=absolute,format=fmt))
    return display

old=BASE.split('\\section{Introduction}\\label{sec:intro}\n\n',1)[1].split('\n\n',1)[0]
new="A dealer's recorded net position can finish inside its limit after exceeding it earlier in the monitoring period, as Figure~\\ref{fig:example} illustrates. The forecasting question concerns the largest sampled exposure before the next review, rather than the endpoint alone. This changes the response and when its training label becomes available. We ask whether additional conditioning improves that peak forecast once historical information is matched, and whether the gain survives alternative references and breach assessment."
replace(old,new,'R1: lead with one forecasting question and its matched-reference/breach criteria')
replace('in the later and earlier periods. Its later advantage survives','in the previously reported later and earlier windows. Its later advantage survives','R4: retain exact original abstract values and distinguish them from the expanded overlapping window')
replace('The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series.\\end{abstract}',
    'The results support joint validation of accuracy, breach behavior, and stability across reference rules, periods, and related series. A controlled simulation rejects a universal narrow-regime explanation, while aggregation and the overlapping backcast further qualify the empirical pattern.\\end{abstract}',
    'R2/R3/R4: add exactly one abstract sentence, honest non-support without a causal-frequency or fresh-validation claim')
replace('Historical rules, regression and local quantiles compete to predict the same peak within each series, using only information available at issue.',
    'In the original ordered comparisons, historical rules, regression and local quantiles compete for the same peak using issue-known observations.',
    'R4: do not extend a real-time-information claim to a backcast whose fixed penalties were selected later')
replace('We establish loss-improving floor projection and a strict-tail bound for true conditional quantiles, and apply the classical Lévy bound under independent symmetric increments.',
    'We record an elementary loss-improving floor projection and the true-quantile strict-tail bound, then apply the classical Lévy inequality under independent symmetric increments.',
    'R1: elementary/classical results support target implementation rather than a new-method claim')
replace('We find that historical rules win most weekly comparisons; repeated regression gains appear in long-history FX data at the shorter horizon.',
    'We find that historical rules win most weekly comparisons, while the original long-history FX gain depends on the chosen reference.',
    'R1/R2: judge observed comparisons rather than announce a universal horizon or frequency boundary')
replace('Section~\\ref{sec:results} reports the gains and failures, and Table~\\ref{tab:map} organizes the frequency--history--horizon decision map.',
    'Section~\\ref{sec:results} reports the gains and failures, and Table~\\ref{tab:map} organizes the observed settings and validation questions. The controlled study rejects the proposed regime restriction, while aggregation supplies a same-dealer contrast without isolating frequency.',
    'R2/R3: C2 includes negative mechanism evidence and the noncausal daily contrast')
replace('We show why peak-limit validation must compare scores, breaches and stability against explicitly matched reference rules.',
    'We show how peak-limit rankings change with the historical reference and breach assessment in these observed forecasting tasks.',
    'R1: established joint evaluation tools are not themselves claimed as the novelty')
replace('We compare same-history and shorter-history rolling controls across two periods, using Murphy diagrams and error-weight preferences to interpret the rankings.',
    'We compare same-history and shorter-history rolling controls across three windows with previously examined outcomes, using established score diagrams and error-weight preferences.',
    'R4/R5: extra displayed window is not an independent period; existing diagnostic lineage remains acknowledged')
# A bounded use statement sits next to the definition, not only in limitations.
replace('We evaluate the latter through pinball loss and count a breach precisely when the observed peak strictly exceeds the reported limit.',
    'We evaluate the latter through pinball loss and count a breach precisely when the observed peak strictly exceeds the reported limit. This report monitors sampled net inventory; its known floor neither measures settlement cash needs nor establishes an optimal operating limit.',
    'R6: measurement/use boundary adjacent to the target')
# New Data facts are read from saved source metadata, never reaggregated.
daily_path='results/revision-v8/wp4/summary.json'
daily=load(daily_path);n_daily=bound(daily_path,'/source_consistency/daily_metadata/n_daily')
n_eval=bound(daily_path,'/cells/0/evaluation/n')
data_add=f'Daily aggregation of the same dealer produces {n_daily} nonempty source-naive calendar days and {n_eval} common evaluation issues. Each day contributes its last record, including partial boundary days, and the report clock follows the end of that day. The timezone and historical release vintage remain unknown; this last-record proxy is distinct from a verified market close or intraday maximum.'
anchor='The data design makes frequency and measurement differences visible instead of treating every sequence as an interchangeable dealer history.'
replace(anchor,anchor+'\n\n'+data_add,'R3: retain actual daily counts and the information/measurement clock near the data definition')
replace('The primary forecasts target the conditional quantile at \\(\\tau=19/20\\), with its upper tail defining the strict-breach event.',
    'The primary forecasts target the conditional quantile at \\(\\tau=19/20\\), with its upper tail defining the strict-breach event. Its nineteen-to-one error preference is hypothetical and is separate from measured funding, trading or settlement costs.',
    'R6: score weights are not measured operating costs')
replace('Parameter selection uses the preceding validation segment, after which the evaluation proceeds on the complete specified issue grid.',
    'The original chronological comparisons select parameters in the preceding validation segment and evaluate the complete specified issue grid. The expanded backcast instead retains penalties selected later, although each coefficient fit and transformation still uses only mature training labels.',
    'R4: label maturity and historical availability of hyperparameters are different conditions')
replace('The earlier FX origins reuse familiar source history, and the later writing-stage HAC comparisons are descriptive rather than independent or prospective confirmation.',
    'The expanded prefix reuses familiar source observations, overlaps the earlier backcast, and follows previous rolling-validation scoring of its target paths. The new extensions were fixed before their own calculations within an already inspected research program. Their tests and the writing-stage HAC comparisons remain descriptive rather than independent or prospective confirmation.',
    'R2/R4/R5/R8: local design freezes do not erase prior inspection or research selection')
# All requested headline MC statistics are pointer-bound, with no new regional search.
mcpath='results/revision-v8/wp3/support.json';mc=load(mcpath)
for field in ['target_clear_gain_count','target_cell_count','outside_clear_gain_count','outside_cell_count']:
    assert mc['procedures']['QR33'][field]==mc['procedures']['QR4'][field]
tg=bound(mcpath,'/procedures/QR33/target_clear_gain_count');tn=bound(mcpath,'/procedures/QR33/target_cell_count')
og=bound(mcpath,'/procedures/QR33/outside_clear_gain_count');on=bound(mcpath,'/procedures/QR33/outside_cell_count')
mcdesign='protocol/revision-v8/wp3-mechanism-design.json';design=load(mcdesign)
reps=bound(mcdesign,'/repetitions')
# The exact count is bound as a difference of frozen endpoints, not a new score.
eval_count=design['evaluation_last']-design['evaluation_first']+1
bindings.append(dict(source=mcdesign,source_sha256=hashlib.sha256((ROOT/mcdesign).read_bytes()).hexdigest(),pointer='/evaluation_first,/evaluation_last',raw_value=[design['evaluation_first'],design['evaluation_last']],display=str(eval_count),derivation='last-first+1'))
mcparagraph=f'The controlled mean-reverting level study with GARCH innovations rejects the proposed narrow-regime explanation \\citep{{bollerslev1986}}. Each regression shows clear gains in only {tg} of {tn} target cells. Both also show clear gains in {og} of {on} outside cells, including homoskedastic and longer-horizon cases. The experiment uses {reps} independent repetition streams with common innovations across conditions and {eval_count} evaluation issues per repetition. Figure~\\ref{{fig:mechanism}} reports relative mean losses with Monte Carlo standard errors. These specified processes therefore do not establish a universal history, volatility or horizon boundary.'
classes=daily['classifications'];wins=sum(c['historical_wins'] for c in classes.values());total=sum(c['planned_comparisons'] for c in classes.values())
bindings.append(dict(source=daily_path,source_sha256=hashlib.sha256((ROOT/daily_path).read_bytes()).hexdigest(),pointer='/classifications/QR33,/classifications/QR4',raw_value={k:{f:c[f] for f in ['historical_wins','planned_comparisons']} for k,c in classes.items()},display=f'{wins} / {total}',derivation='sum both frozen regression counts'))
exceptions=[(i,c) for i,c in enumerate(daily['contrasts']) if c['status']=='COMPLETE' and c['relative_loss_percent']<0]
assert len(exceptions)==1
idx,ex=exceptions[0];assert ex['method']=='QR4' and ex['window']==max(r['window'] for r in daily['cells']) and ex['horizon']==min(r['horizon'] for r in daily['cells'])
rel=bound(daily_path,f'/contrasts/{idx}/relative_loss_percent','.1f',True)
model_i=next(i for i,r in enumerate(daily['cells']) if (r['window'],r['horizon'],r['method'])==(ex['window'],ex['horizon'],ex['method']))
ref_i=next(i for i,r in enumerate(daily['cells']) if (r['window'],r['horizon'],r['method'])==(ex['window'],ex['horizon'],'F'))
hit=bound(daily_path,f'/cells/{model_i}/evaluation/strict_breach_count');refhit=bound(daily_path,f'/cells/{ref_i}/evaluation/strict_breach_count')
dailyparagraph=f'Same-dealer daily aggregation produces predominantly historical-rule score wins. Historical headroom wins {wins} of the {total} specified comparisons. The exception is the longer-history four-predictor regression at the shorter daily horizon, with about a {rel}\\% score reduction. It records {hit} breaches versus {refhit} for historical headroom. Aggregation changes physical histories, horizons, update cadence, predictors, evaluation span and the sampled peak together. Source identity is held fixed, but this contrast does not identify a pure frequency effect.'
bcpath='results/revision-v8/wp5/summary.json';bc=load(bcpath)
matched_i=next(i for i,c in enumerate(bc['contrasts']) if (c['horizon'],c['method'],c['reference'])==(6,'QR33','F_matched'))
rolling_i=next(i for i,c in enumerate(bc['contrasts']) if (c['horizon'],c['method'],c['reference'])==(6,'QR33','F_rolling720'))
a=bound(bcpath,f'/contrasts/{matched_i}/relative_change_percent','.1f',True);b=bound(bcpath,f'/contrasts/{rolling_i}/relative_change_percent','.1f',True)
ah=bound(bcpath,f'/contrasts/{matched_i}/model_breaches');bh=bound(bcpath,f'/contrasts/{matched_i}/reference_breaches');pv=bound(bcpath,f'/contrasts/{rolling_i}/dm/dm_p','.3f')
backcastparagraph=f'An expanded fixed-parameter backcast preserves the reference-sensitive pattern but supplies no fresh independent validation. For original short-horizon FX regression, matched score falls about {a}\\%, while its rolling-reference advantage is about {b}\\%. Matched breaches are {ah} for regression and {bh} for historical headroom. The raw rolling-reference DM p-value is about {pv} and remains descriptive. Earlier rolling-validation scoring already covered these target paths, and the smaller backcast is fully nested. Penalties were chosen later, so these overlapping windows cannot be interpreted as independent replications.'
figure=r'''\begin{figure}[htbp]\centering\includegraphics[width=.98\linewidth]{figures/v8-wp3-qr33-loss.pdf}
\caption{Relative mean loss of the original regression against matched historical headroom in the controlled level-persistence and volatility-clustering grid. Annotations give the relative change with its Monte Carlo standard error. Panels vary horizon and level persistence; cells vary history and variance persistence. Gains outside the prespecified region contradict a universal narrow-condition explanation.}\label{fig:mechanism}
\end{figure}'''
addition='\\FloatBarrier\n\n\\subsection{Controlled and within-record extensions}\\label{sec:extensions}\n\n'+mcparagraph+'\n\n'+figure+'\n\n'+dailyparagraph+'\n\n'+backcastparagraph+'\n\n'
anchor='\\FloatBarrier\n\n\\section{Implications for model validation}'
replace(anchor,addition+anchor,'R2/R3/R4/R5: exactly one MC paragraph/figure and existing daily/backcast results; no new analysis')
replace('Report the mean quantile loss together with strict-hit frequency, overrun amounts, and the magnitude of unused headroom under the same issue grid.',
    'Report the mean quantile loss together with breach frequency, overrun amounts, and unused headroom under the same issue grid.',
    'R6: direct reader-facing language for the measured diagnostics')
replace('Table~\\ref{tab:map} summarizes this checklist and maps the observed frequency, history, and horizon conditions to their principal comparative outcomes.',
    'Table~\\ref{tab:map} organizes observed comparison settings and the validation questions they raise, including the daily and longer-horizon exceptions.',
    'R2/R3/R6: map remains descriptive and does not become a universal eligibility or deployment rule')
replace('The hourly FX result motivates further evaluation of long-history short-horizon regression, while the weekly results support a demanding historical starting benchmark.',
    'The original hourly FX result motivates further evaluation of its named regression, while the weekly and daily comparisons support demanding historical benchmarks.',
    'R3/R6: retain benchmark role without certifying F as an operating limit')
replace('\\caption{Frequency, history and horizon as a validation decision map. Each entry describes executed comparisons rather than a causal frequency effect. Keep the historical rule until the named advantage survives joint validation.}',
    '\\caption{Observed comparison settings and validation questions. Entries organize retrospective evidence rather than a causal frequency effect or deployment policy. A winning score leaves breach behavior and operating suitability to be assessed.}',
    'R3/R6: remove an unsupported imperative to keep/deploy the historical report')
replace('Hourly / either history & Longer & Losses or weaker gains; coherence and preference sensitivity & Check horizon order and loss preferences\\\\',
    'Hourly / either history & Longer & Matched backcast gains coexist with reference-sensitive losses; coherence and preference sensitivity remain & Check the named reference, horizon order and loss preferences\\\\',
    'R2/R4: retain longer-horizon backcast gains rather than a literal short-horizon-only rule')
replace('Weekly / short or long history & Short or longer & Frequent regression losses despite expanded penalties & Keep historical and parsimonious controls\\\\',
    'Daily / same dealer & Horizons in nonempty days & Historical score wins predominate; one four-predictor gain has more breaches & Retain both controls and assess their own breaches\\\\\nWeekly / short or long history & Short or longer & Frequent regression losses despite expanded penalties & Compare historical and parsimonious controls\\\\',
    'R3/R6: add daily row, keep exception, do not turn relative accuracy into nominal safety')
replace('Those periods provide a stability check within this record rather than independent dealer replication or a prospective test on unseen future outcomes.',
    'These overlapping windows and the previously viewed later period describe stability within the record rather than independent dealer replication or prospective performance. The expanded prefix includes the earlier backcast and uses penalties selected after its issue dates.',
    'R4: explicitly retain nesting, past inspection and later-selected hyperparameters')
oldconclusion=text.split('\\section{Conclusion}\\label{sec:conclusion}\n\n',1)[1].split('\n\n',1)[0]
newconclusion='Simple historical rules are strong competitors for predicting the largest sampled absolute position before a monitoring horizon ends. The original long-history FX regression gains against matched headroom survive in the broader backcast on previously examined observations, although score reductions coexist with more breaches. Longer-horizon backcast gains and the daily exception prevent a literal short-horizon or hourly-only interpretation. The controlled simulation also rejects the proposed narrow-regime restriction, while the same-dealer aggregation contrast leaves frequency mixed with measurement and clock changes. The defensible result is reference-sensitive comparative accuracy in these records, rather than a universal mechanism or validated operating-limit rule.'
replace(oldconclusion,newconclusion,'R1–R6: conclusion follows all adverse and qualifying evidence, not only original favorable pattern')
replace('This revision adds no new financial experiment. The completed results include adverse, failed and unavailable cases.',
    'This revision adds three design-frozen exploratory extensions: a controlled simulation, a same-dealer daily aggregation contrast and an expanded inspected backcast. The completed results include adverse, failed and unavailable cases; arithmetic readback establishes artifact consistency rather than independent scientific replication.',
    'R8: remove stale pre-v8 provenance statement without claiming independent reproduction')
# New primary-source bibliography entry has independently verified original metadata.
entry=r'''\bibitem[Bollerslev(1986)]{bollerslev1986} Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. \emph{Journal of Econometrics}, \emph{31}(3), 307--327. \url{https://doi.org/10.1016/0304-4076(86)90063-1}.

'''
replace('\\bibitem[Boudoukh et al.(2004)]',entry+'\\bibitem[Boudoukh et al.(2004)]','Verified original GARCH reference, not the later reprint')
# Preserve every old result-table numeric token, including the map's empty numeric vector.
tables=lambda s:re.findall(r'\\begin\{table\}.*?\\end\{table\}',s,re.S)
assert len(tables(BASE))==len(tables(text))==6
numeric=lambda s:re.findall(r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?',s)
assert all(numeric(a)==numeric(b) for a,b in zip(tables(BASE),tables(text)))
maths=lambda s:re.findall(r'\\\[.*?\\\]',s,re.S)
assert maths(BASE)==maths(text)
source=ROOT/'results/revision-v8/wp3/figures/v8-wp3-qr33-loss.pdf';dest=ROOT/'submission-jof/figures/v8-wp3-qr33-loss.pdf'
if dest.exists():raise ValueError('Figure copy already exists; do not overwrite')
shutil.copyfile(source,dest);assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(dest.read_bytes()).digest()
TARGET.write_text(text)
receipt=dict(generated_utc=datetime.now(timezone.utc).isoformat(),operation='Existing saved fields and prose integration only; no new financial calculation',baseline_commit=BASELINE,before_sha256=hashlib.sha256(BASE.encode()).hexdigest(),after_sha256=hashlib.sha256(text.encode()).hexdigest(),edits=edits,new_reader_numeric_bindings=bindings,all6_original_table_numeric_vectors_unchanged=True,all_original_display_math_blocks_byte_identical=True,main_figures=len(re.findall(r'\\begin\{figure\}',text)),main_tables=len(tables(text)),source_figure_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),abstract_added_sentences=1,main_MC_result_paragraphs=1,scientific_results_modified=False,original_primaries_modified=False)
(ROOT/'notes/revision-v8/wp7-main-integration.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:receipt[k] for k in ['operation','main_figures','main_tables','abstract_added_sentences','main_MC_result_paragraphs','all6_original_table_numeric_vectors_unchanged','all_original_display_math_blocks_byte_identical','scientific_results_modified']},indent=2))
