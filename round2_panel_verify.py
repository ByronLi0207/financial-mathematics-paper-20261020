"""Independent saved-array arithmetic and source/binding readback; no model fit."""
import os
for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[n]='1'
import json,hashlib,math
import numpy as np
from v3_revision import ROOT,RESULT
out=RESULT/'round2/panel';m=json.loads((out/'selection-manifest.json').read_text());source_count=0;cells=0;methods=0;maximum_error=0
for r in m['series']:
 raw=(ROOT/r['local_raw_path']).read_bytes();assert len(raw)==r['bytes'];assert hashlib.sha256(raw).hexdigest()==r['sha256'];source_count+=1
for key in m['eligible']:
 for h in [6,24]:
  for w in [52,260]:
   r=json.loads((out/'cells'/f'{key}-h{h}-w{w}.json').read_text());assert r['selection_manifest_sha256']==hashlib.sha256((out/'selection-manifest.json').read_bytes()).hexdigest()
   with np.load(ROOT/'.scratch/round2/panel-models'/f'{key}-h{h}-w{w}/numeric-traces.npz') as z:
    assert np.array_equal(z['origins'],np.arange(405,682))
    for a in r['records']:
     assert a['status']=='COMPLETE';cap=z[a['method']];peak=z['peak'];loss=.95*np.maximum(peak-cap,0)+.05*np.maximum(cap-peak,0);mean=math.fsum(map(float,loss))/len(loss);error=abs(mean-a['mean_pinball']);maximum_error=max(maximum_error,error);assert error<=1e-10*max(1,abs(mean));assert int(np.sum(peak>cap))==a['strict_breach_count'];assert len(loss)==a['origin_count']==277;methods+=1
     if a['method'] in ('QR33','C2_QR4'):
      menu=a['candidates'];assert len(menu)==(3 if a['method']=='QR33' else 5);assert all(x['status']=='COMPLETE' and x['origin_count']==52 for x in menu);chosen=min(menu,key=lambda x:(x['mean_pinball'],-x['parameter']));assert chosen['parameter']==a['selected_penalty']
      for d in a['fit_diagnostics']:assert d['latest_label_end']==d['refit_index'] and d['latest_label_end']<=681
   assert r['post_result'] and r['exploratory'];cells+=1
binding=json.loads((ROOT/'protocol/revision-20261023/prospective-parameter-binding.json').read_text())
for path,sha in binding['code_and_design_sha256'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
assert len(binding['parameters'])==52;protocol=(ROOT/'protocol/revision-20261023/prospective-public-release-protocol.md').read_text();assert 'exactly H+1 recorded positions' in protocol
print(json.dumps(dict(source_fingerprint_checks=source_count,cell_checks=cells,method_saved_array_checks=methods,maximum_absolute_mean_loss_error=maximum_error,strict_breach_count_mismatches=0,menu_choice_mismatches=0,maturity_mismatches=0,prospective_bound_entries=len(binding['parameters']),prospective_code_design_hashes_match=True,prospective_target='H+1 positions, h0..H',independent_dealer_replication=False),indent=2))
