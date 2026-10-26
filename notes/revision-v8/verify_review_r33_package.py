from pathlib import Path
import json,zipfile,hashlib,subprocess,resource,datetime,re,time,os
from pypdf import PdfReader
from PIL import Image
ROOT=Path.cwd();BASE=ROOT/'.scratch/revision-v8/review-loop-round33';OUT=BASE/'isolated-package';OUT.mkdir(exist_ok=False);SOURCE=OUT/'sources';SOURCE.mkdir();DELIVERY=ROOT/'submission-jof';NOTES=ROOT/'notes/revision-v8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,cwd,path):
 t=time.monotonic();p=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600,env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1'));path.write_text(p.stdout);assert p.returncode==0,(cmd,p.returncode,p.stdout[-2000:]);return {'command':cmd,'returncode':0,'elapsed_seconds':time.monotonic()-t,'output':str(path.relative_to(ROOT))}
with zipfile.ZipFile(DELIVERY/'overleaf-package.zip') as z:
 members=z.namelist();assert len(members)==18
 for name in members:
  assert not Path(name).is_absolute() and '..' not in Path(name).parts;assert z.read(name)==(DELIVERY/name).read_bytes()
 z.extractall(SOURCE)
rows=[]
for stem,n,dpi,basis in [('manuscript',20,125,BASE/'render125'),('supplement',30,140,ROOT/'.scratch/revision-v8/review-loop-round30/render140'),('title-page',1,125,ROOT/'.scratch/revision-v8/wp8-title-final')]:
 out=OUT/(stem+'-output');out.mkdir();cmd=['/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic','-X','compile','--only-cached',stem+'.tex','--outdir',str(out),'--keep-logs','--keep-intermediates'];r=run(cmd,SOURCE,NOTES/('review-r33-package-'+stem+'-compile.txt'))
 a=PdfReader(DELIVERY/(stem+'.pdf'));b=PdfReader(out/(stem+'.pdf'));assert len(a.pages)==len(b.pages)==n;assert [p.extract_text() for p in a.pages]==[p.extract_text() for p in b.pages]
 log=(out/(stem+'.log')).read_text(errors='replace');bad=[l for l in log.splitlines() if re.search(r'^!|Overfull|Undefined control sequence|Missing character|(?:Citation|Reference).*undefined|There were undefined',l)];assert not bad,bad
 r['render']=run(['pdftoppm','-r',str(dpi),'-png',str(out/(stem+'.pdf')),str(out/'page')],SOURCE,NOTES/('review-r33-package-'+stem+'-render.txt'));pixels=[]
 for i in range(1,n+1):
  actual=out/f'page-{i:02}.png';actual=actual if actual.exists() else out/f'page-{i}.png';old=basis/f'page-{i:02}.png';old=old if old.exists() else basis/f'page-{i}.png';x=Image.open(actual).convert('RGB');y=Image.open(old).convert('RGB');assert x.size==y.size and x.tobytes()==y.tobytes(),(stem,i);pixels.append({'page':i,'sha256':sha(actual),'identical_to_viewed_basis':True})
 r.update(stem=stem,pages=n,source_sha256=sha(SOURCE/(stem+'.tex')),delivery_pdf_sha256=sha(DELIVERY/(stem+'.pdf')),rebuilt_pdf_sha256=sha(out/(stem+'.pdf')),all_page_text_equal=True,all_page_pixels_equal=True,pixel_checks=pixels,error_overfull_undefined_missing_glyph=bad,final_log_underfull_count=log.count('Underfull'));rows.append(r)
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','package_sha256':sha(DELIVERY/'overleaf-package.zip'),'package_members':len(members),'all_members_equal_current_source_bytes':True,'documents':rows,'child_peak_rss_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'financial_models_run':0,'raw_financial_inputs_read':0,'network_downloads':0,'scope':'Current ZIP regenerated all51pages with identical text/pixels to current viewed/bound basis. Financial replay and Git-history requirements remain separately BLOCKED.'};(NOTES/'review-r33-isolated-package.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='documents'},indent=2))
