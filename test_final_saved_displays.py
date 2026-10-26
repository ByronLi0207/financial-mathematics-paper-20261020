"""Constructed contracts for the saved-display entry; no financial data or fits."""
import hashlib,json
from pathlib import Path
import pytest
import reproduce_final_displays as display

def test_json_operand_must_match_exact_saved_type_value_and_hash(tmp_path):
    p=tmp_path/'source.json';p.write_text('{"count":10}')
    r=dict(source='source.json',format='json',pointer='/count',value=10)
    value,digest=display.read_bound(r,tmp_path)
    assert value==10 and digest==hashlib.sha256(p.read_bytes()).hexdigest()
    with pytest.raises(ValueError,match='VALUE'):display.read_bound(dict(r,value=11),tmp_path)
    with pytest.raises(ValueError,match='HASH'):display.read_bound(dict(r,source_sha256='0'*64),tmp_path)

def test_csv_selector_cannot_accept_duplicate_or_missing_rows(tmp_path):
    p=tmp_path/'source.csv';p.write_text('id,loss\na,1.25\nb,2.5\n')
    r=dict(source='source.csv',format='csv',where={'id':'a'},field='loss',value='1.25')
    assert display.read_bound(r,tmp_path)[0]=='1.25'
    with pytest.raises(ValueError,match='SELECTOR'):display.read_bound(dict(r,where={'id':'z'}),tmp_path)
    p.write_text(p.read_text()+'a,1.25\n')
    with pytest.raises(ValueError,match='SELECTOR'):display.read_bound(r,tmp_path)

def test_unapproved_parent_path_is_rejected_before_read(tmp_path):
    with pytest.raises(ValueError,match='OUTSIDE'):display.read_bound(dict(source='../outside.json',format='json',pointer='',value=0),tmp_path)

def test_output_must_be_new_and_existing_bytes_survive(tmp_path):
    p=tmp_path/'existing';p.mkdir();f=p/'keep.txt';f.write_text('unchanged')
    with pytest.raises(FileExistsError):display.create_output(p)
    assert f.read_text()=='unchanged'

def test_saved_criterion_status_not_reclassified_from_rounded_fraction():
    tests={key:dict(successes=s,planned=n,status=status) for key,s,n,status in [
        ('P1_QR33',29,34,'SUPPORT'),('P1_QR4',15,17,'SUPPORT'),
        ('P2_QR4',10,17,'NOT_SUPPORT'),('P3_QR4',6,17,'NOT_SUPPORT')]}
    tests['P2_QR33']=dict(planned=0,status='NOT_TESTABLE')
    rows=display.cftc_rows({'tests':tests,'primary_verdict':'PARTLY'})
    assert any('$10/17$ & Not supported' in r for r in rows)
    assert any('NA & Not testable' in r for r in rows)
    assert len(rows)==5

def test_no_optimization_or_model_run_switch():
    with pytest.raises(SystemExit) as e:display.parser().parse_args(['--optimize'])
    assert e.value.code==2
