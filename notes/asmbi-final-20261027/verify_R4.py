#!/usr/bin/python3
from pathlib import Path
import hashlib,json,re,runpy,subprocess
R=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
reader=runpy.run_path(str(R/'notes/v9/writing_check.py'),run_name='R4_existing_metric')
pattern=re.compile(r'matched histories and update schedules|completed-label pool|refitting clock|arm[- ]median|benchmark-default|source-specific scales|issue origin|survivor universe|finite-penalty\s+hindsight',re.I)
hits=[]
for p in (R/'submission-final').rglob('*.tex'):
    for m in pattern.finditer(p.read_text()):hits.append({'path':str(p.relative_to(R)),'term':m.group()})
assert not hits,hits
metrics=reader['unified_manuscript_statistics'](R/'submission-final/manuscript.tex')
assert 16<=metrics['average_sentence_words']<=24 and metrics['over_40_words']==0
edits=json.loads((N/'R4-editorial-edits.json').read_text())
comparisons=[]
for item in edits:
    path=item['path'];before=subprocess.check_output(['git','show','3dba6d906fc181be116c0b630ea97fd1a79fee7c:'+path],cwd=R,text=True)
    if path=='submission-final/manuscript.tex':
        before=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:r'\begin{abstract}'+(N/'abstract-after.txt').read_text().strip()+r'\end{abstract}',before,count=1,flags=re.S)
        a=before.index(r'\section{Limitations}');b=before.index(r'\section*{Data and code availability}',a)
        before=before[:a]+(N/'R3-sections-after.tex').read_text()+before[b:]
        (N/'R4-main-before.tex').write_text(before)
    after=(R/path).read_text()
    old=reader['NUM'].findall(before);new=reader['NUM'].findall(after)
    assert sorted(old)==sorted(new),path
    comparisons.append({'path':path,'numeric_tokens':len(old),'numeric_multiset_exact':True})
result={'step':'R4','status':'PASS','forbidden_terms':len(hits),'average_sentence_words':metrics['average_sentence_words'],'over_40_words':metrics['over_40_words'],'flagged_proportion':metrics['flagged_proportion'],'words':metrics['words'],'sentences':metrics['sentences'],'numeric_comparisons':comparisons,'matched_definition':'same completed past outcomes, training-window length and model update times','forecast_time_definition':'record when a limit is issued'}
(N/'R4-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
