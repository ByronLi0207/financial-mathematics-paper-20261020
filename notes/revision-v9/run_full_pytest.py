"""Default complete discovery in a fresh copy, cached dependencies only."""
import datetime as dt, hashlib, json, os, resource, shutil, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
stage=sys.argv[1]
if not stage.replace('-','').isalnum():raise ValueError('simple stage required')
scratch=ROOT/'.scratch/revision-v9'/stage;copy=scratch/'full-suite-copy'
copy.mkdir(parents=True,exist_ok=False)
paths=[p.decode() for p in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).split(b'\0') if p]
for name in paths:
 target=copy/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,target)
env=dict(os.environ);env.pop('PYTHONPATH',None)
temporary=scratch/'unittest-temp';temporary.mkdir()
env['TMPDIR']=str(temporary)
env.update(UV_OFFLINE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
cmd=['/Users/bingyouli/.local/bin/uv','run','--no-project','--no-env-file','--python','/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3','--with','pytest','--with','arch','--with','scikit-learn','python','-B','-m','pytest','-p','no:cacheprovider','-v','--basetemp',str(scratch/'pytest-temp')]
log=ROOT/'notes/revision-v9'/(stage+'-pytest-output.txt');receipt=log.with_name(stage+'-pytest-receipt.json')
if log.exists() or receipt.exists():raise FileExistsError('existing run evidence')
start=dt.datetime.now(dt.timezone.utc).isoformat();tick=time.monotonic();stop=None;peak_sampled=0
with log.open('w') as stream:
 process=subprocess.Popen(cmd,cwd=copy,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 while process.poll() is None:
  rows=[list(map(int,line.split())) for line in subprocess.check_output(['ps','-axo','pid=,ppid=,rss='],text=True).splitlines() if line.strip()]
  ids={process.pid}
  for _ in range(5):ids.update(pid for pid,ppid,rss in rows if ppid in ids)
  observed=sum(rss*1024 for pid,ppid,rss in rows if pid in ids);peak_sampled=max(peak_sampled,observed)
  if time.monotonic()-tick>595 or observed>2*1024**3:stop='RESOURCE_BUDGET';os.killpg(process.pid,15);break
  time.sleep(.5)
 try:code=process.wait(timeout=4)
 except subprocess.TimeoutExpired:os.killpg(process.pid,9);code=process.wait()
value=dict(command=cmd,cwd=str(copy),scope='Full default discovery; every tracked/indexed file copied; no test filter or skips added',tracked_files_copied=len(paths),started_utc=start,ended_utc=dt.datetime.now(dt.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,returncode=code,child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,sampled_process_tree_peak_rss_bytes=peak_sampled,stop_reason=stop,output_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),numerical_threads=1,UV_OFFLINE=True)
receipt.write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value,indent=2));print('\n'.join(log.read_text().splitlines()[-8:]));raise SystemExit(code if stop is None else 124)
