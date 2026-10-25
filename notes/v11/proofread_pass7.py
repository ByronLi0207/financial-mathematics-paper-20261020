"""Final terminology and already-registered comparison-scope clarifications; no numerical edits."""
from pathlib import Path
from datetime import datetime,timezone
import json,re
ROOT=Path(__file__).resolve().parents[2];edits=[]
def change(path,before,after,why,category='language'):
 p=ROOT/path;t=p.read_text();n=t.count(before);assert n>0,(path,before)
 assert re.findall(r'\d+',before)==re.findall(r'\d+',after)
 p.write_text(t.replace(before,after));edits.append(dict(file=path,before=before,after=after,occurrences=n,reason=why,category=category,numeric_sequence_unchanged=True))
for p in ['submission-v10/manuscript.tex','submission-v10/supplement.tex','submission-v10/generated/v8-daily-results-table.tex']:
 for a,b in [('Parsimonious regression','Four-feature regression'),('parsimonious','four-feature')]:
  if a in(ROOT/p).read_text():change(p,a,b,'Use the same four-feature method name in definitions, prose and table captions; original method IDs stay unchanged.')
caption_before='Saved confirmation criteria under additional synthetic innovation laws.'
caption_after='Saved confirmation criteria for excess loss relative to matched historical headroom under additional synthetic innovation laws.'
note_before='History regions use the method-specific thresholds fixed in the linked original design, conditional on the earlier threshold exercise.'
note_after='History regions use the method-specific thresholds fixed in the linked original design, conditional on the earlier threshold exercise; the history index excludes predictor dimension.'
for p,category in [('submission-v10/generated/v11-confirmation.tex','language'),('notes/v11/build_history_display.py','display wording mirror')]:
 change(p,caption_before,caption_after,'State the already-defined matched historical reference explicitly; WP2 protocol fixes the paired F denominator.',category)
 change(p,note_before,note_after,'Carry the original WP2 design caveat that its history index excludes predictor dimension into the table note; retain the unequal-menu caveat.',category)
record=dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='canonical-model-name-and-source-scope',source='evidence/v11/pr5-v9/protocol/revision-v9/wp2-confirmatory.md, statistical-unit and writing-boundary paragraphs',edits=edits)
(ROOT/'notes/v11/proofreading-pass7.json').write_text(json.dumps(record,indent=2)+'\n')
print(len(edits),'change groups',sum(x['occurrences']for x in edits),'occurrences')
