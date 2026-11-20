# Inside the Codex sandbox

- [Первоисточник — OpenAI](https://openai.com/index/inside-the-codex-sandbox/), 18 ноября 2026.
- Прочитан текст через веб-ридер: прямая загрузка вернула HTTP 403. Статус: `ai-draft`; аудит реализации не проводился.

## Original-language synopsis

Codex translates permission profiles into operating-system restrictions and a network proxy. Filesystem protection, process inheritance, domain authorization and platform-specific isolation jointly determine the effective boundary.

## Мой вывод

Стоит читать рядом с работой о потере происхождения инструкций при compaction. Типизированная история защищает смысл полномочий, а ограничения исполнения — доступные действия; одно не заменяет другое.

Особенно полезны честно описанные границы: широкое чтение файлов по умолчанию, возможность последующего исполнения изменённой зависимости вне изоляции, отдельный режим запуска MCP-серверов. Доменное правило работает лишь при реально включённом прокси; расширение шаблонов запрещённых путей на Linux и Windows фиксируется перед запуском, а не непрерывно.

Это архитектурное объяснение производителя, не доказательство отсутствия обходов. Для собственного harness нужно проверять эффективные права всего дерева процессов и подключённых сервисов на конкретной ОС. Настройки нашего рабочего окружения по этой статье не менялись.

## Опора в тексте

Разделы Choosing the sandbox boundaries, Example: sandboxing an MCP server, Network proxy и платформенные реализации. Способ доступа отмечен в [реестре чтения](../../inbox/2026-W47/web-reading.json).
