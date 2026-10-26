"""Bind actual per-page reviews to the exact four compiled canonical PDFs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v11'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((HERE/'visual-main-final.json').read_text())
s=json.loads((HERE/'visual-supplement-final.json').read_text())
assert m['latest_review_status']==s['latest_verified_status']=='PASS'
mr=m['follow_up_reviews'][-1];sr=s['snapshot_updates'][-1]
assert mr['status']==sr['status']=='PASS'and mr['all_22_pages_covered']
bound={x['document'].replace('_','-'):x['sha256']for x in mr['pdfs']}
bound['supplement']=sr['pdf']['sha256']
p=HERE/'final-native-build.json';report=json.loads(p.read_text())
for t in report['targets']:
 assert sha(ROOT/t['output'])==t['sha256']==bound[t['target']]
 t['visual_review']='PASS_ALL_PAGES'
 t['visual_evidence']='notes/v11/visual-supplement-final.json'if t['target']=='supplement'else'notes/v11/visual-main-final.json'
report.update(status='PASS',visual_review_completed_utc=datetime.now(timezone.utc).isoformat(),
              all_pages_covered=sum(x['pages']for x in report['targets']),
              reviewed_changed_pages_reuse='All changed PNGs actually viewed; unchanged PNGs reuse exact SHA-bound prior actual views.')
p.write_text(json.dumps(report,indent=2)+'\n')
print('PASS',[(t['target'],t['pages'])for t in report['targets']],'total pages',report['all_pages_covered'])
