import json
from pathlib import Path
from typing import Optional, Dict, Any, List

class VerbRecord:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.lemma = data.get("lemma")
        self.forms = data.get("forms", [])
        self.modality = data.get("modality", "OBL")
        self.category = data.get("category", "")
        self.typical_agents = data.get("typical_agents", [])
        self.status = data.get("status", "draft")

class VerbRegistry:
    def __init__(self, path: str = "data/norm_verbs_uk.json"):
        self.path = Path(path)
        self.verbs: List[VerbRecord] = []
        self._load()

    def _load(self):
        if not self.path.exists():
            print(f"⚠️ Registry not found: {self.path}")
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.verbs = [VerbRecord(v) for v in data.get("verbs", [])]

    def find(self, text: str) -> Optional[VerbRecord]:
        """Пошук за lemma або будь-якою формою"""
        if not text:
            return None
        t = text.lower()
        # 1. точний lemma / form
        for v in self.verbs:
            if v.lemma and v.lemma in t:
                return v
            for f in v.forms:
                if f.lower() in t:
                    return v
        # 2. корінь (перші 6 літер lemma)
        for v in self.verbs:
            root = (v.lemma or "")[:6]
            if len(root) >= 5 and root in t:
                return v
        return None

    def find_all(self, text: str) -> List[VerbRecord]:
        """Усі збіги в тексті (для великих документів)"""
        if not text:
            return []
        t = text.lower()
        found = []
        seen = set()
        for v in self.verbs:
            hit = False
            if v.lemma and v.lemma in t:
                hit = True
            else:
                for f in v.forms:
                    if f.lower() in t:
                        hit = True
                        break
            if not hit:
                root = (v.lemma or "")[:6]
                if len(root) >= 5 and root in t:
                    hit = True
            if hit and v.lemma not in seen:
                found.append(v)
                seen.add(v.lemma)
        return found

    def count(self) -> int:
        return len(self.verbs)
