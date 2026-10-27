from pathlib import Path
import datetime as dt, json, re, shutil
R=Path(__file__).resolve().parents[2]; N=Path(__file__).resolve().parent
p=R/'submission-final/manuscript.tex'; before=p.read_text()
after=before.replace('extended result archive','extended results')
old=r'Average-loss tests, strict-hit diagnostics and RMS-state comparisons therefore answer distinct questions (\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/EXTENDED_RESULTS.md#asmbi-extended-s33}{extended accuracy and hit diagnostics}; \citealp{gw2006}).'
new=r'Average-loss tests, strict-hit diagnostics and RMS-state comparisons therefore answer distinct questions \citep{gw2006}; \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/EXTENDED_RESULTS.md#asmbi-extended-s33}{extended accuracy and hit diagnostics} retain the complete comparisons.'
assert old in after
after=after.replace(old,new,1)
num=re.compile(r'(?<![A-Za-z0-9])[-+]?\d+(?:[.,]\d+)*(?![A-Za-z0-9])')
assert num.findall(before)==num.findall(after)
snapshot=N/'R8-main-before-final-language.tex'; assert not snapshot.exists(); snapshot.write_text(before)
p.write_text(after)
record=dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(),
            plain_term_replacements=before.count('extended result archive'),
            citation_punctuation_repair=1,numeric_sequence_exact=True,
            reason='Simpler reader-facing name for the extended results and direct citation punctuation observed on rendered page 11.')
(N/'R8-language-edits.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
