"""Post-run integrity only; never calls MCS or forecasts."""
from pathlib import Path
import json,hashlib,zipfile
import run_v10_mcs as driver
root=Path.cwd(); p=root/'results/v10/mcs'
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.load(open(p/'manifest.json')); idx=driver.verify_seal(m,upstream=True)
rows=json.load(open(p/'full-cells.json')); summary=json.load(open(p/'summary.json'))
assert len(rows)==len(idx['groups'])==98
checked=0
for g,r in zip(idx['groups'],rows):
    assert r['identity']==g['identity']
    if r['status'].startswith('COMPLETE'):
        ids={x['method_id'] for x in g['methods']}
        assert set(r['method_ids'])==ids==set(r['pvalues'])
        assert set(r['included']).isdisjoint(r['excluded'])
        assert set(r['included'])|set(r['excluded'])==ids
        assert set(r['included'])=={k for k,v in r['pvalues'].items() if v>.10}
        for eq in r['unique_loss_groups']:
            assert len({r['pvalues'][x] for x in eq['members']})==1
        checked+=len(ids)
zmeta=json.load(open(p/'formal/units-manifest.json'));zpath=p/'formal/units.zip'
assert sha(zpath.read_bytes())==zmeta['archive_sha256']
with zipfile.ZipFile(zpath) as z:
    assert set(z.namelist())=={x['path'] for x in zmeta['files']}
    for x in zmeta['files']:
        b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256'];assert b==(p/'formal/units'/x['path']).read_bytes()
receipt=dict(status='PASS',comparisons=len(rows),complete_method_pvalues_verified=checked,archive_members=len(zmeta['files']),input_and_code_seal_verified=True,no_bootstrap_or_forecast_recalculation=True,summary_sha256=sha((p/'summary.json').read_bytes()),archive_sha256=zmeta['archive_sha256'])
with (p/'verification.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
