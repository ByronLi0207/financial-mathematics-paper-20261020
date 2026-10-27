"""Inventory public Git document versions from pinned already-local objects."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import quote
import hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[2]
REPO='https://github.com/ByronLi0207/financial-mathematics-paper-20261020'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
heads=[]
for line in (ROOT/'notes/submission/remote-before.txt').read_text().splitlines():
    sha,ref=line.split('\t')
    if ref.startswith('refs/heads/'):
        heads.append(dict(branch=ref[len('refs/heads/'):],commit=sha))
def is_document(path):
    name=Path(path).name.lower()
    return name.endswith('.pdf') and bool(re.search(r'(^main\.pdf$|manuscript|supplement|(^|[-_])paper|title[-_]page|cover[-_]letter)',name))

blob_cache={}
def blob_info(blob):
    if blob not in blob_cache:
        raw=git('cat-file','blob',blob)
        blob_cache[blob]=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    return blob_cache[blob]
documents=[]
for head in heads:
    for item in git('ls-tree','-rz','--full-tree',head['commit']).split(b'\0'):
        if not item:continue
        meta,rawpath=item.split(b'\t',1);mode,kind,blob=meta.decode().split();path=rawpath.decode()
        if kind!='blob' or not is_document(path):continue
        documents.append(dict(**head,path=path,blob=blob,**blob_info(blob),url=REPO+'/blob/'+quote(head['branch'],safe='/')+'/'+quote(path,safe='/'),pinned_url=REPO+'/blob/'+head['commit']+'/'+quote(path,safe='/')))

# Include changed versions in the reachable public history, not private refs.
history=[]
log=git('log','--format=COMMIT:%H','--name-only',*[h['commit'] for h in heads],'--','*.pdf').decode()
current=None;seen=set()
for line in log.splitlines():
    if line.startswith('COMMIT:'):current=line[7:];continue
    if not line or not is_document(line):continue
    q=subprocess.run(['git','rev-parse',current+':'+line],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    if q.returncode:continue
    blob=q.stdout.decode().strip()
    if (line,blob) in seen:continue
    seen.add((line,blob))
    history.append(dict(commit=current,path=line,blob=blob,**blob_info(blob),url=REPO+'/blob/'+current+'/'+quote(line,safe='/')))

prs=json.loads((ROOT/'notes/submission/public-prs.json').read_text())
result=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),scope='Pinned public branch heads recorded in H0 and their reachable PDF history. No claim to know copies outside this public repository. Figures and unrelated reports excluded by documented basename rule.',name_rule='main.pdf, manuscript, supplement, *paper*, title-page, cover-letter PDF basenames',repository=REPO,visibility='public, independently read from connected GitHub PR metadata',branch_count=len(heads),branch_heads=heads,current_document_occurrences=len(documents),unique_pdf_blobs=len(blob_cache),current_documents=documents,reachable_historical_document_versions=len(history),history=history,pull_requests=prs['pull_requests'])
(ROOT/'notes/submission/public-versions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['# 已公开版本与预印本政策','','核查范围：H0所保存的15个公开分支头及其可达PDF修改历史；每份列出固定commit、Git blob、SHA-256和URL。未下载PDF，仅读已经存在的Git对象与公开GitHub元数据；不声称掌握作者在仓库外的其他版本。这里只做同一研究版本清单，不提供未实际运行的相似度百分比。','','## 公开分支头','','| Branch | Pinned head | Document PDFs | Link |','|---|---|---:|---|']
for h in heads:
    count=sum(d['branch']==h['branch'] for d in documents)
    lines.append(f"| `{h['branch']}` | `{h['commit'][:12]}` | {count} | [文件树]({REPO}/tree/{quote(h['branch'],safe='/')}) |")
lines += ['',f'分支头共有 {len(documents)} 个文稿/补充/标题页/附信PDF路径出现；可达历史去重后共有 {len(history)} 个 path/blob 版本。完整逐文件清单与 SHA 在 [public-versions.json](public-versions.json)。同一PDF在多个分支出现不当成多项独立研究。新的 submission-final 文件以最终 MANIFEST 为入口，发布后由H8远端回执确认。','','## PR #3–#6（只读）','','| PR | Title | Head | State |','|---|---|---|']
for p in prs['pull_requests']:
    lines.append(f"| [#{p['number']}]({p['url']}) | {p['title']} | `{p['head']['ref']}` / `{p['head']['sha'][:12]}` | {p['state']}; merged={p['merged']}; draft={p['draft']} |")
lines += ['', '## ASMBI 官方预印本政策', '', '[作者指南](https://onlinelibrary.wiley.com/page/journal/15264025/homepage/forauthors.html)，本轮H6再次直接读取，Preprint Policy原文短引：\n\n> will consider for review articles previously available as preprints', '', '该政策允许考虑已有预印本，也允许作者随时把投稿版本放在预印本服务器，并要求出版后更新最终出版链接。指南同时要求避免已正式发表和同时投他刊；预印本例外不能替作者证明全部原创性、版权或独家投稿条件。', '', '附信第三段披露GitHub工作版本、分支与PR，以及公开代码和汇总；供编辑在其政策下考虑，不断言任何GitHub形式都会自动被接受。受限原始输入的权利与共享例外另由作者确认。作者仍须确认仓库以外版本、所有作者同意和当前独家投稿状态。本轮没有联系期刊、改变公开范围或操作PR。', '', '## 待用户决定', '', '确认仓库外是否还有版本；确认本次只向一家期刊提交及全部作者批准；出版后补最终文章链接；是否调整仓库可见性或处理旧PR留待作者决定。', '']
(ROOT/'notes/submission/public-versions.md').write_text('\n'.join(lines))
print(json.dumps({k:result[k] for k in ['branch_count','current_document_occurrences','unique_pdf_blobs','reachable_historical_document_versions']},indent=2))
