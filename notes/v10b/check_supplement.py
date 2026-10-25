"""Read-only scientific checks for the document-only supplement edit."""
from pathlib import Path
import hashlib, json, re, subprocess
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'submission-v10/supplement.tex'
DEV=ROOT/'.scratch/v10b/supp-dev'
original=subprocess.check_output(['git','show','23fd9fa:submission-v10/supplement.tex'],cwd=ROOT).decode()
current=P.read_text()
source=json.loads((ROOT/'notes/v10b/supplement-moved-passages.json').read_text())
sha=lambda b: hashlib.sha256(b).hexdigest()
assert sha(original.encode())==source['original_source_sha256']
for p in source['passages']:
    assert p['original_tex'] in original
    if p['replacement_tex']:
        assert p['replacement_tex'] in current

# Human-readable column heads and captions may change; all inline data regions
# between the repeated-head/foot declarations and table endings remain intact.
table_body_pattern=r'\\endfoot\s*\n(.*?)\\end\{longtable\}'
assert re.findall(table_body_pattern,original,re.S)==re.findall(table_body_pattern,current,re.S)
assert re.findall(r'\\input\{[^}]+\}',original)==re.findall(r'\\input\{[^}]+\}',current)
sections=lambda s: re.findall(r'\\section\{([^}]+)\}\\label\{([^}]+)\}',s)
assert sections(original)==sections(current)
assert len(sections(current))==34
assert re.findall(r'\\author\{[^}]*\}',original)==re.findall(r'\\author\{[^}]*\}',current)
assert '\\setcounter{tocdepth}{1}' in current
assert 'revision-v10b/notes/v10b/supplement-audit-records.md' in current
reader=PdfReader(DEV/'supplement.pdf')
assert len(reader.pages)<=33
log=(DEV/'supplement.log').read_text()
assert 'Overfull' not in log
assert not re.search(r'(?:Reference|Citation).*undefined',log)
assert len(list((DEV/'render-final').glob('page-*.png')))==len(reader.pages)

reasons={
1:'Retain the path target, strict-event proof and logical construction; no execution metadata in the scientific argument.',
2:'Keep the source attribution and proof assumptions; move source-consultation bookkeeping to A2.',
3:'Keep seeds, path counts, process and shared-stream definitions: these specify the Monte Carlo design, not administrative logs.',
4:'Keep every primary/sensitivity rate, uncertainty qualification and nonfailure boundary; these are results.',
5:'Keep initialized-path counts, shared thresholds, endpoint moments and zero-count limits: these define the sensitivity and its interpretation.',
6:'Keep all comparisons, named inference families and adverse directions; archive links are access routes to scientific results.',
7:'Keep recursion, fitted-parameter eligibility, all comparisons and exploratory status; move numerical readback receipt to A3.',
8:'Keep rank definitions, endpoint nonuniqueness and annual/sparse sensitivities; these define the benchmark.',
9:'Keep exact rational reversal boundaries, native amounts and absence of observed decision costs; these are results and interpretation.',
10:'Keep the frozen v9 table link and exact rational field access; this is the scientific frontier inventory, not a run log.',
11:'Keep panel identity, units, complete results, procedure distinctions and dependence boundary.',
12:'Keep selection-before-evaluation chronology and archive link; move arithmetic-check bookkeeping to A4.',
13:'Keep complete endpoint-plug-in outcomes and original failure/candidate inventory access; these are scientific evidence.',
14:'Keep retrospective status, previous viewing, fixed rule order, fold geometry and chronological sealing: interpretation depends on them.',
15:'Keep exact mandatory-candidate failure statuses and analogue-versus-replication boundary; these are outcomes.',
16:'Keep feedback maturity, update conventions, selection criterion, optimizer limits and NA statuses: these define the procedures.',
17:'Keep comparison-family slots, missing p-values and freeze chronology; linked update equations are technical specifications.',
18:'Keep fixed combination definitions, all counts and missing-constituent statuses; these are scientific procedure/results.',
19:'Keep breakpoint-sign calculation, all crossing results, comparison-family scope and selection limits.',
20:'Keep training-defined state cuts, unchanged reports, all group results and unverified inference assumptions.',
21:'Keep target-specific selections preceding evaluation and NA outcomes; move receipt wording to A5.',
22:'Keep horizon ordering, every crossing and fixed-terminal hit diagnostic; no anytime or independent-validation claim.',
23:'Keep mature-label clocks, normalized objective, eligibility contracts, numerical acceptance and working-reference conventions; move builder/receipt metadata to A6.',
24:'Keep complete frozen simulation design, seeds, MCSE, clear-gain screen, all failure context and numerical-grid links; move receipt and duplicate-heatmap routing to A7.',
25:'Keep day-closing rule, source-naive timing, exact split, results and nonredistribution; move fingerprint/private mapping routing to A8.',
26:'Keep later-selected penalties, every overlap/index bound, fixed screen, raw-HAC formula and all unavailable outcomes; chronology is essential.',
27:'Keep separate calibrated laws, estimand, full failures, missing residual/gap limitations and unsupported/unassessable classifications.',
28:'Keep bootstrap count, moment gate, cut rule, starts/retries, state continuation, failed cells and conclusions; all affect interpretation.',
29:'Keep menu, tie/failure rule, shared streams, phase denominator, pilot/formal order, pre-output design and M1-M3 thresholds/results.',
30:'Keep official source years, eligibility, economic/release dates, information gaps, all method/update settings and post-acquisition format chronology; move only transport timestamps/bytes/hashes/unobserved API fields to A9.',
31:'Keep MCS bootstrap/software settings, deterministic seed/order design, full-grid construction, loss duplicates, unavailable slots and all membership measures.',
32:'Keep exact cost definition, native units, reference scaling, complete coefficient grid, same-origin floor matching, planned denominators and all-method archive routes.',
33:'Keep original test families, complete diagnostics and Murphy plots; only figure display numbering gains the S prefix.',
34:'Keep public availability, compatible-input and nonreplication limits plus full-result routes; move version administration, builder/resources and receipt details to A10-A12.'
}
aux=(DEV/'supplement.aux').read_text()
labels={m[0]:dict(number=m[1],page=int(m[2])) for m in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{(\d+)\}',aux)}
rows=[]
for i,(title,label) in enumerate(sections(current),1):
    rows.append(dict(section=f'S{i}',title=title,label=label,page=labels[label]['page'],decision=reasons[i]))
source['final_source_sha256']=sha(current.encode())
(ROOT/'notes/v10b/supplement-moved-passages.json').write_text(json.dumps(source,indent=2)+'\n')
receipt=dict(status='NATIVE_COMPILE_AND_STRUCTURE_PASS_VISUAL_PENDING',pages=len(reader.pages),page_cap=33,
  original_pages=len(PdfReader(ROOT/'submission-v10/supplement.pdf').pages),
  supplement_source_sha256=sha(current.encode()),developer_pdf_sha256=sha((DEV/'supplement.pdf').read_bytes()),
  original_table_body_regions_byte_identical=True,original_inputs_byte_identical=True,
  scientific_section_labels_retained=34,author_placeholder_unchanged=True,verbatim_moved_passages=len(source['passages']),
  no_overfull=True,no_undefined_references_or_citations=True,underfull_warnings=log.count('Underfull'),
  final_pdf_not_overwritten=True,sections=rows,labels=labels,
  layout_only_changes=['tocdepth=1 native compact section TOC','Supplementary figure S prefix','Removed forced page breaks before S29 and S32 to avoid stranded continuation and fit 32 pages'],
  residual_risks=['Generated v10-menu-full.tex has its existing label repeated in the continuation head; fixed table number S33 is unchanged.',
  'The branch-specific audit URL becomes publicly resolvable only after revision-v10b is pushed.'])
(ROOT/'notes/v10b/supplement-check.json').write_text(json.dumps(receipt,indent=2)+'\n')
md='# Supplement audit/run-metadata decisions by section\n\nAll 34 scientific sections, every existing input and all inline table data regions are retained. Headers and captions use readable method names. Administrative passages are archived verbatim in [supplement-audit-records.md](supplement-audit-records.md). These judgments were made section by section; words such as seed, failure, frozen and chronology do not by themselves make a passage removable.\n\n| Section | Label | Final development page | Decision and reason |\n|---|---|---:|---|\n'
for r in rows:
    md+=f"| {r['section']}: {r['title']} | `{r['label']}` | {r['page']} | {r['decision']} |\n"
md+='\nThe native development compile has '+str(len(reader.pages))+' pages. The original 33-page canonical PDF is unchanged. No experiment, source data, result, protocol or generated table was changed by this task.\n'
(ROOT/'notes/v10b/supplement-metadata-decisions.md').write_text(md)
print(json.dumps({k:receipt[k] for k in ['status','pages','original_table_body_regions_byte_identical','scientific_section_labels_retained','no_overfull','no_undefined_references_or_citations']}))
