"""Two final saved-result figures, with source pointers and actual artists."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse
import csv
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent


def read(name):return json.loads((ROOT/name).read_text())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,data):
    with Path(path).open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')


def points():
    old=read('results/revision-v9/wp4/render-v5/points.json')
    result=[dict(p,code=None,provenance_phase='INHERITED_A') for p in old]
    name='results/final-merge/wp2-cftc-mechanism/summary.json';source=read(name)
    for i,row in enumerate(source['comparisons']):
        if row['status']!='COMPLETE' or row['relative_loss_percent'] is None:
            raise ValueError('CFTC_POINT_UNAVAILABLE_NO_SILENT_DELETION')
        w,h=row['window'],row['horizon'];c=Fraction(w,h+1)
        result.append(dict(point_id=f'cftc:{i}',family='cftc',source='CFTC:'+row['code'],
            method=row['method'],window=w,horizon=h,c_fraction=str(c),c=float(c),
            relative_loss_percent=row['relative_loss_percent'],source_file=name,
            source_index=i,source_y_field='relative_loss_percent',source_sha256=sha(ROOT/name),
            source_json_pointer=f'/comparisons/{i}/relative_loss_percent',status=row['status'],
            category='CFTC',nominal_coefficients=34 if row['method']=='QR33' else 5,
            code=row['code'],provenance_phase='NEW_W520' if w==520 else 'ARCHIVED_W52_W260',
            overlapping_old_FX_cell=False,same_period_key=None))
    if len(result)!=482 or len({r['point_id'] for r in result})!=482:
        raise ValueError('POINT_CENSUS_MISMATCH')
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'results/final-merge/wp3-figures');a=parser.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch,FancyBboxPatch,FancyArrowPatch
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.spines.top':False,
        'axes.spines.right':False,'pdf.fonttype':42,'ps.fonttype':42})
    data=points();save(out/'points.json',data)
    fields=sorted({k for r in data for k in r})
    with (out/'points.csv').open('x',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(data)
    roots=read('notes/revision-v9/wp1-breakeven.json')
    styles={'v8 simulation':('x','#72a4b0',.45,12),'v9 simulation':('+','#d6a55b',.5,17),
        'Hourly FX (old)':('o','#142836',.95,26),'Daily FX':('^','#563c2e',.95,27),
        'Treasury':('s','#193f6a',.95,24),'12 panel series':('D','#285b45',.6,17),
        'CFTC':('p','#a23b75',.83,25)}
    fig,axes=plt.subplots(2,2,figsize=(6.6,7.2),sharex=True,gridspec_kw={'height_ratios':[1,1.15]})
    fig.subplots_adjust(left=.105,right=.98,top=.895,bottom=.30,hspace=.33,wspace=.19)
    lo=min(p['relative_loss_percent'] for p in data)-9;hi=max(p['relative_loss_percent'] for p in data)*1.06
    panels=[]
    for col,method in enumerate(('QR33','QR4')):
        subset=[p for p in data if p['method']==method];m=roots['methods'][method];band=m['intervals']['all_draw_envelope']
        for row in (0,1):
            ax=axes[row,col];ax.set_xscale('log');ax.set_xlim(1.6,1000)
            ax.set_ylim((lo,hi) if row==0 else (-45,65));ax.axvspan(band['lower'],band['upper'],color='#c5cad6',alpha=.35,zorder=0)
            ax.axvline(m['point']['r_star'],color='#6f7180',lw=.8,ls='--',zorder=1);ax.axhline(0,color='#393939',lw=.8,zorder=1)
            artists=[]
            for name,(marker,color,alpha,size) in styles.items():
                group=[p for p in subset if p['category']==name]
                options=dict(marker=marker,s=size,alpha=alpha,linewidths=.65,zorder=5 if name=='CFTC' else 2)
                if name=='Hourly FX (old)':options.update(facecolors='none',edgecolors=color)
                elif name=='CFTC':options.update(facecolors=color,edgecolors='#3b1631',linewidths=.4)
                else:options.update(c=color)
                artist=ax.scatter([p['c'] for p in group],[p['relative_loss_percent'] for p in group],**options)
                artists.append(dict(category=name,kind='scatter',marker=marker,point_ids=[p['point_id'] for p in group],actual_offsets=artist.get_offsets().tolist()))
            for h,marker,color in ((6,'o','#67214a'),(24,'v','#1e2025')):
                group=sorted([p for p in subset if p['family']=='curve' and p['horizon']==h],key=lambda p:p['window'])
                artist=ax.plot([p['c'] for p in group],[p['relative_loss_percent'] for p in group],marker=marker,ms=3.4,color=color,lw=.95,zorder=4)[0]
                artists.append(dict(category=f'FX curve H{h}',kind='line',marker=marker,point_ids=[p['point_id'] for p in group],actual_offsets=[[float(x),float(y)] for x,y in zip(artist.get_xdata(),artist.get_ydata())]))
            label='Full regression (QR33)' if method=='QR33' else 'Four-predictor regression (QR4)'
            ax.set_title(label+'\nComplete range' if row==0 else 'Detail: -45% to 65%',fontsize=9,pad=5)
            ax.grid(axis='x',alpha=.12);ax.tick_params(labelsize=8)
            if row==1:
                ax.set_xlabel('History / (horizon + 1), logarithmic scale',fontsize=8)
                ax.set_xticks([2,10,30,100,400]);ax.set_xticklabels(['2','10','30','100','400'])
            if col==0:ax.set_ylabel('Change in quantile loss (%)',fontsize=8.5)
            panels.append(dict(method=method,full_range=row==0,point_ids=[p['point_id'] for p in subset],
                xlim=list(ax.get_xlim()),ylim=list(ax.get_ylim()),artists=artists))
    names={'v8 simulation':'Discovery simulation','v9 simulation':'Confirmation simulation',
        'CFTC':'CFTC: independent\ndealer source'}
    handles=[Line2D([],[],marker=v[0],color=v[1],ls='',markersize=5,label=names.get(k,k),
        markerfacecolor='none' if k=='Hourly FX (old)' else v[1]) for k,v in styles.items()]
    handles += [Line2D([],[],marker='o',color='#67214a',lw=.9,ms=4,label='FX curve H6'),
        Line2D([],[],marker='v',color='#1e2025',lw=.9,ms=4,label='FX curve H24'),
        Patch(facecolor='#c5cad6',alpha=.5,label='Simulation crossing range')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.065),ncol=3,
        frameon=False,fontsize=7.8,columnspacing=1,handlelength=1.25)
    fig.suptitle('History alone does not guarantee a gain',fontsize=10.4,y=.985)
    fig.text(.105,.022,'All 482 records retained; coincident points may overlap. Negative values favor regression.\nCFTC aggregates dependent markets; shorter-history results were already inspected.\nShading summarizes the simulation grid. Detail panels repeat the full-range records.',fontsize=7.1,color='#3b3b3b')
    meta={'Author':'','CreationDate':None,'ModDate':None}
    fig.savefig(out/'unified-history.pdf',metadata=meta);fig.savefig(out/'unified-history.png',dpi=300);plt.close(fig)

    numeric=[]
    def value(label,path,pointer,fmt,scale=1.):
        raw=read(path)
        for part in pointer.split('/')[1:]:raw=raw[int(part)] if isinstance(raw,list) else raw[part]
        text=format(raw*scale,fmt);numeric.append(dict(id=label,source=path,sha256=sha(ROOT/path),pointer=pointer,
            raw_value=raw,scale=scale,format=fmt,display=text));return text
    result='results/final-merge/wp2-cftc-mechanism/summary.json';menu='results/v10/menu/summary.json';cost='results/v10/cost/report-values.json'
    p1a=value('QR33-low-success',result,'/tests/P1_QR33/successes','.0f')
    p1an=value('QR33-low-n',result,'/tests/P1_QR33/planned','.0f')
    p1b=value('QR4-low-success',result,'/tests/P1_QR4/successes','.0f')
    p1bn=value('QR4-low-n',result,'/tests/P1_QR4/planned','.0f')
    p2=value('QR4-high-success',result,'/tests/P2_QR4/successes','.0f')
    p2n=value('QR4-high-n',result,'/tests/P2_QR4/planned','.0f')
    p3=value('QR4-decrease-success',result,'/tests/P3_QR4/successes','.0f')
    p3n=value('QR4-decrease-n',result,'/tests/P3_QR4/planned','.0f')
    original=value('original-menu',menu,'/predictions/M3/group_operands/constant/original','.2f')
    expanded=value('expanded-menu',menu,'/predictions/M3/group_operands/constant/expanded','.3f')
    low=value('cost-min',cost,'/groups/5/minimum_cheaper_fraction','.1f',100)
    high=value('cost-max',cost,'/groups/5/maximum_cheaper_fraction','.1f',100)
    fig,ax=plt.subplots(figsize=(6.6,4.6));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    boxes=[]
    def box(id,x,y,w,h,text,face='#f4f5f7',size=8.4):
        patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.012,rounding_size=.012',lw=.8,
            facecolor=face,edgecolor='#5c626d');ax.add_patch(patch)
        artist=ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,linespacing=1.38)
        boxes.append(dict(id=id,position=[x,y,w,h],text=text,font_size=size))
    box('benchmark',.15,.80,.70,.14,'Begin with a matched historical limit\nKeep target, dates and available information aligned.','#eaf0f5',9)
    box('history',.025,.32,.29,.36,'History: test the local curve\n\n'+f'Short records: full model loses\nin {p1a}/{p1an} CFTC comparisons.\nSparse model loses in {p1b}/{p1bn}.\n\nAt long history it wins in {p2}/{p2n}.\nStrict improvement holds in {p3}/{p3n}.',size=7.9)
    box('shrinkage',.355,.32,.29,.36,'Shrinkage: test a broad menu\n\n'+f'For the full regression,\na broader menu lowers\nmedian simulation excess loss\nfrom {original}% to {expanded}%.\n\nThis is a menu comparison;\neach penalty need not help.',size=7.9)
    box('cost',.685,.32,.29,.36,'Costs: state the charges\n\n'+f'For the full CFTC regression,\nthe cheaper-limit fraction\nranges from {low}% to {high}%.\n\nExceedance charge is fixed;\nall charges are hypothetical.',size=7.9)
    box('decision',.15,.07,.70,.13,'Compare scores, breaches and stated charges locally\nRetain failures and counterexamples; history gives no automatic cutoff.','#eaf0f5',8.7)
    for x in (.17,.50,.83):
        for y0,y1 in ((.795,.70),(.305,.215)):
            ax.add_patch(FancyArrowPatch((x,y0),(x,y1),arrowstyle='-|>',mutation_scale=9,lw=.8,color='#4f5865'))
    fig.subplots_adjust(left=.02,right=.98,bottom=.04,top=.92)
    fig.suptitle('Validate history, shrinkage and costs together',fontsize=10.4,y=.99)
    fig.savefig(out/'decision-map.pdf',metadata=meta);fig.savefig(out/'decision-map.png',dpi=300);plt.close(fig)
    save(out/'decision-bindings.json',dict(numbers=numeric,boxes=boxes,
        cost_scope=dict(source=cost,group_pointer='/groups/5',primary='CFTC::QR33',fixed_exceedance_charge=1,
            varied_coefficients=['kappa','beta'],fixed_coefficient='c',windows=[52,260],
            original_design='results/v10/cost/manifest.json',
            original_formula=read('results/v10/cost/manifest.json')['design']['formula']),
        shrinkage_scope='Full QR33 regression, constant-parameter simulation arm, original versus expanded fixed menu',
        interpretation='Empirical comparison guidance, no evaluated deployment policy'))
    receipt=dict(point_count=len(data),method_counts=dict(Counter(p['method'] for p in data)),
        family_counts=dict(Counter(p['family'] for p in data)),panels=panels,
        band_source='notes/revision-v9/wp1-breakeven.json',band_sha256=sha(ROOT/'notes/revision-v9/wp1-breakeven.json'),
        bands={m:roots['methods'][m]['intervals']['all_draw_envelope'] for m in ('QR33','QR4')},
        legend=names,duplicated_FX_provenance_records=8,jittered_records=0,rounded_ordinates=0,
        new_model_fits=0,new_statistics=0,diagram_numeric_bindings=len(numeric),
        output_sha256={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()})
    save(out/'render-receipt.json',receipt)
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('panels','output_sha256','bands')},indent=2))


if __name__=='__main__':main()
