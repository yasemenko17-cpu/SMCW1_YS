"""Відкриті приклади 01 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(1)

PUBLIC = [('select_drivers',
  ([{'id': 'R1', 'kind': 'functional', 'importance': 'high', 'difficulty': 'low'},
    {'id': 'R2', 'kind': 'quality', 'importance': 'high', 'difficulty': 'high'},
    {'id': 'R3', 'kind': 'constraint', 'importance': 'high', 'difficulty': 'low'},
    {'id': 'R4', 'kind': 'business', 'importance': 'medium', 'difficulty': 'high'},
    {'id': 'R5', 'kind': 'quality', 'importance': 'high', 'difficulty': 'medium'}],),
  ['R2', 'R5', 'R3']),
 ('select_drivers',
  ([{'id': 'R1', 'kind': 'quality', 'importance': 'critical', 'difficulty': 'high'}],),
  ('ValueError', 'Некоректне значення поля importance: critical'))]


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
    for name in ('select_drivers',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
