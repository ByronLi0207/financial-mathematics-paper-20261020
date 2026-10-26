"""Independent stdlib WP3 arithmetic/readback; never simulate or fit a model.

Run only after study termination and summary generation. Input files are never
modified. The output is exclusive-create. Missing measured resources are
UNVERIFIED, never replaced by a configured budget. This is an arithmetic and
provenance audit, not independent simulation replication.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys

IDENTITY = ('rep','phi_index','p_index','window','horizon','method')
CELL = ('phi_index','p_index','window','horizon','method')
GRID = ('phi','variance_persistence','window','horizon')
ESTIMATES = ('relative_loss_percent','relative_loss_mcse','model_breach_rate',
    'model_breach_mcse','reference_breach_rate','reference_breach_mcse',
    'win_fraction','win_mcse','win_mcse_worst_bound')
TERMINATION_TOLERANCE_SECONDS = 5.


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite(x):
    return type(x) in (int,float) and math.isfinite(x)


def same_value(a,b):
    if a is None or b is None:return a is b
    if type(a) is bool or type(b) is bool:return type(a) is type(b) and a==b
    if type(a) in (int,float) and type(b) in (int,float):
        return finite(a) and finite(b) and math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-12)
    if isinstance(a,dict) and isinstance(b,dict):
        return set(a)==set(b) and all(same_value(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(same_value(x,y) for x,y in zip(a,b))
    return type(a) is type(b) and a==b


def issue(code,**details):
    return dict(code=code,**details)


def inventory_keys(design):
    return set(product(range(design['repetitions']),range(len(design['phi'])),
        range(len(design['variance_persistence'])),design['windows'],
        design['horizons'],design['methods']))


def inventory_errors(design,rows):
    errors=[]; keys=[]
    n=design['evaluation_last']-design['evaluation_first']+1
    expected=inventory_keys(design)
    for i,row in enumerate(rows):
        try:key=tuple(row[k] for k in IDENTITY)
        except (KeyError,TypeError):
            errors.append(issue('MISSING_INVENTORY_FIELDS',row=i));continue
        keys.append(key)
        if key not in expected:
            errors.append(issue('UNEXPECTED_INVENTORY_IDENTITY',identity=list(key)));continue
        rep,pi,gi,w,h,method=key
        if row.get('phi')!=design['phi'][pi] or row.get('variance_persistence')!=design['variance_persistence'][gi]:
            errors.append(issue('INVENTORY_PARAMETER_MISMATCH',identity=list(key)))
        status=row.get('status')
        if status not in ('COMPLETE','FAILED','NOT_ATTEMPTED'):
            errors.append(issue('INVALID_METHOD_STATUS',identity=list(key),actual=status))
        if status=='COMPLETE':
            e=row.get('evaluation') or {}
            if (type(e.get('n')) is not int or e['n']!=n
                or type(e.get('strict_breach_count')) is not int
                or not 0<=e['strict_breach_count']<=n
                or not finite(e.get('mean_loss')) or e['mean_loss']<0
                or not finite(e.get('strict_breach_rate'))
                or e['strict_breach_rate']!=e['strict_breach_count']/n):
                errors.append(issue('INVALID_COMPLETE_SCORE',identity=list(key)))
        elif row.get('evaluation') is not None:
            errors.append(issue('INCOMPLETE_METHOD_HAS_SCORE',identity=list(key)))
    for key,count in Counter(keys).items():
        if count>1:errors.append(issue('DUPLICATE_INVENTORY_IDENTITY',identity=list(key),count=count))
    errors.extend(issue('MISSING_INVENTORY_IDENTITY',identity=list(key)) for key in sorted(expected-set(keys)))
    return errors


def paired_oracle(design,rows):
    """Independent scalar recomputation; no production-code imports."""
    index={tuple(r[k] for k in IDENTITY):r for r in rows}
    output=[]; planned=design['repetitions']
    for pi,gi,w,h,method in product(range(len(design['phi'])),
            range(len(design['variance_persistence'])),design['windows'],design['horizons'],design['methods']):
        a=[];b=[];model_rates=[];reference_rates=[]
        failed=unattempted=0; reasons=Counter(); statuses=Counter()
        for rep in range(planned):
            model=index[(rep,pi,gi,w,h,method)]; ref=index[(rep,pi,gi,w,h,'F')]
            statuses[model['status']]+=1
            if model['status']=='COMPLETE' and ref['status']=='COMPLETE':
                a.append(model['evaluation']['mean_loss']);b.append(ref['evaluation']['mean_loss'])
                model_rates.append(model['evaluation']['strict_breach_rate'])
                reference_rates.append(ref['evaluation']['strict_breach_rate'])
            else:
                unavailable=[r for r in (model,ref) if r['status']!='COMPLETE']
                if any(r['status']=='FAILED' for r in unavailable):failed+=1
                else:unattempted+=1
                for _,reason in {(r['method'],r.get('reason') or r['status']) for r in unavailable}:
                    reasons[reason]+=1
        count=len(a)
        out=dict(phi=design['phi'][pi],phi_index=pi,
            variance_persistence=design['variance_persistence'][gi],p_index=gi,
            window=w,horizon=h,method=method,planned_repetitions=planned,
            complete_repetitions=count,failed_repetitions=failed,
            unattempted_repetitions=unattempted,conditional_on_completion=count!=planned,
            full_procedure_status='COMPLETE' if count==planned else 'NA',
            full_procedure_relative_loss_percent=None,
            method_status_counts=dict(statuses),failure_reasons=dict(reasons))
        out.update({k:None for k in ESTIMATES})
        if count:
            ma=statistics.mean(a);mb=statistics.mean(b)
            out.update(mean_model_loss=ma,mean_reference_loss=mb)
            if mb!=0:
                ratio=ma/mb
                out['relative_loss_percent']=100*(ratio-1)
                if count>1:
                    # The variance is across independent paired repetitions.
                    residual=[x-ratio*y for x,y in zip(a,b)]
                    out['relative_loss_mcse']=100*statistics.stdev(residual)/(math.sqrt(count)*mb)
            for name,values in (('model',model_rates),('reference',reference_rates)):
                out[name+'_breach_rate']=statistics.mean(values)
                if count>1:out[name+'_breach_mcse']=statistics.stdev(values)/math.sqrt(count)
            wins=sum(x<y for x,y in zip(a,b));p=wins/count
            out['win_fraction']=p
            if count>1:out['win_mcse']=math.sqrt(p*(1-p)/count)
            out['win_mcse_worst_bound']=.5/math.sqrt(count)
            if count==planned:out['full_procedure_relative_loss_percent']=out['relative_loss_percent']
        output.append(out)
    return output


def support_oracle(design,rows,method):
    selected=[r for r in rows if r['method']==method]
    expected=set(product(design['phi'],design['variance_persistence'],design['windows'],design['horizons']))
    identities=[tuple(r[k] for k in GRID) for r in selected]
    grid_complete=len(identities)==len(expected) and set(identities)==expected
    target=[];outside=[];target_clear=[];outside_clear=[];missing=[]
    target_unknown=outside_unknown=0
    for r in selected:
        location={k:r[k] for k in GRID}
        is_target=r['horizon']==6 and r['window']>=720 and r['variance_persistence']>=.9
        (target if is_target else outside).append(location)
        known=(r['complete_repetitions']==design['repetitions']
            and r['planned_repetitions']==design['repetitions']
            and r['full_procedure_status']=='COMPLETE'
            and all(finite(r.get(k)) for k in ('relative_loss_percent','relative_loss_mcse','win_fraction')))
        if not known:
            missing.append(location)
            if is_target:target_unknown+=1
            else:outside_unknown+=1
        elif r['relative_loss_percent']+2*r['relative_loss_mcse']<0 and r['win_fraction']>=.75:
            (target_clear if is_target else outside_clear).append(location)
    missing.extend(dict(zip(GRID,k)) for k in sorted(expected-set(identities)))
    if outside_clear:status='MISMATCH'
    elif not grid_complete or outside_unknown:status='INCONCLUSIVE'
    elif len(target_clear)>=6:status='SUPPORTED'
    elif len(target_clear)+target_unknown<6:status='NOT_SUPPORTED'
    else:status='INCONCLUSIVE'
    return dict(method=method,status=status,planned_cells=len(expected),reported_cells=len(selected),
        target_cell_count=len(target),outside_cell_count=len(outside),minimum_target_clear_gains=6,
        target_clear_gain_count=len(target_clear),outside_clear_gain_count=len(outside_clear),
        target_clear_gain_cells=target_clear,outside_clear_gain_cells=outside_clear,
        missing_or_unevaluable_cells=missing,all_cells_fully_evaluable=not missing and grid_complete,
        grid_complete=grid_complete,unevaluable_target_cells=target_unknown,
        unevaluable_outside_cells=outside_unknown)


def maturity_errors(rows):
    errors=[]
    for row in rows:
        identity={k:row.get(k) for k in IDENTITY}
        segments=[('evaluation',row)]
        segments.extend(('validation',c) for c in row.get('candidates',[]))
        for segment,report in segments:
            for d in report.get('fit_diagnostics',[]):
                if (type(d.get('refit_index')) is not int or type(d.get('latest_label_end')) is not int
                        or d['latest_label_end']>d['refit_index']):
                    errors.append(issue('IMMATURE_TRAINING_LABEL',identity=identity,
                        segment=segment,penalty=report.get('penalty'),diagnostic=d))
                if d.get('training_count')!=row.get('window'):
                    errors.append(issue('TRAINING_WINDOW_MISMATCH',identity=identity,segment=segment))
    return errors


def selection_errors(design,rows):
    """Read fixed menu decisions; do not run a candidate or repair a failure."""
    errors=[]
    expected_n=design['validation_last']-design['validation_first']+1
    for row in rows:
        method=row['method']; selected=row.get('selected_penalty')
        if method=='F':
            if selected is not None:errors.append(issue('REFERENCE_HAS_SELECTED_PENALTY',method=method))
            continue
        menu=design['menus'][method]; candidates=row.get('candidates',[])
        identity={k:row.get(k) for k in IDENTITY}
        if [c.get('penalty') for c in candidates]!=menu:
            errors.append(issue('CANDIDATE_MENU_MISMATCH',identity=identity));continue
        complete=[]
        for candidate in candidates:
            status=candidate.get('status')
            if status not in ('COMPLETE','FAILED','INCOMPLETE','NOT_ATTEMPTED'):
                errors.append(issue('INVALID_CANDIDATE_STATUS',identity=identity,actual=status))
            if status=='COMPLETE':
                if (candidate.get('origin_count')!=expected_n or not finite(candidate.get('mean_loss'))
                        or candidate['mean_loss']<0):
                    errors.append(issue('INVALID_COMPLETE_CANDIDATE',identity=identity,penalty=candidate.get('penalty')))
                else:complete.append(candidate)
        eligible=bool(complete) and (method=='QR4' or len(complete)==len(menu))
        expected=None
        if eligible:
            smallest=min(c['mean_loss'] for c in complete)
            tied=[c['penalty'] for c in complete if c['mean_loss']==smallest]
            expected=max(tied) if method=='QR33' else min(tied)
        # With no selected value an interrupted or failed method may have stopped
        # after validation, before its selection receipt. Completed methods cannot.
        if (selected is not None and selected!=expected
                or row['status']=='COMPLETE' and (not eligible or selected!=expected)):
            errors.append(issue('INVALID_SELECTED_PENALTY',identity=identity,method=method,
                expected=expected,actual=selected))
    return errors


def resource_oracle(design,observations):
    errors=[];unverified=[];rss=[];threads=[];elapsed=[]
    limits=design['resources']
    for record in observations:
        unit=record['unit_id']; r=record.get('peak_rss_bytes');t=record.get('maximum_observed_os_threads');e=record.get('elapsed_seconds')
        if not finite(r) or not finite(t) or not finite(e):unverified.append(unit)
        if finite(r):
            rss.append(r)
            if r>limits['public_rss_bytes']:errors.append(issue('RSS_CAP_EXCEEDED',unit_id=unit,actual=r))
        if finite(t):
            threads.append(t)
            if t>limits['maximum_observed_os_threads']:errors.append(issue('THREAD_CAP_EXCEEDED',unit_id=unit,actual=t))
        if finite(e):
            elapsed.append(e)
            if e>limits['worker_hard_wall_seconds']+TERMINATION_TOLERANCE_SECONDS:
                errors.append(issue('WORKER_WALL_EXCEEDED',unit_id=unit,actual=e))
    return dict(status='FAIL' if errors else ('UNVERIFIED' if unverified else 'PASS'),
        differences=errors,unverified_unit_ids=unverified,measured_worker_count=len(observations),
        maximum_observed_rss_bytes=max(rss,default=None),
        maximum_observed_os_threads=max(threads,default=None),
        maximum_observed_worker_wall_seconds=max(elapsed,default=None),
        termination_tolerance_seconds=TERMINATION_TOLERANCE_SECONDS,
        interpretation='Observed samples/receipts, not substituted configured resource budgets.')


def load_json(path):
    return json.loads(Path(path).read_text(),parse_constant=lambda value:(_ for _ in ()).throw(ValueError('Nonfinite JSON '+value)))


def stamp(value):
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def load_resource_observations(root,formal,errors):
    observations=[]
    for folder in sorted((formal/'units').iterdir()):
        if not folder.is_dir():continue
        start_path=folder/'parent-start.json';end_path=folder/'parent-termination.json'
        start=load_json(start_path) if start_path.exists() else {}
        end=load_json(end_path) if end_path.exists() else {}
        elapsed=(stamp(end['ended_utc'])-stamp(start['started_utc'])).total_seconds() if start and end else None
        observation=dict(unit_id=folder.name,elapsed_seconds=elapsed,
            peak_rss_bytes=None,maximum_observed_os_threads=None,source='none')
        receipt_path=folder/'worker-receipt.json'
        if receipt_path.exists():
            receipt=load_json(receipt_path);r=receipt.get('resources') or {}
            observation.update(peak_rss_bytes=r.get('peak_rss_bytes'),
                maximum_observed_os_threads=r.get('maximum_observed_os_threads'),source='worker-receipt')
            for field in ('code_hash_start','code_hash_end'):
                if receipt.get(field)!='PASS':errors.append(issue('WORKER_CODE_SEAL',unit_id=folder.name,field=field))
            if receipt.get('technical_error'):errors.append(issue('WORKER_TECHNICAL_ERROR',unit_id=folder.name))
        # A killed worker may have no final receipt. Keep only aggregate probes;
        # never copy private trace lines or absolute private paths into output.
        if observation['peak_rss_bytes'] is None or observation['maximum_observed_os_threads'] is None:
            location=start.get('private_ps_path')
            if location:
                path=Path(location)
                try:
                    path.resolve().relative_to((root/'.scratch').resolve())
                    if path.exists() and not path.is_symlink():
                        probes=[json.loads(line) for line in path.read_text().splitlines() if line.strip()]
                        observation.update(peak_rss_bytes=max((p['peak_rss_bytes'] for p in probes),default=None),
                            maximum_observed_os_threads=max((p['maximum_observed_os_threads'] for p in probes),default=None),
                            source='aggregate-checkpoint-samples')
                except (ValueError,KeyError,OSError):
                    errors.append(issue('RESOURCE_PROBE_UNREADABLE',unit_id=folder.name))
        observations.append(observation)
    return observations


def rng_receipt_errors(design,formal):
    """Compare saved states; this function never constructs an RNG."""
    errors=[];reference={}
    for path in sorted((formal/'units').glob('*/rng-receipt.json')):
        row=load_json(path);rep=row.get('rep')
        if type(rep) is not int or not 0<=rep<design['repetitions']:
            errors.append(issue('INVALID_RNG_REPETITION',unit_id=path.parent.name));continue
        if row.get('normals')!=design['burn_in']+design['retained_observations']:
            errors.append(issue('RNG_VECTOR_LENGTH_MISMATCH',unit_id=path.parent.name))
        states=(row.get('initial_state'),row.get('final_state'))
        if any(state is None for state in states):
            errors.append(issue('MISSING_RNG_STATE',unit_id=path.parent.name))
        if rep in reference and states!=reference[rep]:
            errors.append(issue('COMMON_RANDOM_STATE_MISMATCH',unit_id=path.parent.name))
        reference.setdefault(rep,states)
    return errors


def audit_bundle(root,formal):
    root=Path(root).resolve();formal=Path(formal).resolve()
    termination_path=formal/'study-termination.json'
    if not termination_path.exists():raise ValueError('STUDY_NOT_TERMINATED; audit must not inspect an in-flight run')
    termination=load_json(termination_path)
    if termination.get('all_workers_terminated') is not True:raise ValueError('STUDY_NOT_TERMINATED')
    required=('manifest.json','inventory.json','summary.json','support.json','study-termination.json')
    input_hashes={name:sha(formal/name) for name in required}
    manifest=load_json(formal/'manifest.json');design=manifest['design']
    inventory=load_json(formal/'inventory.json');summary=load_json(formal/'summary.json');support=load_json(formal/'support.json')
    errors=inventory_errors(design,inventory)+maturity_errors(inventory)+selection_errors(design,inventory)
    errors+=rng_receipt_errors(design,formal)
    for category in ('code_hashes','protocol_hashes'):
        for name,digest in manifest[category].items():
            try:
                path=root/name;path.resolve().relative_to(root)
                if path.is_symlink() or sha(path)!=digest:errors.append(issue('SOURCE_HASH_MISMATCH',category=category,path=name))
            except (OSError,ValueError):errors.append(issue('SOURCE_HASH_UNVERIFIED',category=category,path=name))
    git_errors=[];commit_time=None
    try:
        commit=manifest['design_commit']
        commit_time=subprocess.run(['git','show','-s','--format=%cI',commit],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
        if stamp(commit_time)>=stamp(manifest['started_utc']):git_errors.append(issue('DESIGN_NOT_BEFORE_RUN'))
        for name,digest in manifest['protocol_hashes'].items():
            frozen=subprocess.run(['git','show',commit+':'+name],cwd=root,capture_output=True,check=True).stdout
            if hashlib.sha256(frozen).hexdigest()!=digest:git_errors.append(issue('DESIGN_COMMIT_HASH_MISMATCH',path=name))
        protocol_json=next(name for name in manifest['protocol_hashes'] if name.endswith('.json'))
        if load_json(root/protocol_json)!=design:git_errors.append(issue('MANIFEST_DESIGN_MISMATCH'))
    except (OSError,ValueError,KeyError,StopIteration,subprocess.SubprocessError):git_errors.append(issue('DESIGN_COMMIT_UNVERIFIED'))
    errors+=git_errors
    counts=Counter(r.get('status') for r in inventory)
    if dict(counts)!=termination.get('method_status_counts'):errors.append(issue('TERMINATION_METHOD_COUNTS_MISMATCH'))
    if summary.get('source_inventory_sha256')!=input_hashes['inventory.json']:errors.append(issue('SUMMARY_SOURCE_HASH_MISMATCH'))
    if summary.get('study_status')!=termination.get('status'):errors.append(issue('SUMMARY_STUDY_STATUS_MISMATCH'))
    expected=paired_oracle(design,inventory) if not inventory_errors(design,inventory) else []
    actual=summary.get('cells',[]);index={tuple(r[k] for k in CELL):r for r in actual}
    expected_keys={tuple(r[k] for k in CELL) for r in expected}
    if len(index)!=len(actual) or set(index)!=expected_keys:errors.append(issue('SUMMARY_GRID_MISMATCH',actual=len(actual),expected=len(expected)))
    for row in expected:
        key=tuple(row[k] for k in CELL);reported=index.get(key,{})
        for name,value in row.items():
            if not same_value(reported.get(name),value):errors.append(issue('SUMMARY_VALUE_MISMATCH',cell=list(key),field=name,expected=value,actual=reported.get(name)))
    screens={}
    if expected:
        for method in ('QR33','QR4'):
            screens[method]=support_oracle(design,expected,method)
            reported=support.get('procedures',{}).get(method,{})
            for name,value in screens[method].items():
                if not same_value(reported.get(name),value):errors.append(issue('SUPPORT_VALUE_MISMATCH',method=method,field=name,expected=value,actual=reported.get(name)))
        statuses=[s['status'] for s in screens.values()]
        broad=('MISMATCH' if 'MISMATCH' in statuses else 'INCONCLUSIVE' if 'INCONCLUSIVE' in statuses
            else 'SUPPORTED' if all(s=='SUPPORTED' for s in statuses) else 'NOT_SUPPORTED')
        if support.get('broad_conditional_models_restriction')!=broad:errors.append(issue('BROAD_SUPPORT_MISMATCH',expected=broad))
    observations=load_resource_observations(root,formal,errors)
    resources=resource_oracle(design,observations);errors+=resources['differences']
    if len(observations)!=termination.get('attempted_workers'):errors.append(issue('ATTEMPTED_WORKER_COUNT_MISMATCH'))
    completed_parents=sum(load_json(p).get('status')=='COMPLETE' for p in (formal/'units').glob('*/parent-termination.json'))
    if completed_parents!=termination.get('completed_workers'):errors.append(issue('COMPLETED_WORKER_COUNT_MISMATCH'))
    actual_wall=termination.get('elapsed_seconds')
    if not finite(actual_wall) or actual_wall>design['resources']['total_study_wall_seconds']+TERMINATION_TOLERANCE_SECONDS:
        errors.append(issue('STUDY_WALL_EXCEEDED_OR_UNVERIFIED',actual=actual_wall))
    if termination.get('code_hash_check')!='PASS':errors.append(issue('TERMINATION_SEAL_NOT_PASS'))
    input_changed=[name for name,digest in input_hashes.items() if sha(formal/name)!=digest]
    if input_changed:errors.append(issue('INPUT_CHANGED_DURING_AUDIT',files=input_changed))
    return dict(schema='independent-wp3-audit-1',audited_utc=datetime.now(timezone.utc).isoformat(),
        status='FAIL' if errors else ('UNVERIFIED' if resources['status']=='UNVERIFIED' else 'PASS'),
        scope='Independent scalar arithmetic/provenance/resource readback; not independent study replication.',
        analysis_performed='No draws, forecasts, refits, model tuning or new statistical tests.',
        input_hashes=input_hashes,design_commit=manifest['design_commit'],design_commit_time=commit_time,
        design_before_run=not git_errors,planned_inventory_count=len(inventory_keys(design)),
        actual_inventory_count=len(inventory),summary_cell_count=len(actual),
        paired_summary_values_checked=sum(len(row) for row in expected),
        method_status_counts=dict(counts),study_process_status=termination.get('status'),
        process_completion_is_not_method_success=True,support=screens,
        resources=resources,study_elapsed_seconds=actual_wall,
        differences=errors,difference_count=len(errors))


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--formal',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    root=args.root.resolve();formal=args.formal or root/'results/revision-v8/wp3'
    output=args.output.absolute()
    output.resolve().relative_to(root)
    if any(p.is_symlink() for p in (output,*output.parents)):raise ValueError('OUTPUT_SYMLINK')
    if output.exists():raise FileExistsError('Exclusive audit output already exists')
    result=audit_bundle(root,formal)
    with output.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:result[k] for k in ('status','difference_count','actual_inventory_count','summary_cell_count','method_status_counts')}))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
