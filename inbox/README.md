# Inbox

Inbox содержит **кандидатов на разбор**, а не проверенные рекомендации.

- `YYYY-Www/index.md` — экран ручного triage одной ISO-недели;
- `YYYY-Www/manifest.json` — полный machine-readable discovery snapshot;
- `YYYY-Www/closeout.json` — итог `make week-close`;
- старые `YYYY-MM-DD.md` поддерживаются как legacy snapshots;
- после triage запись получает исход `drop`, `watch`, `note` или `review`;
- важный источник переносится в `SOURCES.md` и тематический файл;
- изменение инженерной позиции отдельно отражается в `ADOPTION.md` и `CHANGELOG.md`.

Для разметки заменить пустой checkbox `[ ]` на `[d]` (drop), `[w]` (watch),
`[n]` (note) или `[r]` (review). Затем запустить:

```bash
make week-process PROVIDER=codex
```

По умолчанию обрабатывается последняя неделя. `drop` теперь сохраняется для
аудита и deduplication, `watch` фиксируется без загрузки статьи, `note` запускает
full-text ingest и deep summary, `review` дополнительно создаёт adoption review.
Для успешных записей скрипт заменяет исход на `[x]` и сам добавляет `Triage`.
Неразмеченные и уже обработанные записи не меняются.

Полезные варианты:

```bash
make week-status WEEK=2026-W34
make week-process WEEK=2026-W34 AIDB_ARGS=--dry-run
make week-process WEEK=2026-W34 PROVIDER=openai MODEL=gpt-5.6
make week-close WEEK=2026-W34
```

Не удаляйте manifest после triage: он хранит решения, ошибки и основу
межнедельной дедупликации. Сами тексты статей в inbox не лежат.
