#!/usr/bin/python3
from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[2]
N=Path(__file__).resolve().parent
pattern='AI-use|AI use|artificial intelligence|generative|language model|AI disclosure|AI statement|AI使用声明|AI 使用声明|AI声明'
args=['rg','-n','-i',pattern,'submission-final','submission-package','README.md','REPRODUCING.md','CANONICAL.md','-g','!*.bak','-g','!**/failed-cuts/**']
p=subprocess.run(args,cwd=R,text=True,capture_output=True)
assert p.returncode in (0,1),p.stderr
lines=p.stdout.splitlines()
reminder='AI 使用声明由作者投稿前自行添加（Wiley 要求披露）'
exceptions=[line for line in lines if line.startswith('submission-final/AUTHOR-TODO.md:') and line.endswith(reminder)]
other=[line for line in lines if line not in exceptions]
assert len(exceptions)==1 and not other,other
relocation=json.loads((N/'R2-template-relocation.json').read_text())
result={'step':'R2','status':'PASS','command':args,'raw_stdout':p.stdout,'raw_stderr':p.stderr,'rg_exit':p.returncode,'disclosure_or_placeholder_matches':len(other),'author_todo_reminder_exceptions':len(exceptions),'original_template_files_preserved':relocation['count']}
(N/'R2-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('$ '+' '.join(args));print('[raw rg stdout]');print(p.stdout,end='');print('[raw rg stderr]');print(p.stderr,end='');print(json.dumps(result,ensure_ascii=False,indent=2))
