# Adoption radar

**Обновлено:** 2026-08-01

Статусы описывают рекомендуемый default для новых прикладных систем, а не универсальную истину. `Adopt` означает «хорошая исходная практика», но всё равно требует use-case eval.

## Статусы

- **Adopt** — использовать по умолчанию.
- **Trial** — пробовать в ограниченном production/пилоте с метриками.
- **Explore** — провести time-boxed эксперимент.
- **Watch** — следить, данных для эксперимента пока недостаточно.
- **Hold** — не добавлять без конкретного доказанного failure mode.

## Общая архитектура

| Подход | Статус | Позиция | Следующий review |
| --- | --- | --- | --- |
| Use-case eval до выбора модели | **Adopt** | Публичный benchmark — фильтр, не замена private eval. | 2026-11 |
| Structured outputs и schema validation | **Adopt** | Снижает неоднозначность интерфейса и упрощает точные проверки. | 2026-11 |
| Версионирование prompt/tool/schema/model | **Adopt** | Trace без версий плохо воспроизводим. | 2026-11 |
| Model routing | **Trial** | Полезен после появления устойчивых классов запросов и cost/quality eval. | 2026-10 |
| Finetuning до сильного prompt/RAG baseline | **Hold** | Сначала локализовать failure mode и собрать evaluation/data pipeline. | 2026-12 |

## RAG

| Подход | Статус | Позиция | Promotion gate |
| --- | --- | --- | --- |
| BM25 / lexical baseline | **Adopt** | Дешёвый baseline, особенно силён на ID, именах и терминах. | Всегда сравнивать более сложный retriever. |
| Hybrid sparse+dense retrieval | **Adopt** | Практичный default для разнородных enterprise corpora. | Улучшение Recall@K и answer quality при приемлемой latency. |
| Reranking | **Adopt** | Добавлять после broad retrieval; измерять latency и cost отдельно. | Выигрыш на representative queries. |
| Parent/child и context-preserving chunks | **Trial** | Борется с потерей контекста при chunking. | Меньше context misses без чрезмерного token budget. |
| Contextual Retrieval | **Trial** | Сильная идея для неоднозначных chunks; vendor report требует своей проверки. | Сравнение с hybrid+reranker baseline. |
| Query rewriting / HyDE | **Explore** | Полезно при vocabulary mismatch, но может увести retrieval. | Query-class eval и защита от topic drift. |
| RAPTOR / hierarchical retrieval | **Explore** | Кандидат для длинных документов и multi-hop/summary questions. | Выигрыш против parent-child baseline и приемлемая стоимость reindex. |
| GraphRAG | **Explore** | Подходит для corpus-level и relational вопросов; indexing дорог и сложен. | Набор вопросов, где граф действительно лучше hybrid retrieval. |
| Self-RAG / Corrective RAG | **Explore** | Полезные исследовательские patterns, но не брать целиком без ablation. | Изолированный выигрыш каждого шага. |
| Agentic RAG / iterative search | **Trial** | Для multi-hop и open-ended research; ограничивать turns и budget. | Better task success при заданном cost/latency ceiling. |
| Vector DB «потому что RAG» | **Hold** | Storage не заменяет retrieval design и evaluation. | Конкретные scale/filter/latency требования. |

## Агенты

| Подход | Статус | Позиция | Promotion gate |
| --- | --- | --- | --- |
| Deterministic workflow + LLM steps | **Adopt** | Лучший baseline, если путь решения известен. | — |
| Single-agent tool loop | **Trial** | Для задач, где последовательность действий нельзя задать заранее. | Task success, budget, stop rules, recovery tests. |
| Human approval перед необратимыми действиями | **Adopt** | Approval должен быть привязан к конкретному action и diff. | — |
| Durable state, checkpoint и idempotent tools | **Adopt** | Обязательны для long-running и state-changing agents. | — |
| Full traces + outcome eval | **Adopt** | Оцениваем final state и ключевые invariants, не один «правильный» путь. | — |
| MCP для agent-to-tool интеграций | **Trial** | Полезная стандартизация; фиксировать spec version и trust boundary. | Security review, allowlist и approval policy. |
| A2A для независимых remote agents | **Explore** | Не нужен для внутренних subagents; полезен на межсистемной границе. | Реальный interoperability use case. |
| Long-term semantic memory | **Explore** | Память — продуктовая политика данных, а не просто vector store. | Consent, TTL, delete, poisoning и retrieval eval. |
| Multi-agent orchestration | **Explore** | Оправдана для действительно параллельных, context-heavy задач. | Выигрыш против сильного single-agent baseline с учётом 10×+ token cost. |
| Fully autonomous high-impact actions | **Hold** | Prompt injection и goal misalignment остаются открытыми рисками. | Независимый safety case и узкие полномочия. |

## Что проверить в первых экспериментах

1. **RAG:** hybrid + reranker против lexical и dense baselines; 50–100 реальных вопросов, включая unanswerable и conflicting evidence.
2. **Agent:** один agent loop с 3–7 узкими tools, лимитом turns, trace и human approval; сравнить с deterministic workflow.
3. **Agentic RAG:** разрешить модели выбирать keyword/semantic search и чтение chunks, но задать budget и остановку; сравнить с one-shot RAG.
4. **Протоколы:** MCP использовать только там, где стандартизация интеграции ценнее прямого typed API; A2A отложить до появления отдельного remote-agent boundary.

