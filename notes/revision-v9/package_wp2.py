"""Package completed WP2 source bytes without deleting or rewriting originals."""
import argparse,csv,gzip,hashlib,io,json,os,shutil,tarfile,time,datetime as dt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def archive_source(source,archive,index):
 source,archive,index=map(Path,(source,archive,index))
 if archive.exists() or index.exists():raise FileExistsError('package output exists')
 paths=sorted(p for p in source.rglob('*') if p.is_file() or p.is_symlink())
 if source.is_symlink() or any(p.is_symlink() for p in paths):raise ValueError('symlink source refused')
 rows=[]
 for p in paths:
  rows.append(dict(path=p.relative_to(source).as_posix(),size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 with archive.open('xb') as raw:
  with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0,filename='') as gz:
   with tarfile.open(fileobj=gz,mode='w|') as tar:
    for row,p in zip(rows,paths):
     content=p.read_bytes()
     if hashlib.sha256(content).hexdigest()!=row['sha256']:raise ValueError('source changed during packaging')
     info=tarfile.TarInfo(row['path']);info.size=len(content);info.mode=0o644;info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
     tar.addfile(info,io.BytesIO(content))
 with index.open('x',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=('path','size','sha256'));writer.writeheader();writer.writerows(rows)
 expected={r['path']:r for r in rows};seen=set();mismatches=[]
 with tarfile.open(archive,'r|gz') as t:
  for member in t:
   if member.name in seen or member.name not in expected:raise ValueError('archive member census mismatch')
   seen.add(member.name);content=t.extractfile(member).read();r=expected[member.name]
   if len(content)!=r['size'] or hashlib.sha256(content).hexdigest()!=r['sha256']:mismatches.append(member.name)
 if set(expected)!=seen or mismatches:raise ValueError('archive byte MISMATCH '+str(mismatches))
 return dict(members=len(rows),uncompressed_bytes=sum(r['size'] for r in rows),archive_bytes=archive.stat().st_size,archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),index_sha256=hashlib.sha256(index.read_bytes()).hexdigest(),mismatches=0,source_files_deleted=0,metadata_sanitized='tar mode644; uid/gid0, empty owner names, mtime0; content bytes unchanged')

def main():
 source=ROOT/'.scratch/revision-v9/wp2-run';target=ROOT/'results/revision-v9/wp2'
 term=json.loads((source/'study-termination.json').read_text());audit=json.loads((ROOT/'notes/revision-v9/wp2-independent-audit.json').read_text())
 if not term['all_workers_terminated'] or audit.get('status')!='PASS':raise ValueError('source/audit gate not passed')
 target.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 for name in ('manifest.json','study-termination.json','summary.json','summary.csv','support.json','budget-decision.json'):
  if (source/name).exists():shutil.copy2(source/name,target/name)
 package=archive_source(source,target/'wp2-driver-output.tar.gz',target/'wp2-driver-output-members.csv')
 if package['archive_bytes']>25*1024**2:raise ValueError('single browser-upload archive exceeds25MiB; retain all sources and report blocked')
 value=dict(status='PASS',actual_utc=dt.datetime.now(dt.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-start,formal_source=str(source.relative_to(ROOT)),**package)
 with (target/'package-receipt.json').open('x') as f:json.dump(value,f,indent=2);f.write('\n')
 print(json.dumps(value,indent=2));return0=0;return return0
if __name__=='__main__':raise SystemExit(main())
