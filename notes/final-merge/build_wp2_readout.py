"""Display the committed WP2 outcomes; no fitting or new statistical choices."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RESULT='results/final-merge/wp2-cftc-mechanism'


def main():
    s=json.loads((ROOT/RESULT/'summary.json').read_text())
    audit=json.loads((ROOT/RESULT/'independent-verification.json').read_text())
    rounding=json.loads((ROOT/RESULT/'verification-roundoff-detail.json').read_text())
    assert audit['mismatch_count']==0
    out=['# WP2 CFTC mechanism result: '+s['primary_verdict'],'',
        'Registered before W=520 forecasts at commit `'+audit['protocol_commit']+'`. The 17 markets, six-candidate menus, chronological split, fixed A thresholds and success rules were not changed after the run. W=52/260 outcomes were already known; only W=520 is a new forecast extension. CFTC aggregates dealers by market and is a separate reporting source, not independent dealer-level replication.','',
        '| Screen | Successful / planned | Threshold | Result |','|---|---:|---:|---|']
    for name,t in s['tests'].items():
        out.append(f"| {name} | {t.get('successes','NA')} / {t['planned']} | {t.get('threshold','NA')} | {t['status']} |")
    out += ['',
        'Both method-specific P1 screens pass; P2-QR4 does not. Ten of seventeen is 58.82352941176471%, below the registered 60% threshold; it is not rounded into a pass. The secondary strict-decrease prediction also fails. QR33 has no registered high-region cell. All 153 method/window/market cells and 102 matched conditional comparisons are complete. There are no omitted failures or unknowns in this run.','',
        'The result supports the limited short-history disadvantage count. It does not validate a generally sufficient history threshold, monotone improvement, parameter normalization, or a uniquely causal estimation-cost explanation. Regime changes, menu selection and shrinkage remain alternative explanations. A first simulation crossing and its wide fixed-grid interval are different from a sufficient financial history bound.','',
        '## Independent algorithm audit','',
        f"{audit['scalar_and_identity_checks']} scalar/identity checks, {audit['complete_traces']} complete evaluation traces, {audit['complete_validation_reports']} complete validation-candidate reports and {audit['maturity_diagnostic_rows']} maturity records: zero mismatches under the predeclared absolute1e-10 + relative1e-12 tolerance. Integer identities and hashes are exact. This is a separate scalar implementation by the same sole executor, not another person/model, independent data acquisition, or a second finite-penalty solver fit.",'',
        f"The largest absolute floating-point discrepancy was {rounding['largest_absolute']['absolute_difference']!r} for an LRV near {rounding['largest_absolute']['inherited']!r}. It uses {rounding['largest_absolute']['fraction_of_allowed']!r} of its allowed error. The largest fraction of any allowed error was {rounding['largest_fraction_of_allowed']['fraction_of_allowed']!r}. Zero mismatches does not mean byte-identical floating-point summation.",'',
        'The summary JSON retains its pre-audit PENDING marker as an execution-stage record. The dated independent-verification.json and final acceptance receipt provide the completed audit status. No model output was overwritten.','',
        '## Every paired cell','',
        'All values below are display-rounded only. Full-precision scalars, statuses, penalties and trace hashes are in `'+RESULT+'/cells.csv` and `comparisons.csv`. The 153-cell inventory includes F separately. Each QR row below carries its own matched F and strict breach counts. Raw normal HAC DM p-values are descriptive dependent comparisons, without a new family-adjusted significance claim; L=6 and n=260 throughout.','',
        '| Code | W | Model | F loss | Model loss | Change % | F breaches | Model breaches | HAC t | Raw p | Selected penalty |',
        '|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|']
    def fmt(x):return 'NA' if x is None else format(x,'.9g')
    for r in s['comparisons']:
        dm=r['dm'] or {}
        out.append('| '+' | '.join([r['code'],str(r['window']),r['method'],fmt(r['reference_loss']),fmt(r['model_loss']),fmt(r['relative_loss_percent']),str(r['reference_breach_count']),str(r['model_breach_count']),fmt(dm.get('dm_t')),fmt(dm.get('dm_p')),str(r['selected_penalty'])])+' |')
    out += ['','## Complete counterexample inventory','',
        'A code can occur in more than one screen. P1 counterexamples are low-region wins or ties; P2 counterexamples are high-region losses or ties. P3 requires both successive decreases, so an endpoint improvement alone is insufficient.','',
        '| Screen | Code | W | Relative change % or QR4 changes at W52,260,520 |',
        '|---|---|---:|---|']
    for r in s['counterexamples']:
        value=', '.join(fmt(x) for x in r['relative_losses']) if 'relative_losses' in r else fmt(r['relative_loss_percent'])
        out.append(f"| {r['screen']} | {r['code']} | {r.get('window','52→260→520')} | {value} |")
    out += ['','The seven P2-QR4 counterexamples are 044601, 043602, 042601, 045601, 099741, 095741 and 232741. Every one remains in the report. The 25 listed screen counterexamples are not 25 distinct markets.','']
    path=ROOT/'notes/final-merge/wp2-cftc-mechanism-results.md';path.write_text('\n'.join(out))
    print(json.dumps(dict(status='PASS',verdict=s['primary_verdict'],displayed_comparisons=len(s['comparisons']),displayed_counterexamples=len(s['counterexamples']),new_model_fits=0,output=str(path.relative_to(ROOT))),indent=2))


if __name__=='__main__':main()
