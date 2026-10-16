# Changelog

Все заметные изменения содержания фиксируются здесь. Автоматически сгенерированный inbox сам по себе не считается изменением позиции базы.

## 2026-10-16

- Исправлено ограниченное discovery: полная пагинация arXiv по дате обновления и GitHub releases, явное начало периода, отсутствие скрытого лимита, отчёт покрытия и ошибка при неполном обходе.
- Дедупликация учитывает старые плоские inbox и versioned papers; повторное обновление сохраняет разборы текущего inbox.
- Восстановлена очередь за 16 сентября — 16 октября и подготовлен [маршрут чтения](inbox/2026-W42/reading-guide.md) по памяти, compaction, мультимодальному RAG и качеству оценки. Выводы не перенесены в adoption radar автоматически.
- Добавлен последовательный разбор явной selection с сохранением каждого результата; улучшены диагностика цитат и проверка чисел в конце предложения. Все AI-разборы требуют отдельного human approval.

## 2026-08-19

- Inbox переведён на папки ISO-недель: `index.md`, `manifest.json`, `closeout.json`; повторный discovery сохраняет ручные marker-решения.
- Добавлены canonical modern/legacy arXiv IDs и жёсткое version pinning: разные `/abs`, `/pdf`, `/html`, `/src` формы сходятся к одной версии, а `v2` не перезаписывает `v1`.
- Реализована загрузка именно статей: HTML + PDF, TeX для review или fallback; raw artifacts кэшируются локально в `.aidb/` с URL/MIME/size/SHA-256 provenance.
- Добавлены semantic HTML extraction, безопасный static TeX parser без компиляции и optional `pdftotext` fallback; abstract/error pages не проходят full-text quality gate.
- Добавлен evidence-first deep summary через изолированный `codex exec` или OpenAI Responses API: строгая JSON Schema, exact-quote/block-ID validation, numeric grounding и deterministic Markdown render.
- Добавлены команды полного ритуала: `week-start`, `week-status`, `week-process`, `review`, `paper-approve`, `week-close`, а также низкоуровневые `paper fetch/extract/summarize/process/status`.
- AI summaries имеют статус `ai-draft` до явного human approval; partial failure не ставит `[x]` и остаётся resumable.

## 2026-08-04

- Добавлен `make triage`: безопасная обработка `drop/watch/note/review`, dry-run и scaffolds для source notes и adoption reviews.
- Triage-исход указывается коротким маркером в checkbox: `[d]` (drop), `[w]` (watch), `[n]` (note), `[r]` (review); ошибочная разметка останавливает обработку с явной ошибкой.
- Checkbox — единственный ручной ввод: поле `Triage` добавляется автоматически после обработки, а в необработанной записи отвергается.
- Каждый inbox содержит краткую легенду допустимых checkbox-маркеров.

## 2026-08-01

- Создана исходная taxonomy по мотивам *AI Engineering* Chip Huyen.
- RAG и агенты выделены в самостоятельные расширенные разделы.
- Добавлены source registry, adoption radar и процесс weekly discovery / monthly synthesis.
- Добавлен seed snapshot: MCP specification 2026-07-28, A2A 1.0, ADK 2.0, текущие agent/RAG материалы и benchmarks.
- Добавлены локальные проверки и scheduled discovery workflow для будущего GitHub-репозитория.
- Добавлен LangGraph adoption snapshot: OSS-метрики, production cases, роль в agentic RAG и статус `Trial`.
