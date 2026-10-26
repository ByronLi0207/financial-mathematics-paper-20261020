"""Synthetic byte-only replay preparation; no financial arrays or execution."""
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ReplaySetupTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('v6_replay_setup'), 'replay helper absent')
        self.api=importlib.import_module('v6_replay_setup')
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name).resolve()
        self.root=self.base/'repo';self.root.mkdir()
        self.private=self.base/'private';self.private.mkdir()
        self.target=self.base/'new-replay'
        self.tracked=[]
        self.inventory={
            'source_inputs':{'synthetic':self.private_entry('.scratch/source.csv',b'synthetic source')},
            'original_cells':[{'traces':[dict(self.private_entry('.scratch/original.npz',b'container byte pin'),
                 manifest_path='.scratch/old/public/manifest.json',manifest_sha256=digest(b'{"old":true}'))]}],
            'panel_source_inputs':[self.private_entry('.scratch/panel.csv',b'panel source')],
            'panel_cells':[self.private_entry('.scratch/panel.npz',b'panel container')],
            'six_csv_checks':[]}
        for n in range(6):
            content=f'audit-{n}'.encode();relative=f'.scratch/audit/{n}.csv';archived=f'results/old/{n}.csv'
            self.write(self.private,relative,content);self.write(self.root,archived,content)
            self.tracked.append(archived)
            self.inventory['six_csv_checks'].append(dict(reproduced_path=relative,archived_path=archived,
                expected_sha256=digest(content),reproduced_matches_manifest=True))
        self.write(self.root,'worker.py',b'# inert synthetic worker\n');self.tracked.append('worker.py')
        self.write(self.root,'results/revision-20261023/v6/wp2/evaluation.json',b'old result')
        self.write(self.root,'.scratch/not-needed',b'not copied')
        self.write(self.root,'.bak/worker.py',b'not copied')
        self.tracked.extend(['results/revision-20261023/v6/wp2/evaluation.json','.scratch/not-needed','.bak/worker.py'])
        self.make_metadata()
        self.tracked_patch=patch.object(self.api,'_tracked_paths',return_value=self.tracked)
        self.tracked_patch.start();self.addCleanup(self.tracked_patch.stop)

    def write(self,base,relative,content):
        p=base/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
        return p

    def private_entry(self,path,content):
        self.write(self.private,path,content)
        return dict(path=path,sha256=digest(content),bytes=len(content))

    def make_metadata(self,extra=None):
        inventory=json.dumps(self.inventory,sort_keys=True).encode()
        members={'.scratch/revision-v6/input-inventory.json':inventory,
                 '.scratch/old/public/manifest.json':b'{"old":true}'}
        if extra:members.update(extra)
        archive=self.root/'protocol/revision-v6/replay-metadata.zip';archive.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive,'w') as z:
            for path,data in members.items():z.writestr(path,data)
        manifest=dict(version=1,zip_sha256=digest(archive.read_bytes()),
            inventory_member='.scratch/revision-v6/input-inventory.json',
            members=[dict(path=p,bytes=len(b),sha256=digest(b)) for p,b in members.items()],scope='synthetic')
        self.write(self.root,'protocol/revision-v6/replay-metadata-manifest.json',json.dumps(manifest).encode())
        self.write(self.root,'protocol/revision-v6/design-freeze.json',json.dumps({'private_input_inventory_sha256':digest(inventory)}).encode())
        for p in ('protocol/revision-v6/replay-metadata.zip','protocol/revision-v6/replay-metadata-manifest.json','protocol/revision-v6/design-freeze.json'):
            if p not in self.tracked:self.tracked.append(p)

    def test_check_is_read_only_and_prepare_copies_only_admitted_inputs(self):
        before={str(p.relative_to(self.base)):p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        report=self.api.check_inputs(self.private,root=self.root)
        self.assertEqual(report['status'],'ADMITTED');self.assertEqual(report['six_csv_count'],6)
        self.assertFalse(self.target.exists())
        self.assertEqual(before,{str(p.relative_to(self.base)):p.read_bytes() for p in self.base.rglob('*') if p.is_file()})
        # A regenerated private-root receipt cannot replace the frozen ZIP bytes.
        self.write(self.private,'.scratch/old/public/manifest.json',b'{"new":true}')
        self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertEqual((self.target/'.scratch/old/public/manifest.json').read_bytes(),b'{"old":true}')
        self.assertEqual((self.target/'.scratch/original.npz').read_bytes(),b'container byte pin')
        self.assertEqual((self.target/'worker.py').read_bytes(),b'# inert synthetic worker\n')
        self.assertFalse((self.target/'results/revision-20261023/v6').exists())
        self.assertFalse((self.target/'.scratch/not-needed').exists())
        self.assertFalse((self.target/'.bak').exists())

    def test_unsafe_zip_paths_never_create_a_target_or_outside_file(self):
        for path in ('../outside','/absolute','a/../../outside','a\\outside'):
            with self.subTest(path=path):
                self.make_metadata({path:b'bad'})
                with self.assertRaises(self.api.ReplaySetupError):
                    self.api.prepare_replay(self.target,self.private,root=self.root)
                self.assertFalse(self.target.exists());self.assertFalse((self.base/'outside').exists())

    def test_wrong_whole_container_hash_fails_before_target_creation(self):
        (self.private/'.scratch/original.npz').write_bytes(b'same semantic? no: different bytes')
        with self.assertRaisesRegex(self.api.ReplaySetupError,'HASH_MISMATCH'):
            self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertFalse(self.target.exists())

    def test_missing_six_csv_fails_even_if_inventory_claims_success(self):
        self.inventory['six_csv_checks'][3]['reproduced_path']='.scratch/missing.csv'
        self.make_metadata()
        with self.assertRaisesRegex(self.api.ReplaySetupError,'MISSING_INPUT'):
            self.api.check_inputs(self.private,root=self.root)
        self.assertFalse(self.target.exists())

    def test_existing_target_is_never_overwritten(self):
        self.target.mkdir();marker=self.target/'keep';marker.write_bytes(b'untouched')
        with self.assertRaisesRegex(self.api.ReplaySetupError,'TARGET_EXISTS'):
            self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertEqual(list(self.target.iterdir()),[marker]);self.assertEqual(marker.read_bytes(),b'untouched')

    def test_zip_fingerprint_and_frozen_inventory_are_both_required(self):
        archive=self.root/'protocol/revision-v6/replay-metadata.zip'
        archive.write_bytes(archive.read_bytes()+b'changed')
        with self.assertRaisesRegex(self.api.ReplaySetupError,'ZIP_HASH_MISMATCH'):
            self.api.check_inputs(self.private,root=self.root)
        self.make_metadata()
        self.write(self.root,'protocol/revision-v6/design-freeze.json',b'{"private_input_inventory_sha256":"0000000000000000000000000000000000000000000000000000000000000000"}')
        with self.assertRaisesRegex(self.api.ReplaySetupError,'FROZEN_INVENTORY_MISMATCH'):
            self.api.check_inputs(self.private,root=self.root)

    def test_private_symlink_escape_is_rejected_without_outside_writes(self):
        outside=self.base/'outside';outside.write_bytes(b'container byte pin')
        self.inventory['original_cells'][0]['traces'][0]['path']='.scratch/linked.npz'
        (self.private/'.scratch/linked.npz').symlink_to(outside)
        self.make_metadata()
        with self.assertRaisesRegex(self.api.ReplaySetupError,'SYMLINK'):
            self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertFalse(self.target.exists());self.assertEqual(outside.read_bytes(),b'container byte pin')

    def test_member_hash_and_manifest_binding_are_not_only_zip_fingerprint(self):
        p=self.root/'protocol/revision-v6/replay-metadata-manifest.json'
        manifest=json.loads(p.read_text());manifest['members'][1]['sha256']='0'*64;p.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(self.api.ReplaySetupError,'MEMBER_HASH_MISMATCH'):
            self.api.check_inputs(self.private,root=self.root)

    def test_every_six_csv_is_hashed_and_not_admitted_by_success_flags(self):
        last=self.inventory['six_csv_checks'][-1]
        self.write(self.private,last['reproduced_path'],b'wrong sixth CSV')
        with self.assertRaisesRegex(self.api.ReplaySetupError,'HASH_MISMATCH'):
            self.api.check_inputs(self.private,root=self.root)

    def test_required_inputs_and_metadata_cannot_fill_reserved_output_slots(self):
        trace=self.inventory['original_cells'][0]['traces'][0]
        trace['path']='results/revision-20261023/v6/required-input.npz'
        self.write(self.private,trace['path'],b'container byte pin');self.make_metadata()
        with self.assertRaisesRegex(self.api.ReplaySetupError,'RESERVED_DESTINATION'):
            self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertFalse(self.target.exists())

    def test_admitted_metadata_fingerprint_cannot_be_rebased_before_copy(self):
        def change_archive_after_admission(root):
            archive=root/self.api.ARCHIVE
            archive.write_bytes(archive.read_bytes()+b'changed after admission')
            return self.tracked
        with patch.object(self.api,'_tracked_paths',side_effect=change_archive_after_admission):
            with self.assertRaisesRegex(self.api.ReplaySetupError,'METADATA_CHANGED'):
                self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertFalse(self.target.exists())

    def test_metadata_members_cannot_fill_reserved_output_slots(self):
        trace=self.inventory['original_cells'][0]['traces'][0]
        trace['path']='.scratch/original.npz'
        trace['manifest_path']='results/revision-20261023/v6/receipt.json'
        # Rebuild the ZIP explicitly so the metadata destination itself is the
        # forbidden path, while all inventory and manifest hashes remain valid.
        inventory=json.dumps(self.inventory,sort_keys=True).encode()
        self.make_metadata()
        archive=self.root/self.api.ARCHIVE
        members={self.api.INVENTORY:inventory,trace['manifest_path']:b'{"old":true}'}
        with zipfile.ZipFile(archive,'w') as z:
            for name,data in members.items():z.writestr(name,data)
        manifest=json.loads((self.root/self.api.MANIFEST).read_text())
        manifest['zip_sha256']=digest(archive.read_bytes())
        manifest['members']=[dict(path=p,bytes=len(b),sha256=digest(b)) for p,b in members.items()]
        (self.root/self.api.MANIFEST).write_text(json.dumps(manifest))
        with self.assertRaisesRegex(self.api.ReplaySetupError,'RESERVED_DESTINATION'):
            self.api.prepare_replay(self.target,self.private,root=self.root)
        self.assertFalse(self.target.exists())


if __name__=='__main__':unittest.main(verbosity=2)
