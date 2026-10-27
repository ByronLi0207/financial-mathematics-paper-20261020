"""Apply individually accepted English-review suggestions, preserving scientific digits."""
from pathlib import Path
from datetime import datetime, timezone
import json,re
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'notes/v11';records=[]

def edit(path,before,after,reason,category='language',expected=1,structural_digits=False):
    p=ROOT/path;text=p.read_text()
    pattern=re.escape(before).replace(r'\ ',r'\s+')
    matches=list(re.finditer(pattern,text))
    assert len(matches)==expected,(path,before,len(matches),expected)
    assert structural_digits or re.findall(r'\d+',before)==re.findall(r'\d+',after),(before,after)
    for m in reversed(matches):text=text[:m.start()]+after+text[m.end():]
    p.write_text(text)
    records.append(dict(id=f'P3-{len(records)+1:03}',file=path,before=before,after=after,
                        occurrences=len(matches),reason=reason,category=category,
                        numeric_sequence_unchanged=not structural_digits,
                        structural_cross_reference_only=structural_digits))

def suggestions(filename,ids,path):
    report=(HERE/filename).read_text()
    for block in re.split(r'(?=^### )',report,flags=re.M):
        head=re.match(r'### (\w+)',block)
        if not head or head.group(1)not in ids:continue
        pair=re.findall(r'```(?:latex|text)\n(.*?)\n```',block.split('\n## ',1)[0],re.S)
        assert len(pair)==2,(filename,head.group(1))
        edit(path,*pair,f'Accepted {filename} {head.group(1)}; language clarification preserves the original comparison and limitations.')

main='submission-v10/manuscript.tex';sup='submission-v10/supplement.tex';letter='submission-v10/cover-letter.tex'
suggestions('english-review-main.md',{'E01','E02','E03','E04','E05','E06','E07','E08','E09','E10','E11','E12','E13','E14','E15','E16','H01','H02','H03','H06','H07'},main)
suggestions('english-review-main.md',{'C03','C04','C05'},letter)
edit(letter,'The paper suits Journal of Forecasting through its comparison of complete forecast procedures under matched histories and update schedules.',
     r'The paper fits the \emph{Journal of Forecasting} because it compares complete forecast procedures under matched histories and update schedules.',
     'Use an idiomatic fit statement and italicize the journal title.')
edit(letter,'Matched FX gains remain reference-dependent, weekly historical controls remain competitive, and CFTC expanded regression is generally cheaper under higher reserve and lower fixed-breach charges, with local exceptions.',
     'Matched FX gains remain reference-dependent, weekly historical controls remain competitive, and expanded-menu regression generally has lower illustrative costs in the CFTC comparisons under higher reserve and lower fixed breach charges, with local exceptions.',
     'Name the expanded-menu procedure and retain the already stated illustrative-cost boundary and local exceptions.')
edit(main,'Both methods retain their original, different penalty menus, and every tested history is shown against its own matched historical headroom.',
     'The methods retain distinct original penalty menus, and every tested history is shown against its own matched historical headroom.',
     'Improve caption wording while preserving its three-sentence limit and unequal original menus.')
edit(main,'Within the original FX period, the learning curve improves over intermediate histories but gives back part of the gain at the longest history',
     'Within the original FX period, the full-regression learning curve improves at intermediate histories but gives back part of the gain at the longest history',
     'Identify the full-regression curve; the four-feature curve has a different shape.')
edit(main,'Together, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.',
     'Supplement Section S35 retains the full contrasts and synthetic confirmation summary. Together, the history and menu comparisons link conditional gains to history length and the availability of strong shrinkage.',
     'Add an exact navigation pointer to the imported supplement section; the new digits identify a section, not a result.',
     category='cross-reference',structural_digits=True)

suggestions('english-review-supplement.md',{'E01','E02','E03','E04','E05','E06','E07','E08','E09','E11','E12','E13','E14','E15','E16','E17','E19','E23','E24','E25'},sup)
edit('submission-v10/generated/v8-daily-results-table.tex',
     'The isolated parsimonious score gain has more breaches than its historical reference.',
     'The parsimonious report yielding the isolated score gain has more breaches than its historical reference.',
     'A report, rather than a score gain, has breaches; the original gain and adverse breach comparison remain.')
edit('submission-v10/generated/v10-mcs-compact.tex','Same-record dailyFX','Same-record daily FX',
     'Restore the space in a prose heading and caption; source keys remain unchanged.',expected=2)
edit('submission-v10/generated/v10-mcs-compact.tex','FX early2015','FX early 2015',
     'Restore the space before the unchanged period label; source keys remain unchanged.',expected=2)

# One model name and one spelling convention in prose, preserving published titles.
for path in [main,sup,'submission-v10/generated/v10-legacy-map.tex']:
    for before,after in [('four-predictor','four-feature'),('Four-predictor','Four-feature')]:
        count=(ROOT/path).read_text().count(before)
        if count:edit(path,before,after,'Use four-feature consistently for the same QR4 procedure; no code identifier changes.',expected=count)
for path in [main,sup]:
    for before,after in [('labelling','labeling'),('labelled','labeled'),('favourable','favorable'),('favour the column','favor the column')]:
        count=(ROOT/path).read_text().count(before)
        if count:edit(path,before,after,'Use American-English spelling in prose, preserving all published titles and names.',expected=count)
edit(main,'[Doctoral thesis, Royal Holloway, University of London].',
     '[Doctoral dissertation, Royal Holloway, University of London].',
     'Use the APA doctoral-dissertation descriptor; degree, institution, year and title are unchanged.','APA')
edit('submission-v10/references.bib','institution = {Royal Holloway, University of London}',
     'institution = {Royal Holloway, University of London},\n  type = {Doctoral dissertation},\n  publisher = {Royal Holloway Research Portal}',
     'Synchronize the APA thesis descriptor and institutional-repository source element.','APA')
edit('submission-v10/references.bib','institution = {Delft University of Technology}',
     "institution = {Delft University of Technology},\n  type = {Master's thesis},\n  publisher = {TU Delft Repository}",
     'Synchronize the verified thesis and institutional-repository source elements.','APA')

report=dict(created_utc=datetime.now(timezone.utc).isoformat(),pass_name='accepted-English-review-and-terminology-pass',
            scope='Scientific results, digits, formulas, identifiers and adverse conclusions preserved; one S35 navigation pointer explicitly excepted.',edits=records)
(HERE/'proofreading-pass3.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('Change groups',len(records),'individual occurrences',sum(r['occurrences']for r in records))
