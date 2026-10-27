"""Export existing vector figure pages as publisher-requested lossless TIFFs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import argparse
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
POPPLER='/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def backup(p):
    if p.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        shutil.copyfile(p,p.with_name(p.name+'.'+stamp+'.bak'))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);args=parser.parse_args()
    scratch=ROOT/'.scratch/submission'/args.run;scratch.mkdir()
    rows=[]
    for source in sorted((ROOT/'submission-final/figures').glob('*.pdf')):
        reader=PdfReader(source);assert len(reader.pages)==1
        prefix=scratch/source.stem
        command=[POPPLER,'-singlefile','-r','1000','-tiff','-tiffcompression','lzw',str(source),str(prefix)]
        subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        tiff=prefix.with_suffix('.tif')
        with Image.open(tiff) as im:
            assert im.format=='TIFF' and im.mode=='RGB'
            assert all(x>=999 for x in im.info['dpi'])
            width,height=im.size;dpi=[float(x) for x in im.info['dpi']]
        outputs=[]
        for journal in ['ASMBI','QF']:
            dest=ROOT/'submission-package'/journal/'figures-upload';dest.mkdir(parents=True,exist_ok=True)
            for src,name in [(source,source.name),(tiff,source.stem+'.tif')]:
                target=dest/name;backup(target);shutil.copyfile(src,target);assert sha(src)==sha(target)
                outputs.append(str(target.relative_to(ROOT)))
        rows.append(dict(source=str(source.relative_to(ROOT)),source_sha256=sha(source),tiff_sha256=sha(tiff),pixels=[width,height],dpi=dpi,compression='LZW',mode='RGB',source_page_points=[float(reader.pages[0].mediabox.width),float(reader.pages[0].mediabox.height)],command=command,outputs=outputs))
        print(source.name,width,height,flush=True)
    receipt=ROOT/'notes/submission/figure-exports.json';backup(receipt)
    receipt.write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='Rasterization and exact file copies only; no forecast or result computation',figures=rows),indent=2)+'\n')

if __name__=='__main__':main()
