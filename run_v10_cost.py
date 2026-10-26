"""Single registered E4 saved-prediction cost run; no forecast or model fit."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,csv,hashlib,io,json,os,subprocess,time,zipfile
ROOT=Path(__file__).resolve().parent
PUBLIC=ROOT/'results/v10/cost'
DESIGN=ROOT/'protocol/v10/cost-design.md'
DESIGN_COMMIT='a112e458500b5dd34e0536074dff77091ab39ed1'
CODE=('run_v10_cost.py','v10_cost.py','v10_cost_inputs.py')
def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def save(p,x):
    with Path(p).open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
def committed(path):
    rel=str(Path(path).relative_to(ROOT));b=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
    if b!=Path(path).read_bytes():raise ValueError('UNCOMMITTED_INPUT:'+rel)
def design():return json.loads(DESIGN.read_text().split('```json\n')[1].split('\n```')[0])
def verify_source():
    import run_v10_mcs as m
    return m.verify_seal(load(ROOT/'results/v10/mcs/manifest.json'),upstream=True)
def seal():
    d=design();subprocess.run(['git','merge-base','--is-ancestor',DESIGN_COMMIT,'HEAD'],cwd=ROOT,check=True)
    for p in [DESIGN,*[ROOT/x for x in CODE],ROOT/d['mcs_index'],ROOT/d['inventory']]:committed(p)
    assert sha(ROOT/d['mcs_index'])==d['mcs_index_sha256'] and sha(ROOT/d['inventory'])==d['inventory_sha256']
    idx=verify_source();assert len(idx['groups'])==d['comparison_count']
    PUBLIC.mkdir(exist_ok=False)
    save(PUBLIC/'manifest.json',dict(design_commit=DESIGN_COMMIT,design_sha256=sha(DESIGN),design=d,code_sha256={x:sha(ROOT/x) for x in CODE},mcs_manifest_sha256=sha(ROOT/'results/v10/mcs/manifest.json'),sealed_utc=utc()))
    print('SEALED98costcomparisoninputs')
def run():
    from v10_cost_inputs import load_cost_group
    from v10_cost import evaluate_costs
    m=load(PUBLIC/'manifest.json');d=m['design'];committed(PUBLIC/'manifest.json')
    assert sha(DESIGN)==m['design_sha256'] and m['design']==design()
    assert sha(ROOT/d['mcs_index'])==d['mcs_index_sha256'] and sha(ROOT/d['inventory'])==d['inventory_sha256']
    assert sha(ROOT/'results/v10/mcs/manifest.json')==m['mcs_manifest_sha256']
    for x,h in m['code_sha256'].items():assert sha(ROOT/x)==h
    idx=verify_source();inventory=load(ROOT/d['inventory'])
    save(PUBLIC/'run-start.json',dict(started_utc=utc(),design_commit=DESIGN_COMMIT,manifest_sha256=sha(PUBLIC/'manifest.json')))
    started=time.monotonic();cells=[];prim=[];regions=[];recover=[];allrows=0
    fields=('period','normalized_source','horizon','window','group_label','method_id','kappa','beta','c','method_mean','reference_mean','difference','cheaper','equal')
    zpath=PUBLIC/'cost-grid.csv.zip'
    with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED) as z:
      with z.open('cost-grid.csv','w') as raw:
       with io.TextIOWrapper(raw,encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fields);writer.writeheader()
        for g in idx['groups']:
            base=dict(g['identity'],group_label=g['group_label']);primary=d['primary_method_by_group'][g['group_label']]
            if time.monotonic()-started>d['run_limit_seconds']:
                cells.append(dict(base,status='UNAVAILABLE',reason='GLOBAL_DEADLINE',known_na=g['unavailable_methods']));continue
            try:
                a=load_cost_group(g,inventory,ROOT)
                result=evaluate_costs(a['capacities'],a['target'],a['floor'],d['reference_id'],d['grid'],primary)
                cell=dict(base,**{k:v for k,v in result.items() if k!='rows'},known_na=g['unavailable_methods'],primary_method=primary)
                recover.extend(dict(base,**x) for x in a['recovery_receipts'])
                cells.append(cell)
                if result['status']!='COMPLETE':continue
                prim.append(dict(base,mean_F_headroom=result['mean_F_headroom'],methods=result['methods']))
                for r in result['rows']:
                    row=dict(base,**r);writer.writerow({k:row[k] for k in fields});allrows+=1
                    if row['method_id']==primary:regions.append(row)
            except Exception as exc:
                cells.append(dict(base,status='UNAVAILABLE',reason=type(exc).__name__+': '+str(exc),known_na=g['unavailable_methods'],primary_method=primary))
    verify_source()
    assert sha(ROOT/d['mcs_index'])==d['mcs_index_sha256'] and sha(ROOT/d['inventory'])==d['inventory_sha256']
    assert sha(ROOT/'results/v10/mcs/manifest.json')==m['mcs_manifest_sha256']
    for x,h in m['code_sha256'].items():assert sha(ROOT/x)==h
    save(PUBLIC/'cells.json',cells);save(PUBLIC/'primitive-stats.json',prim);save(PUBLIC/'floor-recovery.json',recover)
    completed_regions={(tuple(r[k] for k in ('period','normalized_source','horizon','window')),r['kappa'],r['beta'],r['c']):r for r in regions}
    regions=[]
    for cell in cells:
      ident=tuple(cell[k] for k in ('period','normalized_source','horizon','window'))
      for k in d['grid']['kappa']:
       for b in d['grid']['beta']:
        for c in d['grid']['c']:
         r=completed_regions.get((ident,k,b,c))
         if r is not None:regions.append(dict(r,status='COMPLETE',reason=None))
         else:regions.append({**{f:None for f in fields},**{n:cell[n] for n in ('period','normalized_source','horizon','window','group_label')},'method_id':d['primary_method_by_group'][cell['group_label']],'kappa':k,'beta':b,'c':c,'status':'UNAVAILABLE','reason':cell.get('reason') or 'PRIMARY_METHOD_UNAVAILABLE'})
    with (PUBLIC/'primary-regions.csv').open('x',newline='') as f:
        w=csv.DictWriter(f,fields+('status','reason'));w.writeheader();w.writerows(regions)
    summary=[]
    for tag in d['primary_method_by_group']:
        planned=[x for x in idx['groups'] if x['group_label']==tag]
        for c in d['grid']['c']:
          for k in d['grid']['kappa']:
           for b in d['grid']['beta']:
            r=[x for x in regions if x['group_label']==tag and x['c']==c and x['kappa']==k and x['beta']==b and x['status']=='COMPLETE']
            wins=sum(x['cheaper'] for x in r);n=len(planned)
            summary.append(dict(group_label=tag,c=c,kappa=k,beta=b,wins=wins,complete=len(r),planned=n,lower=wins/n,upper=(wins+n-len(r))/n))
    save(PUBLIC/'group-regions.json',summary)
    save(PUBLIC/'summary.json',dict(status='COMPLETE_SAVED_COST_ANALYSIS',comparisons=len(cells),complete=sum(x['status']=='COMPLETE' for x in cells),unavailable=sum(x['status']!='COMPLETE' for x in cells),complete_method_slots=sum(len(x.get('methods',{})) for x in cells if x['status']=='COMPLETE'),grid_points=len(d['grid']['kappa'])*len(d['grid']['beta'])*len(d['grid']['c']),cost_rows=allrows,primary_region_rows=len(regions),floor_recovered_slots=len(recover),ended_utc=utc(),elapsed_seconds=time.monotonic()-started,archive_sha256=sha(zpath),primary_comparator=d['primary_method_by_group']))
    print(json.dumps(load(PUBLIC/'summary.json')))
def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=('seal','run'));a=p.parse_args();{'seal':seal,'run':run}[a.command]()
if __name__=='__main__':main()
