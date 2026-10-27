"""Snapshot and package the saved v9 documents; no research computation."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'submission-jof'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(name, seen=None):
    seen = set() if seen is None else seen
    if name in seen:
        return []
    seen.add(name)
    out = [name]
    for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', (DOC / name).read_text()):
        child += '' if Path(child).suffix else '.tex'
        out += sources(child, seen)
    return out


def run(build_root, receipt):
    audit = ROOT / 'notes/v9/main-number-audit-c6-final.json'
    checked = json.loads(audit.read_text())
    assert checked['current']['main_sha256'] == sha(DOC / 'manuscript.tex')
    assert checked['current']['supplement_sha256'] == sha(DOC / 'supplement.tex')
    assert checked['status'].startswith('PASS'), checked['status']
    inputs = sorted(set(sources('main.tex') + sources('supplement.tex') + sources('title-page.tex')))
    figures = set()
    for name in inputs:
        for graphic in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', (DOC / name).read_text()):
            graphic += '' if Path(graphic).suffix else '.pdf'
            figures.add(graphic)
    assert len([n for n in inputs if n.startswith('generated/')]) == 10
    for stem in ('manuscript', 'supplement', 'title-page'):
        pdf = build_root / stem / (stem + '.pdf')
        assert pdf.is_file(), pdf
        for name in (stem + '.pdf', stem + '-preview.pdf'):
            shutil.copy2(pdf, DOC / name)
    title = re.search(r'\\begin\{center\}.*?bfseries (.*?)\\end\{center\}', (DOC / 'manuscript.tex').read_text()).group(1)
    for stem in ('manuscript', 'supplement'):
        source = DOC / (stem + '.tex')
        snap = dict(schema='v9-current-native-latex-snapshot', title=title,
                    canonical_source=source.name, source_sha256=sha(source), latex=source.read_text(),
                    recursive_inputs=[dict(path=n, sha256=sha(DOC / n), latex=(DOC / n).read_text()) for n in sources(source.name)[1:]],
                    source_bindings='../notes/v9/main-number-audit-c6-final.json',
                    historical_v6_schema=f'../manuscript/revision-v6-preserved/{stem}-content.json',
                    historical_v7_source_commit='b571f324a253480b4e39bc8a8096775ddbcc7017',
                    meaning='Current saved source and recursive TeX inputs; not a second authoring pipeline')
        (DOC / (stem + '-content.json')).write_text(json.dumps(snap, indent=2, ensure_ascii=False) + '\n')
    members = sorted(set(inputs) | figures | {'references.bib', 'README.md', 'AUTHOR-TODO.md', 'cover-letter.md', 'cover-letter.tex'})
    package = DOC / 'overleaf-package.zip'
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name in members:
            p = DOC / name
            assert p.is_file() and not p.is_symlink(), p
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 24, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(package) as z:
        assert z.testzip() is None
        assert z.namelist() == members
        assert all(z.read(n) == (DOC / n).read_bytes() for n in members)
    result = dict(utc=datetime.now(timezone.utc).isoformat(), stage='C6',
                  script_sha256=sha(Path(__file__)), numeric_audit_sha256=sha(audit),
                  source_input_count=len(inputs), generated_input_count=10, figure_input_count=len(figures),
                  members={n:dict(bytes=(DOC / n).stat().st_size, sha256=sha(DOC / n)) for n in members},
                  package_bytes=package.stat().st_size, package_sha256=sha(package),
                  current_pdfs={stem:dict(sha256=sha(DOC / (stem + '.pdf')), preview_alias_equal=(DOC / (stem + '.pdf')).read_bytes() == (DOC / (stem + '-preview.pdf')).read_bytes()) for stem in ('manuscript', 'supplement', 'title-page')},
                  all_members_match_current_sources=True, raw_data_included=False, results_recomputed=False,
                  final_tests_visual_publication='C7 pending; this seals document inputs only')
    with receipt.open('x') as f:
        json.dump(result, f, indent=2); f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='members'}, indent=2))


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-root', type=Path, required=True)
    p.add_argument('--receipt', type=Path, required=True)
    a=p.parse_args(); run(a.build_root, a.receipt)
