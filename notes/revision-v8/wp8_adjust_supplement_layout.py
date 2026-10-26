"""Close reviewed layout defects without changing a number or result row."""
from pathlib import Path
import hashlib,json,re
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];path=ROOT/'submission-jof/supplement.tex'
text=path.read_text();before=text
expected='e9472bb4f2238c4ac941ab4c206bd880a546bc1f2fd7351b94e92c6fd0ac8b28'
assert hashlib.sha256(text.encode()).hexdigest()==expected,'Do not overwrite later edits'
a='The added eight pairwise tests use only raw standard-normal two-sided\nDM-type working references, separate from all original adjusted families.'
b='\\left\\lfloor4(n/100)^{2/9}\\right\\rfloor\\right\\}\\right).\n\\]'
assert text.count(a)==text.count(b)==1
text=text.replace(a,'\\begin{samepage}\n'+a).replace(b,b+'\n\\end{samepage}')
text=text.replace(r'For \(n\) paired loss differences and horizon \(H\),',r'For \(n\) paired losses at horizon \(H\),')
start=text.index('\\paragraph{What is public.}')
route=text.index('\\paragraph{Routes to complete evidence.}')
old=text[start:route]
new=r'''\paragraph{What is public.}
Editable sources, aggregate results, original designs, code and verification
records accompany the paper. Favourable, adverse and failed outputs remain
unchanged, with longer tables linked rather than removed. Source-field
bindings identify every printed aggregate.

\paragraph{What public checking proves.}
Archive checking and document regeneration verify saved aggregates without raw
observations. They establish artifact consistency, not recomputed forecast
accuracy, a new sample, independent replication or journal acceptance.

\paragraph{Full financial replay requires compatible inputs.}
A separately authorized replay requires the original FX member and Treasury
snapshot to match their recorded fingerprints and definitions. Restricted FX
observations and private per-origin forecasts or fitted traces are not
redistributed. Downloaded economic dates are not verified first-release
availability; a matching series name does not establish snapshot identity.

\paragraph{Version-specific entry points.}
The v7 merge preserves canonical supervisor scripts and explicitly named legacy
implementations with their original paths and whole-file identity gates.
Historical contracts retain their original parameters and dates; exact replay
requires the recorded source commit. This edit does not reactivate or reassign
the existing prospective parameter binding.

\paragraph{Resources and software.}
Document assembly uses existing local software and saved results, without
package installation, model fitting, data acquisition, simulation reruns or
parameter searches. The separately executed studies record actual worker time,
resident memory and observed threads, distinct from requested budgets. Tests
use isolated tracked-input copies so synthetic fixtures cannot alter the
scientific archives.

'''
# Every numeric token, URL identifier and old table/math field must survive.
numbers=lambda s:re.findall(r'\d+(?:\.\d+)?',s)
assert numbers(old)==numbers(new)
text=text[:start]+new+text[route:]
assert numbers(before)==numbers(text)
rows=lambda s:[v for v in s.splitlines() if '&' in v and re.search(r'\d',v)]
assert rows(before)==rows(text)
assert re.findall(r'\\\[.*?\\\]',before,re.S)==re.findall(r'\\\[.*?\\\]',text,re.S)
path.write_text(text)
out=dict(checked_utc=datetime.now(timezone.utc).isoformat(),scope='Layout and non-result reproduction prose only',before_source_sha256=expected,after_source_sha256=hashlib.sha256(text.encode()).hexdigest(),all_numeric_tokens_unchanged=True,all_numeric_table_rows_unchanged=True,all_display_math_blocks_byte_identical=True,changes=['Keep the introductory HAC sentences with their bandwidth display; remove lone H, continuation at page start.','Condense repeated availability/replay/resource prose while retaining every rights/vintage/input/independence/prospective-binding/failure constraint and all exact links.'],before_reproduction_prose=old,after_reproduction_prose=new,final_PDF_QA_pending=True,new_financial_computations=0)
(ROOT/'notes/revision-v8/wp8-supplement-layout-source.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'.scratch/revision-v8/wp8-supplement-layout').mkdir(parents=True,exist_ok=False)
print(json.dumps({k:v for k,v in out.items() if k not in ['before_reproduction_prose','after_reproduction_prose']},indent=2))
