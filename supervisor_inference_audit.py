"""Read-only trace audit; writes new supervisor E1/E2/E4 results only.

Original inference_tests.py is imported byte for byte. This helper independently
checks its statistical arithmetic and corrects the conditional CC initialization
in a new output; no archived result or forecast is modified.
"""
import sys
sys.dont_write_bytecode = True
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_name] = '1'
import argparse
import csv
import hashlib
import io
import json
import math
import shutil
from pathlib import Path
import numpy as np
from inference_tests import dm_test, coverage_tests, holm, murphy, student_two_sided

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / '金融数学论文-修订v3-20261023'
OUT = ROOT / 'results/supervisor-20261023/inference'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rows(path):
    with Path(path).open(newline='') as handle:
        return list(csv.DictReader(handle))

def output(name, data):
    if not data:
        raise ValueError('empty output')
    buf = io.StringIO(newline='')
    writer = csv.DictWriter(buf, fieldnames=list(data[0]))
    writer.writeheader()
    writer.writerows(data)
    (OUT / name).write_text(buf.getvalue())

def load_traces(source_root=PRIOR):
    """Return original B5 arrays; no data reloading, estimation or file mutation."""
    source_root = Path(source_root)
    attempt = source_root / '.scratch/revision-20261022/replication-revision-v3-b5-full'
    audit = json.loads((attempt / 'numerical-audit/public/reproduction-comparison.json').read_text())
    assert audit['status'] == 'NUMERICAL_AUDIT_VERIFIED' and audit['exact_csv_byte_agreement']
    assert sha(attempt/'evaluation-queue.json') == audit['queue_sha256']
    queue = json.loads((attempt / 'evaluation-queue.json').read_text())
    result = {}
    for cell in queue['cells']:
        receipt_path=source_root/cell['receipt_path']
        assert sha(receipt_path)==cell['receipt_sha256']
        receipt=json.loads(receipt_path.read_text())
        path = receipt_path.parent.parent / 'private/numeric-traces.npz'
        trace_sha=sha(path)
        artifact=[entry for entry in receipt['artifacts'] if entry['area']=='private' and entry['name']=='numeric-traces.npz']
        assert len(artifact)==1 and artifact[0]['sha256']==trace_sha
        with np.load(path, allow_pickle=False) as values:
            for name in values.files:
                if not name.endswith('_origins'):
                    continue
                method = name[:-8]
                key = (cell['source'], cell['horizon'], cell['window'], method)
                array = {field: values[method + '_' + field].copy()
                         for field in ('origins', 'capacity', 'peak', 'floor', 'pinball')}
                if key in result:
                    for field in array:
                        assert np.array_equal(result[key][field], array[field]), (key, field)
                result[key] = array
        assert sha(path)==trace_sha
    return result

def independent_dm(difference, horizon, lag):
    """Scalar math.fsum autocovariances, independent of NumPy matrix HAC."""
    values = list(map(float, difference))
    n = len(values)
    mean = math.fsum(values) / n
    centered = [x - mean for x in values]
    gamma = [math.fsum(centered[i] * centered[i-k] for i in range(k, n)) / n
             for k in range(lag + 1)]
    variance = gamma[0] + 2 * math.fsum((1-k/(lag+1)) * gamma[k] for k in range(1, lag+1))
    if all(x == values[0] for x in values) or variance <= 0:
        return mean, variance, None, None
    statistic = mean / math.sqrt(variance/n)
    return mean, variance, statistic, math.erfc(abs(statistic)/math.sqrt(2))

def independent_student_tail(statistic, degrees):
    """Numerical angle-integral of Student density, no incomplete beta helper."""
    lower = math.atan(abs(statistic)/math.sqrt(degrees))
    upper = math.pi/2
    constant = math.exp(math.lgamma((degrees+1)/2)-math.lgamma(degrees/2))/math.sqrt(math.pi)
    def density(angle):
        cosine = max(0., math.cos(angle))
        return cosine**(degrees-1) if cosine else (1. if degrees == 1 else 0.)
    def integrate(a, b, fa, fb, fm, whole, tolerance, depth):
        mid = (a+b)/2
        fl, fr = density((a+mid)/2), density((mid+b)/2)
        left = (mid-a)*(fa+4*fl+fm)/6
        right = (b-mid)*(fm+4*fr+fb)/6
        delta = left+right-whole
        if depth == 0 or abs(delta) <= 15*tolerance:
            return left+right+delta/15
        return (integrate(a, mid, fa, fm, fl, left, tolerance/2, depth-1)
                + integrate(mid, b, fm, fb, fr, right, tolerance/2, depth-1))
    fa, fb, fm = density(lower), density(upper), density((lower+upper)/2)
    whole = (upper-lower)*(fa+4*fm+fb)/6
    return 2*constant*integrate(lower, upper, fa, fb, fm, whole, 1e-14, 30)

def independent_coverage(hits, nominal=.05):
    """Binomial POF full n; transition-based IND and conditional UC/CC n-1."""
    hits = list(map(int, hits))
    n, k = len(hits), sum(hits)
    def ll(success, total, probability):
        if (success and probability == 0) or (success < total and probability == 1):
            return -math.inf
        return ((success*math.log(probability) if success else 0.)
                + ((total-success)*math.log1p(-probability) if total-success else 0.))
    def pof(success, total):
        return max(0., 2*(ll(success, total, success/total)-ll(success, total, nominal)))
    counts = [[sum(a == i and b == j for a, b in zip(hits, hits[1:]))
               for j in range(2)] for i in range(2)]
    full_uc = pof(k, n)
    conditional_uc = pof(sum(hits[1:]), n-1) if n > 1 else None
    result = dict(n=n, hits=k, rate=k/n, first_hit=hits[0],
                  pof_lr=full_uc, pof_p=math.erfc(math.sqrt(full_uc/2)),
                  conditional_uc_lr=conditional_uc,
                  conditional_uc_p=math.erfc(math.sqrt(conditional_uc/2)) if conditional_uc is not None else None,
                  ind_lr=None, ind_p=None, cc_lr=None, cc_p=None,
                  cc_initialization='condition_on_first_hit_n_minus_1',
                  ind_status='UNIDENTIFIED_TRANSITION_ROW',
                  boundary=any(value == 0 for row in counts for value in row))
    result.update({f'n{i}{j}': counts[i][j] for i in range(2) for j in range(2)})
    if all(sum(row) for row in counts):
        total1 = sum(row[1] for row in counts)
        common = ll(total1, n-1, total1/(n-1))
        markov = math.fsum(ll(row[1], sum(row), row[1]/sum(row)) for row in counts)
        independence = max(0., 2*(markov-common))
        conditional = max(0., 2*(markov-ll(total1, n-1, nominal)))
        assert math.isclose(conditional, conditional_uc+independence, abs_tol=2e-10)
        result.update(ind_lr=independence, ind_p=math.erfc(math.sqrt(independence/2)),
                      cc_lr=conditional, cc_p=math.exp(-conditional/2),
                      ind_status='BOUNDARY_REFERENCE' if result['boundary'] else 'OK')
    return result

def independent_murphy(left, right, outcome, tau=.95):
    """All-range scores by endpoint counts, independent of weighted event sums."""
    theta = np.unique(np.concatenate([left, right, outcome]))
    def score(forecast):
        above = forecast > outcome
        below = forecast < outcome
        count = lambda endpoint: np.searchsorted(np.sort(endpoint), theta, side='right')
        over = count(outcome[above])-count(forecast[above])
        under = count(forecast[below])-count(outcome[below])
        return ((1-tau)*over+tau*under)/len(outcome)
    sl, sr = score(left), score(right)
    difference = sl-sr
    integral = math.fsum(map(float, np.diff(theta)*difference[:-1]))
    tolerance = 64*np.finfo(float).eps*max(1., float(sl.max()), float(sr.max()))
    return theta, sl, sr, difference, integral, tolerance

def render_murphy_panels(panels):
    """Draw every exact step, using the independent endpoint-count scores."""
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    pdf=canvas.Canvas(str(OUT/'murphy-two-primary-exact.pdf'),pagesize=(720,305),invariant=1)
    pdf.setTitle('Exact empirical Murphy diagrams for the two original primary comparisons')
    for index,(source,theta,left,right) in enumerate(panels):
        x0,y0,width,height=55+index*357,55,288,190
        scale=1e6 if source=='fx_hourly' else 1.
        minimum,maximum=float(theta[0]/scale),float(theta[-1]/scale)
        margin=(maximum-minimum)*.02
        xmin,xmax=minimum-margin,maximum+margin
        ymax=max(float(left.max()),float(right.max()))*1.08
        X=lambda value:x0+(value/scale-xmin)/(xmax-xmin)*width
        Y=lambda value:y0+value/ymax*height
        pdf.setFillColor(colors.HexColor('#182b45'))
        pdf.setFont('Times-Bold',12)
        pdf.drawString(x0,276,'FX, H = 6' if source=='fx_hourly' else 'Treasury, H = 6')
        pdf.setFont('Times-Roman',9)
        pdf.drawString(x0,261,'QR versus rolling F' if source=='fx_hourly' else 'QR versus matched frozen F')
        pdf.setStrokeColor(colors.HexColor('#b8c1cc'))
        for fraction in [0,.25,.5,.75,1.]:
            pdf.line(x0,y0+fraction*height,x0+width,y0+fraction*height)
            pdf.setFillColor(colors.HexColor('#34465f'))
            pdf.setFont('Times-Roman',8)
            pdf.drawRightString(x0-5,y0+fraction*height-3,f'{fraction*ymax:.3f}')
            pdf.drawCentredString(x0+fraction*width,y0-13,f'{xmin+fraction*(xmax-xmin):.0f}')
        for scores,color in [(left,'#af3e34'),(right,'#24638c')]:
            path=pdf.beginPath()
            path.moveTo(x0,Y(0))
            for j,(threshold,score) in enumerate(zip(theta,scores)):
                path.lineTo(X(threshold),Y(float(scores[j-1]) if j else 0.))
                path.lineTo(X(threshold),Y(float(score)))
            path.lineTo(x0+width,Y(0))
            pdf.setStrokeColor(colors.HexColor(color))
            pdf.setLineWidth(.8)
            pdf.drawPath(path)
        pdf.setFont('Times-Roman',9)
        pdf.setFillColor(colors.HexColor('#af3e34'));pdf.drawString(x0+178,261,'QR')
        pdf.setFillColor(colors.HexColor('#24638c'));pdf.drawString(x0+211,261,'F')
        pdf.setFillColor(colors.HexColor('#34465f'))
        pdf.drawCentredString(x0+width/2,23,'Threshold (USD millions)')
    pdf.setFont('Times-Roman',9)
    pdf.setFillColor(colors.HexColor('#34465f'))
    pdf.drawCentredString(360,294,'Mean elementary quantile score, quantile level 0.95')
    pdf.showPage();pdf.save()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    imported = OUT/'inherited-exact'
    imported.mkdir(exist_ok=True)
    import_names = ['dm.csv', 'holm.csv', 'coverage.csv', 'murphy-summary.csv',
                    'murphy-fx_hourly-display.csv', 'murphy-nyfed_weekly-display.csv',
                    'murphy-fx_hourly.pdf', 'murphy-nyfed_weekly.pdf']
    imports = []
    for name in import_names:
        src = PRIOR/'results/revision-20261023/inference'/name
        dst = imported/name
        contents = src.read_bytes()
        dst.write_bytes(contents)
        imports.append(dict(source=str(src), destination=str(dst), sha256=sha(src), bytes=len(contents)))
        assert sha(src) == sha(dst)
    assert sha(PRIOR/'inference_tests.py') == sha(ROOT/'inference_tests.py')
    imports.append(dict(source=str(PRIOR/'inference_tests.py'), destination=str(ROOT/'inference_tests.py'),
                        sha256=sha(ROOT/'inference_tests.py'), bytes=(ROOT/'inference_tests.py').stat().st_size))
    archive_files = ['paired-comparisons.csv', 'evaluation-summary.csv', 'evaluation-nonoverlap.csv']
    archive_checks = []
    for name in archive_files:
        current = ROOT/'results/revision-20261022'/name
        prior = PRIOR/'results/revision-20261022'/name
        assert sha(current) == sha(prior), name
        archive_checks.append(dict(file=name, current_sha256=sha(current), prior_sha256=sha(prior), exact=True))
    traces = load_traces()
    comparisons = rows(ROOT/'results/revision-20261022/paired-comparisons.csv')
    imported_dm = {row['contrast_id']: row for row in rows(imported/'dm.csv')}
    dm_rows = []
    maximum_dm_error = 0.
    for row in comparisons:
        if row['contrast_category'] == 'update_frequency':
            continue
        key = lambda side: (row['source'], int(row['horizon']), int(row[side+'_window']), row[side+'_method'])
        left, right = traces[key('left')], traces[key('right')]
        assert np.array_equal(left['origins'], right['origins'])
        assert np.array_equal(left['peak'], right['peak'])
        difference = left['pinball']-right['pinball']
        horizon = int(row['horizon'])
        result = dm_test(difference, horizon)
        expected = float(row['mean_pinball_difference'])
        assert result['mean_difference'] == expected
        independent = independent_dm(difference, horizon, result['bandwidth'])
        assert math.isclose(independent[1], result['lrv'], rel_tol=2e-12, abs_tol=1e-10)
        if result['status'] == 'OK':
            error = abs(independent[2]-result['dm_t'])
            maximum_dm_error = max(maximum_dm_error, error)
            assert error < 1e-10
            inherited = imported_dm[row['contrast_id']]
            assert float(inherited['dm_t']) == result['dm_t']
            assert float(inherited['dm_p']) == result['dm_p']
            assert float(inherited['hln_t']) == result['hln_t']
            assert float(inherited['hln_p']) == result['hln_p']
        double = dm_test(difference, horizon, min(len(difference)-1, 2*result['bandwidth']))
        if result['status']=='OK':
            assert float(inherited['double_dm_t'])==double['dm_t']
            assert float(inherited['double_dm_p'])==double['dm_p']
            assert float(inherited['double_hln_p'])==double['hln_p']
        dm_rows.append(dict(contrast_id=row['contrast_id'], source=row['source'],
                            left_window=row['left_window'], left_method=row['left_method'],
                            right_window=row['right_window'], right_method=row['right_method'],
                            category=row['contrast_category'], primary=row['declared_source_primary'],
                            legacy=row['h24_legacy_contrast'], **result,
                            double_bandwidth=double['bandwidth'], double_dm_t=double['dm_t'],
                            double_dm_p=double['dm_p'], double_hln_p=double['hln_p']))
    assert len(dm_rows) == 74
    family = [row for row in dm_rows if row['category'] == 'common_history']
    assert len(family) == 72
    p = [row['dm_p'] if row['status'] == 'OK' else 1. for row in family]
    double_p = [row['double_dm_p'] if row['status'] == 'OK' else 1. for row in family]
    hln_p = [row['hln_p'] if row['status'] == 'OK' else 1. for row in family]
    adjusted, double_adjusted, hln_adjusted = holm(p), holm(double_p), holm(hln_p)
    independent_adjusted = [min(1., max((72-i)*p[j] for i,j in enumerate(sorted(range(72),key=lambda j:p[j]))
                                      if p[j] <= value)) for value in p]
    np.testing.assert_allclose(independent_adjusted, adjusted, rtol=0, atol=1e-15)
    for row, raw, adj, dadj, hadj in zip(family, p, adjusted, double_adjusted, hln_adjusted):
        row.update(holm_family_size=72, holm_input_p=raw, holm_p=float(adj),
                   double_holm_p=float(dadj), hln_holm_p=float(hadj))
    inherited_holm={r['contrast_id']:r for r in rows(imported/'holm.csv')}
    assert set(inherited_holm)=={r['contrast_id'] for r in family}
    for row in family:
        assert row['holm_p']==float(inherited_holm[row['contrast_id']]['holm_p'])
    # All rows have the same output schema; cross-window FX has no family p.
    for row in dm_rows:
        if 'holm_p' not in row:
            row.update(holm_family_size=None, holm_input_p=None, holm_p=None, double_holm_p=None, hln_holm_p=None)
    output('dm-verified.csv', dm_rows)
    output('holm72-verified.csv', family)
    table_rows = []
    summary = rows(ROOT/'results/revision-20261022/evaluation-summary.csv')
    by_cell = {(r['source'],int(r['horizon']),int(r['window']),r['method']):r for r in summary}
    dm_map = {(r['source'],int(r['horizon']),int(r['left_window']),r['left_method']):r
              for r in family if r['right_method'] == 'frozen_F'}
    for source, windows in [('fx_hourly',[720,2880]),('nyfed_weekly',[52,260])]:
        for horizon in [6,24]:
            for window in windows:
                reference = by_cell[source,horizon,window,'frozen_F']
                for method in ['frozen_F','frozen_S','frozen_K','QR','KNN','SCALED_KNN']:
                    row = by_cell[source,horizon,window,method]
                    dm = dm_map.get((source,horizon,window,method))
                    relative = 100*(float(row['mean_pinball'])/float(reference['mean_pinball'])-1)
                    loss = float(row['mean_pinball'])/(1e6 if source == 'fx_hourly' else 1.)
                    breach = float(row['strict_breach_rate'])*100
                    table_rows.append(dict(table=3 if source=='fx_hourly' else 4,source=source,horizon=horizon,
                                           window=window,method=method,origin_count=row['origin_count'],
                                           mean_pinball=loss,display_unit='USD millions',relative_own_f_percent=relative,
                                           breach_count=row['strict_breach_count'],breach_rate_percent=breach,
                                           dm_t=dm['dm_t'] if dm else None,
                                           dm_p=dm['dm_p'] if dm else None,holm_p=dm['holm_p'] if dm else None,
                                           p_status=dm['status'] if dm else ('SELF_REFERENCE' if method=='frozen_F' else 'OUTSIDE_72_FAMILY'),
                                           loss_display=f'{loss:.3f}',relative_display=f'{relative:+.3f}',
                                           breach_rate_display=f'{breach:.3f}',
                                           holm_display=('--' if not dm or dm['status']!='OK' else
                                                         ('<0.001' if dm['holm_p']<.0005 else f"{dm['holm_p']:.3f}"))))
    assert len(table_rows) == 48
    output('tables3-4-ready.csv', table_rows)
    (OUT/'tables3-4-ready.json').write_text(json.dumps(table_rows, indent=2)+'\n')
    coverage = []
    inherited_coverage = {(r['source'],int(r['horizon']),int(r['window']),r['method']):r
                          for r in rows(imported/'coverage.csv')}
    max_coverage_difference = 0.
    for (source,horizon,window,method), trace in traces.items():
        origin = trace['origins']
        assert np.array_equal(origin, np.arange(origin[0],origin[0]+len(origin)))
        assert np.all(trace['capacity'] >= trace['floor'])
        assert np.all(trace['peak'] >= trace['floor'])
        assert np.allclose(trace['pinball'], .95*np.maximum(trace['peak']-trace['capacity'],0)
                           + .05*np.maximum(trace['capacity']-trace['peak'],0), rtol=1e-12,atol=1e-10)
        grid = np.arange(0,len(origin),horizon+1)
        hits = (trace['peak'] > trace['capacity']).astype(int)
        result = independent_coverage(hits[grid])
        inherited = inherited_coverage[source,horizon,window,method]
        assert result['n'] == int(inherited['n']) and result['hits'] == int(inherited['hits'])
        for name in ['pof_lr','pof_p','ind_lr','ind_p']:
            old = None if not inherited[name] else float(inherited[name])
            if old is None:
                assert result[name] is None
            else:
                error = abs(old-result[name])
                max_coverage_difference=max(max_coverage_difference,error)
                assert error < 1e-10
        coverage.append(dict(source=source,horizon=horizon,window=window,method=method,
                             grid_stride=horizon+1,first_origin=int(origin[0]),last_grid_origin=int(origin[grid[-1]]),
                             global_grid_anchor=int(origin[0]),**result,
                             ties_on_grid=int(np.sum(trace['peak'][grid]==trace['capacity'][grid])),
                             floor_atoms_on_grid=int(np.sum(trace['peak'][grid]==trace['floor'][grid])),
                             floor_issued_on_grid=int(np.sum(trace['capacity'][grid]==trace['floor'][grid])),
                             inherited_fulln_plus_ind_cc_lr=inherited['cc_lr'],
                             inherited_fulln_plus_ind_cc_p=inherited['cc_p']))
    assert len(coverage) == 90
    output('coverage-verified.csv',coverage)
    murphy_rows=[]
    murphy_panels=[]
    for row in [r for r in comparisons if r['declared_source_primary']=='True']:
        key=lambda side:(row['source'],int(row['horizon']),int(row[side+'_window']),row[side+'_method'])
        left,right=traces[key('left')],traces[key('right')]
        theta, sl,sr,difference,integral,tolerance=independent_murphy(left['capacity'],right['capacity'],left['peak'])
        inherited=murphy(left['capacity'],right['capacity'],left['peak'])
        assert np.array_equal(theta,inherited['theta'])
        np.testing.assert_allclose(sl,inherited['left'],rtol=0,atol=1e-13)
        np.testing.assert_allclose(sr,inherited['right'],rtol=0,atol=1e-13)
        assert difference.min() < -tolerance and difference.max() > tolerance
        murphy_panels.append((row['source'],theta,sl,sr))
        expected=float(row['mean_pinball_difference'])
        assert abs(integral-expected) < 1e-9*max(1,abs(expected))
        crossing_intervals=int(np.sum(np.diff(np.sign(difference[np.abs(difference)>tolerance]))!=0))
        murphy_rows.append(dict(contrast_id=row['contrast_id'],source=row['source'],tau=.95,
                               breakpoint_count=len(theta),ranking='CROSSING',
                               min_elementary_difference=float(difference.min()),max_elementary_difference=float(difference.max()),
                               sign_crossing_count=crossing_intervals,integral_difference=integral,
                               archived_pinball_difference=expected,absolute_integral_error=abs(integral-expected),
                               arithmetic_tolerance=tolerance,all_real_thresholds_covered=True,
                               support_exterior_scores_zero=True))
    output('murphy-verified.csv',murphy_rows)
    render_murphy_panels(murphy_panels)
    student_checks=[]
    for degrees in [1,2,3,276,6624]:
        for statistic in [0.,.2,1.,2.67,5.18,8.]:
            actual=student_two_sided(statistic,degrees)
            expected=independent_student_tail(statistic,degrees)
            assert abs(actual-expected)<3e-10,(degrees,statistic,actual,expected)
            student_checks.append(dict(df=degrees,t=statistic,inherited=actual,numerical_integral=expected,error=abs(actual-expected)))
    output('student-independent-checks.csv',student_checks)
    receipt=dict(status='VERIFIED_WITH_CC_INITIALIZATION_CORRECTION',post_result=True,
                 previous_results_untouched=True,forecast_refits=0,trace_cells=len(traces),dm_contrasts=74,
                 matched_holm_family_size=72,holm_dm_rejections_005=sum(r['holm_p']<.05 for r in family),
                 holm_double_bandwidth_rejections_005=sum(r['double_holm_p']<.05 for r in family),
                 holm_hln_rejections_005=sum(r['hln_holm_p']<.05 for r in family),
                 exact_identity_family_members=sum(r['status']=='IDENTICAL_LOSSES' for r in family),
                 max_independent_dm_t_absolute_error=maximum_dm_error,
                 max_inherited_pof_ind_absolute_error=max_coverage_difference,
                 archive_agreement=archive_checks,imports=imports,
                 independent_checks=['scalar-fsum HAC','Student angle quadrature','direct Bernoulli likelihoods',
                                     'all-breakpoint endpoint-count Murphy scores','independent Holm sorted-max'],
                 trace_provenance_checks=['audit-pinned queue hash','queue-pinned cell receipt hashes',
                                          'receipt-pinned numeric trace hashes','trace hashes unchanged after loading'],
                 imported_module_dependency_review={'imports':['math','numpy'],
                                                    'top_level_file_network_subprocess_mutations':False},
                 corrections=['Christoffersen conditional CC uses first-hit-conditioned UC and IND on same n-1 transitions'],
                 formal_limits=['post-inspection exploratory references, not confirmatory p-values',
                                'H+1 removes target overlap but not shared training dependence',
                                'exact 5% equality differs from at-most-5% quantile upper-bound calibration with atoms',
                                'HLN MSPE-origin multiplier applied to pinball is approximate',
                                'fixed-window GW interpretation requires weak dependence/moments/positive LRV, unverified'])
    # Confirm source import bytes are stable even while another chat owns prior tree.
    for item in imports:
        assert sha(item['source'])==item['sha256'], 'source changed during read: '+item['source']
    (OUT/'audit-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','dm_contrasts','matched_holm_family_size','holm_dm_rejections_005',
                                          'holm_double_bandwidth_rejections_005','holm_hln_rejections_005','trace_cells']},indent=2))

if __name__=='__main__':
    main()
