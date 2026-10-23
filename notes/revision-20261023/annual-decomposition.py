#!/usr/bin/env python3
"""Read three frozen public aggregate CSVs; audit three FX decompositions.

No raw observations, model fits, private arrays, network, or third-party packages.
All arithmetic uses exact Fraction(saved decimal token); Decimal is display only.
Run with --output pointing to a NEW file. Existing outputs are never replaced.
"""
import argparse
import csv
import hashlib
import io
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


DEFAULT_REPO = Path(__file__).resolve().parents[2]
INPUTS = {
    'paired-annual.csv': ('5b0727af566cbfa935fba95c25cf2a7918dc073baa2daf8558d84984161bce40', 388),
    'paired-comparisons.csv': ('a19c804690db029a26c4343a5cfb0689c95d40f0216b8d3f8fd32ced26d079c9', 98),
    'paired-nonoverlap.csv': ('b050007b8ddffc5ba5865ccad90960740d94f55d7dd7a814e88665aa3d55677d', 98),
}
MENU = (
    ('FX H6 primary', 'fx_hourly-h6-QR2880-minus-rolling_F720', 6, 720, 'rolling_F', 'True', 'False'),
    ('FX H6 matched', 'fx_hourly-h6-QR2880-minus-frozen_F2880', 6, 2880, 'frozen_F', 'False', 'False'),
    ('FX H24 legacy', 'fx_hourly-h24-QR2880-minus-rolling_S720', 24, 720, 'rolling_S', 'False', 'True'),
)
MEANS = ('mean_pinball_left', 'mean_pinball_right', 'mean_pinball_difference',
         'mean_positive_overrun_difference', 'mean_unused_allowance_difference')
TOLERANCE = Fraction('0.0000001')  # 1e-7 USD per origin, fixed before readback.


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number(token):
    # Fraction rejects NaN/Infinity. No binary-float conversion is performed.
    require(isinstance(token, str) and bool(token), 'missing numeric token')
    return Fraction(token)


def positive_integer(token):
    require(isinstance(token, str) and token.isascii() and token.isdigit(), 'invalid count')
    value = int(token)
    require(value > 0 and str(value) == token, 'noncanonical or nonpositive count')
    return value


def exact(value):
    value = Fraction(value)
    with localcontext() as ctx:
        ctx.prec = 70
        display = format(Decimal(value.numerator) / Decimal(value.denominator), '.30f')
    return {'numerator': str(value.numerator), 'denominator': str(value.denominator),
            'decimal_30_places': display}


def sign(value):
    return 'negative' if value < 0 else 'positive' if value > 0 else 'zero'


def load_csv(base, filename):
    raw = (base / filename).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    expected_digest, expected_rows = INPUTS[filename]
    require(digest == expected_digest, 'frozen input SHA-256 mismatch: ' + filename)
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''))
    require(reader.fieldnames is not None and len(set(reader.fieldnames)) == len(reader.fieldnames), 'duplicate CSV header')
    rows = list(reader)
    require(len(rows) == expected_rows and all(None not in r and None not in r.values() for r in rows), 'CSV row/schema mismatch')
    indexed = {}
    for row in rows:
        key = (row['contrast_id'], row['calendar_year']) if filename == 'paired-annual.csv' else row['contrast_id']
        require(key not in indexed, 'duplicate public aggregate key: ' + str(key))
        indexed[key] = row
    return indexed, {'path': str(Path('results/revision-20261022') / filename), 'bytes': len(raw), 'sha256': digest,
                     'row_count': len(rows), 'unique_keys_verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=DEFAULT_REPO)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'output already exists; choose a new path')
    base = args.repo / 'results/revision-20261022'
    tables, identities = {}, {}
    for filename in INPUTS:
        tables[filename], identities[filename] = load_csv(base, filename)
    annual = tables['paired-annual.csv']
    all_rows = tables['paired-comparisons.csv']
    sparse = tables['paired-nonoverlap.csv']
    require(set(all_rows) == set(sparse) == {k[0] for k in annual}, 'complete archive menu mismatch')
    require(len(MENU) == 3 and len({m[1] for m in MENU}) == 3, 'three-comparison audit menu is incomplete')
    output = []
    for name, cid, horizon, right_window, right_method, primary, legacy in MENU:
        require(cid in all_rows and cid in sparse, 'missing declared comparison')
        years = {year: row for (contrast, year), row in annual.items() if contrast == cid}
        require(set(years) == {'2016', '2017'}, 'missing or extra FX issue-year group')
        rows = [all_rows[cid], sparse[cid], years['2016'], years['2017']]
        expected = {'source': 'fx_hourly', 'native_unit': 'USD', 'horizon': str(horizon),
                    'left_window': '2880', 'left_method': 'QR', 'right_window': str(right_window),
                    'right_method': right_method, 'declared_source_primary': primary, 'h24_legacy_contrast': legacy}
        require(all(all(r[k] == v for k, v in expected.items()) for r in rows), 'comparison identity/unit binding mismatch')
        counts = {year: positive_integer(row['origin_count']) for year, row in years.items()}
        n = positive_integer(all_rows[cid]['origin_count'])
        require(counts == {'2016': 6262, '2017': 363} and n == 6625 and sum(counts.values()) == n, 'origin count mismatch')
        require([(r['first_source_index'], r['last_source_index']) for r in (years['2016'], years['2017'])]
                == [('11927', '18188'), ('18189', '18551')], 'annual issue-range mismatch')
        require((all_rows[cid]['first_source_index'], all_rows[cid]['last_source_index']) == ('11927', '18551'), 'all-origin range mismatch')
        stride = positive_integer(sparse[cid]['stride_records'])
        grid_n = positive_integer(sparse[cid]['origin_count'])
        require(stride == horizon + 1 and grid_n == (18551 - 11927) // stride + 1, 'fixed-grid count/stride mismatch')
        require(int(sparse[cid]['first_source_index']) == 11927
                and int(sparse[cid]['last_source_index']) == 11927 + stride * (grid_n - 1), 'fixed-grid anchor mismatch')
        reconciliation = {}
        for field in MEANS:
            weighted = sum(counts[y] * number(years[y][field]) for y in years) / n
            saved_all = number(all_rows[cid][field])
            discrepancy = weighted - saved_all
            require(abs(discrepancy) <= TOLERANCE, 'annual/all-origin mean reconciliation failed: ' + field)
            reconciliation[field] = {'annual_weighted_mean': exact(weighted), 'saved_all_origin_mean': exact(saved_all),
                                     'difference': exact(discrepancy), 'pass': True}
        # Both annual means are negative: positive net gains are -n_y * d_y.
        gains = {y: -counts[y] * number(years[y]['mean_pinball_difference']) for y in years}
        require(all(v > 0 for v in gains.values()), 'nonpositive annual net gain; contribution interpretation changed')
        total = sum(gains.values())
        period_rows = {'all_origins': all_rows[cid], '2016': years['2016'], 'partial_2017': years['2017'], 'fixed_sparse_grid': sparse[cid]}
        components = {}
        expected_signs = ('negative', 'negative') if horizon == 6 else ('positive', 'negative')
        for period, row in period_rows.items():
            u, v = number(row['mean_positive_overrun_difference']), number(row['mean_unused_allowance_difference'])
            require((sign(u), sign(v)) == expected_signs, 'component-sign claim failed: ' + period)
            # Pinball decomposition reconciles saved aggregates, without raw losses.
            residual = number(row['mean_pinball_difference']) - (Fraction(19, 20) * u + Fraction(1, 20) * v)
            require(abs(residual) <= TOLERANCE, 'saved pinball/component identity failed')
            components[period] = {'origin_count': positive_integer(row['origin_count']), 'delta_mean_overrun': exact(u),
                                  'delta_mean_unused': exact(v), 'signs': [sign(u), sign(v)],
                                  'pinball_identity_residual': exact(residual)}
        output.append({'name': name, 'contrast_id': cid, 'native_unit': 'USD',
                       'annual_net_gains_from_saved_means': {y: exact(g) for y, g in gains.items()},
                       'total_net_gain_from_saved_annual_means': exact(total),
                       'partial_2017_origin_share_percent': exact(Fraction(100 * counts['2017'], n)),
                       'partial_2017_net_gain_contribution_percent': exact(100 * gains['2017'] / total),
                       'reconciliation': reconciliation, 'component_checks': components})
    result = {'status': 'PASS', 'schema_version': 1, 'audit_id': 'annual-decomposition-20261023',
              'scope': 'Readback of three comparisons from frozen public aggregates only; no new forecast or raw-observation analysis.',
              'arithmetic': 'Exact Fraction of saved decimal tokens. Decimal is used only for 30-place display; integer numerator/denominator is authoritative.',
              'tolerance': {'absolute_per_origin_native_USD': exact(TOLERANCE),
                            'explanation': 'Weighted annual saved means and independently saved all-origin means have separate float64 rounding histories. Each mean and pinball-component reconciliation must differ by at most 1e-7 USD. Equivalently, sum-level discrepancy is at most n*1e-7 USD. Exact decimal-token algebra is not infinite-precision raw-loss truth.'},
              'interpretation': 'Contribution = (-n_2017*d_2017)/sum_years(-n_year*d_year). Issue-year groups, sparse grids and configurations are dependent parts of the same inspected FX archive, not independent replications.',
              'inputs': identities, 'complete_public_contrast_count': len(all_rows), 'audited_comparison_count': len(output),
              'comparisons': output}
    # Exclusive creation happens only after every check passed. No mkdir/replace.
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'output': str(args.output),
                      'contribution_percent': {r['name']: r['partial_2017_net_gain_contribution_percent']['decimal_30_places'] for r in output}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
