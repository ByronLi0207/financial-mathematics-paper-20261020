"""Independent saved-field figure traceability, without replotting or scoring.

Reuses WP2 approval only when exact current source/PDF/style-code bytes match.
For all six MC charts it independently reconstructs every cell annotation from
its explicitly keyed saved summary, rather than testing global number presence.
"""
import argparse,csv,hashlib,json,math,re,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())

def audit_mc(summary,design,receipt):
    problems=[];proof=[]
    keys=lambda r:tuple(r[k] for k in ['method','phi','variance_persistence','window','horizon'])
    rows={keys(row):row for row in summary['cells']}
    expected={(m,phi,p,w,h) for m in design['methods'] for phi in design['phi'] for p in design['variance_persistence'] for w in design['windows'] for h in design['horizons']}
    if len(rows)!=len(summary['cells']) or set(rows)!=expected:problems.append({'code':'SUMMARY_GRID'})
    fields={'loss':('relative_loss_percent','relative_loss_mcse',1.,[-100.,100.]),'breach':('model_breach_rate','model_breach_mcse',100.,[0.,100.]),'win':('win_fraction','win_mcse',100.,[0.,100.])}
    figures={(f['method'],f['metric']):f for f in receipt['figures']}
    if set(figures)!={(m,t) for m in ['QR33','QR4'] for t in fields}:problems.append({'code':'FIGURE_SET'})
    for (method,metric),fig in figures.items():
        value_field,se_field,scale,limits=fields[metric]
        if fig['fixed_color_limits']!=limits:problems.append({'code':'FIXED_SCALE','method':method,'metric':metric})
        seen=[]
        for panel in fig['panels']:
            h,phi=panel['horizon'],panel['phi']
            if panel['windows']!=design['windows'] or panel['persistences']!=design['variance_persistence']:
                problems.append({'code':'PANEL_AXIS_ORDER','method':method,'metric':metric})
            if len(panel['cells'])!=len(design['windows']):problems.append({'code':'PANEL_ROW_COUNT'})
            for wi,line in enumerate(panel['cells']):
                if len(line)!=len(design['variance_persistence']):problems.append({'code':'PANEL_COLUMN_COUNT'})
                for pi,cell in enumerate(line):
                    w=design['windows'][wi];p=design['variance_persistence'][pi];key=(method,phi,p,w,h);seen.append(key)
                    if (cell['window'],cell['variance_persistence'])!=(w,p):problems.append({'code':'CELL_POSITION','identity':key})
                    row=rows.get(key)
                    if row is None:problems.append({'code':'CELL_NOT_IN_SUMMARY','identity':key});continue
                    n,planned=row['complete_repetitions'],row['planned_repetitions'];raw=row.get(value_field);raw_se=row.get(se_field)
                    valid=type(raw) in (int,float) and type(raw_se) in (int,float) and math.isfinite(raw) and math.isfinite(raw_se) and raw_se>=0
                    eligible=n==planned==design['repetitions'] and row['full_procedure_status']=='COMPLETE' and valid
                    value=raw*scale if eligible else None;se=raw_se*scale if eligible else None
                    annotation=f'{value:.1f}\n({se:.1f})' if eligible else f'NA\n{n}/{planned}'
                    for k,v in [('eligible',eligible),('value',value),('mcse',se),('complete_repetitions',n),('planned_repetitions',planned)]:
                        if cell.get(k)!=v:problems.append({'code':'CELL_VALUE_OR_ELIGIBILITY','identity':key,'field':k})
                    if cell['annotation']!=annotation:problems.append({'code':'FIGURE_ANNOTATION','identity':key,'actual':cell['annotation'],'expected':annotation})
                    proof.append(dict(method=method,metric=metric,horizon=h,phi=phi,window=w,variance_persistence=p,summary_field=value_field,mcse_field=se_field,display_scale=scale,display_value=value,display_mcse=se,expected_annotation=annotation,source_complete_repetitions=n))
        expect={(method,phi,p,w,h) for phi in design['phi'] for p in design['variance_persistence'] for w in design['windows'] for h in design['horizons']}
        if len(seen)!=len(expect) or set(seen)!=expect:problems.append({'code':'FIGURE_CELL_COVERAGE','method':method,'metric':metric})
    return problems,proof

def audit(root):
    root=Path(root);errors=[];old=load(root/'notes/revision-v8/wp2-figure-styling.json');old_proof=[]
    code=subprocess.check_output(['git','show','19b1d153:notes/revision-v8/style_figures.py'],cwd=root)
    if hashlib.sha256(code).hexdigest()!=sha(root/'notes/revision-v8/style_figures.py'):errors.append({'code':'OLD_STYLE_CODE_CHANGED'})
    for f in old['figures']:
        for key,path in [('sha256',f['path']),('source_sha256',f['source'])]:
            if sha(root/path)!=f[key]:errors.append({'code':'OLD_SOURCE_OR_FIGURE_HASH','path':path})
        if f['source'].endswith('.json'):
            data=load(root/f['source'])['selection'];xs=data['dates'];ys=[v/1000 for v in data['absolute_positions']];ref=[data['report']/1000]*len(xs)
            if len(xs)!=f['points'] or any(not d.startswith('2021-') for d in xs):errors.append({'code':'EXAMPLE_POINT_COUNT_OR_YEAR'})
            old_proof.append(dict(path=f['path'],source=f['source'],source_sha256=f['source_sha256'],pdf_sha256=f['sha256'],point_count=len(xs),x=xs,y=ys,reference=ref,unit='USD billions',operation='saved USD millions divided by1000; original chronological selection unchanged'))
        else:
            rows=list(csv.DictReader((root/f['source']).open()));scale=f['unit_scale'];xs=[float(r['theta_USD_millions'])*scale for r in rows];ys=[float(r['left_elementary']) for r in rows];ref=[float(r['right_elementary']) for r in rows]
            if len(xs)!=f['points'] or any(not math.isfinite(v) for v in xs+ys+ref):errors.append({'code':'MURPHY_POINT_COUNT_OR_FINITE'})
            old_proof.append(dict(path=f['path'],source=f['source'],source_sha256=f['source_sha256'],pdf_sha256=f['sha256'],point_count=len(xs),x=xs,y=ys,reference=ref,threshold_scale=scale,operation='saved displaygrid only; no elementary-score recomputation or new forecast'))
        if f['scientific_notation'] or any(re.search(r'\de[+-]\d',t,re.I) for t in f['tick_labels']):errors.append({'code':'SCIENTIFIC_TICK'})
    receipt=load(root/'results/revision-v8/wp3/figures/display-receipt.json');summary=load(root/receipt['source']);design=load(root/'protocol/revision-v8/wp3-mechanism-design.json')
    if sha(root/receipt['source'])!=receipt['source_sha256']:errors.append({'code':'MC_SUMMARY_HASH'})
    mc_errors,mc_proof=audit_mc(summary,design,receipt);errors+=mc_errors
    for f in receipt['figures']:
        if sha(root/'results/revision-v8/wp3/figures'/f['pdf'])!=f['pdf_sha256'] or sha(root/'results/revision-v8/wp3/figures'/f['preview'])!=f['preview_sha256']:errors.append({'code':'MC_FIGURE_OR_PREVIEW_HASH','file':f['pdf']})
    current=[]
    for doc in ['manuscript.tex','supplement.tex']:
        names=re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',(root/'submission-jof'/doc).read_text())
        for name in names:current.append((doc,name))
    expected={("manuscript.tex",Path(f['path']).relative_to('submission-jof').as_posix()) for f in old['figures']}|{('manuscript.tex','figures/v8-wp3-qr33-loss.pdf'),('supplement.tex','figures/v8-wp3-qr4-loss.pdf')}
    if len(current)!=5 or set(current)!=expected:errors.append({'code':'CURRENT_INCLUDED_FIGURE_SET','actual':current})
    for doc,name in current:
        if name.startswith('figures/v8-wp3-'):
            f=next(f for f in receipt['figures'] if f['pdf']==Path(name).name)
            if sha(root/'submission-jof'/name)!=f['pdf_sha256']:errors.append({'code':'PAPER_FIGURE_COPY','file':name})
    return dict(checked_utc=datetime.now(timezone.utc).isoformat(),status='FAIL' if errors else 'PASS',scope='Source/byte identity and independently keyed saved-data-to-annotation traceability; actual final-page visual QA is separate.',current_included_figures=current,old_figures_checked=len(old_proof),old_plot_point_vectors=old_proof,all_MC_figures_checked=len(receipt['figures']),MC_cells_independently_checked=len(mc_proof),MC_numeric_annotations_checked=2*len(mc_proof),MC_cell_proof=mc_proof,source_summary_sha256=receipt['source_sha256'],difference_count=len(errors),differences=errors,forecasts_computed=0,new_scores_computed=0,new_simulations=0,global_numeric_presence_used_as_location_proof=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=audit(a.root)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['old_plot_point_vectors','MC_cell_proof']},indent=2));raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
