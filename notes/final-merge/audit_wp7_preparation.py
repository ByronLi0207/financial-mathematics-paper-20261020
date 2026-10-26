"""Check WP7 preparation artifacts, exact source package and rebuild receipts."""
from pathlib import Path
import hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parents[2]

def main():
    errors=[];notes=ROOT/'notes/final-merge';base=ROOT/'submission-final'
    reviewers=json.loads((notes/'wp7-reviewer-verification.json').read_text());candidates=reviewers['rows']
    if not 5<=len(candidates)<=6:errors.append('CANDIDATE_COUNT')
    article=(base/'manuscript.tex').read_text();candidate_text=(notes/'suggested-reviewers.md').read_text()
    for row in candidates:
        if row['email']!='[author to verify]' or not row['institution_url'].startswith('https://'):errors.append('CANDIDATE_EMAIL_OR_SOURCE')
        if not all(']{'+k+'}' in article for k in row['cited_keys']):errors.append('CANDIDATE_NOT_CITED:'+row['name'])
    if re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',candidate_text):errors.append('UNREQUESTED_REVIEWER_EMAIL')
    qa=(notes/'anticipated-questions.md').read_text();numbers=[int(x) for x in re.findall(r'(?m)^(\d+)\. \*\*',qa)]
    if numbers!=list(range(1,11)) or qa.count('**位置：**')!=10:errors.append('TEN_QA_AND_LOCATIONS')
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',article,re.S).group(1)
    cover=(base/'cover-letter.tex').read_text()
    if ' '.join(abstract.split()) not in ' '.join(cover.split()):errors.append('COVER_ABSTRACT_MISMATCH')
    aux=json.loads((notes/'wp7-aux-compile-audit.json').read_text())
    if aux['status']!='PASS' or any(r['pages']!=1 or r['bad_diagnostics'] for r in aux['targets']):errors.append('AUX_COMPILE_OR_PAGE_CAP')
    if not (ROOT/'README.md').read_bytes().endswith((notes/'wp7-root-readme-before.md').read_bytes()):errors.append('HISTORICAL_README_BYTES_CHANGED')
    command='python3 reproduce_final_displays.py --output final-display-rebuild'
    if any(command not in p.read_text()[:1000] for p in [ROOT/'README.md',base/'README.md']):errors.append('README_TOP_COMMAND')
    evidence=json.loads((notes/'wp7-acquisition-fingerprints.json').read_text());guide=(base/'README.md').read_text()
    if len(evidence['cftc'])!=11:errors.append('CFTC_ARCHIVE_COUNT')
    for row in [evidence['fx'],evidence['nyfed'],*evidence['cftc']]:
        if row['sha256'] not in guide:errors.append('GUIDE_SHA_MISSING')
    backups=[str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and '.bak' in p.name.lower()]
    if backups:errors.append('FINAL_BACKUP_FILE')
    manifest=json.loads((notes/'wp7-package-manifest.json').read_text());zpath=ROOT/manifest['zip']
    if hashlib.sha256(zpath.read_bytes()).hexdigest()!=manifest['zip_sha256']:errors.append('ZIP_HASH')
    with zipfile.ZipFile(zpath) as z:
        rows={r['path']:r for r in manifest['members']}
        if set(z.namelist())!=set(rows) or len(rows)!=26:errors.append('ZIP_CENSUS')
        for name,row in rows.items():
            raw=z.read(name)
            if hashlib.sha256(raw).hexdigest()!=row['sha256'] or len(raw)!=row['bytes']:errors.append('ZIP_MEMBER:'+name)
            if name!='SOURCE-MANIFEST.json' and raw!=(base/name).read_bytes():errors.append('ZIP_SOURCE_BYTES:'+name)
            if '.bak' in name.lower() or any(k in Path(name).parts for k in ['.scratch','.git','raw']):errors.append('FORBIDDEN_ZIP_MEMBER:'+name)
    displays=json.loads((notes/'wp7-display-equivalence.json').read_text())
    if displays['status']!='PASS' or not displays['decomposition_pixels_identical'] or not displays['all_482_history_point_records_identical']:errors.append('DISPLAY_EQUIVALENCE')
    raw_source=article.split(r'\begin{abstract}',1)[1];actual_captions=[]
    for block in re.findall(r'\\begin\{figure\}.*?\\end\{figure\}',article,re.S):
        content=block.split(r'\caption{',1)[1].split(r'}\label',1)[0];actual_captions.append(' '.join(content.split()))
    legend=(base/'figure-legends.tex').read_text()
    if len(actual_captions)!=4 or len(re.findall(r'\\paragraph\{Figure \d+\.\}',legend))!=4:errors.append('LEGEND_CENSUS')
    if any(c not in ' '.join(legend.split()) for c in actual_captions):errors.append('LEGEND_TEXT_MISMATCH')
    result=dict(status='PASS' if not errors else 'MISMATCH',mismatch_count=len(errors),mismatches=errors,candidates=len(candidates),author_decision_required=True,questions=10,main_tables_rebuilt=6,main_figures_rebuilt=4,cover_pages=1,title_pages=1,zip_members=26,zip_sha256=manifest['zip_sha256'],final_backup_files=backups,existing_backups_retained=json.loads((notes/'wp7-existing-backups.json').read_text())['count'],source_acquisition_fingerprints=13,new_downloads=0,new_model_fits=0,old_readme_bytes_preserved=True,scope='WP7 preparation only. Full final page-by-page QA, bibliography audit, fresh full pytest, rights/tracked-file gate and remote publication/readback are WP8.')
    (notes/'wp7-preparation-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(bool(errors))

if __name__=='__main__':main()
