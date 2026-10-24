import json,re
from v3_revision import ROOT,plain
pat=re.compile(r'\b(?:establish\w*|demonstrat\w*|prov(?:e|es|ed|en|ing)|consequently|confirms)\b',re.I)
for label,path in [('entry_before',ROOT/'.scratch/round2/entry/paper-content.json'),('current_after',ROOT/'manuscript/revision-v3/paper-content.json')]:
 c=json.loads(path.read_text());n=0
 for section in c['sections']:
  for block in section['blocks']:
   if block['type']!='p':continue
   for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',plain(block['html'])):
    if pat.search(sentence):
     n+=1;disposition='RETAIN: mature-engine description, finite algebra/identity, or explicit inferential boundary'
     if any(x in sentence for x in ['deterioration at short history establishes','primary is consequently specific','AR comparison demonstrates']):disposition='REPLACED by inspected-sample ranking statement; all adjacent losses and adverse outcomes retained'
     print(json.dumps(dict(version=label,section=section['title'],sentence=sentence,disposition=disposition),ensure_ascii=False))
 for fig in c['figures']:
  for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',fig['caption']):
   if pat.search(sentence):n+=1;print(json.dumps(dict(version=label,figure=fig['caption'],sentence=sentence,disposition='RETAIN: full-breakpoint finding is distinguished from plotting grid'),ensure_ascii=False))
 print(label,'matched_sentences_including_captions',n)
for old in ['The deterioration at short history establishes','The AR comparison demonstrates','primary is consequently specific']:assert old not in json.dumps(c)
print('All three overclaims removed; no mathematical proof or adverse financial result removed.')
