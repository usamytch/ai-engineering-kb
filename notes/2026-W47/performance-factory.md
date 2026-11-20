# Performance Factory

- [Первоисточник — OpenAI](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast/), 19 ноября 2026.
- Прочитан текст через веб-ридер после HTTP 403 при прямой загрузке. Статус: `ai-draft`.

## Original-language synopsis

Persistent tasks move through investigation, challenged diagnosis, proposed fix, human review and post-deployment verification. Event subscriptions resume waiting work; separate evaluations assess investigations and engineer-facing reports.

## Мой вывод

Самая полезная часть — проверка восстановления после выкладки. Закрывать задачу по наличию убедительной гипотезы или принятого изменения недостаточно. Состояние задачи живёт вне контекста отдельного агента, поэтому ожидание ревью и смена исполнителя не теряют обязательство проверить результат.

Авторы честно сообщают, что из ста вручную проверенных предположений о причине только 70% признаны точными. Это не доля автоматически исправленных инцидентов. Более 1 700 расследований и 600 найденных причин тоже не дают такой метрики.

Для воспроизводимой оценки важна защита исторических тестов от подсказок: прошлые отчёты и память запрещены, доступные трассы ограничены, сведения после восстановления могут раскрывать ответ. Это практический образец построения контура диагностики; заявленный производственный опыт не является сравнением с контрольной группой.

## Опора в тексте

Разделы Adversarial review, Fixing the regression и Evaluating investigations; [реестр чтения](../../inbox/2026-W47/web-reading.json).
