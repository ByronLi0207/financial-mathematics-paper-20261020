"""Regression checks for the actual recovered math failures, not financial fits."""
import unittest,copy,re
from v3_math_format import normalize_math,prepare_tex_math,restore_tex_math,text_math

class MathematicalTypesetting(unittest.TestCase):
    def content(self,blocks):
        return dict(title='Math fixture',subtitle='',date='',sections=[dict(title='Appendix C. Numerical conventions',blocks=blocks)],references=[],abstract='',figures=[])
    def test_recovered_parameterization_has_real_symbols(self):
        c=self.content([dict(type='p',html='B(i)=mu(B)+s(B)z(i,B). With alpha=mu(B)+a beta(0), theta=a beta+s(B)e(B), multiplying the headroom objective by a gives an equivalent unprojected peak objective with shifted penalty')])
        normalize_math(c)
        text=str(c)
        self.assertNotRegex(text,r'alpha=mu|\bphi1\b')
        self.assertTrue(any(b['type']=='equation' and '\\alpha_' in b['latex'] for b in c['sections'][0]['blocks']))
        self.assertIn('α',text);self.assertIn('μ',text)
    def test_full_inline_formula_is_single_math_span(self):
        c=self.content([dict(type='p',html='Choose k=ceil((n+1)τ)≤n.')])
        normalize_math(c);prepared,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(prepared),bindings)
        self.assertIn(r'\(k=\lceil(n+1)\tau\rceil\le n\)',tex)
        self.assertNotRegex(tex,r'(?<![A-Za-z\\])ceil\(')
    def test_membership_does_not_consume_english_phi(self):
        # A partial-token replacement changed a recursion into a set relation.
        source='fix common coefficients c and phi in N<sub>s+1</sub>=c+phi N<sub>s</sub>+epsilon<sub>s</sub>.'
        self.assertIn('φ in N<sub>s+1</sub>',text_math(source))
        self.assertNotIn('φ∈N',text_math(source))
        self.assertIn(':i∈N<sub>',text_math(':i in N<sub>t,κ,k</sub>'))
    def test_absolute_value_is_not_norm(self):
        c=self.content([dict(type='equation',html='|max<sub>h</sub>|Ñ<sub>i,h</sub><super>tr</super>(x)|−max<sub>h</sub>|M<sub>i,h</sub>(x)‖≤max<sub>0≤h≤H</sub>|1−φ<super>h</super>| |x−N<sub>i</sub>|.',latex=r'\left|a-b\right|\le c.')])
        normalize_math(c)
        self.assertNotIn('‖',c['sections'][0]['blocks'][0]['html'])
    def test_notation_cells_use_whole_tex_expressions(self):
        c=self.content([dict(type='table',caption='Notation.',headers=['Symbol','Definition'],rows=[['aκ; zᵢ,κ','Scale; feature'],['Jλ; Dλ','Objectives']])])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\(a_\kappa;\ z_{i,\kappa}\)',tex)
        self.assertIn(r'\(\mathcal J_\lambda;\ \mathcal D_\lambda\)',tex)
    def test_simple_numeric_reports_are_full_math_spans(self):
        c=self.content([dict(type='p',html='At H=6, ω=19 and k=52.')])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\(H=6\)',tex)
        self.assertIn(r'\(\omega=19\)',tex)
        self.assertIn(r'\(k=52\)',tex)
    def test_long_inline_formulas_and_caption_are_whole_math(self):
        c=self.content([dict(type='p',html='Vᵢ,ₜ=max{x+uᵢ,−x−lᵢ}; max(1,|Jλ|,|Dλ|).'),dict(type='table',caption='Table D1. FX divided by 10^6.',headers=['Value'],rows=[['All ω >= 0']])])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\(V_{i,t}=\max\{x+u_i,-x-l_i\}\)',tex)
        self.assertIn(r'\(\max(1,|\mathcal J_\lambda|,|\mathcal D_\lambda|)\)',tex)
        self.assertIn(r'\(10^6\)',tex)
        self.assertNotIn('textasciicircum',tex)
        self.assertIn('≥',c['sections'][0]['blocks'][1]['cell_html']['All ω >= 0'])
    def test_figure_caption_uses_whole_formula_binding(self):
        c=self.content([]);c['figures']=[dict(path='fixture.pdf',caption='At fixed τ=0.95, retain crossings.')]
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\(\tau=0.95\)',tex)
    def test_canonical_positive_parts_and_equal_window_binding(self):
        c=self.content([dict(type='p',html='Mean overrun averages (P−C)₊; unused averages (C−P)₊. The two selected k=W52 reports match.')])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\((P-C)_+\)',tex)
        self.assertIn(r'\((C-P)_+\)',tex)
        self.assertIn(r'\(k=W=52\)',tex)
        self.assertNotIn(r'\(k=W\)52',tex)
    def test_catalog_does_not_bind_inside_larger_identifiers(self):
        c=self.content([dict(type='p',html='A diagnostic token look=Winter should retain its characters.')])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn('look=Winter',tex)
    def test_current_source_preserves_input_and_idempotence(self):
        c=self.content([dict(type='p',html='At exact phi1, use epsilon(s) and tau=.95.'),dict(type='equation',html='W<super>−1</super> sum ‖θ‖<super>2</super>.',latex=r's_{rB}+\alpha')])
        before=copy.deepcopy(c);normalize_math(c);once=copy.deepcopy(c);normalize_math(c)
        self.assertEqual(c,once)
        self.assertIn('phi1',str(before));self.assertNotIn('phi1',str(c));self.assertNotIn('s_{rB}',str(c))
    def test_round2_table_norm_and_persistence_delta_are_whole_math(self):
        c=self.content([dict(type='table',caption='For boundary fits, δ is persistence minus one.',headers=['‖β‖₂ range','δ'],rows=[['unchanged','unchanged']])])
        normalize_math(c);d,bindings=prepare_tex_math(c)
        from build_tex import build_source
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'\(\|\beta\|_2\) range',tex)
        self.assertEqual(tex.count(r'\(\delta\)'),2)
        self.assertNotRegex(tex,'[δβ₂]')
    def test_adjacent_variance_word_does_not_block_the_complete_formula(self):
        c=self.content([dict(type='p',html='Innovations of variance1−φ² are specified.')])
        from v3_revision import restore_prose_spacing
        from round2_inline_math import bind_round2_math
        from build_tex import build_source
        restore_prose_spacing(c);normalize_math(c)
        c['sections'][0]['title']='Appendix J. Simulation'
        bind_round2_math(c);d,bindings=prepare_tex_math(c)
        tex=restore_tex_math(build_source(d),bindings)
        self.assertIn(r'variance \(1-\phi^2\)',tex)
        self.assertNotIn('²',tex)
if __name__=='__main__':unittest.main()
