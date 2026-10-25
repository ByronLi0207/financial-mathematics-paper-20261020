"""Independent stdlib-only Supplement/overflow source and saved-field audit.

No forecast, simulation, array, hypothesis test, compiler or PDF is run/read.
The legacy guard is imported unchanged only after its Git-byte identity holds.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
BASE='32ee58688bac260de322c31cb8945adbf3b53154'
WP5='d44364c6aa5ca5a9a043f33b9173f0864b771159'
WP6='2e6425881db1b25957d5d5da2f6e8168000a2caf'
SUPP='submission-jof/supplement.tex'
EXT='submission-jof/extended-v9-technical.tex'
TABLE='submission-jof/generated/v9-evidence-tables.tex'
GUARD='notes/revision-v8/check_wp8_supp_numbers.py'
MOVED=('Complete preference frontier: full sample','Complete preference frontier: sparse sensitivity','Numerical implementation and inference conventions')
NUMBER=re.compile(r'[+−-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+−-]?\d+)?')
WORDS=re.compile(r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|both|half|twice|doubled|first|second|third)\b',re.I)
URL='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/revision-v8-goal/'


def exact(actual,expected,context):
    if actual!=expected:raise ValueError(context+' differs')


def once(text,passage,context):
    if not passage or text.count(passage)!=1:raise ValueError(context+' is not unique')
    return text.index(passage)


def identical(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,list):return len(a)==len(b) and all(identical(x,y) for x,y in zip(a,b))
    if isinstance(a,dict):return a.keys()==b.keys() and all(identical(a[k],b[k]) for k in a)
    return a==b


def sha(data):return hashlib.sha256(data).hexdigest()
def read(root,name):return json.loads((root/name).read_text())
def blob(root,commit,name):return subprocess.check_output(['git','show',commit+':'+name],cwd=root)


def ptr(data,path):
    for part in path[1:].split('/') if path else []:
        part=part.replace('~1','/').replace('~0','~')
        data=data[int(part)] if isinstance(data,list) else data[part]
    return data


def mathtext(text):
    if 'e' in text.lower():
        mantissa,exponent=text.lower().split('e')
        text=mantissa+r'\times10^{'+str(int(exponent))+'}'
    return '$'+text+'$'


def render(style,values):
    """Independent closed display policy; source statistics are not recomputed."""
    value=values[0]
    if style=='integer':
        if type(value) is not int:raise ValueError('native integer required')
        plain=str(value)
    elif style=='fraction':
        if len(values)!=2 or any(type(x) is not int for x in values):raise ValueError('two integer counts required')
        plain=f'{values[0]}/{values[1]}'
    elif style in ('percent','loss','sig3','sig4','pvalue'):
        if value is None:return 'NA','NA'
        if style=='percent':plain=f'{value*100:.1f}'
        elif style=='loss':plain=f'{value:+.1f}'
        elif style=='sig3':plain=f'{value:.3g}'
        elif style=='sig4':plain=f'{value:.4g}'
        elif value==0:return '0 (floating-point)',r'$0^{u}$'
        else:plain=f'{value:.2e}' if value<.001 else f'{value:.3g}'
    elif style=='interval4':
        lo,hi=values
        left='0' if lo==0 else f'{lo:.4g}'
        right='unbounded' if hi is None else f'{hi:.4g}'
        return f'[{left}, {right}]','$['+left+', '+(r'\infty' if hi is None else right)+']$'
    elif style=='root':
        if value is None:
            plain='Left-censored' if values[1] else 'Unidentified'
            return plain,plain
        plain=f'{value:.4g}'
    elif style=='status':
        plain={'SUPPORT':'Met','NOT_SUPPORT':'Not met','INCONCLUSIVE':'Inconclusive'}[value]
        return plain,plain
    elif style=='curve_status':
        labels={'FIRST_CUTPOINT_CONSISTENT':'Consistent','FIRST_CUTPOINT_INCONSISTENT':'Inconsistent',
            'NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED':'Compatible, left-censored','INCONSISTENT_LEFT_CENSORED':'Inconsistent, left-censored',
            'NOT_TESTABLE_NA_PREFIX':'Untestable, missing prefix','INCONSISTENT_NO_CROSSING':'Inconsistent, no crossing',
            'NOT_TESTABLE_NO_CROSSING':'Untestable, no crossing','NOT_TESTABLE_NONDISCRIMINATING_INTERVAL':'Untestable interval'}
        plain=labels[value]
        return plain,r'\shortstack[l]{'+plain.replace(', ',r',\\')+'}'
    elif style in ('false_count','identified_count','consistent_count'):
        # Count already-saved classifications only; no forecast/decision is rerun.
        if style=='false_count':count=sum(x['outcome'] is False for x in value)
        elif style=='identified_count':count=sum(x['first_crossing'] is not None for x in value)
        else:count=sum(x['prediction_status']=='FIRST_CUTPOINT_CONSISTENT' for x in value)
        plain=str(count)
    else:raise ValueError('unsupported display policy '+style)
    return plain,mathtext(plain)


def check_rows(text,rows):
    actual=[]
    for line in text.splitlines():
        m=re.fullmatch(r'(.+?)\s*\\\\\s*% v9-row:(\S+)',line)
        if m:actual.append(dict(row_tag=m[2],tokens=[x.strip() for x in m[1].split('&')]))
    if actual!=rows:raise ValueError('ordered tagged rows differ, are missing, or are duplicated')
    return len(actual)


def check_digits(actual,expected,context):
    exact([m.group() for m in NUMBER.finditer(actual)],[m.group() for m in NUMBER.finditer(expected)],context+' ordered numeric tokens')


def sections(text):
    found=list(re.finditer(r'\\section\{([^}]+)\}',text));result={}
    for i,m in enumerate(found):
        end=found[i+1].start() if i+1<len(found) else text.index(r'\end{document}')
        if m[1] in result:raise ValueError('duplicate section '+m[1])
        result[m[1]]=text[m.start():end]
    return result


def relocation(root,*,compact_text=None,extended_text=None):
    before=blob(root,BASE,SUPP).decode()
    compact=(root/SUPP).read_text() if compact_text is None else compact_text
    extended=(root/EXT).read_text() if extended_text is None else extended_text
    proof=read(root,'notes/revision-v9/wp5-supplement-relocation.json')
    exact(sha(before.encode()),proof['before_source_sha256'],'relocation baseline hash')
    old=sections(before);current=sections(compact);moved=[old[name] for name in MOVED]
    receipts=[]
    for name,part,row in zip(MOVED,moved,proof['moved_sections']):
        exact(row['title'],name,'relocation section identity');exact(row['characters'],len(part),'relocation character count')
        exact(row['sha256'],sha(part.encode()),'relocation source fragment hash')
        once(extended,part,'relocated complete section '+name)
        receipts.append(dict(title=name,sha256=sha(part.encode()),characters=len(part),current_extended_occurrences=1))
    ext_sections=sections(extended)
    exact(list(ext_sections),list(MOVED),'extended section set and order')
    for name in MOVED:exact(ext_sections[name].rstrip(),old[name].rstrip(),'extended complete section '+name)
    exact(sha(extended.encode()),proof['extended_source_sha256'],'entire extended source identity')
    bridge=(r'\section{Complete preference frontiers: linked full inventories}\label{sup:frontier-0}\label{sup:frontier-8}'+'\n\n'+r'The unchanged full-sample and fixed-sparse frontiers, including every open region and boundary tie, appear in the \href{'+URL+r'submission-jof/extended-v9-technical.pdf}{complete linked technical PDF}. The identical editable sections and their original source-field tables are indexed in \href{'+URL+r'EXTENDED_RESULTS.md}{EXTENDED RESULTS}. This relocation keeps every favorable, adverse and tied region while making room for the complete new prediction assessments below.'+'\n\n')
    exact(current['Complete preference frontiers: linked full inventories'],bridge,'complete compact frontier bridge')
    prefix=old[MOVED[2]].split(r'\paragraph{Regression and local quantiles.}')[0]
    brief=prefix+'\nThe unchanged normalization, solver-eligibility, working-reference inference and common-pool details appear in the '+r'\href{'+URL+r'submission-jof/extended-v9-technical.pdf}{complete linked technical PDF}.'+' Their full source text is preserved verbatim, rather than replacing failed procedures or recalculating numerical results.\n\n'
    exact(current[MOVED[2]],brief,'complete compact numerical-convention prefix and bridge')
    added=current['History-coordinate discovery and pre-run prediction tests']
    restored=compact.replace(added,'',1).replace(bridge,moved[0]+moved[1],1).replace(brief,moved[2],1)
    restored=restored.replace('The complete linked frontiers include every open region and every boundary tie.','The complete frontiers below include every open region and every boundary tie.')
    title='When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits'
    restored=restored.replace('Online Supplement to '+title,'Online Supplement to Hard to Beat: Historical Rules versus Conditional Quantile Models for Peak Net-Position Limits')
    new='current manuscript and preserves the preceding controlled grid, same-dealer daily\naggregation and fixed-parameter full-prefix backcast. It also reports the post hoc\nhistory-coordinate discovery and the separately specified pre-run tests.'
    old_intro='v8 manuscript and adds the accepted frozen simulation, same-dealer daily\naggregation and fixed-parameter full-prefix backcast.'
    once(restored,new,'only approved non-scientific introduction replacement')
    restored=restored.replace(new,old_intro,1)
    exact(restored,before,'entire inverse-mapped old Supplement; no omitted fragments')
    return restored,added,dict(status='PASS',baseline_commit=BASE,baseline_sha256=sha(before.encode()),
        reconstructed_sha256=sha(restored.encode()),all_baseline_characters_accounted_for=len(before),
        old_numeric_occurrences=len(NUMBER.findall(before)),moved_sections=receipts,
        compact_old_remaining_and_relocated_content_complete=True,inverse_mapping_exact=True,
        approved_non_scientific_changes=['title','intro version/description','frontier below/linked adjective','two complete link bridges'],
        added_section_removed_only_for_legacy_view='History-coordinate discovery and pre-run prediction tests')


def fixture_contract(root,*,require_receipt=True):
    """Only a named ordinary test fixture may differ; all test bodies stay exact."""
    path='notes/revision-v8/test_v8_supp_numbers.py'
    original=blob(root,BASE,path).decode();current=(root/path).read_text()
    old_tree,new_tree=ast.parse(original),ast.parse(current)
    def methods(tree,text):
        cls=next(x for x in tree.body if isinstance(x,ast.ClassDef) and x.name=='SupplementNumericControls')
        return {x.name:ast.get_source_segment(text,x) for x in cls.body if isinstance(x,ast.FunctionDef) and x.name.startswith('test_')}
    old_methods,new_methods=methods(old_tree,original),methods(new_tree,current)
    exact(list(old_methods),list(new_methods),'original test method set/order')
    method_records=[]
    for name,source in old_methods.items():
        exact(new_methods[name],source,'unchanged original test method and assertions '+name)
        method_records.append(dict(name=name,sha256=sha(source.encode()),exact_source_identical=True))
    exact(len(method_records),8,'original eight test methods')
    def permitted_fixture_ast(tree):
        tree=ast.parse(ast.unparse(tree))
        tree.body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom)) and not (
            isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str))]
        for node in tree.body:
            if isinstance(node,ast.ClassDef) and node.name=='SupplementNumericControls':
                node.body=[n for n in node.body if not (isinstance(n,ast.FunctionDef) and n.name=='setUp')]
        return ast.dump(tree,include_attributes=False)
    exact(permitted_fixture_ast(old_tree),permitted_fixture_ast(new_tree),'only module docstring/imports and setUp may change')
    guard_current=(root/GUARD).read_bytes();exact(guard_current,blob(root,BASE,GUARD),'legacy guard remains unchanged')
    proof=dict(status='PASS',path=path,baseline_commit=BASE,old_test_sha256=sha(original.encode()),
        current_test_sha256=sha(current.encode()),test_methods=method_records,all_test_methods_and_assertions_byte_identical=True,
        other_AST_unchanged_after_only_authorized_fixture_docstring_imports=True,old_guard_unchanged=True,
        old_guard_sha256=sha(guard_current),scope='Ordinary version-aware fixture code only; no original test body/assertion, scientific archive, protocol, source field or guard modified')
    if require_receipt:
        receipt=read(root,'notes/revision-v9/wp7-supp-test-fixture-repair.json')
        exact(receipt['fixture_contract'],proof,'sealed fixture-repair contract')
    return proof


def preserve_archives(root):
    entries=subprocess.check_output(['git','ls-tree','--full-tree','-rz',BASE],cwd=root).split(b'\0')
    selected={}
    for entry in entries:
        if not entry:continue
        meta,name=entry.split(b'\t',1);name=name.decode()
        if name.startswith(('results/','protocol/','notes/v7/','notes/revision-v8/')):
            selected[name]=meta.decode().split()[2]
    missing=[name for name in selected if not (root/name).is_file()]
    if missing:raise ValueError('missing frozen public artifacts '+str(missing))
    if any('\n' in name for name in selected):raise ValueError('newline filename unsupported')
    names=sorted(selected)
    hashes=subprocess.check_output(['git','hash-object','--stdin-paths'],input=('\n'.join(names)+'\n').encode(),cwd=root).decode().splitlines()
    exact(len(hashes),len(names),'frozen artifact hash count')
    changes=[dict(path=name,expected_git_blob=selected[name],current_git_blob=value) for name,value in zip(names,hashes) if selected[name]!=value]
    allowed=[]
    for change in changes:
        if change['path']!='notes/revision-v8/test_v8_supp_numbers.py':
            raise ValueError('frozen scientific/proof artifacts changed '+str(change))
        allowed.append(dict(**change,fixture_contract=fixture_contract(root)))
    return dict(status='PASS',baseline_commit=BASE,existing_files_checked=len(names),mismatch_count=0,
        unchanged_files=len(names)-len(allowed),allowed_existing_code_differences=allowed,
        prefixes=['results/','protocol/','notes/v7/','notes/revision-v8/'],
        scope='Every existing tracked public file under the named prefixes at BASE; exactly the recorded ordinary fixture-code difference is permitted. All real result/protocol/proof bytes remain unchanged; new files separately audited, private/scratch excluded')


def protocol_constants(root,text):
    d1=read(root,'protocol/revision-v9/wp1-posthoc-design.json');d2=read(root,'protocol/revision-v9/wp2-confirmatory.json');d3=read(root,'protocol/revision-v9/wp3-learning-curve.json')
    specs=d2['DGP_spec'];s=specs['student_t5'];v=specs['regime_3to1'];j=specs['compound_poisson']
    for path,commit in [('protocol/revision-v9/wp1-posthoc-design.json','7f0fee8f1cfdeed584098bbc27570e88eafaea43'),('protocol/revision-v9/wp2-confirmatory.json','f2ce438ccb2fcf671c849a83032ac700ac6007c6'),('protocol/revision-v9/wp3-learning-curve.json','b26628fbc3950be0a3aaa1aa53b7f8de7dbb896a')]:
        exact((root/path).read_bytes(),blob(root,commit,path),'frozen protocol '+path)
    student=re.fullmatch(r'sqrt\((\d+)/(\d+)\)',s['scale'])
    if student is None or int(student[2])!=s['df'] or int(student[1])!=s['df']-2:raise ValueError('Student scale/df identity')
    def sigma(raw):
        m=re.fullmatch(r'(\d+)/sqrt\((\d+)\)',raw)
        if m is None:raise ValueError('unregistered sigma expression')
        return r'\frac{'+m[1]+r'}{\sqrt{'+m[2]+'}}'
    norm=re.fullmatch(r'1/sqrt\(([^)]+)\)',j['scale'])
    if norm is None:raise ValueError('unregistered jump scale')
    clock=d3['clock'];p1=d2['predictions']['P1'];p2=d2['predictions']['P2']
    exact(p1['region'],'metric<method_rstar/2','low region formula');exact(p2['region'],'metric>2*method_rstar','high region formula')
    specs_expected=[
        ('The post hoc discovery compares', ' '.join(d1['candidate_metrics'][k].replace('*','') for k in ('a','b','c'))+' '+d1['candidate_metrics']['c']),
        ('The new simulation uses',r'N_t=\phi N_{t-1}+\eta_t '+str(d2['phi'])+' '+str(d2['windows'])+' '+str(d2['horizons'])+' '+str(d2['repetitions'])+' '+str(d2['burn_in'])+' '+str(d2['retained_observations'])),
        (r'\item Student:',r'\sqrt{\frac{'+student[1]+'}{'+student[2]+'}} t_{'+str(s['df'])+'}'),
        (r'\item Volatility switching:',r'\sigma_0='+sigma(v['sigma_low'])+r' \sigma_1='+sigma(v['sigma_high'])+r' N(0,1) '+str(v['stay_probability'])+' '+str(v['initial_state_probability_high'])),
        (r'\item Symmetric jumps:',r'Z_t+'+str(j['jump_magnitude_in_Gaussian_SD'])+r'\sum_{j=1}^{K_t} U /\sqrt{'+norm[1]+r'} N(0,1) Poisson('+str(j['count_rate'])+') '+str(j['positive_sign_probability'])),
        ('The seed entropy is',str(d2['master_entropy'])+' P1 '+format(p1['minimum_fraction']*100,'.0f')+r' c<r/2 P2 '+format(p2['minimum_fraction']*100,'.0f')+r' c>2r P3 P1 P2 P3'),
        ('The FX study fixes validation origins',str(clock['validation_origin_first'])+'--'+str(clock['validation_origin_last'])+' '+str(clock['evaluation_origin_first'])+'--'+str(clock['evaluation_origin_last'])),
    ]
    checked=[];covered=[]
    paragraphs=[]
    for paragraph in text.split('\n\n'):
        if not paragraph.strip():continue
        # The itemize environment has one newline, not a blank line, between
        # its separately source-bound innovation definitions.
        if paragraph.startswith(r'\begin{itemize}'):
            paragraphs.extend(paragraph.splitlines())
        else:paragraphs.append(paragraph)
    for anchor,expected in specs_expected:
        hits=[p for p in paragraphs if p.startswith(anchor)]
        if len(hits)!=1:raise ValueError('new protocol paragraph not unique '+anchor)
        actual=hits[0];check_digits(actual,expected,anchor);covered.append(actual)
        checked.append(dict(anchor=anchor,numeric_tokens=[m.group() for m in NUMBER.finditer(actual)],
            source_protocols=['protocol/revision-v9/wp1-posthoc-design.json','protocol/revision-v9/wp2-confirmatory.json','protocol/revision-v9/wp3-learning-curve.json']))
    for p in paragraphs:
        if p in covered:continue
        # These two exact source/section identifiers carry document-version digits.
        if p in (r'\section{History-coordinate discovery and pre-run prediction tests}\label{sup:v9-history}',r'\input{generated/v9-evidence-tables.tex}'):
            continue
        # Only the argument of the two exact registered source links is a URL
        # identifier; an added result after either command remains unclassified.
        if p.startswith('Cutpoints interpolate the relative-loss curve'):
            links=re.findall(r'\\href\{([^}]+)\}',p)
            exact(links,[URL+'protocol/revision-v9/wp2-confirmatory.md',URL+'protocol/revision-v9/wp3-learning-curve.md'],'exact new-section protocol URLs')
            p=re.sub(r'\\href\{[^}]+\}',r'\\href{}',p)
        if NUMBER.search(p):raise ValueError('unclassified new-section numeric paragraph '+p[:150])
    # Whole current new section is unchanged from accepted WP5; paired with the
    # independent protocol-value checks, this also binds count-word contexts.
    exact(text,sections(blob(root,WP5,SUPP).decode())['History-coordinate discovery and pre-run prediction tests'],'accepted new-section full text and count-word contexts')
    return dict(status='PASS',numeric_paragraphs_checked=len(checked),ledger=checked,
        mathematical_constants=['AR lag index','two labelled volatility states','unit-normal mean/variance','sum lower index'],
        criterion_identifiers=['P1','P2','P3'],unclassified_scientific_numeric_paragraphs=0,
        count_word_contexts_exact_WP5=True,all_current_new_section_number_words=len(WORDS.findall(text)))


def check_native_binding(row,document):
    values=[ptr(document,p) for p in row['JSON_pointers']]
    if not identical(values,row['raw_values']):raise ValueError('typed source field mismatch '+row['id'])
    shown,token=render(row['format_style'],values)
    exact(shown,row['display'],'independent display '+row['id']);exact(token,row['tex_token'],'independent TeX display '+row['id'])
    return shown,token


def new_tables(root,*,tex_text=None):
    payload=read(root,'notes/revision-v9/wp6-new-number-bindings.json');old=read(root,'notes/revision-v9/wp5-new-number-bindings.json')
    exact((root/'notes/revision-v9/wp6-new-number-bindings.json').read_bytes(),blob(root,WP6,'notes/revision-v9/wp6-new-number-bindings.json'),'accepted WP6 binding bytes')
    exact((root/'notes/revision-v9/wp5-new-number-bindings.json').read_bytes(),blob(root,WP5,'notes/revision-v9/wp5-new-number-bindings.json'),'preserved WP5 binding bytes')
    for key in ('bindings','table_rows','namedfacts','namedfact_sources','sources','negative_result_preservation'):
        if not identical(payload[key],old[key]):raise ValueError('WP5 numeric binding object altered '+key)
    tex=(root/TABLE).read_text() if tex_text is None else tex_text
    exact(sha(tex.encode()),payload['generated_tex_sha256'],'current complete generated table hash')
    prior=blob(root,WP5,TABLE).decode()
    prior=prior.replace('Prospective simulation criteria, with every fixed denominator.','Pre-run simulation criteria, with every fixed denominator.')
    prior=prior.replace(r'F breaches & DM $p$',r'F breaches & \shortstack{Nominal\\DM $p$}')
    exact(tex,prior,'only two allowed WP6 presentation-label changes')
    docs={}
    for row in payload['sources'].values():
        raw=(root/row['path']).read_bytes();exact(len(raw),row['bytes'],'source byte count');exact(sha(raw),row['sha256'],'source full-file hash')
        docs[row['path']]=json.loads(raw)
    ids=set();located=0;records=[];rows_by_tag={r['row_tag']:r for r in payload['table_rows']}
    note_anchors={'P3 adverse cases':'The universal P3 prediction fails in ',
        'financial left censoring':'For the shorter-horizon four-predictor curve,',
        'financial evaluation count':'Each complete contrast uses the same '}
    for row in payload['bindings']:
        if row['id'] in ids:raise ValueError('duplicate v9 number binding')
        ids.add(row['id']);source=row['source_path'];exact(row['source_sha256'],sha((root/source).read_bytes()),'binding source hash')
        shown,token=check_native_binding(row,docs[source])
        loc=row['table_location']
        if loc is not None:
            if 'row_tag' in loc:exact(rows_by_tag[loc['row_tag']]['tokens'][loc['column']],token,'bound row/column '+row['id'])
            else:
                notes=[line for line in tex.splitlines() if note_anchors[loc['section']] in line]
                if len(notes)!=1 or notes[0].count(token)!=1:raise ValueError('exact note token not unique '+row['id'])
            located+=1
        records.append(dict(id=row['id'],source=source,pointers=row['JSON_pointers'],style=row['format_style'],display=shown,location=loc))
    count=check_rows(tex,payload['table_rows'])
    return dict(status='PASS',source_count=len(docs),native_binding_records_checked=len(records),
        explicitly_located_binding_records=located,main_only_namedfact_records=len(records)-located,
        complete_ordered_rows_checked=count,row_family_counts=dict(Counter(r['row_tag'].split(':')[0] for r in payload['table_rows'])),
        current_tex_sha256=sha(tex.encode()),current_bindings_sha256=sha((root/'notes/revision-v9/wp6-new-number-bindings.json').read_bytes()),
        WP5_numeric_bindings_and_rows_preserved=True,presentation_only_changes=['Pre-run title','Nominal DM label'],
        typed_field_display_location_ledger=records,unclassified_current_table_changes=0)


def audit(root=ROOT,*,view_root=None,legacy_receipt='AUTO'):
    root=Path(root).resolve();start=time.monotonic()
    restored,added,migration=relocation(root)
    archives=preserve_archives(root)
    guard_bytes=(root/GUARD).read_bytes();exact(guard_bytes,blob(root,BASE,GUARD),'unchanged legacy checker bytes')
    spec=importlib.util.spec_from_file_location('unchanged_supp_legacy',root/GUARD)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    attempt=1
    view=Path(view_root) if view_root is not None else root/'.scratch/revision-v9/wp7-supp-legacy-view'
    if view_root is None:
        while view.exists():
            attempt+=1
            view=root/f'.scratch/revision-v9/wp7-supp-legacy-view-{attempt}'
    (view/'submission-jof/generated').mkdir(parents=True,exist_ok=False)
    with (view/SUPP).open('x') as f:f.write(restored)
    for name in module.EXPECTED_INPUTS:
        with (view/name).open('xb') as f:f.write((root/name).read_bytes())
    legacy=module.audit(root,view)
    receipt=('notes/revision-v9/wp7-supp-legacy-number-audit'+('' if attempt==1 else f'-{attempt}')+'.json') if legacy_receipt=='AUTO' else legacy_receipt
    if receipt is not None:
        with (root/receipt).open('x') as f:json.dump(legacy,f,indent=2,ensure_ascii=False);f.write('\n')
    exact(legacy['status'],'PASS_WITH_SCOPE_LIMITS','strict unchanged legacy guard acceptance')
    exact(legacy['failures'],[],'legacy failures');exact(legacy['unresolved'],[],'legacy unresolved');exact(legacy['ambiguous'],[],'legacy ambiguity')
    constants=protocol_constants(root,added);tables=new_tables(root)
    return dict(status='PASS_WITH_SCOPE_LIMITS',generated_utc=datetime.now(timezone.utc).isoformat(),
        snapshot_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip(),
        actual_current_source_hashes={p:sha((root/p).read_bytes()) for p in (SUPP,EXT,TABLE)},
        relocation=migration,frozen_public_science_and_proof_files=archives,
        unchanged_legacy_guard=dict(path=GUARD,sha256=sha(guard_bytes),status=legacy['status'],counts=legacy['counts'],
            numeric_occurrences=legacy['numeric_occurrences'],number_word_occurrences=legacy['number_word_occurrences'],
            failures=0,unresolved=0,ambiguous=0,full_receipt=receipt,
            reconstruction_view=str(view.relative_to(root)) if view.is_relative_to(root) else str(view)),
        new_protocol_constants=constants,new_tables=tables,mismatch_count=0,differences=[],
        scope='Public saved source fields, exact relocation, source-level full-content preservation and current source-bound display only',
        holes=['PDF glyphs/row placement/page count and every-page visual inspection are not performed here.',
               'Included figure values/pixels and bibliography metadata have separate owning gates.',
               'The unchanged legacy census is on the exact inverse-mapped old layout; this is not a claim that the compact document retained the old physical locations.',
               'New-sequence count words are byte-bound to accepted WP5 text plus the explicit source-derived numeric/criteria checks; no new scientific count is inferred from prose.',
               'Private financial raw data and prediction vectors are not read; source consistency is not independent financial replication.'],
        elapsed_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        new_models=0,new_forecasts=0,new_statistics=0,private_arrays_read=False,PDFs_read=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'notes/revision-v9/wp7-supp-number-audit.json')
    args=parser.parse_args();out=args.output.resolve();out.relative_to(ROOT/'notes/revision-v9')
    if not out.name.startswith('wp7-supp-'):raise ValueError('assigned output prefix required')
    result=audit()
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:result[k] for k in ('status','generated_utc','snapshot_commit','actual_current_source_hashes','mismatch_count','elapsed_seconds','peak_rss_bytes','new_models','new_forecasts','new_statistics','private_arrays_read')},indent=2))
    print(json.dumps(dict(old_counts=result['unchanged_legacy_guard']['counts'],old_unresolved=0,new_bindings=result['new_tables']['native_binding_records_checked'],new_rows=result['new_tables']['complete_ordered_rows_checked'],existing_files_checked=result['frozen_public_science_and_proof_files']['existing_files_checked'],unchanged_files=result['frozen_public_science_and_proof_files']['unchanged_files'],allowed_fixture_code_differences=[x['path'] for x in result['frozen_public_science_and_proof_files']['allowed_existing_code_differences']],relocation_all_baseline_characters=result['relocation']['all_baseline_characters_accounted_for']),indent=2))


if __name__=='__main__':main()
