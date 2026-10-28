
"""Сравнение результатов анализа до и после исправлений."""

from __future__ import annotations

from pathlib import Path

from staticcheck import analyze_file, counts

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    before = counts(analyze_file(ROOT / "examples/before.py"))
    after = counts(analyze_file(ROOT / "examples/after.py"))

    print("Правило | До | После")
    for rule in before:
        print(f"{rule:7} | {before[rule]:2} | {after[rule]:5}")

    print(f"Всего: {sum(before.values())} -> {sum(after.values())}")


if __name__ == "__main__":
    main()
