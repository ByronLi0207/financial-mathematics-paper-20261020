"""Copy verified fixed-source Git blobs only. No study/score/inference imports."""
from pathlib import Path
import subprocess,hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[2];SRC='60e03b8ae7a950c96ace3987f0625b3e434e6887'
FILES=[
'protocol/revision-v9/wp2-confirmatory.json','protocol/revision-v9/wp2-confirmatory.md',
'results/revision-v9/wp2/manifest.json','results/revision-v9/wp2/summary.json','results/revision-v9/wp2/summary.csv','results/revision-v9/wp2/support.json','results/revision-v9/wp2/package-receipt.json','results/revision-v9/wp2/study-termination.json',
'notes/revision-v9/wp2-all-prediction-counterexamples.csv',
'protocol/revision-v9/wp3-learning-curve.json','protocol/revision-v9/wp3-learning-curve.md',
'results/revision-v9/wp3/manifest.json','results/revision-v9/wp3/contrasts.json','results/revision-v9/wp3/contrasts.csv','results/revision-v9/wp3/curve-predictions.json','results/revision-v9/wp3/package-receipt.json','results/revision-v9/wp3/study-termination.json','results/revision-v9/wp3/README.md']
rows=[]
for name in FILES:
 data=subprocess.check_output(['git','show',SRC+':'+name],cwd=ROOT);dest=ROOT/'evidence/v11/pr5-v9'/name;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists(),dest;dest.write_bytes(data);assert dest.read_bytes()==data
 rows.append(dict(source_commit=SRC,source_path=name,source_git_blob=subprocess.check_output(['git','rev-parse',SRC+':'+name],cwd=ROOT,text=True).strip(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),imported_path=str(dest.relative_to(ROOT)),exact_copy=True))
(ROOT/'notes/v11/import-manifest.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Only verified WP2/WP3 scientific records and protocols; WP4/title/abstract/narrative excluded.',files=rows),indent=2)+'\n')
print('copied',len(rows),'fixed Git blobs, bytes',sum(x['bytes']for x in rows))
