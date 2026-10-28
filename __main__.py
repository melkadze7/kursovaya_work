"""Точка входа в демонстрацию AST-проверки."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_file, counts


def main() -> None:
    """Вывести диагностические записи для одного указанного файла."""
    parser = argparse.ArgumentParser(description="Учебный статический анализатор")
    parser.add_argument("path", type=Path, help="Python-файл для анализа")
    args = parser.parse_args()
    findings = analyze_file(args.path)
    for item in findings:
        print(f"{item.rule} | строка {item.line}: {item.detail}")
    print(f"Всего срабатываний: {len(findings)}; по правилам: {counts(findings)}")


if __name__ == "__main__":
    main()
