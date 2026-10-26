"""Deterministic reader tables from public v6 aggregates; no private inputs.

Only public JSON receipts and frozen prose protocols are consumed. Every block
and figure caption has a stable regeneration key and current input fingerprints.
No source arrays, fitting, output writes, global mutable document or timestamps.
"""
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 'results/revision-20261023/v6/'
PROTOCOL = 'protocol/revision-v6/'
PREFIX = 'v6supp:'
GAMMAS = (.001, .005, .01, .05)
SOURCES = {
    'fx_hourly': 'FX (USD)', 'nyfed_weekly': 'Treasury bill (USD m)',
    'PDPOSMBS-TOT': 'Agency MBS (USD m)', 'PDPOSCS-TOT': 'Corporate (USD m)',
    'PDPOSFGS-TOT': 'Agency/GSE (USD m)', 'PDPOSTIPS-L2': 'TIPS <=2y (USD m)',
    'PDPOSTIPS-G11': 'TIPS >11y (USD m)', 'PDPOSTIPS-G2': 'TIPS >2y (USD m)',
    'PDPOSTIPS-G6L11': 'TIPS 6-11y (USD m)', 'PDPOSGSC-L2': 'Coupons <=2y (USD m)',
    'PDPOSGSC-G2L3': 'Coupons 2-3y (USD m)', 'PDPOSGSC-G3L6': 'Coupons 3-6y (USD m)',
    'PDPOSGSC-G6L7': 'Coupons 6-7y (USD m)', 'PDPOSGSC-G7L11': 'Coupons 7-11y (USD m)',
}
METHODS = {'ACI_F': 'ACI-F', 'ACI_QR': 'ACI-QR', 'SAV': 'Headroom SAV',
           'frozen_F': 'Frozen F', 'rolling_F': 'Rolling F', 'F': 'Matched frozen F',
           'QR': 'Selected QR', 'MEAN_F_QR': 'mean(F,QR)',
           'MEDIAN_F_QR_KNN': 'median(F,QR,KNN)'}
PROSE_MATH = {
    'α=.05':r'\alpha=0.05',
    'err<sub>i</sub>=1{P<sub>i,H</sub>&gt;C<sub>i</sub>}':r'\mathrm{err}_i=\mathbf1\{P_{i,H}>C_i\}',
    'α←min(1,max(1/(m<sub>t</sub>+1),α+γ(.05−err<sub>i</sub>)))':r'\alpha\leftarrow\min\{1,\max[1/(m_t+1),\alpha+\gamma(0.05-\mathrm{err}_i)]\}',
    'v<sub>0</sub>=max(mean<sub>train</sub>(RMS),10<super>−12</super>)':r'v_0=\max\{\operatorname{mean}_{\rm train}(\operatorname{RMS}),10^{-12}\}',
    's<sub>i</sub>=P<sub>i,H</sub>−C<sub>i</sub><super>base</super>':r's_i=P_{i,H}-C_i^{\rm base}',
    'i+H≤t':r'i+H\le t',
    'α<sub>t</sub>∈[1/(m<sub>t</sub>+1),1]':r'\alpha_t\in[1/(m_t+1),1]',
    'r<sub>t</sub>=⌈(m<sub>t</sub>+1)(1−α<sub>t</sub>)⌉':r'r_t=\lceil(m_t+1)(1-\alpha_t)\rceil',
    'B<sub>i</sub>=|N<sub>i</sub>|':r'B_i=|N_i|',
    'G<sub>i,H</sub>=P<sub>i,H</sub>−B<sub>i</sub>':r'G_{i,H}=P_{i,H}-B_i',
    'g<sub>i</sub>=G<sub>i,H</sub>/a<sub>κ</sub>':r'g_i=G_{i,H}/a_\kappa',
    'q̃<sub>i</sub>=β<sub>0</sub>+β<sub>1</sub>q̃<sub>i−1</sub>+β<sub>2</sub>g<sub>i−H</sub>':r'\widetilde q_i=\beta_0+\beta_1\widetilde q_{i-1}+\beta_2 g_{i-H}',
    'C<sub>t</sub>=B<sub>t</sub>+a<sub>κ</sub>max(0,q̃<sub>t</sub>)':r'C_t=B_t+a_\kappa\max(0,\widetilde q_t)',
    'a<sub>κ</sub>':r'a_\kappa',
    'p<sub>g</sub>=n<sub>g</sub>/n':r'p_g=n_g/n',
    'ψ<sub>t,g</sub>=1{S<sub>t</sub>=g}(d<sub>t</sub>−μ<sub>g</sub>)/p<sub>g</sub>':r'\psi_{t,g}=\mathbf1\{S_t=g\}(d_t-\mu_g)/p_g',
    'SE(μ<sub>g</sub>)=√(HAC(ψ<sub>·,g</sub>)/n)':r'\operatorname{SE}(\mu_g)=\sqrt{\operatorname{HAC}(\psi_{\cdot,g})/n}',
    'Z<sub>t</sub>=[1,d<sub>t−H</sub>/a<sub>0</sub>,RMS<sub>t</sub>/v<sub>0</sub>]<super>T</super>':r'Z_t=[1,d_{t-H}/a_0,\operatorname{RMS}_t/v_0]^{\mathsf T}',
    'm<sub>t</sub>=Z<sub>t</sub>(d<sub>t</sub>/a<sub>0</sub>)':r'm_t=Z_t(d_t/a_0)',
    'd<sub>t</sub>':r'd_t', 'S<sub>t</sub>':r'S_t', 'μ<sub>g</sub>':r'\mu_g',
    'a<sub>0</sub>':r'a_0', 'v<sub>0</sub>':r'v_0',
    'k=⌈(W+1)τ⌉':r'k=\lceil(W+1)\tau\rceil',
    'W(1−τ)≥5':r'W(1-\tau)\ge5',
    'n<sub>val</sub>(1−τ)≥5':r'n_{\rm val}(1-\tau)\ge5',
    'k≤W':r'k\le W', 'τ=.90':r'\tau=0.90', 'τ=.99':r'\tau=0.99',
    'τ=.95':r'\tau=0.95', '1−τ':r'1-\tau',
    'α':r'\alpha', 'κ':r'\kappa', 'τ':r'\tau',
}


def _read(path):
    return json.loads((ROOT / path).read_text())


def _num(value):
    if value is None:
        return 'NA'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    if isinstance(value, int):
        return str(value)
    value = float(value)
    if not math.isfinite(value):
        raise ValueError('nonfinite public aggregate')
    return format(value, '.7g')


def _method(value):
    return METHODS.get(value, str(value))


def _source(row):
    return SOURCES[row['source']]


def _hw(row):
    return f"H{row.get('horizon', 6)} / W{row.get('window', row.get('qr_window'))}"


def _context(row):
    return _source(row) + '; ' + _hw(row)


def _state(value):
    return {'OK': 'OK', 'COMPLETE': 'Complete', 'BOUNDARY_REFERENCE': 'Boundary reference',
            'UNIDENTIFIED_TRANSITION_ROW': 'NA: absent transition row',
            'IDENTICAL_LOSSES': 'Identical losses; raw p NA', 'NA_CELL': 'NA cell',
            'ORIGINAL_PLAIN_KNN_NOT_AVAILABLE': 'plain KNN was not run; no substitute',
            'NONCONVERGENCE': 'NONCONVERGENCE',
            'NOT_ATTEMPTED_TAIL_INFORMATION': 'Not run: tail-information screen'}.get(value, str(value))


def _test_cell(status, p):
    return _state(status) + '; p=' + _num(p)


def _range(row, low, high):
    return _num(row.get(low)) + ' to ' + _num(row.get(high))


def _validation_path(row):
    return BASE + f"wp2/validation-{row['source']}-h{row['horizon']}-w{row['window']}-{row['method']}.json"


def _tau_path(source, tau):
    return BASE + f"wp5-v2/validation-{source}-tau{int(round(tau*100))}.json"


def _build():
    paths = {name: BASE + name + '.json' for name in
             ('wp2-summary', 'wp2-comparisons', 'wp3-combinations', 'wp3-findings', 'wp4-states', 'wp5-tau-summary')}
    w2, d2, w3, f3, w4, w5 = [_read(paths[name]) for name in paths]
    val2_paths = [_validation_path(row) for row in w2['method_rows']]
    val2 = { (r['source'], r['horizon'], r['window'], r['method']): _read(p)
             for r, p in zip(w2['method_rows'], val2_paths) }
    val5_paths = sorted({_tau_path(r['source'], r['tau']) for r in w5['rows']})
    val5 = { (z['source'], z['tau']): z for z in map(_read, val5_paths) }
    p2 = [paths['wp2-summary'], paths['wp2-comparisons'], *val2_paths, PROTOCOL+'wp2-aci-sav.md']
    p3 = [paths['wp3-combinations'], paths['wp3-findings'], PROTOCOL+'wp3-combinations.md']
    p4 = [paths['wp4-states'], PROTOCOL+'wp4-state-gw.md']
    p5 = [paths['wp5-tau-summary'], *val5_paths, PROTOCOL+'wp5-quantile-levels.md']
    blocks = {}; figure_keys = []; table_number = 38
    def put(key, block, inputs):
        block['_generator'] = PREFIX+key
        block['_bindings'] = [{'path': path, 'sha256': hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
                              for path in sorted(set(inputs))]
        blocks[key] = block
    def prose(key, text, inputs):
        block=dict(type='p',html=text)
        pairs=[{'html':html,'latex':latex} for html,latex in PROSE_MATH.items() if html in text]
        if pairs:block['inline_math']=pairs
        put(key,block,inputs)
    def table(key, caption, headers, rows, inputs):
        nonlocal table_number
        if len(headers)>8 or any(len(row)!=len(headers) for row in rows):
            raise ValueError('supplement table shape')
        put(key, dict(type='table', caption=f'Table S{table_number}. '+caption,
                      headers=headers, rows=[[str(c) for c in row] for row in rows]), inputs)
        table_number += 1

    def reason2(row):
        if row.get('status') in ('COMPLETE', 'OK') or ('status' not in row and row.get('scores')):
            text='Complete'
            if row.get('identity'): text+='; '+str(row['identity'])
            return text
        val=val2.get((row['source'],row['horizon'],row['window'],row.get('method')))
        if val and val.get('reason')=='INSUFFICIENT_PREVALIDATION_CALIBRATION':
            return 'NA: initial calibration '+_num(val['grid']['mature_initial_count'])+' < 19'
        return 'NA: '+_state(row.get('reason', row.get('status', 'unavailable')))
    def reason5(row):
        val=val5[(row['source'],row['tau'])]
        if val['status']=='COMPLETE': return _state(row.get('status','COMPLETE'))
        failed=[c for c in val['candidates'] if c['status']=='FAILED']
        if failed:
            return 'NA: whole QR menu ineligible; '+', '.join('lambda='+_num(c['parameter'])+' '+c.get('reason','failed') for c in failed)
        s=val['screen']
        return 'NA: tail information; validation='+s['validation_tail_fraction']+'; window='+', '.join(x['nominal_tail_fraction'] for x in s['window_rows'])+' < '+s['minimum_expected_fraction']
    def score_rows(entries):
        rows=[]
        for row, method, scores, status in entries:
            scores=scores or {}
            rows.append([_source(row),_hw(row),method,_num(scores.get('mean_loss')),
                         _num(scores.get('n')),_num(scores.get('full_hits')),_num(scores.get('full_rate')),status])
        return rows
    def coverage_rows(entries):
        rows=[]
        for row, method, scores, status in entries:
            cov=(scores or {}).get('coverage') or {};full=cov.get('full',{});grid=cov.get('fixed_grid',{});cc=grid.get('transition_cc',{})
            rows.append([_context(row),method,
                         _test_cell(full.get('uc_status',status),full.get('uc_p')),
                         ' / '.join(_num(grid.get(k)) for k in ('n','hits','rate')),
                         _test_cell(grid.get('uc_status',status),grid.get('uc_p')),
                         _num(cc.get('transition_n')),
                         _test_cell(cc.get('status',status),cc.get('p')),
                         _num(cov.get('boundary_count'))+'/'+_num(cov.get('na_count'))])
        return rows
    def dm_rows(rows, work):
        result=[]
        for row in rows:
            if work==5:
                context=_source(row)+'; τ='+_num(row['tau'])
                contrast='QR W'+_num(row['qr_window'])+' minus '+_method(row['reference_method'])+' W'+_num(row['reference_window'])
                difference=_num(row.get('mean_difference'))+'; .95='+_num(row.get('point95_mean_difference'))+'; reversal='+_num(row.get('direction_reversal'))
                status=reason5(row)
            else:
                context=_context(row);contrast=_method(row['left_method'])+' minus '+_method(row['right_method'])
                difference=_num(row.get('mean_difference'));status=_state(row['status'])
                if row['status']=='NA_CELL':
                    if work==3: status='NA: plain KNN was not run'
                    else:
                        causes=[]
                        for method in (row['left_method'],row['right_method']):
                            r=next((x for x in w2['method_rows'] if (x['source'],x['horizon'],x['window'],x['method'])==(row['source'],row['horizon'],row['window'],method)),None)
                            if r and r['status']!='COMPLETE':causes.append(_method(method)+' '+reason2(r))
                        status='; '.join(causes) or status
            result.append([context,contrast,difference,_num(row.get('n'))+'/'+_num(row.get('bandwidth')),
                           _num(row.get('raw_p')),_num(row.get('hln_p')),_num(row.get('holm_p')),
                           status+'; book= '+_num(row['bookkeeping_p'])])
        return result

    all_inputs=[*paths.values(),PROTOCOL+'common-contract.md']
    prose('scope','<b>Post-result / exploratory analyses.</b> These additions use already inspected evaluation archives and preserve the original primary comparisons. The additional methods include finite adaptations of adaptive conformal inference (ACI) and symmetric absolute-value (SAV) recursion. They are not independent dealer replications, prospective validation, a new primary, a deployed switching rule or a financing-policy experiment. FX losses are in USD; original Treasury-bill and added NY Fed net-position tasks are in USD millions. Tables show every declared method and ranking slot, including failures, ties and adverse directions.',all_inputs)
    prose('reading','Rates are fractions and losses retain native units. Displayed finite values are rounded to seven significant digits; counts are integers. Negative differences favor the new procedure under the stated target level. The Diebold and Mariano (1995) DM diagnostic uses the original centered Bartlett-HAC convention associated with Newey and West (1987); Harvey, Leybourne and Newbold (1997) provide the separately reported HLN finite-sample adjustment. All are working-reference diagnostics with unverified dependence, moment and finite-sample assumptions. Holm (1979) adjustment retains separate family sizes of '+', '.join(_num(x['family_n']) for x in (d2,w3,w4,w5))+'. A raw p of NA remains unidentified; book=1 is only bookkeeping and does not create a valid test. These families do not adjust all historical model and analysis selection.',all_inputs)
    table('inventory','Complete additional-analysis inventories. State groups are descriptive rows; test families are distinct.',
          ['Work','New methods/groups','Controls','Test slots','Raw-p NA','Complete methods','NA methods','Scope'],
          [['WP2',_num(w2['method_row_count']),_num(w2['control_row_count']),_num(d2['family_n']),_num(d2['raw_na_count']),_num(w2['complete_method_count']),_num(w2['na_method_count']),'ACI and SAV'],
           ['WP3',_num(w3['method_row_count']),_num(len(w3['control_rows'])),_num(w3['family_n']),_num(w3['raw_na_count']),_num(w3['complete_method_count']),_num(w3['na_method_count']),'Fixed combinations'],
           ['WP4',_num(sum(len(r['groups']) for r in w4['rows'])),'Original primaries',_num(w4['family_n']),_num(w4['raw_na_count']),'Descriptive groups','See test status','States and moments'],
           ['WP5',_num(len(w5['rows'])),'Named F controls',_num(w5['family_n']),_num(w5['raw_na_count']),_num(sum(r['status']!='NA' for r in w5['rows'])),_num(sum(r['status']=='NA' for r in w5['rows'])),'Refitted target levels']],all_inputs)

    prose('wp2-definition','<b>Finite delayed ACI-style calibration and headroom SAV.</b> The ACI-style procedure is motivated by Gibbs and Candès (2021), with the following finite-memory, delayed and projected modifications. Initialize α=.05. At issue t, consume newly matured strict hits err<sub>i</sub>=1{P<sub>i,H</sub>&gt;C<sub>i</sub>} in chronological order, once each, using α←min(1,max(1/(m<sub>t</sub>+1),α+γ(.05−err<sub>i</sub>))). Here m<sub>t</sub> is the current completed-score pool size, also used for a projection immediately before issuing the next report. Its score s<sub>i</sub>=P<sub>i,H</sub>−C<sub>i</sub><super>base</super> uses the actual completed H-horizon peak and that issue\'s base report. At issue t the pool contains at most W scores with i+H≤t; each wrapped breach is consumed once, in order. After delayed feedback the α state itself is projected to α<sub>t</sub>∈[1/(m<sub>t</sub>+1),1], where the current pool size is used, and the exact fractional rank is r<sub>t</sub>=⌈(m<sub>t</sub>+1)(1−α<sub>t</sub>)⌉. Rank zero issues the known floor; other reports are floor-projected base-plus-score quantiles. No original ACI guarantee is imported. Gamma is selected from '+', '.join(map(_num,GAMMAS))+' by validation absolute breach-rate distance to .05, then .95 pinball loss, then smaller gamma; that coverage-first retrospective tuning differs from original QR tuning. The chosen validation state and unconsumed feedback carry across the unissued gap. Headroom SAV adapts the symmetric absolute-value CAViaR recursion of Engle and Manganelli (2004). Define B<sub>i</sub>=|N<sub>i</sub>| and G<sub>i,H</sub>=P<sub>i,H</sub>−B<sub>i</sub>. At each refit use g<sub>i</sub>=G<sub>i,H</sub>/a<sub>κ</sub> and q̃<sub>i</sub>=β<sub>0</sub>+β<sub>1</sub>q̃<sub>i−1</sub>+β<sub>2</sub>g<sub>i−H</sub>, with the positive response scale a<sub>κ</sub> known at refit κ and held until the next refit. The source-unit report is C<sub>t</sub>=B<sub>t</sub>+a<sub>κ</sub>max(0,q̃<sub>t</sub>), so the normalized prediction is multiplied back by the same training scale. It is a headroom adaptation rather than a literal CAViaR return-VaR replication. Its fixed bounded Powell six-start algorithm retains convergence failures and claims no global optimum. Initial history, delayed feedback and solver eligibility can invalidate a whole cell.',p2)
    entries2=[(r,_method(r['method']),r.get('scores'),reason2(r)) for r in w2['method_rows']]
    controls2=[(r,_method(r['method']),r.get('scores'),reason2(r)) for r in w2['control_rows']]
    score_headers=['Task (unit)','H / W','Procedure','Mean loss','n','Hits','Rate','Status / reason']
    table('wp2-methods','All new WP2 evaluation methods; τ=.95. Hits use strict peak > report.',score_headers,score_rows(entries2),p2)
    table('wp2-controls','All matched unwrapped WP2 controls, retained separately from wrapped reports.',score_headers,score_rows(controls2),p2)
    prose('coverage-definition','<b>Coverage diagnostics.</b> Full-sample UC following Kupiec (1995) uses every evaluation issue. The sparse grid is fixed at the first evaluation origin plus j(H+1), without a selected offset. Grid UC uses its full grid sample. Motivated by the Markov coverage framework of Christoffersen (1998), new CC is explicitly transition-conditional: it compares the saturated two-row Markov likelihood with the fixed-α likelihood on the same n−1 adjacent grid pairs, conditioning on the first hit. This differs from the legacy mixed full-sample-UC-plus-transition-independence construction; old reported CC values remain untouched. An absent transition row is NA. Boundary-reference p values and nonrejection do not certify conditional coverage, rule out floor atoms, or establish a guarantee. Boundary/NA counts are diagnostic counts, not removed observations.',[PROTOCOL+'common-contract.md',*paths.values()])
    cov_headers=['Context','Procedure','Full UC status / p','Grid n/hits/rate','Grid UC status / p','CC pairs','CC status / p','Boundary / NA']
    table('wp2-coverage','WP2 full-sample UC, fixed-grid UC and new transition-conditional CC for every method and control.',cov_headers,coverage_rows(entries2+controls2),p2)
    validation_rows=[]; gamma_rows=[]; state_rows=[];feedback_rows=[];effects=[];sav_rows=[]
    for row in w2['method_rows']:
        val=val2[(row['source'],row['horizon'],row['window'],row['method'])]
        selection=val.get('selection',{});sel=selection.get('gamma');cand=next((c for c in val.get('menu',[]) if c['gamma']==sel),{})
        score=val.get('scores') or cand.get('scores') or {}
        validation_rows.append([_source(row),_hw(row),_method(row['method']),reason2({**row,'status':val['status'],'reason':val.get('reason')}),
                                _num(sel),_num(score.get('n'))+'/'+_num(score.get('full_hits')),_num(score.get('mean_loss')),_num(val.get('grid',{}).get('mature_initial_count'))])
        if row['method'].startswith('ACI_'):
            for gamma in GAMMAS:
                c=next((c for c in val.get('menu',[]) if c['gamma']==gamma),None)
                gamma_rows.append([_context(row),_method(row['method']),_num(gamma),_state(c['status']) if c else 'Not run: '+reason2(row),
                                   _num(c.get('origin_count') if c else None),_num(c.get('hits') if c else None),_num(c.get('mean_loss') if c else None),'Yes' if c and sel==gamma else 'No'])
            diag=row.get('diagnostics',{})
            state_rows.append([_context(row),_method(row['method']),_range(diag,'alpha_min','alpha_max'),_range(diag,'calibration_min','calibration_max'),
                               _range(diag,'rank_min','rank_max'),_num(diag.get('initial_calibration_count')),reason2(row)])
            feedback_rows.append([_context(row),_method(row['method']),_num(diag.get('clip_count')),_num(diag.get('clipped_issue_count'))+'/'+_num(diag.get('issue_count')),
                                  _num(diag.get('clipped_issue_fraction')),_num(diag.get('matured_wrapped_feedback_consumed')),_num(diag.get('cumulative_matured_wrapped_feedback')),reason2(row)])
            effects.append([_context(row),_method(row['method']),_num(row.get('selected_gamma')),_num(row.get('wrapped_minus_base_mean_loss')),
                            _num(row.get('wrapped_minus_base_coverage_distance')),_num(row.get('wrapped_minus_base_full_rate')),_num(row.get('wrapped_minus_base_full_hits')),reason2(row)])
        else:
            sav_rows.append([_context(row),_num(row.get('refit_count')),_num(row.get('analytic_refit_count')),_num(row.get('converged_refit_count')),reason2(row)])
    table('wp2-validation','All original WP2 validation method cells; SAV has no gamma selection. Missing initial counts for SAV are not calibration failures.',
          ['Task (unit)','H / W','Procedure','Validation status','Selected gamma','Val n / hits','Val loss','Initial m'],validation_rows,p2)
    table('wp2-gammas','Complete declared ACI gamma inventory, including explicitly not-run slots when initial calibration was inadequate. Candidate metrics are not invented for those slots.',
          ['Context','Wrapper','Gamma','Candidate status','Val n','Hits','Mean loss','Selected'],gamma_rows,p2)
    table('wp2-states','ACI state and calibration ranges on evaluation; all wrappers remain listed.',
          ['Context','Wrapper','Alpha range','m range','Rank range','Initial m','Status'],state_rows,p2)
    table('wp2-feedback','ACI clipping and once-only feedback. Clip updates and clipped issues are different counts.',
          ['Context','Wrapper','Clip updates','Clipped / issues','Clip fraction','Eval feedback','Cumulative feedback','Status'],feedback_rows,p2)
    table('wp2-effects','Wrapper minus its named unwrapped base. Coverage distance is the absolute full-origin breach-rate distance to .05; negative distance changes improve that descriptive measure.',
          ['Context','Wrapper','Gamma','Delta mean loss','Delta abs distance','Delta breach rate','Delta hits','Status'],effects,p2)
    pairrows=[]
    for r in w2['aci_pairs']:
        status='Complete' if r['status']=='COMPLETE' else 'NA: wrapped pair unavailable from initial calibration'
        pairrows.append([_context(r),_num(r.get('unwrapped_qr_minus_f_mean_loss')),_num(r.get('wrapped_qr_minus_f_mean_loss')),
                         _num(r.get('unwrapped_qr_minus_f_coverage_distance')),_num(r.get('wrapped_qr_minus_f_coverage_distance')),
                         _num(r.get('unwrapped_qr_minus_f_full_hits')),_num(r.get('wrapped_qr_minus_f_full_hits')),status])
    table('wp2-pairs','Selected QR minus matched frozen F, before and after the complete ACI procedures. These paired score/coverage changes retain the procedure-level tuning distinction.',
          ['Context','Base loss delta','Wrapped loss delta','Base abs-dist delta','Wrapped abs-dist delta','Base hit delta','Wrapped hit delta','Status'],pairrows,p2)
    table('wp2-sav','All SAV refit inventories; analytic constant fits have a distinct status rather than fictitious numerical convergence.',
          ['Context','Refits','Analytic constant','Converged numeric','Status'],sav_rows,p2)
    ops=[]
    for r in w2['control_rows']:
        a=r['archived_original_aggregate']
        ops.append([_context(r),_method(r['method']),_num(a['mean_capacity']),_num(a['mean_extra_allowance']),_num(a['mean_positive_overrun']),
                    _num(a['conditional_mean_overrun'])+' (n='+_num(a['conditional_overrun_denominator'])+')',_num(a['mean_unused_allowance']),a.get('conditional_overrun_undefined_reason') or 'Defined'])
    table('wp2-control-operations','Archived operational summaries for every unwrapped control. Conditional mean overrun is NA when its own breach denominator is zero.',
          ['Context','Control','Mean report','Mean extra','Mean overrun','Conditional overrun (n)','Mean unused','Conditional status'],ops,p2)
    dm_headers=['Context','New minus named control','Mean delta','n / L','DM raw p','HLN p','Holm p','Status; book p']
    table('wp2-dm','Full WP2 fixed ranking family. Direction is new procedure minus the named control; all NA slots remain in the family.',dm_headers,dm_rows(d2['rows'],2),p2)

    prose('wp3-definition','<b>Fixed report combinations.</b> The arithmetic mean uses matched frozen F and original selected QR; the median additionally requires original selected plain KNN at the same source, horizon, window, issue origins and refit convention. No weight or constituent is selected on outcomes. In the added panel, plain KNN was not run: the median is NA rather than replaced by C2_QR4 or Levy_L. Combining reports preserves the common floor but does not guarantee a conditional quantile, calibration or loss below the best constituent. Where KNN equals F, the median is algebraically F, and an identical-loss raw p stays NA. The quantile elementary-score decomposition of Ehm et al. (2016) supplies the Murphy-diagram comparison: exact signs at every unique breakpoint determine sample dominance or crossing before any display curve is drawn.',p3)
    table('wp3-counts','Descriptive combination counts over the complete context inventory; lower means strictly lower observed mean loss.',
          ['Combination','Total','Complete','NA','Lower than both','Lower than F','Lower than QR','Exactly F'],
          [[_method(name),*[_num(c[k]) for k in ('total','complete','na','lower_than_both','lower_than_F','lower_than_QR','exactly_F')]] for name,c in f3['counts'].items()],p3)
    def status3(row):
        if row.get('status')=='NA':return 'NA: plain KNN was not run; no substitute'
        return 'Complete'+('; '+str(row['identity']) if row.get('identity') else '')
    entries3=[(r,_method(r['method']),r.get('scores'),status3(r)) for r in w3['method_rows']]
    controls3=[(r,_method(r['method']),r['scores'],'Complete') for r in w3['control_rows']]
    table('wp3-methods','Every WP3 combination method record at τ=.95, including all unavailable added-panel medians.',score_headers,score_rows(entries3),p3)
    table('wp3-controls','Every matched F/QR constituent control used by the combinations; units remain source specific.',score_headers,score_rows(controls3),p3)
    table('wp3-relative','All combination percentage loss changes versus their own matched constituents; denominators are the named constituent losses at the same target level. NA medians retain both unavailable changes.',
          ['Context','Combination','Mean loss','Percent vs F','Percent vs QR','Status'],
          [[_context(r),_method(r['method']),_num((r.get('scores') or {}).get('mean_loss')),
            _num(r.get('percent_vs_F')),_num(r.get('percent_vs_QR')),status3(r)] for r in w3['method_rows']],p3)
    table('wp3-coverage','Complete combination and constituent full-sample UC, fixed-grid UC and transition-conditional CC. Absent transition rows and boundary references retain their status.',
          cov_headers,coverage_rows(entries3+controls3),p3)
    table('wp3-dm','Full WP3 fixed DM family. Identical losses retain numerical zero with raw p NA; missing constituents retain their slots.',dm_headers,dm_rows(w3['comparisons'],3),p3)
    murphy=[]
    for r in w3['murphy']:
        murphy.append([_context(r),_method(r['left_method'])+' minus '+_method(r['right_method']),r['ranking'],_num(r['breakpoint_count']),
                       _num(r['positive_breakpoints']),_num(r['negative_breakpoints']),_num(r['zero_breakpoints']),
                       _num(r['pinball_difference'])+'; residual='+_num(r['integral_minus_pinball'])])
    table('wp3-murphy','Exact elementary-score comparisons at every unique breakpoint. The mathematical integral identity is checked numerically; the stored integral-minus-pinball residual is shown without rounding it to zero. These matched-constituent contexts do not replace the original FX cross-window rolling-F primary comparison.',
          ['Context','New minus constituent','Ranking','Breakpoints','Positive','Negative','Zero','Pinball delta; integral residual'],murphy,p3)
    prose('wp3-readout',f"All {len(w3['murphy'])} retained matched-constituent Murphy comparisons are "+('CROSSING' if all(r['ranking']=='CROSSING' for r in w3['murphy']) else 'shown above')+'. Display curves are drawn only after exact all-breakpoint signs were determined; plotted resolution is not the comparison grid. The related NY Fed tasks share measurement systems and are not independent dealer replications. The complete mean/median inventories retain every adverse, equal and unavailable comparison.',p3)

    prose('wp4-definition','<b>Issue-known position-change states.</b> The state is past-only short position-increment RMS, not price or yield volatility. Linear training-only terciles from the first mature QR pool are frozen for evaluation; ties can leave empty groups rather than prompt changed thresholds. Let d<sub>t</sub> be the new-minus-original-reference pinball difference, S<sub>t</sub> the frozen group and μ<sub>g</sub> its group mean. For group share p<sub>g</sub>=n<sub>g</sub>/n, groups retain the complete issue axis through ψ<sub>t,g</sub>=1{S<sub>t</sub>=g}(d<sub>t</sub>−μ<sub>g</sub>)/p<sub>g</sub>. HAC standard errors use SE(μ<sub>g</sub>)=√(HAC(ψ<sub>·,g</sub>)/n), including zeros at other group dates rather than compressed dates. Heterogeneity tests equal group means. Motivated by Giacomini and White (2006), the separate finite-instrument GW-style test uses Z<sub>t</sub>=[1,d<sub>t−H</sub>/a<sub>0</sub>,RMS<sub>t</sub>/v<sub>0</sub>]<super>T</super> and moments m<sub>t</sub>=Z<sub>t</sub>(d<sub>t</sub>/a<sub>0</sub>) after the explicit H-row burn-in. The constant a<sub>0</sub> is the initial mature QR training response scale defined in main Section 4; v<sub>0</sub>=max(mean<sub>train</sub>(RMS),10<super>−12</super>) uses short RMS over that same training pool. Neither constant is fitted on evaluation observations. Its joint rejection may reflect only an unconditional mean advantage, not a state effect or switching policy. Singular, nonpositive, ill-conditioned and other failed references remain NA.',p4)
    groups=[];training=[];diag4=[];tests4=[]
    for r in w4['rows']:
        label=_source(r)+'; QR W'+_num(r['window'])+' minus '+_method(r['reference_method'])+' W'+_num(r['reference_window'])
        for g in r['groups']:
            groups.append([label,g['group'],_num(g['n']),_num(g['mean_difference']),_num(g['hac_se']),_state(g['hac_status']),_num(r['full_n']),_num(r['group_bandwidth'])])
        training.append([label,_num(r['training_first'])+'..'+_num(r['training_last']),_num(r['latest_training_label_end']),_num(r['training_count']),
                         _num(r['a0']),_num(r['v0']),_num(r['cut1']),_num(r['cut2'])])
        for field in ('gw','heterogeneity'):
            t=r[field]
            diag4.append([_source(r),'Joint GW' if field=='gw' else 'Equal group means',_num(t['n'])+'/'+_num(t.get('burn_in',0)),_num(t['bandwidth']),
                          _num(t.get('instrument_rank'))+'/'+_num(t['covariance_rank']),_num(t['covariance_condition']),_num(t['eigen_min'])+' / '+_num(t['eigen_max']),_state(t['status'])])
    for r in w4['ranking']:
        parent=next(x for x in w4['rows'] if x['source']==r['source']);t=parent['gw' if r['test']=='joint_GW' else 'heterogeneity']
        tests4.append([_source(r),'Joint GW' if r['test']=='joint_GW' else 'Equal group means',_num(t['n'])+'/'+_num(t['bandwidth']),_num(t['df']),_num(r['stat']),_num(r['raw_p']),_num(r['holm_p']),_state(r['status'])+'; book= '+_num(r['bookkeeping_p'])])
    table('wp4-groups','All state groups for the unchanged original H6 primaries; means and SEs are in the displayed native units.',
          ['Original primary (unit)','Group','Group n','Mean difference','HAC SE','HAC status','Full n','L'],groups,p4)
    table('wp4-training','Initial mature training pool, response/RMS normalizers and frozen state cut points. Source record maturity, not historical public-release availability, defines the replay clock.',
          ['Original primary (unit)','Training origins','Latest label end','Training n','a₀','v₀','Cut 1','Cut 2'],training,p4)
    blocks['wp4-training']['math_cells']={'a₀':r'a_0','v₀':r'v_0'}
    table('wp4-tests','All four fixed WP4 working-reference tests; joint GW and state-mean heterogeneity are different nulls.',
          ['Task (unit)','Test','n / L','df','Wald','Raw p','Holm p','Status; book p'],tests4,p4)
    table('wp4-diagnostics','Reference diagnostics. GW n excludes burn-in; group means and their covariance retain the full original evaluation axis. No instrument is dropped to rescue a failed test.',
          ['Task (unit)','Test','n / burn-in','L','Instrument / covariance rank','Condition','Eigen min / max','Status'],diag4,p4)

    prose('wp5-definition','<b>Refitted target-level sensitivity.</b> QR is refitted at τ=.90 and τ=.99 using the original features, mature pools, scales, refit grids and solver acceptance. The generic engine must first match the unchanged .95 controls. For each source and target level the entire original lambda menu is evaluated on every validation origin; lowest target-specific pinball wins, with larger lambda on an exact tie. Any failed or incomplete declared candidate invalidates the whole QR cell, even if another candidate completed. Selected parameters and validation receipts are frozen before evaluation. Historical F uses the exact corrected rank k=⌈(W+1)τ⌉, the named rolling/frozen clock and current floor. Every window must first satisfy W(1−τ)≥5, validation must satisfy n<sub>val</sub>(1−τ)≥5, and the corrected rank must satisfy k≤W. This exact nominal-tail screen is a minimum-information convention rather than a calibration theorem. Absolute losses across target levels are different objectives and are not compared as if unchanged.',p5)
    selection_rows=[];screen_rows=[];candidate_rows=[]
    for (source,tau),v in val5.items():
        row={'source':source,'tau':tau};sc=v['screen'];sel=v['selection'];status=reason5(row) if v['status']!='COMPLETE' else 'Complete'
        selection_rows.append([_source(row),_num(tau),_state(v['status']),_num(sel.get('parameter')),sel['status'],_num(sel.get('mean_validation_pinball')),status])
        win='; '.join('W'+_num(x['window'])+': '+x['nominal_tail_fraction']+'; rank '+_num(x['rank'])+' '+('available' if x['rank_available'] else 'unavailable') for x in sc['window_rows'])
        screen_rows.append([_source(row),_num(tau),sc['tau_fraction'],sc['tail_probability_fraction'],sc['validation_tail_fraction'],win,sc['minimum_expected_fraction'],sc['status']+'; '+(sc.get('reason') or 'passed')])
        for c in v['candidates']:
            s=c.get('scores') or {};state=_state(c['status'])
            if c.get('reason'):state+=': '+c['reason']
            candidate_rows.append([_source(row)+'; τ='+_num(tau),_num(c['parameter']),state,_num(c.get('origin_count')),_num(c.get('mean_pinball')),
                                   _num(s.get('full_hits')),_num(s.get('full_rate')),'Yes' if sel.get('status')=='SELECTED' and sel.get('parameter')==c['parameter'] else 'No (whole menu ineligible)' if sel.get('status')!='SELECTED' else 'No'])
    table('wp5-selection','All target-level validation cells; selection is frozen before evaluation and failed full menus remain ineligible.',
          ['Task (unit)','Target level','Cell status','Selected lambda','Selection','Selected validation loss','Full reason'],selection_rows,p5)
    table('wp5-screen','Exact index-only nominal-tail admission. Fraction strings are exact, not rounded floating thresholds.',
          ['Task (unit)','Target level','Exact level','Tail probability','Validation tail count','Window tail / corrected rank','Minimum','Screen / reason'],screen_rows,p5)
    table('wp5-candidates','Every declared lambda candidate in every target-level validation cell. Complete alternatives do not override a failed candidate.',
          ['Task / level','Lambda','Candidate status','Val n','Mean loss','Hits','Rate','Selected'],candidate_rows,p5)
    tau_entries=[]
    for r in w5['rows']:
        for role,scores in [('QR',r.get('qr_scores')),('reference',r.get('reference_scores'))]:
            row={**r,'window':r['qr_window'] if role=='QR' else r['reference_window']}
            method=('QR' if role=='QR' else _method(r['reference_method']))+'; τ='+_num(r['tau'])+'; '+r['reference_kind']
            tau_entries.append((row,method,scores,reason5(r)))
    table('wp5-scores','All procedures underlying the six fixed target-level comparison slots. A missing score after whole-menu invalidation is not a computed zero or an individual F fitting failure.',score_headers,score_rows(tau_entries),p5)
    table('wp5-coverage','Target-specific full-sample and fixed-grid UC and transition-conditional CC; null probability is the stated 1−τ. No tests are manufactured for unavailable evaluation cells.',cov_headers,coverage_rows(tau_entries),p5)
    table('wp5-directions','Every target-level loss direction and same-target percentage change. The unchanged .95 paired mean is a direction benchmark; absolute objectives differ across target levels. Unavailable new-level comparisons have no reversal result.',
          ['Task / level','Named F control','New mean delta','.95 mean delta','Reversal','Percent vs same-target F','Status'],
          [[_source(r)+'; τ='+_num(r['tau']),_method(r['reference_method'])+' W'+_num(r['reference_window']),
            _num(r.get('mean_difference')),_num(r.get('point95_mean_difference')),_num(r.get('direction_reversal')),
            _num(r.get('mean_loss_change_percent')),reason5(r)] for r in w5['rows']],p5)
    table('wp5-dm','All six fixed WP5 DM slots. The mean-delta cell also shows the corresponding unchanged .95 direction benchmark and the explicit reversal flag; NA means the new-level comparison was unavailable, not no reversal.',
          ['Context','QR minus named control','Mean delta; .95; reversal','n / L','DM raw p','HLN p','Holm p','Status; book p'],dm_rows(w5['rows'],5),p5)
    complete90=[r for r in w5['rows'] if r['tau']==.9 and r['status']!='NA']
    level99=[r for r in w5['rows'] if r['tau']==.99]
    causes99='; '.join(_source({'source':source})+': '+reason5({'source':source,'tau':tau})
                       for source,tau in val5 if tau==.99)
    prose('wp5-readout',f"The τ=.90 archive retains {len(complete90)} complete named contrasts, with {sum(bool(r['direction_reversal']) for r in complete90)} directional reversals relative to their own .95 references. The FX primary and matched comparisons remain separately named; Treasury primary and matched coincide and count once. At τ=.99, {sum(r['status']=='NA' for r in level99)} of {len(level99)} named contrasts remain unavailable. The validation causes are {causes99}. No unavailable comparison supplies an evaluated .99 robustness result. Percentage loss changes, where reported in the public record, use the same-target F denominator and are not changes in the .95 objective.",p5)
    prose('limits','The complete records support assessment of the executed procedures on these measurement tasks, including adverse directions, raw-p failures and method unavailability. They do not establish independent replication, universal model superiority, prospective public-release performance or conditional coverage. Treasury uses a downloaded-vintage economic-date replay; the aggregate signed-position peak is not a reconstruction of individual dealer inventories. No new analysis in this Supplement changes either original primary value.',all_inputs)
    for source in ('fx_hourly','nyfed_weekly'):
        rows=[r for r in w3['murphy'] if r['source']==source]
        key='figure-wp3-'+source;figure_keys.append(key)
        context=('This matched F context is distinct from the original FX QR W2880 versus rolling F W720 primary. '
                 if source=='fx_hourly' else
                 'Here the matched F component is also the original-primary historical reference; the plotted pairs compare fixed combinations with constituents rather than the original QR-minus-F pair. ')
        put(key,dict(path='figures/wp3-murphy-'+source+'.pdf',
                     caption=f"Matched-constituent elementary-score comparisons for {_source(rows[0])}, H{rows[0]['horizon']}, W{rows[0]['window']}, τ={_num(rows[0]['tau'])}. The {len(rows)} mean/median-minus-constituent comparisons have exact rankings "+', '.join(r['ranking'] for r in rows)+'. Signs are determined at every unique breakpoint before drawing these display curves. '+context+'Crossing excludes sample dominance for the named pair and does not certify conditional coverage.'),p3)
    return blocks,figure_keys


def generated(key):
    """Regenerate one context exactly for the source-bound numeric dispatcher."""
    blocks,_=_build()
    return deepcopy(blocks[key.removeprefix(PREFIX)])


def additional_section():
    blocks,figures=_build()
    return dict(title='S16. Additional benchmarks and robustness',
                blocks=[deepcopy(block) for key,block in blocks.items() if key not in figures])


def additional_figures():
    blocks,keys=_build()
    return [deepcopy(blocks[key]) for key in keys]
