from pathlib import Path
from collections import Counter
import datetime as dt,json,re
R=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent
p=R/'submission-final/supplement.tex';before=p.read_text();after=before
replacements={
 'extended result archive':'extended results',
 '\nthe original tables in the extended results':'\nThe original tables in the extended results',
 '. the extended results retain':'. The extended results retain',
 ' (the original tables in the extended results)':'',
 '}{the complete confidence-set archive} retains':'}{The complete confidence-set archive} retains',
 'with its original signed loss change} remains':'with its original signed loss change}, remains',
 'The following source-reported monetary values are never pooled':'These source-reported monetary values are never pooled',
 'Historical fallback and adverse outcomes':'Historical selections and adverse outcomes',
 'Historical fallback &':'Historical choice &',
 'The following table retains every within-cell comparison.':'The \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/EXTENDED_RESULTS.md#asmbi-extended-s20}{extended calibration results} retain every within-cell comparison.',
 'The complete inventory of non-complete reports is below.':'The \\href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/blob/submission-final/EXTENDED_RESULTS.md#asmbi-extended-s14}{extended selection results} list every incomplete report.',
}
counts={}
for a,b in replacements.items():
    pattern=re.escape(a).replace(r'\ ',r'\s+')
    counts[a]=len(re.findall(pattern,after))
    assert counts[a],a
    after=re.sub(pattern,lambda match:b,after)
after=after.replace('#asmbi-extended-s36}{complete earlier results}', '#asmbi-extended-s36}{earlier timing records}')
after=after.replace('#asmbi-extended-s38}{complete earlier results}', '#asmbi-extended-s38}{validation records}')
after=after.replace('#asmbi-extended-s39}{complete earlier results}', '#asmbi-extended-s39}{history-extension records}')
# Keep the two source links with the cost definitions, ahead of the two figures.
start=after.index(r'\section{Scores, breaches and specified limit costs}')
end=after.index(r'\section{Longer validation improves medians but leaves losses}',start)
chunk=after[start:end]
paragraph=re.search(r'\\href\{[^}]+#asmbi-extended-s09\}.*?retain the complete comparisons\.',chunk,re.S)
assert paragraph
closing=paragraph[0]
chunk=chunk.replace(closing,'',1)
where=chunk.index(r'\begin{figure}')
chunk=chunk[:where]+closing+'\n\n'+chunk[where:]
after=after[:start]+chunk+after[end:]
NUM=re.compile(r'(?<![A-Za-z0-9])[-+]?\d+(?:[.,]\d+)*(?![A-Za-z0-9])')
# Source-link identities move with their paragraph; factual numbers are unchanged.
def nums(text):
    text=re.sub(r'\\href\{[^}]+\}\{([^}]+)\}',r'\1',text)
    return NUM.findall(text)
assert nums(before)==nums(after)
snapshot=N/'R8-supplement-before-final-language.tex';assert not snapshot.exists();snapshot.write_text(before)
p.write_text(after)
record=dict(utc=dt.datetime.now(dt.timezone.utc).isoformat(),replacements=counts,
            numerical_sequence_excluding_link_addresses_exact=True,
            layout_change='Move the existing extended-cost links ahead of the figures to prevent an almost empty continuation page.',
            source_link_label_change='Use distinct timing, validation and history-extension labels instead of three identical adjacent labels.')
(N/'R8-supplement-language-edits.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
