"""End-to-end software check: fixed invented coefficients, no financial input."""
import json
import pytest


def test_fixed_no_break_fixture_reuses_original_forecast_engine(tmp_path):
    import run_v9_nonstationarity as driver
    d=driver.read_design()
    # An implementation fixture, not a study run or a fitted parameter vector.
    p=dict(intercept=.05,phi=.4,omega=.1,alpha=.05,beta=.8,nu=8.)
    cal=dict(source_id='ARTIFICIAL_SOFTWARE_FIXTURE',source_index=99,M=404,
             calibration_status='COMPLETE',whole_fit={'params':p},
             segment_fits=[{'params':p}],partition={'segment_lengths':[404],'cuts':[]})
    r=driver.simulate_unit(cal,0,1,99,d,tmp_path)
    assert r['complete']
    assert len(r['records'])==8
    for w in d['windows']:
        f=json.loads((tmp_path/'constant'/f'W{w}_H6_F.json').read_text())
        assert f['status']=='COMPLETE' and f['evaluation']['n']==72
        for method in ('QR33','QR4'):
            a=next(v for v in r['records'] if v['arm']=='constant' and v['window']==w and v['method']==method)
            b=next(v for v in r['records'] if v['arm']=='switching' and v['window']==w and v['method']==method)
            assert {k:v for k,v in a.items() if k!='arm'}=={k:v for k,v in b.items() if k!='arm'}
    # Every synthetic stream/phase receipt must survive before any forecast.
    assert list(tmp_path.glob('*geometry*.json')) or list(tmp_path.glob('**/geometry.json'))
