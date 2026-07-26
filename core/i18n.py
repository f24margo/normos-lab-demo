from typing import Dict

class I18n:
    def __init__(self):
        self.translations = {
            "ru": {
                "app_title": "NormOS — Нормативный Двигун",
                "verdict": "Вердикт",
                "trace": "Трассировка",
                "agent": "Субъект",
                "vote_fact": "Факт голосования",
                "quorum": "Кворум",
                "run_button": "Запустить вывод",
                "history": "История запусков",
            },
            "uk": {
                "app_title": "NormOS — Нормативний Двигун",
                "verdict": "Вердикт",
                "trace": "Трасування",
                "agent": "Суб'єкт",
                "vote_fact": "Факт голосування",
                "quorum": "Кворум",
                "run_button": "Запустити вивід",
                "history": "Історія запусків",
            },
            "en": {
                "app_title": "NormOS — Normative Engine",
                "verdict": "Verdict",
                "trace": "Trace",
                "agent": "Agent",
                "vote_fact": "Voting Fact",
                "quorum": "Quorum",
                "run_button": "Run Inference",
                "history": "Run History",
            }
        }
        self.current_lang = "ru"
    
    def set_lang(self, lang: str):
        if lang in self.translations:
            self.current_lang = lang
            print(f"Язык изменён на: {lang.upper()}")
    
    def t(self, key: str) -> str:
        """Перевод строки"""
        return self.translations[self.current_lang].get(key, key)
