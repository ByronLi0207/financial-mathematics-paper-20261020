"""Run the required suite using the user's authorized temporary dependencies."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import time

R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
prior = json.loads((N / 'R8-pytest.json').read_text())
command = [x for x in prior['command'] if x != '--offline']
command[1:1] = ['--cache-dir', str(R / '.scratch/asmbi-authorized-test-cache')]
env = os.environ.copy()
env.update(prior['environment'])
env.update(UV_PYTHON_DOWNLOADS='never', PYTHONDONTWRITEBYTECODE='1')
started = dt.datetime.now(dt.timezone.utc).isoformat()
t0 = time.monotonic()
q = subprocess.run(command, cwd=R, env=env, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT, text=True)
log = N / 'R8-pytest-authorized-console.txt'
assert not log.exists()
log.write_text(q.stdout)
receipt = {'command': command, 'environment': prior['environment'],
           'authorization': 'User replied 可以 after the explicit temporary test-dependency exception request.',
           'temporary_cache': '.scratch/asmbi-authorized-test-cache',
           'system_python_modified': False, 'python_downloads': False,
           'started_utc': started, 'ended_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
           'seconds': time.monotonic() - t0, 'returncode': q.returncode,
           'log': str(log.relative_to(R)),
           'sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
           'tail': q.stdout.splitlines()[-20:]}
(N / 'R8-pytest-authorized.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
raise SystemExit(q.returncode)
