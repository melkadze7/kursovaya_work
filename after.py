"""Исправленные учебные функции без динамического исполнения кода."""

from __future__ import annotations

import os


def parse_score(label: str) -> int:
    """Получить оценку только из ограниченного набора допустимых значений."""
    scores = {"one": 1, "two": 2, "three": 3}
    if label not in scores:
        raise ValueError("Неизвестная оценка")
    return scores[label]


def format_diagnostic(user_option: str) -> str:
    """Сформировать безопасное сообщение без вызова командной оболочки."""
    if not user_option.isidentifier():
        raise ValueError("Недопустимый параметр")
    return f"Проверить: {user_option}"


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Не использовать изменяемый объект в аргументах по умолчанию."""
    result = list(tags) if tags is not None else []
    result.append(tag)
    return result


def to_number(value: str) -> int:
    """Обрабатывать ожидаемую ошибку преобразования, а не все исключения."""
    try:
        return int(value)
    except ValueError:
        return 0


def configured_key() -> str:
    """Читать значение из окружения, не записывая секрет в исходный код."""
    return os.environ.get("DEMO_SERVICE_KEY", "")
