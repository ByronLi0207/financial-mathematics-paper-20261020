"""Display-only E4 figures from saved aggregate cost receipts."""
from pathlib import Path
import hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parent;P=ROOT/'results/v10/cost'
def main():
    rows=json.loads((P/'group-regions.json').read_text());summary=json.loads((P/'summary.json').read_text());d=json.loads((P/'manifest.json').read_text())['design']
    for f in ['cost-regions.pdf','cost-regions.png','report-values.json','report-note-zh.md']:assert not (P/f).exists()
    tags=list(d['primary_method_by_group']);fig,axs=plt.subplots(3,2,figsize=(7.4,8.2),constrained_layout=True);values=[]
    # The decimal point is retained while dropping the leading zero.
    ticklabel=lambda x: '.'+format(x,'g')[2:] if 0<x<1 else format(x,'g')
    for ax,tag in zip(axs.flat,tags):
        rr=[x for x in rows if x['group_label']==tag and x['c']==d['primary_c']]
        a=np.array([[next(r for r in rr if r['kappa']==k and r['beta']==b)['lower'] for b in d['grid']['beta']] for k in d['grid']['kappa']])
        upper=np.array([[next(r for r in rr if r['kappa']==k and r['beta']==b)['upper'] for b in d['grid']['beta']] for k in d['grid']['kappa']])
        image=ax.imshow(a,vmin=0,vmax=1,origin='lower',aspect='auto',cmap='Blues');ax.set_xticks(range(len(d['grid']['beta'])),[ticklabel(x) for x in d['grid']['beta']],fontsize=8);ax.set_yticks(range(len(d['grid']['kappa'])),[ticklabel(x) for x in d['grid']['kappa']],fontsize=8)
        
        for yi,xi in zip(*np.nonzero(a!=upper)):
            ax.text(xi,yi,f'[{a[yi,xi]:.2f},{upper[yi,xi]:.2f}]',ha='center',va='center',fontsize=5,color='darkred')
        complete=rr[0]['complete'];planned=rr[0]['planned'];ax.set_title(f'{tag}\n{complete}/{planned} complete',fontsize=9,pad=5);ax.set_xlabel(r'Breach charge $\beta=b/m_F$',fontsize=8.5,labelpad=3);ax.set_ylabel(r'Reserve coefficient $\kappa$',fontsize=8.5,labelpad=4)
        values.append(dict(group_label=tag,complete=complete,planned=planned,primary=d['primary_method_by_group'][tag],c=d['primary_c'],minimum_cheaper_fraction=float(a.min()),maximum_cheaper_fraction=float(a.max()),unknown_grid_points=int(np.count_nonzero(a!=upper))))
    cb=fig.colorbar(image,ax=list(axs.flat),shrink=.82,fraction=.035,pad=.035);cb.set_label('Planned-cell fraction lower bound: cheaper than F',fontsize=8.5);cb.ax.tick_params(labelsize=8)
    fig.suptitle('Normalized report costs: full registered grid at c = 1',fontsize=11)
    fig.savefig(P/'cost-regions.pdf');fig.savefig(P/'cost-regions.png',dpi=180);plt.close(fig)
    out=dict(groups=values,summary=summary,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [P/'group-regions.json',P/'summary.json',P/'manifest.json']})
    with (P/'report-values.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    note=['# E4 成本区域：保存结果读出','','完整网格及每个方法成本在 cost-grid.csv.zip；每个固定主比较的全部区域在 primary-regions.csv。图中颜色为计划格严格更便宜比例的下界；若有未知格，对应色块另标[下界,上界]，不是跨市场金额均值或独立样本概率。','','|组|完整/计划|c=1全网格较便宜比例范围|固定比较|','|---|---:|---:|---|']
    for r in values:note.append(f"|{r['group_label']}|{r['complete']}/{r['planned']}|{r['minimum_cheaper_fraction']:.1%}–{r['maximum_cheaper_fraction']:.1%}|{r['primary']}|")
    note+=['','日频只能使用已保存的原窄菜单；其他主图采用六菜单QR33。所有其余方法保留在完整成本表，不按 MCS 或成本选择更有利模型。系数不是从业务账簿估计的；论文在 Limitations 集中说明。','']
    with (P/'report-note-zh.md').open('x') as f:f.write('\n'.join(note))
    print(json.dumps(out))
if __name__=='__main__':main()
