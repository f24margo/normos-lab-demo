import unittest
from core.norm_matcher import NormMatcher

class TestMsuUaPackage(unittest.TestCase):
    def setUp(self):
        self.matcher = NormMatcher("packages/msu_ua")

    def test_norm_matcher_exact_match(self):
        cards, warnings = self.matcher.match("вирішувати", "органі місцевого самоврядування")
        self.assertTrue(any(c["id"] in ["N01", "N06"] for c in cards))

    def test_norm_matcher_agent_mismatch_warning(self):
        cards, warnings = self.matcher.match("розпоряджатися", "обласна військова адміністрація")
        self.assertTrue(len(cards) > 0)
        self.assertGreaterEqual(len(warnings), 1)

    def test_n05_card_matching(self):
        cards, warnings = self.matcher.match("управляти", "органі місцевого самоврядування")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N05", matched_ids)

if __name__ == "__main__":
    unittest.main()
