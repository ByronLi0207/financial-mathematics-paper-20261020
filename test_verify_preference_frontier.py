"""Synthetic arithmetic and custody checks for the independent verifier."""
import copy
import csv
import hashlib
import importlib.util
import io
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import tempfile
import unittest


class IndependentFrontierTests(unittest.TestCase):
    def verifier(self):
        self.assertIsNotNone(importlib.util.find_spec('verify_preference_frontier'),
                             'independent frontier verifier must exist')
        import verify_preference_frontier
        return verify_preference_frontier

    @staticmethod
    def fixture():
        # A=2a, B=2-2a, T=1 touches the envelope only at a=1/2.
        return dict(methods={
            'A':dict(u_token='2',v_token='0'),
            'B':dict(u_token='0',v_token='2'),
            'T':dict(u_token='1',v_token='1'),
            'D':dict(u_token='3',v_token='3')},
            frontier=dict(regions=[
                dict(left='0/1',right='1/2',methods=['A']),
                dict(left='1/2',right='1/1',methods=['B'])],
                points=[dict(alpha='0/1',methods=['A']),
                        dict(alpha='1/2',methods=['A','B','T']),
                        dict(alpha='1/1',methods=['B'])]),
            pairs=[
                dict(left='A',right='B',relation='crosses',equality_alpha='1/2'),
                dict(left='A',right='D',relation='left_dominates',equality_alpha=None),
                dict(left='A',right='T',relation='crosses',equality_alpha='1/2'),
                dict(left='B',right='D',relation='left_dominates',equality_alpha=None),
                dict(left='B',right='T',relation='crosses',equality_alpha='1/2'),
                dict(left='D',right='T',relation='right_dominates',equality_alpha=None)],
            dominated_methods=['D'],winners_at_095=['B'])

    def test_inequality_intersection_retains_point_only_winner(self):
        v=self.verifier()
        self.assertEqual(v.feasible_intervals(self.fixture()['methods']), {
            'A':(Fraction(0),Fraction(1,2)),
            'B':(Fraction(1,2),Fraction(1)),
            'T':(Fraction(1,2),Fraction(1,2)), 'D':None})
        v.verify_group(self.fixture())

    def test_missing_boundary_tie_is_rejected(self):
        group=self.fixture();group['frontier']['points'][1]['methods']=['A','B']
        with self.assertRaises(ValueError):self.verifier().verify_group(group)

    def test_missing_pair_and_duplicate_pair_are_rejected(self):
        for duplicate in (False,True):
            group=self.fixture()
            if duplicate:group['pairs'].append(copy.deepcopy(group['pairs'][0]))
            else:group['pairs'].pop()
            with self.assertRaises(ValueError):self.verifier().verify_group(group)

    def test_wrong_crossing_wrong_domination_and_open_winner_are_rejected(self):
        for field in ('crossing','dominated','winner'):
            group=self.fixture()
            if field=='crossing':group['pairs'][0]['equality_alpha']='1/3'
            if field=='dominated':group['dominated_methods']=['D','T']
            if field=='winner':group['frontier']['regions'][0]['methods']=['A','T']
            with self.assertRaises(ValueError):self.verifier().verify_group(group)

    def test_identical_lines_and_endpoint_only_ties(self):
        v=self.verifier()
        self.assertEqual(v.pair_relation(('0','1'),('0','2')),
                         ('left_dominates','1/1'))
        self.assertEqual(v.pair_relation(('0.10','2'),('0.1','2')),
                         ('identical',None))
        self.assertEqual(v.feasible_intervals({
            'A':dict(u_token='0',v_token='1'),
            'B':dict(u_token='0',v_token='2'),
            'C':dict(u_token='0.0',v_token='1.0')}),
            {'A':(Fraction(0),Fraction(1)),
             'B':(Fraction(1),Fraction(1)),
             'C':(Fraction(0),Fraction(1))})

    def test_nonfinite_negative_boolean_and_fraction_tokens_rejected(self):
        for token in ('NaN','Infinity','-1','True','1/2','1e99999'):
            with self.assertRaises(ValueError):self.verifier().decimal_value(token)

    def test_json_duplicate_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            self.verifier().read_json_bytes(b'{"schema_version":1,"schema_version":1}')

    @staticmethod
    def complete_fixture(root):
        # All lines are the identical literal 2-alpha: every method ties.
        methods=['AR1_REPLAY','I','KNN','QR','SCALED_KNN','frozen_F','frozen_K','frozen_S']
        cells=[('fx_hourly','USD',w,h,6625,24) for w in (720,2880) for h in (6,24)]
        cells += [('nyfed_weekly','USD millions',w,h,277,13) for w in (52,260) for h in (6,24)]
        entries=[];groups=[]
        header=['source','native_unit','horizon','window','method','origin_count','refit_step',
                'mean_positive_overrun','mean_unused_allowance','mean_pinball','strict_breach_count','status']
        for sample in ('full','sparse'):
            rows_by_kind={'core':[],'ar':[],'rank':[]}
            for source,unit,window,horizon,full_count,step in cells:
                count=full_count if sample=='full' else (full_count-1)//(horizon+1)+1
                group=dict(sample=sample,source=source,horizon=horizon,window=window,
                    native_unit=unit,origin_count=count,
                    methods={name:dict(u_token='1.0',v_token='2.0',mean_pinball='1.05',
                                       strict_breach_count=1) for name in methods},
                    frontier=dict(regions=[dict(left='0/1',right='1/1',methods=methods)],
                        points=[dict(alpha='0/1',methods=methods),dict(alpha='1/1',methods=methods)]),
                    pairs=[dict(left=l,right=r,relation='identical',equality_alpha=None)
                           for l,r in combinations(methods,2)],dominated_methods=[],winners_at_095=methods)
                groups.append(group)
                for method in methods:
                    kind='ar' if method=='AR1_REPLAY' else 'rank' if method=='I' else 'core'
                    rows_by_kind[kind].append([source,unit,horizon,window,method,count,step,
                                               '1.0','2.0','1.05',1,'COMPLETE'])
                if source=='fx_hourly' and window==720:
                    rows_by_kind['core'].append([source,unit,horizon,window,
                        'rolling_F' if horizon==6 else 'rolling_S',count,1,'1.0','2.0','1.05',1,'COMPLETE'])
            tail='summary' if sample=='full' else 'nonoverlap'
            paths={'core':f'evaluation-{tail}.csv',
                   'ar':f'ar1-replay/ar1-{tail}.csv','rank':f'rank-ablation/{tail}.csv'}
            for kind,name in paths.items():
                path='results/revision-20261022/'+name;stream=io.StringIO(newline='')
                writer=csv.writer(stream);writer.writerow(header);writer.writerows(rows_by_kind[kind])
                raw=stream.getvalue().encode();target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(raw);entries.append(dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
        result=dict(schema_version=1,groups=groups,headline_comparisons=[
            dict(id=name,left=dict(u_token='1.0',v_token='2.0'),right=dict(u_token='1.0',v_token='2.0'),
                 relation='identical',equality_alpha=None)
            for name in ('fx_h6_primary','fx_h6_matched','fx_h24_legacy','treasury_h6_primary')])
        return dict(input_files=entries),result

    def test_complete_source_inventory_and_decimal_custody(self):
        v=self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);freeze,result=self.complete_fixture(root)
            selected,all_rows,identities=v.read_sources(root,freeze)
            self.assertEqual(len(selected),128);self.assertEqual(len(identities),6)
            self.assertEqual(v.verify_result(result,selected,all_rows),dict(
                groups=16,methods=128,pairs=448,regions=16,points=32,headline_comparisons=4))
            changed=copy.deepcopy(result);changed['groups'][0]['methods']['QR']['u_token']='1.00'
            with self.assertRaises(ValueError):v.verify_result(changed,selected,all_rows)
            changed=copy.deepcopy(result);changed['groups'].pop()
            with self.assertRaises(ValueError):v.verify_result(changed,selected,all_rows)
            changed=copy.deepcopy(result);changed['headline_comparisons'].pop()
            with self.assertRaises(ValueError):v.verify_result(changed,selected,all_rows)

    def test_same_byte_source_hash_and_duplicate_cell_rejected(self):
        v=self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);freeze,_=self.complete_fixture(root)
            entry=freeze['input_files'][0];path=root/entry['path'];raw=path.read_bytes()
            path.write_bytes(raw+b'\n')
            with self.assertRaises(ValueError):v.read_sources(root,freeze)
            duplicate=raw+raw.splitlines(keepends=True)[1];path.write_bytes(duplicate)
            entry.update(bytes=len(duplicate),sha256=hashlib.sha256(duplicate).hexdigest())
            with self.assertRaises(ValueError):v.read_sources(root,freeze)

    def test_existing_output_is_preserved_without_source_reads(self):
        v=self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);output=root/'receipt.json';output.write_bytes(b'preserve')
            with self.assertRaises(ValueError):v.verify_files(root/'missing.json',output,root=root)
            self.assertEqual(output.read_bytes(),b'preserve')


if __name__=='__main__':unittest.main()
