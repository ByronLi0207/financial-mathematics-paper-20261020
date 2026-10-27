"""Restore only the already archived official templates; no network access."""
from pathlib import Path
import hashlib, json, shutil, zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
for row in json.loads((ROOT/'notes/submission/template-downloads.json').read_text()):
    archive = ROOT/'submission-package/templates'/row['filename']
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == row['sha256']
    folder = archive.with_suffix('')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist():
            target = folder/name
            assert target.resolve().is_relative_to(folder.resolve())
            if name.endswith('/'):
                target.mkdir(parents=True, exist_ok=True)
                continue
            raw = z.read(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != raw:
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                shutil.copyfile(target, target.with_name(target.name+'.'+stamp+'.bak'))
            if not target.exists() or target.read_bytes() != raw:
                target.write_bytes(raw)
    print(row['filename'], 'verified and extracted locally')
