"""Print-size style copies of saved v13 figures; never alters study results.

Every plotted outcome comes directly from the original figure-source bindings
and is checked against its SHA-bound saved JSON row before drawing.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT=Path(__file__).resolve().parents[2]
BLUE='#0072B2';ORANGE='#D55E00'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def array_sha(values):return hashlib.sha256(np.asarray(values,dtype='<f8').tobytes()).hexdigest()


def backup_untracked(path):
    path=Path(path)
    if path.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(path.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backup=path.with_name(path.name+'.'+stamp+'.bak')
        with backup.open('xb') as stream:stream.write(path.read_bytes())


def save(fig,stem):
    files=[]
    for suffix in ('.pdf','.png'):
        path=ROOT/'submission-v10/figures'/(stem+suffix);backup_untracked(path)
        fig.savefig(path,dpi=200,facecolor='white')
        files.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path),bytes=path.stat().st_size))
    plt.close(fig);return files


def verified_g2():
    path=ROOT/'results/v13/nyfed-validation/figure-source-bindings.json'
    binding=json.loads(path.read_text());sources={}
    for name,digest in binding['sources'].items():
        file=ROOT/name
        if sha(file)!=digest:raise ValueError('G2_BOUND_SOURCE_CHANGED:'+name)
        sources[name]=json.loads(file.read_text())
    for point in binding['points']:
        row=sources[point['source_file']][point['json_row_index']]
        if point['status']!=row['status'] or point['relative_loss_pct']!=row['relative_loss_pct']:
            raise ValueError('G2_POINT_CHANGED')
    return path,binding


def build_g2():
    path,binding=verified_g2();points=binding['points']
    fig,axes=plt.subplots(2,2,figsize=(6.4,5.7),layout='constrained')
    fig.set_constrained_layout_pads(w_pad=.055,h_pad=.055,wspace=.025,hspace=.03)
    actual=[];arrays=[]
    groups=[('v13',6,52,'New York Fed: 52-week history\nHorizon 6 weeks'),('v12',6,52,'CFTC: 52-week history\nHorizon 6 weeks'),('v13',24,52,'New York Fed: 52-week history\nHorizon 24 weeks'),('v12',6,260,'CFTC: 260-week history\nHorizon 6 weeks')]
    for ax,(source,h,w,title) in zip(axes.flat,groups):
        owned=[(i,p) for i,p in enumerate(points) if p['source']==source and p['horizon']==h and p['window']==w]
        keys=list(dict.fromkeys(p['source_key'] for _,p in owned))
        for v,offset,colour,marker in [(52,-.12,BLUE,'o'),(156,.12,ORANGE,'s')]:
            values=[];drawn=[]
            for j,key in enumerate(keys):
                matches=[(i,p) for i,p in owned if p['validation_n']==v and p['source_key']==key]
                if len(matches)!=1:raise ValueError('G2_POINT_NOT_UNIQUE')
                i,p=matches[0]
                if p['status']!='COMPLETE':
                    line,=ax.plot(j+offset,0,marker='x',color=colour,linestyle='none',markersize=5)
                    actual.append(dict(source_point_index=i,status=p['status'],plotted_as='unavailable_cross'))
                else:
                    value=p['relative_loss_pct'];line,=ax.plot(j+offset,value,marker=marker,color=colour,linestyle='none',markersize=4.0)
                    rendered=float(line.get_ydata()[0]);assert rendered==value
                    values.append(value);drawn.append(rendered)
                    actual.append(dict(source_point_index=i,value=value,drawn_value=rendered))
            assert np.array_equal(values,drawn)
            arrays.append(dict(source=source,horizon=h,window=w,validation_n=v,n=len(values),source_array_sha256=array_sha(values),drawn_array_sha256=array_sha(drawn)))
        labels=[k.replace('PDPOS','').replace('PDPOSTIPS','TIPS') for k in keys]
        ax.set_xticks(range(len(keys)),labels,rotation=90,fontsize=7.5)
        ax.tick_params(axis='x',pad=2,length=2);ax.tick_params(axis='y',labelsize=8)
        ax.axhline(0,color='0.4',lw=.7);ax.set_title(title,fontsize=8.5,pad=5)
        ax.set_ylabel('Excess pinball\nloss (%)',fontsize=8)
        ax.set_xlabel('Series / contract',fontsize=8,labelpad=4)
        ax.spines[['top','right']].set_visible(False)
    fig.legend(handles=[Line2D([0],[0],marker='o',color=BLUE,linestyle='none',label='52 validation weeks'),Line2D([0],[0],marker='s',color=ORANGE,linestyle='none',label='156 validation weeks')],loc='outside upper center',ncol=2,frameon=False,fontsize=8.5)
    files=save(fig,'v13-validation-length')
    return dict(binding_path=str(path.relative_to(ROOT)),binding_sha256=sha(path),figure_inches=[6.4,5.7],minimum_font_pt=7.5,files=files,point_count=len(actual),drawn_points=actual,array_checks=arrays,numeric_annotations_added=False)


def build_g3():
    path=ROOT/'results/v13/recommended-protocol/figure-source-bindings.json';binding=json.loads(path.read_text())
    source=ROOT/binding['source'];assert sha(source)==binding['sha256'];rows=json.loads(source.read_text())
    for point in binding['points']:
        row=rows[point['json_row_index']];key=point['method']+'_relative_loss_pct'
        if row['cell_id']!=point['cell_id'] or row[key]!=point['relative_loss_pct'] or row[point['method']+'_status']!=point['status']:
            raise ValueError('G3_BOUND_POINT_CHANGED')
    fig,axes=plt.subplots(1,3,figsize=(6.4,2.0),layout='constrained')
    fig.set_constrained_layout_pads(w_pad=.04,h_pad=.035,wspace=.03,hspace=0)
    actual=[];arrays=[]
    for ax,(group,title) in zip(axes,[('cftc','CFTC'),('nyfed','New York Fed'),('fx','FX')]):
        for x,method,colour,marker in [(0,'ordinary',BLUE,'o'),(1,'rp',ORANGE,'s')]:
            owned=[(i,p) for i,p in enumerate(binding['points']) if p['group']==group and p['method']==method]
            complete=[(i,p) for i,p in owned if p['status']=='COMPLETE' and p['relative_loss_pct'] is not None]
            values=[p['relative_loss_pct'] for _,p in complete];drawn=[]
            if values:
                ax.boxplot([values],positions=[x],widths=.45,showfliers=False,patch_artist=True,
                    medianprops={'color':'black','linewidth':1},boxprops={'facecolor':colour,'alpha':.22,'edgecolor':colour},
                    whiskerprops={'color':colour},capprops={'color':colour})
                jitter=np.linspace(-.12,.12,len(values)) if len(values)>1 else [0.]
                for offset,(i,p) in zip(jitter,complete):
                    dot=ax.scatter(x+offset,p['relative_loss_pct'],s=10,marker=marker,color=colour,alpha=.8,zorder=3)
                    rendered=float(dot.get_offsets()[0,1]);assert rendered==p['relative_loss_pct'];drawn.append(rendered)
                    actual.append(dict(source_point_index=i,value=p['relative_loss_pct'],drawn_value=rendered))
            for i,p in owned:
                if p['status']!='COMPLETE':
                    ax.scatter(x,0,marker='x',s=22,color='black',zorder=4)
                    actual.append(dict(source_point_index=i,status=p['status'],plotted_as='unavailable_cross'))
            assert np.array_equal(values,drawn)
            arrays.append(dict(group=group,method=method,n=len(values),source_array_sha256=array_sha(values),drawn_array_sha256=array_sha(drawn)))
        ax.axhline(0,color='0.4',lw=.7);ax.set_title(title,fontsize=9,pad=4)
        ax.set_xticks([0,1],['Ordinary','Protocol'],fontsize=8);ax.tick_params(axis='y',labelsize=8)
        ax.set_xlim(-.48,1.48);ax.spines[['top','right']].set_visible(False)
    axes[0].set_ylabel('Excess pinball loss (%)',fontsize=8)
    files=save(fig,'v13-rp')
    return dict(binding_path=str(path.relative_to(ROOT)),binding_sha256=sha(path),figure_inches=[6.4,2.0],minimum_font_pt=8.,files=files,point_count=len(actual),drawn_points=actual,array_checks=arrays,completion_count_annotations='Omitted from plot to prevent covering extremes; counts remain in saved results and manuscript caption.',numeric_annotations_added=False)


def main():
    before={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'results/v13').rglob('*')) if p.is_file()}
    a,b=build_g2(),build_g3()
    after={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'results/v13').rglob('*')) if p.is_file()}
    if before!=after:raise ValueError('ARCHIVED_RESULTS_CHANGED')
    check=ROOT/'notes/v13/G5-display-check.json';backup_untracked(check)
    record=dict(created_utc=datetime.now(timezone.utc).isoformat(),status='PASS_ALL_DRAWN_OUTCOMES_EXACT',financial_fits_or_scores=False,archived_v13_files_unchanged=len(before),original_study_code_edited=False,G2=a,G3=b,visual_review='PENDING_DIRECT_PRINT_SIZE_VIEW')
    with check.open('w') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(dict(status=record['status'],unchanged_archived_files=len(before),G2_points=a['point_count'],G3_points=b['point_count'])))


if __name__=='__main__':main()
