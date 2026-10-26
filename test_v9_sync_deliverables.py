"""Two output-contract integration regressions, using constructed documents only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parent
STEMS=('manuscript','supplement','extended-v9-technical','title-page')


@pytest.fixture
def constructed_writer(tmp_path,monkeypatch):
    spec=importlib.util.spec_from_file_location('constructed_v9_sync',ROOT/'notes/revision-v9/sync_deliverables.py')
    writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
    delivery=tmp_path/'submission-jof';delivery.mkdir()
    notes=tmp_path/'notes/revision-v9';notes.mkdir(parents=True)
    (delivery/'generated').mkdir()
    (delivery/'generated/body.tex').write_text('Constructed recursive source.\n')
    for stem in STEMS:
        title=r'\begin{center}\Large\bfseries Constructed document title\end{center}' if stem=='manuscript' else stem
        child='\n'+r'\input{generated/body.tex}' if stem=='manuscript' else ''
        (delivery/(stem+'.tex')).write_text(r'\documentclass{article}'+'\n'+r'\begin{document}'+title+child+r'\end{document}'+'\n')
        (delivery/(stem+'.pdf')).write_bytes(b'%PDF-constructed\n'+stem.encode()+b'\n%%EOF\n')
    for name,content in {'main.tex':r'\input{manuscript.tex}', 'references.bib':'% Constructed bibliography\n',
        'README.md':'Constructed README\n','AUTHOR-TODO.md':'Constructed author fields\n','cover-letter.md':'Constructed letter\n'}.items():
        (delivery/name).write_text(content)
    monkeypatch.setattr(writer,'ROOT',tmp_path)
    monkeypatch.setattr(writer,'DELIVERY',delivery)
    monkeypatch.setattr(writer,'STEMS',STEMS)
    receipt=notes/'constructed-sync-receipt.json'
    monkeypatch.setattr(sys,'argv',['sync_deliverables.py','--receipt',str(receipt.relative_to(tmp_path))])
    return writer,tmp_path,delivery,receipt


def test_fresh_receipt_preserves_three_source_snapshots_and_four_pdf_aliases(constructed_writer):
    writer,root,delivery,receipt=constructed_writer
    writer.main()
    assert receipt.is_file(), 'The requested notes receipt must not be shadowed by a source-snapshot target'
    result=json.loads(receipt.read_text())
    assert result['status']=='PASS'
    assert result['package']=='submission-jof/overleaf-package.zip'
    assert result['sha256']==hashlib.sha256((delivery/'overleaf-package.zip').read_bytes()).hexdigest()
    for stem in STEMS[:-1]:
        source=(delivery/(stem+'.tex')).read_bytes()
        snapshot=json.loads((delivery/(stem+'-content.json')).read_text())
        assert snapshot['schema']=='native-tex-source-snapshot-v9-1'
        assert snapshot['canonical_source']==stem+'.tex'
        assert snapshot['latex'].encode()==source
        assert snapshot['source_sha256']==hashlib.sha256(source).hexdigest()
        for row in snapshot['recursive_inputs']:
            assert row['latex'].encode()==(delivery/row['path']).read_bytes()
    for stem in STEMS:
        assert (delivery/(stem+'-preview.pdf')).read_bytes()==(delivery/(stem+'.pdf')).read_bytes()


def test_existing_receipt_refuses_before_any_output_is_mutated(constructed_writer):
    writer,root,delivery,receipt=constructed_writer
    receipt.write_bytes(b'{"existing_receipt":"preserve exactly"}\n')
    for stem in STEMS:
        (delivery/(stem+'-preview.pdf')).write_bytes(('previous alias '+stem).encode())
    for stem in STEMS[:-1]:
        (delivery/(stem+'-content.json')).write_bytes(('previous source snapshot '+stem).encode())
    (delivery/'overleaf-package.zip').write_bytes(b'previous closed package')
    before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    with pytest.raises(AssertionError,match='fresh receipt'):
        writer.main()
    after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
    assert after==before, 'Existing receipt rejection must precede every snapshot, alias and ZIP mutation'
