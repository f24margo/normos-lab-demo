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

    def test_budget_and_tax_matching(self):
        cards, warnings = self.matcher.match("затверджувати бюджет", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N12", matched_ids)


    def test_land_and_property_tax_matching(self):
        # Перевірка сопоставлення N15 та N16 (земельний податок та нерухомість)
        cards_tax, _ = self.matcher.match("встановлювати ставки", "сільські, селищні, міські ради")
        matched_tax_ids = [c["id"] for c in cards_tax]
        self.assertIn("N15", matched_tax_ids)
        self.assertIn("N16", matched_tax_ids)

        # Перевірка сопоставлення N17 (розпорядження землями)
        cards_land, _ = self.matcher.match("розпоряджатися землями", "територіальні громади")
        matched_land_ids = [c["id"] for c in cards_land]
        self.assertIn("N17", matched_land_ids)


    def test_tourist_tax_matching(self):
        # Перевірка сопоставлення N18 (туристичний збір)
        cards, warnings = self.matcher.match("встановлювати туристичний збір", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N18", matched_ids)


    def test_single_tax_matching(self):
        # Перевірка сопоставлення N19 (єдиний податок)
        cards, warnings = self.matcher.match("встановлювати ставки єдиного податку", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N19", matched_ids)

if __name__ == "__main__":
    unittest.main()
