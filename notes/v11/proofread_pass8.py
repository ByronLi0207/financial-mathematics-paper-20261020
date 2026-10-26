"""Use one name for each saved error amount, distinct from reserved headroom."""
from pathlib import Path
from datetime import datetime,timezone
import json,re
ROOT=Path(__file__).resolve().parents[2];edits=[]
def edit(path,before,after,reason):
 p=ROOT/path;t=p.read_text();assert t.count(before)==1,(path,before)
 assert re.findall(r'\d+',before)==re.findall(r'\d+',after)
 p.write_text(t.replace(before,after));edits.append(dict(file=path,before=before,after=after,reason=reason,category='language',occurrences=1,numeric_sequence_unchanged=True))
edit('submission-v10/manuscript.tex',
     'Both six-step FX comparisons improve mean overrun and unused allowance.',
     'Both six-step FX comparisons reduce mean underprediction and mean unused allowance.',
     'Use the same names as the saved error decomposition and state the existing lower-error direction explicitly.')
edit('submission-v10/manuscript.tex','Show mean underprediction, mean unused headroom and strict-breach count on the same grid.',
     'Show mean underprediction, mean unused allowance and strict-breach count on the same grid.',
     'Use unused allowance for the overprediction amount; reserved headroom in the cost section is a different quantity.')
before=r'\(R_a=aU+(1-a)V\), where \(U=\operatorname{mean}(P-C)_+\) and'+'\n'+r'\(V=\operatorname{mean}(C-P)_+\).'
after=r'\(R_a=aU+(1-a)V\). Here, \(U=\operatorname{mean}(P-C)_+\) is mean underprediction and'+'\n'+r'\(V=\operatorname{mean}(C-P)_+\) is mean unused allowance.'
edit('submission-v10/supplement.tex',before,after,
     'Name both unchanged mathematical quantities explicitly and align them with the existing table headers; retain their passive-error and all-origin interpretation.')
(ROOT/'notes/v11/proofreading-pass8.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='error-amount-terminology',edits=edits),indent=2)+'\n')
print(len(edits),'recorded wording-only changes')
