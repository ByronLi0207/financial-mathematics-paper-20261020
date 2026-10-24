"""Record actual commands and unabridged stdout/stderr under ordered review items."""
from datetime import datetime,timezone
from pathlib import Path
import json,os,re,shlex,subprocess
from v3_revision import ROOT,write,dump
OUT=ROOT/'results/revision-20261023/round2/evidence'

def append(step,text):
    p=ROOT/'REVISION_V3_CHANGELOG.md';s=p.read_text();marker='\n## 待用户决定\n';assert marker in s
    heading='### Round2 '+step+' — '
    if heading not in s:s=s.replace(marker,'\n\n'+heading+'IN PROGRESS\n'+marker)
    start=s.index(heading);match=re.search(r'\n#{2,3} ',s[start+len(heading):]);end=start+len(heading)+match.start() if match else len(s)
    s=s[:end]+'\n\n'+text.strip()+'\n'+s[end:];write(p,s)

def run(step,argv,env=None,timeout=600,allow_failure=False):
    OUT.mkdir(parents=True,exist_ok=True);i=1
    while (OUT/(step+f'-{i:03}.json')).exists():i+=1
    delta=env or {};actual=os.environ.copy();actual.update(delta);start=datetime.now(timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=ROOT,env=actual,capture_output=True,text=True,timeout=timeout)
    end=datetime.now(timezone.utc).isoformat();command=shlex.join(['env',*[k+'='+v for k,v in delta.items()],*map(str,argv)]) if delta else shlex.join(list(map(str,argv)))
    record=dict(step=step,command=command,argv=list(map(str,argv)),environment_delta=delta,started_utc=start,ended_utc=end,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    dump(OUT/(step+f'-{i:03}.json'),record)
    append(step,'Command (actual):\n\n```sh\n'+command+'\n```\n\nReturn code: '+str(p.returncode)+'\n\nSTDOUT (verbatim):\n\n```text\n'+p.stdout+'\n```\n\nSTDERR (verbatim):\n\n```text\n'+p.stderr+'\n```')
    print(json.dumps(dict(step=step,receipt=str((OUT/(step+f'-{i:03}.json')).relative_to(ROOT)),returncode=p.returncode,stdout=p.stdout,stderr=p.stderr),ensure_ascii=False))
    if p.returncode and not allow_failure:raise subprocess.CalledProcessError(p.returncode,argv)
    return record

def finish(step,summary,status='COMPLETE'):
    p=ROOT/'state/round2-state.json';s=json.loads(p.read_text());assert s['order'][len(s['completed'])]==step,(step,s['completed'])
    append(step,summary);ledger=ROOT/'REVISION_V3_CHANGELOG.md';write(ledger,ledger.read_text().replace('### Round2 '+step+' — IN PROGRESS','### Round2 '+step+' — '+status))
    s['tasks'][step]=status;s['completed'].append(step);s['current']=s['order'][len(s['completed'])] if len(s['completed'])<len(s['order']) else 'DONE';dump(p,s)
