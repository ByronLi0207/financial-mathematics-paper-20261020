"""Use the existing writing metric unchanged on the final canonical sources."""
from pathlib import Path
import argparse, hashlib, json, runpy, shutil, datetime, subprocess
ROOT=Path(__file__).resolve().parents[2]

def metrics():
    namespace=runpy.run_path(str(ROOT/'notes/v9/writing_check.py'),run_name='submission_frozen_writing_reader')
    result=namespace['unified_manuscript_statistics'](ROOT/'submission-final/manuscript.tex')
    return result

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
    output=ROOT/args.output
    if output.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(output.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode:
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');shutil.copyfile(output,output.with_name(output.name+'.'+stamp+'.bak'))
    result=metrics();output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['words','sentences','flagged_proportion','average_sentence_words','over_40_words','abstract_words','abstract_numeric_occurrences']},indent=2))

if __name__=='__main__':main()
