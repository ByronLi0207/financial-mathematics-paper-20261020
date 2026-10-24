from copy import deepcopy
from v4_submission import compose,joint_table
from v4_numeric import validate_block

def test_archive_block_accepts_unchanged_science():
 d,_=compose(write_outputs=False);b=next(b for s in d['sections'] for b in s['blocks'] if b.get('_source') and '14.767' in b.get('html',''))
 assert validate_block(b)==[]

def test_wrong_context_value_fails_even_when_it_exists_elsewhere():
 d,_=compose(write_outputs=False);b=deepcopy(next(b for s in d['sections'] for b in s['blocks'] if b.get('_source') and '14.767' in b.get('html','')))
 b['html']=b['html'].replace('14.767','12.660')
 assert validate_block(b)

def test_joint_table_regenerates_all_contextual_cells():
 b=joint_table();assert validate_block(b)==[]
 b['rows'][0][1]=b['rows'][1][1]
 assert validate_block(b)

def test_missing_provenance_is_not_silently_accepted():
 assert validate_block({'type':'p','html':'Observed loss increases 50.79%.'})

def test_definition_cannot_hide_empirical_numbers():
 assert validate_block({'type':'p','html':'Loss is 50.79%.','_definition':'Structural heading'})
