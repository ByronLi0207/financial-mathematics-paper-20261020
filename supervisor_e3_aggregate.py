"""Aggregate all declared E3 cells without changing forecasts or archives."""
import sys
sys.dont_write_bytecode=True
import csv
import io
import json
import math
from pathlib import Path
import numpy as np
import supervisor_e3 as e3
from inference_tests import dm_test,holm
from supervisor_inference_audit import load_traces,independent_dm


def output(name,rows):
    fields=list(dict.fromkeys(key for row in rows for key in row))
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields)
    writer.writeheader();writer.writerows(rows)
    (e3.PUBLIC/name).write_text(stream.getvalue())


def mean(trace):return math.fsum(map(float,trace['pinball']))/len(trace['pinball'])


def paired_row(source,horizon,old_window,new_window,old_name,new_name,old,new):
    row=dict(source=source,horizon=horizon,old_window=old_window,new_window=new_window,
             old_method=old_name,new_method=new_name,direction='new_minus_old',post_result_exploratory=True)
    if old is None or new is None:return dict(row,status='MISSING_COMPLETE_TRACE')
    difference=e3.paired_loss_difference(old,new)
    base=dm_test(difference,horizon);wide=dm_test(difference,horizon,min(len(difference)-1,2*base['bandwidth']))
    for record in (base,wide):
        oracle=independent_dm(difference,horizon,record['bandwidth'])
        for got,want in zip((record['mean_difference'],record['lrv'],record['dm_t'],record['dm_p']),oracle):
            if got is None or want is None:
                if got is not want:raise ValueError('DM independent null mismatch')
            elif not math.isclose(got,want,rel_tol=3e-10,abs_tol=1e-11):
                raise ValueError('DM independent scalar oracle mismatch')
    old_mean,new_mean=mean(old),mean(new)
    row.update(status=base['status'],n=len(difference),old_mean_pinball=old_mean,new_mean_pinball=new_mean,
               relative_percent=100*(new_mean-old_mean)/old_mean,
               old_breaches=int(np.count_nonzero(old['peak']>old['capacity'])),
               new_breaches=int(np.count_nonzero(new['peak']>new['capacity'])))
    row.update({key:value for key,value in base.items() if key not in ('n','horizon','status')})
    row.update({'sensitivity_2L_'+key:value for key,value in wide.items()
                if key in ('bandwidth','dm_t','dm_p','hln_t','hln_p','lrv','status')})
    return row


def main():
    original=load_traces(e3.PRIOR)
    archived=list(csv.DictReader((e3.ROOT/'results/revision-20261022/evaluation-summary.csv').open()))
    summary=[];candidates=[];convergence=[];records={};new={};four={};checks=[]
    for s,h,w in e3.CELLS:
        identity=e3.cell_id(s,h,w);path=e3.PUBLIC/identity/'result.json'
        record=json.loads(path.read_text());records[s,h,w]=record
        prior_row=next(row for row in archived if row['source']==s and int(row['horizon'])==h
                       and int(row['window'])==w and row['method']=='QR')
        f=original[s,h,w,'frozen_F'];q=original[s,h,w,'QR']
        base=dict(source=s,horizon=h,window=w,status=record['status'],
            original33_selected_penalty=float(prior_row['parameter']),
            extended33_selected_penalty=record['selected_penalty'],
            four_selected_penalty=record.get('four_predictor_archive',{}).get('selected_penalty'),
            original33_mean_pinball=mean(q),frozen_F_mean_pinball=mean(f))
        if record['status']=='COMPLETE':
            trace=e3.checked_trace(e3.PRIVATE/identity/'numeric-traces.npz',q['origins'],q['peak'],record['evaluation']['mean_pinball'])
            reduced=e3.checked_trace(e3.PRIVATE/identity/'four-predictor-traces.npz',q['origins'],q['peak'],record['four_predictor_archive']['evaluation']['mean_pinball'])
            new[s,h,w]=trace;four[s,h,w]=reduced
            base.update(extended33_mean_pinball=mean(trace),four_mean_pinball=mean(reduced),
                original33_percent_vs_frozen_F=100*(mean(q)-mean(f))/mean(f),
                extended33_percent_vs_frozen_F=100*(mean(trace)-mean(f))/mean(f),
                four_percent_vs_frozen_F=100*(mean(reduced)-mean(f))/mean(f),
                menu_change_percent=100*(mean(trace)-mean(q))/mean(q),
                common_menu_feature_change_percent=100*(mean(trace)-mean(reduced))/mean(reduced),
                original33_breaches=int(np.count_nonzero(q['peak']>q['capacity'])),
                frozen_F_breaches=int(np.count_nonzero(f['peak']>f['capacity'])),
                extended33_breaches=record['evaluation']['strict_breach_count'],
                four_breaches=record['four_predictor_archive']['evaluation']['strict_breach_count'],
                elapsed_seconds=record['resources']['final_elapsed_seconds'],
                peak_rss_bytes=record['resources']['peak_rss_bytes'],
                maximum_observed_os_threads=record['resources']['maximum_observed_os_threads'])
            if record['selected_penalty']==float(prior_row['parameter']):
                equal=all(np.array_equal(trace[key],q[key]) for key in ('origins','capacity','peak','pinball'))
                if not equal:raise ValueError('unchanged selected penalty did not reproduce original QR exactly')
                checks.append(dict(cell=identity,check='same_selected_lambda_original_trace_exact',status='PASS'))
        summary.append(base)
        for row in record['candidates']:
            diagnostics=row.get('fit_diagnostics',[])
            candidates.append(dict(source=s,horizon=h,window=w,parameter=row['parameter'],status=row['status'],
                origin_count=row.get('origin_count'),mean_pinball=row.get('mean_pinball'),reason=row.get('reason'),
                elapsed_seconds=row.get('elapsed_seconds'),refit_count=len(diagnostics)))
            if diagnostics:convergence.append(convergence_row(s,h,w,'validation',row['parameter'],diagnostics))
        if record.get('fit_diagnostics'):
            convergence.append(convergence_row(s,h,w,'evaluation',record['selected_penalty'],record['fit_diagnostics']))
    comparisons=[]
    for s,h,w in e3.CELLS:
        comparisons.extend([
            paired_row(s,h,w,w,'frozen_F','four_predictor_extended_menu',original[s,h,w,'frozen_F'],four.get((s,h,w))),
            paired_row(s,h,w,w,'four_predictor_extended_menu','33_predictor_extended_menu',four.get((s,h,w)),new.get((s,h,w))),
            paired_row(s,h,w,w,'33_predictor_original_menu','33_predictor_extended_menu',original[s,h,w,'QR'],new.get((s,h,w)))])
    for h in (6,24):
        comparisons.extend([
            paired_row('fx_hourly',h,720,720,'rolling_F','frozen_F',original['fx_hourly',h,720,'rolling_F'],original['fx_hourly',h,720,'frozen_F']),
            paired_row('fx_hourly',h,720,2880,'frozen_F','frozen_F',original['fx_hourly',h,720,'frozen_F'],original['fx_hourly',h,2880,'frozen_F'])])
    if len(comparisons)!=28:raise ValueError('declared E3 contrast family mismatch')
    for key in ('dm_p','hln_p','sensitivity_2L_dm_p','sensitivity_2L_hln_p'):
        # All28 belong to the declared family. Unidentified/identical contrasts
        # take1 for adjustment; their raw null and explicit status are retained.
        adjusted=holm([row.get(key) if row.get(key) is not None else 1. for row in comparisons])
        for row,value in zip(comparisons,adjusted):row[key+'_holm_e3_28']=float(value)
    output('summary.csv',summary);output('validation-menu.csv',candidates)
    output('convergence-summary.csv',convergence);output('paired-dm.csv',comparisons)
    primary=[]
    def step(s,h,ow,nw,old,new,label,number,reverse=False):
        found=next(row for row in comparisons if (row['source'],row['horizon'],row['old_window'],row['new_window'],
                   row['old_method'],row['new_method'])==(s,h,ow,nw,old,new))
        row=dict(found,step=number,component=label)
        if reverse:
            row.update(old_method=found['new_method'],new_method=found['old_method'],
                       old_mean_pinball=found['new_mean_pinball'],new_mean_pinball=found['old_mean_pinball'],
                       old_breaches=found['new_breaches'],new_breaches=found['old_breaches'])
            row['relative_percent']=100*(row['new_mean_pinball']-row['old_mean_pinball'])/row['old_mean_pinball']
            for key in ('mean_difference','dm_t','hln_t','sensitivity_2L_dm_t','sensitivity_2L_hln_t'):
                if row.get(key) is not None:row[key]=-row[key]
            row['orientation_note']='same declared test reversed for display; no additional test'
        primary.append(row)
    step('fx_hourly',6,720,720,'rolling_F','frozen_F','update schedule',1)
    step('fx_hourly',6,720,2880,'frozen_F','frozen_F','history length',2)
    step('fx_hourly',6,2880,2880,'frozen_F','four_predictor_extended_menu','four-predictor QR',3)
    step('fx_hourly',6,2880,2880,'four_predictor_extended_menu','33_predictor_extended_menu','feature specification under common menu',4)
    step('fx_hourly',6,2880,2880,'33_predictor_original_menu','33_predictor_extended_menu','contract ridge menu back to archived primary',5,reverse=True)
    step('nyfed_weekly',6,260,260,'frozen_F','four_predictor_extended_menu','four-predictor QR',1)
    step('nyfed_weekly',6,260,260,'four_predictor_extended_menu','33_predictor_extended_menu','feature specification under common menu',2)
    step('nyfed_weekly',6,260,260,'33_predictor_original_menu','33_predictor_extended_menu','contract ridge menu back to archived primary',3,reverse=True)
    for s in ('fx_hourly','nyfed_weekly'):
        chain=[row for row in primary if row['source']==s];initial=chain[0]['old_mean_pinball']
        for row in chain:row['percentage_points_of_initial_loss']=100*(row['new_mean_pinball']-row['old_mean_pinball'])/initial
        total=100*(chain[-1]['new_mean_pinball']-initial)/initial
        if not math.isclose(sum(row['percentage_points_of_initial_loss'] for row in chain),total,abs_tol=1e-12):
            raise ValueError('primary ordered accounting did not close')
    output('primary-decomposition.csv',primary)
    e3.dump(e3.PUBLIC/'aggregate.json',dict(post_result_exploratory=True,summary=summary,paired_comparisons=comparisons))
    e3.dump(e3.PUBLIC/'verification.json',dict(status='PASS',cell_count=len(records),
        complete_cells=sum(row['status']=='COMPLETE' for row in summary),declared_candidate_count=len(candidates),
        candidate_status_counts={status:sum(row['status']==status for row in candidates) for status in ('COMPLETE','FAILED','INCOMPLETE')},
        paired_comparison_count=len(comparisons),independent_scalar_DM_checks=56,
        trace_checks='all evaluation origins, peaks, per-origin pinball and aggregate means reconciled; four-feature originals verified read-only',
        unchanged_parameter_checks=checks,original_code_hash_agreement={name:e3.sha(e3.ROOT/name)==e3.sha(e3.PRIOR/name) for name in e3.CODE_FILES[1:]},
        executed_runner_snapshot_sha256=e3.sha(e3.PRIVATE/'supervisor_e3-run-start.py'),
        per_cell_runner_hash_matches_snapshot=all(record['code_hashes']['supervisor_e3.py']==e3.sha(e3.PRIVATE/'supervisor_e3-run-start.py') for record in records.values())))
    print(json.dumps(summary,indent=2))


def convergence_row(s,h,w,phase,parameter,details):
    for row in details:
        if (row['iterations']>10000 or row['duality_gap']>row['gap_tolerance']
                or row['primal_residual']>row['primal_tolerance'] or row['dual_residual']>row['dual_tolerance']
                or row['latest_label_end']>row['refit_index']):
            raise ValueError('accepted fit certificate/maturity failed reconciliation')
    return dict(source=s,horizon=h,window=w,phase=phase,parameter=parameter,refit_count=len(details),
        minimum_iterations=min(row['iterations'] for row in details),maximum_iterations=max(row['iterations'] for row in details),
        total_iterations=sum(row['iterations'] for row in details),
        maximum_gap_fraction=max(row['duality_gap']/row['gap_tolerance'] for row in details),
        maximum_primal_fraction=max(row['primal_residual']/row['primal_tolerance'] for row in details),
        maximum_dual_fraction=max(row['dual_residual']/row['dual_tolerance'] for row in details),
        latest_label_maturity='PASS')


if __name__=='__main__':main()
