"""Saved-scalar RP displays; no new fitting, forecasts or statistical tests."""
from pathlib import Path
import hashlib,json


def build_report(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from v13_rp import _usable
    out=Path(out);source=out/'rows.json';rows=json.loads(source.read_text());summary=json.loads((out/'summary.json').read_text())
    fig,axes=plt.subplots(1,3,figsize=(6.4,2.25),constrained_layout=True);points=[]
    for ax,(family,title,planned) in zip(axes,[('cftc','CFTC',34),('nyfed','New York Fed',26),('fx','FX',2)]):
        owned=[(i,r) for i,r in enumerate(rows) if (r['family']=='cftc' if family=='cftc' else r['family'] in ('bill','panel') if family=='nyfed' else r['family']=='fx')]
        for x,method,colour,marker,label in [(0,'ordinary','#0072B2','o','Ordinary'),(1,'rp','#D55E00','s','Protected')]:
            valid=[(i,r) for i,r in owned if _usable(r,method)]
            values=[r[method+'_relative_loss_pct'] for _,r in valid]
            if values:
                box=ax.boxplot([values],positions=[x],widths=.45,showfliers=False,patch_artist=True,medianprops={'color':'black','linewidth':1},boxprops={'facecolor':colour,'alpha':.22,'edgecolor':colour},whiskerprops={'color':colour},capprops={'color':colour})
                offsets=np.linspace(-.12,.12,len(valid)) if len(valid)>1 else [0.]
                for jitter,(index,row) in zip(offsets,valid):
                    ax.scatter(x+jitter,row[method+'_relative_loss_pct'],s=11,marker=marker,color=colour,alpha=.8,zorder=3)
            missing=planned-len(valid)
            if missing:ax.scatter([x],[0],marker='x',color='black',s=24,zorder=5)
            for index,row in owned:
                points.append(dict(group=family,method=method,json_row_index=index,cell_id=row['cell_id'],status=row[method+'_status'],relative_loss_pct=row.get(method+'_relative_loss_pct'),route=row.get('route')))
            ax.text(x,.98,f'{len(valid)}/{planned}',transform=ax.get_xaxis_transform(),ha='center',va='top',fontsize=7)
        ax.axhline(0,color='0.4',lw=.7);ax.set_title(title,fontsize=9)
        ax.set_xticks([0,1],['Ordinary','Protected'],fontsize=8);ax.tick_params(axis='y',labelsize=7)
        ax.set_xlim(-.48,1.48);ax.spines[['top','right']].set_visible(False)
    axes[0].set_ylabel('Excess pinball loss (%)',fontsize=8)
    fig.savefig(out/'recommended-protocol-comparison.pdf',bbox_inches='tight');fig.savefig(out/'recommended-protocol-comparison.png',dpi=200,bbox_inches='tight');plt.close(fig)
    with (out/'figure-source-bindings.json').open('x') as f:json.dump(dict(source='results/v13/recommended-protocol/rows.json',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),points=points,caption='Ordinary expanded-menu regression and the benchmark-protected protocol against matched corrected-rank historical limits. Every available cell is shown; counts use the full planned group and crosses mark unavailable cells. This evaluation is retrospective.'),f,indent=2);f.write('\n')
    fmt=lambda x:'NA' if x is None else f'{x:.6f}'
    lines=['# G3: recommended validation protocol','',f"R1 {summary['R1']}; R2 {summary['R2']}; R3 {summary['R3']}.",'','|Group|RP complete/planned|Ordinary median (%)|RP median (%)|Worst RP (%)|RP >10%|F fallback / planned|','|---|---:|---:|---:|---:|---:|---:|']
    for group,x in [('weekly',summary['weekly']),*summary['groups'].items()]:lines.append(f"|{group}|{x['complete']}/{x['planned']}|{fmt(x['ordinary_median_relative_loss_pct'])}|{fmt(x['median_relative_loss_pct'])}|{fmt(x['worst_relative_loss_pct'])}|{x['adverse_gt10_count']}|{x['fallback_count']}/{x['planned']}|")
    lines+=['','|FX period|Ordinary (%)|RP (%)|Half-gain threshold (%)|Route|R3|','|---|---:|---:|---:|---|---|']
    for period,x in summary['FX']['periods'].items():lines.append(f"|{period}|{fmt(x['ordinary_relative_loss_pct'])}|{fmt(x['rp_relative_loss_pct'])}|{fmt(x['half_gain_threshold_pct'])}|{x['route']}|{x['status']}|")
    lines+=['',summary['interpretation'],'','Rows, all candidates, sealed validation selections/gates and references retain all failures. No failure is credited as a successful return toF.']
    with (out/'REPORT.md').open('x') as f:f.write('\n'.join(lines)+'\n')
