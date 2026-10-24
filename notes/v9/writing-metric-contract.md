# v8 writing metric contract

This freezes B4 editorial measurement before manuscript changes. The original PR3 checker was read at commit `2328994c44ec02bd731ad556f41fe9821f6de6df`, file `notes/supervisor-20261023/writing-pass-check.py`, during the preceding read-only B0 inventory. This audit does not invoke Git. The code below copies the original pure statistic functions and constants; the final function adapts unified v7/v8 manuscript I/O and reproduces the original `inventory()` float/table exclusions. It does not alter manuscripts or create checker outputs.

Scope: Introduction through Conclusion, including Research design and transparency. Headings, tables, figures/captions, displayed formula contents, declarations and references are excluded; captions are checked separately for forbidden words. Inline mathematical letters and numbers remain eligible word tokens. This differs from the v7 `writing_metrics.py`, whose negation and >35-word metrics must not substitute for B4.

The same full-stop sentence splitter, word regex and flagged-term morphology apply before and after. Paragraph boundaries and omitted display formulas do not automatically terminate a sentence. The one 42-word baseline sentence starts at manuscript line 83 with “Define the peak ... by”; the following display is omitted and the next prose sentence joins it. Fix prose punctuation if desired; do not change the splitter.

Original PR3 historical thresholds in `target_pass` are mean <=25 and flagged <8%; user v8 thresholds override those thresholds to mean <=20 and flagged <=8%, with zero sentences >40 words. These are reported separately as `v8_target_pass` so the statistic stays traceable. No deletion of required limitations or scope exclusion is allowed solely to pass metrics.

Verified local v7 baseline: 219 sentences; 4,222 words; 29 flagged sentences; 13.2420091324%; mean 19.2785388128 words; one sentence >40 words; body forbidden occurrences archive=1 and analogue=1. The task-described 16.1% /21.2 /8 did not reproduce for local HEAD5e35dba under this adaptation. Retain that discrepancy explicitly.

The JSON contains sentence-level text/locations, flagged sentences and two-decimal percentage paragraphs to guide revision. The source SHA256 and copied-code fingerprints bind this measurement.

To make a v8 checker, copy the following code to a new v8 module, call `unified_manuscript_statistics(Path("submission-jof/manuscript.tex"))`, and write to a new explicitly named JSON output. Existing untracked outputs require a `.bak` copy before overwrite. Preserve this baseline and the old v7 checker. The code performs no financial analysis.

```python
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
TERMS = ('establish', 'descriptive', 'exploratory', 'post-result', 'inspected',
         'audit', 'readback', 'archive', 'receipt', 'analogue', 'qualify',
         'rather than', 'without', 'does not', 'do not', 'cannot')
FORBIDDEN = ('audit', 'readback', 'archive', 'receipt', 'analogue', 'R0', 'R1',
             'R2', 'R3', 'S1', 'S2', 'S3', 'E3', 'E5', 'R6', '33+', 'Four+')
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?(?:[-‐‑][A-Za-z0-9]+)*|(?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?(?:[-‐‑][A-Za-z]+)*")
NUM = re.compile(r'(?<![A-Za-z0-9])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?|(?<![A-Za-z0-9])[-+−]?\.\d+')
ENV = re.compile(r'\\(begin|end)\{([^}]+)\}')
DISPLAY = ('equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
           'multline', 'multline*', 'displaymath', 'eqnarray', 'eqnarray*')
ABBREVIATIONS = ('e.g.', 'i.e.', 'et al.', 'etc.', 'vs.', 'Dr.', 'Mr.', 'Mrs.',
                 'Prof.', 'Fig.', 'Figs.', 'Eq.', 'Eqs.', 'Sec.', 'No.', 'cf.')

@dataclass
class Blob:
    text: str
    loc: list[tuple[str, int, str]]
    def cut(self, a, b):
        return Blob(self.text[a:b], self.loc[a:b])
    def sub(self, pattern, replacement, flags=0):
        pattern = re.compile(pattern, flags) if isinstance(pattern, str) else pattern
        txt, loc, start = [], [], 0
        for m in pattern.finditer(self.text):
            txt.append(self.text[start:m.start()]); loc.extend(self.loc[start:m.start()])
            value = replacement(m) if callable(replacement) else replacement
            txt.append(value)
            origin = self.loc[m.start()] if self.loc else ('', 0, '')
            loc.extend([origin] * len(value)); start = m.end()
        txt.append(self.text[start:]); loc.extend(self.loc[start:])
        return Blob(''.join(txt), loc)
    def mask(self, intervals):
        chars = list(self.text)
        for a, b in intervals:
            chars[a:b] = ['\n' if c == '\n' else ' ' for c in chars[a:b]]
        return Blob(''.join(chars), self.loc[:])


def balanced(text, opening):
    if opening >= len(text) or text[opening] != '{':
        return None
    depth = 1; i = opening + 1
    while i < len(text):
        if text[i] == '\\':
            i += 2; continue
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if not depth: return i + 1
        i += 1
    raise ValueError('Unclosed TeX group near ' + text[opening:opening + 80])


def command_groups(blob, names, keep=()):
    """Remove named commands and their optional/required groups; keep chosen args."""
    pattern = re.compile(r'\\(' + '|'.join(names) + r')(?![A-Za-z])\*?')
    result_text, result_loc, start = [], [], 0
    for m in pattern.finditer(blob.text):
        if m.start() < start: continue
        i = m.end()
        while i < len(blob.text) and blob.text[i].isspace(): i += 1
        if i < len(blob.text) and blob.text[i] == '[':
            end = blob.text.find(']', i)
            if end >= 0: i = end + 1
        groups = []
        count = 2 if m.group(1) in ('href', 'textcolor', 'colorbox', 'resizebox') else 1
        for _ in range(count):
            while i < len(blob.text) and blob.text[i].isspace(): i += 1
            end = balanced(blob.text, i)
            if end is None: break
            groups.append((i + 1, end - 1)); i = end
        result_text.append(blob.text[start:m.start()]); result_loc.extend(blob.loc[start:m.start()])
        for k in keep:
            if k < len(groups):
                a, b = groups[k]; result_text.append(blob.text[a:b]); result_loc.extend(blob.loc[a:b])
        result_text.append(' '); result_loc.append(blob.loc[m.start()]); start = i
    result_text.append(blob.text[start:]); result_loc.extend(blob.loc[start:])
    return Blob(''.join(result_text), result_loc)


def strip_comments(text):
    return re.sub(r'(?<!\\)%[^\n]*', lambda m: ' ' * len(m.group()), text)


def environment_spans(blob):
    stack, spans = [], []
    for m in ENV.finditer(blob.text):
        name = m.group(2)
        if m.group(1) == 'begin': stack.append((name, m.start(), m.end()))
        else:
            if not stack or stack[-1][0] != name:
                raise ValueError('Mismatched environment: ' + name)
            n, a, inner = stack.pop(); spans.append((n, a, m.end(), inner, m.start()))
    if stack: raise ValueError('Unclosed environment(s): ' + str(stack))
    return sorted(spans, key=lambda x: x[1])


def captions(blob):
    found = []
    for m in re.finditer(r'\\caption(?:\[[^\]]*\])?\s*', blob.text):
        end = balanced(blob.text, m.end())
        if end: found.append((m.start(), end, m.end()+1, end-1))
    return found


def plain(blob, omit_display=False, omit_headings=True):
    if omit_display:
        blob = blob.mask([(a,b) for n,a,b,_,_ in environment_spans(blob) if n in DISPLAY])
        blob = blob.sub(r'\\\[.*?\\\]', ' ', re.S)
    if omit_headings:
        blob = command_groups(blob, ('section', 'subsection', 'subsubsection', 'paragraph'))
    blob = command_groups(blob, ('citep','citet','cite','citealp','citeauthor','citeyear','ref','eqref','pageref','label','url','includegraphics','hspace','vspace','setlength','rule'))
    blob = command_groups(blob, ('href', 'textcolor', 'colorbox'), keep=(1,))
    blob = blob.sub(r'\\(?:begin|end)\{[^}]+\}(?:\[[^\]]*\])?', ' ')
    blob = blob.sub(r'\\(?:toprule|midrule|bottomrule|hline|cline|FloatBarrier|centering|smallskip|medskip|bigskip|par|small|footnotesize|scriptsize|tiny|normalsize|raggedright|linewidth|textwidth)(?![A-Za-z])', ' ')
    blob = blob.sub(r'\\(?:textbf|textit|emph|texttt|textrm|textsf|mbox|text|mathrm|mathbf|mathsf|mathcal|mathbb|operatorname)(?![A-Za-z])', '')
    blob = blob.sub(r'\\(?:left|right|big|Big|bigl|bigr|biggl|biggr)(?![A-Za-z])', '')
    blob = blob.sub(r'\\(?:times|cdot)(?![A-Za-z])', ' × ')
    blob = blob.sub(r'\\(?:leq?|geq?)(?![A-Za-z])', ' ')
    blob = blob.sub(r'\\(?:ldots|cdots|dots)(?![A-Za-z])', ' … ')
    blob = blob.sub(r'\\([%&#_])', lambda m: m.group(1))
    blob = blob.sub(r'\\\\(?:\[[^\]]*\])?', ' ')
    blob = blob.sub(r'\\[A-Za-z]+\*?', ' ')
    blob = blob.sub(r'\\[!,:; ]', ' ')
    blob = blob.sub(r'[{}$^_&]', ' ')
    blob = blob.sub(r'~', ' ')
    blob = blob.sub(r'---|--', '—')
    blob = blob.sub(r'\s+', ' ')
    return blob


def term_regex(term):
    # Match grammatical suffixes for the flagged editorial stems; codes stay exact.
    if term in ('establish', 'qualify'):
        root = r'establish(?:es|ed|ing|ment|ments)?' if term == 'establish' else r'qualif(?:y|ies|ied|ying)'
    elif term in ('audit','readback','archive','receipt','analogue'):
        root = re.escape(term) + (r'(?:s|d|ed|ing)?' if term != 'archive' else r'(?:s|d|ing)?')
    else: root = re.escape(term).replace(r'\ ', r'\s+')
    return re.compile(r'(?<![A-Za-z0-9])' + root + r'(?![A-Za-z0-9])', re.I)


def source_at(blob, pos):
    file, line, macro = blob.loc[min(pos, len(blob.loc)-1)]
    d = {'file': file, 'line': line}
    if macro: d['macro'] = macro
    return d


def sentences(blob):
    protected = set()
    for abbr in ABBREVIATIONS:
        for m in re.finditer(re.escape(abbr), blob.text, re.I):
            protected.update(i for i in range(m.start(),m.end()) if blob.text[i] == '.')
    for m in re.finditer(r'(?<=\d)\.(?=\d)|(?<![A-Za-z0-9])\.(?=\d)|\b[A-Z]\.(?=\s*[A-Z]\.)', blob.text):
        protected.add(m.start())
    out, start = [], 0
    for i,c in enumerate(blob.text):
        if c == '.' and i not in protected:
            if i + 1 < len(blob.text) and not (blob.text[i+1].isspace() or blob.text[i+1] in '\"”\')]}'): continue
            out.append((start, i+1)); start = i+1
    if blob.text[start:].strip(): out.append((start,len(blob.text)))
    records=[]
    for a,b in out:
        s = blob.text[a:b].strip()
        if not WORD.search(s): continue
        offset = a + len(blob.text[a:b]) - len(blob.text[a:b].lstrip())
        records.append({'id':len(records)+1, 'text':s, 'words':len(WORD.findall(s)),
                        'terms':[t for t in TERMS if term_regex(t).search(s)],
                        'location':source_at(blob,offset)})
    return records


def statistics(body, caption_blobs, abstract):
    clean = plain(body, omit_display=True)
    records = sentences(clean)
    hits = [x for x in records if x['terms']]
    forbidden=[]
    for t in FORBIDDEN:
        for m in term_regex(t).finditer(clean.text):
            forbidden.append({'term':t,'matched':m.group(), 'location':source_at(clean,m.start()),
                              'context':clean.text[max(0,m.start()-80):m.end()+100]})
    caps=[]
    for name,bl in caption_blobs:
        cp=plain(bl,omit_headings=False)
        for t in FORBIDDEN:
            for m in term_regex(t).finditer(cp.text):
                caps.append({'caption':name,'term':t,'matched':m.group(),'location':source_at(cp,m.start()),'context':cp.text})
    n=len(records); words=sum(x['words'] for x in records)
    result = {'sentences':n,'words':words,'flagged_sentences':len(hits),
              'flagged_proportion':len(hits)/n if n else 0,
              'average_sentence_words':words/n if n else 0,
              'over_40_words':sum(x['words']>40 for x in records),
              'forbidden_occurrences':len(forbidden),
              'forbidden_by_term':dict(Counter(x['term'] for x in forbidden)),
              'main_caption_forbidden_occurrences':len(caps),
              'target_pass':{'flagged_below_8_percent':len(hits)/n<.08 if n else False,
                             'average_at_most_25':words/n<=25 if n else False,
                             'no_sentences_over_40':all(x['words']<=40 for x in records),
                             'no_forbidden_body_terms':not forbidden},
              'abstract_words':len(WORD.findall(plain(abstract).text)),
              'abstract_numeric_occurrences':len(list(NUM.finditer(plain(abstract).text))),
              'sentences_detail':records,'flagged_detail':hits,
              'long_sentences':[x for x in records if x['words']>40],
              'forbidden_detail':forbidden,'main_caption_forbidden_detail':caps}
    return result

def unified_manuscript_statistics(path):
    # I/O and region adapter only; PR3 text/sentence/term rules are unchanged.
    path=Path(path)
    raw=path.read_text()
    text=strip_comments(raw)
    loc=[]
    for line,row in enumerate(text.splitlines(keepends=True),1):
        loc.extend([(str(path),line,'')]*len(row))
    blob=Blob(text,loc)
    ab=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',text,re.S)
    first=re.search(r'\\section\{Introduction\}',text)
    stop=re.search(r'\\section\*\{(?:Data and code availability|Declarations and availability|References)\}',text)
    if not (ab and first and stop): raise ValueError('Main boundaries unavailable')
    abstract=blob.cut(ab.start(1),ab.end(1))
    sections=blob.cut(first.start(),stop.start())
    spans=environment_spans(sections)
    floats=[s for s in spans if s[0] in ('table','table*','figure','figure*')]
    tables=[s for s in spans if s[0] in ('tabular','tabular*','tabularx','longtable','array')]
    caps=[(f'main-caption-{i}',sections.cut(c,d)) for i,(_,_,c,d) in enumerate(captions(sections),1)]
    body=sections.mask([(a,b) for _,a,b,_,_ in floats]+[(a,b) for _,a,b,_,_ in tables])
    result=statistics(body,caps,abstract)
    result['v8_target_pass']={
        'flagged_at_most_8_percent':result['flagged_proportion']<=.08,
        'average_at_most_20':result['average_sentence_words']<=20,
        'no_sentences_over_40':result['over_40_words']==0,
    }
    return result
```
