"""Render E1 saved-receipt reports; never forecast or rerun a reducer.

Root must invoke this only after formal receipts exist and the PDF-marker
checkpoint has been recorded. This report-only script is intentionally outside
the numerical code seal. Its only inputs are summary.json, ties.json,
manifest.json, pilot/completion.json and formal/completion.json under the fixed
results/v10/menu directory. Missing inputs fail before any report is written.

Run: python -B report_v10_menu.py [--overwrite]
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import io
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT/'results/v10/menu'
INPUTS = ('summary.json', 'ties.json', 'manifest.json',
          'pilot/completion.json', 'formal/completion.json')
OUTPUTS = ('main-table.tex', 'menu-isolation.png', 'menu-isolation.pdf',
           'report-values.json', 'report-note-zh.md')


class ReportError(ValueError):
    """Saved receipts do not support a complete, consistent report inventory."""


def _finite_tree(value):
    if isinstance(value, dict):
        for child in value.values():
            _finite_tree(child)
    elif isinstance(value, list):
        for child in value:
            _finite_tree(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ReportError('NONFINITE_SAVED_JSON_VALUE')


def _read_receipts():
    values, provenance = {}, {}
    for name in INPUTS:
        path = PUBLIC/name
        if path.is_symlink() or not path.is_file():
            raise ReportError('REQUIRED_RECEIPT_ABSENT_OR_NOT_REGULAR:'+name)
        raw = path.read_bytes()
        try:
            value = json.loads(raw)
            _finite_tree(value)
        except (ValueError, TypeError) as exc:
            raise ReportError('INVALID_SAVED_RECEIPT:'+name) from exc
        values[name] = value
        provenance[name] = dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    return values, provenance


def _integer(value):
    return type(value) is int and value >= 0


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _quartile(row, old, which):
    if old:
        key = 'original_'+which
        return row.get(key, row.get(key+'_pct'))
    return row.get(which, row.get(which+'_pct'))


def _group_side(row, cells, source_ids, old):
    prefix = 'original_' if old else ''
    status_key = prefix+'status'
    declared_status = row.get(status_key)
    if declared_status not in ('COMPLETE', 'UNASSESSABLE', 'FAILED'):
        raise ReportError('INVALID_ACROSS_STATUS')
    available = [c for c in cells if c.get(status_key) == 'COMPLETE']
    missing = [s for s in source_ids if next(c for c in cells if c['source_id'] == s).get(status_key) != 'COMPLETE']
    required = len(source_ids)
    if row.get(prefix+'complete_sources') != len(available) or row.get(prefix+'missing_sources') != missing:
        raise ReportError('SAVED_ACROSS_SOURCE_INVENTORY_MISMATCH')
    median = row.get('original_median_pct' if old else 'median_pct')
    low, high = _quartile(row, old, 'q25'), _quartile(row, old, 'q75')
    if declared_status == 'COMPLETE':
        if missing or len(available) != required or not all(_number(v) for v in (median, low, high)):
            raise ReportError('COMPLETE_ACROSS_WITH_MISSING_OPERAND')
        if not low <= median <= high:
            raise ReportError('INVALID_SAVED_IQR_ORDER')
    elif any(v is not None for v in (median, low, high)):
        # A report must never display an accidentally retained successful subset.
        raise ReportError('INCOMPLETE_ACROSS_HAS_SUBSET_STATISTICS')
    cell_value_key = 'original_relative_median_pct' if old else 'relative_median_pct'
    for cell in cells:
        value = cell.get(cell_value_key)
        if (cell.get(status_key) == 'COMPLETE') != _number(value):
            raise ReportError('CELL_STATUS_AND_SAVED_MEDIAN_DISAGREE')
    return dict(status=declared_status, complete_sources=len(available), required_sources=required,
                missing_sources=missing, median_pct=None if median is None else float(median),
                q25_pct=None if low is None else float(low), q75_pct=None if high is None else float(high),
                source_medians_pct={s: next(c for c in cells if c['source_id'] == s).get(cell_value_key)
                                    for s in source_ids})


def _completion(receipt, source_count, phase):
    planned, completed = receipt.get('planned_units'), receipt.get('complete_units')
    if (not _integer(planned) or not planned or planned % source_count
            or not _integer(completed) or completed > planned):
        raise ReportError('INVALID_'+phase.upper()+'_COMPLETION_COUNTS')
    if not isinstance(receipt.get('tasks'), list) or len(receipt['tasks']) != planned:
        raise ReportError('INCOMPLETE_'+phase.upper()+'_TASK_INVENTORY')
    if not isinstance(receipt.get('ended_utc'), str) or not receipt['ended_utc']:
        raise ReportError('UNTERMINATED_'+phase.upper()+'_PHASE')
    return dict(planned_units=planned, complete_units=completed,
                repetitions=planned//source_count, ended_utc=receipt['ended_utc'],
                elapsed_seconds=receipt.get('elapsed_seconds'))


def prepare_report(receipts, provenance):
    """Validate saved inventory and bind displays to saved all-source operands."""
    manifest, summary = receipts['manifest.json'], receipts['summary.json']
    design = manifest['design']
    source_ids = [r['source_id'] for r in design['sources']]
    arms, windows, methods = design['arms'], design['windows'], design['conditional_methods']
    if (not source_ids or len(set(source_ids)) != len(source_ids)
            or len(arms) != 2 or len(set(arms)) != 2
            or len(windows) != 2 or len(set(windows)) != 2
            or len(methods) != 2 or len(set(methods)) != 2):
        raise ReportError('EXPECTED_TWO_ARM_TWO_WINDOW_TWO_METHOD_DESIGN')
    pilot = _completion(receipts['pilot/completion.json'], len(source_ids), 'pilot')
    formal = _completion(receipts['formal/completion.json'], len(source_ids), 'formal')
    if pilot['repetitions'] != design['pilot_repetitions']:
        raise ReportError('PILOT_REPETITION_MISMATCH')
    expected_groups = [(arm, window, method) for arm in arms for window in windows for method in methods]
    group_index = {}
    for row in summary['across_sources']:
        key = (row['arm'], row['window'], row['method'])
        if key not in expected_groups or key in group_index:
            raise ReportError('DUPLICATE_OR_UNPLANNED_ACROSS_GROUP')
        group_index[key] = row
    if set(group_index) != set(expected_groups):
        raise ReportError('MISSING_PLANNED_ACROSS_GROUP')
    expected_cells = {(s, *g) for s in source_ids for g in expected_groups}
    cell_index = {}
    for cell in summary['cells']:
        key = (cell['source_id'], cell['arm'], cell['window'], cell['method'])
        if key not in expected_cells or key in cell_index:
            raise ReportError('DUPLICATE_OR_UNPLANNED_SOURCE_CELL')
        if cell.get('required_repetitions') != formal['repetitions']:
            raise ReportError('FORMAL_REPETITION_PAIRING_MISMATCH')
        cell_index[key] = cell
    if set(cell_index) != expected_cells:
        raise ReportError('MISSING_PLANNED_SOURCE_CELL')
    rows = []
    for key in expected_groups:
        group = group_index[key]
        if group.get('required_sources') != len(source_ids):
            raise ReportError('ACROSS_REQUIRED_SOURCE_COUNT_MISMATCH')
        cells = [cell_index[s, *key] for s in source_ids]
        failures = [dict(source_id=c['source_id'], status=c.get('status'),
                         failed_repetitions=deepcopy(c.get('failed_repetitions', [])),
                         failures=deepcopy(c.get('failures', [])),
                         original_status=c.get('original_status'),
                         original_failed_repetitions=deepcopy(c.get('original_failed_repetitions', [])))
                    for c in cells if c.get('status') != 'COMPLETE' or c.get('original_status') != 'COMPLETE']
        rows.append(dict(arm=key[0], window=key[1], method=key[2],
                         old=_group_side(group, cells, source_ids, True),
                         expanded=_group_side(group, cells, source_ids, False),
                         selected_inf_count=sum(c['selected_inf_count'] for c in cells),
                         selected_inf_count_scope='completed unique repetition receipts; full missing slots remain explicit',
                         unavailable_source_cells=failures))
    ties = deepcopy(receipts['ties.json'])
    if (not _integer(ties.get('exact_ties')) or not _integer(ties.get('legacy_qr4_tie_changed'))
            or set(ties.get('by_method', {})) != set(methods)
            or not all(_integer(v) for v in ties['by_method'].values())
            or sum(ties['by_method'].values()) != ties['exact_ties']
            or ties['legacy_qr4_tie_changed'] > ties['by_method'].get('QR4', 0)):
        raise ReportError('INVALID_SAVED_TIE_COUNTS')
    predictions = deepcopy(summary['predictions'])
    for name in ('M1', 'M2', 'M3'):
        if predictions.get(name, {}).get('status') not in ('SUPPORTED', 'NOT_SUPPORTED', 'UNASSESSABLE'):
            raise ReportError('INVALID_SAVED_REGISTERED_PREDICTION')
    return dict(schema='v10-menu-saved-receipt-report-v1',
                report_kind='saved-receipt derivation; no numerical re-execution',
                code_commit=manifest.get('code_commit'), design_commit=manifest.get('design_commit'),
                source_ids=source_ids, source_count=len(source_ids), arms=list(arms),
                windows=list(windows), methods=list(methods), pilot=pilot, formal=formal,
                rows=rows, predictions=predictions, registered_conditions={k: deepcopy(design[k]) for k in ('M1', 'M2', 'M3')},
                ties=ties, input_receipts=deepcopy(provenance),
                interpretation_boundary='Matched old/new repetitions and all declared source medians; IQR is descriptive, not an independent-source confidence interval. No successful-only median is used.')


def _display(value):
    return 'NA' if value is None else f'{value:.2f}'


def _tex(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
                    '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in str(value))


def _table_value(side):
    if side['status'] != 'COMPLETE':
        return r'\textsc{NA}'
    return '{} [{}, {}]'.format(_display(side['median_pct']), _display(side['q25_pct']), _display(side['q75_pct']))


def table_tex(report):
    lines = [r'\begin{table}[t]', r'\centering', r'\small',
             r'\caption{Penalty-menu isolation on matched calibrated paths. Entries are the median relative loss (\%) across all '
             + str(report['source_count']) + r' source medians, with the descriptive source IQR in brackets.}',
             r'\label{tab:v10-menu-isolation}',
             r'\begin{tabular}{lllrrl}', r'\toprule',
             r'Arm & $W$ & Method & Old menu & Expanded menu & Missing sources \\',
             r' & & & Median [IQR] & Median [IQR] & Old / expanded \\', r'\midrule']
    for row in report['rows']:
        old, new = row['old'], row['expanded']
        lines.append(r'{} & {} & {} & {} & {} & {} / {} \\'.format(
            _tex(row['arm'].capitalize()), _tex(row['window']), _tex(row['method']),
            _table_value(old), _table_value(new), len(old['missing_sources']), len(new['missing_sources'])))
    lines += [r'\bottomrule', r'\end{tabular}', r'\par\vspace{2pt}',
              r'\begin{minipage}{0.97\linewidth}\footnotesize',
              'Each source median uses all '+str(report['formal']['repetitions'])
              + r' matched repetitions. Relative loss is $100(\overline L_{QR}/\overline L_F-1)$ within each repetition. '
              + r'An unavailable old or expanded all-source aggregate is shown as NA; successful subsets are not substituted. '
              + r'Positive values mean higher QR loss. Displays are rounded; registered decisions use the saved full-precision operands. '
              + r'The expanded QR4 exact-tie rule prefers stronger penalties, unlike its old rule. '
              + 'Saved exact ties: '+str(report['ties']['exact_ties'])+'; changed QR4 tie selections: '
              +str(report['ties']['legacy_qr4_tie_changed'])+'.',
              r'\end{minipage}', r'\end{table}', '']
    return '\n'.join(lines)


def figure_bytes(report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'ps.fonttype': 42})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.4), sharey=True, squeeze=False)
    fig.subplots_adjust(left=.10, right=.98, bottom=.19, top=.84, hspace=.36, wspace=.19)
    index = {(r['arm'], r['window'], r['method']): r for r in report['rows']}
    styles = [('old', 'Old menu', '#65717e', 'o', -.11),
              ('expanded', 'Expanded menu', '#17629a', 'D', .11)]
    visible = [side[key] for row in report['rows'] for side in (row['old'], row['expanded'])
               if side['status'] == 'COMPLETE' for key in ('q25_pct', 'median_pct', 'q75_pct')]
    low, high = (min([0., *visible]), max([0., *visible])) if visible else (-1., 1.)
    span = max(high-low, 1.)
    for ai, arm in enumerate(report['arms']):
        for wi, window in enumerate(report['windows']):
            ax = axes[ai, wi]
            ax.set_ylim(low-.10*span, high+.32*span)
            ax.axhline(0, color='#888888', linewidth=.8, linestyle='--', zorder=0)
            ax.grid(axis='y', color='#dddddd', linewidth=.5, alpha=.65)
            for mi, method in enumerate(report['methods']):
                row = index[arm, window, method]
                if all(row[name]['status'] == 'COMPLETE' for name in ('old', 'expanded')):
                    ax.plot([mi-.11, mi+.11], [row['old']['median_pct'], row['expanded']['median_pct']],
                            color='#b9c0c7', linewidth=1., zorder=1)
                missing_labels = []
                for name, label, color, marker, offset in styles:
                    side = row[name]
                    if side['status'] != 'COMPLETE':
                        missing_labels.append(label+': NA ('+str(side['complete_sources'])+'/'+str(side['required_sources'])+')')
                        continue
                    median, q25, q75 = side['median_pct'], side['q25_pct'], side['q75_pct']
                    ax.errorbar(mi+offset, median, yerr=[[median-q25], [q75-median]],
                                color=color, marker=marker, markersize=5., capsize=3.,
                                linewidth=1.35, linestyle='none', zorder=3)
                if missing_labels:
                    ax.text(mi, .96, '\n'.join(missing_labels), transform=ax.get_xaxis_transform(),
                            ha='center', va='top', fontsize=7.2, color='#8b3c32',
                            bbox=dict(facecolor='white', edgecolor='none', alpha=.85, pad=1.5))
            ax.set_xlim(-.48, len(report['methods'])-.52)
            ax.set_xticks(range(len(report['methods'])), report['methods'])
            ax.set_title(arm.capitalize()+' | W='+str(window), fontsize=10, pad=7)
            if wi == 0:
                ax.set_ylabel('QR relative mean-loss change (%)')
    fig.suptitle('Matched old and expanded menus: all-source medians', fontsize=12, y=.98)
    handles = [Line2D([0], [0], color=color, marker=marker, linestyle='none', markersize=6., label=label)
               for _, label, color, marker, _ in styles]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.54, .94), frameon=False, ncol=2)
    fig.text(.10, .105, 'Each point: median across all '+str(report['source_count'])+' source medians; whiskers: descriptive source IQR.', fontsize=8)
    fig.text(.10, .073, 'Within-source medians use '+str(report['formal']['repetitions'])+' matched repetitions. NA retains incomplete groups; no successful subset is plotted.', fontsize=8)
    fig.text(.10, .041, 'Positive = higher QR loss. IQR is not a confidence interval; calibrated sources are related.', fontsize=8)
    output = {}
    try:
        for extension in ('png', 'pdf'):
            buffer = io.BytesIO()
            metadata = {'CreationDate': None, 'ModDate': None} if extension == 'pdf' else {}
            fig.savefig(buffer, format=extension, dpi=200, metadata=metadata)
            output['menu-isolation.'+extension] = buffer.getvalue()
    finally:
        plt.close(fig)
    return output


def note_zh(report):
    p, conditions = report['predictions'], report['registered_conditions']
    names = {'SUPPORTED': '支持', 'NOT_SUPPORTED': '不支持', 'UNASSESSABLE': '不可评估'}
    m1, m2, m3 = p['M1'], p['M2'], p['M3']
    lines = ['# E1 菜单隔离：由已保存回执派生的报告草稿', '',
             '本草稿仅读取 summary、ties、manifest 和两个阶段的 completion 回执。没有重新生成路径、校准、预测、选择惩罚或计算逐点评分。', '',
             '正式计划为每来源 '+str(report['formal']['repetitions'])+' 个配对重复，来源数为 '+str(report['source_count'])
             +'；完整 unit 为 '+str(report['formal']['complete_units'])+'/'+str(report['formal']['planned_units'])
             +'。完整 unit 数不替代每个方法格的完整性判定。', '',
             '每个重复沿用冻结的 100*(QR/F-1) 浮点算术；先取来源内完整重复的中位数，再对全部预定来源中位数等权取中位数和描述性 IQR。没有成功来源子集汇总。显示值作小数舍入，注册判定使用完整精度；临界值核对以 report-values.json 为准。', '',
             'M1：'+names[m1['status']]+'。constant 的 '+conditions['M1']['method']+'、W='+str(conditions['M1']['window'])
             +' 跨来源中位数为 '+_display(m1.get('constant_median_pct'))+'%；闭区间为 ['
             +_display(conditions['M1']['lower_inclusive_pct'])+', '+_display(conditions['M1']['upper_inclusive_pct'])+']%。',
             'M2：'+names[m2['status']]+'。switching 减 constant 的中位数差为 '
             +_display(m2.get('switching_minus_constant_pct_points'))+' 个百分点；注册门槛为至少 '
             +_display(conditions['M2']['minimum_inclusive_percentage_points'])+' 个百分点。',
             'M3：'+names[m3['status']]+'。两臂均严格改善的来源交集为 '+str(m3.get('joint_improved_sources'))
             +'，注册要求至少 '+str(conditions['M3']['minimum_joint_improved_sources'])
             +'；未知来源为 '+('、'.join(m3.get('unknown_source_ids', [])) or '无')+'。来源条件不能用两臂改善来源的并集替代。', '']
    constant = m1.get('constant_median_pct')
    if m1['status'] == 'UNASSESSABLE' or m2['status'] == 'UNASSESSABLE':
        lines.append('注册解释所需操作数存在不完整格，保持不可评估；不能强行归入支持或不支持的解释分支。M3 仍独立报告。')
    elif m1['status'] == 'SUPPORTED' and m2['status'] == 'SUPPORTED':
        lines.append('在这些已校准程序中，允许扩展菜单后，相对损失更集中于 switching 过程；解释只限本次固定比较。')
    elif m1['status'] == 'SUPPORTED' and m2['status'] == 'NOT_SUPPORTED':
        lines.append('该比较更支持菜单是短历史表现的主要来源，未建立注册的 switching 增量；未过门槛不能写成总体等价。')
    elif constant is not None and constant < conditions['M1']['lower_inclusive_pct']:
        lines.append('constant 向负方向超出近似持平区间：这是 QR 改善并错过近似持平门槛，不能写成亏损增加。')
    else:
        lines.append('扩展菜单后 constant 仍未进入注册的近似持平区间；按已保存数值报告剩余相对损失，不迁移门槛。')
    lines += ['', '全部八组旧新汇总：', '',
              '| Arm | W | Method | 旧 median [IQR] | 新 median [IQR] | 缺来源 旧/新 |',
              '|---|---:|---|---:|---:|---|']
    for row in report['rows']:
        def display_side(side):
            return ('NA ('+side['status']+')') if side['status'] != 'COMPLETE' else (
                _display(side['median_pct'])+' ['+_display(side['q25_pct'])+', '+_display(side['q75_pct'])+']')
        lines.append('| '+row['arm']+' | '+str(row['window'])+' | '+row['method']+' | '
                     +display_side(row['old'])+' | '+display_side(row['expanded'])+' | '
                     +str(len(row['old']['missing_sources']))+'/'+str(len(row['expanded']['missing_sources']))+' |')
    lines += ['', '保存的 exact tie 总数为 '+str(report['ties']['exact_ties'])
              +'；因 QR4 改用更强惩罚优先而改变的 tie 选择数为 '+str(report['ties']['legacy_qr4_tie_changed'])
              +'。QR4 tie 约定发生了用户指示的程序变化，不能表述为其余选择程序完全未变。', '',
              '图中 whisker 是相关来源间的描述性 IQR，不是独立来源置信区间。本草稿不提供 E3/MCS、E4 成本或新增真实金融预测结果。', '',
              '逐组完整精度数值、缺失来源及输入回执 SHA256 见同目录 report-values.json。', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite', action='store_true', help='replace only the five fixed report artifacts')
    args = parser.parse_args(argv)
    if not args.overwrite and any((PUBLIC/name).exists() for name in OUTPUTS):
        raise ReportError('REPORT_OUTPUT_EXISTS; review before explicitly using --overwrite')
    receipts, provenance = _read_receipts()
    report = prepare_report(receipts, provenance)
    payloads = {
        'main-table.tex': table_tex(report).encode('utf-8'),
        'report-values.json': (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8'),
        'report-note-zh.md': note_zh(report).encode('utf-8')}
    payloads.update(figure_bytes(report))
    if set(payloads) != set(OUTPUTS):
        raise ReportError('INCOMPLETE_REPORT_PAYLOADS')
    for name in OUTPUTS:
        path = PUBLIC/name
        if path.is_symlink():
            raise ReportError('REPORT_OUTPUT_IS_SYMLINK:'+name)
    for name in OUTPUTS:
        with (PUBLIC/name).open('wb' if args.overwrite else 'xb') as stream:
            stream.write(payloads[name])
    print(json.dumps(dict(status='SAVED_RECEIPT_REPORT_WRITTEN',
                          outputs={name: dict(bytes=len(payloads[name]), sha256=hashlib.sha256(payloads[name]).hexdigest())
                                   for name in OUTPUTS}), allow_nan=False))


if __name__ == '__main__':
    main()
