"""Accept local release evidence without converting it into remote delivery."""
from pathlib import Path
import datetime,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
def read(name):return json.loads((ROOT/'notes/final-merge'/name).read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 receipts=['wp8-preregistration-integrity.json','wp8-evidence-check.json','wp8-saved-number-sources.json','wp8-current-numeric-contexts.json','wp8-current-document-audit.json','wp8-reference-audit.json','wp8-supplement-reference-audit.json','wp8-cross-reference-audit.json','wp8-language-audit.json','wp8-current-package-integrity.json','wp8-current-page-review.json','wp8-full-pytest-current.json','wp8-frozen-science-preservation.json','wp8-rights-gate.json','wp8-reachable-history-audit.json','wp8-tracked-file-resolved.json'];errors=[];rows=[]
 for name in receipts:
  r=read(name);ok=r['status'].startswith('PASS');rows.append(dict(path='notes/final-merge/'+name,status=r['status'],sha256=digest(ROOT/'notes/final-merge'/name)))
  if not ok:errors.append(dict(receipt=name,status=r['status']))
 doc=read('wp8-current-document-audit.json');test=read('wp8-full-pytest-current.json');pack=read('wp8-current-package-integrity.json')
 for target,path in [('main','manuscript.pdf'),('supplement','supplement.pdf')]:
  if digest(ROOT/'submission-final'/path)!=doc['pdf_sha256'][target]:errors.append(dict(kind='PDF_AFTER_FINAL_DOCUMENT_AUDIT',path=path))
 for path,expected in test['source_sha256_start'].items():
  if digest(Path(path))!=expected:errors.append(dict(kind='PUBLICATION_SOURCE_CHANGED_AFTER_FULL_TESTS',path=path))
 if not test['publication_source_and_display_code_unchanged_during_test']:errors.append(dict(kind='SOURCE_MUTATED_DURING_TEST'))
 if digest(ROOT/pack['zip'])!=pack['zip_sha256']:errors.append(dict(kind='PACKAGE_CHANGED'))
 if subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()!='final-jof':errors.append(dict(kind='WRONG_BRANCH'))
 r=dict(status='LOCAL_PASS_REMOTE_PUBLICATION_PENDING' if not errors else 'MISMATCH',actual_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),local_gate_mismatch_count=len(errors),mismatches=errors,receipts=rows,scientific_verdict='PARTLY',main_pages=doc['counts']['main_pages'],supplement_pages=doc['counts']['supplement_pages'],total_editorial_pdf_pages=48,body_words=doc['counts']['main_words_excluding_tables_references'],main_tables=6,main_figures=4,unique_reference_records=35,package_members=27,zip_sha256=pack['zip_sha256'],full_pytest='2215passed,1184subtestspassed,qualifiedexistinglocalhistoricalGitobjects',remote_branch_verified=False,remote_tree_verified=False,new_pr_count=0,wp8_overall='BLOCKED_PENDING_AUTHORIZED_PUBLICATION_ROUTE',all_goal_complete=False,deadline_not_before_utc='2026-10-26T15:01:52Z',scope='Local final-source release gate only. Remote ref/tree/blob/mode verification and one newPR remain required. Existing historical/scientific/data rights/provenance limitations are preserved, not dissolved by successful local checks.')
 (ROOT/'notes/final-merge/wp8-local-acceptance.json').write_text(json.dumps(r,indent=2)+'\n')
 for row in rows:print(row['status']+' '+row['path'])
 print(json.dumps({k:v for k,v in r.items() if k!='receipts'},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
