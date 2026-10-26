"""Public-aggregate supplement inventories and contextual regeneration checks."""
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import re
import unittest


class SupplementTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("v6_supplement"),
                             "v6 supplement generator is not implemented")
        self.api = importlib.import_module("v6_supplement")

    def test_dense_diagnostics_break_at_separators_before_numeric_tokens(self):
        for key in ('wp2-coverage','wp3-coverage','wp5-coverage'):
            t=self.api.generated(key)
            column=t['headers'].index('Grid n/hits/rate')
            for row in t['rows']:
                self.assertIn(' / ',row[column])
        for key in ('wp2-dm','wp3-dm','wp4-tests','wp5-dm'):
            for row in self.api.generated(key)['rows']:
                self.assertIn('book= ',row[-1])

    def test_feedback_and_initial_training_normalizers_are_explained(self):
        aci=self.api.generated('wp2-definition')
        state=self.api.generated('wp4-definition')
        self.assertIn('Initialize',aci['html'])
        self.assertIn('err<sub>i</sub>',aci['html'])
        self.assertTrue(any('\\leftarrow' in x['latex'] for x in aci['inline_math']))
        self.assertIn('initial mature QR training response scale',state['html'])
        self.assertTrue(any('\\max' in x['latex'] and '10^{-12}' in x['latex'] for x in state['inline_math']))

    def test_matched_figure_captions_keep_the_source_specific_primary_identity(self):
        fx=self.api.generated('figure-wp3-fx_hourly')['caption']
        treasury=self.api.generated('figure-wp3-nyfed_weekly')['caption']
        self.assertIn('distinct from the original FX',fx)
        self.assertNotIn('original FX',treasury)
        self.assertIn('also the original-primary historical reference',treasury)

    def test_all_required_inventories_are_printed_without_selection(self):
        expected = {
            "inventory": 4, "wp2-methods": 24, "wp2-controls": 16, "wp2-coverage": 40,
            "wp2-validation": 24, "wp2-gammas": 64, "wp2-states": 16,
            "wp2-feedback": 16, "wp2-effects": 16, "wp2-pairs": 8, "wp2-sav": 8,
            "wp2-control-operations": 16, "wp2-dm": 56,
            "wp3-counts": 2, "wp3-methods": 112, "wp3-controls": 112,
            "wp3-relative": 112, "wp3-coverage": 224, "wp3-dm": 224, "wp3-murphy": 8,
            "wp4-groups": 6, "wp4-training": 2, "wp4-tests": 4, "wp4-diagnostics": 4,
            "wp5-selection": 4, "wp5-screen": 4, "wp5-candidates": 12,
            "wp5-scores": 12, "wp5-coverage": 12, "wp5-directions": 6, "wp5-dm": 6,
        }
        section = self.api.additional_section()
        self.assertEqual(section["title"], "S16. Additional benchmarks and robustness")
        tables = {b["_generator"][7:]: b for b in section["blocks"] if b["type"] == "table"}
        self.assertEqual(set(tables), set(expected))
        for key, count in expected.items():
            with self.subTest(key=key):
                table = tables[key]
                self.assertEqual(len(table["rows"]), count)
                self.assertLessEqual(len(table["headers"]), 8)
                self.assertTrue(all(len(row) == len(table["headers"]) for row in table["rows"]))
                self.assertTrue(all(isinstance(cell, str) for row in table["rows"] for cell in row))

    def test_all_na_and_identity_slots_remain_visible_with_bookkeeping_separate(self):
        for key, na_count in [("wp2-dm", 5), ("wp3-dm", 98), ("wp5-dm", 3)]:
            table = self.api.generated(key)
            raw_index = table["headers"].index("DM raw p")
            absent = [row for row in table["rows"] if row[raw_index] == "NA"]
            self.assertEqual(len(absent), na_count)
            self.assertTrue(all(re.search(r"\bbook=\s*1$",row[-1]) for row in absent))
        median = self.api.generated("wp3-methods")
        self.assertEqual(sum(row[-1].startswith("NA") for row in median["rows"]), 48)
        self.assertEqual(sum("Identical losses" in row[-1] for row in self.api.generated("wp3-dm")["rows"]), 2)
        self.assertEqual(sum("Not run" in row[3] for row in self.api.generated("wp2-gammas")["rows"]), 8)

    def test_complete_na_causes_and_all_lambda_candidates_are_readable(self):
        text = json.dumps(self.api.additional_section(), ensure_ascii=False)
        for phrase in ("NONCONVERGENCE", "initial calibration", "plain KNN was not run",
                       "13/25", "13/5", "not independent dealer replications",
                       "transition-conditional", "no original ACI guarantee"):
            self.assertTrue(phrase.lower() in text.lower(), phrase)
        candidates = self.api.generated("wp5-candidates")["rows"]
        self.assertEqual(sum("NONCONVERGENCE" in row[2] for row in candidates), 1)
        self.assertEqual(sum(row[2].startswith("Not run") for row in candidates), 3)
        murphy = self.api.generated("wp3-murphy")["rows"]
        self.assertEqual(sum(row[2] == "CROSSING" for row in murphy), 8)

    def test_every_fixed_key_regenerates_exactly_with_current_sha_bindings(self):
        section = self.api.additional_section()
        all_blocks = section["blocks"] + self.api.additional_figures()
        keys = [block["_generator"] for block in all_blocks]
        self.assertEqual(len(keys), len(set(keys)))
        for block in all_blocks:
            self.assertEqual(block, self.api.generated(block["_generator"][7:]))
            self.assertTrue(block["_bindings"])
            for binding in block["_bindings"]:
                path = self.api.ROOT / binding["path"]
                self.assertEqual(binding["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertFalse(Path(binding["path"]).is_absolute())
                self.assertNotIn(".scratch", binding["path"])
        with self.assertRaises(KeyError): self.api.generated("unrecognized-context")

    def test_contextual_number_swap_is_rejected_by_regenerated_field_equality(self):
        original = self.api.generated("wp2-methods")
        mutated = deepcopy(original)
        self.assertNotEqual(mutated["rows"][0][3], mutated["rows"][1][3])
        # A valid number from a different real context must not validate here.
        mutated["rows"][0][3] = mutated["rows"][1][3]
        self.assertNotEqual(mutated, self.api.generated("wp2-methods"))
        self.assertEqual(original, self.api.generated("wp2-methods"))

    def test_only_relative_new_figure_assets_are_declared_without_inserting_indices(self):
        figures = self.api.additional_figures()
        self.assertEqual([f["path"] for f in figures],
                         ["figures/wp3-murphy-fx_hourly.pdf", "figures/wp3-murphy-nyfed_weekly.pdf"])
        self.assertTrue(all("matched" in f["caption"].lower() for f in figures))
        self.assertFalse(any(b.get("type") == "figure" for b in self.api.additional_section()["blocks"]))

    def test_method_and_reference_distribution_attributions_are_explicit(self):
        text = " ".join(b.get("html", "") for b in self.api.additional_section()["blocks"])
        for citation in ("Gibbs and Candès (2021)", "Engle and Manganelli (2004)",
                         "Diebold and Mariano (1995)", "Newey and West (1987)",
                         "Harvey, Leybourne and Newbold (1997)", "Holm (1979)",
                         "Kupiec (1995)", "Christoffersen (1998)",
                         "Ehm et al. (2016)", "Giacomini and White (2006)"):
            self.assertTrue(citation in text, citation)

    def test_wp3_coverage_failures_and_fractional_loss_changes_remain_visible(self):
        coverage = self.api.generated("wp3-coverage")["rows"]
        methods, controls = coverage[:112], coverage[112:]
        for rows, absent, boundary in ((methods, 5, 27), (controls, 12, 49)):
            self.assertEqual(sum("absent transition row" in row[6] for row in rows), absent)
            self.assertEqual(sum("Boundary reference" in row[6] for row in rows), boundary)
        relative = self.api.generated("wp3-relative")["rows"]
        self.assertEqual(sum(row[3] == row[4] == "NA" for row in relative), 48)
        directions = self.api.generated("wp5-directions")["rows"]
        self.assertEqual(sum(row[5].startswith("-") for row in directions), 2)
        self.assertEqual(sum(row[5] != "NA" and not row[5].startswith("-") for row in directions), 1)
        self.assertEqual(sum(row[5] == "NA" for row in directions), 3)
        murphy = self.api.generated("wp3-murphy")["rows"]
        self.assertTrue(all("residual=" in row[7] for row in murphy))

    def test_method_math_is_scaled_indexed_and_bound_to_standard_latex(self):
        wp2=self.api.generated("wp2-definition")
        wp4=self.api.generated("wp4-definition")
        wp5=self.api.generated("wp5-definition")
        formulas = {
            "wp2-definition": {
                "s<sub>i</sub>=P<sub>i,H</sub>−C<sub>i</sub><super>base</super>":
                    r"s_i=P_{i,H}-C_i^{\rm base}",
                "g<sub>i</sub>=G<sub>i,H</sub>/a<sub>κ</sub>":
                    r"g_i=G_{i,H}/a_\kappa",
                "q̃<sub>i</sub>=β<sub>0</sub>+β<sub>1</sub>q̃<sub>i−1</sub>+β<sub>2</sub>g<sub>i−H</sub>":
                    r"\widetilde q_i=\beta_0+\beta_1\widetilde q_{i-1}+\beta_2 g_{i-H}",
                "C<sub>t</sub>=B<sub>t</sub>+a<sub>κ</sub>max(0,q̃<sub>t</sub>)":
                    r"C_t=B_t+a_\kappa\max(0,\widetilde q_t)",
            },
            "wp4-definition": {
                "ψ<sub>t,g</sub>=1{S<sub>t</sub>=g}(d<sub>t</sub>−μ<sub>g</sub>)/p<sub>g</sub>":
                    r"\psi_{t,g}=\mathbf1\{S_t=g\}(d_t-\mu_g)/p_g",
                "Z<sub>t</sub>=[1,d<sub>t−H</sub>/a<sub>0</sub>,RMS<sub>t</sub>/v<sub>0</sub>]<super>T</super>":
                    r"Z_t=[1,d_{t-H}/a_0,\operatorname{RMS}_t/v_0]^{\mathsf T}",
            },
            "wp5-definition": {
                "k=⌈(W+1)τ⌉":r"k=\lceil(W+1)\tau\rceil",
                "W(1−τ)≥5":r"W(1-\tau)\ge5",
            },
        }
        for key,pairs in formulas.items():
            block=self.api.generated(key)
            bindings={x['html']:x['latex'] for x in block.get('inline_math',[])}
            for html,latex in pairs.items():
                self.assertTrue(html in block['html'],html)
                self.assertEqual(bindings.get(html),latex)
        self.assertTrue('known at refit κ' in wp2['html'])
        self.assertNotIn('earlier prefix peak',wp2['html'])
        for block in (wp2,wp4,wp5):
            visible=re.sub(r'<[^>]*>','',block['html'])
            self.assertIsNone(re.search(r'beta[012]|q_\(|d_\(|RMS_t|ceil\(|>=|tau=',visible))
        from v4_typeset import math_prepare
        prepared,bindings=math_prepare({'sections':[{'blocks':[wp2,wp4,wp5]}]})
        for pairs in formulas.values():
            for latex in pairs.values():self.assertIn(latex,bindings.values())
        self.assertTrue(all('VTHM' in b['html'] for b in prepared['sections'][0]['blocks']))


if __name__ == "__main__": unittest.main(verbosity=2)
