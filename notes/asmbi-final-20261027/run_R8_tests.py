from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, time
R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
prior = json.loads((R / 'notes/submission/final-tests.json').read_text())
env = os.environ.copy()
env.update(prior['environment'])
started = dt.datetime.now(dt.timezone.utc).isoformat()
t0 = time.monotonic()
q = subprocess.run(prior['command'], cwd=R, env=env, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT, text=True)
log = N / 'R8-pytest-console.txt'
assert not log.exists()
log.write_text(q.stdout)
receipt = dict(command=prior['command'], environment=prior['environment'],
               started_utc=started, ended_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
               seconds=time.monotonic()-t0, returncode=q.returncode,
               log=str(log.relative_to(R)), sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
               tail=q.stdout.splitlines()[-12:])
(N / 'R8-pytest.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
raise SystemExit(q.returncode)
