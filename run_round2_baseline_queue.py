"""One active serial queue; executed cells are not retried automatically."""
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
from v3_revision import ROOT,dump
from round2_evidence import run
v=json.loads((ROOT/'results/revision-20261023/round2/D1-temporary-runtime-invocation.json').read_text())
binding=json.loads((ROOT/'protocol/revision-20261023/round2-D1-execution-binding-v2.json').read_text())
for name,sha in binding['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
p=ROOT/'state/round2-baselines-queue.json'
if p.exists():raise RuntimeError('Existing queue retained; resume explicitly from its unexecuted rows, never reset outcomes')
rows=[dict(source=s,horizon=h,window=w,method=m,status='QUEUED') for m in ('FHS','PEAK_POT','QRF') for s,ws in [('fx_hourly',(720,2880)),('nyfed_weekly',(52,260))] for h in (6,24) for w in ws]
queue=dict(started_utc=datetime.now(timezone.utc).isoformat(),status='RUNNING',serial=True,cells=rows);dump(p,queue)
for i,r in enumerate(rows):
    r['status']='RUNNING';r['started_utc']=datetime.now(timezone.utc).isoformat();dump(p,queue)
    run('D1',v['argv_prefix']+['round2_baselines_run.py','--mode','cell','--source',r['source'],'--horizon',str(r['horizon']),'--window',str(r['window']),'--method',r['method']],env=v['environment'],timeout=620)
    out=ROOT/'results/revision-20261023/round2/baselines'/f"{r['source']}-h{r['horizon']}-w{r['window']}-{r['method']}.json";record=json.loads(out.read_text());r.update(status=record['status'],ended_utc=datetime.now(timezone.utc).isoformat(),receipt=str(out.relative_to(ROOT)));dump(p,queue)
    print('PROGRESS',i+1,'of24',r['source'],r['horizon'],r['window'],r['method'],r['status'],flush=True)
    q=subprocess.run([sys.executable,'-B','round2_check_due.py'],cwd=ROOT,capture_output=True,text=True);assert q.returncode==0,q.stdout+q.stderr
    if q.stdout.startswith('Self-check ' ) and 'not yet' not in q.stdout:print(q.stdout,flush=True)
run('D1',v['argv_prefix']+['round2_baselines_run.py','--mode','aggregate'],env=v['environment'],timeout=120)
queue.update(status='COMPLETE_ALL_PLANNED_ATTEMPTS',ended_utc=datetime.now(timezone.utc).isoformat());dump(p,queue)
