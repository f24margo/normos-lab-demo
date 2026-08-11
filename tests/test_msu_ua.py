import unittest
import json
from pathlib import Path
from scripts.match_cards import match_cards

class TestMsuUaPackage(unittest.TestCase):

    def test_package_structure(self):
        pkg_path = Path("packages/msu_ua")
        self.assertTrue((pkg_path / "package.json").exists(), "package.json відсутній")
        
        cards_dir = pkg_path / "cards"
        cards = list(cards_dir.glob("*.json"))
        self.assertGreaterEqual(len(cards), 4, "Очікується щонайменше 4 картки")

    def test_card_schema_fields(self):
        cards_dir = Path("packages/msu_ua/cards")
        required_fields = {"id", "title", "source", "verbs", "agents", "depends_on", "status"}
        
        for card_file in cards_dir.glob("*.json"):
            with open(card_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                missing = required_fields - set(data.keys())
                self.assertEqual(len(missing), 0, f"У картці {card_file.name} відсутні поля: {missing}")

    def test_matching_exact_agent(self):
        cards, warnings = match_cards("розпоряджатися", "органи місцевого самоврядування")
        self.assertGreater(len(cards), 0)
        self.assertEqual(cards[0]["id"], "N04")
        self.assertEqual(len(warnings), 0)

    def test_matching_agent_mismatch_warning(self):
        cards, warnings = match_cards("розпоряджатися", "обласна військова адміністрація")
        self.assertGreater(len(cards), 0)
        self.assertEqual(cards[0]["id"], "N04")
        self.assertEqual(len(warnings), 1)
        self.assertIn("іншим суб’єктом", warnings[0])

if __name__ == "__main__":
    unittest.main()
