"""Toy aggregate tests of the frozen v12 screens; no financial data reads."""
import importlib
import importlib.util
import unittest


CODES = ['044601','043602','042601','045601','020601','099741','1170E1',
         '097741','096742','095741','090741','232741','33874A','240743',
         '092741','098662','112741']


def row(family,key,window,tau=.95,method='QR33',period='original',
        validation_n=52,relative=10.,penalty=.1,status='COMPLETE',horizon=6):
    return dict(cell_id=f'{family}-{key}-{window}-{tau}-{method}-{period}-{validation_n}',
                family=family,source_key=key,period=period,horizon=horizon,window=window,
                validation_n=validation_n,tau=tau,method=method,status=status,
                selected_penalty=penalty,reference_loss=100.,
                actual_loss=100.+relative,relative_loss_pct=relative,
                strict_breach_count=2,n=260)


def validation_rows(codes=CODES):
    return [row('cftc',key,w,method=method,validation_n=v,
                relative=10. if v==52 else 5.,penalty=.1 if v==52 else 'inf')
            for method in ('QR33','QR4') for w in (52,260)
            for key in codes for v in (52,156)]


def tau_rows():
    result = []
    for tau in (.99,.90):
        for index,key in enumerate(CODES):
            for w in (52,260):
                result.append(row('cftc',key,w,tau=tau,
                    relative=10. if len(result)%37<29 else -5.))
        for period in ('original','early2015'):
            result.append(row('fx','fx_hourly',2880,tau=tau,period=period,
                              validation_n=1440,relative=-10.))
        result.append(row('bill','PDPOSGS-B',260,tau=tau,relative=2.))
    return result


class SummaryTests(unittest.TestCase):
    def call(self, name, *args):
        self.assertIsNotNone(importlib.util.find_spec('v12_summaries'),
                             'new pure summary implementation is required')
        module = importlib.import_module('v12_summaries')
        self.assertTrue(callable(getattr(module,name,None)), 'missing summary API: '+name)
        return getattr(module,name)(*args)

    def test_f2_exact_five_point_boundary_and_strict_infinity_increase(self):
        summary = self.call('summarize_validation',validation_rows(),CODES)
        self.assertEqual(summary['counts']['planned'],136)
        self.assertEqual(summary['V1']['status'],'SUPPORTED')
        self.assertEqual(summary['V2']['status'],'SUPPORTED')
        detail = summary['methods']['QR33']['by_window']['52']
        self.assertEqual(detail['eligible_contracts'],17)
        self.assertEqual(detail['median_difference_pct_points'],-5.)
        self.assertEqual(detail['infinity_fraction_by_validation'],{'52':0.,'156':1.})

    def test_f2_qr4_failure_does_not_replace_primary_qr33(self):
        rows = validation_rows()
        for entry in rows:
            if entry['method']=='QR4' and entry['validation_n']==156:
                entry['relative_loss_pct']=20.
                entry['actual_loss']=120.
        result = self.call('summarize_validation',rows,CODES)
        self.assertEqual(result['V1']['status'],'SUPPORTED')
        self.assertEqual(result['methods']['QR4']['V1']['status'],'NOT_SUPPORTED')

    def test_f2_infinity_fraction_tie_fails_v2(self):
        rows = validation_rows()
        for entry in rows:
            entry['selected_penalty']='inf'
        result = self.call('summarize_validation',rows,CODES)
        self.assertEqual(result['V2']['status'],'NOT_SUPPORTED')

    def test_f2_one_missing_pair_retains_17_denominator_and_descriptive_pairs(self):
        rows = validation_rows()
        rows = [r for r in rows if not (r['method']=='QR33' and r['source_key']==CODES[0]
                and r['window']==52 and r['validation_n']==156)]
        result = self.call('summarize_validation',rows,CODES)
        self.assertEqual(result['V1']['status'],'UNDETERMINED')
        self.assertEqual(result['V2']['status'],'UNDETERMINED')
        detail = result['methods']['QR33']['by_window']['52']
        self.assertEqual(detail['eligible_contracts'],17)
        self.assertEqual(detail['complete_pair_count'],16)
        self.assertEqual(detail['descriptive_complete_pairs']['median_difference_pct_points'],-5.)
        self.assertEqual(result['counts']['missing'],1)

    def test_f2_complete_failure_in_one_window_dominates_other_missing_window(self):
        rows = validation_rows()
        for entry in rows:
            if entry['method']=='QR33' and entry['window']==52 and entry['validation_n']==156:
                entry['relative_loss_pct']=8.
                entry['actual_loss']=108.
        rows = [r for r in rows if not (r['method']=='QR33' and r['window']==260
                and r['source_key']==CODES[0] and r['validation_n']==156)]
        result = self.call('summarize_validation',rows,CODES)
        self.assertEqual(result['V1']['status'],'NOT_SUPPORTED')
        self.assertEqual(result['V1']['by_window']['52'],'NOT_SUPPORTED')
        self.assertEqual(result['V1']['by_window']['260'],'UNDETERMINED')

    def test_f2_uses_difference_of_medians_not_median_of_paired_differences(self):
        codes = CODES[:3]
        rows = validation_rows(codes)
        for entry in rows:
            values = [0.,100.,101.] if entry['validation_n']==52 else [95.,96.,200.]
            entry['relative_loss_pct']=values[codes.index(entry['source_key'])]
            entry['actual_loss']=100.+entry['relative_loss_pct']
        result = self.call('summarize_validation',rows,codes)
        detail = result['methods']['QR33']['by_window']['52']
        self.assertEqual(detail['median_relative_loss_by_validation'],{'52':100.,'156':96.})
        self.assertEqual(detail['median_difference_pct_points'],-4.)
        self.assertEqual(detail['descriptive_complete_pairs']['median_paired_change_pct_points'],95.)
        self.assertEqual(result['V1']['status'],'NOT_SUPPORTED')

    def test_f2_eligibility_is_pre_gate_and_not_selected_from_completed_rows(self):
        eligibility = [dict(source_key=key,eligible=i!=0,
                            reason=None if i else 'INSUFFICIENT_HISTORY')
                       for i,key in enumerate(CODES)]
        rows = validation_rows(CODES[1:])
        result = self.call('summarize_validation',rows,eligibility)
        self.assertEqual(result['counts']['planned'],128)
        self.assertEqual(result['eligible_contract_count'],16)
        self.assertEqual(result['excluded_contracts'][0]['source_key'],CODES[0])
        self.assertEqual(result['V1']['status'],'SUPPORTED')

    def test_duplicate_or_nonfinite_complete_input_is_unknown_not_best_row(self):
        rows = validation_rows()
        duplicate = dict(rows[1],relative_loss_pct=-90.,actual_loss=10.)
        rows.append(duplicate)
        rows[3]['relative_loss_pct']=float('nan')
        result = self.call('summarize_validation',rows,CODES)
        self.assertEqual(result['V1']['status'],'UNDETERMINED')
        self.assertEqual(result['counts']['duplicate_slots'],1)
        self.assertEqual(result['counts']['invalid_complete'],1)

    def test_f3_q1_fixed_29_of_34_and_q2_two_period_conjunction(self):
        result = self.call('summarize_tau',tau_rows())
        self.assertEqual(result['counts']['planned'],74)
        self.assertEqual(result['Q1']['status'],'SUPPORTED')
        self.assertEqual(result['Q1']['support_count'],29)
        self.assertEqual(result['Q1']['denominator'],34)
        self.assertEqual(result['Q2']['status'],'SUPPORTED')
        self.assertEqual(result['Q2']['support_count'],2)

    def test_f3_q1_unknown_bounds_can_support_or_leave_uncertain(self):
        rows = tau_rows()
        cftc = [r for r in rows if r['family']=='cftc' and r['tau']==.99]
        cftc[28]['status']='NOT_RUN_RESOURCE_LIMIT'
        uncertain = self.call('summarize_tau',rows)
        self.assertEqual(uncertain['Q1']['status'],'UNDETERMINED')
        self.assertEqual(uncertain['Q1']['support_count'],28)
        self.assertEqual(uncertain['Q1']['unknown_count'],1)
        self.assertEqual(uncertain['Q1']['support_fraction_bounds'],[28/34,29/34])
        cftc[28]['status']='COMPLETE'
        for entry in cftc[29:]:
            entry['status']='FAILED_NUMERICAL'
        bounded = self.call('summarize_tau',rows)
        self.assertEqual(bounded['Q1']['status'],'SUPPORTED')
        self.assertEqual(bounded['Q1']['unknown_count'],5)

    def test_f3_strict_ties_do_not_count_as_f_or_regression_wins(self):
        rows = tau_rows()
        cftc = [r for r in rows if r['family']=='cftc' and r['tau']==.99]
        cftc[28]['relative_loss_pct']=0.
        cftc[28]['actual_loss']=100.
        fx = next(r for r in rows if r['family']=='fx' and r['tau']==.99)
        fx['relative_loss_pct']=0.
        fx['actual_loss']=100.
        result = self.call('summarize_tau',rows)
        self.assertEqual(result['Q1']['status'],'NOT_SUPPORTED')
        self.assertEqual(result['Q1']['tie_count'],1)
        self.assertEqual(result['Q2']['status'],'NOT_SUPPORTED')

    def test_f3_completed_q2_failure_dominates_missing_other_period(self):
        rows = tau_rows()
        fx = [r for r in rows if r['family']=='fx' and r['tau']==.99]
        fx[0]['relative_loss_pct']=2.
        fx[0]['actual_loss']=102.
        fx[1]['status']='NOT_RUN_RESOURCE_LIMIT'
        result = self.call('summarize_tau',rows)
        self.assertEqual(result['Q2']['status'],'NOT_SUPPORTED')
        self.assertEqual(result['Q2']['unknown_count'],1)

    def test_f3_tau90_cannot_rescue_missing_tau99_and_all_slots_remain(self):
        rows = [r for r in tau_rows() if r['tau']==.90]
        result = self.call('summarize_tau',rows)
        self.assertEqual(result['Q1']['status'],'UNDETERMINED')
        self.assertEqual(result['Q1']['denominator'],34)
        self.assertEqual(result['Q2']['status'],'UNDETERMINED')
        self.assertEqual(result['counts']['planned'],74)
        self.assertEqual(result['counts']['missing'],37)
        self.assertEqual(len(result['slot_inventory']),74)
        self.assertTrue(result['tau90_descriptive_only'])

    def test_group_tables_preserve_planned_resource_and_failure_counts(self):
        rows = tau_rows()
        rows[0]['status']='FAILED_RESOURCE'
        rows[1]['status']='FAILED_NUMERICAL'
        result = self.call('summarize_tau',rows)
        self.assertEqual(result['counts']['resource'],1)
        self.assertEqual(result['counts']['failed'],2)
        group = next(g for g in result['descriptive_groups']
                     if g['family']=='cftc' and g['window']==52 and g['tau']==.99)
        self.assertEqual(group['counts']['planned'],17)
        self.assertEqual(group['counts']['resource'],1)
        self.assertEqual(group['counts']['complete'],16)
        self.assertNotIn('pooled_native_mean_loss',group)


if __name__=='__main__':
    unittest.main()
