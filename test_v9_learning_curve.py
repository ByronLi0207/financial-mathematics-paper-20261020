"""Constructed curve/HAC/equality contracts; no financial file is loaded."""
import importlib,math
import numpy as np
import pytest

@pytest.fixture
def api():
 try:return importlib.import_module('v9_learning_curve')
 except ModuleNotFoundError as e:
  if e.name!='v9_learning_curve':raise
  pytest.fail('learning-curve implementation is absent',pytrace=False)

W=[360,720,1440,2880,5760]
def test_crossing_is_raw_W_and_closed_interval(api):
 x=api.classify_curve(W,[2.,-2.,-3.,-1.,-2.],540.,600.)
 assert x['first_crossing']==540. and x['prediction_status']=='FIRST_CUTPOINT_CONSISTENT'
 assert api.classify_curve(W,[2.,-2.,-3.,-1.,-2.],541.,600.)['prediction_status']=='FIRST_CUTPOINT_INCONSISTENT'

def test_discriminating_interval_is_required(api):
 assert api.classify_curve(W,[2.,-2.,-3.,-1.,-2.],0.,600.)['prediction_status']=='NOT_TESTABLE_NONDISCRIMINATING_INTERVAL'
 assert api.classify_curve(W,[2.,-2.,-3.,-1.,-2.],1.,None)['prediction_status']=='NOT_TESTABLE_NONDISCRIMINATING_INTERVAL'

def test_never_bridge_NA_or_ignore_possible_earlier_root(api):
 x=api.classify_curve(W,[2.,None,-2.,2.,-2.],4000.,5000.)
 assert x['first_crossing'] is None and x['prediction_status']=='NOT_TESTABLE_NA_PREFIX'
 assert x['conditional_crossings']==[4320.]

def test_tail_NA_after_identified_root_does_not_remove_it(api):
 x=api.classify_curve(W,[2.,-2.,-3.,-1.,None],500.,600.)
 assert x['first_crossing']==540. and x['prediction_status']=='FIRST_CUTPOINT_CONSISTENT'

def test_left_censoring_is_compatible_not_point_confirmation(api):
 x=api.classify_curve(W,[-1.,-2.,-3.,-1.,-2.],100.,700.)
 assert x['first_crossing'] is None and x['prediction_status']=='NOT_TESTABLE_COMPATIBLE_LEFT_CENSORED'
 assert api.classify_curve(W,[-1.,-2.,-3.,-1.,-2.],400.,700.)['prediction_status']=='INCONSISTENT_LEFT_CENSORED'

def test_absent_crossing_only_rejects_covered_prediction_range(api):
 assert api.classify_curve(W,[2.,3.,2.,1.,None],700.,2700.)['prediction_status']=='INCONSISTENT_NO_CROSSING'
 assert api.classify_curve(W,[2.,3.,2.,1.,None],100.,2700.)['prediction_status']=='NOT_TESTABLE_NO_CROSSING'

def test_zero_touch_and_multiple_roots_remain_explicit(api):
 x=api.classify_curve(W,[2.,0.,2.,-2.,1.],700.,800.)
 assert x['first_crossing']==720. and x['conditional_crossings']==[720.,2160.]
 assert x['first_right_endpoint_strictly_negative'] is False
 assert x['multiple_crossings'] is True

def test_original_HAC_known_answer_and_direction(api):
 out=api.dm_hac_only(np.array([1.,2.,3.,4.]),2)
 assert out['bandwidth']==2 and out['lrv']==pytest.approx(17/12)
 assert out['dm_t']==pytest.approx(2.5/math.sqrt((17/12)/4))
 assert out['dm_p']==pytest.approx(math.erfc(abs(out['dm_t'])/math.sqrt(2)))
 assert 'hln_t' not in out

def test_degenerate_DM_stays_NA(api):
 out=api.dm_hac_only(np.zeros(30),6)
 assert out['status']=='IDENTICAL_LOSSES' and out['dm_t'] is None and out['dm_p'] is None
 assert api.dm_hac_only(np.ones(30),6)['status']=='ZERO_LONG_RUN_VARIANCE'

def test_exact_baseline_gate_rejects_even_tiny_float_changes(api):
 old={'capacity':np.array([1.,2.]),'origins':np.array([10,11],dtype=np.int64)}
 new={k:v.copy() for k,v in old.items()};new['capacity'][1]+=1e-14
 with pytest.raises(api.BaselineMismatch):api.exact_arrays(new,old)
 assert api.exact_arrays(old,old)['arrays_checked']==2

def test_baseline_gate_binds_shape_dtype_and_missing_fields(api):
 old={'x':np.array([1.,2.])}
 for candidate in ({'x':np.array([1.,2.],dtype=np.float32)},{'x':np.array([[1.,2.]])},{}):
  with pytest.raises(api.BaselineMismatch):api.exact_arrays(candidate,old)

def test_exact_public_scalar_gate_does_not_use_loose_tolerance(api):
 with pytest.raises(api.BaselineMismatch):api.exact_tree({'loss':1.+1e-14},{'loss':1.})
 assert api.exact_tree({'count':5,'loss':1.},{'count':5,'loss':1.})>=2

def test_legacy_F_gate_checks_only_F_from_shared_reference_archive(tmp_path,monkeypatch):
 import run_v9_learning_curve as driver,json
 monkeypatch.setattr(driver,'ROOT',tmp_path)
 old=dict(result=dict(summary_rows=[dict(method='frozen_F',loss=2.),dict(method='rolling_S',loss=999.)],year_rows=[],nonoverlap_rows=[],fit_diagnostics=[],origin_identity={'count':2}))
 (tmp_path/'old.json').write_text(json.dumps(old))
 np.savez(tmp_path/'old.npz',frozen_F_capacity=np.array([1.,2.]),rolling_S_capacity=np.array([999.,999.]))
 d={'legacy_public':[{'horizon':6,'phase':'references','path':'old.json'}],'legacy_private':[{'horizon':6,'phase':'references','path':'old.npz'}]}
 block=dict(summary_rows=[dict(method='frozen_F',loss=2.)],year_rows=[],nonoverlap_rows=[],fit_diagnostics=[{'new_training_metadata':1}],origin_identity={'count':2})
 result=driver.exact_phase_gate(d,6,'references',block,{'frozen_F_capacity':np.array([1.,2.])},'F')
 assert result['arrays_checked']==1 and result['status']=='PASS'

def test_prospective_run_seal_detects_changed_old_input(tmp_path,monkeypatch):
 import run_v9_learning_curve as driver,hashlib
 monkeypatch.setattr(driver,'ROOT',tmp_path);p=tmp_path/'input.csv';p.write_text('fixed')
 manifest={'sealed_files':{'input.csv':hashlib.sha256(p.read_bytes()).hexdigest()}}
 driver.verify_seal(manifest);p.write_text('changed')
 with pytest.raises(ValueError,match='seal'):driver.verify_seal(manifest)

def test_candidate_and_selection_evidence_survives_later_gate_failure(tmp_path):
 import run_v9_learning_curve as driver,json
 public=tmp_path/'public'
 candidate=dict(parameter=.01,status='FAILED',failure={'code':'SOLVER'},mean_pinball=None)
 driver.record_candidate(public,'QR33',0,candidate,[{'refit_index':10,'status':'FAILED'}])
 driver.record_selection(public,'QR33',None,{'status':'INELIGIBLE'})
 try:raise RuntimeError('later exact gate failure')
 except RuntimeError:pass
 row=json.loads((public/'QR33-candidate-0.json').read_text())
 assert row['candidate']==candidate and row['fit_diagnostics'][0]['refit_index']==10
 assert json.loads((public/'QR33-selection.json').read_text())['selected_penalty'] is None
 with pytest.raises(FileExistsError):driver.record_candidate(public,'QR33',0,{},[])
