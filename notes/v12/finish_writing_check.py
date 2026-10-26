"""Assemble final prose and exact frozen writing-statistic acceptance."""
from pathlib import Path
import re,json,datetime,subprocess
R=Path(__file__).resolve().parents[2];D=R/'submission-v10';N=R/'notes/v12';s=(D/'manuscript.tex').read_text();before=subprocess.check_output(['git','show','452064866c2bdc4166b89d09d67b0cb2bc0ae415:submission-v10/manuscript.tex'],cwd=R).decode()
def abstract(t):return re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',t,re.S).group(1)
def sentences(t):return re.split(r'(?<=[.!?])\s+(?=[A-Z])',t)
a,b=sentences(abstract(before)),sentences(abstract(s));assert len(a)==len(b);changed=[i+1 for i,(x,y)in enumerate(zip(a,b))if x!=y];assert len(changed)<=2
labels={}
aux=(R/'.scratch/v12/native-pass4/main/main.aux').read_text()
for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}',aux):labels[m.group(1)]=m.group(2)
def prose(t):
 t=re.sub(r'\\ref\{([^}]+)\}',lambda m:labels[m.group(1)],t)
 t=t.replace('\\%','%').replace('~',' ').replace('---','—').replace('--','–')
 for command in ['textit','textbf','emph']:
  t=re.sub(r'\\'+command+r'\{([^{}]*)\}',r'\1',t)
 return t.strip()
contrib=s.split('The paper makes three empirical findings.',1)[1].split('Section~\\ref{sec:target}',1)[0].strip()
conclusion=s.split('\\section{Conclusion}\\label{sec:conclusion}',1)[1].split('\\FloatBarrier',1)[0].strip()
low=s.split('\\subsection{Why does regression lose at low frequency?}\\label{sec:v12-low-frequency}',1)[1].split('\\subsection{Scores and breach behavior',1)[0]
lowbody=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '',low,flags=re.S).split('\\begin{table}',1)[0].strip()
f=N/'final-prose.md';assert not f.exists();f.write_text('# v12最终正文摘录\n\n## Abstract\n\n'+prose(abstract(s))+'\n\n## Contributions\n\n'+prose(contrib)+'\n\n## Why does regression lose at low frequency?\n\n'+prose(lowbody)+'\n\n## Conclusion\n\n'+prose(conclusion)+'\n')
r=json.loads((N/'writing-final.json').read_text());passed=dict(caution_at_most8_percent=r['flagged_proportion']<=.08,average15_to20=15<=r['average_sentence_words']<=20,none_over40=r['over_40_words']==0,abstract_at_most180=r['abstract_words']<=180,abstract_at_most8_numbers=r['abstract_numeric_occurrences']<=8,at_most2_abstract_sentences_changed=len(changed)<=2)
assert all(passed.values())
report=dict(status='PASS_V12_WRITING_REQUIREMENTS',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),acceptance=passed,changed_abstract_sentence_positions=changed,scope='Unchanged original checker; every new prose paragraph inlined into main source. Numeric targets follow current v12 task.',legacy_literal_code_hits_explanation='Five old forbidden matches are legitimate Supplement S1–S3 cross-references, not method/workflow codes. Raw counter retained without relaxation.',metrics=dict(before=json.loads((N/'writing-before.json').read_text()),after=r),findings_order=['Matched FX gain with reference-sensitive rankings/history','Weekly competitiveness, finite-menu diagnostic and selection losses, bounded simulation comparison','Illustrative reserve/breach cost preferences'])
(N/'writing-acceptance.json').write_text(json.dumps(report,indent=2)+'\n');print(passed,changed)
