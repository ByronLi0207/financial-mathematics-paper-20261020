"""Move an unchanged secondary robustness paragraph to its existing supplement section."""
from pathlib import Path
from datetime import datetime,timezone
import json
ROOT=Path(__file__).resolve().parents[2]
m=ROOT/'submission-v10/manuscript.tex';s=ROOT/'submission-v10/supplement.tex'
nav=r'Supplement Sections S20--S21 and S26 report the state, target-level and overlapping full-prefix comparisons (Tables S19--S21 and S25--S26).'
detail=r'Full-prefix regression lowers matched loss by 12.2\% but records 416 versus 282 breaches. Its rolling-reference DM p-value is 0.055. Longer-horizon gains coexist with reference-sensitive losses in the complete tables.'
mt=m.read_text();st=s.read_text();assert mt.count(nav+' '+detail)==1
anchor=r'\input{generated/v8-three-window-table.tex}'
assert st.count(anchor)==1
m.write_text(mt.replace(nav+' '+detail,nav))
s.write_text(st.replace(anchor,detail+'\n\n'+anchor))
record=dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='secondary-robustness-relocation',edits=[dict(
 id='LAYOUT-S26',file='submission-v10/manuscript.tex → submission-v10/supplement.tex / S26',
 before=detail,after=detail,occurrences=1,reason='The language pass made the main draft 21 pages. Move this unchanged secondary full-prefix result paragraph to its existing supplement section, as authorized; keep the main navigation sentence and all result values.',category='layout relocation',numeric_sequence_unchanged=True)])
(ROOT/'notes/v11/proofreading-pass4.json').write_text(json.dumps(record,indent=2)+'\n')
print('Moved exact secondary-result paragraph to S26; no value or conclusion changed.')
