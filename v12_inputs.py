"""Pinned local inputs and protocol-owned v12 grids, without fits or scoring.

Inventory/grid construction reads saved metadata only. Financial CSV/NPZ parsing
is explicit in load_series; callers own the committed-code/protocol run gate.
Import performs no I/O. No acquisition or old-repository entry point is used.
"""
from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat

import numpy as np


ROOT = Path(__file__).resolve().parent
PROTOCOLS = {'F1':'loss-decomposition-design.md',
             'F2':'validation-length-design.md', 'F3':'tau-design.md'}


def _protocol(experiment, root):
    if experiment not in PROTOCOLS:
        raise ValueError('UNKNOWN_EXPERIMENT')
    text = (Path(root)/'protocol/v12'/PROTOCOLS[experiment]).read_text()
    blocks = re.findall(r'```json\s*\n(.*?)\n```', text, re.S)
    if len(blocks) != 1:
        raise ValueError('PROTOCOL_JSON_REQUIRED')
    result = json.loads(blocks[0])
    if result.get('experiment') != experiment:
        raise ValueError('PROTOCOL_EXPERIMENT_MISMATCH')
    return result


def _path(value, root):
    root = Path(root).absolute()
    path = Path(value)
    if not path.is_absolute():
        path = root/path
    # macOS gives TemporaryDirectory a /var path although that system prefix
    # resolves to /private/var. Normalize the caller's trusted root itself;
    # retain explicit symlink checks on every descendant.
    if path.is_relative_to(root):
        path = root.resolve()/path.relative_to(root)
    if '金融数学论文-修订v3-20261023' in path.parts:
        raise ValueError('SOURCE_POLICY_NO_V3_ACCESS')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('SOURCE_SYMLINK')
    return path


def _pinned_bytes(source, root):
    path = _path(source['path'], root)
    try:
        with path.open('rb') as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError('SOURCE_NOT_REGULAR')
            if before.st_size != source['bytes']:
                raise ValueError('SOURCE_SIZE_MISMATCH')
            raw = stream.read(source['bytes']+1)
            after = os.fstat(stream.fileno())
    except OSError as error:
        raise ValueError('SOURCE_IO') from error
    if (before.st_size,before.st_mtime_ns,before.st_ctime_ns) != (
            after.st_size,after.st_mtime_ns,after.st_ctime_ns):
        raise ValueError('SOURCE_CHANGED_DURING_READ')
    if len(raw) != source['bytes']:
        raise ValueError('SOURCE_SIZE_MISMATCH')
    if hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise ValueError('SOURCE_HASH_MISMATCH')
    return raw


def _settings(geometry):
    return dict(short_scale=int(geometry['short']),long_scale=int(geometry['long']),
                nominal_gap_seconds=int(geometry['gap_seconds']),N=int(geometry['N']))


def source_inventory(root=ROOT):
    """Return all 31 protocol-pinned sources; never parse their observations."""
    root = Path(root)
    design = _protocol('F1',root)
    provenance = design['input_provenance']
    geometry = {g['family']:g for g in design['geometries']}
    raw = provenance['raw_sources']
    sources = []
    for item in provenance['cftc_sources']:
        sources.append(dict(family='cftc',key=item['code'],source_index=item['source_index'],
            path=str(root/item['path']),sha256=item['sha256'],bytes=item['bytes'],
            unit='contracts',**_settings(geometry['cftc'])))
    bill_raw = next(row for row in raw if Path(row['path']).name=='PDPOSGS-B.csv')
    bill = dict(bill_raw,family='bill',key='PDPOSGS-B',
                path=str(root/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv'),
                unit='USD millions',raw_rows=bill_raw['rows'],**_settings(geometry['bill']))
    selection_path = root/'results/supervisor-20261023/e5/inputs/panel/selection-manifest.json'
    selection_raw = selection_path.read_bytes()
    if hashlib.sha256(selection_raw).hexdigest() != provenance['panel_selection_sha256']:
        raise ValueError('PANEL_SELECTION_HASH_MISMATCH')
    selection = json.loads(selection_raw)
    by_key = {Path(row['path']).stem:row for row in raw
              if Path(row['path']).parent.name=='panel'}
    for key in selection['eligible']:
        row = by_key[key]
        sources.append(dict(row,family='panel',key=key,unit='USD millions',
            raw_rows=row['rows'],grid_source=bill.copy(),**_settings(geometry['panel'])))
    sources.append(bill)
    fx_raw = next(row for row in raw if Path(row['path']).name=='1hourNetPositionsKaggle.csv')
    sources.append(dict(fx_raw,family='fx',key='fx_hourly',unit='USD',
                        raw_rows=fx_raw['rows'],**_settings(geometry['fx_original'])))
    expected = {('fx' if name=='fx_original' else name):g['sources']
                for name,g in geometry.items()}
    if any(sum(s['family']==family for s in sources)!=n for family,n in expected.items()):
        raise ValueError('SOURCE_INVENTORY_COUNT_MISMATCH')
    return sources


def _csv_columns(raw, source):
    family = source['family']
    expected = (['datetime','NetPosUsd','NetUsdPnL','AbsVolume','Mid'] if family=='fx'
                else ['As Of Date','Time Series','Value (millions)'])
    reader = csv.reader(io.StringIO(raw.decode('utf-8-sig'),newline=''),strict=True)
    if next(reader,None) != expected:
        raise ValueError('SOURCE_SCHEMA')
    dates, positions = [], []
    for row in reader:
        if len(row) != len(expected):
            raise ValueError('SOURCE_SCHEMA')
        if family != 'fx' and row[1] != source['key']:
            raise ValueError('SOURCE_KEY')
        try:
            stamp = datetime.strptime(row[0],'%Y.%m.%dT%H:%M:%S.%f' if family=='fx' else '%Y-%m-%d')
        except ValueError as error:
            raise ValueError('SOURCE_CHRONOLOGY') from error
        if family != 'fx' and re.fullmatch(r'\d{4}-\d{2}-\d{2}',row[0]) is None:
            raise ValueError('SOURCE_CHRONOLOGY')
        try:
            token = row[1 if family=='fx' else 2].strip()
            if re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',token) is None:
                raise ValueError('SOURCE_POSITION')
            value = float(token)
        except (ValueError,OverflowError) as error:
            raise ValueError('SOURCE_POSITION') from error
        if not np.isfinite(value):
            raise ValueError('SOURCE_POSITION')
        dates.append(stamp)
        positions.append(value)
    times = np.asarray(dates,dtype='datetime64[us]')
    if len(times)==0 or len(set(dates)) != len(times):
        raise ValueError('SOURCE_CHRONOLOGY')
    # Original panel alignment is keyed to the fixed Treasury grid. Other
    # sources retain their source order and must already be increasing.
    if family != 'panel' and np.any(times[1:]<=times[:-1]):
        raise ValueError('SOURCE_CHRONOLOGY')
    if 'raw_rows' in source and len(times) != source['raw_rows']:
        raise ValueError('SOURCE_ROW_COUNT')
    return np.asarray(positions,dtype=np.float64),times


def _readonly(value):
    result = np.array(value,copy=True)
    result.flags.writeable = False
    return result


def load_series(source: dict, root=ROOT):
    """Verify size/SHA before parsing one local series; return no labels/scores."""
    raw = _pinned_bytes(source,root)
    family = source['family']
    if family=='cftc':
        with np.load(io.BytesIO(raw),allow_pickle=False) as archive:
            if set(archive.files) != {'position','model_dates','actual_dates'}:
                raise ValueError('SOURCE_SCHEMA')
            position = np.asarray(archive['position'],dtype=np.float64)
            times = np.asarray(archive['model_dates'])
            actual = np.asarray(archive['actual_dates'])
        if times.dtype.kind!='M' or actual.dtype.kind!='M':
            raise ValueError('SOURCE_CHRONOLOGY')
        times = times.astype('datetime64[us]')
        actual = actual.astype('datetime64[D]')
        raw_rows = len(position)
    elif family in ('bill','fx','panel'):
        position,times = _csv_columns(raw,source)
        raw_rows = len(position)
        if family=='panel':
            grid_source = source.get('grid_source')
            if grid_source is None:
                grid_source = next(s for s in source_inventory(root) if s['family']=='bill')
            grid = load_series(grid_source,root)['times']
            values = {int(t):v for t,v in zip(times.astype(np.int64),position)}
            if any(int(t) not in values for t in grid.astype(np.int64)):
                raise ValueError('MISSING_REQUIRED_DATES')
            position = np.asarray([values[int(t)] for t in grid.astype(np.int64)],dtype=float)
            times = np.asarray(grid)
        actual = times.copy() if family=='fx' else times.astype('datetime64[D]')
    else:
        raise ValueError('UNKNOWN_SOURCE_FAMILY')
    if (position.ndim!=1 or not len(position) or times.shape!=position.shape
            or actual.shape!=position.shape or not np.isfinite(position).all()):
        raise ValueError('SOURCE_POSITION')
    if (np.isnat(times).any() or np.isnat(actual).any()
            or np.any(times[1:]<=times[:-1]) or np.any(actual[1:]<=actual[:-1])):
        raise ValueError('SOURCE_CHRONOLOGY')
    if source.get('N',len(position)) != len(position):
        raise ValueError('SOURCE_ALIGNED_ROW_COUNT')
    if family=='cftc':
        days = times.astype('datetime64[D]')
        weekday = (days.astype(np.int64)+3)%7
        actual_weekday = (actual.astype(np.int64)+3)%7
        if (np.any(weekday!=0) or np.any(times!=days.astype('datetime64[us]'))
                or np.any(np.diff(days)!=np.timedelta64(7,'D'))
                or not np.array_equal(actual-actual_weekday.astype('timedelta64[D]'),days)):
            raise ValueError('CFTC_COMPLETE_WEEK_GRID')
    metadata = dict(family=family,key=source['key'],N=len(position),raw_rows=raw_rows,
        first_model_date=str(times[0]),last_model_date=str(times[-1]),
        first_actual_date=str(actual[0]),last_actual_date=str(actual[-1]),
        sha256=source['sha256'],bytes=source['bytes'],unit=source['unit'],
        spliced=False,imputed=False)
    return dict(position=_readonly(position),times=_readonly(times),
                actual_dates=_readonly(actual),metadata=metadata)


def eligibility(source_N, *, horizon=6, windows=(52,260),
                validation_lengths=(52,156), evaluation_n=260, feature_valid_from=26):
    """Whole-contract F2 history gate, applied before any method is attempted."""
    quantities = [source_N,horizon,evaluation_n,feature_valid_from,*windows,*validation_lengths]
    if any(isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) for v in quantities):
        raise ValueError('INTEGER_GEOMETRY_REQUIRED')
    if source_N<1 or horizon<1 or evaluation_n<1 or feature_valid_from<0 or min(windows)<1 or min(validation_lengths)<1:
        raise ValueError('POSITIVE_GEOMETRY_REQUIRED')
    earliest = int(source_N-3*horizon-evaluation_n-max(validation_lengths)-max(windows)+1)
    minimum = int(3*horizon+evaluation_n+max(validation_lengths)+max(windows)-1+feature_valid_from)
    eligible = earliest>=feature_valid_from
    return dict(source_N=int(source_N),eligible=bool(eligible),minimum_N=minimum,
                earliest_training_origin=earliest,feature_valid_from=int(feature_valid_from),
                status='ELIGIBLE' if eligible else 'EXCLUDED_ENTIRE_CONTRACT',
                reason=None if eligible else 'INSUFFICIENT_COMPLETED_FEATURE_HISTORY')


def f2_eligibility_inventory(root=ROOT):
    """Return all planned CFTC exclusions/eligibilities without reading values."""
    design = _protocol('F2',root)
    return [dict(source_key=s['key'],source_index=s['source_index'],source=s,
                 **eligibility(s['N'],horizon=design['H'],windows=design['windows'],
                    validation_lengths=design['validation_lengths'],
                    feature_valid_from=max(24,s['long_scale'],s['short_scale'])))
            for s in source_inventory(root) if s['family']=='cftc']


def _cell(experiment, source, geometry, horizon, window, tau, period='original'):
    va,vb = map(int,geometry['validation'])
    ea,eb = map(int,geometry['evaluation'])
    vn = vb-va+1
    return dict(cell_id=f"{experiment}-{source['family']}-{source['key']}-{period}-H{horizon}-W{window}-V{vn}-tau{tau:.2f}",
        experiment=experiment,family=source['family'],source_key=source['key'],
        source_index=source.get('source_index'),period=period,horizon=int(horizon),window=int(window),
        refit_step=int(geometry['d']),validation_first=va,validation_last=vb,
        evaluation_first=ea,evaluation_last=eb,validation_n=vn,evaluation_n=eb-ea+1,
        short_scale=source['short_scale'],long_scale=source['long_scale'],
        nominal_gap_seconds=source['nominal_gap_seconds'],tau=float(tau),source=source)


def _explicit_tau_geometry(text):
    match = re.fullmatch(r'H(\d+)/W(\d+),validation(\d+)\.\.(\d+)/evaluation(\d+)\.\.(\d+)/d(\d+)',text)
    if match is None:
        raise ValueError('UNSUPPORTED_TAU_GEOMETRY')
    h,w,va,vb,ea,eb,d = map(int,match.groups())
    return h,w,dict(validation=[va,vb],evaluation=[ea,eb],d=d)


def cells_for(experiment: str, root=ROOT):
    """Return the complete protocol grid, including every planned sensitivity."""
    experiment = experiment.upper()
    design = _protocol(experiment,root)
    original = _protocol('F1',root)
    if design['input_provenance'] != original['input_provenance']:
        raise ValueError('EXPERIMENT_INPUT_PROVENANCE_MISMATCH')
    sources = source_inventory(root)
    geometries = {g['family']:g for g in original['geometries']}
    rows = []
    if experiment=='F1':
        for geometry in design['geometries']:
            family = 'fx' if geometry['family']=='fx_original' else geometry['family']
            owned = [s for s in sources if s['family']==family]
            combinations = ((s,h,w) for w in geometry['W'] for s in owned for h in geometry['H']) if family=='panel' else (
                (s,h,w) for s in owned for h in geometry['H'] for w in geometry['W'])
            rows.extend(_cell(experiment,s,geometry,h,w,design['tau']) for s,h,w in combinations)
        if len(rows)!=design['planned_source_cells']:
            raise ValueError('F1_GRID_COUNT_MISMATCH')
    elif experiment=='F2':
        eligible = [r['source'] for r in f2_eligibility_inventory(root) if r['eligible']]
        for w in design['windows']:
            for source in eligible:
                h = design['H']
                ea = source['N']-h-260
                eb = source['N']-h-1
                vb = ea-h-1
                for vn in design['validation_lengths']:
                    geometry = dict(validation=[vb-vn+1,vb],evaluation=[ea,eb],d=geometries['cftc']['d'])
                    rows.append(_cell(experiment,source,geometry,h,w,design['tau']))
    else:
        # The protocol lists tau values ascending but freezes .99 before .90.
        for tau in sorted(design['tau_values'],reverse=True):
            cftc = re.fullmatch(r'(\d+)xW(\d+)/(\d+),H(\d+),unchangedV(\d+)/eval(\d+)/d(\d+)',design['geometries']['cftc'])
            if cftc is None:
                raise ValueError('UNSUPPORTED_TAU_GEOMETRY')
            count,w1,w2,h,vn,en,d = map(int,cftc.groups())
            owned = [s for s in sources if s['family']=='cftc']
            g = geometries['cftc']
            if len(owned)!=count or g['d']!=d or g['validation'][1]-g['validation'][0]+1!=vn or g['evaluation'][1]-g['evaluation'][0]+1!=en:
                raise ValueError('TAU_CFTC_GEOMETRY_MISMATCH')
            for source in owned:
                rows.extend(_cell(experiment,source,g,h,w,tau) for w in (w1,w2))
            fx = next(s for s in sources if s['family']=='fx')
            for period,key in [('original','fx_original'),('early2015','fx_early2015')]:
                h,w,g = _explicit_tau_geometry(design['geometries'][key])
                rows.append(_cell(experiment,fx,g,h,w,tau,period))
            h,w,g = _explicit_tau_geometry(design['geometries']['bill'])
            rows.append(_cell(experiment,next(s for s in sources if s['family']=='bill'),g,h,w,tau))
        if len(rows)!=design['planned_cells_per_tau']*len(design['tau_values']):
            raise ValueError('F3_GRID_COUNT_MISMATCH')
    if len({r['cell_id'] for r in rows})!=len(rows):
        raise ValueError('DUPLICATE_CELL_ID')
    return rows


def ensure_source_snapshot(source: dict, destination, root=ROOT):
    """Caller-invoked post-gate private copy; verify existing bytes, never replace."""
    path = _path(destination,root)
    private = (Path(root)/'.scratch/v12').resolve()
    if not path.resolve().is_relative_to(private):
        raise ValueError('PRIVATE_DESTINATION_REQUIRED')
    if path.resolve()==_path(source['path'],root).resolve():
        raise ValueError('PRIVATE_DESTINATION_MUST_DIFFER_FROM_SOURCE')
    copied = dict(source,path=str(path),original_path=source['path'])
    if path.exists():
        _pinned_bytes(copied,root)
        return copied
    raw = _pinned_bytes(source,root)
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    descriptor = os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'wb') as stream:
        stream.write(raw)
    _pinned_bytes(copied,root)
    return copied
