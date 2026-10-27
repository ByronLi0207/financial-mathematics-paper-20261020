"""Constructed-scalar/date tests only: no source I/O, DGP or model fits."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import struct

import numpy as np
import pytest


def api():
    return importlib.import_module('v8_daily_fx')


def design():
    return json.loads((Path(__file__).parent/'protocol/revision-v8/wp4-daily-fx-design.json').read_text())


def fixture():
    # Mutation caught: using the first record, filling weekend days, or retaining
    # original observation times as supposedly known final daily report times.
    return np.array([10.,12.,-4.,7.,9.]), np.array([
        '2020-01-03T10:00:00.000001','2020-01-03T22:00:00.000002',
        '2020-01-06T09:00:00.000003','2020-01-06T16:00:00.000004',
        '2020-01-07T08:00:00.000005'],dtype='datetime64[us]')


def test_last_observation_is_reported_at_completed_day_end_without_fill():
    x,t=fixture(); d=api().resample_closed_days(x,t)
    np.testing.assert_array_equal(d.position,[12.,7.,9.])
    np.testing.assert_array_equal(d.selected_indices,[1,3,4])
    np.testing.assert_array_equal(d.selected_raw_times,t[[1,3,4]])
    np.testing.assert_array_equal(d.times,np.array([
        '2020-01-03T23:59:59.999999','2020-01-06T23:59:59.999999',
        '2020-01-07T23:59:59.999999'],dtype='datetime64[us]'))
    assert d.times.dtype==np.dtype('datetime64[us]')
    assert d.metadata['n_original']==5 and d.metadata['n_daily']==3
    assert d.metadata['n_discarded_original']==2
    assert d.metadata['daily_gap_seconds_histogram']=={'86400':1,'259200':1}


def test_selected_arrays_are_readonly_copies_and_inputs_unchanged():
    x,t=fixture(); beforex=x.copy();beforet=t.copy()
    d=api().resample_closed_days(x,t)
    np.testing.assert_array_equal(x,beforex)
    np.testing.assert_array_equal(t,beforet)
    for a in (d.position,d.times,d.selected_indices,d.selected_raw_times):
        assert not a.flags.writeable
        with pytest.raises(ValueError):a[0]=a[-1]
    x[1]=999.;t[1]=np.datetime64('2020-01-03T21:00:00')
    assert d.position[0]==12. and str(d.selected_raw_times[0])=='2020-01-03T22:00:00.000002'
    np.testing.assert_array_equal(beforex,[10.,12.,-4.,7.,9.])
    np.testing.assert_array_equal(beforet,fixture()[1])


def test_fingerprints_use_canonical_little_endian_vectors_and_nul_prefix():
    x=np.array([4.,-3.],dtype='>f8')
    # Hand-chosen integer microseconds relative to epoch: day0 at 00:00:01,
    # day1 at 00:00:02; day-end microseconds are literal independent oracles.
    t=np.array([1_000_000,86_402_000_000],dtype='<i8').view('datetime64[us]')
    d=api().resample_closed_days(x,t)
    vectors=[struct.pack('<2q',0,1),struct.pack('<2q',1_000_000,86_402_000_000),
        struct.pack('<2q',86_399_999_999,172_799_999_999),struct.pack('<2d',4.,-3.)]
    expected=dict(zip(('selected_indices_sha256','selected_raw_times_sha256',
        'issue_times_sha256','position_sha256'),[hashlib.sha256(b).hexdigest() for b in vectors]))
    expected['combined_sha256']=hashlib.sha256(b'v8-daily-v1\x00'+b''.join(vectors)).hexdigest()
    assert d.metadata['fingerprints']==expected


def test_metadata_contains_aggregate_fields_without_raw_vectors():
    x,t=fixture();m=api().resample_closed_days(x,t).metadata
    assert set(m)=={'schema','n_original','n_daily','n_discarded_original',
        'source_first_timestamp','source_last_timestamp','first_issue_time',
        'last_issue_time','daily_gap_seconds_histogram','fingerprints'}
    assert m['source_first_timestamp']=='2020-01-03T10:00:00.000001'
    assert m['last_issue_time']=='2020-01-07T23:59:59.999999'
    json.dumps(m,allow_nan=False)


def test_appending_later_days_cannot_change_completed_day_proxies():
    x,t=fixture();before=api().resample_closed_days(x[:4],t[:4])
    after=api().resample_closed_days(x,t)
    np.testing.assert_array_equal(before.position,after.position[:2])
    np.testing.assert_array_equal(before.times,after.times[:2])


def test_partial_first_and_last_days_are_retained_under_same_rule():
    d=api().resample_closed_days(np.array([11.]),np.array(['2020-01-04T12:01'],dtype='datetime64[m]'))
    assert d.position.tolist()==[11.] and d.selected_indices.tolist()==[0]
    assert str(d.times[0])=='2020-01-04T23:59:59.999999'
    assert d.metadata['daily_gap_seconds_histogram']=={}


@pytest.mark.parametrize('kind',['empty','nonfinite','shape','nat','duplicate','decreasing','not_datetime'])
def test_invalid_source_order_and_values_are_rejected_without_sort_drop_or_impute(kind):
    x,t=fixture()
    if kind=='empty':x=x[:0];t=t[:0]
    elif kind=='nonfinite':x[1]=np.nan
    elif kind=='shape':x=x[:-1]
    elif kind=='nat':t[1]=np.datetime64('NaT')
    elif kind=='duplicate':t[1]=t[0]
    elif kind=='decreasing':t=t[::-1]
    elif kind=='not_datetime':t=np.arange(5)
    with pytest.raises(ValueError):api().resample_closed_days(x,t)


@pytest.mark.parametrize('h,w,first',[(6,52,272),(24,52,254),(6,260,64),(24,260,46)])
def test_original_ordinal_geometry_has_common_tail_and_mature_training(h,w,first):
    g=api().daily_issue_geometry(780,h,w,design())
    assert g==dict(status='READY',reason=None,validation_first=329,validation_last=380,
        validation_count=52,evaluation_first=405,evaluation_last=755,
        evaluation_count=351,earliest_training_origin=first,feature_valid_from=26)
    assert 380+24<405 and first+h+w-1==329


def test_one_complete_evaluation_origin_is_admitted_without_fabricated_padding():
    g=api().daily_issue_geometry(430,24,260,design())
    assert g['status']=='READY' and g['evaluation_first']==g['evaluation_last']==405
    assert g['evaluation_count']==1


def test_empty_common_evaluation_is_na_without_moving_cutoff():
    g=api().daily_issue_geometry(429,6,52,design())
    assert g['status']=='NA_SAMPLE_SIZE' and g['reason']=='EMPTY_EVALUATION_GRID'
    assert g['evaluation_first']==405 and g['evaluation_last']==404 and g['evaluation_count']==0


def test_unavailable_validation_labels_are_na_before_any_score_can_exist():
    g=api().daily_issue_geometry(404,24,260,design())
    assert g['status']=='NA_SAMPLE_SIZE' and g['reason']=='VALIDATION_NOT_FULLY_OBSERVED'
    assert g['validation_first']==329 and g['validation_last']==380


def test_inadequate_feature_history_is_na_without_shortening_window():
    s=design();s['sample']['validation_first']=300
    g=api().daily_issue_geometry(780,24,260,s)
    assert g['status']=='NA_SAMPLE_SIZE' and g['reason']=='INSUFFICIENT_FEATURE_HISTORY'
    assert g['earliest_training_origin']==17 and g['feature_valid_from']==26


@pytest.mark.parametrize('n,h,w',[(True,6,52),(-1,6,52),(780,5,52),(780,6,53)])
def test_invalid_geometry_options_are_rejected(n,h,w):
    with pytest.raises(ValueError):api().daily_issue_geometry(n,h,w,design())


def rows(losses=(2.,2.,2.,.5),method='QR33'):
    output=[]
    for (w,h),loss in zip(((52,6),(52,24),(260,6),(260,24)),losses):
        for m,v in [('F',1.),('QR33',loss if method=='QR33' else 2.),('QR4',loss if method=='QR4' else 2.)]:
            output.append(dict(window=w,horizon=h,method=m,status='COMPLETE',
                evaluation=dict(mean_loss=v,n=100,strict_breach_count=5,strict_breach_rate=.05)))
    return output


def test_historical_majority_and_literal_daily_counterexample_both_remain_visible():
    r=api().classify_against_f(rows(),'QR33',design())
    assert r['status']=='TREASURY_LIKE'
    assert (r['historical_wins'],r['conditional_wins'],r['ties'],r['missing_comparisons'])==(3,1,0,0)
    assert r['planned_comparisons']==r['complete_comparisons']==4
    assert len(r['literal_hourly_counterexamples'])==1
    assert r['literal_hourly_counterexamples'][0]['window']==260
    assert len(r['comparisons'])==4 and r['descriptive_only'] is True


def test_three_conditional_wins_classifies_persistent_gains():
    r=api().classify_against_f(rows((.5,.5,.5,2.),'QR4'),'QR4',design())
    assert r['status']=='CONDITIONAL_GAINS_PERSIST' and r['conditional_wins']==3


def test_ties_are_neither_win_and_mixed_grid_is_not_forced_into_dominance():
    r=api().classify_against_f(rows((.5,2.,1.,1.)),'QR33',design())
    assert r['status']=='MIXED' and r['ties']==2
    assert r['historical_wins']==r['conditional_wins']==1


def test_another_regressions_failure_does_not_contaminate_this_one():
    data=rows()
    for r in data:
        if r['method']=='QR4':r.update(status='FAILED',evaluation=None)
    assert api().classify_against_f(data,'QR33',design())['status']=='TREASURY_LIKE'
    assert api().classify_against_f(data,'QR4',design())['status']=='INCONCLUSIVE'


@pytest.mark.parametrize('missing',['row','reference','failed','sample_na'])
def test_missing_comparison_keeps_four_planned_denominator_and_is_inconclusive(missing):
    data=rows((.5,.5,.5,.5))
    target=next(r for r in data if r['window']==52 and r['horizon']==6 and r['method']=='QR33')
    if missing=='row':data.remove(target)
    elif missing=='reference':data.remove(next(r for r in data if r['window']==52 and r['horizon']==6 and r['method']=='F'))
    else:target.update(status='FAILED' if missing=='failed' else 'NA_SAMPLE_SIZE',evaluation=None)
    result=api().classify_against_f(data,'QR33',design())
    assert result['status']=='INCONCLUSIVE' and result['missing_comparisons']==1
    assert result['complete_comparisons']==3 and result['planned_comparisons']==4
    assert result['conditional_wins']==3 and len(result['literal_hourly_counterexamples'])==3
    assert sum(r['outcome']=='UNAVAILABLE' for r in result['comparisons'])==1


def test_zero_reference_loss_preserves_absolute_comparison_and_exact_tie():
    data=rows((.5,.5,.5,.5))
    for r in data:
        if r['method']=='F':r['evaluation']['mean_loss']=0.
        if r['window']==260 and r['horizon']==24 and r['method']=='QR33':r['evaluation']['mean_loss']=0.
    result=api().classify_against_f(data,'QR33',design())
    assert result['status']=='TREASURY_LIKE' and result['historical_wins']==3 and result['ties']==1


@pytest.mark.parametrize('bad',['duplicate','unknown_method','unexpected_window','negative_loss','nan','mismatched_n','bad_breach'])
def test_malformed_identity_or_complete_score_is_rejected_instead_of_classified(bad):
    data=rows(); target=data[1]
    if bad=='duplicate':data.append(copy.deepcopy(target))
    elif bad=='unknown_method':target['method']='KNN'
    elif bad=='unexpected_window':target['window']=999
    elif bad=='negative_loss':target['evaluation']['mean_loss']=-1.
    elif bad=='nan':target['evaluation']['mean_loss']=float('nan')
    elif bad=='mismatched_n':
        target['evaluation']['n']=99
        target['evaluation']['strict_breach_rate']=5/99
    elif bad=='bad_breach':target['evaluation']['strict_breach_rate']=.25
    with pytest.raises(ValueError):api().classify_against_f(data,'QR33',design())
