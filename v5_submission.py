"""V5 authoring from a frozen v4 text and context-bound saved numerical outputs.

No original result is replaced. New computation remains explicitly exploratory.
"""
from copy import deepcopy
from pathlib import Path
import csv,hashlib,html,json,re
from decimal import Decimal
from v4_submission import ROOT,OUT,dump,plain,p,sub,PAIRS,DM,HOLM,IDS
NOTE=ROOT/'notes/revision-v5-novelty'
RES='results/revision-20261023/v5-novelty/'
BASE='notes/revision-v5-novelty/v4-manuscript-before.json'
SUPP='notes/revision-v5-novelty/v4-supplement-before.json'
TITLE='Forecasting Peak Net Positions: Known Floors, Endpoint-to-Peak Bounds and Score–Coverage Disagreement'
ALTERNATES=['When Do Conditional Quantiles Beat Historical Rules for Sampled Position Peaks?',
'Accuracy, Calibration and Transport of Dealer Position-Peak Forecasts']

def read(path):return json.loads((ROOT/path).read_text())
def row(path,ident):return next(r for r in csv.DictReader((ROOT/path).open()) if r['contrast_id']==ident)
def fp(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def binding(paths):return [{'path':s,'sha256':fp(s)} for s in sorted(set(paths))]
def fmt(x,n=2,sign=False):
 s=f'{Decimal(str(x)):{"+" if sign else ""},.{n}f}';return s.replace('-','−')
def btext(text):return {'type':'p','html':text}
def get_table(doc,prefix):return next(b for s in doc['sections'] for b in s['blocks'] if b['type']=='table' and b['caption'].startswith(prefix))
def _generate(key):
 g=read(RES+'gain-decomposition.json');fx=row(PAIRS,IDS[0]);ma=row(PAIRS,IDS[1]);tr=row(PAIRS,IDS[2])
 supp=read(SUPP);co=get_table(supp,'Table S15');cr=next(r for r in co['rows'] if r[:3]==['FX','720','QR'])
 pa=get_table(supp,'Table S9');wins=[sum(int(r[j].split('/')[0]) for r in pa['rows']) for j in (1,2,3)];cells=sum(int(r[1].split('/')[1]) for r in pa['rows'])
 t=read(RES+'motivating-window-final.json');ex=t['example']
 allpaths=[RES+'gain-decomposition.json',PAIRS,SUPP,DM,HOLM,RES+'motivating-window-final.json']
 if key=='gain_table':
  b={'type':'table','caption':'Table 5†. Exact additive FX primary bridge from saved decimal mean losses. Every percentage-point entry uses the original rolling-F loss as denominator. The middle contrast changes the full conditional procedure; it is not a pure estimator or causal effect.','headers':['Bridge contrast','Mean-loss change (USD)','% of original reference'],
  'rows':[['Rolling F W720 → frozen F W2880',fmt(g['length_update_difference_native'],5,True),fmt(g['length_update_difference_percent_original_reference'],4,True)],['Frozen F W2880 → QR W2880',fmt(g['estimator_difference_native'],5,True),fmt(g['estimator_difference_percent_original_reference'],4,True)],['Original primary total',fmt(g['total_difference_native'],5,True),fmt(g['total_difference_percent_original_reference'],4,True)]]}
 elif key in ('gain_text','gain_text_supp'):
  b=btext(f'Table 5 expresses the original FX primary gain as an exact descriptive bridge: the joint history/update contrast adds {fmt(g["length_update_difference_percent_original_reference"],4,True)} percentage points, and the conditional-procedure contrast adds {fmt(g["estimator_difference_percent_original_reference"],4,True)}, using the same original-reference denominator. Their sum is {fmt(g["total_difference_percent_original_reference"],4,True)}%. The separate matched-reference percentage is {fmt(g["estimator_difference_percent_matched_reference"],4,True)}%; adding it to the first bridge entry would mix denominators. History length and update frequency change together in the first step; features, estimation and procedure change in the second. This post-result / exploratory arithmetic identifies no isolated causal effect.')
  if key=='gain_text_supp':b['html']=b['html'].replace('Table 5','main-article Table 5')
 elif key in ('leakage_table','leakage_text'):
  a=read(RES+'label-maturity-fx_hourly.json');bny=read(RES+'label-maturity-nyfed_weekly.json');allpaths += [RES+'label-maturity-fx_hourly.json',RES+'label-maturity-nyfed_weekly.json']
  if key=='leakage_table':
   rr=[]
   for name,d in [('FX',a),('Treasury',bny)]:
    for r in d['rows']:
     c,o=r['clean'],r['oracle_leakage'];rr.append([name,r['method'],fmt(c['mean_pinball'],6),fmt(o['mean_pinball'],6),fmt(r['illegal_minus_clean_percent'],6,True),f"{c['strict_breach_count']} / {o['strict_breach_count']}"])
   b={'type':'table','caption':f"Table S37†. Deliberately immature-label oracle versus clean training on the first, middle and last complete original refit blocks. FX has {a['origin_count']} origins and Treasury {bny['origin_count']}; each refit adds {a['per_refit_immature_label_count']} illegal labels. Source units are USD for FX and USD millions for Treasury. The oracle-minus-clean percentage has the clean loss as denominator. These are selected clock blocks, not the full evaluation sample; the oracle is not deployable.", 'headers':['Source','Method','Clean loss','Illegal loss','Illegal Δ%','Breaches C/O'],'rows':rr}
  else:
   b=btext(f'A deliberately invalid label-timing control retains the original selected parameters, long history and refit clock on predetermined first, middle and last complete blocks: {a["origin_count"]} FX origins and {bny["origin_count"]} Treasury origins. Replacing the clean pool ending at r−H with one ending at r includes {a["per_refit_immature_label_count"]} immature labels per refit. In Treasury QR the illegal oracle reduces loss by {fmt(-bny["rows"][0]["illegal_minus_clean_percent"],4)}% but changes breaches from {bny["rows"][0]["clean"]["strict_breach_count"]} to {bny["rows"][0]["oracle_leakage"]["strict_breach_count"]}; FX QR instead raises loss by {fmt(a["rows"][0]["illegal_minus_clean_percent"],4)}%. The complete QR, KNN and F outcomes in Supplement Table S37 have mixed directions. This post-result / exploratory control quantifies timing contamination in these blocks, not an inevitable optimism bias or an all-sample performance effect.')
 elif key=='motivation':
  b=btext(f'A position can finish below a monitoring report after exceeding it within the horizon. For the Treasury-bill aggregate at economic date {ex["dates"][0][:10]}, a clean frozen-F report of {fmt(ex["report"],0)} USD millions exceeds the absolute endpoint {fmt(ex["endpoint_absolute"],0)}, yet the sampled path reaches {fmt(ex["peak"],0)} (Figure 1). A script selects the earliest original evaluation origin satisfying absolute endpoint ≤ clean report &lt; sampled peak. This post-result / exploratory illustration uses a downloaded vintage and an explicit selection rule; it is not evidence of typicality, a public-release backtest or the unobserved maximum between source records.')
 elif key=='motivating_caption':
  b={'type':'p','caption':f'Figure 1†. Endpoint versus sampled peak in the earliest eligible Treasury illustration. Origin {ex["origin"]}, economic date {ex["dates"][0][:10]}, horizon {ex["horizon"]} records; positions and clean frozen-F report are in USD millions. The report is {fmt(ex["report"],0)}, the sampled peak {fmt(ex["peak"],0)}, and the absolute endpoint {fmt(ex["endpoint_absolute"],0)}. Selection uses the original evaluation range and the stated endpoint ≤ report < peak rule; economic dates are not original public-release times.'}
 elif key=='contribution1':
  b=btext(f'<b>Contribution on the forecast object.</b> We characterize a sampled absolute-position peak with an issue-known floor, rather than infer it from endpoint marginal forecasts. Proposition 1 gives the pointwise floor projection and the population strict-tail qualification; Proposition 2 makes the classical absolute-displacement endpoint bound explicit, and Proposition 3 bounds common-pool historical-construction differences. True targets are ordered across horizons, but the independently fitted FX QR at W{cr[1]} crosses on {cr[3]}/{cr[4]} archived origins (Supplement Table S15). Wisniewski and coauthors study endpoint intervals, while MaxVaR and the payment-liquidity literature already study other path extrema; those precedents prevent a first-path-risk claim (Table 1). The contribution is the precise target-specific synthesis, qualified mathematical properties and observed coherence failure, with proofs and counterexamples in Section 4 and the Supplement.')
 elif key=='contribution2':
  d=row(DM,IDS[1]);h=row(HOLM,IDS[1])
  b=btext(f'<b>Contribution on model evaluation.</b> We find a statistically favorable score comparison that coexists with more breach occasions in the inspected FX record; elementary-score curves for the distinct original primary cross. Matched-history short-horizon QR changes mean pinball loss by {fmt(ma["relative_mean_loss_difference_percent"],2,True)}%, with {ma["strict_breach_count_left"]} rather than {ma["strict_breach_count_right"]} breaches; its DM statistic is {fmt(d["dm_t"],3)} and Holm p={float(h["holm_p"]):.3g} (Tables 3–4 and Figures 3–4). Table 5 supplies an exact common-denominator bridge for the original primary, and Supplement S15 contrasts clean timing with deliberately illegal labels. CAViaR, Ehm and the endpoint-source studies already combine scoring and calibration, so joint reporting itself is not claimed as a new method (Table 1). The contribution is the decomposed, maturity-controlled evidence on this peak response and the limits it places on a single-score model-validation decision, not a systematic bias of proper pinball scoring.')
 elif key=='contribution3':
  b=btext(f'<b>Contribution on transport.</b> We find that conditional-model success is sensitive to the executed history, horizon and financial measurement process. The separately fitted Treasury QR primary changes mean loss by {fmt(tr["relative_mean_loss_difference_percent"],2,True)}%, while the additional aggregate panel has {wins[0]}/{cells} lower-loss QR33 cells, {wins[1]}/{cells} parsimonious cells and {wins[2]}/{cells} endpoint-bound plug-in cells (Supplement Tables S9 and S32). The source family contains the original bill task plus {len(pa["rows"])} additional related Treasury tasks; these share dealers and reporting systems and are not independent dealer replications. Unlike the same-source endpoint lineage and the different functional in Duffie and coauthors, Section 8 evaluates this common peak target across the FX and aggregate measurement tasks (Table 1). The complete adverse and failed cells delimit the empirical scope, and the decision map in Table 6 organizes validation choices without prescribing a deployed switching policy.')
 elif key=='abstract':
  b=btext(f'Endpoint forecasts do not determine the maximum position reached along a financial path. We study the upper quantile of a sampled absolute net-position peak with a known current-position floor, explicitly matured training labels and matched-history controls. We state a pointwise floor projection, a classical absolute-displacement endpoint-to-peak bound and common-pool construction distances; none creates a new distribution-free coverage guarantee for fitted reports. Three findings delimit the empirical value. On the previously inspected FX record, the matched-history short-horizon regression lowers mean pinball loss by {fmt(-float(ma["relative_mean_loss_difference_percent"]),2)}% but increases breaches from {ma["strict_breach_count_right"]} to {ma["strict_breach_count_left"]}. Elementary-score curves for the distinct original FX primary cross, ruling out dominance for that pair. Horizon-specific short-history FX regression reports cross on {cr[3]}/{cr[4]} origins despite ordered realized targets. The separately fitted Treasury regression primary raises loss by {fmt(tr["relative_mean_loss_difference_percent"],2)}%, and the additional aggregate panel yields only {wins[0]}/{cells} lower-loss original-regression cells. Exact gain decomposition and deliberately invalid label-timing controls are post-result / exploratory, with mixed-direction timing effects retained. The Treasury exercise replays a downloaded vintage by economic date; compatible unseen-dealer and prospective public-release validation remain outstanding. The evidence supports joint validation of accuracy, calibration, report coherence and measurement compatibility, rather than a universal forecasting or funding advantage.')
 elif key=='coherence':
  b=btext(f'Observed targets satisfy P(H6)≤P(H24), and population conditional quantiles under the same origin information inherit that ordering. Independently estimated forecasts need not: FX QR W{cr[1]} crosses on {cr[3]}/{cr[4]} issues (Supplement Table S15). A raise-only repair of the longer-horizon report can increase pinball loss, as the exact counterexample in Supplement S15 shows. This does not rule out all monotone rearrangements: with equally weighted ordered outcomes and a common quantile level, sorting can weakly reduce total pinball loss without guaranteeing each horizon improves. Crossing is a coherence diagnostic, not sufficient proof of calibration failure.')
 elif key=='conditional_significance':
  kn=row(HOLM,'fx_hourly-h6-KNN2880-minus-frozen_F2880');qr=row(HOLM,IDS[1]);qs=row(HOLM,'fx_hourly-h6-QR720-minus-frozen_F720')
  b=btext(f'The long-history FX short-horizon score evidence is not confined to QR: the matched KNN comparison also has Holm p={float(kn["holm_p"]):.4g}, alongside QR p={float(qr["holm_p"]):.3g}. Short-history QR has DM p={float(qs["dm_p"]):.3g} and Holm p={float(qs["holm_p"]):.3g}. These are post-result working-reference diagnostics on the same inspected sample, not selection-adjusted confirmations or evidence that only one conditional family can improve (Supplement Tables S6 and S25).')
 elif key=='decision_table':
  b={'type':'table','caption':'Table 6†. Descriptive validation decision map for the executed archives. Frequency and history are jointly associated with these outcomes; no causal frequency effect, universal model-selection rule or retrospective switching policy is identified.','headers':['Source/history setting','Evidence to examine','Validation caution'],
  'rows':[['FX, longer history, short horizon','QR and KNN score evidence; Tables 3 and S25','More QR breaches and crossed score curves; Tables 3–4, Figure 3'],['FX, shorter history or longer horizon','Full matched comparisons; Supplement Table S3','QR deterioration and horizon crossing remain; Table S15'],['Weekly aggregate, original and added tasks','Historical F, parsimonious and L comparisons; Tables S4, S9, S32','Related aggregate tasks, not unseen dealer validation'],['Endpoint-based bound in any source','Proposition 2; simulations in Supplement S11','Absolute displacement, conditional premises and plug-in uncertainty must be checked']]}
 else:raise KeyError(key)
 b['_generator']='v5:'+key;b['_bindings']=binding(allpaths);return b

def generated(key):
 if key=='positioning_table':
  from v5_positioning import positioning_table
  b=positioning_table();b['caption']='Table 1. '+b['caption'];b['_generator']='v5:'+key
  b['_bindings']=binding(['notes/revision-v5-novelty/literature-a.json','notes/revision-v5-novelty/literature-b.json'])
  return b
 return _generate(key)

def source_block(b,path,pointer):
 b=deepcopy(b);b['_source']={'path':path,'sha256':fp(path),'pointer':pointer};return b

def compose(write_outputs=True):
 d,s=read(BASE),read(SUPP);d=deepcopy(d);s=deepcopy(s)
 d['title']=TITLE;s['title']='Online Supplement: '+TITLE
 d['abstract']=generated('abstract')['html'];d.pop('_abstract_source',None);d['_abstract_generator']='v5:abstract';d['_abstract_bindings']=generated('abstract')['_bindings']
 # Stable remapping of old main figures, moving the annual display to its existing supplement copy.
 for doc in (d,s):
  for sec in doc['sections']:
   for b in sec['blocks']:
    for k in ('html','caption','text'):
     if k in b:
      b[k]=b[k].replace('Figures 2 and 3','Figures 3 and 4')
      b[k]=re.sub(r'Figure ([1-4])\b',lambda m:{'1':'Figure 2','2':'Figure 3','3':'Figure 4','4':'Supplement Figure S3'}[m[1]],b[k])
      b[k]=b[k].replace('main-text Supplement Figure S3','Supplement Figure S3')
      b[k]=b[k].replace('Section 9','Section 10').replace('Proposition 1','Proposition 2')
 # Old budget is retained exactly in Supplement, leaving room for the new positioning table.
 budget=deepcopy(d['sections'][2]['blocks'][3]);budget['caption']=budget['caption'].replace('Table 1.','Table S36.')
 d['sections'][2]['blocks']=[b for b in d['sections'][2]['blocks'] if b is not d['sections'][2]['blocks'][3]]
 d['sections'][2]['blocks'].append(p('Supplement Table S36 retains the source-specific chronological budgets.'))
 # New introduction follows motivation, gap, design, findings and implications.
 oldintro=deepcopy(d['sections'][0]['blocks'])
 d['sections'][0]['blocks']=[oldintro[0],generated('motivation'),{'type':'figure','index':0,'_definition':'Source-bound figure caption and vector asset'},
 p('Endpoint conditional intervals, portfolio drawdown measures and payment-system liquidity maxima have different response functionals. Table 1 locates these precedents and the narrower unresolved comparison: the sampled absolute-position peak, its issue-known floor and mature-label timing under a common forecasting and validation design. The table records unverified dimensions as n.r.; it does not establish global priority.'),
 p('We compare historical headroom, translated-path and floored-peak rules with conditional regression and neighbor quantiles, retaining matched histories and update schedules. The original source primaries remain unchanged. Research questions concern predictive accuracy (RQ1), scoring and calibration (RQ2), and transport and robustness (RQ3); later extensions are explicitly post-result / exploratory.'),
 generated('contribution1'),generated('contribution2'),generated('contribution3'),
 p('For model validation, lower average quantile loss should be read alongside coverage diagnostics, report coherence and the measurement process. Proper pinball scoring aggregates error magnitudes; its ordering need not match a breach-frequency ordering. Neither the stipulated asymmetry nor these passive position envelopes identify realized financing costs, inventory decisions or capital savings.'),
 p('The following sections locate the literature, define data and the target, state the construction properties, and answer the research questions. Model-validation implications precede interpretation and limitations; the Supplement retains all earlier results, unsuccessful cells and later exploratory evidence.')]
 # Positioning, with earlier related-literature text retained but new comparison qualified.
 d['sections'][1]['blocks'].insert(0,generated('positioning_table'))
 d['sections'][1]['blocks'].append(p('The cell-level original-text locators, reading scope and search limits accompany the table in the Supplement and repository search log. Endpoint-source studies already combine scoring with coverage tests; CAViaR and Murphy-diagram work also join accuracy and calibration. MaxVaR already converts endpoint distributional information into path-risk quantities. The present comparison therefore concerns a distinct measured functional and its empirical validation, not priority over these general ideas. The payment-peak thesis remains an acknowledged precedent, but its original text could not be newly retrieved for the cell-by-cell table.'))
 # Fix the structural proposition reference in the method table, without changing empirical cells.
 d['sections'][3]['blocks'][1]['rows'][4][2]='Proposition 2; Supplement S11'
 # Known-floor, common-rank and classical-bound propositions are explicit applications.
 m=d['sections'][3];end=next(i for i,b in enumerate(m['blocks']) if b.get('text')=='Classical maximal-inequality benchmark')
 operational=deepcopy(m['blocks'][end+3]);operational['html']=operational['html'].replace('Proposition 2','Proposition 2')
 m['blocks']=m['blocks'][:end]
 th=read('notes/revision-v5-novelty/theory-source.json')['blocks']
 for j,b in enumerate(th):m['blocks'].append(source_block(b,'notes/revision-v5-novelty/theory-source.json',['blocks',j]))
 m['blocks'] += [operational,generated('coherence'),p('The historical controls also use current information: the headroom and floored-peak rules incorporate the observed magnitude, and path translation uses the current signed anchor. Conditional estimation is therefore compared with already anchored historical forecasts, not with a rule that ignores the current observation.')]
 # Retain the factual joint result table and every archived empirical paragraph.
 d['sections'][5]['blocks'].insert(2,generated('gain_table'));d['sections'][5]['blocks'].insert(3,generated('gain_text'))
 d['sections'][5]['blocks'].append(generated('conditional_significance'))
 d['sections'][4]['blocks'].insert(2,generated('leakage_text'))
 # The old annual main figure is removed as a reference only; the existing asset and Supplement display remain.
 for sec in d['sections']:
  sec['blocks']=[b for b in sec['blocks'] if not (b['type']=='figure' and b.get('index')==3)]
  for b in sec['blocks']:
   if b['type']=='figure' and not (sec is d['sections'][0]):b['index']+=1
 newfig=generated('motivating_caption');d['figures']=[{'path':'figures/endpoint-peak-example.pdf','caption':newfig['caption'],'_generator':'v5:motivating_caption','_bindings':newfig['_bindings']},*d['figures'][:3]]
 for i,f in enumerate(d['figures'][1:],2):f['caption']=re.sub(r'^Figure \d+',f'Figure {i}',f['caption'])
 # Correct the atom claim; do not weaken any empirical failure.
 lim=d['sections'][8]
 lim['blocks'][3]=p('Shared histories, overlapping labels, finite validation and investigator selection limit statistical generalization. An atom at the true quantile may lower its strict-breach probability below the nominal tail probability; the known floor alone does not imply such an atom. Numerical acceptance supplies no conditional-coverage guarantee. Horizon-specific mature scenario sets differ, so zero observed crossings cannot establish population coherence.')
 lim['blocks'].append(p('Anticipated concerns. The Kaggle source supplies a single attributed position series, not independently audited dealer books; original-source documentation, fingerprints and explicit clock checks partly support reproducibility but cannot verify commercial completeness or measurement accuracy. Dealer aggregation permits cancellation and valuation or composition changes; source-unit definitions and the full related-task panel preserve that measured interpretation rather than treating it as individual exposure. The FX interval was previously inspected, so later tests and model choices remain retrospective; preserved primaries, complete adverse outcomes and time-respecting labels reduce selective reporting but do not create a fresh holdout.'))
 imp={'title':'9. Implications for model validation','blocks':[
 p('Jointly report quantile loss, strict-breach frequency and dependence-aware calibration diagnostics. Add elementary-score curves and sensitivity to stipulated loss preferences when an average-score gain might be interpreted as safer limits. A proper quantile score is not systematically biased toward more breaches; it evaluates magnitudes, whereas breach frequency discards them. Equality-based hit tests and valid population upper-quantile inequalities also require distinct interpretations.'),
 p('Use frequency, history and the measurement definition to frame validation comparisons before selecting a method family. Table 6 summarizes the executed evidence and its cautions; it is a descriptive map, not a new switching algorithm. Retain historical and parsimonious controls alongside fitted procedures, compare matching completed-label pools, and preserve numerical failures and adverse cells. The observed contrasts do not isolate a causal frequency effect.'),
 p('For endpoint-based peak bounds, first verify that the available input is an absolute cumulative-displacement quantile at the required level. A generic one-sided endpoint VaR is not interchangeable. Check conditional independence and symmetry if conditional coverage is claimed, and distinguish a population quantile from an estimated overlapping-label plug-in. The classical bound can be conservative or lose its guarantee outside its premises; no cost or operational-resource reduction follows automatically.'),generated('decision_table')]}
 d['sections'].insert(8,imp)
 d['sections'][9]['title']='10. Interpretation and limitations';d['sections'][10]['title']='11. Conclusion'
 d['sections'][10]['blocks']=[
 p('<b>RQ1 — Accuracy.</b> Conditional regression improves the inspected FX short-horizon score, while the separately fitted Treasury regression primary deteriorates. The exact additive bridge separates the joint history/update contrast from the conditional-procedure contrast, without identifying causal estimator effects. Historical, neighbor and conditional-model rankings depend on the executed comparison.'),
 p('<b>RQ2 — Evaluation.</b> A score gain can coexist with more breach occasions, crossed elementary-score curves and horizon-incoherent fitted reports. The floor projection and classical construction properties clarify what can be guaranteed pointwise or under population assumptions; the fitted empirical reports have no automatic coverage guarantee. Score, calibration and report-coherence evidence must retain their distinct nulls and meanings.'),
 p('<b>RQ3 — Transport.</b> Parsimonious regression, related aggregate tasks and strong implemented baselines give mixed and frequently adverse outcomes. The observed aggregate failures delimit portability across financial measurement processes; they are not independent dealer replications or proof that all conditional methods fail.'),
 p('The evidential next steps are execution of the timestamped prospective public-release protocol, access to a compatible unseen dealer series, and extensions such as CAViaR or sequential conformal forecasting with explicit mature-label timing. Investigator selection, downloaded vintages, unexecuted baseline families and the missing decision-cost mapping constrain interpretation. All original adverse cells and unsuccessful fits remain in the Supplement.')]
 # Correct stale appendix-caption routes without touching their data.
 for sec in s['sections']:
  for b in sec['blocks']:
   if 'caption' in b:b['caption']=re.sub(r'Appendix ([A-L])\b',lambda m:'Supplement S'+str(ord(m[1])-ord('A')+2),b['caption'])
 # Supplement append-only extension; every pre-v5 table remains unchanged except its routing label.
 s['sections'].append({'title':'S15. V5 post-result analyses and positioning evidence','blocks':[
 sub('Chronological budgets retained from the main article'),budget,
 sub('Deliberately immature-label oracle'),generated('leakage_text'),generated('leakage_table'),
 p('The clean and illegal arms keep selected parameters fixed; transforms are recomputed within each arm. The blocks are deterministic clock locations rather than favorable outcome selections. Clean stored outputs are independently read back from the original hash-bound trace subset, but this is an implementation check on the same data, not independent financial validation.'),
 sub('Exact gain bridge'),generated('gain_text_supp'),
 sub('Mathematical illustrations'),p('The construction properties are elementary target-specific statements, not newly discovered probability inequalities. Exact finite-distribution checks show that identical marginal observations and identical endpoint marginals need not determine a peak quantile. A separate counterexample rejects substitution of a one-sided endpoint quantile for the absolute-displacement quantile. The executable examples, floor-atom counterexample and raise-only horizon-repair counterexample are retained in the theory source and tests.'),
 p('A raise-only horizon repair can increase loss; this does not imply that every monotone rearrangement fails. Under a common quantile level, equal weights and ordered outcomes, sorting can weakly improve the total pinball sum without ensuring improvement separately at every horizon.'),
 sub('Positioning-table original-text evidence'),p('The following source locators apply to the reported cell values. n.r. means not reported in the actual inspected scope, rather than a verified absence throughout an entire work. The original thesis on conditional cash peaks could not be newly retrieved and is omitted from the table rather than assigned guessed cells.') ]})
 for j,b in enumerate(read('notes/revision-v5-novelty/theory-source.json')['examples']):
  s['sections'][-1]['blocks'].insert(10+j,source_block(b,'notes/revision-v5-novelty/theory-source.json',['examples',j]))
 from v5_positioning import positioning_evidence
 ev=positioning_evidence()
 if write_outputs:dump(NOTE/'positioning-source.json',ev)
 # Evidence is machine-readable with per-cell locators; concise printable appendix is generated separately.
 for bl in positioning_print_blocks(ev):s['sections'][-1]['blocks'].append(bl)
 amendments=NOTE/'reference-amendments.json'
 if amendments.exists():
  data=read(str(amendments.relative_to(ROOT)))
  for rec in data.get('rows',[]):
   for doc in (d,s):
    for ref in doc['references']:
     if ref['id']==rec['id'] and rec.get('proposed_note'):ref['html']=html.escape(rec['proposed_note'])+' '+"<a href='"+rec['proposed_url']+"'>Original source</a>."
 # New cell-level literature locators are independently readable in the Supplement.
 required={'wisniewski2020','wisniewski2024','boudoukh2004','petrunia2019','arjani2020','engle2004','ehm2016','duffie2023'}
 present={r['id'] for r in s['references']}
 s['references'] += [deepcopy(r) for r in d['references'] if r['id'] in required-present]
 s['references'].sort(key=lambda r:plain(r['html']).lower())
 if write_outputs:
  dump(OUT/'manuscript-content.json',d);dump(OUT/'supplement-content.json',s)
  dump(NOTE/'contributions-before-after.json',{'before':oldintro[7]['html'],'after':[generated('contribution'+str(i))['html'] for i in range(1,4)],'selected_title':TITLE,'alternates':ALTERNATES,'abstract':d['abstract']})
 return d,s

def positioning_print_blocks(ev):
 # The generator returns only text for locators; no source prose is quoted at length.
 from v5_positioning import printable_evidence_blocks
 return printable_evidence_blocks(ev)

if __name__=='__main__':
 d,s=compose();print('V5 content assembled; original result rows preserved, new claims regenerated from exact contexts.')
