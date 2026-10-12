"""Відкриті приклади 03 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(3)

PUBLIC = [('solve',
  ([(99.9, 1)], 30),
  "Доступність системи: 99.9000 %\nДопустимий простій за 30 дн.: 43.2 хв\nДев'яток: 3"),
 ('solve',
  ([(99.0, 2)], 30),
  "Доступність системи: 99.9900 %\nДопустимий простій за 30 дн.: 4.3 хв\nДев'яток: 4")]


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
    for name in ('solve',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
