#!/usr/bin/python3
from pathlib import Path
from datetime import datetime, timezone
import json, shlex, subprocess, sys
ROOT=Path(__file__).resolve().parents[2]
NOTES=Path(__file__).resolve().parent
step,label=sys.argv[1:3]
args=sys.argv[3:]
if args and args[0]=='--':args=args[1:]
start=datetime.now(timezone.utc)
result=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
end=datetime.now(timezone.utc)
record={'step':step,'label':label,'command':args,'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'seconds':(end-start).total_seconds(),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
stamp=start.strftime('%Y%m%dT%H%M%S%fZ')
base=NOTES/'commands'/f'{step}-{label}-{stamp}'
base.with_suffix('.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
raw=f'$ {shlex.join(args)}\n[stdout]\n{result.stdout}\n[stderr]\n{result.stderr}\n[exit] {result.returncode}\n'
base.with_suffix('.txt').write_text(raw)
with (ROOT/'ASMBI_FINAL_CHANGELOG.md').open('a') as f:
    f.write(f'\n### {step} / {label} — {start.isoformat()}\n\n```text\n{raw}```\n')
print(raw,end='')
sys.exit(result.returncode)
