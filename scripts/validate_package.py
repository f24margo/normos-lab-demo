import json
import sys
from pathlib import Path

def validate_msu_ua():
    pkg_path = Path("packages/msu_ua")
    manifest_file = pkg_path / "package.json"
    cards_dir = pkg_path / "cards"

    if not manifest_file.exists():
        print("❌ package.json не найден")
        sys.exit(1)

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    print(f"📦 Проверка пакета: {manifest.get('package_id')} v{manifest.get('version')}")

    card_files = list(cards_dir.glob("*.json"))
    card_ids = set()
    cards = []

    for card_file in card_files:
        with open(card_file, "r", encoding="utf-8") as f:
            card = json.load(f)
            cards.append(card)
            cid = card.get("id")
            if cid in card_ids:
                print(f"❌ Дубликат ID: {cid}")
                sys.exit(1)
            card_ids.add(cid)

    # Проверка зависимостей
    for card in cards:
        deps = card.get("depends_on", [])
        for dep in deps:
            if dep not in card_ids:
                print(f"❌ Несуществующая зависимость {dep} в карточке {card.get('id')}")
                sys.exit(1)

    print(f"✅ Успешно проверено карточек: {len(cards)}")

if __name__ == "__main__":
    validate_msu_ua()
