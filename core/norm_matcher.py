import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

class NormMatcher:
    def __init__(self, package_path: str = "packages/msu_ua"):
        self.cards_dir = Path(package_path) / "cards"
        self.cards = self._load_cards()

    def _load_cards(self) -> List[Dict[str, Any]]:
        cards = []
        if not self.cards_dir.exists():
            return cards
        for card_file in sorted(self.cards_dir.glob("*.json")):
            with open(card_file, "r", encoding="utf-8") as f:
                cards.append(json.load(f))
        return cards

    def match(self, verb: str, agent: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        matched = []
        warnings = []

        for card in self.cards:
            card_verbs = card.get("verbs", [])
            card_agents = card.get("agents", [])

            if verb in card_verbs:
                if not card_agents or agent in card_agents:
                    matched.append((card, True))
                else:
                    matched.append((card, False))
                    warnings.append(
                        f"⚠️ Дію '{verb}' виконано суб’єктом '{agent}', що не відповідає правилу {card['id']}"
                    )

        # Приоритет совпадения по агенту
        matched.sort(key=lambda x: (not x[1], x[0]['id']))
        final_cards = [c[0] for c in matched[:2]] # Лимит 2 карточки

        return final_cards, warnings
