#!/usr/bin/env python3
"""Build ASMBI files from the current canonical text and official Wiley NJDv5.

This is a packaging transform only. It does not edit canonical files or run
research calculations. PDFs use cached Tectonic resources only. Re-run after
canonical editorial revisions; every changed existing output is backed up.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import runpy
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

TECTONIC = Path('/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic')
PDFINFO = Path('/Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo')
ROOT = Path(__file__).resolve().parents[2]
STAMP = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
INPUTS: dict[str, str] = {}
BACKUPS: list[str] = []


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_input(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        label = str(path.relative_to(ROOT))
    except ValueError:
        label = str(path)
    INPUTS[label] = digest(data)
    return data


def backup(path: Path) -> None:
    if path.exists():
        candidate = path.with_name(path.name + '.bak')
        if candidate.exists():
            candidate = path.with_name(path.name + '.' + STAMP + '.bak')
        shutil.copy2(path, candidate)
        BACKUPS.append(str(candidate.relative_to(ROOT)))


def write(path: Path, data: str | bytes) -> None:
    raw = data.encode('utf-8') if isinstance(data, str) else data
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == raw:
        return
    backup(path)
    path.write_bytes(raw)


def expand(path: Path, seen: tuple[Path, ...] = ()) -> str:
    if path in seen:
        raise ValueError(f'Circular TeX input: {path}')
    text = read_input(path).decode('utf-8')

    def replace(match: re.Match[str]) -> str:
        # TeX resolves nested \input paths from the compilation working
        # directory, not from the directory of the including .tex file.
        sub = ROOT / 'submission-final' / match.group(1)
        if not sub.suffix:
            sub = sub.with_suffix('.tex')
        return expand(sub.resolve(), seen + (path,))

    return re.sub(r'\\input\{([^}]+)\}', replace, text)


def numeric_citations(text: str, authors: dict[str, str],
                      audit: list[dict] | None = None) -> str:
    """Format numeric citations without asking AMA BBLs for author labels.

    The official AMA bibliography supplies numeric items only. Emit the
    verified author text explicitly for the three authorized narrative keys,
    then use the same superscript numeric citation as the rest of the paper.
    """
    numeric = re.sub(r'\\cite(?:p|alp)\b', r'\\cite', text)
    edits = []

    def textual(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in authors:
            raise ValueError(f'No verified AMA narrative-author mapping: {key}')
        before = match.group(0)
        after = authors[key] + r'\cite{' + key + '}'
        edits.append(dict(key=key, before=before, after=after))
        return after

    formatted = re.sub(r'\\citet\{([^}]+)\}', textual, numeric)
    if re.search(r'\\citet\b', formatted):
        raise ValueError('Unsupported textual citation syntax in AMA package')
    restored = formatted
    for edit in reversed(edits):
        restored = restored.replace(edit['after'], edit['before'], 1)
    if restored != numeric:
        raise AssertionError('Narrative citation transform changed non-citation text')
    if audit is not None:
        audit.extend(dict(**edit, non_citation_text_preserved=True,
                          reversible_to_canonical_citation=True) for edit in edits)
    return formatted


def bib_fields(entry: str) -> dict[str, dict]:
    """Read brace-delimited fields without changing their factual content."""
    head = re.match(r'@[A-Za-z]+\s*\{\s*[^,\s]+\s*,', entry)
    fields = {}
    pos = head.end()
    while pos < len(entry) - 1:
        match = re.match(r'[\s,]*([A-Za-z_]+)\s*=\s*', entry[pos:])
        if not match:
            break
        name = match.group(1).lower()
        start = pos + match.end()
        if entry[start] != '{':
            raise ValueError(f'Expected brace-delimited canonical field: {name}')
        end = start + 1
        depth = 1
        while depth:
            if entry[end] == '{' and entry[end-1] != '\\':
                depth += 1
            elif entry[end] == '}' and entry[end-1] != '\\':
                depth -= 1
            end += 1
        fields[name] = dict(value=entry[start+1:end-1], start=start+1, end=end-1)
        pos = end
    return fields


def set_bib_field(entry: str, field: str, value: str) -> str:
    fields = bib_fields(entry)
    if field in fields:
        f = fields[field]
        return entry[:f['start']] + value + entry[f['end']:]
    ending = entry[:-1].rstrip()
    if not ending.endswith(','):
        ending += ','
    return ending + '\n  ' + field + ' = {' + value + '}\n}'


def verified_narrative_authors(bib: bytes, metadata: dict) -> tuple[dict[str, str], list[dict]]:
    """Derive only the three authorized author labels from verified records."""
    keys = ('LeeKim2024ASMBI', 'Pagnottoni2026ASMBI', 'MuddanaEtAl2025ASMBI')
    records = {record['id']: record for record in metadata['records']}
    bib_text = bib.decode('utf-8')
    labels = {}
    audit = []
    normalize = lambda value: re.sub(r'\s+', ' ', re.sub(r'[{}]', '', value)).strip()
    for key in keys:
        record = records[key]
        match = re.search(r'@[A-Za-z]+\s*\{\s*' + re.escape(key) + r'\s*,', bib_text)
        if match is None:
            raise ValueError(f'Canonical BibTeX lacks narrative key: {key}')
        # bib_fields stops at the first entry-closing brace; no subsequent
        # entry is read or changed by this factual-field check.
        fields = bib_fields(bib_text[match.start():])
        author = fields['author']['value']
        if normalize(author) != normalize(record['bibtex_fields']['author']):
            raise ValueError(f'Canonical/verified author mismatch: {key}')
        if fields['doi']['value'].strip() != record['doi']:
            raise ValueError(f'Canonical/verified DOI mismatch: {key}')
        families = [person['family'] for person in record['authors']]
        if not families or any(not name.strip() for name in families):
            raise ValueError(f'Incomplete verified family names: {key}')
        label = (families[0] if len(families) == 1 else
                 ' and '.join(families) if len(families) == 2 else
                 families[0] + ' et al.')
        labels[key] = label
        audit.append(dict(key=key, author_display=label,
                          canonical_bib_author=author, verified_authors=record['authors'],
                          doi=record['doi'], official_url=record['official_url'],
                          metadata_source='notes/submission/asmbi-recent-literature.json',
                          metadata_json_pointer='/records/' + str(metadata['records'].index(record)),
                          author_facts_identical=True))
    return labels, audit


def ama_bibliography(data: bytes, canonical_source: str = '') -> tuple[str, list[dict]]:
    """Keep all canonical facts; map institutional metadata to AMA fields.

    The supplied Wiley BST assumes optional fields exist even when empty.
    This derivative prevents BibTeX missing-field errors without editing its
    official bytes or changing the canonical .bib file.
    """
    text = data.decode('utf-8')
    edits = []
    parts = []
    cursor = 0
    pattern = re.compile(r'@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,')
    while (match := pattern.search(text, cursor)):
        depth = 1
        pos = match.end()
        while depth:
            ch = text[pos]
            if ch == '{' and (pos == 0 or text[pos-1] != '\\'):
                depth += 1
            elif ch == '}' and (pos == 0 or text[pos-1] != '\\'):
                depth -= 1
            pos += 1
        entry = text[match.start():pos]
        original_fields = {k:v['value'] for k,v in bib_fields(entry).items()}
        institution = original_fields.get('institution', '')
        added = {}
        for field in ('school', 'organization', 'address', 'howpublished'):
            if field not in original_fields:
                value = institution if field in {'school', 'howpublished'} else ''
                added[field] = value
                entry = set_bib_field(entry, field, value)
        key = match.group(1)
        manual = re.search(r'\\bibitem(?:\[[^\n]*?\])?\{' + re.escape(key) + r'\}(.*?)(?=\\bibitem|\\end\{thebibliography\})', canonical_source, re.S)
        if 'year' not in original_fields and manual and '(n.d.)' in manual.group(1):
            entry = set_bib_field(entry, 'year', 'n.d.')
            added['year'] = 'n.d.'
        if key == 'hoogen2017' and original_fields.get('author') == 'van den Hoogen, S.':
            entry = set_bib_field(entry, 'author', '{van den Hoogen}, S.')
        entry_type = re.match(r'@([A-Za-z]+)', entry).group(1).lower()
        if entry_type in {'misc', 'mastersthesis', 'phdthesis', 'inproceedings'} and original_fields.get('url'):
            url = original_fields['url'].replace(r'\_', '_').replace(r'\%', '%').replace(r'\&', '&')
            note = original_fields.get('note', '').strip()
            if url not in note:
                note = (note + ('' if note.endswith(('.', ';', ':')) else '.') + ' ' if note else '') + '\\url{' + url + '}'
                entry = set_bib_field(entry, 'note', note)
        after = {k:v['value'] for k,v in bib_fields(entry).items()}
        protected = {k:after[k] == value for k,value in original_fields.items() if k not in {'author', 'note'}}
        assert all(protected.values()), f'Canonical bibliography fact changed: {key}'
        assert re.sub(r'[{}]', '', after.get('author', '')) == re.sub(r'[{}]', '', original_fields.get('author', ''))
        assert original_fields.get('note', '') in after.get('note', '')
        edits.append(dict(key=key, added_fields=added,
                          before=original_fields, after=after,
                          unchanged_original_fields=protected,
                          author_text_preserved_ignoring_grouping=True,
                          existing_note_preserved=True,
                          missing_year_source='canonical manual bibliography' if 'year' in added else None))
        parts += [text[cursor:match.start()], entry]
        cursor = pos
    parts.append(text[cursor:])
    return ''.join(parts), edits


def clean_ama_bbl(text: str) -> tuple[str, list[dict]]:
    """Remove empty-field/editor punctuation while preserving every word/number."""
    edits = []
    pattern = re.compile(r'\\bibitem\{([^}]+)\}.*?(?=\\bibitem\{|\\end\{thebibliography\})', re.S)

    def clean(match: re.Match[str]) -> str:
        before = match.group(0)
        after = re.sub(r'(\\bibitem\{[^}]+\}\s*\{[^{}]+\})\s+\.', r'\1.', before, count=1)
        after = re.sub(r'\.\s*\\kern-2pt,\s*(eds?\.)', r', \1', after)
        after = re.sub(r'\.\s*:\s*(?=\d{4}\.)', '; ', after)
        after = re.sub(r',\s*;\s*(?=\d{4}\.)', '; ', after)
        after = re.sub(r'\.\s*;\s*(?=n\.d\.)', '. ', after)
        after = re.sub(r'\.\s*;\s*\.', '.', after)
        tokens = lambda s: re.findall(r'[A-Za-z0-9]+', s.replace(r'\kern-2pt', ''))
        assert tokens(before) == tokens(after), f'BBL content changed: {match.group(1)}'
        if before != after:
            edits.append(dict(key=match.group(1), before=before, after=after,
                              all_word_and_number_tokens_identical=True))
        return after

    cleaned = pattern.sub(clean, text)
    if '\\interlinepenalty=10000' not in cleaned:
        cleaned = re.sub(r'(\\begin\{thebibliography\}\{[^}]+\}\n)(?:\\raggedright\n)?',
                         lambda m: m.group(1) + '\\raggedright\n\\interlinepenalty=10000\n',
                         cleaned, count=1)
    return cleaned, edits


def split_tables(text: str) -> tuple[str, list[str]]:
    tables: list[str] = []

    def move(match: re.Match[str]) -> str:
        tables.append(match.group(0))
        return f'% ASMBI_TABLE_{len(tables):02d}\n'

    moved = re.sub(r'\\begin\{table\}(?:\[[^]]*\])?.*?\\end\{table\}', move, text, flags=re.S)
    rebuilt = moved
    for i, table in enumerate(tables, 1):
        rebuilt = rebuilt.replace(f'% ASMBI_TABLE_{i:02d}\n', table)
    if rebuilt != text:
        raise AssertionError('Table movement changed manuscript content')
    return moved, tables


def standard_preamble() -> str:
    return r'''\input{asmbi-template-compat.tex}
\documentclass[AMA,Times1COL]{WileyNJDv5}
\let\LoadClass\ASMBIoriginalLoadClass
% Official Wiley NJDv5 class is copied without modification. The journal's
% 12pt manuscript requirement overrides the template's smaller default body.
\usepackage{amsmath,amssymb,array,longtable,placeins}
\usepackage[unicode,breaklinks=true,hidelinks]{hyperref}
\makeatletter
\renewcommand\normalsize{\@setfontsize\normalsize{12}{15}%
  \abovedisplayskip 10pt plus2pt minus3pt
  \belowdisplayskip\abovedisplayskip
  \abovedisplayshortskip 0pt plus3pt
  \belowdisplayshortskip 6pt plus3pt minus3pt}
\renewcommand\small{\@setfontsize\small{10}{12}}
\renewcommand\footnotesize{\@setfontsize\footnotesize{9}{11}}
\renewcommand\scriptsize{\@setfontsize\scriptsize{8}{10}}
\renewcommand\abstractfont{\normalfont\fontsize{12}{15}\selectfont}
\renewcommand\keywordsfont{\normalfont\fontsize{12}{15}\selectfont}
\makeatother
\AtBeginDocument{\normalsize\typeout{ASMBI_BODY_FONT_PT=12}}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{3pt}
\clubpenalty=10000\widowpenalty=10000
\raggedbottom
'''


def free_format_preamble() -> str:
    return r'''\documentclass[12pt,a4paper]{article}
% Official ASMBI Free Format initial-submission route. This is explicitly
% distinct from an NJDv5 typeset PDF; the original NJDv5 sources accompany it.
\usepackage[margin=20mm]{geometry}
% XeTeX uses the cached default Computer Modern fonts. Loading T1 here
% would select uncached Latin Modern Type1 metrics/physical fonts.
\usepackage{amsmath,amssymb,graphicx,booktabs,array,longtable,placeins}
\usepackage[numbers,super,sort&compress]{natbib}
\usepackage{caption}
\usepackage[unicode,breaklinks=true,hidelinks]{hyperref}
\bibliographystyle{WileyNJD-AMA}
% Four font files come from the downloaded official Wiley template. Direct
% Unicode font declarations avoid uncached Latin Modern optical-size files.
\DeclareFontFamily{TU}{asmbifree}{}
\DeclareFontShape{TU}{asmbifree}{m}{n}{<->\UnicodeFontFile{Fonts/MinionPro/MinionPro-Regular}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{asmbifree}{m}{it}{<->\UnicodeFontFile{Fonts/MinionPro/MinionPro-It}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{asmbifree}{bx}{n}{<->\UnicodeFontFile{Fonts/MinionPro/MinionPro-Bold}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{asmbifree}{bx}{it}{<->\UnicodeFontFile{Fonts/MinionPro/MinionPro-BoldIt}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{asmbifree}{b}{n}{<->ssub*asmbifree/bx/n}{}
\DeclareFontShape{TU}{asmbifree}{b}{it}{<->ssub*asmbifree/bx/it}{}
\DeclareFontShape{TU}{asmbifree}{m}{sl}{<->ssub*asmbifree/m/it}{}
\renewcommand\rmdefault{asmbifree}
\normalfont
% The template's natbib file expects an NJD section command. Free Format
% supplies the ordinary article bibliography heading instead.
\renewcommand\bibsection{\section*{References}}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{3pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\clubpenalty=10000\widowpenalty=10000
\captionsetup{font=small,labelfont=bf}
\AtBeginDocument{\typeout{ASMBI_BODY_FONT_PT=12}}
\raggedbottom
'''


def metadata(title: str, abstract: str = '', keywords: str = '') -> str:
    text = r'''\articletype{Research Article}
\journal{Applied Stochastic Models in Business and Industry}
\copyyear{2026}
\startpage{1}
\title{''' + title + r'''}
\author[1]{[AUTHOR NAME TO BE COMPLETED]}
\address[1]{[AFFILIATION TO BE COMPLETED BY AUTHOR]}
\corres{[CORRESPONDING AUTHOR AND CONTACT TO BE COMPLETED]}
\authormark{[AUTHOR TO BE COMPLETED]}
\titlemark{Historical Rules and Peak Limits}
'''
    if abstract:
        text += '\\abstract[Abstract]{' + abstract + '}\n'
    if keywords:
        text += '\\keywords{' + keywords + '}\n'
    return text


def compile_tex(out: Path, scratch: Path, stem: str) -> dict:
    dest = scratch / STAMP / stem
    dest.mkdir(parents=True, exist_ok=True)
    command = [str(TECTONIC), '-X', 'compile', '-C', '--keep-logs',
               '--keep-intermediates', '--outdir', str(dest), stem + '.tex']
    result = subprocess.run(command, cwd=out, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    console = dest / 'console.txt'
    write(console, result.stdout)
    logpath = dest / (stem + '.log')
    log = logpath.read_text(errors='replace') if logpath.exists() else ''
    warnings = [line.strip() for line in (result.stdout + '\n' + log).splitlines()
                if re.search(r'warning|overfull|underfull|undefined|not found|error:', line, re.I)]
    if result.returncode or not (dest / (stem + '.pdf')).exists():
        # A stale PDF from an earlier successful run must never be confused
        # with this failed current build.
        stale = out / (stem + '.pdf')
        retained = None
        if stale.exists():
            backup(stale)
            retained = dict(path=str(stale.relative_to(ROOT)), sha256=digest(stale.read_bytes()),
                            status='PREVIOUS_PDF_RETAINED_NOT_A_CURRENT_OUTPUT')
        return dict(status='FAIL_COMPILE', command=command, returncode=result.returncode,
                    console=str(console.relative_to(ROOT)), warnings=warnings,
                    log=str(logpath.relative_to(ROOT)), pages=None,
                    current_pdf_produced=False, previous_pdf_retained=retained)
    saved_bbl = dest / (stem + '.bbl')
    tex_path = out / (stem + '.tex')
    if stem in {'manuscript', 'supplement'} and '\\bibliography{references-ama}' in tex_path.read_text() and saved_bbl.exists():
        raw_bbl = saved_bbl.read_text()
        cleaned_bbl, bbl_edits = clean_ama_bbl(raw_bbl)
        write(out / (stem + '.bbl'), cleaned_bbl)
        write(tex_path, tex_path.read_text().replace('\\bibliography{references-ama}', '\\input{' + stem + '.bbl}', 1))
        final = compile_tex(out, scratch / 'cleaned-bibliography', stem)
        final['bibliography_postprocess'] = dict(raw_bbl_sha256=digest(raw_bbl.encode()),
            cleaned_bbl_sha256=digest(cleaned_bbl.encode()), edits=bbl_edits,
            intermediate_log=str(logpath.relative_to(ROOT)),
            reproducibility='Actual upload TeX reads the cleaned self-contained BBL; rebuilding the package regenerates it from canonical BibTeX and the unchanged official AMA BST.')
        return final
    pdf = (dest / (stem + '.pdf')).read_bytes()
    write(out / (stem + '.pdf'), pdf)
    for suffix in ('.bbl', '.aux'):
        saved = dest / (stem + suffix)
        if saved.exists():
            write(out / (stem + suffix), saved.read_bytes())
    info = subprocess.run([str(PDFINFO), str(out / (stem + '.pdf'))],
                          text=True, capture_output=True, check=True).stdout
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    unresolved = bool(re.search(r'undefined citations|undefined references|Citation .* undefined|Reference .* undefined', log, re.I))
    return dict(status='FAIL_UNRESOLVED_REFERENCES' if unresolved else 'COMPILED',
                pages=pages, sha256=digest(pdf), bytes=len(pdf), command=command,
                console=str(console.relative_to(ROOT)), log=str(logpath.relative_to(ROOT)),
                warnings=sorted(set(warnings)), visual_qa='PENDING_ROOT_PAGE_BY_PAGE_REVIEW')


def package_upload(out: Path, results: dict) -> Path:
    compiled = len(results) == 4 and all(v['status'] == 'COMPILED' for v in results.values())
    zip_path = out / ('ASMBI-source-and-pdf.zip' if compiled else 'ASMBI-source-only.zip')
    backup(zip_path)
    upload_docs = {'manuscript.tex', 'supplement.tex', 'title-page.tex', 'cover-letter.tex',
                   'references.bib', 'references-ama.bib', 'natbib.sty', 'WileyNJD-AMA.bst',
                   'manuscript.bbl', 'supplement.bbl'}
    allowed_figures = {'.pdf', '.eps', '.tif', '.tiff', '.png', '.jpg'}
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        # Explicit archive names preserve the class-requested uppercase BST
        # on case-sensitive systems, even when macOS keeps a lower-case entry.
        for name in sorted(upload_docs):
            if (out / name).exists():
                z.write(out / name, name)
        for p in sorted(out.rglob('*')):
            is_font = p.parent == out and p.suffix.lower() == '.pfb'
            is_official_otf = p.parent.name == 'MinionPro' and p.suffix.lower() == '.otf'
            is_figure = p.parent.name == 'figures' and p.suffix.lower() in allowed_figures
            is_doc_pdf = p.parent == out and p.name in {stem + '.pdf' for stem in results}
            if p.is_file() and '.bak' not in p.name and (is_font or is_official_otf or is_figure or is_doc_pdf):
                if is_doc_pdf and results[p.stem]['status'] != 'COMPILED':
                    continue
                z.write(p, p.relative_to(out).as_posix())
        for name in ('build-report.json', 'README.md', 'compatibility.json'):
            z.write(out / name, name)
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        if z.testzip() or len(names) != len(set(names)):
            raise ValueError('ZIP CRC or duplicate-member check failed')
        assert 'WileyNJD-AMA.bst' in names
        assert all(n in upload_docs for n in names if n.endswith('.tex'))
        assert all(z.read(n) == (out / n).read_bytes() for n in names)
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-compile', action='store_true', help='Regenerate sources only')
    parser.add_argument('--repack', action='store_true', help='Repack verified existing PDFs without changing them')
    args = parser.parse_args()
    canonical = ROOT / 'submission-final'
    template = ROOT / 'publisher-templates/WileyNJDv5_Template'
    out = ROOT / 'submission-package/ASMBI'
    scratch = ROOT / '.scratch/submission/asmbi'
    out.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    if args.repack:
        saved = json.loads((out / 'build-report.json').read_text())
        assert not [p for p,sha in saved['inputs_sha256'].items() if digest((ROOT / p).read_bytes()) != sha], 'Canonical inputs changed; run a complete rebuild.'
        assert all(digest((out / (stem + '.pdf')).read_bytes()) == info['sha256'] for stem,info in saved['outputs'].items() if info['status'] == 'COMPILED')
        archive_path = package_upload(out, saved['outputs'])
        print(json.dumps(dict(status='REPACKED_VERIFIED_EXISTING_PDFS', archive=str(archive_path), sha256=digest(archive_path.read_bytes()))))
        return 0
    source = expand(canonical / 'manuscript.tex')
    supplement = expand(canonical / 'supplement.tex')
    # Use the shared read-only adapter and the frozen writing definition;
    # never hard-code a word total that H4/H5 edits could invalidate.
    metrics_helper = ROOT / 'notes/submission/writing_metrics.py'
    read_input(metrics_helper)
    read_input(ROOT / 'notes/v9/writing_check.py')
    writing_stats = runpy.run_path(str(metrics_helper), run_name='asmbi_writing_metrics')['metrics']()
    narrative_words = int(writing_stats['words'])
    word_count_scope = ('Excludes the abstract, citations and references, declarations, '
                        'tables and figures (including captions), and displayed equations; '
                        'uses the frozen narrative-count definition.')
    bib = read_input(canonical / 'references.bib')
    receipt = json.loads(read_input(ROOT / 'notes/submission/template-downloads.json'))
    downloaded = next(r for r in receipt if r['filename'] == 'WileyNJDv5_Template.zip')
    archive = read_input(template.parent / 'WileyNJDv5_Template.zip')
    if digest(archive) != downloaded['sha256']:
        raise ValueError('Official template ZIP does not match download receipt')
    for p in template.iterdir():
        if p.is_file() and (p.suffix.lower() in {'.cls', '.sty'} or p.name.lower() == 'wileynjd-ama.bst' or p.name == 'rhlogo.jpg'):
            write(out / p.name, read_input(p))
    for name in ('MinionPro-Regular.otf', 'MinionPro-It.otf', 'MinionPro-Bold.otf', 'MinionPro-BoldIt.otf'):
        write(out / 'Fonts/MinionPro' / name, read_input(template / 'Fonts/MinionPro' / name))
    # This genuine pre-existing cached Type1 font is not resolved by this
    # bundled executable's PDF backend. Supplying its unchanged local bytes
    # avoids downloads or a substituted mathematical font.
    cached_font_dir = Path('/Users/bingyouli/Library/Caches/Tectonic/bundles/data/6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c')
    for cached_math_font in sorted(cached_font_dir.glob('*.pfb')):
        write(out / cached_math_font.name, read_input(cached_math_font))
    # Class uses this capitalization; alias is byte-identical official BST.
    write(out / 'WileyNJD-AMA.bst', read_input(template / 'wileyNJD-AMA.bst'))
    write(out / 'asmbi-template-compat.tex', r'''% Transparent author-side compatibility, authorized for this package.
% WileyNJDv5.cls stays byte-identical. Only its article base-class fleqn
% option is removed; cached amsmath supplies equivalent left alignment.
\PassOptionsToPackage{fleqn}{amsmath}
\let\ASMBIoriginalLoadClass\LoadClass
\def\LoadClass[#1]#2{\ASMBIoriginalLoadClass[twoside,onecolumn]{#2}}
''')
    write(out / 'references.bib', bib)
    ama_bib, bib_edits = ama_bibliography(bib, source)
    write(out / 'references-ama.bib', ama_bib)
    write(out / 'bibliography-field-audit.json', json.dumps(bib_edits, ensure_ascii=False, indent=2) + '\n')
    for p in sorted((canonical / 'figures').iterdir()):
        if p.is_file():
            write(out / 'figures' / p.name, read_input(p))
    title = re.search(r'\\begin\{center\}\\Large\\bfseries\s+(.*?)\\end\{center\}', source, re.S).group(1)
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', source, re.S).group(1)
    raw_keywords = re.search(r'\\textbf\{Keywords:\}\s*(.*?)\\par\\medskip', source, re.S).group(1)
    keyword_list = [s.strip().rstrip('.') for s in raw_keywords.split(';') if s.strip()]
    keywords = '; '.join(keyword_list[:5])
    if len(keyword_list) < 5:
        raise ValueError('Canonical has fewer than five keywords; author input needed')
    scientific_start = source.index('\\section{Introduction}')
    scientific_end = source.index('\\begin{thebibliography}')
    verified_literature = json.loads(read_input(ROOT / 'notes/submission/asmbi-recent-literature.json'))
    narrative_authors, narrative_author_audit = verified_narrative_authors(bib, verified_literature)
    main_citation_edits: list[dict] = []
    supplement_citation_edits: list[dict] = []
    body = numeric_citations(source[scientific_start:scientific_end],
                             narrative_authors, main_citation_edits)
    retained, tables = split_tables(body)
    keys = re.findall(r'@[A-Za-z]+\s*\{\s*([^,\s]+)', bib.decode('utf-8'))
    cited = [k.strip() for command in re.findall(r'\\cite\w*(?:\[[^]]*\])*\{([^}]+)\}', body) for k in command.split(',')]
    missing = sorted(set(cited) - set(keys))
    if missing:
        raise ValueError(f'Canonical references.bib lacks cited keys: {missing}')
    macros = '\n'.join(line for line in source.split('\\begin{document}')[0].splitlines()
                       if line.startswith(('\\newcommand', '\\newcounter')))
    main_tex = standard_preamble() + macros + '\n\\begin{document}\n'
    main_tex += metadata(title, abstract, keywords) + '\\maketitle\n\n' + retained
    main_tex += '\n\\FloatBarrier\n\\bibliography{references}\n\\clearpage\n'
    table_receipt = []
    for i, table in enumerate(tables, 1):
        moved = re.sub(r'\\begin\{table\}(?:\[[^]]*\])?', r'\\begin{table}[p]', table, count=1)
        main_tex += '\n% Original-order table, separate page.\n\\clearpage\n' + moved + '\n\\clearpage\n'
        labels = re.findall(r'\\label\{([^}]+)\}', table)
        table_receipt.append(dict(order=i, labels=labels, content_sha256=digest(table.encode())))
    main_tex += '\\end{document}\n'
    audit = scratch / 'njd-original-attempt'
    write(audit / 'WileyNJDv5.cls', read_input(template / 'WileyNJDv5.cls'))
    write(audit / 'WileyNJD-AMA.bst', read_input(template / 'wileyNJD-AMA.bst'))
    original_failure = scratch / 'manuscript/manuscript.log'
    if original_failure.exists():
        write(audit / 'original-first-failure.log', original_failure.read_bytes())
    write(audit / 'manuscript-njd.tex', main_tex)
    original_njd = main_tex.replace('\\input{asmbi-template-compat.tex}\n', '', 1).replace('\\let\\LoadClass\\ASMBIoriginalLoadClass\n', '', 1)
    write(audit / 'manuscript-njd-original.tex', original_njd)
    write(out / 'manuscript.tex', main_tex)
    write(out / 'main.tex', '% Default compile target.\n\\input{manuscript.tex}\n')
    supp_body = supplement.split('\\begin{document}', 1)[1].rsplit('\\end{document}', 1)[0]
    supp_body = supp_body.replace('\\maketitle', '', 1)
    supp_preamble = supplement.split('\\begin{document}', 1)[0]
    # Retain the canonical section/paragraph definitions, numbering and lengths.
    custom_start = supp_preamble.index('\\setlength{\\parindent}')
    custom_end = supp_preamble.index('\\title{')
    custom = supp_preamble[custom_start:custom_end]
    supp_title = 'Online Supplement to ' + title
    supp_tex = standard_preamble() + custom + '\n\\begin{document}\n'
    supp_tex += metadata(supp_title) + '\\maketitle\n' + numeric_citations(
        supp_body, narrative_authors, supplement_citation_edits)
    supp_tex += '\n\\FloatBarrier\n% Self-contained bibliography for supporting methods.\n\\nocite{*}\n\\bibliography{references}\n\\end{document}\n'
    write(audit / 'supplement-njd.tex', supp_tex)
    write(audit / 'supplement-njd-original.tex', supp_tex.replace('\\input{asmbi-template-compat.tex}\n', '', 1).replace('\\let\\LoadClass\\ASMBIoriginalLoadClass\n', '', 1))
    write(out / 'supplement.tex', supp_tex)
    repository = re.search(r'\\href\{(https://github\.com/[^}]+)\}\{versioned GitHub repository\}', body).group(1)
    title_tex = free_format_preamble() + '\n\\begin{document}\n\\pagestyle{empty}\n'
    title_tex += '\\section*{' + title + '}\n'
    for label in ('Authors', 'Affiliations', 'Corresponding author and contact', 'ORCID', 'Funding', 'Competing interests', 'CRediT contributions'):
        title_tex += '\\noindent\\textbf{' + label + ':} [TO BE COMPLETED BY AUTHOR].\\par\\medskip\n'
    title_tex += '\\noindent\\textbf{Running title:} Historical Rules and Peak Limits.\\par\\medskip\n'
    title_tex += '\\noindent\\textbf{Main-text narrative word count:} ' + f'{narrative_words:,}' + '.\\par\n'
    title_tex += word_count_scope + '\\par\\medskip\n'
    title_tex += '\\noindent\\textbf{Keywords:} ' + keywords + '.\\par\\medskip\n'
    title_tex += '\\noindent\\textbf{Data and code:} Source rights, excluded raw inputs and reproduction information are stated in the manuscript and the \\href{' + repository + '}{versioned repository}.\\par\\medskip\n'
    title_tex += '\\noindent\\textbf{Data permissions and license compliance:} [TO BE VERIFIED BY AUTHOR].\n\\end{document}\n'
    write(out / 'title-page.tex', title_tex)
    canonical_cover = read_input(canonical / 'cover-letter.tex').decode('utf-8')
    cover_body = canonical_cover.split('\\begin{document}', 1)[1].rsplit('\\end{document}', 1)[0]
    if '\\textbf{' + title + '}' not in cover_body:
        raise ValueError('Canonical cover title does not match manuscript title')
    # Keep the current H6 policy/public-version disclosure verbatim; only the
    # Free Format font/layout preamble belongs to the ASMBI derivative.
    cover = free_format_preamble() + '\n\\begin{document}' + cover_body + '\\end{document}\n'
    write(out / 'cover-letter.tex', cover)
    if re.search(r'\b(?:AI|LLM|ChatGPT)\b', '\n'.join((main_tex, supp_tex, title_tex, cover))):
        raise ValueError('Unexpected prohibited disclosure/placeholder in package text')
    figure_widths = re.findall(r'\\includegraphics\[([^]]+)\]\{(figures/[^}]+)\}', body)
    preserved = all(('\\includegraphics[' + opts + ']{' + path + '}') in main_tex for opts, path in figure_widths)
    if not preserved:
        raise AssertionError('A canonical main-figure width changed')
    results = {}
    njd_probe = None
    format_mode = 'OFFICIAL_NJD_AUTHOR_COMPATIBILITY_SOURCE'
    if not args.no_compile:
        # The previous NJD attempt is explicitly excluded from upload ZIPs.
        # Keep a probe copy beside its official resources only for this check.
        write(out / 'manuscript-njd.tex', main_tex)
        njd_probe = compile_tex(out, scratch, 'manuscript-njd')
        if njd_probe['status'] != 'COMPILED':
            format_mode = 'ASMBI_OFFICIAL_FREE_FORMAT_INITIAL_SUBMISSION'
            njd_header = standard_preamble() + macros + '\n\\begin{document}\n' + metadata(title, abstract, keywords) + '\\maketitle\n\n'
            free_header = free_format_preamble() + macros + '\n\\title{' + title + '}\n\\author{[AUTHOR INFORMATION TO BE COMPLETED]}\n\\date{}\n\\begin{document}\n\\maketitle\n\\begin{abstract}' + abstract + '\\end{abstract}\n\\noindent\\textbf{Keywords:} ' + keywords + '.\\par\\medskip\n'
            assert main_tex.startswith(njd_header)
            main_tex = main_tex.replace(njd_header, free_header, 1)
            main_tex = main_tex.replace('\\bibliography{references}', '\\bibliography{references-ama}')
            njd_supp_header = standard_preamble() + custom + '\n\\begin{document}\n' + metadata(supp_title) + '\\maketitle\n'
            free_supp_header = free_format_preamble() + custom + '\n\\title{' + supp_title + '}\n\\author{}\n\\date{}\n\\begin{document}\n\\maketitle\n'
            assert supp_tex.startswith(njd_supp_header)
            supp_tex = supp_tex.replace(njd_supp_header, free_supp_header, 1)
            supp_tex = supp_tex.replace('\\bibliography{references}', '\\bibliography{references-ama}')
            write(out / 'manuscript.tex', main_tex)
            write(out / 'supplement.tex', supp_tex)
        for stem in ('manuscript', 'supplement', 'title-page', 'cover-letter'):
            results[stem] = compile_tex(out, scratch, stem)
    changed_inputs = [p for p, sha in INPUTS.items() if digest((ROOT / p).read_bytes()) != sha]
    warnings = [
        'All final PDF pages require root visual QA; this script certifies source closure and compilation only.',
        'Author, affiliation, contact, ORCID, funding, competing interests, CRediT and permissions remain author-verification placeholders.',
        'Figures retain canonical PDF previews and widths. Independent EPS/high-DPI exports and >=7pt label preflight are pending root.',
        'Supplement long tables retain native S-section positions; main-article tables alone are moved after references.',
    ]
    if format_mode == 'ASMBI_OFFICIAL_FREE_FORMAT_INITIAL_SUBMISSION':
        warnings.append('Actual PDFs use the journal-permitted Free Format initial-submission route with official Wiley AMA BST. NJDv5 original/compatible sources are retained; NJDv5 PDF did not compile because required packages are not cached.')
    if changed_inputs:
        warnings.append('Canonical inputs changed during build; re-run before using outputs: ' + ', '.join(changed_inputs))
    if (results.get('cover-letter', {}).get('pages') or 0) > 1:
        warnings.append('FAIL: Cover letter exceeds one page.')
    if (results.get('title-page', {}).get('pages') or 0) > 1:
        warnings.append('FAIL: Title page exceeds one page.')
    source_only = args.no_compile
    compiled = len(results) == 4 and all(v['status'] == 'COMPILED' for v in results.values())
    status = 'SOURCES_ONLY' if source_only else ('COMPILED_PENDING_VISUAL_QA' if compiled and not changed_inputs and results['cover-letter']['pages'] <= 1 and results['title-page']['pages'] <= 1 else 'NEEDS_REPAIR')
    report = dict(status=status, build_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  actual_pdf_format=format_mode, njd_compatibility_probe=njd_probe,
                  ama_bibliography_field_normalization=bib_edits,
                  command='python3 notes/submission/build_asmbi_package.py',
                  official_template_zip_sha256=downloaded['sha256'],
                  official_class_sha256=INPUTS[str((template / 'WileyNJDv5.cls').relative_to(ROOT))],
                  inputs_sha256=INPUTS, canonical_changed_during_build=changed_inputs,
                  transformations=dict(scientific_prose_reassembled_exactly=True, title_preserved=True,
                      abstract_preserved=True, citation_format='AMA sequential superscript via official BST; verified narrative authors emitted explicitly',
                      narrative_author_metadata=narrative_author_audit,
                      narrative_citation_edits=dict(main=main_citation_edits, supplement=supplement_citation_edits),
                      narrative_citation_non_citation_text_preserved=True,
                      cover_body_preserved_from_canonical=True,
                      keyword_count=5, keywords=keyword_list[:5], omitted_keyword_metadata=keyword_list[5:],
                      title_page_narrative_word_count=narrative_words,
                      title_page_word_count_scope=word_count_scope,
                      writing_metrics_helper='notes/submission/writing_metrics.py:metrics()["words"]',
                      body_font_pt=12, main_tables_after_references=table_receipt,
                      main_table_count=len(tables), main_figure_widths_preserved=preserved,
                      main_figure_width_options=[dict(options=o, path=p) for o,p in figure_widths],
                      supporting_body_content_preserved=True, supporting_reference_policy='All canonical bib entries appended for a self-contained supplement'),
                  outputs=results, backups=BACKUPS, warnings=warnings)
    compatibility = dict(actual_pdf_format=format_mode,
        official_free_format_policy='https://onlinelibrary.wiley.com/page/journal/15264025/homepage/forauthors.html',
        official_template_zip_sha256=downloaded['sha256'],
        official_class_sha256=report['official_class_sha256'],
        official_bst_sha256=digest((out / 'WileyNJD-AMA.bst').read_bytes()),
        original_failure_log='.scratch/submission/asmbi/njd-original-attempt/original-first-failure.log',
        actual_original_error='fleqn.clo not found',
        minimal_compatibility='Only remove article base-class fleqn option; request left alignment from cached amsmath.',
        compatibility_probe=njd_probe,
        actually_observed_next_missing_dependency='etex.sty' if njd_probe and njd_probe['status'] != 'COMPILED' else None,
        static_missing_package_scan_is_not_runtime_proof=True,
        font_policy='Four unchanged MinionPro fonts from official template; unchanged genuine Type1 fonts already in the local cache supplied explicitly for the PDF backend. No downloads.',
        bibliography_policy='Canonical references.bib is byte-identical. Derived AMA fields map existing institutions, retain existing URLs in notes, protect the existing van den Hoogen surname, and restore missing n.d. only from the canonical manual bibliography. Each original field is checked. Generated BBL cleanup only removes empty-field/editor punctuation, with identical word/number tokens; upload TeX reads this self-contained BBL. Official BST unchanged.',
        upload_zip_excludes_uncompiled_njd_sources=True,
        author_decision_pending='Use the permitted Free Format initial submission, or arrange a complete offline NJDv5 environment for original-template typesetting; original NJDv5 compilation is not claimed.')
    write(out / 'compatibility.json', json.dumps(compatibility, ensure_ascii=False, indent=2) + '\n')
    write(out / 'build-report.json', json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    readme = '# ASMBI submission package\n\nStatus: ' + status + '\n\n'
    readme += 'Rebuild from current canonical sources with `python3 notes/submission/build_asmbi_package.py`.\n'
    readme += 'Actual PDF route: ' + format_mode + '.\n\n'
    readme += 'The official Wiley NJDv5 class and bibliography style files are unmodified; `WileyNJD-AMA.bst` is a case-portable byte-identical alias. Uncompiled original/compatible NJD sources and failure logs are audit records in `.scratch/submission/asmbi/`; they are excluded from the actual upload ZIP. NJDv5 could not compile with offline dependencies, so actual PDFs must not be described as unmodified NJD typesetting.\n\n'
    readme += 'Standalone compile targets: `manuscript.tex`, `supplement.tex`, `title-page.tex`, `cover-letter.tex`; use `tectonic -X compile -C <target>` in this directory.\n\n'
    readme += '\n'.join('- ' + w for w in warnings) + '\n\n'
    readme += '\n'.join(f'- {stem}.pdf: {info.get("pages")} pages; {info["status"]}' for stem, info in results.items()) + '\n'
    write(out / 'README.md', readme)
    if not changed_inputs:
        package_upload(out, results)
    compact_outputs = {stem: {k:v for k,v in info.items() if k not in {'warnings', 'bibliography_postprocess'}} | {'warning_count': len(info.get('warnings', []))} for stem,info in results.items()}
    print(json.dumps(dict(status=status, main_tables=len(tables), outputs=compact_outputs,
                          input_count=len(INPUTS), changed_inputs=changed_inputs,
                          report=str(out / 'build-report.json')), ensure_ascii=False, indent=2))
    return 0 if source_only or status == 'COMPILED_PENDING_VISUAL_QA' else 1


if __name__ == '__main__':
    sys.exit(main())
