# Проект: Примитивная база данных
Консольное приложение для работы с простой базой данных с поддержкой CRUD-операций.

## Управление таблицами
**Команды:**

- `create_table` `<имя> <столбец1:тип> <столбец2:тип> ...` — создать таблицу
- `list_tables` — показать все таблицы
- `drop_table` `<имя>` — удалить таблицу
- `help` — справка
- `exit` — выход

### Поддерживаемые типы данных: `int`, `str`, `bool`.

## Пример использования - Управление таблицами:
https://asciinema.org/a/ZIP55liRdUmSzN0D

## Работа с данными (CRUD):
**Команды:**
- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — создать запись;
- `select from <имя_таблицы>` — показать все записи;
- `select from <имя_таблицы> where <столбец> = <значение>` — показать все записи по условию;
- `update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение>` — обновить запись;
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись из таблицы по условию;
- `info <имя_таблицы>` - информация о таблице

## Пример использования CRUD-операции:

### Примеры команд:
```
# создание таблицы
create_table users name:str age:int is_active:bool
create_table products title:str price:int in_stock:bool

# создание записи
insert into users values ("Мария", 28, true)
insert into users values ("Анна", 25, true)
insert into users values ("Иван", 30, false)

# просмотр всех записей
select from users
select from users where age = 28

# обновление записи
update users set age = 27 where name = "Мария"

# удаление записи
delete from users where ID = 1
delete from users where name = "Мария"

# Информация о таблице
info users
```
## Реализованные декораторы:
- `@handle_db_errors` - обработка исключений ( FileNotFoundError, KeyError, ValueError)
- `@confirm_action("действие")` - запрос подтверждения для опасных операций
- `@log_time` - замер времени выполнения функций
- `create_cacher()` - фабрика функций с замыканием

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
        ├── decorators.py # Декораторы
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
