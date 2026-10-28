
"""Проверки пяти статических правил на минимальных примерах."""

import unittest
from pathlib import Path

from staticcheck import analyze_file, analyze_source, counts

ROOT = Path(__file__).resolve().parents[1]


class AnalyzerTests(unittest.TestCase):
    def test_empty_source(self):
        self.assertEqual(analyze_source(""), [])

    def test_simple_function_clean(self):
        self.assertEqual(analyze_source("def f():\n    return 7\n"), [])

    def test_eval_detected(self):
        self.assertEqual(analyze_source("eval('2+3')")[0].rule, "S01")

    def test_shell_true_detected(self):
        self.assertEqual(analyze_source("run('a', shell=True)")[0].rule, "S02")

    def test_shell_false_allowed(self):
        self.assertEqual(analyze_source("run('a', shell=False)"), [])

    def test_bare_except_detected(self):
        code = "try:\n    pass\nexcept:\n    pass\n"
        self.assertEqual(analyze_source(code)[0].rule, "Q01")

    def test_typed_except_allowed(self):
        code = "try:\n    pass\nexcept ValueError:\n    pass\n"
        self.assertEqual(analyze_source(code), [])

    def test_mutable_list_default(self):
        self.assertEqual(analyze_source("def f(x=[]):\n    return x\n")[0].rule, "Q02")

    def test_mutable_dict_default(self):
        self.assertEqual(analyze_source("def f(x={}):\n    return x\n")[0].rule, "Q02")

    def test_none_default_allowed(self):
        self.assertEqual(analyze_source("def f(x=None):\n    return x\n"), [])

    def test_literal_password_detected(self):
        self.assertEqual(analyze_source("PASSWORD = 'example'\n")[0].rule, "S03")

    def test_environment_key_allowed(self):
        self.assertEqual(analyze_source("API_KEY = environ.get('KEY')\n"), [])

    def test_sample_before_has_five_findings(self):
        self.assertEqual(len(analyze_file(ROOT / "examples/before.py")), 5)

    def test_sample_after_has_zero_findings(self):
        self.assertEqual(analyze_file(ROOT / "examples/after.py"), [])

    def test_counts_return_five_rules(self):
        self.assertEqual(len(counts([])), 5)

    def test_finding_lines_are_sorted(self):
        found = analyze_source("PASSWORD='a'\neval('2')\n")
        self.assertEqual([item.line for item in found], [1, 2])


if __name__ == "__main__":
    unittest.main()

