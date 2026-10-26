"""Committed v9 confirmation primitives; no import-time draw or file write."""
import copy
import hashlib
import math
import numpy as np

def student_innovations(draws):
    return np.asarray(draws,dtype=float)*math.sqrt(3/5)

def regime_innovations(normals, uniforms):
    z,u=np.asarray(normals,float),np.asarray(uniforms,float)
    if z.ndim!=1 or u.shape!=(len(z)+1,) or not np.isfinite(z).all() or not np.isfinite(u).all() or np.any((u<0)|(u>=1)):
        raise ValueError('invalid regime primitive draws')
    states=np.empty(len(z),dtype=np.int64);state=int(u[0]>=.5)
    for i in range(len(z)):
        states[i]=state
        if u[i+1]<.02:state=1-state
    return z*np.where(states==0,1.,3.)/math.sqrt(5),states

def jump_innovations(normals, counts, positive_counts):
    z,k,b=np.asarray(normals,float),np.asarray(counts),np.asarray(positive_counts)
    if z.shape!=k.shape or k.shape!=b.shape or k.dtype.kind not in 'iu' or b.dtype.kind not in 'iu' or np.any(k<0) or np.any(b<0) or np.any(b>k) or not np.isfinite(z).all():
        raise ValueError('invalid compound-Poisson primitive draws')
    return (z+5*(2*b-k))/math.sqrt(1.25)

def level_path(innovations, phi, burn_in):
    eps=np.asarray(innovations,float)
    if eps.ndim!=1 or not np.isfinite(eps).all() or not math.isfinite(phi) or abs(phi)>=1 or not 0<=burn_in<len(eps):
        raise ValueError('invalid level process')
    out=np.empty(len(eps));previous=0.
    for i,shock in enumerate(eps):
        previous=phi*previous+shock;out[i]=previous
    if not np.isfinite(out).all():raise ValueError('nonfinite level process')
    return out[burn_in:].copy()

def make_process(rep, dgp_index, phi, design):
    n=design['burn_in']+design['retained_observations']
    streams=[np.random.Generator(np.random.PCG64(np.random.SeedSequence(design['master_entropy'],spawn_key=(rep,dgp_index,s)))) for s in range(3)]
    initial=[copy.deepcopy(r.bit_generator.state) for r in streams]
    if dgp_index==0:
        eps=student_innovations(streams[0].standard_t(5,size=n))
    elif dgp_index==1:
        eps,_=regime_innovations(streams[0].standard_normal(n),streams[1].random(n+1))
    elif dgp_index==2:
        z=streams[0].standard_normal(n);counts=streams[1].poisson(.01,size=n)
        eps=jump_innovations(z,counts,streams[2].binomial(counts,.5))
    else:raise ValueError('unknown frozen DGP')
    position=level_path(eps,phi,design['burn_in'])
    return position,dict(stream_key=[rep,dgp_index],master_entropy=design['master_entropy'],initial_states=initial,final_states=[copy.deepcopy(r.bit_generator.state) for r in streams],innovation_sha256=hashlib.sha256(eps.astype('<f8').tobytes()).hexdigest(),position_sha256=hashlib.sha256(position.astype('<f8').tobytes()).hexdigest(),innovation_count=n)

def choose_reductions(projected_by_window, projected_overhead, remaining_seconds):
    if set(projected_by_window)!={52,260,720,2880} or any(not math.isfinite(v) or v<0 for v in [*projected_by_window.values(),projected_overhead,remaining_seconds]):
        raise ValueError('invalid runtime-only budget projection')
    projected=math.fsum(projected_by_window.values())+projected_overhead
    allowance=.9*remaining_seconds;removed=[]
    for w in (52,260,720,2880):
        if projected<=allowance:break
        removed.append(w);projected-=projected_by_window[w]
    return dict(removed_windows=removed,projected_seconds_before=math.fsum(projected_by_window.values())+projected_overhead,projected_seconds_after=projected,remaining_seconds=remaining_seconds,allowance_seconds=allowance,can_continue=projected<=allowance)

def fraction_screen(outcomes, minimum_fraction):
    if not outcomes:raise ValueError('empty confirmation region')
    if any(x is not None and type(x) is not bool for x in outcomes):raise ValueError('invalid outcome')
    n=len(outcomes);success=sum(x is True for x in outcomes);missing=sum(x is None for x in outcomes)
    lower=success/n;upper=(success+missing)/n
    status='NOT_SUPPORT' if upper<minimum_fraction else ('INCONCLUSIVE' if missing else ('SUPPORT' if lower>=minimum_fraction else 'NOT_SUPPORT'))
    return dict(status=status,successes=success,missing=missing,denominator=n,lower_bound=lower,upper_bound=upper,observed_fraction=success/n if not missing else None,minimum_fraction=minimum_fraction)

def aggregate_pair(model, reference, planned):
    from v8_mechanism_mc import summary_from_repetitions
    a={r['rep']:r for r in model};b={r['rep']:r for r in reference}
    expected=set(range(planned))
    if len(a)!=len(model) or len(b)!=len(reference) or set(a)!=expected or set(b)!=expected:
        raise ValueError('duplicate/missing planned replication identity')
    rows=[]
    for rep in range(planned):
        x,y=a[rep],b[rep]
        if x['status']=='COMPLETE' and y['status']=='COMPLETE':
            rows.append(dict(rep=rep,status='COMPLETE',model_loss=x['evaluation']['mean_loss'],reference_loss=y['evaluation']['mean_loss'],model_breach_rate=x['evaluation']['strict_breach_rate'],reference_breach_rate=y['evaluation']['strict_breach_rate']))
        elif x['status']=='FAILED' or y['status']=='FAILED':rows.append(dict(rep=rep,status='FAILED'))
        elif x['status']=='NOT_ATTEMPTED' or y['status']=='NOT_ATTEMPTED':rows.append(dict(rep=rep,status='NOT_ATTEMPTED'))
        else:rows.append(dict(rep=rep,status='FAILED'))
    return summary_from_repetitions(rows,planned)

def confirmation_screen(summaries, design):
    conditional=[r for r in summaries if r['method'] in ('QR33','QR4')]
    def primary(rows):
        screens={}
        for name,low in (('P1',True),('P2',False)):
            values=[];keys=[]
            for r in rows:
                threshold=design['thresholds'][r['method']]['r_star'];metric=r['window']/(r['horizon']+1)
                eligible=metric<threshold/2 if low else metric>2*threshold
                if not eligible:continue
                delta=r['full_procedure_relative_loss_percent']
                values.append(None if delta is None else bool(delta>0 if low else delta<0))
                keys.append([r[k] for k in ('dgp','phi_index','window','horizon','method')])
            screens[name]=dict(fraction_screen(values,.8 if low else .6),cells=keys,outcomes=values)
        statuses=[v['status'] for v in screens.values()]
        screens['primary_status']='NOT_SUPPORT' if 'NOT_SUPPORT' in statuses else ('INCONCLUSIVE' if 'INCONCLUSIVE' in statuses else 'SUPPORT')
        return screens
    output=primary(conditional)
    if output['P1']['denominator']!=48 or output['P2']['denominator']!=24:
        raise ValueError('frozen primary region census mismatch')
    output['by_method']={m:primary([r for r in conditional if r['method']==m]) for m in ('QR33','QR4')}
    output['by_DGP']={d:primary([r for r in conditional if r['dgp']==d]) for d in design['dgp']}
    indexed={(r['dgp'],r['phi_index'],r['window'],r['horizon'],r['method']):r for r in conditional}
    values=[];pairs=[]
    for dgp in design['dgp']:
        for pi in range(2):
            for w in design['windows']:
                for h in design['horizons']:
                    a=indexed[dgp,pi,w,h,'QR4']['full_procedure_relative_loss_percent'];b=indexed[dgp,pi,w,h,'QR33']['full_procedure_relative_loss_percent']
                    value=None if a is None or b is None else bool(a<=b)
                    values.append(value);pairs.append(dict(dgp=dgp,phi_index=pi,window=w,horizon=h,QR4_delta=a,QR33_delta=b,outcome=value))
    output['P3']=dict(fraction_screen(values,1.),pairs=pairs,secondary=True)
    output['interpretation']='pooled primary only; contrary method/DGP/P3 outcomes retained; metric excludes p'
    return output
