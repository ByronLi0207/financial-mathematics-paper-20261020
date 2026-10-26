"""WP5 generic-tau controls, frozen selection and whole-cell accounting."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,re,signal
from pathlib import Path
import numpy as np
from conditional_study import StudyConfig,select_parameter
import study_core as core
import v6_worker as w
import v6_inference as inf

OUT=w.PUBLIC/'wp5-v2';PRIVATE=w.PRIVATE/'wp5-v2'
LEVELS={'90':.9,'99':.99}

def select_declared_menu(candidates,menu,count):
    return select_parameter(candidates,menu,expected_count=count)
def direction_reversal(current,old):
    if current is None or not math.isfinite(current):return None
    return (current>0 and old<0) or (current<0 and old>0)
def compare_tau_losses(new,reference):
    result=inf.compare_losses(new,reference,horizon=6)
    result['diagnostic_mean_difference']=result.get('mean_difference')
    result['mean_difference']=core.stable_mean(np.asarray(new)-np.asarray(reference))
    return result
def vector_sha(x):return hashlib.sha256(np.asarray(x,dtype='<f8').tobytes()).hexdigest()
def config_w(config,win):return StudyConfig(config.horizon,win,config.refit_step,config.short_scale,config.long_scale,config.nominal_gap_seconds)
def key(source,level):return f'{source}-tau{level}'
def check_freeze():
    p=w.ROOT/'protocol/revision-v6/wp5-executable-freeze-v2.json';x=w.read_json(p)
    for path,digest in x['files'].items():
        if w.sha(w.ROOT/path)!=digest:raise ValueError('WP5_EXECUTABLE_CHANGED:'+path)
    w.check_execution_freeze();return w.sha(p)
def alarm():signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(RuntimeError('RESOURCE_HARD_WALL')));signal.alarm(600)
def scores(y,c,ids,tau):return inf.summarize_scores(y,c,tau=tau,origins=ids,horizon=6)
def base(source):
    spec=w.read_json(w.ROOT/w.SPEC);win=spec['sources'][source]['primary_window']
    return w.setup(source,6,win)

def control95(source):
    from v6_tau import forecast_qr_tau,historical_f_tau
    freeze=check_freeze();g=w.Guard();alarm();g();s,cfg,c,lam=base(source);checks=[]
    try:
        for phase in ('validation','evaluation'):
            ids=w.ids_for(cfg,phase);old=w.original_trace(source,6,c.window,phase,'QR',position=s.position)
            new=forecast_qr_tau(s.position,s.dates,ids,c,lam,tau=.95,checkpoint=g)
            if not np.array_equal(old['capacity'],new.capacities):raise ValueError('POINT95_QR_FULL_SEGMENT_IDENTITY')
            checks.append(dict(method='QR',phase=phase,n=len(ids),capacity_sha256=vector_sha(new.capacities),original_trace_sha256=old['trace_sha256'],status='EXACT_IDENTITY'))
        ids=w.ids_for(cfg,'evaluation')
        references=[('frozen_F',c.window,False)]+([('rolling_F',720,True)] if source=='fx_hourly' else [])
        for method,win,rolling in references:
            old=w.original_trace(source,6,win,'references',method,position=s.position)
            cap=historical_f_tau(s.position,ids,config_w(c,win),tau=.95,rolling=rolling,checkpoint=g)
            if not np.array_equal(old['capacity'],cap):raise ValueError('POINT95_F_FULL_SEGMENT_IDENTITY')
            checks.append(dict(method=method,window=win,phase='evaluation',n=len(ids),capacity_sha256=vector_sha(cap),original_trace_sha256=old['trace_sha256'],status='EXACT_IDENTITY'))
        g();z=dict(status='COMPLETE_EXACT_IDENTITY',source=source,tau=.95,checks=checks,executable_freeze_sha256=freeze,resources=g.summary())
        w.write_json_new(OUT/f'control95-{source}.json',z);print(json.dumps(z))
    finally:signal.alarm(0)

def validate_control_receipt(z,source,cfg,executable_freeze):
    if (z.get('source')!=source or z.get('tau')!=.95 or
        z.get('status')!='COMPLETE_EXACT_IDENTITY' or
        z.get('executable_freeze_sha256')!=executable_freeze):
        raise ValueError('POINT95_CONTROL_HEADER')
    expected=[('QR','validation',None),('QR','evaluation',None),
              ('frozen_F','evaluation',cfg['primary_window'])]
    if source=='fx_hourly':expected.append(('rolling_F','evaluation',720))
    checks=z.get('checks',[])
    if len(checks)!=len(expected):raise ValueError('POINT95_CONTROL_INVENTORY')
    actual=[]
    for r in checks:
        ident=(r.get('method'),r.get('phase'),r.get('window'))
        if ident not in expected or ident in actual:raise ValueError('POINT95_CONTROL_INVENTORY')
        n=cfg[r['phase']+'_origin_last']-cfg[r['phase']+'_origin_first']+1
        if r.get('n')!=n or isinstance(r.get('n'),bool) or r.get('status')!='EXACT_IDENTITY':
            raise ValueError('POINT95_CONTROL_SEGMENT')
        if any(not re.fullmatch('[a-f0-9]{64}',str(r.get(k,''))) for k in ('capacity_sha256','original_trace_sha256')):
            raise ValueError('POINT95_CONTROL_HASH')
        actual.append(ident)

def validate_phase_receipt(z,source,level,phase,controls,executable_freeze,selection_freeze=None):
    expected=dict(source=source,level=level,tau=LEVELS[level],phase=phase,
                  point95_controls=controls,executable_freeze_sha256=executable_freeze)
    if selection_freeze is not None:expected['selection_freeze_sha256']=selection_freeze
    if any(z.get(k)!=v for k,v in expected.items()) or z.get('status') not in ('COMPLETE','NA'):
        raise ValueError('WP5_PHASE_RECEIPT_IDENTITY')

def validate_selection_binding(cell,validation,evaluation=None):
    expected=dict(status=validation['status'],reason=validation.get('reason'),
                  selected_parameter=validation['selection'].get('parameter'))
    if any(cell.get(k)!=v for k,v in expected.items()):raise ValueError('WP5_SELECTED_VALIDATION_IDENTITY')
    if evaluation is not None and evaluation['status']=='COMPLETE':
        if cell['status']!='COMPLETE' or evaluation.get('selected_parameter')!=cell['selected_parameter']:
            raise ValueError('WP5_EVALUATED_SELECTION_IDENTITY')

def validate_evaluation_arrays(arrays,expected_ids,expected_peak,expected_floor):
    keys=('origins','peak','floor','QR','matched_F','primary_F')
    if any(k not in arrays for k in keys):raise ValueError('WP5_EVALUATION_ARRAY_INVENTORY')
    ids=np.asarray(expected_ids);peak=np.asarray(expected_peak);floor=np.asarray(expected_floor)
    if (ids.ndim!=1 or peak.shape!=ids.shape or floor.shape!=ids.shape or
        any(np.asarray(arrays[k]).shape!=ids.shape for k in keys)):
        raise ValueError('WP5_EVALUATION_ARRAY_SHAPE')
    for k,expected in (('origins',ids),('peak',peak),('floor',floor)):
        if not np.array_equal(arrays[k],expected):raise ValueError('WP5_EVALUATION_'+k.upper()+'_IDENTITY')
    if (not np.isfinite(peak).all() or not np.isfinite(floor).all() or
        np.any(floor<0) or np.any(peak<floor)):
        raise ValueError('WP5_EVALUATION_TARGET_GEOMETRY')
    for k in keys[3:]:
        if not np.isfinite(arrays[k]).all() or np.any(arrays[k]<floor):
            raise ValueError('WP5_EVALUATION_REPORT_GEOMETRY')

def require_controls():
    result={};freeze=check_freeze();spec=w.read_json(w.ROOT/w.SPEC)
    for s in ('fx_hourly','nyfed_weekly'):
        p=OUT/f'control95-{s}.json';z=w.read_json(p)
        validate_control_receipt(z,s,spec['sources'][s],freeze)
        result[s]=w.sha(p)
    return result

def validation(source,level):
    from v6_tau import forecast_qr_tau,tail_admission
    controls=require_controls();freeze=check_freeze();tau=LEVELS[level];g=w.Guard();alarm();arrays={};menu=[];s=None;screen=None
    penalties=w.read_json(w.ROOT/w.SPEC)['qr_penalties']
    try:
        g();s,cfg,c,_=base(source);ids=w.ids_for(cfg,'validation');cache=core.build_label_cache(s.position,6)
        windows=[c.window,720] if source=='fx_hourly' else [c.window]
        screen=tail_admission(windows,len(ids),tau=tau);penalties=w.read_json(w.ROOT/w.SPEC)['qr_penalties']
        if not screen['eligible']:
            z=dict(status='NA',reason='PREDECLARED_TAIL_INFORMATION',screen=screen,candidates=[dict(parameter=p,status='NOT_ATTEMPTED_TAIL_INFORMATION',origin_count=None,mean_pinball=None) for p in penalties],selection=dict(status='INELIGIBLE',parameter=None))
        else:
            resource_failure=None
            for j,p in enumerate(penalties):
                if resource_failure:
                    menu.append(dict(parameter=p,status='NOT_ATTEMPTED_RESOURCE',origin_count=None,mean_pinball=None,reason=resource_failure));continue
                try:
                    fit=forecast_qr_tau(s.position,s.dates,ids,c,p,tau=tau,checkpoint=g)
                    metric=scores(cache.peak[ids],fit.capacities,ids,tau)
                    menu.append(dict(parameter=p,status='COMPLETE',origin_count=len(ids),mean_pinball=metric['mean_loss'],scores=metric,fit_diagnostics=list(fit.fit_diagnostics)))
                    arrays[f'candidate{j}_capacity']=fit.capacities
                except Exception as exc:
                    if isinstance(exc,RuntimeError) and str(exc).startswith('RESOURCE_'):
                        resource_failure=str(exc);menu.append(dict(parameter=p,status='FAILED_RESOURCE',origin_count=None,mean_pinball=None,reason=resource_failure))
                    elif hasattr(exc,'code'):
                        menu.append(dict(parameter=p,status='FAILED',origin_count=None,mean_pinball=None,reason=exc.code,diagnostics=dict(getattr(exc,'diagnostics',{})),failure_context=getattr(exc,'failure_context',None)))
                    else:raise
            selected=select_declared_menu(menu,penalties,len(ids))
            z=dict(status='COMPLETE' if selected['status']=='SELECTED' else 'NA',reason=None if selected['status']=='SELECTED' else 'DECLARED_VALIDATION_MENU_INELIGIBLE',screen=screen,candidates=menu,selection=selected)
            arrays.update(origins=ids,peak=cache.peak[ids],floor=np.abs(s.position[ids]))
            if not resource_failure:g()
        z.update(source=source,tau=tau,level=level,phase='validation',analysis_status='post-result / exploratory',point95_controls=controls,executable_freeze_sha256=freeze,raw_source_sha256=s.sha256,resources=g.summary())
        if arrays:z['private_artifact']=w.save_private(PRIVATE/f'validation-{key(source,level)}.npz',**arrays)
        w.write_json_new(OUT/f'validation-{key(source,level)}.json',z)
        print(json.dumps(dict(source=source,tau=tau,status=z['status'],reason=z['reason'],selection=z['selection'],resources=z['resources'])))
    except RuntimeError as exc:
        if not str(exc).startswith('RESOURCE_'):raise
        seen={r['parameter'] for r in menu}
        menu.extend(dict(parameter=p,status='NOT_ATTEMPTED_RESOURCE',origin_count=None,mean_pinball=None,reason=str(exc)) for p in penalties if p not in seen)
        z=dict(status='NA',reason=str(exc),source=source,tau=tau,level=level,phase='validation',analysis_status='post-result / exploratory',
            screen=screen,candidates=menu,selection=dict(status='INELIGIBLE',parameter=None),point95_controls=controls,
            executable_freeze_sha256=freeze,raw_source_sha256=getattr(s,'sha256',None),resources=g.summary())
        w.write_json_new(OUT/f'validation-{key(source,level)}.json',z)
        print(json.dumps(dict(source=source,tau=tau,status='NA',reason=str(exc),resources=z['resources'])))
    finally:signal.alarm(0)

def freeze_selection():
    controls=require_controls();freeze=check_freeze();x={}
    for source in ('fx_hourly','nyfed_weekly'):
        for level in LEVELS:
            p=OUT/f'validation-{key(source,level)}.json';z=w.read_json(p)
            validate_phase_receipt(z,source,level,'validation',controls,freeze)
            x[key(source,level)]=dict(status=z['status'],reason=z['reason'],selected_parameter=z['selection'].get('parameter'),receipt_sha256=w.sha(p))
    z=dict(status='FROZEN_BEFORE_WP5_EVALUATION',created_utc=w.utc(),cells=x,point95_controls=controls,executable_freeze_sha256=freeze)
    w.write_json_new(OUT/'selection-freeze.json',z);print(json.dumps(z))

def evaluation(source,level):
    from v6_tau import forecast_qr_tau,historical_f_tau
    controls=require_controls();freeze=check_freeze();tau=LEVELS[level];g=w.Guard();alarm();arrays={};sel=w.read_json(OUT/'selection-freeze.json')['cells'][key(source,level)]
    try:
        g();p=OUT/f'validation-{key(source,level)}.json'
        if w.sha(p)!=sel['receipt_sha256']:raise ValueError('WP5_VALIDATION_RECEIPT_CHANGED')
        val=w.read_json(p);validate_phase_receipt(val,source,level,'validation',controls,freeze)
        validate_selection_binding(sel,val)
        selection=w.read_json(OUT/'selection-freeze.json')
        if selection.get('status')!='FROZEN_BEFORE_WP5_EVALUATION' or selection.get('point95_controls')!=controls or selection.get('executable_freeze_sha256')!=freeze:
            raise ValueError('WP5_SELECTION_FREEZE_IDENTITY')
        if sel['status']!='COMPLETE':z=dict(status='NA',reason='VALIDATION_INELIGIBLE',validation_reason=sel['reason'])
        else:
            s,cfg,c,_=base(source);ids=w.ids_for(cfg,'evaluation');cache=core.build_label_cache(s.position,6)
            try:
                fit=forecast_qr_tau(s.position,s.dates,ids,c,sel['selected_parameter'],tau=tau,checkpoint=g)
                reports=dict(QR=fit.capacities,matched_F=historical_f_tau(s.position,ids,c,tau=tau,rolling=False,checkpoint=g))
                if source=='fx_hourly':reports['primary_F']=historical_f_tau(s.position,ids,config_w(c,720),tau=tau,rolling=True,checkpoint=g)
                else:reports['primary_F']=reports['matched_F']
                metrics={name:scores(cache.peak[ids],cap,ids,tau) for name,cap in reports.items()}
                g();z=dict(status='COMPLETE',reason=None,selected_parameter=sel['selected_parameter'],scores=metrics,fit_diagnostics=list(fit.fit_diagnostics))
                arrays=dict(origins=ids,peak=cache.peak[ids],floor=np.abs(s.position[ids]),**reports)
            except Exception as exc:
                if isinstance(exc,RuntimeError) and str(exc).startswith('RESOURCE_'):z=dict(status='NA',reason=str(exc))
                elif hasattr(exc,'code'):z=dict(status='NA',reason=exc.code,diagnostics=dict(getattr(exc,'diagnostics',{})),failure_context=getattr(exc,'failure_context',None))
                else:raise
        z.update(source=source,tau=tau,level=level,phase='evaluation',analysis_status='post-result / exploratory',point95_controls=controls,selection_freeze_sha256=w.sha(OUT/'selection-freeze.json'),executable_freeze_sha256=freeze,resources=g.summary())
        if arrays:z['private_artifact']=w.save_private(PRIVATE/f'evaluation-{key(source,level)}.npz',**arrays)
        w.write_json_new(OUT/f'evaluation-{key(source,level)}.json',z)
        print(json.dumps({k:z.get(k) for k in ('source','tau','status','reason','selected_parameter','scores','resources')}))
    except RuntimeError as exc:
        if not str(exc).startswith('RESOURCE_'):raise
        z=dict(status='NA',reason=str(exc),source=source,tau=tau,level=level,phase='evaluation',analysis_status='post-result / exploratory',point95_controls=controls,
            selection_freeze_sha256=w.sha(OUT/'selection-freeze.json'),executable_freeze_sha256=freeze,resources=g.summary())
        w.write_json_new(OUT/f'evaluation-{key(source,level)}.json',z)
        print(json.dumps(dict(source=source,tau=tau,status='NA',reason=str(exc),resources=z['resources'])))
    finally:signal.alarm(0)

def summarize():
    controls=require_controls();freeze=check_freeze();rows=[];comparisons=[];g=w.Guard();g()
    selection_path=OUT/'selection-freeze.json';selection_hash=w.sha(selection_path);selection=w.read_json(selection_path)
    if selection.get('status')!='FROZEN_BEFORE_WP5_EVALUATION' or selection.get('point95_controls')!=controls or selection.get('executable_freeze_sha256')!=freeze:
        raise ValueError('WP5_SELECTION_FREEZE_IDENTITY')
    with (w.ROOT/'results/revision-20261022/paired-comparisons.csv').open(newline='') as f:old=list(csv.DictReader(f))
    for level,tau in LEVELS.items():
        for source,kind,old_ref,old_win in (('fx_hourly','primary','rolling_F',720),('fx_hourly','matched','frozen_F',2880),('nyfed_weekly','primary','frozen_F',260)):
            p=OUT/f'evaluation-{key(source,level)}.json';z=w.read_json(p);label=f'{source}:tau{level}:{kind}'
            validate_phase_receipt(z,source,level,'evaluation',controls,freeze,selection_freeze=selection_hash)
            val_path=OUT/f'validation-{key(source,level)}.json'
            if w.sha(val_path)!=selection['cells'][key(source,level)]['receipt_sha256']:
                raise ValueError('WP5_VALIDATION_RECEIPT_CHANGED')
            val=w.read_json(val_path);validate_phase_receipt(val,source,level,'validation',controls,freeze)
            validate_selection_binding(selection['cells'][key(source,level)],val,z)
            row=dict(slot_id=label,source=source,tau=tau,reference_kind=kind,status=z['status'],reason=z.get('reason'),selected_parameter=z.get('selected_parameter'),analysis_status='post-result / exploratory',
                direction='QR_minus_reference',horizon=6,qr_window=2880 if source=='fx_hourly' else 260,reference_method=old_ref,reference_window=old_win,reference_update='rolling' if old_ref=='rolling_F' else 'frozen_original_grid',forecast_status=z['status'],raw_p=None,mean_difference=None,direction_reversal=None)
            if z['status']=='COMPLETE':
                path=PRIVATE/f'evaluation-{key(source,level)}.npz'
                if path.stat().st_size!=z['private_artifact']['bytes'] or w.sha(path)!=z['private_artifact']['sha256']:raise ValueError('WP5_PRIVATE_TRACE_CHANGED')
                with np.load(path,allow_pickle=False) as f:arrays={k:np.array(f[k]) for k in f.files}
                s,cfg,c,_=base(source);expected_ids=w.ids_for(cfg,'evaluation');cache=core.build_label_cache(s.position,6)
                validate_evaluation_arrays(arrays,expected_ids,cache.peak[expected_ids],np.abs(s.position[expected_ids]))
                if source=='nyfed_weekly' and not np.array_equal(arrays['primary_F'],arrays['matched_F']):raise ValueError('TREASURY_PRIMARY_MATCHED_IDENTITY')
                ids=arrays['origins'];y=arrays['peak'];q=arrays['QR'];r=arrays[kind+'_F']
                qscore=scores(y,q,ids,tau);rscore=scores(y,r,ids,tau)
                if qscore!=z['scores']['QR'] or rscore!=z['scores'][kind+'_F']:raise ValueError('WP5_SCORE_IDENTITY')
                result=compare_tau_losses(inf.pinball_losses(y,q,tau=tau),inf.pinball_losses(y,r,tau=tau))
                orig=[r for r in old if r['source']==source and r['horizon']=='6' and r['left_method']=='QR' and r['left_window']==str(2880 if source=='fx_hourly' else 260) and r['right_method']==old_ref and r['right_window']==str(old_win)]
                if len(orig)!=1:raise ValueError('SAME_NAMED_POINT95_CONTRAST_MISSING')
                old_diff=float(orig[0]['mean_pinball_difference'])
                row.update(result);row.update(qr_scores=qscore,reference_scores=rscore,raw_p=result.get('dm_p') if result['status']=='OK' else None,
                    mean_loss_change_percent=100*result['mean_difference']/rscore['mean_loss'] if rscore['mean_loss'] else None,
                    point95_mean_difference=old_diff,point95_contrast_id=orig[0]['contrast_id'],direction_reversal=direction_reversal(result['mean_difference'],old_diff))
            rows.append(row)
    slots=[r['slot_id'] for r in rows];design=w.read_json(w.ROOT/'protocol/revision-v6/wp5-executable-freeze-v2.json')
    if slots!=design['contrast_slots']:raise ValueError('SIX_FIXED_TAU_SLOTS_CHANGED')
    adjusted=inf.fixed_slot_holm(slots,{r['slot_id']:r['raw_p'] for r in rows})
    for row,a in zip(rows,adjusted['slots']):row.update(bookkeeping_p=a['bookkeeping_p'],holm_p=a['holm_p'],holm_component_status=a['status'])
    g();report=dict(status='COMPLETE_INVENTORY',analysis_status='post-result / exploratory',family_n=6,raw_na_count=adjusted['raw_na_count'],rows=rows,executable_freeze_sha256=freeze,resources=g.summary(),
        scope='Refitted target-level sensitivity, not fixed-report loss reweighting or robustness to actual funding costs. Absolute losses across tau have different objectives. Treasury primary/matched coincide and count once.')
    w.write_json_new(w.PUBLIC/'wp5-tau-summary.json',report);print(json.dumps(dict(status=report['status'],family_n=6,raw_na_count=adjusted['raw_na_count'],rows=rows,resources=report['resources'])))

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=('control95','validation','freeze','evaluation','summary'));p.add_argument('--source',choices=('fx_hourly','nyfed_weekly'));p.add_argument('--level',choices=tuple(LEVELS));a=p.parse_args()
    if a.operation=='control95':control95(a.source)
    elif a.operation=='validation':validation(a.source,a.level)
    elif a.operation=='evaluation':evaluation(a.source,a.level)
    elif a.operation=='freeze':freeze_selection()
    else:summarize()
if __name__=='__main__':main()
