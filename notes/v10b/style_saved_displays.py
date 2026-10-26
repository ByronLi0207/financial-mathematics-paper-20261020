"""v10b display-only restyling and exact saved-array binding.

Reads saved report-values and display curves only. Does not import a forecasting,
loss, bootstrap, study or reducer module. Writes only notes/v10b and submission
figure/table copies; never writes results, data or protocol.
"""
from pathlib import Path
import csv
import hashlib
import importlib.util
import json
import os
import re
import shutil
import contextlib
import io

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
QA = HERE / 'visual-qa'
BEFORE = QA / 'before'
FIG = ROOT / 'submission-v10/figures'
GEN = ROOT / 'submission-v10/generated'
os.environ['MPLCONFIGDIR'] = str(QA / 'matplotlib-cache')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.text import Text

BLUE = '#0072B2'
VERMILION = '#222222'  # Historical headroom is consistently charcoal.
PURPLE = '#CC79A7'
INK = '#222222'
METHOD = {'QR33': 'Full regression', 'QR4': 'Four-feature'}
SOURCES = [
    'results/v10/menu/report-values.json',
    'results/v10/cftc/report-values.json',
    'results/v10/cost/report-values.json',
    'results/v10/cost/summary.json',
    'results/v10/cost/group-regions.json',
    'results/v10/cost/manifest.json',
    'notes/v7/example-selection.json',
    'results/v9/figures/scalars.json',
    'notes/v7/s5-figure-bindings.json',
    'notes/revision-v8/wp2-figure-styling.json',
    'results/supervisor-20261023/inference/inherited-exact/murphy-fx_hourly-display.csv',
    'results/supervisor-20261023/inference/inherited-exact/murphy-nyfed_weekly-display.csv',
]
STEMS = ['v9-endpoint-peak-example', 'v10-cftc-contract-changes',
         'v10-menu-isolation', 'v10-cost-regions',
         'v7-murphy-fx_hourly', 'v7-murphy-nyfed_weekly']
TABLES = ['v10-cftc-contracts.tex', 'v10-menu-main.tex', 'v10-mcs-main.tex']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def js(path):
    return json.loads((ROOT / path).read_text())


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def arr(a):
    return np.asarray(a, dtype=float).tolist()


def figure_geometry(fig):
    """Actual numerical artist data; no labels, colors or physical geometry."""
    out = []
    for ax in fig.axes:
        if ax.get_label() == '<colorbar>':
            continue
        out.append(dict(
            lines=[dict(x=arr(line.get_xdata()), y=arr(line.get_ydata())) for line in ax.lines],
            offsets=[arr(c.get_offsets()) for c in ax.collections if hasattr(c, 'get_offsets')
                     and c.__class__.__name__ == 'PathCollection'],
            segments=[[arr(s) for s in c.get_segments()] for c in ax.collections
                      if c.__class__.__name__ == 'LineCollection'],
            images=[arr(im.get_array()) for im in ax.images]))
    return out


def original_fig(path, fn, report):
    """Call a display function in memory; bypass all file saving."""
    mod = module(path, 'reference_' + fn + str(len(plt.get_fignums())))
    from matplotlib.figure import Figure
    savefig, close = Figure.savefig, plt.close
    seen = []
    Figure.savefig = lambda *a, **kw: None
    plt.close = lambda f=None: seen.append(f) if isinstance(f, Figure) else None
    try:
        getattr(mod, fn)(report)
        fig = next(f for f in seen if isinstance(f, Figure))
        return figure_geometry(fig)
    finally:
        Figure.savefig, plt.close = savefig, close
        for f in seen:
            if isinstance(f, Figure):
                close(f)


def setup():
    plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
        'axes.labelsize': 10, 'axes.titlesize': 10.5,
        'xtick.labelsize': 9, 'ytick.labelsize': 9,
        'legend.fontsize': 9, 'pdf.fonttype': 42, 'ps.fonttype': 42,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.unicode_minus': False, 'savefig.facecolor': 'white'})


def base(ax):
    ax.grid(axis='y', color='0.88', lw=.55)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=.7)


def save(fig, stem, before, binding, include_geometry=True):
    fig.canvas.draw()
    after = figure_geometry(fig)
    if include_geometry:
        assert before == after, 'PLOTTED_ARRAY_MISMATCH:' + stem
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    clipped = []
    inactive = set()
    for ax in fig.axes:
        for axis, limits in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            for tick in axis.get_major_ticks():
                if not min(limits) <= tick.get_loc() <= max(limits):
                    inactive.update((id(tick.label1), id(tick.label2)))
    for text in fig.findobj(Text):
        if id(text) in inactive or not text.get_visible() or not text.get_text() or text.axes and not text.axes.get_visible():
            continue
        bbox = text.get_window_extent(renderer)
        if bbox.x0 < -1 or bbox.y0 < -1 or bbox.x1 > bounds.width + 1 or bbox.y1 > bounds.height + 1:
            clipped.append(text.get_text())
    assert not clipped, (stem, clipped)
    for ext in ('pdf', 'png'):
        fig.savefig(FIG / f'{stem}.{ext}', dpi=220,
                    metadata={'CreationDate': None, 'ModDate': None} if ext == 'pdf' else {})
    data = dict(figure=stem, before_pdf_sha256=sha(BEFORE / f'{stem}.pdf'),
                after_pdf_sha256=sha(FIG / f'{stem}.pdf'),
                after_png_sha256=sha(FIG / f'{stem}.png'),
                source_binding=binding, before_artist_arrays=before,
                after_artist_arrays=after, array_identity=(before == after),
                array_sha256=hashlib.sha256(json.dumps(after, sort_keys=True).encode()).hexdigest(),
                clipped_text=clipped,
                page_inches=fig.get_size_inches().tolist(),
                minimum_visible_font_pt=min(t.get_fontsize() for t in fig.findobj(Text)
                                           if t.get_visible() and t.get_text()),
                tick_labels=[[t.get_text() for t in a.get_xticklabels()+a.get_yticklabels()] for a in fig.axes])
    plt.close(fig)
    return data


def endpoint():
    source = js('notes/v7/example-selection.json')['selection']
    old = next(x for x in js('results/v9/figures/scalars.json')['figures']
               if x.get('pdf', '').endswith('/v9-endpoint-peak-example.pdf'))
    assert old['pdf_sha256']==sha(BEFORE/'v9-endpoint-peak-example.pdf')
    assert source['absolute_positions'] == old['absolute_positions']
    assert source['dates'] == old['dates'] and source['report'] == old['report']
    x = np.arange(len(source['dates']))
    y = np.array(source['absolute_positions'])
    limit = np.full(len(x), source['report'])
    # Exact arrays already recorded by the original v9 rendering receipt.
    before = [dict(lines=[dict(x=arr(x), y=arr(y)), dict(x=arr(x), y=arr(limit))],
                   offsets=[], segments=[], images=[])]
    fig, ax = plt.subplots(figsize=(6.25, 3.25))
    ax.plot(x, y, color=BLUE, marker='o', ms=4, lw=1.6, label='Observed absolute position')
    ax.plot(x, limit, color=VERMILION, marker='s', markevery=[0, 6], ms=3.6,
            linestyle='--', lw=1.6, label='Historical headroom limit')
    ax.set_xticks(x, [d[5:] for d in source['dates']])
    ax.set(xlabel='Economic date (2021)', ylabel='Absolute position (USD millions)')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:,.0f}'))
    base(ax)
    ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.015), ncol=1, frameon=False)
    fig.subplots_adjust(left=.145, right=.98, bottom=.185, top=.765)
    return save(fig, STEMS[0], before, dict(source='notes/v7/example-selection.json',
        receipt='results/v9/figures/scalars.json', dates=source['dates'], report=source['report'],
        absolute_positions=source['absolute_positions'], unit='USD millions', multiplier=1,
        original_receipt_arrays_equal=True))


def cftc():
    report = js('results/v10/cftc/report-values.json')
    assert sha(ROOT/'results/v10/cftc/contract-changes.pdf')==sha(BEFORE/'v10-cftc-contract-changes.pdf')
    before = original_fig('report_v10_cftc.py', 'figure_bytes', report)
    setup()
    codes = report['selected_codes']
    fig, axes = plt.subplots(1, 2, figsize=(6.25, 5.1), sharex=True, sharey=True)
    fig.subplots_adjust(left=.145, right=.985, top=.85, bottom=.25, wspace=.12)
    values = [r['windows'][str(w)]['QR33']['relative_loss_pct'] for r in report['rows'] for w in (52, 260)]
    visible = [v for v in values if v is not None]
    lo, hi = min([0., *visible]), max([0., *visible]); span = max(hi-lo, 1.)
    for ax, window, marker in zip(axes, (52, 260), ('o', 'D')):
        ax.set_xlim(lo-.09*span, hi+.08*span)
        ax.axvline(0, ls='--', color='.5', lw=.8)
        ax.grid(axis='both', alpha=.18)
        for i, row in enumerate(report['rows']):
            cell = row['windows'][str(window)]['QR33']; value = cell.get('relative_loss_pct')
            if cell['status'] == 'COMPLETE' and value is not None:
                ax.scatter(value, i, color=BLUE, marker=marker, s=27, zorder=3)
            else:
                ax.text(.94, i, 'NA', transform=ax.get_yaxis_transform(), ha='right', va='center', fontsize=9)
        ax.set_yticks(range(len(codes)), codes)
        ax.set_title(f'History {window}', fontsize=10.5)
        ax.set_xlabel('Relative loss change (%)', fontsize=10)
    axes[0].set_ylim(len(codes)-.5, -.5)
    axes[0].set_ylabel('Contract code, fixed open-interest order', fontsize=10)
    fig.suptitle('Full regression versus matched historical headroom', fontsize=11, y=.96)
    fig.text(.145, .130, f'All {len(codes)} selected contracts; positive values mean higher regression loss.', fontsize=8.8)
    fig.text(.145, .088, 'NA retains incomplete or nonpositive-reference slots.', fontsize=8.8)
    fig.text(.145, .046, 'Related contracts are not independent dealers; counts are not dollar exposures.', fontsize=8.8)
    return save(fig, STEMS[1], before, dict(source='results/v10/cftc/report-values.json',
        method='QR33', windows=[52, 260], selected_codes=codes, relative_loss_pct=values))


def menu():
    report = js('results/v10/menu/report-values.json')
    assert sha(ROOT/'results/v10/menu/menu-isolation.pdf')==sha(BEFORE/'v10-menu-isolation.pdf')
    before = original_fig('report_v10_menu.py', 'figure_bytes', report)
    setup()
    fig, axes = plt.subplots(2, 2, figsize=(6.25, 5.1), sharey=True, squeeze=False)
    fig.subplots_adjust(left=.125, right=.98, bottom=.225, top=.79, hspace=.78, wspace=.18)
    index = {(r['arm'], r['window'], r['method']): r for r in report['rows']}
    styles = [('old', 'Old menu', 'o', -.11), ('expanded', 'Expanded menu', 'D', .11)]
    visible = [s[k] for r in report['rows'] for s in (r['old'], r['expanded'])
               if s['status'] == 'COMPLETE' for k in ('q25_pct', 'median_pct', 'q75_pct')]
    low, high = min([0., *visible]), max([0., *visible]); span = max(high-low, 1.)
    for ai, arm in enumerate(report['arms']):
        for wi, window in enumerate(report['windows']):
            ax = axes[ai, wi]
            ax.set_ylim(low-.10*span, high+.32*span)
            ax.axhline(0, color='.5', lw=.8, ls='--', zorder=0)
            ax.grid(axis='y', color='.85', lw=.5)
            for mi, method in enumerate(report['methods']):
                row = index[arm, window, method]
                color = BLUE if method == 'QR33' else PURPLE
                if all(row[n]['status'] == 'COMPLETE' for n in ('old', 'expanded')):
                    ax.plot([mi-.11, mi+.11], [row['old']['median_pct'], row['expanded']['median_pct']],
                            color='.72', lw=1, zorder=1)
                missing = []
                for name, label, marker, offset in styles:
                    side = row[name]
                    if side['status'] != 'COMPLETE':
                        missing.append(f'{label}: NA ({side["complete_sources"]}/{side["required_sources"]})')
                        continue
                    median, q25, q75 = side['median_pct'], side['q25_pct'], side['q75_pct']
                    ax.errorbar(mi+offset, median, yerr=[[median-q25], [q75-median]],
                        color=color, marker=marker, markerfacecolor='white' if name=='old' else color,
                        markersize=5, capsize=3, lw=1.35, ls='none', zorder=3)
                if missing:
                    ax.text(mi, .96, '\n'.join(missing), transform=ax.get_xaxis_transform(),
                        ha='center', va='top', fontsize=8.5, color=INK,
                        bbox=dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5))
            ax.set_xlim(-.48, len(report['methods'])-.52)
            ax.set_xticks(range(len(report['methods'])), [METHOD[m].replace(' ', '\n', 1) for m in report['methods']])
            ax.set_title(f'{arm.capitalize()} | History {window}', fontsize=10)
            if wi == 0:
                ax.set_ylabel('Relative loss change (%)', fontsize=10)
    fig.suptitle('Matched penalty menus: all-source medians', fontsize=11, y=.97)
    handles = [Line2D([0], [0], color=INK, marker=marker, markerfacecolor='white' if name=='old' else INK,
                     ls='none', ms=5, label=label) for name, label, marker, offset in styles]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.55, .925), frameon=False, ncol=2)
    fig.text(.125, .125, f'Points: median across all {report["source_count"]} source medians; whiskers: source IQR.', fontsize=8.8)
    fig.text(.125, .088, f'Each source uses {report["formal"]["repetitions"]} matched repetitions; incomplete groups remain NA.', fontsize=8.8)
    fig.text(.125, .051, 'Positive = higher regression loss; IQR is descriptive, not a confidence interval.', fontsize=8.8)
    return save(fig, STEMS[2], before, dict(source='results/v10/menu/report-values.json',
        rows=report['rows'], source_count=report['source_count'], repetitions=report['formal']['repetitions']))


def cost():
    rows = js('results/v10/cost/group-regions.json')
    report = js('results/v10/cost/report-values.json')
    design = js('results/v10/cost/manifest.json')['design']
    tags = list(design['primary_method_by_group'])
    before = []
    # Verbatim source-comprehension order from report_v10_cost.py.
    for tag in tags:
        rr = [x for x in rows if x['group_label'] == tag and x['c'] == design['primary_c']]
        a = [[next(r for r in rr if r['kappa']==k and r['beta']==b)['lower']
              for b in design['grid']['beta']] for k in design['grid']['kappa']]
        before.append(dict(lines=[], offsets=[], segments=[], images=[a]))
    assert sha(ROOT/'results/v10/cost/cost-regions.pdf')==sha(BEFORE/'v10-cost-regions.pdf')
    # Execute the original aggregate-display main with all outputs redirected
    # to notes/v10b and inspect its real image artists. No scientific routine
    # is called, and the saved result paths are never output destinations.
    ref=QA/'cost-original-reference';ref.mkdir(exist_ok=True)
    for filename in ['group-regions.json','summary.json','manifest.json']:
        shutil.copy2(ROOT/'results/v10/cost'/filename,ref/filename)
    for filename in ['report-values.json','report-note-zh.md']:
        if (ref/filename).exists():(ref/filename).unlink()
    original=module('report_v10_cost.py','inherited_cost_display');original.P=ref
    from matplotlib.figure import Figure
    savefig=Figure.savefig;captured=[]
    Figure.savefig=lambda fig,*a,**kw:captured.append(figure_geometry(fig))
    try:
        with contextlib.redirect_stdout(io.StringIO()):original.main()
    finally:Figure.savefig=savefig
    assert captured and captured[0]==before,'ORIGINAL_COST_IMAGE_ARRAYS_MISMATCH'
    setup()
    fig, axes = plt.subplots(3, 2, figsize=(6.25, 7.2))
    fig.subplots_adjust(left=.10, right=.855, top=.91, bottom=.09, hspace=.64, wspace=.38)
    cmap = LinearSegmentedColormap.from_list('OkabeIto_blue_fraction', ['#FFFFFF', BLUE])
    bindings = []
    def tick(x):
        return '.'+format(x, 'g')[2:] if 0<x<1 else format(x, 'g')
    for ax, tag in zip(axes.flat, tags):
        lookup = {(r['kappa'], r['beta']):r for r in rows if r['group_label']==tag and r['c']==design['primary_c']}
        a = np.array([[lookup[k,b]['lower'] for b in design['grid']['beta']] for k in design['grid']['kappa']])
        upper = np.array([[lookup[k,b]['upper'] for b in design['grid']['beta']] for k in design['grid']['kappa']])
        saved = next(x for x in report['groups'] if x['group_label']==tag)
        assert float(a.min())==saved['minimum_cheaper_fraction'] and float(a.max())==saved['maximum_cheaper_fraction']
        assert int(np.count_nonzero(a!=upper))==saved['unknown_grid_points']
        image=ax.imshow(a, vmin=0, vmax=1, origin='lower', aspect='auto', cmap=cmap)
        ax.set_xticks(range(len(design['grid']['beta'])), [tick(x) for x in design['grid']['beta']], fontsize=8.5)
        plt.setp(ax.get_xticklabels(), rotation=40, ha='right')
        ax.set_yticks(range(len(design['grid']['kappa'])), [tick(x) for x in design['grid']['kappa']], fontsize=8.5)
        for yi,xi in zip(*np.nonzero(a!=upper)):
            ax.text(xi,yi,f'[{a[yi,xi]:.2f},{upper[yi,xi]:.2f}]',ha='center',va='center',fontsize=8)
        rr=next(iter(lookup.values()))
        label=tag.replace('Same-record dailyFX', 'Same-record daily FX').replace('FX early2015', 'FX earlier period')
        ax.set_title(f'{label}\n{rr["complete"]}/{rr["planned"]} complete', fontsize=9.5, pad=5)
        ax.set_xlabel(r'Breach charge $\beta=b/m_F$', fontsize=9, labelpad=4)
        ax.set_ylabel(r'Reserve coefficient $\kappa$', fontsize=9, labelpad=4)
        bindings.append(dict(group_label=tag,beta=design['grid']['beta'],kappa=design['grid']['kappa'],
                             lower=a.tolist(),upper=upper.tolist(),complete=rr['complete'],planned=rr['planned']))
    cax=fig.add_axes([.88,.23,.020,.52], label='<colorbar>')
    cb=fig.colorbar(image,cax=cax);cb.set_label('Fraction cheaper than historical headroom',fontsize=9,labelpad=5)
    cb.ax.tick_params(labelsize=8.5)
    fig.suptitle('Normalized report costs: full registered grid at c = 1', fontsize=11, y=.98)
    return save(fig, STEMS[3], before, dict(sources=['results/v10/cost/group-regions.json',
        'results/v10/cost/report-values.json','results/v10/cost/manifest.json'],c=design['primary_c'],groups=bindings))


def murphy(name):
    path=f'results/supervisor-20261023/inference/inherited-exact/murphy-{name}-display.csv'
    rows=list(csv.DictReader((ROOT/path).open()))
    x=[float(r['theta_USD_millions']) for r in rows]
    left=[float(r['left_elementary']) for r in rows]
    right=[float(r['right_elementary']) for r in rows]
    receipt=next(r for r in js('notes/v7/s5-figure-bindings.json') if r['figure']==f'v7-murphy-{name}')
    assert receipt['sha256']==sha(ROOT/path) and receipt['point_count']==len(x)==201
    # Rebuild the frozen native-TeX source in notes/v10b, then compare every
    # original qbezier segment. This binds the existing PDF's displayed curves,
    # not merely its input filename.
    old_module=module('notes/v7/build_figure_sources.py','old_murphy_'+name)
    old_module.OUT=QA
    old_module.source(f'v7-murphy-{name}',x,[('Conditional regression',left,old_module.BLUE),
        ('Historical headroom reference',right,old_module.ORANGE)],
        'Score threshold (USD millions)','Mean elementary score')
    old_tex=ROOT/f'notes/v7/figure-sources/v7-murphy-{name}.tex'
    generated=QA/f'v7-murphy-{name}.tex'
    assert generated.read_bytes()==old_tex.read_bytes(), 'BASELINE_TEX_CURVES_MISMATCH'
    real_receipt=next(r for r in js('notes/revision-v8/wp2-figure-styling.json')['figures']
                      if r['path'].endswith(f'/v7-murphy-{name}.pdf'))
    assert real_receipt['sha256']==sha(BEFORE/f'v7-murphy-{name}.pdf')
    assert real_receipt['source_sha256']==sha(ROOT/path)
    scale=real_receipt['unit_scale']
    plotted_x=[v*scale for v in x]
    # Capture the actual inherited revision-v8 display routine in memory.
    # Redirect its only direct preview/receipt writes into the QA directory.
    original=module('notes/revision-v8/style_figures.py','inherited_murphy_'+name)
    captured={}
    def capture(fig,ax,stem,xdigits,ydigits):
        captured[stem]=figure_geometry(fig)
        plt.close(fig)
        return dict(preview='notes/v10b/visual-qa/inherited-endpoint-preview.png')
    original.OUT=QA;original.NOTES=QA;original.save=capture
    with contextlib.redirect_stdout(io.StringIO()):original.main()
    before=captured[f'v7-murphy-{name}']
    assert before==[dict(lines=[dict(x=plotted_x,y=left),dict(x=plotted_x,y=right)],offsets=[],segments=[],images=[])]
    setup()
    fig,ax=plt.subplots(figsize=(6.25,3.45))
    ax.plot(plotted_x,left,color=BLUE,lw=1.5,marker='o',markevery=20,ms=3.8,label='Full regression')
    ax.plot(plotted_x,right,color=VERMILION,lw=1.5,ls='--',marker='s',markevery=20,ms=3.6,label='Historical headroom')
    unit='USD millions' if scale==1 else 'USD billions'
    ax.set(xlabel=f'Score threshold ({unit})',ylabel='Mean elementary score (dimensionless)')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:,.0f}'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:.3f}'))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5));base(ax)
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    fig.subplots_adjust(left=.15,right=.94,bottom=.18,top=.82)
    return save(fig,f'v7-murphy-{name}',before,dict(source=path,points=len(x),
        baseline_tex=str(old_tex.relative_to(ROOT)),baseline_tex_sha256=sha(old_tex),
        rebuilt_baseline_tex_sha256=sha(generated),baseline_tex_byte_identity=True,
        inherited_pdf_sha_receipt='notes/revision-v8/wp2-figure-styling.json',
        inherited_pdf_sha_identity=True,actual_inherited_display_function_arrays_captured=True,
        x_USD_millions=x,left_elementary=left,right_elementary=right,
        x_multiplier=scale,plotted_x=plotted_x,plotted_x_unit=unit,y_multiplier=1,new_scores=0))


def table_cells(text):
    """Body rows only; preserve explicit display strings, identifiers and NA."""
    body=text.split(r'\midrule',1)[1].split(r'\bottomrule',1)[0]
    return [r.strip() for r in body.split(r'\\') if r.strip()]


def cftc_table():
    path=GEN/TABLES[0];old=(BEFORE/TABLES[0]).read_text()
    data=js('results/v10/cftc/report-values.json'); old_rows=table_cells(old)
    header=[r'\begin{table}[t]\centering\scriptsize',r'\setlength{\tabcolsep}{2pt}',
        r'\caption{CFTC dealer-category futures: relative loss versus matched historical headroom (\%). All 17 selected literal contract codes are retained.}',
        r'\label{tab:v10-cftc-contracts}',r'\resizebox{\linewidth}{!}{%',
        r'\begin{tabular}{l*{10}{r@{.}l}}\toprule',
        r'Contract & \multicolumn{10}{c}{History 52} & \multicolumn{10}{c}{History 260} \\',
        r'\cmidrule(lr){2-11}\cmidrule(lr){12-21}',
        r'code & '+ ' & '.join(r'\multicolumn{2}{c}{\shortstack{'+x+'}}' for x in
            [r'Intercept\\only',r'Four-\\feature',r'Full\\regression',r'Calibrated\\history',r'Calibrated\\regression']*2)+r' \\ \midrule']
    cells=[];after=[]
    for row,old_row in zip(data['rows'],old_rows):
        expected=[f'{row["windows"][str(w)][m]["relative_loss_pct"]:.2f}'
                  if row['windows'][str(w)][m]['status']=='COMPLETE' else r'\textsc{NA}'
                  for w in (52,260) for m in ('I','QR4','QR33','ACI_F','ACI_QR33')]
        before=[x.strip() for x in old_row.split('&')]
        assert before==[row['code'],*expected]
        pieces=[]
        for value in expected:
            pieces.append(value.replace('.', ' & ') if value!=r'\textsc{NA}' else r'\multicolumn{2}{c}{\textsc{NA}}')
        cells.append(row['code']+' & '+' & '.join(pieces)+r' \\')
        after.append(dict(contract=row['code'],before=expected,after=expected,exact_string_identity=True))
    tail=[r'\bottomrule\end{tabular}}',r'\par\vspace{2pt}\begin{minipage}{.98\linewidth}\footnotesize',
        r'Entries are $100(\overline L_m/\overline L_F-1)$: positive values mean higher loss, NA retains failed/incomplete methods or an unavailable/nonpositive $F$ denominator, and rounded displays leave full-precision decisions unchanged; columns map to $I$, QR4, QR33, ACI-$F$ and ACI-QR33.',
        r'T1 uses all selected-contract/two-history cells (denominator 34) and requires a fraction at least 0.60; T2 requires the full-regression median at both histories inside \mbox{[-10.00, 10.00]\%}; T3 strictly compares complete all-contract four-feature medians.',
        r'No successful-contract subset substitutes for a threshold; all absolute score, breach and selection receipts remain in the saved summary and exported cells.',
        r'\end{minipage}\end{table}','']
    path.write_text('\n'.join(header+cells+tail))
    return dict(table=TABLES[0],rows=after,numeric_cells=170,decimal_places=2,
                decimal_alignment='native r@{.}l columns',note_sentences=3)


def menu_table():
    path=GEN/TABLES[1];old=(BEFORE/TABLES[1]).read_text()
    data=js('results/v10/menu/report-values.json');old_rows=table_cells(old)
    def value(side):
        return r'\textsc{NA}' if side['status']!='COMPLETE' else f'{side["median_pct"]:.2f} [{side["q25_pct"]:.2f}, {side["q75_pct"]:.2f}]'
    def aligned(side):
        if side['status']!='COMPLETE':return r'\textsc{NA}'
        a,b,c=[f'{side[k]:.2f}' for k in ('median_pct','q25_pct','q75_pct')]
        return r'\makebox[3.0em][r]{'+a+r'} [\makebox[3.1em][r]{'+b+r'}, \makebox[3.2em][r]{'+c+r'}]'
    lines=[r'\begin{table}[t]\centering\footnotesize',r'\setlength{\tabcolsep}{2pt}',
        r'\caption{Penalty-menu isolation on matched calibrated paths. Entries are the median relative loss (\%) across all 13 source medians, with the descriptive source IQR in brackets.}',
        r'\label{tab:v10-menu-isolation}',r'\begin{tabular}{lllrrr}\toprule',
        r'Arm & History & Regression & Original menu & Expanded menu & Missing sources \\',
        r' & & & Median [IQR] & Median [IQR] & Original / expanded \\ \midrule']
    checks=[]
    for row,old_row in zip(data['rows'],old_rows):
        before=[x.strip() for x in old_row.split('&')]
        values=[row['arm'].capitalize(),str(row['window']),row['method'],value(row['old']),value(row['expanded']),f'{len(row["old"]["missing_sources"])} / {len(row["expanded"]["missing_sources"])}']
        assert before==values
        lines.append(' & '.join([values[0],values[1],METHOD[row['method']],aligned(row['old']),aligned(row['expanded']),values[-1]])+r' \\')
        checks.append(dict(arm=row['arm'],history=row['window'],method=row['method'],before=values[3:],after=values[3:],exact_string_identity=True))
    lines += [r'\bottomrule\end{tabular}',r'\par\vspace{2pt}\begin{minipage}{.98\linewidth}\footnotesize',
        r'Each source median uses all 32 matched repetitions with relative loss $100(\overline L_{QR}/\overline L_F-1)$; positive values mean higher regression loss, and NA retains unavailable all-source summaries without substituting successful subsets.',
        r'Displays are rounded, while registered decisions use saved full-precision operands; full and four-feature regression correspond to QR33 and QR4.',
        r'The expanded four-feature exact-tie rule prefers stronger penalties, unlike its original rule; saved exact ties: 0, changed selections: 0.',
        r'\end{minipage}\end{table}','']
    path.write_text('\n'.join(lines))
    return dict(table=TABLES[1],rows=checks,decimal_places=2,
                decimal_alignment='fixed-width right-aligned tabular numerals for median and each quartile',note_sentences=3)


def mcs_table():
    path=GEN/TABLES[2];old=(BEFORE/TABLES[2]).read_text();old_rows=table_cells(old)
    def aligned(text):
        m=re.fullmatch(r'([\d/]+) \(([\d.]+)\\%\)',text)
        if not m:return text
        return r'\makebox[3.2em][r]{'+m[1]+r'} (\makebox[2.9em][r]{'+m[2]+r'}\%)'
    lines=[r'\begin{table}[t]\centering\footnotesize',r'\setlength{\tabcolsep}{4pt}',
        r'\caption{Ninety-percent model confidence sets across all planned comparisons. Counts retain their comparison or conditional-procedure denominators.}\label{tab:v10-mcs-main}',
        r'\begin{tabular}{lrrrrr}\toprule',
        r'Group & Complete & Matched history & Sole historical & Conditional & Unavailable \\',
        r' & / planned & included & method & excluded & procedures \\ \midrule']
    checks=[]
    for row in old_rows:
        cells=[x.strip() for x in row.split('&')]
        # The inherited header attaches \\midrule to the first cell; the
        # body parser above deliberately leaves only true body rows.
        assert len(cells)==6,cells
        new=[cells[0].replace('FX early2015','FX earlier period').replace('Same-record dailyFX','Same-record daily FX'),cells[1],*[aligned(x) for x in cells[2:5]],cells[5]]
        lines.append(' & '.join(new)+r' \\')
        checks.append(dict(group=cells[0],before=cells[1:],after=cells[1:],exact_string_identity=True))
    lines += [r'\bottomrule\end{tabular}',r'\par\smallskip\begin{minipage}{.98\linewidth}\footnotesize',
        r'All planned comparisons complete, so successful and planned denominators coincide; matched history means $F/I$, excluding rolling references and query-nearest state baselines, and conditional exclusions count complete procedure slots rather than prior NA methods.',
        r'A sole exact-loss class can retain several procedures: 4/98 sets have such a class containing $F/I$, so the sole-class count differs from the sole-method column; related tasks are not independent replications.',
        r'Supplement Section S31 retains every set, p-value, loss class, secondary membership measure and availability record.',
        r'\end{minipage}\end{table}','']
    path.write_text('\n'.join(lines))
    return dict(table=TABLES[2],rows=checks,percent_decimal_places=1,
                decimal_alignment='fixed-width right-aligned ratios and tabular one-decimal percentages',note_sentences=3,
                compact_full_membership_values_preserved=True)


def supplementary_table_fixes():
    """Only header pagination and phantom spacing; no displayed content removed."""
    checks=[]
    path=GEN/'v10-menu-full.tex';snapshot=BEFORE/path.name
    if not snapshot.exists():shutil.copy2(path,snapshot)
    old=snapshot.read_text()
    header=r'\toprule Source & Arm & W & Predictors & Old median & Expanded median & Complete/R & State \\\midrule'
    assert old.count(header+r'\endhead')==1
    readable_header=header.replace(' & W & ',' & History & ').replace('Old median','Original median').replace('Complete/R','Complete/required')
    new=old.replace(header+r'\endhead',readable_header+r'\endfirsthead'+'\n'+readable_header+r'\endhead')
    # Every numerical body row remains byte-identical.
    body=lambda t:[l for l in t.splitlines() if '&' in l and not l.startswith('\\toprule')]
    assert body(old)==body(new)
    path.write_text(new)
    checks.append(dict(table=path.name,before_sha256=sha(snapshot),after_sha256=sha(path),
        body_rows=len(body(old)),body_rows_byte_identical=True,
        change='caption and label execute only in first head; continuation repeats only column labels'))
    path=GEN/'v10-mcs-compact.tex';snapshot=BEFORE/path.name
    if not snapshot.exists():shutil.copy2(path,snapshot)
    old=snapshot.read_text()
    pattern=r'\$(?:\\mathbf\{)?\d\.\d{3}\}?(?:\^\{\\mathrm\{M\d\d\}\})?\$'
    tokens=re.findall(pattern,old)
    def pad(match):
        s=match[0]
        return s if r'^{\mathrm' in s else s[:-1]+r'\hphantom{^{\mathrm{M00}}}$'
    def block_pad(match):
        block=match[0]
        lines=block.splitlines(keepends=True)
        class_columns=set()
        for line in lines:
            for col,cell in enumerate(line.split('&')):
                if re.search(r'\^\{\\mathrm\{M\d\d\}\}',cell):class_columns.add(col)
        out=[]
        for line in lines:
            cells=line.split('&')
            for col in class_columns:
                if col<len(cells):cells[col]=re.sub(pattern,pad,cells[col])
            out.append('&'.join(cells))
        return ''.join(out)
    new=re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}',block_pad,old,flags=re.S)
    # Strip only our invisible decoration to verify the entire file, not a
    # subset of p-values; IDs, bold memberships, dashes and NA are unchanged.
    assert new.replace(r'\hphantom{^{\mathrm{M00}}}','')==old
    assert len(tokens)==len(re.findall(pattern,new.replace(r'\hphantom{^{\mathrm{M00}}}','')))
    names=[
        r'Hist.\\headroom',r'Intercept\\only',r'Cal. SAV\\history',r'Cal. SAV\\regression',r'SAV\\headroom',
        r'Cal.\\history',r'Cal. full\\regression',r'Full\\regression',r'Four-\\feature',
        r'Expanded\\full reg.',r'Endpoint\\plug-in',r'Four-\\feature',r'Legacy\\multi-fold',
        r'Finite\\ridge',r'Expanded\\ridge',r'One-SE\\ridge',r'Multi-fold\\one-SE',
        r'Original\\full reg.',r'Original\\roll. hist.',r'Full\\regression',r'Four-\\feature',
        r'Filtered\\paths',r'Peak-tail\\fit',r'Quantile\\forest',r'Nearest\\states',r'Original\\full reg.',
        r'Scaled\\neighbors',r'Frozen\\peak',r'Frozen\\transl.',r'State\\headroom',r'State\\peak',
        r'State\\transl.',r'Rolling\\headroom',r'Rolling\\peak',r'Rolling\\transl.',
        r'Expanded\\full reg.',r'Four-\\feature',r'Endpoint\\plug-in',r'Original\\full reg.',r'Mean\\combination',r'Median\\combination']
    mapping={f'M{i:02}':n for i,n in enumerate(names,1)}
    lines=[]
    for line in new.splitlines(keepends=True):
        if line.startswith('Source & $H$ & $W$ &'):
            line=re.sub(r'\\texttt\{(M\d\d)\}',lambda m:r'\rotatebox{90}{\shortstack[l]{'+mapping[m[1]]+'}}',line)
            line=line.replace('$H$',r'\rotatebox{90}{Horizon}').replace('$W$',r'\rotatebox{90}{History}')
        lines.append(line)
    new=''.join(lines).replace(r'\setlength{\tabcolsep}{2.15pt}',r'\setlength{\tabcolsep}{1.35pt}')
    assert re.findall(pattern,new.replace(r'\hphantom{^{\mathrm{M00}}}',''))==tokens
    assert new.count(r'\textsc{NA}')==old.count(r'\textsc{NA}')
    path.write_text(new)
    checks.append(dict(table=path.name,before_sha256=sha(snapshot),after_sha256=sha(path),
        p_value_tokens=len(tokens),all_p_value_tokens_exactly_identical=True,all_NA_retained=True,
        full_file_identity_before_header_renaming_and_after_removing_padding=True,
        readable_header_mapping=mapping,
        added_phantom_slots=new.count(r'\hphantom{^{\mathrm{M00}}}'),
        change='in columns carrying loss-class superscripts, reserve that same width on other p-values; other columns, NA and complete membership remain'))
    return checks


def legacy_header_fixes():
    """Human-readable headers only, with byte identity for all data rows."""
    replacements={
        'v9-stability-W52-table.tex': [('QR33 $\\Delta$ [IQR]',r'Full regression $\Delta$ [IQR]'),('QR4 $\\Delta$ [IQR]',r'Four-feature $\Delta$ [IQR]')],
        'v9-stability-W260-table.tex': [('QR33 $\\Delta$ [IQR]',r'Full regression $\Delta$ [IQR]'),('QR4 $\\Delta$ [IQR]',r'Four-feature $\Delta$ [IQR]')],
        'v9-stability-diagnostics-table.tex': [('$H$',r'Statistic'),('M4',r'\shortstack{Moment\\valid}'),('Cap',r'\shortstack{Break\\cap}')],
        'v9-stability-F-table.tex':[('$W$','History'),('$R$',r'\shortstack{Complete /\\required}')],
        'v9-legacy-simulation-table.tex': [('DGP','Process'),('$W$','History'),('$p$','Features'),('$R$',r'\shortstack{Complete /\\required}'),
            (r'QR $\Delta$ [IQR]',r'Regression $\Delta$ [IQR]'),(r'I $\Delta$',r'\shortstack{Intercept\\change}'),
            (r'O $\Delta$',r'\shortstack{Oracle\\change}'),('F hit',r'\shortstack{Historical\\hit}'),
            ('I hit',r'\shortstack{Intercept\\hit}'),('QR hit',r'\shortstack{Regression\\hit}'),
            ('O hit',r'\shortstack{Oracle\\hit}'),(r'$\infty$',r'\shortstack{Infinite\\penalty}')],
        'v8-three-window-table.tex':[('QR / F','Reg. / hist.')],
        'v8-backcast-complete-table.tex':[('QR / F','Reg. / hist.')],
        'v8-mc-full-table.tex':[('$H$','Horizon'),('vs F','vs history'),('F breach','Historical breach')],
        'v8-mc-four-table.tex':[('$H$','Horizon'),('vs F','vs history'),('F breach','Historical breach')],
    }
    checks=[]
    for name,pairs in replacements.items():
        path=GEN/name;snapshot=BEFORE/name
        if not snapshot.exists():shutil.copy2(path,snapshot)
        old=snapshot.read_text();new_lines=[];changed=[]
        for line in old.splitlines(keepends=True):
            # Exact known header prefixes; never rewrite saved Native comments,
            # captions, data rows or scientific values.
            is_header=(line.startswith(('Source &','DGP &','Window &','Horizon &','$H$ &')))
            if is_header:
                original=line
                for a,b in pairs:line=line.replace(a,b)
                if name=='v9-stability-diagnostics-table.tex':
                    line=line.replace('Statistic',r'\rotatebox{90}{Statistic}')
                    line=line.replace(r'\shortstack{Moment\\valid}',r'\rotatebox{90}{Moment valid}')
                    line=line.replace(r'\shortstack{Break\\cap}',r'\rotatebox{90}{Break cap}')
                if name=='v9-legacy-simulation-table.tex':
                    for phrase in ['History','Features']:
                        line=line.replace(phrase,r'\rotatebox{90}{'+phrase+'}')
                    for phrase in [r'Complete /\\required',r'Intercept\\change',r'Oracle\\change',
                        r'Historical\\hit',r'Intercept\\hit',r'Regression\\hit',r'Oracle\\hit',r'Infinite\\penalty']:
                        line=line.replace(r'\shortstack{'+phrase+'}',r'\rotatebox{90}{\shortstack[l]{'+phrase+'}}')
                if line!=original:changed.append(dict(before=original.strip(),after=line.strip()))
            new_lines.append(line)
        new=''.join(new_lines);path.write_text(new)
        checks.append(dict(table=name,before_sha256=sha(snapshot),after_sha256=sha(path),
            changed_headers=changed,all_non_header_lines_byte_identical=True))
    return checks


def caption_fixes():
    edits={
        'v8-daily-results-table.tex':(
            'Same-dealer daily sampled-position results. History and horizon count recorded nonempty calendar days.',
            'Same-dealer daily sampled-position results; history and horizon count recorded nonempty calendar days.'),
        'v8-three-window-table.tex':(
            'H6 original regression across three inspected windows. The full-prefix window contains the earlier reported backcast, so this is not independent validation.',
            'Six-step original regression across three inspected windows; the full-prefix window contains the earlier reported backcast, so this is not independent validation.'),
        'v8-backcast-complete-table.tex':(
            'Complete full-prefix backcast comparisons. The two regressions use the original later-selected parameters.',
            'Complete full-prefix backcast comparisons; the two regressions use the original later-selected parameters.'),
        'v8-mc-full-table.tex':(
            'Every cell is retained. The frozen narrow-region restriction fails.',
            'Every cell is retained; the frozen narrow-region restriction fails.'),
        'v8-mc-four-table.tex':(
            'Every cell is retained. The frozen narrow-region restriction fails.',
            'Every cell is retained; the frozen narrow-region restriction fails.'),
    }
    checks=[]
    for name,(old,new) in edits.items():
        path=GEN/name;snapshot=BEFORE/name
        if not snapshot.exists():shutil.copy2(path,snapshot)
        text=path.read_text()
        assert old in text or new in text
        path.write_text(text.replace(old,new))
        checks.append(dict(table=name,before_caption=old,after_caption=new,
            caption_sentences_after=3,numerical_body_changed=False))
    return checks


def main():
    QA.mkdir(parents=True,exist_ok=True);BEFORE.mkdir(exist_ok=True)
    sources={p:sha(ROOT/p) for p in SOURCES}
    for stem in STEMS:
        for ext in ('pdf','png'):
            source=FIG/f'{stem}.{ext}';target=BEFORE/source.name
            if source.exists() and not target.exists():shutil.copy2(source,target)
    for name in TABLES:
        if not (BEFORE/name).exists():shutil.copy2(GEN/name,BEFORE/name)
    setup()
    figures=[endpoint(),cftc(),menu(),cost(),murphy('fx_hourly'),murphy('nyfed_weekly')]
    tables=[cftc_table(),menu_table(),mcs_table()]
    supplementary=supplementary_table_fixes()
    legacy=legacy_header_fixes()
    captions=caption_fixes()
    for t in tables:
        t['before_sha256']=sha(BEFORE/t['table']);t['after_sha256']=sha(GEN/t['table'])
    assert sources=={p:sha(ROOT/p) for p in SOURCES},'SAVED_INPUT_CHANGED'
    result=dict(schema='v10b-visual-style-v1',sources_sha256=sources,figures=figures,tables=tables,
        supplementary_display_fixes=supplementary,
        legacy_readable_headers=legacy,
        legacy_caption_merges=captions,
        all_figure_arrays_identical=all(r['array_identity'] for r in figures),
        all_table_display_values_identical=all(x['exact_string_identity'] for t in tables for x in t['rows']),
        source_bytes_unchanged=True,new_forecasts=0,new_scores=0,new_inference=0,
        outputs_only=['submission-v10/figures','submission-v10/generated','notes/v10b'],
        method_colors={'full_regression':BLUE,'four_feature':PURPLE,'historical_headroom':VERMILION},
        accessibility_practice='Okabe-Ito CUD palette plus marker/line/position redundancy; sequential white-to-blue cost scale',
        practice_sources=['https://jfly.uni-koeln.de/color/','https://colorspacious.readthedocs.io/en/latest/tutorial.html'])
    (HERE/'visual-style-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['all_figure_arrays_identical','all_table_display_values_identical','source_bytes_unchanged']}))


if __name__=='__main__':
    main()
