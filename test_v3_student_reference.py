"""Independent Cauchy/t2 checks for the bounded numerical reference auditor."""
import math,unittest
from v3_student_reference import student_angle_tail,readback

class IndependentStudentReference(unittest.TestCase):
    def test_closed_cauchy_and_t2_answers(self):
        for t in [0.,.1,1.,5.,20.]:
            cauchy=1. if t==0 else 2/math.pi*math.atan(1/t)
            root=math.sqrt(t*t+2);t2=2/(root*(root+t))
            self.assertAlmostEqual(student_angle_tail(t,1,256),cauchy,delta=1e-12)
            self.assertAlmostEqual(student_angle_tail(-t,1,256),cauchy,delta=1e-12)
            self.assertAlmostEqual(student_angle_tail(t,2,256),t2,delta=1e-12)
    def test_domain_is_bounded_to_audit_scope(self):
        for t,df in [(float('nan'),2),(33,2),(1,0),(1,10001)]:
            with self.assertRaises(ValueError):student_angle_tail(t,df,128)
    def test_scalar_rows_and_mismatch(self):
        rows=[dict(contrast_id='a',status='OK',n='2',hln_t='1',hln_p='.5'),dict(contrast_id='na',status='IDENTICAL_LOSSES',n='2',hln_t='',hln_p='')]
        report=readback(rows)
        self.assertEqual((report['checked_rows'],report['skipped_rows']),(1,1))
        rows[0]['hln_p']='.4'
        with self.assertRaisesRegex(AssertionError,'reference disagreement'):readback(rows)

if __name__=='__main__':unittest.main()
