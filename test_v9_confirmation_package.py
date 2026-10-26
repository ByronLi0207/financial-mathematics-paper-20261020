"""Packaging tests over constructed files only; no forecasts or DGP draws."""
import importlib.util
from pathlib import Path
import hashlib,json,tarfile
import pytest

@pytest.fixture
def package():
 path=Path(__file__).parent/'notes/revision-v9/package_wp2.py'
 if not path.exists():pytest.fail('WP2 package code not implemented',pytrace=False)
 spec=importlib.util.spec_from_file_location('v9_wp2_package',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def test_member_paths_and_bytes_survive_sanitized_archive(package,tmp_path):
 source=tmp_path/'source';source.mkdir();(source/'unit.json').write_text('{"negative": -1.25}\n')
 (source/'sub').mkdir();(source/'sub'/'sample.npz').write_bytes(b'constructed-data')
 archive=tmp_path/'bundle.tar.gz';index=tmp_path/'members.csv'
 receipt=package.archive_source(source,archive,index)
 assert receipt['members']==2 and receipt['mismatches']==0
 with tarfile.open(archive,'r:gz') as t:
  for m in t:
   assert t.extractfile(m).read()==(source/m.name).read_bytes()
   assert m.uname=='' and m.gname=='' and m.uid==0 and m.gid==0

def test_archive_refuses_overwrite_and_symlink_source(package,tmp_path):
 source=tmp_path/'source';source.mkdir();(source/'x').write_text('x')
 archive=tmp_path/'bundle.tar.gz';index=tmp_path/'members.csv';archive.write_bytes(b'preserved')
 with pytest.raises(FileExistsError):package.archive_source(source,archive,index)
 assert archive.read_bytes()==b'preserved'
 (source/'linked').symlink_to(source/'x')
 with pytest.raises(ValueError,match='symlink'):package.archive_source(source,tmp_path/'other.tar.gz',tmp_path/'other.csv')
