# Процесс обновления базы

**Обновлено:** 2026-08-04

Цель процесса — отделить discovery от принятия решений. Свежесть важна, но одна новая статья не должна автоматически менять production-подход.

## Два цикла

### Еженедельный discovery — 20–30 минут

1. Запустить `make inbox` или дождаться scheduled GitHub Action.
2. Удалить явно нерелевантное и дубликаты.
3. Для потенциально важных записей открыть первоисточник, а не пересказ.
4. Поставить один исход в checkbox (`[note]`) или в поле `Triage`:
   - `drop` — не относится к прикладной AI engineering или не добавляет нового;
   - `watch` — сигнал интересный, но данных мало;
   - `note` — оформить заметку и связать с тематическим разделом;
   - `review` — создать adoption review, если подход может изменить архитектуру.
5. Запустить `make triage`: он удалит `drop`, отметит `watch`, создаст scaffold source note для `note` и adoption review для `review`.
6. Заполнить созданные scaffolds после чтения первоисточника.
7. Зафиксировать содержательные изменения в `CHANGELOG.md`.

### Ежемесячный synthesis — 60–90 минут

1. Просмотреть накопившийся inbox и устаревающие ссылки.
2. Обновить один или несколько тематических файлов: тезисы, failure modes, метрики.
3. Пересмотреть статусы в `ADOPTION.md`.
4. Проверить changelog-и провайдеров, протоколов и ключевых библиотек.
5. Запустить `make check`.
6. В PR ответить на три вопроса:
   - Что действительно изменилось?
   - Какие решения или эксперименты это затрагивает?
   - Какие факты могут опровергнуть новый вывод?

## Поток одной находки

```text
feed / paper / release
        ↓
      inbox
        ↓  ручная разметка + make triage
   source note
        ↓  воспроизводимость / сравнение с baseline
 adoption review
        ↓
 knowledge + SOURCES + ADOPTION + CHANGELOG
```

## Минимальная карточка источника

Использовать [templates/source-note.md](templates/source-note.md). Обязательные поля:

- стабильная ссылка, автор/организация и дата публикации;
- тип: `paper`, `official-docs`, `spec`, `benchmark`, `engineering-report`, `release`;
- краткий claim своими словами;
- какие данные или benchmark поддерживают claim;
- ограничения и конфликт интересов;
- к какому решению это относится;
- дата последней проверки.

## Иерархия доказательств

От более сильного сигнала к более слабому:

1. воспроизводимый эксперимент на нашем use case;
2. независимые воспроизводимые результаты и открытые artifacts;
3. peer-reviewed paper с подходящими данными и baseline;
4. качественный technical report / benchmark с раскрытой методологией;
5. официальная документация — источник истины о конкретном API, но не о сравнительном качестве;
6. engineering blog — полезен как production case study, но результаты могут быть vendor-specific;
7. агрегатор, пост или видео — только discovery, не основание для adoption.

## Правило актуальности

| Тип | Перепроверять | Что считать устаревшим |
| --- | --- | --- |
| Модели, цены, API, deprecations | ежемесячно | snapshot старше 30 дней |
| SDK, agent frameworks, протоколы | ежемесячно | ссылка не на текущую stable spec/release |
| Security guidance | ежеквартально и после инцидентов | заменённая версия стандарта |
| Papers и фундаментальные методы | раз в год | появились сильные опровержения или лучшие baselines |
| Adoption-решения | ежеквартально | нет владельца, метрики или последнего review |

Не хранить в базе цены и leaderboard positions без даты snapshot. Для быстро меняющихся данных лучше хранить ссылку на официальный tracker и собственный результат eval.

## Переходы adoption

- `watch → explore`: есть понятный use case и правдоподобный выигрыш.
- `explore → trial`: определены baseline, dataset, success metric, budget и stop condition.
- `trial → adopt`: выигрыш повторяется на representative eval и окупает complexity/cost.
- `trial → hold`: выигрыш нестабилен, слишком дорог или требует незрелой инфраструктуры.
- `adopt → retire`: новая альтернатива прошла те же gates; есть migration plan.

Шаблон решения — [templates/adoption-review.md](templates/adoption-review.md).

## Критерии для RAG

Минимум отдельно измерять:

- retrieval: Recall@K / nDCG / MRR или task-specific evidence coverage;
- context: долю полезного, шум, дубликаты, потерю parent context;
- answer: correctness, faithfulness, citation correctness, completeness;
- system: p50/p95 latency, стоимость, cache hit rate, freshness;
- robustness: unanswerable queries, конфликтующие и вредоносные документы.

## Критерии для агентов

Минимум отдельно измерять:

- task success и корректный final state;
- tool selection и аргументы вызова;
- policy violations и лишние/опасные действия;
- количество turns/tool calls, latency и стоимость;
- recovery после tool error, timeout и partial failure;
- частоту и качество human escalation;
- повторяемость на нескольких запусках, а не один красивый trace.

## Pull request checklist

- [ ] Ссылка ведёт на первоисточник или явно помечена как discovery.
- [ ] Claim пересказан своими словами и не шире данных.
- [ ] Указаны ограничения и дата проверки.
- [ ] Новая технология не помечена `adopt` без своего eval.
- [ ] Обновлены связанные `knowledge/`, `SOURCES.md`, `ADOPTION.md` и `CHANGELOG.md` там, где нужно.
- [ ] `make check` проходит.
