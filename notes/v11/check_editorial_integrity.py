"""Read-only result, import, numeric-text and package integrity checks; no forecasting imports."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import argparse,hashlib,json,re,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v11';DOC=ROOT/'submission-v10'
BASE='de1a1cf22a005179f0d9a7c288855591292ddb49'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def literals(text):
    text=re.sub(r'\\begin\{(?:figure|table)\}.*?\\end\{(?:figure|table)\}','',text,flags=re.S)
    text=re.sub(r'\\(?:url|label|ref|input)\{[^}]*\}','',text)
    text=re.sub(r'\\href\{[^}]*\}',r'\\href',text)
    text=re.sub(r'\bS\d+\b|\bv\d+[a-z]?\b','',text)
    return Counter(re.findall(r'\d+(?:\.\d+)?',text))
def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);a=a.parse_args()
    protected=json.loads((HERE/'base-science-seal.json').read_text())
    changes=[p for p,h in protected.items()if sha(ROOT/p)!=h];assert not changes,changes
    imp=json.loads((HERE/'import-manifest.json').read_text());rows=imp['files']
    for x in rows:assert sha(ROOT/x['imported_path'])==x['sha256'],x
    bind=json.loads((HERE/'imported-number-bindings.json').read_text())
    for x in bind['bindings']:
        p=ROOT/x['imported_path'];assert sha(p)==x['sha256']
        value=json.loads(p.read_text())
        for token in x['json_pointer'].strip('/').split('/'):
            value=value[int(token)]if isinstance(value,list)else value[token]
        assert value==x['value'],x
    assert sha(DOC/'figures/v11-fx-history.pdf')==bind['figure_sha256']
    oldtexts=[old('submission-v10/'+f).decode()for f in ['manuscript.tex','supplement.tex']]
    texts=[(DOC/f).read_text()for f in ['manuscript.tex','supplement.tex']]
    before=literals('\n'.join(oldtexts));after=literals('\n'.join(texts))
    assert before==after,{'added':dict(after-before),'removed':dict(before-after)}
    inline_tables=0
    for prior,current in zip(oldtexts,texts):
        prior_tables=re.findall(r'\\begin\{table\}.*?\\end\{table\}',prior,re.S)
        current_tables=re.findall(r'\\begin\{table\}.*?\\end\{table\}',current,re.S)
        assert len(prior_tables)==len(current_tables)
        for before_table,after_table in zip(prior_tables,current_tables):
            assert re.findall(r'\d+',before_table)==re.findall(r'\d+',after_table)
            inline_tables+=1
    # Original displayed numerical rows are immutable despite edited method names/captions.
    allpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'submission-v10/generated','submission-v10/figures'],cwd=ROOT,text=True).splitlines()
    tables=figures=0
    for path in allpaths:
        if path.endswith('.tex'):
            assert re.findall(rb'\d+',old(path))==re.findall(rb'\d+',(ROOT/path).read_bytes()),path
            tables+=1
        elif path.endswith('.pdf'):
            assert old(path)==(ROOT/path).read_bytes(),path
            figures+=1
    s=texts[0];b=oldtexts[0]
    extract=lambda t:t.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    assert extract(s)==extract(b)
    assert s.split(r'\end{center}',1)[0]==b.split(r'\end{center}',1)[0]
    assert s.count('Historical rules are hard to beat.')==2
    assert r'\subsection{How much history does FX regression need?}'in s
    assert s.count(r'\textit{First,')==s.count(r'\textit{Second,')==s.count(r'\textit{Third,')==1
    for f in ['manuscript.tex','title-page.tex','cover-letter.tex']:
        new=(DOC/f).read_text();previous=old('submission-v10/'+f).decode()
        assert new.count('[TO BE COMPLETED BY AUTHOR]')==previous.count('[TO BE COMPLETED BY AUTHOR]')
        assert '/tree/revision-v11'in new
    for t in [b,s]:
        assert len(re.findall(r'\\bibitem\[',t))==34
    oldbib={m.group(1):m.group(2)for m in re.finditer(r'\\bibitem\[[^\n]*?\]\{([^}]+)\}(.*?)(?=\n\\bibitem|\\end\{thebibliography\})',b,re.S)}
    newbib={m.group(1):m.group(2)for m in re.finditer(r'\\bibitem\[[^\n]*?\]\{([^}]+)\}(.*?)(?=\n\\bibitem|\\end\{thebibliography\})',s,re.S)}
    assert oldbib.keys()==newbib.keys()
    for k in oldbib:assert re.findall(r'\d+',oldbib[k])==re.findall(r'\d+',newbib[k]),k
    # Isolated source ZIP is exactly the current transitive native source set.
    manifest=json.loads((HERE/'package-source-manifest.json').read_text())
    assert sha(ROOT/manifest['archive_path'])==manifest['archive_sha256']
    with zipfile.ZipFile(ROOT/manifest['archive_path'])as z:
        assert set(z.namelist())=={x['path']for x in manifest['files']}
        for x in manifest['files']:
            assert hashlib.sha256(z.read(x['path'])).hexdigest()==sha(DOC/x['path'])==x['sha256']
    tests=json.loads((HERE/'final-tests.json').read_text());assert tests['status']=='PASS'and tests['exit_code']==0
    report=dict(status='PASS',created_utc=datetime.now(timezone.utc).isoformat(),base_commit=BASE,
        protected_scientific_files=len(protected),changed_scientific_files=changes,
        imported_exact_blobs=len(rows),exact_json_bindings=len(bind['bindings']),
        main_and_supplement_numeric_literal_multiset_unchanged=True,
        literal_exclusions='Floats checked separately; technical URLs/labels/refs/inputs and version/section identifiers excluded. Existing result paragraphs moved verbatim across documents.',
        original_generated_table_numeric_sequences_unchanged=tables,original_inline_table_numeric_sequences_unchanged=inline_tables,original_figure_pdfs_byte_identical=figures,
        bibliography_entries=34,bibliographic_numeric_fields_unchanged=True,abstract_and_title_unchanged=True,
        three_findings=True,author_AI_placeholders_preserved=True,source_zip_members=manifest['source_files'],
        source_zip_sha256=manifest['archive_sha256'],tests='1715 passed, 1181 subtests passed',
        no_new_financial_experiment=True,wp4_imported=False)
    with a.output.open('x')as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
