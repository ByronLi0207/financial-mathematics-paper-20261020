#!/usr/bin/env python3
"""Deterministic, read-only TeX writing and numeric inventory checker.

Only writes the explicitly named JSON outputs. Existing outputs are copied to a
unique .bak file first. No fitting, experiment, build, data, or Git operations.

Snapshot example (run from repository root):
  python3 notes/supervisor-20261023/writing-pass-check.py snapshot \
    --source .scratch/writing-pass-20261023/before/manuscript/supervisor-revision \
    --label before --stats notes/supervisor-20261023/writing-pass-before.json \
    --numbers notes/supervisor-20261023/writing-pass-numbers-before.json
Comparison example:
  python3 notes/supervisor-20261023/writing-pass-check.py compare \
    --before notes/supervisor-20261023/writing-pass-numbers-before.json \
    --after notes/supervisor-20261023/writing-pass-numbers-after.json \
    --out notes/supervisor-20261023/writing-pass-numbers-comparison.json

Counts are editorial diagnostics, not a linguistic gold standard. Every sentence
and numeric occurrence is included with its source location for human review.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import shutil

TERMS = ('establish', 'descriptive', 'exploratory', 'post-result', 'inspected',
         'audit', 'readback', 'archive', 'receipt', 'analogue', 'qualify',
         'rather than', 'without', 'does not', 'do not', 'cannot')
FORBIDDEN = ('audit', 'readback', 'archive', 'receipt', 'analogue', 'R0', 'R1',
             'R2', 'R3', 'S1', 'S2', 'S3', 'E3', 'E5', 'R6', '33+', 'Four+')
WORD = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?(?:[-‐‑][A-Za-z0-9]+)*|(?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?(?:[-‐‑][A-Za-z]+)*")
NUM = re.compile(r'(?<![A-Za-z0-9])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?|(?<![A-Za-z0-9])[-+−]?\.\d+')
STRUCTURAL_REFERENCE = re.compile(r'(?:Sections?|Tables?|Figures?|Equations?|Eqs?|Steps?)\s+(?:\d+(?:\.\d+)?\s*(?:[–—-]|to|and)\s*)?$', re.I)
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


def read_macros(source):
    macros = {}
    for path in sorted((source / 'generated').glob('*facts.tex')):
        text = strip_comments(path.read_text())
        for m in re.finditer(r'\\(?:newcommand|renewcommand)\s*\{\\([A-Za-z]+)\}\s*', text):
            end = balanced(text, m.end())
            if end:
                macros[m.group(1)] = (text[m.end()+1:end-1], str(path.relative_to(source)), text.count('\n', 0, m.start())+1)
    return macros


def load(source, relative, macros, stack=()):
    path = source / relative
    if relative in stack: raise ValueError('Recursive input: ' + relative)
    text = strip_comments(path.read_text())
    loc = []
    for line, row in enumerate(text.splitlines(keepends=True), 1):
        loc.extend([(relative, line, '')] * len(row))
    blob = Blob(text, loc)
    pieces, locations, cursor = [], [], 0
    for m in re.finditer(r'\\input\{([^}]+)\}', blob.text):
        pieces.append(blob.text[cursor:m.start()]); locations.extend(blob.loc[cursor:m.start()])
        child = str(Path(relative).parent / m.group(1))
        if not child.endswith('.tex'): child += '.tex'
        sub = load(source, child, macros, stack + (relative,))
        pieces.append(sub.text); locations.extend(sub.loc); cursor = m.end()
    pieces.append(blob.text[cursor:]); locations.extend(blob.loc[cursor:])
    blob = Blob(''.join(pieces), locations)
    if macros:
        expression = re.compile(r'\\(' + '|'.join(sorted(macros, key=len, reverse=True)) + r')(?![A-Za-z])(?:\{\})?')
        for _ in range(5):
            if not expression.search(blob.text): break
            chunks, origins, cursor = [], [], 0
            for m in expression.finditer(blob.text):
                chunks.append(blob.text[cursor:m.start()]); origins.extend(blob.loc[cursor:m.start()])
                value = macros[m.group(1)][0]; chunks.append(value)
                file, line, _ = blob.loc[m.start()]
                origins.extend([(file, line, m.group(1))] * len(value)); cursor = m.end()
            chunks.append(blob.text[cursor:]); origins.extend(blob.loc[cursor:])
            blob = Blob(''.join(chunks), origins)
    return blob


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
            if i + 1 < len(blob.text) and not (blob.text[i+1].isspace() or blob.text[i+1] in '"”\')]}'): continue
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


def normalize_number(value):
    try:
        d=Decimal(value.replace(',','').replace('−','-'))
        return '0' if not d else format(d.normalize(), 'f')
    except InvalidOperation: return value


def numeric_records(blob, category, context_kind='prose'):
    clean=plain(blob,omit_display=False)
    out=[]
    for m in NUM.finditer(clean.text):
        token=m.group(); pos=m.start()
        if STRUCTURAL_REFERENCE.search(clean.text[max(0,pos-60):pos]):
            continue
        after=clean.text[m.end():m.end()+4]
        value=normalize_number(token)
        # A percentage is a distinct evidence unit from an equal non-percentage.
        unit='percent' if re.match(r'\s*%',after) else 'number'
        out.append({'category':category,'kind':context_kind,'literal':token,'normalized':value,
                    'unit':unit,'key':value+'|'+unit,'location':source_at(clean,pos),
                    'context':clean.text[max(0,pos-100):m.end()+120].strip()})
    return out


def digest(text): return hashlib.sha256(text.encode()).hexdigest()


def inventory(source, macros, abstract, sections, appendix):
    records=[]; table_fingerprints=[]; math_fingerprints=[]; captions_list=[]
    records.extend(numeric_records(abstract,'abstract'))
    body_sections=None
    for label, blob in [('main',sections),('appendix',appendix)]:
        spans=environment_spans(blob)
        float_spans=[s for s in spans if s[0] in ('table','table*','figure','figure*')]
        capspans=captions(blob)
        for idx,(a,b,c,d) in enumerate(capspans,1):
            cp=blob.cut(c,d); name=f'{label}-caption-{idx}'
            records.extend(numeric_records(cp, label+'_captions'))
            if label=='main': captions_list.append((name,cp))
        tables=[s for s in spans if s[0] in ('tabular','tabular*','tabularx','longtable','array')]
        for idx,(env,a,b,c,d) in enumerate(tables,1):
            tb=blob.cut(a,b)
            # Preserve table values and mathematical expressions independent of captions/notes.
            clean=plain(tb,omit_headings=False)
            # Drop the tabular's column specification, whose digits can be formatting widths.
            opener=ENV.match(tb.text)
            data_start=opener.end() if opener else 0
            while data_start<len(tb.text) and tb.text[data_start].isspace():data_start+=1
            if data_start<len(tb.text) and tb.text[data_start]=='{':data_start=balanced(tb.text,data_start)
            data=tb.cut(data_start,len(tb.text))
            rr=numeric_records(data,label+'_table_data','table_data')
            records.extend(rr)
            values=[r['key'] for r in rr]
            formulas=[re.sub(r'\s+','',m.group()) for m in re.finditer(r'\$[^$]*\$|\\\(.*?\\\)',data.text,re.S)]
            table_fingerprints.append({'id':f'{label}-table-{idx}',
                    'location':source_at(blob,a),'numeric_sequence':values,
                    'numeric_sha256':digest(json.dumps(values)),
                    'math_sequence':formulas,'math_sha256':digest(json.dumps(formulas)),
                    'raw_sha256':digest(tb.text)})
        table_float=[s for s in float_spans if s[0].startswith('table')]
        for _,a,b,_,_ in table_float:
            exclusions=[(max(a,x),min(b,y)) for x,y,_,_ in capspans if x>=a and y<=b]
            exclusions += [(x,y) for _,x,y,_,_ in tables if x>=a and y<=b]
            note=blob.mask(exclusions).cut(a,b)
            records.extend(numeric_records(note,label+'_table_notes'))
        outside=blob.mask([(a,b) for _,a,b,_,_ in float_spans]+[(a,b) for _,a,b,_,_ in tables])
        if label=='main': body_sections=outside
        displays=[(a,b) for n,a,b,_,_ in environment_spans(outside) if n in DISPLAY]
        for idx,(a,b) in enumerate(displays,1):
            math=outside.cut(a,b)
            records.extend(numeric_records(math,label+'_body_math','display_math'))
            normalized=re.sub(r'\\label\{[^}]+\}|\s+','',math.text)
            math_fingerprints.append({'id':f'{label}-display-{idx}','location':source_at(outside,a),
                                      'sha256':digest(normalized),'normalized_tex':normalized})
        prose=outside.mask(displays)
        records.extend(numeric_records(prose,label+'_body'))
        # Inline math fingerprints include formulas in the main/appendix body.
        for idx,m in enumerate(re.finditer(r'\$[^$]*\$|\\\(.*?\\\)',prose.text,re.S),1):
            math_fingerprints.append({'id':f'{label}-inline-{idx}','location':source_at(prose,m.start()),
                    'sha256':digest(re.sub(r'\s+','',m.group())), 'normalized_tex':re.sub(r'\s+','',m.group())})
    # References and citation years, section/table/equation references, TeX layout
    # parameters and headings are absent from the empirical-value inventory.
    counts=Counter(r['key'] for r in records)
    return {'occurrence_count':len(records),'counts_by_category':dict(Counter(r['category'] for r in records)),
            'value_multiset':dict(sorted(counts.items())), 'occurrences':records,
            'table_fingerprints':table_fingerprints,'body_math_fingerprints':math_fingerprints},body_sections,captions_list


METHOD = {
 'scope':'Sections 1 through Conclusion from sections.tex and its recursive inputs; no headings, tables, figures/captions, references or appendices. Main captions flagged separately.',
 'macros':'Expand zero-argument newcommand/renewcommand definitions from generated/*facts.tex. Expanded values retain invocation source location and macro name.',
 'sentences':'Split on full stops only (not semicolons, colons, question marks or paragraph breaks); protect decimal points, leading-decimal fractions, listed standard abbreviations and initial sequences. A nonempty final fragment counts as a sentence.',
 'protected_abbreviations':list(ABBREVIATIONS),
 'words':"English alphabetic words, contractions, numeric literals and alphanumeric hyphen compounds; an internal ASCII/nonbreaking hyphen keeps a compound as one word. Math command names and symbols do not count; readable inline letters/numbers count. Displayed formulas omitted from writing statistics.",
 'flagged_terms':list(TERMS),
 'term_matching':'Case-insensitive whole words/phrases. establish and qualify include common inflections; audit/readback/archive/receipt/analogue include common inflections. Codes match whole alphanumeric tokens, including textual occurrences in captions.',
 'number_inventory':'Values expanded before inventory. Categories distinguish abstract, main_body, main_body_math, main_captions, main_table_data, main_table_notes and appendix equivalents. Citations, labels, refs, URL targets, headings and layout widths are removed. Scientific-notation TeX is recorded as its literal numeric components, and the surrounding expression remains in context/fingerprints. Numbers inside model codes are excluded by alphanumeric boundaries. Literal numbered Section/Table/Figure/Equation/Step references are excluded separately; 24-step prediction horizons remain substantive numbers.',
 'numeric_comparison':'Each surviving AFTER empirical number must find an identical normalized value and percent/nonpercent unit in the BEFORE evidence pool, with source context retained. Removed occurrences are expected after condensation. Repeated existing values are allowed but flagged when an AFTER count exceeds BEFORE; counts alone cannot prove claim equivalence. A change in rounding requires an explicit documented exception, never automatic acceptance.',
 'immutability':'Table numeric sequences and inline-math sequences must match exactly in order. All body display formulas are whitespace/label-normalized and compared as a multiset; editorial relocation is allowed. Raw source/figure hashes are also reported for independent provenance.'
}


def safe_write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        backup=Path(str(path)+'.bak');i=1
        while backup.exists():backup=Path(str(path)+f'.bak.{i}');i+=1
        shutil.copy2(path,backup)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def snapshot(args):
    source=Path(args.source).resolve(); macros=read_macros(source)
    abstract=load(source,'abstract.tex',macros)
    sections=load(source,'sections.tex',macros)
    appendix=load(source,'appendices.tex',macros)
    numbers,body,caps=inventory(source,macros,abstract,sections,appendix)
    meta={'label':args.label,'source':str(source),'created_utc':datetime.now(timezone.utc).isoformat(),
          'baseline_commit':args.baseline_commit,'method':METHOD,
          'source_sha256':{str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source.rglob('*')) if p.is_file() and p.suffix in ('.tex','.pdf')},
          'macros':{k:{'value':v[0],'definition_file':v[1],'definition_line':v[2]} for k,v in macros.items()}}
    stats=statistics(body,caps,abstract)
    safe_write(args.stats,{**meta,**stats});safe_write(args.numbers,{**meta,**numbers})
    print(json.dumps({k:stats[k] for k in ('sentences','words','flagged_sentences','flagged_proportion','average_sentence_words','over_40_words','forbidden_occurrences','main_caption_forbidden_occurrences','abstract_words','abstract_numeric_occurrences')},indent=2))
    print('Numeric categories: '+json.dumps(numbers['counts_by_category'],sort_keys=True))


def compare(args):
    before=json.loads(Path(args.before).read_text());after=json.loads(Path(args.after).read_text())
    bc=Counter(before['value_multiset']);ac=Counter(after['value_multiset'])
    unsupported=sorted(set(ac)-set(bc))
    additions={k:ac[k]-bc[k] for k in ac if ac[k]>bc[k]}
    removals={k:bc[k]-ac[k] for k in bc if bc[k]>ac[k]}
    def tables_by_file(items):
        result=defaultdict(list)
        for x in items: result[x['location']['file']].append(x)
        return result
    bb=tables_by_file(before['table_fingerprints'])
    ab=tables_by_file(after['table_fingerprints'])
    table_changes=[]
    for name in sorted(set(bb)|set(ab)):
        a,b=bb.get(name),ab.get(name)
        if not a or not b or [(x['numeric_sequence'],x['math_sequence']) for x in a]!=[(x['numeric_sequence'],x['math_sequence']) for x in b]:
            table_changes.append({'file':name,'before':a,'after':b})
    bmath=Counter(x['sha256'] for x in before['body_math_fingerprints'] if '-display-' in x['id'])
    amath=Counter(x['sha256'] for x in after['body_math_fingerprints'] if '-display-' in x['id'])
    figure_files=set(k for k in before['source_sha256'] if k.startswith('figures/'))|set(k for k in after['source_sha256'] if k.startswith('figures/'))
    figures_changed=[k for k in sorted(figure_files) if before['source_sha256'].get(k)!=after['source_sha256'].get(k)]
    report={'before':args.before,'after':args.after,'method':METHOD,
        'unsupported_numeric_keys':unsupported,'increased_occurrence_counts':additions,
        'removed_occurrence_counts':removals,
        'unsupported_occurrences':[x for x in after['occurrences'] if x['key'] in unsupported],
        'after_to_before_evidence':[{**x,'baseline_locations':[y['location'] for y in before['occurrences'] if y['key']==x['key']]} for x in after['occurrences']],
        'table_data_or_math_changes':table_changes,'display_formula_multiset_equal':bmath==amath,
        'figures_changed':figures_changed,
        'automated_checks_pass':not unsupported and not table_changes and bmath==amath and not figures_changed,
        'human_review_required':'Check contexts for reassigning an existing value to a different claim; review increased counts and any documented rounding exceptions. Mere set membership is not semantic equivalence.'}
    safe_write(args.out,report)
    print(json.dumps({k:report[k] for k in ('unsupported_numeric_keys','increased_occurrence_counts','display_formula_multiset_equal','figures_changed','automated_checks_pass')},indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('snapshot');p.add_argument('--source',required=True);p.add_argument('--label',required=True)
    p.add_argument('--stats',required=True);p.add_argument('--numbers',required=True)
    p.add_argument('--baseline-commit',default='0ebc6e5');p.set_defaults(func=snapshot)
    p=sub.add_parser('compare');p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);p.set_defaults(func=compare)
    args=parser.parse_args();args.func(args)
if __name__=='__main__': main()
