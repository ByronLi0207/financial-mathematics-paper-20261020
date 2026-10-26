import csv,json,hashlib,math,tarfile,re,time,resource,signal,os,subprocess,platform,warnings
from pathlib import Path
from fractions import Fraction
from collections import Counter
import numpy as np
import scipy,sklearn
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
start=time.monotonic(); signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('600s audit limit'))); signal.alarm(590)
R=Path.cwd(); O=R/'results/revision-v9/wp1'; design=json.loads((R/'protocol/revision-v9/wp1-posthoc-design.json').read_text()); saved=json.loads((O/'breakeven.json').read_text()); boot=json.loads((O/'bootstrap.json').read_text()); overlays=json.loads((O/'empirical-overlay.json').read_text()); sealed=json.loads((O/'simulation-cells.json').read_text()); maxthreads=0
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sealed_hashes={str(p):hashfile(p) for p in O.glob('*.json')}
def probe():
 global maxthreads
 text=subprocess.check_output(['ps','-M','-p',str(os.getpid())],text=True); maxthreads=max(maxthreads,len(text.strip().splitlines())-1)
 assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<=2147483648
probe()
for x in design['inputs']:assert hashfile(R/x['path'])==x['sha256'] and (R/x['path']).stat().st_size==x['bytes']
readcsv=lambda p:list(csv.DictReader(p.open(newline='')))
index={x['path']:x for x in readcsv(R/'results/revision-v8/wp3/wp3-driver-output-members.csv')}; raw={}; rx=re.compile(r'^units/rep-(\d{3})_phi-(\d)_p-(\d)/W(\d+)_H(\d+)_(F|QR33|QR4)\.json$')
with tarfile.open(R/'results/revision-v8/wp3/wp3-driver-output.tar.gz','r|gz') as t:
 for m in t:
  q=rx.fullmatch(m.name)
  if not q:continue
  b=t.extractfile(m).read(); assert len(b)==int(index[m.name]['size']) and hashlib.sha256(b).hexdigest()==index[m.name]['sha256']; d=json.loads(b); e=d['evaluation']; k=tuple(map(int,q.groups()[:5]))+(q.group(6),); assert k not in raw and d['status']=='COMPLETE'; raw[k]=e
expected={(r,p,v,w,h,m) for r in range(32) for p in range(3) for v in range(3) for w in (52,260,720,2880) for h in (6,24) for m in ('F','QR33','QR4')}; assert set(raw)==expected
cells=[]; sm={tuple(c[k] for k in ('phi_index','volatility_index','window','horizon','method')):c for c in sealed}; summary=[c for c in readcsv(R/'results/revision-v8/wp3/summary.csv') if c['method']!='F']; max_source_abs=0.
close=lambda a,b:math.isclose(float(a),float(b),rel_tol=1e-12,abs_tol=1e-10)
for s in summary:
 p,v,w,h=map(int,(s['phi_index'],s['p_index'],s['window'],s['horizon'])); m=s['method']; k=(p,v,w,h,m); a=np.array([raw[(r,p,v,w,h,m)]['mean_loss'] for r in range(32)]); f=np.array([raw[(r,p,v,w,h,'F')]['mean_loss'] for r in range(32)]); assert all(raw[(r,p,v,w,h,m)]['n']==raw[(r,p,v,w,h,'F')]['n']==72 for r in range(32)); d=float(100*(a.mean()/f.mean()-1)); old=sm[k]; assert np.array_equal(a,old['model_losses']) and np.array_equal(f,old['reference_losses']); assert close(d,old['relative_loss_percent']) and close(d,s['relative_loss_percent']); max_source_abs=max(max_source_abs,abs(d-float(s['relative_loss_percent']))); cells.append((w,h,m,d,a,f))
assert len(cells)==len(sm)==144 and Counter(c[2] for c in cells)=={'QR33':72,'QR4':72}
print('SOURCE reports=6912 selected_cells=144 replicas_per_cell=32 n=72 fingerprint_mismatches=0 paired_loss_mismatches=0 max_archived_delta_abs_difference='+repr(max_source_abs))
pcount={'QR33':34,'QR4':5}
def metric(w,h,m,c):return Fraction(w,pcount[m] if c=='a' else (h+1)*(pcount[m] if c=='b' else 1))
y=np.array([c[3]<0 for c in cells],int); scores={}; max_corr_error=0.
for candidate in ('a','b','c'):
 rr=np.array([float(metric(*c[:3],candidate)) for c in cells]); x=np.log(rr); x=((x-x.mean())/x.std(ddof=0))[:,None]; fit=LogisticRegression(C=1,l1_ratio=0,solver='lbfgs',max_iter=10000,tol=1e-10,fit_intercept=True,class_weight=None,warm_start=False)
 with warnings.catch_warnings():warnings.simplefilter('error',ConvergenceWarning); fit.fit(x,y)
 assert fit.n_iter_.max()<10000; score=int(((fit.decision_function(x)>0).astype(int)==y).sum()); scores[candidate]=score; assert score==saved['candidate_scores'][candidate]['correct']; delta=np.array([c[3] for c in cells])
 for g in ('pooled','QR33','QR4'):
  mask=np.ones(144,bool) if g=='pooled' else np.array([c[2]==g for c in cells]); rho=float(spearmanr(rr[mask],delta[mask]).statistic); err=abs(rho-saved['candidate_scores'][candidate]['spearman'][g]); max_corr_error=max(max_corr_error,err); assert close(rho,saved['candidate_scores'][candidate]['spearman'][g])
 probe()
chosen=next(k for k in ('c','a','b') if scores[k]==max(scores.values())); assert chosen==saved['selected_metric']; print('METRICS correct_out_of_144='+json.dumps(scores,sort_keys=True)+' selected='+chosen+' label_wins='+str(y.sum())+' score_mismatches=0 spearman_mismatches=0 max_spearman_abs_difference='+repr(max_corr_error))
ids=np.asarray(boot['draw_indices']); assert ids.shape==(1999,32) and np.array_equal(ids,np.random.Generator(np.random.PCG64(np.random.SeedSequence(2026102491))).integers(0,32,(1999,32))); assert [hashlib.sha256(np.asarray(i,dtype='<i8').tobytes()).hexdigest() for i in ids]==boot['draw_index_sha256']
def curve(cs,delta):
 groups={}
 for c,d in zip(cs,delta):groups.setdefault(metric(*c[:3],chosen),[]).append(float(d))
 kk=sorted(groups); xx=[float(k) for k in kk]; yy=[math.fsum(groups[k])/len(groups[k]) for k in kk]; roots=[]
 for j in range(len(xx)-1):
  if yy[j]>0 and yy[j+1]<=0:roots.append(float(xx[j]+(xx[j+1]-xx[j])*yy[j]/(yy[j]-yy[j+1])))
 status='UNIDENTIFIED_LEFT_CENSORED' if yy[0]<=0 else ('IDENTIFIED' if roots else 'UNIDENTIFIED_NO_CROSSING'); return dict(status=status,r_star=roots[0] if status=='IDENTIFIED' else None,crossings=roots,multiple_crossings=len(roots)>1,x=xx,y=yy)
def compare(a,b):
 if isinstance(a,dict):assert set(a)==set(b); return all(compare(a[k],b[k]) for k in a)
 if isinstance(a,list):assert len(a)==len(b);return all(compare(x,y) for x,y in zip(a,b))
 if a is None or isinstance(a,(bool,str)):assert a==b;return True
 assert close(a,b);return True
def order(v,q):v=sorted(v);return float(v[math.ceil(q*len(v))-1])
for method in ('QR33','QR4'):
 cs=[c for c in cells if c[2]==method]; a=np.stack([c[4] for c in cs]); f=np.stack([c[5] for c in cs]); point=curve(cs,[c[3] for c in cs]); old=boot['methods'][method]; compare(point,old['point']); roots=[]; statuses=Counter(); multiple=0; max_curve_diff=0.
 for j,i in enumerate(ids):
  d=100*(a[:,i].mean(axis=1)/f[:,i].mean(axis=1)-1); got=curve(cs,d); compare(got,old['draws'][j]); roots.append(got['r_star']);statuses[got['status']]+=1;multiple+=got['multiple_crossings']; max_curve_diff=max(max_curve_diff,max(abs(x-y) for x,y in zip(got['y'],old['draws'][j]['y'])))
 finite=[r for r in roots if r is not None]; lower=order([0. if r is None else r for r in roots],.05); upper=order([math.inf if r is None else r for r in roots],.95); intervals=old['intervals']; assert intervals['draw_count']==1999 and intervals['finite_count']==len(finite) and intervals['missing_count']==1999-len(finite); assert close(intervals['finite_only']['lower'],order(finite,.05)) and close(intervals['finite_only']['upper'],order(finite,.95)); assert intervals['all_draw_envelope']['lower']==lower and intervals['all_draw_envelope']['upper_unbounded']==(not math.isfinite(upper)) and intervals['all_draw_envelope']['upper']==(upper if math.isfinite(upper) else None); assert dict(statuses)==old['status_counts'] and multiple==old['multiple_crossing_draws']; compare({k:v for k,v in old.items() if k!='draws'},saved['methods'][method]); print('BOOTSTRAP method='+method+' draws=1999 point='+repr(point['r_star'])+' finite='+str(len(finite))+' statuses='+json.dumps(dict(statuses),sort_keys=True)+' envelope='+json.dumps(intervals['all_draw_envelope'],sort_keys=True)+' mismatches=0 max_curve_y_abs_difference='+repr(max_curve_diff));probe()
orig=readcsv(R/'results/revision-20261022/evaluation-summary.csv'); panel=readcsv(R/'results/revision-20261023/round2/panel/summary.csv'); expected_overlay=[]
def add(path,line,row,reference,source,method):
 assert len(reference)==1; ref=reference[0]; assert row.get('status','COMPLETE')==ref.get('status','COMPLETE')=='COMPLETE'; n=int(row['origin_count']); assert n==int(ref['origin_count']); a=float(row['mean_pinball']); f=float(ref['mean_pinball']); assert f>0; expected_overlay.append((path,line,source,method,int(row['window']),int(row['horizon']),n,a,f,100*(a/f-1)))
p='results/revision-20261022/evaluation-summary.csv'
for line,s in enumerate(orig,2):
 if s['method']=='QR':add(p,line,s,[r for r in orig if r['method']=='frozen_F' and all(r[k]==s[k] for k in ('source','window','horizon','refit_step'))],s['source'],'QR33')
p='results/revision-20261023/parsimonious/summary.csv'
for line,s in enumerate(readcsv(R/p),2):add(p,line,s,[r for r in orig if r['method']=='frozen_F' and all(r[k]==s[k] for k in ('source','window','horizon')) and int(r['refit_step'])=={'fx_hourly':24,'nyfed_weekly':13}[s['source']]],s['source'],'QR4')
p='results/revision-v8/wp4/contrasts.csv'
for line,s in enumerate(readcsv(R/p),2):
 assert s['reference_method']=='F'; row=dict(status=s['status'],origin_count=s['n'],mean_pinball=s['model_loss'],window=s['window'],horizon=s['horizon']); add(p,line,row,[dict(status='COMPLETE',origin_count=s['n'],mean_pinball=s['reference_loss'])],'fx_daily',s['method'])
p='results/revision-20261023/round2/panel/summary.csv'
for line,s in enumerate(panel,2):
 if s['method'] in ('QR33','C2_QR4'):add(p,line,s,[r for r in panel if r['method']=='frozen_F' and all(r[k]==s[k] for k in ('series_key','window','horizon'))],'panel:'+s['series_key'],{'QR33':'QR33','C2_QR4':'QR4'}[s['method']])
assert len(expected_overlay)==len(overlays)==120; lookup={(x['source_file'],x['source_row']):x for x in overlays};assert len(lookup)==120
for path,line,source,method,w,h,n,a,f,d in expected_overlay:
 x=lookup[(path,line)]; assert x['source']==source and x['method']==method and x['window']==w and x['horizon']==h and x['n']==n and x['status']=='COMPLETE';assert close(x['model_loss'],a) and close(x['reference_loss'],f) and close(x['relative_loss_percent'],d) and close(x['metric'],float(metric(w,h,method,chosen)))
assert Counter(x[0] for x in expected_overlay)=={'results/revision-20261022/evaluation-summary.csv':8,'results/revision-20261023/parsimonious/summary.csv':8,'results/revision-v8/wp4/contrasts.csv':8,'results/revision-20261023/round2/panel/summary.csv':96};print('OVERLAY census=120 sources=8/8/8/96 unique_locators=120 source_pair_mismatches=0 metric_mismatches=0 status_COMPLETE=120')
assert all(hashfile(Path(p))==h for p,h in sealed_hashes.items());probe();elapsed=time.monotonic()-start;assert elapsed<600;print('RESOURCE '+json.dumps(dict(elapsed_seconds=elapsed,process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,maximum_observed_process_os_threads=maxthreads,numeric_workers=1,numerical_threads_configured=1,versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,scikit_learn=sklearn.__version__)),sort_keys=True));print('PASS independent_wp1_readback imported_v9_posthoc=False original_results_written=False original_outputs_unchanged=True')
