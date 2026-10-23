"""Source-linked literature positioning, with no estimation or external access.

Only the directed sources in literature-a/b are used.  A not-reported cell is
scope-limited; it is never treated as evidence of absence across a whole paper.
The Delft thesis remains a narrative precursor but is excluded from this fresh
primary-body table because the new original-body access attempts failed.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NOTE = Path('notes/revision-v5-novelty')
A_PATH = NOTE / 'literature-a.json'
B_PATH = NOTE / 'literature-b.json'
PANEL_PATH = Path('results/revision-20261023/round2/panel/selection-manifest.json')
COUNTS_PATH = Path('results/revision-20261023/round2/panel/descriptive-counts.json')
BEFORE_PATH = NOTE / 'v4-manuscript-before.json'
OUTPUT_PATH = NOTE / 'positioning-source.json'
SEARCH_PATH = Path('notes/novelty-search.md')
DIMENSIONS = ('target', 'data_unit', 'known_floor', 'mature_labels', 'evaluation',
              'cross_source_transfer')
DIMENSION_NAMES = ('Forecast object', 'Data unit', 'Known peak floor',
                   'Outcome maturity / ordering', 'Evaluation', 'Cross-source scope')


def _read(path):
    return json.loads((ROOT / path).read_text())


def _encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def _fingerprint(path):
    raw = (ROOT / path).read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def _year(citation):
    match = re.search(r'(?<!\d)(?:19|20)\d{2}(?!\d)', citation)
    if match is None:
        raise ValueError('No verified bibliographic year in supplied citation')
    return match.group()


def _sources(a, b):
    result = deepcopy(a['sources'])
    for paper in b['papers']:
        result[paper['id']] = {
            'title_and_citation': paper['citation'],
            'url': paper['primary_url'],
            'actual_reading_scope': paper['actual_reading_scope'],
            'accessed_utc': paper['accessed_utc'],
            'source_fingerprint': paper['source_fingerprint'],
            'metadata_urls': paper.get('metadata_urls', []),
        }
    # A local cache path is unnecessary in the public evidence artifact.
    for source in result.values():
        source.pop('local_private_cache', None)
    return result


def _a_row(item, source_records):
    result = {'id': item['id'], 'label': item['short_label'],
              'verification': item['verification'], 'dimensions': {}}
    for name, cell in item['dimensions'].items():
        key = 'mature_labels' if name == 'maturity_control' else name
        record = deepcopy(cell)
        for evidence in record['evidence']:
            evidence['primary_url'] = source_records[evidence['source_id']]['url']
        result['dimensions'][key] = record
    return result


def _b_row(item):
    result = {'id': item['id'], 'label': item['citation'],
              'verification': 'fresh_partial_primary_body', 'dimensions': {}}
    for key, source in item['dimensions'].items():
        result['dimensions'][key] = {
            'value': source['evidence'],
            'status': 'not_reported_in_read_scope' if 'n.r.' in source['evidence']
                      else 'reported_in_read_scope',
            'evidence': [{'source_id': item['id'], 'locator': source['locator'],
                          'support': source['evidence'],
                          'primary_url': source['primary_url']}],
        }
    return result


def _own_cell(value, pointer, support):
    return {'value': value, 'status': 'current_archived_study',
            'evidence': [{'source_id': 'THIS_STUDY',
                          'locator': str(pointer), 'support': support,
                          'local_source': str(BEFORE_PATH), 'json_pointer': pointer}]}


def _own_row(manifest, counts):
    eligible = manifest['eligible']
    if len(eligible) != counts['series_count'] or len(set(eligible)) != len(eligible):
        raise ValueError('Panel manifest and descriptive series count disagree')
    original = 'PDPOSGS-B'
    if original in eligible:
        raise ValueError('The additional-series list unexpectedly includes original bill')
    if original not in manifest['economic_grid_source']:
        raise ValueError('Original bill identity is not supported by the frozen grid metadata')
    return {
        'id': 'this_study', 'label': 'This study',
        'verification': 'retrospective_own_study_not_independent_replication',
        'dimensions': {
            'target': _own_cell('Sampled absolute position peak', ['sections', 3, 'blocks', 2],
                               'Measured target includes the observed issue position and subsequent source records.'),
            'data_unit': _own_cell('One FX dealer; Treasury aggregates', ['sections', 2],
                                  'The FX record and New York Fed aggregates are separate measurement processes.'),
            'known_floor': _own_cell('Observed |Nₜ| projection', ['sections', 3, 'blocks', 16],
                                    'The observed current magnitude is a report floor; all historical controls use current-anchor information.'),
            'mature_labels': _own_cell('Completed peak-label pools', ['sections', 3, 'blocks', 0],
                                      'Every training label has completed by the refit; rolling and frozen refresh schedules are distinguished.'),
            'evaluation': _own_cell('Pinball, coverage, Murphy, preferences', ['sections', 4],
                                   'Scores, coverage diagnostics and fixed-report preference analysis are retained together.'),
            'cross_source_transfer': {
                'value': 'FX plus related Treasury tasks; no new dealer',
                'status': 'qualified_cross_measurement_application',
                'evidence': [
                    {'source_id': 'THIS_PANEL', 'locator': 'eligible',
                     'local_source': str(PANEL_PATH), 'json_pointer': ['eligible'],
                     'support': 'Additional related aggregate tasks, selected by metadata/calendar before panel models.'},
                    {'source_id': 'THIS_STUDY', 'locator': 'sections[7].blocks[5]',
                     'local_source': str(BEFORE_PATH), 'json_pointer': ['sections', 7, 'blocks', 5],
                     'support': 'The extensions do not supply independent unseen-dealer validation.'},
                ],
                'treasury_task_counts': {
                    'original_bill_series': original,
                    'original_bill_count': len([original]),
                    'additional_aggregate_series': eligible,
                    'additional_aggregate_count': len(eligible),
                    'total_treasury_tasks': len([original, *eligible]),
                    'interpretation': 'The total is one original bill task plus additional related aggregate tasks; not independent dealers.',
                },
            },
        },
    }


def _short_rows(a, b):
    metadata = a['sources']
    other = {p['id']: p for p in b['papers']}
    # Citation years below are read from checked owning-source metadata.
    labels = [
        f"Wisniewski et al. ({metadata['W20']['year']}); Wisniewski ({metadata['W24']['award_year']})",
        f"Boudoukh et al. ({metadata['MAX_FINAL']['year']})",
        f"Petrunia et al. ({_year(other['petrunia2019']['citation'])})",
        f"Arjani et al. ({_year(other['arjani2020']['citation'])})",
        f"Engle–Manganelli ({_year(other['engle2004']['citation'])})",
        f"Ehm et al. ({_year(other['ehm2016']['citation'])})",
        f"Duffie et al. ({_year(other['duffie2023']['citation'])})",
        'This study',
    ]
    values = [
        ['Signed endpoint interval', 'One FX dealer', 'Peak floor n.r.',
         'Ordered endpoint split; peak n.r.', 'Pinball/Winkler; UC/CC', 'n.r. in endpoint task'],
        ['Worst portfolio return', 'Stylized fixed portfolio', 'Initial value known; peak floor n.r.',
         'n.r.; analytic/simulation', 'Tail probability; VaR ratios', 'n.r.; parameter cases'],
        ['Daily cross-participant debit maximum', 'ACSS clearers', 'Peak floor n.r.',
         'Incoming-data updates; peak n.r.', 'Tail fit; collateral shortfalls', 'Within ACSS; source transfer n.r.'],
        ['Remaining-day liquidity ratio', 'LVTS participants', 'Known flows; peak floor n.r.',
         'Chronological split; peak n.r.', 'RMSE; liquidity-risk bands', 'Within LVTS; source transfer n.r.'],
        ['Conditional return quantile', 'Stocks and index returns', 'Peak floor n.r.',
         'Lagged predictors; held-out returns', 'Quantile objective; hits; DQ', 'Several returns; different task'],
        ['Quantile/expectile ranking', 'Survey, probability and wind cases', 'Zero wind support; moving peak floor n.r.',
         'Original splits; peak n.r.', 'Murphy; coverage/sharpness', 'Multiple domains; different tasks'],
        ['Capacity/illiquidity; PnL VaR', 'Dealer and market sources', 'Peak floor n.r.',
         'Expanding VaR; peak n.r.', 'Quantile fit; PnL forecasts', 'Several sources; different task'],
        ['Sampled absolute peak', 'One FX dealer; Treasury totals', 'Observed |Nₜ| projection',
         'Completed peak labels', 'Pinball; coverage; Murphy', 'FX and related Treasury tasks'],
    ]
    return [[label, *cells] for label, cells in zip(labels, values)]


def _appendix(rows, source_records):
    blocks = [{'type': 'p', 'html':
               'Each cell below identifies the actual original passages used. n.r. is limited to the inspected task and reading scope; it is not a claim that a concept is absent from an entire paper or the literature. Related aggregate tasks do not constitute independent dealer validation.'}]
    for row in rows:
        blocks.append({'type': 'subheading', 'text': row['display_label']})
        table_rows = []
        for key, name, short in zip(DIMENSIONS, DIMENSION_NAMES, row['display_values']):
            cell = row['dimensions'][key]
            pieces = []
            for evidence in cell['evidence']:
                link = evidence.get('primary_url', evidence.get('local_source', ''))
                pieces.append(evidence['locator'] + ': ' + evidence['support'] + ' Source: ' + link)
            table_rows.append([name, short, ' '.join(pieces)])
        blocks.append({'type': 'table',
                       'caption': 'Source-linked positioning evidence. Reading scopes are limited as stated in the source register.',
                       'headers': ['Dimension', 'Main-table wording', 'Original passage and boundary'],
                       'rows': table_rows, 'cell_html': {}})
    blocks.append({'type': 'subheading', 'text': 'Source register and actual reading scope'})
    for ident in sorted(source_records):
        if ident == 'HOOGEN':
            continue
        source = source_records[ident]
        scope = source.get('actual_reading_scope', source.get('fresh_reading_scope', ''))
        blocks.append({'type': 'p', 'html': ident + ': ' + scope + ' Source: ' + source['url']})
    return {'title': 'Source-linked literature-positioning evidence', 'blocks': blocks}


def _payload():
    a, b = _read(A_PATH), _read(B_PATH)
    manifest, counts = _read(PANEL_PATH), _read(COUNTS_PATH)
    sources = _sources(a, b)
    a_by_id = {row['id']: row for row in a['rows']}
    rows = [_a_row(a_by_id['wisniewski2020_2024'], sources),
            _a_row(a_by_id['boudoukh2004'], sources)]
    rows.extend(_b_row(paper) for paper in b['papers'])
    rows.append(_own_row(manifest, counts))
    short = _short_rows(a, b)
    if len(rows) != len(short) or len(rows) != len({r['id'] for r in rows}):
        raise ValueError('Positioning row identities are not one-to-one')
    for row, values in zip(rows, short):
        if set(row['dimensions']) != set(DIMENSIONS):
            raise ValueError('Missing evidence dimension for ' + row['id'])
        row['display_label'], row['display_values'] = values[0], values[1:]
        for key, cell in row['dimensions'].items():
            if not cell['evidence']:
                raise ValueError('Missing cell evidence: ' + row['id'] + '/' + key)
    table = {
        'type': 'table',
        'caption': 'Directed literature positioning. Peak floor denotes an origin-known absolute-position report floor; maturity denotes completion of forward path labels. n.r. means not reported in the inspected task/passages, not absence from the paper. The related Treasury tasks are not independent dealers. Source-linked cell evidence is retained in the Online Supplement.',
        'headers': ['Study', 'Forecast object', 'Data unit', 'Peak floor',
                    'Maturity / ordering', 'Evaluation', 'Cross-source scope'],
        'rows': short, 'cell_html': {},
    }
    return {
        'schema': 'v5-positioning-source-v1',
        'inputs': [_fingerprint(p) for p in (A_PATH, B_PATH, PANEL_PATH, COUNTS_PATH, BEFORE_PATH)],
        'table': table, 'evidence_rows': rows, 'source_register': sources,
        'evidence_appendix': _appendix(rows, sources),
        'excluded_rows': [deepcopy(a_by_id['hoogen2017'])],
        'exclusion_ruling': 'The Delft original body could not be reacquired. Its known cash-peak precursor remains acknowledged in the narrative; this fresh-body comparison table excludes it rather than treating unverifiable cells as negative findings.',
        'scope_ruling': 'A directed comparison cannot establish first or unique status for a conjunction. Joint score and coverage evaluation and known support/starting information have clear precedents.',
        'search_logs': {'a': a['search_log_fragment'], 'b': b['search_log']},
    }


def positioning_table():
    """Return a canonical table block bound to its generated source JSON."""
    payload = _payload()
    result = deepcopy(payload['table'])
    result['_source'] = {'path': str(OUTPUT_PATH), 'sha256': sha256(_encoded(payload)).hexdigest(),
                         'pointer': ['table']}
    return result


def positioning_evidence():
    """Return the raw canonical payload; writing it is byte-identical to main().

    Do not attach self-referential source fingerprints to this saved object.
    The public table view adds its fingerprint only after the payload is built.
    """
    return _payload()


def printable_evidence_blocks(evidence=None):
    """Return one concise generated paragraph per row, with all cell locators.

    The caller's numeric validator should regenerate the matching paragraph by
    its ``v5:positioning_evidence:<row id>`` generator key.  The underlying raw
    payload retains longer evidence text, scope and source fingerprints.
    """
    evidence = positioning_evidence() if evidence is None else evidence
    blocks = []
    for row in evidence['evidence_rows']:
        pieces = []
        for key, name, short in zip(DIMENSIONS, DIMENSION_NAMES,
                                    row['display_values']):
            refs = []
            for record in row['dimensions'][key]['evidence']:
                refs.append(record['source_id'] + ', ' + record['locator'])
            pieces.append(name + ': ' + short + ' (' + '; '.join(refs) + ').')
        if row['id'] == 'ehm2016':
            pieces.insert(0,'All Ehm page locators below refer to the arXiv author-v2 revision, not final journal pagination.')
        if row['id'] == 'this_study':
            task = row['dimensions']['cross_source_transfer']['treasury_task_counts']
            pieces.append('Treasury task count: ' +
                          str(task['total_treasury_tasks']) + ' = ' +
                          str(task['original_bill_count']) + ' original bill + ' +
                          str(task['additional_aggregate_count']) +
                          ' related additional aggregates; not independent dealers.')
        blocks.append({
            'type': 'p',
            'html': '<b>' + row['display_label'] + '.</b> ' + ' '.join(pieces),
            '_generator': 'v5:positioning_evidence:' + row['id'],
            '_bindings': deepcopy(evidence['inputs']),
        })
    blocks.append({
        'type': 'p',
        'html': ('Source IDs identify the original links and actual reading ranges '
                 'in the repository source register and novelty-search log. '
                 'The excluded cash-peak thesis remains a narrative precedent; '
                 'failed current access is not evidence that a concept is absent.'),
        '_definition': 'Reading-scope and source-routing qualification; no numerical claim',
    })
    return blocks


def _search_markdown(payload):
    lines = ['# Directed novelty and positioning search', '',
             'This is a bounded source-location audit, not an exhaustive systematic search or proof of priority. No citation-count or popularity claim is made. Dates are the actual directed-search dates retained by the readers.', '',
             '## Search services, dates and exact queries', '']
    for entry in payload['search_logs']['a']:
        lines += ['- Date: ' + entry['date'] + '; service/database: ' + entry['database']]
        lines += ['  - Query: `' + query + '`' for query in entry['queries']]
        lines += ['  - Outcome: ' + entry['result']]
    item = payload['search_logs']['b']
    lines += ['', '- Date: ' + item['date_utc'] + '; service/database: ' + item['service']]
    lines += ['  - Query: `' + query + '`' for query in item['queries']]
    lines += ['  - Limits: ' + item['limits'], '', '## Primary bodies actually read', '']
    for ident, source in payload['source_register'].items():
        scope = source.get('actual_reading_scope', source.get('fresh_reading_scope', ''))
        lines += ['- ' + ident + ': ' + scope, '  - Original: ' + source['url']]
    own = next(row for row in payload['evidence_rows'] if row['id'] == 'this_study')
    task = own['dimensions']['cross_source_transfer']['treasury_task_counts']
    lines += ['', '## What this search does and does not support', '',
              '- ' + payload['scope_ruling'],
              '- Wisniewski’s endpoint study already combines interval/quantile losses and coverage tests with ordered rolling train/calibration/test sets. CAViaR and the Murphy-score literature supply further joint-scoring/calibration precedents.',
              '- ' + payload['exclusion_ruling'],
              '- The study comparison spans ' + str(task['total_treasury_tasks']) + ' Treasury tasks: ' + str(task['original_bill_count']) + ' original bill task plus ' + str(task['additional_aggregate_count']) + ' additional related aggregate tasks. This does not mean independent dealers; the FX record is a separate measurement task, not an additional authenticated dealer replication.',
              '- MaxVaR’s newly inspected journal-layout original labels its page range as 1–6; the old local 14–19 range is not used. Its direct path-risk conversion prevents describing endpoint-to-peak conversion generally as new.',
              '- The Royal Holloway thesis has an award year of 2024 and a cover year of 2023. The table groups its endpoint chapter with the earlier paper; other thesis applications do not establish an independent dealer test of this peak task.', '',
              'Every included table cell has the original URL and page/section locator in `notes/revision-v5-novelty/positioning-source.json`. No third-party source PDFs are redistributed.']
    return '\n'.join(lines) + '\n'


def _write_new_or_identical(path, content):
    destination = ROOT / path
    if destination.exists():
        if destination.read_bytes() != content:
            raise FileExistsError('Refusing to alter existing output: ' + str(path))
        return 'unchanged'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    return 'created'


def main():
    payload = _payload()
    outputs = [(OUTPUT_PATH, _encoded(payload)),
               (SEARCH_PATH, _search_markdown(payload).encode())]
    # Preflight the complete pair so a conflict cannot leave a half-updated pair.
    for path, content in outputs:
        if (ROOT / path).exists() and (ROOT / path).read_bytes() != content:
            raise FileExistsError('Refusing to alter existing output: ' + str(path))
    for path, content in outputs:
        print(str(path) + ': ' + _write_new_or_identical(path, content))
    print('Source-linked positioning rows: ' + str(len(payload['evidence_rows'])))
    print('Every included row has ' + str(len(DIMENSIONS)) + ' evidence dimensions.')


if __name__ == '__main__':
    main()
