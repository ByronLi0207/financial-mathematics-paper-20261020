from pathlib import Path
from collections import Counter
import datetime as dt, hashlib, json, re, runpy, subprocess
R=Path(__file__).resolve().parents[2]; N=Path(__file__).resolve().parent
BASE='3dba6d906fc181be116c0b630ea97fd1a79fee7c'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=json.loads((R/'notes/submission/frozen-science.json').read_text())['files']
bad=[x['path'] for x in frozen if not (R/x['path']).is_file() or sha(R/x['path'])!=x['sha256']]
assert not bad,bad
reader=runpy.run_path(str(R/'notes/v9/writing_check.py'),run_name='R8_existing_number_reader')
NUM=reader['NUM']
def plain_numbers(s):
    blob=reader['Blob'](s,[('',1,'')]*len(s))
    return NUM.findall(reader['plain'](blob).text)
main=(R/'submission-final/manuscript.tex').read_text()
before=(N/'R5-main-before.tex').read_text()
stop=r'\section*{Data and code availability}'
a=Counter(plain_numbers(before.split(stop)[0])); b=Counter(plain_numbers(main.split(stop)[0]))
assert a==b,(a-b,b-a)
generated=[]
for p in sorted((R/'submission-final/generated').glob('*.tex')):
    path=str(p.relative_to(R))
    q=subprocess.run(['git','show',BASE+':'+path],cwd=R,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if q.returncode:continue
    without_link_addresses=lambda text:re.sub(r'\\href\{[^}]+\}\{',lambda match:r'\href{URL}{',text)
    assert NUM.findall(without_link_addresses(q.stdout))==NUM.findall(without_link_addresses(p.read_text())),path
    generated.append(dict(path=path,sha256=sha(p),numeric_sequence_exact=True,link_addresses_excluded=True))
# Every compact-supplement literal number has an original-text location.
# This identity check does not recompute any score, percentage, p-value or verdict.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','submission-final'],cwd=R,text=True).splitlines()
locations={};source_hashes={}
for path in paths:
    if not path.endswith(('.tex','.bib')):continue
    raw=subprocess.check_output(['git','show',BASE+':'+path],cwd=R)
    source_hashes[path]=hashlib.sha256(raw).hexdigest()
    for line,text in enumerate(raw.decode().splitlines(),1):
        for value in NUM.findall(text):locations.setdefault(value,dict(source=path,source_sha256=source_hashes[path],line=line,value=value))
supp=(R/'submission-final/supplement.tex').read_text()
bindings=[]
for line,text in enumerate(supp.splitlines(),1):
    for value in NUM.findall(text):
        assert value in locations,(line,value)
        bindings.append(dict(current_source='submission-final/supplement.tex',current_line=line,**locations[value]))
compact=json.loads((N/'R5-compact-register-bindings.json').read_text())
original=(R/'submission-final/generated/submission-predictions.tex').read_text()
for item in compact:
    match=re.search(r'% row_id: '+re.escape(item['row_id'])+r'\n([^\n]+)',original)
    assert match,item['row_id']
    cells=re.split(r'(?<!\\)&',match[1])
    assert item['criterion_tex']==cells[1].strip()+r'\par\emph{Threshold:} '+cells[2].strip()
    assert item['judgment']==cells[4].strip().split(r'\par')[0].strip()
inventory=json.loads((N/'R5-old-section-inventory.json').read_text())['sections']
old=(N/'supplement-before-R5-expanded.tex').read_text(); extended=(R/'EXTENDED_RESULTS.md').read_text()
assert all(old[x['start']:x['end']] in extended for x in inventory)
panel=(R/'submission-final/generated/v12-data-table.tex').read_text()
panel=panel[panel.index(r'\textit{Panel A.'):panel.index(r'\par\vspace{7pt}')]
assert panel in supp
cover=(R/'submission-final/cover-letter.tex').read_text().split(r'\begin{document}')[1]
cover=re.sub(r'\\setlength\{[^}]+\}\{[^}]+\}','',cover)
assert not plain_numbers(cover)
result=dict(status='PASS',checked_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            mismatch_count=0,frozen_files=len(frozen),frozen_mismatches=[],
            main_numeric_multiset_exact_to_R5_before=True,main_numeric_tokens=sum(b.values()),
            generated_tables_and_sections=generated,supplement_numeric_occurrences_bound=len(bindings),
            original_register_criteria_thresholds_and_judgments_exact=len(compact),
            original_sections_retained_exact=len(inventory),source_summary_panel_exact=True,
            cover_numeric_occurrences=0,base=BASE,
            boundary='No statistic or original verdict recomputed. Main scientific numbers compared exactly; compact supplement copied original values/proofs/table cells and retains the complete previous source.',
            supplement_bindings=bindings)
(N/'R8-number-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'supplement_bindings','generated_tables_and_sections'}}|{'generated_files':len(generated)},indent=2))
