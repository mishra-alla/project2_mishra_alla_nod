# Проект: Примитивная база данных
Консольное приложение для работы с простой базой данных с поддержкой CRUD-операций.

## Управление таблицами
**Команды:**

- `create_table` `<имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу, автоматически добавляется столбец `ID:int`
- `drop_table` `<имя_таблицы>` — удалить таблицу
- `list_tables` — показать все таблицы
- `help` — справка
- `exit` — выход

### Поддерживаемые типы данных: `int`, `str`, `bool`.

## Пример использования - Управление таблицами:


## CRUD-операции (в разработке):
**Команды:**
- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись в таблице;
- `select from <имя_таблицы>` — прочитать все записи таблицы;
- `select from <имя_таблицы> where <столбец> = <значение>` — прочитать все записи таблицы по условию;
- `update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение>` — обновить запись в таблице;
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись из таблицы по условию.

## Пример использования CRUD-операции: (в разработке)

### Примеры команд:
```
# создание записи
insert into users values ("Sergei", 28, true)

# выборка данных
select from users
select from users where age = 28
select from users where name = "Sergei"

# обновление данных
update users set age = 28 where name = "Sergei"
update users set age = 28 where name="Sergei"

# удаление данных
delete from users where ID = 1
delete from users where name = "Sergei"
```

## Обработка ошибок:
- `KeyError` - обращение к несуществующим таблицам
- `ValueError` - ошибки валидации типов данных
- `FileNotFoundError` - проблемы с файлами данных

## Архитектура проекта:
Проект состоит из следующих модулей:
- `main.py` - точка входа в приложение
- `engine.py` - парсинг команд, управление циклом, основной исполнительный файл
- `core.py` - логика работы с таблицами и данными
- `utils.py` - вспомогательные функции для работы с файлами
- `parser.py` - парсинг условий и вводимых выражений
- `decorators.py` - система декораторов

## Структура проекта:
```
project2_Mishra_Alla_nod/
├── .gitignore
├── Makefile          # Автоматизация команд
├── README.md         # Документация
├── pyproject.toml    # Конфигурация Poetry
├── poetry.lock
└── src/
    ├── __init__.py
    └── primitive_db/
        ├── __init__.py
        ├── main.py    # Точка входа с функцией main()
        ├── engine.py  # Логика работы с БД
        ├── core.py
        └── utils.py
```

## Структура данных:
- Метаданные: хранятся в db_meta.json
- Данные таблиц: каждая таблица хранится в отдельном файле в папке data

## Установка
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd project2_Mishra_Alla

# Установка зависимостей
poetry install      # через poetry
make install  # через Makefile

## Запуск
poetry run project  # через poetry
make project        # через Makefile
```
### Установка как пакет
```
bash
# Собрать пакет
make build

# Установить пакет
make package-install

# Запустить
project
```

> Убедитесь, что у вас установлены: Python 3.12 Poetry и/или make

## Автор
mishra-alla email: [allasr22@gmail.com]
