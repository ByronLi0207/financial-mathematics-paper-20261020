"""Conservative S5 source-word and real-PDF pagination checks."""
import argparse
import json
import re
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--current',action='store_true',help='Check the current delivered native PDFs rather than historical S5 drafts')
args=parser.parse_args()
tex=(ROOT/"submission-jof/manuscript.tex").read_text()
sections=re.split(r"\\section\{([^}]+)\}\\label\{[^}]+\}",tex)[1:]
limits=[1300,900,1000,600,800,800,2000,500,500,350]
counts=[]
for j in range(0,len(sections),2):
    title,body=sections[j:j+2]
    body=body.split(r"\section*{Data and code availability}")[0]
    body=re.sub(r"\\begin\{table\}.*?\\end\{table\}"," ",body,flags=re.S)
    body=re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}"," ",body)
    body=re.sub(r"\\(?:label|ref|citep|citet|citealp)\{[^}]*\}"," ",body)
    body=re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?"," ",body)
    words=re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",body)
    counts.append(dict(section=title,words=len(words),limit=limits[j//2],pass_limit=len(words)<=limits[j//2]))
main_path="submission-jof/manuscript.pdf" if args.current else ".scratch/revision-v7/s5/attempt3-manuscript/manuscript.pdf"
supp_path="submission-jof/supplement.pdf" if args.current else ".scratch/revision-v7/s5/attempt3-supplement/supplement.pdf"
main=PdfReader(ROOT/main_path)
supp=PdfReader(ROOT/supp_path)
report=dict(section_counts=counts,total_words=sum(v["words"] for v in counts),total_limit=8800,
            captioned_main_tables=len(re.findall(r"\\begin\{table\}",tex)),
            main_figures=len(re.findall(r"\\begin\{figure\}",tex)),main_pages=len(main.pages),
            supplement_pages=len(supp.pages),supplement_page_limit=30,
            main_pdf_producer=main.metadata.producer,supplement_pdf_producer=supp.metadata.producer,
            main_pdf=main_path,supplement_pdf=supp_path)
passed=(len(counts)==10 and all(v["pass_limit"] for v in counts) and report["total_words"]<=8800
        and report["captioned_main_tables"]<=6 and report["main_figures"]<=4 and report["supplement_pages"]<=30)
report["status"]="PASS" if passed else "FAIL"
print(json.dumps(report,indent=2))
raise SystemExit(not passed)
