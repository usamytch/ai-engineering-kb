# AI Engineering Knowledge Base

Практическая база знаний о разработке приложений на foundation models. Структура вдохновлена книгой Chip Huyen *AI Engineering: Building Applications with Foundation Models*, но RAG и агенты вынесены в отдельные, расширенные направления.

**Состояние базы:** 2026-08-04. Это стартовая версия: здесь уже есть карта области, отобранные первичные источники, adoption radar и процесс регулярного обновления.

## Зачем эта база

- быстро понять, где новый подход находится на шкале от интересной статьи до production-практики;
- хранить не просто ссылки, а выводы, ограничения и проверяемые решения;
- связывать статьи, документацию, эксперименты, метрики и продуктовый эффект;
- не зависеть от конкретного провайдера или фреймворка;
- сохранять историю: что мы приняли, что отложили и почему.

## Карта

| Раздел | Главный вопрос |
| --- | --- |
| [00. Карта AI Engineering](knowledge/00-map.md) | Как части системы связаны друг с другом? |
| [01. Модели и интерфейсы](knowledge/01-models-and-interfaces.md) | Как выбирать модели и следить за изменениями API? |
| [02. Evaluation](knowledge/02-evaluation.md) | Как измерять качество до и после релиза? |
| [03. Context engineering и RAG](knowledge/03-context-and-rag.md) | Как доставлять модели нужные знания и проверять retrieval? |
| [04. Агенты](knowledge/04-agents.md) | Когда нужен агент, как устроить tools, memory и orchestration? |
| [05. Данные и adaptation](knowledge/05-data-and-adaptation.md) | Когда хватит prompting/RAG, а когда нужен finetuning? |
| [06. Production](knowledge/06-production.md) | Как контролировать latency, cost, reliability и observability? |
| [07. Safety и governance](knowledge/07-safety-and-governance.md) | Как ограничивать полномочия и защищать данные и инструменты? |
| [08. Product и adoption](knowledge/08-product-and-adoption.md) | Как переводить технологию из статьи в полезную функцию? |

Отдельно:

- [SOURCES.md](SOURCES.md) — проверенный реестр ключевых источников;
- [ADOPTION.md](ADOPTION.md) — текущие инженерные позиции по подходам;
- [PROCESS.md](PROCESS.md) — недельный и месячный цикл обновления;
- [inbox/](inbox/README.md) — автоматические находки, ещё не принятые в базу;
- [notes/](notes/README.md) — карточки источников после исхода `note`;
- [reviews/](reviews/README.md) — adoption reviews после исхода `review`;
- [CHANGELOG.md](CHANGELOG.md) — история содержательных изменений.

## С чего начать

1. Прочитать [карту](knowledge/00-map.md), чтобы увидеть общий pipeline.
2. Для прикладной разработки — [RAG](knowledge/03-context-and-rag.md), затем [агенты](knowledge/04-agents.md).
3. Перед экспериментом посмотреть [evaluation](knowledge/02-evaluation.md) и [adoption radar](ADOPTION.md).
4. Новую статью сначала положить в inbox или оформить по [шаблону источника](templates/source-note.md). Не переносить вывод в основную базу без проверки первоисточника и применимости.

## Главный принцип

Усложнять систему только после измеренного failure mode:

```text
prompt + structured output
  → retrieval
  → hybrid retrieval + reranking
  → deterministic tool workflow
  → single agent with tools
  → multi-agent / agentic RAG
  → finetuning
```

Это не универсальный порядок внедрения, а безопасный default: каждый следующий уровень добавляет стоимость, nondeterminism и новые способы отказа.

## Локальная работа

Требуется только Python 3.10+.

```bash
make check       # проверить локальные Markdown-ссылки и структуру
make inbox       # собрать свежие записи из watchlist.json
make triage      # применить ручную разметку последнего inbox
```

Перед `make triage` заменить `[ ]` у выбранных записей на `[drop]`, `[watch]`, `[note]` или `[review]`. Поле `Triage` руками добавлять нельзя: после обработки скрипт создаёт его сам как историю решения. Он автоматизирует только механику — удаление `drop`, фиксацию `watch` и создание scaffolds для `note`/`review`. Решение о переносе в `knowledge/`, `SOURCES.md` или `ADOPTION.md` остаётся за человеком.
