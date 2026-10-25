"""Sequential compilation using only the existing cached Tectonic bundle."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,resource,subprocess,time,re
ROOT=Path(__file__).resolve().parents[2]
ENGINE='/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS')
def diagnostics(log):
 return [x for x in log.splitlines() if re.search(r'(^!|undefined|Missing character|Overfull|^\s*(?:fatal\s+)?error\b|LaTeX Error:|Package \S+ Error:)',x,re.I)]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',required=True);parser.add_argument('--targets',nargs='+',default=['manuscript','supplement','extended-v9-technical']);args=parser.parse_args();assert re.fullmatch('[a-z0-9-]+',args.stage)
 records=[]
 for target in args.targets:
  assert re.fullmatch('[a-z0-9-]+',target)
  source=ROOT/'submission-jof'/(target+'.tex');out=ROOT/'.scratch/revision-v9'/args.stage/target;out.mkdir(parents=True,exist_ok=False)
  log=ROOT/'notes/revision-v9'/(args.stage+'-'+target+'-compile-console.txt');receipt=log.with_name(args.stage+'-'+target+'-compile-receipt.json')
  command=[ENGINE,'-X','compile','--only-cached',str(source.relative_to(ROOT)),'--outdir',str(out.relative_to(ROOT)),'--keep-logs','--keep-intermediates']
  start=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat();sha=digest(source)
  with log.open('x') as f:run=subprocess.run(command,cwd=ROOT,env=dict(os.environ,**{k:'1' for k in THREADS}),stdout=f,stderr=subprocess.STDOUT,timeout=590)
  duration=time.monotonic()-start;pdf=out/(target+'.pdf');full=(out/(target+'.log')).read_text(errors='replace') if (out/(target+'.log')).exists() else log.read_text(errors='replace')
  warnings=diagnostics(full)
  record=dict(command=command,started_utc=started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=duration,returncode=run.returncode,source=str(source.relative_to(ROOT)),source_sha256=sha,source_unchanged=sha==digest(source),pdf_path=str(pdf.relative_to(ROOT)) if pdf.exists() else None,pdf_sha256=digest(pdf) if pdf.exists() else None,error_undefined_missing_glyph_overfull_lines=warnings,child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,resource_scope='cumulative maximum child RSS of this sequential compiler wrapper',only_cached=True,numerical_thread_environment=1,packages_installed=0)
  with receipt.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
  records.append(record)
  print(json.dumps(record,indent=2))
  if run.returncode or not pdf.exists() or not record['source_unchanged']:raise SystemExit(1)
if __name__=='__main__':main()
