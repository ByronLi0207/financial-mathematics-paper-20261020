"""Synchronize current document snapshots and a closed source-only ZIP.

No earlier authoring builder, scientific input, model or statistical result is
modified. The ZIP has a deterministic member list derived from actual TeX.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DELIVERY = ROOT / 'submission-jof'
STEMS = ('manuscript', 'supplement', 'extended-v9-technical', 'title-page', 'diagnostic-addendum')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def resolve(name, extension=None):
    path = (DELIVERY / name).resolve()
    path.relative_to(DELIVERY.resolve())
    if extension and not path.suffix:
        path = path.with_suffix(extension)
    assert path.is_file() and not path.is_symlink(), path
    return path


def inputs(path):
    text = path.read_text()
    tex = [resolve(x, '.tex') for x in re.findall(r'\\(?:input|include)\{([^}]+)\}', text)]
    figures = [resolve(x, '.pdf') for x in re.findall(
        r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', text)]
    return tex, figures


def closure(path, active=()):
    assert path not in active, 'Cyclic TeX input'
    direct, figures = inputs(path)
    result = {path, *figures}
    for child in direct:
        result.update(closure(child, (*active, path)))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path,
                        default=Path('notes/revision-v9/wp7-deliverable-sync.json'))
    parser.add_argument('--source-bindings', type=Path, default=None,
                        help='Explicit current document-number audit, within notes/revision-v9')
    args = parser.parse_args()
    receipt_target = (ROOT / args.receipt).resolve()
    receipt_target.relative_to((ROOT / 'notes/revision-v9').resolve())
    assert receipt_target.suffix == '.json' and not receipt_target.exists(), 'Choose a fresh receipt before modifying aliases'
    current_bindings = None
    if args.source_bindings is not None:
        binding_path = (ROOT / args.source_bindings).resolve()
        binding_path.relative_to((ROOT / 'notes/revision-v9').resolve())
        assert binding_path.is_file() and not binding_path.is_symlink()
        assert binding_path.suffix == '.json'
        current_bindings = '../notes/revision-v9/' + binding_path.name
    title = re.search(r'\\begin\{center\}\\Large\\bfseries (.*?)\\end\{center\}',
                      resolve('manuscript.tex').read_text()).group(1)
    snapshot_receipts = []
    for stem in STEMS:
        source = resolve(stem + '.tex')
        if stem != 'title-page':
            recursive = sorted(p for p in closure(source) if p != source and p.suffix == '.tex')
            payload = dict(schema='native-tex-source-snapshot-v9-1', title=title,
                           canonical_source=source.name, source_sha256=sha(source.read_bytes()),
                           latex=source.read_text(), recursive_inputs=[dict(
                               path=str(p.relative_to(DELIVERY)), sha256=sha(p.read_bytes()),
                               latex=p.read_text()) for p in recursive],
                           source_bindings=current_bindings or '../notes/revision-v9/' + (
                               'wp7-main-number-audit.json' if stem == 'manuscript' else
                               'wp7-supp-number-audit-after-fixture.json'),
                           meaning='Current source snapshot, not an independent authoring pipeline')
            target = DELIVERY / (stem + '-content.json')
            target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
            readback = json.loads(target.read_text())
            assert readback['latex'].encode() == source.read_bytes()
            for row in readback['recursive_inputs']:
                assert row['latex'].encode() == resolve(row['path']).read_bytes()
                assert row['sha256'] == sha(resolve(row['path']).read_bytes())
            snapshot_receipts.append(dict(path=str(target.relative_to(ROOT)),
                                          sha256=sha(target.read_bytes()),
                                          recursive_inputs=len(recursive)))
        pdf = resolve(stem + '.pdf')
        preview = DELIVERY / (stem + '-preview.pdf')
        preview.write_bytes(pdf.read_bytes())
        assert preview.read_bytes() == pdf.read_bytes()
        snapshot_receipts.append(dict(path=str(preview.relative_to(ROOT)),
                                      exact_pdf_alias=True, sha256=sha(preview.read_bytes())))
    members = {resolve(x) for x in ('main.tex', 'references.bib', 'README.md',
                                    'AUTHOR-TODO.md', 'cover-letter.md')}
    for stem in STEMS:
        members.update(closure(resolve(stem + '.tex')))
    rows = []
    package = DELIVERY / 'overleaf-package.zip'
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(members):
            name = str(p.relative_to(DELIVERY))
            assert p.suffix not in ('.csv', '.npz', '.npy', '.gz')
            assert '.scratch' not in Path(name).parts and '.git' not in Path(name).parts
            data = p.read_bytes()
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, data)
            rows.append(dict(path=name, bytes=len(data), sha256=sha(data)))
    with zipfile.ZipFile(package) as z:
        assert z.namelist() == [r['path'] for r in rows]
        for row in rows:
            assert z.read(row['path']) == resolve(row['path']).read_bytes()
    result = dict(actual_utc=datetime.now(timezone.utc).isoformat(), status='PASS',
                  operation='Current source snapshots, exact preview aliases and source-only ZIP',
                  package=str(package.relative_to(ROOT)), bytes=package.stat().st_size,
                  sha256=sha(package.read_bytes()), members=rows,
                  snapshots_and_aliases=snapshot_receipts,
                  scientific_results_modified=0, financial_models_run=0,
                  isolated_compile_and_visual_QA='Separate required gates')
    receipt_target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('members','snapshots_and_aliases')}, indent=2))


if __name__ == '__main__':
    main()
