"""Compile the source ZIP in a clean directory; compare actual document pixels.

Requires only already cached Tectonic/Poppler and pypdf. No financial inputs,
model execution, downloads, or manuscript regeneration occur.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time
import zipfile

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/revision-v8/wp8-isolated-package"
DELIVERY = ROOT / "submission-jof"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, cwd, output):
    start = time.monotonic()
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
               VECLIB_MAXIMUM_THREADS="1", MKL_NUM_THREADS="1")
    r = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, env=env, timeout=600)
    output.write_text(r.stdout)
    assert r.returncode == 0, (command, r.stdout[-2000:])
    return dict(command=command, returncode=r.returncode,
                elapsed_seconds=time.monotonic()-start, output=str(output.relative_to(ROOT)))


def check():
    SCRATCH.mkdir(parents=True, exist_ok=False)
    source = SCRATCH / "sources"
    source.mkdir()
    package = DELIVERY / "overleaf-package.zip"
    with zipfile.ZipFile(package) as archive:
        for name in archive.namelist():
            assert not Path(name).is_absolute() and ".." not in Path(name).parts
            assert archive.read(name) == (DELIVERY/name).read_bytes()
        archive.extractall(source)
    visual = json.loads((ROOT/"notes/revision-v8/wp8-supplement-visual-final.json").read_text())
    dpi = {"manuscript": 125, "supplement": 140, "title-page": 125}
    original_images = {
        "manuscript": ROOT/".scratch/revision-v8/wp8-main-final/rendered",
        "title-page": ROOT/".scratch/revision-v8/wp8-title-final",
    }
    supp_images = {p["page"]: Path(p["path"]) for p in visual["pages"]}
    results = []
    for stem, pages in (("manuscript",20),("supplement",30),("title-page",1)):
        out = SCRATCH / (stem + "-output")
        out.mkdir()
        cmd = ["/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic",
               "-X","compile","--only-cached",stem+".tex","--outdir",str(out),
               "--keep-logs","--keep-intermediates"]
        receipt = run(cmd, source, ROOT/f"notes/revision-v8/wp8-package-{stem}-console.txt")
        current = PdfReader(DELIVERY/(stem+".pdf")); rebuilt=PdfReader(out/(stem+".pdf"))
        assert len(current.pages)==len(rebuilt.pages)==pages
        old_text=[p.extract_text() for p in current.pages]
        new_text=[p.extract_text() for p in rebuilt.pages]
        assert old_text==new_text
        assert not any("\ufffd" in t or "??" in t for t in new_text)
        log=(out/(stem+".log")).read_text()
        bad=[line for line in log.splitlines() if re.search(
            r"^!|Overfull|Undefined control sequence|Missing character|(?:Citation|Reference).*undefined|There were undefined",line)]
        assert not bad, bad
        pixel_cmd=["pdftoppm","-r",str(dpi[stem]),"-png",str(out/(stem+".pdf")),str(out/"page")]
        receipt["render"] = run(pixel_cmd,source,ROOT/f"notes/revision-v8/wp8-package-{stem}-render-console.txt")
        rebuilt_images=sorted(out.glob("page-*.png"))
        assert len(rebuilt_images)==pages
        pixel_checks=[]
        for page, png in enumerate(rebuilt_images,1):
            if stem=="supplement": old=supp_images[page]
            else:
                candidates=sorted(original_images[stem].glob(f"page-{page:02}.png")) or sorted(original_images[stem].glob(f"page-{page}.png"))
                assert len(candidates)==1, (stem,page,candidates)
                old=candidates[0]
            assert sha(old)==sha(png), (stem,page)
            pixel_checks.append(dict(page=page,sha256=sha(png),identical_to_actually_viewed_page=True))
        receipt.update(stem=stem,pages=pages,source_sha256=sha(source/(stem+".tex")),
                       original_pdf_sha256=sha(DELIVERY/(stem+".pdf")),
                       rebuilt_pdf_sha256=sha(out/(stem+".pdf")),
                       every_page_text_identical=True,every_page_pixel_identical=True,
                       pixel_checks=pixel_checks,error_overfull_undefined_missing_glyph=[],
                       underfull_warning_count=len(re.findall("Underfull",log)))
        results.append(receipt)
    return dict(utc=datetime.now(timezone.utc).isoformat(),status="PASS",package_sha256=sha(package),
                isolated_source_directory=str(source.relative_to(ROOT)),documents=results,
                child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                financial_models_run=0,raw_financial_inputs_read=0,network_downloads=0,
                scope="Document package/source/text/pixel consistency; original local Git-dependent financial replay remains separate and blocked in browser-only fresh clone")


if __name__=="__main__":
    result=check()
    (ROOT/"notes/revision-v8/wp8-isolated-package-check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="documents"},indent=2))
    for r in result["documents"]:
        print(r["stem"],r["pages"],"all text/pixels identical",r["every_page_pixel_identical"])
