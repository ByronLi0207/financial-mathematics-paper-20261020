"""Transfer completed page reviews only when final rendered PNG bytes match."""
from pathlib import Path
import datetime as dt
import hashlib
import json

R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
old = json.loads((R / 'notes/submission/renders-r8-current-links-final-20261027.json').read_text())
new = json.loads((R / 'notes/submission/renders-r8-final-proof-20261027.json').read_text())
history = [json.loads(line) for line in (N / 'R8-direct-visual-review.jsonl').read_text().splitlines()]
records = []
for t in new['targets']:
    preceding = next(x for x in old['targets'] if x['pdf'] == t['pdf'])
    assert sha(R / t['pdf']) == t['sha256']
    checked = {}
    for rec in history:
        if rec['pdf'] == preceding['pdf'] and rec['pdf_sha256'] == preceding['sha256'] and rec['status'] == 'PASS':
            checked.update({p['page']: p['sha256'] for p in rec['pages']})
    pages = []
    for p in t['rendered_pages']:
        op = next(x for x in preceding['rendered_pages'] if x['page'] == p['page'])
        assert sha(R / op['path']) == op['sha256'] == checked[p['page']] == p['sha256'] == sha(R / p['path'])
        pages.append(p | {'viewed_previous_render': op['path'], 'pixel_sha256_identical': True})
    records.append({'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pdf': t['pdf'],
                    'pdf_sha256': t['sha256'], 'pages': pages, 'status': 'PASS',
                    'method': 'Final PNG byte identity to every preceding page with a completed direct-view record',
                    'observation': 'Only trailing source whitespace changed in the author preparation attachment; all final page pixels are exact to the completed current-links page reviews.'})
with (N / 'R8-direct-visual-review.jsonl').open('a') as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
print(json.dumps({'status': 'PASS', 'pdfs': len(records), 'pages': sum(len(r['pages']) for r in records),
                  'nonidentical_page_pixels': 0}, indent=2))
