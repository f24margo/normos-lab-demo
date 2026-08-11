# ROADMAP — NormOS Lab (draft)

**Оновлено:** 2026-07-27

## Поточний фокус
Demo v0.2 — Registry + пояснюваний вивід (не вітрина на хардкоді).

---

## v0.2.0 / v0.2.1 (зроблено)

- [x] NKS-011 Verb Registry Specification
- [x] data/norm_verbs_uk.json — **52** записи (lemma + forms + modality + category)
- [x] core/verb_registry.py — завантажувач і матчер
- [x] TraceStep + step_type (init / verb_match / coverage / computation / oov)
- [x] deciding_verb ≠ verbs_found
- [x] OOV-лог → data/oov_log.jsonl
- [x] app_v2_registry.py — badges (покриття) + граф ланцюга виводу
- [x] Тест на РЕГЛАМЕНТ.txt: deciding=забороняти (PROH), found=**41/52**

Публічний GitHub normos-lab **не змінювався**.  
Окрема гілка: research/engineering-intent (інженерні експерименти).

---

## Далі (коли продовжимо)

- [ ] Coverage у UI: «N з M»
- [ ] Реєстр → 80–100 записів
- [ ] Golden Tests на новому registry
- [ ] Короткий запис метрик coverage/OOV для протоколу фальсифікації

---

## Горизонт 3–4 тижні (Demo)

Стабільне демо для показу: документ → глаголи + один вирішальний вердикт + Trace.

## Горизонт 24 міс. (грант)

Див. docs/Grant_Concept_NormOS_Agents.md
