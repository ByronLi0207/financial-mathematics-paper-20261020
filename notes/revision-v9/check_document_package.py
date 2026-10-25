"""Independently compile the closed source ZIP and compare every page.

Only existing cached Tectonic, Poppler, Pillow and pypdf are used. Rendering
and byte/text checks are distinct from the human visual-review receipt.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import argparse
import json
import os
import re
import resource
import subprocess
import time
import zipfile
from pypdf import PdfReader
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'submission-jof'
BASE = ROOT / '.scratch/revision-v9/wp7-document-package'
NOTES = ROOT / 'notes/revision-v9'
ENGINE = '/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic'
RENDER = '/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm'
STEMS = ('manuscript', 'supplement', 'extended-v9-technical', 'title-page')
CONSOLE_PREFIX = 'wp7-package-'
RECEIPT_NAME = 'wp7-isolated-document-package.json'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMBA_NUM_THREADS')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(command, cwd, label):
    out = NOTES / (CONSOLE_PREFIX + label + '-console.txt')
    assert not out.exists()
    begin = time.monotonic()
    with out.open('x') as stream:
        p = subprocess.run(command, cwd=cwd, env=dict(os.environ, **{x:'1' for x in THREADS}),
                           stdout=stream, stderr=subprocess.STDOUT, timeout=590)
    receipt = dict(command=command, returncode=p.returncode,
                   elapsed_seconds=time.monotonic()-begin, output=str(out.relative_to(ROOT)),
                   cumulative_child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    assert p.returncode == 0, receipt
    assert receipt['elapsed_seconds'] < 600
    assert receipt['cumulative_child_peak_rss_bytes'] <= 2 * 1024**3
    return receipt


def main():
    global BASE, CONSOLE_PREFIX, RECEIPT_NAME
    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', default='')
    args = parser.parse_args()
    if args.suffix:
        assert re.fullmatch('[a-z0-9-]+', args.suffix)
        BASE = BASE.with_name(BASE.name + '-' + args.suffix)
        CONSOLE_PREFIX = 'wp7-package-' + args.suffix + '-'
        RECEIPT_NAME = 'wp7-isolated-document-package-' + args.suffix + '.json'
    assert not (NOTES / RECEIPT_NAME).exists(), 'Preserve previous gate evidence'
    BASE.mkdir(parents=True, exist_ok=False)
    source = BASE / 'sources'
    source.mkdir()
    member_rows = []
    with zipfile.ZipFile(D / 'overleaf-package.zip') as z:
        names = z.namelist()
        assert len(names) == len(set(names))
        for name in names:
            path = Path(name)
            assert not path.is_absolute() and '..' not in path.parts
            assert '.scratch' not in path.parts and '.git' not in path.parts
            assert z.read(name) == (D/name).read_bytes()
            member_rows.append(dict(path=name, sha256=sha(D/name)))
        z.extractall(source)
    rows = []
    for stem in STEMS:
        out = BASE / (stem + '-rebuilt')
        out.mkdir()
        c = run([ENGINE, '-X', 'compile', '--only-cached', stem+'.tex',
                 '--outdir', str(out), '--keep-logs', '--keep-intermediates'], source, stem+'-compile')
        log = (out/(stem+'.log')).read_text(errors='replace')
        bad = [x for x in log.splitlines() if re.search(
            r'(^!|undefined|Missing character|Overfull|^\s*(?:fatal\s+)?error\b|LaTeX Error:|Package \S+ Error:)', x, re.I)]
        assert not bad, bad
        current, rebuilt = D/(stem+'.pdf'), out/(stem+'.pdf')
        a, b = PdfReader(current), PdfReader(rebuilt)
        texts_a, texts_b = [p.extract_text() for p in a.pages], [p.extract_text() for p in b.pages]
        assert texts_a == texts_b and len(a.pages) == len(b.pages)
        assert all(t.strip() and '\ufffd' not in t and '??' not in t for t in texts_a)
        viewed = BASE / (stem+'-canonical')
        viewed.mkdir()
        render_a = run([RENDER, '-r', '125', '-png', str(current), str(viewed/'page')],
                       ROOT, stem+'-canonical-render')
        render_b = run([RENDER, '-r', '125', '-png', str(rebuilt), str(out/'page')],
                       ROOT, stem+'-rebuilt-render')
        first = sorted(viewed.glob('page-*.png'))
        second = sorted(out.glob('page-*.png'))
        assert len(first) == len(second) == len(a.pages)
        pixels = []
        for page, (x, y) in enumerate(zip(first, second), 1):
            with Image.open(x) as im_a, Image.open(y) as im_b:
                aa, bb = im_a.convert('RGB'), im_b.convert('RGB')
                assert aa.size == bb.size and aa.tobytes() == bb.tobytes(), (stem, page)
                size = aa.size
            pixels.append(dict(page=page, canonical_png=str(x.relative_to(ROOT)),
                               rebuilt_png=str(y.relative_to(ROOT)), canonical_png_sha256=sha(x),
                               rebuilt_png_sha256=sha(y), pixels_identical=True, dimensions=size))
        rows.append(dict(stem=stem, pages=len(a.pages), canonical_pdf_sha256=sha(current),
                         rebuilt_pdf_sha256=sha(rebuilt), source_sha256=sha(source/(stem+'.tex')),
                         every_page_text_identical=True, every_page_pixels_identical=True,
                         error_undefined_missing_glyph_overfull=[], compile=c,
                         renders=[render_a, render_b], pages_proof=pixels))
        print(stem, len(a.pages), 'pages: all text and pixels identical; visual review separate', flush=True)
    result = dict(actual_utc=datetime.now(timezone.utc).isoformat(), status='PASS',
                  package_sha256=sha(D/'overleaf-package.zip'), members=member_rows, documents=rows,
                  total_pages=sum(x['pages'] for x in rows), isolated_source=str(source.relative_to(ROOT)),
                  cumulative_child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  root_process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  installed_packages=0, network_downloads=0, raw_financial_inputs=0,
                  financial_models_run=0, visual_review_performed_here=False,
                  public_financial_replay='Separate; missing original local Git objects/rights-cleared raw input not repaired')
    path = NOTES / RECEIPT_NAME
    assert not path.exists()
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('documents','members')}, indent=2))


if __name__ == '__main__':
    main()
