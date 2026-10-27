"""Integrate accepted WP3--WP5 public aggregates into the v8 Supplement.

Formatting only: no forecasting imports, raw/private inputs, fitted models or
statistical calculations. Existing numeric result rows remain byte-identical.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASELINE = '642d6af'
BINDINGS = []
SOURCES = {}
DATA = {}
GENERATED = ROOT / 'submission-jof/generated'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    path = ROOT / name
    SOURCES[name] = sha(path)
    DATA[name] = json.loads(path.read_text())
    return DATA[name]


def bound(value, source, field, fmt='g', scale=1):
    if field.startswith('variance_parameters.'):
        head, leaf = field.rsplit('.',1)
        tokens = ['variance_parameters',head[len('variance_parameters.'):],leaf]
    else:
        tokens = [int(index) if index else name for name,index in re.findall(r'([^.[\]]+)|\[(\d+)\]',field)]
    current = DATA[source]
    for token in tokens:current = current[token]
    assert current == value, (source,field,current,value)
    if value is None:
        rendered = 'NA'
    else:
        assert type(value) in (int, float) and math.isfinite(value), (field, value)
        rendered = str(value) if type(value) is int and fmt=='g' and scale==1 else format(value * scale, fmt)
    BINDINGS.append(dict(source=source, field=field, original_value=value,
                         field_tokens=tokens, scale=scale, format=fmt, rendered=rendered))
    return rendered


def exact_copy(source, target):
    source, target = ROOT/source, ROOT/target
    SOURCES[str(source.relative_to(ROOT))] = sha(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert source.read_bytes() == target.read_bytes()
    return dict(source=str(source.relative_to(ROOT)), target=str(target.relative_to(ROOT)),
                bytes=target.stat().st_size, sha256=sha(target))


def numeric_rows(tex):
    return [line for line in tex.splitlines() if '&' in line and re.search(r'\d', line)]


def mc_table(summary, method):
    source = 'results/revision-v8/wp3/summary.json'
    selected = [(i, r) for i, r in enumerate(summary['cells']) if r['method'] == method]
    selected.sort(key=lambda pair: tuple(pair[1][k] for k in
                                       ('horizon', 'phi', 'variance_persistence', 'window')))
    assert len(selected) == 72
    assert len({tuple(r[k] for k in ('horizon', 'phi', 'variance_persistence', 'window')) for _, r in selected}) == 72
    reference = {tuple(r[k] for k in ('horizon','phi','variance_persistence','window')):r for r in summary['cells'] if r['method']=='F'}
    for _,row in selected:
        ref=reference[tuple(row[k] for k in ('horizon','phi','variance_persistence','window'))]
        assert row['reference_breach_rate']==ref['model_breach_rate']
        assert row['reference_breach_mcse']==ref['model_breach_mcse']
        assert row['mean_reference_loss']==ref['mean_model_loss']
    title = 'Original full regression' if method == 'QR33' else 'Four-feature regression'
    label = 'full' if method == 'QR33' else 'four'
    lines = [r'\begingroup\footnotesize\setlength{\tabcolsep}{2.4pt}',
             r'\renewcommand{\arraystretch}{1.01}',
             r'\begin{longtable}{rrrrrrrrr}',
             r'\caption{Complete Monte Carlo grid: ' + title.lower() + r'. Entries are estimates with Monte Carlo standard errors in parentheses; percentage rates and their errors are in percentage points. Every cell is retained. The frozen narrow-region restriction fails.}\label{tab:v8-mc-' + label + r'}\\',
             r'\toprule',
             r'$H$ & $\phi$ & $p$ & History & \shortstack{Loss change\\vs F (\%)} & \shortstack{F breach\\rate (\%)} & \shortstack{Regression breach\\rate (\%)} & \shortstack{Win rate\\(\%)} & \shortstack{Complete /\\planned}\\\midrule',
             r'\endfirsthead',
             r'\caption[]{Continued.}\\\toprule',
             r'$H$ & $\phi$ & $p$ & History & \shortstack{Loss change\\vs F (\%)} & \shortstack{F breach\\rate (\%)} & \shortstack{Regression breach\\rate (\%)} & \shortstack{Win rate\\(\%)} & \shortstack{Complete /\\planned}\\\midrule',
             r'\endhead', r'\bottomrule\endfoot']
    identities = []
    for index, row in selected:
        prefix = f'cells[{index}]'
        def v(key, fmt='g', scale=1):
            return bound(row[key], source, prefix+'.'+key, fmt, scale)
        def pair(estimate, error, scale=1):
            return v(estimate, '.2f', scale) + ' (' + v(error, '.2f', scale) + ')'
        cell = [v('horizon'), v('phi'), v('variance_persistence'), v('window'),
                pair('relative_loss_percent', 'relative_loss_mcse'),
                pair('reference_breach_rate', 'reference_breach_mcse', 100),
                pair('model_breach_rate', 'model_breach_mcse', 100),
                pair('win_fraction', 'win_mcse', 100),
                v('complete_repetitions') + ' / ' + v('planned_repetitions')]
        lines.append(' & '.join(cell) + r'\\')
        identities.append(dict(summary_index=index,
            **{key: row[key] for key in ('method', 'horizon', 'phi', 'variance_persistence', 'window')},
            full_procedure_status=row['full_procedure_status']))
    lines += [r'\end{longtable}', r'\endgroup', '']
    path = GENERATED / ('v8-mc-'+label+'-table.tex')
    path.write_text('\n'.join(lines))
    return dict(path=str(path.relative_to(ROOT)), method=method, rows=len(selected),
                identities=identities, sha256=sha(path))


def integrate():
    GENERATED.mkdir(parents=True, exist_ok=True)
    base = subprocess.check_output(['git', 'show', BASELINE+':submission-jof/supplement.tex'], cwd=ROOT).decode()
    tex = base
    # These are prose-only corrections; all old financial table rows stay exact.
    old = '''This compact supplement contains the existing mathematical proofs and the
complete principal adverse-result inventories, with links to unchanged longer
archives. It accompanies the v7 manuscript and does not add models, data,
statistical tests or parameter selection. All later diagnostics are identified
as post-result / exploratory; the two original primary comparisons retain
their values and roles.'''
    new = '''This supplement retains the existing proofs and complete principal adverse-result
inventories, with links to the unchanged longer archives. It accompanies the
v8 manuscript and adds the accepted frozen simulation, same-dealer daily
aggregation and fixed-parameter full-prefix backcast. Each addition was frozen
before its own new output within a post-result / exploratory revision. The
two original primary comparisons retain their values and roles.'''
    assert tex.count(old) == 1
    tex = tex.replace(old, new)
    tex = tex.replace('amsmath,amssymb,booktabs,longtable,array,hyperref',
                      'amsmath,amssymb,booktabs,longtable,array,graphicx,hyperref')
    tex = tex.replace('source-native', 'source-reported').replace('completed responses', 'mature peak responses')
    tex = tex.replace('completed response', 'mature peak response').replace('strict-hit indicator', 'strict breach indicator')
    old = '''The earlier-period experiment applies the saved fixed selection rules
to familiar historical data. The bounded repository audit found no prior
evaluation role for these earlier origins; this is still retrospective, not
external or prospective validation.'''
    new = '''The earlier-period experiment applies the saved fixed selection rules
to familiar historical data. These origins already have validation and
evaluation roles in the current archive, including actual rolling-fold
scoring. They cannot now be treated as untouched evidence for the expanded
backcast. The experiment remains retrospective, not external or prospective
validation.'''
    assert tex.count(old) == 1
    tex = tex.replace(old, new)
    old = '''The accepted solver records primal and dual residuals, objectives, feasibility
and their gap. Ill-conditioned, nonfinite, unsupported-rank or failed candidate
states remain failures under the specified whole-cell selection contract.
Changing the ridge menu changes the procedure even when feature definitions
stay fixed. A successful numerical certificate is separate from the financial
accuracy, economic relevance and inferential validity of a forecast.'''
    new = '''The accepted solver records primal and dual residuals, objectives, feasibility
and their gap. Ill-conditioned, nonfinite, unsupported-rank and failed candidate
states retain their original statuses under each named selection contract.
A mandatory-candidate failure blocks a procedure when its contract requires
every candidate. The original full regression has that requirement; the
four-feature selector may choose among completed eligible candidates. A failed
selected evaluation never receives a replacement penalty or a shortened score.
Changing the ridge menu changes the procedure even when feature definitions
stay fixed. A numerical certificate does not establish financial accuracy,
economic relevance, inferential validity or production continuity.
No production continuity or fallback policy is evaluated here.'''
    assert tex.count(old) == 1
    tex = tex.replace(old, new)
    tex = tex.replace('This supplement describes the existing procedures; its document builder\nimports no forecasting code and performs no new financial computation.',
                      'The separate study receipts identify the executed additions. This document\nbuilder imports no forecasting code and only formats unchanged public results.')
    tex = tex.replace('This revision reads existing local software and results. No package installation,\nmodel fit, additional data acquisition, simulation rerun or parameter search\nbelongs to document assembly.',
                      'Document assembly reads existing local software and the recorded results.\nThe additional frozen studies were executed separately; no package installation,\nmodel fit, data acquisition, simulation rerun or parameter search belongs to\nthis formatting step.')
    tex=tex.replace('Missing compatible external validation and prospective first-release evaluation\nremain research tasks, rather than claims created by these reproducibility\nmaterials.', 'Compatible external and prospective first-release validation remain unmet.')
    assert numeric_rows(base) == numeric_rows(tex)
    old_rows = numeric_rows(base)
    old_result_rows=[row for row in old_rows if not row.startswith('Series &')]

    summary = load('results/revision-v8/wp3/summary.json')
    design = load('protocol/revision-v8/wp3-mechanism-design.json')
    support = load('results/revision-v8/wp3/support.json')
    reading = load('results/revision-v8/wp3/readout-bindings.json')
    daily = load('results/revision-v8/wp4/readout-bindings.json')
    daily_design = load('protocol/revision-v8/wp4-daily-fx-design.json')
    daily_class = load('results/revision-v8/wp4/classification.json')
    backcast = load('results/revision-v8/wp5/summary.json')
    back_design = load('protocol/revision-v8/wp5-fixed-prefix-design.json')
    back_windows = load('results/revision-v8/wp5/three-window-summary.json')
    exposure = load('notes/revision-v8/wp5-prior-exposure-proof.json')
    tables = [mc_table(summary, method) for method in ('QR33', 'QR4')]
    copies = [exact_copy(source, target) for source, target in [
        ('results/revision-v8/wp4/daily-results-table.tex','submission-jof/generated/v8-daily-results-table.tex'),
        ('results/revision-v8/wp5/three-window-table.tex','submission-jof/generated/v8-three-window-table.tex'),
        ('results/revision-v8/wp5/backcast-complete-table.tex','submission-jof/generated/v8-backcast-complete-table.tex'),
        ('results/revision-v8/wp3/figures/v8-wp3-qr4-loss.pdf','submission-jof/figures/v8-wp3-qr4-loss.pdf')]]
    ds = 'protocol/revision-v8/wp3-mechanism-design.json'
    def d(key, fmt='g'):
        return bound(design[key], ds, key, fmt)
    def lis(key):
        return ','.join(bound(value, ds, f'{key}[{i}]') for i,value in enumerate(design[key]))
    parameters = []
    for key, item in design['variance_parameters'].items():
        rendered = ','.join(bound(item[k], ds, f'variance_parameters.{key}.{k}') for k in ('omega','alpha','beta'))
        parameters.append('('+rendered+')')
    sp = support['procedures']['QR33']
    ss = 'results/revision-v8/wp3/support.json'
    sn = lambda k: bound(sp[k], ss, 'procedures.QR33.'+k)
    threshold = re.search(r'>=([0-9.]+)', design['support_screen']['clear_gain']).group(1)
    multiplier = re.search(r'(?:\+|plus) (\d+) delta MC SE', design['support_screen']['clear_gain']).group(1)
    region = re.fullmatch(r'H=(\d+),W>=(\d+),p>=([0-9.]+)', design['support_screen']['target_region'])
    assert region
    failure = reading['failed_candidates'][0]
    assert len(reading['failed_candidates']) == 1 and failure['procedure_status'] == 'COMPLETE'
    rf = 'results/revision-v8/wp3/readout-bindings.json'
    cn = lambda k: bound(reading['candidate_status_counts'][k], rf, 'candidate_status_counts.'+k)
    fn = lambda k: bound(failure['identity'][k], rf, 'failed_candidates[0].identity.'+k)
    penalty = bound(failure['candidate']['penalty'], rf, 'failed_candidates[0].candidate.penalty')
    chosen = bound(failure['selected_penalty'], rf, 'failed_candidates[0].selected_penalty')
    iterations = bound(failure['candidate']['failure_diagnostics']['iterations'], rf, 'failed_candidates[0].candidate.failure_diagnostics.iterations')
    complete = bound(reading['method_status_counts']['COMPLETE'], rf, 'method_status_counts.COMPLETE')
    worst = bound(summary['cells'][0]['win_mcse_worst_bound'], 'results/revision-v8/wp3/summary.json', 'cells[0].win_mcse_worst_bound', '.2f',100)
    mc = r'''
\section{Frozen controlled comparison of inherited procedures}\label{sup:v8-mc}

The simulation compares inherited reports for mean-reverting position levels,
not positively autocorrelated increments and not a fitted reproduction of either
financial source. It uses
\[
N_t=\phi N_{t-1}+\varepsilon_t,\qquad
\varepsilon_t=\sqrt{v_t}z_t,\qquad
v_t=\omega+a\varepsilon_{t-1}^{2}+bv_{t-1},\qquad
z_t\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,1).
\]
The level persistences are \(\phi\in\{PHI\}\), variance persistences
\(p=a+b\in\{PERSIST\}\), histories \(W\in\{WINDOWS\}\), and horizons
\(H\in\{HORIZONS\}\). For the increasing variance-persistence settings, the
\((\omega,a,b)\) triples are TRIPLES. Each innovation has unit unconditional
variance under the specified recursion. Initial level and variance are fixed;
a burn-in of BURN observations precedes RETAIN retained observations.
This is a long-burn approximation, not an exact stationary initialization.
The common hourly calendar has no simulated calendar effect.

There are REPS independent repetition streams, with master entropy SEED and
common normal innovations across conditions within a repetition. Validation
uses origins VALFIRST--VALLAST; evaluation uses EVALFIRST--EVALLAST, with
EVALCOUNT overlapping issues and a refit every REFIT records. Repetition, not
issue or grid cell, is the Monte Carlo uncertainty unit. Training uses exactly
\(W\) origins \(r-H-W+1,\ldots,r-H\), with every label ending by refit \(r\).
The current-position floor and query features use the actual issue state.
The full model keeps its original predictors and the parsimonious model its
original four; their penalty menus and failure rules differ, so their contrast
is not an isolated intervention on predictor count.

For each cell, let \(A_j\) and \(B_j\) be regression and matched-historical mean
loss in repetition \(j\), and \(R\) the planned number of repetitions. The
reported relative change and its delta-method Monte Carlo standard error are
\[
\widehat\Delta=100\left(\dfrac{\overline A}{\overline B}-1\right),\qquad
\operatorname{MCSE}(\widehat\Delta)=
\dfrac{100\,s(A_j-\widehat rB_j)}{\sqrt R\,\overline B},\qquad
\widehat r=\dfrac{\overline A}{\overline B}.
\]
Sample standard deviations use divisor \(R-1\). Breach-rate errors use the
between-repetition standard deviation divided by
\(\sqrt R\). Strict wins require \(A_j<B_j\), with error
\(\sqrt{\widehat\pi(1-\widehat\pi)/R}\). At zero or all wins that plug-in error is
zero without implying certainty; the worst-case error bound is
\(0.5/\sqrt R\), or WORST percentage points here. The short evaluation segments,
common innovations across cells, and fixed process family limit a regime claim.

The frozen descriptive clear-gain screen requires all REPS paired repetitions,
\(\widehat\Delta+MULTIPLIER\operatorname{MCSE}(\widehat\Delta)<0\), and a strict-win
fraction at least \(THRESHOLD\). Its target is \(H=REGIONH\), \(W\ge REGIONW\),
\(p\ge REGIONP\). Support additionally requires at least MINTARGET of TARGET
clear-gain target cells and none among the OUTSIDE outside cells. Each regression
has only INTARGET target gains and OUTGAIN outside gains. The recorded conclusion
is \textbf{MISMATCH}: both the target count and the no-outside requirement fail.
This screen has no family-wide significance guarantee and supplies no new
population endpoint-bound guarantee under dependent financial paths.

\input{generated/v8-mc-full-table.tex}
\input{generated/v8-mc-four-table.tex}

\paragraph{Candidate and procedure statuses.}
The complete inventory contains COMPLETE complete method tasks, CCAND complete
validation candidates and FCAND failed candidate. The failure is the four-feature
candidate at zero-based repetition FREP, \(\phi=FPHI\), \(p=FPERSIST\), \(W=FW\),
\(H=FH\), and penalty \(FPENALTY\). Its duality-gap criterion fails at FITITER
iterations. The frozen eligible-completed-candidate rule selects penalty
\(CHOSEN\), whose full evaluation completes; this is not a retry or substitution
of a failed selected evaluation. The original full-regression selector instead
requires every declared validation candidate. Incomplete procedures retain NA
full-procedure performance, with any available-pair summary labelled conditional
on completion. The saved source summaries retain all cells and their full
precision in \path{results/revision-v8/wp3/summary.json}; all six loss, breach and
win heatmaps and the complete receipt archive remain alongside them.

\begin{figure}[htbp]\centering
\includegraphics[width=.96\linewidth]{figures/v8-wp3-qr4-loss.pdf}
\caption{Four-feature regression in the complete fixed grid. Estimates are
relative mean loss changes against matched historical headroom; parentheses
show Monte Carlo standard errors across independent repetitions. Common
innovations correlate conditions, and shading is not a family-wide test.
Outside-region gains contradict the frozen narrow-condition restriction.}
\label{fig:v8-mc-four}
\end{figure}
'''
    mapping = dict(PHI=lis('phi'), PERSIST=lis('variance_persistence'), WINDOWS=lis('windows'), HORIZONS=lis('horizons'),
        TRIPLES=', '.join('\\('+s+'\\)' for s in parameters), BURN=d('burn_in'), RETAIN=d('retained_observations'),
        REPS=d('repetitions'), SEED=d('master_entropy'), VALFIRST=d('validation_first'), VALLAST=d('validation_last'),
        EVALFIRST=d('evaluation_first'), EVALLAST=d('evaluation_last'), EVALCOUNT=str(design['evaluation_last']-design['evaluation_first']+1),
        REFIT=d('refit_step'), WORST=worst, MULTIPLIER=multiplier, THRESHOLD=threshold, REGIONH=region[1], REGIONW=region[2], REGIONP=region[3],
        MINTARGET=sn('minimum_target_clear_gains'), TARGET=sn('target_cell_count'), OUTSIDE=sn('outside_cell_count'),
        INTARGET=sn('target_clear_gain_count'), OUTGAIN=sn('outside_clear_gain_count'), COMPLETE=complete,
        CCAND=cn('COMPLETE'), FCAND=cn('FAILED'), FREP=fn('rep'), FPHI=fn('phi'), FPERSIST=fn('variance_persistence'), FW=fn('window'), FH=fn('horizon'), FPENALTY=penalty, FITITER=iterations, CHOSEN=chosen)
    for key in sorted(mapping,key=len,reverse=True):
        mc=re.sub(r'\b'+key+r'\b',lambda _:mapping[key],mc)

    daily_source='results/revision-v8/wp4/readout-bindings.json'
    md=daily['daily_metadata'];period=daily['periods']
    n_daily=bound(md['n_daily'],daily_source,'daily_metadata.n_daily')
    n_issue=bound(period['evaluation_count'],daily_source,'periods.evaluation_count')
    dates={key:period[key].split('T')[0] for key in ('validation_first','validation_last','evaluation_first','evaluation_last')}
    daily_summary=load('results/revision-v8/wp4/summary.json')
    qindex,qexample=next((i,c) for i,c in enumerate(daily_summary['contrasts']) if c['method']=='QR4' and c['window']==260 and c['horizon']==6)
    dsec = r'''
\section{Same-dealer completed-day aggregation}\label{sup:v8-daily}

The pinned hourly FX snapshot produces NDAILY nonempty source-naive calendar
days under the frozen last-observation rule, rather than the approximate sample
size in the planning instruction. Each report is issued only at the end of its
completed source-naive day; the selected row's original timestamp is not treated
as an earlier time at which the identity of the last row was already known.
Missing days stay absent, and partial boundary days remain. The timezone and
historical first-release availability are unknown. This is a last-record proxy,
not a verified financial close or a peak over intraday excursions.

Histories and horizons count subsequent nonempty daily observations. The split
copies the Treasury observation-index geometry, not its absolute calendar dates
or a proportional split: validation runs from VSTART to VEND and evaluation from
ESTART to EEND on NISSUE common issues. The exact accepted raw fingerprint and
private resampling mapping are recorded separately; raw or resampled positions
and per-issue trajectories are not redistributed.

\input{generated/v8-daily-results-table.tex}

Historical headroom wins seven of the eight named comparisons, but the
four-feature longer-history, shorter-horizon daily exception lowers loss by
about DGAIN\% with DHITS regression breaches versus FHITS historical breaches.
Both regressions meet the fixed majority-based descriptive classification,
not a dominance or coverage theorem. Same recorded source identity is held
fixed while physical history, horizon, update cadence, calendar predictors,
sampled response and evaluation span change jointly. The contrast cannot
identify a pure frequency effect or supply independent dealer validation.
'''
    dlookup={(r['window'],r['horizon'],r['method']):(i,r['evaluation']) for i,r in enumerate(daily_summary['cells'])}
    dreplace=dict(NDAILY=n_daily,NISSUE=n_issue,VSTART=dates['validation_first'],VEND=dates['validation_last'],ESTART=dates['evaluation_first'],EEND=dates['evaluation_last'],
        DGAIN=bound(qexample['relative_loss_percent'],'results/revision-v8/wp4/summary.json',f'contrasts[{qindex}].relative_loss_percent', '.1f',-1),
        DHITS=bound(dlookup[(260,6,'QR4')][1]['strict_breach_count'],'results/revision-v8/wp4/summary.json',f"cells[{dlookup[(260,6,'QR4')][0]}].evaluation.strict_breach_count"),
        FHITS=bound(dlookup[(260,6,'F')][1]['strict_breach_count'],'results/revision-v8/wp4/summary.json',f"cells[{dlookup[(260,6,'F')][0]}].evaluation.strict_breach_count"))
    for key in sorted(dreplace,key=len,reverse=True):dsec=re.sub(r'\b'+key+r'\b',lambda _:dreplace[key],dsec)

    sample=back_design['sample'];scope='protocol/revision-v8/wp5-fixed-prefix-design.json'
    bn=lambda key:bound(sample[key],scope,'sample.'+key)
    be='notes/revision-v8/wp5-prior-exposure-proof.json'
    overlap=bound(exposure['nested_old_retro_issue_count'],be,'nested_old_retro_issue_count')
    union=exposure['old_H24_target_coverage_merged'][0]
    union_text='--'.join(bound(value,be,f'old_H24_target_coverage_merged[0][{i}]') for i,value in enumerate(union))
    penalties=[]
    for method_index,m in enumerate(back_design['methods']):
        if m['penalty_by_horizon'] is not None:
            penalties.append(('full regression' if m['name']=='QR33' else 'four-feature regression')+': '+', '.join('\\(H='+h+',\\lambda='+bound(v,scope,f'methods[{method_index}].penalty_by_horizon.'+h)+'\\)' for h,v in m['penalty_by_horizon'].items()))
    psec=r'''
\section{Fixed-parameter full-prefix backcast and overlapping windows}\label{sup:v8-backcast}

The additional retrospective backcast uses the complete eligible prefix
FIRST--LAST, with NISSUES common issue origins before the original later
validation. It retains the original later-selected parameters: PENALTIES.
Coefficients, transformations and training labels obey \(i+H\le r\) at each
refit, but those fixed penalties were chosen after the historical issue dates.
Thus this is a fixed-parameter pseudo-out-of-sample backcast with later-selected
parameters, not a real-time historical validation.

The full prefix contains all OVERLAP earlier reported backcast origins,
with inclusive issue indices OLD_FIRST--OLD_LAST.
Actual earlier rolling-validation targets at the longer horizon cover UNION,
exactly the new prefix's longer-horizon target range. Apparent issue gaps between old validation blocks
are not untouched target paths. Three displayed overlapping/inspected windows
therefore do not create a fresh independent third validation period. This
\textbf{MISMATCH} remains regardless of the direction of the added score
comparisons. No window effects, p-values or success counts are pooled.

\input{generated/v8-three-window-table.tex}
\input{generated/v8-backcast-complete-table.tex}

The frozen short-horizon full-regression descriptive screen retains matched
score gains across the three inspected windows and a changing rolling-reference
direction. It is not confirmation after inspection or independent replication.
The complete longer-horizon results also retain matched score gains, and the
full regression's loss against the rolling reference. A score gain can coexist
with more breaches; neither a conditional-coverage certificate nor an economic
operating benefit follows from these tables.

The added eight pairwise tests use only raw standard-normal two-sided
DM-type working references, separate from all original adjusted families.
For \(n\) paired loss differences and horizon \(H\),
\[
L=\min\!\left(n-1,\max\!\left\{H,
\left\lfloor4(n/100)^{2/9}\right\rfloor\right\}\right).
\]
The centered Bartlett Newey--West covariance uses divisor \(n\), and the
statistic is the mean regression-minus-reference loss divided by
\(\sqrt{\widehat{\mathrm{LRV}}/n}\). Nonpositive long-run variance or constant
loss differences retain an unavailable statistic and their specified status;
there is no epsilon repair. These p-values receive no multiplicity or full
selection adjustment and do not establish equivalence, real-time validity or
independent confirmation. Missing old longer-horizon original-menu, parsimonious,
rolling-DM or breach-count fields stay NA; the old five-menu rule is not relabelled
as the original three-menu regression. No missing old test was recalculated.
'''
    preplace=dict(FIRST=bn('evaluation_first'),LAST=bn('evaluation_last'),NISSUES=bn('evaluation_count'),
                  PENALTIES='; '.join(penalties),OVERLAP=overlap,UNION=union_text,
                  OLD_FIRST=bound(back_design['known_exposure']['R6_retro_evaluation'][0],scope,'known_exposure.R6_retro_evaluation[0]'),
                  OLD_LAST=bound(back_design['known_exposure']['R6_retro_evaluation'][1],scope,'known_exposure.R6_retro_evaluation[1]'))
    for key in sorted(preplace,key=len,reverse=True):psec=re.sub(r'\b'+key+r'\b',lambda _:preplace[key],psec)
    marker=r'\section{Reproduction, availability and retained extended results}'
    assert tex.count(marker)==1
    addition=mc+'\n'+dsec+'\n'+psec+'\n'
    tex=tex.replace(marker,addition+marker)
    assert numeric_rows(tex)==old_rows
    # Old numeric lines occur in order, unchanged, on both sides of insertion.
    pos=0
    for line in old_rows:
        at=tex.find(line,pos)
        assert at>=pos,line
        pos=at+len(line)
    (ROOT/'submission-jof/supplement.tex').write_text(tex)
    receipt=dict(generated_utc=datetime.now(timezone.utc).isoformat(),baseline_commit=BASELINE,
        baseline_supplement_sha256=hashlib.sha256(base.encode()).hexdigest(),supplement_sha256=sha(ROOT/'submission-jof/supplement.tex'),
        old_numeric_rows=len(old_rows),old_result_rows=len(old_result_rows),old_numeric_header_rows=len(old_rows)-len(old_result_rows),old_numeric_rows_exact_in_original_order=True,
        source_hashes=SOURCES,mc_tables=tables,exact_copies=copies,bindings=BINDINGS,
        numeric_formula_contexts={
            'Gaussian_DGP_definition':{'source':ds,'fields':['initial_level','initial_variance','rng']},
            'relative_change_and_delta_MCSE':{'source':ds,'fields':['mcse.relative_change','mcse.relative_mcse']},
            'sample_SD_divisor_and_win_error':{'source':ds,'fields':['mcse.breach_rate','mcse.strict_wins']},
            'clear_gain_multiplier_and_threshold':{'source':ds,'field':'support_screen.clear_gain','source_text':design['support_screen']['clear_gain'],'parsed_multiplier':multiplier,'parsed_threshold':threshold},
            'target_region':{'source':ds,'field':'support_screen.target_region','source_text':design['support_screen']['target_region'],'parsed_H':region[1],'parsed_W_min':region[2],'parsed_p_min':region[3]},
            'evaluation_issue_count':{'source':ds,'fields':['evaluation_first','evaluation_last'],'expression':'evaluation_last-evaluation_first+1','rendered':mapping['EVALCOUNT']},
            'raw_DM_bandwidth_formula':{'source':scope,'field':'inference.bandwidth','source_text':back_design['inference']['bandwidth']}},
        date_bindings=[dict(source=daily_source,field='periods.'+k,source_value=period[k],transform='beforeT',rendered=v) for k,v in dates.items()],
        resolved_display_mismatch='MISMATCH-WP7-SEED-DISPLAY: exactintegeridentifier after recorded g-format failure',
        new_financial_computations=0,forecasting_imports=False,raw_or_private_inputs=False,
        unchanged_original_primary_values=True,document_builder_sha256=sha(Path(__file__)))
    path=ROOT/'notes/revision-v8/wp7-supplement-integration.json'
    path.write_text(json.dumps(receipt,indent=2)+'\n')
    seed_binding=next(x for x in BINDINGS if x['field']=='master_entropy')
    assert seed_binding['rendered']==str(design['master_entropy'])
    print(json.dumps({k:receipt[k] for k in ['old_result_rows','old_numeric_header_rows','old_numeric_rows','old_numeric_rows_exact_in_original_order','new_financial_computations','raw_or_private_inputs']},indent=2))
    print(json.dumps({'MC_table_rows':[t['rows'] for t in tables], 'source_bound_values':len(BINDINGS),'exact_copies':len(copies)}))


if __name__=='__main__':integrate()
