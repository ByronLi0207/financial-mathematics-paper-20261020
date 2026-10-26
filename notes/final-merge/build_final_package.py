"""Create a new, source-only Overleaf ZIP from actual final dependencies."""
from pathlib import Path
import argparse,hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'submission-final'

def digest(raw):return hashlib.sha256(raw).hexdigest()
def dependencies():
    found=set();pending=[BASE/p for p in ['main.tex','supplement.tex','title-page.tex','cover-letter.tex','figure-legends.tex','references.bib','README.md']]
    while pending:
        candidate=pending.pop()
        if candidate.is_symlink():raise ValueError('SYMLINK_DEPENDENCY')
        p=candidate.resolve()
        if not p.is_relative_to(BASE.resolve()):raise ValueError('DEPENDENCY_OUTSIDE_FINAL_SOURCE')
        if not p.is_file():raise ValueError('DEPENDENCY_MISSING:'+str(p))
        if p in found:continue
        if '.bak' in p.name.lower() or any(x in p.parts for x in ['.scratch','.git','raw']):raise ValueError('FORBIDDEN_PACKAGE_MEMBER')
        found.add(p)
        if p.suffix!='.tex':continue
        text=re.sub(r'(?<!\\)%[^\n]*','',p.read_text())
        for name in re.findall(r'\\input\{([^}]+)\}',text):
            dep=BASE/name;pending.append(dep if dep.suffix else dep.with_suffix('.tex'))
        for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',text):
            dep=BASE/name
            if not dep.suffix:
                candidates=[dep.with_suffix(ext) for ext in ['.pdf','.png','.jpg'] if dep.with_suffix(ext).exists()]
                if len(candidates)!=1:raise ValueError('AMBIGUOUS_GRAPHIC_DEPENDENCY:'+name)
                dep=candidates[0]
            pending.append(dep)
    return sorted(found)

def build(output):
    output=Path(output);files=dependencies();members={str(p.relative_to(BASE)):p.read_bytes() for p in files}
    manifest=dict(schema='final-editorial-source-zip-v1',entry_points=['main.tex','supplement.tex','title-page.tex','cover-letter.tex'],scope='Only editable final texts, README, bibliography and actual transitive tables/figures; no raw data, code runtime, backups, private vectors, credentials or Git objects.',members=[dict(path=name,bytes=len(raw),sha256=digest(raw)) for name,raw in members.items()])
    members['SOURCE-MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    with output.open('xb') as stream:
        with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,raw in sorted(members.items()):
                info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw)
    with zipfile.ZipFile(output) as z:
        names=z.namelist();assert len(names)==len(set(names))==len(members)
        for name,expected in members.items():
            if z.read(name)!=expected:raise ValueError('ZIP_MEMBER_BYTES_MISMATCH:'+name)
    result=dict(status='PASS',zip=str(output),zip_bytes=output.stat().st_size,zip_sha256=digest(output.read_bytes()),member_count=len(members),backup_members=[],private_or_raw_members=[],deterministic_zip_timestamps='1980ZIP epoch only; not a research or Git timestamp',members=[dict(path=name,bytes=len(raw),sha256=digest(raw)) for name,raw in sorted(members.items())])
    print(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args();r=build(a.output);a.receipt.write_text(json.dumps(r,indent=2)+'\n')
