"""Separate scalar, target, count and selection audit; no forecast fits."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import subprocess
import zipfile

import numpy as np

from final_merge_wp2 import scalar_trace, scalar_hac, check_maturity

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/final-merge/wp2-cftc-mechanism'


def read(path):return json.loads(Path(path).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify():
    summary=read(OUT/'summary.json');seal=read(ROOT/'protocol/final-merge/wp2-input-seal.json')
    mismatches=[];checks=0;max_abs=0.;maturity_rows=0;validation_reports=0
    def need(condition,label):
        nonlocal checks
        checks+=1
        if not condition:mismatches.append(label)
    def close(a,b,label):
        nonlocal max_abs
        if a is None or b is None:need(a is b,label);return
        error=abs(float(a)-float(b));max_abs=max(max_abs,error)
        need(math.isfinite(error) and error<=1e-10+1e-12*abs(float(b)),label)
    def trace_check(path,x,first,last,label):
        with np.load(path,allow_pickle=False) as data:
            t={k:data[k].copy() for k in data.files}
        need(t['origins'].tolist()==list(range(first,last+1)),label+' axis')
        audit=scalar_trace(x,t['origins'].tolist(),t['capacities'].tolist(),6)
        for key,values in audit.items():
            need(len(values)==len(t[key]),label+' '+key+' count')
            for i,(a,b) in enumerate(zip(values,t[key])):
                if key=='strict_breach':need(bool(a)==bool(b),label+f' breach[{i}]')
                else:close(a,b,label+f' {key}[{i}]')
        return t,math.fsum(audit['pinball'])/len(audit['pinball']),sum(audit['strict_breach'])
    for r in seal['inputs']:
        need(sha(ROOT/r['path'])==r['sha256'],r['path']+' frozen SHA')
    start=read(OUT/'start.json');commit=start['protocol_commit']
    for path in ('protocol/final-merge/wp2-cftc-mechanism.md','protocol/final-merge/wp2-input-seal.json'):
        blob=subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT)
        need(blob==(ROOT/path).read_bytes(),path+' registered commit bytes')
    sources=read(ROOT/'results/v10/cftc/sources.json');traces={};scalars={}
    with zipfile.ZipFile(ROOT/'results/v10/cftc/formal/units.zip') as old:
        for s in sources:
            si=s['source_index']
            with np.load(ROOT/s['path'],allow_pickle=False) as a:x=a['position'].tolist()
            for w in (52,260,520):
                for method in ('F','QR4','QR33'):
                    tag=f's{si:02d}/W{w}/{method}'
                    cell=next(r for r in summary['cells'] if (r['source_index'],r['window'],r['method'])==(si,w,method))
                    if w<520:row=json.loads(old.read(f's{si:02d}/W{w}/result-{method}.json'))
                    else:
                        path=OUT/f'units/s{si:02d}/result-{method}.json'
                        row=read(path) if path.exists() else dict(status='NA')
                    need(cell['status']==row['status'],tag+' status')
                    if row['status']!='COMPLETE':continue
                    trace_path=ROOT/cell['trace_path']
                    need(sha(trace_path)==row['trace_sha256']==cell['trace_sha256'],tag+' trace SHA')
                    t,mean,hits=trace_check(trace_path,x,611,870,tag)
                    close(mean,row['mean_loss'],tag+' result mean')
                    close(mean,cell['mean_loss'],tag+' cell mean')
                    need(hits==row['strict_breach_count']==cell['strict_breach_count'],tag+' breach count')
                    traces[(si,w,method)]=t;scalars[(si,w,method)]=(mean,hits)
                    if w!=520:continue
                    unit=OUT/f'units/s{si:02d}'
                    rec=read(unit/f'W520_H6_{method}.json')
                    need(rec['status']==row['status'],tag+' method receipt')
                    diag=rec['fit_diagnostics']
                    maturity_rows+=check_maturity(diag,w,6,method!='F')
                    need([d['refit_index'] for d in diag]==list(range(611,871,13)),tag+' exact evaluation refit grid')
                    if method=='F' or row['selected_penalty']=='inf':
                        # Independently derive every empirical capacity from raw
                        # target headroom and the recorded ordinary/corrected rank.
                        rank=math.ceil((w+1)*19/20) if method=='F' else math.ceil(w*19/20)
                        for j,i in enumerate(range(611,871)):
                            r=611+13*((i-611)//13)
                            headrooms=sorted(max(abs(v) for v in x[k:k+7])-abs(x[k]) for k in range(r-6-w+1,r-6+1))
                            cap=abs(x[i])+headrooms[rank-1]
                            close(cap,t['capacities'][j],tag+f' independent empirical capacity[{j}]')
                    if method=='F':continue
                    candidates=rec['candidates'];menu=[.001,.01,.1,1.,10.,'inf']
                    need([r['penalty'] for r in candidates]==menu,tag+' full menu')
                    completed=[]
                    for index,c in enumerate(candidates):
                        if c['status']!='COMPLETE':continue
                        validation_reports+=1
                        vp=unit/f"validation-{method}-{str(c['penalty'])}.npz"
                        vt,vm,vh=trace_check(vp,x,553,604,tag+f'/candidate{index}')
                        close(vm,c['mean_loss'],tag+f'/candidate{index} loss')
                        need(c['origin_count']==52,tag+f'/candidate{index} complete')
                        maturity_rows+=check_maturity(c['fit_diagnostics'],520,6,True)
                        need([d['refit_index'] for d in c['fit_diagnostics']]==list(range(553,605,13)),tag+f'/candidate{index} refit grid')
                        for d in c['fit_diagnostics']:
                            if c['penalty']!='inf':
                                for metric,tol in [('duality_gap','gap_tolerance'),('primal_residual','primal_tolerance'),('dual_residual','dual_tolerance')]:
                                    need(d[metric]<=d[tol],tag+f'/candidate{index} solver '+metric)
                        completed.append((float(c['mean_loss']),-index,c['penalty']))
                    eligible=bool(completed) and (method=='QR4' or len(completed)==6)
                    need(eligible,tag+' eligible selected result')
                    if eligible:need(min(completed)[2]==row['selected_penalty'],tag+' exact selected penalty')
    independent=[]
    for r in summary['comparisons']:
        key=(r['source_index'],r['window']);fkey=(*key,'F');mkey=(*key,r['method'])
        delta=None
        if fkey in traces and mkey in traces and scalars[fkey][0]>0:
            delta=100*(scalars[mkey][0]/scalars[fkey][0]-1)
            close(delta,r['relative_loss_percent'],str(mkey)+' relative loss')
            d=[float(q)-float(f) for q,f in zip(traces[mkey]['pinball'],traces[fkey]['pinball'])]
            dm=scalar_hac(d,6)
            need(dm['status']==r['dm']['status'],str(mkey)+' HAC status')
            for field in ('n','horizon','bandwidth','mean_difference','lrv','dm_t','dm_p'):
                close(dm[field],r['dm'][field],str(mkey)+' HAC '+field)
        else:need(r['relative_loss_percent'] is None,str(mkey)+' missing paired loss')
        independent.append(dict(si=key[0],w=key[1],method=r['method'],delta=delta))
    # Independent integer count decisions; no call to production screen(),
    # primary_status() or strict_decrease(). Unknowns remain in denominator.
    def decision(values,percent):
        n=len(values);s=sum(x is True for x in values);u=sum(x is None for x in values)
        return 'SUPPORT' if 100*s>=percent*n else 'NOT_SUPPORT' if 100*(s+u)<percent*n else 'NOT_TESTABLE'
    expected={};counterkeys=[]
    for method in ('QR4','QR33'):
        root=seal['rstar'][method]['point']
        for test in ('P1','P2'):
            rows=[r for r in independent if r['method']==method and ((r['w']/7<root/2) if test=='P1' else (r['w']/7>2*root))]
            outcomes=[None if r['delta'] is None else r['delta']>0 if test=='P1' else r['delta']<0 for r in rows]
            key=test+'_'+method
            expected[key]=decision(outcomes,80 if test=='P1' else 60) if rows else 'NOT_TESTABLE'
            need(expected[key]==summary['tests'][key]['status'],key+' decision')
            if rows:
                need(len(rows)==summary['tests'][key]['planned'],key+' planned denominator')
                need(sum(v is True for v in outcomes)==summary['tests'][key]['successes'],key+' successes')
                need(sum(v is None for v in outcomes)==summary['tests'][key]['unknown'],key+' unknowns')
            counterkeys.extend((key,r['si'],r['w'],method) for r,v in zip(rows,outcomes) if v is not True)
    outcomes=[]
    for s in sources:
        si=s['source_index'];v=[next(r['delta'] for r in independent if (r['si'],r['w'],r['method'])==(si,w,'QR4')) for w in (52,260,520)]
        valid=None if any(x is None for x in v) else v[0]>v[1] and v[1]>v[2]
        outcomes.append(valid)
        if valid is not True:counterkeys.append(('P3_QR4',si,None,None))
    expected['P3_QR4']=decision(outcomes,70)
    need(expected['P3_QR4']==summary['tests']['P3_QR4']['status'],'P3 decision')
    p1='NOT_SUPPORT' if 'NOT_SUPPORT' in (expected['P1_QR4'],expected['P1_QR33']) else 'SUPPORT' if expected['P1_QR4']==expected['P1_QR33']=='SUPPORT' else 'NOT_TESTABLE'
    p2=expected['P2_QR4']
    verdict='NOT_TESTABLE' if 'NOT_TESTABLE' in (p1,p2) else 'SUPPORT' if p1==p2=='SUPPORT' else 'PARTLY' if 'SUPPORT' in (p1,p2) else 'NOT_SUPPORT'
    need(verdict==summary['primary_verdict'],'primary verdict')
    actualkeys=[(r['screen'],r['source_index'],r.get('window'),r.get('method')) for r in summary['counterexamples']]
    need(sorted(map(str,counterkeys))==sorted(map(str,actualkeys)),'all counterexamples and unknowns')
    receipt=dict(checked_utc=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        status='PASS' if not mismatches else 'MISMATCH',mismatch_count=len(mismatches),mismatches=mismatches,
        scalar_and_identity_checks=checks,maximum_absolute_difference=max_abs,
        tolerance=dict(absolute=1e-10,relative=1e-12),complete_traces=len(traces),
        complete_validation_reports=validation_reports,maturity_diagnostic_rows=maturity_rows,
        protocol_commit=commit,primary_verdict=verdict,independent_decisions=expected,
        counterexample_or_unknown_count=len(counterkeys),new_model_refits=0,
        scope='Separate scalar target/score/HAC/selection/maturity/count implementation by the sole executor; no second person, data reproduction or solver refit')
    path=OUT/'independent-verification.json'
    with path.open('x') as f:json.dump(receipt,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(receipt,indent=2))
    return 0 if not mismatches else 1


if __name__=='__main__':raise SystemExit(verify())
