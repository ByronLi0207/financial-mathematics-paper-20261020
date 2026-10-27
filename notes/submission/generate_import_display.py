"""Format audited saved WP2 fields only; never fit or score a forecast."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
REL = 'evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism/summary.json'
source = ROOT / REL
j = json.loads(source.read_text())
digest = hashlib.sha256(source.read_bytes()).hexdigest()
assert j['primary_verdict'] == 'PARTLY'
bindings = []

def bind(pointer):
    value = j
    for key in pointer.strip('/').split('/'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    bindings.append(dict(path=REL, sha256=digest, json_pointer=pointer, value=value))
    return value

out = [r'\section{Audited CFTC history-length extension}\label{sup:submission-wp2}',
       'This section imports saved results from the separately developed final-jof branch. '
       'The local design commit precedes calculation; public upload occurred after calculation. '
       'This is not an externally registered or prospective financial confirmation.',
       'The shorter-history outcomes had already been inspected. '
       'Only the longest-history forecasts were added under the fixed extension design. '
       'The same downloaded CFTC source arrays and reporting-vintage limitations apply.',
       r'\begin{table}[htbp]\centering\small',
       r'\caption{Fixed history-length decision screens, including failed and untestable predictions. Counts use the original planned denominators.}\label{tab:submission-wp2}',
       r'\begin{tabular}{lllll}\toprule',
       r'Screen & Regression & Successes / planned & Required fraction & Judgment\\\midrule']
names = {'QR4': 'Four-feature', 'QR33': 'Full'}
statuses = {'SUPPORT':'Supported', 'NOT_SUPPORT':'Not supported', 'NOT_TESTABLE':'Not testable'}
for key in ['P1_QR4','P1_QR33','P2_QR4','P2_QR33','P3_QR4']:
    row=j['tests'][key]; status=bind('/tests/'+key+'/status')
    planned=bind('/tests/'+key+'/planned')
    if planned:
        n=bind('/tests/'+key+'/successes'); threshold=bind('/tests/'+key+'/threshold')
        count=f'{n} / {planned}'; threshold=f'{threshold:.0%}'.replace('%',r'\%')
    else: count='---'; threshold='---'
    p,model=key.split('_');out.append(f'{p} & {names[model]} & {count} & {threshold} & {statuses[status]}'+r'\\')
out += [r'\bottomrule\end{tabular}\end{table}',
        'Both low-history disadvantage screens pass. The longer-history advantage screen '
        'and strict sequential-improvement screen fail. The full regression has no registered '
        'high-region cell. The retained overall judgment is partial support.',
        r'\paragraph{Complete counterexample inventory.} The following rows retain every saved counterexample. '
        'A market can appear under several screens. Loss changes are relative to the matched '
        'historical reference; their signs do not redefine a screen after observing it.',
        r'\begin{longtable}{lllp{7.5cm}}',
        r'\caption{All saved counterexamples to the transported history screens.}\label{tab:submission-wp2-counterexamples}\\',
        r'\toprule Screen & Market code & History & Relative loss change (percent)\\\midrule\endfirsthead',
        r'\toprule Screen & Market code & History & Relative loss change (percent)\\\midrule\endhead']
for idx,row in enumerate(j['counterexamples']):
    for field in ('screen','code'):
        bind(f'/counterexamples/{idx}/{field}')
    screen=row['screen'].replace('_',r'\_'); code=row['code']
    if 'relative_loss_percent' in row:
        value=bind(f'/counterexamples/{idx}/relative_loss_percent')
        window=bind(f'/counterexamples/{idx}/window'); shown=f'{value:+.6f}'
    else:
        # Saved P3 entries carry their own three-point curve; no forecasts are rerun.
        values=bind(f'/counterexamples/{idx}/relative_losses')
        windows=bind(f'/counterexamples/{idx}/windows')
        shown=', '.join(f'{float(v):+.6f}' for v in values)
        window='/'.join(str(w) for w in windows)
    out.append(f'{screen} & {code} & {window} & {shown}'+r'\\')
out += [r'\bottomrule\end{longtable}',
        r'\paragraph{Provenance and interpretation.} The design was committed locally before the recorded execution start; '
        'the audit records both original commit identities and their UTC times. '
        'The saved summary retains its execution-stage verification marker; later acceptance '
        'and scalar-check receipts supply the completed audit status. '
        'Scalar agreement by the same executor is not independent dealer replication or another solver fit.',
        r'Full cells, candidate reports, execution receipts and source identities are preserved in '
        r'\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/submission-final/evidence/submission/final-jof/results/final-merge/wp2-cftc-mechanism}{the audited result archive}. '
        r'The \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/notes/submission/import-audit.md}{import audit} '
        'distinguishes original data from additional non-data code dependencies. '
        'These related-market counts establish neither a sufficient financial history nor a causal mechanism.']
(ROOT/'submission-final/generated/submission-wp2.tex').write_text('\n\n'.join(out)+'\n')
(ROOT/'notes/submission/imported-number-bindings.json').write_text(json.dumps(dict(source_sha256=digest,bindings=bindings),indent=2)+'\n')
print('Formatted saved fields:',len(bindings))
