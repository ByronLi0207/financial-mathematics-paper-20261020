"""Independent causal-feature and completed-pool fixtures; no financial data."""
import importlib.util
import math
import unittest
import numpy as np

if importlib.util.find_spec('conditional_features') is None:
    cf = None
else:
    import conditional_features as cf


class ConditionalFeatureTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(cf, 'conditional feature implementation is missing')

    @staticmethod
    def source(n=260):
        return np.arange(n,dtype=float)**2, np.datetime64('2020-01-06T13:00')+np.arange(n)*np.timedelta64(1,'h')

    def test_quadratic_path_has_exact_past_levels_and_transition_rms(self):
        x,t=self.source(); f=cf.build_features(x,t,short_scale=3,long_scale=5,nominal_gap_seconds=3600)
        row=f.values[200]
        np.testing.assert_array_equal(row[:25],[(200-j)**2 for j in range(25)])
        self.assertEqual(row[25],40000.)
        self.assertAlmostEqual(row[26],math.sqrt((395**2+397**2+399**2)/3))
        self.assertAlmostEqual(row[27],math.sqrt(sum(j*j for j in [391,393,395,397,399])/5))
        self.assertEqual(f.valid_from,24)
        self.assertFalse(f.values.flags.writeable)
        self.assertTrue(np.isnan(f.values[:24]).all())

    def test_future_positions_and_dates_do_not_change_current_features_or_scaler(self):
        x,t=self.source(); f1=cf.build_features(x,t,short_scale=24,long_scale=168,nominal_gap_seconds=3600)
        x2=x.copy();x2[221:]=1e10+np.arange(len(x)-221)
        t2=t.copy();t2[221:]+=np.timedelta64(7,'D')
        f2=cf.build_features(x2,t2,short_scale=24,long_scale=168,nominal_gap_seconds=3600)
        np.testing.assert_array_equal(f1.values[:221],f2.values[:221])
        a=cf.fit_feature_transform(f1.values[168:210]);b=cf.fit_feature_transform(f2.values[168:210])
        np.testing.assert_array_equal(a.mean,b.mean);np.testing.assert_array_equal(a.scale,b.scale)
        np.testing.assert_array_equal(cf.transform_features(f1.values[220:221],a),cf.transform_features(f2.values[220:221],b))

    def test_gap_flag_uses_only_just_observed_gap(self):
        x,t=self.source();t[100:]+=np.timedelta64(48,'h')
        f=cf.build_features(x,t,short_scale=3,long_scale=5,nominal_gap_seconds=3600)
        self.assertEqual(f.values[99,32],0);self.assertEqual(f.values[100,32],1);self.assertEqual(f.values[101,32],0)

    def test_weekday_and_hour_use_source_naive_clock(self):
        x,t=self.source();f=cf.build_features(x,t,short_scale=3,long_scale=5,nominal_gap_seconds=3600)
        # Source index35 is Wednesday2020-01-08 00:00, with Monday=0.
        self.assertAlmostEqual(f.values[35,28],0);self.assertAlmostEqual(f.values[35,29],1)
        self.assertAlmostEqual(f.values[35,30],math.sin(4*math.pi/7))
        self.assertAlmostEqual(f.values[35,31],math.cos(4*math.pi/7))

    def test_constant_columns_transform_to_zero_and_group_weights_are_declared(self):
        a=np.tile(np.arange(33,dtype=float),(30,1));fit=cf.fit_feature_transform(a)
        np.testing.assert_array_equal(cf.transform_features(a,fit),np.zeros_like(a))
        x=np.vstack([np.zeros(33),np.ones(33)]);fit=cf.fit_feature_transform(x)
        ordinary=cf.transform_features(x,fit);weighted=cf.transform_features(x,fit,nearest=True)
        np.testing.assert_allclose(weighted[:,:25],ordinary[:,:25]/5)
        np.testing.assert_allclose(weighted[:,26:32],ordinary[:,26:32]/math.sqrt(2))
        np.testing.assert_array_equal(weighted[:,25],ordinary[:,25])

    def test_repeated_float_calendar_constants_have_exact_zero_transform(self):
        # A Wednesday weekly source has repeated non-binary calendar constants.
        # np.std alone can report roundoff around 1e-15 for these exact repeats.
        for rows in (52,260):
            a=np.tile(np.sin(np.arange(33,dtype=float)),(rows,1))
            fit=cf.fit_feature_transform(a)
            np.testing.assert_array_equal(fit.mean,a[0])
            np.testing.assert_array_equal(fit.scale,np.ones(33))
            np.testing.assert_array_equal(cf.transform_features(a,fit),np.zeros_like(a))

    def test_completed_window_and_refit_schedule_have_no_unfinished_label(self):
        a=cf.completed_training_indices(100,6,52,minimum_feature_index=24)
        np.testing.assert_array_equal(a,np.arange(43,95))
        self.assertTrue(np.all(a+6<=100))
        self.assertEqual(cf.refit_origin(142,120,24),120);self.assertEqual(cf.refit_origin(144,120,24),144)
        with self.assertRaises(ValueError):cf.completed_training_indices(100,24,52,minimum_feature_index=26)

    def test_neighbors_break_distance_ties_by_recent_origin_and_keep_correct_rank(self):
        train=np.zeros((4,3));ids=np.array([10,20,30,40]);y=np.array([1.,2.,30.,40.])
        q,selected=cf.neighbor_quantile(train,np.zeros(3),y,ids,2,numerator=1,denominator=2)
        self.assertEqual(q,40.);np.testing.assert_array_equal(selected,[30,40])
        with self.assertRaises(ValueError):cf.neighbor_quantile(train,np.zeros(3),y,ids,1)

    def test_unsigned_origin_ties_do_not_wrap_at_zero(self):
        q,selected=cf.neighbor_quantile(np.zeros((3,2)),np.zeros(2),
            np.array([100.,10.,20.]),np.array([0,1,2],dtype=np.uint64),2,numerator=1,denominator=2)
        np.testing.assert_array_equal(selected,[1,2]);self.assertEqual(q,20.)

    def test_distance_overflow_does_not_turn_into_a_false_recency_tie(self):
        with self.assertRaises(ValueError):
            cf.neighbor_quantile(np.array([[1e200],[2e200]]),np.zeros(1),
                np.array([1.,2.]),np.array([1,2]),1,numerator=1,denominator=2)

    def test_positive_response_scale_uses_only_supplied_training_rows(self):
        self.assertEqual(cf.response_scale(np.array([0.,2.,4.]),np.array([3.,6.,9.])),2.)
        self.assertEqual(cf.response_scale(np.zeros(3),np.array([3.,6.,9.])),6e-6)
        self.assertGreater(cf.response_scale(np.zeros(3),np.zeros(3)),0)

    def test_response_mean_overflow_stops_instead_of_returning_infinite_scale(self):
        with self.assertRaises(ValueError):
            cf.response_scale(np.array([1e308,1e308]),np.zeros(2))

    def test_nonfinite_chronology_and_inadequate_history_fail_closed(self):
        x,t=self.source();x[100]=np.nan
        with self.assertRaises(ValueError):cf.build_features(x,t,short_scale=3,long_scale=5,nominal_gap_seconds=3600)
        x,t=self.source();t[100]=t[99]
        with self.assertRaises(ValueError):cf.build_features(x,t,short_scale=3,long_scale=5,nominal_gap_seconds=3600)
        with self.assertRaises(ValueError):cf.fit_feature_transform(np.array([[np.nan]*33]))
        with self.assertRaises(ValueError):cf.completed_training_indices(10,6,20,minimum_feature_index=24)

if __name__=='__main__':unittest.main()
