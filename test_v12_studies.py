"""Protocol gates and result-independent runtime ladders, on synthetic metadata."""
import importlib
import importlib.util
import json
import subprocess
import time


def api():
    assert importlib.util.find_spec('run_v12_studies') is not None, 'v12 parent driver is not implemented'
    return importlib.import_module('run_v12_studies')


def cell(family, window, *, tau=.95, key='toy', validation_n=52):
    return dict(cell_id=f'{family}-{key}-{window}-{tau}-{validation_n}', family=family,
                source_key=key, period='original', horizon=6, window=window,
                refit_step=13, validation_first=100, validation_last=100+validation_n-1,
                evaluation_first=400, evaluation_last=659, tau=tau)


def test_workload_counts_metadata_not_observed_losses():
    m = api()
    a = cell('cftc', 52)
    b = dict(a, actual_excess_pct=-99999)
    assert m.work_units(a, 'F1') == m.work_units(b, 'F1') > 0
    assert m.work_units(cell('cftc', 260), 'F1') == 5*m.work_units(a, 'F1')


def test_f1_trims_fx_then_panel_long_history_and_keeps_core():
    m = api()
    cells = [cell('fx', 2880), cell('panel', 260), cell('panel', 52), cell('cftc', 260)]
    r = m.predeclared_scope('F1', cells, seconds_per_work=1e6, remaining_seconds=1)
    assert [x['family'] for x in r['omitted']] == ['fx', 'panel']
    assert {x['family'] for x in r['cells']} == {'panel', 'cftc'}
    assert all(x['window'] != 260 or x['family'] != 'panel' for x in r['cells'])


def test_f2_trims_entire_secondary_method_before_long_history():
    m = api()
    cells = [cell('cftc', 52), cell('cftc', 260)]
    r = m.predeclared_scope('F2', cells, seconds_per_work=1e6, remaining_seconds=1)
    assert r['trim_steps'][:2] == ['omit_QR4', 'omit_W260']
    assert len(r['cells']) == 1 and r['cells'][0]['window'] == 52
    assert r['cells'][0]['methods'] == ['QR33']


def test_f3_keeps_all_primary_cftc_cells_and_trims_tau90_first():
    m = api()
    cells = [cell('cftc', 52, tau=.99, key='a'), cell('cftc', 260, tau=.99, key='b'),
             cell('fx', 2880, tau=.99), cell('bill', 260, tau=.99), cell('cftc', 52, tau=.90)]
    r = m.predeclared_scope('F3', cells, seconds_per_work=1e6, remaining_seconds=1)
    assert r['trim_steps'][0] == 'omit_tau90'
    assert len(r['cells']) == 2
    assert all(x['family'] == 'cftc' and x['tau'] == .99 for x in r['cells'])


def test_protocol_readback_is_the_committed_frozen_design():
    m = api()
    for name, expected in [('F1', 3600), ('F2', 2400), ('F3', 1500)]:
        d, provenance = m.read_design(name)
        assert d['experiment'] == name
        assert provenance['working_bytes_equal_design_commit'] is True
        assert m.wall_cap(d) == expected


def test_scope_retains_all_cells_when_resource_estimate_fits():
    m = api()
    for experiment in ['F1', 'F2', 'F3']:
        cells = [cell('cftc', 52, tau=.99 if experiment == 'F3' else .95)]
        r = m.predeclared_scope(experiment, cells, seconds_per_work=0., remaining_seconds=1)
        assert len(r['cells']) == 1 and not r['omitted'] and not r['trim_steps']


def test_f2_jobs_separate_methods_in_the_frozen_primary_first_order():
    m = api()
    a = cell('cftc', 52, key='a'); a.update(source={'source_index':0}, validation_n=52)
    b = dict(a, cell_id='a-long-validation', validation_n=156)
    c = dict(a, cell_id='a-long-history', window=260)
    groups = m.group_jobs([b,c,a], 'F2')
    assert [g[0]['methods'] for g in groups] == [['QR33'],['QR33'],['QR4'],['QR4']]
    assert [g[0]['window'] for g in groups] == [52,260,52,260]
    assert [x['validation_n'] for x in groups[0]] == [52,156]


def test_results_from_separate_method_jobs_merge_without_overwriting():
    m = api()
    a = {'cell':{'cell_id':'a'},'rows':[{'method':'QR33','status':'COMPLETE'}],'candidates':[{'x':1}]}
    b = {'cell':{'cell_id':'a'},'rows':[{'method':'QR4','status':'FAILED'}],'candidates':[{'x':2}]}
    r = m.merge_cell_results([a,b])['a']
    assert [x['method']for x in r['rows']] == ['QR33','QR4']
    assert len(r['candidates']) == 2


def test_preflight_excludes_every_geometry_of_a_bad_source_before_launch():
    m = api()
    a = cell('cftc',52,key='a'); b = cell('cftc',260,key='a'); c = cell('cftc',52,key='b')
    eligibility = [{'source_key':'a','eligible':True,'status':'ELIGIBLE'},
                   {'source_key':'b','eligible':True,'status':'ELIGIBLE'}]
    status = {('cftc','a'):{'status':'FAILED_SOURCE','reason':'HASH_MISMATCH'},
              ('cftc','b'):{'status':'VERIFIED'}}
    kept, excluded = m.preflight_cells([a,b,c],status,eligibility)
    assert [x['source_key']for x in kept] == ['b']
    assert len(excluded) == 2
    assert eligibility[0]['eligible'] is False
    assert eligibility[0]['status'] == 'EXCLUDED_ENTIRE_CONTRACT'


def test_public_design_ancestor_remains_usable_in_published_history(tmp_path, monkeypatch):
    m = api()
    def g(*args):
        return subprocess.check_output(['git','-c','user.name=V12 Toy','-c',
            'user.email=v12-toy@example.invalid',*args],cwd=tmp_path,stderr=subprocess.PIPE).decode().strip()
    g('init','-q');(tmp_path/'README').write_text('toy\n');g('add','README');g('commit','-qm','base')
    base = g('rev-parse','HEAD');g('switch','-qc','research')
    p = tmp_path/'protocol/v12/toy.md';p.parent.mkdir(parents=True)
    raw = '# Toy\n```json\n'+json.dumps({'experiment':'F1','inherited_code_sha256':{},'runtime':{'total_cap_seconds':1}})+'\n```\n'
    p.write_text(raw);g('add','protocol');g('commit','-qm','standalone design');original=g('rev-parse','HEAD')
    g('switch','-qc','published',base);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(raw)
    g('add','protocol');g('commit','-qm','publish exact standalone design');published=g('rev-parse','HEAD')
    # Force distinct histories even on fast machines whose two commit seconds coincide.
    if original == published:
        g('commit','--amend','-qm','different public design identity');published=g('rev-parse','HEAD')
    monkeypatch.setattr(m,'ROOT',tmp_path)
    monkeypatch.setattr(m,'DESIGNS',{'F1':('toy.md',original,published)})
    _, provenance = m.read_design('F1')
    assert provenance['accepted_design_commit']==published
    assert provenance['working_bytes_equal_design_commit'] is True


def test_hard_deadline_retains_a_completed_method_without_final_stdout(tmp_path, monkeypatch):
    m=api();monkeypatch.setattr(m,'ROOT',tmp_path)
    child=tmp_path/'v12_runner.py'
    child.write_text("import sys,json,time,pathlib\ns=json.loads(pathlib.Path(sys.argv[-1]).read_text())\np=pathlib.Path(s['output_root'])/'a';p.mkdir(parents=True)\n(p/'QR33.result.json').write_text(json.dumps({'method':'QR33','status':'COMPLETE','actual_loss':1.0}))\n(p/'cell-result.json').write_text('{\\\"rows\\\":[')\ntime.sleep(5)\n")
    c=cell('bill',52);c['cell_id']='a';private=tmp_path/'private';private.mkdir()
    results,records,missing=m.start_jobs([[c]],'F1',private,{},time.monotonic()+.5,workers=1)
    assert len(records)==1 and records[0]['timed_out']
    assert not missing
    assert results[0]['rows'][0]['status']=='COMPLETE'
    assert results[0]['read_only_salvage'] is True


def test_missing_row_status_distinguishes_attempted_primary_from_unstarted_secondary():
    m=api()
    launched={('a','QR33'):'FAILED_RESOURCE'}
    omitted={('a','QR4')}
    assert m.missing_row_status(('a','QR33'),launched,omitted)=='FAILED_RESOURCE'
    assert m.missing_row_status(('a','QR4'),launched,omitted)=='NOT_RUN_RESOURCE_LIMIT'
    assert m.missing_row_status(('a','QR33'),launched,omitted|{('a','QR33')})=='FAILED_RESOURCE'
