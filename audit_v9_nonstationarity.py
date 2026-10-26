"""Audit saved formal ZIP receipts and summarize complete F benchmark cells.

This module reads only an already completed archive and never imports a study,
fitting, diagnostic, generation or prediction module. Output audit/ is new and
exclusive. Missing planned receipts are counted explicitly, never as success.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path, PurePosixPath
from statistics import median
import zipfile


INPUTS=('manifest.json','formal/plan.json','formal/completion.json',
        'formal/units-manifest.json','formal/units.zip')


class AuditError(ValueError):
    pass


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _number(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)


def _quantile(values,p):
    values=sorted(values);at=(len(values)-1)*p;left=int(math.floor(at))
    return float(values[left]+(values[min(left+1,len(values)-1)]-values[left])*(at-left))


def _same(a,b):
    if a is None or b is None:return a is b
    return _number(a) and _number(b) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)


def _safe_member(name):
    return isinstance(name,str) and name and not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts and '\\' not in name


def _verify_zip(archive,index):
    expected={}
    for entry in index.get('files',[]):
        name=entry.get('path')
        if not _safe_member(name) or name in expected:
            raise AuditError('INDEX_PATH_INVENTORY')
        if not isinstance(entry.get('bytes'),int) or entry['bytes']<0 or not isinstance(entry.get('sha256'),str):
            raise AuditError('INDEX_ENTRY_FIELDS:'+name)
        expected[name]=entry
    actual=archive.infolist()
    if len(actual)!=len({i.filename for i in actual}):raise AuditError('ZIP_DUPLICATE_MEMBER')
    if {i.filename for i in actual}!=set(expected):raise AuditError('ZIP_INDEX_MEMBER_INVENTORY')
    rows=[]
    for info in actual:
        if info.is_dir() or not _safe_member(info.filename):raise AuditError('ZIP_UNSAFE_MEMBER')
        digest=hashlib.sha256();size=0
        with archive.open(info) as source:
            while True:
                block=source.read(1024*1024)
                if not block:break
                size+=len(block);digest.update(block)
        entry=expected[info.filename]
        if size!=entry['bytes'] or size!=info.file_size or digest.hexdigest()!=entry['sha256']:
            raise AuditError('ENTRY_BYTES_OR_SHA256_MISMATCH:'+info.filename)
        rows.append(dict(path=info.filename,bytes=size,sha256=digest.hexdigest(),status='PASS'))
    return expected,rows


def _member_json(archive,members,name):
    if name not in members:return None,'NOT_ARCHIVED'
    try:
        result=json.loads(archive.read(name))
        if not isinstance(result,dict):raise ValueError('object required')
        return result,None
    except (ValueError,UnicodeError):
        return None,'INVALID_JSON'


def _evaluation(receipt,n):
    e=receipt.get('evaluation')
    if (not isinstance(e,dict) or type(e.get('n')) is not int or e['n']!=n
            or not _number(e.get('mean_loss')) or e['mean_loss']<0
            or type(e.get('strict_breach_count')) is not int
            or not 0<=e['strict_breach_count']<=n
            or not _same(e.get('strict_breach_rate'),e['strict_breach_count']/n)):
        return None
    return e


def _completion_index(completion,expected):
    indexed={}
    for row in completion.get('tasks',[]):
        task=row.get('task') or {};key=(task.get('source'),task.get('rep'))
        if key not in expected or key in indexed:raise AuditError('COMPLETION_TASK_INVENTORY')
        unit=expected[key]
        if task.get('worker')!='worker-forecast' or Path(task.get('output','')).parent.name!=unit:
            raise AuditError('COMPLETION_TASK_IDENTITY')
        indexed[key]=row
    if set(indexed)!=set(expected):raise AuditError('COMPLETION_MISSING_PLANNED_TASK')
    return indexed


def _build_receipts(archive,members,manifest,plan,completion):
    sources=manifest.get('sources',[])
    if len(sources)!=15 or len({s.get('source_id') for s in sources})!=15 or any(s.get('kind')!='weekly' for s in sources[:13]):
        raise AuditError('MANIFEST_SOURCE_INVENTORY')
    weekly=sources[:13];R=plan.get('repetitions');conditional=plan.get('conditional_methods')
    if type(R) is not int or R<1 or conditional not in [['QR33'],['QR33','QR4']]:raise AuditError('FORMAL_PLAN')
    design=manifest.get('design',{});windows=design.get('windows');H=design.get('horizon')
    if windows!=[52,260] or H!=6:raise AuditError('REGISTERED_GEOMETRY')
    n=design['evaluation_last']-design['evaluation_first']+1
    validation_n=design['validation_last']-design['validation_first']+1
    if n!=72 or validation_n!=72:raise AuditError('REGISTERED_ORIGIN_COUNTS')
    menus=design.get('menus',{})
    if menus.get('QR33')!=[.001,.01,.1] or menus.get('QR4')!=[.001,.01,.1,1.,10.]:raise AuditError('REGISTERED_CANDIDATE_MENUS')
    planned_units={(si,rep):f's{si:02}-r{rep:03}' for rep in range(R) for si in range(13)}
    completed=_completion_index(completion,planned_units)
    units,methods,candidates,selections=[],[],[],[]
    for (si,rep),unit in planned_units.items():
        source=weekly[si]['source_id'];result_path=unit+'/result.json'
        result,result_error=_member_json(archive,members,result_path)
        identity_ok=(result is not None and result.get('source_id')==source
                     and result.get('source_index')==si and result.get('rep')==rep)
        task=completed[(si,rep)]
        units.append(dict(source_id=source,source_index=si,rep=rep,unit=unit,
                          result_archived=result_path in members,identity_valid=identity_ok,
                          status='NOT_ARCHIVED' if result is None else 'INVALID_IDENTITY' if not identity_ok else 'TASK_COMPLETE' if result.get('complete') is True else 'TASK_INCOMPLETE',
                          reason=result_error if result is None else result.get('reason'),
                          elapsed_seconds=task.get('elapsed_seconds'),exit_code=task.get('exit_code')))
        for arm,W,method in itertools.product(['constant','switching'],windows,['F',*conditional]):
            prefix=f'{unit}/{arm}/W{W}_H{H}_{method}'
            identity=dict(source_id=source,source_index=si,rep=rep,arm=arm,window=W,horizon=H,method=method,planned=True)
            candidate_rows=[]
            for index,penalty in enumerate(menus.get(method,[])):
                path=prefix+f'_validation-{index}.json';raw,error=_member_json(archive,members,path)
                status=error or raw.get('status','INVALID_RECEIPT')
                reason=error if error else raw.get('reason')
                if raw is not None:
                    if (not _same(raw.get('penalty'),penalty) or status not in ['COMPLETE','FAILED','INCOMPLETE']
                            or (status=='COMPLETE' and (raw.get('origin_count')!=validation_n
                                or not _number(raw.get('mean_loss')) or raw['mean_loss']<0))):
                        status,reason='INVALID_RECEIPT','INVALID_CANDIDATE_FIELDS'
                row=dict(**identity,candidate_index=index,penalty=penalty,path=path,archived=path in members,
                         receipt_status=status,reason=reason,
                         origin_count=None if raw is None else raw.get('origin_count'),
                         mean_loss=None if raw is None else raw.get('mean_loss'),
                         failure_kind=None if raw is None else raw.get('failure_kind'),
                         exception_type=None if raw is None else raw.get('exception_type'),
                         failure_diagnostics=None if raw is None else raw.get('failure_diagnostics'),
                         failure_progress=None if raw is None else raw.get('failure_progress'))
                candidates.append(row);candidate_rows.append(row)
            selected=None;selection_status='NOT_APPLICABLE';selection_error=None
            if method!='F':
                selection_path=prefix+'.selection.json';selection,selection_error=_member_json(archive,members,selection_path)
                selection_status=selection_error or selection.get('status','INVALID_RECEIPT')
                selected=None if selection is None else selection.get('penalty')
                selections.append(dict(**identity,path=selection_path,archived=selection_path in members,
                                       receipt_status=selection_status,selected_penalty=selected,
                                       reason=selection_error))
            path=prefix+'.json';raw,error=_member_json(archive,members,path)
            receipt_status=error or raw.get('status','INVALID_RECEIPT')
            audit_status=receipt_status;reasons=[];evaluation=None
            if error:reasons.append(error)
            elif receipt_status not in ['COMPLETE','FAILED']:
                audit_status='INVALID_RECEIPT';reasons.append('INVALID_METHOD_STATUS')
            elif receipt_status=='COMPLETE':
                evaluation=_evaluation(raw,n)
                if evaluation is None:
                    audit_status='INVALID_RECEIPT';reasons.append('INVALID_COMPLETE_EVALUATION')
                if method!='F':
                    complete_candidates=[r for r in candidate_rows if r['receipt_status']=='COMPLETE']
                    all_present=all(r['receipt_status'] in ['COMPLETE','FAILED','INCOMPLETE'] for r in candidate_rows)
                    eligible=all_present and (len(complete_candidates)==len(candidate_rows) if method=='QR33' else bool(complete_candidates))
                    if not eligible:
                        audit_status='INVALID_RECEIPT';reasons.append('COMPLETE_METHOD_WITH_INELIGIBLE_OR_MISSING_CANDIDATES')
                    else:
                        chosen=min(complete_candidates,key=lambda r:(r['mean_loss'],-r['penalty'] if method=='QR33' else r['candidate_index']))
                        if (selection_status!='SELECTED' or not _same(selected,chosen['penalty'])
                                or not _same(raw.get('selected_penalty'),chosen['penalty'])):
                            audit_status='INVALID_RECEIPT';reasons.append('SELECTED_PENALTY_POLICY_MISMATCH')
                    inline=raw.get('candidates')
                    if not isinstance(inline,list) or len(inline)!=len(candidate_rows):
                        audit_status='INVALID_RECEIPT';reasons.append('INLINE_CANDIDATE_INVENTORY')
                    else:
                        for inline_row,candidate in zip(inline,candidate_rows):
                            if (inline_row.get('status')!=candidate['receipt_status']
                                    or not _same(inline_row.get('penalty'),candidate['penalty'])):
                                audit_status='INVALID_RECEIPT';reasons.append('INLINE_CANDIDATE_STATUS_MISMATCH');break
            if not identity_ok:
                audit_status='INVALID_RECEIPT' if raw is not None else 'NOT_ARCHIVED'
                reasons.append('UNIT_IDENTITY_UNAVAILABLE_OR_INVALID')
            if raw is not None and raw.get('reason'):reasons.append(str(raw['reason']))
            if raw is None and prefix+'.started.json' in members:reasons.append('STARTED_WITHOUT_FINAL_RECEIPT')
            if result is not None and result.get('reason'):reasons.append('UNIT:'+str(result['reason']))
            methods.append(dict(**identity,path=path,archived=path in members,
                                started_archived=prefix+'.started.json' in members,
                                receipt_status=receipt_status,audit_status=audit_status,
                                selected_penalty=None if raw is None else raw.get('selected_penalty'),
                                selection_status=selection_status,candidate_planned=len(candidate_rows),
                                candidate_status_counts=dict(Counter(r['receipt_status'] for r in candidate_rows)),
                                mean_loss=None if evaluation is None or audit_status!='COMPLETE' else evaluation['mean_loss'],
                                strict_breach_count=None if evaluation is None or audit_status!='COMPLETE' else evaluation['strict_breach_count'],
                                strict_breach_rate=None if evaluation is None or audit_status!='COMPLETE' else evaluation['strict_breach_rate'],
                                n=None if evaluation is None else evaluation['n'],reasons=reasons))
    return weekly,R,conditional,units,methods,candidates,selections


def _cells(weekly,R,conditional,methods):
    indexed={(r['source_id'],r['rep'],r['arm'],r['window'],r['method']):r for r in methods}
    method_cells,f_cells,conditional_cells=[],[],[]
    for source,arm,W,method in itertools.product([s['source_id'] for s in weekly],['constant','switching'],[52,260],['F',*conditional]):
        rows=[indexed[(source,rep,arm,W,method)] for rep in range(R)]
        good=[r for r in rows if r['audit_status']=='COMPLETE']
        failed=[r['rep'] for r in rows if r['audit_status']!='COMPLETE']
        cell=dict(source_id=source,arm=arm,window=W,method=method,status='COMPLETE' if not failed else 'FAILED',
                  required_repetitions=R,complete_repetitions=len(good),failed_repetitions=failed,
                  receipt_status_counts=dict(Counter(r['receipt_status'] for r in rows)),
                  audit_status_counts=dict(Counter(r['audit_status'] for r in rows)))
        method_cells.append(cell)
        if method=='F':
            fcell=dict(cell,mean_loss_median=None,mean_loss_q25=None,mean_loss_q75=None,
                       breach_rate_median=None,breach_rate_q25=None,breach_rate_q75=None)
            if not failed:
                losses=[r['mean_loss'] for r in good];breaches=[r['strict_breach_rate'] for r in good]
                fcell.update(mean_loss_median=float(median(losses)),mean_loss_q25=_quantile(losses,.25),mean_loss_q75=_quantile(losses,.75),
                             breach_rate_median=float(median(breaches)),breach_rate_q25=_quantile(breaches,.25),breach_rate_q75=_quantile(breaches,.75))
            f_cells.append(fcell)
        else:
            paired_failed=[rep for rep in range(R) if indexed[(source,rep,arm,W,method)]['audit_status']!='COMPLETE'
                           or indexed[(source,rep,arm,W,'F')]['audit_status']!='COMPLETE']
            conditional_cells.append(dict(source_id=source,arm=arm,window=W,method=method,
                                          status='COMPLETE' if not paired_failed else 'FAILED',required_repetitions=R,
                                          complete_repetitions=R-len(paired_failed),failed_repetitions=paired_failed))
    return method_cells,f_cells,conditional_cells


def _display(value):
    if value is None:return 'NA'
    return json.dumps(value,ensure_ascii=False,separators=(',',':')) if isinstance(value,(list,dict)) else str(value)


def _table(rows,columns):
    return '\n'.join(['| '+' | '.join(columns)+' |','|'+'|'.join(['---']*len(columns))+'|']+
                     ['| '+' | '.join(_display(row.get(k)).replace('|','\\|').replace('\n',' ') for k in columns)+' |' for row in rows])+'\n'


def _write_table(directory,name,rows):
    if not rows:return
    columns=list(rows[0])
    with (directory/(name+'.csv')).open('x',newline='') as f:
        writer=csv.DictWriter(f,columns);writer.writeheader()
        for row in rows:writer.writerow({k:_display(v) if isinstance(v,(list,dict)) else v for k,v in row.items()})
    with (directory/(name+'.md')).open('x') as f:f.write('# '+name+'\n\n'+_table(rows,columns))


def audit_archive(archive_dir):
    root=Path(archive_dir);payloads={};input_hashes={}
    for name in INPUTS:
        path=root/name
        if not path.is_file() or path.is_symlink():raise AuditError('MISSING_OR_NONREGULAR_INPUT:'+name)
        raw=path.read_bytes();input_hashes[name]=_sha(raw)
        if not name.endswith('.zip'):payloads[name]=json.loads(raw)
    index=payloads['formal/units-manifest.json']
    if input_hashes['formal/units.zip']!=index.get('archive_sha256'):raise AuditError('ZIP_SHA256_MISMATCH')
    with zipfile.ZipFile(root/'formal/units.zip') as archive:
        members,files=_verify_zip(archive,index)
        weekly,R,conditional,units,methods,candidates,selections=_build_receipts(archive,members,payloads['manifest.json'],payloads['formal/plan.json'],payloads['formal/completion.json'])
    method_cells,f_cells,conditional_cells=_cells(weekly,R,conditional,methods)
    counts=dict(unit_tasks=dict(Counter(r['status'] for r in units)),method_receipt_status=dict(Counter(r['receipt_status'] for r in methods)),
                audited_methods=dict(Counter(r['audit_status'] for r in methods)),candidate_receipt_status=dict(Counter(r['receipt_status'] for r in candidates)),
                selection_receipt_status=dict(Counter(r['receipt_status'] for r in selections)),F_cells=dict(Counter(r['status'] for r in f_cells)),
                conditional_cells=dict(Counter(r['status'] for r in conditional_cells)))
    failures=dict(failed_candidates=[r for r in candidates if r['receipt_status'] in ['FAILED','INCOMPLETE']],
                  unarchived_candidates=[r for r in candidates if r['receipt_status']=='NOT_ARCHIVED'],
                  invalid_candidates=[r for r in candidates if r['receipt_status'] not in ['COMPLETE','FAILED','INCOMPLETE','NOT_ARCHIVED']],
                  failed_or_missing_methods=[r for r in methods if r['audit_status']!='COMPLETE'],
                  failed_F_cells=[r for r in f_cells if r['status']!='COMPLETE'],
                  failed_conditional_cells=[r for r in conditional_cells if r['status']!='COMPLETE'])
    report=dict(schema='v9-formal-zip-audit-v1',status='AUDITED',created_utc=datetime.now(timezone.utc).isoformat(),
                integrity=dict(status='PASS',verified_files=len(files),zip_sha256=input_hashes['formal/units.zip']),
                input_sha256=input_hashes,
                planned=dict(sources=13,repetitions=R,units=13*R,method_receipts=len(methods),candidate_receipts=len(candidates),
                             F_cells=52,conditional_cells=len(conditional_cells),conditional_methods=conditional),
                counts=counts,failures=failures,units=units,methods=methods,candidates=candidates,selections=selections,
                method_cells=method_cells,f_cells=f_cells,conditional_cells=conditional_cells,
                interpretation='ZIP integrity and saved-receipt census only; failed F cells have no partial median. No rerun or repaired output.')
    out=root/'audit';out.mkdir(exist_ok=False)
    for name,rows in [('integrity-files',files),('unit-tasks',units),('selected-method-receipts',methods),
                      ('candidate-receipts',candidates),('selection-receipts',selections),('method-cells',method_cells),
                      ('f-benchmark-cells',f_cells),('conditional-cells',conditional_cells)]:
        _write_table(out,name,rows)
    with (out/'summary.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    with (out/'failures.json').open('x') as f:json.dump(failures,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    text=['# 正式归档审计与 F 基准汇总','',
          '仅核对已保存 ZIP/index、计划、completion 与模型/候选回执；未重跑、补跑、修复或改变研究规则。所有候选按正式计划逐项列出，未落盘不会当成功。','',
          '## ZIP完整性','',json.dumps(report['integrity'],ensure_ascii=False),'',
          '## 计划与回执计数','',json.dumps(report['planned'],ensure_ascii=False,indent=2),'',json.dumps(counts,ensure_ascii=False,indent=2),'',
          '## 完整 F 格','',
          '每格必须有全部登记重复且最终 F 回执有效，才报告各重复的平均 pinball loss 及 breach rate 的中位数与IQR。任何失败/缺失格全部汇总留空，不用成功部分的中位数。',
          _table(f_cells,list(f_cells[0])),'',
          '## 真正失败与未落盘分开','',
          f"真实 FAILED/INCOMPLETE 候选 {len(failures['failed_candidates'])}；未落盘候选 {len(failures['unarchived_candidates'])}；非法候选回执 {len(failures['invalid_candidates'])}。", 
          f"F整格失败 {len(failures['failed_F_cells'])}；配对条件整格失败 {len(failures['failed_conditional_cells'])}。完整 source/rep/arm/W/method/index/penalty/reason 见 failures.json 与全量CSV。", 
          'QR4 的非必需候选失败可与其最终所选方法成功并存；QR33 必须全部验证候选成功。TASK_COMPLETE 仅指worker归档完成，不等于所有模型成功。','']
    with (out/'summary.md').open('x') as f:f.write('\n'.join(text))
    outputs={p.name:dict(bytes=p.stat().st_size,sha256=_sha(p.read_bytes())) for p in out.iterdir() if p.is_file()}
    with (out/'audit-manifest.json').open('x') as f:json.dump(dict(inputs=input_hashes,outputs=outputs,exclusive=True,financial_recomputations=0),f,ensure_ascii=False,indent=2);f.write('\n')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive_dir',type=Path);args=parser.parse_args()
    report=audit_archive(args.archive_dir)
    print(json.dumps(dict(status=report['status'],integrity=report['integrity'],planned=report['planned'],counts=report['counts'],
                          failed_candidates=len(report['failures']['failed_candidates']),unarchived_candidates=len(report['failures']['unarchived_candidates'])),ensure_ascii=False))


if __name__=='__main__':main()
