#!/usr/bin/python3
from pathlib import Path
import hashlib, json, re, runpy, subprocess
R=Path(__file__).resolve().parents[2]
N=Path(__file__).resolve().parent
reader=runpy.run_path(str(R/'notes/v9/writing_check.py'),run_name='read_existing_abstract_metrics')
old=subprocess.check_output(['git','show','3dba6d906fc181be116c0b630ea97fd1a79fee7c:submission-final/manuscript.tex'],cwd=R,text=True)
new=(R/'submission-final/manuscript.tex').read_text()
pattern=re.compile(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',re.S)
def one(source):
    text=pattern.search(source).group(1)
    blob=reader['Blob'](text,[('abstract',1,'')]*len(text))
    plain=reader['plain'](blob).text
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+',plain) if s.strip()]
    return dict(text=plain,words=len(reader['WORD'].findall(plain)),numeric_occurrences=len(reader['NUM'].findall(plain)),sentences=len(sentences),sentence_word_counts=[len(reader['WORD'].findall(s)) for s in sentences])
before,after=one(old),one(new)
assert after['words']<=200 and after['numeric_occurrences']<=5 and after['sentences']==5
assert max(after['sentence_word_counts'])<=40
for term in ('benchmark-default gate','the better realized historical score wins 29 of 34','arm-median'):
    assert term.lower() not in after['text'].lower()
assert pattern.sub('<ABSTRACT>',old)==pattern.sub('<ABSTRACT>',new),'Non-abstract text changed in R1'
(N/'abstract-before.txt').write_text(before['text']+'\n')
(N/'abstract-after.txt').write_text(after['text']+'\n')
result={'step':'R1','status':'PASS','before':before,'after':after,'non_abstract_source_unchanged':True,'new_numeric_findings_added':False}
(N/'R1-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(N/'abstract-comparison.md').write_text('# R1 摘要改写前后\n\n## 改前\n\n'+before['text']+'\n\n## 改后\n\n'+after['text']+'\n\n```json\n'+json.dumps({k:{a:b for a,b in v.items() if a!='text'} for k,v in [('before',before),('after',after)]},ensure_ascii=False,indent=2)+'\n```\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
