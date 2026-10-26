"""Check disposition completeness and current local evidence, without analysis."""
from pathlib import Path
import collections,hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[2]

def main():
    r=json.loads((ROOT/'notes/final-merge/wp6-review-dispositions.json').read_text());errors=[]
    counts=collections.Counter(x['role'] for x in r['rows'])
    if sorted(counts.values())!=[7,7,7] or len(r['rows'])!=21:errors.append('ROLE_COUNTS')
    if len(set(x['id'] for x in r['rows']))!=21:errors.append('COMMENT_IDENTITIES')
    for row in r['rows']:
        if row['status'] not in ('RESOLVED','JUSTIFIED_LIMITATION'):errors.append(row['id']+':UNDISPOSED')
        if not row['response'] or not row['evidence']:errors.append(row['id']+':EMPTY_RESPONSE')
        for evidence in row['evidence']:
            file=evidence.split(': ',1)[0]
            if not (ROOT/file).is_file() and not (ROOT/file).is_dir():errors.append(row['id']+':MISSING_EVIDENCE:'+file)
    for file,expected in r['reviewed_source_sha256'].items():
        if hashlib.sha256((ROOT/file).read_bytes()).hexdigest()!=expected:errors.append('REVIEWED_SOURCE_CHANGED:'+file)
    link_rows=[]
    for p in (ROOT/'submission-final').rglob('*.tex'):
        text=p.read_text()
        for kind,ref,path in re.findall(r'https://github\.com/ByronLi0207/financial-mathematics-paper-20261020/(blob|tree)/([^/}]+)(?:/([^}\s]*))?',text):
            if ref!='final-jof':errors.append('FINAL_SOURCE_OLD_BRANCH_LINK:'+ref)
            if not (ROOT/path).exists():errors.append('LINK_PATH_MISSING:'+path)
            link_rows.append(dict(source=str(p.relative_to(ROOT)),ref=ref,path=path,exists=(ROOT/path).exists()))
        # Only a link inside the balanced visible-text argument is nested;
        # sequential hyperlinks on one line are valid separate references.
        for m in re.finditer(r'\\href\{[^}]*\}\{',text):
            depth=1;i=m.end();start=i
            while i<len(text) and depth:
                if text[i]=='{' and text[i-1]!='\\':depth+=1
                elif text[i]=='}' and text[i-1]!='\\':depth-=1
                i+=1
            if r'\href' in text[start:i-1]:errors.append('NESTED_LINK:'+str(p.relative_to(ROOT)))
    legacy=json.loads((ROOT/'results/revision-v8/wp3/summary.json').read_text());legacy_counts=collections.Counter(x['method'] for x in legacy['cells'])
    if legacy_counts!={'F':72,'QR4':72,'QR33':72}:errors.append('CONTROLLED_CENSUS')
    frozen={}
    for key,ref,paths in [('protocol','effa537bd6d9b89855002aa79f95f62f9ff3761c',['protocol/final-merge','final_merge_wp2.py','run_final_merge_wp2.py','verify_final_merge_wp2.py','test_final_merge_wp2.py']),('results','3396aed2b88e99c66bcb8c602911e65698d0d1ba',['results/final-merge/wp2-cftc-mechanism'])]:
        changed=subprocess.check_output(['git','diff','--name-only',ref,'--']+paths,cwd=ROOT,text=True).splitlines();frozen[key]=changed
        if changed:errors.append('FIXED_'+key.upper()+'_CHANGED')
    changed=subprocess.check_output(['git','diff','--name-only','7629f0f3dfa6e388d2bbc15301f2bf21e30e7d7e','--','results','protocol'],cwd=ROOT,text=True).splitlines()
    if changed:errors.append('ANY_SCIENTIFIC_OUTPUT_OR_PROTOCOL_CHANGED_SINCE_WP5')
    language=json.loads((ROOT/'notes/final-merge/wp6-language-audit.json').read_text());docs=json.loads((ROOT/'notes/final-merge/wp6-document-audit.json').read_text())
    if language['status']!='PASS' or docs['status']!='PASS':errors.append('LANGUAGE_OR_DOCUMENT_GATE')
    out=dict(status='PASS' if not errors else 'MISMATCH',mismatch_count=len(errors),mismatches=errors,role_counts=dict(counts),comments=21,major_count=r['major_count'],undisposed_major=0,explicit_retained_limitations=r['retained_limitations'],controlled_records=dict(legacy_counts),local_link_count=len(link_rows),local_links=link_rows,frozen_diffs=frozen,scientific_paths_changed_since_wp5=changed,language_gates=language['gates'],document_counts=docs['counts'],source_sha256=r['reviewed_source_sha256'],scope='Single-executor reading and writing checkpoint. Local link existence is not remote publication proof; retained scientific/rights/provenance limits remain. Full final-page QA and fresh full pytest remain WP8.',new_model_fits=0)
    (ROOT/'notes/final-merge/wp6-review-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('local_links','source_sha256','document_counts')},indent=2));raise SystemExit(bool(errors))

if __name__=='__main__':main()
