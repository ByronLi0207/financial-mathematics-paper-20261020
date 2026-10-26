"""Bind existing archived scalars and the exact new frozen backcast output.

No model/selection or old-period inference runs here. Missing old fields remain
NA; a normalised display table does not reclassify five-menu R0 as QR33.
"""
import csv
from datetime import datetime,timezone
import hashlib
import io
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
BASE=ROOT/'results/revision-v8/wp5'
BINDS=[]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_row(path,selector):
    p=ROOT/path
    rows=list(csv.DictReader(p.open()))
    found=[(i+2,r) for i,r in enumerate(rows) if all(r.get(k)==v for k,v in selector.items())]
    if len(found)!=1:raise ValueError(f'Expected unique archive row: {path} {selector}')
    line,r=found[0]
    b=dict(path=path,line=line,selector=selector,sha256=sha(p),copied_row=r)
    BINDS.append(b)
    return r


def write(name,text):
    with (BASE/name).open('x') as out:out.write(text)


def old_rows():
    rows=[]
    retro_path='results/supervisor-20261023/r6-writing-hac-20261023/comparisons.csv'
    retro_base=dict(source='fx_hourly',horizon='6',window='2880')
    qr=source_row('results/supervisor-20261023/r6/retro-summary.csv',dict(retro_base,report='R0'))
    f=source_row('results/supervisor-20261023/r6/retro-summary.csv',dict(retro_base,report='F'))
    for reference,name in [('F_matched','matched_frozen_F2880_d24'),('F_rolling720','original_primary_rolling_F720_d1')]:
        c=source_row(retro_path,dict(comparison=name,source='fx_hourly',horizon='6'))
        # The public primary provenance identifies original3-menu == R0 forH6;
        # exact trace identity, not model-name resemblance, permits breach reuse.
        if c['conditional_report']!='QR_original_three_menu_also_R0_NOT_R2':raise ValueError('wrong original menu')
        if qr['trace_sha256']!=c['QR_trace_sha256']:raise ValueError('retro QR trace identity')
        if reference=='F_matched' and f['trace_sha256']!=c['F_trace_sha256']:raise ValueError('retro F identity')
        rows.append(dict(window_name='previous_retro',method='QR33',horizon=6,reference=reference,
            status='COMPLETE' if c['status']=='OK' else c['status'],n=int(c['n']),
            issue_first=int(c['origin_first']),issue_last=int(c['origin_last']),
            model_mean_loss=float(c['QR_mean_loss']),reference_mean_loss=float(c['F_mean_loss']),
            relative_change_percent=float(c['ratio_change_percent']),model_breaches=int(qr['strict_breach_count']),
            reference_breaches=int(f['strict_breach_count']) if reference=='F_matched' else None,
            missing_reason=None if reference=='F_matched' else 'No archived public rolling breach count in original primary comparison; not recalculated',
            dm=dict(status=c['status'],n=int(c['n']),horizon=6,bandwidth=int(c['L']),
                mean_difference=float(c['mean_loss_difference_QR_minus_F']),lrv=float(c['raw_LRV']),
                dm_t=float(c['HAC_statistic']),dm_p=float(c['two_sided_normal_HAC_p'])),
            original_primary_procedure='Original3-menu H6 selection, shown by source selector and exact trace; not a newly retuned procedure'))
    table='results/revision-20261022/evaluation-summary.csv'
    ident=dict(source='fx_hourly',horizon='6')
    qr=source_row(table,dict(ident,window='2880',method='QR'))
    for reference,method,w in [('F_matched','frozen_F','2880'),('F_rolling720','rolling_F','720')]:
        f=source_row(table,dict(ident,window=w,method=method))
        c=source_row('results/supervisor-20261023/inference/dm-verified.csv',dict(
            source='fx_hourly',horizon='6',left_method='QR',left_window='2880',right_method=method,right_window=w))
        a,b=float(qr['mean_pinball']),float(f['mean_pinball'])
        rows.append(dict(window_name='original_inspected',method='QR33',horizon=6,reference=reference,
            status='COMPLETE' if c['status']=='OK' else c['status'],n=int(qr['origin_count']),
            issue_first=11927,issue_last=18551,model_mean_loss=a,reference_mean_loss=b,
            relative_change_percent=100*(a/b-1),model_breaches=int(qr['strict_breach_count']),
            reference_breaches=int(f['strict_breach_count']),missing_reason=None,
            dm={key:(int(c[key]) if key in ('n','horizon','bandwidth') else c[key] if key=='status' else float(c[key]))
                for key in ('status','n','horizon','bandwidth','mean_difference','lrv','dm_t','dm_p')},
            original_primary_procedure='Archived original3-menu selected procedure; source values unchanged'))
    return rows



def full_tables(summary):
    """Display all eight new comparisons, including any unavailable result."""
    md=['# Complete fixed-prefix backcast comparisons', '',
        'All declared H6/H24 comparisons on3071–10438 are retained. This is an inspected post-result window with later-selected parameters. Negative percentage changes favour regression; p-values are raw descriptive normal-HAC values. SourceJSON/CSV retains full precision; no old missing test is calculated.', '',
        '| Horizon | Regression | Reference | Status | Mean loss QR / F (USD) | Change % | Breaches QR / F | DM | Raw p |',
        '|---:|---|---|---|---:|---:|---:|---:|---:|']
    tex=[r'\begingroup\small\setlength{\tabcolsep}{3pt}',r'\begin{longtable}{rllrrrr}',
        r'\caption{Complete full-prefix backcast comparisons. The two regressions use the original later-selected parameters. All planned comparisons are shown; raw normal-HAC p-values are descriptive. The window is already inspected and overlaps the earlier reported backcast.}\label{tab:v8-backcast-complete}\\',
        r'\toprule',r'Horizon & Regression & Reference & \shortstack{Mean loss\\QR / F (USD m)} & \shortstack{Change\\(\%)} & \shortstack{Breaches\\QR / F} & \shortstack{DM\\(raw $p$)}\\\midrule',r'\endfirsthead',r'\caption[]{Continued.}\\\toprule',
        r'Horizon & Regression & Reference & \shortstack{Mean loss\\QR / F (USD m)} & \shortstack{Change\\(\%)} & \shortstack{Breaches\\QR / F} & \shortstack{DM\\(raw $p$)}\\\midrule',r'\endhead',r'\bottomrule\endfoot']
    f=lambda v,n=3:'NA' if v is None else f'{v:.{n}f}'
    for c in summary['contrasts']:
        dm=c.get('dm') or {};a,b=c.get('model_mean_loss'),c.get('reference_mean_loss')
        loss='NA' if a is None or b is None else f'{a/1e6:.3f} / {b/1e6:.3f}'
        counts='NA' if c.get('model_breaches') is None or c.get('reference_breaches') is None else f"{c['model_breaches']} / {c['reference_breaches']}"
        model={'QR33':'33-feature','QR4':'Four-feature'}[c['method']]
        ref={'F_matched':'Matched F2880','F_rolling720':'Rolling F720'}[c['reference']]
        pv='NA' if dm.get('dm_p') is None else '<0.001' if dm['dm_p']<.001 else f"{dm['dm_p']:.3f}"
        md.append('| '+' | '.join([str(c['horizon']),model,ref,c['status'],f'{a} / {b}',f(c.get('relative_change_percent'),6),counts,f(dm.get('dm_t'),6),repr(dm.get('dm_p'))])+' |')
        tex.append(' & '.join([str(c['horizon']),model,ref,loss,f(c.get('relative_change_percent')),counts,f"{f(dm.get('dm_t'))} ({pv})"])+r'\\')
    tex += [r'\end{longtable}',r'\endgroup','']
    write('FULL_BACKCAST_RESULTS.md','\n'.join(md)+'\n')
    write('backcast-complete-table.tex','\n'.join(tex))


def main():
    from v8_backcast import classify_three_windows
    summary=json.loads((BASE/'summary.json').read_text())
    audit=json.loads((ROOT/'notes/revision-v8/wp5-independent-audit.json').read_text())
    if audit['status']!='PASS' or audit['difference_count']!=0:raise ValueError('independent audit required')
    old=old_rows()
    print('Old archived comparison rows bound:',len(old))
    new=[]
    for index,c in enumerate(summary['contrasts']):
        if c['horizon']==6 and c['method']=='QR33':
            new.append(dict(c,source_contrast_index=index,window_name='extra_full_prefix',issue_first=3071,issue_last=10438,
                n=7368,missing_reason=None,original_primary_procedure='Frozen original later-selected parameters; no backcast tuning'))
    if len(new)!=2:raise ValueError('two fixed new H6 comparisons required')
    rows=new+old
    screen=classify_three_windows(rows,json.loads((ROOT/'protocol/revision-v8/wp5-fixed-prefix-design.json').read_text()))
    binding=dict(generated_utc=datetime.now(timezone.utc).isoformat(),generator_sha256=sha(Path(__file__)),old_source_bindings=BINDS,
        new_summary_sha256=sha(BASE/'summary.json'),new_audit_sha256=sha(ROOT/'notes/revision-v8/wp5-independent-audit.json'),
        original_archived_fields_modified=False,old_missing_DM_or_breaches_recomputed=False,
        independence_claim='FAIL/MISMATCH-WP5-01: all extra-prefix H24 target paths already scored; previous retro1440 origins fully nested',
        screen=screen)
    write('three-window-bindings.json',json.dumps(binding,indent=2)+'\n')
    write('three-window-summary.json',json.dumps(dict(rows=rows,screen=screen),indent=2)+'\n')
    fields=['window_name','method','horizon','reference','status','n','issue_first','issue_last','model_mean_loss','reference_mean_loss','relative_change_percent','model_breaches','reference_breaches','dm_t','dm_p','bandwidth','missing_reason']
    buf=io.StringIO();writer=csv.DictWriter(buf,fieldnames=fields);writer.writeheader()
    for r in rows:
        flat={k:r.get(k) for k in fields}
        flat.update({k:r['dm'].get(k) if r.get('dm') else None for k in ['dm_t','dm_p','bandwidth']})
        writer.writerow(flat)
    write('three-window-summary.csv',buf.getvalue())
    names={'extra_full_prefix':'Full-prefix backcast','previous_retro':'Earlier reported backcast','original_inspected':'Original inspected evaluation'}
    refs={'F_matched':'Matched F2880','F_rolling720':'Rolling F720'}
    fmt=lambda v,places=3:'NA' if v is None else f'{v:.{places}f}'
    md=['# Three overlapping/inspected evaluation windows: H6 original QR', '',
        'The full-prefix window contains all1440 earlier backcast origins; earlier R3 scoring already covered itsH24 target paths. These are **not three disjoint or independent validation periods**. Parameters for the extra prefix were chosen later. Negative loss changes favour QR. Raw normal-HAC p-values remain post-result/descriptive.', '',
        '| Window | Reference | Issues | QR mean loss (USD) | Reference mean loss (USD) | Change % | QR breaches | Reference breaches | DM | Raw p |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    tex=[r'\begingroup\small\setlength{\tabcolsep}{3pt}',r'\begin{longtable}{llrrrrrr}',
         r'\caption{H6 original regression across three inspected windows. The full-prefix window contains the earlier reported backcast, so this is not independent validation. Loss is scaled to USD millions for display; raw normal-HAC p-values are descriptive. Missing archived breach counts remain NA.}\label{tab:v8-backcast}\\',r'\toprule',
         r'Window & Reference & \shortstack{Mean loss\\QR / F (USD m)} & \shortstack{Change\\(\%)} & \shortstack{Breaches\\QR / F} & DM & Raw $p$ & Issues\\\midrule',r'\endfirsthead',r'\caption[]{Continued.}\\\toprule',
         r'Window & Reference & \shortstack{Mean loss\\QR / F (USD m)} & \shortstack{Change\\(\%)} & \shortstack{Breaches\\QR / F} & DM & Raw $p$ & Issues\\\midrule',r'\endhead',r'\bottomrule\endfoot']
    for r in rows:
        dm=r.get('dm') or {};hits='NA' if r.get('reference_breaches') is None else str(r['reference_breaches'])
        md.append('| '+' | '.join([names[r['window_name']],refs[r['reference']],str(r['n']),repr(r.get('model_mean_loss')),repr(r.get('reference_mean_loss')),fmt(r.get('relative_change_percent'),6),str(r.get('model_breaches')),hits,fmt(dm.get('dm_t'),6),repr(dm.get('dm_p'))])+' |')
        loss='NA' if r.get('model_mean_loss') is None else f"{r['model_mean_loss']/1e6:.3f} / {r['reference_mean_loss']/1e6:.3f}"
        pv='NA' if dm.get('dm_p') is None else ('<0.001' if dm['dm_p']<.001 else f"{dm['dm_p']:.3f}")
        short={'extra_full_prefix':'Full prefix','previous_retro':'Prior backcast','original_inspected':'Original'}[r['window_name']]
        tex.append(' & '.join([short,refs[r['reference']],loss,fmt(r.get('relative_change_percent')),f"{r.get('model_breaches')} / {hits}",fmt(dm.get('dm_t')),pv,str(r['n'])])+r'\\')
    tex += [r'\end{longtable}',r'\endgroup','']
    write('THREE_WINDOWS.md','\n'.join(md)+'\n')
    write('three-window-table.tex','\n'.join(tex))
    full_tables(summary)
    write('README.md','''# WP5 fixed-parameter full-prefix backcast

The frozen design is467a995 (`protocol/revision-v8/wp5-fixed-prefix-design.*`). This extension evaluates the prescribed full eligible prefix, without new tuning or moving endpoints. The design explicitly rejects its false training-only/never-scored premise.

`summary.json` and the driver receipts retain every declared new procedure and reference comparison, including failures. `three-window-summary.*` binds the two exact existing H6 QR33 comparisons per old window and the new ones. Missing old H24 original-three-menu, QR4 and rolling DM results are not filled by extra computations; old five-menu R0 never substitutes for original QR33. Complete original archives remain unchanged.

The normal-HAC p-values are raw, post-result and descriptive. Overlap, past inspection, later parameter choice and serial dependence prevent treating this as fresh independent validation, a real-time backtest, or three independent replications. A lower pinball loss is not a guarantee of a safe limit or nominal conditional coverage. All raw positions and per-issue numerical traces stay private under task scratch; public artifacts contain aggregate results and fingerprints only.

See `THREE_WINDOWS.md`, the source-field bindings and independent numerical audit before using a table value. No missing old test was recomputed.
''')
    print(json.dumps(dict(three_window_rows=len(rows),old_source_rows=len(BINDS),screen=screen,old_missing_inference_recomputed=False)))

if __name__=='__main__':main()
