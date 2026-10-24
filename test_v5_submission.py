from copy import deepcopy
import v5_submission as v5
from v4_numeric import validate_block

def test_gain_uses_same_denominator_and_keeps_original_primary():
 b=v5.generated('gain_table');assert len(b['rows'])==3
 assert b['rows'][0][2]=='+2.4716' and b['rows'][1][2]=='−15.1317'
 assert b['rows'][2][2]=='−12.6601'
 assert validate_block(b)==[]

def test_generated_context_swap_is_rejected():
 b=deepcopy(v5.generated('gain_table'));b['rows'][0][2]=b['rows'][1][2]
 assert validate_block(b)

def test_maturity_table_preserves_both_directions():
 b=v5.generated('leakage_table');assert len(b['rows'])==6
 assert b['rows'][0][4].startswith('+0.0639') and b['rows'][3][4].startswith('−33.3988')
 assert validate_block(b)==[]

def test_abstract_is_deterministic_and_source_regenerated():
 b=v5.generated('abstract');assert '50.79%' in b['html'] and '3/48' in b['html']
 assert validate_block(b)==[]
