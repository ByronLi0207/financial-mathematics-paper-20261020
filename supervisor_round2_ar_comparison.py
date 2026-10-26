"""W4 arithmetic readback of eight archived AR cells; no fitting or inference."""
import csv
import hashlib
import io
import json
import math
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results/supervisor-20261023/w4'
INPUTS={
    'ar_summary':'results/revision-20261022/ar1-replay/ar1-summary.csv',
    'ar_paired':'results/revision-20261022/ar1-replay/ar1-paired.csv',
    'original_summary':'results/revision-20261022/evaluation-summary.csv',
    'extended_summary':'results/supervisor-20261023/e3/summary.csv',
    'study_spec':'protocol/revision-20261022/study-spec.json',
}


def readcsv(name):
    with (ROOT/INPUTS[name]).open(newline='') as stream:return list(csv.DictReader(stream))


def key(row):return row['source'],int(row['horizon']),int(row['window'])


def value(row,name):
    number=float(row[name])
    if not math.isfinite(number):raise ValueError('nonfinite archived value')
    return number


def same(left,right):
    if not math.isclose(left,right,rel_tol=2e-14,abs_tol=1e-12):raise ValueError('archived aggregates differ')


def counts(rows,reference):
    losses=[r[f'AR_percent_vs_{reference}'] for r in rows]
    breaches=[r[f'AR_breaches_minus_{reference}'] for r in rows]
    return dict(cells=len(rows),lower_loss=sum(x<0 for x in losses),equal_loss=sum(x==0 for x in losses),
                higher_loss=sum(x>0 for x in losses),fewer_breaches=sum(x<0 for x in breaches),
                equal_breaches=sum(x==0 for x in breaches),more_breaches=sum(x>0 for x in breaches))


def run():
    ar=readcsv('ar_summary');paired=readcsv('ar_paired');original=readcsv('original_summary');extended=readcsv('extended_summary')
    spec=json.loads((ROOT/INPUTS['study_spec']).read_text())
    assert len(ar)==len(extended)==8 and len(paired)==24
    expected={(s,h,w) for s,cfg in spec['sources'].items() for h in (6,24) for w in cfg['windows']}
    assert len(expected)==8 and {key(r) for r in ar}=={key(r) for r in extended}==expected
    assert len({key(r) for r in ar})==len(ar) and len({key(r) for r in extended})==len(extended)
    original_index={(key(r),r['method']):r for r in original}
    assert len(original_index)==len(original)
    paired_index={(key(r),r['right_method']):r for r in paired}
    assert len(paired_index)==len(paired)
    extended_index={key(r):r for r in extended}
    inputs=list(INPUTS.values());rows=[];reconciled=0
    for a in ar:
        source,h,w=key(a);cfg=spec['sources'][source];n=cfg['evaluation_origin_last']-cfg['evaluation_origin_first']+1
        e=extended_index[(source,h,w)]
        assert a['status']==e['status']=='COMPLETE' and a['method']=='AR1_REPLAY'
        assert int(a['expected_origin_count'])==int(a['completed_origin_count'])==int(a['origin_count'])==n
        assert int(a['refit_step'])==cfg['refit_step'] and a['native_unit']==cfg['native_unit']
        result_path=f'results/supervisor-20261023/e3/{source}-h{h}-w{w}/result.json'
        inputs.append(result_path);result=json.loads((ROOT/result_path).read_text())
        assert result['status']=='COMPLETE' and result['source']==source and result['horizon']==h and result['window']==w
        assert result['evaluation']['origin_count']==n and result['date_ranges']['evaluation']['count']==n
        same(value(e,'extended33_mean_pinball'),result['evaluation']['mean_pinball'])
        assert int(e['extended33_breaches'])==result['evaluation']['strict_breach_count']
        row=dict(source=source,native_unit=a['native_unit'],horizon=h,window=w,origin_count=n,
                 first_source_index=cfg['evaluation_origin_first'],last_source_index=cfg['evaluation_origin_last'],
                 AR_mean_pinball=value(a,'mean_pinball'),AR_strict_breach_count=int(a['strict_breach_count']),
                 source_primary_cell=h==cfg['primary_contrast']['horizon'] and w==cfg['primary_window'])
        assert 0<=row['AR_strict_breach_count']<=n and row['AR_mean_pinball']>=0
        for reference,method,ecol,bcol in [('F','frozen_F','frozen_F_mean_pinball','frozen_F_breaches'),
                ('S','frozen_S',None,None),('original_QR33','QR','original33_mean_pinball','original33_breaches')]:
            baseline=original_index[((source,h,w),method)];pair=paired_index[((source,h,w),method)]
            assert int(baseline['origin_count'])==int(pair['origin_count'])==n
            assert int(baseline['refit_step'])==int(pair['refit_step'])==cfg['refit_step']
            assert baseline['native_unit']==pair['native_unit']==a['native_unit']
            assert pair['status']=='COMPLETE' and pair['left_method']=='AR1_REPLAY'
            assert int(pair['first_source_index'])==row['first_source_index'] and int(pair['last_source_index'])==row['last_source_index']
            loss=value(baseline,'mean_pinball');breaches=int(baseline['strict_breach_count']);assert loss>0 and 0<=breaches<=n
            same(row['AR_mean_pinball'],value(pair,'mean_pinball_left'));same(loss,value(pair,'mean_pinball_right'))
            assert int(pair['strict_breach_count_left'])==row['AR_strict_breach_count'] and int(pair['strict_breach_count_right'])==breaches
            percent=100*(row['AR_mean_pinball']-loss)/loss
            same(percent,value(pair,'relative_mean_loss_difference_percent'))
            if ecol:same(loss,value(e,ecol));assert breaches==int(e[bcol])
            row.update({reference+'_mean_pinball':loss,reference+'_strict_breach_count':breaches,
                        'AR_percent_vs_'+reference:percent,'AR_breaches_minus_'+reference:row['AR_strict_breach_count']-breaches})
            reconciled+=1
        loss=value(e,'extended33_mean_pinball');breaches=int(e['extended33_breaches']);assert loss>0 and 0<=breaches<=n
        row.update(QR33_plus_mean_pinball=loss,QR33_plus_strict_breach_count=breaches,
                   AR_percent_vs_QR33_plus=100*(row['AR_mean_pinball']-loss)/loss,
                   AR_breaches_minus_QR33_plus=row['AR_strict_breach_count']-breaches)
        rows.append(row)
    OUT.mkdir(parents=True,exist_ok=False)
    text=io.StringIO(newline='');writer=csv.DictWriter(text,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'ar-comparison.csv').write_text(text.getvalue())
    digest=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
    references=('F','S','original_QR33','QR33_plus')
    report=dict(status='PASS',created_utc=datetime.now(timezone.utc).isoformat(),post_result_exploratory=True,
        formula='100 * (AR mean pinball - reference mean pinball) / reference mean pinball; negative favors AR',
        breach_difference='AR strict breach count minus reference strict breach count',
        comparison_scope='Matched source/H/W/refit and original evaluation origins. Source-primary cell denotes the cell only; FX original primary reference is a different-window rolling F.',
        checks=dict(retained_all_eight_cells=True,finite_losses=True,matching_origin_counts_and_paired_bounds=True,
             matching_refit_steps_and_units=True,original_paired_rows_reconciled=reconciled,
             extended_summary_reconciled_with_eight_terminal_results=True,no_new_fit=True,no_inference=True,
             scope='Aggregate CSV/JSON alignment readback; no new per-origin replay or raw data analysis.'),
        counts_all={reference:counts(rows,reference) for reference in references},
        counts_by_source={s:{reference:counts([r for r in rows if r['source']==s],reference) for reference in references} for s in spec['sources']},
        primary_cells=[r for r in rows if r['source_primary_cell']],
        input_sha256={p:digest(p) for p in inputs},script_sha256=digest(Path(__file__).relative_to(ROOT)),
        output_csv_sha256=hashlib.sha256((OUT/'ar-comparison.csv').read_bytes()).hexdigest(),rows=rows)
    with (OUT/'ar-comparison.json').open('x') as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('rows','input_sha256')},indent=2))


if __name__=='__main__':run()
