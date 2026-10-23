import importlib,importlib.util,unittest
import numpy as np
from pathlib import Path
import tempfile
from unittest.mock import patch
from conditional_study import score_predictions,summarize_scores

class WP4Admission(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_wp4'),'WP4 primary admission API missing')
        return importlib.import_module('v6_wp4')
    def fixture(self):
        ids=np.arange(10,20);y=np.arange(10.)+1;f=np.zeros(10)
        q=dict(origins=ids,peak=y,floor=f,capacity=y-.1)
        ref=dict(origins=ids,peak=y,floor=f,capacity=y+.5)
        a=summarize_scores(score_predictions(y,q['capacity'],f,ids));b=summarize_scores(score_predictions(y,ref['capacity'],f,ids))
        import study_core
        d=score_predictions(y,q['capacity'],f,ids).pinball-score_predictions(y,ref['capacity'],f,ids).pinball
        row=dict(origin_count='10',first_source_index='10',last_source_index='19',mean_pinball_left=str(a['mean_pinball']),mean_pinball_right=str(b['mean_pinball']),mean_pinball_difference=str(study_core.stable_mean(d)))
        return q,ref,row,d
    def test_primary_vector_reproduces_fixed_old_paired_row(self):
        q,r,row,d=self.fixture();got=self.api().admit_primary(q,r,row)
        np.testing.assert_array_equal(got,d)
    def test_analysis_metadata_merges_equal_keys_without_duplicate_kwargs(self):
        a=self.api();z=a.merge_analysis(dict(horizon=6,analysis_status='post-result / exploratory'),dict(horizon=6,analysis_status='post-result / exploratory',groups=[]))
        self.assertEqual(z['groups'],[])
        with self.assertRaises(ValueError):a.merge_analysis(dict(horizon=6),dict(horizon=24))
    def test_resource_failures_preserve_two_sources_and_four_na_slots(self):
        a=self.api();import v6_worker as w
        contrasts=['fx_hourly-h6-QR2880-minus-rolling_F720','nyfed_weekly-h6-QR260-minus-frozen_F260']
        freeze=dict(files={},contrast_slots=[c+':'+name for c in contrasts for name in ('joint_GW','group_heterogeneity')])
        class G:
            def __call__(self):pass
            def summary(self):return dict(peak_rss_bytes=1,maximum_observed_os_threads=1,elapsed_seconds=.1)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);paired=root/'results/revision-20261022/paired-comparisons.csv';paired.parent.mkdir(parents=True);paired.write_text('contrast_id\n')
            with patch.object(w,'ROOT',root),patch.object(w,'PUBLIC',root/'public'),patch.object(w,'read_json',return_value=freeze),patch.object(w,'check_execution_freeze'),patch.object(w,'sha',return_value='0'*64),patch.object(w,'Guard',G),patch.object(w,'setup',side_effect=RuntimeError('RESOURCE_RSS')),patch.object(a.signal,'alarm'),patch.object(a.signal,'signal'):
                a.main()
            import json
            out=json.loads((root/'public/wp4-states.json').read_text())
            self.assertEqual(len(out['rows']),2);self.assertEqual(len(out['ranking']),4)
            self.assertEqual(out['raw_na_count'],4)
            self.assertTrue(all(r['bookkeeping_p']==1 for r in out['ranking']))

    def test_reference_target_or_paired_direction_change_stops(self):
        q,r,row,d=self.fixture();r['peak']=r['peak']+1
        with self.assertRaises(ValueError):self.api().admit_primary(q,r,row)
        q,r,row,d=self.fixture();row['mean_pinball_difference']=str(-float(row['mean_pinball_difference']))
        with self.assertRaises(ValueError):self.api().admit_primary(q,r,row)
if __name__=='__main__':unittest.main()
