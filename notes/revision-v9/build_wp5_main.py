"""Evidence-bounded v9 prose; copy all original numerical results unchanged."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE='32ee58688bac260de322c31cb8945adbf3b53154'
SNAP=ROOT/'notes/revision-v9/wp5-source-before.tex'
SOURCE_FILES={'wp1':'results/revision-v9/wp1/breakeven.json','wp2':'results/revision-v9/wp2/support.json','curves':'results/revision-v9/wp3/curve-predictions.json','clock':'protocol/revision-v9/wp3-learning-curve.json','coordinate':'protocol/revision-v9/wp1-posthoc-design.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def get(data,pointer):
 for part in pointer.lstrip('/').split('/') if pointer else []:data=data[int(part)] if isinstance(data,list) else data[part]
 return data

def main():
 before=subprocess.check_output(['git','show',BASE+':submission-jof/manuscript.tex'],cwd=ROOT)
 if not SNAP.exists():
  with SNAP.open('xb') as f:f.write(before)
 assert SNAP.read_bytes()==before
 s=before.decode();original=s;sources={k:json.loads((ROOT/p).read_text()) for k,p in SOURCE_FILES.items()};contexts=[];changes=[]
 def replace(old,new,ident):
  nonlocal s
  assert s.count(old)==1,(ident,s.count(old));s=s.replace(old,new);changes.append(dict(id=ident,before=old,after=new))
 def paragraph(anchor,new,ident):
  start=s.index(anchor);end=s.index('\n\n',start);replace(s[start:end],new,ident)
 def bound(ident,text,definitions):
  binds=[]
  for needle,source_key,pointer,operation,kind in definitions:
   raw=get(sources[source_key],pointer);op=operation
   if op['type']=='format':shown=format(raw,op['spec'])
   elif op['type']=='exact':shown=str(raw)
   elif op['type']=='count_eq':
    n=sum(get(x,op['field'])==op['equals'] for x in raw);shown=['zero','one','two','three','four'][n] if op.get('as')=='word' else str(n)
   else:raise ValueError(op)
   assert shown==needle,(ident,shown,needle);assert text.count(needle)==1,(ident,needle)
   path=SOURCE_FILES[source_key];binds.append(dict(kind=kind,offset=text.index(needle),literal=needle,source=path,source_sha256=sha((ROOT/path).read_bytes()),pointer=pointer,raw_value=raw,display_operation=op))
  contexts.append(dict(id=ident,file='main',text=text,bindings=binds))
 title='When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits'
 replace('Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits',title,'title')
 oldabstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',s,re.S).group(1)
 original_percent_sentence='At the shorter horizon, long-history FX regression lowers matched loss by 14.8\\% and 16.6\\% in the previously reported later and earlier windows.'
 assert original_percent_sentence in oldabstract
 abstract=('Peak-position limits concern the largest absolute inventory reached before a review ends, making completed path labels and the observed current position central to forecasting. '
 'We compare historical and conditional quantile reports for an FX market maker and weekly primary-dealer position aggregates, using matched histories and update schedules. '
 'Simple historical rules remain demanding benchmarks across frequencies, position categories and reference choices. '+original_percent_sentence+' '
 'A post hoc history-to-horizon coordinate organizes simulation gains, and a new simulation passes its short-history and long-history prediction screens. '
 'Real-record learning curves partly support the predicted first cutpoints, while left censoring, large-history reversals and failures of universal simplification qualify that pattern. '
 'For limit managers, these findings motivate matching historical information before assessing conditional forecasts jointly on score, breaches and stability, with history length guiding evaluation.')
 replace(oldabstract,abstract,'abstract')
 paragraph("A dealer's recorded net position can finish",r"An inventory limit can look adequate at the horizon endpoint even when a dealer's position has crossed it earlier in the review period. Figure~\ref{fig:example} shows why the relevant forecast is a sampled path maximum rather than an endpoint interval. The challenge is to learn that peak from completed historical labels while preserving the information available when the position is observed. We ask when additional conditioning improves on historical headroom forecasts that use the same training history, and how longer histories alter that comparison.",'intro-first')
 old='We examine these competing effects through matched histories, alternative reference rules, and repeated chronological comparisons.'
 new=old+'\n\nTraining-history length provides an organizing question for the comparisons, with the proposed explanation tested rather than imposed on every favorable and adverse result. A post hoc coordinate comparison motivates predictions for a new simulation grid and fixed-period FX learning curves under unchanged validation and evaluation clocks. The resulting support is partial: the broad simulated loss pattern survives, while universal simplification fails and the financial curves show censoring and reversals. This evidence guides history-sensitivity validation without identifying a unique estimation-cost channel or a permanent sample-size threshold.'
 replace(old,new,'intro-central-claim')
 paragraph(r'\textbf{C2.}',r'\textbf{C2.} We find that horizon-adjusted training history organizes conditional peak-forecast gains, with partial support from a new simulation grid and retrospective learning curves. We compare the same peak target for one FX record and thirteen weekly position-category aggregates with matched histories and update schedules. Even after extending the regression penalty menu, historical rules win in 34 of 48 additional-panel comparisons. The new simulations satisfy their short-history and long-history criteria, while the predicted universal advantage of the smaller regression fails in the comparable cells. Where Duffie et al. (2023) examine capacity, illiquidity and PnL quantiles, and Wisniewski et al. (2020) forecast one market maker\'s endpoints, we compare these peak-position tasks. Section~\ref{sec:results} and Figure~\ref{fig:mechanism} connect that contrast to post hoc first cutpoints, left censoring and long-history reversals, guiding matched history-sensitivity validation.'.replace("market maker\\'s","market maker's"),'C2')
 paragraph('Quantile estimation and evaluation supply established tools',r'Quantile estimation and evaluation supply established tools for comparing conditional peak forecasts against historical rules on a shared response. Regression quantiles target asymmetric forecast errors, providing the basic statistical building block for the proposed conditional reports \citep{koenker1978}. Conditional autoregressive quantiles and quantile forests offer additional conditioning structures for forecasting applications that differ in response, predictors and estimation \citep{engle2004,meinshausen2006}. Learning-curve research documents diverse and sometimes nonmonotone relationships between training size and predictive performance across methods and data conditions \citep{viering2023}. Our fixed-period curves compare relative loss against a historical reference that also changes with training history, differing from an independent-sample expected-risk curve. Consistent scoring tools explain ranking differences across evaluation questions \citep{gneiting2011,ehm2016}; Table~\ref{tab:literature} locates the shared peak target, mature labels and matched reference design.','learning-literature')
 old='Their tests and the writing-stage HAC comparisons remain descriptive rather than independent or prospective confirmation.'
 replace(old,'These earlier tests and the writing-stage HAC comparisons remain descriptive rather than independent or prospective confirmation.','earlier-transparency-scope')
 clock=sources['clock'];w=clock['run_order'][0][1]
 transparency=(r'The history-coordinate comparison is a post hoc discovery on an existing simulation grid. We recorded the subsequent simulation equations, random streams, classification criteria and financial crossing predictions before running their new calculations, with local design commits and chronology available in the repository. This is a pre-run specification within an already examined research program, not a public external registration or an untouched financial holdout. The new simulations change innovation laws and random streams, whereas the FX learning curve reuses the known validation and evaluation period.'+'\n\n'+
 r'Every history shares the original validation segment and evaluation start, with complete mature-label pools and the original update convention; unavailable cases would remain NA. Both W'+str(w)+r' cases exactly reproduced all available old scientific arrays, summary fields and parameter selections before other histories were attempted. Some older parsimonious trace fields were absent, so their unavailable historical comparisons remain outside that claim. The bootstrap holds the selected coordinate fixed when resampling repetition clusters; its endpoint envelope conditions on that choice and the discovery grid. The new paired-loss diagnostics use the original Bartlett HAC convention with a normal reference and no family adjustment, treating financial dependence conditions as working premises.')
 anchor='The Supplement provides the complete prior and later comparison inventories'
 pos=s.index(anchor);s=s[:pos]+transparency+'\n\n'+s[pos:];changes.append(dict(id='new-transparency',before='',after=transparency));bound('new-transparency',transparency,[(str(w),'clock','/run_order/0/1',{'type':'exact'},'digit')])
 p1=sources['wp2']['P1'];p2=sources['wp2']['P2'];p3=sources['wp2']['P3'];rfull=format(sources['wp1']['methods']['QR33']['point']['r_star'],'.4g');rfour=format(sources['wp1']['methods']['QR4']['point']['r_star'],'.4g')
 discovery=(r'The post hoc selected coordinate is \(c=W/(H+1)\), a history-to-horizon proxy that omits coefficient count and differs from estimated effective sample size. On the discovery grid, the original regression\'s first cutpoint is '+rfull+', whereas the smaller regression\'s first cutpoint is '+rfour+r'. Both endpoint envelopes are wide and condition on the selected coordinate and grid, with multiple crossings appearing for the smaller regression. These descriptions make history sensitivity a candidate explanation to test against new procedures and data conditions, rather than a general threshold rule.').replace("regression\\'s","regression's")
 confirmation=('The new simulation grid satisfies its prespecified short-history and long-history prediction screens across the pooled cases and reported method and process subgroups. The short-history criterion is met in '+str(p1['successes'])+' of '+str(p1['denominator'])+' applicable cells, while the applicable regions remain fixed from each method\'s discovery cutpoint. The long-history criterion is met in '+str(p2['successes'])+' of '+str(p2['denominator'])+' applicable cells, supporting the loss pattern for these procedures under the new innovation laws. The universal simplification criterion holds in '+str(p3['successes'])+' of '+str(p3['denominator'])+' paired cells, so its all-cell prediction fails and the counterexamples remain part of the finding. Candidate records and every contrary cell appear together in the Supplement, giving the screen its complete comparison denominator and procedural scope.')
 financial=('The fixed-period FX learning curves yield partly supportive first-cutpoint evidence while exposing reversals that a single history comparison would miss. Identified crossings lie within their prespecified bands, but the shorter-horizon smaller regression is already below the historical rule at the smallest history. The compatible left-censored case remains untestable as a first-cutpoint prediction, rather than supplying another identified crossing for the overall confirmation rule. At the largest history, both longer-horizon regressions lose again against their own matched historical rule, making the relative-loss relationship visibly nonmonotone. The Supplement reports every history, breach count and nominal paired-loss diagnostic, alongside the complete prediction assessment for the specified grid.')
 processes=(r'The confirmation processes use Student innovations, Markov volatility switching and compound-Poisson jumps to probe the history pattern under changed innovation distributions. Simple switching and jump constructions have mature financial precedents, while these experiments remain discrete mean-reverting level models with their own specified equations \citep{turner1989,merton1976}. The complete menus and chronological selection rules stay fixed, preserving the comparison between the implemented procedures rather than asserting an oracle-risk decomposition.')
 add='\\subsection{History-length patterns and their limits}\n\n'+discovery+'\n\n'+processes+'\n\n'+confirmation+'\n\n'+financial+'\n\n'
 anchor=r'\begin{figure}[htbp]\centering\includegraphics[width=.98\linewidth]{figures/v9-unified-history.pdf}'
 assert s.count(anchor)==1;s=s.replace(anchor,add+anchor)
 bound('discovery-coordinate-and-cutpoints',discovery,[('W/(H+1)','coordinate','/candidate_metrics/c',{'type':'exact'},'numeric_fragment'),(rfull,'wp1','/methods/QR33/point/r_star',{'type':'format','spec':'.4g'},'digit'),(rfour,'wp1','/methods/QR4/point/r_star',{'type':'format','spec':'.4g'},'digit')])
 # Bind each original integer occurrence independently, even when denominators repeat.
 for part,tag in [('P1','The short-history criterion'),('P2','The long-history criterion'),('P3','The universal simplification criterion')]:
  start=confirmation.index(tag);end=confirmation.index('.',start)+1;text=confirmation[start:end];row=sources['wp2'][part]
  bound('confirmation-'+part,text,[(str(row['successes']),'wp2','/'+part+'/successes',{'type':'exact'},'digit'),(str(row['denominator']),'wp2','/'+part+'/denominator',{'type':'exact'},'digit')])
 caption=re.search(r'\\caption\{Conditional-regression loss.*?\\label\{fig:mechanism\}',s,re.S).group()
 revised=caption.replace("post hoc 90\\% first-cutpoint envelopes","post hoc first-cutpoint envelopes").replace('Three identified FX cutpoints are consistent with their prespecified intervals, while the remaining case stays untestable through left censoring.','Of the FX curve predictions, three identified cutpoints agree with their prespecified intervals, while the remaining case stays untestable through left censoring.').replace('Repeated FX cells use the same study period, so these comparisons support a partial, nonmonotone history-length pattern.','Repeated FX cells use the same period, and crossing estimates interpolate raw history; these comparisons support a partial, nonmonotone history-length pattern.')
 replace(caption,revised,'unified-caption-provenance')
 bound('unified-caption',revised,[('W/(H+1)','coordinate','/candidate_metrics/c',{'type':'exact'},'numeric_fragment'),('three','curves','',{'type':'count_eq','field':'/prediction_status','equals':'FIRST_CUTPOINT_CONSISTENT','as':'word'},'word')])
 practical='A practical history screen is to examine the entire matched-loss curve around the available history and verify its breach behavior and temporal stability. The coordinate and its cutpoints can organize that investigation, but left censoring and later reversals require testing the actual reporting configuration. Treat a favorable region as a candidate for further validation rather than a permanent minimum-sample rule or an empirically measured sample-per-parameter threshold.'
 anchor=r'\begin{table}[htbp]\centering\small'+'\n'+r'\caption{Observed comparison settings and validation questions.'
 assert s.count(anchor)==1;s=s.replace(anchor,practical+'\n\n'+anchor);changes.append(dict(id='decision-rule',before='',after=practical))
 old='A winning score leaves breach behavior and operating suitability to be assessed.';replace(old,'The map guides history-sensitivity checks alongside breach behavior and operating suitability.','map-caption')
 newlim='The history coordinate is descriptive, with parameter count absent from the selected index and dependence beyond the response horizon left unmeasured. Different penalty menus and approximation errors move together with predictor count, so the comparison does not isolate an estimation-cost channel. The new simulation\'s specified loss-pattern screens are met, while universal simplification fails and the financial grid supplies partial first-cutpoint consistency. Wide post hoc endpoint envelopes and left censoring limit threshold precision, while the longest-history reversals contradict a permanent operating cutoff. Weekly grids lack a dedicated broad-history learning curve, and some exceed the smaller model\'s point cutpoint without uniformly winning.'
 anchor='The later analyses and working-reference tests describe'
 pos=s.index(anchor);s=s[:pos]+newlim+'\n\n'+s[pos:];changes.append(dict(id='mechanism-limitations',before='',after=newlim))
 paragraph('Simple historical rules are strong competitors for predicting',"Historical rules remain demanding competitors for sampled peak-position quantiles, with conditional gains depending on the reference, training history and forecast horizon. The post hoc history-to-horizon coordinate organizes the original simulations, and the new simulation grid supports its specified short-history and long-history loss patterns. Retrospective FX curves provide partial first-cutpoint consistency, while left censoring, long-history reversals and failed universal simplification qualify a single-threshold interpretation. The controlled study's earlier narrow-regime explanation still fails, so the history pattern adds a bounded organizing description rather than replacing contrary evidence. These results motivate validation at the actual history and reference, combining score, breach frequency and stability before a limit manager adopts additional conditioning.",'conclusion-first')
 s=s.replace('\\FloatBarrier\n\n\\section{Implications for model validation}', 'Historical comparisons remain reference-sensitive, and history length supplies a useful but incomplete guide to the gains from additional conditioning.\n\n'+'\\FloatBarrier\n\n\\section{Implications for model validation}')
 # This revision updates the availability description only; author-provided fields stay exact.
 old='This revision adds three design-frozen exploratory extensions: a controlled simulation, a same-dealer daily aggregation contrast and an expanded inspected backcast.'
 new='The earlier controlled grid, same-dealer daily contrast and overlapping backcast remain complete. This revision adds the post hoc coordinate comparison, pre-run simulation screen and fixed-period financial learning curve, with all counterexamples and unavailable prediction statuses visible.'
 replace(old,new,'availability-current')
 bibliography=r'''
\bibitem[Merton(1976)]{merton1976} Merton, R. C. (1976). Option pricing when underlying stock returns are discontinuous. \emph{Journal of Financial Economics}, \emph{3}(1--2), 125--144. \url{https://doi.org/10.1016/0304-405X(76)90022-2}.

\bibitem[Turner et al.(1989)]{turner1989} Turner, C. M., Startz, R., \& Nelson, C. R. (1989). A Markov model of heteroskedasticity, risk, and learning in the stock market. \emph{Journal of Financial Economics}, \emph{25}(1), 3--22. \url{https://doi.org/10.1016/0304-405X(89)90094-9}.

\bibitem[Viering \& Loog(2023)]{viering2023} Viering, T., \& Loog, M. (2023). The shape of learning curves: A review. \emph{IEEE Transactions on Pattern Analysis and Machine Intelligence}, \emph{45}(6), 7799--7819. \url{https://doi.org/10.1109/TPAMI.2022.3220744}.

'''
 s=s.replace(r'\end{thebibliography}',bibliography+r'\end{thebibliography}')
 # Original scientific table numeric vectors and display equations must survive unchanged.
 tables=lambda x:{re.search(r'\\label\{(tab:[^}]+)\}',t).group(1):re.findall(r'[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?',t) for t in re.findall(r'\\begin\{table\}.*?\\end\{table\}',x,re.S)}
 assert tables(original)==tables(s)
 assert re.findall(r'\\\[.*?\\\]',original,re.S)==re.findall(r'\\\[.*?\\\]',s,re.S)
 before_author=original.split(r'\section*{Author-provided information}',1)[1].split(r'\begin{thebibliography}',1)[0]
 assert before_author==s.split(r'\section*{Author-provided information}',1)[1].split(r'\begin{thebibliography}',1)[0]
 (ROOT/'submission-jof/manuscript.tex').write_text(s)
 figure='submission-jof/figures/v9-unified-history.pdf';source='results/revision-v9/wp4/render-v5/unified-history.pdf'
 fg={'path':figure,'source':source,'sha256':sha((ROOT/figure).read_bytes())}
 for name,path in [('placement','notes/revision-v9/wp4-final-placement-v5.json'),('point_audit','notes/revision-v9/wp4-independent-audit.json'),('visual_receipt','notes/revision-v9/wp4-visual-QA.json')]:fg[name]={'source':path,'sha256':sha((ROOT/path).read_bytes())}
 binding=dict(schema='v9-main-context-bindings-1',contexts=contexts,figures=[fg],scope='Additive exact-located new numeric occurrences only; unchanged v8 guard owns all inherited source, table and mathematical evidence')
 with (ROOT/'notes/revision-v9/wp5-main-context-bindings.json').open('x') as f:json.dump(binding,f,indent=2);f.write('\n')
 with (ROOT/'notes/revision-v9/wp5-prose-before-after.json').open('x') as f:json.dump(dict(source_commit=BASE,source_before_sha256=sha(before),current_main_sha256=sha(s.encode()),title=title,changes=changes,abstract_before=oldabstract,abstract_after=abstract,scientific_old_table_vectors_unchanged=True,original_display_equations_unchanged=True,author_fields_unchanged=True),f,indent=2);f.write('\n')
 print(json.dumps(dict(status='PROSE_GENERATED_PENDING_GATES',changes=len(changes),new_numeric_contexts=len(contexts),new_numeric_bindings=sum(len(c['bindings']) for c in contexts),old_table_vectors_unchanged=True,old_display_equations_unchanged=True,author_fields_unchanged=True),indent=2))
if __name__=='__main__':main()
