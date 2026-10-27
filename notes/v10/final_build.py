"""Native final source-package compilation and every-page render, no financial code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,subprocess,zipfile
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'.scratch/v10/e7-native';BASE.mkdir();SOURCE=BASE/'source';SOURCE.mkdir()
manifest=json.load(open(ROOT/'notes/v10/package-source-manifest.json'));zpath=ROOT/manifest['archive_path']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(zpath)==manifest['archive_sha256']
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())=={x['path'] for x in manifest['files']}
 for x in manifest['files']:
  b=z.read(x['path']);assert hashlib.sha256(b).hexdigest()==x['sha256'] and b==(ROOT/'submission-v10'/x['path']).read_bytes()
 z.extractall(SOURCE)
records=[]
for name,dest,cap in [('main','manuscript',20),('supplement','supplement',35),('title-page','title-page',1),('cover-letter','cover-letter',1)]:
 out=BASE/name;out.mkdir();command=['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic','-X','compile',str(SOURCE/(name+'.tex')),'--outdir',str(out),'--keep-logs'];start=datetime.now(timezone.utc);q=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/'console.txt').write_text(q.stdout);assert q.returncode==0,q.stdout
 pdf=out/(name+'.pdf');log=(out/(name+'.log')).read_text();assert 'Overfull' not in log and not re.search(r'(?:Reference|Citation).*undefined',log)
 reader=PdfReader(pdf);assert 0<len(reader.pages)<=cap
 canonical=ROOT/'submission-v10'/(dest+'.pdf');shutil.copyfile(pdf,canonical)
 renders=BASE/('render-'+dest);renders.mkdir();cmd=['/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm','-scale-to','1500','-png',str(pdf),str(renders/'page')];subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 images=sorted(renders.glob('page-*.png'));assert len(images)==len(reader.pages)
 records.append(dict(target=dest,compiled_from=name+'.tex',started_utc=start.isoformat(),ended_utc=datetime.now(timezone.utc).isoformat(),output=str(canonical.relative_to(ROOT)),sha256=sha(canonical),pages=len(reader.pages),page_cap=cap,command=command,no_overfull=True,no_unresolved=True,underfull_warnings=log.count('Underfull'),rendered_pages=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in images],visual_review='PENDING_PER_PAGE'))
receipt=dict(status='NATIVE_COMPILE_RENDER_PASS_VISUAL_PENDING',source_zip_sha256=sha(zpath),source_files=manifest['source_files'],targets=records)
(ROOT/'notes/v10/final-native-build.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({r['target']:r['pages'] for r in records}))
