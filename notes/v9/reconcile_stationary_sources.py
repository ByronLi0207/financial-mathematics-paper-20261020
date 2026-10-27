"""Existing stationary outputs only: resolve the task's contradicted premise."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('legacy_directory',type=Path);a=p.parse_args()
    root=Path(__file__).resolve().parents[2]
    current=root/'results/revision-v8/wp3/summary.json'
    legacy=a.legacy_directory/'results/v8/mc/summary.json'
    settings=a.legacy_directory/'results/v8/mc/experiment-settings.json'
    files={str(v):v.read_bytes() for v in [current,legacy,settings]}
    wp3=json.loads(files[str(current)])['cells'];old=json.loads(files[str(legacy)])
    groups=[]
    for method in ('QR33','QR4'):
        for w in (52,260):
            selected=[r for r in wp3 if r['method']==method and r['window']==w and r['horizon']==6]
            assert len(selected)==9 and all(r['full_procedure_status']=='COMPLETE' for r in selected)
            values=[r['relative_loss_percent'] for r in selected]
            groups.append(dict(source='PR5 WP3',method=method,window=w,horizon=6,
                estimand='ratio of mean losses across repetitions',n_settings=len(selected),
                minimum_pct=min(values),maximum_pct=max(values),
                rows=[{k:r[k] for k in ('phi','variance_persistence','window','horizon','method','relative_loss_percent')} for r in selected]))
    old52=[r for r in old if r['dgp'] in ('D0','D2') and r['window']==52 and r['features']==33]
    assert len(old52)==2
    result=dict(purpose='Correct the task premise by reading frozen outputs; no experiment or fit.',
        source_sha256={name:hashlib.sha256(raw).hexdigest() for name,raw in files.items()},
        pr5_groups=groups,legacy_W52_QR33=old52,legacy_settings=json.loads(files[str(settings)]),
        conclusion='PR5 already has large stationary short-history losses. Legacy D0/D2 parity is specific to a different menu/clock/geometry/calibration/estimand. Neither grid establishes a universal sample-size or instability mechanism.')
    directory=root/'results/v9/nonstationarity'
    with (directory/'prior-stationary-reconciliation.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    lines=['# Frozen stationary grids: premise correction','',
        'No result was changed or recomputed by a forecasting procedure. All values below are read from the archived summaries.','',
        '| Source | Method | W/H | Summary | Relative loss (%) |','|---|---|---|---|---|']
    for r in groups:lines.append(f"|PR5 WP3|{r['method']}|{r['window']}/6|ratio of means|{r['minimum_pct']:+.4f} to {r['maximum_pct']:+.4f}|")
    for r in old52:lines.append(f"|legacy {r['dgp']}|QR33|52/6|median of repetition ratios|{r['qr_median_pct']:+.6f}|")
    lines+=['','The legacy design includes the intercept-only limit, has 100 repetitions and 500 evaluation origins, and uses weekly RMS6/26 and refit13 for D0/D2. WP3 uses three QR33 penalties, 32 repetitions, 72 evaluation origins, RMS24/168 and refit24. The numerical summaries also differ. These are not interchangeable controls.','',result['conclusion']]
    with (directory/'prior-stationary-reconciliation.md').open('x') as f:f.write('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
