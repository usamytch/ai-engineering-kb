# Реестр источников

**Проверено:** 2026-08-01

Реестр хранит основные опорные источники. Новые находки сначала попадают в `inbox/`; сюда они переходят после проверки relevance и первоисточника. `Paper` означает опубликованную работу/preprint и не гарантирует воспроизводимость или production readiness.

## Каркас AI Engineering

| Источник | Тип | Зачем |
| --- | --- | --- |
| [AI Engineering book resources — Chip Huyen](https://github.com/chiphuyen/aie-book) | Author repo | TOC, summaries, study notes, resources и case studies книги |
| [Table of Contents](https://github.com/chiphuyen/aie-book/blob/main/ToC.md) | Author repo | Исходная taxonomy: models, evals, prompts, RAG/agents, finetuning, data, inference, architecture |
| [Chapter summaries](https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md) | Author repo | Краткая проверка ключевых тезисов глав |

## Models и provider trackers

Эти ссылки используются вместо ручной таблицы «актуальных моделей».

| Источник | Тип | Зачем |
| --- | --- | --- |
| [OpenAI model catalog](https://developers.openai.com/api/docs/models) | Official docs | Текущие models/capabilities/limits |
| [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) | Official changelog | Releases и изменения API |
| [Claude models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | Official docs | Текущая линейка и migration targets |
| [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview) | Official changelog | API и platform changes |
| [Gemini models](https://ai.google.dev/gemini-api/docs/models) | Official docs | Текущие stable/preview/experimental models |
| [Gemini changelog](https://ai.google.dev/gemini-api/docs/changelog) | Official changelog | Releases и API changes |
| [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations) | Official docs | Shutdown dates и replacements |

## Evaluation

| Источник | Тип | Зачем |
| --- | --- | --- |
| [OpenAI — Working with evals](https://developers.openai.com/api/docs/guides/evals) | Official docs | Datasets, graders и eval workflow |
| [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Engineering report | Outcome, transcript и grader patterns для agents |
| [Ragas metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) | Project docs | Каталог RAG и tool/agent metrics |
| [τ-bench](https://arxiv.org/abs/2406.12045) | Paper / benchmark | Dynamic tool-agent-user interaction |
| [GAIA](https://arxiv.org/abs/2311.12983) | Paper / benchmark | Real-world questions с reasoning, tools и multimodality |
| [SWE-bench](https://arxiv.org/abs/2310.06770) | Paper / benchmark | Repository-level software engineering agents |
| [Agentic Benchmark Checklist](https://arxiv.org/abs/2507.02825) | Paper | Риски task/reward design и checklist benchmark rigor |
| [How Many Tasks Are Enough for Agent Benchmark Decisions?](https://arxiv.org/abs/2607.12338) | Paper | Свежий анализ partial agent benchmark runs |

## RAG foundations и retrieval

| Источник | Тип | Главная идея / роль |
| --- | --- | --- |
| [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) | Paper | Исходная формулировка RAG для knowledge-intensive NLP |
| [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906) | Paper | Dense dual-encoder retrieval baseline |
| [ColBERTv2](https://arxiv.org/abs/2112.01488) | Paper | Late interaction и compressed multi-vector retrieval |
| [HyDE](https://arxiv.org/abs/2212.10496) | Paper | Hypothetical document для zero-shot dense retrieval |
| [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | Engineering report | Contextual embeddings + contextual BM25 + reranking |
| [RAPTOR](https://arxiv.org/abs/2401.18059) | Paper | Tree-organized multi-level summaries для retrieval |
| [Self-RAG](https://arxiv.org/abs/2310.11511) | Paper | Retrieve/generate/critique через reflection tokens |
| [Corrective RAG](https://arxiv.org/abs/2401.15884) | Paper | Retrieval evaluation и corrective actions |
| [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | Official repository | Graph extraction, community summaries, local/global search |
| [GraphRAG docs](https://microsoft.github.io/graphrag/) | Project docs | Implementation, configuration и предупреждения о cost |

## RAG evaluation и agentic retrieval

| Источник | Тип | Главная идея / роль |
| --- | --- | --- |
| [Sub-question coverage for RAG](https://aclanthology.org/2025.naacl-long.301/) | Peer-reviewed paper | Оценка полноты open-ended ответов по facets |
| [mtRAG](https://aclanthology.org/2025.tacl-1.36/) | Peer-reviewed benchmark | Multi-turn, non-standalone и unanswerable RAG queries |
| [Deep Search over Heterogeneous Enterprise Data](https://aclanthology.org/2025.emnlp-industry.34/) | Peer-reviewed benchmark | Source-aware multi-hop reasoning across enterprise artifacts |
| [Search Wisely](https://aclanthology.org/2025.emnlp-main.998/) | Peer-reviewed paper | Over-search/under-search и uncertainty в agentic RAG |
| [A-RAG](https://arxiv.org/abs/2602.03442) | Paper | Hierarchical keyword/semantic/chunk-read interfaces для agentic retrieval |
| [SoK: Agentic RAG](https://arxiv.org/abs/2603.07379) | Paper / survey | Taxonomy, sequential decision framing, evaluation и risks |
| [Agentic-R](https://aclanthology.org/2026.findings-acl.785/) | Peer-reviewed paper | Retriever training с local relevance и global answer utility |

## Agents: architecture и engineering

| Источник | Тип | Зачем |
| --- | --- | --- |
| [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Engineering report | Workflow vs agent и composable orchestration patterns |
| [Anthropic — Effective context engineering for agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Engineering report | Context selection, just-in-time retrieval, compaction, memory |
| [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Production case study | Orchestrator-workers, parallel research, evals, durability и cost |
| [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | Official SDK docs | Agent loop, tools, handoffs, guardrails, sessions, tracing |
| [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | Project docs | Stateful graph orchestration, durable execution, persistence и human-in-the-loop |
| [LangGraph repository](https://github.com/langchain-ai/langgraph) | Official repository | Releases, activity, contributors и implementation |
| [LangGraph custom RAG agent](https://docs.langchain.com/oss/python/langgraph/agentic-rag) | Project tutorial | Conditional retrieval, grading, query rewrite и generation graph |
| [Three years of graph engineering](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) | Vendor engineering retrospective | Когда graph полезен и когда open-ended harness проще; vendor-reported adoption |
| [GitHub dependents](https://github.com/langchain-ai/langgraph/network/dependents) | Platform metadata | Breadth proxy; включает production, prototypes и transitive dependencies |
| [Elastic Security + LangGraph](https://www.elastic.co/blog/building-automatic-import-attack-discovery-langchain) | Company production case | ES\|QL generation, Automatic Import и controllable agent workflows |
| [Klarna AI Assistant](https://www.langchain.com/blog/customers-klarna) | Vendor case study | Large-scale multi-agent support; product metrics нельзя приписывать одному framework |
| [AppFolio Realm-X](https://www.langchain.com/blog/customers-appfolio) | Vendor case study | Parallel branches, state management, production tracing и eval workflow |
| [Google Agent Development Kit](https://adk.dev/) | Official project docs | Graph/multi-agent workflows, runtime, evaluation, deployment |

## Protocols и interoperability

| Источник | Snapshot | Зачем |
| --- | --- | --- |
| [Model Context Protocol specification](https://modelcontextprotocol.io/specification/latest) | Latest → 2026-07-28 при проверке | Agent/app ↔ tools/resources/prompts; authoritative spec |
| [A2A Protocol](https://a2a-protocol.org/latest/) | v1.0 при проверке | Interoperability независимых opaque agents |

MCP и A2A решают разные задачи: первый стандартизирует доступ agent/application к capabilities и context, второй — взаимодействие самостоятельных agents.

## Production и observability

| Источник | Тип | Зачем |
| --- | --- | --- |
| [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Open standard | Vendor-neutral attributes/events/spans для GenAI и agents |
| [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-python/tracing/) | Official SDK docs | Пример tracing model/tool/handoff/guardrail events |
| [LangGraph memory](https://docs.langchain.com/oss/python/langgraph/memory) | Project docs | Checkpoints, thread-scoped state и cross-thread store |

## Safety и governance

| Источник | Тип | Зачем |
| --- | --- | --- |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) | Community standard | Agent goal hijack, tool misuse, identity, supply chain, memory и другие risks |
| [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | Community standard | Prompt injection, disclosure, excessive agency и application risks |
| [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | Government framework | Govern, map, measure и manage AI risk |
| [NIST GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Government profile | Generative-AI-specific risks и suggested actions |
| [MITRE ATLAS](https://atlas.mitre.org/) | Threat knowledge base | Adversarial tactics и techniques для AI systems |
| [Anthropic — Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) | Research/engineering position | Human control, user intent, security, transparency и privacy |
| [Anthropic — Prompt injection defenses in browser use](https://www.anthropic.com/research/prompt-injection-defenses) | Research report | Layered defenses и residual risk для browser agents |

## Правила для новых источников

1. Предпочитать canonical paper, official spec/docs/repo или раскрытый engineering report.
2. Вторичный обзор хранить только если он даёт уникальную taxonomy; помечать как secondary.
3. Не добавлять vendor benchmark claim без методологии и ограничений.
4. Для быстро меняющихся страниц хранить `last checked` и при необходимости snapshot в заметке.
5. Любой источник, меняющий adoption status, должен быть связан с собственным experiment/eval либо оставаться `Explore/Watch`.
