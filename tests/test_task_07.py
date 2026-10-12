"""Відкриті приклади 07 (з картки). Повний набір перевірок — у викладача."""
import re
from conftest import load

M = load(7)

HEADINGS = ["Статус", "Контекст", "Розглянуті варіанти", "Рішення", "Наслідки", "Драйвери"]


def test_title_and_sections():
    text = M.adr_text()
    assert text.strip().splitlines()[0].startswith("# ADR 7. ")
    assert re.findall(r"^## (.+)$", text, flags=re.M) == HEADINGS


def test_status_and_drivers():
    text = M.adr_text()
    assert re.search(r"^## Статус\n+прийнято\n", text, flags=re.M)
    assert "- Q2" in text and "- Q5" in text


def test_functions_exist():
    for name in ('adr_text',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
