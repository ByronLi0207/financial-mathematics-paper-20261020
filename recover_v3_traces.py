"""B5: recover exact source traces, serially, without changing the archive.

No file is deleted. FX acquisition uses the original bounded anonymous endpoint;
failure is retained and the authorized Treasury-only fallback is used.
"""
import sys
sys.dont_write_bytecode = True
import os, json, hashlib, time, subprocess, csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PY=sys.executable
OUT=ROOT/'results/revision-20261023/recovery'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(path,b):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(b)
def js(path,v):save(path,(json.dumps(v,indent=2,allow_nan=False)+'\n').encode())
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'recovery.json').exists():raise RuntimeError('Retained run exists; inspect rather than overwrite')
    for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[n]='1'
    import reproduce_conditional as rep
    archive=rep.verify_archive(ROOT)
    spec=archive['spec'];sel=archive['selection']
    state=dict(archive_verified=True,workers=[],fx_status=None,treasury_status='PENDING')
    fx=ROOT/spec['sources']['fx_hourly']['input_relative_path']
    if not fx.exists():
        import study_data
        source=json.loads((ROOT/'protocol/study-spec.json').read_text())['source']
        started=time.monotonic()
        try:
            payload,facts=study_data._download(source,lambda:60-(time.monotonic()-started),None)
            raw=study_data._unpack(payload,source,lambda:60-(time.monotonic()-started),None)
            save(fx,raw);state['fx_download']=facts
            state['fx_status']='EXACT_SOURCE_RECOVERED'
        except study_data.SourceError as error:
            state['fx_status']='blocked: raw input unavailable'
            state['fx_failure']=dict(code=error.code,reason=error.reason)
    else:
        raw=fx.read_bytes();cfg=spec['sources']['fx_hourly']
        if (len(raw),sha(raw))!=(cfg['bytes'],cfg['sha256']):raise RuntimeError('Existing FX identity mismatch; STOP')
        state['fx_status']='EXACT_SOURCE_RECOVERED'
    js(OUT/'source-recovery.json',state)
    cfg=spec['sources']['nyfed_weekly'];ny=ROOT/cfg['input_relative_path']
    public=ROOT/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv';raw=public.read_bytes()
    assert (len(raw),sha(raw))==(cfg['bytes'],cfg['sha256'])
    if ny.exists():assert ny.read_bytes()==raw
    else:save(ny,raw)
    if state['fx_status']=='EXACT_SOURCE_RECOVERED':
        # The original controller is the requested all-source route.
        cmd=[PY,'-B','reproduce_conditional.py','replicate','--attempt-id','revision-v3-b5-full']
        p=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=600)
        save(OUT/'full-replication.stdout',p.stdout);save(OUT/'full-replication.stderr',p.stderr)
        state['full_replicate_returncode']=p.returncode
        js(OUT/'recovery.json',state)
        print(json.dumps(state));return
    # Preserve original selection receipt bytes at their frozen historical paths.
    for c in sel['cells']:
        key=tuple(c[n] for n in ('source','horizon','window','family'))
        receipt=(ROOT/rep.public_validation_name(key)).read_bytes()
        path=ROOT/rep.historical_validation_name(key)
        if path.exists():assert path.read_bytes()==receipt
        else:save(path,receipt)
    # Each worker owns a new directory; no parallel numerical experiments.
    selected=(ROOT/rep.SELECTION_PATH,rep.SELECTION)
    jobs=[j for phase in ('evaluation','references') for j in rep.phase_jobs(spec,phase) if j[1]=='nyfed_weekly']
    for job in jobs:
        phase,s,h,w,f=job
        attempt=ROOT/'.scratch/v3-recovery'/(f'{phase}-{s}-h{h}-w{w}'+('' if f is None else '-'+f))
        if attempt.exists():raise RuntimeError('Worker attempt exists; do not overwrite')
        cmd=[PY,'-B','run_conditional_study.py','--phase',phase,'--source',s,'--horizon',str(h),'--window',str(w),'--attempt-dir',str(attempt),'--freeze-sha256',rep.FREEZE]
        if f:cmd+=['--family',f,'--selection-freeze',str(selected[0]),'--selection-sha256',selected[1]]
        p=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=600)
        save(OUT/(attempt.name+'.stdout'),p.stdout);save(OUT/(attempt.name+'.stderr'),p.stderr)
        receipt=json.loads((attempt/'public/manifest.json').read_text())
        item=dict(job=list(job),attempt=str(attempt.relative_to(ROOT)),returncode=p.returncode,status=receipt['status'],stop_code=receipt['stop_code'],resources=receipt['resources'])
        state['workers'].append(item)
        print(json.dumps(item),flush=True)
        if p.returncode or receipt['status']!='COMPLETE':
            state['treasury_status']='STOPPED_WORKER_FAILURE';js(OUT/'recovery.json',state);return
    state['treasury_status']='TRACES_RECOVERED_AWAITING_RECONCILIATION'
    js(OUT/'recovery.json',state)
if __name__=='__main__':main()
