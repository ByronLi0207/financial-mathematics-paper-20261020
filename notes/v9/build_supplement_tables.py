"""Generate compact supplement tables from saved native archive fields only.

No fitting, forecasting, simulation, inference or summary re-estimation is
performed. Every displayed row has a native-value binding and source SHA.
Optional legacy import copies original bytes from the protected v8 checkout.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
LEGACY=Path('results/v9/legacy-calibrated')
REPORT=Path('results/v9/nonstationarity/postrun/analysis/report.json')
FCSV=Path('results/v9/nonstationarity/audit/f-benchmark-cells.csv')
TABLES={
 'legacy':'v9-legacy-simulation-table.tex',
 'diagnostics':'v9-stability-diagnostics-table.tex',
 'W52':'v9-stability-W52-table.tex',
 'W260':'v9-stability-W260-table.tex',
 'F':'v9-stability-F-table.tex',
}


def sha(raw):return hashlib.sha256(raw).hexdigest()


def prepare_new(path):
    """Preserve any pre-existing untracked output before exclusive creation."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() or path.is_symlink():
        relative=path.resolve().relative_to(ROOT)
        tracked=subprocess.run(['git','ls-files','--error-unmatch',str(relative)],cwd=ROOT,capture_output=True).returncode==0
        if tracked:raise FileExistsError('Refusing to replace tracked output: '+str(path))
        backup=path.with_name(path.name+'.bak');index=1
        while backup.exists() or backup.is_symlink():
            backup=path.with_name(path.name+f'.{index:03}.bak');index+=1
        path.rename(backup)


def write_new(path,raw):
    data=raw if isinstance(raw,bytes) else raw.encode()
    if Path(path).is_file() and not Path(path).is_symlink() and Path(path).read_bytes()==data:
        return  # Identical existing artifact is verified, never overwritten.
    prepare_new(path)
    with Path(path).open('xb') as f:f.write(data)


def import_legacy(source_root):
    source_root=Path(source_root).resolve();destination=ROOT/LEGACY
    if destination.exists():raise FileExistsError(str(destination))
    names=['analysis-facts.json','calibration.json','environment.json','experiment-settings.json',
           'main-results.md','predictions.json','run-plan.json','summary.csv','summary.json','verification.json',
           'pilot-timing.json','formal/completion.json','formal/receipt.json','formal/replicates.json',
           'formal/worker-logs-manifest.json','formal/worker-logs.zip',
           'pilot/completion.json','pilot/receipt.json','pilot/replicates.json']
    pairs=[(Path('results/v8/mc')/name,Path(name)) for name in names]
    pairs += [(Path(name),Path('source')/Path(name).name) for name in
              ['v8_mc.py','v8_mc_calibrate.py','v8_mc_dgp.py','protocol/v8/mc-design.md',
               'notes/v8/mc-main-bindings.json','notes/v8/mc-supplement-bindings.json']]
    raw={}
    for original,target in pairs:
        path=source_root/original
        if path.is_symlink() or not path.is_file():raise ValueError('INVALID_LEGACY_SOURCE:'+str(path))
        raw[str(target)]=path.read_bytes()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source_root,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=source_root,text=True).strip()
    destination.mkdir(parents=True,exist_ok=False);entries=[]
    for original,target in pairs:
        data=raw[str(target)];path=destination/target
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f:f.write(data)
        if path.read_bytes()!=data or (source_root/original).read_bytes()!=data:raise ValueError('LEGACY_BYTE_COPY_MISMATCH')
        entries.append(dict(source_path=str(original),destination_path=str(target),bytes=len(data),sha256=sha(data)))
    manifest=dict(schema='v9-legacy-calibrated-import-1',created_utc=datetime.now(timezone.utc).isoformat(),
                  source_checkout=str(source_root),source_head=head,source_branch=branch,
                  source_read_only=True,numerical_rerun=False,files=entries)
    with (destination/'manifest.json').open('x') as f:json.dump(manifest,f,indent=2);f.write('\n')
    readme=f'''# Legacy calibrated Monte Carlo: byte-preserved v8 import

Source checkout: `{source_root}`; branch `{branch}`; HEAD `{head}`.
Every imported source/destination byte count and SHA-256 is in `manifest.json`.
All {len(entries)} imported files were copied and compared as raw bytes. The source checkout was read only.
No experiment, fit, forecast, diagnosis, statistical test, aggregation or repair was run.

`summary.json` is the sole v9 native source for the new 24-row legacy table:
17 COMPLETE cells and seven FAILED D1 cells. Partial success never supplies a failed-cell median.
The complete replicate archive and all 300 worker logs remain in their original ZIP/index.
Original protocol, three MC modules and numeric bindings are retained under `source/` for provenance;
they are snapshots, not a promise that executing that subdirectory reproduces the original checkout.

D0 must be described as **constant-variance AR(1) levels, where the peak depends on the current position**.
The peak therefore carries conditional information. Any older narrative implying no conditional signal is not adopted.
Archive bytes, including historical wording, are preserved rather than rewritten.
D1 denotes the old FX-calibrated hourly design; seven of its eight required cells failed ADMM convergence.
D2 is the old weekly-calibrated design. These designs differ from PR5 WP3 and C2 in menus, clocks,
features, calibration, repetition/evaluation lengths and estimands; they must not be merged numerically.

The original `{source_root}/results/v8/mc/` and all protected branches/results remain untouched.
'''
    with (destination/'README.md').open('x') as f:f.write(readme)
    return manifest


def tex(value):
    translations={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}
    return ''.join(translations.get(c,c) for c in str(value))


def code(source):return source[5:] if source.startswith('PDPOS') else {'fx_daily':'FX daily','fx_hourly':'FX hourly'}.get(source,source)
def number(value,digits=3):return '--' if value is None else f'{float(value):.{digits}g}'
def fixed(value,digits=3):return '--' if value is None else f'{float(value):.{digits}f}'
def delta(value):return '--' if value is None else f'{float(value):+.1f}'
def interval(m,q1,q3,loss=False):
    if m is None:return '--'
    fmt=(lambda x:f'{float(x):.4g}') if loss else (lambda x:f'{float(x):.1f}')
    return r'\('+fmt(m)+r'\,['+fmt(q1)+','+fmt(q3)+r']\)'


def longtable(caption,label,spec,header,body,notes):
    columns=len(header);head=' & '.join(header)+r'\\'
    result=[r'\begingroup',r'\fontsize{9}{10.2}\selectfont',r'\setlength{\tabcolsep}{2.2pt}',
            r'\renewcommand{\arraystretch}{1.05}',r'\setlength{\LTpre}{2pt}',r'\setlength{\LTpost}{3pt}',
            r'\begin{longtable}{'+spec+'}',r'\caption{'+caption+r'}\label{'+label+r'}\\',r'\toprule',head,r'\midrule',r'\endfirsthead',
            r'\toprule',head,r'\midrule',r'\endhead',r'\midrule',r'\multicolumn{'+str(columns)+r'}{r}{\emph{Continued on next page}}\\',
            r'\endfoot',r'\bottomrule',r'\endlastfoot']
    result += body
    result += [r'\end{longtable}',r'\noindent\parbox{\linewidth}{\fontsize{8}{9.2}\selectfont '+notes+'}',r'\endgroup','']
    return '\n'.join(result)


def build(output_dir=None):
    output_dir=ROOT/'submission-jof/generated' if output_dir is None else Path(output_dir)
    legacy_path=ROOT/LEGACY/'summary.json';facts_path=ROOT/LEGACY/'analysis-facts.json';report_path=ROOT/REPORT;f_path=ROOT/FCSV
    legacy=json.loads(legacy_path.read_text());report=json.loads(report_path.read_text())
    facts=json.loads(facts_path.read_text())
    frows=list(csv.DictReader(f_path.open()))
    if len(legacy)!=24 or Counter(r['status'] for r in legacy)!=Counter(COMPLETE=17,FAILED=7):raise ValueError('LEGACY_GRID_CENSUS')
    if any(r['dgp']!='D1' for r in legacy if r['status']=='FAILED'):raise ValueError('LEGACY_FAILURE_IDENTITY')
    if len(report['diagnostics'])!=15 or len(report['cells'])!=104 or len(frows)!=52:raise ValueError('C2_TABLE_CENSUS')
    inputs={str(LEGACY/'summary.json'):sha(legacy_path.read_bytes()),str(LEGACY/'analysis-facts.json'):sha(facts_path.read_bytes()),
            str(REPORT):sha(report_path.read_bytes()),str(FCSV):sha(f_path.read_bytes())}
    bindings=[];outputs={}
    def bind(table,source,selector,native,display):
        bindings.append(dict(table=table,source=source,selector=selector,native=native,display=display))
        return '% Native: '+json.dumps(dict(source=source,selector=selector,native=native),separators=(',',':'))

    body=[]
    for index,row in enumerate(legacy):
        complete=row['status']=='COMPLETE'
        values=[row['dgp'],str(row['window']),str(row['features']),f"{row['completed_repetitions']}/{row['required_repetitions']}",
                interval(row['qr_median_pct'],row['qr_q25_pct'],row['qr_q75_pct']) if complete else r'\textbf{FAIL}',
                fixed(row['win_rate']),('--' if row['i_median_pct'] is None else f"{row['i_median_pct']:+.3f}"),
                delta(row['oracle_median_pct']),fixed(row['f_breach_median']),fixed(row['i_breach_median']),
                fixed(row['qr_breach_median']),fixed(row['oracle_breach_median']),fixed(row['infinity_frequency'])]
        body += [bind('legacy',str(LEGACY/'summary.json'),{'index':index,'dgp':row['dgp'],'window':row['window'],'features':row['features']},row,values),' & '.join(values)+r'\\']
    outputs['legacy']=longtable('Legacy calibrated simulation: all 24 planned cells.','tab:v9-legacy-mc',
         r'crrcp{33mm}rrrrrrrr',['DGP','$W$','$p$','$R$','QR $\Delta$ [IQR]','Win','I $\Delta$','O $\Delta$','F hit','I hit','QR hit','O hit','$\infty$'],body,
         r'$\Delta$ is the median relative loss change against F (percent); IQR is across registered repetitions. Win and hit columns are proportions; I is the ordinary empirical quantile and O is the finite nested oracle. '
         r'The $\infty$ column is the frequency of selecting the intercept limit. '
         r'All seven failed D1 rows remain unavailable after ADMM nonconvergence, even when some repetitions completed. '
         r'D0: constant-variance AR(1) levels, where the peak depends on the current position. D1: FX-calibrated hourly; D2: weekly-calibrated. '
         r'The broader legacy menu includes the intercept limit; these results are not the WP3 ratio-of-mean-losses.')
    events=facts['failure_events']
    if len(events)!=7:raise ValueError('LEGACY_FAILURE_EVENT_CENSUS')
    failures=[]
    for index,row in enumerate(events):
        values=[tex(row['dgp']),str(row['window']),str(row['features']),str(row['rep']),tex(row['failure_stage']),
                number(row['failure_lambda']),tex(row['reason'])]
        failures += [bind('legacy-failures',str(LEGACY/'analysis-facts.json'),{'index':index},row,values),' & '.join(values)+r'\\']
    outputs['legacy'] += longtable('First recorded failure in each unavailable legacy cell.','tab:v9-legacy-failures',
        r'crrrlrp{60mm}',['DGP','$W$','$p$','Rep','Stage','$\lambda$','Saved reason'],failures,
        r'Repetition identifiers are zero based. Each event belongs to a whole failed cell in Table~\ref{tab:v9-legacy-mc}; no partial repetition summary is substituted. '
        r'The original failure stage, penalty and reason are retained without a rerun.')

    body=[]
    for row in report['diagnostics']:
        state=('NR' if row['status']=='NONREGULAR_NULL' else 'OF' if row['status']=='FAILED' and 'GARCH_OPTIMIZATION_FAILED' in row['failures']
               else 'BF' if row.get('null_boundary_status')=='BOUNDARY_FIT' else 'OK' if row['status']=='COMPLETE' else 'FAIL')
        dates='/'.join(v.split('T')[0] for v in row['break_dates']) or '--'
        values=[tex(code(row['source_id'])),number(row['statistic']),number(row['p_value']),number(row['holm13_p']),
                'Y' if row['moment_qualified'] is True else 'N' if row['moment_qualified'] is False else '--',number(row['q4']),
                '--' if row['cuts'] is None else '/'.join(map(str,row['cuts'])) or 'none',tex(dates),
                '--' if row['segment_lengths'] is None else '/'.join(map(str,row['segment_lengths'])),
                '--' if row['min_segment'] is None else str(row['min_segment']), 'Y' if row['cap_reached'] is True else 'N' if row['cap_reached'] is False else '--',state]
        body += [bind('diagnostics',str(REPORT),{'source_id':row['source_id']},row,values),' & '.join(values)+r'\\']
    outputs['diagnostics']=longtable('Registered prefix stability diagnostics: all 15 source rows.','tab:v9-stability-diagnostics',
        r'lrrrcrlllrcc',['Source','$H$','$p$','Holm','M4','$q_4$','Cuts','Dates','Segments','$h$','Cap','State'],body,
        r'$H$: Hansen joint statistic; $h$: minimum segment transitions; M4: registered fitted-null fourth-moment qualification. '
        r'Cuts use transition-row units; dates mark the first target after each cut. Unarchived dates remain -- even when cuts are available. Source codes omit the common PDPOS prefix. '
        r'NR: daily FX NONREGULAR\_NULL (Student fourth moment unavailable); OF: hourly FX GARCH\_OPTIMIZATION\_FAILED. '
        r'BF: a restricted-boundary fit; OK does not certify the model. Unavailable raw $p$ and Holm values remain --; internal Holm placeholders are not tests. '
        r'Segmentation is descriptive, and the two-break cap does not establish significant individual breaks.')

    by={(r['source_id'],r['arm'],r['window'],r['method']):r for r in report['cells']}
    sources=[r['source_id'] for r in report['diagnostics'] if r['kind']=='weekly']
    for W in [52,260]:
        body=[]
        for source in sources:
            for arm in ['constant','switching']:
                values=[tex(code(source)),'C' if arm=='constant' else 'S'];native={}
                for method in ['QR33','QR4']:
                    row=by[(source,arm,W,method)];native[method]=row
                    if row['status']=='COMPLETE':
                        values += [interval(row['relative_median_pct'],row['q25_pct'],row['q75_pct']),fixed(row['win_fraction']),fixed(row['qr_breach_median'])]
                    else:
                        values += [r'\textbf{FAIL} '+f"{row['completed_repetitions']}/{row['required_repetitions']}",'--','--']
                body += [bind('W'+str(W),str(REPORT),{'source_id':source,'arm':arm,'window':W},native,values),' & '.join(values)+r'\\']
        outputs['W'+str(W)]=longtable('Complete source-by-arm conditional comparison, $W='+str(W)+r'$.','tab:v9-stability-w'+str(W),
              r'lcp{37mm}rrp{37mm}rr',['Source','Arm','QR33 $\Delta$ [IQR]','Win','Hit','QR4 $\Delta$ [IQR]','Win','Hit'],body,
              r'C: fitted constant control; S: parameter-switching stress. Source codes omit PDPOS. '
              r'$\Delta$: median percent relative loss against the matched F across all 32 registered repetitions, with IQR. Win and QR hit are proportions. '
              r'FAIL $31/32$ is a whole failed cell, with no partial median or win/hit summary; all mandatory repeats must succeed. '
              r'The failed QR33 W260 cells are PDPOSTIPS-G11, repetition 24, in both arms, caused by validation NONCONVERGENCE. '
              r'QR4 may select a completed candidate under the unchanged registered policy; its failed candidates remain in the archive.')

    body=[]
    for row in frows:
        def native(key):return None if row[key]=='' else float(row[key])
        values=[tex(code(row['source_id'])),'C' if row['arm']=='constant' else 'S',row['window'],f"{row['complete_repetitions']}/{row['required_repetitions']}",
                interval(native('mean_loss_median'),native('mean_loss_q25'),native('mean_loss_q75'),loss=True),
                interval(native('breach_rate_median'),native('breach_rate_q25'),native('breach_rate_q75'),loss=True)]
        if row['status']!='COMPLETE':values[4:]=[r'\textbf{FAIL}','--']
        body += [bind('F',str(FCSV),{'source_id':row['source_id'],'arm':row['arm'],'window':row['window']},row,values),' & '.join(values)+r'\\']
    outputs['F']=longtable('Corrected-rank F benchmark: all 52 source-by-arm-history cells.','tab:v9-stability-f',
          r'lcrcp{44mm}p{44mm}',['Source','Arm','$W$','$R$','Loss [IQR]','Hit [IQR]'],body,
          r'C: fitted constant control; S: parameter-switching stress. Source codes omit PDPOS. '
          r'Loss is the median across repetitions of the within-repetition mean pinball score, with IQR; Hit is the corresponding breach-rate median and IQR. '
          r'All 52 cells have 32/32 valid final F receipts. Loss units follow each source-specific whole-prefix SD normalization; different sources are not pooled. '
          r'No failed-cell partial median is substituted.')
    for key,text in outputs.items():
        filename=TABLES[key]
        header='% Generated by notes/v9/build_supplement_tables.py; saved-field display only.\n'
        header += '% Source SHA256: '+json.dumps(inputs,separators=(',',':'))+'\n'
        write_new(output_dir/filename,header+text)
    receipt=dict(schema='v9-supplement-native-table-bindings-1',generator_sha256=sha(Path(__file__).read_bytes()),
                 input_sha256=inputs,planned_rows={'legacy':24,'legacy-failures':7,'diagnostics':15,'W52':26,'W260':26,'F':52},
                 native_bindings=bindings,output_sha256={TABLES[k]:sha((output_dir/TABLES[k]).read_bytes()) for k in outputs},
                 scientific_computations=0,models_refitted=0)
    write_new(output_dir/'v9-table-bindings.json',json.dumps(receipt,indent=2)+'\n')
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--import-legacy-source',type=Path);parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    if args.import_legacy_source:import_legacy(args.import_legacy_source)
    receipt=build(args.output_dir)
    print(json.dumps(dict(rows=receipt['planned_rows'],native_rows=len(receipt['native_bindings']),outputs=receipt['output_sha256']),indent=2))


if __name__=='__main__':main()
