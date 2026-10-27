from pathlib import Path
import json, re, subprocess
R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
fields = ['Authors', 'Affiliations', 'Corresponding author and contact', 'ORCID',
          'Funding', 'Conflict of interest', 'CRediT contributions']
title = (R / 'submission-final/title-page.tex').read_text()
for field in fields:
    assert field + ': [TO BE COMPLETED BY AUTHOR]' in title, field
running = re.search(r'Running title: ([^\\]+)', title).group(1).strip()
assert len(running) <= 70
cover = (R / 'submission-final/cover-letter.tex').read_text()
assert 'Applied Stochastic Models in Business and Industry' in cover
assert 'Three findings' in cover and 'Short training or validation histories' in cover
assert 'Lower forecast scores' in cover and 'gains that depend on the reference' in cover
assert 'Preprint working versions are publicly available' in cover
assert 'TO BE CONFIRMED BY AUTHOR: This manuscript is not under consideration elsewhere' in cover
assert 'submission-final' in cover
assert not re.search(r'AI[- ]use|AI disclosure|artificial intelligence|language model|generative', title + cover, re.I)
build = json.loads((R / 'submission-package/ASMBI/build-report.json').read_text())
pages = {name: build['outputs'][name]['pages'] for name in ['title-page', 'cover-letter']}
assert all(x == 1 for x in pages.values())
for path in ['submission-final/title-page.tex', 'submission-final/cover-letter.tex']:
    before = subprocess.check_output(['git', 'show', '3dba6d9:' + path], cwd=R, text=True)
    (N / (Path(path).stem + '-before-R7.tex')).write_text(before)
result = {'step': 'R7', 'status': 'PASS', 'author_fields': len(fields),
          'running_title': running, 'running_title_characters': len(running),
          'compiled_pages': pages, 'unsupported_author_warranties': 0,
          'pending_author_confirmation': ['Exclusive submission', 'All-author approval', 'Required data permissions'],
          'visual_review': 'Final all-page review in R8'}
(N / 'R7-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
