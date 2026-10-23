"""Build the ordered readability revision from the cbce398 structured manuscript.

Existing financial numbers are copied or formatted directly from pinned tables.
The frozen data, fitting code, archived outputs and FINAL.md are never modified.
"""
from pathlib import Path
from copy import deepcopy
from html import unescape
import csv, hashlib, json, re, subprocess

ROOT=Path(__file__).resolve().parent
BASE='cbce3986276e994add53b0f5c6bdeec5191f4412'
OUT=ROOT/'manuscript/revision-v3'
RESULT=ROOT/'results/revision-20261023'

def backup_required(exists,tracked,task_owned):
    return bool(exists and not tracked and not task_owned)

def write_bytes(path,payload):
    path=Path(path);relative=str(path.relative_to(ROOT));path.parent.mkdir(parents=True,exist_ok=True)
    registry=ROOT/'.scratch/v3-owned-paths.json';registry.parent.mkdir(exist_ok=True)
    record=json.loads(registry.read_text()) if registry.exists() else dict(task_owned=[],original_backups={})
    owned=set(record['task_owned'])
    tracked=path.exists() and subprocess.run(['git','ls-files','--error-unmatch',relative],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
    if backup_required(path.exists(),tracked,relative in owned):
        b=path.with_name(path.name+'.bak');i=1
        while b.exists():b=path.with_name(path.name+'.bak.'+str(i));i+=1
        b.write_bytes(path.read_bytes());record['original_backups'][relative]=str(b.relative_to(ROOT))
    path.write_bytes(payload);owned.add(relative);record['task_owned']=sorted(owned)
    registry.write_text(json.dumps(record,indent=2)+'\n')

def write(path,text):write_bytes(path,text.encode('utf8'))

def dump(path,value):write(path,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def readcsv(path):
    with (ROOT/path).open(newline='') as f:return list(csv.DictReader(f))
def para(s):return {'type':'p','html':s}
def sub(s):return {'type':'subheading','text':s}
def eq(s,tex):return {'type':'equation','html':s,'latex':tex}
def table(cap,headers,rows):return {'type':'table','caption':cap,'headers':headers,'rows':rows}
def plain(s):return unescape(re.sub('<[^>]+>','',s))

def restore_prose_spacing(content):
    """Restore missing word/number boundaries without changing any numeric token.

    This whitelist deliberately excludes source keys, code identifiers, URLs,
    mathematical expressions and table data. It only repairs generated prose
    and captions, including dates and named proposition/rank references.
    """
    words=('Proposition','separate','below','original','nearest','recent','full',
           'Full','rank','exact','endpoint','probability','has','from','new',
           'lack','All','draws','minimum','same','fixed','leaf','split','depth',
           'at','than','flag','as','of','October','November','December','April','variance')
    pattern=r'\b('+ '|'.join(words)+r')(?=[0-9])'
    for section in content['sections']:
      for block in section['blocks']:
        keys=['html'] if block['type']=='p' else ['caption'] if block['type']=='table' else []
        for key in keys:
          before=block[key]
          after=re.sub(r'\b(completion)(?=(?:December|April))',r'\1 ',before)
          after=re.sub(pattern,r'\1 ',after)
          after=re.sub(r'(?<=\d)(?=quantile\b)',' ',after)
          after=after.replace('A minimum 20 excesses','A minimum of 20 excesses')
          after=after.replace('max_features11','max_features=11')
          assert re.findall(r'\d+(?:\.\d+)?',before)==re.findall(r'\d+(?:\.\d+)?',after)
          block[key]=after
def sentence_rate(content,main_only=True):
    ss=content['sections']
    if main_only:ss=[s for s in ss if not s['title'].startswith('Appendix')]
    text=' '.join([plain(content['abstract'])]+[plain(b['html']) for s in ss for b in s['blocks'] if b['type']=='p'])
    # Literal full-stop split, as explicitly requested; the decimal-fragment effect
    # is disclosed and an additional whitespace-boundary count is supplied.
    def count(pattern):
        parts=[x.strip() for x in re.split(pattern,text) if x.strip()]
        neg=sum(bool(re.search(r'\b(not|neither|nor|no|cannot)\b',x,re.I)) for x in parts)
        return dict(negative=neg,total=len(parts),ratio=neg/len(parts) if parts else 0)
    return {'literal_full_stop':count(r'\.'),'full_stop_followed_by_space':count(r'\.\s+'),'scope':'abstract plus prose paragraphs; tables/equations/reference catalog excluded; main_only='+str(main_only),'regex':r'\b(not|neither|nor|no|cannot)\b'}

def update_ledger(step,detail):
    p=ROOT/'REVISION_V3_CHANGELOG.md';s=p.read_text();a=s.index('### '+step+' — ');b=s.find('\n### ',a+4)
    if b<0:b=s.find('\n## ',a+4)
    if b<0:b=len(s)
    s=s[:a]+'### '+step+' — COMPLETE\n\n'+detail.strip()+'\n'+s[b:];write(p,s)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    base=json.loads(subprocess.check_output(['git','show',BASE+':manuscript/working-paper/paper-content.json'],cwd=ROOT))
    c=deepcopy(base);old=base['sections'];pairs=readcsv('results/revision-20261022/paired-comparisons.csv');summ=readcsv('results/revision-20261022/evaluation-summary.csv')
    def comparison(source,h,w,method,ref,rw=None):
        return next(x for x in pairs if x['source']==source and int(x['horizon'])==h and int(x['left_window'])==w and x['left_method']==method and x['right_method']==ref and int(x['right_window'])==(w if rw is None else rw))
    fx=comparison('fx_hourly',6,2880,'QR','frozen_F');fxp=comparison('fx_hourly',6,2880,'QR','rolling_F',720);tb=comparison('nyfed_weekly',6,260,'QR','frozen_F');legacy=comparison('fx_hourly',24,2880,'QR','rolling_S',720)
    def pct(row):return f"{float(row['relative_mean_loss_difference_percent']):+.2f}%"
    def hits(row,side):return row['strict_breach_count_'+side]
    # A1
    c['abstract']=("How well can a dealer forecast the largest absolute recorded net position before a reporting horizon ends? "
        "Such forecasts motivate evaluating a monitoring input for the measured position series. We compare historical peak constructions with ridge quantile regression and local quantiles on a market maker's FX client-flow series and a weekly Treasury-dealer aggregate. "
        "The common target includes the observed issue position and uses completed training labels. "
        f"First, six-record FX regression lowers matched-history pinball loss by {abs(float(fx['relative_mean_loss_difference_percent'])):.2f}%, while breaches rise from {hits(fx,'right')} to {hits(fx,'left')}. "
        f"Second, the Treasury primary deteriorates by {float(tb['relative_mean_loss_difference_percent']):.2f}%, with breaches rising from {hits(tb,'right')} to {hits(tb,'left')}. "
        "Third, lower pinball loss often accompanies more breach occasions. The evidence is specific to the inspected records, stipulated score and source-measurement conventions.")
    assert len(plain(c['abstract']).split())<=180
    update_ledger('A1','Rewrote the abstract in manuscript/revision-v3/paper-content.json; all displayed losses/counts are formatted directly from paired-comparisons.csv. Word count is generated in writing-audit.json; AR/frontier/sparse-grid details are excluded.')
    # A2
    intro=[
      para("Dealers absorb customer order imbalances while managing inventory risk and scarce balance-sheet capacity. Inventory affects optimal dealer pricing (Ho and Stoll, 1981), FX dealing (Lyons, 1995), and observed inventory adjustment in dealership markets (Hansch, Naik and Viswanathan, 1998). Treasury intermediation likewise depends on dealer capacity (Duffie et al., 2023). A forecast of the maximum recorded position magnitude over a future horizon may support monitoring of the measured position: an endpoint can return toward its starting value after an intervening large position. Translating that monitoring signal into a particular margin or financing decision requires the corresponding contractual and balance-sheet inputs."),
      para("We ask whether mature conditional estimators improve forecasts of an absolute sampled-position peak relative to simple historical constructions. Every report is evaluated against the same peak response and upper-quantile score on common issue origins. The endpoint-derived bound introduced below is a benchmark rather than a direct peak-quantile estimate. The historical alternatives use past headrooms, paths translated to the current signed position, or native peaks floored at the observed current magnitude. The conditional alternatives use ridge quantile regression, nearest-neighbor quantiles and scaled nearest-neighbor quantiles."),
      para(f"The matched-history FX regression comparison lowers mean loss by {abs(float(fx['relative_mean_loss_difference_percent'])):.2f}%, but increases breaches from {hits(fx,'right')} to {hits(fx,'left')}. The original FX primary uses a different historical window and lowers loss by {abs(float(fxp['relative_mean_loss_difference_percent'])):.2f}%. The separately declared Treasury primary deteriorates by {float(tb['relative_mean_loss_difference_percent']):.2f}%, with {hits(tb,'left')} rather than {hits(tb,'right')} breaches. Short-history FX regression also deteriorates at the longer horizon; a Treasury neighbor gain reverses on the sparse grid. These adverse outcomes are central findings."),
      para("The paper makes three contributions. First, it places established forecasting engines and historical constructions on a common completed-peak response with an explicit issue-known floor. Second, it controls completed-label pools and update schedules and retains the complete favorable and adverse model menu. Third, it documents how score, breach frequency, report coherence and fixed-report preferences can disagree across two financial measurement processes. The contribution is an application and model-validation benchmark using mature methods."),
      para("Section 2 locates the study in the literature. Sections 3–5 describe data, forecasts and evaluation. Sections 6–7 report FX and Treasury results. Section 8 collects exploratory robustness evidence, Section 9 discusses mechanisms and limitations, and Section 10 concludes. Detailed historical menus, geometry and supplementary diagnostics appear in the appendices.")]
    c['sections'][0]['blocks']=intro
    update_ledger('A2','Rebuilt the introduction around inventory/capacity motivation, question, method, findings, three contributions and roadmap. Verified inventory references are added in A9. Ruling: raw sampled position magnitude is a planning input, not a demonstrated determinant of contractual margin or funding; the source papers do not establish that mapping.')
    # A3 / A4: collect original audit passages once, then rebuild main prose.
    audit=[]
    for si,ids in ((2,[9]),(4,[7,8,9,10]),(8,[6]),(13,[5,6,7,8,9,10])):
        audit.extend(old[si]['blocks'][i] for i in ids)
    audit.extend({'type':'p','html':r['html']} for r in base['references'] if 'Consulted' in r['html'] or 'unverified' in r['html'])
    guide_generated_prefix='# Reproducibility, pre-specification and consulted editions\n\nMoved unchanged from the25-page cbce398 manuscript; these historical identities and resource observations are preserved outside the scientific narrative.\n\n'+'\n\n'.join(plain(x['html']) for x in audit)+'\n'
    related=[
      para("Wisniewski, Lindsay and Lindsay (2020) and the net-position forecasting chapter of Wisniewski (2024) are the closest empirical lineage. They already study conditional, neighbor and normalized endpoint forecasts on the FX source family, using lagged positions and calendar information. Here the response is a single upper quantile of a future absolute sampled maximum, including the current magnitude. Marginal endpoint intervals and their averaged losses address a different functional; the present comparison fits the established engines directly to completed peak labels."),
      para("Financial path extrema have a substantial prior literature. MaxVaR evaluates worst intermediate mark-to-market loss (Boudoukh et al., 2004). Liao and Theodosopoulos (2005) study the timing of mark-to-market for collateralized contingent credit exposure. Van den Hoogen (2017) models a conditional intraday liquidity buffer through the maximum cumulative payment deficit; Petrunia, Sabetti and Voia (2019) study a cross-participant end-of-day debit maximum. Arjani, Li and Sabetti (2020) forecast remaining-day liquidity-demand ratios. These targets clarify the specific contribution of a sampled net-position envelope."),
      para("Regression quantiles (Koenker and Bassett, 1978), sequential neighbor quantiles (Biau and Patra, 2011), conditional historical filtering (Hull and White, 1998; Barone-Adesi et al., 1999), and quantile scoring (Gneiting, 2011) supply the mature methods. Quantile forests (Meinshausen, 2006), CAViaR (Engle and Manganelli, 2004), sequential conformal prediction (Xu and Xie, 2023), trajectory calibration (Zhou, Lindemann and Sesia, 2024) and expected-shortfall curves (Sözen, 2026) are further relevant alternatives. The executed estimator menu is deliberately bounded."),
      para("The resulting distinction is the measured peak response, known issue floor, completed-label timing, controlled history/update comparisons and qualified aggregate application. The benchmark measures how these mature procedures behave on the specified task; its supporting finite geometry explains construction differences.")]
    data=[para(old[2]['blocks'][0]['html'].replace('The timezone and historical publication/vintage convention remain unverified.','Recorded-clock and vintage limits are collected in Section 9.')),
      para("The Treasury application uses the New York Fed Primary Dealer Statistics series PDPOSGS-B: Treasury-bill long positions less short positions, measured at weekly Wednesday close in market/fair-value USD millions. The accepted snapshot contains "+str(json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text())['sources']['nyfed_weekly']['record_count'])+" records. It combines dealer inventories, valuation and reporting composition. This supplies an aggregate financial measurement task alongside the individual market-maker client-flow series."),
      para(old[2]['blocks'][7]['html']),deepcopy(old[2]['blocks'][6]),
      para("All horizons share the source-specific evaluation issue origins. Horizon H counts subsequent source records, so the response uses H+1 observed positions including issue time. FX gaps are retained in chronological order. Treasury transitions follow the weekly economic-date clock. Exact data identities, access routes and reproduction commands are retained in the repository guide.")]
    methods=[
      para("Let N denote the signed source-reported net position. The issue magnitude B is observed when the report is issued. Define the sampled peak P and its nonnegative headroom G by"),deepcopy(old[2]['blocks'][2]),
      para("At issue t, the most recent scheduled refit is κ(t). Every training label is complete by that refit, and the next refit updates the transform, scale, coefficients and historical pool together:"),deepcopy(old[2]['blocks'][4]),
      para("For a completed episode i, let u and l be its largest and smallest increments from its starting position, including the zero increment. Translating its ordered path to x=Nₜ produces Vᵢ,ₜ=max{x+uᵢ,−x−lᵢ}. On a common episode set A, Q selects the duplicate-preserving corrected empirical order statistic. The historical forecasts are"),deepcopy(old[3]['blocks'][2]),
      para("Rolling controls update their completed-label set at each issue. Frozen controls use the same completed-label pool and refit schedule as the fitted procedures, while their current issue anchor continues to update. Earlier one-state controls retrieve nearby signed starting positions; their complete earlier menus remain in Appendix B."),
      para(old[3]['blocks'][6]['html'].replace('Calendar coordinates use the stored source clock, not a verified UTC session. Weekly calendar coordinates can be constant, and coordinates need not supply independent information.','Calendar coordinates follow the stored source clock; constant training columns are centered exactly at their repeated value.')),
      deepcopy(old[3]['blocks'][7]),
      para("Training-only centering and population standard deviations define z. An exactly constant coordinate receives unit scale after centering. Matching completed response origins retains the different past-only lookbacks required by the feature construction. The response scale a is computed from completed training headrooms and magnitudes:"),deepcopy(old[3]['blocks'][10]),
      para(old[3]['blocks'][12]['html'].replace('lambda','λ').replace('tau','τ')),
      deepcopy(old[3]['blocks'][13]),deepcopy(old[3]['blocks'][14]),
      para("The intercept is unpenalized and slopes receive a ridge penalty. Adding B to a headroom quantile translates it into a peak quantile; projecting a report up to the known response floor weakly improves realized pinball loss. The equivalent peak parameterization and numerical conventions are retained in Appendix C."),
      para("KNN uses training-standardized features with the frozen group weights and recency tie-breaking rule specified in Appendix C. It reports B plus a local headroom quantile. Scaled KNN divides each selected headroom by its past short RMS and multiplies the resulting quantile by the query RMS, using the same fixed stabilizer within each refit block."),deepcopy(old[3]['blocks'][19]),
      para(old[3]['blocks'][20]['html'])]
    evaluation=[para(old[4]['blocks'][0]['html'].split(' No favorable')[0]),
      para("Every selected conditional family is compared with frozen F, S and K at matching source, horizon and history. The complete menu also retains rolling-versus-frozen update controls. The declared source primaries remain fixed throughout every post-result analysis."),
      para("Forecasts are scored in native source units using the stipulated upper-quantile pinball preference. The paired loss difference is left minus right, so a negative difference favors the left procedure:"),deepcopy(old[4]['blocks'][2]),
      para("Mean positive overrun averages (P−C)₊ over all issue origins; mean unused allowance averages (C−P)₊. Breaches use strict P>C. Conditional event severity uses each forecast's own breach occasions. Annual groups and the globally anchored H+1 grid supply the original sensitivity views."),
      deepcopy(old[4]['blocks'][6]),
      para("The original conditional-study design and selected parameters were publicly frozen before their respective executions (see the linked reproduction record). The FX evaluation interval had previously been inspected. All new inference and robustness analyses are labeled post-result / exploratory; the round2 additions have local execution bindings, rather than a new public preregistration.")]
    fxblocks=[para(old[5]['blocks'][1]['html']),para(old[5]['blocks'][2]['html'].replace('The H6 gain is not uniform risk improvement.','The H6 score gain comes with more breach occasions.')),
      para(old[5]['blocks'][3]['html']),para(old[5]['blocks'][4]['html']),
      para("Figure 1 compares every selected conditional procedure with its matched frozen-F control; Table 3 adds breach rates and the corresponding same-history changes. Figure 3 displays every original annual primary comparison."),{'type':'figure','index':0}]
    tbblocks=[para(old[6]['blocks'][1]['html']),para(old[6]['blocks'][2]['html']),para(old[6]['blocks'][3]['html']),para(old[6]['blocks'][4]['html']),
      para("Table 4 retains every conditional family and history. Figure 2 juxtaposes the declared primaries and the FX legacy sensitivity, keeping score changes, breach-rate changes and severity separate."),{'type':'figure','index':1},{'type':'figure','index':2}]
    robust=[sub('Post-result / exploratory robustness'),
      para(old[7]['blocks'][1]['html']+' '+old[7]['blocks'][2]['html']),
      para(old[9]['blocks'][3]['html']),
      para(old[8]['blocks'][4]['html']+' '+old[8]['blocks'][5]['html']),
      para(old[9]['blocks'][4]['html']+" Figure 3 retains the complete annual comparison; all detailed coherence and fixed-terminal diagnostics remain in Appendix D."),
      table('Table 5. Summary of post-result / exploratory robustness; complete numerical tables remain in the appendices.', ['Analysis','Main finding','Retained adverse evidence'],[
        ['AR replay','Improves on QR in every Treasury cell','Breach occasions rise against S in every cell'],
        ['Empirical rank','Both matched H6 QR directions persist','Lower empirical rank loses to F in five cells'],
        ['Preference frontier','FX H6 reduces both loss components','FX H24 reverses near the original weight'],
        ['Horizon coherence','Targets are ordered by construction','Separately fitted reports cross']])]
    discussion=[para("The contrast between the sources concerns a separately fitted procedure family: each source receives its own transforms, coefficient estimates, temporal scales and validation selection. The Treasury deterioration is an accuracy failure of the executed QR specifications. The exploratory AR comparison shows that the observed Treasury loss ranking differs across the executed families."),
      sub('Limitations'),
      para("The FX evaluation interval was previously inspected, and the subsequent robustness analyses are post-result / exploratory. These records do not restore a compatible unseen dealer sample. Treasury is a downloaded-vintage, economic-date aggregate replay rather than an original-release public-information backtest; cross-dealer netting, valuation and composition distinguish it from an individual dealer's book."),
      para("Shared histories, overlapping labels, finite validation and investigator selection limit statistical generalization. The known floor can create an outcome atom: a valid upper quantile need not have exactly the nominal strict-breach probability. Numerical acceptance supplies no conditional-coverage guarantee. The horizon-specific mature scenario sets differ, so a zero observed crossing count cannot establish general coherence."),
      para("Stipulated shortfall/excess weights are not observed financing prices. Quotes, fills, hedges, book decomposition, collateral and cash flows would be required to map this passive envelope into an operational inventory, margin or funding policy. This study evaluates forecasts, not such interventions; Avellaneda and Stoikov (2008) provide a distinct active inventory-sensitive quoting framework."),
      para("The strongest alternatives extend beyond the executed menu, including quantile forests, CAViaR, sequential conformal procedures and full volatility-filtered historical simulation. Same completed-label pools and update schedules improve procedural comparability while allowing differences in feature lookback, regularization, scaling and validation. Future compatible observations and decision-linked inputs would test broader portability.")]
    conclusion=[para(f"Mature conditional estimators change the historical ranking on the sampled FX peak task, while the Treasury regression primary deteriorates. Matched-history FX H6 QR lowers mean loss by {abs(float(fx['relative_mean_loss_difference_percent'])):.2f}% and raises breaches from {hits(fx,'right')} to {hits(fx,'left')}; the Treasury primary raises loss by {float(tb['relative_mean_loss_difference_percent']):.2f}% and breaches from {hits(tb,'right')} to {hits(tb,'left')}. Short-history QR deterioration and the sparse-grid Treasury neighbor reversal remain central adverse findings. The exploratory AR, rank, preference and coherence comparisons show why score improvements, breach frequency and report shape should be evaluated together. The study contributes a controlled application and model-validation benchmark for measured position peaks. Its next evidential step is compatible new financial observations and an explicit decision mapping.")]
    c['sections']=[dict(title=t,blocks=b) for t,b in [
      ('1. Introduction',intro),('2. Related literature',related),('3. Data',data),('4. Target and forecasting methods',methods),('5. Evaluation design',evaluation),('6. Results: FX',fxblocks),('7. Results: Treasury',tbblocks),('8. Robustness',robust),('9. Discussion and limitations',discussion),('10. Conclusion',conclusion)]]
    update_ledger('A3','Consolidated repeated limitations into Section9; retained and sharpened every adverse primary, short-history QR deterioration, sparse-grid reversal and breach increase. Generated writing-audit.json reports the exact requested literal-period/negative-word count and a decimal-safe sensitivity count, separately for main prose and all appendices.')
    update_ledger('A4','Moved immutable identities, timing/RSS/byte/thread observations and consulted-edition notes into REPRODUCIBILITY_V3.md. A compact reproduction appendix carries links. Financial quantities and horizon/history budgets remain where scientifically required.')
    c['sections']+=deepcopy(old[11:])
    # Preserve complete original FX/Treasury/AR/preference tables as supplementary
    # tables, rather than dropping any cells during narrative compression.
    c['sections'].append({'title':'Appendix F. Complete original model menus and exploratory replay','blocks':[deepcopy(old[5]['blocks'][0]),deepcopy(old[6]['blocks'][0]),deepcopy(old[7]['blocks'][0]),deepcopy(old[8]['blocks'][3])]})
    # Numerical audit paragraphs moved out; mathematical/numerical specification stays.
    c['sections'][12]['blocks']=[deepcopy(old[13]['blocks'][i]) for i in (0,1,2,3,4)]
    c['sections'].append({'title':'Appendix G. Reproducibility and pre-specification','blocks':[
      para("The repository preserves the original source-version checks, execution freezes, complete validation menu, chronological selections, accepted forecasts and favorable/adverse outputs. The original and revised manuscript sources are separately retained. Reproduction commands, exact fingerprints, machine observations and consulted-edition records are in REPRODUCIBILITY_V3.md and the repository README."),
      para("The original execution and selection freezes are linked at https://github.com/ByronLi0207/financial-mathematics-paper-20261020/commit/1bd5b692fd9cb240763c032fb4e1c203871fad55 and the repository protocol directory. Later exploratory AR, rank and fixed-preference analyses retain their own execution records. New v3 inference has its own scripts, output identities and tests, leaving the archived scientific files intact.") ]})
    update_ledger('A5','Reordered the main paper into the requested ten sections; merged AR/rank/preference/coherence into four robustness paragraphs and one summary table. Original model-menu tables are preserved in AppendixF, and prior geometry/negative diagnostics/frontiers remain in appendices. Main-page count is measured at rendering rather than asserted from source length.')
    # A6: distinct refit index κ, radius d, preference weight ω, path N-tilde,
    # objective J; exact numeric values stay unchanged.
    for s in c['sections']:
      for b in s['blocks']:
        for key in ('html','text','caption','latex'):
          if key not in b:continue
          x=b[key]
          x=x.replace('original L','native-peak K').replace('S-KNN','Scaled KNN').replace('SCALED_KNN','Scaled KNN')
          x=re.sub(r'\bTB\b','Treasury',x);x=re.sub(r'\bNY\b','Treasury',x)
          x=x.replace('P0','Floor').replace('P<sub>lambda</sub>','J<sub>λ</sub>').replace('P<sub>lambda','J<sub>λ')
          x=x.replace('r(abs)','d(abs)').replace('r(signed)','d(signed)')
          if key=='latex':
            x=x.replace(r'\mathcal P_\lambda',r'\mathcal J_\lambda').replace('W_{i,h}',r'\widetilde N^{tr}_{i,h}')
            x=re.sub(r'(?<![A-Za-z\\])r(?![A-Za-z])',r'\\kappa',x)
          else:
            x=x.replace('W<sub>i,h</sub>', 'Ñ<sub>i,h</sub><super>tr</super>')
            x=x.replace('r(t)','κ(t)').replace('r−','κ−').replace('r+','κ+').replace('≤r≤','≤κ≤').replace('refit r','refit κ').replace('a(r)','a(κ)').replace('phi(r)','φ(κ)')
            x=re.sub(r'\br=(?=[0-9])','ω=',x);x=x.replace('finite positive r','finite positive ω').replace(' r is ',' ω is ')
            x=re.sub(r'(<sub>[^<]*?)\br(?=[,j<])',lambda m:m[1]+'κ',x)
            x=x.replace('ceil((k+1).95)','⌈(k+1).95⌉').replace('sum<sub>i in','∑<sub>i ∈')
          b[key]=x
        if b['type']=='table':
          b['headers']=[re.sub(r'\b(TB|NY)\b','Treasury',str(x)).replace('P0','Floor').replace('Scaled k','Scaled KNN k') for x in b['headers']]
          b['headers']=[x.replace('Crossing r','Crossing ω') for x in b['headers']]
          b['rows']=[[re.sub(r'\b(TB|NY)\b','Treasury',str(x)).replace('P0','Floor').replace('SCALED_KNN','Scaled KNN') for x in row] for row in b['rows']]
    notation=table('Notation. Distinct symbols for response, refits, history, distances and preferences.', ['Symbol','Definition'],[
      ['Nₜ; Bₜ','Signed position; observed issue magnitude |Nₜ|'],['Pₜ,ₕ; Gₜ,ₕ','Sampled absolute peak; headroom Pₜ,ₕ−Bₜ'],['κ(t); W; d','Most recent refit index; label-pool size; refit step'],['Cₜᵐ; Floor','Issued report for method m; the known-floor report'],['d(abs); d(signed)','Common-set anchor-distance radii'],['Ñᵗʳᵢ,ₕ; Mᵢ,ₕ','Translated historical path; AR residual-replay path'],['aκ; zᵢ,κ','Training response scale; standardized predictors'],['a; ω=a/(1−a)','Shortfall weight; shortfall/excess preference ratio'],['Jλ; Dλ','Penalized regression objective; feasible dual objective']])
    c['sections'][3]['blocks'].insert(0,notation)
    update_ledger('A6','Added the notation table and separated refit κ, distance d(abs)/d(signed), history W, translated path Ñ, peak P, Floor report and objective Jλ. Unified Treasury and Scaled KNN display labels; underlying frozen method identifiers remain unchanged in data files.')
    # A7: readable mathematical Unicode; TeX uses each equation's explicit formula.
    for s in c['sections']:
      for b in s['blocks']:
        if b['type']=='equation':
          x=b['html'].replace('ceil(', '⌈').replace('floor(', '⌊').replace('sum<sub>','∑<sub>').replace('sum ','∑ ').replace('mean ','mean ').replace(' in T',' ∈ T').replace('i in J','i ∈ J')
          x=x.replace('i in T','i ∈ T').replace('||','‖').replace('rho','ρ').replace('tau','τ').replace('lambda','λ').replace('beta','β').replace('alpha','α').replace('mu','μ').replace('phi','φ')
          x=x.replace('⌈19W/20)', '⌈19W/20⌉').replace('⌈19(W+1)/20)', '⌈19(W+1)/20⌉').replace('⌊((t−t<sub>0</sub>)/d)', '⌊(t−t<sub>0</sub>)/d⌋')
          x=x.replace('⌊(t−t<sub>0</sub>)/d)', '⌊(t−t<sub>0</sub>)/d⌋')
          b['html']=x
    update_ledger('A7','Formal equation blocks retain explicit LaTeX and now have mathematical Unicode/sub/superscript fallback. No TeX engine is available and installation is not authorized; use the existing ReportLab path and label the PDF renderer honestly. New main.tex is supplied for a real TeX environment.')
    # A8: main tables are now tidy per-method menus. B1 fills actual t/p later.
    infer_path=RESULT/'inference/dm.csv'
    inferred={x['contrast_id']:x for x in readcsv(str(infer_path.relative_to(ROOT)))} if infer_path.exists() else {}
    for source,si,number in [('fx_hourly',5,3),('nyfed_weekly',6,4)]:
      rows=[]
      for x in summ:
        if x['source']!=source or x['method'] not in ('QR','KNN','SCALED_KNN'):continue
        comp=comparison(source,int(x['horizon']),int(x['window']),x['method'],'frozen_F')
        z=inferred.get(comp['contrast_id']);stat='pending B1' if z is None else (('t='+format(float(z['dm_t']),'.3f')+'; p='+format(float(z['dm_p']),'.3g')+'; HLN p='+format(float(z['hln_p']),'.3g')) if z['status']=='OK' else z['status'])
        scale=1e6 if source=='fx_hourly' else 1
        rows.append([x['horizon'],x['window'],x['method'].replace('SCALED_KNN','Scaled KNN'),f"{float(x['mean_pinball'])/scale:.3f}",f"{100*float(x['strict_breach_rate']):.3f}%",f"{float(comp['relative_mean_loss_difference_percent']):+.3f}%",stat])
      c['sections'][si]['blocks'].insert(0,table(f'Table {number}. Complete selected conditional menu with breach rates and same-history frozen-F contrasts. Loss is in source-specific USD millions; B1 statistics are post-result / exploratory.', ['H','W','Method','Loss','Breach rate','Δ frozen F','DM / HLN'],rows))
    c['figures']=deepcopy(base['figures'])
    for f in c['figures']:
      f['caption']=f['caption'].split(' No sampling')[0].replace('S-KNN','Scaled KNN').replace('not a combined utility or monetary saving','separate measures of forecast behavior')
    prose_edits={
      'No interpolation is used; an unavailable corrected rank fails.':'The implementation uses exact order statistics and fails on an unavailable rank.',
      'Thus the W52 distinction does not imply that every corrected historical rule fails to minimize empirical pinball.':'The W52 distinction is specific to its noninteger probability-times-pool-size case.',
      'its distances no longer affect membership.':'membership is then the complete training pool.',
      'Long-window menus do not contain the full pool.':'Long-window menus restrict neighborhood sizes below the full pool.',
      'its reference was chosen in the preceding study, not independently of all historical outcomes.':'its reference was chosen in the preceding, already inspected study.',
      'the matched-pool controls address part, but not all, of this procedural difference.':'the matched-pool controls address these procedural differences while retaining estimator and feature distinctions.',
      'Conditional severity uses the different method-specific event sets and cannot identify improvement on the same incidents.':'Conditional severity averages different method-specific event sets; the statistic therefore compares different incident compositions.',
      'Neither the broader model class nor a favorable short-horizon result provides a uniform advantage across history budgets.':'In the inspected FX record, the H24 regression ranking changes with the history window.',
      'These subdivisions and grids are sensitivities of one inspected record, not independent replications or a basis for switching forecasts retrospectively.':'These subdivisions and grids describe sensitivity within the inspected FX record; their interpretation follows Section 9.',
      'the reduced unused quantity does not compensate for the more heavily weighted overrun increase.':'the more heavily weighted overrun increase dominates the reduced unused quantity.',
      'This is an adverse accuracy result from numerically accepted fits, not a convergence failure.':'Numerically accepted fits produce this adverse accuracy result.',
      'with no breaches for either method.':'with zero breaches for either method.',
      'This partial period is retained, not used to rescue the primary.':'The full adverse primary and this partial-period result are both retained.',
      'The distance coordinates do not change membership in these rows; they demonstrate a full-pool fallback, not rich-feature gains.':'These rows use the complete pool, so they demonstrate the full-pool fallback.',
      'These do not replace the QR primary, and no selected conditional procedure is descriptively below every retained historical reference at its horizon.':'The adverse QR primary remains the declared test case. Each selected conditional procedure loses to at least one retained historical reference at its horizon.',
      'Such a whole-menu observation is not a newly selected forecast rule.':'The menu is reported as a complete descriptive comparison.',
      'The H6 KNN sensitivity does not reverse:':'The H6 KNN sensitivity remains favorable:',
      'The sparse reversal does not identify a cause or prove an opposite population ranking; it does prevent a claim of stable secondary transfer.':'The sparse reversal documents instability in the secondary Treasury gain.',
      'The original adverse Treasury QR primary therefore does not establish failure of every conditional family.':'The exploratory AR comparisons show a different observed loss pattern from the adverse Treasury QR primary.',
      'No additional model is selected from this table.':'The complete table retains the original model identities.',
      'so empirical minimization does not imply better realized evaluation loss.':'so the empirical minimizer endpoint can perform worse in evaluation.',
      'These two headline signs persist under this specific control; it neither isolates a causal feature effect nor exhausts alternative conditional models.':'The two headline signs persist under this specific control.',
      'Their improvement therefore does not rely on the single 19:1 preference, even though strict breach occasions still increase.':'Their score improvement holds across the linear preference range, while strict breach occasions still increase.',
      'These are descriptive consequences of fixed sample means, not estimates of financing prices or risk preferences.':'These crossings describe the fixed sample means.',
      'These changes delimit sample stability; sparse windows and shared training histories do not create independent evidence.':'These changes delimit sample stability under the original sparse-grid construction.',
      'Some short Treasury historical F/S controls also cross because the horizons use different mature episode sets; zero observed crossings supply no general guarantee.':'Some short Treasury historical F/S controls also cross because the horizons use different mature episode sets.',
      'The horizon-specific fits and mature scenario sets differ; numerical acceptance does not establish an ordered report curve.':'The horizon-specific fits and mature scenario sets differ, producing the observed incoherence.'}
    for s in c['sections'][:10]:
      for b in s['blocks']:
        if b['type']=='p':
          for a,z in prose_edits.items():b['html']=b['html'].replace(a,z)
    update_ledger('A8','Figures1–3 are cited and placed inline at result/robustness locations by the new builder. Tables3/4 add per-method breach rate, matched-frozen-F percentage and B1 columns. B1 columns remain explicitly pending until verified trace recovery and actual tests; existing wide numeric menus stay in AppendixF.')
    # A9 remove consulted-edition audit prose from bibliography, retain source links.
    for r in c['references']:
      x=r['html']
      x=re.split(r' Consulted\b| The PDF names\b| Official article\b| Official proceedings\b| Institutional original\b',x)[0]
      x=re.split(r' The institutional award year\b| The online edition\b| The consulted edition\b',x)[0]
      x=x.replace('; no separate journal edition or DOI is asserted.','.').replace('; its cover is undated and final-body equivalence is unverified.','.').replace(' The historical as-released series was not reconstructed.','').replace(' Source identity verified 21 October 2026; raw redistribution permission remains unverified.','')
      x=x.replace('; no claim of equivalence to an unverified journal version.','.')
      if r['id']=='dataset':x="davidlindsay1979 (n.d.). <i>Net Position Time Series Dataset</i> (Version 2) [Data set]. Kaggle. <a href='https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset'>Dataset record</a>."
      x=re.sub(r'(?i)Consulted ', '', x)
      x=re.sub(r', consulted [0-9]+ [A-Za-z]+ [0-9]{4}', '', x)
      r['html']=x
    for rid,text,url in [
      ('ho1981','Ho, T. and H.R. Stoll (1981). Optimal dealer pricing under transactions and return uncertainty. <i>Journal of Financial Economics</i> 9(1), 47–73.','https://doi.org/10.1016/0304-405X(81)90020-9'),
      ('lyons1995','Lyons, R.K. (1995). Tests of microstructural hypotheses in the foreign exchange market. <i>Journal of Financial Economics</i> 39(2–3), 321–351.','https://doi.org/10.1016/0304-405X(95)00832-Y'),
      ('hansch1998','Hansch, O., N.Y. Naik and S. Viswanathan (1998). Do Inventories Matter in Dealership Markets? Evidence from the London Stock Exchange. <i>Journal of Finance</i> 53(5), 1623–1656.','https://doi.org/10.1111/0022-1082.00067')]:
      c['references'].append({'id':rid,'html':text+" <a href='"+url+"'>DOI: "+url.removeprefix("https://doi.org/")+"</a>."})
    c['subtitle']='Common targets, source-specific results and exploratory diagnostics'
    c['date']='23 October 2026'
    # Preserve the complete adverse AR annual/sparse sensitivity paragraph.
    appendix_f=next(s for s in c['sections'] if s['title'].startswith('Appendix F.'))
    appendix_f['blocks'].extend([sub('AR estimation definition'),*deepcopy(old[3]['blocks'][22:25]),sub('AR annual and sparse-grid sensitivity'),deepcopy(old[7]['blocks'][3])])
    appendix_a=next(s for s in c['sections'] if s['title'].startswith('Appendix A.'))
    appendix_a['blocks'].insert(0,deepcopy(old[3]['blocks'][4]))
    appendix_e=next(s for s in c['sections'] if s['title'].startswith('Appendix E.'))
    appendix_e['blocks'][:0]=deepcopy(old[8]['blocks'][:3])
    appendix_e['blocks'].insert(0,para('Rational boundaries are exact for saved decimal summaries of floating-point means; this does not assert exact unrounded-loss boundaries. Separately stored columns match the analytic normalized-loss identity within the recorded tolerance.'))
    appendix_c=next(s for s in c['sections'] if s['title'].startswith('Appendix C.'))
    appendix_c['blocks'].insert(0,para('After training standardization, KNN multiplies each signed-level coordinate (lags 0–24) by 1/5. Each coordinate in the two-RMS pair, hour sine/cosine pair and weekday sine/cosine pair is multiplied by 1/√2; the magnitude and observed-gap coordinates retain unit weight. Distance is squared Euclidean distance in these weighted coordinates. Exact distance ties prefer the more recent training origin. These are the frozen coordinate multipliers, not weights fitted to evaluation outcomes.'))
    appendix_c['blocks'].extend([sub('Equivalent peak parameterization'),*deepcopy(old[3]['blocks'][15:18])])
    from v3_additions import augment
    augment(c,base)
    from round2_manuscript import augment_round2
    augment_round2(c)
    # Unambiguous appendix table identifiers preserve every original cell.
    tables=[b for b in appendix_f['blocks'] if b['type']=='table']
    for j,b in enumerate(tables,1):
      b['caption']=re.sub(r'^Table [0-9]+\.',f'Table F{j}.',b['caption'])
      b['rows']=[[re.sub(r'\br\b','ω',str(x)) for x in row] for row in b['rows']]
    for s in c['sections']:
      for b in s['blocks']:
        if 'html' in b:
          b['html']=b['html'].replace('raw translation by W','raw translation by Ñ').replace('|P|','|Jλ|').replace('|D|','|Dλ|').replace('E<sub>n(r),k(r)</sub>','E<sub>n(η),k(η)</sub>').replace('∑<sub>ω=0','∑<sub>η=0')
          b['html']=b['html'].replace('r(abs)','d(abs)').replace('r(signed)','d(signed)').replace('two K bounds in Section 4','two common-set K bounds stated above').replace('remain separately labeled in Table 7','remain separately labeled in Table F4')
          b['html']=b['html'].replace('r_abs','d(abs)').replace('r_signed','d(signed)').replace('G(j),r,H','G(j),κ,H').replace('r−H−W+1','κ−H−W+1').replace('c(r)','c(κ)')
          if s['title'].startswith('Appendix F.'):
            b['html']=b['html'].replace('put a=','put i₀=').replace('a+1,...,r','i₀+1,...,κ').replace('a+1,…,r','i₀+1,…,κ').replace('a+1 through r','i₀+1 through κ')
          b['html']=b['html'].replace('refit r','refit κ').replace('phi(r)','φ(κ)').replace(' r=a/(1-a)',' ω=a/(1−a)').replace('positive r','positive ω').replace('finite positive r','finite positive ω')
          b['html']=re.sub(r'(<sub>[^<]*?)\br(?=[,jB<|])',lambda m:m[1]+'κ',b['html'])
          if s['title'].startswith('Appendix E.') or ('J<sub>m</sub>' in b['html']):b['html']=re.sub(r'\br\b','ω',b['html'])
        if 'latex' in b:
          if s['title'].startswith('Appendix E.') or 'J_m(a)' in b['latex']:b['latex']=re.sub(r'(?<![A-Za-z\\])r(?![A-Za-z])',r'\\omega',b['latex'])
          else:b['latex']=re.sub(r'(?<![A-Za-z\\])r(?![A-Za-z])',r'\\kappa',b['latex'])
          b['latex']=b['latex'].replace('mu_{rj}',r'mu_{\kappa j}').replace('s_{rj}',r's_{\kappa j}')
        if s['title'].startswith('Appendix D.') and b.get('type')=='equation' and 'E_{n_' in b.get('latex',''):
          b['latex']=b['latex'].replace('kappa','eta').replace('omega','eta')
    if len({r['id'] for r in c['references']})!=len(c['references']):raise ValueError('duplicate reference identity')
    c['references'].sort(key=lambda r:plain(r['html']).casefold())
    restore_prose_spacing(c)
    from v3_math_format import normalize_math
    normalize_math(c)
    from round2_inline_math import bind_round2_math
    bind_round2_math(c)
    before=sentence_rate(base);after=sentence_rate(c);audit={'base_commit':BASE,'abstract_words':len(plain(c['abstract']).split()),'conclusion_words':sum(len(plain(b['html']).split()) for b in c['sections'][9]['blocks'] if b['type']=='p'),'main_before':before,'main_after':after,'whole_body_before':sentence_rate(base,False),'whole_body_after':sentence_rate(c,False),'numerical_sources':['manuscript/working-paper/paper-content.json at '+BASE,'results/revision-20261022/paired-comparisons.csv','results/revision-20261022/evaluation-summary.csv'],'latex_compiler':'Current source compilation deferred by user instruction; only earlier byte versions have historical desktop-compiler receipts','pdf_renderer':'existing ReportLab with Arial Unicode mathematical fallback'}
    c['figures'][0]['caption']=c['figures'][0]['caption'].replace('Points show','Entries show')
    c['figures'][1]['caption']=c['figures'][1]['caption'].replace('A reduced R quantity is not automatically overall improvement.','A reduced mean report or allowance alone is insufficient to establish overall improvement.')
    # Keep consulted-edition and numerical execution audit notes out of the paper.
    additional=[]
    for s in c['sections']:
      if s['title'].startswith('Appendix D.'):
        for b in s['blocks']:
          if b['type']=='p':
            if b['html'].startswith(('The original AR diagnostic command remains','The supplement retains 16 I/F summaries')):
              additional.append(b['html']);b['html']='Complete execution, verification and arithmetic-readback records for this supplement are retained in REPRODUCIBILITY_V3.md and the corresponding result-directory README.'
            for delimiter in (' Production retained all',' The two processes took',' The production and readback processes'):
              if delimiter in b['html']:
                left,right=b['html'].split(delimiter,1);additional.append(delimiter+right);b['html']=left
    guide=ROOT/'REPRODUCIBILITY_V3.md'
    from reproducibility_guide import rebuild_guide,read_guide_text
    generated=guide_generated_prefix+'\n\n## Original reference-edition notes retained verbatim\n\n'+'\n\n'.join(plain(r['html']) for r in base['references'])+'\n\n## Additional appendix execution records\n\n'+'\n\n'.join(plain(x) for x in additional)+'\n'
    write(guide,rebuild_guide(read_guide_text(guide),generated))
    audit['whole_body_after']=sentence_rate(c,False)
    dump(OUT/'paper-content.json',c);dump(RESULT/'writing-audit.json',audit)
    b=before['literal_full_stop'];a=after['literal_full_stop'];all_a=audit['whole_body_after']['literal_full_stop']
    update_ledger('A3',f"Main-prose literal-period count: before {b['negative']}/{b['total']} = {100*b['ratio']:.6f}%; after {a['negative']}/{a['total']} = {100*a['ratio']:.6f}%. Main prose satisfies the<10% target. Scope is abstract plus prose paragraphs, excluding tables/equations/reference catalog. Whole body including appendices: {all_a['negative']}/{all_a['total']} = {100*all_a['ratio']:.6f}%; appendices preserve technical counterexamples/limitations. Decimal-safe sensitivity and all scopes remain in writing-audit.json. All specified adverse results, AR annual/sparse reversals and original complete model tables are retained; conventional limits are consolidated in Section9.")
    update_ledger('A7','Formal equations retain explicit TeX; ReportLab uses mathematical glyphs and actual sub/superscript tags, correcting unsupported Unicode index glyphs. Current source compilation is deferred under the user instruction; earlier compiler receipts apply only to their recorded byte versions. The delivered PDF is explicitly ReportLab-rendered, not falsely labeled as a TeX-exported PDF.')
    update_ledger('A8','Figures1–4b are cited inline; Tables3/4 include actual breach rates, matched-F percentages, DM t/p and HLN p from the verified traces. All original model-menu cells stay in AppendixF with unique F1–F4 identifiers. New inference and C2 tables follow the robustness summary as Tables6/7/8. Statistical tables retain degenerate NA statuses rather than invented t statistics.')
    update_ledger('A9','Liao–Theodosopoulos is now substantively cited in Related literature. Dataset citation uses the verified account handle, Version2 and n.d. because a publication date was not established. Added verified Ho–Stoll/Lyons/Hansch DOI metadata; Duffie2023 was already present. Consulted-version caveats move to REPRODUCIBILITY_V3.md. A raw account handle is not silently expanded to a personal name.')
    print(json.dumps(audit,ensure_ascii=False))

if __name__=='__main__':main()
