"""Відкриті приклади 05 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(5)

PUBLIC = [('view',
  ([{'name': 'Студент', 'kind': 'person'},
    {'name': 'Адміністратор', 'kind': 'person'},
    {'name': 'Каталог', 'kind': 'system'},
    {'name': 'Облікові записи', 'kind': 'system'},
    {'name': 'Вебзастосунок', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'API', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'База даних', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'Пошта', 'kind': 'container', 'parent': 'Облікові записи'},
    {'name': 'Контролер списку', 'kind': 'component', 'parent': 'API'},
    {'name': 'Сервіс кешу', 'kind': 'component', 'parent': 'API'},
    {'name': 'Форма пошуку', 'kind': 'component', 'parent': 'Вебзастосунок'}],
   'context'),
  ['Студент', 'Адміністратор', 'Каталог', 'Облікові записи']),
 ('view',
  ([{'name': 'Студент', 'kind': 'person'},
    {'name': 'Адміністратор', 'kind': 'person'},
    {'name': 'Каталог', 'kind': 'system'},
    {'name': 'Облікові записи', 'kind': 'system'},
    {'name': 'Вебзастосунок', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'API', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'База даних', 'kind': 'container', 'parent': 'Каталог'},
    {'name': 'Пошта', 'kind': 'container', 'parent': 'Облікові записи'},
    {'name': 'Контролер списку', 'kind': 'component', 'parent': 'API'},
    {'name': 'Сервіс кешу', 'kind': 'component', 'parent': 'API'},
    {'name': 'Форма пошуку', 'kind': 'component', 'parent': 'Вебзастосунок'}],
   'container',
   'Каталог'),
  ['Студент', 'Адміністратор', 'Облікові записи', 'Вебзастосунок', 'API', 'База даних'])]


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
    for name in ('view',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
