from pathlib import Path
import datetime as dt, hashlib, json, sys
R=Path(__file__).resolve().parents[2]; N=Path(__file__).resolve().parent
document,pages,observation=sys.argv[1:4]
manifest=json.loads((R/'notes/submission/renders-r8-current-links-final-20261027.json').read_text())
target=next(t for t in manifest['targets'] if t['pdf']==document)
assert hashlib.sha256((R/document).read_bytes()).hexdigest()==target['sha256']
selected=[int(p) for p in pages.split(',')]
record={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pdf':document,
        'pdf_sha256':target['sha256'],'pages':[], 'observation':observation,
        'method':'Root direct view of rendered full-page PNGs with view_image', 'status':'PASS'}
for number in selected:
    page=next(p for p in target['rendered_pages'] if p['page']==number)
    assert hashlib.sha256((R/page['path']).read_bytes()).hexdigest()==page['sha256']
    if any(flag in sys.argv[4:] for flag in ['--from-previous','--from-verified','--from-delivery','--from-closure']):
        prior_name=('renders-r8-closure-final-20261027.json' if '--from-closure' in sys.argv[4:] else
                    'renders-r8-delivery-cut-20261027.json' if '--from-delivery' in sys.argv[4:] else
                    'renders-r8-verified-cut-20261027.json' if '--from-verified' in sys.argv[4:] else
                    'renders-r8-asmbi-final-20261027.json')
        prior=json.loads((R/'notes/submission'/prior_name).read_text())
        old=next(t for t in prior['targets'] if t['pdf']==document)
        oldpage=next(p for p in old['rendered_pages'] if p['page']==number)
        assert hashlib.sha256((R/oldpage['path']).read_bytes()).hexdigest()==oldpage['sha256']==page['sha256']
        page=page|{'viewed_previous_render':oldpage['path'],'pixel_sha256_identical':True}
        record['method']='Root direct view of preceding render, transferred only after exact final PNG byte identity'
    if '--from-preview' in sys.argv[4:]:
        preview=R/'.scratch/submission'/f'r8-supp-orphan-check-page-{number:02}.png'
        assert hashlib.sha256(preview.read_bytes()).hexdigest()==page['sha256']
        page=page|{'viewed_previous_render':str(preview.relative_to(R)),'pixel_sha256_identical':True}
        record['method']='Root direct view of supplementary preview, transferred only after exact final PNG byte identity'
    record['pages'].append(page)
with (N/'R8-direct-visual-review.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='pages'}|{'pages':selected},ensure_ascii=False,indent=2))
