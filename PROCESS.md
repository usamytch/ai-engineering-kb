# Процесс обновления базы

**Обновлено:** 2026-10-16

Цель процесса — отделить discovery от принятия решений. Свежесть важна, но одна новая статья не должна автоматически менять production-подход.

После перерыва задавать `week-start --since YYYY-MM-DD`. Обычный запуск
смотрит на 8 дней назад и не восстанавливает месяц автоматически. Успешность
обновления проверять по `manifest.json → discovery.complete`, датам окна и
числу просмотренных страниц, а не только по числу карточек. `--limit-per-feed 0`
означает отсутствие лимита; положительный лимит, сработавший на источнике,
помечает сбор неполным. Пагинация сохраняет новые ревизии старых статей.

Полный discovery-каталог, просмотр abstract и чтение полного текста — разные
уровни работы. В reading guide явно указывать глубину проверки и список
действительно прочитанных статей. AI-анализ остаётся `ai-draft`; подтвердить
его от имени человека можно только после явного человеческого approval.

## Два цикла

### Еженедельный discovery — 30–60 минут

1. Запустить `make week-start` или дождаться scheduled GitHub Action. Результат
   — `inbox/YYYY-Www/index.md` и точный `manifest.json`.
2. Просмотреть title + abstract и поставить один исход:
   - `[d]` / drop — нерелевантно, дубль или не добавляет нового;
   - `[w]` / watch — сигнал интересный, но deep read сейчас не окупится;
   - `[n]` / note — скачать именно статью и получить deep source summary;
   - `[r]` / review — deep summary плюс adoption-review scaffold.
3. Проверить план: `make week-process AIDB_ARGS=--dry-run`.
4. Запустить `make week-process PROVIDER=codex`. Для каждого `[n]`/`[r]`
   pipeline последовательно:
   - скачивает arXiv HTML и PDF, а для review/HTML fallback — TeX source;
   - отвергает abstract/error page как «полную статью»;
   - строит canonical `document.jsonl` со стабильными block IDs и locators;
   - получает structured deep summary на доминирующем языке самой статьи
     от отдельной LLM-сесии; evidence quotes не переводятся;
   - проверяет JSON Schema, block IDs, exact quotes и grounding чисел;
   - пишет tracked analysis/summary и только затем ставит `[x]`.
5. Запустить `make review`, открыть summary и вручную проверить основной claim,
   ключевое число, ablation/negative result и главное ограничение.
6. Подтвердить проверенное: `make paper-approve PAPER=<id> REVIEWER=<name>`.
7. Перенести в `SOURCES.md`/`knowledge/` только собственный синтез. Одна статья
   сама по себе не переводит технологию в Trial/Adopt.
8. Запустить `make week-close`: команда проверит незавершённые решения, создаст
   digest/closeout; затем `make check`.

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
feed / arXiv metadata / release
             ↓
   inbox/YYYY-Www/{index,manifest}
             ↓  d/w/n/r + make week-process
   full article → canonical blocks
             ↓  structured LLM + evidence validation
 papers/<id>/versions/vN/{analysis,summary,manifest}
             ↓  human approval / local experiment
 knowledge + SOURCES + ADOPTION + CHANGELOG
```

## Где лежат сами статьи

```text
inbox/2026-W34/                  weekly queue + machine state
papers/arxiv/2608.16889/        долговечная tracked сущность статьи
  metadata.json
  index.md
  versions/v1/
    manifest.json               URLs, hashes, extractor/provider provenance
    analysis.json               source of truth для summary
    summary.md                  deterministic render, статус ai-draft/verified
.aidb/artifacts/arxiv/2608.16889/v1/
  article.html
  paper.pdf
  source.tar.gz
  document.jsonl
  document.md
```

`.aidb/` не попадает в Git: лицензии arXiv различаются, а бинарные и полные
тексты слишком тяжёлы для обычного repository history. Tracked manifest хранит
URL, MIME, размер и SHA-256, поэтому локальный artifact можно проверить и
воспроизвести. Конкретная версия arXiv является единицей анализа: новая `v2`
получает отдельную папку.

TeX считается недоверенным вводом. AIDB никогда не компилирует его, не включает
shell escape, не распаковывает symlinks/path traversal и ограничивает число и
размер файлов. Summarizer работает без web/MCP/tools; текст статьи передаётся
как данные, а не как инструкция.

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
