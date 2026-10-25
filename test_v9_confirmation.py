"""Small constructed-input contracts, not the formal v9 confirmation seed."""
import importlib
import math
import numpy as np
import pytest

@pytest.fixture
def api():
 try:return importlib.import_module('v9_confirmation')
 except ModuleNotFoundError as error:
  if error.name!='v9_confirmation':raise
  pytest.fail('v9 confirmation is not implemented',pytrace=False)

def test_student_normalization_and_level_recursion(api):
 innovations=api.student_innovations(np.array([1.,-2.,3.]))
 assert innovations==pytest.approx(np.array([1.,-2.,3.])*math.sqrt(3/5))
 assert api.level_path(np.array([1.,2.,-1.]),.5,0)==pytest.approx([1.,2.5,.25])

def test_regime_uses_current_state_then_transition(api):
 # Initial .25 => low; transitions .01 switch, .99 stay, .01 switch.
 eps,states=api.regime_innovations(np.ones(3),np.array([.25,.01,.99,.01]))
 assert states.tolist()==[0,1,1]
 assert eps==pytest.approx(np.array([1.,3.,3.])/math.sqrt(5))

def test_poisson_jumps_are_independent_per_event_signs(api):
 # Two opposite signs cancel, not +/- ten.
 out=api.jump_innovations(np.array([1.,1.,1.]),np.array([0,2,3]),np.array([0,1,3]))
 assert out==pytest.approx(np.array([1.,1.,16.])/math.sqrt(1.25))

def test_budget_review_halves_requested_windows_in_fixed_order(api):
 out=api.choose_reductions({52:10.,260:20.,720:30.,2880:40.},5.,90.)
 assert out['removed_windows']==[52,260]
 assert out['projected_seconds_after']==75.

def test_budget_review_never_looks_at_losses_or_drops_full_cells(api):
 out=api.choose_reductions({52:10.,260:20.,720:30.,2880:40.},5.,200.)
 assert out['removed_windows']==[] and out['projected_seconds_after']==105.

def test_screen_exact_boundaries_and_ties(api):
 p1=api.fraction_screen([True,True,True,True,False],.8)
 assert p1['status']=='SUPPORT' and p1['denominator']==5
 assert api.fraction_screen([True,True,False,False,False],.6)['status']=='NOT_SUPPORT'

def test_missing_primary_cannot_be_promoted_to_support(api):
 out=api.fraction_screen([True]*9+[None],.8)
 assert out['lower_bound']==.9 and out['status']=='INCONCLUSIVE'
 assert api.fraction_screen([False]*9+[None],.8)['status']=='NOT_SUPPORT'

def test_paired_aggregate_does_not_drop_failed_rep_or_replace_it(api):
 rows=[{'rep':0,'status':'COMPLETE','evaluation':{'mean_loss':2.,'strict_breach_rate':.1}}, {'rep':1,'status':'FAILED','evaluation':None}]
 reference=[{'rep':0,'status':'COMPLETE','evaluation':{'mean_loss':1.,'strict_breach_rate':.2}}, {'rep':1,'status':'COMPLETE','evaluation':{'mean_loss':1.,'strict_breach_rate':.2}}]
 out=api.aggregate_pair(rows,reference,2)
 assert out['full_procedure_status']=='NA' and out['failed_repetitions']==1
 assert out['relative_loss_percent']==100. and out['full_procedure_relative_loss_percent'] is None

def test_seed_stream_receipt_is_reproducible_and_distinct(api):
 design={'master_entropy':19,'burn_in':10,'retained_observations':25}
 x,a=api.make_process(0,2,.7,design);y,b=api.make_process(0,2,.9,design)
 z,c=api.make_process(1,2,.7,design)
 assert a['innovation_sha256']==b['innovation_sha256'] and a['innovation_sha256']!=c['innovation_sha256']
 assert a['position_sha256']!=b['position_sha256'] and len(x)==25

def test_seed_process_is_finite_without_fitting_any_forecast(api):
 for dgp in range(3):
  x,receipt=api.make_process(0,dgp,.7,{'master_entropy':19,'burn_in':10,'retained_observations':25})
  assert np.isfinite(x).all() and receipt['stream_key'][0]==0

def screen_fixture():
 import json
 from pathlib import Path
 d=json.loads((Path(__file__).parent/'protocol/revision-v9/wp2-confirmatory.json').read_text())
 rows=[]
 for dgp in d['dgp']:
  for pi in range(2):
   for w in d['windows']:
    for h in d['horizons']:
     for method in ['QR33','QR4']:
      delta=1. if w/(h+1)<d['thresholds'][method]['r_star']/2 else -1.
      rows.append(dict(dgp=dgp,phi_index=pi,window=w,horizon=h,method=method,full_procedure_relative_loss_percent=delta))
 return rows,d

def test_frozen_region_census_primary_and_secondary_are_distinct(api):
 rows,d=screen_fixture();out=api.confirmation_screen(rows,d)
 assert out['P1']['denominator']==48 and out['P2']['denominator']==24 and out['P3']['denominator']==48
 assert out['primary_status']=='SUPPORT' and out['P3']['status']=='SUPPORT'
 # Both rows at this WH lie outside P1/P2. One secondary failure stays visible.
 target=next(x for x in rows if x['dgp']==d['dgp'][0] and x['phi_index']==0 and x['window']==720 and x['horizon']==6 and x['method']=='QR33')
 target['full_procedure_relative_loss_percent']=-2.
 out=api.confirmation_screen(rows,d)
 assert out['primary_status']=='SUPPORT' and out['P3']['status']=='NOT_SUPPORT'
 assert out['P3']['successes']==47

def test_pooled_failure_is_not_hidden_by_passing_other_primary(api):
 rows,d=screen_fixture()
 for row in rows:row['full_procedure_relative_loss_percent']=1. if row['method']=='QR33' else -1.
 out=api.confirmation_screen(rows,d)
 assert out['P1']['status']=='NOT_SUPPORT' and out['P2']['status']=='SUPPORT'
 assert out['primary_status']=='NOT_SUPPORT' and out['by_method']['QR33']['P2']['status']=='NOT_SUPPORT'

def test_paired_failure_precedes_unattempted_other_method(api):
 model=[{'rep':0,'status':'NOT_ATTEMPTED','evaluation':None}]
 reference=[{'rep':0,'status':'FAILED','evaluation':None}]
 out=api.aggregate_pair(model,reference,1)
 assert out['failed_repetitions']==1 and out['unattempted_repetitions']==0
 assert out['full_procedure_status']=='NA'
