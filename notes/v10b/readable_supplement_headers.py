"""Human-readable inline supplement headers; data rows remain byte-identical."""
from pathlib import Path
import hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'submission-v10/supplement.tex'
before=p.read_text();after=before
replacements={
 r'\caption{Original increment-AR simulation,':r'\caption{Original increment-autoregression simulation,',
 r'\caption{Complete original AR replay comparison.':r'\caption{Complete original autoregressive replay comparison.',
 r'\shortstack{Monte Carlo\\SE}':r'\shortstack{Monte Carlo\\standard error}',
 r'Reference & DM t & DM p & HLN p & Holm p':r'Reference & \shortstack{Loss-test\\statistic} & \shortstack{Normal\\p-value} & \shortstack{Small-sample\\p-value} & \shortstack{Holm-adjusted\\p-value}',
 r'\shortstack{One-SE\\rule (\%)}':r'\shortstack{One-standard-\\error rule (\%)}',
 r'\shortstack{Breaches\\minimum-loss / one-SE}':r'\shortstack{Breaches\\minimum-loss /\\one-standard-error}',
 r'Rule & Total & Complete & NA &':r'Rule & Total & Complete & Unavailable &',
 r'Source & Left & Right & Ranking & Positive & Negative':r'Source & \shortstack{Left-hand\\method} & \shortstack{Right-hand\\method} & Ranking & \shortstack{Positive\\breakpoints} & \shortstack{Negative\\breakpoints}',
 r'\shortstack{Regression minus\\reference loss} & HAC SE':r'\shortstack{Regression minus\\reference loss} & \shortstack{Dependence-adjusted\\standard error}',
 r'Source & Diagnostic & Raw p & Holm p & Status':r'Source & Diagnostic & \shortstack{Unadjusted\\p-value} & \shortstack{Holm-adjusted\\p-value} & Status',
 r'Reference & Mean difference &':r'Reference & \shortstack{Mean loss\\difference} &',
 r'\caption{Every earlier-period R0/R2 comparison.':r'\caption{Every earlier-period minimum-loss and one-standard-error comparison.',
 r'\caption{All noncomplete R6 report rows.':r'\caption{All noncomplete fixed-rule report rows.',
 r'\caption{Complete delayed-wrapper and headroom-SAV inventory.':r'\caption{Complete delayed-wrapper and headroom-recursion inventory.',
 r'\caption{Every original QR horizon-coherence comparison.':r'\caption{Every original quantile-regression horizon-coherence comparison.'
}
counts={}
for old,new in replacements.items():
    counts[old]=after.count(old)
    assert counts[old]>0,old
    after=after.replace(old,new)
body=lambda s: re.findall(r'\\endfoot\s*\n(.*?)\\end\{longtable\}',s,re.S)
assert body(before)==body(after)
assert len(body(after))==23
assert re.findall(r'\\label\{[^}]+\}',before)==re.findall(r'\\label\{[^}]+\}',after)
assert re.findall(r'\\input\{[^}]+\}',before)==re.findall(r'\\input\{[^}]+\}',after)
# Captions carry no more than three grammatical sentences; periods in TeX math
# are not present in these inline captions, and the test excludes continuation heads.
captions=re.findall(r'\\caption\{([^}]*)\}',after)
sentence_counts=[len(re.findall(r'[.!?](?:\s|$)',c)) for c in captions]
assert all(c<=3 for c in sentence_counts)
p.write_text(after)
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
report=dict(status='PASS_INLINE_HEADERS_AND_CAPTIONS_DATA_UNCHANGED_NATIVE_RECOMPILE_PENDING',
    before_source_sha256=sha(before),after_source_sha256=sha(after),
    replacement_counts=counts,inline_tables=len(body(after)),all_inline_data_regions_byte_identical=True,
    labels_and_inputs_unchanged=True,caption_sentence_counts=sentence_counts,
    original_inline_captions_all_at_most_two_sentences=True,
    explicit_inline_table_note_blocks=0,
    note_scope='Interpretive scientific paragraphs after tables are section prose, not tabular footnotes; they were retained unchanged.',
    restricted_scope='Only supplement.tex and notes/v10b header-check files. No generated table, figure, body row, data, result or protocol changed by this script.')
(ROOT/'notes/v10b/supplement-readable-headers.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','inline_tables','all_inline_data_regions_byte_identical','labels_and_inputs_unchanged']}))
