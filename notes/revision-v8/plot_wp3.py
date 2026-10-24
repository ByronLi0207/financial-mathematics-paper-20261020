"""Plot saved WP3 summaries; no RNG, simulation, forecasting or score fitting.

The import and grid-validation path use only the standard library. Matplotlib
is loaded only when render() is called. Plotting never changes or completes study results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path

PHIS = (.7,.9,.98)
PERSISTENCES = (0.,.9,.98)
WINDOWS = (52,260,720,2880)
HORIZONS = (6,24)
METHODS = ('F','QR33','QR4')
DISPLAY_METHODS = ('QR33','QR4')
REPETITIONS = 32
METRICS = {
    'loss': dict(field='relative_loss_percent', se='relative_loss_mcse', scale=1.,
        limits=(-100.,100.), ticks=(-100.,-50.,0.,50.,100.),
        label='Relative mean loss against matched F (%)',
        description='Negative values favor regression; positive values favor historical headroom.'),
    'breach': dict(field='model_breach_rate', se='model_breach_mcse', scale=100.,
        limits=(0.,100.), ticks=(0.,25.,50.,75.,100.),
        label='Mean strict breach rate (%)',
        description='A strict breach is an observed peak above the reported limit; the target is 5%.'),
    'win': dict(field='win_fraction', se='win_mcse', scale=100.,
        limits=(0.,100.), ticks=(0.,25.,50.,75.,100.),
        label='Repetitions with lower mean loss than matched F (%)',
        description='A strict win requires lower mean loss than matched F within the same repetition; ties are not wins.'),
}


def _finite(value):
    return type(value) in (int,float) and math.isfinite(value)


def _cell_index(summary):
    try:
        rows=summary['cells']
        if not isinstance(rows,list): raise ValueError('cells must be a list')
        expected={(method,phi,p,w,h) for method in METHODS for phi in PHIS
            for p in PERSISTENCES for w in WINDOWS for h in HORIZONS}
        index={}
        for row in rows:
            key=tuple(row[k] for k in ('method','phi','variance_persistence','window','horizon'))
            if key not in expected or key in index:
                raise ValueError('unexpected or duplicate cell identity')
            index[key]=row
        if set(index)!=expected: raise ValueError('incomplete full factorial inventory')
    except (KeyError,TypeError) as exc:
        raise ValueError('invalid summary inventory') from exc
    return index


def prepare_grids(summary,method,metric):
    """Return six explicit scalar display panels, masking incomplete procedures.

    Conditional-on-completion values stay in ``conditional_value`` for audit;
    they never enter the colored grid. Every drawn eligible cell retains its
    original finite value and MC SE, before presentation rounding/unit scaling.
    """
    if method not in DISPLAY_METHODS or metric not in METRICS:
        raise ValueError('unsupported display method or metric')
    index=_cell_index(summary); spec=METRICS[metric];panels=[]
    for h in HORIZONS:
        for phi in PHIS:
            panel=dict(horizon=h,phi=phi,windows=list(WINDOWS),persistences=list(PERSISTENCES),cells=[])
            for w in WINDOWS:
                displayed=[]
                for p in PERSISTENCES:
                    row=index[(method,phi,p,w,h)]
                    n=row.get('complete_repetitions'); planned=row.get('planned_repetitions')
                    if type(n) is not int or type(planned) is not int or not 0<=n<=planned or planned!=REPETITIONS:
                        raise ValueError('invalid planned/completed repetition inventory')
                    raw=row.get(spec['field']);raw_se=row.get(spec['se'])
                    valid_number=_finite(raw) and _finite(raw_se) and raw_se>=0
                    eligible=(n==REPETITIONS and row.get('full_procedure_status')=='COMPLETE' and valid_number)
                    reason=None if eligible else ('INCOMPLETE_FULL_PROCEDURE' if n!=REPETITIONS or row.get('full_procedure_status')!='COMPLETE' else 'MISSING_OR_NONFINITE_ESTIMATE')
                    value=raw*spec['scale'] if eligible else None
                    se=raw_se*spec['scale'] if eligible else None
                    annotation=(f'{value:.1f}\n({se:.1f})' if eligible else f'NA\n{n}/{planned}')
                    displayed.append(dict(window=w,variance_persistence=p,value=value,mcse=se,
                        eligible=eligible,annotation=annotation,reason=reason,complete_repetitions=n,
                        planned_repetitions=planned,conditional_value=raw if _finite(raw) else None))
                panel['cells'].append(displayed)
            panels.append(panel)
    return panels


def caption(method,metric):
    spec=METRICS[metric]
    name='33-feature quantile regression' if method=='QR33' else 'four-feature quantile regression'
    win_uncertainty=('The plug-in binomial Monte Carlo SE is zero for all wins or no wins; '
        'this does not imply certainty from 32 repetitions. The saved summary also '
        'reports the worst-case SE bound 0.5/√32. ' if metric=='win' else '')
    return (f'{name.capitalize()}: {spec["label"].lower()}. '
        'Rows of panels show horizons H=6 and H=24; columns show level persistence '
        'φ=0.7, 0.9 and 0.98. Within each panel, rows are history length W and columns '
        'are innovation-variance persistence p=α+β. Annotations give the estimate '
        'with Monte Carlo standard error in parentheses, measured across independent '
        'repetitions. A cell is colored only when all 32 planned paired repetitions '
        'complete and its estimate and standard error are finite. Hatched NA cells '
        'show completed/planned counts; NA is neither zero nor evidence of equal '
        'performance. Conditional-on-completion values, solver failures and '
        'unattempted repetitions remain in the complete saved summary and inventory. '
        f'{spec["description"]} {win_uncertainty}'
        'Shading uses fixed limits in every panel; any value beyond a color limit '
        'keeps its uncapped numeric annotation. The finite grid describes these '
        'specified processes and does not establish a universal regime boundary.')


def _no_symlinks(path):
    path=Path(path).absolute()
    if any(p.is_symlink() for p in (path,*path.parents)):
        raise ValueError('symlink output is not allowed')


def render(summary_path,output_dir):
    """Render six PDFs and previews into one new directory; never overwrite."""
    summary_path=Path(summary_path);output_dir=Path(output_dir)
    source_bytes=summary_path.read_bytes();summary=json.loads(source_bytes)
    # Validate every display before creating output; no hidden numerical work.
    all_panels={(method,metric):prepare_grids(summary,method,metric)
        for method in DISPLAY_METHODS for metric in METRICS}
    _no_symlinks(output_dir)
    output_dir.mkdir(parents=True,exist_ok=False)
    os.environ.setdefault('MPLCONFIGDIR',str(output_dir/'matplotlib-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from matplotlib.patches import Rectangle
    plt.rcParams.update({'font.family':'serif','font.size':10.5,'axes.titlesize':10.5,
        'axes.labelsize':10.5,'xtick.labelsize':10,'ytick.labelsize':10,
        'pdf.fonttype':42,'ps.fonttype':42})
    figures=[]
    for (method,metric),panels in all_panels.items():
        spec=METRICS[metric];vmin,vmax=spec['limits'];norm=Normalize(vmin=vmin,vmax=vmax,clip=True)
        cmap=matplotlib.colormaps['Greys'];fig,axes=plt.subplots(2,3,figsize=(7.4,6.4))
        for panel,ax in zip(panels,axes.flat):
            ax.set_xlim(-.5,2.5);ax.set_ylim(3.5,-.5)
            ax.set_xticks(range(3),['0','0.9','0.98']);ax.set_yticks(range(4),[str(w) for w in WINDOWS])
            ax.tick_params(length=0,pad=3)
            ax.set_title(f'H = {panel["horizon"]}, φ = {panel["phi"]:g}',pad=8)
            if panel['phi']==PHIS[0]:ax.set_ylabel('History length W')
            if panel['horizon']==HORIZONS[-1]:ax.set_xlabel('Variance persistence p')
            for y,row in enumerate(panel['cells']):
                for x,cell in enumerate(row):
                    face=cmap(norm(cell['value'])) if cell['eligible'] else 'white'
                    ax.add_patch(Rectangle((x-.5,y-.5),1.,1.,facecolor=face,
                        edgecolor='0.65',linewidth=.6,hatch=None if cell['eligible'] else '///'))
                    dark=cell['eligible'] and norm(cell['value'])>.58
                    ax.text(x,y,cell['annotation'],ha='center',va='center',fontsize=8.8,
                        color='white' if dark else 'black',linespacing=1.15,
                        bbox=None if cell['eligible'] else dict(facecolor='white',edgecolor='none',pad=.8))
            for spine in ax.spines.values():spine.set_visible(False)
        fig.subplots_adjust(left=.10,right=.97,bottom=.25,top=.91,hspace=.48,wspace=.28)
        bar_ax=fig.add_axes((.20,.12,.63,.025))
        scalar=matplotlib.cm.ScalarMappable(norm=norm,cmap=cmap)
        colorbar=fig.colorbar(scalar,cax=bar_ax,orientation='horizontal',ticks=spec['ticks'],extend='both' if metric=='loss' else 'neither')
        colorbar.set_label(spec['label'],labelpad=5)
        fig.text(.5,.015,'Estimate (Monte Carlo SE); hatched NA = incomplete or unavailable full procedure',
            ha='center',va='bottom',fontsize=8.5)
        fig.suptitle('33-feature quantile regression' if method=='QR33' else 'Four-feature quantile regression',fontsize=11.5,y=.985)
        stem=f'v8-wp3-{method.lower()}-{metric}';pdf=output_dir/(stem+'.pdf');png=output_dir/(stem+'.png')
        with pdf.open('xb') as stream:
            fig.savefig(stream,format='pdf',metadata={'Title':f'{method} {metric}; fixed-grid saved summary',
                'Creator':'Matplotlib; saved-summary display only'})
        with png.open('xb') as stream:fig.savefig(stream,format='png',dpi=180)
        plt.close(fig)
        figures.append(dict(method=method,metric=metric,pdf=pdf.name,preview=png.name,
            pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
            preview_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),
            colored_cells=sum(c['eligible'] for p in panels for row in p['cells'] for c in row),
            planned_cells=72,fixed_color_limits=list(spec['limits']),caption=caption(method,metric),
            panels=panels))
    if summary_path.read_bytes()!=source_bytes:
        raise ValueError('source summary changed during display')
    report=dict(operation='saved-summary display only; no model computation',
        source=str(summary_path),source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        forecasts_computed=0,scores_computed=0,new_random_draws=0,figures=figures)
    with (output_dir/'display-receipt.json').open('x') as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    with (output_dir/'captions.md').open('x') as stream:
        stream.write('# WP3 saved-summary figure captions\n\n')
        for row in figures:stream.write('## '+row['pdf']+'\n\n'+row['caption']+'\n\n')
    print(json.dumps(dict(figures=len(figures),source_sha256=report['source_sha256'],output_directory=str(output_dir))))
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--summary',type=Path,required=True)
    parser.add_argument('--outdir',type=Path,required=True)
    args=parser.parse_args(argv)
    render(args.summary,args.outdir)


if __name__=='__main__':main()
