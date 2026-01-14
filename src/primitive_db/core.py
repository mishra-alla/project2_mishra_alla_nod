#!/usr/bin/env python3
"""Core functionality for the primitive database."""

import json
import os
from prettytable import PrettyTable
from .decorators import handle_db_errors, confirm_action, log_time, query_cacher
from .constants import VALID_TYPES

@handle_db_errors
def create_table(metadata, table_name, columns):
    """создание таблицы"""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    parsed_columns = []
    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Формат: имя:тип")
            return None
        name, dtype = col.split(":", 1)
        if not name or dtype not in VALID_TYPES:
            print(
                f"Некорректное значение: {col}.\
                Тип должен быть int, str или bool."
            )
            return None
        parsed_columns.append(f"{name}:{dtype}")

    final_columns = ["ID:int"] + parsed_columns

    metadata[table_name] = final_columns
    print(
        f'Таблица "{table_name}" успешно создана'
        f" со столбцами: {', '.join(final_columns)}"
    )
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name, confirm=True):
    """
    удаление таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    del metadata[table_name]

    # Удаляем файл с данными если он существует
    data_file = f"data/{table_name}.json"
    if os.path.exists(data_file):
        os.remove(data_file)

    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
def list_tables(metadata):
    """
    список всех таблиц
    """
    if not metadata:
        print("Нет созданных таблиц.")
        return

    for table in sorted(metadata.keys()):
        print(f"- {table}")


def _load_table_data(table_name):
    """Загружает данные таблицы из файла."""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def _save_table_data(table_name, data):
    """Сохраняет данные таблицы в файл."""
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse_value(value, expected_type):
    """Парсит значение в соответствии с типом."""
    value = value.strip()

    if expected_type == "int":
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Некорректное целое число: {value}")

    elif expected_type == "bool":
        value_lower = value.lower()
        if value_lower in ("true", "1", "yes", "да"):
            return True
        elif value_lower in ("false", "0", "no", "нет"):
            return False
        else:
            raise ValueError(f"Некорректное булево значение: {value}")

    elif expected_type == "str":
        # Удаляем кавычки если они есть
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    return value


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """
    вставка данных в таблицу
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    # Загружаем текущие данные
    table_data = _load_table_data(table_name)

    # Получаем схему таблицы (без ID)
    columns_schema = metadata[table_name]
    data_columns = columns_schema[1:]  # Пропускаем ID:int

    # Проверяем количество значений
    if len(values) != len(data_columns):
        print(f"Ошибка: Ожидается {len(data_columns)} значений, получено {len(values)}")
        return None

    # Парсим значения
    parsed_values = []
    for i, value in enumerate(values):
        col_name, col_type = data_columns[i].split(":")
        try:
            parsed_value = _parse_value(value, col_type)
            parsed_values.append(parsed_value)
        except ValueError as e:
            print(f'Ошибка в значении "{value}" для столбца "{col_name}": {e}')
            return None

    # Генерируем ID
    new_id = 1
    if table_data:
        ids = [record.get("ID", 0) for record in table_data]
        if ids:
            new_id = max(ids) + 1

    # Создаём запись
    record = {"ID": new_id}
    for i, col in enumerate(data_columns):
        col_name = col.split(":")[0]
        record[col_name] = parsed_values[i]

    # Добавляем запись
    table_data.append(record)
    _save_table_data(table_name, table_data)

    # Очищаем кэш для этой таблицы
    query_cacher.clear()

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


def _parse_where(where_clause):
    """Парсит условие WHERE."""
    if "=" in where_clause:
        parts = where_clause.split("=", 1)
        column = parts[0].strip()
        value = parts[1].strip()
        return column, value
    return None, None


@handle_db_errors
@log_time
def select(metadata, table_name, where_clause=None):
    """
    выборка данных из таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    # Функция для выполнения запроса (будет кэшироваться)
    def _execute_select():
        table_data = _load_table_data(table_name)

        if not table_data:
            print(f'Таблица "{table_name}" пуста.')
            return

        # Фильтруем данные если есть условие
        filtered_data = table_data
        if where_clause:
            column, value = _parse_where(where_clause)
            if not column:
                print("Некорректное условие WHERE.")
                return

            # Определяем тип столбца для парсинга значения
            col_type = "str"
            for col_schema in metadata[table_name]:
                col_name, col_type_str = col_schema.split(":")
                if col_name == column:
                    col_type = col_type_str
                    break

            try:
                parsed_value = _parse_value(value, col_type)
            except ValueError as e:
                print(f"Ошибка в условии WHERE: {e}")
                return

            # Фильтруем записи
            filtered_data = [
                record
                for record in table_data
                if str(record.get(column, "")) == str(parsed_value)
            ]

        if not filtered_data:
            print("Записи не найдены.")
            return

        # Создаём таблицу для вывода
        table = PrettyTable()
        table.field_names = [col.split(":")[0] for col in metadata[table_name]]

        for record in filtered_data:
            row = []
            for col in metadata[table_name]:
                col_name = col.split(":")[0]
                value = record.get(col_name, "")
                if isinstance(value, bool):
                    row.append(str(value))
                else:
                    row.append(str(value))
            table.add_row(row)

        print(table)
        return filtered_data

    # Создаём ключ для кэша
    cache_key = f"select_{table_name}_{where_clause}"

    # Используем кэш
    return query_cacher(cache_key, _execute_select)


@handle_db_errors
def update(metadata, table_name, set_clause, where_clause):
    """
    обновление данных в таблице
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    table_data = _load_table_data(table_name)

    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return None

    # Парсим условия SET и WHERE
    set_column, set_value = _parse_where(set_clause)
    where_column, where_value = _parse_where(where_clause)

    if not set_column or not where_column:
        print("Некорректный формат SET или WHERE условия.")
        return None

    # Определяем типы для значений
    set_type = "str"
    where_type = "str"

    for col_schema in metadata[table_name]:
        col_name, col_type = col_schema.split(":")
        if col_name == set_column:
            set_type = col_type
        if col_name == where_column:
            where_type = col_type

    # Парсим значения
    try:
        parsed_set_value = _parse_value(set_value, set_type)
        parsed_where_value = _parse_value(where_value, where_type)
    except ValueError as e:
        print(f"Ошибка в значении: {e}")
        return None

    # Обновляем записи
    updated_count = 0
    for record in table_data:
        if str(record.get(where_column, "")) == str(parsed_where_value):
            record[set_column] = parsed_set_value
            updated_count += 1

    if updated_count == 0:
        print("Записи для обновления не найдены.")
        return None

    _save_table_data(table_name, table_data)

    # Очищаем кэш
    query_cacher.clear()

    print(f'Успешно обновлено {updated_count} записей в таблице "{table_name}".')
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(metadata, table_name, where_clause, confirm=True):
    """
    удаление данных из таблицы
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    table_data = _load_table_data(table_name)

    if not table_data:
        print(f'Таблица "{table_name}" пуста.')
        return None

    # Парсим условие WHERE
    where_column, where_value = _parse_where(where_clause)
    if not where_column:
        print("Некорректное условие WHERE.")
        return None

    # Определяем тип для значения WHERE
    where_type = "str"
    for col_schema in metadata[table_name]:
        col_name, col_type = col_schema.split(":")
        if col_name == where_column:
            where_type = col_type
            break

    # Парсим значение
    try:
        parsed_where_value = _parse_value(where_value, where_type)
    except ValueError as e:
        print(f"Ошибка в условии WHERE: {e}")
        return None

    # Удаляем записи
    filtered_data = []
    deleted_count = 0
    for record in table_data:
        if str(record.get(where_column, "")) == str(parsed_where_value):
            deleted_count += 1
        else:
            filtered_data.append(record)

    if deleted_count == 0:
        print("Записи для удаления не найдены.")
        return None

    _save_table_data(table_name, filtered_data)

    # Очищаем кэш
    query_cacher.clear()

    print(f'Успешно удалено {deleted_count} записей из таблицы "{table_name}".')
    return filtered_data


@handle_db_errors
def info(metadata, table_name):
    """
    информация о таблице
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return

    table_data = _load_table_data(table_name)

    print(f"Таблица: {table_name}")
    print(f"Столбцы: {', '.join(metadata[table_name])}")
    print(f"Количество записей: {len(table_data)}")
