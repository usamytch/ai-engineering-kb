# 02. Evaluation

**Обновлено:** 2026-08-01

## Позиция

Evaluation — не последняя стадия и не один score. Это executable specification поведения системы. Начать можно с 20–50 тщательно выбранных случаев; затем dataset растёт из production failures и новых продуктовых сценариев.

## Пирамида

```text
production outcomes + user feedback
  end-to-end offline tasks / final state
    component evals: retrieval, tools, model, guardrails
      deterministic unit/contract tests
```

Нижние уровни быстрее локализуют проблему; верхние отвечают, полезна ли система в целом.

## Набор методов

| Метод | Хорош для | Ограничение |
| --- | --- | --- |
| Exact / executable | schema, code, SQL, state change, citations | Не покрывает открытое качество |
| Reference-based | QA с эталоном, extraction | Эталон может быть неполным |
| Pairwise comparison | выбор лучшего варианта | Position/order bias, нужен anchor |
| LLM-as-judge | open-ended rubrics, масштабирование | Judge drift и bias; калибровать на людях |
| Human review | subtle quality, policy, discovery | Дорого и медленно |
| Online outcome | реальная польза | Confounders, delayed signal, риск для пользователя |

## Дизайн eval set

- representative happy paths;
- high-value и high-risk cases;
- long-tail failures из production;
- unanswerable/ambiguous inputs;
- conflicting, stale и adversarial context;
- tool/API failures и partial state;
- разные языки, длины, роли и permission levels;
- slice labels, чтобы общий score не скрывал регрессию.

Каждый case должен иметь `input`, `expected invariants`, `allowed variation`, `failure severity` и provenance.

## RAG evaluation

Не оценивать только финальный текст. Разделять:

1. **Retrieval:** Recall@K, precision, MRR/nDCG, evidence/sub-question coverage.
2. **Context assembly:** noise, duplication, context order, token budget, source diversity.
3. **Generation:** correctness, faithfulness, completeness, citation correctness, abstention.
4. **System:** freshness, latency, cost и robustness.

[Ragas](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/) полезен как каталог и реализация метрик, но готовая LLM-metric не заменяет калибровку на вашем домене.

## Agent evaluation

Агент может прийти к верному результату разными путями, поэтому главный слой — **outcome/final state**. Trajectory нужна для диагностики и policy checks.

Минимальный scorecard:

| Категория | Примеры |
| --- | --- |
| Outcome | task success, correct final state, completeness |
| Actions | tool choice, argument validity, prohibited actions |
| Process | loops, redundant calls, handoff quality, recovery |
| Resources | turns, tokens, tools, wall time, cost per success |
| Oversight | correct escalation, approval bypass attempts |
| Robustness | success distribution по 3–10 повторам |

В 2026 agent benchmarks всё ещё требуют осторожности: [Agentic Benchmark Checklist](https://arxiv.org/abs/2507.02825) показывает, что task setup и reward design могут сильно искажать выводы. Для примеров сред полезны [τ-bench](https://arxiv.org/abs/2406.12045), [GAIA](https://arxiv.org/abs/2311.12983) и [SWE-bench](https://arxiv.org/abs/2310.06770), но выбор модели для продукта должен опираться на private eval.

Практические engineering guides: [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) и [OpenAI evals](https://developers.openai.com/api/docs/guides/evals).

## LLM-as-judge checklist

- rubric с наблюдаемыми критериями, а не «насколько ответ хорош»;
- reference/source context там, где проверяется факт;
- blinded candidate order для сравнений;
- human-labeled calibration set;
- judge model и prompt version в trace;
- периодическая проверка disagreement и drift;
- exact checks поверх judge там, где возможно.

## Release gate

Не требовать улучшения каждого score, но заранее задать:

- primary metric и non-inferiority thresholds;
- critical slices без регрессий;
- safety invariants с нулевой или очень низкой tolerance;
- p95 latency и cost ceiling;
- rollback trigger после canary.

