"""Artificial ZIP/index fixtures only; no actual study archive is opened."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import zipfile

import pytest


def api():
    assert Path(__file__).with_name('audit_v9_nonstationarity.py').exists(), 'archive auditor is absent'
    return importlib.import_module('audit_v9_nonstationarity')


def fixture(path, methods=('QR33','QR4')):
    sources=[dict(source_id=f's{i:02}',kind='weekly') for i in range(13)]
    sources += [dict(source_id='fx_daily',kind='daily'),dict(source_id='fx_hourly',kind='hourly')]
    menus={'QR33':[.001,.01,.1],'QR4':[.001,.01,.1,1.,10.]}
    manifest=dict(sources=sources,design=dict(menus=menus,horizon=6,windows=[52,260],
                                           validation_first=0,validation_last=71,evaluation_first=100,evaluation_last=171))
    plan=dict(repetitions=2,conditional_methods=list(methods),stream_tag=2)
    files,tasks={},[]
    for rep in range(2):
        for si in range(13):
            unit=f's{si:02}-r{rep:03}'
            files[f'{unit}/result.json']=dict(source_id=f's{si:02}',source_index=si,rep=rep,complete=True,records=[])
            tasks.append(dict(task=dict(source=si,rep=rep,worker='worker-forecast',output=f'/artificial/formal/units/{unit}/result.json'),elapsed_seconds=1.,exit_code=0))
            for arm in ['constant','switching']:
                for W in [52,260]:
                    for method in ['F',*methods]:
                        base=f'{unit}/{arm}/W{W}_H6_{method}'
                        evaluation=dict(n=72,mean_loss=100+si+rep+(0 if arm=='constant' else 10)+W/100,
                                        strict_breach_count=rep+1,strict_breach_rate=(rep+1)/72)
                        candidates=[]
                        for index,penalty in enumerate(menus.get(method,[])):
                            candidate=dict(penalty=penalty,status='COMPLETE',origin_count=72,mean_loss=200.)
                            files[f'{base}_validation-{index}.json']=candidate
                            candidates.append(copy.deepcopy(candidate))
                        selected=None
                        if method!='F':
                            selected=menus[method][-1] if method=='QR33' else menus[method][0]
                            files[f'{base}.selection.json']=dict(status='SELECTED',penalty=selected,mean_validation_loss=200.)
                        files[f'{base}.started.json']=dict(status='STARTED')
                        files[f'{base}.json']=dict(status='COMPLETE',reason=None,selected_penalty=selected,
                                                  evaluation=evaluation,candidates=candidates)
    return dict(manifest=manifest,plan=plan,completion=dict(ended_utc='2026-01-01T00:00:00Z',tasks=tasks),files=files)


def seal(path, data):
    formal=path/'formal';formal.mkdir(parents=True,exist_ok=True)
    for name,value in [('manifest.json',data['manifest']),('formal/plan.json',data['plan']),('formal/completion.json',data['completion'])]:
        (path/name).write_text(json.dumps(value))
    entries=[]
    with zipfile.ZipFile(formal/'units.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,value in sorted(data['files'].items()):
            raw=json.dumps(value,sort_keys=True).encode();z.writestr(name,raw)
            entries.append(dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    index=dict(files=entries,archive_sha256=hashlib.sha256((formal/'units.zip').read_bytes()).hexdigest(),loose_files_retained=True)
    (formal/'units-manifest.json').write_text(json.dumps(index))


def test_complete_zip_verifies_every_entry_and_all_52_f_cells(tmp_path):
    m=api();data=fixture(tmp_path);seal(tmp_path,data)
    report=m.audit_archive(tmp_path)
    assert report['integrity']['verified_files']==len(data['files'])
    assert report['planned']['units']==26 and report['planned']['method_receipts']==312
    assert report['planned']['candidate_receipts']==832
    assert len(report['f_cells'])==52 and all(r['status']=='COMPLETE' for r in report['f_cells'])
    first=next(r for r in report['f_cells'] if r['source_id']=='s00' and r['arm']=='constant' and r['window']==52)
    assert first['mean_loss_median']==pytest.approx(101.02)
    assert first['breach_rate_median']==pytest.approx(1.5/72)
    assert first['mean_loss_q25']==pytest.approx(100.77)
    assert not report['failures']['failed_candidates']
    assert (tmp_path/'audit/f-benchmark-cells.csv').exists()


def test_failed_qr4_candidate_is_preserved_without_failing_selected_qr4(tmp_path):
    m=api();data=fixture(tmp_path)
    base='s00-r000/constant/W52_H6_QR4'
    failed=dict(penalty=.01,status='FAILED',reason='ADMM_NONCONVERGENCE',origin_count=0,mean_loss=None)
    data['files'][base+'_validation-1.json']=failed
    data['files'][base+'.json']['candidates'][1]=copy.deepcopy(failed)
    seal(tmp_path,data);report=m.audit_archive(tmp_path)
    assert len(report['failures']['failed_candidates'])==1
    cell=next(r for r in report['conditional_cells'] if r['source_id']=='s00' and r['arm']=='constant' and r['window']==52 and r['method']=='QR4')
    assert cell['status']=='COMPLETE'


def test_qr33_validation_failure_fails_whole_cell_and_leaves_f_untouched(tmp_path):
    m=api();data=fixture(tmp_path)
    base='s00-r000/constant/W52_H6_QR33'
    failed=dict(penalty=.01,status='FAILED',reason='ADMM_NONCONVERGENCE',origin_count=0,mean_loss=None)
    data['files'][base+'_validation-1.json']=failed
    data['files'][base+'.json'].update(status='FAILED',reason='VALIDATION_INELIGIBLE',evaluation=None,selected_penalty=None)
    data['files'][base+'.json']['candidates'][1]=copy.deepcopy(failed)
    data['files'][base+'.selection.json']=dict(status='INELIGIBLE',penalty=None)
    seal(tmp_path,data);report=m.audit_archive(tmp_path)
    assert len(report['failures']['failed_candidates'])==1
    cell=next(r for r in report['conditional_cells'] if r['source_id']=='s00' and r['arm']=='constant' and r['window']==52 and r['method']=='QR33')
    assert cell['status']=='FAILED' and cell['failed_repetitions']==[0]
    assert all(r['status']=='COMPLETE' for r in report['f_cells'])


def test_missing_f_final_receipt_is_never_success_or_partial_median(tmp_path):
    m=api();data=fixture(tmp_path)
    del data['files']['s00-r001/constant/W52_H6_F.json']
    seal(tmp_path,data);report=m.audit_archive(tmp_path)
    cell=next(r for r in report['f_cells'] if r['source_id']=='s00' and r['arm']=='constant' and r['window']==52)
    assert cell['status']=='FAILED' and cell['complete_repetitions']==1
    assert cell['mean_loss_median'] is None and cell['breach_rate_median'] is None
    assert any(r['method']=='F' and r['receipt_status']=='NOT_ARCHIVED' for r in report['methods'])


def test_missing_candidate_invalidates_claimed_complete_method(tmp_path):
    m=api();data=fixture(tmp_path)
    del data['files']['s00-r000/constant/W52_H6_QR33_validation-1.json']
    seal(tmp_path,data);report=m.audit_archive(tmp_path)
    assert len(report['failures']['unarchived_candidates'])==1
    method=next(r for r in report['methods'] if r['source_id']=='s00' and r['rep']==0 and r['arm']=='constant' and r['window']==52 and r['method']=='QR33')
    assert method['audit_status']=='INVALID_RECEIPT'


def test_zip_hash_mismatch_fails_before_any_audit_output(tmp_path):
    m=api();data=fixture(tmp_path);seal(tmp_path,data)
    p=tmp_path/'formal/units-manifest.json';index=json.loads(p.read_text());index['archive_sha256']='0'*64;p.write_text(json.dumps(index))
    with pytest.raises(m.AuditError,match='ZIP_SHA256'):
        m.audit_archive(tmp_path)
    assert not (tmp_path/'audit').exists()


def test_entry_bytes_hash_mismatch_is_not_hidden_by_valid_zip_hash(tmp_path):
    m=api();data=fixture(tmp_path);seal(tmp_path,data)
    p=tmp_path/'formal/units-manifest.json';index=json.loads(p.read_text());index['files'][0]['bytes']+=1;p.write_text(json.dumps(index))
    with pytest.raises(m.AuditError,match='ENTRY'):
        m.audit_archive(tmp_path)
    assert not (tmp_path/'audit').exists()


def test_completion_inventory_cannot_duplicate_a_planned_unit(tmp_path):
    m=api();data=fixture(tmp_path)
    data['completion']['tasks'].append(copy.deepcopy(data['completion']['tasks'][0]))
    seal(tmp_path,data)
    with pytest.raises(m.AuditError,match='COMPLETION'):
        m.audit_archive(tmp_path)


def test_only_qr33_run_has_explicit_smaller_candidate_plan(tmp_path):
    m=api();data=fixture(tmp_path,methods=('QR33',));seal(tmp_path,data)
    report=m.audit_archive(tmp_path)
    assert report['planned']['method_receipts']==208
    assert report['planned']['candidate_receipts']==312
    assert len(report['conditional_cells'])==52 and len(report['f_cells'])==52


def test_exclusive_output_preserves_source_zip_and_all_input_bytes(tmp_path):
    m=api();data=fixture(tmp_path);seal(tmp_path,data)
    names=['manifest.json','formal/plan.json','formal/completion.json','formal/units.zip','formal/units-manifest.json']
    before={name:hashlib.sha256((tmp_path/name).read_bytes()).hexdigest() for name in names}
    m.audit_archive(tmp_path)
    with pytest.raises(FileExistsError):m.audit_archive(tmp_path)
    assert before=={name:hashlib.sha256((tmp_path/name).read_bytes()).hexdigest() for name in names}
