"""Record actual ten-minute checks; never backfill missed checks or work time."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    path = root / 'notes/revision-v6/state.json'
    state = json.loads(path.read_text())
    now = datetime.now(timezone.utc)
    due = datetime.fromisoformat(state['next_self_check_utc'])
    if now < due:
        print('NOT_DUE', now.isoformat(), 'next', due.isoformat())
        raise SystemExit(0)
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=root, text=True).strip()
    allowed = set(state.get('allowed_v6_changes', []))
    changed, missing = [], []
    for name, expected in state['protected_v5_sha256'].items():
        p = root / name
        if not p.is_file():
            missing.append(name)
        elif hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            changed.append(name)
    unauthorized = sorted(set(changed) - allowed)
    start = datetime.fromisoformat(state['start_utc'])
    elapsed = (now - start).total_seconds()
    check = dict(actual_utc=now.isoformat(), scheduled_due_utc=due.isoformat(),
        lateness_seconds=(now-due).total_seconds(), elapsed_window_seconds=elapsed,
        current_wp=state['current_wp'], branch=branch,
        protected_file_count=len(state['protected_v5_sha256']),
        allowed_modified=sorted(set(changed) & allowed),
        unauthorized_modified=unauthorized, missing=missing,
        deadline_reached=now >= datetime.fromisoformat(state['deadline_utc']),
        idle_or_parallel_time_credited_as_reading=False,
        status='PASS' if branch == state['branch'] and not unauthorized and not missing else 'ATTENTION')
    state['checks'].append(check)
    state['next_self_check_utc'] = (start + timedelta(seconds=(int(elapsed)//600+1)*600)).isoformat()
    state['last_self_check_utc'] = now.isoformat()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n')
    out = root / 'notes/revision-v6' / ('self-check-%03d.json' % len(state['checks']))
    with out.open('x') as stream:
        json.dump(check, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(check, ensure_ascii=False))
    raise SystemExit(0 if check['status'] == 'PASS' else 1)
