"""Saved-display axis-label and grayscale styling only; no model or scoring imports."""
from pathlib import Path
import os,json,hashlib,re,subprocess
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'.scratch/submission/cost-style-final-v2'
OUT.mkdir(exist_ok=False)
os.environ['MPLCONFIGDIR']=str(OUT/'matplotlib-cache')
from pypdf import PdfReader
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
BLUE='#0072B2'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
arr=lambda a:np.asarray(a,dtype=float).tolist()
def setup():
    plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
        'axes.labelsize': 10, 'axes.titlesize': 10.5,
        'xtick.labelsize': 9, 'ytick.labelsize': 9,
        'legend.fontsize': 9, 'pdf.fonttype': 42, 'ps.fonttype': 42,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.unicode_minus': False, 'savefig.facecolor': 'white'})
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
def main():
    rows=json.loads((ROOT/'results/v10/cost/group-regions.json').read_text())
    report=json.loads((ROOT/'results/v10/cost/report-values.json').read_text())
    design=json.loads((ROOT/'results/v10/cost/manifest.json').read_text())['design']
    tags=list(design['primary_method_by_group'])
    setup()
    fig, axes = plt.subplots(3, 2, figsize=(6.25, 7.2))
    fig.subplots_adjust(left=.10, right=.855, top=.91, bottom=.09, hspace=.64, wspace=.38)
    cmap = LinearSegmentedColormap.from_list('OkabeIto_blue_fraction', ['#F1F1F1', BLUE])
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
        ax.set_xlabel(r'Normalized breach charge $\beta$', fontsize=9, labelpad=4)
        ax.set_ylabel(r'Reserve coefficient $\kappa$', fontsize=9, labelpad=4)
        bindings.append(dict(group_label=tag,beta=design['grid']['beta'],kappa=design['grid']['kappa'],
                             lower=a.tolist(),upper=upper.tolist(),complete=rr['complete'],planned=rr['planned']))
    cax=fig.add_axes([.88,.23,.020,.52], label='<colorbar>')
    cb=fig.colorbar(image,cax=cax);cb.set_label('Fraction cheaper than historical headroom',fontsize=9,labelpad=5)
    cb.ax.tick_params(labelsize=8.5)
    fig.suptitle('Normalized report costs: full pre-specified grid at c = 1', fontsize=11, y=.98)
    figure=ROOT/'submission-final/figures/v10-cost-regions.pdf'
    before=ROOT/'submission-v10/figures/v10-cost-regions.pdf'
    fig.savefig(figure,metadata={'CreationDate':None,'ModDate':None})
    fig.savefig(OUT/'after.png',dpi=220)
    def text(p):
        return '\n'.join(page.extract_text() for page in PdfReader(p).pages)
    a,b=text(before),text(figure)
    nums=lambda s:re.findall(r'(?<![A-Za-z])(?:\d*\.)?\d+',s)
    assert nums(a)==nums(b),(nums(a),nums(b))
    normalize=lambda s:re.sub(r'\s+',' ',s).strip()
    assert normalize(a.replace('Breach charge \u03b2 = b/mF','Normalized breach charge \u03b2'))==normalize(b),(a,b)
    source_arrays=[dict(lines=[],offsets=[],segments=[],images=[r['lower']])for r in bindings]
    assert figure_geometry(fig)==source_arrays
    receipt=dict(axis_before='Breach charge beta=b/m_F',axis_after='Normalized breach charge beta',style_only=True,before_sha256=sha(before),after_sha256=sha(figure),numeric_text_tokens=nums(a),numeric_text_equal=True,all_other_pdf_text_equal=True,source_arrays_equal=True,bindings=bindings,source_sha256={str(p.relative_to(ROOT)):sha(p)for p in [ROOT/'results/v10/cost/group-regions.json',ROOT/'results/v10/cost/report-values.json',ROOT/'results/v10/cost/manifest.json']})
    (ROOT/'notes/submission/cost-figure-style-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(numeric_tokens=len(nums(a)),all_equal=True)))
if __name__=='__main__':main()
