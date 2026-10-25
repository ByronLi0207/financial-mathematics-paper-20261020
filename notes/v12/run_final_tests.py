"""Run the full inherited and v12 test suite with the fixed temporary runtime."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,os,time,hashlib
R=Path(__file__).resolve().parents[2];old=json.loads((R/'notes/v11/closure-tests.json').read_text());env=os.environ.copy();env.update(old['thread_environment']);env.update(old['additional_environment']);path=R/'.scratch/v12/final-pytest.txt';assert not path.exists();start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
with path.open('x')as out:q=subprocess.run(old['command'],cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT)
r=dict(status='PASS'if q.returncode==0 else'FAIL',start_utc=start,end_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,command=old['command'],thread_environment=old['thread_environment'],additional_environment=old['additional_environment'],exit_code=q.returncode,output_path=str(path.relative_to(R)),output_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),output_tail=path.read_text()[-4500:],scope='Full inherited plus v12 toy/unit suite in original qualified historical-object environment; no financial experiment rerun.')
f=R/'notes/v12/final-tests.json';assert not f.exists();f.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(q.returncode)
