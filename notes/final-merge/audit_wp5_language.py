"""Fixed, display-only WP5 language census; never computes forecast results.

The rule is established against the saved WP4 source before WP5 prose edits.
Abstract and all scholarly main text through the conclusion are primary.
Captions and table explanatory notes are included; tabular cells, headings,
displayed formulae, bibliography, URLs and citation/reference identifiers are
excluded. Inline-math numerical literals remain. Availability prose is also
reported, separately. Spelled numerals count, including hyphenated numerals;
model identifiers such as QR33 and P1 are identifiers, not observed values.
"""
from pathlib import Path
import argparse, hashlib, json, re

ROOT=Path(__file__).resolve().parents[2]
WORD=re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[,.]\d+)*(?:/\d+(?:\.\d+)?)?")
VALUE=re.compile(r"(?<![A-Za-z0-9])[-+]?\d+(?:,\d{3})*(?:\.\d+)?(?![A-Za-z0-9])|\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)\b",re.I)
NEG=re.compile(r"\b(?:not|no|never|neither|nor|cannot|without|can't|don't|doesn't|isn't|aren't|wasn't|weren't|hasn't|haven't|won't|wouldn't|couldn't|shouldn't)\b",re.I)
BROAD_NEG=re.compile(r"\b(?:unavailable|unidentified|unresolved|unmeasured|unobserved|uneliminated|incomplete|fail\w*|adverse|miss\w*)\b",re.I)
BANNED=[r'finite[ -]penalty\s+hindsight',r'constant[ -]parameter\s+median\s+excess\s+loss',r'switching\s+adds?\s+no\s+observed\s+median\s+loss',r'history[ -]to[ -]horizon\s+displays?',r'cutpoint\s+bands?',r'prespecified\s+history[ -]region\s+screens?',r'pooled\s+simulation\s+tasks?',r'issue\s+origins?',r'completed[ -]label\s+pools?',r'source[ -]native']

def command_arg(text,start):
    if text[start]!='{':raise ValueError('expected argument')
    depth=1;i=start+1
    while i<len(text) and depth:
        if text[i]=='{' and text[i-1]!='\\':depth+=1
        elif text[i]=='}' and text[i-1]!='\\':depth-=1
        i+=1
    if depth:raise ValueError('unbalanced TeX')
    return text[start+1:i-1],i

def remove_commands(text,names):
    pattern=re.compile(r'\\(?:'+names+r')\*?(?:\[[^\]]*\])?\s*\{')
    while (m:=pattern.search(text)):
        _,end=command_arg(text,m.end()-1);text=text[:m.start()]+' '+text[end:]
    return text

def clean(raw):
    raw=re.sub(r'(?<!\\)%[^\n]*','',raw)
    raw=re.sub(r'\\begin\{(?:tabular|tabular\*)\}.*?\\end\{(?:tabular|tabular\*)\}',' ',raw,flags=re.S)
    raw=re.sub(r'\\\[.*?\\\]|\\begin\{(?:equation\*?|align\*?)\}.*?\\end\{(?:equation\*?|align\*?)\}',' ',raw,flags=re.S)
    raw=re.sub(r'\\setlength\{[^}]*\}\{[^}]*\}',' ',raw)
    raw=re.sub(r'\\begin\{minipage\}(?:\[[^\]]*\])?\{[^}]*\}',' ',raw)
    raw=remove_commands(raw,r'section|subsection|subsubsection|paragraph|cite\w*|label|ref|eqref|url|includegraphics|refstepcounter')
    # A hyperlink's visible wording belongs to the prose; its URL does not.
    raw=remove_commands(raw,r'href')
    raw=re.sub(r'\\input\{[^}]*\}',' ',raw)
    raw=re.sub(r'\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?',' ',raw)
    raw=re.sub(r'\\item\b','\n\n',raw)
    raw=re.sub(r'\\textbf\{([^{}]*\.)\}', ' ',raw) # bold paragraph recommendation labels
    raw=raw.replace(r'\%', '%').replace(r'\&','and').replace('~',' ')
    raw=re.sub(r'\\[A-Za-z]+\*?(?:\[[^\]]*\])?',' ',raw)
    raw=raw.replace('$',' ').replace(r'\(',' ').replace(r'\)',' ')
    raw=raw.translate(str.maketrans({'{':' ','}':' ','\\':' ','_':' '}))
    raw=re.sub(r'\b([A-Za-z]+)(\d+)\b',r'\1ID',raw) # scientific/model and section identifiers
    raw=raw.replace('U.S.','US').replace('e.g.','eg').replace('i.e.','ie')
    return raw

def sentences(raw):
    rows=[]
    for para in re.split(r'\n\s*\n',clean(raw)):
        para=' '.join(para.split())
        if not para:continue
        # A decimal point is not a sentence boundary. Paragraph endings count
        # as sentence/fragment endings instead of silently discarding text.
        for sentence in re.split(r'(?<=[.!?])\s+',para):
            if not re.search(r'[A-Za-z]{2}',sentence):continue
            words=WORD.findall(sentence);values=VALUE.findall(sentence)
            rows.append(dict(text=sentence,words=len(words),numeric_values=values,numeric_value_count=len(values),grammatical_negation=bool(NEG.search(sentence)),adverse_or_uncertainty_lexicon=bool(BROAD_NEG.search(sentence))))
    return rows

def census(raw):
    raw=raw.split(r'\begin{document}',1)[-1].split(r'\begin{thebibliography}',1)[0]
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',raw,re.S).group(1)
    start=raw.index(r'\begin{abstract}');end=raw.index(r'\section*{Data and code availability}')
    primary=raw[start:end]
    primary=re.sub(r'\\noindent\\textbf\{Keywords:\}.*?\\par\\medskip',' ',primary,flags=re.S)
    primary=re.sub(r'\\refstepcounter\{proposition\}\\noindent\\textbf\{Proposition.*?\}\\label\{[^}]*\}',' ',primary,flags=re.S)
    # A displayed identity interrupts a sentence typographically. Its symbols
    # belong to the separate formula census; keep surrounding prose together.
    primary=re.sub(r'\s*\\\[.*?\\\]\s*',' FORMULA ',primary,flags=re.S)
    # Expanded generated table text is data cells, not running sentences.
    rows=sentences(primary);arows=sentences(abstract)
    mean=sum(r['words'] for r in rows)/len(rows);neg=sum(r['grammatical_negation'] for r in rows)
    banned=[]
    for pattern in BANNED:
        banned.extend(dict(pattern=pattern,text=m.group()) for m in re.finditer(pattern,' '.join(re.sub(r'(?<!\\)%[^\n]*','',raw).split()),re.I))
    overloaded=[dict(sentence=i+1,**r) for i,r in enumerate(rows) if r['numeric_value_count']>2]
    return dict(rule_version='WP5-before-edit-v1',source_sha256=hashlib.sha256(raw.encode()).hexdigest(),abstract=dict(sentence_count=len(arows),word_count=sum(r['words'] for r in arows),sentences=arows),primary=dict(sentence_count=len(rows),word_count=sum(r['words'] for r in rows),mean_sentence_words=mean,grammatically_negative_sentences=neg,grammatically_negative_percent=100*neg/len(rows),adverse_or_uncertainty_sentences=sum(r['adverse_or_uncertainty_lexicon'] for r in rows),max_numeric_values=max(r['numeric_value_count'] for r in rows),overloaded_numeric_sentences=overloaded,sentences=rows),availability=sentences(raw[end:]),banned_count=len(banned),banned_matches=banned,gates=dict(abstract_five_sentences=len(arows)==5,abstract_at_most_170_words=sum(r['words'] for r in arows)<=170,mean_18_to_24=18<=mean<=24,every_sentence_at_most_two_numeric_values=not overloaded,grammatical_negatives_at_most_8_percent=100*neg/len(rows)<=8,banned_zero=not banned))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--enforce',action='store_true');a=p.parse_args();r=census(a.source.read_text());r['counting_rule_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();r['status']='PASS' if all(r['gates'].values()) else 'MISMATCH';a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('primary','abstract','availability')}|{'abstract':{k:v for k,v in r['abstract'].items() if k!='sentences'},'primary':{k:v for k,v in r['primary'].items() if k!='sentences'}},indent=2));raise SystemExit(a.enforce and r['status']!='PASS')
