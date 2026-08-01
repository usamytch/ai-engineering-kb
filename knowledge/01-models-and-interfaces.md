# 01. Модели и интерфейсы

**Обновлено:** 2026-08-01

## Позиция

Не поддерживать вручную «лучшую модель месяца». Быстро меняющиеся названия, цены и лимиты должны жить в официальных каталогах, а в базе — критерии выбора, snapshots собственных evals и migration notes.

Официальные trackers:

- [OpenAI models](https://developers.openai.com/api/docs/models) и [changelog](https://developers.openai.com/api/docs/changelog);
- [Claude models](https://platform.claude.com/docs/en/about-claude/models/overview) и [release notes](https://platform.claude.com/docs/en/release-notes/overview);
- [Gemini models](https://ai.google.dev/gemini-api/docs/models), [release notes](https://ai.google.dev/gemini-api/docs/changelog) и [deprecations](https://ai.google.dev/gemini-api/docs/deprecations).

## Выбор модели — не один leaderboard

Сначала сформировать набор задач, затем сравнивать кандидатов по нескольким осям:

| Ось | Примеры измерений |
| --- | --- |
| Task quality | pass rate, correctness, rubric score, pairwise preference |
| Tool use | tool choice, argument validity, recovery, parallel calls |
| Grounding | faithfulness, citation correctness, abstention |
| Reliability | variance по повторам, schema violations, timeouts |
| Latency | TTFT, time-to-final, p50/p95 end-to-end |
| Cost | tokens, tool/API cost, retries, cache-adjusted cost per success |
| Operations | rate limits, regions, privacy, logging, version pinning, deprecation window |

Для agentic workloads считать **cost per successful task**, а не только цену миллиона tokens: более дорогая модель может сделать меньше неудачных turns, а дешёвая — уйти в длинный цикл.

## Interface-first design

Модель должна быть заменяемым компонентом за стабильным приложенческим интерфейсом:

- typed input/output schema;
- нормализованный tool-call format;
- явные timeout, retry и cancellation;
- provider-specific features изолированы адаптером;
- model ID и settings записываются в trace;
- stable model versions pin-ятся в production; `latest` используется только при осознанном canary/eval процессе;
- prompt caching, reasoning budget и parallel tool calls считаются частью конфигурации версии.

## Routing

Routing полезен, когда существуют устойчивые классы запросов: простой extraction, сложное reasoning, multimodal, long context, high-risk action. Начинать с правил; model-based router добавлять только с eval router accuracy и fallback.

Минимальный routing log:

```text
request_class, selected_model, reason, fallback,
quality_score, latency_ms, total_cost, success
```

## Open weights vs API

Решение зависит не только от benchmark:

- privacy и residency;
- predictable capacity и unit economics;
- возможность fine-tune/quantize;
- стоимость команды serving/observability;
- feature gap в tools, multimodality, context и safety;
- лицензия и model/data provenance.

Для build-vs-buy сохранять decision record и пересматривать его при существенном изменении workload, требований или цен.

## Checklist обновления модели

1. Заморозить старую версию и representative eval set.
2. Прогнать candidate минимум несколько раз на nondeterministic задачах.
3. Сравнить качество, safety, latency и cost per success.
4. Проверить tool schemas, structured outputs и context limits.
5. Canary rollout с отдельными traces и rollback threshold.
6. Зафиксировать snapshot в changelog/decision record.

