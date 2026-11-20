# The sleep framework

- [Первоисточник — Google Research](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning/), 27 октября 2026.
- Прочитан полный текст публикации; связанная научная работа отдельно не разобрана. Статус: `ai-draft`.

## Original-language synopsis

The framework alternates active processing with parameter consolidation and synthetic rehearsal. It activates preallocated expert capacity, distills short-term information into slower memory parameters, and trains on selected generated examples.

## Мой вывод

Это другой смысл «сна», чем у Anthropic: здесь меняются веса модели, там — внешние заметки и представления. Смешивать их в один рецепт памяти нельзя.

Интересна проверка на последовательном освоении языков, фактах и длинном контексте. Но заявленная работа с десятью миллионами токенов на BABILong не означает такое же качество на произвольной истории пользователя. Без анализа исходного протокола нельзя приравнять сохранение результатов на этих задачах к отсутствию забывания вообще.

Для AIDB это направление исследования, а не готовая замена retrieval. Перед экспериментом нужны доступ к весам, бюджет обучения и контроль сохранности прежних навыков; сравнивать следует полный цикл обучения и ответа с поиском по исходным данным.

## Опора в тексте

Блоки `b00013-d3bf7d5add`, `b00018-3ae33d7938`–`b00028-0070777787`, `b00036-3de6228e36`–`b00039-724db49011`; [реестр снимков](../../inbox/2026-W47/web-reading.json).
