import datetime as dt, hashlib, json, os, resource, subprocess, time
from pathlib import Path
root=Path.cwd();dest=root/'notes/revision-v9'
command=['/Users/bingyouli/.local/bin/uv','run','--no-project','--no-env-file','--python','/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3','--with','pytest','--with','arch','--with','scikit-learn','python','-B','v9_posthoc.py','--output','results/revision-v9/wp1']
env=dict(os.environ,UV_OFFLINE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(root/'.scratch/revision-v9/mpl-wp1'))
log=dest/'wp1-analysis-console.txt'; receipt=dest/'wp1-analysis-receipt.json'
if log.exists() or receipt.exists(): raise FileExistsError('immutable run evidence exists')
start=dt.datetime.now(dt.timezone.utc).isoformat();tick=time.monotonic()
maximum_sampled_descendant_rss=0; maximum_numeric_threads=0; observations=0; stopped=None
with log.open('w') as stream:
 p=subprocess.Popen(command,cwd=root,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 while p.poll() is None:
  raw=subprocess.check_output(['ps','-axo','pid=,ppid=,rss='],text=True)
  rows=[list(map(int,line.split())) for line in raw.splitlines() if line.strip()]
  ids={p.pid}
  for _ in range(5): ids.update(pid for pid,ppid,rss in rows if ppid in ids)
  rss=sum(rss*1024 for pid,ppid,rss in rows if pid in ids);maximum_sampled_descendant_rss=max(maximum_sampled_descendant_rss,rss)
  for pid,ppid,rss_kib in rows:
   if pid in ids and pid!=p.pid:
    try:
     threads=subprocess.check_output(['ps','-M','-p',str(pid),'-o','pid='],text=True,stderr=subprocess.DEVNULL)
     maximum_numeric_threads=max(maximum_numeric_threads,len([x for x in threads.splitlines() if x.strip()]))
    except subprocess.CalledProcessError: pass
  observations+=1
  if time.monotonic()-tick>595 or rss>2*1024**3 or maximum_numeric_threads>2:
   stopped='RESOURCE_BUDGET';os.killpg(p.pid,15);break
  time.sleep(.25)
 try: code=p.wait(timeout=4)
 except subprocess.TimeoutExpired: os.killpg(p.pid,9);code=p.wait()
peak=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
value=dict(command=command,cwd=str(root),started_utc=start,ended_utc=dt.datetime.now(dt.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,returncode=code,child_peak_rss_bytes=peak,sampled_process_tree_peak_rss_bytes=maximum_sampled_descendant_rss,maximum_observed_numeric_os_threads=maximum_numeric_threads,resource_samples=observations,stop_reason=stopped,numerical_workers=1,numerical_threads_configured=1,UV_OFFLINE=True,output_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
receipt.write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value,indent=2));print(log.read_text()[-4000:]);raise SystemExit(code if stopped is None else 124)
