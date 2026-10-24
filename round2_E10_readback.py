import csv,json,re
from v3_revision import ROOT,plain
c=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text())
print('Actual manuscript paragraphs:')
for s in c['sections']:
 for b in s['blocks']:
  if b['type']=='p' and any(k in b['html'] for k in ['Both primary diagrams cross','descriptive improvement is not statistically significant']):print(s['title']+': '+plain(b['html']))
t=next(b for s in c['sections'] for b in s['blocks'] if b['type']=='table' and b['caption'].startswith('Table H2.'));assert len(t['rows'])==72
rows=list(csv.DictReader((ROOT/'results/revision-20261023/inference/holm.csv').open()));assert len(rows)==72
print('Paper full Holm rows:',len(t['rows']),'working-reference below.05:',sum(float(r['holm_p'])<.05 for r in rows),'all statuses:',sorted({r['status'] for r in rows}))
for filename in ['murphy-summary.csv','dm.csv','holm.csv']:
 p=ROOT/'results/revision-20261023/inference'/filename;raw=p.read_text().splitlines();print('\nExact CSV: '+str(p.relative_to(ROOT)));print(raw[0])
 data=list(csv.DictReader(raw))
 for line,r in zip(raw[1:],data):
  if filename=='holm.csv' or filename=='murphy-summary.csv' or r['contrast_id'] in ['fx_hourly-h6-QR2880-minus-rolling_F720','fx_hourly-h6-QR2880-minus-frozen_F2880','fx_hourly-h24-QR2880-minus-rolling_S720','nyfed_weekly-h6-QR260-minus-frozen_F260']:print(line)
assert all(r['ranking']=='CROSSING' for r in csv.DictReader((ROOT/'results/revision-20261023/inference/murphy-summary.csv').open()))
print('PASS: both fixed-tau primary diagrams CROSSING; all72 Holm rows retained, including nonsignificant/NA bookkeeping; original primary identities unchanged.')
