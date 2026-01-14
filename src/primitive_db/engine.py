#!/usr/bin/env python3
"""Engine module for the primitive database."""

import shlex
from .constants import HELP_TEXT
from .core import (
    create_table,
    drop_table,
    list_tables,
    insert,
    select,
    update,
    delete,
    info,
)
from .utils import load_metadata, save_metadata


def print_help():
    """справочная информация"""
    print(HELP_TEXT)


def run():
    """основной рабочий цикл"""
    print("\n***БАЗА ДАННЫХ***")
    print_help()

    while True:
        metadata = load_metadata()

        try:
            user_input = input(">>> Введите команду: ").strip()
            if not user_input:
                continue

            args = shlex.split(user_input)
            command = args[0].lower()

            if command == "create_table":
                if len(args) < 3:
                    print(
                        "Недостаточно аргументов. Формат: "
                        "create_table <имя> <столбец:тип> ..."
                    )
                    continue
                table_name = args[1]
                columns = args[2:]
                result = create_table(metadata, table_name, columns)
                if result is not None:
                    save_metadata(result)

            elif command == "drop_table":
                if len(args) != 2:
                    print("Неверный формат. Используйте: drop_table <имя_таблицы>")
                    continue
                table_name = args[1]
                result = drop_table(metadata, table_name)
                if result is not None:
                    save_metadata(result)

            elif command == "list_tables":
                list_tables(metadata)

            elif command == "insert":
                if (
                    len(args) < 4
                    or args[1].lower() != "into"
                    or args[3].lower() != "values"
                ):
                    print(
                        "Неверный формат. Используйте: "
                        "insert into <таблица> values (<значение1>, <значение2>, ...)"
                    )
                    continue

                table_name = args[2]
                values_str = " ".join(args[4:])

                # Используем парсер
                from .parser import parse_values

                values = parse_values(values_str)
                if values is None:
                    print("Значения должны быть в скобках.")
                    continue

                insert(metadata, table_name, values)

            elif command == "select":
                if len(args) < 3 or args[1].lower() != "from":
                    print(
                        "Неверный формат. Используйте: select from "
                        "<таблица> [where <условие>]"
                    )
                    continue

                table_name = args[2]

                if len(args) > 4 and args[3].lower() == "where":
                    where_clause = " ".join(args[4:])
                    select(metadata, table_name, where_clause)
                else:
                    select(metadata, table_name)

            elif command == "update":
                if len(args) < 6:
                    print(
                        "Неверный формат. Используйте: "
                        "update <таблица> set <столбец>=<значение> where <условие>"
                    )
                    continue

                table_name = args[1]

                # Ищем индексы set и where
                set_idx = next(
                    (i for i, arg in enumerate(args) if arg.lower() == "set"), -1
                )
                where_idx = next(
                    (i for i, arg in enumerate(args) if arg.lower() == "where"), -1
                )

                if set_idx == -1 or where_idx == -1:
                    print(
                        "Неверный формат. Используйте: update <таблица> "
                        "set <столбец>=<значение> where <условие>"
                    )
                    continue

                set_clause = " ".join(args[set_idx + 1 : where_idx])
                where_clause = " ".join(args[where_idx + 1 :])

                update(metadata, table_name, set_clause, where_clause)

            elif command == "delete":
                if len(args) < 4:
                    print(
                        "Неверный формат. Используйте: delete "
                        "from <таблица> where <условие>"
                    )
                    continue

                table_name = args[2]  # после "from"
                where_clause = " ".join(args[4:])  # после "where"

                delete(metadata, table_name, where_clause)

            elif command == "info":
                if len(args) != 2:
                    print("Неверный формат. Используйте: info <имя_таблицы>")
                    continue
                table_name = args[1]
                info(metadata, table_name)

            elif command == "help":
                print_help()

            elif command == "exit":
                print("Программа завершена. До свидания!")
                break

            else:
                print(f'Функции "{command}" нет. Попробуйте снова.')

        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}. Попробуйте снова.")
