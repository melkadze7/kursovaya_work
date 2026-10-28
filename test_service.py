"""Проверки бизнес-логики без сетевых зависимостей."""

import json
import tempfile
import unittest
from pathlib import Path

from static_guard import TicketBoard, ValidationError


class TicketBoardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "tickets.json"
        self.board = TicketBoard(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_initial_empty(self):
        self.assertEqual(self.board.summary(), {"всего": 0, "закрыто": 0})

    def test_add_id(self):
        self.assertEqual(self.board.add("Задача", "Анна").identifier, 1)

    def test_add_trims_whitespace(self):
        self.assertEqual(self.board.add("  Задача  ", " Анна ").title, "Задача")

    def test_add_two_increments(self):
        self.board.add("Первая", "Анна")
        self.assertEqual(self.board.add("Вторая", "Борис").identifier, 2)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.board.add("  ", "Анна")

    def test_long_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.board.add("x" * 81, "Анна")

    def test_empty_assignee_rejected(self):
        with self.assertRaises(ValidationError):
            self.board.add("Задача", " ")

    def test_bad_title_type_rejected(self):
        with self.assertRaises(ValidationError):
            self.board.add(None, "Анна")

    def test_bad_assignee_type_rejected(self):
        with self.assertRaises(ValidationError):
            self.board.add("Задача", None)

    def test_close(self):
        self.board.add("Задача", "Анна")
        self.assertEqual(self.board.close(1).status, "Закрыта")

    def test_find_missing(self):
        with self.assertRaises(ValidationError):
            self.board.find(10)

    def test_close_missing(self):
        with self.assertRaises(ValidationError):
            self.board.close(10)

    def test_summary_after_close(self):
        self.board.add("Задача", "Анна")
        self.board.add("Вторая", "Борис")
        self.board.close(1)
        self.assertEqual(self.board.summary(), {"всего": 2, "закрыто": 1})

    def test_json_persistence(self):
        self.board.add("Задача", "Анна")
        self.assertEqual(TicketBoard(self.path).find(1).title, "Задача")

    def test_no_temporary_file_remains(self):
        self.board.add("Задача", "Анна")
        self.assertFalse(self.path.with_suffix(".json.tmp").exists())

    def test_invalid_json_structure_rejected(self):
        self.path.write_text(json.dumps({"wrong": 1}), encoding="utf-8")
        with self.assertRaises(ValidationError):
            TicketBoard(self.path)


if __name__ == "__main__":
    unittest.main()
