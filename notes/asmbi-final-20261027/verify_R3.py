#!/usr/bin/python3
from pathlib import Path
import json, re, runpy
R=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
reader=runpy.run_path(str(R/'notes/v9/writing_check.py'),run_name='read_existing_R3_metrics')
before=(N/'R3-sections-before.tex').read_text();after=(N/'R3-sections-after.tex').read_text()
def parts(text):
    limited,conclusion=text.split(r'\section{Conclusion}',1)
    return limited,conclusion
lim,con=parts(after)
assert r'\begin{itemize}' not in lim
for text in (lim,con):
    assert not re.search(r'finite-penalty hindsight bound|survivor universe|Supplement Section S(?:36|40)|arm-median|benchmark-default',text,re.I)
body=lambda s:re.sub(r'\\section\{[^}]+\}|\\label\{[^}]+\}|\\FloatBarrier','',s).strip()
lim_pars=[x for x in body(lim).split('\n\n') if x.strip()]
con_pars=[x for x in body(con).split('\n\n') if x.strip()]
assert len(lim_pars)==3 and len(con_pars)==2
strip_layout=lambda s: re.sub(r'\\setlength\{[^}]+\}\{[^}]+\}', '', s)
old_nums=reader['NUM'].findall(strip_layout(before));new_nums=reader['NUM'].findall(strip_layout(after))
assert sorted(old_nums)==sorted(new_nums),(old_nums,new_nums)
assert 'inspected before conditional models' in lim and 'retrospective' in lim
assert 'unmeasured' in lim and 'one market maker' in lim and '6 of 10' in lim
assert not re.search(r'retrospect|inspected|rejected|coverage guarantee|stipulated|unmeasured',con,re.I)
result={'step':'R3','status':'PASS','limitations_paragraphs':len(lim_pars),'conclusion_paragraphs':len(con_pars),'forbidden_terms':0,'factual_numeric_tokens_before':old_nums,'factual_numeric_tokens_after':new_nums,'numeric_multiset_exact':True,'all_three_research_questions_answered':all('RQ'+str(x) in con for x in (1,2,3))}
(N/'R3-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(N/'R3-comparison.md').write_text('# R3 局限与结论前后对照\n\n## 改前\n\n```tex\n'+before+'\n```\n\n## 改后\n\n```tex\n'+after+'\n```\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
