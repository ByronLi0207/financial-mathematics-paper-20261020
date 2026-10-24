"""Small constructed packaging fixtures; no financial study data or models."""
import csv
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

import pytest

SPEC=importlib.util.spec_from_file_location('wp3_package',Path(__file__).parent/'notes/revision-v8/package_wp3.py')
pack=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(pack)


def fixture_source(tmp_path,*,terminated=True,audit_status='PASS'):
    root=tmp_path/'repo';root.mkdir()
    formal=root/'results/revision-v8/wp3';formal.mkdir(parents=True)
    payloads={
        'manifest.json':{'schema':'fixture'},
        'inventory.json':[{'status':'FAILED'}],
        'progress.jsonl':None,
        'summary.csv':None,
        'summary.json':{'cells':[{'status':'NA'}]},
        'support.json':{'procedures':{'QR33':{'status':'INCONCLUSIVE'}}},
        'study-termination.json':{'all_workers_terminated':terminated,'status':'BUDGET_STOP'},
    }
    for name,value in payloads.items():
        (formal/name).write_text(json.dumps(value) if value is not None else 'fixture\n')
    unit=formal/'units'/'rep-000_phi-0_p-0';unit.mkdir(parents=True)
    (unit/'process.log').write_bytes(b'')
    (unit/'worker-receipt.json').write_text('{"status":"FAILED"}\n')
    (unit/'progress.jsonl').write_text('{"event":"method_end"}\n')
    audit=root/'audit.json'
    audit.write_text(json.dumps(dict(schema='independent-wp3-audit-1',status=audit_status,
        difference_count=0,resources={'status':'PASS'},
        input_hashes={name:hashlib.sha256((formal/name).read_bytes()).hexdigest()
            for name in ('manifest.json','inventory.json','summary.json','support.json','study-termination.json')})))
    return root,formal,audit


def test_unterminated_study_is_rejected_without_creating_scratch(tmp_path):
    root,formal,audit=fixture_source(tmp_path,terminated=False)
    with pytest.raises(ValueError,match='STUDY_NOT_TERMINATED'):pack.package_bundle(root,formal,audit)
    assert not (root/'.scratch').exists()


def test_nonpass_or_stale_audit_is_rejected(tmp_path):
    root,formal,audit=fixture_source(tmp_path,audit_status='FAIL')
    with pytest.raises(ValueError,match='AUDIT_NOT_PASS'):pack.package_bundle(root,formal,audit)
    value=json.loads(audit.read_text());value['status']='PASS';audit.write_text(json.dumps(value))
    (formal/'inventory.json').write_text('[]')
    with pytest.raises(ValueError,match='AUDIT_INPUT_HASH_MISMATCH'):pack.package_bundle(root,formal,audit)


def test_collects_exact_driver_outputs_empty_logs_and_no_figures(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    (formal/'heatmap.png').write_bytes(b'excluded figure')
    rows=pack.collect_members(formal)
    names=[r['path'] for r in rows]
    assert len(names)==10 and names==sorted(names)
    assert 'units/rep-000_phi-0_p-0/process.log' in names
    assert next(r for r in rows if r['path'].endswith('process.log'))['size']==0
    assert 'heatmap.png' not in names


def test_symlink_to_external_file_is_refused(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    outside=tmp_path/'unrelated';outside.write_bytes(b'do not include')
    (formal/'units'/'link.json').symlink_to(outside)
    with pytest.raises(ValueError,match='SYMLINK'):pack.collect_members(formal)


def test_private_cache_and_raw_source_paths_are_refused(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    private=formal/'units'/'.scratch';private.mkdir();(private/'private.json').write_text('{}')
    with pytest.raises(ValueError,match='FORBIDDEN_MEMBER'):pack.collect_members(formal)


def test_archive_is_deterministic_despite_source_times_and_permissions(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    members=pack.collect_members(formal)
    a=tmp_path/'a.tar.gz';b=tmp_path/'b.tar.gz'
    pack.create_archive(formal,members,a)
    for row in members:
        source=formal/row['path'];os.utime(source,(123456,123456));os.chmod(source,0o600)
    pack.create_archive(formal,members,b)
    assert a.read_bytes()==b.read_bytes()
    data=a.read_bytes()
    assert data[3]==0 and data[4:8]==b'\0\0\0\0'
    with tarfile.open(a,'r:gz') as archive:
        for member in archive:
            assert member.isfile() and member.mtime==0 and member.mode==0o644
            assert member.uid==member.gid==0 and member.uname==member.gname==''


def test_complete_fixture_packaging_preserves_sources_and_verifies_every_member(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    before=pack.collect_members(formal)
    receipt=pack.package_bundle(root,formal,audit)
    assert receipt['status']=='PASS' and receipt['member_count']==10
    assert receipt['archive_member_verification']=='PASS'
    assert receipt['source_hashes_unchanged']=='PASS'
    archive=formal/pack.ARCHIVE_NAME;index=formal/pack.INDEX_NAME
    assert archive.exists() and index.exists() and (formal/pack.RECEIPT_NAME).exists()
    assert pack.collect_members(formal)==before
    assert len(list(csv.DictReader(index.open())))==10
    assert pack.verify_archive(archive,before)['member_count']==10


def test_archive_cap_failure_leaves_scratch_and_never_publishes_partial_package(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    with pytest.raises(ValueError,match='ARCHIVE_EXCEEDS_LIMIT'):pack.package_bundle(root,formal,audit,maximum_bytes=32)
    assert not any((formal/n).exists() for n in (pack.ARCHIVE_NAME,pack.INDEX_NAME,pack.RECEIPT_NAME))
    assert list((root/'.scratch').rglob('*.tar.gz'))


def test_public_limit_cannot_be_raised(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    with pytest.raises(ValueError,match='INVALID_ARCHIVE_LIMIT'):pack.package_bundle(root,formal,audit,maximum_bytes=25*1024*1024)
    assert not (root/'.scratch').exists()


def test_member_readback_rejects_wrong_hash_and_unlisted_duplicate(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    rows=pack.collect_members(formal);target=tmp_path/'archive.tar.gz'
    pack.create_archive(formal,rows,target)
    bad=[dict(r) for r in rows];bad[0]['sha256']='0'*64
    with pytest.raises(ValueError,match='ARCHIVE_MEMBER_HASH_MISMATCH'):pack.verify_archive(target,bad)
    duplicate=tmp_path/'duplicate.tar.gz'
    with tarfile.open(duplicate,'w:gz') as stream:
        for _ in range(2):
            info=tarfile.TarInfo(rows[0]['path']);data=(formal/rows[0]['path']).read_bytes();info.size=len(data)
            stream.addfile(info,io.BytesIO(data))
    with pytest.raises(ValueError,match='DUPLICATE_ARCHIVE_MEMBER'):pack.verify_archive(duplicate,rows)


def test_source_change_is_detected_without_altering_it(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    rows=pack.collect_members(formal)
    (formal/'units/rep-000_phi-0_p-0/process.log').write_text('changed')
    with pytest.raises(ValueError,match='SOURCE_CHANGED'):pack.assert_sources_unchanged(formal,rows)
    assert (formal/'units/rep-000_phi-0_p-0/process.log').read_text()=='changed'


def test_existing_public_package_is_preserved_and_no_scratch_created(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    (formal/pack.ARCHIVE_NAME).write_bytes(b'existing')
    with pytest.raises(FileExistsError):pack.package_bundle(root,formal,audit)
    assert (formal/pack.ARCHIVE_NAME).read_bytes()==b'existing'
    assert not (root/'.scratch').exists()


def test_import_and_help_do_not_load_numeric_or_study_modules():
    location=Path(__file__).parent/'notes/revision-v8/package_wp3.py'
    code="import importlib.util,sys;s=importlib.util.spec_from_file_location('p',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);assert not any(n in sys.modules for n in ('numpy','scipy','v8_mechanism_mc','run_v8_wp3'))"
    r=subprocess.run([sys.executable,'-B','-c',code,str(location)],capture_output=True,text=True)
    assert r.returncode==0,r.stderr


def test_source_mutation_during_build_blocks_public_delivery_and_is_preserved(tmp_path,monkeypatch):
    root,formal,audit=fixture_source(tmp_path)
    original=pack.create_archive
    def mutate_after_build(formal,members,target):
        original(formal,members,target)
        (formal/'units/rep-000_phi-0_p-0/process.log').write_text('fixture mutation')
    monkeypatch.setattr(pack,'create_archive',mutate_after_build)
    with pytest.raises(ValueError,match='SOURCE_CHANGED'):pack.package_bundle(root,formal,audit)
    assert (formal/'units/rep-000_phi-0_p-0/process.log').read_text()=='fixture mutation'
    assert not any((formal/name).exists() for name in (pack.ARCHIVE_NAME,pack.INDEX_NAME,pack.RECEIPT_NAME))
    assert list((root/'.scratch').rglob('*.tar.gz'))


def test_raw_fx_member_is_refused_before_archive_creation(tmp_path):
    root,formal,audit=fixture_source(tmp_path)
    (formal/'units/1hourNetPositionsKaggle.csv').write_bytes(b'private fixture')
    with pytest.raises(ValueError,match='FORBIDDEN_MEMBER'):pack.package_bundle(root,formal,audit)
    assert not (root/'.scratch').exists()
