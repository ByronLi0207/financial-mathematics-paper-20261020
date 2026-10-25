"""Constructed document/readback controls only; no research calculations."""
import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).with_name('wp7_supplement_numeric_audit.py')
spec = importlib.util.spec_from_file_location('supp_guard',PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class Controls(unittest.TestCase):
    def test_exact_migration_is_not_numeric_set_membership(self):
        with self.assertRaises(ValueError):
            guard.exact('Old loss 42 and 47.', 'Old loss 47 and 42.','mutation')

    def test_typed_field_not_numeric_equivalence(self):
        self.assertFalse(guard.identical(42,42.0))
        self.assertFalse(guard.identical(True,1))

    def test_fraction_preserves_pairing(self):
        self.assertEqual(guard.render('fraction',[47,48])[0],'47/48')
        self.assertNotEqual(guard.render('fraction',[48,47])[0],'47/48')

    def test_scientific_format_and_missing_are_explicit(self):
        self.assertEqual(guard.render('pvalue',[0.0000025]),('2.50e-06',r'$2.50\times10^{-6}$'))
        self.assertEqual(guard.render('pvalue',[None]),('NA','NA'))
        self.assertEqual(guard.render('root',[None,True]),('Left-censored','Left-censored'))

    def test_tagged_rows_cannot_be_swapped_deleted_or_duplicated(self):
        rows=[{'row_tag':'first','tokens':['A','$47$','$48$']},{'row_tag':'second','tokens':['B','$42$','$43$']}]
        a=r'A & $47$ & $48$ \\ % v9-row:first'
        b=r'B & $42$ & $43$ \\ % v9-row:second'
        guard.check_rows(a+'\n'+b,rows)
        for wrong in (b+'\n'+a,a,a+'\n'+b+'\n'+b):
            with self.subTest(wrong=wrong):
                with self.assertRaises(ValueError):guard.check_rows(wrong,rows)

    def test_unbound_digit_in_protocol_paragraph_is_rejected(self):
        expected='The seed entropy is 2026102492; P1 is 80 and P2 is 60.'
        guard.check_digits(expected,expected,'seed')
        for wrong in (expected.replace('2026102492','2026102493'),expected+' p=0.123'):
            with self.assertRaises(ValueError):guard.check_digits(wrong,expected,'seed')

    def test_duplicate_exact_passage_cannot_authorize_occurrence(self):
        with self.assertRaises(ValueError):guard.once('Loss 47. Loss 47.','Loss 47.','duplicate')

    def test_unknown_formatter_fails_closed(self):
        with self.assertRaises(ValueError):guard.render('freeform', [47])


if __name__=='__main__':unittest.main(verbosity=2)
