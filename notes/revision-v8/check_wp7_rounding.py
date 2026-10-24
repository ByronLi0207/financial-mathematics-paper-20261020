"""Current-sentence saved-field checks for every main-prose percentage.

Retains the original17field checks and adds exactlythree new displayvalues.
This is a display/lookup check, not a new financial analysis.
"""
from pathlib import Path
import argparse,importlib.util,json,re
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('old_rounding',ROOT/'notes/revision-v8/check_wp1_rounding.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def pointer(path,key):
    value=json.loads((ROOT/path).read_text())
    for piece in key.strip('/').split('/'):value=value[int(piece)] if isinstance(value,list) else value[piece]
    return value

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    abstract,paragraphs=old.writing.prose((ROOT/'submission-jof/manuscript.tex').read_text())
    sentences=old.writing.v7.sentences(abstract+' '+' '.join(paragraphs));records=[];bound=[]
    for anchor,ids in old.CASES:
        matches=[s for s in sentences if s.startswith(anchor)];assert len(matches)==1,(anchor,matches)
        sentence=matches[0];actual=re.findall(r'(?<![\w.])([+-]?\d+(?:\.\d+)?)\s*%',sentence)
        raw=[old.original_value(old.ROWS[i]) for i in ids];expected=[format(abs(float(v)),'.1f') for v in raw]
        records.append(dict(anchor=anchor,sentence=sentence,old_field_ids=ids,raw_values=raw,expected_display=expected,actual_display=actual,match=actual==expected));bound.append(sentence)
    new=json.loads((ROOT/'notes/revision-v8/wp7-main-integration.json').read_text())['new_reader_numeric_bindings']
    cases=[('The exception is the longer-history four-predictor regression',[r for r in new if r['source']=='results/revision-v8/wp4/summary.json' and 'relative_loss_percent' in r.get('pointer','')]),('For original short-horizon FX regression',[r for r in new if r['source']=='results/revision-v8/wp5/summary.json' and 'relative_change_percent' in r.get('pointer','')])]
    for anchor,fields in cases:
        matches=[s for s in sentences if s.startswith(anchor)];assert len(matches)==1,(anchor,matches)
        sentence=matches[0];actual=re.findall(r'(?<![\w.])([+-]?\d+(?:\.\d+)?)\s*%',sentence)
        raw=[pointer(r['source'],r['pointer']) for r in fields]
        assert all(v==r['raw_value'] for v,r in zip(raw,fields))
        expected=[format(abs(float(v)),'.1f') for v in raw]
        records.append(dict(anchor=anchor,sentence=sentence,source_bindings=fields,expected_display=expected,actual_display=actual,match=actual==expected));bound.append(sentence)
    percentage_sentences=[s for s in sentences if re.search(r'\d\s*%',s)]
    assert percentage_sentences==bound,'Unbound or reordered current percentage sentence'
    differences=[r for r in records if not r['match']]
    out=dict(status='FAIL' if differences else 'PASS',operation='exactsavedfieldlookup andone-decimalprosedisplayonly',original_bound_percentage_fields=17,new_bound_percentage_fields=3,total_bound_percentage_fields=sum(len(r['expected_display']) for r in records),current_percentage_sentences=len(percentage_sentences),unbound_percentage_sentences=0,mismatches=len(differences),records=records,failures=differences)
    (ROOT/args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['records','failures']},indent=2));raise SystemExit(bool(differences))

if __name__=='__main__':main()
