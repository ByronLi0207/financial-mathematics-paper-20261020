"""V7 S6 reproducible sentence statistics, with a fixed before/after scope.

Scope: abstract separately; main prose and figure captions before declarations
or references. Tables, their notes, displayed equations, headings and the
heading explicitly named Research design and transparency are excluded.
The older named whole section and the new subsection use the same name rule.
Citation years and numbers in inline mathematics count toward the per-sentence
numeric limit. Decimal/scientific values are single numbers; a ratio has two.
"""
import argparse
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BANNED=["retained","declared","frozen","receipt","archive(d)","byte","hash",
        "post-result","exploratory","inspected","stipulated","issued","admissible",
        "source-specific","no ... is claimed","does not establish"]


def plain(text, labels):
    def citation(m):
        return " ("+"; ".join(labels.get(k.strip(),k.strip()) for k in m.group(1).split(","))+") "
    text=re.sub(r"\\cite(?:p|t|alp)?\{([^}]+)\}",citation,text)
    text=re.sub(r"\\(?:ref|label)\{[^}]*\}"," ",text)
    text=re.sub(r"(\d+(?:\.\d+)?)\s*\\times\s*10\^\{?(-?\d+)\}?",r"\1e\2",text)
    text=re.sub(r"\\(?:href|url)\{[^}]*\}"," ",text)
    text=text.replace("\\%","%").replace("~"," ")
    text=re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?"," ",text)
    text=re.sub(r"[{}$\\]"," ",text)
    return re.sub(r"\s+"," ",text).strip()


def sentences(text):
    for pattern in (r"\bet al\.",r"\be\.g\.",r"\bi\.e\.",r"\bn\.r\.",r"\bn\.d\.",r"\bU\.S\."):
        text=re.sub(pattern,lambda m:m.group().replace(".","\ue000"),text,flags=re.I)
    result=re.split(r"(?<=[!?])\s+|(?<!\d)\.(?:\s+|$)|(?<=\d)\.(?=\s+[A-Z])",text)
    return [part.replace("\ue000",".").strip() for part in result if re.search(r"[A-Za-z]",part)]


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",text))


def numeric_count(text):
    return len(re.findall(r"(?<![A-Za-z])\d+(?:,\d{3})*(?:\.\d+)?(?:[eE][+-]?\d+)?",text))


def metrics(path):
    tex=path.read_text()
    labels={key:label for label,key in re.findall(r"\\bibitem\[([^\]]+)\]\{([^}]+)\}",tex)}
    # Older text uses plain author-year passages, so no citation substitution is needed there.
    abstract=re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",tex,re.S).group(1)
    abstract=plain(abstract,labels)
    start=re.search(r"\\section\*?\{(?:1\. )?Introduction\}",tex)
    body=tex[start.start():]
    body=re.split(r"\\section\*?\{(?:Declarations and availability|Data and code availability|References)\}",body)[0]
    body=re.sub(r"\\begin\{table\}.*?\\end\{table\}","\n\n",body,flags=re.S)
    body=re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}","\n\n",body,flags=re.S)
    body=re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}","\n\n",body,flags=re.S)
    body=re.sub(r"\\begin\{samepage\}.*?\\end\{samepage\}","\n\n",body,flags=re.S)
    body=re.sub(r"\{\\footnotesize Hit tests.*?\}\s*", "\n\n", body,flags=re.S)
    body=re.sub(r"\\\[.*?\\\]","\n\n",body,flags=re.S)
    # Preserve figure-caption prose, not image filenames or geometry commands.
    body=re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}","",body)
    excluded=[]
    pattern=r"\\(section|subsection)\*?\{([^}]*Research design and transparency[^}]*)\}.*?(?=\\(?:section|subsection)\*?\{|\Z)"
    for m in re.finditer(pattern,body,flags=re.S):excluded.append(m.group(2))
    body=re.sub(pattern,"\n\n",body,flags=re.S)
    body=re.sub(r"\\(?:section|subsection|paragraph)\*?\{[^}]*\}","\n\n",body)
    body=re.sub(r"\\textbf\{(?:C[123]\.|Contribution on[^}]+|Proposition[^}]+)\}","",body)
    body=re.sub(r"\\(?:begin|end)\{(?:figure|center|minipage)\}(?:\[[^\]]*\])?","",body)
    body=body.replace(r"\FloatBarrier","").replace(r"\centering","")
    paragraphs=[plain(part,labels) for part in re.split(r"\n\s*\n",body)]
    paragraphs=[p for p in paragraphs if re.search(r"[A-Za-z]",p)]
    all_sentences=[s for p in paragraphs for s in sentences(p)]
    lengths=[word_count(s) for s in all_sentences]
    negatives=[s for s in all_sentences if re.search(r"\b(?:not|no|neither|nor|cannot)\b",s,re.I)]
    banned={}
    full=" ".join(paragraphs)
    for term in BANNED:
        if term=="archive(d)":pattern=r"\barchive(?:d|s)?\b"
        elif term=="no ... is claimed":pattern=r"\bno\b[^.!?]*\bis claimed\b"
        else:pattern=r"\b"+re.escape(term)+r"\b"
        banned[term]=len(re.findall(pattern,full,flags=re.I))
    numeric_violations=[dict(sentence=s,numbers=numeric_count(s)) for s in all_sentences if numeric_count(s)>2]
    paragraph_violations=[dict(paragraph=p,sentences=len(sentences(p))) for p in paragraphs if len(sentences(p))>6]
    long=[s for s,n in zip(all_sentences,lengths) if n>35]
    report=dict(source=str(path.relative_to(ROOT)),abstract_words=word_count(abstract),abstract_numbers=numeric_count(abstract),
                main_sentences=len(all_sentences),main_words=sum(lengths),mean_sentence_words=sum(lengths)/len(lengths),
                sentences_over35=len(long),over35_percent=100*len(long)/len(lengths),negation_sentences=len(negatives),
                negation_percent=100*len(negatives)/len(lengths),max_numbers_per_sentence=max(map(numeric_count,all_sentences)),
                numeric_violations=numeric_violations,paragraphs_over6=paragraph_violations,banned_counts=banned,
                excluded_transparency=excluded,abstract_text=abstract,long_sentences=long)
    report['pass_quantitative']=(report['abstract_words']<=180 and report['abstract_numbers']<=5 and
        18<=report['mean_sentence_words']<=24 and report['over35_percent']<=8 and report['negation_percent']<=8 and
        not numeric_violations and not paragraph_violations and not any(banned.values()))
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output');parser.add_argument('--summary',action='store_true');parser.add_argument('--require-pass',action='store_true');args=parser.parse_args()
    before=metrics(ROOT/'manuscript/revision-v6-preserved/manuscript.tex')
    after=metrics(ROOT/'submission-jof/manuscript.tex')
    report=dict(before=before,after=after)
    if args.output:(ROOT/args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    if args.summary:
        keys=('abstract_words','abstract_numbers','main_sentences','main_words','mean_sentence_words',
              'sentences_over35','over35_percent','negation_sentences','negation_percent','max_numbers_per_sentence',
              'pass_quantitative')
        summary={name:{key:data[key] for key in keys} for name,data in report.items()}
        for name,data in report.items():
            summary[name]['paragraphs_over6']=len(data['paragraphs_over6'])
            summary[name]['banned_total']=sum(data['banned_counts'].values())
        summary['after_failures']={k:after[k] for k in ('numeric_violations','paragraphs_over6','banned_counts')}
        print(json.dumps(summary,indent=2,ensure_ascii=False))
    else:print(json.dumps(report,indent=2,ensure_ascii=False))
    if args.require_pass:raise SystemExit(not after['pass_quantitative'])


if __name__=='__main__':main()
