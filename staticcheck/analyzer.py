"""Небольшой статический анализатор пяти учебных AST-шаблонов.

Отчёт показывает потенциальные проблемы, а не доказанные уязвимости.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    """Одна диагностическая запись с идентификатором правила и строкой."""

    rule: str
    line: int
    detail: str


SECRETS = {"PASSWORD", "SECRET", "SECRET_KEY", "API_KEY", "TOKEN", "SECRET_TOKEN"}


def _literal_secret(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, str) and bool(node.value)


def _is_eval(call: ast.Call) -> bool:
    return isinstance(call.func, ast.Name) and call.func.id == "eval"


def analyze_source(source: str) -> list[Finding]:
    """Выявить пять демонстрационных паттернов, не выполняя исходный код."""
    tree = ast.parse(source)
    findings: list[Finding] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if _is_eval(node):
                findings.append(Finding("S01", node.lineno, "Динамическое выполнение eval"))
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append(Finding("S02", node.lineno, "Запуск команды с shell=True"))
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding("Q01", node.lineno, "Обработчик except без указанного исключения"))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            defaults = [*node.args.defaults, *(value for value in node.args.kw_defaults if value is not None)]
            if any(isinstance(value, (ast.List, ast.Dict, ast.Set)) for value in defaults):
                findings.append(Finding("Q02", node.lineno, "Изменяемое значение аргумента по умолчанию"))
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            if value is not None and _literal_secret(value):
                for target in targets:
                    if isinstance(target, ast.Name) and target.id.upper() in SECRETS:
                        findings.append(Finding("S03", node.lineno, "Строковый секрет в исходном коде"))
    return sorted(findings, key=lambda item: (item.line, item.rule))


def analyze_file(path: str | Path) -> list[Finding]:
    """Прочитать Python-файл в UTF-8 и проверить его AST."""
    return analyze_source(Path(path).read_text(encoding="utf-8"))


def counts(findings: list[Finding]) -> dict[str, int]:
    """Подсчитать диагностические срабатывания по кодам правил."""
    return {rule: sum(item.rule == rule for item in findings) for rule in ("S01", "S02", "S03", "Q01", "Q02")}
