#!/usr/bin/python3
from pathlib import Path
from collections import Counter
import hashlib,json,re,runpy
R=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
report=json.loads((R/'submission-package/ASMBI/build-report.json').read_text())
assert report['status']=='COMPILED_PENDING_VISUAL_QA'
assert all(x['status']=='COMPILED' for x in report['outputs'].values())
info=report['outputs']['supplement'];assert info['pages']<=30
source=(R/'submission-final/supplement.tex').read_text()
body=source.split(r'\begin{document}',1)[1]
assert len(re.findall(r'\\section\{',body))==12
labels=set(re.findall(r'\\label\{([^}]+)\}',body))
refs=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',body))
assert not refs-labels,sorted(refs-labels)
log=(R/info['log']).read_text()
assert not re.search(r'LaTeX Warning: (?:Reference|Citation).*undefined|There were undefined references',log)
aux=(R/info['log']).with_suffix('.aux').read_text()
auxlabels={m.group(1):m.group(2) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}',aux)}
mapping=json.loads((N/'R5-section-map.json').read_text())
inventory=json.loads((N/'R5-old-section-inventory.json').read_text())['sections']
archive=(R/mapping['archived_source']).read_text()
assert hashlib.sha256(archive.encode()).hexdigest()==mapping['archived_source_sha256']
extended=(R/'EXTENDED_RESULTS.md').read_text()
for item in inventory:
    chunk=archive[item['start']:item['end']]
    assert chunk in extended,item['old_section']
    assert auxlabels[item['label']]=='S'+str(mapping['old_to_new_section'][str(item['old_section'])])
# Both proof texts remain intact in the compact version, not only in the archive.
for item in inventory[:2]:
    chunk=archive[item['start']:item['end']]
    chunk=re.sub(r'^\\section\{[^}]+\}\\label\{[^}]+\}','',chunk).strip()
    chunk=re.sub(r'\\(?:clearpage|FloatBarrier)\s*$','',chunk).strip()
    assert chunk in body,item['label']
rows=json.loads((N/'R5-compact-register-bindings.json').read_text())
register=json.loads((R/'notes/submission/prediction-register.json').read_text())
assert {x['row_id'] for x in rows}=={x['row_id'] for x in register['rows']}
counts=Counter(x['judgment'] for x in rows)
assert counts=={'Supported':20,'Not supported':11,'Undetermined':5},counts
main=(R/'submission-final/manuscript.tex').read_text()
macro=re.search(r'\\newcommand\{\\vthirteenMCSTable\}\{([^}]+)\}',main).group(1)
assert macro==auxlabels['tab:v10-mcs-main']
assert auxlabels['fig:murphyfx']=='S2' and auxlabels['fig:murphybill']=='S3'
for m in re.finditer(r'\bSections?\s+(S\d+)(?:--(S\d+))?',main):
    assert 1<=int(m.group(1)[1:])<=12
    if m.group(2):assert 1<=int(m.group(2)[1:])<=12
reader=runpy.run_path(str(R/'notes/v9/writing_check.py'),run_name='R5_numeric_reader')
def nums(s):
    s=s.split(r'\begin{thebibliography}',1)[0]
    blob=reader['Blob'](s,[('',1,'')]*len(s))
    return reader['NUM'].findall(reader['plain'](blob).text)
oldnums=nums((N/'R5-main-before.tex').read_text());newnums=nums(main)
assert Counter(oldnums)==Counter(newnums),(Counter(oldnums)-Counter(newnums),Counter(newnums)-Counter(oldnums))
out={'step':'R5','status':'PASS','supplement_pages':info['pages'],'supplement_sections':12,'unresolved_internal_references':0,'archived_old_sections_exact':len(inventory),'complete_original_supplement_preserved':True,'both_complete_proof_texts_retained':True,'compact_register_rows':len(rows),'saved_judgments':dict(counts),'confidence_set_table':macro,'murphy_figures':[auxlabels['fig:murphyfx'],auxlabels['fig:murphybill']],'main_factual_numeric_multiset_exact':True,'visual_review':'scheduled for R8 final PDFs; no claim of completed visual review here'}
(N/'R5-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
