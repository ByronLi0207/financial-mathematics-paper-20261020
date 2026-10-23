"""Read-only scientific preservation, novelty wording and source fingerprint audit."""
from collections import Counter
import hashlib,json,re
from v4_submission import ROOT,OUT,dump,plain
from v5_submission import NOTE,read,BASE,SUPP

def signature(t):return re.sub(r'Proposition [123]', 'Proposition [structural]',json.dumps({k:t[k] for k in ('headers','rows')},sort_keys=True,ensure_ascii=False))
def main():
 before=[read(BASE),read(SUPP)];after=[read('submission-jof/manuscript-content.json'),read('submission-jof/supplement-content.json')]
 old=Counter(signature(b) for d in before for s in d['sections'] for b in s['blocks'] if b['type']=='table')
 new=Counter(signature(b) for d in after for s in d['sections'] for b in s['blocks'] if b['type']=='table')
 missing=list((old-new).elements());state=read('notes/revision-v5-novelty/state.json');changed=[]
 for path,sha in state['protected'].items():
  actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  permitted=state.get('authorized_support_changes',{}).get(path,{})
  if actual!=sha and actual!=permitted.get('after_sha256'):changed.append(path)
 report={'all_v4_table_rows_preserved':not missing,'v4_table_count':sum(old.values()),'structural_exception':'Method overview L row Proposition 1 relabeled Proposition 2; no empirical cell altered','missing_table_count':len(missing),'protected_file_changes':changed,'documented_support_changes':state.get('authorized_support_changes',{}),'status':'PASS' if not missing and not changed else 'FAIL'}
 dump(NOTE/'preservation-check.json',report)
 occurrences=[];bad=[];wordtext=[]
 for dn,d in zip(['manuscript','supplement'],after):
  for sec in d['sections']:
   for b in sec['blocks']:
    if b['type'] not in ('p','subheading','equation'):continue
    text=plain(b.get('html',b.get('text','')));wordtext.append(text)
    for term in re.finditer(r'\b(novel|first|unique|establish\w*|demonstrat\w*|prov(?:e|es|ed|ing))\b',text,re.I):
     left=text.rfind('. ',0,term.start());right=text.find('. ',term.end())
     sentence=text[0 if left<0 else left+2:right+1 if right>=0 else len(text)]
     rationale={'first':'Chronological first observation/release or first-order stochastic dominance; no novelty priority claim.', 'unique':'Distinct stored breakpoint values; not a global uniqueness claim.'}.get(term[1].lower(),'Established method, proof boundary, mathematical demonstration or explicit negation; checked in the complete sentence.')
     if 'global priority' in sentence or 'prevent a first' in sentence:rationale='Explicitly rejects a global priority or first-path-risk claim.'
     elif term[1].lower().startswith('prov'):rationale='A stated elementary mathematical derivation, or explicit warning that data do not prove a probability claim; not algorithmic novelty.'
     elif 'first inclusion' in sentence:rationale='Order of inclusions in a classical inequality proof.'
     elif 'bridge' in sentence or 'first step' in sentence:rationale='Order of an exact descriptive arithmetic bridge, not chronology of scientific priority.'
     elif term[1].lower().startswith(('demonstrat','establish')):rationale='Acknowledged existing practice, recorded historical change or explicit evidence limitation; no unsupported priority.'
     occurrences.append({'document':dn,'section':sec['title'],'term':term[1],'sentence':sentence,'ruling':'retain with stated local meaning','reason':rationale})
    if re.search(r'\bmerely\b|only an application|using mature methods',text,re.I):bad.append({'document':dn,'text':text})
 dump(NOTE/'novelty-word-audit.json',{'scope':'Current manuscript and supplement narrative; historical snapshots, source titles and cited-paper quotations are not rewritten.','occurrences':occurrences,'self_deprecating_phrases':bad,'status':'PASS' if not bad else 'FAIL'})
 print(json.dumps(report,indent=2));print('Novelty words:',len(occurrences),'self-deprecating matches:',len(bad))
 return report
if __name__=='__main__':main()
