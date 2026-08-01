# 05. Данные и adaptation

**Обновлено:** 2026-08-01

## Порядок выбора

| Проблема | Первый рычаг |
| --- | --- |
| Неясная задача или формат | prompt + examples + schema |
| Нет актуальных/частных знаний | RAG / tools |
| Плохой retrieval | corpus, parser, chunking, retriever, reranker |
| Нужен устойчивый стиль/поведение | prompt; затем SFT при масштабе |
| Модель не умеет доменную задачу | data + finetuning, если base model действительно не справляется |
| Высокая latency/cost | smaller model, routing, distillation/finetuning |
| Agent выбирает неверные actions | tool design, traces, trajectory data; затем training при достаточном dataset |

Finetuning не является способом регулярно обновлять факты. RAG не является способом научить модель новому устойчивому поведению. Эти механизмы могут сочетаться.

## Prompt и context как versioned artifact

Хранить вместе:

- system/developer instructions;
- few-shot examples;
- tool descriptions и schemas;
- output schema;
- model/settings;
- retrieval/context policy;
- eval dataset/version и результаты.

Изменение tool description может быть таким же существенным, как изменение кода. Оно должно проходить eval и rollout.

## Dataset engineering

Критерии из книги — quality, coverage, quantity — остаются полезным default. Для прикладной системы добавить:

- provenance и право использования;
- temporal validity;
- data classification/PII;
- deduplication и contamination checks;
- slice labels и failure taxonomy;
- связь training example ↔ eval exclusion;
- human annotation guideline и disagreement;
- deletion/update path.

Лучший источник данных для улучшения системы — реальные failures, но production data нельзя автоматически превращать в training set без privacy, consent и quality gates.

## Synthetic data

Использовать для покрытия редких сценариев, adversarial variants, tool errors и controlled transformations. Не использовать как единственный источник truth.

Проверять:

- diversity и mode collapse;
- leakage из генератора;
- соответствие реальному input distribution;
- независимую верификацию labels;
- баланс easy/hard/ambiguous/unanswerable;
- не обучается ли система на стиле своего будущего judge.

## Когда finetuning готов к trial

- baseline prompt/RAG/tool design стабилен;
- failure повторяется и локализован в model behavior;
- есть representative train/eval split без leakage;
- improvement можно измерить executable/rubric metrics;
- объём вызовов оправдывает data/training/serving complexity;
- есть plan переобучения, rollback и monitoring drift.

Для агентов особенно ценны traces с outcome labels, но сырые trajectories содержат ошибки. Перед training нужно отделить successful reasoning/actions от случайно успешных и от policy violations.

## Knowledge lifecycle

```text
production failure
  → taxonomy + eval case
  → prompt/tool/retrieval fix
  → repeated pattern
  → curated training example
  → finetune/distill
  → regression + canary
```

Eval cases не должны бесконтрольно попадать в training data: иначе локальный прогресс превратится в contamination.

## Decision record

Для adaptation-эксперимента зафиксировать:

- failure mode и baseline;
- почему prompt/RAG/tool fix недостаточен;
- dataset provenance и sizes;
- method и base model version;
- offline results by slice;
- serving cost/latency;
- rollback и retraining trigger.

Книжные материалы: [chapter summaries](https://github.com/chiphuyen/aie-book/blob/main/chapter-summaries.md) и [resources](https://github.com/chiphuyen/aie-book/blob/main/resources.md).

