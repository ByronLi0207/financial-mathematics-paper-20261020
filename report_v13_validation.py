"""Display only saved G2 and original F2 scalar outcomes, without new models."""
from pathlib import Path
import hashlib,json


def build_report(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from v13_validation import NYFED_KEYS
    from v12_decomposition import CFTC_SOURCE_KEYS
    out=Path(out);root=Path(__file__).resolve().parent
    current=out/'rows.json';original=root/'results/v12/validation-length/rows.json'
    new=json.loads(current.read_text());old=json.loads(original.read_text())
    fig,axes=plt.subplots(2,2,figsize=(10.4,5.6),sharey=False,constrained_layout=True)
    points=[]
    for ax,(source,rows,keys,h,w,title) in zip(axes.flat,[('v13',new,NYFED_KEYS,6,52,'New York Fed: horizon 6, history 52 weeks'),('v12',old,CFTC_SOURCE_KEYS,6,52,'CFTC: horizon 6, history 52 weeks'),('v13',new,NYFED_KEYS,24,52,'New York Fed: horizon 24, history 52 weeks'),('v12',old,CFTC_SOURCE_KEYS,6,260,'CFTC: horizon 6, history 260 weeks')]):
        for vi,(v,offset,colour,marker) in enumerate([(52,-.12,'#0072B2','o'),(156,.12,'#D55E00','s')]):
            for j,key in enumerate(keys):
                hits=[r for r in rows if r.get('source_key')==key and r.get('method')=='QR33' and r.get('horizon')==h and r.get('window')==w and r.get('validation_n')==v]
                row=hits[0] if len(hits)==1 else None
                complete=row is not None and row.get('status')=='COMPLETE' and row.get('relative_loss_pct') is not None
                points.append(dict(source=source,source_key=key,horizon=h,window=w,validation_n=v,status=row.get('status') if row else 'MISSING_OR_DUPLICATE',relative_loss_pct=row.get('relative_loss_pct') if row else None,source_file=str(current.relative_to(root)) if source=='v13' else str(original.relative_to(root)),json_row_index=rows.index(row) if row else None))
                if complete:ax.plot(j+offset,row['relative_loss_pct'],marker=marker,color=colour,linestyle='none',markersize=4.2)
                else:ax.plot(j+offset,0,marker='x',color=colour,linestyle='none',markersize=6)
        ax.axhline(0,color='0.35',lw=.8);ax.set_title(title,fontsize=9)
        ax.set_xticks(range(len(keys)),[key.replace('PDPOS','').replace('PDPOSTIPS','TIPS') for key in keys],rotation=65,ha='right',fontsize=7)
        ax.set_xlabel('Series / contract',fontsize=8);ax.set_ylabel('Regression excess pinball loss (%)',fontsize=8)
        ax.tick_params(axis='y',labelsize=8);ax.spines[['top','right']].set_visible(False)
    fig.legend(handles=[Line2D([0],[0],marker='o',color='#0072B2',linestyle='none',label='52 validation observations'),Line2D([0],[0],marker='s',color='#D55E00',linestyle='none',label='156 validation observations')],loc='outside upper center',ncol=2,frameon=False,fontsize=9)
    fig.savefig(out/'validation-length-comparison.pdf',bbox_inches='tight');fig.savefig(out/'validation-length-comparison.png',dpi=180,bbox_inches='tight');plt.close(fig)
    binding=dict(sources={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (current,original)},points=points,caption='Matched regression excess loss against corrected-rank historical limits for every planned series. NY Fed horizon6 also moves the long-validation endpoint18weeks; CFTC outcomes are unchanged v12 results. Crosses atzero mark unavailable cells rather than a zero loss.')
    with (out/'figure-source-bindings.json').open('x') as f:json.dump(binding,f,indent=2);f.write('\n')
    summary=json.loads((out/'summary.json').read_text())
    lines=['# G2: NY Fed validation-length replication','',f"Primary V3: {summary['V3']}; V4: {summary['V4']}.",'','|Method|H|Complete pairs /13|Median V52 (%)|Median V156 (%)|Difference (pp)|Infinity V52→V156|V3|V4|','|---|---:|---:|---:|---:|---:|---|---|---|']
    fmt=lambda x:'NA' if x is None else f'{x:.6f}'
    for method in ('QR33','QR4'):
        for h in ('6','24'):
            x=summary['methods'][method]['by_horizon'][h];m=x['median_relative_loss_by_validation'];c=x['infinity_count_by_validation']
            lines.append(f"|{method}|{h}|{x['complete_pair_count']}/13|{fmt(m['52'])}|{fmt(m['156'])}|{fmt(x['median_difference_pct_points'])}|{c['52']}→{c['156']}|{x['V3']}|{x['V4']}|")
    lines+=['',summary['interpretation'],'','All method cells, failures and candidate provenance remain in rows.json/candidates.json. No successful subset replaces a full denominator.']
    with (out/'REPORT.md').open('x') as f:f.write('\n'.join(lines)+'\n')
