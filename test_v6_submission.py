"""Paper-facing integration checks against the retained v5 document snapshots."""
import importlib,importlib.util,json,re
from pathlib import Path
from copy import deepcopy

ROOT=Path(__file__).parent

def api():
    assert importlib.util.find_spec('v6_submission'),'v6 composition missing'
    return importlib.import_module('v6_submission')

def table(doc,label):
    return next(b for s in doc['sections'] for b in s['blocks'] if b['type']=='table' and re.match(r'Table '+str(label)+r'(?:†|\.)',b['caption']))

def test_original_empirical_main_rows_and_all_supplement_rows_remain_exact():
    m=api();d,s=m.compose(write_outputs=False)
    old=json.loads((ROOT/m.BASE).read_text());olds=json.loads((ROOT/m.SUPP).read_text())
    for before,after in [(3,3),(4,5),(5,4)]:
        a,b=table(old,before),table(d,after)
        assert (a['headers'],a['rows'])==(b['headers'],b['rows'])
    oldtables=[b for sec in olds['sections'] for b in sec['blocks'] if b['type']=='table']
    newtables=[b for sec in s['sections'][:len(olds['sections'])] for b in sec['blocks'] if b['type']=='table']
    assert len(oldtables)==len(newtables)
    assert [(b['headers'],b['rows']) for b in oldtables]==[(b['headers'],b['rows']) for b in newtables]

def test_physical_main_table_order_and_target_specific_curve_routing():
    d,s=api().compose(write_outputs=False)
    assert [int(re.match(r'Table (\d+)',b['caption'])[1]) for sec in d['sections'] for b in sec['blocks'] if b['type']=='table']==list(range(1,7))
    contribution=next(b['html'] for b in d['sections'][0]['blocks'] if b.get('html','').startswith('<b>Contribution on model evaluation'))
    assert 'Tables 3 and 5' in contribution
    assert 'Figure 3' in contribution and 'original' in contribution
    assert 'statistically favorable score comparison' not in contribution
    assert any(sec['title']=='S16. Additional benchmarks and robustness' for sec in s['sections'])

def test_main_extension_has_one_source_generated_empirical_number_and_honest_limits():
    d,s=api().compose(write_outputs=False)
    extra=next(b for sec in d['sections'] for b in sec['blocks'] if b.get('_v6_role')=='new_evidence_paragraph')
    from v4_numeric import content_numbers
    assert content_numbers(extra['html'])==['15.00']
    assert 'post-result / exploratory' in extra['html'] and 'guarantee' in extra['html']
    text=' '.join(b.get('html','') for sec in d['sections'] for b in sec['blocks'])
    assert 'Further alternatives include CAViaR, sequential conformal' not in text
    assert 'AI-use disclosure:' not in text
    assert 'Sussman, 2023' in text

def test_deterministic_context_regeneration_and_no_writes_in_read_only_composition():
    m=api();paths=list((ROOT/'submission-jof').glob('*-content.json'))
    before={p:p.read_bytes() for p in paths};d,s=m.compose(write_outputs=False)
    assert before=={p:p.read_bytes() for p in paths}
    for doc in (d,s):
        for sec in doc['sections']:
            for b in sec['blocks']:
                if b.get('_generator','').startswith('v6:'):
                    key=b['_generator'][3:];expected=m.generated(key)
                    from v4_numeric import fields
                    assert fields(b)==fields(expected)

def test_numbered_sections_do_not_repeat_the_same_first_subheading():
    d,_=api().compose(write_outputs=False)
    for sec in d['sections']:
        title=re.sub(r'^\d+\.\s*','',sec['title']).casefold()
        if sec['blocks'] and sec['blocks'][0]['type']=='subheading':
            assert sec['blocks'][0]['text'].casefold()!=title

def test_additional_method_locators_distinguish_section_s16_from_old_table_s16():
    d,_=api().compose(write_outputs=False)
    assert 'Supplement S16' in table(d,2)['caption']
    route=table(d,6)['rows'][0][1]
    assert 'Tables 3, 5 and S16' not in route
    assert 'Tables 3 and 5; Supplement S16' in route

def test_acronyms_and_selected_identity_have_explicit_meanings():
    d,s=api().compose(write_outputs=False)
    for doc in (d,s):
        text=json.dumps(doc,ensure_ascii=False)
        assert 'root-mean-square (RMS)' in text
        assert 'conformal inference (ACI)' in text
        assert 'absolute-value (SAV)' in text
    assert 'full-pool fallback' not in json.dumps(d)
