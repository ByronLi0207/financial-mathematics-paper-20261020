"""Versioned document-source ZIP and transitive dependency manifest; no study code."""
from pathlib import Path
import hashlib,json,re,zipfile,shutil
ROOT=Path(__file__).resolve().parents[2];DOC=ROOT/'submission-v10'
def sha(b):return hashlib.sha256(b).hexdigest()
def dependencies():
    seen=set();waiting=['main.tex','manuscript.tex','supplement.tex','title-page.tex','cover-letter.tex','references.bib','README.md','AUTHOR-TODO.md']
    while waiting:
        name=waiting.pop();p=DOC/name
        if name in seen:continue
        if not p.is_file():raise ValueError('MISSING_SOURCE_DEPENDENCY:'+name)
        seen.add(name)
        if p.suffix=='.tex':
            s=p.read_text()
            for kind,target in re.findall(r'\\(input|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',s):
                if not Path(target).suffix:target+=('.tex' if kind=='input' else '.pdf')
                q=(DOC/target).resolve();assert q.is_relative_to(DOC.resolve());waiting.append(str(q.relative_to(DOC.resolve())))
    return sorted(seen)
def backup_if_untracked(p):
    # New own-document outputs are preserved before replacing an earlier build.
    if p.exists():
        b=p.with_name(p.name+'.bak');i=1
        while b.exists():b=p.with_name(p.name+f'.{i}.bak');i+=1
        shutil.copyfile(p,b)
def main():
    names=dependencies();items=[];path=DOC/'overleaf-package.zip';backup_if_untracked(path)
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in names:
            b=(DOC/name).read_bytes();z.writestr(name,b);items.append(dict(path=name,bytes=len(b),sha256=sha(b)))
    receipt=dict(schema='v10-source-package-v1',source_files=len(items),files=items,archive_path=str(path.relative_to(ROOT)),archive_bytes=path.stat().st_size,archive_sha256=sha(path.read_bytes()),entry_targets=['main.tex','supplement.tex','title-page.tex','cover-letter.tex'],scope='Native editable sources and exactly the used local dependencies; no private financial vectors or PDF preview aliases.')
    out=ROOT/'notes/v10/package-source-manifest.json';backup_if_untracked(out)
    out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
if __name__=='__main__':main()
