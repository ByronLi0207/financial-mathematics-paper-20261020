"""Count stored-clock label durations without reading forecast outcomes.

Post-result source-timing audit only; no numeric position parsing, fitting,
selection, resampling, file replacement, network access or third-party download.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import resource
import subprocess
import time

import reproduce_conditional as rep
import run_study as resource_helpers

ROOT=Path(__file__).resolve().parent


def require(ok,code):
    if not ok:raise ValueError(code)


def integer_seconds(delta):
    require(delta.microseconds==0,'SUBSECOND_CLOCK')
    return delta.days*86400+delta.seconds


def thread_count():
    try:
        probe=subprocess.run(['/bin/ps','-M','-p',str(os.getpid()),'-o','pid='],
            capture_output=True,text=True,check=True,timeout=5)
        return resource_helpers.parse_thread_snapshot(probe.stdout,os.getpid())
    except (OSError,subprocess.SubprocessError,ValueError):
        raise ValueError('THREAD_PROBE_FAILED') from None


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args(argv)
    target=ROOT/args.output
    require(not any(x.is_symlink() for x in (target,*target.parents)),'OUTPUT_SYMLINK')
    require(target.resolve().is_relative_to(ROOT/'state/revision-20261022') and target.parent.is_dir()
        and not target.exists(),'OUTPUT_PATH')
    started=time.monotonic();began=datetime.now(timezone.utc).isoformat();threads=[thread_count()]
    spec_raw=rep.read_bytes(ROOT,Path('protocol/revision-20261022/study-spec.json'))
    freeze=json.loads(rep.read_bytes(ROOT,Path('protocol/revision-20261022/executable-freeze.json')))
    spec_hash=hashlib.sha256(spec_raw).hexdigest()
    require(spec_hash==freeze['files']['protocol/revision-20261022/study-spec.json'],'SPEC_IDENTITY')
    spec=json.loads(spec_raw);rows=[];inputs={};windows_checked=0
    for source,cfg in spec['sources'].items():
        raw=rep.read_bytes(ROOT,Path(cfg['input_relative_path']),cap=25*1024*1024)
        require(len(raw)==cfg['bytes'] and hashlib.sha256(raw).hexdigest()==cfg['sha256'],'SOURCE_IDENTITY')
        reader=csv.reader(io.StringIO(raw.decode('utf-8'),newline=''),strict=True)
        header=next(reader);fmt='%Y.%m.%dT%H:%M:%S.%f' if source=='fx_hourly' else '%Y-%m-%d'
        require(header==(['datetime','NetPosUsd','NetUsdPnL','AbsVolume','Mid'] if source=='fx_hourly'
                         else ['As Of Date','Time Series','Value (millions)']),'SOURCE_HEADER')
        stamps=[]
        for row in reader:
            require(len(row)==len(header),'SOURCE_ROW')
            if source=='nyfed_weekly':require(row[1]=='PDPOSGS-B','SOURCE_SERIES')
            t=datetime.strptime(row[0],fmt)
            require(not stamps or t>stamps[-1],'SOURCE_CHRONOLOGY');stamps.append(t)
        require(len(stamps)==cfg['record_count'],'SOURCE_LENGTH')
        gaps=[integer_seconds(stamps[i+1]-stamps[i]) for i in range(len(stamps)-1)]
        unit,divisor=('stored_naive_clock_hours',3600) if source=='fx_hourly' else ('as_of_calendar_days',86400)
        for segment in ('validation','evaluation'):
            first,last=(cfg[segment+'_origin_'+s] for s in ('first','last'))
            for h in (6,24):
                require(0<=first<=last and last+h<len(stamps),'SEGMENT_BOUNDS')
                counts=Counter()
                for i in range(first,last+1):
                    direct=integer_seconds(stamps[i+h]-stamps[i])
                    adjacent=sum(gaps[j] for j in range(i,i+h))
                    require(direct==adjacent and direct%divisor==0,'CLOCK_ENDPOINT_MISMATCH')
                    counts[direct//divisor]+=1;windows_checked+=1
                require(sum(counts.values())==last-first+1,'SEGMENT_COUNT')
                for duration,count in sorted(counts.items()):
                    rows.append(dict(source=source,segment=segment,horizon_records=h,duration=duration,
                        duration_unit=unit,origin_count=count,segment_origin_count=last-first+1))
        require(rep.read_bytes(ROOT,Path(cfg['input_relative_path']),cap=25*1024*1024)==raw,'SOURCE_CHANGED')
        inputs[source]=dict(bytes=len(raw),sha256=cfg['sha256'],record_count=len(stamps),
            first_record=stamps[0].isoformat(),last_record=stamps[-1].isoformat())
    threads.append(thread_count());rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if os.uname().sysname!='Darwin':rss*=1024
    result=dict(version=1,status='RECORD_CLOCK_DURATION_VERIFIED',verified_utc=datetime.now(timezone.utc).isoformat(),
        plan='notes/revision-20261022/record-clock-duration-check-plan.md',
        spec_sha256=spec_hash,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs=inputs,rows=rows,all_direct_windows_equal_adjacent_sums=True,windows_checked=windows_checked,
        financial_values_used=False,forecast_results_read=False,models_fitted=False,origins_removed=False,
        resources=dict(started_utc=began,elapsed_seconds=time.monotonic()-started,peak_rss_bytes=rss,
            os_thread_snapshots=threads,maximum_observed_os_threads=max(threads),
            thread_scope='before and after only; not a continuous bound'),
        interpretation='FX units are naive stored-clock differences, not verified UTC elapsed time; Treasury units are economic as-of calendar dates. No cross-source pooling, forecast selection or operational inference.')
    rep.write_json(target,result,exclusive=True)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
