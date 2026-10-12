"""Відкриті приклади 02 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(2)

PUBLIC = [('check_scenario',
  ({'source': 'студент',
    'stimulus': 'відкриває список обладнання',
    'environment': '300 одночасних користувачів',
    'artifact': 'вебзастосунок і база даних',
    'response': 'показує актуальну доступність',
    'measure': '95-й процентиль відповіді не більше 800 мс'},),
  []),
 ('check_scenario',
  ({'source': '',
    'stimulus': 'відкриває список обладнання',
    'environment': '300 одночасних користувачів',
    'artifact': 'вебзастосунок і база даних',
    'response': 'показує актуальну доступність',
    'measure': 'відповідь швидко'},),
  ['Порожнє поле: source', 'Міра без числа й одиниці', 'Невимірне слово: швидко'])]


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
    for name in ('check_scenario',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
