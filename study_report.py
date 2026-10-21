"""Strict public aggregate serialization; no source or numerical-library inputs.

The runner supplies an already frozen schema and a parent-created staging directory.
Only the four public row lists cross this boundary. ReportLab is imported lazily
inside PDF creation. Manifest writing is separate, exclusive, and last.
"""

from dataclasses import dataclass
from decimal import Decimal
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re


CELL_IDS = ("main", "h12", "h24", "n480", "n1440", "tau90", "tau99")
METHOD_IDS = ("F", "S", "R", "L", "P0")
LENGTHS = (120, 240, 720, 1440)
TABLE_PATHS = ("results/summary.csv", "results/paired-comparison.csv",
               "results/stability.csv", "results/diagnostics.csv")
FIGURE_PATHS = (
    "manuscript/working-paper/figures/within-cell-paired-means.pdf",
    "manuscript/working-paper/figures/primary-monthly-paired-means.pdf",
    "manuscript/working-paper/figures/primary-resampling-ranges.pdf",
)
PUBLIC_PATHS = TABLE_PATHS + FIGURE_PATHS
METADATA = ("cell_id", "horizon", "window", "tau_numerator", "tau_denominator", "rank", "origin_count")
COUNT_METRICS = frozenset(("strict_breach_count", "conditional_overrun_denominator",
                           "aux_breach_count", "strict_aux_disagreement_count", "near_event_boundary_count"))
METHOD_METRICS = ("mean_pinball", "mean_capacity", "mean_extra_allowance", "strict_breach_count",
                  "strict_breach_rate", "mean_positive_overrun", "conditional_mean_overrun",
                  "conditional_overrun_denominator", "mean_unused_allowance", "aux_breach_count",
                  "strict_aux_disagreement_count", "near_event_boundary_count")
FIXED_GROUPS = (
    ("current_sign", ("negative", "zero", "positive")),
    ("development_magnitude_tercile", ("low", "middle", "high")),
    ("source_index_modulo_6", ("0", "1", "2", "3", "4", "5")),
    ("retrospective_gap_free_path", ("gap_free", "has_gap")),
)
MAX_PUBLIC_BYTES = 10485760
MAX_MANIFEST_BYTES = 1048576
SPEC_SHA256 = "0b8eda7bfd858c038bae22a96a7caa5ff21838317de58bc56eef98ca696c54ff"
SOURCE_HASH = "b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa"
SOURCE_ENDPOINT = "https://api.kaggle.com/v1/datasets.DatasetApiService/DownloadDataset"


@dataclass(slots=True)
class AggregateBundle:
    """Exactly four lists of plain, public scalar row dictionaries."""

    summary: list
    paired: list
    stability: list
    diagnostics: list


class ReportError(ValueError):
    """Fixed sanitized boundary error suitable for the runner stop-code mapping."""

    code = "OUTPUT_INTEGRITY"


def _fail():
    raise ReportError("invalid public aggregate or manifest contract")


def _public_tree(value, depth=0):
    if depth > 12:
        _fail()
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            _fail()
        for child in value.values():
            _public_tree(child, depth + 1)
    elif type(value) is list:
        for child in value:
            _public_tree(child, depth + 1)
    else:
        _scalar(value)


def _mapping(value, keys):
    if type(value) is not dict:
        raise TypeError("public records must be plain dictionaries")
    if set(value) != set(keys) or any(type(key) is not str for key in value):
        _fail()


def _list(value):
    if type(value) is not list:
        raise TypeError("public collections must be plain lists")


def _scalar(value):
    if type(value) not in (str, int, float, bool, type(None)):
        raise TypeError("public leaves must be exact built-in scalars")
    if type(value) is float and not math.isfinite(value):
        _fail()


def _integer(value, minimum=0, maximum=None, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not int:
        raise TypeError("expected an exact built-in integer")
    if value < minimum or (maximum is not None and value > maximum):
        _fail()


def _number(value, nonnegative=False, nullable=False):
    if nullable and value is None:
        return
    if type(value) is not float:
        raise TypeError("expected an exact built-in finite float")
    if not math.isfinite(value) or (nonnegative and value < 0):
        _fail()


def _boolean(value):
    if type(value) is not bool:
        raise TypeError("expected an exact built-in boolean")


def _text(value, nullable=False, pattern=None):
    if nullable and value is None:
        return
    if type(value) is not str:
        raise TypeError("expected an exact built-in string")
    if not value or len(value) > 256 or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        _fail()
    if pattern is not None and re.fullmatch(pattern, value) is None:
        _fail()


def _hash(value, nullable=False):
    _text(value, nullable=nullable, pattern=r"[0-9a-f]{64}")


def _utc(value, nullable=False):
    _text(value, nullable=nullable, pattern=r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z")
    if value is not None:
        from datetime import datetime
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            _fail()


def _close(actual, expected, count=1, scale=None):
    """Fixed arithmetic reconciliation only, never an event/score tolerance."""
    if actual == expected:
        return True
    eps = 2.0 ** -52
    qeps = (2 * count + 2) * eps
    if qeps >= 1:
        _fail()
    base = max(1.0, abs(actual), abs(expected), 0.0 if scale is None else scale)
    tolerance = 8 * qeps / (1 - qeps) * base
    return abs(actual - expected) <= tolerance


def _require_close(actual, expected, count=1, scale=None):
    if not _close(actual, expected, count, scale):
        _fail()


def _row(row, columns):
    _mapping(row, columns)
    for value in row.values():
        _scalar(value)


def _meta(row):
    if row["cell_id"] not in CELL_IDS or type(row["cell_id"]) is not str:
        _fail()
    for key in METADATA[1:]:
        _integer(row[key], 1)
    numerator, denominator, window = row["tau_numerator"], row["tau_denominator"], row["window"]
    if numerator >= denominator or row["rank"] != ((window + 1) * numerator + denominator - 1) // denominator:
        _fail()
    if row["rank"] > window:
        _fail()


def _same_meta(left, right):
    if any(left[key] != right[key] for key in METADATA):
        _fail()


def _method_values(values, count, reason):
    for metric in METHOD_METRICS:
        value = values[metric]
        if metric in COUNT_METRICS:
            _integer(value, 0, count)
        else:
            _number(value, nonnegative=True, nullable=metric == "conditional_mean_overrun")
    breaches = values["strict_breach_count"]
    if values["conditional_overrun_denominator"] != breaches:
        _fail()
    _require_close(values["strict_breach_rate"], breaches / count, count)
    if breaches == 0:
        if values["conditional_mean_overrun"] is not None or reason != "NO_STRICT_BREACHES":
            _fail()
        if values["mean_positive_overrun"] != 0.0:
            _fail()
    else:
        if values["conditional_mean_overrun"] is None or reason is not None:
            _fail()
        _require_close(values["conditional_mean_overrun"] * (breaches / count), values["mean_positive_overrun"], count)
    if values["aux_breach_count"] > breaches:
        _fail()
    if values["strict_aux_disagreement_count"] != breaches - values["aux_breach_count"]:
        _fail()


def _month_sequence(months):
    if not months:
        _fail()
    previous = None
    for month in months:
        _text(month, pattern=r"\d{4}-(?:0[1-9]|1[0-2])")
        year, month_number = map(int, month.split("-"))
        index = year * 12 + month_number - 1
        if previous is not None and index != previous + 1:
            _fail()
        previous = index


def _diagnostic_groups(bundle, schema):
    rows = bundle.diagnostics
    if len(rows) % 61 or not rows:
        _fail()
    groups = [rows[offset:offset + 61] for offset in range(0, len(rows), 61)]
    months = [group[0]["group"] for group in groups if group[0]["panel"] == "naive_origin_month"]
    _month_sequence(months)
    expected = [(panel, name) for panel, names in FIXED_GROUPS[:3] for name in names]
    expected += [("naive_origin_month", month) for month in months]
    expected += [(panel, name) for panel, names in FIXED_GROUPS[3:] for name in names]
    if [(group[0]["panel"], group[0]["group"]) for group in groups] != expected:
        _fail()
    if len(rows) != 61 * (14 + len(months)):
        _fail()
    columns = schema["tables"][TABLE_PATHS[3]]["columns"]
    main_count = bundle.paired[0]["origin_count"]
    group_keys = [(method, metric) for method in METHOD_IDS for metric in METHOD_METRICS]
    group_keys += [("F_MINUS_S", "mean_pinball_difference")]
    for group in groups:
        count = group[0]["origin_count"]
        _integer(count, 0, main_count)
        status = "DISPLAYED" if count >= 30 else "BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
        for row, key in zip(group, group_keys):
            _row(row, columns)
            if row["cell_id"] != "main" or (row["method_or_comparison"], row["metric"]) != key:
                _fail()
            if any(row[field] != group[0][field] for field in ("panel", "group", "origin_count")):
                _fail()
            if row["display_status"] != status:
                _fail()
            if count < 30:
                reason = "GROUP_BELOW_DISPLAY_MIN" if count else "NO_ORIGINS"
                if row["value"] is not None or row["undefined_reason"] != reason:
                    _fail()
            elif key[0] == "F_MINUS_S":
                _number(row["value"])
                if row["undefined_reason"] is not None:
                    _fail()
        if count >= 30:
            for index, method in enumerate(METHOD_IDS):
                method_rows = group[index * 12:(index + 1) * 12]
                values = {row["metric"]: row["value"] for row in method_rows}
                conditional_reason = method_rows[6]["undefined_reason"]
                _method_values(values, count, conditional_reason)
                if any(row["undefined_reason"] is not None for row in method_rows if row["metric"] != "conditional_mean_overrun"):
                    _fail()
            _require_close(group[60]["value"], group[0]["value"] - group[12]["value"], count,
                           count * max(group[0]["value"], group[12]["value"]))
    for panel in ("current_sign", "development_magnitude_tercile", "source_index_modulo_6", "naive_origin_month", "retrospective_gap_free_path"):
        panel_groups = [group for group in groups if group[0]["panel"] == panel]
        if sum(group[0]["origin_count"] for group in panel_groups) != main_count:
            _fail()
        # A suppressed group cannot be reconstructed. Reconcile all fully public partitions.
        if any(0 < group[0]["origin_count"] < 30 for group in panel_groups):
            continue
        displayed = [group for group in panel_groups if group[0]["origin_count"] >= 30]
        for index, method in enumerate(METHOD_IDS):
            summary = bundle.summary[index]
            for j, metric in enumerate(METHOD_METRICS):
                if metric == "conditional_mean_overrun":
                    continue
                if metric in COUNT_METRICS:
                    if sum(group[index * 12 + j]["value"] for group in displayed) != summary[metric]:
                        _fail()
                else:
                    mean = math.fsum(group[index * 12 + j]["value"] * group[0]["origin_count"] / main_count for group in displayed)
                    _require_close(mean, summary[metric], main_count,
                                   main_count * max(1.0, summary[metric], *(group[index * 12 + j]["value"] for group in displayed)))
        mean_d = math.fsum(group[60]["value"] * group[0]["origin_count"] / main_count for group in displayed)
        _require_close(mean_d, bundle.paired[0]["mean_pinball_difference"], main_count,
                       main_count * max(1.0, bundle.summary[0]["mean_pinball"], bundle.summary[1]["mean_pinball"]))
    return groups


def validate_aggregate_bundle(bundle, schema):
    """Reject unsafe/inconsistent complete public rows without coercing objects."""
    if type(bundle) is not AggregateBundle:
        raise TypeError("only AggregateBundle is a public scientific input")
    for rows, expected in zip((bundle.summary, bundle.paired, bundle.stability), (35, 7, 4)):
        _list(rows)
        if len(rows) != expected:
            _fail()
    _list(bundle.diagnostics)
    expected_summary = [(cell, method) for cell in CELL_IDS for method in METHOD_IDS]
    actual_summary = []
    references = {}
    common_count = None
    for row in bundle.summary:
        _row(row, schema["tables"][TABLE_PATHS[0]]["columns"])
        _meta(row)
        if type(row["method_id"]) is not str or row["method_id"] not in METHOD_IDS:
            _fail()
        actual_summary.append((row["cell_id"], row["method_id"]))
        if row["cell_id"] in references:
            _same_meta(row, references[row["cell_id"]])
        else:
            references[row["cell_id"]] = row
        if common_count is None:
            common_count = row["origin_count"]
        elif common_count != row["origin_count"]:
            _fail()
        _method_values(row, common_count, row["conditional_overrun_undefined_reason"])
        if row["method_id"] == "P0" and (row["mean_extra_allowance"] != 0.0 or row["mean_unused_allowance"] != 0.0):
            _fail()
    if actual_summary != expected_summary:
        _fail()
    for index, row in enumerate(bundle.paired):
        _row(row, schema["tables"][TABLE_PATHS[1]]["columns"])
        _meta(row)
        if row["cell_id"] != CELL_IDS[index]:
            _fail()
        _same_meta(row, references[row["cell_id"]])
        for key in ("f_lower_count", "equal_capacity_count", "f_higher_count", "near_fs_capacity_count",
                    "paired_scores_equal_count", "scores_changed_allowances_equal_count",
                    "allowances_changed_capacities_equal_count", "capacities_different_count"):
            _integer(row[key], 0, common_count)
        low, equal, high = row["f_lower_count"], row["equal_capacity_count"], row["f_higher_count"]
        mechanisms = [row[key] for key in ("paired_scores_equal_count", "scores_changed_allowances_equal_count",
                                          "allowances_changed_capacities_equal_count", "capacities_different_count")]
        if low + equal + high != common_count or sum(mechanisms) != common_count:
            _fail()
        if equal != sum(mechanisms[:3]) or mechanisms[3] != low + high:
            _fail()
        for fraction, count_key in (("f_lower_fraction", "f_lower_count"), ("equal_capacity_fraction", "equal_capacity_count"),
                                    ("f_higher_fraction", "f_higher_count"), ("near_fs_capacity_fraction", "near_fs_capacity_count")):
            _number(row[fraction], nonnegative=True)
            if row[fraction] > 1:
                _fail()
            _require_close(row[fraction], row[count_key] / common_count, common_count)
        _number(row["mean_pinball_difference"])
        s_loss = bundle.summary[index * 5 + 1]["mean_pinball"]
        f_loss = bundle.summary[index * 5]["mean_pinball"]
        _require_close(row["mean_pinball_difference"], f_loss - s_loss, common_count,
                       common_count * max(f_loss, s_loss))
        if s_loss == 0:
            if row["relative_difference_to_S"] is not None or row["relative_difference_undefined_reason"] != "ZERO_MEAN_LOSS_S":
                _fail()
        else:
            _number(row["relative_difference_to_S"])
            if row["relative_difference_undefined_reason"] is not None:
                _fail()
            _require_close(row["relative_difference_to_S"], row["mean_pinball_difference"] / s_loss, common_count)
    for index, row in enumerate(bundle.stability):
        _row(row, schema["tables"][TABLE_PATHS[2]]["columns"])
        _meta(row)
        _same_meta(row, references["main"])
        for key in ("ell", "replicates", "lower_rank", "upper_rank", "seed_base", "seed_length"):
            _integer(row[key], 1)
        for key in ("ell_over_origin_count", "expected_used_blocks", "observed_mean_d", "resampled_mean_average",
                    "resampled_mean_sd_ddof1", "resampled_mean_order25", "resampled_mean_order975"):
            _number(row[key])
        for key in ("constant_input", "constant_shortcut_used"):
            _boolean(row[key])
        if row["ell"] != LENGTHS[index] or row["seed_length"] != row["ell"]:
            _fail()
        for key, value in schema["tables"][TABLE_PATHS[2]]["fixed_values"].items():
            if row[key] != value or type(row[key]) is not type(value):
                _fail()
        _require_close(row["ell_over_origin_count"], row["ell"] / common_count, common_count)
        _require_close(row["expected_used_blocks"], 1 + (common_count - 1) / row["ell"], common_count)
        _require_close(row["observed_mean_d"], bundle.paired[0]["mean_pinball_difference"], common_count)
        low, high = row["resampled_mean_order25"], row["resampled_mean_order975"]
        if low > high or row["resampled_mean_sd_ddof1"] < 0:
            _fail()
        if row["constant_input"] != row["constant_shortcut_used"]:
            _fail()
        if row["constant_input"]:
            c = row["observed_mean_d"]
            if any(row[key] != c for key in ("resampled_mean_average", "resampled_mean_order25", "resampled_mean_order975")) or row["resampled_mean_sd_ddof1"] != 0.0:
                _fail()
        if row["resampled_mean_sd_ddof1"] == 0.0 and not (low == high == row["resampled_mean_average"]):
            _fail()
    _diagnostic_groups(bundle, schema)


def _csv_value(value):
    # Explicit dispatch follows validation; there is no arbitrary-object fallback.
    if value is None:
        return ""
    if type(value) is str:
        return value
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if type(value) is float and math.isfinite(value):
        return repr(value)
    raise TypeError("unsafe CSV scalar")


def _csv_bytes(rows, columns):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(columns)
    writer.writerows([_csv_value(row[column]) for column in columns] for row in rows)
    return stream.getvalue().encode("utf-8")


def _destination(destination):
    if type(destination) not in (str, Path) and not isinstance(destination, Path):
        raise TypeError("destination must be a path")
    path = Path(destination)
    if ".." in path.parts:
        _fail()
    path = path.absolute()
    for component in (path, *path.parents):
        if component.is_symlink():
            _fail()
    if not path.is_dir():
        _fail()
    return path


def _target(root, relative, create=False):
    if relative not in PUBLIC_PATHS + ("results/run-manifest.json",):
        _fail()
    path = root
    parts = relative.split("/")
    for part in parts[:-1]:
        path = path / part
        if path.is_symlink():
            _fail()
        if path.exists():
            if not path.is_dir():
                _fail()
        elif create:
            path.mkdir(mode=0o700)
    path = path / parts[-1]
    if path.is_symlink():
        _fail()
    return path


def _preflight(root, relatives):
    if _target(root, "results/run-manifest.json").exists():
        raise FileExistsError("attempt already has a final manifest")
    for relative in relatives:
        if _target(root, relative).exists():
            raise FileExistsError("public artifact already exists")


def _write(root, relative, data, kind, row_count):
    target = _target(root, relative, create=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
        stream.flush()
    actual = target.read_bytes()
    if actual != data:
        _fail()
    return dict(relative_path=relative, kind=kind, bytes=len(actual),
                sha256=hashlib.sha256(actual).hexdigest(), row_count=row_count)


def _money_label(value):
    # Decimal scaling preserves nonzero annotations even below float subnormal range.
    if value == 0:
        return "0"
    return format(Decimal(repr(value)).scaleb(-6), ".12g")


def _domain(values):
    lower, upper = min(0.0, *values), max(0.0, *values)
    if lower == upper:
        return -1.0, 1.0
    # Padding is a viewport choice only. Scientific operands are never changed.
    padding = (upper - lower) * 0.08
    if not math.isfinite(padding):
        padding = 0.0
    return lower - padding, upper + padding


def _coordinate(value, limits, start, end):
    low, high = limits
    scale = max(abs(low), abs(high))
    if scale == 0:
        return (start + end) / 2
    return start + ((value / scale - low / scale) / (high / scale - low / scale)) * (end - start)


def _canvas(title):
    from reportlab.pdfgen import canvas
    buffer = io.BytesIO()
    document = canvas.Canvas(buffer, pagesize=(792, 612), pageCompression=0, invariant=1)
    document.setTitle(title)
    document.setAuthor("")
    document.setSubject("Original public aggregate figure")
    document.setFont("Helvetica-Bold", 16)
    document.drawString(45, 574, title)
    document.setFont("Helvetica", 9)
    return buffer, document


def _finish(buffer, document):
    document.showPage()
    document.save()
    data = buffer.getvalue()
    if len(data) > MAX_PUBLIC_BYTES:
        _fail()
    return data


def _axis(document, limits, start, end, baseline, vertical=False):
    document.setStrokeColorRGB(0.75, 0.78, 0.81)
    document.setLineWidth(0.5)
    if vertical:
        document.line(baseline, start, baseline, end)
    else:
        document.line(start, baseline, end, baseline)
    document.setFont("Helvetica", 8)
    for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        value = limits[0] * (1 - fraction) + limits[1] * fraction
        point = start + (end - start) * fraction
        if vertical:
            document.drawRightString(baseline - 7, point - 3, _money_label(value))
        else:
            document.drawCentredString(point, baseline - 15, _money_label(value))


def _within_pdf(bundle):
    buffer, document = _canvas("Within-cell paired mean loss differences")
    document.drawString(45, 553, "F minus S; USD millions. Negative values favor F within the same fixed cell.")
    values = [row["mean_pinball_difference"] for row in bundle.paired]
    limits = _domain(values)
    left, right = 225, 590
    zero = _coordinate(0.0, limits, left, right)
    document.setStrokeColorRGB(0.5, 0.5, 0.5)
    document.setLineWidth(0.7)
    document.line(zero, 135, zero, 522)
    for index, row in enumerate(bundle.paired):
        y = 500 - index * 51
        document.setFont("Helvetica", 10)
        document.setFillColorRGB(0.12, 0.15, 0.18)
        label = f"{row['cell_id']}: H{row['horizon']} n{row['window']} tau {row['tau_numerator']}/{row['tau_denominator']}"
        document.drawString(45, y - 3, label)
        x = _coordinate(values[index], limits, left, right)
        document.setFillColorRGB(0.1, 0.35, 0.65)
        document.circle(x, y, 3.5, stroke=0, fill=1)
        document.setFillColorRGB(0.12, 0.15, 0.18)
        document.drawString(625, y - 3, _money_label(values[index]))
    _axis(document, limits, left, right, 135)
    document.drawString(45, 80, "Seven declared cells in fixed order; no comparison of raw losses across different tau objectives.")
    document.drawString(45, 64, "Points are finite-record paired means; the zero line is descriptive, not an inferential threshold.")
    return _finish(buffer, document)


def _monthly_pdf(bundle):
    buffer, document = _canvas("Primary monthly paired means and origin counts")
    document.drawString(45, 553, "F minus S; USD millions. Every inclusive month is retained; points are never joined across gaps.")
    rows = [row for row in bundle.diagnostics if row["panel"] == "naive_origin_month" and row["method_or_comparison"] == "F_MINUS_S"]
    values = [row["value"] for row in rows if row["value"] is not None]
    limits = _domain(values or [0.0])
    left, right, bottom, top = 125, 745, 170, 505
    zero = _coordinate(0.0, limits, bottom, top)
    document.setStrokeColorRGB(0.65, 0.65, 0.65)
    document.line(left, zero, right, zero)
    _axis(document, limits, bottom, top, left, vertical=True)
    width = (right - left) / len(rows)
    for index, row in enumerate(rows):
        x = left + width * (index + 0.5)
        document.setFillColorRGB(0.12, 0.15, 0.18)
        document.setFont("Helvetica", 8)
        document.saveState()
        document.translate(x, 122)
        document.rotate(50)
        document.drawRightString(0, 0, row["group"])
        document.restoreState()
        document.drawCentredString(x, 144, f"n={row['origin_count']}")
        if row["value"] is None:
            document.saveState()
            document.translate(x, 188)
            document.rotate(90)
            document.setFillColorRGB(0.5, 0.5, 0.5)
            document.drawString(0, 0, row["display_status"])
            document.restoreState()
        else:
            y = _coordinate(row["value"], limits, bottom, top)
            document.setFillColorRGB(0.1, 0.35, 0.65)
            document.circle(x, y, 3, stroke=0, fill=1)
            document.saveState()
            document.translate(x + 3, y + 8)
            document.rotate(55)
            document.setFont("Helvetica", 7)
            document.drawString(0, 0, _money_label(row["value"]))
            document.restoreState()
    document.setFillColorRGB(0.12, 0.15, 0.18)
    document.setFont("Helvetica", 9)
    document.drawString(45, 57, "DISPLAYED requires at least 30 origins. Empty/suppressed months have no fabricated numerical mean.")
    document.drawString(45, 41, "Group display rules do not remove origins from global scoring, calibration or resampling.")
    return _finish(buffer, document)


def _ranges_pdf(bundle):
    buffer, document = _canvas("Primary descriptive resampling-stability ranges")
    document.drawString(45, 553, "USD millions. Blue bars: stored order25/order975 endpoints. Red point: separate observed paired mean.")
    values = [row[key] for row in bundle.stability for key in ("resampled_mean_order25", "resampled_mean_order975", "observed_mean_d")]
    limits = _domain(values)
    left, right = 120, 485
    zero = _coordinate(0.0, limits, left, right)
    document.setStrokeColorRGB(0.6, 0.6, 0.6)
    document.line(zero, 180, zero, 520)
    for index, row in enumerate(bundle.stability):
        y = 480 - index * 78
        low, high, observed = (row[key] for key in ("resampled_mean_order25", "resampled_mean_order975", "observed_mean_d"))
        xlow, xhigh, xobs = [_coordinate(value, limits, left, right) for value in (low, high, observed)]
        document.setFillColorRGB(0.12, 0.15, 0.18)
        document.setFont("Helvetica", 10)
        document.drawString(45, y - 3, f"ell={row['ell']}")
        document.setStrokeColorRGB(0.1, 0.35, 0.65)
        document.setLineWidth(3)
        document.line(xlow, y, xhigh, y)
        document.setLineWidth(1)
        document.line(xlow, y - 7, xlow, y + 7)
        document.line(xhigh, y - 7, xhigh, y + 7)
        document.setFillColorRGB(0.8, 0.17, 0.16)
        document.circle(xobs, y, 3.7, stroke=0, fill=1)
        document.setFillColorRGB(0.12, 0.15, 0.18)
        document.setFont("Helvetica", 9)
        document.drawString(515, y + 14, f"Observed: {_money_label(observed)}")
        document.drawString(515, y - 1, f"Range: [{_money_label(low)}, {_money_label(high)}]")
        document.drawString(515, y - 16, f"Resampled average: {_money_label(row['resampled_mean_average'])}")
        if low == high:
            document.drawString(515, y - 31, "zero width; original endpoints retained")
    _axis(document, limits, left, right, 180)
    document.drawString(45, 115, "All four fixed lengths, each with 999 replicate identities; no widening, jitter or favorable-length selection.")
    document.drawString(45, 97, "An observed point may lie outside a resampled range. Constant-input rows use analytic identities.")
    document.drawString(45, 79, "These are descriptive paired resampling ranges, not population confidence intervals or superiority probabilities.")
    return _finish(buffer, document)


def write_aggregate_outputs(bundle, destination, schema):
    """Write exactly seven complete public artifacts, returning actual byte identities."""
    validate_aggregate_bundle(bundle, schema)
    root = _destination(destination)
    _preflight(root, PUBLIC_PATHS)
    payloads = [_csv_bytes(rows, schema["tables"][path]["columns"])
                for path, rows in zip(TABLE_PATHS, (bundle.summary, bundle.paired, bundle.stability, bundle.diagnostics))]
    payloads.extend((_within_pdf(bundle), _monthly_pdf(bundle), _ranges_pdf(bundle)))
    if sum(map(len, payloads)) > MAX_PUBLIC_BYTES:
        _fail()
    counts = [len(bundle.summary), len(bundle.paired), len(bundle.stability), len(bundle.diagnostics), None, None, None]
    return [_write(root, path, data, "table" if index < 4 else "figure", counts[index])
            for index, (path, data) in enumerate(zip(PUBLIC_PATHS, payloads))]


def _nested(manifest, schema, name, value):
    _mapping(value, schema["run_manifest"]["nested_fields"][name])


def _source_manifest(source, schema):
    _nested(None, schema, "source", source)
    constants = dict(dataset="davidlindsay1979/net-position-time-series-dataset", version=2,
                     public_url="https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset",
                     requested_member="1hourNetPositionsKaggle/1hourNetPositionsKaggle.csv",
                     expected_csv_bytes=1286391, expected_csv_sha256=SOURCE_HASH,
                     timestamp_timezone="unspecified_naive", observed_rights_label="Data files \u00a9 Original Authors",
                     raw_redistribution_verified=False)
    for key, expected in constants.items():
        if type(source[key]) is not type(expected) or source[key] != expected:
            _fail()
    _boolean(source["source_verified"])
    _boolean(source["request_performed_this_attempt"])
    if source["acquisition_mode"] not in (None, "local_reuse", "explicit_fetch"):
        _fail()
    _integer(source["accepted_csv_bytes"], 1, nullable=True)
    _hash(source["accepted_csv_sha256"], nullable=True)
    for key in ("historical_access_utc", "local_validation_utc"):
        _utc(source[key], nullable=True)
    if source["source_verified"]:
        if source["accepted_csv_bytes"] != source["expected_csv_bytes"] or source["accepted_csv_sha256"] != source["expected_csv_sha256"]:
            _fail()
        if source["local_validation_utc"] is None or source["acquisition_mode"] is None:
            _fail()
    elif any(source[key] is not None for key in ("accepted_csv_bytes", "accepted_csv_sha256", "historical_access_utc", "local_validation_utc")):
        _fail()
    if source["request_performed_this_attempt"]:
        if source["acquisition_mode"] != "explicit_fetch":
            _fail()
    elif source["download"] is not None or source["acquisition_mode"] == "explicit_fetch":
        _fail()
    download = source["download"]
    if source["source_verified"] and source["request_performed_this_attempt"] and download is None:
        _fail()
    if download is not None:
        _nested(None, schema, "source.download", download)
        if download["endpoint"] != SOURCE_ENDPOINT or type(download["endpoint"]) is not str:
            _fail()
        _integer(download["http_status"], 100, 599, nullable=True)
        _list(download["redirect_hosts"])
        _list(download["redirect_statuses"])
        if download["redirect_hosts"] not in ([], ["storage.googleapis.com"]):
            _fail()
        if download["redirect_statuses"] not in ([], [302]) or any(type(value) is not int for value in download["redirect_statuses"]):
            _fail()
        if len(download["redirect_hosts"]) != len(download["redirect_statuses"]):
            _fail()
        if download["query_present"] is not None:
            _boolean(download["query_present"])
        _integer(download["archive_bytes"], 0, 26214400, nullable=True)
        _hash(download["archive_sha256"], nullable=True)
        if source["source_verified"] and (download["http_status"] != 200 or download["archive_bytes"] is None or download["archive_sha256"] is None):
            _fail()


def _spec_manifest(specification, schema):
    _nested(None, schema, "specification", specification)
    if specification["relative_path"] != "protocol/study-spec.json" or specification["sha256"] != SPEC_SHA256:
        _fail()
    _integer(specification["schema_version"], 1, 1)
    if specification["primary_cell_id"] != "main" or specification["amends_sha256"] is not None:
        _fail()
    _hash(specification["common_origin_reference_sha256"], nullable=True)
    _list(specification["cells"])
    expected = (("main", 6, 720, 19, 20, 685), ("h12", 12, 720, 19, 20, 685),
                ("h24", 24, 720, 19, 20, 685), ("n480", 6, 480, 19, 20, 457),
                ("n1440", 6, 1440, 19, 20, 1369), ("tau90", 6, 720, 9, 10, 649),
                ("tau99", 6, 720, 99, 100, 714))
    if len(specification["cells"]) != 7:
        _fail()
    keys = schema["run_manifest"]["nested_fields"]["specification.cells[]"]
    for row, values in zip(specification["cells"], expected):
        _mapping(row, keys)
        for key, expected_value in zip(keys, values):
            if type(row[key]) is not type(expected_value) or row[key] != expected_value:
                _fail()
    bounds = specification["evaluation_bounds"]
    _nested(None, schema, "specification.evaluation_bounds", bounds)
    if all(value is None for value in bounds.values()):
        if specification["common_origin_reference_sha256"] is not None:
            _fail()
    else:
        for key, value in bounds.items():
            _integer(value, 1 if key == "origin_count" else 0)
        if bounds["last_source_index"] - bounds["first_source_index"] + 1 != bounds["origin_count"]:
            _fail()
        if specification["common_origin_reference_sha256"] is None:
            _fail()


def _code_environment(manifest, schema, complete):
    code = manifest["code"]
    _nested(None, schema, "code", code)
    _text(code["revision"], nullable=True, pattern=r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
    _list(code["files"])
    names = []
    for record in code["files"]:
        _nested(None, schema, "code.files[]", record)
        _text(record["relative_path"])
        _hash(record["sha256"])
        names.append(record["relative_path"])
    allowed = schema["run_manifest"]["code_file_allowlist"]
    if len(names) != len(set(names)) or any(name not in allowed for name in names):
        _fail()
    if complete and set(names) != set(allowed):
        _fail()
    environment = manifest["environment"]
    _nested(None, schema, "environment", environment)
    for key in ("python_implementation", "python_version", "os_family", "os_version", "architecture", "numpy_version", "reportlab_version"):
        _text(environment[key], nullable=True, pattern=r"[A-Za-z0-9][A-Za-z0-9._+-]{0,79}")
    requests = environment["thread_requests"]
    _nested(None, schema, "environment.thread_requests", requests)
    for value in requests.values():
        if value is not None and (type(value) is not str or value != "1"):
            _fail()
    if complete:
        for key, expected in (("python_implementation", "CPython"), ("python_version", "3.12.14"),
                              ("os_family", "Darwin"), ("numpy_version", "2.3.5"), ("reportlab_version", "4.4.9")):
            if environment[key] != expected:
                _fail()
        if environment["os_version"] is None or environment["architecture"] is None or any(value != "1" for value in requests.values()):
            _fail()


def _resources_manifest(resources, schema, complete):
    _nested(None, schema, "resources", resources)
    for key in ("started_utc", "checkpoint_utc"):
        _utc(resources[key], nullable=True)
    if resources["measurement_point"] != "final_checkpoint_before_manifest":
        _fail()
    _integer(resources["requested_numerical_threads"], 1, 1)
    _number(resources["elapsed_seconds"], nonnegative=True, nullable=True)
    for key in ("peak_rss_bytes", "maximum_observed_os_threads", "thread_snapshot_count", "completed_origins_current_cell",
                "completed_replicates_current_length", "new_output_bytes_at_checkpoint", "private_numeric_output_bytes_at_checkpoint",
                "public_analysis_output_bytes_at_checkpoint"):
        _integer(resources[key], 0, nullable=True)
    if resources["thread_probe_status"] not in ("PASS", "FAIL", "UNVERIFIED", "NOT_RUN"):
        _fail()
    _list(resources["completed_stability_lengths"])
    lengths = resources["completed_stability_lengths"]
    if any(type(value) is not int or value not in LENGTHS for value in lengths) or lengths != [ell for ell in LENGTHS if ell in lengths]:
        _fail()
    _text(resources["current_stage"], nullable=True, pattern=r"[A-Za-z][A-Za-z0-9_-]{0,79}")
    if resources["current_cell_id"] is not None and (type(resources["current_cell_id"]) is not str or resources["current_cell_id"] not in CELL_IDS):
        _fail()
    if resources["current_length"] is not None:
        _integer(resources["current_length"], 1)
        if resources["current_length"] not in LENGTHS:
            _fail()
    if resources["completed_replicates_current_length"] is not None and resources["completed_replicates_current_length"] > 999:
        _fail()
    if complete:
        required = ("started_utc", "checkpoint_utc", "elapsed_seconds", "peak_rss_bytes", "maximum_observed_os_threads",
                    "thread_snapshot_count", "new_output_bytes_at_checkpoint", "private_numeric_output_bytes_at_checkpoint", "public_analysis_output_bytes_at_checkpoint")
        if any(resources[key] is None for key in required):
            _fail()
        if not (0.0 <= resources["elapsed_seconds"] < 540.0 and 0 < resources["peak_rss_bytes"] <= 2147483648):
            _fail()
        if not (0 < resources["maximum_observed_os_threads"] <= 2 and resources["thread_snapshot_count"] > 0):
            _fail()
        if resources["thread_probe_status"] != "PASS" or lengths != list(LENGTHS):
            _fail()
        public = resources["public_analysis_output_bytes_at_checkpoint"]
        private = resources["private_numeric_output_bytes_at_checkpoint"]
        new = resources["new_output_bytes_at_checkpoint"]
        if public > MAX_PUBLIC_BYTES or private > 67108864 or new > 83886080 or public + private > new:
            _fail()


def _artifact_manifest(records, schema, complete):
    _list(records)
    names = []
    for record in records:
        _nested(None, schema, "outputs.artifacts[]", record)
        _text(record["relative_path"])
        name = record["relative_path"]
        if name not in PUBLIC_PATHS:
            _fail()
        names.append(name)
        kind = "table" if name in TABLE_PATHS else "figure"
        if type(record["kind"]) is not str or record["kind"] != kind:
            _fail()
        _integer(record["bytes"], 1, MAX_PUBLIC_BYTES)
        _hash(record["sha256"])
        if kind == "figure":
            if record["row_count"] is not None:
                _fail()
        else:
            _integer(record["row_count"], 0)
            if complete:
                expected = {TABLE_PATHS[0]: 35, TABLE_PATHS[1]: 7, TABLE_PATHS[2]: 4}.get(name)
                if expected is not None and record["row_count"] != expected:
                    _fail()
                if name == TABLE_PATHS[3] and (record["row_count"] < 915 or record["row_count"] % 61):
                    _fail()
    if names != [name for name in PUBLIC_PATHS if name in names] or sum(record["bytes"] for record in records) > MAX_PUBLIC_BYTES:
        _fail()
    if complete and names != list(PUBLIC_PATHS):
        _fail()


def validate_run_manifest(manifest, schema):
    """Validate exact nested public metadata, including truthful incomplete nulls."""
    _mapping(manifest, schema["run_manifest"]["top_level_fields"])
    _public_tree(manifest)
    _integer(manifest["manifest_schema_version"], 1, 1)
    if manifest["declared_scope"] != "seven_cell_sampled_inventory_peak_study" or manifest["study_id"] != "sampled-inventory-peaks-v1":
        _fail()
    _text(manifest["attempt_id"], pattern=r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")
    if manifest["run_status"] not in schema["run_manifest"]["run_status"] or type(manifest["run_status"]) is not str:
        _fail()
    complete = manifest["run_status"] == "COMPLETE"
    if manifest["stop_code"] not in schema["run_manifest"]["stop_code"] or type(manifest["stop_code"]) is not str:
        _fail()
    if (manifest["stop_code"] == "NONE") != complete:
        _fail()
    for key in ("planned_cell_ids", "completed_cell_ids", "method_ids"):
        _list(manifest[key])
        if any(type(value) is not str for value in manifest[key]):
            _fail()
    if manifest["planned_cell_ids"] != list(CELL_IDS) or manifest["method_ids"] != list(METHOD_IDS):
        _fail()
    completed = manifest["completed_cell_ids"]
    if completed != [cell for cell in CELL_IDS if cell in completed] or (complete and completed != list(CELL_IDS)):
        _fail()
    _source_manifest(manifest["source"], schema)
    _spec_manifest(manifest["specification"], schema)
    _code_environment(manifest, schema, complete)
    _resources_manifest(manifest["resources"], schema, complete)
    _nested(None, schema, "checks", manifest["checks"])
    for value in manifest["checks"].values():
        if type(value) is not str or value not in schema["run_manifest"]["checks_status"]:
            _fail()
    _nested(None, schema, "outputs", manifest["outputs"])
    _artifact_manifest(manifest["outputs"]["artifacts"], schema, complete)
    conventions = manifest["undefined_conventions"]
    _nested(None, schema, "undefined_conventions", conventions)
    expected = dict(csv_empty_is_null=True, json_nonfinite_allowed=False,
                    zero_breach_reason="NO_STRICT_BREACHES", zero_s_loss_reason="ZERO_MEAN_LOSS_S",
                    display_min_origins=30, below_display_reason="GROUP_BELOW_DISPLAY_MIN", empty_group_reason="NO_ORIGINS")
    for key, value in expected.items():
        if type(conventions[key]) is not type(value) or conventions[key] != value:
            _fail()
    if complete:
        if not manifest["source"]["source_verified"] or any(value != "PASS" for value in manifest["checks"].values()):
            _fail()
        if manifest["specification"]["evaluation_bounds"]["origin_count"] is None:
            _fail()


def _parse_public_csv(data, path, schema):
    try:
        reader = csv.reader(io.StringIO(data.decode("utf-8"), newline=""), strict=True)
        columns = next(reader)
        if columns != schema["tables"][path]["columns"]:
            _fail()
        rows = []
        text_fields = {"cell_id", "method_id", "conditional_overrun_undefined_reason", "relative_difference_undefined_reason",
                       "generator", "panel", "group", "method_or_comparison", "metric", "display_status", "undefined_reason"}
        integer_fields = set(METADATA[1:]) | COUNT_METRICS | {
            "f_lower_count", "equal_capacity_count", "f_higher_count", "near_fs_capacity_count", "paired_scores_equal_count",
            "scores_changed_allowances_equal_count", "allowances_changed_capacities_equal_count", "capacities_different_count",
            "ell", "replicates", "lower_rank", "upper_rank", "seed_base", "seed_length"}
        for fields in reader:
            if len(fields) != len(columns):
                _fail()
            row = {}
            for key, value in zip(columns, fields):
                if value == "":
                    row[key] = None
                elif key in text_fields:
                    row[key] = value
                elif key in ("constant_input", "constant_shortcut_used"):
                    if value not in ("true", "false"):
                        _fail()
                    row[key] = value == "true"
                elif key in integer_fields:
                    if re.fullmatch(r"(?:0|[1-9][0-9]*)", value) is None:
                        _fail()
                    row[key] = int(value)
                elif key == "value" and row.get("metric") in COUNT_METRICS:
                    if re.fullmatch(r"(?:0|[1-9][0-9]*)", value) is None:
                        _fail()
                    row[key] = int(value)
                else:
                    row[key] = float(value)
                    if not math.isfinite(row[key]):
                        _fail()
            rows.append(row)
        return rows
    except (UnicodeError, csv.Error, StopIteration, OverflowError):
        _fail()


def _verify_artifacts(manifest, root, schema):
    tables = {}
    for record in manifest["outputs"]["artifacts"]:
        target = _target(root, record["relative_path"])
        if not target.is_file() or target.stat().st_size != record["bytes"]:
            _fail()
        if target.stat().st_size > MAX_PUBLIC_BYTES:
            _fail()
        data = target.read_bytes()
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            _fail()
        if record["kind"] == "table":
            rows = _parse_public_csv(data, record["relative_path"], schema)
            if len(rows) != record["row_count"]:
                _fail()
            tables[record["relative_path"]] = rows
        elif not data.startswith(b"%PDF-"):
            _fail()
    if manifest["run_status"] == "COMPLETE":
        bundle = AggregateBundle(*(tables[path] for path in TABLE_PATHS))
        validate_aggregate_bundle(bundle, schema)
        count = manifest["specification"]["evaluation_bounds"]["origin_count"]
        if count != bundle.paired[0]["origin_count"]:
            _fail()
        for row, cell in zip(bundle.paired, manifest["specification"]["cells"]):
            if any(row[key] != cell[key] for key in ("cell_id", "horizon", "window", "tau_numerator", "tau_denominator")) or row["rank"] != cell["expected_rank"]:
                _fail()


def write_run_manifest(manifest, destination, schema):
    """Verify recorded artifacts, then exclusively write the final public manifest."""
    validate_run_manifest(manifest, schema)
    root = _destination(destination)
    _preflight(root, ("results/run-manifest.json",))
    _verify_artifacts(manifest, root, schema)
    data = (json.dumps(manifest, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
    if len(data) > MAX_MANIFEST_BYTES:
        _fail()
    return _write(root, "results/run-manifest.json", data, "manifest", None)
