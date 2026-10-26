"""Publish unchanged scalar-only formal outputs; private financial vectors excluded."""
from pathlib import Path
import csv,gzip,hashlib,io,json,tarfile,time,resource,datetime
ROOT=Path.cwd();source=ROOT/'.scratch/revision-v9/wp3-run';out=ROOT/'results/revision-v9/wp3'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2,allow_nan=False);f.write('\n')
began=time.monotonic();out.mkdir(parents=True,exist_ok=False)
term=json.loads((source/'study-termination.json').read_text());assert term['all_workers_terminated'] and term['status']=='COMPLETE'
audit=json.loads((ROOT/'notes/revision-v9/wp3-independent-audit.json').read_text());assert audit['audit_status']=='PASS' and audit['independent_legacy_exact_difference_count']==0
files=sorted(p for p in source.rglob('*') if p.is_file());assert all(not p.is_symlink() and p.suffix in ('.json','.jsonl','.csv','.log') for p in files)
rows=[dict(path=str(p.relative_to(source)),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files]
archive=out/'wp3-scalar-driver-output.tar.gz'
with archive.open('xb') as raw:
 with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tar:
   for p,row in zip(files,rows):
    b=p.read_bytes();info=tarfile.TarInfo(row['path']);info.size=len(b);info.mode=0o644;info.uid=info.gid=info.mtime=0;info.uname=info.gname='';tar.addfile(info,io.BytesIO(b))
with (out/'wp3-scalar-members.csv').open('x',newline='') as f:
 writer=csv.DictWriter(f,('path','bytes','sha256'));writer.writeheader();writer.writerows(rows)
with tarfile.open(archive,'r:gz') as tar:
 members=tar.getmembers();assert [x.name for x in members]==[r['path'] for r in rows]
 for item,row in zip(members,rows):
  b=tar.extractfile(item).read();assert item.isfile() and len(b)==row['bytes'] and sha(b)==row['sha256'] and b==(source/row['path']).read_bytes()
for name in ('manifest.json','study-termination.json','contrasts.json','contrasts.csv','curve-predictions.json'):
 with (out/name).open('xb') as f:f.write((source/name).read_bytes())
receipt=dict(actual_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',source_members=len(rows),uncompressed_bytes=sum(r['bytes'] for r in rows),archive_bytes=archive.stat().st_size,archive_sha256=sha(archive.read_bytes()),index_sha256=sha((out/'wp3-scalar-members.csv').read_bytes()),byte_mismatches=0,raw_financial_files_included=0,private_forecast_vectors_included=0,original_files_deleted=0,scope='scalar formal output preservation and byte identity, not independent financial replication',elapsed_seconds=time.monotonic()-began,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
save(out/'package-receipt.json',receipt)
with (out/'README.md').open('x') as f:f.write('# WP3 retrospective FX learning curve\n\nDesign was committed before this run at `b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a`; the JSON hash is in manifest.json. All ten fixed H/W units completed, with both exact W2880 archive gates passing. Three identified first cutpoints are consistent; the QR4/H6 curve is compatible-left-censored and NOT_TESTABLE, so an all-four confirmation is absent. H24 gain reverses at the longest W. No specification or prediction was changed after the run.\n\ncontrasts.csv/json retain every fixed conditional row and its pointwise nominal post-result DM/HAC diagnostic. curve-predictions.json retains all loss rows and roots. The scalar-only tar stores all candidate/selection/fit diagnostics, baseline gate receipts, progress and resources, with member hashes and exact byte checks. The source CSV and private forecast vectors remain unpublished in .scratch. Their fingerprints and acquisition version are documented; a public scalar archive is not a public financial-data license or independent dealer replication. Existing archives were not changed.\n\nIndependent saved-trace arithmetic verification is recorded in notes/revision-v9/wp3-independent-audit.json. It performs no QR refit or new forecast. The publicly cloned browser-upload history lacks the local pre-run design commit object required by the strict ancestry guard; this known fresh-clone replay limitation is not resolved by file identity and has not been bypassed.\n')
print(json.dumps(receipt,indent=2))
