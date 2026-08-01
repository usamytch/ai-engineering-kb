# 06. Production: inference, cost и observability

**Обновлено:** 2026-08-01

## Что оптимизировать

Для обычного generation полезны TTFT, TPOT, throughput и cost/request. Для RAG/agents важнее end-to-end:

- time-to-useful-result и p50/p95/p99;
- cost per successful task;
- tool/retrieval/model latency breakdown;
- retries, loops и timeout rate;
- queue time, cache hit rate и rate-limit failures;
- user correction/escalation rate.

Оптимизировать tokens/request без task success опасно: система может стать дешевле за счёт худшего результата и большего числа повторов пользователя.

## Версии и воспроизводимость

Каждый run должен быть связан с:

```text
application_version
model_provider + model_id + settings
prompt/tool/schema/policy versions
retriever + embedding + reranker + index versions
dataset/eval version
feature flags + tenant/permission context
```

Secrets и sensitive prompts/tool payloads не обязаны попадать в trace. Хранить hashes, IDs, redacted fields и sampling policy там, где полный payload нарушает privacy.

## Trace для RAG/agent run

- root task span;
- model turns/generations;
- retrieval queries, filters, document IDs и scores;
- reranking/context assembly;
- tool calls, approvals, errors и retries;
- handoffs/subtasks;
- checkpoints/resume;
- final outcome/eval/feedback;
- token, money и time budgets.

[OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — полезная vendor-neutral точка для атрибутов и spans. У agent SDK также могут быть встроенные traces, например [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/).

## Reliability patterns

- timeout на каждом external boundary;
- retry только transient/idempotent operations;
- circuit breaker и fallback model/tool;
- idempotency keys для side effects;
- checkpoint перед/после дорогих шагов;
- bulkhead для tenants и workloads;
- bounded queues и backpressure;
- cancellation, deadline propagation и budget enforcement;
- canary/rainbow deployment для long-running agents;
- graceful degradation: search only, draft, ask human, abstain.

## Cost toolbox

Порядок проверки:

1. убрать лишние turns, context и duplicate retrieval;
2. parallelize независимые I/O, не reasoning dependencies;
3. cache stable prefixes, retrieval и deterministic tool results;
4. route простые задачи на меньшую модель;
5. уменьшить candidate set после измерения Recall@K;
6. batch offline workloads;
7. только затем рассматривать self-hosting, quantization и specialized serving.

Для multi-agent отдельно измерять fan-out, duplicate work и synthesis loss. Token budget — часть product economics.

## SLO example

```text
Task success ≥ 92% on critical slice
Policy violations = 0 on release gate
p95 time-to-final ≤ 20 s
p95 cost per successful task ≤ $X
Tool timeout recovery ≥ 95%
Human escalation on ambiguous high-risk cases ≥ 99%
```

Числа задаются use case, таблица показывает форму контракта.

## Feedback loop

Не собирать только thumbs up/down. Полезные события:

- пользователь исправил факт/действие;
- открыл/не открыл citation;
- повторил запрос другими словами;
- отменил tool action;
- принял draft с edits;
- решил задачу downstream;
- эскалировал человеку.

Feedback превращается в improvement только после taxonomy, review и добавления regression case.

## Release checklist

- [ ] Offline eval и critical slices пройдены.
- [ ] Cost/latency budget проверен на representative load.
- [ ] Traces связывают все versions.
- [ ] PII/secrets redaction и retention настроены.
- [ ] Rate limits, timeouts, retries, cancellation протестированы.
- [ ] Есть canary, alerts и rollback.
- [ ] Для long-running runs обновление не ломает in-flight state.

