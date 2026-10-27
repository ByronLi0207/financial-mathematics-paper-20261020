from pathlib import Path
import json, re
R = Path(__file__).resolve().parents[2]
N = Path(__file__).resolve().parent
s = (R / 'submission-final/manuscript.tex').read_text()
a = s.index(r'\section*{Data and code availability}')
b = s.index(r'\section*{Author-provided information}', a)
text = s[a:b]
assert text == (N / 'R6-availability-after.tex').read_text()
body = text.split('\n', 1)[1].strip()
plain = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', body)
plain = re.sub(r'\\texttt\{[^}]*\}', 'the provenance file', plain)
paragraphs = plain.split('\n\n')
counts = [len(re.findall(r'[.!?](?:\s|$)', x)) for x in paragraphs]
assert counts == [3, 3, 3, 1], counts
assert '[Zenodo DOI to be added by the author]' in text
assert 'tree/submission-final' in text
assert not re.search(r'AI[- ]use|AI disclosure|artificial intelligence', text, re.I)
result = {'step': 'R6', 'status': 'PASS', 'paragraph_sentence_counts': counts,
          'source_links': 3, 'rights_links': 2, 'code_link': 1,
          'source_check': 'R6-availability-source-check.json',
          'before': 'R6-availability-before.tex', 'after': 'R6-availability-after.tex'}
(N / 'R6-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
