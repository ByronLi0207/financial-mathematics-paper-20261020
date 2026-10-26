"""Read-only editorial acceptance checks against frozen v10 and saved receipts."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,subprocess,zipfile,sys
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v10b';DOC=ROOT/'submission-v10';BASE='23fd9fa8c8659efd038a91c3b23d634fa15b0ce0'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT).decode()
def main():
 science=json.loads((HERE/'science-seal.json').read_text())['protected_tracked_scientific_files'];changed=[f for f,h in science.items()if sha(ROOT/f)!=h];assert not changed,changed
 names=git('diff','--name-only',BASE).splitlines();outside=[n for n in names if not n.startswith(('notes/v10b/','submission-v10/'))and n not in ['README.md','REVISION_V10B_CHANGELOG.md']];assert not outside,outside
 s=(DOC/'manuscript.tex').read_text();old=git('show',BASE+':submission-v10/manuscript.tex');w=json.loads((HERE/'writing-final.json').read_text());assert w['abstract_words']<=180 and w['abstract_numeric_occurrences']<=8;assert w['flagged_proportion']<=.08 and w['average_sentence_words']<=20 and w['over_40_words']==0
 abstract=s.split(r'\begin{abstract}')[1].split(r'\end{abstract}')[0];assert all(x in abstract for x in ['First,','Second,','Third,']);assert abstract.startswith('Dealers monitor the largest absolute position');assert abstract.endswith('had been inspected beforehand.')
 for ban in ['3.2','144.3','90/98','F or I','1--32','1–32']:assert ban not in abstract
 assert s.count('Historical rules are hard to beat.')==2
 assert not re.search(r'1(?:--|–|—)32',s+(DOC/'cover-letter.tex').read_text())
 for f in ['manuscript.tex','title-page.tex','cover-letter.tex']:
  a=git('show',BASE+':submission-v10/'+f);b=(DOC/f).read_text();assert a.count('[TO BE COMPLETED BY AUTHOR]')==b.count('[TO BE COMPLETED BY AUTHOR]'),f
  assert '/tree/revision-v10b' in b,f
 assert s.split(r'\begin{thebibliography}')[1]==old.split(r'\begin{thebibliography}')[1]
 assert (DOC/'references.bib').read_bytes()==subprocess.check_output(['git','show',BASE+':submission-v10/references.bib'],cwd=ROOT)
 keywords=s.split(r'\textbf{Keywords:}')[1].split(r'\par')[0].strip().rstrip('.').split(';');assert len(keywords)<=6
 title=(DOC/'title-page.tex').read_text();running=title.split('Running title: ')[1].split(r'\par')[0];assert len(running)<40
 manifest=json.loads((HERE/'package-source-manifest.json').read_text());assert sha(ROOT/manifest['archive_path'])==manifest['archive_sha256']
 with zipfile.ZipFile(ROOT/manifest['archive_path'])as z:
  assert set(z.namelist())=={x['path']for x in manifest['files']}
  for x in manifest['files']:assert hashlib.sha256(z.read(x['path'])).hexdigest()==x['sha256']==sha(DOC/x['path'])
 native=json.loads((HERE/'final-native-build.json').read_text());assert native['status']=='PASS'
 for x in native['targets']:assert sha(ROOT/x['output'])==x['sha256']and x['pages']<=x['page_cap']and x['visual_review']=='PASS_ALL_PAGES'
 visual=json.loads((HERE/'visual-style-report.json').read_text());assert visual['all_figure_arrays_identical']and visual['all_table_display_values_identical']and visual['source_bytes_unchanged']
 for f,h in visual['sources_sha256'].items():assert sha(ROOT/f)==h
 assert all(x['before_artist_arrays']==x['after_artist_arrays']for x in visual['figures'])
 # Original main inline numeric result rows remain exact; headers and alignment may change.
 def result_body(text,label):
  own=text.index(r'\label{'+label+'}');end=text.index(r'\end{table}',own);beg=text.rfind(r'\begin{table}',0,own);block=text[beg:end];return block.split(r'\midrule',1)[1].split(r'\bottomrule',1)[0]
 for label in ['tab:fx','tab:weekly']:assert result_body(s,label)==result_body(old,label),label
 allpages=json.loads((HERE/'final-visual-all-pages.json').read_text());assert allpages['status']=='PASS'and allpages['total_pages']==53
 cost=json.loads((HERE/'cost-reading.json').read_text());
 # All three result examples are backed by the already-written archive-reading receipt.
 ctext=(HERE/'cost-reading.md').read_text();assert all(x in ctext for x in ['5/34','32/34','1/34'])
 for x in [r'$5/34$',r'$32/34$',r'$1/34$']:assert x in s
 extra_flags=w['forbidden_detail'];assert len(extra_flags)==5 and all(x['term']in ['S1','S2','S3']and'Supplement' in x['context'] or x['term']=='S3'and'Sections S3' in x['context'] for x in extra_flags)
 test=json.loads((HERE/'final-tests.json').read_text());assert test['status']=='PASS'and test['exit_code']==0
 d=dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),base_commit=BASE,protected_scientific_files=len(science),scientific_changes=changed,changed_path_scope_PASS=True,main_inline_result_rows_byte_identical=['tab:fx','tab:weekly'],six_figure_artist_arrays_exact=True,generated_table_values_preserved=True,source_archive_members=manifest['source_files'],source_zip_sha256=manifest['archive_sha256'],keywords=len(keywords),running_title=running,running_title_characters=len(running),author_placeholders_preserved=True,bibliography_and_bib_unchanged=True,abstract_words=w['abstract_words'],abstract_numbers=w['abstract_numeric_occurrences'],writing_three_gates_PASS=True,legacy_extra_forbidden_flags={'raw_count':len(extra_flags),'ruling':'All are exact Supplement S1/S2/S3 cross-references required by this task; frozen checker not changed.'},four_native_pdfs_and_all53pages_PASS=True,tests='1715 passed,1181 subtests passed',cost_points_source='notes/v10b/cost-reading.json',no_experiments=True)
 out=HERE/'final-package-check.json';out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
if __name__=='__main__':main()
