"""Format already archived history records; never imports a forecasting/statistics driver."""
from pathlib import Path
import json,hashlib,os
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v11';DOC=ROOT/'submission-v10';BASE=ROOT/'evidence/v11/pr5-v9'
os.environ['MPLCONFIGDIR']=str(ROOT/'.scratch/v11/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
source='results/revision-v9/wp3/contrasts.json';path=BASE/source;rows=json.loads(path.read_text());digest=hashlib.sha256(path.read_bytes()).hexdigest();bindings=[]
fig,ax=plt.subplots(figsize=(6.25,2.3));fig.subplots_adjust(left=.12,right=.98,top=.82,bottom=.25)
for method,label,color,marker in [('QR33','Full regression','#0072B2','o'),('QR4','Four-feature','#CC79A7','D')]:
 chosen=sorted([(i,r)for i,r in enumerate(rows)if r['horizon']==6 and r['method']==method],key=lambda x:x[1]['window']);assert len(chosen)==5
 x=[r['window']for _,r in chosen];y=[r['relative_loss_percent']for _,r in chosen];assert all(r['status']=='COMPLETE'for _,r in chosen)
 ax.plot(x,y,color=color,marker=marker,ms=5,lw=1.5,label=label)
 for i,r in chosen:
  for k in ['window','horizon','relative_loss_percent','n']:
   bindings.append({'destination':'main learning-curve plot','source_commit':'60e03b8ae7a950c96ace3987f0625b3e434e6887','source_path':source,'imported_path':str(path.relative_to(ROOT)),'sha256':digest,'json_pointer':f'/{i}/{k}','value':r[k]})
ax.set_xscale('log',base=2);ax.set_xticks([r['window']for _,r in chosen],[str(r['window'])for _,r in chosen]);ax.axhline(0,color='#222222',ls='--',lw=.8);ax.grid(axis='y',color='.86',lw=.5);ax.set_xlabel('Training history (completed hourly labels)',fontsize=9);ax.set_ylabel('Relative loss change (%)',fontsize=9);ax.tick_params(labelsize=9);ax.spines[['top','right']].set_visible(False);fig.legend(loc='upper center',bbox_to_anchor=(.56,1.03),ncol=2,frameon=False,fontsize=9)
(DOC/'figures').mkdir(exist_ok=True)
fig.savefig(DOC/'figures/v11-fx-history.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(ROOT/'.scratch/v11/fx-history.png',dpi=220);plt.close(fig)
# Display the prewritten pooled criteria exactly; no support calculation is performed.
source2='results/revision-v9/wp2/support.json';sp=BASE/source2;support=json.loads(sp.read_text());sd=hashlib.sha256(sp.read_bytes()).hexdigest()
labels={'P1':'Positive excess loss in the low-history region','P2':'Negative excess loss in the high-history region','P3':'Four-feature loss never exceeds full-regression loss'}
lines=[r'\begin{table}[htbp]\centering\small',r'\caption{Saved confirmation criteria for excess loss relative to matched historical headroom under additional synthetic innovation laws. Counts use the original fixed pooled denominators, including all counterexamples.}\label{tab:v11-confirmation}',r'\begin{tabular}{p{7.2cm}rrrr}\toprule',r'Prewritten criterion & Successes & Missing & Required & Result \\ \midrule']
for k in ['P1','P2','P3']:
 r=support[k];status='Supported'if r['status']=='SUPPORT'else'Not supported';lines.append(labels[k]+' & '+f"{r['successes']}/{r['denominator']} & {r['missing']} & {r['minimum_fraction']:.0%}".replace('%',r'\%')+' & '+status+r' \\')
 for f in ['successes','denominator','missing','minimum_fraction','status']:
  bindings.append({'destination':'Supplement confirmation table','source_commit':'60e03b8ae7a950c96ace3987f0625b3e434e6887','source_path':source2,'imported_path':str(sp.relative_to(ROOT)),'sha256':sd,'json_pointer':f'/{k}/{f}','value':r[f]})
lines +=[r'\bottomrule\end{tabular}',r'\par\smallskip\begin{minipage}{.98\linewidth}\footnotesize',r'History regions use the method-specific thresholds fixed in the linked original design, conditional on the earlier threshold exercise; the history index excludes predictor dimension.',r'Full and four-feature regressions retain different original penalty menus, so their ordering does not isolate predictor dimension.',r'The universal ordering prediction is not supported; the complete records retain all counterexamples and candidate failures.',r'\end{minipage}\end{table}','']
(DOC/'generated/v11-confirmation.tex').write_text('\n'.join(lines))
# Explicit bindings also cover the prose's negative/turning-point values and sample structure.
for i in [0,4,8,12,16,18,19]:
 for k in ['window','horizon','relative_loss_percent']:
  bindings.append({'destination':'history paragraph / full-contrast availability','source_commit':'60e03b8ae7a950c96ace3987f0625b3e434e6887','source_path':source,'imported_path':str(path.relative_to(ROOT)),'sha256':digest,'json_pointer':f'/{i}/{k}','value':rows[i][k]})
(HERE/'imported-number-bindings.json').write_text(json.dumps({'scope':'Direct saved fields only; formatting and plotting are not new estimates. Zero WP4 points imported.','bindings':bindings,'source_input_sha256':{source:digest,source2:sd},'figure_sha256':hashlib.sha256((DOC/'figures/v11-fx-history.pdf').read_bytes()).hexdigest()},indent=2)+'\n')
print('curve10points, table3criteria, bindings',len(bindings))
