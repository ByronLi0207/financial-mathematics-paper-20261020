"""Report tests use only manually assembled JSON archives in tmp_path."""
import copy
import hashlib
import importlib
import json
from pathlib import Path

import pytest


def api():
    assert Path(__file__).with_name('summarize_v9_nonstationarity.py').exists(), 'archive-only reporter is absent'
    return importlib.import_module('summarize_v9_nonstationarity')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def fixture_archive(path, methods=('QR33', 'QR4')):
    sources = [dict(source_id=f's{i:02}', kind='weekly', stop=405) for i in range(13)]
    sources += [dict(source_id='fx_daily', kind='daily', stop=405), dict(source_id='fx_hourly', kind='hourly', stop=8109)]
    diagnostics = []
    for i, source in enumerate(sources):
        n = source['stop']
        cuts = [201] if source['kind'] == 'weekly' else [134, 269] if source['kind'] == 'daily' else [4000]
        bounds = [0, *cuts, n-1]
        diagnostics.append(dict(source, n=n, M=n-1, status='COMPLETE', p_value=.001 if i < 8 or i == 13 else .5,
                                statistic=float(i+1), moment=dict(qualified=True, nu_gt4=True, kappa=4.2, q4=.6),
                                partition=dict(cuts=cuts, segment_lengths=[b-a for a,b in zip(bounds[:-1],bounds[1:])],
                                               min_segment=104 if n == 405 else 1622, cap_reached=len(cuts) == 2),
                                break_dates=['2018-01-01']*len(cuts), calibration_status='COMPLETE' if i < 13 else 'NOT_A_FORECAST_SOURCE'))
    summary, records = [], []
    for source in sources[:13]:
        for arm in ['constant', 'switching']:
            for window in [52, 260]:
                for method in methods:
                    value = (0. if window == 52 else .5) if arm == 'constant' else (6. if window == 52 else 7.)
                    if method == 'QR4':
                        value += 1.
                    row = dict(source_id=source['source_id'], arm=arm, window=window, method=method,
                               status='COMPLETE', required_repetitions=2, completed_repetitions=2,
                               failed_repetitions=[], relative_median_pct=value, q25_pct=value-.25,
                               q75_pct=value+.25, win_fraction=0.5 if value == 0 else 0.,
                               qr_breach_median=4/72, f_breach_median=3/72)
                    summary.append(row)
                    for rep, delta in enumerate([-.5, .5]):
                        records.append(dict(source_id=source['source_id'], arm=arm, window=window, method=method,
                                            rep=rep, status='COMPLETE', n=72, qr_mean_loss=100+value+delta,
                                            f_mean_loss=100., qr_breaches=4, f_breaches=3))
    predictions = dict(N1=dict(status='SUPPORTED', known_rejections=8, maximum_rejections=8, unknown=0),
                       N2=dict(status='SUPPORTED', switching_W52_median_pct=6., switching_W260_median_pct=7.),
                       N3=dict(status='SUPPORTED', constant_W52_median_pct=0.),
                       N4=dict(status='SUPPORTED', daily_breaks_per100=200/405, hourly_breaks_per100=100/8109))
    manifest = dict(schema='artificial-test-archive', design_commit='artificial-design', started_utc='2026-01-01T00:00:00+00:00',
                    sources=sources, design=dict(windows=[52,260], fx_common_calendar_start='2014-02-05T00:00:00',
                                               fx_common_calendar_stop_exclusive='2015-05-24T00:00:00',
                                               alpha=.05, N1_min_rejections=7, N2_median_percent_strict_min=5.,
                                               N3_median_percent_inclusive_bounds=[-3.,3.]))
    payloads = {'diagnostics.json': diagnostics, 'summary.json': summary, 'predictions.json': predictions,
                'formal/replicate-scores.json': records, 'manifest.json': manifest}
    for name, value in payloads.items():
        write(path/name, value)
    return payloads


def fail_cell(path, payloads, *, method='QR33', arm='switching', window=52):
    row = next(x for x in payloads['summary.json'] if x['source_id'] == 's00' and x['method'] == method and x['arm'] == arm and x['window'] == window)
    row.update(status='FAILED', completed_repetitions=1, failed_repetitions=[1], relative_median_pct=None,
               q25_pct=None, q75_pct=None, win_fraction=None, qr_breach_median=None, f_breach_median=None)
    payloads['formal/replicate-scores.json'] = [r for r in payloads['formal/replicate-scores.json'] if not (r['source_id']=='s00' and r['method']==method and r['arm']==arm and r['window']==window and r['rep']==1)]
    if method == 'QR33' and arm == 'switching':
        payloads['predictions.json']['N2'].update(status='UNASSESSABLE', **{f'switching_W{window}_median_pct': None})
    for name in ['summary.json', 'formal/replicate-scores.json', 'predictions.json']:
        write(path/name, payloads[name])


def test_complete_archive_produces_15_diagnostics_104_cells_and_real_artifacts(tmp_path):
    m = api()
    fixture_archive(tmp_path)
    report = m.build_report(tmp_path)
    assert len(report['diagnostics']) == 15 and len(report['cells']) == 104
    assert len(report['across_source']) == 4
    assert all(r['complete_sources'] == 13 and r['median_pct'] is not None for r in report['across_source'])
    assert report['predictions']['N1']['status'] == 'SUPPORTED'
    assert report['predictions']['N4']['daily_breaks_per_calendar_year'] > report['predictions']['N4']['hourly_breaks_per_calendar_year']
    assert (tmp_path/'analysis/qr33-comparison.png').read_bytes().startswith(b'\x89PNG')
    assert (tmp_path/'analysis/qr33-comparison.pdf').read_bytes().startswith(b'%PDF')
    assert '人工' in (tmp_path/'analysis/research-memo-zh.md').read_text()


def test_failed_required_source_removes_preset_aggregate_but_labels_completed_description(tmp_path):
    m = api(); payloads = fixture_archive(tmp_path)
    fail_cell(tmp_path, payloads)
    report = m.build_report(tmp_path)
    row = next(r for r in report['across_source'] if r['arm']=='switching' and r['window']==52)
    assert row['median_pct'] is None and row['complete_sources'] == 12
    assert row['completed_only_median_pct'] == pytest.approx(6.)
    assert row['status'] == 'UNASSESSABLE'
    assert report['predictions']['N2']['status'] == 'UNASSESSABLE'
    assert '不作为预设命题' in (tmp_path/'analysis/research-memo-zh.md').read_text()


def test_qr4_failure_does_not_destroy_complete_qr33_primary(tmp_path):
    m = api(); payloads = fixture_archive(tmp_path)
    fail_cell(tmp_path, payloads, method='QR4')
    report = m.build_report(tmp_path)
    assert report['predictions']['N2']['status'] == 'SUPPORTED'


def test_nonregular_null_is_unknown_not_stability(tmp_path):
    m = api(); p = fixture_archive(tmp_path)
    for row in p['diagnostics.json'][:13]:
        if row['source_id'] >= 's06':
            row.update(status='NONREGULAR_NULL', p_value=None, moment=dict(qualified=False, nu_gt4=False, q4=None, kappa=None))
    p['predictions.json']['N1'] = dict(status='UNASSESSABLE',known_rejections=6,maximum_rejections=13,unknown=7,
                                     holm_p_by_source={f's{i:02}':.013 if i<6 else 1. for i in range(13)})
    write(tmp_path/'diagnostics.json',p['diagnostics.json']);write(tmp_path/'predictions.json',p['predictions.json'])
    report = m.build_report(tmp_path)
    assert report['predictions']['N1']['status'] == 'UNASSESSABLE'
    assert report['diagnostics'][6]['p_value'] is None
    assert report['diagnostics'][6]['holm13_p'] is None
    assert report['diagnostics'][6]['holm_internal_placeholder']
    assert report['archived_predictions']['N1']['holm_p_by_source']['s06']==1.
    assert report['diagnostics'][6]['global_interpretation'] == '不可评估'


def test_summary_disagreement_stops_before_any_output(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    p['summary.json'][0]['relative_median_pct']=90.
    write(tmp_path/'summary.json',p['summary.json'])
    with pytest.raises(m.ArchiveError,match='SUMMARY'):
        m.build_report(tmp_path)
    assert not (tmp_path/'analysis').exists()


def test_prediction_disagreement_stops_before_any_output(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    p['predictions.json']['N2']['status']='NOT_SUPPORTED'
    write(tmp_path/'predictions.json',p['predictions.json'])
    with pytest.raises(m.ArchiveError,match='PREDICTION'):
        m.build_report(tmp_path)
    assert not (tmp_path/'analysis').exists()


def test_all_source_files_stay_identical_and_second_report_never_overwrites(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    before={name:hashlib.sha256((tmp_path/name).read_bytes()).hexdigest() for name in p}
    m.build_report(tmp_path)
    output=tmp_path/'analysis/research-memo-zh.md';saved=output.read_bytes()
    with pytest.raises(FileExistsError):
        m.build_report(tmp_path)
    assert output.read_bytes()==saved
    assert before=={name:hashlib.sha256((tmp_path/name).read_bytes()).hexdigest() for name in p}


def test_reduced_qr33_grid_has_exactly_52_cells(tmp_path):
    m=api();fixture_archive(tmp_path,methods=('QR33',))
    report=m.build_report(tmp_path)
    assert len(report['cells'])==52


def test_unarchived_break_dates_are_missing_not_invented(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    p['diagnostics.json'][13].pop('break_dates')
    write(tmp_path/'diagnostics.json',p['diagnostics.json'])
    report=m.build_report(tmp_path)
    assert report['diagnostics'][13]['break_dates']==[]
    assert 'BREAK_DATES_NOT_ARCHIVED' in report['diagnostics'][13]['failures']


def test_nonregular_with_numeric_primary_p_is_inconsistent_archive(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    p['diagnostics.json'][0]['status']='NONREGULAR_NULL'
    p['diagnostics.json'][0]['moment']['qualified']=False
    write(tmp_path/'diagnostics.json',p['diagnostics.json'])
    with pytest.raises(m.ArchiveError,match='DIAGNOSTIC'):
        m.build_report(tmp_path)


def test_n3_failure_is_reported_as_contrary_constant_control_evidence(tmp_path):
    m=api();p=fixture_archive(tmp_path)
    for cell in p['summary.json']:
        if cell['arm']=='constant' and cell['window']==52 and cell['method']=='QR33':
            cell.update(relative_median_pct=8.,q25_pct=7.75,q75_pct=8.25,win_fraction=0.)
    for row in p['formal/replicate-scores.json']:
        if row['arm']=='constant' and row['window']==52 and row['method']=='QR33':
            row['qr_mean_loss']+=8.
    p['predictions.json']['N3']=dict(status='NOT_SUPPORTED',constant_W52_median_pct=8.)
    for name in ['summary.json','formal/replicate-scores.json','predictions.json']:write(tmp_path/name,p[name])
    report=m.build_report(tmp_path)
    memo=(tmp_path/'analysis/research-memo-zh.md').read_text()
    assert report['predictions']['N3']['status']=='NOT_SUPPORTED'
    assert '相反证据' in memo and '不能概括为' in memo
