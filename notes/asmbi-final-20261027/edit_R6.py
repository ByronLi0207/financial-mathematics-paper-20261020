from pathlib import Path
import json

R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
p = R / 'submission-final/manuscript.tex'
s = p.read_text()
a = s.index(r'\section*{Data and code availability}')
b = s.index(r'\section*{Author-provided information}', a)
before = s[a:b]
after = r'''\section*{Data and code availability}
The FX observations come from the specified version of the \href{https://www.kaggle.com/datasets/davidlindsay1979/net-position-time-series-dataset}{Kaggle Net Position Time Series Dataset}, obtained through Kaggle. Its metadata attributes data-file copyright to the original authors, whose terms govern reuse. The repository records acquisition instructions and the input fingerprint, excluding raw observations and private prediction vectors.

New York Fed aggregates are obtained through its \href{https://www.newyorkfed.org/markets/counterparties/primary-dealers-statistics}{Primary Dealer Statistics service}. Reuse follows the Bank's \href{https://www.newyorkfed.org/privacy/termsofuse.html}{Terms of Use}, including attribution, source notices and clear labeling of modifications. The repository preserves the attributed Treasury snapshot, excluding the original panel CSV; current public vintages can differ from the study inputs.

CFTC observations were downloaded from the official \href{https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm}{Traders in Financial Futures historical archive}. The CFTC's \href{https://www.cftc.gov/sites/default/files/cftc/cftcprivacy.htm}{Web Policy} permits copying government information and requests acknowledgement, while separately protecting third-party material. Unchanged downloads and their source URLs, acquisition times, byte counts and fingerprints are recorded in \texttt{data/cftc-tff/provenance.json}.

Code, protocols, aggregate results and reproduction instructions are available in the \href{https://github.com/ByronLi0207/financial-mathematics-paper-20261020/tree/submission-final}{versioned GitHub repository}; [Zenodo DOI to be added by the author].

'''
assert not (N / 'R6-availability-before.tex').exists()
(N / 'R6-availability-before.tex').write_text(before)
(N / 'R6-availability-after.tex').write_text(after)
p.write_text(s[:a] + after + s[b:])
record = {
    'source_paragraph_sentences': [3, 3, 3], 'code_sentences': 1,
    'rights_checked_utc': '2026-10-27T09:27:00Z',
    'official_sources': [
        {'url': 'https://www.newyorkfed.org/privacy/termsofuse.html',
         'finding': 'Permits copying/distribution subject to attribution, notices, modification labeling and further conditions.'},
        {'url': 'https://www.cftc.gov/sites/default/files/cftc/cftcprivacy.htm',
         'finding': 'Government information is public domain; acknowledgement requested; third-party rights separate.'}
    ],
    'fx_rights': 'Original-source metadata and existing input audit; redistribution permission not inferred.',
    'new_downloads': 0, 'new_financial_computation': 0,
    'outside_availability_unchanged': p.read_text() == s[:a] + after + s[b:]
}
(N / 'R6-availability-source-check.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
