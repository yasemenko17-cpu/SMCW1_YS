"""Відкриті приклади 06 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(6)

PUBLIC = [('utility_tree',
  ([{'id': 'Q1',
     'attribute': 'Продуктивність',
     'refinement': 'Затримка',
     'importance': 'high',
     'difficulty': 'high'},
    {'id': 'Q2',
     'attribute': 'Безпека',
     'refinement': 'Автентифікація',
     'importance': 'high',
     'difficulty': 'low'}],),
  'Корисність системи\n'
  '  Продуктивність\n'
  '    Затримка\n'
  '      Q1 (важливість: висока, складність: висока) — драйвер\n'
  '  Безпека\n'
  '    Автентифікація\n'
  '      Q2 (важливість: висока, складність: низька) — реалізувати\n'
  'Драйвери: Q1'),
 ('utility_tree',
  ([{'id': 'Q1', 'attribute': 'A', 'refinement': 'a', 'importance': 'high', 'difficulty': 'high'},
    {'id': 'Q1', 'attribute': 'B', 'refinement': 'b', 'importance': 'low', 'difficulty': 'low'}],),
  ('ValueError', 'Дубль ідентифікатора: Q1'))]


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
    for name in ('utility_tree',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
