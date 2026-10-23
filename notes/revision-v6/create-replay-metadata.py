"""Copy exact historical metadata only; never include raw files or NPZ arrays."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,datetime
ROOT=Path(__file__).resolve().parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inventory=ROOT/'.scratch/revision-v6/input-inventory.json';data=json.loads(inventory.read_text())
files={'.scratch/revision-v6/input-inventory.json':inventory}
for cell in data['original_cells']:
    for trace in cell['traces']:
        key=trace['manifest_path'];p=ROOT/key
        assert p.is_file() and sha(p)==trace['manifest_sha256']
        assert not PurePosixPath(key).is_absolute() and '..' not in PurePosixPath(key).parts
        assert key.startswith('.scratch/') and key.endswith('/public/manifest.json')
        files[key]=p
assert len(files)==41
for key,p in files.items():
    assert p.suffix=='.json' and not p.is_symlink()
    text=p.read_text();json.loads(text)
    assert '/Users/' not in text and '/home/' not in text
    assert not any(secret in text.lower() for secret in ['access_token','refresh_token','api_key','password','cookie','bearer '])
archive=ROOT/'protocol/revision-v6/replay-metadata.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for key,p in sorted(files.items()):
        info=zipfile.ZipInfo(key,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
members=[dict(path=key,bytes=p.stat().st_size,sha256=sha(p)) for key,p in sorted(files.items())]
manifest=dict(version=1,zip_sha256=sha(archive),inventory_member='.scratch/revision-v6/input-inventory.json',members=members,
 scope='Exact dated source/trace fingerprints, NPY header/index metadata and historical scalar/refit diagnostics only. No raw source, private forecast arrays, coefficients, credentials or UI context. Replaying frozen gates requires regenerated private NPZ whole-file hashes and all six CSV hashes to match; restored historical metadata does not make a changed artifact match.',
 created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),uncompressed_bytes=sum(x['bytes'] for x in members),compressed_bytes=archive.stat().st_size)
with (ROOT/'protocol/revision-v6/replay-metadata-manifest.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
print(json.dumps(dict(status='EXACT_METADATA_PACKAGED',members=len(members),uncompressed_bytes=manifest['uncompressed_bytes'],zip_bytes=manifest['compressed_bytes'],zip_sha256=manifest['zip_sha256'])))
