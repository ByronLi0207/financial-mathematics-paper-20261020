"""Toy tests for the fixed v13 G2 geometry and complete-denominator screens."""
from copy import deepcopy
import pytest


def test_geometry_retains_original_short_and_completed_long_boundaries():
    from v13_validation import validation_geometry
    assert validation_geometry(6,52)==(329,380)
    assert validation_geometry(24,52)==(329,380)
    assert validation_geometry(6,156)==(243,398)
    assert validation_geometry(24,156)==(225,380)
    assert validation_geometry(6,156)[1]+6==404
    assert validation_geometry(24,156)[1]+24==404
    with pytest.raises(ValueError):validation_geometry(12,156)


def test_full_grid_has_exactly52_geometries_with_mature_feature_history():
    from v13_validation import g2_cells
    sources=[dict(family='bill' if i==0 else 'panel',key=f's{i}',short_scale=6,
                  long_scale=26,nominal_gap_seconds=604800,N=706) for i in range(13)]
    cells=g2_cells(sources)
    assert len(cells)==52
    assert len({c['cell_id'] for c in cells})==52
    assert {c['window'] for c in cells}=={52}
    assert {c['evaluation_n'] for c in cells}=={277}
    assert min(c['validation_first']-c['horizon']-c['window']+1 for c in cells)==150
    assert all(c['validation_last']+c['horizon']<c['evaluation_first'] for c in cells)
    with pytest.raises(ValueError):g2_cells(sources[:-1])


def toy_rows():
    from v13_validation import NYFED_KEYS
    rows=[]
    for method in ('QR33','QR4'):
        for h in (6,24):
            for v in (52,156):
                for i,key in enumerate(NYFED_KEYS):
                    rows.append(dict(method=method,horizon=h,window=52,validation_n=v,
                        source_key=key,status='COMPLETE',relative_loss_pct=10. if v==52 else 3.,
                        actual_loss=11. if v==52 else 10.3,reference_loss=10.,
                        selected_penalty='inf' if v==156 else .1))
    return rows


def test_five_point_and_infinity_rules_require_both_fixed13_horizons():
    from v13_validation import summarize_g2
    got=summarize_g2(toy_rows())
    assert got['V3']=='SUPPORTED' and got['V4']=='SUPPORTED'
    assert got['methods']['QR33']['by_horizon']['6']['median_difference_pct_points']==-7
    assert got['methods']['QR33']['by_horizon']['24']['infinity_count_by_validation']=={'52':0,'156':13}


def test_missing_or_failed_pair_does_not_promote_successful_subset():
    from v13_validation import summarize_g2
    rows=toy_rows(); rows[13]['status']='FAILED';rows[13]['relative_loss_pct']=None
    got=summarize_g2(rows)
    h=got['methods']['QR33']['by_horizon']['6']
    assert h['complete_pair_count']==12
    assert h['median_difference_pct_points'] is None
    assert h['V3']=='UNDETERMINED' and h['V4']=='UNDETERMINED'
    assert got['V3']=='UNDETERMINED'
    assert h['descriptive_complete_pairs']['median_difference_pct_points']==-7


def test_complete_counterexample_beats_unknown_other_horizon():
    from v13_validation import summarize_g2
    rows=toy_rows()
    for row in rows:
        if row['method']=='QR33' and row['horizon']==24 and row['validation_n']==156:
            row['relative_loss_pct']=8.
    rows[13]['status']='FAILED'
    got=summarize_g2(rows)
    assert got['V3']=='NOT_SUPPORTED'


def test_duplicate_cannot_replace_fixed_source_slot():
    from v13_validation import summarize_g2
    rows=toy_rows();rows.append(deepcopy(rows[0]))
    got=summarize_g2(rows)
    assert got['methods']['QR33']['by_horizon']['6']['complete_pair_count']==12
    assert got['V3']=='UNDETERMINED'


def test_old_failed_cache_is_read_only_and_not_retried(tmp_path):
    import json
    import numpy as np
    from v12_forecast import make_context
    from v12_runner import _identity
    from v13_validation_runner import attempt_cached
    series=dict(position=np.arange(160,dtype=float),times=np.arange('2020-01-01','2023-01-25',7,dtype='datetime64[D]'))
    series['times']=np.arange(160).astype('timedelta64[D]')*7+np.datetime64('2020-01-01')
    cell=dict(horizon=6,window=52,refit_step=13,short_scale=6,long_scale=26,nominal_gap_seconds=604800)
    context=make_context(series,cell);ids=np.arange(100,110,dtype=np.int64)
    source=dict(sha256='toy',bytes=1)
    identity,key,_,_=_identity(context,source,ids,'QR33',.001,.95)
    old=tmp_path/'old';folder=old/key;folder.mkdir(parents=True)
    terminal=folder/'terminal.json';terminal.write_text(json.dumps(dict(identity=identity,status='FAILED',reason='NONCONVERGENCE')))
    before=terminal.read_bytes();stamp=terminal.stat().st_mtime_ns
    got=attempt_cached(context,source,ids,'QR33',.001,.95,tmp_path/'new',old,lambda **_:None)
    assert got['status']=='FAILED' and got['reason']=='NONCONVERGENCE'
    assert got['cache_source']=='v12'
    assert terminal.read_bytes()==before and terminal.stat().st_mtime_ns==stamp
    assert not (tmp_path/'new').exists()


def test_resource_failure_cannot_be_reported_as_completed_mean(tmp_path):
    import numpy as np
    from v13_validation_runner import attempt_cached
    from v12_forecast import make_context
    from v12_runner import ResourceStop
    x=np.arange(160,dtype=float);t=np.arange(160).astype('timedelta64[D]')+np.datetime64('2020-01-01')
    context=make_context(dict(position=x,times=t),dict(horizon=6,window=52,refit_step=13,short_scale=6,long_scale=26,nominal_gap_seconds=86400))
    def stopped(**_):raise ResourceStop('RESOURCE_DEADLINE')
    got=attempt_cached(context,dict(sha256='toy',bytes=1),np.arange(100,110),'F',None,.95,tmp_path/'new',tmp_path/'old',stopped)
    assert got['status']=='NOT_RUN_RESOURCE_LIMIT'
    assert 'summary' not in got


def test_whole_method_failure_retains_all_six_and_never_selects_success_subset(tmp_path):
    import hashlib,json
    import numpy as np
    from v12_forecast import make_context
    from v12_inputs import load_series
    from v12_runner import _identity
    from v13_validation_runner import compute_method
    csv=tmp_path/'toy.csv'
    dates=np.datetime64('2020-01-01')+np.arange(160)*np.timedelta64(7,'D')
    csv.write_text('As Of Date,Time Series,Value (millions)\n'+'\n'.join(f'{d},toy,{10+np.sin(i/7)}' for i,d in enumerate(dates))+'\n')
    source=dict(family='bill',key='toy',path=str(csv),sha256=hashlib.sha256(csv.read_bytes()).hexdigest(),bytes=csv.stat().st_size,N=160,unit='toy units')
    cell=dict(experiment='G2',cell_id='toy',family='bill',source_key='toy',period='original',horizon=6,window=52,refit_step=13,short_scale=6,long_scale=26,nominal_gap_seconds=604800,tau=.95,validation_first=100,validation_last=105,validation_n=6,evaluation_first=120,evaluation_last=129,evaluation_n=10,source=source)
    context=make_context(load_series(source),cell);ids=np.arange(100,106,dtype=np.int64)
    identity,key,_,_=_identity(context,source,ids,'QR33',.001,.95)
    old=tmp_path/'old';folder=old/key;folder.mkdir(parents=True)
    (folder/'terminal.json').write_text(json.dumps(dict(identity=identity,status='FAILED',reason='PREVIOUS_NONCONVERGENCE')))
    got=compute_method(cell,'QR33',tmp_path/'new',old,tmp_path/'private',None)
    assert got['row']['status']=='FAILED'
    assert got['row']['reason']=='PREVIOUS_NONCONVERGENCE'
    assert got['row']['selected_penalty'] is None
    assert len(got['candidates'])==6
    assert [c['penalty'] for c in got['candidates']]==[.001,.01,.1,1.,10.,'inf']
    assert got['selection']['status']=='FAILED'
    assert not any(c['segment']=='evaluation' for c in got['candidates'])
    assert not (tmp_path/'new'/key).exists()
