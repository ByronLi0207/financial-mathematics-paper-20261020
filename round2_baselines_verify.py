"""Independent scalar saved-output and failure readback; no estimator fitting."""
import csv,hashlib,json,math
from pathlib import Path
import numpy as np
from conditional_sources import load_source
from v3_revision import ROOT,RESULT,dump

OUT=RESULT/'round2/baselines'

def classification(r):
    if r['status']=='COMPLETE':return dict(kind='COMPLETE')
    detail=r.get('failure_context',{}).get('detail',{})
    g=detail.get('garch_failure',{});p=g.get('native_parameters',{})
    if p:
        persistence=p['alpha']+p['beta'];ceiling=1.+1e-10
        only=(g['optimizer']['convergence_flag']==0 and p['omega']>0 and p['alpha']>=0 and p['beta']>=0 and persistence>ceiling)
        return dict(kind='PERSISTENCE_GATE_WITH_OPTIMIZER_SUCCESS' if only else 'OTHER_GARCH_FAILURE',optimizer_convergence_flag=g['optimizer']['convergence_flag'],persistence=persistence,persistence_minus_one=persistence-1.,declared_ceiling=ceiling,excess_over_declared_ceiling=persistence-ceiling,interpretation='No scoring or relaxed-tolerance rerun; this is not optimizer nonconvergence or a performance comparison.')
    if 'structurally unavailable' in r.get('failure_reason',''):
        return dict(kind='POT_STRUCTURAL_TAIL_SIZE',tail_sample_window=r['window'],maximum_nominal_tail_count=r['window']//10,required_strict_exceedances=20)
    return dict(kind=r.get('failure_type','UNCLASSIFIED'),reason=r.get('failure_reason'))

def scalar_dm(diff,h,L):
    n=len(diff);mean=math.fsum(diff)/n
    # Deliberately separate Python scalar contractions from the production BLAS HAC.
    center=[float(x)-mean for x in diff]
    v=math.fsum(x*x for x in center)/n
    for k in range(1,L+1):v+=2*(1-k/(L+1))*math.fsum(center[j]*center[j-k] for j in range(k,n))/n
    t=mean/math.sqrt(v/n);factor=math.sqrt((n+1-2*h+h*(h-1)/n)/n)
    from scipy.stats import t as student
    return dict(mean_difference=mean,lrv=v,dm_t=t,dm_p=math.erfc(abs(t)/math.sqrt(2)),hln_t=t*factor,hln_p=float(2*student.sf(abs(t*factor),n-1)))

def fixed_garch_readback(r,x):
    """Evaluate already stored coefficients, with NO optimizer or new forecast."""
    from arch import arch_model
    detail=r['failure_context']['detail'];g=detail['garch_failure'];bounds=detail['failed_refit']
    a,k=bounds['training_first_origin'],bounds['refit_index'];delta=np.diff(x[a:k+1]);rms=g['normalization_rms'];p=g['normalized_parameters']
    fixed=arch_model(delta/rms,mean='Constant',vol='GARCH',p=1,o=0,q=1,dist='normal',rescale=False).fix([p[n] for n in ('mu','omega','alpha[1]','beta[1]')])
    v=np.asarray(fixed.conditional_volatility,dtype=float)**2*rms*rms;residual=np.asarray(fixed.std_resid,dtype=float)
    def sha(z):return hashlib.sha256(np.asarray(z,dtype='<f8').tobytes()).hexdigest()
    return dict(optimizer_called=False,new_forecasts_issued=False,increment_count=len(delta),variance_shape_matches=bool(v.shape==delta.shape),residual_shape_matches=bool(residual.shape==delta.shape),positive_finite_variances=bool(np.isfinite(v).all() and np.all(v>0)),finite_residual_pool=bool(np.isfinite(residual).all()),conditional_variance_sha256_matches=sha(v)==g['conditional_variance_sha256'],residual_pool_sha256_matches=sha(residual)==g['residual_pool_sha256'])

def main():
    from run_v3_inference import traces
    reference=traces();spec=json.loads((ROOT/'protocol/revision-20261022/study-spec.json').read_text());series={}
    for s,cfg in spec['sources'].items():series[s]=load_source(ROOT/cfg['input_relative_path'],s,expected_sha256=cfg['sha256'],expected_bytes=cfg['bytes']).position
    records=[json.loads((OUT/f'{s}-h{h}-w{w}-{m}.json').read_text()) for s,ws in [('fx_hourly',(720,2880)),('nyfed_weekly',(52,260))] for h in (6,24) for w in ws for m in ('FHS','PEAK_POT','QRF')]
    completed=0;scored=0;fits=0;errors={k:0. for k in ('mean_pinball','mean_difference','lrv_relative','dm_t','dm_p','hln_p')};failures=[]
    for r in records:
        s,h,w,m=(r[k] for k in ('source','horizon','window','method'))
        assert r['post_result'] and r['exploratory']
        if r['status']!='COMPLETE':
            assert r['evaluation'] is None and r['comparisons']==[]
            detail=classification(r)
            if detail['kind']=='PERSISTENCE_GATE_WITH_OPTIMIZER_SUCCESS':
                check=fixed_garch_readback(r,series[s]);detail['fixed_parameter_readback']=check
                assert all(check[k] for k in ('variance_shape_matches','residual_shape_matches','positive_finite_variances','finite_residual_pool','conditional_variance_sha256_matches','residual_pool_sha256_matches'))
                detail['all_other_recorded_admissibility_conditions_verified']=True
            failures.append(dict(source=s,horizon=h,window=w,method=m,issued_before_failure=r.get('completed_origin_count'),**detail))
            continue
        completed+=1;f=reference[s,h,w,'frozen_F'];qr=reference[s,h,w,'QR'];path=ROOT/r['private_trace']
        with np.load(path,allow_pickle=False) as z:a={k:z[k].copy() for k in z.files}
        assert np.array_equal(a['origins'],f['origins']) and np.array_equal(a['peak'],f['peak']) and np.array_equal(a['floor'],f['floor'])
        x=series[s];o=a['origins'];cap=a['capacity'];peak=np.array([max(abs(float(z)) for z in x[t:t+h+1]) for t in o])
        assert np.array_equal(peak,a['peak']) and np.array_equal(np.abs(x[o]),a['floor']) and np.all(cap>=a['floor'])
        losses=[.95*max(float(y-c),0.)+.05*max(float(c-y),0.) for y,c in zip(peak,cap)];hits=sum(y>c for y,c in zip(peak,cap));mean=math.fsum(losses)/len(losses)
        assert np.array_equal(np.array(losses),a['pinball']);assert hits==r['evaluation']['strict_breach_count'];assert mean==r['evaluation']['mean_pinball']
        errors['mean_pinball']=max(errors['mean_pinball'],abs(mean-r['evaluation']['mean_pinball']));scored+=len(o)
        step=spec['sources'][s]['refit_step'];expected=np.array([int(o[0])+step*((int(t)-int(o[0]))//step) for t in o]);assert np.array_equal(expected,a['refit_indices'])
        assert [p['refit_index'] for p in r['refits']]==sorted(set(expected.tolist()))
        for p in r['refits']:
            k=p['refit_index'];assert p['training_first_origin']==k-h-w+1 and p['training_last_origin']==k-h and p['latest_label_end']==k and p['training_count']==w;fits+=1
            if m in ('FHS','PEAK_POT'):assert p['increment_count']==w+h-1 and p['increment_last_end']==k and p['increment_first_end']==k-h-w+2
            if m=='FHS':
                text=f'20261023|{s}|{h}|{w}|{k}';seed=int.from_bytes(hashlib.sha256(text.encode()).digest()[:8],'big');assert p['scenarios']==2048 and p['seed_input']==text and p['seed']==seed
            if m=='QRF':assert p['bootstrap_multiplicity_in_cdf'] is False and p['forest_parameters']['n_estimators']==100 and p['forest_parameters']['n_jobs']==1
        for row in r['comparisons']:
            b=f if row['right_method']=='frozen_F' else qr;d=[float(y)-float(z) for y,z in zip(losses,b['pinball'])]
            for prefix,L in [('',row['bandwidth']),('double_',row['double_bandwidth'])]:
                independent=scalar_dm(d,h,L)
                for key in ('dm_t','dm_p','hln_p'):
                    actual=row[prefix+key];err=abs(independent[key]-actual);errors[key]=max(errors[key],err);assert math.isclose(independent[key],actual,rel_tol=3e-11,abs_tol=3e-12),(s,h,w,m,prefix,key,err)
                if not prefix:
                    errors['mean_difference']=max(errors['mean_difference'],abs(independent['mean_difference']-row['mean_difference']));errors['lrv_relative']=max(errors['lrv_relative'],abs(independent['lrv']-row['lrv'])/row['lrv'])
                    assert math.isclose(independent['lrv'],row['lrv'],rel_tol=3e-12)
        for fact in r['private_files']:
            p=path.parent/fact['name'];assert p.stat().st_size==fact['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==fact['sha256']
    pairs=list(csv.DictReader((OUT/'paired-tests.csv').open()));assert len(pairs)==48
    work=[float(p['dm_p']) if p['status']=='OK' else 1. for p in pairs];order=sorted(range(48),key=lambda i:(work[i],i));adjusted=[None]*48;running=0.
    for rank,index in enumerate(order):running=max(running,(48-rank)*work[index]);adjusted[index]=min(1.,running)
    for i,p in enumerate(pairs):
        if p['status']=='OK':assert math.isclose(adjusted[i],float(p['holm_p']),rel_tol=0,abs_tol=1e-15)
        else:assert p['holm_p']==''
    report=dict(status='VERIFIED_SAVED_OUTPUTS_NOT_REFITTING',planned_cells=len(records),complete_cells=completed,NA_cells=len(failures),independently_scored_origins=scored,verified_refit_receipts=fits,maturity_or_label_or_floor_mismatches=0,separate_Holm_slots=48,scalar_check_max_errors=errors,failures=failures,statistical_validity_claim=False)
    dump(OUT/'independent-readback.json',report);print(json.dumps(report,ensure_ascii=False,allow_nan=False,indent=2))

if __name__=='__main__':main()
