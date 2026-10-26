"""Frozen CFTC TFF parsing/universe helpers; bytes in, JSON-native objects out.

No network, filesystem acquisition, extraction, forecasting or empirical study
runs occur here. The caller owns the committed design and archive provenance.
"""
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from fractions import Fraction
import csv
import hashlib
import io
import math
import re
import zipfile


class CFTCDataError(ValueError):
    """A dataset-wide identity/schema/calendar failure, never a repaired row."""


def _integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('invalid integer configuration')
    return value


def _economic_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise CFTCDataError('INVALID_POSITION_DATE')
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise CFTCDataError('INVALID_POSITION_DATE') from exc
    if result > datetime.now(timezone.utc).date():
        raise CFTCDataError('FUTURE_POSITION_DATE')
    return result


def _code(value):
    if not isinstance(value, str) or not value.strip():
        raise CFTCDataError('MISSING_CONTRACT_CODE')
    return value.strip()


def _week(value):
    return (value-timedelta(days=value.weekday())).isoformat()


def _count(value, allow_zero_fraction=False):
    text = value.strip() if isinstance(value, str) else ''
    pattern = r'(?:[0-9]+|[0-9]{1,3}(?:,[0-9]{3})+)'
    if allow_zero_fraction is True:
        pattern += r'(?:\.0+)?'
    if not re.fullmatch(pattern, text):
        return None
    try:
        # The grammar proves that every fractional digit is zero. Parse the
        # integer text directly; never round or cast a floating count.
        result = int(text.split('.', 1)[0].replace(',', ''))
        return result if math.isfinite(float(result)) else None
    except (ValueError, OverflowError):
        return None


def _full_date(value, accepted_literal_suffix=None):
    text = value.strip()
    # The caller verifies the separately committed ingestion clarification.
    # Its only extension is this exact terminal midnight decoration; the
    # registered date formats and primary-date equality remain unchanged.
    if (accepted_literal_suffix == ' 12:00:00 AM'
            and text.endswith(accepted_literal_suffix)):
        text = text[:-len(accepted_literal_suffix)]
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', text):
            return date.fromisoformat(text)
        if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', text):
            return datetime.strptime(text, '%m/%d/%Y').date()
    except ValueError:
        pass
    raise CFTCDataError('INVALID_FULL_POSITION_DATE')


def read_archive(raw_bytes, ownership, design):
    """Parse one owned official archive without extracting or repairing rows.

    Bad dates/code/schema raise CFTCDataError for the whole data stage. Bad
    counts remain attached to the named code with errors, allowing the fixed
    universe selector to mark that entire contract ineligible. Exclusion audit
    pointers plus retained raw ZIP bytes reconstruct every ownership exclusion.
    """
    if not isinstance(raw_bytes, bytes):
        raise CFTCDataError('ARCHIVE_BYTES_REQUIRED')
    first = _integer(ownership['first_position_year'], 2000)
    last = _integer(ownership['last_position_year'], first)
    try:
        with zipfile.ZipFile(io.BytesIO(raw_bytes)) as archive:
            tables = [m for m in archive.infolist() if not m.is_dir()
                      and m.filename.lower().endswith(('.txt', '.csv'))]
            if len(tables) != 1:
                raise CFTCDataError('EXACTLY_ONE_TABLE_REQUIRED')
            payload = tables[0].filename
            content = archive.read(tables[0])
    except (zipfile.BadZipFile, RuntimeError, OSError, EOFError, NotImplementedError) as exc:
        raise CFTCDataError('INVALID_ARCHIVE') from exc
    encoding = 'utf-8-sig'
    try:
        text = content.decode(encoding)
    except UnicodeDecodeError:
        encoding = 'cp1252'
        try:
            text = content.decode(encoding)
        except UnicodeDecodeError as exc:
            raise CFTCDataError('TEXT_ENCODING') from exc
    reader = csv.DictReader(io.StringIO(text, newline=''), strict=True)
    try:
        fields = reader.fieldnames
        if (not fields or len(set(fields)) != len(fields)
                or any(name not in fields for name in design['required_columns'])):
            raise CFTCDataError('REQUIRED_SCHEMA')
        audit = dict(file=ownership['file'], url=ownership['url'], payload=payload,
            archive_bytes=len(raw_bytes), archive_sha256=hashlib.sha256(raw_bytes).hexdigest(),
            encoding=encoding, fieldnames=fields, raw_rows=0, retained_rows=0,
            ownership_excluded_count=0, ownership_excluded_rows=[], invalid_count_rows=0,
            report_type_markers={}, report_type_marker_present='FutOnly_or_Combined' in fields)
        rows = []
        marker_counts = Counter()
        last_line = reader.line_num
        for original in reader:
            line_start = last_line+1
            last_line = reader.line_num
            audit['raw_rows'] += 1
            if None in original or any(v is None for v in original.values()):
                raise CFTCDataError('RAGGED_CSV_RECORD')
            code = _code(original['CFTC_Contract_Market_Code'])
            compact = original['As_of_Date_In_Form_YYMMDD'].strip()
            if not re.fullmatch(r'[0-9]{6}', compact):
                raise CFTCDataError('INVALID_COMPACT_POSITION_DATE')
            try:
                actual = date(2000+int(compact[:2]), int(compact[2:4]), int(compact[4:6]))
            except ValueError as exc:
                raise CFTCDataError('INVALID_COMPACT_POSITION_DATE') from exc
            actual = _economic_date(actual.isoformat())
            clarification = design.get('ingestion_clarification') or {}
            literal_suffix = clarification.get('accepted_literal_suffix')
            for alias in design['date_header_aliases']:
                if alias in fields and _full_date(original[alias], literal_suffix) != actual:
                    raise CFTCDataError('INCONSISTENT_POSITION_DATES')
            if 'FutOnly_or_Combined' in fields:
                # The report identity applies to the entire payload, including
                # rows excluded by the predeclared position-year ownership.
                marker_counts[original['FutOnly_or_Combined'].strip()] += 1
            if not first <= actual.year <= last:
                audit['ownership_excluded_rows'].append(dict(file=ownership['file'],
                    payload=payload, record=audit['raw_rows'], line_start=line_start,
                    line_end=reader.line_num, position_date=actual.isoformat(),
                    reason='OUTSIDE_OWNERSHIP_YEAR'))
                audit['ownership_excluded_count'] += 1
                continue
            errors = []
            counts = {}
            count_clarification = design.get('count_notation_clarification') or {}
            allow_zero_fraction = count_clarification.get('accepted_zero_fraction') is True
            for key, column in [('open_interest', 'Open_Interest_All'),
                                ('long', 'Dealer_Positions_Long_All'),
                                ('short', 'Dealer_Positions_Short_All')]:
                counts[key] = _count(original[column], allow_zero_fraction)
                if counts[key] is None:
                    errors.append('INVALID_'+key.upper())
            if errors:
                audit['invalid_count_rows'] += 1
            net = None if counts['long'] is None or counts['short'] is None else counts['long']-counts['short']
            rows.append(dict(code=code, name=original['Market_and_Exchange_Names'].strip(),
                exchange=original['CFTC_Market_Code'].strip(), units=original['Contract_Units'].strip(),
                position_date=actual.isoformat(), week=_week(actual), **counts,
                net=net, errors=errors, source_file=ownership['file'], source_payload=payload,
                source_record=audit['raw_rows'], source_line_start=line_start,
                source_line_end=reader.line_num))
        audit['retained_rows'] = len(rows)
        audit['report_type_markers'] = dict(sorted(marker_counts.items()))
        if 'report_type_marker' in design:
            for marker in marker_counts:
                normalized = re.sub(r'[^A-Z0-9]', '', marker.upper())
                if marker and normalized not in ('FUTONLY', 'FUTURESONLY'):
                    raise CFTCDataError('INVALID_REPORT_TYPE_MARKER')
        if 'required_year_payload' in design and not rows:
            raise CFTCDataError('EMPTY_REQUIRED_YEAR_PAYLOAD')
        return rows, audit
    except csv.Error as exc:
        raise CFTCDataError('MALFORMED_CSV') from exc


def split_indices(N, H=6):
    """Exact 52/260 split with H unissued origins and fully mature outcomes."""
    _integer(N, 1); _integer(H, 1)
    evaluation_first = N-H-260
    validation_last = evaluation_first-H-1
    validation_first = validation_last-51
    if validation_first < 0:
        raise ValueError('INSUFFICIENT_SPLIT_HISTORY')
    return dict(validation_first=validation_first, validation_last=validation_last,
                evaluation_first=evaluation_first, evaluation_last=N-H-1,
                validation_n=52, evaluation_n=260, unissued_gap_n=H)


def _enough_history(N, design):
    h = _integer(design['horizon'], 1)
    step = _integer(design['refit_step'], 1)
    minimum_feature = max(24, _integer(design.get('feature_rms_short', 6), 1),
                          _integer(design['feature_rms_long'], 1))
    windows = [_integer(w, 1) for w in design['windows']]
    try:
        first = split_indices(N, h)['validation_first']
    except ValueError:
        return False
    for window in windows:
        if first-h-window+1 < minimum_feature:
            return False
        if math.ceil((window+1)*19/20) > window:
            return False
    ancillary = design.get('ancillary', {})
    if ancillary.get('methods'):
        from v6_aci import initialization_grid
        minimum = _integer(ancillary.get('minimum_calibration', 19), 1)
        for window in windows:
            for method in ancillary['methods']:
                feature_min = minimum_feature if method == 'ACI_QR33' else 0
                grid = initialization_grid(first, h, window, step, feature_min)
                if grid['mature_initial_count'] < minimum:
                    return False
    return True


def _normal_exchange(value):
    return value.strip().upper() if isinstance(value, str) else ''


def _normal_units(value):
    return ' '.join(value.upper().replace(',', '').split()) if isinstance(value, str) else ''


def _valid_counts(row):
    values = [row.get(k) for k in ('open_interest', 'long', 'short')]
    if row.get('errors') or any(type(v) is not int or v < 0 for v in values):
        return False
    try:
        if not all(math.isfinite(float(v)) for v in values):
            return False
    except OverflowError:
        return False
    return type(row.get('net')) is int and row['net'] == row['long']-row['short']


def _name_spans(rows):
    by_name = defaultdict(list)
    for row in rows:
        by_name[str(row.get('name', ''))].append(row['position_date'])
    result = [dict(name=name, first_date=min(dates), last_date=max(dates), rows=len(dates))
              for name, dates in by_name.items()]
    return sorted(result, key=lambda item: (item['first_date'], item['name']))


def select_universe(rows, design):
    """Apply fixed whole-code filters, then rank common-calendar mean total OI.

    Calendar endpoint uses every owned legal date/code before numeric or scope
    exclusion. Duplicate weeks are never collapsed. Only selected complete
    codes receive model arrays; all codes retain eligibility metadata.
    """
    start = date.fromisoformat(design['first_expected_week'])
    if start.weekday() != 0:
        raise ValueError('FIRST_EXPECTED_WEEK_NOT_MONDAY')
    first_position = date.fromisoformat(design['first_included_position_date'])
    groups = defaultdict(list)
    all_weeks = []
    outside_start = 0
    for row in rows:
        code = _code(row.get('code'))
        actual = _economic_date(row.get('position_date'))
        expected_week = _week(actual)
        if actual < first_position or expected_week < start.isoformat():
            outside_start += 1
            continue
        groups[code].append(row)
        all_weeks.append(expected_week)
    result = dict(status='UNAVAILABLE', calendar=[], selected=[], contracts=[],
                  arrays_by_code={}, N=0, before_start_rows=outside_start)
    if not all_weeks:
        return result
    latest = date.fromisoformat(max(all_weeks))
    calendar = [(start+timedelta(weeks=i)).isoformat()
                for i in range((latest-start).days//7+1)]
    expected = set(calendar)
    history_ok = _enough_history(len(calendar), design)
    prefixes = tuple(design['known_scope_change_excluded_code_prefixes'])
    rank_totals = {}
    for code in sorted(groups):
        entries = groups[code]
        reasons = []
        # Invalid week objects stay in entries and fail the whole code; only
        # strings can be keys in its audit counter, never a repaired model row.
        weeks = Counter(r.get('week') for r in entries if isinstance(r.get('week'), str))
        missing = sorted(expected-set(weeks))
        duplicates = sorted(w for w, count in weeks.items() if count > 1)
        if any(r.get('week') != _week(date.fromisoformat(r['position_date'])) for r in entries):
            reasons.append('INVALID_WEEK')
        if duplicates:
            reasons.append('DUPLICATE_WEEK')
        if missing:
            reasons.append('MISSING_WEEK')
        exchange = {_normal_exchange(r.get('exchange')) for r in entries}
        units = {_normal_units(r.get('units')) for r in entries}
        if '' in exchange:
            reasons.append('INVALID_EXCHANGE')
        if len(exchange) != 1:
            reasons.append('UNSTABLE_EXCHANGE')
        if '' in units:
            reasons.append('INVALID_UNITS')
        if len(units) != 1:
            reasons.append('UNSTABLE_UNITS')
        counts_valid = all(_valid_counts(row) for row in entries)
        if not counts_valid:
            reasons.append('INVALID_COUNTS')
        if code.startswith(prefixes):
            reasons.append('KNOWN_SCOPE_CHANGE_PREFIX')
        if not history_ok:
            reasons.append('INSUFFICIENT_HISTORY')
        full_unique_counts = counts_valid and not missing and not duplicates and 'INVALID_WEEK' not in reasons
        total = sum(r['open_interest'] for r in entries) if full_unique_counts else None
        mean = float(Fraction(total, len(calendar))) if total is not None else None
        eligible = not reasons
        metadata = dict(code=code, eligible=eligible, selected=False, reasons=reasons,
            mean_open_interest=mean, observations=len(entries), required_weeks=len(calendar),
            missing_weeks=missing, duplicate_weeks=duplicates, exchanges=sorted(exchange),
            normalized_units=sorted(units), name_spans=_name_spans(entries),
            first_position_date=min(r['position_date'] for r in entries),
            last_position_date=max(r['position_date'] for r in entries))
        result['contracts'].append(metadata)
        if eligible:
            rank_totals[code] = total
    limit = _integer(design['top_contracts'], 1)
    selected = sorted(rank_totals, key=lambda code: (-rank_totals[code], code))[:limit]
    for metadata in result['contracts']:
        metadata['selected'] = metadata['code'] in selected
    arrays = {}
    for code in selected:
        by_week = {r['week']: r for r in groups[code]}
        ordered = [by_week[week] for week in calendar]
        arrays[code] = dict(position=[float(r['net']) for r in ordered],
            actual_dates=[r['position_date'] for r in ordered], model_dates=calendar[:])
    result.update(status='AVAILABLE' if selected else 'UNAVAILABLE', calendar=calendar,
                  selected=selected, arrays_by_code=arrays, N=len(calendar))
    return result
