"""Tiny artificial byte fixtures only; never touches the actual study ZIP."""
import hashlib
import importlib
import json
from pathlib import Path

import pytest


def api():
    assert Path(__file__).with_name('restore_v9_archive.py').exists(), 'lossless archive helper is absent'
    return importlib.import_module('restore_v9_archive')


def artificial(tmp_path):
    raw=bytes(range(256))*5+b'formal-artificial-zip-bytes'
    source=tmp_path/'units.zip';source.write_bytes(raw)
    index=tmp_path/'units-manifest.json'
    index.write_text(json.dumps(dict(archive_sha256=hashlib.sha256(raw).hexdigest())))
    return source,index,raw


def test_lossless_parts_roundtrip_bytes_sha_and_source_preservation(tmp_path):
    m=api();source,index,raw=artificial(tmp_path)
    before_index=index.read_bytes()
    manifest=m.split_archive(source,index,max_part_bytes=257)
    assert manifest['bytes']==len(raw)
    assert manifest['sha256']==hashlib.sha256(raw).hexdigest()
    assert all(part['bytes']<=257 for part in manifest['parts'])
    target=tmp_path/'independent'/'restored.zip';target.parent.mkdir()
    receipt=m.restore_archive(tmp_path/'archive-parts.json',target)
    assert receipt['status']=='RESTORED'
    assert target.read_bytes()==raw
    assert receipt['bytes']==len(raw) and receipt['sha256']==hashlib.sha256(raw).hexdigest()
    assert source.read_bytes()==raw and index.read_bytes()==before_index
    with pytest.raises(FileExistsError):m.split_archive(source,index,max_part_bytes=257)


def test_polluted_part_or_whole_digest_is_rejected_before_target_creation(tmp_path):
    m=api();source,index,raw=artificial(tmp_path)
    manifest=m.split_archive(source,index,max_part_bytes=300)
    first=tmp_path/manifest['parts'][0]['path'];original=first.read_bytes()
    first.write_bytes(bytes([original[0]^1])+original[1:])
    target=tmp_path/'bad-restoration.zip'
    with pytest.raises(m.ArchiveTransferError,match='PART_'):
        m.restore_archive(tmp_path/'archive-parts.json',target)
    assert not target.exists()
    first.write_bytes(original)
    manifest['sha256']='0'*64
    (tmp_path/'archive-parts.json').write_text(json.dumps(manifest))
    with pytest.raises(m.ArchiveTransferError,match='WHOLE_'):
        m.restore_archive(tmp_path/'archive-parts.json',target)
    assert not target.exists()


def test_existing_target_is_verified_without_overwrite_and_pollution_refused(tmp_path):
    m=api();source,index,raw=artificial(tmp_path)
    manifest=m.split_archive(source,index,max_part_bytes=300)
    target=tmp_path/'existing.zip';target.write_bytes(b'polluted existing target')
    before=target.read_bytes()
    with pytest.raises(m.ArchiveTransferError,match='EXISTING_TARGET_'):
        m.restore_archive(tmp_path/'archive-parts.json',target)
    assert target.read_bytes()==before
    target.write_bytes(raw);mtime=target.stat().st_mtime_ns
    # A matching existing target is checked directly; missing parts do not
    # trigger any attempted reconstruction or overwrite of the valid target.
    (tmp_path/manifest['parts'][0]['path']).unlink()
    receipt=m.restore_archive(tmp_path/'archive-parts.json',target)
    assert receipt['status']=='EXISTING_VERIFIED'
    assert target.read_bytes()==raw and target.stat().st_mtime_ns==mtime
