"""Add exact source/context bindings to the unchanged v8 numeric audit.

This guard can resolve only located UNBOUND numeric/word occurrences and an
explicit new figure's identity failure. Every other legacy failure survives.
It neither reads private arrays nor performs financial/statistical analysis.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEGACY_PATH = 'notes/revision-v8/check_wp8_main_numbers.py'
LEGACY_SHA256 = 'a2fa6f10a085dfda25fd73faf8eec814b77f290fd167e863f16e5a2b437688c1'
MAIN = 'submission-jof/manuscript.tex'
LETTER = 'submission-jof/cover-letter.md'
DEFAULT_BINDINGS = 'notes/revision-v9/wp6-main-context-bindings.json'
TOKEN = re.compile(r'[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?')
WORDS = re.compile(r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|hundred|thousand)\b', re.I)
NUMBER_WORDS = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()


class BindingError(ValueError):
    def __init__(self, category, **detail):
        super().__init__(category)
        self.category, self.detail = category, detail


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identical(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, list):
        return len(a) == len(b) and all(identical(x,y) for x,y in zip(a,b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(identical(a[k],b[k]) for k in a)
    return a == b


def inside(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError('repository-relative path required')
    path = (Path(root) / relative).resolve()
    path.relative_to(Path(root).resolve())
    return path


def pointer(value, path):
    if path == '':
        return value
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('JSON pointer must be empty or start with slash')
    for part in path[1:].split('/'):
        part = part.replace('~1','/').replace('~0','~')
        value = value[int(part)] if isinstance(value,list) else value[part]
    return value


def read_bound_json(root, relative, digest):
    raw = inside(root, relative).read_bytes()
    if sha(raw) != digest:
        raise BindingError('V9_SOURCE_HASH_MISMATCH', source=relative)
    return json.loads(raw, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON constant')))


def display(value, operation):
    """Small explicit presentation/count algebra, never arbitrary evaluation."""
    if not isinstance(operation, dict):
        raise ValueError('display_operation must be an object')
    kind = operation['type']
    if kind == 'exact':
        shown = value
    elif kind == 'format':
        if type(value) not in (int,float) or not math.isfinite(value):
            raise ValueError('finite real required for formatting')
        spec = operation['spec']
        if not re.fullmatch(r'[+]?\.\d{1,2}[fg]', spec):
            raise ValueError('only explicit fixed/significant-digit formatting is allowed')
        shown = format(value,spec)
    elif kind == 'fraction':
        if not isinstance(value,list) or len(value)!=2 or any(type(x) is not int for x in value):
            raise ValueError('fraction needs exactly two native integer counts')
        shown = f'{value[0]}/{value[1]}'
    elif kind == 'length':
        if not isinstance(value,list):
            raise ValueError('length requires an explicit source array')
        shown = len(value)
    elif kind == 'count_eq':
        if not isinstance(value,list):
            raise ValueError('count_eq requires an explicit source array')
        values = [pointer(x,operation['field']) for x in value] if 'field' in operation else value
        shown = sum(identical(x,operation['equals']) for x in values)
    else:
        raise ValueError('unsupported display operation')
    if operation.get('as') == 'word':
        if type(shown) is not int or not 0 <= shown <= 20:
            raise ValueError('source-bound word count must be an integer from zero to twenty')
        return NUMBER_WORDS[shown]
    if type(shown) not in (int,float,str) or isinstance(shown,bool):
        raise ValueError('display must be native integer, finite real, or exact text')
    if isinstance(shown,float) and not math.isfinite(shown):
        raise ValueError('nonfinite display')
    return str(shown)


def source_display(row, root):
    data = read_bound_json(root,row['source'],row['source_sha256'])
    paths = row.get('pointers')
    value = [pointer(data,p) for p in paths] if paths is not None else pointer(data,row['pointer'])
    if not identical(value,row['raw_value']):
        raise BindingError('V9_SOURCE_VALUE_MISMATCH',source=row['source'],pointer=paths or row.get('pointer'))
    return display(value,row['display_operation'])


def digit_key(file, text, start, literal):
    return file,text.count('\n',0,start)+1,start-(text.rfind('\n',0,start)+1)+1,literal


def word_key(file, text, match):
    return file,text.count('\n',0,match.start())+1,match.group(),text[max(0,match.start()-70):min(len(text),match.end()+120)]


def verify_figure(row, root):
    """Verify copy/receipt identity; defer numerical values and pixels."""
    source = inside(root,row['source'])
    target = inside(root,row['path'])
    digest = row['sha256']
    if sha(source.read_bytes()) != digest or sha(target.read_bytes()) != digest:
        raise ValueError('figure source/copy hash mismatch')
    receipts = {key:read_bound_json(root,row[key]['source'],row[key]['sha256'])
                for key in ('placement','point_audit','visual_receipt')}
    matches = [x for x in receipts['placement']['assets']
               if (x['source'],x['target'],x['sha256']) == (row['source'],row['path'],digest)]
    if len(matches) != 1:
        raise ValueError('unique exact placement receipt row required')
    audit, visual = receipts['point_audit'], receipts['visual_receipt']
    directory = str(Path(row['source']).parent)
    if not (audit['status']=='PASS' and audit['difference_count']==0 and audit['mismatch_count']==0
            and audit['render_directory']==directory and audit['output_sha256'][source.name]==digest):
        raise ValueError('point-audit receipt does not identify this final figure')
    if not (visual['status']=='PASS_FINAL_PDF_RENDER_AND_PNG' and visual['chosen_directory']==directory
            and visual['actual_raster_observed'] is True and visual['render_returncode']==0):
        raise ValueError('separate completed visual receipt required')
    return dict(path=row['path'],sha256=digest,receipt_paths={k:row[k]['source'] for k in receipts},
                values_verified_here=False,visual_review_performed_here=False)


def resolve_additions(legacy_report, texts, bindings, *, root=ROOT):
    """Pure additive resolution around a complete, unchanged legacy report."""
    report = copy.deepcopy(legacy_report)
    old_failures = copy.deepcopy(report['failures'])
    extra, verified = [], []
    numeric_locations, word_locations, figure_locations = {}, {}, {}
    def fail(category, **details):
        extra.append(dict(category=category,**details))
    if bindings.get('schema') != 'v9-main-context-bindings-1':
        fail('V9_BINDING_SCHEMA_MISMATCH')
        contexts, figures = [], []
    else:
        contexts, figures = bindings.get('contexts',[]),bindings.get('figures',[])
    seen_ids = set()
    for context in contexts:
        ident = context.get('id')
        try:
            if not isinstance(ident,str) or ident in seen_ids:
                raise ValueError('unique nonempty context id required')
            seen_ids.add(ident)
            file, passage = context['file'],context['text']
            if file not in ('main','cover_letter') or not isinstance(passage,str) or not passage:
                raise ValueError('nonempty exact document context required')
            text = texts[file]
            found = [m.start() for m in re.finditer(re.escape(passage),text)]
            if len(found)!=1:
                raise BindingError('V9_CONTEXT_NOT_UNIQUE',id=ident,hits=len(found))
            start = found[0]
            local_numeric, local_words, checked = {}, {}, []
            for index,row in enumerate(context['bindings']):
                literal, offset, kind = row['literal'],row['offset'],row['kind']
                if type(offset) is not int or offset<0 or not isinstance(literal,str) or not literal or passage[offset:offset+len(literal)]!=literal:
                    raise BindingError('V9_LITERAL_OFFSET_MISMATCH',id=ident,binding=index)
                shown = source_display(row,root)
                if shown != literal:
                    raise BindingError('V9_DISPLAY_MISMATCH',id=ident,binding=index,actual=shown,expected=literal)
                a = start+offset
                evidence = dict(context_id=ident,binding_index=index,source=row['source'],source_sha256=row['source_sha256'],
                                pointer=row.get('pointers',row.get('pointer')),native_value=row['raw_value'],
                                display_operation=row['display_operation'],literal=literal)
                if kind in ('digit','numeric_fragment'):
                    if kind=='digit' and TOKEN.fullmatch(literal) is None:
                        raise ValueError('digit binding must identify one whole numeric token')
                    matches = list(TOKEN.finditer(literal))
                    if not matches:
                        raise ValueError('numeric fragment contains no number')
                    whole = {(m.start(),m.end(),m.group()) for m in TOKEN.finditer(text)}
                    for m in matches:
                        if (a+m.start(),a+m.end(),m.group()) not in whole:
                            raise ValueError('binding covers part of a larger numeric token')
                        key = digit_key(file,text,a+m.start(),m.group())
                        if key in numeric_locations or key in local_numeric:
                            raise ValueError('duplicate numeric occurrence binding')
                        local_numeric[key] = evidence
                elif kind=='word':
                    if WORDS.fullmatch(literal) is None:
                        raise ValueError('word binding must be one complete number word')
                    if not any(m.start()==a and m.end()==a+len(literal) for m in WORDS.finditer(text)):
                        raise ValueError('binding covers part of a larger word')
                    key = (file,a,a+len(literal))
                    if key in word_locations or key in local_words:
                        raise ValueError('duplicate number-word occurrence binding')
                    local_words[key] = evidence
                else:
                    raise ValueError('unsupported binding kind')
                checked.append(evidence)
            numeric_locations.update(local_numeric)
            word_locations.update(local_words)
            verified.append(dict(id=ident,file=file,start=start,end=start+len(passage),text_sha256=sha(passage.encode()),bindings=checked))
        except BindingError as exc:
            fail(exc.category,**exc.detail)
        except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
            fail('V9_BINDING_INVALID',id=ident,error=type(exc).__name__,detail=str(exc))
    for row in figures:
        try:
            path = row['path']
            if path in figure_locations:
                raise ValueError('duplicate figure binding')
            figure_locations[path] = verify_figure(row,root)
        except (OSError,ValueError,KeyError,TypeError,IndexError) as exc:
            fail('V9_FIGURE_BINDING_INVALID',path=row.get('path'),error=type(exc).__name__,detail=str(exc))

    # The old word inventory omits columns. Reconstruct its exact historical
    # failure signature and require a unique actual occurrence before resolving.
    word_occurrences = defaultdict(list)
    for file,text in texts.items():
        text = text.split(r'\begin{thebibliography}',1)[0]
        for m in WORDS.finditer(text):
            word_occurrences[word_key(file,text,m)].append((file,m.start(),m.end()))
    remaining, resolved = [], []
    for failure in old_failures:
        category = failure['category']
        if category=='UNBOUND_NUMERIC_OCCURRENCE':
            key = (failure['file'],failure['line'],failure['column'],failure['token'])
            if key in numeric_locations:
                resolved.append(dict(failure=failure,evidence=numeric_locations[key]))
                continue
        elif category=='UNBOUND_NUMBER_WORD':
            key = (failure['file'],failure['line'],failure['word'],failure['context'])
            positions = word_occurrences.get(key,[])
            if len(positions)==1 and positions[0] in word_locations:
                resolved.append(dict(failure=failure,location=positions[0],evidence=word_locations[positions[0]]))
                continue
        elif category=='UNBOUND_OR_CHANGED_FIGURE_SOURCE' and failure['path'] in figure_locations:
            resolved.append(dict(failure=failure,evidence=figure_locations[failure['path']]))
            continue
        remaining.append(failure)
    resolved_digits = {(x['failure']['file'],x['failure']['line'],x['failure']['column'],x['failure']['token']):x['evidence']
                       for x in resolved if x['failure']['category']=='UNBOUND_NUMERIC_OCCURRENCE'}
    for row in report['inventory']:
        key = (row['file'],row['line'],row['column'],row['token'])
        if row['category']=='unclassified' and key in resolved_digits:
            row.update(category='v9_located_source_binding',evidence=resolved_digits[key])
    resolved_words = {(x['failure']['file'],x['failure']['line'],x['failure']['word'],x['failure']['context']):x
                      for x in resolved if x['failure']['category']=='UNBOUND_NUMBER_WORD'}
    for row in report['number_words']:
        key = (row['file'],row['line'],row['word'],row.get('context'))
        if key in resolved_words:
            match = resolved_words[key]
            text = texts[row['file']]
            a = match['location'][1]
            row.update(column=a-(text.rfind('\n',0,a)+1)+1,category='v9_located_number_word',evidence=match['evidence'])
    for row in report.get('figure_paths',[]):
        if row['path'] in figure_locations:
            row.update(copy_identity_verified=True,expected_receipt_sha256=figure_locations[row['path']]['sha256'],
                       v9_identity_evidence=figure_locations[row['path']],values_verified_here=False)
    failures = remaining+extra
    report.update(schema='v9-additive-current-main-number-audit-1',checked_utc=datetime.now(timezone.utc).isoformat(),
                  status='FAIL' if failures else 'PASS',failures=failures,mismatches=len(failures),
                  legacy_failures=old_failures,legacy_status=legacy_report['status'],
                  v9_verified_contexts=verified,v9_resolved_failures=resolved,
                  v9_resolved_numeric_occurrences=len(resolved_digits),v9_resolved_number_words=len(resolved_words),
                  v9_verified_figure_identities=list(figure_locations.values()),
                  unclassified_numeric_occurrences=sum(x['category']=='unclassified' for x in report['inventory']),
                  unbound_number_word_occurrences=sum(x['category']=='UNBOUND_NUMBER_WORD' for x in failures),
                  category_counts=dict(Counter(x['category'] for x in report['inventory'])),
                  figure_values_verified_here=False,reference_metadata_verified_here=False,
                  full_artifact_numeric_acceptance=False,new_financial_computations=0,models_refitted=0,
                  new_hypothesis_tests=0,private_arrays_read=False)
    return report


def audit_documents(main_path,letter_path,*,root=ROOT,bindings_path=None):
    root = Path(root).resolve()
    legacy_path = root/LEGACY_PATH
    if sha(legacy_path.read_bytes()) != LEGACY_SHA256:
        raise ValueError('frozen v8 checker bytes changed; do not weaken or silently replace it')
    spec = importlib.util.spec_from_file_location('unchanged_v8_numeric_guard',legacy_path)
    legacy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(legacy)
    result = legacy.audit_documents(main_path,letter_path,root=root)
    bindings_path = Path(bindings_path) if bindings_path is not None else root/DEFAULT_BINDINGS
    bindings = json.loads(bindings_path.read_text())
    result = resolve_additions(result,{'main':Path(main_path).read_text(),'cover_letter':Path(letter_path).read_text()},bindings,root=root)
    result.update(legacy_checker_path=LEGACY_PATH,legacy_checker_sha256=LEGACY_SHA256,
                  v9_bindings_sha256=sha(bindings_path.read_bytes()))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--main-path',type=Path,default=ROOT/MAIN)
    parser.add_argument('--letter-path',type=Path,default=ROOT/LETTER)
    parser.add_argument('--bindings-path',type=Path,default=ROOT/DEFAULT_BINDINGS)
    args = parser.parse_args(argv)
    output = args.output.absolute()
    output.relative_to((ROOT/'notes/revision-v9').absolute())
    if not output.name.startswith(('wp5-main-','wp7-main-')):
        raise ValueError('new v9 wp5-main-/wp7-main- output prefix required')
    result = audit_documents(args.main_path,args.letter_path,bindings_path=args.bindings_path)
    with output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inventory','number_words','source_hashes','legacy_failures','v9_verified_contexts','v9_resolved_failures')},indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
