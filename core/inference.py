from .registry import NormVerbRegistry
from .parser import parse_normative_verb
from datetime import datetime
import uuid
import re
from typing import Dict, Any, List

registry = NormVerbRegistry()

class InferenceEngine:
    def infer(self, query: str, fact: Dict[str, Any] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        trace = ["Ініціалізація Тетради виводу."]
        
        # Якщо текст довгий — шукаємо кілька глаголів
        if len(query) > 300:
            return self._infer_document(query, trace)
        
        # Звичайний режим (короткий запит)
        parsed = parse_normative_verb(query)
        
        if not parsed:
            trace.append("❌ Нормативний глагол не знайдено в реестрі.")
            suggested = self._suggest_verbs(query)
            if suggested:
                trace.append("🔍 Рекомендації для самообучення:")
                for s in suggested[:5]:
                    trace.append(f"   - Додати/виправити: {s}")
            return {"result": "Не визначено", "trace": trace, "suggested_verbs": suggested}
        
        modality = parsed["modality"]
        trace.append(f"✅ Знайдено глагол: {parsed['base_form']} (модальність: {modality})")
        
        result = self._modality_to_result(modality)
        trace.append("Обчислення нормативного переходу завершено.")
        
        return {
            "id": str(uuid.uuid4()),
            "result": result,
            "verb": parsed["base_form"],
            "modality": modality,
            "trace": trace,
            "timestamp": datetime.now().isoformat()
        }
    
    def _infer_document(self, text: str, trace: List[str]) -> Dict[str, Any]:
        """Аналіз великого документа — шукаємо всі нормативні глаголи"""
        found = []
        text_lower = text.lower()
        
        for form, verb in registry.verbs.items():
            if form in text_lower or any(form[:6] in w for w in re.findall(r'\b\w+\b', text_lower) if len(w) > 5):
                found.append({
                    "base_form": verb.base_form,
                    "modality": verb.modality
                })
        
        # Унікальні
        unique = {v["base_form"]: v for v in found}
        found = list(unique.values())
        
        if not found:
            trace.append("❌ У документі не знайдено нормативних глаголів з реєстру.")
            return {"result": "Не визначено", "trace": trace, "verbs_found": []}
        
        trace.append(f"✅ Знайдено {len(found)} нормативних глаголів:")
        for v in found[:12]:
            trace.append(f"   - {v['base_form']} ({v['modality']})")
        
        # Загальний вердикт
        modalities = [v["modality"] for v in found]
        if "PROH" in modalities:
            result = "Документ містить заборони (PROH)"
        elif "POW" in modalities:
            result = "Документ містить повноваження (POW)"
        elif "OBL" in modalities:
            result = "Документ містить обов'язки (OBL)"
        else:
            result = "Документ містить дозволи (PERM)"
        
        trace.append("Аналіз документа завершено.")
        
        return {
            "id": str(uuid.uuid4()),
            "result": result,
            "verb": ", ".join([v["base_form"] for v in found[:5]]),
            "modality": "MIXED",
            "trace": trace,
            "verbs_found": found,
            "timestamp": datetime.now().isoformat()
        }
    
    def _modality_to_result(self, modality: str) -> str:
        if modality == "POW":
            return "Дозволено (PERM) — Повноваження"
        if modality == "OBL":
            return "Обов'язково (OBL)"
        if modality == "PROH":
            return "Заборонено (PROH)"
        return "Дозволено (PERM)"
    
    def _suggest_verbs(self, text: str) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        suggestions = []
        for word in words:
            if len(word) > 5 and word.endswith(('ти', 'ати', 'яти', 'ити', 'нути', 'вати')):
                suggestions.append(word)
        return list(set(suggestions))[:10]
