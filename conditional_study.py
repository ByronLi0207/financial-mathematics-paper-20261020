"""Source-independent, chronologically fitted same-target comparisons.

No financial files are opened at import or by these helpers. Label caches may
contain future rows, but fitting explicitly slices completed labels at refit r;
each issued query uses current t. Future peaks enter only the separate scorer.
"""
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import math
import time
import numpy as np
import study_core as core
from conditional_features import (build_features, completed_training_indices,
    fit_feature_transform, transform_features, refit_origin, response_scale,
    neighbor_quantile)
from conditional_quantile import fit_quantile_ridge, QuantileFitError


FAMILIES=('QR','KNN','SCALED_KNN')


def _int(value,name,minimum=1):return core._integer(value,name,minimum)


def _ids(origins,size):
    ids=core._indices(origins,'issue origins')
    if np.any(ids>np.iinfo(np.int64).max):raise ValueError('issue index overflow')
    ids=ids.astype(np.int64,copy=False)
    if np.any(np.diff(ids)!=1) or ids[-1]>=size:raise ValueError('noncontiguous or out-of-range issue origins')
    return ids


@dataclass(frozen=True)
class StudyConfig:
    horizon:int
    window:int
    refit_step:int
    short_scale:int
    long_scale:int
    nominal_gap_seconds:int

    def __post_init__(self):
        for name in ('horizon','window','refit_step','short_scale','long_scale','nominal_gap_seconds'):
            object.__setattr__(self,name,_int(getattr(self,name),name))
        if core.exact_rank(self.window,19,20)>self.window:raise ValueError('unavailable full-window rank')


@dataclass(frozen=True)
class ConditionalForecast:
    origins:np.ndarray
    capacities:np.ndarray
    floors:np.ndarray
    refit_indices:np.ndarray
    fit_diagnostics:tuple
    family:str
    parameter:float|int


def _qr_diagnostics(fit):
    names=('iterations','primal_objective','dual_objective','duality_gap',
        'primal_residual','dual_residual','primal_tolerance','dual_tolerance',
        'gap_tolerance','dual_grid_denominator','dual_integer_sum',
        'dual_integer_lower','dual_integer_upper')
    result={name:getattr(fit,name) for name in names}
    result['coefficients_sha256']=hashlib.sha256(fit.coefficients.astype('<f8').tobytes()).hexdigest()
    result['dual_numerators_sha256']=hashlib.sha256(fit.dual_grid_numerators.astype('<i8').tobytes()).hexdigest()
    return result


def conditional_forecast(position,times,origins,config,family,parameter,checkpoint=None):
    """Issue a complete fixed-parameter segment, or propagate an explicit failure.

    No partial-return path, tuning, row omission or fallback forecast exists.
    A caller may retain failed attempt diagnostics but may not score a shortened
    segment as complete. Numerical cancellation exceptions propagate unchanged.
    """
    if not isinstance(config,StudyConfig) or family not in FAMILIES:raise ValueError('invalid conditional configuration')
    x=core._vector(position,'conditional positions');ids=_ids(origins,len(x))
    if ids[-1]+config.horizon>=len(x):raise ValueError('incomplete evaluation outcome')
    if family=='QR':
        if np.asarray(parameter).ndim or isinstance(parameter,(bool,np.bool_)):
            raise ValueError('invalid ridge penalty')
        parameter=float(parameter)
        if not math.isfinite(parameter) or parameter<=0:raise ValueError('invalid ridge penalty')
    else:
        parameter=_int(parameter,'neighbor count')
        if parameter>config.window or core.exact_rank(parameter,19,20)>parameter:raise ValueError('unavailable neighbor rank')
    features=build_features(x,times,short_scale=config.short_scale,long_scale=config.long_scale,
        nominal_gap_seconds=config.nominal_gap_seconds)
    cache=core.build_label_cache(x,config.horizon)
    caps=np.empty(len(ids));floors=np.abs(x[ids]);refits=np.empty(len(ids),dtype=np.int64)
    diagnostics=[];previous_refit=None
    last_probe=[-math.inf]

    def fit_progress(_progress):
        # The solver's progress keys differ from the owning resource guard.
        now=time.monotonic()
        if checkpoint is not None and now-last_probe[0]>=.25:
            checkpoint(stage='conditional_fit')
            last_probe[0]=now

    for j,raw_t in enumerate(ids):
        t=int(raw_t);r=refit_origin(t,int(ids[0]),config.refit_step)
        if not r<=t<r+config.refit_step:raise ValueError('query/refit schedule mismatch')
        if r!=previous_refit:
            if checkpoint is not None:checkpoint(stage='conditional_refit',completed_origins=j)
            pool=completed_training_indices(r,config.horizon,config.window,minimum_feature_index=features.valid_from)
            if not np.all(cache.label_end[pool]<=r):raise ValueError('unfinished training labels')
            transform=fit_feature_transform(features.values[pool])
            train=transform_features(features.values[pool],transform,nearest=family!='QR')
            train_g=cache.headroom[pool];scale=response_scale(train_g,x[pool])
            detail=dict(refit_index=r,training_first_origin=int(pool[0]),training_last_origin=int(pool[-1]),
                training_count=len(pool),latest_label_end=int(cache.label_end[pool[-1]]),response_scale=scale)
            if family=='QR':
                try:
                    fit=fit_quantile_ridge(np.column_stack((np.ones(len(pool)),train)),train_g/scale,
                        tau=float(Fraction(19,20)),penalty=parameter,checkpoint=fit_progress)
                except QuantileFitError as exc:
                    # Preserve completed issues and the failed fit's exact timing.
                    # This is a private partial trace, never a complete score.
                    exc.failure_context=dict(detail,query_issue=t,issued_origin_count=j)
                    exc.partial_forecast=ConditionalForecast(core._readonly(ids[:j]),core._readonly(caps[:j]),
                        core._readonly(floors[:j]),core._readonly(refits[:j]),tuple(diagnostics),family,parameter)
                    raise
                detail.update(_qr_diagnostics(fit))
            elif family=='SCALED_KNN':
                train_g=train_g/np.maximum(features.short_rms[pool],1e-6*scale)
            diagnostics.append(detail);previous_refit=r
        query=transform_features(features.values[t:t+1],transform,nearest=family!='QR')[0]
        if family=='QR':
            predicted=scale*float(fit.coefficients[0]+query@fit.coefficients[1:])
        else:
            predicted,_=neighbor_quantile(train,query,train_g,pool,parameter)
            if family=='SCALED_KNN':predicted*=max(float(features.short_rms[t]),1e-6*scale)
        if not math.isfinite(predicted):raise ValueError('nonfinite predicted headroom')
        caps[j]=floors[j]+max(0.,predicted);refits[j]=r
        if checkpoint is not None and (j%32==31 or j==len(ids)-1):
            checkpoint(stage='conditional_issue',completed_origins=j+1)
    if not np.isfinite(caps).all() or np.any(caps<floors):raise ValueError('invalid final conditional capacity')
    return ConditionalForecast(core._readonly(ids),core._readonly(caps),core._readonly(floors),
        core._readonly(refits),tuple(diagnostics),family,parameter)


def issue_historical(position,cache,*,issue,refit,window,step,neighbors=None):
    """F/S/K from a distinct frozen-refit pool, reanchored at actual query t."""
    x=core._vector(position,'historical positions')
    issue=_int(issue,'actual issue',0);refit=_int(refit,'refit',0)
    window=_int(window,'window');step=_int(step,'step')
    if not isinstance(cache,core.LabelCache) or len(cache.peak)+cache.horizon!=len(x):raise ValueError('historical cache mismatch')
    if not refit<=issue<refit+step or issue>=len(x):raise ValueError('query outside frozen block')
    pool=completed_training_indices(refit,cache.horizon,window,minimum_feature_index=0)
    if not np.all(cache.label_end[pool]<=refit):raise ValueError('historical maturity mismatch')
    if not np.array_equal(cache.peak[pool]-np.abs(x[pool]),cache.headroom[pool]):raise ValueError('anchor/cache mismatch')
    if neighbors is not None:
        neighbors=_int(neighbors,'one-state count')
        if neighbors>window:raise ValueError('one-state count exceeds history')
        distance=np.abs(x[pool]-x[issue])
        if not np.isfinite(distance).all():raise ValueError('nonfinite one-state distance')
        selected=np.lexsort((-pool,distance))[:neighbors]
        pool=pool[np.sort(selected)]
    rank=core.exact_rank(len(pool),19,20)
    if rank>len(pool):raise ValueError('unavailable historical rank')
    current=float(x[issue]);floor=abs(current)
    with np.errstate(over='raise',invalid='raise'):
        # Preserve original S's subtract -> rank -> add floating arithmetic.
        scores_s=np.maximum(current+cache.upper_increment[pool],-current-cache.lower_increment[pool])-floor
        caps=np.array((floor+core.order_statistic(cache.headroom[pool],rank),
            floor+core.order_statistic(scores_s,rank),max(floor,core.order_statistic(cache.peak[pool],rank))))
    if np.any(scores_s<0) or not np.isfinite(caps).all() or np.any(caps<floor):raise ValueError('invalid historical capacity')
    return core._readonly(caps)


def historical_forecasts(position,origins,config,neighbor_count=None,checkpoint=None):
    if not isinstance(config,StudyConfig):raise ValueError('invalid historical configuration')
    x=core._vector(position,'historical positions');ids=_ids(origins,len(x))
    if ids[-1]+config.horizon>=len(x):raise ValueError('incomplete historical outcome')
    cache=core.build_label_cache(x,config.horizon)
    prefixes=('rolling','frozen')+(('one_state',) if neighbor_count is not None else ())
    result={prefix+'_'+rule:np.empty(len(ids)) for prefix in prefixes for rule in ('F','S','K')}
    for j,t in enumerate(ids):
        t=int(t);r=refit_origin(t,int(ids[0]),config.refit_step)
        for prefix in prefixes:
            caps=issue_historical(x,cache,issue=t,refit=r if prefix=='frozen' else t,
                window=config.window,step=config.refit_step if prefix=='frozen' else 1,
                neighbors=neighbor_count if prefix=='one_state' else None)
            for k,rule in enumerate(('F','S','K')):result[prefix+'_'+rule][j]=caps[k]
        if checkpoint is not None and (j%32==31 or j==len(ids)-1):
            checkpoint(stage='historical_issue',completed_origins=j+1)
    return {name:core._readonly(values) for name,values in result.items()}


@dataclass(frozen=True)
class PredictionScores:
    origins:np.ndarray
    capacities:np.ndarray
    floors:np.ndarray
    errors:np.ndarray
    pinball:np.ndarray
    overrun:np.ndarray
    unused:np.ndarray
    strict_breach:np.ndarray


def score_predictions(peak,capacities,floors,origins):
    peak=core._vector(peak,'peak');capacity=core._vector(capacities,'capacity');floor=core._vector(floors,'floor')
    ids=core._indices(origins,'score origins')
    if capacity.shape!=peak.shape or floor.shape!=peak.shape or ids.shape!=peak.shape or np.any(floor<0) or np.any(peak<floor) or np.any(capacity<floor):
        raise ValueError('invalid score alignment/floor')
    with np.errstate(over='raise',invalid='raise'):
        error=peak-capacity;overrun=np.maximum(error,0);unused=np.maximum(-error,0)
        pinball=float(Fraction(19,20))*overrun+float(Fraction(1,20))*unused
    if not all(np.isfinite(a).all() for a in (error,overrun,unused,pinball)):raise ValueError('nonfinite score')
    return PredictionScores(*(core._readonly(a) for a in (ids,capacity,floor,error,pinball,overrun,unused,error>0)))


def summarize_scores(scores):
    if not isinstance(scores,PredictionScores):raise ValueError('invalid scores')
    n=len(scores.origins);breaches=int(np.count_nonzero(scores.strict_breach))
    overrun=core.stable_mean(scores.overrun);unused=core.stable_mean(scores.unused)
    conditional=math.fsum(map(float,scores.overrun))/breaches if breaches else None
    result=dict(origin_count=n,mean_pinball=core.stable_mean(scores.pinball),mean_capacity=core.stable_mean(scores.capacities),
        mean_extra_allowance=core.stable_mean(scores.capacities-scores.floors),strict_breach_count=breaches,
        strict_breach_rate=breaches/n,mean_positive_overrun=overrun,conditional_mean_overrun=conditional,
        conditional_overrun_denominator=breaches,conditional_overrun_undefined_reason=None if breaches else 'NO_STRICT_BREACHES',
        mean_unused_allowance=unused)
    core._assert_mean_equal(result['mean_pinball'],float(Fraction(19,20))*overrun+float(Fraction(1,20))*unused,n,max(1.,result['mean_pinball']))
    if conditional is not None:core._assert_mean_equal(overrun,result['strict_breach_rate']*conditional,n,max(1.,overrun,conditional))
    return result


def select_parameter(rows,candidates,*,expected_count):
    """Strict full-menu eligibility; a failed declared candidate blocks the cell."""
    expected_count=_int(expected_count,'validation count')
    candidates=list(candidates);rows=list(rows)
    if not candidates or len(set(candidates))!=len(candidates) or len(rows)!=len(candidates):raise ValueError('validation menu mismatch')
    if sorted(row['parameter'] for row in rows)!=sorted(candidates):raise ValueError('validation candidate mismatch')
    if any(row.get('status') not in ('COMPLETE','FAILED','INCOMPLETE') for row in rows):raise ValueError('invalid candidate status')
    failed=[];incomplete=[]
    for row in rows:
        if row['status']=='FAILED':failed.append(row['parameter']);continue
        if row['status']=='INCOMPLETE':incomplete.append(row['parameter']);continue
        loss=row.get('mean_pinball')
        if row.get('origin_count')!=expected_count or type(loss) not in (int,float) or not math.isfinite(loss) or loss<0:
            raise ValueError('invalid complete candidate score')
    if failed or incomplete:return dict(status='INELIGIBLE',parameter=None,failed_candidates=failed,
        incomplete_candidates=incomplete,reason='DECLARED_CANDIDATE_INCOMPLETE' if incomplete else 'DECLARED_CANDIDATE_FAILED')
    winner=min(rows,key=lambda row:(row['mean_pinball'],-row['parameter']))
    return dict(status='SELECTED',parameter=winner['parameter'],mean_validation_pinball=winner['mean_pinball'])


def nonoverlap_origins(first,last,horizon):
    first=_int(first,'first',0);last=_int(last,'last',0);horizon=_int(horizon,'horizon')
    if last<first:raise ValueError('empty nonoverlap grid')
    return core._readonly(np.arange(first,last+1,horizon+1,dtype=np.int64))


def paired_comparison(left,right,issue_dates,*,horizon):
    """Descriptive paired means; callers bind source/unit/forecast identities.

    The two series must share exact origins and issue floors. No uncertainty,
    selection, statistical independence or cross-source pooling is inferred.
    H+1 selection starts once at the global evaluation start, not each year.
    """
    if not isinstance(left,PredictionScores) or not isinstance(right,PredictionScores):raise ValueError('invalid comparison scores')
    if not np.array_equal(left.origins,right.origins) or not np.array_equal(left.floors,right.floors):raise ValueError('paired origin/floor mismatch')
    ids=_ids(left.origins,int(left.origins[-1])+1)
    dates=np.asarray(issue_dates)
    if dates.shape!=ids.shape or dates.dtype.kind!='M' or np.isnat(dates).any() or np.any(dates[1:]<=dates[:-1]):raise ValueError('paired date mismatch')

    def group(mask):
        n=int(np.count_nonzero(mask))
        if n==0:raise ValueError('empty paired group')
        a=core.stable_mean(left.pinball[mask]);b=core.stable_mean(right.pinball[mask])
        difference=core.stable_mean(left.pinball[mask]-right.pinball[mask])
        core._assert_mean_equal(difference,a-b,n,max(1.,a,b,abs(difference)))
        relative=100*(difference/b) if b>0 else None
        undefined=None if b>0 else 'ZERO_REFERENCE_MEAN_LOSS'
        if relative is not None and not math.isfinite(relative):
            relative=None;undefined='RELATIVE_DIFFERENCE_NOT_FINITE'
        return dict(origin_count=n,first_source_index=int(ids[mask][0]),last_source_index=int(ids[mask][-1]),
            mean_pinball_left=a,mean_pinball_right=b,mean_pinball_difference=difference,
            relative_mean_loss_difference_percent=relative,
            relative_difference_undefined_reason=undefined,
            mean_capacity_difference=core.stable_mean(left.capacities[mask]-right.capacities[mask]),
            mean_positive_overrun_difference=core.stable_mean(left.overrun[mask]-right.overrun[mask]),
            mean_unused_allowance_difference=core.stable_mean(left.unused[mask]-right.unused[mask]),
            strict_breach_count_left=int(np.count_nonzero(left.strict_breach[mask])),
            strict_breach_count_right=int(np.count_nonzero(right.strict_breach[mask])))

    years=dates.astype('datetime64[Y]');annual=[]
    for year in np.unique(years):annual.append(dict(calendar_year=str(year),**group(years==year)))
    grid=nonoverlap_origins(int(ids[0]),int(ids[-1]),horizon)
    return dict(all=group(np.ones(len(ids),dtype=bool)),years=annual,
        nonoverlap=dict(stride_records=int(horizon)+1,**group(np.isin(ids,grid))))
