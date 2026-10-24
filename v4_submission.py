"""Journal package assembly: immutable numerical sources, no forecast estimation."""
from pathlib import Path
from copy import deepcopy
import csv, hashlib, html, io, json, re, shutil, zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'submission-jof'
NOTE=ROOT/'notes/revision-v4-jof'
TITLE='Forecasting Sampled Net-Position Peaks: Historical Rules, Conditional Quantiles and Validation'
ALTERNATES=['Accuracy and Calibration of Sampled Position-Peak Forecasts across FX and Treasury Tasks',
'When Conditional Quantiles Improve Position-Peak Forecasts: A Retrospective Model-Validation Study']
V3='manuscript/revision-v3/paper-content.json'
MAIN='manuscript/working-paper/paper-content.json'
PAIRS='results/revision-20261022/paired-comparisons.csv'
DM='results/revision-20261023/inference/dm.csv'
COV='results/revision-20261023/inference/coverage.csv'
HOLM='results/revision-20261023/inference/holm.csv'
IDS=['fx_hourly-h6-QR2880-minus-rolling_F720','fx_hourly-h6-QR2880-minus-frozen_F2880','nyfed_weekly-h6-QR260-minus-frozen_F260','fx_hourly-h24-QR2880-minus-rolling_S720']

def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def plain(s):return html.unescape(re.sub('<[^>]*>','',str(s)))
def rows(path):return list(csv.DictReader((ROOT/path).open()))
def p(s):return {'type':'p','html':s,'_definition':'Author synthesis; contains no new numerical empirical claim'}
def sub(s):return {'type':'subheading','text':s,'_definition':'Structural heading'}
def clean(s):
 s=s.replace('establishes','supports').replace('establish ','support ').replace('demonstrates','indicates').replace('demonstrate ','show ')
 s=s.replace('issue origin','forecast origin').replace('issue origins','forecast origins').replace('completed-label pool','mature training-outcome pool')
 s=s.replace('native peaks','historical peaks').replace('native peak','historical peak').replace('reanchored increments','translated increments')
 s=s.replace('Mean positive overrun','Mean underprediction amount').replace('mean overrun / unused allowance','mean underprediction / overprediction').replace('overrun and unused-allowance','underprediction and overprediction').replace('unused quantity','overprediction amount').replace('overrun / unused-allowance','underprediction / overprediction')
 s=s.replace('mean positive overrun','mean underprediction amount').replace('mean unused allowance','mean overprediction amount')
 s=s.replace('small total net gain','summed forecast-score reduction').replace('H6 primary net gain','H6 primary forecast-score reduction').replace('H6 net gain','H6 forecast-score reduction')
 return s

def joint_table():
 pp={r['contrast_id']:r for r in rows(PAIRS)};dd={r['contrast_id']:r for r in rows(DM)};hh={r['contrast_id']:r for r in rows(HOLM)};cc=rows(COV)
 result=[];bind=[]
 names=['FX original primary','FX matched control','Treasury primary','FX legacy sensitivity']
 for name,ident in zip(names,IDS):
  r=pp[ident];d=dd[ident]
  def cov(method,win):return next(x for x in cc if x['source']==r['source'] and x['horizon']==r['horizon'] and x['method']==method and x['window']==win)
  a=cov(r['left_method'],r['left_window']);b=cov(r['right_method'],r['right_window'])
  f=lambda v:f'{float(v):.3g}'
  result.append([name,f"{float(r['relative_mean_loss_difference_percent']):+.2f}",f(d['dm_p']),f(d['hln_p']),f(hh[ident]['holm_p']) if ident in hh else 'Outside family',
      f"{100*int(r['strict_breach_count_left'])/int(r['origin_count']):.3f} / {100*int(r['strict_breach_count_right'])/int(r['origin_count']):.3f}",f(a['pof_p'])+' / '+f(b['pof_p'])])
  bind.append({'contrast_id':ident,'paired':PAIRS,'dm':DM,'holm':HOLM,'coverage':COV,'coverage_left':{'source':a['source'],'horizon':a['horizon'],'window':a['window'],'method':a['method']},'coverage_right':{'source':b['source'],'horizon':b['horizon'],'window':b['window'],'method':b['method']}})
 return {'type':'table','caption':'Table 3†. Fixed paired comparisons. Loss change uses all forecast origins; breach-rate columns are left/reference percentages on those same origins. Kupiec p uses the fixed sparse grid instead, with its denominators reported in Table 4. The matched FX control is separate from the original primary. Outside family means no Holm value is assigned.',
 'headers':['Comparison','Loss Δ%','DM p','HLN p','Holm p','Breach % L/R','Kupiec p L/R'],'rows':result,
 '_generator':'joint_table','_bindings':bind}

def compose(write_outputs=True):
 c=json.loads((NOTE/'scientific-port.json').read_text());src=deepcopy(c)
 # Correct symbols from the old-main prose while preserving v3's mathematical notation.
 for s in c['sections']:
  for b in s['blocks']:
   for key in ('html','caption','text'):
    if key in b:b[key]=clean(b[key])
 b=c['sections'][10]['blocks'][24]
 b['html']=b['html'].replace('c and phi','c and φ').replace('epsilon(s)=N(s+1)−c−phi N(s)','ε<sub>s</sub>=N<sub>s+1</sub>−c−φN<sub>s</sub>').replace('raw translation by W','raw translation by Ñ<super>tr</super>')
 c['sections'][3]['blocks'][12]['html']=c['sections'][3]['blocks'][12]['html'].replace('lambda','λ').replace('tau','τ')
 c['sections'][12]['blocks'][3]['html']=c['sections'][12]['blocks'][3]['html'].replace('rho','ρ').replace('real tau','real τ')
 c['sections'][14]['blocks'][3]['html']=c['sections'][14]['blocks'][3]['html'].replace('is preferable for every nonnegative linear weighting','gives weak improvement for every constant nonnegative linear weighting')
 # Tables and references get stable new identifiers. All original tables are retained.
 tablemap={};aux=[]
 for si,s in enumerate(c['sections']):
  for bi,b in enumerate(s['blocks']):
   if b['type']=='table':
    match=re.match(r'Table\s+([A-L]?\d+)\.',b['caption'])
    if si==2 and bi==3:new='1'
    elif si==7 and bi==8:new='4'
    else:
     aux.append((si,bi));new=f'S{len(aux)}'
    if match:tablemap[match[1]]=new
    b['caption']=re.sub(r'^Table\s+[A-L]?\d+\.', 'Table '+new+('†' if si==7 or si>=13 else '')+'.',b['caption']) if match else 'Table '+new+'. '+b['caption']
 # Supplement section labels replace prior appendix labels, before numerical validation.
 smap={chr(65+i):f'S{i+2}' for i in range(12)}
 def remap(text):
  text=re.sub(r'Appendix ([A-L])\b',lambda m:'Supplement '+smap[m[1]],text)
  text=re.sub(r'Table ([A-L]?\d+)\b',lambda m:'Table '+tablemap.get(m[1],m[1]),text)
  # Main port's original preference table/section references differ from v3.
  text=re.sub(r'(?<![A-Za-z])([ABC])\.(\d+)\b',lambda m:smap[m[1]]+'.'+m[2],text)
  text=text.replace('As in Section 9, the omitted','As in the finite-menu comparison, the omitted')
  text=text.replace('Section 8 fits a specified mean recursion','Supplement S7 fits a specified mean recursion')
  text=text.replace('Section 9 fits a specified mean recursion','Supplement S7 fits a specified mean recursion')
  return text
 for s in c['sections']:
  for b in s['blocks']:
   for key in ('html','caption','text'):
    if key in b:b[key]=remap(b[key]) if key!='caption' else b[key]
   if b.get('_source',{}).get('path')==MAIN and b.get('_source',{}).get('pointer')==['sections',8,'blocks',5]:b['html']=b['html'].replace('Table '+tablemap.get('6','6'),'Table '+tablemap['F4'])
   if b['type']=='subheading':b['text']=re.sub(r'^(Post-result\s*/?\s*exploratory|Post-result)\s*','',b['text'],flags=re.I).capitalize()
 # Rewrite introduction as questions; reuse archived results verbatim in their sections.
 intro=[c['sections'][0]['blocks'][0],p('This study evaluates established forecasting procedures for a measured financial path maximum. The response, information clock and known current-position floor distinguish the task from endpoint interval prediction. We organize the evidence around accuracy, scoring and calibration, and transport across financial measurement processes.'),
  sub('Research questions'),p('<b>RQ1 — Predictive accuracy.</b> Can conditional quantiles improve on historical peak rules when responses, mature training outcomes and update schedules are controlled? We retain the original source primaries and distinguish the matched-history control from the cross-window FX primary.'),
  p('<b>RQ2 — Scoring and calibration.</b> Does a lower quantile score coincide with fewer breaches or favorable rankings across consistent scores and hypothetical loss preferences? The principle of sharpness subject to calibration motivates reporting these dimensions separately (Gneiting, Balabdaoui and Raftery, 2007).'),
  p('<b>RQ3 — Transport and robustness.</b> Do conclusions survive parsimonious regression, other aggregate position tasks and mature conditional baselines? A classical maximal-inequality benchmark supplies a sharply qualified reference under independent symmetric increments.'),
  c['sections'][0]['blocks'][2],c['sections'][0]['blocks'][3],
  p('The next sections locate the empirical lineage, define the measurement and forecasting design, and answer the research questions. The separate Online Supplement retains every archived model cell, failed cell and mathematical or implementation qualification.')]
 methods_anchor_note=p('The historical controls also use current information: F and K incorporate the current magnitude, while S uses the signed current anchor. The comparison therefore concerns construction and estimation choices, not presence versus absence of the current observation.')
 c['sections'][3]['blocks'].append(methods_anchor_note)
 c['sections'][2]['blocks'].append({'type':'p','html':'Data sources: Lindsay (2020); Federal Reserve Bank of New York (2026).','_citation_ids':['dataset','nyfeddata']})
 # Definition numerals belong to question labels; bibliography years are bound to verified references later.
 transparency=p('The original conditional-study design and selected parameters were publicly frozen before their respective executions. The FX evaluation interval had already been inspected. Subsequent inference, AR replay, rank and preference analyses, parsimonious regression, maximal-inequality simulations, aggregate-panel extension and mature-baseline additions are post-result / exploratory. Local execution bindings do not create a new public preregistration. A dagger (†) marks these analyses in tables and figure captions; it applies throughout the Supplement. Equal-loss tests are working-reference diagnostics under their stated dependence and moment assumptions, not selection-adjusted confirmation. The full retrospective record and unsuccessful cells remain visible.')
 methods=deepcopy(c['sections'][3]);methods['title']='4. Target and forecasting methods';methods['blocks']=[b for b in methods['blocks'] if b['type']!='table']
 methods['blocks'].insert(0,p('A forecast origin is the record at which the report is issued. Mature training outcomes are completed future-path labels available by the latest scheduled refit. Fixed-at-refit (frozen) F holds that label pool between refits; per-origin (rolling) F refreshes it at each forecast origin. Both update the observed current anchor. Historical peaks use their original recorded positions; translated increments shift historical signed paths to the current position. Headroom is the nonnegative excess above the observed floor, the absolute current position. These are forecasting definitions, not cash-resource allocations.'))
 menu={'type':'table','caption':'Table 2. Method overview. Parameter menus and fitted choices are retained in Supplement Table '+tablemap['2']+'. All fitted methods use mature training outcomes; controls distinguish per-origin and fixed-at-refit updates.',
 'headers':['Method','Forecast definition','Parameter/menu reference'],
 'rows':[['F / S / K','Historical headroom / translated paths / floored historical peaks','Common history and refit controls'],['QR','Ridge quantile regression of normalized headroom','Validation penalty menu'],['KNN / scaled KNN','Local headroom quantile / local volatility-scaled quantile','Validation neighbor menu'],['I / AR†','Ordinary empirical rank / ordered-residual mean replay','Supplement S5 and S7'],['L†','Classical-bound endpoint plug-in plus observed floor','Proposition 1; Supplement S11'],['FHS / peak POT / QRF†','Filtered path simulation / scaled peak tail / leaf-distribution quantile','Supplement S13'] ],'_definition':'Qualitative method overview; names and mathematical definitions refer to archived methods'}
 methods['blocks'].insert(1,menu)
 evals=deepcopy(c['sections'][4]);evals['title']='5. Research design and transparency';evals['blocks']=[sub('Research design and transparency'),transparency]+[b for i,b in enumerate(evals['blocks']) if i not in (5,6,7)]
 fx=deepcopy(c['sections'][5]);fx['blocks']=[b for b in fx['blocks'] if b['type'] not in ('table','figure')]
 tre=deepcopy(c['sections'][6]);tre['blocks']=[b for b in tre['blocks'] if b['type'] not in ('table','figure')]
 accuracy={'title':'6. Predictive accuracy (RQ1)','blocks':[joint_table(),*fx['blocks'],*tre['blocks']]}
 # Keep calibration and frontier interpretation in main; full robustness outputs move to S1.
 r=c['sections'][7]
 scoring={'title':'7. Scoring and calibration (RQ2)','blocks':[r['blocks'][8],r['blocks'][9],r['blocks'][10],r['blocks'][25],r['blocks'][3],
 p('The fixed menu excludes the feasible floor-only report. Its endpoint winners are therefore menu comparisons, not global action optima. The actual Murphy diagrams cross for both original primaries. The full rank, horizon-coherence and e-value diagnostics are in Supplement S5; complete preference envelopes and selected-fit shrinkage readbacks are in Supplements S6–S7 and S10.') ]}
 transport={'title':'8. Transport and robustness (RQ3)','blocks':[r['blocks'][16],r['blocks'][18],r['blocks'][20],r['blocks'][23],r['blocks'][24],
 p('Complete baseline and panel tables, including all unsuccessful cells, are in Supplement S1 and Supplements S12–S13. The original positive-increment simulation and corrected mean-reverting level and negative-increment cases are all retained in Supplement S11. None supplies independent unseen-dealer validation.') ]}
 discussion=deepcopy(c['sections'][8]);discussion['title']='9. Interpretation and limitations';discussion['blocks']=[b for i,b in enumerate(discussion['blocks']) if i not in (0,4,5)]
 # Conclusion answers the same questions and preserves every adverse conclusion.
 conclusion={'title':'10. Conclusion','blocks':[p('<b>RQ1.</b> Conditional regression improves the inspected FX short-horizon score but the separately fitted Treasury regression primary deteriorates. The original comparisons and matched controls answer distinct procedural questions.'),
 c['sections'][9]['blocks'][0],p('<b>RQ2.</b> More frequent breaches can accompany lower mean quantile loss. Crossed elementary-score diagrams and the finite-menu preference analysis prevent interpreting a stipulated-score gain as uniform tail-risk improvement.'),
 p('<b>RQ3.</b> Parsimonious regression, related aggregate tasks and mature baselines produce mixed and frequently adverse outcomes. These extensions strengthen the model-validation evidence while leaving compatible new dealer observations and a prospective public-release exercise uncompleted.'),*c['sections'][9]['blocks'][1:]]}
 # Remaining original main material, including every original table, is retained once in S1.
 selected_sources={(b['_source']['path'],tuple(b['_source']['pointer'])) for s in [*([{'blocks':intro}]),c['sections'][1],c['sections'][2],methods,evals,accuracy,scoring,transport,discussion,conclusion] for b in s['blocks'] if '_source' in b}
 auxblocks=[]
 for si,s in enumerate(c['sections'][:10]):
  candidates=[b for bi,b in enumerate(s['blocks']) if not (si==0 and bi==4) and b['type'] not in ('figure','subheading') and '_source' in b and (b['_source']['path'],tuple(b['_source']['pointer'])) not in selected_sources]
  if candidates:auxblocks += [sub(re.sub(r'^\d+\. ','',s['title']))]+candidates
 supplement=[{'title':'S1. Complete report menus and robustness outputs','blocks':auxblocks}]
 for i,s in enumerate(c['sections'][10:]):
  s=deepcopy(s);s['title']=f'S{i+2}. '+re.sub(r'^Appendix [A-L]\. ','',s['title']);s['title']=re.sub(r'(Post-result\s*/\s*exploratory|exploratory|post-result)\s*','',s['title'],flags=re.I)
  supplement.append(s)
 # Capture modern data/code statements. No author declaration is inferred.
 declarations={'title':'Declarations and availability','blocks':[
 p('Data availability. The FX inputs are available from the original Kaggle source, Net Position Time Series Dataset. The repository provides acquisition instructions and source fingerprints; redistribution is not assumed. Treasury measurements are from New York Fed Primary Dealer Statistics. © Federal Reserve Bank of New York. Content is subject to the New York Fed Terms of Use. Both datasets retain their source-measurement and vintage limitations.'),
 p("Code availability. Reproduction code, archived aggregate results and this revision are available at <a href='https://github.com/ByronLi0207/financial-mathematics-paper-20261020'>the study repository</a>. Private raw FX observations and private per-origin forecast traces are not redistributed."),
 p('Author information and ORCID: [TO BE COMPLETED BY AUTHOR].'),p('Funding: [TO BE COMPLETED BY AUTHOR].'),p('Conflict of interest: [TO BE COMPLETED BY AUTHOR].'),p('AI-use disclosure: [TO BE COMPLETED BY AUTHOR].')]}
 main={'title':TITLE,'subtitle':'Retrospective forecasting evaluation and model validation','date':'','abstract':clean(c['abstract']).replace('These retrospective comparisons support source-, horizon-, history- and family-dependent rankings, without coverage guarantees or observed trading and funding benefits.','Within these inspected archives, rankings vary across sources, horizons, history lengths and model families. Related aggregate tasks and mature baselines yield mixed and adverse outcomes, with incomplete cells retained. No coverage guarantee or trading or funding benefit is inferred.'),
 '_abstract_source':c['_abstract_source'],'sections':[{'title':'1. Introduction','blocks':intro},c['sections'][1],c['sections'][2],methods,evals,accuracy,scoring,transport,discussion,conclusion,declarations],
 'references':c['references'],'figures':[]}
 # Main has four vector figures; all old figures also remain available in the Supplement.
 for i,old in enumerate([0,3,4,2]):
  f=deepcopy(c['figures'][old]);f['path']='figures/'+Path(f['path']).name
  f['caption']=re.sub(r'^Figure [\da-z]+\.',f'Figure {i+1}'+('†' if old in (3,4) else '')+'.',clean(f['caption']))
  f['_source']={'path':V3,'pointer':['figures',old],'sha256':hashlib.sha256((ROOT/V3).read_bytes()).hexdigest()}
  main['figures'].append(f)
 main['sections'][5]['blocks'].append({'type':'figure','index':0,'_definition':'Structural figure placement'})
 main['sections'][6]['blocks'] += [{'type':'figure','index':1,'_definition':'Structural figure placement'},{'type':'figure','index':2,'_definition':'Structural figure placement'}]
 main['sections'][7]['blocks'].append({'type':'figure','index':3,'_definition':'Structural figure placement'})
 sf=[]
 for i,f in enumerate(c['figures']):
  f=deepcopy(f);f['_source']={'path':V3,'pointer':['figures',i],'sha256':hashlib.sha256((ROOT/V3).read_bytes()).hexdigest()};f['caption']=re.sub(r'^Figure [\da-z]+\.',f'Figure S{i+1}'+('†' if i in (3,4) else '')+'.',clean(f['caption']));sf.append(f)
 supplement[0]['blocks'].append(p('The annual decomposition is a readback of published aggregates. Year-specific paired mean differences are weighted by their origin counts before computing contribution shares; annual percentage improvements are not averaged. Exact rational arithmetic operates on saved decimal tokens and does not recover infinite-precision original individual losses. The archived annual-decomposition receipt and helper retain source hashes, reconciliation tolerances and observed differences.'))
 supplement.append({'title':'S14. Additional archived vector figures','blocks':[{'type':'figure','index':i,'_definition':'Structural figure placement'} for i in range(len(sf))]})
 supp={'title':'Online Supplement: '+TITLE,'subtitle':'Detailed constructions, full outputs and diagnostics; † denotes later analyses','date':'','abstract':'','sections':supplement,'references':c['references'],'figures':sf}
 # Fix old figure numbering in adopted annual prose and old main routing text.
 for d in (main,supp):
  for s in d['sections']:
   for b in s['blocks']:
    if b['type']=='p':
     b['html']=b['html'].replace('Figure 3 shows the issue-year contrasts','Figure 4 shows the issue-year contrasts').replace('Figure 3 presents all issue-year groups','Figure 4 presents all issue-year groups').replace('Figure 3 displays every original annual primary comparison','Figure 4 displays every original annual primary comparison').replace('Figure 2 juxtaposes','Supplement Figure S2 juxtaposes').replace('Figure 3 retains the complete annual comparison','main-text Figure 4 retains the complete annual comparison').replace('Figure 2 separates','Supplement Figure S2 separates').replace('Figure 2 displays','Supplement Figure S2 displays').replace('Figure 4 fixes τ','Figures 2 and 3 fix τ').replace('and varies the elementary-score','and vary the elementary-score')
     b['html']=re.sub(r'All adverse cells remain in Table \S+\.', 'All adverse cells remain in the complete Supplement tables.',b['html'])
  # Conservative keep all currently cited references; reference agent will resolve metadata.
  audit=NOTE/'reference-audit.json'
  if audit.exists():
   a=json.loads(audit.read_text()); entries=a.get('references',a.get('entries',[]))
   for ref in d['references']:
    rec=next((x for x in entries if x.get('id')==ref['id']),None)
    if rec and rec.get('suggested_html'):ref['html']=rec['suggested_html']
  main['references']=[r for r in main['references'] if r['id'] not in {'boyd2011','casgrain2023','henzi2022','politis1994'}]
  supp['references']=[r for r in supp['references'] if r['id'] in {'barone1999','boyd2011','casgrain2023','christ1998','gneiting2011','henzi2022','hull1998','mcneilfrey2000','politis1994'}]
  # Reference selection is based on author/year presence across both outputs, not arbitrary index deletion.
 if write_outputs:
  dump(OUT/'manuscript-content.json',main);dump(OUT/'supplement-content.json',supp)
  dump(NOTE/'routing.json',{'table_map':tablemap,'supplement_sections':smap,'selected_title':TITLE,'alternate_titles':ALTERNATES,'all_v3_table_count':sum(b['type']=='table' for s in src['sections'] for b in s['blocks'])})
 return main,supp

if __name__=='__main__':
 compose();print('Content composed from immutable v3 and merged-main blocks; no models fitted.')
