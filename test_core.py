"""Wholly artificial behavioral oracles for the frozen core contract.

Run only in the parent-serialized, thread-limited numerical worker.
Each expected literal below comes from the prospective V01--V12 hand matrix.
"""

from dataclasses import replace
from fractions import Fraction
import math
import unittest

import numpy as np

try:
    import study_core as core
except ModuleNotFoundError as exc:
    if exc.name != "study_core":
        raise
    core = None


MENU = (
    ("main", 6, 720, 19, 20, 685),
    ("h12", 12, 720, 19, 20, 685),
    ("h24", 24, 720, 19, 20, 685),
    ("n480", 6, 480, 19, 20, 457),
    ("n1440", 6, 1440, 19, 20, 1369),
    ("tau90", 6, 720, 9, 10, 649),
    ("tau99", 6, 720, 99, 100, 714),
)


class CoreOracles(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(core, "study_core implementation is absent: frozen artificial behaviors are not yet implemented")

    def cell(self, H=1, n=3, num=3, den=4, rank=3, name="tiny"):
        return core.CellSpec(name, H, n, num, den, rank)

    def issue(self, values, cell=None, t=None):
        cell = self.cell() if cell is None else cell
        position = np.asarray(values, dtype=np.float64)
        t = len(position) - 1 if t is None else t
        cache = core.build_label_cache(position, cell.horizon)
        labels = core.mature_window(cache, t, cell)
        issued = core.issue_capacities(t, float(position[t]), labels, labels.origins, cell)
        return issued, cache, labels

    def full_fixture(self):
        position = np.zeros(1500, dtype=np.float64)
        position[[1245, 1345]] = 4
        position[[1447, 1453, 1465]] = [2, 3, 5]
        times = np.datetime64("2016-01-01T00:00:00", "us") + (np.arange(1500) - 1445) * np.timedelta64(1, "h")
        cells = [core.CellSpec(*row) for row in MENU]
        origins = core.common_origins(times, cells, "2016-01-01T00:00:00")
        cache_by_h = {h: core.build_label_cache(position, h) for h in (6, 12, 24)}
        results = {}
        for cell in cells:
            cache = cache_by_h[cell.horizon]
            batch = core.forecast_cell(position, cache, origins, cell)
            evaluation = core.evaluate_caps(cache.peak[origins], batch, cell.tau)
            results[cell.cell_id] = (cell, batch, evaluation, cache)
        return position, times, cells, origins, results

    def test_v01_peak_includes_current_and_distinguishes_radius(self):
        cache = core.build_label_cache(np.array([-3., 1., -2.]), 2)
        self.assertEqual(len(cache.peak), 1)
        self.assertEqual(cache.origins.tolist(), [0])
        self.assertEqual(cache.label_end.tolist(), [2])
        self.assertEqual(cache.peak.tolist(), [3.])
        self.assertEqual(cache.headroom.tolist(), [0.])
        self.assertEqual(cache.lower_increment.tolist(), [0.])
        self.assertEqual(cache.upper_increment.tolist(), [4.])
        self.assertEqual(cache.radius.tolist(), [4.])
        # An endpoint-only target would miss the middle spike.
        spike = core.build_label_cache(np.array([0., 9., 0.]), 2)
        self.assertEqual(spike.peak.tolist(), [9.])

    def test_v02_exact_ranks_ties_and_generic_unavailable_rank(self):
        for n, num, den, want in ((720,9,10,649), (720,19,20,685), (720,99,100,714), (480,19,20,457), (1440,19,20,1369)):
            self.assertEqual(core.exact_rank(n, num, den), want)
            self.assertEqual(core.order_statistic(np.arange(n, 0, -1, dtype=float), want), float(want))
        self.assertEqual(core.order_statistic(np.array([0., 0., 2.]), 2), 0.)
        self.assertEqual(core.exact_rank(3, 9, 10), 4)
        self.assertEqual(core.order_statistic(np.array([0., 0., 2.]), 4), math.inf)
        with self.assertRaises(ValueError):
            self.cell(num=9, den=10, rank=4)
        with self.assertRaises(ValueError):
            self.cell(rank=2)
        with self.assertRaises(ValueError):
            self.cell(H=0)
        with self.assertRaises(ValueError):
            core.order_statistic(np.array([1., np.nan]), 1)

    def test_v03_prefix_capacities_and_exact_mature_pool(self):
        cell = self.cell(H=2, num=1, den=2, rank=2)
        issued, _, labels = self.issue([0, 1, -1, 2, 0], cell)
        self.assertEqual(labels.origins.tolist(), [0,1,2])
        self.assertEqual(labels.label_end.tolist(), [2,3,4])
        self.assertEqual(labels.headroom.tolist(), [1.,1.,1.])
        self.assertEqual(labels.radius.tolist(), [1.,2.,3.])
        np.testing.assert_array_equal(issued.capacities, [1,2,2,2,0])
        full = core.build_label_cache(np.array([0.,1.,-1.,2.,0.,0.,0.]), 2)
        immature = core.mature_window(full, 5, cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(4, 0., immature, immature.origins, cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(5, 0., labels, labels.origins, cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(4, 0., labels, np.array([0,1,3]), cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(4, 0., replace(labels, horizon=1), labels.origins, cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(4, 0., replace(labels, window=2), labels.origins, cell)
        with self.assertRaises(ValueError):
            core.issue_capacities(4, 0., replace(labels, label_end=np.array([2,3,3])), labels.origins, cell)

    def test_v04_future_suffix_changes_target_but_cannot_change_issue(self):
        cell = self.cell(H=2, num=1, den=2, rank=2)
        prefix = [0,1,-1,2,0]
        short, _, _ = self.issue(prefix, cell)
        low, low_cache, _ = self.issue(prefix + [0,0], cell, t=4)
        high, high_cache, _ = self.issue(prefix + [100,-100], cell, t=4)
        for issued in (short, low, high):
            np.testing.assert_array_equal(issued.capacities, [1,2,2,2,0])
        self.assertEqual(low_cache.peak[4], 0.)
        self.assertEqual(high_cache.peak[4], 100.)
        before = [getattr(high_cache, name).copy() for name in ("peak","headroom","lower_increment","upper_increment","radius","origins","label_end")]
        position = np.array(prefix + [100,-100], dtype=float)
        for t in (5,4):
            labels = core.mature_window(high_cache,t,cell)
            core.issue_capacities(t,float(position[t]),labels,labels.origins,cell)
        for name, want in zip(("peak","headroom","lower_increment","upper_increment","radius","origins","label_end"), before):
            np.testing.assert_array_equal(getattr(high_cache,name),want)
            self.assertFalse(getattr(high_cache,name).flags.writeable)
        with self.assertRaises(ValueError):
            high_cache.headroom[0] = 8

    def test_v05_v06_full_menu_shared_origins_and_strict_hand_differences(self):
        _, _, _, origins, results = self.full_fixture()
        self.assertEqual(origins.tolist(), list(range(1445,1476)))
        self.assertEqual((origins[:3] % 6).tolist(), [5,0,1])
        self.assertEqual([int(np.sum(origins % 6 == j)) for j in range(6)], [5,5,5,5,5,6])
        self.assertEqual([results[c][2].peak[0] for c in ("main","h12","h24")], [2.,3.,5.])
        self.assertEqual([results[c][1].capacities[0,3] for c in ("main","h12","h24")], [0.,0.,4.])
        for j in range(4):
            self.assertEqual([results[c][1].capacities[0,j] for c in ("tau90","main","tau99")], [0.,0.,4.])
        self.assertTrue(core.validate_cross_cells(results))
        bad = dict(results)
        cell,batch,ev,cache = bad["h12"]
        bad["h12"] = (cell,replace(batch,origins=origins+1),ev,cache)
        with self.assertRaises(ValueError):
            core.validate_cross_cells(bad)

    def test_constant_nonzero_full_menu_has_zero_losses_and_null_severity(self):
        cells = [core.CellSpec(*row) for row in MENU]
        position = np.full(1500,5.)
        times = np.datetime64("2016-01-01","us") + (np.arange(1500)-1445)*np.timedelta64(1,"h")
        origins = core.common_origins(times,cells,"2016-01-01")
        for cell in cells:
            cache = core.build_label_cache(position,cell.horizon)
            batch = core.forecast_cell(position,cache,origins,cell)
            ev = core.evaluate_caps(cache.peak[origins],batch,cell.tau)
            np.testing.assert_array_equal(batch.capacities,np.full((31,5),5.))
            np.testing.assert_array_equal(ev.pinball,np.zeros((31,5)))
            rows, paired = core.summarize_cell(cell,batch,ev)
            self.assertEqual(paired["mean_pinball_difference"],0.)
            self.assertIsNone(paired["relative_difference_to_S"])
            self.assertEqual(paired["relative_difference_undefined_reason"],"ZERO_MEAN_LOSS_S")
            for row in rows:
                self.assertIsNone(row["conditional_mean_overrun"])
                self.assertEqual(row["conditional_overrun_undefined_reason"],"NO_STRICT_BREACHES")

    def test_v07_bidirectional_capacities_and_joined_future_loss_flips(self):
        cell = self.cell()
        for history, future, want_caps, want_losses, want_d in (
            ([6,4,2,0],1,[0,2,2,6,0],[.75,.25],.5),
            ([6,4,2,0],0,[0,2,2,6,0],[0.,.5],-.5),
            ([0,-4,-1,2],7,[6,5,6,4,2],[.75,1.5],-.75),
            ([0,-4,-1,2],2,[6,5,6,4,2],[1.,.75],.25),
        ):
            position=np.array(history+[future],dtype=float)
            cache=core.build_label_cache(position,1)
            batch=core.forecast_cell(position,cache,np.array([3]),cell)
            np.testing.assert_array_equal(batch.capacities[0],want_caps)
            ev=core.evaluate_caps(cache.peak[batch.origins],batch,cell.tau)
            np.testing.assert_array_equal(ev.pinball[0,:2],want_losses)
            _,paired=core.summarize_cell(cell,batch,ev)
            self.assertEqual(paired["mean_pinball_difference"],want_d)

    def test_v08_four_categories_keep_selected_allowance_rounding_collapse(self):
        B=float(2**53)
        fixtures=(
            ([5,5,5,5],self.cell(),"paired_scores_equal"),
            ([0,1,0,0],self.cell(),"scores_changed_allowances_equal"),
            ([0,-1,-2,B],self.cell(num=1,den=2,rank=2),"allowances_changed_capacities_equal"),
            ([6,4,2,0],self.cell(),"capacities_different"),
            ([0,-4,-1,2],self.cell(),"capacities_different"),
        )
        categories=[]
        directions=[]
        for values,cell,want in fixtures:
            issued,_,_=self.issue(values,cell)
            categories.append(issued.mechanism)
            self.assertEqual(issued.mechanism,want)
            directions.append(int(np.sign(issued.capacities[0]-issued.capacities[1])))
            if want=="allowances_changed_capacities_equal":
                np.testing.assert_array_equal(issued.selected_fs,[1.,0.])
                np.testing.assert_array_equal(issued.capacities[:2],[B,B])
                np.testing.assert_array_equal(issued.issued_extras[:2],[0.,0.])
        self.assertEqual([categories.count(x) for x in ("paired_scores_equal","scores_changed_allowances_equal","allowances_changed_capacities_equal","capacities_different")],[1,1,1,2])
        self.assertEqual([directions.count(x) for x in (-1,0,1)],[1,3,1])

    def test_v09_direct_error_loss_tie_and_p0_overrun(self):
        caps=np.array([[10.,14.,10.,14.,2.]])
        ev=core.evaluate_caps(np.array([11.]),caps,Fraction(3,4),origins=np.array([7]))
        np.testing.assert_array_equal(ev.errors[0,:2],[1.,-3.])
        np.testing.assert_array_equal(ev.pinball[0,:2],[.75,.75])
        self.assertEqual(ev.origins.tolist(),[7])
        ev=core.evaluate_caps(np.array([5.25]),np.full((1,5),2.),Fraction(3,4))
        self.assertEqual(ev.overrun[0,4],3.25)
        self.assertEqual(ev.pinball[0,4],39/16)
        self.assertTrue(ev.strict_breach[0,4])
        self.assertEqual(ev.unused[0,4],0.)
        zero=core.evaluate_caps(np.array([2.]),np.full((1,5),2.),Fraction(3,4))
        self.assertFalse(zero.strict_breach.any())

    def test_direct_stored_error_and_exact_separate_complement(self):
        # At B=2**53, subtracting the floor first need not match direct subtraction.
        B=float(2**53)
        peak=np.array([B+2.])
        caps=np.array([[B,B+2.,B,B+2.,B]])
        ev=core.evaluate_caps(peak,caps,Fraction(19,20))
        np.testing.assert_array_equal(ev.errors,[[2.,0.,2.,0.,2.]])
        # With a conceptual floor1, subtracting it from both sides first
        # rounds (2**54-1)-(2-1) back to 2**54; the direct error retains -2.
        large=float(2**54)
        direct=core.evaluate_caps(np.array([large]),np.full((1,5),2.),Fraction(3,4))
        self.assertEqual(direct.errors[0,0],large-2.)
        self.assertEqual(core.evaluate_caps(np.array([0.]),np.full((1,5),1.),Fraction(19,20)).pinball[0,0],float(Fraction(1,20)))
        with self.assertRaises(ValueError):
            core.evaluate_caps(np.array([[1.]]),np.ones((1,5)),Fraction(3,4))
        with self.assertRaises(ValueError):
            core.evaluate_caps(np.array([1.,2.]),np.ones((1,5)),Fraction(3,4))
        with self.assertRaises(ValueError):
            core.evaluate_caps(np.array([np.inf]),np.ones((1,5)),Fraction(3,4))

    def test_raw_strict_and_aux_near_events_are_separate(self):
        eps=np.finfo(float).eps
        caps=np.full((2,5),1.)
        ev=core.evaluate_caps(np.array([1.+eps,1.+64*eps]),caps,Fraction(3,4))
        self.assertTrue(ev.strict_breach.all())
        self.assertFalse(ev.aux_breach[0].any())
        self.assertTrue(ev.aux_breach[1].all())
        self.assertTrue(ev.near_event_boundary[0].all())
        self.assertFalse(ev.near_event_boundary[1].any())

    def test_upper_geometry_tolerance_retains_small_discrepancy_but_rejects_material(self):
        cell=self.cell(num=1,den=2,rank=2)
        _,_,labels=self.issue([0,1,0,0],cell)
        tiny=np.nextafter(1.,2.)
        tolerant=replace(labels,headroom=np.full(3,tiny),radius=np.ones(3))
        issued=core.issue_capacities(3,0.,tolerant,tolerant.origins,cell)
        self.assertEqual(issued.capacities[0],tiny)
        self.assertGreater(issued.capacities[0],issued.capacities[2])
        with self.assertRaises(ValueError):
            bad=replace(labels,headroom=np.full(3,2.),radius=np.ones(3))
            core.issue_capacities(3,0.,bad,bad.origins,cell)
        with self.assertRaises(ValueError):
            bad=replace(labels,headroom=np.full(3,-np.finfo(float).eps))
            core.issue_capacities(3,0.,bad,bad.origins,cell)

    def test_moderate_sign_reversal_and_eight_scale_preserve_capacities(self):
        values=np.array([0.,1.,-1.,2.,0.])
        cell=self.cell(H=2,num=1,den=2,rank=2)
        direct,_,_=self.issue(values,cell)
        signed,_,_=self.issue(-values,cell)
        scaled,_,_=self.issue(values*8.,cell)
        np.testing.assert_array_equal(direct.capacities,signed.capacities)
        np.testing.assert_array_equal(scaled.capacities,[8.,16.,16.,16.,0.])

    def test_horizon_nonorders_remain_admissible_for_f_s_r(self):
        t=800
        main=core.CellSpec(*MENU[0])
        h12=core.CellSpec(*MENU[1])
        first=np.ones(825)
        for start in (200,300,400,500,600,789):
            first[start:start+6]=0.
        result=[]
        for cell in (main,h12):
            batch=core.forecast_cell(first,core.build_label_cache(first,cell.horizon),np.array([t]),cell)
            result.append(batch.capacities[0,:2].tolist())
        self.assertEqual(result,[[2.,2.],[1.,1.]])
        second=np.zeros(825)
        for start in (200,300,400,500,600,789):
            second[start:start+6]=-1.
            second[start+6:start+12]=1.
        result=[]
        for cell in (main,h12):
            batch=core.forecast_cell(second,core.build_label_cache(second,cell.horizon),np.array([t]),cell)
            result.append(batch.capacities[0,[1,2]].tolist())
        self.assertEqual(result[0],[3.,3.])
        self.assertTrue(all(value<=2. for value in result[1]))

    def test_diagnostics_keeps_915_rows_and_uniformly_suppresses_sparse_groups(self):
        position,times,_,origins,results=self.full_fixture()
        cell,batch,ev,_=results["main"]
        rows=core.diagnostics_main(times,position,origins,cell,batch,ev,"2016-01-01")
        self.assertEqual(len(rows),915)
        by_group={}
        for row in rows:
            by_group.setdefault((row["panel"],row["group"]),[]).append(row)
        self.assertTrue(all(len(v)==61 for v in by_group.values()))
        expected={
            ("current_sign","negative"):0,("current_sign","zero"):28,("current_sign","positive"):3,
            ("development_magnitude_tercile","low"):28,("development_magnitude_tercile","middle"):0,("development_magnitude_tercile","high"):3,
            ("naive_origin_month","2016-01"):31,
            ("retrospective_gap_free_path","gap_free"):31,("retrospective_gap_free_path","has_gap"):0,
        }
        expected.update({("source_index_modulo_6",str(j)):(6 if j==5 else 5) for j in range(6)})
        for key,count in expected.items():
            for row in by_group[key]:
                self.assertEqual(row["origin_count"],count)
                if count<30:
                    self.assertIsNone(row["value"])
                    self.assertEqual(row["display_status"],"NO_ORIGINS" if count==0 else "BELOW_DISPLAY_MIN")
                    self.assertEqual(row["undefined_reason"],"NO_ORIGINS" if count==0 else "GROUP_BELOW_DISPLAY_MIN")
        self.assertTrue(all(r["display_status"]=="DISPLAYED" for r in by_group[("naive_origin_month","2016-01")]))

    def test_diagnostics_includes_empty_intermediate_calendar_month_and_future_gap(self):
        cell=self.cell(H=1,num=1,den=2,rank=2,name="main")
        times=np.array(["2015-12-01","2015-12-02","2015-12-03","2016-01-01","2016-03-01","2016-03-01T01:00:00"],dtype="datetime64[us]")
        position=np.full(6,5.)
        origins=np.array([3,4])
        cache=core.build_label_cache(position,1)
        batch=core.forecast_cell(position,cache,origins,cell)
        ev=core.evaluate_caps(cache.peak[origins],batch,cell.tau)
        rows=core.diagnostics_main(times,position,origins,cell,batch,ev,"2016-01-01")
        months={r["group"]:r["origin_count"] for r in rows if r["panel"]=="naive_origin_month"}
        self.assertEqual(months,{"2016-01":1,"2016-02":0,"2016-03":1})
        gaps={r["group"]:r["origin_count"] for r in rows if r["panel"]=="retrospective_gap_free_path"}
        self.assertEqual(gaps,{"gap_free":1,"has_gap":1})
        self.assertEqual(len(rows),61*17)

    def test_safe_summary_leaves_and_category_partitions(self):
        _,_,_,_,results=self.full_fixture()
        for cell,batch,ev,_ in results.values():
            rows,paired=core.summarize_cell(cell,batch,ev)
            self.assertEqual(len(rows),5)
            self.assertEqual([r["method_id"] for r in rows],["F","S","R","L","P0"])
            self.assertEqual(paired["f_lower_count"]+paired["equal_capacity_count"]+paired["f_higher_count"],31)
            self.assertEqual(sum(paired[k] for k in ("paired_scores_equal_count","scores_changed_allowances_equal_count","allowances_changed_capacities_equal_count","capacities_different_count")),31)
            self.assertEqual(paired["equal_capacity_count"],sum(paired[k] for k in ("paired_scores_equal_count","scores_changed_allowances_equal_count","allowances_changed_capacities_equal_count")))
            for row in rows+[paired]:
                for value in row.values():
                    self.assertIn(type(value),(str,int,float,bool,type(None)))
                    if type(value) is float:
                        self.assertTrue(math.isfinite(value))

    def test_v10_exact_constant_mean_and_constant_profile(self):
        c=.1
        self.assertEqual(core.stable_mean(np.full(999,c)),c)
        with self.assertRaises(ValueError):
            core.stable_mean(np.array([]))
        progress=[]
        result=core.stationary_mean_profile(np.full(4,3.),[120,240,720,1440],999,20261020,lambda **kw:progress.append(kw))
        self.assertEqual(len(result.rows),4)
        for row in result.rows:
            for key in ("observed_mean_d","resampled_mean_average","resampled_mean_order25","resampled_mean_order975"):
                self.assertEqual(row[key],3.)
            self.assertEqual(row["resampled_mean_sd_ddof1"],0.)
            self.assertTrue(row["constant_input"])
            self.assertTrue(row["constant_shortcut_used"])
            self.assertEqual(row["expected_used_blocks"],1+3/row["ell"])
            self.assertEqual(result.replicate_means[row["ell"]].tolist(),[3.]*999)
        self.assertTrue(any(p.get("completed_replicates")==999 for p in progress))
        self.assertEqual(core.explicit_block_mean(np.array([1.,-1.,1.,-1.]),[(0,1)]*4),1.)

    def test_v11_explicit_blocks_wrap_truncate_and_do_not_prefix_cancel(self):
        d=np.array([2.,-1.,4.,0.])
        for route in ("slices","indices"):
            self.assertEqual(core.explicit_block_mean(d,[(3,3),(0,4)],route=route),.75)
            self.assertEqual(core.explicit_block_mean(d,[(2,9)],route=route),1.25)
            cancellation=np.array([float(2**53),1.,-float(2**53),1.])
            self.assertEqual(core.explicit_block_mean(cancellation,[(1,1)]*4,route=route),1.)
        self.assertTrue(core.check_explicit_block_equivalence(d,[(3,3),(0,4)]))
        with self.assertRaises(ValueError):
            core.explicit_block_mean(d,[(3,0)])
        with self.assertRaises(ValueError):
            core.explicit_block_mean(d,[(0,1)])

    def test_v12_replicate_summary_uses_own_center_and_exact_endpoint_ranks(self):
        row=core.summarize_replicates(np.arange(999.,0.,-1.),0.)
        self.assertEqual(row["observed_mean_d"],0.)
        self.assertEqual(row["resampled_mean_average"],500.)
        self.assertEqual(row["resampled_mean_order25"],25.)
        self.assertEqual(row["resampled_mean_order975"],975.)
        self.assertEqual(row["lower_rank"],25)
        self.assertEqual(row["upper_rank"],975)
        self.assertAlmostEqual(row["resampled_mean_sd_ddof1"],math.sqrt(83250),places=12)

    def test_stationary_draw_order_positive_lengths_and_one_stream_per_length(self):
        class TraceRng:
            def __init__(self):
                self.events=[]
            def integers(self,low,high):
                self.events.append(("start",low,high))
                return 0
            def geometric(self,p):
                self.events.append(("length",p))
                return 1
        fake=TraceRng()
        self.assertEqual(core.stationary_replicate(np.array([1.,-1.,1.,-1.]),120,fake),1.)
        self.assertEqual(fake.events,[("start",0,4),("length",1/120)]*4)
        d=np.array([1.,-1.,1.,-1.])
        a=core.stationary_mean_profile(d,[120,240],999,20261020)
        b=core.stationary_mean_profile(d,[240,120],999,20261020)
        self.assertFalse(a.constant_input)
        self.assertFalse(a.constant_shortcut_used)
        for ell in (120,240):
            np.testing.assert_array_equal(a.replicate_means[ell],b.replicate_means[ell])

    def test_checkpoint_keywords_are_safe_and_forecast_boundary_is_reported(self):
        cell=self.cell(H=1,num=1,den=2,rank=2)
        position=np.full(105,5.)
        cache=core.build_label_cache(position,1)
        calls=[]
        core.forecast_cell(position,cache,np.arange(3,104),cell,lambda **kw:calls.append(kw))
        self.assertEqual([r["completed_origins"] for r in calls],[100,101])
        for row in calls:
            self.assertEqual(set(row),{"stage","cell_id","completed_origins"})
            self.assertEqual(row["stage"],"forecast")
            self.assertTrue(all(type(v) in (str,int) for v in row.values()))


if __name__ == "__main__":
    unittest.main()
