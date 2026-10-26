"""Byte-only admission and isolated preparation for the frozen v6 replay.

This stdlib tool never fits models, decodes source values/NPZ arrays, fetches,
installs, deletes, or overwrites. Check mode is read-only. Preparation requires a
new target with an existing parent and leaves every canonical v6 output absent.

The original workers still require their pinned numerical runtime and exact
archived input bytes, including whole NPZ containers. A semantically equivalent
new NPZ is not admitted. This helper does not recreate unavailable private data,
guarantee an unconditional fresh-clone run, or establish independent validation.
Use the documented frozen runtime separately; this tool does not install it.
An I/O failure may leave a partial new target, which is never deleted or reused.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parent
PROTOCOL='protocol/revision-v6/'
ARCHIVE=PROTOCOL+'replay-metadata.zip'
MANIFEST=PROTOCOL+'replay-metadata-manifest.json'
INVENTORY='.scratch/revision-v6/input-inventory.json'
OUTPUT='results/revision-20261023/v6'
CHUNK=1024*1024
MAX_METADATA_BYTES=64*1024*1024


class ReplaySetupError(ValueError):
    """Admission failure; messages contain relative labels, never source values."""


def _fail(code,label=''):
    raise ReplaySetupError(code+(': '+label if label else ''))


def _relative(value):
    if (not isinstance(value,str) or not value or '\\' in value or ':' in value
            or any(ord(c)<32 for c in value) or value.startswith('/')
            or any(p in ('','.', '..') for p in value.split('/'))):
        _fail('UNSAFE_PATH')
    return PurePosixPath(value).as_posix()


def _sha(value):
    if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{64}',value):
        _fail('INVALID_SHA256')
    return value


def _count(value):
    if type(value) is not int or value<0:_fail('INVALID_BYTE_COUNT')
    return value


def _file(root,relative):
    relative=_relative(relative);p=root
    for part in relative.split('/'):
        p=p/part
        if p.is_symlink():_fail('SYMLINK_INPUT',relative)
    if not p.is_file():_fail('MISSING_INPUT',relative)
    return p


def _fingerprint(path):
    h=hashlib.sha256();n=0
    with path.open('rb') as f:
        for data in iter(lambda:f.read(CHUNK),b''):
            n+=len(data);h.update(data)
    return n,h.hexdigest()


def _json_file(root,relative,*,pins=None):
    p=_file(root,relative)
    if p.stat().st_size>MAX_METADATA_BYTES:_fail('METADATA_TOO_LARGE',relative)
    data=p.read_bytes()
    if pins is not None:pins[relative]=dict(source=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    try:return json.loads(data)
    except (ValueError,UnicodeError):_fail('INVALID_JSON',relative)


def _metadata(root):
    protected={}
    manifest=_json_file(root,MANIFEST,pins=protected)
    if manifest.get('version')!=1 or manifest.get('inventory_member')!=INVENTORY:
        _fail('METADATA_SCHEMA')
    archive=_file(root,ARCHIVE)
    archive_bytes,archive_hash=_fingerprint(archive)
    if archive_hash!=_sha(manifest['zip_sha256']):_fail('ZIP_HASH_MISMATCH')
    protected[ARCHIVE]=dict(source=archive,bytes=archive_bytes,sha256=archive_hash)
    specs={}
    for row in manifest['members']:
        path=_relative(row['path'])
        if path in specs:_fail('DUPLICATE_MEMBER',path)
        specs[path]=(_count(row['bytes']),_sha(row['sha256']))
    if sum(n for n,h in specs.values())>MAX_METADATA_BYTES:_fail('METADATA_TOO_LARGE')
    blobs={}
    try:
        with zipfile.ZipFile(archive) as z:
            infos=z.infolist();names=[_relative(i.filename) for i in infos]
            if len(names)!=len(set(names)):_fail('DUPLICATE_MEMBER')
            if set(names)!=set(specs):_fail('ZIP_MEMBER_INVENTORY')
            for info in infos:
                mode=info.external_attr>>16
                if info.is_dir() or stat.S_ISLNK(mode):_fail('UNSAFE_ZIP_MEMBER',info.filename)
                size,pin=specs[info.filename]
                if info.file_size!=size:_fail('MEMBER_BYTE_MISMATCH',info.filename)
                with z.open(info) as source:
                    data=source.read(size+1)
                if len(data)!=size:_fail('MEMBER_BYTE_MISMATCH',info.filename)
                if hashlib.sha256(data).hexdigest()!=pin:_fail('MEMBER_HASH_MISMATCH',info.filename)
                blobs[info.filename]=data
    except (zipfile.BadZipFile,RuntimeError,NotImplementedError):_fail('INVALID_ZIP')
    if INVENTORY not in blobs:_fail('MISSING_INVENTORY_MEMBER')
    frozen=_json_file(root,PROTOCOL+'design-freeze.json',pins=protected)['private_input_inventory_sha256']
    actual=hashlib.sha256(blobs[INVENTORY]).hexdigest()
    if actual!=_sha(frozen):_fail('FROZEN_INVENTORY_MISMATCH')
    for p in (root/PROTOCOL).glob('*freeze*.json'):
        document=_json_file(root,p.relative_to(root).as_posix(),pins=protected)
        for key in ('private_inventory_sha256','private_input_inventory_sha256'):
            if key in document and document[key]!=actual:_fail('FROZEN_INVENTORY_MISMATCH',p.name)
    try:inventory=json.loads(blobs[INVENTORY])
    except (ValueError,UnicodeError):_fail('INVALID_INVENTORY_JSON')
    expected={INVENTORY:actual}
    for cell in inventory['original_cells']:
        for trace in cell['traces']:
            path=_relative(trace['manifest_path']);pin=_sha(trace['manifest_sha256'])
            if path in expected and expected[path]!=pin:_fail('MANIFEST_PIN_CONFLICT',path)
            expected[path]=pin
    if set(expected)!=set(blobs):_fail('FROZEN_MANIFEST_INVENTORY')
    for path,pin in expected.items():
        if hashlib.sha256(blobs[path]).hexdigest()!=pin:_fail('FROZEN_MANIFEST_MISMATCH',path)
    # A file cannot also be another member's parent directory.
    _no_parent_conflicts(blobs)
    return inventory,blobs,manifest['zip_sha256'],protected


def _tracked_paths(root):
    try:
        result=subprocess.run(['git','-C',str(root),'ls-files','-z'],check=True,capture_output=True)
    except (OSError,subprocess.CalledProcessError):_fail('GIT_TRACKED_INVENTORY_UNAVAILABLE')
    return [os.fsdecode(p) for p in result.stdout.split(b'\0') if p]


def _excluded(path):
    parts=PurePosixPath(path).parts
    return (any(p in ('.git','.scratch','.bak') or p.endswith('.bak') for p in parts)
            or path==OUTPUT or path.startswith(OUTPUT+'/'))


def _no_parent_conflicts(paths):
    names=set(paths)
    for path in names:
        if path==OUTPUT or path.startswith(OUTPUT+'/') or '.git' in PurePosixPath(path).parts:
            _fail('RESERVED_DESTINATION',path)
        if any(p.as_posix() in names for p in PurePosixPath(path).parents if p.as_posix()!='.'):
            _fail('CONFLICTING_DESTINATION',path)


def _pin(entry):
    pins=[entry[k] for k in ('expected_sha256','sha256') if k in entry]
    if not pins or len(set(pins))!=1:_fail('METADATA_PIN_CONFLICT')
    sizes=[entry[k] for k in ('expected_bytes','bytes') if k in entry]
    if len(set(sizes))>1:_fail('METADATA_BYTE_CONFLICT')
    return _sha(pins[0]),_count(sizes[0]) if sizes else None


def _admit(root,private):
    inventory,blobs,zip_sha,protected=_metadata(root)
    tracked={_relative(p) for p in _tracked_paths(root)}
    plan={};private_paths=set()
    def add(path,pin,size=None,*,public=False):
        path=_relative(path);pin=_sha(pin)
        if path in blobs:_fail('CONFLICTING_DESTINATION',path)
        if public and path not in tracked:_fail('PUBLIC_INPUT_NOT_TRACKED',path)
        is_private=not(public or path in tracked and not _excluded(path))
        base=private if is_private else root
        p=_file(base,path);n,h=_fingerprint(p)
        if h!=pin:_fail('HASH_MISMATCH',path)
        if size is not None and n!=size:_fail('BYTE_MISMATCH',path)
        if path in plan and plan[path]['sha256']!=h:_fail('CONFLICTING_DESTINATION',path)
        plan[path]=dict(source=p,bytes=n,sha256=h)
        if is_private:private_paths.add(path)
    for entry in inventory['source_inputs'].values():
        pin,size=_pin(entry);add(entry['path'],pin,size)
    for cell in inventory['original_cells']:
        for entry in cell['traces']:
            pin,size=_pin(entry);add(entry['path'],pin,size)
    for entry in inventory['panel_source_inputs']:
        pin,size=_pin(entry);add(entry['path'],pin,size)
        if 'provenance_path' in entry:add(entry['provenance_path'],entry['provenance_sha256'],public=True)
    for entry in inventory['panel_cells']:
        pin,size=_pin(entry);add(entry['path'],pin,size)
        if 'public_cell_path' in entry:add(entry['public_cell_path'],entry['public_cell_sha256'],public=True)
    if inventory.get('panel_selection'):
        entry=inventory['panel_selection'];add(entry['path'],entry['sha256'],public=True)
    checks=inventory['six_csv_checks']
    if len(checks)!=6 or len({e['reproduced_path'] for e in checks})!=6:_fail('SIX_CSV_INVENTORY')
    for entry in checks:
        add(entry['reproduced_path'],entry['expected_sha256'])
        add(entry['archived_path'],entry['expected_sha256'],public=True)
    for path,entry in protected.items():
        if _fingerprint(_file(root,path))!=(entry['bytes'],entry['sha256']):
            _fail('METADATA_CHANGED',path)
    _no_parent_conflicts([*plan,*blobs])
    report=dict(status='ADMITTED',metadata_member_count=len(blobs),six_csv_count=len(checks),
        required_file_count=len(plan),private_file_count=len(private_paths),
        required_bytes=sum(e['bytes'] for e in plan.values()),metadata_zip_sha256=zip_sha,
        admission='exact whole-file SHA-256; no model or array-value inspection',
        limitation='Pinned numerical runtime and byte-identical private archives are still required; this is not independent validation.')
    return report,plan,blobs,tracked,protected


def _roots(root,private_input_root):
    root=Path(ROOT if root is None else root).resolve(strict=True)
    private=Path(root if private_input_root is None else private_input_root).resolve(strict=True)
    if not root.is_dir() or not private.is_dir():_fail('INPUT_ROOT_NOT_DIRECTORY')
    return root,private


def check_inputs(private_input_root=None,*,root=None):
    """Read-only byte admission; no directories, reports or target are written."""
    root,private=_roots(root,private_input_root)
    return _admit(root,private)[0]


def prepare_replay(target,private_input_root=None,*,root=None):
    """Prepare a fresh isolated tree, after all metadata and inputs are admitted."""
    target=Path(target).absolute()
    if target.exists() or target.is_symlink():_fail('TARGET_EXISTS')
    if not target.parent.is_dir():_fail('TARGET_PARENT_MISSING')
    if any(p.is_symlink() for p in target.parents):_fail('SYMLINK_TARGET_PARENT')
    root,private=_roots(root,private_input_root)
    report,plan,blobs,tracked,protected=_admit(root,private)
    for path,entry in protected.items():
        if path in tracked or path in (ARCHIVE,MANIFEST):plan[path]=entry
    # Metadata and this helper can be copied while newly added and not yet in Git.
    for relative in sorted(tracked|{ARCHIVE,MANIFEST,'v6_replay_setup.py'}):
        if relative in blobs or relative in plan or _excluded(relative):continue
        if relative=='v6_replay_setup.py' and not (root/relative).exists():continue
        p=_file(root,relative);n,h=_fingerprint(p)
        plan[relative]=dict(source=p,bytes=n,sha256=h)
    _no_parent_conflicts([*plan,*blobs])
    target.mkdir(exist_ok=False)
    for relative,entry in sorted(plan.items()):
        destination=target/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        h=hashlib.sha256();n=0
        with entry['source'].open('rb') as source,destination.open('xb') as output:
            for data in iter(lambda:source.read(CHUNK),b''):
                output.write(data);h.update(data);n+=len(data)
        if (n,h.hexdigest())!=(entry['bytes'],entry['sha256']):_fail('INPUT_CHANGED_DURING_COPY',relative)
    for relative,data in sorted(blobs.items()):
        destination=target/relative;destination.parent.mkdir(parents=True,exist_ok=True)
        with destination.open('xb') as output:output.write(data)
    return dict(report,status='PREPARED',copied_file_count=len(plan)+len(blobs),
                canonical_v6_output_slots='EMPTY',target=str(target))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--check',action='store_true',help='Read-only exact-byte admission.')
    action.add_argument('--prepare',action='store_true',help='Prepare only a new isolated target; never run analysis.')
    parser.add_argument('--target',type=Path)
    parser.add_argument('--private-input-root',type=Path,default=ROOT)
    args=parser.parse_args(argv)
    if args.prepare and args.target is None:parser.error('--prepare requires --target')
    if args.check and args.target is not None:parser.error('--check does not accept --target')
    try:
        report=prepare_replay(args.target,args.private_input_root) if args.prepare else check_inputs(args.private_input_root)
    except (ReplaySetupError,OSError,KeyError,TypeError) as error:
        print(json.dumps(dict(status='REFUSED',reason=str(error))));return 2
    print(json.dumps(report,sort_keys=True));return 0


if __name__=='__main__':raise SystemExit(main())
