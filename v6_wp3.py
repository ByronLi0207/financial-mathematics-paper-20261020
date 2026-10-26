"""WP3 complete fixed report combinations. Root-owned serial financial entry."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import v6_inference as inf
from v6_combinations import combine_reports,murphy_exact,METHODS

CONTROLS=('F','QR')

def aggregate(cells,load):
    if len(cells)!=56 or len({r['cell_id'] for r in cells})!=56:raise ValueError('EXACT_56_UNIQUE_CELLS_REQUIRED')
    rows=[];comparisons=[];controls=[];murphy=[];curves={};input_proofs=[]
    for cell in cells:
        data=load(cell);ids=np.asarray(data['origins']);floor=np.asarray(data['floor']);peak=np.asarray(data['peak'])
        if peak.shape!=floor.shape or peak.shape!=ids.shape or not np.isfinite(peak).all() or np.any(peak<floor):raise ValueError('PEAK_FLOOR_IDENTITY')
        identity={k:cell[k] for k in ('cell_id','source','horizon','window','native_unit','original')}
        h=cell['horizon'];combos=combine_reports(ids,floor,data['F'],data['QR'],data.get('KNN'))
        base_scores={m:inf.summarize_scores(peak,data[m],tau=.95,origins=ids,horizon=h) for m in CONTROLS}
        losses={m:inf.pinball_losses(peak,data[m],tau=.95) for m in CONTROLS}
        input_proofs.append(dict(**identity,proof=data.get('proof',{})))
        for m in CONTROLS:controls.append(dict(**identity,method=m,scores=base_scores[m],analysis_status='post-result / exploratory'))
        for m,r in combos.items():
            row=dict(**identity,method=m,status=r['status'],reason=r.get('reason'),identity=r.get('identity'),analysis_status='post-result / exploratory')
            if r['status']=='COMPLETE':
                row['scores']=inf.summarize_scores(peak,r['capacity'],tau=.95,origins=ids,horizon=h)
                losses[m]=inf.pinball_losses(peak,r['capacity'],tau=.95)
                row['percent_vs_F']=100*(row['scores']['mean_loss']/base_scores['F']['mean_loss']-1) if base_scores['F']['mean_loss'] else None
                row['percent_vs_QR']=100*(row['scores']['mean_loss']/base_scores['QR']['mean_loss']-1) if base_scores['QR']['mean_loss'] else None
            rows.append(row)
            for control in CONTROLS:
                slot=cell['cell_id']+':'+m+'-minus-'+control
                z=dict(**identity,slot_id=slot,left_method=m,right_method=control,tau=.95,status='NA_CELL',raw_p=None,mean_difference=None,direction='new_minus_control')
                if r['status']=='COMPLETE':
                    z.update(inf.compare_losses(losses[m],losses[control],horizon=h));z['raw_p']=z.get('dm_p') if z['status']=='OK' else None
                comparisons.append(z)
                if cell.get('murphy_context'):
                    if r['status']!='COMPLETE':murphy.append(dict(**identity,slot_id=slot,status='NA',reason=r.get('reason')));continue
                    diagram=murphy_exact(r['capacity'],data[control],peak,tau=.95)
                    scalar={k:v for k,v in diagram.items() if not isinstance(v,np.ndarray)}
                    scale=max(1.,row['scores']['mean_loss'],base_scores[control]['mean_loss'])
                    if abs(diagram['integral_minus_pinball'])>1e-9*scale:raise ValueError('MURPHY_INTEGRAL_IDENTITY')
                    murphy.append(dict(**identity,slot_id=slot,status='COMPLETE',left_method=m,right_method=control,reference_scope='Matched constituents in original-primary source/H/W context; original FX rolling-F primary is distinct',**scalar))
                    curves[slot]={k:v for k,v in diagram.items() if isinstance(v,np.ndarray)}
    slots=[r['slot_id'] for r in comparisons]
    holm=inf.fixed_slot_holm(slots,{r['slot_id']:r['raw_p'] for r in comparisons})
    for r,z in zip(comparisons,holm['slots']):r.update(bookkeeping_p=z['bookkeeping_p'],holm_p=z['holm_p'],holm_component_status=z['status'])
    return dict(status='COMPLETE_WITH_NA',analysis_status='post-result / exploratory',tau=.95,cell_count=56,
        method_row_count=len(rows),complete_method_count=sum(r['status']=='COMPLETE' for r in rows),na_method_count=sum(r['status']=='NA' for r in rows),
        method_rows=rows,control_rows=controls,comparisons=comparisons,family_n=224,raw_na_count=holm['raw_na_count'],
        input_proofs=input_proofs,murphy= murphy,
        note='Untuned combinations, no conditional quantile or coverage guarantee; normal-DM Holm family224, HLN unadjusted, overlapping/dependent inspected records.'),curves

def cells_from(spec,inventory):
    cells=[]
    for source,cfg in spec['sources'].items():
        for h in spec['horizons']:
            for w in cfg['windows']:
                cells.append(dict(cell_id=f'{source}:H{h}:W{w}',source=source,horizon=h,window=w,
                    native_unit=cfg['native_unit'],original=True,murphy_context=h==6 and w==cfg['primary_window']))
    for entry in inventory['panel_cells']:
        s=entry['series_key'];h=entry['horizon'];w=entry['window']
        cells.append(dict(cell_id=f'{s}:H{h}:W{w}',source=s,horizon=h,window=w,native_unit='USD millions',original=False,murphy_context=False))
    if len(cells)!=56 or len({r['cell_id'] for r in cells})!=56:raise ValueError('CELL_INVENTORY')
    return cells

def main():
    import v6_worker as w
    from v6_panel_admission import load_panel_cell
    freeze=w.read_json(w.ROOT/'protocol/revision-v6/wp3-executable-freeze.json')
    for p,digest in freeze['files'].items():
        if w.sha(w.ROOT/p)!=digest:raise ValueError('WP3_EXECUTABLE_CHANGED:'+p)
    w.check_execution_freeze();guard=w.Guard();guard()
    spec=w.read_json(w.ROOT/w.SPEC);inventory=w.read_json(w.PRIVATE/'input-inventory.json');cells=cells_from(spec,inventory)
    if [c['cell_id']+':'+m+'-minus-'+b for c in cells for m in METHODS for b in CONTROLS]!=freeze['contrast_slots']:raise ValueError('FROZEN_CONTRAST_IDENTITY')
    entries={(e['series_key'],e['horizon'],e['window']):e for e in inventory['panel_cells']}
    def loader(cell):
        guard();s,h,win=(cell[k] for k in ('source','horizon','window'))
        if not cell['original']:return load_panel_cell(entries[(s,h,win)],root=w.ROOT)
        bundle={m:w.original_trace(s,h,win,'references' if m=='frozen_F' else 'evaluation',m) for m in ('frozen_F','QR','KNN')}
        ref=bundle['frozen_F']
        for r in bundle.values():
            if not all(np.array_equal(r[k],ref[k]) for k in ('origins','peak','floor')):raise ValueError('ORIGINAL_CONSTITUENT_IDENTITY')
        return dict(origins=ref['origins'],peak=ref['peak'],floor=ref['floor'],F=ref['capacity'],QR=bundle['QR']['capacity'],KNN=bundle['KNN']['capacity'],
            proof=dict(trace_sha256={m:r['trace_sha256'] for m,r in bundle.items()},source_sha256=spec['sources'][s]['sha256'],native_unit=cell['native_unit']))
    report,curves=aggregate(cells,loader);guard()
    if len(report['murphy'])!=8:raise ValueError('MURPHY_INVENTORY')
    private={f'curve{j}_{k}':v for j,data in enumerate(curves.values()) for k,v in data.items()}
    proof=w.save_private(w.PRIVATE/'wp3-murphy-curves.npz',**private)
    report['private_curve_artifact']=proof;report['curve_order']=list(curves)
    report['execution_freeze_sha256']=w.sha(w.ROOT/'protocol/revision-v6/wp3-executable-freeze.json')
    report['resources']=guard.summary()
    w.write_json_new(w.PUBLIC/'wp3-combinations.json',report)
    print(json.dumps({k:report[k] for k in ('status','cell_count','method_row_count','complete_method_count','na_method_count','family_n','raw_na_count','resources')}))

if __name__=='__main__':main()
