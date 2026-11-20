# Building strong safety evaluations

- [Первоисточник — Anthropic](https://www.anthropic.com/research/building-strong-safety-evaluations), 13 ноября 2026.
- Прочитан полный текст. Статус: `ai-draft`; методические рекомендации производителя.

## Original-language synopsis

The article separates observational comparisons from causal interventions, and refusal rates from appropriate behavior. It recommends realistic multi-turn scenarios, calibrated graders, preregistered comparisons, paired uncertainty estimates and complete configuration reporting.

## Мой вывод

Стоит прочитать перед следующим сравнением систем памяти. Правильный ответ, обоснованный ответ и безопасное действие — разные измеряемые свойства. Для каждого нужен свой критерий и проверка судьи на человеческой разметке.

Практически полезны независимое варьирование факторов, фиксация протокола до результатов и явный учёт поломок оценщика. Средний балл легко скрывает деградацию отдельного сценария; насыщенный тест годится для контроля регрессий, но плохо различает новые модели.

Рекомендованные авторами минимальные размеры выборок нельзя превращать в универсальное правило: необходимый объём зависит от эффекта, зависимости примеров и разброса. И сравнение API с продуктом измеряет весь комплект настроек, а не отдельную строку системного промпта. Это методическая статья с внутренними примерами, не независимая проверка безопасности Claude.

## Опора в тексте

Разделы Design, Run и Report; локальные блоки `b00060-e7e68f90b6`, `b00062-b9ca513cf1`, `b00065-a254b1efa7`, `b00066-5748ccd0e5`, `b00073-c6b78fd380`. Снимок — в [реестре чтения](../../inbox/2026-W47/web-reading.json).
