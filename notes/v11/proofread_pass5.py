"""Apply only the small spacing and grammar defects seen in rendered-page review."""
from pathlib import Path
from datetime import datetime,timezone
import json,re
ROOT=Path(__file__).resolve().parents[2];edits=[]
def patch(path,before,after,reason,category='language'):
 p=ROOT/path;t=p.read_text();assert t.count(before)==1,(path,before)
 assert re.findall(r'\d+',before)==re.findall(r'\d+',after)
 p.write_text(t.replace(before,after));edits.append(dict(file=path,before=before,after=after,reason=reason,category=category,occurrences=1,numeric_sequence_unchanged=True))
for a,b in [('minimum-validation-\nloss','minimum-validation-loss'),('conditional-\nmoment','conditional-moment'),('target-\nlevel','target-level'),('equal-\nweight','equal-weight')]:
 patch('submission-v10/supplement.tex',a,b,'Join a compound split by a source newline that printed an unintended space after the hyphen.')
patch('submission-v10/generated/v10-mcs-main.tex','All planned comparisons complete, so',
      'All planned comparisons are complete, so','Supply the missing verb in the MCS table note; all saved counts remain unchanged.')
# The FloatBarrier was applied immediately after the rendered interruption was reported.
edits.append(dict(file='submission-v10/manuscript.tex',before=r'\subsection{How much history does FX regression need?}',
                 after='\\FloatBarrier\n'+r'\subsection{How much history does FX regression need?}',
                 reason='Keep the preceding FX table before the history subsection so it cannot interrupt its single paragraph.',
                 category='layout',occurrences=1,numeric_sequence_unchanged=True))
(ROOT/'notes/v11/proofreading-pass5.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='rendered-page-proofreading',edits=edits),indent=2)+'\n')
print(len(edits),'recorded changes')
