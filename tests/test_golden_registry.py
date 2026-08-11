"""Golden Tests — NormOS v0.2 Registry + Inference"""
from core.inference import InferenceEngine

engine = InferenceEngine()

CASES = [
    {
        "id": "G001",
        "query": "Голова зобов'язаний підписати рішення",
        "expect_modality": "OBL",
        "expect_verb": "підписати",
        "expect_oov": False,
    },
    {
        "id": "G002",
        "query": "Рада може делегувати повноваження",
        "expect_modality": "PERM",  # контекст «може» або POW від делегувати
        "expect_verb": "делегувати",
        "expect_oov": False,
        "allow_modalities": ["PERM", "POW"],
    },
    {
        "id": "G003",
        "query": "Забороняється проводити збори без кворуму",
        "expect_modality": "PROH",
        "expect_verb": "забороняти",
        "expect_oov": False,
    },
    {
        "id": "G004",
        "query": "Секретар повинен розглянути проект",
        "expect_modality": "OBL",
        "expect_verb": "розглянути",
        "expect_oov": False,
    },
    {
        "id": "G005",
        "query": "Рада ухвалює рішення більшістю голосів",
        "expect_modality": "POW",
        "expect_verb": "ухвалювати",
        "expect_oov": False,
    },
    {
        "id": "G006",
        "query": "невідомий текст без нормативного глагола xyz",
        "expect_modality": None,
        "expect_verb": None,
        "expect_oov": True,
    },
    {
        "id": "G007",
        "query": "Голова скликає сесію ради",
        "expect_modality": "POW",
        "expect_verb": "скликати",
        "expect_oov": False,
    },
    {
        "id": "G008",
        "query": "Депутат вносить проект рішення",
        "expect_modality": "PERM",
        "expect_verb": "вносити",
        "expect_oov": False,
    },
]

def run():
    passed = 0
    print("=== GOLDEN TESTS Registry v0.2 ===\n")
    for c in CASES:
        r = engine.infer(c["query"])
        ok = True
        reasons = []

        if c["expect_oov"]:
            if not r.get("oov"):
                ok = False
                reasons.append(f"oov expected True, got {r.get('oov')}")
        else:
            if r.get("oov"):
                ok = False
                reasons.append("unexpected OOV")
            verb = r.get("deciding_verb") or r.get("verb")
            if c["expect_verb"] and verb != c["expect_verb"]:
                # допуск: інший lemma з forms
                if c["expect_verb"] not in (verb or ""):
                    ok = False
                    reasons.append(f"verb {verb} != {c['expect_verb']}")
            mod = r.get("modality")
            allowed = c.get("allow_modalities") or ([c["expect_modality"]] if c["expect_modality"] else [])
            if allowed and mod not in allowed:
                ok = False
                reasons.append(f"modality {mod} not in {allowed}")

        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"{c['id']} {status}: {c['query'][:50]}")
        print(f"     → result={r.get('result')} verb={r.get('deciding_verb')} mod={r.get('modality')} oov={r.get('oov')}")
        if reasons:
            print(f"     !! {reasons}")
        print()

    total = len(CASES)
    print(f"=== {passed}/{total} passed ({100*passed/total:.0f}%) ===")
    return passed == total

if __name__ == "__main__":
    import sys
    sys.exit(0 if run() else 1)
