"""Bounded v12 studies: committed protocols, single attempts, saved scalar reports."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
DESIGNS = {
    'F1': ('loss-decomposition-design.md', '9679e15824bf24bbcf06b645688ee5c030793c30', '4c5abeba018b22c39dbff57d16200934af6f6c39'),
    'F2': ('validation-length-design.md', 'f8628dbf83ebeebf5fcd4e494985c11603f11eb5', '12e86a23f0be1ad55d6ab980473972442cd006f0'),
    'F3': ('tau-design.md', '185e1ae9a63046b56181a77bb031c6a7a24a0138', '9fa50a76e9b93fa26cb0931e9bde38a4fac27485'),
}
OUT_NAMES = {'F1': 'decomposition', 'F2': 'validation-length', 'F3': 'tau'}
CODE = ('run_v12_studies.py', 'v12_runner.py', 'v12_inputs.py', 'v12_forecast.py',
        'v12_decomposition.py', 'v12_summaries.py')
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMBA_NUM_THREADS')


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')


def append(path, value):
    with Path(path).open('a') as f:
        f.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n')


def read_design(experiment):
    name, original_commit, public_commit = DESIGNS[experiment]
    path = 'protocol/v12/' + name
    raw = (ROOT/path).read_bytes()
    commit = None
    for candidate in (original_commit, public_commit):
        ancestry = subprocess.run(['git','merge-base','--is-ancestor',candidate,'HEAD'],
                                  cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if ancestry.returncode == 0:
            if git('show', candidate+':'+path) != raw:
                raise ValueError('PROTOCOL_BYTES_CHANGED')
            commit = candidate
            break
    if commit is None:
        raise ValueError('NO_VERIFIED_DESIGN_ANCESTOR')
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
    if changed != [path]:
        raise ValueError('DESIGN_NOT_STANDALONE_COMMIT')
    d = json.loads(re.search(r'```json\n(.*?)\n```', raw.decode(), re.S).group(1))
    for filename, digest in d['inherited_code_sha256'].items():
        if sha(ROOT/filename) != digest:
            raise ValueError('FROZEN_MODEL_CHANGED:'+filename)
    return d, dict(path=path, local_design_commit=original_commit, accepted_design_commit=commit,
                   public_design_commit=public_commit, sha256=sha(ROOT/path),
                   accepted_commit_time=git('show', '-s', '--format=%cI', commit).decode().strip(),
                   working_bytes_equal_design_commit=True)


def wall_cap(design):
    r = design['runtime']
    return r.get('total_cap_seconds', r.get('total_cap_seconds_including_pilot'))


def work_units(cell, experiment):
    """A conservative scheduling proxy; it contains no observed financial result."""
    d = cell['refit_step']
    vn = cell['validation_last']-cell['validation_first']+1
    en = cell['evaluation_last']-cell['evaluation_first']+1
    v, e = math.ceil(vn/d), math.ceil(en/d)
    models = cell.get('methods', ['QR33'] if experiment == 'F3' else ['QR33', 'QR4'])
    width = sum(34 if m == 'QR33' else 5 for m in models)
    count = 5*(v+e) if experiment == 'F1' else 5*v+e
    return float(cell['window']*width*count)


def predeclared_scope(experiment, cells, *, seconds_per_work, remaining_seconds):
    retained = [dict(c) for c in cells]
    omitted, steps = [], []
    estimate = lambda: seconds_per_work*sum(work_units(c, experiment) for c in retained)/4
    def drop(predicate, label):
        nonlocal retained
        gone = [c for c in retained if predicate(c)]
        retained = [c for c in retained if not predicate(c)]
        if gone:
            omitted.extend(gone)
            steps.append(label)
    if estimate() > remaining_seconds:
        if experiment == 'F1':
            drop(lambda c: c['family'] == 'fx', 'omit_FX')
            if estimate() > remaining_seconds:
                drop(lambda c: c['family'] == 'panel' and c['window'] == 260, 'omit_panel_W260')
        elif experiment == 'F2':
            for c in retained:
                c['methods'] = ['QR33']
            steps.append('omit_QR4')
            if estimate() > remaining_seconds:
                drop(lambda c: c['window'] == 260, 'omit_W260')
        else:
            drop(lambda c: c['tau'] == .90, 'omit_tau90')
            if estimate() > remaining_seconds:
                drop(lambda c: c['family'] == 'bill', 'omit_bill_secondary')
            if estimate() > remaining_seconds:
                drop(lambda c: c['family'] == 'fx', 'omit_FX_secondary')
    return dict(cells=retained, omitted=omitted, trim_steps=steps,
                projected_remaining_seconds=estimate(), seconds_per_work=seconds_per_work)


def priority(c, experiment):
    if experiment == 'F1':
        group = (0 if c['family'] == 'cftc' else 1 if c['family'] == 'panel' and c['window'] == 52
                 else 2 if c['family'] == 'bill' else 3 if c['family'] == 'panel' else 4)
    elif experiment == 'F2':
        group = 0 if c['window'] == 52 else 1
    else:
        group = (0 if c['tau'] == .99 else 10)+(0 if c['family'] == 'cftc' else 1 if c['family'] == 'fx' else 2)
    return (group, c['source'].get('source_index', 0), c['source_key'], c['horizon'], c['window'],
            0 if c['period'] == 'original' else 1, c['validation_first'])


def group_jobs(cells, experiment):
    ordered = sorted(cells, key=lambda c: priority(c, experiment))
    if experiment != 'F2':
        return [[c] for c in ordered]
    groups = {}
    for method in ('QR33','QR4'):
        for c in ordered:
            if method not in c.get('methods',['QR33','QR4']):
                continue
            groups.setdefault((method,c['source_key'], c['window']), []).append(dict(c,methods=[method]))
    return [sorted(v, key=lambda c: c['validation_n']) for v in groups.values()]


def merge_cell_results(results):
    merged = {}
    for result in results:
        key = result['cell']['cell_id']
        item = merged.setdefault(key, dict(cell=result['cell'], rows=[], candidates=[], references={}))
        old = {row['method'] for row in item['rows']}
        if old.intersection(row['method'] for row in result.get('rows', [])):
            raise ValueError('DUPLICATE_METHOD_RESULT')
        item['rows'].extend(result.get('rows', []))
        item['candidates'].extend(result.get('candidates', []))
        item['references'].update(result.get('references', {}))
    return merged


def preflight_cells(cells, source_status, eligibility=None):
    excluded_keys = {key for key,value in source_status.items() if value['status']!='VERIFIED'}
    for item in eligibility or []:
        key = ('cftc',item['source_key'])
        if key in excluded_keys:
            item.update(eligible=False,status='EXCLUDED_ENTIRE_CONTRACT',reason='SOURCE_PRECHECK_FAILED')
        if not item['eligible']:
            excluded_keys.add(key)
    return ([c for c in cells if (c['family'],c['source_key'])not in excluded_keys],
            [c for c in cells if (c['family'],c['source_key'])in excluded_keys])


def salvage_job(folder, cells):
    """Read immutable completed scalar receipts after a hard stop; never refit."""
    results = []
    def receipt(path):
        try:
            return json.loads(path.read_text())
        except (OSError, ValueError):
            return None
    for cell in cells:
        path = folder/'outputs'/cell['cell_id']
        final = path/'cell-result.json'
        complete = receipt(final)
        if isinstance(complete,dict) and isinstance(complete.get('rows'),list):
            results.append(complete)
            continue
        rows = [r for p in sorted(path.glob('*.result.json'))if isinstance(r:=receipt(p),dict)]
        if not rows:
            continue
        candidates = []
        for p in sorted(path.glob('*.selection.json')):
            value=receipt(p)
            if isinstance(value,dict): candidates.extend(value.get('validation_candidates', []))
        for p in sorted(path.glob('*.evaluation-candidates.json')):
            value=receipt(p)
            if isinstance(value,list): candidates.extend(value)
        results.append(dict(cell=cell,rows=rows,candidates=candidates,references={},
                            status='SALVAGED_TERMINAL_METHODS',read_only_salvage=True))
    return results


def method_slots(cells, experiment):
    return [(c['cell_id'],m)for c in cells for m in c.get('methods',
            ['QR33']if experiment=='F3'else['QR33','QR4'])]


def missing_row_status(slot, launched, omitted):
    if slot in launched:
        return 'FAILED_RESOURCE'if launched[slot]=='FAILED_RESOURCE'else'FAILED_TECHNICAL'
    return 'NOT_RUN_RESOURCE_LIMIT'if slot in omitted else'FAILED_SOURCE'


def start_jobs(groups, experiment, private, code_hashes, deadline, *, workers=4, offset=0):
    """Each declared job is launched once. The parent never resubmits a failure."""
    queue, active, records, results = list(enumerate(groups, offset)), {}, [], []
    cell_cap = 600 if experiment == 'F1' else 300
    env = dict(os.environ, **{n: '1' for n in THREADS}, PYTHONDONTWRITEBYTECODE='1')
    while queue or active:
        remaining = deadline-time.monotonic()
        while queue and len(active) < workers and remaining > 0:
            idx, cells = queue.pop(0)
            folder = private/f'job-{idx:03d}'
            folder.mkdir()
            spec = dict(experiment=experiment, cells=cells, cache_root=str(ROOT/'.scratch/v12/cache'),
                        output_root=str(folder/'outputs'), cell_cap_seconds=cell_cap,
                        cap_seconds=min(cell_cap*len(cells), remaining), expected_code_sha256=code_hashes)
            write(folder/'job.json', spec)
            stdout = (folder/'stdout.txt').open('x')
            stderr = (folder/'stderr.txt').open('x')
            p = subprocess.Popen([sys.executable, '-B', str(ROOT/'v12_runner.py'), '--job', str(folder/'job.json')],
                                 cwd=ROOT, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            active[idx] = dict(process=p, cells=cells, folder=folder, started=utc(),
                               monotonic=time.monotonic(), cap=spec['cap_seconds'], stdout=stdout, stderr=stderr)
            append(private/'progress.jsonl', dict(event='job_start', job=idx, utc=utc(), cell_ids=[c['cell_id']for c in cells]))
            remaining = deadline-time.monotonic()
        for idx, item in list(active.items()):
            p = item['process']
            timeout = time.monotonic() >= deadline or time.monotonic()-item['monotonic'] > item['cap']+2
            if p.poll() is None and timeout:
                os.killpg(p.pid, signal.SIGTERM)
                try:
                    p.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    os.killpg(p.pid, signal.SIGKILL)
                    p.wait()
            if p.poll() is not None:
                item['stdout'].close(); item['stderr'].close()
                record = dict(job=idx, started_utc=item['started'], ended_utc=utc(),
                              elapsed_seconds=time.monotonic()-item['monotonic'], exit_code=p.returncode,
                              timed_out=timeout, cell_ids=[c['cell_id']for c in item['cells']],
                              method_slots=method_slots(item['cells'],experiment))
                try:
                    data = json.loads((item['folder']/'stdout.txt').read_text())
                    if not isinstance(data.get('rows'), list):
                        raise ValueError('MISSING_ROWS')
                    results.extend(data.get('cells', []))
                    record['result_status'] = data.get('status')
                except (ValueError, KeyError, OSError) as exc:
                    record.update(result_status='FAILED_RESOURCE' if timeout else 'FAILED_TECHNICAL',
                                  reason=type(exc).__name__)
                    saved = salvage_job(item['folder'],item['cells'])
                    results.extend(saved)
                    record['salvaged_method_rows'] = sum(len(x['rows'])for x in saved)
                records.append(record)
                append(private/'progress.jsonl', dict(event='job_end', **record))
                del active[idx]
        if time.monotonic() >= deadline:
            break
        if active:
            time.sleep(.05)
    # Children still alive at the common deadline are terminal, not queued for retry.
    for idx, item in active.items():
        p = item['process']
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL); p.wait()
        item['stdout'].close(); item['stderr'].close()
        results.extend(salvage_job(item['folder'],item['cells']))
        records.append(dict(job=idx, started_utc=item['started'], ended_utc=utc(),
                            elapsed_seconds=time.monotonic()-item['monotonic'], exit_code=p.returncode,
                            timed_out=True, result_status='FAILED_RESOURCE', cell_ids=[c['cell_id']for c in item['cells']],
                            method_slots=method_slots(item['cells'],experiment)))
    return results, records, [c for _, cells in queue for c in cells]


def start_ordered_jobs(cells, experiment, private, code_hashes, deadline, *, offset=0):
    """Complete primary method/family waves before starting a secondary wave."""
    groups = group_jobs(cells,experiment)
    batches = {}
    for group in groups:
        c = group[0]
        key = ((c['methods'][0],c['window'])if experiment=='F2' else priority(c,experiment)[0])
        batches.setdefault(key,[]).append(group)
    results,records,unstarted = [],[],[]
    for batch in batches.values():
        r,log,missing = start_jobs(batch,experiment,private,code_hashes,deadline,offset=offset)
        results.extend(r);records.extend(log);unstarted.extend(missing);offset += len(batch)
    return results,records,unstarted


def csv_write(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open('x', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})


def run(experiment):
    design, provenance = read_design(experiment)
    public = ROOT/'results/v12'/OUT_NAMES[experiment]
    private = ROOT/'.scratch/v12'/OUT_NAMES[experiment]
    public.mkdir(); private.mkdir()
    publication = [json.loads(line)for line in (ROOT/'notes/v12/design-publication.jsonl').read_text().splitlines()]
    published = next(x for x in publication if x['experiment'] == experiment)
    if published['sha256'] != provenance['sha256'] or git('show', published['public_commit']+':'+provenance['path']) != (ROOT/provenance['path']).read_bytes():
        raise ValueError('PUBLIC_DESIGN_READBACK_MISMATCH')
    code_hashes = {p: sha(ROOT/p)for p in CODE}
    for p in CODE:
        if git('show', 'HEAD:'+p) != (ROOT/p).read_bytes():
            raise ValueError('UNCOMMITTED_V12_CODE:'+p)
    write(public/'code-seal.json', dict(created_utc=utc(), code_commit=git('rev-parse', 'HEAD').decode().strip(),
                                      sha256=code_hashes, design=provenance, public_design=published))
    from v12_inputs import cells_for, load_series, f2_eligibility_inventory
    cells = cells_for(experiment)
    source_status = {}
    for c in cells:
        key = (c['family'], c['source_key'])
        if key not in source_status:
            try:
                a = load_series(c['source'])
                source_status[key] = dict(status='VERIFIED', n=len(a['position']))
            except Exception as exc:
                source_status[key] = dict(status='FAILED_SOURCE', reason=type(exc).__name__+':'+str(exc))
    eligibility = f2_eligibility_inventory() if experiment == 'F2' else None
    eligible_cells,source_excluded = preflight_cells(cells,source_status,eligibility)
    write(public/'input-preflight.json', dict(checked_utc=utc(), sources=[dict(family=k[0],source_key=k[1],**v)for k,v in source_status.items()], eligibility=eligibility))
    start, stamp = time.monotonic(), utc()
    deadline = start+wall_cap(design)
    write(public/'run-start.json', dict(experiment=experiment, started_utc=stamp,
                                       wall_cap_including_pilot=wall_cap(design), planned_geometry_cells=len(cells)))
    pilot_results, pilot_records, pilot_cells = [], [], []
    if experiment == 'F1':
        pilot_cells = [c for c in eligible_cells if c['family'] == 'cftc' and c['source_key'] == '044601']
        pilot_results, pilot_records, _ = start_jobs(group_jobs(pilot_cells, experiment), experiment, private, code_hashes, deadline, workers=1)
        write(public/'pilot.json', dict(started_utc=stamp, ended_utc=utc(), elapsed_seconds=time.monotonic()-start,
                                       reused_without_retry=True, jobs=pilot_records))
    prior_rate = 0.
    if experiment == 'F1':
        completed_work = sum(work_units(c, experiment)for c in pilot_cells
                             if any(result.get('cell', {}).get('cell_id') == c['cell_id'] and all(r.get('status')=='COMPLETE'for r in result.get('rows', [])) for result in pilot_results))
        prior_rate = 3*(time.monotonic()-start)/completed_work if completed_work else float('inf')
    else:
        earlier = json.loads((ROOT/'results/v12/decomposition/runtime.json').read_text())
        prior_rate = earlier['measured_seconds_per_work']*3
    remaining = [c for c in eligible_cells if c['cell_id'] not in {x['cell_id']for x in pilot_cells}]
    scope = predeclared_scope(experiment, remaining, seconds_per_work=prior_rate, remaining_seconds=max(0,deadline-time.monotonic()))
    # JSON has no nonfinite pseudo-numbers; an unmeasurable pilot remains explicit.
    plan_record = dict(scope)
    for k in ('seconds_per_work','projected_remaining_seconds'):
        if not math.isfinite(plan_record[k]): plan_record[k] = None
    write(public/'resource-plan.json', dict(**plan_record, set_before_formal_remaining_run_utc=utc(), rule='No outcomes enter the workload proxy; failed pilot has no trustworthy timing rate.'))
    write(public/'formal-start.json', dict(started_utc=utc(), elapsed_pilot_seconds=time.monotonic()-start))
    results, records, not_started = start_ordered_jobs(scope['cells'], experiment, private, code_hashes, deadline, offset=len(pilot_records))
    results = pilot_results+results; records = pilot_records+records
    by_id = merge_cell_results(results)
    rows, candidates = [], []
    omitted_slots = set(method_slots(scope['omitted']+not_started,experiment))
    if experiment=='F2' and 'omit_QR4'in scope['trim_steps']:
        omitted_slots.update((c['cell_id'],'QR4')for c in cells)
    launched_slots = {tuple(slot):r['result_status']for r in records for slot in r['method_slots']}
    for c in cells:
        expected_methods = ['QR33'] if experiment == 'F3' else ['QR33','QR4']
        data = by_id.get(c['cell_id'], {})
        candidates.extend(data.get('candidates', []))
        actual = {r['method']:r for r in data.get('rows', [])}
        for method in expected_methods:
            if method in actual:
                row = actual[method]
            else:
                missing_state = missing_row_status((c['cell_id'],method),launched_slots,omitted_slots)
                resource = missing_state=='NOT_RUN_RESOURCE_LIMIT'
                source_failed = c['cell_id']in {x['cell_id']for x in source_excluded}
                row = dict(cell_id=c['cell_id'], family=c['family'], source_key=c['source_key'], period=c['period'],
                           horizon=c['horizon'], window=c['window'], validation_n=c['validation_n'], tau=c['tau'], method=method,
                           status='EXCLUDED_ENTIRE_CONTRACT'if source_failed and experiment=='F2' else missing_state,
                           reason=source_status[(c['family'],c['source_key'])].get('reason','SOURCE_PRECHECK_FAILED')if source_failed else'PREDECLARED_RESOURCE_OMISSION'if resource else'NO_COMPLETE_WORKER_RESULT',
                           selected_penalty=None, reference_loss=None, actual_loss=None, relative_loss_pct=None,
                           actual_excess_pct=None, selection_component_pct=None, signal_gap_pct=None)
            rows.append(row)
    write(public/'rows.json', rows); csv_write(public/'rows.csv', rows)
    write(public/'candidates.json', candidates); csv_write(public/'candidates.csv', candidates)
    if experiment == 'F1':
        from v12_decomposition import evaluate_predictions, summarize_rows
        predictions, summary = evaluate_predictions(rows), summarize_rows(rows)
    elif experiment == 'F2':
        from v12_summaries import summarize_validation
        predictions = summarize_validation(rows, eligibility); summary = predictions.get('descriptive_groups', [])
    else:
        from v12_summaries import summarize_tau
        predictions = summarize_tau(rows); summary = predictions['descriptive_groups']
    write(public/'predictions.json', predictions); write(public/'summary.json', summary)
    if summary: csv_write(public/'summary.csv', summary)
    elapsed = time.monotonic()-start
    total_work = sum(work_units(c, experiment)for c in cells if c['cell_id']in by_id)
    runtime = dict(experiment=experiment, started_utc=stamp, completed_utc=utc(), elapsed_seconds=elapsed,
                   wall_cap_seconds=wall_cap(design), pilot_included=True, planned_method_rows=len(rows),
                   complete_method_rows=sum(r['status']=='COMPLETE'for r in rows), jobs=records,
                   measured_seconds_per_work=elapsed/total_work if total_work else 0.,
                   no_candidate_or_cell_retries=True, no_financial_download=True)
    write(public/'runtime.json', runtime)
    write(public/'output-manifest.json', dict(created_utc=utc(),files=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p))for p in sorted(public.iterdir())if p.is_file()]))
    print(json.dumps(dict(experiment=experiment, elapsed_seconds=elapsed, complete=runtime['complete_method_rows'], planned=len(rows), outputs=str(public.relative_to(ROOT))),indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('experiment', choices=['F1','F2','F3'])
    run(parser.parse_args().experiment)
