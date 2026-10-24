"""Generate presentation quantities solely from the frozen aggregate WP2 files."""
import json,hashlib
from pathlib import Path

def build(summary,comparisons,phase_receipts):
    rows=summary['method_rows']+summary['control_rows'];out=[]
    for source,h,w in [(s,h,w) for s,h,w in dict.fromkeys((r['source'],r['horizon'],r['window']) for r in summary['method_rows'])]:
        local={r['method']:r for r in rows if (r['source'],r['horizon'],r['window'])==(source,h,w)}
        if local['ACI_QR']['status']=='COMPLETE' and local['ACI_F']['status']=='COMPLETE':
            q,f=(local[k]['scores'] for k in ('ACI_QR','ACI_F'))
            out.append(dict(source=source,horizon=h,window=w,status='COMPLETE',
                qr_minus_f_loss_percent=100*(q['mean_loss']/f['mean_loss']-1),
                qr_mean_loss=q['mean_loss'],f_mean_loss=f['mean_loss'],
                qr_hits=q['full_hits'],f_hits=f['full_hits'],n=q['n'],
                qr_rate=q['full_rate'],f_rate=f['full_rate'],
                qr_coverage_distance=q['coverage_distance'],f_coverage_distance=f['coverage_distance']))
        else:out.append(dict(source=source,horizon=h,window=w,status='NA',reason='DECLARED_WRAPPED_PAIR_UNAVAILABLE'))
    resources=dict(canonical_phase_receipt_count=len(phase_receipts),complete_phase_count=sum(r['status']=='COMPLETE' for r in phase_receipts),
        na_phase_count=sum(r['status']=='NA' for r in phase_receipts),
        peak_rss_bytes=max(r['resources']['peak_rss_bytes'] for r in phase_receipts),
        maximum_worker_seconds=max(r['resources']['elapsed_seconds'] for r in phase_receipts),
        maximum_observed_os_threads=max(r['resources']['maximum_observed_os_threads'] for r in phase_receipts))
    return dict(status='COMPLETE',analysis_status='post-result / exploratory',wrapped_pairs=out,resources=resources,
        method_inventory={m:dict(complete=sum(r['method']==m and r['status']=='COMPLETE' for r in summary['method_rows']),na=sum(r['method']==m and r['status']!='COMPLETE' for r in summary['method_rows'])) for m in ('ACI_F','ACI_QR','SAV')},
        family_n=comparisons['family_n'],raw_na_count=comparisons['raw_na_count'])

def main():
    root=Path(__file__).resolve().parent;p=root/'results/revision-20261023/v6'
    inputs={name:json.loads((p/name).read_text()) for name in ('wp2-summary.json','wp2-comparisons.json')}
    receipts=[json.loads(f.read_text()) for f in sorted((p/'wp2').glob('*.json'))]
    z=build(inputs['wp2-summary.json'],inputs['wp2-comparisons.json'],receipts)
    z['input_sha256']={name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in inputs}
    with (p/'wp2-findings.json').open('x') as f:json.dump(z,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(z,indent=2))
if __name__=='__main__':main()
