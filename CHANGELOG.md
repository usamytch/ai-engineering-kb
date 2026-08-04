# Changelog

Все заметные изменения содержания фиксируются здесь. Автоматически сгенерированный inbox сам по себе не считается изменением позиции базы.

## 2026-08-04

- Добавлен `make triage`: безопасная обработка `drop/watch/note/review`, dry-run и scaffolds для source notes и adoption reviews.
- Triage-исход теперь можно указывать прямо в checkbox (`[drop]`, `[watch]`, `[note]`, `[review]`); конфликтующая или ошибочная разметка останавливает обработку с явной ошибкой.
- Новые inbox используют checkbox как единственный ручной ввод; поле `Triage` добавляется автоматически только после обработки.

## 2026-08-01

- Создана исходная taxonomy по мотивам *AI Engineering* Chip Huyen.
- RAG и агенты выделены в самостоятельные расширенные разделы.
- Добавлены source registry, adoption radar и процесс weekly discovery / monthly synthesis.
- Добавлен seed snapshot: MCP specification 2026-07-28, A2A 1.0, ADK 2.0, текущие agent/RAG материалы и benchmarks.
- Добавлены локальные проверки и scheduled discovery workflow для будущего GitHub-репозитория.
- Добавлен LangGraph adoption snapshot: OSS-метрики, production cases, роль в agentic RAG и статус `Trial`.
