"""УМЫШЛЕННО НЕБЕЗОПАСНЫЙ УЧЕБНЫЙ ПРИМЕР: НЕ ЗАПУСКАТЬ.

Используется исключительно как текст для статического анализа.
"""

import subprocess

SECRET_KEY = "demo-only-placeholder"


def parse_score(expression):
    return eval(expression)


def run_diagnostic(user_option):
    return subprocess.run("echo " + user_option, shell=True, check=False)


def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


def to_number(value):
    try:
        return int(value)
    except:
        return 0
