import json
from pathlib import Path

def match_cards(found_verb, agent_input):
    cards_dir = Path("packages/msu_ua/cards")
    matched = []
    warnings = []

    for card_file in sorted(cards_dir.glob("*.json")):
        with open(card_file, "r", encoding="utf-8") as f:
            card = json.load(f)

        card_verbs = card.get("verbs", [])
        card_agents = card.get("agents", [])

        if found_verb in card_verbs:
            if not card_agents or agent_input in card_agents:
                matched.append((card, True))
            else:
                matched.append((card, False))
                warnings.append(f"⚠️ Дію виконано іншим суб’єктом ('{agent_input}'), ніж у правилі {card['id']}")

    # Приоритет: совпадение по агенту > только по глаголу
    matched.sort(key=lambda x: (not x[1], x[0]['id']))

    # Лимит 2 карточки по NKS-013
    final_cards = [c[0] for c in matched[:2]]

    # Проверка порядка зависит от depends_on
    final_ids = {c['id'] for c in final_cards}
    for c in final_cards:
        deps = [d for d in c.get('depends_on', []) if d in final_ids]
        if deps:
            print(f"ℹ️ [UI Ordering]: Спочатку {', '.join(deps)}, потім {c['id']}")

    return final_cards, warnings

if __name__ == "__main__":
    print("--- Тест 1: Совпадение по глаголу и агенту ---")
    cards, msgs = match_cards("розпоряджатися", "органи місцевого самоврядування")
    print("Знайдені картки:", [c['id'] for c in cards])
    for m in msgs: print(m)

    print("\n--- Тест 2: Глагол совпал, субъект не тот ---")
    cards, msgs = match_cards("розпоряджатися", "обласна військова адміністрація")
    print("Знайдені картки:", [c['id'] for c in cards])
    for m in msgs: print(m)
