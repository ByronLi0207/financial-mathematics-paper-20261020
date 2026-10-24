"""Transport regression: immutable solver failure diagnostics remain public NA."""
import importlib,importlib.util,json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np
import pytest
from conditional_study import StudyConfig
from conditional_quantile import QuantileFitError

@pytest.mark.parametrize('phase',['validation','evaluation'])
def test_readonly_solver_diagnostics_serialize_without_changing_failure_rule(tmp_path,phase):
    assert importlib.util.find_spec('v6_tau_worker_v2'),'transport-only worker v2 missing'
    m=importlib.import_module('v6_tau_worker_v2')
    controls={'fx_hourly':'a'*64,'nyfed_weekly':'b'*64};execution='c'*64
    source=SimpleNamespace(position=np.sin(np.arange(1000))*.1+10,dates=np.arange(1000),sha256='e'*64)
    cfg={'validation_origin_first':800,'validation_origin_last':849,'evaluation_origin_first':860,'evaluation_origin_last':869}
    c=StudyConfig(6,720,24,24,168,3600)
    class Guard:
        def __call__(self,*a,**k):pass
        def summary(self):return {'peak_rss_bytes':1}
    validation=dict(status='COMPLETE',reason=None,source='fx_hourly',level='90',tau=.9,phase='validation',point95_controls=controls,
                    executable_freeze_sha256=execution,selection={'status':'SELECTED','parameter':.01})
    valpath=tmp_path/'validation-fx_hourly-tau90.json'
    if phase=='evaluation':
        valpath.write_text(json.dumps(validation))
        selection=dict(status='FROZEN_BEFORE_WP5_EVALUATION',point95_controls=controls,executable_freeze_sha256=execution,
            cells={'fx_hourly-tau90':dict(status='COMPLETE',reason=None,selected_parameter=.01,receipt_sha256=m.w.sha(valpath))})
        (tmp_path/'selection-freeze.json').write_text(json.dumps(selection))
    with patch.object(m,'OUT',tmp_path),patch.object(m,'PRIVATE',tmp_path/'private'),patch.object(m,'base',return_value=(source,cfg,c,.01)),patch.object(m,'require_controls',return_value=controls),patch.object(m,'check_freeze',return_value=execution),patch.object(m.w,'Guard',Guard),patch.object(m.signal,'signal'),patch.object(m.signal,'alarm'),patch('v6_tau.forecast_qr_tau',side_effect=QuantileFitError('NONCONVERGENCE',{'iterations':10000})):
        getattr(m,phase)('fx_hourly','90')
    receipt=json.loads((tmp_path/(phase+'-fx_hourly-tau90.json')).read_text())
    assert receipt['status']=='NA'
    if phase=='validation':
        assert len(receipt['candidates'])==3
        assert all(r['status']=='FAILED' and r['reason']=='NONCONVERGENCE' and r['diagnostics']=={'iterations':10000} for r in receipt['candidates'])
        assert receipt['selection']['status']=='INELIGIBLE'
    else:
        assert receipt['reason']=='NONCONVERGENCE' and receipt['diagnostics']=={'iterations':10000}
        assert 'scores' not in receipt and 'private_artifact' not in receipt
