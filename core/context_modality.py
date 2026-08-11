"""NKS-012: context modality resolution (Demo v0.1)"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

class ContextModalityResolver:
    def __init__(self, path: str = "data/context_markers_uk.json"):
        self.path = Path(path)
        self.priority: List[str] = ["PROH", "OBL", "PERM"]
        self.negation_tokens: List[str] = ["не", "без"]
        self.negation_window: int = 4
        self.markers: Dict[str, List[str]] = {}
        self.contrast: List[str] = ["а", "проте", "однак"]
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.priority = data.get("priority", self.priority)
        self.negation_tokens = data.get("negation_tokens", self.negation_tokens)
        self.negation_window = int(data.get("negation_window", 4))
        self.markers = data.get("markers", {})
        self.contrast = data.get("contrast_conjunctions", self.contrast)

    def resolve(self, text: str, registry_modality: Optional[str] = None) -> Dict[str, Any]:
        """
        Повертає:
          modality, modality_source, markers_found, notes
        """
        if not text or not text.strip():
            return {
                "modality": registry_modality,
                "modality_source": "registry" if registry_modality else None,
                "markers_found": [],
                "notes": [],
            }

        # Demo: працюємо з цілим коротким запитом як однією зоною;
        # для складених — грубе розбиття лише по contrast-сполучниках
        zones = self._split_zones(text.lower())
        # беремо зону з найбільшою «силою» маркера (консервативно по всьому тексту)
        all_hits: List[Tuple[str, str, bool]] = []  # modality, marker, negated

        for zone in zones:
            tokens = re.findall(r"\b\w+\b", zone)
            for mod, words in self.markers.items():
                for w in sorted(words, key=len, reverse=True):
                    if w.lower() in zone:
                        negated = self._is_negated(tokens, w.lower())
                        all_hits.append((mod, w, negated))

        notes: List[str] = []
        if not all_hits:
            return {
                "modality": registry_modality,
                "modality_source": "registry" if registry_modality else None,
                "markers_found": [],
                "notes": notes,
            }

        # заперечення
        neg = [h for h in all_hits if h[2]]
        pos = [h for h in all_hits if not h[2]]

        if neg and not pos:
            return {
                "modality": None,
                "modality_source": "negation_scope",
                "markers_found": [{"modality": m, "marker": w, "negated": True} for m, w, _ in neg],
                "notes": ["Маркер під запереченням — потрібна перевірка людиною"],
            }

        if not pos:
            return {
                "modality": registry_modality,
                "modality_source": "registry" if registry_modality else None,
                "markers_found": [{"modality": m, "marker": w, "negated": True} for m, w, _ in neg],
                "notes": notes,
            }

        mods = {m for m, _, _ in pos}
        if len(mods) > 1:
            chosen = self._pick_priority(mods)
            notes.append("Кілька маркерів одночасно → консервативний вердикт")
            return {
                "modality": chosen,
                "modality_source": "conflict_default",
                "markers_found": [{"modality": m, "marker": w, "negated": False} for m, w, _ in pos],
                "notes": notes,
            }

        only = next(iter(mods))
        return {
            "modality": only,
            "modality_source": "context",
            "markers_found": [{"modality": m, "marker": w, "negated": False} for m, w, _ in pos],
            "notes": notes,
        }

    def _split_zones(self, text: str) -> List[str]:
        # розбиття лише по contrast (а|проте|однак), не по кожній комі
        parts = re.split(r"\b(?:а|проте|однак)\b", text)
        return [p.strip() for p in parts if p.strip()] or [text]

    def _is_negated(self, tokens: List[str], marker: str) -> bool:
        # маркер може бути кілька слів — шукаємо позицію першого слова
        m_toks = marker.split()
        if not m_toks:
            return False
        first = m_toks[0]
        for i, tok in enumerate(tokens):
            if tok != first:
                continue
            # вікно 1..negation_window токенів ліворуч
            left = tokens[max(0, i - self.negation_window) : i]
            if any(n in left for n in self.negation_tokens):
                return True
        return False

    def _pick_priority(self, mods: set) -> str:
        for p in self.priority:
            if p in mods:
                return p
        return next(iter(mods))
