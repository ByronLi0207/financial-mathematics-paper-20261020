"""Structural WP6 review/disposition acceptance; no financial computation."""
from pathlib import Path
import re,json,hashlib,datetime,subprocess
root=Path(__file__).resolve().parents[2];notes=root/'notes/revision-v8';reviews={};severities={}
for role,name in [('A','review-A-editor.md'),('B','review-B-econometrics.md'),('C','review-C-risk-manager.md')]:
    s=(notes/name).read_text()
    pattern=r'^([1-9])\.\s+\*\*(MAJOR|MINOR)' if role!='C' else r'^## C([1-9]) — (MAJOR|MINOR)'
    hits=re.findall(pattern,s,re.M)
    assert [int(i) for i,_ in hits]==list(range(1,10)),(role,hits)
    reviews[role]=dict(path=str((notes/name).relative_to(root)),sha256=hashlib.sha256(s.encode()).hexdigest(),count=len(hits),major=sum(v=='MAJOR' for _,v in hits),minor=sum(v=='MINOR' for _,v in hits))
    severities.update({role+i:v for i,v in hits})
body=(notes/'internal-review-2.md').read_text()
rows=re.findall(r'^\| ([ABC][1-9]) \| (MAJOR|MINOR) \| (.+?) \| (.+?) \|$',body,re.M)
assert len(rows)==27 and len({r[0] for r in rows})==27
assert all(severities[i]==level and action and reason for i,level,action,reason in rows)
assert sum(v['major'] for v in reviews.values())==20
changes=subprocess.check_output(['git','diff','--name-only','831d5fc','--','submission-jof'],cwd=root,text=True).splitlines()
assert not changes,changes
out=dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',wp='WP6',review_roles=reviews,total_findings=27,major_findings=20,minor_findings=7,dispositions=27,major_without_response_or_reason=0,new_financial_computations=0,new_models_data_tests_or_tuning=False,unresolved_scientific_gaps_explicitly_retained=True,manuscript_integration_not_yet_claimed='WP7 next; currentTeXunchanged inWP6',premature_submission_file_edits=changes,external_or_cross_model_review=False,response_sha256=hashlib.sha256(body.encode()).hexdigest())
(notes/'wp6-acceptance.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
