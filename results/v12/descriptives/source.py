"""Prepare the five-row v12 data table, only after F3's completion receipt.

Import and toy helpers perform no source I/O. The CLI requires --run, verifies
the completed F3 runtime before loading pinned series, and writes a new output
directory exclusively. No model, forecast scoring, acquisition or Git is used.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime,timezone
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import median
import time

import numpy as np


ROOT = Path(__file__).resolve().parent
STAT_KEYS = tuple(f'{quantity}_{statistic}' for quantity in ('abs_N','peak_Y','headroom_Z')
                  for statistic in ('mean','sd','p95'))
ORDER = ('fx_hourly','fx_daily','bill','panel','cftc')
LABELS = {'fx_hourly':'FX, hourly','fx_daily':'FX, daily','bill':'Treasury bills',
          'panel':'NY Fed panel','cftc':'CFTC panel'}
FREQUENCIES = {'fx_hourly':'Hourly records','fx_daily':'Day-end records',
               'bill':'Weekly','panel':'Weekly','cftc':'Weekly'}
DEFINITIONS = dict(horizon=6,first_origin=0,last_origin='N-H-1 inclusive',
    sample='All N-H origins with complete six-record future peak, including the issue anchor.',
    abs_N='B_t=abs(N_t) on the matched origins',
    peak_Y='Y_t=max(abs(N_t),...,abs(N_(t+H))) on the matched origins',
    headroom_Z='Z_t=Y_t-B_t on exactly the same origins',
    mean='Constant-preserving stable_mean; otherwise math.fsum(values)/m',
    sd='Sample standard deviation sqrt(math.fsum((x-mean)^2)/(m-1))',sd_ddof=1,
    p95='Lower empirical/inverted-CDF order statistic at one-based rank ceil(95*m/100); no interpolation',
    quantile_numerator=95,quantile_denominator=100,
    FX_display_divisor=1000000,table_significant_digits=3,
    multi_series='Median of each within-series mean, sample SD and p95; nine separate medians. No pooled exposure or independence inference.')


def describe_series(position, *, horizon=6,display_divisor=1.):
    """Pure matched-sample summaries; accepts constructed arrays in unit tests."""
    from study_core import stable_mean
    x = np.asarray(position,dtype=np.float64)
    if (x.ndim!=1 or not np.isfinite(x).all() or isinstance(horizon,bool)
            or not isinstance(horizon,(int,np.integer)) or horizon<1
            or len(x)-horizon<2 or not math.isfinite(display_divisor) or display_divisor<=0):
        raise ValueError('INVALID_DESCRIPTIVE_SAMPLE')
    magnitude = np.abs(x)/display_divisor
    m = len(x)-horizon
    anchor = magnitude[:m].copy()
    peak = anchor.copy()
    for lag in range(1,horizon+1):
        np.maximum(peak,magnitude[lag:lag+m],out=peak)
    headroom = peak-anchor
    rank = (95*m+99)//100
    statistics = {}
    for name,values in [('abs_N',anchor),('peak_Y',peak),('headroom_Z',headroom)]:
        mean = stable_mean(values)
        sd = math.sqrt(math.fsum((float(value)-mean)**2 for value in values)/(m-1))
        statistics.update({name+'_mean':mean,name+'_sd':sd,
                           name+'_p95':float(np.sort(values)[rank-1])})
    return dict(N=len(x),horizon=int(horizon),origin_count=m,first_origin=0,
                last_origin=m-1,display_divisor=float(display_divisor),statistics=statistics)


def aggregate_statistics(rows):
    """Keep singleton rows and median each statistic within multi-series panels."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['family']].append(row)
    result = []
    for family in ORDER:
        owned = grouped.get(family,[])
        if not owned:
            continue
        units = {r['display_unit'] for r in owned}
        if len(units)!=1:
            raise ValueError('INCONSISTENT_DISPLAY_UNITS')
        values = {key:float(median([r['display_statistics'][key] for r in owned])) for key in STAT_KEYS}
        result.append(dict(family=family,label=LABELS[family],series_count=len(owned),
            source_keys=[r['source_key'] for r in owned],display_unit=next(iter(units)),
            N_per_series=sorted({r['N'] for r in owned}),
            origin_count_per_series=sorted({r['origin_count'] for r in owned}),
            aggregation='median of within-series statistics' if len(owned)>1 else 'within-series statistics',
            statistics=values))
    return result


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _json(path):
    return json.loads(Path(path).read_text())


def _completion_gate(root):
    path = Path(root)/'results/v12/tau/runtime.json'
    try:
        runtime = _json(path)
        start = datetime.fromisoformat(runtime['started_utc'].replace('Z','+00:00'))
        end = datetime.fromisoformat(runtime['completed_utc'].replace('Z','+00:00'))
        valid = (runtime.get('experiment')=='F3' and runtime.get('status','COMPLETE')=='COMPLETE'
                 and start.tzinfo is not None and end.tzinfo is not None and start<=end
                 and end<=datetime.now(timezone.utc))
    except (OSError,ValueError,KeyError,TypeError,AttributeError) as error:
        raise ValueError('F3_COMPLETION_GATE: completed F3 runtime receipt required') from error
    if not valid:
        raise ValueError('F3_COMPLETION_GATE: invalid completion identity or timestamp')
    return dict(path=str(path),sha256=_sha(path),started_utc=runtime['started_utc'],
                completed_utc=runtime['completed_utc'])


def _stamp(value):
    return str(np.datetime_as_string(np.datetime64(value),unit='us'))


def _period(data,cell,period,*,display_clock='actual_dates'):
    model = np.asarray(data['times'])
    actual = np.asarray(data['actual_dates'])
    clock = np.asarray(data[display_clock])
    result = dict(period=period,horizon=6,display_clock=display_clock)
    for segment in ('validation','evaluation'):
        first,last = cell[segment+'_first'],cell[segment+'_last']
        result[segment] = dict(first_index=int(first),last_index=int(last),n=int(last-first+1),
            first=_stamp(clock[first]),last=_stamp(clock[last]),
            model_first=_stamp(model[first]),model_last=_stamp(model[last]),
            actual_first=_stamp(actual[first]),actual_last=_stamp(actual[last]),
            last_H6_label_end=_stamp(clock[last+6]))
    return result


def _date(value):
    return str(value)[:10].replace('.','-')


def _collect(root,gate):
    from v12_inputs import source_inventory,load_series,cells_for
    from v8_daily_fx import resample_closed_days
    sources = source_inventory(root)
    original = cells_for('F1',root)
    tau = cells_for('F3',root)
    archive_paths = ['protocol/v12/loss-decomposition-design.md','protocol/v12/tau-design.md',
        'protocol/revision-v8/wp4-daily-fx-design.json',
        'results/revision-v8/wp4/readout-bindings.json',
        'results/revision-v8/wp4/cells/W260_H6/cell-geometry.json',
        'results/revision-v8/wp4/cells/W260_H6/worker-source.json',
        'results/v10/cftc/splits.json']
    old_daily = _json(root/'results/revision-v8/wp4/readout-bindings.json')
    daily_geometry = _json(root/'results/revision-v8/wp4/cells/W260_H6/cell-geometry.json')
    daily_design = _json(root/'protocol/revision-v8/wp4-daily-fx-design.json')
    daily_source = _json(root/'results/revision-v8/wp4/cells/W260_H6/worker-source.json')
    cftc_splits = _json(root/'results/v10/cftc/splits.json')
    rows,metadata = [],[]

    def append(source,data,family,periods,*,daily=False):
        divisor = 1000000. if family.startswith('fx_') else 1.
        native = describe_series(data['position'])
        shown = describe_series(data['position'],display_divisor=divisor) if divisor!=1 else native
        display_unit = 'USD millions' if family!='cftc' else 'contracts'
        row = dict(family=family,source_key='fx_daily' if daily else source['key'],
            N=native['N'],horizon=6,origin_count=native['origin_count'],
            first_origin=0,last_origin=native['last_origin'],native_unit=source['unit'],
            display_unit=display_unit,display_divisor=divisor,
            native_statistics=native['statistics'],display_statistics=shown['statistics'])
        rows.append(row)
        actual = data['actual_dates'];times=data['times']
        metadata.append(dict(family=family,source_key=row['source_key'],
            frequency=FREQUENCIES[family],N=row['N'],raw_N=source.get('raw_rows',source['N']),
            matched_origin_count=row['origin_count'],
            raw_first=source.get('first_date',str(actual[0])),
            raw_last=source.get('last_date',str(actual[-1])),
            aligned_actual_first=_stamp(actual[0]),aligned_actual_last=_stamp(actual[-1]),
            aligned_model_first=_stamp(times[0]),aligned_model_last=_stamp(times[-1]),
            matched_first=_stamp(times[0]),matched_last=_stamp(times[row['last_origin']]),
            source_sha256=source['sha256'],source_bytes=source['bytes'],source_path=source['path'],
            native_unit=row['native_unit'],display_unit=display_unit,display_divisor=divisor,
            periods=periods,scope='Same-dealer deterministic calendar aggregation' if daily else data['metadata'].get('key',source['key'])))

    for source in sources:
        data = load_series(source,root)
        family = 'fx_hourly' if source['family']=='fx' else source['family']
        if family=='fx_hourly':
            owned = [c for c in tau if c['family']=='fx' and c['tau']==.99]
            periods = [_period(data,c,c['period'],display_clock='times') for c in owned]
            append(source,data,family,periods)
            daily = resample_closed_days(data['position'],data['times'])
            if (daily.metadata!=old_daily['daily_metadata']
                    or daily.metadata!=daily_source['daily_metadata']
                    or source['sha256']!=daily_source['source_identity']['accepted_csv_sha256']):
                raise ValueError('DAILY_ARCHIVE_FINGERPRINT_MISMATCH')
            if (daily_geometry['validation_first']!=daily_design['sample']['validation_first']
                    or daily_geometry['validation_last']!=daily_design['sample']['validation_last']
                    or daily_geometry['evaluation_first']!=daily_design['sample']['evaluation_first']
                    or daily_geometry['evaluation_last']!=len(daily.position)-1-max(daily_design['clock_and_target']['horizons'])):
                raise ValueError('DAILY_ARCHIVE_GEOMETRY_MISMATCH')
            daily_data = dict(position=daily.position,times=daily.times,
                              actual_dates=daily.selected_raw_times,metadata={})
            p = _period(daily_data,daily_geometry,'original',display_clock='times')
            for segment in ('validation','evaluation'):
                for edge in ('first','last'):
                    if p[segment][edge]!=old_daily['periods'][segment+'_'+edge]:
                        raise ValueError('DAILY_ARCHIVE_DATE_MISMATCH')
            append(source,daily_data,'fx_daily',[p],daily=True)
            metadata[-1]['resampling_metadata']=daily.metadata
        else:
            cell = next(c for c in original if c['family']==source['family']
                        and c['source_key']==source['key'] and c['horizon']==6)
            p = _period(data,cell,'original')
            if family=='cftc':
                saved = cftc_splits['per_contract'][source['key']]
                for segment in ('validation','evaluation'):
                    for edge in ('first','last'):
                        if (np.datetime64(p[segment][edge])!=np.datetime64(saved['actual_dates'][segment][edge])
                                or np.datetime64(p[segment]['model_'+edge])!=np.datetime64(saved['model_clock'][segment][edge])):
                            raise ValueError('CFTC_ARCHIVE_DATE_MISMATCH')
            append(source,data,family,[p])
    expected = {'fx_hourly':1,'fx_daily':1,'bill':1,'panel':12,'cftc':17}
    if any(sum(r['family']==f for r in rows)!=n for f,n in expected.items()):
        raise ValueError('DESCRIPTIVE_SOURCE_COUNT_MISMATCH')
    summaries = aggregate_statistics(rows)
    grouped_metadata = []
    for summary in summaries:
        owned = [m for m in metadata if m['family']==summary['family']]
        periods = owned[0]['periods']
        if any(m['periods']!=periods for m in owned[1:]):
            raise ValueError('GROUP_SPLIT_DATE_MISMATCH')
        grouped_metadata.append(dict(family=summary['family'],label=summary['label'],
            frequency=FREQUENCIES[summary['family']],series_count=len(owned),
            N_per_series=summary['N_per_series'],matched_origin_count_per_series=summary['origin_count_per_series'],
            raw_N_per_series=sorted({m['raw_N'] for m in owned}),display_unit=summary['display_unit'],
            raw_first=min(_date(m['raw_first']) for m in owned),raw_last=max(_date(m['raw_last']) for m in owned),
            aligned_first=min(_date(m['aligned_actual_first' if summary['family']=='cftc' else 'aligned_model_first']) for m in owned),
            aligned_last=max(_date(m['aligned_actual_last' if summary['family']=='cftc' else 'aligned_model_last']) for m in owned),
            display_sample_clock='actual economic dates' if summary['family']=='cftc' else 'model issue times',periods=periods))
    report_metadata = dict(created_utc=datetime.now(timezone.utc).isoformat(),F3_gate=gate,
        definitions=DEFINITIONS,series=metadata,groups=grouped_metadata,
        input_files=[dict(path=relative,sha256=_sha(root/relative)) for relative in archive_paths],
        code_files=[dict(path=relative,sha256=_sha(root/relative)) for relative in
                    ('report_v12_descriptives.py','v12_inputs.py','v8_daily_fx.py','study_core.py')],
        caveats=['Both hourly FX periods were already inspected; the daily series is the same dealer.',
            'Descriptions use the full complete-H6 source sample, not only validation or evaluation.',
            'Panel medians summarize related series and do not pool dollar exposure or independent observations.',
            'CFTC retains heterogeneous native contract counts; there is no common dollar interpretation.',
            'Economic-date downloaded-vintage replays do not establish historical public availability.'])
    # Re-read bytes, independently of parsed arrays and stored pin values, after
    # calculation. This verifies source identity without constructing new labels.
    input_proofs = []
    for path in sorted({m['source_path'] for m in metadata}):
        owned = [m for m in metadata if m['source_path']==path]
        raw = Path(path).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if any(digest!=m['source_sha256'] or len(raw)!=m['source_bytes'] for m in owned):
            raise ValueError('SOURCE_BYTES_CHANGED_AFTER_DESCRIPTION')
        input_proofs.append(dict(path=path,bytes=len(raw),sha256=digest,
            verification='Independent byte read after descriptive calculation; agrees with pre-parse pinned snapshot verification.'))
    report_metadata['verified_input_bytes']=input_proofs
    return rows,summaries,report_metadata


def _write_json(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')


def _write_csv(path,rows):
    with Path(path).open('x',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def _tex(value):
    return str(value).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')


def _number(value):
    text = format(float(value),'.3g')
    if 'e' in text:
        mantissa,exponent = text.split('e')
        return '$'+mantissa+r'\!\times\!10^{'+str(int(exponent))+'}$'
    return text


def _table(summaries,metadata):
    lines = [r'\begin{table}[!htbp]',r'\centering',
        r'\caption{Data and matched six-record peak summaries.}\label{tab:v12-data}',
        r'\begingroup\scriptsize\setlength{\tabcolsep}{2.5pt}',
        r'\textit{Panel A. Sources, aligned samples and existing split dates}\\[3pt]',
        r'\begin{tabular}{@{}p{.13\linewidth}p{.08\linewidth}p{.11\linewidth}p{.08\linewidth}p{.15\linewidth}p{.16\linewidth}p{.16\linewidth}@{}}',
        r'\toprule',r'Data & Frequency & Series / rows & Unit & Sample dates & Validation & Evaluation \\',r'\midrule']
    bindings = []
    for i,g in enumerate(metadata['groups']):
        n = ','.join(f'{v:,}' for v in g['N_per_series'])
        m = ','.join(f'{v:,}' for v in g['matched_origin_count_per_series'])
        count = r'\shortstack[l]{'+str(g['series_count'])+' series'+r'\\'+n+' rows'+r'\\'+m+' peaks}'
        span = r'\shortstack[l]{'+g['aligned_first']+r'\\--'+g['aligned_last']+'}'
        date_cells = []
        for segment in ('validation','evaluation'):
            values = []
            for j,p in enumerate(g['periods']):
                if j:values.append(r'[2pt]')
                values.extend([_date(p[segment]['first']),r'--'+_date(p[segment]['last'])])
                for edge in ('first','last'):
                    bindings.append(dict(table_panel='A',row=i,field=segment+'_'+p['period']+'_'+edge,
                        source_file='metadata.json',pointer=f'/groups/{i}/periods/{j}/{segment}/{edge}',
                        display_text=_date(p[segment][edge]),definition='First ten ISO date characters of the preserved displayed issue/economic clock.'))
            # Four stacked lines for two periods; no ambiguous range abbreviations.
            date_cells.append(r'\shortstack[l]{'+r'\\'.join(v for v in values if v!=r'[2pt]')+'}')
        unit = 'USD mn' if g['display_unit']=='USD millions' else 'Contracts'
        frequency = {'fx_hourly':'Hourly','fx_daily':'Day end'}.get(g['family'],'Weekly')
        lines.append(' & '.join([_tex(g['label']),frequency,count,unit,span,*date_cells])+r' \\')
        for field in ('series_count','N_per_series','matched_origin_count_per_series','aligned_first','aligned_last'):
            value = g[field]
            for k,item in enumerate(value if isinstance(value,list) else [value]):
                pointer=f'/groups/{i}/{field}'+(f'/{k}' if isinstance(value,list) else '')
                shown = f'{item:,}' if isinstance(item,int) else str(item)
                bindings.append(dict(table_panel='A',row=i,field=field,source_file='metadata.json',pointer=pointer,
                    display_text=shown,definition='Aligned per-series count or source-clock date; peaks count N-H.'))
    lines.extend([r'\bottomrule',r'\end{tabular}',r'\par\vspace{7pt}',
        r'\textit{Panel B. Within-series mean, sample SD and empirical 95th percentile}\\[3pt]',
        r'\begin{tabular}{@{}l*{9}{r}@{}}',r'\toprule',
        r' & \multicolumn{3}{c}{$|N|$} & \multicolumn{3}{c}{Peak $Y$} & \multicolumn{3}{c}{Headroom $Z$} \\',
        r'\cmidrule(lr){2-4}\cmidrule(lr){5-7}\cmidrule(lr){8-10}',
        r'Data & Mean & SD & 95th & Mean & SD & 95th & Mean & SD & 95th \\',r'\midrule'])
    for i,row in enumerate(summaries):
        values = [_number(row['statistics'][key]) for key in STAT_KEYS]
        lines.append(' & '.join([_tex(row['label']),*values])+r' \\')
        for key,shown in zip(STAT_KEYS,values):
            bindings.append(dict(table_panel='B',row=i,field=key,source_file='summary.json',
                pointer=f'/{i}/statistics/{key}',display_text=shown,
                definition='Three significant digits of the saved statistic; multi-series rows are medians of within-series statistics.'))
    lines.extend([r'\bottomrule',r'\end{tabular}',r'\endgroup',
        r'\begin{minipage}{.98\linewidth}\footnotesize\emph{Notes.} All summaries use complete $H=6$ origins and include the issue anchor; SD uses $m-1$, and the empirical 95th percentile has rank $\lceil95m/100\rceil$. Daily FX uses the last record of each nonempty source-naive calendar day at day end; the reported FX comparison periods were already inspected. Dollar values are in millions; panel entries are nine separate medians of within-series summaries, without exposure pooling or independence inference, and CFTC retains heterogeneous native contract counts.\end{minipage}',
        r'\end{table}'])
    for field in ('horizon','sd_ddof','quantile_numerator','quantile_denominator','FX_display_divisor','table_significant_digits'):
        bindings.append(dict(table_panel='definition',field=field,source_file='metadata.json',
            pointer='/definitions/'+field,display_text=str(metadata['definitions'][field]),definition='Declared display/statistical convention; see metadata definitions.'))
    return '\n'.join(lines)+'\n',bindings


def _numeric_leaves(value,pointer=''):
    if isinstance(value,dict):
        for key,item in value.items():
            escaped=str(key).replace('~','~0').replace('/','~1')
            yield from _numeric_leaves(item,pointer+'/'+escaped)
    elif isinstance(value,list):
        for i,item in enumerate(value):
            yield from _numeric_leaves(item,pointer+'/'+str(i))
    elif isinstance(value,(int,float)) and not isinstance(value,bool):
        yield pointer,value


def run(*,root=ROOT,output=None):
    """Explicit real-data entry; the F3 gate precedes all source access/writes."""
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    root = Path(root).resolve()
    gate = _completion_gate(root)
    output = Path(output) if output is not None else root/'results/v12/descriptives'
    if output.exists():
        raise ValueError('DESCRIPTIVE_OUTPUT_ALREADY_EXISTS')
    rows,summaries,metadata = _collect(root,gate)
    table,table_bindings = _table(summaries,metadata)
    output.mkdir(parents=True,exist_ok=False)
    _write_json(output/'rawstats.json',rows)
    _write_json(output/'summary.json',summaries)
    _write_json(output/'metadata.json',metadata)
    raw_csv = [{**{k:r[k] for k in ('family','source_key','N','horizon','origin_count','first_origin','last_origin','native_unit','display_unit','display_divisor')},
                **{'native_'+k:r['native_statistics'][k] for k in STAT_KEYS},
                **{'display_'+k:r['display_statistics'][k] for k in STAT_KEYS}} for r in rows]
    summary_csv = [{**{k:r[k] for k in ('family','label','series_count','display_unit','aggregation')},
                    'N_per_series':','.join(map(str,r['N_per_series'])),
                    'origin_count_per_series':','.join(map(str,r['origin_count_per_series'])),
                    **r['statistics']} for r in summaries]
    _write_csv(output/'rawstats.csv',raw_csv)
    _write_csv(output/'summary.csv',summary_csv)
    with (output/'data-table.tex').open('x') as stream:stream.write(table)
    with (output/'source.py').open('xb') as stream:stream.write(Path(__file__).read_bytes())
    if _sha(output/'source.py')!=_sha(Path(__file__)):
        raise ValueError('DESCRIPTIVE_SOURCE_COPY_MISMATCH')
    numeric = []
    for filename,value in [('rawstats.json',rows),('summary.json',summaries),('metadata.json',metadata)]:
        digest = _sha(output/filename)
        numeric.extend(dict(source_file=filename,sha256=digest,pointer=pointer,value=number,
            definition='See metadata.json /definitions and the indicated source/summary row; source counts/dates are descriptive provenance.')
            for pointer,number in _numeric_leaves(value))
    for binding in table_bindings:
        binding['sha256']=_sha(output/binding['source_file'])
    files = [dict(path=p.name,bytes=p.stat().st_size,sha256=_sha(p)) for p in sorted(output.iterdir()) if p.is_file()]
    _write_json(output/'number-bindings.json',dict(schema='v12-data-table-bindings-v1',
        generated_utc=datetime.now(timezone.utc).isoformat(),files=files,
        numeric_bindings=numeric,table_bindings=table_bindings,
        metadata_sha256=_sha(output/'metadata.json')))
    runtime = dict(status='COMPLETE',started_utc=started_utc,
        completed_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-started,
        operation='Descriptive statistics and data table only; no model fit, forecast score or acquisition.',
        F3_gate=gate,source_stat_rows=len(rows),displayed_family_rows=len(summaries),
        independently_verified_source_files=len(metadata['verified_input_bytes']),
        exact_source_copy_sha256=_sha(output/'source.py'),
        number_bindings_sha256=_sha(output/'number-bindings.json'))
    _write_json(output/'runtime.json',runtime)
    _write_json(output/'manifest.json',dict(schema='v12-descriptives-output-manifest-v1',
        created_utc=datetime.now(timezone.utc).isoformat(),
        files=[dict(path=p.name,bytes=p.stat().st_size,sha256=_sha(p))
               for p in sorted(output.iterdir()) if p.is_file()],
        exact_source_copy=dict(path='source.py',root_source=str(Path(__file__).resolve()),
                               sha256=_sha(output/'source.py')),
        input_byte_proofs=metadata['verified_input_bytes']))
    return dict(output=str(output),source_stat_rows=len(rows),table_rows=len(summaries),
                table=str(output/'data-table.tex'),bindings=str(output/'number-bindings.json'),
                runtime=str(output/'runtime.json'),manifest=str(output/'manifest.json'),
                source_copy=str(output/'source.py'),elapsed_seconds=runtime['elapsed_seconds'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='Generate the table only after completed F3.')
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    if not args.run:
        parser.error('--run is required; no financial computation was performed')
    print(json.dumps(run(root=args.root,output=args.output),indent=2))


if __name__=='__main__':
    main()
