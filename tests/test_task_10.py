"""Відкриті приклади 10 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(10)

PUBLIC = [('trace_report',
  (['Q1', 'Q2', 'Q3'],
   [{'id': 'ADR-1', 'status': 'прийнято', 'scenarios': ['Q1']},
    {'id': 'ADR-2', 'status': 'прийнято', 'scenarios': ['Q2', 'Q3']}]),
  'Покриття: 3 з 3\nПідсумок: коректно'),
 ('trace_report',
  (['Q1', 'Q2'],
   [{'id': 'ADR-1', 'status': 'замінено', 'scenarios': ['Q1']},
    {'id': 'ADR-2', 'status': 'прийнято', 'scenarios': ['Q1'], 'supersedes': 'ADR-1'},
    {'id': 'ADR-3', 'status': 'запропоновано', 'scenarios': ['Q2']}]),
  'Покриття: 1 з 2\nБез рішення: Q2\nПідсумок: проблем 1')]


def _check(fn, args, expected):
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            getattr(M, fn)(*copy.deepcopy(args))
        assert str(info.value) == expected[1]
    else:
        assert getattr(M, fn)(*copy.deepcopy(args)) == expected


@pytest.mark.parametrize("fn,args,expected", PUBLIC, ids=[f"p{i}" for i in range(len(PUBLIC))])
def test_public(fn, args, expected):
    _check(fn, args, expected)


def test_functions_exist():
    for name in ('trace_report',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
