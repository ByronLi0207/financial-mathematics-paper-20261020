"""Accounting and archive checks from saved E4 primitives, no new grid or forecasts."""
from pathlib import Path
import csv,hashlib,io,json,zipfile
P=Path('results/v10/cost');summary=json.load(open(P/'summary.json'));cells=json.load(open(P/'cells.json'));d=json.load(open(P/'manifest.json'))['design']
ids=lambda r:tuple(r[k] for k in ('period','normalized_source','horizon','window'))
lookup={ids(r):r for r in cells};count=0
with zipfile.ZipFile(P/'cost-grid.csv.zip') as z:
 assert z.namelist()==['cost-grid.csv']
 for r in csv.DictReader(io.StringIO(z.read('cost-grid.csv').decode())):
  key=(r['period'],r['normalized_source'],int(r['horizon']),int(r['window']));cell=lookup[key]
  a=cell['methods'][r['method_id']];f=cell['methods']['F'];k,b,c=map(float,[r['kappa'],r['beta'],r['c']])
  def cost(s):return k*s['normalized_mean_headroom']+b*s['strict_breach_rate']+c*s['normalized_mean_excess']
  assert float(r['method_mean'])==cost(a) and float(r['reference_mean'])==cost(f)
  delta=cost(a)-cost(f);assert float(r['difference'])==delta and (r['cheaper']=='True')==(delta<0) and (r['equal']=='True')==(delta==0)
  count+=1
assert count==summary['cost_rows']
with (P/'primary-regions.csv').open() as f:rr=list(csv.DictReader(f))
assert len(rr)==98*189==summary['primary_region_rows']
assert len({ids(r) for r in rr})==98
for cell in cells:
 expected=189;assert sum(ids(r)==tuple(str(x) for x in ids(cell)) for r in rr)==expected
assert len(json.load(open(P/'floor-recovery.json')))==summary['floor_recovered_slots']
r=dict(status='PASS',all_cost_rows_accounted=count,all_planned_primary_grid_rows=len(rr),comparison_count=98,whole_cell_statuses={s:sum(x['status']==s for x in cells) for s in {x['status'] for x in cells}},cost_archive_sha256=hashlib.sha256((P/'cost-grid.csv.zip').read_bytes()).hexdigest(),no_new_model_grid_or_forecasts=True)
with (P/'verification.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps(r))
