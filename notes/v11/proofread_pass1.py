"""Apply recorded language/APA/layout edits only; assert all digit sequences stay fixed."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'notes/v11'
records = []

def replace(path, before, after, reason, category='language', count=1):
    p = ROOT / path
    text = p.read_text()
    assert text.count(before) == count, (path, before, text.count(before))
    # Paragraph-level numeric strings, including bibliographic metadata, are immutable.
    assert re.findall(r'\d+', before) == re.findall(r'\d+', after), (before, after)
    p.write_text(text.replace(before, after))
    records.append(dict(id=f'P{len(records)+1:03}', file=path, before=before,
                        after=after, occurrences=count, reason=reason,
                        category=category, numeric_sequence_unchanged=True))

main = 'submission-v10/manuscript.tex'
bib = 'submission-v10/references.bib'
sup = 'submission-v10/supplement.tex'

replace(main, 'The two official weekly systems report different aggregate exposures.',
        'The two official weekly reporting systems describe different aggregate exposures.',
        'Clarify that the systems are reporting systems; avoid report/reporting repetition.')
replace(main, 'Original protocol comparisons retain their original reference procedures and values.',
        'The protocol comparisons retain their original reference procedures and values.',
        'Remove repeated original while preserving the frozen-protocol statement.')
replace(main, 'Wisniewski and colleagues forecast signed next-hour position intervals',
        'Earlier FX studies forecast signed next-hour position intervals',
        'The citation includes a multi-author article and a single-author thesis; avoid misattributing coauthors.')
replace(main, 'The larger set contains 33 predictors plus an unpenalized intercept.',
        'Full regression uses 33 predictors plus an unpenalized intercept.',
        'Use the established method name rather than an implicit larger set.')
replace(main, 'The four-predictor variant uses current magnitude, signed level and two increment RMS measures.',
        'The four-feature variant uses current magnitude, signed level and two increment RMS measures.',
        'Use four-feature consistently with the saved curve and method label.')

# Strict APA DOI/URL punctuation applies to the reference list, not prose URLs.
p = ROOT / main
text = p.read_text()
start = text.index(r'\begin{thebibliography}')
prefix, refs = text[:start], text[start:]
for match in list(re.finditer(r'\\url\{[^}]+\}\.(?=\s*(?:\\bibitem|\\end\{thebibliography\}|\\raggedright))', refs)):
    before = match.group(0)
    replace(main, before, before[:-1], 'APA: no terminal period after a final DOI or URL; identifier unchanged.', 'APA')

for author, date in [
    ('Board of Governors of the Federal Reserve System', '2013, March'),
    ('Board of Governors of the Federal Reserve System', '2024, July'),
    ('Commodity Futures Trading Commission', 'n.d.'),
    ('Federal Reserve Bank of New York', 'n.d.'),
]:
    replace(main, f'}} {author} ({date}).', f'}} {author}. ({date}).',
            'APA: finish the corporate-author element with a period.', 'APA')

replace(main,
        r'\emph{Traders in financial futures: Historical compressed reports}. \url{https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm}. Retrieved October 24, 2026.',
        r'\emph{Historical compressed}. Retrieved October 24, 2026, from \url{https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm}',
        'Use the official page H1 and put the unchanged retrieval date before its URL.', 'APA')
replace(bib, 'title={Traders in financial futures: Historical compressed reports}',
        'title={Historical compressed}', 'Synchronize official CFTC web-page title with the rendered reference.', 'APA')
replace(main,
        r'\emph{Primary dealer statistics} [Data set]. Federal Reserve Bank of New York. \url{https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics}. Retrieved October 23, 2026.',
        r'\emph{Primary dealer statistics} [Data set]. Retrieved October 23, 2026, from \url{https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics}',
        'APA: omit duplicated publisher and position the unchanged retrieval date before the URL.', 'APA')
for title in [
    'Reporting guidelines for preparing the FR 2004 primary government securities dealers reports',
    'Instructions for the preparation of government securities dealers reports: Reporting form FR 2004'
]:
    replace(main, r'\emph{'+title+r'}. Board of Governors of the Federal Reserve System.',
            r'\emph{'+title+r'}.', 'APA: omit the publisher when it is identical to the corporate author.', 'APA')

replace(main,
        r'Adaptive conformal inference under distribution shift. \emph{Advances in Neural Information Processing Systems}, \emph{34}, 1660--1672.',
        r'Adaptive conformal inference under distribution shift. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P. S. Liang, \& J. Wortman Vaughan (Eds.), \emph{Advances in Neural Information Processing Systems} (Vol. 34, pp. 1660--1672). Curran Associates, Inc.',
        'APA published-proceedings format; editors and publisher verified against the official NeurIPS BibTeX.', 'APA')
replace(bib,
        'booktitle = {Advances in Neural Information Processing Systems}',
        'booktitle = {Advances in Neural Information Processing Systems},\n  editor = {Ranzato, M. and Beygelzimer, A. and Dauphin, Y. and Liang, P. S. and Wortman Vaughan, J.},\n  publisher = {Curran Associates, Inc.}',
        'Synchronize verified conference editors and publisher with the rendered reference.', 'APA')
replace(main,
        r'In \emph{Proceedings of the Ninth Symposium on Conformal and Probabilistic Prediction and Applications} (Proceedings of Machine Learning Research, Vol. 128, pp. 285--301).',
        r'In A. Gammerman, V. Vovk, Z. Luo, E. Smirnov, \& G. Cherubin (Eds.), \emph{Proceedings of the Ninth Symposium on Conformal and Probabilistic Prediction and Applications} (Proceedings of Machine Learning Research, Vol. 128, pp. 285--301). PMLR.',
        'APA published-proceedings format; editor names and publisher verified against the official PMLR record.', 'APA')
replace(bib,
        'booktitle = {Proceedings of the Ninth Symposium on Conformal and Probabilistic Prediction and Applications}',
        'booktitle = {Proceedings of the Ninth Symposium on Conformal and Probabilistic Prediction and Applications},\n  editor = {Gammerman, A. and Vovk, V. and Luo, Z. and Smirnov, E. and Cherubin, G.},\n  publisher = {PMLR}',
        'Synchronize verified conference editors and publisher with the rendered reference.', 'APA')
for title, repository in [
    (r"[Master's thesis, Delft University of Technology].", 'TU Delft Repository'),
    (r'[Doctoral thesis, Royal Holloway, University of London].', 'Royal Holloway Research Portal')
]:
    replace(main, title, title+' '+repository+'.',
            'APA: add the verified institutional-repository source element for a published thesis.', 'APA')

replace(sup,
        r'Individual-dealer external validation and prospective first-release validation remain unmet.\section{Additional saved evidence on history length}',
        'Individual-dealer external validation and prospective first-release validation remain unmet.\n\n'+r'\FloatBarrier'+'\n\n'+r'\section{Additional saved evidence on history length}',
        'Flush earlier Murphy plots before the imported section; keep the section command on a separate line.', 'layout')

report = dict(created_utc=datetime.now(timezone.utc).isoformat(), pass_name='first-language-and-APA-pass',
              scope='Editorial changes only. All digit sequences within every edited passage remain unchanged.',
              sources=['notes/v11/APA-review-part1.md', 'notes/v11/APA-review-part2.md'], edits=records)
(HERE / 'proofreading-pass1.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
print('Recorded changes:', len(records))
