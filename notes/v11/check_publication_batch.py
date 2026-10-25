"""Verify one already submitted browser upload by reading only GitHub's published Git objects."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2];PLAN=ROOT/'.scratch/v11/publication-plan.json'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def main():
 a=argparse.ArgumentParser();a.add_argument('--directory',required=True);a.add_argument('--previous',required=True);a.add_argument('--current');a=a.parse_args()
 subprocess.run(['git','fetch','--quiet','--no-tags','origin','refs/heads/revision-v11:refs/remotes/origin/revision-v11'],cwd=ROOT,check=True)
 current=a.current or git('rev-parse','origin/revision-v11').decode().strip()
 plan=json.loads(PLAN.read_text());rows=plan['groups'][a.directory];expected={r['path']for r in rows}
 actual=set(git('diff','--name-only',a.previous,current).decode().splitlines());assert actual==expected,(actual,expected)
 checked=[]
 for row in rows:
  raw=git('show',current+':'+row['path']);assert hashlib.sha256(raw).hexdigest()==row['sha256']
  assert raw==git('show',plan['source_commit']+':'+row['path'])
  mode=git('ls-tree',current,'--',row['path']).decode().split()[0];assert mode=='100644',mode
  checked.append(dict(path=row['path'],bytes=len(raw),sha256=row['sha256'],mode=mode))
 record=dict(status='PASS',verified_utc=datetime.now(timezone.utc).isoformat(),previous=a.previous,published_commit=current,
             frozen_local_source=plan['source_commit'],directory=a.directory,files=checked)
 with(ROOT/'notes/v11/publication-batches.jsonl').open('a')as f:f.write(json.dumps(record)+'\n')
 print(json.dumps(dict(status='PASS',commit=current,directory=a.directory,files=len(rows),bytes=sum(x['bytes']for x in checked))))
if __name__=='__main__':main()
