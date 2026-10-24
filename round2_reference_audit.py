import sys,json,re
from v3_revision import ROOT,plain
for v,p in [('round2_entry_before',ROOT/'.scratch/round2/entry/paper-content.json'),('current_after',ROOT/'manuscript/revision-v3/paper-content.json')]:
 c=json.loads(p.read_text());text='\n'.join(plain(r['html']) for r in c['references'])
 patterns=['Consulted','The PDF names','The institutional award year','no claim of equivalence']
 print(v, json.dumps({k:len(re.findall(re.escape(k),text,re.I)) for k in patterns}))
 for r in c['references']:
  if re.search('|'.join(map(re.escape,patterns)),plain(r['html']),re.I):print(r['id'],plain(r['html']))
g=(ROOT/'REPRODUCIBILITY_V3.md').read_text();print('Original reference-edition notes preserved in guide:', '## Original reference-edition notes retained verbatim' in g, 'Consulted' in g)
assert not re.search('|'.join(map(re.escape,patterns)),'\n'.join(plain(r['html']) for r in c['references']),re.I)
