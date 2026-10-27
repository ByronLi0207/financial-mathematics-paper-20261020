"""Make unambiguous single-document source uploads from verified full packages."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,shutil,subprocess,zipfile
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
TEX='/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic'
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def backup(p):
    if p.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');shutil.copyfile(p,p.with_name(p.name+'.'+stamp+'.bak'))

def main():
    a=argparse.ArgumentParser();a.add_argument('--run',required=True);args=a.parse_args()
    scratch=ROOT/'.scratch/submission'/args.run;scratch.mkdir()
    records=[]
    config={'ASMBI':('ASMBI-source-and-pdf.zip','manuscript.tex','manuscript.pdf'),
            'QF':('source-package.zip','main.tex','main.pdf')}
    for journal,(master_name,main_tex,main_pdf) in config.items():
        folder=ROOT/'submission-package'/journal;master=folder/master_name
        with zipfile.ZipFile(master) as z:payload={n:z.read(n) for n in z.namelist()}
        for kind,entry,reference in [('main',main_tex,main_pdf),('supplement','supplement.tex','supplement.pdf')]:
            keeptex={'manuscript.tex'} if journal=='ASMBI' and kind=='main' else {entry}
            if journal=='QF':
                keeptex |= {'qf-compat.tex','qf-fonts.tex'}
                if kind=='main':keeptex.add('manuscript.tex')
            members={}
            for name,raw in payload.items():
                p=Path(name)
                # Generated tables/sections are transitive inputs, not extra
                # top-level documents. Keep the existing generated TeX closure
                # while retaining one unambiguous root document per upload.
                if p.suffix=='.tex' and name not in keeptex and not (p.parts[0]=='generated'):continue
                if p.suffix=='.pdf' and not name.startswith('figures/'):continue
                if p.suffix=='.bbl' and p.stem!=Path(entry).stem:continue
                if name in {'README.md','build-report.json','BUILD-RECEIPT.json','source-manifest.json','compatibility.json'}:continue
                members[name]=raw
            assert entry in members
            manifest={n:dict(bytes=len(raw),sha256=sha(raw)) for n,raw in sorted(members.items())}
            members['UPLOAD-SOURCE-MANIFEST.json']=(json.dumps(dict(journal=journal,document=kind,entry=entry,source_master_sha256=sha(master.read_bytes()),files=manifest),indent=2)+'\n').encode()
            archive=folder/(kind+'-document-source.zip');backup(archive)
            with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
                for name,raw in members.items():z.writestr(name,raw)
            with zipfile.ZipFile(archive) as z:
                assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
                for name,raw in members.items():assert z.read(name)==raw
                work=scratch/journal/kind;work.mkdir(parents=True);z.extractall(work)
            output=work/'build';output.mkdir()
            cmd=[TEX,'-X','compile','-C',entry,'--outdir',str(output),'--keep-logs','--keep-intermediates']
            old=folder/reference;reference_before=sha(old.read_bytes())
            q=subprocess.run(cmd,cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            (output/'console.txt').write_text(q.stdout);assert q.returncode==0,q.stdout
            result=output/(Path(entry).stem+'.pdf')
            reader=PdfReader(result);expected=PdfReader(old)
            assert len(reader.pages)==len(expected.pages)
            actual_text=[p.extract_text() for p in reader.pages]
            reference_text=[p.extract_text() for p in expected.pages]
            assert actual_text==reference_text
            assert sha(old.read_bytes())==reference_before,'Active reference PDF changed during verification'
            page_text_comparisons=[dict(page=i+1,exact_match=a==b,compiled_text_sha256=sha((a or '').encode()),reference_text_sha256=sha((b or '').encode())) for i,(a,b) in enumerate(zip(actual_text,reference_text))]
            records.append(dict(journal=journal,document=kind,archive=str(archive.relative_to(ROOT)),archive_sha256=sha(archive.read_bytes()),source_master_sha256=sha(master.read_bytes()),members=len(members),generated_tex_members=sorted(n for n in members if n.startswith('generated/') and n.endswith('.tex')),entry=entry,compiled_pages=len(reader.pages),compiled_pdf_sha256=sha(result.read_bytes()),rendered_text_exact_to_active_pdf=True,page_text_comparisons=page_text_comparisons,reference_pdf=str(old.relative_to(ROOT)),reference_sha256=reference_before,reference_unchanged_during_check=True,only_cached=True,checked_utc=datetime.now(timezone.utc).isoformat(),command=cmd,log=str((output/'console.txt').relative_to(ROOT))))
            print(journal,kind,len(reader.pages),'pages',flush=True)
    target=ROOT/'notes/submission/upload-source-archives.json';backup(target);target.write_text(json.dumps(records,indent=2)+'\n')

if __name__=='__main__':main()
