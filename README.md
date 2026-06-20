# YML Feed Generator

Тестовое задание: исправить функцию `build_yml()` для формирования товарного YML-фида Яндекс Директа.

## Структура

- `feed_task.py` — исходный модуль с данными и функцией `build_yml()`
- `django_app.py` — пример подключения к Django View и минимальный сервер для проверки
- `tests/` — автоматические тесты

## Требования

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Быстрый старт

```bash
uv sync
make test
make run
```

> **Примечание для Windows:** если у вас нет команды `make`, вы можете установить её через пакетный менеджер (например, Scoop: `scoop install make`) либо выполнять команды напрямую: `uv run python django_app.py` (вместо `make run`) и `uv run pytest tests/` (вместо `make test`).

## Полезные команды

```bash
make run        # запуск Django-сервера (http://127.0.0.1:8000/yandex-market.yml)
make test       # запуск тестов
make lint       # линтеры
make format     # форматирование
make validate   # format + lint + type-check
```
