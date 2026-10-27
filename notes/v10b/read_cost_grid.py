# -*- coding: utf-8 -*-
"""Read archived v10 flags and summaries; never evaluate a cost or fit a model.

Run from any directory with Python's standard library. Only cost-reading.json
and cost-reading.md beside this script are written. CSV line numbers count the
header as line 1; ZIP member line numbers refer to cost-grid.csv after decoding.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE_RECEIPTS = {}


def utc():
    return datetime.now(timezone.utc).isoformat()


def read_bytes(relative):
    path = ROOT / relative
    started = utc()
    raw = path.read_bytes()
    SOURCE_RECEIPTS[relative] = {
        "read_started_utc": started, "read_finished_utc": utc(),
        "bytes": len(raw), "sha256_before": hashlib.sha256(raw).hexdigest(),
    }
    return raw


def read_json(relative):
    return json.loads(read_bytes(relative))


def csv_rows(raw):
    # Existing fields contain no embedded newlines. reader.line_num is still
    # used rather than assuming a fixed physical line count per record.
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
    fields = reader.fieldnames
    return fields, [(reader.line_num, dict(row)) for row in reader]


def number(value):
    return Decimal(str(value))


def fmt(value):
    return format(number(value), "f").rstrip("0").rstrip(".") if "." in str(value) else str(value)


def flag(value):
    assert value in {"True", "False"}, value
    return value == "True"


def key(row):
    return tuple(row[k] for k in ("period", "normalized_source", "horizon", "window", "method_id")) + tuple(number(row[k]) for k in ("kappa", "beta", "c"))


def binding(relative, pointer, value):
    return {"source": relative, "json_pointer": pointer, "archived_value": value}


def main():
    started = utc()
    primary_path = "results/v10/cost/primary-regions.csv"
    archive_path = "results/v10/cost/cost-grid.csv.zip"
    manifest_path = "results/v10/cost/manifest.json"
    primary_fields, primary = csv_rows(read_bytes(primary_path))
    archive_raw = read_bytes(archive_path)
    with zipfile.ZipFile(io.BytesIO(archive_raw)) as archive:
        assert archive.namelist() == ["cost-grid.csv"]
        member = archive.read("cost-grid.csv")
    grid_fields, grid = csv_rows(member)
    manifest = read_json(manifest_path)
    design = manifest["design"]
    assert design["reference_id"] == "F"
    assert design["primary_c"] == 1
    assert design["primary_method_by_group"]["CFTC"] == "CFTC::QR33"
    assert "difference<0" in design["ties"]
    assert set(grid_fields).issubset(primary_fields)

    def wanted(row):
        return row["group_label"] == "CFTC" and row["method_id"] == "CFTC::QR33" and number(row["c"]) == 1

    selected = [(line, row) for line, row in primary if wanted(row)]
    archive_lookup = {key(row): (line, row) for line, row in grid if wanted(row)}
    assert len(archive_lookup) == sum(wanted(row) for _, row in grid)
    assert len(archive_lookup) == len(selected)
    receipts = []
    for line, row in selected:
        grid_line, other = archive_lookup[key(row)]
        assert row["status"] == "COMPLETE" and row["reason"] == ""
        assert all(row[field] == other[field] for field in grid_fields)
        assert not (flag(row["cheaper"]) and flag(row["equal"]))
        receipts.append({
            "primary_csv_line": line, "cost_grid_member_line": grid_line,
            "archived_fields": row,
        })
    kappas = sorted({number(r["archived_fields"]["kappa"]) for r in receipts})
    betas = sorted({number(r["archived_fields"]["beta"]) for r in receipts})
    assert kappas == sorted(map(number, design["grid"]["kappa"]))
    assert betas == sorted(map(number, design["grid"]["beta"]))
    assert len(kappas) % 2 == len(betas) % 2 == 1
    contracts = sorted({r["archived_fields"]["normalized_source"] for r in receipts})
    windows = sorted({int(r["archived_fields"]["window"]) for r in receipts})
    cells = sorted({(r["archived_fields"]["normalized_source"], r["archived_fields"]["window"]) for r in receipts})
    assert len(contracts) == 17 and windows == [52, 260] and len(cells) == 34
    assert {r["archived_fields"]["horizon"] for r in receipts} == {"6"}
    assert {r["archived_fields"]["period"] for r in receipts} == {"economic_date_replay_2021_2026"}
    points = {}
    for k in kappas:
        for b in betas:
            rr = [r for r in receipts if number(r["archived_fields"]["kappa"]) == k and number(r["archived_fields"]["beta"]) == b]
            assert len(rr) == len(cells)
            assert len({(r["archived_fields"]["normalized_source"], r["archived_fields"]["window"]) for r in rr}) == len(cells)
            points[k, b] = {
                "kappa": str(k), "beta": str(b), "c": "1",
                "strict_cheaper_count": sum(flag(r["archived_fields"]["cheaper"]) for r in rr),
                "equal_count": sum(flag(r["archived_fields"]["equal"]) for r in rr),
                "complete_denominator": len(rr), "planned_denominator": len(cells),
                "primary_csv_lines": [r["primary_csv_line"] for r in rr],
                "cost_grid_member_lines": [r["cost_grid_member_line"] for r in rr],
            }
    chosen = [
        ("sorted_position_center", (kappas[len(kappas) // 2], betas[len(betas) // 2])),
        ("higher_reserve_lower_breach_corner", (kappas[-1], betas[0])),
        ("lower_reserve_higher_breach_corner", (kappas[0], betas[-1])),
    ]
    examples = [{"selection": label, **points[point]} for label, point in chosen]
    lookup = {(r["archived_fields"]["normalized_source"], r["archived_fields"]["window"], number(r["archived_fields"]["kappa"]), number(r["archived_fields"]["beta"])): r for r in receipts}
    exceptions = {"higher_kappa_true_to_false": [], "higher_beta_false_to_true": []}
    for contract, window in cells:
        for beta in betas:
            for low, high in zip(kappas, kappas[1:]):
                before, after = lookup[contract, window, low, beta], lookup[contract, window, high, beta]
                if flag(before["archived_fields"]["cheaper"]) and not flag(after["archived_fields"]["cheaper"]):
                    exceptions["higher_kappa_true_to_false"].append({"before": before, "after": after})
        for kappa in kappas:
            for low, high in zip(betas, betas[1:]):
                before, after = lookup[contract, window, kappa, low], lookup[contract, window, kappa, high]
                if not flag(before["archived_fields"]["cheaper"]) and flag(after["archived_fields"]["cheaper"]):
                    exceptions["higher_beta_false_to_true"].append({"before": before, "after": after})
    aggregate_exceptions = []
    for beta in betas:
        for low, high in zip(kappas, kappas[1:]):
            before, after = points[low, beta], points[high, beta]
            if after["strict_cheaper_count"] < before["strict_cheaper_count"]:
                aggregate_exceptions.append({"direction": "higher_kappa_reduces_count", "before": before, "after": after})
    for kappa in kappas:
        for low, high in zip(betas, betas[1:]):
            before, after = points[kappa, low], points[kappa, high]
            if after["strict_cheaper_count"] > before["strict_cheaper_count"]:
                aggregate_exceptions.append({"direction": "higher_beta_increases_count", "before": before, "after": after})

    mcs_path = "results/v10/mcs/summary.json"
    mcs = read_json(mcs_path)
    overall = mcs["overall"]
    mcs_cells_path = "results/v10/mcs/full-cells.json"
    mcs_cells = read_json(mcs_cells_path)
    mcs_evidence = [{"json_pointer": f"/{i}", "identity": cell["identity"], "status": cell["status"], "included": cell["included"], "matched_FI_present": bool({"F", "I"} & set(cell["included"]))} for i, cell in enumerate(mcs_cells)]
    assert len(mcs_evidence) == overall["planned_comparisons"] == 98
    assert sum(r["matched_FI_present"] for r in mcs_evidence) == overall["metrics"]["matched_FI_membership"]["count_successful"] == 90
    assert all(r["status"] == "COMPLETE" for r in mcs_evidence)
    menu_path = "results/v10/menu/summary.json"
    menu = read_json(menu_path)
    menu_bindings = []
    for i, row in enumerate(menu["across_sources"]):
        if row["window"] == 52 and row["method"] == "QR33":
            for field in ("arm", "window", "method", "status", "complete_sources", "original_median_pct", "median_pct"):
                menu_bindings.append(binding(menu_path, f"/across_sources/{i}/{field}", row[field]))
    for field, value in menu["predictions"]["M2"].items():
        menu_bindings.append(binding(menu_path, f"/predictions/M2/{field}", value))
    assert menu["predictions"]["M2"]["status"] == "NOT_SUPPORTED"
    assert menu["predictions"]["M2"]["switching_minus_constant_pct_points"] == -0.43471629487539243

    for relative, receipt in SOURCE_RECEIPTS.items():
        receipt["sha256_after"] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        receipt["unchanged"] = receipt["sha256_before"] == receipt["sha256_after"]
        assert receipt["unchanged"], relative
    direction = "Expanded QR33 is more often cheaper than F toward higher reserve coefficients and lower fixed-breach charges, with one contract/history exception to monotonicity."
    center, favorable, adverse = examples
    three_sentences = [
        "At fixed $c=1$, expanded-menu QR33 is generally cheaper than F more often with higher reserve coefficient $\\kappa$ and lower fixed-breach coefficient $\\beta$, although the archived grid is not monotone.",
        "Across the 17 contracts and two histories, it is strictly cheaper in 5/34 comparisons at the sorted-grid centre $(\\kappa,\\beta)=(0.1,0.25)$, versus 32/34 at $(1,0)$ and 1/34 at the opposite corner $(0.01,5)$.",
        "These coefficients are illustrative preferences rather than observed business costs, so the rankings do not establish funding gains or a cost-optimal policy.",
    ]
    out = {
        "status": "PASS_READ_ONLY_ARCHIVED_FLAGS", "read_started_utc": started, "read_finished_utc": utc(),
        "scope": "Only reads archived cheaper/equal flags, identities and existing summaries; no loss/cost recalculation, model fitting, selection, new data, or experiment.",
        "sources": SOURCE_RECEIPTS,
        "zip_member": {"name": "cost-grid.csv", "bytes": len(member), "sha256": hashlib.sha256(member).hexdigest(), "csv_fields": grid_fields, "data_rows": len(grid)},
        "primary_csv": {"fields": primary_fields, "data_rows": len(primary)},
        "reference_and_slice_bindings": [binding(manifest_path, "/design/" + name, design[name]) for name in ("reference_id", "primary_c", "grid", "primary_method_by_group", "ties", "formula", "scale", "interpretation")],
        "denominator": {"contract_ids": contracts, "contract_count": len(contracts), "history_windows": windows, "history_count": len(windows), "planned_contract_history_count": len(cells), "complete_contract_history_count_at_every_point": len(cells), "derivation": "Unique normalized_source x window in the matched row bindings; 17 contracts x 2 windows = 34, no pooled independence claim."},
        "sorted_grid": {"kappa": list(map(str, kappas)), "beta": list(map(str, betas)), "center_rule": "Middle sorted position on each odd-length archived axis; no interpolation or arithmetic midpoint."},
        "examples": examples, "all_c1_point_counts": list(points.values()),
        "two_file_match": {"matched_c1_CFTC_QR33_rows": len(receipts), "fields_compared_exactly": grid_fields, "result": "ALL_ARCHIVED_FIELDS_IDENTICAL", "row_bindings": receipts},
        "direction": direction,
        "monotonicity": {"strict_monotone": not any(exceptions.values()), "individual_exceptions": exceptions, "aggregate_count_exceptions": aggregate_exceptions, "exception_cell_ids": sorted({(e["before"]["archived_fields"]["normalized_source"], e["before"]["archived_fields"]["window"]) for values in exceptions.values() for e in values})},
        "abstract_checks": {
            "MCS": {"bindings": [binding(mcs_path, "/overall/planned_comparisons", overall["planned_comparisons"]), binding(mcs_path, "/overall/metrics/matched_FI_membership", overall["metrics"]["matched_FI_membership"]), binding(mcs_path, "/overall/metrics/literal_sole_FI", overall["metrics"]["literal_sole_FI"])], "full_cells_source": mcs_cells_path, "full_cell_membership_evidence": mcs_evidence, "wording": "Nearly always describes 90/98=91.8% of these related comparisons, not unique superiority or predictive-risk equality; prefer exact wording 'in 90 of 98 comparisons'."},
            "menu_and_M2": {"bindings": menu_bindings, "wording": "The constant-arm short-history median excess loss falls from 116.24327967680179% to 0.2069371499562489% (116.2% to 0.2% at one decimal); switching is 121.40097999787356% to -0.22777914491914353%. M2=-0.43471629487539243 percentage points misses the registered +5-point threshold. This does not establish no effect or equivalence."},
        },
        "recommended_cost_subsection_exactly_three_sentences": three_sentences,
        "recommended_contribution_3": "Third, score gains translate into lower limit costs only in parts of the coefficient grid; CFTC expanded-regression cost advantages are more prevalent under higher reserve and lower fixed-breach charges, with exceptions to monotonicity.",
        "recommended_RQ3_answer": "For RQ3, score gains imply lower limit costs only for some illustrative reserve, breach-frequency and exceedance preferences; the CFTC grid generally favors expanded regression as reserve charges rise and fixed-breach charges fall, with exceptions to monotonicity.",
        "recommended_letter": "The third finding separates forecast-score gains from limit-cost rankings: expanded regression is generally cheaper in more CFTC comparisons under higher reserve and lower fixed-breach charges, while the illustrative coefficient grid contains exceptions to monotonicity.",
        "editorial_note": "The cost subsection's three sentences contain the full three-point numerical example. Use qualitative versions in contribution 3, RQ3 conclusion and letter to avoid repeating the same result numbers. Relocate the existing illustrative-cost caveat from Limitations if needed so that it appears only once in the main manuscript. Do not turn the direction into an exception-free comparative-static claim.",
    }
    (OUT / "cost-reading.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    lines = ["# v10b 归档成本只读核对", "", f"状态：`{out['status']}`。实际读取 UTC：`{started}` 至 `{out['read_finished_utc']}`。", "", "只读取已有 cheaper/equal、身份字段与已存汇总；没有重算损失/成本，没有模型、实验或归档写入。分母为17个 normalized_source 合约 × 两个 window（52、260）=34个相关合约/历史比较。", "", "两份表在 c=1、group_label=CFTC、method_id=CFTC::QR33 下的2142条记录逐字段完全相同；所有点均有34条 COMPLETE，没有未知或等价记录。完整逐行证据见 JSON 的 two_file_match.row_bindings；CSV 表头算第1行，ZIP行号指解压后 member cost-grid.csv。", "", "|原文件|SHA-256（读取前后相同）|", "|---|---|"]
    lines += [f"|`{p}`|`{s['sha256_before']}`|" for p, s in SOURCE_RECEIPTS.items()]
    lines += ["", "固定参考 F、c=1 与严格 cheaper 的定义绑定 `manifest.json#/design/reference_id`、`/design/primary_c`、`/design/ties`；计算只数 `cheaper=True`，没有由 difference 重新判定。中心按已归档轴排序位置：κ第4/7项=.1，β第5/9项=.25。", "", "|位置|κ|β|严格较便宜/分母|equal|primary行号 / ZIP member行号|", "|---|---:|---:|---:|---:|---|"]
    for example in examples:
        lines.append(f"|{example['selection']}|{example['kappa']}|{example['beta']}|{example['strict_cheaper_count']}/{example['complete_denominator']}|{example['equal_count']}|JSON examples 对应两组34行；逐项 join 到 two_file_match.row_bindings|")
    lines += ["", "## 方向与非单调例外", "", direction, "", "总体有利方向是更高κ、较低β，但不应写成必然单调：唯一例外单元是 cftc:090741、W260，κ升高有9条 True→False 相邻边，β升高有2条 False→True 相邻边。以下列出每条原始 cheaper 标记及两表行号；未重算任何金额。", "", "|方向|κ前→后|β前→后|cheaper前→后|primary行前→后|ZIP行前→后|", "|---|---|---|---|---|---|"]
    for name, values in exceptions.items():
        for e in values:
            a, b = e["before"], e["after"]
            x, y = a["archived_fields"], b["archived_fields"]
            lines.append(f"|{name}|{x['kappa']}→{y['kappa']}|{x['beta']}→{y['beta']}|{x['cheaper']}→{y['cheaper']}|{a['primary_csv_line']}→{b['primary_csv_line']}|{a['cost_grid_member_line']}→{b['cost_grid_member_line']}|")
    lines += ["", "聚合计数也不是处处单调：", "", "|方向|κ前→后|β前→后|严格较便宜计数前→后（分母均34）|", "|---|---|---|---|"]
    for e in aggregate_exceptions:
        a, b = e["before"], e["after"]
        lines.append(f"|{e['direction']}|{a['kappa']}→{b['kappa']}|{a['beta']}→{b['beta']}|{a['strict_cheaper_count']}→{b['strict_cheaper_count']}|")
    lines += ["", "完整计数矩阵（行κ、列β；每项为 cheaper=True/34，全部原始行在 JSON）：", "", "|κ / β|" + "|".join(map(str, betas)) + "|", "|---|" + "---:|" * len(betas)]
    lines += ["|" + str(k) + "|" + "|".join(str(points[k, b]["strict_cheaper_count"]) for b in betas) + "|" for k in kappas]
    lines += ["", "## 成本小节精确三句英文", ""] + three_sentences
    lines += ["", "## 其他三处同口径建议", "", "贡献3：" + out["recommended_contribution_3"], "", "RQ3结论：" + out["recommended_RQ3_answer"], "", "Letter：" + out["recommended_letter"], "", out["editorial_note"], "", "## 摘要顺带核对", "", "- `results/v10/mcs/summary.json#/overall/metrics/matched_FI_membership/count_successful=90`，`denominator_successful=98`，`fraction_successful=.9183673469387755`；逐个核对 full-cells.json 已存 included 字段得到同样90/98。可写 nearly always，但更建议精确 in 90 of 98 comparisons；这不是独占胜出。`literal_sole_FI/count_successful=2`；非排除不证明风险相等。", "- `results/v10/menu/summary.json#/across_sources/0` 的 `arm=constant,window=52,method=QR33,status=COMPLETE,complete_sources=13,original_median_pct=116.24327967680179,median_pct=.2069371499562489`，支持116.2%→0.2%；`/across_sources/4` 的 switching 对应121.40097999787356%→−.22777914491914353%。这是每来源重复中位数再跨13来源中位数，不是全部重复混合或观测商业损益。", "- 同文件 `/predictions/M2/switching_minus_constant_pct_points=-.43471629487539243`，`minimum_inclusive_percentage_points=5.0,status=NOT_SUPPORTED`。只能写注册的额外损失阈值未获支持，不能写切换无效应或两组等价。所有数值的精确字段绑定在 JSON abstract_checks。", ""]
    (OUT / "cost-reading.md").write_text("\n".join(lines))
    print(json.dumps({"status": out["status"], "matched_rows": len(receipts), "examples": [{k: e[k] for k in ("selection", "kappa", "beta", "strict_cheaper_count", "complete_denominator")} for e in examples], "all_source_hashes_unchanged": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
