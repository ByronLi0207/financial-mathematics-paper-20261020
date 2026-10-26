"""Prepare E2 tables/figures solely from saved summary and metadata receipts.

No raw CFTC observations, ZIP, model, score routine, study driver or reducer is
loaded. Run only after root has saved the final receipts. This script has been
prepared separately from numerical execution; it never starts a study.

Inputs: results/v10/cftc/{summary,eligibility,splits}.json and
data/cftc-tff/provenance.json. Outputs stay in results/v10/cftc.
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
PUBLIC = ROOT/'results/v10/cftc'
INPUTS = dict(summary=PUBLIC/'summary.json', eligibility=PUBLIC/'eligibility.json',
              splits=PUBLIC/'splits.json', provenance=ROOT/'data/cftc-tff/provenance.json')
PERFORMANCE_OUTPUTS = ('contract-table.tex', 'contract-changes.png', 'contract-changes.pdf')
METHODS = ('F', 'I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33')
TABLE_METHODS = ('I', 'QR4', 'QR33', 'ACI_F', 'ACI_QR33')
WINDOWS = (52, 260)


class ReportError(ValueError):
    """Saved summary and selected-contract metadata disagree."""


def _finite(value):
    if isinstance(value, dict):
        for child in value.values():_finite(child)
    elif isinstance(value, list):
        for child in value:_finite(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ReportError('NONFINITE_SAVED_JSON')


def read_saved():
    receipts, hashes = {}, {}
    for name, path in INPUTS.items():
        if path.is_symlink() or not path.is_file():
            raise ReportError('MISSING_SAVED_RECEIPT:'+str(path.relative_to(ROOT)))
        raw = path.read_bytes()
        receipts[name] = json.loads(raw)
        _finite(receipts[name])
        hashes[name] = dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    return receipts, hashes


def prepare_report(receipts, hashes):
    summary, eligibility = receipts['summary'], receipts['eligibility']
    codes = list(eligibility.get('selected', []))
    if any(not isinstance(c, str) for c in codes) or len(codes) != len(set(codes)):
        raise ReportError('INVALID_SELECTED_LITERAL_CODES')
    contract_index = {r['code']: r for r in summary['contracts']}
    if len(contract_index) != len(summary['contracts']) or set(contract_index) != set(codes):
        raise ReportError('SUMMARY_AND_SELECTED_CONTRACT_INVENTORIES_DISAGREE')
    cells = {}
    planned = {(code, window, method) for code in codes for window in WINDOWS for method in METHODS}
    for cell in summary['cells']:
        key = (cell['code'], cell['window'], cell['method'])
        if key not in planned or key in cells:
            raise ReportError('DUPLICATE_OR_UNPLANNED_METHOD_SLOT')
        cells[key] = cell
    if set(cells) != planned:
        raise ReportError('MISSING_PLANNED_METHOD_SLOT')
    metadata = {r['code']: r for r in eligibility.get('contracts', []) if 'code' in r}
    rows = []
    for code in codes:
        method_rows = {str(window): {method: deepcopy(cells[code, window, method]) for method in METHODS}
                       for window in WINDOWS}
        meta = metadata.get(code, {})
        rows.append(dict(code=code, status=contract_index[code]['status'], windows=method_rows,
            market_names=deepcopy(meta.get('name_spans', [])),
            exchange_metadata=deepcopy(meta.get('exchanges', [])), units_metadata=deepcopy(meta.get('normalized_units', [])),
            first_position_date=meta.get('first_position_date'), last_position_date=meta.get('last_position_date'),
            mean_open_interest=meta.get('mean_open_interest'), observations=meta.get('observations'),
            failed_method_slots=deepcopy(contract_index[code].get('failed_method_slots', []))))
    available = bool(codes)
    return dict(schema='v10-cftc-saved-receipt-report-v1',
        status='AVAILABLE' if available else 'UNAVAILABLE', selected_codes=codes, contract_count=len(codes),
        rows=rows, across_contracts=deepcopy(summary['across_contracts']), predictions=deepcopy(summary['predictions']),
        eligibility_status=eligibility.get('status'), N=eligibility.get('N', receipts['splits'].get('N')),
        splits=deepcopy(receipts['splits']), source_provenance=deepcopy(receipts['provenance']), input_receipts=deepcopy(hashes),
        output_status={name: dict(status='READY' if available else 'UNAVAILABLE',
            reason=None if available else 'No selected contracts; no contract performance table/figure is fabricated.') for name in PERFORMANCE_OUTPUTS},
        interpretation_boundary='Downloaded economic-date replay; related category-aggregate futures markets, contract counts not dollar exposure; no pooled independent-series test.')


def _display(value):
    return 'NA' if value is None else f'{value:.2f}'


def _tex(value):
    special = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
               '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(special.get(c, c) for c in str(value))


def table_tex(report):
    lines = [r'\begin{table}[t]', r'\centering', r'\scriptsize',
        r'\caption{CFTC dealer-category futures application: within-contract relative loss versus matched $F$ (\%). All '
        +str(report['contract_count'])+r' selected literal contract codes are retained.}',
        r'\label{tab:v10-cftc-contracts}', r'\resizebox{\linewidth}{!}{%',
        r'\begin{tabular}{lrrrrrrrrrr}', r'\toprule',
        r'Contract code & \multicolumn{5}{c}{$W=52$} & \multicolumn{5}{c}{$W=260$} \\',
        r'\cmidrule(lr){2-6}\cmidrule(lr){7-11}',
        r' & $I$ & QR4 & QR33 & ACI-$F$ & ACI-QR33 & $I$ & QR4 & QR33 & ACI-$F$ & ACI-QR33 \\', r'\midrule']
    for row in report['rows']:
        values = []
        for window in WINDOWS:
            for method in TABLE_METHODS:
                cell = row['windows'][str(window)][method]
                values.append(_display(cell.get('relative_loss_pct')) if cell['status'] == 'COMPLETE' else r'\textsc{NA}')
        lines.append(_tex(row['code'])+' & '+' & '.join(values)+r' \\')
    t1, t2 = report['predictions']['T1'], report['predictions']['T2']
    lines += [r'\bottomrule', r'\end{tabular}}', r'\par\vspace{2pt}',
        r'\begin{minipage}{0.98\linewidth}\footnotesize',
        r'Each entry is $100(\overline L_m/\overline L_F-1)$ using the saved complete evaluation. '
        r'NA retains failed/incomplete methods or an unavailable/nonpositive $F$ denominator. '
        r'Positive values indicate higher loss. T1 uses every selected-contract/two-window cell (denominator '
        +str(t1.get('required_cells'))+'), with the registered fraction at least '+_display(t1.get('minimum_inclusive_fraction'))
        +r'; T2 requires the all-contract QR33 median at both windows inside ['
        +_display(t2.get('lower_inclusive_pct'))+', '+_display(t2.get('upper_inclusive_pct'))+r']\%. '
        r'T3 compares complete all-contract QR4 medians strictly. No successful-contract subset substitutes for any threshold. '
        r'Displays are rounded; decisions use saved full-precision operands. F and every absolute score/breach/selection receipt remain in the detailed summary and exported cell CSV.',
        r'\end{minipage}', r'\end{table}', '']
    return '\n'.join(lines)


def figure_bytes(report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    codes = report['selected_codes']
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 6.8), sharex=True, sharey=True)
    fig.subplots_adjust(left=.105, right=.985, top=.86, bottom=.17, wspace=.10)
    styles = [(52, '#17629a', 'o'), (260, '#ad4934', 'D')]
    values = [row['windows'][str(w)]['QR33'].get('relative_loss_pct') for row in report['rows'] for w in WINDOWS]
    visible = [v for v in values if v is not None]
    lo, hi = (min([0., *visible]), max([0., *visible])) if visible else (-1., 1.)
    span = max(hi-lo, 1.)
    for ax, (window, color, marker) in zip(axes, styles):
        ax.set_xlim(lo-.09*span, hi+.08*span)
        ax.axvline(0, linestyle='--', color='#888888', linewidth=.8)
        ax.grid(axis='both', alpha=.18)
        for i, row in enumerate(report['rows']):
            cell = row['windows'][str(window)]['QR33']; value = cell.get('relative_loss_pct')
            if cell['status'] == 'COMPLETE' and value is not None:
                ax.scatter(value, i, color=color, marker=marker, s=28, zorder=3)
            else:
                ax.text(.94, i, 'NA', transform=ax.get_yaxis_transform(),
                        ha='right', va='center', fontsize=7.5, color=color)
        ax.set_yticks(range(len(codes)), codes, fontsize=8)
        ax.set_title('$W='+str(window)+'$', fontsize=12)
        ax.set_xlabel('QR33/F relative loss change (%)', fontsize=9)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    axes[0].set_ylim(len(codes)-.5, -.5)
    axes[0].set_ylabel('Literal contract code, frozen OI-ranked order', fontsize=9)
    fig.suptitle('CFTC dealer-category positions: all selected contracts', fontsize=13, y=.94)
    fig.text(.105, .085, 'Each column retains all '+str(len(codes))+' selected contracts. Positive values mean higher QR33 loss.', fontsize=8)
    fig.text(.105, .055, 'NA retains failed, incomplete or nonpositive-F slots. Related contracts are not independent dealers.', fontsize=8)
    fig.text(.105, .025, 'Contract counts are not dollar exposures. No successful-contract subset is substituted.', fontsize=8)
    payloads = {}
    try:
        for extension in ('png', 'pdf'):
            buffer = io.BytesIO()
            metadata = {'CreationDate': None, 'ModDate': None} if extension == 'pdf' else {}
            fig.savefig(buffer, format=extension, dpi=200, metadata=metadata)
            payloads['contract-changes.'+extension] = buffer.getvalue()
    finally:
        plt.close(fig)
    return payloads


def note_zh(report):
    names = {'SUPPORTED': '支持', 'NOT_SUPPORTED': '不支持', 'UNASSESSABLE': '不可评估', 'UNAVAILABLE': '不可用'}
    lines = ['# E2 CFTC：已保存回执报告草稿', '',
        '本草稿只读取 saved summary、eligibility、splits 与来源 provenance 元数据，不读取 raw observations，不运行筛选、校准、预测或新增检验。', '',
        '已保存的选中合约数为 '+str(report['contract_count'])+'，按 eligibility 的原顺序保留字面 code；不补成20个合约。', '']
    if not report['selected_codes']:
        lines += ['没有选中合约：保留 UNAVAILABLE。没有生成合约表现表或图；缺失输出的状态记录在 report-values.json，不合成任何合约或表现数值。', '']
    else:
        for name in ('T1', 'T2', 'T3'):
            row = report['predictions'][name]
            lines.append(name+'：'+names.get(row.get('status'), str(row.get('status')))+'。完整精度操作数：`'
                         +json.dumps(row, ensure_ascii=False, allow_nan=False)+'`。')
        lines += ['', '全部所选合约在图轴及主表各保留一行。主表展示 I、QR4、QR33、ACI_F、ACI_QR33 在两 W 相对其自身 F 的变化；F 原始均值、所有绝对评分、breach、惩罚、gamma 和失败槽仍在完整 cells/CSV 中。', '',
            '图只显示逐合约 QR33/F 的两 W 对照，失败或非正 F 显示 NA；没有成功合约子集的汇总线。所有数字由 saved cells/across_contracts/predictions 直接引用。显示舍入不改变完整精度门槛。', '']
    lines += ['来源状态：'+str(report['source_provenance'].get('status'))+'。下载 vintage 的经济头寸日期与 Monday 模型时钟分开；Monday 标签不代表当时已公开信息。来源是独立于 NYFed 的报告系统，但 futures dealer 类别是聚合数据，contract counts 不是美元敞口。', '',
        'OI 全历史排名是事后 universe 选择；相关市场不构成独立交易员样本，不进行合并独立性检验，也不作跨合约美元或原始损失聚合。', '',
        '保存的 split 元数据（原样引用，不推算缺失日期）：', '', '```json',
        json.dumps(report['splits'], ensure_ascii=False, indent=2, allow_nan=False), '```', '',
        '输入路径、bytes、SHA256 和逐合约完整精度绑定见 report-values.json。此稿不产生 E3/MCS 或 E4 成本结果。', '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite', action='store_true', help='replace only fixed report artifacts')
    args = parser.parse_args(argv)
    receipts, hashes = read_saved()
    report = prepare_report(receipts, hashes)
    payloads = {'report-values.json': (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8'),
                'report-note-zh.md': note_zh(report).encode('utf-8')}
    if report['selected_codes']:
        payloads['contract-table.tex'] = table_tex(report).encode('utf-8')
        payloads.update(figure_bytes(report))
    elif any((PUBLIC/name).exists() for name in PERFORMANCE_OUTPUTS):
        raise ReportError('UNAVAILABLE_UNIVERSE_WITH_STALE_PERFORMANCE_OUTPUT; preserve and review separately')
    for name in payloads:
        path = PUBLIC/name
        if path.is_symlink() or (path.exists() and not args.overwrite):
            raise ReportError('REPORT_OUTPUT_EXISTS_OR_IS_SYMLINK:'+name)
    for name, payload in payloads.items():
        with (PUBLIC/name).open('wb' if args.overwrite else 'xb') as stream:stream.write(payload)
    print(json.dumps(dict(status=report['status'], outputs={name: dict(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
          for name, payload in payloads.items()}), allow_nan=False))


if __name__ == '__main__':
    main()
