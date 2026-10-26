"""Same frozen writing statistic, plus separately labeled primary counts."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
from writing_check import unified_manuscript_statistics


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--label',required=True)
    a=p.parse_args();raw=a.source.read_bytes();report=unified_manuscript_statistics(a.source)
    body=' '.join(s['text'] for s in report['sentences_detail'])
    # The original counter remains unchanged. This distinct supplemental count
    # implements the v9 task's additional primary-word acceptance condition.
    report['primary_body_occurrences']=len(re.findall(r'\bprimary\b',body,re.I))
    source=raw.decode();main=source.split(r'\section{Introduction}',1)[1]
    main=re.split(r'\\section\*\{(?:Data and code availability|Declarations and availability|References)\}',main)[0]
    report['primary_main_source_occurrences']=len(re.findall(r'\bprimary\b',main,re.I))
    report['v9_acceptance']=dict(flagged_at_most_8_percent=report['flagged_proportion']<=.08,
        average_at_most20=report['average_sentence_words']<=20,
        zero_over40=report['over_40_words']==0,primary_at_most3=report['primary_main_source_occurrences']<=3,
        no_forbidden_body=report['forbidden_occurrences']==0)
    report.update(label=a.label,created_utc=datetime.now(timezone.utc).isoformat(),
        source=str(a.source.resolve()),source_sha256=hashlib.sha256(raw).hexdigest(),
        checker_sha256=hashlib.sha256(Path(__file__).with_name('writing_check.py').read_bytes()).hexdigest(),
        scope='Original PR3 full-stop/word/term rules; Introduction through Conclusion excluding floats, displays, references and declarations. Abstract/captions separately reported.')
    with a.output.open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n')
    keys=['label','sentences','flagged_proportion','average_sentence_words','over_40_words','primary_body_occurrences','primary_main_source_occurrences','forbidden_occurrences','abstract_words','abstract_numeric_occurrences','v9_acceptance']
    print(json.dumps({k:report[k] for k in keys},indent=2))


if __name__=='__main__':main()
