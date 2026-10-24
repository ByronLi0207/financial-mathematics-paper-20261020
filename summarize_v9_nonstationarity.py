"""Read-only saved-archive report; never imports a study or fitting module.

Usage: python summarize_v9_nonstationarity.py /path/to/results/v9/nonstationarity
The five registered input JSON files are read once. New analysis/ is created
exclusively; existing reports are never overwritten. No repair/rerun is done.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import median


INPUT_FILES = ('diagnostics.json', 'summary.json', 'predictions.json',
               'formal/replicate-scores.json', 'manifest.json')
ARMS = ('constant', 'switching')
WINDOWS = (52, 260)


class ArchiveError(ValueError):
    """The saved archive does not support an internally consistent report."""


def _number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def _quantile(values, probability):
    ordered = sorted(values)
    position = (len(ordered)-1)*probability
    first = int(math.floor(position))
    return float(ordered[first] + (ordered[min(first+1, len(ordered)-1)]-ordered[first])*(position-first))


def _same(a, b):
    if a is None or b is None:
        return a is b
    return _number(a) and _number(b) and math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10)


def _holm(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    adjusted, running = [1.]*len(values), 0.
    for rank, index in enumerate(order):
        running = max(running, (len(values)-rank)*values[index])
        adjusted[index] = min(1., running)
    return adjusted


def _raw_p(row):
    p = row.get('p_value')
    if p is None:
        return None
    if (not _number(p) or not 0 <= p <= 1 or row.get('status') != 'COMPLETE'
            or row.get('moment', {}).get('qualified') is not True):
        raise ArchiveError('DIAGNOSTIC_PRIMARY_P_WITHOUT_QUALIFIED_COMPLETE_NULL:'+row['source_id'])
    return float(p)


def _diagnostic_rows(diagnostics, sources):
    allowed = {r['source_id'] for r in sources}
    indexed = {}
    for row in diagnostics:
        key = row.get('source_id')
        if key not in allowed or key in indexed:
            raise ArchiveError('DIAGNOSTIC_SOURCE_INVENTORY')
        indexed[key] = row
    rows = []
    for source in sources:
        key = source['source_id']
        row = indexed.get(key, dict(source_id=key, status='NOT_ARCHIVED', p_value=None))
        p = _raw_p(row)
        partition = row.get('partition')
        n = row.get('n', source.get('stop'))
        if not isinstance(n, int) or n < 2:
            raise ArchiveError('DIAGNOSTIC_N_UNAVAILABLE:'+key)
        cuts = None if not isinstance(partition, dict) else partition.get('cuts')
        lengths = None if partition is None else partition.get('segment_lengths')
        if cuts is not None:
            if (not isinstance(cuts, list) or any(not isinstance(k, int) for k in cuts)
                    or cuts != sorted(set(cuts)) or any(k <= 0 or k >= n-1 for k in cuts)):
                raise ArchiveError('DIAGNOSTIC_INVALID_CUTS:'+key)
            expected_lengths = [b-a for a,b in zip([0,*cuts], [*cuts,n-1])]
            if lengths != expected_lengths:
                raise ArchiveError('DIAGNOSTIC_SEGMENT_CENSUS:'+key)
        failures = []
        if row.get('reason'):
            failures.append(str(row['reason']))
        if row.get('partition_failure'):
            failures.append('PARTITION:'+str(row['partition_failure'].get('reason', 'FAILED')))
        if row.get('calibration_status', '').startswith('FAILED'):
            failures.append(row['calibration_status'])
        for index, fit in enumerate(row.get('segment_fits', [])):
            if fit.get('reason'):
                failures.append('SEGMENT_'+str(index)+':'+str(fit['reason']))
        break_dates = row.get('break_dates', [])
        if cuts and len(break_dates) != len(cuts):
            failures.append('BREAK_DATES_NOT_ARCHIVED')
            break_dates = []
        moment = row.get('moment') or {}
        null_fit = row.get('whole_fit') or {}
        null_diagnostics = null_fit.get('diagnostics') or {}
        rows.append(dict(source_id=key, kind=source['kind'], n=n, M=n-1,
                         first_time=row.get('first_time'), last_time=row.get('last_time'),
                         status=row.get('status','NOT_ARCHIVED'), statistic=row.get('statistic'),
                         p_value=p, holm13_p=None, holm_internal_placeholder=False,
                         moment_qualified=moment.get('qualified'), nu_gt4=moment.get('nu_gt4'),
                         kappa=moment.get('kappa'), q4=moment.get('q4'),
                         null_boundary_status=null_diagnostics.get('status'),
                         boundary_hits=null_diagnostics.get('boundary_hits'),
                         calibration_status=row.get('calibration_status'),
                         selected_breaks=None if cuts is None else len(cuts), cuts=cuts,
                         break_dates=break_dates, segment_lengths=lengths,
                         min_segment=None if partition is None else partition.get('min_segment'),
                         cap_reached=None if partition is None else partition.get('cap_reached'),
                         global_interpretation='不可评估' if p is None else '拒绝固定模型稳定性' if p<=.05 else '未拒绝固定模型稳定性',
                         failures=failures))
    weekly = [r for r in rows if r['kind']=='weekly']
    adjusted = _holm([1. if r['p_value'] is None else r['p_value'] for r in weekly])
    for row, value in zip(weekly, adjusted):
        row['holm13_p'] = None if row['p_value'] is None else value
        row['holm_internal_placeholder'] = row['p_value'] is None
    return rows


def _key(row):
    return row.get('source_id'), row.get('arm'), row.get('window'), row.get('method')


def _simulation_rows(summary, records, sources):
    ids = [r['source_id'] for r in sources if r['kind']=='weekly']
    methods = sorted({r.get('method') for r in summary})
    if methods not in [['QR33'], ['QR33','QR4']]:
        raise ArchiveError('SUMMARY_CONDITIONAL_METHOD_INVENTORY')
    required = {r.get('required_repetitions') for r in summary}
    if len(required)!=1 or not isinstance(next(iter(required)),int) or next(iter(required))<1:
        raise ArchiveError('SUMMARY_REPETITION_INVENTORY')
    R = next(iter(required))
    expected = list(itertools.product(ids, ARMS, WINDOWS, methods))
    allowed, indexed, grouped = set(expected), {}, {k: [] for k in expected}
    for row in summary:
        key = _key(row)
        if key not in allowed or key in indexed:
            raise ArchiveError('SUMMARY_CELL_INVENTORY')
        indexed[key] = row
    for row in records:
        key = _key(row)
        if key not in grouped:
            raise ArchiveError('REPLICATE_CELL_INVENTORY')
        grouped[key].append(row)
    rows = []
    for key in expected:
        archived = indexed.get(key)
        rep_rows = grouped[key]
        valid = [r for r in rep_rows if r.get('status')=='COMPLETE' and r.get('n')==72
                 and _number(r.get('f_mean_loss')) and r['f_mean_loss']>0
                 and _number(r.get('qr_mean_loss'))]
        complete = (len(rep_rows)==R and len(valid)==R
                    and sorted(r.get('rep') for r in rep_rows)==list(range(R)))
        values = [100*(r['qr_mean_loss']/r['f_mean_loss']-1) for r in valid]
        if not all(_number(v) for v in values):
            complete = False
        derived = dict(relative_median_pct=None, q25_pct=None, q75_pct=None,
                       win_fraction=None, qr_breach_median=None, f_breach_median=None)
        if complete:
            if any(not isinstance(r.get(k), int) or not 0<=r[k]<=72 for r in valid for k in ['qr_breaches','f_breaches']):
                raise ArchiveError('REPLICATE_BREACH_CENSUS:'+str(key))
            derived.update(relative_median_pct=float(median(values)),q25_pct=_quantile(values,.25),q75_pct=_quantile(values,.75),
                           win_fraction=sum(r['qr_mean_loss']<r['f_mean_loss'] for r in valid)/R,
                           qr_breach_median=float(median(r['qr_breaches']/72 for r in valid)),
                           f_breach_median=float(median(r['f_breaches']/72 for r in valid)))
        if archived is not None:
            if complete != (archived.get('status')=='COMPLETE'):
                raise ArchiveError('SUMMARY_STATUS_DISAGREEMENT:'+str(key))
            for field, value in derived.items():
                if not _same(archived.get(field),value):
                    raise ArchiveError('SUMMARY_FIELD_DISAGREEMENT:'+str(key)+':'+field)
            if archived.get('completed_repetitions')!=len(valid):
                raise ArchiveError('SUMMARY_COMPLETION_COUNT_DISAGREEMENT:'+str(key))
        source, arm, window, method = key
        rows.append(dict(source_id=source,arm=arm,window=window,method=method,
                         status='MISSING' if archived is None else archived['status'],
                         required_repetitions=R,completed_repetitions=len(valid),
                         failed_repetitions=[r for r in range(R) if not any(x.get('rep')==r for x in valid)],
                         **derived,
                         archived_summary_present=archived is not None,
                         completed_rep_description_median_pct=float(median(values)) if values else None,
                         partial_description_only=not complete or archived is None,
                         failure_reasons=sorted({str(r.get(k)) for r in rep_rows for k in ['qr_reason','f_reason'] if r.get(k)})))
    return rows, R, methods


def _across_source(cells, sources):
    ids = [r['source_id'] for r in sources if r['kind']=='weekly']
    rows=[]
    for arm, window in itertools.product(ARMS,WINDOWS):
        selected=[r for r in cells if r['arm']==arm and r['window']==window and r['method']=='QR33']
        complete=[r for r in selected if r['status']=='COMPLETE' and r['relative_median_pct'] is not None]
        values=[r['relative_median_pct'] for r in complete]
        full=len(complete)==len(ids)==13
        rows.append(dict(arm=arm,window=window,method='QR33',status='COMPLETE' if full else 'UNASSESSABLE',
                         required_sources=13,complete_sources=len(complete),
                         median_pct=float(median(values)) if full else None,
                         q25_pct=_quantile(values,.25) if full else None,q75_pct=_quantile(values,.75) if full else None,
                         completed_only_median_pct=float(median(values)) if values else None,
                         completed_only_q25_pct=_quantile(values,.25) if values else None,
                         completed_only_q75_pct=_quantile(values,.75) if values else None,
                         missing_sources=[s for s in ids if s not in {r['source_id'] for r in complete}]))
    return rows


def _predictions(diagnostics, across, manifest):
    weekly=[r for r in diagnostics if r['kind']=='weekly']
    known=sum(r['p_value'] is not None and r['p_value']<=.05 for r in weekly)
    unknown=sum(r['p_value'] is None for r in weekly)
    n1='SUPPORTED' if known>=7 else 'NOT_SUPPORTED' if known+unknown<7 else 'UNASSESSABLE'
    get=lambda arm,w:next(r['median_pct'] for r in across if r['arm']==arm and r['window']==w)
    a,b,c=get('switching',52),get('switching',260),get('constant',52)
    result=dict(N1=dict(status=n1,known_rejections=known,maximum_rejections=known+unknown,unknown=unknown,family_size=13,
                        holm_rejections=sum(r['holm13_p'] is not None and r['holm13_p']<=.05 for r in weekly)),
                N2=dict(status='UNASSESSABLE' if a is None or b is None else 'SUPPORTED' if a>5 and b>5 else 'NOT_SUPPORTED',switching_W52_median_pct=a,switching_W260_median_pct=b),
                N3=dict(status='UNASSESSABLE' if c is None else 'SUPPORTED' if -3<=c<=3 else 'NOT_SUPPORTED',constant_W52_median_pct=c))
    daily=next(r for r in diagnostics if r['kind']=='daily');hourly=next(r for r in diagnostics if r['kind']=='hourly')
    design=manifest.get('design',{})
    first=design.get('fx_common_calendar_start');stop=design.get('fx_common_calendar_stop_exclusive')
    if first is None or stop is None:
        raise ArchiveError('COMMON_CALENDAR_NOT_ARCHIVED')
    seconds=(datetime.fromisoformat(stop)-datetime.fromisoformat(first)).total_seconds()
    if seconds<=0:
        raise ArchiveError('INVALID_COMMON_CALENDAR')
    years=seconds/(365.2425*86400)
    valid=all(r['p_value'] is not None and r['cuts'] is not None for r in [daily,hourly])
    dd=None if daily['cuts'] is None else 100*len(daily['cuts'])/daily['n']
    hd=None if hourly['cuts'] is None else 100*len(hourly['cuts'])/hourly['n']
    result['N4']=dict(status='UNASSESSABLE' if not valid else 'SUPPORTED' if daily['p_value']<=.05 and dd>hd else 'NOT_SUPPORTED',
                      daily_breaks_per100=dd if valid else None,hourly_breaks_per100=hd if valid else None,
                      daily_descriptive_breaks_per100=dd,hourly_descriptive_breaks_per100=hd,
                      daily_breaks_per_calendar_year=None if daily['cuts'] is None else len(daily['cuts'])/years,
                      hourly_breaks_per_calendar_year=None if hourly['cuts'] is None else len(hourly['cuts'])/years,
                      common_calendar_start=first,common_calendar_stop_exclusive=stop,
                      calendar_years=years,calendar_year_days=365.2425,
                      interpretation='相同日历区间；每100观测密度受观测时钟和最多两断点上限机械影响，不识别纯频率效应。')
    return result


def _audit_predictions(archived, computed, diagnostics):
    for name in ['N1','N2','N3','N4']:
        if archived.get(name,{}).get('status')!=computed[name]['status']:
            raise ArchiveError('PREDICTION_STATUS_DISAGREEMENT:'+name)
        for field,value in archived[name].items():
            if field in computed[name] and field!='status' and (_number(value) or value is None):
                if not _same(value,computed[name][field]):
                    raise ArchiveError('PREDICTION_FIELD_DISAGREEMENT:'+name+':'+field)
    mapping=archived['N1'].get('holm_p_by_source')
    if mapping is not None:
        weekly=[r for r in diagnostics if r['kind']=='weekly']
        adjusted=_holm([r['p_value'] if r['p_value'] is not None else 1. for r in weekly])
        if set(mapping)!={r['source_id'] for r in weekly}:
            raise ArchiveError('PREDICTION_HOLM_INVENTORY')
        for row,value in zip(weekly,adjusted):
            if not _same(mapping[row['source_id']],value):
                raise ArchiveError('PREDICTION_HOLM_DISAGREEMENT:'+row['source_id'])


def _display(value):
    if value is None:
        return '不可评估'
    if isinstance(value,(dict,list,tuple)):
        return json.dumps(value,ensure_ascii=False,separators=(',',':'))
    return str(value)


def _markdown(rows, columns):
    text=['| '+' | '.join(columns)+' |','|'+'|'.join(['---']*len(columns))+'|']
    for row in rows:
        text.append('| '+' | '.join(_display(row.get(k)).replace('|','\\|').replace('\n',' ') for k in columns)+' |')
    return '\n'.join(text)+'\n'


def _write_csv(path, rows):
    fields=list(rows[0])
    with path.open('x',newline='') as f:
        writer=csv.DictWriter(f,fields);writer.writeheader()
        for row in rows:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict,tuple)) else v for k,v in row.items()})


def _write_text(path, value):
    with path.open('x') as f:
        f.write(value)


def _plot(path, across):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7.2,4.8))
    fig.subplots_adjust(left=.12,right=.98,bottom=.20,top=.88)
    colors={'constant':'#315b96','switching':'#b44735'}
    for index,arm in enumerate(ARMS):
        rows=sorted([r for r in across if r['arm']==arm],key=lambda r:r['window'])
        values=[float('nan') if r['median_pct'] is None else r['median_pct'] for r in rows]
        ax.plot(WINDOWS,values,marker='o',linewidth=2,color=colors[arm],label=arm.capitalize())
        if all(r['median_pct'] is not None for r in rows):
            ax.fill_between(WINDOWS,[r['q25_pct'] for r in rows],[r['q75_pct'] for r in rows],color=colors[arm],alpha=.12)
        for row in rows:
            if row['median_pct'] is None:
                ax.annotate(f"{arm.capitalize()}: incomplete ({row['complete_sources']}/13)",
                            xy=(row['window'],.96-index*.075),xycoords=('data','axes fraction'),
                            ha='left' if row['window']==52 else 'right',va='top',fontsize=9,color=colors[arm])
    ax.axhline(0,color='#777777',linewidth=.9,linestyle='--')
    ax.set(xticks=WINDOWS,xlabel='History W (observations)',ylabel='QR33 relative loss (%)',
           title='Registered medians across all 13 source medians')
    ax.grid(axis='y',alpha=.2);ax.legend(loc='best')
    fig.text(.01,.03,'Shading: IQR across source medians; incomplete aggregates are unavailable.',fontsize=8)
    for extension in ['png','pdf']:
        with (path/f'qr33-comparison.{extension}').open('xb') as f:
            fig.savefig(f,format=extension,dpi=180)
    plt.close(fig)


def _memo(report):
    p=report['predictions'];n1,n2,n3,n4=[p[k] for k in ['N1','N2','N3','N4']]
    status={'SUPPORTED':'成立','NOT_SUPPORTED':'不成立','UNASSESSABLE':'不可评估'}
    if all(p[k]['status']=='SUPPORTED' for k in ['N1','N2','N3']):
        interpretation='在本次注册的校准参数切换 stress 模拟中，参数切换能够复现相对历史规则的亏损；人工循环排程与拟合模型限制仍须明确，结果不证明真实数据的因果机制。'
    elif n1['status']!='SUPPORTED':
        interpretation='N1 未成立或不可评估；主线不能据本轮结果主张低频序列的不稳定性解释。各批已完成模拟的发现应分别陈述。'
    elif n2['status']=='NOT_SUPPORTED':
        interpretation='低频固定模型稳定性筛查出现拒绝，但本次注册的参数切换模拟未满足复现亏损的预设门槛。'
    else:
        interpretation='完整解释所需的 N1、N2、N3 条件未全部成立；分别报告各项结果，不使用完整机制解释。'
    contrary=''
    if n3['status']=='NOT_SUPPORTED':
        if n3['constant_W52_median_pct']>3:
            contrary='\n本轮 constant control 提供了需要保留的相反证据：W52 汇总变化为 '+_display(n3['constant_W52_median_pct'])+'%，拟合的平稳控制本身产生了回归亏损。不能概括为“所有平稳过程都不会亏损”或“平稳过程普遍排除了短样本解释”。应区分此前两批 v8 网格与本轮拟合控制过程。\n'
        else:
            contrary='\n本轮 constant control 的 W52 变化为 '+_display(n3['constant_W52_median_pct'])+'%，向负方向超出预设 ±3% 区间。这是回归收益，不能称作平稳控制产生了亏损；N3 仍不成立，不应改写为已通过控制条件。此前两批 v8 与本轮 C2 的结果须分别陈述。\n'
    elif n3['status']=='UNASSESSABLE':
        contrary='\n本轮 constant control 的必要网格不完整，N3 不可评估；不能把缺失当作平稳控制已经通过。\n'
    lines=['# C2 中文研究备忘录（由实际归档自动填写）','',
           '报告仅做既存输出的算术核对与展示，没有重跑诊断、模型、预测或 Monte Carlo。输入 SHA-256 已绑定在 report.json。',
           '',f"诊断共 {len(report['diagnostics'])} 行；条件模拟共 {len(report['cells'])} 格；每格登记 {report['repetitions']} 次重复。完整的失败格和不可评估结果保留。",'',
           f"N1：{status[n1['status']]}。13 条周度序列中，已知 raw 5% 拒绝 {n1['known_rejections']} 条，未知 {n1['unknown']} 条，最多可能拒绝 {n1['maximum_rejections']} 条；Holm13 拒绝 {n1['holm_rejections']} 条。", 
           'NONREGULAR_NULL 是拟合 null 的矩资格不足，不能称为稳定或不稳定。未知行仅在内部 Holm 运算中占位 p=1；该值不是有效的检验结果。','',
           f"N2：{status[n2['status']]}。switching QR33 的 W52 / W260 汇总中位数分别为 {_display(n2['switching_W52_median_pct'])}% / {_display(n2['switching_W260_median_pct'])}%；门槛是两者均严格大于 +5%。",'',
           f"N3：{status[n3['status']]}。constant QR33 的 W52 汇总中位数为 {_display(n3['constant_W52_median_pct'])}%；门槛为 [-3%,+3%]。",contrary,
           f"N4：{status[n4['status']]}。共同日历区间 {n4['common_calendar_start']} 至 {n4['common_calendar_stop_exclusive']}（右端不含）。日频/小时每100观测描述性断点密度为 {_display(n4['daily_descriptive_breaks_per100'])} / {_display(n4['hourly_descriptive_breaks_per100'])}；每日历年为 {_display(n4['daily_breaks_per_calendar_year'])} / {_display(n4['hourly_breaks_per_calendar_year'])}。", 
           n4['interpretation']+' 每日历年以365.2425天换算，相关区间长度明示在 report.json。','',
           interpretation,'','## 汇总口径与缺失','',
           '先对每 source 的全部登记 repetitions 相对平均损失比取中位数，再对全部13个 source 的中位数等权取中位数。IQR 也明确区分 source 内重复与13个 source 之间的分布。该指标与 WP3 的 ratio-of-mean-losses 不同，不作为同一个数值指标比较。',
           '任一必需 source 缺失时，预设汇总与图中该点为不可评估；表里的 completed_only 数值只是已完成 source 的描述，不作为预设命题的成立依据。QR4 失败不自动取消完整 QR33 判定。','',
           _markdown(report['across_source'],['arm','window','status','complete_sources','median_pct','q25_pct','q75_pct','completed_only_median_pct','missing_sources']),
           '## 图与完整表','', '[QR33 比较图 PNG](qr33-comparison.png) · [PDF](qr33-comparison.pdf) · [15行诊断表](diagnostics.md) · [全部条件模拟格](simulation-cells.md) · [CSV](simulation-cells.csv)','',
           '拟合断点只是描述性校准分区。生成器循环中的 last→first 转移是人工排程，不能当作真实历史事件。没有对相关周度序列作独立样本合并检验；没有新增真实数据预测；没有前瞻性或因果机制保证。','']
    return '\n'.join(lines)


def build_report(archive_dir):
    """Read exactly the five saved JSON inputs and create exclusive analysis/."""
    root=Path(archive_dir)
    payloads,hashes={},{}
    for name in INPUT_FILES:
        path=root/name
        if path.is_symlink() or not path.is_file():
            raise ArchiveError('MISSING_OR_NONREGULAR_ARCHIVE_INPUT:'+name)
        raw=path.read_bytes();hashes[name]=hashlib.sha256(raw).hexdigest()
        payloads[name]=json.loads(raw)
    manifest=payloads['manifest.json'];sources=manifest.get('sources',[])
    if (len(sources)!=15 or len({r.get('source_id') for r in sources})!=15
            or Counter(r.get('kind') for r in sources)!=Counter(weekly=13,daily=1,hourly=1)):
        raise ArchiveError('MANIFEST_SOURCE_INVENTORY')
    diagnostics=_diagnostic_rows(payloads['diagnostics.json'],sources)
    cells,R,methods=_simulation_rows(payloads['summary.json'],payloads['formal/replicate-scores.json'],sources)
    across=_across_source(cells,sources)
    predictions=_predictions(diagnostics,across,manifest)
    _audit_predictions(payloads['predictions.json'],predictions,diagnostics)
    report=dict(schema='v9-archive-only-analysis-v1',status='PASS',created_utc=datetime.now(timezone.utc).isoformat(),
                input_sha256=hashes,design_commit=manifest.get('design_commit'),
                repetitions=R,conditional_methods=methods,diagnostics=diagnostics,cells=cells,
                across_source=across,predictions=predictions,archived_predictions=payloads['predictions.json'],
                numeric_scope='Saved output arithmetic/display only; no source data or model computation',
                source_independence_claim=False)
    output=root/'analysis';output.mkdir(exist_ok=False)
    with (output/'report.json').open('x') as f:
        json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    _write_csv(output/'diagnostics.csv',diagnostics)
    _write_csv(output/'simulation-cells.csv',cells)
    _write_csv(output/'qr33-across-sources.csv',across)
    _write_text(output/'diagnostics.md','# 完整15行诊断\n\n'+_markdown(diagnostics,list(diagnostics[0]))+'\n未知 raw p 的 Holm 显示为不可评估；内部占位1不是有效p。每个 cuts 与 break_dates 均直接取自归档；未归档日期不推算。\n')
    _write_text(output/'simulation-cells.md','# 全部条件模拟格\n\n'+_markdown(cells,list(cells[0]))+'\ncompleted_rep_description 只描述已完成重复，不能作为失败格的预设结果。\n')
    _write_text(output/'qr33-across-sources.md','# QR33 全部13来源两层中位数\n\n'+_markdown(across,list(across[0])))
    _write_text(output/'predictions.md','# N1–N4 预设结果\n\n'+_markdown([dict(prediction=k,**v) for k,v in predictions.items()],['prediction','status'])+'\n'+json.dumps(predictions,ensure_ascii=False,indent=2)+'\n')
    _write_text(output/'research-memo-zh.md',_memo(report))
    _plot(output,across)
    files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in output.iterdir() if p.is_file()}
    with (output/'analysis-manifest.json').open('x') as f:
        json.dump(dict(input_sha256=hashes,outputs=files,overwrite=False,financial_computations=0),f,ensure_ascii=False,indent=2);f.write('\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive_dir',type=Path)
    args=parser.parse_args()
    report=build_report(args.archive_dir)
    print(json.dumps(dict(status=report['status'],diagnostic_rows=len(report['diagnostics']),simulation_cells=len(report['cells']),
                          predictions={k:v['status'] for k,v in report['predictions'].items()}),ensure_ascii=False))


if __name__=='__main__':
    main()
