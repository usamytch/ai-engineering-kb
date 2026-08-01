# 04. Агенты

**Обновлено:** 2026-08-01

## Определение

Рабочее определение: агент — модель, которая в цикле сама выбирает действия и tools на основе наблюдений до достижения цели, лимита или передачи решения человеку.

```text
goal → decide → act/tool → observe → update state → stop / ask / repeat
```

Если последовательность шагов известна заранее, это workflow с LLM-компонентами — обычно более простой и надёжный вариант. Полезное различие между workflow и agent разобрано в [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## Когда агент оправдан

- задача open-ended и путь зависит от промежуточных результатов;
- требуется несколько heterogeneous tools;
- ошибки можно обнаружить по observation и исправить;
- ценность результата покрывает дополнительные turns/cost;
- у задачи есть ясное состояние завершения или escalation;
- полномочия можно сузить и наблюдать.

Не начинать с агента для deterministic ETL, простого routing, одной retrieval операции или необратимых действий без approval.

## Production anatomy

```mermaid
flowchart LR
    G["Goal + policy"] --> L["Agent loop"]
    L --> M["Model"]
    M --> T["Typed tools"]
    T --> X["Sandbox / external systems"]
    X --> O["Observations"]
    O --> L
    S["Durable state + checkpoints"] -.-> L
    H["Human approval / escalation"] -.-> L
    B["Budgets + guardrails"] -.-> L
    L --> Z["Final state / artifact"]
    L --> R["Traces + evals"]
```

Модель — planner/decision-maker, но harness отвечает за permissions, execution, state, retries, timeouts, budgets, observability и policy enforcement.

## Tool design

Хороший tool:

- имеет одно ясное назначение и отличимое имя;
- использует строгую schema и enum вместо свободного текста;
- возвращает compact structured observation и actionable errors;
- сообщает read-only он или state-changing;
- проверяет authentication/authorization вне модели;
- поддерживает idempotency key там, где возможен retry;
- имеет timeout, cancellation и rate limit;
- для опасного действия показывает пользователю точный diff/target перед approval.

Сначала 3–7 узких tools. Большой каталог ухудшает выбор; использовать namespacing, allowlist или tool search только после eval.

## Orchestration patterns

| Pattern | Когда использовать | Failure mode |
| --- | --- | --- |
| Prompt chaining | фиксированная последовательность | propagation error |
| Routing | классы задач известны | misrouting |
| Parallel fan-out/fan-in | независимые проверки/исследования | дубли, cost, synthesis loss |
| Orchestrator–workers | динамическая декомпозиция | плохие boundaries и coordination |
| Evaluator–optimizer | критерий можно проверять итеративно | бесконечный polishing loop |
| Handoff | отдельный specialist должен принять conversation | context loss, unclear ownership |
| Agent-as-tool | manager сохраняет контроль и вызывает specialist | bottleneck у manager |

Multi-agent нужен не из-за количества ролей в prompt. Он оправдан отдельными context windows, параллелизмом, trust boundaries или independently deployable services.

[Anthropic multi-agent research case study](https://www.anthropic.com/engineering/multi-agent-research-system) показывает сильный breadth-first use case, но также сообщает существенно больший token расход и сложность coordination. Поэтому статус multi-agent в этой базе — `Explore`.

## Context и memory

Context window — рабочая память, не база данных. Для длинных runs:

- хранить authoritative state вне prompt;
- checkpoint после значимого action;
- compact old turns, сохраняя goals, decisions, open items и artifact references;
- подгружать context just-in-time через tools;
- передавать subagent-ам task contract и ссылки на artifacts, а не весь transcript;
- версионировать memory writes и позволять delete/correct.

[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — хороший current overview just-in-time retrieval, compaction и context hygiene.

## Durable execution

Long-running agent — распределённая state machine с nondeterministic policy. Поэтому нужны:

- persistent run/task ID и state version;
- idempotent tool calls;
- checkpoint/replay/resume;
- retry policy по типу ошибки, а не слепой retry;
- deterministic side-effect boundary;
- cancellation и deadline;
- version pinning для активных runs;
- partial failure handling и compensation.

[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) фокусируется на явном state graph, durable execution, persistence и human-in-the-loop; [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — на agent loop, tools, handoffs, guardrails, sessions и tracing; [Google ADK](https://adk.dev/) — на graph/multi-agent workflows, runtime, evaluation и deployment. Выбирать после требований и небольшого spike, а не по популярности.

### LangGraph: актуальность и adoption

**Вывод на 2026-08-01:** LangGraph актуален и относится к широко используемым agent frameworks, но его правильный статус — `Trial`, а не универсальный `Adopt`. Это low-level orchestration framework для long-running stateful agents и workflows, а не готовый «умный агент» и не retrieval engine.

Он особенно уместен, когда системе нужны явные state transitions, циклы и retries, parallel branches, checkpoint/resume, interrupt перед side effect и воспроизводимый путь выполнения. Для one-shot RAG, простого tool loop или open-ended research agent с постоянно меняющимся планом graph abstraction может добавить лишние nodes, state schemas и framework coupling. Сами авторы [отдельно описывают случаи, когда graph не нужен](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph#when-not-to-use-graphs).

#### Сигналы масштаба

| Сигнал | Snapshot 2026-08-01 | Что он действительно доказывает |
| --- | --- | --- |
| Core release | [1.2.10 от 2026-07-28](https://github.com/langchain-ai/langgraph/releases/tag/1.2.10); 1.0 вышел в октябре 2025 | Есть stable major и активное развитие, но API всё ещё меняется заметно. |
| GitHub | [38.6k stars, 6.5k forks, 283 contributors](https://github.com/langchain-ai/langgraph) | Большое и активное OSS-сообщество; stars не равны production usage. |
| Dependents | [42,365 repositories и 3,022 packages](https://github.com/langchain-ai/langgraph/network/dependents) | Широкое включение в manifests; сюда входят tutorials, prototypes и transitive dependencies. |
| Активность | 227 commits в `main` и 42 monorepo releases с 2026-05-01 | Проект живой; высокая частота релизов одновременно повышает migration load. |
| Downloads | Авторы сообщают о [65M+ downloads в месяц](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) | Сильный сигнал распространения, но это vendor-reported metric без разбивки direct/transitive/prod. |

#### Публичные production cases

| Case | Насколько глубоко | Качество evidence |
| --- | --- | --- |
| [Elastic Security](https://www.elastic.co/blog/building-automatic-import-attack-discovery-langchain) | LangGraph управлял end-to-end ES\|QL generation и Automatic Import; в публикации 2024 года AI Assistant описан как production deployment с 350+ users. | Сильный технический разбор на сайте самой компании, но ранний snapshot и совместное авторство с LangChain. |
| [Klarna AI Assistant](https://www.langchain.com/blog/customers-klarna) | Multi-agent routing для payments/refunds/escalations; case сообщает 2.5M conversations, ~70% automation repetitive support и 80% reduction resolution time. | Реальный крупный deployment и цитата CEO, но материал опубликован vendor-ом; эффект нельзя приписать только LangGraph. |
| [AppFolio Realm-X](https://www.langchain.com/blog/customers-appfolio) | Parallel graph branches, aggregation, state management и self-validation в production copilot; ранние пользователи сообщали 10+ saved hours/week. | Есть архитектурные детали, но это vendor case study, а продуктовый результат относится ко всей системе. |

[Vendor showcase](https://www.langchain.com/built-with-langgraph) также называет LinkedIn, Uber и другие компании. Это полезный breadth signal, но без собственного technical report компании не считать его независимым доказательством глубины внедрения.

#### Практическая позиция

- **Ширина adoption:** высокая относительно agent frameworks; ecosystem уже далеко за пределами demo-проектов.
- **Глубина adoption:** доказаны stateful production workflows и customer-facing agents, включая крупные компании; публичных независимых данных о reliability, incident rate, migration cost и доле traffic мало.
- **Использовать:** для контролируемого graph/workflow с agentic nodes, durable state и human interrupts.
- **Не использовать по умолчанию:** для простого линейного pipeline, одного retrieval call или полностью open-ended harness.
- **Promotion gate:** fault-injection на resume/idempotency, latency/cost против собственного orchestrator, version/checkpoint migration test, trace coverage, security review и возможность вынести business logic из framework-specific nodes.

## MCP и A2A

| Протокол | Граница | Использование |
| --- | --- | --- |
| [MCP](https://modelcontextprotocol.io/specification/latest) | agent/application ↔ tools, resources, prompts | стандартизировать подключение context и capabilities |
| [A2A](https://a2a-protocol.org/latest/) | independent agent ↔ independent agent | discovery, delegation и обмен task/results между opaque systems |

MCP не является agent framework, а A2A не нужен для обычного локального subagent call. Protocol adoption не отменяет allowlist, OAuth/scopes, consent, input validation и threat modeling. Фиксировать поддерживаемую версию spec: latest MCP на дату snapshot — 2026-07-28, A2A — 1.0.

## Human-in-the-loop

Approval нужен перед:

- отправкой сообщения/публикацией;
- покупкой, переводом денег, удалением и irreversible writes;
- повышением permissions или раскрытием данных;
- выполнением кода вне узкого sandbox;
- действием при высокой неопределённости или policy conflict.

Плохой approval: «Разрешить агенту продолжить?». Хороший: actor, exact action, target, diff, cost, source of instruction и возможность отклонить/изменить.

## Stop conditions и budgets

Harness должен ограничивать:

- max turns и max repeated action;
- token/tool/money budget;
- wall-clock deadline;
- allowed domains/resources;
- maximum delegation depth/fan-out;
- no-progress detection;
- escalation after ambiguity, conflict or repeated failure.

Модель может предложить остановку, но enforcement должен быть deterministic.

## Evaluation

Главное — task outcome/final state. Дополнительно:

- policy compliance;
- tool selection и argument correctness;
- trajectory efficiency;
- recovery и escalation;
- cost/latency per success;
- variance across repeated runs;
- adversarial environment/user/tool outputs.

Для state-changing agents создавать disposable simulated environment и проверять state diff. См. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) и [evaluation section](02-evaluation.md).

## Security baseline

- treat all retrieved/tool content as untrusted data;
- least privilege и short-lived credentials;
- read/write tools разделены;
- sandbox для code/browser/computer use;
- egress allowlist и secret isolation;
- approval на high-impact actions;
- memory write validation и provenance;
- tool/MCP server supply-chain review;
- audit trail без бесконтрольного хранения sensitive content;
- tests на indirect prompt injection, confused deputy и data exfiltration.

Ориентиры: [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) и [MCP security principles](https://modelcontextprotocol.io/specification/latest#security-and-trust-safety).

## First production agent checklist

- [ ] Есть сильный non-agent/workflow baseline.
- [ ] Цель и successful final state executable.
- [ ] Tools узкие, typed, permissioned и idempotent.
- [ ] Есть max turns/budget/no-progress stop.
- [ ] State/checkpoints живут вне context window.
- [ ] Side effects требуют appropriate approval.
- [ ] Traces содержат версии model/prompt/tool/schema/policy.
- [ ] Есть failure-injection eval: timeout, malformed output, stale data, prompt injection.
- [ ] Canary и rollback не ломают активные runs.
