from .registry import NormVerbRegistry
import re

registry = NormVerbRegistry()

def parse_normative_verb(text: str):
    """Парсер з покращеним пошуком по кореню"""
    if not text:
        return None
    
    text_lower = text.lower()
    
    # 1. Точний пошук
    for form, verb in registry.verbs.items():
        if form in text_lower:
            modality = _detect_modality(text_lower, verb.modality)
            return _make_result(verb, modality, 0.95)
    
    # 2. Пошук по кореню (6–7 літер)
    words = re.findall(r'\b\w+\b', text_lower)
    for word in words:
        if len(word) < 5:
            continue
        for form, verb in registry.verbs.items():
            root = form[:7] if len(form) >= 7 else form[:5]
            if root in word or word.startswith(root[:5]):
                modality = _detect_modality(text_lower, verb.modality)
                return _make_result(verb, modality, 0.8)
    
    # 3. Спеціальні патерни
    patterns = {
        r'затверд': 'затвердити',
        r'ухвал': 'ухвалювати',
        r'голосув': 'голосувати',
        r'підпис': 'підписати',
        r'прийм': 'приймати',
        r'скас': 'скасовувати',
        r'делег': 'делегувати',
        r'заборо': 'забороняти',
        r'забезпеч': 'забезпечити',
        r'признач': 'призначати',
        r'створ': 'створювати',
        r'провед': 'проводити',
        r'розгляд': 'розглянути',
        r'звітув': 'звітувати',
    }
    
    for pattern, form in patterns.items():
        if re.search(pattern, text_lower):
            verb = registry.verbs.get(form)
            if verb:
                modality = _detect_modality(text_lower, verb.modality)
                return _make_result(verb, modality, 0.85)
    
    return None

def _detect_modality(text: str, default: str) -> str:
    """Визначає модальність за контекстом"""
    if any(w in text for w in ["повинен", "зобов'язаний", "зобов'язана", "зобов'язано", "має обов"]):
        return "OBL"
    if any(w in text for w in ["може", "має право", "дозволяється"]):
        return "PERM"
    if any(w in text for w in ["забороняється", "заборонено", "не можна", "не дозволяється"]):
        return "PROH"
    return default

def _make_result(verb, modality, confidence):
    return {
        "verb_id": verb.verb_id,
        "base_form": verb.base_form,
        "modality": modality,
        "transition_type": verb.transition_type,
        "description": verb.post_state or verb.base_form,
        "confidence": confidence
    }
