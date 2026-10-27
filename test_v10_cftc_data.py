"""Artificial in-memory archives and clocks only; never open acquired CFTC files."""
from copy import deepcopy
from datetime import date, timedelta
import csv
import importlib
import importlib.util
import io
import json
import unittest
import zipfile


HEADERS = ['Market_and_Exchange_Names', 'As_of_Date_In_Form_YYMMDD',
           'CFTC_Contract_Market_Code', 'CFTC_Market_Code', 'Open_Interest_All',
           'Dealer_Positions_Long_All', 'Dealer_Positions_Short_All', 'Contract_Units']


def api():
    assert importlib.util.find_spec('v10_cftc_data') is not None, 'CFTC data module is missing'
    return importlib.import_module('v10_cftc_data')


def settings():
    return dict(required_columns=HEADERS[:], date_header_aliases=[
        'Report_Date_as_MM_DD_YYYY', 'Report_Date_as_YYYY-MM-DD'],
        first_included_position_date='2010-01-01', first_expected_week='2010-01-04',
        top_contracts=20, known_scope_change_excluded_code_prefixes=['13874', '20974', '12460'],
        horizon=6, windows=[52, 260], refit_step=13, feature_rms_long=26,
        ancillary={'methods': ['ACI_F', 'ACI_QR33']})


def ownership():
    return dict(file='artificial.zip', url='https://www.cftc.gov/artificial.zip',
                first_position_year=2010, last_position_year=2016)


def source_row(**changes):
    row = dict(zip(HEADERS, ['Artificial market', '100105', '001234', 'CME',
                            '1,200', '200', '350', 'CONTRACTS OF $1,000']))
    row.update(changes)
    return row


def archive(rows, headers=None, encoding='utf-8-sig', members=None):
    text = io.StringIO(newline='')
    writer = csv.DictWriter(text, fieldnames=headers or HEADERS)
    writer.writeheader(); writer.writerows(rows)
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        z.writestr('artificial.txt', text.getvalue().encode(encoding))
        for name, payload in members or []:
            z.writestr(name, payload)
    return out.getvalue()


def series(code='001234', oi=100, count=660, start='2010-01-04'):
    first = date.fromisoformat(start)
    rows = []
    for i in range(count):
        week = first + timedelta(weeks=i)
        actual = week + timedelta(days=1)
        rows.append(dict(code=code, name='Artificial '+code, exchange='CME', units='CONTRACTS',
            position_date=actual.isoformat(), week=week.isoformat(), open_interest=oi,
            long=20, short=30, net=-10, errors=[]))
    return rows


class ArchiveTests(unittest.TestCase):
    def test_canonical_values_preserve_string_code_and_signed_net(self):
        rows, audit = api().read_archive(archive([source_row()]), ownership(), settings())
        row = rows[0]
        self.assertEqual((row['code'], row['week'], row['position_date']),
                         ('001234', '2010-01-04', '2010-01-05'))
        self.assertEqual((row['open_interest'], row['long'], row['short'], row['net']),
                         (1200, 200, 350, -150))
        self.assertEqual(audit['raw_rows'], 1)
        self.assertEqual(audit['retained_rows'], 1)
        self.assertEqual(audit['encoding'], 'utf-8-sig')

    def test_ownership_exclusions_keep_original_rows_without_deduplicating(self):
        old = source_row(As_of_Date_In_Form_YYMMDD='090106')
        newer = source_row(As_of_Date_In_Form_YYMMDD='170103')
        retained = source_row()
        rows, audit = api().read_archive(archive([old, retained, newer]), ownership(), settings())
        self.assertEqual(len(rows), 1)
        self.assertEqual(audit['ownership_excluded_count'], 2)
        self.assertEqual([r['line_start'] for r in audit['ownership_excluded_rows']], [2, 4])
        self.assertEqual([r['position_date'] for r in audit['ownership_excluded_rows']], ['2009-01-06', '2017-01-03'])
        self.assertEqual(audit['raw_rows'], 3)

    def test_only_frozen_full_date_aliases_are_cross_checked(self):
        for alias, full in [('Report_Date_as_MM_DD_YYYY', '01/05/2010'),
                            ('Report_Date_as_YYYY-MM-DD', '2010-01-05')]:
            with self.subTest(alias=alias):
                rows, _ = api().read_archive(archive([source_row(**{alias: full})], HEADERS+[alias]), ownership(), settings())
                self.assertEqual(rows[0]['position_date'], '2010-01-05')
                with self.assertRaises(ValueError):
                    api().read_archive(archive([source_row(**{alias: '2010-01-06'})], HEADERS+[alias]), ownership(), settings())

    def test_literal_midnight_is_rejected_without_clarification_and_accepted_only_with_it(self):
        alias = 'Report_Date_as_MM_DD_YYYY'
        raw = archive([source_row(As_of_Date_In_Form_YYMMDD='161227',
            **{alias: '12/27/2016 12:00:00 AM'})], HEADERS+[alias])
        with self.assertRaises(ValueError):
            api().read_archive(raw, ownership(), settings())
        design = settings()
        design['ingestion_clarification'] = {'accepted_literal_suffix': ' 12:00:00 AM'}
        try:
            rows, _ = api().read_archive(raw, ownership(), design)
        except ValueError as exc:
            self.fail('Verified literal midnight clarification was rejected: '+str(exc))
        self.assertEqual(rows[0]['position_date'], '2016-12-27')
        self.assertEqual(rows[0]['week'], '2016-12-26')

    def test_midnight_clarification_does_not_accept_mismatch_other_times_or_suffixes(self):
        alias = 'Report_Date_as_MM_DD_YYYY'
        design = settings()
        design['ingestion_clarification'] = {'accepted_literal_suffix': ' 12:00:00 AM'}
        for value in ['12/26/2016 12:00:00 AM', '12/27/2016 01:00:00 AM',
                      '12/27/2016 12:00:00 PM', '12/27/2016 00:00:00',
                      '12/27/2016 12:00:00 am', '12/27/2016 12:00:00 AM UTC',
                      '12/27/2016  12:00:00 AM']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                raw = archive([source_row(As_of_Date_In_Form_YYMMDD='161227',
                    **{alias: value})], HEADERS+[alias])
                api().read_archive(raw, ownership(), design)
        for suffix in ['', ' 01:00:00 AM', ' 12:00:00 AM UTC', None]:
            with self.subTest(clarification=suffix), self.assertRaises(ValueError):
                changed = deepcopy(design)
                changed['ingestion_clarification']['accepted_literal_suffix'] = suffix
                raw = archive([source_row(As_of_Date_In_Form_YYMMDD='161227',
                    **{alias: '12/27/2016 12:00:00 AM'})], HEADERS+[alias])
                api().read_archive(raw, ownership(), changed)

    def test_frozen_report_type_gate_accepts_only_normalized_futures_only_or_blank(self):
        marker = 'FutOnly_or_Combined'
        design = settings(); design['report_type_marker'] = 'frozen report-type rule'
        for value in ['FutOnly', 'Futures Only', ' FUT-ONLY ', 'FUTURES_ONLY', '', '   ']:
            with self.subTest(marker=value):
                raw = archive([source_row(**{marker: value})], HEADERS+[marker])
                rows, audit = api().read_archive(raw, ownership(), design)
                self.assertEqual(len(rows), 1)
                self.assertTrue(audit['report_type_marker_present'])
        rows, audit = api().read_archive(archive([source_row()]), ownership(), design)
        self.assertEqual(len(rows), 1)
        self.assertFalse(audit['report_type_marker_present'])

    def test_frozen_report_type_gate_rejects_unknown_or_combined_even_outside_ownership(self):
        marker = 'FutOnly_or_Combined'
        design = settings(); design['report_type_marker'] = 'frozen report-type rule'
        for value in ['Combined', 'FuturesAndOptions', 'Unknown', '---']:
            with self.subTest(marker=value), self.assertRaises(ValueError):
                raw = archive([source_row(**{marker: value})], HEADERS+[marker])
                api().read_archive(raw, ownership(), design)
        with self.assertRaises(ValueError):
            raw = archive([source_row(**{marker: 'FutOnly'}),
                source_row(As_of_Date_In_Form_YYMMDD='090106', **{marker: 'Combined'})], HEADERS+[marker])
            api().read_archive(raw, ownership(), design)

    def test_required_year_payload_rejects_empty_owned_year_without_replacement(self):
        design = settings(); design['required_year_payload'] = 'frozen required annual owner rule'
        owner = ownership(); owner.update(first_position_year=2011, last_position_year=2011)
        for raw in [archive([]), archive([source_row()])]:
            with self.subTest(size=len(raw)), self.assertRaises(ValueError):
                api().read_archive(raw, owner, design)
        rows, audit = api().read_archive(archive([source_row(As_of_Date_In_Form_YYMMDD='110104')]), owner, design)
        self.assertEqual(rows[0]['position_date'], '2011-01-04')
        self.assertEqual(audit['retained_rows'], 1)
        # The optional design key gates the new enforcement; artificial legacy
        # fixtures without it retain the previous empty-owned-row semantics.
        rows, audit = api().read_archive(archive([source_row()]), owner, settings())
        self.assertEqual(rows, [])
        self.assertEqual(audit['ownership_excluded_count'], 1)

    def test_decode_falls_back_to_cp1252_only_for_decode_failure(self):
        rows, audit = api().read_archive(archive([source_row(Market_and_Exchange_Names='Artificiel €')], encoding='cp1252'), ownership(), settings())
        self.assertEqual(rows[0]['name'], 'Artificiel €')
        self.assertEqual(audit['encoding'], 'cp1252')

    def test_bad_date_or_missing_code_stops_dataset_even_outside_owned_years(self):
        for changes in [dict(As_of_Date_In_Form_YYMMDD='notdate'),
                        dict(As_of_Date_In_Form_YYMMDD='991231'),
                        dict(As_of_Date_In_Form_YYMMDD='100230'),
                        dict(CFTC_Contract_Market_Code=' '),
                        dict(As_of_Date_In_Form_YYMMDD='090106', CFTC_Contract_Market_Code='')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                api().read_archive(archive([source_row(**changes)]), ownership(), settings())

    def test_invalid_counts_remain_attached_to_named_code(self):
        for value in ['', '-1', '1.5', 'nan', 'inf', 'True', '1,2']:
            with self.subTest(value=value):
                rows, audit = api().read_archive(archive([source_row(Open_Interest_All=value)]), ownership(), settings())
                self.assertEqual(rows[0]['code'], '001234')
                self.assertTrue(rows[0]['errors'])
                self.assertIsNone(rows[0]['open_interest'])
                self.assertEqual(audit['invalid_count_rows'], 1)

    def test_zero_fraction_counts_require_true_clarification_and_convert_exactly(self):
        raw = archive([source_row(Open_Interest_All='1,200.000000',
            Dealer_Positions_Long_All='200.0', Dealer_Positions_Short_All='350.00')])
        old_rows, _ = api().read_archive(raw, ownership(), settings())
        self.assertIsNone(old_rows[0]['open_interest'])
        self.assertTrue(old_rows[0]['errors'])
        design = settings()
        design['count_notation_clarification'] = {'accepted_zero_fraction': True}
        rows, audit = api().read_archive(raw, ownership(), design)
        self.assertEqual((rows[0]['open_interest'], rows[0]['long'], rows[0]['short'], rows[0]['net']),
                         (1200, 200, 350, -150))
        self.assertIs(type(rows[0]['open_interest']), int)
        self.assertEqual(audit['invalid_count_rows'], 0)
        # Above 2**53: a float-round-and-cast implementation loses this integer.
        raw = archive([source_row(Open_Interest_All='9,007,199,254,740,993.000000')])
        rows, _ = api().read_archive(raw, ownership(), design)
        self.assertEqual(rows[0]['open_interest'], 9007199254740993)

    def test_zero_fraction_enable_flag_is_exact_boolean_true(self):
        raw = archive([source_row(Open_Interest_All='0.000000')])
        for flag in [False, None, 1, 'true', 'True']:
            with self.subTest(flag=flag):
                design = settings()
                design['count_notation_clarification'] = {'accepted_zero_fraction': flag}
                rows, _ = api().read_archive(raw, ownership(), design)
                self.assertIsNone(rows[0]['open_interest'])
        design['count_notation_clarification']['accepted_zero_fraction'] = True
        rows, _ = api().read_archive(raw, ownership(), design)
        self.assertEqual(rows[0]['open_interest'], 0)
        self.assertIs(type(rows[0]['open_interest']), int)

    def test_zero_fraction_clarification_never_rounds_or_accepts_other_count_notations(self):
        design = settings()
        design['count_notation_clarification'] = {'accepted_zero_fraction': True}
        for value in ['1.000001', '-1.0', '-0.0', '+1.0', '1e3', '1.0e3', '',
                      'NA', 'nan', 'inf', '.0', '1.', '1,2.0', '1.00.0']:
            with self.subTest(value=value):
                rows, audit = api().read_archive(archive([source_row(Open_Interest_All=value)]), ownership(), design)
                self.assertIsNone(rows[0]['open_interest'])
                self.assertTrue(rows[0]['errors'])
                self.assertEqual(audit['invalid_count_rows'], 1)

    def test_missing_required_or_duplicate_header_is_dataset_failure(self):
        row = source_row(); del row['Contract_Units']
        with self.assertRaises(ValueError):
            api().read_archive(archive([row], HEADERS[:-1]), ownership(), settings())
        with self.assertRaises(ValueError):
            api().read_archive(archive([source_row()], HEADERS+['Contract_Units']), ownership(), settings())

    def test_zip_must_contain_exactly_one_table_and_never_extracts_paths(self):
        for payload in [b'not a zip', archive([source_row()], members=[('second.csv', b'a\n1\n')])]:
            with self.subTest(payload_size=len(payload)), self.assertRaises(ValueError):
                api().read_archive(payload, ownership(), settings())
        rows, audit = api().read_archive(archive([source_row()], members=[('README.md', b'artificial')]), ownership(), settings())
        self.assertEqual(len(rows), 1)
        self.assertEqual(audit['payload'], 'artificial.txt')

    def test_monday_holiday_and_plus_code_are_preserved(self):
        rows, _ = api().read_archive(archive([source_row(As_of_Date_In_Form_YYMMDD='100104', CFTC_Contract_Market_Code='13874+')]), ownership(), settings())
        self.assertEqual((rows[0]['position_date'], rows[0]['week'], rows[0]['code']),
                         ('2010-01-04', '2010-01-04', '13874+'))


class UniverseTests(unittest.TestCase):
    def test_selection_is_ranked_by_total_oi_and_literal_code_ties(self):
        rows = series('000002', 200)+series('000003', 100)+series('000001', 200)
        before = deepcopy(rows); d = settings(); d['top_contracts'] = 2
        result = api().select_universe(rows, d)
        self.assertEqual(result['selected'], ['000001', '000002'])
        self.assertEqual(result['status'], 'AVAILABLE')
        self.assertEqual(result['calendar'][0], '2010-01-04')
        self.assertEqual(len(result['calendar']), 660)
        self.assertEqual(result['arrays_by_code']['000001']['position'][:2], [-10., -10.])
        self.assertEqual(result['arrays_by_code']['000001']['model_dates'][:2], ['2010-01-04', '2010-01-11'])
        self.assertEqual(result['arrays_by_code']['000001']['actual_dates'][:2], ['2010-01-05', '2010-01-12'])
        self.assertEqual(rows, before)
        self.assertTrue(all(c['eligible'] for c in result['contracts']))
        self.assertEqual({c['code']: c['mean_open_interest'] for c in result['contracts']},
                         {'000001': 200., '000002': 200., '000003': 100.})

    def test_calendar_is_full_range_not_union_and_no_gap_is_compressed(self):
        rows = series(); del rows[1]
        got = api().select_universe(rows, settings())
        self.assertEqual(len(got['calendar']), 660)
        self.assertEqual(got['calendar'][1], '2010-01-11')
        self.assertEqual(got['selected'], [])
        self.assertEqual(got['status'], 'UNAVAILABLE')
        self.assertIn('MISSING_WEEK', got['contracts'][0]['reasons'])

    def test_latest_week_is_global_before_prefix_or_count_filtering(self):
        rows = series()+series('13874+', 900, count=661)
        rows[-1].update(open_interest=None, errors=['INVALID_OPEN_INTEREST'])
        got = api().select_universe(rows, settings())
        self.assertEqual(len(got['calendar']), 661)
        self.assertEqual(got['selected'], [])
        self.assertIn('MISSING_WEEK', {c['code']: c for c in got['contracts']}['001234']['reasons'])

    def test_identical_or_monday_tuesday_same_week_duplicates_disqualify(self):
        for monday in [False, True]:
            with self.subTest(monday=monday):
                rows = series(); extra = deepcopy(rows[0])
                if monday: extra['position_date'] = extra['week']
                rows.append(extra)
                got = api().select_universe(rows, settings())
                self.assertEqual(got['selected'], [])
                self.assertIn('DUPLICATE_WEEK', got['contracts'][0]['reasons'])

    def test_exchange_and_unit_changes_disqualify_but_frozen_cosmetics_do_not(self):
        for field, changed, reason in [('exchange', 'ICE', 'UNSTABLE_EXCHANGE'),
                                       ('units', 'OTHER CONTRACT', 'UNSTABLE_UNITS'),
                                       ('exchange', '', 'INVALID_EXCHANGE'),
                                       ('units', '', 'INVALID_UNITS')]:
            with self.subTest(field=field, changed=changed):
                rows = series(); rows[1][field] = changed
                got = api().select_universe(rows, settings())
                self.assertEqual(got['selected'], [])
                self.assertIn(reason, got['contracts'][0]['reasons'])
        rows = series(); rows[0]['exchange'] = ' cme '; rows[0]['units'] = ' contracts  '
        self.assertEqual(api().select_universe(rows, settings())['selected'], ['001234'])

    def test_prefix_exclusion_is_broader_than_documented_plus_code(self):
        rows = []
        for code in ['138741', '20974+', '124600', '000099']: rows += series(code)
        got = api().select_universe(rows, settings())
        self.assertEqual(got['selected'], ['000099'])
        self.assertEqual(sum('KNOWN_SCOPE_CHANGE_PREFIX' in c['reasons'] for c in got['contracts']), 3)

    def test_bad_count_or_inconsistent_net_fails_whole_code_without_row_drop(self):
        for changes in [dict(open_interest=None, errors=['INVALID_OPEN_INTEREST']),
                        dict(long=-1), dict(net=900), dict(short=1.5), dict(open_interest=True)]:
            with self.subTest(changes=changes):
                rows = series(); rows[10].update(changes)
                got = api().select_universe(rows, settings())
                self.assertEqual(got['selected'], [])
                self.assertIn('INVALID_COUNTS', got['contracts'][0]['reasons'])

    def test_names_are_audited_in_spans_but_never_joined_or_filtered(self):
        rows = series()
        for r in rows[2:]: r['name'] = 'Renamed label'
        got = api().select_universe(rows, settings())
        self.assertEqual(got['selected'], ['001234'])
        spans = got['contracts'][0]['name_spans']
        self.assertEqual(len(spans), 2)
        self.assertEqual(spans[0]['first_date'], '2010-01-05')
        self.assertEqual(spans[0]['last_date'], '2010-01-12')
        self.assertEqual(spans[1]['first_date'], '2010-01-19')

    def test_short_history_is_unavailable_and_fewer_than_twenty_stays_fewer(self):
        got = api().select_universe(series(count=10), settings())
        self.assertEqual(got['selected'], [])
        self.assertIn('INSUFFICIENT_HISTORY', got['contracts'][0]['reasons'])
        self.assertEqual(api().select_universe(series(), settings())['selected'], ['001234'])

    def test_raw_bad_global_dates_or_missing_code_raise_instead_of_shortening_calendar(self):
        for changes in [dict(code=''), dict(position_date='bad'), dict(position_date='2099-01-05')]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                rows = series(); rows[0].update(changes)
                api().select_universe(rows, settings())

    def test_bad_week_is_code_ineligible_without_clock_repair(self):
        for value in ['2010-01-11', None, [], 'not-a-week']:
            with self.subTest(value=value):
                rows = series(); rows[0]['week'] = value
                got = api().select_universe(rows, settings())
                self.assertEqual(got['selected'], [])
                self.assertIn('INVALID_WEEK', got['contracts'][0]['reasons'])

    def test_empty_data_is_unavailable_with_json_native_outputs(self):
        got = api().select_universe([], settings())
        self.assertEqual((got['calendar'], got['selected'], got['contracts']), ([], [], []))
        self.assertEqual(got['status'], 'UNAVAILABLE')
        json.dumps(got, allow_nan=False)


class SplitTests(unittest.TestCase):
    def test_split_indices_have_six_unissued_origins_and_no_incomplete_labels(self):
        got = api().split_indices(700, H=6)
        self.assertEqual({k: got[k] for k in ['validation_first', 'validation_last', 'evaluation_first', 'evaluation_last']},
                         dict(validation_first=376, validation_last=427, evaluation_first=434, evaluation_last=693))
        self.assertEqual((got['validation_n'], got['evaluation_n'], got['unissued_gap_n']), (52, 260, 6))
        self.assertEqual(got['validation_last']+6, got['evaluation_first']-1)
        self.assertEqual(got['evaluation_last']+6, 699)

    def test_invalid_or_too_short_clock_raises(self):
        for n,h in [(True,6), (0,6), (323,6), (700,0), (700,True), (700,6.0)]:
            with self.subTest(n=n,h=h), self.assertRaises(ValueError):
                api().split_indices(n,H=h)


if __name__ == '__main__': unittest.main()
