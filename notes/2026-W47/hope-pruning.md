# Higher-Order Pruning of Experts

- [Первоисточник — Amazon, публикация на Hugging Face](https://huggingface.co/blog/amazon/higher-order-pruning-experts), 9 ноября 2026.
- Прочитан текст обзора HOPE. Статус: `ai-draft`; исходная научная работа и код отдельно не воспроизводились.

## Original-language synopsis

HOPE selects experts for removal using pairwise co-activation statistics rather than independent importance scores. A calibrated quadratic surrogate is optimized through continuous relaxation and rounding, independently for each layer.

## Мой вывод

Это полезная альтернатива streaming: эксперты удаляются окончательно, поэтому выигрыш памяти оплачивается возможной потерей качества, а не чтением SSD на каждом промахе.

Авторы сравнивают три модели, две калибровочные выборки и несколько степеней pruning. Преимущество заметнее при удалении 40–50% экспертов; на меньших долях простые методы бывают конкурентоспособны. Лучший средний ранг не означает победу на каждой задаче, а единичное превышение несжатой модели не доказывает общий выигрыш от удаления экспертов.

Меня интересует проверка на собственных agent-трассах с контролем редких навыков. Парные взаимодействия внутри слоя не учитывают зависимости между слоями; калибровочная выборка может не представлять будущую нагрузку. Нужны также реальные замеры latency и throughput: сокращение весов само по себе их не определяет.

## Опора в тексте

Блоки `b00018-1f64d9b2c6`–`b00029-cfcd862b07`, `b00033-1f7a0f2e70`–`b00038-cb37a05774`, `b00056-c53935a2e1`; [реестр снимков](../../inbox/2026-W47/web-reading.json).
