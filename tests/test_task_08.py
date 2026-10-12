"""Відкриті приклади 08 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(8)

PUBLIC = [('decide',
  ({'Без кешу': {'latency': 900, 'staleness': 0, 'ops': 1},
    "Кеш у пам'яті": {'latency': 200, 'staleness': 60, 'ops': 1},
    'Спільний кеш': {'latency': 250, 'staleness': 5, 'ops': 3}},
   {'latency': {'weight': 0.4, 'direction': 'min'},
    'staleness': {'weight': 0.3, 'direction': 'min'},
    'ops': {'weight': 0.3, 'direction': 'min'}},
   [('latency', '<=', 800)]),
  'Відсічено: Без кешу (latency <= 800)\n'
  'Оцінки:\n'
  "Кеш у пам'яті: 0.700\n"
  'Спільний кеш: 0.300\n'
  "Рішення: Кеш у пам'яті\n"
  'Відрив від другого: 0.400'),
 ('decide',
  ({'Без кешу': {'latency': 900, 'staleness': 0, 'ops': 1},
    "Кеш у пам'яті": {'latency': 200, 'staleness': 60, 'ops': 1},
    'Спільний кеш': {'latency': 250, 'staleness': 5, 'ops': 3}},
   {'latency': {'weight': 0.5, 'direction': 'min'},
    'staleness': {'weight': 0.4, 'direction': 'min'},
    'ops': {'weight': 0.0, 'direction': 'min'}},
   []),
  ('ValueError', 'Сума ваг має дорівнювати 1'))]


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
    for name in ('decide',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
