# Inbox

Inbox содержит **кандидатов на разбор**, а не проверенные рекомендации.

- `YYYY-MM-DD.md` — результат `make inbox` или scheduled GitHub Action;
- после triage запись получает исход `drop`, `watch`, `note` или `review`;
- важный источник переносится в `SOURCES.md` и тематический файл;
- изменение инженерной позиции отдельно отражается в `ADOPTION.md` и `CHANGELOG.md`.

Автогенерируемые файлы можно удалять после triage: Git history сохранит snapshot.

