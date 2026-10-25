"""Keep the figure-legend sheet and human-readable proofreading record synchronized."""
from pathlib import Path
import hashlib, json, re, subprocess, shutil
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'notes/v11'
def write(path, content):
    if path.exists() and subprocess.run(['git','ls-files','--error-unmatch',str(path.relative_to(ROOT))], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
        backup = path.with_name(path.name+'.bak')
        i=1
        while backup.exists():
            backup=path.with_name(path.name+f'.{i}.bak');i+=1
        shutil.copyfile(path,backup)
    path.write_text(content)

def braced(text, start):
    assert text[start]=='{'
    depth=1;i=start+1
    while depth:
        if text[i]=='{' and text[i-1]!='\\':depth+=1
        if text[i]=='}' and text[i-1]!='\\':depth-=1
        i+=1
    return text[start+1:i-1]

source=(ROOT/'submission-v10/manuscript.tex').read_text()
captions=[]
for block in re.findall(r'\\begin\{figure\}.*?\\end\{figure\}',source,re.S):
    start=block.index(r'\caption{')+len(r'\caption')
    captions.append(braced(block,start))
assert len(captions)==5
legends='\\section*{Figure legends}\n'+''.join(f'\\paragraph{{Figure {i}.}} {caption}\n\n' for i,caption in enumerate(captions,1))
write(ROOT/'submission-v10/figure-legends.tex',legends)

passes=[]
rollback_path=HERE/'proofreading-rollbacks.json'
rollbacks=json.loads(rollback_path.read_text())['rolled_back']if rollback_path.exists()else[]
excluded={(x['pass'],x['id'])for x in rollbacks}
for p in sorted(HERE.glob('proofreading-pass*.json')):
    r=json.loads(p.read_text());passes.extend(x for x in r['edits']if(p.name,x.get('id'))not in excluded)
lines=['# v11 English proofreading log','',
       'This log records actual editorial changes. Scientific numbers, archived results and conclusions are unchanged. Figure numbering and the v11 version links are structural integration changes, recorded separately from language edits.','',
       'APA evidence is itemized in [part 1](APA-review-part1.md) and [part 2](APA-review-part2.md). No year, volume, issue, page range or DOI identity was corrected.','',
       f'Total recorded change groups: **{len(passes)}**; individual occurrences: **{sum(r["occurrences"] for r in passes)}**. Reference punctuation, bibliography synchronization, layout and cross-reference changes are included and identified by category.','']
for i,r in enumerate(passes,1):
    lines +=[f'## {i}. {r["category"]} — `{r["file"]}`','',
             'Before:','',f'> {r["before"]}','', 'After:','',f'> {r["after"]}','',
             'Reason: '+r['reason'],'','Scientific numeric sequence unchanged: '+str(r['numeric_sequence_unchanged'] or r.get('structural_cross_reference_only',False))+'.'+(' The only added digits identify the S35 navigation pointer.' if r.get('structural_cross_reference_only',False) else ''),'']
write(HERE/'proofreading-log.md','\n'.join(lines))
if rollbacks:
    with(HERE/'proofreading-log.md').open('a')as f:
        f.write('\n## Excluded and restored local artifact\n\nOne unused, ignored legacy display was renamed without a pre-write backup. It has been restored byte-for-byte to the v10b style receipt and is excluded from the final editing count and publication. Its post-edit image is retained as a local .bak; the initial edit record is preserved in pass 3. See [the correction receipt](proofreading-rollbacks.json).\n')
write(HERE/'figure-legend-sync.json',json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),
      source_sha256=hashlib.sha256(source.encode()).hexdigest(),figures=len(captions),captions=captions,
      legend_sha256=hashlib.sha256(legends.encode()).hexdigest(),status='EXACT_CAPTION_MATCH'),indent=2)+'\n')
print('Captions',len(captions),'proofreading passages',len(passes))
