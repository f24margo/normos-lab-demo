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


    def test_land_lease_matching(self):
        # Перевірка сопоставлення N20 (оренда землі)
        cards, warnings = self.matcher.match("передавати земельні ділянки в оренду", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N20", matched_ids)


    def test_land_privatization_matching(self):
        # Перевірка сопоставлення N21 (безоплатна приватизація землі)
        cards, warnings = self.matcher.match("передавати безоплатно у власність", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N21", matched_ids)


    def test_general_plan_matching(self):
        # Перевірка сопоставлення N22 (генеральний план)
        cards, warnings = self.matcher.match("затверджувати генеральний план", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N22", matched_ids)


    def test_dpt_matching(self):
        # Перевірка сопоставлення N23 (детальний план території)
        cards, warnings = self.matcher.match("затверджувати детальний план території", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N23", matched_ids)


    def test_mbuo_matching(self):
        # Перевірка сопоставлення N24 (містобудівні умови та обмеження)
        cards, warnings = self.matcher.match("надавати містобудівні умови та обмеження", "виконавчі органи сільських, селищних, міських рад")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N24", matched_ids)


    def test_communal_property_matching(self):
        # Перевірка сопоставлення N25 (комунальна власність)
        cards, warnings = self.matcher.match("засновувати комунальні підприємства", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N25", matched_ids)


    def test_small_privatization_matching(self):
        # Перевірка сопоставлення N26 (мала приватизація комунального майна)
        cards, warnings = self.matcher.match("затверджувати переліки об’єктів приватизації", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N26", matched_ids)


    def test_blagoustroy_matching(self):
        # Перевірка сопоставлення N27 (правила благоустрою)
        cards, warnings = self.matcher.match("затверджувати правила благоустрою", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N27", matched_ids)


    def test_jhk_tariffs_matching(self):
        # Перевірка сопоставлення N28 (тарифи на комунальні послуги)
        cards, warnings = self.matcher.match("встановлювати тарифи на комунальні послуги", "виконавчі органи сільських, селищних, міських рад")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N28", matched_ids)


    def test_cnap_matching(self):
        # Перевірка сопоставлення N29 (утворення ЦНАП)
        cards, warnings = self.matcher.match("утворювати центр надання адміністративних послуг", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N29", matched_ids)


    def test_social_protection_matching(self):
        # Перевірка сопоставлення N30 (соціальний захист)
        cards, warnings = self.matcher.match("забезпечувати надання соціальних послуг", "виконавчі органи сільських, селищних, міських рад")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N30", matched_ids)


    def test_civil_protection_matching(self):
        # Перевірка сопоставлення N31 (цивільний захист)
        cards, warnings = self.matcher.match("забезпечувати цивільний захист", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N31", matched_ids)


    def test_public_order_matching(self):
        # Перевірка сопоставлення N32 (забезпечення громадського порядку)
        cards, warnings = self.matcher.match("забезпечувати громадський порядок", "виконавчі органи сільських, селищних, міських рад")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N32", matched_ids)


    def test_regulatory_plan_matching(self):
        # Перевірка сопоставлення N33 (планування регуляторної діяльності)
        cards, warnings = self.matcher.match("затверджувати план діяльності з підготовки проектів регуляторних актів", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N33", matched_ids)


    def test_education_matching(self):
        # Перевірка сопоставлення N34 (заклади освіти)
        cards, warnings = self.matcher.match("засновувати заклади освіти", "сільські, селищні, міські ради")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N34", matched_ids)


    def test_culture_and_sports_matching(self):
        # Перевірка сопоставлення N35 (культура та спорт)
        cards, warnings = self.matcher.match("управляти закладами культури", "виконавчі органи сільських, селищних, міських рад")
        matched_ids = [c["id"] for c in cards]
        self.assertIn("N35", matched_ids)

if __name__ == "__main__":
    unittest.main()
