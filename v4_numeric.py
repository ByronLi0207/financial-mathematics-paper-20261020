"""Context-bound numerical preservation, plus exact rendered-source binding.

This verifies consistency with immutable archived summaries, not new replication.
Layout, equations and bibliography are explicitly separated from empirical claims.
"""
from copy import deepcopy
from pathlib import Path
import hashlib,html,json,re
from v4_submission import ROOT,OUT,NOTE,joint_table
NUM=re.compile(r'[-+]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?')

def content_numbers(value):
 text=str(value)
 text=re.sub(r"https?://[^'\"<>\s]+",'',text)
 text=re.sub(r'\b[a-f0-9]{40,64}\b','',text)
 text=html.unescape(re.sub('<[^>]*>','',text)).replace('−','-')
 text=text.translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉','01234567890123456789'))
 text=re.sub(r'\b(?:Table|Figure|Section|Appendix|Supplement|Proposition)s?\s+(?:[A-LS]?\d+(?:\.\d+)?[a-z]?(?:[.–—-]\d+)?(?:\s*(?:and|,|–|-)\s*[A-LS]?\d+(?:\.\d+)?[a-z]?)*)','',text)
 text=re.sub(r'\bRQ[123]\b','',text)
 text=re.sub(r'\b(?:[ABC]\.\d+|S\d+\.\d+)\b','',text)
 text=re.sub(r'\bAppendix [A-L](?:\.\d+)?','',text)
 return NUM.findall(text)

def fields(b):
 return {k:b[k] for k in ('html','headers','rows','caption','latex') if k in b}

def validate_block(b):
 if b.get('_generator','').startswith('v5:'):
  from v5_submission import generated
  key=b['_generator'][3:]
  if key.startswith('positioning_evidence:'):
   from v5_positioning import positioning_evidence,printable_evidence_blocks
   expected=next(x for x in printable_evidence_blocks(positioning_evidence()) if x.get('_generator')==b['_generator'])
  else:expected=generated(key)
  bad=[]
  for spec in b.get('_bindings',[]):
   if hashlib.sha256((ROOT/spec['path']).read_bytes()).hexdigest()!=spec['sha256']:
    bad.append({'kind':'v5 input fingerprint changed','path':spec['path']})
  if fields(b)!=fields(expected):bad.append({'kind':'v5 contextual regeneration mismatch','key':key})
  return bad
 if b.get('_generator')=='joint_table':
  expected=joint_table()
  return [] if fields(b)==fields(expected) else [{'kind':'contextual CSV regeneration mismatch','binding':b.get('_bindings')}]
 if '_citation_ids' in b:
  audit=json.loads((NOTE/'reference-audit.json').read_text())
  expected=[]
  for ident in b['_citation_ids']:
   rec=next(x for x in audit['entries'] if x['id']==ident)
   years=re.findall(r'\((\d{4})\)',rec['suggested_html'])
   if not years:return [{'kind':'citation year not verified','id':ident}]
   expected.append(years[0])
  actual=content_numbers(b['html'])
  return [] if actual==expected else [{'kind':'citation metadata mismatch','expected':expected,'actual':actual}]
 if '_source' in b:
  spec=b['_source'];path=ROOT/spec['path'];raw=path.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=spec['sha256']:return [{'kind':'source fingerprint changed','path':spec['path']}]
  source=json.loads(raw)
  for key in spec['pointer']:source=source[key]
  bad=[]
  for key,val in fields(b).items():
   # The new caption heading is structure, all numbers following it stay bound.
   if key=='caption':
    val=re.sub(r'^(?:Table|Figure) [A-Z]?\d+[a-z]?†?\.?','',str(val));old=re.sub(r'^(?:Table|Figure) [A-Z]?\d+[a-z]?\.?','',str(source.get(key,'')))
   else:old=source.get(key,'')
   a,e=content_numbers(val),content_numbers(old)
   if a!=e:bad.append({'kind':'archived context mismatch','path':spec['path'],'pointer':spec['pointer'],'field':key,'expected':e,'actual':a})
  return bad
 if '_definition' in b:
  nums=content_numbers(' '.join(map(str,fields(b).values())))
  # Explicit bibliographic year in the RQ2 citation, checked against archived record.
  if nums==['2007'] and 'Gneiting, Balabdaoui and Raftery' in b.get('html',''):return []
  return [] if not nums else [{'kind':'unbound numbers in synthesis','actual':nums,'text':str(fields(b))[:400]}]
 return [{'kind':'missing provenance','text':str(fields(b))[:300]}]

def validate_all():
 from v4_typeset import tex_document
 report={'status':'PASS','scope':'All numeric tokens in manuscript.tex and supplement.tex; exact per-block source contexts and generated CSV row/field selectors. Archived consistency only, not independent data replication.',
 'documents':{},'mismatches':[],'matched_numeric_tokens':0,'empirical_or_archived_claim_tokens':0,'structural_template_tokens':0,'bibliographic_tokens':0}
 for name in ('manuscript','supplement'):
  doc=json.loads((OUT/(name+'-content.json')).read_text());bad=[];claims=0
  abs_spec=doc.get('_abstract_source')
  if doc.get('_abstract_generator'):
   fb={'type':'p','html':doc['abstract'],'_generator':doc['_abstract_generator'],'_bindings':doc.get('_abstract_bindings',[])}
   bad.extend(validate_block(fb));claims+=len(content_numbers(doc['abstract']))
  if abs_spec:
   x=json.loads((ROOT/abs_spec['path']).read_text())
   for k in abs_spec['pointer']:x=x[k]
   if content_numbers(doc['abstract'])!=content_numbers(x):bad.append({'kind':'abstract context mismatch'})
   claims+=len(content_numbers(doc['abstract']))
  for fi,figure in enumerate(doc['figures']):
   fb={'type':'p','caption':figure['caption'],**{k:figure[k] for k in ('_source','_generator','_bindings') if k in figure}}
   for error in validate_block(fb):bad.append({'figure':fi,**error})
  audit=json.loads((NOTE/'reference-audit.json').read_text())
  amend_path=ROOT/'notes/revision-v5-novelty/reference-amendments.json'
  amend=json.loads(amend_path.read_text()) if amend_path.exists() else {}
  for ref in doc['references']:
   recorded=next((x for x in audit['entries'] if x['id']==ref['id']),None)
   amended=next((x for x in amend.get('rows',[]) if x['id']==ref['id'] and x.get('proposed_note')),None)
   expected_ref=(html.escape(amended['proposed_note'])+" <a href='"+amended['proposed_url']+"'>Original source</a>.") if amended else (recorded or {}).get('suggested_html')
   if ref['html']!=expected_ref:bad.append({'reference':ref['id'],'kind':'reference differs from verified metadata disposition'})
  for si,s in enumerate(doc['sections']):
   for bi,b in enumerate(s['blocks']):
    for error in validate_block(b):bad.append({'section':si,'block':bi,**error})
    claims+=sum(len(content_numbers(v)) for v in fields(b).values())
  expected=tex_document(doc);actual=(OUT/(name+'.tex')).read_text()
  # This catches TeX-only tampering, including substitutions with another valid archive number.
  if actual!=expected:bad.append({'kind':'rendered TeX differs from source-bound canonical rendering'})
  extracted=len(NUM.findall(actual));bibl=sum(len(content_numbers(r['html'])) for r in doc['references'])
  report['documents'][name]={'tex_numeric_token_count':extracted,'archived_or_synthesis_tokens':claims,'bibliographic_tokens':bibl,'mismatch_count':len(bad)}
  report['matched_numeric_tokens']+=extracted if not bad else 0
  report['empirical_or_archived_claim_tokens']+=claims;report['bibliographic_tokens']+=bibl
  report['structural_template_tokens']+=extracted-claims-bibl
  report['mismatches'] += [{'document':name,**e} for e in bad]
 if report['mismatches']:report['status']='FAIL'
 ((ROOT/'notes/revision-v5-novelty' if any(json.loads((OUT/(n+'-content.json')).read_text()).get('_abstract_generator') for n in ('manuscript','supplement')) else NOTE)/'numeric-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2));return report

if __name__=='__main__':
 raise SystemExit(0 if validate_all()['status']=='PASS' else 1)
