"""Rebuild all six main tables and four figures from saved public results.

No acquisition, raw financial observations, fits, scores, HAC, bootstrap or
scientific summary recomputation. Existing outputs are never overwritten.
Requires an already available Python environment with numpy and matplotlib.
"""
from pathlib import Path
import argparse,csv,hashlib,importlib.util,json,os,re,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())
def at(value,pointer):
    for token in pointer.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~');value=value[int(token)] if isinstance(value,list) else value[token]
    return value

def read_bound(record,root=ROOT):
    root=Path(root).resolve();p=(root/record['source']).resolve()
    if not p.is_relative_to(root):raise ValueError('SOURCE_OUTSIDE_REPOSITORY')
    raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if record.get('source_sha256',digest)!=digest:raise ValueError('SOURCE_HASH_MISMATCH:'+str(p))
    if record['format']=='json':value=at(json.loads(raw),record['pointer'])
    elif record['format']=='csv':
        matches=[r for r in csv.DictReader(raw.decode('utf-8-sig').splitlines()) if all(r[k]==str(v) for k,v in record['where'].items())]
        if len(matches)!=1:raise ValueError('CSV_SELECTOR_NOT_UNIQUE')
        value=matches[0][record['field']]
    else:raise ValueError('UNSUPPORTED_FIELD_FORMAT')
    if value!=record['value'] or type(value) is not type(record['value']):raise ValueError('SOURCE_VALUE_MISMATCH')
    return value,digest

def create_output(path):Path(path).mkdir(parents=True,exist_ok=False)

def cftc_rows(summary):
    if summary['primary_verdict']!='PARTLY':raise ValueError('SAVED_VERDICT_CHANGED')
    settings=[('P1_QR33','P1','Full regression',r'$c<r^*/2$'),('P1_QR4','P1','Four predictors',r'$c<r^*/2$'),('P2_QR4','P2','Four predictors',r'$c>2r^*$'),('P2_QR33','P2','Full regression','No eligible high-region cell'),('P3_QR4','P3','Four predictors','Strict fall at both history steps')]
    statuses={'SUPPORT':'Supported','NOT_SUPPORT':'Not supported','NOT_TESTABLE':'Not testable'};rows=[]
    for key,name,method,region in settings:
        r=summary['tests'][key];count='$'+str(r['successes'])+'/'+str(r['planned'])+'$' if r['planned'] else 'NA'
        rows.append(' & '.join([name,method,region,count,statuses[r['status']]])+r'\\')
    return rows

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def substitute(template,spec,bindings):
    def replace(m):
        key,form=m.group(1),m.group(2) or '';r=spec['operands'][key];value,digest=read_bound(r)
        if form in ('set','mathset'):
            rendered=r'\{'+','.join(r'\infty' if v=='inf' else format(float(v),'g') for v in value)+r'\}'
        elif form:rendered=format(float(value),form)
        else:rendered=str(value)
        bindings.append(dict(id=key,source=r['source'],source_sha256=digest,pointer=r.get('pointer'),where=r.get('where'),field=r.get('field'),value=value,format=form,display=rendered));return rendered
    return re.sub(r'@@([A-Z0-9_]+)(?:\|([^@]*))?@@',replace,template)

def mcs_rows(report):
    result=[]
    def metric(x):
        return r'\makebox[3.2em][r]{'+str(x['count_successful'])+'/'+str(x['denominator_successful'])+r'} (\makebox[2.9em][r]{'+format(100*x['fraction_successful'],'.1f')+r'}\%)'
    for row in report['groups']:
        cond=row['conditional_exclusion'];conditional=dict(count_successful=cond['excluded_slots'],denominator_successful=cond['successful_complete_slots'],fraction_successful=cond['fraction_successful'])
        label=row['group_label'].replace('FX early2015','FX earlier period').replace('Same-record dailyFX','Same-record daily FX')
        result.append(' & '.join([label,str(row['successful_comparisons'])+'/'+str(row['planned_comparisons']),metric(row['metrics']['matched_FI_membership']),metric(row['metrics']['literal_sole_FI']),metric(conditional),str(row['unavailable_method_slots'])])+r' \\')
    return result

def table_rows(text):
    body=text.split(r'\midrule',1)[1].split(r'\bottomrule',1)[0]
    return [[x.strip() for x in row.strip().split('&')] for row in body.split(r'\\') if row.strip()]

def tables(out,spec):
    bindings=[];result={}
    data=module('final_display_descriptives',ROOT/'report_v12_descriptives.py')
    tex,source_bindings=data._table(load(ROOT/'results/v12/descriptives/summary.json'),load(ROOT/'results/v12/descriptives/metadata.json'))
    tex=tex.replace(r'p{.13\linewidth}p{.08\linewidth}',r'p{.13\linewidth}p{.09\linewidth}')
    result['table01-data']=tex
    for key in ['table02-methods','table03-fx','table04-weekly']:result[key]=substitute(spec['templates'][key],spec,bindings)
    result['table05-mcs']=spec['templates']['table05-mcs'].replace('@@ROWS@@','\n'.join(mcs_rows(load(ROOT/'results/v10/mcs/report-values.json'))))
    result['table06-cftc']=spec['templates']['table06-cftc'].replace('@@ROWS@@','\n'.join(cftc_rows(load(ROOT/'results/final-merge/wp2-cftc-mechanism/summary.json'))))
    current=(ROOT/'submission-final/manuscript.tex').read_text();blocks=re.findall(r'\\begin\{table\}.*?\\end\{table\}',current,re.S)
    for key,label in [('table02-methods','tab:methods'),('table03-fx','tab:fx'),('table04-weekly','tab:weekly'),('table06-cftc','tab:cftc-mechanism')]:
        expected=next(b for b in blocks if '\\label{'+label+'}' in b)
        if table_rows(result[key])!=table_rows(expected):raise ValueError('CURRENT_TABLE_CELL_MISMATCH:'+key)
    for key,file in [('table01-data','v12-data-table.tex'),('table05-mcs','v10-mcs-main.tex')]:
        if table_rows(result[key])!=table_rows((ROOT/'submission-final/generated'/file).read_text()):raise ValueError('CURRENT_GENERATED_TABLE_MISMATCH:'+key)
    if result['table01-data'].strip()!=(ROOT/'submission-final/generated/v12-data-table.tex').read_text().strip():raise ValueError('COMPLETE_DATA_TABLE_PANELS_OR_NOTES_MISMATCH')
    for key,tex in result.items():
        if '@@' in tex:raise ValueError('UNRESOLVED_TABLE_TOKEN')
        (out/(key+'.tex')).write_text(tex+'\n')
    return dict(tables=6,source_field_bindings=bindings,data_table_display_bindings=source_bindings,actual_current_table_cells_match=True)

def endpoint(out):
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter,MaxNLocator
    source=load(ROOT/'notes/v7/example-selection.json')['selection'];old=next(r for r in load(ROOT/'results/v9/figures/scalars.json')['figures'] if r.get('pdf','').endswith('/v9-endpoint-peak-example.pdf'))
    if any(source[k]!=old[k] for k in ['absolute_positions','dates','report']):raise ValueError('ENDPOINT_SAVED_SOURCE_MISMATCH')
    plt.rcParams.update({'font.family':'serif','font.size':10,'axes.labelsize':10,'axes.titlesize':10.5,'xtick.labelsize':9,'ytick.labelsize':9,'legend.fontsize':9,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'savefig.facecolor':'white'})
    x=np.arange(len(source['dates']));y=np.array(source['absolute_positions']);limit=np.full(len(x),source['report'])
    fig,ax=plt.subplots(figsize=(6.25,3.25));ax.plot(x,y,color='#0072B2',marker='o',ms=4,lw=1.6,label='Observed absolute position');ax.plot(x,limit,color='#222222',marker='s',markevery=[0,6],ms=3.6,linestyle='--',lw=1.6,label='Historical headroom limit');ax.set_xticks(x,[d[5:] for d in source['dates']]);ax.set(xlabel='Economic date (2021)',ylabel='Absolute position (USD millions)');ax.yaxis.set_major_locator(MaxNLocator(nbins=5));ax.yaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v:,.0f}'));ax.grid(axis='y',color='0.88',lw=.55);ax.set_axisbelow(True);ax.tick_params(length=3,width=.7);ax.legend(loc='lower center',bbox_to_anchor=(.5,1.015),ncol=1,frameon=False);fig.subplots_adjust(left=.145,right=.98,bottom=.185,top=.765)
    observed=[dict(x=line.get_xdata().tolist(),y=line.get_ydata().tolist()) for line in ax.lines]
    expected=[dict(x=x.tolist(),y=y.tolist()),dict(x=x.tolist(),y=limit.tolist())]
    if observed!=expected:raise ValueError('ENDPOINT_ARTIST_MISMATCH')
    fig.savefig(out/'figure01-endpoint.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(out/'figure01-endpoint.png',dpi=220);plt.close(fig)
    return dict(source='notes/v7/example-selection.json',source_sha256=sha(ROOT/'notes/v7/example-selection.json'),dates=source['dates'],actual_artist_lines=observed,new_statistics=0)

def parser():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('final-display-rebuild'));return p

def build(output):
    output=Path(output).resolve()
    for folder in ['results','protocol','data','submission-final','submission-jof','submission-v10','archive','notes']:
        if output.is_relative_to(ROOT/folder):raise ValueError('OUTPUT_INSIDE_PRESERVED_SOURCE_TREE')
    create_output(output);os.environ['MPLCONFIGDIR']=str(output/'matplotlib-cache')
    spec=load(ROOT/'notes/final-merge/wp7-display-spec.json');(output/'tables').mkdir();(output/'figures').mkdir();table_receipt=tables(output/'tables',spec);fig1=endpoint(output/'figures');commands=[]
    for cmd in [[sys.executable,'-B',str(ROOT/'report_v12_decomposition.py'),'--output-dir',str(output/'decomposition')],[sys.executable,'-B',str(ROOT/'plot_final_merge_figures.py'),'--output',str(output/'unified-and-decision')]]:
        r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);commands.append(dict(command=cmd,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr))
        if r.returncode:raise RuntimeError('SAVED_DISPLAY_CHILD_FAILED:'+r.stdout+r.stderr)
    for original,name in [('decomposition/decomposition.pdf','figure02-decomposition.pdf'),('decomposition/decomposition.png','figure02-decomposition.png'),('unified-and-decision/unified-history.pdf','figure03-history.pdf'),('unified-and-decision/unified-history.png','figure03-history.png'),('unified-and-decision/decision-map.pdf','figure04-decision.pdf'),('unified-and-decision/decision-map.png','figure04-decision.png')]:shutil.copyfile(output/original,output/'figures'/name)
    frozen_points=load(ROOT/'results/final-merge/wp3-figures/render-v4/points.json');rebuilt_points=load(output/'unified-and-decision/points.json')
    if rebuilt_points!=frozen_points:raise ValueError('ALL482_FROZEN_POINTS_MISMATCH')
    result=dict(status='PASS',operation='Saved public field formatting and plotting only; no raw financial source access, model fit, loss/HAC/bootstrap rerun or new scientific summary.',table_count=6,figure_count=4,new_model_fits=0,new_statistics=0,all_482_points_match=True,tables=table_receipt,endpoint=fig1,commands=commands,artifacts=[dict(path=str(p.relative_to(output)),bytes=p.stat().st_size,sha256=sha(p)) for folder in ['tables','figures'] for p in sorted((output/folder).iterdir())])
    (output/'rebuild-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('tables','endpoint','commands','artifacts')},indent=2));return result

if __name__=='__main__':build(parser().parse_args().output)
