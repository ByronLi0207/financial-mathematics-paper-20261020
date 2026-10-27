"""Lossless transport parts for the saved v9 ZIP; no research computation.

Split preserves the original ZIP, index and loose files. Restore first verifies
every part and the joined digest, then creates a new target exclusively. An
existing target is only fingerprinted; matching bytes are never rewritten.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re


MAX_PART_BYTES=20*1024*1024


class ArchiveTransferError(ValueError):
    pass


def _fingerprint(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file():
        raise ArchiveTransferError('NONREGULAR_FILE:'+str(path))
    size=0;digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            size+=len(block);digest.update(block)
    return size,digest.hexdigest()


def _digest(value):
    return isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None


def _basename(value):
    return isinstance(value,str) and value not in ('','.','..') and PurePosixPath(value).name==value and '\\' not in value


def split_archive(archive_path,source_manifest_path,max_part_bytes=MAX_PART_BYTES):
    """Create units.zip.part-NNN plus archive-parts.json; overwrite nothing."""
    archive,source_manifest=Path(archive_path),Path(source_manifest_path)
    if type(max_part_bytes) is not int or not 1<=max_part_bytes<=MAX_PART_BYTES:
        raise ArchiveTransferError('PART_SIZE_OUTSIDE_20_MIB_LIMIT')
    whole_bytes,whole_sha=_fingerprint(archive)
    _,source_manifest_sha=_fingerprint(source_manifest)
    source_index=json.loads(source_manifest.read_text())
    if not _digest(source_index.get('archive_sha256')) or whole_sha!=source_index['archive_sha256']:
        raise ArchiveTransferError('SOURCE_ARCHIVE_SHA256_MISMATCH')
    if whole_bytes<=0:raise ArchiveTransferError('EMPTY_ARCHIVE')
    count=math.ceil(whole_bytes/max_part_bytes)
    paths=[archive.with_name(archive.name+f'.part-{i:03}') for i in range(count)]
    manifest_path=archive.with_name('archive-parts.json')
    for path in [manifest_path,*paths]:
        if path.exists() or path.is_symlink():raise FileExistsError(str(path))
    parts=[];joined_sha=hashlib.sha256();joined_bytes=0
    with archive.open('rb') as source:
        for path in paths:
            raw=source.read(max_part_bytes)
            if not raw:raise ArchiveTransferError('SOURCE_CHANGED_DURING_SPLIT')
            with path.open('xb') as output:output.write(raw)
            digest=hashlib.sha256(raw).hexdigest()
            actual_bytes,actual_sha=_fingerprint(path)
            if actual_bytes!=len(raw) or actual_sha!=digest:
                raise ArchiveTransferError('PART_WRITE_VERIFICATION_FAILED:'+path.name)
            parts.append(dict(path=path.name,bytes=len(raw),sha256=digest))
            joined_sha.update(raw);joined_bytes+=len(raw)
        if source.read(1):raise ArchiveTransferError('SOURCE_CHANGED_DURING_SPLIT')
    if joined_bytes!=whole_bytes or joined_sha.hexdigest()!=whole_sha:
        raise ArchiveTransferError('SOURCE_CHANGED_DURING_SPLIT')
    if _fingerprint(archive)!=(whole_bytes,whole_sha) or _fingerprint(source_manifest)[1]!=source_manifest_sha:
        raise ArchiveTransferError('SOURCE_CHANGED_DURING_SPLIT')
    manifest=dict(schema='v9-lossless-archive-parts-v1',created_utc=datetime.now(timezone.utc).isoformat(),
                  archive_name=archive.name,bytes=whole_bytes,sha256=whole_sha,max_part_bytes=max_part_bytes,
                  source_manifest=source_manifest.name,source_manifest_sha256=source_manifest_sha,
                  original_archive_retained=True,loose_files_retained=True,parts=parts)
    with manifest_path.open('x') as f:json.dump(manifest,f,indent=2,allow_nan=False);f.write('\n')
    return manifest


def _read_parts_manifest(path):
    _fingerprint(path)
    manifest=json.loads(Path(path).read_text())
    if (manifest.get('schema')!='v9-lossless-archive-parts-v1'
            or not _basename(manifest.get('archive_name'))
            or type(manifest.get('bytes')) is not int or manifest['bytes']<=0
            or not _digest(manifest.get('sha256'))):
        raise ArchiveTransferError('INVALID_WHOLE_MANIFEST')
    parts=manifest.get('parts')
    if not isinstance(parts,list) or not parts:raise ArchiveTransferError('INVALID_PART_INVENTORY')
    total=0
    for index,part in enumerate(parts):
        if (not isinstance(part,dict) or part.get('path')!=manifest['archive_name']+f'.part-{index:03}'
                or not _basename(part['path']) or type(part.get('bytes')) is not int
                or not 1<=part['bytes']<=MAX_PART_BYTES or not _digest(part.get('sha256'))):
            raise ArchiveTransferError('INVALID_PART_MANIFEST')
        total+=part['bytes']
    if total!=manifest['bytes']:raise ArchiveTransferError('WHOLE_BYTE_CENSUS_MISMATCH')
    return manifest


def restore_archive(parts_manifest_path,target_path=None):
    """Verify all input parts before exclusive creation; never replace target."""
    manifest_path=Path(parts_manifest_path);manifest=_read_parts_manifest(manifest_path)
    target=manifest_path.with_name(manifest['archive_name']) if target_path is None else Path(target_path)
    if target.exists() or target.is_symlink():
        try:size,digest=_fingerprint(target)
        except ArchiveTransferError as exc:raise ArchiveTransferError('EXISTING_TARGET_NOT_REGULAR') from exc
        if size!=manifest['bytes'] or digest!=manifest['sha256']:
            raise ArchiveTransferError('EXISTING_TARGET_BYTES_OR_SHA256_MISMATCH')
        return dict(status='EXISTING_VERIFIED',target=str(target),bytes=size,sha256=digest,overwritten=False)
    joined=hashlib.sha256();total=0
    for part in manifest['parts']:
        path=manifest_path.with_name(part['path'])
        try:size,digest=_fingerprint(path)
        except ArchiveTransferError as exc:raise ArchiveTransferError('PART_NOT_REGULAR:'+part['path']) from exc
        if size!=part['bytes'] or digest!=part['sha256']:
            raise ArchiveTransferError('PART_BYTES_OR_SHA256_MISMATCH:'+part['path'])
        with path.open('rb') as source:
            for block in iter(lambda:source.read(1024*1024),b''):
                joined.update(block);total+=len(block)
    if total!=manifest['bytes'] or joined.hexdigest()!=manifest['sha256']:
        raise ArchiveTransferError('WHOLE_REJOIN_BYTES_OR_SHA256_MISMATCH')
    # Every part and the complete joined digest have passed before any target
    # is created. Exclusive mode also rejects a concurrently created target.
    target.parent.mkdir(parents=True,exist_ok=True)
    written_sha=hashlib.sha256();written_bytes=0
    with target.open('xb') as output:
        for part in manifest['parts']:
            with manifest_path.with_name(part['path']).open('rb') as source:
                for block in iter(lambda:source.read(1024*1024),b''):
                    output.write(block);written_sha.update(block);written_bytes+=len(block)
    if written_bytes!=manifest['bytes'] or written_sha.hexdigest()!=manifest['sha256']:
        raise ArchiveTransferError('PART_CHANGED_DURING_RESTORE')
    if _fingerprint(target)!=(manifest['bytes'],manifest['sha256']):
        raise ArchiveTransferError('RESTORED_TARGET_VERIFICATION_FAILED')
    return dict(status='RESTORED',target=str(target),bytes=written_bytes,sha256=written_sha.hexdigest(),overwritten=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    split=sub.add_parser('split');split.add_argument('archive',type=Path);split.add_argument('--source-manifest',type=Path,required=True)
    restore=sub.add_parser('restore');restore.add_argument('parts_manifest',type=Path);restore.add_argument('--target',type=Path)
    args=parser.parse_args()
    result=split_archive(args.archive,args.source_manifest) if args.command=='split' else restore_archive(args.parts_manifest,args.target)
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()
