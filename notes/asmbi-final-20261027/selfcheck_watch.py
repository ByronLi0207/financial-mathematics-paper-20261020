#!/usr/bin/python3
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, time
ROOT=Path(__file__).resolve().parents[2]
N=Path(__file__).resolve().parent
frozen=json.loads((ROOT/'notes/submission/frozen-science.json').read_text())['files']
start=time.monotonic()
next_due=start
while ROOT.exists() and time.monotonic()-start < 8*3600:
    if (N/'STOP_SELFCHECK').exists():break
    if time.monotonic() >= next_due:
        state=json.loads((N/'state.json').read_text())
        bad=[]
        for item in frozen:
            p=ROOT/item['path']
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:
                bad.append(item['path'])
        branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
        row={'utc':datetime.now(timezone.utc).isoformat(),'step':state['current_step'],'branch':branch,'frozen_files':len(frozen),'frozen_mismatches':bad,'status':'PASS' if branch=='submission-final' and not bad else 'BLOCKED'}
        with (N/'selfchecks.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
        with (ROOT/'ASMBI_FINAL_CHANGELOG.md').open('a') as f:f.write('\n### 10-minute self-check\n\n```json\n'+json.dumps(row,ensure_ascii=False,indent=2)+'\n```\n')
        print(json.dumps(row,ensure_ascii=False),flush=True)
        next_due += 600
    time.sleep(5)
