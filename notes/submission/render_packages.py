"""Render every active submission PDF and bind each page image to its bytes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, subprocess, shutil
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
POP='/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    a=argparse.ArgumentParser();a.add_argument('--run',required=True);args=a.parse_args()
    base=ROOT/'.scratch/submission'/args.run;base.mkdir()
    records=[]
    files=[ROOT/'submission-package/ASMBI'/n for n in ['manuscript.pdf','supplement.pdf','title-page.pdf','cover-letter.pdf']]
    files += [ROOT/'submission-package/QF'/n for n in ['main.pdf','supplement.pdf','title-page.pdf','cover-letter.pdf']]
    files += [ROOT/'submission-package/SHARED'/n for n in ['declarations.pdf','suggested-reviewers.pdf','author-qa.pdf','editable-tables.pdf']]
    for pdf in files:
        destination=base/pdf.parent.name/pdf.stem;destination.mkdir(parents=True)
        subprocess.run([POP,'-scale-to','1500','-png',str(pdf),str(destination/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        images=sorted(destination.glob('page-*.png'));count=len(PdfReader(pdf).pages);assert len(images)==count
        records.append(dict(pdf=str(pdf.relative_to(ROOT)),sha256=sha(pdf),pages=count,rendered_pages=[dict(page=i+1,path=str(p.relative_to(ROOT)),sha256=sha(p)) for i,p in enumerate(images)],visual_status='PENDING_DIRECT_VIEW'))
        print(pdf.relative_to(ROOT),count,'pages',flush=True)
    output=ROOT/'notes/submission'/('renders-'+args.run+'.json');assert not output.exists()
    output.write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),targets=records),indent=2)+'\n')

if __name__=='__main__':main()
