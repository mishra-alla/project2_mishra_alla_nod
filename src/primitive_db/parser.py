#!/usr/bin/env python3
"""Parser functions for the primitive database."""


def parse_values(values_str):
    """
    Парсит строку значений вида "(значение1, значение2, ...)"

    Args:
        values_str: Строка со значениями в скобках

    Returns:
        Список значений или None если формат неверный
    """
    if values_str.startswith("(") and values_str.endswith(")"):
        values_str = values_str[1:-1]
        return [v.strip() for v in values_str.split(",")]
    return None


def parse_where(where_clause):
    """
    Парсит условие WHERE вида "столбец = значение"

    Args:
        where_clause: Строка условия

    Returns:
        Кортеж (column, value) или (None, None) если формат неверный
    """
    if "=" in where_clause:
        parts = where_clause.split("=", 1)
        column = parts[0].strip()
        value = parts[1].strip()
        return column, value
    return None, None


def parse_set(set_clause):
    """
    Парсит условие SET вида "столбец = значение"

    Args:
        set_clause: Строка условия SET

    Returns:
        Кортеж (column, value) или (None, None) если формат неверный
    """
    return parse_where(set_clause)  # Та же логика
