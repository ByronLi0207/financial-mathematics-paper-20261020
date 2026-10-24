"""S7 actual-file citation/bibliography/placeholder cross-check."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
main=(ROOT/'submission-jof/manuscript.tex').read_text()
bib=(ROOT/'submission-jof/references.bib').read_text()
entries=json.loads((ROOT/'notes/v7/references-verified.json').read_text())
cited={key.strip() for match in re.findall(r'\\cite(?:p|t|alp)?\{([^}]+)\}',main) for key in match.split(',')}
bibkeys=set(re.findall(r'@\w+\{([^,]+),',bib))
printed=set(re.findall(r'\\bibitem\[[^\]]+\]\{([^}]+)\}',main))
placeholders={field:bool(re.search(re.escape(field)+r': \[TO BE COMPLETED BY AUTHOR\]',main))
              for field in ('Author information','ORCID','Funding','Competing interests','AI statement')}
passed=(cited==bibkeys==printed=={r['key'] for r in entries} and all(placeholders.values())
        and all(r['evidence_urls'] for r in entries))
report=dict(status='PASS' if passed else 'FAIL',cited=len(cited),bib_entries=len(bibkeys),printed_entries=len(printed),
            missing=sorted(cited-bibkeys),unused=sorted(bibkeys-cited),print_mismatches=sorted(cited^printed),
            metadata_entries_with_primary_evidence=sum(bool(r['evidence_urls']) for r in entries),
            author_placeholders=placeholders,author_declarations_completed=0)
print(json.dumps(report,indent=2));raise SystemExit(not passed)
