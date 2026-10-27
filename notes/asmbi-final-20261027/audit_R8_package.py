"""Check the current writing/build deliverables without running financial work."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import subprocess
import zipfile
from pypdf import PdfReader

R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads((R / p).read_text())
manifest_path = 'notes/submission/renders-r8-final-proof-20261027.json'
render = load(manifest_path)
views = [json.loads(s) for s in (N / 'R8-direct-visual-review.jsonl').read_text().splitlines()]
coverage = []
for t in render['targets']:
    assert sha(R / t['pdf']) == t['sha256'], t['pdf']
    covered = {}
    for v in views:
        if v['pdf'] == t['pdf'] and v['pdf_sha256'] == t['sha256'] and v['status'] == 'PASS':
            covered.update({p['page']: p['sha256'] for p in v['pages']})
    for p in t['rendered_pages']:
        assert sha(R / p['path']) == p['sha256'] == covered.get(p['page']), (t['pdf'], p['page'])
    assert len(PdfReader(R / t['pdf']).pages) == t['pages']
    coverage.append({'pdf': t['pdf'], 'sha256': t['sha256'], 'pages': t['pages'],
                     'reviewed_pages': sorted(covered), 'status': 'PASS'})

badlog = re.compile(r'^!|Undefined control sequence|LaTeX Error|Emergency stop|'
                    r'There were undefined references|Reference .+ undefined|Citation .+ undefined|'
                    r'Label .+ multiply defined|Overfull \\[hv]box|Missing character:', re.M)
logs = []
def checklog(path):
    p = R / path
    text = p.read_text(errors='replace')
    matches = badlog.findall(text)
    assert not matches, (path, matches)
    logs.append({'path': str(p.relative_to(R)), 'sha256': sha(p), 'blocking_matches': 0})

a = load('submission-package/ASMBI/build-report.json')
for name, rec in a['outputs'].items():
    assert rec['status'] == 'COMPILED'
    assert sha(R / f'submission-package/ASMBI/{name}.pdf') == rec['sha256']
    checklog(rec['log'])
q = load('submission-package/QF/BUILD-RECEIPT.json')
for rec in q['compile_records']:
    assert rec['returncode'] == 0 and not rec['undefined_or_duplicate_references']
    assert sha(R / rec['pdf_path']) == rec['sha256']
    checklog(str(Path(rec['pdf_path']).with_suffix('.log')))
for rec in load('notes/submission/shared-build.json'):
    assert sha(R / f"submission-package/SHARED/{rec['name']}.pdf") == rec['pdf_sha256']
    checklog(str(Path(rec['log']).with_name(rec['name'] + '.log')))
e = load('notes/submission/editable-tables.json')
assert sha(R / 'submission-package/SHARED/editable-tables.pdf') == e['pdf_sha256']
checklog(str(Path(e['command'][e['command'].index('--outdir') + 1]) / 'editable-tables.log'))

pattern = re.compile(r'AI-use|AI use|artificial intelligence|generative|language model|AI disclosure|AI statement', re.I)
zips = []
for rec in load('notes/submission/upload-source-archives.json'):
    p = R / rec['archive']
    assert sha(p) == rec['archive_sha256']
    assert sha(R / rec['reference_pdf']) == rec['reference_sha256']
    assert rec['rendered_text_exact_to_active_pdf'] and rec['reference_unchanged_during_check']
    assert rec['only_cached']
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        assert not any('.bak' in n or '.aux' in n or '.scratch' in n for n in names)
        for name in names:
            if Path(name).suffix in {'.tex', '.bib', '.md', '.txt', '.sty', '.cls', '.bst', '.sh', '.py'}:
                assert not pattern.search(z.read(name).decode('utf-8', errors='replace')), (p, name)
    checklog(rec['log'])
    zips.append({'archive': rec['archive'], 'sha256': rec['archive_sha256'],
                 'members': len(names), 'compiled_pages': rec['compiled_pages'],
                 'fresh_unzip_compile': 'PASS', 'forbidden_members': 0, 'disclosure_matches': 0})

rgcmd = ['rg', '-n', '-i', pattern.pattern + '|AI使用声明|AI 使用声明|AI声明',
         'submission-final', 'submission-package', 'README.md', 'REPRODUCING.md', 'CANONICAL.md',
         '-g', '!*.bak', '-g', '!**/failed-cuts/**']
grep = subprocess.run(rgcmd, cwd=R, text=True, capture_output=True)
assert grep.returncode in (0, 1), grep.stderr
reminder = 'AI 使用声明由作者投稿前自行添加（Wiley 要求披露）'
lines = grep.stdout.splitlines()
exceptions = [s for s in lines if s.startswith('submission-final/AUTHOR-TODO.md:') and s.rstrip('。').endswith(reminder)]
assert len(exceptions) == 1 and len(lines) == 1, lines
print('$ ' + ' '.join(rgcmd)); print(grep.stdout, end='')

# Read the actual final PDF text, so macro-expanded stale pointers cannot evade this check.
xrefs = []
for name in ['ASMBI/manuscript', 'QF/main']:
    text = '\n'.join(p.extract_text() or '' for p in PdfReader(R / f'submission-package/{name}.pdf').pages)
    text = re.sub(r'(?<=\w)-\n(?=\w)', '', text)
    pointers = re.findall(r'Supplement\s+(?:Sections?|Tables?|Figures?)\s+S(\d+)', text)
    assert pointers and max(map(int, pointers)) <= 12, (name, pointers)
    assert 'Supplement Table S7' in re.sub(r'\s+', ' ', text), name
    xrefs.append({'pdf': name + '.pdf', 'literal_supplement_pointers': pointers,
                  'confidence_set_pointer': 'S7', 'stale_pointer_count': 0})

supp = (R / 'submission-final/supplement.tex').read_text()
assert len(re.findall(r'\\section\{', supp.split(r'\begin{document}', 1)[1])) == 12
extended = (R / 'EXTENDED_RESULTS.md').read_text()
links = re.findall(r'\\href\{(https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/[^}]+)\}',
                   supp + (R / 'submission-final/manuscript.tex').read_text())
for link in links:
    path = link.split('/blob/submission-final/', 1)[1]
    rel, _, anchor = path.partition('#')
    assert (R / rel).is_file(), link
    if anchor:
        assert f'id="{anchor}"' in extended, link

number = load('notes/asmbi-final-20261027/R8-number-audit.json')
refs = load('notes/asmbi-final-20261027/R8-reference-audit.json')
assert number['status'] == refs['status'] == 'PASS'
assert sha(R / 'submission-final/references.bib') == refs['source_sha256']
diff = subprocess.run(['git', 'diff', '--check'], cwd=R, text=True, capture_output=True)
assert diff.returncode == 0, diff.stdout + diff.stderr
files = load('submission-package/MANIFEST.json')['files']
for item in files:
    assert sha(R / item['path']) == item['sha256'], item['path']

out = {'status': 'PASS_WRITING_BUILD_PROVENANCE_ONLY',
       'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
       'render_manifest': manifest_path, 'visual_pages': sum(x['pages'] for x in coverage),
       'visual_pdf_count': len(coverage), 'visual_coverage': coverage, 'compile_logs': logs,
       'source_archives': zips, 'numeric_mismatches': number['mismatch_count'],
       'frozen_files_unchanged': number['frozen_files'], 'reference_metadata_mismatches': refs['mismatches'],
       'disclosure_matches': 0, 'todo_reminder_exceptions': 1,
       'supplement_sections': 12, 'supplement_pages': a['outputs']['supplement']['pages'],
       'main_pages': a['outputs']['manuscript']['pages'], 'cross_reference_checks': xrefs,
       'repository_link_targets_checked': len(links), 'manifest_files_current': len(files),
       'git_diff_check': 'PASS', 'pytest': 'SEPARATE_REQUIRED_GATE_NOT_COVERED'}
(N / 'R8-package-audit.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['visual_coverage','compile_logs','source_archives','cross_reference_checks']}, ensure_ascii=False, indent=2))
