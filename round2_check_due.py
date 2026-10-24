"""Real on-demand ten-minute task check; no daemon, sleep, or synthetic work time."""
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
from v3_revision import ROOT,dump
p=ROOT/'state/seven-hour-quality-state.json';s=json.loads(p.read_text());now=datetime.now(timezone.utc);last=datetime.fromisoformat(s['last_check_utc']);delta=(now-last).total_seconds()
if delta<600:print('Self-check not yet due; elapsed seconds:',delta);raise SystemExit(0)
r=json.loads((ROOT/'state/round2-state.json').read_text());check=subprocess.run([sys.executable,'-B','round2_preservation_check.py'],cwd=ROOT,capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
i=10
while (ROOT/f'state/self-check-20261023-{i:02}.json').exists():i+=1
s['last_check_utc']=now.isoformat();s['phase']='round2 '+r['current'];s['last_findings']=['Completed ordered steps:'+','.join(r['completed']),'Immutable original440 and old-final3 hashes checked now; no mismatches','Current provided feedback file unchanged unless its exact hash differs'];dump(p,s)
feedback=ROOT # only the explicitly supplied review file is read
path=r['plan_path'];sha=hashlib.sha256(__import__('pathlib').Path(path).read_bytes()).hexdigest()
dump(ROOT/f'state/self-check-20261023-{i:02}.json',dict(check=i,actual_utc=now.isoformat(),status='ACTIVE',phase=s['phase'],completed=r['completed'],preservation_stdout=check.stdout,preservation_stderr=check.stderr,feedback_file_sha256=sha,feedback_changed=sha!=r['plan_sha256'],native_Claude_inbox_checked=False,waiting_counted_as_work=False))
print('Self-check',i,now.isoformat(),'current',r['current'],'feedback changed',sha!=r['plan_sha256']);print(check.stdout)
