"""Deterministic packaging of terminated, audited WP3 public driver outputs.

This module imports only the standard library, never generates data or runs a
model. Inputs remain intact. An oversize/failing package is retained in the new
scratch directory; no files are deleted and no archive is split automatically.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import sys
import tarfile
import uuid
import zlib

ARCHIVE_NAME='wp3-driver-output.tar.gz'
INDEX_NAME='wp3-driver-output-members.csv'
RECEIPT_NAME='wp3-package-receipt.json'
TOP_LEVEL=('manifest.json','inventory.json','progress.jsonl','summary.csv',
    'summary.json','support.json','study-termination.json')
AUDITED_FILES=('manifest.json','inventory.json','summary.json','support.json','study-termination.json')
MAX_ARCHIVE_BYTES=24*1024*1024
CHUNK=1024*1024
FORBIDDEN_PARTS={'.scratch','.git','__pycache__','.pytest_cache','.mypy_cache','.cache'}


def no_symlinks(path):
    path=Path(path).absolute()
    if any(p.is_symlink() for p in (path,*path.parents)):
        raise ValueError('SYMLINK_REFUSED: '+str(path))


def sha_file(path):
    no_symlinks(path);digest=hashlib.sha256()
    with open(path,'rb') as stream:
        for chunk in iter(lambda:stream.read(CHUNK),b''):digest.update(chunk)
    return digest.hexdigest()


def load_json(path):
    no_symlinks(path)
    def reject(value):raise ValueError('NONFINITE_JSON: '+value)
    with open(path,encoding='utf-8') as stream:return json.load(stream,parse_constant=reject)


def safe_member(name):
    path=PurePosixPath(name)
    if (path.is_absolute() or '\\' in name or any(p in ('','..','.') for p in path.parts)
            or any(p.lower() in FORBIDDEN_PARTS for p in path.parts)
            or any('kaggle' in p.lower() or '1hournetposition' in p.lower() for p in path.parts)
            or name.endswith('.pyc')):
        raise ValueError('FORBIDDEN_MEMBER: '+name)
    if name not in TOP_LEVEL:
        if len(path.parts)<2 or path.parts[0]!='units' or path.suffix not in ('.json','.jsonl','.log'):
            raise ValueError('FORBIDDEN_MEMBER: '+name)


def collect_members(formal):
    """Return only the exact public driver payload, never package/plot extras."""
    formal=Path(formal).absolute();no_symlinks(formal)
    selected=[]
    for name in TOP_LEVEL:
        path=formal/name;no_symlinks(path)
        if not path.is_file():raise ValueError('MISSING_DRIVER_OUTPUT: '+name)
        selected.append(path)
    units=formal/'units';no_symlinks(units)
    if not units.is_dir():raise ValueError('MISSING_DRIVER_UNITS')
    for path in units.rglob('*'):
        no_symlinks(path)
        name=path.relative_to(formal).as_posix()
        if any(p.lower() in FORBIDDEN_PARTS for p in PurePosixPath(name).parts):
            raise ValueError('FORBIDDEN_MEMBER: '+name)
        if path.is_file():selected.append(path)
        elif not path.is_dir():raise ValueError('NONREGULAR_DRIVER_MEMBER: '+name)
    output=[]
    for path in sorted(selected,key=lambda p:p.relative_to(formal).as_posix()):
        name=path.relative_to(formal).as_posix();safe_member(name)
        output.append(dict(path=name,size=path.stat().st_size,sha256=sha_file(path)))
    if len({r['path'] for r in output})!=len(output):raise ValueError('DUPLICATE_SOURCE_MEMBER')
    return output


def create_archive(formal,members,target):
    formal=Path(formal);target=Path(target);no_symlinks(target)
    with target.open('xb') as raw:
        # Blank filename suppresses the original-path header; zero mtime is fixed.
        with gzip.GzipFile(filename='',mode='wb',compresslevel=9,fileobj=raw,mtime=0) as zipped:
            with tarfile.open(fileobj=zipped,mode='w',format=tarfile.PAX_FORMAT) as archive:
                for row in members:
                    name=row['path'];safe_member(name);source=formal/name;no_symlinks(source)
                    info=tarfile.TarInfo(name)
                    info.type=tarfile.REGTYPE;info.size=row['size'];info.mtime=0
                    info.uid=info.gid=0;info.uname=info.gname='';info.mode=0o644
                    info.pax_headers={}
                    with source.open('rb') as stream:archive.addfile(info,stream)
        raw.flush();os.fsync(raw.fileno())


def verify_archive(archive_path,members):
    """Re-open compressed bytes, stream every member and validate the gzip CRC."""
    expected={r['path']:r for r in members};seen=set();total=0
    if len(expected)!=len(members):raise ValueError('DUPLICATE_EXPECTED_MEMBER')
    with gzip.open(archive_path,'rb') as zipped:
        with tarfile.open(fileobj=zipped,mode='r|') as archive:
            for info in archive:
                name=info.name
                if name in seen:raise ValueError('DUPLICATE_ARCHIVE_MEMBER: '+name)
                seen.add(name);safe_member(name)
                if name not in expected:raise ValueError('UNLISTED_ARCHIVE_MEMBER: '+name)
                if not info.isfile():raise ValueError('NONREGULAR_ARCHIVE_MEMBER: '+name)
                if (info.uid!=0 or info.gid!=0 or info.uname!='' or info.gname!=''
                        or info.mtime!=0 or info.mode!=0o644):
                    raise ValueError('NONNORMALIZED_ARCHIVE_METADATA: '+name)
                row=expected[name]
                if info.size!=row['size']:raise ValueError('ARCHIVE_MEMBER_SIZE_MISMATCH: '+name)
                stream=archive.extractfile(info)
                if stream is None:raise ValueError('ARCHIVE_MEMBER_UNREADABLE: '+name)
                digest=hashlib.sha256();size=0
                for chunk in iter(lambda:stream.read(CHUNK),b''):
                    digest.update(chunk);size+=len(chunk)
                if size!=row['size'] or digest.hexdigest()!=row['sha256']:
                    raise ValueError('ARCHIVE_MEMBER_HASH_MISMATCH: '+name)
                total+=size
        # Force the gzip trailer/CRC check beyond the tar end-of-archive marker.
        while zipped.read(CHUNK):pass
    if seen!=set(expected):raise ValueError('MISSING_ARCHIVE_MEMBERS')
    return dict(member_count=len(seen),uncompressed_source_bytes=total,status='PASS')


def assert_sources_unchanged(formal,before):
    after=collect_members(formal)
    if after!=before:raise ValueError('SOURCE_CHANGED_DURING_PACKAGING')
    return after


def preconditions(formal,audit_path):
    termination=load_json(Path(formal)/'study-termination.json')
    if termination.get('all_workers_terminated') is not True:
        raise ValueError('STUDY_NOT_TERMINATED')
    # Summary must exist before any scratch output is created.
    load_json(Path(formal)/'summary.json')
    audit=load_json(audit_path)
    if (audit.get('schema')!='independent-wp3-audit-1' or audit.get('status')!='PASS'
            or type(audit.get('difference_count')) is not int or audit['difference_count']!=0
            or audit.get('resources',{}).get('status')!='PASS'):
        raise ValueError('AUDIT_NOT_PASS')
    bindings=audit.get('input_hashes',{})
    for name in AUDITED_FILES:
        if name not in bindings or sha_file(Path(formal)/name)!=bindings[name]:
            raise ValueError('AUDIT_INPUT_HASH_MISMATCH: '+name)
    return dict(audit_sha256=sha_file(audit_path),audited_input_hashes={n:bindings[n] for n in AUDITED_FILES})


def copy_exclusive(source,target):
    no_symlinks(source);no_symlinks(target)
    with open(source,'rb') as inp,open(target,'xb') as out:
        shutil.copyfileobj(inp,out,length=CHUNK)
        out.flush();os.fsync(out.fileno())
    if sha_file(source)!=sha_file(target):raise ValueError('PUBLIC_COPY_HASH_MISMATCH: '+target.name)


def package_bundle(root,formal,audit_path,*,maximum_bytes=MAX_ARCHIVE_BYTES):
    if type(maximum_bytes) is not int or not 0<maximum_bytes<=MAX_ARCHIVE_BYTES:
        raise ValueError('INVALID_ARCHIVE_LIMIT')
    root,formal,audit_path=map(lambda p:Path(p).absolute(),(root,formal,audit_path))
    for path in (root,formal,audit_path):no_symlinks(path)
    formal.relative_to(root);audit_path.relative_to(root)
    bindings=preconditions(formal,audit_path)
    names=(ARCHIVE_NAME,INDEX_NAME,RECEIPT_NAME)
    for name in names:
        no_symlinks(formal/name)
        if (formal/name).exists():raise FileExistsError('PUBLIC_PACKAGE_ALREADY_EXISTS: '+name)
    members=collect_members(formal)
    scratch=root/'.scratch/revision-v8/wp3-package'/uuid.uuid4().hex
    no_symlinks(scratch);scratch.mkdir(parents=True,exist_ok=False)
    archive=scratch/ARCHIVE_NAME;index=scratch/INDEX_NAME;receipt_path=scratch/RECEIPT_NAME
    create_archive(formal,members,archive)
    with index.open('x',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=('path','size','sha256'),lineterminator='\n')
        writer.writeheader();writer.writerows(members)
        out.flush();os.fsync(out.fileno())
    compressed_size=archive.stat().st_size
    if compressed_size>maximum_bytes:
        raise ValueError(f'ARCHIVE_EXCEEDS_LIMIT: {compressed_size}>{maximum_bytes}; scratch retained at {scratch}')
    verified=verify_archive(archive,members)
    assert_sources_unchanged(formal,members)
    if sha_file(audit_path)!=bindings['audit_sha256']:raise ValueError('AUDIT_CHANGED_DURING_PACKAGING')
    # Revalidate all audit bindings after streaming, before public delivery.
    if preconditions(formal,audit_path)!=bindings:raise ValueError('AUDIT_BINDINGS_CHANGED')
    receipt=dict(schema='v8-wp3-deterministic-package-1',status='PASS',
        packaged_utc=datetime.now(timezone.utc).isoformat(),
        scope='All original public WP3 driver payload files; no plots, package extras, caches or private traces.',
        archive_name=ARCHIVE_NAME,member_index_name=INDEX_NAME,
        archive_sha256=sha_file(archive),index_sha256=sha_file(index),
        member_count=verified['member_count'],uncompressed_source_bytes=verified['uncompressed_source_bytes'],
        archive_bytes=compressed_size,maximum_archive_bytes=MAX_ARCHIVE_BYTES,
        effective_test_or_production_cap_bytes=maximum_bytes,
        archive_member_verification='PASS',source_hashes_unchanged='PASS',
        metadata=dict(gzip_mtime=0,gzip_filename='',compression_level=9,tar_mtime=0,
            uid=0,gid=0,uname='',gname='',mode='0644',format='PAX',path_order='lexicographic'),
        audit_binding=bindings,tool_sha256=sha_file(Path(__file__)),
        runtime=dict(python=platform.python_version(),zlib_compile=zlib.ZLIB_VERSION,zlib_runtime=zlib.ZLIB_RUNTIME_VERSION),
        originals_retained=True,files_deleted=0,automatic_splitting=False)
    with receipt_path.open('x',encoding='utf-8') as out:
        json.dump(receipt,out,indent=2,allow_nan=False);out.write('\n');out.flush();os.fsync(out.fileno())
    # Originals and scratch artifacts survive any copy failure. No retries or cleanup.
    for name in names[:2]:copy_exclusive(scratch/name,formal/name)
    # Verify the delivered compressed bytes and index again, without extraction.
    verify_archive(formal/ARCHIVE_NAME,members)
    if sha_file(formal/INDEX_NAME)!=receipt['index_sha256']:raise ValueError('DELIVERED_INDEX_HASH_MISMATCH')
    assert_sources_unchanged(formal,members)
    # Publish the PASS receipt last, after the delivered archive/index pass too.
    copy_exclusive(receipt_path,formal/RECEIPT_NAME)
    return receipt


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--formal',type=Path)
    parser.add_argument('--audit',type=Path,required=True)
    args=parser.parse_args(argv)
    formal=args.formal or args.root/'results/revision-v8/wp3'
    result=package_bundle(args.root,formal,args.audit)
    print(json.dumps({k:result[k] for k in ('status','archive_name','member_count','archive_bytes','archive_sha256','source_hashes_unchanged')}))
    return 0


if __name__=='__main__':raise SystemExit(main())
