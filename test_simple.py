#!/usr/bin/env python3
"""Простой тест CRUD."""

import sys
import os
sys.path.insert(0, 'src')

from primitive_db.engine import run

# Очищаем старые данные
if os.path.exists('db_meta.json'):
    os.remove('db_meta.json')
if os.path.exists('data'):
    import shutil
    shutil.rmtree('data')

# Тестовые команды
commands = [
    "create_table users name:str age:int is_active:bool",
    "insert into users values (\"Sergei\", 28, true)",
    "select from users",
    "update users set age = 29 where name = \"Sergei\"",
    "select from users",
    "delete from users where name = \"Sergei\"",
    "select from users",
    "info users",
    "exit"
]

# Простой мок input
input_index = 0
def mock_input(prompt):
    global input_index
    if input_index < len(commands):
        cmd = commands[input_index]
        print(f"{prompt}{cmd}")
        input_index += 1
        return cmd
    return "exit"

import builtins
original_input = builtins.input
builtins.input = mock_input

print("=== ТЕСТ CRUD ===")
run()
builtins.input = original_input
print("=== ТЕСТ ЗАВЕРШЕН ===")
