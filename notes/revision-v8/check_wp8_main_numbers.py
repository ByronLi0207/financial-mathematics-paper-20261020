"""Located current main/letter numeric audit; source lookups and display only.

Legacy evidence is inherited only through frozen exact contexts or a labelled
whole-table-row numeric sequence, never through equal-value global membership.
New context checks use WP7 saved source locators. No scientific engine is run.
References, figure values and PDF positioning have separate owning audits.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from datetime import datetime,timezone
from decimal import Decimal,InvalidOperation
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASELINE='b571f324a253480b4e39bc8a8096775ddbcc7017'
PRE_INTEGRATION='642d6af'
TOKEN=re.compile(r'[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?')
WORDS=re.compile(r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|hundred|thousand)\b',re.I)
MAIN='submission-jof/manuscript.tex'
LETTER='submission-jof/cover-letter.md'


def sha(data):return hashlib.sha256(data).hexdigest()

def pointer(value,path):
    if not path:return value
    for part in path.lstrip('/').split('/'):
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value


def identical(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,list):return len(a)==len(b) and all(identical(x,y) for x,y in zip(a,b))
    if isinstance(a,dict):return a.keys()==b.keys() and all(identical(a[k],b[k]) for k in a)
    return a==b


def numeric_equal(a,b):
    try:return Decimal(a)==Decimal(b)
    except InvalidOperation:return False


def lex(text,start=0):return [(start+m.start(),start+m.end(),m.group()) for m in TOKEN.finditer(text)]


def blocks(text):
    """Exact lines and sentences, preserving offsets; not token-only anchors."""
    result=[];offset=0
    for line in text.splitlines(keepends=True):
        stripped=line.strip();left=offset+len(line)-len(line.lstrip())
        if len(stripped)>=20:result.append((left,left+len(stripped),stripped,'line'))
        offset+=len(line)
    for paragraph in re.finditer(r'\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*',text):
        raw=paragraph.group();last=0
        for ending in re.finditer(r'[.!?](?=\s|$)',raw):
            part=raw[last:ending.end()];trimmed=part.strip();left=paragraph.start()+last+len(part)-len(part.lstrip())
            if len(trimmed)>=25:result.append((left,left+len(trimmed),trimmed,'sentence'))
            last=ending.end()
    return result


def table_blocks(text):
    rows=[]
    for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}',text,re.S):
        labels=re.findall(r'\\label\{(tab:[^}]+)\}',m.group())
        if len(labels)!=1:continue
        rows.append((labels[0],m.start(),m.end(),m.group()))
    return rows


def section_at(text,offset):
    found=list(re.finditer(r'\\label\{(sec:[^}]+)\}',text[:offset]))
    return found[-1].group(1) if found else 'preamble_or_abstract'


def actual_source(root,row,cache):
    name=row['source'];path=(root/name).resolve();path.relative_to(root.resolve())
    kind=row['format'];key=(name,kind)
    if key not in cache:
        raw=path.read_bytes()
        cache[key]=(json.loads(raw) if kind=='json' else list(csv.DictReader(raw.decode('utf-8-sig').splitlines())) if kind=='csv' else raw.decode('utf-8'))
    data=cache[key]
    if kind=='json':return pointer(data,row.get('pointer',''))
    if kind=='csv':
        matches=[r for r in data if all(r.get(k)==str(v) for k,v in row['where'].items())]
        if len(matches)!=1:raise ValueError('nonunique CSV source selector')
        return matches[0][row['field']]
    if row['value'] not in data:raise ValueError('exact old source passage absent')
    return row['value']


def audit_documents(main_path,letter_path,*,root=ROOT):
    root=Path(root).resolve();main=Path(main_path).read_text();letter=Path(letter_path).read_text()
    failures=[];annotations=defaultdict(list);word_annotations=defaultdict(list);cache={};source_hashes={}
    def fail(category,**detail):failures.append(dict(category=category,**detail))
    def mark(file,a,b,category,**evidence):annotations[file].append((a,b,dict(category=category,evidence=evidence)))
    def wordmark(file,a,b,category,**evidence):word_annotations[file].append((a,b,dict(category=category,evidence=evidence)))
    for artifact in ['notes/v7/s9-number-token-inventory.json','notes/v7/s9-number-check.json','notes/v7/main-v7-numeric-bindings.json']:
        frozen=subprocess.check_output(['git','show',BASELINE+':'+artifact],cwd=root)
        if (root/artifact).read_bytes()!=frozen:fail('HISTORICAL_PROOF_BYTES_CHANGED',path=artifact)
    old=subprocess.check_output(['git','show',BASELINE+':'+MAIN],cwd=root).decode()
    history=json.loads((root/'notes/v7/s9-number-token-inventory.json').read_text())
    historical_report=json.loads((root/'notes/v7/s9-number-check.json').read_text())
    if sha(old.encode())!=history['files'][MAIN]['sha256']:fail('HISTORICAL_CONTEXT_IDENTITY_MISMATCH')
    if historical_report['status']!='PASS' or historical_report['mismatches']!=0:fail('HISTORICAL_SOURCE_PROOF_NOT_PASS')
    old_records={};oldlines=old.splitlines(keepends=True);starts=[];total=0
    for line in oldlines:starts.append(total);total+=len(line)
    for r in history['tokens']:
        if r['file']!=MAIN:continue
        a=starts[r['line']-1]+r['column']-1;b=a+len(r['token'])
        if old[a:b]!=r['token']:fail('HISTORICAL_TOKEN_OFFSET_MISMATCH',line=r['line'])
        old_records[(a,b)]=r
    evidences={}
    for p in sorted((root/'notes/v7/evidence-parts').glob('*.json')):
        for r in json.loads(p.read_text()):
            if r['id'] in evidences:fail('DUPLICATE_OLD_EVIDENCE_ID',id=r['id'])
            evidences[r['id']]=r
    for r in evidences.values():
        try:
            actual=actual_source(root,r,cache)
            if not identical(actual,r['value']):fail('ORIGINAL_SOURCE_FIELD_MISMATCH',id=r['id'])
            digest=sha((root/r['source']).read_bytes());source_hashes[r['source']]=digest
            frozen=historical_report['source_hashes'].get(r['source'],{}).get('expected')
            if digest!=frozen:fail('ORIGINAL_SOURCE_HASH_MISMATCH',source=r['source'])
        except (OSError,ValueError,KeyError,TypeError) as exc:fail('ORIGINAL_SOURCE_READ_FAILURE',id=r['id'],error=type(exc).__name__)
    legacy_bindings=json.loads((root/'notes/v7/main-v7-numeric-bindings.json').read_text())
    for i,b in enumerate(legacy_bindings):
        if b['id'] not in evidences or not identical(evidences[b['id']]['value'],b['raw_value']):fail('ORIGINAL_MAIN_BINDING_VALUE_MISMATCH',binding=i)

    def inherit(a,b,oa,ob,method):
        part=main[a:b];prior=old[oa:ob]
        if part!=prior:return
        for left,right,_ in lex(part,a):
            oldkey=(oa+left-a,oa+right-a);record=old_records.get(oldkey)
            if record:
                mark('main',left,right,record['category'],method=method,historical_line=record['line'],historical_token=record['token'],historical_evidence=record.get('evidence'),baseline_commit=BASELINE)
        for m in WORDS.finditer(part):wordmark('main',a+m.start(),a+m.end(),'unchanged_reviewed_legacy_number_word',method=method,baseline_commit=BASELINE,exact_context=part)

    old_contexts=defaultdict(list);current_contexts=defaultdict(list)
    for a,b,s,kind in blocks(old):old_contexts[(kind,s)].append((a,b))
    for a,b,s,kind in blocks(main):current_contexts[(kind,s)].append((a,b))
    for key,current in current_contexts.items():
        prior=old_contexts.get(key,[])
        if len(prior)==1:
            for a,b in current:inherit(a,b,*prior[0],'exact_frozen_'+key[0])

    # Verify both directions: correct remaining rows do not justify deleting
    # an adverse original row. WP7 accepted the pre-integration WP2 typography;
    # all six labelled original table numeric vectors must remain complete.
    pre_integration=subprocess.check_output(['git','show',PRE_INTEGRATION+':'+MAIN],cwd=root).decode()
    original_table_vectors={label:[v for _,_,v in lex(body)] for label,_,_,body in table_blocks(pre_integration)}
    current_table_vectors={label:[v for _,_,v in lex(body)] for label,_,_,body in table_blocks(main)}
    if (set(original_table_vectors)!=set(current_table_vectors)
            or len(table_blocks(main))!=len(original_table_vectors)):
        fail('PRESERVED_TABLE_LABEL_SET_MISMATCH',expected=list(original_table_vectors),actual=[r[0] for r in table_blocks(main)])
    table_vector_mismatches=[]
    for label,expected in original_table_vectors.items():
        actual=current_table_vectors.get(label)
        if actual!=expected:
            table_vector_mismatches.append(label)
            fail('PRESERVED_TABLE_NUMERIC_VECTOR_MISMATCH',table=label,expected_tokens=expected,actual_tokens=actual)

    # Whole labelled rows: padding-equivalent decimals are allowed, but paired
    # order, reference label and all other row text must remain the same.
    table_rows_checked=table_tokens_checked=0
    old_tables={label:(offset,body) for label,offset,_,body in table_blocks(old)}
    for label,offset,_,body in table_blocks(main):
        if label not in old_tables:continue
        oldoffset,oldbody=old_tables[label];lookup=defaultdict(list)
        for m in re.finditer(r'[^\n]+',oldbody):
            line=m.group()
            if '&' in line and line.rstrip().endswith(r'\\'):
                skeleton=re.sub(r'\s+',' ',TOKEN.sub('#',line.strip()))
                lookup[skeleton].append((oldoffset+m.start(),line))
        for m in re.finditer(r'[^\n]+',body):
            line=m.group()
            if '&' not in line or not line.rstrip().endswith(r'\\') or not TOKEN.search(line):continue
            key=re.sub(r'\s+',' ',TOKEN.sub('#',line.strip()));candidates=lookup.get(key,[])
            if len(candidates)!=1:continue
            oa,prior=candidates[0];current=lex(line,offset+m.start());before=lex(prior,oa)
            if len(current)!=len(before) or any(not numeric_equal(a[2],b[2]) for a,b in zip(current,before)):
                fail('TABLE_NUMERIC_SEQUENCE_MISMATCH',table=label,current_tokens=[x[2] for x in current],expected_tokens=[x[2] for x in before])
                continue
            table_rows_checked+=1;table_tokens_checked+=len(current)
            for (a,b,value),(x,y,priorvalue) in zip(current,before):
                record=old_records.get((x,y))
                if record:mark('main',a,b,record['category'],method='labelled_whole_row_ordered_sequence',table=label,baseline_commit=BASELINE,original_display=priorvalue,decimal_equivalent_display=value!=priorvalue,historical_evidence=record.get('evidence'))
            for w in WORDS.finditer(line):wordmark('main',offset+m.start()+w.start(),offset+m.start()+w.end(),'unchanged_labelled_row_number_word',table=label,baseline_commit=BASELINE)

    # Accepted old maths must be exactly preserved; adding a new inline p-value
    # never enters this list just because it is wrapped in maths.
    patterns=(r'\\\[.*?\\\]',r'\\\(.*?\\\)',r'(?<!\\)\$[^$]*?\$')
    old_math=defaultdict(list);preserved_math_fragments=0
    for pattern in patterns:
        for m in re.finditer(pattern,old,re.S):old_math[(section_at(old,m.start()),m.group())].append(m.span())
    for pattern in patterns:
        for m in re.finditer(pattern,main,re.S):
            matches=old_math.get((section_at(main,m.start()),m.group()),[])
            if len(matches)==1:
                inherit(m.start(),m.end(),*matches[0],'exact_frozen_math_fragment_in_same_section');preserved_math_fragments+=1
    old_displays=re.findall(r'\\\[.*?\\\]',old,re.S);current_displays=re.findall(r'\\\[.*?\\\]',main,re.S)
    if old_displays!=current_displays:fail('PRESERVED_MATH_MISMATCH',scope='ordered original display equations')

    # Current percentages: exact sentence anchors and original native fields.
    rounding=json.loads((root/'notes/revision-v8/wp7-rounding-check.json').read_text())
    def sentence(anchor,expected,category,details,*,percent_only=False):
        found=[m.start() for m in re.finditer(re.escape(anchor),main)]
        if len(found)!=1:
            fail('AMBIGUOUS_CONTEXT' if len(found)>1 else 'MISSING_CONTEXT',anchor=anchor,hits=len(found));return
        start=found[0];ending=re.search(r'[.!?](?=\s|\\end\{abstract\}|$)',main[start:])
        end=start+ending.end() if ending else len(main)
        actual=lex(main[start:end],start)
        # Citation and structural labels in a context are excluded only by
        # their explicit command role, not by numeric value.
        ignored=[]
        for m in re.finditer(r'\\(?:cite\w*|label|ref)\{[^}]*\}',main[start:end]):ignored.append((start+m.start(),start+m.end()))
        actual=[r for r in actual if not any(a<=r[0] and r[1]<=b for a,b in ignored)]
        if percent_only:
            actual=[r for r in actual if main[r[1]:].startswith(('%',r'\%'))]
        if [v for _,_,v in actual]!=expected:
            fail(category,anchor=anchor,actual=[v for _,_,v in actual],expected=expected)
            return
        for (a,b,value),detail in zip(actual,details):mark('main',a,b,'current_located_source_binding',anchor=anchor,**detail)
    percent_count=0
    for record in rounding['records']:
        if 'old_field_ids' in record:
            fields=[evidences[k] for k in record['old_field_ids']]
            raw=[actual_source(root,r,cache) for r in fields]
            details=[dict(source=r['source'],id=r['id'],native_value=v,display_operation='absolute one-decimal percentage from original native field') for r,v in zip(fields,raw)]
        else:
            fields=record['source_bindings'];raw=[];details=[]
            for r in fields:
                actual=pointer(json.loads((root/r['source']).read_text()),r['pointer'])
                if not identical(actual,r['raw_value']) or sha((root/r['source']).read_bytes())!=r['source_sha256']:fail('NEW_SOURCE_BINDING_MISMATCH',source=r['source'],pointer=r['pointer'])
                raw.append(actual);details.append(dict(source=r['source'],pointer=r['pointer'],native_value=actual,display_operation='absolute one-decimal percentage from native field'))
        expected=[format(abs(float(v)),'.1f') for v in raw]
        sentence(record['anchor'],expected,'PERCENTAGE_DISPLAY_MISMATCH',details,percent_only=True);percent_count+=len(expected)

    # This revised percentage sentence also carries an original paired count.
    # Bind the count to its own exact source field, never to a global equal value.
    bill_ids=['PANEL_BILL_QR_H6_W260_LOSS_PERCENT','PANEL_BILL_QR_H6_W260_QR_HITS']
    bill_raw=[actual_source(root,evidences[k],cache) for k in bill_ids]
    sentence('Its loss increase is',[format(float(bill_raw[0]),'.1f'),str(bill_raw[1])],
        'LEGACY_CONTEXT_VALUE_MISMATCH',[dict(id=k,source=evidences[k]['source'],native_value=v,
        display_operation='one-decimal percentage' if i==0 else 'exact original paired breach count')
        for i,(k,v) in enumerate(zip(bill_ids,bill_raw))])

    integration=json.loads((root/'notes/revision-v8/wp7-main-integration.json').read_text());new=integration['new_reader_numeric_bindings']
    def newvalue(index):
        row=new[index];source=root/row['source'];data=json.loads(source.read_text());source_hashes[row['source']]=sha(source.read_bytes())
        if source_hashes[row['source']]!=row['source_sha256']:fail('NEW_SOURCE_HASH_MISMATCH',source=row['source'])
        if row.get('derivation')=='last-first+1':
            keys=row['pointer'].split(',');value=[pointer(data,k) for k in keys];display=str(value[1]-value[0]+1)
        elif row.get('derivation')=='sum both frozen regression counts':
            value={method:{k: data['classifications'][method][k] for k in ('historical_wins','planned_comparisons')} for method in ('QR33','QR4')}
            display=f"{sum(r['historical_wins'] for r in value.values())} / {sum(r['planned_comparisons'] for r in value.values())}"
        else:
            value=pointer(data,row['pointer']);shown=abs(value) if row.get('absolute_display') else value
            display=format(shown,row['format']) if row.get('format') else str(shown)
        if not identical(value,row['raw_value']) or display!=row['display']:fail('NEW_SOURCE_BINDING_MISMATCH',index=index)
        return display,dict(source=row['source'],pointer=row['pointer'],native_value=value,display_operation=row.get('derivation') or row.get('format') or 'exact native integer')
    values=[newvalue(i) for i in range(len(new))]
    contexts=[('Daily aggregation of the same dealer produces',[0,1]),('Each regression shows clear gains in only',[2,3]),('Both also show clear gains in',[4,5]),('The experiment uses',[6,7]),('Historical headroom wins',[8]),('It records 37 breaches versus',[10,11]),('Matched breaches are',[14,15]),('The raw rolling-reference DM p-value is about',[16])]
    for anchor,ids in contexts:
        expected=[];details=[]
        for i in ids:
            display,detail=values[i]
            for _,_,token in lex(display):expected.append(token);details.append(detail)
        sentence(anchor,expected,'NEW_CONTEXT_VALUE_MISMATCH',details)
    support=json.loads((root/'results/revision-v8/wp3/support.json').read_text())['procedures']
    for field in ('target_clear_gain_count','target_cell_count','outside_clear_gain_count','outside_cell_count'):
        if support['QR33'][field]!=support['QR4'][field]:fail('BOTH_REGRESSIONS_CLAIM_MISMATCH',field=field)

    # Explicit role spans: bibliography/citation/URL/labels/layout are delegated
    # metadata or display roles. No whole-line/math catch-all is used.
    texts={'main':main,'cover_letter':letter}
    for name,text in texts.items():
        bib=text.find(r'\begin{thebibliography}')
        if bib>=0:
            for a,b,_ in lex(text[bib:],bib):mark(name,a,b,'reference_metadata',verified_here=False,owning_gate='WP8 reference audit')
        for pattern,role in [(r'\\(?:cite\w*|label|ref)\{[^}]*\}','reference_or_crossref_identifier'),(r'\\(?:url|href)\{[^}]*\}','source_URL_identifier'),(r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}','figure_path_or_display_parameter'),(r'\\textbf\{C[123]\.\}','contribution_counter')]:
            for m in re.finditer(pattern,text):
                for a,b,_ in lex(m.group(),m.start()):mark(name,a,b,role,verified_here=False if 'reference' in role else True)
        # Existing exact contexts above cover the accepted preamble. New lengths
        # are recognised only inside their explicit TeX option/length arguments.
        for m in re.finditer(r'\\(?:documentclass|usepackage)\[[^\]]*\]|\\setlength\{[^}]+\}\{[^}]*\}|\\(?:clubpenalty|widowpenalty)=\d+',text):
            for a,b,_ in lex(m.group(),m.start()):mark(name,a,b,'layout_parameter',scope='TeX layout, not a measured result')

    # New meaningful number words are bound by complete phrases and metadata;
    # unchanged reviewed contexts are inherited above. Newly invented numeric
    # prose does not acquire this classification by equal word membership.
    for phase,name in [('wp3','wp3-mechanism-design.json'),('wp4','wp4-daily-fx-design.json'),('wp5','wp5-fixed-prefix-design.json')]:
        relative='protocol/revision-v8/'+name;digest=sha((root/relative).read_bytes())
        manifest=json.loads((root/f'results/revision-v8/{phase}/manifest.json').read_text())
        if manifest['protocol_hashes'].get(relative)!=digest:fail('NEW_DESIGN_HASH_MISMATCH',source=relative)
        source_hashes[relative]=digest
    wp3=json.loads((root/'protocol/revision-v8/wp3-mechanism-design.json').read_text())
    wp5=json.loads((root/'protocol/revision-v8/wp5-fixed-prefix-design.json').read_text())
    patterns=[(r'three windows with previously examined outcomes',len(wp5['three_window_summary']['windows']),3,'WP5 three_window_summary/windows'),(r'three design-frozen exploratory extensions',len([x for x in ('wp3-mechanism-design.json','wp4-daily-fx-design.json','wp5-fixed-prefix-design.json') if (root/'protocol/revision-v8'/x).is_file()]),3,'three actual frozen protocol files'),(r'nineteen-to-one', (wp3['tau_numerator'],wp3['tau_denominator']-wp3['tau_numerator']),(19,1),'tau numerator/(denominator-numerator)'),(r'four-predictor',len(json.loads((root/'protocol/revision-v8/wp4-daily-fx-design.json').read_text())['features']['qr4_column_indices']),4,'WP4 features/qr4_column_indices'),(r'five-point penalty menu',len(wp3['menus']['QR4']),5,'WP3 menus/QR4'),(r'one four-predictor gain',json.loads((root/'results/revision-v8/wp4/summary.json').read_text())['classifications']['QR4']['conditional_wins'],1,'WP4 QR4 conditional_wins')]
    study_spec=json.loads((root/'protocol/revision-20261022/study-spec.json').read_text())
    fx_source_count=sum(name=='fx_hourly' for name in study_spec['sources'])
    wrapper=json.loads((root/'results/revision-20261023/v6/wp2-findings.json').read_text())
    wrapped=[r for r in wrapper['wrapped_pairs'] if (r['source'],r['horizon'],r['window'])==('fx_hourly',6,2880)]
    if len(wrapped)!=1:fail('NONUNIQUE_WRAPPER_NUMBER_WORD_CONTEXT')
    paired_methods=0 if not wrapped else sum(k in wrapped[0] for k in ('qr_hits','f_hits'))
    total_weekly_tasks=int(evidences['PANEL_ORIGINAL_SERIES_COUNT']['value'])+int(bool(evidences['META_BILL_SERIES_KEY']['value']))
    patterns += [(r'one FX record and thirteen weekly position-category aggregates',(fx_source_count,total_weekly_tasks),(1,13),'Original study singleFX source; addedpanel series_count plus original bill series'),
        (r'one market maker',fx_source_count,1,'Original study sources/fx_hourly identity'),
        (r'two observed breach frequencies',paired_methods,2,'Original wrapped H6/W2880 qr_hits and f_hits'),
        (r'two implemented procedures',paired_methods,2,'Original wrapped H6/W2880 qr_hits and f_hits')]
    # Four predictor count uses its actual frozen column-list source rather
    # than a coincidental number elsewhere.
    wp4design=json.loads((root/'protocol/revision-v8/wp4-daily-fx-design.json').read_text())
    patterns=[(p,len(wp4design['features']['qr4_column_indices']) if p=='four-predictor' else value,want,source) for p,value,want,source in patterns]
    for pattern,value,wanted,source in patterns:
        if value!=wanted:fail('NUMBER_WORD_SOURCE_MISMATCH',phrase=pattern,source=source)
        for m in re.finditer(pattern,main,re.I):
            for w in WORDS.finditer(m.group()):wordmark('main',m.start()+w.start(),m.start()+w.end(),'located_number_word',source=source,native_value=value)

    # Final exhaustive digit census; unknown result values remain explicit.
    inventory=[];unclassified=[]
    for name,text in texts.items():
        for a,b,token in lex(text):
            candidates=[r for x,y,r in annotations[name] if x<=a and b<=y]
            # A source binding takes priority over structural/metadata roles.
            candidates.sort(key=lambda r: (r['category'] not in ('current_located_source_binding','existing_binding'),r['category']=='mathematical_definition_or_structure'))
            if not candidates:
                item=dict(file=name,line=text.count('\n',0,a)+1,column=a-(text.rfind('\n',0,a)+1)+1,token=token,category='unclassified',context=text[max(0,a-100):min(len(text),b+120)])
                unclassified.append(item);fail('UNBOUND_NUMERIC_OCCURRENCE',**{k:v for k,v in item.items() if k!='category'})
            else:item=dict(file=name,line=text.count('\n',0,a)+1,column=a-(text.rfind('\n',0,a)+1)+1,token=token,**candidates[0])
            inventory.append(item)
    words=[];unbound_words=[]
    for name,text in texts.items():
        text=text.split(r'\begin{thebibliography}',1)[0]
        for w in WORDS.finditer(text):
            candidates=[r for x,y,r in word_annotations[name] if x<=w.start() and w.end()<=y]
            candidates.sort(key=lambda r:r['category']!='located_number_word')
            if not candidates:
                item=dict(file=name,line=text.count('\n',0,w.start())+1,word=w.group(),context=text[max(0,w.start()-70):min(len(text),w.end()+120)])
                unbound_words.append(item);fail('UNBOUND_NUMBER_WORD',**item)
            else:item=dict(file=name,line=text.count('\n',0,w.start())+1,word=w.group(),**candidates[0])
            words.append(item)

    figures=[];style=json.loads((root/'notes/revision-v8/wp2-figure-styling.json').read_text())
    known={r['path']:r['sha256'] for r in style['figures']}
    mcfig=json.loads((root/'results/revision-v8/wp3/figures/display-receipt.json').read_text())
    for r in mcfig['figures']:known['submission-jof/figures/'+r['pdf']]=r['pdf_sha256']
    for m in re.finditer(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',main):
        relative='submission-jof/'+m.group(1);path=root/relative
        if not path.is_file():fail('MISSING_CURRENT_FIGURE',path=relative);continue
        digest=sha(path.read_bytes());expected=known.get(relative)
        if digest!=expected:fail('UNBOUND_OR_CHANGED_FIGURE_SOURCE',path=relative)
        figures.append(dict(path=relative,current_sha256=digest,expected_receipt_sha256=expected,copy_identity_verified=digest==expected,values_verified_here=False))
    status='FAIL' if failures else 'PASS'
    return dict(schema='v8-current-main-number-audit-1',status=status,checked_utc=datetime.now(timezone.utc).isoformat(),scope='Current main and cover-letter located numeric occurrence/word audit; source lookup/display preservation only. Figure values, reference metadata and PDF positioning have separate owning gates.',current_main_sha256=sha(main.encode()),current_cover_letter_sha256=sha(letter.encode()),original_evidence_fields_checked=len(evidences),original_main_saved_bindings_checked=len(legacy_bindings),original_table_preservation_commit=PRE_INTEGRATION,original_table_vectors_checked=len(original_table_vectors),original_table_vector_mismatches=table_vector_mismatches,labelled_table_rows_checked=table_rows_checked,labelled_table_numeric_tokens_checked=table_tokens_checked,original_display_math_blocks_checked=len(old_displays),accepted_exact_math_fragments_checked=preserved_math_fragments,source_hashes=source_hashes,total_numeric_occurrences=len(inventory),main_numeric_occurrences=sum(x['file']=='main' for x in inventory),cover_letter_numeric_occurrences=sum(x['file']=='cover_letter' for x in inventory),category_counts=dict(Counter(x['category'] for x in inventory)),unclassified_numeric_occurrences=len(unclassified),ambiguous_numeric_locations=sum(x['category']=='AMBIGUOUS_CONTEXT' for x in failures),meaningful_number_word_occurrences=len(words),unbound_number_word_occurrences=len(unbound_words),old_and_new_percentage_fields_checked=percent_count,failures=failures,mismatches=len(failures),inventory=inventory,number_words=words,figure_paths=figures,figure_values_verified_here=False,reference_metadata_verified_here=False,reference_metadata_occurrences=sum(x['category'] in ('reference_metadata','reference_or_crossref_identifier','reference_or_source_identifier') for x in inventory),full_artifact_numeric_acceptance=False,required_separate_gates=['Actual included figure value/annotation audit','Current reference metadata audit','Current source-to-PDF identity and every-page visual QA','Supplement numeric audit'],new_financial_computations=0,models_refitted=0,new_hypothesis_tests=0,private_arrays_read=False)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--main-path',type=Path,default=ROOT/MAIN);parser.add_argument('--letter-path',type=Path,default=ROOT/LETTER)
    args=parser.parse_args(argv);out=args.output.absolute();out.relative_to((ROOT/'notes/revision-v8').absolute())
    if not out.name.startswith('wp8-main-'):raise ValueError('new v8 main output prefix required')
    result=audit_documents(args.main_path,args.letter_path)
    with out.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inventory','number_words','source_hashes')},indent=2))
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
