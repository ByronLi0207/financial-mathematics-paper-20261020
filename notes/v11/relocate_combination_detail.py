"""Keep a secondary combination-result detail verbatim in its existing supplement section."""
from pathlib import Path
from datetime import datetime,timezone
import json
ROOT=Path(__file__).resolve().parents[2]
m=ROOT/'submission-v10/manuscript.tex';s=ROOT/'submission-v10/supplement.tex'
detail=r'The median combination lowers Treasury-bill loss by 4.0\%, while the mean combination raises it by 2.8\%.'
mt=m.read_text();st=s.read_text();assert mt.count(detail)==1
anchor=r'\section{Untuned forecast combinations}\label{sup:wp3}'
assert st.count(anchor)==1
m.write_text(mt.replace(' '+detail,''))
s.write_text(st.replace(anchor,anchor+'\n\n'+detail))
record=dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='secondary-combination-relocation',edits=[dict(
 file='submission-v10/manuscript.tex → submission-v10/supplement.tex / S18',before=detail,after=detail,
 occurrences=1,reason='Keep the continuous history subsection and main page cap by moving only this unchanged secondary combination detail to its existing supplement section. The main mixed-results sentence and reference remain.',
 category='layout relocation',numeric_sequence_unchanged=True)])
(ROOT/'notes/v11/proofreading-pass6.json').write_text(json.dumps(record,indent=2)+'\n')
