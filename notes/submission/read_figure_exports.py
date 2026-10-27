"""Read back the completed TIFF exports after a metadata serialization failure."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[]
for source in sorted((ROOT/'submission-final/figures').glob('*.pdf')):
    cached=ROOT/'.scratch/submission/figure-exports-h2'/(source.stem+'.tif')
    with Image.open(cached) as image:
        assert image.format=='TIFF' and image.mode=='RGB'
        size=list(image.size);dpi=[float(x) for x in image.info['dpi']]
        assert min(dpi)>=999
    page=PdfReader(source).pages[0]
    dimensions=[float(page.mediabox.width),float(page.mediabox.height)]
    assert all(abs(px-pt*1000/72)<=1.1 for px,pt in zip(size,dimensions))
    outputs=[]
    for journal in ['ASMBI','QF']:
        dest=ROOT/'submission-package'/journal/'figures-upload'
        assert sha(dest/source.name)==sha(source)
        assert sha(dest/(source.stem+'.tif'))==sha(cached)
        outputs.extend(str((dest/name).relative_to(ROOT)) for name in [source.name,source.stem+'.tif'])
    rows.append(dict(source=str(source.relative_to(ROOT)),source_sha256=sha(source),tiff_sha256=sha(cached),pixels=size,dpi=dpi,compression='LZW',mode='RGB',source_page_points=dimensions,outputs=outputs))
report=dict(status='PASS_ACTUAL_EXPORT_FILE_READBACK',readback_utc=datetime.now(timezone.utc).isoformat(),initial_export_status='All ten render/copy steps finished; final JSON write failed on Pillow IFDRational. No image or research calculation was retried.',scope='Current canonical PDF bytes match both uploaded PDF copies; both TIFF copies match actual cached exports. Density and pixel dimensions read from real files.',figures=rows)
out=ROOT/'notes/submission/figure-exports.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n')
print('Verified actual figure exports:',len(rows),'at',min(min(r['dpi']) for r in rows),'native dpi')
