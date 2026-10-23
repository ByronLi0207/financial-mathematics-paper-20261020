"""Port verified PR2 science without changing either archived manuscript."""
from copy import deepcopy
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'notes/revision-v4-jof'
SOURCES = ['manuscript/revision-v3/paper-content.json',
           'manuscript/working-paper/paper-content.json']

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def main():
    v, m = [json.loads((ROOT / p).read_text()) for p in SOURCES]
    c = deepcopy(v)
    for si, sec in enumerate(c['sections']):
        for bi, b in enumerate(sec['blocks']):
            b['_source'] = {'path': SOURCES[0], 'sha256': digest(SOURCES[0]),
                            'pointer': ['sections', si, 'blocks', bi]}
    def adopt(vs, vb, ms, mb):
        b = deepcopy(m['sections'][ms]['blocks'][mb])
        b['_source'] = {'path': SOURCES[1], 'sha256': digest(SOURCES[1]),
                        'pointer': ['sections', ms, 'blocks', mb]}
        c['sections'][vs]['blocks'][vb] = b
    adopt(2, 1, 2, 1)
    clock = deepcopy(m['sections'][2]['blocks'][8])
    clock['_source'] = {'path': SOURCES[1], 'sha256': digest(SOURCES[1]),
                        'pointer': ['sections', 2, 'blocks', 8]}
    c['sections'][2]['blocks'].append(clock)
    adopt(4, 4, 4, 3)
    adopt(5, 4, 5, 4)
    adopt(7, 3, 8, 5)
    adopt(3, 12, 3, 12)
    adopt(10, 24, 11, 23)
    adopt(10, 28, 11, 27)
    adopt(12, 3, 13, 2)
    adopt(14, 7, 15, 3)
    fosd = deepcopy(m['sections'][9]['blocks'][1])
    fosd['_source'] = {'path': SOURCES[1], 'sha256': digest(SOURCES[1]),
                       'pointer': ['sections', 9, 'blocks', 1]}
    c['sections'][7]['blocks'].append(fosd)
    c['abstract'] = m['abstract']
    c['_abstract_source'] = {'path': SOURCES[1], 'sha256': digest(SOURCES[1]),
                             'pointer': ['abstract']}
    for sec in c['sections']:
        for b in sec['blocks']:
            for key in ('html', 'caption', 'text'):
                if key in b:
                    b[key] = b[key].replace('ordered innovations', 'ordered residuals')
                    b[key] = b[key].replace('standardize/rescale innovations', 'standardize/rescale residuals')
                    b[key] = b[key].replace('complete lower envelope', 'lower envelope within the archived report menu')
                    b[key] = b[key].replace('every nonnegative weighting', 'every constant nonnegative linear weighting')
    c['sections'][14]['title'] = 'Lower envelopes of eight archived reports'
    c['sections'][14]['blocks'][3]['html'] += (' The comparison is weak for every constant nonnegative linear weighting, '
        'and strict when a positively weighted component strictly decreases. '
        'Actual primary Murphy curves cross, so this statement does not extend to all consistent quantile scores.')
    c['sections'][12]['blocks'].append({'type': 'p', 'html':
        'The exact-real flat-objective illustration describes identification by the objective, not a finding of exact nonuniqueness in accepted financial fits. '
        'The binary floating-point quantile level slightly tilts that illustration. No accepted report is refitted or changed.',
        '_definition': 'PR2 REVIEW numerical-acceptance boundary; no new numerical assertion'})
    for i, ref in enumerate(c['references']):
        if ref['id'] == 'fr2004':
            c['references'][i] = deepcopy(next(r for r in m['references'] if r['id'] == 'fr2004'))
    (OUT / 'scientific-port.json').write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n')
    print('Scientific port saved; source manuscripts unchanged; two primary definitions and all v3 tables retained.')

if __name__ == '__main__':
    main()
