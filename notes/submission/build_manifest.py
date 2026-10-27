"""Read actual deliverables and map them to upload columns; no result calculation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'submission-package'

def save(p, text):
    if p.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copyfile(p,p.with_name(p.name+'.'+stamp+'.bak'))
    p.write_text(text)

items=[]
def add(path, column, role):
    p=OUT/path
    assert p.is_file(),p
    raw=p.read_bytes()
    pages=len(PdfReader(p).pages) if p.suffix=='.pdf' else None
    items.append(dict(path=str(p.relative_to(ROOT)),column=column,role=role,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pages=pages))

for journal,main,master in [('ASMBI','manuscript','ASMBI-source-and-pdf.zip'),('QF','main','source-package.zip')]:
    for stem,col in [(main,'Main document'),('supplement','Supporting information'),('title-page','Title page'),('cover-letter','Cover letter')]:
        add(f'{journal}/{stem}.pdf',col,'PDF for editor/system preview; fill personal placeholders before submission')
        add(f'{journal}/{stem}.tex',col+' source','Editable source; use the corresponding single-document ZIP for dependency closure')
    add(f'{journal}/main-document-source.zip','Main document source','Select '+main+'.tex as the main file; contains only this manuscript and dependencies')
    add(f'{journal}/supplement-document-source.zip','Supporting information source','Select supplement.tex as the main file')
    add(f'{journal}/{master}','Author working archive','Complete authoring backup; do not upload as a second scientific manuscript')
    for p in sorted((OUT/journal/'figures-upload').glob('*')):
        if '.bak' in p.name:continue
        add(str(p.relative_to(OUT)),'Figure / Supporting figure','TIFF is 1000 dpi LZW; PDF is the same vector display. Match figure number in mapping below')
for stem,col in [('declarations','Declarations / statements'),('suggested-reviewers','Suggested reviewers, if requested'),('author-qa','Author preparation only'),('editable-tables','Tables / editable source if requested')]:
    for suffix in ['pdf','tex']:
        add(f'SHARED/{stem}.{suffix}',col,'Author-facing preparation; review and complete all personal fields')

lines=['# Submission upload manifest','',
'Primary target: **Applied Stochastic Models in Business and Industry (ASMBI)**. Alternative format: **Quantitative Finance (QF)**. These are alternative packages of the same study, not simultaneous submissions. Actual portal labels may differ; the official journal submission link governs.', '',
'ASMBI permits Free Format at initial submission. The official Wiley template and AMA bibliography style were downloaded and recorded; the NJDv5 class lacks cached dependencies in this environment. Actual ASMBI PDFs therefore use the journal-permitted 12-point Free Format route with the unchanged official AMA BST. They are not represented as an unmodified NJDv5 compile. QF uses its unchanged official class/BST with explicit local compatibility and page-layout settings. See each package README and build receipt.', '',
'Authors, affiliations, ORCID, corresponding author, funding, competing interests, CRediT, source permissions, license/DOI and exclusive-submission approval require author completion. No account, manuscript submission or reviewer contact has occurred. A graphical abstract/highlights file is not a mandatory item identified for these two targets; do not treat the author FAQ as journal evidence.', '',
'| File | Upload column / use | Actual pages | Instructions |','|---|---|---:|---|']
for r in items:
    rel=r['path'].removeprefix('submission-package/')
    lines.append(f"| [{rel}]({rel}) | {r['column']} | {r['pages'] if r['pages'] is not None else '—'} | {r['role']} |")
lines += ['', '## Figure-number mapping', '', '| Number | File stem |', '|---|---|']
for number,stem in [('1','v9-endpoint-peak-example'),('2','v11-fx-history'),('3','v10-cftc-contract-changes'),('4','v12-decomposition'),('5','v10-cost-regions'),('6','v13-rp'),('S1','v10-menu-isolation'),('S2','v7-murphy-fx_hourly'),('S3','v7-murphy-nyfed_weekly'),('S4','v13-validation-length')]:
    lines.append(f'| {number} | `{stem}.tif` (upload) / `{stem}.pdf` (vector copy) |')
lines += ['', 'Use the TIFF and vector PDF as alternatives if the portal asks for one format, rather than registering the same figure twice. Main tables 1–8 are editable TeX in both source ZIPs and in SHARED/editable-tables.tex; ASMBI places each after the references on a separate page. Supplement tables and equations remain editable in its source ZIP.', '',
'The hashes, byte counts and page counts of all listed active files are in [MANIFEST.json](MANIFEST.json). Historical attempts, backups, `.scratch/` and unused template examples are not upload files. Final visual coverage and compilation are recorded separately under notes/submission; file existence alone is not visual approval.', '']
save(OUT/'MANIFEST.json',json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),files=items),ensure_ascii=False,indent=2)+'\n')
save(OUT/'MANIFEST.md','\n'.join(lines))
print(json.dumps(dict(files=len(items),pdf_pages=sum(x['pages'] or 0 for x in items)),indent=2))
