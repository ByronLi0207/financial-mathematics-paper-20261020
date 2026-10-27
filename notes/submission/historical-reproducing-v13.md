# Reproducing revision-v13

The editable submission is `submission-v10/` on `revision-v13`. This recipe
re-estimates existing comparisons without changing model code, menus, targets,
evaluation periods, or saved results. It was added after G4's initial clean-clone
check found that the previous version-specific notes lacked executable raw-data
re-estimation steps. The initial check is `notes/v13/G4-initial-check.json`;
the completed check, once run, is `notes/v13/independent-reproduction.md`.

## 1. Obtain a clean checkout

Clone the desired v13 commit into a new directory. For a not-yet-published local
commit, `git clone --no-local --no-hardlinks --single-branch --branch revision-v13
<source-repository> <new-directory>` provides an independent object database.
For the published version use the GitHub repository URL instead. Record
`git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, and an initially empty
`git status --porcelain`. Run the following commands from that fresh checkout.
Do not copy any prior `.scratch/`, fitted models, prediction traces, caches, or
prepared CFTC `sources/*.npz` into it.

Do not run old prose builders: they overwrite subsequent manual editing. Old
one-shot experiment drivers intentionally target their original saved output
paths and require original historical design commits. This recipe calls their
unchanged source-independent helpers into a new output directory; it does not
remove or weaken those guards. Historical full-suite Git-object prerequisites
are separate from this scientific re-estimation check.

## 2. Supply pinned original raw inputs

The eleven original CFTC ZIPs and the Treasury-bill CSV are already versioned.
No download is needed. CFTC raw bytes are checked against
`data/cftc-tff/provenance.json` before parsing. The panel's original raw CSV and
the private FX original CSV are not redistributed in this repository. Supply
only these two raw files; their saved numerical forecasts cannot substitute:

- `V13_PANEL_RAW`: PDPOSCS-TOT CSV, 24,713 bytes, SHA-256
  `169fdb5201f6a34152936f0aa2b444d9ea0f8814d39750bfd4a4bc942a41fade`.
  The source contains 707 dates; the unchanged alignment helper selects the
  original 706-date Treasury-bill grid, without filling missing dates.
- `V13_FX_RAW`: original hourly FX CSV, 1,286,391 bytes, SHA-256
  `b8e92c54a76b49990b028252d6a89195e92193990e72f10228f2280a11a967fa`.
  This check verifies the raw input's identity but does not run an additional
  FX comparison.

For the author's already downloaded raw copies on the task machine:

```bash
export V13_PANEL_RAW='/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/panel/PDPOSCS-TOT.csv'
export V13_FX_RAW='/Users/bingyouli/Research/论文/金融数学论文-v9-20261024/.scratch/v9/inputs/1hourNetPositionsKaggle.csv'
export V13_REPRO_OUTPUT="$PWD/.scratch/v13-independent-check"
```

Use a new `V13_REPRO_OUTPUT` every time; an existing directory is rejected.
Missing raw bytes mean that part cannot be reproduced offline. Do not download
replacement vintages or substitute a processed vector to make the check pass.

## 3. Run the check in a temporary environment

Use uv, not a system-Python installation. The following command uses the task
machine's existing Python and Tectonic binaries. On another machine point
`V13_TECTONIC` at its existing Tectonic executable and use an equivalent Python
3.12 interpreter. All numerical thread variables are set before NumPy import.
No scientific Python module in the repository is edited by this command.

The task referred to the CFTC contract display as Table 5. In the current v13 manuscript it is Table 6 (`tab:v10-cftc-contracts`, `submission-v10/generated/v10-cftc-contracts.tex`); the tested command identifies this source file rather than relying on the printed number.

The CFTC table prints 170 relative percentages: 17 contracts × two histories ×
five non-reference columns. Its corrected historical reference must also be
re-estimated, giving 204 method cells. All CFTC regressions here use the original
six-point menu. The original bill primary and original panel full regression
instead use three penalties; the panel's four-feature regression uses five.

```bash
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pypdf python -B - <<'PY_REPRO'
from pathlib import Path
import os, json, hashlib, re, csv, io, time, datetime, subprocess, math
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS',
             'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','NUMBA_NUM_THREADS'):
    os.environ[name] = '1'
import numpy as np
from pypdf import PdfReader
from v10_cftc_data import read_archive, select_universe
from v10_cftc_forecast import forecast_cell
from v10_cftc_summary import summarize
from conditional_sources import load_source
from conditional_study import (StudyConfig, conditional_forecast, score_predictions,
                               summarize_scores, select_parameter, historical_forecasts)
from conditional_quantile import QuantileFitError
from study_core import build_label_cache, stable_mean
from round2_panel_sources import align_source
from round2_levy import predict as endpoint_predict
from parsimonious_v3 import features4, forecast as four_forecast
from run_study import StudyStop

root = Path.cwd()
out = Path(os.environ['V13_REPRO_OUTPUT']).absolute()
assert not out.exists(), 'Choose a new empty reproduction output directory'
out.mkdir(parents=True)
started = time.monotonic()
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda raw: hashlib.sha256(raw).hexdigest()
load = lambda rel: json.loads((root/rel).read_text())
def save(name, value):
    with (out/name).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False, default=dict)
        stream.write('\n')
def protocol(rel):
    return json.loads(re.search(r'```json\n(.*?)\n```', (root/rel).read_text(), re.S)[1])
def raw_pin(path, count, digest):
    path = Path(path)
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes()
    assert len(raw) == count and sha(raw) == digest, str(path)
    return raw
checks = []
def compare(path, actual, expected):
    numeric = isinstance(expected,(int,float)) and not isinstance(expected,bool)
    valid_actual = (isinstance(actual,(int,float,np.number)) and
                    not isinstance(actual,(bool,np.bool_)) and math.isfinite(float(actual)))
    equal = bool(actual == expected) if not numeric or valid_actual else False
    checks.append(dict(path=path,actual=actual,expected=expected,equal=equal,
        numeric_expected=numeric,
        absolute_difference=abs(float(actual)-expected) if numeric and valid_actual else None))
def compare_scores(prefix, actual, expected):
    for key, value in actual.items():
        if key in expected: compare(prefix+'/'+key, value, expected[key])
def checkpoint(**detail):
    if time.monotonic()-started > 3600:
        raise StudyStop('G4_REPRODUCTION_WALL_LIMIT')
identity = dict(started_utc=utc(),head=subprocess.check_output(
    ['git','rev-parse','HEAD'],text=True).strip(),tree=subprocess.check_output(
    ['git','rev-parse','HEAD^{tree}'],text=True).strip(),numpy=np.__version__,
    input_rule='Raw ZIP/CSV only; no prior intermediate predictions or prepared CFTC NPZ')
save('start.json',identity)
spec = load('protocol/revision-20261022/study-spec.json')
fx = spec['sources']['fx_hourly']
raw_pin(os.environ['V13_FX_RAW'],fx['bytes'],fx['sha256'])
panel_source = load('results/revision-20261023/round2/panel/sources/PDPOSCS-TOT/provenance.json')
panel_raw = raw_pin(os.environ['V13_PANEL_RAW'],panel_source['bytes'],panel_source['sha256'])
save('external-raw-inputs.json',dict(FX=dict(path=os.environ['V13_FX_RAW'],bytes=fx['bytes'],sha256=fx['sha256'],forecast_run=False),panel=dict(path=os.environ['V13_PANEL_RAW'],bytes=panel_source['bytes'],sha256=panel_source['sha256'],kind='original CSV, not derived intermediate')))

# Compile the clone's native source, never its saved PDF.
t = time.monotonic(); native = out/'native'; native.mkdir()
tectonic = os.environ.get('V13_TECTONIC','/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic')
cmd = [tectonic,'-X','compile',str(root/'submission-v10/main.tex'),
       '--outdir',str(native),'--keep-logs','--keep-intermediates']
p = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(native/'console.txt').write_text(p.stdout)
assert p.returncode == 0, p.stdout
log = (native/'main.log').read_text()
bad = re.findall(r'Overfull[^\n]*|(?:Reference|Citation)[^\n]*undefined|Label[^\n]*multiply defined',log)
assert not bad, bad
save('native-compile.json',dict(command=cmd,elapsed_seconds=time.monotonic()-t,
    pages=len(PdfReader(native/'main.pdf').pages),returncode=p.returncode,
    pdf_sha256=sha((native/'main.pdf').read_bytes()),source_compiled=True,
    no_overfull_or_unresolved_or_duplicate_labels=True))

# Rebuild CFTC arrays from every original raw ZIP, with both original parser clarifications.
t = time.monotonic(); design = protocol('protocol/v10/cftc-design.md')
design['ingestion_clarification'] = protocol('protocol/v10/cftc-ingestion-clarification.md')
design['count_notation_clarification'] = protocol('protocol/v10/cftc-count-notation-clarification.md')
provenance = load('data/cftc-tff/provenance.json')
all_rows, source_checks = [], []
assert len(design['downloads_in_fixed_order']) == len(provenance['files']) == 11
for owner, entry in zip(design['downloads_in_fixed_order'],provenance['files']):
    assert owner['url'] == entry['url']
    raw = raw_pin(root/entry['local_path'],entry['bytes'],entry['sha256'])
    parsed, audit = read_archive(raw,owner,design)
    all_rows.extend(parsed)
    source_checks.append(dict(path=entry['local_path'],bytes=len(raw),sha256=sha(raw),
                             parsed_rows=len(parsed),ownership_excluded=audit['ownership_excluded_count']))
assert len(source_checks) == 11
universe = select_universe(all_rows,design)
expected_codes = [row['code'] for row in load('results/v10/cftc/sources.json')]
assert universe['selected'] == expected_codes and len(expected_codes) == 17
save('raw-cftc-ingestion.json',dict(sources=source_checks,codes=expected_codes,N=universe['N'],
    elapsed_seconds=time.monotonic()-t,prepared_NPZ_read=False))
records = []; formal_started = utc(); formal_clock = time.monotonic()
for code in expected_codes:
    arrays = universe['arrays_by_code'][code]
    for window in (52,260):
        checkpoint()
        result = forecast_cell(np.asarray(arrays['position'],dtype=float),
            np.asarray(arrays['model_dates'],dtype='datetime64[us]'),design,window,
            out/'cftc'/code/f'W{window}',checkpoint=checkpoint)
        records.extend(dict(row,code=code,window=window) for row in result['methods'])
        print('CFTC',code,window,[(row['method'],row['status'])for row in result['methods']],flush=True)
recomputed = summarize(records,expected_codes,design)
save('cftc-recomputed.json',recomputed)
old = load('results/v10/cftc/summary.json')
assert len(recomputed['cells']) == len(old['cells']) == 204
cell_id = lambda row: (row['code'],row['window'],row['method'])
actual_cells = {cell_id(row):row for row in recomputed['cells']}
expected_cells = {cell_id(row):row for row in old['cells']}
assert len(actual_cells) == len(expected_cells) == 204
assert set(actual_cells) == set(expected_cells)
for identity_key, expected in expected_cells.items():
    actual = actual_cells[identity_key]
    prefix=f"CFTC/{actual['code']}/W{actual['window']}/{actual['method']}"
    for key in ('status','n','mean_loss','strict_breach_count','strict_breach_rate',
                'selected_penalty','selected_gamma','relative_loss_pct'):
        compare(prefix+'/'+key,actual[key],expected[key])
index = {(row['code'],row['window'],row['method']):row for row in recomputed['cells']}
printed = []
tex = (root/'submission-v10/generated/v10-cftc-contracts.tex').read_text()
for code in expected_codes:
    line = next(line for line in tex.splitlines() if line.startswith(code+' & '))
    fields = [field.strip() for field in line.split('&')][1:]
    fields[-1] = fields[-1].rstrip(chr(92)).strip()
    assert len(fields) == 20
    expected_text = [fields[i]+'.'+fields[i+1] for i in range(0,20,2)]
    identities = [(w,m) for w in (52,260) for m in ('I','QR4','QR33','ACI_F','ACI_QR33')]
    for (window,method),display in zip(identities,expected_text):
        actual = format(index[code,window,method]['relative_loss_pct'],'.2f')
        printed.append(dict(code=code,window=window,method=method,actual=actual,expected=display,equal=actual==display))
assert len(printed) == 170
save('cftc-printed-comparison.json',dict(cells=printed,all_equal=all(row['equal']for row in printed)))
save('cftc-timing.json',dict(started_utc=formal_started,elapsed_seconds=time.monotonic()-formal_clock,
                           required_method_cells=204,complete_method_cells=sum(row['status']=='COMPLETE'for row in recomputed['cells'])))

# Original bill and chosen panel cell: original menus and original scoring arithmetic.
val = np.arange(329,381,dtype=np.int64); ev = np.arange(405,682,dtype=np.int64)
def original_cell(x,dates,window,include_panel_methods=False):
    cfg = StudyConfig(6,window,13,6,26,604800); cache = build_label_cache(x,6)
    floor = np.abs(x[ev]); capacities = historical_forecasts(x,ev,cfg)['frozen_F']
    base_scores = score_predictions(cache.peak[ev],capacities,floor,ev)
    summaries = {'frozen_F':summarize_scores(base_scores)}
    candidates = {}; selections = {}; paired_percent = {'frozen_F':0.0}
    methods = [('QR33',(.001,.01,.1))]
    if include_panel_methods:
        cap = endpoint_predict(x,ev,6,window,13,checkpoint=checkpoint)['capacity']
        summaries['Levy_L'] = summarize_scores(score_predictions(cache.peak[ev],cap,floor,ev))
        methods.append(('C2_QR4',(.001,.01,.1,1.,10.)))
        feature,valid = features4(x,dates,6,26,604800)
    for method,menu in methods:
        rows = []
        def report(ids,penalty):
            if method=='QR33':
                return conditional_forecast(x,dates,ids,cfg,'QR',penalty,checkpoint=checkpoint).capacities
            return four_forecast(x,feature,valid,cache,ids,6,window,13,penalty,checkpoint)[0]
        for penalty in menu:
            checkpoint()
            try:
                cap = report(val,penalty)
                rows.append(dict(parameter=penalty,status='COMPLETE',**summarize_scores(
                    score_predictions(cache.peak[val],cap,np.abs(x[val]),val))))
            except QuantileFitError as error:
                rows.append(dict(parameter=penalty,status='FAILED',origin_count=0,
                                 mean_pinball=None,reason=error.code))
        choice = select_parameter(rows,menu,expected_count=52)
        candidates[method]=rows;selections[method]=choice
        if choice['status']!='SELECTED':continue
        cap=report(ev,choice['parameter'])
        scores=score_predictions(cache.peak[ev],cap,floor,ev)
        summaries[method]=summarize_scores(scores)
        paired_percent[method]=100*stable_mean(scores.pinball-base_scores.pinball)/summaries['frozen_F']['mean_pinball']
    for method,row in summaries.items():
        f=summaries['frozen_F']
        row['percent_vs_frozen_F']=100*(row['mean_pinball']-f['mean_pinball'])/f['mean_pinball']
        row['breaches_frozen_F']=f['strict_breach_count']
    return dict(summaries=summaries,candidates=candidates,selections=selections,
                paired_percent_vs_frozen_F=paired_percent)

t = time.monotonic(); billcfg = spec['sources']['nyfed_weekly']
billpath=root/'data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv'
bill=load_source(billpath,'nyfed_weekly',expected_sha256=billcfg['sha256'],expected_bytes=billcfg['bytes'])
bill_result=original_cell(bill.position,bill.dates,260)
old_qr=load('results/revision-20261022/evaluation-nyfed_weekly-h6-w260-QR.json')['result']['summary_rows'][0]
old_f=next(row for row in load('results/revision-20261022/references-nyfed_weekly-h6-w260.json')['result']['summary_rows']if row['method']=='frozen_F')
compare_scores('bill/QR',bill_result['summaries']['QR33'],old_qr)
compare_scores('bill/F',bill_result['summaries']['frozen_F'],old_f)
old_val=load('results/revision-20261022/validation-nyfed_weekly-h6-w260-QR.json')['result']
compare('bill/selected_penalty',bill_result['selections']['QR33']['parameter'],old_val['selection']['parameter'])
assert len(bill_result['candidates']['QR33']) == len(old_val['candidate_rows']) == 3
for row,expected in zip(bill_result['candidates']['QR33'],old_val['candidate_rows']):
    for key in ('parameter','status','origin_count','mean_pinball'):
        compare('bill/candidate/'+str(row['parameter'])+'/'+key,row[key],expected[key])
paired=next(row for row in csv.DictReader((root/'results/revision-20261022/paired-comparisons.csv').open())if row['source']=='nyfed_weekly'and row['horizon']=='6'and row['left_window']=='260'and row['left_method']=='QR'and row['right_method']=='frozen_F')
compare('bill/original_primary_percent',bill_result['paired_percent_vs_frozen_F']['QR33'],float(paired['relative_mean_loss_difference_percent']))
save('bill-recomputed.json',dict(**bill_result,elapsed_seconds=time.monotonic()-t))

t=time.monotonic();grid=[row['As Of Date']for row in csv.DictReader(io.StringIO(billpath.read_text()))]
x,alignment=align_source(panel_raw,'PDPOSCS-TOT',grid)
panel_result=original_cell(x,np.asarray(grid,dtype='datetime64[D]'),52,True)
old_panel=load('results/revision-20261023/round2/panel/cells/PDPOSCS-TOT-h6-w52.json')
for expected in old_panel['records']:
    method=expected['method'];assert method in panel_result['summaries']
    compare_scores('panel/'+method,panel_result['summaries'][method],expected)
    if method in panel_result['selections']:
        compare('panel/'+method+'/selected_penalty',panel_result['selections'][method]['parameter'],expected['selected_penalty'])
        assert len(panel_result['candidates'][method]) == len(expected['candidates'])
        for actual,candidate in zip(panel_result['candidates'][method],expected['candidates']):
            compare_scores('panel/'+method+'/candidate/'+str(actual['parameter']),actual,candidate)
save('panel-recomputed.json',dict(**panel_result,alignment=alignment,elapsed_seconds=time.monotonic()-t))

subprocess.run(['git','diff','--exit-code','HEAD','--'],check=True)
numeric=[row for row in checks if row['numeric_expected']]
mismatches=[row for row in checks if not row['equal']]
receipt=dict(**identity,ended_utc=utc(),elapsed_seconds=time.monotonic()-started,
    comparison_count=len(checks),numeric_comparison_count=len(numeric),
    maximum_absolute_numeric_difference=max((row['absolute_difference']for row in numeric if row['absolute_difference']is not None),default=0),
    exact_mismatch_count=len(mismatches),mismatches=mismatches,
    printed_CFTC_count=len(printed),printed_CFTC_all_equal=all(row['equal']for row in printed),
    no_old_intermediates_used=True,no_download=True,no_code_or_saved_results_changed=True,
    all_exact=(not mismatches and all(row['equal']for row in printed)))
save('comparisons.json',checks);save('completion.json',receipt)
print(json.dumps(receipt,indent=2))
assert receipt['all_exact'], 'Report differences; do not modify code, settings or saved results'
PY_REPRO
```

Read the new directory's `completion.json`, `comparisons.json`,
`cftc-printed-comparison.json`, per-method statuses and timing receipts. The original bill paired percentage uses the mean of the pointwise loss
differences, while panel percentages retain their original difference-of-means
arithmetic. Neither requires an additional fit. The check also asserts complete
204-cell identities and equal candidate-list lengths before comparison. Exact
numeric equality is required by this check; it does not silently round full
precision discrepancies away. If a method fails, report that failure and do
not retry it or replace it with a saved forecast. All old outputs remain intact.

## 4. Other manuscript targets and tests

The same native compilation pattern applies to `supplement.tex`,
`title-page.tex` and `cover-letter.tex` in separate new output directories.
Compilation is distinct from rendered-page visual review. The final v13 delivery
records four builds and every reviewed page under `notes/v13/`.

The complete test suite uses the pinned temporary environment described by the
final v13 test receipt. Some legacy tests additionally require original local
Git objects that may not be reachable from a public single-branch clone; the
historical v12 receipt explicitly disclosed this condition. Do not weaken those
tests, replace missing private data with synthetic observations, or present a
source compilation as a complete experiment reproduction.


## G4 documentation-only recovery of a table-row parser

The first execution of the recipe at commit `79ac6b8` completed all financial
fits once. All 1,338 full-precision numerical comparisons were exactly equal.
Its final assertion failed because the documentation's LaTeX row parser removed
only one of the two terminal backslashes. This affected the expected text in
17 last-column display comparisons, not a number, model, data input or saved
forecast. The corrected main recipe above removes the row terminator in full.

Do not rerun fitted cells to recover this documentation failure. When the first
run's new scalar outputs exist, run this saved-scalar-only comparison instead.
Keep the original failed completion and console unchanged. This command reads
only the scalars just recomputed by the fresh clone; it does not read old fitted
traces or re-estimate any model.

```bash
/Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with numpy==2.3.5 --with pypdf python -B - <<'PY_TABLE_RECHECK'
from pathlib import Path
import os,json,time,datetime,hashlib,subprocess
root=Path.cwd();out=Path(os.environ['V13_REPRO_OUTPUT']).absolute()
started=time.monotonic()
old_completion=json.loads((out/'completion.json').read_text())
comparisons=json.loads((out/'comparisons.json').read_text())
assert old_completion['exact_mismatch_count']==0
assert old_completion['numeric_comparison_count']==1338
assert len(comparisons)==1826 and all(row['equal']for row in comparisons)
recomputed=json.loads((out/'cftc-recomputed.json').read_text())
assert len(recomputed['cells'])==204
index={(row['code'],row['window'],row['method']):row for row in recomputed['cells']}
assert len(index)==204
codes=[row['code']for row in json.loads((root/'results/v10/cftc/sources.json').read_text())]
tex=(root/'submission-v10/generated/v10-cftc-contracts.tex').read_text()
printed=[]
for code in codes:
    line=next(line for line in tex.splitlines()if line.startswith(code+' & '))
    fields=[field.strip()for field in line.split('&')][1:]
    fields[-1]=fields[-1].rstrip(chr(92)).strip()
    assert len(fields)==20
    expected=[fields[i]+'.'+fields[i+1]for i in range(0,20,2)]
    identities=[(w,m)for w in (52,260)for m in ('I','QR4','QR33','ACI_F','ACI_QR33')]
    for (window,method),display in zip(identities,expected):
        actual=format(index[code,window,method]['relative_loss_pct'],'.2f')
        printed.append(dict(code=code,window=window,method=method,actual=actual,expected=display,equal=actual==display))
assert len(printed)==170 and all(row['equal']for row in printed)
receipt=dict(status='ALL_REQUESTED_REPRODUCTIONS_EXACT_AFTER_DOCUMENTATION_PARSER_CORRECTION',
    created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    elapsed_seconds=time.monotonic()-started,financial_fits_rerun=False,
    original_failed_completion_sha256=hashlib.sha256((out/'completion.json').read_bytes()).hexdigest(),
    original_returncode=1,full_precision_comparisons=1338,full_precision_maximum_difference=0,
    total_scalar_or_status_comparisons=1826,printed_percentages=170,
    printed_percentages_all_equal=True,
    recomputed_scalar_sha256=hashlib.sha256((out/'cftc-recomputed.json').read_bytes()).hexdigest(),
    source_table_sha256=hashlib.sha256((root/'submission-v10/generated/v10-cftc-contracts.tex').read_bytes()).hexdigest())
with (out/'cftc-printed-comparison-corrected.json').open('x')as f:json.dump(printed,f,indent=2);f.write('\n')
with (out/'completion-after-documentation-correction.json').open('x')as f:json.dump(receipt,f,indent=2);f.write('\n')
subprocess.run(['git','diff','--exit-code','HEAD','--'],check=True)
print(json.dumps(receipt,indent=2))
PY_TABLE_RECHECK
```
