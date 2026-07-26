import json
from pathlib import Path
from typing import Dict, Optional, List

class NormVerb:
    def __init__(self, data: Dict):
        self.verb_id = data.get("verb_id")
        self.base_form = data.get("base_form")
        self.modality = data.get("modality", "OBL")
        self.transition_type = data.get("transition_type", "state_change")
        self.pre_condition = data.get("pre_condition", [])
        self.post_state = data.get("post_state", "")
        self.consequences = data.get("consequences", [])
        self.frequency = data.get("frequency", 0)
        self.status = data.get("status", "draft")

class NormVerbRegistry:
    def __init__(self):
        self.verbs: Dict[str, NormVerb] = {}
        self.load_from_json()
    
    def load_from_json(self):
        """Завантажує реєстр з JSON"""
        path = Path("data/norm_verb_registry.json")
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for base_form, vdata in data.get("verbs", {}).items():
                    self.verbs[base_form] = NormVerb(vdata)
        else:
            print("⚠️ JSON-реєстр не знайдено. Використовуємо порожній.")
    
    def find(self, text: str) -> Optional[NormVerb]:
        """Пошук глагола"""
        text_lower = text.lower()
        for form, verb in self.verbs.items():
            if form in text_lower:
                return verb
        return None
    
    def get_all(self) -> List[NormVerb]:
        return list(self.verbs.values())
