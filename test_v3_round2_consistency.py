import json,unittest
from v3_revision import ROOT,plain
class Round2ContentAudit(unittest.TestCase):
 def test_conclusion_count_includes_every_paragraph(self):
  c=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text());a=json.loads((ROOT/'results/revision-20261023/writing-audit.json').read_text());section=next(s for s in c['sections'] if s['title'].startswith('10.'))
  words=sum(len(plain(b['html']).split()) for b in section['blocks'] if b['type']=='p');self.assertEqual(a['conclusion_words'],words);self.assertLessEqual(words,200)
 def test_original_primaries_and_all_holm_rows_retained(self):
  c=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text());h=next(b for s in c['sections'] for b in s['blocks'] if b['type']=='table' and b['caption'].startswith('Table H2.'));self.assertEqual(len(h['rows']),72)
  a=c['abstract'];self.assertIn('14.77%',a);self.assertIn('50.79%',a);self.assertIn('360 to 376',a);self.assertIn('28 to 54',a)

 def test_D2_new_formulas_are_whole_TeX_math_spans(self):
  from build_revision_v3 import tex_source
  c=json.loads((ROOT/'manuscript/revision-v3/paper-content.json').read_text());tex=tex_source(c)
  for formula in [r'S_0=0',r'S_h=\sum_{j=1}^{h}X_j',r'q=\inf\{u:\Pr(|S_H|\le u)\ge0.975\}',r'\lceil39(W+1)/40\rceil']:
   self.assertIn(r'\('+formula+r'\)',tex)
