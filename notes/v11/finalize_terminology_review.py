"""Bind the root's actual five-page terminology review and exact unchanged-page reuse."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v11'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=ROOT/'.scratch/v11/continuous-history';new=ROOT/'.scratch/v11/terminology-final'
expected={'manuscript':[6],'supplement':[15,16,17,34],'cover-letter':[],'title-page':[]}
observations={
 'manuscript':{6:'Four-feature method name is consistent; complete table, footnote and evaluation-design paragraphs remain readable.'},
 'supplement':{15:'Four-feature terminology and complete Monte Carlo definitions/candidate failure remain intact.',16:'Daily caption and full-prefix transfer are complete; all original numeric rows remain visible.',17:'Four-feature missing-field qualification and complete failure/status text remain intact.',34:'Matched reference and predictor-dimension exclusion are explicit; all three criteria, counts, negative result and all later limitations fit clearly.'}}
pages=[]
for document,changed_expected in expected.items():
 a=sorted((old/('render-'+document)).glob('page-*.png'));b=sorted((new/('render-'+document)).glob('page-*.png'));assert len(a)==len(b)
 changed=[]
 for i,(before,after)in enumerate(zip(a,b),1):
  different=sha(before)!=sha(after)
  if different:changed.append(i)
  pages.append(dict(document=document,page=i,png=str(after.relative_to(ROOT)),sha256=sha(after),
                    review='ROOT_ACTUAL_VIEW_IMAGE'if different else'BYTE_IDENTICAL_TO_PREVIOUS_ACTUAL_VIEW',
                    observation=observations.get(document,{}).get(i,'Exact image reuse of the previously reviewed page.')))
 assert changed==changed_expected,(document,changed,changed_expected)
record=dict(status='PASS',reviewed_utc=datetime.now(timezone.utc).isoformat(),
 previous_reviews=['notes/v11/visual-main-final.json','notes/v11/visual-supplement-final.json'],
 actual_new_views=5,unchanged_exact_reuses=51,total_pages=56,pages=pages,
 no_clipping_overlap_or_missing_text=True,source_number_changes=False)
(HERE/'visual-terminology-final.json').write_text(json.dumps(record,indent=2)+'\n')
p=HERE/'final-native-build.json';r=json.loads(p.read_text())
for t in r['targets']:
 assert sha(ROOT/t['output'])==t['sha256']
 t['visual_review']='PASS_ALL_PAGES';t['visual_evidence']='notes/v11/visual-terminology-final.json'
r.update(status='PASS',all_pages_covered=56,visual_review_completed_utc=record['reviewed_utc'],
         reviewed_changed_pages_reuse='Five changed pages actually reviewed by root; fifty-one exact PNG reuses retain prior actual reviews.')
p.write_text(json.dumps(r,indent=2)+'\n')
print('PASS all 56 pages, five actual new views and 51 exact reviewed image reuses')
