"""Read-only arithmetic audit of frozen v3 scalar tables, not raw-data inference.

Independently written direct LR/G-test/step-down formulae. This checks stored
scalar relations only; it does not reconstruct losses, HAC, hit order or DQ
matrices and cannot validate asymptotic references or external validity.
"""
import sys
sys.dont_write_bytecode=True
import csv,hashlib,json,math
from collections import Counter
from pathlib import Path

def main():
    base=Path(__file__).resolve().parent/'results/revision-20261023/inference'
    fingerprints={}
    def read(name):
        raw=(base/name).read_bytes();fingerprints[name]=hashlib.sha256(raw).hexdigest()
        return list(csv.DictReader(raw.decode('utf8').splitlines()))
    dm,cv,ho=map(read,('dm.csv','coverage.csv','holm.csv'))
    maximum={};counts=Counter();bad=[]
    def compare(label,actual,expected,key):
        actual=float(actual);error=abs(actual-expected);counts[label]+=1
        if not math.isfinite(actual) or not math.isfinite(expected) or error>1e-9:bad.append(dict(label=label,id=key,actual=actual,expected=expected))
        maximum[label]=max(maximum.get(label,0.),error)
    def flag(ok,label,key):
        if not ok:bad.append(dict(label=label,id=key))
    for r in dm:
        key=r['contrast_id'];n=int(r['n']);h=int(r['horizon']);variance=float(r['lrv']);mean=float(r['mean_difference'])
        L=max(h,int(4*(n/100)**(2/9)));flag(int(r['bandwidth'])==L and int(r['double_bandwidth'])==2*L,'bandwidth',key)
        if r['status']=='OK':
            t=mean/math.sqrt(variance/n);factor=math.sqrt((n+1-2*h+h*(h-1)/n)/n)
            compare('dm_t',r['dm_t'],t,key);compare('hln_t',r['hln_t'],t*factor,key)
            compare('dm_p',r['dm_p'],math.erfc(abs(t)/math.sqrt(2)),key)
            compare('double_dm_p_from_stored_t',r['double_dm_p'],math.erfc(abs(float(r['double_dm_t']))/math.sqrt(2)),key)
        else:
            flag(r['status']=='IDENTICAL_LOSSES' and mean==variance==0 and all(r[c]=='' for c in ['dm_t','dm_p','hln_t','hln_p','double_dm_t','double_dm_p','double_hln_p']),'DM_NA',key)
    def xlogratio(count,numerator,denominator):return 0. if count==0 else count*math.log(numerator/denominator)
    for r in cv:
        key='-'.join(r[k] for k in ['source','horizon','window','method']);n=int(r['n']);k=int(r['hits']);ns=[int(r[x]) for x in ['n00','n01','n10','n11']];a,b,c,d=ns;m=sum(ns)
        uc=max(0.,2*(xlogratio(k,k,n*.05)+xlogratio(n-k,n-k,n*.95)))
        compare('rate',r['rate'],k/n,key);compare('pof_lr',r['pof_lr'],uc,key);compare('pof_p',r['pof_p'],math.erfc(math.sqrt(uc/2)),key)
        flag(m==n-1 and all(x>=0 for x in ns) and k-(b+d) in [0,1] and k-(c+d) in [0,1],'transition_counts',key)
        boundary=any(x==0 for x in ns);flag((r['boundary']=='True')==boundary,'boundary',key)
        if a+b>0 and c+d>0:
            rows=[a+b,c+d];cols=[a+c,b+d]
            ind=max(0.,2*sum(xlogratio(ns[2*i+j],ns[2*i+j]*m,rows[i]*cols[j]) for i in [0,1] for j in [0,1]))
            compare('ind_lr',r['ind_lr'],ind,key);compare('ind_p',r['ind_p'],math.erfc(math.sqrt(ind/2)),key)
            compare('cc_lr',r['cc_lr'],uc+ind,key);compare('cc_p',r['cc_p'],math.exp(-(uc+ind)/2),key)
            flag(r['ind_status']==('BOUNDARY_REFERENCE' if boundary else 'OK'),'ind_status',key)
        else:flag(r['ind_status']=='UNIDENTIFIED_TRANSITION_ROW' and all(r[x]=='' for x in ['ind_lr','ind_p','cc_lr','cc_p']),'ind_NA',key)
        flag(int(r['grid_stride'])==int(r['horizon'])+1,'grid_stride',key)
        if r['dq_status']=='OK' and int(r['dq_df'])==6:
            x=float(r['dq_stat'])/2;compare('dq_tail_from_stored_stat_only',r['dq_p'],math.exp(-x)*(1+x+x*x/2),key)
        else:bad.append(dict(label='unexpected_DQ_scalar_scope',id=key))
    common={r['contrast_id']:r for r in dm if r['category']=='common_history'};hids={r['contrast_id'] for r in ho}
    flag(len(common)==len(ho)==len(hids)==72 and set(common)==hids,'fixed_family','all')
    for r in ho:
        key=r['contrast_id'];original=common[key];flag(all(r[k]==original[k] for k in original),'retained_columns',key)
        p=1. if r['status']=='IDENTICAL_LOSSES' else float(r['dm_p']);compare('holm_input',r['holm_input_p'],p,key);flag(r['holm_family_size']=='72','family_size',key)
    running=0.
    for j,r in enumerate(sorted(ho,key=lambda x:float(x['holm_input_p']))):
        running=min(1.,max(running,(72-j)*float(r['holm_input_p'])));compare('holm_p',r['holm_p'],running,r['contrast_id'])
    rejected=[r for r in ho if float(r['holm_p'])<.05]
    directional={label:sorted(r['contrast_id'] for r in rejected if (float(r['mean_difference'])<0 if label=='favorable' else float(r['mean_difference'])>0)) for label in ['favorable','adverse']}
    result=dict(status='SCALAR_ARITHMETIC_AGREES' if not bad else 'MISMATCH',input_sha256=fingerprints,row_counts=dict(dm=len(dm),coverage=len(cv),holm=len(ho)),status_counts=dict(dm=dict(Counter(r['status'] for r in dm)),coverage=dict(Counter(r['ind_status'] for r in cv))),checked_scalar_counts=dict(counts),max_absolute_errors=maximum,absolute_tolerance=1e-9,mismatch_count=len(bad),mismatches=bad,holm_direction_counts={k:len(v) for k,v in directional.items()},holm_direction_ids=directional,not_verified=['raw loss pairing or source observations','HAC/LRV construction','double t from unavailable double LRV','raw hit order or actual grid first origin','DQ instruments, covariance, rank or Wald statistic','asymptotic distribution calibration or external validity'])
    print(json.dumps(result,indent=2));return int(bool(bad))

if __name__=='__main__':raise SystemExit(main())
