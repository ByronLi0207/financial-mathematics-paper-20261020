import unittest,uuid
from pathlib import Path
from v3_revision import ROOT,write,backup_required

class WriteOwnership(unittest.TestCase):
    def test_backup_policy(self):
        self.assertFalse(backup_required(False,False,False))
        self.assertFalse(backup_required(True,True,False))
        self.assertFalse(backup_required(True,False,True))
        self.assertTrue(backup_required(True,False,False))
    def test_new_owned_file_rewrites_without_backup(self):
        p=ROOT/'.scratch/round2'/('writer-test-'+uuid.uuid4().hex+'.txt')
        write(p,'one\n');write(p,'two\n')
        self.assertEqual(p.read_text(),'two\n')
        self.assertFalse(list(p.parent.glob(p.name+'.bak*')))

if __name__=='__main__':unittest.main()
