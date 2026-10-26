"""Current-source section/figure/table/page budgets; no financial computation."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,re,subprocess
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('prose_base',ROOT/'notes/v7/writing_metrics.py');v7=importlib.util.module_from_spec(spec);spec.loader.exec_module(v7)

def prose(raw):
    for env in ['table','longtable','tabular']:
        raw=re.sub(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}',' ',raw,flags=re.S)
    raw=re.sub(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}',' ',raw)
    raw=re.sub(r'\\(?:section|subsection|paragraph)\*?\{[^}]*\}',' ',raw)
    raw=re.sub(r'\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?',' ',raw)
    return v7.plain(raw,{})

def pages(path):
    text=subprocess.check_output(['pdfinfo',str(path)],text=True)
    return int(re.search(r'^Pages:\s+(\d+)',text,re.M).group(1))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    path=ROOT/'submission-jof/manuscript.tex';tex=path.read_text();prefix=tex.split('\\begin{thebibliography}',1)[0]
    start=prefix.index('\\section{Introduction}');sectional=prefix[start:]
    matches=list(re.finditer(r'\\section\*?\{([^}]+)\}',sectional));counts={}
    for i,m in enumerate(matches):
        if m[1]=='Author-provided information':continue
        block=sectional[m.end():matches[i+1].start() if i+1<len(matches) else len(sectional)]
        counts[m[1]]=v7.word_count(prose(block))
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    abstract_words=v7.word_count(prose(abstract))
    # Research-design/transparency, figure captions, inline and displayed math
    # tokens remain in this budget. This is broader than sentence-style gates.
    body_words=sum(counts.values());budget_words=body_words+abstract_words
    figures=len(re.findall(r'\\begin\{figure\}',tex));tables=len(re.findall(r'\\begin\{table\}',tex))
    main_pdf=ROOT/'.scratch/revision-v8/wp7-main-final-layout/manuscript.pdf'
    sup_receipt=json.loads((ROOT/'notes/revision-v8/wp7-supplement-compile-receipt.json').read_text());sup_pdf=ROOT/sup_receipt['pdf_path']
    assert hashlib.sha256((ROOT/'submission-jof/supplement.tex').read_bytes()).hexdigest()==sup_receipt['source_sha256']
    assert hashlib.sha256(sup_pdf.read_bytes()).hexdigest()==sup_receipt['pdf_sha256']
    p_main,p_sup=pages(main_pdf),pages(sup_pdf)
    out=dict(checked_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if budget_words<=9000 and figures<=4 and tables<=6 and p_sup<=30 else 'FAIL',
        operation='Word/layout/source checks only',word_count_method='Regexalphanumeric tokens including numeric/math tokens, figure captions and full Research design/transparency; excludes all table environments/references/author-provided placeholder block. Abstract added separately. No favorable exclusion of transparency from this budget.',section_words_excluding_table_environments=counts,main_body_words=body_words,abstract_words=abstract_words,budget_words_including_abstract=budget_words,word_limit=9000,main_figures=figures,main_tables=tables,main_pages=p_main,supplement_pages=p_sup,supplement_page_limit=30,
        main_source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),main_pdf_path=str(main_pdf.relative_to(ROOT)),main_pdf_sha256=hashlib.sha256(main_pdf.read_bytes()).hexdigest(),supplement_source_sha256=sup_receipt['source_sha256'],supplement_pdf_path=sup_receipt['pdf_path'],supplement_pdf_sha256=sup_receipt['pdf_sha256'],final_all_page_QA_not_yet_claimed='WP8 required')
    (ROOT/a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
