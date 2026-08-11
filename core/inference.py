from .verb_registry import VerbRegistry
from .context_modality import ContextModalityResolver
from .entities import TraceStep
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List, Optional
import re
import json
from pathlib import Path

registry = VerbRegistry()
_modality_resolver = ContextModalityResolver()

class InferenceEngine:
    def infer(self, query: str, fact: Dict[str, Any] = None, context: Dict[str, Any] = None) -> Dict[str, Any]:
        trace: List[TraceStep] = [
            TraceStep(label="Ініціалізація Тетради виводу.", step_type="init")
        ]

        if not query or not query.strip():
            trace.append(TraceStep(label="Порожній запит.", step_type="oov"))
            return self._pack("Не визначено", None, None, trace, oov=True)

        if len(query) > 300:
            return self._infer_document(query, trace)

        verb = registry.find(query)
        if not verb:
            trace.append(TraceStep(label="❌ Нормативний глагол не знайдено (OOV).", step_type="oov"))
            self._log_oov(query)
            for s in self._suggest(query)[:5]:
                trace.append(TraceStep(label=f"Рекомендація: додати «{s}»", step_type="oov"))
            return self._pack("Не визначено", None, None, trace, oov=True)

        resolved = _modality_resolver.resolve(query, verb.modality)
        modality = resolved.get("modality")
        source = resolved.get("modality_source")
        notes = resolved.get("notes") or []

        trace.append(TraceStep(
            label=f"✅ Знайдено: {verb.lemma}",
            matched_verb=verb.id or verb.lemma,
            modality=modality or verb.modality,
            step_type="verb_match",
        ))

        # NKS-012: modality resolve step
        if source == "negation_scope":
            trace.append(TraceStep(
                label="⚠️ Маркер під запереченням — потрібна перевірка людиною",
                matched_verb=verb.id or verb.lemma,
                modality=None,
                step_type="modality_resolve",
            ))
            for n in notes:
                trace.append(TraceStep(label=n, step_type="modality_resolve"))
            trace.append(TraceStep(label="Автовердикт не застосовано (negation_scope).", step_type="computation"))
            return self._pack(
                "Потрібна перевірка людиною (заперечення в контексті)",
                verb.lemma,
                None,
                trace,
                modality_source=source,
                markers_found=resolved.get("markers_found"),
            )

        if modality is None:
            modality = verb.modality
            source = source or "registry"

        src_label = {
            "context": "модальность з контексту",
            "registry": "типова модальность з реєстру",
            "conflict_default": "консервативний вибір при конфлікті маркерів",
        }.get(source, source or "registry")

        trace.append(TraceStep(
            label=f"Модальність: {modality} ({src_label})",
            matched_verb=verb.id or verb.lemma,
            modality=modality,
            step_type="modality_resolve",
        ))
        for n in notes:
            trace.append(TraceStep(label=f"⚠️ {n}", modality=modality, step_type="modality_resolve"))

        result = self._modality_to_result(modality)
        trace.append(TraceStep(
            label="Обчислення нормативного переходу завершено.",
            modality=modality,
            step_type="computation",
        ))

        return self._pack(
            result,
            verb.lemma,
            modality,
            trace,
            modality_source=source,
            markers_found=resolved.get("markers_found"),
            verbs_found=[{"lemma": verb.lemma, "modality": modality}],
        )

    def _infer_document(self, text: str, trace: List[TraceStep]) -> Dict[str, Any]:
        found = registry.find_all(text)
        if not found:
            trace.append(TraceStep(label="❌ У документі не знайдено глаголів (OOV).", step_type="oov"))
            self._log_oov(text[:500])
            return self._pack("Не визначено", None, None, trace, oov=True)

        verbs_found = [{"lemma": v.lemma, "modality": v.modality} for v in found]
        priority = {"PROH": 0, "OBL": 1, "POW": 2, "PERM": 3, "IMM": 4}
        deciding = sorted(found, key=lambda v: priority.get(v.modality, 9))[0]

        # для документа: спочатку покриття реєстром; modality document-level з пріоритету lemma
        # плюс легкий context scan всього тексту (маркери заборони тощо)
        resolved = _modality_resolver.resolve(text[:2000], deciding.modality)
        doc_mod = deciding.modality
        source = "registry"
        if resolved.get("modality_source") == "context" and resolved.get("modality"):
            # якщо в тексті явний PROH-маркер — підсилюємо ярлик документа
            if resolved["modality"] == "PROH":
                doc_mod = "PROH"
                source = "context"
                deciding_lemma = deciding.lemma
            else:
                deciding_lemma = deciding.lemma
        else:
            deciding_lemma = deciding.lemma

        # якщо context дав PROH, deciding для ярлика може лишитись lemma з PROH у реєстрі
        if doc_mod == "PROH":
            proh_verbs = [v for v in found if v.modality == "PROH"]
            if proh_verbs:
                deciding_lemma = proh_verbs[0].lemma

        trace.append(TraceStep(
            label=f"✅ Знайдено: {deciding_lemma}",
            matched_verb=deciding_lemma,
            modality=doc_mod,
            step_type="verb_match",
        ))
        trace.append(TraceStep(
            label=f"Покриття реєстру: {len(found)} з {registry.count()}",
            step_type="coverage",
        ))
        trace.append(TraceStep(
            label=f"Модальність документа: {doc_mod} ({source})",
            modality=doc_mod,
            step_type="modality_resolve",
        ))

        if doc_mod == "PROH":
            result = "Заборонено (PROH)" if source == "context" else "Документ містить заборони (PROH)"
        elif doc_mod == "OBL":
            result = "Документ містить обов'язки (OBL)"
        elif doc_mod == "POW":
            result = "Документ містить повноваження (POW)"
        else:
            result = "Документ містить дозволи (PERM)"

        trace.append(TraceStep(label="Обчислення нормативного переходу завершено.", modality=doc_mod, step_type="computation"))
        return self._pack(
            result,
            deciding_lemma,
            doc_mod,
            trace,
            modality_source=source,
            verbs_found=verbs_found,
        )

    def _modality_to_result(self, modality: str) -> str:
        return {
            "POW": "Дозволено (PERM) — Повноваження",
            "OBL": "Обов'язково (OBL)",
            "PROH": "Заборонено (PROH)",
            "PERM": "Дозволено (PERM)",
        }.get(modality, "Дозволено (PERM)")

    def _pack(
        self,
        result,
        deciding_verb,
        modality,
        trace,
        oov=False,
        verbs_found=None,
        modality_source=None,
        markers_found=None,
    ):
        return {
            "id": str(uuid4()),
            "result": result,
            "verb": deciding_verb,
            "deciding_verb": deciding_verb,
            "modality": modality,
            "modality_source": modality_source,
            "markers_found": markers_found or [],
            "trace": [
                (s.model_dump() if hasattr(s, "model_dump") else s.dict())
                for s in trace
            ],
            "oov": oov,
            "verbs_found": verbs_found or [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _log_oov(self, text: str):
        path = Path("data/oov_log.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat(), "text": text[:1000]}, ensure_ascii=False) + "\n")

    def _suggest(self, text: str) -> List[str]:
        words = re.findall(r"\b\w+\b", text.lower())
        return list({w for w in words if len(w) > 5 and w.endswith(("ти", "ати", "яти", "ити", "вати"))})[:10]
