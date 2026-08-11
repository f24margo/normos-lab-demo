# NKS-013: Norm Card Schema & Matching Protocol

## 1. Schema Definition

Усі нормативні картки в пакетах (наприклад, `msu_ua`) повинні відповідати наступній схемі JSON:

```json
{
  "id": "string",               // Унікальний ідентифікатор (наприклад, N01)
  "title": "string",            // Коротка назва правила
  "source": {
    "act_id": "string",         // ID акта з package.json
    "article": "string",        // Номер статті
    "paragraph": "string",      // Номер пункту/частини
    "text_quote": "string"      // Цитата з норми
  },
  "source_confidence": "verified | approximate",
  "verbs": ["string"],          // Лемми дієслів з реєстру NKS-011
  "agents": ["string"],         // Порожній = будь-який суб'єкт; непорожній = обов'язковий збіг
  "condition_hint": "string",   // Підказка щодо контексту застосування
  "risk_if_missing": "string",  // Опис ризику
  "depends_on": ["string"],     // Масив ID карток, від яких залежить ця картка
  "status": "draft | active"    // Статус видимості
}
