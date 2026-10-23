import json,hashlib,subprocess
from pathlib import Path
from v3_revision import ROOT
r=json.loads((ROOT/'results/revision-20261023/baseline-identities.json').read_text());bad=[]
for name,fact in r['original_tracked_files'].items():
 p=ROOT/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=fact['sha256']:bad.append(name)
old=[]
for name,sha in r['protected_old_final_files'].items():
 if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=sha:old.append(name)
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT).decode().strip();print(json.dumps(dict(branch=branch,original_file_count=len(r['original_tracked_files']),original_mismatches=bad,old_final_file_count=len(r['protected_old_final_files']),old_final_mismatches=old,FINAL_md_sha256=hashlib.sha256((ROOT/'FINAL.md').read_bytes()).hexdigest()),ensure_ascii=False));assert not bad and not old;assert branch=='revision-v3-readability'
