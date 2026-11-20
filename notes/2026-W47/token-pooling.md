# Token Pooling-Aware Training

- [Первоисточник — Tom Aarsen / Hugging Face](https://huggingface.co/blog/token-pooling), 11 ноября 2026.
- Прочитан полный текст, включая условия обучения и таблицу. Статус: `ai-draft`; код не запускался.

## Original-language synopsis

Training combines retrieval losses on full and pooled document vectors. Ward clustering supplies token groups; a straight-through estimator propagates gradients without differentiating cluster assignments. Query vectors remain unpooled.

## Мой вывод

Хороший кандидат для небольшого воспроизводимого эксперимента с multi-vector retrieval. В сопоставленных запусках ModernBERT при четырёхкратном pooling nDCG@10 на NanoBEIR растёт с 49,03 до 51,23 при одинаковом числе векторов. Условия сравнения раскрыты: один seed, одинаковые 120 тысяч MS MARCO triplets и настройки.

Ограничение существенное: уменьшение числа векторов не равно такому же сокращению всего индекса или времени ответа. Нужны замеры хранения, построения индекса и поиска на собственном корпусе; adaptive threshold дополнительно калибруется по распределению документов. Процент сохранённого качества считается относительно несжатой версии каждого отдельного encoder — сравнивать только эти проценты недостаточно.

## Опора в тексте

Блоки `b00052-b9e7c8d47d`, `b00084-1c41265c87`–`b00089-0c51825da0`; [реестр снимков](../../inbox/2026-W47/web-reading.json).
