"""Metadata/index exposure audit only; never opens financial values or fits."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'results/supervisor-20261023/r6/retro-cells.json'
j=json.loads(p.read_text())
g=next(x for x in j['groups'] if all(x['group'].get(k)==v for k,v in
    [('phase','retro'),('source','fx_hourly'),('horizon',24),('window',2880)]))
assert g['selections']['R3']['status']=='SELECTED'
assert all(x['status']=='COMPLETE' for x in g['selections']['R3']['candidates'])
assert next(x for x in g['rows'] if x['report']=='R3')['status']=='COMPLETE'
intervals=[(a,b+24) for a,b in g['r3_fold_bounds']]+[(8999,10438+24)]
merged=[]
for a,b in sorted(intervals):
    if merged and a<=merged[-1][1]+1:merged[-1][1]=max(merged[-1][1],b)
    else:merged.append([a,b])
assert merged==[[3071,10462]]
old=[8999,10438];new=[3071,10438]
overlap=max(0,min(old[1],new[1])-max(old[0],new[0])+1)
assert overlap==1440
out=dict(status='PASS',scope='Public metadata and source-index arithmetic, not new financial analysis',
    source='results/supervisor-20261023/r6/retro-cells.json',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
    R3_selection_status=g['selections']['R3']['status'],R3_complete_candidate_count=len(g['selections']['R3']['candidates']),
    R3_candidate_scored_issue_count=g['selections']['R3']['candidates'][0]['n'],
    old_H24_target_coverage_merged=merged,new_full_prefix_issue_bounds=new,
    new_H24_target_bounds=[new[0],new[1]+24],nested_old_retro_issue_count=overlap,
    fresh_unscored_third_period=False,mismatch='MISMATCH-WP5-01')
path=ROOT/'notes/revision-v8/wp5-prior-exposure-proof.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
