"""Report-only E3 LaTeX/JSON derivation from two saved public receipts.

Prepared for root to run after MCS completion. No loss, arch, bootstrap, study
driver or numerical reducer is imported. Inputs are only summary.json and
input-index.json under results/v10/mcs. Short IDs are display aliases only.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT/'results/v10/mcs'
OUTPUTS = ('main-table.tex', 'full-table.tex', 'report-values.json', 'report-note-zh.md')
GROUP_TAGS = {'FX original': 'FX-O', 'FX early2015': 'FX-E', 'Treasury bills': 'TB',
              'Other NYFed panels': 'NY', 'Same-record dailyFX': 'DFX', 'CFTC': 'CFTC'}
STATUS_TAGS = {'COMPLETE': 'OK', 'COMPLETE_IDENTICAL_LOSSES': 'EQ', 'COMPLETE_SINGLE_METHOD': 'ONE',
               'FAILED_INPUT': 'INPUT', 'MCS_FAILED': 'MCS-FAIL', 'MISSING_RESULT': 'MISSING',
               'DUPLICATE_RESULT': 'DUPLICATE', 'UNAVAILABLE': 'UNAV'}


class ReportError(ValueError):
    """Saved report inventory or display-ID binding is inconsistent."""


def _finite(value):
    if isinstance(value, dict):
        for child in value.values():_finite(child)
    elif isinstance(value, list):
        for child in value:_finite(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ReportError('NONFINITE_SAVED_REPORT_VALUE')


def read_saved():
    receipts, hashes = {}, {}
    for name in ('summary.json', 'input-index.json'):
        path = PUBLIC/name
        if path.is_symlink() or not path.is_file():
            raise ReportError('MISSING_OR_NONREGULAR_SAVED_RECEIPT:'+name)
        raw = path.read_bytes(); value = json.loads(raw); _finite(value)
        receipts[name] = value
        hashes[name] = dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    return receipts, hashes


def _short(prefix, text):
    return prefix+hashlib.sha256(text.encode('utf-8')).hexdigest()[:10]


def prepare_report(receipts, hashes):
    summary = deepcopy(receipts['summary.json'])
    all_ids, classes = set(), {}
    cell_ids, seen_cells = {}, set()
    for cell in summary['cells']:
        encoded = json.dumps([cell['identity'][k] for k in ('period', 'normalized_source', 'horizon', 'window')],
                             separators=(',', ':'), ensure_ascii=True)
        cid = _short('C', encoded)
        if cid in seen_cells:raise ReportError('DUPLICATE_COMPARISON_OR_CELL_DISPLAY_ID')
        seen_cells.add(cid); cell_ids[cid] = deepcopy(cell['identity']); cell['display_cell_id'] = cid
        for method, kind in cell['method_classes'].items():
            all_ids.add(method); classes.setdefault(method, set()).add(kind)
        for item in cell['unavailable_methods']:
            method = item['method_id']; all_ids.add(method)
            if item.get('method_class') is not None:classes.setdefault(method, set()).add(item['method_class'])
        if set(cell.get('method_ids', [])) != set(cell['method_classes']):
            raise ReportError('SAVED_METHOD_CLASS_INVENTORY_MISMATCH')
    legend, reverse = {}, {}
    for method in sorted(all_ids):
        sid = _short('M', method)
        if sid in reverse:raise ReportError('METHOD_SHORT_ID_COLLISION')
        reverse[sid] = method
        legend[method] = dict(short_id=sid, method_id=method, explicit_classes=sorted(classes.get(method, set())))
    rows = summary['groups_summary']+[summary['overall']]
    if len({row['group_label'] for row in rows}) != len(rows):
        raise ReportError('DUPLICATE_REPORT_GROUP')
    return dict(schema='v10-mcs-saved-receipt-report-v1',
        derivation='Display-only binding; no MCS or p-value calculation.', groups=rows, cells=summary['cells'],
        method_legend=list(legend.values()), method_short_ids={k: v['short_id'] for k, v in legend.items()},
        comparison_legend=cell_ids, source_group_tags=deepcopy(GROUP_TAGS), status_tags=deepcopy(STATUS_TAGS),
        input_receipts=deepcopy(hashes), input_index_top_keys=sorted(receipts['input-index.json']) if isinstance(receipts['input-index.json'], dict) else None,
        interpretation='Related source/period/H/W tasks; descriptive fractions and failed-grid bounds, not independent pooled p-values or a future coverage guarantee.')


def _tex(value):
    special = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
               '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(special.get(c, c) for c in str(value))


def _break_tex(value):
    return ''.join(_tex(part)+(r'\allowbreak{}' if part in ('::', '_', '-', '/') else '')
                   for part in re.split(r'(::|_|-|/)', str(value)))


def _percent(value):
    return 'NA' if value is None else f'{100*value:.1f}'


def _metric_display(metric):
    first = str(metric['count_successful'])+'/'+str(metric['denominator_successful'])
    first += ' ('+_percent(metric['fraction_successful'])+r'\%)' if metric['fraction_successful'] is not None else ' (NA)'
    low, high = metric['fraction_all_planned_lower'], metric['fraction_all_planned_upper']
    second = 'NA' if low is None else '['+_percent(low)+', '+_percent(high)+r']\%'
    return r'\shortstack{'+first+r'\\{}'+second+'}'


def _conditional_display(value):
    first = str(value['excluded_slots'])+'/'+str(value['successful_complete_slots'])
    first += ' ('+_percent(value['fraction_successful'])+r'\%)' if value['fraction_successful'] is not None else ' (NA)'
    low, high = value['fraction_all_planned_lower'], value['fraction_all_planned_upper']
    second = 'NA' if low is None else '['+_percent(low)+', '+_percent(high)+r']\%'
    return r'\shortstack{'+first+r'\\P='+str(value['planned_complete_slots'])+'; '+second+'}'


def main_table(report):
    lines = [r'\begin{table}[t]', r'\centering', r'\small',
        r'\caption{Registered MCS membership across all planned comparisons. First lines show successful-denominator counts and percentages; second lines show all-planned lower/upper percentages with failed comparisons unknown.}',
        r'\label{tab:v10-mcs-main}', r'\resizebox{\linewidth}{!}{%', r'\begin{tabular}{lrrrrrr}', r'\toprule',
        r'Group & Complete/planned & Matched $F/I$ in set & Sole literal $F/I$ & Sole loss class with $F/I$ & Conditional exclusion & NA methods (cond.) \\', r'\midrule']
    for row in report['groups']:
        metrics, cond = row['metrics'], row['conditional_exclusion']
        values = [_tex(row['group_label']), str(row['successful_comparisons'])+'/'+str(row['planned_comparisons']),
            _metric_display(metrics['matched_FI_membership']), _metric_display(metrics['literal_sole_FI']),
            _metric_display(metrics['sole_loss_class_FI']), _conditional_display(cond),
            str(row['unavailable_method_slots'])+' ('+str(cond['known_na_slots'])+')']
        lines.append(' & '.join(values)+r' \\')
    lines += [r'\bottomrule', r'\end{tabular}}', r'\par\vspace{2pt}', r'\begin{minipage}{0.98\linewidth}\footnotesize',
        r'Matched historical membership excludes rolling-$F$ and query-nearest state baselines. Sole literal membership and a sole surviving exact-loss class are distinct: the latter can contain conditional procedures with identical losses. '
        r'Conditional exclusion uses distinct complete conditional-procedure slots in successful comparisons; known NA slots are not statistical exclusions. Its planned bounds treat complete conditional slots in failed comparisons as unknown. '
        r'Every failed comparison remains in planned counts. Empty denominators are NA. Related markets and overlapping tasks are not independent replications. Full sets, p-values, equivalence classes and secondary historical/rolling statistics appear in the Supplement and machine receipt.',
        r'\end{minipage}', r'\end{table}', '']
    return '\n'.join(lines)


def _id_list(methods, ids):
    return ', '.join(r'\texttt{'+ids[m]+'}' for m in methods) if methods else r'---'


def full_table(report):
    ids = report['method_short_ids']
    lines = [r'\begingroup', r'\scriptsize', r'\setlength{\tabcolsep}{3pt}',
        r'\begin{longtable}{p{.15\linewidth}p{.17\linewidth}p{.17\linewidth}p{.25\linewidth}p{.14\linewidth}}',
        r'\caption{Every planned comparison: unfolded membership and all method p-values. Display IDs bind unchanged full method labels in the legend below.}\label{tab:v10-mcs-full}\\',
        r'\toprule', r'Grid / status & Included & Excluded & All p-values & Exact-loss duplicates / known NA \\', r'\midrule', r'\endfirsthead',
        r'\toprule', r'Grid / status & Included & Excluded & All p-values & Exact-loss duplicates / known NA \\', r'\midrule', r'\endhead',
        r'\midrule\multicolumn{5}{r}{Continued on next page}\\\endfoot', r'\bottomrule\endlastfoot']
    for cell in report['cells']:
        identity = cell['identity']; status = STATUS_TAGS.get(cell['status'], cell['status'])
        grid = r'\texttt{'+cell['display_cell_id']+r'}\par '+_tex(GROUP_TAGS.get(cell['group_label'], cell['group_label']))
        grid += r'\par '+_break_tex(identity['normalized_source'])+r'\par $H='+str(identity['horizon'])+',W='+str(identity['window'])+'$'
        grid += r'\par '+_tex(status)+(', $n='+str(cell['n'])+'$' if cell.get('n') is not None else '')
        if cell['successful']:
            included, excluded = _id_list(cell['included'], ids), _id_list(cell['excluded'], ids)
            pvalues = ', '.join(r'\texttt{'+ids[m]+r'}: '+format(cell['pvalues'][m], '.4g') for m in cell['method_ids'])
        else:
            included = excluded = pvalues = r'\emph{Unavailable}'
        duplicate_classes = [g for g in cell.get('unique_loss_groups', []) if len(g['members']) > 1]
        equivalence = '; '.join(r'\{'+_id_list(g['members'], ids)+r'\}' for g in duplicate_classes)
        if not equivalence:equivalence = 'Singleton classes' if cell['successful'] else 'Classes unavailable'
        unavailable = [m['method_id'] for m in cell['unavailable_methods']]
        if unavailable:equivalence += r'\par NA: '+_id_list(unavailable, ids)
        failure = cell.get('summary_failure') or cell.get('reason')
        if failure and not cell['successful']:equivalence += r'\par '+_break_tex(failure)
        lines.append(' & '.join([grid, included, excluded, pvalues, equivalence])+r' \\')
    lines += [r'\end{longtable}', r'\endgroup', r'\begingroup', '',
        r'\noindent\footnotesize Displayed p-values are rounded for typesetting; exact saved values and the literal arch inclusion partition are retained in report-values.json. '
        r'All multi-member exact-loss classes are listed; unlisted successful classes are singletons. A duplicated-loss class does not merge distinct conditional procedure semantics. '
        r'OK=COMPLETE; EQ=COMPLETE\_IDENTICAL\_LOSSES; ONE=COMPLETE\_SINGLE\_METHOD (analytic, no discrimination claim); INPUT=FAILED\_INPUT; MCS-FAIL=MCS\_FAILED; MISSING/DUPLICATE retain absent/repeated result receipts; UNAV=UNAVAILABLE.', '',
        r'\paragraph{Source-group tags.} '+ '; '.join(_tex(tag)+'='+_tex(name) for name, tag in GROUP_TAGS.items())+'.', '',
        r'\paragraph{Stable method display legend.} IDs are SHA256-derived display aliases, not new models, classes or semantic merges.',
        r'\begin{longtable}{p{.19\linewidth}p{.58\linewidth}p{.15\linewidth}}', r'\toprule',
        r'Short ID & Unchanged full method ID & Explicit class(es) \\', r'\midrule', r'\endhead']
    for item in report['method_legend']:
        kinds = ', '.join(item['explicit_classes']) or 'unclassified known NA'
        lines.append(r'\texttt{'+item['short_id']+'} & '+_break_tex(item['method_id'])+' & '+_break_tex(kinds)+r' \\')
    lines += [r'\bottomrule', r'\end{longtable}', '',
        r'\paragraph{Secondary historical membership.} Same successful/planned denominators and failed-grid bounds; no pooled significance test.',
        r'\begin{center}\small\begin{tabular}{lrrrr}', r'\toprule',
        r'Group & Complete/planned & Matched $F/I$ only & Rolling $F$ included & Matched $F/I$ or rolling $F$ included \\', r'\midrule']
    for row in report['groups']:
        values = [_tex(row['group_label']), str(row['successful_comparisons'])+'/'+str(row['planned_comparisons'])]+[_metric_display(row['metrics'][name]) for name in
                  ('historical_only', 'rolling_F_membership', 'broad_FI_or_rolling_F_membership')]
        lines.append(' & '.join(values)+r' \\')
    lines += [r'\bottomrule', r'\end{tabular}\end{center}', r'\endgroup', '']
    return '\n'.join(lines)


def note_zh(report):
    lines = ['# E3 MCS：保存回执的描述性报告草稿', '',
        '本稿只读取 summary.json 与 input-index.json，不读取 loss 向量、不调用 arch、不重跑 bootstrap 或数值汇总器。', '',
        '成功分母与计划分母同时保留。失败格不是支持历史规则的证据，也不是统计排除；已知 NA 方法不进入条件方法排除分母。', '',
        '| 组别 | 成功/计划 | F/I 成员 | 唯一字面 F/I | 唯一损失类含 F/I | 条件排除/成功完整 slots | 已知 NA |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for row in report['groups']:
        def display(metric):
            return (str(metric['count_successful'])+'/'+str(metric['denominator_successful'])+' ('+_percent(metric['fraction_successful'])
                    +'%; 全计划界限['+_percent(metric['fraction_all_planned_lower'])+','+_percent(metric['fraction_all_planned_upper'])+']%)')
        cond = row['conditional_exclusion']
        lines.append('| '+row['group_label']+' | '+str(row['successful_comparisons'])+'/'+str(row['planned_comparisons'])+' | '
            +display(row['metrics']['matched_FI_membership'])+' | '+display(row['metrics']['literal_sole_FI'])+' | '
            +display(row['metrics']['sole_loss_class_FI'])+' | '+str(cond['excluded_slots'])+'/'+str(cond['successful_complete_slots'])
            +' ('+_percent(cond['fraction_successful'])+'%; 全计划界限['+_percent(cond['fraction_all_planned_lower'])+','
            +_percent(cond['fraction_all_planned_upper'])+']%; 计划完整slots='+str(cond['planned_complete_slots'])
            +', 失败未知slots='+str(cond['failed_complete_slots'])+') | '+str(row['unavailable_method_slots'])+' |')
    lines += ['', '唯一字面成员和唯一损失等价类不能互换：后一种仍可能包含多个条件选择程序。选择 infinity、实现相同容量或相同 loss 不会事后把 conditional 改称历史规则。Matched F/I、rolling F 以及 query-nearest one-state baselines 分别按 registry 显式分类报告。', '',
        '全部单格 included/excluded/p-values、损失等价类、已知 NA、失败状态和稳定 short-ID 对照列于 full-table.tex 与 report-values.json。短 ID 只改变展示，不改变 full method ID 或任何方法语义。', '',
        '这些是相关、重叠任务之间的描述性比例。没有独立来源 pooled p-value 检验、跨格同时覆盖保证、未来风险覆盖或经济价值结论。单方法及全相同 loss 的解析格单独标注，不称统计区分证据。', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite', action='store_true', help='replace only the four fixed report files')
    args = parser.parse_args(argv)
    for name in OUTPUTS:
        path = PUBLIC/name
        if path.is_symlink() or (path.exists() and not args.overwrite):
            raise ReportError('REPORT_OUTPUT_EXISTS_OR_IS_SYMLINK:'+name)
    receipts, hashes = read_saved(); report = prepare_report(receipts, hashes)
    payloads = {'main-table.tex': main_table(report), 'full-table.tex': full_table(report),
                'report-values.json': json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n',
                'report-note-zh.md': note_zh(report)}
    for name, content in payloads.items():
        with (PUBLIC/name).open('w' if args.overwrite else 'x') as stream:stream.write(content)
    print(json.dumps(dict(status='SAVED_RECEIPT_REPORT_WRITTEN',
        outputs={name: dict(bytes=len(value.encode('utf-8')), sha256=hashlib.sha256(value.encode('utf-8')).hexdigest())
                 for name, value in payloads.items()}), allow_nan=False))


if __name__ == '__main__':
    main()
