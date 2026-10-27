#!/usr/bin/python3
from pathlib import Path
from datetime import datetime, timezone
import json, os, sys
N=Path(__file__).resolve().parent
R=N.parents[1]
step=sys.argv[1]
proof=json.loads((N/(step+'-verification.json')).read_text())
assert proof['status']=='PASS',proof
state=json.loads((N/'state.json').read_text())
assert state['current_step']==step,(state['current_step'],step)
order=[*[f'R{i}' for i in range(10)],'C1','C2','C3']
assert all(state['steps'][x]=='PASS' for x in order[:order.index(step)])
now=datetime.now(timezone.utc)
state.setdefault('timings',{})[step]={'started_utc':state['step_started_utc'],'finished_utc':now.isoformat(),'seconds':(now-datetime.fromisoformat(state['step_started_utc'])).total_seconds()}
state['steps'][step]='PASS'
state['current_step']=order[order.index(step)+1] if step!=order[-1] else 'COMPLETE'
state['step_started_utc']=now.isoformat()
p=N/'state.json.tmp'
p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
os.replace(p,N/'state.json')
with (R/'ASMBI_FINAL_CHANGELOG.md').open('a') as f:f.write(f'\n## {step}: PASS\n\n验收：`notes/asmbi-final-20261027/{step}-verification.json`；原始命令和输出见本节之前记录。完成UTC：`{now.isoformat()}`。\n')
print(step+': PASS; next='+state['current_step'])
