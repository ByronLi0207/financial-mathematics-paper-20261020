#!/usr/bin/env python3
"""Build a source-bound QF alternative without editing the canonical manuscript.

Run with the existing uv environment, e.g.:
uv run --offline --no-project --no-env-file --python <existing-python> \
  --with pypdf python -B notes/submission/build_qf_package.py
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import zipfile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
CITE = re.compile(r"(\\cite(?:p|t|alp|alt|author|year|yearpar)?\*?(?:\[[^\]]*\]){0,2})\{([^}]+)\}")
LOCAL = re.compile(r"\\(input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}")
TECTONIC = Path('/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic')
# Only these exact three paragraph labels omit their source full stop: the
# publisher class supplies its own paragraph-heading stop. No other body
# punctuation or paragraph-heading normalization is permitted.
ALLOWED_BODY_LABEL_PUNCTUATION = (
    (r'\paragraph{Data availability.}', r'\paragraph{Data availability}'),
    (r'\paragraph{Code availability.}', r'\paragraph{Code availability}'),
    (r'\paragraph{A fixed CFTC history-length extension.}',
     r'\paragraph{A fixed CFTC history-length extension}'),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def strip_comments(text: str) -> str:
    return re.sub(r'(?m)(?<!\\)%.*$', '', text)


def bib_entries(text: str) -> dict[str, str]:
    """Brace-aware entry slicing; do not rewrite inherited bibliographic fields."""
    entries = {}
    for m in re.finditer(r'@\w+\s*\{\s*([^,]+),', text):
        level, pos = 1, m.end()
        while level and pos < len(text):
            if text[pos] == '{' and text[pos - 1] != '\\':
                level += 1
            elif text[pos] == '}' and text[pos - 1] != '\\':
                level -= 1
            pos += 1
        if level:
            raise ValueError(f'Unclosed BibTeX entry: {m.group(1)}')
        if m.group(1).strip() in entries:
            raise ValueError(f'Duplicate BibTeX entry: {m.group(1)}')
        entries[m.group(1).strip()] = text[m.start():pos]
    return entries


def cited_keys(text: str) -> set[str]:
    return {key.strip() for m in CITE.finditer(strip_comments(text))
            for key in m.group(2).split(',')}


def bib_field(entry: str, name: str):
    m = re.search(r'\b' + re.escape(name) + r'\s*=\s*\{', entry, re.I)
    if not m:
        return None
    level, pos = 1, m.end()
    while level and pos < len(entry):
        if entry[pos] == '{' and entry[pos - 1] != '\\':
            level += 1
        elif entry[pos] == '}' and entry[pos - 1] != '\\':
            level -= 1
        pos += 1
    if level:
        raise ValueError(f'Unclosed BibTeX field {name}')
    return entry[m.end():pos - 1], m.end(), pos - 1


def normalize_citations(text: str) -> str:
    return CITE.sub(lambda m: m.group(1) + '{' + ','.join(sorted(
        key.strip() for key in m.group(2).split(','))) + '}', text)


def normalize_explicit_packaging_only(text: str) -> str:
    """Citation ordering plus the three named label stops, never general prose."""
    for source, derived in ALLOWED_BODY_LABEL_PUNCTUATION:
        text = text.replace(source, derived)
    return normalize_citations(text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical', type=Path, default=ROOT / 'submission-final')
    args = parser.parse_args()
    canonical = args.canonical.resolve()
    if not canonical.is_dir():
        raise FileNotFoundError(canonical)
    if canonical != (ROOT / 'submission-final').resolve():
        raise ValueError('The frozen shared word metric is bound to submission-final/')
    out = ROOT / 'submission-package/QF'
    templates = ROOT / 'publisher-templates/rqufLatex'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    logs = ROOT / '.scratch/submission/qf' / stamp
    logs.mkdir(parents=True, exist_ok=False)
    out.mkdir(parents=True, exist_ok=True)
    protected = {p.relative_to(canonical).as_posix(): sha(p.read_bytes())
                 for p in canonical.rglob('*') if p.is_file()}
    backups = []

    # Preserve the visually rejected cut before replacing any generated output.
    # Its PDF and source ZIP remain available even if later builds are tracked.
    failed_cut = None
    previous_manuscript = out / 'manuscript.tex'
    if ((out / 'main.pdf').is_file() and previous_manuscript.is_file()
            and 'hoffset=0pt,voffset=0pt' not in previous_manuscript.read_text()):
        legacy_footer = 'QF-GEOMETRY-AFTER' not in previous_manuscript.read_text()
        evidence = out / 'failed-cuts' / stamp
        evidence.mkdir(parents=True, exist_ok=False)
        preserved = {}
        for name in ('main.pdf', 'main.tex', 'manuscript.tex', 'qf-compat.tex',
                     'source-package.zip', 'BUILD-RECEIPT.json'):
            source = out / name
            if source.is_file():
                raw = source.read_bytes()
                (evidence / name).write_bytes(raw)
                preserved[name] = {'sha256': sha(raw), 'bytes': len(raw)}
        failed_cut = {
            'status': ('FAIL_VISUAL_PAGE_FOOTER_COLLISION_SUPERSEDED' if legacy_footer
                       else 'FAIL_VISUAL_INHERITED_PAGE_OFFSETS_SUPERSEDED'),
            'recorded_utc': now(),
            'reported_by': 'Root direct visual inspection and full-page QA',
            'collision_page': 3 if legacy_footer else None,
            'insufficient_footer_clearance_pages': ([2, 4, 5, 7, 9, 10, 12, 13, 18, 19]
                                                   if legacy_footer else []),
            'cause': ('The unchanged 2014 class sets footskip=4pt and textheight=676pt; these lengths are unsuitable with the restored modern kernel outputpage.'
                      if legacy_footer else 'The first geometry trial retained the class hoffset=-1in and voffset=-54pt, which displaced content beyond the left page edge; direct page-2 rendering rejected it.'),
            'preserved_files': preserved,
            'evidence_directory': str(evidence.relative_to(ROOT)),
            'previous_receipt_claim_is_superseded': True,
        }
        (evidence / 'FAILED-CUT-RECEIPT.json').write_text(
            json.dumps(failed_cut, indent=2) + '\n')

    def put(relative: str, data: str | bytes) -> None:
        p = out / relative
        p.resolve().relative_to(out.resolve())
        raw = data.encode() if isinstance(data, str) else data
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            if p.read_bytes() == raw:
                return
            tracked = subprocess.run(['git', 'ls-files', '--error-unmatch',
                p.relative_to(ROOT).as_posix()], cwd=ROOT, capture_output=True).returncode == 0
            if not tracked or p.suffix.lower() == '.pdf' or p.name == 'BUILD-RECEIPT.json':
                backup = p.with_name(p.name + '.bak.' + stamp)
                if backup.exists():
                    raise FileExistsError(backup)
                backup.write_bytes(p.read_bytes())
                backups.append(backup.relative_to(ROOT).as_posix())
        p.write_bytes(raw)

    original = (canonical / 'manuscript.tex').read_text()
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', original, re.S)
    title_match = re.search(r'\\begin\{center\}\\Large\\bfseries (.*?)\\end\{center\}', original, re.S)
    keywords_match = re.search(r'\\textbf\{Keywords:\}\s*(.*?)\\par\\medskip', original, re.S)
    if not all((abstract_match, title_match, keywords_match)):
        raise ValueError('Canonical front matter changed: inspect title/abstract/keyword parser')
    title = title_match.group(1).strip()
    abstract = abstract_match.group(1).strip()
    keywords = keywords_match.group(1).strip().rstrip('.')
    keywords_list = [k.strip() for k in keywords.split(';')]
    metric_reader = ROOT / 'notes/submission/writing_metrics.py'
    metric_source = ROOT / 'notes/v9/writing_check.py'
    writing = runpy.run_path(str(metric_reader),
                            run_name='qf_shared_frozen_metric_reader')['metrics']()
    narrative_words = writing['words']
    if not isinstance(narrative_words, int) or narrative_words <= 0:
        raise ValueError('The frozen canonical narrative count must be a positive integer')
    word_count_scope = ('Excludes abstract, citations, declarations, tables and figures, '
                        'their captions, and displayed equations; uses the frozen '
                        'canonical narrative-count definition.')
    abstract_plain = re.sub(r'\\[a-zA-Z]+(?:\[[^]]*\])?', ' ', abstract).replace('\\%', '%')
    abstract_words = len(abstract_plain.split())
    if abstract_words > 200 or not 4 <= len(keywords_list) <= 6:
        raise ValueError(f'QF front-matter limits: {abstract_words} words / {len(keywords_list)} keywords')

    bibliography_start = original.index('\\begin{thebibliography}')
    bibliography_end = original.index('\\end{thebibliography}') + len('\\end{thebibliography}')
    body_start = original.index('\\section{Introduction}')
    body = original[body_start:bibliography_start]
    database = (canonical / 'references.bib').read_text()
    entries = bib_entries(database)
    bibliography_mappings = []
    for key, entry in list(entries.items()):
        changed = entry
        kind = re.match(r'@(\w+)', entry).group(1).lower()
        institution = bib_field(entry, 'institution')
        additions = {}
        if kind in ('mastersthesis', 'phdthesis') and institution and not bib_field(entry, 'school'):
            additions['school'] = institution[0]
        if kind == 'misc' and institution and not bib_field(entry, 'howpublished'):
            additions['howpublished'] = institution[0]
        url = bib_field(entry, 'url')
        doi = bib_field(entry, 'doi')
        source_url = url[0] if url else ('https://doi.org/' + doi[0] if doi else None)
        if source_url:
            source_url = source_url.replace('\\_', '_')
            note = bib_field(entry, 'note')
            if not note or source_url not in note[0]:
                value = ((note[0].rstrip().rstrip('.') + '. ') if note else '') + '\\url{' + source_url + '}'
                if note:
                    changed = changed[:note[1]] + value + changed[note[2]:]
                    bibliography_mappings.append({'key': key, 'field': 'note', 'source': 'Existing note plus existing URL/DOI'})
                else:
                    additions['note'] = value
        for field, value in additions.items():
            changed = changed[:-1].rstrip().rstrip(',') + ',\n  ' + field + ' = {' + value + '}\n}'
            bibliography_mappings.append({'key': key, 'field': field,
                'source': 'Existing institution' if field in ('school', 'howpublished') else 'Existing URL/DOI'})
        if key == 'wisniewski2020' and kind == 'inproceedings':
            booktitle = bib_field(changed, 'booktitle')
            prefix = 'Proceedings of the '
            if booktitle and booktitle[0].startswith(prefix):
                replacement = booktitle[0][len(prefix):]
                changed = changed[:booktitle[1]] + replacement + changed[booktitle[2]:]
                bibliography_mappings.append({'key': key, 'field': 'booktitle',
                    'before': booktitle[0], 'after': replacement,
                    'source': 'Remove only the existing literal prefix because unchanged official rQUF.bst format.inproc.booktitle supplies Proceedings of the automatically.'})
        database = database.replace(entry, changed)
    entries = bib_entries(database)
    date_additions = []
    for key, entry in list(entries.items()):
        if re.search(r'\byear\s*=', entry, re.I):
            continue
        # Preserve an explicit no-date label already printed in the canonical manuscript.
        manual = re.search(r'\\bibitem\[([^\n]+)\]\{' + re.escape(key) + r'\}',
                           original[bibliography_start:bibliography_end])
        if manual and '(n.d.)' in manual.group(1):
            replaced = entry[:-1].rstrip() + ',\n  year = {n.d.}\n}'
            database = database.replace(entry, replaced)
            date_additions.append({'key': key, 'year': 'n.d.',
                                   'source': 'Canonical hand-written bibliography label'})
    entries = bib_entries(database)

    def year(key: str) -> int:
        m = re.search(r'\byear\s*=\s*[{"]\s*(\d{4})', entries[key], re.I)
        return int(m.group(1)) if m else 9999

    reorderings = []

    def chronological(m: re.Match) -> str:
        keys = [k.strip() for k in m.group(2).split(',')]
        missing = set(keys) - entries.keys()
        if missing:
            raise ValueError(f'Citation missing from canonical references.bib: {missing}')
        ordered = sorted(keys, key=year)  # stable same-year order
        if ordered != keys:
            reorderings.append({'before': keys, 'after': ordered})
        return m.group(1) + '{' + ','.join(ordered) + '}'

    qf_body = CITE.sub(chronological, body)
    label_punctuation_changes = []
    for source, derived in ALLOWED_BODY_LABEL_PUNCTUATION:
        count = qf_body.count(source)
        if count > 1:
            raise ValueError(f'Unexpected duplicate exact paragraph label: {source}')
        if count:
            qf_body = qf_body.replace(source, derived, 1)
            label_punctuation_changes.append({'before': source, 'after': derived,
                'occurrences': count,
                'reason': 'The unchanged QF class appends the paragraph-heading full stop.'})
    if normalize_explicit_packaging_only(qf_body) != normalize_explicit_packaging_only(body):
        raise ValueError('Unexpected scientific body change')
    bib_commands = '\\bibliographystyle{rQUF}\n\\bibliography{references}\n'
    # Use the publisher class unchanged; replace its fictitious publication header only.
    preamble = r'''% QF alternative: generated from the current canonical submission-final sources.
\input{qf-compat.tex}
\documentclass{rQUF2e}
\QFRestoreKernelDocument
\input{qf-fonts.tex}
% Class declares letterpaper but predates kernel stock-size initialization.
\setlength{\paperwidth}{8.5in}\setlength{\paperheight}{11in}
% The class's 4pt footer gap collides with the restored modern output routine.
% Keep publisher typography, and explicitly fit body/header/footer to letter stock.
\typeout{QF-GEOMETRY-BEFORE textwidth=\the\textwidth; textheight=\the\textheight; footskip=\the\footskip; headheight=\the\headheight; headsep=\the\headsep; hoffset=\the\hoffset; voffset=\the\voffset; topmargin=\the\topmargin; QF-GEOMETRY-END}
\usepackage[letterpaper,hoffset=0pt,voffset=0pt,left=22mm,right=22mm,top=24mm,bottom=24mm,includeheadfoot,headheight=14pt,headsep=15pt,footskip=20pt]{geometry}
\AtBeginDocument{\typeout{QF-GEOMETRY-AFTER textwidth=\the\textwidth; textheight=\the\textheight; footskip=\the\footskip; headheight=\the\headheight; headsep=\the\headsep; hoffset=\the\hoffset; voffset=\the\voffset; topmargin=\the\topmargin; paperwidth=\the\paperwidth; paperheight=\the\paperheight; QF-GEOMETRY-END}}
% Select the required bold face before its large size; avoid loading an
% unused large regular face not present in the cache.
\renewcommand{\titlefont}{\normalfont\bfseries\fontsize{18}{22}\selectfont\centering}
\usepackage{booktabs,array,placeins}
\usepackage[unicode,breaklinks=true,hidelinks]{hyperref}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{3pt}
\clubpenalty=10000\widowpenalty=10000
\newcounter{proposition}
\newcommand{\vthirteenMCSTable}{S7}
\bibpunct{(}{)}{,}{a}{}{,}
\makeatletter
\def\ps@qfsubmission{%
  \def\@oddhead{\hfil\small Quantitative Finance submission draft\hfil}%
  \let\@evenhead\@oddhead
  \def\@oddfoot{\hfil\thepage\hfil}\let\@evenfoot\@oddfoot}
\let\ps@plain\ps@qfsubmission
\makeatother
\pagestyle{qfsubmission}
\begin{document}
'''
    front = ('\\title{' + title + '}\n'
        '\\author{[AUTHOR NAMES TO BE COMPLETED]\\\\\n'
        '\\affil{[AFFILIATIONS TO BE COMPLETED]}}\n'
        '\\received{Submission draft; author details pending}\n\\maketitle\n\n'
        '\\begin{abstract}' + abstract + '\\end{abstract}\n\n'
        '\\begin{keywords}' + keywords + '\\end{keywords}\n'
        '\\begin{classcode}[TO BE COMPLETED BY AUTHOR]\\end{classcode}\n\n')
    manuscript = preamble + front + qf_body + bib_commands + '\\end{document}\n'
    put('main.tex', '% Main QF manuscript target.\n\\input{manuscript.tex}\n')
    put('manuscript.tex', manuscript)
    put('references.bib', database)
    def add_fonts(text: str) -> str:
        return text.replace('\\begin{document}', '\\input{qf-fonts.tex}\n\\begin{document}', 1)
    put('supplement.tex', add_fonts((canonical / 'supplement.tex').read_text()))
    title_page = (canonical / 'title-page.tex').read_text()
    count_metadata = ('\\textbf{Narrative word count:} ' + str(narrative_words)
                      + '.\\par\n{\\small ' + word_count_scope + '}\\par\\medskip\n'
                      '\\textbf{Keywords:} ' + keywords + '.\\par\\medskip\n')
    marker = 'Authors:'
    if marker not in title_page:
        raise ValueError('Canonical title-page author marker changed; inspect the metadata placement')
    title_page = title_page.replace(marker, count_metadata + marker, 1)
    if 'CRediT' not in title_page:
        title_page = title_page.replace('\\end{document}',
            'CRediT author contributions: [TO BE COMPLETED BY AUTHOR].\\par\\medskip\n'
            '\\end{document}', 1)
    if 'JEL classification:' not in title_page:
        title_page = title_page.replace('\\end{document}',
            'JEL classification: [TO BE COMPLETED BY AUTHOR].\\par\\medskip\n'
            '\\end{document}', 1)
    put('title-page.tex', add_fonts(title_page))
    for name in ('rQUF2e.cls', 'rQUF.bst', 'epsfig.sty', 'rotating.sty'):
        put(name, (templates / name).read_bytes())
    put('qf-compat.tex', r'''% Author-side cache compatibility; the publisher class is unchanged.
% The class loads enumerate.sty, which is neither in its distributed ZIP nor
% in this machine's Tectonic cache. No extended enumerate syntax is used.
% Standard LaTeX list environments remain available; reject extended syntax
% in the Python builder rather than silently approximating it.
% The 2014 class also replaces kernel document/enddocument with pre-2020
% implementations. Preserve the installed kernel entry points while retaining
% all publisher typography, headings, citations and layout definitions.
\let\QFKernelDocument\document
\let\QFKernelEndDocument\enddocument
\makeatletter
\let\QFKernelOutputPage\@outputpage
\newcommand{\QFRestoreKernelDocument}{%
  \let\document\QFKernelDocument\let\enddocument\QFKernelEndDocument
  \let\@outputpage\QFKernelOutputPage}
\@namedef{ver@enumerate.sty}{2026/10/27 unused optional interface skipped}
\makeatother
''')
    put('qf-fonts.tex', r'''% Cached Latin Modern OpenType faces; no font download or system install.
% Scalable Computer Modern-derived faces avoid absent optical-size TFM files.
\usepackage[TU]{fontenc}
\DeclareFontFamily{TU}{qflmr}{}
\DeclareFontShape{TU}{qflmr}{m}{n}{<->\UnicodeFontFile{lmroman10-regular}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{qflmr}{m}{it}{<->\UnicodeFontFile{lmroman10-italic}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{qflmr}{m}{sl}{<->ssub*qflmr/m/it}{}
\DeclareFontShape{TU}{qflmr}{m}{sc}{<->ssub*qflmr/m/n}{}
\DeclareFontShape{TU}{qflmr}{bx}{n}{<->\UnicodeFontFile{lmroman10-bold}{\UnicodeFontTeXLigatures}}{}
\DeclareFontShape{TU}{qflmr}{bx}{it}{<->\UnicodeFontFile{lmroman10-italic}{\UnicodeFontTeXLigatures embolden=1.8;}}{}
\DeclareFontShape{TU}{qflmr}{b}{n}{<->ssub*qflmr/bx/n}{}
\DeclareFontShape{TU}{qflmr}{b}{it}{<->ssub*qflmr/bx/it}{}
\DeclareFontFamily{TU}{qflmtt}{}
\DeclareFontShape{TU}{qflmtt}{m}{n}{<->\UnicodeFontFile{lmmono10-regular}{}}{}
\DeclareFontShape{TU}{qflmtt}{m}{it}{<->ssub*qflmtt/m/n}{}
\DeclareFontShape{TU}{qflmtt}{bx}{n}{<->ssub*qflmtt/m/n}{}
\renewcommand{\rmdefault}{qflmr}\renewcommand{\ttdefault}{qflmtt}
\normalfont
''')

    # Copy only transitive local TeX/PDF dependencies. No new scientific figure is made.
    copied = set()
    def copy_dependencies(text: str) -> None:
        for m in LOCAL.finditer(strip_comments(text)):
            command, rel = m.groups()
            path = Path(rel)
            if command in ('input', 'include') and not path.suffix:
                path = path.with_suffix('.tex')
            if command == 'includegraphics' and not path.suffix:
                path = path.with_suffix('.pdf')
            key = path.as_posix()
            if key in copied:
                continue
            source = (canonical / path).resolve()
            source.relative_to(canonical)
            if not source.is_file():
                raise FileNotFoundError(source)
            if command == 'includegraphics' and source.suffix.lower() != '.pdf':
                raise ValueError(f'Expected an existing PDF figure, got {source}')
            copied.add(key)
            put(key, source.read_bytes())
            if source.suffix == '.tex':
                copy_dependencies(source.read_text())
    copy_dependencies(qf_body)
    copy_dependencies((canonical / 'supplement.tex').read_text())

    cover = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=25mm]{geometry}
\usepackage[unicode,hidelinks,breaklinks=true]{hyperref}
\input{qf-fonts.tex}
\setlength{\parindent}{0pt}\setlength{\parskip}{10pt}\pagestyle{empty}
\begin{document}
\textbf{Submission to Quantitative Finance:} ''' + title + r'''

Dear Editors,

Matched foreign exchange (FX) gains depend on the reference; longer validation narrows weekly regression losses, but the historical default rule leaves adverse cases; illustrative costs depend on reserve and breach charges.

The manuscript offers matched empirical forecast comparisons for peak inventory limits and separates average accuracy, breaches and illustrative cost preferences. This fits the journal's scope of ``both theoretical and empirical approaches'' and its coverage of financial econometrics, liquidity modelling, market prediction and operational risk. The scope is stated on the journal's \href{https://www.tandfonline.com/journals/rquf20/about-this-journal}{official journal page}.

The publisher permits preprints under its \href{https://authorservices.taylorandfrancis.com/publishing-your-research/making-your-submission/posting-to-a-preprint-server/}{preprint policy}. We disclose the study's GitHub working versions, revision branches and PRs in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/notes/submission/public-versions.md}{public-version inventory}, alongside code and aggregate results. The evidence is retrospective and restricted raw inputs are excluded; source-specific acquisition and reproduction requirements are documented. [AUTHOR TO CONFIRM OTHER VERSIONS, ALL-AUTHOR APPROVAL, EXCLUSIVE SUBMISSION AND DATA-SHARING PERMISSIONS].

Sincerely,\par [TO BE COMPLETED BY AUTHOR]
\end{document}
'''
    put('cover-letter.tex', cover)

    source_names = {'main.tex', 'manuscript.tex', 'references.bib', 'supplement.tex',
                    'title-page.tex', 'cover-letter.tex', 'rQUF2e.cls', 'rQUF.bst',
                    'epsfig.sty', 'rotating.sty', 'qf-compat.tex', 'qf-fonts.tex'} | copied
    recursive_text = manuscript + '\n' + '\n'.join((out / n).read_text()
                         for n in sorted(copied) if n.endswith('.tex'))
    cites = cited_keys(recursive_text)
    if re.search(r'\\begin\{enumerate\}\s*\[', recursive_text):
        raise ValueError('Extended enumerate syntax now requires a real cached enumerate package')
    if cites - entries.keys():
        raise ValueError(f'Missing bibliography keys: {cites - entries.keys()}')
    if re.search(r'AI statement|generative AI|AI-assisted|large language model',
                 manuscript + cover + (out / 'title-page.tex').read_text(), re.I):
        raise ValueError('Unexpected declaration text in submission files')

    compiled = []
    env = dict(os.environ, SOURCE_DATE_EPOCH='0')
    def compile_one(directory: Path, target: str, destination: Path) -> dict:
        destination.mkdir(parents=True, exist_ok=False)
        command = [str(TECTONIC), '-X', 'compile', '-C', '--keep-logs',
                   '--keep-intermediates', '--makefile-rules',
                   str(destination / 'dependencies.mk'), '--outdir', str(destination),
                   str(directory / target)]
        started = now()
        result = subprocess.run(command, cwd=directory, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (destination / 'console.txt').write_text(result.stdout)
        log_path = destination / (Path(target).stem + '.log')
        log = log_path.read_text(errors='replace') if log_path.exists() else ''
        blg_path = destination / (Path(target).stem + '.blg')
        blg = blg_path.read_text(errors='replace') if blg_path.exists() else ''
        errors = re.findall(r'(?im)^.*(?:undefined references|undefined citations|'
                            r'Citation .* undefined|Reference .* undefined|'
                            r'Label .* multiply defined|I couldn.t open database|'
                            r'Warning--I didn.t find a database entry).*$' , log + '\n' + blg)
        pdf = destination / (Path(target).stem + '.pdf')
        if result.returncode or not pdf.is_file() or errors:
            raise RuntimeError(f'{target} compile failed: {destination}\n'
                               + '\n'.join(errors) + '\n' + result.stdout[-2500:])
        warnings = re.findall(r'(?m)^.*(?:Warning|Overfull|Underfull|warning:).*$' , log)
        geometry_log = {stage: re.sub(r'\s+', ' ', values).strip()
            for stage, values in re.findall(
                r'QF-GEOMETRY-(BEFORE|AFTER)\s+([\s\S]*?)QF-GEOMETRY-END',
                log.replace('\n', ''))}
        return {'target': target, 'command': command, 'started_utc': started,
                'completed_utc': now(), 'returncode': result.returncode,
                'pdf_path': str(pdf.relative_to(ROOT)),
                'pages': len(PdfReader(pdf).pages), 'sha256': sha(pdf.read_bytes()),
                'warnings': warnings, 'undefined_or_duplicate_references': errors,
                'bibliography_warnings': re.findall(r'(?m)^Warning--.*$', blg),
                'geometry_log': geometry_log,
                'only_cached': True}

    for target in ('main.tex', 'supplement.tex', 'title-page.tex', 'cover-letter.tex'):
        rec = compile_one(out, target, logs / Path(target).stem)
        compiled.append(rec)
        raw = (ROOT / rec['pdf_path']).read_bytes()
        put(Path(target).with_suffix('.pdf').as_posix(), raw)
        if target == 'main.tex':
            put('main.bbl', (logs / 'main/main.bbl').read_bytes())
            source_names.add('main.bbl')
    page_map = {c['target']: c['pages'] for c in compiled}
    if (page_map['main.tex'] > 35 or page_map['cover-letter.tex'] > 1
            or page_map['title-page.tex'] > 1):
        raise ValueError(f'QF page cap failed: {page_map}')
    bbl = (out / 'main.bbl').read_text()
    printed = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', bbl))
    if printed != cites:
        raise ValueError(f'Bibliography mismatch: missing={cites-printed}, uncited={printed-cites}')

    readme = f'''# Quantitative Finance alternative package

Generated from the current canonical `submission-final/`; the canonical sources are read-only inputs.
This is the regular Research Article alternative. QF uses single-blind review; author fields remain placeholders.

## Files

- `main.tex` / `manuscript.tex` / `main.pdf`: official rQUF2e single-column manuscript with embedded existing tables and vector figures.
- `supplement.tex` / `supplement.pdf`: unchanged canonical supplement content and its local dependencies.
- `title-page.tex` / `title-page.pdf`: canonical author-information template plus the actual frozen narrative word count, current canonical keywords, and CRediT/JEL placeholders; capped at one page.
- `cover-letter.tex` / `cover-letter.pdf`: three substantive paragraphs for QF, scope quotation and GitHub-preprint disclosure.
- `references.bib`, `rQUF.bst`, `main.bbl`: source bibliography, unchanged publisher bibliography style and the actual cited reference list.
- `rQUF2e.cls`: unchanged publisher class. The author-side preamble replaces the class's fictional publication header with a submission-draft header. Its cached `geometry` setup preserves letter paper, resets the class's inherited horizontal/vertical offsets to zero, sets left/right margins to 22 mm and top/bottom margins to 24 mm including headers/footers, and sets header height/separation to 14/15 pt and footer separation to 20 pt. This corrects the old class's 4 pt footer collision under the restored modern output routine. The resulting body width is larger than the canonical 160 mm body width; scientific figures are unchanged.
- `epsfig.sty` and `rotating.sty`: unchanged support files from the same official ZIP. `qf-compat.tex` retains the installed LaTeX kernel's document entry points, replacing the class's incompatible 2014 copies; publisher typography remains, with the explicit author-side page geometry described above. It skips the unused extended-enumeration interface, unavailable in both the ZIP and local cache; standard lists remain, and the builder rejects extended enumerate syntax.
- `qf-fonts.tex`: scalable cached Latin Modern OpenType text faces, with standard math left in Computer Modern. Small caps use the regular face and bold italic uses explicit emboldening of the italic face; this avoids unavailable cache fonts without downloading. Only font setup is added to the supplement/title-page preambles; their bodies stay unchanged.
- `source-manifest.json` and `source-package.zip`: complete transitive local source closure; backups and compiler logs are excluded.
- `BUILD-RECEIPT.json`: actual input/output hashes, commands, page counts and source-ZIP compilation checks.

## Rebuild

Use the existing environment from the repository root:

```sh
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pypdf python -B notes/submission/build_qf_package.py
```

The builder reads the current canonical files on each run and backs up changed, untracked outputs before replacement. It never changes canonical science, results or figures. It compiles with cached Tectonic only, and writes logs below `.scratch/submission/qf/`.
Changed PDF outputs and build receipts are backed up even if tracked. Rejected pre-geometry and inherited-offset trial cuts are retained below `failed-cuts/` with explicit `FAIL_VISUAL_*_SUPERSEDED` receipts; their old success claims apply only to source compilation and are explicitly superseded for visual use. No failed PDF is deleted.

## Editorial checks and remaining author actions

The abstract is unchanged ({abstract_words} source words); there are {len(keywords_list)} unchanged keywords. The title page reports the actual canonical narrative count ({narrative_words} words), read from the shared frozen `notes/submission/writing_metrics.py` definition, together with its exclusions and the canonical keywords. Main, title-page and cover-letter page caps are checked automatically. Citation groups are ordered by the inherited bibliography years without changing their membership. Only cited references are printed; historical uncited database entries remain in the database. An explicit canonical `(n.d.)` label is supplied as a packaging-only BibTeX date where the database omitted its date.
Existing institution fields are mapped to school/howpublished where the publisher style requires them, and existing URL/DOI values are repeated in notes so the old style does not silently omit access routes. No bibliographic fact is acquired or invented. Original missing publication addresses, if any, remain warnings in the receipt.
The derived Wisniewski2020 booktitle omits only its existing literal `Proceedings of the ` prefix, which the unchanged publisher bibliography style adds automatically. Only the exact `Data availability.`, `Code availability.` and `A fixed CFTC history-length extension.` paragraph labels lose their trailing source full stops, because the unchanged class adds those stops. The scientific-body equivalence check permits exactly these three label-punctuation conversions and citation-group ordering; it performs no general punctuation normalization.

Final full-page visual QA is assigned to the root task and is not asserted by this builder. Complete author names, affiliations, corresponding contact, ORCID, funding, competing interests and CRediT roles before any actual submission. The official template requests a JEL classification; its choice remains the author's decision, with a placeholder rather than an invented code. The actual narrative count and keywords update automatically on each build. The author must separately resolve applicable disclosure requirements against the policy record. No claim of permission to redistribute restricted inputs, acceptance, fee payment or completed submission is made.
'''
    put('README.md', readme)
    source_names.add('README.md')
    source_manifest = {n: {'bytes': (out / n).stat().st_size,
                            'sha256': sha((out / n).read_bytes())}
                       for n in sorted(source_names)}
    put('source-manifest.json', json.dumps(source_manifest, indent=2) + '\n')
    source_names.add('source-manifest.json')
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in sorted(source_names):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, (out / name).read_bytes())
    put('source-package.zip', archive.getvalue())
    extracted = logs / 'source-zip-extracted'
    extracted.mkdir()
    with zipfile.ZipFile(io.BytesIO(archive.getvalue())) as z:
        if z.testzip() is not None or set(z.namelist()) != source_names:
            raise ValueError('Source ZIP CRC/member mismatch')
        for n in z.namelist():
            if z.read(n) != (out / n).read_bytes():
                raise ValueError(f'ZIP byte mismatch: {n}')
        z.extractall(extracted)
    zip_compiled = [compile_one(extracted, t, logs / 'zip-check' / Path(t).stem)
                    for t in ('main.tex', 'supplement.tex', 'title-page.tex', 'cover-letter.tex')]
    protected_after = {p.relative_to(canonical).as_posix(): sha(p.read_bytes())
                       for p in canonical.rglob('*') if p.is_file()}
    if protected != protected_after:
        raise RuntimeError('Canonical inputs changed during build; rebuild after the concurrent edit')
    receipt = {
        'status': 'PASS_SOURCE_CLOSURE_COMPILED_VISUAL_QA_PENDING',
        'generated_utc': now(), 'canonical_directory': str(canonical.relative_to(ROOT)),
        'canonical_input_sha256': protected, 'canonical_unchanged_during_build': True,
        'template_download_receipt': 'notes/submission/template-downloads.json',
        'official_template_sha256': {n: sha((templates / n).read_bytes()) for n in ('rQUF2e.cls', 'rQUF.bst')},
        'publisher_class_and_bst_unchanged': all((out / n).read_bytes() == (templates / n).read_bytes() for n in ('rQUF2e.cls', 'rQUF.bst')),
        'page_geometry': {'paper': 'letter', 'left_mm': 22, 'right_mm': 22,
            'top_mm': 24, 'bottom_mm': 24, 'includeheadfoot': True,
            'headheight_pt': 14, 'headsep_pt': 15, 'footskip_pt': 20,
            'hoffset_pt': 0, 'voffset_pt': 0,
            'canonical_body_width_mm': 160, 'qf_body_width_mm': 171.9,
            'root_cause': 'Publisher class footskip=4pt under restored modern kernel outputpage'},
        'superseded_failed_cut': failed_cut,
        'cache_compatibility': 'Author-side macro restores the installed kernel document/enddocument and outputpage entry points in place of incompatible 2014 class copies. Unused enumerate.sty interface is skipped; no extended enumeration syntax is present. Optional sample latexrelease.sty is not used. Official epsfig/rotating support files are included unchanged.',
        'body_equal_after_citation_order_normalization': normalize_citations(qf_body) == normalize_citations(body),
        'body_equal_after_explicit_packaging_normalization': True,
        'science_text_equivalence_rules': {
            'citation_group_order': 'Same key membership; order only',
            'allowed_exact_label_punctuation_pair_count': len(ALLOWED_BODY_LABEL_PUNCTUATION),
            'allowed_exact_label_punctuation_pairs': [
                {'source': source, 'derived': derived}
                for source, derived in ALLOWED_BODY_LABEL_PUNCTUATION],
            'actual_label_punctuation_changes': label_punctuation_changes,
            'other_body_changes_permitted': False},
        'supplement_body_equal': (out / 'supplement.tex').read_text().split('\\begin{document}', 1)[1] == (canonical / 'supplement.tex').read_text().split('\\begin{document}', 1)[1],
        'body_original_sha256': sha(body.encode()), 'body_qf_sha256': sha(qf_body.encode()),
        'citation_group_reorderings': reorderings,
        'bibliography_date_completion': date_additions,
        'bibliography_packaging_field_mappings': bibliography_mappings,
        'cited_keys': sorted(cites), 'printed_keys': sorted(printed),
        'missing_printed_references': sorted(cites - printed),
        'uncited_printed_references': sorted(printed - cites),
        'uncited_database_keys_not_printed': sorted(entries.keys() - cites),
        'abstract_source_words': abstract_words, 'keywords': keywords_list,
        'narrative_word_count': narrative_words,
        'narrative_word_count_scope': word_count_scope,
        'frozen_writing_metric_sha256': {
            str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in (metric_reader, metric_source)},
        'title_page_metadata': {'word_count': narrative_words,
            'keywords': keywords_list, 'CRediT': 'AUTHOR_PLACEHOLDER',
            'JEL': 'AUTHOR_DECISION_PLACEHOLDER'},
        'page_counts': page_map, 'source_package_members': len(source_names),
        'source_package_sha256': sha(archive.getvalue()),
        'existing_vector_figure_sha256': {n: sha((out / n).read_bytes()) for n in sorted(copied) if n.endswith('.pdf')},
        'compile_records': compiled, 'source_zip_compile_records': zip_compiled,
        'backup_files_created': backups, 'visual_qa': 'PENDING_ROOT_ALL_PAGES',
        'no_downloads_no_scientific_recalculation': True,
        'author_fields': 'PLACEHOLDERS', 'review_mode': 'SINGLE_BLIND',
        'warnings_and_risks': ['Final page-by-page visual QA has not been performed by this builder.',
            'Personal metadata, CRediT roles and JEL classification still require author completion; narrative word count and keywords are generated from canonical inputs.',
            'Inherited bibliography journal-name spelling is preserved; publisher abbreviation checks remain editorial.',
            'Supplement uses its canonical article formatting, separate from the QF main manuscript class.']}
    put('BUILD-RECEIPT.json', json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'page_counts': page_map,
                      'source_members': len(source_names), 'citation_count': len(cites),
                      'logs': str(logs.relative_to(ROOT)),
                      'receipt': str((out / 'BUILD-RECEIPT.json').relative_to(ROOT))}, indent=2))


if __name__ == '__main__':
    main()
