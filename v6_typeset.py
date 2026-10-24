"""Render source-bound v6 content without overwriting prior audit metrics."""
from pathlib import Path
import hashlib,json
from v4_submission import ROOT,OUT,plain
from v4_typeset import tex_document,pdf_document


def main():
    metrics={}
    for name in ('manuscript','supplement'):
        d=json.loads((OUT/(name+'-content.json')).read_text())
        (OUT/(name+'.tex')).write_text(tex_document(d))
        pages=pdf_document(d,OUT/(name+'-preview.pdf'))
        text=' '.join(plain(b.get('html',b.get('text',''))) for s in d['sections'] for b in s['blocks'] if b['type'] in ('p','subheading'))
        metrics[name]={'pages':pages,'prose_words_excluding_abstract_references_tables_captions':len(text.split()),'abstract_words':len(plain(d['abstract']).split()),'tables':sum(b['type']=='table' for s in d['sections'] for b in s['blocks']),'figures':len(d['figures']),'tex_sha256':hashlib.sha256((OUT/(name+'.tex')).read_bytes()).hexdigest(),'preview_sha256':hashlib.sha256((OUT/(name+'-preview.pdf')).read_bytes()).hexdigest()}
    metrics['budget_scope']='Project budget only: <=9000 main prose words, <=6 tables, <=4 figures. No numerical journal word/page cap was verified in the official preparation guidance.'
    m=metrics['manuscript']
    if m['prose_words_excluding_abstract_references_tables_captions']>9000 or m['tables']>6 or m['figures']>4:raise ValueError('PROJECT_MAIN_BUDGET_EXCEEDED')
    (ROOT/'notes/revision-v6/document-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
