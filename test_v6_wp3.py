import importlib,importlib.util,unittest
import numpy as np

class WP3Tests(unittest.TestCase):
    def api(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_wp3'),'WP3 aggregation API missing')
        return importlib.import_module('v6_wp3')
    def test_all_slots_and_unavailable_medians_are_retained(self):
        a=self.api();cells=[]
        for j in range(56):
            cells.append(dict(cell_id='c'+str(j),source='synthetic',horizon=1,window=20,native_unit='synthetic',original=j<8))
        def load(cell):
            return dict(origins=np.arange(10,30),floor=np.zeros(20),peak=np.tile([1.,3.],10),F=np.ones(20)*2,QR=np.ones(20)*1.5,KNN=np.ones(20)*2 if cell['original'] else None,proof={})
        z,curves=a.aggregate(cells,load)
        self.assertEqual(len(z['method_rows']),112);self.assertEqual(len(z['comparisons']),224)
        self.assertEqual(z['na_method_count'],48)
        self.assertEqual(z['family_n'],224)
        self.assertEqual(sum(r['status']=='NA_CELL' for r in z['comparisons']),96)
        self.assertTrue(all(r['bookkeeping_p']==1 for r in z['comparisons'] if r['status']=='NA_CELL'))
    def test_target_floor_geometry_and_duplicate_cells_stop(self):
        a=self.api();cell=dict(cell_id='c',source='synthetic',horizon=1,window=20,native_unit='synthetic',original=False)
        def load(_):return dict(origins=np.arange(10,30),floor=np.ones(20)*2,peak=np.ones(20),F=np.ones(20)*2,QR=np.ones(20)*3,KNN=None,proof={})
        with self.assertRaises(ValueError):a.aggregate([cell]*56,load)
if __name__=='__main__':unittest.main()
