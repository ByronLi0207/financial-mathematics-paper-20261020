"""Verify saved register locators and bytes; never recompute a judgment."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, shutil, subprocess

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'notes/submission/prediction-register.json'
register=json.loads(source.read_text())
cache={}
records=[]

def pointer(document, path):
    obj=document
    for part in path.lstrip('/').split('/') if path else []:
        part=part.replace('~1','/').replace('~0','~')
        obj=obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj

for row in register['rows']:
    for kind in ['design_bindings','result_bindings']:
        for binding in row[kind]:
            key=binding['source_commit']+':'+binding['path']
            if key not in cache:
                cache[key]=subprocess.check_output(['git','show',key],cwd=ROOT)
            raw=cache[key]
            assert hashlib.sha256(raw).hexdigest()==binding['sha256'],key
            text=raw.decode()
            fmt=binding['format']
            if fmt=='json':
                assert pointer(json.loads(text),binding['json_pointer'])==binding['value'],binding
            elif fmt=='markdown-json-fence':
                matches=[]
                for fence in re.findall(r'```json\s*\n(.*?)\n```',text,re.S):
                    try:matches.append(pointer(json.loads(fence),binding['json_pointer'])==binding['value'])
                    except (KeyError,IndexError,TypeError,ValueError):pass
                assert any(matches),binding
            elif fmt=='markdown-literal':
                quote='\n'.join(text.splitlines()[binding['line']-1:binding.get('line_end',binding['line'])])
                assert quote==binding['quote'],binding
            else:raise ValueError(fmt)
            records.append(dict(row_id=row['row_id'],kind=kind,source=key,format=fmt,sha256=binding['sha256'],pointer=binding.get('json_pointer'),status='EXACT'))
assert len(register['rows'])==register['row_counts']['total']==36
assert len({r['row_id'] for r in register['rows']})==36
assert set(register['latex_table_handoff']['row_order'])=={r['row_id'] for r in register['rows']}
output=ROOT/'notes/submission/prediction-register-verification.json'
if output.exists():
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    shutil.copyfile(output,output.with_name(output.name+'.'+stamp+'.bak'))
result=dict(status='PASS_EXACT_SAVED_LOCATORS_NO_JUDGMENT_RECALCULATION',verified_utc=datetime.now(timezone.utc).isoformat(),register_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rows=36,bindings=len(records),unique_source_blobs=len(cache),saved_decision_counts=register['row_counts']['by_saved_decision'],records=records)
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},ensure_ascii=False,indent=2))
