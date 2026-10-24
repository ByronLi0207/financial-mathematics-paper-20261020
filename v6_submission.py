"""V6 reader-facing synthesis; immutable v5 snapshots and new aggregate bindings."""
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import csv,hashlib,html,json,re
from v4_submission import ROOT,OUT,plain
from v4_numeric import fields

NOTE=ROOT/'notes/revision-v6'
BASE='notes/revision-v6/v5-manuscript-before.json'
SUPP='notes/revision-v6/v5-supplement-before.json'
RES='results/revision-20261023/v6/'
INPUTS=[BASE,SUPP,'protocol/revision-20261022/study-spec.json','results/revision-20261022/paired-comparisons.csv',
        RES+'wp2-findings.json',RES+'wp2-summary.json',RES+'wp2-comparisons.json',RES+'wp3-combinations.json',RES+'wp3-findings.json',RES+'wp4-states.json',RES+'wp5-tau-summary.json',
        'notes/revision-v6/reference-additions.json']

def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def bindings():return [{'path':p,'sha256':sha(p)} for p in INPUTS]
def p(text,**meta):return {'type':'p','html':text,**meta}
def fmt(x,n=2):return f'{abs(float(x)):.{n}f}'

def remap_tables(text):
    return re.sub(r'\bTable 4\b|\bTable 5\b|\bTables 3[–-]4\b',lambda m:{'Table 4':'Table 5','Table 5':'Table 4','Tables 3–4':'Tables 3 and 5','Tables 3-4':'Tables 3 and 5'}[m[0]],text)

def map_visible(b):
    for key in ('html','caption','text'):
        if key in b:b[key]=remap_tables(b[key]).replace('on277','on 277')
    for key in ('headers','rows'):
        if key in b:
            def walk(x):return [walk(y) for y in x] if isinstance(x,list) else remap_tables(x) if isinstance(x,str) else x
            b[key]=walk(b[key])

def inputs_signature():
    # Content fingerprints remain in every emitted binding. Stat tuples only key
    # this process-local deterministic composition cache; they are not provenance.
    paths=INPUTS+['v6_submission.py','v6_supplement.py']
    paths += [str(x.relative_to(ROOT)) for x in (ROOT/RES).rglob('*.json')]
    return tuple((q,(ROOT/q).stat().st_mtime_ns,(ROOT/q).stat().st_size) for q in sorted(set(paths)))

@lru_cache(maxsize=3)
def _documents(_signature):
    from v6_supplement import additional_section,additional_figures
    oldd,olds=read(BASE),read(SUPP);d,s=deepcopy(oldd),deepcopy(olds)
    for doc in (d,s):
        for sec in doc['sections']:
            for b in sec['blocks']:map_visible(b)
    # The tables now read in physical order; old scientific cells are untouched.
    # Main contribution routes its matched contrast to its own tables, separately
    # from the original-primary elementary score diagrams.
    c=d['sections'][0]['blocks'][6]
    c['html']=c['html'].replace('We find a statistically favorable score comparison that coexists with more breach occasions in the inspected FX record; elementary-score curves for the distinct original primary cross.',
        'We find a lower mean score with a favorable DM working-reference diagnostic alongside more breach occasions in the inspected FX record; this retrospective diagnostic is not selection-adjusted confirmation.')
    c['html']=c['html'].replace('(Tables 3 and 5 and Figures 3–4).','(Tables 3 and 5). The distinct original FX primary has crossed elementary-score curves (Figure 3); the original Treasury primary is shown separately in Figure 4.')
    # Keep every old abstract empirical value and add the exact original FX primary
    # before the separately named matched control, rather than swap their identities.
    with (ROOT/'results/revision-20261022/paired-comparisons.csv').open(newline='') as f:archive=list(csv.DictReader(f))
    fx=next(r for r in archive if r['contrast_id']=='fx_hourly-h6-QR2880-minus-rolling_F720')
    d['abstract']=d['abstract'].replace('On the previously inspected FX record, the matched-history short-horizon regression lowers',
        'The original FX primary lowers mean loss by '+fmt(fx['relative_mean_loss_difference_percent'],3)+'% on the previously inspected record. Its separately identified matched-history short-horizon regression lowers')
    d['abstract']=d['abstract'].replace('Exact gain decomposition and deliberately invalid label-timing controls are post-result / exploratory, with mixed-direction timing effects retained.',
        'Exact gain decomposition, label-timing controls and additional mature benchmarks are post-result / exploratory, with mixed directions, failed fits and incomplete upper-target evidence retained.')
    # Data interpretation is the measured source sample, not an audited whole book.
    data=d['sections'][2]['blocks'][0]
    data['html']=data['html'].replace('Wisniewski et al. (2020) describe aggregate client-flow positions across five liquid currency pairs for one market maker.',
        'Wisniewski et al. (2020) attribute these aggregate client-flow positions across five liquid currency pairs to one market maker; this source description does not independently verify a complete dealer book.')
    d['sections'][2]['blocks'][1]['html']=d['sections'][2]['blocks'][1]['html'].replace('It does not identify gross exposures or pure customer order flow.',
        'The absolute signed aggregate is not the sum of absolute dealer positions and does not identify gross exposures or pure customer order flow.')
    cfg=read('protocol/revision-20261022/study-spec.json')['sources']
    counts={source:{phase:z[phase+'_origin_last']-z[phase+'_origin_first']+1 for phase in ('validation','evaluation')} for source,z in cfg.items()}
    d['sections'][2]['blocks'][6]=p('The FX validation and evaluation segments contain '+str(counts['fx_hourly']['validation'])+' and '+str(counts['fx_hourly']['evaluation'])+' origins, with histories '+str(cfg['fx_hourly']['windows'][0])+' or '+str(cfg['fx_hourly']['windows'][1])+' and scheduled refits every '+str(cfg['fx_hourly']['refit_step'])+' records. Treasury contains '+str(counts['nyfed_weekly']['validation'])+' and '+str(counts['nyfed_weekly']['evaluation'])+' origins, histories '+str(cfg['nyfed_weekly']['windows'][0])+' or '+str(cfg['nyfed_weekly']['windows'][1])+' and refits every '+str(cfg['nyfed_weekly']['refit_step'])+' records. Supplement Table S36 gives the full chronological and computational budgets.')
    # Inventory-control motivation is separate from identification of active policies.
    d['sections'][0]['blocks'][0]['html'] += ' The inventory literature motivates monitoring; this passive forecast comparison identifies no change in optimal quotes, hedges or realized funding requirements.'
    method=d['sections'][3]['blocks'][1]
    method['caption']=method['caption'].replace('Parameter menus and fitted choices are retained in Supplement Table S2.', 'Original QR/KNN parameter menus and fitted choices are retained in Supplement Table S2; the additional finite adaptations and combinations are defined in Supplement S16.')
    method['rows'] += [
        ['Finite delayed ACI-style','One-sided mature residual calibration around frozen F or QR','Supplement S16; finite projected adaptation, no inherited coverage guarantee'],
        ['Headroom SAV','Symmetric absolute-value (SAV) recursion driven by the latest mature headroom','Supplement S16; CAViaR-inspired adaptation, fixed multi-start menu and complete-cell failure rule'],
        ['Fixed combinations','Mean of F/QR; median of F/QR/plain KNN','Supplement S16; matched histories, no fitted weights or missing-constituent substitution']]
    related=d['sections'][1]['blocks'][3]
    related['html']=related['html'].replace('sequential conformal prediction (Xu and Xie, 2023)',
        'adaptive conformal inference (ACI) of Gibbs and Candès (2021), sequential conformal prediction (Xu and Xie, 2023)')
    d['sections'][3]['blocks'][25]['html']=d['sections'][3]['blocks'][25]['html'].replace('classical Lévy maximal inequality,','classical Lévy maximal inequality (Sussman, 2023),')
    # Keep strict-improvement language within the nonzero nonnegative-weight domain.
    weight_old='their sample-average improvement persists under every constant nonnegative linear weighting of those components.'
    weight_new='their sample-average loss is lower under every constant nonnegative linear weighting of those components with at least one positive weight.'
    weight_blocks=[b for b in d['sections'][6]['blocks'] if weight_old in b.get('html','')]
    if len(weight_blocks)!=1:raise ValueError('WEIGHT_LANGUAGE_ANCHOR_NOT_UNIQUE')
    weight_blocks[0]['html']=weight_blocks[0]['html'].replace(weight_old,weight_new)
    # Explicit old/new diagnostic definition distinction preserves old reported CC.
    control_horizon=read('protocol/revision-20261022/study-spec.json')['horizons'][0]
    for old,new in [
        ('deliberately invalid label-timing control','deliberately invalid H'+str(control_horizon)+' label-timing control'),
        ('common-history family receives Holm','common-history equal-loss ranking family receives Holm')]:
        matches=[b for b in d['sections'][4]['blocks'] if old in b.get('html','')]
        if len(matches)!=1:raise ValueError('EVALUATION_CLARITY_ANCHOR_NOT_UNIQUE')
        matches[0]['html']=matches[0]['html'].replace(old,new)
    d['sections'][4]['blocks'][10]['html'] += ' The additional benchmarks in Supplement S16 use a separately stated transition-conditional CC likelihood on adjacent sparse-grid pairs, conditioning on the initial hit; their values do not replace this archived convention. Their ranking families are frozen separately, and NA adjustment bookkeeping is kept distinct from an observed p-value.'
    # Name each comparator without changing its saved score or grid identity.
    grid_old='H6/H24 legacy-reference'
    grid_blocks=[b for b in d['sections'][5]['blocks'] if grid_old in b.get('html','')]
    if len(grid_blocks)!=1:raise ValueError('GRID_COMPARATOR_LABEL_ANCHOR_NOT_UNIQUE')
    grid_blocks[0]['html']=grid_blocks[0]['html'].replace(grid_old,'H6 original-primary and H24 legacy-reference')
    wrapped=next(r for r in read(RES+'wp2-findings.json')['wrapped_pairs'] if (r['source'],r['horizon'],r['window'])==('fx_hourly',6,2880))
    extra=p('Additional post-result / exploratory benchmarks sharpen this distinction. In the long-history short-horizon FX matched context, finite projected delayed ACI-style wrappers leave QR with '+fmt(wrapped['qr_minus_f_loss_percent'])+'% lower mean loss than the wrapped historical rule while both observed breach frequencies are close to the nominal tail target. This is an empirical joint score–frequency result, not a conditional-coverage or canonical ACI guarantee. Headroom SAV does not beat matched F in either primary context. The fixed median improves on matched F and QR in the Treasury primary context, but its breach frequency still exceeds the nominal tail target; neither fixed combination beats QR in the FX primary context. For the original FX primary, observed mean loss favors QR in every training-defined position-change state; the evidence does not support an advantage confined to the high state or significance in every group. The original Treasury primary remains adverse across states. The lower target-level check retains the available comparison directions; the upper level remains unevaluable because of failed validation or insufficient tail information. Supplement S16 retains every menu, adverse cell, NA and working-reference diagnostic.',_v6_role='new_evidence_paragraph')
    for old,new in [('leave QR with','leave wrapped QR (ACI-QR) with'),('than the wrapped historical rule','than wrapped F (ACI-F)')]:
        if extra['html'].count(old)!=1:raise ValueError('ACI_COMPARATOR_LABEL_ANCHOR_NOT_UNIQUE')
        extra['html']=extra['html'].replace(old,new)
    d['sections'][6]['blocks'].append(extra)
    decision=d['sections'][8]['blocks'][3]
    decision['rows'][0]=['FX, longer history, short horizon','Matched score evidence, finite ACI-style and fixed combinations; Tables 3 and 5; Supplement S16','Original-primary score crossing is Figure 3; matched wrappers have separate diagnostics. Check actual frequency and the named control.']
    decision['rows'][2][1] += '; fixed combinations and headroom SAV: Supplement S16'
    decision['rows'][2][2] += '; a lower combination score does not establish nominal coverage'
    decision['rows'].append(['Issue-known position-change state','Training-defined RMS groups and separate conditional-moment tests; Supplement S16','Observed mean loss for the original FX primary versus rolling F favors QR across groups, without strong group-heterogeneity evidence or significance in every group; Treasury remains adverse with imbalanced small groups. No deployed switching rule.'])
    decision['rows'].append(['Original source primaries and named FX matched control','Target-level refits under the same original clocks; Supplement S16','Available lower-level comparisons retain direction; upper-level evidence is unavailable under full-menu or tail-information rules. This does not cover shorter-history or longer-horizon targets.'])
    d['sections'][9]['blocks'][5]=p('The executed finite projected delayed ACI-style, headroom SAV and fixed combinations in Supplement S16 broaden the benchmark menu without representing their entire method classes. Canonical sequential conformal procedures, richer mean or volatility dynamics, and innovation-tail conditional EVT remain distinct alternatives. The fixed FHS, QRF and peak-POT additions in Supplement S13 retain their failures and resource limits. Matching mature-label pools and update schedules leaves feature lookbacks, assumptions and estimation rules different. Compatible new dealer observations, historical release vintages and decision-linked inputs remain necessary for broader portability.')
    d['sections'][10]['blocks'][3]=p('The evidential next steps are execution of the timestamped prospective public-release protocol, access to a compatible unseen dealer series, and evaluation of the remaining method classes under explicit mature-label timing. The additional finite adaptations and combinations do not close those evidence gaps. Investigator selection, downloaded vintages, unexecuted alternatives and the missing decision-cost mapping constrain interpretation. All original adverse cells and unsuccessful fits remain in the Supplement.')
    d['sections'][11]['blocks']=[b for b in d['sections'][11]['blocks'] if not b.get('html','').startswith('AI-use disclosure:')]
    # Reader-facing locators replace revision labels and bare machine filenames.
    s['sections'][14]['title']='S15. Post-result analyses and positioning evidence'
    s['sections'][12]['blocks'][12]['html']='Following the leaf-distribution quantile construction of Meinshausen (2006), '+s['sections'][12]['blocks'][12]['html'][0].lower()+s['sections'][12]['blocks'][12]['html'][1:]
    replacements={
        'The public results.json retains exact rational boundaries and every endpoint/tie set, all 128 input summaries, 448 pair relations and coefficientwise dominance.':'The exact companion inventory for this section retains rational boundaries and every endpoint/tie set, all 128 input summaries, 448 pair relations and coefficientwise dominance; the repository reproduction guide links the machine-readable files.',
        'New v3 inference has its own scripts, output identities and tests, leaving the archived scientific files intact.':'The later inference has its own scripts, output identities and tests, leaving the archived scientific files intact.',
        'No D1 result replaces either original primary':'No added baseline result replaces either original primary',
        'parameter-binding JSON':'machine-readable parameter binding'}
    for sec in s['sections']:
        for b in sec['blocks']:
            if 'html' in b:
                for a,z in replacements.items():b['html']=b['html'].replace(a,z)
    additions=additional_section();s['sections'].append(additions)
    base_fi=len(s['figures']);figures=additional_figures()
    for i,f in enumerate(figures):
        f=deepcopy(f);f['caption']='Figure S'+str(base_fi+i+1)+'†. '+f['caption']
        # Add the figure number in root canonical generation; the agent generator
        # continues to own the numerical caption and plot input hashes.
        f['_generator']='v6:figure:supplement:'+str(base_fi+i);f['_bindings']=bindings()+f.get('_bindings',[])
        s['figures'].append(f);additions['blocks'].append({'type':'figure','index':base_fi+i,'_definition':'Additional fixed-combination diagrams; matched controls only'})
    # Include actual new citations where they occur; retain old references pending
    # the separate citation completeness audit, never invent metadata.
    union={r['id']:deepcopy(r) for doc in (oldd,olds) for r in doc['references']}
    for ref in read('notes/revision-v6/reference-additions.json')['entries']:union[ref['id']]={'id':ref['id'],'html':ref['html']}
    for doc,required in [(d,{'gibbs2021'}),(s,{'gibbs2021','engle2004','gw2006','kupiec1995','christ1998','dm1995','nw1987','hln1997','holm1979','ehm2016','meinshausen2006'})]:
        present={r['id'] for r in doc['references']}
        doc['references'] += [deepcopy(union[k]) for k in sorted(required-present)]
        doc['references'].sort(key=lambda r:plain(r['html']).casefold())
    for doc in (d,s):
        for sec in doc['sections']:
            sec['title']={'S5. Explicitly report diagnostics':'S5. Diagnostics of issued reports','S10. selected-fit shrinkage diagnostics':'S10. Diagnostics for selected fits','S13. mature-baseline methods and complete outputs':'S13. Mature baselines: methods and complete outputs'}.get(sec['title'],sec['title'])
            for block in sec['blocks']:
                if block['type']=='subheading' and block.get('text','').startswith('Ar '):block['text']='AR '+block['text'][3:]
                if 'html' in block:
                    block['html']=block['html'].replace('short/long past increment RMS','short/long past increment root-mean-square (RMS) summaries').replace('the two-RMS pair','the pair of root-mean-square (RMS) summaries').replace('show the full-pool fallback','show the selected full-pool identity')
                    block['html']=block['html'].replace('it applies throughout the Supplement.', 'it applies throughout the Supplement, with the section-wide post-result label in S16 also covering its unmarked tables.').replace('lower-loss QR33 cells','lower-loss QR33 (original QR) cells').replace('parsimonious cells and','parsimonious QR (C2) cells and').replace('bandwidth,72-family','bandwidth, 72-family').replace('40 or12','40 or 12').replace('on277','on 277').replace('All new paths use the prerecord of two independent random streams, fixed seeds and bounded batches.', 'All new paths use two independent random streams with seeds fixed before execution and bounded batches.')
                    if block['html'].startswith('main-article Table'):block['html']='Main-article Table'+block['html'][len('main-article Table'):]
    first_supp_prose=next(b for b in s['sections'][0]['blocks'] if b['type']=='p')
    first_supp_prose['html']+=' In this Supplement, QR33 denotes the original regression and C2 denotes its four-predictor parsimonious specification; neither is a substitute for missing plain KNN.'
    # The numbered section already supplies this heading. Remove only an exact
    # duplicate first subheading; scientific prose, tables and results are intact.
    for sec in d['sections']:
        title=re.sub(r'^\d+\.\s*','',sec['title']).casefold()
        if sec['blocks'] and sec['blocks'][0]['type']=='subheading' and sec['blocks'][0]['text'].casefold()==title:
            sec['blocks']=sec['blocks'][1:]
    # Every changed/new root block is deterministically regenerated. Untouched
    # old generators/source bindings remain intact for the original audit paths.
    bb=bindings()
    for name,doc,old in [('manuscript',d,oldd),('supplement',s,olds)]:
        for si,sec in enumerate(doc['sections']):
            for bi,b in enumerate(sec['blocks']):
                before=old['sections'][si]['blocks'][bi] if si<len(old['sections']) and bi<len(old['sections'][si]['blocks']) else None
                if b.get('_generator','').startswith('v6supp:'):continue
                if before is None or fields(before)!=fields(b):
                    b['_generator']=f'v6:block:{name}:{si}:{bi}';b['_bindings']=deepcopy(bb)
                    for key in ('_source','_definition'):b.pop(key,None)
        if doc['abstract']!=old['abstract']:
            doc['_abstract_generator']='v6:abstract';doc['_abstract_bindings']=deepcopy(bb);doc.pop('_abstract_source',None)
    return d,s

def compose(write_outputs=False):
    docs=deepcopy(_documents(inputs_signature()))
    if write_outputs:
        for name,doc in zip(('manuscript','supplement'),docs):(OUT/(name+'-content.json')).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
    return docs

def generated(key):
    docs=_documents(inputs_signature())
    if key=='abstract':return {'type':'p','html':docs[0]['abstract'],'_generator':'v6:abstract','_bindings':docs[0]['_abstract_bindings']}
    if key.startswith('block:'):
        _,name,si,bi=key.split(':');doc=docs[0 if name=='manuscript' else 1];return deepcopy(doc['sections'][int(si)]['blocks'][int(bi)])
    if key.startswith('figure:'):
        _,name,fi=key.split(':');doc=docs[0 if name=='manuscript' else 1];return {'type':'p','caption':doc['figures'][int(fi)]['caption'],'_generator':'v6:'+key,'_bindings':doc['figures'][int(fi)]['_bindings']}
    raise KeyError(key)

def main():
    docs=compose(write_outputs=True)
    print(json.dumps({'status':'V6_CONTENT_ASSEMBLED','main_sections':len(docs[0]['sections']),'supplement_sections':len(docs[1]['sections']),'original_primaries':'unchanged','new_results':'post-result / exploratory'}))
if __name__=='__main__':main()
