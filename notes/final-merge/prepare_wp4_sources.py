"""Create a separate final source tree; preserve exact relocated legacy blocks."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'submission-v10'
DEST=ROOT/'submission-final'
TITLE='When Is History Long Enough? Conditional Quantile Models versus Historical Rules for Peak Net-Position Limits'
KEEP={'sup:floor','sup:levy','sup:rank','sup:coherence','sup:implementation',
      'sup:v8-mc','sup:v8-daily','sup:v8-backcast','sup:v10-menu','sup:v10-cftc',
      'sup:v10-mcs','sup:v10-cost','sup:reproduction','sup:v11-history','sup:v12-details'}


def digest(raw):return hashlib.sha256(raw).hexdigest()


def main():
    assert DEST.is_dir() and (DEST/'main.tex').exists()
    assert not (DEST/'manuscript.tex').exists(),'Refuse to replace a previous final draft'
    entries=subprocess.check_output(['git','ls-files','-z','submission-v10'],cwd=ROOT).split(b'\0')
    copies=[]
    for raw in entries:
        if not raw:continue
        source=ROOT/raw.decode();name=source.relative_to(SOURCE)
        allowed=(source.suffix in ('.tex','.bib') or name.parts[0]=='figures' and source.suffix=='.pdf')
        if not allowed or name.as_posix() in ('main.tex','cover-letter.tex','supplement.tex'):continue
        target=DEST/name;target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists()
        content=source.read_bytes();target.write_bytes(content)
        copies.append(dict(source=str(source.relative_to(ROOT)),destination=str(target.relative_to(ROOT)),bytes=len(content),sha256=digest(content)))
    for name,source in [('final-unified-history.pdf','unified-history.pdf'),('final-decision-map.pdf','decision-map.pdf')]:
        raw=(ROOT/'results/final-merge/wp3-figures/render-v4'/source).read_bytes()
        target=DEST/'figures'/name;target.write_bytes(raw)
        copies.append(dict(source='results/final-merge/wp3-figures/render-v4/'+source,destination=str(target.relative_to(ROOT)),bytes=len(raw),sha256=digest(raw)))
    text=(SOURCE/'supplement.tex').read_text();body_start=text.index(r'\begin{document}')
    matches=list(re.finditer(r'\\section\{([^}]+)\}',text[body_start:]));assert len(matches)==36
    retained=[];moved=[];mapping=[]
    relocation=ROOT/'notes/final-merge/wp4-relocation';relocation.mkdir()
    for i,m in enumerate(matches):
        first=body_start+m.start();last=body_start+matches[i+1].start() if i+1<len(matches) else text.index(r'\end{document}',first)
        chunk=text[first:last];labels=re.findall(r'\\label\{([^}]+)\}',chunk)
        selected=bool(KEEP.intersection(labels))
        record=dict(original_section=i+1,title=m.group(1),labels=labels,bytes=len(chunk.encode()),sha256=digest(chunk.encode()),retained_in_compact=selected)
        if selected:
            retained.append(chunk);record['compact_section']=len(retained)
        else:
            path=relocation/f'original-S{i+1:02d}.tex';path.write_text(chunk)
            assert path.read_bytes()==chunk.encode();record['exact_relocated_copy']=str(path.relative_to(ROOT));moved.append(dict(record,content=chunk))
        mapping.append(record)
    assert len(retained)==len(KEEP)==15
    preamble=text[:body_start]
    preamble=re.sub(r'\\title\{[^\n]+\}',lambda _:r'\title{Online Supplement to '+TITLE+'}',preamble)
    intro=r'''
\begin{document}
\maketitle
This compact Supplement accompanies the consolidated manuscript. It retains
proofs, principal comparison inventories and the numerical and information-date
qualifications. Earlier longer inventories are preserved verbatim in
\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/EXTENDED_RESULTS.md}{the extended-results index},
alongside their original complete PDF and editable source. Their relocation
does not remove adverse, failed or unavailable outcomes.
\begingroup\small\setlength{\parskip}{0pt}\setcounter{tocdepth}{1}
\tableofcontents\endgroup\medskip
'''
    (DEST/'supplement.tex').write_text(preamble+intro+'\n'.join(retained)+'\n'+r'\end{document}'+'\n')
    prefix=['# Consolidated final-jof extended results','',
        'The current manuscript is in `submission-final/`. This index preserves exact overflow source blocks from the v12 backbone while the compact Supplement is prepared. The original complete [v12 Supplement](submission-v10/supplement.pdf) and [editable source](submission-v10/supplement.tex) remain unchanged. These are retained historical evidence, not additional analyses.','',
        '## Original-to-compact section map','',
        '| Original section | Topic | Current location |','|---|---|---|']
    for row in mapping:
        location='Compact Supplement S'+str(row['compact_section']) if row['retained_in_compact'] else '[Exact overflow source]('+row['exact_relocated_copy']+')'
        prefix.append(f"| S{row['original_section']} | {row['title']} | {location} |")
    prefix+=['','## Exact relocated section sources','',
        'Each block below is byte-identical to its original section in the v12 editable Supplement. Hashes refer to UTF-8 source bytes. Generated table/figure dependencies remain in the original package; no result is recalculated.','']
    for row in moved:
        prefix += [f"### Original Supplement S{row['original_section']}: {row['title']}",'',
            'Original source: `submission-v10/supplement.tex`; SHA-256 `'+row['sha256']+'`.',
            '', '```latex',row['content'].rstrip('\n'),'```','']
    baseline=(ROOT/'EXTENDED_RESULTS.md').read_text()
    (relocation/'previous-EXTENDED_RESULTS.md').write_text(baseline)
    (ROOT/'EXTENDED_RESULTS.md').write_text('\n'.join(prefix)+'\n\n---\n\n# Earlier extended-results index, retained verbatim\n\n'+baseline)
    (DEST/'README.md').write_text('# Consolidated final-jof source draft\n\nWork in progress under WP4. Main file: `main.tex`; Supplement: `supplement.tex`. The only final manuscript directory is this one; inherited A/B packages remain as evidence archives. WP4 compilation/counts, WP5 language, WP6 review, WP7 preparation and WP8 release gates must pass before the twelve-hour report. No submission has occurred.\n')
    report=dict(status='COPIED_AND_RELOCATED_DRAFT_NOT_ACCEPTED',title=TITLE,copied_files=copies,
        original_supplement_sections=36,compact_original_sections=15,relocated_sections=len(moved),
        section_mapping=mapping,source_supplement_sha256=digest((SOURCE/'supplement.tex').read_bytes()),
        inherited_files_changed=0,deleted_files=0,new_model_fits=0,raw_inputs_copied=0,
        next='Rewrite main argument/new mechanism section, update current cross-references, add CFTC appendix, compile and measure actual caps')
    (ROOT/'notes/final-merge/wp4-source-preparation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('copied_files','section_mapping')},indent=2))


if __name__=='__main__':main()
