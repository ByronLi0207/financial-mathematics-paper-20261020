"""Verify one browser-published branch batch by exact Git blob bytes."""
from pathlib import Path
import subprocess,json,datetime,sys,hashlib
R=Path(__file__).resolve().parents[2];directory=sys.argv[1];stage=R/'.scratch/v12/publish-final-3982092';groups=json.loads((stage/'groups.json').read_text());expected={str(Path(directory)/n)for n in groups[directory]}
subprocess.run(['git','fetch','origin','refs/heads/revision-v12:refs/remotes/origin/revision-v12'],cwd=R,check=True)
sha=subprocess.check_output(['git','rev-parse','origin/revision-v12'],cwd=R).decode().strip();files=set(subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',sha],cwd=R).decode().splitlines());assert files==expected,(files,expected)
for n in files:assert subprocess.check_output(['git','show',sha+':'+n],cwd=R)==(stage/n).read_bytes(),n
record=dict(public_commit=sha,directory=directory,files=len(files),source_local_commit='3982092',readback_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='EXACT_ALL_BLOBS_PASS')
with (R/'notes/v12/editorial-publication.jsonl').open('a')as f:f.write(json.dumps(record)+'\n')
print(json.dumps(record))
