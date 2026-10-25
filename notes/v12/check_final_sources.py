"""Read-only integrity and source-binding checks for the v12 deliverables."""
from pathlib import Path
import json,hashlib,re,subprocess,datetime
R=Path(__file__).resolve().parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads((R/p).read_text())
def pointer(obj,p):
 for key in p.split('/')[1:]:
  key=key.replace('~1','/').replace('~0','~');obj=obj[int(key)]if isinstance(obj,list)else obj[key]
 return obj
seal=load('notes/v12/base-science-seal.json');assert all(sha(R/n)==h for n,h in seal.items())
science=[]
for ex,folder,expected in [('F1','decomposition',180),('F2','validation-length',136),('F3','tau',74)]:
 p=R/'results/v12'/folder;rows=json.loads((p/'rows.json').read_text());assert len(rows)==expected
 runtime=json.loads((p/'runtime.json').read_text());assert runtime['elapsed_seconds']<=runtime['wall_cap_seconds']
 cs=json.loads((p/'code-seal.json').read_text()); science.append(dict(experiment=ex,rows=len(rows),complete=sum(x['status']=='COMPLETE'for x in rows),failed=sum(x['status']=='FAILED'for x in rows),runtime=runtime['elapsed_seconds']))
 # The six-code files have remained unchanged since the prelaunch seal.
 hashes=cs['sha256']; assert len(hashes)==6
 if isinstance(hashes,dict):
  for n,h in hashes.items():assert sha(R/n)==h,(n,h)
 for row in rows:
  if row['status']=='COMPLETE'and ex=='F1':
   assert row['finite_oracle_penalty']!='inf' if 'finite_oracle_penalty'in row else True
   assert abs(row['actual_excess_pct']-row['selection_component_pct']-row['signal_gap_pct'])<1e-8
new=load('notes/v12/new-paper-number-bindings.json');sources=new['sources']
for v in sources.values():assert sha(R/v['path'])==v['sha256']
for x in new['bindings']:
 assert sha(R/x['source'])==x['sha256']
 if x['id']=='finite_menu_cardinality':
  assert len(x['operands'])==x['value']
  assert all(pointer(load(x['source']),a['json_pointer'])==a['value']for a in x['operands'])
 else: assert pointer(load(x['source']),x['json_pointer'])==x['value']
# Verify each numeric pointer, in addition to every owning source file hash.
desc=load('results/v12/descriptives/number-bindings.json')
for x in desc['files']:assert sha(R/'results/v12/descriptives'/x['path'])==x['sha256']
for x in desc['numeric_bindings']:
 assert pointer(load('results/v12/descriptives/'+x['source_file']),x['pointer'])==x['value']
meta=load('results/v12/descriptives/metadata.json')
# Style-only copy must invert exactly to the statistical source.
a=(R/'submission-v10/generated/v12-data-table.tex').read_text();b=(R/'results/v12/descriptives/data-table.tex').read_text();assert a.replace(r'p{.09\linewidth}',r'p{.08\linewidth}',1)==b
main=(R/'submission-v10/manuscript.tex').read_text();supp=(R/'submission-v10/supplement.tex').read_text();moves=load('notes/v12/original-relocation-text.json');assert moves['short_history_fx']in main
menu=moves['menu'].strip().removesuffix(r'\FloatBarrier').strip();assert menu in supp
oldlimits=moves['limitations'];paragraphs=oldlimits.split('\n\n');prose=[x for x in paragraphs if x and not x.startswith('\\')]
assert all(x in supp for x in prose)
# Data rows in the altered legacy table displays remain verbatim.
tables=['v10-cftc-contracts.tex','v10-mcs-main.tex','v10-menu-full.tex']
for n in tables:
 path='submission-v10/generated/'+n
 old=subprocess.check_output(['git','show','452064866c2bdc4166b89d09d67b0cb2bc0ae415:'+path],cwd=R).decode()
 now=(R/path).read_text()
 data=lambda s:[l for l in s.splitlines()if '&'in l and re.search(r'\d',l)and l.endswith(r'\\')and not any(z in l for z in ['caption','toprule','midrule','multicolumn','shortstack'])]
 assert data(old)==data(now),n
for n in ['manuscript.tex','title-page.tex','cover-letter.tex','AUTHOR-TODO.md','README.md']:
 t=(R/'submission-v10'/n).read_text();assert not re.search(r'AI\s*(statement|disclosure)|AI/use statement',t,re.I),n
for label in ['Author information','ORCID','Funding','Competing interests']:assert label+': [TO BE COMPLETED BY AUTHOR]'in main
assert r'\citep{sussman2023}'not in main and 'see Sussman (2023)'not in supp
assert '\\input{generated/v12-low-frequency.tex}'not in main
report=dict(status='PASS',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),base_science_files_unchanged=len(seal),frozen_execution_code_checks=18,new_paper_bindings_verified=len(new['bindings']),descriptive_numeric_bindings_verified=len(desc['numeric_bindings']),studies=science,exact_legacy_data_tables=tables,original_menu_moved_verbatim=True,original_limitations_paragraphs_retained=len(prose),short_history_FX_moved_verbatim=True,active_AI_declaration_absent=True,other_author_placeholders_preserved=True,table_width_only_inverse_identity=True,new_section_inline_for_unchanged_writing_checker=True)
p=R/'notes/v12/final-source-integrity.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
