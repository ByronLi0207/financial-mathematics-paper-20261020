"""Map old hardcoded section references to the current compact source."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'submission-final'
URL='https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/final-jof/EXTENDED_RESULTS.md'


def main():
    rows=json.loads((ROOT/'notes/final-merge/wp4-source-preparation.json').read_text())['section_mapping']
    mapping={r['original_section']:r['compact_section'] for r in rows if r['retained_in_compact']}
    changes=[]
    pattern=r'(?P<prefix>(?:Supplement\s+)?Sections?)\s+(?P<ids>S\d+(?:(?:--|\s*(?:,|and)\s*)S\d+)*)'
    for path in [BASE/'manuscript.tex',BASE/'supplement.tex',*(BASE/'generated').glob('*.tex')]:
        # The exact A analytic source remains byte-identical and has no hardcoded S refs.
        if path.name=='final-analytic-qualifications.tex':continue
        text=path.read_text();before=text
        def section(match):
            original=match.group(0);numbers=[int(x) for x in re.findall(r'S(\d+)',match['ids'])]
            required=set(numbers)
            for a,b in re.findall(r'S(\d+)--S(\d+)',match['ids']):required.update(range(int(a),int(b)+1))
            if required.issubset(mapping):
                ids=re.sub(r'S(\d+)',lambda m:'S'+str(mapping[int(m.group(1))]),match['ids'])
                replacement=match['prefix']+' '+ids
            else:replacement=r'\href{'+URL+'}{the original full Supplement: '+original.replace('Supplement ','')+'}'
            if replacement!=original:changes.append(dict(file=str(path.relative_to(ROOT)),before=original,after=replacement))
            return replacement
        text=re.sub(pattern,section,text)
        # Table and figure numbers without labels refer to the preserved original
        # full source, rather than being silently renumbered as current items.
        text=re.sub(r'(?<!original )(?:Supplement\s+)?(?:Tables?|Figures?)\s+S\d+(?:(?:--|\s*(?:,|and)\s*)S\d+)*',
            lambda m:r'\href{'+URL+'}{the original full Supplement: '+m.group(0).replace('Supplement ','')+'}',text)
        if text!=before:path.write_text(text)
    report=dict(status='UPDATED_PENDING_COMPILE',section_map=mapping,changes=changes,scientific_numeric_fields_changed=0,
        scope='Reference identifiers/prose only; original scientific table cells, results and protocol files unchanged')
    (ROOT/'notes/final-merge/wp4-crossref-changes.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],section_reference_changes=len(changes),scientific_numeric_fields_changed=0),indent=2))


if __name__=='__main__':main()
