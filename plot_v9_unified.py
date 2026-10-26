"""Saved-result display only: all conditional ordinates and source identities retained."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import csv,hashlib,json,math,time,resource,datetime,os,subprocess,argparse
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/revision-v9/wp4'
SOURCES=('results/revision-v9/wp1/simulation-cells.json','results/revision-v9/wp2/summary.json','results/revision-v9/wp1/empirical-overlay.json','results/revision-v9/wp3/contrasts.json')
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def category(family,source):
 if family=='v8_sim':return 'v8 simulation'
 if family=='v9_sim':return 'v9 simulation'
 if family=='curve':return 'FX curve'
 if source=='fx_hourly':return 'Hourly FX (old)'
 if source=='fx_daily':return 'Daily FX'
 if source=='nyfed_weekly':return 'Treasury'
 if source.startswith('panel:'):return '12 panel series'
 raise ValueError('unknown source '+source)
def build_points():
 points=[];excluded=[];bindings=[]
 for filename,family in zip(SOURCES,('v8_sim','v9_sim','empirical','curve')):
  path=ROOT/filename;rows=read(path);sha=digest(path);bindings.append(dict(path=filename,sha256=sha,bytes=path.stat().st_size,source_rows=len(rows)))
  for index,row in enumerate(rows):
   if row['method']=='F':excluded.append(dict(source_file=filename,source_index=index,method='F',reason='reference self-comparison, not a conditional-model point'));continue
   assert row['method'] in ('QR33','QR4')
   y_field='full_procedure_relative_loss_percent' if family=='v9_sim' else 'relative_loss_percent'
   value=row[y_field];assert value is not None and math.isfinite(value)
   w,h=row['window'],row['horizon'];metric=Fraction(w,h+1)
   source=row.get('source',row.get('dgp','v8_AR_GARCH' if family=='v8_sim' else 'fx_hourly'))
   point=dict(point_id=family+':'+str(index),family=family,source=source,method=row['method'],window=w,horizon=h,c_fraction=str(metric),c=float(metric),relative_loss_percent=value,source_file=filename,source_index=index,source_sha256=sha,status=row.get('status',row.get('full_procedure_status','COMPLETE')),category=category(family,source),nominal_coefficients=34 if row['method']=='QR33' else 5,underlying_source_file=row.get('source_file'),underlying_source_row=row.get('source_row'),dgp=row.get('dgp'),phi=row.get('phi'),variance_persistence=row.get('variance_persistence'),overlapping_old_FX_cell=family=='curve' and w in (720,2880),same_period_key=('fx_hourly:'+str(h)+':'+str(w)+':'+row['method']) if source=='fx_hourly' and w in (720,2880) else None)
   points.append(point)
   point['source_y_field']=y_field
 assert len({p['point_id'] for p in points})==len(points)
 return points,excluded,bindings

def main():
 global OUT
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=OUT);args=parser.parse_args();OUT=args.output.resolve()
 assert OUT.is_relative_to(ROOT/'results/revision-v9/wp4')
 began=time.monotonic();OUT.mkdir(parents=True,exist_ok=False)
 thread_samples=[len(subprocess.check_output(['ps','-M','-p',str(os.getpid())],text=True).strip().splitlines())-1]
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.lines import Line2D
 from matplotlib.patches import Patch
 points,excluded,bindings=build_points();breakinfo=read(ROOT/'results/revision-v9/wp1/breakeven.json')
 assert breakinfo['selected_metric']=='c' and breakinfo['definition']=='W/(H+1)'
 save(OUT/'points.json',points);save(OUT/'excluded-reference-rows.json',excluded)
 with (OUT/'points.csv').open('x',newline='') as f:
  writer=csv.DictWriter(f,points[0].keys());writer.writeheader();writer.writerows(points)
 styles={'v8 simulation':('x','#72a4b0',.48,13),'v9 simulation':('+','#d6a55b',.52,18),'Hourly FX (old)':('o','#142836',.95,27),'Daily FX':('^','#563c2e',.95,28),'Treasury':('s','#193f6a',.95,25),'12 panel series':('D','#285b45',.68,17)}
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
 fig,axes=plt.subplots(2,2,figsize=(6.6,6.4),sharex=True,gridspec_kw={'height_ratios':[1,1.15]})
 fig.subplots_adjust(left=.105,right=.98,top=.885,bottom=.285,hspace=.31,wspace=.19)
 ymin=min(p['relative_loss_percent'] for p in points)-9;ymax=max(p['relative_loss_percent'] for p in points)*1.06
 render=[]
 for col,method in enumerate(('QR33','QR4')):
  subset=[p for p in points if p['method']==method];m=breakinfo['methods'][method];band=m['intervals']['all_draw_envelope'];assert not band['upper_unbounded']
  for row in (0,1):
   ax=axes[row,col];ax.set_xscale('log');ax.set_xlim(1.6,1000);ax.set_ylim((ymin,ymax) if row==0 else (-30,60));ax.axvspan(band['lower'],band['upper'],color='#c5cad6',alpha=.35,zorder=0);ax.axvline(m['point']['r_star'],color='#6f7180',lw=.8,ls='--',zorder=1);ax.axhline(0,color='#393939',lw=.8,zorder=1)
   artists=[]
   for label,(marker,color,alpha,size) in styles.items():
    group=[p for p in subset if p['category']==label]
    opts=dict(marker=marker,s=size,alpha=alpha,linewidths=.75,zorder=3 if label not in ('v8 simulation','v9 simulation') else 2)
    if label=='Hourly FX (old)':opts.update(facecolors='none',edgecolors=color)
    else:opts.update(c=color)
    art=ax.scatter([p['c'] for p in group],[p['relative_loss_percent'] for p in group],**opts)
    artists.append(dict(category=label,kind='scatter',marker=marker,point_ids=[p['point_id'] for p in group],actual_offsets=art.get_offsets().tolist()))
   for h,marker,color in ((6,'o','#67214a'),(24,'v','#1e2025')):
    group=sorted([p for p in subset if p['family']=='curve' and p['horizon']==h],key=lambda p:p['window'])
    art=ax.plot([p['c'] for p in group],[p['relative_loss_percent'] for p in group],marker=marker,ms=3.4,color=color,lw=.95,zorder=4)[0]
    artists.append(dict(category='FX curve H'+str(h),kind='line',marker=marker,point_ids=[p['point_id'] for p in group],actual_offsets=[[float(x),float(y)] for x,y in zip(art.get_xdata(),art.get_ydata())]))
   display_method='Original regression' if method=='QR33' else 'Four-predictor regression'
   ax.set_title(display_method+'\nComplete range' if row==0 else 'Detail: −30% to 60%',fontsize=9,pad=5)
   ax.grid(axis='x',alpha=.12);ax.tick_params(labelsize=8)
   if row==1:ax.set_xlabel('c = W/(H+1), logarithmic scale',fontsize=8.5);ax.set_xticks([2,10,30,100,400]);ax.set_xticklabels(['2','10','30','100','400'])
   if col==0:ax.set_ylabel('Relative quantile loss (%)',fontsize=8.5)
   render.append(dict(panel=method+('_all' if row==0 else '_detail'),point_ids=[p['point_id'] for p in subset],visible_point_ids=[p['point_id'] for p in subset if ax.get_ylim()[0]<=p['relative_loss_percent']<=ax.get_ylim()[1]],xlim=list(ax.get_xlim()),ylim=list(ax.get_ylim()),full_range=row==0,artists=artists))
 legend_names={'v8 simulation':'Discovery simulation','v9 simulation':'Confirmation simulation'}
 handles=[Line2D([],[],marker=v[0],color=v[1],ls='',markersize=5,label=legend_names.get(k,k),markerfacecolor='none' if k=='Hourly FX (old)' else v[1]) for k,v in styles.items()]
 handles.extend([Line2D([],[],marker='o',color='#67214a',lw=.9,ms=4,label='FX curve H6'),Line2D([],[],marker='v',color='#1e2025',lw=.9,ms=4,label='FX curve H24'),Patch(facecolor='#c5cad6',alpha=.5,label='Post-hoc 90% envelope')])
 fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.065),ncol=3,frameon=False,fontsize=7.5,columnspacing=1.2,handlelength=1.3)
 fig.suptitle('History relative to horizon: a partly supported pattern',fontsize=10.2,y=.987)
 fig.text(.105,.019,f"All {len(points)} records shown. {sum(p['overlapping_old_FX_cell'] for p in points)} FX cells repeat the old period; no independent sample added.\nc excludes parameter count. Lower panels repeat the same data in a labelled detail range.",fontsize=7.1,color='#3b3b3b')
 fig.savefig(OUT/'unified-history.pdf',metadata={'Title':'History relative to horizon: a partly supported pattern','Author':'','CreationDate':None,'ModDate':None});fig.savefig(OUT/'unified-history.png',dpi=240);plt.close(fig)
 receipt=dict(status='GENERATED_PENDING_INDEPENDENT_READBACK_VISUAL_QA',actual_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),metric='c=W/(H+1)',x_scale='log',parameter_count_in_metric=False,source_bindings=bindings,point_count=len(points),family_counts=dict(Counter(p['family'] for p in points)),method_counts=dict(Counter(p['method'] for p in points)),source_counts=dict(Counter(p['source'] for p in points)),excluded_F_reference_self_rows=len(excluded),overlapping_old_FX_curve_records=sum(p['overlapping_old_FX_cell'] for p in points),deduplicated_records=0,jittered_records=0,rounded_ordinates=0,panels=render,band_source='results/revision-v9/wp1/breakeven.json',band_source_sha256=digest(ROOT/'results/revision-v9/wp1/breakeven.json'),bands={k:breakinfo['methods'][k]['intervals']['all_draw_envelope'] for k in ('QR33','QR4')},output_sha256={n:digest(OUT/n) for n in ('points.json','points.csv','excluded-reference-rows.json','unified-history.pdf','unified-history.png')},elapsed_seconds=time.monotonic()-began,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_model_fits=0,new_predictions=0)
 thread_samples.append(len(subprocess.check_output(['ps','-M','-p',str(os.getpid())],text=True).strip().splitlines())-1)
 receipt.update(observed_os_thread_samples=thread_samples,maximum_observed_os_threads=max(thread_samples),requested_numerical_threads=1)
 assert receipt['maximum_observed_os_threads']<=2 and receipt['peak_rss_bytes']<=2147483648 and receipt['elapsed_seconds']<=600
 save(OUT/'render-receipt.json',receipt)
 print(json.dumps({k:v for k,v in receipt.items() if k not in ('panels','output_sha256')},indent=2))
if __name__=='__main__':main()
