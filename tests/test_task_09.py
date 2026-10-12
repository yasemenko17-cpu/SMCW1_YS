"""Відкриті приклади 09 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(9)

PUBLIC = [('to_mermaid',
  ({'title': 'Каталог ресурсів: контейнери',
    'scope': 'catalog',
    'people': [{'id': 'student', 'name': 'Студент', 'description': 'Переглядає каталог'}],
    'systems': [{'id': 'catalog',
                 'name': 'Каталог ресурсів',
                 'description': 'Облік обладнання',
                 'external': False},
                {'id': 'accounts',
                 'name': 'Облікові записи коледжу',
                 'description': 'Зовнішня система входу',
                 'external': True}],
    'containers': [{'id': 'web',
                    'name': 'Вебзастосунок',
                    'technology': 'TypeScript, React',
                    'description': 'Показує список',
                    'kind': 'app'},
                   {'id': 'api',
                    'name': 'API',
                    'technology': 'Python, FastAPI',
                    'description': 'Бізнес-логіка',
                    'kind': 'app'},
                   {'id': 'db',
                    'name': 'База даних',
                    'technology': 'PostgreSQL',
                    'description': 'Зберігає ресурси',
                    'kind': 'database'}],
    'relations': [{'from': 'student',
                   'to': 'web',
                   'description': 'Переглядає каталог',
                   'technology': 'HTTPS'},
                  {'from': 'web',
                   'to': 'api',
                   'description': 'Викликає',
                   'technology': 'JSON/HTTPS'},
                  {'from': 'api',
                   'to': 'db',
                   'description': 'Читає й записує',
                   'technology': 'SQL'},
                  {'from': 'api',
                   'to': 'accounts',
                   'description': 'Перевіряє вхід',
                   'technology': 'OIDC'}]},),
  'C4Container\n'
  '    title Каталог ресурсів: контейнери\n'
  '    Person(student, "Студент", "Переглядає каталог")\n'
  '    System_Ext(accounts, "Облікові записи коледжу", "Зовнішня система входу")\n'
  '    System_Boundary(catalog, "Каталог ресурсів") {\n'
  '        Container(web, "Вебзастосунок", "TypeScript, React", "Показує список")\n'
  '        Container(api, "API", "Python, FastAPI", "Бізнес-логіка")\n'
  '        ContainerDb(db, "База даних", "PostgreSQL", "Зберігає ресурси")\n'
  '    }\n'
  '    Rel(student, web, "Переглядає каталог", "HTTPS")\n'
  '    Rel(web, api, "Викликає", "JSON/HTTPS")\n'
  '    Rel(api, db, "Читає й записує", "SQL")\n'
  '    Rel(api, accounts, "Перевіряє вхід", "OIDC")'),
 ('validate_model',
  ({'title': 'Каталог ресурсів: контейнери',
    'scope': 'catalog',
    'people': [{'id': 'student', 'name': 'Студент', 'description': 'Переглядає каталог'}],
    'systems': [{'id': 'catalog',
                 'name': 'Каталог ресурсів',
                 'description': 'Облік обладнання',
                 'external': False},
                {'id': 'accounts',
                 'name': 'Облікові записи коледжу',
                 'description': 'Зовнішня система входу',
                 'external': True}],
    'containers': [{'id': 'web',
                    'name': 'Вебзастосунок',
                    'technology': 'TypeScript, React',
                    'description': 'Показує список',
                    'kind': 'app'},
                   {'id': 'api',
                    'name': 'API',
                    'technology': 'Python, FastAPI',
                    'description': 'Бізнес-логіка',
                    'kind': 'app'},
                   {'id': 'db',
                    'name': 'База даних',
                    'technology': 'PostgreSQL',
                    'description': 'Зберігає ресурси',
                    'kind': 'database'}],
    'relations': [{'from': 'student',
                   'to': 'web',
                   'description': 'Переглядає каталог',
                   'technology': 'HTTPS'},
                  {'from': 'web',
                   'to': 'api',
                   'description': 'Викликає',
                   'technology': 'JSON/HTTPS'},
                  {'from': 'api',
                   'to': 'db',
                   'description': 'Читає й записує',
                   'technology': 'SQL'},
                  {'from': 'api',
                   'to': 'accounts',
                   'description': 'Перевіряє вхід',
                   'technology': 'OIDC'},
                  {'from': 'api', 'to': 'ghost', 'description': 'Шукає', 'technology': 'x'}]},),
  ["Зв'язок 5: невідомий елемент ghost"])]


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
    for name in ('to_mermaid', 'validate_model'):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
