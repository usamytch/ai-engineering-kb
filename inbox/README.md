# Inbox

Inbox содержит **кандидатов на разбор**, а не проверенные рекомендации.

- `YYYY-MM-DD.md` — результат `make inbox` или scheduled GitHub Action;
- после triage запись получает исход `drop`, `watch`, `note` или `review`;
- важный источник переносится в `SOURCES.md` и тематический файл;
- изменение инженерной позиции отдельно отражается в `ADOPTION.md` и `CHANGELOG.md`.

Для разметки заменить пустой checkbox `[ ]` на `[drop]`, `[watch]`, `[note]`
или `[review]`. Затем запустить:

```bash
make triage
```

По умолчанию обрабатывается последний датированный inbox. `drop` удаляется, `watch` помечается обработанным, `note` создаёт карточку в `notes/`, а `review` — adoption review в `reviews/`. Для сохранённых записей скрипт заменяет исход на `[x]` и сам добавляет поле `Triage` как историю решения. Неразмеченные и уже обработанные записи не меняются.

Полезные варианты:

```bash
make triage TRIAGE_ARGS=--dry-run
make triage TRIAGE_FILE=inbox/2026-08-04.md
make triage TRIAGE_ARGS=--all
```

Автогенерируемые файлы можно удалять после triage: Git history сохранит snapshot.
