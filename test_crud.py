#!/usr/bin/env python3
"""Тестирование CRUD операций."""

import sys
import os
sys.path.insert(0, 'src')

from primitive_db.engine import run

# Тестовые команды
test_commands = [
    "help",
    "create_table users name:str age:int is_active:bool",
    "insert into users values (\"Sergei\", 28, true)",
    "select from users",
    "select from users where age = 28",
    "update users set age = 29 where name = \"Sergei\"",
    "select from users",
    "delete from users where ID = 1",
    "select from users",
    "info users",
    "exit"
]

# Мокаем input
input_index = 0
original_input = __builtins__.input

def mock_input(prompt=""):
    global input_index
    if input_index < len(test_commands):
        cmd = test_commands[input_index]
        print(f"{prompt}{cmd}")
        input_index += 1
        return cmd
    return "exit"

__builtins__.input = mock_input

print("=== ТЕСТИРОВАНИЕ CRUD ОПЕРАЦИЙ ===")
print("=" * 60)

try:
    run()
except SystemExit:
    pass
finally:
    __builtins__.input = original_input

print("=" * 60)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

# Проверяем созданные файлы
print("\nПроверка файлов:")
if os.path.exists('db_meta.json'):
    print("db_meta.json создан")
if os.path.exists('data/users.json'):
    print("data/users.json создан")
    import json
    with open('data/users.json', 'r') as f:
        data = json.load(f)
        print(f"Записей в таблице: {len(data)}")
