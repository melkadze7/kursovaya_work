"""Построить воспроизводимую таблицу AST-срабатываний до и после правки."""

from __future__ import annotations

from pathlib import Path

from static_guard import analyze_file, counts


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Вывести сравнение пяти правил на двух учебных файлах."""
    before = counts(analyze_file(ROOT / "samples/before.py"))
    after = counts(analyze_file(ROOT / "samples/after.py"))
    print("Правило | До | После")
    for rule in before:
        print(f"{rule:7} | {before[rule]:2} | {after[rule]:5}")
    print(f"Всего: {sum(before.values())} -> {sum(after.values())}")


if __name__ == "__main__":
    main()
