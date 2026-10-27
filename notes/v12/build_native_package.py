"""Build and render native editorial submission files; no financial code imported."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,shutil,subprocess,zipfile,argparse
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'submission-v10';HERE=ROOT/'notes/v12'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dependency_names():
    seen=set();todo=['main.tex','manuscript.tex','supplement.tex','title-page.tex','cover-letter.tex','references.bib','README.md','AUTHOR-TODO.md','figure-legends.tex']
    while todo:
        name=todo.pop();p=DOC/name
        if name in seen:continue
        assert p.is_file(),name
        seen.add(name)
        if p.suffix=='.tex':
            for kind,target in re.findall(r'\\(input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',p.read_text()):
                if not Path(target).suffix:target+=('.tex'if kind=='input'else'.pdf')
                q=(DOC/target).resolve();assert q.is_relative_to(DOC.resolve());todo.append(str(q.relative_to(DOC.resolve())))
    return sorted(seen)
def backup(p):
    if p.exists():
        b=p.with_name(p.name+'.v12.bak');i=1
        while b.exists():b=p.with_name(p.name+f'.v12.{i}.bak');i+=1
        shutil.copyfile(p,b)
def main():
    a=argparse.ArgumentParser();a.add_argument('--run',default='final-native');a=a.parse_args();base=ROOT/'.scratch/v12'/a.run;base.mkdir();source=base/'source';source.mkdir()
    files=[dict(path=n,bytes=(DOC/n).stat().st_size,sha256=sha(DOC/n))for n in dependency_names()];zpath=DOC/'overleaf-package.zip';backup(zpath)
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED)as z:
        for x in files:z.write(DOC/x['path'],x['path'])
    with zipfile.ZipFile(zpath)as z:
        assert set(z.namelist())=={x['path']for x in files}
        for x in files:assert hashlib.sha256(z.read(x['path'])).hexdigest()==x['sha256']
        z.extractall(source)
    manifest=dict(schema='v12-native-sources-v1',created_utc=datetime.now(timezone.utc).isoformat(),base_commit='452064866c2bdc4166b89d09d67b0cb2bc0ae415',source_files=len(files),files=files,archive_path=str(zpath.relative_to(ROOT)),archive_bytes=zpath.stat().st_size,archive_sha256=sha(zpath),scope='Native v12 manuscript and exact transitive display dependencies; new F1-F3 aggregate diagnostics added, all v11 archived science unchanged.')
    backup(HERE/'package-source-manifest.json');(HERE/'package-source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    records=[]
    for name,dest,cap in [('main','manuscript',20),('supplement','supplement',38),('title-page','title-page',1),('cover-letter','cover-letter',1)]:
        out=base/name;out.mkdir();cmd=['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic','-X','compile',str(source/(name+'.tex')),'--outdir',str(out),'--keep-logs','--keep-intermediates'];start=datetime.now(timezone.utc).isoformat();q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/'console.txt').write_text(q.stdout);assert q.returncode==0,q.stdout
        pdf=out/(name+'.pdf');log=(out/(name+'.log')).read_text();bad=re.findall(r'Overfull[^\n]*|(?:Reference|Citation)[^\n]*undefined|Label[^\n]*multiply defined',log);assert not bad,bad
        reader=PdfReader(pdf);assert 0<len(reader.pages)<=cap,(name,len(reader.pages),cap)
        canonical=DOC/(dest+'.pdf');backup(canonical);shutil.copyfile(pdf,canonical)
        renders=base/('render-'+dest);renders.mkdir();subprocess.run(['/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm','-scale-to','1500','-png',str(pdf),str(renders/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        images=sorted(renders.glob('page-*.png'));assert len(images)==len(reader.pages)
        records.append(dict(target=dest,source=name+'.tex',started_utc=start,ended_utc=datetime.now(timezone.utc).isoformat(),output=str(canonical.relative_to(ROOT)),sha256=sha(canonical),pages=len(reader.pages),page_cap=cap,command=cmd,no_overfull=True,no_unresolved=True,no_multiply_defined=True,underfull_warnings=log.count('Underfull'),rendered_pages=[dict(page=i+1,path=str(p.relative_to(ROOT)),sha256=sha(p))for i,p in enumerate(images)],visual_review='PENDING'))
        print(name,len(reader.pages),'pages',flush=True)
    receipt=dict(status='NATIVE_COMPILE_RENDER_PASS_VISUAL_PENDING',created_utc=datetime.now(timezone.utc).isoformat(),source_zip_sha256=sha(zpath),source_files=len(files),targets=records)
    backup(HERE/'final-native-build.json');(HERE/'final-native-build.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
